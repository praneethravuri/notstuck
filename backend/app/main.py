# app/main.py
# uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
# cd backend/.venv/Scripts && activate && cd .. && cd .. && uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload

import logging
import os
from fastapi import FastAPI
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from app.clients import pinecone_index, openai_client, mongodb_client
from app.routes import ask, pdfs, upload, reset_db, chats
import app.logging_config

logger = logging.getLogger(__name__)

# A global readiness flag
IS_READY = False

app = FastAPI()

# Enable CORS if needed
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.on_event("startup")
async def startup_event():
    global IS_READY
    # Example: Check MongoDB
    try:
        await mongodb_client.admin.command("ping")
        logger.info("MongoDB connection successful.")
    except Exception as e:
        logger.error(f"MongoDB connection error: {e}")
        # If you want to fail startup, raise an exception

    # Example: Check Pinecone
    try:
        # Just log something to confirm initialization
        logger.info("Pinecone index is initialized.")
    except Exception as e:
        logger.error(f"Pinecone initialization error: {e}")

    # Example: Check OpenAI
    if openai_client.api_key:
        logger.info("OpenAI client is ready.")
    else:
        logger.error("OpenAI client is not configured properly.")

    # If everything succeeds, set readiness to True
    IS_READY = True
    logger.info("Application startup complete.")

# A simple readiness/health-check endpoint
@app.get("/api/health-check")
def health_check():
    if IS_READY:
        return {"ready": True, "message": "Backend startup complete!"}
    else:
        return JSONResponse(
            content={"ready": False, "message": "Still starting up..."},
            status_code=503,
        )

# Include your other routes
app.include_router(ask.router, prefix="/api")
app.include_router(pdfs.router, prefix="/api")
app.include_router(upload.router, prefix="/api")
app.include_router(reset_db.router, prefix="/api")
app.include_router(chats.router, prefix="/api")
