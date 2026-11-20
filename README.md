# Data Engineering & Modern Data Stack Lab

整理自實務資料工程研究與 PoC 實驗的公開範本庫（所有帳號、密碼、IP 與內部連線資訊皆已去識別化），涵蓋資料管線排程、dbt 轉換與資料品質監控、雲端倉儲查詢引擎、以及 RAG／向量資料庫實驗。

## 模組總覽

| 目錄 | 主題 | 內容說明 |
| :--- | :--- | :--- |
| [`airflow_docker/`](airflow_docker/) | **Airflow + dbt + Elementary + BigQuery** | Docker Compose 完整架構，內含 `bigquery_to_db` / `gcp_to_db` / `dbt_exec` DAGs、dbt 專案與 Elementary Data 品質監控報表（EDR） |
| [`airflow/`](airflow/) | **Airflow 基礎操作筆記** | Airflow 安裝、介面操作截圖與使用說明 |
| [`dagster_server/`](dagster_server/) | **Dagster 編排伺服器** | Dagster 專案設定（`dagster.yaml`、schedules、單元測試與操作文件） |
| [`prefect_dbt_server/`](prefect_dbt_server/) | **Prefect + dbt 整合** | Prefect Docker Compose 部署與 dbt 排程整合實驗 |
| [`Buckets實驗/`](Buckets實驗/) | **Cloud Storage Buckets** | 物件儲存上傳／下載 Python 範例腳本與設定筆記 |
| [`chain_test/`](chain_test/) | **LangChain / RAG 測試** | `rag_chain` 套件化測試與 API 串接實驗 |
| [`向量資料庫實驗/`](向量資料庫實驗/) | **Vector Database** | 向量資料庫建置設定與 Python 檢索 Demo |
| [`其他研究文檔/`](其他研究文檔/) | **資料架構與查詢引擎研究** | Presto / Trino 比較與安裝、Presto 連接 BigQuery、Redshift 測試、SQL 資料庫選型、LangChain 與 RAG 架構筆記 |
| [`vue3/`](vue3/) | **Vue 3 前端展示** | 輕量級前端整合範例 |
| [`構思/`](構思/) | **系統構思文件** | OrbitCommune 中英文架構構思筆記 |

## 技術堆疊

- **Workflow Orchestration**: Apache Airflow, Dagster, Prefect
- **Data Transformation & Quality**: dbt, Elementary Data
- **Data Warehouse & Query Engines**: Google BigQuery, Trino, Presto, Amazon Redshift
- **AI / Retrieval**: LangChain, RAG, Vector Database
- **Infra & Frontend**: Docker Compose, Python, Vue 3

## 隱私與安全說明

本倉庫所有實務範例均已移除與遮蔽敏感資訊（帳號、密碼、IP、正式資料庫名稱與金鑰），僅保留可公開展示之架構、DAG 範本與技術文件。
