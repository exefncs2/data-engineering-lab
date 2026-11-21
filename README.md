# Data Engineering & Modern Data Stack Lab（資料工程學習與實作報告）

> 本 Repo 整理自我在工作與自學過程中可公開的資料工程實驗、POC 程式碼與技術調研筆記，定位為**個人學習報告與實作紀錄庫**。

## 1. 版本與整理歷程

- **2023/10/02（v1.0.1）**：從工作實驗移植並刪去不需要的部分，遮蔽所有敏感資訊（帳號、密碼、IP、資料庫名稱等）。
- **2024/03/28**：新增 `airflow-dbt`（原 `airflow_docker`）的 dbt + Elementary 實作範例，並排除敏感設定與清理部分文字。
- **2026/11（結構與規範統一）**：完成當初列在「待處理」的幾項整理——依資料工程階段重整英文目錄結構、清除 `node_modules` 與壞掉的舊空指標、移除編輯器暫存檔、統一純繁體中文與套件安全版本，並補齊 GCS 模組的三檔分離與測試。

---

## 2. 學習主題與架構整理心得

整份學習紀錄依照現代資料工程（Modern Data Stack）的常見環節分成四大區塊：

### (1) 排程編排與資料轉換比較（`01-orchestration/`）
為了搞清楚實務上不同排程器跟 dbt 整合起來的體感差異，分別實作了三個環境：
- **Airflow + dbt + Elementary（`airflow-dbt` / `airflow-basics`）**：企業最普及、Operator 生態最完整，搭配 Elementary Data 可以直接產出資料品質報表；缺點是本機容器啟動與設定相對較重。
- **Prefect + dbt（`prefect-dbt`）**：寫法最貼近原生 Python 函式，開發體驗輕快，部署結構比 Airflow 單純。
- **Dagster（`dagster`）**：以資料資產（Asset）而非單純任務順序為核心，思考資料血緣與單元測試時最直覺。

### (2) 雲端儲存與 API 閘道實驗（`02-cloud-storage/gcs-buckets/`）
驗證在 GCP（搭配 PVC／內部網路）環境下，如何透過 FastAPI 建立二進位檔案上傳閘道寫入 Google Cloud Storage，並搭配獨立的上傳／下載 CLI 小工具。整理時將上傳閘道改為「參數（`config.py`）／核心（`storage_service.py`）／進入點（`main.py`）」三檔分離，而單純的 `upload_file.py` 與 `get_file.py` 維持單檔工具。

### (3) AI 檢索與向量資料庫實驗（`03-ai-rag/`）
- **`rag-chain/`**：練習把資料庫連線、GCP Secret Manager、OpenAI Embeddings 與文字切塊拆成標準 Python 套件結構。
- **`vector-db/`**：實驗 Pinecone 的稠密向量（Dense）與稀疏向量（Sparse）混合檢索公式（`alpha * dense + (1 - alpha) * sparse`）與基本 CRUD 操作。

### (4) 查詢引擎與架構調研報告（`docs/`）
整理在評估分散式查詢引擎與資料倉儲時的比較與實測筆記：
- **查詢引擎比較**：[Trino vs. Presto 比較](docs/architecture-research/trino-vs-presto.md) · [Trino 安裝](docs/architecture-research/trino-installation.md) · [Presto 安裝](docs/architecture-research/presto-installation.md)
- **雲端資料倉儲**：[Presto 連接 BigQuery](docs/architecture-research/presto-bigquery-connector.md) · [Presto 查詢筆記](docs/architecture-research/presto-query-guide.md) · [Redshift 實測結果](docs/architecture-research/redshift-benchmark.md) · [SQL 資料庫選型](docs/architecture-research/sql-database-selection.md)
- **LLM 與前端筆記**：[LangChain 筆記](docs/architecture-research/langchain-notes.md) · [RAG 系統架構](docs/architecture-research/rag-architecture.md) · [Vue 3 + Axios 筆記](docs/architecture-research/vue3-axios-notes.md)
- **系統構想文件**：[OrbitCommune 架構構想（中文）](docs/system-proposals/orbit-commune-zh.md) · [OrbitCommune Proposal（EN）](docs/system-proposals/orbit-commune-en.md)

---

## 3. 目錄總覽

```text
data-engineering-lab/
├── 01-orchestration/
│   ├── airflow-dbt/          # Airflow + dbt + Elementary + BigQuery Docker Compose 實例
│   ├── airflow-basics/       # Airflow 基礎安裝與操作筆記
│   ├── dagster/              # Dagster Asset 編排、排程與測試範例
│   └── prefect-dbt/          # Prefect + dbt Docker Compose 整合範本
├── 02-cloud-storage/
│   └── gcs-buckets/          # FastAPI GCS 上傳閘道（三檔分離）與單檔 CLI 工具
├── 03-ai-rag/
│   ├── rag-chain/            # LangChain RAG 套件化結構實驗
│   └── vector-db/            # Pinecone Dense + Sparse 混合檢索實驗
└── docs/
    ├── architecture-research/ # 查詢引擎、資料倉儲、RAG 與前端研究筆記
    └── system-proposals/      # 系統架構構想文件
```

---

## 4. 正式使用方式

本 Repo 內各子專案互相獨立，請進入想執行的子目錄並依該目錄內的 README 與 `.env.example` 設定環境變數後啟動：

```bash
# 範例 1：啟動 Airflow + dbt 容器環境
cd 01-orchestration/airflow-dbt
docker compose up -d

# 範例 2：啟動 Prefect + dbt 容器環境
cd 01-orchestration/prefect-dbt/prefect_docker
docker compose up -d

# 範例 3：啟動 GCS 上傳閘道（先設定 GCS_BUCKET_NAME 與金鑰環境變數）
cd 02-cloud-storage/gcs-buckets
cp .env.example .env
python main.py

# 執行 GCS 設定單元測試
python -m unittest discover -s tests -v
```

> **安全提醒**：所有範例皆已遮蔽原本的帳號、密碼、IP 與正式專案名稱，執行前請自行填入對應的本機或測試環境參數。
