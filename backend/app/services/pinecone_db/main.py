# app/services/pinecone_db/main.py

import os
import shutil
import uuid
import logging
from typing import List, Optional, Dict

from pinecone import Pinecone, ServerlessSpec

from ..config import (
    RAW_DATA_PATH,
    PROCESSED_DATA_PATH,
    PINECONE_API_KEY,
    PINECONE_ENV,
    PINECONE_INDEX_NAME,
    PINECONE_EMBEDDING_DIMENSIONS,
    SIMILARITY_THRESHOLD,
    EXACT_MATCH_THRESHOLD,
)
from ..document_pipeline.document_converter import convert_all_docs_in_raw_folder
from ..document_pipeline.document_chunker import load_and_split_pdf
from ..embeddings.generate_embeddings import get_embedding_function

logger = logging.getLogger(__name__)

def init_pinecone():
    """
    Initializes a Pinecone client and creates (or retrieves) the index.
    """
    if not PINECONE_API_KEY or not PINECONE_ENV:
        raise ValueError("Missing Pinecone credentials. Check config or environment variables.")

    pc = Pinecone(api_key=PINECONE_API_KEY)
    existing_indexes = [idx.name for idx in pc.list_indexes()]
    if PINECONE_INDEX_NAME not in existing_indexes:
        logger.info(f"Index '{PINECONE_INDEX_NAME}' not found. Creating it now...")
        pc.create_index(
            name=PINECONE_INDEX_NAME,
            dimension=PINECONE_EMBEDDING_DIMENSIONS,
            metric="cosine",
            spec=ServerlessSpec(
                region=PINECONE_ENV,
                cloud="aws"
            )
        )
    return pc.Index(PINECONE_INDEX_NAME)

def delete_all_data(namespace: Optional[str] = None):
    """
    Deletes all vectors in the Pinecone index for a given namespace (or entire index if None).
    """
    index = init_pinecone()
    index.delete(delete_all=True, namespace=namespace)
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
    Splits the PDF into chunks, embeds them, and upserts into Pinecone.
    """
    docs = load_and_split_pdf(pdf_path)
    if not docs:
        logger.warning(f"No chunks created or error reading PDF: {pdf_path}")
        return

    logger.info(f"Loaded and split '{os.path.basename(pdf_path)}' into {len(docs)} chunks.")
    embedding_func = get_embedding_function()
    index = init_pinecone()

    for doc in docs:
        chunk_text = doc.page_content.strip()
        if not chunk_text:
            continue

        try:
            embedding = embedding_func.embed_documents([chunk_text])[0]
        except Exception as e:
            logger.error(f"Error embedding chunk: {e}")
            continue

        if embedding:
            chunk_metadata = {"source_file": os.path.basename(pdf_path)}
            upsert_chunk_with_similarity_check(
                index=index,
                embedding=embedding,
                chunk_text=chunk_text,
                metadata=chunk_metadata,
                namespace=namespace
            )

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
