"""conftest.py - options for tests/test_suite_rows.py. Do not edit.

    --suite FILE    suite to run (default: review/approved_suite.json, written by `lab.py signoff`)
    --impl NAME     giftcard (correct) or giftcard_buggy
    --unreviewed    allow a suite that has NOT been signed off (Stage 4 comparison only)
"""
import sys
from pathlib import Path

HERE = Path(__file__).parent
sys.path.insert(0, str(HERE))


def pytest_addoption(parser):
    parser.addoption("--suite", default=str(HERE / "review" / "approved_suite.json"))
    parser.addoption("--impl", default="giftcard", choices=["giftcard", "giftcard_buggy"])
    parser.addoption("--unreviewed", action="store_true")
