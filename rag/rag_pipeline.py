from ingestion.pdf_loader import process_all_pdfs_from_s3
from processing.splitter import split_documents
from processing.embeddings import EmbeddingManager
from processing.vector_store import VectorStore
from rag.retriever import RAGRetriever
from rag.groq_llm import GroqLLM


# ---------------- Ingestion ----------------
class IngestionPipeline:
    def __init__(self, bucket_name, prefix, embedder=None, store=None):
        self.bucket_name = bucket_name
        self.prefix = prefix
        self.embedder = embedder or EmbeddingManager()
        self.store = store or VectorStore()

    def run(self):
        docs = process_all_pdfs_from_s3(self.bucket_name, self.prefix)
        chunks = split_documents(docs)
        embeddings = self.embedder.generate_embeddings([c.page_content for c in chunks])
        self.store.add_documents(chunks, embeddings)
        print("✅ Ingestion complete!")


# ---------------- Query ----------------
class QueryPipeline:
    def __init__(self, store=None, embedder=None, llm=None):
        self.embedder = embedder or EmbeddingManager()
        self.store = store or VectorStore()
        self.retriever = RAGRetriever(self.store, self.embedder)
        self.llm = GroqLLM()

    def ask(self, query: str) -> str:
        context = "\n".join([d["content"] for d in self.retriever.retrieve(query)])
        return self.llm.generate_response(query, context)
