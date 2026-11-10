"""Автоматичні перевірки лабораторної роботи № 6."""

from pathlib import Path
import sys
import unittest

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from solve_lab6 import (  # noqa: E402
    POINTS,
    Q,
    conditional_center_of_mass,
    geometric_median,
    solve,
    sum_distances,
    weighted_squared_criterion,
)


class WarehouseLocationTests(unittest.TestCase):
    def test_source_data(self) -> None:
        self.assertEqual(POINTS.shape, (10, 2))
        self.assertEqual(int(Q.sum()), 35)

    def test_initial_position(self) -> None:
        position, history = geometric_median()
        self.assertTrue(np.allclose(position, [6.0, 4.0], atol=1e-8))
        self.assertAlmostEqual(sum_distances(position), 32.6539920374708)
        self.assertGreater(len(history), 1)

    def test_initial_position_is_geometric_median(self) -> None:
        position, _ = geometric_median()
        perturbations = np.array([[0.001, 0], [-0.001, 0], [0, 0.001], [0, -0.001]])
        self.assertTrue(all(sum_distances(position) <= sum_distances(position + delta) for delta in perturbations))

    def test_conditional_center_of_mass(self) -> None:
        center = conditional_center_of_mass()
        self.assertTrue(np.allclose(center, [5.2, 4.0]))

    def test_center_minimizes_weighted_squared_criterion(self) -> None:
        center = conditional_center_of_mass()
        self.assertAlmostEqual(weighted_squared_criterion(center), 389.6)
        self.assertLess(weighted_squared_criterion(center), weighted_squared_criterion(np.array([6.0, 4.0])))

    def test_distances(self) -> None:
        result = solve()
        self.assertAlmostEqual(result.initial_distances[4], 0.0)
        self.assertAlmostEqual(result.center_distances[4], 0.8)
        self.assertAlmostEqual(result.center_distances[8], np.sqrt(4.04))


if __name__ == "__main__":
    unittest.main(verbosity=2)
