"""
LLM Query Module

This module provides the core LLM querying functionality.
It supports any OpenAI-compatible API including OpenRouter.
"""
import logging
from typing import List, Dict, Optional
from app.clients.openai_client import openai_client
from app.config import DEFAULT_LLM_MODEL

logger = logging.getLogger(__name__)

def query_llm(
    model_name: str,
    messages: List[Dict[str, str]],
    temperature: float,
    max_tokens: int
) -> str:
    """
    Queries an LLM (Language Model) with the given parameters.

    This function works with any OpenAI-compatible API, including:
    - OpenAI
    - OpenRouter (for multi-model access)
    - Other compatible services

    Args:
        model_name: The model identifier (e.g., 'openai/gpt-4-turbo-preview', 'anthropic/claude-3-opus')
        messages: List of message dicts with 'role' and 'content' keys
        temperature: Sampling temperature (0.0 to 2.0)
        max_tokens: Maximum tokens to generate

    Returns:
        str: The model's response text

    Raises:
        Exception: If the API call fails

    Example:
        >>> messages = [
        ...     {"role": "system", "content": "You are a helpful assistant."},
        ...     {"role": "user", "content": "What is Python?"}
        ... ]
        >>> response = query_llm("openai/gpt-4-turbo-preview", messages, 0.7, 500)
    """
    if not openai_client:
        logger.error("LLM client is not initialized")
        raise RuntimeError("LLM client is not initialized. Check your configuration.")

    logger.info(f"Querying LLM model: {model_name} with temperature={temperature}, max_tokens={max_tokens}")
    logger.debug(f"Messages: {messages}")

    try:
        response = openai_client.chat.completions.create(
            model=model_name,
            messages=messages,
            temperature=temperature,
            max_completion_tokens=max_tokens
        )
        response_text = response.choices[0].message.content.strip()
        logger.debug(f"LLM Response: {response_text}")
        return response_text
    except Exception as e:
        logger.error(f"Error calling LLM API with model {model_name}", exc_info=True)
        raise


def query_llm_simple(
    prompt: str,
    model_name: Optional[str] = None,
    temperature: float = 0.7,
    max_tokens: int = 500
) -> str:
    """
    Simplified interface for querying an LLM with a single prompt.

    Args:
        prompt: The user's prompt/question
        model_name: Optional model name (defaults to DEFAULT_LLM_MODEL from config)
        temperature: Sampling temperature (default: 0.7)
        max_tokens: Maximum tokens to generate (default: 500)

    Returns:
        str: The model's response text

    Example:
        >>> response = query_llm_simple("Explain Python in one sentence")
    """
    model = model_name or DEFAULT_LLM_MODEL
    messages = [{"role": "user", "content": prompt}]
    return query_llm(model, messages, temperature, max_tokens)
