# Лабораторна робота №11

Калькулятор Tkinter з арифметичними функціями з wheel-пакета лабораторної №9. Для номера 8 за циклічним відліком обрано варіант 2, вісімкову систему.

[Звіт](./Звіт.md) · [Код](./calculator_gui.py) · [Тести](./test_calculator_gui.py) · [Методична вказівка](./Завдання.pdf)

## Запуск у Windows

Виконайте команди з папки цієї роботи. Потрібен Python 3.10 або новіший із Tkinter та сусідня папка лабораторної №9.

```powershell
python -m venv .venv
.\.venv\Scripts\python.exe -m pip install "..\Лабораторна робота №9\dist\levchenko_python_toolkit-1.0.0-py3-none-any.whl"
.\.venv\Scripts\python.exe calculator_gui.py
.\.venv\Scripts\python.exe -m unittest -v
```

У PyCharm виберіть `.venv\Scripts\python.exe` як інтерпретатор і запустіть `calculator_gui.py`. Введіть десяткові числа A і B та виберіть операцію. Квадратний корінь використовує лише A. Кнопка «Перетворити A у вісімкове» приймає ціле число. Префікс `0o` позначає вісімковий запис у Python.

GitHub відображає код і звіт. Графічне вікно відкривається під час локального запуску.
