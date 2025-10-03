import os
from openai import OpenAI
from typing import List, Optional


class OpenAIClient:
    """Client for OpenAI API operations."""

    _instance: Optional['OpenAIClient'] = None

    def __init__(self):
        """Initialize OpenAI client with environment variables."""
        self.api_key = os.getenv("OPENAI_API_KEY")
        self.embedding_model = os.getenv("DEFAULT_EMBEDDING_MODEL", "text-embedding-3-large")
        # Dimension for embeddings (1024 to match Pinecone index)
        self.embedding_dimension = int(os.getenv("EMBEDDING_DIMENSION", "1024"))

        if not self.api_key:
            raise ValueError("OPENAI_API_KEY not found in environment variables")

        # Initialize OpenAI client
        self.client = OpenAI(api_key=self.api_key)

    @classmethod
    def get_instance(cls) -> 'OpenAIClient':
        """Get singleton instance of OpenAIClient."""
        if cls._instance is None:
            cls._instance = cls()
        return cls._instance

    def create_embedding(self, text: str, model: Optional[str] = None) -> List[float]:
        """
        Create embedding for a single text.

        Args:
            text: Text to embed
            model: Embedding model to use (defaults to DEFAULT_EMBEDDING_MODEL)

        Returns:
            List of embedding values
        """
        model = model or self.embedding_model
        response = self.client.embeddings.create(
            input=text,
            model=model,
            dimensions=self.embedding_dimension
        )
        return response.data[0].embedding

    def create_embeddings(self, texts: List[str], model: Optional[str] = None) -> List[List[float]]:
        """
        Create embeddings for multiple texts.

        Args:
            texts: List of texts to embed
            model: Embedding model to use (defaults to DEFAULT_EMBEDDING_MODEL)

        Returns:
            List of embedding vectors
        """
        model = model or self.embedding_model
        response = self.client.embeddings.create(
            input=texts,
            model=model,
            dimensions=self.embedding_dimension
        )
        return [item.embedding for item in response.data]


# Convenience function to get client instance
def get_openai_client() -> OpenAIClient:
    """Get singleton instance of OpenAIClient."""
    return OpenAIClient.get_instance()
