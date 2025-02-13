from app.vector_search_db.pinecone_db import PineconeDB
from pinecone import Pinecone, ServerlessSpec
from fastapi import APIRouter, HTTPException

router = APIRouter()
pinecone_db = PineconeDB()

@router.delete("/reset-db")
def reset_db():
    print("Reset DB route accessed")  # Debug print
    try:
        pinecone_db.delete_all_data(namespace="my-namespace")
        return "Database reset successful."
    except Exception as e:
        print("Error in reset_db:", e)
        raise HTTPException(status_code=500, detail=str(e))

