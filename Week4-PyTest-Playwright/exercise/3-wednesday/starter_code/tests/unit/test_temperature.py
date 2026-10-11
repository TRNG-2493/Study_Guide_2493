"""Tests for qe_utils.temperature (inline data source). Read the SPECIFICATION first."""
import pytest
from helpers.assertions import assert_close
from qe_utils.temperature import celsius_to_fahrenheit


# TODO (Task 3d): inline-parametrize at least 5 rows with ids: freezing (0 -> 32), boiling (100 -> 212),
#   body (37 -> 98.6), negative (-40 -> -40), absolute-zero (-273.15 -> -459.67).
#   Compare with assert_close (Task 4b), NOT ==, because 37 * 9 / 5 + 32 is not exactly 98.6.
def test_celsius_to_fahrenheit_values():
    """Conversion matches the formula within a tiny tolerance."""
    pytest.fail("TODO Task 3d + 4b")


# TODO (Task 5c): pytest.raises tests: "hot" -> TypeError, True -> TypeError, -273.16 -> ValueError("below absolute zero")
def test_celsius_to_fahrenheit_invalid_input_raises():
    """Wrong type or impossible temperature raises."""
    pytest.fail("TODO Task 5c")
