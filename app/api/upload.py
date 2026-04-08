from fastapi import APIRouter, UploadFile, File
import os
import shutil
from datetime import datetime

router = APIRouter()

UPLOAD_DIR = "uploaded"

# 保存先フォルダを作成
os.makedirs(UPLOAD_DIR, exist_ok=True)

@router.post("/upload")
async def upload_file(file: UploadFile = File(...)):
    """
    ドラッグ＆ドロップされたファイルを uploaded/ に保存する
    """
    # ファイル名衝突を避けるためにタイムスタンプ付与
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S_%f")
    safe_filename = f"{timestamp}_{file.filename}"

    save_path = os.path.join(UPLOAD_DIR, safe_filename)

    # 保存処理
    with open(save_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    return {
        "status": "ok",
        "filename": file.filename,
        "saved_as": safe_filename
    }
