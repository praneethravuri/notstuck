# app/query_llm/prompt_builder.py

import logging
from typing import Optional
# 1) Import your summarization function
from app.utils.chat_summary import summarize_chat_history

logger = logging.getLogger(__name__)

def build_system_prompt(response_style: str, reasoning: bool = False) -> str:
    if response_style == "concise":
        system_prompt = (
            "You are a helpful AI assistant. Provide a concise answer to the question using the context if relevant. "
            "If the context doesn't help, answer from your own knowledge."
        )
    elif response_style == "technical":
        system_prompt = (
            "You are a technical AI assistant. Provide a detailed and technical answer to the question using the context if relevant. "
            "If the context doesn't help, answer from your own knowledge."
        )
    elif response_style == "casual":
        system_prompt = (
            "You are a friendly AI assistant. Provide a casual and easy-to-understand answer to the question using the context if relevant. "
            "If the context doesn't help, answer from your own knowledge."
        )
    else:
        system_prompt = (
            "You are a helpful AI assistant. Provide a detailed answer to the question using the context if relevant. "
            "If the context doesn't help, answer from your own knowledge."
        )
    if reasoning:
        system_prompt += (
            "\n\nProvide a step-by-step reasoning process for your answer. Break down your thought process into clear and logical steps."
        )
    system_prompt += "\n\nProvide the answer in Markdown format."
    return system_prompt

def build_user_prompt(context_text: str, question: str) -> str:
    """
    Original synchronous prompt builder, if you just want doc context + question
    """
    return f"Context:\n{context_text}\n\nQuestion:\n{question}"

# 2) Define a new async function that includes chat summary
async def build_user_prompt_with_chat(
    context_text: str,
    question: str,
    chat_id: Optional[str] = None
) -> str:
    """
    Asynchronously fetches the summarized chat (if chat_id provided),
    then merges it with the provided context_text (e.g., from Pinecone),
    and the user's new question.
    """
    chat_summary = ""
    if chat_id:
        try:
            chat_summary = await summarize_chat_history(chat_id)
            if not chat_summary.strip():
                logger.info(f"No summary for chat_id={chat_id}.")
        except Exception as e:
            logger.error(f"Error summarizing chat history for chat_id={chat_id}: {e}")
            chat_summary = ""

    # Combine everything
    # - The chat summary (if any)
    # - The retrieved context from documents
    # - The new user question
    user_prompt = (
        f"Previous Chat Summary:\n{chat_summary}\n\n"
        f"Additional Context:\n{context_text}\n\n"
        f"Question:\n{question}"
    )
    
    print(f"user prompt: {user_prompt}")
    
    return user_prompt
