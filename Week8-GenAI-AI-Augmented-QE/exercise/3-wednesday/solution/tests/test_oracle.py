"""Sanity tests for YOUR oracle (Stage 2). They use only AC2 to AC4, which need no PO answer.
Expected today: they fail with NotImplementedError until you write oracle_us420. Do not edit."""
import pytest

from qa_flow.stories import MSG_NO_BALANCE, MSG_NOT_RECOGNISED, oracle_us420

CODE = "QATEST26ABCD1234"


def test_partial_payment():          # AC2: balance smaller than the total
    assert oracle_us420(80.00, CODE, 50.00) == {"gift_card_pays": 50.00, "remainder": 30.00, "message": None}


def test_balance_covers_everything():  # AC2: balance larger than the total
    assert oracle_us420(80.00, CODE, 120.00) == {"gift_card_pays": 80.00, "remainder": 0.00, "message": None}


def test_cent_precision():           # AC2 at the cent
    got = oracle_us420(80.00, CODE, 79.99)
    assert got["gift_card_pays"] == pytest.approx(79.99) and got["remainder"] == pytest.approx(0.01)


def test_zero_balance():             # AC3
    assert oracle_us420(80.00, CODE, 0.00)["message"] == MSG_NO_BALANCE


def test_bad_character():            # AC1 + AC4
    assert oracle_us420(80.00, "QATEST26ABCD123!", 50.00)["message"] == MSG_NOT_RECOGNISED
