import re
import pandas as pd # type: ignore
import subprocess

ip=input("ip базы \n")

script_path = "./test_pg.sh"

statistika = subprocess.run(
    ["bash", script_path, ip],           # или просто [script_path], если в скрипте есть shebang (#!)
    capture_output=True,             # чтобы получить stdout и stderr
    text=True                        # чтобы получить строки, а не байты
)

stdout = statistika.stdout
return_code = statistika.returncode

print("Код возврата:", return_code)

# Функция парсинга статистики
def parse_sql_stats(text):
    def get(pattern, cast=str, default=None):
        match = re.search(pattern, text)
        if match:
            return cast(match.group(1))
        print(f"⚠️ Не найдено: {pattern}")
        return default

    metrics = {
        "transactions": get(r"transactions:\s+(\d+)", int),
        "transactions_per_sec": get(r"transactions:\s+\d+\s+\(([\d.]+)", float),
        "total_queries": get(r"queries:\s+(\d+)", int),
        "queries_per_sec": get(r"queries:\s+\d+\s+\(([\d.]+)", float),
        "latency_min": get(r"min:\s+([\d.]+)", float),
        "latency_avg": get(r"avg:\s+([\d.]+)", float),
        "latency_max": get(r"max:\s+([\d.]+)", float),
        "latency_95": get(r"95th percentile:\s+([\d.]+)", float),
        "errors": get(r"ignored errors:\s+(\d+)", int),
        "reconnects": get(r"reconnects:\s+(\d+)", int)
    }

    return list(metrics.values())

# Получение результатов
result = parse_sql_stats(stdout)

# Вывод или дальнейшее использование
print('"sel-sel":', result)

data = {
    "Метрика": [
        "Транзакции",
        "Транзакции/сек",
        "Всего запросов",
        "Запросов/сек",
        "Min задержка (мс)",
        "Avg задержка (мс)",
        "Max задержка (мс)",
        "95% перцентиль (мс)",
        "Ошибки",
        "Reconnects"
    ],
    "sel-sel": result
}

df = pd.DataFrame(data)

# Сохранение в Excel
file_path = "./sql_benchmark_report.xlsx"
df.to_excel(file_path, index=False)

file_path
