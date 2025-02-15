# app/routes/ask.py

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import Optional
from app.database.db import create_chat_session, append_message_to_chat, get_chat_by_id
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
    chatName: Optional[str] = None
    subject: Optional[str] = None  # <-- New optional field for subject filtering

@router.post("/ask")
async def ask_question(payload: QuestionPayload):
    try:
        print("DEBUG: Received payload:", payload.dict())

        if payload.chatId:
            print("DEBUG: Chat ID provided; fetching existing chat details...")
            chat = await get_chat_by_id(payload.chatId)
            print("DEBUG: Result of get_chat_by_id:", chat)
            if not chat:
                print("DEBUG: No chat found for provided chatId:", payload.chatId)
                raise HTTPException(status_code=404, detail="Chat session not found")
            chat_id = payload.chatId
            chat_name = chat.get("name")
            if not chat_name:
                print("DEBUG: Existing chat has no name; setting default name.")
                chat_name = "Unnamed Chat"
            print("DEBUG: Using existing chat; ID:", chat_id, "Name:", chat_name)
        else:
            print("DEBUG: No chatId provided; creating a new chat session.")
            if payload.chatName:
                chat_name = payload.chatName
                print("DEBUG: Using provided chatName:", chat_name)
            else:
                chat_name = await generate_chat_name_from_llm(payload.question)
                print("DEBUG: Generated chat name:", chat_name)
            chat_session = await create_chat_session(chat_name=chat_name)
            print("DEBUG: New chat session created:", chat_session)
            chat_id = chat_session["chatId"]
            chat_name = chat_session["name"]
        
        print("DEBUG: Appending user message to chat (ID:", chat_id, ")")
        await append_message_to_chat(chat_id, {
            "role": "user",
            "content": payload.question
        })
        print("DEBUG: User message appended.")

        print("DEBUG: Calling answer_question with question:", payload.question)
        result = answer_question(
            question=payload.question,
            top_k=payload.similarResults,
            threshold=payload.similarityThreshold,
            temperature=payload.temperature,
            max_tokens=payload.maxTokens,
            response_style=payload.responseStyle,
            namespace="my-namespace",
            model_name=payload.modelName,
            subject_filter=payload.subject  # Pass the subject filter if provided
        )
        print("DEBUG: answer_question returned:", result)

        print("DEBUG: Appending AI answer to chat (ID:", chat_id, ")")
        await append_message_to_chat(chat_id, {
            "role": "ai",
            "content": result.get("answer", "")
        })
        print("DEBUG: AI answer appended.")

        response_payload = {
            "chatId": chat_id,
            "chatName": chat_name,
            "answer": result.get("answer", ""),
            "relevant_chunks": result.get("relevant_chunks", []),
            "source_files": result.get("source_files", [])
        }
        print("DEBUG: Returning response payload:", response_payload)
        return response_payload
    except Exception as e:
        print("DEBUG: Exception occurred:", e)
        raise HTTPException(status_code=500, detail=str(e))
