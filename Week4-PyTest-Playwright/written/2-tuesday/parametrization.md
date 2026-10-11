# Parametrization in PyTest

## Learning Objectives

By the end of this lesson you will be able to:

- Explain what parametrization is and why it replaces copy-pasted tests.
- Use `@pytest.mark.parametrize` with one argument and with several arguments.
- Provide readable test IDs using `ids=` and `pytest.param(..., id=...)`.
- Mark individual parameter sets with `skip`, `xfail`, or custom markers.
- Stack decorators to create all combinations (a Cartesian product).
- Load parameter data from a Python list, a helper function, and a CSV/JSON file.
- Select one parameter case from the command line.
- Compare `parametrize` with parametrized fixtures (`params=`).

## Why This Matters

Our weekly epic converts manual test design into automation. Manual test design relies on techniques such as **equivalence partitioning** and **boundary value analysis**, which naturally produce a *table* of inputs and expected results: "age 17 -> invalid, age 18 -> valid, age 65 -> valid, age -1 -> invalid". Automating this table should not mean writing eight nearly identical test functions.

Parametrization lets you write the test **once** and feed it the table. In **Project 1 (QE Foundations)** your utility tests (validators, calculators, formatters) are perfect candidates. Adding a new case means adding one line of data, not a new function. On Wednesday we go further into *data-driven test design* (we will cover this in depth on Wednesday); today you learn the PyTest mechanism that makes it possible.

You should recall from Monday: test functions, `assert`, and markers (`@pytest.mark.xxx`). Today's lesson uses markers heavily.

## The Concept

### 1. The problem: copy-paste tests

Here is a function we want to test:

```python
# validators.py
def is_adult(age):
    """Return True if age is 18 or more. Reject non-integers and negatives."""
    if not isinstance(age, int) or isinstance(age, bool):
        raise TypeError("age must be an integer")
    if age < 0:
        raise ValueError("age cannot be negative")
    return age >= 18
```

Naive tests:

```python
from validators import is_adult

def test_age_17():
    assert is_adult(17) is False

def test_age_18():
    assert is_adult(18) is True

def test_age_19():
    assert is_adult(19) is True

def test_age_0():
    assert is_adult(0) is False
```

Four functions, one idea. Worse, if the first assertion fails, the others still run (good), but you maintain four bodies (bad).

### 2. The basic form

```python
import pytest
from validators import is_adult

@pytest.mark.parametrize("age, expected", [
    (0, False),
    (17, False),
    (18, True),
    (19, True),
    (100, True),
])
def test_is_adult(age, expected):
    assert is_adult(age) is expected
```

**Line-by-line explanation**

- `@pytest.mark.parametrize(...)` - a marker (like the ones you learned on Monday) that tells PyTest to generate several tests from one function.
- `"age, expected"` - a **comma-separated string** naming the function arguments that will receive values. (You can also pass a list or tuple of names: `["age", "expected"]`.)
- The second argument is a **list of tuples**. Each tuple is one **parameter set** (one test case). Values are matched to names by position: first item to `age`, second to `expected`.
- `def test_is_adult(age, expected):` - the function must have parameters with those exact names.
- PyTest creates **five separate tests**, reported individually. If the case `(18, True)` fails, the other four still show as passed.

Run:

```bash
pytest test_validators.py -v
```

Output:

```
test_validators.py::test_is_adult[0-False] PASSED
test_validators.py::test_is_adult[17-False] PASSED
test_validators.py::test_is_adult[18-True] PASSED
test_validators.py::test_is_adult[19-True] PASSED
test_validators.py::test_is_adult[100-True] PASSED
```

The bit inside `[...]` is the **test ID** PyTest generated from the values.

### 3. A single argument

When there is just one name, supply a flat list:

```python
@pytest.mark.parametrize("word", ["level", "radar", "madam"])
def test_palindromes(word):
    assert word == word[::-1]
```

`word[::-1]` is Python slicing that reverses a string. Three tests are generated.

### 4. Readable test IDs

Auto IDs like `[0-False]` are cryptic, and for objects they become `obj0`, `obj1`. Use `ids` to improve readability:

```python
@pytest.mark.parametrize(
    "age, expected",
    [(17, False), (18, True), (0, False)],
    ids=["just-below-limit", "exact-limit", "zero"],
)
def test_is_adult_ids(age, expected):
    assert is_adult(age) is expected
```

IDs now read `test_is_adult_ids[just-below-limit]`. This helps in reports (and later in HTML reports on Wednesday). The list of `ids` must be the same length as the data.

`ids` can also be a **function** that receives each value and returns a string:

```python
def age_id(value):
    return f"age={value}" if isinstance(value, int) else None

@pytest.mark.parametrize("age", [10, 18, 30], ids=age_id)
def test_ids_function(age):
    assert isinstance(age, int)
```

Returning `None` lets PyTest fall back to its default ID.

### 5. `pytest.param`: per-case ID, marks

`pytest.param` wraps one parameter set so you can attach an `id` and `marks`:

```python
import pytest
from validators import is_adult

@pytest.mark.parametrize("age, expected", [
    pytest.param(17, False, id="below-18"),
    pytest.param(18, True, id="boundary"),
    pytest.param(
        200, True, id="very-old",
        marks=pytest.mark.slow,
    ),
    pytest.param(
        -1, False, id="negative-bug",
        marks=pytest.mark.xfail(reason="negative ages raise ValueError, not False", raises=ValueError),
    ),
    pytest.param(
        30, True, id="skip-me",
        marks=pytest.mark.skip(reason="demo of skipping one case"),
    ),
])
def test_is_adult_marks(age, expected):
    assert is_adult(age) is expected
```

**Explanation**

- `id="boundary"` names this case.
- `marks=pytest.mark.slow` attaches a custom marker (remember to register custom markers in `pytest.ini` to avoid warnings; see Monday's *Markers* lesson). You can then run `pytest -m slow`.
- `xfail` means "expected failure": the case is known to fail. With `raises=ValueError`, only that exception counts as the expected failure. Here `is_adult(-1)` raises `ValueError`, so the case is reported as `xfailed` (not as a failure).
- `skip` excludes just that case. The rest still run.
- Multiple marks go in a list: `marks=[pytest.mark.slow, pytest.mark.smoke]`.

### 6. Expecting exceptions in parameter sets

Often some inputs should raise. A neat approach is to parametrize the input and the expected exception separately:

```python
import pytest
from validators import is_adult

@pytest.mark.parametrize("bad_input, exc", [
    (-5, ValueError),
    ("18", TypeError),
    (18.5, TypeError),
    (True, TypeError),
])
def test_is_adult_errors(bad_input, exc):
    with pytest.raises(exc):
        is_adult(bad_input)
```

`pytest.raises(exc)` is a context manager that passes only if the code inside raises `exc`. (Exception testing gets its own full lesson on Wednesday.)

### 7. Stacking decorators: all combinations

Stacking multiple `parametrize` decorators creates the **Cartesian product** (every combination):

```python
import pytest

@pytest.mark.parametrize("x", [1, 2, 3])
@pytest.mark.parametrize("y", [10, 20])
def test_multiplication_commutes(x, y):
    assert x * y == y * x
```

This generates 3 x 2 = 6 tests: `[10-1]`, `[10-2]`, `[10-3]`, `[20-1]`, `[20-2]`, `[20-3]`. Notice the **bottom decorator's** value appears first in the ID. Use stacking for independent dimensions, like browser x screen-size, or currency x amount.

Be careful: combinations grow multiplicatively. Three decorators with 10 values each give 1,000 tests.

### 8. Parametrizing with objects and dictionaries

Parameters can be any Python object:

```python
import pytest

CASES = [
    {"email": "a@b.com", "valid": True},
    {"email": "no-at-sign.com", "valid": False},
    {"email": "x@y", "valid": False},
]

def looks_like_email(text):
    if "@" not in text:
        return False
    local, _, domain = text.partition("@")
    return bool(local) and "." in domain

@pytest.mark.parametrize("case", CASES, ids=lambda c: c["email"])
def test_email(case):
    assert looks_like_email(case["email"]) is case["valid"]
```

- `lambda c: c["email"]` is an anonymous function used for the ID.
- `str.partition("@")` splits at the first `@` into `(before, "@", after)`.

### 9. Loading parameters from files

Hard-coding data is fine for small tables. For large or shared data, keep it in a file. Reading happens when PyTest *collects* tests, so the file must be read at import time or in a helper.

```python
# test_prices_from_csv.py
import csv
from pathlib import Path
import pytest

def load_cases(filename):
    path = Path(__file__).parent / filename
    with open(path, newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        return [
            pytest.param(float(r["price"]), int(r["qty"]), float(r["total"]), id=r["case"])
            for r in reader
        ]

@pytest.mark.parametrize("price, qty, total", load_cases("prices.csv"))
def test_line_total(price, qty, total):
    assert price * qty == pytest.approx(total)
```

With `prices.csv` next to the test:

```csv
case,price,qty,total
one-item,2.50,1,2.50
three-items,2.50,3,7.50
zero-qty,9.99,0,0
```

**Explanation**

- `Path(__file__).parent` - the folder containing this test file, so the path works no matter where you run `pytest` from.
- `csv.DictReader` turns each row into a dictionary keyed by the header.
- CSV values are strings, so we convert with `float()` and `int()`.
- `pytest.approx` compares floating-point numbers with a tolerance (because `0.1 + 0.2 != 0.3` exactly).
- The same pattern works with JSON using `json.load`.

### 10. Generating parameters with Python

```python
import pytest

def boundary_values(low, high):
    return [low - 1, low, low + 1, high - 1, high, high + 1]

@pytest.mark.parametrize("n", boundary_values(1, 10))
def test_in_range_only_inside(n):
    inside = 1 <= n <= 10
    assert inside == (n in range(1, 11))
```

This directly models **boundary value analysis** from manual test design.

### 11. Parametrizing classes and `indirect`

You can apply `parametrize` to a class; then every test method must accept the argument:

```python
@pytest.mark.parametrize("n", [1, 2])
class TestNumbers:
    def test_positive(self, n):
        assert n > 0

    def test_integer(self, n):
        assert isinstance(n, int)
```

This produces four tests. 

`indirect=True` routes the value through a fixture of the same name first. We cover that in the next lesson, *Combining fixtures and parametrization*.

### 12. Parametrized fixtures vs `parametrize`

From the *Fixtures* lesson: `@pytest.fixture(params=[...])`.

| `@pytest.mark.parametrize` | `@pytest.fixture(params=...)` |
|----------------------------|-------------------------------|
| Applies to one test function (or class) | Applies to **every** test that uses the fixture |
| Data is visible right at the test | Data is hidden in the fixture |
| Most common for input/expected tables | Good for "run everything under each environment" (browser, database) |

### 13. Running and selecting parametrized cases

```bash
pytest -v                                        # all cases
pytest -k "boundary"                             # by ID substring
pytest "test_validators.py::test_is_adult[18-True]"   # one exact case
pytest -m slow                                   # by marker attached via pytest.param
pytest --collect-only -q                         # list generated test IDs without running
```

Quote the node ID so your shell does not interpret the brackets. `--collect-only` is the best way to preview the IDs you will get.

## Code Examples: a Project 1 scenario

Project 1 utilities often include a *discount calculator*. Here is a function and a data-driven test.

```python
# pricing.py
def discounted_price(price, customer_type):
    """Apply discounts: regular 0%, silver 10%, gold 20%. Price must be >= 0."""
    if price < 0:
        raise ValueError("price cannot be negative")
    rates = {"regular": 0.0, "silver": 0.10, "gold": 0.20}
    if customer_type not in rates:
        raise KeyError(f"unknown customer type: {customer_type}")
    return round(price * (1 - rates[customer_type]), 2)
```

```python
# test_pricing.py
import pytest
from pricing import discounted_price

@pytest.mark.parametrize("price, ctype, expected", [
    pytest.param(100, "regular", 100.00, id="regular-no-discount"),
    pytest.param(100, "silver", 90.00, id="silver-10pct"),
    pytest.param(100, "gold", 80.00, id="gold-20pct"),
    pytest.param(0, "gold", 0.00, id="zero-price"),
    pytest.param(19.99, "silver", 17.99, id="decimal-rounding"),
])
def test_discounted_price(price, ctype, expected):
    assert discounted_price(price, ctype) == pytest.approx(expected)

@pytest.mark.parametrize("price, ctype, exc", [
    (-1, "regular", ValueError),
    (10, "platinum", KeyError),
])
def test_discounted_price_errors(price, ctype, exc):
    with pytest.raises(exc):
        discounted_price(price, ctype)
```

**Explanation:** The first test covers valid equivalence classes and boundaries (zero, decimals); the second covers invalid ones. Each table row maps one-to-one to a line in your manual test design document, so reviewers can compare the two easily. Check the math: 19.99 x 0.9 = 17.991, rounded to 17.99.

## Real-World Scenarios

1. **Form validation:** dozens of valid/invalid emails, passwords, and phone numbers in a table.
2. **Cross-browser/viewport testing:** stack decorators for browser x viewport (Playwright integration will be covered in depth on Friday).
3. **API status codes:** `(endpoint, method, expected_status)` rows.
4. **Localization:** `(language, key, expected_text)` rows.
5. **Regression:** each fixed bug adds one parameter row proving it does not return.

## Common Mistakes

1. **Name mismatch.** The names in the string must match function parameters exactly, or you get "function uses no argument 'xyz'".
2. **Wrong number of values per tuple.** `("age, expected", [(17,)])` raises an error at collection time.
3. **Passing a string instead of a list for a single argument:** `parametrize("x", "abc")` iterates over characters. Use `["abc"]`.
4. **Mutable parameter objects shared across cases.** A list or dict passed as a parameter is the *same object* each time it is used; mutating it in one test affects others. Copy it inside the test.
5. **Unreadable IDs.** Provide `ids` or `pytest.param(id=...)` for non-trivial data.
6. **Giant Cartesian products** that make runs slow.
7. **Putting logic in the test** (`if age < 18: expected = False`). That re-implements the code under test; use literal expected values.
8. **Reading files relative to the current directory** instead of `__file__`, which breaks when run from another folder.
9. **Duplicate IDs.** PyTest appends suffixes (`0`, `1`) to disambiguate; avoid duplicates by naming cases.

## Practice Exercises

**Exercise 1.** Parametrize a test for a function `square(n)` with inputs `-3, 0, 2, 5`. Expected values: `9, 0, 4, 25`.

*Solution:*

```python
import pytest

def square(n):
    return n * n

@pytest.mark.parametrize("n, expected", [(-3, 9), (0, 0), (2, 4), (5, 25)])
def test_square(n, expected):
    assert square(n) == expected
```

**Exercise 2.** Add `ids=["negative","zero","small","larger"]` to Exercise 1 and verify with `pytest -v`.

**Exercise 3.** Write a function `grade(score)` returning "A" for 90+, "B" for 80-89, "C" for 70-79, otherwise "F". Parametrize boundary values: 69, 70, 79, 80, 89, 90, 100.

*Hint:* boundaries sit on both sides of each cut-off.

**Exercise 4.** Use `pytest.param` with an `xfail` mark for a known bug: a function `half(n)` that uses `n / 2` but should return an `int` for even numbers. Add one case documenting the bug.

**Exercise 5.** Stack two decorators (`x` in 1..3, `y` in 1..2) and run `pytest --collect-only -q`. How many tests? Which ID comes first? *(Six; the bottom decorator's value comes first.)*

**Exercise 6.** Create `emails.json` with five objects like `{"email": "...", "valid": true}` and parametrize `looks_like_email` from it using `json.load`.

*Hint:* mirror the CSV loader, but use `json.load(f)` and a list comprehension with `pytest.param(..., id=...)`.

**Exercise 7 (Project 1 link).** Pick one of your Project 1 utility tests with three or more near-duplicate functions and merge them into one parametrized test with readable IDs. Confirm the number of collected tests stays the same using `--collect-only`.

## Summary

- Parametrization generates many tests from one function and a table of data.
- Syntax: `@pytest.mark.parametrize("a, b", [(1, 2), (3, 4)])`; parameter names must match the function arguments.
- Improve readability with `ids=` or `pytest.param(..., id=...)`.
- `pytest.param` can attach `marks` (skip, xfail, custom) to individual cases.
- Stacked decorators create a Cartesian product; watch the count.
- Parameter data can come from lists, generator functions, CSV, or JSON.
- Select cases with `-k`, `-m`, or a full node ID; preview with `--collect-only`.
- Choose `parametrize` for input/expected tables, parametrized fixtures for environments.
- Next: combining fixtures and parametrization.

## Additional Resources

- How to parametrize fixtures and test functions: https://docs.pytest.org/en/stable/how-to/parametrize.html
- `pytest.param` and `Metafunc` reference: https://docs.pytest.org/en/stable/reference/reference.html#pytest-param
- Python `csv` module: https://docs.python.org/3/library/csv.html
