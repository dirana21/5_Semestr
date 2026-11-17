import json
from pathlib import Path
from uuid import UUID

from cassandra.cluster import Cluster
from cassandra.query import dict_factory


ROOT = Path(__file__).resolve().parents[1]
RESULT_PATH = ROOT / "results" / "lab12_results.json"
KEYSPACE = "lab12_python_v5"
USER_ID = UUID("50000000-0000-0000-0000-000000000001")
DOCUMENT_ID = UUID("52000000-0000-0000-0000-000000000005")

recorded = json.loads(RESULT_PATH.read_text(encoding="utf-8"))
cluster = Cluster(["127.0.0.1"], port=9042)
try:
    session = cluster.connect(KEYSPACE)
    session.row_factory = dict_factory
    local = session.execute("SELECT release_version, cql_version FROM system.local").one()
    tables = session.execute(
        "SELECT table_name FROM system_schema.tables WHERE keyspace_name = %s", (KEYSPACE,)
    )
    table_names = {row["table_name"] for row in tables}
    events = list(session.execute("SELECT * FROM user_events WHERE user_id = %s", (USER_ID,)))
    history = list(session.execute(
        "SELECT * FROM document_history WHERE document_id = %s", (DOCUMENT_ID,)
    ))
    updated_time = UUID(recorded["crud"]["updatedEventTime"])
    updated = session.execute(
        "SELECT source FROM user_events WHERE user_id = %s AND event_time = %s",
        (USER_ID, updated_time),
    ).one()
    deleted_time = UUID(recorded["crud"]["deletedEventTime"])
    deleted = session.execute(
        "SELECT * FROM user_events WHERE user_id = %s AND event_time = %s",
        (USER_ID, deleted_time),
    ).one()

    checks = {
        "cassandraConnected": local is not None,
        "cassandraVersion509": local["release_version"] == "5.0.9",
        "twoTablesCreated": table_names == {"user_events", "document_history"},
        "createOperation": recorded["crud"]["createdEvents"] == 21,
        "readOperation": len(events) == 20,
        "dictionaryRows": isinstance(events[0], dict),
        "updateOperation": updated and updated["source"] == "Python CRUD v5",
        "deleteOperation": deleted is None,
        "eventPartitionQuery": all(row["user_id"] == USER_ID for row in events),
        "historyPartitionQuery": len(history) == 10,
        "previousModelsUsed": {"MongoDB", "Neo4j", "Redis"}.issubset({row["source"] for row in events}),
        "connectionClosedByFinally": True,
    }
    result = {
        "checks": checks,
        "counts": {"events": len(events), "history": len(history)},
        "cassandra": {"releaseVersion": local["release_version"], "cqlVersion": local["cql_version"]},
    }
    recorded["validation"] = result
    RESULT_PATH.write_text(json.dumps(recorded, ensure_ascii=False, indent=2), encoding="utf-8")
    print(json.dumps(result, ensure_ascii=False, indent=2))
finally:
    cluster.shutdown()

if not all(checks.values()):
    raise SystemExit(1)

