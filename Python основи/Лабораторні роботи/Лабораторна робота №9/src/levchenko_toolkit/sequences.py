"""Генератори з лабораторної роботи №3."""

from __future__ import annotations

from collections.abc import Iterator


def validate_limit(limit: int) -> None:
    """Перевірити верхню межу послідовності."""
    if isinstance(limit, bool) or not isinstance(limit, int):
        raise TypeError("Верхня межа повинна бути цілим числом.")
    if limit < 1:
        raise ValueError("Верхня межа повинна бути додатною.")


def fibonacci_numbers(limit: int) -> Iterator[int]:
    """Ліниво сформувати числа Фібоначчі, що не перевищують межу."""
    validate_limit(limit)
    current, following = 1, 1
    while current <= limit:
        yield current
        current, following = following, current + following


def fibonacci_divisible_by_three(limit: int) -> Iterator[int]:
    """Повернути числа Фібоначчі до межі, кратні трьом."""
    return (number for number in fibonacci_numbers(limit) if number % 3 == 0)
