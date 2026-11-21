"""CLI helper to download an object from a Google Cloud Storage bucket."""

from __future__ import annotations

import argparse
import logging

from google.cloud import storage

logging.basicConfig(level=logging.INFO, format="%(asctime)s | %(levelname)-8s | %(message)s")
logger = logging.getLogger("gcs_download")


def download_blob(bucket_name: str, source_blob_name: str, destination_file_name: str) -> None:
    """Download a single blob from GCS to a local path."""
    storage_client = storage.Client()
    bucket = storage_client.bucket(bucket_name)
    blob = bucket.blob(source_blob_name)
    blob.download_to_filename(destination_file_name)
    logger.info("Downloaded gs://%s/%s -> %s", bucket_name, source_blob_name, destination_file_name)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Download a file from Google Cloud Storage")
    parser.add_argument("--bucket", required=True, help="GCS bucket name")
    parser.add_argument("--source", required=True, help="Blob path inside the bucket")
    parser.add_argument("--dest", required=True, help="Local destination file path")
    return parser.parse_args()


if __name__ == "__main__":
    args = parse_args()
    download_blob(args.bucket, args.source, args.dest)
