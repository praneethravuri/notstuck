import logging
from typing import Dict, List, Optional
from app.config import TOP_K, SIMILARITY_THRESHOLD
from app.clients.pinecone_client import pinecone_index

logger = logging.getLogger(__name__)

def retrieve_matches(weighted_dense: List[float], weighted_sparse: Dict, filter_criteria: Optional[Dict], namespace: str) -> List[Dict]:
    """
    Query Pinecone using the weighted dense and sparse vectors.
    """
    query_response = pinecone_index.query(
        top_k=TOP_K,
        vector=weighted_dense,
        sparse_vector=weighted_sparse,
        namespace=namespace,
        filter=filter_criteria,
        include_metadata=True
    )
    return query_response.get("matches", [])

def filter_matches_by_threshold(matches: List[Dict]) -> List[Dict]:
    """
    Filter matches to include only those with a score above the SIMILARITY_THRESHOLD.
    """
    return [m for m in matches if m["score"] >= SIMILARITY_THRESHOLD]
