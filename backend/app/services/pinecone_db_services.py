import logging
from fastapi import HTTPException
from app.vector_db.pinecone_db import delete_all_data
from app.config import PINECONE_NAMESPACE

logger = logging.getLogger(__name__)

def reset_database() -> str:
    """Resets the database by deleting all data in the configured namespace."""
    try:
        delete_all_data(namespace=PINECONE_NAMESPACE)
        logger.info("Database reset successful for namespace '%s'.", PINECONE_NAMESPACE)
        return "Database reset successful."
    except Exception as e:
        logger.error("Error resetting database for namespace '%s': %s", PINECONE_NAMESPACE, e, exc_info=True)
        raise HTTPException(status_code=500, detail=str(e))
