import os
from dotenv import load_dotenv
from pinecone import Pinecone, ServerlessSpec
from langchain_pinecone import PineconeVectorStore
from langchain.embeddings import HuggingFaceEmbeddings  # ✅ Hugging Face embeddings

# Load environment variables
load_dotenv()

# Pinecone credentials
PINECONE_API_KEY = os.getenv("PINECONE_API_KEY")
PINECONE_REGION = os.getenv("PINECONE_ENVIRONMENT")  # e.g., "us-east-1"

# Index name and dimension
INDEX_NAME = "autogpt1"
DIMENSION = 384  # must match embedding model dimension

# Initialize Pinecone client
pc = Pinecone(api_key="pcsk_6TQGiu_5V5sRTDyAFViTUtDsjiaZbVVopqVJFr4XJhGm8M4gP174qJk4dRFnWGgmJ1GUqr")

# Create index if it doesn't exist
existing = [idx["name"] for idx in pc.list_indexes()]
if INDEX_NAME not in existing:
    pc.create_index(
        name=INDEX_NAME,
        dimension=DIMENSION,
        metric="cosine",
        spec=ServerlessSpec(cloud="aws", region=PINECONE_REGION)
    )

# Get index handle
index = pc.Index(INDEX_NAME)

# HuggingFace embedding model
embedding_model = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")

# LangChain Pinecone wrapper
vectorstore = PineconeVectorStore(index=index, embedding=embedding_model)

# ✅ Add to Pinecone
def add_to_vector_db(text, metadata=None):
    vectorstore.add_texts([text], metadatas=[metadata or {}])

# ✅ Search Pinecone
def search_similar(query_text, top_k=3):
    return vectorstore.similarity_search(query_text, k=top_k)
