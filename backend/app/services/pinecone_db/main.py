# backend/app/services/pinecone_db/main.py

import os
import uuid
from typing import List

# Pinecone v2 imports
from pinecone import Pinecone, ServerlessSpec

# Import your config parameters
from backend.config import (
    RAW_DATA_PATH,
    PROCESSED_DATA_PATH,
    PINECONE_API_KEY,
    PINECONE_ENV,
    PINECONE_INDEX_NAME,
    PINECONE_EMBEDDING_DIMENSIONS
)

# Import the chunking and embedding functions
# Adjust these paths if your actual structure is different
from ..document_pipeline.document_chunker import load_and_split_pdf
from ..document_pipeline.document_converter import convert_all_docs_in_raw_folder
from ..embeddings.generate_embeddings import get_embedding_function

def init_pinecone():
    """
    Initializes Pinecone v2 using credentials from config.
    Creates (or retrieves) the index if it doesn't exist yet.
    Returns a Pinecone 'Index' object for upserts/queries.
    """
    if not PINECONE_API_KEY or not PINECONE_ENV:
        raise ValueError("Missing Pinecone credentials. Check your config or environment variables.")

    # Create a Pinecone client instance
    pc = Pinecone(api_key=PINECONE_API_KEY)
    
    # List existing indexes. (pc.list_indexes() returns a list of IndexSummary objects.)
    existing_indexes = [idx.name for idx in pc.list_indexes()]
    
    if PINECONE_INDEX_NAME not in existing_indexes:
        # Create the index if it doesn't exist
        print(f"Index '{PINECONE_INDEX_NAME}' not found. Creating...")
        pc.create_index(
            name=PINECONE_INDEX_NAME,
            dimension=PINECONE_EMBEDDING_DIMENSIONS,
            metric="cosine",   # or "dotproduct", "euclidean"
            # Provide a ServerlessSpec with region = PINECONE_ENV
            # The default cloud is 'aws' so you typically only need region
            spec=ServerlessSpec(
                region=PINECONE_ENV,  
                cloud="aws"
            )
        )

    # Return an Index object from this Pinecone client
    return pc.Index(PINECONE_INDEX_NAME)

def embed_and_upsert_chunks(pdf_path: str, namespace: str = None):
    """
    1. Loads & splits the given PDF into chunks.
    2. Embeds each chunk using OpenAI embeddings.
    3. Upserts each chunk (embedding + metadata) into the Pinecone index.
    """
    # Load and split PDF into chunks
    docs = load_and_split_pdf(pdf_path)
    if not docs:
        print(f"No chunks created or error reading PDF: {pdf_path}")
        return

    print(f"Loaded and split '{os.path.basename(pdf_path)}' into {len(docs)} chunks.")

    # Get embedding function from your generate_embeddings.py
    embedding_func = get_embedding_function()

    # Initialize Pinecone index (v2 style)
    index = init_pinecone()

    vectors_to_upsert = []
    for doc in docs:
        chunk_text = doc.page_content.strip()
        if not chunk_text:
            continue
        
        # Use .embed_documents([text]) or .embed_query(text)
        # depending on your embedding library
        try:
            embedding = embedding_func.embed_documents([chunk_text])[0]
        except Exception as e:
            print(f"Error embedding chunk: {e}")
            continue

        if not embedding:
            continue

        # Create a unique ID for this chunk
        vector_id = str(uuid.uuid4())

        # Additional metadata you might want to store
        chunk_metadata = {
            "source_file": os.path.basename(pdf_path),
            "text": chunk_text
        }

        vectors_to_upsert.append({
            "id": vector_id,
            "values": embedding,
            "metadata": chunk_metadata
        })

    # Upsert into Pinecone
    if vectors_to_upsert:
        index.upsert(vectors=vectors_to_upsert, namespace=namespace)
        print(f"Upserted {len(vectors_to_upsert)} chunks from '{os.path.basename(pdf_path)}' into Pinecone (namespace='{namespace}').")
    else:
        print(f"No vectors to upsert for '{os.path.basename(pdf_path)}'.")

def process_and_push_all_pdfs(namespace: str = None):
    """
    High-level pipeline:
      1. Convert non-PDF docs from RAW_DATA_PATH -> PDF in PROCESSED_DATA_PATH
      2. For each PDF in PROCESSED_DATA_PATH, embed and upsert chunks into Pinecone
    """
    # 1) Convert all raw docs (docx/img -> pdf) and move to processed
    print(f"Converting files in '{RAW_DATA_PATH}' to PDF (if needed) and moving them to '{PROCESSED_DATA_PATH}'...")
    convert_all_docs_in_raw_folder()

    # 2) Iterate over PDFs in processed, embed & upsert to Pinecone
    print(f"\nEmbedding and uploading PDFs from '{PROCESSED_DATA_PATH}'...")
    for filename in os.listdir(PROCESSED_DATA_PATH):
        if filename.lower().endswith(".pdf"):
            pdf_path = os.path.join(PROCESSED_DATA_PATH, filename)
            embed_and_upsert_chunks(pdf_path, namespace=namespace)
    print("\n✅ All PDFs processed and uploaded.")

if __name__ == "__main__":
    # Example usage:
    # Run this file as a script to process all documents in RAW_DATA_PATH,
    # convert them to PDF, chunk, embed, and upload to Pinecone.
    process_and_push_all_pdfs(namespace="my-namespace")
