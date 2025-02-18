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
    """
    from app.clients.openai_embeddings import get_embedding_function
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
            logger.debug("BM25Encoder fitted on corpus with %d texts.", len(all_chunk_texts))
        except Exception as fit_err:
            logger.error("Error fitting BM25Encoder: %s", fit_err, exc_info=True)
            bm25_encoder = BM25Encoder().default()
            logger.debug("Using default BM25Encoder values due to fitting error.")
    else:
        bm25_encoder = BM25Encoder().default()
        logger.debug("No chunk texts found; using default BM25Encoder values.")

    # Dump the BM25 encoder state to JSON.
    try:
        bm25_encoder.dump(BM25_JSON_PATH)
        logger.debug("BM25 encoder state saved to %s", BM25_JSON_PATH)
    except Exception as e:
        logger.error("Error dumping BM25 encoder state: %s", e, exc_info=True)

    # Obtain the dense embedding function.
    try:
        dense_embedding_func = get_embedding_function()
        logger.debug("Obtained dense embedding function successfully.")
    except Exception as e:
        logger.error("Error obtaining dense embedding function: %s", e, exc_info=True)
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
            logger.debug("Generated dense embeddings for %d chunks in '%s'.", len(chunk_texts), pdf_name)
            sparse_embeddings = bm25_encoder.encode_documents(chunk_texts)
            logger.debug("Generated sparse embeddings for %d chunks in '%s'.", len(chunk_texts), pdf_name)
        except Exception as e:
            logger.error("Error generating embeddings for '%s': %s", pdf_name, e, exc_info=True)
            continue

        vectors = []
        for i, (chunk, dense_embedding, sparse_embedding) in enumerate(
            zip(chunks, dense_embeddings, sparse_embeddings)
        ):
            try:
                vector_id = str(uuid.uuid4())
                logger.debug("Processing chunk %d for '%s'.", i, pdf_name)

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
                logger.error("Error processing chunk %d for '%s': %s", i, pdf_name, e, exc_info=True)
                continue

        if vectors:
            try:
                index.upsert(vectors=vectors, namespace=namespace)
                logger.debug("Hybrid upserted %d vectors from '%s'.", len(vectors), pdf_name)
            except Exception as e:
                logger.error("Error upserting vectors for '%s': %s", pdf_name, e, exc_info=True)

        try:
            src_path = os.path.join(RAW_DATA_PATH, pdf_name)
            dest_path = os.path.join(PROCESSED_DATA_PATH, pdf_name)
            shutil.move(src_path, dest_path)
            logger.debug("Moved processed PDF to: %s", dest_path)
        except Exception as move_err:
            logger.error("Error moving PDF '%s' to processed dir: %s", pdf_name, move_err, exc_info=True)

    logger.info("All documents have been processed and moved.")
