"""Автоматична перевірка обчислень лабораторної роботи №1."""

from fractions import Fraction
from pathlib import Path
import sys
import unittest


SRC_DIR = Path(__file__).resolve().parents[1] / "src"
sys.path.insert(0, str(SRC_DIR))

from solve_lab1 import Problem, continuous_vertices, integer_optimum, objective  # noqa: E402


class SolutionTests(unittest.TestCase):
    def setUp(self) -> None:
        self.problem = Problem(n=12, k=Fraction(1, 2))

    def test_variant_coefficients(self) -> None:
        self.assertEqual(self.problem.sa, Fraction(3))
        self.assertEqual(self.problem.ta, Fraction(24))
        self.assertEqual(self.problem.sb, Fraction(12))
        self.assertEqual(self.problem.tb, Fraction(12, 5))
        self.assertEqual(self.problem.wa, Fraction(6))
        self.assertEqual(self.problem.wb, Fraction(36, 5))

    def test_continuous_optimum(self) -> None:
        vertices = continuous_vertices(self.problem)
        optimum = max(vertices, key=lambda point: objective(self.problem, point))
        self.assertEqual(optimum, (Fraction(700, 13), Fraction(5000, 39)))
        self.assertEqual(objective(self.problem, optimum), Fraction(16200, 13))

    def test_optimum_exhausts_resources(self) -> None:
        x_a, x_b = Fraction(700, 13), Fraction(5000, 39)
        self.assertEqual(self.problem.sa * x_a + self.problem.sb * x_b, 1700)
        self.assertEqual(self.problem.ta * x_a + self.problem.tb * x_b, 1600)

    def test_integer_optimum(self) -> None:
        point, value = integer_optimum(self.problem)
        self.assertEqual(point, (Fraction(53), Fraction(128)))
        self.assertEqual(value, Fraction(6198, 5))


if __name__ == "__main__":
    unittest.main()
