#!/usr/bin/env python3
"""check_exercise.py -- self-check for the Thursday pair-programming exercise.

Copy this file to the ROOT of your qe-foundations repository, then run:

    python check_exercise.py              (Windows: py check_exercise.py)
    python check_exercise.py --verbose    (show the details of every check)
    python check_exercise.py --skip-git   (skip the Git collaboration section)

It checks, in order:   1 Files   2 SQL rules   3 Python runner   4 Unit tests
                       5 Docs     6 Git collaboration

Result words:  PASS = good   WARN = fix it if you can, not a blocker
               FAIL = must fix before you submit   SKIP = not applicable

It uses only the Python standard library, never changes your files, and runs the
rules against its OWN copy of the seed data, so a green result means your SQL really
finds the planted defects. (It tells you HOW MANY rows a rule should return, never
WHICH ones -- finding them is the exercise.)

Exit code: 0 = no FAIL, 1 = at least one FAIL.
"""
import argparse
import hashlib
import json
import os
import re
import sqlite3
import subprocess
import sys
import tempfile
from pathlib import Path

# rule id -> (expected number of rows, fingerprint of the expected run_ids, common trap)
EXPECTED = {
    'R-01': (3, 'ba93ff443c98b575', "'Missing' is NULL, but also '' and a space-only string."),
    'R-02': (2, '02dea5338884a671', "Do not re-flag NULL/blank rows (that is R-01's job); the pattern is '%@%.%'."),
    'R-03': (4, 'e6491ecdcd85f9a9', 'NOT IN skips NULL rows, so add IS NULL. Matching is exact: case and trailing spaces count.'),
    'R-04': (2, '625480aa1b99f707', 'NULL must be reported; 0 ms is LEGAL (a SKIPPED run), so use < 0, not <= 0.'),
    'R-05': (2, '824fb0fef836b10c', 'Strictly more than 600000; exactly 600000 is legal.'),
    'R-06': (2, 'deb0ab8afbf64f94', 'BETWEEN is inclusive (3 is legal); NULL needs its own IS NULL.'),
    'R-07': (3, '9001be04de87a8f5', 'Exact, case-sensitive list; NULL needs its own IS NULL.'),
    'R-08': (3, 'd6f5e1d00e794ea8', 'Compare each of the THREE columns with its TRIM().'),
    'R-09': (3, '6963511adde8e8d4', 'Check BOTH columns, for NULL and for shape; the LIKE pattern is 4-2-2 characters, a SPACE, then 2-2-2.'),
    'R-10': (2, 'bab4b81623ae18e9', "Two conditions joined with OR; 'future' means later than date('now')."),
    'R-11': (3, '0db805d8a814aee1', 'Use parentheses: (FAILED/ERROR with NULL or blank message) OR (PASSED with any message). SKIPPED may keep a message.'),
    'R-12': (4, 'a6de1413e158cba4', 'In SQLite, LIKE ignores letter case: also compare build_id with UPPER(build_id); NULL too.'),
    'E-01': (1, '4f6533047a577021', 'Put EVERY expected value in the WHERE clause; exactly one row must come back.'),
    'E-02': (1, 'ef6ad2aa85656e43', "environment = 'QA' AND status = 'FAILED' (exact), ORDER BY started_at DESC, LIMIT 1."),
    'S-01': (32, '7952bfbf5a387db3', 'One OR chain; wrap each sub-rule in parentheses; each run_id appears once.'),
    'S-02': (2, 'c228f97df7b86d64', 'Look for two rows with the same test_name, environment, build_id and started_at.'),
    'S-03': (3, '55dc07587f671ca4', 'Filter to plausible durations first (BETWEEN 0 AND 600000), then ORDER BY duration_ms DESC LIMIT 3.'),
}

REQUIRED_RULES = [f"R-{n:02d}" for n in range(1, 13)] + ["E-01", "E-02"]
STRETCH_RULES = ["S-01", "S-02", "S-03"]
EXPECT_ROWS = {rid: (0 if rid.startswith("R-") else 1) for rid in REQUIRED_RULES}

FILES = [
    "sql/validation_queries.sql",
    "qe_foundations/data/test_runs_schema.sql",
    "qe_foundations/data/test_runs_seed.sql",
    "qe_foundations/validation/__init__.py",
    "qe_foundations/validation/__main__.py",
    "qe_foundations/validation/exceptions.py",
    "qe_foundations/validation/runner.py",
    "qe_foundations/tests/test_validation.py",
    "qe_foundations/docs/defect_checklist.md",
    "qe_foundations/docs/defect_reports.md",
    "qe_foundations/docs/pairing_log.md",
    "qe_foundations/docs/retrospective.md",
]

results = []          # (section, status, title, detail)


def add(section, status, title, detail=""):
    results.append((section, status, title, detail))


def fingerprint(rule_id, ids):
    text = rule_id + ":" + ",".join(str(i) for i in sorted(ids))
    return hashlib.sha256(text.encode()).hexdigest()[:16]


def run(cmd, cwd, timeout=60, env=None):
    e = dict(os.environ)
    e["PYTHONPATH"] = str(cwd) + os.pathsep + e.get("PYTHONPATH", "")
    e["PYTHONIOENCODING"] = "utf-8"
    if env:
        e.update(env)
    return subprocess.run(cmd, cwd=str(cwd), capture_output=True, text=True,
                          timeout=timeout, env=e, encoding="utf-8", errors="replace")


# ------------------------------------------------------------------ 1 files
def check_files(repo):
    s = "1 Files"
    missing = [f for f in FILES if not (repo / f).is_file()]
    if missing:
        add(s, "FAIL", f"{len(missing)} required file(s) missing", "\n".join(missing))
    else:
        add(s, "PASS", "all required files exist")
    gi = repo / ".gitignore"
    text = gi.read_text(encoding="utf-8", errors="replace") if gi.is_file() else ""
    lacking = [p for p in ("logs/", "*.db", "__pycache__") if p not in text]
    if lacking:
        add(s, "WARN", ".gitignore does not ignore: " + ", ".join(lacking),
            "Generated files (logs, .db files, caches) do not belong in Git.")
    else:
        add(s, "PASS", ".gitignore ignores logs, databases and caches")


# ------------------------------------------------------------------ 2 sql
RULE_HEADER = re.compile(r"^--\s*@rule\s+(\S+)\s*\|\s*([^|]*?)\s*\|\s*(.*?)\s*$")
EXPECT_LINE = re.compile(r"^--\s*@expect\s+(\d+|any)\s*$", re.I)


def parse_rules(path):
    rules, cur = {}, None
    for line in path.read_text(encoding="utf-8", errors="replace").splitlines():
        m = RULE_HEADER.match(line.strip())
        if m:
            cur = {"expect": 0, "sql": []}
            rules[m.group(1)] = cur
            continue
        if cur is None:
            continue
        e = EXPECT_LINE.match(line.strip())
        if e:
            cur["expect"] = None if e.group(1).lower() == "any" else int(e.group(1))
        elif not line.strip().startswith("--"):
            cur["sql"].append(line)
    for r in rules.values():
        r["sql"] = "\n".join(r["sql"]).strip()
    return rules


def build_db(repo):
    conn = sqlite3.connect(":memory:")
    for name in ("test_runs_schema.sql", "test_runs_seed.sql"):
        conn.executescript((repo / "qe_foundations" / "data" / name).read_text(encoding="utf-8"))
    return conn


FORBIDDEN_WRITE = re.compile(r"\b(INSERT|UPDATE|DELETE|DROP|ALTER|CREATE|REPLACE\s+INTO|PRAGMA|ATTACH)\b", re.I)
FRIDAY = re.compile(r"\b(JOIN|GROUP\s+BY|HAVING|UNION|INTERSECT|EXCEPT)\b", re.I)


def check_sql(repo, verbose):
    s = "2 SQL rules"
    path = repo / "sql" / "validation_queries.sql"
    if not path.is_file():
        add(s, "FAIL", "sql/validation_queries.sql not found")
        return {}
    rules = parse_rules(path)
    try:
        conn = build_db(repo)
    except (OSError, sqlite3.Error) as exc:
        add(s, "FAIL", "could not load the seed data", str(exc))
        return {}
    actual = {}
    for rid in REQUIRED_RULES + STRETCH_RULES:
        stretch = rid.startswith("S-")
        if rid not in rules:
            if stretch:
                add(s, "SKIP", f"{rid} stretch rule not attempted")
            else:
                add(s, "FAIL", f"{rid}: rule header missing", "Keep the '-- @rule ...' header lines of the starter file.")
            continue
        rule = rules[rid]
        sql = rule["sql"]
        if not stretch and rule["expect"] != EXPECT_ROWS[rid]:
            add(s, "FAIL", f"{rid}: '-- @expect' was changed to {rule['expect']}",
                f"Leave it at {EXPECT_ROWS[rid]}; make the QUERY right instead.")
            continue
        if not sql:
            add(s, "FAIL", f"{rid}: no SQL under the header")
            continue
        body = re.sub(r"'[^']*'", "''", sql)
        if FORBIDDEN_WRITE.search(body):
            add(s, "FAIL", f"{rid}: only read-only SELECT statements are allowed")
            continue
        if sql.rstrip().rstrip(";").count(";"):
            add(s, "FAIL", f"{rid}: more than one statement; use exactly one SELECT")
            continue
        try:
            cur = conn.execute(sql)
            cols = [d[0] for d in cur.description]
            rows = cur.fetchall()
        except sqlite3.Error as exc:
            add(s, "FAIL", f"{rid}: SQL error: {exc}",
                "Read the message, find the clause it points at, fix, re-run.")
            continue
        if cols[0].lower() != "run_id":
            add(s, "FAIL", f"{rid}: the FIRST selected column must be run_id (yours is '{cols[0]}')")
            continue
        ids = [r[0] for r in rows]
        actual[rid] = set(ids)
        notes = []
        if FRIDAY.search(body) or len(re.findall(r"\bSELECT\b", body, re.I)) > 1:
            notes.append("uses a Friday feature (JOIN/GROUP BY/HAVING/UNION/sub-query); Thursday's toolkit is enough")
        exp_count, fp, trap = EXPECTED[rid]
        if len(ids) == exp_count and fingerprint(rid, ids) == fp:
            add(s, "PASS", f"{rid}: returns exactly the expected {exp_count} row(s)")
        elif not ids:
            add(s, "FAIL", f"{rid}: returns 0 rows but {exp_count} expected -- a FALSE PASS?", trap)
        elif len(ids) > exp_count:
            add(s, "FAIL", f"{rid}: returns {len(ids)} row(s), expected {exp_count} -- too broad (false alarms)", trap)
        elif len(ids) < exp_count:
            add(s, "FAIL", f"{rid}: returns {len(ids)} row(s), expected {exp_count} -- too narrow (missed defects)", trap)
        else:
            add(s, "FAIL", f"{rid}: right number of rows ({exp_count}) but not the right rows", trap)
        if notes:
            add(s, "WARN", f"{rid}: " + notes[0])
    return actual


# ------------------------------------------------------------------ 3 runner
PROBE = r'''
import json, sqlite3, inspect
out = {}
try:
    from qe_foundations.validation import runner
    from qe_foundations.validation.exceptions import ValidationFailedError as E
except Exception as exc:
    print(json.dumps({"import_error": repr(exc)})); raise SystemExit
out["is_exception"] = isinstance(E, type) and issubclass(E, Exception) and E is not Exception
conn = runner.connect(":memory:"); runner.load_seed(conn)
def rule(sql, expect=0, rid="T-99"):
    return runner.Rule(rid, "Test", "probe rule", sql, expect)
def attempt(r):
    try:
        rows = runner.run_rule(conn, r); return {"raised": False, "rows": [list(x) for x in rows]}
    except E as exc:
        return {"raised": True, "rule_id": getattr(exc, "rule_id", None), "rows": [list(x) for x in getattr(exc, "rows", [])] if hasattr(exc, "rows") else None, "has_desc": hasattr(exc, "description"), "msg": str(exc)}
    except Exception as exc:
        return {"other": repr(exc)}
out["clean"] = attempt(rule("SELECT run_id FROM test_runs WHERE run_id = -1"))
out["dirty"] = attempt(rule("SELECT run_id FROM test_runs WHERE run_id = 5003"))
out["expect_missing"] = attempt(rule("SELECT run_id FROM test_runs WHERE run_id = -1", expect=1))
out["expect_ok"] = attempt(rule("SELECT run_id FROM test_runs WHERE run_id = 5001", expect=1))
out["info"] = attempt(rule("SELECT run_id FROM test_runs WHERE run_id = 5003", expect=None))
import tempfile, pathlib, logging
try:
    p = pathlib.Path(tempfile.mkdtemp()) / "x" / "probe.log"
    runner.setup_logging(p); lg = runner.setup_logging(p)
    out["handlers_after_two_calls"] = len(lg.handlers)
    for h in list(lg.handlers):
        h.close(); lg.removeHandler(h)
except Exception as exc:
    out["handlers_after_two_calls"] = repr(exc)
print(json.dumps(out))
'''


def check_runner(repo, actual, verbose):
    s = "3 Python runner"
    try:
        p = run([sys.executable, "-c", PROBE], repo)
    except subprocess.TimeoutExpired:
        add(s, "FAIL", "probe timed out"); return
    try:
        info = json.loads(p.stdout.strip().splitlines()[-1])
    except (ValueError, IndexError):
        add(s, "FAIL", "could not import/run your runner", (p.stderr or p.stdout).strip()[-600:])
        return
    if "import_error" in info:
        add(s, "FAIL", "could not import your runner/exception", info["import_error"])
        return
    # custom exception
    if info["is_exception"]:
        add(s, "PASS", "ValidationFailedError is a custom Exception subclass")
    else:
        add(s, "FAIL", "ValidationFailedError must be a subclass of Exception")
    d = info["dirty"]
    if "other" in d:
        add(s, "FAIL", "run_rule: " + d["other"], "Implement run_rule (and the exception's __init__(rule, rows)).")
    elif not d.get("raised"):
        add(s, "FAIL", "run_rule did not raise ValidationFailedError for a rule that returned unexpected rows")
    else:
        ok = d.get("rule_id") == "T-99" and d.get("rows") == [[5003]] and d.get("has_desc") and "T-99" in d.get("msg", "")
        if ok:
            add(s, "PASS", "ValidationFailedError carries rule_id, description, rows and a message naming the rule")
        else:
            add(s, "FAIL", "ValidationFailedError needs .rule_id, .description, .rows and a message that names the rule",
                f"got rule_id={d.get('rule_id')!r}, rows={d.get('rows')!r}, message={d.get('msg')!r}")
    c, em, eo, inf = info["clean"], info["expect_missing"], info["expect_ok"], info["info"]
    if c.get("raised") is False and c.get("rows") == []:
        add(s, "PASS", "run_rule returns normally when a violation query finds nothing")
    else:
        add(s, "FAIL", "run_rule must return the (empty) rows when a violation query returns 0 rows", str(c))
    if em.get("raised") and eo.get("raised") is False:
        add(s, "PASS", "expectation rules: PASS with the expected row count, raise when the row is missing")
    else:
        add(s, "FAIL", "expectation rule logic wrong (expect=1: 1 row passes, 0 rows must raise)", f"{em} / {eo}")
    if inf.get("raised") is False:
        add(s, "PASS", "informational rules (expect=None) never raise")
    else:
        add(s, "FAIL", "a rule with expect=None is informational and must never raise", str(inf))

    # command line
    tmp = Path(tempfile.mkdtemp(prefix="qe_check_"))
    logf = tmp / "check.log"
    try:
        p = run([sys.executable, "-m", "qe_foundations.validation", "--allow-failures", "--log-file", str(logf)], repo)
    except subprocess.TimeoutExpired:
        add(s, "FAIL", "the runner did not finish within 60 s"); return
    out = p.stdout
    if p.returncode != 0:
        add(s, "FAIL", f"python -m qe_foundations.validation --allow-failures exited with code {p.returncode}",
            (p.stderr or out).strip()[-700:])
        return
    lines = {}
    for ln in out.splitlines():
        m = re.match(r"^(PASS|FAIL|INFO)\s+([A-Z]-\d\d)\b", ln)
        if m:
            lines[m.group(2)] = m.group(1)
    missing = [r for r in REQUIRED_RULES if r not in lines]
    if missing:
        add(s, "FAIL", "no 'PASS/FAIL  <rule-id>' line printed for: " + ", ".join(missing),
            "Each line must start with PASS, FAIL or INFO, then the rule id.")
    else:
        add(s, "PASS", "runner prints one PASS/FAIL line per required rule")
        wrong = []
        for rid in REQUIRED_RULES:
            if rid in actual:
                want = "PASS" if len(actual[rid]) == EXPECT_ROWS[rid] else "FAIL"
                if lines[rid] != want:
                    wrong.append(f"{rid} printed {lines[rid]}, its query result means {want}")
        if wrong:
            add(s, "FAIL", "PASS/FAIL lines disagree with the query results", "\n".join(wrong))
        else:
            add(s, "PASS", "printed PASS/FAIL agrees with what each query returns")
    ev = [ln for ln in out.splitlines() if ln.startswith(" ") and ln.strip()]
    if any(v == "FAIL" for v in lines.values()):
        if ev:
            add(s, "PASS", "FAIL lines are followed by the evidence rows")
        else:
            add(s, "WARN", "no evidence rows printed under the FAIL lines (indent each violating row)")
    # exit code without --allow-failures
    if any(v == "FAIL" for v in lines.values()):
        p2 = run([sys.executable, "-m", "qe_foundations.validation", "--log-file", str(tmp / "c2.log")], repo)
        if p2.returncode == 1:
            add(s, "PASS", "exit code is 1 when a rule fails (and 0 with --allow-failures)")
        else:
            add(s, "FAIL", f"exit code should be 1 when a rule FAILs (got {p2.returncode})")
    # logging
    if logf.is_file():
        log = logf.read_text(encoding="utf-8", errors="replace")
        ids_in_log = [r for r in REQUIRED_RULES if r in log]
        levels = {lv for lv in ("DEBUG", "INFO", "WARNING") if lv in log}
        if len(ids_in_log) == len(REQUIRED_RULES) and {"INFO", "WARNING"} <= levels:
            add(s, "PASS", "log file written: every rule logged, INFO for passes, WARNING for failures")
        else:
            add(s, "FAIL", "log file incomplete",
                f"rules in log: {len(ids_in_log)}/{len(REQUIRED_RULES)}; levels seen: {sorted(levels)} "
                "(log INFO for PASS, WARNING for FAIL)")
        if "DEBUG" in levels:
            add(s, "PASS", "file handler records DEBUG detail")
        else:
            add(s, "WARN", "no DEBUG lines in the log file (log each query before running it)")
        if info.get("handlers_after_two_calls") == 2:
            add(s, "PASS", "setup_logging() is safe to call twice (no duplicate handlers)")
        else:
            add(s, "FAIL", "setup_logging() added handlers twice (duplicate log lines: Wednesday pitfall)",
                f"handlers after two calls: {info.get('handlers_after_two_calls')} (expected 2: console + file)")
    else:
        add(s, "FAIL", "no log file written to the --log-file path", "setup_logging must create the folder and the file handler.")
    src = (repo / "qe_foundations/validation/runner.py").read_text(encoding="utf-8", errors="replace")
    if "except Exception" in src and "raise" not in src.split("except Exception", 1)[1][:400]:
        add(s, "WARN", "run_all swallows unexpected exceptions; a broken query is not 'bad data' -- log and re-raise")


# ------------------------------------------------------------------ 4 unit tests
def check_tests(repo):
    s = "4 Unit tests"
    tf = repo / "qe_foundations/tests/test_validation.py"
    try:
        p = run([sys.executable, "-m", "unittest", "qe_foundations.tests.test_validation"], repo)
    except subprocess.TimeoutExpired:
        add(s, "FAIL", "tests did not finish within 60 s"); return
    err = p.stderr
    m = re.search(r"Ran (\d+) tests?", err)
    n = int(m.group(1)) if m else 0
    if p.returncode == 0 and n >= 5:
        add(s, "PASS", f"{n} unittest tests run and all pass")
    elif p.returncode == 0:
        add(s, "FAIL", f"only {n} test(s); at least 5 are required")
    else:
        summary = re.findall(r"^(?:FAIL|ERROR): .*", err, re.M)[:6]
        add(s, "FAIL", f"unittest reports failures ({n} ran)", "\n".join(summary) or err.strip()[-500:])
    text = tf.read_text(encoding="utf-8", errors="replace") if tf.is_file() else ""
    raw = text
    text = "\n".join(ln for ln in text.splitlines() if not ln.strip().startswith("#"))   # ignore comments
    if re.search(r"assertRaises\(\s*ValidationFailedError", text):
        add(s, "PASS", "a test covers the custom exception (assertRaises)")
    else:
        add(s, "FAIL", "no test uses assertRaises with ValidationFailedError")
    if re.search(r"\b50\d\d\b", text):
        add(s, "PASS", "a test checks specific planted defects (run_ids)")
    else:
        add(s, "WARN", "no test mentions a specific planted run_id; prove a rule catches a KNOWN bad row")
    if 'self.fail("TODO' in raw:
        add(s, "FAIL", "TODO stub tests are still in the file")


# ------------------------------------------------------------------ 5 docs
def body_words(text):
    text = re.sub(r"<!--.*?-->", "", text, flags=re.S)
    text = re.sub(r"^#+.*$", "", text, flags=re.M)
    return len(re.findall(r"[A-Za-z]{2,}", text))


def check_docs(repo, actual):
    s = "5 Docs"
    d = repo / "qe_foundations" / "docs"

    def read(name):
        f = d / name
        return f.read_text(encoding="utf-8", errors="replace") if f.is_file() else None

    # pairing log
    t = read("pairing_log.md")
    if t is None:
        add(s, "FAIL", "pairing_log.md missing")
    else:
        lines = t.splitlines()
        start = next((i for i, ln in enumerate(lines) if re.match(r"^\|\s*Block\s*\|", ln.strip())), None)
        filled = 0
        if start is not None:
            for ln in lines[start + 2:]:                 # skip header + separator
                if not ln.strip().startswith("|"):
                    break
                cells = [c.strip() for c in ln.strip().strip("|").split("|")]
                if sum(1 for c in cells if c and not re.fullmatch(r"[_.\-\s]*", c)) >= 4:
                    filled += 1
        if filled >= 5:
            add(s, "PASS", f"pairing log: {filled} swap blocks recorded")
        elif filled >= 3:
            add(s, "WARN", f"pairing log: only {filled} filled rows; a 3-hour session has 5 driving blocks")
        else:
            add(s, "FAIL", f"pairing log not filled in ({filled} row(s) complete)")
    # retrospective
    t = read("retrospective.md")
    if t is None:
        add(s, "FAIL", "retrospective.md missing")
    else:
        clean = re.sub(r"<!--.*?-->", "", t, flags=re.S)
        sections = re.split(r"^##\s+", clean, flags=re.M)[1:]
        thin = [sec.splitlines()[0].strip() for sec in sections if body_words("\n".join(sec.splitlines()[1:])) < 12]
        if len(sections) < 5:
            add(s, "FAIL", f"retrospective has {len(sections)} '##' sections; keep the template's sections")
        elif thin:
            add(s, "FAIL", f"{len(thin)} retrospective section(s) still empty or too short", "\n".join(thin))
        elif body_words(clean) < 200:
            add(s, "WARN", "retrospective is under ~200 words; say something specific")
        else:
            add(s, "PASS", "retrospective complete")
    # checklist
    t = read("defect_checklist.md")
    if t is None:
        add(s, "FAIL", "defect_checklist.md missing")
    else:
        found = {}
        for ln in t.splitlines():
            m = re.match(r"^\|\s*(R-\d\d)\s*\|([^|]*)\|", ln)
            if m:
                found[m.group(1)] = {int(x) for x in re.findall(r"\b\d{4}\b", m.group(2))}
        empty = [r for r in REQUIRED_RULES if r.startswith("R-") and not found.get(r)]
        if empty:
            add(s, "FAIL", f"checklist has no run_ids for: {', '.join(empty)}",
                "Fill 'Defects found (run_ids)' for every rule from your query results.")
        else:
            mism = [r for r in found if r in actual and found[r] != actual[r]]
            if mism:
                add(s, "WARN", "checklist and query results differ for: " + ", ".join(sorted(mism)),
                    "Update whichever is stale.")
            else:
                add(s, "PASS", "defect checklist filled in and consistent with your query results")
    # defect reports
    t = read("defect_reports.md")
    if t is None:
        add(s, "FAIL", "defect_reports.md missing")
    else:
        n_title = len(re.findall(r"(?im)^\W*title\W*:", t))
        n_sel = len(re.findall(r"(?i)\bSELECT\b", re.sub(r"<!--.*?-->", "", t, flags=re.S)))
        if n_title >= 2 and n_sel >= 2 and body_words(t) >= 80:
            add(s, "PASS", f"{n_title} defect reports with reproducing queries")
        else:
            add(s, "FAIL", "defect_reports.md needs 2 reports, each with a Title, the SQL query and evidence",
                f"found {n_title} title(s), {n_sel} SELECT query/queries")


# ------------------------------------------------------------------ 6 git
def git(repo, *args):
    p = subprocess.run(["git", *args], cwd=str(repo), capture_output=True, text=True,
                       encoding="utf-8", errors="replace")
    return p.returncode, p.stdout.strip()


def check_git(repo):
    s = "6 Git"
    try:
        rc, _ = git(repo, "rev-parse", "--is-inside-work-tree")
    except OSError:
        add(s, "SKIP", "git is not installed or not on PATH"); return
    if rc != 0:
        add(s, "SKIP", "not a Git repository (run this inside your qe-foundations clone)"); return
    _, branch = git(repo, "rev-parse", "--abbrev-ref", "HEAD")
    if branch in ("main", "master", "HEAD"):
        add(s, "FAIL", f"you are on '{branch}'; work on a feature branch (e.g. feature/sql-validation-<names>)")
    elif branch.startswith(("feature/", "feat/")):
        add(s, "PASS", f"on feature branch '{branch}'")
    else:
        add(s, "WARN", f"branch '{branch}' works, but name it feature/<topic> by convention")
    base = None
    for cand in ("main", "master", "origin/main", "origin/master"):
        if git(repo, "rev-parse", "--verify", "--quiet", cand)[0] == 0 and cand != branch:
            base = cand; break
    spec = f"{base}..HEAD" if base else "HEAD"
    _, log = git(repo, "log", spec, "--format=%an%x09%s")
    commits = [ln.split("\t", 1) for ln in log.splitlines() if ln.strip()]
    authors = {}
    for a, _ in commits:
        authors[a] = authors.get(a, 0) + 1
    scope = f"on this branch (vs {base})" if base else "in the history"
    if len(commits) >= 6:
        add(s, "PASS", f"{len(commits)} commits {scope}")
    elif len(commits) >= 3:
        add(s, "WARN", f"only {len(commits)} commits {scope}; commit at least at every swap (>= 6)")
    else:
        add(s, "FAIL", f"only {len(commits)} commit(s) {scope}; commit small and often")
    if len(authors) >= 2:
        thin = [a for a, c in authors.items() if c < 2]
        if thin:
            add(s, "WARN", "both partners committed, but " + ", ".join(thin) + " has only 1 commit", str(authors))
        else:
            add(s, "PASS", "both partners committed under their own names", str(authors))
    else:
        add(s, "FAIL", "only one commit author; each partner must commit with their own name",
            "Set  git config user.name  on each laptop (or use  git commit --author=...).")
    weak = [m for _, m in commits if len(m.strip()) < 12 or m.strip().lower() in ("update", "fix", "wip", "changes", "stuff", "asdf")]
    if commits and len(weak) > len(commits) / 3:
        add(s, "WARN", f"{len(weak)} commit message(s) are vague ('update', 'wip'...): say what and why")
    elif commits:
        add(s, "PASS", "commit messages are descriptive")
    _, status = git(repo, "status", "--porcelain")
    add(s, "PASS" if not status else "WARN", "working tree clean" if not status else "uncommitted changes in the working tree",
        status[:300])
    _, remotes = git(repo, "remote")
    if not remotes:
        add(s, "WARN", "no remote configured; the pair needs a shared remote (GitHub or a local bare repo)")
    else:
        rc, ahead = git(repo, "rev-list", "--count", "@{u}..HEAD")
        if rc != 0:
            add(s, "WARN", "branch has no upstream: push it with  git push -u origin " + branch)
        elif ahead != "0":
            add(s, "WARN", f"{ahead} commit(s) not pushed yet")
        else:
            add(s, "PASS", "branch is pushed and up to date with its upstream")
    _, files = git(repo, "ls-files")
    junk = [f for f in files.splitlines() if f.endswith((".db", ".sqlite", ".log", ".pyc")) or "__pycache__/" in f]
    add(s, "PASS" if not junk else "FAIL", "no generated files tracked" if not junk else "generated files are tracked in Git",
        "\n".join(junk[:8]))
    rc, hits = git(repo, "grep", "-l", "-E", "^(<<<<<<< |>>>>>>> )")
    add(s, "FAIL" if hits else "PASS", "merge-conflict markers left in files" if hits else "no merge-conflict markers", hits[:300])


# ------------------------------------------------------------------ main
def main():
    ap = argparse.ArgumentParser(description="Self-check for the Thursday pair exercise.")
    ap.add_argument("--repo", default=str(Path(__file__).resolve().parent), help="repository root (default: this file's folder)")
    ap.add_argument("--verbose", action="store_true", help="show details for every check")
    ap.add_argument("--skip-git", action="store_true")
    args = ap.parse_args()
    repo = Path(args.repo).resolve()

    check_files(repo)
    actual = check_sql(repo, args.verbose)
    if (repo / "qe_foundations/validation/runner.py").is_file():
        try:
            check_runner(repo, actual, args.verbose)
        except Exception as exc:                     # the check must never crash on trainee code
            add("3 Python runner", "FAIL", "runner check crashed", repr(exc))
    else:
        add("3 Python runner", "FAIL", "runner.py missing")
    check_tests(repo) if (repo / "qe_foundations/tests/test_validation.py").is_file() else add("4 Unit tests", "FAIL", "test_validation.py missing")
    check_docs(repo, actual)
    if args.skip_git:
        add("6 Git", "SKIP", "skipped (--skip-git)")
    else:
        check_git(repo)

    print(f"\nThursday pair exercise -- self-check of {repo}\n")
    section = None
    for sec, status, title, detail in results:
        if sec != section:
            section = sec
            print(f"== {sec}")
        print(f"  [{status}] {title}")
        if detail and (args.verbose or status in ("FAIL", "WARN")):
            for ln in str(detail).splitlines()[:8]:
                print(f"         {ln}")
    tally = {k: sum(1 for r in results if r[1] == k) for k in ("PASS", "WARN", "FAIL", "SKIP")}
    print(f"\nPASS {tally['PASS']}   WARN {tally['WARN']}   FAIL {tally['FAIL']}   SKIP {tally['SKIP']}")
    if tally["FAIL"]:
        print(f"NOT READY: fix the {tally['FAIL']} FAIL item(s) above, then run this again.")
        return 1
    print("READY: no FAIL items. Review any WARN lines, then open your pull request.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
