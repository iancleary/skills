"""Consumer version policy; safe to include in release checks."""
import datetime as dt
import unittest
from unittest.mock import patch

import release_policy


class ReleasePolicyTests(unittest.TestCase):
    def test_rejects_invalid_dates_and_formats(self):
        for value in ("1.2.3", "2026.02.30.0", "2026.09.07.01", "-bad", "2026.09.07.0\n"):
            with self.subTest(value=value), self.assertRaises(ValueError):
                release_policy.validate_version(value)
        release_policy.validate_version("2024.02.29.0")

    def test_daily_serial_and_date_rollover(self):
        with patch.object(release_policy, "versions", return_value=[(2026, 12, 31, 9), (2026, 12, 31, 10)]):
            self.assertEqual(release_policy.next_version(dt.date(2026, 12, 31)), "2026.12.31.11")
            self.assertEqual(release_policy.next_version(dt.date(2027, 1, 1)), "2027.01.01.0")

    def test_unrelated_and_invalid_tags_are_ignored(self):
        with patch.object(release_policy, "git", return_value="v1.0.0\n2026.02.30.0\n2026.09.07.0"):
            self.assertEqual(release_policy.versions(), [(2026, 9, 7, 0)])


if __name__ == "__main__":
    unittest.main()
