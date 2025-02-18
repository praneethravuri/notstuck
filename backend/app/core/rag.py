import os
import logging
from typing import Dict, Optional
from app.core.prompt_builder import build_user_prompt_with_chat, build_system_prompt
from app.core.query_llm import query_llm
from app.utils.text_cleaning import clean_text
from app.clients.openai_embeddings import get_embedding_function
from pinecone_text.sparse import BM25Encoder
from app.clients.pinecone_client import pinecone_index
from app.config import HYBRID_WEIGHT_RATIO, TOP_K, SIMILARITY_THRESHOLD, BM25_JSON_PATH

logger = logging.getLogger(__name__)

def load_bm25_encoder(json_path: str = BM25_JSON_PATH):
    """
    Load the BM25 encoder from a JSON file, or fallback to the default encoder if loading fails.
    """
    try:
        encoder = BM25Encoder().load(json_path)
        logger.info(f"Loaded BM25 encoder state from {json_path}")
    except Exception as e:
        logger.error(f"Error loading BM25 state: {e}. Using default encoder.", exc_info=True)
        encoder = BM25Encoder().default()
    return encoder

def hybrid_score_norm(dense, sparse, alpha: float):
    """
    Normalize hybrid scores by applying a convex weighting.
    """
    if alpha < 0 or alpha > 1:
        raise ValueError("Alpha must be between 0 and 1")
    hsparse = {
        'indices': sparse['indices'],
        'values': [v * (1 - alpha) for v in sparse['values']]
    }
    hdense = [v * alpha for v in dense]
    return hdense, hsparse

async def answer_question(
    question: str,
    namespace: str,
    model_name: str,
    subject_filter: Optional[str] = None,
    chat_id: Optional[str] = None
) -> Dict:
    """
    Performs a hybrid search query and uses retrieved context to answer the given question.
    """
    logger.info(f"Starting answer generation for question: {question[:100]}")  # Log first 100 chars of the question

    try:
        # 1. Generate dense query vector.
        dense_embedding_func = get_embedding_function()
        dense_query = dense_embedding_func.embed_query(question)

        # 2. Generate sparse query vector.
        bm25_encoder = load_bm25_encoder()
        sparse_query_list = bm25_encoder.encode_documents([question])
        sparse_query = sparse_query_list[0] if sparse_query_list else BM25Encoder().default()

        # 3. Apply hybrid weighting.
        alpha = HYBRID_WEIGHT_RATIO
        weighted_dense, weighted_sparse = hybrid_score_norm(dense_query, sparse_query, alpha)

        # 4. Build filter if needed.
        filter_criteria = None
        if subject_filter:
            filter_criteria = {"subjects": {"$in": [subject_filter.lower().strip()]}}
        
        # 5. Query Pinecone with both weighted dense and sparse vectors.
        query_response = pinecone_index.query(
            top_k=TOP_K,
            vector=weighted_dense,
            sparse_vector=weighted_sparse,
            namespace=namespace,
            filter=filter_criteria,
            include_metadata=True
        )

        matches = query_response.get("matches", [])

        # 6. Post-filter matches by a similarity threshold.
        filtered_matches = [m for m in matches if m["score"] >= SIMILARITY_THRESHOLD]

        if filtered_matches:
            # Build context from retrieved matches.
            context_chunks = [
                clean_text(match["metadata"].get("text", ""))
                for match in filtered_matches if match.get("metadata", {}).get("text")
            ]
            context_text = "\n\n---\n\n".join(context_chunks)
            logger.debug(f"Context text (first 200 chars): {context_text[:200]}")
        else:
            # If no matches pass the threshold, use empty context with a note.
            logger.info("No relevant context found; using fallback prompt.")
            context_text = ""  # or you can also set it to a custom note if preferred

        # 7. Build prompts.
        system_prompt = build_system_prompt()
        # If no context is found, include a note in the prompt.
        if not filtered_matches:
            fallback_note = "No relevant context was found for this query. Please answer using your general knowledge."
            user_prompt = await build_user_prompt_with_chat(
                context_text=fallback_note,
                question=question,
                chat_id=chat_id
            )
        else:
            user_prompt = await build_user_prompt_with_chat(
                context_text=context_text,
                question=question,
                chat_id=chat_id
            )

        messages = [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt}
        ]

        # 8. Call the LLM API.
        final_answer = query_llm(
            model_name=model_name,
            messages=messages,
            temperature=0.7,
            max_tokens=5000
        )

        logger.info("Successfully generated an answer.")

        return {
            "answer": final_answer,
            "relevant_chunks": context_chunks if filtered_matches else [],
            "sources_metadata": [m["metadata"] for m in filtered_matches] if filtered_matches else []
        }

    except Exception as e:
        logger.error(f"Error in answer_question: {e}", exc_info=True)
        return {
            "answer": "An error occurred while processing the request.",
            "relevant_chunks": [],
            "sources_metadata": []
        }
