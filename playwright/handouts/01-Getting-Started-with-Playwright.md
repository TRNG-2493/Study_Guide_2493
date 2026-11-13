# 01 — Getting Started with Playwright

> **Before you start**
>
> - **By the end you can:** explain what Playwright is, describe browser → context → page, write and run a first test, and use command-line options and `pytest.ini`.
> - **Practice site:** Swag Labs — <https://www.saucedemo.com/> (a demo store made for test automation).
> - **Login details:** username `standard_user`, password `secret_sauce` (shown on the login page).
> - **Create:** a folder `lecture01/` with an empty file `test_first.py` inside it.
> - **Run tests with:** `pytest` (from inside `lecture01/`, with your virtual environment active)

---

## Topic 1 — What Playwright is and how it talks to the browser

### Definition

Playwright is an open-source library from Microsoft for automating web browsers. We use it to write **end-to-end (E2E) tests**: tests that open a real browser, click and type like a user, and check that the page behaves correctly.

### Key ideas

- Works with **Chromium** (Chrome, Edge), **Firefox** and **WebKit** (Safari's engine).
- Your Python code → the **Playwright driver** → the **browser**, over one persistent connection. That connection is what makes **auto-waiting** possible.
- Object hierarchy:

| Object | What it is | Cost |
|---|---|---|
| `Browser` | One running browser | Expensive, shared across tests |
| `BrowserContext` | An isolated session (own cookies, storage) — like an incognito window | Cheap, one per test |
| `Page` | One tab | Almost everything goes through `page` |

- Compared with Selenium: no separate driver per browser, built-in auto-waiting, and a fresh context per test instead of a fresh browser.

### Worked example — see the hierarchy for yourself

**Step 1.** In `test_first.py`, ask pytest for all three objects:

```python
def test_hierarchy(browser, context, page):
    pass
```

**Step 2.** Print the browser's name and version:

```python
def test_hierarchy(browser, context, page):
    print("Browser:", browser.browser_type.name, browser.version)
```

**Step 3.** Show that the page belongs to the context:

```python
def test_hierarchy(browser, context, page):
    print("Browser:", browser.browser_type.name, browser.version)
    print("Pages in this context:", len(context.pages))
    assert page.context == context
```

> **Predict:** how many pages will the context have? Why?

**Step 4.** Run it with `-s` so `print()` output is shown:

```bash
pytest -s
```

### Checkpoint

```
Browser: chromium 1xx.0.xxxx.xx
Pages in this context: 1
.
1 passed
```

### Your turn

1. Add `print(page.url)` before the assertion. What URL does a brand-new page have?
   *Hint: nothing has been opened yet.*
2. Add `page.goto("https://www.saucedemo.com/")` and print `page.title()`.
   *Hint: `goto` must come before `title()`.*
3. Run the test with `--browser firefox`. What changes in the output?
   *Hint: if it fails, run `playwright install firefox` first.*

---

## Topic 2 — How tests run: pytest + pytest-playwright

### Definition

**pytest** finds and runs tests. **pytest-playwright** is a plugin that starts the browser for you and hands your tests ready-made **fixtures** such as `page`. You ask for a fixture just by adding its name as a function parameter.

### Key ideas

| Piece | Job |
|---|---|
| `playwright` | Controls the browser |
| `pytest` | Finds `test_*.py` files and `test_` functions, reports pass/fail |
| `pytest-playwright` | Provides `page`, `context`, `browser`, `browser_name` |

- `page` and `context` are **new for every test**, so tests never share cookies, logins or tabs.
- `browser` is started **once per session** and shared.
- Python has **no** Playwright Test runner (`npx playwright test`). Use <https://playwright.dev/python>.

### Worked example — prove that tests are isolated

**Step 1.** Create a test that logs in to Swag Labs:

```python
def test_first_visit(page, context):
    page.goto("https://www.saucedemo.com/")
    page.get_by_placeholder("Username").fill("standard_user")
    page.get_by_placeholder("Password").fill("secret_sauce")
    page.get_by_role("button", name="Login").click()
```

**Step 2.** Print the cookie names — logging in creates a session cookie:

```python
    print("Cookies in test 1:", [c["name"] for c in context.cookies()])
```

**Step 3.** Add a second test that opens the products page **without** logging in:

```python
def test_second_visit(page, context):
    page.goto("https://www.saucedemo.com/inventory.html")
    print("Cookies in test 2:", [c["name"] for c in context.cookies()])
    print("Ended up at:", page.url)
```

> **Predict:** will test 2 still be logged in from test 1?

**Step 4.** Run `pytest -s -v`.

### Checkpoint

Test 1 prints a list containing `session-username`. Test 2 prints an empty list and ends up back on the login page — it got its own fresh context.

### Your turn

1. Add `browser_name` as a parameter to one test and print it.
2. Rename `test_second_visit` to `second_visit` and run again. How many tests ran?
   *Hint: look at how pytest discovers tests.*
3. Run only one test using `pytest test_first.py::test_first_visit`.

### Common errors

| Error | Fix |
|---|---|
| `fixture 'page' not found` | Virtual environment not active, or `pytest-playwright` not installed |
| `0 tests collected` | File or function name doesn't start with `test_` |
| Copying `npx` / `.ts` examples | Those are for JavaScript; use the Python docs |

---

## Topic 3 — Your first test

### Definition

A Playwright test is a normal pytest function that receives `page`, navigates with `page.goto()` and checks results with `expect()`. `expect` keeps retrying (up to 5 seconds) until the check passes, which makes tests reliable on pages that load over time.

### Key ideas

- Import from `playwright.sync_api` — we use the **sync** API (no `async`/`await`).
- `page.goto(url)` opens the URL and waits for it to load.
- `expect(page).to_have_title(...)` retries; `assert page.title() == ...` checks **once**.

### Worked example — check the home page title

**Step 1.** Import what you need:

```python
from playwright.sync_api import Page, expect
```

**Step 2.** Define the test and ask for `page`:

```python
def test_homepage_has_title(page: Page):
    pass
```

**Step 3.** Open the site:

```python
def test_homepage_has_title(page: Page):
    page.goto("https://www.saucedemo.com/")
```

**Step 4.** Check the title:

```python
def test_homepage_has_title(page: Page):
    page.goto("https://www.saucedemo.com/")
    expect(page).to_have_title("Swag Labs")
```

> **Predict:** what happens if you change the expected title to `"Swag Labs!"`? How long does the failure take?

**Step 5.** Run `pytest`.

### Checkpoint

```
test_first.py .                                   [100%]
1 passed
```

With the wrong title: a failure after about 5 seconds showing `Expected value: "Swag Labs!"` and `Received value: "Swag Labs"`.

### Your turn

1. Write `test_login_goes_to_products`: log in as `standard_user` and check the URL with `expect(page).to_have_url("https://www.saucedemo.com/inventory.html")`.
2. In the same test, check the title is still `"Swag Labs"`.
3. Rewrite one check using `assert page.title() == ...`. Both pass here — when would `assert` fail but `expect` pass?
   *Hint: think about a page that is still loading.*

### Common errors

| Error | Fix |
|---|---|
| `NameError: name 'page' is not defined` | Add `page: Page` to the function's parameters |
| `NameError: name 'expect' is not defined` | Import it from `playwright.sync_api` |
| "I don't see a browser" | Tests are headless by default; add `--headed` |

---

## Topic 4 — Command-line options

### Definition

Command-line options change **how** tests run without changing the code: which browser, whether you can see it, how fast it moves, and what gets recorded. By default tests run **headless** in **Chromium**.

### Key ideas

| Option | Example |
|---|---|
| `--headed` | `pytest --headed` |
| `--browser` (repeatable) | `pytest --browser chromium --browser firefox` |
| `--slowmo` (ms) | `pytest --headed --slowmo 1000` |
| `--base-url` | `pytest --base-url https://www.saucedemo.com` |
| `--screenshot` / `--video` / `--tracing` | `pytest --screenshot only-on-failure` |
| `-v`, `-s`, `-k name` | verbose, show prints, filter by name |

### Worked example — watch, then switch browsers

**Step 1.** Run the login test so you can see it:

```bash
pytest --headed -k login
```

**Step 2.** Slow it down to follow each action:

```bash
pytest --headed --slowmo 1000 -k login
```

**Step 3.** Run on two browsers:

```bash
pytest -v --browser chromium --browser firefox
```

**Step 4.** Shorten URLs with a base URL. Change the code:

```python
page.goto("/")
```

and run:

```bash
pytest -v --base-url https://www.saucedemo.com
```

> **Predict:** what happens if you run Step 4's code **without** `--base-url`?

### Checkpoint

```
test_first.py::test_homepage_has_title[chromium] PASSED
test_first.py::test_homepage_has_title[firefox] PASSED
```

### Your turn

1. Run with `--screenshot on`. Find the screenshots in `test-results/`.
2. Change the `inventory.html` URL check to use a relative path with `page.goto("/inventory.html")` in a new test. Where do you end up, and why?
   *Hint: you are not logged in.*
3. Use `--browser-channel chrome` to run in your installed Chrome.
   *Hint: only works if Chrome is installed on your machine.*

### Common errors

| Error | Fix |
|---|---|
| `Executable doesn't exist` for Firefox/WebKit | `playwright install firefox webkit` |
| `Cannot navigate to invalid URL` with `"/"` | You forgot `--base-url` |

---

## Topic 5 — Saving options in `pytest.ini`

### Definition

`pytest.ini` is a settings file in the project folder. Options in it apply to every `pytest` run, so you don't have to retype them.

### Key ideas

- `base_url = ...` sets the base URL.
- `addopts = ...` adds command-line options to every run.
- `--browser` options **add up**: one in `pytest.ini` plus one on the command line = two browsers.

### Worked example — move your options into a file

**Step 1.** Create `pytest.ini` next to `test_first.py`:

```ini
[pytest]
```

**Step 2.** Add the base URL:

```ini
[pytest]
base_url = https://www.saucedemo.com
```

**Step 3.** Add default options:

```ini
[pytest]
base_url = https://www.saucedemo.com
addopts = -v --browser chromium
```

**Step 4.** Run just `pytest`.

> **Predict:** if you now run `pytest --browser firefox`, how many times does each test run?

### Checkpoint

`pytest` on its own runs verbosely in Chromium, and `page.goto("/")` works with no extra options.

### Your turn

1. Add `--screenshot only-on-failure` to `addopts`. Break a test and confirm a screenshot appears.
2. Change all full URLs in your tests to relative paths (`/`, `/inventory.html`).
3. Run `pytest --browser firefox` and explain the result.
   *Hint: re-read the third key idea.*

### Common errors

| Error | Fix |
|---|---|
| Settings ignored | File must be named exactly `pytest.ini` and start with `[pytest]` |
| Tests run on two browsers unexpectedly | Remove `--browser` from `addopts` or from the command line |

---

## Stretch challenge

Write three tests: the login page title, a successful login that lands on `/inventory.html`, and a `locked_out_user` login that stays on `/`. Use only relative paths and `pytest.ini`, and run them on Chromium and Firefox with a single command.

## Exit ticket

1. What is the difference between a `Browser` and a `BrowserContext`?
2. Why is `expect(page).to_have_title(...)` safer than `assert page.title() == ...`?
3. Which option shows the browser window, and which one slows it down?

## Cheat sheet

| Command / code | Purpose |
|---|---|
| `from playwright.sync_api import Page, expect` | Standard imports |
| `def test_x(page: Page):` | Get a fresh tab |
| `page.goto(url)` | Open a page |
| `page.title()` / `page.url` | Read title / URL |
| `expect(page).to_have_title(...)` | Check title (retries) |
| `expect(page).to_have_url(...)` | Check URL (retries) |
| `context.cookies()` | Cookies in this context |
| `pytest --headed --slowmo 500` | Watch a slow run |
| `pytest --browser firefox` | Choose browser |
| `pytest --base-url URL` | Allow `page.goto("/path")` |
| `pytest -v -s -k name` | Verbose, prints, filter |
| `pytest.ini` → `base_url`, `addopts` | Save options |
