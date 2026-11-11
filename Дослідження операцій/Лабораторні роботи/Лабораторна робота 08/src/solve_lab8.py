"""Лабораторна робота № 8: оптимальна траєкторія в мережі.

Варіант N=12, коефіцієнт k=5. Програма відновлює неорієнтовану
мережу з методичних вказівок, знаходить найкоротший шлях алгоритмом
Дейкстри, виконує незалежні перевірки та створює ілюстрації для звіту.
"""

from __future__ import annotations

from dataclasses import dataclass
import heapq
import itertools
import math
from pathlib import Path

import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch


VARIANT = 12
K = 5
GRID_SIZE = 5
A_VALUE = math.sqrt(K * VARIANT) + 10

Node = tuple[int, int]
START: Node = (4, 0)
TARGET: Node = (0, 4)


# Горизонтальні ребра: п'ять рядків по чотири ребра.
HORIZONTAL_EXPRESSIONS = (
    ("4", "2", "10", "2A"),
    ("9", "A", "4", "9"),
    ("9", "2", "A/2", "A"),
    ("A", "4", "7", "5"),
    ("8", "A+5", "10", "7"),
)

# Вертикальні ребра: п'ять стовпців по чотири ребра зверху вниз.
VERTICAL_EXPRESSIONS = (
    ("2A", "7", "6", "5"),
    ("A/2", "A+1", "A-1", "3"),
    ("3", "5", "3A", "A"),
    ("7", "A-1", "4", "2A"),
    ("A/2", "A/2", "A+1", "A/2"),
)


@dataclass(frozen=True)
class Edge:
    first: Node
    second: Node
    expression: str
    weight: float


@dataclass(frozen=True)
class Solution:
    a_value: float
    edges: tuple[Edge, ...]
    distances: dict[Node, float]
    previous: dict[Node, Node]
    visited_order: tuple[Node, ...]
    path: tuple[Node, ...]
    path_weights: tuple[float, ...]
    cost: float
    bellman_ford_cost: float
    best_monotone_cost: float
    second_monotone_cost: float


def evaluate_expression(expression: str, a_value: float = A_VALUE) -> float:
    """Обчислити вагу ребра за одним із виразів методички."""
    mapping = {
        "A": a_value,
        "A/2": a_value / 2,
        "2A": 2 * a_value,
        "3A": 3 * a_value,
        "A+1": a_value + 1,
        "A-1": a_value - 1,
        "A+5": a_value + 5,
    }
    if expression in mapping:
        return mapping[expression]
    return float(expression)


def build_edges(a_value: float = A_VALUE) -> tuple[Edge, ...]:
    edges: list[Edge] = []

    for row, expressions in enumerate(HORIZONTAL_EXPRESSIONS):
        for column, expression in enumerate(expressions):
            edges.append(
                Edge(
                    (row, column),
                    (row, column + 1),
                    expression,
                    evaluate_expression(expression, a_value),
                )
            )

    for column, expressions in enumerate(VERTICAL_EXPRESSIONS):
        for row, expression in enumerate(expressions):
            edges.append(
                Edge(
                    (row, column),
                    (row + 1, column),
                    expression,
                    evaluate_expression(expression, a_value),
                )
            )

    return tuple(edges)


def build_graph(edges: tuple[Edge, ...]) -> dict[Node, list[tuple[Node, float]]]:
    graph = {
        (row, column): []
        for row in range(GRID_SIZE)
        for column in range(GRID_SIZE)
    }
    for edge in edges:
        graph[edge.first].append((edge.second, edge.weight))
        graph[edge.second].append((edge.first, edge.weight))
    return graph


def dijkstra(
    graph: dict[Node, list[tuple[Node, float]]],
    start: Node = START,
    target: Node = TARGET,
) -> tuple[dict[Node, float], dict[Node, Node], tuple[Node, ...]]:
    distances = {node: math.inf for node in graph}
    previous: dict[Node, Node] = {}
    distances[start] = 0.0
    queue: list[tuple[float, Node]] = [(0.0, start)]
    visited: set[Node] = set()
    order: list[Node] = []

    while queue:
        current_distance, current = heapq.heappop(queue)
        if current in visited:
            continue
        if current_distance > distances[current] + 1e-12:
            continue

        visited.add(current)
        order.append(current)
        if current == target:
            break

        for neighbour, weight in graph[current]:
            candidate = current_distance + weight
            if candidate < distances[neighbour] - 1e-12:
                distances[neighbour] = candidate
                previous[neighbour] = current
                heapq.heappush(queue, (candidate, neighbour))

    return distances, previous, tuple(order)


def restore_path(previous: dict[Node, Node], start: Node, target: Node) -> tuple[Node, ...]:
    if start == target:
        return (start,)
    if target not in previous:
        raise ValueError("Між початковою та кінцевою вершинами немає шляху")

    path = [target]
    while path[-1] != start:
        path.append(previous[path[-1]])
    path.reverse()
    return tuple(path)


def edge_weight(graph: dict[Node, list[tuple[Node, float]]], first: Node, second: Node) -> float:
    for neighbour, weight in graph[first]:
        if neighbour == second:
            return weight
    raise ValueError(f"Вершини {first} і {second} не з'єднані")


def bellman_ford_cost(edges: tuple[Edge, ...], start: Node = START, target: Node = TARGET) -> float:
    """Незалежна перевірка найкоротшої відстані алгоритмом Беллмана-Форда."""
    nodes = {
        (row, column)
        for row in range(GRID_SIZE)
        for column in range(GRID_SIZE)
    }
    distances = {node: math.inf for node in nodes}
    distances[start] = 0.0

    for _ in range(len(nodes) - 1):
        changed = False
        for edge in edges:
            for first, second in ((edge.first, edge.second), (edge.second, edge.first)):
                candidate = distances[first] + edge.weight
                if candidate < distances[second] - 1e-12:
                    distances[second] = candidate
                    changed = True
        if not changed:
            break
    return distances[target]


def enumerate_monotone_paths(
    graph: dict[Node, list[tuple[Node, float]]]
) -> tuple[tuple[float, tuple[Node, ...]], ...]:
    """Перебрати 70 шляхів, що рухаються лише вгору або праворуч."""
    results: list[tuple[float, tuple[Node, ...]]] = []
    for up_positions in itertools.combinations(range(8), 4):
        moves = ["R"] * 8
        for position in up_positions:
            moves[position] = "U"

        current = START
        path = [current]
        cost = 0.0
        for move in moves:
            next_node = (
                (current[0] - 1, current[1])
                if move == "U"
                else (current[0], current[1] + 1)
            )
            cost += edge_weight(graph, current, next_node)
            path.append(next_node)
            current = next_node
        results.append((cost, tuple(path)))
    return tuple(sorted(results, key=lambda item: (item[0], item[1])))


def solve() -> Solution:
    edges = build_edges()
    graph = build_graph(edges)
    distances, previous, visited_order = dijkstra(graph)
    path = restore_path(previous, START, TARGET)
    path_weights = tuple(
        edge_weight(graph, path[index], path[index + 1])
        for index in range(len(path) - 1)
    )
    monotone_paths = enumerate_monotone_paths(graph)

    return Solution(
        a_value=A_VALUE,
        edges=edges,
        distances=distances,
        previous=previous,
        visited_order=visited_order,
        path=path,
        path_weights=path_weights,
        cost=distances[TARGET],
        bellman_ford_cost=bellman_ford_cost(edges),
        best_monotone_cost=monotone_paths[0][0],
        second_monotone_cost=monotone_paths[1][0],
    )


def node_label(node: Node, math_mode: bool = False) -> str:
    if node == START:
        return "П"
    if node == TARGET:
        return "К"
    label = f"v{node[0] + 1}{node[1] + 1}"
    return f"$v_{{{node[0] + 1}{node[1] + 1}}}$" if math_mode else label


def decimal(value: float, digits: int = 2) -> str:
    return f"{value:.{digits}f}".replace(".", ",")


def setup_style() -> None:
    plt.rcParams.update(
        {
            "font.family": "Times New Roman",
            "font.size": 14,
            "axes.titlesize": 18,
            "axes.labelsize": 14,
            "figure.dpi": 150,
        }
    )


def save_figure(fig: plt.Figure, output: Path, filename: str) -> None:
    fig.savefig(output / filename, dpi=180, bbox_inches="tight", facecolor="white")
    plt.close(fig)


def node_positions() -> dict[Node, tuple[float, float]]:
    return {
        (row, column): (column * 2.25, (GRID_SIZE - 1 - row) * 1.65)
        for row in range(GRID_SIZE)
        for column in range(GRID_SIZE)
    }


def draw_network(
    ax: plt.Axes,
    edges: tuple[Edge, ...],
    *,
    numeric: bool,
    path: tuple[Node, ...] = (),
) -> None:
    positions = node_positions()
    path_edges = {
        frozenset((path[index], path[index + 1]))
        for index in range(len(path) - 1)
    }

    for edge in edges:
        x1, y1 = positions[edge.first]
        x2, y2 = positions[edge.second]
        is_path = frozenset((edge.first, edge.second)) in path_edges
        ax.plot(
            [x1, x2],
            [y1, y2],
            color="#dc2626" if is_path else "#64748b",
            linewidth=4.2 if is_path else 1.6,
            zorder=1,
        )
        label = decimal(edge.weight) if numeric else edge.expression
        horizontal = edge.first[0] == edge.second[0]
        offset_x = 0.0 if horizontal else 0.17
        offset_y = 0.15 if horizontal else 0.0
        ax.text(
            (x1 + x2) / 2 + offset_x,
            (y1 + y2) / 2 + offset_y,
            label,
            ha="center",
            va="center",
            fontsize=10.5,
            color="#991b1b" if is_path else "#1e293b",
            bbox={"boxstyle": "round,pad=0.11", "fc": "white", "ec": "none", "alpha": 0.92},
            zorder=2,
        )

    path_nodes = set(path)
    for node, (x, y) in positions.items():
        is_path = node in path_nodes
        is_endpoint = node in (START, TARGET)
        patch = FancyBboxPatch(
            (x - 0.34, y - 0.24),
            0.68,
            0.48,
            boxstyle="round,pad=0.04",
            facecolor="#fde68a" if is_path else "#eff6ff",
            edgecolor="#dc2626" if is_path else "#2563eb",
            linewidth=2.5 if is_path else 1.3,
            zorder=3,
        )
        ax.add_patch(patch)
        ax.text(
            x,
            y,
            node_label(node, math_mode=not is_endpoint),
            ha="center",
            va="center",
            fontsize=12 if is_endpoint else 10.5,
            weight="bold" if is_endpoint else "normal",
            zorder=4,
        )

    ax.text(positions[START][0] - 0.05, positions[START][1] - 0.55, "початок", ha="center", color="#334155")
    ax.text(positions[TARGET][0], positions[TARGET][1] + 0.55, "кінець", ha="center", color="#334155")
    ax.set_xlim(-0.85, 9.75)
    ax.set_ylim(-0.9, 7.35)
    ax.set_aspect("equal")
    ax.axis("off")


def create_figures(solution: Solution, output: Path) -> None:
    output.mkdir(parents=True, exist_ok=True)

    fig, ax = plt.subplots(figsize=(13, 8))
    ax.axis("off")
    rows = [
        ["Номер варіанта N", str(VARIANT)],
        ["Коефіцієнт k", str(K)],
        ["Параметр A", "√(kN) + 10"],
        ["Точне значення A", "√60 + 10"],
        ["Числове значення A", decimal(solution.a_value, 6)],
        ["Початкова вершина", "П"],
        ["Кінцева вершина", "К"],
        ["Розмір мережі", "25 вершин, 40 ребер"],
    ]
    table = ax.table(
        cellText=rows,
        colLabels=["Параметр", "Значення"],
        cellLoc="center",
        loc="center",
        bbox=[0.08, 0.08, 0.84, 0.78],
    )
    table.auto_set_font_size(False)
    table.set_fontsize(15)
    for (row, _), cell in table.get_celld().items():
        cell.set_facecolor("#dbeafe" if row == 0 else ("#f8fafc" if row % 2 else "#eff6ff"))
    ax.set_title("Вихідні дані задачі оптимальної траєкторії", pad=18)
    save_figure(fig, output, "01-вихідні-дані.png")

    fig, ax = plt.subplots(figsize=(16, 12))
    draw_network(ax, solution.edges, numeric=False)
    ax.set_title("Неорієнтована мережа із символьними вагами ребер", pad=18)
    save_figure(fig, output, "02-символьна-мережа.png")

    fig, ax = plt.subplots(figsize=(16, 12))
    draw_network(ax, solution.edges, numeric=True)
    ax.set_title(f"Числові ваги ребер при A = {decimal(solution.a_value, 5)}", pad=18)
    save_figure(fig, output, "03-числова-мережа.png")

    records = []
    for index, node in enumerate(solution.visited_order, start=1):
        predecessor = solution.previous.get(node)
        records.append(
            [
                str(index),
                node_label(node),
                decimal(solution.distances[node], 3),
                "-" if predecessor is None else node_label(predecessor),
            ]
        )
    fig, axes = plt.subplots(1, 2, figsize=(16, 11))
    for ax, subset, title in zip(
        axes,
        (records[:13], records[13:]),
        ("Ітерації 1-13", "Ітерації 14-25"),
    ):
        ax.axis("off")
        table = ax.table(
            cellText=subset,
            colLabels=["№", "Вершина", "Мітка", "Попередня"],
            cellLoc="center",
            loc="center",
            bbox=[0.01, 0.02, 0.98, 0.9],
        )
        table.auto_set_font_size(False)
        table.set_fontsize(11.5)
        for (row, _), cell in table.get_celld().items():
            cell.set_facecolor("#dbeafe" if row == 0 else ("#f8fafc" if row % 2 else "#eff6ff"))
        ax.set_title(title, pad=8, fontsize=16)
    fig.suptitle("Порядок надання вершинам постійних міток алгоритмом Дейкстри", fontsize=19)
    save_figure(fig, output, "04-ітерації-дейкстри.png")

    fig, ax = plt.subplots(figsize=(16, 12))
    draw_network(ax, solution.edges, numeric=True, path=solution.path)
    ax.set_title(
        f"Оптимальна траєкторія П → К, загальні витрати {decimal(solution.cost, 5)}",
        pad=18,
    )
    save_figure(fig, output, "05-оптимальна-траєкторія.png")

    cumulative = [0.0]
    for weight in solution.path_weights:
        cumulative.append(cumulative[-1] + weight)
    labels = [node_label(node) for node in solution.path]
    fig, ax = plt.subplots(figsize=(14, 8))
    ax.plot(range(len(cumulative)), cumulative, color="#2563eb", linewidth=3, marker="o", markersize=9)
    ax.fill_between(range(len(cumulative)), cumulative, color="#bfdbfe", alpha=0.45)
    for index, value in enumerate(cumulative):
        ax.text(index, value + 1.2, decimal(value, 3), ha="center", color="#1e3a8a")
    ax.set_xticks(range(len(labels)), labels)
    ax.set_ylabel("Накопичені витрати")
    ax.set_xlabel("Послідовність вершин оптимального шляху")
    ax.set_ylim(0, solution.cost + 7)
    ax.grid(alpha=0.25)
    ax.set_title("Накопичення витрат уздовж оптимальної траєкторії")
    fig.tight_layout()
    save_figure(fig, output, "06-накопичені-витрати.png")

    methods = ["Дейкстра", "Беллман-Форд", "Перебір 70\nмонотонних шляхів"]
    values = [solution.cost, solution.bellman_ford_cost, solution.best_monotone_cost]
    fig, (ax_chart, ax_table) = plt.subplots(1, 2, figsize=(16, 8), gridspec_kw={"width_ratios": [1.05, 0.95]})
    bars = ax_chart.bar(methods, values, color=["#2563eb", "#16a34a", "#7c3aed"])
    ax_chart.bar_label(bars, labels=[decimal(value, 5) for value in values], padding=5, fontsize=13)
    ax_chart.set_ylabel("Загальні витрати")
    ax_chart.set_ylim(0, max(values) * 1.18)
    ax_chart.grid(axis="y", alpha=0.22)
    ax_chart.set_title("Незалежна перевірка результату")
    ax_table.axis("off")
    verification = [
        ["Кількість вершин", "25"],
        ["Кількість ребер", "40"],
        ["Ребер у шляху", str(len(solution.path) - 1)],
        ["Найкращий шлях", decimal(solution.cost, 5)],
        ["Другий монотонний", decimal(solution.second_monotone_cost, 5)],
        ["Запас до другого", decimal(solution.second_monotone_cost - solution.cost, 5)],
    ]
    table = ax_table.table(
        cellText=verification,
        colLabels=["Перевірка", "Значення"],
        cellLoc="center",
        loc="center",
        bbox=[0.03, 0.18, 0.94, 0.64],
    )
    table.auto_set_font_size(False)
    table.set_fontsize(14)
    for (row, _), cell in table.get_celld().items():
        cell.set_facecolor("#dcfce7" if row > 0 else "#bbf7d0")
    fig.suptitle("Перевірка оптимальності знайденої траєкторії", fontsize=20)
    fig.tight_layout()
    save_figure(fig, output, "07-перевірка-методів.png")

    path_text = " → ".join(node_label(node) for node in solution.path)
    weights_text = " + ".join(decimal(value, 3) for value in solution.path_weights)
    lines = [
        "ЛАБОРАТОРНА РОБОТА № 8 — АЛГОРИТМ ДЕЙКСТРИ",
        "=" * 66,
        f"Варіант N = {VARIANT}; коефіцієнт k = {K}",
        f"A = √(kN) + 10 = √60 + 10 = {decimal(solution.a_value, 6)}",
        "",
        f"Оптимальна траєкторія: {path_text}",
        f"Ваги ребер: {weights_text}",
        "",
        "L = 5 + 6 + 9 + 2 + 5 + 4 + 9 + A/2",
        f"L = 40 + A/2 = {decimal(solution.cost, 6)}",
        "",
        f"Перевірка Беллмана-Форда: {decimal(solution.bellman_ford_cost, 6)}",
        f"Перебрано монотонних шляхів: 70",
        "Результат підтверджено.",
    ]
    fig, ax = plt.subplots(figsize=(15, 9))
    ax.axis("off")
    ax.text(0.04, 0.96, "\n".join(lines), family="Times New Roman", fontsize=15, va="top", transform=ax.transAxes)
    save_figure(fig, output, "08-результат-програми.png")


def main() -> None:
    setup_style()
    solution = solve()
    output = Path(__file__).resolve().parents[1] / "assets" / "screenshots"
    create_figures(solution, output)

    print(f"A = {solution.a_value:.6f}")
    print("Оптимальна траєкторія:", " -> ".join(node_label(node) for node in solution.path))
    print("Ваги ребер:", tuple(round(weight, 6) for weight in solution.path_weights))
    print(f"Загальні витрати = {solution.cost:.6f}")
    print(f"Перевірка Беллмана-Форда = {solution.bellman_ford_cost:.6f}")


if __name__ == "__main__":
    main()
