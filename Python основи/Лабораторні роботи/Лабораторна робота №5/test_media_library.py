"""Автоматичні тести медіатеки з лабораторної роботи №5."""

import unittest

from media_library import Book, DVD, Library, Magazine, MediaItem


class MediaLibraryTests(unittest.TestCase):
    def setUp(self) -> None:
        self.book = Book("Кобзар", 1840, "Тарас Шевченко", 352)
        self.dvd = DVD("Земля", 1930, "Олександр Довженко", 75)
        self.magazine = Magazine("Куншт", 2026, 3)

    def test_subclasses_inherit_media_item(self) -> None:
        for item in (self.book, self.dvd, self.magazine):
            self.assertIsInstance(item, MediaItem)

    def test_book_polymorphic_description(self) -> None:
        self.assertEqual(
            str(self.book),
            "Книга: «Кобзар» (1840) — автор: Тарас Шевченко; 352 с.",
        )

    def test_dvd_polymorphic_description(self) -> None:
        self.assertIn("режисер: Олександр Довженко; 75 хв", self.dvd.describe())

    def test_magazine_polymorphic_description(self) -> None:
        self.assertTrue(self.magazine.describe().endswith("випуск №3"))

    def test_library_add_and_length(self) -> None:
        library = Library("Медіатека")
        library.add(self.book)
        library.add(self.dvd)
        self.assertEqual(len(library), 2)

    def test_library_is_iterable_in_insertion_order(self) -> None:
        library = Library("Медіатека")
        for item in (self.book, self.dvd, self.magazine):
            library.add(item)
        self.assertEqual([item.title for item in library], ["Кобзар", "Земля", "Куншт"])

    def test_two_iterators_are_independent(self) -> None:
        library = Library("Медіатека")
        library.add(self.book)
        library.add(self.dvd)
        first_iterator = iter(library)
        second_iterator = iter(library)
        self.assertIs(next(first_iterator), self.book)
        self.assertIs(next(second_iterator), self.book)

    def test_find_by_title_is_case_insensitive(self) -> None:
        library = Library("Медіатека")
        library.add(self.dvd)
        self.assertEqual(library.find_by_title("ЗЕМЛЯ"), [self.dvd])

    def test_empty_search_returns_empty_list(self) -> None:
        library = Library("Медіатека")
        library.add(self.book)
        self.assertEqual(library.find_by_title("   "), [])

    def test_title_property_validates_empty_value(self) -> None:
        with self.assertRaises(ValueError):
            self.book.title = "   "

    def test_invalid_year_is_rejected(self) -> None:
        with self.assertRaises(ValueError):
            Magazine("Журнал", 0, 1)

    def test_invalid_specific_values_are_rejected(self) -> None:
        with self.assertRaises(ValueError):
            Book("Книга", 2026, "Автор", 0)
        with self.assertRaises(ValueError):
            DVD("Фільм", 2026, "Режисер", -1)

    def test_library_rejects_non_media_objects(self) -> None:
        library = Library("Медіатека")
        with self.assertRaises(TypeError):
            library.add("не медіа")  # type: ignore[arg-type]


if __name__ == "__main__":
    unittest.main(verbosity=2)
