"""Навчальна реалізація RSA для варіанта 12."""

import argparse
from pathlib import Path


P, Q = 3, 13
N = P * Q
PHI = (P - 1) * (Q - 1)
E = 5
D = pow(E, -1, PHI)
ALPHABET = "0123456789"


def encrypt(message: str) -> list[int]:
    if not message or any(digit not in ALPHABET for digit in message):
        raise ValueError("Повідомлення має містити лише цифри від 0 до 9.")
    return [pow(int(digit), E, N) for digit in message]


def decrypt(ciphertext: list[int]) -> str:
    if not ciphertext or any(not 0 <= block < N for block in ciphertext):
        raise ValueError(f"Криптограма має містити числа від 0 до {N - 1}.")
    decoded = [pow(block, D, N) for block in ciphertext]
    if any(value >= len(ALPHABET) for value in decoded):
        raise ValueError("Один із блоків не відповідає цифрі вихідного алфавіту.")
    return "".join(str(value) for value in decoded)


def main() -> None:
    parser = argparse.ArgumentParser(description="Шифрування цифр методом RSA, варіант 12")
    parser.add_argument("mode", choices=("encrypt", "decrypt"))
    parser.add_argument("source", type=Path)
    parser.add_argument("destination", type=Path)
    args = parser.parse_args()
    try:
        source = args.source.read_text(encoding="utf-8").strip()
        if args.mode == "encrypt":
            result = " ".join(map(str, encrypt(source)))
        else:
            result = decrypt([int(token) for token in source.split()])
        with args.destination.open("x", encoding="utf-8", newline="\n") as output:
            output.write(result + "\n")
    except (OSError, ValueError) as error:
        parser.exit(1, f"Помилка: {error}\n")
    print(f"Відкритий ключ (e, N) = ({E}, {N})")
    print(f"Результат: {result}")
    print(f"Збережено у {args.destination}")


if __name__ == "__main__":
    main()
