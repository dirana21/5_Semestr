import json
import os
from datetime import datetime
from pathlib import Path

from neo4j import GraphDatabase


ROOT = Path(__file__).resolve().parents[1]
RESULTS_PATH = ROOT / "results" / "lab7_results.json"
URI = os.getenv("NEO4J_URI", "bolt://127.0.0.1:7687")
USER = os.getenv("NEO4J_USER")
PASSWORD = os.getenv("NEO4J_PASSWORD")
AUTH = (USER, PASSWORD) if USER and PASSWORD else None
MARKER = "nosql-lab7-variant5"


SCHEMA_QUERIES = [
    "CREATE CONSTRAINT student_id_unique IF NOT EXISTS FOR (n:Student) REQUIRE n.studentId IS UNIQUE",
    "CREATE CONSTRAINT course_code_unique IF NOT EXISTS FOR (n:Course) REQUIRE n.code IS UNIQUE",
    "CREATE CONSTRAINT lab_number_unique IF NOT EXISTS FOR (n:LaboratoryWork) REQUIRE n.number IS UNIQUE",
    "CREATE CONSTRAINT technology_name_unique IF NOT EXISTS FOR (n:Technology) REQUIRE n.name IS UNIQUE",
    "CREATE CONSTRAINT tool_name_unique IF NOT EXISTS FOR (n:Tool) REQUIRE n.name IS UNIQUE",
    "CREATE INDEX lab_title_idx IF NOT EXISTS FOR (n:LaboratoryWork) ON (n.title)",
    "CREATE INDEX lab_status_idx IF NOT EXISTS FOR (n:LaboratoryWork) ON (n.status)",
]


def records_as_dicts(result):
    return [record.data() for record in result]


def run():
    driver = GraphDatabase.driver(URI, auth=AUTH)
    driver.verify_connectivity()

    with driver.session(database="neo4j") as session:
        session.run(
            "MATCH (n {labMarker: $marker}) DETACH DELETE n",
            marker=MARKER,
        ).consume()

        for query in SCHEMA_QUERIES:
            session.run(query).consume()

        session.run(
            """
            MERGE (student:Student {studentId: 'student-variant-5'})
            SET student.name = 'Левченко Д. В.',
                student.variant = 5,
                student.labMarker = $marker
            MERGE (course:Course {code: 'NOSQL'})
            SET course.title = 'NoSQL бази даних',
                course.labMarker = $marker
            MERGE (city:City {name: 'Кременчук'})
            SET city.country = 'Україна',
                city.labMarker = $marker
            MERGE (student)-[:STUDIES {semester: 5}]->(course)
            MERGE (student)-[:LOCATED_IN]->(city)
            """,
            marker=MARKER,
        ).consume()

        session.run(
            """
            LOAD CSV WITH HEADERS FROM 'file:///lab7_labs.csv' AS row
            WITH row, toInteger(row.number) AS labNumber
            MERGE (lab:LaboratoryWork {number: labNumber})
            SET lab.title = row.title,
                lab.status = row.status,
                lab.variant = 5,
                lab.labMarker = $marker
            MERGE (technology:Technology {name: row.technology})
            SET technology.labMarker = $marker
            MERGE (tool:Tool {name: row.tool})
            SET tool.labMarker = $marker
            MERGE (course:Course {code: 'NOSQL'})
            MERGE (student:Student {studentId: 'student-variant-5'})
            MERGE (course)-[:INCLUDES]->(lab)
            MERGE (student)-[:COMPLETED {result: 'зараховано'}]->(lab)
            MERGE (lab)-[:USES]->(technology)
            MERGE (lab)-[:PERFORMED_IN]->(tool)
            """,
            marker=MARKER,
        ).consume()

        session.run(
            """
            MATCH (previous:LaboratoryWork), (current:LaboratoryWork)
            WHERE current.number = previous.number + 1
              AND previous.number >= 1 AND current.number <= 7
            MERGE (current)-[:EXTENDS]->(previous)
            """
        ).consume()

        counts = session.run(
            """
            MATCH (n {labMarker: $marker})
            WITH count(n) AS nodes
            MATCH ()-[r]->()
            WHERE startNode(r).labMarker = $marker AND endNode(r).labMarker = $marker
            RETURN nodes, count(r) AS relationships
            """,
            marker=MARKER,
        ).single().data()

        labels = records_as_dicts(
            session.run(
                "MATCH (n {labMarker: $marker}) UNWIND labels(n) AS label RETURN label, count(*) AS count ORDER BY label",
                marker=MARKER,
            )
        )
        relationship_types = records_as_dicts(
            session.run(
                """
                MATCH (a {labMarker: $marker})-[r]->(b {labMarker: $marker})
                RETURN type(r) AS type, count(*) AS count ORDER BY type
                """,
                marker=MARKER,
            )
        )
        laboratories = records_as_dicts(
            session.run(
                """
                MATCH (student:Student)-[:COMPLETED]->(lab:LaboratoryWork)-[:USES]->(technology:Technology)
                RETURN lab.number AS number, lab.title AS title, technology.name AS technology
                ORDER BY number
                """
            )
        )
        route = session.run(
            """
            MATCH path=(last:LaboratoryWork {number: 7})-[:EXTENDS*]->(first:LaboratoryWork {number: 1})
            RETURN [node IN nodes(path) | node.number] AS labNumbers, length(path) AS length
            """
        ).single().data()
        constraints = records_as_dicts(
            session.run(
                "SHOW CONSTRAINTS YIELD name, type, labelsOrTypes, properties RETURN name, type, labelsOrTypes, properties ORDER BY name"
            )
        )
        indexes = records_as_dicts(
            session.run(
                "SHOW INDEXES YIELD name, type, entityType, labelsOrTypes, properties, state RETURN name, type, entityType, labelsOrTypes, properties, state ORDER BY name"
            )
        )

    driver.close()

    checks = {
        "neo4jConnected": True,
        "csvImportedSevenLabs": len(laboratories) == 7,
        "variantFiveApplied": all(item["number"] in range(1, 8) for item in laboratories),
        "graphNodeCount": counts["nodes"] == 16,
        "graphRelationshipCount": counts["relationships"] == 36,
        "uniqueConstraintsCreated": len([c for c in constraints if "UNIQUENESS" in c["type"]]) >= 5,
        "searchIndexesOnline": all(i["state"] == "ONLINE" for i in indexes),
        "extensionPathComplete": route["labNumbers"] == [7, 6, 5, 4, 3, 2, 1],
    }

    result = {
        "ok": all(checks.values()),
        "laboratoryWork": 7,
        "variant": 5,
        "student": "Левченко Д. В.",
        "reviewer": "Андреєв П. І.",
        "generatedAt": datetime.now().isoformat(timespec="seconds"),
        "neo4j": {"uri": URI, "database": "neo4j", **counts},
        "labels": labels,
        "relationshipTypes": relationship_types,
        "laboratories": laboratories,
        "extensionPath": route,
        "constraints": constraints,
        "indexes": indexes,
        "checks": checks,
    }
    RESULTS_PATH.parent.mkdir(parents=True, exist_ok=True)
    RESULTS_PATH.write_text(json.dumps(result, ensure_ascii=False, indent=2), encoding="utf-8")
    print(json.dumps(result, ensure_ascii=False, indent=2))
    if not result["ok"]:
        raise SystemExit(1)


if __name__ == "__main__":
    run()
