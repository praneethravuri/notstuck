import logging
from typing import Dict, List, Optional, Tuple
from pinecone_text.sparse import BM25Encoder
from app.utils.text_cleaning import clean_text
from app.config import BM25_JSON_PATH, HYBRID_WEIGHT_RATIO, MAX_CONTEXT_TOKENS

logger = logging.getLogger(__name__)

def load_bm25_encoder(json_path: str = BM25_JSON_PATH) -> BM25Encoder:
    """
    Load the BM25 encoder from a JSON file, or fallback to the default encoder if loading fails.
    """
    try:
        encoder = BM25Encoder().load(json_path)
        logger.info(f"Loaded BM25 encoder state from {json_path}")
    except Exception as e:
        logger.error(f"Error loading BM25 state: {e}. Using default encoder.", exc_info=True)
        encoder = BM25Encoder().default()
    return encoder

def hybrid_score_norm(dense: List[float], sparse: Dict, alpha: float = HYBRID_WEIGHT_RATIO) -> Tuple[List[float], Dict]:
    """
    Normalize hybrid scores by applying a convex weighting.
    """
    if alpha < 0 or alpha > 1:
        raise ValueError("Alpha must be between 0 and 1")
    hsparse = {
        'indices': sparse['indices'],
        'values': [v * (1 - alpha) for v in sparse['values']]
    }
    hdense = [v * alpha for v in dense]
    return hdense, hsparse

def generate_queries(question: str) -> Tuple[List[float], Dict]:
    """
    Generate dense and sparse query vectors for the given question.
    """
    from app.clients.openai_embeddings import get_embedding_function
    dense_embedding_func = get_embedding_function()
    dense_query = dense_embedding_func.embed_query(question)
    bm25_encoder = load_bm25_encoder()
    sparse_query_list = bm25_encoder.encode_documents([question])
    sparse_query = sparse_query_list[0] if sparse_query_list else BM25Encoder().default()
    return dense_query, sparse_query

def apply_hybrid_weighting(dense_query: List[float], sparse_query: Dict) -> Tuple[List[float], Dict]:
    """
    Apply hybrid weighting to the dense and sparse query vectors.
    """
    return hybrid_score_norm(dense_query, sparse_query)

def build_filter(subject_filter: Optional[str]) -> Optional[Dict]:
    """
    Build the Pinecone filter if a subject_filter is provided.
    """
    if subject_filter:
        return {"subjects": {"$in": [subject_filter.lower().strip()]}}
    return None

def deduplicate_chunks(chunks: List[str], similarity_threshold: float = 0.85) -> List[str]:
    """
    Remove duplicate or highly similar chunks based on text overlap.

    Args:
        chunks: List of text chunks
        similarity_threshold: Threshold for considering chunks as duplicates (0-1)

    Returns:
        Deduplicated list of chunks
    """
    if not chunks:
        return []

    def calculate_jaccard_similarity(text1: str, text2: str) -> float:
        """Calculate Jaccard similarity between two texts."""
        words1 = set(text1.lower().split())
        words2 = set(text2.lower().split())
        if not words1 or not words2:
            return 0.0
        intersection = len(words1.intersection(words2))
        union = len(words1.union(words2))
        return intersection / union if union > 0 else 0.0

    deduplicated = []
    for chunk in chunks:
        is_duplicate = False
        for existing_chunk in deduplicated:
            similarity = calculate_jaccard_similarity(chunk, existing_chunk)
            if similarity >= similarity_threshold:
                logger.debug(f"Removing duplicate chunk (similarity: {similarity:.2f})")
                is_duplicate = True
                break
        if not is_duplicate:
            deduplicated.append(chunk)

    logger.info(f"Deduplication: {len(chunks)} -> {len(deduplicated)} chunks")
    return deduplicated

def estimate_tokens(text: str) -> int:
    """
    Rough estimation of token count (approximately 4 characters per token).

    Args:
        text: Input text

    Returns:
        Estimated token count
    """
    return len(text) // 4

def truncate_context(chunks: List[str], max_tokens: int = MAX_CONTEXT_TOKENS) -> List[str]:
    """
    Intelligently truncate context to fit within token limit.
    Prioritizes earlier chunks (higher relevance) while respecting token limits.

    Args:
        chunks: List of context chunks (ordered by relevance)
        max_tokens: Maximum tokens allowed

    Returns:
        Truncated list of chunks
    """
    truncated = []
    total_tokens = 0

    for chunk in chunks:
        chunk_tokens = estimate_tokens(chunk)
        if total_tokens + chunk_tokens <= max_tokens:
            truncated.append(chunk)
            total_tokens += chunk_tokens
        else:
            logger.info(f"Context truncated at {len(truncated)} chunks ({total_tokens} tokens)")
            break

    return truncated

def build_context_text(filtered_matches: List[Dict]) -> Tuple[str, List[str]]:
    """
    Build optimized context text with deduplication and truncation.

    Process:
    1. Extract and clean text from matches
    2. Deduplicate similar chunks
    3. Truncate to fit token limits
    4. Build final context string

    Args:
        filtered_matches: Filtered Pinecone matches

    Returns:
        Tuple of (context_text, context_chunks)
    """
    # Extract and clean chunks
    raw_chunks = [
        clean_text(match["metadata"].get("text", ""))
        for match in filtered_matches
        if match.get("metadata", {}).get("text")
    ]

    if not raw_chunks:
        logger.warning("No text content found in matches")
        return "", []

    # Deduplicate
    deduplicated_chunks = deduplicate_chunks(raw_chunks)

    # Truncate to token limit
    final_chunks = truncate_context(deduplicated_chunks)

    # Build context text with clear separators
    context_text = "\n\n---\n\n".join(final_chunks)

    logger.info(f"Built context: {len(final_chunks)} chunks, ~{estimate_tokens(context_text)} tokens")

    return context_text, final_chunks
