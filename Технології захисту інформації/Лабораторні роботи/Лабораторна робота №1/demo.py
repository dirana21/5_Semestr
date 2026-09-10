from transposition_cipher import decrypt, print_table


ciphertext = "НЗСИАТХХД_ИА"
row_key = (2, 3, 1)

print("Лабораторна робота №1. Варіант 12")
print(f"Шифротекст: {ciphertext}")
print(f"Ключ рядків: {' '.join(map(str, row_key))}")
print_table(ciphertext, len(row_key))
print(f"\nРозшифроване повідомлення: {decrypt(ciphertext, row_key)}")
