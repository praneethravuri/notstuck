# backend/app/routes/chats.py

import logging
from fastapi import APIRouter, HTTPException
from app.database.db import get_all_chats, get_chat_by_id

router = APIRouter()
logger = logging.getLogger(__name__)

@router.get("/chats")
async def list_chats():
    """Return a list of all chat sessions."""
    try:
        chats = await get_all_chats()
        logger.info("Retrieved %d chat sessions.", len(chats))
        return chats
    except Exception as e:
        logger.error("Error listing chats: %s", e, exc_info=True)
        raise HTTPException(status_code=500, detail="Error retrieving chats.")

@router.get("/chats/{chat_id}")
async def get_chat(chat_id: str):
    """Return the conversation history for a specific chat session."""
    try:
        chat = await get_chat_by_id(chat_id)
        if not chat:
            logger.warning("Chat session not found for id: %s", chat_id)
            raise HTTPException(status_code=404, detail="Chat session not found")
        logger.info("Retrieved chat session for id: %s", chat_id)
        return chat
    except Exception as e:
        logger.error("Error retrieving chat with id %s: %s", chat_id, e, exc_info=True)
        raise HTTPException(status_code=500, detail="Error retrieving chat session.")
