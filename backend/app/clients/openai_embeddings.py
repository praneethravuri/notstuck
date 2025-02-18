import logging
from langchain_community.embeddings.openai import OpenAIEmbeddings
from app.config import OPENAI_API_KEY, EMBEDDING_MODEL

logger = logging.getLogger(__name__)

def get_embedding_function():
    """Returns an OpenAI embedding callable for LangChain."""
    try:
        embedding_function = OpenAIEmbeddings(
            openai_api_key=OPENAI_API_KEY,
            model=EMBEDDING_MODEL
        )
        logger.info("OpenAI embeddings initialized successfully.")
        return embedding_function
    except Exception as e:
        logger.error("Failed to initialize OpenAI embeddings.", exc_info=True)
        return None
