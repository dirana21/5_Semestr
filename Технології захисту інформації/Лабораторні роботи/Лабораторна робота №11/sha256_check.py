"""Обчислення SHA-256 файлу та порівняння з еталоном."""

import argparse
import hashlib
import re
import sys
from pathlib import Path


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        while chunk := stream.read(4096):
            digest.update(chunk)
    return digest.hexdigest()


def main() -> int:
    parser = argparse.ArgumentParser(description="Перевірка SHA-256 файлу.")
    parser.add_argument("file", type=Path, help="файл для перевірки")
    parser.add_argument("--expected", help="еталонний SHA-256 із 64 hex-символів")
    args = parser.parse_args()

    if args.expected is not None and not re.fullmatch(r"[0-9a-fA-F]{64}", args.expected):
        parser.error("Еталон має містити рівно 64 шістнадцяткові символи.")

    try:
        actual = sha256_file(args.file)
    except OSError as error:
        print(f"Помилка читання: {error}", file=sys.stderr)
        return 2

    print(actual)
    if args.expected is None:
        return 0

    expected = args.expected.lower()
    changed_bits = (int(actual, 16) ^ int(expected, 16)).bit_count()
    print(f"Еталон: {expected}")
    print(f"Відмінних бітів хешу: {changed_bits} з 256")
    print("Результат: хеші збігаються." if not changed_bits else "Результат: хеші різні.")
    return int(changed_bits != 0)


if __name__ == "__main__":
    sys.exit(main())
