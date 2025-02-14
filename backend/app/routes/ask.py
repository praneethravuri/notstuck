# backend/app/routes/ask.py
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import Optional
from app.database.db import create_chat_session, append_message_to_chat
from app.utils.chat_name_generator import generate_chat_name_from_llm
from app.query_llm.rag import answer_question

router = APIRouter()

class QuestionPayload(BaseModel):
    question: str
    similarityThreshold: float
    similarResults: int
    temperature: float
    maxTokens: int
    responseStyle: str
    modelName: str
    chatId: Optional[str] = None
    chatName: Optional[str] = None  # optional field from client

@router.post("/ask")
async def ask_question(payload: QuestionPayload):
    try:
        if payload.chatId:
            chat_id = payload.chatId
        else:
            # If a chat name is provided from the client, use it.
            # Otherwise, use the LLM to generate one based on the question.
            if payload.chatName:
                chat_name = payload.chatName
            else:
                chat_name = await generate_chat_name_from_llm(payload.question)
                print(f"Chat name generated: {chat_name}")
            
            chat_session = await create_chat_session(chat_name=chat_name)
            chat_id = chat_session["chatId"]

        # Store the user message.
        await append_message_to_chat(chat_id, {
            "role": "user",
            "content": payload.question
        })

        # Generate the answer (replace with your actual function call).
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

        # Store the AI answer.
        await append_message_to_chat(chat_id, {
            "role": "ai",
            "content": result.get("answer", "")
        })

        return {
            "chatId": chat_id,
            "chatName": payload.chatId and None or chat_session.get("name"),
            "answer": result.get("answer", ""),
            "relevant_chunks": result.get("relevant_chunks", []),
            "source_files": result.get("source_files", [])
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
