"""Автоматичні тести контекстного менеджера ConfigContext."""

import unittest

from config_context import (
    ApplicationConfig,
    ConfigContext,
    InvalidConfigValueError,
    UnknownConfigKeyError,
)


class ConfigContextTests(unittest.TestCase):
    def setUp(self) -> None:
        self.config = ApplicationConfig(debug=False, timeout=30, theme="light")

    def test_context_applies_all_overrides(self) -> None:
        with ConfigContext(self.config, debug=True, timeout=5) as temporary:
            self.assertTrue(temporary["debug"])
            self.assertEqual(temporary["timeout"], 5)

    def test_context_returns_same_config_object(self) -> None:
        with ConfigContext(self.config, debug=True) as temporary:
            self.assertIs(temporary, self.config)

    def test_values_are_restored_after_normal_exit(self) -> None:
        original = self.config.as_dict()
        with ConfigContext(self.config, theme="dark"):
            pass
        self.assertEqual(self.config.as_dict(), original)

    def test_values_are_restored_after_exception(self) -> None:
        original = self.config.as_dict()
        with self.assertRaises(RuntimeError):
            with ConfigContext(self.config, debug=True):
                raise RuntimeError("test")
        self.assertEqual(self.config.as_dict(), original)

    def test_original_exception_is_not_suppressed(self) -> None:
        with self.assertRaisesRegex(RuntimeError, "test"):
            with ConfigContext(self.config, debug=True):
                raise RuntimeError("test")

    def test_nested_contexts_restore_their_own_snapshots(self) -> None:
        with ConfigContext(self.config, debug=True):
            self.assertTrue(self.config["debug"])
            with ConfigContext(self.config, timeout=10):
                self.assertEqual(self.config["timeout"], 10)
            self.assertEqual(self.config["timeout"], 30)
            self.assertTrue(self.config["debug"])
        self.assertFalse(self.config["debug"])

    def test_unknown_override_raises_custom_exception(self) -> None:
        with self.assertRaises(UnknownConfigKeyError):
            with ConfigContext(self.config, unknown="value"):
                pass

    def test_invalid_type_raises_custom_exception(self) -> None:
        with self.assertRaises(InvalidConfigValueError):
            with ConfigContext(self.config, timeout="fast"):
                pass

    def test_failed_enter_does_not_change_other_values(self) -> None:
        original = self.config.as_dict()
        with self.assertRaises(UnknownConfigKeyError):
            with ConfigContext(self.config, debug=True, unknown="value"):
                pass
        self.assertEqual(self.config.as_dict(), original)

    def test_configuration_copy_is_independent(self) -> None:
        copied = self.config.as_dict()
        copied["debug"] = True
        self.assertFalse(self.config["debug"])

    def test_unknown_getitem_raises_custom_exception(self) -> None:
        with self.assertRaises(UnknownConfigKeyError):
            _ = self.config["missing"]

    def test_empty_configuration_is_rejected(self) -> None:
        with self.assertRaises(ValueError):
            ApplicationConfig()

    def test_empty_context_is_rejected(self) -> None:
        with self.assertRaises(ValueError):
            ConfigContext(self.config)

    def test_wrong_config_object_is_rejected(self) -> None:
        with self.assertRaises(TypeError):
            ConfigContext({"debug": False}, debug=True)  # type: ignore[arg-type]

    def test_configuration_supports_iteration_and_length(self) -> None:
        self.assertEqual(list(self.config), ["debug", "timeout", "theme"])
        self.assertEqual(len(self.config), 3)


if __name__ == "__main__":
    unittest.main(verbosity=2)
