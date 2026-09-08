"""Автоматичні тести консольного калькулятора."""

import unittest

from calculator import add, divide, multiply, square_root, subtract


class CalculatorTests(unittest.TestCase):
    def test_add(self) -> None:
        self.assertEqual(add(8, 2), 10)

    def test_subtract(self) -> None:
        self.assertEqual(subtract(8, 3), 5)

    def test_multiply(self) -> None:
        self.assertEqual(multiply(8, 4), 32)

    def test_divide(self) -> None:
        self.assertEqual(divide(8, 2), 4)

    def test_division_by_zero(self) -> None:
        with self.assertRaisesRegex(ValueError, "Ділити на нуль"):
            divide(8, 0)

    def test_square_root(self) -> None:
        self.assertEqual(square_root(81), 9)

    def test_square_root_of_negative_number(self) -> None:
        with self.assertRaisesRegex(ValueError, "від'ємного числа"):
            square_root(-1)


if __name__ == "__main__":
    unittest.main()

