"""Лабораторна робота № 5: задача комівояжера та маршрутизація.

Варіант 12. Програма відтворює транспортний граф із методичних
вказівок, будує мінімальне дерево, матрицю найкоротших відстаней,
маршрути методом Свіра та точний розв'язок задачі маршрутизації.
"""

from __future__ import annotations

from dataclasses import dataclass
from functools import lru_cache
from itertools import permutations
from math import atan2, ceil, degrees
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
from scipy.sparse.csgraph import minimum_spanning_tree


VARIANT = 12
CAPACITY = 100
DEMANDS = np.array([30, 26, 20, 19, 18, 18, 24, 27, 20, 21], dtype=int)
NODES = list(range(11))  # 0 — склад C, 1..10 — споживачі

# Ребра графа варіанта 2, 12: (початок, кінець, довжина).
EDGES = [
    (0, 1, 33.4), (0, 2, 36.1), (0, 6, 25.0), (0, 7, 22.4),
    (1, 2, 63.5), (1, 3, 32.3), (1, 4, 44.2), (1, 6, 38.6),
    (2, 3, 65.2), (2, 7, 40.0), (2, 8, 47.2), (2, 9, 31.6),
    (3, 4, 66.1), (4, 6, 61.8), (4, 5, 85.6), (5, 6, 35.4),
    (5, 7, 40.3), (5, 8, 44.7), (5, 10, 33.0), (6, 7, 25.0),
    (7, 8, 25.0), (8, 9, 30.4), (8, 10, 42.1), (9, 10, 70.5),
]

# Координати відновлено за підписаними довжинами ребер (похибка < 0,2).
COORDINATES = np.array(
    [
        (0.00, 0.00), (-31.90, -9.70), (15.40, 32.60),
        (-48.23, 18.03), (-53.69, -47.97), (31.93, -45.87),
        (3.59, -24.73), (21.24, -7.00), (45.95, -3.40),
        (46.49, 26.99), (64.59, -41.15),
    ],
    dtype=float,
)


@dataclass(frozen=True)
class RoutePlan:
    name: str
    routes: tuple[tuple[int, ...], ...]
    loads: tuple[int, ...]
    lengths: tuple[float, ...]

    @property
    def total_length(self) -> float:
        return float(sum(self.lengths))


def node_name(node: int) -> str:
    return "C" if node == 0 else str(node)


def build_adjacency() -> np.ndarray:
    matrix = np.full((11, 11), np.inf, dtype=float)
    np.fill_diagonal(matrix, 0.0)
    for start, end, length in EDGES:
        matrix[start, end] = matrix[end, start] = length
    return matrix


def floyd_warshall(adjacency: np.ndarray) -> tuple[np.ndarray, np.ndarray]:
    """Повертає матрицю найкоротших відстаней і наступні вершини шляхів."""
    distance = adjacency.copy()
    next_node = np.full(distance.shape, -1, dtype=int)
    for i in NODES:
        for j in NODES:
            if i != j and np.isfinite(distance[i, j]):
                next_node[i, j] = j
    for k in NODES:
        for i in NODES:
            for j in NODES:
                candidate = distance[i, k] + distance[k, j]
                if candidate < distance[i, j] - 1e-9:
                    distance[i, j] = candidate
                    next_node[i, j] = next_node[i, k]
    return distance, next_node


def reconstruct_path(start: int, end: int, next_node: np.ndarray) -> list[int]:
    if next_node[start, end] < 0:
        raise ValueError(f"Немає шляху між {start} та {end}")
    path = [start]
    while start != end:
        start = int(next_node[start, end])
        path.append(start)
    return path


def minimum_tree_edges() -> tuple[tuple[int, int, float], ...]:
    adjacency = build_adjacency()
    sparse_input = np.where(np.isfinite(adjacency), adjacency, 0.0)
    tree = minimum_spanning_tree(sparse_input).toarray()
    return tuple((i, j, float(tree[i, j])) for i in NODES for j in NODES if tree[i, j] > 0)


def tree_schemes() -> tuple[tuple[str, tuple[tuple[int, int, float], ...]], ...]:
    base = list(minimum_tree_edges())
    edge_map = {(min(i, j), max(i, j)): length for i, j, length in EDGES}

    def replace(remove: tuple[int, int], add: tuple[int, int]) -> tuple[tuple[int, int, float], ...]:
        result = [(i, j, w) for i, j, w in base if (min(i, j), max(i, j)) != remove]
        result.append((add[0], add[1], edge_map[(min(add), max(add))]))
        return tuple(result)

    return (
        ("Схема 1", tuple(base)),
        ("Схема 2", replace((0, 6), (6, 7))),
        ("Схема 3", replace((0, 7), (6, 7))),
    )


def tree_components(tree_edges: tuple[tuple[int, int, float], ...]) -> list[list[int]]:
    neighbors = {node: set() for node in range(1, 11)}
    for start, end, _ in tree_edges:
        if start != 0 and end != 0:
            neighbors[start].add(end)
            neighbors[end].add(start)
    components = []
    unseen = set(range(1, 11))
    while unseen:
        root = min(unseen)
        stack = [root]
        component = []
        while stack:
            node = stack.pop()
            if node not in unseen:
                continue
            unseen.remove(node)
            component.append(node)
            stack.extend(neighbors[node])
        components.append(sorted(component))
    return components


def route_length(route: tuple[int, ...], distance: np.ndarray) -> float:
    chain = (0,) + route + (0,)
    return float(sum(distance[chain[i], chain[i + 1]] for i in range(len(chain) - 1)))


@lru_cache(maxsize=None)
def _tsp_cached(customers: tuple[int, ...], distance_key: bytes) -> tuple[float, tuple[int, ...]]:
    distance = np.frombuffer(distance_key, dtype=np.float64).reshape((11, 11))
    best_length = np.inf
    best_route: tuple[int, ...] = ()
    for order in permutations(customers):
        length = route_length(order, distance)
        if length < best_length - 1e-9:
            best_length = length
            best_route = tuple(order)
    return float(best_length), best_route


def tsp_route(customers: list[int] | tuple[int, ...], distance: np.ndarray) -> tuple[float, tuple[int, ...]]:
    return _tsp_cached(tuple(sorted(customers)), distance.astype(np.float64).tobytes())


def plan_from_groups(name: str, groups: list[list[int]], distance: np.ndarray) -> RoutePlan:
    routes = []
    loads = []
    lengths = []
    for group in groups:
        length, route = tsp_route(group, distance)
        routes.append(route)
        loads.append(int(sum(DEMANDS[node - 1] for node in group)))
        lengths.append(round(length, 1))
    return RoutePlan(name, tuple(routes), tuple(loads), tuple(lengths))


def minimum_tree_plan(distance: np.ndarray) -> RoutePlan:
    groups = tree_components(minimum_tree_edges())
    return plan_from_groups("Мінімальне дерево", groups, distance)


def polar_angles() -> dict[int, float]:
    return {
        node: (degrees(atan2(COORDINATES[node, 1], COORDINATES[node, 0])) + 360.0) % 360.0
        for node in range(1, 11)
    }


def sweep_groups(capacity: int = CAPACITY) -> list[list[int]]:
    ordered = sorted(range(1, 11), key=lambda node: (polar_angles()[node], node))
    groups: list[list[int]] = [[]]
    current_load = 0
    for node in ordered:
        demand = int(DEMANDS[node - 1])
        if groups[-1] and current_load + demand > capacity:
            groups.append([])
            current_load = 0
        groups[-1].append(node)
        current_load += demand
    return groups


def sweep_plan(distance: np.ndarray) -> RoutePlan:
    return plan_from_groups("Метод Свіра", sweep_groups(), distance)


def exact_cvrp(distance: np.ndarray, capacity: int = CAPACITY) -> RoutePlan:
    """Точний перебір допустимих підмножин із TSP-оптимізацією маршрутів."""
    full_mask = (1 << 10) - 1
    number_of_routes = ceil(int(DEMANDS.sum()) / capacity)
    feasible: dict[int, tuple[float, tuple[int, ...], int]] = {}
    for mask in range(1, full_mask + 1):
        customers = [index + 1 for index in range(10) if mask & (1 << index)]
        load = int(sum(DEMANDS[node - 1] for node in customers))
        if load <= capacity:
            length, route = tsp_route(customers, distance)
            feasible[mask] = (length, route, load)

    @lru_cache(maxsize=None)
    def search(remaining: int, routes_left: int):
        if remaining == 0 and routes_left == 0:
            return 0.0, ()
        if remaining == 0 or routes_left == 0:
            return np.inf, ()
        first_bit = remaining & -remaining
        best = (np.inf, ())
        subset = remaining
        while subset:
            if subset & first_bit and subset in feasible:
                tail_cost, tail_masks = search(remaining ^ subset, routes_left - 1)
                candidate = feasible[subset][0] + tail_cost
                if candidate < best[0] - 1e-9:
                    best = (candidate, (subset,) + tail_masks)
            subset = (subset - 1) & remaining
        return best

    _, masks = search(full_mask, number_of_routes)
    records = sorted((feasible[mask] for mask in masks), key=lambda item: min(item[1]))
    return RoutePlan(
        "Точний розв'язок",
        tuple(item[1] for item in records),
        tuple(item[2] for item in records),
        tuple(round(item[0], 1) for item in records),
    )


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


def draw_base_graph(ax: plt.Axes, edge_labels: bool = True) -> None:
    for start, end, length in EDGES:
        x = [COORDINATES[start, 0], COORDINATES[end, 0]]
        y = [COORDINATES[start, 1], COORDINATES[end, 1]]
        ax.plot(x, y, color="#94a3b8", linewidth=1.4, zorder=1)
        if edge_labels:
            ax.text(np.mean(x), np.mean(y), f"{length:.1f}".replace(".", ","), fontsize=9,
                    ha="center", va="center", bbox={"fc": "white", "ec": "none", "alpha": 0.8})
    ax.scatter(COORDINATES[1:, 0], COORDINATES[1:, 1], s=500, color="#2563eb", zorder=3)
    ax.scatter([0], [0], s=650, marker="s", color="#16a34a", zorder=3)
    ax.text(0, 0, "C", ha="center", va="center", color="white", weight="bold", zorder=4)
    for node in range(1, 11):
        ax.text(*COORDINATES[node], str(node), ha="center", va="center", color="white", weight="bold", zorder=4)
    ax.set_aspect("equal")
    ax.axis("off")


def draw_routes(ax: plt.Axes, plan: RoutePlan, next_node: np.ndarray, title: str) -> None:
    draw_base_graph(ax, edge_labels=False)
    colors = ["#dc2626", "#7c3aed", "#ea580c", "#0891b2"]
    for route_index, (route, load, length) in enumerate(zip(plan.routes, plan.loads, plan.lengths)):
        color = colors[route_index]
        service_chain = (0,) + route + (0,)
        for index in range(len(service_chain) - 1):
            path = reconstruct_path(service_chain[index], service_chain[index + 1], next_node)
            for start, end in zip(path, path[1:]):
                ax.plot(
                    [COORDINATES[start, 0], COORDINATES[end, 0]],
                    [COORDINATES[start, 1], COORDINATES[end, 1]],
                    color=color, linewidth=4.0, alpha=0.78, zorder=2,
                )
        route_text = "C–" + "–".join(map(str, route)) + "–C"
        ax.plot([], [], color=color, linewidth=4,
                label=f"{route_text}; Q={load} кг; L={length:.1f}".replace(".", ","))
    ax.legend(loc="upper left", bbox_to_anchor=(0.0, -0.02), frameon=False, fontsize=11)
    ax.set_title(title)


def create_figures(
    distance: np.ndarray,
    next_node: np.ndarray,
    tree_plan: RoutePlan,
    sweep: RoutePlan,
    exact: RoutePlan,
    output: Path,
) -> None:
    output.mkdir(parents=True, exist_ok=True)

    fig, (ax_graph, ax_table) = plt.subplots(1, 2, figsize=(18, 9), gridspec_kw={"width_ratios": [1.45, 0.8]})
    draw_base_graph(ax_graph, edge_labels=True)
    ax_graph.set_title("Транспортний граф варіанта 12")
    ax_table.axis("off")
    rows = [[str(node), str(DEMANDS[node - 1])] for node in range(1, 11)]
    table = ax_table.table(cellText=rows, colLabels=["Споживач", "Потреба, кг"], cellLoc="center",
                           loc="center", bbox=[0.12, 0.13, 0.76, 0.75])
    table.auto_set_font_size(False)
    table.set_fontsize(14)
    for (row, _), cell in table.get_celld().items():
        cell.set_facecolor("#dbeafe" if row == 0 else ("#f8fafc" if row % 2 else "#eff6ff"))
    ax_table.text(0.5, 0.05, f"ΣQ = {DEMANDS.sum()} кг; q = {CAPACITY} кг; N = 3",
                  ha="center", weight="bold", transform=ax_table.transAxes)
    fig.suptitle("Вихідні дані задачі маршрутизації", fontsize=20)
    fig.tight_layout()
    save_figure(fig, output / "01-вихідні-дані-та-граф.png")

    schemes = tree_schemes()
    fig, axes = plt.subplots(1, 3, figsize=(21, 7), constrained_layout=True)
    for ax, (name, edges) in zip(axes, schemes):
        draw_base_graph(ax, edge_labels=False)
        for start, end, _ in edges:
            ax.plot([COORDINATES[start, 0], COORDINATES[end, 0]],
                    [COORDINATES[start, 1], COORDINATES[end, 1]],
                    color="#dc2626", linewidth=4.5, zorder=2)
        total = sum(edge[2] for edge in edges)
        ax.set_title(f"{name}\nΣL = {total:.1f}".replace(".", ","))
    fig.suptitle("Порівняння схем найкоротшої з'єднувальної мережі", fontsize=20)
    save_figure(fig, output / "02-схеми-мінімального-дерева.png")

    fig, ax = plt.subplots(figsize=(13, 10))
    image = ax.imshow(distance, cmap="YlGnBu")
    labels = ["C"] + [str(node) for node in range(1, 11)]
    ax.set_xticks(range(11), labels)
    ax.set_yticks(range(11), labels)
    ax.set_xlabel("Пункт призначення")
    ax.set_ylabel("Пункт відправлення")
    ax.set_title("Матриця найкоротших відстаней між пунктами")
    for i in NODES:
        for j in NODES:
            color = "white" if distance[i, j] > 75 else "black"
            ax.text(j, i, f"{distance[i, j]:.1f}".replace(".", ","), ha="center", va="center", fontsize=9, color=color)
    fig.colorbar(image, ax=ax, shrink=0.82, label="Відстань")
    fig.tight_layout()
    save_figure(fig, output / "03-матриця-відстаней.png")

    fig, ax = plt.subplots(figsize=(13, 9))
    draw_routes(ax, tree_plan, next_node, "Кільцеві маршрути за вибраним мінімальним деревом")
    fig.tight_layout()
    save_figure(fig, output / "04-маршрути-мінімального-дерева.png")

    angles = polar_angles()
    groups = sweep_groups()
    group_of = {node: index for index, group in enumerate(groups) for node in group}
    colors = ["#dc2626", "#7c3aed", "#ea580c"]
    fig = plt.figure(figsize=(12, 10))
    ax = fig.add_subplot(111, projection="polar")
    for node in range(1, 11):
        angle = np.radians(angles[node])
        radius = distance[0, node]
        color = colors[group_of[node]]
        ax.scatter(angle, radius, s=650, color=color, zorder=3)
        ax.text(angle, radius, f"{node}\nQ={DEMANDS[node - 1]}", ha="center", va="center", color="white", fontsize=10, zorder=4)
        ax.plot([angle, angle], [0, radius], color=color, alpha=0.35, linewidth=1.5)
    for index, group in enumerate(groups):
        load = sum(DEMANDS[node - 1] for node in group)
        ax.plot([], [], marker="o", linestyle="", color=colors[index], markersize=11,
                label=f"Маршрут {index + 1}: {group}; Q={load} кг")
    ax.set_theta_zero_location("E")
    ax.set_theta_direction(1)
    ax.set_title("Графік Свіра: обхід проти годинникової стрілки", pad=25)
    ax.set_rlabel_position(135)
    ax.legend(loc="lower center", bbox_to_anchor=(0.5, -0.16), frameon=False)
    save_figure(fig, output / "05-графік-свіра.png")

    fig, ax = plt.subplots(figsize=(13, 9))
    draw_routes(ax, sweep, next_node, "Маршрути, сформовані методом Свіра")
    fig.tight_layout()
    save_figure(fig, output / "06-маршрути-свіра.png")

    fig, (ax_graph, ax_bar) = plt.subplots(1, 2, figsize=(18, 8), gridspec_kw={"width_ratios": [1.4, 0.8]})
    draw_routes(ax_graph, exact, next_node, "Точний оптимальний план маршрутів")
    names = [tree_plan.name, sweep.name, exact.name]
    values = [tree_plan.total_length, sweep.total_length, exact.total_length]
    bars = ax_bar.bar(names, values, color=["#2563eb", "#7c3aed", "#16a34a"])
    ax_bar.bar_label(bars, labels=[f"{value:.1f}".replace(".", ",") for value in values], padding=5)
    ax_bar.set_ylabel("Сумарна довжина")
    ax_bar.set_title("Порівняння методів")
    ax_bar.grid(axis="y", alpha=0.25)
    ax_bar.tick_params(axis="x", rotation=20)
    ax_bar.set_ylim(0, max(values) * 1.18)
    fig.suptitle("Оптимізація маршрутів для вантажопідйомності 100 кг", fontsize=20)
    fig.tight_layout()
    save_figure(fig, output / "07-оптимальний-план-та-порівняння.png")

    lines = [
        "ЛАБОРАТОРНА РОБОТА № 5 — ЗАДАЧА КОМІВОЯЖЕРА",
        "=" * 66,
        f"Варіант: {VARIANT}",
        f"Сумарна потреба: {DEMANDS.sum()} кг",
        f"Вантажопідйомність: {CAPACITY} кг",
        f"Кількість маршрутів: ceil({DEMANDS.sum()}/{CAPACITY}) = {ceil(DEMANDS.sum()/CAPACITY)}",
        "",
        f"Мінімальне дерево: {sum(edge[2] for edge in minimum_tree_edges()):.1f}",
        f"Маршрути за деревом: {tree_plan.total_length:.1f}",
        f"Метод Свіра:         {sweep.total_length:.1f}",
        f"Точний розв'язок:    {exact.total_length:.1f}",
        "",
        "ТОЧНІ МАРШРУТИ:",
    ]
    for index, (route, load, length) in enumerate(zip(exact.routes, exact.loads, exact.lengths), 1):
        text_route = "C–" + "–".join(map(str, route)) + "–C"
        lines.append(f"{index}. {text_route:<22} Q={load:>3} кг   L={length:>5.1f}")
    fig, ax = plt.subplots(figsize=(13, 8))
    ax.axis("off")
    ax.text(0.04, 0.96, "\n".join(lines).replace(".", ","), family="DejaVu Sans Mono",
            fontsize=14, va="top", transform=ax.transAxes)
    save_figure(fig, output / "08-результат-програми.png")


def main() -> None:
    setup_style()
    adjacency = build_adjacency()
    distance, next_node = floyd_warshall(adjacency)
    tree_plan = minimum_tree_plan(distance)
    sweep = sweep_plan(distance)
    exact = exact_cvrp(distance)
    output = Path(__file__).resolve().parents[1] / "assets" / "screenshots"
    create_figures(distance, next_node, tree_plan, sweep, exact, output)

    print(f"Варіант: {VARIANT}")
    print(f"Сумарна потреба: {DEMANDS.sum()} кг")
    print(f"Вантажопідйомність: {CAPACITY} кг")
    print(f"Кількість маршрутів: {ceil(DEMANDS.sum() / CAPACITY)}")
    print(f"Довжина мінімального дерева: {sum(edge[2] for edge in minimum_tree_edges()):.1f}")
    for plan in (tree_plan, sweep, exact):
        print(f"\n{plan.name}: {plan.total_length:.1f}")
        for route, load, length in zip(plan.routes, plan.loads, plan.lengths):
            print("  C–" + "–".join(map(str, route)) + f"–C; Q={load}; L={length:.1f}")


if __name__ == "__main__":
    main()
