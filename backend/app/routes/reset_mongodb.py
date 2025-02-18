# app/routes/reset_mongodb.py

import logging
from fastapi import APIRouter, HTTPException
from app.database.db import db, MONGO_COLLECTION_NAME

router = APIRouter()
logger = logging.getLogger(__name__)

@router.delete("/reset-mongodb")
async def reset_mongodb():
    """
    Resets the MongoDB chat collection by dropping it.
    """
    try:
        collection = db.get_collection(MONGO_COLLECTION_NAME)
        await collection.drop()
        logger.info("MongoDB collection '%s' dropped successfully.", MONGO_COLLECTION_NAME)
        # Optionally, recreate the collection if you have initial indexes or settings to apply.
        # For example:
        # new_collection = db.create_collection(MONGO_COLLECTION_NAME)
        # logger.info("MongoDB collection '%s' recreated.", MONGO_COLLECTION_NAME)
        return {"message": "MongoDB reset successful."}
    except Exception as e:
        logger.error("Error resetting MongoDB: %s", e, exc_info=True)
        raise HTTPException(status_code=500, detail="Error resetting MongoDB.")
