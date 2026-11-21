import unittest

from calculator_gui import calculate, parse_number, to_octal


class CalculatorTests(unittest.TestCase):
    def test_wheel_operations(self):
        for operation, expected in (("+", 72), ("−", 56), ("×", 512), ("÷", 8), ("√", 8)):
            with self.subTest(operation=operation):
                self.assertEqual(calculate(operation, "64", "8"), expected)

    def test_octal(self):
        self.assertEqual(to_octal(calculate("+", "64", "8")), "0o110")
        self.assertEqual(to_octal(-8), "-0o10")
        self.assertEqual(to_octal(0), "0o0")

    def test_fraction(self):
        result = calculate("÷", "3", "2")
        self.assertEqual(result, 1.5)
        with self.assertRaises(ValueError):
            to_octal(result)

    def test_invalid_input(self):
        self.assertEqual(parse_number("2,5"), 2.5)
        for text in ("", "abc", "nan", "inf"):
            with self.subTest(text=text), self.assertRaises(ValueError):
                parse_number(text)

    def test_arithmetic_errors(self):
        with self.assertRaisesRegex(ValueError, "нуль"):
            calculate("÷", "64", "0")
        with self.assertRaisesRegex(ValueError, "від'ємного"):
            calculate("√", "-1", "")


if __name__ == "__main__":
    unittest.main()
