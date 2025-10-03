import logging
import itertools
import time
import shutil
import os
import sys
import json
import asyncio
import uuid
from datetime import datetime
import concurrent.futures
from pathlib import Path
from typing import List, Dict, Optional
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.document_loaders import PyPDFLoader
from langchain.schema import Document

# Add the project root directory to the Python path
project_root = str(Path(__file__).parent.parent.parent)
sys.path.append(project_root)

from app.config import (
    BACKEND_DIR,
    RAW_TEST_DATA_PATH,
    PROCESSED_TEST_DATA_PATH,
    
)
from app.vector_db.pinecone_db import delete_all_data
from app.routes.ask import process_question, QuestionPayload
from app.utils.generate_embeddings import get_embedding_function
from app.clients import pinecone_index
from app.utils.pdf_text_cleaner import clean_pdf_text

PINECONE_NAMESPACE = "test-namespace"

# Test configuration
TEST_QUESTIONS = [
    # ---------------------
    # 10 RELEVANT QUESTIONS
    # ---------------------
    {
        "query": "What is the basic definition of opportunity cost?",
        "expected_keywords": ["trade-off", "foregone", "choice", "scarcity"]
    },
    {
        "query": "How do economists use opportunity cost to measure the cost of production?",
        "expected_keywords": ["economists", "trade-off", "foregone", "production"]
    },
    {
        "query": "In microeconomics, how does opportunity cost relate to resource allocation?",
        "expected_keywords": ["resource allocation", "alternatives", "choice", "foregone benefit"]
    },
    {
        "query": "Can you provide a real-life example of opportunity cost in personal finance?",
        "expected_keywords": ["personal finance", "foregone", "trade-off", "sacrifice"]
    },
    {
        "query": "Why do opportunity costs vary between individuals or firms?",
        "expected_keywords": ["alternatives", "cost differences", "trade-off", "preferences"]
    },
    {
        "query": "How does opportunity cost affect investment decisions in capital markets?",
        "expected_keywords": ["investment", "trade-off", "capital markets", "foregone returns"]
    },
    {
        "query": "What role does opportunity cost play in government policy-making?",
        "expected_keywords": ["policy-making", "budgeting", "trade-off", "scarcity"]
    },
    {
        "query": "Explain the concept of opportunity cost in the context of time management.",
        "expected_keywords": ["time management", "alternatives", "lost opportunity", "trade-off"]
    },
    {
        "query": "Is opportunity cost always measured in monetary terms?",
        "expected_keywords": ["non-monetary", "foregone", "utility", "choice"]
    },
    {
        "query": "What is the difference between explicit and implicit opportunity costs?",
        "expected_keywords": ["explicit cost", "implicit cost", "foregone", "trade-off"]
    },

    # -------------------------
    # 10 NON-RELEVANT QUESTIONS
    # -------------------------
    {
        "query": "What is the capital city of Canada?",
        "expected_keywords": ["ottawa", "capital", "geography"]
    },
    {
        "query": "Who won the 2022 FIFA World Cup?",
        "expected_keywords": ["argentina", "soccer", "tournament"]
    },
    {
        "query": "Explain the process of photosynthesis in plants.",
        "expected_keywords": ["photosynthesis", "chlorophyll", "sunlight"]
    },
    {
        "query": "What are the main differences between HTTP and HTTPS protocols?",
        "expected_keywords": ["encryption", "TLS", "port 443"]
    },
    {
        "query": "How do I bake a classic chocolate cake from scratch?",
        "expected_keywords": ["cake", "baking", "recipe"]
    },
    {
        "query": "Describe the orbital path of Earth around the Sun.",
        "expected_keywords": ["ellipse", "astronomy", "revolution"]
    },
    {
        "query": "When did the first human land on the Moon?",
        "expected_keywords": ["apollo 11", "1969", "NASA"]
    },
    {
        "query": "What are the basic concepts in object-oriented programming?",
        "expected_keywords": ["encapsulation", "inheritance", "polymorphism"]
    },
    {
        "query": "Who was Ludwig van Beethoven?",
        "expected_keywords": ["composer", "classical music", "pianist"]
    },
    {
        "query": "How can I improve my running stamina?",
        "expected_keywords": ["cardiovascular", "endurance", "training"]
    }
]


CHUNK_SIZE_OPTIONS = [300, 500, 750, 1000]
CHUNK_OVERLAP_OPTIONS = [50, 100, 150]
THRESHOLD_OPTIONS = [0.5, 0.7, 0.9]

def create_splitter(chunk_size: int, chunk_overlap: int) -> RecursiveCharacterTextSplitter:
    """Create a text splitter with specified parameters."""
    return RecursiveCharacterTextSplitter(
        chunk_size=chunk_size,
        chunk_overlap=chunk_overlap,
        length_function=len,
        separators=["\n\n", "\n", ".", "!", "?", ",", " ", ""]
    )

def load_and_chunk_pdf(
    pdf_path: str,
    chunk_size: int,
    chunk_overlap: int
) -> List[Document]:
    """
    Test-specific implementation of PDF loading and chunking.
    """
    print(f"\nChunking PDF: {pdf_path}")
    print(f"Parameters: chunk_size={chunk_size}, chunk_overlap={chunk_overlap}")
    
    try:
        loader = PyPDFLoader(pdf_path)
        pages = loader.load()
        print(f"Loaded {len(pages)} pages from PDF")
        
        splitter = create_splitter(chunk_size, chunk_overlap)
        
        all_chunks = []
        for page_num, page in enumerate(pages, 1):
            chunks = splitter.split_documents([page])
            
            for chunk in chunks:
                # Clean the text and add metadata
                if hasattr(chunk, "page_content") and chunk.page_content:
                    chunk.page_content = clean_pdf_text(chunk.page_content)
                
                chunk.metadata.update({
                    "source_file": os.path.basename(pdf_path),
                    "page_number": page_num
                })
                all_chunks.append(chunk)
            
            print(f"Page {page_num}: Created {len(chunks)} chunks")
        
        print(f"Total chunks created: {len(all_chunks)}")
        return all_chunks
    
    except Exception as e:
        print(f"Error chunking PDF: {e}")
        return []

def embed_and_upsert_test_chunks(
    chunks: List[Document],
    namespace: str,
    similarity_threshold: float,
    exact_match_threshold: float
) -> None:
    """
    Test-specific embed and upsert function that mimics the original pinecone_db.py logic
    but with configurable threshold values.
    """
    if not chunks:
        print("No chunks to process")
        return
    
    print(f"\nProcessing {len(chunks)} chunks")
    print(f"Using thresholds: similarity={similarity_threshold}, exact_match={exact_match_threshold}")
    
    embedding_func = get_embedding_function()
    index = pinecone_index
    
    # Extract non-empty text chunks
    chunk_texts = [chunk.page_content.strip() for chunk in chunks if chunk.page_content.strip()]
    if not chunk_texts:
        print("No valid text found in chunks")
        return
    
    try:
        # Generate embeddings
        print("Generating embeddings...")
        embeddings = embedding_func.embed_documents(chunk_texts)
        
        # Run similarity checks concurrently
        print("Running similarity checks...")
        similarity_results = [None] * len(chunk_texts)
        with concurrent.futures.ThreadPoolExecutor(max_workers=8) as executor:
            future_to_index = {
                executor.submit(
                    index.query,
                    vector=emb,
                    top_k=1,
                    include_metadata=True,
                    namespace=namespace
                ): i for i, emb in enumerate(embeddings)
            }
            for future in concurrent.futures.as_completed(future_to_index):
                i = future_to_index[future]
                try:
                    similarity_results[i] = future.result()
                except Exception as exc:
                    print(f"Similarity check for chunk {i} failed: {exc}")
                    similarity_results[i] = None
        
        # Build upsert vectors based on similarity checks
        vectors = []
        for i, (chunk_text, embedding) in enumerate(zip(chunk_texts, embeddings)):
            result = similarity_results[i]
            vector_id = None
            matched_score = 0.0
            
            # Get original chunk's metadata
            original_chunk = chunks[i]
            page_number = original_chunk.metadata.get("page_number", None)
            source_file = original_chunk.metadata.get("source_file", "unknown")
            
            if result and "matches" in result and result["matches"]:
                best_match = result["matches"][0]
                matched_score = best_match["score"]
                
                if matched_score >= exact_match_threshold:
                    print(f"Skipping chunk {i} (score={matched_score:.5f}). Identical chunk exists.")
                    continue
                elif matched_score >= similarity_threshold:
                    vector_id = best_match["id"]
                    print(f"Updating chunk {i} (score={matched_score:.5f}) with existing ID={vector_id}")
            
            if vector_id is None:
                vector_id = f"test-{uuid.uuid4()}"
                print(f"Inserting new chunk {i} (score={matched_score:.5f}). ID={vector_id}")
            
            vectors.append({
                "id": vector_id,
                "values": embedding,
                "metadata": {
                    "text": chunk_text,
                    "source_file": source_file,
                    "page_number": page_number
                }
            })
        
        # Upsert to Pinecone
        if vectors:
            print(f"Upserting {len(vectors)} vectors to Pinecone...")
            pinecone_index.upsert(vectors=vectors, namespace=namespace)
            print("Upsert complete")
        else:
            print("No vectors to upsert (all chunks were duplicates)")
        
    except Exception as e:
        print(f"Error processing chunks: {e}")

def reset_pdfs():
    """Move PDFs back to RAW_TEST_DATA_PATH for testing."""
    if not os.path.exists(PROCESSED_TEST_DATA_PATH):
        return
        
    for fname in os.listdir(PROCESSED_TEST_DATA_PATH):
        if fname.lower().endswith(".pdf"):
            src = os.path.join(PROCESSED_TEST_DATA_PATH, fname)
            dst = os.path.join(RAW_TEST_DATA_PATH, fname)
            shutil.move(src, dst)

def calculate_score(answer: str, expected_keywords: List[str]) -> float:
    """Calculate simple keyword-based score."""
    print(f"\nCalculating score...")
    print(f"Answer: {answer[:200]}... (truncated)")
    print(f"Expected keywords: {expected_keywords}")
    
    answer_lower = answer.lower()
    hits = sum(keyword.lower() in answer_lower for keyword in expected_keywords)
    score = hits / len(expected_keywords)
    
    print(f"Found {hits}/{len(expected_keywords)} keywords. Score: {score:.2f}")
    return score

async def run_single_test(question: str, expected_keywords: List[str], threshold: float) -> float:
    """Run a single test query."""
    payload = QuestionPayload(
        question=question,
        similarityThreshold=threshold,
        similarResults=5,
        temperature=0.7,
        maxTokens=200,
        responseStyle="detailed",
        modelName="openai/gpt-3.5-turbo"  # OpenRouter format
    )

    result = await process_question(payload, chat_id="dummy-chat-id")
    return calculate_score(result["answer"], expected_keywords)

async def run_experiment():
    """Run the complete parameter tuning experiment."""
    results = []
    start_time = datetime.now()
    
    # Get list of PDFs to process
    pdf_files = [f for f in os.listdir(RAW_TEST_DATA_PATH) if f.lower().endswith('.pdf')]
    if not pdf_files:
        print("No PDFs found in RAW_TEST_DATA_PATH")
        return
    
    total_combinations = len(CHUNK_SIZE_OPTIONS) * len(CHUNK_OVERLAP_OPTIONS) * len(THRESHOLD_OPTIONS)
    print(f"\nTesting {total_combinations} parameter combinations")
    
    experiment_data = {
        "start_time": start_time.isoformat(),
        "pdfs_tested": pdf_files,
        "test_questions": TEST_QUESTIONS,
        "parameters_tested": {
            "chunk_sizes": CHUNK_SIZE_OPTIONS,
            "chunk_overlaps": CHUNK_OVERLAP_OPTIONS,
            "thresholds": THRESHOLD_OPTIONS
        },
        "results": []
    }
    
    for cs in CHUNK_SIZE_OPTIONS:
        for co in CHUNK_OVERLAP_OPTIONS:
            for sim_thresh in THRESHOLD_OPTIONS:
                # Using a fixed ratio for exact match threshold
                exact_thresh = min(1.0, sim_thresh + 0.2)
                
                print(f"\n{'='*50}")
                print(f"Testing configuration:")
                print(f"  Chunk size: {cs}")
                print(f"  Chunk overlap: {co}")
                print(f"  Similarity threshold: {sim_thresh}")
                print(f"  Exact match threshold: {exact_thresh}")
                
                test_start_time = datetime.now()
                
                # Reset and prepare
                reset_pdfs()
                
                try:
                    delete_all_data(namespace=PINECONE_NAMESPACE)
                    print("Successfully deleted existing data")
                except Exception as e:
                    if "Namespace not found" in str(e):
                        print("Namespace already deleted or doesn't exist, continuing...")
                    else:
                        print(f"Warning: Unexpected error during data deletion: {e}")
                        print("Continuing with experiment...")
                
                chunk_counts = {}
                # Process each PDF with current parameters
                for pdf_file in pdf_files:
                    pdf_path = os.path.join(RAW_TEST_DATA_PATH, pdf_file)
                    
                    # Chunk the PDF
                    chunks = load_and_chunk_pdf(pdf_path, cs, co)
                    chunk_counts[pdf_file] = len(chunks)
                    
                    # Embed and store chunks with both threshold values
                    embed_and_upsert_test_chunks(
                        chunks=chunks,
                        namespace=PINECONE_NAMESPACE,
                        similarity_threshold=sim_thresh,
                        exact_match_threshold=exact_thresh
                    )
                
                # Run test questions
                test_scores = []
                question_results = []
                for test in TEST_QUESTIONS:
                    score = await run_single_test(
                        test["query"],
                        test["expected_keywords"],
                        sim_thresh
                    )
                    test_scores.append(score)
                    question_results.append({
                        "question": test["query"],
                        "score": score
                    })
                
                avg_score = sum(test_scores) / len(test_scores)
                test_duration = (datetime.now() - test_start_time).total_seconds()
                
                result = {
                    "parameters": {
                        "chunk_size": cs,
                        "chunk_overlap": co,
                        "similarity_threshold": sim_thresh,
                        "exact_match_threshold": exact_thresh
                    },
                    "results": {
                        "average_score": avg_score,
                        "chunk_counts": chunk_counts,
                        "question_scores": question_results,
                        "test_duration_seconds": test_duration
                    }
                }
                
                experiment_data["results"].append(result)
                print(f"Average score: {avg_score:.3f}")
    
    # Add completion time
    experiment_data["end_time"] = datetime.now().isoformat()
    experiment_data["total_duration_seconds"] = (datetime.now() - start_time).total_seconds()
    
    # Sort results by average score
    experiment_data["results"].sort(
        key=lambda x: x["results"]["average_score"], 
        reverse=True
    )
    
    # Save results to JSON file with timestamp
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    results_dir = os.path.join(project_root, "test_results")
    os.makedirs(results_dir, exist_ok=True)
    
    json_path = os.path.join(results_dir, f"parameter_test_results_{timestamp}.json")
    with open(json_path, 'w') as f:
        json.dump(experiment_data, f, indent=2)
    
    print(f"\nResults saved to: {json_path}")
    
    # Print summary of best results
    print("\nTop 5 Configurations:")
    for i, r in enumerate(experiment_data["results"][:5], 1):
        params = r["parameters"]
        score = r["results"]["average_score"]
        print(f"\n{i}. Score: {score:.3f}")
        print(f"   Chunk Size: {params['chunk_size']}")
        print(f"   Overlap: {params['chunk_overlap']}")
        print(f"   Similarity Threshold: {params['similarity_threshold']:.2f}")
        print(f"   Exact Match Threshold: {params['exact_match_threshold']:.2f}")
        
    reset_pdfs()

def main():
    asyncio.run(run_experiment())

if __name__ == "__main__":
    main()