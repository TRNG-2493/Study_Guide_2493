"""legacy_helpers.py - the ONE-FILE helper script you inherited.

Your job (see README.md, Part 2): split these functions into modules inside
the package qe_foundations/utils/, then DELETE this file from your repo.

Target modules:
    strings.py   -> slugify, normalize_whitespace, is_valid_email
    numbers.py   -> is_positive_int, clamp, percent
    dates.py     -> add_days, is_weekend, timestamp_for_filename
    data_gen.py  -> FIRST_NAMES, ROLES, make_users

Known problems you must fix while moving the code:
  * It prints and runs "demo" code at import time (see the bottom of the file).
    A library must be SILENT when imported - use `if __name__ == "__main__":`.
  * Everything lives in one file, so nothing can be imported selectively.
"""

import random
from datetime import datetime, timedelta

print("legacy_helpers loaded")  # <- side effect on import: remove it


# ---------------------------------------------------------------- strings
def normalize_whitespace(text):
    """Trim the text and collapse runs of whitespace into one space."""
    return " ".join(text.split())


def slugify(text):
    """'  Login Page: Happy Path ' -> 'login-page-happy-path'."""
    cleaned = normalize_whitespace(text).lower()
    kept = [ch if ch.isalnum() else " " for ch in cleaned]
    return "-".join("".join(kept).split())


def is_valid_email(email):
    """True when email has exactly one '@' and a '.' in the domain part."""
    return email.count("@") == 1 and "." in email.split("@")[1]


# --------------------------------------------------------------- numbers
def is_positive_int(value):
    """True for ints greater than zero (bool is NOT accepted)."""
    return isinstance(value, int) and not isinstance(value, bool) and value > 0


def clamp(value, low, high):
    """Limit value to the range low..high."""
    return max(low, min(value, high))


def percent(part, whole):
    """part as a percentage of whole, rounded to 1 decimal; 0.0 if whole is 0."""
    if whole == 0:
        return 0.0
    return round(part / whole * 100, 1)


# ----------------------------------------------------------------- dates
def add_days(day, days):
    """Return the date `days` after `day` (a datetime.date). Negative goes back."""
    return day + timedelta(days=days)


def is_weekend(day):
    """True when the date falls on Saturday or Sunday."""
    return day.weekday() >= 5


def timestamp_for_filename(moment=None):
    """'20250131_093000' - safe to use inside file and folder names."""
    moment = moment or datetime.now()
    return moment.strftime("%Y%m%d_%H%M%S")


# -------------------------------------------------------------- test data
FIRST_NAMES = ["Asha", "Ben", "Carla", "Dev", "Elena", "Farid"]
ROLES = ["viewer", "editor", "admin"]


def make_users(count, seed=None):
    """Return `count` user dicts. The same seed always gives the same users."""
    rng = random.Random(seed)
    users = []
    for i in range(1, count + 1):
        name = rng.choice(FIRST_NAMES)
        users.append({
            "id": i,
            "name": name,
            "email": f"{name.lower()}{i}@example.com",
            "age": rng.randint(18, 65),
            "role": rng.choice(ROLES),
        })
    return users


# ----------------------------------------------- leftover demo code (BAD)
print(slugify("  Login Page: Happy Path "))
print(make_users(2, seed=1))
