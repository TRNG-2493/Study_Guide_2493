# PyTest Skills Assessment

## Learning Objectives

By the end of this lesson you will be able to:

- Describe what the PyTest skills assessment measures and how the competencies map to Monday, Tuesday and Wednesday's lessons.
- Use a structured **review checklist** covering every PyTest skill from this week so far.
- Work through a full **practice assessment** with realistic tasks (functions, fixtures, parametrization, mocks, custom assertions, exceptions, markers, reporting) and compare it to a model solution.
- Self-assess against a rubric and identify weak areas for targeted revision.
- Apply a repeatable approach to time-boxed practical exams: read, plan, build in small steps, run often, debug from the output.
- Diagnose the most frequent failure messages quickly.

> **Note on format:** Your instructor will confirm the exact format, time limit, and allowed resources for the assessment on the day. This lesson prepares you for a *practical, hands-on* assessment in which you write and run PyTest code, and it includes a full practice version so that nothing on the day is a surprise.

---

## Why This Matters

The weekly epic is to turn manual test design into automation, moving from PyTest basics to a **reporting framework** for Project 1 – QE Foundations. Wednesday afternoon is the checkpoint: before we leave PyTest and begin web locators and browser automation on Thursday, we confirm that the foundation is solid.

This matters for three reasons:

1. **Everything later builds on PyTest.** Next, we will write browser tests in a PyTest-based setup. Misunderstanding fixtures, markers or assertions now would multiply confusion later. We will cover browser automation in depth on Thursday and Friday.
2. **It is what employers test.** Interviews for QE and SDET roles commonly include a live-coding task such as "write tests for this function, use parametrization, and show how you would handle bad input." The practice assessment below mirrors that.
3. **It shows you where to invest your time.** An honest self-assessment today is cheaper than discovering gaps on a project deadline.

---

## The Concept

### 1. What the assessment covers

The assessment samples the skills from the first three days of the week:

| Day | Topic | Skills you may be asked to show |
|-----|-------|---------------------------------|
| Monday | PyTest fundamentals | Install and configure; naming and discovery; test functions and classes; plain `assert` and introspection; markers (`skip`, `skipif`, `xfail`, custom); running, selecting and filtering (`-k`, `-m`, node IDs, `-v`, `-x`) |
| Tuesday | Advanced features | Fixtures (setup/teardown with `yield`), scopes, parametrization, combining fixtures and parameters, `conftest.py`, sharing fixtures, `unittest.mock` (`patch`, `Mock`, `return_value`, `side_effect`, `assert_called_with`) |
| Wednesday | Framework and reporting | Data-driven design (inline/JSON/CSV, `pytest.param`), custom assertions, `pytest.raises`/`pytest.warns`, organization and templates, `pytest.ini`, HTML reports, performance diagnostics (`--durations`) |

### 2. Typical task types

Expect a mix of the following; each is practised in section 6:

1. **Write tests for a given function** including normal, boundary and invalid cases.
2. **Fix a broken test file** (a bug in a fixture, a typo in a marker, a misuse of `pytest.raises`).
3. **Refactor duplicated tests** into a parametrized, data-driven test.
4. **Create fixtures** and place them in `conftest.py`.
5. **Mock an external dependency** so a test does not touch the network or clock.
6. **Write a custom assertion helper** with a useful message.
7. **Configure the project** (`pytest.ini` with markers and report options) and **generate an HTML report**.
8. **Explain results**: interpret a failure output or a `--durations` listing in writing.

### 3. How you will be evaluated (rubric)

A rubric is a scoring guide. Knowing it in advance lets you aim your effort.

| Criterion | What "excellent" looks like | Weight |
|-----------|----------------------------|--------|
| **Correctness** | Tests run, pass/fail for the right reasons, and detect real defects | 30% |
| **Coverage of cases** | Happy path, boundaries, invalid input and exceptions are all considered | 20% |
| **Use of PyTest features** | Appropriate fixtures, parametrization, markers, `pytest.raises`, `approx` | 20% |
| **Structure and readability** | Clear names, AAA, no duplication, sensible file layout | 15% |
| **Configuration and reporting** | `pytest.ini`, registered markers, working HTML report | 10% |
| **Explanation** | Short written notes explaining choices and results | 5% |

(Weights are indicative; your instructor will share the official scoring.)

### 4. The competency checklist

Use this section as a revision list. For each item, you should be able to **do it from memory in under a few minutes**, and explain **why**. Tick items you are confident about; revise the rest.

#### Monday: fundamentals

- [ ] I can create a virtual environment and install PyTest (`python -m pip install pytest`) and check the version (`pytest --version`).
- [ ] I know the default discovery rules: `test_*.py` or `*_test.py` files; `test_*` functions; `Test*` classes without `__init__`.
- [ ] I can write a test function and a test class and know each test in a class gets a fresh instance.
- [ ] I can use plain `assert` and explain what assertion introspection (rewriting) does.
- [ ] I can apply `skip`, `skipif`, `xfail` and a custom marker, and register markers in `pytest.ini`.
- [ ] I can run: one file, one test by node ID (`file::test`), by keyword (`-k`), by marker (`-m`), stop at first failure (`-x`), verbose (`-v`), show reasons (`-ra`).

#### Tuesday: advanced

- [ ] I can write a fixture, inject it by parameter name, and use `yield` for teardown.
- [ ] I can choose between `function`, `class`, `module`, `package` and `session` scope and explain the trade-off.
- [ ] I can parametrize with `@pytest.mark.parametrize`, multiple parameter names and custom IDs.
- [ ] I can parametrize a fixture (`params=`) and combine fixtures with parameters.
- [ ] I know what `conftest.py` is, where PyTest looks for it, and that fixtures in it need no import.
- [ ] I can patch a dependency with `unittest.mock.patch`, set `return_value` or `side_effect`, and assert calls.

#### Wednesday: framework

- [ ] I can load test data from a list, a JSON file and a CSV file and feed it to `parametrize` with `pathlib` paths.
- [ ] I can use `pytest.param(..., id=..., marks=...)`.
- [ ] I can write assertion helpers with `__tracebackhide__` and good messages, and use `pytest.approx` for floats.
- [ ] I can test exceptions with `pytest.raises(..., match=...)`, inspect `excinfo`, and test warnings with `pytest.warns`.
- [ ] I can set up the recommended folder layout, `pytest.ini` (`testpaths`, `pythonpath`, `addopts`, `markers`), and AAA tests.
- [ ] I can generate a self-contained HTML report with `pytest --html=... --self-contained-html` and customise title/metadata.
- [ ] I can find slow tests with `--durations` and explain setup vs call vs teardown.

### 5. A strategy for time-boxed practical assessments

1. **Read everything first (2-3 minutes).** Note all tasks, their weights, and the deliverables (file names!). Missing a required file name is the cheapest way to lose marks.
2. **Plan the order.** Do easy, high-weight tasks first. Leave polish for the end.
3. **Set up the project skeleton immediately**: folder, `pytest.ini`, a first passing test. A green starting point is a safe base.
4. **Build in small steps.** Write one test, run it, then write the next. Never write 200 lines before the first run.
5. **Run often with useful flags**: `pytest -v -ra --tb=short`, and `-x` while debugging.
6. **Read error messages from the bottom up.** The last lines (`E ...`) say what went wrong; the lines above say where.
7. **Keep tests independent.** If a test only passes after another one, fix it.
8. **Reserve the last 10% of time** to: run the full suite, regenerate the HTML report, re-read the task list, and remove debug prints.
9. **If stuck for more than ~7 minutes, move on** and note the issue. Come back later with a fresh mind.
10. **Write short notes** explaining the key decisions; they earn marks and show understanding.

### 6. Fast diagnosis: decode common errors

| What you see | Usual cause | Fix |
|--------------|-------------|-----|
| `ModuleNotFoundError: No module named 'xyz'` | Import path wrong; `pythonpath` not set; package not installed | Check file names and `pytest.ini`; run from project root |
| `fixture 'abc' not found` | Typo, or fixture is in a file/folder not visible to this test | Check name; move to `conftest.py` in a parent folder |
| `'smoek' not found in markers configuration option` | Unregistered/misspelled marker with `--strict-markers` | Register or fix the typo |
| `ScopeMismatch` | A wide-scope fixture requests a narrower-scope fixture | Widen the dependency's scope or narrow the dependent's |
| `Failed: DID NOT RAISE` | Code did not raise the expected exception | Check input or the logic under test |
| `fixture ... called directly` | Calling a fixture function like a normal function | Request it as a parameter instead |
| `collected 0 items` | File/function names do not match the pattern, or wrong folder | Rename to `test_*`; check `testpaths` |
| `import file mismatch` | Two test files with the same name in different folders without `__init__.py` | Unique names or `__init__.py` |
| `In test_x: function uses no argument 'y'` | `parametrize` names do not match the function parameters | Align names |
| `AssertionError` showing `0.30000000000000004` | Float precision | `pytest.approx` |
| `unrecognized arguments: --html` | Plugin missing in the active environment | `python -m pip install pytest-html` |

### 7. Writing short explanations

Many assessments ask, "Explain why you chose X." Use this three-part formula: **What** you did, **Why** it was the right tool, **Trade-off** or limitation. Example:

> "I used `@pytest.mark.parametrize` with `pytest.param` IDs for the discount tests. This keeps one test function for all rows and gives a separate result for each. The trade-off is that very large tables become harder to read, so for more than about ten rows I would move the data to a JSON file."

---

## Practice Assessment (with model solutions)

**Instructions:** Try each task yourself first, in a fresh project folder. Time yourself (suggested total: 90 minutes). Only then compare with the model solutions. The solution code is intended to be runnable.

### Scenario

You are testing a small "Order Utilities" library used by an online shop. Create this project structure:

```
assessment/
├── pytest.ini
├── src/
│   └── shop/
│       ├── __init__.py
│       └── orders.py
└── tests/
    ├── conftest.py
    ├── data/
    │   └── discount_cases.json
    ├── helpers/
    │   ├── __init__.py
    │   └── assertions.py
    ├── test_discounts.py
    ├── test_validation.py
    ├── test_checkout.py
    └── test_cart.py
```

The code under test (`src/shop/__init__.py` is an empty file):

```python
# src/shop/orders.py
import datetime as dt


class OutOfStockError(Exception):
    def __init__(self, sku, requested, available):
        self.sku = sku
        self.requested = requested
        self.available = available
        super().__init__(f"{sku}: requested {requested}, only {available} available")


def apply_discount(price: float, percent: float) -> float:
    if price < 0:
        raise ValueError("price must not be negative")
    if not 0 <= percent <= 100:
        raise ValueError("percent must be between 0 and 100")
    return round(price * (1 - percent / 100), 2)


def is_valid_postcode(code: str) -> bool:
    """Valid postcode: exactly 5 digits."""
    return isinstance(code, str) and len(code) == 5 and code.isdigit()


class Cart:
    def __init__(self):
        self.items = {}          # sku -> (unit_price, qty)

    def add(self, sku, unit_price, qty=1):
        if qty <= 0:
            raise ValueError("qty must be positive")
        _, existing = self.items.get(sku, (unit_price, 0))
        self.items[sku] = (unit_price, existing + qty)

    def total(self):
        return round(sum(p * q for p, q in self.items.values()), 2)


class InventoryClient:
    """Pretend this calls a remote service."""

    def stock_for(self, sku):
        raise RuntimeError("network not available in tests")


def checkout(cart: Cart, inventory: InventoryClient, now=None):
    now = now or dt.datetime.now()
    for sku, (_, qty) in cart.items.items():
        available = inventory.stock_for(sku)
        if qty > available:
            raise OutOfStockError(sku, qty, available)
    return {"total": cart.total(), "placed_at": now.isoformat(timespec="seconds")}
```

### Task 1: Configuration (10 points)

Create `pytest.ini` that: sets `testpaths`, adds `src` and `tests` to `pythonpath`, registers markers `smoke`, `regression` and `slow`, enables `--strict-markers` and `-ra`, and shows the 5 slowest tests.

<details>
<summary>Model solution</summary>

```ini
[pytest]
minversion = 8.0
testpaths = tests
pythonpath = src tests
addopts = -ra --strict-markers --durations=5
markers =
    smoke: quick sanity checks
    regression: broader checks before release
    slow: tests that take noticeably longer
```
</details>

### Task 2: Data-driven discount tests (20 points)

Create `tests/data/discount_cases.json` with at least six valid rows (include 0 and 100 percent) and test `apply_discount` using one parametrized test fed from the JSON using `pathlib`. Give each row an `id`. Mark the "full discount" row as `smoke`. Add a second parametrized test for invalid inputs using `pytest.raises` with `match`.

<details>
<summary>Model solution</summary>

`tests/data/discount_cases.json`:

```json
[
  {"id": "typical-10",   "price": 100.0, "percent": 10,  "expected": 90.0, "smoke": false},
  {"id": "no-discount",  "price": 100.0, "percent": 0,   "expected": 100.0, "smoke": false},
  {"id": "full-discount","price": 100.0, "percent": 100, "expected": 0.0,   "smoke": true},
  {"id": "half",         "price": 80.0,  "percent": 50,  "expected": 40.0,  "smoke": false},
  {"id": "cents",        "price": 19.99, "percent": 15,  "expected": 16.99, "smoke": false},
  {"id": "zero-price",   "price": 0.0,   "percent": 25,  "expected": 0.0,   "smoke": false}
]
```

`tests/test_discounts.py`:

```python
import json
from pathlib import Path

import pytest

from shop.orders import apply_discount

DATA_FILE = Path(__file__).parent / "data" / "discount_cases.json"


def load_valid_cases():
    rows = json.loads(DATA_FILE.read_text(encoding="utf-8"))
    params = []
    for r in rows:
        marks = [pytest.mark.smoke] if r.get("smoke") else []
        params.append(
            pytest.param(r["price"], r["percent"], r["expected"], id=r["id"], marks=marks)
        )
    return params


@pytest.mark.parametrize("price, percent, expected", load_valid_cases())
def test_apply_discount_valid(price, percent, expected):
    assert apply_discount(price, percent) == pytest.approx(expected)


@pytest.mark.parametrize(
    "price, percent, message",
    [
        pytest.param(-1.0, 10, "price must not be negative", id="negative-price"),
        pytest.param(100.0, -1, "between 0 and 100", id="percent-below-range"),
        pytest.param(100.0, 101, "between 0 and 100", id="percent-above-range"),
    ],
)
def test_apply_discount_invalid(price, percent, message):
    with pytest.raises(ValueError, match=message):
        apply_discount(price, percent)
```

Points to explain in your notes: file path built from `__file__` so it works from any directory; `pytest.param` with `id` and `marks`; `approx` for floats; the invalid cases are in a separate test to avoid `if/else` in the body.
</details>

### Task 3: Custom assertion (10 points)

In `tests/helpers/assertions.py` create `assert_valid_postcode(value)` that fails with a message including the offending value and *why* it failed (wrong type, wrong length, non-digit). Use `__tracebackhide__`. Write parametrized tests that check both passing and failing values *of the helper itself*, using `pytest.raises(AssertionError, match=...)`.

<details>
<summary>Model solution</summary>

`tests/helpers/__init__.py` is an empty file.

```python
# tests/helpers/assertions.py
def assert_valid_postcode(value):
    __tracebackhide__ = True
    assert isinstance(value, str), f"Postcode {value!r} must be a str, got {type(value).__name__}"
    assert len(value) == 5, f"Postcode {value!r} must have 5 characters, got {len(value)}"
    assert value.isdigit(), f"Postcode {value!r} must contain only digits"
```

```python
# tests/test_validation.py
import pytest

from helpers.assertions import assert_valid_postcode
from shop.orders import is_valid_postcode


@pytest.mark.parametrize("code", ["12345", "00000", "99999"])
def test_helper_accepts_valid(code):
    assert_valid_postcode(code)


@pytest.mark.parametrize(
    "code, message",
    [
        pytest.param(12345, "must be a str", id="wrong-type"),
        pytest.param("1234", "5 characters", id="too-short"),
        pytest.param("123456", "5 characters", id="too-long"),
        pytest.param("12a45", "only digits", id="letters"),
    ],
)
def test_helper_rejects_invalid(code, message):
    with pytest.raises(AssertionError, match=message):
        assert_valid_postcode(code)


@pytest.mark.parametrize("code", ["12345", "00000"])
def test_is_valid_postcode_true(code):
    assert is_valid_postcode(code) is True


@pytest.mark.parametrize("code", ["", "1234", "123456", "abcde", 12345, None])
def test_is_valid_postcode_false(code):
    assert is_valid_postcode(code) is False
```

Here the application function and the assertion helper are tested separately; the helper gives *diagnostic detail*, the application function gives a simple boolean.
</details>

### Task 4: Fixtures and `conftest.py` (15 points)

In `tests/conftest.py` create: an `empty_cart` fixture; a `cart_with_items` fixture that depends on it (two SKUs); and a `fake_inventory` fixture returning a `Mock(spec=InventoryClient)` whose `stock_for` returns 10. Write cart tests: adding the same SKU twice sums quantity; total is correct; adding a non-positive quantity raises `ValueError`; each test gets a clean cart.

<details>
<summary>Model solution</summary>

```python
# tests/conftest.py
from unittest.mock import Mock

import pytest

from shop.orders import Cart, InventoryClient


@pytest.fixture
def empty_cart():
    return Cart()


@pytest.fixture
def cart_with_items(empty_cart):
    empty_cart.add("PEN", 2.50, 4)
    empty_cart.add("BOOK", 12.00, 1)
    return empty_cart


@pytest.fixture
def fake_inventory():
    inventory = Mock(spec=InventoryClient)
    inventory.stock_for.return_value = 10
    return inventory
```

```python
# tests/test_cart.py
import pytest


@pytest.mark.smoke
def test_total_with_items(cart_with_items):
    assert cart_with_items.total() == 22.00


def test_adding_same_sku_twice_sums_quantity(empty_cart):
    empty_cart.add("PEN", 2.50, 2)
    empty_cart.add("PEN", 2.50, 3)
    assert empty_cart.items["PEN"] == (2.50, 5)


@pytest.mark.parametrize("qty", [0, -1, -100])
def test_add_non_positive_qty_raises(empty_cart, qty):
    with pytest.raises(ValueError, match="qty must be positive"):
        empty_cart.add("PEN", 2.50, qty)


def test_each_test_gets_a_clean_cart(empty_cart):
    assert empty_cart.items == {}
```

`Mock(spec=InventoryClient)` creates a mock that only allows attributes that exist on the real class, so a typo such as `inventory.stok_for` raises `AttributeError` instead of silently succeeding.
</details>

### Task 5: Mocking and time (15 points)

Test `checkout` in `tests/test_checkout.py` without touching a real network: (a) success path with a fixed `now`, verifying total and `placed_at`; (b) out-of-stock path using `side_effect` or `return_value`, checking the exception attributes through `excinfo`; (c) verify `stock_for` was called once per SKU using `assert_any_call` / `call_count`.

<details>
<summary>Model solution</summary>

```python
# tests/test_checkout.py
import datetime as dt

import pytest

from shop.orders import OutOfStockError, checkout


def test_checkout_success_with_fixed_time(cart_with_items, fake_inventory):
    fixed = dt.datetime(2025, 1, 15, 10, 30, 0)

    order = checkout(cart_with_items, fake_inventory, now=fixed)

    assert order == {"total": 22.00, "placed_at": "2025-01-15T10:30:00"}


def test_checkout_checks_stock_for_each_sku(cart_with_items, fake_inventory):
    checkout(cart_with_items, fake_inventory)

    assert fake_inventory.stock_for.call_count == 2
    fake_inventory.stock_for.assert_any_call("PEN")
    fake_inventory.stock_for.assert_any_call("BOOK")


def test_checkout_out_of_stock(cart_with_items, fake_inventory):
    fake_inventory.stock_for.return_value = 1     # only one in stock

    with pytest.raises(OutOfStockError) as excinfo:
        checkout(cart_with_items, fake_inventory)

    err = excinfo.value
    assert err.sku == "PEN"          # PEN (qty 4) is checked first
    assert err.requested == 4
    assert err.available == 1
    assert "requested 4" in str(err)
```

Notes: injecting `now` as a parameter made the function easy to test, which is a design lesson (dependency injection). Dictionaries keep insertion order in Python 3.7+, so "PEN" is checked first.
</details>

### Task 6: Reporting (10 points)

Generate an HTML report named `reports/assessment_report.html` that is self-contained, includes a custom title and an "Environment" metadata entry named `Candidate` with your name. Run only `smoke` tests into a second report `reports/smoke_report.html`.

<details>
<summary>Model solution</summary>

Install: `python -m pip install pytest pytest-html`

Add to `tests/conftest.py`:

```python
from pytest_metadata.plugin import metadata_key


def pytest_configure(config):
    config.stash[metadata_key]["Candidate"] = "Your Name"
    config.stash[metadata_key]["Project"] = "PyTest Skills Assessment"


def pytest_html_report_title(report):
    report.title = "PyTest Skills Assessment Report"
```

Commands:

```bash
pytest --html=reports/assessment_report.html --self-contained-html
pytest -m smoke --html=reports/smoke_report.html --self-contained-html
```
(If the plugin hooks differ in your installed `pytest-html` version, consult the plugin's documentation; the commands are unchanged.)
</details>

### Task 7: Debug a broken file (10 points)

The following file has **five** problems. Find and fix them without looking at the hints.

```python
# tests/test_broken.py
import pytest
from shop.orders import apply_discount, Cart


@pytest.fixture(scope="session")
def cart():
    return Cart()


@pytest.mark.smoek
def test_cart_starts_empty(cart):
    assert cart.items == {}


def test_cart_add(cart):
    cart.add("PEN", 2.5, 2)
    assert cart.total() == 5


def test_cart_is_empty_again(cart):
    assert cart.items == {}


def test_discount_error():
    try:
        apply_discount(-1, 10)
    except ValueError:
        pass


@pytest.mark.parametrize("price, percent", [(100, 10, 90)])
def test_discount_values(price, percent, expected):
    assert apply_discount(price, percent) == expected
```

<details>
<summary>Hints and solution</summary>

1. `@pytest.mark.smoek` is a misspelt marker (error under `--strict-markers`); fix to `smoke`.
2. The `cart` fixture has `scope="session"`, so state leaks: `test_cart_add` adds an item and `test_cart_is_empty_again` then fails. Use the default function scope.
3. `test_cart_add` is fine logically once isolated (note `5 == 5.0` is true in Python, but `pytest.approx` would be preferred for floats).
4. `test_discount_error` uses `try/except` and can never fail; use `with pytest.raises(ValueError):`.
5. The parametrize decorator names two parameters but each row has three values, and the test function requires `expected`. Fix to `"price, percent, expected"`.

Corrected file:

```python
import pytest
from shop.orders import apply_discount, Cart


@pytest.fixture
def cart():
    return Cart()


@pytest.mark.smoke
def test_cart_starts_empty(cart):
    assert cart.items == {}


def test_cart_add(cart):
    cart.add("PEN", 2.5, 2)
    assert cart.total() == pytest.approx(5.0)


def test_cart_is_empty_again(cart):
    assert cart.items == {}


def test_discount_error():
    with pytest.raises(ValueError):
        apply_discount(-1, 10)


@pytest.mark.parametrize("price, percent, expected", [(100, 10, 90)])
def test_discount_values(price, percent, expected):
    assert apply_discount(price, percent) == expected
```
</details>

### Task 8: Short written answers (5 points)

Answer in two or three sentences each:

1. Why is `try/except` a poor way to test for an exception?
2. When would you choose `scope="module"` for a fixture, and what risk does it add?
3. What is the difference between a test *failure* and a test *error* in the PyTest report?
4. Why should `reports/` not be committed to version control?

<details>
<summary>Model answers</summary>

1. The test passes whether or not the exception happens, so it can never detect a regression. `pytest.raises` fails with `DID NOT RAISE` if nothing is raised and also checks the exception type and message.
2. Use module scope when creating the resource is expensive and it can be safely shared by all tests in the file, such as a read-only data set. The risk is state leaking between tests, so mutable resources must be reset.
3. A failure means the test body ran and an assertion or exception inside the test occurred. An error means something failed outside the test body, usually in fixture setup or teardown, so the test could not run properly.
4. Reports are generated, change on every run, and can be large; committing them causes noise and merge conflicts. They should be produced by the pipeline and stored as artifacts instead.
</details>

### Self-scoring

| Task | Points available | Your score |
|------|------------------|-----------|
| 1 Configuration | 10 | |
| 2 Data-driven discounts | 20 | |
| 3 Custom assertion | 10 | |
| 4 Fixtures / conftest | 15 | |
| 5 Mocking | 15 | |
| 6 Reporting | 10 | |
| 7 Debugging | 10 | |
| 8 Short answers | 5 | |
| **Total** | **95** | |

(Scale to 100 by dividing by 0.95.) Interpretation: **85+** strong; **70-84** solid with a few gaps, revise the topics where you lost points; **below 70** revisit the lessons for those topics and repeat the tasks you struggled with before the assessment.

---

## Real-World Scenarios

1. **Technical interview.** The interviewer provides a function and a 45-minute window: "show me how you'd test this." Following the strategy in section 5 (read, plan, small steps, run often) and demonstrating parametrization, `pytest.raises` and a fixture is exactly what Tasks 2-5 train.
2. **Inheriting a legacy suite.** On a new team you are asked to fix a failing nightly job. The error decoder in section 6 and the broken-file task are the daily reality of QE work.
3. **Code review.** Reviewing a colleague's tests, you apply the checklist: Are markers registered? Are fixtures scoped properly? Are error cases tested with `pytest.raises`? Do failure messages help?
4. **Preparing for Thursday.** Next, we shift from Python logic to web locators and browser automation, where PyTest remains the runner. A confident foundation makes that transition smooth. We will cover those topics in depth on Thursday and Friday.

---

## Common Mistakes

| Mistake | Effect | Prevention |
|---------|--------|-----------|
| Not reading all tasks before starting | Missed deliverables, wrong file names | Read first; make a checklist |
| Writing a large amount of code before the first run | A wall of errors | Run after every test |
| Forgetting to register markers | Errors with `--strict-markers` | Add to `pytest.ini` first |
| Asserting with `==` on floats | Spurious failures | `pytest.approx` |
| Hard-coded paths | Breaks when run from another folder | `Path(__file__).parent` |
| Copy-pasting tests instead of parametrizing | Lower marks and harder maintenance | Use `parametrize` |
| Tests depend on each other | Pass/fail depends on order | Function-scoped fixtures |
| Leaving the report generation to the last minute | Plugin or hook issues cost time | Generate a report early, regenerate at the end |
| Not running the whole suite at the end | Hidden failures | Final full run, `-ra` |
| No notes | Lost explanation marks | Brief "what/why/trade-off" notes |

---

## Practice Exercises

These are extra drills if your self-score showed gaps. Pick the ones that match your weak areas.

### Exercise 1: Marker and filter drill

Create ten tests with a mixture of `smoke`, `regression` and `slow` markers (some with two). Without running, predict how many tests each of these selects, then check with `--collect-only -q`:

1. `pytest -m smoke`
2. `pytest -m "regression and not slow"`
3. `pytest -k "cart and not empty"`
4. `pytest -m "smoke or slow"`

### Exercise 2: Fixture scope drill

Create a fixture that appends to a module-level list `LOG` on setup and teardown. Use it with `function`, `module` and `session` scopes in turn, running three tests each time. Print `LOG` at the end (use `-s`) and explain how many setups occurred with each scope.

### Exercise 3: Parametrize drill

Take a function `fizzbuzz(n)` that returns `"Fizz"`, `"Buzz"`, `"FizzBuzz"` or `str(n)`. Test it with an inline table of at least 10 rows, then move the table to a CSV file. Ensure types are converted correctly.

### Exercise 4: Mock drill

Write a function `get_username(user_id, http_get)` that calls `http_get(f"/users/{user_id}")` and returns `response["name"]`, raising `LookupError` if the key is missing. Test it with a `Mock` for `http_get` for success and failure, verifying the URL used.

<details>
<summary>Sketch</summary>

```python
from unittest.mock import Mock
import pytest


def get_username(user_id, http_get):
    response = http_get(f"/users/{user_id}")
    try:
        return response["name"]
    except KeyError as exc:
        raise LookupError(f"user {user_id} has no name") from exc


def test_get_username_success():
    http_get = Mock(return_value={"name": "Ana"})
    assert get_username(7, http_get) == "Ana"
    http_get.assert_called_once_with("/users/7")


def test_get_username_missing_name():
    http_get = Mock(return_value={})
    with pytest.raises(LookupError, match="no name"):
        get_username(7, http_get)
```
</details>

### Exercise 5: Retrospective

Write a half-page retrospective: which three skills were hardest during the practice assessment, what you will do to practise them, and which PyTest feature you think will save your Project 1 team the most time.

---

## Summary

- The PyTest skills assessment is a practical check of Monday, Tuesday and Wednesday's skills: fundamentals, fixtures/parametrization/mocking, and framework design with exceptions, custom assertions, reporting and performance awareness.
- Use the competency checklist to find gaps, and the error-decoder table to debug quickly.
- Work methodically: read everything, plan, build the skeleton, add one test at a time, run often, reserve time to regenerate reports and re-run the full suite.
- Explain decisions in "what / why / trade-off" form.
- The practice assessment mirrors real tasks; use the rubric to score yourself honestly and revisit weak topics before moving on to web locators and browser automation on Thursday.

---

## Additional Resources

- PyTest documentation - Get Started: https://docs.pytest.org/en/stable/getting-started.html
- PyTest documentation - How-to guides (fixtures, parametrization, marks, exceptions): https://docs.pytest.org/en/stable/how-to/index.html
- Python documentation - `unittest.mock` library: https://docs.python.org/3/library/unittest.mock.html
