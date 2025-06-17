import os
from dotenv import load_dotenv
from langchain.vectorstores import Pinecone as LangchainPinecone
from langchain.embeddings import HuggingFaceEmbeddings
from pinecone import Pinecone, ServerlessSpec

load_dotenv()

api_key = os.getenv("PINECONE_API_KEY")
environment = os.getenv("PINECONE_ENVIRONMENT")  # "us-east-1"
index_name = "autogpt1"
dimension = 384

# Initialize Pinecone client (v3+)
pc = Pinecone(api_key=api_key)

# Create index if it doesn't exist
if index_name not in pc.list_indexes().names():
    pc.create_index(
        name=index_name,
        dimension=dimension,
        metric="cosine",
        spec=ServerlessSpec(cloud="aws", region=environment)
    )

# ✅ Get the actual index object, not just name
index = pc.Index(index_name)

# HuggingFace embeddings
embedding_model = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")

# Add to Pinecone using LangChain
def add_to_vector_db(text, metadata=None):
    LangchainPinecone.from_texts(
        texts=[text],
        embedding=embedding_model,
        index=index,  # ✅ Pass actual index object, not index_name
        metadatas=[metadata or {}]
    )


# Semantic search
def search_similar(query_text, top_k=3):
    vectorstore = LangchainPinecone(index, embedding_model, text_key="text")
    return vectorstore.similarity_search(query_text, k=top_k)
