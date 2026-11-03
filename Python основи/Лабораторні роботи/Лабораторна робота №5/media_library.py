"""Лабораторна робота №5: бібліотека медіа (варіант 8 → 1)."""

from __future__ import annotations

from abc import ABC, abstractmethod
from collections.abc import Iterator


class MediaItem(ABC):
    """Абстрактний базовий клас для всіх елементів медіатеки."""

    def __init__(self, title: str, year: int) -> None:
        self.title = title
        self.year = year

    @property
    def title(self) -> str:
        """Повернути назву медіаелемента."""
        return self.__title

    @title.setter
    def title(self, value: str) -> None:
        cleaned = value.strip()
        if not cleaned:
            raise ValueError("Назва не може бути порожньою.")
        self.__title = cleaned

    @property
    def year(self) -> int:
        """Повернути рік видання."""
        return self.__year

    @year.setter
    def year(self, value: int) -> None:
        if isinstance(value, bool) or not isinstance(value, int):
            raise TypeError("Рік повинен бути цілим числом.")
        if not 1 <= value <= 2100:
            raise ValueError("Рік повинен бути в межах від 1 до 2100.")
        self.__year = value

    @property
    @abstractmethod
    def media_type(self) -> str:
        """Повернути назву типу медіаелемента."""

    @abstractmethod
    def details(self) -> str:
        """Повернути специфічні для підкласу відомості."""

    def describe(self) -> str:
        """Сформувати поліморфний опис елемента."""
        return f"{self.media_type}: «{self.title}» ({self.year}) — {self.details()}"

    def __str__(self) -> str:
        return self.describe()


class Book(MediaItem):
    """Книга з автором і кількістю сторінок."""

    def __init__(self, title: str, year: int, author: str, pages: int) -> None:
        super().__init__(title, year)
        cleaned_author = author.strip()
        if not cleaned_author:
            raise ValueError("Ім'я автора не може бути порожнім.")
        if isinstance(pages, bool) or not isinstance(pages, int) or pages <= 0:
            raise ValueError("Кількість сторінок повинна бути додатним цілим числом.")
        self.__author = cleaned_author
        self.__pages = pages

    @property
    def media_type(self) -> str:
        return "Книга"

    def details(self) -> str:
        return f"автор: {self.__author}; {self.__pages} с."


class DVD(MediaItem):
    """DVD-диск із режисером і тривалістю відтворення."""

    def __init__(self, title: str, year: int, director: str, duration: int) -> None:
        super().__init__(title, year)
        cleaned_director = director.strip()
        if not cleaned_director:
            raise ValueError("Ім'я режисера не може бути порожнім.")
        if isinstance(duration, bool) or not isinstance(duration, int) or duration <= 0:
            raise ValueError("Тривалість повинна бути додатним цілим числом.")
        self.__director = cleaned_director
        self.__duration = duration

    @property
    def media_type(self) -> str:
        return "DVD"

    def details(self) -> str:
        return f"режисер: {self.__director}; {self.__duration} хв"


class Magazine(MediaItem):
    """Журнал із номером випуску."""

    def __init__(self, title: str, year: int, issue: int) -> None:
        super().__init__(title, year)
        if isinstance(issue, bool) or not isinstance(issue, int) or issue <= 0:
            raise ValueError("Номер випуску повинен бути додатним цілим числом.")
        self.__issue = issue

    @property
    def media_type(self) -> str:
        return "Журнал"

    def details(self) -> str:
        return f"випуск №{self.__issue}"


class Library:
    """Ітерована колекція медіаелементів."""

    def __init__(self, name: str) -> None:
        cleaned_name = name.strip()
        if not cleaned_name:
            raise ValueError("Назва бібліотеки не може бути порожньою.")
        self.__name = cleaned_name
        self.__items: list[MediaItem] = []

    @property
    def name(self) -> str:
        return self.__name

    def add(self, item: MediaItem) -> None:
        """Додати елемент до бібліотеки."""
        if not isinstance(item, MediaItem):
            raise TypeError("До бібліотеки можна додавати лише медіаелементи.")
        self.__items.append(item)

    def find_by_title(self, query: str) -> list[MediaItem]:
        """Знайти елементи, у назві яких є заданий фрагмент."""
        normalized_query = query.strip().casefold()
        if not normalized_query:
            return []
        return [item for item in self.__items if normalized_query in item.title.casefold()]

    def __iter__(self) -> Iterator[MediaItem]:
        """Створити незалежний ітератор для послідовного обходу бібліотеки."""
        return iter(self.__items.copy())

    def __len__(self) -> int:
        return len(self.__items)


def main() -> None:
    """Продемонструвати успадкування, поліморфізм та ітерацію."""
    library = Library("Навчальна медіатека")
    library.add(Book("Кобзар", 1840, "Тарас Шевченко", 352))
    library.add(DVD("Земля", 1930, "Олександр Довженко", 75))
    library.add(Magazine("Куншт", 2026, 3))

    print("Лабораторна робота №5. Варіант 8 -> 1.")
    print(f"{library.name}: {len(library)} елементи\n")
    print("Поліморфний обхід бібліотеки:")
    for number, item in enumerate(library, start=1):
        print(f"{number}. {item}")

    print("\nПошук за словом «земля»:")
    for item in library.find_by_title("земля"):
        print(item)


if __name__ == "__main__":
    main()
