#!/bin/bash

# Настройки подключения
MYSQL_HOST=$1
MYSQL_PORT=3306
MYSQL_USER="gen_user"
MYSQL_PASSWORD='joaFWafw*1111122'
MYSQL_DB="default_db"

# Параметры теста
TABLES=10
TABLE_SIZE=10000
THREADS=10   
DURATION=300
SCRIPT="/usr/share/sysbench/oltp_read_write.lua"

OUTPUT_FILE="susbanch_$MYSQL_HOST.txt"

# Подготовка
echo $MYSQL_HOST
echo "🔧 Подготовка данных..."
sysbench $SCRIPT \
  --mysql-host=$MYSQL_HOST \
  --mysql-port=$MYSQL_PORT \
  --mysql-user=$MYSQL_USER \
  --mysql-password=$MYSQL_PASSWORD \
  --mysql-db=$MYSQL_DB \
  --tables=$TABLES \
  --table-size=$TABLE_SIZE \
  --threads=$THREADS \

  prepare

# Запуск теста
echo "🚀 Запуск теста..."
sysbench $SCRIPT \
  --mysql-host=$MYSQL_HOST \
  --mysql-port=$MYSQL_PORT \
  --mysql-user=$MYSQL_USER \
  --mysql-password=$MYSQL_PASSWORD \
  --mysql-db=$MYSQL_DB \
  --tables=$TABLES \
  --table-size=$TABLE_SIZE \
  --threads=$THREADS \
  --time=$DURATION \
  run | tee $OUTPUT_FILE

# Очистка
echo "🧹 Очистка данных..."
sysbench $SCRIPT \
  --mysql-host=$MYSQL_HOST \
  --mysql-port=$MYSQL_PORT \
  --mysql-user=$MYSQL_USER \
  --mysql-password=$MYSQL_PASSWORD \
  --mysql-db=$MYSQL_DB \
  --tables=$TABLES \
  --table-size=$TABLE_SIZE \
  --threads=$THREADS \
  cleanup

echo "✅ Готово!"
