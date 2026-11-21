# Data Engineering & Modern Data Stack Lab

![Python](https://img.shields.io/badge/Python-3.10%2B-3776AB?logo=python&logoColor=white)
![Airflow](https://img.shields.io/badge/Apache%20Airflow-Orchestration-017CEE?logo=apacheairflow&logoColor=white)
![dbt](https://img.shields.io/badge/dbt-Transformation-FF694B?logo=dbt&logoColor=white)
![Docker](https://img.shields.io/badge/Docker-Compose-2496ED?logo=docker&logoColor=white)
![BigQuery](https://img.shields.io/badge/Google-BigQuery-4285F4?logo=googlebigquery&logoColor=white)

現代資料工程（Modern Data Stack）與 AI 檢索架構的實作實驗室。收錄從零建立至容器化的資料管線排程編排、dbt 資料轉換與品質監控、雲端儲存閘道、RAG／向量資料庫實驗，以及分散式 SQL 查詢引擎研究等筆記。

## 專案架構總覽

```text
data-engineering-lab/
├── 01-orchestration/
│   ├── airflow-dbt/          # Airflow + dbt + Elementary Data + BigQuery Docker Compose 完整架構
│   ├── airflow-basics/       # Airflow 基礎安裝與介面操作筆記
│   ├── dagster/              # Dagster Asset 編排、Schedules 與測試範例
│   └── prefect-dbt/          # Prefect + dbt Docker Compose 整合範本
├── 02-cloud-storage/
│   └── gcs-buckets/          # FastAPI GCS 上傳閘道（三檔分離）與 CLI 下載／上傳小工具
├── 03-ai-rag/
│   ├── rag-chain/            # LangChain RAG 套件化實驗（含 DB / GCP Secret / OpenAI Embedding）
│   └── vector-db/            # Pinecone Dense + Sparse Hybrid Search 實驗
└── docs/
    ├── architecture-research/ # Trino / Presto / BigQuery / Redshift / SQL 選型 / RAG / Vue 3 技術筆記
    └── system-proposals/      # OrbitCommune 系統架構構想（中／英）
```

## 重點模組與文件索引

### 1. 資料管線編排與轉換（`01-orchestration/`）
- [**Airflow + dbt + Elementary (`airflow-dbt`)**](01-orchestration/airflow-dbt/)：包含 `bigquery_to_db`、`gcp_to_db`、`dbt_exec` DAGs、Docker Compose 部署與 Elementary 資料品質報表。
- [**Dagster (`dagster`)**](01-orchestration/dagster/)：以 Software-Defined Assets 實作的排程與測試專案。
- [**Prefect + dbt (`prefect-dbt`)**](01-orchestration/prefect-dbt/)：Prefect 容器化部署與 dbt 模型串接。

### 2. 雲端儲存與 AI 檢索實驗（`02-cloud-storage/`、`03-ai-rag/`）
- [**GCS Upload Gateway (`gcs-buckets`)**](02-cloud-storage/gcs-buckets/)：基於 FastAPI 的 Google Cloud Storage 上傳 API（`config.py` / `storage_service.py` / `main.py`）與單檔 CLI 工具。
- [**RAG Chain (`rag-chain`)**](03-ai-rag/rag-chain/)：模組化 LangChain RAG 套件結構（核心設定、DB 操作、GCP Secret Manager、OpenAI Embeddings）。
- [**Pinecone Hybrid Search (`vector-db`)**](03-ai-rag/vector-db/)：Dense + Sparse 混合向量加權檢索與 CRUD 範例。

### 3. 架構研究文件（`docs/architecture-research/`）
| 主題 | 文件 |
| :--- | :--- |
| **查詢引擎比較** | [Trino vs. Presto 比較表](docs/architecture-research/trino-vs-presto.md) · [Trino 安裝](docs/architecture-research/trino-installation.md) · [Presto 安裝](docs/architecture-research/presto-installation.md) |
| **雲端資料倉儲** | [Presto 連接 BigQuery](docs/architecture-research/presto-bigquery-connector.md) · [Presto 查詢使用](docs/architecture-research/presto-query-guide.md) · [Redshift 測試結果](docs/architecture-research/redshift-benchmark.md) · [SQL 資料庫選型](docs/architecture-research/sql-database-selection.md) |
| **LLM 與前端筆記** | [LangChain 筆記](docs/architecture-research/langchain-notes.md) · [RAG 系統架構](docs/architecture-research/rag-architecture.md) · [Vue 3 + Axios 筆記](docs/architecture-research/vue3-axios-notes.md) |

## 安全與隱私聲明
所有實驗程式皆已移除帳號、密碼、IP 與正式環境連線資訊，請依各模組的 `.env.example` 或 README 指示注入環境變數後使用。
