# GCS Upload Gateway & CLI Tools

基於 FastAPI 的 Google Cloud Storage 上傳閘道，採**三檔分離架構**，並附帶兩個獨立單檔 CLI 小工具。

## 檔案架構

```text
gcs-buckets/
├── config.py           # 參數設定檔：不可變 GcsConfig 與環境變數 Fail Fast 驗證
├── storage_service.py  # 核心邏輯檔：封裝 GCS 串流上傳與下載操作
├── main.py             # 呼叫進入點：FastAPI 上傳 API 路由
├── get_file.py         # 單檔 CLI 小工具：下載單一 GCS 物件
├── upload_file.py      # 單檔 CLI 小工具：呼叫上傳 API 傳送本機檔案
└── tests/              # 設定單元測試
```

## 快速開始

```bash
export GCS_BUCKET_NAME="your-bucket-name"
export GOOGLE_APPLICATION_CREDENTIALS="/path/to/service-account.json"

python main.py
```
