"""runner.py -- load the seed data into SQLite and run every validation rule.

Project 1 (QE Foundations), Thursday milestone:
    sql/validation_queries.sql   <-- the RULES (SQL)   you write them
    this module                  <-- the RUNNER (Python)

HOW TO READ THIS FILE
    PROVIDED  = already works; read it, do not rewrite it.
    TODO      = you and your partner implement it (marked with  # TODO).

Usage (run from the repository root; on Windows use `py` if `python` is not found):

    python -m qe_foundations.validation --show R-03       # PREVIEW: print the rows rule R-03 returns
    python -m qe_foundations.validation --show            # preview ALL rules
    python -m qe_foundations.validation --query "SELECT * FROM test_runs LIMIT 5"
    python -m qe_foundations.validation --setup-only --db test_runs.db   # make a file for DB Browser
    python -m qe_foundations.validation                   # THE FULL SUITE (needs your TODOs)
    python -m qe_foundations.validation --allow-failures  # same, but exit code 0 even when rules FAIL
"""
import argparse
import logging
import re
import sqlite3
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import List, Optional

from .exceptions import ValidationFailedError

# ---------------------------------------------------------------- paths (PROVIDED)
REPO_ROOT = Path(__file__).resolve().parents[2]        # .../qe-foundations
DATA_DIR = REPO_ROOT / "qe_foundations" / "data"
DEFAULT_RULES_FILE = REPO_ROOT / "sql" / "validation_queries.sql"
DEFAULT_LOG_FILE = REPO_ROOT / "logs" / "validation.log"
LOGGER_NAME = "qe_foundations.validation"


# ---------------------------------------------------------------- data model (PROVIDED)
@dataclass
class Rule:
    """One validation rule parsed from sql/validation_queries.sql."""
    rule_id: str                # e.g. "R-03"
    dimension: str              # e.g. "Validity"
    description: str            # plain-English rule
    sql: str                    # ONE SELECT statement
    expect: Optional[int] = 0   # rows required to PASS; 0 = violation query, None = informational ("any")


@dataclass
class RuleResult:
    """Outcome of running one rule (PROVIDED -- run_all returns a list of these)."""
    rule: Rule
    status: str                 # "PASS", "FAIL" or "INFO"
    rows: list                  # the rows the query returned (the evidence)


_HEADER = re.compile(r"^--\s*@rule\s+(?P<id>\S+)\s*\|\s*(?P<dim>[^|]*?)\s*\|\s*(?P<desc>.*?)\s*$")
_EXPECT = re.compile(r"^--\s*@expect\s+(?P<n>\d+|any)\s*$", re.IGNORECASE)


def parse_rules(path: Path = DEFAULT_RULES_FILE) -> List[Rule]:
    """PROVIDED. Read the rules file. Format of one rule:

        -- @rule R-01 | Completeness | executed_by must be present
        -- @expect 1            (optional; default 0; "any" = informational)
        SELECT run_id, ... FROM test_runs WHERE ... ;
    """
    rules: List[Rule] = []
    current = None
    for line in Path(path).read_text(encoding="utf-8").splitlines():
        header = _HEADER.match(line.strip())
        if header:
            current = {"id": header["id"], "dim": header["dim"], "desc": header["desc"],
                       "expect": 0, "sql": []}
            rules.append(current)
            continue
        if current is None:
            continue                                   # preamble before the first rule
        expect = _EXPECT.match(line.strip())
        if expect:
            current["expect"] = None if expect["n"].lower() == "any" else int(expect["n"])
        elif not line.strip().startswith("--"):        # skip comment lines inside a rule
            current["sql"].append(line)
    return [Rule(r["id"], r["dim"], r["desc"], "\n".join(r["sql"]).strip(), r["expect"])
            for r in rules]


# ---------------------------------------------------------------- database (PROVIDED)
def connect(db_path: str = ":memory:") -> sqlite3.Connection:
    """Open a SQLite database. ':memory:' = a throw-away DB that vanishes on exit."""
    return sqlite3.connect(db_path)


def load_seed(conn: sqlite3.Connection, data_dir: Path = DATA_DIR) -> None:
    """Create the test_runs table and insert the seed rows (schema first, then seed)."""
    for name in ("test_runs_schema.sql", "test_runs_seed.sql"):
        conn.executescript((Path(data_dir) / name).read_text(encoding="utf-8"))
    conn.commit()


def fetch_rows(conn: sqlite3.Connection, sql: str):
    """Run one SELECT. Returns (column_names, list_of_row_tuples)."""
    cursor = conn.execute(sql)
    columns = [d[0] for d in cursor.description] if cursor.description else []
    return columns, cursor.fetchall()


def print_table(columns, rows) -> None:
    """Print rows as a simple aligned text table (PROVIDED)."""
    cells = [[("NULL" if v is None else str(v)) for v in row] for row in rows]
    widths = [max([len(c)] + [len(r[i]) for r in cells]) for i, c in enumerate(columns)]
    print("  " + " | ".join(c.ljust(w) for c, w in zip(columns, widths)))
    print("  " + "-+-".join("-" * w for w in widths))
    for r in cells:
        print("  " + " | ".join(v.ljust(w) for v, w in zip(r, widths)))
    print(f"  ({len(rows)} row(s))")


# ---------------------------------------------------------------- TODO 1: logging (Wednesday)
def setup_logging(log_file: Path = DEFAULT_LOG_FILE) -> logging.Logger:
    """TODO (Block 4): build and return the logger named LOGGER_NAME.

    Requirements:
      * console handler at INFO, file handler at DEBUG (so the file has more detail)
      * the file is written to `log_file`; create its parent folder first
        (Path.mkdir(parents=True, exist_ok=True)) and open it with encoding="utf-8"
      * a formatter with timestamp, level and message
      * calling setup_logging() twice must NOT duplicate handlers (see Wednesday's
        "duplicate log lines" pitfall)
    Hint: Wednesday demo file demos/3-wednesday/code/qa_logging.py.
    """
    raise NotImplementedError("TODO: implement setup_logging")


# ---------------------------------------------------------------- TODO 2: run one rule
def run_rule(conn: sqlite3.Connection, rule: Rule) -> list:
    """TODO (Block 4): run ONE rule and decide PASS or FAIL.

      * execute rule.sql (use fetch_rows)
      * if rule.expect is None  -> informational: just return the rows
      * if len(rows) == rule.expect -> the rule holds: return the rows
      * otherwise -> raise ValidationFailedError(rule, rows)   (see exceptions.py)
    """
    raise NotImplementedError("TODO: implement run_rule")


# ---------------------------------------------------------------- TODO 3: run the whole suite
def run_all(conn: sqlite3.Connection, rules: List[Rule], logger: logging.Logger) -> List[RuleResult]:
    """TODO (Block 4): run every rule, print one line each, log everything, return results.

    For each rule, call run_rule inside try/except and print EXACTLY this shape
    (check_exercise.py parses it):

        PASS  R-01  Completeness  executed_by must be present
        FAIL  R-02  Validity      executed_by, when present, must look like an e-mail  (2 violating row(s))
        INFO  S-01  Stretch       combined dirty-rows list  (23 row(s))

      * PASS: logger.info(...)
      * FAIL (you caught ValidationFailedError): logger.warning(...), then print each
        evidence row indented under the FAIL line, e.g.  "      (5011, 'priya.nair')"
        -- one rule failing must NOT stop the other rules from running
      * INFO: expect is None (informational rules)
      * any OTHER exception (a typo in your SQL!) is a different problem: log it with
        logger.exception(...) and re-raise it, so a broken query is never mistaken
        for "the data is bad"
      * finish with a one-line summary: how many PASS / FAIL / INFO
    Return a list with one RuleResult per rule, in file order.
    """
    raise NotImplementedError("TODO: implement run_all")


# ---------------------------------------------------------------- command line (PROVIDED + 1 TODO)
def build_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(prog="python -m qe_foundations.validation",
                                description="Run the SQL data-validation rules on test_runs.")
    p.add_argument("--db", default=":memory:", help="SQLite file to use (default: throw-away in-memory DB)")
    p.add_argument("--sql-file", default=str(DEFAULT_RULES_FILE), help="rules file (default: sql/validation_queries.sql)")
    p.add_argument("--log-file", default=str(DEFAULT_LOG_FILE), help="log file (default: logs/validation.log)")
    p.add_argument("--show", nargs="*", metavar="RULE_ID",
                   help="PREVIEW mode: print the rows of the given rules (or all rules) and exit")
    p.add_argument("--query", metavar="SQL", help="run one ad-hoc SELECT and print the result")
    p.add_argument("--setup-only", action="store_true", help="build the database, then stop")
    p.add_argument("--allow-failures", action="store_true",
                   help="exit with code 0 even if some rules FAIL (useful in a demo)")
    return p


def main(argv=None) -> int:
    args = build_parser().parse_args(argv)
    conn = connect(args.db)
    load_seed(conn)

    if args.setup_only:                                  # PROVIDED
        conn.commit()
        print(f"Database ready ({args.db}).")
        return 0

    if args.query:                                       # PROVIDED: ad-hoc SQL
        print_table(*fetch_rows(conn, args.query))
        return 0

    rules = parse_rules(Path(args.sql_file))

    if args.show is not None:                            # PROVIDED: preview mode
        wanted = {r.upper() for r in args.show}
        for rule in rules:
            if wanted and rule.rule_id.upper() not in wanted:
                continue
            print(f"\n{rule.rule_id} | {rule.dimension} | {rule.description}")
            print_table(*fetch_rows(conn, rule.sql))
        return 0

    # ---- TODO 4 (Block 4): the real suite run --------------------------------
    #   1. logger = setup_logging(Path(args.log_file))
    #   2. results = run_all(conn, rules, logger)
    #   3. return 0 if no result has status "FAIL" or args.allow_failures is set,
    #      otherwise return 1   (a non-zero exit code is how CI notices a failure)
    raise NotImplementedError("TODO: wire up setup_logging, run_all and the exit code")


if __name__ == "__main__":
    sys.exit(main())
