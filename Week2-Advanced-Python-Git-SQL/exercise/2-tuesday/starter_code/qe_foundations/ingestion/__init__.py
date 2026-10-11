"""qe_foundations.ingestion - load QE test data from CSV, JSON and XML files.

Public interface (this file is PROVIDED; do not edit it):

    from qe_foundations.ingestion import load_test_cases, load_directory
    report = load_test_cases("data/ingestion/test_cases_messy.csv")
    print(report.summary())
"""

from .contexts import LoadSession, open_source
from .exceptions import *  # noqa: F401,F403  (every exception class, see exceptions.py)
from .loader import (
    BatchResult,
    IngestionReport,
    load_directory,
    load_test_cases,
    write_rejected_csv,
)
from .validation import REQUIRED_FIELDS, VALID_STATUSES, validate_record
