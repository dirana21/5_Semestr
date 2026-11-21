#!/usr/bin/env python3
"""Прийняти дані форми та повернути HTML-відповідь через CGI."""

import cgi
from html import escape
from math import isfinite
import sys

from levchenko_toolkit.calculator import add, divide, multiply, square_root, subtract


OPERATIONS = {
    "add": (add, "+"),
    "subtract": (subtract, "−"),
    "multiply": (multiply, "×"),
    "divide": (divide, "÷"),
}


def read_number(text):
    value = float(text.strip().replace(",", "."))
    if not isfinite(value):
        raise ValueError("Введіть скінченне десяткове число.")
    return value


def calculate(mode, operation, a, b):
    if mode == "convert":
        try:
            number = int(a.strip(), 10)
        except ValueError as error:
            raise ValueError("Для перетворення введіть ціле десяткове число в полі A.") from error
        return f"Перетворення числа {number}₁₀", str(number), oct(number)
    if mode != "calculate" or (operation != "root" and operation not in OPERATIONS):
        raise ValueError("Виберіть підтримувану операцію.")

    try:
        first = read_number(a)
        second = read_number(b) if operation != "root" else None
    except ValueError as error:
        raise ValueError("Введіть коректні скінченні десяткові числа.") from error

    if operation == "root":
        value = square_root(first)
        expression = f"√{first}"
    else:
        function, symbol = OPERATIONS[operation]
        value = function(first, second)
        expression = f"{first} {symbol} {second}"
    if not isfinite(value):
        raise ValueError("Результат виходить за межі числового формату.")
    if value.is_integer():
        integer = int(value)
        return expression, str(integer), oct(integer)
    return expression, str(value), None


def result_page(content):
    return f"""<!doctype html>
<html lang="uk">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>Результат · Вісімковий калькулятор</title>
  <link rel="stylesheet" href="/style.css">
</head>
<body>
  <main>
    <header>
      <p class="eyebrow">Python основи / Лабораторна робота №12</p>
      <h1>Вісімковий калькулятор</h1>
      <p class="muted">Вебверсія калькулятора на Python CGI · Варіант 2</p>
    </header>
    <section class="card" aria-labelledby="result-title">
      <h2 id="result-title">Результат обчислення</h2>
      {content}
      <a class="back" href="/">Повернутися до форми</a>
    </section>
  </main>
</body>
</html>"""


def main():
    sys.stdout.reconfigure(encoding="utf-8")
    form = cgi.FieldStorage(keep_blank_values=True)
    try:
        expression, decimal, octal = calculate(
            form.getfirst("mode", "calculate"),
            form.getfirst("operation", "add"),
            form.getfirst("a", ""),
            form.getfirst("b", ""),
        )
    except ValueError as error:
        content = f'<p class="error" role="alert">{escape(str(error))}</p>'
    else:
        note = "" if octal else "<p>Вісімковий запис доступний для цілих результатів.</p>"
        content = f"""<p class="muted">{escape(expression)}</p>
      <dl class="results">
        <div><dt>Десятковий результат</dt><dd>{escape(decimal)}</dd></div>
        <div><dt>Вісімковий запис</dt><dd>{escape(octal or "—")}</dd></div>
      </dl>
      {note}"""
    print("Content-Type: text/html; charset=utf-8")
    print()
    print(result_page(content))


if __name__ == "__main__":
    main()
