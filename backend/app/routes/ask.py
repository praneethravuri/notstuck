from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field, validator
from typing import Optional
from app.core.rag import answer_question
from app.config import PINECONE_NAMESPACE
import logging

router = APIRouter()
logger = logging.getLogger(__name__)

class QuestionPayload(BaseModel):
    question: str = Field(..., min_length=1, max_length=5000, description="User question")
    modelName: str = Field(..., min_length=1, max_length=200, description="Model identifier")
    subject: Optional[str] = Field(None, max_length=100, description="Optional subject filter")

    @validator('question')
    def validate_question(cls, v):
        if not v or not v.strip():
            raise ValueError("Question cannot be empty or whitespace only")
        return v.strip()

    @validator('modelName')
    def validate_model_name(cls, v):
        if not v or not v.strip():
            raise ValueError("Model name cannot be empty")
        return v.strip()

    @validator('subject')
    def validate_subject(cls, v):
        if v:
            return v.strip() if v.strip() else None
        return None

@router.post("/ask")
async def ask_question(payload: QuestionPayload):
    """
    Process a question using RAG and return an answer.

    Args:
        payload: Question payload containing question, model name, and optional subject filter

    Returns:
        Response with answer, relevant chunks, and source metadata

    Raises:
        HTTPException: On validation or processing errors
    """
    try:
        logger.info(f"Processing question: '{payload.question[:100]}...' with model: {payload.modelName}")

        # Process the question using RAG
        result = await answer_question(
            question=payload.question,
            namespace=PINECONE_NAMESPACE,
            model_name=payload.modelName,
            subject_filter=payload.subject
        )

        # Validate result structure
        if not isinstance(result, dict):
            logger.error(f"Invalid result type from answer_question: {type(result)}")
            raise HTTPException(status_code=500, detail="Internal processing error")

        # Return the response payload
        response_payload = {
            "answer": result.get("answer", ""),
            "relevant_chunks": result.get("relevant_chunks", []),
            "sources_metadata": result.get("sources_metadata", [])
        }

        logger.info("Successfully processed question")
        return response_payload

    except ValueError as ve:
        logger.warning(f"Validation error: {ve}")
        raise HTTPException(status_code=400, detail=str(ve))
    except HTTPException:
        raise
    except Exception as e:
        logger.error("Exception occurred in ask_question: %s", e, exc_info=True)
        raise HTTPException(status_code=500, detail="An error occurred while processing your question. Please try again.")
