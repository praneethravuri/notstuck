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
    relevant_chunks = []
    sources_metadata = []
    print(f"\n\n\nMATCHES: {matches}")
    for match in matches:
        metadata = match.get("metadata", {})
        text_content = metadata.get("text", "")
        source_file = metadata.get("source_file", "unknown source")
        page_number = metadata.get("page_number", None)
            
        relevant_chunks.append(text_content)

        sources_metadata.append({
            "source_file": source_file,
            "page_number": page_number,
        })

    return relevant_chunks, sources_metadata

