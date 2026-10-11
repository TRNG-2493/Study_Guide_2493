"""
test_example.py - WORKED EXAMPLES of the format we expect (one per technique style).
These examples use fields you are NOT asked to design: the large-order threshold (DSC-07).

Conventions
  * Test ID pattern: <TECH>-<AREA>-<NN>-<short-meaning>, set through pytest.param(id=...)
  * Requirement ID in the module docstring or a comment (traceability).
  * One behaviour per test; expected result written in the test, not computed from the code.
"""
import pytest
from membership import (discount_percent, is_large_order, ACTIVE, PENDING, VERIFIED)

# ---- Boundary Value Analysis (3-value) on the order total. Requirement: DSC-07 (large = 100 or more)
LARGE_CASES = [
    pytest.param(99,    False, id="EX-BVA-LRG-01-99-below-min"),
    pytest.param(100,   True,  id="EX-BVA-LRG-02-100-min"),
    pytest.param(101,   True,  id="EX-BVA-LRG-03-101-min+1"),
]


@pytest.mark.parametrize("total, expected", LARGE_CASES)
def test_large_order_boundary(total, expected):
    """DSC-07: totals of 100 or more are 'large'."""
    assert is_large_order(total) is expected


# ---- Decision-table style: one rule (column) = one test. Requirement: DSC-01
def test_example_decision_rule_member_with_valid_promo():
    """EX-DT-DSC-01 - DSC-01: member + valid promo -> 20 percent (other conditions: small order, not student)."""
    assert discount_percent(is_member=True, order_total=40, promo_code="SAVE10", is_student=False) == 20


# ---- State transition style: start state, event, expected result AND expected new state. Requirement: ACC-02
def test_example_state_transition_verify_from_pending(new_account):
    """EX-ST-ACC-01 - ACC-02: Pending --verify--> Active."""
    account = new_account()
    assert account.state == PENDING
    result = account.verify()
    assert result.ok is True and result.code == VERIFIED
    assert account.state == ACTIVE
