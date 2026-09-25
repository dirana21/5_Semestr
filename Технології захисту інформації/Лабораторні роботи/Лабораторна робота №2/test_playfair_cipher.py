import tempfile
import unittest
from pathlib import Path

from playfair_cipher import (
    ALPHABET,
    build_square,
    decrypt,
    decrypt_file,
    encrypt_for_check,
    prepare_plaintext,
)


class PlayfairCipherTests(unittest.TestCase):
    def test_square_contains_every_symbol_once(self):
        square = build_square("БЕЗПЕКА")
        symbols = "".join("".join(row) for row in square)
        self.assertEqual(len(symbols), 36)
        self.assertEqual(set(symbols), set(ALPHABET))

    def test_keyword_symbols_go_first_without_repeats(self):
        square = build_square("БЕЗПЕКА")
        self.assertTrue("".join(square[0]).startswith("БЕЗПКА"))

    def test_decrypt_known_ciphertext(self):
        self.assertEqual(decrypt("ПБФІТУПЙБУІФ", "БЕЗПЕКА"), "ЗАХИСТ ДАНИХ")

    def test_round_trip(self):
        source = "КОНФІДЕНЦІЙНІ ДАНІ."
        keyword = "КРИПТОГРАФІЯ"
        encrypted = encrypt_for_check(source, keyword)
        self.assertEqual(decrypt(encrypted, keyword), prepare_plaintext(source))

    def test_odd_ciphertext_is_rejected(self):
        with self.assertRaises(ValueError):
            decrypt("АБВ", "КЛЮЧ")

    def test_unknown_symbol_is_rejected(self):
        with self.assertRaises(ValueError):
            decrypt("А!", "КЛЮЧ")

    def test_file_is_decrypted_and_saved(self):
        with tempfile.TemporaryDirectory() as directory:
            source = Path(directory) / "encrypted.txt"
            destination = Path(directory) / "decrypted.txt"
            source.write_text("ПБФІТУПЙБУІФ", encoding="utf-8")
            result = decrypt_file(source, destination, "БЕЗПЕКА")
            self.assertEqual(result, "ЗАХИСТ ДАНИХ")
            self.assertEqual(destination.read_text(encoding="utf-8"), result)


if __name__ == "__main__":
    unittest.main()
