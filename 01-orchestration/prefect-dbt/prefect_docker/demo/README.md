# dbt FHIR 轉 OMOP 拆分實驗說明

## 1. 基本說明

由 FHIR 轉 OMOP 的資料拆分練習：先將 `p_origin` 的 `data` 欄位（FHIR JSON）拆分成 `row_data`，接著用 `base_table_macros` 拆成不同類別的總表（`models/sources`），再由 OMOP 表（`models/staging`）建構目標表。
- **優點**：全拆分設計在有新欄位重跑時會自動帶入。
- **缺點**：可能發生 OMOP 有該欄位但 FHIR 沒有，進而帶入錯誤。
- 此篇 OMOP 表僅完成部分欄位，主要作為拆分方法之技術參考。

## 2. 基本資料表（`vars` 設定）

- `myrow_data: 'row_data'`：`row_data` 拆分表，將 JSON 拆成碎片化結構使用。
- `myschema: 'dbt'`：目標 Schema 名稱。
- `myorigin: 'p_origin'`：最基本的原始表，由 Bucket 直接把資料灌入，僅含兩個欄位：`data (jsonb)` 放整個 JSON 檔、`insert_date (date)` 記錄寫入日期。

## 3. 補充文件

可參考 [文書使用說明](./read_file/文書使用說明.md) 與 [edr 說明](./read_file/edr說明.md) 中的兩種外掛設定：
- `elementary`
- `dbt_artifacts`

---

## 4. 正式使用方式

```bash
dbt run
dbt test
```
