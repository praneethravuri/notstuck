# backend/app/services/db.py

from motor.motor_asyncio import AsyncIOMotorClient
from datetime import datetime
from bson.objectid import ObjectId
from app.services.config import MONGODB_URI

# Create a Mongo client and get the default database.
client = AsyncIOMotorClient(MONGODB_URI)
db = client.get_database("notstuck")
chats_collection = db.get_collection("chats")

async def create_chat_session() -> str:
    """Create a new chat session document with an empty messages list."""
    chat_doc = {
        "messages": [],
        "created_at": datetime.utcnow()
    }
    result = await chats_collection.insert_one(chat_doc)
    return str(result.inserted_id)

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
    """Return a list of all chat sessions (with minimal info)."""
    chats = []
    async for chat in chats_collection.find({}):
        chat["chatId"] = str(chat["_id"])
        del chat["_id"]
        chats.append(chat)
    return chats
