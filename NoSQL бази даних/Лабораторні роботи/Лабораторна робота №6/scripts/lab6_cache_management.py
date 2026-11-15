from __future__ import annotations

import json
import time
from datetime import date, datetime, timezone
from pathlib import Path
from typing import Any

import redis
from bson import ObjectId
from pymongo import MongoClient


BASE_DIR = Path(__file__).resolve().parents[1]
RESULT_PATH = BASE_DIR / "results" / "lab6_results.json"

MONGO_URI = "mongodb://127.0.0.1:27017"
MONGO_DATABASE = "nosql_lab1_variant5"
SOURCE_COLLECTION = "laboratory_works"
DEMO_COLLECTION = "lab6_cache_management"
REDIS_HOST = "127.0.0.1"
REDIS_PORT = 6379
CACHE_TTL_SECONDS = 300
SESSION_TTL_SECONDS = 300
EXPIRY_TEST_SECONDS = 1
VARIANT = 5
DEMO_ID = "lab6-demo-variant5"


def json_default(value: Any) -> str:
    if isinstance(value, ObjectId):
        return str(value)
    if isinstance(value, (datetime, date)):
        return value.isoformat()
    raise TypeError(f"Unsupported value: {type(value)!r}")


def encode(value: Any) -> str:
    return json.dumps(value, ensure_ascii=False, default=json_default, separators=(",", ":"))


def clear_lab6_keys(client: redis.Redis) -> int:
    keys = list(client.scan_iter(match="lab6:*"))
    return client.delete(*keys) if keys else 0


class ManagedCache:
    def __init__(self, collection, client: redis.Redis, ttl: int = CACHE_TTL_SECONDS):
        self.collection = collection
        self.client = client
        self.ttl = ttl

    @staticmethod
    def cache_key(document_id: str) -> str:
        return f"lab6:cache:{document_id}"

    def cache_aside(self, document_id: str) -> tuple[dict[str, Any] | None, str]:
        key = self.cache_key(document_id)
        cached = self.client.get(key)
        if cached is not None:
            self.client.hincrby("lab6:metrics", "hits", 1)
            return json.loads(cached), "redis"

        self.client.hincrby("lab6:metrics", "misses", 1)
        document = self.collection.find_one({"_id": document_id})
        if document is not None:
            self.client.setex(key, self.ttl, encode(document))
        return document, "mongodb"

    def write_through(self, document_id: str, changes: dict[str, Any]) -> dict[str, Any]:
        self.collection.update_one({"_id": document_id}, {"$set": changes})
        document = self.collection.find_one({"_id": document_id})
        if document is None:
            raise RuntimeError("Document was not found after write-through update")
        self.client.setex(self.cache_key(document_id), self.ttl, encode(document))
        return document


def transfer_funds(client: redis.Redis, source: str, target: str, amount: int) -> dict[str, int]:
    source_key = f"lab6:balance:{source}"
    target_key = f"lab6:balance:{target}"
    while True:
        with client.pipeline() as pipe:
            try:
                pipe.watch(source_key, target_key)
                source_before = int(pipe.get(source_key) or 0)
                target_before = int(pipe.get(target_key) or 0)
                if source_before < amount:
                    pipe.unwatch()
                    raise ValueError("Insufficient funds")

                pipe.multi()
                pipe.decrby(source_key, amount)
                pipe.incrby(target_key, amount)
                summary = {
                    "source": source,
                    "target": target,
                    "amount": amount,
                    "source_before": source_before,
                    "target_before": target_before,
                    "source_after": source_before - amount,
                    "target_after": target_before + amount,
                }
                summary_arguments = [item for pair in summary.items() for item in pair]
                pipe.execute_command("HMSET", "lab6:transaction:summary", *summary_arguments)
                pipe.execute()
                return {
                    "sourceBefore": source_before,
                    "targetBefore": target_before,
                    "sourceAfter": source_before - amount,
                    "targetAfter": target_before + amount,
                    "amount": amount,
                }
            except redis.WatchError:
                continue


def main() -> None:
    mongo_client = MongoClient(MONGO_URI, serverSelectionTimeoutMS=5000)
    mongo_ping = mongo_client.admin.command("ping").get("ok") == 1.0
    database = mongo_client[MONGO_DATABASE]
    source_collection = database[SOURCE_COLLECTION]
    demo_collection = database[DEMO_COLLECTION]

    redis_client = redis.Redis(host=REDIS_HOST, port=REDIS_PORT, decode_responses=True)
    redis_ping = redis_client.ping()
    redis_version = redis_client.info(section="server")["redis_version"]
    eviction_policy = redis_client.config_get("maxmemory-policy").get("maxmemory-policy", "unknown")

    removed = clear_lab6_keys(redis_client)
    source_document = source_collection.find_one({"_id": "lab-01"})
    if source_document is None:
        raise RuntimeError("Source document lab-01 is missing")

    seed_document = {
        "_id": DEMO_ID,
        "variant": VARIANT,
        "sourceLabId": source_document["_id"],
        "title": source_document.get("title", "Лабораторна робота"),
        "status": "підготовлено",
        "cacheMode": "cache-aside",
        "cacheTtlSeconds": CACHE_TTL_SECONDS,
        "student": "Левченко Д. В.",
    }
    demo_collection.replace_one({"_id": DEMO_ID}, seed_document, upsert=True)

    cache = ManagedCache(demo_collection, redis_client)
    first_document, first_source = cache.cache_aside(DEMO_ID)
    second_document, second_source = cache.cache_aside(DEMO_ID)

    write_through_document = cache.write_through(
        DEMO_ID,
        {
            "status": "активний",
            "cacheMode": "write-through",
            "updatedAt": datetime.now(timezone.utc).replace(microsecond=0),
        },
    )

    redis_client.setex("lab6:session:variant5", SESSION_TTL_SECONDS, "active")
    session_ttl = redis_client.ttl("lab6:session:variant5")
    redis_client.setex("lab6:temporary:expiry-check", EXPIRY_TEST_SECONDS, "delete-me")
    expiry_ttl_before = redis_client.ttl("lab6:temporary:expiry-check")
    time.sleep(EXPIRY_TEST_SECONDS + 0.25)
    expiry_value_after = redis_client.get("lab6:temporary:expiry-check")
    redis_client.setex("lab6:temporary:preview", 180, "automatic-expiration-enabled")

    redis_client.mset({"lab6:balance:account1": 1000, "lab6:balance:account2": 500})
    transaction = transfer_funds(redis_client, "account1", "account2", 200)
    view_count = redis_client.incrby(f"lab6:views:{DEMO_ID}", 5)

    cached_after_write = json.loads(redis_client.get(cache.cache_key(DEMO_ID)) or "null")
    mongo_after_write = demo_collection.find_one({"_id": DEMO_ID})
    cache_ttl = redis_client.ttl(cache.cache_key(DEMO_ID))
    metrics = {key: int(value) for key, value in redis_client.hgetall("lab6:metrics").items()}
    transaction_summary = redis_client.hgetall("lab6:transaction:summary")

    checks = {
        "mongoConnected": mongo_ping,
        "redisConnected": redis_ping is True,
        "firstReadFromMongo": first_source == "mongodb",
        "secondReadFromRedis": second_source == "redis",
        "cacheAsideDocumentsEqual": first_document == second_document and first_document is not None,
        "writeThroughSynchronized": cached_after_write == json.loads(encode(mongo_after_write)),
        "cacheTtlConfigured": 0 < cache_ttl <= CACHE_TTL_SECONDS,
        "sessionTtlConfigured": 0 < session_ttl <= SESSION_TTL_SECONDS,
        "temporaryKeyExpired": expiry_ttl_before > 0 and expiry_value_after is None,
        "transactionAtomicResult": transaction["sourceAfter"] == 800 and transaction["targetAfter"] == 700,
        "atomicCounterUpdated": view_count == 5,
        "evictionPolicyRead": eviction_policy != "unknown",
    }

    result = {
        "ok": all(checks.values()),
        "laboratoryWork": 6,
        "variant": VARIANT,
        "student": "Левченко Д. В.",
        "reviewer": "Андреєв П. І.",
        "mongodb": {
            "uri": MONGO_URI,
            "database": MONGO_DATABASE,
            "sourceCollection": SOURCE_COLLECTION,
            "demoCollection": DEMO_COLLECTION,
            "sourceDocumentId": source_document["_id"],
            "demoDocument": mongo_after_write,
            "ping": mongo_ping,
        },
        "redis": {
            "host": REDIS_HOST,
            "port": REDIS_PORT,
            "version": redis_version,
            "ping": redis_ping,
            "maxmemoryPolicy": eviction_policy,
            "recommendedCachePolicy": "allkeys-lru",
        },
        "removedPreviousKeys": removed,
        "checks": checks,
        "cachePatterns": {
            "cacheKey": cache.cache_key(DEMO_ID),
            "cacheTtlSeconds": CACHE_TTL_SECONDS,
            "firstReadSource": first_source,
            "secondReadSource": second_source,
            "metrics": metrics,
            "writeThroughStatus": write_through_document["status"],
            "writeThroughMode": write_through_document["cacheMode"],
        },
        "lifecycle": {
            "sessionKey": "lab6:session:variant5",
            "sessionTtlSeconds": session_ttl,
            "expiryTestTtlBefore": expiry_ttl_before,
            "expiryTestValueAfter": expiry_value_after,
            "previewKey": "lab6:temporary:preview",
            "previewTtlSeconds": redis_client.ttl("lab6:temporary:preview"),
        },
        "transaction": {
            **transaction,
            "summary": transaction_summary,
        },
        "atomicCounter": {
            "key": f"lab6:views:{DEMO_ID}",
            "value": view_count,
            "command": "INCRBY 5",
        },
    }

    RESULT_PATH.parent.mkdir(parents=True, exist_ok=True)
    RESULT_PATH.write_text(json.dumps(result, ensure_ascii=False, indent=2, default=json_default), encoding="utf-8")
    print(json.dumps(result, ensure_ascii=False, indent=2, default=json_default))
    if not result["ok"]:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
