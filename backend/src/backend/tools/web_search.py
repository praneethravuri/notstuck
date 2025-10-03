"""
Web Search Tool for CrewAI using DuckDuckGo search.

This tool provides web search capabilities without requiring an API key.
DuckDuckGo is used as it's free and doesn't require authentication.
"""

from typing import Optional
from crewai.tools import BaseTool
from pydantic import BaseModel, Field
import requests


class WebSearchInput(BaseModel):
    """Input schema for WebSearch."""
    query: str = Field(..., description="Search query to search the web")
    max_results: int = Field(default=5, description="Maximum number of results to return")


class WebSearchTool(BaseTool):
    """Tool for searching the web when no relevant context is found in the knowledge base."""

    name: str = "Web Search"
    description: str = (
        "Searches the web for information when no relevant context is found "
        "in the knowledge base. Returns web search results that can be used "
        "to answer questions. Use this as a fallback when Pinecone Search returns no results."
    )
    args_schema: type[BaseModel] = WebSearchInput

    def _run(self, query: str, max_results: int = 5) -> str:
        """
        Search the web using DuckDuckGo.

        Args:
            query: Search query
            max_results: Maximum number of results to return

        Returns:
            Formatted string with search results
        """
        try:
            # Use DuckDuckGo HTML API (no API key required)
            url = "https://html.duckduckgo.com/html/"
            params = {"q": query}
            headers = {
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
            }

            response = requests.post(url, data=params, headers=headers, timeout=10)

            if response.status_code == 200:
                # Simple parsing of DuckDuckGo results
                # Note: This is a basic implementation. For production, consider using
                # a proper HTML parser like BeautifulSoup or a dedicated search API
                results_text = []
                content = response.text

                # Basic extraction of result snippets
                # This is a simplified version - in production you'd want to use BeautifulSoup
                snippets = content.split('result__snippet')
                for i, snippet in enumerate(snippets[1:max_results+1], 1):
                    # Extract text between > and <
                    try:
                        text_start = snippet.find('>') + 1
                        text_end = snippet.find('</a>', text_start)
                        if text_start > 0 and text_end > 0:
                            result_text = snippet[text_start:text_end].strip()
                            if result_text:
                                results_text.append(f"[Result {i}] {result_text}")
                    except:
                        continue

                if results_text:
                    return "\n\n".join(results_text)
                else:
                    return f"Web search completed for '{query}' but no clear results were extracted. " \
                           f"Consider rephrasing the question or noting that current information may be limited."
            else:
                return f"Web search failed with status code: {response.status_code}"

        except Exception as e:
            return f"Error performing web search: {str(e)}. Unable to retrieve web information at this time."


# Alternative: If you have a Serper API key, you can use this implementation instead
class SerperWebSearchTool(BaseTool):
    """
    Alternative web search tool using Serper API.
    Requires SERPER_API_KEY environment variable to be set.
    """

    name: str = "Serper Web Search"
    description: str = (
        "Searches the web using Serper API when no relevant context is found "
        "in the knowledge base. Requires SERPER_API_KEY to be set."
    )
    args_schema: type[BaseModel] = WebSearchInput

    def _run(self, query: str, max_results: int = 5) -> str:
        """Search the web using Serper API."""
        import os

        api_key = os.getenv("SERPER_API_KEY")
        if not api_key:
            return "Serper API key not configured. Unable to perform web search."

        try:
            url = "https://google.serper.dev/search"
            headers = {
                "X-API-KEY": api_key,
                "Content-Type": "application/json"
            }
            payload = {
                "q": query,
                "num": max_results
            }

            response = requests.post(url, json=payload, headers=headers, timeout=10)

            if response.status_code == 200:
                data = response.json()
                results = data.get("organic", [])

                formatted_results = []
                for i, result in enumerate(results[:max_results], 1):
                    title = result.get("title", "")
                    snippet = result.get("snippet", "")
                    formatted_results.append(f"[Result {i}] {title}\n{snippet}")

                if formatted_results:
                    return "\n\n".join(formatted_results)
                else:
                    return "No results found for the query."
            else:
                return f"Serper API request failed: {response.status_code}"

        except Exception as e:
            return f"Error using Serper API: {str(e)}"
