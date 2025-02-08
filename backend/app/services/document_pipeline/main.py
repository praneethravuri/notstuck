# backend/app/services/document_pipeline/main.py

import os

# Import paths from your config
from backend.config import PROCESSED_DATA_PATH

# Import the functions from your pipeline modules
from .document_converter import convert_all_docs_in_raw_folder
from .document_chunker import load_and_split_pdf

def document_pipeline():
    """
    1. Convert all non-PDF files in RAW_DATA_PATH to PDF 
       and move them to PROCESSED_DATA_PATH.
    2. Then load and chunk each PDF in PROCESSED_DATA_PATH.
    """
    # Step 1: Convert documents & move them to 'processed'
    convert_all_docs_in_raw_folder()

    # Step 2: For each PDF now in 'processed', load and split into chunks
    for filename in os.listdir(PROCESSED_DATA_PATH):
        if filename.lower().endswith(".pdf"):
            pdf_path = os.path.join(PROCESSED_DATA_PATH, filename)
            docs = load_and_split_pdf(pdf_path)
            print(f"Chunked '{filename}' into {len(docs)} LangChain Document objects.")