"""
membership.py - Project 1: Account Membership and Promo Codes (module under test)

Standard library only. Requirement IDs refer to templates/feature-spec-membership-promo-codes.md.
Treat this module as a BLACK BOX: design your tests from the specification, not from this code.

Public API
    signup(age, student)                                  -> Result      (MEM-01..MEM-04)
    validate_promo(code)                                  -> Result      (PRM-01..PRM-05)
    is_large_order(order_total)                           -> bool        (DSC-07)
    discount_percent(is_member, order_total, promo_code, is_student) -> int   (DSC-01..DSC-09)
    Account(balance_due=0) with verify(), suspend(reason), reactivate(), close()   (ACC-01..ACC-08)
"""
from dataclasses import dataclass

# ---------------------------------------------------------------- result codes
MEMBER_CREATED = "MEMBER_CREATED"
AGE_INVALID = "AGE_INVALID"
STUDENT_INVALID = "STUDENT_INVALID"

PROMO_OK = "PROMO_OK"
PROMO_TYPE = "PROMO_TYPE"
PROMO_LENGTH = "PROMO_LENGTH"
PROMO_CHARS = "PROMO_CHARS"
PROMO_UNKNOWN = "PROMO_UNKNOWN"

VERIFIED = "VERIFIED"
SUSPENDED_OK = "SUSPENDED"
REACTIVATED = "REACTIVATED"
CLOSED_OK = "CLOSED"
INVALID_TRANSITION = "INVALID_TRANSITION"
REASON_REQUIRED = "REASON_REQUIRED"
BALANCE_OUTSTANDING = "BALANCE_OUTSTANDING"

# ---------------------------------------------------------------- account states
PENDING, ACTIVE, SUSPENDED, CLOSED = "Pending", "Active", "Suspended", "Closed"

# ---------------------------------------------------------------- business constants
MIN_AGE, MAX_AGE = 16, 65            # MEM-01
MIN_PROMO, MAX_PROMO = 6, 10         # PRM-01
LARGE_ORDER_MIN = 100                # DSC-07
PROMO_CATALOG = {"SAVE10", "WELCOME10", "MEGASALE10"}   # PRM-04


@dataclass(frozen=True)
class Result:
    ok: bool
    code: str


# ================================================================ membership signup
def signup(age, student):
    """MEM-01..MEM-04. First failing check wins: age, then student flag."""
    if isinstance(age, bool) or not isinstance(age, (int, float)):   # MEM-02
        return Result(False, AGE_INVALID)
    if age < MIN_AGE or age >= MAX_AGE:                              # MEM-01
        return Result(False, AGE_INVALID)
    if student is not True and student is not False:                 # MEM-03
        return Result(False, STUDENT_INVALID)
    return Result(True, MEMBER_CREATED)                              # MEM-04


# ================================================================ promo codes
def validate_promo(code):
    """PRM-01..PRM-05. Checks run in this order: type, length, characters, catalog."""
    if not isinstance(code, str):                                    # PRM-05
        return Result(False, PROMO_TYPE)
    text = code.upper()                                              # PRM-03
    if len(text) < MIN_PROMO or len(text) > MAX_PROMO:               # PRM-01
        return Result(False, PROMO_LENGTH)
    if not (text.isascii() and text.isalnum()):                      # PRM-02
        return Result(False, PROMO_CHARS)
    if text not in PROMO_CATALOG:                                    # PRM-04
        return Result(False, PROMO_UNKNOWN)
    return Result(True, PROMO_OK)


# ================================================================ discount decision rule
def is_large_order(order_total):
    """DSC-07: an order is 'large' when the total is 100 or more."""
    return order_total >= LARGE_ORDER_MIN


def discount_percent(is_member, order_total, promo_code, is_student):
    """DSC-01..DSC-09. Returns the discount as a whole percent."""
    promo_ok = validate_promo(promo_code).ok                         # DSC-08
    large = is_large_order(order_total)
    if is_student and not is_member:                                 # DSC-05
        return 5
    if promo_ok:                                                     # DSC-01, DSC-02
        return 20 if is_member else 10
    if is_member:                                                    # DSC-03, DSC-04
        return 15 if large else 5
    return 0                                                         # DSC-06


# ================================================================ account lifecycle
def _invalid():
    return Result(False, INVALID_TRANSITION)


class Account:
    """ACC-01..ACC-08. Pending -> Active -> Suspended -> Closed."""

    def __init__(self, balance_due=0):
        self.state = PENDING                                         # ACC-01
        self.balance_due = balance_due

    def verify(self):
        if self.state != PENDING:                                    # ACC-02
            return _invalid()
        self.state = ACTIVE
        return Result(True, VERIFIED)

    def suspend(self, reason=None):
        if self.state != ACTIVE:                                     # ACC-03
            return _invalid()
        if not isinstance(reason, str) or not reason.strip():        # ACC-04
            return Result(False, REASON_REQUIRED)
        self.state = SUSPENDED
        return Result(True, SUSPENDED_OK)

    def reactivate(self):
        if self.state not in (SUSPENDED, CLOSED):                    # ACC-05
            return _invalid()
        self.state = ACTIVE
        return Result(True, REACTIVATED)

    def close(self):
        if self.state == CLOSED:                                     # ACC-06
            return _invalid()
        if self.balance_due > 0 and self.state != SUSPENDED:         # ACC-07
            return Result(False, BALANCE_OUTSTANDING)
        self.state = CLOSED
        return Result(True, CLOSED_OK)
