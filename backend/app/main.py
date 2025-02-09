# uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload

from typing import Optional
import os
from fastapi import FastAPI, HTTPException, Query, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from pydantic import BaseModel
from .services.rag.main import answer_question
from .services.pinecone_db.main import process_and_push_all_pdfs

# Initialize FastAPI app
app = FastAPI()

# Define paths first
BASE_DIR = os.path.dirname(__file__)
DATA_DIR = os.path.join(BASE_DIR, "data")
PROCESSED_DIR = os.path.join(DATA_DIR, "processed")
RAW_DATA_PATH = os.path.join(DATA_DIR, "raw")

# Create necessary directories
os.makedirs(PROCESSED_DIR, exist_ok=True)
os.makedirs(RAW_DATA_PATH, exist_ok=True)

UPLOAD_DIR = os.path.join(os.path.dirname(__file__), "data", "raw")
os.makedirs(UPLOAD_DIR, exist_ok=True)

# Pydantic model
class QuestionPayload(BaseModel):
    question: str
    similarityThreshold: float
    similarResults: int
    temperature: float
    maxTokens: int
    responseStyle: str

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# File validation helpers
ALLOWED_EXTENSIONS = {'pdf', 'txt', 'doc', 'docx'}
MAX_FILE_SIZE = 10 * 1024 * 1024  # 10MB

def allowed_file(filename: str) -> bool:
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def validate_file_size(size: int) -> bool:
    return size <= MAX_FILE_SIZE

# API endpoints
@app.post("/api/ask")
def ask_question(payload: QuestionPayload):
    try:
        answer = answer_question(
            question=payload.question,
            top_k=payload.similarResults,
            threshold=payload.similarityThreshold,
            namespace="my-namespace"
        )
        return {"answer": answer}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/get-pdfs")
def pdf_endpoint(filename: Optional[str] = Query(None)):
    """
    If 'filename' is not provided => Return JSON list of PDFs.
    If 'filename' is provided => Return the PDF file as FileResponse.
    """
    try:
        # 1. If no filename is provided, list PDFs
        if filename is None:
            if not os.path.isdir(PROCESSED_DIR):
                return {"files": []}
            files = [f for f in os.listdir(PROCESSED_DIR) if f.lower().endswith(".pdf")]
            return {"files": files}

        # 2. If a filename is provided, serve that PDF
        pdf_path = os.path.join(PROCESSED_DIR, filename)
        if not os.path.isfile(pdf_path) or not filename.lower().endswith(".pdf"):
            raise HTTPException(status_code=404, detail="PDF not found")
        return FileResponse(pdf_path, media_type="application/pdf")
    except Exception as e:
        if isinstance(e, HTTPException):
            raise e
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/upload")
async def upload_files(files: list[UploadFile] = File(...)):
    try:
        # First save all files
        for file in files:
            file_path = os.path.join(UPLOAD_DIR, file.filename)
            content = await file.read()
            with open(file_path, "wb") as f:
                f.write(content)
        
        # After successful upload, process the PDFs
        try:
            print("Processing and pushing PDFs to Pinecone...")
            process_and_push_all_pdfs(namespace="my-namespace")
            return {
                "message": "Files uploaded and processed successfully",
                "files": [file.filename for file in files]
            }
        except Exception as process_error:
            # If processing fails, we still return a partial success
            return {
                "message": "Files uploaded but processing failed",
                "error": str(process_error),
                "files": [file.filename for file in files]
            }
            
    except Exception as upload_error:
        return {"error": f"Upload failed: {str(upload_error)}"}