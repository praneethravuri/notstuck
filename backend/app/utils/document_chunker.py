import os
from langchain_community.document_loaders import PyPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.schema import Document
from app.config import CHUNK_SIZE, CHUNK_OVERLAP
import concurrent.futures
from typing import Union, List, Dict

# Create a single splitter instance to avoid re-instantiation overhead.
splitter = RecursiveCharacterTextSplitter(
    chunk_size=CHUNK_SIZE,
    chunk_overlap=CHUNK_OVERLAP,
    length_function=len
)


def _load_and_split_single_pdf(pdf_path: str) -> List[Document]:
    """
    Loads and splits a single PDF into Document chunks.
    """
    try:
        loader = PyPDFLoader(pdf_path)
        pages = loader.load()
    except Exception as exc:
        print(f"Error loading PDF '{pdf_path}': {exc}")
        return []
    return splitter.split_documents(pages)


def load_and_split_pdf(pdf_input: Union[str, List[str]]) -> Union[List[Document], Dict[str, List[Document]]]:
    """
    Main function to load and split PDF(s) into Document chunks.

    If pdf_input is a string (a single PDF path), it returns a list of Document objects.
    If pdf_input is a list of PDF paths, it processes them concurrently and returns a 
    dictionary mapping each PDF path to its list of Document objects.
    """
    if isinstance(pdf_input, str):
        # Process a single PDF.
        return _load_and_split_single_pdf(pdf_input)
    elif isinstance(pdf_input, list):
        # Process multiple PDFs concurrently.
        results: Dict[str, List[Document]] = {}
        # Use a thread pool; adjust max_workers as needed.
        with concurrent.futures.ThreadPoolExecutor(max_workers=min(8, len(pdf_input))) as executor:
            future_to_pdf = {
                executor.submit(_load_and_split_single_pdf, pdf_path): pdf_path
                for pdf_path in pdf_input
            }
            for future in concurrent.futures.as_completed(future_to_pdf):
                pdf_path = future_to_pdf[future]
                try:
                    documents = future.result()
                    results[pdf_path] = documents
                except Exception as e:
                    print(f"Error processing {pdf_path}: {e}")
                    results[pdf_path] = []
        return results
    else:
        raise ValueError("pdf_input must be a string or a list of strings.")
