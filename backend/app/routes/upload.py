# app/routes/upload.py

import os
from fastapi import APIRouter, HTTPException, UploadFile, File
from app.services.pinecone_db.main import process_and_push_all_pdfs  # adjust as needed

router = APIRouter()

# Define the upload directory (adjust the path as needed)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
UPLOAD_DIR = os.path.join(BASE_DIR, "data", "raw")
os.makedirs(UPLOAD_DIR, exist_ok=True)

@router.post("/upload")
async def upload_files(files: list[UploadFile] = File(...)):
    try:
        # Save each uploaded file
        for file in files:
            file_path = os.path.join(UPLOAD_DIR, file.filename)
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
