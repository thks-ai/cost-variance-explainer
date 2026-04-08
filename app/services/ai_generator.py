from openai import OpenAI

client = OpenAI()

def generate_reason(query: str, references: list):
    """
    query: ユーザーが入力した内容（例：材料費が増加した理由を説明して）
    references: RAG 検索結果（list of dict）
    """

    # 参考文献をまとめる
    ref_text = "\n".join([f"- {r['text']}" for r in references])

    prompt = f"""
あなたは製造業の原価差異分析の専門家です。

以下の「参考理由文（過去データ）」を踏まえて、
ユーザーの質問に対して、簡潔で一貫性のある理由説明を作成してください。

【参考理由文】
{ref_text}

【ユーザーの質問】
{query}

【出力ルール】
- 文章は2〜3文でまとめる
- 専門用語は使いすぎない
- 過去データと矛盾しない内容にする
- 過去データが無い場合は一般的な理由を述べる
- 箇条書きは禁止
- 「です」「ます」調で書く
"""

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "user", "content": prompt}
        ]
    )

    return response.choices[0].message.content



