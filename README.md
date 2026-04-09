# 📘 原価差異ナレッジAI（Cost Variance Explainer）【無料版】

製造業の **原価差異の原因説明文を AI が自動生成**する “無料版” です。

Word / Excel / PDF / PPT / TXT を **単一ファイルで** 読み取り、  
AI が簡易的な説明文を生成します。

※ この無料版は「体験版」です。  
※ 実務レベルの機能は有料版（BOOTH）に搭載しています。

---

## 🚀 無料版でできること

- 📄 **単一ファイルの読み込み（フォルダ不可）**
- 🤖 **簡易的な理由文生成（1パターン）**
- 📝 **コピーして使えるテキスト出力**
- 🖥 **ブラウザで動くシンプルな UI（FastAPI）**

---

## ⚠ 無料版の制限（有料版との違い）

無料版は「体験用」のため、以下の機能は含まれていません。

- ❌ **フォルダ一括取り込み**
- ❌ **RAG（過去理由文検索）**
- ❌ **根拠ハイライト表示**
- ❌ **自己学習（SQLite + ベクトルストア）**
- ❌ **複数パターン生成**
- ❌ **Excel / PDF 出力**
- ❌ **1クリック起動（start_app.bat）**

これらは **すべて有料版で利用可能** です。

---

## 🧩 技術スタック（無料版）

- FastAPI  
- OpenAI API  
- SentenceTransformer（MiniLM）  
- Jinja2 Templates  
- JavaScript / HTML / CSS  

※ RAG / FAISS / SQLite は無料版では使用しません。

---

## 📁 ディレクトリ構成（無料版）

```
app/
├─ main.py
├─ config.py
└─ __pycache__（あってOK）

templates/
├─ index.html

README.md
requirements.txt


```

---

## 🛠 セットアップ

### 🔑 OpenAI APIキーの設定

Windows:
setx OPENAI_API_KEY "sk-xxxx"


Mac / Linux:
export OPENAI_API_KEY="sk-xxxx"


---

## ▶ 起動方法

1. ライブラリのインストール
pip install -r requirements.txt


2. サーバー起動
uvicorn app.main:app --reload


3. ブラウザでアクセス
http://localhost:8000


---

## 🧪 主な API エンドポイント（無料版）

| エンドポイント | 説明 |
|---------------|------|
| /analyze | 単一ファイルを解析し、簡易説明文を生成 |
| /generate | 原価差異の理由文を生成（1パターン） |
| /upload_files | 単一ファイルのアップロード |

---

## 🔐 セキュリティ

以下は `.gitignore` により GitHub にアップロードされません：

- uploaded/（ユーザーアップロード）
- venv/
- __pycache__/
- *.db
- *.pyc

---

## 💼 有料版について（BOOTH）

無料版では体験できない以下の機能を搭載しています：

- 📁 **フォルダ一括取り込み**
- 🔍 **RAG（過去理由文検索）**
- 📊 **根拠ハイライト表示**
- 🧠 **自己学習（SQLite + ベクトルストア）**
- 🤖 **高品質生成（複数パターン）**
- 📄 **Excel / PDF 出力**
- 🟦 **1クリック起動（Windows）**

👉 **有料版はこちら（BOOTH）**  
※ リンクを貼る

---

## ✨ 作者

thks-ai  
AI × 原価管理の効率化を推進するエンジニア
