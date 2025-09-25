import numpy as np
from sentence_transformers import SentenceTransformer
from typing import List

class EmbeddingManager:
    def __init__(self, model_name="all-MiniLM-L6-v2"):
        print(f"Loading model {model_name}")
        self.model = SentenceTransformer(model_name)

    def generate_embeddings(self, texts: List[str]) -> np.ndarray:
        return self.model.encode(texts, show_progress_bar=True)