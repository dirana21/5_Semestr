"""Лабораторна робота №3: ітератори та генератори."""

from __future__ import annotations

from collections.abc import Iterator


def validate_limit(limit: int) -> None:
    """Перевірити верхню межу послідовності."""
    if isinstance(limit, bool) or not isinstance(limit, int):
        raise TypeError("Верхня межа N повинна бути цілим числом.")
    if limit < 1:
        raise ValueError("Верхня межа N повинна бути додатною.")


def fibonacci_numbers(limit: int) -> Iterator[int]:
    """Ліниво сформувати додатні числа Фібоначчі, що не перевищують N."""
    validate_limit(limit)
    current, following = 1, 1

    while current <= limit:
        yield current
        current, following = following, current + following


def fibonacci_divisible_by_three(limit: int) -> Iterator[int]:
    """За допомогою yield повернути числа Фібоначчі до N, кратні 3."""
    for number in fibonacci_numbers(limit):
        if number % 3 == 0:
            yield number


def fibonacci_divisible_expression(limit: int) -> Iterator[int]:
    """Створити аналогічний генератор за допомогою генераторного виразу."""
    return (number for number in fibonacci_numbers(limit) if number % 3 == 0)


def main() -> None:
    """Продемонструвати обидва способи створення генератора."""
    limit = 1000

    yield_generator = fibonacci_divisible_by_three(limit)
    expression_generator = fibonacci_divisible_expression(limit)

    print("Лабораторна робота №3. Варіант 8 → 1.")
    print(f"Верхня межа N: {limit}\n")
    print("Генераторна функція з yield:")
    print(list(yield_generator))
    print("\nГенераторний вираз:")
    print(list(expression_generator))
    print("\nОбидва обчислення виконуються ліниво та дають однаковий результат.")


if __name__ == "__main__":
    main()
