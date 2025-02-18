import os
import logging
from fastapi import HTTPException
from app.config import PROCESSED_DATA_PATH

logger = logging.getLogger(__name__)

def list_pdfs():
    """Return a list of PDF filenames from the processed directory."""
    if not os.path.isdir(PROCESSED_DATA_PATH):
        logger.warning("Processed data path '%s' is not a directory.", PROCESSED_DATA_PATH)
        return []
    
    files = [f for f in os.listdir(PROCESSED_DATA_PATH) if f.lower().endswith(".pdf")]
    logger.info("Found %d PDF(s) in '%s'.", len(files), PROCESSED_DATA_PATH)
    return files

def get_pdf_path(filename: str) -> str:
    """Construct and validate the full PDF path."""
    pdf_path = os.path.join(PROCESSED_DATA_PATH, filename)
    if not os.path.isfile(pdf_path) or not filename.lower().endswith(".pdf"):
        logger.error("PDF '%s' not found at path '%s'.", filename, pdf_path)
        raise HTTPException(status_code=404, detail="PDF not found")
    
    logger.info("PDF '%s' found at path '%s'.", filename, pdf_path)
    return pdf_path
