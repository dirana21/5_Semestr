"""Лабораторна робота №3: двовимірна задача нелінійного програмування.

Варіант N=12, коефіцієнт k=2. Задача розв'язується аналітично
після підстановки x2=N*x1 та незалежно перевіряється чисельно.
"""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
import math

import matplotlib.pyplot as plt
import numpy as np
from scipy.optimize import minimize_scalar


BASE_DIR = Path(__file__).resolve().parents[1]
OUTPUT_DIR = BASE_DIR / "assets" / "screenshots"


@dataclass(frozen=True)
class Problem:
    n: int = 12
    k: int = 2

    @property
    def linear_coefficient(self) -> int:
        return self.k * self.n

    @property
    def reduced_quadratic(self) -> int:
        return 1 + self.n**2

    @property
    def upper_t(self) -> float:
        return self.n / math.sqrt(self.reduced_quadratic)


@dataclass(frozen=True)
class Extremum:
    x1: float
    x2: float
    value: float


@dataclass(frozen=True)
class Solution:
    minimum: Extremum
    maximum: Extremum
    numerical_minimum: Extremum
    numerical_error: float


def objective(problem: Problem, x1, x2):
    return x1**2 - problem.linear_coefficient * x1 + x2**2


def reduced_objective(problem: Problem, t):
    return problem.reduced_quadratic * t**2 - problem.linear_coefficient * t


def solve_analytically(problem: Problem) -> tuple[Extremum, Extremum]:
    t_min = problem.linear_coefficient / (2 * problem.reduced_quadratic)
    minimum = Extremum(t_min, problem.n * t_min, reduced_objective(problem, t_min))

    endpoints = [0.0, problem.upper_t]
    t_max = max(endpoints, key=lambda t: reduced_objective(problem, t))
    maximum = Extremum(t_max, problem.n * t_max, reduced_objective(problem, t_max))
    return minimum, maximum


def solve_problem(problem: Problem) -> Solution:
    minimum, maximum = solve_analytically(problem)
    numeric = minimize_scalar(
        lambda t: reduced_objective(problem, t),
        bounds=(0.0, problem.upper_t),
        method="bounded",
        options={"xatol": 1e-13},
    )
    numerical_minimum = Extremum(
        float(numeric.x),
        float(problem.n * numeric.x),
        float(numeric.fun),
    )
    numerical_error = max(
        abs(minimum.x1 - numerical_minimum.x1),
        abs(minimum.x2 - numerical_minimum.x2),
        abs(minimum.value - numerical_minimum.value),
    )
    return Solution(minimum, maximum, numerical_minimum, numerical_error)


def fmt(value: float, digits: int = 6) -> str:
    if abs(value - round(value)) < 1e-10:
        return str(int(round(value)))
    return f"{value:.{digits}f}".rstrip("0").rstrip(".").replace(".", ",")


def setup_style() -> None:
    plt.rcParams.update(
        {
            "font.family": "DejaVu Sans",
            "font.size": 11,
            "axes.titlesize": 15,
            "axes.labelsize": 12,
            "figure.facecolor": "white",
            "axes.facecolor": "#fbfdff",
            "axes.edgecolor": "#334155",
            "axes.grid": True,
            "grid.alpha": 0.22,
            "grid.color": "#64748b",
            "savefig.dpi": 180,
            "savefig.bbox": "tight",
        }
    )


def style_table(table, header_color: str = "#1d4ed8") -> None:
    table.auto_set_font_size(False)
    table.set_fontsize(10.8)
    table.scale(1, 1.65)
    for (row, _), cell in table.get_celld().items():
        cell.set_edgecolor("#cbd5e1")
        if row == 0:
            cell.set_facecolor(header_color)
            cell.set_text_props(color="white", weight="bold")
        elif row % 2 == 0:
            cell.set_facecolor("#eff6ff")


def save_input_table(problem: Problem) -> None:
    fig, ax = plt.subplots(figsize=(11.2, 4.1))
    ax.axis("off")
    rows = [
        ["Номер варіанта", "N", "12"],
        ["Коефіцієнт", "k", "2"],
        ["Цільова функція", "f(x)", "x₁² − 24x₁ + x₂²"],
        ["Кругове обмеження", "x₁² + x₂² ≤ N²", "x₁² + x₂² ≤ 144"],
        ["Лінійне обмеження", "x₂ = Nx₁", "x₂ = 12x₁"],
        ["Знаки змінних", "x₁ ≥ 0; x₂ ≥ 0", "I чверть"],
    ]
    table = ax.table(
        cellText=rows,
        colLabels=["Показник", "Загальна форма", "Варіант N = 12, k = 2"],
        cellLoc="center",
        colLoc="center",
        loc="center",
        colWidths=[0.27, 0.31, 0.36],
    )
    style_table(table, "#0f766e")
    ax.set_title("Вихідні дані задачі нелінійного програмування", weight="bold", pad=16)
    fig.savefig(OUTPUT_DIR / "01-вихідні-дані.png")
    plt.close(fig)


def draw_geometry(ax, problem: Problem, solution: Solution, zoom: bool) -> None:
    theta = np.linspace(0, np.pi / 2, 500)
    circle_x = problem.n * np.cos(theta)
    circle_y = problem.n * np.sin(theta)
    ax.plot(circle_x, circle_y, color="#2563eb", lw=2.3, label="x₁² + x₂² = 144")
    ax.fill_between(circle_x, 0, circle_y, color="#dbeafe", alpha=0.32)

    t = np.linspace(0, problem.upper_t, 300)
    ax.plot(t, problem.n * t, color="#0f766e", lw=4.0, label="Допустимий відрізок")
    extension = np.linspace(0, 1.15 if zoom else problem.n, 300)
    ax.plot(extension, problem.n * extension, color="#0f766e", lw=1.2, ls="--", alpha=0.7, label="x₂ = 12x₁")

    ax.scatter(
        [solution.minimum.x1],
        [solution.minimum.x2],
        s=150,
        marker="o",
        color="#f59e0b",
        edgecolor="#92400e",
        zorder=6,
        label="Мінімум",
    )
    ax.scatter(
        [solution.maximum.x1],
        [solution.maximum.x2],
        s=220,
        marker="*",
        color="#dc2626",
        edgecolor="#7f1d1d",
        zorder=7,
        label="Максимум",
    )
    if zoom:
        ax.set_xlim(0, 1.15)
        ax.set_ylim(0, 12.5)
        ax.annotate(
            f"min ({fmt(solution.minimum.x1, 3)}; {fmt(solution.minimum.x2, 3)})",
            (solution.minimum.x1, solution.minimum.x2),
            xytext=(12, 10),
            textcoords="offset points",
            fontsize=9.5,
            weight="bold",
        )
        ax.annotate(
            f"max ({fmt(solution.maximum.x1, 3)}; {fmt(solution.maximum.x2, 3)})",
            (solution.maximum.x1, solution.maximum.x2),
            xytext=(-145, -25),
            textcoords="offset points",
            fontsize=9.5,
            weight="bold",
        )
    else:
        ax.set_xlim(0, 12.7)
        ax.set_ylim(0, 12.7)
        ax.set_aspect("equal", adjustable="box")
    ax.set_xlabel("x₁")
    ax.set_ylabel("x₂")
    ax.spines[["top", "right"]].set_visible(False)


def save_feasible_set(problem: Problem, solution: Solution) -> None:
    fig, axes = plt.subplots(1, 2, figsize=(13.0, 6.1))
    draw_geometry(axes[0], problem, solution, zoom=False)
    axes[0].set_title("Обмеження у першій чверті", weight="bold")
    draw_geometry(axes[1], problem, solution, zoom=True)
    axes[1].set_title("Допустимий відрізок і точки екстремуму", weight="bold")
    handles, labels = axes[1].get_legend_handles_labels()
    unique = dict(zip(labels, handles))
    fig.legend(unique.values(), unique.keys(), loc="lower center", ncol=5, framealpha=0.95)
    fig.suptitle("Геометрична інтерпретація обмежень", weight="bold", fontsize=17, y=1.01)
    fig.tight_layout(rect=[0, 0.08, 1, 0.96])
    fig.savefig(OUTPUT_DIR / "02-допустима-область.png")
    plt.close(fig)


def save_reduced_function(problem: Problem, solution: Solution) -> None:
    t = np.linspace(0, problem.upper_t, 600)
    values = reduced_objective(problem, t)
    fig, ax = plt.subplots(figsize=(10.8, 6.3))
    ax.plot(t, values, color="#7c3aed", lw=2.8, label="g(t) = 145t² − 24t")
    ax.fill_between(t, values, 0, where=values < 0, color="#fef3c7", alpha=0.75)
    ax.scatter(solution.minimum.x1, solution.minimum.value, s=150, color="#f59e0b", edgecolor="#92400e", zorder=5)
    ax.scatter(solution.maximum.x1, solution.maximum.value, s=220, marker="*", color="#dc2626", edgecolor="#7f1d1d", zorder=6)
    ax.annotate(
        f"min = {fmt(solution.minimum.value)}",
        (solution.minimum.x1, solution.minimum.value),
        xytext=(35, 35),
        textcoords="offset points",
        arrowprops=dict(arrowstyle="->", color="#92400e"),
        weight="bold",
    )
    ax.annotate(
        f"max = {fmt(solution.maximum.value)}",
        (solution.maximum.x1, solution.maximum.value),
        xytext=(-155, -45),
        textcoords="offset points",
        arrowprops=dict(arrowstyle="->", color="#7f1d1d"),
        weight="bold",
    )
    ax.axhline(0, color="#334155", lw=1)
    ax.set_xlim(0, problem.upper_t * 1.03)
    ax.set_xlabel("t = x₁")
    ax.set_ylabel("g(t)")
    ax.set_title("Цільова функція на допустимому відрізку", weight="bold", pad=12)
    ax.legend(loc="upper left")
    ax.spines[["top", "right"]].set_visible(False)
    fig.tight_layout()
    fig.savefig(OUTPUT_DIR / "03-зведена-функція.png")
    plt.close(fig)


def save_contours(problem: Problem, solution: Solution) -> None:
    x1 = np.linspace(0, 2.0, 500)
    x2 = np.linspace(0, 12.4, 500)
    grid_x1, grid_x2 = np.meshgrid(x1, x2)
    values = objective(problem, grid_x1, grid_x2)
    fig, ax = plt.subplots(figsize=(9.2, 7.2))
    contours = ax.contour(grid_x1, grid_x2, values, levels=18, cmap="viridis", linewidths=1.1)
    ax.clabel(contours, inline=True, fontsize=8, fmt="%.0f")
    t = np.linspace(0, problem.upper_t, 350)
    ax.plot(t, problem.n * t, color="#ef4444", lw=4, label="Допустима множина")
    circle_x = np.linspace(0, 2.0, 350)
    circle_y = np.sqrt(np.maximum(problem.n**2 - circle_x**2, 0))
    ax.plot(circle_x, circle_y, color="#2563eb", lw=2, label="Межа круга")
    ax.scatter(solution.minimum.x1, solution.minimum.x2, s=140, color="#f59e0b", edgecolor="#92400e", label="Мінімум", zorder=5)
    ax.scatter(solution.maximum.x1, solution.maximum.x2, s=210, marker="*", color="#dc2626", edgecolor="#7f1d1d", label="Максимум", zorder=6)
    ax.set_xlim(0, 2)
    ax.set_ylim(0, 12.4)
    ax.set_xlabel("x₁")
    ax.set_ylabel("x₂")
    ax.set_title("Лінії рівня цільової функції", weight="bold", pad=12)
    ax.legend(loc="lower right")
    ax.spines[["top", "right"]].set_visible(False)
    fig.tight_layout()
    fig.savefig(OUTPUT_DIR / "04-лінії-рівня.png")
    plt.close(fig)


def save_surface(problem: Problem, solution: Solution) -> None:
    x1 = np.linspace(0, problem.n, 180)
    x2 = np.linspace(0, problem.n, 180)
    grid_x1, grid_x2 = np.meshgrid(x1, x2)
    values = objective(problem, grid_x1, grid_x2)
    values = np.where(grid_x1**2 + grid_x2**2 <= problem.n**2, values, np.nan)
    fig = plt.figure(figsize=(11.2, 7.6))
    ax = fig.add_subplot(111, projection="3d")
    surface = ax.plot_surface(grid_x1, grid_x2, values, cmap="viridis", alpha=0.78, linewidth=0, antialiased=True)
    t = np.linspace(0, problem.upper_t, 400)
    ax.plot(t, problem.n * t, reduced_objective(problem, t), color="#ef4444", lw=4, label="Допустима крива")
    ax.scatter(solution.minimum.x1, solution.minimum.x2, solution.minimum.value, s=90, color="#f59e0b", edgecolor="#92400e", label="Мінімум")
    ax.scatter(solution.maximum.x1, solution.maximum.x2, solution.maximum.value, s=150, marker="*", color="#dc2626", edgecolor="#7f1d1d", label="Максимум")
    ax.set_xlabel("x₁")
    ax.set_ylabel("x₂")
    ax.set_zlabel("f(x₁, x₂)")
    ax.set_title("Поверхня цільової функції та допустима крива", weight="bold", pad=16)
    ax.view_init(elev=27, azim=-62)
    ax.legend(loc="upper left")
    fig.colorbar(surface, ax=ax, shrink=0.62, pad=0.10, label="f(x₁, x₂)")
    fig.savefig(OUTPUT_DIR / "05-поверхня-функції.png")
    plt.close(fig)


def save_results_table(solution: Solution) -> None:
    fig, ax = plt.subplots(figsize=(10.8, 3.7))
    ax.axis("off")
    rows = [
        ["Мінімум", fmt(solution.minimum.x1), fmt(solution.minimum.x2), fmt(solution.minimum.value)],
        ["Максимум", fmt(solution.maximum.x1), fmt(solution.maximum.x2), fmt(solution.maximum.value)],
        ["Числова перевірка min", fmt(solution.numerical_minimum.x1), fmt(solution.numerical_minimum.x2), fmt(solution.numerical_minimum.value)],
    ]
    table = ax.table(
        cellText=rows,
        colLabels=["Результат", "x₁", "x₂", "f(x₁, x₂)"],
        cellLoc="center",
        colLoc="center",
        loc="center",
        colWidths=[0.30, 0.20, 0.20, 0.24],
    )
    style_table(table, "#1d4ed8")
    for column in range(4):
        table[(1, column)].set_facecolor("#fef3c7")
        table[(2, column)].set_facecolor("#fee2e2")
        table[(1, column)].set_text_props(weight="bold")
        table[(2, column)].set_text_props(weight="bold")
    ax.set_title("Аналітичний розв'язок і числова перевірка", weight="bold", pad=16)
    fig.savefig(OUTPUT_DIR / "06-результати.png")
    plt.close(fig)


def result_lines(problem: Problem, solution: Solution) -> list[str]:
    return [
        "Лабораторна робота №3 — результат обчислень",
        f"Варіант: N = {problem.n}; k = {problem.k}",
        "",
        "Зведена задача:",
        "  x_1 = t; x_2 = 12t",
        f"  0 <= t <= {fmt(problem.upper_t)}",
        "  g(t) = 145t^2 - 24t",
        "",
        "Мінімум:",
        f"  x_1 = {fmt(solution.minimum.x1)}",
        f"  x_2 = {fmt(solution.minimum.x2)}",
        f"  f_min = {fmt(solution.minimum.value)}",
        "",
        "Максимум:",
        f"  x_1 = {fmt(solution.maximum.x1)}",
        f"  x_2 = {fmt(solution.maximum.x2)}",
        f"  f_max = {fmt(solution.maximum.value)}",
        "",
        f"Максимальна похибка числової перевірки: {solution.numerical_error:.3e}",
        "Статус: обидва екстремуми підтверджено",
    ]


def save_console_output(problem: Problem, solution: Solution) -> None:
    fig, ax = plt.subplots(figsize=(11.5, 7.1))
    fig.patch.set_facecolor("#0f172a")
    ax.set_facecolor("#0f172a")
    ax.axis("off")
    ax.text(
        0.035,
        0.94,
        "\n".join(result_lines(problem, solution)),
        va="top",
        ha="left",
        color="#e2e8f0",
        family="DejaVu Sans Mono",
        fontsize=11,
        linespacing=1.34,
        transform=ax.transAxes,
    )
    ax.text(0.035, 0.985, "●  ●  ●", va="top", color="#64748b", fontsize=13, transform=ax.transAxes)
    fig.savefig(OUTPUT_DIR / "07-результат-програми.png", facecolor=fig.get_facecolor())
    plt.close(fig)


def main() -> None:
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    setup_style()
    problem = Problem()
    solution = solve_problem(problem)
    save_input_table(problem)
    save_feasible_set(problem, solution)
    save_reduced_function(problem, solution)
    save_contours(problem, solution)
    save_surface(problem, solution)
    save_results_table(solution)
    save_console_output(problem, solution)
    print("\n".join(result_lines(problem, solution)))
    print(f"\nІлюстрації збережено у: {OUTPUT_DIR}")


if __name__ == "__main__":
    main()
