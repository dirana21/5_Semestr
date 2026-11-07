"""Автоматичні тести навчального пакета."""

from __future__ import annotations

import sys
import tempfile
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).with_name("src")))

from levchenko_toolkit import (  # noqa: E402
    JsonDataError,
    add,
    calculate_numbers_sum,
    divide,
    fibonacci_divisible_by_three,
    fibonacci_numbers,
    load_json,
    multiply,
    save_json,
    square_root,
    subtract,
)


class StudentToolkitTests(unittest.TestCase):
    def test_add(self) -> None:
        self.assertEqual(add(8, 9), 17)

    def test_subtract(self) -> None:
        self.assertEqual(subtract(9, 8), 1)

    def test_multiply(self) -> None:
        self.assertEqual(multiply(8, 9), 72)

    def test_divide(self) -> None:
        self.assertEqual(divide(72, 8), 9)

    def test_divide_by_zero(self) -> None:
        with self.assertRaises(ValueError):
            divide(8, 0)

    def test_square_root(self) -> None:
        self.assertEqual(square_root(81), 9)

    def test_negative_square_root(self) -> None:
        with self.assertRaises(ValueError):
            square_root(-1)

    def test_fibonacci_numbers(self) -> None:
        self.assertEqual(list(fibonacci_numbers(13)), [1, 1, 2, 3, 5, 8, 13])

    def test_fibonacci_divisible_by_three(self) -> None:
        self.assertEqual(list(fibonacci_divisible_by_three(100)), [3, 21])

    def test_fibonacci_rejects_boolean_limit(self) -> None:
        with self.assertRaises(TypeError):
            list(fibonacci_numbers(True))

    def test_fibonacci_rejects_nonpositive_limit(self) -> None:
        with self.assertRaises(ValueError):
            list(fibonacci_numbers(0))

    def test_calculate_numbers_sum(self) -> None:
        self.assertEqual(calculate_numbers_sum({"numbers": [8, 9, 10]}), 27)

    def test_calculate_numbers_sum_rejects_missing_list(self) -> None:
        with self.assertRaises(JsonDataError):
            calculate_numbers_sum({})

    def test_calculate_numbers_sum_rejects_boolean(self) -> None:
        with self.assertRaises(JsonDataError):
            calculate_numbers_sum({"numbers": [8, True]})

    def test_json_round_trip(self) -> None:
        with tempfile.TemporaryDirectory(ignore_cleanup_errors=True) as directory:
            path = Path(directory) / "data.json"
            source = {"numbers": [8, 9], "student": "Левченко Д. В."}
            save_json(source, path)
            self.assertEqual(load_json(path), source)


if __name__ == "__main__":
    unittest.main(verbosity=2)
