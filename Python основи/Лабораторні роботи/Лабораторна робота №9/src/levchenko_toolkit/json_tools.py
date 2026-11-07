"""Засоби роботи з JSON з лабораторної роботи №7."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any


class JsonDataError(ValueError):
    """Помилка структури або значень JSON-даних."""


def save_json(data: dict[str, Any], file_path: Path) -> None:
    """Серіалізувати словник у файл JSON із кодуванням UTF-8."""
    if not isinstance(data, dict):
        raise TypeError("Для збереження очікується словник.")
    file_path.parent.mkdir(parents=True, exist_ok=True)
    file_path.write_text(
        json.dumps(data, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )


def load_json(file_path: Path) -> dict[str, Any]:
    """Прочитати JSON-файл і повернути словник."""
    try:
        text = file_path.read_text(encoding="utf-8")
    except FileNotFoundError as error:
        raise JsonDataError(f"Файл не знайдено: {file_path}") from error
    try:
        data = json.loads(text)
    except json.JSONDecodeError as error:
        raise JsonDataError(f"Некоректний JSON у файлі {file_path.name}.") from error
    if not isinstance(data, dict):
        raise JsonDataError("Кореневий елемент JSON повинен бути об'єктом.")
    return data


def calculate_numbers_sum(data: dict[str, Any]) -> int | float:
    """Обчислити суму чисел зі списку за ключем numbers."""
    numbers = data.get("numbers")
    if not isinstance(numbers, list) or not numbers:
        raise JsonDataError("Ключ 'numbers' повинен містити непорожній список.")
    if any(isinstance(value, bool) or not isinstance(value, (int, float)) for value in numbers):
        raise JsonDataError("Список 'numbers' повинен містити лише числа.")
    return sum(numbers)
