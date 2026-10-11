"""Self-check for the Day 1 exercise: Test-Case ID Formatter.

Run it from the folder that contains your project files:

    python check_exercise.py          (Windows: python or py)
    python3 check_exercise.py         (macOS / Linux)

It runs YOUR test_case_id_formatter.py several times with sample answers and
compares what it prints with what is expected. It also looks at your Git
history. Each check prints PASS or FAIL with a hint. No extra tools needed.

Instructors: add --skip-git to skip the Git checks.
"""
import os
import subprocess
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
SCRIPT = os.path.join(HERE, "test_case_id_formatter.py")
SKIP_GIT = "--skip-git" in sys.argv

# Each case: the 5 answers typed in (in order) and the lines that must appear.
CASES = [
    {
        "name": "login / 42 / 34 of 40 passed",
        "answers": ["login", "42", "Valid login", "40", "34"],
        "expected": [
            "Generated ID: LOGIN-0042",
            "Title: Valid login",
            "Failed: 6",
            "Pass rate: 85.0%",
            "Release ready: False",
        ],
    },
    {
        "name": "messy spaces, everything passed",
        "answers": ["  checkout ", "7", "  Pay by card ", "25", "25"],
        "expected": [
            "Generated ID: CHECKOUT-0007",
            "Title: Pay by card",
            "Failed: 0",
            "Pass rate: 100.0%",
            "Release ready: True",
        ],
    },
    {
        "name": "rounding: 2 of 3 passed",
        "answers": ["api", "1234", "Health check", "3", "2"],
        "expected": [
            "Generated ID: API-1234",
            "Title: Health check",
            "Failed: 1",
            "Pass rate: 66.7%",
            "Release ready: False",
        ],
    },
    {
        "name": "exactly on the threshold and a 3-digit number",
        "answers": ["search", "105", "Empty query", "200", "180"],
        "expected": [
            "Generated ID: SEARCH-0105",
            "Title: Empty query",
            "Failed: 20",
            "Pass rate: 90.0%",
            "Release ready: True",
        ],
    },
]

results = []  # (label, passed, message)


def run_program(answers):
    """Run the student's script, typing the answers. Returns (stdout, error)."""
    if not os.path.exists(SCRIPT):
        return None, "test_case_id_formatter.py not found next to check_exercise.py"
    try:
        done = subprocess.run(
            [sys.executable, SCRIPT],
            input="\n".join(answers) + "\n",
            capture_output=True, text=True, timeout=10, cwd=HERE,
        )
    except subprocess.TimeoutExpired:
        return None, "the program did not finish in 10 seconds (waiting for more input?)"
    if done.returncode != 0:
        last = done.stderr.strip().splitlines()[-1:] or ["unknown error"]
        return None, "the program crashed: " + last[0]
    return done.stdout, None


def lines_of(text):
    return [line.rstrip() for line in text.splitlines()]


def has_line(output, expected):
    # A prompt may sit on the same line as your first print, so endswith is used.
    return any(line == expected or line.endswith(expected) for line in lines_of(output))


def check(label, test_function):
    """Run one check; an AssertionError means FAIL and carries the hint."""
    try:
        test_function()
        results.append((label, True, ""))
        print(f"  PASS  {label}")
    except AssertionError as problem:
        results.append((label, False, str(problem)))
        print(f"  FAIL  {label}")
        print(f"        -> {problem}")


def make_case_check(case):
    def run_case():
        output, error = run_program(case["answers"])
        assert error is None, error
        for want in case["expected"]:
            assert has_line(output, want), (
                f"expected a line  {want!r}  but did not find it. "
                f"Your last line was {lines_of(output)[-1] if output.strip() else '(nothing printed)'!r}"
            )
    return run_case


def git(*args):
    return subprocess.run(["git", "-C", HERE, *args], capture_output=True, text=True)


def git_is_own_repo():
    top = git("rev-parse", "--show-toplevel")
    assert top.returncode == 0, "no Git repository here. Run  git init  in your project folder."
    assert os.path.realpath(top.stdout.strip()) == os.path.realpath(HERE), (
        "this folder is inside another Git repository. Create your project in a clean folder and run git init there."
    )


def git_commit_count():
    git_is_own_repo()
    log = git("log", "--format=%s")
    assert log.returncode == 0, "no commits yet. Use git add and git commit -m."
    count = len(log.stdout.strip().splitlines())
    assert count >= 3, f"found {count} commit(s); at least 3 are required."


def git_messages_meaningful():
    git_is_own_repo()
    messages = [m.strip() for m in git("log", "--format=%s").stdout.splitlines()]
    assert messages, "no commits yet."
    vague = {"update", "updates", "fix", "fixes", "stuff", "changes", "final", "wip", "commit", "test", "asdf", "."}
    for message in messages:
        assert message.lower() not in vague, f"vague commit message: {message!r}. Say WHAT changed."
        assert len(message.split()) >= 3, f"commit message too short: {message!r}. Use at least 3 words."
    assert len(set(m.lower() for m in messages)) == len(messages), "two commits share the same message."


def git_formatter_history():
    git_is_own_repo()
    log = git("log", "--format=%h", "--", "test_case_id_formatter.py")
    count = len(log.stdout.split())
    assert count >= 3, (
        f"test_case_id_formatter.py appears in {count} commit(s); it must change across at least 3 commits "
        "(one per README part)."
    )


def git_clean():
    git_is_own_repo()
    status = git("status", "--porcelain")
    assert status.stdout.strip() == "", "uncommitted changes remain:\n" + status.stdout.rstrip() + "\n        Stage and commit them."


def bonus_next_id():
    output, error = run_program(CASES[0]["answers"])
    assert error is None, error
    assert has_line(output, "Next ID: LOGIN-0043"), "not found (stretch goal 1)"


def bonus_length():
    output, error = run_program(CASES[0]["answers"])
    assert error is None, error
    assert has_line(output, "ID length: 10"), "not found (stretch goal 2)"


print("=== Program checks (4 sample runs) ===")
for case in CASES:
    check("Sample run: " + case["name"], make_case_check(case))

if SKIP_GIT:
    print("\n=== Git checks skipped (--skip-git) ===")
else:
    print("\n=== Git checks ===")
    check("At least 3 commits", git_commit_count)
    check("Commit messages are specific", git_messages_meaningful)
    check("Formatter file changed in 3+ commits", git_formatter_history)
    check("Working tree clean (nothing left uncommitted)", git_clean)

core = list(results)
print("\n=== Stretch goals (optional, do not affect the result) ===")
for label, fn in [("Stretch 1: Next ID line", bonus_next_id), ("Stretch 2: ID length line", bonus_length)]:
    try:
        fn()
        print(f"  DONE  {label}")
    except AssertionError:
        print(f"  --    {label} (not done)")

failed = [r for r in core if not r[1]]
print()
if failed:
    print(f"RESULT: {len(core) - len(failed)} of {len(core)} checks passed. Fix the FAIL items above and run again.")
    sys.exit(1)
print(f"RESULT: all {len(core)} checks passed. Paste this output into your submission.")
