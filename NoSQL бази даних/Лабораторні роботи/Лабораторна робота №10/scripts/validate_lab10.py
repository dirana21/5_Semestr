import json
from pathlib import Path

from cassandra.cluster import Cluster


ROOT = Path(__file__).resolve().parents[1]
OUTPUT = ROOT / "results" / "lab10_results.json"
HOST = "127.0.0.1"
PORT = 9042
NETWORK_KS = "lab10_university_v5"
SIMPLE_KS = "lab10_simple_v5"


def rows(result):
    return [dict(row._asdict()) for row in result]


def main():
    cluster = Cluster([HOST], port=PORT, connect_timeout=10)
    session = cluster.connect()

    local = session.execute(
        "SELECT release_version, cql_version, data_center FROM system.local"
    ).one()
    keyspaces = rows(
        session.execute(
            """
            SELECT keyspace_name, replication, durable_writes
            FROM system_schema.keyspaces
            WHERE keyspace_name IN (%s, %s)
            """,
            (SIMPLE_KS, NETWORK_KS),
        )
    )
    tables = rows(
        session.execute(
            """
            SELECT table_name
            FROM system_schema.tables
            WHERE keyspace_name = %s
            """,
            (NETWORK_KS,),
        )
    )
    columns = rows(
        session.execute(
            """
            SELECT table_name, column_name, kind, position, type
            FROM system_schema.columns
            WHERE keyspace_name = %s
            """,
            (NETWORK_KS,),
        )
    )
    students = rows(session.execute(f"SELECT * FROM {NETWORK_KS}.students"))
    sensors = rows(
        session.execute(
            f"SELECT * FROM {NETWORK_KS}.sensor_readings WHERE sensor_id = %s",
            ("sensor-v5",),
        )
    )
    enrollments = rows(
        session.execute(
            f"""
            SELECT * FROM {NETWORK_KS}.course_enrollments
            WHERE faculty = %s AND group_code = %s
            """,
            ("FKS", "KN-31"),
        )
    )

    simple = next(x for x in keyspaces if x["keyspace_name"] == SIMPLE_KS)
    network = next(x for x in keyspaces if x["keyspace_name"] == NETWORK_KS)
    kinds = {(x["table_name"], x["column_name"]): x["kind"] for x in columns}
    table_names = {x["table_name"] for x in tables}

    checks = {
        "cassandraConnected": local is not None,
        "cassandraVersion509": str(local.release_version) == "5.0.9",
        "simpleKeyspaceCreated": simple["replication"].get("class", "").endswith("SimpleStrategy"),
        "networkKeyspaceCreated": network["replication"].get("class", "").endswith("NetworkTopologyStrategy"),
        "threeTablesCreated": table_names == {"students", "sensor_readings", "course_enrollments"},
        "simplePrimaryKey": kinds.get(("students", "student_id")) == "partition_key",
        "compoundPrimaryKey": kinds.get(("sensor_readings", "sensor_id")) == "partition_key" and kinds.get(("sensor_readings", "recorded_at")) == "clustering",
        "compositePartitionKey": kinds.get(("course_enrollments", "faculty")) == "partition_key" and kinds.get(("course_enrollments", "group_code")) == "partition_key" and kinds.get(("course_enrollments", "student_id")) == "clustering",
        "csvImported": len(students) == 5,
        "variantFiveImported": all(x["variant"] == 5 for x in students),
        "sensorRowsCreated": len(sensors) == 3,
        "enrollmentRowsCreated": len(enrollments) == 2,
    }
    if not all(checks.values()):
        raise RuntimeError(f"Lab 10 validation failed: {checks}")

    def convert(value):
        if hasattr(value, "isoformat"):
            return value.isoformat()
        return str(value)

    result = {
        "lab": 10,
        "variant": 5,
        "student": "Левченко Д. В.",
        "reviewer": "Андреєв П. І.",
        "cassandra": {
            "host": HOST,
            "port": PORT,
            "releaseVersion": str(local.release_version),
            "cqlVersion": str(local.cql_version),
            "dataCenter": str(local.data_center),
        },
        "keyspaces": keyspaces,
        "tables": sorted(table_names),
        "columns": columns,
        "students": students,
        "sensorReadings": sensors,
        "courseEnrollments": enrollments,
        "counts": {"students": len(students), "sensorReadings": len(sensors), "courseEnrollments": len(enrollments)},
        "checks": checks,
    }
    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    OUTPUT.write_text(
        json.dumps(result, ensure_ascii=False, indent=2, default=convert),
        encoding="utf-8",
    )
    print(json.dumps({"checks": checks, "counts": result["counts"]}, ensure_ascii=False, indent=2))
    cluster.shutdown()


if __name__ == "__main__":
    main()
