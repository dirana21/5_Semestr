"""Лабораторна робота № 4: транспортна задача.

Програма формує відтворювану матрицю тарифів, будує дев'ять
початкових опорних планів, знаходить оптимальний план методом
лінійного програмування та створює ілюстрації для звіту.
"""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Callable

import matplotlib.pyplot as plt
import numpy as np
from scipy.optimize import linprog


SEED = 1204
SUPPLY = np.array([180, 280, 220, 160, 200, 150, 300, 210], dtype=int)
DEMAND = np.array([120, 150, 230, 180, 200, 120, 185, 140, 160, 215], dtype=int)
SUPPLIER_NAMES = [f"A{i}" for i in range(1, 9)]
CONSUMER_NAMES = [f"B{j}" for j in range(1, 11)]


@dataclass(frozen=True)
class Solution:
    name: str
    plan: np.ndarray
    cost: int


def generate_costs(seed: int = SEED) -> np.ndarray:
    """Імітує Excel ROUND(100*RAND();0) з фіксованим seed."""
    rng = np.random.default_rng(seed)
    return np.floor(100 * rng.random((8, 10)) + 0.5).astype(int)


def plan_cost(plan: np.ndarray, costs: np.ndarray) -> int:
    return int(np.sum(plan * costs))


def validate_plan(plan: np.ndarray) -> None:
    if plan.shape != (8, 10):
        raise ValueError("План повинен мати розмір 8×10")
    if np.any(plan < 0):
        raise ValueError("Обсяги перевезень не можуть бути від'ємними")
    if not np.array_equal(plan.sum(axis=1), SUPPLY):
        raise ValueError("План не задовольняє запаси постачальників")
    if not np.array_equal(plan.sum(axis=0), DEMAND):
        raise ValueError("План не задовольняє потреби споживачів")


def corner_plan(row_order: list[int], col_order: list[int]) -> np.ndarray:
    """Універсальний алгоритм кутового методу для заданих напрямків."""
    supply = SUPPLY.copy()
    demand = DEMAND.copy()
    plan = np.zeros((8, 10), dtype=int)
    r = c = 0
    while r < len(row_order) and c < len(col_order):
        i, j = row_order[r], col_order[c]
        amount = min(supply[i], demand[j])
        plan[i, j] += amount
        supply[i] -= amount
        demand[j] -= amount
        if supply[i] == 0:
            r += 1
        if demand[j] == 0:
            c += 1
    validate_plan(plan)
    return plan


def minimum_by_row(costs: np.ndarray) -> np.ndarray:
    supply = SUPPLY.copy()
    demand = DEMAND.copy()
    plan = np.zeros_like(costs)
    for i in range(8):
        while supply[i] > 0:
            active = np.flatnonzero(demand > 0)
            j = min(active, key=lambda col: (costs[i, col], col))
            amount = min(supply[i], demand[j])
            plan[i, j] += amount
            supply[i] -= amount
            demand[j] -= amount
    validate_plan(plan)
    return plan


def minimum_by_column(costs: np.ndarray) -> np.ndarray:
    supply = SUPPLY.copy()
    demand = DEMAND.copy()
    plan = np.zeros_like(costs)
    for j in range(10):
        while demand[j] > 0:
            active = np.flatnonzero(supply > 0)
            i = min(active, key=lambda row: (costs[row, j], row))
            amount = min(supply[i], demand[j])
            plan[i, j] += amount
            supply[i] -= amount
            demand[j] -= amount
    validate_plan(plan)
    return plan


def global_minimum(costs: np.ndarray) -> np.ndarray:
    supply = SUPPLY.copy()
    demand = DEMAND.copy()
    plan = np.zeros_like(costs)
    while supply.sum() > 0:
        active_rows = np.flatnonzero(supply > 0)
        active_cols = np.flatnonzero(demand > 0)
        i, j = min(
            ((i, j) for i in active_rows for j in active_cols),
            key=lambda cell: (costs[cell], cell[0], cell[1]),
        )
        amount = min(supply[i], demand[j])
        plan[i, j] += amount
        supply[i] -= amount
        demand[j] -= amount
    validate_plan(plan)
    return plan


def double_preference(costs: np.ndarray) -> np.ndarray:
    """Динамічний метод подвійної переваги.

    На кожному кроці пріоритет мають тарифи, мінімальні одночасно
    у своїх активних рядку та стовпці, потім одинарні переваги.
    """
    supply = SUPPLY.copy()
    demand = DEMAND.copy()
    plan = np.zeros_like(costs)
    while supply.sum() > 0:
        rows = np.flatnonzero(supply > 0)
        cols = np.flatnonzero(demand > 0)
        row_min = {i: min(costs[i, j] for j in cols) for i in rows}
        col_min = {j: min(costs[i, j] for i in rows) for j in cols}
        candidates = []
        for i in rows:
            for j in cols:
                score = int(costs[i, j] == row_min[i]) + int(costs[i, j] == col_min[j])
                candidates.append((-score, costs[i, j], i, j))
        _, _, i, j = min(candidates)
        amount = min(supply[i], demand[j])
        plan[i, j] += amount
        supply[i] -= amount
        demand[j] -= amount
    validate_plan(plan)
    return plan


def vogel(costs: np.ndarray) -> np.ndarray:
    supply = SUPPLY.copy()
    demand = DEMAND.copy()
    plan = np.zeros_like(costs)
    while supply.sum() > 0:
        rows = np.flatnonzero(supply > 0)
        cols = np.flatnonzero(demand > 0)
        lines: list[tuple[int, int, int, int]] = []
        for i in rows:
            values = sorted((costs[i, j], j) for j in cols)
            penalty = values[1][0] - values[0][0] if len(values) > 1 else values[0][0]
            lines.append((-penalty, values[0][0], 0, i))
        for j in cols:
            values = sorted((costs[i, j], i) for i in rows)
            penalty = values[1][0] - values[0][0] if len(values) > 1 else values[0][0]
            lines.append((-penalty, values[0][0], 1, j))
        _, _, kind, index = min(lines)
        if kind == 0:
            i = index
            j = min(cols, key=lambda col: (costs[i, col], col))
        else:
            j = index
            i = min(rows, key=lambda row: (costs[row, j], row))
        amount = min(supply[i], demand[j])
        plan[i, j] += amount
        supply[i] -= amount
        demand[j] -= amount
    validate_plan(plan)
    return plan


def optimize(costs: np.ndarray) -> np.ndarray:
    variables = costs.size
    a_eq = []
    b_eq = []
    for i in range(8):
        row = np.zeros(variables)
        row[i * 10 : (i + 1) * 10] = 1
        a_eq.append(row)
        b_eq.append(SUPPLY[i])
    for j in range(10):
        col = np.zeros(variables)
        col[j::10] = 1
        a_eq.append(col)
        b_eq.append(DEMAND[j])
    result = linprog(
        costs.ravel(),
        A_eq=np.array(a_eq),
        b_eq=np.array(b_eq),
        bounds=(0, None),
        method="highs",
    )
    if not result.success:
        raise RuntimeError(f"Не вдалося знайти оптимум: {result.message}")
    plan = np.rint(result.x.reshape(costs.shape)).astype(int)
    validate_plan(plan)
    return plan


def solve_all(costs: np.ndarray) -> list[Solution]:
    methods: list[tuple[str, Callable[[np.ndarray], np.ndarray]]] = [
        ("Північно-західний кут", lambda _: corner_plan(list(range(8)), list(range(10)))),
        ("Північно-східний кут", lambda _: corner_plan(list(range(8)), list(range(9, -1, -1)))),
        ("Південно-західний кут", lambda _: corner_plan(list(range(7, -1, -1)), list(range(10)))),
        ("Південно-східний кут", lambda _: corner_plan(list(range(7, -1, -1)), list(range(9, -1, -1)))),
        ("Мінімум за стовпцями", minimum_by_column),
        ("Мінімум за рядками", minimum_by_row),
        ("Мінімум за таблицею", global_minimum),
        ("Подвійна перевага", double_preference),
        ("Метод Фогеля", vogel),
    ]
    return [Solution(name, plan, plan_cost(plan, costs)) for name, fn in methods for plan in [fn(costs)]]


def setup_style() -> None:
    plt.rcParams.update(
        {
            "font.family": "Times New Roman",
            "font.size": 14,
            "axes.titlesize": 16,
            "axes.labelsize": 14,
            "figure.dpi": 150,
        }
    )


def save_figure(fig: plt.Figure, path: Path) -> None:
    fig.savefig(path, dpi=180, bbox_inches="tight", facecolor="white")
    plt.close(fig)


def draw_plan(ax: plt.Axes, plan: np.ndarray, title: str, cost: int) -> None:
    ax.imshow(plan, cmap="Blues", aspect="auto", vmin=0, vmax=max(1, int(plan.max())))
    ax.set_xticks(range(10), CONSUMER_NAMES, fontsize=10)
    ax.set_yticks(range(8), SUPPLIER_NAMES, fontsize=10)
    ax.set_title(f"{title}\nВартість: {cost:,}".replace(",", " "), fontsize=13)
    for i in range(8):
        for j in range(10):
            if plan[i, j] > 0:
                ax.text(j, i, str(plan[i, j]), ha="center", va="center", fontsize=9,
                        color="white" if plan[i, j] > plan.max() * 0.48 else "black")
    ax.set_xlabel("Споживачі")
    ax.set_ylabel("Постачальники")


def create_figures(costs: np.ndarray, solutions: list[Solution], optimal: Solution, output: Path) -> None:
    output.mkdir(parents=True, exist_ok=True)
    by_name = {s.name: s for s in solutions}

    fig, ax = plt.subplots(figsize=(15, 7.5))
    ax.axis("off")
    table_data = np.column_stack([costs, SUPPLY])
    cell_text = [[str(v) for v in row] for row in table_data]
    table = ax.table(
        cellText=cell_text,
        rowLabels=SUPPLIER_NAMES,
        colLabels=CONSUMER_NAMES + ["Запас"],
        cellLoc="center",
        loc="center",
        bbox=[0.02, 0.12, 0.96, 0.76],
    )
    table.auto_set_font_size(False)
    table.set_fontsize(12)
    for (r, c), cell in table.get_celld().items():
        if r == 0 or c == -1:
            cell.set_facecolor("#dbeafe")
        if c == 10:
            cell.set_facecolor("#dcfce7")
    demand_line = "Потреби: " + "   ".join(f"{name} = {value}" for name, value in zip(CONSUMER_NAMES, DEMAND))
    ax.text(0.5, 0.04, demand_line, ha="center", va="center", transform=ax.transAxes, fontsize=12)
    ax.set_title("Матриця вартостей перевезень і балансові дані", pad=18)
    save_figure(fig, output / "01-вихідні-дані.png")

    corner_names = [
        "Північно-західний кут", "Північно-східний кут",
        "Південно-західний кут", "Південно-східний кут",
    ]
    fig, axes = plt.subplots(2, 2, figsize=(17, 12), constrained_layout=True)
    for ax, name in zip(axes.ravel(), corner_names):
        item = by_name[name]
        draw_plan(ax, item.plan, name, item.cost)
    fig.suptitle("Початкові плани, побудовані кутовими методами", fontsize=19)
    save_figure(fig, output / "02-кутові-методи.png")

    minimum_names = ["Мінімум за стовпцями", "Мінімум за рядками", "Мінімум за таблицею"]
    fig, axes = plt.subplots(1, 3, figsize=(20, 6.5), constrained_layout=True)
    for ax, name in zip(axes, minimum_names):
        item = by_name[name]
        draw_plan(ax, item.plan, name, item.cost)
    fig.suptitle("Початкові плани методами мінімальної вартості", fontsize=19)
    save_figure(fig, output / "03-методи-мінімальної-вартості.png")

    preference_names = ["Подвійна перевага", "Метод Фогеля"]
    fig, axes = plt.subplots(1, 2, figsize=(15, 7), constrained_layout=True)
    for ax, name in zip(axes, preference_names):
        item = by_name[name]
        draw_plan(ax, item.plan, name, item.cost)
    fig.suptitle("Плани методами подвійної переваги та Фогеля", fontsize=19)
    save_figure(fig, output / "04-перевага-та-фогель.png")

    ordered = sorted(solutions, key=lambda s: s.cost)
    names = [s.name for s in ordered] + ["Оптимальний план"]
    values = [s.cost for s in ordered] + [optimal.cost]
    colors = ["#2563eb"] * len(ordered) + ["#16a34a"]
    fig, ax = plt.subplots(figsize=(15, 8))
    bars = ax.barh(names[::-1], values[::-1], color=colors[::-1])
    ax.bar_label(bars, labels=[f"{v:,}".replace(",", " ") for v in values[::-1]], padding=5, fontsize=11)
    ax.set_xlabel("Сумарна вартість перевезень")
    ax.set_title("Порівняння транспортних планів за вартістю")
    ax.grid(axis="x", alpha=0.25)
    ax.set_xlim(0, max(values) * 1.12)
    save_figure(fig, output / "05-порівняння-планів.png")

    fig, ax = plt.subplots(figsize=(13, 7))
    draw_plan(ax, optimal.plan, "Оптимальний транспортний план", optimal.cost)
    fig.tight_layout()
    save_figure(fig, output / "06-оптимальний-план.png")

    routes = []
    for i, j in np.argwhere(optimal.plan > 0):
        amount = int(optimal.plan[i, j])
        tariff = int(costs[i, j])
        routes.append([f"{SUPPLIER_NAMES[i]} → {CONSUMER_NAMES[j]}", amount, tariff, amount * tariff])
    fig, ax = plt.subplots(figsize=(13, 10))
    ax.axis("off")
    table = ax.table(
        cellText=[[route, f"{amount}", f"{tariff}", f"{value:,}".replace(",", " ")] for route, amount, tariff, value in routes],
        colLabels=["Маршрут", "Обсяг", "Тариф", "Вартість"],
        cellLoc="center",
        loc="center",
        bbox=[0.12, 0.05, 0.76, 0.88],
    )
    table.auto_set_font_size(False)
    table.set_fontsize(13)
    for (row, col), cell in table.get_celld().items():
        if row == 0:
            cell.set_facecolor("#2563eb")
            cell.set_text_props(color="white", weight="bold")
        elif row % 2 == 0:
            cell.set_facecolor("#eff6ff")
    ax.text(0.5, 0.015, f"Разом: {optimal.cost:,}".replace(",", " "), ha="center", va="center",
            fontsize=15, weight="bold", transform=ax.transAxes)
    ax.set_title("Маршрутна відомість оптимального транспортного плану", pad=24, fontsize=18)
    save_figure(fig, output / "07-маршрути-оптимального-плану.png")

    lines = [
        "ЛАБОРАТОРНА РОБОТА № 4 — ТРАНСПОРТНА ЗАДАЧА",
        "=" * 66,
        f"Баланс: Σaᵢ = {SUPPLY.sum()}, Σbⱼ = {DEMAND.sum()} — задача закрита",
        f"Seed генератора тарифів: {SEED}",
        "",
        "ПЛАНИ ЗА ЗРОСТАННЯМ ВАРТОСТІ:",
    ]
    lines += [f"{index:>2}. {s.name:<29} {s.cost:>8}" for index, s in enumerate(ordered, 1)]
    lines += ["", f"ОПТИМАЛЬНА ВАРТІСТЬ: {optimal.cost}", f"Кількість завантажених маршрутів: {np.count_nonzero(optimal.plan)}"]
    fig, ax = plt.subplots(figsize=(13, 8))
    ax.axis("off")
    ax.text(0.04, 0.96, "\n".join(lines), family="DejaVu Sans Mono", fontsize=14, va="top", transform=ax.transAxes)
    save_figure(fig, output / "08-результат-програми.png")


def main() -> None:
    setup_style()
    costs = generate_costs()
    solutions = solve_all(costs)
    optimal_plan = optimize(costs)
    optimal = Solution("Оптимальний план", optimal_plan, plan_cost(optimal_plan, costs))
    output = Path(__file__).resolve().parents[1] / "assets" / "screenshots"
    create_figures(costs, solutions, optimal, output)

    print("Баланс задачі:", SUPPLY.sum(), "=", DEMAND.sum())
    print("Матриця тарифів:")
    print(costs)
    print("\nПлани за зростанням вартості:")
    for solution in sorted(solutions, key=lambda item: item.cost):
        print(f"  {solution.name:<29} {solution.cost:>8}")
    print(f"\nОптимальна вартість: {optimal.cost}")
    print("Оптимальний план:")
    print(optimal.plan)


if __name__ == "__main__":
    main()
