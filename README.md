# Data Engineering & Modern Data Stack Lab

這份 Repo 是我整理自己研究現代資料工程（Modern Data Stack）與相關工具時留下的**實作實驗與調研筆記集合**，涵蓋排程編排、dbt 資料轉換與品質監控、雲端儲存串接、RAG 實驗，以及多個分散式查詢引擎的比較紀錄。

## 1. 為什麼這樣整理這份 Repo

這些程式碼與筆記是不同時期為了驗證個別技術環節寫下來的 POC（概念驗證），原本全散在根目錄下、中英文夾雜。整理後依照資料工程的工作階段分成四塊，方便自己回頭翻找，也讓外部讀者能一眼看出每個子資料夾的目的：

- **`01-orchestration/`（排程與轉換比較）**：實際把 Airflow、Prefect、Dagster 三套排程器分別跑過一輪，並對接 dbt 與 Elementary Data 觀察資料品質報表。
  - **Airflow + dbt**：生態最完整、企業最常見，但本機容器啟動較重。
  - **Prefect + dbt**：對原生 Python 函式最友善，寫起來最輕快。
  - **Dagster**：從資料資產（Asset）與血緣角度切入，測試與依賴關係最直覺。
- **`02-cloud-storage/`（雲端儲存串接）**：驗證在 GCP 環境下以 FastAPI 建上傳閘道寫入 GCS Bucket，並搭配獨立的二進位上傳／下載 CLI 工具；閘道服務拆成三檔分離，兩個單純 CLI 工具則維持單檔避免過度設計。
- **`03-ai-rag/`（檢索與向量資料庫實驗）**：測試把 LangChain、GCP Secret Manager、PostgreSQL 與 OpenAI Embeddings 打包成套件結構，以及測試 Pinecone 的稠密＋稀疏混合加權檢索公式。
- **`docs/`（查詢引擎與架構筆記）**：比較 Trino vs. Presto、Presto 接 BigQuery、Redshift 實測數據與 SQL 資料庫選型心得。

---

## 2. 目前定位與使用提醒

- 本 Repo 的定位是**個人技術實驗室與筆記庫**，並非單一可一鍵啟動的完整產品；各子專案各自獨立，需進到對應資料夾依照其內部說明與 `.env.example` 啟動。
- 所有範例皆已移除原本的帳密、IP 與正式專案名稱，僅保留去識別化設定範本。

---

## 3. 目錄與文件索引

```text
data-engineering-lab/
├── 01-orchestration/
│   ├── airflow-dbt/          # Airflow + dbt + Elementary + BigQuery 容器整合
│   ├── airflow-basics/       # Airflow 基礎安裝與介面筆記
│   ├── dagster/              # Dagster Asset 編排、排程與測試範例
│   └── prefect-dbt/          # Prefect + dbt 容器整合範本
├── 02-cloud-storage/
│   └── gcs-buckets/          # FastAPI GCS 上傳閘道（config / storage_service / main）與 CLI 工具
├── 03-ai-rag/
│   ├── rag-chain/            # LangChain RAG 套件化結構實驗
│   └── vector-db/            # Pinecone Dense + Sparse 混合檢索腳本
└── docs/
    ├── architecture-research/ # Trino / Presto / BigQuery / Redshift / SQL 選型 / RAG / Vue 3 筆記
    └── system-proposals/      # OrbitCommune 系統架構構想（中／英）
```

### 研究筆記快速連結
- **查詢引擎與倉儲**：[Trino vs. Presto 比較](docs/architecture-research/trino-vs-presto.md) · [Trino 安裝](docs/architecture-research/trino-installation.md) · [Presto 安裝](docs/architecture-research/presto-installation.md) · [Presto 連接 BigQuery](docs/architecture-research/presto-bigquery-connector.md) · [Presto 查詢筆記](docs/architecture-research/presto-query-guide.md) · [Redshift 實測](docs/architecture-research/redshift-benchmark.md) · [SQL 資料庫選型](docs/architecture-research/sql-database-selection.md)
- **LLM 與前端筆記**：[LangChain 筆記](docs/architecture-research/langchain-notes.md) · [RAG 系統架構](docs/architecture-research/rag-architecture.md) · [Vue 3 + Axios 筆記](docs/architecture-research/vue3-axios-notes.md)
