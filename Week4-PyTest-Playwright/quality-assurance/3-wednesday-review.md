# Interview Questions: Week 4 - PyTest-Playwright - Wednesday

**Scope:** Monday to Wednesday content only. Wednesday lessons covered: Data-Driven Test Design, Custom Assertions, Exception Testing, Test Organization and Reusable Templates, HTML Reporting, Performance Profiling, PyTest Skills Assessment.
**Distribution:** 20 questions = 14 Beginner (70%), 5 Intermediate (25%), 1 Advanced (5%).

---

## Beginner (Foundational)

### Q1: What is a custom assertion in PyTest, and why would you write one instead of using a plain `assert`?
**Keywords:** helper function, reuse, clear message, `assert_` prefix, business meaning
**Hint:** Think about a nightly run failing at 6 p.m. and someone else reading the report.
<details>
<summary>Click to Reveal Answer</summary>

A custom assertion is just a function, conventionally named `assert_...`, that raises `AssertionError` when a check fails; there is no framework magic. I write one when the same multi-line check is duplicated across tests, when the check has a business meaning worth naming (such as `assert_valid_email`), or when the built-in message would only say `assert False`. A good helper includes the actual and expected values in its message, so whoever reads the failure can tell what went wrong without re-running the test. It also means a rule change is made in one place instead of fifty.

```python
def assert_valid_email(value):
    assert isinstance(value, str), f"Email must be a str, got {type(value).__name__}"
    assert "@" in value, f"'{value}' is not a valid email address"
```
</details>

---

### Q2: What is wrong with `assert (age >= 18, "Expected an adult")`, and what is the correct way to add a message to an assertion?
**Keywords:** tuple, always truthy, never fails, `assert condition, message`
<details>
<summary>Click to Reveal Answer</summary>

Putting the condition and message together in parentheses creates a two-element tuple, and a non-empty tuple is always truthy. So the assertion can never fail, and the check silently does nothing. The correct form has the message after a comma and no wrapping parentheses: `assert age >= 18, f"Expected an adult but age was {age}"`. PyTest then shows both your message and its own introspection of the expression.
</details>

---

### Q3: What does `__tracebackhide__ = True` do in an assertion helper, and does it change whether the check passes or fails?
**Keywords:** traceback, helper frame, readability, points at the test
<details>
<summary>Click to Reveal Answer</summary>

Setting the local variable `__tracebackhide__ = True` tells PyTest to omit that helper's frame from the failure report. The traceback then points at the line in the test that called the helper, instead of making the reader dig through helper internals. It has no effect on correctness: the check passes or fails exactly as before, so it is purely a readability feature. The lesson recommends putting it as the first line of every assertion helper.
</details>

---

### Q4: Why does `assert 0.1 + 0.2 == 0.3` fail, and how do you compare floats properly in PyTest?
**Keywords:** binary representation, `pytest.approx`, tolerance, `abs`, `rel`
<details>
<summary>Click to Reveal Answer</summary>

Computers store decimals in binary, so some values cannot be represented exactly; `0.1 + 0.2` is actually `0.30000000000000004`. The test would fail for a reason unrelated to your code. I use `pytest.approx`, for example `assert 0.1 + 0.2 == pytest.approx(0.3)`. By default it uses a relative tolerance of 1e-6 and an absolute tolerance of 1e-12, and I can override those with `rel=` or `abs=`. It also works on lists, tuples and dicts. For exact money maths the lesson says to prefer `decimal.Decimal` rather than floats.
</details>

---

### Q5: What is data-driven testing, and what are its three parts?
**Keywords:** same logic, different data, data source, loader, test logic
**Hint:** Think of a cookie cutter and dough.
<details>
<summary>Click to Reveal Answer</summary>

Data-driven testing means running the same test logic many times with different input and expected-output data, while keeping the data separate from the logic. The three parts are the data source (an inline list, Python module, JSON or CSV file), the loader that turns the source into Python objects, and the test function that receives one row at a time. In PyTest the glue is `@pytest.mark.parametrize`. The benefit is that adding a scenario means adding a row, not copying a function, and each row is reported as its own result so one failure does not hide the others.
</details>

---

### Q6: When you load test data from a CSV file, what two things commonly go wrong, and how do you avoid them?
**Keywords:** strings, type conversion, `Path(__file__).parent`, relative path, `csv.DictReader`
<details>
<summary>Click to Reveal Answer</summary>

First, everything read from a CSV is a string, so `"true"` is not `True` and `"5"` is not `5`; you must convert explicitly, for example `row["expected_valid"].strip().lower() == "true"` or `int(...)`. Second, relative paths like `open("test_data/cases.json")` only work when you launch pytest from one particular folder. The fix is to build the path from the test file itself: `Path(__file__).parent / "test_data" / "cases.csv"`, which works from any directory and in CI. `csv.DictReader` helps readability because rows are keyed by header name.
</details>

---

### Q7: Why use `try/except` inside a test to check for an exception is a mistake, and what should you use instead?
**Keywords:** can never fail, `pytest.raises`, DID NOT RAISE, context manager
<details>
<summary>Click to Reveal Answer</summary>

A test written with `try: ... except ValueError: pass` passes both when the exception is raised and when it is not, so it can never detect a regression. The correct tool is `with pytest.raises(ValueError):`. If the code inside raises a `ValueError` (or subclass) the test continues; if nothing is raised the test fails with `DID NOT RAISE`; and if a different exception type is raised, that exception propagates and the test fails. So it passes only when the expected kind of exception actually happens.

```python
with pytest.raises(ValueError):
    withdraw(100, -5)
```
</details>

---

### Q8: How do you check an exception's message and its attributes with `pytest.raises`, and where should you put assertions about `excinfo`?
**Keywords:** `match`, regular expression, `excinfo.value`, outside the `with` block, `re.escape`
<details>
<summary>Click to Reveal Answer</summary>

`match=` takes a regular expression that PyTest searches in `str(exception)`, so special characters such as `.`, `(` or `$` need `re.escape`. To inspect more, I capture the info object with `as excinfo`; `excinfo.value` is the exception instance, so I can read custom attributes, and `excinfo.type` is the class. Assertions about `excinfo` go after the `with` block, because it is only populated once the block has exited, and any code after the raising line inside the block never runs.

```python
with pytest.raises(InsufficientFundsError) as excinfo:
    withdraw(50, 80)
assert excinfo.value.balance == 50
```
</details>

---

### Q9: What do `testpaths`, `pythonpath`, `addopts` and `markers` do in `pytest.ini`, and why is `--strict-markers` recommended?
**Keywords:** `pytest.ini`, `testpaths`, `pythonpath`, `addopts`, `--strict-markers`
<details>
<summary>Click to Reveal Answer</summary>

`testpaths` tells PyTest where to look when you run plain `pytest` from the root, so it does not scan `src/` or virtual environments. `pythonpath` adds folders such as `src` and `tests` to the import path so tests can import product code and helpers without installing or hacking `sys.path`. `addopts` lists options added to every command line (for example `-ra`), and `markers` registers custom markers with descriptions. `--strict-markers` turns a typo like `@pytest.mark.smoek` into an error instead of a quiet warning, so tests are not silently excluded from a `-m smoke` run.

```ini
[pytest]
testpaths = tests
pythonpath = src tests
addopts = -ra --strict-markers
markers =
    smoke: fast checks that prove the build is alive
```
</details>

---

### Q10: What is the Arrange-Act-Assert pattern, and how do the lesson's "DRY in setup, DAMP in tests" principles relate to it?
**Keywords:** Arrange, Act, Assert, one action, DRY, DAMP
<details>
<summary>Click to Reveal Answer</summary>

Arrange-Act-Assert structures every test into three visible phases: arrange the objects and data, perform the single action under test, then verify the outcome. A reader immediately sees what is being tested from the Act line, and a test with many acts usually tests too many things and should be split. DRY means avoiding repeated setup, for example through fixtures and builders. DAMP means Descriptive And Meaningful Phrases: each test should still be readable on its own, so you keep the Act and Assert lines visible rather than hiding everything in helpers.
</details>

---

### Q11: In a PyTest report, what is the difference between a failure and an error, and what does each tell you?
**Keywords:** `F`, `E`, test body, fixture setup, product vs environment
<details>
<summary>Click to Reveal Answer</summary>

A failure (`F`) means the test body ran and an assertion, or another exception inside the test, failed. An error (`E`) means something went wrong outside the test body, usually in fixture setup or teardown, so the test could not run properly. The distinction tells you whether the product misbehaved or the test environment is broken. In the progress line the other symbols are `.` pass, `s` skip, `x` expected failure and `X` unexpected pass. When reading a report you check errors first, because setup problems can hide many tests.
</details>

---

### Q12: What does `--self-contained-html` do for a `pytest-html` report, and how does an HTML report differ from JUnit XML?
**Keywords:** `--html`, `--self-contained-html`, single file, JUnit XML, CI tools
<details>
<summary>Click to Reveal Answer</summary>

`pytest --html=reports/report.html` writes the report, but by default the CSS and assets live in a separate folder, so emailing only the `.html` loses the formatting. `--self-contained-html` embeds CSS, JavaScript and images into one file, which is what you want for email, Jira tickets or CI artifacts. The HTML report is for people such as testers, managers and clients. JUnit XML (`--junitxml=reports/junit.xml`) needs no plugin and is a standard machine-readable format that CI servers like Jenkins or GitHub Actions use for dashboards and trends, but it is unreadable for humans. You can produce both in one run.
</details>

---

### Q13: How do you find slow tests with PyTest, and what is the difference between the setup, call and teardown phases in that output?
**Keywords:** `--durations`, `--durations-min`, setup, call, teardown, `perf_counter`
<details>
<summary>Click to Reveal Answer</summary>

`pytest --durations=5` lists the five slowest phases, `--durations=0` shows all of them, and `--durations-min=1.0` hides anything shorter than a second. Each test has three phases: setup is fixture creation, call is the test body, and teardown is fixture cleanup. A slow `setup` points at a heavy fixture, which you might fix by widening its scope, whereas a slow `call` points at the test body or the code under test. For timing code manually, use `time.perf_counter()` rather than `time.time()`, because `perf_counter` is monotonic and not affected by system clock changes.
</details>

---

### Q14: You see `ScopeMismatch`, `fixture 'abc' not found`, `collected 0 items` and `import file mismatch`. What is the usual cause and fix for each?
**Keywords:** scope, `conftest.py`, naming pattern, `__init__.py`, error decoder
<details>
<summary>Click to Reveal Answer</summary>

`ScopeMismatch` happens when a wider-scope fixture requests a narrower-scope one; widen the dependency's scope or narrow the dependent's. `fixture 'abc' not found` is a typo, or the fixture is somewhere not visible to the test, so check the name or move it to a `conftest.py` in a parent folder. `collected 0 items` means file or function names do not match the discovery pattern or you are in the wrong folder, so rename to `test_*` and check `testpaths`. `import file mismatch` means two test files share a name in different folders without `__init__.py`; use unique names, add `__init__.py` files, or use `--import-mode=importlib`.
</details>

---

## Intermediate (Application)

### Q15: Your JSON test-data file has twenty discount rows, and one row fails because of a known rounding bug (BUG-1234). How do you keep the suite green without deleting the row, and how do you handle the invalid-input rows?
**Keywords:** `pytest.param`, `xfail`, `strict`, separate tests, `id`
**Hint:** Marks can be attached to a single row.
<details>
<summary>Click to Reveal Answer</summary>

I would load the rows in a loader function and wrap each one in `pytest.param(..., id=...)`, attaching `marks=pytest.mark.xfail(reason="BUG-1234: rounding", strict=False)` to just that row. It then reports as `xfailed` instead of failing, and the rest of the table still runs. With `strict=True`, an unexpected pass becomes a failure, which tells the team the bug is fixed and the marker should be removed. For invalid-input rows I use a separate parametrized test with `pytest.raises`, rather than an `if expected_error:` branch inside one test. Positive and negative rows live in separate tests, and expected values stay hard-coded from the specification.
</details>

---

### Q16: A form has twelve fields to validate and the tester wants to see every wrong field in one run. How would you do that, and when would you avoid it?
**Keywords:** soft assertion, collect errors, fixture with `yield`, `pytest.fail`, dependent steps
<details>
<summary>Click to Reveal Answer</summary>

PyTest has no built-in soft assert, so I would write a small `SoftAssert` class that appends messages to a list instead of raising, exposed through a fixture. After the `yield` the fixture calls an `assert_all()` method that uses `pytest.fail` to report every collected failure together. The trade-off from the lesson is that a failure in teardown may be shown as an error rather than a failure in some reports, so an alternative is calling `assert_all()` explicitly as the last line of the test. I would not use soft assertions where later steps depend on earlier ones: if login failed, checking the dashboard only produces cascading meaningless failures, so normal asserts are better there.

```python
soft.equal(profile["age"], 31, "age")
soft.equal(profile["country"], "ES", "country")   # both reported together
```
</details>

---

### Q17: `load_config` catches a `json.JSONDecodeError` and raises your own `ConfigError`. How do you test that the friendly error is raised and that the original problem is preserved?
**Keywords:** `raise ... from`, `__cause__`, `pytest.raises`, `match`, `excinfo`
<details>
<summary>Click to Reveal Answer</summary>

In the function, `raise ConfigError("Config is not valid JSON") from exc` stores the original exception in `__cause__`. In the test I use `pytest.raises(ConfigError, match="not valid JSON") as excinfo`, call `load_config("{bad json")` as the only statement inside the block, and then, after the block, assert `isinstance(excinfo.value.__cause__, json.JSONDecodeError)`. That confirms both the friendly error for users and the underlying cause for engineers. Keeping only the single raising call inside the `with` block makes it clear which line raised.

```python
with pytest.raises(ConfigError, match="not valid JSON") as excinfo:
    load_config("{bad json")
assert isinstance(excinfo.value.__cause__, json.JSONDecodeError)
```
</details>

---

### Q18: Your suite takes 40 minutes and developers have stopped running it. Walk me through how you would investigate and speed it up safely.
**Keywords:** `--durations`, fixture scope, mock, `pytest-xdist`, measure first
**Hint:** Goal, baseline, biggest cost, change one thing, re-measure.
<details>
<summary>Click to Reveal Answer</summary>

I would not guess; I would define a goal, then measure a baseline with `pytest --durations=20` and `--setup-show`. If many top entries are `setup` phases of a fixture that is recreated for every test, I widen it to session scope and reset state in a small function-scoped fixture, accepting the risk of leaked state. I would mock slow external calls with `patch`, remove arbitrary `time.sleep` calls in favour of waiting on a condition, and run subsets with `-m smoke` locally. Finally, `pytest -n auto` with `pytest-xdist` runs independent tests in parallel, though session fixtures then run once per worker and tests must not share files or database rows. I change one thing at a time, re-measure, and keep a behaviour test so faster is not wrong.
</details>

---

### Q19: This file has several bugs. Name them and fix them.
```python
@pytest.fixture(scope="session")
def cart():
    return Cart()

@pytest.mark.smoek
def test_cart_starts_empty(cart): ...

def test_discount_error():
    try:
        apply_discount(-1, 10)
    except ValueError:
        pass

@pytest.mark.parametrize("price, percent", [(100, 10, 90)])
def test_discount_values(price, percent, expected): ...
```
**Keywords:** session scope leak, `smoek`, `try/except`, `parametrize` names, `pytest.raises`
<details>
<summary>Click to Reveal Answer</summary>

There are four issues. The `cart` fixture is session-scoped, so state leaks between tests; use the default function scope so each test gets a fresh cart. `smoek` is a misspelt marker, which fails under `--strict-markers`; it should be `smoke`. `test_discount_error` uses `try/except` so it can never fail; use `with pytest.raises(ValueError): apply_discount(-1, 10)`. Finally, `parametrize` names two parameters but each row has three values and the function needs `expected`, so the names should be `"price, percent, expected"`. I would also prefer `pytest.approx` when comparing float totals.
</details>

---

## Advanced (Deep Dive)

### Q20: Your helper `assert_equal(a, b)` contains a bare `assert a == b`. When it fails, the report shows only `AssertionError` with no values, although the same assert inside a test shows a rich diff. Why does this happen, and what are your options?
**Keywords:** assertion rewriting, import time, helper module, `register_assert_rewrite`, explicit message
**Hint:** PyTest rewrites only certain modules.
<details>
<summary>Click to Reveal Answer</summary>

PyTest's introspection works by rewriting assert statements at import time, but it only does this for test modules, `conftest.py` files and plugins. A plain helper module imported by tests is not rewritten, so its bare `assert` raises a plain `AssertionError` with no sub-expression details. There are two fixes. The simplest and most reliable is to put an explicit f-string message in the helper's asserts, such as `assert a == b, f"expected {b!r} but got {a!r}"`. The other is to call `pytest.register_assert_rewrite("helpers.assertions")` before the module is imported, typically at the top of the root `conftest.py`, which gives full introspection inside helpers. Many frameworks do both, and I would also keep `__tracebackhide__ = True` so the report points at the test.

```python
# conftest.py (top)
import pytest
pytest.register_assert_rewrite("helpers.assertions")
```
</details>

---

## Coverage Table

| Lesson | Question numbers |
|--------|------------------|
| Custom Assertions | Q1, Q2, Q3, Q4, Q16, Q20 |
| Data-Driven Test Design | Q5, Q6, Q15 |
| Exception Testing | Q7, Q8, Q17 |
| Test Organization and Reusable Templates | Q9, Q10 |
| HTML Reporting | Q11, Q12 |
| Performance Profiling | Q13, Q18 |
| PyTest Skills Assessment | Q14, Q19 |
