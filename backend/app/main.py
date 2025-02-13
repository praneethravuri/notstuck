# app/main.py
# uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload 
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import logging
import os

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

# @app.on_event("startup")
# async def startup_event():
#     host = os.getenv("HOST", "0.0.0.0")
#     port = os.getenv("PORT", "8000")
#     complete_url = f"http://{host}:{port}"
#     logger.info(f"Backend running at {complete_url}")

# Include routers with a common prefix (e.g., /api)
app.include_router(ask.router, prefix="/api")
app.include_router(pdfs.router, prefix="/api")
app.include_router(upload.router, prefix="/api")
app.include_router(reset_db.router, prefix="/api")
app.include_router(chats.router, prefix="/api")

logger.info("Application startup complete.")