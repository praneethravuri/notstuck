from fastapi import APIRouter, HTTPException
from app.vector_db.pinecone_db import delete_all_data  # delete_all_data now uses the shared pinecone_index

router = APIRouter()

@router.delete("/reset-db")
def reset_db():
    print("Reset DB route accessed")  # Debug print
    try:
        delete_all_data(namespace="my-namespace")
        return "Database reset successful."
    except Exception as e:
        print("Error in reset_db:", e)
        raise HTTPException(status_code=500, detail=str(e))
