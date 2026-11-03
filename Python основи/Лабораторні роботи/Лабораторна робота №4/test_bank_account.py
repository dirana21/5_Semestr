"""Автоматичні тести класу BankAccount."""

from __future__ import annotations

import unittest
from decimal import Decimal

from bank_account import BankAccount


class BankAccountTests(unittest.TestCase):
    def test_initializes_and_formats_balance(self) -> None:
        account = BankAccount("Дмитро", "1250.5")
        self.assertEqual(account.name, "Дмитро")
        self.assertEqual(account.balance, Decimal("1250.50"))
        self.assertEqual(str(account), "Дмитро: 1250.50 грн")

    def test_rejects_empty_name(self) -> None:
        with self.assertRaisesRegex(ValueError, "не може бути порожнім"):
            BankAccount("   ", 100)

    def test_rejects_negative_initial_balance(self) -> None:
        with self.assertRaisesRegex(ValueError, "не може бути від'ємним"):
            BankAccount("Дмитро", -1)

    def test_deposit_increases_balance(self) -> None:
        account = BankAccount("Дмитро", 100)
        account.deposit("25.50")
        self.assertEqual(account.balance, Decimal("125.50"))

    def test_withdraw_decreases_balance(self) -> None:
        account = BankAccount("Дмитро", 100)
        account.withdraw(40)
        self.assertEqual(account.balance, Decimal("60.00"))

    def test_rejects_withdrawal_above_balance(self) -> None:
        account = BankAccount("Дмитро", 100)
        with self.assertRaisesRegex(ValueError, "Недостатньо коштів"):
            account.withdraw(101)

    def test_add_merges_accounts_without_changing_originals(self) -> None:
        first = BankAccount("Перший", 100)
        second = BankAccount("Другий", 50)

        merged = first + second

        self.assertEqual(merged.name, "Перший + Другий")
        self.assertEqual(merged.balance, Decimal("150.00"))
        self.assertEqual(first.balance, Decimal("100.00"))
        self.assertEqual(second.balance, Decimal("50.00"))

    def test_accounts_are_equal_by_balance(self) -> None:
        self.assertEqual(BankAccount("Перший", 100), BankAccount("Другий", 100))

    def test_accounts_are_ordered_by_balance(self) -> None:
        poorer = BankAccount("Менший", 50)
        richer = BankAccount("Більший", 100)
        self.assertLess(poorer, richer)
        self.assertGreater(richer, poorer)

    def test_addition_with_other_type_is_not_supported(self) -> None:
        account = BankAccount("Дмитро", 100)
        with self.assertRaises(TypeError):
            _ = account + 50


if __name__ == "__main__":
    unittest.main()
