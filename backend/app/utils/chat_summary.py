# app/utils/chat_summary.py

import logging
from fastapi import HTTPException
from app.database.db import get_chat_by_id
from app.clients import openai_client as client
from app.utils.text_cleaning import clean_text

logger = logging.getLogger(__name__)

async def summarize_chat_history(chat_id: str) -> str:
    chat = await get_chat_by_id(chat_id)
    if not chat:
        raise HTTPException(status_code=404, detail="Chat session not found.")

    messages = chat.get("messages", [])
    if not messages:
        logger.info("No messages to summarize.")
        return ""

    conversation_lines = []
    for msg in messages:
        role = msg.get("role", "user").upper()
        cleaned = clean_text(msg.get("content", ""))
        conversation_lines.append(f"{role}: {cleaned}")

    conversation_text = "\n".join(conversation_lines)
    if not conversation_text.strip():
        return ""

    try:
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a helpful assistant. Summarize the conversation below."},
                {"role": "user", "content": conversation_text}
            ],
            temperature=0.7,
            max_tokens=100
        )
        summary = response.choices[0].message.content.strip()
        return summary
    except Exception as e:
        logger.error(f"Error summarizing chat: {e}")
        return conversation_text  # fallback
