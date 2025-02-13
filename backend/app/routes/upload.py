import os
import aiofiles
import shutil
from fastapi import APIRouter, HTTPException, UploadFile, File
from app.vector_search_db.pinecone_db import PineconeDB
from app.utils.document_loader import DocumentLoader

router = APIRouter()
pinecone_db = PineconeDB()
load_document = DocumentLoader()

# Define the directories (adjust paths as needed)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
UPLOAD_DIR = os.path.join(BASE_DIR, "data", "raw")
PROCESSED_DIR = os.path.join(BASE_DIR, "data", "processed")
os.makedirs(UPLOAD_DIR, exist_ok=True)
os.makedirs(PROCESSED_DIR, exist_ok=True)

@router.post("/upload")
async def upload_files(files: list[UploadFile] = File(...)):
    try:
        file_paths = []
        # Save each file to disk in the raw folder
        for file in files:
            file_path = os.path.join(UPLOAD_DIR, file.filename)
            file_paths.append(file_path)
            async with aiofiles.open(file_path, "wb") as out_file:
                content = await file.read()  # Read the uploaded file content
                await out_file.write(content)  # Save the file content to disk

        # Process the saved files.
        docs = await load_document.load_pdf_documents(file_paths=file_paths)
        await pinecone_db.upsert_documents_with_similarity_check(docs)
        
        # After successful processing, move each file from raw to processed.
        for file in files:
            raw_file_path = os.path.join(UPLOAD_DIR, file.filename)
            processed_file_path = os.path.join(PROCESSED_DIR, file.filename)
            try:
                shutil.move(raw_file_path, processed_file_path)
            except Exception as e:
                print(f"Error moving file {file.filename}: {e}")
        
        return {
            "message": "Files uploaded, processed, and moved successfully",
            "files": [file.filename for file in files]
        }

    except Exception as process_error:
        raise HTTPException(
            status_code=500,
            detail=f"An error occurred during file processing: {str(process_error)}"
        )
