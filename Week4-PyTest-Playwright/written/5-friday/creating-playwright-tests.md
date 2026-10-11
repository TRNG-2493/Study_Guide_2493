# Creating Playwright Tests

## Learning Objectives

By the end of this lesson you will be able to:

- Explain what Playwright is and how the `pytest-playwright` plugin lets you write browser tests as ordinary PyTest tests.
- Install Playwright for Python, download browsers, and verify the installation.
- Write your first test using the built-in `page` fixture.
- Use `page.goto()`, `page.locator()`, actions such as `click()` and `fill()`, and web-first assertions with `expect()`.
- Structure a test using the Arrange-Act-Assert pattern, and give tests clear names.
- Write a complete end-to-end login-and-search style test and understand every line of it.
- Recognize and avoid the most common beginner mistakes.

---

## Why This Matters

This week's epic is to turn manual test design into automation: you started on Monday with PyTest basics, built up through fixtures, parametrization and reporting, and on Thursday you learned how to find elements on a page with CSS and XPath and how Playwright is put together. Today the pieces connect. You will write real browser tests.

In **Project 1: QE Foundations**, you designed manual test cases for an application. Many of those cases are UI scenarios such as "a registered user can log in", "searching for a product shows matching results", or "an invalid password shows an error message". Each of these is a perfect candidate for automation. A manual tester might repeat such a scenario fifty times across a release cycle. An automated Playwright test repeats it in seconds, identically, every single time, on every code change.

Playwright is one of the most widely adopted modern browser automation tools in industry. Knowing how to create a clean, reliable Playwright test is a core skill for a Test Automation Engineer, and everything else you learn today (the runner, auto-waiting, locators, the Inspector and codegen) builds on the test structure you learn here.

---

## The Concept

### 1. A quick recap of what you already know

- **PyTest** (Monday and Tuesday): discovers files named `test_*.py` or `*_test.py`, runs functions named `test_*`, supports `assert`, fixtures, markers and parametrization.
- **Fixtures** (Tuesday): functions decorated with `@pytest.fixture` that provide setup (and teardown) to tests. A test requests a fixture simply by naming it as a parameter.
- **Locators and architecture** (Thursday): you saw that Playwright controls a real browser through a process-based architecture: your Python code talks to a Playwright driver, which talks to the browser. A **Browser** contains one or more **Browser Contexts** (isolated, incognito-like sessions), and each context contains one or more **Pages** (tabs).

Today's key idea: **the `pytest-playwright` plugin gives you fixtures that create the Browser, Context and Page for you.** You just ask for `page` in your test function.

### 2. Two ways to use Playwright in Python

Playwright for Python provides two styles:

| Style | Import | Typical use |
|-------|--------|-------------|
| **Sync API** | `from playwright.sync_api import ...` | Tests and scripts. Simple, top to bottom code. **This is what we use.** |
| **Async API** | `from playwright.async_api import ...` | Applications that already use `asyncio`. |

For beginners writing tests, the sync API is the right choice. Every example in this course uses it.

There are also two ways to run it:

1. **Standalone script**: you start Playwright yourself with `with sync_playwright() as p:`, launch a browser, create a page, and close everything. Good for understanding what happens under the hood.
2. **With PyTest plugin (recommended for testing)**: `pytest-playwright` handles launching and closing, and you get the powerful PyTest features (fixtures, markers, parametrization, reports) for free.

### 3. Installation step by step

Make sure you are in a virtual environment (you created one on Monday). Then:

```bash
pip install pytest-playwright
playwright install
```

What each command does:

- `pip install pytest-playwright` installs the PyTest plugin and, as a dependency, the `playwright` Python package.
- `playwright install` downloads the browser binaries that Playwright controls: Chromium, Firefox and WebKit. These are special builds of the browsers, tested against the Playwright version. They are stored in a cache folder on your machine (not inside your project).

To download only one browser (faster, smaller):

```bash
playwright install chromium
```

On a Linux machine (or a CI server) you may also need operating system libraries:

```bash
playwright install --with-deps chromium
```

Verify the installation:

```bash
playwright --version
pytest --version
pip list | grep -i playwright     # on Windows PowerShell: pip list | findstr -i playwright
```

> **Tip:** If `playwright` is "not recognized", your virtual environment is probably not activated. Re-activate it and try again. As an alternative, `python -m playwright install` works anywhere Python works.

### 4. The anatomy of a Playwright test

Create a file `test_first.py`:

```python
import re
from playwright.sync_api import Page, expect


def test_playwright_homepage_has_title(page: Page):
    page.goto("https://playwright.dev/python/")
    expect(page).to_have_title(re.compile("Playwright"))
```

Run it:

```bash
pytest test_first.py
```

By default the browser runs **headless** (no visible window), so you will only see the PyTest dots. To watch it:

```bash
pytest test_first.py --headed
```

#### Line-by-line explanation

| Line | Explanation |
|------|-------------|
| `import re` | Python's regular-expression module. We use it to match part of the title instead of the whole title. |
| `from playwright.sync_api import Page, expect` | `Page` is the class representing a browser tab. We import it for **type hints** (helps your editor give autocomplete). `expect` is Playwright's assertion helper. |
| `def test_playwright_homepage_has_title(page: Page):` | A normal PyTest test function. The name starts with `test_` so PyTest discovers it. The parameter `page` is a **fixture** supplied by `pytest-playwright`. The `: Page` part is only a type hint; it does not change behavior. |
| `page.goto("https://playwright.dev/python/")` | Navigates the tab to the URL and waits for the page to load (by default until the `load` event). |
| `expect(page).to_have_title(re.compile("Playwright"))` | A **web-first assertion**: it checks the page title, and if the title is not yet correct, it **retries** until it matches or the timeout (5 seconds by default) expires. |

Notice there is no browser setup code, no `close()` call, and no `time.sleep()`. The plugin and Playwright take care of all of it.

### 5. What the `page` fixture really gives you

When your test requests `page`, `pytest-playwright` does the following for each test:

1. Starts (or reuses) a **browser** (a session-scoped fixture, so the browser launches once per test run).
2. Creates a brand-new **browser context** (function-scoped, so each test is isolated: fresh cookies, fresh local storage, fresh cache).
3. Creates a new **page** in that context and hands it to you.
4. After the test finishes, closes the page and context.

Because each test gets a fresh context, tests do not leak state into each other. This is the single most important reason Playwright tests are reliable: **test isolation is built in**. Compare this with the "shared fixture state" mistakes you might remember from Tuesday: here the plugin has already made the safe choice for you.

The plugin also gives you other fixtures you will use:

| Fixture | What it is |
|---------|-----------|
| `page` | A fresh tab, isolated per test. |
| `context` | The browser context the page lives in. Use it to open extra tabs or set cookies. |
| `browser` | The browser instance (session scope). |
| `browser_name` | `"chromium"`, `"firefox"` or `"webkit"`. |
| `playwright` | The top-level Playwright object. |
| `base_url` | The value of `--base-url`, if you provided one. |

We will look more closely at how to run with different options in the **Playwright test runner** lesson today.

### 6. Navigating: `page.goto()`

```python
page.goto("https://www.saucedemo.com/")
```

`saucedemo.com` is a public practice e-commerce site created for test automation training. It publishes its demo credentials on the login page (`standard_user` / `secret_sauce`), which makes it ideal for learning.

If you configure a base URL, you can use relative paths:

```bash
pytest --base-url https://www.saucedemo.com
```

```python
page.goto("/")            # becomes https://www.saucedemo.com/
page.goto("/inventory.html")
```

Why use a base URL? So that the same tests can run against development, staging and production-like environments by changing just one command-line option instead of editing code.

### 7. Finding elements: locators

A **locator** describes how to find an element. You met CSS and XPath yesterday. Playwright accepts both through `page.locator()`:

```python
page.locator("#user-name")                 # CSS selector: id
page.locator("input[name='password']")     # CSS selector: attribute
page.locator("xpath=//button[@id='login-button']")   # XPath
```

Playwright also offers **built-in locators** such as `get_by_role`, `get_by_label` and `get_by_placeholder`. These are more resilient and more readable, and they are the recommended default. We will study them in depth in the **Built-in locators** lesson today. In this lesson we will use a mixture so you can read both styles.

A crucial property: **a locator is lazy.** Creating a locator does not touch the page. Playwright only searches for the element when you perform an action or an assertion on it. This means a locator can be defined once and reused, and it always looks up the *current* element at the moment of use. That is why Playwright tests are less likely to suffer from "stale element" errors that you may hear about in other tools.

### 8. Performing actions

Common actions on a locator:

| Method | What it does |
|--------|--------------|
| `click()` | Clicks the element. |
| `dblclick()` | Double-clicks. |
| `fill("text")` | Clears the input and sets the value. |
| `press("Enter")` | Presses a key while focused on the element. |
| `press_sequentially("abc")` | Types character by character (use when a site reacts to each keystroke). |
| `check()` / `uncheck()` | Ticks or unticks a checkbox or radio button. |
| `select_option("value")` | Chooses an option in a `<select>`. |
| `hover()` | Moves the mouse over the element. |
| `clear()` | Empties an input. |

Before each action, Playwright automatically waits for the element to be ready (visible, enabled, stable and so on). We cover this in detail in **Auto-waiting and synchronization** today.

> **Note:** In older tutorials you may see `page.type()` or `locator.type()`. These are deprecated. Use `fill()` for normal inputs and `press_sequentially()` when you truly need per-key typing.

### 9. Assertions with `expect()`

Playwright's assertions are called **web-first assertions** because they understand that web pages change over time. They wait and retry.

```python
from playwright.sync_api import expect

expect(page).to_have_url("https://www.saucedemo.com/inventory.html")
expect(page).to_have_title("Swag Labs")
expect(locator).to_be_visible()
expect(locator).to_have_text("Products")
expect(locator).to_contain_text("Prod")
expect(locator).to_have_count(6)
expect(locator).to_have_value("standard_user")
expect(locator).to_be_enabled()
expect(locator).to_be_checked()
expect(locator).to_have_attribute("href", "/inventory.html")
expect(locator).not_to_be_visible()          # negation
```

Compare with a plain Python assertion:

```python
assert locator.is_visible()      # checks ONCE, immediately. No retry!
```

`is_visible()` returns the answer at that very instant. If the element appears 200 ms later, the plain `assert` fails and the test is flaky. `expect(locator).to_be_visible()` keeps trying for up to five seconds. **Prefer `expect()` for anything that depends on the page.** Plain `assert` remains perfectly fine for pure Python values (for example, comparing two numbers or lists that you already extracted).

### 10. The Arrange-Act-Assert pattern

Every good test follows three phases (you saw similar ideas in Monday's test design):

1. **Arrange**: get into a known starting state (open the page, prepare data).
2. **Act**: perform the behavior under test (fill the form, click the button).
3. **Assert**: verify the observable outcome.

Keeping these phases visible makes tests readable. Use blank lines or comments to separate them.

---

## Code Examples

### Example 1: A complete login test

```python
# test_login.py
from playwright.sync_api import Page, expect


def test_standard_user_can_log_in(page: Page):
    # Arrange
    page.goto("https://www.saucedemo.com/")

    # Act
    page.locator("#user-name").fill("standard_user")
    page.locator("#password").fill("secret_sauce")
    page.locator("#login-button").click()

    # Assert
    expect(page).to_have_url("https://www.saucedemo.com/inventory.html")
    expect(page.locator(".title")).to_have_text("Products")
```

**Explanation:**

- `page.locator("#user-name")` builds a locator from a CSS id selector (`#` means id). Remember Thursday: `#id` is the fastest and clearest CSS selector when ids are stable.
- `.fill("standard_user")` focuses the input, clears it and enters the text.
- `.click()` clicks the login button. Playwright waits for the button to be visible and enabled first.
- `expect(page).to_have_url(...)` waits until the browser has navigated to the inventory page.
- `page.locator(".title")` uses a CSS class selector (`.` means class). The text "Products" is the page heading shown after login.

### Example 2: A negative login test

```python
def test_locked_out_user_sees_error(page: Page):
    page.goto("https://www.saucedemo.com/")

    page.locator("#user-name").fill("locked_out_user")
    page.locator("#password").fill("secret_sauce")
    page.locator("#login-button").click()

    error = page.locator("[data-test='error']")
    expect(error).to_be_visible()
    expect(error).to_contain_text("locked out")
```

**Explanation:** A good test suite covers both the happy path and failure paths. Here we assign the error locator to a variable named `error` so that we can reuse it for two assertions. `[data-test='error']` is an attribute selector (Thursday). `to_contain_text("locked out")` passes if the element text includes that substring, which is less brittle than matching the entire message.

### Example 3: Login and "search" (filter) flow end to end

SauceDemo has no free-text search box, but it has a sort dropdown and a product list. A very typical "search-like" scenario is: log in, then find a specific product and verify it. We will use Playwright's own documentation site for a true search later in the day. For now:

```python
# test_inventory.py
from playwright.sync_api import Page, expect


def test_login_then_find_backpack(page: Page):
    # Arrange: log in
    page.goto("https://www.saucedemo.com/")
    page.locator("#user-name").fill("standard_user")
    page.locator("#password").fill("secret_sauce")
    page.locator("#login-button").click()
    expect(page).to_have_url("https://www.saucedemo.com/inventory.html")

    # Act: look at the product names
    names = page.locator(".inventory_item_name")

    # Assert
    expect(names).to_have_count(6)
    expect(names.first).to_have_text("Sauce Labs Backpack")
```

**Explanation:**

- `names` is a locator that matches *multiple* elements (all product names). It is not an error for a locator to match many elements, but actions like `click()` would then raise a "strict mode violation" (see Common Mistakes).
- `to_have_count(6)` waits until exactly six elements match.
- `.first` narrows the locator to the first match; we assert its text.

### Example 4: A true search test on the Playwright documentation site

```python
# test_docs_search.py
import re
from playwright.sync_api import Page, expect


def test_docs_navigation(page: Page):
    page.goto("https://playwright.dev/python/")

    page.get_by_role("link", name="Docs").click()

    expect(page).to_have_url(re.compile(r".*intro"))
    expect(page.get_by_role("heading", name="Installation")).to_be_visible()
```

**Explanation:**

- `get_by_role("link", name="Docs")` finds a link (an `<a>` element) whose accessible name is "Docs". This is a user-facing locator. Notice it reads like a sentence: "the link named Docs".
- `re.compile(r".*intro")` is a regular expression; the `r` prefix makes it a raw string so backslashes are not interpreted. The URL passes if it contains `intro`.
- The final line asserts that a heading called "Installation" is visible.

> The documentation website may change its structure over time. If a practice test breaks, this is a good learning moment: use the Inspector (later today) to re-inspect the page and update the locator.

### Example 5: Grouping tests in a class

```python
class TestLogin:
    URL = "https://www.saucedemo.com/"

    def test_valid_login(self, page: Page):
        page.goto(self.URL)
        page.locator("#user-name").fill("standard_user")
        page.locator("#password").fill("secret_sauce")
        page.locator("#login-button").click()
        expect(page).to_have_url(re.compile("inventory"))

    def test_empty_credentials_show_error(self, page: Page):
        page.goto(self.URL)
        page.locator("#login-button").click()
        expect(page.locator("[data-test='error']")).to_contain_text("Username is required")
```

(Add `import re` at the top.) As you learned on Monday, test classes need names starting with `Test` and must not define `__init__`. Each method still gets its own fresh `page`.

### Example 6: Reducing repetition with a fixture

Tuesday's fixtures are perfect for the repeated login steps:

```python
import pytest
from playwright.sync_api import Page, expect


@pytest.fixture
def logged_in_page(page: Page) -> Page:
    page.goto("https://www.saucedemo.com/")
    page.locator("#user-name").fill("standard_user")
    page.locator("#password").fill("secret_sauce")
    page.locator("#login-button").click()
    expect(page).to_have_url("https://www.saucedemo.com/inventory.html")
    return page


def test_cart_starts_empty(logged_in_page: Page):
    expect(logged_in_page.locator(".shopping_cart_badge")).to_have_count(0)


def test_add_item_updates_cart_badge(logged_in_page: Page):
    logged_in_page.locator("[data-test='add-to-cart-sauce-labs-backpack']").click()
    expect(logged_in_page.locator(".shopping_cart_badge")).to_have_text("1")
```

**Explanation:** `logged_in_page` depends on the `page` fixture, performs the login, and returns the page. Any test that requests `logged_in_page` starts already logged in. Note `to_have_count(0)` is the correct way to assert that an element does *not* exist. (We will see a more organized way to model pages in later lessons of the course; for now a fixture is a good start.)

### Example 7: Running without the plugin (to see what is hidden)

```python
# script_without_plugin.py
from playwright.sync_api import sync_playwright

with sync_playwright() as p:
    browser = p.chromium.launch(headless=False)
    context = browser.new_context()
    page = context.new_page()
    page.goto("https://playwright.dev/python/")
    print(page.title())
    browser.close()
```

**Explanation:** `sync_playwright()` starts the driver; `p.chromium.launch()` starts the browser; `browser.new_context()` creates an isolated session; `context.new_page()` opens a tab. This is exactly what the `page` fixture does for you, plus cleanup even when tests fail. Run it with `python script_without_plugin.py`.

---

## Real-World Scenarios

1. **Smoke test after every deployment.** A team runs three Playwright tests (login, search, add to cart) immediately after each deployment. If any fail, the release pipeline stops. Writing small, fast, reliable tests like Example 1 is precisely the skill needed.
2. **Regression of a reported bug.** A customer reports that locked-out users see a blank screen instead of an error. The engineer writes Example 2 first (it fails), fixes the application, and keeps the test forever so the bug cannot come back silently.
3. **Replacing manual checks.** In Project 1 you wrote manual test cases such as "TC-LOGIN-001: Valid login". Today's automation of that case is a direct translation: steps become actions, expected results become `expect()` assertions.

---

## Common Mistakes

1. **Forgetting to name the file or function correctly.** `login_test.py` with `def check_login()` is not collected. Use `test_*.py` and `test_*`.
2. **Using `time.sleep()` to wait.** It makes tests slow and still flaky. Rely on auto-waiting and `expect()`.
3. **Using plain `assert` with instantaneous checks.** `assert locator.is_visible()` does not retry. Use `expect(locator).to_be_visible()`.
4. **Strict mode violations.** If a locator matches more than one element and you call `click()` or `fill()`, Playwright raises an error listing the matches. Fix by making the locator more specific, or deliberately choose with `.first`, `.last` or `.nth(i)`.
5. **Forgetting `playwright install`.** Error: "Executable doesn't exist at ...". Run `playwright install`.
6. **Sharing state between tests.** Do not rely on test A having logged in for test B. Each test gets a fresh context, so each must set up its own state (or use a fixture).
7. **Hard-coding secrets in tests.** The demo site publishes its credentials, but real applications do not. In real projects, read credentials from environment variables.
8. **Over-specific assertions.** Matching an entire long error message makes the test break for trivial copy changes. Use `to_contain_text` or a regex when the exact wording is not what you are testing.
9. **Using the old `page.type()` or `page.click(selector)` shortcuts everywhere.** The locator-based approach (`page.locator(...).click()`) is the recommended modern style.

---

## Practice Exercises

**Exercise 1 (warm-up).** Install `pytest-playwright`, run `playwright install chromium`, and run the first example with `--headed`. Then run it with `--browser firefox` (you may need `playwright install firefox`).

*Hint:* Use `pytest test_first.py --headed --browser chromium`.

**Exercise 2.** Write a test named `test_invalid_password_shows_error` for SauceDemo. Use `standard_user` and a wrong password. Assert that the error element is visible and contains the text "do not match".

*Solution:*

```python
def test_invalid_password_shows_error(page: Page):
    page.goto("https://www.saucedemo.com/")
    page.locator("#user-name").fill("standard_user")
    page.locator("#password").fill("wrong_password")
    page.locator("#login-button").click()

    error = page.locator("[data-test='error']")
    expect(error).to_be_visible()
    expect(error).to_contain_text("do not match")
```

**Exercise 3.** Write a test that logs in, adds "Sauce Labs Backpack" to the cart, opens the cart (click `.shopping_cart_link`) and asserts that the cart page lists the backpack (`.inventory_item_name`).

*Hint:* After adding, the badge shows 1. After clicking the cart link, the URL ends with `cart.html`.

**Exercise 4.** Refactor Exercises 2 and 3 so they share a `logged_in_page` fixture, and put the fixture into a `conftest.py` (you learned this on Tuesday).

**Exercise 5 (Project 1 link).** Pick two UI test cases from your Project 1 manual test suite. Translate each manual step into a Playwright action and each expected result into an `expect()` assertion. Keep a table with columns: *Manual step | Playwright code*.

**Exercise 6 (challenge).** Parametrize the negative login test with three data rows (empty username, empty password, wrong password) using `@pytest.mark.parametrize` (Tuesday), each with its expected error message.

---

## Summary

- `pytest-playwright` lets you write browser tests as plain PyTest tests; install with `pip install pytest-playwright` and `playwright install`.
- The `page` fixture provides a fresh, isolated tab for every test; no setup or teardown code is needed.
- Use `page.goto()` to navigate, `page.locator()` (or built-in locators) to find elements, actions like `click()` and `fill()` to interact, and `expect()` to assert.
- Web-first assertions retry until they pass or time out, which removes the need for sleeps.
- Locators are lazy and re-evaluated at use time; strict mode protects you from clicking the wrong element.
- Structure each test as Arrange, Act, Assert, and use fixtures and classes (Monday and Tuesday skills) to avoid repetition.

---

## Additional Resources

- Playwright for Python: Writing tests: https://playwright.dev/python/docs/writing-tests
- Playwright for Python: Installation: https://playwright.dev/python/docs/intro
- Playwright for Python: Assertions: https://playwright.dev/python/docs/test-assertions
