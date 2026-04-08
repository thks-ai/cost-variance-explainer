import sqlite3
import numpy as np
import faiss
from sentence_transformers import SentenceTransformer
import os

# ============================
# モデル読み込み（384次元）
# ============================
model = SentenceTransformer("sentence-transformers/all-MiniLM-L6-v2")

# ============================
# DBから理由文を取得
# ============================
def load_reasons():
    conn = sqlite3.connect("data/reason_log.db")
    cur = conn.cursor()
    cur.execute("SELECT id, reason FROM reason_log")
    rows = cur.fetchall()
    conn.close()
    return rows

reasons = load_reasons()
texts = [r[1] for r in reasons]

# ============================
# 埋め込み生成（float32）
# ============================
embeddings = model.encode(texts, convert_to_numpy=True).astype("float32")

# ============================
# Cosine 類似度用に正規化
# ============================
faiss.normalize_L2(embeddings)

# ============================
# 次元数（384）
# ============================
dim = embeddings.shape[1]
print("Embedding dimension =", dim)

# ============================
# FAISS IndexFlatIP（Cosine）
# ============================
index = faiss.IndexFlatIP(dim)

# ベクトル追加
index.add(embeddings)

# ============================
# 保存先を rag.py と完全一致させる
# ============================
os.makedirs("data/vector_index", exist_ok=True)
faiss.write_index(index, "data/vector_index/vector.index")

print("FAISS index rebuilt with cosine similarity.")




