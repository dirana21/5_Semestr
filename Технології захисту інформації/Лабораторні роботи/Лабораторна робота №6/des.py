"""Навчальна реалізація 16 раундів DES."""

from collections.abc import Iterable

from des_tables import E, FP, IP, P, PC1, PC2, SHIFTS, S_BOXES


BLOCK_SIZE = 8
HALF_MASK = (1 << 28) - 1


def permute(value: int, width: int, table: tuple[int, ...]) -> int:
    result = 0
    for position in table:
        result = (result << 1) | ((value >> (width - position)) & 1)
    return result


def round_keys(key: bytes) -> tuple[int, ...]:
    if len(key) != BLOCK_SIZE:
        raise ValueError("Ключ DES має містити 8 байтів.")
    selected = permute(int.from_bytes(key, "big"), 64, PC1)
    left, right = selected >> 28, selected & HALF_MASK
    keys = []
    for shift in SHIFTS:
        left = ((left << shift) | (left >> (28 - shift))) & HALF_MASK
        right = ((right << shift) | (right >> (28 - shift))) & HALF_MASK
        keys.append(permute((left << 28) | right, 56, PC2))
    return tuple(keys)


def feistel(right: int, key: int) -> int:
    mixed = permute(right, 32, E) ^ key
    substituted = 0
    for index, box in enumerate(S_BOXES):
        group = (mixed >> (42 - 6 * index)) & 0x3F
        row = ((group >> 5) << 1) | (group & 1)
        column = (group >> 1) & 0xF
        substituted = (substituted << 4) | box[row][column]
    return permute(substituted, 32, P)


def transform_block(block: bytes, keys: Iterable[int]) -> bytes:
    if len(block) != BLOCK_SIZE:
        raise ValueError("Блок DES має містити 8 байтів.")
    initial = permute(int.from_bytes(block, "big"), 64, IP)
    left, right = initial >> 32, initial & 0xFFFFFFFF
    for key in keys:
        left, right = right, left ^ feistel(right, key)
    final = permute((right << 32) | left, 64, FP)
    return final.to_bytes(BLOCK_SIZE, "big")
