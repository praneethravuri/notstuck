from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import os
from app.vector_search_db.pinecone_db import PineconeDB

# Import the routers
from app.routes import ask, pdfs, upload, reset_db, chats

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
    # Initialize the Pinecone DB once at startup and store it in the app state
    app.state.pinecone_db = PineconeDB()
    print("Pinecone DB initialized.")

# Include routers with a common prefix (e.g., /api)
app.include_router(ask.router, prefix="/api")
app.include_router(pdfs.router, prefix="/api")
app.include_router(upload.router, prefix="/api")
app.include_router(reset_db.router, prefix="/api")
app.include_router(chats.router, prefix="/api")
