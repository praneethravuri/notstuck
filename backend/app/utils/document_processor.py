# app/utils/document_chunker.py
import os
import concurrent.futures
from typing import Union, List, Dict
from langchain_community.document_loaders import PyPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from app.config import CHUNK_SIZE, CHUNK_OVERLAP
from app.utils.pdf_text_cleaner import clean_pdf_text
from app.utils.subjects_classifier import detect_subjects

splitter = RecursiveCharacterTextSplitter(
    chunk_size=CHUNK_SIZE,
    chunk_overlap=CHUNK_OVERLAP,
    length_function=len
)

def process_single_pdf(pdf_path: str) -> Dict:
    """
    Process a single PDF and return structured data with chunks and metadata
    """
    try:
        # Load PDF
        loader = PyPDFLoader(pdf_path)
        pages = loader.load()
        
        # Get PDF name
        pdf_name = os.path.basename(pdf_path)
        
        # Get sample text for subject detection
        sample_text = "\n".join([
            pages[i].page_content[:1000] 
            for i in [0, len(pages)//2, -1] 
            if i < len(pages)
        ])
        
        # Detect subjects
        detected_subjects = detect_subjects(sample_text)
        tags = detected_subjects if isinstance(detected_subjects, list) else [detected_subjects]
        
        # Process chunks
        chunks = []
        for page_doc in pages:
            page_chunks = splitter.split_documents([page_doc])
            page_num = page_doc.metadata.get("page")
            
            for chunk in page_chunks:
                cleaned_text = clean_pdf_text(chunk.page_content)
                if cleaned_text.strip():  # Only add non-empty chunks
                    chunks.append({
                        "chunk_data": cleaned_text,
                        "page_num": page_num
                    })
        
        return {
            "pdf_name": pdf_name,
            "tags": tags,
            "chunks": chunks
        }
        
    except Exception as exc:
        print(f"Error processing PDF '{pdf_path}': {exc}")
        return None

def process_pdf_files(pdf_paths: List[str]) -> List[Dict]:
    """
    Process multiple PDF files concurrently and return structured data
    """
    processed_documents = []
    
    with concurrent.futures.ThreadPoolExecutor(max_workers=min(8, len(pdf_paths))) as executor:
        future_to_pdf = {
            executor.submit(process_single_pdf, pdf_path): pdf_path
            for pdf_path in pdf_paths
        }
        
        for future in concurrent.futures.as_completed(future_to_pdf):
            pdf_path = future_to_pdf[future]
            try:
                result = future.result()
                if result:
                    processed_documents.append(result)
            except Exception as e:
                print(f"Error processing {pdf_path}: {e}")
    
    return processed_documents