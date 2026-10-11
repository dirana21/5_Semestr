"""Лабораторна робота №2: 25 запитів PyMongo та аналіз індексу."""

from __future__ import annotations

import argparse
import json
from datetime import date, datetime
from pathlib import Path
from typing import Any

from bson import ObjectId
from pymongo import ASCENDING, MongoClient
from pymongo.collection import Collection


MONGO_URI = "mongodb://127.0.0.1:27017"
DATABASE_NAME = "nosql_lab1_variant5"
INDEX_NAME = "variant_1_lab2"


QUERIES: list[dict[str, Any]] = [
    {"title": "Дисципліни п'ятого семестру", "category": "$eq", "collection": "disciplines", "filter": {"semester": 5}},
    {"title": "Дисципліни з кількістю кредитів понад три", "category": "$gt", "collection": "disciplines", "filter": {"credits": {"$gt": 3}}},
    {"title": "Дисципліни щонайменше з чотирма кредитами", "category": "$gte", "collection": "disciplines", "filter": {"credits": {"$gte": 4}}},
    {"title": "Дисципліни з кількістю кредитів менше чотирьох", "category": "$lt", "collection": "disciplines", "filter": {"credits": {"$lt": 4}}},
    {"title": "Лабораторні роботи з номером не більше одного", "category": "$lte", "collection": "laboratory_works", "filter": {"number": {"$lte": 1}}},
    {"title": "Дисципліни, код яких відрізняється від NOSQL-05", "category": "$ne", "collection": "disciplines", "filter": {"code": {"$ne": "NOSQL-05"}}},
    {"title": "Дисципліни з вибраного переліку кодів", "category": "$in", "collection": "disciplines", "filter": {"code": {"$in": ["NOSQL-05", "PY-05", "SEC-05"]}}},
    {"title": "Лабораторні без варіантів 1 і 12", "category": "$nin", "collection": "laboratory_works", "filter": {"variant": {"$nin": [1, 12]}}},
    {"title": "Лабораторні варіанта 5 у запланованому стані", "category": "$and", "collection": "laboratory_works", "filter": {"$and": [{"variant": 5}, {"status": "заплановано"}]}},
    {"title": "Завершені або заплановані лабораторні", "category": "$or", "collection": "laboratory_works", "filter": {"$or": [{"status": "завершено"}, {"status": "заплановано"}]}},
    {"title": "Лабораторні, які не є запланованими та не мають варіант 1", "category": "$nor", "collection": "laboratory_works", "filter": {"$nor": [{"status": "заплановано"}, {"variant": 1}]}},
    {"title": "Студенти, ім'я яких не починається зі слова Студент", "category": "$not", "collection": "students", "filter": {"fullName": {"$not": {"$regex": "^Студент"}}}},
    {"title": "Дисципліна NoSQL за регулярним виразом", "category": "$regex", "collection": "disciplines", "filter": {"name": {"$regex": "^NoSQL", "$options": "i"}}},
    {"title": "Лабораторні, назва яких містить слово шифр", "category": "$regex", "collection": "laboratory_works", "filter": {"title": {"$regex": "шифр", "$options": "i"}}},
    {"title": "Дисципліни викладача teacher-01", "category": "вкладене поле", "collection": "disciplines", "filter": {"curator.teacherId": "teacher-01"}},
    {"title": "Дисципліни з варіантом 12 у джерелі", "category": "вкладене поле", "collection": "disciplines", "filter": {"source.variant": 12}},
    {"title": "Власник репозиторію портфоліо", "category": "вкладене поле", "collection": "students", "filter": {"portfolio.owner": True}},
    {"title": "Завдання з вимогою щонайменше семи колекцій", "category": "вкладене поле", "collection": "assignments", "filter": {"requirements.minCollections": {"$gte": 7}}},
    {"title": "Подання до репозиторію dirana21", "category": "вкладене поле", "collection": "submissions", "filter": {"repository.owner": "dirana21"}},
    {"title": "Лабораторні, у масиві tools яких є MongoDB", "category": "масив", "collection": "laboratory_works", "filter": {"tools": "MongoDB"}},
    {"title": "Студент із навичками Python і MongoDB", "category": "$all", "collection": "students", "filter": {"skills": {"$all": ["Python", "MongoDB"]}}},
    {"title": "Викладач із трьома дисциплінами", "category": "$size", "collection": "teachers", "filter": {"disciplines": {"$size": 3}}},
    {"title": "Завдання з методом, назва якого починається з insert", "category": "$elemMatch", "collection": "assignments", "filter": {"requirements.requiredMethods": {"$elemMatch": {"$regex": "^insert"}}}},
    {"title": "Завершені лабораторні з Python у переліку інструментів", "category": "$and + масив", "collection": "laboratory_works", "filter": {"$and": [{"status": "завершено"}, {"tools": {"$in": ["Python"]}}]}},
    {"title": "Оцінювання без виставленого бала, що очікує перевірки", "category": "$and + null", "collection": "grades", "filter": {"$and": [{"score": None}, {"status": "очікує перевірки"}]}},
]


def json_safe(value: Any) -> Any:
    if isinstance(value, dict):
        return {key: json_safe(item) for key, item in value.items()}
    if isinstance(value, list):
        return [json_safe(item) for item in value]
    if isinstance(value, (datetime, date)):
        return value.isoformat()
    if isinstance(value, ObjectId):
        return str(value)
    return value


def plan_stages(node: Any) -> set[str]:
    """Повертає всі назви stage з дерева explain()."""
    stages: set[str] = set()
    if isinstance(node, dict):
        stage = node.get("stage")
        if isinstance(stage, str):
            stages.add(stage)
        for value in node.values():
            stages.update(plan_stages(value))
    elif isinstance(node, list):
        for value in node:
            stages.update(plan_stages(value))
    return stages


def explain_query(collection: Collection, query_filter: dict[str, Any]) -> dict[str, Any]:
    result = collection.database.command(
        "explain",
        {"find": collection.name, "filter": query_filter},
        verbosity="executionStats",
    )
    stats = result["executionStats"]
    planner = result["queryPlanner"]
    stages = sorted(plan_stages(planner.get("winningPlan", {})))
    return {
        "stages": stages,
        "executionSuccess": stats["executionSuccess"],
        "nReturned": stats["nReturned"],
        "totalKeysExamined": stats["totalKeysExamined"],
        "totalDocsExamined": stats["totalDocsExamined"],
    }


def run_queries(database) -> list[dict[str, Any]]:
    results: list[dict[str, Any]] = []
    for number, query in enumerate(QUERIES, start=1):
        collection = database[query["collection"]]
        documents = list(collection.find(query["filter"]).sort("_id", ASCENDING))
        if not documents:
            raise AssertionError(f"Запит {number} не повернув жодного документа")
        results.append(
            {
                "number": number,
                "title": query["title"],
                "category": query["category"],
                "collection": query["collection"],
                "filter": json_safe(query["filter"]),
                "matched": len(documents),
                "sampleIds": [str(document["_id"]) for document in documents[:3]],
            }
        )
    return results


def analyze_index(database) -> dict[str, Any]:
    collection = database["laboratory_works"]
    query_filter = {"variant": 5}

    if INDEX_NAME in collection.index_information():
        collection.drop_index(INDEX_NAME)
    before = explain_query(collection, query_filter)

    collection.create_index([("variant", ASCENDING)], name=INDEX_NAME)
    after = explain_query(collection, query_filter)

    if "COLLSCAN" not in before["stages"]:
        raise AssertionError(f"До створення індексу очікувався COLLSCAN: {before}")
    if "IXSCAN" not in after["stages"]:
        raise AssertionError(f"Після створення індексу очікувався IXSCAN: {after}")

    return {
        "collection": collection.name,
        "filter": query_filter,
        "index": {"name": INDEX_NAME, "keys": {"variant": 1}},
        "before": before,
        "after": after,
    }


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--uri", default=MONGO_URI)
    parser.add_argument("--database", default=DATABASE_NAME)
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()

    client = MongoClient(args.uri, serverSelectionTimeoutMS=5_000)
    client.admin.command("ping")
    database = client[args.database]

    required_collections = {query["collection"] for query in QUERIES}
    missing = sorted(required_collections - set(database.list_collection_names()))
    if missing:
        raise RuntimeError(f"У базі відсутні колекції: {', '.join(missing)}")

    results = run_queries(database)
    index_analysis = analyze_index(database)
    report = {
        "ok": True,
        "database": database.name,
        "queryCount": len(results),
        "queries": results,
        "indexAnalysis": index_analysis,
    }

    text = json.dumps(report, ensure_ascii=False, indent=2)
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(text + "\n", encoding="utf-8")
    print(text)
    client.close()


if __name__ == "__main__":
    main()
