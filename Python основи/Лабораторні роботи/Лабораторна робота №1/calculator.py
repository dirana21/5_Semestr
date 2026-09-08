"""Консольний калькулятор для лабораторної роботи №1."""

from __future__ import annotations

import math
from collections.abc import Callable


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


def read_number(prompt: str) -> float:
    """Зчитати дійсне число, дозволивши крапку або кому як роздільник."""
    while True:
        raw_value = input(prompt).strip().replace(",", ".")
        try:
            return float(raw_value)
        except ValueError:
            print("Помилка: введіть коректне число.")


def format_number(number: float) -> str:
    """Подати ціле значення без зайвої десяткової частини."""
    if number.is_integer():
        return str(int(number))
    return f"{number:.10g}"


def perform_binary_operation(operation: Callable[[float, float], float]) -> None:
    """Зчитати два числа та вивести результат бінарної операції."""
    first = read_number("Введіть перше число: ")
    second = read_number("Введіть друге число: ")
    print(f"Результат: {format_number(operation(first, second))}")


def perform_square_root() -> None:
    """Зчитати число та вивести його квадратний корінь."""
    number = read_number("Введіть число: ")
    print(f"Результат: {format_number(square_root(number))}")


def print_menu() -> None:
    """Вивести меню калькулятора."""
    print(
        "\nОберіть операцію:\n"
        "1 - Додавання\n"
        "2 - Віднімання\n"
        "3 - Множення\n"
        "4 - Ділення\n"
        "5 - Квадратний корінь\n"
        "0 - Завершити роботу"
    )


def main() -> None:
    """Запустити інтерактивний цикл калькулятора."""
    operations: dict[str, Callable[[float, float], float]] = {
        "1": add,
        "2": subtract,
        "3": multiply,
        "4": divide,
    }

    print("Консольний калькулятор. Варіант 1.")
    while True:
        print_menu()
        choice = input("Ваш вибір: ").strip()

        if choice == "0":
            print("Роботу калькулятора завершено.")
            break

        try:
            if choice in operations:
                perform_binary_operation(operations[choice])
            elif choice == "5":
                perform_square_root()
            else:
                print("Помилка: виберіть пункт меню від 0 до 5.")
        except ValueError as error:
            print(f"Помилка: {error}")


if __name__ == "__main__":
    main()

