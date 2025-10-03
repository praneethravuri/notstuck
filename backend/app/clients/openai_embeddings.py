"""
Embedding Client Module

This module provides embeddings functionality using OpenRouter API with manual HTTP requests.
OpenRouter's embeddings response format is incompatible with OpenAI SDK parsing.
"""
import logging
from typing import List
import requests
from app.config import (
    OPENROUTER_API_KEY,
    OPENROUTER_BASE_URL,
    EMBEDDING_MODEL
)

logger = logging.getLogger(__name__)

class DirectEmbeddings:
    """
    Direct embeddings using OpenRouter API via manual HTTP requests.
    """

    def __init__(self, model: str = EMBEDDING_MODEL):
        self.model = model
        self.base_url = OPENROUTER_BASE_URL
        self.api_key = OPENROUTER_API_KEY
        logger.info(f"Embeddings initialized with model: {self.model} via OpenRouter (manual HTTP)")

    def embed_documents(self, texts: List[str]) -> List[List[float]]:
        """
        Embed a list of documents using OpenRouter.

        Args:
            texts: List of text strings to embed

        Returns:
            List of embedding vectors
        """
        try:
            url = f"{self.base_url}/embeddings"
            headers = {
                "Authorization": f"Bearer {self.api_key}",
                "Content-Type": "application/json",
                "HTTP-Referer": "https://notstuck.app",
                "X-Title": "NotStuck"
            }

            payload = {
                "model": self.model,
                "input": texts
            }

            response = requests.post(url, json=payload, headers=headers, timeout=60)
            response.raise_for_status()

            data = response.json()

            # Extract embeddings from response
            embeddings = [item["embedding"] for item in data["data"]]
            logger.debug(f"Generated {len(embeddings)} embeddings via OpenRouter")
            return embeddings

        except Exception as e:
            logger.error(f"Error generating embeddings: {e}", exc_info=True)
            raise

    def embed_query(self, text: str) -> List[float]:
        """
        Embed a single query text using OpenRouter.

        Args:
            text: Query text to embed

        Returns:
            Embedding vector
        """
        try:
            url = f"{self.base_url}/embeddings"
            headers = {
                "Authorization": f"Bearer {self.api_key}",
                "Content-Type": "application/json",
                "HTTP-Referer": "https://notstuck.app",
                "X-Title": "NotStuck"
            }

            payload = {
                "model": self.model,
                "input": [text]
            }

            response = requests.post(url, json=payload, headers=headers, timeout=60)
            response.raise_for_status()

            data = response.json()

            embedding = data["data"][0]["embedding"]
            logger.debug("Generated query embedding via OpenRouter")
            return embedding

        except Exception as e:
            logger.error(f"Error embedding query: {e}", exc_info=True)
            raise

def get_embedding_function():
    """
    Returns a direct embedding function.

    Returns:
        DirectEmbeddings: Initialized embedding function

    Raises:
        ValueError: If API key is not configured
    """
    if not OPENROUTER_API_KEY:
        logger.error("OPENROUTER_API_KEY is not set in environment variables")
        raise ValueError("OPENROUTER_API_KEY must be set in .env file")

    try:
        return DirectEmbeddings()
    except Exception as e:
        logger.error("Failed to initialize embeddings.", exc_info=True)
        raise
