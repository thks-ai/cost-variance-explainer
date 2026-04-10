from fastapi import FastAPI, UploadFile, File, Form
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi import Request
import tempfile
import os

from openai import OpenAI
client = OpenAI()

app = FastAPI()

templates = Jinja2Templates(directory="templates")
templates.env.cache = {}

# -------------------------
# ルート（UI表示）
# -------------------------
@app.get("/", response_class=HTMLResponse)
async def index(request: Request):
    return templates.TemplateResponse(
        name="index.html",
        context={"request": request},
        request=request
    )

# -------------------------
# 単一ファイルアップロード（テキストのみ）
# -------------------------
@app.post("/upload_files")
async def upload_files(file: UploadFile = File(...)):
    # 一時ファイルとして保存
    with tempfile.NamedTemporaryFile(delete=False) as tmp:
        tmp.write(await file.read())
        tmp_path = tmp.name

    # テキストとして読み取る（無料版仕様）
    try:
        with open(tmp_path, "rb") as f:
            content = f.read().decode("utf-8", errors="ignore")
    except:
        content = "（このファイル形式は簡易読み取りに対応していません）"

    os.remove(tmp_path)

    return {"content": content}

# -------------------------
# 理由文生成（1パターン）
# -------------------------
@app.post("/generate")
async def generate_reason(content: str = Form(...)):
    prompt = f"""
あなたは製造業の原価差異分析の専門家です。
以下の資料内容を読み取り、簡易的な原価差異の理由文を1つだけ生成してください。

資料内容:
{content}

出力形式:
- 原価差異の理由文（短め）
"""

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": prompt}],
        max_tokens=300,
    )

    result = response.choices[0].message.content
    return {"result": result}






















