from langchain_community.retrievers import PineconeHybridSearchRetriever
from app.utils.generate_embeddings import get_embedding_function
from pinecone_text.sparse import BM25Encoder
from app.clients import pinecone_index

# Create your dense and sparse encoder instances
dense_embedding_func = get_embedding_function()
bm25_encoder = BM25Encoder().default()  # or your fitted BM25Encoder

# Create the retriever
retriever = PineconeHybridSearchRetriever(
    embeddings=dense_embedding_func,
    sparse_encoder=bm25_encoder,
    index=pinecone_index
)

# Test a query
result = retriever.invoke("example query")
print(result)
