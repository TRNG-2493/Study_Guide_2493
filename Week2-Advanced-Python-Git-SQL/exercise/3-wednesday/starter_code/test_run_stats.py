"""
test_run_stats.py -- Part C: your unit tests for run_stats.py.

Run from the starter_code folder:
    python -m unittest -v test_run_stats

Requirements (see README, Part C):
  * at least 12 test methods
  * one regression test for each of the 7 bugs (a test that FAILS on the buggy file and PASSES once fixed)
  * at least 3 tests of bad or unusual input (empty list, n == 0, missing key)
  * at least 1 test that uses assertRaises
  * at least 1 use of setUp (so tests stay independent) and at least 1 use of assertLogs (Part B)
Name every test for the behaviour it protects, e.g. test_even_count_averages_two_middle_values.
"""
import unittest

import run_stats


class TestMedian(unittest.TestCase):
    # Worked example: Arrange, Act, Assert.
    def test_odd_count_returns_middle(self):
        values = [5, 1, 3]                       # Arrange
        result = run_stats.median(values)        # Act
        self.assertEqual(result, 3)              # Assert

    # TODO: even count (BUG-1)    TODO: empty list (BUG-7)    TODO: input list not changed


class TestSlowest(unittest.TestCase):
    pass
    # TODO: n items, biggest first (BUG-2)    TODO: n == 0    TODO: caller's list not reordered (BUG-6)


class TestGroupBySuite(unittest.TestCase):
    pass
    # TODO: counts per suite and status (BUG-3)    TODO: missing "suite" -> "unknown"    TODO: assertLogs WARNING


class TestNoteFlaky(unittest.TestCase):
    pass
    # TODO: two calls without a list do not share state (BUG-4)    TODO: caller's own list is extended


class TestRunIdAndSummary(unittest.TestCase):
    def setUp(self):
        run_stats.run_counter = 0                # reset shared state so each test starts clean
        self.results = [{"test": "t1", "suite": "login", "status": "pass"}]

    pass
    # TODO: ids increase (BUG-5)    TODO: summary with durations (latest_ms, BUG-6)    TODO: summary with [] (BUG-7)


if __name__ == "__main__":
    unittest.main()
