"""GCS 上傳閘道參數設定模組。"""

from __future__ import annotations

import os
from dataclasses import dataclass
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
STATIC_DIR = BASE_DIR / "static"
DEFAULT_UPLOAD_TIMEOUT_SECONDS = 60


@dataclass(frozen=True)
class GcsConfig:
    """不可變 Google Cloud Storage 連線設定。"""

    bucket_name: str
    credentials_path: Path | None = None

    @classmethod
    def from_env(cls) -> "GcsConfig":
        """由環境變數載入 GCS 設定，缺少 Bucket 名稱時立即失敗。"""
        bucket_name = os.getenv("GCS_BUCKET_NAME", "").strip()
        if not bucket_name:
            raise ValueError("缺少必要環境變數：GCS_BUCKET_NAME")

        raw_cred = os.getenv("GOOGLE_APPLICATION_CREDENTIALS", "").strip()
        return cls(
            bucket_name=bucket_name,
            credentials_path=Path(raw_cred) if raw_cred else None,
        )
