"""qe_foundations/ingestion/validation.py  -  TASK 5 (about 25 min)

validate_record() decides whether ONE raw record is acceptable.

IMPORTANT: this is VALIDATION OF EXTERNAL DATA. Raise exceptions here.
Do NOT use `assert` in this file (assertions can be switched off with `python -O`).
See README Task 5 for the exact rules.
"""

from .exceptions import InvalidValueError, MissingFieldError

REQUIRED_FIELDS = ("id", "title", "status", "duration")
VALID_STATUSES = ("pass", "fail", "blocked")


def validate_record(row, raw):
    """Turn one raw record into a clean dict, or raise a RecordValidationError.

    row : 1-based record number in the file (used in error messages)
    raw : whatever the reader produced for that record (usually a dict)

    Returns {"id": str, "title": str, "status": str, "duration": float}.
    """
    raise NotImplementedError("Task 5: write validate_record")
