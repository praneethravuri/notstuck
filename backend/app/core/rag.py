# app/core/rag.py
import logging
from typing import Dict, Optional
from app.core.prompt_builder import build_system_prompt, build_user_prompt_with_chat
from app.core.openai_client import call_openai_api
from app.utils.text_cleaning import clean_text

from app.utils.generate_embeddings import get_embedding_function
from pinecone_text.sparse import BM25Encoder
import os
from app.clients import pinecone_index

BM25_JSON_PATH = "bm25_values.json"

def load_bm25_encoder(json_path: str = BM25_JSON_PATH):
    try:
        encoder = BM25Encoder().load(json_path)
        print(f"DEBUG: Loaded BM25 encoder state from {json_path}")
    except Exception as e:
        print(f"DEBUG: Error loading BM25 state: {e}. Using default encoder.")
        encoder = BM25Encoder().default()
    return encoder

def hybrid_score_norm(dense, sparse, alpha: float):
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
    top_k: int,
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
    Performs a hybrid search query by:
      1. Generating a dense query vector.
      2. Generating a sparse query vector using BM25 (loaded from JSON).
      3. Applying a convex weighting via an alpha parameter.
      4. Querying the Pinecone index with the weighted dense and sparse vectors.
      5. Filtering out any results with a score < similarity_threshold.
         If none are found, a prompt is built with an empty context and a note that no relevant context was found.
      6. Sending the prompt (with context or fallback) and the question to the LLM.
    """
    # 1. Generate dense query vector.
    dense_embedding_func = get_embedding_function()
    dense_query = dense_embedding_func.embed_query(question)
    
    # 2. Generate sparse query vector.
    bm25_encoder = load_bm25_encoder()
    sparse_query_list = bm25_encoder.encode_documents([question])
    sparse_query = sparse_query_list[0] if sparse_query_list else BM25Encoder().default()
    
    # 3. Apply hybrid weighting.
    alpha = 0.75
    weighted_dense, weighted_sparse = hybrid_score_norm(dense_query, sparse_query, alpha)
    
    # 4. Build filter if needed.
    filter_criteria = None
    if subject_filter:
        filter_criteria = {"subjects": {"$in": [subject_filter.lower().strip()]}}
    
    # 5. Query Pinecone with both weighted dense and sparse vectors.
    query_response = pinecone_index.query(
        top_k=top_k,
        vector=weighted_dense,
        sparse_vector=weighted_sparse,
        namespace=namespace,
        filter=filter_criteria,
        include_metadata=True
    )
    
    matches = query_response.get("matches", [])
    
    # 6. Post-filter matches by a similarity threshold.
    similarity_threshold = 0.4
    filtered_matches = [m for m in matches if m["score"] >= similarity_threshold]
    
    if filtered_matches:
        # Build context from retrieved matches.
        context_chunks = []
        for match in filtered_matches:
            meta = match.get("metadata", {})
            text = meta.get("text", "")
            if text:
                context_chunks.append(clean_text(text))
        context_text = "\n\n---\n\n".join(context_chunks)
        print("DEBUG: Context text (first 200 chars):", context_text[:200])
    else:
        # If no matches pass the threshold, use empty context with a note.
        print("DEBUG: No relevant context found; using fallback prompt.")
        context_text = ""  # or you can also set it to a custom note if preferred
    
    # 7. Build prompts.
    system_prompt = build_system_prompt(response_style, reasoning)
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
    final_answer = call_openai_api(
        model_name=model_name,
        messages=messages,
        temperature=temperature,
        max_tokens=max_tokens
    )
    
    return {
        "answer": final_answer,
        "relevant_chunks": context_chunks if filtered_matches else [],
        "sources_metadata": [m["metadata"] for m in filtered_matches] if filtered_matches else []
    }
