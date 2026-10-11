"""Custom assertions (lesson: custom-assertions.md). Non-test code: nothing here is collected as a test."""
import re  # noqa: F401  (useful for assert_valid_username)

import pytest  # noqa: F401  (useful for pytest.approx / pytest.fail)


def assert_between(value, low, high, label="value"):
    """WORKED EXAMPLE (already done): read it, then copy the style for your own helpers."""
    __tracebackhide__ = True  # the failure points at the TEST line, not at this helper
    assert low <= value <= high, f"{label} {value!r} is outside the range {low}..{high}"


def assert_valid_username(value):
    """TODO (Task 4a): fail with a message that says WHY the username is invalid.

    Check, in this order, and use a different message for each reason:
      1. it is a str            -> "Username must be a str, got <type name>"
      2. length is 3..15 after strip()/lower()   -> mention the actual length
      3. starts with a letter   -> mention the first character
      4. only letters, digits, underscore        -> mention the offending characters
    Start the function with:  __tracebackhide__ = True
    """
    raise NotImplementedError("TODO: implement assert_valid_username")


def assert_close(actual, expected, tolerance=1e-6, label="value"):
    """TODO (Task 4b): assert two floats are equal within `tolerance`.

    Use pytest.approx or abs() - NEVER == on floats. The failure message must show
    actual, expected, the difference and the tolerance, e.g.
        temperature 98.60001 differs from expected 98.6 by 1e-05 (tolerance 1e-06)
    """
    raise NotImplementedError("TODO: implement assert_close")
