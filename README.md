# 📘 原価差異ナレッジAI（Cost Variance Explainer）

製造業の **原価差異の原因説明文を AI が自動生成**するツールです。

Word / Excel / PDF / PPT / TXT / フォルダ をドラッグ＆ドロップするだけで、
資料の内容を読み取り、RAG（過去理由文検索）＋ LLM により
**最も妥当な原因説明文を生成**します。

---

## 🚀 特徴

- 📁 **複数ファイルの一括取り込み（フォルダ対応）**
- 🔍 **FAISS ベースの RAG（過去理由文検索）**
- 🤖 **OpenAI GPT-4o-mini による理由文生成**
- 📊 **根拠のハイライト表示**
- 📝 **理由文の自動要約・品質スコアリング（拡張可能）**
- 📦 **SQLite + ベクトルストアによる自己学習**
- 🖥 **ブラウザで動く直感的な UI（FastAPI + Jinja2）**
- 🟦 **Windows 1クリック起動（start_app.bat 同梱）**

---

## 🧩 技術スタック

- **FastAPI**
- **OpenAI API**
- **FAISS（vector search）**
- **SentenceTransformer（MiniLM）**
- **SQLite**
- **Jinja2 Templates**
- **JavaScript / HTML / CSS**

---

## 📁 ディレクトリ構成



app/
├─ main.py
├─ api/
├─ services/
├─ database/
├─ vector_store/
├─ templates/
└─ static/

scripts/
requirements.txt
README.md
start_app.bat

---

## 🛠 セットアップ

🔑 **OpenAI APIキーについて**  
本ツールを利用するには OpenAI APIキーが必要です。  
各自で取得し、環境変数 **OPENAI_API_KEY** に設定してください。

Windows:
setx OPENAI_API_KEY "sk-xxxx"


Mac / Linux:
export OPENAI_API_KEY="sk-xxxx"


※ APIキーは絶対に公開しないでください。  
※ 本リポジトリには APIキーは含まれていません。

---

## 🟦 1クリック起動（Windows）

本リポジトリには **start_app.bat** を同梱しています。  
このファイルをダブルクリックするだけで、以下が自動で実行されます。

- 仮想環境（venv）の有効化  
- FastAPI サーバーの起動  
- 5秒待機（サーバー起動の安定化）  
- ブラウザで `http://localhost:8000` を自動オープン  

初心者でも迷わず起動できるように設計されています。

---

### 1. ライブラリのインストール
pip install -r requirements.txt


### 2. サーバー起動
uvicorn app.main:app --reload


### 3. ブラウザでアクセス
http://localhost:8000


---

## 🧪 主な API エンドポイント

| エンドポイント | 説明 |
|---------------|------|
| /analyze | 資料を解析し、AI が総評を生成 |
| /generate | 原価差異の理由文を生成 |
| /upload_files | ファイル取り込み（フォルダ対応） |
| /edit | 理由文の編集画面 |

---

## 🔐 セキュリティ

以下は `.gitignore` により GitHub にアップロードされません：

- data/（DB・ベクトルデータ）
- uploaded/（ユーザーアップロード）
- venv/
- __pycache__/
- *.db
- *.pyc
- app/vector_store/*.faiss
- app/vector_store/*.pkl

---

## 📄 ライセンス

MIT License

---

## ✨ 作者

thks-ai  
AI × 原価管理の効率化を推進するエンジニア






