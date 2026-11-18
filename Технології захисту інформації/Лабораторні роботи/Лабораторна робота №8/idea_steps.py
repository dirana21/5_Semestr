"""Операції 5–9 раунду шифрування IDEA, варіант 2."""

import argparse
from typing import NamedTuple


WORD_MODULUS = 1 << 16
PRODUCT_MODULUS = WORD_MODULUS + 1


class Steps(NamedTuple):
    step5: int
    step6: int
    step7: int
    step8: int
    step9: int


def multiply(left: int, right: int) -> int:
    """Множення IDEA з кодуванням числа 65536 словом 0000."""
    product = ((left or WORD_MODULUS) * (right or WORD_MODULUS)) % PRODUCT_MODULUS
    return product % WORD_MODULUS


def round_steps(a: int, b: int, c: int, d: int, z5: int, z6: int) -> Steps:
    """Приймає результати кроків 1–4 та два останні підключі раунду."""
    if any(not 0 <= word < WORD_MODULUS for word in (a, b, c, d, z5, z6)):
        raise ValueError("Кожне вхідне слово має належати діапазону 0000–FFFF.")

    step5 = a ^ c
    step6 = b ^ d
    step7 = multiply(step5, z5)
    step8 = (step6 + step7) % WORD_MODULUS
    step9 = multiply(step8, z6)
    return Steps(step5, step6, step7, step8, step9)


def main() -> None:
    parser = argparse.ArgumentParser(description="IDEA, операції 5–9 раунду")
    parser.add_argument("--words", nargs=4, metavar="HEX", type=lambda s: int(s, 16),
                        default=(0, 3, 5, 12), help="Результати операцій 1–4")
    parser.add_argument("--keys", nargs=2, metavar="HEX", type=lambda s: int(s, 16),
                        default=(5, 6), help="Підключі Z5 і Z6")
    args = parser.parse_args()
    try:
        result = round_steps(*args.words, *args.keys)
    except ValueError as error:
        parser.error(str(error))

    print("Результати кроків 1–4:", " ".join(f"{word:04X}" for word in args.words))
    print("Підключі Z5, Z6:", " ".join(f"{word:04X}" for word in args.keys))
    for number, value in enumerate(result, 5):
        print(f"Крок {number}: {value:04X} ({value})")


if __name__ == "__main__":
    main()
