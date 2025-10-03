"""
Models endpoint to return available LLM models.
"""

from fastapi import APIRouter
from pydantic import BaseModel
from typing import List

router = APIRouter()


class ModelInfo(BaseModel):
    """Model information."""
    id: str
    name: str
    provider: str


class ModelsResponse(BaseModel):
    """Response model for models endpoint."""
    models: List[ModelInfo]


@router.get("/models", response_model=ModelsResponse)
async def get_models():
    """
    Get list of available LLM models.

    Returns:
        ModelsResponse with list of available models
    """
    # Define available models (OpenRouter format)
    models = [
        ModelInfo(
            id="openai/gpt-4o",
            name="GPT-4o",
            provider="OpenAI"
        ),
        ModelInfo(
            id="openai/gpt-4-turbo",
            name="GPT-4 Turbo",
            provider="OpenAI"
        ),
        ModelInfo(
            id="openai/gpt-4",
            name="GPT-4",
            provider="OpenAI"
        ),
        ModelInfo(
            id="openai/gpt-3.5-turbo",
            name="GPT-3.5 Turbo",
            provider="OpenAI"
        ),
        ModelInfo(
            id="anthropic/claude-3.5-sonnet",
            name="Claude 3.5 Sonnet",
            provider="Anthropic"
        ),
        ModelInfo(
            id="anthropic/claude-3-opus",
            name="Claude 3 Opus",
            provider="Anthropic"
        ),
        ModelInfo(
            id="anthropic/claude-3-haiku",
            name="Claude 3 Haiku",
            provider="Anthropic"
        ),
    ]

    return ModelsResponse(models=models)
