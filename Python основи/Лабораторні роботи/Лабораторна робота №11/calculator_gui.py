"""Калькулятор Tkinter із вісімковим представленням цілих чисел."""

import math
import tkinter as tk
from tkinter import ttk

from levchenko_toolkit.calculator import add, divide, multiply, square_root, subtract


OPERATIONS = {"+": add, "−": subtract, "×": multiply, "÷": divide}


def parse_number(text):
    """Прочитати десяткове число з крапкою або комою."""
    try:
        value = float(text.strip().replace(",", "."))
    except ValueError as error:
        raise ValueError("Введіть коректне десяткове число.") from error
    if not math.isfinite(value):
        raise ValueError("Введіть скінченне число.")
    return value


def calculate(operation, first_text, second_text):
    """Передати операнди функції з установленого wheel-пакета."""
    first = parse_number(first_text)
    if operation == "√":
        result = square_root(first)
    else:
        result = OPERATIONS[operation](first, parse_number(second_text))
    if not math.isfinite(result):
        raise ValueError("Результат виходить за межі числового формату.")
    return result


def to_octal(value):
    """Подати ціле число у вісімковій системі зі збереженням знака."""
    if not math.isfinite(value) or value != int(value):
        raise ValueError("Вісімкове перетворення доступне для цілих чисел.")
    return oct(int(value))


class CalculatorApp:
    def __init__(self, root):
        root.title("Калькулятор · Лабораторна №11")
        root.minsize(500, 405)
        root.columnconfigure(0, weight=1)

        panel = ttk.Frame(root, padding=24)
        panel.grid(sticky="nsew")
        panel.columnconfigure(1, weight=1)

        self.first = tk.StringVar(value="64")
        self.second = tk.StringVar(value="8")
        self.operation = tk.StringVar(value="+")
        self.decimal = tk.StringVar(value="—")
        self.octal = tk.StringVar(value="—")
        self.status = tk.StringVar()

        ttk.Label(panel, text="Калькулятор", font=("Segoe UI", 21, "bold")).grid(
            row=0, columnspan=2, sticky="w"
        )
        ttk.Label(panel, text="Варіант 2 · Вісімкова система числення").grid(
            row=1, columnspan=2, sticky="w", pady=(0, 18)
        )
        for row, label, variable in ((2, "Число A", self.first), (4, "Число B", self.second)):
            ttk.Label(panel, text=label).grid(row=row, column=0, sticky="w", padx=(0, 16))
            entry = ttk.Entry(panel, textvariable=variable)
            entry.grid(row=row, column=1, sticky="ew", pady=4)
            if row == 2:
                entry.focus_set()

        ttk.Label(panel, text="Операція").grid(row=3, column=0, sticky="w")
        operation_box = ttk.Combobox(
            panel, values=(*OPERATIONS, "√"), textvariable=self.operation, state="readonly"
        )
        operation_box.grid(row=3, column=1, sticky="ew", pady=4)

        actions = ttk.Frame(panel)
        actions.grid(row=5, columnspan=2, sticky="w", pady=14)
        ttk.Button(actions, text="Обчислити", command=self.compute).pack(side="left")
        ttk.Button(actions, text="Перетворити A у вісімкове", command=self.convert).pack(
            side="left", padx=8
        )
        ttk.Separator(panel).grid(row=6, columnspan=2, sticky="ew", pady=(0, 8))
        for row, label, variable in (
            (7, "Десятковий результат", self.decimal),
            (8, "Вісімковий запис", self.octal),
        ):
            ttk.Label(panel, text=label).grid(row=row, column=0, sticky="w", padx=(0, 12))
            ttk.Entry(panel, textvariable=variable, state="readonly").grid(
                row=row, column=1, sticky="ew", pady=4
            )
        ttk.Label(panel, textvariable=self.status, wraplength=440).grid(
            row=9, columnspan=2, sticky="w", pady=(10, 0)
        )
        root.bind("<Return>", lambda event: self.compute())

    def show_result(self, value):
        self.decimal.set(str(int(value)) if value.is_integer() else str(value))
        self.octal.set("—")
        self.status.set("")
        try:
            self.octal.set(to_octal(value))
        except ValueError as error:
            self.status.set(str(error))

    def show_error(self, error):
        self.decimal.set("—")
        self.octal.set("—")
        self.status.set(str(error))

    def compute(self):
        try:
            self.show_result(calculate(self.operation.get(), self.first.get(), self.second.get()))
        except ValueError as error:
            self.show_error(error)

    def convert(self):
        try:
            number = int(self.first.get().strip(), 10)
        except ValueError:
            self.show_error("Для перетворення введіть ціле десяткове число в полі A.")
            return
        self.decimal.set(str(number))
        self.octal.set(oct(number))
        self.status.set("")


if __name__ == "__main__":
    window = tk.Tk()
    CalculatorApp(window)
    window.mainloop()
