import unittest

from detector import DEMO_MARKER, inspect_process


class DetectorTests(unittest.TestCase):
    def test_match_from_name_case_insensitive(self):
        finding = inspect_process({"pid": 11, "name": "KeyLogger.exe", "cmdline": None})
        self.assertEqual(finding.matches, ("keylogger",))
        self.assertFalse(finding.demo)

    def test_demo_argument(self):
        finding = inspect_process({"pid": 12, "name": "python.exe", "cmdline": [DEMO_MARKER]})
        self.assertEqual(finding.pid, 12)
        self.assertEqual(finding.matches, ("keylogger",))
        self.assertTrue(finding.demo)

    def test_benign_substring(self):
        self.assertIsNone(inspect_process({"pid": 13, "name": "webhook.exe", "cmdline": []}))

    def test_missing_metadata(self):
        self.assertIsNone(inspect_process({"pid": 14, "name": None, "cmdline": None}))

    def test_multiple_indicators(self):
        finding = inspect_process({"pid": 15, "name": "keyboard-tool.exe", "cmdline": ["--hook"]})
        self.assertEqual(finding.matches, ("keyboard", "hook"))
        self.assertFalse(finding.demo)


if __name__ == "__main__":
    unittest.main()
