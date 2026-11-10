"""Автоматичні перевірки лабораторної роботи № 5."""

from math import ceil
from pathlib import Path
import sys
import unittest

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from solve_lab5 import (  # noqa: E402
    CAPACITY,
    DEMANDS,
    build_adjacency,
    exact_cvrp,
    floyd_warshall,
    minimum_tree_edges,
    minimum_tree_plan,
    sweep_groups,
    sweep_plan,
    tree_schemes,
)


class RoutingSolutionTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.distance, _ = floyd_warshall(build_adjacency())

    def test_demands_capacity_and_route_count(self) -> None:
        self.assertEqual(int(DEMANDS.sum()), 223)
        self.assertEqual(CAPACITY, 100)
        self.assertEqual(ceil(DEMANDS.sum() / CAPACITY), 3)

    def test_distance_matrix(self) -> None:
        self.assertTrue(np.allclose(self.distance, self.distance.T))
        self.assertTrue(np.allclose(np.diag(self.distance), 0))
        self.assertAlmostEqual(self.distance[0, 10], 89.5)

    def test_minimum_tree_schemes(self) -> None:
        self.assertEqual(len(minimum_tree_edges()), 10)
        self.assertAlmostEqual(sum(edge[2] for edge in minimum_tree_edges()), 312.7)
        totals = [sum(edge[2] for edge in edges) for _, edges in tree_schemes()]
        self.assertEqual([round(value, 1) for value in totals], [312.7, 312.7, 315.3])

    def test_tree_routes_are_feasible(self) -> None:
        plan = minimum_tree_plan(self.distance)
        self.assertEqual(sorted(plan.loads), [57, 69, 97])
        self.assertTrue(all(load <= CAPACITY for load in plan.loads))
        self.assertAlmostEqual(plan.total_length, 537.8)

    def test_sweep_groups_and_routes(self) -> None:
        self.assertEqual(sweep_groups(), [[9, 2, 3, 1], [4, 6, 5, 10, 7], [8]])
        plan = sweep_plan(self.distance)
        self.assertEqual(plan.loads, (96, 100, 27))
        self.assertAlmostEqual(plan.total_length, 619.9)

    def test_exact_solution_is_best(self) -> None:
        tree = minimum_tree_plan(self.distance)
        sweep = sweep_plan(self.distance)
        exact = exact_cvrp(self.distance)
        self.assertEqual(exact.loads, (87, 46, 90))
        self.assertAlmostEqual(exact.total_length, 536.9)
        self.assertLessEqual(exact.total_length, tree.total_length)
        self.assertLessEqual(exact.total_length, sweep.total_length)


if __name__ == "__main__":
    unittest.main(verbosity=2)
