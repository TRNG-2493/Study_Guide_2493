"""Unit tests for the new SQL-validation code.  Run from the repo root:
    python -m unittest discover -s tests -t . -v
(tests/ needs an empty __init__.py; keep your Wednesday tests there too.)
You need at least 5 tests in total across the repo; the four marked TODO below are yours to write.
"""
import sqlite3
import unittest
from pathlib import Path

from qe_foundations.validation.sql_checks import parse_checks

ROOT = Path(__file__).resolve().parents[1]
CHECKS = parse_checks((ROOT / "sql" / "part_e_checks.sql").read_text(encoding="utf-8"))


class TestParseChecks(unittest.TestCase):
    def test_finds_twenty_checks(self):                       # [given]
        self.assertEqual(len(CHECKS), 20)
        self.assertEqual([c.check_id for c in CHECKS][:2], ["E-01", "E-02"])


class TestChecksOnKnownData(unittest.TestCase):
    """Load data/ (dirty) or data/clean into an in-memory database with your loader, then run single checks."""

    def test_dirty_seed_has_two_surplus_duplicate_runs(self):
        self.fail("TODO: load data/ with load_all(conn, ROOT / 'data', ROOT / 'sql' / 'schema.sql'), run check E-05, assert 2 violations")

    def test_clean_data_passes_every_check(self):
        self.fail("TODO: load data/clean, run_all, assert overall_status(results) == 'PASS'")

    def test_a_check_can_fail_on_purpose(self):
        self.fail("TODO (testing the test): load data/clean, UPDATE one run's result to 'PASSED', assert E-14 now reports that run_id")


class TestIngestionContract(unittest.TestCase):
    def test_blank_cells_become_null_and_bad_ids_raise(self):
        self.fail("TODO: call convert_records on tiny hand-made records: '' -> None, 'abc' as id -> your invalid-value exception")


if __name__ == "__main__":
    unittest.main()
