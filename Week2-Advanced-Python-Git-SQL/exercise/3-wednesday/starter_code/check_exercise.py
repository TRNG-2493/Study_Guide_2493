"""
check_exercise.py -- self-check for the Wednesday exercise (Python Debugging & Testing Foundations).

Run it from the starter_code folder. Standard library only.

    python check_exercise.py                                   # Parts A, B, C (your run_stats.py + tests)
    python check_exercise.py --conflict-repo ../conflict-lab   # adds Part D
    python check_exercise.py --project C:\\path\\to\\qe-foundations   # adds Part E (Project 1 milestone)
    python check_exercise.py --part A                          # only one part (A, B, C, D or E)

(On Windows use `py` instead of `python` if `python` opens the Microsoft Store.)
A green result means "the automatic checks pass". Your mentor still reads your debug log and your code.
"""
import argparse
import ast
import importlib.util
import json
import os
import re
import shutil
import subprocess
import sys
import tempfile
import textwrap

HERE = os.path.dirname(os.path.abspath(__file__))
RESULTS = []          # (part, ok, label, hint)


def check(part, label, ok, hint=""):
    RESULTS.append((part, bool(ok), label, hint))
    print(f"  [{'PASS' if ok else 'FAIL'}] {label}")
    if not ok and hint:
        print(f"         hint: {hint}")
    return bool(ok)


def warn(label):
    print(f"  [WARN] {label}")


def read(path):
    try:
        with open(path, encoding="utf-8") as handle:
            return handle.read()
    except OSError:
        return None


def load_module(path, name):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def run(cmd, cwd, timeout=120):
    return subprocess.run(cmd, cwd=cwd, capture_output=True, text=True, timeout=timeout)


def strip_comments(source):
    """Source with # comments and docstrings blanked, so words in comments do not count."""
    try:
        tree = ast.parse(source)
    except SyntaxError:
        return source
    for node in ast.walk(tree):
        if isinstance(node, (ast.Module, ast.FunctionDef, ast.ClassDef)) and node.body:
            first = node.body[0]
            if isinstance(first, ast.Expr) and isinstance(getattr(first, "value", None), ast.Constant) \
                    and isinstance(first.value.value, str):
                first.value.value = ""
    return ast.unparse(tree)


def count_tests(source):
    """Number of test methods in unittest.TestCase subclasses (ast, not text)."""
    try:
        tree = ast.parse(source)
    except SyntaxError:
        return -1
    total = 0
    for node in ast.walk(tree):
        if isinstance(node, ast.ClassDef):
            total += sum(1 for n in node.body
                         if isinstance(n, ast.FunctionDef) and n.name.startswith("test"))
    return total


# ---------------------------------------------------------------- Part A
def part_a():
    print("\nPart A - Debugging: do all 7 tickets behave as specified?")
    path = os.path.join(HERE, "run_stats.py")
    source = read(path)
    if source is None:
        return check("A", "run_stats.py exists in starter_code", False, "run the check from the starter_code folder")
    try:
        rs = load_module(path, "run_stats_under_check")
    except Exception as exc:                                  # syntax error etc.
        return check("A", "run_stats.py imports without error", False, f"{type(exc).__name__}: {exc}")

    def expect(label, func, hint):
        try:
            ok = func()
        except Exception as exc:
            ok, hint = False, f"raised {type(exc).__name__}: {exc}. {hint}"
        check("A", label, ok, hint)

    def fresh_counter():
        rs.run_counter = 0

    expect("BUG-1 median of an even-sized list is the mean of the two middle values",
           lambda: abs(rs.median([4, 1, 3, 2]) - 2.5) < 1e-9 and rs.median([5, 1, 3]) == 3 and rs.median([7]) == 7,
           "median([4, 1, 3, 2]) should be 2.5")

    def bug2():
        d = [120, 80, 340, 95, 210, 150]
        return rs.slowest(list(d), 3) == [340, 210, 150] and rs.slowest(list(d), 0) == [] \
            and len(rs.slowest(list(d), 99)) == 6
    expect("BUG-2 slowest(durations, n) returns exactly n items (n == 0 gives [])", bug2,
           "an off-by-one in the slice; also try n == 0")

    def bug3():
        res = [{"test": "t1", "suite": "login", "status": "pass"}, {"test": "t2", "suite": "login", "status": "fail"},
               {"test": "t3", "suite": "login", "status": "pass"}, {"test": "t4", "suite": "search", "status": "pass"}]
        return rs.group_by_suite(res) == {"login": {"pass": 2, "fail": 1}, "search": {"pass": 1}} \
            and rs.group_by_suite([]) == {} \
            and rs.group_by_suite([{"test": "x", "status": "skip"}]) == {"unknown": {"skip": 1}}
    expect("BUG-3 group_by_suite counts per suite/status; missing suite goes to 'unknown'", bug3,
           "a dict key must exist before you add to it")

    def bug4():
        first = rs.note_flaky("t2")
        second = rs.note_flaky("t9")
        mine = ["t1"]
        out = rs.note_flaky("t2", mine)
        return first == ["t2"] and second == ["t9"] and out is mine and mine == ["t1", "t2"]
    expect("BUG-4 note_flaky() calls without a list do not share state", bug4,
           "mutability-and-memory.md: default values are created once")

    def bug5():
        fresh_counter()
        return rs.next_run_id() == "RUN-0001" and rs.next_run_id() == "RUN-0002"
    expect("BUG-5 next_run_id() returns RUN-0001, RUN-0002, ...", bug5, "scope-and-namespaces.md: assignment makes a name local")

    def bug6():
        fresh_counter()
        res = [{"test": "t1", "suite": "login", "status": "pass"}]
        data = [120, 80, 340, 95, 210, 150]
        before = list(data)
        s = rs.summarise_run(res, data)
        return s["latest_ms"] == 150 and s["slowest_ms"] == [340, 210, 150] and data == before and s["median_ms"] == 135.0
    expect("BUG-6 summarise_run reports latest_ms 150 and leaves the caller's list in order", bug6,
           "who is changing your list, and when? Print id() or the list before and after each call")

    def bug7():
        fresh_counter()
        res = [{"test": "t1", "suite": "login", "status": "pass"}]
        s = rs.summarise_run(res, [])
        try:
            rs.median([])
        except ValueError:
            raised = True
        else:
            raised = False
        return raised and s["median_ms"] is None and s["slowest_ms"] == [] and s["latest_ms"] is None
    expect("BUG-7 median([]) raises ValueError; summarise_run(results, []) gives median_ms None", bug7,
           "decide where the empty case is handled: the helper raises, the caller guards")

    code = strip_comments(source)
    check("A", "no breakpoint() or pdb.set_trace() left in run_stats.py", "breakpoint(" not in code and "set_trace" not in code,
          "remove debugger calls before you commit")

    log = read(os.path.join(HERE, "debug_log.md")) or ""
    evidence = re.findall(r"^- Evidence[^:\n]*:[ \t]*(\S.*)$", log, flags=re.M)
    check("A", "debug_log.md has an Evidence line filled in for at least 5 tickets", len(evidence) >= 5,
          "write what you actually saw: a pdb command and its output")
    check("A", "debug_log.md has a reflection", bool(re.search(r"## Reflection[^\n]*\n+(?!\(?Which bug)\S", log)) and len(log) > 1500,
          "answer the three reflection questions")


# ---------------------------------------------------------------- Part B
def part_b():
    print("\nPart B - Logging: run_stats.py logs, run_report.py configures")
    path = os.path.join(HERE, "run_stats.py")
    source = read(path)
    if source is None:
        return check("B", "run_stats.py exists", False)
    code = strip_comments(source)
    check("B", "run_stats.py creates a module logger with logging.getLogger(__name__)", "getLogger(__name__)" in code.replace(" ", ""),
          "library modules get a logger; they do not configure one")
    check("B", "run_stats.py does not call logging.basicConfig or add handlers", "basicConfig" not in code and "addHandler" not in code,
          "configuration belongs in the entry point (run_report.py)")
    check("B", "run_stats.py has no print() calls", not re.search(r"\bprint\(", code), "replace prints with logger calls")
    try:
        import logging
        rs = load_module(path, "run_stats_logging_check")
        rs.run_counter = 0

        def records(level, func):
            try:
                with _assert_logs(logging, rs.logger.name if hasattr(rs, "logger") else "run_stats_logging_check", level) as cm:
                    func()
                return cm.records
            except AssertionError:
                return []
        mod_logger = getattr(rs, "logger", None)
        check("B", "module has a variable named `logger` that is a logging.Logger", isinstance(mod_logger, logging.Logger),
              "logger = logging.getLogger(__name__)")
        if isinstance(mod_logger, logging.Logger):
            check("B", "median() emits at least one DEBUG record", len(records("DEBUG", lambda: rs.median([3, 1, 2]))) >= 1,
                  "log the input size and the result at DEBUG")
            check("B", "group_by_suite() emits a WARNING for a result with no suite",
                  any(r.levelno == logging.WARNING for r in records("WARNING", lambda: rs.group_by_suite([{"test": "t", "status": "pass"}]))),
                  "logger.warning(...) when you fall back to 'unknown'")
            check("B", "summarise_run() emits an INFO record", any(r.levelno == logging.INFO for r in records(
                "INFO", lambda: rs.summarise_run([{"test": "t", "suite": "a", "status": "pass"}], [5, 6]))),
                  "one INFO line per report: run id and totals")
            check("B", "log messages use %-style arguments, not f-strings, in at least one call",
                  bool(re.search(r"logger\.\w+\(\s*['\"][^'\"]*%[sdr]", source)), "logger.debug('got %d values', len(v))")
    except Exception as exc:
        check("B", "run_stats.py can be loaded for the logging checks", False, f"{type(exc).__name__}: {exc}")

    # run_report.py: configure once, console INFO, file DEBUG
    tmp = tempfile.mkdtemp(prefix="check_b_")
    try:
        for name in ("run_stats.py", "run_report.py"):
            shutil.copy(os.path.join(HERE, name), tmp)
        proc = run([sys.executable, "run_report.py"], tmp)
        logfile = os.path.join(tmp, "run_report.log")
        log_text = read(logfile) or ""
        out = proc.stdout
        check("B", "python run_report.py runs and writes run_report.log", proc.returncode == 0 and bool(log_text),
              (proc.stderr or "").strip().splitlines()[-1] if proc.stderr.strip() else "add a FileHandler in run_report.py main()")
        check("B", "the file log contains DEBUG lines", "DEBUG" in log_text, "file handler level DEBUG, logger level DEBUG")
        check("B", "the console shows INFO but no DEBUG lines", "INFO" in out and "DEBUG" not in out,
              "console handler level INFO; remember the logger itself must allow DEBUG")
        def info_lines(times):
            code = f"import run_report\nfor _ in range({times}): run_report.main(['run_report.py', '6'])"
            result = run([sys.executable, "-c", code], tmp)
            return sum(1 for ln in result.stdout.splitlines() if "INFO" in ln)
        once, twice = info_lines(1), info_lines(2)
        check("B", "configuring logging twice does not duplicate lines (handlers added once)",
              once >= 1 and twice == 2 * once, "guard: if logger.handlers: return")
    finally:
        shutil.rmtree(tmp, ignore_errors=True)


class _assert_logs:
    """Tiny stand-in for TestCase.assertLogs so the checker can capture records."""
    def __init__(self, logging, name, level):
        self.logging, self.name, self.level = logging, name, level

    def __enter__(self):
        import unittest
        self.cm = unittest.TestCase().assertLogs(self.name, self.level)
        return self.cm.__enter__()

    def __exit__(self, *exc):
        return self.cm.__exit__(*exc)


# ---------------------------------------------------------------- Part C
def part_c():
    print("\nPart C - Unit tests for run_stats.py")
    path = os.path.join(HERE, "test_run_stats.py")
    source = read(path)
    if source is None:
        return check("C", "test_run_stats.py exists in starter_code", False)
    n = count_tests(source)
    code = strip_comments(source)
    check("C", f"at least 12 test methods (found {n})", n >= 12, "one test, one behaviour")
    check("C", "uses assertRaises at least once", "assertRaises" in code, "with self.assertRaises(ValueError):")
    check("C", "at least 3 tests of bad or unusual input (3+ of: empty, zero, missing, unknown, None)",
          len(re.findall(r"def test\w*(?:empty|zero|missing|unknown|none|no_)\w*", source, flags=re.I)) >= 3,
          "name tests for the edge case they cover, e.g. test_empty_raises_value_error")
    check("C", "uses setUp so tests stay independent", "def setUp" in code, "reset shared state such as run_stats.run_counter")
    check("C", "uses assertLogs at least once", "assertLogs" in code, "log messages are behaviour too")
    check("C", "no test is an empty placeholder (no leftover 'pass' only classes)",
          not re.search(r"class Test\w+\(unittest\.TestCase\):\s*\n\s*pass\s*\n", source), "fill in or delete the TODO classes")

    proc = run([sys.executable, "-m", "unittest", "test_run_stats"], HERE)
    last = proc.stderr.strip().splitlines()[-1] if proc.stderr.strip() else ""
    check("C", "your tests PASS against your fixed run_stats.py", proc.returncode == 0, f"unittest says: {last}")

    baseline = os.path.join(HERE, "_baseline", "run_stats_buggy.py")
    if not os.path.exists(baseline):
        return warn("_baseline/run_stats_buggy.py is missing; skipped the 'catches the bugs' check")
    tmp = tempfile.mkdtemp(prefix="check_c_")
    try:
        shutil.copy(baseline, os.path.join(tmp, "run_stats.py"))
        shutil.copy(path, tmp)
        proc = run([sys.executable, "-m", "unittest", "test_run_stats"], tmp)
        m = re.search(r"FAILED \((?:failures=(\d+))?(?:, )?(?:errors=(\d+))?", proc.stderr)
        failing = (int(m.group(1) or 0) + int(m.group(2) or 0)) if m else 0
        check("C", f"your tests FAIL against the original buggy file in _baseline/ (found {failing} failing, need 7)",
              failing >= 7, "a good regression test fails on the bug it protects; you need roughly one per bug")
    finally:
        shutil.rmtree(tmp, ignore_errors=True)


# ---------------------------------------------------------------- Part D
def git(repo, *args):
    return run(["git", *args], repo)


def part_d(repo):
    print(f"\nPart D - Merge conflict resolved in: {repo}")
    if not repo or not os.path.isdir(os.path.join(repo, ".git")):
        return check("D", "the folder is a Git repository (pass --conflict-repo path)", False, "run setup_conflict first")
    repo = os.path.abspath(repo)
    check("D", "no unmerged files remain (git ls-files -u is empty)", git(repo, "ls-files", "-u").stdout.strip() == "",
          "git add each resolved file")
    check("D", "the merge is finished (no MERGE_HEAD)", git(repo, "rev-parse", "-q", "--verify", "MERGE_HEAD").returncode != 0,
          "git commit to finish the merge")
    parents = git(repo, "rev-list", "--parents", "-n", "1", "HEAD").stdout.split()
    check("D", "HEAD is a merge commit (2 parents)", len(parents) == 3, "finish with git commit, not git merge --abort")
    subjects = git(repo, "log", "--format=%s", "HEAD").stdout
    check("D", "history keeps both teammates' commits", "Lower gate and add checkout suite" in subjects
          and "Add strict gate and payments suite" in subjects, "do not rebuild or reset the repo")
    markers = []
    for name in ("settings.py", "report.py", "CHANGELOG.md"):
        text = read(os.path.join(repo, name)) or ""
        if re.search(r"^(<<<<<<< |=======$|>>>>>>> )", text, flags=re.M):
            markers.append(name)
    check("D", "no conflict markers (<<<<<<<, =======, >>>>>>>) in any file", not markers, f"still in: {', '.join(markers)}")

    probe = textwrap.dedent("""
        import json, settings, report
        print(json.dumps({
            "threshold": settings.PASS_THRESHOLD, "suites": settings.SUITES,
            "summary": report.summary_line(3, 4),
            "failing": report.failing_suites([{"suite": "login", "status": "fail"}, {"suite": "search", "status": "pass"}]),
            "verdict": report.verdict(93.0)}))
    """)
    proc = run([sys.executable, "-c", probe], repo)
    try:
        info = json.loads(proc.stdout.strip().splitlines()[-1])
    except (ValueError, IndexError):
        info = None
    if info is None:
        return check("D", "settings.py and report.py import and run", False,
                     (proc.stderr.strip().splitlines() or ["syntax error?"])[-1])
    check("D", "PASS_THRESHOLD is 95 (the QA lead's decision, see README)", info["threshold"] == 95, "keep Sam's number")
    check("D", "SUITES has all four: login, search, checkout, payments (in that order)",
          info["suites"] == ["login", "search", "checkout", "payments"], "keep BOTH new suites")
    check("D", "report.py keeps BOTH new functions (summary_line and failing_suites)",
          info["summary"] == "3/4 passed (75.0%)" and info["failing"] == ["login"], "both sides added a function; keep both")
    proc = run([sys.executable, "report.py"], repo)
    check("D", "python report.py prints the expected two lines",
          proc.stdout.splitlines() == ["Suites: login, search, checkout, payments", "Verdict for 93.0%: RED"],
          f"got: {proc.stdout.strip()!r}")
    changelog = read(os.path.join(repo, "CHANGELOG.md")) or ""
    check("D", "CHANGELOG.md keeps both teammates' lines (it merged automatically; do not lose it)",
          "Strict gate" in changelog and "QE Foundations" in changelog, "git merge handled this file for you")


# ---------------------------------------------------------------- Part E
def part_e(project):
    print(f"\nPart E - Project 1 milestone in: {project}")
    if not project or not os.path.isdir(project):
        return check("E", "the project folder exists (pass --project path)", False)
    project = os.path.abspath(project)
    pkg = os.path.join(project, "qe_foundations")
    for sub in ("utils", "ingestion"):
        check("E", f"qe_foundations/{sub}/ exists with an __init__.py", os.path.isfile(os.path.join(pkg, sub, "__init__.py")),
              "folder layout from Monday and Tuesday")
    for sub in ("tests", "data", "docs"):
        check("E", f"{sub}/ folder exists", os.path.isdir(os.path.join(project, sub)))

    # --- logging
    ing_dir = os.path.join(pkg, "ingestion")
    ing_sources = {}
    for name in sorted(os.listdir(ing_dir)) if os.path.isdir(ing_dir) else []:
        if name.endswith(".py") and name != "__init__.py":
            ing_sources[name] = strip_comments(read(os.path.join(ing_dir, name)) or "")
    joined = "\n".join(ing_sources.values())
    check("E", "an ingestion module uses logging.getLogger(__name__)", "getLogger(__name__)" in joined.replace(" ", ""),
          "logger = logging.getLogger(__name__) at the top of your loader module")
    calls = re.findall(r"\blog(?:ger)?\.(debug|info|warning|error|exception|critical)\(", joined)
    check("E", f"ingestion logs at 2+ different levels, 3+ calls (found {len(calls)} calls, levels {sorted(set(calls))})",
          len(calls) >= 3 and len(set(calls)) >= 2, "INFO for start/finish, WARNING for a skipped bad row, ERROR/exception for a failed file")
    offenders = []
    for root, _dirs, files in os.walk(pkg):
        for name in files:
            if name.endswith(".py"):
                rel = os.path.relpath(os.path.join(root, name), project).replace("\\", "/")
                if rel != "qe_foundations/utils/logging_setup.py" and "basicConfig(" in strip_comments(read(os.path.join(root, name)) or ""):
                    offenders.append(rel)
    check("E", "logging.basicConfig is only used (if at all) in utils/logging_setup.py", not offenders, f"remove from: {', '.join(offenders)}")
    if re.search(r"\bprint\(", joined):
        warn("ingestion still uses print(); replace with logger calls where it reports progress or problems")

    probe = textwrap.dedent("""
        import json, logging, os, shutil, tempfile
        from qe_foundations.utils.logging_setup import setup_logging
        d = tempfile.mkdtemp()
        out = {}
        try:
            f = os.path.join(d, "t.log")
            lg = setup_logging(level="INFO", logfile=f)
            n1 = len(lg.handlers)
            lg2 = setup_logging(level="INFO", logfile=f)
            out["returns_logger"] = isinstance(lg, logging.Logger) and lg is lg2
            out["name"] = lg.name
            out["idempotent"] = len(lg2.handlers) == n1 and n1 >= 2
            logging.getLogger("qe_foundations.ingestion.probe").debug("probe-debug-line")
            for h in lg.handlers: h.flush()
            out["file_has_debug"] = "probe-debug-line" in open(f, encoding="utf-8").read()
        finally:
            logging.shutdown()
            shutil.rmtree(d, ignore_errors=True)
        print(json.dumps(out))
    """)
    proc = run([sys.executable, "-c", probe], project)
    try:
        info = json.loads(proc.stdout.strip().splitlines()[-1])
    except (ValueError, IndexError):
        info = {}
        check("E", "qe_foundations.utils.logging_setup.setup_logging can be imported and called", False,
              (proc.stderr.strip().splitlines() or ["file missing?"])[-1])
    if info:
        check("E", "setup_logging returns the 'qe_foundations' logger (same object on a second call)",
              info.get("returns_logger") and info.get("name") == "qe_foundations", "logging.getLogger('qe_foundations')")
        check("E", "setup_logging adds console + file handlers once (second call adds none)", info.get("idempotent"),
              "if logger.handlers: return logger")
        check("E", "the log file receives DEBUG records from child loggers (qe_foundations.*)", info.get("file_has_debug"),
              "logger level DEBUG, file handler level DEBUG")

    # --- tests
    tests_dir = os.path.join(project, "tests")
    groups = {"utils": [0, 0, ""], "ingestion": [0, 0, ""]}     # tests, assertRaises, source
    for name in sorted(os.listdir(tests_dir)) if os.path.isdir(tests_dir) else []:
        if not (name.startswith("test_") and name.endswith(".py")):
            continue
        src = read(os.path.join(tests_dir, name)) or ""
        key = "utils" if "utils" in name else "ingestion" if ("ingestion" in name or "loader" in name) else None
        if key:
            groups[key][0] += max(count_tests(src), 0)
            groups[key][1] += len(re.findall(r"assertRaises", src))
            groups[key][2] += src
    check("E", f"tests/test_utils*.py has at least 4 tests (found {groups['utils'][0]})", groups["utils"][0] >= 4,
          "name the files test_utils.py and test_ingestion.py")
    check("E", f"tests/test_ingestion*.py has at least 4 tests (found {groups['ingestion'][0]})", groups["ingestion"][0] >= 4)
    check("E", "at least 1 bad-input test for utils (assertRaises)", groups["utils"][1] >= 1)
    check("E", "at least 2 bad-input tests for ingestion (assertRaises: missing file, bad row...)", groups["ingestion"][1] >= 2)
    check("E", "an ingestion test uses assertLogs", "assertLogs" in groups["ingestion"][2], "check that your WARNING really is logged")
    check("E", "an ingestion test builds its own test file (tempfile) and cleans up (addCleanup/tearDown/with)",
          "tempfile" in groups["ingestion"][2], "never depend on a file that exists only on your laptop")
    proc = run([sys.executable, "-m", "unittest", "discover", "-s", "tests"], project)
    summary = (proc.stderr.strip().splitlines() or [""])[-1]
    ran = re.search(r"Ran (\d+) tests?", proc.stderr)
    check("E", "python -m unittest discover -s tests runs and passes", proc.returncode == 0 and bool(ran), f"unittest says: {summary}")
    check("E", f"discover ran at least 8 tests (ran {ran.group(1) if ran else 0})", bool(ran) and int(ran.group(1)) >= 8)

    gitignore = read(os.path.join(project, ".gitignore")) or ""
    check("E", ".gitignore ignores *.log", "*.log" in gitignore, "log files are output, not source")
    docs_ok = any("unittest discover" in (read(os.path.join(project, "docs", n)) or "")
                  for n in (os.listdir(os.path.join(project, "docs")) if os.path.isdir(os.path.join(project, "docs")) else []))
    check("E", "a file in docs/ explains how to run the tests (mentions 'unittest discover') and where the log goes", docs_ok,
          "docs/testing.md, 5 lines is enough")


# ---------------------------------------------------------------- main
def main():
    parser = argparse.ArgumentParser(description="Self-check for the Wednesday exercise.")
    parser.add_argument("--part", choices=list("ABCDE"), help="run only one part")
    parser.add_argument("--conflict-repo", help="path to your conflict-lab repo (Part D)")
    parser.add_argument("--project", help="path to your qe-foundations repo (Part E)")
    args = parser.parse_args()
    wanted = [args.part] if args.part else ["A", "B", "C"] + (["D"] if args.conflict_repo else []) + (["E"] if args.project else [])
    if not args.part:
        if not args.conflict_repo:
            print("(Part D skipped: add --conflict-repo path\\to\\conflict-lab)")
        if not args.project:
            print("(Part E skipped: add --project path\\to\\qe-foundations)")
    for part in wanted:
        {"A": part_a, "B": part_b, "C": part_c, "D": lambda: part_d(args.conflict_repo),
         "E": lambda: part_e(args.project)}[part]()
    print("\nSummary")
    for part in wanted:
        mine = [r for r in RESULTS if r[0] == part]
        print(f"  Part {part}: {sum(1 for r in mine if r[1])}/{len(mine)} checks pass")
    failed = [r for r in RESULTS if not r[1]]
    print("\nALL CHECKS PASS" if not failed else f"\n{len(failed)} check(s) still failing. Fix them and run again.")
    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(main())
