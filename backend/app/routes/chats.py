# backend/app/routes/chats.py

from fastapi import APIRouter, HTTPException
from app.database.db import get_all_chats, get_chat_by_id

router = APIRouter()

@router.get("/chats")
async def list_chats():
    """Return a list of all chat sessions."""
    chats = await get_all_chats()
    return chats

@router.get("/chats/{chat_id}")
async def get_chat(chat_id: str):
    """Return the conversation history for a specific chat session."""
    chat = await get_chat_by_id(chat_id)
    if not chat:
        raise HTTPException(status_code=404, detail="Chat session not found")
    return chat
