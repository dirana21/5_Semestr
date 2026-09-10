import unittest

from transposition_cipher import decrypt, encrypt_for_check, parse_row_key


class RowTranspositionTests(unittest.TestCase):
    def test_decrypt_known_ciphertext(self):
        self.assertEqual(decrypt("НЗСИАТХХД_ИА", (2, 3, 1)), "ЗАХИСТДАНИХ")

    def test_encrypt_and_decrypt(self):
        source = "ТЕХНОЛОГІЇ ЗАХИСТУ"
        key = (3, 1, 4, 2)
        self.assertEqual(decrypt(encrypt_for_check(source, key), key), source)

    def test_key_can_use_commas(self):
        self.assertEqual(parse_row_key("2, 3, 1"), (2, 3, 1))

    def test_repeated_number_in_key_is_rejected(self):
        with self.assertRaises(ValueError):
            parse_row_key("1 1 3")

    def test_incomplete_table_is_rejected(self):
        with self.assertRaises(ValueError):
            decrypt("АБВГД", (2, 3, 1))

    def test_empty_ciphertext_is_rejected(self):
        with self.assertRaises(ValueError):
            decrypt("", (2, 3, 1))


if __name__ == "__main__":
    unittest.main()
