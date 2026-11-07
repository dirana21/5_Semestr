"""Навчальний пакет, що об'єднує напрацювання попередніх лабораторних робіт."""

from .calculator import add, divide, multiply, square_root, subtract
from .json_tools import JsonDataError, calculate_numbers_sum, load_json, save_json
from .sequences import fibonacci_divisible_by_three, fibonacci_numbers

__all__ = [
    "JsonDataError",
    "add",
    "calculate_numbers_sum",
    "divide",
    "fibonacci_divisible_by_three",
    "fibonacci_numbers",
    "load_json",
    "multiply",
    "save_json",
    "square_root",
    "subtract",
]

__version__ = "1.0.0"
