import argparse
import os
import re
from langchain_chroma import Chroma  # Updated import for Chroma
from langchain_core.prompts import ChatPromptTemplate  # Updated import for ChatPromptTemplate
from langchain_openai import ChatOpenAI  # Updated import for OpenAI
from get_embedding_function import get_embedding_function
from dotenv import load_dotenv

load_dotenv()

# Define the path to the Chroma database
CHROMA_PATH = os.path.join(os.path.dirname(__file__), "..", "chroma")

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

# Template for the prompt
PROMPT_TEMPLATE = """
Answer the question based ONLY on the following context:

{context}

---

Answer the question based on the above context: {question}
"""

def main():
    # Create CLI.
    parser = argparse.ArgumentParser(description="Query the RAG system with a question.")
    parser.add_argument("query_text", type=str, help="The query text.")
    args = parser.parse_args()
    query_text = args.query_text

    # Query the RAG system.
    query_rag(query_text)

def query_rag(query_text: str):
    """
    Query the RAG system with the given query text.

    Args:
        query_text (str): The query text to search for.
    """
    # Prepare the DB.
    embedding_function = get_embedding_function()
    db = Chroma(persist_directory=CHROMA_PATH, embedding_function=embedding_function)

    # Search the DB.
    results = db.similarity_search_with_score(query_text, k=5)

    # Combine the context from the search results.
    context_text = "\n\n---\n\n".join([doc.page_content for doc, _score in results])

    # Prepare the prompt.
    prompt_template = ChatPromptTemplate.from_template(PROMPT_TEMPLATE)
    prompt = prompt_template.format(context=context_text, question=query_text)

    # Initialize the OpenAI model.
    #
    # NOTE: Make sure to either:
    #   1) Pass `openai_api_key="YOUR_KEY_HERE"` below, OR
    #   2) Set the OPENAI_API_KEY in your environment variables (recommended).
    #
    model = ChatOpenAI(
        openai_api_key = OPENAI_API_KEY,
        model="gpt-3.5-turbo"
    )

    # Generate the response. This returns an object (such as a BaseMessage),
    # which, when converted to string, might include metadata like
    # "content='...' additional_kwargs=... response_metadata=..."
    response = model.invoke(prompt)

    # Convert the response object to a string for parsing.
    raw_response_str = str(response)

    # ----------------------------------------------------------------
    # 1) Extract the "Answer" (the main content) from the raw string
    # ----------------------------------------------------------------
    #
    # The raw string from the ChatOpenAI object often looks like:
    #  content='Some text...' additional_kwargs=... response_metadata=...
    # So we'll capture everything in between content=' ... '.
    #
    # If your library returns just .content directly, you can simply do:
    #   final_answer = response.content
    # but we'll be safe with regex to match the example you showed.
    content_pattern = r"content='(.*?)'"
    match = re.search(content_pattern, raw_response_str, flags=re.DOTALL)
    if match:
        final_answer = match.group(1)
    else:
        # Fallback if we can’t find it easily
        final_answer = raw_response_str

    # ----------------------------------------------------------------
    # 2) Extract & format the "Sources"
    # ----------------------------------------------------------------
    #
    # Each result has doc.metadata["id"], something like:
    #   "C:\\...\\data\\clue.pdf:2:3"
    # We want to break it into (pdf name) and (page number).
    sources_raw = [doc.metadata.get("id", "") for doc, _score in results]

    formatted_sources = []
    for src in sources_raw:
        # If the metadata ID is empty or malformed, skip
        if not src:
            continue
        # The ID is typically "C:\\path\\to\\pdfName.pdf:PAGE:CHUNK"
        # We'll rsplit on ":" because the path might contain colons on Windows.
        try:
            path, page_str, chunk_str = src.rsplit(":", 2)
        except ValueError:
            # If it doesn't split nicely, just keep the whole string
            formatted_sources.append(src)
            continue

        # Extract just the base file name, e.g. "clue.pdf"
        pdf_name = os.path.basename(path)

        # The stored page might be 0-based; many times you'd do page + 1 for user-friendly:
        try:
            page_num = int(page_str) + 1
        except ValueError:
            page_num = page_str  # fallback if it's not an integer

        # Build a nice display
        display_str = f"{pdf_name} (Page {page_num})"
        formatted_sources.append(display_str)

    # ----------------------------------------------------------------
    # 3) Print or Return the final result in the format we want
    # ----------------------------------------------------------------
    print("Answer:")
    print(final_answer.strip())
    print("\nSources:")
    for idx, source in enumerate(formatted_sources, start=1):
        print(f"{idx}. {source}")

    return final_answer

if __name__ == "__main__":
    main()
