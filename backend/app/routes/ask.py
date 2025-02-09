# app/routes/ask.py

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from app.services.rag.main import answer_question  # adjust the import path as needed

router = APIRouter()

class QuestionPayload(BaseModel):
    question: str
    similarityThreshold: float
    similarResults: int
    temperature: float
    maxTokens: int
    responseStyle: str

@router.post("/ask")
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
