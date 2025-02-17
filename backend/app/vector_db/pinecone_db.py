# app/services/pinecone_db/main.py
import os
import shutil
import uuid
import logging
from typing import List, Optional, Dict
from app.utils.generate_embeddings import get_embedding_function
from app.clients import pinecone_index
from app.config import (
    RAW_DATA_PATH,
    PROCESSED_DATA_PATH,
)

logger = logging.getLogger(__name__)

def delete_all_data(namespace: Optional[str] = None):
    """
    Deletes all vectors in the Pinecone index for a given namespace (or entire index if None).
    """
    index = pinecone_index
    index.delete(delete_all=True, namespace=namespace)
    logger.info(
        f"Deleted all data{' in namespace ' + namespace if namespace else ''}.")

def process_chunks_and_upsert(processed_documents: List[Dict], namespace: Optional[str] = None):
    """
    Takes processed document data and upserts to Pinecone
    """
    embedding_func = get_embedding_function()
    index = pinecone_index

    for doc in processed_documents:
        pdf_name = doc["pdf_name"]
        tags = doc["tags"]
        chunks = doc["chunks"]
        
        # Get text from chunks for embedding
        chunk_texts = [chunk["chunk_data"] for chunk in chunks]
        
        try:
            # Generate embeddings
            embeddings = embedding_func.embed_documents(chunk_texts)
            
            # Prepare vectors for upsert
            vectors = []
            for i, (chunk, embedding) in enumerate(zip(chunks, embeddings)):
                vector_id = str(uuid.uuid4())
                logger.info(f"Processing chunk {i} for '{pdf_name}'")
                
                vectors.append({
                    "id": vector_id,
                    "values": embedding,
                    "metadata": {
                        "text": chunk["chunk_data"],
                        "source_file": pdf_name,
                        "page_number": chunk["page_num"],
                        "subjects": ", ".join(tags)
                    }
                })
            
            # Batch upsert vectors
            if vectors:
                index.upsert(vectors=vectors, namespace=namespace)
                logger.info(f"Batch upserted {len(vectors)} vectors from '{pdf_name}'.")
            
            # Move processed file
            src_path = os.path.join(RAW_DATA_PATH, pdf_name)
            dest_path = os.path.join(PROCESSED_DATA_PATH, pdf_name)
            try:
                shutil.move(src_path, dest_path)
                logger.info(f"Moved processed PDF to: {dest_path}")
            except Exception as e:
                logger.error(f"Error moving PDF '{pdf_name}' to processed dir: {e}")
                
        except Exception as e:
            logger.error(f"Error processing '{pdf_name}': {e}")
            continue

    logger.info("✅ Done. All documents have been processed and moved.")