# backend/app/routes/ask.py

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import Optional
from app.services.rag.main import answer_question  # adjust the import path as needed
from app.services.mongo_db.db import create_chat_session, append_message_to_chat
from datetime import datetime

router = APIRouter()

class QuestionPayload(BaseModel):
    question: str
    similarityThreshold: float
    similarResults: int
    temperature: float
    maxTokens: int
    responseStyle: str
    modelName: str
    chatId: Optional[str] = None  # New field for chat session

@router.post("/ask")
async def ask_question(payload: QuestionPayload):
    try:
        # Determine the chat session: use provided chatId or create a new session.
        if payload.chatId:
            chat_id = payload.chatId
        else:
            chat_id = await create_chat_session()
        
        # Store the user message
        await append_message_to_chat(chat_id, {
            "role": "user",
            "content": payload.question
        })
        
        # Get the AI answer
        result = answer_question(
            question=payload.question,
            top_k=payload.similarResults,
            threshold=payload.similarityThreshold,
            temperature=payload.temperature,
            max_tokens=payload.maxTokens,
            response_style=payload.responseStyle,
            namespace="my-namespace",
            model_name=payload.modelName
        )
        
        # Store the AI answer
        await append_message_to_chat(chat_id, {
            "role": "ai",
            "content": result["answer"]
        })

        # Return the answer along with the chat session ID
        return {
            "chatId": chat_id,
            "answer": result["answer"],
            "relevant_chunks": result.get("relevant_chunks", []),
            "source_files": result.get("source_files", [])
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
