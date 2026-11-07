"""Лабораторна робота №6: тимчасова конфігурація (варіант 8 -> 1)."""

from __future__ import annotations

from collections.abc import Iterator, Mapping
from typing import Any


class ConfigurationError(Exception):
    """Базовий виняток для помилок конфігурації."""


class UnknownConfigKeyError(ConfigurationError):
    """Виникає під час спроби змінити невідому настройку."""


class InvalidConfigValueError(ConfigurationError):
    """Виникає, якщо значення настройки має неправильний тип."""


class ApplicationConfig:
    """Інкапсульоване сховище параметрів програми."""

    def __init__(self, **values: Any) -> None:
        if not values:
            raise ValueError("Конфігурація повинна містити хоча б один параметр.")
        self.__values = dict(values)
        self.__types = {key: type(value) for key, value in values.items()}

    def __getitem__(self, key: str) -> Any:
        try:
            return self.__values[key]
        except KeyError as error:
            raise UnknownConfigKeyError(f"Невідомий параметр: {key}") from error

    def __iter__(self) -> Iterator[str]:
        return iter(self.__values.copy())

    def __len__(self) -> int:
        return len(self.__values)

    def as_dict(self) -> dict[str, Any]:
        """Повернути незалежну копію поточних параметрів."""
        return self.__values.copy()

    def update(self, values: Mapping[str, Any]) -> None:
        """Перевірити та застосувати набір параметрів атомарно."""
        checked: dict[str, Any] = {}
        for key, value in values.items():
            if key not in self.__values:
                raise UnknownConfigKeyError(f"Невідомий параметр: {key}")
            expected_type = self.__types[key]
            if type(value) is not expected_type:
                raise InvalidConfigValueError(
                    f"Параметр '{key}' очікує {expected_type.__name__}, "
                    f"отримано {type(value).__name__}."
                )
            checked[key] = value
        self.__values.update(checked)

    def _restore(self, snapshot: Mapping[str, Any]) -> None:
        """Відновити перевірений внутрішній знімок конфігурації."""
        self.__values = dict(snapshot)

    def __str__(self) -> str:
        pairs = ", ".join(f"{key}={value!r}" for key, value in self.__values.items())
        return f"ApplicationConfig({pairs})"


class ConfigContext:
    """Тимчасово змінює конфігурацію та завжди відновлює її стан."""

    def __init__(self, config: ApplicationConfig, **overrides: Any) -> None:
        if not isinstance(config, ApplicationConfig):
            raise TypeError("config повинен бути об'єктом ApplicationConfig.")
        if not overrides:
            raise ValueError("Потрібно передати хоча б одну тимчасову настройку.")
        self.__config = config
        self.__overrides = overrides
        self.__snapshot: dict[str, Any] | None = None

    def __enter__(self) -> ApplicationConfig:
        self.__snapshot = self.__config.as_dict()
        try:
            self.__config.update(self.__overrides)
        except Exception:
            self.__snapshot = None
            raise
        return self.__config

    def __exit__(self, exc_type: object, exc_value: object, traceback: object) -> bool:
        if self.__snapshot is not None:
            self.__config._restore(self.__snapshot)
            self.__snapshot = None
        return False


def main() -> None:
    """Продемонструвати нормальний вихід, виняток і власну помилку."""
    config = ApplicationConfig(debug=False, timeout=30, theme="light")

    print("Лабораторна робота №6. Варіант 8 -> 1.")
    print(f"Початкові настройки: {config}")

    with ConfigContext(config, debug=True, timeout=5, theme="dark") as temporary:
        print(f"Усередині ConfigContext: {temporary}")

    print(f"Після звичайного виходу: {config}")

    try:
        with ConfigContext(config, debug=True):
            print(f"Перед винятком: {config}")
            raise RuntimeError("імітація помилки програми")
    except RuntimeError as error:
        print(f"Перехоплено виняток: {error}")

    print(f"Після винятку: {config}")

    try:
        with ConfigContext(config, unknown="value"):
            pass
    except UnknownConfigKeyError as error:
        print(f"Власний виняток: {error}")


if __name__ == "__main__":
    main()
