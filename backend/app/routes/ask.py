from fastapi import APIRouter, HTTPException
from app.models import QuestionRequest, QuestionResponse, SourceMetadata
from app.core.rag import answer_question
from app.config import PINECONE_NAMESPACE
import logging

router = APIRouter()
logger = logging.getLogger(__name__)

@router.post("/ask", response_model=QuestionResponse)
async def ask_question(payload: QuestionRequest):
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

        # Convert sources_metadata to Pydantic models
        sources_metadata = [
            SourceMetadata(
                source_file=meta.get("source_file", "unknown"),
                page_number=meta.get("page_number"),
                text=meta.get("text", ""),
                subjects=meta.get("subjects")
            )
            for meta in result.get("sources_metadata", [])
        ]

        # Build response using Pydantic model
        response = QuestionResponse(
            answer=result.get("answer", ""),
            relevant_chunks=result.get("relevant_chunks", []),
            sources_metadata=sources_metadata
        )

        logger.info("Successfully processed question")
        return response

    except ValueError as ve:
        logger.warning(f"Validation error: {ve}")
        raise HTTPException(status_code=400, detail=str(ve))
    except HTTPException:
        raise
    except Exception as e:
        logger.error("Exception occurred in ask_question: %s", e, exc_info=True)
        raise HTTPException(status_code=500, detail="An error occurred while processing your question. Please try again.")
