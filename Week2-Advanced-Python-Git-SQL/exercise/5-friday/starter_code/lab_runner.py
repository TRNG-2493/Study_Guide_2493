"""
lab_runner.py - run the exercise .sql files with Python's built-in sqlite3 (works on Windows, macOS, Linux).

Usage (from this folder, PowerShell or bash - the commands are identical):

    python lab_runner.py sql/part_b_joins.sql             # run every task in the file and print the results
    python lab_runner.py sql/part_b_joins.sql --only B3   # run everything, print only task B3
    python lab_runner.py --checks sql/part_e_checks.sql   # Part E: run the validation suite, print PASS/FAIL per check
    python lab_runner.py --checks sql/part_e_checks.sql --only E-05 --show   # also list the offending ids

Every run builds a FRESH in-memory database from sql/schema.sql + sql/seed.sql, so you can never damage the seed.
Statements are cut apart with sqlite3.complete_statement(); the "-- @Q id title" comment in front of a statement is its label.
"""
import argparse
import os
import re
import sqlite3
import sys
from collections import namedtuple

HERE = os.path.dirname(os.path.abspath(__file__))
SCHEMA = os.path.join(HERE, "sql", "schema.sql")
SEED = os.path.join(HERE, "sql", "seed.sql")

TAG_Q = re.compile(r"^--\s*@Q\s+(\S+)\s*(.*)$")
TAG_CHECK = re.compile(r"^--\s*@CHECK\s+(.*)$")

Statement = namedtuple("Statement", "qid title sql expect_error")
Result = namedtuple("Result", "qid title sql expect_error ok error_type error_msg cols rows rowcount")
Check = namedtuple("Check", "check_id category description returns sql")

TODO_MARKERS = ("'TODO' AS todo", "NULL AS violating_id WHERE 1 = 0")


def build_db(schema_path=SCHEMA, seed_path=SEED):
    """Return a fresh in-memory database. Autocommit mode so BEGIN/ROLLBACK and PRAGMA behave as written."""
    conn = sqlite3.connect(":memory:", isolation_level=None)
    with open(schema_path, encoding="utf-8") as f:
        conn.executescript(f.read())
    with open(seed_path, encoding="utf-8") as f:
        conn.executescript(f.read())
    return conn


def split_statements(text):
    """Yield Statement(qid, title, sql, expect_error) for every complete statement in the text."""
    buf, out = [], []
    for line in text.splitlines():
        buf.append(line)
        chunk = "\n".join(buf)
        if line.rstrip().endswith(";") and sqlite3.complete_statement(chunk):
            qid, title = "?", ""
            for b in buf:
                m = TAG_Q.match(b.strip())
                if m:
                    qid, title = m.group(1), m.group(2)
                m = TAG_CHECK.match(b.strip())
                if m:
                    parts = [p.strip() for p in m.group(1).split("|")]
                    qid, title = parts[0], " | ".join(parts[1:])
            out.append(Statement(qid, title, chunk.strip(), "EXPECT-ERROR" in title))
            buf = []
    return out


def code_only(sql):
    """The statement without its comment lines."""
    return "\n".join(l for l in sql.splitlines() if not l.strip().startswith("--"))


def is_placeholder(sql):
    code = code_only(sql)
    return any(marker in code for marker in TODO_MARKERS)


def execute(conn, st):
    """Run one statement and capture rows or the error (never raises)."""
    try:
        cur = conn.execute(st.sql)
        cols = [d[0] for d in cur.description] if cur.description else None
        rows = cur.fetchall() if cols is not None else []
        return Result(st.qid, st.title, st.sql, st.expect_error, True, None, None, cols, rows, cur.rowcount)
    except sqlite3.Error as exc:
        return Result(st.qid, st.title, st.sql, st.expect_error, False, type(exc).__name__, str(exc), None, [], -1)


def run_file(conn, path):
    with open(path, encoding="utf-8") as f:
        text = f.read()
    return [execute(conn, st) for st in split_statements(text)]


def parse_checks(text):
    """Parse the Part E file format into a list of Check tuples (same format Part F reads)."""
    checks = []
    for st in split_statements(text):
        if not st.title or st.qid == "?":
            continue
        if not re.match(r"^E-\d+$", st.qid):
            continue
        parts = [p.strip() for p in st.title.split("|")]
        category = parts[0] if parts else ""
        description = parts[1] if len(parts) > 1 else ""
        returns = parts[2].replace("returns", "").strip() if len(parts) > 2 else ""
        checks.append(Check(st.qid, category, description, returns, st.sql))
    return checks


# ----------------------------------------------------------------- normalising results (used by check_exercise.py)

def normalise_rows(rows):
    """Order-independent, float-tolerant representation of a result set."""
    def norm(v):
        if isinstance(v, float):
            return round(v, 2)
        return v
    return sorted((tuple(norm(v) for v in r) for r in rows), key=repr)


# ----------------------------------------------------------------- pretty printing

def fmt_value(v):
    return "NULL" if v is None else str(v)


def fmt_table(cols, rows):
    data = [[fmt_value(v) for v in r] for r in rows]
    widths = [max([len(c)] + [len(r[i]) for r in data]) for i, c in enumerate(cols)]
    head = " | ".join(c.ljust(w) for c, w in zip(cols, widths)).rstrip()
    rule = "-+-".join("-" * w for w in widths)
    body = [" | ".join(v.ljust(w) for v, w in zip(r, widths)).rstrip() for r in data]
    n = len(rows)
    return "\n".join([head, rule] + body + ["(%d row%s)" % (n, "" if n == 1 else "s")])


def wanted(qid, only):
    if not only:
        return True
    return re.match(r"^%s(?!\d)" % re.escape(only), qid) is not None


def print_results(results, only=None):
    shown = 0
    for r in results:
        if not wanted(r.qid, only):
            continue
        shown += 1
        print("=" * 78)
        print("%s  %s" % (r.qid, r.title))
        print("-" * 78)
        if not r.ok:
            if r.expect_error:
                print("EXPECTED ERROR (good, the constraint did its job): %s: %s" % (r.error_type, r.error_msg))
            else:
                print("ERROR: %s: %s" % (r.error_type, r.error_msg))
        elif r.expect_error:
            print("WARNING: this statement was expected to FAIL but it succeeded.")
        elif r.cols is None:
            print("OK (statement executed; rows affected: %s)" % (r.rowcount if r.rowcount >= 0 else "n/a"))
        else:
            print(fmt_table(r.cols, r.rows))
            if "todo" in [c.lower() for c in r.cols]:
                print("-> TODO: you have not replaced the placeholder yet.")
        print()
    if only and shown == 0:
        print("No task matches --only %s" % only)


def run_checks(conn, checks, only=None, show=False):
    failed = todo = 0
    shown = 0
    for c in checks:
        if not wanted(c.check_id, only):
            continue
        shown += 1
        res = execute(conn, Statement(c.check_id, c.description, c.sql, False))
        if not res.ok:
            print("[ERROR] %s %-22s %s: %s" % (c.check_id, c.category, res.error_type, res.error_msg))
            failed += 1
            continue
        if is_placeholder(c.sql):
            print("[TODO ] %s %-22s not written yet" % (c.check_id, c.category))
            todo += 1
            continue
        n = len(res.rows)
        status = "PASS" if n == 0 else "FAIL"
        failed += n > 0
        print("[%s] %s %-22s %2d violation(s)  %s" % (status, c.check_id, c.category, n, c.description))
        if show and n:
            ids = [r[0] for r in res.rows]
            print("        offending %s: %s" % (c.returns or "ids", ids))
    if only and shown == 0:
        print("No check matches --only %s" % only)
    print()
    print("%d check(s) listed, %d with violations, %d still TODO" % (shown, failed, todo))


def main(argv=None):
    ap = argparse.ArgumentParser(description="Run exercise SQL files against a fresh in-memory Release Tracker database.")
    ap.add_argument("sql_file", nargs="?", help="a part_*.sql file (Parts A-D)")
    ap.add_argument("--checks", metavar="FILE", help="run a Part E check file and print a PASS/FAIL line per check")
    ap.add_argument("--only", help="show only this task/check id (prefix match, e.g. B3 or E-05)")
    ap.add_argument("--show", action="store_true", help="with --checks: also print the offending ids")
    args = ap.parse_args(argv)
    if not args.sql_file and not args.checks:
        ap.error("give a .sql file, or --checks FILE")
    print("SQLite library version: %s" % sqlite3.sqlite_version)
    conn = build_db()
    if args.checks:
        with open(args.checks, encoding="utf-8") as f:
            checks = parse_checks(f.read())
        run_checks(conn, checks, args.only, args.show)
    else:
        print_results(run_file(conn, args.sql_file), args.only)
    return 0


if __name__ == "__main__":
    sys.exit(main())
