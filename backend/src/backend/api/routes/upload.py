"""
Upload endpoint for document processing.
"""

import os
import tempfile
from typing import List
from fastapi import APIRouter, UploadFile, File, HTTPException
from pydantic import BaseModel

from backend.tools.document_processor import DocumentProcessorTool

router = APIRouter()


class UploadResponse(BaseModel):
    """Response model for upload endpoint."""
    message: str
    files_processed: int
    details: List[str]


@router.post("/upload", response_model=UploadResponse)
async def upload_documents(files: List[UploadFile] = File(...)):
    """
    Upload and process documents (PDF, DOCX, TXT).

    Args:
        files: List of files to upload

    Returns:
        UploadResponse with processing details
    """
    if not files:
        raise HTTPException(status_code=400, detail="No files provided")

    # Initialize document processor tool
    doc_processor = DocumentProcessorTool()

    processed_files = []
    processing_details = []

    for file in files:
        # Validate file type
        file_ext = os.path.splitext(file.filename)[1].lower()
        if file_ext not in ['.pdf', '.docx', '.txt']:
            processing_details.append(f"Skipped {file.filename}: Unsupported file type")
            continue

        try:
            # Create a temporary file to store the upload
            with tempfile.NamedTemporaryFile(delete=False, suffix=file_ext) as temp_file:
                # Read and write file content
                content = await file.read()
                temp_file.write(content)
                temp_file_path = temp_file.name

            # Process the document with original filename
            print(f"Processing file: {file.filename} (temp path: {temp_file_path})")
            result = doc_processor._run(file_path=temp_file_path, original_filename=file.filename)
            print(f"Result: {result}")

            # Check if processing was successful
            if "Error processing document" in result or "error" in result.lower():
                processing_details.append(f"❌ {file.filename}: {result}")
                print(f"ERROR: {file.filename} - {result}")
            else:
                processed_files.append(file.filename)
                processing_details.append(f"✅ {file.filename}: {result}")
                print(f"SUCCESS: {file.filename} - {result}")

        except Exception as e:
            error_msg = f"Error processing {file.filename}: {str(e)}"
            processing_details.append(f"❌ {error_msg}")
            print(f"EXCEPTION: {error_msg}")
            import traceback
            traceback.print_exc()
            # Clean up temp file if it exists
            try:
                if 'temp_file_path' in locals():
                    os.remove(temp_file_path)
            except:
                pass

    return UploadResponse(
        message=f"Processed {len(processed_files)} file(s)",
        files_processed=len(processed_files),
        details=processing_details
    )
