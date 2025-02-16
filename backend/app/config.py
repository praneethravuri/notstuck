import os
from dotenv import load_dotenv

load_dotenv()

# Paths
APP_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
BACKEND_DIR = APP_DIR
RAW_DATA_PATH = os.path.join(BACKEND_DIR, "data", "raw")
PROCESSED_DATA_PATH = os.path.join(BACKEND_DIR, "data", "processed")

RAW_TEST_DATA_PATH = os.path.join(BACKEND_DIR, "test_data", "raw")
PROCESSED_TEST_DATA_PATH = os.path.join(BACKEND_DIR, "test_data", "processed")

# MongoDB
MONGODB_URI = os.getenv("MONGODB_URI")
MONGO_DATABASE_NAME = "unstuck"
MONGO_COLLECTION_NAME = "chats"

# Pinecone
PINECONE_API_KEY = os.getenv("PINECONE_API_KEY")
PINECONE_ENV = os.getenv("PINECONE_ENV")
PINECONE_INDEX_NAME = os.getenv("PINECONE_INDEX_NAME")
PINECONE_EMBEDDING_DIMENSIONS = 3072
PINECONE_NAMESPACE = "my-namespace"

# OpenAI
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
EMBEDDING_MODEL = "text-embedding-3-large"

# Embedding Dimensions
CHUNK_SIZE = 750
CHUNK_OVERLAP = 100

# Match threshold
SIMILARITY_THRESHOLD = 0.1
EXACT_MATCH_THRESHOLD = 0.1
