"""Self-check for the Thursday pair project (plain asserts, no pytest).

Run from the folder that contains test_utils/ :

    python3 check_exercise.py

Each check prints PASS or FAIL with a message that says what was expected and what
your code returned. Fix the first FAIL in the section you are working on, then re-run.
Exit code is 0 only when everything passes.

(You do not need to understand the "runner" at the bottom of this file. The checks
themselves are plain functions with assert statements: read them, they are the spec.)
"""
import random
import time

from test_utils import validators, generators, helpers, decorators
import demo_report


def expect(actual, expected, label):
    """assert with a helpful message (shows what the call returned)."""
    assert actual == expected, f"{label} -> expected {expected!r}, got {actual!r}"


# ---------------------------------------------------------------- validators
def check_is_in_range():
    expect(validators.is_in_range(5, 1, 10), True, "is_in_range(5, 1, 10)")
    expect(validators.is_in_range(1, 1, 10), True, "is_in_range(1, 1, 10)  (low is included)")
    expect(validators.is_in_range(10, 1, 10), True, "is_in_range(10, 1, 10)  (high is included)")
    expect(validators.is_in_range(0, 1, 10), False, "is_in_range(0, 1, 10)")
    expect(validators.is_in_range(11, 1, 10), False, "is_in_range(11, 1, 10)")


def check_is_valid_test_id():
    v = validators.is_valid_test_id
    expect(v("TC-007"), True, 'is_valid_test_id("TC-007")')
    expect(v("TC-7"), False, 'is_valid_test_id("TC-7")  (too few digits)')
    expect(v("TC-0071"), False, 'is_valid_test_id("TC-0071")  (too many digits)')
    expect(v("tc-007"), False, 'is_valid_test_id("tc-007")  (prefix is case-sensitive)')
    expect(v("TC-00a"), False, 'is_valid_test_id("TC-00a")  (letter instead of digit)')
    expect(v("TC007"), False, 'is_valid_test_id("TC007")  (missing dash)')
    expect(v("QA-12", prefix="QA", digits=2), True, 'is_valid_test_id("QA-12", prefix="QA", digits=2)')
    expect(v("QA-12"), False, 'is_valid_test_id("QA-12")  (default prefix is TC)')


def check_is_valid_status_code():
    v = validators.is_valid_status_code
    expect(v(200), True, "is_valid_status_code(200)")
    expect(v(100), True, "is_valid_status_code(100)")
    expect(v(599), True, "is_valid_status_code(599)")
    expect(v(99), False, "is_valid_status_code(99)")
    expect(v(600), False, "is_valid_status_code(600)")


def check_is_valid_email():
    v = validators.is_valid_email
    for good in ["qa.tester@example.com", "a@b.co"]:
        expect(v(good), True, f"is_valid_email({good!r})")
    bad = {
        "no-at.example.com": "no @",
        "a@@b.com": "two @",
        "@example.com": "nothing before @",
        "a@example": "no dot in domain",
        "a@.com": "domain starts with a dot",
        "a@com.": "domain ends with a dot",
        "a b@example.com": "contains a space",
    }
    for text, why in bad.items():
        expect(v(text), False, f"is_valid_email({text!r})  ({why})")


def check_is_strong_password():
    v = validators.is_strong_password
    expect(v("Passw0rdOK"), True, 'is_strong_password("Passw0rdOK")')
    expect(v("short1A"), False, 'is_strong_password("short1A")  (7 chars, min is 8)')
    expect(v("alllowercase1"), False, 'is_strong_password("alllowercase1")  (no uppercase)')
    expect(v("ALLUPPER123"), False, 'is_strong_password("ALLUPPER123")  (no lowercase)')
    expect(v("NoDigitsHere"), False, 'is_strong_password("NoDigitsHere")  (no digit)')
    expect(v("Ab1", min_length=3), True, 'is_strong_password("Ab1", min_length=3)')
    expect(v("Ab1", min_length=4), False, 'is_strong_password("Ab1", min_length=4)')


def check_all_pass():
    ends_with_1 = lambda text: text.endswith("1")
    ends_with_9 = lambda text: text.endswith("9")
    expect(validators.all_pass("TC-001", validators.is_valid_test_id, ends_with_1), True,
           'all_pass("TC-001", is_valid_test_id, endswith 1)')
    expect(validators.all_pass("TC-001", validators.is_valid_test_id, ends_with_9), False,
           'all_pass("TC-001", is_valid_test_id, endswith 9)  (one check fails)')
    expect(validators.all_pass("TC-001"), True, 'all_pass("TC-001")  (no checks at all)')
    expect(validators.all_pass("hello", ends_with_9), False, 'all_pass("hello", endswith 9)')


# ---------------------------------------------------------------- generators
def check_generate_username():
    g = generators.generate_username
    name = g(seed=1)
    assert type(name) is str, f"generate_username(seed=1) should return a str, got {name!r}"
    assert name.startswith("user") and name[4:].isdigit() and len(name) == 8, \
        f"generate_username(seed=1) should look like 'user4821', got {name!r}"
    expect(g(seed=1), name, "generate_username(seed=1) called twice (same seed, same result)")
    other = g("qa_", 6, seed=2)
    assert other.startswith("qa_") and other[3:].isdigit() and len(other) == 9, \
        f"generate_username('qa_', 6, seed=2) should be 'qa_' + 6 digits, got {other!r}"


def check_generate_usernames():
    g = generators.generate_usernames
    names = g(20, seed=3)
    assert type(names) is list, f"generate_usernames(20, seed=3) should return a list, got {names!r}"
    expect(len(names), 20, "len(generate_usernames(20, seed=3))")
    expect(len(set(names)), 20, "number of UNIQUE names in generate_usernames(20, seed=3)")
    for name in names:
        assert name.startswith("user") and name[4:].isdigit() and len(name) == 8, \
            f"every username should look like 'user4821', got {name!r}"
    expect(g(20, seed=3), names, "generate_usernames(20, seed=3) called twice")
    assert g(5, seed=1) != g(5, seed=2), "different seeds should (almost always) give different lists"
    expect(g(0, seed=1), [], "generate_usernames(0)")


def check_generate_password():
    g = generators.generate_password
    for length in (8, 12, 20):
        pw = g(length, seed=length)
        assert type(pw) is str, f"generate_password({length}, seed={length}) should return a str, got {pw!r}"
        expect(len(pw), length, f"len(generate_password({length}))")
        assert validators.is_strong_password(pw, min_length=length), \
            f"generate_password({length}) = {pw!r} must be a strong password (upper, lower, digit)"
    expect(g(12, seed=5), g(12, seed=5), "generate_password(12, seed=5) called twice")


def check_generate_test_id():
    g = generators.generate_test_id
    expect(g(7), "TC-007", "generate_test_id(7)")
    expect(g(42), "TC-042", "generate_test_id(42)")
    expect(g(123), "TC-123", "generate_test_id(123)")
    expect(g(42, prefix="API", digits=4), "API-0042", 'generate_test_id(42, prefix="API", digits=4)')
    assert validators.is_valid_test_id(g(9, "QA", 2), "QA", 2), "generated IDs must pass is_valid_test_id"


def check_make_test_case():
    m = generators.make_test_case
    expect(m("TC-001", "Login"),
           {"id": "TC-001", "name": "Login", "priority": "Medium", "status": "New", "duration": 0.0},
           'make_test_case("TC-001", "Login")')
    case = m("TC-002", "Search", priority="High", browser="Chrome")
    expect(case["priority"], "High", "priority option overrides the default")
    expect(case["browser"], "Chrome", "extra option (browser) is added to the dict")
    expect(case["status"], "New", "defaults not mentioned in options are kept")
    first = m("TC-003", "A")
    first["status"] = "Failed"
    expect(m("TC-003", "A")["status"], "New", "each call must return a NEW dict")


def check_generate_test_cases():
    g = generators.generate_test_cases
    cases = g(12, seed=4)
    assert type(cases) is list, f"generate_test_cases(12, seed=4) should return a list, got {cases!r}"
    expect(len(cases), 12, "len(generate_test_cases(12, seed=4))")
    expect([c["id"] for c in cases], [f"TC-{n:03d}" for n in range(1, 13)], "IDs are TC-001..TC-012 in order")
    expect(cases[0]["name"], "Test case 1", "name of the first case")
    for case in cases:
        assert case["priority"] in ("Low", "Medium", "High"), f"bad priority in {case!r}"
        assert case["status"] in ("New", "Passed", "Failed"), f"bad status in {case!r}"
        assert 0.10 <= case["duration"] <= 5.00, f"duration must be 0.10 to 5.00, got {case!r}"
    expect(g(12, seed=4), cases, "generate_test_cases(12, seed=4) called twice")
    assert g(12, seed=4) != g(12, seed=5), "different seeds should give different data"
    expect(g(0, seed=1), [], "generate_test_cases(0)")


def check_generators_do_not_touch_global_random():
    """Generators must use their own random.Random(seed), not random.seed(...)."""
    assert generators.generate_username(seed=1) is not None, "generate_username still returns None (TODO)"
    random.seed(123)
    expected = random.random()
    random.seed(123)
    generators.generate_username(seed=1)
    generators.generate_usernames(3, seed=1)
    generators.generate_password(8, seed=1)
    generators.generate_test_cases(3, seed=1)
    expect(random.random(), expected,
           "global random after calling generators (use rng = random.Random(seed), not random.seed(seed))")


# ---------------------------------------------------------------- helpers
SAMPLE = [
    {"id": "TC-001", "name": "a", "priority": "High", "status": "Passed", "duration": 2.5},
    {"id": "TC-002", "name": "b", "priority": "Low", "status": "Failed", "duration": 0.5},
    {"id": "TC-003", "name": "c", "priority": "High", "status": "Passed", "duration": 4.0},
]


def check_sort_cases():
    by_duration = helpers.sort_cases(SAMPLE, "duration")
    expect([c["id"] for c in by_duration], ["TC-002", "TC-001", "TC-003"], 'sort_cases(SAMPLE, "duration")')
    slow_first = helpers.sort_cases(SAMPLE, "duration", reverse=True)
    expect([c["id"] for c in slow_first], ["TC-003", "TC-001", "TC-002"], 'sort_cases(SAMPLE, "duration", reverse=True)')
    expect([c["id"] for c in helpers.sort_cases(SAMPLE, "id", reverse=True)],
           ["TC-003", "TC-002", "TC-001"], 'sort_cases(SAMPLE, "id", reverse=True)')
    expect([c["id"] for c in SAMPLE], ["TC-001", "TC-002", "TC-003"], "the ORIGINAL list must stay unchanged")


def check_slowest():
    expect(helpers.slowest(SAMPLE)["id"], "TC-003", "slowest(SAMPLE)['id']")
    expect(helpers.slowest([]), None, "slowest([])")


def check_count_by():
    expect(helpers.count_by(SAMPLE, "priority"), {"High": 2, "Low": 1}, 'count_by(SAMPLE, "priority")')
    expect(helpers.count_by(SAMPLE, "status"), {"Passed": 2, "Failed": 1}, 'count_by(SAMPLE, "status")')
    expect(helpers.count_by([], "status"), {}, 'count_by([], "status")')


# ---------------------------------------------------------------- decorators
def check_timer():
    decorators.TIMING_LOG.clear()

    @decorators.timer
    def slow_add(a, b=0):
        """Add two numbers slowly."""
        time.sleep(0.05)
        return a + b

    expect(slow_add(2, b=3), 5, "a @timer function must still return its result: slow_add(2, b=3)")
    expect(slow_add.__name__, "slow_add", "slow_add.__name__ (use @wraps(func))")
    expect(slow_add.__doc__, "Add two numbers slowly.", "slow_add.__doc__ (use @wraps(func))")
    expect(len(decorators.TIMING_LOG), 1, "len(TIMING_LOG) after one call")
    name, seconds = decorators.TIMING_LOG[0]
    expect(name, "slow_add", "TIMING_LOG[0] function name")
    assert 0.04 <= seconds < 1.0, f"TIMING_LOG[0] seconds should be about 0.05, got {seconds!r}"
    slow_add(1)
    expect(len(decorators.TIMING_LOG), 2, "len(TIMING_LOG) after two calls")


# ---------------------------------------------------------------- integration
def check_demo_report():
    decorators.TIMING_LOG.clear()
    text = demo_report.build_demo_report(count=6, seed=7)
    assert type(text) is str and text != "", f"build_demo_report() should return the report text, got {text!r}"
    lines = text.split("\n")
    expect(lines[0], "TEST DATA REPORT", "report line 1")
    expect(lines[1], "Total: 6", "report line 2")
    assert lines[2].startswith("Slowest: TC-"), f"report line 3 should start 'Slowest: TC-', got {lines[2]!r}"
    assert lines[3].startswith("By priority: "), f"report line 4 should start 'By priority: ', got {lines[3]!r}"
    expect(len(lines), 4 + 6, "number of report lines (4 header lines + one per case)")
    durations = [float(line.split(" | ")[3].replace(" s", "")) for line in lines[4:]]
    expect(durations, sorted(durations, reverse=True), "case lines must be sorted slowest first")
    assert lines[2].split("(")[1].startswith(f"{durations[0]:.2f}"), \
        "the 'Slowest:' line must match the first (slowest) case line"
    expect(demo_report.build_demo_report(count=6, seed=7), text, "build_demo_report(6, 7) called twice")
    expect(demo_report.build_demo_report.__name__, "build_demo_report", "decorated function keeps its name")
    expect(decorators.TIMING_LOG[0][0], "build_demo_report", "build_demo_report must be decorated with @timer")


# ---------------------------------------------------------------- git / collaboration files
def read_file(path):
    try:
        with open(path) as handle:
            return handle.read()
    except OSError:
        return None


def check_gitignore():
    text = read_file(".gitignore")
    assert text is not None, ".gitignore is missing: create it in the repo root (Milestone 0)"
    assert "__pycache__" in text, ".gitignore must list __pycache__/ so compiled files are not committed"


def check_retrospective():
    text = read_file("RETROSPECTIVE.md")
    assert text is not None, "RETROSPECTIVE.md is missing: copy templates/RETROSPECTIVE.md to the repo root and fill it in"
    assert "[WRITE HERE]" not in text, "RETROSPECTIVE.md still contains [WRITE HERE] placeholders: fill every section"
    assert len(text) > 600, f"RETROSPECTIVE.md looks too short ({len(text)} characters): answer every prompt properly"


SECTIONS = [
    ("Milestone 1-2: validators", [check_is_in_range, check_is_valid_test_id, check_is_valid_status_code,
                                   check_is_valid_email, check_is_strong_password, check_all_pass]),
    ("Milestone 3-4: generators", [check_generate_username, check_generate_usernames, check_generate_password,
                                   check_generate_test_id, check_make_test_case, check_generate_test_cases,
                                   check_generators_do_not_touch_global_random]),
    ("Milestone 4: timing decorator", [check_timer]),
    ("Milestone 5: lambda helpers", [check_sort_cases, check_slowest, check_count_by]),
    ("Milestone 5: integration report", [check_demo_report]),
    ("Milestone 0 and 6: git / retrospective files", [check_gitignore, check_retrospective]),
]


def main():
    passed = 0
    total = 0
    for title, checks in SECTIONS:
        print(f"\n== {title} ==")
        for check in checks:
            total += 1
            name = check.__name__.replace("check_", "")
            try:
                check()
                print(f"  PASS  {name}")
                passed += 1
            except AssertionError as error:
                print(f"  FAIL  {name}: {error}")
            except Exception as error:      # a crash is also a failure; show the type
                print(f"  FAIL  {name}: your code crashed with {type(error).__name__}: {error}")
    print(f"\n{passed}/{total} checks passed")
    if passed == total:
        print("ALL CHECKS PASSED: library, report and files are in place. Now finish the Definition of Done.")
    return 0 if passed == total else 1


if __name__ == "__main__":
    raise SystemExit(main())
