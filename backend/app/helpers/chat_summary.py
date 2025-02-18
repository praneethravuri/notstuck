# app/utils/chat_summary.py

import logging
from fastapi import HTTPException
from app.database.db import get_chat_by_id
from app.clients.openai_client import openai_client
from app.utils.text_cleaning import clean_text

logger = logging.getLogger(__name__)

async def summarize_chat_history(chat_id: str) -> str:
    chat = await get_chat_by_id(chat_id)
    if not chat:
        raise HTTPException(status_code=404, detail="Chat session not found.")

    messages = chat.get("messages", [])
    if not messages:
        logger.info("No messages to summarize for chat_id=%s.", chat_id)
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
        response = openai_client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {
                    "role": "system", 
                    "content": "You are a helpful assistant. Summarize the conversation below."
                },
                {"role": "user", "content": conversation_text}
            ],
            temperature=0.7,
            max_tokens=100
        )
        summary = response.choices[0].message.content.strip()
        logger.info("Chat summary generated successfully for chat_id=%s.", chat_id)
        return summary
    except Exception as e:
        logger.error("Error summarizing chat for chat_id=%s: %s", chat_id, e, exc_info=True)
        # Fallback: return the raw conversation text if summarization fails.
        return conversation_text
