"""CLI client for uploading a local file to the FastAPI GCS Upload Gateway."""

from __future__ import annotations

import argparse
import logging
from pathlib import Path

import requests

logging.basicConfig(level=logging.INFO, format="%(asctime)s | %(levelname)-8s | %(message)s")
logger = logging.getLogger("gcs_upload_client")


def send_file(file_path: Path, target_dir: str, url: str = "http://127.0.0.1:8000/upload") -> None:
    if not file_path.is_file():
        raise FileNotFoundError(f"File not found: {file_path}")

    with file_path.open("rb") as fp:
        response = requests.post(url, files={"file": fp}, params={"dir": target_dir}, timeout=60)

    if response.ok:
        logger.info("Upload succeeded: %s", response.json())
    else:
        logger.error("Upload failed (HTTP %d): %s", response.status_code, response.text)
        response.raise_for_status()


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Upload a local file via the GCS Upload Gateway API")
    parser.add_argument("--file", required=True, type=Path, help="Local file to upload")
    parser.add_argument("--dir", required=True, help="Target directory prefix in GCS")
    parser.add_argument("--url", default="http://127.0.0.1:8000/upload", help="Gateway upload endpoint URL")
    return parser.parse_args()


if __name__ == "__main__":
    args = parse_args()
    send_file(args.file, args.dir, args.url)
