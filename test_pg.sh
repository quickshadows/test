#!/bin/bash

# Настройки подключения
PGSQL_HOST=$1
PGSQL_PORT=5432
PGSQL_USER="gen_user"
PGSQL_PASSWORD='joaFWafw*1111122'
PGSQL_DB="default_db"

# Параметры теста
TABLES=10
TABLE_SIZE=100000
THREADS=10   
DURATION=300
SCRIPT="/usr/share/sysbench/oltp_read_write.lua"

OUTPUT_FILE="susbanch_$PGSQL_HOST.txt"

# Подготовка
echo $PGSQL_HOST
echo "🔧 Подготовка данных..."
sysbench --db-driver=pgsql $SCRIPT \
  --pgsql-host=$PGSQL_HOST \
  --pgsql-port=$PGSQL_PORT \
  --pgsql-user=$PGSQL_USER \
  --pgsql-password=$PGSQL_PASSWORD \
  --pgsql-db=$PGSQL_DB \
  --tables=$TABLES \
  --table-size=$TABLE_SIZE \
  --threads=$THREADS \
  prepare

# Запуск теста
echo "🚀 Запуск теста..."
sysbench --db-driver=pgsql $SCRIPT \
  --pgsql-host=$PGSQL_HOST \
  --pgsql-port=$PGSQL_PORT \
  --pgsql-user=$PGSQL_USER \
  --pgsql-password=$PGSQL_PASSWORD \
  --pgsql-db=$PGSQL_DB \
  --tables=$TABLES \
  --table-size=$TABLE_SIZE \
  --threads=$THREADS \
  --time=$DURATION \
  run | tee $OUTPUT_FILE

# Очистка
echo "🧹 Очистка данных..."
sysbench --db-driver=pgsql $SCRIPT \
  --pgsql-host=$PGSQL_HOST \
  --pgsql-port=$PGSQL_PORT \
  --pgsql-user=$PGSQL_USER \
  --pgsql-password=$PGSQL_PASSWORD \
  --pgsql-db=$PGSQL_DB \
  --tables=$TABLES \
  --table-size=$TABLE_SIZE \
  --threads=$THREADS \
  cleanup

echo "✅ Готово!"
