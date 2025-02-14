# app/routes/upload.py

import os
from fastapi import APIRouter, HTTPException, UploadFile, File
from app.vector_db.pinecone_db import process_and_push_all_pdfs
from app.config import RAW_DATA_PATH, PROCESSED_DATA_PATH

router = APIRouter()

@router.post("/upload")
async def upload_files(files: list[UploadFile] = File(...)):
    try:
        # Save each uploaded file
        for file in files:
            file_path = os.path.join(RAW_DATA_PATH, file.filename)
            content = await file.read()
            with open(file_path, "wb") as f:
                f.write(content)
        
        # Process PDFs after upload
        try:
            print("Processing and pushing PDFs to Pinecone...")
            process_and_push_all_pdfs(namespace="my-namespace")
            return {
                "message": "Files uploaded and processed successfully",
                "files": [file.filename for file in files]
            }
        except Exception as process_error:
            return {
                "message": "Files uploaded but processing failed",
                "error": str(process_error),
                "files": [file.filename for file in files]
            }
            
    except Exception as upload_error:
        raise HTTPException(status_code=500, detail=f"Upload failed: {str(upload_error)}")
