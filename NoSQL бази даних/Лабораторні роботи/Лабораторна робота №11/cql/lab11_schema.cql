DROP KEYSPACE IF EXISTS lab11_queries_v5;

CREATE KEYSPACE lab11_queries_v5
WITH replication = {
  'class': 'NetworkTopologyStrategy',
  'datacenter1': 1
};

USE lab11_queries_v5;

-- Простий ключ партиціювання.
CREATE TABLE users_by_id (
  user_id uuid PRIMARY KEY,
  full_name text,
  city text,
  age int,
  variant int
);

-- Partition key + дві clustering columns з різними напрямками сортування.
CREATE TABLE orders_by_user (
  user_id uuid,
  order_date date,
  order_id uuid,
  total decimal,
  status text,
  PRIMARY KEY (user_id, order_date, order_id)
) WITH CLUSTERING ORDER BY (order_date DESC, order_id ASC);

-- Композитний partition key і clustering columns.
CREATE TABLE activity_by_group (
  faculty text,
  group_code text,
  event_date date,
  event_id timeuuid,
  student_name text,
  action text,
  PRIMARY KEY ((faculty, group_code), event_date, event_id)
) WITH CLUSTERING ORDER BY (event_date DESC, event_id ASC);

CREATE INDEX idx_order_status_v5 ON orders_by_user (status);

