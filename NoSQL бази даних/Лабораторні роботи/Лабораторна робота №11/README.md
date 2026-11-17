# Лабораторна робота №11

Виконання запитів до таблиць Cassandra мовою CQL.

- Варіант: 5
- Виконав: Левченко Д. В.
- Перевірив: Андреєв П. І.

Повний звіт у форматі GitHub: [Звіт.md](./Звіт.md).

## Склад роботи

- `cql/lab11_schema.cql` — keyspace, таблиці та вторинний індекс;
- `cql/lab11_queries.cql` — запити SELECT, ORDER BY, ALLOW FILTERING і TRACING;
- `scripts/setup_lab11.py` — створення схеми та 25 записів у кожній таблиці;
- `scripts/validate_lab11.py` — автоматична перевірка запитів і трасування;
- `results/lab11_results.json` — машинний протокол результатів.

