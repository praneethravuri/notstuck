# app/utils/document_chunker.py

import os
import concurrent.futures
from typing import Union, List, Dict
from langchain_community.document_loaders import PyPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.schema import Document
from app.config import CHUNK_SIZE, CHUNK_OVERLAP
from app.utils.pdf_text_cleaner import clean_pdf_text

splitter = RecursiveCharacterTextSplitter(
    chunk_size=CHUNK_SIZE,
    chunk_overlap=CHUNK_OVERLAP,
    length_function=len
)

def _load_and_split_single_pdf(pdf_path: str) -> List[Document]:
    """
    Loads and splits a single PDF into Document chunks,
    attaching 'page_number' in metadata where possible.
    """
    try:
        loader = PyPDFLoader(pdf_path)
        pages = loader.load()  # Typically returns a list of Document objects (one per page).
    except Exception as exc:
        print(f"Error loading PDF '{pdf_path}': {exc}")
        return []

    # By default, PyPDFLoader sets doc.metadata["page"] to the 1-based page index.
    # But let's confirm or set it manually.
    all_docs = []
    for page_doc in pages:
        # The page_doc usually has `page_doc.metadata["page"] = <page_number>`.
        # Now let's split each page_doc using the splitter:
        chunks = splitter.split_documents([page_doc])

        for chunk in chunks:
            # If the loader provides a "page" key in the metadata, rename it or keep it as is.
            # We'll store it under something like "page_number".
            chunk_page_number = page_doc.metadata.get("page")
            if chunk_page_number is not None:
                chunk.metadata["page_number"] = chunk_page_number

            # Clean the text
            if hasattr(chunk, "page_content") and chunk.page_content:
                chunk.page_content = clean_pdf_text(chunk.page_content)

            all_docs.append(chunk)

    return all_docs

def load_and_split_pdf(pdf_input: Union[str, List[str]]) -> Union[List[Document], Dict[str, List[Document]]]:
    """
    Main function to load and split PDF(s) into Document chunks, with page metadata attached.
    """
    if isinstance(pdf_input, str):
        return _load_and_split_single_pdf(pdf_input)
    elif isinstance(pdf_input, list):
        results: Dict[str, List[Document]] = {}
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
