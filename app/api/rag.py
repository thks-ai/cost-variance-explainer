from fastapi import APIRouter
import sqlite3
import numpy as np
import faiss
import re
from sentence_transformers import SentenceTransformer
from openai import OpenAI
from datetime import datetime

router = APIRouter()
client = OpenAI()

# ============================
# SentenceTransformer（MiniLM）
# ============================
model = SentenceTransformer("sentence-transformers/all-MiniLM-L6-v2")

# ============================
# FAISS インデックス読み込み（正規化済み）
# ============================
index = faiss.read_index("data/vector_index/vector.index")

# ============================
# 理由文読み込み（tag + created_at）
# ============================
def load_reasons():
    conn = sqlite3.connect("data/reason_log.db")
    cur = conn.cursor()
    cur.execute("SELECT id, reason, tag, created_at FROM reason_log")
    rows = cur.fetchall()
    conn.close()
    return rows

reasons = load_reasons()

# ============================
# 理由文クリーニング
# ============================
def clean_reason(text: str) -> str:
    text = text.replace("\n", " ")
    text = re.sub(r"\s+", " ", text)
    text = re.sub(r"(と思われる|と考えられる|可能性がある)$", "", text)
    return text.strip()

# ============================
# クエリをカテゴリ分類（LLM）
# ============================
def classify_query_tag(query: str) -> str:
    prompt = f"""
以下の質問を、製造業の原価差異カテゴリの中から最も適切な1つに分類してください。
カテゴリ一覧：
- 材料費
- 価格差異
- 数量差異
- 工数差異
- 不良・歩留まり
- 設備
- 外注費
- その他

質問：
{query}

出力はカテゴリ名のみ。
"""

    res = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": prompt}],
        temperature=0
    )

    return res.choices[0].message.content.strip()

# ============================
# RAG検索（カテゴリ × 類似度 × 時系列 × 重み学習）
# ============================
def search_similar_reasons(query: str, top_k: int = 5):
    # ① クエリをカテゴリ分類
    query_tag = classify_query_tag(query)

    # ② 同じカテゴリの理由文だけ抽出
    filtered = [(i, r, t, c) for (i, r, t, c) in reasons if t == query_tag]

    # fallback：カテゴリ一致が0件のときだけ全体検索
    use_all = False
    if len(filtered) == 0:
        filtered = reasons
        use_all = True

    # ③ 類似度検索
    query_vec = model.encode([query], convert_to_numpy=True)
    query_vec = np.array(query_vec, dtype="float32").reshape(1, -1)
    faiss.normalize_L2(query_vec)

    scores, ids = index.search(query_vec, top_k)

    results = []
    for score, idx in zip(scores[0], ids[0]):

        # 無効スコア除外
        if score < -1e20:
            continue

        # 類似度が低すぎる場合は除外（重要）
        if score < 0.2:
            continue

        reason_id, reason_text, tag, created_at = reasons[idx]

        # カテゴリ一致モードのときはカテゴリ一致のみ採用
        if not use_all and tag != query_tag:
            continue

        # ④ 時系列補正（新しいほど +0.05）
        try:
            dt = datetime.fromisoformat(created_at)
            age_days = (datetime.now() - dt).days
            time_bonus = max(0, 0.05 - age_days * 0.002)
        except:
            time_bonus = 0

        # ⑤ 重み学習（品質スコア × 0.1）
        conn = sqlite3.connect("data/weight_log.db")
        cur = conn.cursor()
        cur.execute("SELECT quality FROM weight_log WHERE reason_id = ?", (reason_id,))
        row = cur.fetchone()
        conn.close()

        weight_bonus = row[0] * 0.1 if row else 0

        final_score = float(score) + time_bonus + weight_bonus

        reason_text = clean_reason(reason_text)

        results.append({
            "id": reason_id,
            "reason": reason_text,
            "tag": tag,
            "created_at": created_at,
            "score": final_score
        })

    # ⑥ スコア順に並び替え
    results = sorted(results, key=lambda x: x["score"], reverse=True)

    return results













