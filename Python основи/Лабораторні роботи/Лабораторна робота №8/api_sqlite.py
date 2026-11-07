"""Лабораторна робота №8: HTTP-запити в потоках і збереження у SQLite."""

from __future__ import annotations

import json
import sqlite3
from concurrent.futures import ThreadPoolExecutor
from dataclasses import dataclass
from pathlib import Path
from typing import Any
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen


API_BASE_URL = "https://jsonplaceholder.typicode.com"


class ApiRequestError(RuntimeError):
    """Помилка виконання або обробки HTTP-запиту."""


@dataclass(frozen=True)
class ApiTask:
    """Опис одного HTTP-запиту."""

    method: str
    url: str
    payload: dict[str, Any] | None = None

    def __post_init__(self) -> None:
        normalized_method = self.method.upper()
        if normalized_method not in {"GET", "POST"}:
            raise ValueError("Підтримуються лише методи GET і POST.")
        object.__setattr__(self, "method", normalized_method)


@dataclass(frozen=True)
class ApiRecord:
    """Нормалізований запис для збереження в базі даних."""

    method: str
    source_url: str
    response_id: int | None
    title: str
    body: str


def fetch_json(task: ApiTask, timeout: float = 10.0) -> dict[str, Any]:
    """Виконати GET або POST і повернути JSON-об'єкт."""
    data = None
    headers = {"Accept": "application/json"}
    if task.payload is not None:
        data = json.dumps(task.payload).encode("utf-8")
        headers["Content-Type"] = "application/json; charset=UTF-8"

    request = Request(task.url, data=data, headers=headers, method=task.method)
    try:
        with urlopen(request, timeout=timeout) as response:
            payload = json.loads(response.read().decode("utf-8"))
    except (HTTPError, URLError, TimeoutError, json.JSONDecodeError) as error:
        raise ApiRequestError(f"Не вдалося виконати {task.method} {task.url}") from error

    if not isinstance(payload, dict):
        raise ApiRequestError("REST API повинен повернути JSON-об'єкт.")
    return payload


def run_in_threads(tasks: list[ApiTask], max_workers: int = 2) -> list[dict[str, Any]]:
    """Виконати HTTP-запити конкурентно в окремих потоках."""
    if not tasks:
        return []
    if max_workers <= 0:
        raise ValueError("Кількість потоків повинна бути додатною.")
    with ThreadPoolExecutor(max_workers=min(max_workers, len(tasks))) as executor:
        return list(executor.map(fetch_json, tasks))


def normalize_record(task: ApiTask, response: dict[str, Any]) -> ApiRecord:
    """Перетворити відповідь API на структуру для SQLite."""
    response_id = response.get("id")
    if response_id is not None and (isinstance(response_id, bool) or not isinstance(response_id, int)):
        raise ApiRequestError("Поле 'id' повинно бути цілим числом або null.")
    return ApiRecord(
        method=task.method,
        source_url=task.url,
        response_id=response_id,
        title=str(response.get("title", "")),
        body=str(response.get("body", "")),
    )


def initialize_database(connection: sqlite3.Connection) -> None:
    """Створити таблицю для відповідей API, якщо вона ще не існує."""
    connection.execute(
        """
        CREATE TABLE IF NOT EXISTS api_records (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            method TEXT NOT NULL CHECK(method IN ('GET', 'POST')),
            source_url TEXT NOT NULL,
            response_id INTEGER,
            title TEXT NOT NULL,
            body TEXT NOT NULL
        )
        """
    )


def replace_records(database_path: Path, records: list[ApiRecord]) -> None:
    """Атомарно замінити збережені записи новими результатами."""
    database_path.parent.mkdir(parents=True, exist_ok=True)
    with sqlite3.connect(database_path) as connection:
        initialize_database(connection)
        connection.execute("DELETE FROM api_records")
        connection.executemany(
            """
            INSERT INTO api_records (method, source_url, response_id, title, body)
            VALUES (?, ?, ?, ?, ?)
            """,
            [
                (record.method, record.source_url, record.response_id, record.title, record.body)
                for record in records
            ],
        )


def read_records(database_path: Path) -> list[ApiRecord]:
    """Прочитати збережені записи з SQLite у порядку додавання."""
    if not database_path.exists():
        raise FileNotFoundError(f"Базу даних не знайдено: {database_path}")
    with sqlite3.connect(database_path) as connection:
        initialize_database(connection)
        rows = connection.execute(
            """
            SELECT method, source_url, response_id, title, body
            FROM api_records
            ORDER BY id
            """
        ).fetchall()
    return [ApiRecord(*row) for row in rows]


def build_tasks() -> list[ApiTask]:
    """Підготувати GET- і POST-запити до JSONPlaceholder."""
    return [
        ApiTask("GET", f"{API_BASE_URL}/posts/1"),
        ApiTask(
            "POST",
            f"{API_BASE_URL}/posts",
            {"title": "Python Lab 8", "body": "Левченко Д. В.", "userId": 8},
        ),
    ]


def main() -> None:
    """Виконати запити, зберегти відповіді та прочитати їх із SQLite."""
    database_path = Path(__file__).with_name("api_data.db")
    tasks = build_tasks()
    responses = run_in_threads(tasks)
    records = [normalize_record(task, response) for task, response in zip(tasks, responses)]
    replace_records(database_path, records)
    saved_records = read_records(database_path)

    print("Лабораторна робота №8. Загальне завдання.")
    print(f"Виконано HTTP-запитів у потоках: {len(tasks)}")
    print(f"База даних: {database_path.name}")
    print("Збережені записи:")
    for number, record in enumerate(saved_records, start=1):
        print(
            f"{number}. {record.method}: id={record.response_id}, "
            f"title={record.title!r}"
        )
    print(f"Усього прочитано з SQLite: {len(saved_records)}")


if __name__ == "__main__":
    main()
