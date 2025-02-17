# app/vector_db/pinecone_db.py
import os
import shutil
import uuid
import logging
from typing import List, Optional, Dict

from app.clients import pinecone_index
from app.config import RAW_DATA_PATH, PROCESSED_DATA_PATH

logger = logging.getLogger(__name__)

BM25_JSON_PATH = "bm25_values.json"

def delete_all_data(namespace: Optional[str] = None):
    index = pinecone_index
    index.delete(delete_all=True, namespace=namespace)
    logger.info(f"Deleted all data{' in namespace ' + namespace if namespace else ''}.")

def process_chunks_and_upsert(processed_documents: List[Dict], namespace: Optional[str] = None):
    """
    Processes document chunks, generates both dense and sparse embeddings,
    upserts them to Pinecone, and updates the BM25 encoder state stored in a JSON file.
    """
    from app.utils.generate_embeddings import get_embedding_function
    from pinecone_text.sparse import BM25Encoder

    # Gather all chunk texts from the processed documents.
    all_chunk_texts = []
    for doc in processed_documents:
        for chunk in doc.get("chunks", []):
            all_chunk_texts.append(chunk["chunk_data"])

    # Initialize and fit the BM25 encoder.
    bm25_encoder = BM25Encoder()
    if all_chunk_texts:
        try:
            bm25_encoder.fit(all_chunk_texts)
            print(f"DEBUG: BM25Encoder fitted on corpus with {len(all_chunk_texts)} texts.")
        except Exception as fit_err:
            print(f"DEBUG: Error fitting BM25Encoder: {fit_err}")
            bm25_encoder = BM25Encoder().default()
            print("DEBUG: Using default BM25Encoder values due to fitting error.")
    else:
        bm25_encoder = BM25Encoder().default()
        print("DEBUG: No chunk texts found; using default BM25Encoder values.")

    # Dump the BM25 encoder state to JSON.
    try:
        bm25_encoder.dump(BM25_JSON_PATH)
        print(f"DEBUG: BM25 encoder state saved to {BM25_JSON_PATH}")
    except Exception as e:
        print(f"DEBUG: Error dumping BM25 encoder state: {e}")

    # Obtain the dense embedding function.
    try:
        dense_embedding_func = get_embedding_function()
        print("DEBUG: Obtained dense embedding function successfully.")
    except Exception as e:
        print(f"DEBUG: Error obtaining dense embedding function: {e}")
        return

    index = pinecone_index

    # Process each document and upsert its vectors.
    for doc in processed_documents:
        pdf_name = doc["pdf_name"]
        tags = doc["tags"]
        chunks = doc.get("chunks", [])
        chunk_texts = [chunk["chunk_data"] for chunk in chunks]

        try:
            dense_embeddings = dense_embedding_func.embed_documents(chunk_texts)
            print(f"DEBUG: Generated dense embeddings for {len(chunk_texts)} chunks in '{pdf_name}'.")
            sparse_embeddings = bm25_encoder.encode_documents(chunk_texts)
            print(f"DEBUG: Generated sparse embeddings for {len(chunk_texts)} chunks in '{pdf_name}'.")
        except Exception as e:
            print(f"DEBUG: Error generating embeddings for '{pdf_name}': {e}")
            continue

        vectors = []
        for i, (chunk, dense_embedding, sparse_embedding) in enumerate(
            zip(chunks, dense_embeddings, sparse_embeddings)
        ):
            try:
                vector_id = str(uuid.uuid4())
                print(f"DEBUG: Processing chunk {i} for '{pdf_name}'.")

                # Convert dense embedding to a list if needed.
                dense_values = dense_embedding.tolist() if hasattr(dense_embedding, "tolist") else dense_embedding

                # Ensure sparse_embedding is in the proper format.
                if isinstance(sparse_embedding, dict):
                    sparse_values = sparse_embedding
                else:
                    sparse_values = {
                        "indices": list(range(len(sparse_embedding))),
                        "values": sparse_embedding
                    }
                
                vector = {
                    "id": vector_id,
                    "values": dense_values,
                    "sparse_values": sparse_values,
                    "metadata": {
                        "text": chunk["chunk_data"],
                        "source_file": pdf_name,
                        "page_number": chunk["page_num"],
                        "subjects": ", ".join(tags)
                    }
                }
                vectors.append(vector)
            except Exception as e:
                print(f"DEBUG: Error processing chunk {i} for '{pdf_name}': {e}")
                continue

        if vectors:
            try:
                index.upsert(vectors=vectors, namespace=namespace)
                print(f"DEBUG: Hybrid upserted {len(vectors)} vectors from '{pdf_name}'.")
            except Exception as e:
                print(f"DEBUG: Error upserting vectors for '{pdf_name}': {e}")

        try:
            src_path = os.path.join(RAW_DATA_PATH, pdf_name)
            dest_path = os.path.join(PROCESSED_DATA_PATH, pdf_name)
            shutil.move(src_path, dest_path)
            print(f"DEBUG: Moved processed PDF to: {dest_path}")
        except Exception as move_err:
            print(f"DEBUG: Error moving PDF '{pdf_name}' to processed dir: {move_err}")

    print("DEBUG: ✅ Done. All documents have been processed and moved.")
