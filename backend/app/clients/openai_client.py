"""
LLM Client Module

This module provides a unified OpenAI-compatible client that can work with:
- OpenAI API
- OpenRouter API (for multi-model support)
- Any other OpenAI-compatible API

The client is initialized based on the OPENROUTER_API_KEY and OPENROUTER_BASE_URL
environment variables.
"""
import logging
from openai import OpenAI
from app.config import OPENROUTER_API_KEY, OPENROUTER_BASE_URL

logger = logging.getLogger(__name__)

def get_llm_client() -> OpenAI:
    """
    Returns an initialized OpenAI-compatible client.

    This client can connect to OpenRouter or any OpenAI-compatible API
    based on the configuration in the .env file.

    Returns:
        OpenAI: Initialized OpenAI client instance

    Raises:
        ValueError: If API key is not configured
    """
    if not OPENROUTER_API_KEY:
        logger.error("OPENROUTER_API_KEY is not set in environment variables")
        raise ValueError("OPENROUTER_API_KEY must be set in .env file")

    try:
        client = OpenAI(
            api_key=OPENROUTER_API_KEY,
            base_url=OPENROUTER_BASE_URL
        )
        logger.info(f"LLM client initialized successfully with base_url: {OPENROUTER_BASE_URL}")
        return client
    except Exception as e:
        logger.error("Failed to initialize LLM client.", exc_info=True)
        raise

# Initialize the global client instance
try:
    openai_client = get_llm_client()
except Exception as e:
    logger.error("Failed to initialize global LLM client.", exc_info=True)
    openai_client = None
