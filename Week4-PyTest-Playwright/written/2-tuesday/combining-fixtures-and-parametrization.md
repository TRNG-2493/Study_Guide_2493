# Combining Fixtures and Parametrization

## Learning Objectives

By the end of this lesson you will be able to:

- Use a parametrized test together with ordinary fixtures in the same test function.
- Create parametrized fixtures with `params=` and read values through `request.param`.
- Use `indirect=True` (and `indirect=["name"]`) to send parameter values *through* a fixture.
- Understand how PyTest builds the combinations when both are used, and how scope influences how often fixtures run.
- Apply `ids=` and `pytest.param` for readable output in combined scenarios.
- Choose between direct parametrization, parametrized fixtures, and indirect parametrization.

## Why This Matters

The weekly epic is to turn manual test design into a reliable automation framework. Real tests nearly always need **both** things you learned this morning: *prepared objects* (fixtures) and *many data sets* (parametrization). For example, a manual test case might say: "For each user role (admin, editor, viewer), log in and check which menu items are visible." The *role* is data; the *logged-in session* is a fixture that depends on the role.

In **Project 1 (QE Foundations)** you will refactor utility tests so that setup lives in fixtures and inputs live in tables. If you cannot combine the two, you end up falling back to copy and paste. Combining them is also the pattern behind cross-browser Playwright tests, which we will cover in depth on Thursday and Friday.

Make sure you remember the previous lessons today: *Fixtures* (`@pytest.fixture`, `yield`, `request`), *Fixture scopes*, and *Parametrization* (`@pytest.mark.parametrize`, `pytest.param`, `ids`).

## The Concept

### 1. The simplest combination: parametrize plus a fixture

A test function can use a fixture **and** be parametrized. PyTest fills the parametrize arguments from the table and the fixture arguments from fixture functions. They sit side by side in the parameter list.

First our code under test:

```python
# cart.py
class ShoppingCart:
    def __init__(self):
        self.items = {}

    def add(self, name, price, quantity=1):
        if price < 0:
            raise ValueError("price cannot be negative")
        if quantity <= 0:
            raise ValueError("quantity must be positive")
        if name in self.items:
            p, q = self.items[name]
            self.items[name] = (p, q + quantity)
        else:
            self.items[name] = (price, quantity)

    def total(self):
        return sum(p * q for p, q in self.items.values())
```

Now the test:

```python
# test_cart_combined.py
import pytest
from cart import ShoppingCart

@pytest.fixture
def cart():
    return ShoppingCart()

@pytest.mark.parametrize("name, price, qty, expected_total", [
    ("pen", 2.0, 1, 2.0),
    ("pen", 2.0, 5, 10.0),
    ("book", 12.5, 2, 25.0),
])
def test_add_single_item_total(cart, name, price, qty, expected_total):
    cart.add(name, price, qty)
    assert cart.total() == pytest.approx(expected_total)
```

**Line-by-line explanation**

- The fixture `cart` is a normal function-scope fixture: each of the three generated tests receives a **brand-new** `ShoppingCart`. That is critical: because of isolation, the first case cannot leak into the second.
- `@pytest.mark.parametrize(...)` supplies `name, price, qty, expected_total`.
- In the signature `cart` comes first by habit, but order does not matter for correctness; PyTest matches by name.
- Three tests are generated: `test_add_single_item_total[pen-2.0-1-2.0]`, and so on.

This is the most common combination, and it is all you need ninety percent of the time. Fixtures provide the **object**, parametrization provides the **inputs and expected outputs**.

### 2. Parametrized fixtures (`params=`)

Recall from the *Fixtures* lesson that a fixture can declare `params`. Every test using it runs once per param.

```python
# test_fixture_params.py
import pytest
from cart import ShoppingCart

@pytest.fixture(params=[0.0, 1.0, 99.99], ids=["free", "cheap", "pricey"])
def price(request):
    return request.param

def test_adding_any_price_is_allowed(price):
    cart = ShoppingCart()
    cart.add("thing", price)
    assert cart.total() == pytest.approx(price)
```

**Explanation**

- `params=[...]` lists the values the fixture will take.
- `ids=[...]` gives them readable names (optional but recommended).
- `request` is the built-in fixture; `request.param` holds the **current** value for this run.
- `test_adding_any_price_is_allowed` runs three times: `[free]`, `[cheap]`, `[pricey]`.

The big difference from `@pytest.mark.parametrize` is **reach**: *every* test that uses the `price` fixture gets the three variants automatically.

### 3. Fixtures and parametrization together: Cartesian products

Now combine both in one test:

```python
import pytest

@pytest.fixture(params=["USD", "EUR"])
def currency(request):
    return request.param

@pytest.mark.parametrize("amount", [1, 100])
def test_format(currency, amount):
    text = f"{amount} {currency}"
    assert str(amount) in text and currency in text
```

PyTest generates **2 x 2 = 4** tests: `[1-USD]`, `[1-EUR]`, `[100-USD]`, `[100-EUR]`. (IDs list the parametrize values and fixture values; use `--collect-only -q` to see the exact order.) Everything multiplies. If you have a parametrized fixture used by several fixtures in a chain, the combinations multiply across the chain.

**Rule of thumb:** count your dimensions and multiply. If the result is more than a few dozen, ask whether you really need all combinations (a technique called *pairwise testing* reduces them; mention it in discussion only).

### 4. Fixtures that depend on a parametrized fixture

Parametrization flows through the dependency chain:

```python
import pytest

@pytest.fixture(params=["admin", "editor", "viewer"])
def role(request):
    return request.param

@pytest.fixture
def user(role):
    return {"name": f"{role}_user", "role": role}

def can_delete(user):
    return user["role"] == "admin"

def test_delete_permission(user):
    expected = user["role"] == "admin"
    assert can_delete(user) is expected
```

`test_delete_permission` requests only `user`, but because `user` depends on `role`, the test runs three times. Hidden fan-out like this is powerful, but it can surprise readers, so name fixtures clearly and use `--setup-show` to inspect.

(An important style note: `expected = user["role"] == "admin"` duplicates the logic under test. In a real test use literal values via a table. We show it here to keep the focus on the mechanism.)

### 5. `indirect`: parametrize *through* a fixture

Suppose a fixture builds a complex object *from* a simple value, and you want to pick that value in the test's parametrize table. You do not want the raw value passed straight to the test; you want it to go *into the fixture first*. That is what `indirect=True` does.

```python
# test_indirect.py
import pytest
from cart import ShoppingCart

@pytest.fixture
def cart_with_qty(request):
    """Builds a cart containing 'pen' (price 2.0) with the quantity given by the test."""
    qty = request.param          # value from parametrize
    cart = ShoppingCart()
    cart.add("pen", 2.0, qty)
    return cart

@pytest.mark.parametrize("cart_with_qty, expected", [
    (1, 2.0),
    (3, 6.0),
    (10, 20.0),
], indirect=["cart_with_qty"])
def test_total_by_qty(cart_with_qty, expected):
    assert cart_with_qty.total() == pytest.approx(expected)
```

**Line-by-line explanation**

- The parametrize name `"cart_with_qty"` **matches the fixture name**.
- `indirect=["cart_with_qty"]` says: for *this* argument, do not hand the value directly to the test; deliver it to the fixture as `request.param`, and give the test whatever the fixture returns.
- `expected` is *not* in `indirect`, so it is passed straight to the test (a plain value).
- The values `1`, `3`, `10` become `request.param` inside the fixture; the test receives a fully built `ShoppingCart`.
- `indirect=True` (no list) would redirect **all** parametrized arguments through fixtures with matching names, which is rarely what you want when mixing raw and indirect values. Prefer the explicit list.

Why is this useful? The test table stays short and readable (`1, 3, 10`) while the *building logic* stays in the fixture and can include teardown. A real example: parametrize `"browser_type"` with `["chromium", "firefox"]` indirectly and let the fixture launch the right browser and close it afterwards.

### 6. A teardown example with indirect parametrization

```python
import pytest

class FakeBrowser:
    def __init__(self, kind):
        self.kind = kind
        self.open = True
    def close(self):
        self.open = False

@pytest.fixture
def browser(request):
    b = FakeBrowser(request.param)
    print(f"\n[launch {b.kind}]")
    yield b
    b.close()
    print(f"\n[close {b.kind}]")

@pytest.mark.parametrize("browser", ["chromium", "firefox"], indirect=True)
def test_browser_is_open(browser):
    assert browser.open is True
    assert browser.kind in {"chromium", "firefox"}
```

`indirect=True` is fine here because there is only one parametrized argument. Run with `-s` to watch launch/close happen for each browser. (We will use the real Playwright API later in the week; this fake class lets us study the pattern without installing anything.)

### 7. Parametrized fixture vs. indirect vs. direct: choosing

| Technique | Use when | Pros | Cons |
|-----------|----------|------|------|
| **Direct** `parametrize` | The test receives plain input/expected values | Simplest, visible in the test | Setup must be repeated unless also using a fixture |
| **Parametrized fixture** (`params=`) | Many tests should all run under every variant (browser, database) | Written once, applies everywhere | Hidden multiplication, less visible |
| **Indirect** | Test chooses a variant, fixture *builds* the resource | Short tables, logic and teardown in fixture | Slightly more advanced to read |

### 8. Scope interactions

Scope still applies to parametrized fixtures. A **module-scoped** parametrized fixture is created once *per parameter value per module*, and PyTest reorders tests to minimise the number of setups. For example:

```python
import pytest

@pytest.fixture(scope="module", params=["db_a", "db_b"])
def database(request):
    print(f"\n[connect {request.param}]")
    yield request.param
    print(f"\n[disconnect {request.param}]")

def test_one(database):
    assert database.startswith("db_")

def test_two(database):
    assert database.startswith("db_")
```

Run with `-s -v`. You will see: connect `db_a`, run `test_one[db_a]` and `test_two[db_a]`, disconnect `db_a`, then the same for `db_b`. PyTest groups tests so each connect/disconnect happens only twice, not four times. That reordering is intentional and efficient. For function scope there is no grouping.

### 9. Marks and IDs in combined scenarios

`pytest.param` works with indirect, too:

```python
import pytest

@pytest.mark.parametrize("browser", [
    pytest.param("chromium", id="chrome-like"),
    pytest.param("firefox", id="fox"),
    pytest.param("webkit", id="safari-like", marks=pytest.mark.skip(reason="not installed here")),
], indirect=True)
def test_something(browser):
    assert browser.open
```

(This relies on the `browser` fixture defined in section 6 being visible, for instance in the same file or `conftest.py`.)

For fixture `params`, you can use `pytest.param` inside the list:

```python
@pytest.fixture(params=[
    pytest.param("sqlite", id="sqlite"),
    pytest.param("postgres", id="pg", marks=pytest.mark.slow),
])
def engine(request):
    return request.param
```

### 10. Overriding a fixture with parametrize (direct)

A fascinating trick: parametrizing an argument that is **also a fixture name**, *without* `indirect`, **overrides** the fixture for that test with the raw values.

```python
import pytest

@pytest.fixture
def number():
    return 1

@pytest.mark.parametrize("number", [10, 20])
def test_override(number):
    assert number in (10, 20)   # fixture value 1 is NOT used
```

This is legal and sometimes helpful (to try specific values in one test), but can confuse people. Prefer unique names.

### 11. Debugging combinations

Useful commands:

```bash
pytest --collect-only -q            # list every generated test ID
pytest --setup-plan                 # show which fixtures would be set up, no execution
pytest --setup-show test_x.py       # show actual setup/teardown with scopes and params
pytest -k "admin and not viewer"    # filter by ID text
```

The `--setup-show` output includes the param in square brackets, such as `SETUP F role['admin']`.

## Code Examples: a Project 1 scenario

Let us test a `Report` utility that writes results in different formats. The format is the parameter, and a temp file is the fixture.

```python
# report_writer.py
import csv
import json

def write_report(path, rows, fmt):
    """Write list-of-dict rows to path in 'json' or 'csv' format."""
    if fmt == "json":
        with open(path, "w", encoding="utf-8") as f:
            json.dump(rows, f)
    elif fmt == "csv":
        with open(path, "w", newline="", encoding="utf-8") as f:
            writer = csv.DictWriter(f, fieldnames=list(rows[0].keys()))
            writer.writeheader()
            writer.writerows(rows)
    else:
        raise ValueError(f"unsupported format: {fmt}")
```

```python
# test_report_writer.py
import csv
import json
import pytest
from report_writer import write_report

@pytest.fixture
def rows():
    return [
        {"test": "login", "status": "pass"},
        {"test": "search", "status": "fail"},
    ]

@pytest.fixture
def output_file(tmp_path, request):
    # Name the file by the test's parametrized format, if any
    return tmp_path / f"report.{request.param}"

@pytest.mark.parametrize("output_file", ["json", "csv"], indirect=True)
def test_file_is_created(output_file, rows):
    fmt = output_file.suffix.lstrip(".")
    write_report(output_file, rows, fmt)
    assert output_file.exists()
    assert output_file.stat().st_size > 0

def test_json_content(tmp_path, rows):
    path = tmp_path / "r.json"
    write_report(path, rows, "json")
    assert json.loads(path.read_text()) == rows

def test_csv_content(tmp_path, rows):
    path = tmp_path / "r.csv"
    write_report(path, rows, "csv")
    with open(path, newline="") as f:
        assert list(csv.DictReader(f)) == rows

def test_unsupported_format(tmp_path, rows):
    with pytest.raises(ValueError):
        write_report(tmp_path / "r.xml", rows, "xml")
```

**Explanation**

- `output_file` combines two fixtures' worth of information: the built-in `tmp_path` and the indirect parameter via `request.param`.
- `test_file_is_created` runs twice (`json`, `csv`) and also uses the plain `rows` fixture.
- `suffix.lstrip(".")` turns `".json"` into `"json"`. `Path.suffix` includes the dot.
- The remaining tests use fixtures only. This mix of styles in one file is normal.

## Real-World Scenarios

1. **Roles x pages:** a parametrized `role` fixture logs in as each role; a parametrize table lists pages and the expected access. This is the manual "access matrix" automated.
2. **Cross-browser:** run every UI test on chromium, firefox, and webkit through a parametrized fixture (we will cover real Playwright setup on Thursday and Friday).
3. **Database engines:** run the same repository tests on SQLite and PostgreSQL via a module-scoped parametrized fixture.
4. **Environment matrix:** `dev`, `staging` x `v1`, `v2` API versions.
5. **Locale testing:** fixture builds a formatter for a given locale (indirect), test table provides numbers and expected strings.

## Common Mistakes

1. **Forgetting `indirect`.** Without it, the raw value (`"chromium"`) reaches the test, not the fixture's product. The tell-tale error is `AttributeError: 'str' object has no attribute ...`.
2. **Using `request.param` in a fixture that is not parametrized.** You get `AttributeError: 'SubRequest' object has no attribute 'param'`. Add `params=` or parametrize it with `indirect`.
3. **Using `indirect=True` when mixing raw and fixture-backed arguments.** Use the explicit list form.
4. **Combinatorial explosion.** Three 10-value dimensions yield 1,000 tests.
5. **Scope mismatch with parameters.** A session fixture that depends on a function-scope parametrized fixture still raises `ScopeMismatch`.
6. **Reusing the same name for a fixture and a direct parametrize argument by accident**, silently overriding the fixture.
7. **Unreadable IDs** such as `[chromium-<Page object at 0x...>]`. Use `ids`.
8. **Putting assertions about parameter *selection* inside fixtures.** Keep fixtures free of asserts.

## Practice Exercises

**Exercise 1.** Create a fixture `empty_cart` and a parametrized test that adds `(name, price)` pairs `("pen", 1.0)`, `("book", 5.0)`, `("bag", 20.0)` and asserts the cart total equals the price.

*Solution:*

```python
import pytest
from cart import ShoppingCart

@pytest.fixture
def empty_cart():
    return ShoppingCart()

@pytest.mark.parametrize("name, price", [("pen", 1.0), ("book", 5.0), ("bag", 20.0)])
def test_single_item(empty_cart, name, price):
    empty_cart.add(name, price)
    assert empty_cart.total() == pytest.approx(price)
```

**Exercise 2.** Make a fixture `size` with `params=["S", "M", "L"]` and write one test that asserts `size in "SML"`. Verify there are three tests with `--collect-only -q`.

**Exercise 3.** Add `@pytest.mark.parametrize("color", ["red", "blue"])` to the Exercise 2 test. How many tests now? *(Six.)*

**Exercise 4.** Write a fixture `numbers(request)` that returns `list(range(request.param))`, then use `indirect` to run a test with `request.param` values `0, 1, 5` and verify `len(numbers)` equals the value used. 

*Hint:* parametrize `("numbers, expected_len", [(0, 0), (1, 1), (5, 5)], indirect=["numbers"])`.

**Exercise 5.** Make a module-scoped parametrized fixture with two values, print in setup/teardown, and use `-s` to confirm setup runs twice (once per value) for a file with three tests.

**Exercise 6 (debugging).** The following test errors. Explain why and fix it.

```python
@pytest.fixture
def conn(request):
    return f"connection-{request.param}"

def test_conn(conn):
    assert conn
```

*Answer:* `conn` uses `request.param` but nobody supplies one. Fix by adding `params=[...]` to the fixture or `@pytest.mark.parametrize("conn", [...], indirect=True)` to the test.

**Exercise 7 (Project 1 link).** Take a Project 1 utility with several input categories and write one fixture that builds the utility object plus one parametrized table of inputs. Add readable IDs and use `--collect-only -q` to show the final list in your notes.

## Summary

- Fixtures supply prepared objects; parametrization supplies data sets. They combine naturally in one test.
- `@pytest.fixture(params=[...])` plus `request.param` runs every dependent test once per value.
- Direct parametrize and parametrized fixtures multiply into a Cartesian product.
- `indirect=["name"]` routes a parametrize value into a fixture of the same name, via `request.param`.
- Scope still applies: module-scoped parametrized fixtures are set up once per value, and PyTest groups tests to reduce setups.
- Use `ids`, `pytest.param`, `--collect-only`, and `--setup-show` to keep combinations understandable.
- Choose the simplest technique that keeps the test readable.

## Additional Resources

- Parametrizing fixtures and test functions (including `indirect`): https://docs.pytest.org/en/stable/how-to/parametrize.html
- Fixture parametrization (`params`) in the fixtures how-to: https://docs.pytest.org/en/stable/how-to/fixtures.html#fixture-parametrization
- `request` object reference: https://docs.pytest.org/en/stable/reference/reference.html#request
