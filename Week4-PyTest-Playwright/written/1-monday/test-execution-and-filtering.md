# Test Execution and Filtering

## Learning Objectives

By the end of this lesson you will be able to:

- Run tests at every level: whole suite, folder, file, class, single function, using node IDs.
- Control output with `-v`, `-q`, `-s`, `-r`, `--tb`, and `--durations`.
- Select tests by **name** with `-k` and by **marker** with `-m`, and explain the difference.
- Stop early with `-x` and `--maxfail`, and re-run failures with `--lf`, `--ff`, and `--sw`.
- Use `--collect-only`, `--deselect`, and `--ignore` to control what runs.
- Read the PyTest summary line and understand exit codes.
- Put your favourite options in `addopts` and build a practical command cheat sheet for Project 1.

---

## Why This Matters

Writing tests is half the job; **running the right tests at the right time** is the other half. In the weekly epic, you move from a few tests today to a data-driven reporting framework on Wednesday and browser tests on Thursday and Friday. As the suite grows, running "everything" gets slower, and a failing test needs to be re-run quickly while you debug.

Knowing the command line well makes you faster and more professional:

- Debugging one failing test takes seconds instead of minutes.
- You can select the smoke suite for quick feedback and the regression suite for confidence.
- CI pipelines (automated build servers) call exactly these commands, and they decide pass/fail from the **exit code**.

In **Project 1: QE Foundations**, today's milestone is a PyTest suite for the utility functions with markers. This lesson gives you the commands to run, slice, and report on that suite.

---

## The Concept

### 1. The anatomy of a PyTest command

```
python -m pytest  [options]  [paths or node IDs]
```

- Without paths, PyTest uses `testpaths` from your config or the current directory.
- Options start with `-` (short) or `--` (long).
- Short options can be combined: `-vx` means `-v -x`.

### 2. Choosing **what** to run (by location)

```bash
python -m pytest                                                # everything under testpaths
python -m pytest tests/                                         # one folder
python -m pytest tests/test_utils.py                            # one file
python -m pytest tests/test_utils.py::test_add                  # one function
python -m pytest tests/test_utils.py::TestMath                  # one class
python -m pytest tests/test_utils.py::TestMath::test_add        # one method
python -m pytest tests/test_a.py tests/test_b.py                # several files
python -m pytest "tests/test_utils.py::test_add" "tests/test_utils.py::test_is_even"
```

The `::`-separated paths are **node IDs**, which you saw in *Test Discovery and Organization*. Tip: when a failure prints its node ID, copy and paste it into the command to re-run precisely that test.

### 3. Controlling **output**

#### 3.1 Verbosity: `-v`, `-vv`, `-q`

| Option | Effect |
|---|---|
| (default) | One character per test (`.` `F` `s`...) |
| `-v` | One line per test with its full node ID and `PASSED`/`FAILED` |
| `-vv` | Even more detail; full (untruncated) diffs in assertion failures |
| `-q` | Quiet: shorter header and summary |
| `-qq` | Even quieter |

Example with `-v`:

```
tests/test_utils.py::test_add_two_positive_numbers PASSED          [ 50%]
tests/test_utils.py::test_is_even_returns_true_for_four PASSED     [100%]
```

#### 3.2 Showing `print()` output: `-s`

By default PyTest **captures** anything your tests print, and only shows it if the test fails. This keeps output clean. To see prints live:

```bash
python -m pytest -s
```

`-s` is shorthand for `--capture=no`. It is useful for debugging; do not leave `print`-based checks in finished tests (use `assert`).

Other capture modes: `--capture=fd` (default), `--capture=sys`, `--capture=tee-sys` (show *and* capture).

#### 3.3 Traceback style: `--tb`

When a test fails, PyTest prints a traceback (the chain of calls leading to the error). You can choose how much:

| Option | Meaning |
|---|---|
| `--tb=auto` | Default; long for first and last failure, short for others |
| `--tb=long` | Full detail |
| `--tb=short` | One short block per failure |
| `--tb=line` | One line per failure (great overview) |
| `--tb=no` | No tracebacks |
| `--tb=native` | Standard Python traceback format |

When the suite has many failures, `--tb=line` or `--tb=short` helps you see the pattern first.

#### 3.4 The short summary: `-r`

`-r` takes letters that choose which outcomes to list at the end:

| Letter | Meaning |
|---|---|
| `f` | failed |
| `E` | errors |
| `s` | skipped |
| `x` | xfailed |
| `X` | xpassed |
| `p` | passed |
| `P` | passed with output |
| `a` | all except passed |
| `A` | all |

Common choice: `-ra` ("show everything notable"), which is why we put it in `addopts` earlier today. Example:

```
=========================== short test summary info ===========================
SKIPPED [1] tests/test_markers_demo.py:30: feature not built yet
XFAIL tests/test_markers_demo.py::test_round_half_up - BUG-204: Python rounds half to even
FAILED tests/test_utils.py::test_add - assert 4 == 5
```

#### 3.5 Finding slow tests: `--durations`

```bash
python -m pytest --durations=5           # show the 5 slowest test phases
python -m pytest --durations=0           # show all
```

Output lists time per test, helping you decide what to mark `slow`. (Wednesday's *Performance Profiling* lesson goes further. Today just remember the option exists.)

### 4. Choosing **which** tests to run: filtering by name with `-k`

`-k` takes an **expression** that is matched against test **names** (the node ID parts: file, class, function names). Matching is **case-insensitive substring** matching.

```bash
python -m pytest -k "add"                       # names containing "add"
python -m pytest -k "add or divide"             # either
python -m pytest -k "add and not negative"      # add but not negative
python -m pytest -k "TestMath"                  # a class name
python -m pytest -k "TestMath and test_add"     # a method within the class
python -m pytest -k "not slow"
```

Operators: `and`, `or`, `not`, parentheses. Quote the expression.

Notes:

- `-k` matches substrings of any part of the name, which is powerful but can match more than you expect (`-k add` also matches `test_address`).
- It also matches marker names on a test (markers are considered keywords), which makes `-k smoke` sometimes work. Prefer `-m` for markers because it is explicit and exact.

### 5. Choosing **which** tests to run: filtering by marker with `-m`

Covered in the previous lesson, but here is the full comparison.

| | `-k` | `-m` |
|---|---|---|
| Matches | Names (file, class, function) as substrings | Marker names, exactly |
| Needs setup | None | Markers registered (with `--strict-markers`) |
| Good for | Quick ad-hoc "run the tests about X" | Stable suite categories: smoke, regression |
| Risk | Over-matching because of substrings | Typos (prevented with `--strict-markers`) |

```bash
python -m pytest -m smoke
python -m pytest -m "regression and not slow"
python -m pytest -m smoke -k "add"             # both filters together: marker AND name
```

When you provide both, a test must satisfy **both** filters to run.

### 6. Failing fast and re-running failures

#### Stop early

```bash
python -m pytest -x               # stop after the first failure
python -m pytest --maxfail=3      # stop after 3 failures
```

Useful when a failure makes the rest meaningless, or during debugging so you do not scroll through 40 failures.

#### Re-run only what failed: the cache

PyTest remembers results in the `.pytest_cache` folder.

| Option | Behaviour |
|---|---|
| `--lf` / `--last-failed` | Run only tests that failed last time |
| `--ff` / `--failed-first` | Run all, but failed ones first |
| `--nf` / `--new-first` | Run tests from newest files first |
| `--sw` / `--stepwise` | Stop at the first failure; next run resumes from that test |
| `--cache-clear` | Delete the cache before running |

Typical debugging loop:

```bash
python -m pytest                  # 3 failures
python -m pytest --lf             # re-run just those 3 while you fix code
python -m pytest                  # full run to confirm nothing else broke
```

(If nothing failed last time, `--lf` runs everything by default; control it with `--lfnf=none` to run nothing instead.)

### 7. Seeing without running: `--collect-only`, `--deselect`, `--ignore`

```bash
python -m pytest --collect-only -q            # list node IDs, run nothing
python -m pytest -m smoke --collect-only -q   # which tests would a filter pick?
python -m pytest --deselect tests/test_utils.py::test_slow_one
python -m pytest --ignore=tests/legacy
```

Always do a `--collect-only` check when you create a new filter expression; it is a "dry run" that costs nothing.

### 8. Reading the result summary

The last line of a run looks like:

```
===== 2 failed, 10 passed, 1 skipped, 1 xfailed, 3 deselected in 1.42s =====
```

| Word | Meaning |
|---|---|
| passed | Completed with no exceptions |
| failed | A test raised an assertion error or other exception |
| error | A problem outside the test body (collection, setup) |
| skipped | `skip`/`skipif` or `pytest.skip()` |
| xfailed | Expected failure that did fail |
| xpassed | Expected failure that passed |
| deselected | Excluded by `-k`, `-m`, or `--deselect` |

### 9. Exit codes

When PyTest finishes it returns a number to the operating system. CI tools read this number. Scripts can check it too.

| Code | Meaning |
|---|---|
| 0 | All tests passed (xfail/skip do not break this) |
| 1 | Some tests failed |
| 2 | Run was interrupted by the user (Ctrl+C) |
| 3 | Internal error in PyTest |
| 4 | Command-line usage error (e.g. bad option) |
| 5 | No tests were collected |

Check the code right after a run:

```bash
# Linux / macOS
python -m pytest; echo $?

# Windows Command Prompt
python -m pytest
echo %ERRORLEVEL%

# Windows PowerShell
python -m pytest; $LASTEXITCODE
```

Exit code **5** surprises beginners: a filter that matches nothing (for example a typo in `-k`) is not "green"; it is reported as "no tests ran". That is helpful in CI.

### 10. Saving your favourite options

Put defaults in `pytest.ini` so everyone gets them:

```ini
[pytest]
addopts = -ra --strict-markers --tb=short
testpaths = tests
```

Options given on the command line are appended after `addopts`, so later ones can override earlier ones (for example `--tb=long` on the command line beats `--tb=short` from `addopts`).

You can also use the environment variable `PYTEST_ADDOPTS`:

```bash
# Linux/macOS
PYTEST_ADDOPTS="-vv" python -m pytest
```

### 11. Useful extras

| Option | Purpose |
|---|---|
| `--version` | Print PyTest version |
| `--help` | List all options |
| `--markers` | List registered markers |
| `--setup-show` | Show setup/teardown steps (becomes relevant on Tuesday) |
| `--junitxml=report.xml` | Write a JUnit-style XML report; CI tools read it |
| `-p no:cacheprovider` | Disable the cache plugin |
| `--rootdir=PATH` | Force the root directory |
| `-W error` | Turn Python warnings into errors |
| `--co` | Alias for `--collect-only` |

HTML reports are produced with a plugin, and we will create them on Wednesday in *HTML Reporting*.

---

## Code Examples with Line-by-Line Explanations

Use this small suite throughout the examples.

`pytest.ini`:

```ini
[pytest]
testpaths = tests
pythonpath = .
addopts = -ra --strict-markers
markers =
    smoke: quick sanity checks
    regression: broad pre-release checks
    slow: slow tests
```

`src/calc.py`:

```python
def add(a, b):
    return a + b


def subtract(a, b):
    return a - b


def multiply(a, b):
    return a * b


def divide(a, b):
    if b == 0:
        raise ZeroDivisionError("division by zero")
    return a / b
```

`tests/test_calc.py`:

```python
import time
import pytest

from src.calc import add, subtract, multiply, divide


@pytest.mark.smoke
def test_add_positive():
    assert add(2, 3) == 5


@pytest.mark.regression
def test_add_negative():
    assert add(-2, -3) == -5


@pytest.mark.smoke
def test_subtract_basic():
    assert subtract(5, 3) == 2


@pytest.mark.regression
def test_multiply_by_zero():
    assert multiply(7, 0) == 0


class TestDivide:
    @pytest.mark.smoke
    def test_divide_evenly(self):
        assert divide(10, 2) == 5

    @pytest.mark.regression
    def test_divide_by_zero_raises(self):
        with pytest.raises(ZeroDivisionError):
            divide(1, 0)


@pytest.mark.slow
def test_slow_operation():
    time.sleep(1)
    assert add(1, 1) == 2


def test_deliberate_failure():
    assert multiply(2, 3) == 7          # wrong on purpose, to practise failure handling
```

### Walk-through of commands

**1. Run everything**

```bash
python -m pytest
```

Expected summary: `1 failed, 7 passed` (the deliberate failure plus 7 passes). Because `-ra` is in `addopts`, the failure appears in the short summary.

**2. Verbose, with only the first failure**

```bash
python -m pytest -v -x
```

Order: tests run in file order (top to bottom). The suite stops at the deliberate failure, which is last, so all others pass first. If the failing test were earlier, remaining tests would be skipped from the run (not shown).

**3. Only smoke tests**

```bash
python -m pytest -m smoke -v
```

Selected: `test_add_positive`, `test_subtract_basic`, `TestDivide::test_divide_evenly`. Others show as `deselected`.

**4. Everything except slow**

```bash
python -m pytest -m "not slow"
```

**5. Name-based**

```bash
python -m pytest -k "add" -v
```

Matches `test_add_positive`, `test_add_negative`. Note: it would also match any name containing "add", including "address"; none here.

```bash
python -m pytest -k "TestDivide and not zero" -v
```

Matches `TestDivide::test_divide_evenly` only. Explanation: `TestDivide` matches the class name; `not zero` excludes the method whose name contains `zero`.

**6. Combine filters**

```bash
python -m pytest -m smoke -k "divide" -v
```

Only `TestDivide::test_divide_evenly`, because it must be both `smoke` and have `divide` in its name.

**7. Failure workflow**

```bash
python -m pytest --tb=short          # compact failure info
python -m pytest --lf -v             # re-run only test_deliberate_failure
```

Now fix the test by changing `7` to `6`, and run:

```bash
python -m pytest --lf                # that test now passes
python -m pytest                     # full run, all green
```

**8. Slow tests**

```bash
python -m pytest --durations=3
```

The report shows `test_slow_operation` near the top at ~1.00s.

**9. Dry-run**

```bash
python -m pytest -m "smoke or regression" --collect-only -q
```

Prints seven node IDs and `7 tests collected`, running nothing.

**10. Exit codes**

```bash
python -m pytest -k "nothing_matches_this"
echo %ERRORLEVEL%     # on Windows cmd; expect 5 (no tests collected)
```

**11. Seeing prints**

Add `print("calculating...")` to any test, run normally (not shown if the test passes), then run with `-s` to see it.

---

## Real-World Scenarios

1. **Debugging a flaky nightly failure.** The build log shows `FAILED tests/test_calc.py::TestDivide::test_divide_by_zero_raises`. The engineer copies the node ID, runs it alone with `-vv --tb=long`, finds the cause, and fixes it, then runs `--lf` and finally the full suite.
2. **Pre-commit smoke run.** `python -m pytest -m smoke -x -q` takes seconds and stops at the first problem.
3. **CI gate.** The pipeline runs `python -m pytest -m "not slow" --junitxml=results.xml`. A non-zero exit code fails the build; the XML file feeds the dashboard.
4. **Speed investigation.** The suite takes 12 minutes. `--durations=10` reveals three tests taking 8 of them. The team marks them `slow` and runs them in a separate job.
5. **Focus on a feature.** A developer changing division logic runs `-k divide` for immediate feedback.

---

## Common Mistakes

| Mistake | Consequence | Fix |
|---|---|---|
| Running from the wrong directory | Config not found, paths wrong | `cd` to the project root. |
| Unquoted expressions: `-k not slow` | Shell passes `not` and `slow` as separate arguments, so PyTest treats `slow` as a path | `-k "not slow"` |
| Using `-k` to select markers | Over-matching or misses | Use `-m` for markers. |
| Assuming `-k add` matches only the `add` function | Substring matching also catches `address`, `padding` | Be specific: `-k "test_add_"` or use markers. |
| Ignoring exit code 5 | A filter typo makes CI pass silently if only the printed output is checked | Treat exit code 5 as an error in scripts. |
| Debugging with `print` and forgetting `-s` | No output shown | Use `-s`, or better, rely on assertion introspection. |
| Using `--lf` when nothing failed last time | It runs everything, which may surprise you | Use `--lfnf=none` if you want nothing. |
| Leaving `-x` in `addopts` | You never see the full list of failures | Use `-x` only ad hoc. |
| Forgetting `.pytest_cache` is stale after big changes | Strange `--lf` behaviour | `--cache-clear`. |
| Reading only the last line | Missing skipped and xfailed tests | Keep `-ra` in `addopts`. |

---

## Practice Exercises

### Exercise 1: Run at every level
Using the sample suite, write the command to run (a) just `test_add_positive`, (b) the class `TestDivide`, (c) only `test_divide_by_zero_raises`, (d) the whole file.

**Solution:**

```bash
python -m pytest tests/test_calc.py::test_add_positive
python -m pytest tests/test_calc.py::TestDivide
python -m pytest tests/test_calc.py::TestDivide::test_divide_by_zero_raises
python -m pytest tests/test_calc.py
```

### Exercise 2: Filter drills
Write the command and predict the selected tests:

1. Everything marked `regression`.
2. Everything that is `smoke` but with a name that does *not* contain `divide`.
3. Every test whose name includes `add` or `subtract`.
4. Everything except slow and except the deliberate failure.

**Solutions:**

```bash
python -m pytest -m regression
python -m pytest -m smoke -k "not divide"
python -m pytest -k "add or subtract"
python -m pytest -m "not slow" -k "not deliberate"
```

### Exercise 3: Output control
Run the suite with `-q`, `-v`, `-vv`. Compare the outputs and write down one situation where you would prefer each.

### Exercise 4: The failure loop
Using the deliberate failure: run the suite, re-run with `--lf`, fix the test, re-run with `--lf`, then run the full suite. Write the sequence and the summary line at each step.

### Exercise 5: Exit codes
Produce exit codes 0, 1, and 5 deliberately and record the command that gave each.

*Hint:* passing suite for 0; the deliberate failure for 1; an unmatched `-k` for 5.

### Exercise 6: Find slow tests
Add three tests that call `time.sleep` for different durations. Use `--durations=3` to list them in order. Mark the slowest as `slow` and run the suite excluding them.

### Exercise 7: Fast-feedback pipeline
Write three commands that a team could use: (a) pre-commit, (b) pull-request check, (c) nightly build. Justify each in one sentence.

*Possible answer:* (a) `python -m pytest -m smoke -x -q`; (b) `python -m pytest -m "not slow"`; (c) `python -m pytest --junitxml=results.xml`.

### Exercise 8 (challenge): Cheat sheet
Create a one-page `RUNNING_TESTS.md` for the Project 1 repository listing at least ten commands from this lesson with one-line descriptions, plus the exit-code table.

---

## Summary

- Run tests at any level using paths and node IDs: `file::Class::method`.
- Control output with `-v/-vv/-q`, `-s` (show prints), `--tb=...` (traceback style), `-ra` (summary of non-passing), and `--durations=N` (slowest tests).
- Filter by **name** with `-k` (substring, case-insensitive) and by **marker** with `-m` (exact names); both accept `and`, `or`, `not`, and parentheses; combine them to require both.
- Use `-x`, `--maxfail`, `--lf`, `--ff`, and `--sw` to speed up debugging.
- Use `--collect-only`, `--deselect`, and `--ignore` to preview and control what runs.
- Read the summary line and the **exit code** (0 pass, 1 failures, 2 interrupted, 3 internal error, 4 usage error, 5 no tests).
- Store default options in `addopts` in your configuration file.
- Tomorrow (Tuesday) you will learn fixtures and parametrization, which build directly on everything you can now run and filter.

---

## Additional Resources

- PyTest: Usage and invocations: https://docs.pytest.org/en/stable/how-to/usage.html
- PyTest: How to invoke pytest (command-line flags reference): https://docs.pytest.org/en/stable/reference/reference.html#command-line-flags
- PyTest: How to re-run failed tests and maintain state between test runs (cache): https://docs.pytest.org/en/stable/how-to/cache.html
