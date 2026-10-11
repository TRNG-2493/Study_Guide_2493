# Fixture Scopes

## Learning Objectives

By the end of this lesson you will be able to:

- Explain what a fixture *scope* is and list the five scopes: `function`, `class`, `module`, `package`, and `session`.
- Choose the right scope by weighing speed against test isolation.
- Predict how many times a fixture runs and when its teardown happens for each scope.
- Understand the rule that a fixture can only depend on fixtures of the same or a wider scope.
- Use `tmp_path_factory` and `request` with wider-scoped fixtures.
- Recognise the "shared mutable state" trap and avoid it.

## Why This Matters

Our weekly epic is converting manual test design into a fast, reliable automation framework. Reliability comes from **isolation** (tests do not affect each other). Speed comes from **not repeating expensive work**. Scopes are PyTest's tool for balancing those two forces.

In Project 1 (QE Foundations) you may load a large test-data file, connect to a service, or later launch a browser. Doing that for every one of 200 tests wastes minutes. Doing it once for the whole run saves time but risks one test's leftovers poisoning another. Choosing the right scope is a daily decision for a test automation engineer. When you start Playwright (we will cover it in depth on Thursday and Friday), you will see exactly this: the *browser* is expensive and shared widely, while each *page* is cheap and isolated per test.

You should be comfortable with the previous lesson (*Fixtures*): `@pytest.fixture`, requesting by parameter name, and `yield` for teardown.

## The Concept

### 1. What is a scope?

A fixture's **scope** controls **how long the fixture's value lives** and therefore **how often it is created**. You set it with the `scope` argument:

```python
@pytest.fixture(scope="module")
def shared_resource():
    ...
```

Imagine a restaurant. A *function*-scoped fixture is a clean plate for every dish. A *module*-scoped fixture is a pot of soup made once for a whole dinner service. A *session*-scoped fixture is the building's electricity: switched on once for the entire day.

### 2. The five scopes

| Scope | Created | Destroyed (teardown) | Typical use |
|-------|---------|----------------------|-------------|
| `function` (default) | Before each test | After each test | Fresh objects, anything mutable |
| `class` | Once per test class | After the last test in the class | Setup shared by a class's tests |
| `module` | Once per `.py` test file | After the last test in the file | Loading a file, a module-level connection |
| `package` | Once per package (directory with tests) | After the last test in the package | Per-feature setup |
| `session` | Once per whole `pytest` run | At the very end | Expensive: browser, DB, auth token |

Notes:

- `function` is the default and the safest. Start there.
- `package` scope is rarely used; know it exists.
- Scope names are strings. A scope can also be a **callable** (dynamic scope), described near the end.

### 3. Seeing scopes in action

The best way to learn scopes is to print when each fixture runs. Create `test_scopes_demo.py`:

```python
# test_scopes_demo.py
import pytest

@pytest.fixture(scope="session")
def session_fx():
    print("\n[session setup]")
    yield "S"
    print("\n[session teardown]")

@pytest.fixture(scope="module")
def module_fx():
    print("\n[module setup]")
    yield "M"
    print("\n[module teardown]")

@pytest.fixture(scope="class")
def class_fx():
    print("\n[class setup]")
    yield "C"
    print("\n[class teardown]")

@pytest.fixture  # function scope
def function_fx():
    print("\n[function setup]")
    yield "F"
    print("\n[function teardown]")

class TestGroupA:
    def test_a1(self, session_fx, module_fx, class_fx, function_fx):
        print("running test_a1")

    def test_a2(self, session_fx, module_fx, class_fx, function_fx):
        print("running test_a2")

class TestGroupB:
    def test_b1(self, session_fx, module_fx, class_fx, function_fx):
        print("running test_b1")
```

Run it with output shown (`-s`):

```bash
pytest test_scopes_demo.py -s
```

You will see roughly:

```
[session setup]
[module setup]
[class setup]
[function setup]
running test_a1
[function teardown]
[function setup]
running test_a2
[function teardown]
[class teardown]
[class setup]
[function setup]
running test_b1
[function teardown]
[class teardown]
[module teardown]
[session teardown]
```

**Line-by-line explanation**

- `scope="session"` -> `session_fx` is built before the first test that needs it and torn down once at the very end.
- `module_fx` is built once for the file and torn down after the last test in the file.
- `class_fx` is built **separately for each class**: once for `TestGroupA` (shared by `test_a1` and `test_a2`), once for `TestGroupB`.
- `function_fx` is built and destroyed around **every** test.
- Teardown always happens in the reverse order of setup: narrower scopes finish first.
- Fixtures are created **lazily**: only when the first test requests them (unless `autouse`). A session fixture nobody uses never runs.

### 4. Scope and the cost/isolation trade-off

| Wider scope | Narrower scope |
|-------------|----------------|
| Faster (expensive work done once) | Slower (work repeated) |
| Tests may influence each other | Tests are independent |
| Harder to debug (state leakage) | Easier to debug |

**Rule of thumb:** use the *narrowest* scope that keeps your suite fast enough. Widen only for things that are (a) expensive to create *and* (b) read-only or safely resettable.

### 5. Example: expensive read-only data (module scope)

```python
# test_catalog.py
import json
import pytest

@pytest.fixture(scope="module")
def catalog(tmp_path_factory):
    # Imagine this is a big file that takes a long time to parse.
    folder = tmp_path_factory.mktemp("data")
    file = folder / "catalog.json"
    file.write_text(json.dumps({"pen": 2.0, "book": 10.0, "bag": 25.0}))
    print("\nLoading catalog (expensive!)")
    with open(file) as f:
        return json.load(f)

def test_pen_price(catalog):
    assert catalog["pen"] == 2.0

def test_book_price(catalog):
    assert catalog["book"] == 10.0

def test_catalog_size(catalog):
    assert len(catalog) == 3
```

**Explanation:**

- `tmp_path_factory` is the **wider-scope sibling of `tmp_path`**. `tmp_path` is function scoped, so a module-scoped fixture cannot use it (see the scope rule below). `tmp_path_factory.mktemp("data")` creates a new temp directory and returns a `Path`.
- "Loading catalog" prints **once**, even though three tests use it.
- The tests only *read* the dictionary, so sharing is safe.

### 6. The scope-dependency rule

> A fixture can only request fixtures with the **same or wider** scope.

Why? A `session` fixture lives for the whole run. If it depended on a `function` fixture that is destroyed after each test, it would be holding a dead object. PyTest prevents this:

```python
import pytest

@pytest.fixture
def per_test():
    return 1

@pytest.fixture(scope="session")
def long_lived(per_test):    # WRONG
    return per_test + 1

def test_x(long_lived):
    pass
```

Running this produces:

```
ScopeMismatch: You tried to access the function scoped fixture per_test
with a session scoped request object ...
```

**Fix:** make `per_test` wider scoped, or make `long_lived` narrower. The order from narrowest to widest is: `function` < `class` < `module` < `package` < `session`.

The *opposite* direction is perfectly fine: a function-scoped fixture may request a session-scoped one.

### 7. The shared mutable state trap

A wide-scoped fixture that returns a **mutable** object (list, dict, class instance) is shared by reference. If one test changes it, later tests see the change.

```python
import pytest

@pytest.fixture(scope="module")
def shared_list():
    return []

def test_first(shared_list):
    shared_list.append("a")
    assert shared_list == ["a"]

def test_second(shared_list):
    # This FAILS if test_first runs before it, because the list is already ["a"]
    assert shared_list == []
```

`test_second` fails because the list persists. That failure depends on **test order**, the nastiest kind of bug: if someone runs only `test_second`, it passes. This is called a **flaky or order-dependent test**.

Two safe patterns:

1. **Return immutable data** (tuples, strings, numbers, `frozenset`, `types.MappingProxyType`).
2. **Use a wide-scoped expensive resource plus a narrow-scoped reset fixture**:

```python
import pytest

class FakeDatabase:
    def __init__(self):
        self.rows = []
    def insert(self, row):
        self.rows.append(row)
    def clear(self):
        self.rows.clear()

@pytest.fixture(scope="session")
def database():
    print("\n[connect once]")
    db = FakeDatabase()
    yield db
    print("\n[disconnect once]")

@pytest.fixture
def clean_db(database):          # function scope: runs for each test
    database.clear()
    yield database
    database.clear()

def test_insert_one(clean_db):
    clean_db.insert({"id": 1})
    assert len(clean_db.rows) == 1

def test_starts_empty(clean_db):
    assert clean_db.rows == []
```

**Explanation:** the "connection" is expensive and made once per session; the `clean_db` wrapper gives every test a pristine state. This *wide resource + narrow reset* pattern is the foundation of real automation frameworks. (Playwright does similarly: one browser, a fresh context per test; we will cover that on Friday.)

### 8. Class scope in detail

`scope="class"` is useful when tests are grouped in classes (you learned about test classes on Monday).

```python
import pytest

@pytest.fixture(scope="class")
def counter_store():
    print("\n[create store]")
    return {"count": 0}

class TestCounting:
    def test_start(self, counter_store):
        assert counter_store["count"] == 0

    def test_increment(self, counter_store):
        counter_store["count"] += 1
        assert counter_store["count"] == 1
```

Tests in a class run top to bottom by default, so this works, but it makes the tests dependent on order. Use class scope for *read-only* shared setup when possible.

You may also apply a fixture to every test in a class without passing it as an argument by using the `usefixtures` marker:

```python
@pytest.mark.usefixtures("counter_store")
class TestNoArgNeeded:
    def test_runs(self):
        assert True
```

### 9. Session scope in detail

Session scope is perfect for things done once per `pytest` command: starting a service, reading config, logging in via API to get a token.

```python
# conftest.py (fixtures there are shared; conftest is covered later today)
import pytest

@pytest.fixture(scope="session")
def api_token():
    print("\n[requesting token once]")
    return "abc123-token"
```

Any test in the folder can then take `api_token` as a parameter. The token request occurs one time per run.

**pytest-xdist caveat:** if you later run tests in parallel with several worker processes, "session" means once *per worker*, not once overall. For now just remember that wide scope is not the same as "globally once" in parallel runs.

### 10. Package scope

`scope="package"` creates the fixture once for each Python package (a directory with an `__init__.py`) containing the tests and tears it down after the last test of the package. It is uncommon; mention it in conversation but prefer `module` or `session`.

### 11. Dynamic scope

Sometimes the scope should be decided at runtime, for example from a command-line option. You can pass a function that receives `fixture_name` and `config`:

```python
import pytest

def determine_scope(fixture_name, config):
    if config.getoption("--keep-db", default=False):
        return "session"
    return "function"

@pytest.fixture(scope=determine_scope)
def db():
    ...
```

(For the option to exist you must register it in a `conftest.py` with `pytest_addoption`; that is an advanced topic, so treat this as awareness only.)

### 12. Scope and `autouse`

You can combine them: an `autouse` session fixture runs automatically once, at the beginning:

```python
@pytest.fixture(scope="session", autouse=True)
def announce_run():
    print("\n=== Test run starting ===")
    yield
    print("\n=== Test run finished ===")
```

### 13. Checking scopes and setup plans

Use `--setup-show` to watch fixture setup/teardown without adding prints:

```bash
pytest test_scopes_demo.py --setup-show
```

Output shows lines like `SETUP    S session_fx`, `SETUP    M module_fx`, `TEARDOWN F function_fx`. The letters S, M, C, F (and P for package) denote the scope. This is the single best debugging tool for scope questions.

## Code Examples: a Project 1 style scenario

We want to test a `UserRepository` backed by a dictionary. Creating it is "expensive", but each test needs clean data.

```python
# user_repo.py
class UserRepository:
    def __init__(self):
        self._users = {}

    def add(self, user_id, name):
        if user_id in self._users:
            raise ValueError("duplicate id")
        self._users[user_id] = name

    def get(self, user_id):
        return self._users.get(user_id)

    def clear(self):
        self._users.clear()

    def count(self):
        return len(self._users)
```

```python
# test_user_repo.py
import pytest
from user_repo import UserRepository

@pytest.fixture(scope="module")
def repo_instance():
    print("\n[expensive init]")
    return UserRepository()

@pytest.fixture
def repo(repo_instance):
    repo_instance.clear()
    yield repo_instance
    repo_instance.clear()

def test_add_and_get(repo):
    repo.add(1, "Meera")
    assert repo.get(1) == "Meera"

def test_duplicate_rejected(repo):
    repo.add(1, "Meera")
    with pytest.raises(ValueError):
        repo.add(1, "Other")

def test_empty_on_start(repo):
    assert repo.count() == 0
```

**Explanation:** `repo_instance` is module scoped, so "[expensive init]" prints once. `repo` is function scoped and requests the wider one (allowed). It clears the data before *and* after each test, so tests are independent in any order. Run `pytest test_user_repo.py -p no:randomly` or even `pytest test_user_repo.py::test_empty_on_start` alone and it still passes.

## Real-World Scenarios

- **Browser automation:** one browser per session (launching takes seconds), a fresh page/context per test (so cookies do not leak). We will cover this in depth when we reach Playwright on Thursday and Friday.
- **API tests:** an access token at session scope; a created order at function scope that is deleted in teardown.
- **Database tests:** schema creation once per session; each test wraps changes in a transaction rolled back after the test.
- **Large reference data:** a module-scoped fixture parses a big CSV once.

## Common Mistakes

1. **Using function scope for everything and having a slow suite.** Profile it, and widen scope for expensive read-only items.
2. **Using session scope for mutable data.** This creates order-dependent failures.
3. **ScopeMismatch errors.** Remember: depend on the same or wider scope only.
4. **Assuming a wide fixture runs before the first test of the run.** It is lazy; it runs when first requested (unless `autouse`).
5. **Forgetting that teardown for a wide fixture is delayed.** Resources stay open until the scope ends; be aware of resource limits.
6. **Thinking `module` scope spans multiple files.** It is *per file*. Use `session` to share across files.
7. **Defining the same session fixture in several files** and expecting it to run once. Each definition is separate. Put shared fixtures in `conftest.py` (next lessons).

## Practice Exercises

**Exercise 1.** Create a fixture with `scope="module"` that prints "setup" and yields the string "data". Write three tests that use it. Run with `-s`. How many times does "setup" print? *(Once.)*

**Exercise 2.** Change the scope to `function` and re-run. What changes? *(Prints three times.)*

**Exercise 3.** Write this code and predict the result before running:

```python
import pytest

@pytest.fixture
def small():
    return 1

@pytest.fixture(scope="module")
def big(small):
    return small
```

*Answer:* a `ScopeMismatch` error, because a module fixture cannot use a function fixture. Fix by changing `small` to module scope.

**Exercise 4.** Use `pytest --setup-show` on `test_scopes_demo.py` and identify which letter marks each fixture's scope. 

**Exercise 5.** Fix the shared-list bug from section 7 by (a) making the fixture function-scoped, and (b) keeping it module-scoped but adding a clearing fixture.

*Hint for (b):* create `@pytest.fixture` `clean_list(shared_list)` that calls `shared_list.clear()` before `yield shared_list`.

**Exercise 6.** Write a session-scoped `autouse` fixture that records the start time using `time.time()` and prints the elapsed seconds in teardown. 

*Solution:*

```python
import time
import pytest

@pytest.fixture(scope="session", autouse=True)
def timer():
    start = time.time()
    yield
    print(f"\nTotal elapsed: {time.time() - start:.2f}s")
```

**Exercise 7 (Project 1 link).** Find one expensive-looking setup in your Project 1 tests (for example loading a data file) and move it to a module-scoped fixture while keeping a function-scoped reset fixture. Confirm tests pass individually and together.

## Summary

- Scope = lifetime = how often the fixture is created: `function` (default), `class`, `module`, `package`, `session`.
- Wider scope is faster but risks shared state; narrower scope is safer but slower.
- A fixture may only depend on fixtures of equal or wider scope; otherwise `ScopeMismatch`.
- Fixtures are lazy: created on first request. Teardown runs in reverse order, narrowest first.
- Pattern: expensive resource at wide scope + cheap reset fixture at function scope.
- Use `--setup-show` to inspect scope behaviour; use `tmp_path_factory` for wide-scope temp dirs.
- Next up: parametrization, which runs one test with many data sets.

## Additional Resources

- PyTest fixture scopes: https://docs.pytest.org/en/stable/how-to/fixtures.html#fixture-scopes
- Fixture reference (scope, autouse, dynamic scope): https://docs.pytest.org/en/stable/reference/fixtures.html
- `--setup-show` and other CLI options: https://docs.pytest.org/en/stable/reference/reference.html#command-line-flags
