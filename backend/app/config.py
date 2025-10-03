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

# Directories for BM25 values and logs.
BM25_JSON_VALUES = os.path.join(APP_DIR, "bm25_values")
LOG_DIR = os.path.join(APP_DIR, "logs")

# Ensure the directories exist.
os.makedirs(BM25_JSON_VALUES, exist_ok=True)
os.makedirs(LOG_DIR, exist_ok=True)

# Full paths for the BM25 JSON file and the application log file.
BM25_JSON_PATH = os.path.join(BM25_JSON_VALUES, "bm25_values.json")
LOG_FILE_PATH = os.path.join(LOG_DIR, "application.log")

# Pinecone Configuration
PINECONE_API_KEY = os.getenv("PINECONE_API_KEY")
PINECONE_ENV = os.getenv("PINECONE_ENV")
PINECONE_INDEX_NAME = os.getenv("PINECONE_INDEX_NAME")
PINECONE_EMBEDDING_DIMENSIONS = 3072
PINECONE_NAMESPACE = "my-namespace"

# OpenRouter Configuration (OpenAI-compatible API)
OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")
OPENROUTER_BASE_URL = os.getenv("OPENROUTER_BASE_URL", "https://openrouter.ai/api/v1")

# Model Configuration
DEFAULT_LLM_MODEL = os.getenv("DEFAULT_LLM_MODEL", "openai/gpt-4-turbo-preview")
DEFAULT_EMBEDDING_MODEL = os.getenv("DEFAULT_EMBEDDING_MODEL", "openai/text-embedding-3-large")
EMBEDDING_MODEL = DEFAULT_EMBEDDING_MODEL

# Legacy OpenAI API Key support (for backward compatibility)
# OpenRouter uses the same API key format as OpenAI
OPENAI_API_KEY = OPENROUTER_API_KEY

# Chunking Configuration
CHUNK_SIZE = 1000
CHUNK_OVERLAP = 200
CHUNK_MIN_SIZE = 100  # Minimum chunk size to prevent tiny chunks

# Pinecone Constants
TOP_K = 30  # Increased for better recall
PINECONE_METRIC = "cosine"  # Changed from dotproduct to cosine for better similarity

# RAG Constants
HYBRID_WEIGHT_RATIO = 0.7  # Higher weight for dense embeddings (semantic)
SIMILARITY_THRESHOLD = 0.65  # Adaptive threshold, will use avg in code
TEMPERATURE = 0.3  # Lower for more focused answers
MAX_TOKENS = 3000
MAX_CONTEXT_TOKENS = 8000  # Maximum tokens for context
