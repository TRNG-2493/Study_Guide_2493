# 07 — Hooks and Fixtures

> **Before you start**
>
> - **By the end you can:** use setup/teardown hooks, write fixtures with `yield`, share fixtures in `conftest.py`, choose fixture scopes, and log in once with `storage_state`.
> - **Practice site:** Swag Labs — <https://www.saucedemo.com/>. Users `standard_user`, `problem_user`, `locked_out_user`; password `secret_sauce`.
> - **Create:** a folder `lecture07/` with the same `pytest.ini` and `conftest.py` as Lecture 2 (base URL + `data-test` setting). You'll add more to `conftest.py` today.
> - **Start each test file with:**
>
> ```python
> import pytest
> from playwright.sync_api import Page, expect
> ```
>
> - **Run tests with:** `pytest -s -v`

---

## Topic 1 — Setup and teardown hooks

### Definition

Hooks are specially named functions that pytest runs automatically **before** and **after** tests — the same idea as `setUp`/`tearDown` in unittest. With Playwright we use an **`autouse` fixture** instead, because hooks can't receive fixtures like `page`.

### Key ideas

| Hook | Runs |
|---|---|
| `setup_module` / `teardown_module` | Once per file |
| `setup_function` / `teardown_function` | Around each test function |
| `setup_class` / `teardown_class` | Once per class (`@classmethod`) |
| `setup_method` / `teardown_method` | Around each test method in a class |

- `def setup_method(self, page)` does **not** work — hooks can't get fixtures.
- `@pytest.fixture(autouse=True)` runs for every test **and** can use `page`.

### Worked example — see the order, then switch to `autouse`

**Step 1.** In `test_01_hooks.py`, add module and function hooks:

```python
def setup_module(module):
    print("\n>>> setup_module")

def teardown_module(module):
    print("<<< teardown_module")

def setup_function(function):
    print(f"  > before {function.__name__}")

def teardown_function(function):
    print(f"  < after {function.__name__}")
```

**Step 2.** Add two tests:

```python
def test_first():
    print("    running test_first")

def test_second():
    print("    running test_second")
```

> **Predict:** how many times will `setup_module` print?

**Step 3.** Run `pytest test_01_hooks.py -s`.

**Step 4.** Now the Playwright way — a class with an `autouse` fixture:

```python
class TestLoginPage:
    @pytest.fixture(autouse=True)
    def open_login_page(self, page):
        page.goto("/")

    def test_login_button(self, page):
        expect(page.get_by_role("button", name="Login")).to_be_visible()
```

### Checkpoint

```
>>> setup_module
  > before test_first
    running test_first
  < after test_first
  > before test_second
    running test_second
  < after test_second
...
<<< teardown_module
```

and `test_login_button` passes.

### Your turn

1. Add `setup_method` / `teardown_method` to the class and print messages. Where do they appear?
2. Add a second test to `TestLoginPage` that checks the title is "Swag Labs". Does it need its own `goto`?
3. Try `def setup_method(self, method, page):` and read the error.

---

## Topic 2 — Fixtures with `yield`

### Definition

A **fixture** prepares something a test needs and hands it over. With `yield`, everything before `yield` is setup, the test runs at the `yield`, and everything after is teardown — which runs **even if the test fails**.

### Key ideas

- `return` = setup only. `yield` = setup **and** teardown.
- Code after `return` never runs.
- Fixtures can use other fixtures, return a value, and run only for tests that ask for them.

### Worked example — a user fixture with cleanup

**Step 1.** A setup-only fixture with `return`, in `test_02_fixtures.py`:

```python
@pytest.fixture
def login_page(page):
    page.goto("/")
    return page


def test_title(login_page):
    expect(login_page).to_have_title("Swag Labs")
```

**Step 2.** A fixture with setup and teardown:

```python
@pytest.fixture
def test_user():
    user = {"username": "standard_user", "password": "secret_sauce"}
    print("\ncreated user")
    yield user
    print("cleaned up user")
```

**Step 3.** A test that uses it:

```python
def test_user_name(test_user):
    print("running test")
    assert test_user["username"] == "standard_user"
```

**Step 4.** Make the test fail on purpose (`== "problem_user"`) and run again.

> **Predict:** will "cleaned up user" still print when the test fails?

### Checkpoint

```
created user
running test
.cleaned up user
```

After Step 4 the test fails, **and** "cleaned up user" still prints.

### Your turn

1. Change `yield user` to `return user` and keep the print after it. What happens?
2. Write an `inventory_page` fixture that logs in, yields the page, then logs out in teardown (**Open Menu** → **Logout**).
3. List two advantages fixtures have over `setup_method`.

---

## Topic 3 — Custom fixtures and `conftest.py`

### Definition

`conftest.py` is a file that holds fixtures shared by every test in its folder and subfolders. pytest loads it automatically — tests **never import it**; they just ask for fixtures by name.

### Key ideas

- A lower `conftest.py` **overrides** a fixture with the same name higher up.
- Fixtures can build on other fixtures.
- **Factory fixture:** return a *function*, so a test can create several things.
- Handy built-ins: `tmp_path`, `tmp_path_factory`, `request`, `pytestconfig`; pytest-playwright adds `new_context`.

### Worked example — a logged-in page, shared by all tests

**Step 1.** At the bottom of `conftest.py`, add a login helper:

```python
from playwright.sync_api import expect


def log_in(page, username="standard_user"):
    page.goto("/")
    page.get_by_placeholder("Username").fill(username)
    page.get_by_placeholder("Password").fill("secret_sauce")
    page.get_by_role("button", name="Login").click()
    expect(page).to_have_url("https://www.saucedemo.com/inventory.html")
```

**Step 2.** Add a fixture that uses it:

```python
@pytest.fixture
def ui_logged_in_page(page):
    log_in(page)
    return page
```

**Step 3.** Build a second fixture on top of the first:

```python
@pytest.fixture
def page_with_two_items(ui_logged_in_page):
    ui_logged_in_page.get_by_test_id("add-to-cart-sauce-labs-backpack").click()
    ui_logged_in_page.get_by_test_id("add-to-cart-sauce-labs-onesie").click()
    return ui_logged_in_page
```

**Step 4.** Use them in `test_03_conftest.py` — **no import**:

```python
def test_products_title(ui_logged_in_page):
    expect(ui_logged_in_page.get_by_test_id("title")).to_have_text("Products")


def test_two_items(page_with_two_items):
    expect(page_with_two_items.get_by_test_id("shopping-cart-badge")).to_have_text("2")
```

> **Predict:** what error do you get if you add `from conftest import log_in` and run from another folder?

### Checkpoint

`2 passed`.

### Your turn

1. Write a factory fixture `login_as` that takes a username and returns a logged-in page in a **new context**.
   *Hint: ask for `new_context`; inside, `page = new_context().new_page()`, then `log_in(page, username)`.*
2. Use it to log in as `standard_user` **and** `problem_user` in the same test. Add an item for one user — does the other user's cart change?
3. Print `request.node.name` from a fixture.

### Common errors

| Error | Fix |
|---|---|
| `from conftest import ...` | Don't import; ask for the fixture by name |
| `fixture 'x' not found` | `conftest.py` is in the wrong folder |

---

## Topic 4 — Fixture scopes

### Definition

A fixture's **scope** controls how often it is created: once per test (`function`, the default), per class, per file (`module`), or once for the whole run (`session`).

### Key ideas

| Scope | Created once per… | Typical use |
|---|---|---|
| `function` | Test | `page`, data tests change |
| `class` | Test class | Shared setup for a group |
| `module` | File | Read a data file once |
| `session` | Whole run | Browser, saved login |

- Wider = **faster**; narrower = **safer**.
- Share things that are expensive and **never change**.
- A fixture can't use a fixture with a **narrower** scope → `ScopeMismatch`.

### Worked example — shared data leaks between tests

**Step 1.** Two fixtures with different scopes, in `test_04_scopes.py`:

```python
@pytest.fixture
def function_cart():
    return {"items": []}


@pytest.fixture(scope="module")
def module_cart():
    return {"items": []}
```

**Step 2.** The first test changes both:

```python
def test_a(function_cart, module_cart):
    function_cart["items"].append("Backpack")
    module_cart["items"].append("Backpack")
```

**Step 3.** The second test checks them:

```python
def test_b(function_cart, module_cart):
    function_cart["items"].append("Onesie")
    module_cart["items"].append("Onesie")
    assert function_cart["items"] == ["Onesie"]
    assert module_cart["items"] == ["Backpack", "Onesie"]
```

> **Predict:** what happens if you run only `test_b` with `-k test_b`?

### Checkpoint

`2 passed` — the module-scoped cart still contains `"Backpack"` from the previous test.

### Your turn

1. Add `print("creating module_cart")` inside `module_cart`. How many times does it print?
2. Write a session fixture that asks for `page`. Read the `ScopeMismatch` error.
3. For each, choose a scope: a page object, a JSON file of test data, a saved login file.

### Common errors

| Error | Fix |
|---|---|
| `ScopeMismatch ... function scoped fixture page` | Use `browser` and create your own context |
| Tests pass alone but fail together | Shared mutable data; use function scope |

---

## Topic 5 — Browser contexts and saved login state

### Definition

`storage_state` saves a browser context's cookies and `localStorage` to a JSON file. A new context created from that file starts **already logged in** — so you log in once per run instead of once per test.

### Key ideas

- Every test still gets its **own** context (independent), but skips the UI login.
- Save once in a **session** fixture (uses `browser`); load in a **function** fixture (uses `new_context`).
- The file holds real login tokens — keep it out of Git (`.gitignore`).
- `browser_context_args` changes settings for every context; always keep `**browser_context_args`.

### Worked example — log in once, reuse everywhere

**Step 1.** In `conftest.py`, log in once and save the state:

```python
@pytest.fixture(scope="session")
def user_state(browser, base_url, tmp_path_factory):
    context = browser.new_context(base_url=base_url)
    page = context.new_page()
    log_in(page)
```

**Step 2.** Save it to a file and close the context:

```python
    state_file = tmp_path_factory.mktemp("auth") / "standard_user.json"
    context.storage_state(path=state_file)
    context.close()
    return state_file
```

**Step 3.** A per-test fixture that loads it:

```python
@pytest.fixture
def logged_in_page(new_context, user_state):
    context = new_context(storage_state=user_state)
    page = context.new_page()
    page.goto("/inventory.html")
    return page
```

**Step 4.** Three tests in `test_05_login_state.py`:

```python
def test_title(logged_in_page):
    expect(logged_in_page.get_by_test_id("title")).to_have_text("Products")

def test_add_to_cart(logged_in_page):
    logged_in_page.get_by_test_id("add-to-cart-sauce-labs-backpack").click()
    expect(logged_in_page.get_by_test_id("shopping-cart-badge")).to_have_text("1")

def test_cart_starts_empty(logged_in_page):
    expect(logged_in_page.get_by_test_id("shopping-cart-badge")).to_be_hidden()
```

**Step 5.** Compare timings:

```bash
pytest test_05_login_state.py --durations=0
```

> **Predict:** `test_add_to_cart` runs before `test_cart_starts_empty`. Will the cart still be empty?

### Checkpoint

`3 passed`. Only the first test's setup includes the login; the others start straight on `/inventory.html`.

### Your turn

1. Print the contents of the saved JSON file. Find the `session-username` cookie.
2. Create a `problem_user_state` fixture and a `problem_page` fixture.
3. Override `browser_context_args` in `conftest.py` to use a 1280×720 viewport and `locale="en-GB"`.
   *Hint: start with `return {**browser_context_args, ...}`.*

### Common errors

| Error | Fix |
|---|---|
| Sent back to the login page in every test | You forgot `storage_state=` when creating the context |
| `base_url` stops working after overriding `browser_context_args` | Include `**browser_context_args` |
| State file committed to Git | Add its folder to `.gitignore` |

---

## Stretch challenge

Write one test that uses `login_as` to open a `standard_user` page and a `problem_user` page side by side, adds an item to the first user's cart, and checks the second user's cart badge is hidden. Explain in a comment why they don't affect each other.

## Exit ticket

1. Why can't `setup_method` open a page with Playwright?
2. Where does teardown code go in a fixture, and when does it run?
3. Why is the saved-login fixture session-scoped, while `logged_in_page` is function-scoped?

## Cheat sheet

| Code | Purpose |
|---|---|
| `setup_function` / `teardown_function` | xunit hooks (no fixtures) |
| `@pytest.fixture(autouse=True)` | Run for every test, can use `page` |
| `@pytest.fixture` + `return` | Setup only |
| `@pytest.fixture` + `yield` | Setup + teardown |
| `conftest.py` | Shared fixtures, no imports |
| `def fixture_b(fixture_a):` | Fixture uses fixture |
| `def factory(): def _make(x): ...; return _make` | Factory fixture |
| `@pytest.fixture(scope="session")` | Create once per run |
| `tmp_path_factory.mktemp("auth")` | Temp folder for session fixtures |
| `context.storage_state(path=file)` | Save login state |
| `new_context(storage_state=file)` | Load login state |
| `browser_context_args` override | Settings for every context |
| `pytest --durations=0` | Show timings |
