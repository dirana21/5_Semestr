"""Перевірка пакета після встановлення з wheel у нове середовище."""

from __future__ import annotations

from importlib.metadata import version
from pathlib import Path

import levchenko_toolkit
from levchenko_toolkit import (
    add,
    calculate_numbers_sum,
    divide,
    fibonacci_divisible_by_three,
    multiply,
    square_root,
)


def main() -> None:
    """Продемонструвати імпорт і функції встановленого пакета."""
    package_path = Path(levchenko_toolkit.__file__).resolve()
    if "site-packages" not in str(package_path):
        raise RuntimeError("Пакет потрібно запускати після встановлення wheel у venv.")

    print("Лабораторна робота №9. Загальне завдання.")
    print(f"Версія пакета: {version('levchenko-python-toolkit')}")
    print(f"Пакет завантажено з: {package_path}")
    print(f"8 + 9 = {add(8, 9)}")
    print(f"8 * 9 = {multiply(8, 9)}")
    print(f"72 / 8 = {divide(72, 8):g}")
    print(f"Квадратний корінь із 81 = {square_root(81):g}")
    print(f"Числа Фібоначчі до 100, кратні 3: {list(fibonacci_divisible_by_three(100))}")
    print(f"Сума чисел у JSON-структурі: {calculate_numbers_sum({'numbers': [8, 9, 10]})}")
    print("Wheel-пакет успішно встановлено та перевірено.")


if __name__ == "__main__":
    main()
