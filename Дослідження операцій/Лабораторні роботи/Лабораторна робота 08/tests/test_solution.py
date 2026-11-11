"""Автоматичні перевірки лабораторної роботи № 8."""

from pathlib import Path
import math
import sys
import unittest

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from solve_lab8 import (  # noqa: E402
    A_VALUE,
    START,
    TARGET,
    bellman_ford_cost,
    build_edges,
    build_graph,
    edge_weight,
    enumerate_monotone_paths,
    evaluate_expression,
    solve,
)


EXPECTED_PATH = (
    (4, 0),
    (3, 0),
    (2, 0),
    (2, 1),
    (2, 2),
    (1, 2),
    (1, 3),
    (1, 4),
    (0, 4),
)


class ShortestPathTests(unittest.TestCase):
    def test_parameter_a(self) -> None:
        self.assertAlmostEqual(A_VALUE, math.sqrt(60) + 10)
        self.assertAlmostEqual(A_VALUE, 17.745966692414832)

    def test_expression_evaluation(self) -> None:
        self.assertAlmostEqual(evaluate_expression("A/2"), A_VALUE / 2)
        self.assertAlmostEqual(evaluate_expression("2A"), 2 * A_VALUE)
        self.assertAlmostEqual(evaluate_expression("A-1"), A_VALUE - 1)
        self.assertEqual(evaluate_expression("9"), 9.0)

    def test_network_size_and_positive_weights(self) -> None:
        edges = build_edges()
        graph = build_graph(edges)
        self.assertEqual(len(edges), 40)
        self.assertEqual(len(graph), 25)
        self.assertTrue(all(edge.weight > 0 for edge in edges))
        self.assertEqual(sum(len(neighbours) for neighbours in graph.values()), 80)

    def test_optimal_path(self) -> None:
        solution = solve()
        self.assertEqual(solution.path, EXPECTED_PATH)
        self.assertEqual(solution.path[0], START)
        self.assertEqual(solution.path[-1], TARGET)

    def test_optimal_cost(self) -> None:
        solution = solve()
        expected = 40 + A_VALUE / 2
        self.assertAlmostEqual(solution.cost, expected)
        self.assertAlmostEqual(solution.cost, 48.87298334620742)

    def test_path_weights(self) -> None:
        solution = solve()
        expected = (5.0, 6.0, 9.0, 2.0, 5.0, 4.0, 9.0, A_VALUE / 2)
        self.assertEqual(len(solution.path_weights), 8)
        for actual, wanted in zip(solution.path_weights, expected):
            self.assertAlmostEqual(actual, wanted)
        self.assertAlmostEqual(sum(solution.path_weights), solution.cost)

    def test_independent_verification(self) -> None:
        edges = build_edges()
        graph = build_graph(edges)
        solution = solve()
        self.assertAlmostEqual(bellman_ford_cost(edges), solution.cost)
        monotone = enumerate_monotone_paths(graph)
        self.assertEqual(len(monotone), 70)
        self.assertAlmostEqual(monotone[0][0], solution.cost)
        self.assertGreater(monotone[1][0], solution.cost)

    def test_every_path_pair_is_an_edge(self) -> None:
        solution = solve()
        graph = build_graph(solution.edges)
        for first, second in zip(solution.path, solution.path[1:]):
            self.assertGreater(edge_weight(graph, first, second), 0)


if __name__ == "__main__":
    unittest.main(verbosity=2)
