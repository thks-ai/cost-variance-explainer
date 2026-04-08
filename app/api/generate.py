from fastapi import APIRouter
from pydantic import BaseModel
from app.api.rag import search_similar_reasons
from openai import OpenAI
import sqlite3
import re

router = APIRouter()
client = OpenAI()

class Query(BaseModel):
    query: str

# ============================
# 理由文タグ分類（簡易ルール）
# ============================
def classify_reason_tag(reason: str) -> str:
    text = reason

    if any(k in text for k in ["材料", "原料", "仕入"]):
        return "材料費"
    if any(k in text for k in ["価格", "単価"]):
        return "価格差異"
    if any(k in text for k in ["数量", "量", "過剰", "不足"]):
        return "数量差異"
    if any(k in text for k in ["工数", "作業", "時間"]):
        return "工数差異"
    if any(k in text for k in ["不良", "歩留まり", "欠陥"]):
        return "不良・歩留まり"
    if any(k in text for k in ["設備", "機械", "停止"]):
        return "設備"
    if any(k in text for k in ["外注", "委託"]):
        return "外注費"

    return "その他"

# ============================
# 理由文の正規化
# ============================
def normalize_reason(text: str) -> str:
    text = text.replace("\n", " ")
    text = re.sub(r"\s+", " ", text)
    text = re.sub(r"(と思われる|と考えられる|可能性がある|と推測される)$", "", text)
    text = re.sub(r"ために", "ため", text)
    text = re.sub(r"ことにより", "ことが要因となり", text)
    text = re.sub(r"によって", "ため", text)

    if not text.endswith("です"):
        text = text.rstrip("。") + "ためです"

    return text.strip()

# ============================
# 理由文の自動要約
# ============================
def summarize_reason(text: str) -> str:
    prompt = f"""
以下の文章を、意味を変えずに **1文・80〜120文字** に要約してください。
文体は「です・ます調」、箇条書き禁止。

文章：
{text}
"""

    res = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": prompt}],
        temperature=0
    )

    return res.choices[0].message.content.strip()

# ============================
# 理由文の品質スコアリング
# ============================
def evaluate_reason_quality(text: str) -> float:
    prompt = f"""
以下の文章の品質を 0〜1 の数値で評価してください。

【評価基準】
- 明確さ
- 一貫性
- 文法の正しさ
- 冗長性の少なさ
- 製造業の理由文としての妥当性

出力は数値のみ（例：0.82）。

文章：
{text}
"""

    res = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": prompt}],
        temperature=0
    )

    score_str = res.choices[0].message.content.strip()

    try:
        return float(score_str)
    except:
        return 0.0

# ============================
# 自己学習保存
# ============================
def save_reason_to_db(reason: str):
    normalized = normalize_reason(reason)
    summarized = summarize_reason(normalized)
    quality = evaluate_reason_quality(summarized)

    if quality < 0.70:
        print("品質不足のため保存しません:", summarized)
        return

    tag = classify_reason_tag(summarized)

    conn = sqlite3.connect("data/reason_log.db")
    cur = conn.cursor()

    cur.execute("SELECT id FROM reason_log WHERE reason = ?", (summarized,))
    row = cur.fetchone()

    if row:
        reason_id = row[0]
    else:
        cur.execute(
            "INSERT INTO reason_log (reason, tag, created_at) VALUES (?, ?, datetime('now'))",
            (summarized, tag)
        )
        conn.commit()
        reason_id = cur.lastrowid

    conn.close()

    conn = sqlite3.connect("data/weight_log.db")
    cur = conn.cursor()
    cur.execute(
        "INSERT INTO weight_log (reason_id, quality, created_at) VALUES (?, ?, datetime('now'))",
        (reason_id, quality)
    )
    conn.commit()
    conn.close()

# ============================
# /generate 本体
# ============================
@router.post("/generate")
def generate_answer(data: Query):
    query = data.query

    results = search_similar_reasons(query)

    weighted_refs = []
    for r in results:
        weighted_refs.append({
            "reason": r["reason"],
            "tag": r["tag"],
            "created_at": r["created_at"],
            "score": round(r["score"], 3)
        })

    prompt = f"""
あなたは製造業の改善活動を支援するAIアシスタントです。
以下の「参照理由文（重み付き）」をもとに、
ユーザーの質問に対して **1文で簡潔かつ丁寧に** 回答してください。

【重要ルール】
- 重みの高い理由文を最優先で統合する
- 事実のみを述べ、推測や新情報の追加は禁止
- 参照文にない内容は絶対に書かない
- 文体は「です・ます調」
- 1文でまとめる（80〜130文字）
- 箇条書き禁止
- 「参照文によると」などのメタ表現禁止
- 重複内容は自然に統合する
- 参照文が1件でも自然に統合する
- 参照文が0件の場合は「情報不足のため判断できません」と返す

【ユーザーの質問】
{query}

【参照理由文（重み付き）】
{chr(10).join([f"[重み:{r['score']}] {r['reason']}" for r in weighted_refs]) if weighted_refs else "（該当なし）"}
"""

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.2
    )

    answer = response.choices[0].message.content

    save_reason_to_db(answer)

    return {
        "answer": answer,
        "references": weighted_refs
    }








