"""Run the SQL data-quality checks stored in sql/part_e_checks.sql.   (Part F - Thursday validation + Friday joins)

The file format (one block per check):
    -- @CHECK E-05 | uniqueness | One run per (build, case) ... | returns test_runs.run_id
    SELECT ... ;          <- returns the VIOLATING rows, first column = primary key. Zero rows = PASS.
"""
import logging
import re
import sqlite3
from collections import namedtuple

log = logging.getLogger(__name__)

Check = namedtuple("Check", "check_id category description returns sql")
CheckResult = namedtuple("CheckResult", "check_id category description returns violating_ids status")

_TAG = re.compile(r"^--\s*@CHECK\s+(.*)$")


def parse_checks(text):
    """[given] Parse the check-file text into a list of Check tuples (comment lines inside a block are ignored)."""
    checks, header, sql_lines = [], None, []
    for line in text.splitlines():
        match = _TAG.match(line.strip())
        if match:
            header, sql_lines = [p.strip() for p in match.group(1).split("|")], []
            continue
        if header is None or line.strip().startswith("--"):
            continue
        sql_lines.append(line)
        sql = "\n".join(sql_lines).strip()
        if sql.endswith(";") and sqlite3.complete_statement(sql):
            checks.append(Check(header[0], header[1], header[2],
                                header[3].replace("returns", "").strip() if len(header) > 3 else "", sql))
            header, sql_lines = None, []
    return checks


def run_check(conn, check):
    """Execute ONE check and return a CheckResult.

    TODO 1: rows = conn.execute(check.sql).fetchall(); violating_ids = the first column of every row;
            status = "PASS" when there are no rows, otherwise "FAIL".
    """
    raise NotImplementedError("TODO 1: implement run_check")


def run_all(conn, checks):
    """Run every check and return the list of CheckResult (same order as the file).

    TODO 2: log each outcome with the logging module (NOT print):
            PASS -> log.info(...)   FAIL -> log.warning(...) including the check id, the count and the offending ids.
    """
    raise NotImplementedError("TODO 2: implement run_all")


def overall_status(results):
    """TODO 3: return "FAIL" if any result has status "FAIL", else "PASS"."""
    raise NotImplementedError("TODO 3: implement overall_status")
