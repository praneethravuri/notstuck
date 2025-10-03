import logging

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

def build_user_prompt(context_text: str, question: str) -> str:
    """
    Builds the user prompt by including:
      - Retrieved context (e.g., documents)
      - The user question
    """
    user_prompt = (
        f"Context:\n{context_text}\n\n"
        f"Question:\n{question}"
    )

    logger.debug(f"user prompt: {user_prompt}")
    return user_prompt
