"""qe_foundations/ingestion/exceptions.py  -  TASK 2 (about 25 min)

The exception hierarchy for the data-ingestion module. Target tree:

    IngestionError
    +-- SourceError                 the FILE is unusable      -> stop loading that file
    |   +-- SourceNotFoundError
    |   +-- SourceUnreadableError
    |   +-- UnsupportedFormatError
    |   +-- MalformedSourceError
    |   +-- MissingColumnsError
    +-- RecordValidationError       ONE RECORD is bad         -> reject it, keep going
        +-- MissingFieldError
        +-- InvalidValueError
        +-- DuplicateIdError

Already done for you: IngestionError, SourceError, SourceNotFoundError and
RecordValidationError. They show the pattern (store useful attributes, build a
readable message, call super().__init__).

YOUR JOB: replace every `pass  # TODO` below with a real class body.
See README Task 2 for the exact attributes and message rules.
"""

from pathlib import Path


class IngestionError(Exception):
    """Base class: `except IngestionError` catches everything this module raises."""


# ---- The whole source (file) is unusable ----------------------------------
class SourceError(IngestionError):
    """A file as a whole cannot be used. Carries the path and a detail text."""

    def __init__(self, path, detail):
        self.path = str(path)
        self.detail = detail
        super().__init__(f"{Path(path).name}: {detail}")


class SourceNotFoundError(SourceError):
    """EXAMPLE (done for you): the file does not exist."""

    def __init__(self, path):
        super().__init__(path, "file not found")


class SourceUnreadableError(SourceError):
    """TODO: the path exists but cannot be read (permissions, it is a folder, ...).

    __init__(self, path, os_error); the detail should mention the NAME of the
    OS error's class, e.g. "cannot be read (PermissionError)".
    """

    pass  # TODO


class UnsupportedFormatError(SourceError):
    """TODO: the file extension is not .csv/.json/.xml.

    __init__(self, path, suffix); must store `self.suffix`.
    """

    pass  # TODO


class MalformedSourceError(SourceError):
    """TODO: content is invalid for its format (bad JSON, unclosed XML, bad encoding).

    Hint: it can simply reuse SourceError's __init__(path, detail).
    """

    pass  # TODO


class MissingColumnsError(SourceError):
    """TODO: a CSV file lacks required columns.

    __init__(self, path, missing); must store `self.missing` as a list.
    """

    pass  # TODO


# ---- One record is invalid -------------------------------------------------
class RecordValidationError(IngestionError):
    """One record is invalid. `row` is the 1-based record number in the file."""

    def __init__(self, row, field_name, message):
        self.row = row
        self.field = field_name
        super().__init__(f"Row {row}: {message}")


class MissingFieldError(RecordValidationError):
    """TODO: a required field is absent, None, or blank.

    __init__(self, row, field_name)
    """

    pass  # TODO


class InvalidValueError(RecordValidationError):
    """TODO: a field is present but its value is not acceptable.

    __init__(self, row, field_name, value, expected); store `self.value` and
    `self.expected`.
    """

    pass  # TODO


class DuplicateIdError(RecordValidationError):
    """TODO: the same test id appeared earlier in the file.

    __init__(self, row, test_id); store `self.test_id`; the field is "id".
    """

    pass  # TODO
