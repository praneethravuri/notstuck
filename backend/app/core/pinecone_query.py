# app/core/pinecone_query.py
import logging
from app.clients.pinecone_client import pinecone_index

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
        logger.error(f"Error querying Pinecone: {e}", exc_info=True)
        raise

def filter_matches(matches, threshold: float):
    """
    Filter matches from the query results based on a threshold and return relevant text content and sources metadata.
    """
    relevant_chunks = []
    sources_metadata = []
    
    # Log the matches at debug level instead of printing to the console.
    logger.debug(f"Filtering matches: {matches}")
    
    try:
        for match in matches:
            metadata = match.get("metadata", {})
            text_content = metadata.get("text", "")
            source_file = metadata.get("source_file", "unknown source")
            page_number = metadata.get("page_number", None)
            
            # Here, you could filter based on the threshold if necessary.
            relevant_chunks.append(text_content)
            sources_metadata.append({
                "source_file": source_file,
                "page_number": page_number,
            })
    
        return relevant_chunks, sources_metadata
    except Exception as e:
        logger.error(f"Error filtering matches: {e}", exc_info=True)
        raise
