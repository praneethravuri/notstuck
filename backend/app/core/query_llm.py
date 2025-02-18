# app/core/openai_client.py
import logging
from app.clients.openai_client import openai_client

logger = logging.getLogger(__name__)

def query_llm(model_name: str, messages: list, temperature: float, max_tokens: int) -> str:
    """
    Queries the OpenAI LLM (Language Model) with the given parameters.
    Logs the request and response for debugging and error handling.
    """
    logger.info(f"Querying OpenAI model: {model_name} with temperature={temperature}, max_tokens={max_tokens}")
    logger.debug(f"Messages: {messages}")

    try:
        response = openai_client.chat.completions.create(
            model=model_name,
            messages=messages,
            temperature=temperature,
            max_completion_tokens=max_tokens
        )
        response_text = response.choices[0].message.content.strip()
        logger.debug(f"OpenAI Response: {response_text}")
        return response_text
    except Exception as e:
        logger.error("Error calling OpenAI API", exc_info=True)
        raise
