import logging
import uuid
import os
import shutil
from typing import Optional, List
from pinecone import Pinecone, ServerlessSpec

from ..config import (
    PINECONE_API_KEY,
    PINECONE_ENV,
    PINECONE_INDEX_NAME,
    PINECONE_EMBEDDING_DIMENSIONS,
    SIMILARITY_THRESHOLD,
    EXACT_MATCH_THRESHOLD,
    RAW_DATA_PATH,
    PROCESSED_DATA_PATH,
)
from langchain.docstore.document import Document
from app.utils.embedding_provider import OpenAIEmbeddingProvider
from app.utils.document_loader import DocumentLoader

logger = logging.getLogger(__name__)


class PineconeDB:
    def __init__(
        self,
        api_key: Optional[str] = None,
        environment: Optional[str] = None,
        index_name: Optional[str] = None,
        embedding_dimensions: Optional[int] = None,
    ):
        """
        Initializes the PineconeDB instance by setting up the Pinecone API
        and ensuring the specified index exists.
        """
        self.api_key = api_key or PINECONE_API_KEY
        self.environment = environment or PINECONE_ENV
        self.index_name = index_name or PINECONE_INDEX_NAME
        self.embedding_dimensions = embedding_dimensions or PINECONE_EMBEDDING_DIMENSIONS
        
        # Initialize the embedding provider.
        embedding_provider = OpenAIEmbeddingProvider()
        self.embedding_function = embedding_provider.get_embedding_function()

        if not self.api_key or not self.environment:
            raise ValueError("Missing Pinecone credentials. Check config or environment variables.")

        # Initialize the Pinecone client.
        self.pc = Pinecone(api_key=self.api_key)
        self.index = self._init_index()

    def _init_index(self):
        """
        Ensures that the Pinecone index exists. If it does not, it will be created.
        """
        existing_indexes = [idx.name for idx in self.pc.list_indexes()]
        if self.index_name not in existing_indexes:
            self.pc.create_index(
                name=self.index_name,
                dimension=self.embedding_dimensions,
                metric="cosine",
                spec=ServerlessSpec(
                    region=self.environment,
                    cloud="aws"
                )
            )
            logger.info(f"Created new Pinecone index: {self.index_name}")
        else:
            logger.info(f"Using existing Pinecone index: {self.index_name}")

        return self.pc.Index(self.index_name)

    def delete_all_data(self, namespace: Optional[str] = None) -> None:
        """
        Deletes all data from the specified namespace in the Pinecone index.
        If no namespace is provided, deletes data from the default namespace.
        """
        self.index.delete(delete_all=True, namespace=namespace)
        logger.info(f"Deleted all data{' in namespace ' + namespace if namespace else ''}.")

    async def upsert_documents_with_similarity_check(self, documents: List[Document], namespace: Optional[str] = None) -> None:
        """
        Upserts a list of Document objects into the Pinecone index with a similarity check.
        For each document, its embedding is generated and the index is queried to check for similar vectors.
        If a similar vector is found with a similarity score greater than or equal to SIMILARITY_THRESHOLD,
        the document is skipped to avoid duplicate entries.
        
        Args:
            documents (List[Document]): List of Document objects.
            namespace (Optional[str]): The namespace in the Pinecone index.
        """
        vectors_to_upsert = []
        for doc in documents:
            text = doc.page_content
            # Generate embedding for the document text.
            embedding = self.embedding_function.embed_query(text)
            
            # Query the Pinecone index for the most similar vector.
            query_result = self.index.query(
                vector=embedding,
                top_k=1,
                include_values=False,
                namespace=namespace
            )
            
            skip_document = False
            if query_result and query_result.matches:
                best_match = query_result.matches[0]
                similarity_score = best_match.get("score", 0)
                # If the similarity score exceeds the threshold, skip upserting this document.
                if similarity_score >= SIMILARITY_THRESHOLD:
                    logger.info(
                        f"Skipping upsert for document from {doc.metadata.get('source', 'unknown source')} "
                        f"due to similarity score {similarity_score} >= threshold {SIMILARITY_THRESHOLD}."
                    )
                    skip_document = True
            
            if not skip_document:
                vector_id = uuid.uuid4().hex
                vectors_to_upsert.append({
                    "id": vector_id,
                    "values": embedding,
                    "metadata": doc.metadata,
                })
        
        if vectors_to_upsert:
            self.index.upsert(vectors=vectors_to_upsert, namespace=namespace)
            logger.info(
                f"Upserted {len(vectors_to_upsert)} vectors into Pinecone index '{self.index_name}' in namespace '{namespace}' after similarity check."
            )
        else:
            logger.info("No new documents to upsert after similarity check.")


    def move_file_to_processed(file_name: str) -> None:
        """
        Moves a file from the raw directory to the processed directory.
        
        Args:
            file_name (str): The file name to move.
        """
        raw_file_path = os.path.join(RAW_DATA_PATH, file_name)
        processed_file_path = os.path.join(PROCESSED_DATA_PATH, file_name)
        os.makedirs(PROCESSED_DATA_PATH, exist_ok=True)
        try:
            shutil.move(raw_file_path, processed_file_path)
            logger.info(f"Moved file '{raw_file_path}' to '{processed_file_path}'.")
        except Exception as e:
            logger.error(f"Failed to move file '{raw_file_path}' to '{processed_file_path}': {e}")


# ======================
# Example Usage
# ======================
if __name__ == "__main__":
    import asyncio
    
    async def main():
        # List of PDF file names (assumed to be located in RAW_DATA_PATH).
        pdf_file_names = ["document1.pdf", "document2.pdf"]
        # Build full paths for document loader if needed,
        # or pass file names if your loader constructs full paths from RAW_DATA_PATH.
        pdf_file_paths = [os.path.join(RAW_DATA_PATH, file_name) for file_name in pdf_file_names]
        
        # Load and split PDF documents into chunks.
        documents = await DocumentLoader.load_pdf_documents(pdf_file_paths)
        
        # Initialize the PineconeDB instance.
        pinecone_db = PineconeDB()
        
        # Option: Upsert with similarity check to avoid duplicates.
        pinecone_db.upsert_documents_with_similarity_check(documents, namespace="my-namespace")
        
        # After successful upsert, move each file from raw to processed directory.
        for file_name in pdf_file_names:
            move_file_to_processed(file_name)
    
    asyncio.run(main())
