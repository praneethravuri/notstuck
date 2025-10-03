import logging
import numpy as np
from typing import Dict, List, Optional
from app.config import TOP_K, SIMILARITY_THRESHOLD
from app.clients.pinecone_client import pinecone_index

logger = logging.getLogger(__name__)

def retrieve_matches(weighted_dense: List[float], weighted_sparse: Dict, filter_criteria: Optional[Dict], namespace: str) -> List[Dict]:
    """
    Query Pinecone using the weighted dense and sparse vectors.
    Returns raw matches from Pinecone.
    """
    query_response = pinecone_index.query(
        top_k=TOP_K,
        vector=weighted_dense,
        sparse_vector=weighted_sparse,
        namespace=namespace,
        filter=filter_criteria,
        include_metadata=True
    )
    matches = query_response.get("matches", [])
    logger.info(f"Retrieved {len(matches)} matches from Pinecone")
    return matches

def filter_matches_by_threshold(matches: List[Dict]) -> List[Dict]:
    """
    Advanced filtering strategy using adaptive thresholding.

    Strategy:
    1. Use statistical analysis (mean + std dev) for better threshold
    2. Ensure minimum quality by combining with absolute threshold
    3. Keep at least top matches even if below threshold
    """
    if not matches:
        logger.warning("No matches to filter")
        return []

    scores = [m["score"] for m in matches]

    # Calculate statistics
    mean_score = np.mean(scores)
    std_score = np.std(scores)

    # Adaptive threshold: mean - 0.5*std, but not below absolute minimum
    adaptive_threshold = max(mean_score - 0.5 * std_score, SIMILARITY_THRESHOLD)

    logger.info(f"Score statistics - Mean: {mean_score:.4f}, Std: {std_score:.4f}, Threshold: {adaptive_threshold:.4f}")

    # Filter by adaptive threshold
    filtered = [m for m in matches if m["score"] >= adaptive_threshold]

    # Ensure we keep at least top 3 matches if available, even if below threshold
    if len(filtered) < 3 and len(matches) >= 3:
        logger.info(f"Keeping top 3 matches despite low scores")
        filtered = sorted(matches, key=lambda x: x["score"], reverse=True)[:3]

    logger.info(f"Filtered to {len(filtered)} matches (from {len(matches)})")
    return filtered

def rerank_matches(matches: List[Dict], query_embedding: List[float]) -> List[Dict]:
    """
    Rerank matches using additional similarity computation.
    This provides a second-pass refinement of results.

    Args:
        matches: Initial matches from Pinecone
        query_embedding: The dense query embedding

    Returns:
        Reranked matches
    """
    if not matches:
        return matches

    # For now, return matches as-is since Pinecone already provides good scores
    # This is a placeholder for future enhancements like cross-encoder reranking
    logger.debug(f"Reranking {len(matches)} matches")
    return matches
