"""Дешифрування файлів біграмним шифром Плейфейра. Варіант 12."""

from pathlib import Path


ALPHABET = "АБВГҐДЕЄЖЗИІЇЙКЛМНОПРСТУФХЦЧШЩЬЮЯ '."
SIDE = 6
FILLER = "Х"


def normalize(text: str) -> str:
    """Готує український текст до роботи з квадратом 6×6."""
    result = text.upper().replace("’", "'").replace("`", "'")
    result = result.replace("\r", " ").replace("\n", " ").strip()
    unsupported = sorted(set(result) - set(ALPHABET))
    if unsupported:
        raise ValueError(f"Непідтримувані символи: {' '.join(unsupported)}")
    return result


def build_square(keyword: str) -> list[list[str]]:
    """Створює квадрат Плейфейра: спочатку ключ, потім решта алфавіту."""
    keyword = normalize(keyword)
    symbols: list[str] = []

    for symbol in keyword + ALPHABET:
        if symbol not in symbols:
            symbols.append(symbol)

    return [symbols[start : start + SIDE] for start in range(0, len(symbols), SIDE)]


def positions(square: list[list[str]]) -> dict[str, tuple[int, int]]:
    return {
        symbol: (row, column)
        for row, line in enumerate(square)
        for column, symbol in enumerate(line)
    }


def prepare_plaintext(text: str) -> str:
    """Ділить відкритий текст на біграми та додає Х за потреби."""
    text = normalize(text)
    prepared: list[str] = []
    index = 0

    while index < len(text):
        first = text[index]
        if index + 1 >= len(text):
            prepared.extend((first, FILLER))
            break

        second = text[index + 1]
        if first == second:
            prepared.extend((first, FILLER))
            index += 1
        else:
            prepared.extend((first, second))
            index += 2

    return "".join(prepared)


def transform_pair(
    first: str,
    second: str,
    square: list[list[str]],
    shift: int,
) -> str:
    location = positions(square)
    row1, column1 = location[first]
    row2, column2 = location[second]

    if row1 == row2:
        return square[row1][(column1 + shift) % SIDE] + square[row2][(column2 + shift) % SIDE]
    if column1 == column2:
        return square[(row1 + shift) % SIDE][column1] + square[(row2 + shift) % SIDE][column2]
    return square[row1][column2] + square[row2][column1]


def encrypt_for_check(plaintext: str, keyword: str) -> str:
    """Допоміжне шифрування для підготовки прикладу і тестів."""
    square = build_square(keyword)
    prepared = prepare_plaintext(plaintext)
    return "".join(
        transform_pair(prepared[index], prepared[index + 1], square, 1)
        for index in range(0, len(prepared), 2)
    )


def decrypt(ciphertext: str, keyword: str) -> str:
    """Розшифровує біграми: ліворуч, угору або за прямокутником."""
    ciphertext = normalize(ciphertext)
    if not ciphertext or len(ciphertext) % 2 != 0:
        raise ValueError("Шифротекст має містити парну кількість символів.")

    square = build_square(keyword)
    return "".join(
        transform_pair(ciphertext[index], ciphertext[index + 1], square, -1)
        for index in range(0, len(ciphertext), 2)
    )


def decrypt_file(source: Path, destination: Path, keyword: str) -> str:
    ciphertext = source.read_text(encoding="utf-8")
    plaintext = decrypt(ciphertext, keyword)
    destination.write_text(plaintext, encoding="utf-8")
    return plaintext


def print_square(keyword: str) -> None:
    print("\nКвадрат Плейфейра:")
    for row in build_square(keyword):
        print(" ".join("␠" if symbol == " " else symbol for symbol in row))


def main() -> None:
    print("Лабораторна робота №2. Варіант 12")
    print("Дешифрування файлу біграмним шифром Плейфейра")

    try:
        source = Path(input("Файл із шифротекстом: ").strip())
        destination = Path(input("Файл для результату: ").strip())
        keyword = input("Ключове слово: ").strip()
        if not keyword:
            raise ValueError("Ключове слово не може бути порожнім.")

        print_square(keyword)
        plaintext = decrypt_file(source, destination, keyword)
        print(f"\nРозшифрований текст: {plaintext}")
        print(f"Результат записано у файл: {destination}")
    except (OSError, ValueError) as error:
        print(f"Помилка: {error}")


if __name__ == "__main__":
    main()
