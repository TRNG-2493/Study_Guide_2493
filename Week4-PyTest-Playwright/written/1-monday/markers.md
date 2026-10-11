# Markers

## Learning Objectives

By the end of this lesson you will be able to:

- Explain what a PyTest marker is and why teams use markers to categorise tests.
- Apply markers to functions, classes, and whole modules (`pytestmark`).
- Use the built-in markers `skip`, `skipif`, `xfail`, and recognise `parametrize` and `usefixtures`.
- Create and **register** custom markers such as `smoke`, `regression`, and `slow`.
- Use `--strict-markers` to prevent typos.
- Combine several markers on one test and explain how they stack.
- List registered markers with `pytest --markers`.
- Apply markers to organise the Project 1 test suite.

---

## Why This Matters

The weekly epic ends with a reporting framework and browser automation. By Friday your suite will contain fast utility tests, data-driven tests, and slower browser tests. Running everything on every save is impractical. Real teams need to answer questions like:

- "Run only the quick sanity checks before I commit."
- "Run the full regression suite overnight."
- "Skip the Windows-only tests on the Linux build server."
- "This test is broken because of known bug #204. Do not fail the build, but keep it visible."

**Markers** are PyTest's answer. They are labels you attach to tests so that you can **select, skip, or treat them specially**. In **Project 1: QE Foundations**, you will tag your automated utility tests today (for example `smoke` and `regression`), and the exercise asks you to use these markers to run subsets. Tomorrow and Wednesday you will reuse the same markers for fixtures, data-driven tests, and reports.

**Analogy:** think of markers as coloured sticky notes on test cases in a test management tool. Red for "smoke", blue for "regression", yellow for "slow". Once labelled, you can ask for "show me all red notes".

---

## The Concept

### 1. What is a marker?

A **marker** is metadata attached to a test, written as a **decorator**: `@pytest.mark.<name>`. It does not change what the test does by itself. Instead PyTest (or you, via the command line) can **read** the metadata and act on it.

```python
import pytest


@pytest.mark.smoke
def test_add():
    assert 1 + 1 == 2
```

Line by line:

- `import pytest`: the marker tools live in the `pytest` package.
- `@pytest.mark.smoke`: a *decorator*, a line starting with `@` placed above a function that wraps or annotates it. Here it attaches a marker named `smoke`.
- `def test_add()`: the test itself, unchanged.

A **decorator** in Python is just a function applied to another function; `@x` above `def f()` is shorthand for `f = x(f)`. You do not need to write decorators yourself to use markers, only to apply them.

### 2. Two kinds of markers

| Kind | Examples | Who defines the behaviour |
|---|---|---|
| **Built-in markers** | `skip`, `skipif`, `xfail`, `parametrize`, `usefixtures`, `filterwarnings` | PyTest itself gives them special behaviour. |
| **Custom markers** | `smoke`, `regression`, `slow`, `api`, `ui` | You define the name and meaning; PyTest only records them. You *select* by name with `-m`. |

### 3. Built-in markers

#### 3.1 `skip`: do not run this test

```python
@pytest.mark.skip(reason="waiting for the new validation rules")
def test_new_validation():
    assert False
```

The test is never executed and appears as `SKIPPED` with the reason. Always give a `reason`; it shows up in the summary when you run with `-rs` or `-ra`.

Skip imperatively (inside a test or setup) with `pytest.skip()`:

```python
def test_needs_something():
    if not something_available():
        pytest.skip("something is not available on this machine")
    ...
```

`pytest.skip()` raises a special exception to stop the test immediately, so code after it does not run.

#### 3.2 `skipif`: skip conditionally

```python
import sys
import pytest


@pytest.mark.skipif(sys.version_info < (3, 10), reason="requires Python 3.10+")
def test_structural_pattern_matching_feature():
    assert True


@pytest.mark.skipif(sys.platform != "win32", reason="Windows only")
def test_windows_path_behaviour():
    assert True
```

The first argument is a **boolean condition** evaluated at import time. If true, the test is skipped. Common conditions: Python version, operating system (`sys.platform`), environment variables, or whether an optional library can be imported.

You can define a condition once and reuse it:

```python
import os
import pytest

requires_ci = pytest.mark.skipif(os.getenv("CI") is None, reason="runs only on the CI server")


@requires_ci
def test_one():
    assert True


@requires_ci
def test_two():
    assert True
```

#### 3.3 `xfail`: expected failure

`xfail` means "this test is **expected to fail** because of a known problem". PyTest still **runs** it, which differentiates it from `skip`.

```python
@pytest.mark.xfail(reason="BUG-204: rounding is wrong for halves")
def test_round_half_up():
    assert round(2.5) == 3        # Python rounds half to even, so this returns 2
```

Outcomes:

| What happens | Reported as | Build effect |
|---|---|---|
| The test fails | `XFAIL` (shown `x`) | Does not fail the build |
| The test passes | `XPASS` (shown `X`) | Does not fail the build, unless `strict=True` |

Parameters:

- `reason="..."`: strongly recommended; link the bug ID.
- `strict=True`: an unexpected pass **fails** the suite, forcing you to remove the marker once the bug is fixed.
- `raises=SomeError`: only treat failure as expected if that exception type is raised, so a different error is still reported as a real failure.
- `condition`: expected failure only when true, like `skipif`.

```python
@pytest.mark.xfail(raises=ZeroDivisionError, strict=True, reason="BUG-317")
def test_known_division_bug():
    1 / 0
```

You can make strict mode the default for the project in `pytest.ini` with `xfail_strict = true`.

**Skip versus xfail, in one sentence:** use `skip` when the test *cannot or should not run*; use `xfail` when the test *runs and is known to fail*, so you will notice when it starts passing.

#### 3.4 `parametrize` and `usefixtures` (just a mention)

PyTest has two more important built-in markers. `@pytest.mark.parametrize` runs one test with many data sets, and `@pytest.mark.usefixtures` applies setup code. **We will cover both in depth on Tuesday** (fixtures, parametrization) and use them again on Wednesday (data-driven design), so do not worry about them today.

### 4. Custom markers

A custom marker is any name you invent:

```python
@pytest.mark.smoke
def test_login_utility_basic():
    ...

@pytest.mark.regression
def test_login_utility_all_edge_cases():
    ...

@pytest.mark.slow
def test_large_data_processing():
    ...
```

Common marker vocabularies in QA teams:

| Marker | Typical meaning |
|---|---|
| `smoke` | Small set (minutes) proving the basics work. Run on every build. |
| `regression` | Broad checks proving old features still work. Run nightly or pre-release. |
| `slow` | Tests that take long; excluded from quick runs. |
| `api`, `ui`, `unit` | The layer being tested. |
| `negative` | Invalid-input / error-path tests. |
| `bug_123` or `wip` | Temporary labels for traceability. |

Keep the vocabulary small. Ten well-understood markers beat fifty confusing ones.

### 5. Registering markers (very important)

If you use an unregistered custom marker, PyTest still runs the test but prints a warning:

```
PytestUnknownMarkWarning: Unknown pytest.mark.smoke - is this a typo?
```

Two reasons to register markers:

1. It documents their meaning for the team.
2. With `--strict-markers`, **a typo becomes an error** instead of a silent mistake. Without strictness, `@pytest.mark.smok` quietly creates a new marker and the test would never be selected by `-m smoke`, so your "smoke" test silently never runs in the smoke suite!

Register in `pytest.ini`:

```ini
[pytest]
addopts = -ra --strict-markers
markers =
    smoke: quick sanity checks, run on every build
    regression: broad checks run before releases
    slow: tests that take more than a few seconds
    negative: invalid-input and error-path tests
```

Or in `pyproject.toml`:

```toml
[tool.pytest.ini_options]
addopts = "-ra --strict-markers"
markers = [
    "smoke: quick sanity checks, run on every build",
    "regression: broad checks run before releases",
    "slow: tests that take more than a few seconds",
    "negative: invalid-input and error-path tests",
]
```

List all markers (built-in and yours) with descriptions:

```bash
python -m pytest --markers
```

### 6. Applying markers at different levels

#### On a function

```python
@pytest.mark.smoke
def test_one():
    ...
```

#### On a class (applies to **every** test method inside)

```python
@pytest.mark.regression
class TestDivide:
    def test_even_division(self):
        assert 10 / 2 == 5

    def test_fractional_division(self):
        assert 1 / 4 == 0.25
```

Both methods carry the `regression` marker.

#### On a whole module with `pytestmark`

Define a module-level variable named exactly `pytestmark`:

```python
import pytest

pytestmark = pytest.mark.regression          # one marker for every test in this file
# or several: pytestmark = [pytest.mark.regression, pytest.mark.slow]


def test_a():
    ...

def test_b():
    ...
```

#### Stacking multiple markers

```python
@pytest.mark.smoke
@pytest.mark.negative
def test_divide_by_zero():
    ...
```

Markers combine. Marker selection (`-m`) sees **all** of them, including those inherited from the class and module. A test in a `regression` class that is also decorated `smoke` has both labels.

### 7. Selecting tests by marker: `-m`

Select with the `-m` option and a **marker expression**:

```bash
python -m pytest -m smoke                   # only smoke tests
python -m pytest -m "not slow"              # everything except slow
python -m pytest -m "smoke or regression"   # either label
python -m pytest -m "regression and not slow"
python -m pytest -m "(smoke or regression) and not negative"
```

Rules:

- Use `and`, `or`, `not`, and parentheses.
- Quote the expression so the shell does not break it.
- Selection uses marker **names only**; it cannot look at marker arguments (such as the `reason`).

Selection by name with `-k` is different and is covered in the lesson *Test Execution and Filtering*, where both options are compared side by side.

### 8. Markers do not change code behaviour (except built-ins)

A custom marker is only a label. `@pytest.mark.smoke` does not make a test faster, run first, or run at all. It only helps *you* choose. If you run `python -m pytest` with no `-m`, **all** tests run regardless of markers (except skipped ones).

### 9. Inspecting markers programmatically (preview)

In later lessons you will use hooks and fixtures to read markers. For now, the key idea is that markers are stored on the test item and can be examined, which is how the HTML reports built on Wednesday can group tests by marker.

---

## Code Examples with Line-by-Line Explanations

### Example 1: A fully configured marker setup

`pytest.ini`:

```ini
[pytest]
minversion = 8.0
testpaths = tests
pythonpath = .
addopts = -ra --strict-markers
xfail_strict = true
markers =
    smoke: quick sanity checks
    regression: broad pre-release checks
    slow: tests that take a long time
    negative: invalid-input tests
```

- `xfail_strict = true`: every `xfail` becomes strict by default (an unexpected pass fails the run).
- `-ra`: print a short summary for all non-passing outcomes (skipped, xfail, failed...). This ensures that skip and xfail reasons are visible.

`src/utils.py`:

```python
import time


def add(a, b):
    return a + b


def divide(a, b):
    return a / b


def slow_sum(numbers):
    time.sleep(1)               # pretend this is an expensive operation
    return sum(numbers)
```

`tests/test_markers_demo.py`:

```python
import sys
import pytest

from src.utils import add, divide, slow_sum


@pytest.mark.smoke
def test_add_two_numbers():
    assert add(2, 3) == 5


@pytest.mark.smoke
@pytest.mark.regression
def test_add_negative_numbers():
    assert add(-2, -3) == -5


@pytest.mark.negative
@pytest.mark.regression
def test_divide_by_zero_raises():
    with pytest.raises(ZeroDivisionError):
        divide(1, 0)


@pytest.mark.slow
@pytest.mark.regression
def test_slow_sum_of_large_list():
    assert slow_sum(range(1000)) == 499500


@pytest.mark.skip(reason="feature not built yet")
def test_future_feature():
    assert False


@pytest.mark.skipif(sys.platform == "win32", reason="POSIX-only behaviour")
def test_posix_only():
    assert True


@pytest.mark.xfail(reason="BUG-204: Python rounds half to even")
def test_round_half_up():
    assert round(2.5) == 3
```

Explanation:

- `slow_sum` sleeps for one second to simulate a slow test; `sum(range(1000))` is `0 + 1 + ... + 999 = 499500`.
- `test_add_negative_numbers` has two markers, so it appears in both the `smoke` and `regression` selections.
- `test_future_feature` is skipped. `test_posix_only` is skipped on Windows and runs elsewhere.
- `test_round_half_up` fails (Python's `round(2.5)` is `2`), so it is reported as `XFAIL`, not a red failure.

Commands to try:

```bash
python -m pytest -m smoke -v
python -m pytest -m "not slow" -v
python -m pytest -m "regression and not slow" -v
python -m pytest -m "smoke or negative" --collect-only -q
python -m pytest --markers
```

Expected results (approximate):

| Command | Which tests run |
|---|---|
| `-m smoke` | `test_add_two_numbers`, `test_add_negative_numbers` |
| `-m "not slow"` | everything except `test_slow_sum_of_large_list` |
| `-m "regression and not slow"` | `test_add_negative_numbers`, `test_divide_by_zero_raises` |
| `-m "smoke or negative"` | first two plus `test_divide_by_zero_raises` |

Note: unselected tests are reported as *deselected*, e.g. `5 deselected`.

### Example 2: Class-level and module-level markers

```python
import pytest

pytestmark = pytest.mark.regression            # applies to everything in this module


@pytest.mark.smoke                             # applies to every method in this class
class TestAdd:
    def test_small_numbers(self):
        assert 1 + 1 == 2

    def test_zero(self):
        assert 0 + 0 == 0


class TestSubtract:
    def test_basic(self):
        assert 5 - 3 == 2

    @pytest.mark.slow
    def test_many_operations(self):
        total = 1_000_000
        for _ in range(10):
            total -= 1
        assert total == 999_990
```

Resulting labels:

| Test | Markers |
|---|---|
| `TestAdd::test_small_numbers` | regression (module), smoke (class) |
| `TestAdd::test_zero` | regression, smoke |
| `TestSubtract::test_basic` | regression |
| `TestSubtract::test_many_operations` | regression, slow |

`1_000_000` uses underscores for readability; Python ignores them in numeric literals.

### Example 3: Reusable marker objects

```python
import os
import pytest

only_on_ci = pytest.mark.skipif(
    os.getenv("CI") != "true",
    reason="runs only when CI=true",
)

smoke = pytest.mark.smoke


@smoke
@only_on_ci
def test_pipeline_gate():
    assert True
```

Explanation: `pytest.mark.skipif(...)` returns a marker object you can store in a variable and reuse as a decorator. Reuse prevents duplicated conditions.

### Example 4: The typo trap

```python
@pytest.mark.smoek        # typo
def test_important():
    assert True
```

- Without `--strict-markers`: a warning only; `python -m pytest -m smoke` silently skips this test.
- With `--strict-markers`: error `'smoek' not found in 'markers' configuration option`; you fix it at once.

---

## Real-World Scenarios

1. **Pre-commit routine.** A developer runs `python -m pytest -m smoke` (about 20 seconds) before every commit, and the full suite runs on the build server.
2. **Nightly regression.** The CI schedule runs `python -m pytest -m "regression and not slow"` on every merge, and a weekly job adds the slow tests.
3. **Cross-platform suite.** Some tests exercise Windows file paths. `skipif(sys.platform != "win32")` keeps the suite green on Linux build agents while remaining honest in the report.
4. **Known-bug management.** A defect is logged but will take two sprints to fix. The test is marked `xfail(reason="BUG-204", strict=True)`. The build stays green, the failure is visible in every report, and the moment a developer fixes the bug, strict mode flags it so the marker is removed.
5. **Test traceability.** Teams attach markers like `req_12` to link tests to requirements, then run `-m req_12` to prove coverage for a requirement.

---

## Common Mistakes

| Mistake | Consequence | Fix |
|---|---|---|
| Not registering custom markers | Warnings, no documentation | Add them under `markers` in the config. |
| Missing `--strict-markers` | Typos create new unused markers | Put it in `addopts`. |
| `skip` without a `reason` | Nobody knows why | Always write a reason with a ticket ID. |
| Using `skip` for known bugs | You never learn when the bug is fixed | Use `xfail` (preferably `strict=True`). |
| Permanent `xfail` without a ticket | Zombie tests nobody owns | Include a bug ID and review them regularly. |
| Unquoted `-m not slow` | Shell splits the words; PyTest error | Quote: `-m "not slow"`. |
| Misspelling `pytestmark` (e.g. `pytest_mark`) | Marker silently not applied | Use the exact name `pytestmark`. |
| Expecting `-m` to match marker arguments | It only matches names | Use separate marker names. |
| Too many markers | Confusion | Keep a small, documented vocabulary. |
| Believing a marker "turns off" other tests | Running `pytest` without `-m` runs everything | Use `-m` to select. |
| Putting `@pytest.mark.skipif(condition)` without a `reason` keyword | Error: `Error evaluating 'skipif' condition: you need to specify reason=STRING` | Provide `reason=`. |

---

## Practice Exercises

### Exercise 1: Register and apply
Register the markers `smoke` and `regression` in `pytest.ini` with `--strict-markers`. Tag three of your utility tests as `smoke` and five as `regression` (some can have both). Run each selection and count the tests.

### Exercise 2: Predict the selection
Given the tests below, which are selected by `-m "regression and not slow"`?

```python
@pytest.mark.regression
def test_a(): ...

@pytest.mark.regression
@pytest.mark.slow
def test_b(): ...

@pytest.mark.smoke
def test_c(): ...

@pytest.mark.slow
def test_d(): ...
```

*Answer:* only `test_a`.

### Exercise 3: Skip versus xfail
For each situation, choose `skip`, `skipif`, or `xfail`, and justify it:

1. A test of a feature that the developers have not started.
2. A test that checks Windows registry behaviour and the build server runs on Linux.
3. A test that currently fails due to a logged defect, and you want to know when it is fixed.

*Answers:* 1) `skip` (cannot run meaningfully); 2) `skipif(sys.platform != "win32")`; 3) `xfail(strict=True)`.

### Exercise 4: Module-level marker
Create a test file where every test is automatically `slow`, using `pytestmark`. Verify with `python -m pytest -m slow --collect-only -q`.

### Exercise 5: Catch the typo
Add a deliberate typo to a marker name. Show the behaviour with and without `--strict-markers`. Write two sentences explaining why strictness protects a smoke suite.

### Exercise 6: Strict xfail
Write an `xfail(strict=True)` test that actually passes. Observe that the run fails with `XPASS(strict)`. Remove the marker and confirm the run is green.

### Exercise 7: Reusable skip condition
Create a reusable `requires_python_310 = pytest.mark.skipif(...)` marker and apply it to two tests in different functions.

*Hint:* `sys.version_info < (3, 10)` is the condition.

### Exercise 8 (challenge): Project 1 marker plan
Design a marker vocabulary (4 to 6 markers) for the Project 1 suite, write the `markers` section with descriptions, and list which of your tests belong to which markers in a table. Then write three commands the team would run: (a) before commit, (b) nightly, (c) weekly full run.

---

## Summary

- A **marker** is metadata attached with `@pytest.mark.<name>`; it labels tests so they can be selected, skipped, or handled specially.
- Built-in markers with special behaviour: `skip`, `skipif`, `xfail` (plus `parametrize` and `usefixtures`, covered on Tuesday).
- **Custom markers** (`smoke`, `regression`, `slow`, `negative`...) are pure labels you select with `-m`.
- **Register** custom markers under `markers` in your config and use `--strict-markers` so typos fail loudly.
- Apply markers to functions, classes (all methods), or entire modules with `pytestmark`; multiple markers stack.
- Use `-m "expr"` with `and`, `or`, `not`, and parentheses; always quote the expression.
- Prefer `xfail(strict=True, reason=...)` over `skip` for known bugs, and always record reasons.
- Next lesson: how to run, filter, and report using these markers and many other command-line options.

---

## Additional Resources

- PyTest: Working with custom markers: https://docs.pytest.org/en/stable/example/markers.html
- PyTest: How to mark test functions with attributes: https://docs.pytest.org/en/stable/how-to/mark.html
- PyTest: How to use skip and xfail to deal with tests that cannot succeed: https://docs.pytest.org/en/stable/how-to/skipping.html
