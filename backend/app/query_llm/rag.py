# app/services/rag/main.py

import logging
from typing import Optional, List
from app.clients import pinecone_index, openai_client as client
from app.config import OPENAI_API_KEY
from app.utils.generate_embeddings import get_embedding_function

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
    reasoning: bool = False
) -> dict:
    """
    1) Embed the user question.
    2) Query Pinecone for top_k relevant chunks (score >= threshold).
    3) Build a prompt with the retrieved context.
    4) Get and return the answer from the ChatGPT model.
    """
    
    logger.info(f"Received question: {question}")
    logger.info(
        f"Parameters: top_k={top_k}, threshold={threshold}, temperature={temperature}, "
        f"max_tokens={max_tokens}, response_style={response_style}, namespace={namespace}, "
        f"model_name={model_name}, reasoning={reasoning}"
    )

    # 1) Embed the user question.
    embedding_func = get_embedding_function()
    try:
        question_embedding = embedding_func.embed_query(question)
    except Exception as e:
        logger.error(f"Error embedding query: {e}")
        return {"answer": "Unable to embed your question at this time.", "relevant_chunks": [], "source_files": []}

    if not question_embedding:
        return {"answer": "Got an empty embedding for your question.", "relevant_chunks": [], "source_files": []}

    # 2) Query Pinecone with the user question embedding.
    # Use the shared Pinecone client instance.
    index = pinecone_index
    try:
        query_response = index.query(
            vector=question_embedding,
            top_k=top_k,
            include_metadata=True,
            namespace=namespace
        )
    except Exception as e:
        logger.error(f"Error querying Pinecone: {e}")
        return {"answer": "Error querying the database.", "relevant_chunks": [], "source_files": []}

    matches = query_response.get("matches", [])
    relevant_chunks: List[str] = []
    source_files: List[str] = []
    for match in matches:
        score = match["score"]
        metadata = match.get("metadata", {})
        text_chunk = metadata.get("text", "")
        source_file = metadata.get("source_file", "unknown source")
        if score >= threshold:
            relevant_chunks.append(text_chunk)
            source_files.append(source_file)

    context_text = "\n\n---\n\n".join(relevant_chunks) if relevant_chunks else ""
    logger.info(f"Found {len(relevant_chunks)} relevant chunks.")

    # 3) Build the prompt.
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
    else:  # Default to "detailed"
        system_prompt = (
            "You are a helpful AI assistant. Provide a detailed answer to the question using the context if relevant. "
            "If the context doesn't help, answer from your own knowledge."
        )

    if reasoning:
        system_prompt += (
            "\n\nProvide a step-by-step reasoning process for your answer. Break down your thought process into clear and logical steps."
        )
    system_prompt += "\n\nProvide the answer in Markdown format."

    user_prompt = f"Context:\n{context_text}\n\nQuestion:\n{question}"
    messages = [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": user_prompt}
    ]
    
    # 4) Call ChatGPT using the shared OpenAI client.
    try:
        response = client.chat.completions.create(
            model=model_name,
            messages=messages,
            temperature=temperature,
            max_completion_tokens=max_tokens
        )
        final_answer = response.choices[0].message.content.strip()
    except Exception as e:
        logger.error(f"Error calling OpenAI API: {e}")
        return {"answer": "There was an error calling the OpenAI API.", "relevant_chunks": [], "source_files": []}

    return {"answer": final_answer, "relevant_chunks": relevant_chunks, "source_files": source_files}

# SAMPLE USAGE (CLI)
if __name__ == "__main__":
    sample_question = "how to win at game of life?"
    result = answer_question(
        question=sample_question,
        top_k=5,
        threshold=0.9,
        temperature=0.7,
        max_tokens=150,
        response_style="detailed",
        namespace="my-namespace",
        model_name="gpt-3.5-turbo",
        reasoning=True
    )
    logger.info("FINAL ANSWER (Markdown):")
    logger.info(result)
