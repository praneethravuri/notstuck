"""
FastAPI application for NotStuck RAG chatbot.
"""

import os
import sys
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv

# Fix Windows console encoding for emoji support (CrewAI logs)
if sys.platform == "win32":
    # Set console to UTF-8 mode on Windows
    if hasattr(sys.stdout, 'reconfigure'):
        sys.stdout.reconfigure(encoding='utf-8')
    if hasattr(sys.stderr, 'reconfigure'):
        sys.stderr.reconfigure(encoding='utf-8')
    # Also set environment variable for subprocess/child processes
    os.environ['PYTHONIOENCODING'] = 'utf-8'

# Load environment variables
load_dotenv()

# Import routers
from backend.api.routes import upload, ask, models

# Create FastAPI app
app = FastAPI(
    title="NotStuck API",
    description="RAG-powered chatbot API using CrewAI, Pinecone, and OpenAI",
    version="1.0.0"
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, replace with specific origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(upload.router, prefix="/api", tags=["upload"])
app.include_router(ask.router, prefix="/api", tags=["ask"])
app.include_router(models.router, prefix="/api", tags=["models"])


@app.on_event("startup")
async def startup_event():
    """Reset Pinecone database on startup."""
    print("🔄 Resetting Pinecone database on startup...")
    try:
        from backend.clients.pinecone_client import get_pinecone_client

        pinecone_client = get_pinecone_client()
        index = pinecone_client.get_index()

        # Delete all vectors in the index
        index.delete(delete_all=True)

        print("✅ Pinecone database reset complete")
    except Exception as e:
        print(f"⚠️ Warning: Could not reset Pinecone database: {e}")


@app.get("/")
async def root():
    """Root endpoint."""
    return {
        "message": "NotStuck API",
        "status": "running",
        "version": "1.0.0"
    }


@app.get("/health")
async def health_check():
    """Health check endpoint."""
    return {"status": "healthy"}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
