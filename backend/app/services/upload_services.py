import os
import logging
from fastapi import HTTPException
from app.vector_db.pinecone_db import process_chunks_and_upsert
from app.services.document_services import process_pdf_files
from app.config import RAW_DATA_PATH, PROCESSED_DATA_PATH

logger = logging.getLogger(__name__)

def save_files(files):
    """
    Save uploaded files to RAW_DATA_PATH and return a list of file paths.
    """
    os.makedirs(RAW_DATA_PATH, exist_ok=True)
    os.makedirs(PROCESSED_DATA_PATH, exist_ok=True)

    file_paths = []
    for file in files:
        file_path = os.path.join(RAW_DATA_PATH, file.filename)
        try:
            # For synchronous file reading; if using async, use: await file.read()
            content = file.file.read()
            with open(file_path, "wb") as f:
                f.write(content)
            logger.info("File saved successfully: %s", file_path)
            file_paths.append(file_path)
        except Exception as e:
            logger.error("Error saving file %s: %s", file.filename, e, exc_info=True)
            raise HTTPException(status_code=500, detail=f"Error saving file {file.filename}")
    return file_paths

def process_and_upsert(file_paths, namespace: str = "my-namespace"):
    """
    Process PDFs and upsert the chunks to Pinecone.
    Returns processed_documents for potential further use.
    """
    try:
        logger.info("Starting PDF processing for %d file(s).", len(file_paths))
        processed_documents = process_pdf_files(file_paths)
        logger.info("Processing complete. Upserting data to Pinecone in namespace '%s'.", namespace)
        process_chunks_and_upsert(processed_documents, namespace=namespace)
        logger.info("Data upserted to Pinecone successfully.")
        return processed_documents
    except Exception as process_error:
        logger.error("Error processing and upserting files: %s", process_error, exc_info=True)
        raise HTTPException(status_code=500, detail=f"Processing failed: {process_error}")
