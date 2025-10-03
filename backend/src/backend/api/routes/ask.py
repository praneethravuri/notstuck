"""
Ask endpoint for RAG-powered question answering using CrewAI.
"""

import os
import json
from typing import List, Optional, AsyncGenerator
from fastapi import APIRouter, HTTPException
from fastapi.responses import StreamingResponse
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


@router.post("/ask")
async def ask_question(request: AskRequest):
    """
    Answer a question using RAG pipeline with CrewAI (streaming).

    The crew will:
    1. Analyze the question
    2. Search Pinecone for relevant context
    3. If context found, use it to answer
    4. If no context, use web search to answer

    Args:
        request: AskRequest containing question and model name

    Returns:
        Streaming response with answer chunks
    """
    async def generate_stream() -> AsyncGenerator[str, None]:
        try:
            # Set the model via environment variable (CrewAI will use this)
            if request.modelName:
                os.environ["OPENAI_MODEL_NAME"] = request.modelName

            # Get sources first
            sources = await _extract_sources(request.question)

            # Send sources first
            yield f"data: {json.dumps({'type': 'sources', 'data': [s.model_dump() for s in sources]})}\n\n"

            # Initialize the crew
            backend_crew = Backend()

            # Prepare inputs for the crew
            inputs = {"question": request.question}

            # Run the crew (non-streaming for now, as CrewAI streaming is complex)
            result = backend_crew.crew().kickoff(inputs=inputs)
            answer = str(result)

            # Stream the answer in chunks
            chunk_size = 50
            for i in range(0, len(answer), chunk_size):
                chunk = answer[i:i + chunk_size]
                yield f"data: {json.dumps({'type': 'content', 'data': chunk})}\n\n"

            # Send completion signal
            yield f"data: {json.dumps({'type': 'done'})}\n\n"

        except Exception as e:
            yield f"data: {json.dumps({'type': 'error', 'data': str(e)})}\n\n"

    return StreamingResponse(
        generate_stream(),
        media_type="text/event-stream",
        headers={
            "Cache-Control": "no-cache",
            "Connection": "keep-alive",
        }
    )


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
