from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import Optional, Dict, Any
from app.core.rag import answer_question
from app.config import PINECONE_NAMESPACE
import logging

router = APIRouter()
logger = logging.getLogger(__name__)

class QuestionPayload(BaseModel):
    question: str
    modelName: str
    subject: Optional[str] = None

@router.post("/ask")
async def ask_question(payload: QuestionPayload):
    try:
        logger.debug("Received payload: %s", payload.dict())

        # Process the question using RAG
        result = await answer_question(
            question=payload.question,
            namespace=PINECONE_NAMESPACE,
            model_name=payload.modelName,
            subject_filter=payload.subject
        )

        # Return the response payload
        response_payload = {
            "answer": result.get("answer", ""),
            "relevant_chunks": result.get("relevant_chunks", []),
            "sources_metadata": result.get("sources_metadata", [])
        }
        logger.debug("Returning response payload: %s", response_payload)
        return response_payload

    except Exception as e:
        logger.error("Exception occurred in ask_question: %s", e, exc_info=True)
        raise HTTPException(status_code=500, detail=str(e))
