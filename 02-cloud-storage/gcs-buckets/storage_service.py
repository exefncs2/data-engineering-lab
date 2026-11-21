"""GCS 核心儲存服務模組：封裝物件上傳與下載邏輯。"""

from __future__ import annotations

import logging
from pathlib import Path
from typing import BinaryIO

from google.cloud import storage

from config import GcsConfig

logger = logging.getLogger(__name__)


class GcsStorageService:
    """封裝 Google Cloud Storage 常用操作，支援設定注入以利測試。"""

    def __init__(self, config: GcsConfig) -> None:
        self._config = config
        self._client = self._build_client(config.credentials_path)

    @staticmethod
    def _build_client(credentials_path: Path | None) -> storage.Client:
        if credentials_path is not None:
            return storage.Client.from_service_account_json(str(credentials_path))
        return storage.Client()

    def upload_stream(self, file_obj: BinaryIO, target_dir: str, filename: str) -> str:
        """將串流物件上傳至指定前綴目錄並回傳 gs:// 路徑。"""
        prefix = target_dir.strip("/")
        blob_path = f"{prefix}/{filename}" if prefix else filename

        bucket = self._client.bucket(self._config.bucket_name)
        blob = bucket.blob(blob_path)
        blob.upload_from_file(file_obj)

        uri = f"gs://{self._config.bucket_name}/{blob_path}"
        logger.info("檔案上傳完成：%s", uri)
        return uri

    def download_file(self, source_blob_name: str, destination_path: Path) -> Path:
        """由 GCS 下載指定物件至本機路徑。"""
        destination_path.parent.mkdir(parents=True, exist_ok=True)
        bucket = self._client.bucket(self._config.bucket_name)
        blob = bucket.blob(source_blob_name)
        blob.download_to_filename(str(destination_path))
        logger.info("檔案下載完成：gs://%s/%s -> %s", self._config.bucket_name, source_blob_name, destination_path)
        return destination_path
