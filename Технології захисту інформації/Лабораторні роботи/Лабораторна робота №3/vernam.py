"""Декодер Вернама з адитивним генератором."""

from collections.abc import Iterator


def additive_sequence(y0: int, y1: int, modulus: int) -> Iterator[int]:
    if modulus < 2 or not (0 <= y0 < modulus and 0 <= y1 < modulus):
        raise ValueError("Початкові числа мають бути від 0 до m − 1, а m ≥ 2.")
    previous, current = y0, y1
    while True:
        yield previous
        previous, current = current, (previous + current) % modulus


def xor_data(data: bytes, y0: int, y1: int, modulus: int) -> bytes:
    sequence = additive_sequence(y0, y1, modulus)
    result = bytearray()
    for byte in data:
        gamma = 0
        for _ in range(8):
            gamma = (gamma << 1) | (next(sequence) & 1)
        result.append(byte ^ gamma)
    return bytes(result)


def decrypt(ciphertext: str, y0: int, y1: int, modulus: int) -> str:
    data = bytes.fromhex(ciphertext)
    if not data:
        raise ValueError("Введіть шифротекст у форматі HEX.")
    return xor_data(data, y0, y1, modulus).decode("utf-8")


def main() -> None:
    print("Лабораторна робота №3. Варіант 6")
    print("Дешифрування методом Вернама")
    try:
        ciphertext = input("Шифротекст (HEX): ")
        y0 = int(input("Початкове число y0: "))
        y1 = int(input("Початкове число y1: "))
        modulus = int(input("Модуль m: "))
        print("Відновлений текст:", decrypt(ciphertext, y0, y1, modulus))
    except UnicodeDecodeError:
        print("Помилка: результат не є текстом UTF-8. Перевірте параметри.")
    except ValueError as error:
        print("Помилка:", error)


if __name__ == "__main__":
    main()
