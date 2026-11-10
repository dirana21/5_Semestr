"""Автоматичні перевірки розв'язку лабораторної роботи № 4."""

from pathlib import Path
import sys
import unittest

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from solve_lab4 import (  # noqa: E402
    DEMAND,
    SEED,
    SUPPLY,
    generate_costs,
    optimize,
    plan_cost,
    solve_all,
    validate_plan,
)


class TransportationSolutionTests(unittest.TestCase):
    def test_problem_is_balanced(self) -> None:
        self.assertEqual(SUPPLY.sum(), DEMAND.sum())
        self.assertEqual(SUPPLY.sum(), 1700)

    def test_cost_generation_is_reproducible(self) -> None:
        first = generate_costs(SEED)
        second = generate_costs(SEED)
        self.assertTrue(np.array_equal(first, second))
        self.assertEqual(first.shape, (8, 10))
        self.assertTrue(np.all((0 <= first) & (first <= 100)))

    def test_all_initial_plans_are_feasible(self) -> None:
        costs = generate_costs()
        solutions = solve_all(costs)
        self.assertEqual(len(solutions), 9)
        for solution in solutions:
            validate_plan(solution.plan)
            self.assertEqual(solution.cost, plan_cost(solution.plan, costs))

    def test_optimal_plan_is_feasible_and_not_worse(self) -> None:
        costs = generate_costs()
        initial = solve_all(costs)
        optimal = optimize(costs)
        validate_plan(optimal)
        self.assertLessEqual(plan_cost(optimal, costs), min(solution.cost for solution in initial))

    def test_optimal_cost_regression(self) -> None:
        costs = generate_costs()
        self.assertEqual(plan_cost(optimize(costs), costs), 30710)


if __name__ == "__main__":
    unittest.main(verbosity=2)
