import tempfile
import unittest
from itertools import islice
from pathlib import Path

from gamma_cipher import run, transform
from generators import SEED, additive_step, cycle, gamma_bytes


class GammaCipherTests(unittest.TestCase):
    def test_periods(self):
        self.assertEqual(cycle(SEED, additive_step), (0, 6144))
        self.assertEqual(cycle(4003, lambda x: (5 * x + 7) % 4096), (0, 4096))
        self.assertEqual(cycle(502, lambda x: (7 * x) % 4096), (0, 256))

    def test_first_gamma_block(self):
        self.assertEqual(bytes(islice(gamma_bytes(), 8)).hex(), "fa303bfde019ff70")

    def test_known_xor(self):
        self.assertEqual(transform("Г".encode()), bytes.fromhex("2a a3"))
        self.assertEqual(transform(bytes.fromhex("2a a3")), "Г".encode())

    def test_empty_and_partial_blocks(self):
        for source in (b"", bytes(range(9)), bytes(range(17))):
            with self.subTest(length=len(source)):
                encoded = transform(source)
                self.assertEqual(len(encoded), len(source))
                self.assertEqual(transform(encoded), source)

    def test_files_restore_exact_bytes(self):
        with tempfile.TemporaryDirectory() as folder:
            directory = Path(folder)
            source = "Гамування.\r\n".encode()
            (directory / "Source.txt").write_bytes(source)
            run("encrypt", directory)
            run("decrypt", directory)
            self.assertEqual((directory / "DeCoded.txt").read_bytes(), source)


if __name__ == "__main__":
    unittest.main()
