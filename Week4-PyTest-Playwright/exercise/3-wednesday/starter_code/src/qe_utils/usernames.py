"""Code under test: username utilities (Project 1 utility function).

SPECIFICATION:
  normalize_username(name): strip surrounding whitespace and lower-case it.
      Not a string -> TypeError("username must be a string").
  is_valid_username(name): True when the NORMALIZED name
      * is 3 to 15 characters long,
      * starts with a letter,
      * contains only letters, digits and underscores.
      Anything that is not a string -> False (no exception).
"""
import re

_PATTERN = re.compile(r"^[a-z][a-z0-9_]{2,14}$")


def normalize_username(name):
    if not isinstance(name, str):
        raise TypeError("username must be a string")
    return name.strip().lower()


def is_valid_username(name):
    if not isinstance(name, str):
        return False
    return bool(_PATTERN.match(normalize_username(name)))
