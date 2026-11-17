"""Шифрування та дешифрування файла гамуванням."""

import argparse
from itertools import islice
from pathlib import Path

from generators import gamma_bytes


BLOCK_SIZE = 8
FILES = {
    "encrypt": ("Source.txt", "Coded.txt"),
    "decrypt": ("Coded.txt", "DeCoded.txt"),
}


def transform(data: bytes) -> bytes:
    gamma = gamma_bytes()
    result = bytearray()
    for offset in range(0, len(data), BLOCK_SIZE):
        block = data[offset : offset + BLOCK_SIZE]
        mask = islice(gamma, len(block))
        result.extend(byte ^ key_byte for byte, key_byte in zip(block, mask))
    return bytes(result)


def run(mode: str, directory: Path) -> Path:
    source, destination = (directory / name for name in FILES[mode])
    result = transform(source.read_bytes())
    destination.write_bytes(result)
    return destination


def main() -> None:
    parser = argparse.ArgumentParser(description="Шифрування методом гамування, варіант 12")
    parser.add_argument("mode", choices=FILES)
    parser.add_argument("directory", type=Path, nargs="?", default=Path("."))
    args = parser.parse_args()
    try:
        destination = run(args.mode, args.directory)
    except OSError as error:
        parser.exit(1, f"Помилка: {error}\n")
    print(f"Результат записано у {destination}")


if __name__ == "__main__":
    main()
