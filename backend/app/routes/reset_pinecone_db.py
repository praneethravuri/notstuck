# app/routes/reset_db.py

import logging
from fastapi import APIRouter
from app.services.pinecone_db_services import reset_database

router = APIRouter()
logger = logging.getLogger(__name__)

@router.delete("/reset-pinecone-db")
def reset_db():
    logger.info("Reset DB route accessed")
    try:
        result = reset_database()
        logger.info("Database reset successfully")
        return result
    except Exception as e:
        logger.error("Error resetting Pinecone DB: %s", e, exc_info=True)
        raise
