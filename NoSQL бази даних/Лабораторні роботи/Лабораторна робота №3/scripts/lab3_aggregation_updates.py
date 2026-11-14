"""ЛР3: агрегація та модифікація документів у MongoDB, варіант 5."""

from __future__ import annotations

import argparse
import json
from datetime import date, datetime
from pathlib import Path
from typing import Any

from bson import ObjectId
from pymongo import MongoClient


MONGO_URI = "mongodb://127.0.0.1:27017"
DATABASE_NAME = "nosql_lab1_variant5"
SANDBOX_COLLECTION = "lab3_updates"
LAB_MARKER = "nosql-lab3-v5"


AGGREGATIONS: list[dict[str, Any]] = [
    {
        "name": "Статуси лабораторних робіт",
        "collection": "laboratory_works",
        "pipeline": [
            {"$match": {"number": {"$gte": 1}}},
            {
                "$group": {
                    "_id": "$status",
                    "count": {"$sum": 1},
                    "averageNumber": {"$avg": "$number"},
                    "minimumNumber": {"$min": "$number"},
                    "maximumNumber": {"$max": "$number"},
                }
            },
            {"$sort": {"count": -1, "_id": 1}},
            {
                "$project": {
                    "_id": 0,
                    "status": "$_id",
                    "count": 1,
                    "averageNumber": {"$round": ["$averageNumber", 2]},
                    "minimumNumber": 1,
                    "maximumNumber": 1,
                }
            },
        ],
    },
    {
        "name": "Навчальне навантаження викладачів",
        "collection": "disciplines",
        "pipeline": [
            {
                "$lookup": {
                    "from": "laboratory_works",
                    "localField": "_id",
                    "foreignField": "courseId",
                    "as": "laboratoryWorks",
                }
            },
            {"$unwind": "$laboratoryWorks"},
            {
                "$group": {
                    "_id": "$curator.teacherId",
                    "teacher": {"$first": "$curator.name"},
                    "firstCourse": {"$first": "$name"},
                    "lastCourse": {"$last": "$name"},
                    "laboratoryCount": {"$sum": 1},
                    "averageCredits": {"$avg": "$credits"},
                    "minimumVariant": {"$min": "$laboratoryWorks.variant"},
                    "maximumVariant": {"$max": "$laboratoryWorks.variant"},
                }
            },
            {"$sort": {"laboratoryCount": -1, "_id": 1}},
            {
                "$project": {
                    "_id": 0,
                    "teacherId": "$_id",
                    "teacher": 1,
                    "firstCourse": 1,
                    "lastCourse": 1,
                    "laboratoryCount": 1,
                    "averageCredits": {"$round": ["$averageCredits", 2]},
                    "minimumVariant": 1,
                    "maximumVariant": 1,
                }
            },
        ],
    },
    {
        "name": "Найпоширеніші технології",
        "collection": "disciplines",
        "pipeline": [
            {"$unwind": "$technologies"},
            {"$group": {"_id": "$technologies", "uses": {"$sum": 1}}},
            {"$sort": {"uses": -1, "_id": 1}},
            {"$skip": 0},
            {"$limit": 10},
            {"$project": {"_id": 0, "technology": "$_id", "uses": 1}},
        ],
    },
    {
        "name": "Огляд дисциплін п'ятого семестру",
        "collection": "disciplines",
        "pipeline": [
            {"$match": {"semester": 5}},
            {
                "$lookup": {
                    "from": "laboratory_works",
                    "localField": "_id",
                    "foreignField": "courseId",
                    "as": "laboratoryWorks",
                }
            },
            {
                "$addFields": {
                    "laboratoryCount": {"$size": "$laboratoryWorks"},
                    "creditHours": {"$multiply": ["$credits", 30]},
                }
            },
            {
                "$project": {
                    "_id": 0,
                    "code": 1,
                    "name": 1,
                    "credits": 1,
                    "creditHours": 1,
                    "laboratoryCount": 1,
                }
            },
            {"$sort": {"laboratoryCount": -1, "code": 1}},
            {"$skip": 1},
            {"$limit": 5},
        ],
    },
    {
        "name": "Кількість робіт варіанта 5",
        "collection": "laboratory_works",
        "pipeline": [
            {"$match": {"variant": 5}},
            {"$count": "variant5Count"},
        ],
    },
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


def collect_keys(value: Any) -> set[str]:
    keys: set[str] = set()
    if isinstance(value, dict):
        for key, item in value.items():
            keys.add(key)
            keys.update(collect_keys(item))
    elif isinstance(value, list):
        for item in value:
            keys.update(collect_keys(item))
    return keys


def run_aggregations(database) -> tuple[list[dict[str, Any]], dict[str, list[str]]]:
    results: list[dict[str, Any]] = []
    stages: set[str] = set()
    functions: set[str] = set()
    aggregate_functions = {"$sum", "$avg", "$max", "$min", "$first", "$last"}

    for item in AGGREGATIONS:
        pipeline_keys = collect_keys(item["pipeline"])
        stages.update(key for key in pipeline_keys if key in {
            "$match", "$project", "$group", "$unwind", "$lookup",
            "$sort", "$limit", "$skip", "$addFields", "$count",
        })
        functions.update(pipeline_keys & aggregate_functions)
        documents = list(database[item["collection"]].aggregate(item["pipeline"]))
        if not documents:
            raise AssertionError(f"Агрегація '{item['name']}' не повернула результатів")
        results.append({
            "name": item["name"],
            "collection": item["collection"],
            "pipeline": json_safe(item["pipeline"]),
            "resultCount": len(documents),
            "documents": json_safe(documents),
        })

    required_stages = {
        "$match", "$project", "$group", "$unwind", "$lookup",
        "$sort", "$limit", "$skip", "$addFields", "$count",
    }
    required_functions = {"$sum", "$avg", "$max", "$min", "$first", "$last"}
    if stages != required_stages:
        raise AssertionError(f"Неповне покриття етапів: {sorted(required_stages - stages)}")
    if functions != required_functions:
        raise AssertionError(f"Неповне покриття функцій: {sorted(required_functions - functions)}")
    return results, {"stages": sorted(stages), "functions": sorted(functions)}


def operation_result(name: str, method: str, operator: str, result: Any) -> dict[str, Any]:
    return {
        "name": name,
        "method": method,
        "operator": operator,
        "matched": result.matched_count,
        "modified": result.modified_count,
        "upsertedId": str(result.upserted_id) if result.upserted_id else None,
    }


def run_updates(database) -> tuple[list[dict[str, Any]], list[dict[str, Any]]]:
    collection = database[SANDBOX_COLLECTION]
    collection.delete_many({"labMarker": LAB_MARKER})
    collection.insert_many([
        {"_id": "lab3-student-01", "labMarker": LAB_MARKER, "name": "Левченко Д. В.", "status": "new", "score": 70, "credits": 4, "tags": ["python", "mongodb"], "note": "temporary"},
        {"_id": "lab3-student-02", "labMarker": LAB_MARKER, "name": "Student 02", "status": "new", "score": 65, "credits": 3, "tags": ["nosql", "aggregation"], "note": "temporary"},
        {"_id": "lab3-student-03", "labMarker": LAB_MARKER, "name": "Student 03", "status": "new", "score": 60, "credits": 2, "tags": ["mongodb"], "note": "temporary"},
    ])

    operations: list[dict[str, Any]] = []
    result = collection.update_one({"_id": "lab3-student-01"}, {"$set": {"status": "active", "variant": 5}})
    operations.append(operation_result("Встановлення стану та варіанта", "update_one", "$set", result))

    result = collection.update_many({"labMarker": LAB_MARKER}, {"$inc": {"score": 5}, "$mul": {"credits": 1.5}})
    operations.append(operation_result("Перерахунок балів і кредитів", "update_many", "$inc + $mul", result))

    result = collection.update_one({"_id": "lab3-student-01"}, {"$unset": {"note": ""}})
    operations.append(operation_result("Видалення тимчасової примітки", "update_one", "$unset", result))

    result = collection.update_one({"_id": "lab3-student-01"}, {"$rename": {"status": "state"}})
    operations.append(operation_result("Перейменування поля стану", "update_one", "$rename", result))

    result = collection.update_one({"_id": "lab3-student-01"}, {"$push": {"tags": "visual-studio-code"}})
    operations.append(operation_result("Додавання елемента масиву", "update_one", "$push", result))

    result = collection.update_one({"_id": "lab3-student-02"}, {"$pop": {"tags": -1}})
    operations.append(operation_result("Видалення першого елемента масиву", "update_one", "$pop", result))

    replacement = {
        "_id": "lab3-student-03",
        "labMarker": LAB_MARKER,
        "name": "Student 03 replaced",
        "state": "archived",
        "score": 100,
        "credits": 6,
        "tags": ["replacement"],
        "variant": 5,
    }
    result = collection.replace_one({"_id": "lab3-student-03"}, replacement)
    operations.append(operation_result("Повна заміна документа", "replace_one", "replacement", result))

    required_methods = {"update_one", "update_many", "replace_one"}
    used_methods = {item["method"] for item in operations}
    required_operators = {"$set", "$unset", "$inc", "$mul", "$rename", "$push", "$pop"}
    used_operators = {
        token
        for item in operations
        for token in item["operator"].split(" + ")
        if token.startswith("$")
    }
    if not required_methods.issubset(used_methods):
        raise AssertionError(f"Не використано методи: {sorted(required_methods - used_methods)}")
    if not required_operators.issubset(used_operators):
        raise AssertionError(f"Не використано оператори: {sorted(required_operators - used_operators)}")

    documents = list(collection.find({"labMarker": LAB_MARKER}).sort("_id", 1))
    return operations, json_safe(documents)


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--uri", default=MONGO_URI)
    parser.add_argument("--database", default=DATABASE_NAME)
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()

    client = MongoClient(args.uri, serverSelectionTimeoutMS=5_000)
    client.admin.command("ping")
    database = client[args.database]
    required = {"disciplines", "laboratory_works", "students", "teachers"}
    missing = sorted(required - set(database.list_collection_names()))
    if missing:
        raise RuntimeError(f"У базі відсутні колекції: {', '.join(missing)}")

    aggregations, coverage = run_aggregations(database)
    updates, final_documents = run_updates(database)
    report = {
        "ok": True,
        "database": database.name,
        "variant": 5,
        "aggregationCount": len(aggregations),
        "aggregationCoverage": coverage,
        "aggregations": aggregations,
        "updateOperationCount": len(updates),
        "updateOperations": updates,
        "finalSandboxDocuments": final_documents,
    }

    text = json.dumps(report, ensure_ascii=False, indent=2)
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(text + "\n", encoding="utf-8")
    print(text)
    client.close()


if __name__ == "__main__":
    main()
