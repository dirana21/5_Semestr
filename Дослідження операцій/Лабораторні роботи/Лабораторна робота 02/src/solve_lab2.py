"""Лабораторна робота №2: планування оптимального виробництва.

Варіант N=12, коефіцієнт k=2. Коефіцієнти генеруються за формулами
методичних вказівок із фіксованим seed=1202, щоб результат можна було
відтворити. Задача розв'язується методом dual simplex (HiGHS-DS).
"""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
import math
import random

import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch
import numpy as np
from scipy.optimize import linprog


BASE_DIR = Path(__file__).resolve().parents[1]
OUTPUT_DIR = BASE_DIR / "assets" / "screenshots"


@dataclass(frozen=True)
class Problem:
    n: int
    k: int
    seed: int
    coefficients: np.ndarray
    profit: np.ndarray
    limits: np.ndarray


@dataclass(frozen=True)
class Solution:
    quantities: np.ndarray
    objective: float
    used: np.ndarray
    slack: np.ndarray
    iterations: int
    message: str


def excel_round(value: float) -> int:
    """ROUND для невід'ємних значень, сумісний із формулою Excel."""
    return math.floor(value + 0.5)


def generate_problem(n: int = 12, k: int = 2, seed: int = 1202) -> Problem:
    rng = random.Random(seed)
    scale = n * k
    coefficients = np.array(
        [
            [excel_round(rng.random() * scale) for _ in range(5)]
            for _ in range(5)
        ],
        dtype=float,
    )
    profit = np.array(
        [excel_round(rng.random() * scale * 10) for _ in range(5)],
        dtype=float,
    )
    limits = np.array(
        [n * k * factor for factor in (100, 150, 120, 200, 80)],
        dtype=float,
    )
    return Problem(n, k, seed, coefficients, profit, limits)


def solve_problem(problem: Problem) -> Solution:
    result = linprog(
        c=-problem.profit,
        A_ub=problem.coefficients,
        b_ub=problem.limits,
        bounds=[(0, None)] * 5,
        method="highs-ds",
    )
    if not result.success:
        raise RuntimeError(f"Не вдалося знайти оптимум: {result.message}")

    quantities = np.where(np.abs(result.x) < 1e-9, 0.0, result.x)
    used = problem.coefficients @ quantities
    slack = np.where(np.abs(problem.limits - used) < 1e-8, 0.0, problem.limits - used)
    return Solution(
        quantities=quantities,
        objective=float(problem.profit @ quantities),
        used=used,
        slack=slack,
        iterations=int(result.nit),
        message=str(result.message),
    )


def fmt(value: float, digits: int = 3) -> str:
    if abs(value - round(value)) < 1e-9:
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
    table.set_fontsize(10.5)
    table.scale(1, 1.55)
    for (row, _), cell in table.get_celld().items():
        cell.set_edgecolor("#cbd5e1")
        if row == 0:
            cell.set_facecolor(header_color)
            cell.set_text_props(color="white", weight="bold")
        elif row % 2 == 0:
            cell.set_facecolor("#eff6ff")


def save_input_table(problem: Problem) -> None:
    fig, ax = plt.subplots(figsize=(11.8, 4.5))
    ax.axis("off")
    columns = ["Показник", "x₁", "x₂", "x₃", "x₄", "x₅", "Запас"]
    rows = [
        [f"Ресурс {i + 1}"]
        + [fmt(value) for value in problem.coefficients[i]]
        + [fmt(problem.limits[i])]
        for i in range(5)
    ]
    rows.append(["Прибуток"] + [fmt(value) for value in problem.profit] + ["max"])
    table = ax.table(
        cellText=rows,
        colLabels=columns,
        cellLoc="center",
        colLoc="center",
        loc="center",
        colWidths=[0.20, 0.105, 0.105, 0.105, 0.105, 0.105, 0.16],
    )
    style_table(table, "#0f766e")
    for column in range(len(columns)):
        table[(6, column)].set_facecolor("#ccfbf1")
        table[(6, column)].set_text_props(weight="bold")
    ax.set_title(
        "Згенеровані коефіцієнти задачі (N = 12, k = 2, seed = 1202)",
        weight="bold",
        pad=18,
    )
    fig.savefig(OUTPUT_DIR / "01-вихідні-дані.png")
    plt.close(fig)


def save_support_plan(problem: Problem, solution: Solution) -> None:
    fig, axes = plt.subplots(2, 1, figsize=(11.8, 6.8), gridspec_kw={"height_ratios": [1, 1.65]})
    for ax in axes:
        ax.axis("off")

    variable_rows = [
        ["Початковий план", "0", "0", "0", "0", "0", "0"],
        ["Оптимальний план"]
        + [fmt(value) for value in solution.quantities]
        + [fmt(solution.objective)],
    ]
    variable_table = axes[0].table(
        cellText=variable_rows,
        colLabels=["План", "x₁", "x₂", "x₃", "x₄", "x₅", "F"],
        cellLoc="center",
        colLoc="center",
        loc="center",
        colWidths=[0.23, 0.1, 0.1, 0.1, 0.1, 0.1, 0.18],
    )
    style_table(variable_table, "#1d4ed8")
    for column in range(7):
        variable_table[(2, column)].set_facecolor("#fef3c7")
        variable_table[(2, column)].set_text_props(weight="bold")

    resource_rows = []
    for index in range(5):
        resource_rows.append(
            [
                f"Ресурс {index + 1}",
                fmt(solution.used[index]),
                "≤",
                fmt(problem.limits[index]),
                fmt(solution.slack[index]),
                "активне" if solution.slack[index] == 0 else "резерв",
            ]
        )
    resource_table = axes[1].table(
        cellText=resource_rows,
        colLabels=["Обмеження", "Використано", "Знак", "Запас", "Залишок", "Стан"],
        cellLoc="center",
        colLoc="center",
        loc="center",
        colWidths=[0.20, 0.18, 0.09, 0.16, 0.17, 0.16],
    )
    style_table(resource_table, "#1d4ed8")
    for row in (1, 5):
        for column in range(6):
            resource_table[(row, column)].set_facecolor("#dcfce7")
            resource_table[(row, column)].set_text_props(weight="bold")

    fig.suptitle("Опорна таблиця та оптимальний план", weight="bold", fontsize=16, y=0.98)
    fig.tight_layout(rect=[0, 0, 1, 0.95])
    fig.savefig(OUTPUT_DIR / "02-опорна-таблиця.png")
    plt.close(fig)


def save_solver_settings(problem: Problem) -> None:
    fig, ax = plt.subplots(figsize=(10.8, 6.2))
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)
    ax.axis("off")
    panel = FancyBboxPatch(
        (0.08, 0.08),
        0.84,
        0.82,
        boxstyle="round,pad=0.018,rounding_size=0.02",
        facecolor="#f8fafc",
        edgecolor="#94a3b8",
        linewidth=1.6,
    )
    ax.add_patch(panel)
    ax.text(0.12, 0.84, "Параметри розв'язувача", fontsize=17, weight="bold", color="#0f172a")
    fields = [
        ("Цільова функція", "F = 209x₁ + 198x₂ + 95x₃ + 33x₄ + 80x₅"),
        ("Оптимізація", "Максимум"),
        ("Змінні", "x₁, x₂, x₃, x₄, x₅"),
        ("Обмеження", "A·x ≤ b;  x ≥ 0"),
        ("Метод", "HiGHS Dual Simplex (highs-ds)"),
        ("Тип змінних", "Неперервні"),
    ]
    y = 0.73
    for label, value in fields:
        ax.text(0.13, y, label, fontsize=11, color="#475569", weight="bold")
        box = FancyBboxPatch(
            (0.34, y - 0.026),
            0.50,
            0.055,
            boxstyle="round,pad=0.008,rounding_size=0.008",
            facecolor="white",
            edgecolor="#cbd5e1",
        )
        ax.add_patch(box)
        ax.text(0.36, y, value, fontsize=10.8, color="#0f172a", va="center")
        y -= 0.105
    ax.text(
        0.13,
        0.12,
        "Ліміти ресурсів: " + ", ".join(fmt(value) for value in problem.limits),
        fontsize=10.5,
        color="#334155",
    )
    fig.savefig(OUTPUT_DIR / "03-параметри-розв'язувача.png")
    plt.close(fig)


def save_solution_chart(solution: Solution) -> None:
    labels = ["x₁", "x₂", "x₃", "x₄", "x₅"]
    colors = ["#0f766e" if value > 0 else "#cbd5e1" for value in solution.quantities]
    fig, ax = plt.subplots(figsize=(10.5, 6.1))
    bars = ax.bar(labels, solution.quantities, color=colors, edgecolor="#334155", linewidth=0.8)
    ax.set_title("Оптимальний виробничий план", weight="bold", pad=12)
    ax.set_xlabel("Види продукції")
    ax.set_ylabel("Кількість одиниць")
    ax.spines[["top", "right"]].set_visible(False)
    ax.bar_label(bars, labels=[fmt(value) for value in solution.quantities], padding=5, weight="bold")
    ax.set_ylim(0, max(solution.quantities) * 1.18)
    fig.tight_layout()
    fig.savefig(OUTPUT_DIR / "04-оптимальний-план.png")
    plt.close(fig)


def save_resource_chart(problem: Problem, solution: Solution) -> None:
    labels = [f"Ресурс {index}" for index in range(1, 6)]
    positions = np.arange(5)
    fig, ax = plt.subplots(figsize=(11.0, 6.5))
    used = ax.barh(positions, solution.used, color="#2563eb", label="Використано")
    ax.barh(
        positions,
        solution.slack,
        left=solution.used,
        color="#dbeafe",
        edgecolor="#93c5fd",
        label="Залишок",
    )
    ax.set_yticks(positions, labels)
    ax.invert_yaxis()
    ax.set_xlabel("Одиниці ресурсу")
    ax.set_title("Використання та залишки ресурсів", weight="bold", pad=12)
    ax.legend(loc="lower right")
    ax.spines[["top", "right"]].set_visible(False)
    for index, bar in enumerate(used):
        percentage = solution.used[index] / problem.limits[index] * 100
        ax.text(
            bar.get_width() + problem.limits.max() * 0.012,
            bar.get_y() + bar.get_height() / 2,
            f"{fmt(solution.used[index])} ({percentage:.1f}%)".replace(".", ","),
            va="center",
            fontsize=9.5,
            weight="semibold",
        )
    ax.set_xlim(0, problem.limits.max() * 1.22)
    fig.tight_layout()
    fig.savefig(OUTPUT_DIR / "05-використання-ресурсів.png")
    plt.close(fig)


def result_lines(problem: Problem, solution: Solution) -> list[str]:
    lines = [
        "Лабораторна робота №2 — результат обчислень",
        f"Варіант: N = {problem.n}; k = {problem.k}; seed = {problem.seed}",
        "Метод: HiGHS Dual Simplex",
        "",
        "Оптимальний план:",
    ]
    lines.extend(
        f"  x_{index + 1} = {fmt(value)}" for index, value in enumerate(solution.quantities)
    )
    lines.extend(
        [
            f"  F_max = {fmt(solution.objective)}",
            "",
            "Використання ресурсів:",
        ]
    )
    for index in range(5):
        lines.append(
            f"  Z_{index + 1}: {fmt(solution.used[index])} / "
            f"{fmt(problem.limits[index])}; залишок = {fmt(solution.slack[index])}"
        )
    lines.extend(["", f"Ітерацій: {solution.iterations}", "Статус: оптимальний розв'язок знайдено"])
    return lines


def save_console_output(problem: Problem, solution: Solution) -> None:
    fig, ax = plt.subplots(figsize=(11.5, 7.2))
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
        fontsize=10.9,
        linespacing=1.30,
        transform=ax.transAxes,
    )
    ax.text(0.035, 0.985, "●  ●  ●", va="top", color="#64748b", fontsize=13, transform=ax.transAxes)
    fig.savefig(OUTPUT_DIR / "06-результат-програми.png", facecolor=fig.get_facecolor())
    plt.close(fig)


def main() -> None:
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    setup_style()
    problem = generate_problem()
    solution = solve_problem(problem)
    save_input_table(problem)
    save_support_plan(problem, solution)
    save_solver_settings(problem)
    save_solution_chart(solution)
    save_resource_chart(problem, solution)
    save_console_output(problem, solution)
    print("\n".join(result_lines(problem, solution)))
    print(f"\nІлюстрації збережено у: {OUTPUT_DIR}")


if __name__ == "__main__":
    main()
