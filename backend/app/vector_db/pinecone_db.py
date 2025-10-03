import os
import shutil
import uuid
import logging
from typing import List, Optional, Dict
from app.clients.pinecone_client import pinecone_client, pinecone_index
from app.config import RAW_DATA_PATH, PROCESSED_DATA_PATH, BM25_JSON_VALUES

logger = logging.getLogger(__name__)

# Ensure the BM25 encoder directory exists
os.makedirs(BM25_JSON_VALUES, exist_ok=True)
BM25_JSON_PATH = os.path.join(BM25_JSON_VALUES, "bm25_values.json")

def delete_all_data(namespace: Optional[str] = None):
    index = pinecone_index
    index.delete(delete_all=True, namespace=namespace)
    logger.info("Deleted all data%s.", f" in namespace {namespace}" if namespace else "")

def process_chunks_and_upsert(processed_documents: List[Dict], namespace: Optional[str] = None):
    """
    Processes document chunks, generates both dense and sparse embeddings,
    upserts them to Pinecone, and updates the BM25 encoder state stored in a JSON file.

    Optimizations:
    - Batch embedding generation for efficiency
    - Error handling per document to avoid failing entire batch
    - Optimized batch size for Pinecone upserts
    """
    from app.clients.openai_embeddings import get_embedding_function
    from pinecone_text.sparse import BM25Encoder

    if not processed_documents:
        logger.warning("No documents to process")
        return

    # Gather all chunk texts from the processed documents.
    all_chunk_texts = []
    for doc in processed_documents:
        for chunk in doc.get("chunks", []):
            all_chunk_texts.append(chunk["chunk_data"])

    logger.info(f"Processing {len(all_chunk_texts)} total chunks from {len(processed_documents)} documents")

    # Initialize and fit the BM25 encoder.
    bm25_encoder = BM25Encoder()
    if all_chunk_texts:
        try:
            bm25_encoder.fit(all_chunk_texts)
            logger.info(f"BM25Encoder fitted on corpus with {len(all_chunk_texts)} texts")
        except Exception as fit_err:
            logger.error("Error fitting BM25Encoder: %s", fit_err, exc_info=True)
            bm25_encoder = BM25Encoder().default()
            logger.warning("Using default BM25Encoder values due to fitting error")
    else:
        bm25_encoder = BM25Encoder().default()
        logger.info("No chunk texts found; using default BM25Encoder values")

    # Dump the BM25 encoder state to JSON.
    try:
        bm25_encoder.dump(BM25_JSON_PATH)
        logger.info(f"BM25 encoder state saved to {BM25_JSON_PATH}")
    except Exception as e:
        logger.error("Error dumping BM25 encoder state: %s", e, exc_info=True)

    # Obtain the dense embedding function.
    try:
        dense_embedding_func = get_embedding_function()
        logger.info("Dense embedding function obtained successfully")
    except Exception as e:
        logger.error("Error obtaining dense embedding function: %s", e, exc_info=True)
        return

    index = pinecone_index
    total_vectors_upserted = 0

    # Process each document and upsert its vectors.
    for doc_idx, doc in enumerate(processed_documents, 1):
        pdf_name = doc["pdf_name"]
        tags = doc["tags"]
        chunks = doc.get("chunks", [])

        if not chunks:
            logger.warning(f"Document '{pdf_name}' has no chunks, skipping")
            continue

        chunk_texts = [chunk["chunk_data"] for chunk in chunks]
        logger.info(f"Processing document {doc_idx}/{len(processed_documents)}: '{pdf_name}' ({len(chunk_texts)} chunks)")

        try:
            # Batch embedding generation (already optimized by OpenAI client)
            dense_embeddings = dense_embedding_func.embed_documents(chunk_texts)
            logger.debug(f"Generated dense embeddings for {len(chunk_texts)} chunks")

            sparse_embeddings = bm25_encoder.encode_documents(chunk_texts)
            logger.debug(f"Generated sparse embeddings for {len(chunk_texts)} chunks")
        except Exception as e:
            logger.error(f"Error generating embeddings for '{pdf_name}': {e}", exc_info=True)
            continue

        vectors = []
        for i, (chunk, dense_embedding, sparse_embedding) in enumerate(
            zip(chunks, dense_embeddings, sparse_embeddings)
        ):
            try:
                vector_id = str(uuid.uuid4())

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
                logger.error(f"Error processing chunk {i} for '{pdf_name}': {e}", exc_info=True)
                continue

        if vectors:
            try:
                # Optimized batch size for Pinecone (100 is recommended)
                BATCH_SIZE = 100
                batches_count = (len(vectors) + BATCH_SIZE - 1) // BATCH_SIZE

                for batch_idx in range(0, len(vectors), BATCH_SIZE):
                    batch = vectors[batch_idx:batch_idx+BATCH_SIZE]
                    index.upsert(vectors=batch, namespace=namespace)
                    total_vectors_upserted += len(batch)
                    logger.debug(f"Upserted batch {(batch_idx//BATCH_SIZE)+1}/{batches_count} ({len(batch)} vectors) for '{pdf_name}'")

                logger.info(f"Successfully upserted {len(vectors)} vectors for '{pdf_name}'")
            except Exception as e:
                logger.error(f"Error upserting vectors for '{pdf_name}': {e}", exc_info=True)
                continue

        # Note: Files are not saved locally anymore, using temp files only
        logger.debug(f"Completed processing '{pdf_name}' (temp file will be auto-cleaned)")

    logger.info(f"Processing complete. Total vectors upserted: {total_vectors_upserted}")
