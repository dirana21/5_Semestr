import unittest

from rsa import D, E, N, PHI, decrypt, encrypt


class RsaTests(unittest.TestCase):
    def test_variant_parameters(self):
        self.assertEqual((N, PHI, E, D), (39, 24, 5, 5))
        self.assertEqual(E * D % PHI, 1)

    def test_all_ten_digits(self):
        cipher = [0, 1, 32, 9, 10, 5, 15, 37, 8, 3]
        self.assertEqual(encrypt("0123456789"), cipher)
        self.assertEqual(decrypt(cipher), "0123456789")

    def test_preserves_leading_zeros_and_repetitions(self):
        self.assertEqual(decrypt(encrypt("0077700")), "0077700")

    def test_rejects_bad_plaintext(self):
        for value in ("", "123A", "1 2", "١"):
            with self.subTest(value=value), self.assertRaises(ValueError):
                encrypt(value)

    def test_rejects_bad_ciphertext(self):
        for value in ([], [-1], [39], [38]):
            with self.subTest(value=value), self.assertRaises(ValueError):
                decrypt(value)


if __name__ == "__main__":
    unittest.main()
