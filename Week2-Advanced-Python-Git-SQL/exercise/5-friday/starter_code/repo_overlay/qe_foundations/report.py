"""python -m qe_foundations.report   (Part F: the Week 2 integration command)

Ingest the seed data into SQLite, run the SQL validation suite, log the results and print a PASS/FAIL data-quality summary.

Exit codes:  0 = every check passed   1 = at least one check failed   2 = the data could not be ingested (or the SQL failed)

Required printed format (check_exercise.py parses it - keep it exactly):
    [PASS] E-01 reconciliation          0 violation(s)  <description>
    [FAIL] E-05 uniqueness              2 violation(s)  <description>
    (blank line)
    DATA QUALITY: FAIL (20 of 20 checks failed, 35 violating row(s))        <- or:  DATA QUALITY: PASS (20 of 20 checks passed)
"""
import argparse
import logging
import sqlite3
import sys
from pathlib import Path

# TODO 1: import what you need from your own modules (the lines below are suggestions; adjust to your names):
# from qe_foundations.ingestion.exceptions import IngestionError
# from qe_foundations.ingestion.sqlite_loader import load_all
# from qe_foundations.utils.logging_setup import setup_logging      # your Wednesday logging helper
# from qe_foundations.validation.sql_checks import overall_status, parse_checks, run_all

log = logging.getLogger("qe_foundations.report")


def build_parser():
    """[given] The command-line interface."""
    parser = argparse.ArgumentParser(prog="python -m qe_foundations.report",
                                     description="Ingest test data and print a data-quality report.")
    parser.add_argument("--data", default="data", help="folder with builds.csv, test_cases.csv, test_runs.json, defects.json")
    parser.add_argument("--db", default=":memory:", help="SQLite database file (default: in memory)")
    parser.add_argument("--checks", default="sql/part_e_checks.sql", help="file with the @CHECK queries")
    parser.add_argument("--schema", default="sql/schema.sql", help="CREATE TABLE script")
    parser.add_argument("--log-file", default="logs/report.log", help="where to write the log")
    parser.add_argument("--show", action="store_true", help="also print the offending ids of failed checks")
    return parser


def format_report(results, show=False):
    """Return the report as a list of text lines (a pure function, so you can unit test it).

    TODO 2: one line per result in the required format, an extra indented line with the offending ids when show is True
            and the result has violations, then a blank line and the final 'DATA QUALITY: ...' line.
    """
    raise NotImplementedError("TODO 2: implement format_report")


def main(argv=None):
    """Return the exit code (the __main__ block passes it to sys.exit).

    TODO 3: args = build_parser().parse_args(argv); set up logging to args.log_file; log "report started".
    TODO 4: connect to args.db; load_all(...); parse the check file; run_all(...).
            Catch your ingestion exception base class (and sqlite3.Error / OSError): log.error(...) with the reason, print ONE line
            "ERROR: <message>" to sys.stderr (no traceback), return 2.
    TODO 5: print the "Loaded: ..." line and format_report(...) lines; log "report finished: PASS/FAIL"; return 0 or 1.
    Always close the connection (try/finally).
    """
    raise NotImplementedError("TODO 3-5: implement main")


if __name__ == "__main__":
    sys.exit(main())
