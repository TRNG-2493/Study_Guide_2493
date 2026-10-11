"""TASK 5 - mock the external rate API. No test in this file may touch the network.

Read src/pricing.py and src/exchange.py first. Note HOW pricing gets get_rate.
Reminder: patch the name where it is LOOKED UP.
"""
from unittest.mock import MagicMock, patch   # noqa: F401  (you will need these)

import pytest
import requests                              # noqa: F401  (for the error scenarios)

import exchange                              # noqa: F401
import pricing                               # noqa: F401


@pytest.fixture
def mock_get_rate():
    pytest.skip("TODO (Task 5): patch the right target and YIELD the mock (use `with patch(...) as m: yield m`)")


def test_price_in_converts_with_mocked_rate(mock_get_rate):
    pytest.fail("TODO: rate 0.5, price 10 -> 5.0, and assert get_rate was called once with ('USD','EUR')")


def test_price_in_parametrized_rates(mock_get_rate):
    pytest.fail("TODO: parametrize (price, rate, expected) with >= 4 rows incl. rounding and zero price")


def test_price_in_usd_makes_no_lookup(mock_get_rate):
    pytest.fail("TODO: price_in(10,'USD') == 10 and the mock was never called")


def test_price_in_rejects_negative(mock_get_rate):
    pytest.fail("TODO: ValueError, and no lookup happened")


def test_price_label_formats_two_decimals(mock_get_rate):
    pytest.fail("TODO: rate 0.5, price 37 -> '18.50 EUR'")


def test_price_label_degrades_when_api_fails(mock_get_rate):
    pytest.fail("TODO: parametrize 3 requests exceptions as side_effect (ConnectionError, Timeout, HTTPError) -> 'Price unavailable'")


def test_price_label_does_not_swallow_other_errors(mock_get_rate):
    pytest.fail("TODO: side_effect=KeyError('rate') must propagate out of price_label")


def test_patching_the_wrong_target_does_not_work():
    pytest.fail("TODO: patch 'exchange.get_rate' (wrong place) and show price_in still hits the network blocker -> RuntimeError")


def test_get_rate_reads_json_and_calls_api_correctly():
    pytest.fail("TODO: patch requests.get as seen from exchange; fake response json {'rate': 0.91}; check the call arguments and raise_for_status")


def test_get_rate_propagates_http_errors():
    pytest.fail("TODO: fake response whose raise_for_status raises HTTPError; the error must reach the caller")


@pytest.mark.skip(reason="Stretch C: create_autospec(exchange.get_rate) and show a wrong call signature raises TypeError")
def test_stretch_autospec():
    ...


@pytest.mark.skip(reason="Stretch C: redo one test with monkeypatch.setattr(pricing, 'get_rate', ...) instead of patch")
def test_stretch_monkeypatch():
    ...
