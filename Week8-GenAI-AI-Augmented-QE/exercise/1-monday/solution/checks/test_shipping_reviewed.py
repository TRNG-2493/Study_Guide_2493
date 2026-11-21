"""Reference human-reviewed tests for shipping.py (instructor only).

Each test names the docstring sentence it proves. Use it to compare against the
trainees' Claude-drafted test_shipping_ai.py in Stage 5.
Run from this folder:  python -m pytest -q test_shipping_reviewed.py
"""
import pytest

from shipping import shipping_cost


# Sentence 1: US orders with a subtotal of $75.00 or more ship free.
@pytest.mark.parametrize("subtotal", [75.00, 75.01, 500.00])
def test_us_at_or_above_75_ships_free(subtotal):
    assert shipping_cost(subtotal, "US") == 0.0


# Sentence 2: US orders under $75.00 pay a flat $5.99. (Boundary just below, and zero.)
@pytest.mark.parametrize("subtotal", [0.00, 20.00, 74.99])
def test_us_under_75_pays_flat_rate(subtotal):
    assert shipping_cost(subtotal, "US") == 5.99


# Sentence 3: Canadian orders pay a flat $12.00, whatever the subtotal.
@pytest.mark.parametrize("subtotal", [0.00, 74.99, 75.00, 500.00])
def test_ca_flat_rate_ignores_subtotal(subtotal):
    assert shipping_cost(subtotal, "CA") == 12.00


# Sentence 4: Express adds $10.00, including free-shipping orders.
@pytest.mark.parametrize(
    "subtotal, country, expected",
    [(75.00, "US", 10.00), (74.99, "US", 15.99), (10.00, "CA", 22.00)],
)
def test_express_adds_ten(subtotal, country, expected):
    assert shipping_cost(subtotal, country, express=True) == expected


# Sentence 5: any other country code raises ValueError.
@pytest.mark.parametrize("country", ["GB", "", "USA"])
def test_unsupported_country_raises(country):
    with pytest.raises(ValueError):
        shipping_cost(50.00, country)


# Sentence 6: a negative subtotal raises ValueError.
def test_negative_subtotal_raises():
    with pytest.raises(ValueError):
        shipping_cost(-0.01, "US")


# NOT SPECIFIED: is "us" (lower case) accepted? The docstring is silent.
# The code rejects it. This is a question for the product owner, not an assertion.
# A Claude draft that asserts shipping_cost(80, "us") == 0.0 has invented a requirement.
