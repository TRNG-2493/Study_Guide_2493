# Playwright Test Runner

## Learning Objectives

By the end of this lesson you will be able to:

- Explain how the PyTest runner and the `pytest-playwright` plugin work together.
- Run Playwright tests in headed or headless mode, in different browsers, with slow motion, and against a base URL.
- Select tests using the PyTest filters you learned on Monday (`-k`, `-m`, node ids) in a Playwright context.
- Capture screenshots, videos and traces for debugging, and open a trace with the Trace Viewer.
- Configure browser context options (viewport, locale, permissions, device emulation) using fixtures and `conftest.py`.
- Create a `pytest.ini` that stores sensible defaults for your Playwright project.
- Run tests in parallel and re-run flaky tests, and understand the trade-offs.

---

## Why This Matters

This week's epic moves you from writing individual tests toward a working automation framework for Project 1: QE Foundations. A test you can only run on your own laptop, headed, in one browser, is not much use to a team. A **test runner** is the machinery that finds, runs, filters, reports and debugs tests. In industry, the same suite must run:

- on a developer laptop, headed, with slow motion for debugging;
- in a CI pipeline, headless, in several browsers, in parallel;
- against different environments (development, staging) without code changes.

Playwright for Python does not ship its own separate runner. **It uses PyTest** (which you have practiced since Monday). The plugin `pytest-playwright` adds command-line options and fixtures. Because you already know PyTest, you already know most of the runner; today you learn the Playwright-specific parts.

---

## The Concept

### 1. Who does what?

| Component | Responsibility |
|-----------|----------------|
| **PyTest** | Finds tests (discovery), runs them, handles fixtures/markers/parametrization, reports pass/fail. |
| **`pytest-playwright` plugin** | Provides fixtures (`page`, `context`, `browser`...), adds CLI options (`--headed`, `--browser`, ...), manages artifacts (screenshots, video, traces). |
| **Playwright library** | Controls the actual browser. |

Check which options the plugin added to your PyTest:

```bash
pytest --help
```

Scroll to the section titled **playwright**. You will see the options described below.

### 2. Running tests: the basics

Everything from Monday still works:

```bash
pytest                                  # run everything discovered
pytest tests/test_login.py              # a single file
pytest tests/test_login.py::test_valid_login      # a single test (node id)
pytest tests/test_login.py::TestLogin::test_valid_login   # a method in a class
pytest -k "login and not locked"        # by keyword expression
pytest -m smoke                         # by marker
pytest -v                               # verbose names
pytest -x                               # stop at first failure
pytest --lf                             # re-run only last failures
```

Markers deserve a reminder: register them in `pytest.ini`, otherwise PyTest warns about unknown markers (and with `--strict-markers` fails).

### 3. Playwright command-line options

| Option | Meaning | Example |
|--------|---------|---------|
| `--headed` | Show the browser window (default is headless). | `pytest --headed` |
| `--browser` | Choose `chromium`, `firefox` or `webkit`. Can be repeated. | `pytest --browser firefox` |
| `--browser-channel` | Use an installed branded browser such as `chrome` or `msedge`. | `pytest --browser-channel chrome` |
| `--slowmo` | Delay each operation by N milliseconds, for watching. | `pytest --headed --slowmo 500` |
| `--device` | Emulate a device from Playwright's device list. | `pytest --device "iPhone 13"` |
| `--base-url` | Prefix for relative `page.goto()` paths. | `pytest --base-url https://www.saucedemo.com` |
| `--screenshot` | `on`, `off` or `only-on-failure`. | `pytest --screenshot only-on-failure` |
| `--video` | `on`, `off` or `retain-on-failure`. | `pytest --video retain-on-failure` |
| `--tracing` | `on`, `off` or `retain-on-failure`. | `pytest --tracing retain-on-failure` |
| `--output` | Folder for artifacts (default `test-results`). | `pytest --output artifacts` |
| `--full-page-screenshot` | Capture the whole scrollable page. | `pytest --screenshot on --full-page-screenshot` |

Run `pytest --help` to confirm the exact list for your installed version; options evolve between releases.

**Headed vs headless.** Headless means the browser runs without a window. It is faster and works on servers that have no screen. Headed is for development: you can see what is happening. A common workflow is to write and debug headed, then run headless in CI.

**Multiple browsers.** Repeating `--browser` runs each test once per browser:

```bash
pytest --browser chromium --browser firefox --browser webkit
```

Test names then show the browser, such as `test_valid_login[chromium]`. This is *cross-browser testing*: confirming your app behaves correctly in all major engines. Be aware it multiplies your run time by the number of browsers.

### 4. Artifacts for debugging: screenshots, video, traces

When a test fails on a server you cannot watch, you need evidence. Playwright produces three kinds.

**Screenshots**

```bash
pytest --screenshot only-on-failure
```

A PNG of the page is saved under `test-results/<test-name>/` when the test fails.

**Videos**

```bash
pytest --video retain-on-failure
```

A video of the browser session is recorded for each test and kept only for failures.

**Traces (the most powerful)**

```bash
pytest --tracing retain-on-failure
```

A trace is a `.zip` file containing a timeline of every action, a DOM snapshot before and after each action, network requests, console messages, and the source line. Open it with:

```bash
playwright show-trace test-results/test-login-test-valid-login-chromium/trace.zip
```

(The exact folder name depends on your test; PyTest prints it, or look inside `test-results`.) The Trace Viewer lets you click through each step as if time-travelling. A recommended team default is `--tracing retain-on-failure` plus `--screenshot only-on-failure`: cheap when everything passes, rich when something breaks.

> Playwright's trace and debugging tools are broad; today we focus on enabling and opening a trace. The Inspector (separate lesson today) handles live debugging.

### 5. Configuring defaults in `pytest.ini`

Typing long commands is tedious and easy to get wrong. Put your defaults in `pytest.ini` (Monday), using `addopts`:

```ini
[pytest]
addopts = --tracing retain-on-failure --screenshot only-on-failure -v
base_url = https://www.saucedemo.com
testpaths = tests
markers =
    smoke: quick checks that the app is alive
    regression: broader checks run before a release
```

- `addopts` adds those options to every run.
- `base_url` is a setting provided by `pytest-playwright`, so relative paths work in `page.goto("/")`.
- `testpaths` tells PyTest where to look.
- `markers` registers custom markers.

A command-line option given at run time overrides the ini value. For example, `pytest --headed` still works with the file above.

### 6. Configuring browser contexts

Each test gets a browser context; you can configure it through fixtures. The plugin looks for a fixture called `browser_context_args` (session scope) that returns a dictionary of options passed to `browser.new_context()`. Override it in `conftest.py`:

```python
# conftest.py
import pytest


@pytest.fixture(scope="session")
def browser_context_args(browser_context_args):
    return {
        **browser_context_args,
        "viewport": {"width": 1280, "height": 720},
        "locale": "en-US",
        "timezone_id": "America/New_York",
        "ignore_https_errors": True,
    }
```

Explanation:

- The fixture takes the *original* `browser_context_args` as a parameter (the plugin's default) and returns a new dictionary starting with the old values (`**browser_context_args` unpacks them) and then adds or overrides keys.
- `viewport` sets the window size, important because responsive sites change layout by width.
- `locale` and `timezone_id` make date/number formatting deterministic regardless of where tests run.
- `ignore_https_errors` is useful for test environments with self-signed certificates. Do not use it for real production checks.

Similarly, `browser_type_launch_args` controls how the browser is launched:

```python
@pytest.fixture(scope="session")
def browser_type_launch_args(browser_type_launch_args):
    return {**browser_type_launch_args, "slow_mo": 100}
```

There are also marker-based per-test options:

```python
import pytest

@pytest.mark.skip_browser("firefox")
def test_only_chromium_and_webkit(page):
    ...

@pytest.mark.only_browser("chromium")
def test_chromium_only(page):
    ...
```

`skip_browser` and `only_browser` are markers provided by the plugin for browser-specific tests.

### 7. Timeouts

- **Action timeout** (clicks, fills): default 30 seconds.
- **`expect()` timeout**: default 5 seconds.
- **Navigation timeout**: default 30 seconds.

Change them per page:

```python
page.set_default_timeout(10_000)              # all actions, milliseconds
page.set_default_navigation_timeout(45_000)   # navigations
```

Or for a single assertion:

```python
expect(locator).to_be_visible(timeout=15_000)
```

Raising a timeout is acceptable for genuinely slow operations (a report that takes 12 seconds to generate), but never use a huge timeout to hide a problem; it just makes failures slow.

### 8. Parallel execution and retries

Install the `pytest-xdist` plugin (a general PyTest plugin, not Playwright-specific):

```bash
pip install pytest-xdist
pytest -n 4          # four worker processes
pytest -n auto       # one worker per CPU core
```

Because each test gets its own browser context, tests are naturally isolated and safe to run in parallel *as long as they do not share external state* (for example, two tests editing the same user account in the database). Tests that violate this need separate data or must not run in parallel.

To re-run failures automatically, use `pytest-rerunfailures`:

```bash
pip install pytest-rerunfailures
pytest --reruns 2 --reruns-delay 1
```

Treat retries as a safety net and a *signal*, not a cure. A test that passes only on retry is flaky and should be investigated (see Common Mistakes).

### 9. Where do results go?

By default Playwright writes artifacts to `test-results/`. Add this folder to `.gitignore`, because artifacts are build output, not source code. HTML reporting (which you built on Wednesday) can be combined with Playwright artifacts:

```bash
pytest --html=report.html --self-contained-html --tracing retain-on-failure
```

---

## Code Examples

### Example 1: Project layout

```
project1-qe/
    pytest.ini
    conftest.py
    tests/
        test_login.py
        test_inventory.py
```

`pytest.ini`:

```ini
[pytest]
addopts = -v --tracing retain-on-failure --screenshot only-on-failure
base_url = https://www.saucedemo.com
testpaths = tests
markers =
    smoke: quick sanity checks
    regression: full regression
```

`conftest.py`:

```python
import pytest
from playwright.sync_api import Page, expect


@pytest.fixture(scope="session")
def browser_context_args(browser_context_args):
    return {**browser_context_args, "viewport": {"width": 1366, "height": 768}}


@pytest.fixture
def logged_in_page(page: Page) -> Page:
    page.goto("/")
    page.locator("#user-name").fill("standard_user")
    page.locator("#password").fill("secret_sauce")
    page.locator("#login-button").click()
    expect(page).to_have_url("/inventory.html")
    return page
```

Note `expect(page).to_have_url("/inventory.html")`: when `base_url` is configured, a relative URL is resolved against it in `to_have_url`. This keeps environment switching to one setting.

`tests/test_login.py`:

```python
import pytest
from playwright.sync_api import Page, expect


@pytest.mark.smoke
def test_valid_login(logged_in_page: Page):
    expect(logged_in_page.locator(".title")).to_have_text("Products")


@pytest.mark.regression
def test_empty_form_shows_error(page: Page):
    page.goto("/")
    page.locator("#login-button").click()
    expect(page.locator("[data-test='error']")).to_contain_text("Username is required")
```

### Example 2: Commands for different situations

```bash
# 1. Developer debugging: watch it run, slowly
pytest tests/test_login.py::test_valid_login --headed --slowmo 700

# 2. Fast smoke check
pytest -m smoke

# 3. Cross-browser regression, in parallel
pytest -m regression --browser chromium --browser firefox -n 4

# 4. Against another environment
pytest --base-url https://staging.example.com -m smoke

# 5. Mobile emulation
pytest tests/test_login.py --device "iPhone 13" --browser webkit

# 6. Keep every video and trace (investigating something odd)
pytest --video on --tracing on
```

Line by line, example 1: the node id (`file::function`) selects exactly one test (Monday); `--headed` shows the window; `--slowmo 700` waits 700 ms between operations so humans can follow.

### Example 3: Opening a trace

```bash
pytest tests/test_login.py --tracing on
playwright show-trace test-results/<folder>/trace.zip
```

In the Trace Viewer: the left column lists actions (such as `locator.fill`), the middle shows a DOM snapshot at that moment (you can hover to see what was targeted), and the bottom tabs show Source, Network, Console and Errors. Clicking a failed action shows the page exactly as Playwright saw it.

### Example 4: Browser-specific tests

```python
import pytest
from playwright.sync_api import Page, expect


@pytest.mark.only_browser("chromium")
def test_feature_supported_only_in_chromium(page: Page):
    page.goto("/")
    expect(page).to_have_title("Swag Labs")


def test_browser_name_is_available(page: Page, browser_name: str):
    print(f"Running on {browser_name}")
    page.goto("/")
```

`browser_name` is a fixture; it returns the name of the current browser, useful for conditional logic or reporting.

### Example 5: Custom per-test timeouts through a fixture

```python
@pytest.fixture(autouse=True)
def default_timeouts(page: Page):
    page.set_default_timeout(10_000)
    page.set_default_navigation_timeout(20_000)
```

`autouse=True` (Tuesday) means it runs for every test without being requested. Because it requests `page`, it applies to the same page the test receives (PyTest caches a fixture per test).

---

## Real-World Scenarios

1. **CI pipeline.** The pipeline runs `pytest -m smoke -n 4 --tracing retain-on-failure --output artifacts`. After the run, the `artifacts` folder is uploaded. A failed test links to its trace, so engineers diagnose without reproducing locally.
2. **Cross-browser bug.** A checkout button works in Chromium but is misaligned in WebKit (Safari engine). The team added `--browser webkit` to the nightly job and caught the issue before customers did.
3. **Mobile layout checks.** Product owners care about phones. `--device "Pixel 5"` re-runs the same test with a mobile viewport, touch support and user agent, with no new code.

---

## Common Mistakes

1. **Putting `--headed` in `addopts` and then breaking CI.** CI servers have no display; keep defaults headless and add `--headed` only locally.
2. **Forgetting to register markers**, leading to warnings or errors under `--strict-markers`.
3. **Running in parallel with shared data.** Two tests using the same user cart can interfere. Design tests to use independent data.
4. **Using retries to hide flakiness.** If a test needs `--reruns 3` to pass, find the root cause (usually bad waits or shared state).
5. **Overriding `browser_context_args` without including the original.** If you write `return {"viewport": ...}` alone, you lose plugin defaults such as the base URL and recorded video settings. Always spread the original with `**browser_context_args`.
6. **Committing `test-results/`** to source control. Add it to `.gitignore`.
7. **Huge global timeouts.** A 120 second timeout turns a quick failure into a two-minute wait per broken test.
8. **Expecting `--slowmo` in CI.** It is a debugging aid only.
9. **Mixing up `-k` and `-m`.** `-k` matches names; `-m` matches markers.

---

## Practice Exercises

**Exercise 1.** Create the project layout from Example 1. Run `pytest` and confirm the tests are collected from `tests/` only.

**Exercise 2.** Run the smoke test headed with `--slowmo 1000`. Observe each step. Then run it headless in three browsers. How many test results appear? *(Answer: one per browser, so three.)*

**Exercise 3.** Deliberately break a locator (change `#login-button` to `#login-buton`) and run with `--tracing retain-on-failure --screenshot only-on-failure`. Find the files in `test-results/`, open the trace, and identify which action failed and why. Fix the locator.

**Exercise 4.** Add a session-scoped `browser_context_args` fixture that sets the viewport to 375x667 (phone size). Write a test that checks a mobile-specific behavior (for SauceDemo, verify the burger menu button `#react-burger-menu-btn` is visible).

**Exercise 5.** Install `pytest-xdist` and run your tests with `-n 2`. Compare the run time with a serial run. Which tests might not be safe for parallel running in a real application, and why?

**Exercise 6 (Project 1).** Add `smoke` and `regression` markers to your Project 1 UI tests, register them in `pytest.ini`, and write a one-paragraph note explaining which commands the team should run (a) before every commit, (b) nightly.

*Hint:* before every commit run only smoke tests, headless, in one browser; nightly run everything in multiple browsers in parallel.

---

## Summary

- Playwright for Python uses PyTest as its runner; `pytest-playwright` adds fixtures and options.
- Important options: `--headed`, `--browser`, `--slowmo`, `--device`, `--base-url`, `--screenshot`, `--video`, `--tracing`, `--output`.
- Use traces (`--tracing retain-on-failure`) with `playwright show-trace` for powerful post-mortem debugging.
- Put project defaults in `pytest.ini` and context settings in `conftest.py` fixtures such as `browser_context_args`.
- Use `pytest-xdist` for parallel execution and `pytest-rerunfailures` carefully; flaky tests should be fixed, not hidden.
- All the filtering skills from Monday (`-k`, `-m`, node ids) apply unchanged.

---

## Additional Resources

- Playwright for Python: Pytest plugin reference: https://playwright.dev/python/docs/test-runners
- Playwright for Python: Trace Viewer: https://playwright.dev/python/docs/trace-viewer
- Pytest documentation: How to invoke pytest: https://docs.pytest.org/en/stable/how-to/usage.html
