import json
import os
import statistics
import time
from datetime import datetime
from pathlib import Path

from neo4j import GraphDatabase


ROOT = Path(__file__).resolve().parents[1]
RESULTS_PATH = ROOT / "results" / "lab8_results.json"
URI = os.getenv("NEO4J_URI", "bolt://127.0.0.1:7687")
USER = os.getenv("NEO4J_USER")
PASSWORD = os.getenv("NEO4J_PASSWORD")
AUTH = (USER, PASSWORD) if USER and PASSWORD else None
MARKER = "nosql-lab8-variant5"
INDEX_NAME = "search_sample_code_idx"
SAMPLE_COUNT = 500
TARGET_CODE = "sample-0420"


SEARCH_QUERY = """
MATCH (sample:SearchSample {code: $code})
RETURN sample.code AS code,
       sample.category AS category,
       sample.score AS score
"""


def plan_to_dict(plan):
    if plan is None:
        return None
    if isinstance(plan, dict):
        return {
            "operator": plan.get("operatorType") or plan.get("operator"),
            "identifiers": sorted(plan.get("identifiers") or []),
            "arguments": dict(plan.get("args") or plan.get("arguments") or {}),
            "dbHits": plan.get("dbHits", 0),
            "records": plan.get("records", 0),
            "children": [plan_to_dict(child) for child in plan.get("children") or []],
        }
    result = {
        "operator": plan.operator_type,
        "identifiers": sorted(plan.identifiers),
        "arguments": dict(plan.arguments),
        "children": [plan_to_dict(child) for child in plan.children],
    }
    if hasattr(plan, "db_hits"):
        result["dbHits"] = plan.db_hits
    if hasattr(plan, "records"):
        result["records"] = plan.records
    return result


def flatten_operators(plan):
    if not plan:
        return []
    return [plan["operator"]] + [name for child in plan["children"] for name in flatten_operators(child)]


def total_db_hits(plan):
    if not plan:
        return 0
    return int(plan.get("dbHits") or 0) + sum(total_db_hits(child) for child in plan["children"])


def profile_query(session, code):
    result = session.run("PROFILE " + SEARCH_QUERY, code=code)
    records = [record.data() for record in result]
    summary = result.consume()
    profile = plan_to_dict(summary.profile)
    return {
        "records": records,
        "plan": profile,
        "operators": flatten_operators(profile),
        "totalDbHits": total_db_hits(profile),
    }


def explain_query(session, code):
    result = session.run("EXPLAIN " + SEARCH_QUERY, code=code)
    summary = result.consume()
    plan = plan_to_dict(summary.plan)
    return {"plan": plan, "operators": flatten_operators(plan)}


def benchmark(session, code, iterations=120):
    samples = []
    for _ in range(iterations):
        started = time.perf_counter_ns()
        session.run(SEARCH_QUERY, code=code).consume()
        samples.append((time.perf_counter_ns() - started) / 1_000_000)
    return {
        "iterations": iterations,
        "medianMs": round(statistics.median(samples), 4),
        "averageMs": round(statistics.mean(samples), 4),
        "minMs": round(min(samples), 4),
        "maxMs": round(max(samples), 4),
    }


def run():
    driver = GraphDatabase.driver(URI, auth=AUTH)
    driver.verify_connectivity()

    with driver.session(database="neo4j") as session:
        base_counts = session.run(
            """
            MATCH (lab:LaboratoryWork)
            RETURN count(lab) AS laboratoryWorks,
                   count(CASE WHEN lab.variant = 5 THEN 1 END) AS variantFiveLabs
            """
        ).single().data()
        if base_counts["laboratoryWorks"] < 7:
            raise RuntimeError("Спочатку потрібно виконати лабораторну роботу №7")

        session.run(f"DROP INDEX {INDEX_NAME} IF EXISTS").consume()
        session.run(
            "MATCH (sample:SearchSample {labMarker: $marker}) DETACH DELETE sample",
            marker=MARKER,
        ).consume()

        session.run(
            """
            UNWIND range(1, $sampleCount) AS value
            MATCH (lab:LaboratoryWork {number: ((value - 1) % 7) + 1})
            CREATE (sample:SearchSample {
                code: 'sample-' + right('0000' + toString(value), 4),
                category: CASE WHEN value % 2 = 0 THEN 'even' ELSE 'odd' END,
                score: value,
                variant: 5,
                labMarker: $marker
            })
            CREATE (sample)-[:REFERS_TO]->(lab)
            """,
            sampleCount=SAMPLE_COUNT,
            marker=MARKER,
        ).consume()

        sample_counts = session.run(
            """
            MATCH (sample:SearchSample {labMarker: $marker})
            OPTIONAL MATCH (sample)-[r:REFERS_TO]->(:LaboratoryWork)
            RETURN count(DISTINCT sample) AS nodes, count(r) AS relationships
            """,
            marker=MARKER,
        ).single().data()

        technology_usage = [record.data() for record in session.run(
            """
            MATCH (lab:LaboratoryWork)-[:USES]->(technology:Technology)
            RETURN technology.name AS technology, count(lab) AS laboratoryCount
            ORDER BY laboratoryCount DESC, technology
            """
        )]
        node_degrees = [record.data() for record in session.run(
            """
            MATCH (lab:LaboratoryWork)
            OPTIONAL MATCH (lab)-[relationship]-()
            RETURN lab.number AS laboratoryNumber, lab.title AS title,
                   count(relationship) AS degree
            ORDER BY degree DESC, laboratoryNumber
            """
        )]
        shortest_path = session.run(
            """
            MATCH path=shortestPath(
                (:Student {studentId: 'student-variant-5'})-[*..6]-(:Technology {name: 'Neo4j'})
            )
            RETURN length(path) AS length,
                   [node IN nodes(path) |
                       coalesce(node.name, node.title, node.studentId, toString(node.number))
                   ] AS nodes,
                   [relationship IN relationships(path) | type(relationship)] AS relationships
            """
        ).single().data()

        before_profile = profile_query(session, TARGET_CODE)
        before_benchmark = benchmark(session, TARGET_CODE)

        session.run(
            f"CREATE INDEX {INDEX_NAME} IF NOT EXISTS FOR (sample:SearchSample) ON (sample.code)"
        ).consume()
        session.run("CALL db.awaitIndexes(30)").consume()

        after_explain = explain_query(session, TARGET_CODE)
        after_profile = profile_query(session, TARGET_CODE)
        after_benchmark = benchmark(session, TARGET_CODE)
        index_state = session.run(
            """
            SHOW INDEXES YIELD name, state, type, labelsOrTypes, properties
            WHERE name = $indexName
            RETURN name, state, type, labelsOrTypes, properties
            """,
            indexName=INDEX_NAME,
        ).single().data()

    driver.close()

    before_scan = any("NodeByLabelScan" in operator for operator in before_profile["operators"])
    after_seek = any("IndexSeek" in operator for operator in after_profile["operators"])
    checks = {
        "neo4jConnected": True,
        "previousGraphLoaded": base_counts["laboratoryWorks"] >= 7,
        "variantFiveLoaded": base_counts["variantFiveLabs"] >= 7,
        "analysisDatasetCreated": sample_counts["nodes"] == SAMPLE_COUNT,
        "analysisRelationshipsCreated": sample_counts["relationships"] == SAMPLE_COUNT,
        "searchResultCorrect": after_profile["records"] == [
            {"code": TARGET_CODE, "category": "even", "score": 420}
        ],
        "beforeUsesLabelScan": before_scan,
        "afterUsesIndexSeek": after_seek,
        "indexOnline": index_state["state"] == "ONLINE",
        "indexReducesDbHits": after_profile["totalDbHits"] < before_profile["totalDbHits"],
        "shortestPathFound": shortest_path["length"] == 2,
    }

    result = {
        "ok": all(checks.values()),
        "laboratoryWork": 8,
        "variant": 5,
        "student": "Левченко Д. В.",
        "reviewer": "Андреєв П. І.",
        "generatedAt": datetime.now().isoformat(timespec="seconds"),
        "neo4j": {"uri": URI, "database": "neo4j"},
        "baseGraph": base_counts,
        "analysisDataset": {**sample_counts, "targetCode": TARGET_CODE},
        "technologyUsage": technology_usage,
        "nodeDegrees": node_degrees,
        "shortestPath": shortest_path,
        "indexAnalysis": {
            "index": index_state,
            "before": {"profile": before_profile, "benchmark": before_benchmark},
            "after": {
                "explain": after_explain,
                "profile": after_profile,
                "benchmark": after_benchmark,
            },
        },
        "checks": checks,
    }
    RESULTS_PATH.parent.mkdir(parents=True, exist_ok=True)
    RESULTS_PATH.write_text(json.dumps(result, ensure_ascii=False, indent=2), encoding="utf-8")
    print(json.dumps(result, ensure_ascii=False, indent=2))
    if not result["ok"]:
        raise SystemExit(1)


if __name__ == "__main__":
    run()
