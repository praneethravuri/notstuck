import os
import re
import uuid
import unicodedata
from typing import List, Dict, Any
from pathlib import Path
from crewai.tools import BaseTool
from pydantic import BaseModel, Field
from pypdf import PdfReader
from docx import Document as DocxDocument

from backend.clients.openai_client import get_openai_client
from backend.clients.pinecone_client import get_pinecone_client


class DocumentProcessorInput(BaseModel):
    """Input schema for DocumentProcessor."""
    file_path: str = Field(..., description="Path to the document file to process")
    original_filename: str = Field(default=None, description="Original filename to preserve in metadata")
    chunk_size: int = Field(default=1000, description="Size of text chunks in characters")
    chunk_overlap: int = Field(default=200, description="Overlap between chunks in characters")


class DocumentProcessorTool(BaseTool):
    """Tool for processing documents: chunking, embedding, and upserting to Pinecone."""

    name: str = "Document Processor"
    description: str = (
        "Processes documents (PDF, DOCX, TXT) by extracting text, chunking it, "
        "generating embeddings, and upserting to Pinecone vector database. "
        "Returns the number of chunks processed and automatically deletes the file after processing."
    )
    args_schema: type[BaseModel] = DocumentProcessorInput

    def _run(self, file_path: str, original_filename: str = None, chunk_size: int = 1000, chunk_overlap: int = 200) -> str:
        """
        Process a document file.

        Args:
            file_path: Path to the document file
            original_filename: Original filename to preserve
            chunk_size: Size of text chunks in characters
            chunk_overlap: Overlap between chunks

        Returns:
            Status message with number of chunks processed
        """
        try:
            # Extract text from file
            text = self._extract_text(file_path)
            filename = original_filename or Path(file_path).name

            # Clean text
            text = self._clean_text(text)

            # Chunk text
            chunks = self._chunk_text(text, chunk_size, chunk_overlap)

            # Generate embeddings and upsert to Pinecone
            num_chunks = self._upsert_to_pinecone(chunks, filename)

            # Delete the file
            try:
                os.remove(file_path)
            except Exception as e:
                print(f"Warning: Could not delete file {file_path}: {e}")

            return f"Successfully processed {num_chunks} chunks from {filename}"

        except Exception as e:
            return f"Error processing document: {str(e)}"

    def _extract_text(self, file_path: str) -> str:
        """Extract text from PDF, DOCX, or TXT file."""
        file_ext = Path(file_path).suffix.lower()

        if file_ext == '.pdf':
            return self._extract_from_pdf(file_path)
        elif file_ext == '.docx':
            return self._extract_from_docx(file_path)
        elif file_ext == '.txt':
            return self._extract_from_txt(file_path)
        else:
            raise ValueError(f"Unsupported file type: {file_ext}")

    def _extract_from_pdf(self, file_path: str) -> str:
        """Extract text from PDF file."""
        reader = PdfReader(file_path)
        text = ""
        for page in reader.pages:
            text += page.extract_text() + "\n"
        return text

    def _extract_from_docx(self, file_path: str) -> str:
        """Extract text from DOCX file."""
        doc = DocxDocument(file_path)
        text = ""
        for paragraph in doc.paragraphs:
            text += paragraph.text + "\n"
        return text

    def _extract_from_txt(self, file_path: str) -> str:
        """Extract text from TXT file."""
        with open(file_path, 'r', encoding='utf-8') as f:
            return f.read()

    def _clean_text(self, text: str) -> str:
        """
        Clean text by removing unwanted unicode characters, escape sequences, etc.

        Args:
            text: Raw text to clean

        Returns:
            Cleaned text
        """
        # Normalize unicode characters
        text = unicodedata.normalize('NFKD', text)

        # Remove common escape sequences
        text = text.replace('\\n', '\n').replace('\\r', '\r').replace('\\t', '\t')

        # Remove control characters except newlines, tabs, and carriage returns
        text = ''.join(char for char in text if unicodedata.category(char)[0] != 'C' or char in '\n\r\t')

        # Remove excessive whitespace while preserving paragraph structure
        text = re.sub(r'[ \t]+', ' ', text)  # Multiple spaces/tabs to single space
        text = re.sub(r'\n\s*\n\s*\n+', '\n\n', text)  # Multiple newlines to double newline

        # Remove common PDF artifacts
        text = re.sub(r'[\x00-\x08\x0b\x0c\x0e-\x1f\x7f-\x9f]', '', text)

        # Strip leading/trailing whitespace
        text = text.strip()

        return text

    def _chunk_text(self, text: str, chunk_size: int, chunk_overlap: int) -> List[str]:
        """
        Split text into overlapping chunks.

        Args:
            text: Text to chunk
            chunk_size: Size of each chunk in characters
            chunk_overlap: Overlap between chunks

        Returns:
            List of text chunks
        """
        chunks = []
        start = 0

        while start < len(text):
            end = start + chunk_size
            chunk = text[start:end]

            # Only add non-empty chunks
            if chunk.strip():
                chunks.append(chunk)

            start = end - chunk_overlap

        return chunks

    def _upsert_to_pinecone(self, chunks: List[str], filename: str) -> int:
        """
        Generate embeddings for chunks and upsert to Pinecone.

        Args:
            chunks: List of text chunks
            filename: Source filename for metadata

        Returns:
            Number of chunks processed
        """
        openai_client = get_openai_client()
        pinecone_client = get_pinecone_client()

        # Get or create index
        index = pinecone_client.get_or_create_index()

        # Process chunks in batches
        batch_size = 100
        for i in range(0, len(chunks), batch_size):
            batch_chunks = chunks[i:i + batch_size]

            # Generate embeddings
            embeddings = openai_client.create_embeddings(batch_chunks)

            # Prepare vectors for upsert
            vectors = []
            for j, (chunk, embedding) in enumerate(zip(batch_chunks, embeddings)):
                # Clean chunk one more time before storing
                cleaned_chunk = self._clean_text(chunk)
                vector_id = f"{filename}_{i+j}_{uuid.uuid4().hex[:8]}"
                vectors.append({
                    "id": vector_id,
                    "values": embedding,
                    "metadata": {
                        "text": cleaned_chunk,
                        "source_file": filename,
                        "chunk_index": i + j
                    }
                })

            # Upsert to Pinecone
            index.upsert(vectors=vectors)

        return len(chunks)
