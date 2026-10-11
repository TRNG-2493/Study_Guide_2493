# Fixtures and Custom Fixtures

## Learning Objectives

By the end of this lesson you will be able to:

- Explain, in plain language, what a pytest fixture is and what problem it solves.
- Use the built-in fixtures that `pytest-playwright` gives you (`page`, `context`, `browser`, `playwright`, `browser_name`, `base_url`, and others) without writing any setup code yourself.
- Write your own fixtures with the `@pytest.fixture` decorator, including fixtures that **return** a value and fixtures that **yield** a value so they can clean up afterwards.
- Choose the correct fixture **scope** (`function`, `class`, `module`, `package`, `session`) and recognise the `ScopeMismatch` error.
- Share fixtures across many test files by placing them in `conftest.py`.
- Customise how Playwright launches browsers and creates contexts by overriding `browser_type_launch_args` and `browser_context_args`.
- Build fixtures that depend on other fixtures (composition), parameterised fixtures, "factory" fixtures, and `autouse` fixtures.
- Create a reusable **logged-in state** fixture using Playwright's `storage_state`, so you do not log in through the UI before every single test.
- Inspect and debug fixtures with `pytest --fixtures` and `pytest --setup-show`.

---

## Why This Matters

Over the last two days you learned how to drive complicated UI behaviour with Playwright: dialogs, form controls, keyboard and mouse actions on Monday; frames, tables, date pickers, multiple tabs, shadow DOM, dynamic elements, navigation events and file transfer on Tuesday. Every one of those scripts started with the same boilerplate: start Playwright, launch a browser, create a context, open a page, do the work, close everything. If you wrote that boilerplate in every test, a 50-test suite would contain 50 copies of it, and changing one detail (say, "run with a bigger viewport") would mean editing 50 places.

This week's epic is to **structure** your Playwright tests so they are maintainable: fixtures, hooks, the Page Object Model, data-driven tests, retries, and reporting. Fixtures are the foundation of all of that. Today's other topics (hooks, page objects, JSON data, retries, reports) are all wired together *through* fixtures:

- The **page objects** you will build later today are handed to your tests by fixtures.
- The **JSON test data** is loaded by fixtures and parameterisation.
- The **hooks** that take screenshots on failure rely on the `page` fixture.
- The **retry** and **reporting** plug-ins interact with fixture setup and teardown.

This also directly supports **Project 1 - QE Foundations**. The Project 1 UI milestone for this week is to turn a set of working UI tests into a clean, maintainable test framework. A reviewer looking at your repository will immediately judge its quality by whether the browser lifecycle is handled by fixtures in `conftest.py` rather than copy-pasted into each test. Good fixtures are the clearest signal that you think like a Quality Engineer who builds frameworks, not just scripts.

> **A note on vocabulary.** The word "fixture" is used in more than one tool. In this lesson it always means a **pytest fixture**. Cypress, which we cover in depth on Thursday, also has something it calls "fixtures" (static data files), which is a different idea. Do not mix them up.

---

## The Concept

### 1. The problem fixtures solve

Imagine you are testing the login of `https://www.saucedemo.com`. Here is a first, "naive" test written with the Playwright **sync API** and no pytest-Playwright help at all:

```python
# test_naive_login.py
from playwright.sync_api import sync_playwright, expect


def test_standard_user_can_log_in():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        context = browser.new_context()
        page = context.new_page()

        page.goto("https://www.saucedemo.com")
        page.locator("#user-name").fill("standard_user")
        page.locator("#password").fill("secret_sauce")
        page.locator("#login-button").click()

        expect(page).to_have_url("https://www.saucedemo.com/inventory.html")

        context.close()
        browser.close()
```

This works. But look at what is wrong with scaling it:

1. **Repetition.** The first three lines and the last two lines have nothing to do with "logging in". They would appear in every test.
2. **Leaks on failure.** If `expect(...)` fails, the exception is raised *before* `context.close()` and `browser.close()`. The `with` block saves us here, but if we had written manual `p.chromium.launch()` calls, the browser process would be left open.
3. **Slow.** Launching a browser for every test is expensive. Ideally one browser is launched for the whole run, and each test gets a **fresh, isolated context** (like a brand-new incognito profile), which is nearly instant to create.
4. **Hard to configure.** Want to run Firefox instead? Add a viewport? Record video? You must edit every test.

A **fixture** solves all four problems by moving *setup* and *teardown* out of the test and into a named, reusable, centrally-managed function.

### 2. What is a pytest fixture?

A fixture is a Python function, decorated with `@pytest.fixture`, that pytest runs **for you** to prepare something a test needs. You ask for a fixture simply by adding its name as a **parameter** of your test function. pytest sees the parameter name, finds the fixture with that name, runs it, and passes in the result.

An analogy: think of a restaurant. You (the test) just say "I'd like a table" (a parameter called `table`). You do not lay the tablecloth, fetch the cutlery, or clean up afterwards; the restaurant staff (pytest) does it. Different customers can ask for the same kind of table and each gets a clean one.

The smallest possible example, with no browser at all:

```python
import pytest


@pytest.fixture
def greeting():
    return "hello"


def test_greeting_is_hello(greeting):
    assert greeting == "hello"
```

Line by line:

- `import pytest` makes the `pytest` module available. The decorator lives in it.
- `@pytest.fixture` is a **decorator**. A decorator is a function that wraps another function to change its behaviour. This one tells pytest "do not treat the following function as a test; register it as a fixture".
- `def greeting():` defines the fixture. The function's **name** (`greeting`) is the name tests use to request it.
- `return "hello"` is the value that will be injected into tests.
- `def test_greeting_is_hello(greeting):` is a normal test (name starts with `test_`). The parameter `greeting` matches the fixture's name, so pytest calls `greeting()` first and passes the return value in.
- `assert greeting == "hello"` uses the plain Python `assert` statement, which pytest enhances with detailed failure messages.

You never call `greeting()` yourself. This idea, **dependency injection** (the framework supplies what you declare you need), is the heart of pytest.

### 3. Built-in fixtures from `pytest-playwright`

When you install the plugin:

```bash
pip install pytest-playwright
playwright install        # downloads Chromium, Firefox and WebKit browsers
```

pytest automatically discovers the plugin and makes a family of fixtures available. You do not import them; they simply exist. The most important ones:

| Fixture | Scope | What you get |
|---|---|---|
| `playwright` | session | The top-level Playwright object (what `sync_playwright()` gave you). Useful for `playwright.request`, `playwright.selectors`, `playwright.devices`. |
| `browser_type` | session | The browser type selected by `--browser` (`chromium`, `firefox`, `webkit`). |
| `browser` | session | One launched `Browser`. Shared by all tests in the run, so launching happens once. |
| `browser_name` | session | The string name of the current browser, e.g. `"chromium"`. |
| `browser_channel` | session | The `--browser-channel` value (e.g. `"chrome"`, `"msedge"`) or `None`. |
| `browser_type_launch_args` | session | A `dict` of keyword arguments used to launch the browser (e.g. `headless`, `slow_mo`). **You can override this.** |
| `browser_context_args` | session | A `dict` of keyword arguments used to create every context (e.g. `viewport`, `locale`, `storage_state`). **You can override this.** |
| `new_context` | function | A *factory function*: call it with keyword arguments to create an extra context in a test (for example, two users at once). |
| `context` | function | A fresh `BrowserContext` for **each test**, created from `browser_context_args`. |
| `page` | function | A fresh `Page` inside that context for **each test**. This is the one you use most. |
| `is_chromium`, `is_firefox`, `is_webkit` | session | Booleans for browser-specific logic. |
| `base_url` | session | The value of `--base-url` (or the `base_url` ini option), or `None`. Provided by the `pytest-base-url` plug-in that `pytest-playwright` depends on. |
| `connect_options` | session | Options if connecting to a remote browser. Rarely needed at this stage. |

Because `browser` is **session** scoped and `context`/`page` are **function** scoped, you get both speed (one browser process) and isolation (a new context per test, so cookies and local storage never leak between tests). This is the correct trade-off and it is why you almost never need to launch browsers yourself.

Here is the naive test rewritten using the built-in `page` fixture:

```python
# tests/test_login_builtin.py
from playwright.sync_api import Page, expect


def test_standard_user_can_log_in(page: Page):
    page.goto("https://www.saucedemo.com")
    page.locator("#user-name").fill("standard_user")
    page.locator("#password").fill("secret_sauce")
    page.locator("#login-button").click()

    expect(page).to_have_url("https://www.saucedemo.com/inventory.html")
```

Line by line:

- `from playwright.sync_api import Page, expect` imports the `Page` *type* (so your editor can auto-complete methods) and `expect`, Playwright's web-first assertion helper (it auto-retries until the condition is true or it times out; this was covered when you learned about waiting and assertions earlier in the course).
- `def test_standard_user_can_log_in(page: Page):` asks pytest for the `page` fixture. The `: Page` after the name is a **type hint**. It does not change behaviour; it only helps tools and humans understand what `page` is.
- The next four lines are the real test; all the browser plumbing is gone.
- Cleanup happens automatically: when the test ends (pass or fail), pytest-playwright closes the context.

Run it:

```bash
pytest tests/test_login_builtin.py            # headless Chromium by default
pytest tests/test_login_builtin.py --headed   # watch the browser
pytest tests/test_login_builtin.py --browser firefox --browser webkit   # run in two browsers
```

The most useful command-line options pytest-playwright adds are: `--headed`, `--browser`, `--browser-channel`, `--slowmo` (milliseconds between actions), `--device` (emulate a device, e.g. `--device "iPhone 13"`), `--output` (folder for artefacts), `--tracing`, `--video`, `--screenshot`, and `--base-url`. We use several of these in the Reporting lesson.

### 4. Returning vs. yielding: setup and teardown in one function

A fixture that uses `return` can only do **setup**. If you also need **teardown** (cleanup), use `yield` instead. Everything before `yield` is setup; the yielded value is given to the test; everything after `yield` runs after the test finishes, **even if the test failed**.

```python
import pytest


@pytest.fixture
def temp_user():
    user = create_user_via_api()      # setup: runs BEFORE the test
    yield user                        # the test receives `user`
    delete_user_via_api(user["id"])   # teardown: runs AFTER the test
```

Think of `yield` as a pause button. pytest runs the fixture up to `yield`, hands the value to the test, runs the test, then un-pauses the fixture to run the rest.

Teardown order is the **reverse** of setup order, like unstacking plates: if the test requested fixture A then fixture B, B is torn down first, then A. This matters when B depends on A (for example, a "page" depends on a "context").

### 5. Scope: how long does a fixture live?

By default a fixture is created fresh for **every test function** that requests it (`scope="function"`). You can widen the scope to share one instance across many tests, trading isolation for speed.

| Scope | Created | Destroyed | Typical use |
|---|---|---|---|
| `function` (default) | once per test | after that test | Anything stateful: `page`, a fresh cart, a test record. |
| `class` | once per test class | after the last test in the class | A set of tests in a class that share expensive setup. |
| `module` | once per `.py` file | after the last test in the file | Per-file data, e.g. loaded config. |
| `package` | once per package (folder with `__init__.py`) | after the package's tests | Rare. |
| `session` | once per `pytest` run | at the very end | Browser launch, auth state, config, API tokens. |

You choose the scope with an argument:

```python
@pytest.fixture(scope="session")
def api_base_url():
    return "https://www.saucedemo.com"
```

**The golden rule of scope: a fixture can only depend on fixtures with the same or a wider scope.** A session-scoped fixture cannot request the function-scoped `page` fixture. If you try, pytest raises:

```
ScopeMismatch: You tried to access the function scoped fixture page with a session scoped request object
```

The logic is simple: the session fixture lives for the entire run, but `page` is destroyed after each test, so the session fixture would be holding a dead object. When you hit this error, either narrow the dependent fixture's scope or depend on something with a wider scope (for example, request `browser` instead of `page`, then create your own context).

### 6. `conftest.py`: sharing fixtures without importing them

If you define a fixture inside `test_a.py`, only tests in that file can use it. To share fixtures across files, put them in a special file named **`conftest.py`**. pytest loads it automatically; you never `import` from it. A `conftest.py` in the project root is visible to all tests; one inside `tests/checkout/` is visible only to tests in that folder (and below). Fixtures defined closer to the test **override** same-named fixtures from higher up. That makes it possible to specialise behaviour per folder.

A typical layout for our running example:

```
saucedemo_framework/
├── conftest.py              # fixtures shared by every test
├── pytest.ini               # configuration (base_url, markers, addopts)
├── pages/                   # page objects (next lessons)
├── data/                    # JSON test data (later lesson)
└── tests/
    ├── test_login.py
    └── checkout/
        ├── conftest.py      # fixtures only for checkout tests
        └── test_checkout.py
```

### 7. Overriding `browser_type_launch_args` and `browser_context_args`

Two session-scoped fixtures return dictionaries that are fed to Playwright. Because they are fixtures, you can **override** them in `conftest.py` to change how all tests run, without touching any test.

```python
# conftest.py
import pytest


@pytest.fixture(scope="session")
def browser_type_launch_args(browser_type_launch_args):
    # Take the dict pytest-playwright built (it includes CLI flags like --headed)
    # and return a new dict with our additions.
    return {
        **browser_type_launch_args,
        "slow_mo": 0,
        "args": ["--start-maximized"],
    }


@pytest.fixture(scope="session")
def browser_context_args(browser_context_args):
    return {
        **browser_context_args,
        "viewport": {"width": 1366, "height": 768},
        "locale": "en-US",
        "timezone_id": "America/New_York",
        "ignore_https_errors": True,
    }
```

Line by line:

- `@pytest.fixture(scope="session")` marks the fixture as session scoped, matching the scope of the one we override.
- `def browser_type_launch_args(browser_type_launch_args):` this looks odd: the fixture has the **same name as its own parameter**. That is intentional and legal. When a fixture in `conftest.py` has the same name as a fixture from a plug-in, the parameter refers to the **original (parent) version**. This lets you "extend" instead of "replace".
- `{**browser_type_launch_args, "slow_mo": 0, ...}` is **dictionary unpacking**. `**d` copies all key/value pairs from dictionary `d` into the new dictionary. Keys written afterwards override earlier keys with the same name. The result is the original options plus (or overriding) our additions.
- `viewport`, `locale`, `timezone_id`, and `ignore_https_errors` are all legitimate keyword arguments of `browser.new_context(...)`. Every context that pytest-playwright creates will use them.

You can also pass `storage_state`, `record_video_dir`, `permissions`, `geolocation`, `extra_http_headers`, `http_credentials`, and anything else `new_context` accepts.

**Why not just put these in the test?** Because they are *environment* decisions, not test logic. Centralising them follows the principle of "one reason to change": if the viewport requirement changes, you edit one fixture.

### 8. `base_url`: stop hard-coding hosts

Hard-coding `https://www.saucedemo.com` in every test makes it impossible to run the same suite against staging and production. pytest-playwright (through `pytest-base-url`) lets you set a base URL once. In `pytest.ini`:

```ini
[pytest]
base_url = https://www.saucedemo.com
```

or on the command line: `pytest --base-url https://staging.example.com`. With a base URL in place, `page.goto("/")` and `page.goto("/inventory.html")` are resolved relative to it, because pytest-playwright passes `base_url` into every new context. You can also request the `base_url` fixture directly in a test if you need the raw string.

### 9. Fixture composition (fixtures using fixtures)

Fixtures can request other fixtures exactly the way tests do. pytest builds a **dependency graph** and runs them in the right order.

```python
# conftest.py
import pytest
from playwright.sync_api import Page


@pytest.fixture
def login_page_open(page: Page) -> Page:
    """Opens the SauceDemo login screen and returns the page."""
    page.goto("/")
    return page


@pytest.fixture
def logged_in_page(login_page_open: Page) -> Page:
    """Logs in as the standard user and returns the page on the inventory screen."""
    login_page_open.locator("#user-name").fill("standard_user")
    login_page_open.locator("#password").fill("secret_sauce")
    login_page_open.locator("#login-button").click()
    login_page_open.wait_for_url("**/inventory.html")
    return login_page_open
```

Line by line:

- `login_page_open(page: Page) -> Page` requests the built-in `page` fixture, navigates to `"/"` (resolved against `base_url`), and returns the same page object. The text in triple quotes right under the `def` is a **docstring**; `pytest --fixtures` prints it, so write a clear one-liner.
- `logged_in_page(login_page_open: Page)` requests the previous fixture. So when a test asks for `logged_in_page`, pytest runs `page`, then `login_page_open`, then `logged_in_page`, in that order.
- `wait_for_url("**/inventory.html")` waits for navigation to complete; the `**` is a glob that matches any prefix.

A test then becomes tiny:

```python
def test_inventory_shows_six_products(logged_in_page):
    assert logged_in_page.locator(".inventory_item").count() == 6
```

Notice the test says nothing about *how* login happens. If the login screen changes, only the fixture changes.

### 10. `autouse` fixtures: setup that applies automatically

Normally a test must name a fixture to get it. With `autouse=True`, pytest applies the fixture to every test in its scope automatically, even when no test mentions it. Use this for cross-cutting concerns such as logging, setting default timeouts, or configuring Playwright's test-id attribute.

The SauceDemo site marks its elements with a `data-test` attribute (for example `data-test="username"`), while Playwright's `get_by_test_id()` looks for `data-testid` by default. You can tell Playwright to use `data-test` instead via the `playwright` fixture's selectors object:

```python
# conftest.py
import pytest


@pytest.fixture(scope="session", autouse=True)
def configure_test_id(playwright):
    playwright.selectors.set_test_id_attribute("data-test")
```

Line by line:

- `scope="session", autouse=True` run this exactly once per test run, automatically, before any test.
- `configure_test_id(playwright)` requests the session-scoped `playwright` fixture.
- `playwright.selectors.set_test_id_attribute("data-test")` changes the attribute that `page.get_by_test_id(...)` reads. After this, `page.get_by_test_id("username")` finds `<input data-test="username">`.

Use `autouse` sparingly. Invisible behaviour can confuse people ("why is this happening?"). Reserve it for things every test genuinely needs, and give the fixture a descriptive name.

### 11. Parameterised fixtures

A fixture can run the *same tests* multiple times with different values using `params`. Each value produces a separate test run.

```python
import pytest


@pytest.fixture(params=["standard_user", "problem_user", "performance_glitch_user"])
def valid_username(request):
    return request.param
```

- `params=[...]` lists the values.
- `request` is a **built-in pytest fixture** representing the current fixture request. `request.param` holds the current value.
- Any test that takes `valid_username` runs three times, once per user. pytest names them `test_x[standard_user]`, `test_x[problem_user]`, and so on.

Parameterising tests directly with `pytest.mark.parametrize` is covered in the Data-Driven Testing lesson later today; parameterised fixtures are most useful when *many* tests should be repeated across the same dimension (e.g., every test across multiple user types).

### 12. Factory fixtures

Sometimes a test needs to create several objects, or objects with custom values. A **factory fixture** returns a *function* that builds the object on demand and (optionally) cleans up everything it built.

```python
import pytest


@pytest.fixture
def make_context(browser):
    contexts = []

    def _make(**kwargs):
        ctx = browser.new_context(**kwargs)
        contexts.append(ctx)
        return ctx

    yield _make

    for ctx in contexts:
        ctx.close()
```

Line by line:

- `make_context(browser)` depends on the session-scoped `browser`.
- `contexts = []` keeps track of everything created, so we can close it all later.
- `def _make(**kwargs):` an inner function. `**kwargs` collects any keyword arguments (`viewport=...`, `locale=...`) into a dictionary.
- `ctx = browser.new_context(**kwargs)` the `**` here does the reverse: it spreads the dictionary back out into keyword arguments.
- `yield _make` gives the test the *function*, not a context.
- After the test, the loop closes every context that was created. This is teardown that scales with however many contexts the test made.

(pytest-playwright already provides exactly this idea as the built-in `new_context` fixture; writing your own is a good way to understand the pattern, and the pattern applies to any resource: users, orders, files.)

### 13. A reusable authenticated state with `storage_state`

Logging in through the UI before every test is slow and makes every test depend on the login page working. A better approach used by professional frameworks: **log in once, save the browser's cookies and local storage to a JSON file, and start later contexts already logged in.** Playwright calls this `storage_state`.

```python
# conftest.py
from pathlib import Path
import pytest

AUTH_FILE = Path(".auth/standard_user.json")


@pytest.fixture(scope="session")
def auth_state_path(browser, base_url) -> str:
    """Log in once through the UI and save the session to disk."""
    AUTH_FILE.parent.mkdir(exist_ok=True)

    context = browser.new_context(base_url=base_url)
    page = context.new_page()
    page.goto("/")
    page.locator("#user-name").fill("standard_user")
    page.locator("#password").fill("secret_sauce")
    page.locator("#login-button").click()
    page.wait_for_url("**/inventory.html")

    context.storage_state(path=str(AUTH_FILE))
    context.close()
    return str(AUTH_FILE)


@pytest.fixture
def logged_in_page_fast(browser, base_url, auth_state_path):
    """A fresh page that is already authenticated, without touching the login UI."""
    context = browser.new_context(base_url=base_url, storage_state=auth_state_path)
    page = context.new_page()
    yield page
    context.close()
```

Line by line:

- `from pathlib import Path` gives an object-oriented way to handle file paths. `Path(".auth/standard_user.json")` represents a relative path.
- `scope="session"` means the login happens **once per run**. Notice that this fixture requests `browser` (session scope), not `page`, so we avoid `ScopeMismatch`.
- `AUTH_FILE.parent.mkdir(exist_ok=True)` creates the `.auth` folder if it does not already exist.
- `browser.new_context(base_url=base_url)` creates a private context; `base_url` is the session fixture string (or `None`, so set it in `pytest.ini`).
- The four lines that fill and click are the normal login steps.
- `context.storage_state(path=...)` writes cookies and local storage to the file. SauceDemo keeps its session in a cookie, so this captures the logged-in state.
- `context.close()` releases that helper context. The function returns the file's path as a string.
- `logged_in_page_fast` is function-scoped, so every test gets an isolated context, but each one is created with `storage_state=auth_state_path`, so it **starts already logged in**. After the test, `yield` resumes and the context is closed.

Add `.auth/` to `.gitignore`. Storage-state files can contain session tokens and must never be committed.

> **Honest caveat:** this technique tests everything *except* the login page itself, so you still need dedicated login tests that use the UI. Mixing the two is the standard approach: UI login in login tests, `storage_state` everywhere else.

### 14. Seeing what is going on: `--fixtures` and `--setup-show`

Fixtures are invisible machinery, so pytest gives you two tools to reveal them:

```bash
pytest --fixtures                 # lists all available fixtures with their docstrings
pytest --setup-show tests/test_login_builtin.py
```

`--setup-show` prints each fixture's setup (`SETUP`) and teardown (`TEARDOWN`) with its scope letter (`S` session, `M` module, `C` class, `F` function). A shortened output:

```
SETUP    S playwright
SETUP    S browser_type
SETUP    S browser (fixtures used: browser_type, ...)
        SETUP    F context (fixtures used: browser, ...)
        SETUP    F page (fixtures used: context)
        tests/test_login_builtin.py::test_standard_user_can_log_in PASSED
        TEARDOWN F page
        TEARDOWN F context
TEARDOWN S browser
```

Seeing that the browser is set up once and pages once per test is a very good way to confirm your mental model.

---

## Code Examples

### Example A: A complete, small, realistic `conftest.py`

This file combines the ideas above into a base for the running SauceDemo project.

```python
# conftest.py
from pathlib import Path

import pytest
from playwright.sync_api import Page

VALID_USER = "standard_user"
VALID_PASSWORD = "secret_sauce"
AUTH_FILE = Path(".auth") / f"{VALID_USER}.json"


# ---------- 1. Configuration fixtures (session scope) ----------

@pytest.fixture(scope="session", autouse=True)
def configure_test_id(playwright):
    """SauceDemo uses data-test, not data-testid."""
    playwright.selectors.set_test_id_attribute("data-test")


@pytest.fixture(scope="session")
def browser_context_args(browser_context_args):
    """Apply a consistent viewport and locale to every context."""
    return {
        **browser_context_args,
        "viewport": {"width": 1366, "height": 768},
        "locale": "en-US",
    }


# ---------- 2. Authentication fixtures ----------

@pytest.fixture(scope="session")
def auth_state_path(browser, base_url) -> str:
    """Log in once via the UI and persist cookies/local storage."""
    AUTH_FILE.parent.mkdir(exist_ok=True)
    context = browser.new_context(base_url=base_url)
    page = context.new_page()
    page.goto("/")
    page.get_by_test_id("username").fill(VALID_USER)
    page.get_by_test_id("password").fill(VALID_PASSWORD)
    page.get_by_test_id("login-button").click()
    page.wait_for_url("**/inventory.html")
    context.storage_state(path=str(AUTH_FILE))
    context.close()
    return str(AUTH_FILE)


@pytest.fixture
def authenticated_page(browser, base_url, auth_state_path) -> Page:
    """Fresh, isolated, already-logged-in page for each test."""
    context = browser.new_context(
        base_url=base_url,
        storage_state=auth_state_path,
        viewport={"width": 1366, "height": 768},
    )
    page = context.new_page()
    page.goto("/inventory.html")
    yield page
    context.close()
```

Walkthrough of what is new compared with earlier snippets:

- Constants at the top (`VALID_USER`, `VALID_PASSWORD`) avoid "magic strings" scattered around. In a real project, credentials for non-public systems must come from environment variables (`os.environ["APP_PASSWORD"]`) or a secrets manager, never committed to source control. SauceDemo's credentials are published openly on its login page, so using them here is fine.
- The `Path(".auth") / f"{VALID_USER}.json"` expression uses the `/` operator, which `Path` overloads to join path parts. The `f"..."` is an **f-string** that inserts the variable's value.
- `page.get_by_test_id("username")` now works because of the `configure_test_id` fixture. It is more readable and more resilient than CSS IDs.
- `authenticated_page` combines three fixtures: `browser`, `base_url`, and `auth_state_path`. Because it passes its own `viewport` argument, note that arguments supplied directly to `new_context` are used *instead of* those coming from `browser_context_args` (we are bypassing the `context` fixture here), which is why we repeat the viewport.

A test using it:

```python
# tests/test_inventory.py
from playwright.sync_api import Page, expect


def test_inventory_lists_six_products(authenticated_page: Page):
    items = authenticated_page.get_by_test_id("inventory-item")
    expect(items).to_have_count(6)


def test_add_backpack_updates_cart_badge(authenticated_page: Page):
    authenticated_page.get_by_test_id("add-to-cart-sauce-labs-backpack").click()
    expect(authenticated_page.get_by_test_id("shopping-cart-badge")).to_have_text("1")
```

Both tests start on the inventory page in an isolated context, without ever seeing the login form. (SauceDemo's `data-test` values may change between site versions; if a locator fails, inspect the page and adjust.)

### Example B: A function-scoped fixture with teardown logging

```python
import pytest


@pytest.fixture(autouse=True)
def log_test_boundaries(request):
    print(f"\n--- START {request.node.name} ---")
    yield
    print(f"--- END   {request.node.name} ---")
```

- `request.node` is the test item currently running; `.name` is its function name.
- `print` output is captured by pytest and shown only for failures, or always when you run `pytest -s`.
- The code after `yield` runs after the test regardless of pass or fail.

### Example C: Overriding a fixture at a lower level

Suppose most tests use a 1366x768 viewport, but the mobile-layout tests need a phone-sized screen. Put this in `tests/mobile/conftest.py`:

```python
import pytest


@pytest.fixture(scope="session")
def browser_context_args(browser_context_args, playwright):
    iphone = playwright.devices["iPhone 13"]
    return {**browser_context_args, **iphone}
```

- `playwright.devices` is a dictionary of ready-made device descriptors (viewport, user agent, touch support, device scale factor).
- Tests under `tests/mobile/` get the iPhone configuration; all others keep the root version. No test code changes.

---

## Real-World Scenarios

**Scenario 1: Multi-role testing.** An e-commerce company needs to check that an admin sees an "Approve order" button that a customer does not. With the `new_context` factory fixture, one test opens two contexts (admin and customer), each with its own `storage_state`, and verifies both views side by side, with guaranteed cleanup.

**Scenario 2: Environment switching in CI.** The same suite runs nightly against `https://staging.example.com` and before release against `https://preprod.example.com`. A single `--base-url` argument in the pipeline definition does it; no test file changes.

**Scenario 3: Slow login.** An enterprise app's login involves a redirect to a single-sign-on provider and takes 8 seconds. With 300 tests, UI login every time costs 40 minutes. Moving to a session-scoped `storage_state` fixture reduces it to 8 seconds in total.

**Scenario 4: Test data hygiene.** A test creates an order through the API. A yield fixture deletes the order afterwards, even when the test fails halfway, so the test environment is not polluted by failing runs. This is exactly what the teardown half of `yield` is for.

---

## Common Pitfalls and Best Practices

**Pitfalls**

1. **`ScopeMismatch` errors.** Remember: wide-scope fixtures cannot depend on narrower-scope ones. Request `browser` (session), not `page` (function), in session fixtures.
2. **Forgetting `yield` and putting teardown after `return`.** Code after `return` never runs. Use `yield` whenever cleanup is needed.
3. **Sharing state through wide scopes.** If a module-scoped fixture returns a mutable object (a list, a page) and one test changes it, later tests see the change. Tests then pass or fail depending on order. Keep stateful things function-scoped.
4. **Importing fixtures from `conftest.py`.** Do not write `from conftest import page_fixture`. pytest finds them automatically; importing causes confusing duplicate-registration behaviour.
5. **Overriding a fixture with the wrong signature.** When overriding `browser_context_args`, remember to accept and extend the parent (`{**browser_context_args, ...}`); otherwise you silently discard options like `--device` or `--base-url` handling.
6. **Doing assertions inside fixtures.** Fixtures should prepare state; the test decides what is correct. A failing assertion in a fixture is reported as an *error* (setup failure), not a *failure*, which confuses triage. (Light sanity checks such as waiting for the inventory URL are acceptable.)
7. **Autouse overuse.** Hidden behaviour makes tests hard to reason about.
8. **Committing `.auth/*.json`.** These files hold session tokens.
9. **Forgetting to close what you open.** Any `browser.new_context()` you call yourself must be closed in teardown. The built-in `context` and `page` fixtures close themselves; hand-made ones do not.

**Best practices**

- Prefer **function scope** for anything holding state; widen scope only for read-only or genuinely expensive setup.
- Give fixtures **noun names** describing what the test receives (`authenticated_page`, `checkout_data`), not verbs.
- Add a **docstring** to every fixture in `conftest.py`; `pytest --fixtures` displays it.
- Keep `conftest.py` focused. If it grows beyond a couple of hundred lines, split fixtures into modules (`fixtures/auth.py`, `fixtures/pages.py`) and register them with `pytest_plugins = ["fixtures.auth", "fixtures.pages"]` in the root `conftest.py`.
- Use **composition** instead of copy-paste: small fixtures, combined.
- Use `--setup-show` whenever fixture order surprises you.
- Provide **type hints** (`page: Page`) so editors autocomplete Playwright methods.

---

## Mini Practice Exercises

**Exercise 1 (warm-up): a greeting fixture.**
Write a fixture `config` that returns the dictionary `{"user": "standard_user", "password": "secret_sauce"}`, and a test `test_config_has_user(config)` asserting that `config["user"]` equals `"standard_user"`.
*Hint:* `@pytest.fixture` and `return`. Run with `pytest --setup-show` and read the output.

**Exercise 2: remove the boilerplate.**
Take the "naive" test in Section 1 and rewrite it so it uses the `page` fixture and the `base_url` set in `pytest.ini`. Confirm it passes in Chromium and Firefox with `--browser chromium --browser firefox`.
*Solution outline:* Put `base_url = https://www.saucedemo.com` in `pytest.ini`, then call `page.goto("/")` and take `page: Page` as a parameter.

**Exercise 3: a yield fixture.**
Create a fixture `cart_cleaner(authenticated_page)` that yields the page, then after the test opens the cart (`/cart.html`) and clicks every "Remove" button.
*Hint:* After `yield`, use `page.get_by_role("button", name="Remove")` and loop with `.all()`. Check `.count()` first so that you do not fail when the cart is empty.

**Exercise 4: ScopeMismatch on purpose.**
Write a `scope="session"` fixture that takes `page` as a parameter and a test that uses it. Read the error message, then fix it by changing the fixture to depend on `browser`.

**Exercise 5: viewport override.**
Override `browser_context_args` so every context uses a viewport of 390x844. Write a test that asserts `page.viewport_size == {"width": 390, "height": 844}`.
*Solution:*
```python
@pytest.fixture(scope="session")
def browser_context_args(browser_context_args):
    return {**browser_context_args, "viewport": {"width": 390, "height": 844}}

def test_viewport(page):
    assert page.viewport_size == {"width": 390, "height": 844}
```

**Exercise 6 (Project 1 link): auth fixture.**
In your Project 1 repository, create a session-scoped fixture that logs in once and stores state to `.auth/`, then switch at least two existing tests to use it. Record how much faster the suite runs (use `pytest --durations=5`).

---

## Summary / Key Takeaways

- A **fixture** is a function marked `@pytest.fixture` that prepares (and optionally cleans up) something a test needs. Tests request fixtures by naming them as parameters.
- `pytest-playwright` supplies ready-made fixtures: `playwright`, `browser`, `context`, `page`, `new_context`, `browser_name`, `base_url`, plus overridable `browser_type_launch_args` and `browser_context_args`.
- The browser is launched **once per session**; each test gets a **new context and page**, which gives speed and isolation.
- Use `yield` for setup-and-teardown; code after `yield` runs even if the test fails. Teardown order is the reverse of setup.
- **Scope** controls lifetime (`function`, `class`, `module`, `package`, `session`). Wider-scope fixtures cannot depend on narrower ones.
- Put shared fixtures in **`conftest.py`**; never import them.
- Compose fixtures, parameterise them with `params`, build factory fixtures, and use `autouse` carefully.
- `storage_state` lets you log in once and reuse the authenticated session for faster, more focused tests.
- Debug with `pytest --fixtures` and `pytest --setup-show`.

---

## External Resources

- pytest documentation, "How to use fixtures": https://docs.pytest.org/en/stable/how-to/fixtures.html
- Playwright for Python, "Pytest plugin reference" (built-in fixtures and CLI options): https://playwright.dev/python/docs/test-runners
- Playwright for Python, "Authentication" (`storage_state`): https://playwright.dev/python/docs/auth
