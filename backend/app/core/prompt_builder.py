import logging
from typing import Optional
from app.helpers.chat_summary import summarize_chat_history

logger = logging.getLogger(__name__)

def build_system_prompt() -> str:
    # Define a base system prompt and add further instructions.
    system_prompt = "You are an expert assistant."
    system_prompt += (
        "\n\nPlease understand the given context and answer the question based on the context. "
        "If no context is given or if it is empty, use your knowledge. "
        "Do not mention that you relied on the provided context."
    )
    return system_prompt

async def build_user_prompt_with_chat(
    context_text: str,
    question: str,
    chat_id: Optional[str] = None
) -> str:
    """
    Asynchronously builds the user prompt by including:
      - A summary of the previous chat (if chat_id is provided)
      - Additional context (e.g., retrieved documents)
      - The new user question.
    """
    chat_summary = ""
    if chat_id:
        try:
            chat_summary = await summarize_chat_history(chat_id)
            if not chat_summary.strip():
                logger.info(f"No summary available for chat_id={chat_id}.")
        except Exception as e:
            logger.error(f"Error summarizing chat history for chat_id={chat_id}: {e}", exc_info=True)
            chat_summary = ""

    user_prompt = (
        f"Previous Chat Summary:\n{chat_summary}\n\n"
        f"Additional Context:\n{context_text}\n\n"
        f"Question:\n{question}"
    )
    
    logger.debug(f"user prompt: {user_prompt}")
    return user_prompt
