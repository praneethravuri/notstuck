"""
Embedding Client Module

This module provides embeddings functionality using OpenAI-compatible APIs.
It supports OpenRouter and other OpenAI-compatible embedding services.
"""
import logging
from langchain_community.embeddings.openai import OpenAIEmbeddings
from app.config import (
    OPENROUTER_API_KEY,
    OPENROUTER_BASE_URL,
    EMBEDDING_MODEL
)

logger = logging.getLogger(__name__)

def get_embedding_function():
    """
    Returns an OpenAI-compatible embedding function for LangChain.

    This function initializes embeddings that work with:
    - OpenAI API
    - OpenRouter API
    - Any OpenAI-compatible embedding service

    Returns:
        OpenAIEmbeddings: Initialized embedding function

    Raises:
        ValueError: If API key is not configured
    """
    if not OPENROUTER_API_KEY:
        logger.error("OPENROUTER_API_KEY is not set in environment variables")
        raise ValueError("OPENROUTER_API_KEY must be set in .env file")

    try:
        # Configure OpenAIEmbeddings to work with OpenRouter or other compatible APIs
        embedding_function = OpenAIEmbeddings(
            openai_api_key=OPENROUTER_API_KEY,
            openai_api_base=OPENROUTER_BASE_URL,
            model=EMBEDDING_MODEL
        )
        logger.info(f"Embeddings initialized successfully with model: {EMBEDDING_MODEL}")
        logger.info(f"Using base URL: {OPENROUTER_BASE_URL}")
        return embedding_function
    except Exception as e:
        logger.error("Failed to initialize embeddings.", exc_info=True)
        raise
