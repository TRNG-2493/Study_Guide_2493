# Test Organization and Reusable Templates

## Learning Objectives

By the end of this lesson you will be able to:

- Design a clear folder structure for a PyTest project that scales from 10 to 1,000 tests.
- Apply naming conventions that make tests discoverable and self-explanatory.
- Configure the project with `pytest.ini` (or `pyproject.toml`): `testpaths`, `pythonpath`, `addopts`, `markers`, `python_files`, and strict options.
- Separate unit, integration and end-to-end style tests with folders and markers.
- Structure each test using the **Arrange-Act-Assert (AAA)** pattern.
- Build reusable **test templates**: base data builders, factory fixtures, helper modules, and a starter skeleton you can copy into new projects.
- Use shared fixtures in `conftest.py` and shared helpers without circular or fragile imports.
- Decide when to group tests in classes, modules and packages.
- Recognise and avoid organizational anti-patterns (giant test files, hidden dependencies, duplicated setup).

---

## Why This Matters

The weekly epic is to take PyTest from basics to a **reporting framework** for Project 1 – QE Foundations. On Monday you learned discovery rules; on Tuesday fixtures and `conftest.py`; earlier today you saw data-driven tests and custom assertions. Today's lesson is the glue: **where do all of these pieces live, and how do we make a new test cheap to write?**

Consider two teams:

- Team A keeps 300 tests in one file named `test_stuff.py`, each test with its own copy of setup code. Adding a test takes 20 minutes because you must find where it fits and copy a similar one. A change in the login flow means editing 60 places.
- Team B has a predictable layout, shared fixtures, helper builders and a template. Adding a test takes 3 minutes, and a change to login is made once.

Both teams started with the same tools. The difference is **organization**. In industry, test code is read far more often than it is written, and it lives for years. Treating test code as "real code" with structure is a hallmark of a mature QE engineer, and it is exactly what Project 1 needs: a framework others can extend.

---

## The Concept

### 1. Principles of good test organization

1. **Predictability**: anyone can guess where a test lives.
2. **Mirror the product**: test folders reflect the application structure (or the feature structure).
3. **Isolation**: tests do not depend on each other or on execution order.
4. **DRY in setup, DAMP in tests**: avoid repeating setup (DRY: Don't Repeat Yourself), but keep each test *readable on its own* (DAMP: Descriptive And Meaningful Phrases). A test should tell its story without hunting through five files.
5. **Fast feedback**: separate fast tests from slow ones so developers can run the quick set constantly.
6. **Configuration over convention-by-memory**: write rules in `pytest.ini` so the whole team and CI behave identically.

### 2. A recommended project layout

```
project1-qe-framework/
├── pytest.ini                 # project-wide PyTest configuration
├── requirements.txt           # pytest, pytest-html, ...
├── README.md
├── src/                       # the application code under test
│   └── qe_utils/
│       ├── __init__.py
│       ├── validators.py
│       └── pricing.py
├── tests/
│   ├── conftest.py            # fixtures shared by ALL tests
│   ├── helpers/               # reusable non-test code
│   │   ├── __init__.py
│   │   ├── assertions.py      # custom assertions (see previous lesson)
│   │   ├── builders.py        # test-data builders / factories
│   │   └── data_loader.py     # JSON/CSV loading (see data-driven lesson)
│   ├── data/                  # JSON, CSV test data
│   │   ├── discount_cases.json
│   │   └── login_cases.csv
│   ├── unit/
│   │   ├── conftest.py        # fixtures only for unit tests
│   │   ├── test_validators.py
│   │   └── test_pricing.py
│   ├── integration/
│   │   ├── conftest.py
│   │   └── test_checkout_flow.py
│   └── e2e/                   # browser tests will live here later this week
│       └── conftest.py
└── reports/                   # generated output (add to .gitignore)
```

Why each part exists:

- **`src/`** separates product code from test code. (You may see projects with the package at the root; both are valid, but `src/` prevents accidentally importing the local folder instead of the installed package.)
- **`tests/`** holds everything test-related; one clear place for CI to run.
- **`conftest.py` at several levels**: fixtures are available to tests in the same folder and below. Put widely used fixtures at the top; specialised ones close to their tests (Tuesday's *conftest.py* lesson).
- **`helpers/`** is for plain Python (not tests). Its files **do not start with `test_`**, so PyTest will not try to collect them.
- **`data/`** keeps test data out of code.
- **`unit/`, `integration/`, `e2e/`** classify by scope and speed.
- **`reports/`** is where HTML reports and logs go; never commit generated files.

Do the folders need `__init__.py`? It depends on your import mode. With PyTest's default (`prepend`) import mode, two test files with the same name in different folders (for example `unit/test_login.py` and `integration/test_login.py`) cause an "import file mismatch" error **unless** the folders contain `__init__.py` files (making them packages) or filenames are unique. A common beginner-safe rule: **give every test file a unique name or add `__init__.py` files to the test folders.** PyTest also supports `--import-mode=importlib`, which avoids the problem; see the docs linked below.

### 3. Naming conventions

PyTest's default discovery rules (Monday's lesson): files `test_*.py` or `*_test.py`; functions `test_*`; classes `Test*` without an `__init__`. Build on them:

| Item | Convention | Example |
|------|-----------|---------|
| Test file | `test_<unit_or_feature>.py` | `test_pricing.py` |
| Test function | `test_<unit>_<scenario>_<expected>` | `test_apply_discount_over_100_raises_value_error` |
| Test class | `Test<Feature>` | `TestShoppingCart` |
| Fixture | noun describing what it provides | `empty_cart`, `logged_in_user` |
| Helper function | verb phrase | `build_user`, `assert_valid_email` |
| Constants | UPPER_SNAKE_CASE | `DEFAULT_TIMEOUT_MS` |
| Markers | short lowercase words | `smoke`, `regression`, `slow` |

A good test name reads like a sentence in the failure report: when the nightly run says `test_login_locked_account_shows_error FAILED`, nobody needs to open the code to know what broke.

### 4. Project configuration with `pytest.ini`

Create `pytest.ini` in the project root:

```ini
[pytest]
minversion = 8.0
testpaths = tests
pythonpath = src tests
addopts = -ra --strict-markers --strict-config
python_files = test_*.py
python_functions = test_*
markers =
    smoke: fast checks that prove the build is alive
    regression: broader checks run before a release
    slow: tests that take more than a second
    unit: isolated tests of a single unit
    integration: tests that combine several units
```

**Explanation of every line:**

- `[pytest]` is the required section header.
- `minversion = 8.0` makes PyTest abort with a clear message if someone has an older version.
- `testpaths = tests` tells PyTest where to look when you run plain `pytest` from the root, so it does not scan `src/`, `reports/`, or virtual environments.
- `pythonpath = src tests` adds those folders to Python's import path (feature available since PyTest 7). It lets tests write `from qe_utils.pricing import apply_discount` and `from helpers.assertions import assert_valid_email` without installing the package or hacking `sys.path`. Separate multiple entries with spaces or newlines.
- `addopts` lists options automatically added to every command line:
  - `-ra` prints a short summary of everything that is **not** a pass (skips, xfails, errors).
  - `--strict-markers` turns a typo such as `@pytest.mark.smoek` into an **error** instead of a quiet warning. Always enable it.
  - `--strict-config` makes unknown configuration keys an error.
- `python_files` / `python_functions` restate defaults; list them explicitly only if you need to change the naming pattern.
- `markers` registers custom markers with descriptions; `pytest --markers` lists them.

PyTest looks for configuration in this order: `pytest.ini`, `pyproject.toml`, `tox.ini`, `setup.cfg`. The first file that matches wins. The equivalent in `pyproject.toml` is:

```toml
[tool.pytest.ini_options]
minversion = "8.0"
testpaths = ["tests"]
pythonpath = ["src", "tests"]
addopts = "-ra --strict-markers --strict-config"
markers = [
    "smoke: fast checks that prove the build is alive",
    "regression: broader checks run before a release",
    "slow: tests that take more than a second",
]
```

Run `pytest --version` and look at the first lines of any run (`rootdir:`, `configfile:`) to confirm which config file PyTest is using. This is the first thing to check when "it works on my machine".

### 5. Classifying tests with folders **and** markers

Folders tell you *what level* a test is; markers tell you *why you would run it*. They are complementary:

```python
# tests/unit/test_pricing.py
import pytest
from qe_utils.pricing import apply_discount

pytestmark = pytest.mark.unit   # applies to every test in this module


@pytest.mark.smoke
def test_apply_discount_typical_value():
    assert apply_discount(100.0, 10) == 90.0


@pytest.mark.regression
@pytest.mark.parametrize("percent", [-1, 101])
def test_apply_discount_out_of_range_raises(percent):
    with pytest.raises(ValueError):
        apply_discount(100.0, percent)
```

- `pytestmark = pytest.mark.unit` is a module-level variable that PyTest reads; the marker is applied to every test in the file. Use a list to apply several: `pytestmark = [pytest.mark.unit, pytest.mark.regression]`.
- Commands:
  - `pytest tests/unit` runs a folder.
  - `pytest -m smoke` runs only smoke-marked tests across all folders.
  - `pytest -m "unit and not slow"` combines marker expressions.
  - `pytest tests/unit/test_pricing.py::test_apply_discount_typical_value` runs one test by node ID.

You can also apply markers automatically by folder using a hook in `conftest.py`, so nobody forgets:

```python
# tests/conftest.py
import pytest


def pytest_collection_modifyitems(items):
    for item in items:
        path = str(item.fspath)
        if "/unit/" in path.replace("\\", "/"):
            item.add_marker(pytest.mark.unit)
        elif "/integration/" in path.replace("\\", "/"):
            item.add_marker(pytest.mark.integration)
```

- `pytest_collection_modifyitems` is a hook that PyTest calls after collecting tests, giving you the list `items` to inspect or modify.
- `item.fspath` is the test's file path (a legacy attribute that still works; newer code may use `item.path`).
- `.replace("\\", "/")` normalises Windows paths so the check works on every operating system.

### 6. The Arrange-Act-Assert (AAA) pattern

Every test, regardless of size, should have three visible phases:

1. **Arrange**: create objects and prepare data.
2. **Act**: perform the one action under test.
3. **Assert**: verify the outcome.

```python
def test_cart_total_includes_all_items():
    # Arrange
    cart = ShoppingCart()
    cart.add("pen", price=2.50, qty=4)
    cart.add("book", price=12.00, qty=1)

    # Act
    total = cart.total()

    # Assert
    assert total == 22.00
```

Why it helps:

- A reader instantly sees what is being tested (the Act line).
- Tests that "act" many times usually test too many things; split them.
- Blank lines or comments separating the phases make long tests scannable.

Let's define a minimal `ShoppingCart` so this is runnable:

```python
# src/qe_utils/cart.py
class ShoppingCart:
    def __init__(self):
        self._items = []

    def add(self, name: str, price: float, qty: int = 1) -> None:
        if qty <= 0:
            raise ValueError("qty must be positive")
        self._items.append((name, price, qty))

    def total(self) -> float:
        return round(sum(price * qty for _, price, qty in self._items), 2)

    def count(self) -> int:
        return sum(qty for _, _, qty in self._items)
```

- `_items` with a leading underscore signals "internal use" by convention.
- `for _, price, qty in self._items` unpacks each tuple; `_` is the conventional name for a value we ignore.
- `sum(generator)` adds up the values produced by the generator expression.

### 7. Reusable template 1: test-data builders (factory functions)

Tests often need a "valid user", "valid order", etc. Instead of repeating a long dictionary, create a **builder** with sensible defaults that tests override only where it matters:

```python
# tests/helpers/builders.py
import itertools

_counter = itertools.count(1)


def build_user(**overrides):
    """Return a valid user dict. Override only the fields a test cares about."""
    n = next(_counter)
    user = {
        "id": n,
        "username": f"user{n}",
        "email": f"user{n}@example.com",
        "age": 30,
        "active": True,
    }
    user.update(overrides)
    return user
```

```python
# tests/unit/test_users.py
from helpers.builders import build_user


def test_inactive_user_flag():
    user = build_user(active=False)
    assert user["active"] is False


def test_each_user_has_unique_username():
    assert build_user()["username"] != build_user()["username"]
```

**Explanation:**

- `**overrides` collects any keyword arguments into a dict (`{"active": False}`).
- `user.update(overrides)` replaces defaults with the overrides.
- `itertools.count(1)` creates an endless counter (1, 2, 3, ...). `next()` takes the next number, guaranteeing unique usernames and avoiding collisions in tests that create many users.
- The *test* shows only the field it cares about (`active=False`). This **highlights intent** and keeps the test short. When a new required field is added to users, only the builder changes.

### 8. Reusable template 2: factory fixtures

When a builder needs cleanup or access to other fixtures, make it a **factory fixture**: a fixture that returns a function.

```python
# tests/conftest.py
import pytest
from helpers.builders import build_user


@pytest.fixture
def make_user():
    created = []

    def _make(**overrides):
        user = build_user(**overrides)
        created.append(user)
        return user

    yield _make

    # teardown: runs after the test, even if it failed
    created.clear()
```

```python
# tests/unit/test_users_factory.py
def test_two_users_are_distinct(make_user):
    first = make_user(username="ana")
    second = make_user(username="ben")
    assert first["username"] != second["username"]
```

- `make_user` returns the inner function `_make`; the test calls it as many times as needed.
- Code after `yield` is teardown; here it is a placeholder where you would delete users from a database or temp files.
- This is the pattern recommended in PyTest's documentation ("factories as fixtures").

### 9. Reusable template 3: base fixtures for common objects

```python
# tests/conftest.py (continued)
import pytest
from qe_utils.cart import ShoppingCart


@pytest.fixture
def empty_cart():
    return ShoppingCart()


@pytest.fixture
def cart_with_items(empty_cart):
    empty_cart.add("pen", 2.50, 4)
    empty_cart.add("book", 12.00, 1)
    return empty_cart
```

```python
# tests/unit/test_cart.py
def test_total_with_items(cart_with_items):
    assert cart_with_items.total() == 22.00


def test_count_with_items(cart_with_items):
    assert cart_with_items.count() == 5


def test_new_cart_is_empty(empty_cart):
    assert empty_cart.total() == 0
    assert empty_cart.count() == 0
```

`cart_with_items` *depends on* `empty_cart` by listing it as a parameter. PyTest builds the chain automatically. Because both are function-scoped, every test gets a **fresh** cart: no leaking state.

### 10. Organizing with classes

Classes group related tests under one name and allow shared fixtures/marker application:

```python
import pytest
from qe_utils.cart import ShoppingCart


@pytest.mark.unit
class TestShoppingCartAdd:
    def test_add_increases_count(self, empty_cart):
        empty_cart.add("pen", 1.0, 3)
        assert empty_cart.count() == 3

    def test_add_zero_qty_raises(self, empty_cart):
        with pytest.raises(ValueError, match="qty"):
            empty_cart.add("pen", 1.0, 0)


@pytest.mark.unit
class TestShoppingCartTotal:
    def test_total_rounds_to_cents(self, empty_cart):
        empty_cart.add("x", 0.1, 3)
        assert empty_cart.total() == 0.3
```

Guidelines:

- The class has no `__init__`, and its name starts with `Test`.
- Each test gets a **new instance** of the class, so instance attributes do not carry over (never rely on sharing state through `self`).
- Use classes when tests share a theme or markers; otherwise plain functions in a well-named module are simpler.
- Name classes after a *behaviour group* (`TestShoppingCartAdd`), not after "TestStuff".

### 11. A starter template you can copy for every new feature

Keep a file `tests/_template_test.py.txt` (with a non-`.py` extension so it is not collected) as your team's boilerplate:

```python
"""Tests for <FEATURE>.

Covers:
    - happy path
    - boundaries
    - invalid input
"""
import pytest

# from qe_utils.<module> import <function>
# from helpers.builders import build_user
# from helpers.assertions import assert_valid_email

pytestmark = pytest.mark.unit


# ---------- Happy path ----------
@pytest.mark.smoke
def test_<unit>_<scenario>_<expected>():
    # Arrange

    # Act

    # Assert
    ...


# ---------- Boundaries / data-driven ----------
@pytest.mark.parametrize(
    "value, expected",
    [
        pytest.param(0, ..., id="lower-bound"),
        pytest.param(1, ..., id="just-above-lower"),
    ],
)
def test_<unit>_boundaries(value, expected):
    ...


# ---------- Invalid input ----------
def test_<unit>_invalid_input_raises():
    with pytest.raises(ValueError, match="..."):
        ...
```

(The angle-bracket placeholders deliberately make this file invalid Python until filled in, which is another reason it is saved with a `.txt` extension.)

### 12. Keeping helper imports healthy

- Put helpers in `tests/helpers/` and add `tests` to `pythonpath` in `pytest.ini` so imports are `from helpers.x import y` everywhere.
- **Never** import one test file from another test file. Share code via helpers or fixtures.
- Avoid importing from `conftest.py` in tests; fixtures are injected by name, not imported.
- Avoid circular imports: helpers must not import tests; `conftest.py` may import helpers.
- Use `pytest.register_assert_rewrite("helpers.assertions")` at the top of the root `conftest.py` if you want rich assertion introspection inside helpers (see *Custom assertions*).

### 13. Controlling what runs and in what order

- **Fast first:** `pytest -m "not slow"` for developers; the full suite on CI.
- **Fail fast:** `pytest -x` stops after the first failure; `--maxfail=3` stops after three.
- **Last failed:** `pytest --lf` re-runs only tests that failed last time; `--ff` runs failures first.
- **Do not depend on order.** If your tests only pass in a particular order they are coupled, and parallel running or reordering will expose it. Fix the coupling with fixtures.

### 14. Documenting the framework

A short `README.md` at the root saves hours for new teammates: how to install (`pip install -r requirements.txt`), how to run (`pytest`, `pytest -m smoke`), how to add a test (point to the template), how to view reports (covered in the next lesson, *HTML reporting*), and the naming/marker conventions.

---

## Real-World Scenarios

1. **Onboarding a new tester.** The new hire copies the template, fills in three sections and has a passing test on day one because fixtures, data loaders and assertions already exist.
2. **Release gate.** The pipeline runs `pytest -m smoke` on every commit (30 seconds) and `pytest -m "regression"` nightly (20 minutes). Because markers are registered and strict, a mistyped marker fails the build instead of silently excluding tests.
3. **Refactoring the product.** The login API adds a mandatory `tenant` field. Only `build_user` needs a new default; 200 tests keep working.
4. **UI layer later this week.** When browser tests arrive, they will live in `tests/e2e/` with their own `conftest.py`; we will cover browser automation in depth on Thursday and Friday.

---

## Common Mistakes

| Mistake | Consequence | Fix |
|---------|-------------|-----|
| One giant test file | Hard to navigate; merge conflicts | One module per unit/feature |
| Duplicate `test_login.py` in two folders without `__init__.py` | "import file mismatch" error | Unique names, `__init__.py`, or `--import-mode=importlib` |
| Helpers named `test_*.py` | PyTest tries to collect them | Name them without `test_` prefix |
| Custom markers not registered | Warnings (or errors with `--strict-markers`) | Register in `pytest.ini` |
| Hard-coded absolute paths (`C:\Users\...`) | Fails on other machines/CI | `Path(__file__).parent`, `pytest.ini` `pythonpath` |
| Fixtures holding mutable shared state at wide scope | Tests interfere with each other | Function scope, or factories that create fresh objects |
| Tests that import from other tests | Hidden coupling | Move shared code to helpers/fixtures |
| Over-abstracting (every line hidden in helpers) | Tests unreadable | Keep the Act and Assert lines visible in the test |
| Committing `reports/` and `.pytest_cache/` | Noise in git | Add to `.gitignore` |
| Running from different folders and getting different results | Config not found | Keep `pytest.ini` in the root and run from there |

---

## Practice Exercises

### Exercise 1: Build the skeleton

Create the folder structure from section 2 for a mini project called `qe_utils` with one module, `validators.py`, containing `is_valid_age(age)` (valid 0-120) and `is_valid_username(name)` (3-20 characters, letters/digits/underscore only). Create `pytest.ini` with `testpaths`, `pythonpath`, `addopts` and three registered markers. Confirm that `pytest` run from the root and `pytest` run from inside `tests/unit` both find the tests.

<details>
<summary>Hint</summary>
`rootdir` and `configfile` in the first lines of output prove which `pytest.ini` was used. PyTest searches upward from the current directory for the config file.
</details>

### Exercise 2: Strict markers

Add `--strict-markers` to `addopts`. Then deliberately write `@pytest.mark.smoek` in a test and run PyTest. Read the error. Fix the typo.

### Exercise 3: A builder

Write `build_order(**overrides)` in `helpers/builders.py` returning a dict with `order_id`, `customer`, `items` (a list of one item dict), and `status="NEW"`. Use it in two tests: one overriding `status`, one overriding `items` with an empty list.

<details>
<summary>Solution sketch</summary>

```python
import itertools

_ids = itertools.count(1000)


def build_order(**overrides):
    order = {
        "order_id": next(_ids),
        "customer": "alice",
        "items": [{"sku": "PEN-1", "qty": 1, "price": 2.5}],
        "status": "NEW",
    }
    order.update(overrides)
    return order
```
</details>

### Exercise 4: AAA refactor

Rewrite this test so that it follows AAA, uses a fixture and has a descriptive name:

```python
def test1():
    c = ShoppingCart()
    c.add("a", 1.0, 2)
    c.add("b", 3.0, 1)
    assert c.total() == 5.0
    assert c.count() == 3
    c.add("c", 0, 0)
```

<details>
<summary>Answer</summary>
Three problems: poor name, two behaviours (total and count) in one test, and a final line that would raise `ValueError` and is not asserted. Use a `cart_with_items`-style fixture, split `total` and `count` into two tests, and test the zero-quantity error separately with `pytest.raises`.
</details>

### Exercise 5: Auto-marking

Using `pytest_collection_modifyitems`, automatically add the `slow` marker to any test whose name ends with `_slow`. Verify with `pytest -m slow --collect-only -q`.

<details>
<summary>Hint</summary>
Inside the loop use `if item.name.endswith("_slow"): item.add_marker(pytest.mark.slow)`.
</details>

### Exercise 6: Project 1 framework layout

Take your Project 1 tests from Monday and Tuesday and reorganize them into the recommended layout. Move shared data into `tests/data`, shared fixtures into `tests/conftest.py`, and create a README with a "How to add a test" section. Run the full suite before and after the move; the number of passed tests must not change.

---

## Summary

- Organized tests are predictable, isolated and fast to extend; organization is a feature of the framework.
- Use a clear layout (`src/`, `tests/unit|integration|e2e`, `helpers/`, `data/`, `reports/`) and consistent naming that makes reports read like sentences.
- Centralise configuration in `pytest.ini`: `testpaths`, `pythonpath`, `addopts` (`-ra --strict-markers`), registered markers.
- Combine folders (level) with markers (purpose); use `pytestmark` and hooks to apply them consistently.
- Write every test in Arrange-Act-Assert form with one Act.
- Reuse through builders, factory fixtures and base fixtures; keep tests readable (DAMP) while keeping setup DRY.
- Never import tests from tests; share through helpers and fixtures.
- Keep a template and a README so new tests are cheap to write.

---

## Additional Resources

- PyTest documentation - Good Integration Practices: https://docs.pytest.org/en/stable/explanation/goodpractices.html
- PyTest documentation - Configuration files (`pytest.ini`, `pyproject.toml`): https://docs.pytest.org/en/stable/reference/customize.html
- PyTest documentation - Fixtures, including factories as fixtures: https://docs.pytest.org/en/stable/how-to/fixtures.html
