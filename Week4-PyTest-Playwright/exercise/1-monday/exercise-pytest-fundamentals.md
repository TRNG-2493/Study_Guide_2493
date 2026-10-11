# Lab: Automate the Project 1 Utility Tests with PyTest and Markers

**Week 4 - Day 1 (Monday) | Mode A: Implementation (Code Lab) | Individual | 2-3 hours**
**Project 1 - QE Foundations | Milestone M1: "PyTest suite with markers"**

---

## 1. The scenario

Your team's Project 1 repo contains a small module of utility functions (`qe_utils.py`): username validation, a shopping-cart total, a temperature converter, a grade mapper, a word counter and a text truncator. Until now they were verified only with **manual test cases**. Every release someone re-types the same inputs by hand. It is slow, boring and error-prone.

Your job today: turn those manual checks into an **automated PyTest suite**, tag the tests with **markers** so the team can run "just the quick smoke checks" before a commit and "everything" before a release, and document what you learned. While you are at it, one of the functions has a **hidden bug**. A good tester finds it with boundary-value tests and records it responsibly (not by silently deleting the failing test).

## 2. Learning objectives

By the end you can:
1. Create a virtual environment, install PyTest and configure `pytest.ini` (`testpaths`, `--strict-markers`, registered markers).
2. Write function-style and class-style tests using Arrange / Act / Assert, with descriptive names.
3. Choose the right assertion: plain `assert`, `pytest.approx` for floats, `pytest.raises(..., match=...)` for exceptions.
4. Apply markers at function and class level; use `skip`, `skipif` and `xfail`.
5. Select tests with `-m`, `-k` and node IDs, and explain exit codes.

Lessons used (all from this week's Monday written content): `pytest-installation-and-configuration`, `test-functions-and-classes`, `assertions-and-assertion-introspection`, `test-discovery-and-organization`, `markers`, `test-execution-and-filtering`. Nothing from Tuesday onward (fixtures, parametrize, mocking) is needed. **Do not use fixtures or `parametrize` today**; plain repeated tests are intentional.

## 3. Prerequisites

- Python 3.9+ and a terminal (PowerShell, Git Bash, macOS/Linux terminal).
- Read the six Monday lessons and attended the demo.
- A Project 1 Git repo (or create a new folder `project1-qe-foundations` and `git init`).
- Use a folder path **without spaces** (Windows tip from the demo).

## 4. Setup (about 10 minutes)

1. Copy the contents of `starter_code/` into your Project 1 repo (so `qe_utils.py`, `pytest.ini`, `requirements.txt`, `check_milestone.py`, `SELECTION_LOG.md` sit at the repo root and `tests/` beside them).
2. Create and activate a virtual environment:
   - PowerShell: `python -m venv .venv` then `.venv\Scripts\Activate.ps1`
   - Git Bash / macOS / Linux: `python3 -m venv .venv` then `source .venv/bin/activate` (Git Bash on Windows: `source .venv/Scripts/activate`)
3. `python -m pip install -r requirements.txt`, then `python -m pytest --version`.
4. Add `.venv/`, `__pycache__/`, `.pytest_cache/` to `.gitignore`.
5. Run `python -m pytest`. **Expected: errors**, because `pytest.ini` uses `--strict-markers` but the markers are not registered yet. That is Task 2. Always run tests with `python -m pytest` from the repo root.

## 5. Core tasks (step by step)

Work through in order. Commit after each task with a clear message.

### Task 1 - Read before you test (10 min)
Open `qe_utils.py`. For each function, write down (in a scratch note, not in the file) the rules from its docstring: valid inputs, invalid inputs, boundaries. **Do not edit `qe_utils.py`.** The docstring is the requirement; if the code disagrees with it, you have found a bug.

### Task 2 - Configure and register markers (10 min)
In `pytest.ini`, register four markers with one-line descriptions: `smoke`, `regression`, `boundary`, `slow`. Run `python -m pytest --markers` and confirm they appear. Run `python -m pytest`: errors should disappear and you should see the TODO tests fail (26 failures expected, 3 passes from the worked examples).

### Task 3 - Implement the happy-path and boundary tests (50 min)
In `tests/test_text_utils.py`, `tests/test_numbers.py` and `tests/test_cart.py`, replace each `pytest.fail("TODO: implement")` with a real test. Rules:
- Keep Arrange / Act / Assert visible (blank lines or comments are fine).
- Apply the markers named in each TODO comment. Put `@pytest.mark.regression` on the **whole** `TestCartTotal` class.
- One behaviour per test (two closely related asserts are allowed where the TODO says so).
- Do not rename the tests; the self-check and your selection log depend on the names.
- Study the three **worked examples** first (the first test in each file).

### Task 4 - Pick the right assertion (20 min)
Finish the tests that need special assertions:
- `pytest.approx` for float comparisons (body temperature and rounded cart total).
- `pytest.raises(ExceptionType, match="...")` for every "raises" test. The `match` text must come from the function's real message (read `qe_utils.py`, which you are allowed to read).
- Deliberately break one assertion (for example expect `5` instead of `4` words), run it, and read the introspection output. Add 2 sentences to `SELECTION_LOG.md` under a heading "Reading a failure" describing what PyTest showed you. Then restore the assertion.

### Task 5 - Skip and slow (10 min)
Add the three tests described in the TODO comments:
- `test_..._skipif_example` in `test_numbers.py` using `@pytest.mark.skipif(...)`.
- `test_large_cart_of_10000_items` in `TestCartTotal`, marked `slow`.
- `test_discount_coupons_not_supported_yet` in `TestCartTotal`, using `@pytest.mark.skip(reason=...)`.

### Task 6 - Find the bug, record it with xfail (15 min)
Complete `test_truncate_text_exactly_max_len_is_unchanged` **exactly as the docstring of `truncate` says**. Run it. It fails. Decide: is the test wrong or the code wrong? (Re-read the docstring.) Then mark the test:
`@pytest.mark.xfail(reason="BUG: <one-line explanation>", strict=True)`
and confirm the run now shows `xfailed` and exits green. In `SELECTION_LOG.md` question 3, explain what `strict=True` does when someone later fixes the bug. **Do not edit `qe_utils.py` in the core tasks.** Testers report bugs; they do not silently patch them.

### Task 7 - Selection practice and log (15 min)
Complete the table and questions in `SELECTION_LOG.md`: run each command, record how many tests it selected, and write one sentence on when a team would use it. (Tip: `--collect-only -q` lists IDs without running them.)

### Task 8 - Milestone check and submit (10 min)
Run `python check_milestone.py` until every line says `[PASS]`. Then submit (Section 9).

## 6. Stretch tasks (optional, in rough order of difficulty)

- **S1 - Run one test by node ID and by class:** `python -m pytest tests/test_cart.py::TestCartTotal -v`. Add the commands you used to `SELECTION_LOG.md`.
- **S2 - Module-level marker:** put `pytestmark = pytest.mark.regression` in `test_cart.py` instead of the class decorator and explain the difference in 2 sentences.
- **S3 - Fix the bug:** change `>=` to `>` in `truncate`, re-run, and observe `XPASS(strict)` failing. Remove the `xfail` marker, and note it in your log. (Commit the fix separately: "fix: truncate no longer cuts exact-length text".)
- **S4 - Add 3 new boundary tests of your own** for functions where you spotted a missing case (hint: `letter_grade(59)`, `letter_grade(60)`, `calculate_cart_total` with a `0.0` price).
- **S5 - Exit codes:** record the exit code for a green run (0), a failing run (1), `-k zzzz` (5) and the typo-in-marker case (2). On Windows PowerShell use `$LASTEXITCODE`; in Bash use `echo $?`.

## 7. Project 1 - QE Foundations milestone

> Instructors: no Project 1 specification was supplied when this exercise was authored. The milestone below is a sensible default aligned with the Week 4 log and the Monday demo; **please adjust it to match your actual Project 1 brief** (module names, thresholds, repo layout).

**Milestone M1 (due end of Monday): "Automated utility tests with markers."**
Your Project 1 repository must contain:
1. A `tests/` folder with PyTest tests for all functions in `qe_utils.py` (at least 25 tests; the starter provides 29 and the self-check counts the rest).
2. `pytest.ini` with `testpaths`, `--strict-markers` and the four registered markers.
3. A working `smoke` subset (at least 6 tests) that the team can run with `python -m pytest -m smoke` in a few seconds.
4. At least one `skip`/`skipif`, and one documented known bug via `xfail`.
5. `SELECTION_LOG.md` completed (the start of your Project 1 test documentation).
6. A clean git history (at least 4 commits with meaningful messages).

**Why it matters:** Tuesday you will refactor this same suite with fixtures and parametrization, Wednesday you will complete the framework and reporting, and Thursday/Friday you will move on to browser tests with Playwright, which also run on PyTest and markers. Anything you leave sloppy today you will refactor later.

## 8. Definition of Done / rubric (100 points)

| Area | Points | "Done" means |
|---|---|---|
| Setup and config | 10 | venv + pinned `requirements.txt`; `pytest.ini` has `--strict-markers` and 4 registered markers with descriptions; `python -m pytest` works from the repo root |
| Test quality (Task 3) | 25 | All TODO tests implemented; AAA structure visible; descriptive names; one behaviour per test; no test duplicated or trivially true (`assert True`) |
| Assertions (Task 4) | 15 | `approx` for floats; `raises` with correct exception type and `match`; "Reading a failure" notes present |
| Markers (Tasks 2, 3, 5) | 15 | Markers match the TODO instructions; class-level marker used; `smoke` suite is fast and meaningful; `skip`, `skipif` have reasons |
| Bug handling (Task 6) | 10 | Bug found, test follows the docstring, `xfail(strict=True)` with a clear reason; `qe_utils.py` untouched in the core submission |
| Selection log (Task 7) | 10 | Table filled with correct counts; questions answered in own words |
| Milestone and hygiene | 10 | `check_milestone.py` all `[PASS]`; `.gitignore`; at least 4 meaningful commits |
| Stretch | +5 bonus | Any two stretch tasks done correctly |

Final run must look like: `N passed, 1 skipped, 1 xfailed` with exit code 0 (the `skipif` test passes on current Python, so one skip comes from `skip`).

## 9. Deliverables and submission

1. Push your Project 1 repo (branch `week4-monday-pytest`) and open a pull request, or zip the folder without `.venv`, as your instructor directs.
2. Include: `qe_utils.py` (unchanged), `pytest.ini`, `requirements.txt`, `tests/`, `SELECTION_LOG.md`, `.gitignore`.
3. Paste the output of `python check_milestone.py` and of `python -m pytest -q` into the PR description (or a `RESULTS.txt`).
4. Submit before the next morning's stand-up.

## 10. Hints (try before reading)

- **PyTest does not find my tests:** file names must start with `test_`, functions with `test`, classes with `Test` (no `__init__`).
- **`ERROR ... not found in markers configuration`:** the marker is spelled differently from the registration, or not registered.
- **Float test fails with `0.30000000000000004`:** use `pytest.approx`.
- **`raises` test fails with "Regex pattern did not match":** print the real message, copy a stable part of it into `match`.
- **Stacking markers:** put several `@pytest.mark.x` lines above the function.
- **`-k` and `-m` combined** both must be true for a test to run.
- **Bug search:** test exactly at the boundary, one below, one above.
- **Counting selected tests:** the final line says `N passed, M deselected`.
- **Import error `No module named qe_utils`:** you are not in the repo root, or you used `pytest` instead of `python -m pytest`.

## 11. Suggested time plan (about 2 h 30 min)

| Time | Activity |
|---|---|
| 0:00-0:10 | Setup (Section 4) |
| 0:10-0:20 | Task 1 - read requirements |
| 0:20-0:30 | Task 2 - markers and config |
| 0:30-1:20 | Task 3 - implement tests |
| 1:20-1:40 | Task 4 - assertions, read a failure |
| 1:40-1:50 | Task 5 - skip, skipif, slow |
| 1:50-2:05 | Task 6 - bug and xfail |
| 2:05-2:20 | Task 7 - selection log |
| 2:20-2:30 | Task 8 - check and submit |
| Any extra time | Stretch tasks |

## 12. Files in this package

- `starter_code/` - runnable scaffold (`qe_utils.py`, `pytest.ini`, `requirements.txt`, `tests/` with TODOs, `SELECTION_LOG.md`, `check_milestone.py`).
- `solution/` - **instructor only**, do not share with trainees before submission.

*Note: the lab uses a different set of utility functions than the live demo (which used `add`, `divide`, `apply_discount` etc.), so apply the same skills to new code rather than copying the demo tests.*
