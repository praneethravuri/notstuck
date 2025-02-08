# backend/app/main.py

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

from .services.rag.main import answer_question

app = FastAPI()

# If you're running frontend at http://localhost:3000
# or any other domain, add it to allowed origins:
origins = ["http://localhost:3000"]

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
    """
    Receives a JSON object with {"question": "..."}
    and returns the answer from answer_question().
    """
    print("Received question:", payload.question)
    question_text = payload.question
    answer = answer_question(
        question=question_text,
        top_k=5,
        threshold=0.9,
        namespace="my-namespace"
    )
    return {"answer": answer}
