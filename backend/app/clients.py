# app/clients.py
import os
from openai import OpenAI
from pinecone import Pinecone, ServerlessSpec
from motor.motor_asyncio import AsyncIOMotorClient
from app.config import (
    OPENAI_API_KEY,
    PINECONE_API_KEY,
    PINECONE_ENV,
    MONGODB_URI,
    PINECONE_INDEX_NAME,
    PINECONE_EMBEDDING_DIMENSIONS
)
import nltk

nltk.download('punkt')
nltk.download('stopwords')
nltk.download('wordnet')

# --- Initialize OpenAI Client ---
openai_client = OpenAI(api_key=OPENAI_API_KEY)

# --- Initialize Pinecone Client & Index ---
pinecone_client = Pinecone(api_key=PINECONE_API_KEY)
existing_indexes = [idx.name for idx in pinecone_client.list_indexes()]
if PINECONE_INDEX_NAME not in existing_indexes:
    pinecone_client.create_index(
        name=PINECONE_INDEX_NAME,
        dimension=PINECONE_EMBEDDING_DIMENSIONS,
        metric="cosine",
        spec=ServerlessSpec(region=PINECONE_ENV, cloud="aws")
    )
pinecone_index = pinecone_client.Index(PINECONE_INDEX_NAME)

# --- Initialize MongoDB Client ---
mongodb_client = AsyncIOMotorClient(MONGODB_URI)
