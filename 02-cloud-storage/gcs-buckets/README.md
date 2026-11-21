# GCS Upload Gateway & CLI Tools（Buckets 站點 API）

基於 FastAPI 的 Google Cloud Storage 上傳閘道，採**三檔分離架構**，並附帶兩個獨立單檔 CLI 小工具。

> **部署注意事項（原實驗筆記）**：此站點設計於 Google Cloud Platform（GCP）環境運行，建議搭配 VPC／內部網路並透過環境變數設定服務帳號金鑰；單純從 Bucket 下載（`get_file.py`）可直接使用 GCP 預設認證（ADC）。

## 檔案架構

```text
gcs-buckets/
├── config.py           # 參數設定檔：不可變 GcsConfig 與環境變數 Fail Fast 驗證
├── storage_service.py  # 核心邏輯檔：封裝 GCS 串流上傳與下載操作（物件路徑：{dir}/{filename}）
├── main.py             # 呼叫進入點：FastAPI /upload API 路由
├── get_file.py         # 單檔 CLI 小工具：透過 GCP 預設認證下載單一 GCS 物件
├── upload_file.py      # 單檔 CLI 小工具：以二進位（rb）模式呼叫 /upload API 上傳檔案
└── tests/              # 設定單元測試
```

## 快速開始

```bash
export GCS_BUCKET_NAME="your-bucket-name"
export GOOGLE_APPLICATION_CREDENTIALS="/path/to/service-account.json"

# 啟動上傳閘道
python main.py

# 使用 CLI 上傳與下載
python upload_file.py --file ./sample.csv --dir raw_data
python get_file.py --bucket your-bucket-name --source raw_data/sample.csv --dest ./downloaded.csv
```
