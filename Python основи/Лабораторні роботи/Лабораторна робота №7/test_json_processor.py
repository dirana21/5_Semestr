"""Автоматичні тести обробки JSON із лабораторної роботи №7."""

import json
import tempfile
import unittest
from pathlib import Path

from json_processor import (
    JsonDataError,
    VARIANT_DATA,
    calculate_numbers_sum,
    load_json,
    process_variant,
    save_json,
)


class JsonProcessorTests(unittest.TestCase):
    def setUp(self) -> None:
        self.temp_directory = tempfile.TemporaryDirectory()
        self.file_path = Path(self.temp_directory.name) / "output.json"

    def tearDown(self) -> None:
        self.temp_directory.cleanup()

    def test_save_json_creates_file(self) -> None:
        save_json(VARIANT_DATA, self.file_path)
        self.assertTrue(self.file_path.exists())

    def test_saved_file_is_valid_json(self) -> None:
        save_json(VARIANT_DATA, self.file_path)
        parsed = json.loads(self.file_path.read_text(encoding="utf-8"))
        self.assertEqual(parsed, VARIANT_DATA)

    def test_load_json_restores_dictionary(self) -> None:
        save_json(VARIANT_DATA, self.file_path)
        self.assertEqual(load_json(self.file_path), VARIANT_DATA)

    def test_variant_sum_equals_150(self) -> None:
        self.assertEqual(calculate_numbers_sum(VARIANT_DATA), 150)

    def test_process_variant_performs_full_cycle(self) -> None:
        restored, result = process_variant(self.file_path)
        self.assertEqual(restored, VARIANT_DATA)
        self.assertEqual(result, 150)

    def test_calculate_sum_supports_floats(self) -> None:
        self.assertAlmostEqual(calculate_numbers_sum({"numbers": [1.5, 2.25]}), 3.75)

    def test_missing_numbers_key_is_rejected(self) -> None:
        with self.assertRaises(JsonDataError):
            calculate_numbers_sum({"id": 1})

    def test_non_list_numbers_is_rejected(self) -> None:
        with self.assertRaises(JsonDataError):
            calculate_numbers_sum({"numbers": "10, 20"})

    def test_empty_numbers_is_rejected(self) -> None:
        with self.assertRaises(JsonDataError):
            calculate_numbers_sum({"numbers": []})

    def test_boolean_in_numbers_is_rejected(self) -> None:
        with self.assertRaises(JsonDataError):
            calculate_numbers_sum({"numbers": [10, True]})

    def test_non_numeric_item_is_rejected(self) -> None:
        with self.assertRaises(JsonDataError):
            calculate_numbers_sum({"numbers": [10, "20"]})

    def test_missing_file_raises_data_error(self) -> None:
        with self.assertRaises(JsonDataError):
            load_json(self.file_path)

    def test_invalid_json_raises_data_error(self) -> None:
        self.file_path.write_text("{broken", encoding="utf-8")
        with self.assertRaises(JsonDataError):
            load_json(self.file_path)

    def test_json_array_root_is_rejected(self) -> None:
        self.file_path.write_text("[1, 2, 3]", encoding="utf-8")
        with self.assertRaises(JsonDataError):
            load_json(self.file_path)

    def test_save_json_rejects_non_dictionary(self) -> None:
        with self.assertRaises(TypeError):
            save_json([1, 2, 3], self.file_path)  # type: ignore[arg-type]


if __name__ == "__main__":
    unittest.main(verbosity=2)
