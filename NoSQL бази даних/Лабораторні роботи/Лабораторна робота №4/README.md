# Лабораторна робота №4

**Тема:** створення сховища ключів і початкове заповнення даними в Redis.

- Виконав: Левченко Д. В.
- Перевірив: Андреєв П. І.
- Варіант: 5

> [Повний звіт у форматі GitHub](./Звіт.md)

## Виконано

- підключення до локального Redis на `localhost:6379`;
- створення ключів типів String, Hash, List, Set і Sorted Set;
- серіалізація 10 Python-об'єктів у JSON;
- читання `data/products.csv` та пакетне завантаження 10 записів через Redis pipeline;
- перевірка збережених даних у Redis Insight;
- формування машинозчитуваного результату `results/lab4_results.json`.

## Запуск

```text
python -m pip install -r requirements.txt
python scripts/lab4_redis_storage.py
```

Після запуску в Redis Insight доступні службові ключі `lab4:*`, JSON-об'єкти `lab4:object:*` і товари `product:501` - `product:510`.

## Структура

- `scripts/lab4_redis_storage.py` - основний сценарій;
- `data/products.csv` - початковий набір даних;
- `results/lab4_results.json` - результати перевірки;
- [`screenshots/01-redisinsight-key-groups.png`](screenshots/01-redisinsight-key-groups.png) - групи ключів;
- [`screenshots/02-redisinsight-product-json.png`](screenshots/02-redisinsight-product-json.png) - товари з CSV і JSON;
- [`screenshots/03-redisinsight-key-types.png`](screenshots/03-redisinsight-key-types.png) - типи даних Redis;
- [`Звіт_ЛР4_Левченко.docx`](Звіт_ЛР4_Левченко.docx) - звіт про виконання.

