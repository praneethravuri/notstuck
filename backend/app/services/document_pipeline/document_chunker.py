import os
from langchain_community.document_loaders import PyPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.schema import Document
from .document_converter import convert_all_docs_in_raw_folder
from backend.config import CHUNK_SIZE, CHUNK_OVERLAP
from backend.config import PROCESSED_DATA_PATH

def load_and_split_pdf(pdf_path: str) -> list[Document]:
    """
    Uses LangChain's PyPDFLoader to read a PDF and then splits it into chunks
    using RecursiveCharacterTextSplitter.
    Returns a list of Document objects.
    """
    try:
        loader = PyPDFLoader(pdf_path)
        pages = loader.load()
    except Exception as exc:
        print(f"Error loading PDF '{pdf_path}': {exc}")
        return []

    splitter = RecursiveCharacterTextSplitter(
        chunk_size=CHUNK_SIZE,
        chunk_overlap=CHUNK_OVERLAP,
        length_function=len
    )
    documents = splitter.split_documents(pages)
    return documents