DROP KEYSPACE IF EXISTS lab12_python_v5;

CREATE KEYSPACE lab12_python_v5
WITH replication = {
  'class': 'NetworkTopologyStrategy',
  'datacenter1': 1
};

USE lab12_python_v5;

-- Події користувачів, зібрані з прикладних моделей MongoDB, Neo4j і Redis.
CREATE TABLE user_events (
  user_id uuid,
  event_time timeuuid,
  event_type text,
  event_data text,
  source text,
  related_lab int,
  PRIMARY KEY (user_id, event_time)
) WITH CLUSTERING ORDER BY (event_time DESC);

-- Історія змін документів.
CREATE TABLE document_history (
  document_id uuid,
  changed_at timeuuid,
  change_id uuid,
  actor text,
  change_type text,
  previous_data text,
  new_data text,
  source_model text,
  PRIMARY KEY (document_id, changed_at)
) WITH CLUSTERING ORDER BY (changed_at DESC);

