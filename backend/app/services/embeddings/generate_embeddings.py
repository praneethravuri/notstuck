import os
from dotenv import load_dotenv
from langchain_community.embeddings.openai import OpenAIEmbeddings
from ..config import OPENAI_API_KEY, EMBEDDING_MODEL

def get_embedding_function():
    """Returns an OpenAI embedding callable for LangChain."""
    return OpenAIEmbeddings(
        openai_api_key=OPENAI_API_KEY,
        model=EMBEDDING_MODEL
    )

