CREATE DATABASE prefect;

CREATE ROLE prefect_role;

-- 授予角色 "prefect_role" 超級使用者權限（最大權限）
ALTER ROLE prefect_role SUPERUSER;

-- 授予角色 "prefect_role" 建立資料庫的權限
ALTER ROLE prefect_role CREATEDB;

-- 授予角色 "prefect_role" 連接到資料庫的權限
ALTER ROLE prefect_role CONNECTION LIMIT -1;

-- 建立一個使用者 "prefect" 並設置密碼，並分配給角色 "prefect_role"
CREATE USER prefect WITH PASSWORD 'prefect';
GRANT prefect_role TO prefect;

