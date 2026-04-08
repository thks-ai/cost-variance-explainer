import faiss
import pickle
import numpy as np

# ★ あなたのプロジェクト構造に合わせた正しいパス
INDEX_PATH = "app/vector_store/index.faiss"
PICKLE_PATH = "app/vector_store/vectors.pkl"


class VectorStore:
    def __init__(self):
        print("=== VectorStore Debug Start ===")
        print("[DEBUG] INDEX_PATH :", INDEX_PATH)
        print("[DEBUG] PICKLE_PATH:", PICKLE_PATH)

        # --- FAISS index の読み込み ---
        try:
            self.index = faiss.read_index(INDEX_PATH)
            print("[INFO] FAISS index loaded successfully.")
            print("[INFO] index.ntotal =", self.index.ntotal)
            print("[INFO] index dimension =", self.index.d)
        except Exception as e:
            print(f"[ERROR] Failed to load FAISS index: {e}")
            self.index = None

        # --- vectors.pkl の読み込み ---
        try:
            with open(PICKLE_PATH, "rb") as f:
                self.vectors = pickle.load(f)
            print("[INFO] vectors.pkl loaded successfully.")
            print("[INFO] vectors count =", len(self.vectors))
        except Exception as e:
            print(f"[ERROR] Failed to load vectors.pkl: {e}")
            self.vectors = []

        print("=== VectorStore Debug End ===\n")

    def search(self, query_vector, top_k=5):
        """
        query_vector: list[float] (1536次元)
        top_k: 返す件数
        """

        if self.index is None or len(self.vectors) == 0:
            print("[WARN] VectorStore is empty. (index or vectors missing)")
            return []

        # numpy 形式に変換
        q = np.array([query_vector]).astype("float32")

        # --- FAISS 検索 ---
        distances, indices = self.index.search(q, top_k)

        results = []
        for dist, idx in zip(distances[0], indices[0]):
            if idx == -1:
                continue

            item = self.vectors[idx]

            results.append({
                "reason_log_id": item.get("reason_log_id"),
                "text": item.get("text"),
                "vector": item.get("vector"),
                "score": float(dist)
            })

        return results

