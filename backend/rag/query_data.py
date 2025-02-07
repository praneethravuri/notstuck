import argparse
import os
import re
from dotenv import load_dotenv

from langchain_chroma import Chroma
from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI
from get_embedding_function import get_embedding_function

load_dotenv()

CHROMA_PATH = os.path.join(os.path.dirname(__file__), "..", "chroma")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

# Template for the prompt
PROMPT_TEMPLATE = """
Answer the question based on the following context. 
If there is no relevant context, use your general knowledge to answer the question. 
Do not tell the user you got this answer from the context.
Format the answer in markdown

Context:
{context}

---
Question: {question}
"""

def main():
    parser = argparse.ArgumentParser(description="Query the RAG system with a question.")
    parser.add_argument("query_text", type=str, help="The query text.")
    args = parser.parse_args()
    query_text = args.query_text

    query_rag(query_text)

def query_rag(query_text: str):
    # Prepare the DB.
    embedding_function = get_embedding_function()
    db = Chroma(persist_directory=CHROMA_PATH, embedding_function=embedding_function)

    # Retrieve from the DB with similarity scores
    results = db.similarity_search_with_score(query_text, k=5)
    
    # ----------------------------------------------------------------
    # 1) Filter by a threshold.
    #    - If your DB returns *distance*, you want distance < threshold
    #    - If your DB returns *similarity*, you want similarity > threshold
    #
    #    Let's assume these "scores" are distances, so lower is better.
    #    Adjust the threshold based on your typical data:
    # ----------------------------------------------------------------
    THRESHOLD = 0.8
    filtered_results = [(doc, score) for doc, score in results if score < THRESHOLD]

    if filtered_results:
        # If we have at least one doc above the threshold of relevance,
        # combine them into a context string
        context_text = "\n\n---\n\n".join([doc.page_content for doc, _ in filtered_results])
    else:
        # If no document is relevant enough, pass an empty context 
        # (or some note that no relevant docs were found)
        context_text = ""

    # Prepare the prompt
    prompt_template = ChatPromptTemplate.from_template(PROMPT_TEMPLATE)
    prompt = prompt_template.format(context=context_text, question=query_text)

    # Initialize the OpenAI model
    model = ChatOpenAI(
        openai_api_key=OPENAI_API_KEY,
        model="gpt-3.5-turbo",
    )

    # Generate the response
    response = model.invoke(prompt)
    raw_response_str = str(response)

    # Use regex to extract the content (if needed)
    content_pattern = r"content='(.*?)'"
    match = re.search(content_pattern, raw_response_str, flags=re.DOTALL)
    if match:
        final_answer = match.group(1)
    else:
        final_answer = raw_response_str

    # Optionally, create a list of sources
    sources_raw = [doc.metadata.get("id", "") for doc, _score in filtered_results]
    formatted_sources = []
    for src in sources_raw:
        if not src:
            continue
        try:
            path, page_str, chunk_str = src.rsplit(":", 2)
            pdf_name = os.path.basename(path)
            page_num = int(page_str) + 1  # if stored page is 0-based
            formatted_sources.append(f"{pdf_name} (Page {page_num})")
        except ValueError:
            formatted_sources.append(src)

    print("Answer:")
    print(final_answer.strip())
    print("\nSources:")
    if formatted_sources:
        for idx, source in enumerate(formatted_sources, start=1):
            print(f"{idx}. {source}")
    else:
        print("No relevant document sources used.")

    return final_answer

if __name__ == "__main__":
    main()
