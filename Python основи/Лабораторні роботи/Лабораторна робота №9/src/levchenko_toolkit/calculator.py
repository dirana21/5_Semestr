"""Арифметичні функції з лабораторної роботи №1."""

from __future__ import annotations

import math


def add(first: float, second: float) -> float:
    """Повернути суму двох чисел."""
    return first + second


def subtract(first: float, second: float) -> float:
    """Повернути різницю двох чисел."""
    return first - second


def multiply(first: float, second: float) -> float:
    """Повернути добуток двох чисел."""
    return first * second


def divide(first: float, second: float) -> float:
    """Поділити перше число на друге."""
    if second == 0:
        raise ValueError("Ділити на нуль не можна.")
    return first / second


def square_root(number: float) -> float:
    """Обчислити квадратний корінь невід'ємного числа."""
    if number < 0:
        raise ValueError("Квадратний корінь з від'ємного числа не визначений.")
    return math.sqrt(number)
