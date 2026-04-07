# cost-variance-explainer
原価差異が発生した際の「原因説明文」をAIで自動生成するツールです。  
Excel・PDF・Word・PowerPoint などの資料を読み取り、RAG（検索拡張生成）を用いて、  
根拠に基づいた自然な説明文を自動生成します。

---

## 🚀 主な機能
- 原価差異の原因説明文をAIが自動生成
- Excel / PDF / Word / PowerPoint からのテキスト抽出に対応
- 過去の原因データベースを用いた RAG 検索
- エビデンス付きの説明文生成（根拠ハイライト）
- Excel 形式でのレポート出力に対応
- 非エンジニアでも使える GUI（ドラッグ＆ドロップ対応）

---

## 🧠 技術構成
- Python / FastAPI
- OpenAI GPT-4o-mini（または highspeed）
- FAISS ベクトル検索
- LangChain（RAG 構築）
- PyMuPDF / python-docx / openpyxl などの抽出系ライブラリ

---

## 📁 ディレクトリ構成（例）

```

app/
├─ main.py
├─ rag/
├─ extractor/
├─ generator/
templates/
requirements.txt
README.md

```


---

## 📝 使い方
1. GUI 画面を起動  
2. 原価差異に関する資料（Excel / PDF / Word / PPT）をドラッグ＆ドロップ  
3. AI が内容を解析し、原因説明文を生成  
4. 必要に応じて編集し、Excel 形式で出力

---

## 📌 想定ユーザー
- 製造業の原価管理担当者  
- 経理・管理会計部門  
- 原価差異の説明文作成に時間がかかっている現場  
- レポート作成を効率化したい企業

---

## 📄 ライセンス
MIT License

