# app/main.py
# cd backend/.venv/Scripts && activate && cd .. && cd .. && uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload

import logging
import os
from fastapi import FastAPI
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from app.clients.openai_client import openai_client
from app.clients.pinecone_client import pinecone_index
from app.clients.mongodb_client import mongodb_client
from app.routes import ask, pdfs, upload, reset_pinecone_db, chats, reset_mongodb
import app.logging_config

logger = logging.getLogger(__name__)
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

    # Validate MongoDB connection
    try:
        await mongodb_client.admin.command("ping")
        logger.info("MongoDB connection successful.")
    except Exception as e:
        logger.error("MongoDB connection error: %s", e, exc_info=True)
        # Optionally: raise Exception("MongoDB failed to connect.")

    # Validate Pinecone (if you have extra checks, you can add them here)
    try:
        # The fact that pinecone_index is imported and available means it has been initialized.
        logger.info("Pinecone index is initialized.")
    except Exception as e:
        logger.error("Pinecone initialization error: %s", e, exc_info=True)

    # Validate OpenAI
    if getattr(openai_client, "api_key", None):
        logger.info("OpenAI client is ready.")
    else:
        logger.error("OpenAI client is not configured properly.")

    IS_READY = True
    logger.info("Application startup complete.")

@app.get("/api/health-check")
def health_check():
    if IS_READY:
        logger.debug("Health-check passed: Application is ready.")
        return {"ready": True, "message": "Backend startup complete!"}
    else:
        logger.warning("Health-check: Application still starting up.")
        return JSONResponse(
            content={"ready": False, "message": "Still starting up..."},
            status_code=503,
        )

# Include your other routes
app.include_router(ask.router, prefix="/api")
app.include_router(pdfs.router, prefix="/api")
app.include_router(upload.router, prefix="/api")
app.include_router(reset_pinecone_db.router, prefix="/api")
app.include_router(chats.router, prefix="/api")
app.include_router(reset_mongodb.router, prefix="/api")
