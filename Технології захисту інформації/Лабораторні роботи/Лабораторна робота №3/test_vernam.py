import unittest
from itertools import islice

from vernam import additive_sequence, decrypt, xor_data


class VernamTests(unittest.TestCase):
    def test_additive_sequence(self):
        sequence = additive_sequence(4003, 59, 4096)
        self.assertEqual(list(islice(sequence, 5)), [4003, 59, 4062, 25, 4087])

    def test_first_gamma_byte(self):
        # Молодші біти перших восьми чисел: 11011011.
        self.assertEqual(xor_data(b"\x00", 4003, 59, 4096), b"\xdb")

    def test_round_trip_utf8(self):
        source = "Захист інформації!"
        key = (4003, 59, 4096)
        ciphertext = xor_data(source.encode("utf-8"), *key)
        self.assertEqual(decrypt(ciphertext.hex(), *key), source)

    def test_invalid_hex(self):
        with self.assertRaises(ValueError):
            decrypt("GG", 4003, 59, 4096)

    def test_invalid_parameters(self):
        with self.assertRaises(ValueError):
            decrypt("00", 4003, 59, 1)


if __name__ == "__main__":
    unittest.main()
