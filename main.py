from ingestion.pdf_loader import process_all_pdfs_from_s3
from processing.splitter import split_documents
from processing.embeddings import EmbeddingManager
from processing.vector_store import VectorStore
from rag.retriever import RAGRetriever
from rag.groq_llm import GroqLLM
import os
from dotenv import load_dotenv

load_dotenv()
if __name__ == "__main__":
    # 1. Load PDFs
    docs = process_all_pdfs_from_s3(
        os.getenv("BUCKET_NAME"),
        os.getenv("S3_PREFIX")
    )
    chunks = split_documents(docs)

    # 2. Embeddings + VectorStore
    embedder = EmbeddingManager()
    store = VectorStore()
    embeddings = embedder.generate_embeddings([c.page_content for c in chunks])
    store.add_documents(chunks, embeddings)

    # 3. RAG pipeline
    retriever = RAGRetriever(store, embedder)
    groq = GroqLLM()
    query = "What policies are recommended for decarbonization in Africa?"
    context = "\n".join([d["content"] for d in retriever.retrieve(query)])
    answer = groq.generate_response(query, context)

    print("Q:", query)
    print("A:", answer)