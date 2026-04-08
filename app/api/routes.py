from fastapi import APIRouter, Request
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse

router = APIRouter()

# templates フォルダを指定
templates = Jinja2Templates(directory="app/templates")

# -------------------------------
# ルート：トップページ（index.html）
# -------------------------------
@router.get("/", response_class=HTMLResponse)
async def serve_index(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})



