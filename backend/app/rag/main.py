# app/services/rag/main.py

from app.core.enhanced_retriever import EnhancedRetriever
from app.core.query_classifier import QueryClassifier
from app.core.greeting_handler import GreetingHandler
from app.core.rag_chain import EnhancedRAGChain
from app.database.db import create_chat_session, append_message_to_chat
from app.config import OPENAI_API_KEY, PINECONE_API_KEY, PINECONE_ENV, PINECONE_INDEX_NAME, PINECONE_EMBEDDING_DIMENSIONS, CHUNK_SIZE, CHUNK_OVERLAP
from app.vector_search_db.pinecone_db import PineconeDB
from langchain_community.retrievers import BM25Retriever  # make sure to configure this if needed
from langchain.memory import ConversationBufferWindowMemory
from app.utils.embedding_provider import OpenAIEmbeddingProvider
from openai import OpenAI

def initialize_llm():
    # Initialize your OpenAI LLM
    llm = OpenAI(api_key=OPENAI_API_KEY)
    return llm

def get_rag_chain():
    # Instantiate the LLM
    llm = initialize_llm()

    # Set up the vector retriever using PineconeDB.
    pinecone_db = PineconeDB(api_key=PINECONE_API_KEY, environment=PINECONE_ENV, index_name=PINECONE_INDEX_NAME, embedding_dimensions=PINECONE_EMBEDDING_DIMENSIONS)
    
    # For BM25, instantiate with the necessary parameters.
    bm25_retriever = BM25Retriever(  # Ensure you configure BM25Retriever properly, e.g., with your corpus or embedding settings.
        # You might need to pass in the document store or corpus here.
    )
    
    # Configure retrieval parameters.
    from models.configs import RetrievalConfig  # assuming you have a config for retrieval parameters
    retrieval_config = RetrievalConfig(
        sub_queries=3,        # number of sub-queries to generate (adjust as needed)
        viewpoints=3,         # number of viewpoints for opinion queries
        vector_k=5            # number of documents to retrieve
    )
    
    # Create the enhanced retriever.
    enhanced_retriever = EnhancedRetriever(
        vector_retriever=pinecone_db,  # assuming your PineconeDB has the required agnostic interface
        bm25_retriever=bm25_retriever,
        llm=llm,
        config=retrieval_config
    )
    
    # Instantiate the query classifier and greeting handler.
    classifier = QueryClassifier(llm)
    greeting_handler = GreetingHandler(llm)
    
    # Set up conversation memory.
    memory = ConversationBufferWindowMemory(k=5)
    
    # Initialize the Enhanced RAG Chain.
    rag_chain = EnhancedRAGChain(
        retriever=enhanced_retriever,
        classifier=classifier,
        greeting_handler=greeting_handler,
        memory=memory,
        llm=llm
    )
    
    return rag_chain

def answer_question(
    question: str,
    top_k: int,
    threshold: float,
    temperature: float,
    max_tokens: int,
    response_style: str,
    namespace: str,
    model_name: str,
    reasoning: bool = False,
    context: str = None
):
    """
    This function is called by your /ask API route. It uses the RAG chain to process the question.
    """
    rag_chain = get_rag_chain()
    
    # Process the query through the RAG pipeline
    result = rag_chain.process_query(question, context)
    
    # You can post-process the result here (e.g., format the answer or attach source references)
    answer = result.get("answer")
    relevant_chunks = [doc.page_content for doc in result.get("sources", [])]
    
    return {
        "answer": answer,
        "relevant_chunks": relevant_chunks,
        "query_type": result.get("query_type")
    }
