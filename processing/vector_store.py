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

    def add_documents(self, documents, embeddings: np.ndarray, batch_size: int = 5000):
        ids, docs_text, metadatas, embeddings_list = [], [], [], []

        for i, (doc, emb) in enumerate(zip(documents, embeddings)):
            ids.append(f"doc_{uuid.uuid4().hex[:8]}_{i}")
            docs_text.append(doc.page_content)
            metadatas.append({**doc.metadata, "content_length": len(doc.page_content)})
            embeddings_list.append(emb.tolist())

        # Insert in safe batches
        for start in range(0, len(ids), batch_size):
            end = start + batch_size
            self.collection.add(
                ids=ids[start:end],
                documents=docs_text[start:end],
                metadatas=metadatas[start:end],
                embeddings=embeddings_list[start:end],
            )
