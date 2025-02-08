from langchain_community.document_loaders import PyPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.schema import Document

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
        chunk_size=1000,
        chunk_overlap=150,
        length_function=len
    )
    documents = splitter.split_documents(pages)
    return documents
