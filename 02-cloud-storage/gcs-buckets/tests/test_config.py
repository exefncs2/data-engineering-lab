"""GCS 設定載入與 Fail Fast 驗證單元測試。"""

import os
import unittest
from pathlib import Path
from unittest.mock import patch

from config import GcsConfig


class TestGcsConfig(unittest.TestCase):
    """驗證 GcsConfig 環境變數檢核規則。"""

    def test_missing_bucket_name_raises_value_error(self) -> None:
        with patch.dict(os.environ, {}, clear=True):
            with self.assertRaises(ValueError):
                GcsConfig.from_env()

    def test_valid_env_loads_config(self) -> None:
        env = {
            "GCS_BUCKET_NAME": "demo-bucket",
            "GOOGLE_APPLICATION_CREDENTIALS": "/tmp/key.json",
        }
        with patch.dict(os.environ, env, clear=True):
            cfg = GcsConfig.from_env()
            self.assertEqual(cfg.bucket_name, "demo-bucket")
            self.assertEqual(cfg.credentials_path, Path("/tmp/key.json"))


if __name__ == "__main__":
    unittest.main()
