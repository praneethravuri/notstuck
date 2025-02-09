import os
from dotenv import load_dotenv

load_dotenv()
# Paths
BASE_DIR = os.path.dirname(os.path.dirname(__file__))
RAW_DATA_PATH = os.path.join(BASE_DIR, "data", "raw")
PROCESSED_DATA_PATH = os.path.join(BASE_DIR, "data", "processed")

# API Keys
PINECONE_API_KEY = os.getenv("PINECONE_API_KEY")
PINECONE_ENV = os.getenv("PINECONE_ENV")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
PINECONE_INDEX_NAME = os.getenv("PINECONE_INDEX_NAME")

# Embedding Dimensions
PINECONE_EMBEDDING_DIMENSIONS = 1536

CHUNK_SIZE = 1000
CHUNK_OVERLAP = 150
EMBEDDING_MODEL = "text-embedding-3-small"

SIMILARITY_THRESHOLD = 0.99999  # 99.999% similar
EXACT_MATCH_THRESHOLD = 1.0     # 100% similar