"""Backup "AI draft" for Stage 5 (instructor only).

Representative of what a plain prompt often returns. Use it if Claude is
unavailable, or to show a class the review step. Expected: 3 failed, 3 passed.
The code is right; the failing tests are wrong. The passing ones miss boundaries.
"""
import pytest

from shipping import shipping_cost


def test_free_shipping_over_75():
    assert shipping_cost(100, "US") == 0


def test_standard_shipping_under_75():
    assert shipping_cost(50, "US") == 5.99


def test_canada_shipping():
    assert shipping_cost(50, "CA") == 12.00


def test_express_free_order_is_still_free():          # contradicts sentence 4
    assert shipping_cost(100, "US", express=True) == 0


def test_country_code_is_case_insensitive():           # invented requirement
    assert shipping_cost(100, "us") == 0


def test_unknown_country_returns_zero():               # contradicts sentence 5
    assert shipping_cost(50, "GB") == 0
