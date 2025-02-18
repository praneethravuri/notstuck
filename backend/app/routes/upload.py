from fastapi import APIRouter, HTTPException, UploadFile, File, Form
from app.services.upload_services import save_files, process_and_upsert
import logging

router = APIRouter()
logger = logging.getLogger(__name__)

@router.post("/upload")
async def upload_files(
    files: list[UploadFile] = File(...),
    subjects: str = Form(None)
):
    try:
        logger.info("Received upload request for %d files.", len(files))
        
        # Save files to disk
        file_paths = save_files(files)
        logger.info("Files saved to disk: %s", file_paths)
        
        # Process PDFs and upsert to Pinecone
        try:
            process_and_upsert(file_paths, namespace="my-namespace")
            logger.info("Files processed and upserted to Pinecone successfully.")
            return {
                "message": "Files uploaded and processed successfully",
                "files": [f.filename for f in files]
            }
        except Exception as process_error:
            logger.error("Error during processing and upsert: %s", process_error, exc_info=True)
            return {
                "message": "Files uploaded but processing failed",
                "error": str(process_error),
                "files": [f.filename for f in files]
            }

    except Exception as upload_error:
        logger.error("Upload failed: %s", upload_error, exc_info=True)
        raise HTTPException(
            status_code=500,
            detail=f"Upload failed: {str(upload_error)}"
        )
