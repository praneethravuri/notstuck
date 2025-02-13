from openai import OpenAI
from ..vector_search_db.pinecone_db import PineconeDB
from langchain_community.retrievers import BM25Retriever
from langchain.memory import ConversationBufferWindowMemory
from langchain_community.chat_message_histories import ChatMessageHistory
from ..config import (
    PINECONE_API_KEY,
    PINECONE_ENV,
    PINECONE_INDEX_NAME,
    PINECONE_EMBEDDING_DIMENSIONS,
    OPENAI_API_KEY
)
from ..utils.embedding_provider import OpenAIEmbeddingProvider

client = OpenAI()
client.api_key = OPENAI_API_KEY