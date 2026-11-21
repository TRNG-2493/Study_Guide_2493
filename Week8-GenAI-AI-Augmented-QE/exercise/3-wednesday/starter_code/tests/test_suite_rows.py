"""test_suite_rows.py - runs a signed-off test case suite (JSON) as parametrized pytest rows.

The sign-off GATE is part of the suite: a file without status APPROVED is refused unless
--unreviewed is passed. Same design as the Wednesday demo. Do not edit.

    python -m pytest -q tests/test_suite_rows.py                                  # approved suite, correct app
    python -m pytest -q tests/test_suite_rows.py --impl giftcard_buggy
    python -m pytest -q tests/test_suite_rows.py --suite evidence/<draft>.txt --unreviewed

AC5 (speed) is skipped here: it is not a unit-level check.
"""
import importlib
import json
from pathlib import Path

import pytest

from qa_flow.reqs_review import extract_json


def _load(config):
    path = Path(config.getoption("--suite"))
    if not path.exists():
        return None
    data = json.loads(extract_json(path.read_text(encoding="utf-8")))
    if data.get("status") != "APPROVED" and not config.getoption("--unreviewed"):
        raise pytest.UsageError(f"{path} has not been signed off (status={data.get('status')!r}). "
                                "Run 'python lab.py signoff' first.")
    return data["test_cases"]


def pytest_generate_tests(metafunc):
    if "case" in metafunc.fixturenames:
        cases = _load(metafunc.config)
        if cases is None:
            metafunc.parametrize("case", [pytest.param({}, marks=pytest.mark.skip(
                reason="no signed-off suite yet (review/approved_suite.json)"))])
            return
        metafunc.parametrize("case", cases, ids=[c["id"] for c in cases])


@pytest.fixture
def apply_gift_card(request):
    return importlib.import_module("shopfront." + request.config.getoption("--impl")).apply_gift_card


def test_row(case, apply_gift_card):
    if case.get("ac") == "AC5":
        pytest.skip("AC5 (speed) is not a unit-level check")
    td = case.get("test_data") or {}
    got = apply_gift_card(float(td["order_total"]), td["code"], float(td["balance"]))
    if case.get("expected_gift_card_pays") is None and case.get("expected_message") is None:
        pytest.fail(f"{case['id']} has no expected result: it is not a test yet")
    if case.get("expected_gift_card_pays") is not None:
        assert got["gift_card_pays"] == pytest.approx(float(case["expected_gift_card_pays"]), abs=0.001)
    if case.get("expected_remainder") is not None:
        assert got["remainder"] == pytest.approx(float(case["expected_remainder"]), abs=0.001)
    assert got["message"] == (case.get("expected_message") or None)
