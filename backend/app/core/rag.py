import logging
from typing import Dict, Optional
from app.core.prompt_builder import build_user_prompt, build_system_prompt
from app.core.query_llm import query_llm
from app.config import TEMPERATURE, MAX_TOKENS
from app.core.rag_utils import generate_queries, apply_hybrid_weighting, build_filter, build_context_text
from app.core.pinecone_query import retrieve_matches, filter_matches_by_threshold

logger = logging.getLogger(__name__)

async def answer_question(
    question: str,
    namespace: str,
    model_name: str,
    subject_filter: Optional[str] = None
) -> Dict:
    """
    Performs a hybrid search query and uses retrieved context to answer the given question.
    """
    logger.info(f"Starting answer generation for question: {question[:100]}")

    try:
        # 1. Generate dense and sparse query vectors.
        dense_query, sparse_query = generate_queries(question)

        # 2. Apply hybrid weighting.
        weighted_dense, weighted_sparse = apply_hybrid_weighting(dense_query, sparse_query)

        # 3. Build filter criteria if needed.
        filter_criteria = build_filter(subject_filter)

        # 4. Retrieve matches from Pinecone.
        matches = retrieve_matches(weighted_dense, weighted_sparse, filter_criteria, namespace)

        # 5. Filter matches by similarity threshold.
        filtered_matches = filter_matches_by_threshold(matches)

        # 6. Build context text.
        if filtered_matches:
            context_text, context_chunks = build_context_text(filtered_matches)
            logger.debug(f"Context text (first 200 chars): {context_text[:200]}")
        else:
            logger.info("No relevant context found; using fallback prompt.")
            context_text = ""
            context_chunks = []

        # 7. Build system and user prompts.
        system_prompt = build_system_prompt()
        if not filtered_matches:
            fallback_note = "No relevant context was found for this query. Please answer using your general knowledge."
            user_prompt = build_user_prompt(
                context_text=fallback_note,
                question=question
            )
        else:
            user_prompt = build_user_prompt(
                context_text=context_text,
                question=question
            )

        messages = [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt}
        ]

        # 8. Call the LLM API.
        final_answer = query_llm(
            model_name=model_name,
            messages=messages,
            temperature=TEMPERATURE,
            max_tokens=MAX_TOKENS
        )

        logger.info("Successfully generated an answer.")

        return {
            "answer": final_answer,
            "relevant_chunks": context_chunks,
            "sources_metadata": [m["metadata"] for m in filtered_matches]
        }

    except Exception as e:
        logger.error(f"Error in answer_question: {e}", exc_info=True)
        return {
            "answer": "An error occurred while processing the request.",
            "relevant_chunks": [],
            "sources_metadata": []
        }
