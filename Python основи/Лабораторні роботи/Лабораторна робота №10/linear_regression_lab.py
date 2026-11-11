"""Лабораторна робота №10: NumPy, Matplotlib і лінійна регресія."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

import matplotlib

matplotlib.use("Agg")

import matplotlib.pyplot as plt
import numpy as np
from sklearn.linear_model import LinearRegression
from sklearn.metrics import r2_score


VARIANT = 8
SAMPLE_COUNT = 100
RANDOM_SEED = 42


@dataclass(frozen=True)
class RegressionResult:
    """Підсумкові характеристики навченої моделі."""

    variant: int
    sample_count: int
    slope: float
    intercept: float
    r2: float
    plot_path: Path


def validate_parameters(variant: int, sample_count: int) -> None:
    """Перевірити номер варіанта та кількість спостережень."""
    if isinstance(variant, bool) or not isinstance(variant, int) or variant <= 0:
        raise ValueError("Номер варіанта повинен бути додатним цілим числом.")
    if isinstance(sample_count, bool) or not isinstance(sample_count, int) or sample_count < 2:
        raise ValueError("Кількість точок повинна бути цілим числом не меншим за 2.")


def generate_data(
    variant: int = VARIANT,
    sample_count: int = SAMPLE_COUNT,
    seed: int = RANDOM_SEED,
) -> tuple[np.ndarray, np.ndarray]:
    """Згенерувати x у межах [0, 20] і y = variant * x + 2 + шум."""
    validate_parameters(variant, sample_count)
    generator = np.random.default_rng(seed)
    x = generator.uniform(0.0, 20.0, sample_count)
    noise = generator.normal(0.0, 2.0, sample_count)
    y = variant * x + 2.0 + noise
    return x, y


def train_model(x: np.ndarray, y: np.ndarray) -> LinearRegression:
    """Навчити модель лінійної регресії на одновимірних даних."""
    x_array = np.asarray(x, dtype=float)
    y_array = np.asarray(y, dtype=float)
    if x_array.ndim != 1 or y_array.ndim != 1:
        raise ValueError("Масиви x та y повинні бути одновимірними.")
    if x_array.size != y_array.size or x_array.size < 2:
        raise ValueError("Масиви x та y повинні мати однакову довжину не менше 2.")
    model = LinearRegression()
    model.fit(x_array.reshape(-1, 1), y_array)
    return model


def create_plot(
    x: np.ndarray,
    y: np.ndarray,
    model: LinearRegression,
    output_path: Path,
) -> Path:
    """Побудувати діаграму розсіювання та лінію регресії."""
    output_path.parent.mkdir(parents=True, exist_ok=True)
    x_line = np.linspace(0.0, 20.0, 200)
    y_line = model.predict(x_line.reshape(-1, 1))

    figure, axes = plt.subplots(figsize=(9, 6))
    axes.scatter(x, y, alpha=0.72, color="#2563eb", label="Згенеровані дані")
    axes.plot(x_line, y_line, color="#dc2626", linewidth=2.5, label="Лінійна регресія")
    axes.set_title("Лінійна регресія: варіант 8")
    axes.set_xlabel("x")
    axes.set_ylabel("y")
    axes.grid(True, alpha=0.28)
    axes.legend()
    figure.tight_layout()
    figure.savefig(output_path, dpi=160)
    plt.close(figure)
    return output_path


def run_experiment(output_path: Path) -> RegressionResult:
    """Згенерувати дані, навчити модель, оцінити її та зберегти графік."""
    x, y = generate_data()
    model = train_model(x, y)
    predictions = model.predict(x.reshape(-1, 1))
    saved_plot = create_plot(x, y, model, output_path)
    return RegressionResult(
        variant=VARIANT,
        sample_count=SAMPLE_COUNT,
        slope=float(model.coef_[0]),
        intercept=float(model.intercept_),
        r2=float(r2_score(y, predictions)),
        plot_path=saved_plot,
    )


def main() -> None:
    """Виконати завдання варіанта 8 і вивести підсумок."""
    output_path = Path(__file__).with_name("results") / "regression_variant_8.png"
    result = run_experiment(output_path)

    print("Лабораторна робота №10. Варіант 8.")
    print(f"Кількість згенерованих точок: {result.sample_count}")
    print("Формула даних: y = 8 * x + 2 + N(0, 2)")
    print(f"Коефіцієнт моделі: {result.slope:.4f}")
    print(f"Вільний член моделі: {result.intercept:.4f}")
    print(f"Коефіцієнт детермінації R2: {result.r2:.4f}")
    print(f"Графік збережено: {result.plot_path}")


if __name__ == "__main__":
    main()
