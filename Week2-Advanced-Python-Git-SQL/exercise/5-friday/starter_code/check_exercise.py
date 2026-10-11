"""
check_exercise.py - self-check for the Week 2 / 5-friday exercise (SQL joins, data validation, Week 2 integration).

    python check_exercise.py                         # Parts A-E (your files in sql/)
    python check_exercise.py --repo ..\\qe-foundations  # Parts A-E + Part F (your qe-foundations repo; bash: ../qe-foundations)
    python check_exercise.py --part B                # one part only (A, B, C, D, E or F)
    python check_exercise.py --sql-dir DIR           # read part_*.sql from another folder (instructors: solution/sql)

Run Part F with your virtual environment ACTIVE, from any folder: the script launches
"python -m qe_foundations.report" inside the repo with the same Python that runs this script.

What it does: runs your SQL against a fresh copy of the seed database and compares the RESULTS with the expected ones
(stored as hashes, so the answers are not printed here). Row order and column aliases do not matter; column ORDER
and values do. It tells you which tasks pass, which are still TODO, and gives a hint when a result is wrong.
Exit code 0 only if everything that was checked passed.
"""
import argparse
import hashlib
import json
import os
import re
import subprocess
import sys
import tempfile

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import lab_runner as lr  # noqa: E402

# BEGIN EXPECTED (generated from the instructor solution; hashes only)
EXPECTED = {
 "E": {
  "E-01": {
   "count": 2,
   "ids": "7dd07a550efb"
  },
  "E-02": {
   "count": 2,
   "ids": "5960c5d1b77a"
  },
  "E-03": {
   "count": 1,
   "ids": "fe94b827f045"
  },
  "E-04": {
   "count": 2,
   "ids": "97b0bcd3f640"
  },
  "E-05": {
   "count": 2,
   "ids": "4f83d753425f"
  },
  "E-06": {
   "count": 1,
   "ids": "3bcf2afdb32e"
  },
  "E-07": {
   "count": 2,
   "ids": "fd8ec61301ce"
  },
  "E-08": {
   "count": 5,
   "ids": "57808449b0f1"
  },
  "E-09": {
   "count": 2,
   "ids": "21fa2eb01b2e"
  },
  "E-10": {
   "count": 2,
   "ids": "469918f9ef17"
  },
  "E-11": {
   "count": 1,
   "ids": "b86b1ea11b28"
  },
  "E-12": {
   "count": 1,
   "ids": "b8d52dc8aa20"
  },
  "E-13": {
   "count": 1,
   "ids": "3bcf2afdb32e"
  },
  "E-14": {
   "count": 1,
   "ids": "080a9ed42855"
  },
  "E-15": {
   "count": 2,
   "ids": "5bf775530e2e"
  },
  "E-16": {
   "count": 1,
   "ids": "16390873ae6b"
  },
  "E-17": {
   "count": 2,
   "ids": "1e5fea1b37ba"
  },
  "E-18": {
   "count": 1,
   "ids": "525ec3b5ad9a"
  },
  "E-19": {
   "count": 1,
   "ids": "1ae3592f8248"
  },
  "E-20": {
   "count": 3,
   "ids": "32a32804800e"
  }
 },
 "ERR": {
  "A2b": "FOREIGN KEY",
  "A7c": "CHECK constraint",
  "A7d": "NOT NULL constraint",
  "A7e": "UNIQUE constraint"
 },
 "Q": {
  "A1": {
   "hash": "0e18b7436505",
   "ncols": 4,
   "nrows": 5
  },
  "A2c": {
   "hash": "db407f11d7ed",
   "ncols": 1,
   "nrows": 1
  },
  "A3v": {
   "hash": "1b5ef3d1e950",
   "ncols": 3,
   "nrows": 1
  },
  "A4a": {
   "hash": "1216b8943990",
   "ncols": 2,
   "nrows": 1
  },
  "A4v": {
   "hash": "cf0fa2da4307",
   "ncols": 2,
   "nrows": 4
  },
  "A5a": {
   "hash": "89f691b973e7",
   "ncols": 7,
   "nrows": 2
  },
  "A5v": {
   "hash": "3c764ccbffcd",
   "ncols": 1,
   "nrows": 1
  },
  "A6v1": {
   "hash": "3f66491d7b1f",
   "ncols": 3,
   "nrows": 2
  },
  "A6v2": {
   "hash": "db407f11d7ed",
   "ncols": 1,
   "nrows": 1
  },
  "A7v": {
   "hash": "4d2191dd6739",
   "ncols": 3,
   "nrows": 1
  },
  "A8c": {
   "hash": "db407f11d7ed",
   "ncols": 1,
   "nrows": 1
  },
  "A8e": {
   "hash": "bd9f136b622b",
   "ncols": 1,
   "nrows": 1
  },
  "B1": {
   "hash": "3304b97e5122",
   "ncols": 4,
   "nrows": 40
  },
  "B2": {
   "hash": "c88219a148b2",
   "ncols": 3,
   "nrows": 3
  },
  "B3": {
   "hash": "f6e5ed3f19aa",
   "ncols": 2,
   "nrows": 1
  },
  "B4": {
   "hash": "56dae39f7f96",
   "ncols": 2,
   "nrows": 3
  },
  "B5": {
   "hash": "bcfb6da2d1d9",
   "ncols": 3,
   "nrows": 6
  },
  "B6": {
   "hash": "bcfb6da2d1d9",
   "ncols": 3,
   "nrows": 6
  },
  "B7": {
   "hash": "4301525028dc",
   "ncols": 4,
   "nrows": 10
  },
  "C1": {
   "hash": "c5aa9b4a38cb",
   "ncols": 2,
   "nrows": 7
  },
  "C2": {
   "hash": "4f53cda18c2b",
   "ncols": 2,
   "nrows": 0
  },
  "C3": {
   "hash": "fa0920696726",
   "ncols": 2,
   "nrows": 3
  },
  "C4a": {
   "hash": "35032ff71bb2",
   "ncols": 2,
   "nrows": 1
  },
  "C4b": {
   "hash": "c4f517830088",
   "ncols": 2,
   "nrows": 23
  },
  "C5": {
   "hash": "eeabd8e733b4",
   "ncols": 1,
   "nrows": 1
  },
  "D1": {
   "hash": "7e6a161df64c",
   "ncols": 5,
   "nrows": 6
  },
  "D2": {
   "hash": "3828a6db8c37",
   "ncols": 3,
   "nrows": 2
  },
  "D3": {
   "hash": "e924e39b15e1",
   "ncols": 4,
   "nrows": 5
  },
  "D4": {
   "hash": "65ba1340b6b1",
   "ncols": 3,
   "nrows": 6
  },
  "D5": {
   "hash": "fea54cc9db3f",
   "ncols": 3,
   "nrows": 2
  },
  "D6": {
   "hash": "3b183a4e56d7",
   "ncols": 3,
   "nrows": 4
  }
 }
}
# END EXPECTED

PART_FILES = {
    "A": "part_a_dml.sql", "B": "part_b_joins.sql", "C": "part_c_subqueries.sql",
    "D": "part_d_aggregates.sql", "E": "part_e_checks.sql",
}
PART_TITLES = {
    "A": "DML + constraints", "B": "Joins", "C": "Subqueries", "D": "GROUP BY / HAVING / aggregates",
    "E": "Validation suite (20 checks)", "F": "Week 2 integration (qe-foundations repo)",
}
PASS, FAIL, TODO, WARN = "PASS", "FAIL", "TODO", "WARN"


def digest(obj):
    return hashlib.sha256(json.dumps(obj, default=str).encode("utf-8")).hexdigest()[:12]


def rows_digest(rows):
    return digest(lr.normalise_rows(rows))


def ids_digest(ids):
    return digest(sorted(ids, key=repr))


def line(status, name, msg=""):
    print("  [%-4s] %-6s %s" % (status, name, msg))
    return status


# ------------------------------------------------------------------------------------------- Parts A-D

def check_task_part(part, sql_dir):
    path = os.path.join(sql_dir, PART_FILES[part])
    if not os.path.isfile(path):
        return [line(FAIL, part, "file not found: %s" % path)]
    conn = lr.build_db()
    out = []
    todo_groups = set()          # task groups (A3, A4 ...) that still contain a placeholder
    for r in lr.run_file(conn, path):
        exp = EXPECTED["Q"].get(r.qid)
        expect_err = EXPECTED["ERR"].get(r.qid)
        group = re.match(r"[A-Z]\d+", r.qid).group(0)
        if r.cols == ["todo"]:
            todo_groups.add(group)
            out.append(line(TODO, r.qid, "placeholder not replaced yet"))
        elif "(given)" in r.title and group in todo_groups:
            out.append(line(TODO, r.qid, "(given) query: waiting for the %s task(s) above" % group))
        elif expect_err:
            if r.ok:
                out.append(line(FAIL, r.qid, "this statement should have been REJECTED by the database but it succeeded"))
            elif expect_err.lower() not in (r.error_msg or "").lower():
                out.append(line(FAIL, r.qid, "rejected, but for another reason: %s" % r.error_msg))
            else:
                out.append(line(PASS, r.qid, "rejected as expected (%s)" % expect_err))
        elif not r.ok:
            out.append(line(FAIL, r.qid, "%s: %s" % (r.error_type, r.error_msg)))
        elif exp is None:
            out.append(line(PASS, r.qid, "statement ran (its effect is verified by the next (given) query)"))
        elif rows_digest(r.rows) == exp["hash"]:
            out.append(line(PASS, r.qid, "%d row(s)" % len(r.rows)))
        else:
            msg = "wrong result: %d row(s) / %d column(s) returned" % (len(r.rows), len(r.cols))
            if len(r.cols) != exp["ncols"]:
                msg += "; expected %d column(s) in the order named in RETURNS" % exp["ncols"]
            elif len(r.rows) != exp["nrows"]:
                msg += "; expected a different number of rows (%s)" % ("fewer" if len(r.rows) > exp["nrows"] else "more")
            else:
                msg += "; the number of rows is right but some values differ"
            out.append(line(FAIL, r.qid, msg))
    return out


# ------------------------------------------------------------------------------------------- Part E

def check_part_e(sql_dir):
    path = os.path.join(sql_dir, PART_FILES["E"])
    if not os.path.isfile(path):
        return [line(FAIL, "E", "file not found: %s" % path)]
    with open(path, encoding="utf-8") as f:
        checks = {c.check_id: c for c in lr.parse_checks(f.read())}
    conn = lr.build_db()
    out = []
    for cid in sorted(EXPECTED["E"]):
        exp = EXPECTED["E"][cid]
        c = checks.get(cid)
        if c is None:
            out.append(line(FAIL, cid, "check not found in the file (keep the '-- @CHECK %s | ...' header line)" % cid))
            continue
        if lr.is_placeholder(c.sql):
            out.append(line(TODO, cid, "placeholder not replaced yet"))
            continue
        res = lr.execute(conn, lr.Statement(cid, "", c.sql, False))
        if not res.ok:
            out.append(line(FAIL, cid, "%s: %s" % (res.error_type, res.error_msg)))
            continue
        ids = [r[0] for r in res.rows]
        if len(ids) != exp["count"]:
            hint = "returned %d row(s); expected %s" % (len(ids), "more" if len(ids) < exp["count"] else "fewer")
            out.append(line(FAIL, cid, hint))
        elif ids_digest(ids) != exp["ids"]:
            out.append(line(FAIL, cid, "right number of rows (%d) but the wrong rows: check the first column is the PK named in 'returns'" % len(ids)))
        else:
            out.append(line(PASS, cid, "%d violation(s) found, the right ones" % len(ids)))
    extra = sorted(set(checks) - set(EXPECTED["E"]))
    if extra:
        out.append(line(WARN, "E", "extra check ids ignored by this script: %s" % ", ".join(extra)))
    return out


# ------------------------------------------------------------------------------------------- Part F

def run_report(repo, data, log_file, db_file):
    cmd = [sys.executable, "-m", "qe_foundations.report", "--data", data, "--db", db_file, "--log-file", log_file]
    env = dict(os.environ, PYTHONIOENCODING="utf-8")
    try:
        p = subprocess.run(cmd, cwd=repo, capture_output=True, text=True, timeout=120, env=env, encoding="utf-8", errors="replace")
        return p.returncode, p.stdout, p.stderr
    except subprocess.TimeoutExpired:
        return -1, "", "timed out after 120 s"


def parse_report(stdout):
    rows = {}
    for ln in stdout.splitlines():
        m = re.match(r"^\[(PASS|FAIL)\]\s+(E-\d+)\b.*?(\d+)\s+violation", ln.strip())
        if m:
            rows[m.group(2)] = (m.group(1), int(m.group(3)))
    summary = re.search(r"^DATA QUALITY: (PASS|FAIL)\b", stdout, flags=re.M)
    return rows, (summary.group(1) if summary else None)


def git(repo, *args):
    try:
        p = subprocess.run(["git", "-C", repo] + list(args), capture_output=True, text=True, timeout=30)
        return p.returncode, p.stdout.strip()
    except (OSError, subprocess.TimeoutExpired):
        return 127, ""


def word_count(path):
    with open(path, encoding="utf-8") as f:
        text = f.read()
    return len(re.findall(r"[A-Za-z']+", text)), text


def check_part_f(repo):
    out = []
    repo = os.path.abspath(repo)
    if not os.path.isdir(repo):
        return [line(FAIL, "F", "repo folder not found: %s" % repo)]
    j = lambda *p: os.path.join(repo, *p)  # noqa: E731

    # F1 structure
    needed = ["qe_foundations/__init__.py", "qe_foundations/utils", "qe_foundations/ingestion", "qe_foundations/validation",
              "qe_foundations/report.py", "tests", "data/builds.csv", "data/test_cases.csv", "data/test_runs.json",
              "data/defects.json", "data/clean", "data/malformed", "sql/schema.sql", "sql/part_e_checks.sql",
              "docs", "requirements.txt", ".gitignore", "README.md"]
    missing = [p for p in needed if not os.path.exists(j(*p.split("/")))]
    out.append(line(FAIL if missing else PASS, "F1", "missing: " + ", ".join(missing) if missing else "repo structure complete"))

    # F2 requirements/gitignore
    problems = []
    if os.path.isfile(j("requirements.txt")) and os.path.getsize(j("requirements.txt")) == 0:
        problems.append("requirements.txt is empty (add a comment line or your pinned packages)")
    if os.path.isfile(j(".gitignore")):
        gi = open(j(".gitignore"), encoding="utf-8").read()
        if not re.search(r"^\.?venv/?$|^\.venv", gi, flags=re.M):
            problems.append(".gitignore does not ignore your virtual environment folder")
        if "__pycache__" not in gi:
            problems.append(".gitignore does not ignore __pycache__")
    out.append(line(FAIL if problems else PASS, "F2", "; ".join(problems) if problems else "requirements.txt and .gitignore look right"))

    if not os.path.isfile(j("qe_foundations", "report.py")):
        out.append(line(FAIL, "F3", "cannot run the report: qe_foundations/report.py does not exist"))
        return out

    tmp = tempfile.mkdtemp(prefix="qe_check_")
    log_dirty = os.path.join(tmp, "dirty.log")

    # F3 dirty data: exit 1 + per-check counts
    rc, so, se = run_report(repo, "data", log_dirty, os.path.join(tmp, "dirty.db"))
    rows, summary = parse_report(so)
    if rc != 1 or summary != "FAIL":
        out.append(line(FAIL, "F3", "dirty data: expected exit code 1 and a 'DATA QUALITY: FAIL' line, got exit code %s, summary %s. stderr: %s"
                        % (rc, summary, se.strip()[-300:])))
    else:
        bad = []
        for cid, exp in EXPECTED["E"].items():
            got = rows.get(cid)
            if got is None:
                bad.append("%s missing" % cid)
            elif got[1] != exp["count"]:
                bad.append("%s=%d" % (cid, got[1]))
        out.append(line(FAIL if bad else PASS, "F3", ("wrong or missing per-check counts: " + ", ".join(bad[:8])) if bad
                        else "dirty data -> exit code 1, DATA QUALITY: FAIL, all 20 per-check counts correct"))

    # F4 clean data: exit 0
    rc, so, se = run_report(repo, os.path.join("data", "clean"), os.path.join(tmp, "clean.log"), os.path.join(tmp, "clean.db"))
    rows, summary = parse_report(so)
    ok = rc == 0 and summary == "PASS" and len(rows) == 20 and all(v[0] == "PASS" for v in rows.values())
    out.append(line(PASS if ok else FAIL, "F4", "clean data -> exit code 0, DATA QUALITY: PASS" if ok else
                    "clean data: expected exit code 0, 20 PASS lines and 'DATA QUALITY: PASS'; got exit code %s, %d line(s), summary %s. stderr: %s"
                    % (rc, len(rows), summary, se.strip()[-300:])))

    # F5 malformed data: exit 2 without a traceback
    log_bad = os.path.join(tmp, "bad.log")
    rc, so, se = run_report(repo, os.path.join("data", "malformed"), log_bad, os.path.join(tmp, "bad.db"))
    if rc == 2 and "Traceback" not in so + se and se.strip():
        out.append(line(PASS, "F5", "malformed JSON -> exit code 2, readable message, no traceback"))
    else:
        out.append(line(FAIL, "F5", "malformed data: expected exit code 2, a one-line error on stderr and NO traceback; got exit code %s%s"
                        % (rc, ", traceback printed" if "Traceback" in so + se else "")))

    # F6 logging
    lp = []
    if not os.path.isfile(log_dirty):
        lp.append("--log-file was not honoured (no log file written)")
    else:
        text = open(log_dirty, encoding="utf-8", errors="replace").read()
        miss = [c for c in EXPECTED["E"] if c not in text]
        if miss:
            lp.append("log does not mention every check id (missing %s...)" % ", ".join(miss[:3]))
        if not re.search(r"\b(WARNING|ERROR)\b", text):
            lp.append("failed checks should be logged at WARNING (or ERROR) level")
    if os.path.isfile(log_bad):
        if "ERROR" not in open(log_bad, encoding="utf-8", errors="replace").read():
            lp.append("the ingestion failure was not logged at ERROR level")
    else:
        lp.append("no log written for the malformed run")
    out.append(line(FAIL if lp else PASS, "F6", "; ".join(lp) if lp else "log file written; checks and the ingestion error are logged"))

    # F7 unit tests
    p = subprocess.run([sys.executable, "-m", "unittest", "discover", "-s", "tests", "-t", ".", "-v"], cwd=repo,
                       capture_output=True, text=True, timeout=180, encoding="utf-8", errors="replace")
    ran = re.search(r"Ran (\d+) tests?", p.stderr)
    n = int(ran.group(1)) if ran else 0
    sql_tests = [f for f in os.listdir(j("tests")) if f.startswith("test_") and "sql" in f] if os.path.isdir(j("tests")) else []
    if p.returncode != 0 or n < 5:
        out.append(line(FAIL, "F7", "unittest: exit code %s, %d test(s) run (need all passing and at least 5 in total). Tail: %s"
                        % (p.returncode, n, p.stderr.strip()[-250:])))
    elif not sql_tests:
        out.append(line(FAIL, "F7", "tests pass (%d) but there is no tests/test_*sql*.py file for the new SQL-check code" % n))
    else:
        out.append(line(PASS, "F7", "%d unit tests pass (python -m unittest discover -s tests -t .)" % n))

    # F8 findings + reflection documents
    fp, rp = j("docs", "DATA_QUALITY_FINDINGS.md"), j("docs", "WEEK2_REFLECTION.md")
    if not os.path.isfile(fp):
        out.append(line(FAIL, "F8", "docs/DATA_QUALITY_FINDINGS.md not found"))
    else:
        _, text = word_count(fp)
        ids = set(re.findall(r"E-\d\d", text))
        out.append(line(FAIL if len(ids) < 18 or "TODO" in text else PASS, "F8",
                        "findings document covers %d of 20 check ids%s" % (len(ids), " and still contains TODO" if "TODO" in text else "")))
    if not os.path.isfile(rp):
        out.append(line(FAIL, "F9", "docs/WEEK2_REFLECTION.md not found"))
    else:
        words, text = word_count(rp)
        bad = []
        if words < 150:
            bad.append("only %d words (aim for 150-300)" % words)
        if "TODO" in text or "<!--" in text:
            bad.append("template prompts or TODO markers still present")
        out.append(line(FAIL if bad else PASS, "F9", "; ".join(bad) if bad else "reflection written (%d words); quality is graded by the instructor" % words))

    # F10 git
    rc, top = git(repo, "rev-parse", "--show-toplevel")
    if rc != 0:
        out.append(line(FAIL, "F10", "not a git repository"))
    else:
        rc_t, tag = git(repo, "rev-parse", "-q", "--verify", "refs/tags/week2-complete^{commit}")
        _, head = git(repo, "rev-parse", "HEAD")
        _, dirty = git(repo, "status", "--porcelain")
        msgs, st = [], PASS
        if rc_t != 0:
            msgs.append("tag week2-complete not found (git tag week2-complete)")
            st = FAIL
        elif tag != head:
            msgs.append("tag week2-complete is not on the latest commit (move it: git tag -f week2-complete)")
            st = FAIL
        if dirty:
            msgs.append("uncommitted changes in the working tree")
            st = FAIL
        out.append(line(st, "F10", "; ".join(msgs) if msgs else "tag week2-complete is on the latest commit, working tree clean"))
        rc_r, remote = git(repo, "remote")
        if rc_r == 0 and remote:
            rc_l, ls = git(repo, "ls-remote", "--tags", "origin", "week2-complete")
            out.append(line(PASS if (rc_l == 0 and ls) else WARN, "F11",
                            "tag is on the remote" if (rc_l == 0 and ls) else "could not confirm the tag on the remote: run  git push origin main --tags"))
        else:
            out.append(line(WARN, "F11", "no remote configured: add one and push (git remote add origin <url>; git push -u origin main --tags)"))
    return out


# ------------------------------------------------------------------------------------------- main

def main():
    ap = argparse.ArgumentParser(description="Self-check for the 5-friday exercise.")
    ap.add_argument("--sql-dir", default=os.path.join(HERE, "sql"), help="folder with your part_*.sql files (default: ./sql)")
    ap.add_argument("--repo", help="path to your qe-foundations repo (enables Part F)")
    ap.add_argument("--part", choices=list("ABCDEF"), help="check one part only")
    args = ap.parse_args()

    totals = {}
    parts = [args.part] if args.part else list("ABCDE") + (["F"] if args.repo else [])
    if args.part == "F" and not args.repo:
        sys.exit("--part F needs --repo PATH")
    print("SQLite library version: %s   Python %s" % (lr.sqlite3.sqlite_version, sys.version.split()[0]))
    for part in parts:
        print("\nPart %s - %s" % (part, PART_TITLES[part]))
        if part == "E":
            res = check_part_e(args.sql_dir)
        elif part == "F":
            res = check_part_f(args.repo)
        else:
            res = check_task_part(part, args.sql_dir)
        totals[part] = res
    print("\n" + "=" * 70)
    print("SUMMARY")
    ok = True
    for part, res in totals.items():
        n = len(res)
        p = res.count(PASS)
        t = res.count(TODO)
        f = res.count(FAIL)
        w = res.count(WARN)
        print("  Part %s  %2d/%2d PASS   %d FAIL   %d TODO%s" % (part, p, n - w, f, t, ("   %d warning(s)" % w) if w else ""))
        ok = ok and f == 0 and t == 0
    if not args.repo and not args.part:
        print("  Part F  not checked (add --repo PATH to your qe-foundations repo)")
    print("RESULT:", "ALL CHECKS PASSED" if ok else "NOT DONE YET (fix FAIL / TODO lines above)")
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
