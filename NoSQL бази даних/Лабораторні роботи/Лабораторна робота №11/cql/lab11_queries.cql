USE lab11_queries_v5;

-- Повний ключ партиціювання.
SELECT * FROM orders_by_user
WHERE user_id = 50000000-0000-0000-0000-000000000001;

-- Повний композитний partition key.
SELECT * FROM activity_by_group
WHERE faculty = 'FKS' AND group_code = 'KN-31';

-- Частковий композитний partition key: потрібне ALLOW FILTERING.
SELECT * FROM activity_by_group
WHERE faculty = 'FKS' ALLOW FILTERING;

-- Запит без partition key.
SELECT * FROM users_by_id
WHERE city = 'Кременчук' ALLOW FILTERING;

-- ORDER BY дозволено після фільтрації за partition key.
SELECT * FROM orders_by_user
WHERE user_id = 50000000-0000-0000-0000-000000000001
ORDER BY order_date DESC, order_id ASC;

-- Запит за колонкою з вторинним індексом.
SELECT * FROM orders_by_user WHERE status = 'completed';

TRACING ON;
SELECT * FROM orders_by_user
WHERE user_id = 50000000-0000-0000-0000-000000000001
LIMIT 5;
TRACING OFF;

