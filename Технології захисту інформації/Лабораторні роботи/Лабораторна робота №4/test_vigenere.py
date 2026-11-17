import contextlib
import io
import tempfile
import unittest
from pathlib import Path

from vigenere import ALPHABET, decrypt, encrypt, generate_key, run


class VigenereTests(unittest.TestCase):
    def test_shift_wraps_in_both_directions(self):
        self.assertEqual(encrypt("Я", "Б"), "А")
        self.assertEqual(decrypt("А", "Б"), "Я")

    def test_different_shifts_for_same_letter(self):
        self.assertEqual(encrypt("ААА", "АБВ"), "АБВ")

    def test_generated_key(self):
        key = generate_key(12)
        self.assertEqual(len(key), 12)
        self.assertTrue(set(key) <= set(ALPHABET))

    def test_rejects_wrong_key_length(self):
        with self.assertRaises(ValueError):
            decrypt("АБ", "А")

    def test_rejects_symbol_outside_alphabet(self):
        with self.assertRaises(ValueError):
            encrypt("A", "А")

    def test_four_files_and_round_trip(self):
        with tempfile.TemporaryDirectory() as folder:
            source = Path(folder) / "input.txt"
            source.write_text("повідомлення\n", encoding="utf-8")
            output = Path(folder) / "result"
            with contextlib.redirect_stdout(io.StringIO()):
                run(source, output)
            self.assertEqual(
                {path.name for path in output.iterdir()},
                {"message.txt", "encrypted.txt", "key.txt", "decrypted.txt"},
            )
            files = {path.stem: path.read_text(encoding="utf-8").strip()
                     for path in output.iterdir()}
            self.assertEqual(files["decrypted"], "ПОВІДОМЛЕННЯ")
            self.assertEqual(decrypt(files["encrypted"], files["key"]), files["message"])


if __name__ == "__main__":
    unittest.main()
