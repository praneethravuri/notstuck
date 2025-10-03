"""
Ask endpoint for RAG-powered question answering using CrewAI.
"""

import os
from typing import List, Optional
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

from backend.crew import Backend
from backend.tools.pinecone_search import PineconeSearchTool

router = APIRouter()


class AskRequest(BaseModel):
    """Request model for ask endpoint."""
    question: str
    modelName: Optional[str] = "openai/gpt-4o"


class SourceMetadata(BaseModel):
    """Source metadata for citations."""
    source_file: str
    page_number: Optional[int] = None
    text: str


class AskResponse(BaseModel):
    """Response model for ask endpoint."""
    answer: str
    sources_metadata: List[SourceMetadata] = []


@router.post("/ask", response_model=AskResponse)
async def ask_question(request: AskRequest):
    """
    Answer a question using RAG pipeline with CrewAI.

    The crew will:
    1. Analyze the question
    2. Search Pinecone for relevant context
    3. If context found, use it to answer
    4. If no context, use web search to answer

    Args:
        request: AskRequest containing question and model name

    Returns:
        AskResponse with answer and source citations
    """
    try:
        # Set the model via environment variable (CrewAI will use this)
        # Note: This assumes the model uses OpenRouter format
        if request.modelName:
            os.environ["OPENAI_MODEL_NAME"] = request.modelName

        # Initialize the crew
        backend_crew = Backend()

        # Prepare inputs for the crew
        inputs = {
            "question": request.question
        }

        # Run the crew
        result = backend_crew.crew().kickoff(inputs=inputs)

        # Get the answer from the crew result
        answer = str(result)

        # Get sources from Pinecone search
        sources = await _extract_sources(request.question)

        return AskResponse(
            answer=answer,
            sources_metadata=sources
        )

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error processing question: {str(e)}")


async def _extract_sources(question: str) -> List[SourceMetadata]:
    """
    Extract source metadata from Pinecone search results.

    Args:
        question: User's question

    Returns:
        List of source metadata
    """
    try:
        # Search Pinecone to get source metadata
        pinecone_search = PineconeSearchTool()
        search_results = pinecone_search.search_with_metadata(
            query=question,
            top_k=5
        )

        sources = []
        if search_results.get("found_context", False):
            for result in search_results.get("results", []):
                sources.append(SourceMetadata(
                    source_file=result.get("source_file", "Unknown"),
                    page_number=result.get("chunk_index"),
                    text=result.get("text", "")
                ))

        return sources

    except Exception as e:
        print(f"Error extracting sources: {e}")
        return []
