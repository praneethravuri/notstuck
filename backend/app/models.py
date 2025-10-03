"""
Pydantic Models for API Request/Response Validation

This module defines all the data models used across the API endpoints
for structured input validation and response formatting.
"""
from typing import Optional, List, Dict, Any
from pydantic import BaseModel, Field, validator


# ============================================================================
# Question/Ask Endpoint Models
# ============================================================================

class QuestionRequest(BaseModel):
    """Request model for asking questions to the RAG system."""
    question: str = Field(
        ...,
        min_length=1,
        max_length=5000,
        description="User's question to be answered",
        example="What is the main topic of the document?"
    )
    modelName: str = Field(
        ...,
        min_length=1,
        max_length=200,
        description="OpenRouter model identifier",
        example="openai/gpt-4o"
    )
    subject: Optional[str] = Field(
        None,
        max_length=100,
        description="Optional subject filter for document retrieval",
        example="programming"
    )

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


class SourceMetadata(BaseModel):
    """Metadata for a single source chunk."""
    source_file: str = Field(..., description="Source PDF filename")
    page_number: Optional[int] = Field(None, description="Page number in PDF")
    text: str = Field(..., description="Text content of the chunk")
    subjects: Optional[str] = Field(None, description="Detected subjects/tags")


class QuestionResponse(BaseModel):
    """Response model for question answers."""
    answer: str = Field(..., description="Generated answer from LLM")
    relevant_chunks: List[str] = Field(
        default_factory=list,
        description="List of relevant text chunks used for context"
    )
    sources_metadata: List[SourceMetadata] = Field(
        default_factory=list,
        description="Metadata for each source chunk"
    )


# ============================================================================
# Upload Endpoint Models
# ============================================================================

class UploadResponse(BaseModel):
    """Response model for file upload."""
    message: str = Field(..., description="Status message")
    files: List[str] = Field(..., description="List of uploaded filenames")
    count: int = Field(..., description="Number of files processed")


# ============================================================================
# Model List Endpoint Models
# ============================================================================

class ModelInfo(BaseModel):
    """Information about an available LLM model."""
    id: str = Field(..., description="Model identifier for API calls")
    name: str = Field(..., description="Human-readable model name")
    description: Optional[str] = Field(None, description="Model description")
    context_length: Optional[int] = Field(None, description="Maximum context length")
    pricing: Optional[Dict[str, float]] = Field(None, description="Pricing information")
    provider: Optional[str] = Field(None, description="Model provider (e.g., openai, anthropic)")


class ModelsListResponse(BaseModel):
    """Response model for available models list."""
    models: List[ModelInfo] = Field(..., description="List of available models")
    count: int = Field(..., description="Total number of models")


# ============================================================================
# Health Check Models
# ============================================================================

class HealthCheckResponse(BaseModel):
    """Response model for health check endpoint."""
    ready: bool = Field(..., description="Whether the backend is ready")
    message: str = Field(..., description="Status message")


# ============================================================================
# Reset Database Models
# ============================================================================

class ResetDatabaseResponse(BaseModel):
    """Response model for database reset."""
    message: str = Field(..., description="Reset status message")
    namespace: str = Field(..., description="Namespace that was reset")


# ============================================================================
# Error Response Models
# ============================================================================

class ErrorResponse(BaseModel):
    """Generic error response model."""
    error: str = Field(..., description="Error message")
    detail: Optional[str] = Field(None, description="Detailed error information")
    status_code: int = Field(..., description="HTTP status code")
