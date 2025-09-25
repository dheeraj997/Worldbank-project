class RAGRetriever:
    def __init__(self, vector_store, embedding_manager):
        self.vector_store = vector_store
        self.embedding_manager = embedding_manager

    def retrieve(self, query: str, top_k=5, score_threshold=0.0):
        query_embedding = self.embedding_manager.generate_embeddings([query])[0]
        results = self.vector_store.collection.query(
            query_embeddings=[query_embedding.tolist()],
            n_results=top_k
        )
        docs = []
        for i, (doc, metadata, dist, doc_id) in enumerate(zip(
            results['documents'][0], results['metadatas'][0], results['distances'][0], results['ids'][0]
        )):
            score = 1 - dist
            if score >= score_threshold:
                docs.append({"id": doc_id, "content": doc, "metadata": metadata, "score": score})
        return docs