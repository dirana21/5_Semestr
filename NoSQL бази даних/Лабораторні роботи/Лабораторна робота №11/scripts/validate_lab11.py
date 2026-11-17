import json
from pathlib import Path
from uuid import UUID

from cassandra.cluster import Cluster


ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "results" / "lab11_results.json"
KEYSPACE = "lab11_queries_v5"
USER_ID = UUID("50000000-0000-0000-0000-000000000001")

cluster = Cluster(["127.0.0.1"], port=9042)
session = cluster.connect(KEYSPACE)

release = session.execute("SELECT release_version, cql_version, data_center FROM system.local").one()
counts = {
    "users": session.execute("SELECT COUNT(*) FROM users_by_id").one()[0],
    "orders": session.execute("SELECT COUNT(*) FROM orders_by_user").one()[0],
    "activity": session.execute("SELECT COUNT(*) FROM activity_by_group").one()[0],
}

full_key = list(session.execute("SELECT * FROM orders_by_user WHERE user_id = %s", (USER_ID,)))
composite_key = list(session.execute(
    "SELECT * FROM activity_by_group WHERE faculty = 'FKS' AND group_code = 'KN-31'"
))
partial_key = list(session.execute(
    "SELECT * FROM activity_by_group WHERE faculty = 'FKS' ALLOW FILTERING"
))
without_key = list(session.execute(
    "SELECT * FROM users_by_id WHERE city = 'Кременчук' ALLOW FILTERING"
))
ordered = list(session.execute(
    "SELECT order_date, order_id, status, total FROM orders_by_user "
    "WHERE user_id = %s ORDER BY order_date DESC, order_id ASC", (USER_ID,)
))
indexed = list(session.execute("SELECT * FROM orders_by_user WHERE status = 'completed'"))

trace_future = session.execute_async(
    "SELECT * FROM orders_by_user WHERE user_id = %s LIMIT 5", (USER_ID,), trace=True
)
traced_rows = list(trace_future.result())
trace = trace_future.get_query_trace(max_wait=10)
events = list(trace.events) if trace else []

index_rows = list(session.execute(
    "SELECT index_name, kind FROM system_schema.indexes "
    "WHERE keyspace_name = 'lab11_queries_v5' AND table_name = 'orders_by_user'"
))
dates = [str(row.order_date) for row in ordered]
checks = {
    "cassandraConnected": release is not None,
    "cassandraVersion509": release.release_version == "5.0.9",
    "threeTablesHave25Rows": all(value == 25 for value in counts.values()),
    "fullPartitionKeyQuery": len(full_key) == 5,
    "fullCompositeKeyQuery": len(composite_key) == 10,
    "partialPartitionKeyFiltering": len(partial_key) == 15,
    "withoutPartitionKeyFiltering": len(without_key) == 5,
    "clusteringOrderDescending": dates == sorted(dates, reverse=True),
    "secondaryIndexCreated": any(row.index_name == "idx_order_status_v5" for row in index_rows),
    "secondaryIndexQuery": len(indexed) == 10,
    "queryTracingEnabled": trace is not None and len(events) > 0,
    "tracedQueryReturnedRows": len(traced_rows) == 5,
}

result = {
    "lab": 11,
    "variant": 5,
    "student": "Левченко Д. В.",
    "reviewer": "Андреєв П. І.",
    "cassandra": {
        "releaseVersion": release.release_version,
        "cqlVersion": release.cql_version,
        "dataCenter": release.data_center,
    },
    "counts": counts,
    "queryResults": {
        "fullPartitionKeyRows": len(full_key),
        "fullCompositeKeyRows": len(composite_key),
        "partialPartitionKeyRows": len(partial_key),
        "withoutPartitionKeyRows": len(without_key),
        "indexedStatusRows": len(indexed),
        "orderedDates": dates,
    },
    "tracing": {
        "traceId": str(trace.trace_id) if trace else None,
        "coordinator": str(trace.coordinator) if trace else None,
        "durationMicros": int(trace.duration.total_seconds() * 1_000_000) if trace and trace.duration else None,
        "eventCount": len(events),
        "sampleEvents": [event.description for event in events[:8]],
    },
    "indexes": [{"name": row.index_name, "kind": row.kind} for row in index_rows],
    "checks": checks,
}
OUT.parent.mkdir(parents=True, exist_ok=True)
OUT.write_text(json.dumps(result, ensure_ascii=False, indent=2), encoding="utf-8")
print(json.dumps({"checks": checks, "counts": counts, "tracingEvents": len(events)}, ensure_ascii=False, indent=2))

cluster.shutdown()
if not all(checks.values()):
    raise SystemExit(1)

