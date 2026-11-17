import json
from pathlib import Path
from uuid import UUID, uuid1, uuid4

from cassandra.cluster import Cluster
from cassandra.query import dict_factory


ROOT = Path(__file__).resolve().parents[1]
SCHEMA = ROOT / "cql" / "lab12_schema.cql"
OUTPUT = ROOT / "results" / "lab12_results.json"
KEYSPACE = "lab12_python_v5"
USER_ID = UUID("50000000-0000-0000-0000-000000000001")
DOCUMENT_ID = UUID("52000000-0000-0000-0000-000000000005")


def split_cql(text):
    current = []
    for raw in text.splitlines():
        line = raw.strip()
        if not line or line.startswith("--"):
            continue
        current.append(raw)
        if line.endswith(";"):
            yield "\n".join(current).rstrip(";\n ")
            current = []


def create_event(session, user_id, event_type, event_data, source, related_lab):
    event_time = uuid1()
    statement = session.prepare(
        "INSERT INTO user_events "
        "(user_id, event_time, event_type, event_data, source, related_lab) "
        "VALUES (?, ?, ?, ?, ?, ?)"
    )
    session.execute(statement, (user_id, event_time, event_type, json.dumps(event_data, ensure_ascii=False), source, related_lab))
    return event_time


def read_events(session, user_id, limit=100):
    statement = session.prepare(
        "SELECT user_id, event_time, event_type, event_data, source, related_lab "
        "FROM user_events WHERE user_id = ? LIMIT ?"
    )
    return list(session.execute(statement, (user_id, limit)))


def update_event_source(session, user_id, event_time, new_source):
    statement = session.prepare(
        "UPDATE user_events SET source = ? WHERE user_id = ? AND event_time = ?"
    )
    session.execute(statement, (new_source, user_id, event_time))


def delete_event(session, user_id, event_time):
    statement = session.prepare(
        "DELETE FROM user_events WHERE user_id = ? AND event_time = ?"
    )
    session.execute(statement, (user_id, event_time))


cluster = Cluster(["127.0.0.1"], port=9042)
try:
    session = cluster.connect()
    for statement in split_cql(SCHEMA.read_text(encoding="utf-8")):
        session.execute(statement)
    session.set_keyspace(KEYSPACE)
    session.row_factory = dict_factory

    sources = [
        ("MongoDB", 3, "document_view", {"collection": "students", "document": "variant-5"}),
        ("Neo4j", 8, "relationship_open", {"node": "Levchenko", "relation": "PERFORMS"}),
        ("Redis", 6, "cache_hit", {"key": "student:variant:5", "ttl": 300}),
        ("Cassandra", 11, "cql_query", {"table": "orders_by_user", "rows": 5}),
    ]
    created_times = []
    for i in range(21):
        source, lab, event_type, payload = sources[i % len(sources)]
        data = dict(payload); data["sequence"] = i + 1; data["variant"] = 5
        created_times.append(create_event(session, USER_ID, event_type, data, source, lab))

    history_insert = session.prepare(
        "INSERT INTO document_history "
        "(document_id, changed_at, change_id, actor, change_type, previous_data, new_data, source_model) "
        "VALUES (?, ?, ?, ?, ?, ?, ?, ?)"
    )
    for i in range(10):
        previous = {"version": i, "status": "draft" if i < 5 else "review"}
        current = {"version": i + 1, "status": "review" if i < 5 else "approved"}
        session.execute(history_insert, (
            DOCUMENT_ID, uuid1(), uuid4(), "Левченко Д. В.", "UPDATE",
            json.dumps(previous, ensure_ascii=False), json.dumps(current, ensure_ascii=False),
            ["MongoDB", "Neo4j", "Redis"][i % 3],
        ))

    before = read_events(session, USER_ID)
    updated_time = created_times[0]
    deleted_time = created_times[-1]
    update_event_source(session, USER_ID, updated_time, "Python CRUD v5")
    delete_event(session, USER_ID, deleted_time)
    after = read_events(session, USER_ID)

    updated_row = session.execute(
        "SELECT * FROM user_events WHERE user_id = %s AND event_time = %s",
        (USER_ID, updated_time),
    ).one()
    deleted_row = session.execute(
        "SELECT * FROM user_events WHERE user_id = %s AND event_time = %s",
        (USER_ID, deleted_time),
    ).one()
    history = list(session.execute(
        "SELECT * FROM document_history WHERE document_id = %s", (DOCUMENT_ID,)
    ))

    result = {
        "lab": 12,
        "variant": 5,
        "student": "Левченко Д. В.",
        "reviewer": "Андреєв П. І.",
        "connection": {"host": "127.0.0.1", "port": 9042, "keyspace": KEYSPACE},
        "crud": {
            "createdEvents": len(before),
            "readReturnedDictionaries": isinstance(before[0], dict),
            "updatedEventTime": str(updated_time),
            "updatedSource": updated_row["source"],
            "deletedEventTime": str(deleted_time),
            "deleteConfirmed": deleted_row is None,
            "remainingEvents": len(after),
            "historyRows": len(history),
        },
        "sourceModels": sorted({row["source"] for row in after}),
        "sampleEvents": [
            {
                "event_time": str(row["event_time"]),
                "event_type": row["event_type"],
                "source": row["source"],
                "related_lab": row["related_lab"],
            }
            for row in after[:6]
        ],
        "sampleHistory": [
            {
                "changed_at": str(row["changed_at"]),
                "change_type": row["change_type"],
                "source_model": row["source_model"],
            }
            for row in history[:4]
        ],
    }
    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    OUTPUT.write_text(json.dumps(result, ensure_ascii=False, indent=2), encoding="utf-8")
    print(json.dumps(result["crud"], ensure_ascii=False, indent=2))
finally:
    cluster.shutdown()

