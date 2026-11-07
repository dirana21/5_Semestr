# Лабораторна робота №9

**Дисципліна:** «Python основи»<br>
**Виконав:** Левченко Д. В.<br>
**Номер студента:** 8<br>
**Варіант:** загальне завдання без поділу на варіанти

## Завдання

Об'єднати напрацювання попередніх лабораторних робіт у модулі й пакет, описати проєкт у `pyproject.toml`, створити wheel, установити його в нове віртуальне середовище та перевірити імпорт і роботу встановленого пакета.

## Вміст папки

- [Звіт](./Звіт.md) — звіт українською мовою.
- [Пакет](./src/levchenko_toolkit/) — калькулятор, генератори та JSON-засоби.
- [Конфігурація](./pyproject.toml) — метадані та правила складання.
- [Wheel-пакет](./dist/levchenko_python_toolkit-1.0.0-py3-none-any.whl) — готовий дистрибутив.
- [Перевірка wheel](./verify_wheel.py) — демонстрація імпорту із `site-packages`.
- [Тести](./test_student_toolkit.py) — 15 автоматичних тестів.
- [Завдання](./Завдання.pdf) — методична вказівка.
- [Скріншоти](./screenshots/) — запуск установленого пакета і тестів у PyCharm.

## Відтворення

```powershell
python -m venv .venv
.venv\Scripts\python -m pip install -r requirements.txt
.venv\Scripts\python -m build --wheel
.venv\Scripts\python -m pip install --force-reinstall dist\levchenko_python_toolkit-1.0.0-py3-none-any.whl
.venv\Scripts\python verify_wheel.py
.venv\Scripts\python -m unittest -v test_student_toolkit.py
```

Пакет не має зовнішніх залежностей під час виконання; `build` потрібен лише для створення wheel.
