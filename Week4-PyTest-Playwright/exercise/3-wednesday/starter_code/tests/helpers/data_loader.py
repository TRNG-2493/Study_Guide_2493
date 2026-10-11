"""LOADERS: turn files in tests/data/ into pytest.param rows (lesson: data-driven-test-design.md)."""
import csv  # noqa: F401  (you need it for load_csv_cases)
import json
from pathlib import Path

import pytest

DATA_DIR = Path(__file__).resolve().parent.parent / "data"   # works from ANY working directory


def load_cases(filename, fields):
    """WORKED EXAMPLE (already done): read a JSON list of dicts.

    Returns pytest.param rows whose values are taken from `fields` (in that order)
    and whose test ID comes from the row's "id" key.
    """
    rows = json.loads((DATA_DIR / filename).read_text(encoding="utf-8"))
    return [pytest.param(*(r[f] for f in fields), id=r["id"]) for r in rows]


def load_csv_cases(filename):
    """TODO (Task 3b): read tests/data/<filename> and return pytest.param(username, expected, id=row id).

    Remember: every CSV value is TEXT. Convert "true"/"false" to a real bool HERE, not in the test.
    Open the file with newline="" and encoding="utf-8" and use csv.DictReader.
    Do not strip the username: the leading/trailing spaces in some rows are on purpose.
    """
    return []   # TODO: replace. (An empty list makes PyTest SKIP the test: that is the expected starter state.)
