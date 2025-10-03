"""
Models List Route

Endpoint to fetch available OpenRouter models.
"""
import logging
from fastapi import APIRouter, HTTPException
from typing import List, Dict, Any
from app.models import ModelInfo, ModelsListResponse

router = APIRouter()
logger = logging.getLogger(__name__)

# Curated list of recommended OpenRouter models
# You can extend this list or fetch dynamically from OpenRouter API
RECOMMENDED_MODELS: List[Dict[str, Any]] = [
    {
        "id": "openai/gpt-4o",
        "name": "GPT-4o",
        "description": "OpenAI's most advanced model with vision capabilities",
        "context_length": 128000,
        "provider": "openai"
    },
    {
        "id": "openai/gpt-4o-mini",
        "name": "GPT-4o Mini",
        "description": "Faster and more affordable than GPT-4o",
        "context_length": 128000,
        "provider": "openai"
    },
    {
        "id": "openai/gpt-4-turbo",
        "name": "GPT-4 Turbo",
        "description": "High-intelligence flagship model for complex tasks",
        "context_length": 128000,
        "provider": "openai"
    },
    {
        "id": "openai/gpt-3.5-turbo",
        "name": "GPT-3.5 Turbo",
        "description": "Fast, affordable model for simple tasks",
        "context_length": 16385,
        "provider": "openai"
    },
    {
        "id": "anthropic/claude-3.5-sonnet",
        "name": "Claude 3.5 Sonnet",
        "description": "Anthropic's most intelligent model",
        "context_length": 200000,
        "provider": "anthropic"
    },
    {
        "id": "anthropic/claude-3-haiku",
        "name": "Claude 3 Haiku",
        "description": "Fast and compact model for lightweight tasks",
        "context_length": 200000,
        "provider": "anthropic"
    },
    {
        "id": "google/gemini-pro-1.5",
        "name": "Gemini Pro 1.5",
        "description": "Google's advanced multimodal model",
        "context_length": 1000000,
        "provider": "google"
    },
    {
        "id": "meta-llama/llama-3.1-70b-instruct",
        "name": "Llama 3.1 70B",
        "description": "Meta's powerful open-source model",
        "context_length": 131072,
        "provider": "meta"
    },
    {
        "id": "mistralai/mistral-large",
        "name": "Mistral Large",
        "description": "Mistral's flagship model for complex tasks",
        "context_length": 128000,
        "provider": "mistral"
    },
    {
        "id": "cohere/command-r-plus",
        "name": "Command R+",
        "description": "Cohere's advanced model for RAG and tool use",
        "context_length": 128000,
        "provider": "cohere"
    }
]


@router.get("/models", response_model=ModelsListResponse)
async def get_available_models():
    """
    Get list of available OpenRouter models for the frontend.

    Returns:
        ModelsListResponse: List of available models with metadata

    Raises:
        HTTPException: If there's an error fetching models
    """
    try:
        logger.info("Fetching available models list")

        models = [ModelInfo(**model) for model in RECOMMENDED_MODELS]

        response = ModelsListResponse(
            models=models,
            count=len(models)
        )

        logger.info(f"Returning {len(models)} available models")
        return response

    except Exception as e:
        logger.error(f"Error fetching models: {e}", exc_info=True)
        raise HTTPException(
            status_code=500,
            detail="Failed to fetch available models"
        )


@router.get("/models/default")
async def get_default_model():
    """
    Get the default model configuration.

    Returns:
        dict: Default model information
    """
    try:
        default_model = RECOMMENDED_MODELS[0]  # GPT-4o as default
        logger.info(f"Returning default model: {default_model['id']}")
        return {
            "model": ModelInfo(**default_model),
            "message": "Default model retrieved successfully"
        }
    except Exception as e:
        logger.error(f"Error fetching default model: {e}", exc_info=True)
        raise HTTPException(
            status_code=500,
            detail="Failed to fetch default model"
        )
