# app/query_llm/rag.py
import logging
from typing import Dict
from app.query_llm.embedding import embed_question
from app.query_llm.pinecone_query import query_vector, filter_matches
from app.query_llm.prompt_builder import build_system_prompt, build_user_prompt
from app.query_llm.openai_client import call_openai_api

logger = logging.getLogger(__name__)


def answer_question(
    question: str,
    top_k: int,
    threshold: float,
    temperature: float,
    max_tokens: int,
    response_style: str,
    namespace: str,
    model_name: str,
    reasoning: bool = False,
    subject_filter: str = None
) -> Dict:
    """
    Orchestrates the full retrieval-augmented generation process.
    """
    logger.info(f"Received question: {question}")

    # 1. Embed the question.
    try:
        question_embedding = embed_question(question)
    except Exception as e:
        return {"answer": "Unable to embed your question at this time.", "relevant_chunks": [], "source_files": []}

    if not question_embedding:
        return {"answer": "Got an empty embedding for your question.", "relevant_chunks": [], "source_files": []}

    # 2. Query Pinecone.
    try:
        matches = query_vector(question_embedding, top_k,
                               namespace, subject_filter)
    except Exception as e:
        return {"answer": "Error querying the database.", "relevant_chunks": [], "source_files": []}

    relevant_chunks, source_files = filter_matches(matches, threshold)
    context_text = "\n\n---\n\n".join(
        relevant_chunks) if relevant_chunks else ""

    # 3. Build the prompts.
    system_prompt = build_system_prompt(response_style, reasoning)
    user_prompt = build_user_prompt(context_text, question)
    messages = [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": user_prompt}
    ]

    # 4. Call the OpenAI API.
    try:
        final_answer = call_openai_api(
            model_name, messages, temperature, max_tokens)
    except Exception as e:
        return {"answer": "There was an error calling the OpenAI API.", "relevant_chunks": [], "source_files": []}

    return {"answer": final_answer, "relevant_chunks": relevant_chunks, "source_files": source_files}
