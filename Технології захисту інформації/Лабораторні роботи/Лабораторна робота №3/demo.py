from vernam import decrypt


CIPHERTEXT = "0B FA 66 6B BC 33 0B D5 67 5A BC 34 FB BC 20 0B D0 67 5F BD 08 0A ED 66 67 BD 06 0A EB 67 4D BC 21 FA"

if __name__ == "__main__":
    print("Лабораторна робота №3. Варіант 6")
    print("Параметри: y0 = 4003, y1 = 59, m = 4096")
    print("Шифротекст (HEX):", CIPHERTEXT)
    print("Відновлений текст:", decrypt(CIPHERTEXT, 4003, 59, 4096))
