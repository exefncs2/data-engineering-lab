#!/bin/bash
echo "-------------------------init--------------------------------"
# 定義工作目錄和初始化文件路徑
WORK_DIR=/opt/airflow/work
INIT_FILE=$WORK_DIR/.init

echo ! -f "$INIT_FILE"
if [ ! -f "$INIT_FILE" ]; then
    echo "-----------------Initialization steps start---------------" 
    cd /opt/airflow/work/imgenie-dbt
    
    pip3 install --upgrade pip 
    pip3 install -r requirements.txt 
    
    pip3 install airflow-dbt==0.4.0 # 次序必須最後面不然會有問題

    dbt clean
    dbt deps
    
    cd /opt/airflow/work/imgenie-dbt-bigquery
    
    dbt clean
    dbt deps

    echo "========================================initialize airflow========================================"
    cd /opt/airflow/


    # Initialize Airflow database
    airflow db init    

    echo "==================================== end init ======================================="
# 在操作完成後建立 .init 文件
     # 取得當前日期和時間
    current_datetime=$(date)
    
    # 取得啓動容器的使用者名稱
    container_user=$(whoami)
    
    # 記錄啓動時間、日期、記錄者和使用者到文件
    echo "Container started by $container_user on $current_datetime"
    
    echo "Container started by $container_user on $current_datetime" >> $INIT_FILE
else
    echo ".init file exists, skipping initialization steps"
fi

echo "-------------------start start.sh------------------------"
sh /opt/airflow/work/start.sh
