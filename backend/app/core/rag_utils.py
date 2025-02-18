import logging
from typing import Dict, List, Optional, Tuple
from pinecone_text.sparse import BM25Encoder
from app.utils.text_cleaning import clean_text
from app.config import BM25_JSON_PATH, HYBRID_WEIGHT_RATIO

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

def build_context_text(filtered_matches: List[Dict]) -> Tuple[str, List[str]]:
    """
    Build the context text and list of context chunks from the filtered matches.
    """
    context_chunks = [
        clean_text(match["metadata"].get("text", ""))
        for match in filtered_matches if match.get("metadata", {}).get("text")
    ]
    context_text = "\n\n---\n\n".join(context_chunks)
    return context_text, context_chunks
