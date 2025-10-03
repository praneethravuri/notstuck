import logging
import tempfile
import os
from fastapi import HTTPException, UploadFile
from typing import List
from app.vector_db.pinecone_db import process_chunks_and_upsert
from app.services.document_services import process_pdf_files

logger = logging.getLogger(__name__)

def process_and_upsert_direct(files: List[UploadFile], namespace: str = "my-namespace"):
    """
    Process PDF files directly from upload without saving to disk.
    Uses temporary files that are automatically cleaned up.

    Args:
        files: List of uploaded files
        namespace: Pinecone namespace to upsert to

    Returns:
        Number of files processed
    """
    temp_files = []
    try:
        logger.info(f"Processing {len(files)} file(s) directly from upload")

        # Create temporary files for processing
        file_paths = []
        for file in files:
            # Create temp file
            temp_file = tempfile.NamedTemporaryFile(mode='wb', suffix='.pdf', delete=False)
            content = file.file.read()
            temp_file.write(content)
            temp_file.close()

            temp_files.append(temp_file.name)
            file_paths.append(temp_file.name)
            logger.debug(f"Created temp file for '{file.filename}': {temp_file.name}")

        # Process PDFs from temp files
        logger.info("Starting PDF processing...")
        processed_documents = process_pdf_files(file_paths)

        logger.info(f"Processing complete. Upserting to Pinecone namespace '{namespace}'")
        process_chunks_and_upsert(processed_documents, namespace=namespace)

        logger.info(f"Successfully processed and upserted {len(files)} file(s)")
        return len(processed_documents)

    except Exception as process_error:
        logger.error(f"Error processing files: {process_error}", exc_info=True)
        raise HTTPException(status_code=500, detail=f"Processing failed: {process_error}")

    finally:
        # Clean up temporary files
        for temp_file in temp_files:
            try:
                if os.path.exists(temp_file):
                    os.unlink(temp_file)
                    logger.debug(f"Cleaned up temp file: {temp_file}")
            except Exception as cleanup_err:
                logger.warning(f"Could not delete temp file {temp_file}: {cleanup_err}")
