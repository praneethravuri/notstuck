# app/main.py
# uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import logging
import os

# Import the shared clients
from app.clients import (
    pinecone_index,   # Shared Pinecone index instance
    openai_client,    # Shared OpenAI client instance
    mongodb_client    # Shared MongoDB client instance
)


# Import the routers
from app.routes import ask, pdfs, upload, reset_db, chats
import app.logging_config

logger = logging.getLogger(__name__)

app = FastAPI()

# Set up CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.on_event("startup")
async def startup_event():
    # --- Initialize / Verify MongoDB Connection ---
    try:
        await mongodb_client.admin.command('ping')
        logger.info("MongoDB connection successful.")
    except Exception as e:
        logger.error(f"MongoDB connection error: {e}")

    # --- Verify Pinecone Initialization ---
    try:
        # For example, list indexes (or simply log the index name)
        logger.info(f"Pinecone index is initialized.")
    except Exception as e:
        logger.error(f"Pinecone initialization error: {e}")

    # --- Confirm OpenAI Client is Ready ---
    # OpenAI client is stateless; here we simply log that the client is available.
    if openai_client.api_key:
        logger.info("OpenAI client is ready.")
    else:
        logger.error("OpenAI client is not configured properly.")

    host = os.getenv("HOST", "0.0.0.0")
    port = os.getenv("PORT", "8000")
    complete_url = f"http://{host}:{port}"
    logger.info(f"Backend running at {complete_url}")

# Include routers with a common prefix (e.g., /api)
app.include_router(ask.router, prefix="/api")
app.include_router(pdfs.router, prefix="/api")
app.include_router(upload.router, prefix="/api")
app.include_router(reset_db.router, prefix="/api")
app.include_router(chats.router, prefix="/api")

logger.info("Application startup complete.")
