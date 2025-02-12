import pytest
import logging
import os
import sys

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# Import the answer_question function for testing
from app.services.rag.main import answer_question

# --- Create fake implementations for testing purposes ---
class FakeIndex:
    def query(self, vector, top_k, include_metadata, namespace):
        # Return a fake query response with predetermined matches.
        return {
            "matches": [
                {
                    "id": "fake-id-1",
                    "score": 0.95,
                    "metadata": {
                        "text": "This is a sample passage about production readiness.",
                        "source_file": "sample.pdf"
                    }
                },
                {
                    "id": "fake-id-2",
                    "score": 0.90,
                    "metadata": {
                        "text": "Another relevant passage about test queries.",
                        "source_file": "sample2.pdf"
                    }
                }
            ]
        }
    
    def upsert(self, vectors, namespace):
        pass

def fake_init_pinecone():
    return FakeIndex()

def fake_embed_query(query: str):
    # Return a dummy embedding vector (the exact values are not important for the fake test)
    return [0.1] * 1536

class FakeEmbedding:
    def embed_query(self, query: str):
        return fake_embed_query(query)
    
    def embed_documents(self, docs):
        # Return dummy embeddings for each document in the list.
        return [[0.1] * 1536 for _ in docs]

def fake_get_embedding_function():
    return FakeEmbedding()

# Monkey-patch the functions in the modules used by answer_question.
import app.services.rag.main as rag_main
rag_main.init_pinecone = fake_init_pinecone

import app.services.embeddings.generate_embeddings as emb_gen
emb_gen.get_embedding_function = fake_get_embedding_function

# --- Define sample test queries ---
@pytest.mark.parametrize("query", [
    "How do I ensure production readiness?",
    "What steps are needed for a robust system?",
    "How can I test retrieval performance?"
])
def test_answer_question(query):
    result = rag_main.answer_question(
        question=query,
        top_k=5,
        threshold=0.85,
        temperature=0.7,
        max_tokens=150,
        response_style="detailed",
        namespace="test-namespace",
        model_name="gpt-3.5-turbo",
        reasoning=False
    )
    # Check that an answer is returned and that relevant_chunks contains entries.
    assert "answer" in result
    assert "relevant_chunks" in result
    assert len(result["relevant_chunks"]) > 0

    # For retrieval relevance, check that a known passage is among the fetched results.
    expected_passage = "This is a sample passage about production readiness."
    found = any(expected_passage in chunk for chunk in result["relevant_chunks"])
    assert found, "Expected passage not found in the top results."

    # Optionally, log the result for debugging.
    logging.getLogger(__name__).info(f"Test query: '{query}' returned: {result}")
