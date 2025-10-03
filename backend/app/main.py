"""
NotStuck Backend API

FastAPI application for RAG (Retrieval-Augmented Generation) system
that supports multiple LLM providers via OpenRouter.

To run:
    uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
"""
import logging
from fastapi import FastAPI
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from app.clients.openai_client import openai_client
from app.clients.pinecone_client import pinecone_index
from app.routes import ask, pdfs, upload, reset_pinecone_db
from app.config import OPENROUTER_API_KEY, OPENROUTER_BASE_URL
import app.logging_config

logger = logging.getLogger(__name__)
IS_READY = False

# Initialize FastAPI app
app = FastAPI(
    title="NotStuck RAG API",
    description="Retrieval-Augmented Generation API with multi-model support via OpenRouter",
    version="1.0.0"
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Configure based on your deployment needs
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.on_event("startup")
async def startup_event():
    """
    Application startup event handler.
    Validates all required services are initialized properly.
    """
    global IS_READY

    # Validate Pinecone
    try:
        if pinecone_index:
            logger.info("✓ Pinecone index initialized successfully")
        else:
            logger.error("✗ Pinecone index not initialized")
    except Exception as e:
        logger.error("✗ Pinecone initialization error: %s", e, exc_info=True)

    # Validate LLM Client (OpenRouter/OpenAI)
    try:
        if openai_client and OPENROUTER_API_KEY:
            logger.info(f"✓ LLM client initialized successfully")
            logger.info(f"  Base URL: {OPENROUTER_BASE_URL}")
        else:
            logger.error("✗ LLM client not configured properly")
    except Exception as e:
        logger.error("✗ LLM client initialization error: %s", e, exc_info=True)

    IS_READY = True
    logger.info("=" * 50)
    logger.info("Application startup complete!")
    logger.info("=" * 50)

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
