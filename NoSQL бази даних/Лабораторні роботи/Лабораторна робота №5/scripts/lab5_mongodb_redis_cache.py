from __future__ import annotations

import json
import statistics
import time
from datetime import date, datetime
from pathlib import Path
from typing import Any

import redis
from bson import ObjectId
from pymongo import MongoClient


BASE_DIR = Path(__file__).resolve().parents[1]
RESULT_PATH = BASE_DIR / "results" / "lab5_results.json"

MONGO_URI = "mongodb://127.0.0.1:27017"
MONGO_DATABASE = "nosql_lab1_variant5"
MONGO_COLLECTION = "laboratory_works"
REDIS_HOST = "127.0.0.1"
REDIS_PORT = 6379
CACHE_TTL_SECONDS = 300
VARIANT = 5


def json_default(value: Any) -> str:
    if isinstance(value, ObjectId):
        return str(value)
    if isinstance(value, (datetime, date)):
        return value.isoformat()
    raise TypeError(f"Unsupported value: {type(value)!r}")


def encode(value: Any) -> str:
    return json.dumps(value, ensure_ascii=False, default=json_default, separators=(",", ":"))


class LaboratoryWorkCache:
    def __init__(self, mongo_collection, redis_client: redis.Redis, ttl: int = CACHE_TTL_SECONDS):
        self.collection = mongo_collection
        self.redis = redis_client
        self.ttl = ttl

    @staticmethod
    def key(lab_id: str) -> str:
        return f"lab5:lab:{lab_id}"

    def get(self, lab_id: str) -> tuple[dict[str, Any] | None, str, float]:
        started = time.perf_counter_ns()
        cached = self.redis.get(self.key(lab_id))
        if cached is not None:
            self.redis.hincrby("lab5:metrics", "hits", 1)
            elapsed_ms = (time.perf_counter_ns() - started) / 1_000_000
            return json.loads(cached), "redis", elapsed_ms

        self.redis.hincrby("lab5:metrics", "misses", 1)
        document = self.collection.find_one({"_id": lab_id})
        if document is not None:
            self.redis.setex(self.key(lab_id), self.ttl, encode(document))
        elapsed_ms = (time.perf_counter_ns() - started) / 1_000_000
        return document, "mongodb", elapsed_ms

    def invalidate(self, lab_id: str) -> int:
        return self.redis.delete(self.key(lab_id))


def clear_lab5_keys(client: redis.Redis) -> int:
    keys = list(client.scan_iter(match="lab5:*"))
    return client.delete(*keys) if keys else 0


def fill_supporting_structures(collection, client: redis.Redis) -> dict[str, Any]:
    documents = list(collection.find({}, {"_id": 1, "number": 1, "title": 1, "tools": 1}).sort("number", -1))

    pipeline = client.pipeline(transaction=True)
    pipeline.delete("lab5:recent_labs")
    for document in documents[:5]:
        pipeline.rpush("lab5:recent_labs", encode(document))
    pipeline.ltrim("lab5:recent_labs", 0, 4)
    pipeline.delete("lab5:tools")
    unique_tools = sorted({tool for document in documents for tool in document.get("tools", [])})
    if unique_tools:
        pipeline.sadd("lab5:tools", *unique_tools)
    pipeline.delete("lab5:lab_order")
    pipeline.zadd("lab5:lab_order", {document["_id"]: document.get("number", 0) for document in documents})
    pipeline_results = pipeline.execute()

    return {
        "recentLabCount": client.llen("lab5:recent_labs"),
        "uniqueToolCount": client.scard("lab5:tools"),
        "sortedLabCount": client.zcard("lab5:lab_order"),
        "pipelineCommandCount": len(pipeline_results),
    }


def benchmark(collection, cache: LaboratoryWorkCache, lab_id: str, iterations: int = 100) -> dict[str, Any]:
    mongo_times: list[float] = []
    redis_times: list[float] = []
    for _ in range(iterations):
        started = time.perf_counter_ns()
        collection.find_one({"_id": lab_id})
        mongo_times.append((time.perf_counter_ns() - started) / 1_000_000)

        started = time.perf_counter_ns()
        cache.redis.get(cache.key(lab_id))
        redis_times.append((time.perf_counter_ns() - started) / 1_000_000)

    mongo_median = statistics.median(mongo_times)
    redis_median = statistics.median(redis_times)
    return {
        "iterations": iterations,
        "mongoMedianMs": round(mongo_median, 4),
        "redisMedianMs": round(redis_median, 4),
        "speedup": round(mongo_median / redis_median, 2) if redis_median else None,
    }


def main() -> None:
    mongo_client = MongoClient(MONGO_URI, serverSelectionTimeoutMS=5000)
    mongo_ping = mongo_client.admin.command("ping").get("ok") == 1.0
    collection = mongo_client[MONGO_DATABASE][MONGO_COLLECTION]

    redis_client = redis.Redis(host=REDIS_HOST, port=REDIS_PORT, decode_responses=True)
    redis_ping = redis_client.ping()
    redis_version = redis_client.info(section="server")["redis_version"]

    removed = clear_lab5_keys(redis_client)
    cache = LaboratoryWorkCache(collection, redis_client)
    target_id = "lab-01"

    first_document, first_source, first_ms = cache.get(target_id)
    second_document, second_source, second_ms = cache.get(target_id)
    structures = fill_supporting_structures(collection, redis_client)
    benchmark_result = benchmark(collection, cache, target_id)

    metrics = {key: int(value) for key, value in redis_client.hgetall("lab5:metrics").items()}
    ttl = redis_client.ttl(cache.key(target_id))
    recent_ids = [json.loads(value)["_id"] for value in redis_client.lrange("lab5:recent_labs", 0, -1)]
    tools = sorted(redis_client.smembers("lab5:tools"))
    ordered_labs = redis_client.zrevrange("lab5:lab_order", 0, 4, withscores=True)

    checks = {
        "mongoConnected": mongo_ping,
        "redisConnected": redis_ping is True,
        "firstReadFromMongo": first_source == "mongodb",
        "secondReadFromRedis": second_source == "redis",
        "documentsEqual": first_document == second_document and first_document is not None,
        "ttlConfigured": 0 < ttl <= CACHE_TTL_SECONDS,
        "recentListLimited": structures["recentLabCount"] == 5,
        "toolSetCreated": structures["uniqueToolCount"] > 0,
        "sortedSetCreated": structures["sortedLabCount"] == collection.count_documents({}),
    }

    result = {
        "ok": all(checks.values()),
        "laboratoryWork": 5,
        "variant": VARIANT,
        "student": "Левченко Д. В.",
        "reviewer": "Андреєв П. І.",
        "mongodb": {
            "uri": MONGO_URI,
            "database": MONGO_DATABASE,
            "collection": MONGO_COLLECTION,
            "documentCount": collection.count_documents({}),
            "ping": mongo_ping,
        },
        "redis": {
            "host": REDIS_HOST,
            "port": REDIS_PORT,
            "version": redis_version,
            "ping": redis_ping,
            "cacheTtlSeconds": CACHE_TTL_SECONDS,
        },
        "removedPreviousKeys": removed,
        "checks": checks,
        "cacheAside": {
            "key": cache.key(target_id),
            "firstRead": {"source": first_source, "elapsedMs": round(first_ms, 4)},
            "secondRead": {"source": second_source, "elapsedMs": round(second_ms, 4)},
            "ttlRemainingSeconds": ttl,
            "metrics": metrics,
            "document": second_document,
        },
        "structures": {
            **structures,
            "recentLabIds": recent_ids,
            "tools": tools,
            "topFiveLabOrder": [{"id": lab_id, "number": score} for lab_id, score in ordered_labs],
        },
        "benchmark": benchmark_result,
    }

    RESULT_PATH.parent.mkdir(parents=True, exist_ok=True)
    RESULT_PATH.write_text(json.dumps(result, ensure_ascii=False, indent=2), encoding="utf-8")
    print(json.dumps(result, ensure_ascii=False, indent=2))
    if not result["ok"]:
        raise SystemExit(1)


if __name__ == "__main__":
    main()

