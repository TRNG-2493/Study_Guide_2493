"""Starter tests for release 1.1. Two worked examples plus one data-driven example.
Add your own tests below; keep markers consistent with your tier table.
"""
import csv
import pathlib
import sys

import pytest

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent.parent))
from project1_release import AuthService, OK, DENIED, validate_promo  # noqa: E402

DATA = pathlib.Path(__file__).resolve().parent.parent / "data" / "login_cases_starter.csv"


def make_service():
    svc = AuthService()
    svc.add_user("alice", "Passw0rd!")
    return svc


# Worked example 1: a smoke test (Tier 1) - the most important happy path.
@pytest.mark.smoke
def test_valid_login_succeeds():
    assert make_service().login("alice", "Passw0rd!") == OK


# Worked example 2: a regression test (Tier 2) using boundary values of the OLD rule only.
# Your job: extend it for the release 1.1 rule (see the exercise README).
@pytest.mark.regression
@pytest.mark.parametrize("code, expected", [("ABCDEFGH", True), ("ABCDEFG", False)])
def test_promo_lower_boundary(code, expected):
    assert validate_promo(code) is expected


# Data-driven worked example: one test function, many rows from a CSV file.
def load_rows():
    with open(DATA, newline="") as handle:
        return list(csv.DictReader(handle))


@pytest.mark.regression
@pytest.mark.parametrize("row", load_rows(), ids=lambda r: r["case_id"])
def test_login_cases_from_csv(row):
    svc = make_service()
    for _ in range(int(row["prior_wrong_attempts"])):
        svc.login(row["username"], "definitely-wrong")
    assert svc.login(row["username"], row["password"]) == row["expected"]
