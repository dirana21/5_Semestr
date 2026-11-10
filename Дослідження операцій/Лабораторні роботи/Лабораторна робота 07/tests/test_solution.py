"""Автоматичні перевірки лабораторної роботи № 7."""

from pathlib import Path
import sys
import unittest

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from solve_lab7 import (  # noqa: E402
    GOMORY_COEFFICIENTS,
    GOMORY_RHS,
    enumerate_integer_points,
    final_simplex_tableau,
    gomory_cut_from_tableau,
    is_feasible,
    solve,
    solve_lp_relaxation,
)


class GomorySolutionTests(unittest.TestCase):
    def test_lp_relaxation(self) -> None:
        point, value = solve_lp_relaxation()
        self.assertTrue(np.allclose(point, [0.0, 6.5]))
        self.assertAlmostEqual(value, 6.5)

    def test_final_tableau(self) -> None:
        tableau = final_simplex_tableau()
        self.assertEqual(tableau.shape, (3, 5))
        self.assertAlmostEqual(tableau[0, 0], 6.5)
        self.assertAlmostEqual(tableau[0, 1], 1.5)
        self.assertAlmostEqual(tableau[0, 4], 0.5)

    def test_gomory_fractional_cut(self) -> None:
        coefficients, rhs = gomory_cut_from_tableau()
        self.assertTrue(np.allclose(coefficients, [0.5, 0.5]))
        self.assertAlmostEqual(rhs, 0.5)
        self.assertTrue(np.array_equal(GOMORY_COEFFICIENTS, [1.0, 1.0]))
        self.assertEqual(GOMORY_RHS, 6.0)

    def test_cut_removes_fractional_optimum(self) -> None:
        point, _ = solve_lp_relaxation()
        self.assertTrue(is_feasible(point, include_cut=False))
        self.assertFalse(is_feasible(point, include_cut=True))

    def test_integer_enumeration(self) -> None:
        points = enumerate_integer_points()
        self.assertEqual(len(points), 20)
        self.assertIn((0, 6, 6), points)
        self.assertIn((1, 5, 6), points)

    def test_integer_optima(self) -> None:
        solution = solve()
        self.assertEqual(solution.optima, ((0, 6, 6), (1, 5, 6)))
        self.assertEqual(solution.optima[0][2], 6)
        self.assertTrue(all(is_feasible(np.array(point[:2]), include_cut=True) for point in solution.optima))


if __name__ == "__main__":
    unittest.main(verbosity=2)
