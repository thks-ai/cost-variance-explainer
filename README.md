\# 📘 原価差異ナレッジAI（Cost Variance Explainer）



製造業の \*\*原価差異の原因説明文を AI が自動生成\*\*するツールです。  

Word / Excel / PDF / PPT / TXT / フォルダ をドラッグ＆ドロップするだけで、  

資料の内容を読み取り、RAG（過去理由文検索）＋ LLM により  

\*\*最も妥当な原因説明文を生成\*\*します。



\---



\## 🚀 特徴



\- 📁 \*\*複数ファイルの一括取り込み（フォルダ対応）\*\*

\- 🔍 \*\*FAISS ベースの RAG（過去理由文検索）\*\*

\- 🤖 \*\*OpenAI GPT-4o-mini による理由文生成\*\*

\- 📊 \*\*根拠のハイライト表示\*\*

\- 📝 \*\*理由文の自動要約・品質スコアリング（拡張可能）\*\*

\- 📦 \*\*SQLite + ベクトルストアによる自己学習\*\*

\- 🖥 \*\*ブラウザで動く直感的な UI（FastAPI + Jinja2）\*\*



\---



\## 🧩 技術スタック



\- \*\*FastAPI\*\*

\- \*\*OpenAI API\*\*

\- \*\*FAISS（vector search）\*\*

\- \*\*SentenceTransformer（MiniLM）\*\*

\- \*\*SQLite\*\*

\- \*\*Jinja2 Templates\*\*

\- \*\*JavaScript / HTML / CSS\*\*



\---



\## 📁 ディレクトリ構成



```
app/

├─ main.py

├─ api/

├─ services/

├─ database/

├─ vector\_store/

├─ templates/

└─ static/

scripts/

requirements.txt

README.md

```


\---



\## 🛠 セットアップ



\### 1. ライブラリのインストール

pip install -r requirements.txt



\### 2. サーバー起動

uvicorn app.main:app --reload



\### 3. ブラウザでアクセス

http://localhost:8000



\---



\## 🧪 主な API エンドポイント



| エンドポイント | 説明 |

|---------------|------|

| `/analyze` | 資料を解析し、AI が総評を生成 |

| `/generate` | 原価差異の理由文を生成 |

| `/upload\_files` | ファイル取り込み（フォルダ対応） |

| `/edit` | 理由文の編集画面 |



\---



\## 🔐 セキュリティ



以下は `.gitignore` により GitHub にアップロードされません：



\- `data/`（DB・ベクトルデータ）

\- `uploaded/`（ユーザーアップロード）

\- `venv/`

\- `\_\_pycache\_\_/`

\- `\*.db`

\- `\*.pyc`

\- `app/vector\_store/\*.faiss`

\- `app/vector\_store/\*.pkl`



\---



\## 📄 ライセンス



MIT License



\---



\## ✨ 作者



thks-ai 

AI × 原価管理の効率化を推進するエンジニア






