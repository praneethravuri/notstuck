from typing import List
from langchain.docstore.document import Document
import pymupdf4llm
from langchain.text_splitter import RecursiveCharacterTextSplitter

class DocumentLoader:
    @staticmethod
    async def load_pdf_documents(file_paths: List[str], chunk_size: int = 1500, chunk_overlap: int = 300) -> List[Document]:
        """
        Loads PDF documents and splits them into chunks.
        
        Args:
            file_paths (List[str]): List of file paths to PDF documents.
            chunk_size (int): Maximum size of each text chunk.
            chunk_overlap (int): Number of overlapping characters between chunks.
        
        Returns:
            List[Document]: A list of Document objects containing text chunks and metadata.
        """
        for f in file_paths:
            print(f"Received file: {f}")
            
            
        text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=chunk_size,
            chunk_overlap=chunk_overlap
        )
        
        documents = []
        for file_path in file_paths:
            # Convert the PDF file to markdown text.
            pdf_text = pymupdf4llm.to_markdown(file_path)
            
            # Split the text into chunks.
            texts = text_splitter.split_text(pdf_text)
            
            # Wrap each chunk in a Document with metadata.
            docs = [
                Document(
                    page_content=text,
                    metadata={"source": file_path}
                )
                for text in texts
            ]
            documents.extend(docs)
            print(f"Finished chunking {file_path}")
        
        return documents
