#!/usr/bin/env python3
import subprocess
import re
import pandas as pd
from datetime import datetime
from pathlib import Path

# ------------------ Параметры ------------------
MYSQL_HOST = input("IP или хост MySQL: ").strip()
MYSQL_PORT = 3306
MYSQL_USER = "gen_user"
MYSQL_PASSWORD = "Passwd123"
MYSQL_DB = "default_db"

TABLES = 10
TABLE_SIZE = 100000
THREADS = 10
DURATION = 300
SCRIPT = "/usr/share/sysbench/oltp_read_write.lua"

timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
txt_file = Path(f"sysbench_mysql{MYSQL_HOST}_{timestamp}.txt")
csv_file = Path(f"sysbench_mysql{MYSQL_HOST}_{timestamp}.csv")

# ------------------ Вспомогательная функция запуска ------------------
def run_sysbench(args, capture_output=True):
    """Запуск sysbench с аргументами, возврат stdout, stderr и returncode"""
    result = subprocess.run(
        ["sysbench"] + args,
        capture_output=capture_output,
        text=True
    )
    return result.stdout, result.stderr, result.returncode

# ------------------ Подготовка ------------------
print("🔧 Подготовка данных...")
stdout, stderr, rc = run_sysbench([
    SCRIPT,
    f"--mysql-host={MYSQL_HOST}",
    f"--mysql-port={MYSQL_PORT}",
    f"--mysql-user={MYSQL_USER}",
    f"--mysql-password={MYSQL_PASSWORD}",
    f"--mysql-db={MYSQL_DB}",
    f"--tables={TABLES}",
    f"--table-size={TABLE_SIZE}",
    f"--threads={THREADS}",
    "prepare"
])
txt_file.write_text(stdout + stderr)

# ------------------ Тестирование ------------------
print("🚀 Запуск теста...")
stdout, stderr, rc = run_sysbench([
    SCRIPT,
    f"--mysql-host={MYSQL_HOST}",
    f"--mysql-port={MYSQL_PORT}",
    f"--mysql-user={MYSQL_USER}",
    f"--mysql-password={MYSQL_PASSWORD}",
    f"--mysql-db={MYSQL_DB}",
    f"--tables={TABLES}",
    f"--table-size={TABLE_SIZE}",
    f"--threads={THREADS}",
    f"--time={DURATION}",
    "run"
])
txt_file.write_text(txt_file.read_text() + "\n" + stdout + "\n" + stderr)

# ------------------ Очистка ------------------
print("🧹 Очистка данных...")
stdout_clean, stderr_clean, rc = run_sysbench([
    SCRIPT,
    f"--mysql-host={MYSQL_HOST}",
    f"--mysql-port={MYSQL_PORT}",
    f"--mysql-user={MYSQL_USER}",
    f"--mysql-password={MYSQL_PASSWORD}",
    f"--mysql-db={MYSQL_DB}",
    f"--tables={TABLES}",
    f"--table-size={TABLE_SIZE}",
    f"--threads={THREADS}",
    "cleanup"
])
txt_file.write_text(txt_file.read_text() + "\n" + stdout_clean + "\n" + stderr_clean)

# ------------------ Парсинг ключевых метрик ------------------
def parse_key_metrics(output: str):
    def get(pattern, cast=float, default=0):
        match = re.search(pattern, output)
        if match:
            return cast(match.group(1))
        return default

    metrics = {
        "Транзакций/сек": get(r"transactions:\s+\d+\s+\(([\d.]+)"),
        "Запросов/сек": get(r"queries:\s+\d+\s+\(([\d.]+)"),
        "Avg задержка (мс)": get(r"avg:\s+([\d.]+)"),
        "Ошибки": get(r"ignored errors:\s+(\d+)", int)
    }
    return metrics

metrics = parse_key_metrics(stdout)

# ------------------ Сохранение CSV/Excel ------------------
df = pd.DataFrame([metrics])
df.to_csv(csv_file, index=False)
excel_file = csv_file.with_suffix(".xlsx")
df.to_excel(excel_file, index=False)

print("✅ Тест завершён!")
print(f"📄 Полный вывод: {txt_file}")
print(f"📊 CSV: {csv_file}")
print(f"📊 Excel: {excel_file}")