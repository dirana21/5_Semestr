
"""Лабораторна робота №2: функції, аргументи та декоратори."""

from __future__ import annotations

from collections.abc import Callable
from datetime import datetime
from functools import wraps
from typing import ParamSpec, TypeVar


P = ParamSpec("P")
R = TypeVar("R")

VALID_LEVELS = {"DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"}


def log(level: str = "INFO") -> Callable[[Callable[P, R]], Callable[P, R]]:
    """Логувати час, рівень, аргументи та результат виклику функції."""
    normalized_level = level.upper()
    if normalized_level not in VALID_LEVELS:
        allowed = ", ".join(sorted(VALID_LEVELS))
        raise ValueError(f"Невідомий рівень '{level}'. Доступні рівні: {allowed}.")

    def decorator(function: Callable[P, R]) -> Callable[P, R]:
        @wraps(function)
        def wrapper(*args: P.args, **kwargs: P.kwargs) -> R:
            called_at = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            positional = [repr(argument) for argument in args]
            keyword = [f"{name}={value!r}" for name, value in kwargs.items()]
            arguments = ", ".join(positional + keyword)

            print(
                f"[{called_at}] {normalized_level} | "
                f"Виклик {function.__name__}({arguments})"
            )

            try:
                result = function(*args, **kwargs)
            except Exception as error:
                print(
                    f"[{called_at}] ERROR | {function.__name__} "
                    f"завершилася помилкою: {error}"
                )
                raise

            print(
                f"[{called_at}] {normalized_level} | "
                f"Результат {function.__name__}: {result!r}"
            )
            return result

        return wrapper

    return decorator


@log()
def calculate_area(width: float, height: float) -> float:
    """Обчислити площу прямокутника."""
    return width * height


@log(level="INFO")
def calculate_average(*values: float) -> float:
    """Обчислити середнє арифметичне довільної кількості чисел."""
    if not values:
        raise ValueError("Потрібно передати хоча б одне число.")
    return sum(values) / len(values)


@log(level="INFO")
def create_greeting(name: str, *, greeting: str = "Вітаю") -> str:
    """Створити привітання з ключовим параметром."""
    return f"{greeting}, {name}!"


def main() -> None:
    """Продемонструвати роботу декоратора на функціях різних типів."""
    print("Демонстрація декоратора @log. Варіант 8 → 1.\n")

    area = calculate_area(8, 5)
    print(f"Площа прямокутника: {area}\n")

    average = calculate_average(8, 10, 12)
    print(f"Середнє арифметичне: {average}\n")

    greeting = create_greeting("Дмитро", greeting="Добрий день")
    print(f"Повідомлення: {greeting}")


if __name__ == "__main__":
    main()
