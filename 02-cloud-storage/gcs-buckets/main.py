"""FastAPI 上傳閘道呼叫進入點。"""

from __future__ import annotations

import logging

from fastapi import FastAPI, File, HTTPException, Query, UploadFile
from fastapi.staticfiles import StaticFiles

from config import GcsConfig, STATIC_DIR
from storage_service import GcsStorageService

logging.basicConfig(level=logging.INFO, format="%(asctime)s | %(levelname)-8s | %(message)s")

app = FastAPI(title="GCS Upload Gateway", version="1.0.0")
if STATIC_DIR.exists():
    app.mount("/static", StaticFiles(directory=str(STATIC_DIR)), name="static")


def _get_storage_service() -> GcsStorageService:
    """於請求邊界載入設定並建立儲存服務，設定異常時回傳明確錯誤。"""
    try:
        return GcsStorageService(GcsConfig.from_env())
    except ValueError as exc:
        raise HTTPException(status_code=500, detail=str(exc)) from exc


@app.post("/upload")
async def upload_file(
    target_dir: str = Query(..., alias="dir", description="目標 Bucket 內的子目錄前綴"),
    file: UploadFile = File(...),
) -> dict[str, str]:
    """接收上傳檔案並轉存至 Google Cloud Storage。"""
    if not file.filename:
        raise HTTPException(status_code=400, detail="上傳檔案缺少有效檔名")

    service = _get_storage_service()
    uri = service.upload_stream(file.file, target_dir=target_dir, filename=file.filename)
    return {"message": "檔案上傳成功", "uri": uri}


if __name__ == "__main__":
    import uvicorn

    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
