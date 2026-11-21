"""輕量單檔 CLI 工具：從 Google Cloud Storage 下載指定檔案。"""

from __future__ import annotations

import argparse
import logging
from pathlib import Path

from google.cloud import storage

logging.basicConfig(level=logging.INFO, format="%(asctime)s | %(levelname)-8s | %(message)s")
logger = logging.getLogger(__name__)


def download_blob(bucket_name: str, source_blob_name: str, destination_path: Path) -> None:
    """下載單一 GCS 物件至指定本機路徑。"""
    destination_path.parent.mkdir(parents=True, exist_ok=True)
    client = storage.Client()
    blob = client.bucket(bucket_name).blob(source_blob_name)
    blob.download_to_filename(str(destination_path))
    logger.info("已下載 gs://%s/%s -> %s", bucket_name, source_blob_name, destination_path)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="從 Google Cloud Storage 下載單一檔案")
    parser.add_argument("--bucket", required=True, help="GCS Bucket 名稱")
    parser.add_argument("--source", required=True, help="Bucket 內的來源物件路徑")
    parser.add_argument("--dest", required=True, type=Path, help="本機儲存路徑")
    return parser.parse_args()


if __name__ == "__main__":
    args = parse_args()
    download_blob(args.bucket, args.source, args.dest)
