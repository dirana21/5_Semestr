"""Автоматичні тести лабораторної роботи №10."""

from __future__ import annotations

import tempfile
import unittest
from pathlib import Path

import numpy as np

from linear_regression_lab import (
    RANDOM_SEED,
    SAMPLE_COUNT,
    VARIANT,
    create_plot,
    generate_data,
    run_experiment,
    train_model,
    validate_parameters,
)


class LinearRegressionLabTests(unittest.TestCase):
    def test_constants_match_variant(self) -> None:
        self.assertEqual((VARIANT, SAMPLE_COUNT, RANDOM_SEED), (8, 100, 42))

    def test_generate_data_shapes(self) -> None:
        x, y = generate_data()
        self.assertEqual((x.shape, y.shape), ((100,), (100,)))

    def test_x_values_are_in_required_range(self) -> None:
        x, _ = generate_data()
        self.assertTrue(np.all((x >= 0) & (x <= 20)))

    def test_generation_is_reproducible(self) -> None:
        first = generate_data(seed=10)
        second = generate_data(seed=10)
        self.assertTrue(np.array_equal(first[0], second[0]) and np.array_equal(first[1], second[1]))

    def test_different_seeds_change_data(self) -> None:
        first, _ = generate_data(seed=1)
        second, _ = generate_data(seed=2)
        self.assertFalse(np.array_equal(first, second))

    def test_invalid_variant_is_rejected(self) -> None:
        with self.assertRaises(ValueError):
            validate_parameters(0, 100)

    def test_boolean_variant_is_rejected(self) -> None:
        with self.assertRaises(ValueError):
            validate_parameters(True, 100)

    def test_too_few_samples_are_rejected(self) -> None:
        with self.assertRaises(ValueError):
            validate_parameters(8, 1)

    def test_model_slope_is_close_to_eight(self) -> None:
        x, y = generate_data()
        model = train_model(x, y)
        self.assertAlmostEqual(float(model.coef_[0]), 8.0, delta=0.15)

    def test_model_intercept_is_close_to_two(self) -> None:
        x, y = generate_data()
        model = train_model(x, y)
        self.assertAlmostEqual(float(model.intercept_), 2.0, delta=0.6)

    def test_predictions_have_expected_shape(self) -> None:
        x, y = generate_data()
        predictions = train_model(x, y).predict(x.reshape(-1, 1))
        self.assertEqual(predictions.shape, (100,))

    def test_predictions_increase_with_x(self) -> None:
        x, y = generate_data()
        model = train_model(x, y)
        prediction = model.predict(np.array([[1.0], [2.0]]))
        self.assertLess(prediction[0], prediction[1])

    def test_train_model_rejects_different_lengths(self) -> None:
        with self.assertRaises(ValueError):
            train_model(np.array([1.0, 2.0]), np.array([1.0]))

    def test_create_plot_writes_png(self) -> None:
        x, y = generate_data(sample_count=10)
        model = train_model(x, y)
        with tempfile.TemporaryDirectory(ignore_cleanup_errors=True) as directory:
            path = create_plot(x, y, model, Path(directory) / "plot.png")
            self.assertEqual(path.read_bytes()[:8], b"\x89PNG\r\n\x1a\n")

    def test_run_experiment_returns_high_quality_model(self) -> None:
        with tempfile.TemporaryDirectory(ignore_cleanup_errors=True) as directory:
            result = run_experiment(Path(directory) / "result.png")
            self.assertGreater(result.r2, 0.99)
            self.assertTrue(result.plot_path.exists())


if __name__ == "__main__":
    unittest.main(verbosity=2)
