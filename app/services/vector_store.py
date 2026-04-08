# app/services/vector_store.py

import faiss
import numpy as np
import json
import os

INDEX_PATH = "data/faiss_index/index.faiss"
META_PATH = "data/faiss_index/meta.json"

class VectorStore:

    def __init__(self):
        self.index = None
        self.meta = None
        self.load()

    def load(self):
        if os.path.exists(INDEX_PATH):
            self.index = faiss.read_index(INDEX_PATH)
        else:
            self.index = None

        if os.path.exists(META_PATH):
            with open(META_PATH, "r", encoding="utf-8") as f:
                self.meta = json.load(f)
        else:
            self.meta = []

    def search(self, query_vector, top_k=5):
        if self.index is None:
            return []

        query = np.array([query_vector]).astype("float32")
        distances, ids = self.index.search(query, top_k)

        results = []
        for idx in ids[0]:
            if idx == -1:
                continue
            results.append(self.meta[idx])

        return results
