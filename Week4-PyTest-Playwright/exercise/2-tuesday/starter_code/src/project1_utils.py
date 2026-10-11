"""
project1_utils.py - the "application code" we test in the Monday demo.

These are small, pure Python functions in the style of the Project 1 utility
functions (QE Foundations). They have no I/O and no dependencies, which makes
them ideal first targets for automation.

NOTE FOR INSTRUCTOR: three of these functions contain behaviour worth probing
(divide by zero, float rounding, negative discount) so students have real
edge cases to turn into tests.
"""


def add(a, b):
    """Return a + b."""
    return a + b


def divide(a, b):
    """Return a / b. Raises ZeroDivisionError-style ValueError for b == 0."""
    if b == 0:
        raise ValueError("cannot divide by zero")
    return a / b


def is_even(n):
    """Return True when n is an even integer."""
    return n % 2 == 0


def reverse_string(text):
    """Return text reversed."""
    return text[::-1]


def is_palindrome(text):
    """Case-insensitive palindrome check that ignores spaces."""
    cleaned = text.replace(" ", "").lower()
    return cleaned == cleaned[::-1]


def apply_discount(price, percent):
    """Return price reduced by percent (0-100). Rounded to 2 decimals."""
    if price < 0:
        raise ValueError("price must not be negative")
    if not 0 <= percent <= 100:
        raise ValueError("percent must be between 0 and 100")
    return round(price * (1 - percent / 100), 2)


def average(numbers):
    """Return the arithmetic mean of a non-empty list."""
    if not numbers:
        raise ValueError("numbers must not be empty")
    return sum(numbers) / len(numbers)
