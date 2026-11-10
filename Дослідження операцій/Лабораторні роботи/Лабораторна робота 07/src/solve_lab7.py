"""Лабораторна робота № 7: цілочисельне програмування методом Гоморі.

Варіант 12. Програма знаходить розв'язок LP-релаксації, формує
відтинання Гоморі, перевіряє всі цілочисельні точки та створює
ілюстрації для звіту.
"""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
from matplotlib.patches import FancyArrowPatch
from scipy.optimize import linprog


VARIANT = 12
OBJECTIVE = np.array([1.0, 1.0])
A = np.array([[8.0, -3.0], [3.0, 2.0]])
B = np.array([24.0, 13.0])
GOMORY_COEFFICIENTS = np.array([1.0, 1.0])
GOMORY_RHS = 6.0


@dataclass(frozen=True)
class Solution:
    lp_point: np.ndarray
    lp_value: float
    integer_points: tuple[tuple[int, int, int], ...]
    optima: tuple[tuple[int, int, int], ...]


def is_feasible(point: np.ndarray, include_cut: bool = False, tolerance: float = 1e-9) -> bool:
    if np.any(point < -tolerance):
        return False
    if np.any(A @ point - B > tolerance):
        return False
    if include_cut and GOMORY_COEFFICIENTS @ point - GOMORY_RHS > tolerance:
        return False
    return True


def solve_lp_relaxation() -> tuple[np.ndarray, float]:
    result = linprog(-OBJECTIVE, A_ub=A, b_ub=B, bounds=(0, None), method="highs")
    if not result.success:
        raise RuntimeError(result.message)
    return result.x, float(-result.fun)


def enumerate_integer_points() -> tuple[tuple[int, int, int], ...]:
    points = []
    for x1 in range(10):
        for x2 in range(10):
            point = np.array([x1, x2], dtype=float)
            if is_feasible(point):
                points.append((x1, x2, x1 + x2))
    return tuple(points)


def solve() -> Solution:
    lp_point, lp_value = solve_lp_relaxation()
    integer_points = enumerate_integer_points()
    best_value = max(point[2] for point in integer_points)
    optima = tuple(point for point in integer_points if point[2] == best_value)
    return Solution(lp_point, lp_value, integer_points, optima)


def final_simplex_tableau() -> np.ndarray:
    """Таблиця у формі x_B + A* x_N = b для базису (x2, s1)."""
    return np.array(
        [
            [6.5, 1.5, 1.0, 0.0, 0.5],
            [43.5, 12.5, 0.0, 1.0, 1.5],
            [6.5, 0.5, 0.0, 0.0, 0.5],
        ]
    )


def fractional_part(value: float) -> float:
    return float(value - np.floor(value))


def gomory_cut_from_tableau() -> tuple[np.ndarray, float]:
    row = final_simplex_tableau()[0]
    coefficients = np.array([fractional_part(row[1]), fractional_part(row[4])])
    rhs = fractional_part(row[0])
    return coefficients, rhs


def setup_style() -> None:
    plt.rcParams.update(
        {
            "font.family": "Times New Roman",
            "font.size": 14,
            "axes.titlesize": 17,
            "axes.labelsize": 14,
            "figure.dpi": 150,
        }
    )


def save_figure(fig: plt.Figure, path: Path) -> None:
    fig.savefig(path, dpi=180, bbox_inches="tight", facecolor="white")
    plt.close(fig)


def region_mask(xx: np.ndarray, yy: np.ndarray, include_cut: bool) -> np.ndarray:
    mask = (8 * xx - 3 * yy <= 24 + 1e-9) & (3 * xx + 2 * yy <= 13 + 1e-9)
    mask &= (xx >= 0) & (yy >= 0)
    if include_cut:
        mask &= xx + yy <= 6 + 1e-9
    return mask


def draw_constraint_lines(ax: plt.Axes, include_cut: bool = False) -> None:
    x = np.linspace(0, 5.1, 500)
    ax.plot(x, (8 * x - 24) / 3, color="#2563eb", linewidth=2.2, label="$8x_1-3x_2=24$")
    ax.plot(x, (13 - 3 * x) / 2, color="#7c3aed", linewidth=2.2, label="$3x_1+2x_2=13$")
    if include_cut:
        ax.plot(x, 6 - x, color="#dc2626", linewidth=3.0, label="Відтинання $x_1+x_2=6$")
    ax.set_xlim(0, 5.0)
    ax.set_ylim(0, 7.2)
    ax.set_xlabel("$x_1$")
    ax.set_ylabel("$x_2$")
    ax.grid(alpha=0.22)


def create_figures(solution: Solution, output: Path) -> None:
    output.mkdir(parents=True, exist_ok=True)

    fig, ax = plt.subplots(figsize=(13, 8))
    ax.axis("off")
    model = [
        ["Варіант", "12"],
        ["Цільова функція", "F = x₁ + x₂ → max"],
        ["Обмеження 1", "8x₁ − 3x₂ ≤ 24"],
        ["Обмеження 2", "3x₁ + 2x₂ ≤ 13"],
        ["Невід'ємність", "x₁ ≥ 0, x₂ ≥ 0"],
        ["Цілочисельність", "x₁, x₂ — цілі"],
    ]
    table = ax.table(cellText=model, colLabels=["Елемент моделі", "Математичний запис"],
                     cellLoc="center", loc="center", bbox=[0.08, 0.14, 0.84, 0.7])
    table.auto_set_font_size(False)
    table.set_fontsize(15)
    for (row, _), cell in table.get_celld().items():
        cell.set_facecolor("#dbeafe" if row == 0 else ("#f8fafc" if row % 2 else "#eff6ff"))
    ax.set_title("Математична модель задачі цілочисельного програмування", pad=20)
    save_figure(fig, output / "01-постановка-задачі.png")

    gx = np.linspace(0, 5, 500)
    gy = np.linspace(0, 7.2, 500)
    xx, yy = np.meshgrid(gx, gy)
    mask = region_mask(xx, yy, False)
    fig, ax = plt.subplots(figsize=(12, 9))
    ax.contourf(xx, yy, mask.astype(float), levels=[0.5, 1.5], colors=["#bfdbfe"], alpha=0.75)
    draw_constraint_lines(ax)
    for value, style in [(4, "--"), (5, "--"), (6, "--"), (6.5, "-")]:
        ax.plot(gx, value - gx, color="#64748b" if value < 6.5 else "#16a34a",
                linestyle=style, linewidth=1.2 if value < 6.5 else 2.6,
                alpha=0.8, label=f"$F={str(value).replace('.', ',')}$" if value == 6.5 else None)
    ax.scatter(*solution.lp_point, s=260, marker="*", color="#16a34a", edgecolor="white", linewidth=1.2, zorder=5,
               label="LP-оптимум $(0;6,5)$")
    ax.annotate("дробове значення $x_2$", xy=solution.lp_point, xytext=(1.0, 6.85),
                arrowprops={"arrowstyle": "->", "color": "#166534"}, color="#166534")
    ax.legend(loc="upper right")
    ax.set_title("Розв'язок LP-релаксації без умови цілочисельності")
    fig.tight_layout()
    save_figure(fig, output / "02-lp-релаксація.png")

    tableau = final_simplex_tableau()
    fig, ax = plt.subplots(figsize=(14, 7))
    ax.axis("off")
    cell_text = [[str(value).replace(".", ",") for value in row] for row in tableau]
    table = ax.table(cellText=cell_text, rowLabels=["x₂", "s₁", "F"],
                     colLabels=["b", "x₁", "x₂", "s₁", "s₂"],
                     cellLoc="center", loc="center", bbox=[0.08, 0.3, 0.84, 0.48])
    table.auto_set_font_size(False)
    table.set_fontsize(16)
    for (row, col), cell in table.get_celld().items():
        if row == 0:
            cell.set_facecolor("#dbeafe")
        elif row == 1:
            cell.set_facecolor("#fef3c7")
        elif col == -1:
            cell.set_facecolor("#e2e8f0")
    ax.text(0.5, 0.2, "Базисний розв'язок: x₁ = 0; x₂ = 6,5; s₁ = 43,5; s₂ = 0; F = 6,5",
            ha="center", transform=ax.transAxes, fontsize=15)
    ax.text(0.5, 0.11, "Дробова базисна змінна x₂ визначає рядок для побудови відтинання.",
            ha="center", transform=ax.transAxes, fontsize=14, color="#92400e")
    ax.set_title("Фінальна симплекс-таблиця LP-релаксації", pad=18)
    save_figure(fig, output / "03-фінальна-симплекс-таблиця.png")

    fig, ax = plt.subplots(figsize=(16, 8))
    ax.set_xlim(0, 16)
    ax.set_ylim(0, 8)
    ax.axis("off")
    boxes = [
        (1.8, 5.4, "Дробовий рядок\nx₂ + 1,5x₁ + 0,5s₂ = 6,5"),
        (5.6, 5.4, "Дробові частини\nf(1,5)=0,5; f(0,5)=0,5\nf(6,5)=0,5"),
        (9.8, 5.4, "Нерівність Гоморі\n0,5x₁ + 0,5s₂ ≥ 0,5"),
        (13.8, 5.4, "Підстановка s₂\nx₁ + x₂ ≤ 6"),
    ]
    for x, y, text_value in boxes:
        ax.text(x, y, text_value, ha="center", va="center", fontsize=14,
                bbox={"boxstyle": "round,pad=0.65", "fc": "#eff6ff", "ec": "#2563eb", "lw": 1.7})
    for first, second in zip(boxes, boxes[1:]):
        arrow = FancyArrowPatch((first[0] + 1.45, first[1]), (second[0] - 1.45, second[1]),
                                arrowstyle="-|>", mutation_scale=18, linewidth=2, color="#475569")
        ax.add_patch(arrow)
    ax.text(8, 2.1, "Відтинання вилучає дробовий LP-оптимум, але не вилучає жодної допустимої цілочисельної точки.",
            ha="center", fontsize=15,
            bbox={"boxstyle": "round,pad=0.45", "fc": "#dcfce7", "ec": "#16a34a"})
    ax.set_title("Формування першого відтинання Гоморі", fontsize=20, pad=20)
    save_figure(fig, output / "04-побудова-відтинання.png")

    cut_mask = region_mask(xx, yy, True)
    fig, ax = plt.subplots(figsize=(12, 9))
    ax.contourf(xx, yy, mask.astype(float), levels=[0.5, 1.5], colors=["#cbd5e1"], alpha=0.45)
    ax.contourf(xx, yy, cut_mask.astype(float), levels=[0.5, 1.5], colors=["#bbf7d0"], alpha=0.9)
    draw_constraint_lines(ax, include_cut=True)
    ax.scatter(*solution.lp_point, s=180, marker="x", color="#dc2626", linewidth=3, zorder=5,
               label="Вилучений LP-оптимум")
    optimal_segment = np.array([[0, 6], [1, 5]])
    ax.plot(optimal_segment[:, 0], optimal_segment[:, 1], color="#f59e0b", linewidth=7, alpha=0.75,
            label="Оптимальне цілочисельне ребро")
    for x1, x2, _ in solution.optima:
        ax.scatter(x1, x2, s=220, color="#f59e0b", edgecolor="white", linewidth=1.5, zorder=6)
        ax.text(x1 + 0.12, x2 + 0.12, f"({x1}; {x2})", color="#92400e", weight="bold")
    ax.legend(loc="upper right")
    ax.set_title("Допустима область після додавання відтинання Гоморі")
    fig.tight_layout()
    save_figure(fig, output / "05-область-після-відтинання.png")

    fig, ax = plt.subplots(figsize=(12, 9))
    draw_constraint_lines(ax)
    values = np.array([point[2] for point in solution.integer_points])
    scatter = ax.scatter([point[0] for point in solution.integer_points], [point[1] for point in solution.integer_points],
                         c=values, cmap="viridis", s=170, edgecolor="white", linewidth=1.0, zorder=4)
    for x1, x2, value in solution.integer_points:
        ax.text(x1, x2, str(value), ha="center", va="center", color="white" if value >= 4 else "black",
                fontsize=10, weight="bold", zorder=5)
    for x1, x2, _ in solution.optima:
        ax.scatter(x1, x2, s=360, facecolors="none", edgecolors="#dc2626", linewidth=3, zorder=6)
    fig.colorbar(scatter, ax=ax, shrink=0.82, label="Значення F = x₁ + x₂")
    ax.set_title("Перевірка всіх допустимих цілочисельних точок")
    fig.tight_layout()
    save_figure(fig, output / "06-цілочисельні-точки.png")

    fig, (ax_bar, ax_table) = plt.subplots(1, 2, figsize=(16, 7), gridspec_kw={"width_ratios": [0.8, 1.2]})
    bars = ax_bar.bar(["LP-релаксація", "Цілочисельна задача"], [solution.lp_value, solution.optima[0][2]],
                      color=["#2563eb", "#16a34a"])
    ax_bar.bar_label(bars, labels=["6,5", "6"], padding=5, fontsize=14)
    ax_bar.set_ylabel("Максимальне значення F")
    ax_bar.set_ylim(0, 7.3)
    ax_bar.set_title("Порівняння оптимумів")
    ax_bar.grid(axis="y", alpha=0.22)
    ax_table.axis("off")
    rows = [["1", "(0; 6)", "6", "виконуються"], ["2", "(1; 5)", "6", "виконуються"]]
    table = ax_table.table(cellText=rows, colLabels=["№", "(x₁; x₂)", "F", "Обмеження"],
                           cellLoc="center", loc="center", bbox=[0.02, 0.25, 0.96, 0.5])
    table.auto_set_font_size(False)
    table.set_fontsize(14)
    for (row, _), cell in table.get_celld().items():
        cell.set_facecolor("#dcfce7" if row > 0 else "#bbf7d0")
    ax_table.set_title("Рівноцінні оптимальні цілочисельні плани", pad=20)
    fig.suptitle("Підсумок розв'язання методом Гоморі", fontsize=20)
    fig.tight_layout()
    save_figure(fig, output / "07-порівняння-розв'язків.png")

    cut_coefficients, cut_rhs = gomory_cut_from_tableau()
    lines = [
        "ЛАБОРАТОРНА РОБОТА № 7 — МЕТОД ГОМОРІ",
        "=" * 62,
        f"Варіант: {VARIANT}",
        "F = x₁ + x₂ → max",
        "8x₁ − 3x₂ ≤ 24; 3x₁ + 2x₂ ≤ 13",
        "",
        f"LP-оптимум: x = ({solution.lp_point[0]:.1f}; {solution.lp_point[1]:.1f}), F = {solution.lp_value:.1f}",
        f"Дробові частини: ({cut_coefficients[0]:.1f}; {cut_coefficients[1]:.1f}) ≥ {cut_rhs:.1f}",
        "Відтинання Гоморі: x₁ + x₂ ≤ 6",
        "",
        "ЦІЛОЧИСЕЛЬНІ ОПТИМУМИ:",
    ]
    lines.extend(f"x = ({x1}; {x2}), F = {value}" for x1, x2, value in solution.optima)
    lines += ["", f"Fmax = {solution.optima[0][2]}", "Кількість відтинань: 1"]
    fig, ax = plt.subplots(figsize=(13, 8))
    ax.axis("off")
    ax.text(0.04, 0.96, "\n".join(lines).replace(".", ","), family="DejaVu Sans Mono",
            fontsize=14, va="top", transform=ax.transAxes)
    save_figure(fig, output / "08-результат-програми.png")


def main() -> None:
    setup_style()
    solution = solve()
    output = Path(__file__).resolve().parents[1] / "assets" / "screenshots"
    create_figures(solution, output)

    print("LP-релаксація:", solution.lp_point, "F =", solution.lp_value)
    print("Відтинання Гоморі: x1 + x2 <= 6")
    print("Допустимі цілочисельні точки:", solution.integer_points)
    print("Оптимальні цілочисельні плани:", solution.optima)


if __name__ == "__main__":
    main()
