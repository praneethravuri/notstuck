import os
from dotenv import load_dotenv
from langchain_community.embeddings.openai import OpenAIEmbeddings
from backend.config import OPENAI_API_KEY, EMBEDDING_MODEL

load_dotenv()

def get_embedding_function():
    """Returns an OpenAI embedding callable for LangChain."""
    return OpenAIEmbeddings(
        openai_api_key=OPENAI_API_KEY,
        model="text-embedding-ada-002"
    )

