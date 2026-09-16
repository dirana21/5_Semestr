"""Лабораторна робота №1: графічний розв'язок двовимірної ЗЛП.

Варіант N=12, коефіцієнт k=0.5.
Скрипт обчислює неперервний та цілочисельний плани й відтворює
всі ілюстрації, наведені у звіті.
"""

from __future__ import annotations

from dataclasses import dataclass
from fractions import Fraction
from pathlib import Path

import matplotlib.pyplot as plt
from matplotlib.ticker import MultipleLocator


BASE_DIR = Path(__file__).resolve().parents[1]
OUTPUT_DIR = BASE_DIR / "assets" / "screenshots"


@dataclass(frozen=True)
class Problem:
    n: int
    k: Fraction
    material_limit: Fraction = Fraction(1700)
    time_limit: Fraction = Fraction(1600)

    @property
    def sa(self) -> Fraction:
        return Fraction(1, 2) * self.n * self.k

    @property
    def ta(self) -> Fraction:
        return Fraction(self.n) / self.k

    @property
    def sb(self) -> Fraction:
        return Fraction(self.n)

    @property
    def tb(self) -> Fraction:
        return Fraction(2, 5) * self.n * self.k

    @property
    def wa(self) -> Fraction:
        return Fraction(self.n) * self.k

    @property
    def wb(self) -> Fraction:
        return Fraction(6, 5) * self.n * self.k


Point = tuple[Fraction, Fraction]


def objective(problem: Problem, point: Point) -> Fraction:
    x_a, x_b = point
    return problem.wa * x_a + problem.wb * x_b


def continuous_vertices(problem: Problem) -> list[Point]:
    """Повертає вершини допустимого багатокутника проти годинника."""
    x_axis = min(
        problem.material_limit / problem.sa,
        problem.time_limit / problem.ta,
    )
    y_axis = min(
        problem.material_limit / problem.sb,
        problem.time_limit / problem.tb,
    )

    determinant = problem.sa * problem.tb - problem.sb * problem.ta
    intersection_a = (
        problem.material_limit * problem.tb
        - problem.sb * problem.time_limit
    ) / determinant
    intersection_b = (
        problem.sa * problem.time_limit
        - problem.material_limit * problem.ta
    ) / determinant

    return [
        (Fraction(0), Fraction(0)),
        (x_axis, Fraction(0)),
        (intersection_a, intersection_b),
        (Fraction(0), y_axis),
    ]


def integer_optimum(problem: Problem) -> tuple[Point, Fraction]:
    """Повний перебір цілих невід'ємних виробничих планів."""
    best_point = (Fraction(0), Fraction(0))
    best_value = Fraction(0)
    max_a = int(problem.time_limit / problem.ta)
    max_b = int(problem.material_limit / problem.sb)

    for x_a in range(max_a + 1):
        for x_b in range(max_b + 1):
            point = (Fraction(x_a), Fraction(x_b))
            material = problem.sa * x_a + problem.sb * x_b
            time = problem.ta * x_a + problem.tb * x_b
            value = objective(problem, point)
            if (
                material <= problem.material_limit
                and time <= problem.time_limit
                and value > best_value
            ):
                best_point, best_value = point, value

    return best_point, best_value


def fmt(value: Fraction, digits: int = 3) -> str:
    number = float(value)
    if value.denominator == 1:
        return str(value.numerator)
    return f"{number:.{digits}f}".rstrip("0").rstrip(".").replace(".", ",")


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


def save_input_table(problem: Problem) -> None:
    fig, ax = plt.subplots(figsize=(11.2, 3.2))
    ax.axis("off")
    columns = ["Показник", "Формула", "Підстановка", "Значення"]
    rows = [
        ["Сировина A, Sₐ", "0,5·N·k", "0,5·12·0,5", fmt(problem.sa)],
        ["Машинний час A, Tₐ", "N/k", "12/0,5", fmt(problem.ta)],
        ["Сировина B, Sᵦ", "N", "12", fmt(problem.sb)],
        ["Машинний час B, Tᵦ", "0,4·N·k", "0,4·12·0,5", fmt(problem.tb)],
        ["Прибуток A, Wₐ", "N·k", "12·0,5", fmt(problem.wa)],
        ["Прибуток B, Wᵦ", "1,2·N·k", "1,2·12·0,5", fmt(problem.wb)],
    ]
    table = ax.table(
        cellText=rows,
        colLabels=columns,
        cellLoc="center",
        colLoc="center",
        loc="center",
        colWidths=[0.29, 0.21, 0.25, 0.18],
    )
    table.auto_set_font_size(False)
    table.set_fontsize(10.5)
    table.scale(1, 1.48)
    for (row, _), cell in table.get_celld().items():
        cell.set_edgecolor("#cbd5e1")
        if row == 0:
            cell.set_facecolor("#0f766e")
            cell.set_text_props(color="white", weight="bold")
        elif row % 2 == 0:
            cell.set_facecolor("#f0fdfa")
    ax.set_title("Вихідні дані варіанта N = 12, k = 0,5", weight="bold", pad=14)
    fig.savefig(OUTPUT_DIR / "01-вихідні-дані.png")
    plt.close(fig)


def plot_base(problem: Problem, title: str):
    fig, ax = plt.subplots(figsize=(10.5, 7.1))
    xs = [value / 2 for value in range(0, 361)]
    material_y = [
        float((problem.material_limit - problem.sa * Fraction(str(x))) / problem.sb)
        for x in xs
    ]
    time_y = [
        float((problem.time_limit - problem.ta * Fraction(str(x))) / problem.tb)
        for x in xs
    ]
    ax.plot(xs, material_y, color="#2563eb", lw=2.3, label="3xₐ + 12xᵦ = 1700")
    ax.plot(xs, time_y, color="#dc2626", lw=2.3, label="24xₐ + 2,4xᵦ = 1600")

    vertices = continuous_vertices(problem)
    polygon = [(float(x), float(y)) for x, y in vertices]
    ax.fill(
        [point[0] for point in polygon],
        [point[1] for point in polygon],
        color="#14b8a6",
        alpha=0.24,
        label="Область допустимих розв'язків",
        zorder=1,
    )
    ax.plot(
        [point[0] for point in polygon] + [polygon[0][0]],
        [point[1] for point in polygon] + [polygon[0][1]],
        color="#0f766e",
        lw=1.6,
        zorder=2,
    )
    for index, (x, y) in enumerate(vertices):
        ax.scatter(float(x), float(y), s=48, color="#0f172a", zorder=5)
        offset = (6, 7) if index != 2 else (7, -18)
        ax.annotate(
            f"P{index} ({fmt(x, digits=2)}; {fmt(y, digits=2)})",
            (float(x), float(y)),
            xytext=offset,
            textcoords="offset points",
            fontsize=9.5,
            weight="semibold",
        )

    optimum = max(vertices, key=lambda point: objective(problem, point))
    ax.scatter(
        float(optimum[0]),
        float(optimum[1]),
        marker="*",
        s=300,
        color="#f59e0b",
        edgecolor="#92400e",
        linewidth=1.1,
        label="Оптимальна точка",
        zorder=7,
    )
    ax.set_xlim(0, 180)
    ax.set_ylim(0, 180)
    ax.xaxis.set_major_locator(MultipleLocator(20))
    ax.yaxis.set_major_locator(MultipleLocator(20))
    ax.set_xlabel("Кількість столів моделі A, xₐ")
    ax.set_ylabel("Кількість столів моделі B, xᵦ")
    ax.set_title(title, weight="bold", pad=12)
    ax.spines[["top", "right"]].set_visible(False)
    return fig, ax, optimum


def save_feasible_region(problem: Problem) -> None:
    fig, ax, _ = plot_base(problem, "Графічне визначення області допустимих розв'язків")
    ax.legend(loc="upper right", framealpha=0.95)
    fig.tight_layout()
    fig.savefig(OUTPUT_DIR / "02-область-допустимих-розв'язків.png")
    plt.close(fig)


def save_objective_plot(problem: Problem) -> None:
    fig, ax, optimum = plot_base(problem, "Пошук максимуму цільової функції")
    optimum_value = objective(problem, optimum)
    xs = [value / 2 for value in range(0, 361)]
    objective_y = [
        float((optimum_value - problem.wa * Fraction(str(x))) / problem.wb)
        for x in xs
    ]
    ax.plot(
        xs,
        objective_y,
        color="#7c3aed",
        lw=2.2,
        linestyle="--",
        label=f"F = {fmt(optimum_value, digits=2)}",
    )
    ax.annotate(
        "напрям зростання F",
        xy=(130, 58),
        xytext=(105, 28),
        arrowprops=dict(arrowstyle="-|>", color="#7c3aed", lw=2),
        color="#6d28d9",
        weight="bold",
    )
    ax.annotate(
        "max F",
        xy=(float(optimum[0]), float(optimum[1])),
        xytext=(78, 151),
        arrowprops=dict(arrowstyle="->", color="#92400e", lw=1.8),
        color="#92400e",
        fontsize=12,
        weight="bold",
    )
    ax.legend(loc="upper right", framealpha=0.95)
    fig.tight_layout()
    fig.savefig(OUTPUT_DIR / "03-цільова-функція.png")
    plt.close(fig)


def save_vertex_table(problem: Problem) -> None:
    vertices = continuous_vertices(problem)
    fig, ax = plt.subplots(figsize=(10.2, 3.5))
    ax.axis("off")
    rows = []
    for index, point in enumerate(vertices):
        rows.append(
            [
                f"P{index}",
                fmt(point[0]),
                fmt(point[1]),
                fmt(objective(problem, point)),
                "оптимум" if objective(problem, point) == max(map(lambda p: objective(problem, p), vertices)) else "",
            ]
        )
    table = ax.table(
        cellText=rows,
        colLabels=["Вершина", "xₐ", "xᵦ", "F = 6xₐ + 7,2xᵦ", "Висновок"],
        cellLoc="center",
        colLoc="center",
        loc="center",
        colWidths=[0.14, 0.17, 0.17, 0.27, 0.17],
    )
    table.auto_set_font_size(False)
    table.set_fontsize(11)
    table.scale(1, 1.7)
    for (row, _), cell in table.get_celld().items():
        cell.set_edgecolor("#cbd5e1")
        if row == 0:
            cell.set_facecolor("#1d4ed8")
            cell.set_text_props(color="white", weight="bold")
        elif row == 3:
            cell.set_facecolor("#fef3c7")
            cell.set_text_props(weight="bold")
        elif row % 2 == 0:
            cell.set_facecolor("#eff6ff")
    ax.set_title("Перевірка цільової функції у вершинах", weight="bold", pad=12)
    fig.savefig(OUTPUT_DIR / "04-перевірка-вершин.png")
    plt.close(fig)


def result_lines(problem: Problem) -> list[str]:
    vertices = continuous_vertices(problem)
    optimum = max(vertices, key=lambda point: objective(problem, point))
    integer_point, integer_value = integer_optimum(problem)
    material_used = problem.sa * optimum[0] + problem.sb * optimum[1]
    time_used = problem.ta * optimum[0] + problem.tb * optimum[1]
    int_material = problem.sa * integer_point[0] + problem.sb * integer_point[1]
    int_time = problem.ta * integer_point[0] + problem.tb * integer_point[1]
    return [
        "Лабораторна робота №1 — результат обчислень",
        "Варіант: N = 12; k = 0,5",
        "",
        "Неперервний графічний розв'язок:",
        f"  x_A = {fmt(optimum[0])} ({optimum[0]})",
        f"  x_B = {fmt(optimum[1])} ({optimum[1]})",
        f"  F_max = {fmt(objective(problem, optimum))} ({objective(problem, optimum)})",
        f"  використано сировини = {fmt(material_used)} із {fmt(problem.material_limit)}",
        f"  використано часу     = {fmt(time_used)} із {fmt(problem.time_limit)}",
        f"  залишки               = {fmt(problem.material_limit - material_used)}; {fmt(problem.time_limit - time_used)}",
        "",
        "Практичний цілочисельний план:",
        f"  x_A = {fmt(integer_point[0])}; x_B = {fmt(integer_point[1])}",
        f"  F = {fmt(integer_value)}",
        f"  залишок сировини = {fmt(problem.material_limit - int_material)}",
        f"  залишок часу     = {fmt(problem.time_limit - int_time)}",
    ]


def save_console_output(problem: Problem) -> None:
    lines = result_lines(problem)
    fig, ax = plt.subplots(figsize=(11.5, 6.4))
    fig.patch.set_facecolor("#0f172a")
    ax.set_facecolor("#0f172a")
    ax.axis("off")
    ax.text(
        0.035,
        0.94,
        "\n".join(lines),
        va="top",
        ha="left",
        color="#e2e8f0",
        family="DejaVu Sans Mono",
        fontsize=11.5,
        linespacing=1.35,
        transform=ax.transAxes,
    )
    ax.text(
        0.035,
        0.985,
        "●  ●  ●",
        va="top",
        color="#64748b",
        fontsize=13,
        transform=ax.transAxes,
    )
    fig.savefig(OUTPUT_DIR / "05-результат-програми.png", facecolor=fig.get_facecolor())
    plt.close(fig)


def main() -> None:
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    setup_style()
    problem = Problem(n=12, k=Fraction(1, 2))
    save_input_table(problem)
    save_feasible_region(problem)
    save_objective_plot(problem)
    save_vertex_table(problem)
    save_console_output(problem)
    print("\n".join(result_lines(problem)))
    print(f"\nІлюстрації збережено у: {OUTPUT_DIR}")


if __name__ == "__main__":
    main()
