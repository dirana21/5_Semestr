# Лабораторна робота №5

**Тема:** робота зі структурами даних Redis і кешування MongoDB.

- Виконав: Левченко Д. В.
- Перевірив: Андреєв П. І.
- Варіант: 5

> [Повний звіт у форматі GitHub](./Звіт.md)

## Реалізовано

- патерн cache-aside для колекції `nosql_lab1_variant5.laboratory_works`;
- перше читання документа `lab-01` з MongoDB і повторне читання з Redis;
- кешування JSON з TTL 300 секунд;
- лічильники cache hit/cache miss у Redis Hash;
- останні п'ять лабораторних робіт у Redis List;
- унікальні інструменти у Redis Set;
- порядок лабораторних робіт у Redis Sorted Set;
- порівняльний тест швидкості MongoDB і Redis;
- структурований результат у `results/lab5_results.json`.

## Запуск

Перед запуском мають працювати локальні MongoDB і Redis.

```text
python -m pip install -r requirements.txt
python scripts/lab5_mongodb_redis_cache.py
```

## Структура

- `scripts/lab5_mongodb_redis_cache.py` - кеш-прослойка та перевірки;
- `results/lab5_results.json` - результат виконання;
- `screenshots/` - знімки Redis Insight і MongoDB Compass;
- `Звіт_ЛР5_Левченко.docx` - звіт про виконання.

