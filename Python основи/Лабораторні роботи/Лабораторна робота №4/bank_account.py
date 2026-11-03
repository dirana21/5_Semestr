"""Лабораторна робота №4: класи, об'єкти та спеціальні методи."""

from __future__ import annotations

from decimal import Decimal, InvalidOperation, ROUND_HALF_UP
from functools import total_ordering


MoneyValue = Decimal | int | float | str
CENT = Decimal("0.01")


def to_money(value: MoneyValue) -> Decimal:
    """Перетворити значення на суму з двома десятковими знаками."""
    if isinstance(value, bool):
        raise TypeError("Сума повинна бути числом.")

    try:
        amount = Decimal(str(value)).quantize(CENT, rounding=ROUND_HALF_UP)
    except (InvalidOperation, ValueError) as error:
        raise TypeError("Сума повинна бути числом.") from error

    if not amount.is_finite():
        raise ValueError("Сума повинна бути скінченним числом.")
    return amount


@total_ordering
class BankAccount:
    """Банківський рахунок, який підтримує злиття та порівняння за балансом."""

    bank_name = "Навчальний банк"

    def __init__(self, name: str, balance: MoneyValue = 0) -> None:
        cleaned_name = name.strip()
        if not cleaned_name:
            raise ValueError("Ім'я власника рахунку не може бути порожнім.")

        initial_balance = to_money(balance)
        if initial_balance < 0:
            raise ValueError("Початковий баланс не може бути від'ємним.")

        self.name = cleaned_name
        self.balance = initial_balance

    def deposit(self, amount: MoneyValue) -> None:
        """Поповнити рахунок на додатну суму."""
        money = to_money(amount)
        if money <= 0:
            raise ValueError("Сума поповнення повинна бути додатною.")
        self.balance += money

    def withdraw(self, amount: MoneyValue) -> None:
        """Зняти кошти, якщо на рахунку достатньо грошей."""
        money = to_money(amount)
        if money <= 0:
            raise ValueError("Сума зняття повинна бути додатною.")
        if money > self.balance:
            raise ValueError("Недостатньо коштів на рахунку.")
        self.balance -= money

    def __add__(self, other: object) -> BankAccount:
        """Об'єднати два рахунки в новий рахунок із сумарним балансом."""
        if not isinstance(other, BankAccount):
            return NotImplemented
        merged_name = f"{self.name} + {other.name}"
        return BankAccount(merged_name, self.balance + other.balance)

    def __eq__(self, other: object) -> bool:
        """Перевірити рівність рахунків за балансом."""
        if not isinstance(other, BankAccount):
            return NotImplemented
        return self.balance == other.balance

    def __lt__(self, other: BankAccount) -> bool:
        """Порівняти рахунки за балансом."""
        if not isinstance(other, BankAccount):
            return NotImplemented
        return self.balance < other.balance

    def __str__(self) -> str:
        """Повернути зрозуміле текстове подання рахунку."""
        return f"{self.name}: {self.balance:.2f} грн"

    def __repr__(self) -> str:
        """Повернути технічне подання об'єкта."""
        return f"BankAccount(name={self.name!r}, balance={str(self.balance)!r})"


def main() -> None:
    """Продемонструвати створення, зміну, злиття та порівняння рахунків."""
    first = BankAccount("Левченко Д. В.", "12500.50")
    second = BankAccount("Навчальний рахунок", 7500)

    print("Лабораторна робота №4. Варіант 8 → 1.")
    print(f"Банк: {BankAccount.bank_name}\n")
    print(f"Перший рахунок: {first}")
    print(f"Другий рахунок: {second}\n")

    first.deposit(500)
    second.withdraw(1000)
    print("Після операцій:")
    print(f"Перший рахунок: {first}")
    print(f"Другий рахунок: {second}\n")

    merged = first + second
    print(f"Об'єднаний рахунок: {merged}")
    print(f"Перший рахунок має більший баланс: {first > second}")
    print(f"Баланси рахунків рівні: {first == second}")


if __name__ == "__main__":
    main()
