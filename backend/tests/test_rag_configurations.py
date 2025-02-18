import pytest
import asyncio
import sys
import os

# Ensure the project root is on sys.path.
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# --- Global variable so our fake Pinecone index knows the current test question ---
CURRENT_TEST_QUESTION = ""

# --- Fake Pinecone Index ---
class FakePineconeIndex:
    def query(self, vector, top_k, include_metadata, namespace, **kwargs):
        global CURRENT_TEST_QUESTION
        q = CURRENT_TEST_QUESTION.lower()
        if "opportunity" in q:
            return {
                "matches": [
                    {
                        "id": "opp-1",
                        "score": 0.95,
                        "metadata": {
                            "text": "Opportunity cost is the trade-off between choices.",
                            "source_file": "econ1.pdf"
                        }
                    },
                    {
                        "id": "opp-2",
                        "score": 0.90,
                        "metadata": {
                            "text": "In economics, opportunity cost measures the foregone alternative.",
                            "source_file": "econ2.pdf"
                        }
                    }
                ]
            }
        elif "production" in q or "system reliability" in q:
            return {
                "matches": [
                    {
                        "id": "prod-1",
                        "score": 0.96,
                        "metadata": {
                            "text": "Production readiness involves monitoring, scaling, reliability, and deployment.",
                            "source_file": "prod1.pdf"
                        }
                    },
                    {
                        "id": "prod-2",
                        "score": 0.93,
                        "metadata": {
                            "text": "System reliability is crucial for production environments.",
                            "source_file": "prod2.pdf"
                        }
                    },
                    {
                        "id": "prod-3",
                        "score": 0.91,
                        "metadata": {
                            "text": "Robust systems require proper readiness checks and performance monitoring.",
                            "source_file": "prod3.pdf"
                        }
                    }
                ]
            }
        else:
            # For out-of-context questions, return a fallback match.
            return {
                "matches": [
                    {
                        "id": "fallback-1",
                        "score": 0.80,
                        "metadata": {
                            "text": "No relevant context found.",
                            "source_file": "fallback.pdf"
                        }
                    }
                ]
            }
    
    def upsert(self, vectors, namespace):
        # Fake upsert does nothing.
        pass

# --- Fake Embedding Function ---
class FakeEmbeddingFunction:
    def embed_query(self, query: str):
        # Return a dummy vector (dimension here is 512).
        return [0.1] * 512

    def embed_documents(self, docs):
        # Return a dummy embedding for each document.
        return [[0.1] * 512 for _ in docs]

# --- Monkey-patch the OpenAI Embeddings ---
from app.clients.openai_embeddings import get_embedding_function as real_get_embedding_function

def fake_get_embedding_function():
    return FakeEmbeddingFunction()

import app.clients.openai_embeddings as embeddings_mod
embeddings_mod.get_embedding_function = fake_get_embedding_function

# --- Monkey-patch the Pinecone index in our RAG module ---
import app.core.rag as rag_mod
rag_mod.pinecone_index = FakePineconeIndex()

# --- Monkey-patch the LLM query function so that we don’t call OpenAI’s API ---
def fake_query_llm(model_name: str, messages: list, temperature: float, max_tokens: int):
    # Return a fake answer; you could customize this further if needed.
    return "Fake answer from LLM."

rag_mod.query_llm = fake_query_llm

# --- Candidate Configurations (example values from tuning experiments) ---
candidate_configurations = [
    {
        "CHUNK_SIZE": 512,
        "CHUNK_OVERLAP": 20,
        "HYBRID_WEIGHT_RATIO": 0.75,
        "TOP_K": 20,
        "SIMILARITY_THRESHOLD": 0.5,
        "TEMPERATURE": 0.7,
        "MAX_TOKENS": 4096  # Set within limits for testing
    },
    {
        "CHUNK_SIZE": 256,
        "CHUNK_OVERLAP": 50,
        "HYBRID_WEIGHT_RATIO": 0.6,
        "TOP_K": 10,
        "SIMILARITY_THRESHOLD": 0.7,
        "TEMPERATURE": 0.7,
        "MAX_TOKENS": 3000
    },
    {
        "CHUNK_SIZE": 768,
        "CHUNK_OVERLAP": 10,
        "HYBRID_WEIGHT_RATIO": 0.8,
        "TOP_K": 30,
        "SIMILARITY_THRESHOLD": 0.5,
        "TEMPERATURE": 0.9,
        "MAX_TOKENS": 3500
    },
]

# --- Test Cases: questions with expected relevant source substrings (or None for out-of-context) ---
test_cases = [
    {
        "question": "What is opportunity cost?",
        "expected_source": "Opportunity cost is the trade-off between choices.",
        "description": "Economics-related question."
    },
    {
        "question": "How do economists measure opportunity cost?",
        "expected_source": "foregone alternative",
        "description": "Another economics question."
    },
    {
        "question": "Tell me about production readiness and system reliability.",
        "expected_source": "Production readiness involves monitoring",
        "description": "Production readiness question."
    },
    {
        "question": "What is the capital of France?",
        "expected_source": None,
        "description": "Out-of-context geography question."
    },
    {
        "question": "Explain the process of photosynthesis in plants.",
        "expected_source": None,
        "description": "Out-of-context science question."
    },
    {
        "question": "Who won the 2022 FIFA World Cup?",
        "expected_source": None,
        "description": "Out-of-context sports question."
    }
]

# --- Helper: Override app configuration parameters ---
import app.config as config

def apply_candidate_config(candidate):
    config.CHUNK_SIZE = candidate["CHUNK_SIZE"]
    config.CHUNK_OVERLAP = candidate["CHUNK_OVERLAP"]
    config.HYBRID_WEIGHT_RATIO = candidate["HYBRID_WEIGHT_RATIO"]
    config.TOP_K = candidate["TOP_K"]
    config.SIMILARITY_THRESHOLD = candidate["SIMILARITY_THRESHOLD"]
    config.TEMPERATURE = candidate["TEMPERATURE"]
    config.MAX_TOKENS = candidate["MAX_TOKENS"]

# --- The Parameterized Test ---
# We use nested parameterization: one over candidate configurations and one over test cases.
@pytest.mark.asyncio
@pytest.mark.parametrize("candidate_config", candidate_configurations)
@pytest.mark.parametrize("test_case", test_cases)
async def test_rag_pipeline(candidate_config, test_case):
    global CURRENT_TEST_QUESTION
    # Apply the candidate configuration.
    apply_candidate_config(candidate_config)

    # Set the current test question for our FakePineconeIndex.
    CURRENT_TEST_QUESTION = test_case["question"]

    # Call the RAG pipeline (answer_question) from our rag module.
    result = await rag_mod.answer_question(
        question=test_case["question"],
        namespace="test-namespace",
        model_name="gpt-3.5-turbo",
        subject_filter=None,
        chat_id=None
    )

    # Assert that an answer is produced.
    assert "answer" in result, "Result should contain an 'answer' field."
    answer = result["answer"]
    assert isinstance(answer, str) and answer.strip() != "", "Answer should be a nonempty string."

    # Assert that we have retrieved chunks.
    assert "relevant_chunks" in result, "Result should contain 'relevant_chunks'."
    chunks = result["relevant_chunks"]
    assert isinstance(chunks, list) and len(chunks) > 0, "There should be at least one retrieved chunk."

    # Check for expected source content if provided.
    if test_case["expected_source"]:
        expected = test_case["expected_source"].lower()
        found = any(expected in chunk.lower() for chunk in chunks)
        assert found, (
            f"Expected source substring '{expected}' not found in retrieved chunks "
            f"for question: {test_case['question']}."
        )
    else:
        # For out-of-context questions, we expect the fallback response.
        fallback_text = "no relevant context found."
        found_fallback = any(fallback_text in chunk.lower() for chunk in chunks)
        assert found_fallback, (
            f"For out-of-context question '{test_case['question']}', expected fallback context not found."
        )

    # Optionally, print configuration and results for debugging.
    print("\nCandidate Config:", candidate_config)
    print("Test Question:", test_case["question"])
    print("Answer:", answer)
    print("Retrieved Chunks:", chunks)
