"""Tests for qe_utils.shipping. Read the SPECIFICATION in src/qe_utils/shipping.py first."""
import pytest
from helpers.data_loader import load_cases
from qe_utils.shipping import shipping_cost


@pytest.mark.smoke
@pytest.mark.parametrize("weight, zone, expected",
                         load_cases("shipping_cases.json", ["weight", "zone", "expected"]))
def test_shipping_cost_from_json(weight, zone, expected):
    """WORKED EXAMPLE: rates come from tests/data/shipping_cases.json (Task 3a: add rows to that file)."""
    assert shipping_cost(weight, zone) == expected


# TODO (Task 5a): replace the body with a parametrized pytest.raises test (at least 6 rows):
#   (0, "local", ValueError, "between 0 and 30"), (30.01, ...), ("5", ..., TypeError), (True, ...),
#   (2, "mars", ValueError, "unknown zone"), (2, 5, TypeError, "zone must be a string") ...
#   Use pytest.raises(exc_type, match=message) and give every row an id= via pytest.param.
def test_shipping_cost_invalid_input_raises():
    """Invalid weight or zone raises the right exception type with the right message."""
    pytest.fail("TODO Task 5a: write the parametrized pytest.raises test")


# TODO (Task 3c): the spec says "UP TO AND INCLUDING 5 kg" is the light rate. Write a test for exactly 5 kg
#   (national -> 6.50). Run it. If it fails, you found a real defect: DO NOT change src/.
#   Mark the test @pytest.mark.xfail(reason="BUG-001: ...", strict=True) and write the bug report in NOTES.md.
def test_shipping_cost_exactly_5kg_is_light_rate():
    """Boundary: 5 kg is still a light parcel."""
    pytest.fail("TODO Task 3c: write and (if it fails) xfail-mark the boundary test")
