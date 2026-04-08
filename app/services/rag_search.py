from app.services.vector_store import VectorStore
from openai import OpenAI
import numpy as np

client = OpenAI()
vs = VectorStore()

SIMILARITY_THRESHOLD = 0.75  # 類似度の最低ライン

def cosine_similarity(a, b):
    a = np.array(a)
    b = np.array(b)
    return np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b))

def rag_search(query: str, top_k: int = 5):
    # クエリをベクトル化
    emb = client.embeddings.create(
        model="text-embedding-3-small",
        input=query
    )
    query_vector = emb.data[0].embedding

    # FAISS 検索
    results = vs.search(query_vector, top_k=top_k)

    # 類似度スコアを計算してフィルタリング
    filtered = []
    for r in results:
        score = cosine_similarity(query_vector, r["vector"])
        if score >= SIMILARITY_THRESHOLD:
            filtered.append({
                "reason_log_id": r["reason_log_id"],
                "text": r["text"],
                "score": float(score)
            })

    return filtered


