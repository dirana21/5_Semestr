"""Автоматична перевірка розрахунків лабораторної роботи №3."""

from pathlib import Path
import math
import sys
import unittest


SRC_DIR = Path(__file__).resolve().parents[1] / "src"
sys.path.insert(0, str(SRC_DIR))

from solve_lab3 import Problem, objective, solve_problem  # noqa: E402


class SolutionTests(unittest.TestCase):
    def setUp(self) -> None:
        self.problem = Problem()
        self.solution = solve_problem(self.problem)

    def assert_feasible(self, x1: float, x2: float) -> None:
        self.assertGreaterEqual(x1, -1e-10)
        self.assertGreaterEqual(x2, -1e-10)
        self.assertLessEqual(x1**2 + x2**2, self.problem.n**2 + 1e-8)
        self.assertAlmostEqual(x2, self.problem.n * x1, places=8)

    def test_minimum_exact_values(self) -> None:
        self.assertAlmostEqual(self.solution.minimum.x1, 12 / 145, places=12)
        self.assertAlmostEqual(self.solution.minimum.x2, 144 / 145, places=12)
        self.assertAlmostEqual(self.solution.minimum.value, -144 / 145, places=12)

    def test_maximum_exact_values(self) -> None:
        self.assertAlmostEqual(self.solution.maximum.x1, 12 / math.sqrt(145), places=12)
        self.assertAlmostEqual(self.solution.maximum.x2, 144 / math.sqrt(145), places=12)
        self.assertAlmostEqual(
            self.solution.maximum.value,
            144 - 288 / math.sqrt(145),
            places=10,
        )

    def test_extrema_are_feasible(self) -> None:
        self.assert_feasible(self.solution.minimum.x1, self.solution.minimum.x2)
        self.assert_feasible(self.solution.maximum.x1, self.solution.maximum.x2)

    def test_objective_and_numerical_verification(self) -> None:
        self.assertAlmostEqual(
            objective(self.problem, self.solution.minimum.x1, self.solution.minimum.x2),
            self.solution.minimum.value,
            places=12,
        )
        self.assertLess(self.solution.numerical_error, 1e-6)


if __name__ == "__main__":
    unittest.main()
