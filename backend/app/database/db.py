# backend/app/services/db.py

import logging
from datetime import datetime
from bson.objectid import ObjectId
from fastapi import HTTPException
from app.clients.mongodb_client import mongodb_client
from app.config import MONGO_DATABASE_NAME, MONGO_COLLECTION_NAME

logger = logging.getLogger(__name__)

# Use the shared MongoDB client instance to get the default database.
db = mongodb_client.get_database(MONGO_DATABASE_NAME)
chats_collection = db.get_collection(MONGO_COLLECTION_NAME)

async def create_chat_session(chat_name: str = None) -> dict:
    if chat_name is None:
        # Optionally, you could generate a basic default name here
        chat_name = f"Chat {datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S')}"
    chat_doc = {
        "name": chat_name,
        "messages": [],
        "created_at": datetime.utcnow()
    }
    try:
        result = await chats_collection.insert_one(chat_doc)
        logger.info(f"Chat session created with id: {result.inserted_id}")
        return {"chatId": str(result.inserted_id), "name": chat_name}
    except Exception as e:
        logger.error(f"Error creating chat session: {e}", exc_info=True)
        raise HTTPException(
            status_code=500, detail=f"Error creating chat session: {e}"
        )

async def append_message_to_chat(chat_id: str, message: dict) -> int:
    """Append a message (with a timestamp) to the chat session identified by chat_id."""
    message["timestamp"] = datetime.utcnow()
    try:
        result = await chats_collection.update_one(
            {"_id": ObjectId(chat_id)},
            {"$push": {"messages": message}}
        )
        logger.info(f"Appended message to chat with id: {chat_id}")
        return result.modified_count
    except Exception as e:
        logger.error(f"Error appending message to chat {chat_id}: {e}", exc_info=True)
        raise HTTPException(
            status_code=500, detail=f"Error appending message to chat {chat_id}: {e}"
        )

async def get_chat_by_id(chat_id: str) -> dict:
    """Retrieve a single chat session by its ID."""
    try:
        chat = await chats_collection.find_one({"_id": ObjectId(chat_id)})
        if chat:
            chat["chatId"] = str(chat["_id"])
            del chat["_id"]
            logger.info(f"Retrieved chat with id: {chat_id}")
        else:
            logger.info(f"No chat found with id: {chat_id}")
        return chat
    except Exception as e:
        logger.error(f"Error retrieving chat with id {chat_id}: {e}", exc_info=True)
        raise HTTPException(
            status_code=500, detail=f"Error retrieving chat: {e}"
        )

async def get_all_chats() -> list:
    """Return a list of all chat sessions, sorted by creation date (latest first)."""
    chats = []
    try:
        async for chat in chats_collection.find({}).sort("created_at", -1):
            chat["chatId"] = str(chat["_id"])
            del chat["_id"]
            chats.append(chat)
        logger.info(f"Retrieved {len(chats)} chat sessions.")
        return chats
    except Exception as e:
        logger.error(f"Error retrieving all chats: {e}", exc_info=True)
        raise HTTPException(
            status_code=500, detail=f"Error retrieving chats: {e}"
        )
