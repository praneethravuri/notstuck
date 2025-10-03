import os
from pinecone import Pinecone, ServerlessSpec
from typing import Optional


class PineconeClient:
    """Client for Pinecone vector database operations."""

    _instance: Optional['PineconeClient'] = None

    def __init__(self):
        """Initialize Pinecone client with environment variables."""
        self.api_key = os.getenv("PINECONE_API_KEY")
        self.environment = os.getenv("PINECONE_ENV", "us-east-1")
        self.index_name = os.getenv("PINECONE_INDEX_NAME", "notstuck-index")

        if not self.api_key:
            raise ValueError("PINECONE_API_KEY not found in environment variables")

        # Initialize Pinecone
        self.pc = Pinecone(api_key=self.api_key)
        self.index = None

    @classmethod
    def get_instance(cls) -> 'PineconeClient':
        """Get singleton instance of PineconeClient."""
        if cls._instance is None:
            cls._instance = cls()
        return cls._instance

    def get_or_create_index(self, dimension: int = 1024, metric: str = "dotproduct"):
        """
        Get existing index or create new one if it doesn't exist.

        Args:
            dimension: Embedding dimension (default 1024 to match index)
            metric: Distance metric (dotproduct as specified)
        """
        # Check if index exists
        existing_indexes = self.pc.list_indexes()
        index_names = [idx.name for idx in existing_indexes]

        if self.index_name not in index_names:
            # Create index if it doesn't exist
            self.pc.create_index(
                name=self.index_name,
                dimension=dimension,
                metric=metric,
                spec=ServerlessSpec(
                    cloud='aws',
                    region=self.environment
                )
            )

        # Connect to index
        self.index = self.pc.Index(self.index_name)
        return self.index

    def get_index(self):
        """Get the current index connection."""
        if self.index is None:
            self.index = self.pc.Index(self.index_name)
        return self.index


# Convenience function to get client instance
def get_pinecone_client() -> PineconeClient:
    """Get singleton instance of PineconeClient."""
    return PineconeClient.get_instance()
