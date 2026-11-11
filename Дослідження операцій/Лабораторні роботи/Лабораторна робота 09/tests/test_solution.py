"""Автоматичні тести для лабораторної роботи № 9."""

import importlib.util
import sys
import unittest
from pathlib import Path


MODULE_PATH = Path(__file__).resolve().parents[1] / "src" / "solve_lab9.py"
SPEC = importlib.util.spec_from_file_location("solve_lab9", MODULE_PATH)
MODULE = importlib.util.module_from_spec(SPEC)
sys.modules[SPEC.name] = MODULE
SPEC.loader.exec_module(MODULE)


class Lab9SolutionTests(unittest.TestCase):
    def test_variant_is_derived_from_student_number(self):
        self.assertEqual(MODULE.STUDENT_NUMBER, 12)
        self.assertEqual(MODULE.VARIANT, 2)

    def test_response_table(self):
        MODULE.validate_data()
        self.assertEqual(MODULE.RESPONSES[2][2], 34)
        self.assertEqual(MODULE.RESPONSES[4][2], 35)

    def test_resource_levels(self):
        self.assertEqual(MODULE.RESOURCE_LEVELS, (0, 20, 40, 60, 80, 100))

    def test_sequential_method(self):
        solution, dp, choice = MODULE.sequential_dynamic_programming()
        self.assertEqual(solution.allocation, (0, 40, 20, 40))
        self.assertEqual(solution.value, 82)
        self.assertEqual(dp[4][5], 82)
        self.assertEqual(len(choice), 5)

    def test_transition_cost_method(self):
        solution, best, predecessor = MODULE.transition_cost_method()
        self.assertEqual(solution.allocation, (0, 40, 20, 40))
        self.assertEqual(solution.value, 82)
        self.assertEqual(best[(4, 5)], 82)
        self.assertIn((4, 5), predecessor)

    def test_exhaustive_search(self):
        ranked = MODULE.exhaustive_search()
        self.assertEqual(len(ranked), 56)
        self.assertEqual(ranked[0].allocation, (0, 40, 20, 40))
        self.assertEqual(ranked[0].value, 82)
        self.assertEqual(ranked[1].value, 81)

    def test_solution_uses_all_resources(self):
        solution, _dp, _choice = MODULE.sequential_dynamic_programming()
        self.assertEqual(sum(solution.allocation), MODULE.TOTAL_RESOURCE)

    def test_profit_decomposition(self):
        solution, _dp, _choice = MODULE.sequential_dynamic_programming()
        self.assertEqual(solution.profits, (0, 34, 13, 35))
        self.assertEqual(sum(solution.profits), solution.value)

    def test_all_methods_agree(self):
        sequential, _dp, _choice = MODULE.sequential_dynamic_programming()
        transitions, _best, _predecessor = MODULE.transition_cost_method()
        exhaustive = MODULE.exhaustive_search()[0]
        self.assertEqual(sequential, transitions)
        self.assertEqual(sequential, exhaustive)


if __name__ == "__main__":
    unittest.main()
