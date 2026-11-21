"""FastAPI upload gateway for Google Cloud Storage (GCS) buckets."""

from __future__ import annotations

import logging
import os
from pathlib import Path
from typing import BinaryIO

from fastapi import FastAPI, File, HTTPException, Query, UploadFile
from fastapi.staticfiles import StaticFiles
from google.cloud import storage

logging.basicConfig(level=logging.INFO, format="%(asctime)s | %(levelname)-8s | %(message)s")
logger = logging.getLogger("gcs_upload_gateway")

GOOGLE_CREDENTIALS_PATH = os.getenv("GOOGLE_APPLICATION_CREDENTIALS", "")
GCS_BUCKET_NAME = os.getenv("GCS_BUCKET_NAME", "")

app = FastAPI(title="GCS Upload Gateway", version="1.0.0")

static_dir = Path(__file__).resolve().parent / "static"
if static_dir.exists():
    app.mount("/static", StaticFiles(directory=str(static_dir)), name="static")


def get_storage_client() -> storage.Client:
    if GOOGLE_CREDENTIALS_PATH:
        return storage.Client.from_service_account_json(GOOGLE_CREDENTIALS_PATH)
    return storage.Client()


def upload_to_gcs(file_obj: BinaryIO, bucket_name: str, destination_blob_name: str) -> str:
    """Upload a file-like object to GCS and return the gs:// URI."""
    client = get_storage_client()
    bucket = client.bucket(bucket_name)
    blob = bucket.blob(destination_blob_name)
    blob.upload_from_file(file_obj)
    uri = f"gs://{bucket_name}/{destination_blob_name}"
    logger.info("Uploaded object to %s", uri)
    return uri


@app.post("/upload")
async def upload_file(
    target_dir: str = Query(..., alias="dir", description="Target prefix inside the GCS bucket"),
    file: UploadFile = File(...),
):
    if not GCS_BUCKET_NAME:
        raise HTTPException(status_code=500, detail="GCS_BUCKET_NAME environment variable is not set")

    prefix = target_dir.strip("/")
    blob_path = f"{prefix}/{file.filename}" if prefix else file.filename
    uri = upload_to_gcs(file.file, GCS_BUCKET_NAME, blob_path)
    return {"message": "File uploaded successfully.", "uri": uri}


if __name__ == "__main__":
    import uvicorn

    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
