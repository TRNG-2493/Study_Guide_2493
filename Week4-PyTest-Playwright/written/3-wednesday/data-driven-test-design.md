# Data-Driven Test Design

## Learning Objectives

By the end of this lesson you will be able to:

- Explain what data-driven testing (DDT) is and how it differs from copy-pasting similar tests.
- Separate **test logic** from **test data** so that adding a new test case means adding a row of data, not writing a new function.
- Store test data in Python structures, JSON files, and CSV files, and load them safely using paths that work from any directory.
- Feed external data into `@pytest.mark.parametrize` with readable test IDs.
- Use `pytest.param` to attach IDs, marks (`skip`, `xfail`), and expected-failure information to individual data rows.
- Design good test data using techniques you know from manual testing: equivalence partitioning, boundary value analysis, and negative cases.
- Recognise the common mistakes that make data-driven suites hard to maintain.

---

## Why This Matters

This week's epic is to convert your **manual test design into automation**, growing from PyTest basics to a complete reporting framework. On Monday you learned how to write and run individual tests. On Tuesday you learned fixtures, parametrization, `conftest.py` and mocking. Today we put those pieces together into a **framework**, and the single most important design decision in any framework is how you handle test data.

In **Project 1 – QE Foundations**, you wrote manual test cases that look like this:

| Test ID | Input | Expected result |
|---------|-------|-----------------|
| TC-01 | age = 17 | Not eligible |
| TC-02 | age = 18 | Eligible |
| TC-03 | age = 65 | Eligible |
| TC-04 | age = -1 | Error: invalid age |

Notice the shape: **the steps are identical, only the input and expected result change.** A manual tester often keeps this as a table in a spreadsheet. Data-driven testing is the automation equivalent: the table becomes a Python list (or a JSON/CSV file), and **one** test function runs once per row.

In industry this matters because:

- Business teams add new scenarios constantly (new countries, new price tiers, new validation rules). If adding a scenario means copying a function, the suite becomes unmaintainable within weeks.
- Data can be reviewed by non-programmers (a business analyst can read a CSV).
- A bug in the test *logic* is fixed in one place instead of in fifty copies.

---

## The Concept

### 1. What is data-driven testing?

**Definition:** Data-driven testing is a design approach where the *same test logic* is executed multiple times with *different sets of input data* and expected outputs, and the data is kept separate from the logic.

Think of a **cookie cutter and dough**. The cookie cutter (test logic) never changes. You press it into different pieces of dough (data) and get different cookies (test results). If you wanted a new cookie you would not build a new cutter; you would just roll out more dough.

#### Without data-driven design (the "copy-paste" smell)

```python
# test_discount_bad.py
from pricing import apply_discount


def test_discount_10_percent():
    assert apply_discount(100.0, 10) == 90.0


def test_discount_0_percent():
    assert apply_discount(100.0, 0) == 100.0


def test_discount_100_percent():
    assert apply_discount(100.0, 100) == 0.0


def test_discount_50_percent():
    assert apply_discount(80.0, 50) == 40.0
```

Four functions, one idea. If the signature of `apply_discount` changes, you edit four places. With 40 scenarios you edit forty.

#### With data-driven design

```python
# test_discount_good.py
import pytest
from pricing import apply_discount


@pytest.mark.parametrize(
    "price, percent, expected",
    [
        (100.0, 10, 90.0),
        (100.0, 0, 100.0),
        (100.0, 100, 0.0),
        (80.0, 50, 40.0),
    ],
)
def test_apply_discount(price, percent, expected):
    assert apply_discount(price, percent) == expected
```

One function, four test cases. PyTest reports four separate results, so a failure in one row does not hide the others.

For these examples we use a tiny helper module. Create `pricing.py` next to your tests:

```python
# pricing.py
def apply_discount(price: float, percent: float) -> float:
    """Return price after applying a percentage discount (0-100)."""
    if price < 0:
        raise ValueError("price must not be negative")
    if not 0 <= percent <= 100:
        raise ValueError("percent must be between 0 and 100")
    return round(price * (1 - percent / 100), 2)
```

**Line-by-line:**

- `def apply_discount(price: float, percent: float) -> float:` defines a function; `: float` are *type hints* (documentation for humans and tools; Python does not enforce them at runtime).
- The `if price < 0: raise ValueError(...)` guard rejects invalid input by raising an exception. We will test exceptions properly in the *Exception testing* lesson later today.
- `0 <= percent <= 100` is Python's chained comparison: true only if percent is between 0 and 100 inclusive.
- `round(..., 2)` rounds to two decimal places to avoid floating point noise such as `89.99999999`.

### 2. The three parts of a data-driven test

Every data-driven design has three parts. Naming them helps you design cleanly:

1. **Data source**: where the rows live (inline list, Python module, JSON, CSV, database, spreadsheet, API).
2. **Loader**: code that reads the source and turns it into Python objects (a list of tuples or dicts).
3. **Test logic**: the test function that receives one row at a time.

```
 data source  -->  loader  -->  parametrize  -->  test function (runs N times)
 (cases.json)      (load_cases)  (@pytest.mark.parametrize)   (test_apply_discount)
```

### 3. Inline data (the simplest form)

For up to roughly 10 rows, keeping the data directly above the test is perfectly fine and usually the most readable option. You already know this from Tuesday's *Parametrization* lesson.

```python
import pytest
from pricing import apply_discount

CASES = [
    (100.0, 10, 90.0),
    (100.0, 0, 100.0),
    (19.99, 15, 16.99),
]


@pytest.mark.parametrize("price, percent, expected", CASES)
def test_apply_discount_inline(price, percent, expected):
    assert apply_discount(price, percent) == expected
```

Here `CASES` is a module-level constant (UPPER_CASE is a Python convention for constants). Moving the list into a named variable keeps the decorator tidy and lets you reuse the list in several tests.

**When to use inline data:** few rows, data that developers own, data that rarely changes.

### 4. Data in a separate Python module

When the table grows, move it to its own file, for example `test_data/discount_data.py`:

```python
# test_data/discount_data.py
VALID_DISCOUNTS = [
    (100.0, 10, 90.0),
    (100.0, 0, 100.0),
    (100.0, 100, 0.0),
    (80.0, 50, 40.0),
]

INVALID_DISCOUNTS = [
    (-5.0, 10),
    (100.0, -1),
    (100.0, 101),
]
```

And import it:

```python
# test_discount_module_data.py
import pytest
from pricing import apply_discount
from test_data.discount_data import VALID_DISCOUNTS


@pytest.mark.parametrize("price, percent, expected", VALID_DISCOUNTS)
def test_valid_discounts(price, percent, expected):
    assert apply_discount(price, percent) == expected
```

Remember to create an empty `test_data/__init__.py` (or configure `pythonpath` in `pytest.ini`, covered in the *Test organization* lesson) so Python can import the folder as a package.

### 5. Data in a JSON file

JSON (JavaScript Object Notation) is a text format for structured data. It is widely used because both humans and programs can read it, and Python has built-in support through the `json` module.

Create `test_data/discount_cases.json`:

```json
[
  {"id": "ten-percent",   "price": 100.0, "percent": 10,  "expected": 90.0},
  {"id": "zero-percent",  "price": 100.0, "percent": 0,   "expected": 100.0},
  {"id": "full-discount", "price": 100.0, "percent": 100, "expected": 0.0},
  {"id": "half-price",    "price": 80.0,  "percent": 50,  "expected": 40.0}
]
```

Now write the loader and the test:

```python
# test_discount_json.py
import json
from pathlib import Path

import pytest

from pricing import apply_discount

DATA_FILE = Path(__file__).parent / "test_data" / "discount_cases.json"


def load_cases():
    with DATA_FILE.open(encoding="utf-8") as f:
        rows = json.load(f)
    return [
        pytest.param(r["price"], r["percent"], r["expected"], id=r["id"])
        for r in rows
    ]


@pytest.mark.parametrize("price, percent, expected", load_cases())
def test_apply_discount_from_json(price, percent, expected):
    assert apply_discount(price, percent) == expected
```

**Line-by-line explanation:**

- `from pathlib import Path` imports an object-oriented way to work with file paths; it works on Windows, macOS and Linux.
- `Path(__file__)` is the path of the current test file. `__file__` is a special variable Python sets for every module. `.parent` is the folder containing it. The `/` operator joins path parts. This means the data file is found **no matter which directory you launch `pytest` from**. A very common beginner bug is writing `open("test_data/cases.json")`, which only works when you run from one specific folder.
- `DATA_FILE.open(encoding="utf-8")` opens the file; specifying the encoding avoids surprises on Windows.
- `with ... as f:` is a *context manager*: the file is closed automatically even if an error occurs.
- `json.load(f)` parses the JSON into Python lists and dicts.
- The list comprehension `[ ... for r in rows ]` builds one `pytest.param` per row.
- `pytest.param(..., id=r["id"])` wraps one row and gives it a readable name. In the output you will see `test_apply_discount_from_json[ten-percent]` instead of `[100.0-10-90.0]`.
- `load_cases()` is called **at collection time** (when PyTest scans your files, before running any test). That means if the JSON is broken, the whole module fails to collect with a clear error. This is a feature: you find out before any test runs.

### 6. Data in a CSV file

CSV (Comma Separated Values) is what spreadsheets export. It is the best format for handing data to non-programmers because they can edit it in Excel.

`test_data/login_cases.csv`:

```csv
case_id,username,password,expected_valid
valid-user,alice,Secret123!,true
empty-username,,Secret123!,false
empty-password,alice,,false
short-password,alice,abc,false
```

The function we test:

```python
# auth.py
def is_valid_login(username: str, password: str) -> bool:
    """Very small rule set used for teaching purposes."""
    if not username or not password:
        return False
    if len(password) < 8:
        return False
    return True
```

The data-driven test:

```python
# test_login_csv.py
import csv
from pathlib import Path

import pytest

from auth import is_valid_login

DATA_FILE = Path(__file__).parent / "test_data" / "login_cases.csv"


def load_login_cases():
    cases = []
    with DATA_FILE.open(newline="", encoding="utf-8") as f:
        for row in csv.DictReader(f):
            cases.append(
                pytest.param(
                    row["username"],
                    row["password"],
                    row["expected_valid"].strip().lower() == "true",
                    id=row["case_id"],
                )
            )
    return cases


@pytest.mark.parametrize("username, password, expected", load_login_cases())
def test_is_valid_login(username, password, expected):
    assert is_valid_login(username, password) is expected
```

**Key points:**

- `csv.DictReader` reads each row as a dictionary keyed by the header names, so `row["username"]` is self-explanatory.
- **Everything read from a CSV is a string.** The text `true` is not the boolean `True`. That is why we convert with `row["expected_valid"].strip().lower() == "true"`. Forgetting this conversion is the number one CSV bug: `assert result is "false"` would never behave as you expect. Similarly, numbers must be converted with `int(...)` or `float(...)`.
- `newline=""` is what the `csv` module documentation recommends when opening CSV files, so line endings are handled correctly.
- An empty cell becomes the empty string `""`, which is exactly what we want to test the "empty username" scenario.

### 7. Using `pytest.param` for IDs and marks

You saw `pytest.param` in the previous example. It lets you attach metadata to **one specific row**:

```python
import pytest
from pricing import apply_discount

CASES = [
    pytest.param(100.0, 10, 90.0, id="typical"),
    pytest.param(100.0, 0, 100.0, id="no-discount"),
    pytest.param(
        100.0, 100, 0.0,
        id="free-item",
        marks=pytest.mark.smoke,
    ),
    pytest.param(
        19.995, 0, 20.0,
        id="rounding-bug-known",
        marks=pytest.mark.xfail(reason="BUG-1234: rounding of .995", strict=False),
    ),
    pytest.param(
        50.0, 50, 25.0,
        id="windows-only",
        marks=pytest.mark.skipif(
            __import__("sys").platform != "win32",
            reason="demonstration of a conditional skip",
        ),
    ),
]


@pytest.mark.parametrize("price, percent, expected", CASES)
def test_discount_with_marks(price, percent, expected):
    assert apply_discount(price, percent) == expected
```

Explanation:

- `id="typical"` sets the test-ID suffix.
- `marks=pytest.mark.smoke` applies a custom marker to only that row, so `pytest -m smoke` will select only it. (Remember to register custom markers in `pytest.ini`, as covered on Monday, otherwise PyTest warns about unknown markers.)
- `pytest.mark.xfail(reason=...)` means "we *expect* this to fail because of a known bug". If it fails, the result is reported as `xfailed` (not a failure). If it unexpectedly passes, it is `xpassed`; with `strict=True` an unexpected pass would be reported as a failure, which is a good way to be told "the bug is fixed, remove the marker".
- `pytest.mark.skipif(condition, reason=...)` skips only when the condition is true.

This is extremely useful in data-driven suites because a single bad row can be marked without disabling the entire test.

### 8. Choosing readable IDs automatically

If you do not give an ID, PyTest generates one from the values (`100.0-10-90.0`). That is fine for numbers, but for objects, dictionaries and long strings you get `data0`, `data1` which is useless in a report. You can supply `ids=` as a list or a function:

```python
import pytest

emails = ["a@b.com", "no-at-sign", "", "x@y"]


@pytest.mark.parametrize("email", emails, ids=lambda e: repr(e) if e == "" else e)
def test_email_is_string(email):
    assert isinstance(email, str)
```

Here the `ids` callable is invoked for each value and returns the label. An empty string would otherwise produce an unhelpful empty ID, so we use `repr(e)` to show `''`.

### 9. Designing good test data

Having a mechanism for data is half the job. The other half is deciding **which rows to include**. Use the techniques from your manual testing training.

#### Equivalence partitioning

Divide inputs into groups that the system should treat identically, then pick one representative from each group. For a discount percent (valid range 0-100):

| Partition | Example |
|-----------|---------|
| Below range (invalid) | -10 |
| In range (valid) | 25 |
| Above range (invalid) | 150 |

#### Boundary value analysis

Bugs love the edges. Test exactly at, just below and just above each boundary: `-1, 0, 1, 99, 100, 101`.

#### Negative and unusual input

Empty string, `None`, very long strings, strings with spaces, special characters (`'`, `"`, `<`, `>`), Unicode, zero, negative numbers, extremely large numbers.

#### Putting it together

```python
import pytest
from pricing import apply_discount

BOUNDARY_VALID = [
    pytest.param(0, 100.0, id="lower-bound-0"),
    pytest.param(1, 99.0, id="just-above-lower"),
    pytest.param(99, 1.0, id="just-below-upper"),
    pytest.param(100, 0.0, id="upper-bound-100"),
]

BOUNDARY_INVALID = [
    pytest.param(-1, id="just-below-lower"),
    pytest.param(101, id="just-above-upper"),
]


@pytest.mark.parametrize("percent, expected", BOUNDARY_VALID)
def test_percent_boundaries_valid(percent, expected):
    assert apply_discount(100.0, percent) == expected


@pytest.mark.parametrize("percent", BOUNDARY_INVALID)
def test_percent_boundaries_invalid(percent):
    with pytest.raises(ValueError):
        apply_discount(100.0, percent)
```

Notice that valid and invalid inputs live in **separate tests**. A single test should not contain an `if expected_error:` branch; that is a smell we discuss below.

### 10. Data-driven tests with dictionaries (self-documenting rows)

When a row has more than three or four columns, positional tuples become hard to read ("what was the fourth value again?"). Use dictionaries or a small `dataclass`:

```python
from dataclasses import dataclass

import pytest


@dataclass(frozen=True)
class ShippingCase:
    weight_kg: float
    country: str
    express: bool
    expected_cost: float


def shipping_cost(weight_kg, country, express):
    base = 5.0 if country == "US" else 12.0
    cost = base + weight_kg * 1.5
    if express:
        cost *= 2
    return round(cost, 2)


CASES = [
    pytest.param(ShippingCase(1.0, "US", False, 6.5), id="us-standard"),
    pytest.param(ShippingCase(1.0, "US", True, 13.0), id="us-express"),
    pytest.param(ShippingCase(2.0, "DE", False, 15.0), id="de-standard"),
]


@pytest.mark.parametrize("case", CASES)
def test_shipping_cost(case):
    result = shipping_cost(case.weight_kg, case.country, case.express)
    assert result == case.expected_cost
```

- `@dataclass` generates `__init__`, `__repr__` and comparison methods for a class that is mostly data. `frozen=True` makes instances immutable, which stops a test from accidentally altering shared data.
- Each parametrized test now receives **one** argument (`case`) and reads `case.country`, which is clearer than `row[1]`.

### 11. Combining data-driven tests with fixtures

You learned on Tuesday that fixtures provide set-up objects. They combine naturally with parametrization:

```python
import pytest


@pytest.fixture
def cart():
    # a fresh empty cart for every test row
    return []


@pytest.mark.parametrize("item, qty", [("pen", 1), ("book", 3), ("lamp", 2)])
def test_add_items(cart, item, qty):
    cart.append((item, qty))
    assert cart == [(item, qty)]
```

The fixture `cart` is created fresh for each parametrized call (function scope), so rows never leak state into each other. That isolation is essential: **data rows must be independent**. Never write a test that only passes if the previous row ran first.

### 12. Loading data via a fixture or `conftest.py`

You can also expose data through fixtures defined in `conftest.py` (see Tuesday). This is useful when the *loading itself* is expensive (a large file, a database query) and you want it done once:

```python
# conftest.py
import json
from pathlib import Path

import pytest


@pytest.fixture(scope="session")
def discount_rows():
    path = Path(__file__).parent / "test_data" / "discount_cases.json"
    return json.loads(path.read_text(encoding="utf-8"))
```

```python
# test_loop_in_fixture.py
from pricing import apply_discount


def test_all_rows(discount_rows):
    for row in discount_rows:
        assert apply_discount(row["price"], row["percent"]) == row["expected"]
```

**Trade-off:** this runs all rows inside one test, so the first failing row stops the loop and the report shows one test, not N. Parametrization (sections 3-8) gives separate pass/fail per row and is almost always better for reporting. Use the fixture-with-loop approach only for cheap "sanity sweep" checks.

### 13. When data-driven design is NOT the right tool

- The scenarios differ in *steps*, not only in data. Write separate tests.
- Each row needs its own complicated setup. Use fixtures or separate tests.
- You have thousands of random combinations. Consider property-based testing (e.g. the Hypothesis library); we will not go deeper here.

---

## Real-World Scenarios

1. **Registration form validation.** A QA team keeps a CSV with 60 rows of username/email/password combinations and expected error messages. A single test function covers every validation rule; when product adds a rule, a tester adds rows.
2. **Tax calculation for multiple regions.** Rates live in a JSON file maintained by the finance team. The test reads it and checks the calculator against every region.
3. **Cross-browser or cross-environment checks.** Later this week, once we introduce browser automation, the same data-driven approach lets one test run for many user types and pages. We will cover this in depth on Thursday and Friday.

---

## Common Mistakes

| Mistake | Why it hurts | Fix |
|---------|--------------|-----|
| Relative file paths such as `open("data.json")` | Fails when run from another folder or by CI | Build paths from `Path(__file__).parent` |
| Forgetting CSV values are strings | `"5" == 5` is `False`; booleans come out wrong | Convert with `int()`, `float()`, explicit boolean parsing |
| `if`/`else` logic inside the test to handle "expected error" rows | Test becomes a mini-program that can itself be wrong | Split into positive and negative tests |
| One enormous table mixing unrelated scenarios | Nobody can tell what each row proves | Group rows by behaviour; one table per test |
| No IDs | Reports say `[0]`, `[1]`, `[2]` | Use `id=` or `ids=` |
| Rows that depend on one another | Fail when run alone or in random order | Keep rows independent; use fixtures for setup |
| Computing the expected value with the same code you are testing | Test can never fail | Hard-code expected values from the specification |
| Loading data at import time without error handling | A missing file produces a confusing collection error | Use clear paths and let the error name the file; add a helpful assertion/message |

---

## Practice Exercises

### Exercise 1: Inline table

Given:

```python
def is_leap_year(year: int) -> bool:
    return year % 4 == 0 and (year % 100 != 0 or year % 400 == 0)
```

Write one parametrized test with at least eight rows (include 1900, 2000, 2023, 2024, 2100, and one negative case of your choice). Give each row an `id`.

<details>
<summary>Solution</summary>

```python
import pytest


def is_leap_year(year: int) -> bool:
    return year % 4 == 0 and (year % 100 != 0 or year % 400 == 0)


@pytest.mark.parametrize(
    "year, expected",
    [
        pytest.param(1900, False, id="century-not-leap"),
        pytest.param(2000, True, id="400-divisible-leap"),
        pytest.param(2023, False, id="ordinary-non-leap"),
        pytest.param(2024, True, id="ordinary-leap"),
        pytest.param(2100, False, id="century-2100"),
        pytest.param(4, True, id="year-4"),
        pytest.param(1, False, id="year-1"),
        pytest.param(0, True, id="year-zero"),
    ],
)
def test_is_leap_year(year, expected):
    assert is_leap_year(year) is expected
```
</details>

### Exercise 2: Move the data to JSON

Take Exercise 1 and move the data to `test_data/leap_years.json`. Write `load_cases()` using `pathlib`. Verify you can run `pytest` from the project root *and* from inside the tests folder.

*Hint:* use `Path(__file__).parent / "test_data" / "leap_years.json"`.

### Exercise 3: CSV with type conversion

Create a CSV with columns `case_id,a,b,expected` for an `add(a, b)` function. Include rows for negative numbers and zero. In your loader convert `a`, `b`, `expected` to `int`. Add a deliberately wrong row and confirm the report shows which `case_id` failed, then fix the row.

### Exercise 4: Boundary analysis for Project 1

Choose one utility function from your Project 1 test plan (for example an age-eligibility check, password strength check, or a discount calculator). List its equivalence partitions and boundaries on paper, then create a data table that covers them. Implement it as a parametrized test with `pytest.param` IDs. Mark one boundary row as `smoke`.

### Exercise 5: Spot the bug

What is wrong with this test, and how would you fix it?

```python
@pytest.mark.parametrize("a, b", [(1, 2), (2, 3), (3, 4)])
def test_add(a, b):
    expected = a + b
    assert a + b == expected
```

<details>
<summary>Answer</summary>
The expected value is calculated with the same expression as the code under test, so the assertion is always true (a tautology). Provide a third parameter with a hard-coded expected value taken from the specification: `(1, 2, 3)`, and call the real function under test, not `a + b`.
</details>

---

## Summary

- Data-driven testing separates **test logic** from **test data**: one function, many rows.
- Data can live inline, in a Python module, in JSON, or in CSV. Choose the simplest option that fits the data size and the people who edit it.
- Always build file paths from `Path(__file__).parent` so tests run from anywhere.
- CSV values are strings; convert them explicitly.
- `pytest.param` gives per-row IDs and marks (`skip`, `skipif`, `xfail`, custom markers).
- Choose data deliberately with equivalence partitions, boundary values and negative cases.
- Keep rows independent, keep positive and negative tests separate, and hard-code expected results.

---

## Additional Resources

- PyTest documentation - How to parametrize fixtures and test functions: https://docs.pytest.org/en/stable/how-to/parametrize.html
- Python documentation - `csv` module: https://docs.python.org/3/library/csv.html
- Python documentation - `json` module: https://docs.python.org/3/library/json.html
