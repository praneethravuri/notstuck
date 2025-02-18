import logging
from motor.motor_asyncio import AsyncIOMotorClient
from app.config import MONGODB_URI

logger = logging.getLogger(__name__)

try:
    mongodb_client = AsyncIOMotorClient(MONGODB_URI)
    logger.info("MongoDB client initialized successfully.")
except Exception as e:
    logger.error("Failed to initialize MongoDB client.", exc_info=True)
    mongodb_client = None
