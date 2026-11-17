from datetime import date, timedelta
from decimal import Decimal
from pathlib import Path
from uuid import UUID, uuid1

from cassandra.cluster import Cluster


ROOT = Path(__file__).resolve().parents[1]
SCHEMA = ROOT / "cql" / "lab11_schema.cql"
KEYSPACE = "lab11_queries_v5"


def statements(text: str):
    current = []
    for raw in text.splitlines():
        line = raw.strip()
        if not line or line.startswith("--"):
            continue
        current.append(raw)
        if line.endswith(";"):
            yield "\n".join(current).rstrip(";\n ")
            current = []
    if current:
        yield "\n".join(current)


cluster = Cluster(["127.0.0.1"], port=9042)
session = cluster.connect()
for statement in statements(SCHEMA.read_text(encoding="utf-8")):
    session.execute(statement)

session.set_keyspace(KEYSPACE)

cities = ["Кременчук", "Київ", "Полтава", "Дніпро", "Черкаси"]
names = [
    "Левченко Дмитро", "Бондаренко Ірина", "Коваль Олег", "Мельник Анна",
    "Шевченко Максим", "Ткаченко Марія", "Олійник Богдан", "Кравченко Софія",
    "Іваненко Артем", "Петренко Дарина", "Савченко Назар", "Романенко Юлія",
    "Мороз Владислав", "Лисенко Аліна", "Павленко Денис", "Гриценко Катерина",
    "Сидоренко Андрій", "Поліщук Олена", "Марченко Ілля", "Руденко Вікторія",
    "Козак Михайло", "Бойко Христина", "Клименко Роман", "Захарченко Єва",
    "Даниленко Кирило",
]

insert_user = session.prepare(
    "INSERT INTO users_by_id (user_id, full_name, city, age, variant) VALUES (?, ?, ?, ?, ?)"
)
for i, name in enumerate(names, 1):
    session.execute(insert_user, (UUID(f"50000000-0000-0000-0000-{i:012d}"), name, cities[(i - 1) % 5], 18 + i % 8, 5))

insert_order = session.prepare(
    "INSERT INTO orders_by_user (user_id, order_date, order_id, total, status) VALUES (?, ?, ?, ?, ?)"
)
statuses = ["completed", "processing", "cancelled", "completed", "shipped"]
base = date(2026, 11, 1)
for i in range(25):
    user_no = i // 5 + 1
    user_id = UUID(f"50000000-0000-0000-0000-{user_no:012d}")
    order_id = UUID(f"51000000-0000-0000-0000-{i + 1:012d}")
    session.execute(insert_order, (user_id, base + timedelta(days=i), order_id, Decimal(f"{125 + i * 13}.50"), statuses[i % 5]))

insert_activity = session.prepare(
    "INSERT INTO activity_by_group (faculty, group_code, event_date, event_id, student_name, action) VALUES (?, ?, ?, ?, ?, ?)"
)
groups = [("FKS", "KN-31"), ("FKS", "KN-32"), ("FEU", "EK-31"), ("FKS", "KN-31"), ("FEU", "EK-32")]
actions = ["login", "query", "submit", "review", "logout"]
for i in range(25):
    faculty, group = groups[i % 5]
    session.execute(insert_activity, (faculty, group, base + timedelta(days=i), uuid1(), names[i], actions[i % 5]))

print("Created lab11_queries_v5: 25 users, 25 orders, 25 activity rows")
cluster.shutdown()

