DROP KEYSPACE IF EXISTS lab10_simple_v5;
DROP KEYSPACE IF EXISTS lab10_university_v5;

CREATE KEYSPACE lab10_simple_v5
WITH replication = {
  'class': 'SimpleStrategy',
  'replication_factor': 1
};

CREATE KEYSPACE lab10_university_v5
WITH replication = {
  'class': 'NetworkTopologyStrategy',
  'datacenter1': 1
};

USE lab10_university_v5;

CREATE TABLE students (
  student_id uuid PRIMARY KEY,
  full_name text,
  email text,
  variant int,
  city text
);

CREATE TABLE sensor_readings (
  sensor_id text,
  recorded_at timestamp,
  temperature double,
  room text,
  PRIMARY KEY (sensor_id, recorded_at)
) WITH CLUSTERING ORDER BY (recorded_at DESC);

CREATE TABLE course_enrollments (
  faculty text,
  group_code text,
  student_id uuid,
  course text,
  semester int,
  grade double,
  PRIMARY KEY ((faculty, group_code), student_id)
);

INSERT INTO sensor_readings (sensor_id, recorded_at, temperature, room)
VALUES ('sensor-v5', '2026-11-17T09:00:00Z', 21.5, 'A-101');
INSERT INTO sensor_readings (sensor_id, recorded_at, temperature, room)
VALUES ('sensor-v5', '2026-11-17T10:00:00Z', 22.1, 'A-101');
INSERT INTO sensor_readings (sensor_id, recorded_at, temperature, room)
VALUES ('sensor-v5', '2026-11-17T11:00:00Z', 22.8, 'A-101');

INSERT INTO course_enrollments
  (faculty, group_code, student_id, course, semester, grade)
VALUES
  ('FKS', 'KN-31', 50000000-0000-0000-0000-000000000001,
   'NoSQL бази даних', 5, 95.0);
INSERT INTO course_enrollments
  (faculty, group_code, student_id, course, semester, grade)
VALUES
  ('FKS', 'KN-31', 50000000-0000-0000-0000-000000000002,
   'NoSQL бази даних', 5, 91.0);

