"""輕量單檔 CLI 工具：將本機檔案上傳至 FastAPI GCS 上傳閘道。"""

from __future__ import annotations

import argparse
import logging
from pathlib import Path

import requests

logging.basicConfig(level=logging.INFO, format="%(asctime)s | %(levelname)-8s | %(message)s")
logger = logging.getLogger(__name__)

DEFAULT_UPLOAD_URL = "http://127.0.0.1:8000/upload"
REQUEST_TIMEOUT_SECONDS = 60


def send_file(file_path: Path, target_dir: str, url: str = DEFAULT_UPLOAD_URL) -> None:
    """發送 multipart/form-data 請求上傳檔案。"""
    if not file_path.is_file():
        raise FileNotFoundError(f"找不到指定的本機檔案：{file_path}")

    with file_path.open("rb") as fp:
        response = requests.post(
            url,
            files={"file": fp},
            params={"dir": target_dir},
            timeout=REQUEST_TIMEOUT_SECONDS,
        )

    if not response.ok:
        logger.error("上傳失敗（HTTP %d）：%s", response.status_code, response.text)
        response.raise_for_status()

    logger.info("檔案上傳成功：%s", response.json())


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="透過 GCS 上傳閘道 API 上傳本機檔案")
    parser.add_argument("--file", required=True, type=Path, help="要上傳的本機檔案路徑")
    parser.add_argument("--dir", required=True, help="目標目錄前綴")
    parser.add_argument("--url", default=DEFAULT_UPLOAD_URL, help="上傳閘道端點網址")
    return parser.parse_args()


if __name__ == "__main__":
    args = parse_args()
    send_file(args.file, args.dir, args.url)
