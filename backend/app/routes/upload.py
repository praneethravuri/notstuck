from fastapi import APIRouter, HTTPException, UploadFile, File, Form
from app.services.upload_services import save_files, process_and_upsert
from app.config import PINECONE_NAMESPACE
import logging

router = APIRouter()
logger = logging.getLogger(__name__)

# Configuration
MAX_FILE_SIZE = 50 * 1024 * 1024  # 50MB
MAX_FILES = 20
ALLOWED_EXTENSIONS = {".pdf"}

@router.post("/upload")
async def upload_files(
    files: list[UploadFile] = File(...),
    subjects: str = Form(None)
):
    """
    Upload and process PDF files for RAG system.

    Args:
        files: List of PDF files to upload
        subjects: Optional subjects/tags for the files

    Returns:
        Upload status and processed file names

    Raises:
        HTTPException: On validation or processing errors
    """
    try:
        # Validation
        if not files:
            raise HTTPException(status_code=400, detail="No files provided")

        if len(files) > MAX_FILES:
            raise HTTPException(
                status_code=400,
                detail=f"Too many files. Maximum {MAX_FILES} files allowed per upload."
            )

        # Validate each file
        for file in files:
            # Check filename
            if not file.filename:
                raise HTTPException(status_code=400, detail="File must have a filename")

            # Check extension
            file_ext = file.filename[file.filename.rfind("."):].lower() if "." in file.filename else ""
            if file_ext not in ALLOWED_EXTENSIONS:
                raise HTTPException(
                    status_code=400,
                    detail=f"File '{file.filename}' has invalid extension. Only PDF files are allowed."
                )

            # Check file size (if available)
            if hasattr(file, 'size') and file.size and file.size > MAX_FILE_SIZE:
                raise HTTPException(
                    status_code=400,
                    detail=f"File '{file.filename}' exceeds maximum size of {MAX_FILE_SIZE // (1024*1024)}MB"
                )

        logger.info(f"Received upload request for {len(files)} valid file(s)")

        # Save files to disk
        file_paths = save_files(files)
        logger.info(f"Files saved to disk: {file_paths}")

        # Process PDFs and upsert to Pinecone
        try:
            process_and_upsert(file_paths, namespace=PINECONE_NAMESPACE)
            logger.info("Files processed and upserted to Pinecone successfully")
            return {
                "message": "Files uploaded and processed successfully",
                "files": [f.filename for f in files],
                "count": len(files)
            }
        except Exception as process_error:
            logger.error(f"Error during processing and upsert: {process_error}", exc_info=True)
            raise HTTPException(
                status_code=500,
                detail=f"Files uploaded but processing failed: {str(process_error)}"
            )

    except HTTPException:
        raise
    except Exception as upload_error:
        logger.error(f"Upload failed: {upload_error}", exc_info=True)
        raise HTTPException(
            status_code=500,
            detail=f"Upload failed: {str(upload_error)}"
        )
