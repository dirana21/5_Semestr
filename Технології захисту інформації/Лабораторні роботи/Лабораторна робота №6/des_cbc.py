"""Файловий режим CBC із доповненням PKCS#7."""

import argparse
from pathlib import Path

from des import BLOCK_SIZE, round_keys, transform_block


def xor_block(left: bytes, right: bytes) -> bytes:
    return bytes(a ^ b for a, b in zip(left, right))


def cbc_blocks(data: bytes, key: bytes, iv: bytes, *, decrypt: bool = False) -> bytes:
    if len(iv) != BLOCK_SIZE:
        raise ValueError("IV має містити 8 байтів.")
    if len(data) % BLOCK_SIZE:
        raise ValueError("Довжина даних має бути кратною 8 байтам.")
    keys = round_keys(key)
    if decrypt:
        keys = keys[::-1]

    previous = iv
    result = bytearray()
    for offset in range(0, len(data), BLOCK_SIZE):
        block = data[offset : offset + BLOCK_SIZE]
        if decrypt:
            result.extend(xor_block(transform_block(block, keys), previous))
            previous = block
        else:
            previous = transform_block(xor_block(block, previous), keys)
            result.extend(previous)
    return bytes(result)


def encrypt(data: bytes, key: bytes, iv: bytes) -> bytes:
    pad_size = BLOCK_SIZE - len(data) % BLOCK_SIZE
    return cbc_blocks(data + bytes([pad_size]) * pad_size, key, iv)


def decrypt(ciphertext: bytes, key: bytes, iv: bytes) -> bytes:
    if not ciphertext:
        raise ValueError("Шифротекст порожній.")
    data = cbc_blocks(ciphertext, key, iv, decrypt=True)
    pad_size = data[-1]
    if not 1 <= pad_size <= BLOCK_SIZE or data[-pad_size:] != bytes([pad_size]) * pad_size:
        raise ValueError("Некоректне доповнення PKCS#7.")
    return data[:-pad_size]


def main() -> None:
    parser = argparse.ArgumentParser(description="DES-CBC, варіант 4")
    parser.add_argument("mode", choices=("encrypt", "decrypt"))
    parser.add_argument("source", type=Path)
    parser.add_argument("destination", type=Path)
    parser.add_argument("--key", required=True, help="8 байтів у HEX")
    parser.add_argument("--iv", required=True, help="8 байтів у HEX")
    args = parser.parse_args()
    try:
        key, iv = bytes.fromhex(args.key), bytes.fromhex(args.iv)
        operation = encrypt if args.mode == "encrypt" else decrypt
        result = operation(args.source.read_bytes(), key, iv)
        with args.destination.open("xb") as output:
            output.write(result)
    except (OSError, ValueError) as error:
        parser.exit(1, f"Помилка: {error}\n")
    print(f"Записано {len(result)} байтів у {args.destination}")


if __name__ == "__main__":
    main()
