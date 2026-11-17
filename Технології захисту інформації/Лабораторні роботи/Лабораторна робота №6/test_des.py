import unittest

from des import permute, round_keys, transform_block
from des_cbc import cbc_blocks, decrypt, encrypt
from des_tables import FP, IP


KEY = bytes.fromhex("0123456789ABCDEF")
IV = bytes.fromhex("1234567890ABCDEF")


class DesTests(unittest.TestCase):
    def test_des_block(self):
        block = bytes.fromhex("0123456789ABCDEF")
        keys = round_keys(bytes.fromhex("133457799BBCDFF1"))
        expected = bytes.fromhex("85E813540F0AB405")
        self.assertEqual(keys[0], 0x1B02EFFC7072)
        self.assertEqual(transform_block(block, keys), expected)
        self.assertEqual(transform_block(expected, reversed(keys)), block)

    def test_permutations_are_inverse(self):
        for bit in range(64):
            self.assertEqual(permute(permute(1 << bit, 64, IP), 64, FP), 1 << bit)

    def test_fips_81_cbc(self):
        message = b"Now is the time for all "
        expected = bytes.fromhex("E5C7CDDE872BF27C 43E934008C389C0F 683788499A7C05F6")
        self.assertEqual(cbc_blocks(message, KEY, IV), expected)
        self.assertEqual(cbc_blocks(expected, KEY, IV, decrypt=True), message)

    def test_padding_round_trip(self):
        for source in (b"", b"12345678", "Захист інформації!\n".encode()):
            with self.subTest(length=len(source)):
                encoded = encrypt(source, KEY, IV)
                self.assertGreater(len(encoded), len(source))
                self.assertEqual(decrypt(encoded, KEY, IV), source)

    def test_invalid_padding(self):
        ciphertext = cbc_blocks(b"invalid\x00", KEY, IV)
        with self.assertRaisesRegex(ValueError, "PKCS"):
            decrypt(ciphertext, KEY, IV)

    def test_invalid_lengths(self):
        for data, key, iv in ((b"123", KEY, IV), (b"12345678", b"bad", IV),
                              (b"12345678", KEY, b"bad")):
            with self.subTest(data=data, key=key, iv=iv), self.assertRaises(ValueError):
                cbc_blocks(data, key, iv)


if __name__ == "__main__":
    unittest.main()
