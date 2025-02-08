# uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload

from typing import Optional
import os
from fastapi import FastAPI, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from pydantic import BaseModel

from .services.rag.main import answer_question

app = FastAPI()

PROCESSED_DIR = os.path.join(
    os.path.dirname(__file__),
    "",
    "data",
    "processed"
)
PROCESSED_DIR = os.path.abspath(PROCESSED_DIR)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class QuestionPayload(BaseModel):
    question: str

@app.post("/api/ask")
def ask_question(payload: QuestionPayload):
    question_text = payload.question
    answer = answer_question(question=question_text, top_k=5, threshold=0.9, namespace="my-namespace")
    return {"answer": answer}

@app.get("/api/get-pdfs")
def pdf_endpoint(filename: Optional[str] = Query(None)):
    """
    If 'filename' is not provided => Return JSON list of PDFs.
    If 'filename' is provided => Return the PDF file as FileResponse.
    """
    # 1. If no filename is provided, list PDFs
    if filename is None:
        if not os.path.isdir(PROCESSED_DIR):
            return {"files": []}

        files = []
        for f in os.listdir(PROCESSED_DIR):
            if f.lower().endswith(".pdf"):
                files.append(f)
        return {"files": files}

    # 2. If a filename is provided, serve that PDF
    pdf_path = os.path.join(PROCESSED_DIR, filename)
    if not os.path.isfile(pdf_path) or not filename.lower().endswith(".pdf"):
        raise HTTPException(status_code=404, detail="PDF not found")

    return FileResponse(pdf_path, media_type="application/pdf")
