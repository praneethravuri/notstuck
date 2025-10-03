from typing import List, Dict, Any
from crewai.tools import BaseTool
from pydantic import BaseModel, Field

from backend.clients.openai_client import get_openai_client
from backend.clients.pinecone_client import get_pinecone_client


class PineconeSearchInput(BaseModel):
    """Input schema for PineconeSearch."""
    query: str = Field(..., description="Search query to find relevant documents")
    top_k: int = Field(default=5, description="Number of top results to return")


class PineconeSearchTool(BaseTool):
    """Tool for searching Pinecone vector database with hybrid search."""

    name: str = "Pinecone Search"
    description: str = (
        "Searches the Pinecone vector database for relevant document chunks "
        "using hybrid search (semantic similarity). Returns relevant text chunks "
        "with source file information. Use this tool to find context from uploaded documents "
        "before answering questions."
    )
    args_schema: type[BaseModel] = PineconeSearchInput

    def _run(self, query: str, top_k: int = 5) -> str:
        """
        Search Pinecone for relevant document chunks.

        Args:
            query: Search query
            top_k: Number of top results to return

        Returns:
            Formatted string with search results including text and source files
        """
        try:
            openai_client = get_openai_client()
            pinecone_client = get_pinecone_client()

            # Get index
            index = pinecone_client.get_index()

            # Generate query embedding
            query_embedding = openai_client.create_embedding(query)

            # Search Pinecone
            results = index.query(
                vector=query_embedding,
                top_k=top_k,
                include_metadata=True
            )

            # Check if we found any matches
            if not results.matches or len(results.matches) == 0:
                return "No relevant context found in the knowledge base."

            # Format results
            formatted_results = []
            sources = set()

            for i, match in enumerate(results.matches, 1):
                score = match.score
                metadata = match.metadata

                text = metadata.get('text', 'No text available')
                source_file = metadata.get('source_file', 'Unknown source')
                chunk_index = metadata.get('chunk_index', 0)

                sources.add(source_file)

                formatted_results.append(
                    f"[Result {i}] (Score: {score:.4f}, Source: {source_file}, Chunk: {chunk_index})\n"
                    f"{text}\n"
                )

            result_text = "\n".join(formatted_results)
            sources_text = "Sources: " + ", ".join(sorted(sources))

            return f"{result_text}\n{sources_text}"

        except Exception as e:
            return f"Error searching Pinecone: {str(e)}"

    def search_with_metadata(self, query: str, top_k: int = 5) -> Dict[str, Any]:
        """
        Search Pinecone and return structured results with metadata.
        This method is for use outside of CrewAI context (e.g., in FastAPI endpoints).

        Args:
            query: Search query
            top_k: Number of top results to return

        Returns:
            Dictionary with results and metadata
        """
        try:
            openai_client = get_openai_client()
            pinecone_client = get_pinecone_client()

            # Get index
            index = pinecone_client.get_index()

            # Generate query embedding
            query_embedding = openai_client.create_embedding(query)

            # Search Pinecone
            results = index.query(
                vector=query_embedding,
                top_k=top_k,
                include_metadata=True
            )

            # Check if we found any matches
            if not results.matches or len(results.matches) == 0:
                return {
                    "found_context": False,
                    "results": [],
                    "sources": []
                }

            # Format results
            formatted_results = []
            sources = []

            for match in results.matches:
                metadata = match.metadata
                formatted_results.append({
                    "text": metadata.get('text', ''),
                    "source_file": metadata.get('source_file', 'Unknown'),
                    "chunk_index": metadata.get('chunk_index', 0),
                    "score": match.score
                })

                # Track unique sources
                source_info = {
                    "source_file": metadata.get('source_file', 'Unknown'),
                }
                if source_info not in sources:
                    sources.append(source_info)

            return {
                "found_context": True,
                "results": formatted_results,
                "sources": sources
            }

        except Exception as e:
            return {
                "found_context": False,
                "results": [],
                "sources": [],
                "error": str(e)
            }
