# Interview Questions: Week 4 - PyTest-Playwright - Tuesday

Topic of the day: PyTest Advanced Features (fixtures, scopes, parametrization, combining the two, conftest.py, sharing fixtures, mocking with unittest.mock).

How to use this bank: read the question, answer out loud in 30 to 60 seconds, then reveal the answer and check that your answer contains the keywords.

## Beginner (Foundational)

### Q1: What is a fixture in PyTest, and what problem does it solve?
**Keywords:** `@pytest.fixture`, setup, teardown, DRY, injection
**Hint:** Think about what happens when ten tests all start with the same three lines.
<details>
<summary>Click to Reveal Answer</summary>

A fixture is a function decorated with `@pytest.fixture` that PyTest runs for you to prepare something a test needs (the arrange step) and, optionally, to clean up afterwards. A test requests it simply by naming it as a parameter, and PyTest injects the returned value (dependency injection). It solves repeated setup, which violates DRY, and forgotten cleanup, because teardown code in a fixture still runs when a test fails halfway. By default a fixture runs once per test, so each test gets a fresh object.

```python
@pytest.fixture
def filled_cart():
    cart = ShoppingCart()
    cart.add("pen", 2.0, 3)
    return cart

def test_total(filled_cart):      # PyTest calls the fixture and passes the result
    assert filled_cart.total() == 6.0
```
</details>

---

### Q2: Explain the difference between `return` and `yield` in a fixture. When would you use each?
**Keywords:** `return`, `yield`, teardown, cleanup, runs after the test
**Hint:** Which one leaves you a place to put cleanup code?
<details>
<summary>Click to Reveal Answer</summary>

With `return` the fixture function ends and you only get setup, so there is nowhere to put cleanup. With `yield`, PyTest pauses the fixture at the `yield`, injects the yielded value, runs the test, and then resumes the fixture so the code after the `yield` acts as teardown. That teardown runs whether the test passed or failed. I use `return` for plain data and `yield` for resources like files, connections, or browsers that must be closed. If several fixtures are involved, teardown happens in reverse order of setup.

```python
@pytest.fixture
def log_file(tmp_path):
    handle = open(tmp_path / "run.log", "w")   # setup
    yield handle                               # test runs here
    handle.close()                             # teardown
```
</details>

---

### Q3: What does `autouse=True` do on a fixture, and why should you use it sparingly?
**Keywords:** `autouse`, automatic, hidden dependency, readability, global state
**Hint:** Does the test need to name the fixture?
<details>
<summary>Click to Reveal Answer</summary>

With `autouse=True` every test in the fixture's scope uses the fixture automatically, without naming it as an argument. It is good for things like resetting global state, setting up logging, or setting an environment variable for every test. The downside is that it is hidden magic: readers cannot see from the test signature what it depends on. So I would never use it to create objects the test needs; those should be explicit arguments so the test documents its own dependencies.

```python
@pytest.fixture(autouse=True)
def banner():
    print("--- test starting ---")
    yield
    print("--- test finished ---")
```
</details>

---

### Q4: What are the five fixture scopes, which is the default, and what is the trade-off when choosing one?
**Keywords:** `function`, `class`, `module`, `package`, `session`
**Hint:** Narrowest to widest.
<details>
<summary>Click to Reveal Answer</summary>

From narrowest to widest the scopes are `function`, `class`, `module`, `package`, and `session`, and `function` is the default. Scope controls how long a fixture's value lives and so how often it is created: function means before each test, module means once per test file, session means once per whole `pytest` run. A wider scope is faster because expensive work is done once, but tests can influence each other through shared state, which is harder to debug. The rule of thumb is to use the narrowest scope that keeps the suite fast enough, and widen only for things that are expensive and read-only or safely resettable.

```python
@pytest.fixture(scope="session")
def api_token():
    return "abc123-token"      # requested once per run
```
</details>

---

### Q5: What is a `ScopeMismatch` error and how do you fix it?
**Keywords:** `ScopeMismatch`, same or wider scope, session, function
**Hint:** Which fixture lives longer, and what would it be holding?
<details>
<summary>Click to Reveal Answer</summary>

A fixture can only request fixtures with the same or a wider scope. If a `session` fixture requests a `function` fixture, PyTest raises `ScopeMismatch`, because the long-lived fixture would hold an object that is destroyed after each test. The fix is to make the dependency wider scoped, or make the dependent fixture narrower. The opposite direction is fine: a function-scoped fixture may request a session-scoped one.

```python
@pytest.fixture
def per_test(): return 1

@pytest.fixture(scope="session")
def long_lived(per_test):   # ScopeMismatch: session cannot use function
    return per_test + 1
```
</details>

---

### Q6: Explain the two meanings of "sharing a fixture": sharing the definition versus sharing the value.
**Keywords:** definition, value, scope, code reuse, same object
**Hint:** One is about code reuse, the other is about performance and danger.
<details>
<summary>Click to Reveal Answer</summary>

Sharing the definition means many tests can use the same fixture function, and because the default scope is function, each test still gets its own fresh result. That is about code reuse, and where you put the fixture (module, `conftest.py`, and so on) decides who can see it. Sharing the value means many tests receive the same object because the fixture has a wider scope. That is about performance, and it is dangerous if the object is mutable. I should always be clear which one I intend: location decides the first, scope decides the second.
</details>

---

### Q7: What does `@pytest.mark.parametrize` do, and how are the argument names matched?
**Keywords:** parameter set, names string, list of tuples, separate tests, exact names
**Hint:** One function, many tests.
<details>
<summary>Click to Reveal Answer</summary>

Parametrization generates several tests from one test function and a table of data, so adding a case means adding one row, not a new function. The first argument is a comma-separated string of names, and those must match the function's parameter names exactly. The second is a list of tuples, where each tuple is one parameter set and values are matched to names by position. Each set is reported as its own test, so one failing case does not hide the others.

```python
@pytest.mark.parametrize("age, expected", [(17, False), (18, True), (19, True)])
def test_is_adult(age, expected):
    assert is_adult(age) is expected   # 3 tests generated
```
</details>

---

### Q8: How do you make parametrized test IDs readable, and what can `pytest.param` add to an individual case?
**Keywords:** `ids`, `pytest.param`, `id=`, `marks`, `xfail`
**Hint:** Auto IDs like `[0-False]` are cryptic.
<details>
<summary>Click to Reveal Answer</summary>

You can pass `ids=[...]` (a list of the same length as the data, or a function) so reports show names like `[just-below-limit]`. For finer control, wrap one case in `pytest.param(..., id="...")`. `pytest.param` can also attach `marks` to that single case, such as `skip`, `xfail` (with a `reason` and optionally `raises=`), or a custom marker like `slow`. The other cases in the table are unaffected.

```python
@pytest.mark.parametrize("age, expected", [
    pytest.param(17, False, id="below-18"),
    pytest.param(-1, False, id="negative-bug",
                 marks=pytest.mark.xfail(reason="raises ValueError", raises=ValueError)),
])
def test_is_adult(age, expected):
    assert is_adult(age) is expected
```
</details>

---

### Q9: What happens when you stack two `parametrize` decorators? How many tests are generated?
**Keywords:** stacking, Cartesian product, multiply, combinations, bottom decorator
**Hint:** Think multiplication, not addition.
<details>
<summary>Click to Reveal Answer</summary>

Stacked `parametrize` decorators produce the Cartesian product, meaning every combination of the values. With `x` in `[1, 2, 3]` and `y` in `[10, 20]` you get 3 x 2 = 6 tests, and the bottom decorator's value appears first in the ID (for example `[10-1]`). It is useful for independent dimensions such as browser by screen size. The caution is that combinations grow multiplicatively: three decorators with 10 values each give 1,000 tests, so check the count with `pytest --collect-only -q`.

```python
@pytest.mark.parametrize("x", [1, 2, 3])
@pytest.mark.parametrize("y", [10, 20])
def test_mult(x, y): ...          # 6 tests: [10-1], [10-2], [10-3], [20-1], ...
```
</details>

---

### Q10: Explain the difference between `@pytest.mark.parametrize` and a parametrized fixture (`@pytest.fixture(params=...)`).
**Keywords:** reach, one test, every test, `request.param`, hidden multiplication
**Hint:** Who gets the extra runs?
<details>
<summary>Click to Reveal Answer</summary>

`@pytest.mark.parametrize` applies to one test function (or class), and the data is visible right at the test, which makes it ideal for input/expected tables. A parametrized fixture applies to every test that uses the fixture, so the same test suite automatically runs under each variant, for example each browser or database. The fixture reads the current value through `request.param`. The trade-off is that the data and the multiplication are hidden in the fixture, so readers can be surprised; `--setup-show` and `--collect-only -q` help inspect it.

```python
@pytest.fixture(params=["chrome", "firefox", "webkit"])
def browser_name(request):
    return request.param      # every test using it runs 3 times
```
</details>

---

### Q11: What is `conftest.py` and why does PyTest treat it specially?
**Keywords:** auto-loaded, no import, fixtures, hooks, directory tree
**Hint:** Do tests ever `import` from it?
<details>
<summary>Click to Reveal Answer</summary>

`conftest.py` is an ordinary Python file with a special name that PyTest looks for and loads automatically while collecting tests. Fixtures, hooks (functions named `pytest_...`), and helper code defined in it are available to tests in that directory and all subdirectories, and you never import it. It is not a test file, so PyTest does not collect tests from it. Putting a shared fixture there removes the need to copy it into every test file. The file name must be exactly `conftest.py`; a misspelling silently does nothing.
</details>

---

### Q12: How do multiple `conftest.py` files interact? What happens when two define a fixture with the same name?
**Keywords:** hierarchy, closest wins, override, siblings, parent fixture
**Hint:** Think of a tree: which fixtures can a test see?
<details>
<summary>Click to Reveal Answer</summary>

A test sees fixtures from its own folder's `conftest.py` and every parent up to the rootdir. If two levels define the same fixture name, the closest one to the test wins, so the child overrides the parent. Sibling folders do not see each other's conftest, so `api/` cannot use fixtures defined in `unit/conftest.py`. A child can also extend rather than replace the parent by requesting the fixture of the same name as an argument. A test module's own definition is nearer than any conftest and overrides it too.

```python
# tests/unit/conftest.py
@pytest.fixture
def greeting(greeting):                 # takes the parent's greeting as input
    return greeting + " (unit-flavoured)"
```
</details>

---

### Q13: What is a test double? Explain the difference between a stub, a fake, and a mock.
**Keywords:** test double, stub, fake, mock, verify calls
**Hint:** Which one records how it was used?
<details>
<summary>Click to Reveal Answer</summary>

A test double is any object that stands in for a real dependency during a test, like a stunt double. A stub returns canned answers (for example `get_price()` always returns 9.99). A fake is a simplified working implementation, such as an in-memory dictionary instead of a database. A mock records how it was used so you can verify interactions, such as "was `send_email` called once with the right address?". A dummy just fills a parameter, and a spy wraps a real object to record calls. In everyday talk people say "mock" for all of them, and `unittest.mock.Mock` can play the stub, mock, and spy roles.
</details>

---

### Q14: What is the difference between `return_value` and `side_effect` on a mock?
**Keywords:** `return_value`, `side_effect`, exception, sequence, function
**Hint:** One always gives the same answer; the other is more flexible.
<details>
<summary>Click to Reveal Answer</summary>

`return_value` always returns the same thing when the mock is called. `side_effect` is more flexible and has three forms: give it an exception and the mock raises it, give it an iterable and the mock returns a different value on each call, or give it a function to compute the result. If an item in an iterable is an exception, that exception is raised at that call, which is perfect for "fail twice then succeed" retry tests. A fourth call on a three-item list raises `StopIteration`.

```python
boom = Mock(side_effect=ConnectionError("network down"))   # raises when called
seq  = Mock(side_effect=[1, 2, 3])                          # seq() -> 1, then 2, then 3
```
</details>

---

## Intermediate (Application)

### Q15: Your fixture builds a complex object from a simple value, and you want to choose that value in the test's parametrize table. How do you do it, and what error do you see if you forget?
**Keywords:** `indirect`, `request.param`, fixture name, explicit list, `AttributeError`
**Hint:** The value must go through the fixture first, not straight to the test.
<details>
<summary>Click to Reveal Answer</summary>

I use `indirect`. The parametrize argument name matches the fixture name, and `indirect=["cart_with_qty"]` tells PyTest to deliver each value to the fixture as `request.param` and give the test whatever the fixture returns. Arguments not listed, like `expected`, are passed straight to the test. I prefer the explicit list over `indirect=True` when mixing raw and fixture-backed arguments. This keeps the table short (`1, 3, 10`) while building logic and teardown stay in the fixture. If I forget `indirect`, the raw value reaches the test and I typically see something like `AttributeError: 'int' object has no attribute ...`.

```python
@pytest.fixture
def cart_with_qty(request):
    cart = ShoppingCart()
    cart.add("pen", 2.0, request.param)
    return cart

@pytest.mark.parametrize("cart_with_qty, expected", [(1, 2.0), (3, 6.0)],
                         indirect=["cart_with_qty"])
def test_total(cart_with_qty, expected):
    assert cart_with_qty.total() == pytest.approx(expected)
```
</details>

---

### Q16: Creating a database connection takes seconds, but your tests insert rows and must not see each other's data. How do you design the fixtures?
**Keywords:** session scope, function scope, reset fixture, wide resource, isolation
**Hint:** Two fixtures, two different scopes.
<details>
<summary>Click to Reveal Answer</summary>

I use the "wide resource plus narrow reset" pattern. The expensive connection goes in a `session`-scoped fixture so it is made once and torn down at the end. On top of it I add a function-scoped fixture that requests the connection, clears the data before the test, yields it, and clears again afterwards. This is allowed because a narrow fixture may depend on a wide one. Tests stay independent and order-proof, and I keep the speed benefit. Playwright does something similar: one browser, a fresh context per test.

```python
@pytest.fixture(scope="session")
def database():
    db = FakeDatabase()
    yield db

@pytest.fixture
def clean_db(database):        # function scope, runs for each test
    database.clear()
    yield database
    database.clear()
```
</details>

---

### Q17: You patched `requests.get` but your test still hits the real function. The module under test does `from requests import get`. What went wrong and how do you fix it?
**Keywords:** patch where looked up, namespace, `from ... import`, own reference, `patch("module_a.get")`
**Hint:** Where does the name `get` live after a `from` import?
<details>
<summary>Click to Reveal Answer</summary>

The golden rule is to patch the name where it is looked up, not where it is defined. After `from requests import get`, the name `get` lives inside that module's own namespace, so patching `requests.get` changes the original but the module still holds its own reference to the real function. The fix is to patch the name in the module under test, for example `patch("module_a.get")`. If the module did `import requests` and called `requests.get(...)`, the lookup happens at call time on the shared module object, so patching `requests.get` would also work. The safest habit is to patch the name in the namespace of the code under test.

```python
# module_a.py:  from requests import get
with patch("module_a.get", return_value=fake_response):
    result = module_a.load()
```
</details>

---

### Q18: A session-scoped fixture returns a template dict that tests then modify, and tests start failing depending on order. How do you fix it while keeping one shared template?
**Keywords:** mutable, `copy.deepcopy`, function-scoped wrapper, order-dependent, immutable
**Hint:** Keep the template shared, but give each test its own copy.
<details>
<summary>Click to Reveal Answer</summary>

A wide-scoped fixture that returns a mutable object is shared by reference, so one test's changes leak into later tests and failures depend on test order. My options are to return immutable data (tuples, `frozenset`, `types.MappingProxyType` read-only dict), or keep the session-scoped template and add a function-scoped fixture that returns `copy.deepcopy` of it. I use `deepcopy` and not `copy.copy` because a shallow copy would still share nested objects like an inner list. With that, both tests pass in any order. The leading underscore on the template name signals "do not request directly".

```python
@pytest.fixture(scope="session")
def _template_user():
    return {"name": "Template", "tags": ["a", "b"]}

@pytest.fixture
def user(_template_user):
    return copy.deepcopy(_template_user)
```
</details>

---

### Q19: Your team wants slow tests skipped by default but runnable with a `--runslow` flag. How do you implement this in PyTest?
**Keywords:** `pytest_addoption`, `pytest_collection_modifyitems`, `item.keywords`, skip marker, top-level conftest
**Hint:** Two hooks in the top-level conftest.
<details>
<summary>Click to Reveal Answer</summary>

In the top-level `conftest.py` I register the option with the `pytest_addoption` hook, which must be top-level so PyTest knows the option before parsing the command line. Then in `pytest_collection_modifyitems(config, items)` I check the option: if `--runslow` is given I return without changing anything; otherwise I loop over `items` and add a skip marker to every test whose `item.keywords` contains `slow`. I also register the `slow` marker so there is no unknown-marker warning. Running `pytest -rs` shows the skipped tests with the reason and `pytest --runslow` runs them.

```python
def pytest_addoption(parser):
    parser.addoption("--runslow", action="store_true", default=False,
                     help="run tests marked slow")

def pytest_collection_modifyitems(config, items):
    if config.getoption("--runslow"):
        return
    skip_slow = pytest.mark.skip(reason="need --runslow to run")
    for item in items:
        if "slow" in item.keywords:
            item.add_marker(skip_slow)
```
</details>

---

## Advanced (Deep Dive)

### Q20: A module-scoped fixture has `params=["db_a", "db_b"]` and the file has two tests that use it. In what order do setup, tests, and teardown happen, and how many times does the fixture connect?
**Keywords:** module scope, parametrized fixture, once per param, reordering, grouping
**Hint:** Think about how PyTest minimizes the number of setups.
<details>
<summary>Click to Reveal Answer</summary>

A module-scoped parametrized fixture is created once per parameter value per module, and PyTest deliberately reorders the tests to group them by parameter and minimise setups. So the order is: connect `db_a`, run `test_one[db_a]` and `test_two[db_a]`, disconnect `db_a`, then connect `db_b`, run `test_one[db_b]` and `test_two[db_b]`, disconnect `db_b`. The fixture connects only twice, not four times. With function scope there is no such grouping, because the fixture would be rebuilt around every test anyway. I would confirm it with `pytest -s -v` or `--setup-show`, which shows the param in brackets, such as `SETUP M database['db_a']`.

```python
@pytest.fixture(scope="module", params=["db_a", "db_b"])
def database(request):
    print(f"[connect {request.param}]")
    yield request.param
    print(f"[disconnect {request.param}]")
```
</details>

---

## Coverage Table

| Lesson | Question numbers |
|--------|------------------|
| fixtures.md | Q1, Q2, Q3 |
| fixture-scopes.md | Q4, Q5, Q16 |
| parametrization.md | Q7, Q8, Q9 |
| combining-fixtures-and-parametrization.md | Q10, Q15, Q20 |
| conftest-py.md | Q11, Q12, Q19 |
| sharing-fixtures-across-tests.md | Q6, Q18 |
| mocking-with-unittest-mock.md | Q13, Q14, Q17 |

Distribution: 14 Beginner (70%), 5 Intermediate (25%), 1 Advanced (5%) = 20 questions.
