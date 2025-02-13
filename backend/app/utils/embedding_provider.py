from langchain_community.embeddings.openai import OpenAIEmbeddings
from ..config import OPENAI_API_KEY, EMBEDDING_MODEL

class OpenAIEmbeddingProvider:
    def __init__(self, api_key: str = OPENAI_API_KEY, model: str = None):
        """
        Initializes the embedding provider with the OpenAI API key and model name.
        If no model is provided, defaults to "text-embedding-ada-002".
        """
        self.api_key = api_key
        self.model = model or "text-embedding-ada-002"
        self.embedding_instance = OpenAIEmbeddings(openai_api_key=self.api_key, model=self.model)

    def get_embedding_function(self) -> OpenAIEmbeddings:
        """
        Returns the OpenAI embedding callable instance.
        """
        return self.embedding_instance
