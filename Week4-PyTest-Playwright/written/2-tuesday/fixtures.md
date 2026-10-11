# Fixtures in PyTest

## Learning Objectives

By the end of this lesson you will be able to:

- Explain what a fixture is and which problem it solves in test automation.
- Create a fixture with the `@pytest.fixture` decorator and request it by naming it as a test-function argument.
- Use `yield` to write fixtures that perform setup before a test and teardown (cleanup) after it.
- Build fixtures that depend on other fixtures, and understand the order PyTest resolves them in.
- Use built-in fixtures such as `tmp_path` and `capsys`, and the `request` fixture for introspection.
- Use `autouse=True`, fixture `params`, and the `name=` argument appropriately.
- Recognise and avoid the most common beginner mistakes with fixtures.

## Why This Matters

This week's epic is to turn manual test design into automation: PyTest from basics to a reporting framework, then CSS/XPath locators and Playwright. On Monday you learned to write test functions, assertions, and markers. Those skills are enough to write tests, but not enough to write **good, maintainable** tests at scale.

Think about **Project 1 (QE Foundations)**. Your utility tests probably all need the same things: a sample user, a sample shopping cart, a temporary file, a configured object. Without fixtures you copy and paste that setup code into every test. When the setup changes, you must edit every test. When a test fails halfway, the cleanup code at the bottom of the test never runs, leaving garbage behind that breaks later tests.

Fixtures solve all of this. They are the single most important feature of PyTest, and on Friday you will see that Playwright's PyTest plugin gives you a browser `page` object **as a fixture**. If you understand fixtures now, Playwright will feel natural later. (We will cover Playwright in depth on Thursday and Friday.)

## The Concept

### 1. The problem: repeated setup and forgotten cleanup

Imagine we are testing a tiny `ShoppingCart` class. Here is the code under test, saved as `cart.py`:

```python
# cart.py
class ShoppingCart:
    def __init__(self):
        self.items = {}          # maps product name -> (price, quantity)

    def add(self, name, price, quantity=1):
        if price < 0:
            raise ValueError("price cannot be negative")
        if quantity <= 0:
            raise ValueError("quantity must be positive")
        if name in self.items:
            old_price, old_qty = self.items[name]
            self.items[name] = (old_price, old_qty + quantity)
        else:
            self.items[name] = (price, quantity)

    def remove(self, name):
        del self.items[name]     # raises KeyError if missing

    def total(self):
        return sum(price * qty for price, qty in self.items.values())

    def count(self):
        return sum(qty for _, qty in self.items.values())
```

Without fixtures, tests look like this:

```python
# test_cart_no_fixtures.py
from cart import ShoppingCart

def test_total_with_two_items():
    cart = ShoppingCart()
    cart.add("pen", 2.0, 3)
    cart.add("book", 10.0)
    assert cart.total() == 16.0

def test_count_with_two_items():
    cart = ShoppingCart()
    cart.add("pen", 2.0, 3)
    cart.add("book", 10.0)
    assert cart.count() == 4
```

The first three lines of each test are identical. This violates the **DRY principle** (Don't Repeat Yourself). If `ShoppingCart()` later needs a constructor argument, you edit every test.

### 2. What is a fixture?

A **fixture** is a function that PyTest runs for you to **prepare something a test needs** (the *arrange* step) and, optionally, to **clean up afterwards**. The thing it prepares is handed to the test.

A real-world analogy: before a chef cooks (the test), a kitchen assistant lays out the ingredients (the fixture's setup) and afterwards washes the dishes (the fixture's teardown). The chef never has to think about either.

Key vocabulary:

| Term | Meaning |
|------|---------|
| **Fixture function** | A function decorated with `@pytest.fixture`. |
| **Setup** | Code in the fixture that runs *before* the test. |
| **Teardown / finalizer** | Code that runs *after* the test, even if the test failed. |
| **Requesting a fixture** | Adding the fixture's name as a parameter of a test (or of another fixture). |
| **Injection** | PyTest automatically calling the fixture and passing its return value. This is also called *dependency injection*. |

### 3. Your first fixture

```python
# test_cart_fixtures.py
import pytest
from cart import ShoppingCart

@pytest.fixture
def empty_cart():
    return ShoppingCart()

@pytest.fixture
def filled_cart():
    cart = ShoppingCart()
    cart.add("pen", 2.0, 3)
    cart.add("book", 10.0)
    return cart

def test_new_cart_is_empty(empty_cart):
    assert empty_cart.count() == 0
    assert empty_cart.total() == 0

def test_total(filled_cart):
    assert filled_cart.total() == 16.0

def test_count(filled_cart):
    assert filled_cart.count() == 4
```

**Line-by-line explanation**

- `import pytest` - we need the `pytest` module for the `fixture` decorator.
- `@pytest.fixture` - a **decorator**. A decorator is a function that wraps another function to add behaviour. Here it tells PyTest "this function is not a test, it is a fixture provider".
- `def empty_cart():` - the fixture's **name** is the function name. Tests use this name to request it.
- `return ShoppingCart()` - whatever the fixture returns is the value injected into the test.
- `def test_new_cart_is_empty(empty_cart):` - the parameter name `empty_cart` matches the fixture name. PyTest sees the parameter, finds a fixture with that name, runs it, and passes the result in. You never call `empty_cart()` yourself.
- `filled_cart` builds a cart and adds two products, then returns it.

Run it:

```bash
pytest test_cart_fixtures.py -v
```

Expected output (abbreviated):

```
test_cart_fixtures.py::test_new_cart_is_empty PASSED
test_cart_fixtures.py::test_total PASSED
test_cart_fixtures.py::test_count PASSED
```

**Important:** by default a fixture runs **once per test** that requests it, and each test gets a **fresh** object. `test_total` and `test_count` each get their own `filled_cart`, so they cannot interfere with one another. This isolation is a core principle of reliable tests. (Tomorrow's other lesson, *fixture scopes*, shows how to change how often a fixture runs.)

### 4. Setup and teardown with `yield`

Some resources must be cleaned up: files, database connections, browser windows, temporary directories. If you use `return`, the function ends and there is no place to put cleanup. Use `yield` instead.

```python
# test_yield_fixture.py
import pytest

@pytest.fixture
def log_file(tmp_path):
    path = tmp_path / "run.log"
    handle = open(path, "w")
    print("\n[setup] log file opened")
    yield handle                      # the test runs here
    handle.close()
    print("\n[teardown] log file closed")

def test_write_log(log_file):
    log_file.write("hello\n")
    log_file.flush()
    assert not log_file.closed
```

**Line-by-line explanation**

- `tmp_path` - a **built-in fixture** (see section 7) that gives each test a unique temporary directory as a `pathlib.Path`. A fixture can request another fixture just like a test does.
- `path = tmp_path / "run.log"` - the `/` operator on `Path` joins path parts.
- `handle = open(path, "w")` - this is **setup**.
- `yield handle` - PyTest pauses the fixture here, injects `handle` into the test, and runs the test.
- Everything **after** `yield` is **teardown**. PyTest resumes the fixture after the test finishes, whether the test passed **or failed**.
- Run with `pytest -s` to see the `print` messages; by default PyTest captures output.

A useful mental model:

```
setup code
yield value   <-- test body runs here
teardown code
```

If the code *before* the `yield` raises an error, the teardown after it does not run (the yield was never reached). That is why you should keep setup minimal and put each resource in its own fixture so one failure does not leak another.

For extra safety you can use `try/finally`:

```python
@pytest.fixture
def connection():
    conn = make_connection()   # hypothetical helper
    try:
        yield conn
    finally:
        conn.close()
```

Here `finally` guarantees `close()` is called even if something unexpected happens during teardown logic.

### 5. Fixtures that use other fixtures

Fixtures can request other fixtures. PyTest builds a **dependency graph** and runs fixtures in the right order.

```python
# test_fixture_chain.py
import pytest
from cart import ShoppingCart

@pytest.fixture
def cart():
    return ShoppingCart()

@pytest.fixture
def cart_with_pen(cart):
    cart.add("pen", 2.0)
    return cart

@pytest.fixture
def cart_with_pen_and_book(cart_with_pen):
    cart_with_pen.add("book", 10.0)
    return cart_with_pen

def test_chain(cart_with_pen_and_book):
    assert cart_with_pen_and_book.total() == 12.0
```

When `test_chain` runs, PyTest resolves: `cart` -> `cart_with_pen` -> `cart_with_pen_and_book` -> test. Notice that all three fixtures return the **same** `ShoppingCart` object within one test; the base `cart` fixture is only created once per test even if multiple fixtures request it. That is called **fixture caching within a test**.

Teardown order is the **reverse** of setup order (last in, first out), just like stacking and unstacking plates.

### 6. Fixture return values can be anything

Fixtures can return numbers, strings, dictionaries, objects, functions, classes, or `None`. A very useful pattern is the **factory fixture**: the fixture returns a *function* that tests can call multiple times with different arguments.

```python
# test_factory_fixture.py
import pytest
from cart import ShoppingCart

@pytest.fixture
def make_cart():
    created = []

    def _make(*items):
        cart = ShoppingCart()
        for name, price, qty in items:
            cart.add(name, price, qty)
        created.append(cart)
        return cart

    yield _make
    # teardown: demonstrate cleanup of everything created
    for c in created:
        c.items.clear()

def test_factory(make_cart):
    small = make_cart(("pen", 1.0, 2))
    large = make_cart(("pen", 1.0, 2), ("book", 10.0, 3))
    assert small.total() == 2.0
    assert large.total() == 32.0
```

**Explanation:** `make_cart` returns the inner function `_make`. The test calls `make_cart(...)` as many times as it needs. The `created` list remembers everything built so teardown can clean up. Use a factory when a test needs **several different instances** of the same kind of thing.

### 7. Built-in fixtures you should know

PyTest ships with many fixtures. You do not define them; you just request them by name.

| Fixture | What it gives you |
|---------|-------------------|
| `tmp_path` | A unique `pathlib.Path` temporary directory per test. |
| `tmp_path_factory` | Create temp directories at wider scopes. |
| `capsys` | Capture text written to stdout/stderr. |
| `monkeypatch` | Safely change attributes, dict items, or environment variables for one test. |
| `request` | Information about the requesting test (name, scope, params). |
| `caplog` | Capture log records. |

Examples:

```python
# test_builtin_fixtures.py
import os

def greet(name):
    print(f"Hello, {name}!")

def test_greet_output(capsys):
    greet("Asha")
    captured = capsys.readouterr()
    assert captured.out == "Hello, Asha!\n"

def test_write_temp_file(tmp_path):
    f = tmp_path / "data.txt"
    f.write_text("42")
    assert f.read_text() == "42"

def test_env_var(monkeypatch):
    monkeypatch.setenv("APP_MODE", "test")
    assert os.environ["APP_MODE"] == "test"
    # after this test, APP_MODE is automatically restored
```

- `capsys.readouterr()` returns an object with `.out` and `.err` attributes.
- `monkeypatch.setenv` changes an environment variable and **automatically undoes** the change when the test ends. This is how you make tests independent of the machine they run on.

You can list every available fixture with:

```bash
pytest --fixtures
```

### 8. The `request` fixture

`request` lets a fixture learn about the test that asked for it.

```python
import pytest

@pytest.fixture
def announce(request):
    print(f"\nPreparing for test: {request.node.name}")
    yield
    print(f"\nFinished: {request.node.name}")

def test_demo(announce):
    assert True
```

`request.node` is the test item; `.name` is its name. You will also use `request.param` when a fixture is parametrized (below), and `request.addfinalizer(fn)` to register cleanup functions.

### 9. `autouse=True`: fixtures applied automatically

Normally a test must name a fixture to use it. With `autouse=True`, every test in scope uses it automatically.

```python
import pytest

@pytest.fixture(autouse=True)
def banner():
    print("\n--- test starting ---")
    yield
    print("--- test finished ---")

def test_one():
    assert 1 + 1 == 2

def test_two():
    assert "a".upper() == "A"
```

Both tests print the banner without requesting `banner`. Use `autouse` sparingly: it is "hidden magic" and can confuse readers. Good uses are resetting global state, setting up logging, or freezing the clock. Bad use: creating objects the test then needs (those should be explicit arguments so the test documents its own dependencies).

### 10. Parametrized fixtures with `params`

A fixture can run its dependent tests once for every value in `params`:

```python
import pytest

@pytest.fixture(params=["chrome", "firefox", "webkit"])
def browser_name(request):
    return request.param

def test_browser_name_is_known(browser_name):
    assert browser_name in {"chrome", "firefox", "webkit"}
```

This test runs three times, with ids like `test_browser_name_is_known[chrome]`. `request.param` holds the current value. Tomorrow's *Parametrization* lesson covers the more common `@pytest.mark.parametrize` and compares both techniques.

### 11. Renaming a fixture with `name=`

```python
@pytest.fixture(name="cart")
def _cart_fixture():
    return ShoppingCart()

def test_x(cart):
    assert cart.count() == 0
```

This avoids a confusing linting warning (redefining a name from an outer scope) when the test parameter has the same name as the fixture function. It is optional.

### 12. Where can fixtures live?

- In the **same test file** (as we did above) - visible only to that file.
- In a file named **`conftest.py`** - visible to all tests in that directory and below. We cover this in depth in the `conftest-py` lesson today.
- In **plugins** (installed packages, such as `pytest-playwright`).

### 13. How PyTest finds a fixture (lookup order)

When a test requests `cart`, PyTest searches, from nearest to farthest: the test class, the test module, `conftest.py` files from the test's folder up to the root, then installed plugins. The nearest definition **wins**; this lets you *override* a fixture locally.

## Code Examples: a realistic Project 1 scenario

Suppose Project 1's utility module validates user records and writes a report. Here we test a function that saves a report to disk.

```python
# report_utils.py
import json

def save_report(path, results):
    """Write a list of result dicts to a JSON file; return number written."""
    with open(path, "w", encoding="utf-8") as f:
        json.dump(results, f, indent=2)
    return len(results)

def load_report(path):
    with open(path, encoding="utf-8") as f:
        return json.load(f)
```

```python
# test_report_utils.py
import pytest
from report_utils import save_report, load_report

@pytest.fixture
def sample_results():
    return [
        {"test": "login", "status": "pass"},
        {"test": "search", "status": "fail"},
    ]

@pytest.fixture
def report_path(tmp_path):
    return tmp_path / "report.json"

def test_save_returns_count(report_path, sample_results):
    assert save_report(report_path, sample_results) == 2

def test_roundtrip(report_path, sample_results):
    save_report(report_path, sample_results)
    assert load_report(report_path) == sample_results
```

**Explanation:** `sample_results` provides data, `report_path` provides a safe temp location (nothing is written into your project, and PyTest cleans up old temp dirs). Each test has two arguments, so the arrange step is fully declarative. The tests contain only *act* and *assert* - the shape every good test should have (Arrange-Act-Assert).

## Real-World Scenarios

1. **UI test login:** a `logged_in_page` fixture opens the browser, logs in, yields the page, and closes the browser. Every UI test starts already logged in. (Playwright specifics come on Friday.)
2. **API tests:** an `auth_token` fixture requests a token once; tests use it in headers.
3. **Database tests:** a `db_connection` fixture opens a transaction and rolls it back after each test so the database stays clean.
4. **Test data:** a `make_user` factory fixture creates unique users per test, preventing collisions.

## Common Mistakes

1. **Calling the fixture directly.** Writing `cart = filled_cart()` inside a test raises an error in modern PyTest ("Fixture called directly"). Request it as a parameter instead.
2. **Typing the wrong name.** If the parameter name does not match any fixture, you get `fixture 'filld_cart' not found`. Check spelling and use `pytest --fixtures`.
3. **Using `return` when cleanup is needed.** Switch to `yield`.
4. **Putting asserts inside fixtures.** Fixtures prepare; tests verify. A failing assert in a fixture shows as an *error*, not a *failure*, which confuses reports.
5. **Overusing `autouse`.** Hidden dependencies make tests hard to read.
6. **Sharing mutable state accidentally.** If a fixture returns a module-level list, every test mutates the same list. Create new objects inside the fixture.
7. **Giant "do-everything" fixtures.** Prefer small fixtures that compose.

## Practice Exercises

**Exercise 1.** Create a fixture `user` that returns the dict `{"name": "Ravi", "age": 30}`. Write two tests that use it: one asserting the name, one asserting age is at least 18.

*Solution:*

```python
import pytest

@pytest.fixture
def user():
    return {"name": "Ravi", "age": 30}

def test_name(user):
    assert user["name"] == "Ravi"

def test_adult(user):
    assert user["age"] >= 18
```

**Exercise 2.** Write a `yield` fixture `temp_notes` that creates a file `notes.txt` in `tmp_path`, writes "todo", yields the path, and after the test prints "cleanup". Test that reading the file returns "todo". Run with `-s`.

*Hint:* use `tmp_path`, `write_text`, then `yield path`, then `print("cleanup")`.

**Exercise 3.** Build a fixture chain `base_cart` -> `cart_with_items` -> test that checks `count()`. Predict the number of times `base_cart` runs per test (answer: once).

**Exercise 4.** Write a factory fixture `make_user(name, age=20)` that returns a dict and records how many users were created. In teardown assert that the recorded count equals the number of calls made in the test.

**Exercise 5.** Use `capsys` to test a function `shout(text)` that prints `text.upper()`. 

*Solution:*

```python
def shout(text):
    print(text.upper())

def test_shout(capsys):
    shout("hi")
    assert capsys.readouterr().out == "HI\n"
```

**Exercise 6 (Project 1 link).** Take two of your Project 1 utility tests that repeat the same setup. Move the setup to a fixture and confirm both tests still pass. This is the start of today's exercise.

## Summary

- A fixture is a function marked `@pytest.fixture` that prepares (and optionally cleans up) what tests need.
- A test requests a fixture by naming it as a parameter; PyTest injects the value.
- `return` gives setup only; `yield` gives setup plus teardown, and teardown runs even if the test fails.
- Fixtures can depend on fixtures; teardown happens in reverse order.
- Factory fixtures return functions for creating many objects.
- Built-ins like `tmp_path`, `capsys`, `monkeypatch`, and `request` save huge effort.
- `autouse=True` applies a fixture automatically; use it sparingly.
- Keep fixtures small, free of assertions, and isolated per test.
- Next: how often fixtures run (fixture scopes), which we cover in the next lesson today.

## Additional Resources

- PyTest fixtures how-to: https://docs.pytest.org/en/stable/how-to/fixtures.html
- PyTest fixtures reference: https://docs.pytest.org/en/stable/reference/fixtures.html
- Python `contextlib` and generators background: https://docs.python.org/3/tutorial/classes.html#generators
