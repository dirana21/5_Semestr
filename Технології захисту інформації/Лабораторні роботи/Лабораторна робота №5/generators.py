"""Датчики і порівняння їхніх періодів для варіанта 12."""

from collections.abc import Callable, Hashable, Iterator


MODULUS = 4096
SEED = (4003, 59)


def additive_step(state: tuple[int, int]) -> tuple[int, int]:
    x, y = state
    return y, (x + y) % MODULUS


def cycle(start: Hashable, step: Callable) -> tuple[int, int]:
    """Повертає довжину передперіоду та довжину циклу."""
    seen = {}
    state = start
    while state not in seen:
        seen[state] = len(seen)
        state = step(state)
    return seen[state], len(seen) - seen[state]


def gamma_bytes() -> Iterator[int]:
    state = SEED
    while True:
        x, y = state
        # Два 12-бітові числа утворюють 24 біти без доповнення.
        yield x >> 4
        yield ((x & 15) << 4) | (y >> 8)
        yield y & 255
        state = additive_step(additive_step(state))


if __name__ == "__main__":
    for name, start, step in (
        ("Адитивний", SEED, additive_step),
        ("Лінійний конгруентний", 4003, lambda x: (5 * x + 7) % MODULUS),
        ("Мультиплікативний", 502, lambda x: (7 * x) % MODULUS),
    ):
        prefix, period = cycle(start, step)
        print(f"{name}: передперіод {prefix}, період {period}")
