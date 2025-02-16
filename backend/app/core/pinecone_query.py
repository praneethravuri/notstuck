# app/core/pinecone_query.py
import logging
from app.clients import pinecone_index

logger = logging.getLogger(__name__)


def query_vector(vector, top_k: int, namespace: str, subject_filter: str = None):
    """
    Query the Pinecone index using the provided vector.
    """
    query_params = {
        "vector": vector,
        "top_k": top_k,
        "include_metadata": True,
        "namespace": namespace,
    }
    if subject_filter:
        query_params["filter"] = {
            "subjects": {"$in": [subject_filter.lower().strip()]}
        }
    try:
        response = pinecone_index.query(**query_params)
        return response.get("matches", [])
    except Exception as e:
        logger.error(f"Error querying Pinecone: {e}")
        raise e


def filter_matches(matches, threshold: float):
    """
    Filter matches based on the threshold score.
    """
    relevant_chunks = []
    source_files = []
    for match in matches:
        if match.get("score", 0) >= threshold:
            relevant_chunks.append(match.get("metadata", {}).get("text", ""))
            source_files.append(match.get("metadata", {}).get(
                "source_file", "unknown source"))
    return relevant_chunks, source_files
