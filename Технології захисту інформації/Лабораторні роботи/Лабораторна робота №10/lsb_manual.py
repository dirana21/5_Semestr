"""Запис і читання UTF-8 у молодших бітах каналів RGB."""

from PIL import Image


SIGNATURE = b"LSB1"
HEADER_BYTES = len(SIGNATURE) + 4


def hide(image: Image.Image, message: str) -> Image.Image:
    """Повернути копію RGB-зображення з вбудованим повідомленням."""
    rgb = image.convert("RGB")
    channels = bytearray(rgb.tobytes())
    payload = message.encode("utf-8")
    if (HEADER_BYTES + len(payload)) * 8 > len(channels):
        raise ValueError("Повідомлення не вміщується у зображення.")

    header = SIGNATURE + len(payload).to_bytes(4, "big")
    channel_index = 0
    for value in header + payload:
        for shift in range(7, -1, -1):
            bit = (value >> shift) & 1
            channels[channel_index] = (channels[channel_index] & 0xFE) | bit
            channel_index += 1

    return Image.frombytes("RGB", rgb.size, bytes(channels))


def read_bytes(channels: bytes, offset: int, count: int) -> bytes:
    """Прочитати count байтів, починаючи з каналу offset."""
    result = bytearray()
    for start in range(offset, offset + count * 8, 8):
        value = 0
        for channel in channels[start : start + 8]:
            value = (value << 1) | (channel & 1)
        result.append(value)
    return bytes(result)


def reveal(image: Image.Image) -> str:
    """Повернути повідомлення після перевірки заголовка."""
    channels = image.convert("RGB").tobytes()
    header_bits = HEADER_BYTES * 8
    if len(channels) < header_bits:
        raise ValueError("Зображення замале для заголовка.")

    header = read_bytes(channels, 0, HEADER_BYTES)
    if not header.startswith(SIGNATURE):
        raise ValueError("У зображенні відсутня сигнатура LSB1.")

    length = int.from_bytes(header[len(SIGNATURE) :], "big")
    if length * 8 > len(channels) - header_bits:
        raise ValueError("Довжина в заголовку перевищує місткість зображення.")

    return read_bytes(channels, header_bits, length).decode("utf-8")
