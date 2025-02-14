# app/services/pinecone_db/main.py

import os
import shutil
import uuid
import logging
import concurrent.futures
from typing import List, Optional, Dict
from app.utils.document_converter import convert_all_docs_in_raw_folder
from app.utils.document_chunker import load_and_split_pdf
from app.utils.generate_embeddings import get_embedding_function
from app.clients import pinecone_index  # Shared Pinecone client
from app.config import (
    RAW_DATA_PATH,
    PROCESSED_DATA_PATH,
    SIMILARITY_THRESHOLD,
    EXACT_MATCH_THRESHOLD,
)

logger = logging.getLogger(__name__)

def delete_all_data(namespace: Optional[str] = None):
    """
    Deletes all vectors in the Pinecone index for a given namespace (or entire index if None).
    """
    pinecone_index.delete(delete_all=True, namespace=namespace)
    logger.info(f"Deleted all data{' in namespace ' + namespace if namespace else ''}.")

def upsert_chunk_with_similarity_check(
    index,
    embedding: List[float],
    chunk_text: str,
    metadata: Optional[Dict] = None,
    namespace: Optional[str] = None
):
    """
    Queries Pinecone for a similar chunk and decides to skip, update, or insert.
    """
    if not embedding:
        logger.warning("No embedding provided. Skipping upsert.")
        return

    query_result = index.query(
        vector=embedding,
        top_k=1,
        include_metadata=True,
        namespace=namespace
    )

    matched_id = None
    matched_score = 0.0

    if query_result and "matches" in query_result and query_result["matches"]:
        best_match = query_result["matches"][0]
        matched_id = best_match["id"]
        matched_score = best_match["score"]

    if matched_score >= EXACT_MATCH_THRESHOLD:
        logger.info(f"Skipping chunk (score=1.0). Identical chunk exists.")
        return
    elif matched_score >= SIMILARITY_THRESHOLD:
        vector_id = matched_id
        logger.info(f"Updating chunk (score={matched_score:.5f}) with existing ID={vector_id}.")
    else:
        vector_id = str(uuid.uuid4())
        logger.info(f"Inserting new chunk (score={matched_score:.5f}). ID={vector_id}.")

    upsert_vector = {
        "id": vector_id,
        "values": embedding,
        "metadata": {"text": chunk_text}
    }
    if metadata:
        upsert_vector["metadata"].update(metadata)

    index.upsert(vectors=[upsert_vector], namespace=namespace)

def embed_and_upsert_chunks(pdf_path: str, namespace: Optional[str] = None):
    """
    Splits a PDF into chunks, embeds them, runs similarity checks concurrently,
    and then upserts the chunks in batch into Pinecone.
    """
    docs = load_and_split_pdf(pdf_path)
    if not docs:
        logger.warning(f"No chunks created or error reading PDF: {pdf_path}")
        return

    logger.info(f"Loaded and split '{os.path.basename(pdf_path)}' into {len(docs)} chunks.")
    embedding_func = get_embedding_function()
    # Use the shared Pinecone index
    index = pinecone_index

    # Extract non-empty text chunks.
    chunks = [doc.page_content.strip() for doc in docs if doc.page_content.strip()]
    if not chunks:
        logger.warning(f"No valid text found in PDF: {pdf_path}")
        return

    try:
        # Batch embed all chunks at once.
        embeddings = embedding_func.embed_documents(chunks)
    except Exception as e:
        logger.error(f"Error embedding chunks: {e}")
        return

    # Run similarity checks concurrently.
    similarity_results = [None] * len(chunks)
    with concurrent.futures.ThreadPoolExecutor(max_workers=8) as executor:
        # Submit all similarity queries in parallel.
        future_to_index = {
            executor.submit(
                index.query,
                vector=emb,
                top_k=1,
                include_metadata=True,
                namespace=namespace
            ): i for i, emb in enumerate(embeddings)
        }
        for future in concurrent.futures.as_completed(future_to_index):
            i = future_to_index[future]
            try:
                similarity_results[i] = future.result()
            except Exception as exc:
                logger.error(f"Similarity check for chunk {i} generated an exception: {exc}")
                similarity_results[i] = None

    # Build upsert vectors based on similarity checks.
    vectors = []
    for i, (chunk_text, embedding) in enumerate(zip(chunks, embeddings)):
        result = similarity_results[i]
        vector_id = None
        matched_score = 0.0

        if result and "matches" in result and result["matches"]:
            best_match = result["matches"][0]
            matched_score = best_match["score"]
            if matched_score >= EXACT_MATCH_THRESHOLD:
                logger.info(f"Skipping chunk {i} (score=1.0). Identical chunk exists.")
                continue  # Skip upserting this chunk.
            elif matched_score >= SIMILARITY_THRESHOLD:
                vector_id = best_match["id"]
                logger.info(f"Updating chunk {i} (score={matched_score:.5f}) with existing ID={vector_id}.")

        if vector_id is None:
            vector_id = str(uuid.uuid4())
            logger.info(f"Inserting new chunk {i} (score={matched_score:.5f}). ID={vector_id}.")

        vectors.append({
            "id": vector_id,
            "values": embedding,
            "metadata": {
                "text": chunk_text,
                "source_file": os.path.basename(pdf_path)
            }
        })

    try:
        # Batch upsert all vectors at once.
        index.upsert(vectors=vectors, namespace=namespace)
        logger.info(f"Batch upserted {len(vectors)} vectors from '{os.path.basename(pdf_path)}'.")
    except Exception as e:
        logger.error(f"Error during batch upsert: {e}")

def process_and_push_all_pdfs(namespace: Optional[str] = None):
    """
    Pipeline: converts docs to PDFs, embeds & upserts them, and moves processed PDFs.
    """
    if not os.path.exists(PROCESSED_DATA_PATH):
        os.makedirs(PROCESSED_DATA_PATH, exist_ok=True)

    logger.info(f"[STEP 1] Converting documents in '{RAW_DATA_PATH}' to PDFs...")
    convert_all_docs_in_raw_folder()

    logger.info(f"\n[STEP 2] Embedding & upserting PDFs from '{RAW_DATA_PATH}' into Pinecone...")
    for filename in os.listdir(RAW_DATA_PATH):
        if filename.lower().endswith(".pdf"):
            pdf_path = os.path.join(RAW_DATA_PATH, filename)
            embed_and_upsert_chunks(pdf_path, namespace=namespace)

            dest_path = os.path.join(PROCESSED_DATA_PATH, filename)
            try:
                shutil.move(pdf_path, dest_path)
                logger.info(f"Moved processed PDF to: {dest_path}")
            except Exception as e:
                logger.error(f"Error moving PDF '{pdf_path}' to processed dir: {e}")

    logger.info("✅ Done. All documents have been processed and moved.")

if __name__ == "__main__":
    # For production, you can call the pipeline or data deletion as needed:
    # process_and_push_all_pdfs(namespace="my-namespace")
    delete_all_data(namespace="my-namespace")
