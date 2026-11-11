# Лабораторна робота №10

**Дисципліна:** «Python основи»<br>
**Виконав:** Левченко Д. В.<br>
**Номер студента і варіанта:** 8

## Завдання

За допомогою NumPy згенерувати 100 точок за формулою `y = 8 * x + 2 + N(0, 2)`, навчити лінійну регресію Scikit-learn і побудувати в Matplotlib діаграму розсіювання з лінією моделі.

## Вміст папки

- [Jupyter Notebook](./lab10_regression.ipynb) — виконаний notebook із результатами та графіком.
- [Програма](./linear_regression_lab.py) — відтворюваний запуск експерименту в PyCharm.
- [Графік](./results/regression_variant_8.png) — результат візуалізації.
- [Тести](./test_linear_regression.py) — 15 автоматичних тестів.
- [Звіт](./Звіт.md) — оформлений звіт українською мовою.
- [Завдання](./Завдання.pdf) — методична вказівка.
- [Скріншоти](./screenshots/) — запуск програми й тестів у PyCharm.

## Запуск

```powershell
python -m venv .venv
.venv\Scripts\python -m pip install -r requirements.txt
.venv\Scripts\python linear_regression_lab.py
.venv\Scripts\python -m unittest -v test_linear_regression.py
.venv\Scripts\jupyter nbconvert --to notebook --execute --inplace lab10_regression.ipynb
```
