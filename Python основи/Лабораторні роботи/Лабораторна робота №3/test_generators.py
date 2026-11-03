"""Автоматичні тести генераторів чисел Фібоначчі."""

from __future__ import annotations

import types
import unittest

from generators import (
    fibonacci_divisible_by_three,
    fibonacci_divisible_expression,
    fibonacci_numbers,
)


class FibonacciGeneratorTests(unittest.TestCase):
    def test_fibonacci_sequence_up_to_limit(self) -> None:
        self.assertEqual(
            list(fibonacci_numbers(21)),
            [1, 1, 2, 3, 5, 8, 13, 21],
        )

    def test_yield_generator_returns_only_multiples_of_three(self) -> None:
        self.assertEqual(
            list(fibonacci_divisible_by_three(1000)),
            [3, 21, 144, 987],
        )

    def test_generator_expression_returns_same_result(self) -> None:
        self.assertEqual(
            list(fibonacci_divisible_expression(1000)),
            [3, 21, 144, 987],
        )

    def test_function_is_lazy_generator(self) -> None:
        result = fibonacci_divisible_by_three(100)
        self.assertIsInstance(result, types.GeneratorType)

    def test_expression_is_lazy_generator(self) -> None:
        result = fibonacci_divisible_expression(100)
        self.assertIsInstance(result, types.GeneratorType)

    def test_limit_without_matching_numbers_returns_empty_sequence(self) -> None:
        self.assertEqual(list(fibonacci_divisible_by_three(2)), [])

    def test_non_positive_limit_is_rejected(self) -> None:
        with self.assertRaisesRegex(ValueError, "додатною"):
            list(fibonacci_divisible_by_three(0))

    def test_non_integer_limit_is_rejected(self) -> None:
        with self.assertRaisesRegex(TypeError, "цілим числом"):
            list(fibonacci_divisible_expression(10.5))


if __name__ == "__main__":
    unittest.main()
