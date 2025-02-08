# backend/app/services/pinecone_db/main.py

import os
import uuid
from typing import List, Optional, Dict

# Pinecone v2 imports
from pinecone import Pinecone, ServerlessSpec

# Local imports from your existing code
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

############################################
# PINECONE INITIALIZATION (v2)
############################################
def init_pinecone():
    """
    Initializes a Pinecone client using your API key and environment from config.
    Creates (or retrieves) the index if needed, returning a pinecone.Index object.
    """
    if not PINECONE_API_KEY or not PINECONE_ENV:
        raise ValueError("Missing Pinecone credentials. Check config or environment variables.")

    pc = Pinecone(api_key=PINECONE_API_KEY)

    # Check existing indexes
    existing_indexes = [idx.name for idx in pc.list_indexes()]
    if PINECONE_INDEX_NAME not in existing_indexes:
        print(f"Index '{PINECONE_INDEX_NAME}' not found. Creating it now...")
        pc.create_index(
            name=PINECONE_INDEX_NAME,
            dimension=PINECONE_EMBEDDING_DIMENSIONS,
            metric="cosine",  # or "dotproduct", "euclidean" as needed
            spec=ServerlessSpec(
                region=PINECONE_ENV,
                cloud="aws"      # default is 'aws'
            )
        )
    return pc.Index(PINECONE_INDEX_NAME)


############################################
# SIMILARITY-CHECK UPSERT
############################################
def upsert_chunk_with_similarity_check(
    index,
    embedding: List[float],
    chunk_text: str,
    metadata: Optional[Dict] = None,
    namespace: Optional[str] = None
):
    """
    Query Pinecone for the most similar chunk to 'embedding'.
      - If similarity == 1.0, skip (identical chunk already exists).
      - If similarity >= 0.99999, upsert using the existing ID (update).
      - Otherwise, insert a new ID.
    """
    if not embedding:
        print("No embedding provided. Skipping.")
        return

    # Query top 1 to see if there's an almost-identical vector
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

    # Decide how to upsert based on matched_score
    if matched_score >= EXACT_MATCH_THRESHOLD:
        # If score == 1.0, skip
        print(f"Skipping chunk (score=1.0). Identical chunk exists.")
        return
    elif matched_score >= SIMILARITY_THRESHOLD:
        # If score >= 0.99999 (and < 1.0), update the existing chunk
        vector_id = matched_id
        print(f"Updating chunk (score={matched_score:.5f}) with existing ID={vector_id}.")
    else:
        # Otherwise, insert a new vector
        vector_id = str(uuid.uuid4())
        print(f"Inserting new chunk (score={matched_score:.5f}). ID={vector_id}.")

    # Construct the vector data
    upsert_vector = {
        "id": vector_id,
        "values": embedding,
        "metadata": {
            "text": chunk_text
        }
    }
    if metadata:
        upsert_vector["metadata"].update(metadata)

    # Upsert to Pinecone (insert or update)
    index.upsert(vectors=[upsert_vector], namespace=namespace)


############################################
# EMBED + UPSERT (WITH SIMILARITY CHECK)
############################################
def embed_and_upsert_chunks(pdf_path: str, namespace: Optional[str] = None):
    """
    1. Splits the PDF into chunks (via load_and_split_pdf).
    2. Embeds each chunk using get_embedding_function().
    3. Calls upsert_chunk_with_similarity_check for each chunk.
    """
    docs = load_and_split_pdf(pdf_path)
    if not docs:
        print(f"No chunks created or error reading PDF: {pdf_path}")
        return

    print(f"Loaded and split '{os.path.basename(pdf_path)}' into {len(docs)} chunks.")

    embedding_func = get_embedding_function()
    index = init_pinecone()

    for doc in docs:
        chunk_text = doc.page_content.strip()
        if not chunk_text:
            continue

        try:
            # embed_documents returns a list of embeddings, we want the first
            embedding = embedding_func.embed_documents([chunk_text])[0]
        except Exception as e:
            print(f"Error embedding chunk: {e}")
            continue

        if embedding:
            # Provide optional metadata
            chunk_metadata = {"source_file": os.path.basename(pdf_path)}
            upsert_chunk_with_similarity_check(
                index=index,
                embedding=embedding,
                chunk_text=chunk_text,
                metadata=chunk_metadata,
                namespace=namespace
            )


############################################
# MAIN PIPELINE
############################################
def process_and_push_all_pdfs(namespace: Optional[str] = None):
    """
    1. Convert raw docs (docx/img -> PDF) to the processed folder.
    2. For each PDF in processed, embed & upsert chunks into Pinecone with similarity checks.
    """
    # 1) Convert all raw docs to PDF in processed
    print(f"[STEP 1] Converting documents from '{RAW_DATA_PATH}' to '{PROCESSED_DATA_PATH}'...")
    convert_all_docs_in_raw_folder()

    # 2) Embed + upsert each PDF
    print(f"\n[STEP 2] Embedding & upserting PDFs from '{PROCESSED_DATA_PATH}' into Pinecone...")
    for filename in os.listdir(PROCESSED_DATA_PATH):
        if filename.lower().endswith(".pdf"):
            pdf_path = os.path.join(PROCESSED_DATA_PATH, filename)
            embed_and_upsert_chunks(pdf_path, namespace=namespace)
    print("\n✅ Done. All PDFs processed and uploaded to Pinecone.")


############################################
# CLI ENTRY POINT
############################################
if __name__ == "__main__":
    # Run as: python -m backend.app.services.pinecone_db.main
    # This will process all docs in RAW_DATA_PATH and push them into Pinecone.
    process_and_push_all_pdfs(namespace="my-namespace")
