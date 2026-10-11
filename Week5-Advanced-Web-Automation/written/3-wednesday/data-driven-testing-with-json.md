# Data-Driven Testing with JSON

## Learning Objectives

By the end of this lesson you will be able to:

- Define data-driven testing and explain why separating **test logic** from **test data** makes suites smaller, clearer, and easier to extend.
- Read and write **JSON** confidently: objects, arrays, strings, numbers, booleans, `null`, nesting, and the syntax rules that most often cause errors.
- Use Python's built-in **`json` module** (`json.load`, `json.loads`, `json.dump`, `json.dumps`) together with `pathlib` to read data files reliably, regardless of where pytest is launched from.
- Use **`@pytest.mark.parametrize`** to run one test body many times, with readable test ids, multiple arguments, and per-case marks (`skip`, `xfail`) via `pytest.param`.
- Build a small **data-loader utility** and combine it with parametrisation to drive Playwright tests from JSON files.
- Use fixtures, `indirect` parametrisation, stacked parametrisation, and the `pytest_generate_tests` hook for more advanced data-driven designs.
- Design good JSON test data: naming, structure, expected results, negative cases, environment-specific data, and keeping secrets out.
- Combine data-driven tests with the Page Object Model on SauceDemo (login, checkout validation, product sorting).
- Avoid the traps: over-large data sets, logic hidden in data, invalid JSON, wrongly relative paths, and unreadable test ids.

---

## Why This Matters

The SauceDemo login page supports several user types: `standard_user`, `locked_out_user`, `problem_user`, `performance_glitch_user`, plus all the invalid combinations a tester should try (empty username, empty password, wrong password, unknown user). Without data-driven design you would write one test function per combination, each a near copy of the last. With data-driven design you write **one** test and a **table of cases**. Adding the next case becomes a one-line data change, not a new function, and a non-programmer (a business analyst or manual tester) can often read or even add rows.

This is core to this week's epic: structuring Playwright tests so they are maintainable. Fixtures, hooks, and the Page Object Model (covered earlier today) separate *infrastructure* and *page mechanics* from tests. Data-driven testing is the final separation: **what we test with** (data) from **what we test** (behaviour).

It also directly matches the Wednesday exercise and **Project 1 - QE Foundations**: you are asked to refactor your UI tests into POM *with data-driven JSON*. Reviewers look for an obvious `data/` folder, tests driven by it, and no copy-pasted test bodies. The skill also transfers: the same idea underlies API testing with request/response tables, database test cases, and even the CSV-driven approaches you may meet in other tools.

You will use the skills from earlier this week: page objects to perform actions, fixtures to deliver them, and the locators and interactions from Monday and Tuesday. Retries and reporting (the next two lessons) will also benefit: readable test ids make failures in reports instantly understandable.

---

## The Concept

### 1. What is data-driven testing?

**Data-driven testing (DDT)** is a technique where the same test logic runs repeatedly against different input data sets, and each data set may have its own expected result. The data lives outside the test function (in a list, a file, a database), and the test function is parameterised.

An analogy: a recipe (the logic) used with different ingredient lists (the data) gives different dishes, but you do not rewrite the cooking method for each dish.

A concrete comparison, without a framework:

```python
# Not data-driven: three nearly identical tests
def test_login_locked_out(login_page):
    login_page.login_as("locked_out_user", "secret_sauce")
    assert "locked out" in login_page.get_error_message()

def test_login_wrong_password(login_page):
    login_page.login_as("standard_user", "wrong")
    assert "do not match" in login_page.get_error_message()

def test_login_empty_username(login_page):
    login_page.login_as("", "secret_sauce")
    assert "Username is required" in login_page.get_error_message()
```

```python
# Data-driven: one test, a table of cases
import pytest

CASES = [
    ("locked_out_user", "secret_sauce", "locked out"),
    ("standard_user",   "wrong",        "do not match"),
    ("",                "secret_sauce", "Username is required"),
]

@pytest.mark.parametrize("username, password, expected", CASES)
def test_invalid_login(login_page, username, password, expected):
    login_page.login_as(username, password)
    assert expected in login_page.get_error_message()
```

Benefits:

- **Less code.** The logic is written once.
- **More coverage with less effort.** A new scenario is a new row.
- **Clearer reports.** Each row is its own test result; you see precisely which row failed.
- **Separation of roles.** Anyone can maintain the data; engineers maintain the logic.

Costs and limits:

- Data-driven tests are best when the *behaviour is the same* and only inputs/outputs differ. If different rows need different steps, you need different tests.
- Large tables of unclear data are unreadable. Name your cases.

### 2. JSON in 10 minutes

**JSON (JavaScript Object Notation)** is a text format for structured data. Despite the name, it is language-independent; Python, Java, JavaScript, and nearly everything else can read it. It is the most common format for test data and for API payloads, which makes it a doubly useful skill.

JSON has exactly six kinds of value:

| JSON type | Example | Python equivalent after loading |
|---|---|---|
| object | `{"name": "Asha", "age": 30}` | `dict` |
| array | `[1, 2, 3]` | `list` |
| string | `"hello"` | `str` |
| number | `42`, `3.14` | `int`, `float` |
| boolean | `true`, `false` | `True`, `False` |
| null | `null` | `None` |

An example of a test-data file for SauceDemo login scenarios:

```json
{
  "valid_users": [
    { "username": "standard_user", "password": "secret_sauce" },
    { "username": "problem_user",  "password": "secret_sauce" },
    { "username": "performance_glitch_user", "password": "secret_sauce" }
  ],
  "invalid_logins": [
    {
      "id": "locked-out-user",
      "username": "locked_out_user",
      "password": "secret_sauce",
      "expected_error": "Epic sadface: Sorry, this user has been locked out."
    },
    {
      "id": "wrong-password",
      "username": "standard_user",
      "password": "not_the_password",
      "expected_error": "Epic sadface: Username and password do not match any user in this service"
    },
    {
      "id": "empty-username",
      "username": "",
      "password": "secret_sauce",
      "expected_error": "Epic sadface: Username is required"
    },
    {
      "id": "empty-password",
      "username": "standard_user",
      "password": "",
      "expected_error": "Epic sadface: Password is required"
    }
  ]
}
```

**Syntax rules that trip up beginners:**

1. **Keys must be in double quotes.** `{name: "x"}` is invalid JSON (that is JavaScript syntax). Single quotes are not allowed anywhere.
2. **No trailing commas.** `[1, 2, 3,]` is invalid. This is the most common error when editing by hand.
3. **No comments.** JSON does not support `//` or `#`. If you need explanations, add a field such as `"description"`.
4. **Strings must escape special characters:** `\"` for a quote, `\\` for a backslash, `\n` for a newline.
5. **Booleans and null are lower case:** `true`, `false`, `null`, not `True`/`None`.
6. **Numbers have no quotes** (a quoted number is a string).

When a file will not load, Python raises `json.JSONDecodeError` with the line and column, which usually points right at the problem. VS Code highlights JSON errors as you type, and the command `python -m json.tool data/login_data.json` validates a file from the terminal and pretty-prints it.

### 3. Reading JSON in Python with the `json` module

`json` is part of Python's standard library; there is nothing to install.

```python
import json

# From a string
text = '{"username": "standard_user", "attempts": 3, "locked": false}'
data = json.loads(text)          # loads = "load string"
print(data["username"])          # standard_user
print(type(data["attempts"]))    # <class 'int'>
print(data["locked"])            # False

# From a file
with open("data/login_data.json", encoding="utf-8") as f:
    data = json.load(f)          # load = "load from a file object"
```

Line by line:

- `import json` makes the module available.
- `json.loads(text)` ("load **s**tring") parses a string into Python objects. The letter `s` is the trick for remembering: `loads`/`dumps` work with **s**trings; `load`/`dump` work with file objects.
- `data["username"]` indexes the resulting `dict` like any Python dictionary.
- `with open(...) as f:` opens a file and **guarantees it is closed** when the indented block finishes, even if an error occurs. `encoding="utf-8"` avoids platform-dependent decoding problems (Windows defaults to a different encoding).
- `json.load(f)` reads the file and parses it.

Writing JSON (useful for saving results or generating data):

```python
payload = {"username": "standard_user", "items": ["backpack", "bike light"]}

print(json.dumps(payload))                 # compact string
print(json.dumps(payload, indent=2))       # pretty-printed string

with open("out.json", "w", encoding="utf-8") as f:
    json.dump(payload, f, indent=2)        # write to file
```

- `json.dumps` ("dump string") turns Python objects into a JSON string; `indent=2` adds line breaks and two-space indentation to make it readable.
- `json.dump(obj, f)` writes directly to the open file.
- Opening with `"w"` truncates (empties) the file first.

### 4. Finding the file reliably: `pathlib`

A very common mistake is `open("data/login_data.json")`. That path is relative to the **current working directory**, which depends on where you launched pytest from (project root, an IDE's default folder, a CI runner). Running from a different place yields `FileNotFoundError`. The fix is to build paths relative to *the file that uses them*:

```python
# utils/data_loader.py
import json
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent
DATA_DIR = PROJECT_ROOT / "data"


def load_json(filename: str):
    path = DATA_DIR / filename
    with path.open(encoding="utf-8") as f:
        return json.load(f)
```

Line by line:

- `__file__` is a built-in variable containing the path of the current Python file (`utils/data_loader.py`).
- `Path(__file__).resolve()` converts to an absolute path with symbolic links resolved.
- `.parent` gives the containing folder (`utils/`); `.parent.parent` goes up one more (project root).
- `PROJECT_ROOT / "data"` uses the `/` operator for joining paths (works on Windows and Linux).
- `path.open(encoding="utf-8")` is the `Path` equivalent of `open(path, ...)`.
- The function returns the parsed Python object. We keep it generic: callers decide what to do with the structure.

Calling `load_json("login_data.json")` now works regardless of the directory pytest was started from.

### 5. `pytest.mark.parametrize`: the engine of data-driven tests

`@pytest.mark.parametrize(argnames, argvalues)` tells pytest: "run this test once per row of `argvalues`, passing the row's values as arguments named `argnames`".

```python
import pytest

@pytest.mark.parametrize("a, b, expected", [(1, 2, 3), (2, 3, 5), (10, 5, 15)])
def test_add(a, b, expected):
    assert a + b == expected
```

- The first argument is a string of **comma-separated parameter names** (it can also be a list: `["a", "b", "expected"]`).
- The second is a **list of tuples** (or lists), one per test case, each with values in the same order as the names.
- pytest creates three tests: `test_add[1-2-3]`, `test_add[2-3-5]`, `test_add[10-5-15]`. Each passes or fails independently.

**Readable test ids.** The auto-generated ids are fine for numbers but awful for long strings. Provide your own with `ids=`:

```python
@pytest.mark.parametrize(
    "username, password, expected",
    [("locked_out_user", "secret_sauce", "locked out"),
     ("standard_user", "bad", "do not match")],
    ids=["locked-out-user", "wrong-password"],
)
def test_invalid_login(login_page, username, password, expected):
    ...
```

Reports now show `test_invalid_login[locked-out-user]` which is self-explanatory. `ids` may also be a **function** that receives each value and returns a string.

**Per-case marks with `pytest.param`.** To skip or expect failure for one row only:

```python
@pytest.mark.parametrize(
    "username",
    [
        "standard_user",
        pytest.param("problem_user", marks=pytest.mark.xfail(reason="BUG-123 broken images")),
        pytest.param("performance_glitch_user", marks=pytest.mark.slow, id="slow-user"),
    ],
)
def test_login_works(login_page, username):
    ...
```

- `pytest.param(value, marks=..., id=...)` wraps a row to attach marks or a custom id.
- `xfail` means "expected to fail": if it fails, the result is `xfailed` (not a failure); if it unexpectedly passes, it is `xpassed`, flagging that the bug may have been fixed.

**Stacking decorators = cross product.**

```python
@pytest.mark.parametrize("sort_value", ["az", "za", "lohi", "hilo"])
@pytest.mark.parametrize("user", ["standard_user", "problem_user"])
def test_sort_for_each_user(sort_value, user): ...
```

Stacking two `parametrize` decorators generates all combinations (4 x 2 = 8 tests). Use it when combinations genuinely matter; otherwise the number of tests explodes.

### 6. Combining JSON and `parametrize`

Two steps: load the JSON, convert to the form `parametrize` expects.

```python
# tests/test_login_data_driven.py
import pytest

from utils.data_loader import load_json

LOGIN_DATA = load_json("login_data.json")
INVALID_LOGINS = LOGIN_DATA["invalid_logins"]


@pytest.mark.parametrize(
    "case",
    INVALID_LOGINS,
    ids=[case["id"] for case in INVALID_LOGINS],
)
def test_invalid_login_shows_error(login_page, case):
    login_page.login_as(case["username"], case["password"])
    assert login_page.get_error_message() == case["expected_error"]
```

Line by line:

- `LOGIN_DATA = load_json("login_data.json")` runs at **import time**, when pytest collects tests. That is required because `parametrize` needs its data *before* tests run.
- `INVALID_LOGINS = LOGIN_DATA["invalid_logins"]` picks the array of case objects (a list of dicts).
- `"case"` is a single parameter name. Each row is one whole dictionary, so the test receives `case` as a `dict`. This is convenient when objects have many fields.
- `ids=[case["id"] for case in INVALID_LOGINS]` is a **list comprehension** building a list of ids from the `id` field of each case. Reports read `test_invalid_login_shows_error[locked-out-user]`.
- `login_page` is the POM fixture from the previous lessons.
- The test body is two lines; the data carries the variation.

Run it with `pytest tests/test_login_data_driven.py -v` and you see four results for four JSON entries. Add a fifth object to the JSON and you get a fifth test without touching Python.

### 7. A helper that turns JSON into `parametrize` arguments

If you parametrise often, wrap the pattern:

```python
# utils/data_loader.py (continued)
import pytest


def cases_from_json(filename: str, key: str | None = None):
    """Return (params, ids) ready for pytest.mark.parametrize.

    Each JSON item must be an object; if it has an "id" field, it is used as the test id.
    Optionally, an item may include "xfail": "reason" or "skip": "reason".
    """
    data = load_json(filename)
    items = data[key] if key else data
    params, ids = [], []
    for index, item in enumerate(items):
        marks = []
        if "skip" in item:
            marks.append(pytest.mark.skip(reason=item["skip"]))
        if "xfail" in item:
            marks.append(pytest.mark.xfail(reason=item["xfail"]))
        params.append(pytest.param(item, marks=marks))
        ids.append(item.get("id", f"case-{index}"))
    return params, ids
```

Usage:

```python
from utils.data_loader import cases_from_json

params, ids = cases_from_json("login_data.json", "invalid_logins")

@pytest.mark.parametrize("case", params, ids=ids)
def test_invalid_login_shows_error(login_page, case):
    ...
```

Line by line:

- `key: str | None = None` is a type hint meaning "a string or `None`, defaulting to `None`" (Python 3.10+; use `Optional[str]` on older versions).
- `data[key] if key else data` is a conditional expression: use the sub-list if a key is given, else the whole data.
- `params, ids = [], []` creates two empty lists in one line.
- `enumerate(items)` yields `(index, item)` pairs; the index is used for a fallback id.
- `"skip" in item` checks whether the dictionary contains that key. This lets data authors mark a case as skipped or expected-to-fail *in the JSON itself*: `{"id": "problem-user", "xfail": "BUG-123", ...}`.
- `pytest.param(item, marks=marks)` wraps the data with its marks; pytest accepts an empty `marks` list.
- `item.get("id", f"case-{index}")` returns the id or the fallback; `.get()` never raises `KeyError`.

This small utility is the kind of reusable framework piece that impresses reviewers.

### 8. Loading data through fixtures

Sometimes you do not want to *parametrise* a test; you want to hand it data as a dependency. A fixture works nicely:

```python
# conftest.py
import pytest

from utils.data_loader import load_json


@pytest.fixture(scope="session")
def users():
    return load_json("users.json")


@pytest.fixture(scope="session")
def checkout_info():
    return load_json("checkout_data.json")["valid"]
```

```python
def test_complete_purchase(inventory_page, checkout_info):
    ...
```

- `scope="session"` loads each file **once** per run; the data is read-only, so sharing is safe.
- Treat loaded data as **read-only**. If a test mutates the dict (for example, `checkout_info["first_name"] = "x"`), later tests see the change. When in doubt return a copy: `copy.deepcopy(data)`.

You can also use a fixture with `params`:

```python
@pytest.fixture(params=load_json("login_data.json")["valid_users"], ids=lambda u: u["username"])
def valid_user(request):
    return request.param
```

- `ids=lambda u: u["username"]` produces test ids from each value.
- Every test that requests `valid_user` runs once per user, a powerful way to run *many* tests against *each* user type.

### 9. `indirect` parametrisation: data into fixtures

Suppose each case is a user name and you want a fixture to log that user in and return the inventory page. With `indirect=True`, the parametrised value is passed to the **fixture** (via `request.param`) rather than directly to the test:

```python
@pytest.fixture
def inventory_for(login_page, request):
    credentials = request.param            # {"username": ..., "password": ...}
    return login_page.login_successfully(credentials["username"], credentials["password"])


@pytest.mark.parametrize(
    "inventory_for",
    LOGIN_DATA["valid_users"],
    indirect=True,
    ids=lambda u: u["username"],
)
def test_all_valid_users_see_six_products(inventory_for):
    assert inventory_for.product_count() == 6
```

- The parameter name in the decorator (`"inventory_for"`) matches the **fixture** name.
- `indirect=True` redirects values to that fixture's `request.param`.
- The test receives the fixture's *return value* (an `InventoryPage`), not the raw dictionary.
- Use `indirect` when setup must happen between data and test: logging in, creating records, opening pages.

### 10. `pytest_generate_tests`: parametrise dynamically

For large frameworks, a hook can generate parameters based on fixture names, keeping decorators out of tests:

```python
# conftest.py
from utils.data_loader import load_json


def pytest_generate_tests(metafunc):
    if "product" in metafunc.fixturenames:
        products = load_json("products.json")
        metafunc.parametrize("product", products, ids=[p["name"] for p in products])
```

- `metafunc` describes a test function during collection.
- `metafunc.fixturenames` lists names of arguments/fixtures the test uses.
- Any test with an argument called `product` automatically runs once per product in `products.json`. This is neat but "magical"; document it in your README so teammates are not surprised.

### 11. Designing good test-data files

A data file is a **contract** between the people writing cases and the test code. Good ones follow rules:

1. **One file per concern**: `login_data.json`, `checkout_data.json`, `products.json`. Avoid one giant file.
2. **Meaningful ids** on every case, because they become test names in reports.
3. **Put expected results with the inputs.** The case describes input *and* expectation, which makes the test body generic.
4. **Include negative and boundary cases** (empty strings, very long strings, special characters, unicode) as well as the happy path.
5. **Keep logic out of data.** If you find yourself encoding `"if": ...` conditions in JSON, write separate tests instead.
6. **Never store real secrets.** SauceDemo's credentials are public demo values, which is why they appear here. For a real system, read secrets from environment variables (`os.environ["APP_PASSWORD"]`) or a secrets manager, and keep only non-sensitive identifiers (like role names) in JSON.
7. **Use environment-specific files** when needed: `data/staging/users.json`, `data/demo/users.json`, selected by the `--env` option (hooks lesson).
8. **Version the data with the code** (Git). Data and tests change together.
9. **Validate the data early.** A typo such as `"expected_eror"` should fail loudly with a clear message, not as a mysterious `KeyError` mid-run:

```python
REQUIRED = {"id", "username", "password", "expected_error"}

for case in INVALID_LOGINS:
    missing = REQUIRED - case.keys()
    assert not missing, f"Case {case.get('id')} is missing fields: {missing}"
```

`REQUIRED - case.keys()` is **set difference**: fields required but not present.

### 12. Typed data with `dataclasses` (optional polish)

A dictionary access like `case["username"]` is easy to mistype. A dataclass gives names and editor autocomplete:

```python
from dataclasses import dataclass


@dataclass(frozen=True)
class LoginCase:
    id: str
    username: str
    password: str
    expected_error: str


def load_login_cases() -> list[LoginCase]:
    raw = load_json("login_data.json")["invalid_logins"]
    return [LoginCase(**item) for item in raw]
```

- `@dataclass` auto-generates `__init__`, `__repr__` and equality from the annotated fields.
- `frozen=True` makes instances immutable, preventing accidental mutation.
- `LoginCase(**item)` unpacks the dict into keyword arguments; if the JSON has an unexpected or missing field Python raises `TypeError` immediately, which doubles as validation.

Then the test uses `case.username` rather than `case["username"]`.

---

## Code Examples

### Example A: Complete data-driven login suite (POM + JSON)

**`data/login_data.json`** (as in Section 2)

**`tests/test_login_data_driven.py`**

```python
import pytest
from playwright.sync_api import expect

from utils.data_loader import cases_from_json, load_json

INVALID_PARAMS, INVALID_IDS = cases_from_json("login_data.json", "invalid_logins")
VALID_USERS = load_json("login_data.json")["valid_users"]


@pytest.mark.parametrize("case", INVALID_PARAMS, ids=INVALID_IDS)
def test_invalid_login_shows_error(login_page, case):
    login_page.login_as(case["username"], case["password"])
    expect(login_page.error_message).to_have_text(case["expected_error"])


@pytest.mark.parametrize("user", VALID_USERS, ids=[u["username"] for u in VALID_USERS])
def test_valid_users_reach_inventory(login_page, user):
    inventory = login_page.login_successfully(user["username"], user["password"])
    assert inventory.product_count() == 6
```

Walkthrough:

- Two loads happen once at import time.
- In the first test, we use `expect(locator).to_have_text(...)` (web-first, retries) rather than reading text and comparing, which protects against timing issues.
- The second test confirms that every valid user type reaches an inventory of six products. `login_successfully` includes the readiness check from the POM lessons.

### Example B: Data-driven checkout validation

**`data/checkout_data.json`**

```json
{
  "valid": { "first_name": "Asha", "last_name": "Patel", "postal_code": "560001" },
  "invalid": [
    { "id": "missing-first-name",  "first_name": "",     "last_name": "Patel", "postal_code": "560001", "expected_error": "Error: First Name is required" },
    { "id": "missing-last-name",   "first_name": "Asha", "last_name": "",      "postal_code": "560001", "expected_error": "Error: Last Name is required" },
    { "id": "missing-postal-code", "first_name": "Asha", "last_name": "Patel", "postal_code": "",       "expected_error": "Error: Postal Code is required" }
  ]
}
```

**`tests/test_checkout_data_driven.py`**

```python
import pytest
from playwright.sync_api import expect

from utils.data_loader import cases_from_json

PARAMS, IDS = cases_from_json("checkout_data.json", "invalid")


@pytest.fixture
def checkout_info_page(inventory_page):
    return (
        inventory_page.add_product_to_cart("Sauce Labs Backpack")
        .open_cart()
        .proceed_to_checkout()
    )


@pytest.mark.parametrize("case", PARAMS, ids=IDS)
def test_checkout_validation(checkout_info_page, case):
    checkout_info_page.fill_details(case["first_name"], case["last_name"], case["postal_code"])
    checkout_info_page.continue_expecting_error()
    expect(checkout_info_page.error_message).to_have_text(case["expected_error"])
```

Explanation: three data rows produce three tests. Each starts from a fresh `checkout_info_page` (function-scoped fixture chain), so tests do not influence each other. Note that `fill("")` with an empty string simply clears the field, which is what we want for "missing".

### Example C: Data-driven sorting with expected order

**`data/sort_data.json`**

```json
[
  { "id": "name-a-to-z",   "option": "az",   "check": "names_ascending" },
  { "id": "name-z-to-a",   "option": "za",   "check": "names_descending" },
  { "id": "price-low-high","option": "lohi", "check": "prices_ascending" },
  { "id": "price-high-low","option": "hilo", "check": "prices_descending" }
]
```

```python
import pytest

from utils.data_loader import cases_from_json

PARAMS, IDS = cases_from_json("sort_data.json")


@pytest.mark.parametrize("case", PARAMS, ids=IDS)
def test_sorting(inventory_page, case):
    inventory_page.sort_by(case["option"])

    names = inventory_page.items.get_by_test_id("inventory-item-name").all_inner_texts()
    prices = inventory_page.get_prices()

    expectations = {
        "names_ascending":   names == sorted(names),
        "names_descending":  names == sorted(names, reverse=True),
        "prices_ascending":  prices == sorted(prices),
        "prices_descending": prices == sorted(prices, reverse=True),
    }
    assert expectations[case["check"]], f"{case['check']} failed; names={names}, prices={prices}"
```

Explanation:

- The JSON names the *check*, and the test maps names to boolean results via a dictionary. (Keep such mapping tiny; if checks diverge a lot, use separate tests.)
- The `assert` message (after the comma) prints the actual data on failure, saving debugging time.
- Note one subtlety: all four comparisons are evaluated every time, which is cheap. If a check were expensive, build a dictionary of lambdas and call only the one needed.

### Example D: Multiple data dimensions with a fixture

```python
@pytest.fixture(params=load_json("login_data.json")["valid_users"], ids=lambda u: u["username"])
def valid_user(request):
    return request.param


def test_add_to_cart_for_every_user(login_page, valid_user):
    inventory = login_page.login_successfully(valid_user["username"], valid_user["password"])
    inventory.add_product_to_cart("Sauce Labs Backpack")
    assert inventory.header.cart_count() == 1
```

Interesting detail: `problem_user` on the demo site has intentional UI bugs, so this test may fail for that user. That is *useful*: the data-driven approach pinpoints exactly which user type fails (`test_add_to_cart_for_every_user[problem_user]`). In a real team you would then mark that row `xfail` with the defect id until it is fixed.

---

## Real-World Scenarios

**Scenario 1: Form validation matrix.** A bank's account-opening form has 12 fields with rules (length, format, required). A QE builds a JSON file listing each field's valid and invalid values with the expected message. One generic test fills the field, submits, and checks the message. A requirement change for one rule is a one-line data edit.

**Scenario 2: Localisation.** The same checkout flow must be validated in six languages. A JSON file holds the expected headings per locale. The test sets the locale in the browser context (`browser_context_args`) and compares the visible text with the file's value.

**Scenario 3: Business-analyst contributions.** An analyst who does not write Python adds rows to `discount_cases.json` (cart total, coupon code, expected discount). Because JSON is human-readable and the test ids come from an `id` field, review in pull requests is easy.

**Scenario 4: Cross-user smoke test.** A smoke test runs the "login and view products" path for every role defined in `roles.json` (customer, admin, auditor), catching permission regressions fast.

**Scenario 5: Defect tracking.** When a defect is raised for one data row, the team adds `"xfail": "BUG-481"` to that row's JSON. The suite stays green but still tracks the defect, and when the defect is fixed the test reports `XPASS`, a signal to remove the marker.

---

## Common Pitfalls and Best Practices

**Pitfalls**

1. **Invalid JSON** (trailing comma, single quotes, comments). Validate with `python -m json.tool file.json`.
2. **Relative paths that break** when the working directory changes. Build paths from `__file__` with `pathlib`.
3. **Forgetting the encoding** (`encoding="utf-8"`), causing surprises with non-ASCII characters on Windows.
4. **Unreadable ids.** Without `ids=`, a dictionary case appears as `case0`, `case1`, which tells nobody anything.
5. **Duplicate ids.** pytest will add suffixes (`-0`, `-1`) but confusing duplicates indicate a data problem; keep ids unique.
6. **Mutating shared data** in a test (especially session-scoped data). Copy before modifying.
7. **Logic in data.** A JSON field named `"steps": ["click login", "click cart"]` that your test interprets is a mini programming language; avoid it (that is what code is for).
8. **Combinatorial explosion** from stacked `parametrize` decorators. 5 x 5 x 5 x 5 = 625 browser tests will make your CI crawl. Use pairwise/selected combinations.
9. **Over-parametrising UI tests.** Each row is a full browser test, which is far slower than a unit test. For pure validation logic that does not need a browser, test lower in the stack (the testing pyramid).
10. **Parametrising at import time with side effects.** Loading a file at import is fine; calling a network API at import time slows collection and makes it fragile.
11. **Storing real passwords** in the repository. Use environment variables or a secrets manager.
12. **Expected values copied from the application's output** instead of from requirements. A test whose expectation was generated by the application can never find a bug in that output.
13. **Misordered `parametrize` arguments**: `"username, password"` with tuples written `(password, username)`. Named dictionary cases avoid this class of bug.

**Best practices**

- Use dictionaries with named fields instead of long positional tuples.
- Give every case an `id`, and make it describe the **scenario** (`empty-username`), not the position (`case-3`).
- Keep **one assertion theme per test**: a test about error messages should not also check sorting.
- Put shared loading code in `utils/data_loader.py`; keep tests short.
- Document the data schema (fields, meanings) in your README or the file header (as a `"description"` property).
- Review data in pull requests with the same rigour as code.
- Use `pytest --collect-only -q` to see the generated test ids before running anything.
- Run a single case with `pytest -k "empty-username"` or by node id: `pytest "tests/test_login_data_driven.py::test_invalid_login_shows_error[empty-username]"`.

---

## Mini Practice Exercises

**Exercise 1: JSON syntax doctor.**
The following file has five errors. Find and fix them:
```json
{
  'users': [
    {username: "standard_user", "password": "secret_sauce",},
    {"username": "locked_out_user" "password": "secret_sauce"}
  ],  // test users
  "active": True
}
```
*Answer:* single quotes around `users`; unquoted key `username`; trailing comma after the password; missing comma between the two fields of the second object; the comment; `True` must be `true`. (Six issues; the comment and the single quotes count as one each.)

**Exercise 2: first parametrised test.**
Write a parametrised test `test_title_length` with `("Products", 8)`, `("Cart", 4)` rows that asserts `len(text) == expected`. Run with `-v` and read the ids. Then add custom ids.

**Exercise 3: build `users.json`.**
Create `data/users.json` with the four SauceDemo user types and a `"expected_outcome"` field (`"success"`, `"locked_out"`). Write one test that logs in each user and asserts the right outcome.
*Hint:* parametrise on the whole dict; branch the assertion using a small mapping, or split into two data lists (preferred) and two tests.

**Exercise 4: validation.**
Add a loop (or a pytest session fixture) that fails collection with a clear message if any case lacks `id` or `expected_error`.

**Exercise 5: xfail from data.**
Add `"xfail": "BUG-1 demo defect"` to one case in a JSON file and use `cases_from_json` to apply it. Run the suite and read the summary line (`1 xfailed`). Remove the marker and observe.

**Exercise 6: indirect.**
Rewrite Example D using `indirect=True` so that the test receives an `InventoryPage` directly for each user.

**Exercise 7 (Project 1 link):** Identify at least three UI tests in Project 1 whose bodies differ only in input values. Merge each group into a single parametrised test driven by a JSON file in `data/`. Record how many lines you removed and how many test cases you gained.

---

## Summary / Key Takeaways

- **Data-driven testing** runs one test body against many data rows; the data lives outside the code.
- **JSON** supports objects, arrays, strings, numbers, booleans, and `null`. Watch for trailing commas, single quotes, and comments, none of which are allowed.
- Python's **`json` module** reads with `json.load` (file) / `json.loads` (string) and writes with `json.dump` / `json.dumps`. Build file paths with **`pathlib`** relative to `__file__`.
- **`@pytest.mark.parametrize`** generates one test per row; use `ids` for readable names and `pytest.param(..., marks=...)` for per-row `skip`/`xfail`.
- Wrap loading in a reusable **data-loader utility**; use fixtures for shared read-only data, `indirect` for data passed into fixtures, and `pytest_generate_tests` for dynamic parametrisation.
- Good data files have **meaningful ids, expected results with the inputs, negative cases, no secrets, and no embedded logic**.
- Combine DDT with POM: page objects do the actions, JSON supplies the scenarios, tests assert.
- Keep UI parametrisation proportionate: each row costs a browser test.

---

## External Resources

- pytest documentation, "How to parametrize fixtures and test functions": https://docs.pytest.org/en/stable/how-to/parametrize.html
- Python documentation, `json` module: https://docs.python.org/3/library/json.html
- Python documentation, `pathlib` module: https://docs.python.org/3/library/pathlib.html
