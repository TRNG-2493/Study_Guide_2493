"""Tests for celsius_to_fahrenheit and letter_grade (function-style tests)."""
import pytest

from qe_utils import celsius_to_fahrenheit, letter_grade


# ---- WORKED EXAMPLE ----
@pytest.mark.smoke
def test_freezing_point_converts_to_32f():
    assert celsius_to_fahrenheit(0) == 32


# ---- TODO tests ----

def test_boiling_point_converts_to_212f():
    # TODO (Task 3): 100 C -> 212 F. Marker: regression
    pytest.fail("TODO: implement")


def test_body_temperature_uses_approx():
    # TODO (Task 4): 37 C is 98.6 F. Compare with pytest.approx, NOT ==. Marker: regression
    pytest.fail("TODO: implement")


def test_minus_40_is_same_in_both_scales():
    # TODO (Task 3): celsius_to_fahrenheit(-40) == -40. Marker: boundary
    pytest.fail("TODO: implement")


def test_grade_90_is_a():
    # TODO (Task 3): boundary 90 -> "A". Markers: boundary, smoke
    pytest.fail("TODO: implement")


def test_grade_89_is_b():
    # TODO (Task 3): just below 90 -> "B". Marker: boundary
    pytest.fail("TODO: implement")


def test_grade_0_is_f_and_100_is_a():
    # TODO (Task 3): the two extreme valid scores. Marker: boundary
    pytest.fail("TODO: implement")


def test_grade_below_zero_raises_value_error():
    # TODO (Task 4): -1 -> ValueError (check message with match=). Marker: regression
    pytest.fail("TODO: implement")


def test_grade_above_100_raises_value_error():
    # TODO (Task 4): 101 -> ValueError. Marker: regression
    pytest.fail("TODO: implement")


# TODO (Task 5): add ONE test that uses @pytest.mark.skipif on a condition, e.g.
#   @pytest.mark.skipif(sys.version_info < (3, 8), reason="needs Python 3.8+")
# (import sys at the top). Any simple, truthful test is fine. Name it test_..._skipif_example.
