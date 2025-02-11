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
    modelName: str

@router.post("/ask")
def ask_question(payload: QuestionPayload):
    try:
        result = answer_question(
            question=payload.question,
            top_k=payload.similarResults,
            threshold=payload.similarityThreshold,
            temperature=payload.temperature,
            max_tokens=payload.maxTokens,
            response_style=payload.responseStyle,
            namespace="my-namespace",
            model_name=payload.modelName
        )
        
        print(result)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
