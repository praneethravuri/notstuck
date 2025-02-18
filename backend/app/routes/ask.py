from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import Optional, Dict, Any
from app.database.db import create_chat_session, append_message_to_chat, get_chat_by_id
from app.utils.chat_name_generator import generate_chat_name_from_llm
from app.core.rag import answer_question
from app.config import PINECONE_NAMESPACE

router = APIRouter()

class QuestionPayload(BaseModel):
    question: str
    modelName: str
    chatId: Optional[str] = None
    chatName: Optional[str] = None
    subject: Optional[str] = None


async def get_or_create_chat(payload: QuestionPayload) -> Dict[str, str]:
    if payload.chatId:
        print("DEBUG: Chat ID provided; fetching existing chat details...")
        chat = await get_chat_by_id(payload.chatId)
        if not chat:
            raise HTTPException(status_code=404, detail="Chat session not found")
        chat_id = payload.chatId
        chat_name = chat.get("name") or "Unnamed Chat"
    else:
        if payload.chatName:
            chat_name = payload.chatName
        else:
            chat_name = await generate_chat_name_from_llm(payload.question)
        chat_session = await create_chat_session(chat_name=chat_name)
        chat_id = chat_session["chatId"]
        chat_name = chat_session["name"]
    return {"chatId": chat_id, "chatName": chat_name}


async def append_user_message(chat_id: str, question: str) -> None:
    await append_message_to_chat(chat_id, {"role": "user", "content": question})


# Modified to accept an optional "sources" parameter.
async def append_ai_message(chat_id: str, answer: str, sources: Optional[list] = None) -> None:
    message = {"role": "ai", "content": answer}
    if sources:
        message["sources"] = sources
    await append_message_to_chat(chat_id, message)


# Change process_question to ASYNC so we can await answer_question
async def process_question(payload: QuestionPayload, chat_id: str) -> Dict[str, Any]:
    """
    Pass the chat_id to answer_question, along with all other parameters.
    """
    return await answer_question(
        question=payload.question,
        namespace=PINECONE_NAMESPACE,
        model_name=payload.modelName,
        subject_filter=payload.subject,
        chat_id=chat_id
    )


@router.post("/ask")
async def ask_question(payload: QuestionPayload):
    try:
        print("DEBUG: Received payload:", payload.dict())
        # 1) Create or fetch an existing chat session
        chat_info = await get_or_create_chat(payload)
        chat_id = chat_info["chatId"]
        chat_name = chat_info["chatName"]

        # 2) Log the user's question in the chat history
        await append_user_message(chat_id, payload.question)

        # 3) Process the question (includes RAG flow + chat_id)
        result = await process_question(payload, chat_id)

        # 4) Log the AI’s answer in the chat (including its sources)
        await append_ai_message(
            chat_id,
            result.get("answer", ""),
            result.get("sources_metadata", [])
        )

        # 5) Return a response payload
        response_payload = {
            "chatId": chat_id,
            "chatName": chat_name,
            "answer": result.get("answer", ""),
            "relevant_chunks": result.get("relevant_chunks", []),
            "sources_metadata": result.get("sources_metadata", [])
        }
        print("DEBUG: Returning response payload :", response_payload)
        return response_payload

    except Exception as e:
        print("DEBUG: Exception occurred in ask.py:", e)
        raise HTTPException(status_code=500, detail=str(e))
