"""Validators: functions that answer yes/no. Every validator RETURNS True or False (never prints)."""


def is_in_range(value, low, high):
    """Return True if low <= value <= high (both ends included)."""
    # TODO: one comparison; Python allows low <= value <= high
    pass


def is_valid_test_id(test_id, prefix="TC", digits=3):
    """Return True for IDs like 'TC-007': the prefix, a dash, then exactly `digits` digits."""
    # TODO: check the start with .startswith, slice off the prefix, then .isdigit() and len()
    pass


def is_valid_email(email):
    """Return True for a simple email shape (a deliberately simple teaching version).

    Rules: no spaces, exactly one '@', something before the '@',
    and a domain that contains a '.' but does not start or end with one.
    """
    # TODO: early `return False` checks first (space, count of '@'), then split('@')
    pass


def is_strong_password(password, min_length=8):
    """Return True if the password has at least `min_length` characters and
    contains at least one uppercase letter, one lowercase letter and one digit."""
    # TODO: loop over the characters with a flag per kind; .isupper() .islower() .isdigit()
    pass


def is_valid_status_code(code):
    """Return True for HTTP status codes from 100 to 599. Reuses is_in_range."""
    # TODO: ONE line: reuse is_in_range
    pass


def all_pass(value, *checks):
    """Return True only if EVERY check function returns a true value for `value`.

    With no checks at all, return True.
    Example: all_pass("TC-001", is_valid_test_id, lambda s: s.endswith("1"))
    """
    # TODO: loop over `checks`; return False as soon as one fails; return True after the loop
    pass
