# app.py
from fastapi import FastAPI
from pydantic import BaseModel
from ingestion.pdf_loader import process_all_pdfs_from_s3
from processing.splitter import split_documents
from processing.embeddings import EmbeddingManager
from processing.vector_store import VectorStore
from rag.retriever import RAGRetriever
from rag.groq_llm import GroqLLM
import os
from dotenv import load_dotenv
from fastapi.middleware.cors import CORSMiddleware

load_dotenv()
app = FastAPI()

# Allow React frontend to call this backend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # React dev server
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Load docs once at startup
docs = process_all_pdfs_from_s3(
    os.getenv("BUCKET_NAME"),
    os.getenv("S3_PREFIX")
)
chunks = split_documents(docs)
embedder = EmbeddingManager()
store = VectorStore()
embeddings = embedder.generate_embeddings([c.page_content for c in chunks])
store.add_documents(chunks, embeddings)
retriever = RAGRetriever(store, embedder)
groq = GroqLLM()

class QueryRequest(BaseModel):
    query: str

@app.post("/ask")
def ask_question(req: QueryRequest):
    context = "\n".join([d["content"] for d in retriever.retrieve(req.query)])
    answer = groq.generate_response(req.query, context)
    return {"query": req.query, "answer": answer}
