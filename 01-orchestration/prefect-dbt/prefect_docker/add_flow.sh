#!/bin/bash
cd /work
directory="logs"

if [ ! -d "$directory" ]; then
    mkdir -p "$directory"
    echo "目錄已建立：$directory"
else
    echo "目錄已存在：$directory"
fi

nohup python /work/prefect/main.py  > ./logs/main.log 2>&1 &

