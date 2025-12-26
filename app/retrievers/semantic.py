from sentence_transformers import SentenceTransformer
import faiss
import numpy as np
import os
import json

INDEX_PATH = "app/data/faiss.index"
DOC_PATH = "app/data/documents.json"


class SemanticRetriever:
    def __init__(self):
        self.model = SentenceTransformer("all-MiniLM-L6-v2")
        self.index = None
        self.documents = []

        if os.path.exists(INDEX_PATH) and os.path.exists(DOC_PATH):
            self._load()

    def build_index(self, texts):
        embeddings = self.model.encode(texts, convert_to_numpy=True)
        dim = embeddings.shape[1]

        self.index = faiss.IndexFlatL2(dim)
        self.index.add(embeddings)

        self.documents = texts

        os.makedirs("app/data", exist_ok=True)
        faiss.write_index(self.index, INDEX_PATH)

        with open(DOC_PATH, "w", encoding="utf-8") as f:
            json.dump(self.documents, f)

    def _load(self):
        self.index = faiss.read_index(INDEX_PATH)
        with open(DOC_PATH, "r", encoding="utf-8") as f:
            self.documents = json.load(f)

    def retrieve(self, query, top_k=5):
        if self.index is None:
            return []

        q_emb = self.model.encode([query], convert_to_numpy=True)
        scores, indices = self.index.search(q_emb, top_k)

        results = []
        for idx, score in zip(indices[0], scores[0]):
            if idx < 0 or idx >= len(self.documents):
                continue

            results.append({
                "text": self.documents[idx],
                "score": float(score),
                "source": "semantic"
            })

        return results
