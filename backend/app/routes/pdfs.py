# app/routes/pdfs.py

import os
from typing import Optional
from fastapi import APIRouter, HTTPException, Query
from fastapi.responses import FileResponse
from app.config import PROCESSED_DATA_PATH

router = APIRouter()


@router.get("/get-pdfs")
def pdf_endpoint(filename: Optional[str] = Query(None)):
    """
    If 'filename' is not provided => Return JSON list of PDFs.
    If 'filename' is provided => Return the PDF file as FileResponse.
    """
    try:
        if filename is None:
            if not os.path.isdir(PROCESSED_DATA_PATH):
                return {"files": []}
            files = [f for f in os.listdir(
                PROCESSED_DATA_PATH) if f.lower().endswith(".pdf")]
            return {"files": files}

        pdf_path = os.path.join(PROCESSED_DATA_PATH, filename)
        if not os.path.isfile(pdf_path) or not filename.lower().endswith(".pdf"):
            raise HTTPException(status_code=404, detail="PDF not found")
        return FileResponse(pdf_path, media_type="application/pdf")
    except Exception as e:
        if isinstance(e, HTTPException):
            raise e
        raise HTTPException(status_code=500, detail=str(e))
