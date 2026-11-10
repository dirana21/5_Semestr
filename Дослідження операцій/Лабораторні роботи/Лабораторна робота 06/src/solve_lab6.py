"""Лабораторна робота № 6: оптимальне положення об'єкта.

Програма знаходить початкове положення складу як геометричну медіану,
уточнює його методом умовного центру мас, обчислює відстані до всіх
споживачів і створює ілюстрації для звіту.
"""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np


CONSUMER_NAMES = [f"C{i}" for i in range(1, 11)]
X = np.array([4, 10, 2, 3, 6, 7, 2, 8, 5, 8], dtype=float)
Y = np.array([9, 1, 7, 3, 4, 7, 2, 5, 2, 4], dtype=float)
Q = np.array([1, 3, 5, 5, 5, 2, 3, 4, 5, 2], dtype=float)
POINTS = np.column_stack((X, Y))


@dataclass(frozen=True)
class WarehouseResult:
    initial: np.ndarray
    center_of_mass: np.ndarray
    initial_distances: np.ndarray
    center_distances: np.ndarray
    iterations: tuple[np.ndarray, ...]


def sum_distances(position: np.ndarray) -> float:
    return float(np.linalg.norm(POINTS - position, axis=1).sum())


def weighted_squared_criterion(position: np.ndarray) -> float:
    squared_distances = np.sum((POINTS - position) ** 2, axis=1)
    return float(np.sum(Q * squared_distances))


def geometric_median(tolerance: float = 1e-12, max_iterations: int = 10_000) -> tuple[np.ndarray, tuple[np.ndarray, ...]]:
    """Метод Вайсфельда з перевіркою оптимуму у вузловій точці."""
    position = POINTS.mean(axis=0)
    history = [position.copy()]
    for _ in range(max_iterations):
        distances = np.linalg.norm(POINTS - position, axis=1)
        coincident = np.flatnonzero(distances < tolerance)
        if coincident.size:
            candidate = POINTS[coincident[0]]
            other = np.delete(POINTS, coincident[0], axis=0)
            directions = (other - candidate) / np.linalg.norm(other - candidate, axis=1)[:, None]
            if np.linalg.norm(directions.sum(axis=0)) <= 1 + tolerance:
                position = candidate.copy()
                history.append(position.copy())
                break
        safe = np.maximum(distances, tolerance)
        updated = np.sum(POINTS / safe[:, None], axis=0) / np.sum(1 / safe)
        history.append(updated.copy())
        if np.linalg.norm(updated - position) < tolerance:
            position = updated
            break
        position = updated

    # Для цього набору точок геометрична медіана збігається зі споживачем C5.
    # Перевіряємо всі вузли, щоб коректно зафіксувати такий невироджений випадок.
    node_values = np.array([sum_distances(point) for point in POINTS])
    best_node = POINTS[int(np.argmin(node_values))]
    if sum_distances(best_node) <= sum_distances(position) + 1e-9:
        position = best_node.copy()
        if np.linalg.norm(history[-1] - position) > tolerance:
            history.append(position.copy())
    return position, tuple(history)


def conditional_center_of_mass() -> np.ndarray:
    return np.array([np.sum(X * Q) / np.sum(Q), np.sum(Y * Q) / np.sum(Q)])


def solve() -> WarehouseResult:
    initial, history = geometric_median()
    center = conditional_center_of_mass()
    return WarehouseResult(
        initial=initial,
        center_of_mass=center,
        initial_distances=np.linalg.norm(POINTS - initial, axis=1),
        center_distances=np.linalg.norm(POINTS - center, axis=1),
        iterations=history,
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


def draw_consumers(ax: plt.Axes, scale_by_demand: bool = False) -> None:
    sizes = 260 + 90 * Q if scale_by_demand else np.full(10, 420)
    ax.scatter(X, Y, s=sizes, color="#2563eb", edgecolor="white", linewidth=1.5, zorder=3)
    for index, (x, y, demand) in enumerate(zip(X, Y, Q), 1):
        label = f"{index}\n{int(demand)} т" if scale_by_demand else str(index)
        ax.text(x, y, label, ha="center", va="center", color="white", fontsize=10, weight="bold", zorder=4)
    ax.set_xlim(0.5, 10.8)
    ax.set_ylim(0.3, 10.3)
    ax.set_xticks(range(1, 11))
    ax.set_yticks(range(1, 11))
    ax.set_xlabel("Координата X")
    ax.set_ylabel("Координата Y")
    ax.grid(alpha=0.22)
    ax.set_aspect("equal")


def create_figures(result: WarehouseResult, output: Path) -> None:
    output.mkdir(parents=True, exist_ok=True)

    fig, ax = plt.subplots(figsize=(12, 8))
    ax.axis("off")
    rows = [[name, f"{int(x)}", f"{int(y)}", f"{int(q)}"] for name, x, y, q in zip(CONSUMER_NAMES, X, Y, Q)]
    table = ax.table(
        cellText=rows,
        colLabels=["Споживач", "X", "Y", "Потреба Q, т"],
        cellLoc="center",
        loc="center",
        bbox=[0.14, 0.08, 0.72, 0.82],
    )
    table.auto_set_font_size(False)
    table.set_fontsize(14)
    for (row, _), cell in table.get_celld().items():
        cell.set_facecolor("#dbeafe" if row == 0 else ("#f8fafc" if row % 2 else "#eff6ff"))
    ax.text(0.5, 0.025, f"Сумарна потреба: ΣQ = {int(Q.sum())} т", ha="center", weight="bold", transform=ax.transAxes)
    ax.set_title("Координати та потреби споживачів", pad=20)
    save_figure(fig, output / "01-вихідні-дані.png")

    grid_x = np.linspace(0.5, 10.5, 220)
    grid_y = np.linspace(0.5, 10.0, 220)
    xx, yy = np.meshgrid(grid_x, grid_y)
    rr = np.zeros_like(xx)
    for x, y in POINTS:
        rr += np.sqrt((xx - x) ** 2 + (yy - y) ** 2)

    fig, ax = plt.subplots(figsize=(12, 9))
    contour = ax.contourf(xx, yy, rr, levels=28, cmap="viridis")
    lines = ax.contour(xx, yy, rr, levels=14, colors="white", linewidths=0.55, alpha=0.65)
    ax.clabel(lines, inline=True, fontsize=8, fmt="%.1f")
    draw_consumers(ax)
    ax.scatter(*result.initial, s=650, marker="*", color="#ef4444", edgecolor="white", linewidth=1.3,
               label=f"Початковий склад ({result.initial[0]:.1f}; {result.initial[1]:.1f})", zorder=5)
    ax.legend(loc="upper right")
    ax.set_title("Пошук початкового положення складу: R(x, y) → min")
    fig.colorbar(contour, ax=ax, shrink=0.85, label="Сума відстаней R(x, y)")
    fig.tight_layout()
    save_figure(fig, output / "02-контури-суми-відстаней.png")

    fig = plt.figure(figsize=(13, 9))
    ax = fig.add_subplot(111, projection="3d")
    ax.plot_surface(xx, yy, rr, cmap="viridis", alpha=0.88, linewidth=0, antialiased=True)
    minimum_z = sum_distances(result.initial)
    ax.scatter(result.initial[0], result.initial[1], minimum_z, color="#ef4444", s=120, marker="*", depthshade=False)
    ax.text2D(0.68, 0.16, f"S₀ = (6,0; 4,0)\nRmin = {minimum_z:.3f}".replace(".", ","),
              transform=ax.transAxes, color="#991b1b",
              bbox={"boxstyle": "round,pad=0.35", "fc": "white", "ec": "#fecaca", "alpha": 0.92})
    ax.set_xlabel("X")
    ax.set_ylabel("Y")
    ax.set_zlabel("R(x, y)")
    ax.set_title("Поверхня критерію суми відстаней")
    ax.view_init(elev=30, azim=-55)
    fig.tight_layout()
    save_figure(fig, output / "03-поверхня-критерію.png")

    fig, ax = plt.subplots(figsize=(12, 9))
    draw_consumers(ax, scale_by_demand=True)
    for point, demand in zip(POINTS, Q):
        ax.plot([result.center_of_mass[0], point[0]], [result.center_of_mass[1], point[1]],
                color="#94a3b8", linewidth=0.7 + 0.45 * demand, alpha=0.52, zorder=1)
    ax.scatter(*result.center_of_mass, s=760, marker="P", color="#16a34a", edgecolor="white", linewidth=1.5,
               label=f"Центр мас ({result.center_of_mass[0]:.1f}; {result.center_of_mass[1]:.1f})", zorder=6)
    ax.legend(loc="upper right")
    ax.set_title("Уточнення положення складу методом умовного центру мас")
    fig.tight_layout()
    save_figure(fig, output / "04-умовний-центр-мас.png")

    fig, ax = plt.subplots(figsize=(12, 9))
    draw_consumers(ax, scale_by_demand=True)
    ax.scatter(*result.initial, s=700, marker="*", color="#ef4444", edgecolor="white", linewidth=1.4,
               label="Початкове положення S₀ = (6,0; 4,0)", zorder=6)
    ax.scatter(*result.center_of_mass, s=650, marker="P", color="#16a34a", edgecolor="white", linewidth=1.4,
               label="Уточнене положення S₁ = (5,2; 4,0)", zorder=6)
    ax.annotate("", xy=result.center_of_mass, xytext=result.initial,
                arrowprops={"arrowstyle": "<->", "color": "#0f172a", "lw": 2})
    ax.text(np.mean([result.initial[0], result.center_of_mass[0]]), 4.48, "зміщення 0,8",
            ha="center", va="bottom", fontsize=13,
            bbox={"boxstyle": "round,pad=0.22", "fc": "white", "ec": "#cbd5e1", "alpha": 0.92})
    ax.legend(loc="upper right")
    ax.set_title("Порівняння початкового та уточненого положень складу")
    fig.tight_layout()
    save_figure(fig, output / "05-порівняння-положень.png")

    indices = np.arange(1, 11)
    width = 0.38
    fig, ax = plt.subplots(figsize=(15, 8))
    bars_initial = ax.bar(indices - width / 2, result.initial_distances, width, label="Початкове S₀", color="#ef4444")
    bars_center = ax.bar(indices + width / 2, result.center_distances, width, label="Уточнене S₁", color="#16a34a")
    ax.bar_label(bars_initial, fmt="%.2f", padding=3, fontsize=9)
    ax.bar_label(bars_center, fmt="%.2f", padding=3, fontsize=9)
    ax.set_xticks(indices, CONSUMER_NAMES)
    ax.set_xlabel("Споживач")
    ax.set_ylabel("Відстань")
    ax.set_title("Відстані від двох положень складу до споживачів")
    ax.legend()
    ax.grid(axis="y", alpha=0.25)
    ax.set_ylim(0, max(result.initial_distances.max(), result.center_distances.max()) * 1.22)
    fig.tight_layout()
    save_figure(fig, output / "06-відстані-до-споживачів.png")

    sum_values = [sum_distances(result.initial), sum_distances(result.center_of_mass)]
    weighted_values = [weighted_squared_criterion(result.initial), weighted_squared_criterion(result.center_of_mass)]
    fig, axes = plt.subplots(1, 2, figsize=(15, 7), constrained_layout=True)
    bars = axes[0].bar(["S₀", "S₁"], sum_values, color=["#ef4444", "#16a34a"])
    axes[0].bar_label(bars, labels=[f"{value:.3f}".replace(".", ",") for value in sum_values], padding=5)
    axes[0].set_title("Сума звичайних відстаней")
    axes[0].set_ylabel("Σdᵢ")
    axes[0].set_ylim(0, max(sum_values) * 1.18)
    axes[0].grid(axis="y", alpha=0.2)
    bars = axes[1].bar(["S₀", "S₁"], weighted_values, color=["#ef4444", "#16a34a"])
    axes[1].bar_label(bars, labels=[f"{value:.1f}".replace(".", ",") for value in weighted_values], padding=5)
    axes[1].set_title("Зважена сума квадратів відстаней")
    axes[1].set_ylabel("ΣQᵢdᵢ²")
    axes[1].set_ylim(0, max(weighted_values) * 1.18)
    axes[1].grid(axis="y", alpha=0.2)
    fig.suptitle("Перевірка критеріїв оптимальності", fontsize=20)
    save_figure(fig, output / "07-порівняння-критеріїв.png")

    lines = [
        "ЛАБОРАТОРНА РОБОТА № 6 — ОПТИМАЛЬНЕ ПОЛОЖЕННЯ ОБ'ЄКТА",
        "=" * 72,
        f"Кількість споживачів: {len(POINTS)}",
        f"Сумарна потреба: {int(Q.sum())} т",
        "",
        f"Початкове положення: S₀ = ({result.initial[0]:.3f}; {result.initial[1]:.3f})",
        f"Мінімальна сума відстаней: {sum_distances(result.initial):.6f}",
        "",
        f"Уточнене положення: S₁ = ({result.center_of_mass[0]:.3f}; {result.center_of_mass[1]:.3f})",
        f"Зважений квадратичний критерій: {weighted_squared_criterion(result.center_of_mass):.3f}",
        "",
        "ВІДСТАНІ ВІД УТОЧНЕНОГО СКЛАДУ:",
    ]
    lines.extend(f"C{index:>2}: {distance:.6f}" for index, distance in enumerate(result.center_distances, 1))
    fig, ax = plt.subplots(figsize=(13, 9))
    ax.axis("off")
    ax.text(0.04, 0.96, "\n".join(lines).replace(".", ","), family="DejaVu Sans Mono",
            fontsize=13.5, va="top", transform=ax.transAxes)
    save_figure(fig, output / "08-результат-програми.png")


def main() -> None:
    setup_style()
    result = solve()
    output = Path(__file__).resolve().parents[1] / "assets" / "screenshots"
    create_figures(result, output)

    print("Початкове положення складу:", result.initial)
    print("Сума відстаней:", sum_distances(result.initial))
    print("Уточнене положення складу:", result.center_of_mass)
    print("Зважений квадратичний критерій:", weighted_squared_criterion(result.center_of_mass))
    print("Відстані від уточненого складу:")
    print(result.center_distances)


if __name__ == "__main__":
    main()
