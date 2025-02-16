# app/core/rag.py

import logging
from typing import Dict, Optional
from app.core.embedding import embed_question
from app.core.pinecone_query import query_vector, filter_matches
from app.core.prompt_builder import build_system_prompt, build_user_prompt_with_chat
from app.core.openai_client import call_openai_api
from app.utils.text_cleaning import clean_text

logger = logging.getLogger(__name__)

# Mark this function as async
async def answer_question(
    question: str,
    top_k: int,
    threshold: float,
    temperature: float,
    max_tokens: int,
    response_style: str,
    namespace: str,
    model_name: str,
    reasoning: bool = False,
    subject_filter: Optional[str] = None,
    chat_id: Optional[str] = None
) -> Dict:
    """
    Orchestrates the full retrieval-augmented generation process.
    """
    logger.info(f"Received question: {question}")

    # 1. Embed the question
    try:
        question_embedding = embed_question(question)
    except Exception as e:
        return {
            "answer": "Unable to embed your question at this time.",
            "relevant_chunks": [],
            "source_files": []
        }

    if not question_embedding:
        return {
            "answer": "Got an empty embedding for your question.",
            "relevant_chunks": [],
            "source_files": []
        }

    # 2. Query Pinecone
    try:
        matches = query_vector(
            vector=question_embedding,
            top_k=top_k,
            namespace=namespace,
            subject_filter=subject_filter
        )
    except Exception as e:
        return {
            "answer": "Error querying the database.",
            "relevant_chunks": [],
            "source_files": []
        }

    relevant_chunks, source_files = filter_matches(matches, threshold)

    # 3. Prepare a cleaned context text from the matches
    cleaned_chunks = [clean_text(chunk) for chunk in relevant_chunks]
    context_text = "\n\n---\n\n".join(cleaned_chunks) if cleaned_chunks else ""

    # 4. Build the system prompt
    system_prompt = build_system_prompt(response_style, reasoning)

    # 5. Build the user prompt, which includes the chat summary if we have a chat_id
    user_prompt = await build_user_prompt_with_chat(
        context_text=context_text, 
        question=question,
        chat_id=chat_id
    )

    # 6. Construct the final messages for OpenAI
    messages = [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": user_prompt}
    ]

    # 7. Call the OpenAI API
    try:
        final_answer = call_openai_api(
            model_name=model_name,
            messages=messages,
            temperature=temperature,
            max_tokens=max_tokens
        )
    except Exception as e:
        return {
            "answer": "There was an error calling the OpenAI API.",
            "relevant_chunks": [],
            "source_files": []
        }

    return {
        "answer": final_answer,
        "relevant_chunks": relevant_chunks,
        "source_files": source_files
    }
