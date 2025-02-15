# app/routes/upload.py

import os
from fastapi import APIRouter, HTTPException, UploadFile, File, Form
from app.vector_db.pinecone_db import process_and_push_all_pdfs
from app.config import RAW_DATA_PATH, PROCESSED_DATA_PATH
from app.utils.subjects_classifier import detect_subjects
from app.utils.document_chunker import _load_and_split_single_pdf

router = APIRouter()


@router.post("/upload")
async def upload_files(
    files: list[UploadFile] = File(...),
    subjects: str = Form(None)
):
    try:
        os.makedirs(RAW_DATA_PATH, exist_ok=True)
        os.makedirs(PROCESSED_DATA_PATH, exist_ok=True)

        file_names = []
        for file in files:
            file_path = os.path.join(RAW_DATA_PATH, file.filename)
            content = await file.read()
            with open(file_path, "wb") as f:
                f.write(content)
            file_names.append(file.filename)

        # Process PDFs after upload with the provided or detected subjects.
        try:
            print("Processing and pushing PDFs to Pinecone with subjects:", subjects)
            process_and_push_all_pdfs(
                namespace="my-namespace", subjects=subjects)
            return {
                "message": "Files uploaded and processed successfully",
                "files": file_names,
                "subjects": subjects
            }
        except Exception as process_error:
            return {
                "message": "Files uploaded but processing failed",
                "error": str(process_error),
                "files": file_names
            }

    except Exception as upload_error:
        raise HTTPException(
            status_code=500, detail=f"Upload failed: {str(upload_error)}")
