# app/routes/upload.py
import os
from fastapi import APIRouter, HTTPException, UploadFile, File, Form
from app.vector_db.pinecone_db import process_chunks_and_upsert
from app.utils.document_processor import process_pdf_files
from app.config import RAW_DATA_PATH, PROCESSED_DATA_PATH

router = APIRouter()

@router.post("/upload")
async def upload_files(
    files: list[UploadFile] = File(...),
    subjects: str = Form(None)
):
    try:
        os.makedirs(RAW_DATA_PATH, exist_ok=True)
        os.makedirs(PROCESSED_DATA_PATH, exist_ok=True)

        # Save files temporarily and collect paths
        file_paths = []
        for file in files:
            file_path = os.path.join(RAW_DATA_PATH, file.filename)
            content = await file.read()
            with open(file_path, "wb") as f:
                f.write(content)
            file_paths.append(file_path)

        # Process PDFs through document chunker
        try:
            processed_documents = process_pdf_files(file_paths)

            # Send to Pinecone for processing
            process_chunks_and_upsert(
                processed_documents,
                namespace="my-namespace"
            )

            return {
                "message": "Files uploaded and processed successfully",
                "files": [f.filename for f in files]
            }

        except Exception as process_error:
            return {
                "message": "Files uploaded but processing failed",
                "error": str(process_error),
                "files": [f.filename for f in files]
            }

    except Exception as upload_error:
        raise HTTPException(
            status_code=500,
            detail=f"Upload failed: {str(upload_error)}"
        )
