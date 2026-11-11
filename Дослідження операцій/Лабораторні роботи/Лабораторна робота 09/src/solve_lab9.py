"""Лабораторна робота № 9: розподіл обмежених ресурсів.

Варіант 2 (остання цифра номера студента N=12). Загальний ресурс —
100 у. о., крок — 20 у. о. Розв'язок будується послідовним методом
динамічного програмування та методом вартості переходів у шаруватому графі.
"""

from __future__ import annotations

from dataclasses import dataclass
from itertools import product
from pathlib import Path
from typing import Dict, Iterable, List, Sequence, Tuple

import matplotlib.pyplot as plt
from matplotlib.patches import FancyArrowPatch


STUDENT_NUMBER = 12
VARIANT = STUDENT_NUMBER % 10
RESOURCE_STEP = 20
TOTAL_RESOURCE = 100
ENTERPRISES = (1, 2, 3, 4)
RESOURCE_LEVELS = tuple(range(0, TOTAL_RESOURCE + RESOURCE_STEP, RESOURCE_STEP))

# Значення функцій відгуку для варіанта 2. Нульовому вкладенню
# відповідає нульовий приріст випуску продукції.
RESPONSES: Dict[int, Tuple[int, ...]] = {
    1: (0, 9, 17, 29, 38, 47),
    2: (0, 11, 34, 46, 53, 75),
    3: (0, 13, 28, 37, 49, 61),
    4: (0, 12, 35, 40, 54, 73),
}


@dataclass(frozen=True)
class Solution:
    """Оптимальний розподіл та значення цільової функції."""

    allocation_units: Tuple[int, ...]
    value: int

    @property
    def allocation(self) -> Tuple[int, ...]:
        return tuple(x * RESOURCE_STEP for x in self.allocation_units)

    @property
    def profits(self) -> Tuple[int, ...]:
        return tuple(RESPONSES[i][self.allocation_units[i - 1]] for i in ENTERPRISES)


def validate_data(responses: Dict[int, Sequence[int]] = RESPONSES) -> None:
    """Перевірити повноту та узгодженість таблиці функцій відгуку."""

    if set(responses) != set(ENTERPRISES):
        raise ValueError("Потрібні функції відгуку для чотирьох підприємств")
    expected_length = len(RESOURCE_LEVELS)
    for enterprise, values in responses.items():
        if len(values) != expected_length:
            raise ValueError(f"Підприємство {enterprise}: некоректна кількість значень")
        if values[0] != 0:
            raise ValueError(f"Підприємство {enterprise}: f(0) має дорівнювати нулю")
        if any(value < 0 for value in values):
            raise ValueError("Функції відгуку не можуть бути від'ємними")


def sequential_dynamic_programming(
    responses: Dict[int, Sequence[int]] = RESPONSES,
) -> Tuple[Solution, List[List[int]], List[List[int]]]:
    """Послідовний метод на основі рекурентного співвідношення Беллмана.

    dp[i][s] — максимальний відгук перших i підприємств, якщо між ними
    розподілено s дискретних одиниць ресурсу. choice[i][s] зберігає
    кількість одиниць, виділених i-му підприємству.
    """

    validate_data(responses)
    unit_count = TOTAL_RESOURCE // RESOURCE_STEP
    stage_count = len(ENTERPRISES)
    dp = [[0] * (unit_count + 1) for _ in range(stage_count + 1)]
    choice = [[0] * (unit_count + 1) for _ in range(stage_count + 1)]

    for stage, enterprise in enumerate(ENTERPRISES, start=1):
        for available in range(unit_count + 1):
            candidates = [
                (dp[stage - 1][available - allocated] + responses[enterprise][allocated], allocated)
                for allocated in range(available + 1)
            ]
            best_value, best_allocated = max(candidates, key=lambda item: (item[0], -item[1]))
            dp[stage][available] = best_value
            choice[stage][available] = best_allocated

    remaining = unit_count
    allocation = [0] * stage_count
    for stage in range(stage_count, 0, -1):
        allocation[stage - 1] = choice[stage][remaining]
        remaining -= allocation[stage - 1]

    return Solution(tuple(allocation), dp[stage_count][unit_count]), dp, choice


def transition_cost_method(
    responses: Dict[int, Sequence[int]] = RESPONSES,
) -> Tuple[Solution, Dict[Tuple[int, int], int], Dict[Tuple[int, int], Tuple[int, int]]]:
    """Знайти найдорожчий шлях у шаруватому ациклічному графі станів.

    Вершина (i, s) означає, що опрацьовано i підприємств і використано
    s одиниць ресурсу. Ребро відповідає виділенню ресурсу наступному
    підприємству, а його вартість дорівнює значенню функції відгуку.
    """

    validate_data(responses)
    unit_count = TOTAL_RESOURCE // RESOURCE_STEP
    best: Dict[Tuple[int, int], int] = {(0, 0): 0}
    predecessor: Dict[Tuple[int, int], Tuple[int, int]] = {}

    for stage, enterprise in enumerate(ENTERPRISES, start=1):
        for used_before in range(unit_count + 1):
            previous = (stage - 1, used_before)
            if previous not in best:
                continue
            for allocated in range(unit_count - used_before + 1):
                used_after = used_before + allocated
                node = (stage, used_after)
                candidate = best[previous] + responses[enterprise][allocated]
                if candidate > best.get(node, -1):
                    best[node] = candidate
                    predecessor[node] = previous

    node = (len(ENTERPRISES), unit_count)
    allocation_reversed: List[int] = []
    while node[0] > 0:
        previous = predecessor[node]
        allocation_reversed.append(node[1] - previous[1])
        node = previous
    allocation = tuple(reversed(allocation_reversed))
    solution = Solution(allocation, best[(len(ENTERPRISES), unit_count)])
    return solution, best, predecessor


def exhaustive_search(
    responses: Dict[int, Sequence[int]] = RESPONSES,
) -> List[Solution]:
    """Перебрати всі цілочислові розподіли п'яти одиниць ресурсу."""

    validate_data(responses)
    unit_count = TOTAL_RESOURCE // RESOURCE_STEP
    variants: List[Solution] = []
    for allocation in product(range(unit_count + 1), repeat=len(ENTERPRISES)):
        if sum(allocation) != unit_count:
            continue
        value = sum(responses[i][allocation[i - 1]] for i in ENTERPRISES)
        variants.append(Solution(tuple(allocation), value))
    return sorted(variants, key=lambda item: (-item.value, item.allocation_units))


def decimal_comma(value: float, digits: int = 0) -> str:
    """Форматувати число з українським десятковим роздільником."""

    return f"{value:.{digits}f}".replace(".", ",")


def configure_style() -> None:
    """Установити єдине оформлення ілюстрацій звіту."""

    plt.rcParams.update(
        {
            "font.family": "Times New Roman",
            "font.size": 14,
            "axes.titlesize": 16,
            "axes.labelsize": 14,
            "xtick.labelsize": 12,
            "ytick.labelsize": 12,
            "figure.dpi": 130,
            "savefig.dpi": 160,
        }
    )


def save_figure(fig: plt.Figure, path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(path, bbox_inches="tight", facecolor=fig.get_facecolor())
    plt.close(fig)


def figure_input_data(output: Path) -> None:
    fig, ax = plt.subplots(figsize=(13.5, 6.3))
    ax.axis("off")
    ax.set_title("Вихідні дані: функції відгуку, варіант 2", fontweight="bold", pad=18)
    columns = ["Підприємство"] + [str(x) for x in RESOURCE_LEVELS]
    rows = [[f"№ {i}"] + list(RESPONSES[i]) for i in ENTERPRISES]
    table = ax.table(cellText=rows, colLabels=columns, cellLoc="center", loc="center")
    table.auto_set_font_size(False)
    table.set_fontsize(14)
    table.scale(1, 2.1)
    for (row, _column), cell in table.get_celld().items():
        cell.set_edgecolor("#334155")
        if row == 0:
            cell.set_facecolor("#1d4ed8")
            cell.get_text().set_color("white")
            cell.get_text().set_fontweight("bold")
        elif row % 2 == 0:
            cell.set_facecolor("#eff6ff")
    ax.text(
        0.5,
        0.08,
        "Загальний ресурс S = 100 у. о.; крок дискретизації — 20 у. о.",
        ha="center",
        transform=ax.transAxes,
        fontweight="bold",
    )
    save_figure(fig, output / "01-вихідні-дані.png")


def figure_response_curves(output: Path) -> None:
    fig, ax = plt.subplots(figsize=(12.5, 7.2))
    colors = ("#2563eb", "#dc2626", "#059669", "#7c3aed")
    for enterprise, color in zip(ENTERPRISES, colors):
        ax.plot(
            RESOURCE_LEVELS,
            RESPONSES[enterprise],
            marker="o",
            linewidth=2.4,
            markersize=7,
            color=color,
            label=f"Підприємство № {enterprise}",
        )
    ax.set_title("Функції відгуку підприємств", fontweight="bold")
    ax.set_xlabel("Виділений ресурс, у. о.")
    ax.set_ylabel("Приріст випуску продукції")
    ax.set_xticks(RESOURCE_LEVELS)
    ax.grid(True, alpha=0.25)
    ax.legend(loc="upper left", frameon=True)
    save_figure(fig, output / "02-функції-відгуку.png")


def figure_dp_table(output: Path, dp: Sequence[Sequence[int]]) -> None:
    fig, ax = plt.subplots(figsize=(13.5, 6.6))
    ax.axis("off")
    ax.set_title("Таблиця послідовного методу Беллмана", fontweight="bold", pad=18)
    columns = ["Етап"] + [str(x) for x in RESOURCE_LEVELS]
    rows = [[f"φ{i}(X)"] + list(dp[i]) for i in range(1, len(ENTERPRISES) + 1)]
    table = ax.table(cellText=rows, colLabels=columns, cellLoc="center", loc="center")
    table.auto_set_font_size(False)
    table.set_fontsize(14)
    table.scale(1, 2.15)
    for (row, column), cell in table.get_celld().items():
        cell.set_edgecolor("#334155")
        if row == 0:
            cell.set_facecolor("#0f766e")
            cell.get_text().set_color("white")
            cell.get_text().set_fontweight("bold")
        elif column == 0:
            cell.set_facecolor("#ccfbf1")
            cell.get_text().set_fontweight("bold")
        elif row == len(ENTERPRISES) and column == len(RESOURCE_LEVELS):
            cell.set_facecolor("#fbbf24")
            cell.get_text().set_fontweight("bold")
    ax.text(
        0.5,
        0.07,
        "Оптимальне значення: φ₄(100) = 82",
        ha="center",
        transform=ax.transAxes,
        fontweight="bold",
    )
    save_figure(fig, output / "03-таблиця-беллмана.png")


def figure_stage_values(output: Path, dp: Sequence[Sequence[int]]) -> None:
    fig, ax = plt.subplots(figsize=(12.5, 7.2))
    colors = ("#2563eb", "#dc2626", "#059669", "#7c3aed")
    for stage, color in zip(range(1, len(ENTERPRISES) + 1), colors):
        ax.plot(
            RESOURCE_LEVELS,
            dp[stage],
            marker="o",
            linewidth=2.3,
            color=color,
            label=f"Після {stage} підпр.",
        )
    ax.scatter([100], [dp[4][5]], s=180, color="#f59e0b", edgecolor="#92400e", zorder=5)
    ax.annotate(
        "максимум 82",
        xy=(100, 82),
        xytext=(70, 75),
        arrowprops={"arrowstyle": "->", "color": "#92400e"},
        fontweight="bold",
    )
    ax.set_title("Зміна оптимального відгуку за етапами", fontweight="bold")
    ax.set_xlabel("Розподілений ресурс X, у. о.")
    ax.set_ylabel("Максимальний сумарний відгук φᵢ(X)")
    ax.set_xticks(RESOURCE_LEVELS)
    ax.grid(True, alpha=0.25)
    ax.legend(loc="upper left")
    save_figure(fig, output / "04-етапи-оптимізації.png")


def figure_transition_graph(output: Path, solution: Solution) -> None:
    fig, ax = plt.subplots(figsize=(14.5, 8.2))
    ax.set_xlim(-0.4, 4.4)
    ax.set_ylim(-0.7, 5.7)
    ax.axis("off")
    ax.set_title("Метод вартості переходів: оптимальний шлях у графі станів", fontweight="bold", pad=15)

    # Усі допустимі вершини шаруватого графа.
    for stage in range(5):
        for units in range(6):
            ax.scatter(stage, units, s=180, color="#e2e8f0", edgecolor="#64748b", zorder=3)
            ax.text(stage, units - 0.22, f"{units * 20}", ha="center", va="top", fontsize=10)
    for stage in range(5):
        ax.text(stage, 5.45, "Початок" if stage == 0 else f"Після П{stage}", ha="center", fontweight="bold")

    cumulative = [0]
    for units in solution.allocation_units:
        cumulative.append(cumulative[-1] + units)
    for stage in range(4):
        start = (stage, cumulative[stage])
        end = (stage + 1, cumulative[stage + 1])
        allocated = solution.allocation[stage]
        gain = solution.profits[stage]
        arrow = FancyArrowPatch(
            start,
            end,
            arrowstyle="-|>",
            mutation_scale=18,
            linewidth=3.2,
            color="#dc2626",
            zorder=4,
        )
        ax.add_patch(arrow)
        ax.text(
            (start[0] + end[0]) / 2,
            (start[1] + end[1]) / 2 + 0.28,
            f"x{stage + 1}={allocated}; +{gain}",
            ha="center",
            color="#991b1b",
            fontweight="bold",
            bbox={"boxstyle": "round,pad=0.2", "fc": "white", "ec": "none", "alpha": 0.9},
        )
    ax.scatter(range(5), cumulative, s=260, color="#fbbf24", edgecolor="#92400e", zorder=5)
    ax.text(2, -0.55, "Шлях: (0, 0) → (1, 0) → (2, 40) → (3, 60) → (4, 100)", ha="center", fontweight="bold")
    ax.text(-0.33, 2.5, "Використаний ресурс, у. о.", rotation=90, ha="center", va="center")
    save_figure(fig, output / "05-граф-переходів.png")


def figure_optimal_allocation(output: Path, solution: Solution) -> None:
    fig, axes = plt.subplots(1, 2, figsize=(13.5, 6.8))
    labels = [f"Підпр. {i}" for i in ENTERPRISES]
    colors = ("#94a3b8", "#2563eb", "#059669", "#7c3aed")
    axes[0].bar(labels, solution.allocation, color=colors, edgecolor="#334155")
    axes[0].set_title("Оптимальний розподіл ресурсу", fontweight="bold")
    axes[0].set_ylabel("Ресурс, у. о.")
    axes[0].set_ylim(0, 50)
    axes[0].grid(axis="y", alpha=0.25)
    axes[1].bar(labels, solution.profits, color=colors, edgecolor="#334155")
    axes[1].set_title("Отриманий відгук", fontweight="bold")
    axes[1].set_ylabel("Приріст випуску")
    axes[1].set_ylim(0, 42)
    axes[1].grid(axis="y", alpha=0.25)
    for ax, values in zip(axes, (solution.allocation, solution.profits)):
        for idx, value in enumerate(values):
            ax.text(idx, value + 1, str(value), ha="center", fontweight="bold")
    fig.suptitle("Результат: S = 100 у. о., Fmax = 82", fontweight="bold", fontsize=17)
    fig.tight_layout(rect=(0, 0, 1, 0.94))
    save_figure(fig, output / "06-оптимальний-розподіл.png")


def figure_verification(output: Path, ranked: Sequence[Solution]) -> None:
    top = ranked[:8]
    labels = ["–".join(str(x) for x in item.allocation) for item in top]
    values = [item.value for item in top]
    colors = ["#16a34a"] + ["#93c5fd"] * (len(top) - 1)
    fig, ax = plt.subplots(figsize=(13.5, 7.4))
    bars = ax.barh(range(len(top)), values, color=colors, edgecolor="#334155")
    ax.set_yticks(range(len(top)), labels)
    ax.invert_yaxis()
    ax.set_xlim(0, 90)
    ax.set_xlabel("Сумарний відгук")
    ax.set_ylabel("Розподіл (x₁–x₂–x₃–x₄), у. о.")
    ax.set_title("Перевірка: найкращі з 56 допустимих розподілів", fontweight="bold")
    ax.grid(axis="x", alpha=0.25)
    for bar, value in zip(bars, values):
        ax.text(value + 0.7, bar.get_y() + bar.get_height() / 2, str(value), va="center", fontweight="bold")
    ax.text(
        0.98,
        0.05,
        "Послідовний метод = 82\nМетод переходів = 82\nПовний перебір = 82",
        transform=ax.transAxes,
        ha="right",
        va="bottom",
        bbox={"boxstyle": "round,pad=0.5", "fc": "#f0fdf4", "ec": "#16a34a"},
        fontweight="bold",
    )
    save_figure(fig, output / "07-перевірка-методів.png")


def figure_console_result(output: Path, solution: Solution, variants_count: int) -> None:
    fig, ax = plt.subplots(figsize=(13.5, 6.8))
    fig.patch.set_facecolor("#111827")
    ax.set_facecolor("#111827")
    ax.axis("off")
    lines = [
        "ЛАБОРАТОРНА РОБОТА № 9",
        "Розподіл обмежених ресурсів",
        "",
        f"Номер студента: N = {STUDENT_NUMBER}; варіант = {VARIANT}",
        f"Загальний ресурс: S = {TOTAL_RESOURCE} у. о.",
        "",
        "Оптимальний розподіл:",
        f"  x₁ = {solution.allocation[0]}, x₂ = {solution.allocation[1]}, "
        f"x₃ = {solution.allocation[2]}, x₄ = {solution.allocation[3]}",
        f"  відгуки: {solution.profits[0]} + {solution.profits[1]} + "
        f"{solution.profits[2]} + {solution.profits[3]} = {solution.value}",
        "",
        f"Послідовний метод:      Fmax = {solution.value}",
        f"Метод вартості переходів: Fmax = {solution.value}",
        f"Повний перебір ({variants_count} варіантів): Fmax = {solution.value}",
        "",
        "Результати всіх методів збігаються.",
    ]
    y = 0.92
    for index, line in enumerate(lines):
        color = "#fbbf24" if index in (0, 6, 14) else "#e5e7eb"
        weight = "bold" if index in (0, 6, 14) else "normal"
        ax.text(0.06, y, line, transform=ax.transAxes, color=color, fontweight=weight, va="top")
        y -= 0.058
    save_figure(fig, output / "08-результат-програми.png")


def generate_figures(output: Path, solution: Solution, dp: Sequence[Sequence[int]], ranked: Sequence[Solution]) -> None:
    configure_style()
    figure_input_data(output)
    figure_response_curves(output)
    figure_dp_table(output, dp)
    figure_stage_values(output, dp)
    figure_transition_graph(output, solution)
    figure_optimal_allocation(output, solution)
    figure_verification(output, ranked)
    figure_console_result(output, solution, len(ranked))


def main() -> None:
    sequential, dp, _choice = sequential_dynamic_programming()
    transitions, _best, _predecessor = transition_cost_method()
    ranked = exhaustive_search()
    if not (sequential == transitions == ranked[0]):
        raise RuntimeError("Незалежні методи дали різні результати")

    output = Path(__file__).resolve().parents[1] / "assets" / "screenshots"
    generate_figures(output, sequential, dp, ranked)

    allocation = ", ".join(str(value) for value in sequential.allocation)
    profits = " + ".join(str(value) for value in sequential.profits)
    print("Лабораторна робота № 9 — розподіл обмежених ресурсів")
    print(f"N = {STUDENT_NUMBER}; варіант = {VARIANT}; S = {TOTAL_RESOURCE}")
    print(f"Оптимальний розподіл: ({allocation})")
    print(f"Сумарний відгук: {profits} = {sequential.value}")
    print(f"Перевірено повним перебором: {len(ranked)} розподілів")
    print("Послідовний метод, метод переходів і повний перебір збігаються.")


if __name__ == "__main__":
    main()
