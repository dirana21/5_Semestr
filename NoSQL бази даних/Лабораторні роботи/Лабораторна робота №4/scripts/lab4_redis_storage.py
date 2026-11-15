from __future__ import annotations

import csv
import json
from pathlib import Path
from typing import Any

import redis


BASE_DIR = Path(__file__).resolve().parents[1]
CSV_PATH = BASE_DIR / "data" / "products.csv"
RESULT_PATH = BASE_DIR / "results" / "lab4_results.json"

HOST = "localhost"
PORT = 6379
VARIANT = 5


OBJECTS = [
    {"id": 501, "name": "Plasma Blade", "category": "Weapon", "price": 1450, "stock": 12, "rarity": "Legendary"},
    {"id": 502, "name": "Thunder Hammer", "category": "Weapon", "price": 1120, "stock": 9, "rarity": "Epic"},
    {"id": 503, "name": "Guardian Shield", "category": "Armor", "price": 780, "stock": 18, "rarity": "Rare"},
    {"id": 504, "name": "Scout Boots", "category": "Armor", "price": 430, "stock": 26, "rarity": "Uncommon"},
    {"id": 505, "name": "Energy Core", "category": "Resource", "price": 260, "stock": 40, "rarity": "Rare"},
    {"id": 506, "name": "Nano Repair Kit", "category": "Consumable", "price": 190, "stock": 55, "rarity": "Common"},
    {"id": 507, "name": "Cryo Grenade", "category": "Consumable", "price": 310, "stock": 24, "rarity": "Rare"},
    {"id": 508, "name": "Targeting Module", "category": "Module", "price": 670, "stock": 16, "rarity": "Epic"},
    {"id": 509, "name": "Stealth Field", "category": "Module", "price": 980, "stock": 7, "rarity": "Legendary"},
    {"id": 510, "name": "Combat Drone", "category": "Companion", "price": 1250, "stock": 6, "rarity": "Epic"},
]


def json_text(value: Any) -> str:
    return json.dumps(value, ensure_ascii=False, separators=(",", ":"))


def clear_lab_keys(client: redis.Redis) -> int:
    patterns = ("lab4:*", "product:5*")
    keys = sorted({key for pattern in patterns for key in client.scan_iter(match=pattern)})
    return client.delete(*keys) if keys else 0


def create_keys_of_different_types(client: redis.Redis) -> dict[str, str]:
    client.set("lab4:string:status", "Лабораторна робота 4, варіант 5")
    student_fields = {
        "name": "Левченко Д. В.",
        "reviewer": "Андреєв П. І.",
        "variant": str(VARIANT),
        "topic": "Redis key storage",
    }
    for field, value in student_fields.items():
        client.hset("lab4:hash:student", field, value)
    client.rpush("lab4:list:tasks", "connect", "create_keys", "serialize_json", "load_csv", "pipeline")
    client.sadd("lab4:set:categories", *(item["category"] for item in OBJECTS))
    client.zadd("lab4:zset:price_rating", {item["name"]: item["price"] for item in OBJECTS})
    return {
        "lab4:string:status": client.type("lab4:string:status"),
        "lab4:hash:student": client.type("lab4:hash:student"),
        "lab4:list:tasks": client.type("lab4:list:tasks"),
        "lab4:set:categories": client.type("lab4:set:categories"),
        "lab4:zset:price_rating": client.type("lab4:zset:price_rating"),
    }


def save_python_objects(client: redis.Redis) -> list[str]:
    keys: list[str] = []
    for item in OBJECTS:
        key = f"lab4:object:{item['id']}"
        client.set(key, json_text(item))
        keys.append(key)
    return keys


def load_csv_with_pipeline(client: redis.Redis) -> tuple[list[str], list[Any]]:
    keys: list[str] = []
    pipeline = client.pipeline(transaction=True)
    with CSV_PATH.open("r", encoding="utf-8", newline="") as stream:
        for row in csv.DictReader(stream):
            product = {
                "id": int(row["id"]),
                "name": row["name"],
                "category": row["category"],
                "price": int(row["price"]),
                "stock": int(row["stock"]),
                "rarity": row["rarity"],
                "source": "CSV pipeline",
                "variant": VARIANT,
            }
            key = f"product:{product['id']}"
            pipeline.set(key, json_text(product))
            keys.append(key)
    return keys, pipeline.execute()


def main() -> None:
    client = redis.Redis(host=HOST, port=PORT, decode_responses=True)
    ping = client.ping()
    redis_version = client.info(section="server")["redis_version"]
    removed = clear_lab_keys(client)
    key_types = create_keys_of_different_types(client)
    object_keys = save_python_objects(client)
    product_keys, pipeline_results = load_csv_with_pipeline(client)

    sample_product = json.loads(client.get("product:505"))
    restored_object = json.loads(client.get("lab4:object:501"))
    categories = sorted(client.smembers("lab4:set:categories"))
    price_rating = client.zrevrange("lab4:zset:price_rating", 0, 2, withscores=True)

    checks = {
        "serverPing": ping is True,
        "differentTypes": set(key_types.values()) == {"string", "hash", "list", "set", "zset"},
        "pythonObjectsStored": len(object_keys) == 10,
        "csvProductsStored": len(product_keys) == 10 and all(pipeline_results),
        "jsonRestored": restored_object == OBJECTS[0],
    }
    result = {
        "ok": all(checks.values()),
        "laboratoryWork": 4,
        "variant": VARIANT,
        "student": "Левченко Д. В.",
        "reviewer": "Андреєв П. І.",
        "connection": {"host": HOST, "port": PORT, "redisVersion": redis_version, "ping": ping},
        "removedPreviousKeys": removed,
        "checks": checks,
        "keyTypes": key_types,
        "pythonObjectKeys": object_keys,
        "pipeline": {
            "source": str(CSV_PATH.relative_to(BASE_DIR)),
            "commandCount": len(pipeline_results),
            "successfulCommands": sum(bool(item) for item in pipeline_results),
            "productKeys": product_keys,
        },
        "sampleProduct": sample_product,
        "categories": categories,
        "topThreeByPrice": [{"name": name, "price": score} for name, score in price_rating],
    }
    RESULT_PATH.parent.mkdir(parents=True, exist_ok=True)
    RESULT_PATH.write_text(json.dumps(result, ensure_ascii=False, indent=2), encoding="utf-8")
    print(json.dumps(result, ensure_ascii=False, indent=2))
    if not result["ok"]:
        raise SystemExit(1)


if __name__ == "__main__":
    main()

