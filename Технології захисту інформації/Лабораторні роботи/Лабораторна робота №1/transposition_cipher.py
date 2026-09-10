"""Таблична перестановка з ключем рядків. Варіант 12."""


def parse_row_key(value: str) -> tuple[int, ...]:
    """Перетворює рядок виду '2 3 1' на ключ перестановки рядків."""
    try:
        key = tuple(int(number) for number in value.replace(",", " ").split())
    except ValueError as exc:
        raise ValueError("Ключ має складатися з цілих чисел.") from exc

    if len(key) < 2 or set(key) != set(range(1, len(key) + 1)):
        raise ValueError("Ключ має містити числа від 1 до кількості рядків без повторень.")
    return key


def decrypt(ciphertext: str, row_key: tuple[int, ...], filler: str = "_") -> str:
    """Розшифровує текст, записаний по стовпцях після перестановки рядків."""
    row_count = len(row_key)
    if not ciphertext:
        raise ValueError("Шифротекст не може бути порожнім.")
    if len(ciphertext) % row_count != 0:
        raise ValueError("Довжина шифротексту має ділитися на кількість рядків.")

    column_count = len(ciphertext) // row_count
    permuted_table = [[""] * column_count for _ in range(row_count)]

    position = 0
    for column in range(column_count):
        for row in range(row_count):
            permuted_table[row][column] = ciphertext[position]
            position += 1

    original_table = [[""] * column_count for _ in range(row_count)]
    for original_row, new_place in enumerate(row_key):
        original_table[original_row] = permuted_table[new_place - 1]

    return "".join("".join(row) for row in original_table).rstrip(filler)


def encrypt_for_check(text: str, row_key: tuple[int, ...], filler: str = "_") -> str:
    """Допоміжне шифрування для самоперевірки алгоритму дешифрування."""
    row_count = len(row_key)
    column_count = (len(text) + row_count - 1) // row_count
    prepared = text.ljust(row_count * column_count, filler)
    original_table = [
        list(prepared[start : start + column_count])
        for start in range(0, len(prepared), column_count)
    ]

    permuted_table = [[""] * column_count for _ in range(row_count)]
    for original_row, new_place in enumerate(row_key):
        permuted_table[new_place - 1] = original_table[original_row]

    return "".join(
        permuted_table[row][column]
        for column in range(column_count)
        for row in range(row_count)
    )


def print_table(ciphertext: str, row_count: int) -> None:
    """Показує таблицю, яку заповнено шифротекстом по стовпцях."""
    column_count = len(ciphertext) // row_count
    table = [[""] * column_count for _ in range(row_count)]
    position = 0
    for column in range(column_count):
        for row in range(row_count):
            table[row][column] = ciphertext[position]
            position += 1

    print("\nТаблиця після заповнення шифротекстом:")
    for row in table:
        print(" ".join(row))


def main() -> None:
    print("Лабораторна робота №1. Варіант 12")
    print("Дешифрування табличної перестановки з ключем рядків")

    try:
        ciphertext = input("Введіть шифротекст: ").strip()
        row_key = parse_row_key(input("Ключ рядків (наприклад, 2 3 1): "))
        if len(ciphertext) % len(row_key) == 0:
            print_table(ciphertext, len(row_key))
        plaintext = decrypt(ciphertext, row_key)
        print(f"\nРозшифроване повідомлення: {plaintext}")
    except ValueError as error:
        print(f"Помилка: {error}")


if __name__ == "__main__":
    main()
