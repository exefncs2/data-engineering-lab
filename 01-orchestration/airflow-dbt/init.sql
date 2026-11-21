CREATE DATABASE airflow;

CREATE ROLE airflow_role;

-- 授予角色 "airflow_role" 超級使用者權限（最大權限）
ALTER ROLE airflow_role SUPERUSER;

-- 授予角色 "airflow_role" 建立資料庫的權限
ALTER ROLE airflow_role CREATEDB;

-- 授予角色 "airflow_role" 連接到資料庫的權限
ALTER ROLE airflow_role CONNECTION LIMIT -1;

-- 建立一個使用者 "airflow" 並設置密碼，並分配給角色 "airflow_role"
CREATE USER airflow WITH PASSWORD 'airflow';
GRANT airflow_role TO airflow;

