"""Лабораторна робота №7: робота з файлами та JSON (варіант 8 -> 1)."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any


class JsonDataError(ValueError):
    """Помилка структури або значень JSON-даних."""


VARIANT_DATA: dict[str, Any] = {
    "id": 1,
    "numbers": [10, 20, 30, 40, 50],
    "active": True,
}


def save_json(data: dict[str, Any], file_path: Path) -> None:
    """Серіалізувати словник у файл JSON із кодуванням UTF-8."""
    if not isinstance(data, dict):
        raise TypeError("Для збереження очікується словник.")
    file_path.parent.mkdir(parents=True, exist_ok=True)
    text = json.dumps(data, ensure_ascii=False, indent=2)
    file_path.write_text(text + "\n", encoding="utf-8")


def load_json(file_path: Path) -> dict[str, Any]:
    """Прочитати JSON-файл і повернути десеріалізований словник."""
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
    """Обчислити суму всіх чисел зі списку за ключем numbers."""
    if "numbers" not in data:
        raise JsonDataError("У даних відсутній ключ 'numbers'.")

    numbers = data["numbers"]
    if not isinstance(numbers, list):
        raise JsonDataError("Значення 'numbers' повинно бути списком.")
    if not numbers:
        raise JsonDataError("Список 'numbers' не може бути порожнім.")
    if any(isinstance(value, bool) or not isinstance(value, (int, float)) for value in numbers):
        raise JsonDataError("Список 'numbers' повинен містити лише числа.")
    return sum(numbers)


def process_variant(file_path: Path) -> tuple[dict[str, Any], int | float]:
    """Зберегти дані варіанта, завантажити їх і обчислити суму."""
    save_json(VARIANT_DATA, file_path)
    restored_data = load_json(file_path)
    result = calculate_numbers_sum(restored_data)
    return restored_data, result


def main() -> None:
    """Виконати повний цикл серіалізації, десеріалізації та обробки."""
    output_path = Path(__file__).with_name("output.json")
    restored_data, result = process_variant(output_path)

    print("Лабораторна робота №7. Варіант 8 -> 1.")
    print(f"Файл створено: {output_path.name}")
    print("Десеріалізовані дані:")
    print(json.dumps(restored_data, ensure_ascii=False, indent=2))
    print(f"Сума чисел за ключем 'numbers': {result}")


if __name__ == "__main__":
    main()
