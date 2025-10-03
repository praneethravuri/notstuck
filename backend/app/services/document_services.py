import os
import concurrent.futures
import logging
from typing import List, Dict
from langchain_community.document_loaders import PyPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from app.config import CHUNK_SIZE, CHUNK_OVERLAP, CHUNK_MIN_SIZE
from app.utils.pdf_text_cleaner import clean_pdf_text
from app.helpers.subjects_classifier import detect_subjects

logger = logging.getLogger(__name__)

# Optimized splitter with better separators for semantic coherence
splitter = RecursiveCharacterTextSplitter(
    chunk_size=CHUNK_SIZE,
    chunk_overlap=CHUNK_OVERLAP,
    length_function=len,
    separators=[
        "\n\n\n",  # Major section breaks
        "\n\n",    # Paragraph breaks
        "\n",      # Line breaks
        ". ",      # Sentence breaks
        "! ",
        "? ",
        "; ",
        ", ",
        " ",
        ""
    ],
    keep_separator=True,  # Preserve context
    strip_whitespace=True
)

def process_single_pdf(pdf_path: str) -> Dict:
    """
    Process a single PDF and return structured data with chunks and metadata.
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
                # Only add non-empty chunks that meet minimum size
                if cleaned_text.strip() and len(cleaned_text.strip()) >= CHUNK_MIN_SIZE:
                    chunks.append({
                        "chunk_data": cleaned_text,
                        "page_num": page_num
                    })
        
        logger.info("Processed PDF '%s' successfully.", pdf_name)
        return {
            "pdf_name": pdf_name,
            "tags": tags,
            "chunks": chunks
        }
        
    except Exception as exc:
        logger.error("Error processing PDF '%s': %s", pdf_path, exc, exc_info=True)
        return None

def process_pdf_files(pdf_paths: List[str]) -> List[Dict]:
    """
    Process multiple PDF files concurrently and return structured data.
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
                logger.error("Error processing %s: %s", pdf_path, e, exc_info=True)
    
    logger.info("Processed %d PDF file(s).", len(processed_documents))
    return processed_documents
