from fastapi import APIRouter, HTTPException, UploadFile, File, Form
from app.services.upload_services import process_and_upsert_direct
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
    Files are processed directly without saving to disk permanently.

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

        # Process PDFs directly and upsert to Pinecone (no disk saving)
        count = process_and_upsert_direct(files, namespace=PINECONE_NAMESPACE)

        logger.info(f"Successfully processed {count} file(s)")
        return {
            "message": "Files uploaded and processed successfully",
            "files": [f.filename for f in files],
            "count": count
        }

    except HTTPException:
        raise
    except Exception as upload_error:
        logger.error(f"Upload failed: {upload_error}", exc_info=True)
        raise HTTPException(
            status_code=500,
            detail=f"Upload failed: {str(upload_error)}"
        )
