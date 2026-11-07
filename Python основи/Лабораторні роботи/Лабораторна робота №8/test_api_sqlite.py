"""Автоматичні тести потокових HTTP-запитів і SQLite."""

import json
import sqlite3
import tempfile
import unittest
from pathlib import Path
from unittest.mock import MagicMock, patch

from api_sqlite import (
    ApiRecord,
    ApiRequestError,
    ApiTask,
    build_tasks,
    fetch_json,
    initialize_database,
    normalize_record,
    read_records,
    replace_records,
    run_in_threads,
)


class ApiSqliteTests(unittest.TestCase):
    def setUp(self) -> None:
        self.temp_directory = tempfile.TemporaryDirectory(ignore_cleanup_errors=True)
        self.database_path = Path(self.temp_directory.name) / "test.db"

    def tearDown(self) -> None:
        self.temp_directory.cleanup()

    def test_api_task_normalizes_method(self) -> None:
        self.assertEqual(ApiTask("get", "https://example.com").method, "GET")

    def test_api_task_rejects_unsupported_method(self) -> None:
        with self.assertRaises(ValueError):
            ApiTask("DELETE", "https://example.com")

    def test_build_tasks_contains_get_and_post(self) -> None:
        self.assertEqual([task.method for task in build_tasks()], ["GET", "POST"])

    @patch("api_sqlite.urlopen")
    def test_fetch_json_decodes_response(self, mocked_urlopen: MagicMock) -> None:
        response = MagicMock()
        response.read.return_value = json.dumps({"id": 1, "title": "Test"}).encode()
        mocked_urlopen.return_value.__enter__.return_value = response
        self.assertEqual(fetch_json(ApiTask("GET", "https://example.com"))["id"], 1)

    @patch("api_sqlite.urlopen")
    def test_fetch_json_rejects_array_response(self, mocked_urlopen: MagicMock) -> None:
        response = MagicMock()
        response.read.return_value = b"[1, 2]"
        mocked_urlopen.return_value.__enter__.return_value = response
        with self.assertRaises(ApiRequestError):
            fetch_json(ApiTask("GET", "https://example.com"))

    def test_empty_task_list_returns_empty_result(self) -> None:
        self.assertEqual(run_in_threads([]), [])

    def test_invalid_worker_count_is_rejected(self) -> None:
        with self.assertRaises(ValueError):
            run_in_threads([ApiTask("GET", "https://example.com")], max_workers=0)

    @patch("api_sqlite.fetch_json")
    def test_thread_results_keep_task_order(self, mocked_fetch: MagicMock) -> None:
        mocked_fetch.side_effect = lambda task: {"title": task.method}
        tasks = [ApiTask("GET", "https://a"), ApiTask("POST", "https://b", {})]
        self.assertEqual(run_in_threads(tasks), [{"title": "GET"}, {"title": "POST"}])

    def test_normalize_record_extracts_fields(self) -> None:
        record = normalize_record(
            ApiTask("GET", "https://example.com"),
            {"id": 7, "title": "Title", "body": "Body"},
        )
        self.assertEqual(record, ApiRecord("GET", "https://example.com", 7, "Title", "Body"))

    def test_normalize_record_rejects_invalid_id(self) -> None:
        with self.assertRaises(ApiRequestError):
            normalize_record(ApiTask("GET", "https://example.com"), {"id": "1"})

    def test_initialize_database_creates_table(self) -> None:
        with sqlite3.connect(self.database_path) as connection:
            initialize_database(connection)
            table = connection.execute(
                "SELECT name FROM sqlite_master WHERE type='table' AND name='api_records'"
            ).fetchone()
        self.assertEqual(table, ("api_records",))

    def test_replace_and_read_records(self) -> None:
        records = [ApiRecord("GET", "https://a", 1, "A", "Body A")]
        replace_records(self.database_path, records)
        self.assertEqual(read_records(self.database_path), records)

    def test_replace_records_removes_old_rows(self) -> None:
        replace_records(self.database_path, [ApiRecord("GET", "https://a", 1, "A", "")])
        replacement = [ApiRecord("POST", "https://b", 101, "B", "")]
        replace_records(self.database_path, replacement)
        self.assertEqual(read_records(self.database_path), replacement)

    def test_database_preserves_record_order(self) -> None:
        records = [
            ApiRecord("GET", "https://a", 1, "A", ""),
            ApiRecord("POST", "https://b", 101, "B", ""),
        ]
        replace_records(self.database_path, records)
        self.assertEqual(read_records(self.database_path), records)

    def test_read_missing_database_raises_error(self) -> None:
        with self.assertRaises(FileNotFoundError):
            read_records(self.database_path)


if __name__ == "__main__":
    unittest.main(verbosity=2)
