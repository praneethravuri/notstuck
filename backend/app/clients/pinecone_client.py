import logging
from pinecone import Pinecone, ServerlessSpec
from app.config import (
    PINECONE_API_KEY,
    PINECONE_ENV,
    PINECONE_INDEX_NAME,
    PINECONE_EMBEDDING_DIMENSIONS,
    PINECONE_METRIC
)

logger = logging.getLogger(__name__)

# Initialize the Pinecone client
try:
    pinecone_client = Pinecone(api_key=PINECONE_API_KEY)
    logger.info("Pinecone client initialized successfully.")
except Exception as e:
    logger.error("Failed to initialize Pinecone client.", exc_info=True)
    pinecone_client = None

if pinecone_client is not None:
    # Check for the existing indexes
    try:
        existing_indexes = [idx.name for idx in pinecone_client.list_indexes()]
        logger.info("Retrieved existing Pinecone indexes.")
    except Exception as e:
        logger.error("Failed to list Pinecone indexes.", exc_info=True)
        existing_indexes = []

    # Create index if it doesn't exist
    if PINECONE_INDEX_NAME not in existing_indexes:
        try:
            pinecone_client.create_index(
                name=PINECONE_INDEX_NAME,
                dimension=PINECONE_EMBEDDING_DIMENSIONS,
                metric=PINECONE_METRIC,
                spec=ServerlessSpec(region=PINECONE_ENV, cloud="aws")
            )
            logger.info(f"Created Pinecone index '{PINECONE_INDEX_NAME}' with metric='{PINECONE_METRIC}'.")
        except Exception as e:
            logger.error(f"Failed to create Pinecone index {PINECONE_INDEX_NAME}.", exc_info=True)
    else:
        logger.info(f"Using existing Pinecone index '{PINECONE_INDEX_NAME}'. Note: If you changed PINECONE_METRIC, you need to recreate the index.")

    # Get the index object
    try:
        pinecone_index = pinecone_client.Index(PINECONE_INDEX_NAME)
        logger.info(f"Retrieved Pinecone index: {PINECONE_INDEX_NAME}.")
    except Exception as e:
        logger.error(f"Failed to get Pinecone index {PINECONE_INDEX_NAME}.", exc_info=True)
        pinecone_index = None
else:
    pinecone_index = None
