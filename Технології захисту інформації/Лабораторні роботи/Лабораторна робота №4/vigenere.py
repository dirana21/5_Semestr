"""Шифр Віженера з випадковим ключем на довжину повідомлення."""

import argparse
from pathlib import Path
from secrets import choice


ALPHABET = "АБВГҐДЕЄЖЗИІЇЙКЛМНОПРСТУФХЦЧШЩЬЮЯ"
INDICES = {letter: index for index, letter in enumerate(ALPHABET)}


def generate_key(length: int) -> str:
    return "".join(choice(ALPHABET) for _ in range(length))


def transform(text: str, key: str, direction: int) -> str:
    if not text or len(text) != len(key):
        raise ValueError("Текст має бути непорожнім, а ключ — такої самої довжини.")
    if set(text + key) - INDICES.keys():
        raise ValueError("Текст і ключ мають містити лише великі українські літери.")

    result = []
    for letter, key_letter in zip(text, key):
        index = (INDICES[letter] + direction * INDICES[key_letter]) % len(ALPHABET)
        result.append(ALPHABET[index])
    return "".join(result)


def encrypt(text: str, key: str) -> str:
    return transform(text, key, 1)


def decrypt(ciphertext: str, key: str) -> str:
    return transform(ciphertext, key, -1)


def run(input_path: Path, output_dir: Path) -> None:
    text = input_path.read_text(encoding="utf-8").strip().upper()
    key = generate_key(len(text))
    ciphertext = encrypt(text, key)

    output_dir.mkdir()
    (output_dir / "message.txt").write_text(text + "\n", encoding="utf-8")
    (output_dir / "key.txt").write_text(key + "\n", encoding="utf-8")
    (output_dir / "encrypted.txt").write_text(ciphertext + "\n", encoding="utf-8")

    saved_key = (output_dir / "key.txt").read_text(encoding="utf-8").strip()
    saved_ciphertext = (output_dir / "encrypted.txt").read_text(encoding="utf-8").strip()
    restored = decrypt(saved_ciphertext, saved_key)
    (output_dir / "decrypted.txt").write_text(restored + "\n", encoding="utf-8")

    print(f"Вихідне повідомлення: {text}")
    print(f"Шифротекст: {ciphertext}")
    print(f"Відновлене повідомлення: {restored}")
    print(f"Файли записано до {output_dir}")


def main() -> None:
    parser = argparse.ArgumentParser(description="Шифр Віженера, варіант 12")
    parser.add_argument("input", type=Path, help="Вхідний файл UTF-8")
    parser.add_argument("output", type=Path, help="Нова папка для результатів")
    args = parser.parse_args()
    try:
        run(args.input, args.output)
    except (OSError, ValueError) as error:
        parser.exit(1, f"Помилка: {error}\n")


if __name__ == "__main__":
    main()
