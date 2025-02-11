# backend/app/services/rag/answer_question.py

import os
from typing import Optional, List
from pinecone import Pinecone, ServerlessSpec

# If you are using langchain_community for ChatOpenAI:
from langchain_community.chat_models import ChatOpenAI

from ..pinecone_db.main import init_pinecone

# Or, if you're using official LangChain:
# from langchain.chat_models import ChatOpenAI

# Import your config variables
from ..config import (
    PINECONE_API_KEY,
    PINECONE_ENV,
    PINECONE_INDEX_NAME,
    PINECONE_EMBEDDING_DIMENSIONS,
    OPENAI_API_KEY
)

# Import your existing embedding function
# e.g. from backend/app/services/embeddings/generate_embeddings.py
from ..embeddings.generate_embeddings import get_embedding_function

#############################################################################
# MAIN FUNCTION: ANSWER A QUESTION
#############################################################################

def answer_question(question,
                    top_k,
                    threshold,
                    temperature,
                    max_tokens,
                    response_style,
                    namespace,
                    model_name):
    """
    1) Embed the user question with get_embedding_function().
    2) Query Pinecone for top_k relevant chunks (distance < threshold).
    3) Build a final prompt with those chunks as context.
    4) Ask the OpenAI model (via ChatOpenAI) and return the answer in Markdown.
    """
    
    print(f"The rag received the following question: {question}")
    print(f"top_k: {top_k}, threshold: {threshold}, temperature: {temperature}, max_tokens: {max_tokens}, response_style: {response_style}, namespace: {namespace}, model_name: {model_name}")  

    # 1) Embed the user question
    embedding_func = get_embedding_function()
    try:
        question_embedding = embedding_func.embed_query(question)
    except Exception as e:
        print(f"Error embedding query: {e}")
        return "Unable to embed your question at this time."

    if not question_embedding:
        return "Got an empty embedding for your question."

    # 2) Query Pinecone with the user question embedding
    index = init_pinecone()
    query_response = index.query(
        vector=question_embedding,
        top_k=top_k,
        include_metadata=True,
        namespace=namespace
    )

    matches = query_response.get("matches", [])
    relevant_chunks = []
    for match in matches:
        score = match["score"]
        metadata = match.get("metadata", {})
        text_chunk = metadata.get("text", "")

        if score >= threshold:  # Only include chunks with a score >= threshold
            relevant_chunks.append(text_chunk)

    if relevant_chunks:
        context_text = "\n\n---\n\n".join(relevant_chunks)
    else:
        context_text = ""

    # Adjust system prompt based on response_style
    if response_style == "concise":
        system_prompt = """You are a helpful AI assistant. Provide a concise answer to the question using the context if relevant. If the context doesn't help, answer from your own knowledge. Provide the answer in Markdown format."""
    elif response_style == "technical":
        system_prompt = """You are a technical AI assistant. Provide a detailed and technical answer to the question using the context if relevant. If the context doesn't help, answer from your own knowledge. Provide the answer in Markdown format."""
    elif response_style == "casual":
        system_prompt = """You are a friendly AI assistant. Provide a casual and easy-to-understand answer to the question using the context if relevant. If the context doesn't help, answer from your own knowledge. Provide the answer in Markdown format."""
    else:  # Default to "detailed"
        system_prompt = """You are a helpful AI assistant. Provide a detailed answer to the question using the context if relevant. If the context doesn't help, answer from your own knowledge. Provide the answer in Markdown format."""

    user_prompt = f"Context:\n{context_text}\n\nQuestion:\n{question}"

    llm = ChatOpenAI(
        openai_api_key=OPENAI_API_KEY,
        model=model_name,
        temperature=temperature,
        max_tokens=max_tokens
    )

    messages = [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": user_prompt}
    ]

    response = llm.invoke(messages)
    final_answer = getattr(response, "content", str(response))

    return final_answer.strip()

#############################################################################
# SAMPLE USAGE (CLI)
#############################################################################

if __name__ == "__main__":
    # Example question
    sample_question = "how to win at game of life?"
    answer = answer_question(
        question=sample_question,
        top_k=5,
        threshold=0.9,
        namespace="my-namespace"
    )
    print("\nFINAL ANSWER (Markdown):\n")
    print(answer)
