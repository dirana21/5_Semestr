from pathlib import Path

from playfair_cipher import decrypt_file, print_square


keyword = "БЕЗПЕКА"
source = Path("encrypted.txt")
destination = Path("decrypted.txt")

print("Лабораторна робота №2. Варіант 12")
print(f"Вхідний файл: {source}")
print(f"Ключове слово: {keyword}")
print(f"Шифротекст: {source.read_text(encoding='utf-8')}")
print_square(keyword)
plaintext = decrypt_file(source, destination, keyword)
print(f"\nРозшифрований текст: {plaintext}")
print(f"Результат записано у файл: {destination}")
