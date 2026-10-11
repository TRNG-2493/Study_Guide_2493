# Sharing Fixtures Across Tests

## Learning Objectives

By the end of this lesson you will be able to:

- List and compare the ways PyTest lets multiple tests share a fixture: same module, `conftest.py`, helper modules loaded with `pytest_plugins`, and installed plugins.
- Share fixtures between test classes and test functions, including via `@pytest.mark.usefixtures`.
- Decide between *sharing the fixture definition* (reuse code) and *sharing the fixture value* (reuse the same object through scope).
- Override and extend a shared fixture at module, class, or directory level.
- Build fixtures from other shared fixtures (layering).
- Use `pytest --fixtures` and `--fixtures-per-test` to find where a shared fixture comes from.
- Avoid hidden coupling and shared-state bugs.

## Why This Matters

The weekly epic is to grow from "a few tests" to "a framework". In a framework, dozens of tests, written by several people, rely on the same few building blocks: a configured client, a logged-in user, a data builder. If each author writes their own version, you get inconsistent, brittle suites. If they share well-designed fixtures, a change in one place updates everything.

In **Project 1 (QE Foundations)** you work in a team repository. Teammates must be able to use your fixtures without reading your code. Sharing is also exactly how Playwright's `page` fixture reaches your tests (it is shared through an installed plugin); we will cover Playwright in depth on Thursday and Friday. On Wednesday we will assemble a reusable framework skeleton (we will cover this in depth on Wednesday), so today is the foundation for it.

Before reading on, recall: *Fixtures*, *Fixture scopes* (especially "module is per file; session is per run"), *conftest.py* (the hierarchy and overriding rules).

## The Concept

### 1. Two meanings of "sharing"

Beginners often mix up two different ideas:

1. **Sharing the definition** - many tests can *use* the same fixture function (each test gets its own fresh result, because the default scope is function). This is about code reuse.
2. **Sharing the value** - many tests receive the *same object* (because the fixture has a wider scope). This is about performance, and about danger if the object is mutable.

Both are valid. Be clear which one you intend. Everything in this lesson about *where to put* a fixture concerns (1); the scope decides (2).

### 2. Level 1: fixtures within the same module

Define a fixture in the test file; all test functions and classes **in that file** can use it.

```python
# test_module_sharing.py
import pytest

@pytest.fixture
def numbers():
    return [3, 1, 2]

def test_sorted(numbers):
    assert sorted(numbers) == [1, 2, 3]

class TestStats:
    def test_max(self, numbers):
        assert max(numbers) == 3

    def test_min(self, numbers):
        assert min(numbers) == 1
```

Functions *and* methods use `numbers`. Each gets its own list because the scope is `function`.

### 3. Level 2: class-level fixtures

A fixture defined *inside* a class is only visible to the methods of that class, which is a neat way to keep specialised setup local. Note that `self` is the first parameter:

```python
import pytest

class TestAccount:
    @pytest.fixture
    def account(self):
        return {"balance": 100}

    def test_balance(self, account):
        assert account["balance"] == 100

    def test_deposit(self, account):
        account["balance"] += 50
        assert account["balance"] == 150

def test_outside_cannot_see_it():
    # a plain function here could NOT request 'account'
    assert True
```

### 4. Applying fixtures without arguments: `usefixtures`

If a test does not need the *value* of a fixture but only its *effect*, use the marker:

```python
import os
import pytest

@pytest.fixture
def clean_env(monkeypatch):
    monkeypatch.delenv("DEBUG", raising=False)

@pytest.mark.usefixtures("clean_env")
def test_debug_not_set():
    assert "DEBUG" not in os.environ

@pytest.mark.usefixtures("clean_env")
class TestAllClean:
    def test_a(self):
        assert os.environ.get("DEBUG") is None

    def test_b(self):
        assert os.environ.get("DEBUG") is None
```

Explanation: `monkeypatch.delenv(name, raising=False)` removes an environment variable if present and does not error if it is absent. `usefixtures` applied to a class covers all its methods. It is also usable at module level:

```python
pytestmark = pytest.mark.usefixtures("clean_env")
```

`pytestmark` is a special module-level variable: markers assigned to it apply to every test in the file.

Limitations: `usefixtures` cannot pass the fixture's *value* to the test. If you need the value, request it as an argument.

### 5. Level 3: sharing across files with conftest.py

Covered in the previous lesson: a fixture in `conftest.py` is available to every test in that directory and below. This is the **default, recommended** sharing mechanism. Keep this guideline:

> *Put each fixture at the lowest level that still covers all the tests that need it.*

A fixture needed by only the `api` tests belongs in `tests/api/conftest.py`, not the root conftest. This keeps scope of knowledge small and discoverable.

### 6. Level 4: fixture modules loaded with `pytest_plugins`

When `conftest.py` becomes crowded, split fixtures into several regular Python modules and load them from a **top-level** conftest with the `pytest_plugins` variable. Treat each module as a mini plugin:

```
tests/
├── conftest.py
├── fixtures/
│   ├── __init__.py
│   ├── users.py
│   └── files.py
└── test_profile.py
```

`tests/fixtures/users.py`:

```python
import pytest

@pytest.fixture
def make_user():
    def _make(name="Dana", role="viewer"):
        return {"name": name, "role": role}
    return _make

@pytest.fixture
def admin_user(make_user):
    return make_user(name="Root", role="admin")
```

`tests/fixtures/files.py`:

```python
import pytest

@pytest.fixture
def scratch_file(tmp_path):
    path = tmp_path / "scratch.txt"
    path.write_text("")
    return path
```

`tests/conftest.py`:

```python
pytest_plugins = [
    "tests.fixtures.users",
    "tests.fixtures.files",
]
```

`tests/test_profile.py`:

```python
def test_admin_role(admin_user):
    assert admin_user["role"] == "admin"

def test_scratch_starts_empty(scratch_file):
    assert scratch_file.read_text() == ""
```

**Explanation**

- `pytest_plugins` is a list of **importable module names**. PyTest imports each module and registers its fixtures as if they were defined in the conftest.
- The dotted names must be importable from `sys.path`. With the layout above you run `pytest` from the project root, where `tests` is a package (that is why `tests/__init__.py` is typically added, or set `pythonpath = .` in `pytest.ini`). If you get `ModuleNotFoundError`, check `__init__.py` files and `pythonpath`.
- `pytest_plugins` should be declared in the **top-level** conftest (or in the test module). PyTest warns or errors if it is declared in non-top-level conftests in modern versions.
- This approach lets you organise fixtures by theme (users, files, browser, data), each in a file of manageable size.

### 7. Why not `from module import fixture`?

You *can* import a fixture function into a test module or conftest and it will work:

```python
from fixtures.users import make_user   # works, but...
```

Downsides: linters complain about "unused import" and "redefinition" (because you then take it as a parameter), and a wildcard import (`import *`) can bring surprises. `pytest_plugins` is the clean, supported way for bulk sharing.

### 8. Level 5: installed plugins and packages

Fixtures also arrive from **installed plugins**. For example, `pytest-playwright` (which you install on Thursday; we will cover this in depth then) provides `page`, `browser`, and `context` fixtures. Your own organisation can package shared fixtures as an internal plugin, published to a package index, and used across many repositories. A plugin registers itself through an *entry point* in its packaging configuration. This is advanced; for now know that "fixtures can come from pip-installed packages" and that `pytest --fixtures` lists them under their package.

### 9. Overriding shared fixtures where needed

Because the nearest definition wins, any test module, class, or sub-directory can customise a shared fixture:

```python
# tests/conftest.py
import pytest

@pytest.fixture
def base_url():
    return "https://staging.example.test"
```

```python
# tests/test_local.py
import pytest

@pytest.fixture
def base_url():                        # module-level override
    return "http://localhost:8000"

def test_uses_local(base_url):
    assert base_url.startswith("http://localhost")
```

You can also override with parametrization (see *Combining fixtures and parametrization*):

```python
@pytest.mark.parametrize("base_url", ["http://a.test", "http://b.test"])
def test_each_url(base_url):
    assert base_url.endswith(".test")
```

Overriding is a sharp tool; document why when you do it.

### 10. Layering shared fixtures

Good frameworks build **layers**: small low-level fixtures plus higher-level ones that compose them.

```python
# tests/conftest.py
import pytest

@pytest.fixture(scope="session")
def settings():
    return {"base_url": "https://example.test", "timeout": 5}

@pytest.fixture
def http_client(settings):
    class Client:
        def __init__(self, base_url, timeout):
            self.base_url = base_url
            self.timeout = timeout
        def url(self, path):
            return f"{self.base_url}/{path.lstrip('/')}"
    return Client(settings["base_url"], settings["timeout"])

@pytest.fixture
def orders_client(http_client):
    class Orders:
        def __init__(self, client):
            self.client = client
        def list_url(self):
            return self.client.url("/orders")
    return Orders(http_client)
```

```python
# tests/test_orders.py
def test_orders_url(orders_client):
    assert orders_client.list_url() == "https://example.test/orders"
```

Layering keeps each fixture small, testable, and reusable. A test requests only the top layer; PyTest builds the rest. Notice the scopes: `settings` is session scoped and read-only; the clients are function scoped; this respects the scope rule (narrow may depend on wide).

### 11. Sharing *values* safely

When you intentionally share one object (a wide scope), choose one of the safe patterns:

- **Immutable data:** tuples, `frozenset`, numbers, strings.
- **Read-only wrapper:** `types.MappingProxyType(dict)` makes a read-only dict view.
- **Copy on request:** a function-scoped fixture that returns a deep copy of a session-scoped template.

```python
import copy
import pytest

@pytest.fixture(scope="session")
def _template_user():
    return {"name": "Template", "tags": ["a", "b"]}

@pytest.fixture
def user(_template_user):
    return copy.deepcopy(_template_user)

def test_mutation_is_local(user):
    user["tags"].append("c")
    assert user["tags"] == ["a", "b", "c"]

def test_template_untouched(user):
    assert user["tags"] == ["a", "b"]
```

Both tests pass in any order because each one gets its own deep copy. The leading underscore in `_template_user` signals "internal, do not request directly". `copy.deepcopy` copies nested objects as well (a plain `copy.copy` would share the inner list).

### 12. Finding where a fixture comes from

```bash
pytest --fixtures                   # all fixtures visible, grouped by file
pytest --fixtures -v                # with more detail, includes private ones with -v
pytest --fixtures-per-test          # fixtures used by each test, and their origin
pytest --setup-show                 # at run time, shows order, scope and parameters
```

Typical output:

```
------------- fixtures defined from tests/conftest.py -------------
settings [session scope] -- tests/conftest.py:4
http_client -- tests/conftest.py:8
```

Use these when you inherit a framework and wonder "where does `page` (or `settings`) come from?".

### 13. Design guidelines for shared fixtures

1. **Name clearly** (`logged_in_admin`, not `fx1`).
2. **Document** with a docstring: `pytest --fixtures` prints the first line of the docstring.
3. **Keep fixtures independent** of test order.
4. **Prefer factories** to many near-identical fixtures.
5. **Do not hide assertions** in shared fixtures.
6. **Version carefully:** changing a shared fixture can break many tests; run the whole suite.
7. **Prefer explicit over implicit:** `autouse` in shared files affects everyone below it.

## Code Examples: a Project 1 scenario

Layout for a small team repo:

```
project1/
├── pytest.ini
├── src/
│   └── inventory.py
└── tests/
    ├── conftest.py
    ├── fixtures/
    │   ├── __init__.py
    │   └── inventory_fixtures.py
    ├── unit/
    │   └── test_inventory_unit.py
    └── integration/
        └── test_inventory_report.py
```

`src/inventory.py`:

```python
class Inventory:
    def __init__(self):
        self._stock = {}

    def add(self, sku, qty):
        if qty <= 0:
            raise ValueError("qty must be positive")
        self._stock[sku] = self._stock.get(sku, 0) + qty

    def remove(self, sku, qty):
        have = self._stock.get(sku, 0)
        if qty > have:
            raise ValueError("insufficient stock")
        self._stock[sku] = have - qty

    def quantity(self, sku):
        return self._stock.get(sku, 0)

    def skus(self):
        return sorted(self._stock)
```

`pytest.ini`:

```ini
[pytest]
testpaths = tests
pythonpath = src .
```

(`pythonpath = src .` adds both the `src` directory and the project root to `sys.path`; the root is needed so `tests.fixtures...` is importable.)

`tests/fixtures/inventory_fixtures.py`:

```python
import pytest
from inventory import Inventory

@pytest.fixture
def empty_inventory():
    """A brand-new, empty Inventory."""
    return Inventory()

@pytest.fixture
def stocked_inventory(empty_inventory):
    """Inventory containing pens (10) and books (4)."""
    empty_inventory.add("pen", 10)
    empty_inventory.add("book", 4)
    return empty_inventory
```

`tests/conftest.py`:

```python
pytest_plugins = ["tests.fixtures.inventory_fixtures"]
```

`tests/unit/test_inventory_unit.py`:

```python
import pytest

def test_add_increases_quantity(empty_inventory):
    empty_inventory.add("pen", 3)
    assert empty_inventory.quantity("pen") == 3

def test_remove_too_much_fails(stocked_inventory):
    with pytest.raises(ValueError, match="insufficient"):
        stocked_inventory.remove("book", 5)
```

`tests/integration/test_inventory_report.py`:

```python
def test_skus_sorted(stocked_inventory):
    assert stocked_inventory.skus() == ["book", "pen"]
```

**Explanation**

- The fixtures are defined once in a themed module and shared with `pytest_plugins`.
- `unit` and `integration` folders (siblings) both use them; sibling folders would *not* share a fixture defined in the other's conftest, but they can share through the top-level conftest.
- `stocked_inventory` layers on `empty_inventory`; since each test gets a fresh object, tests never interfere.
- `pytest.raises(ValueError, match="insufficient")` checks both the exception type and that its message matches the regular expression "insufficient".

## Real-World Scenarios

1. **Team framework:** a "core" fixtures package everyone depends on; each squad adds its own conftest on top.
2. **Multiple repos:** an internal pip package provides `api_client` and `auth` fixtures to all repos.
3. **Large suites:** fixtures split by domain (`users.py`, `orders.py`, `payments.py`) loaded via `pytest_plugins`.
4. **Local override for debugging:** one test file temporarily overrides `base_url` to hit a local server.
5. **UI automation:** a shared `logged_in_page` fixture used by dozens of tests so a login-flow change is a one-line fix (we will cover Playwright on Thursday and Friday).

## Common Mistakes

1. **Defining the same fixture in several files** (copy and paste) instead of sharing.
2. **Expecting `module` scope to be shared across files.** Use `session` (and put it in conftest).
3. **Wide-scoped mutable fixtures** causing order-dependent failures.
4. **Importing fixture functions** manually; prefer conftest or `pytest_plugins`.
5. **Declaring `pytest_plugins` in a non-top-level conftest**, leading to warnings or errors; keep it in the root conftest.
6. **Module not importable** in `pytest_plugins`: missing `__init__.py` or `pythonpath`.
7. **Silent overrides** by same-named fixtures at a lower level.
8. **Using `usefixtures` and expecting the value.** It provides no value.
9. **Everything `autouse`.** Tests become impossible to read.
10. **Giant fixtures** that do ten things; compose small ones.

## Practice Exercises

**Exercise 1.** In one file create a fixture `words` returning `["apple", "banana"]` and use it from both a plain function test and a test method inside a class.

**Exercise 2.** Define a class-local fixture `wallet` inside `class TestWallet` and write two tests. Then try using `wallet` from a function outside the class; read the error message (`fixture 'wallet' not found`) and explain why.

**Exercise 3.** Write a fixture `temp_cwd(tmp_path, monkeypatch)` that changes the working directory to `tmp_path` using `monkeypatch.chdir(tmp_path)`. Apply it to a test class using `@pytest.mark.usefixtures("temp_cwd")` and in each test create a file named `x.txt` and assert it exists with `Path("x.txt").exists()`.

*Solution:*

```python
from pathlib import Path
import pytest

@pytest.fixture
def temp_cwd(tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)
    return tmp_path

@pytest.mark.usefixtures("temp_cwd")
class TestFiles:
    def test_create(self):
        Path("x.txt").write_text("hi")
        assert Path("x.txt").exists()

    def test_isolated(self):
        assert not Path("x.txt").exists()
```

**Exercise 4.** Move your fixtures from Exercise 1 into `tests/fixtures/text_fixtures.py` and load them with `pytest_plugins`. Verify with `pytest --fixtures`.

**Exercise 5.** Create root-level `base_url` in conftest and override it in one test module. Write one test for each and confirm each sees the right value.

**Exercise 6.** Build a three-layer fixture chain (`settings` -> `client` -> `service`) and use `pytest --setup-show` to confirm the order and scopes.

**Exercise 7.** Demonstrate the shared mutable state bug with a session-scoped list, then fix it using `copy.deepcopy` in a function-scoped wrapper.

**Exercise 8 (Project 1 link).** Audit your Project 1 tests: list every fixture, where it is defined, and who uses it. Move any fixture used by more than one file into the appropriate `conftest.py` level, and write a short comment above each saying who should use it.

## Summary

- Sharing a fixture *definition* (code reuse) is different from sharing a *value* (wider scope).
- Options: same module, class-local, `conftest.py` (default choice), fixture modules via `pytest_plugins` (top-level conftest), and installed plugins.
- `usefixtures` / `pytestmark` apply fixtures for their side effects without arguments.
- The closest fixture definition wins; use this to override carefully.
- Layer small fixtures into bigger ones, and respect the scope rule.
- Share wide-scoped values only if immutable, read-only, or copied per test.
- Discover origins with `--fixtures`, `--fixtures-per-test`, `--setup-show`.
- Next: replacing external dependencies in tests with mocks.

## Additional Resources

- Sharing fixtures with conftest.py: https://docs.pytest.org/en/stable/reference/fixtures.html#conftest-py-sharing-fixtures-across-multiple-files
- Using plugins and `pytest_plugins`: https://docs.pytest.org/en/stable/how-to/plugins.html
- Overriding fixtures on various levels: https://docs.pytest.org/en/stable/how-to/fixtures.html#overriding-fixtures-on-various-levels
