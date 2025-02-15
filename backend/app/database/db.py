# backend/app/services/db.py

from datetime import datetime
from bson.objectid import ObjectId
from fastapi import HTTPException
from app.clients import mongodb_client
from app.config import MONGO_DATABASE_NAME, MONGO_COLLECTION_NAME

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
        return {"chatId": str(result.inserted_id), "name": chat_name}
    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Error creating chat session: {e}")


async def append_message_to_chat(chat_id: str, message: dict) -> int:
    """Append a message (with a timestamp) to the chat session identified by chat_id."""
    message["timestamp"] = datetime.utcnow()
    result = await chats_collection.update_one(
        {"_id": ObjectId(chat_id)},
        {"$push": {"messages": message}}
    )
    return result.modified_count


async def get_chat_by_id(chat_id: str) -> dict:
    """Retrieve a single chat session by its ID."""
    chat = await chats_collection.find_one({"_id": ObjectId(chat_id)})
    if chat:
        chat["chatId"] = str(chat["_id"])
        del chat["_id"]
    return chat


async def get_all_chats() -> list:
    """Return a list of all chat sessions, sorted by creation date (latest first)."""
    chats = []
    async for chat in chats_collection.find({}).sort("created_at", -1):
        chat["chatId"] = str(chat["_id"])
        del chat["_id"]
        chats.append(chat)
    return chats
