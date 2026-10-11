"""
check_exercise.py - self-check for the Day 2 exercise (QEA v1, Week 1).

Plain Python, plain `assert` statements, no pytest. It runs YOUR programs
non-interactively, the way a test framework would:
  - number_guess.py gets scripted guesses on stdin and its constants
    SECRET_NUMBER / MAX_ATTEMPTS are overridden in a temporary copy
  - log_scanner.py is pointed at several small log files via LOG_FILE

USAGE (from the folder that holds your programs)
    python3 check_exercise.py            (Windows: python check_exercise.py)
    python3 check_exercise.py path/to/folder     (optional: another folder)

Exit code 0 = every check passed (SKIPs are fine), 1 = something failed.
You do not need to understand this file today. Read the FAIL messages.
"""
import os
import re
import shutil
import subprocess
import sys
import tempfile

HERE = os.path.dirname(os.path.abspath(__file__))
TARGET = os.path.abspath(sys.argv[1]) if len(sys.argv) > 1 else HERE
TIMEOUT = 5  # seconds; protects against infinite loops

results = []   # (status, name, detail)


# ----------------------------------------------------------------- helpers
def check(name):
    """Decorator: run the function, record PASS/FAIL/SKIP."""
    def wrap(fn):
        try:
            fn()
            results.append(("PASS", name, ""))
        except AssertionError as err:
            results.append(("FAIL", name, str(err)))
        except Skip as err:
            results.append(("SKIP", name, str(err)))
        except Exception as err:  # unexpected problem in the checker itself
            results.append(("FAIL", name, f"checker error: {err!r}"))
        return fn
    return wrap


class Skip(Exception):
    pass


def read_source(filename):
    path = os.path.join(TARGET, filename)
    assert os.path.exists(path), f"{filename} not found in {TARGET}"
    with open(path, encoding="utf-8") as f:
        return f.read()


def run_program(filename, stdin_text="", replace=None):
    """Run a temp copy of `filename` with constants replaced; return (stdout, stderr, code)."""
    source = read_source(filename)
    for const, value in (replace or {}).items():
        pattern = re.compile(rf"^{const}\s*=.*$", re.M)
        assert pattern.search(source), (
            f"{filename}: could not find a line starting with '{const} =' "
            f"(keep that constant name on its own line)")
        source = pattern.sub(lambda m: f"{const} = {value}", source, count=1)
    workdir = tempfile.mkdtemp(prefix="qea_check_")
    try:
        script = os.path.join(workdir, filename)
        with open(script, "w", encoding="utf-8") as f:
            f.write(source)
        try:
            proc = subprocess.run(
                [sys.executable, script], input=stdin_text, capture_output=True,
                text=True, timeout=TIMEOUT, cwd=workdir)
        except subprocess.TimeoutExpired:
            raise AssertionError(
                f"{filename} did not finish within {TIMEOUT}s with input "
                f"{stdin_text.split()!r}: infinite loop? Is there a break on every exit path?")
        return proc.stdout, proc.stderr, proc.returncode
    finally:
        shutil.rmtree(workdir, ignore_errors=True)


def code_lines(filename):
    """Source lines without comments/blank lines, for light 'did you use it' checks."""
    out = []
    in_doc = False
    for line in read_source(filename).splitlines():
        s = line.strip()
        if s.count('"""') == 1:
            in_doc = not in_doc
            continue
        if in_doc or s.startswith("#") or s == "" or s.startswith('"""'):
            continue
        out.append(s)
    return "\n".join(out)


# ----------------------------------------------------------- number guess
def play(guesses, secret=42, max_attempts=7):
    stdin = "\n".join(guesses) + "\n"
    out, err, code = run_program(
        "number_guess.py", stdin,
        {"SECRET_NUMBER": str(secret), "MAX_ATTEMPTS": str(max_attempts)})
    assert "Traceback" not in err, (
        f"number_guess.py crashed with input {guesses}:\n{err.strip().splitlines()[-1]}")
    return out


def expect_result(out, status, attempts, guesses):
    m = re.search(r"^RESULT: (\w+) attempts=(\d+)\s*$", out, re.M)
    assert m, "no final 'RESULT: ... attempts=...' line found (is it still the provided last line?)"
    got = (m.group(1), int(m.group(2)))
    assert got == (status, attempts), (
        f"with guesses {guesses} expected RESULT: {status} attempts={attempts} "
        f"but got RESULT: {got[0]} attempts={got[1]}")


@check("number_guess: win in 3 (high, low, correct)")
def _():
    g = ["50", "25", "42"]
    out = play(g)
    low = out.lower()
    assert "too high" in low, "guess 50 vs secret 42 should print 'Too high'"
    assert "too low" in low, "guess 25 vs secret 42 should print 'Too low'"
    assert low.index("too high") < low.index("too low"), "messages are in the wrong order for 50 then 25"
    assert "correct! you needed 3 attempts." in low, "expected 'Correct! You needed 3 attempts.'"
    expect_result(out, "WIN", 3, g)


@check("number_guess: win on the first try")
def _():
    out = play(["42"])
    assert "too high" not in out.lower() and "too low" not in out.lower(), \
        "a correct first guess must not print Too high / Too low"
    expect_result(out, "WIN", 1, ["42"])


@check("number_guess: works for another secret (not hard-coded to 42)")
def _():
    g = ["3", "9", "7"]
    out = play(g, secret=7)
    low = out.lower()
    assert "too low" in low and "too high" in low and low.index("too low") < low.index("too high"), \
        "3 vs secret 7 should print 'Too low', then 9 should print 'Too high'"
    expect_result(out, "WIN", 3, g)


@check("number_guess: lose after MAX_ATTEMPTS wrong guesses")
def _():
    g = ["1", "2", "3"]
    out = play(g, max_attempts=3)
    assert "out of attempts! the number was 42." in out.lower(), \
        "expected 'Out of attempts! The number was 42.'"
    assert "correct" not in out.lower(), "a losing game must not print 'Correct'"
    expect_result(out, "LOSE", 3, g)


@check("number_guess: a correct guess on the LAST attempt is a WIN")
def _():
    g = ["1", "2", "42"]
    out = play(g, max_attempts=3)
    assert "out of attempts" not in out.lower(), \
        "check for the correct answer BEFORE checking attempts >= MAX_ATTEMPTS"
    expect_result(out, "WIN", 3, g)


@check("number_guess: invalid and out-of-range input do not use attempts")
def _():
    g = ["abc", "", "0", "101", "-5", "42"]
    out = play(g, max_attempts=2)
    low = out.lower()
    assert low.count("invalid input: please type a whole number.") == 3, \
        "'abc', '' and '-5' should each print 'Invalid input: please type a whole number.'"
    assert low.count("out of range: choose a number from 1 to 100.") == 2, \
        "'0' and '101' should each print 'Out of range: choose a number from 1 to 100.'"
    expect_result(out, "WIN", 1, g)


@check("number_guess: q quits (any case) and later input is ignored")
def _():
    g = ["10", "Q", "42"]
    out = play(g)
    assert "you quit. the number was 42." in out.lower(), "expected 'You quit. The number was 42.'"
    expect_result(out, "QUIT", 1, g)


@check("number_guess: uses while + break + continue + if/elif/else")
def _():
    src = code_lines("number_guess.py")
    for word in ("while", "break", "continue", "elif"):
        assert re.search(rf"\b{word}\b", src), f"number_guess.py never uses '{word}'"


# ------------------------------------------------------------ log scanner
def scan(log_text):
    """Write log_text to a temp file, run log_scanner.py against it, return parsed summary."""
    workdir = tempfile.mkdtemp(prefix="qea_log_")
    try:
        log_path = os.path.join(workdir, "case.log")
        with open(log_path, "w", encoding="utf-8", newline="") as f:
            f.write(log_text)
        out, err, code = run_program("log_scanner.py", "", {"LOG_FILE": repr(log_path)})
    finally:
        shutil.rmtree(workdir, ignore_errors=True)
    assert "Traceback" not in err, f"log_scanner.py crashed:\n{err.strip().splitlines()[-1]}"
    return out


def expect_summary(out, expected, label):
    for key, want in expected.items():
        m = re.search(rf"^{re.escape(key)}:\s*(.+?)\s*$", out, re.M)
        assert m, f"[{label}] summary line '{key}: ...' is missing"
        got = m.group(1)
        assert got == str(want), f"[{label}] '{key}' expected {want} but got {got}"


SAMPLE_EXPECTED = {
    "Lines scanned": 10, "Skipped": 4, "ERROR": 3, "WARN": 2, "INFO": 4,
    "UNKNOWN": 1, "First ERROR": "line 6", "Verdict": "FAIL",
}


@check("log_scanner: sample_app.log gives the expected summary")
def _():
    path = os.path.join(TARGET, "sample_app.log")
    assert os.path.exists(path), "sample_app.log is missing from your folder (is *.log ignoring it? see the '!' rule)"
    with open(path, encoding="utf-8") as f:
        out = scan(f.read())
    expect_summary(out, SAMPLE_EXPECTED, "sample_app.log")


@check("log_scanner: prints each ERROR line with its line number")
def _():
    with open(os.path.join(TARGET, "sample_app.log"), encoding="utf-8") as f:
        out = scan(f.read())
    assert "ERROR on line 6: 2026-03-02 09:15:12 | ERROR | Database connection refused" in out, \
        "expected 'ERROR on line 6: <the stripped line>'"
    assert "ERROR on line 14:" in out, "expected an 'ERROR on line 14:' line"
    assert "line 16" not in out, "line 16 is after END and must never be read"
    assert "END marker reached, stopping." in out, "expected 'END marker reached, stopping.'"


@check("log_scanner: clean log, no END, indented lines, 'Error' only in a message")
def _():
    log = ("  2026-01-01 00:00:01 | INFO | boot\n"
           "\n"
           "# note\n"
           "2026-01-01 00:00:02 | WARN | disk 85%\n"
           "2026-01-01 00:00:03 | INFO | Error budget ok\n")
    out = scan(log)
    expect_summary(out, {"Lines scanned": 3, "Skipped": 2, "ERROR": 0, "WARN": 1,
                         "INFO": 2, "UNKNOWN": 0, "First ERROR": "none",
                         "Verdict": "PASS"}, "clean log")


@check("log_scanner: END on line 2 stops immediately; Windows line endings work")
def _():
    log = ("2026-01-01 00:00:01 | ERROR | first\r\n"
           "END  \r\n"
           "2026-01-01 00:00:03 | ERROR | never\r\n")
    out = scan(log)
    expect_summary(out, {"Lines scanned": 1, "Skipped": 0, "ERROR": 1, "WARN": 0,
                         "INFO": 0, "UNKNOWN": 0, "First ERROR": "line 1",
                         "Verdict": "FAIL"}, "early END")


@check("log_scanner: empty log and unknown-only log")
def _():
    out = scan("")
    expect_summary(out, {"Lines scanned": 0, "Skipped": 0, "ERROR": 0, "UNKNOWN": 0,
                         "First ERROR": "none", "Verdict": "PASS"}, "empty log")
    out = scan("garbage one\n\ngarbage two\n")
    expect_summary(out, {"Lines scanned": 2, "Skipped": 1, "UNKNOWN": 2, "ERROR": 0,
                         "Verdict": "PASS"}, "unknown-only log")


@check("log_scanner: uses for + continue + break + if/elif/else")
def _():
    src = code_lines("log_scanner.py")
    for word in ("for", "continue", "break", "elif"):
        assert re.search(rf"\b{word}\b", src), f"log_scanner.py never uses '{word}'"


# ---------------------------------------------------------- git hygiene
def find_gitignore():
    for folder in (TARGET, os.path.dirname(TARGET)):
        path = os.path.join(folder, ".gitignore")
        if os.path.exists(path):
            return path
    return None


def git(*args):
    try:
        p = subprocess.run(["git", "-C", TARGET, *args], capture_output=True,
                           text=True, timeout=10)
    except (FileNotFoundError, subprocess.TimeoutExpired):
        raise Skip("git not available")
    return p


@check(".gitignore exists and lists the required patterns")
def _():
    path = find_gitignore()
    assert path, "no .gitignore found in your project folder (or its parent)"
    with open(path, encoding="utf-8") as f:
        entries = {ln.strip().rstrip("/") for ln in f if ln.strip() and not ln.strip().startswith("#")}
    for need in ("__pycache__", ".venv", ".env", "*.log", "!sample_app.log"):
        assert need in entries, (
            f".gitignore is missing '{need}'" +
            (" (sample_app.log must stay tracked even though *.log is ignored)"
             if need.startswith("!") else ""))


@check("git: ignore rules behave (git check-ignore)")
def _():
    if git("rev-parse", "--is-inside-work-tree").returncode != 0:
        raise Skip("not inside a git repository (run this from your cloned repo)")
    for path in ("__pycache__/x.pyc", ".env", "debug.log"):
        code = git("check-ignore", "-q", path).returncode
        assert code == 0, f"'{path}' should be ignored but is not"
    code = git("check-ignore", "-q", "sample_app.log").returncode
    assert code == 1, "'sample_app.log' must NOT be ignored (add '!sample_app.log' AFTER '*.log')"


@check("git: no cache/secret files tracked, and at least 4 commits")
def _():
    if git("rev-parse", "--is-inside-work-tree").returncode != 0:
        raise Skip("not inside a git repository (run this from your cloned repo)")
    tracked = git("ls-files").stdout.split()
    bad = [t for t in tracked if "__pycache__" in t or t.endswith(".pyc")
           or os.path.basename(t) == ".env" or (t.endswith(".log") and os.path.basename(t) != "sample_app.log")]
    assert not bad, f"these files must not be committed: {bad} (use git rm --cached, see the .gitignore lesson section 7)"
    count = git("rev-list", "--count", "HEAD").stdout.strip()
    assert count.isdigit() and int(count) >= 4, \
        f"expected at least 4 commits (small, meaningful steps) but found {count or 0}"


# ---------------------------------------------------------------- report
print(f"Checking programs in: {TARGET}\n")
for status, name, detail in results:
    print(f"[{status}] {name}")
    if detail:
        for line in detail.splitlines():
            print(f"       {line}")
failed = sum(1 for r in results if r[0] == "FAIL")
passed = sum(1 for r in results if r[0] == "PASS")
skipped = sum(1 for r in results if r[0] == "SKIP")
print(f"\n{passed} passed, {failed} failed, {skipped} skipped (of {len(results)} checks)")
if failed:
    print("Fix the first FAIL, run again. Work top to bottom.")
sys.exit(1 if failed else 0)
