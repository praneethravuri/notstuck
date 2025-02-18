import os
import logging
from typing import Optional
from fastapi import APIRouter, HTTPException, Query
from fastapi.responses import FileResponse
from app.services.pdf_services import list_pdfs, get_pdf_path

router = APIRouter()
logger = logging.getLogger(__name__)

@router.get("/get-pdfs")
def pdf_endpoint(filename: Optional[str] = Query(None)):
    """
    If 'filename' is not provided => Return JSON list of PDFs.
    If 'filename' is provided => Return the PDF file as FileResponse.
    """
    try:
        if filename is None:
            logger.info("Listing available PDFs.")
            files = list_pdfs()
            logger.debug("PDF files found: %s", files)
            return {"files": files}
        
        logger.info("Requesting PDF file: %s", filename)
        pdf_path = get_pdf_path(filename)
        logger.info("Serving PDF file from path: %s", pdf_path)
        return FileResponse(pdf_path, media_type="application/pdf")
    except Exception as e:
        logger.error("Error in pdf_endpoint: %s", e, exc_info=True)
        if isinstance(e, HTTPException):
            raise e
        raise HTTPException(status_code=500, detail=str(e))
