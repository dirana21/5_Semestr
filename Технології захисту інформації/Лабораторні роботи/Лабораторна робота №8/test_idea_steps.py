import unittest

from idea_steps import multiply, round_steps


class IdeaStepsTests(unittest.TestCase):
    def test_first_round_example(self):
        self.assertEqual(round_steps(0, 3, 5, 12, 5, 6), (5, 15, 25, 40, 240))

    def test_wraparound_and_zero_key(self):
        self.assertEqual(
            round_steps(0xFFFE, 0xFFFF, 0, 0, 1, 0),
            (0xFFFE, 0xFFFF, 0xFFFE, 0xFFFD, 4),
        )

    def test_zero_word_multiplication(self):
        self.assertEqual(multiply(0, 0), 1)
        self.assertEqual(multiply(0, 1), 0)
        self.assertEqual(multiply(0, 2), 0xFFFF)

    def test_zero_after_xor(self):
        self.assertEqual(round_steps(7, 8, 7, 8, 1, 1), (0, 0, 0, 0, 0))

    def test_invalid_word(self):
        for word in (-1, 0x10000):
            with self.subTest(word=word), self.assertRaises(ValueError):
                round_steps(0, 3, 5, 12, 5, word)


if __name__ == "__main__":
    unittest.main()
