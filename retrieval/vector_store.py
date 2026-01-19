import faiss
import numpy as np
from sentence_transformers import SentenceTransformer

class VectorStore:
    def __init__(self, model_name="all-MiniLM-L6-v2"):
        self.model = SentenceTransformer(model_name)
        self.index = None
        self.chunk_map = {}
        self.dimension = None

    def build(self, chunks):
        texts = [c["text"] for c in chunks]
        embeddings = self.model.encode(texts, show_progress_bar=True)

        self.dimension = embeddings.shape[1]
        self.index = faiss.IndexFlatIP(self.dimension)
        faiss.normalize_L2(embeddings)

        self.index.add(embeddings)

        for i, chunk in enumerate(chunks):
            self.chunk_map[i] = chunk

    def search(self, query, top_k=5):
        query_emb = self.model.encode([query])
        faiss.normalize_L2(query_emb)

        scores, indices = self.index.search(query_emb, top_k)

        results = []
        for score, idx in zip(scores[0], indices[0]):
            if idx == -1:
                continue
            chunk = self.chunk_map[idx]
            results.append((chunk, float(score)))

        return results
