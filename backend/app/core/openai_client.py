# app/core/openai_client.py
import logging
from app.clients import openai_client

logger = logging.getLogger(__name__)


def call_openai_api(model_name: str, messages: list, temperature: float, max_tokens: int) -> str:
    try:
        response = openai_client.chat.completions.create(
            model=model_name,
            messages=messages,
            temperature=temperature,
            max_completion_tokens=max_tokens
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        logger.error(f"Error calling OpenAI API: {e}")
        raise e
