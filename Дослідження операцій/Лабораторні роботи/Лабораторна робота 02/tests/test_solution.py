"""Автоматична перевірка розрахунків лабораторної роботи №2."""

from pathlib import Path
import sys
import unittest

import numpy as np


SRC_DIR = Path(__file__).resolve().parents[1] / "src"
sys.path.insert(0, str(SRC_DIR))

from solve_lab2 import generate_problem, solve_problem  # noqa: E402


class SolutionTests(unittest.TestCase):
    def setUp(self) -> None:
        self.problem = generate_problem()
        self.solution = solve_problem(self.problem)

    def test_generated_coefficients_are_reproducible(self) -> None:
        expected = np.array(
            [
                [7, 11, 21, 21, 22],
                [1, 7, 23, 9, 17],
                [4, 11, 19, 12, 20],
                [3, 7, 2, 4, 17],
                [20, 5, 14, 2, 10],
            ],
            dtype=float,
        )
        np.testing.assert_array_equal(self.problem.coefficients, expected)
        np.testing.assert_array_equal(self.problem.profit, [209, 198, 95, 33, 80])
        np.testing.assert_array_equal(self.problem.limits, [2400, 3600, 2880, 4800, 1920])

    def test_optimal_plan(self) -> None:
        expected = np.array([1824 / 37, 6912 / 37, 0, 0, 0])
        np.testing.assert_allclose(self.solution.quantities, expected, rtol=0, atol=1e-8)
        self.assertAlmostEqual(self.solution.objective, 1749792 / 37, places=7)

    def test_solution_is_feasible(self) -> None:
        self.assertTrue(np.all(self.solution.quantities >= -1e-9))
        self.assertTrue(np.all(self.solution.used <= self.problem.limits + 1e-8))

    def test_active_constraints(self) -> None:
        self.assertAlmostEqual(self.solution.slack[0], 0, places=8)
        self.assertAlmostEqual(self.solution.slack[4], 0, places=8)
        self.assertTrue(np.all(self.solution.slack[1:4] > 0))


if __name__ == "__main__":
    unittest.main()
