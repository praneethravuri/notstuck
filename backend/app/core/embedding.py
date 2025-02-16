# app/core/embedding.py
import logging
from app.utils.generate_embeddings import get_embedding_function

logger = logging.getLogger(__name__)


def embed_question(question: str):
    """
    Embed the user question using the configured embedding function.
    """
    embedding_func = get_embedding_function()
    try:
        return embedding_func.embed_query(question)
    except Exception as e:
        logger.error(f"Error embedding question: {e}")
        raise e
