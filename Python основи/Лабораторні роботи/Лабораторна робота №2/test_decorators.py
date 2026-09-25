"""Автоматичні тести декоратора @log."""

from __future__ import annotations

import io
import re
import unittest
from contextlib import redirect_stdout

from decorators import log


class LogDecoratorTests(unittest.TestCase):
    def test_returns_original_result(self) -> None:
        @log()
        def add(first: int, second: int) -> int:
            return first + second

        with redirect_stdout(io.StringIO()):
            result = add(8, 4)

        self.assertEqual(result, 12)

    def test_uses_info_as_default_level(self) -> None:
        @log()
        def identity(value: int) -> int:
            return value

        output = io.StringIO()
        with redirect_stdout(output):
            identity(8)

        self.assertIn("INFO | Виклик identity(8)", output.getvalue())

    def test_logs_timestamp_arguments_and_result(self) -> None:
        @log(level="DEBUG")
        def power(number: int, *, exponent: int = 2) -> int:
            return number**exponent

        output = io.StringIO()
        with redirect_stdout(output):
            power(3, exponent=3)

        text = output.getvalue()
        self.assertRegex(text, r"\[\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}\]")
        self.assertIn("DEBUG | Виклик power(3, exponent=3)", text)
        self.assertIn("Результат power: 27", text)

    def test_preserves_function_metadata(self) -> None:
        @log()
        def sample() -> str:
            """Тестова функція."""
            return "ok"

        self.assertEqual(sample.__name__, "sample")
        self.assertEqual(sample.__doc__, "Тестова функція.")

    def test_rejects_unknown_level(self) -> None:
        with self.assertRaisesRegex(ValueError, "Невідомий рівень"):
            log("TRACE")

    def test_logs_and_reraises_exception(self) -> None:
        @log()
        def divide(first: float, second: float) -> float:
            return first / second

        output = io.StringIO()
        with self.assertRaises(ZeroDivisionError), redirect_stdout(output):
            divide(8, 0)

        self.assertIn("ERROR | divide завершилася помилкою", output.getvalue())


if __name__ == "__main__":
    unittest.main()

