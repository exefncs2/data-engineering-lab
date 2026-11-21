# Data Engineering & Modern Data Stack Lab（個人實驗與調研筆記庫）

> 本 Repo 整理自我在工作與自學過程留下的可公開實驗程式與研究文件，屬於**零散主題的學習報告與實作紀錄集合**，並非單一整合產品。

## 1. 版本與整理紀錄

- **2023/10/02（v1.0.1）**：由既有工作實驗移植並刪除不需公開的部分，遮蔽帳號、密碼、IP、資料庫名稱等專用值。
- **2024/03/28**：加入 `airflow-dbt`（原 `airflow_docker`）的 dbt 實例並遮蔽敏感設定與清理部分文字。
- **2026/11**：完成原本列在「待處理」的目錄與檔案整理——將根目錄散落的中英文資料夾重新歸類、移除誤推的 `node_modules`、壞掉的空 `vue3/origin` 指標與編輯器暫存檔、統一純繁體中文與套件安全版本，並補齊 `gcs-buckets` 三檔整理與測試。

---

## 2. 各資料夾實際收錄內容（對照檔案）

### (1) 排程與 dbt 實作紀錄（`01-orchestration/`）
各自獨立的小型容器與腳本實驗，記錄不同工具的實際設定與寫法：
- **`airflow-dbt/`**：內含 `docker-compose.yml`、7 支 Airflow DAG（`bigquery_to_db.py`、`gcp_to_db.py`、`dbt_exec.py`、`dbt_update.py`、`once_dag.py` 等）、兩個 dbt 專案目錄（`imgenie-dbt`、`imgenie-dbt-update`，含 Elementary 產出報表範例），以及總體說明 `README.md` 與 `api說明.md`。
- **`airflow-basics/`**：Airflow Docker 基礎安裝檔（`airflow.cfg`、`start.sh`）與介面操作截圖說明（`README.md`）。
- **`dagster/`**：簡單的 Dagster 練習專案，包含 `assets.py`、`schedules.py`、`mydag.py`、呼叫外部 HTTP API 的 `api_link.py` 與 `test_assets.py`。
- **`prefect-dbt/`**：Prefect + dbt 容器設定檔，內含從 GCS 讀取 JSON 寫入資料庫（`bucket_to_db.py`）、觸發 dbt CLI（`dbt_cil.py`）與註冊排程（`main.py`）的範例腳本。

### (2) GCP Bucket 上傳／下載範例（`02-cloud-storage/gcs-buckets/`）
- 在 GCP 環境下用 FastAPI 開一個 `/upload` 端點把檔案寫進 GCS（整理成 `config.py`、`storage_service.py`、`main.py` 三檔）。
- 附兩個獨立單檔 CLI 工具：`upload_file.py`（用二進位呼叫 `/upload`）與 `get_file.py`（直接用 GCP 預設認證下載物件）。

### (3) RAG 與向量資料庫實驗（`03-ai-rag/`）
- **`rag-chain/`**：練習將資料庫連線（SQLAlchemy）、GCP Secret Manager、OpenAI Embeddings 與文字切塊拆成標準 Python 套件目錄結構，並附一份簡易 FastAPI 測試端點（`test_api/`）。
- **`vector-db/demo.py`**：單檔腳本，用來測試 Pinecone 的稠密＋稀疏向量加權公式（`alpha * dense + (1 - alpha) * sparse`）與隨機向量 Upsert / Query / Update / Delete 操作。

### (4) 個人研究與操作筆記（`docs/`）
- **查詢引擎與資料庫筆記**：[Trino vs. Presto 比較](docs/architecture-research/trino-vs-presto.md) · [Trino 安裝](docs/architecture-research/trino-installation.md) · [Presto 安裝](docs/architecture-research/presto-installation.md) · [Presto 連接 BigQuery](docs/architecture-research/presto-bigquery-connector.md) · [Presto 查詢使用](docs/architecture-research/presto-query-guide.md) · [Redshift 測試結果](docs/architecture-research/redshift-benchmark.md) · [SQL 資料庫選型](docs/architecture-research/sql-database-selection.md)
- **LLM 與前端筆記**：[LangChain 筆記](docs/architecture-research/langchain-notes.md) · [RAG 系統架構](docs/architecture-research/rag-architecture.md) · [Vue 3 + Axios 筆記](docs/architecture-research/vue3-axios-notes.md)
- **系統構想筆記**：[OrbitCommune（中文）](docs/system-proposals/orbit-commune-zh.md) · [OrbitCommune（EN）](docs/system-proposals/orbit-commune-en.md)

---

## 3. 目錄總覽

```text
data-engineering-lab/
├── 01-orchestration/
│   ├── airflow-dbt/
│   ├── airflow-basics/
│   ├── dagster/
│   └── prefect-dbt/
├── 02-cloud-storage/
│   └── gcs-buckets/
├── 03-ai-rag/
│   ├── rag-chain/
│   └── vector-db/
└── docs/
    ├── architecture-research/
    └── system-proposals/
```

---

## 4. 正式使用方式

各子資料夾皆獨立運作，請依要測試的模組進入對應目錄並參照裡面的說明檔與 `.env.example` 設定後執行：

```bash
# 啟動 Airflow + dbt 容器範例
cd 01-orchestration/airflow-dbt
docker compose up -d

# 啟動 Prefect + dbt 容器範例
cd 01-orchestration/prefect-dbt/prefect_docker
docker compose up -d

# 啟動 GCS 上傳閘道與設定單元測試
cd 02-cloud-storage/gcs-buckets
cp .env.example .env
python main.py
python -m unittest discover -s tests -v
```
