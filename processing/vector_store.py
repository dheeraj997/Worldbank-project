import os, uuid, chromadb
import numpy as np

class VectorStore:
    def __init__(self, collection_name="pdf_documents", persist_directory="../data/vector_store"):
        os.makedirs(persist_directory, exist_ok=True)
        self.client = chromadb.PersistentClient(path=persist_directory)
        self.collection = self.client.get_or_create_collection(
            name=collection_name,
            metadata={"description": "PDF embeddings for RAG"}
        )

    def add_documents(self, documents, embeddings: np.ndarray):
        ids, docs_text, metadatas, embeddings_list = [], [], [], []
        for i, (doc, emb) in enumerate(zip(documents, embeddings)):
            ids.append(f"doc_{uuid.uuid4().hex[:8]}_{i}")
            docs_text.append(doc.page_content)
            metadatas.append({**doc.metadata, "content_length": len(doc.page_content)})
            embeddings_list.append(emb.tolist())
        self.collection.add(ids=ids, documents=docs_text, metadatas=metadatas, embeddings=embeddings_list)