# Hooks

## Learning Objectives

By the end of this lesson you will be able to:

- Define a "hook" in test automation and explain the difference between **setup/teardown hooks** (what you run before and after tests) and **pytest plug-in hooks** (functions pytest calls at specific moments of a test run).
- Implement "before each / after each" behaviour in pytest using `yield` fixtures, and explain why this is the preferred approach for Playwright tests.
- Use `autouse` fixtures to run setup and teardown around every test.
- Use classic xunit-style hooks (`setup_module`, `setup_class`, `setup_method`, and their `teardown_` partners) and know when they are appropriate.
- Write hooks in `conftest.py`: `pytest_addoption`, `pytest_configure`, `pytest_collection_modifyitems`, `pytest_runtest_setup`, `pytest_runtest_makereport`, `pytest_sessionstart`, and `pytest_sessionfinish`.
- Capture a screenshot, page URL, and page HTML **automatically when a test fails**, using the `pytest_runtest_makereport` hook.
- Skip or mark tests dynamically from a hook.
- Avoid the common traps: hook order, `hookwrapper` mistakes, hooks that hide failures, and work done in hooks that belongs in fixtures.

---

## Why This Matters

Every automated test, no matter the tool, follows the same lifecycle: **prepare the world**, **do the thing**, **check the result**, **clean up**. Preparing and cleaning up are not the interesting part of a test, so frameworks provide *hooks*: places to attach code that runs automatically at specific moments, such as "before each test", "after each test", "once before everything", or "when a test fails".

This week's epic is about structuring Playwright tests with fixtures, hooks, and the Page Object Model so that a team can maintain hundreds of them. Hooks are what turn a loose pile of scripts into a *framework*:

- A **failure hook** that takes a screenshot means that when a nightly run fails at 3 a.m., the engineer in the morning has visual evidence instead of a mystery.
- A **setup hook** that clears cookies or resets test data stops one test from poisoning the next.
- A **session hook** that prints the environment name at the start of the run prevents "which environment was this?" confusion.
- **Collection hooks** let you automatically mark or skip tests by name or folder.

For **Project 1 - QE Foundations**, a rubric item for a professional test project is almost always "evidence on failure" (screenshots, logs, traces). In pytest, that evidence is produced by hooks, and you will write exactly that hook today.

> **Cross-tool note.** If you have seen Mocha, Jasmine, or the Playwright Test runner for JavaScript, you may know hooks called `beforeEach` and `afterEach`. Cypress also has hooks with similar names; we cover those in depth on Thursday. pytest does not use those names. In pytest, the idiomatic equivalent is a *fixture with `yield`*. This lesson shows you how to translate your thinking.

---

## The Concept

### 1. Two different things people call "hooks"

The word is overloaded, so let us separate the two meanings right away.

1. **Setup/teardown hooks (lifecycle code you write for your tests).** "Run this before each test; run that after each test." In pytest you implement these with fixtures (recommended) or the older xunit-style methods.
2. **Plug-in hooks (extension points pytest itself defines).** pytest announces events during a run ("a test is about to be set up", "a test report was just created", "the session is finishing"). Any function in `conftest.py` named exactly like one of these events (`pytest_runtest_makereport`, `pytest_configure`, ...) is called by pytest at that moment. You **do not decorate** most of them; the *name* is the contract.

Beginners often mix these up. A helpful question: "Am I preparing something for a test, or am I reacting to something pytest is doing?" Preparing is a fixture. Reacting is a plug-in hook.

### 2. Setup and teardown with `yield` fixtures (the recommended way)

You learned in the previous lesson that code before `yield` runs before the test and code after `yield` runs after. That *is* "before each / after each".

```python
# conftest.py
import pytest
from playwright.sync_api import Page


@pytest.fixture
def clean_page(page: Page):
    # --- "beforeEach" part ---
    page.context.clear_cookies()
    page.goto("/")
    yield page
    # --- "afterEach" part ---
    page.evaluate("window.localStorage.clear()")
```

Line by line:

- `@pytest.fixture` registers the function; it is function-scoped by default, so it runs once per test: a "before/after each".
- `page: Page` receives the built-in `page` fixture.
- `page.context.clear_cookies()` removes all cookies from the browser context. (Each test already has a fresh context, so this is redundant here; we show it to illustrate the "before" slot.)
- `page.goto("/")` opens the base URL.
- `yield page` pauses the fixture and gives the page to the test.
- After the test finishes (pass *or* fail), execution resumes after `yield`, and `localStorage` is cleared via `page.evaluate`, which runs JavaScript in the page.

Why is this preferred over separate "before" and "after" functions?

- **Setup and teardown live side by side**, so you cannot forget the cleanup half.
- **Only tests that request it** pay the price (unless it is `autouse`).
- **Teardown runs even if setup partly fails**, up to the point of the failure, because pytest tracks which fixtures finished setting up.
- It composes: fixtures can request other fixtures.

### 3. `autouse` fixtures: hooks that apply to every test

To make a fixture behave like a global "beforeEach/afterEach", add `autouse=True`:

```python
@pytest.fixture(autouse=True)
def default_timeouts(page):
    page.set_default_timeout(10_000)             # actions & assertions wait up to 10 s
    page.set_default_navigation_timeout(30_000)  # page loads wait up to 30 s
    yield
```

- `10_000` is Python's way of writing 10000 with a readable underscore separator.
- `page.set_default_timeout(ms)` changes the default wait for actions such as `click()` and `fill()`; `set_default_navigation_timeout` does the same for navigation methods such as `goto()`.
- A bare `yield` (no value) is fine when there is nothing to give the test. Here there is no teardown, so the `yield` could even be replaced with `return`. We kept `yield` to show the shape.

**Caution about autouse + `page`:** an autouse fixture that requests `page` forces a browser page to be created for *every* test in scope, even non-browser tests such as unit tests of a helper function. If your project mixes both kinds of tests, scope the autouse fixture to the UI folder by placing it in `tests/ui/conftest.py`.

### 4. Fixture scope as hook granularity

Frameworks like xUnit talk about "before suite / before class / before test". In pytest, **scope** gives you all of these with the same mechanism:

| You want to run... | Use this |
|---|---|
| Once before the whole run | `@pytest.fixture(scope="session", autouse=True)` |
| Once per test file | `scope="module"` (autouse if needed) |
| Once per test class | `scope="class"` |
| Before each test | default `scope="function"` |

Example "before all / after all" at session scope:

```python
@pytest.fixture(scope="session", autouse=True)
def banner(base_url):
    print(f"\n==== Run started against: {base_url} ====")
    yield
    print("==== Run finished ====")
```

- `base_url` is the fixture from the previous lesson. (If you did not configure one it will be `None`.)
- The first `print` executes before the first test. The second executes after the last.
- Use `pytest -s` to see `print` output live; otherwise pytest captures it.

### 5. Classic xunit-style hooks

pytest also supports a family of special function names inherited from the xUnit tradition (JUnit, unittest). You will meet them in older codebases.

```python
# tests/test_xunit_style.py

def setup_module(module):
    print("\nsetup_module: runs once before the first test in this FILE")


def teardown_module(module):
    print("teardown_module: runs once after the last test in this FILE")


class TestCart:
    @classmethod
    def setup_class(cls):
        print("\nsetup_class: once before the first test in this CLASS")

    @classmethod
    def teardown_class(cls):
        print("teardown_class: once after the last test in this CLASS")

    def setup_method(self, method):
        print("\nsetup_method: before EACH test method")

    def teardown_method(self, method):
        print("teardown_method: after EACH test method")

    def test_one(self):
        assert True

    def test_two(self):
        assert True
```

Line by line:

- `setup_module(module)` / `teardown_module(module)` are plain functions at the file's top level, called once per file.
- Inside a class, `@classmethod` methods `setup_class(cls)` / `teardown_class(cls)` run once per class. `@classmethod` is a Python decorator that makes the method receive the *class* (`cls`) rather than an instance.
- `setup_method(self, method)` / `teardown_method(self, method)` run around each test method. `method` is the test function object about to run.
- Plain function tests outside a class can use `setup_function(function)` and `teardown_function(function)`.

**Limitations that explain why fixtures are preferred:**

- You cannot easily pass a value from a `setup_method` to a test except by assigning to `self`, which hides the dependency.
- You cannot request built-in fixtures like `page` in the signature; you would need workarounds.
- They are tied to classes/modules, not reusable across files without inheritance tricks.

Use xunit-style only when maintaining legacy code or when a team strongly prefers class-based tests. For new Playwright work, use fixtures.

### 6. Plug-in hooks in `conftest.py`

These are functions with specific names that pytest calls. Put them in `conftest.py`. Below are the ones that matter most for UI automation. The full catalogue is in pytest's API reference ("Hook reference").

#### 6.1 `pytest_addoption(parser)`: add your own command-line options

```python
# conftest.py
def pytest_addoption(parser):
    parser.addoption(
        "--env",
        action="store",
        default="demo",
        choices=["demo", "staging"],
        help="Target environment name used in report metadata",
    )
```

- `parser` is pytest's argument parser. `addoption` works like Python's `argparse.add_argument`.
- `action="store"` means "store the value given after the flag".
- `default="demo"` is used when the user omits the flag.
- `choices=[...]` rejects unknown values with a helpful message.
- Tests or fixtures read it with `request.config.getoption("--env")` or `pytestconfig.getoption("env")`.

```python
@pytest.fixture(scope="session")
def env_name(request):
    return request.config.getoption("--env")
```

Run: `pytest --env staging`.

> **Warning:** `pytest_addoption` must live in a root-level `conftest.py` (or a plug-in), because options are registered before test collection starts.

#### 6.2 `pytest_configure(config)`: once, at startup

```python
def pytest_configure(config):
    config.addinivalue_line(
        "markers", "smoke: quick checks that run on every commit"
    )
    config.addinivalue_line(
        "markers", "regression: full coverage tests"
    )
```

- `config` is the pytest configuration object.
- `addinivalue_line("markers", "name: description")` registers a custom marker so `pytest --markers` lists it and so `--strict-markers` will not reject it. (You can also declare markers in `pytest.ini`.)

#### 6.3 `pytest_collection_modifyitems(config, items)`: change the list of collected tests

After pytest finds all tests (the "collection" phase), it gives you the list. You can add markers, reorder, or deselect.

```python
import pytest


def pytest_collection_modifyitems(config, items):
    for item in items:
        # Auto-mark every test inside a folder called 'smoke' with the smoke marker
        if "smoke" in item.nodeid:
            item.add_marker(pytest.mark.smoke)

        # Put slow tests last
    items.sort(key=lambda it: it.get_closest_marker("slow") is not None)
```

- `items` is a list of *test items*; each has `nodeid` (a string like `tests/smoke/test_login.py::test_valid`), `name`, `get_closest_marker`, and `add_marker`.
- `item.add_marker(pytest.mark.smoke)` attaches the marker dynamically.
- `items.sort(key=...)` sorts in place. The `key` function returns `False` (0) for tests without a `slow` marker and `True` (1) for those with it; `False < True`, so slow tests go to the end. `lambda it: ...` is an inline anonymous function.

#### 6.4 `pytest_runtest_setup(item)`: before each test's setup

```python
def pytest_runtest_setup(item):
    if "wip" in item.keywords and not item.config.getoption("--run-wip", default=False):
        pytest.skip("work in progress; use --run-wip to include")
```

- `item.keywords` contains the marker names and test name parts.
- `pytest.skip(reason)` skips the test with a message. (This example assumes a `--run-wip` flag you registered with `pytest_addoption`.)

#### 6.5 `pytest_runtest_makereport(item, call)`: the most important one for failure evidence

pytest runs each test in three **phases**: `setup` (fixtures are created), `call` (the test body), and `teardown` (fixtures are cleaned up). After each phase, pytest builds a **report** object saying whether that phase passed, failed, or was skipped. The hook `pytest_runtest_makereport` lets you observe, and even modify, that report.

To use it correctly, you need one new concept: a **hook wrapper**.

A *wrapper* hook surrounds the normal implementations. Code before `yield` runs before pytest builds the report; `yield` hands control to pytest, which builds the report; code after `yield` can inspect the finished report. In current pytest (8.x) you can write it in two equivalent ways:

```python
# Style 1: classic hookwrapper (works in all modern pytest versions)
@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item, call):
    outcome = yield              # pytest builds the report
    report = outcome.get_result()
    ...
```

```python
# Style 2: new-style wrapper (pytest 8+)
@pytest.hookimpl(wrapper=True)
def pytest_runtest_makereport(item, call):
    report = yield               # the yield expression returns the result directly
    ...
    return report                # new-style wrappers must return the result
```

The two differ in mechanics (in Style 2 you must `return` the result), but achieve the same goal. This course uses Style 1 because it works across versions and is widespread in tutorials and existing code.

**Step 1: store the report on the test item so fixtures can read it.**

```python
# conftest.py
import pytest


@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item, call):
    outcome = yield
    report = outcome.get_result()
    # Save as rep_setup, rep_call, rep_teardown on the item
    setattr(item, f"rep_{report.when}", report)
```

Line by line:

- `@pytest.hookimpl(hookwrapper=True)` tells pluggy (the plug-in system under pytest) that this function wraps other implementations.
- `def pytest_runtest_makereport(item, call):` `item` is the test; `call` describes the phase that just ran (including `call.excinfo`, the exception info if it raised).
- `outcome = yield` runs the real report-building code and returns an `Outcome` object.
- `outcome.get_result()` extracts the `TestReport`.
- `report.when` is one of `"setup"`, `"call"`, `"teardown"`.
- `setattr(item, "rep_call", report)` dynamically creates an attribute named `rep_call` (or `rep_setup`, `rep_teardown`) on the test item. `f"rep_{report.when}"` builds that name with an **f-string**.

**Step 2: use it in a fixture to take a screenshot on failure.**

```python
# conftest.py (continued)
from datetime import datetime
from pathlib import Path

ARTIFACT_DIR = Path("reports/failures")


@pytest.fixture
def page_with_evidence(page, request):
    """A page that saves a screenshot and the HTML when its test fails."""
    yield page                                   # the test body runs here
    # --- after the test ---
    rep = getattr(request.node, "rep_call", None)
    if rep is None or not rep.failed:
        return                                   # no call phase, or it passed

    ARTIFACT_DIR.mkdir(parents=True, exist_ok=True)
    stamp = datetime.now().strftime("%Y%m%d-%H%M%S")
    safe_name = "".join(c if c.isalnum() or c in "-_" else "_" for c in request.node.name)
    base = ARTIFACT_DIR / f"{safe_name}-{stamp}"

    page.screenshot(path=f"{base}.png", full_page=True)
    Path(f"{base}.html").write_text(page.content(), encoding="utf-8")
    print(f"\nFailure evidence saved: {base}.png / .html  (URL: {page.url})")
```

Line by line:

- `def page_with_evidence(page, request)` requests the built-in `page` and the built-in `request` fixture, which gives access to the current test through `request.node`.
- `yield page` pauses; the test body runs with the page; then we continue below.
- `getattr(request.node, "rep_call", None)` safely reads the attribute stored by our hook. If setup failed, the test body never ran and `rep_call` does not exist, so we default to `None`. (Without this safety you would get `AttributeError`.)
- `rep.failed` is `True` when the `call` phase failed.
- `ARTIFACT_DIR.mkdir(parents=True, exist_ok=True)` creates the folder and any missing parents, without error if it already exists.
- `datetime.now().strftime(...)` makes a timestamp string so successive failures do not overwrite each other.
- `safe_name` is built with a **generator expression**: it keeps letters, digits, `-` and `_`, and replaces everything else with `_`. Parametrised test names contain characters such as `[`, `]` and `/` that are awkward in file names.
- `page.screenshot(path=..., full_page=True)` saves a PNG of the whole scrollable page.
- `page.content()` returns the full current HTML; `Path.write_text` saves it.
- The final `print` tells the engineer where to look.

> **Why does this fixture take `page` as a parameter?** Fixtures are torn down in the reverse order of their setup. Because `page_with_evidence` requests `page`, `page` is set up first and torn down **last**, so when our code after `yield` runs, the page is still open. If you instead wrote an `autouse` fixture that did *not* request `page` and fished it out of `request.node.funcargs`, it might be set up *before* `page` and therefore torn down *after* it, meaning the page could already be closed when you try to screenshot it. Always make the dependency explicit.

**Pytest-playwright already has built-in failure screenshots.** You can get this behaviour without any hook at all: `pytest --screenshot only-on-failure --tracing retain-on-failure --video retain-on-failure`. We still teach the hook because (a) you will learn the pattern that powers *every* custom failure behaviour (logging, sending a Slack message, saving browser console logs), and (b) a custom hook lets you control file names and add the HTML dump.

#### 6.6 `pytest_sessionstart(session)` and `pytest_sessionfinish(session, exitstatus)`

```python
def pytest_sessionstart(session):
    print("\n[hook] Session starting")


def pytest_sessionfinish(session, exitstatus):
    print(f"\n[hook] Session finished with exit status {exitstatus}")
```

- `session` is the object representing the whole run.
- `exitstatus` is an integer: `0` all passed, `1` some failed, `2` interrupted, `5` no tests collected, etc.
- Typical real uses: archive report folders, send a notification, clean up shared test data.

#### 6.7 `pytest_report_header(config)`: add lines to the console header

```python
def pytest_report_header(config):
    return [f"Target: {config.getoption('--env')}", "Application: SauceDemo"]
```

pytest prints each returned string at the top of the run output. Great for making log files self-explanatory.

### 7. Order of execution (the full picture)

For one test run in a session, the order is:

```
pytest_sessionstart
pytest_configure                       (actually earlier, during startup)
pytest_collection_modifyitems
  session-scoped fixtures setup       (as first needed)
    module-scoped fixtures setup
      pytest_runtest_setup
        function-scoped fixtures setup  (autouse first, then requested)
        TEST BODY
        function-scoped fixtures teardown (reverse order)
      pytest_runtest_makereport  (after each phase: setup, call, teardown)
    module-scoped fixtures teardown
  session-scoped fixtures teardown
pytest_sessionfinish
```

Use `pytest --setup-show` to see the fixture part for real, and add `print` statements in hooks to see the rest. Understanding this order explains most "why did X happen before Y?" confusion.

---

## Code Examples

### Example A: Failure-evidence fixture with console log capture

This builds on Step 2 above by also recording the browser's console messages, which are often the quickest clue to a front-end failure.

```python
# conftest.py
from datetime import datetime
from pathlib import Path

import pytest

ARTIFACT_DIR = Path("reports/failures")


@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item, call):
    outcome = yield
    report = outcome.get_result()
    setattr(item, f"rep_{report.when}", report)


@pytest.fixture
def page_with_evidence(page, request):
    """A page that saves a screenshot, HTML and console log when its test fails."""
    console_messages = []
    page.on("console", lambda msg: console_messages.append(f"[{msg.type}] {msg.text}"))

    yield page                                          # the test body runs here

    rep = getattr(request.node, "rep_call", None)
    if rep is not None and rep.failed:
        ARTIFACT_DIR.mkdir(parents=True, exist_ok=True)
        stamp = datetime.now().strftime("%H%M%S")
        name = "".join(c if c.isalnum() or c in "-_" else "_" for c in request.node.name)
        base = ARTIFACT_DIR / f"{name}-{stamp}"

        page.screenshot(path=f"{base}.png", full_page=True)
        Path(f"{base}.html").write_text(page.content(), encoding="utf-8")
        Path(f"{base}.log").write_text("\n".join(console_messages), encoding="utf-8")
```

Line by line (new parts only):

- `page.on("console", handler)` registers an **event listener**. Playwright calls the handler for every `console.log`, `console.error` and so on from the page. `lambda msg: ...` is a short anonymous function receiving a `ConsoleMessage`; `msg.type` is `"log"`, `"error"`, `"warning"`, etc.; `msg.text` is the message.
- `console_messages` collects strings for later saving. Because the lambda refers to this list, it "closes over" it, so every message is appended to the same list.
- `"\n".join(console_messages)` joins the list into lines for the `.log` file.

In your tests, request `page_with_evidence` instead of `page`:

```python
def test_locked_out_user_sees_error(page_with_evidence):
    page = page_with_evidence
    page.goto("/")
    page.get_by_test_id("username").fill("locked_out_user")
    page.get_by_test_id("password").fill("secret_sauce")
    page.get_by_test_id("login-button").click()
    assert "locked out" in page.get_by_test_id("error").inner_text()
```

If this ever fails, three files appear in `reports/failures/`.

### Example B: Feeding the `makereport` hook into pytest-html

If you use `pytest-html` (covered in the Reporting lesson), the same hook is where you attach the screenshot to the report. A preview:

```python
import base64
import pytest


@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item, call):
    outcome = yield
    report = outcome.get_result()
    setattr(item, f"rep_{report.when}", report)

    if report.when == "call" and report.failed:
        page = item.funcargs.get("page")
        if page is not None:
            png = page.screenshot()
            encoded = base64.b64encode(png).decode("utf-8")
            from pytest_html import extras
            report.extras = getattr(report, "extras", []) + [extras.png(encoded, "Failure screenshot")]
```

- `page.screenshot()` without a `path` returns the PNG as `bytes`.
- `base64.b64encode(...).decode("utf-8")` converts bytes to a text string that can be embedded directly in an HTML file.
- `report.extras` is the list of attachments pytest-html will render in its row. (Details and the exact API version differences are in the Reporting lesson.)

### Example C: Environment banner with a custom option

```python
# conftest.py
def pytest_addoption(parser):
    parser.addoption("--env", default="demo", help="demo or staging")


def pytest_report_header(config):
    return f"Environment: {config.getoption('--env')}"


@pytest.fixture(scope="session")
def env_name(pytestconfig):
    return pytestconfig.getoption("--env")
```

`pytestconfig` is a built-in session-scoped fixture returning the config object, a convenient alternative to `request.config`.

### Example D: Skipping tests dynamically by browser

```python
# conftest.py
import pytest


@pytest.fixture(autouse=True)
def skip_if_not_supported(request, browser_name):
    marker = request.node.get_closest_marker("skip_on")
    if marker and browser_name in marker.args:
        pytest.skip(f"Not supported on {browser_name}")
```

```python
@pytest.mark.skip_on("webkit")
def test_feature_unavailable_on_webkit(page):
    ...
```

- `get_closest_marker("skip_on")` finds a custom marker on the test (register it via `pytest_configure`).
- `marker.args` is a tuple of the arguments passed to the marker (`("webkit",)`).
- `browser_name` is the built-in fixture from pytest-playwright.
- pytest-playwright also has built-in markers `@pytest.mark.skip_browser("webkit")` and `@pytest.mark.only_browser("chromium")` which do the same job without custom code. Prefer the built-ins; this example is for understanding.

---

## Real-World Scenarios

**Scenario 1: Debugging a nightly failure.** A regression suite of 400 tests runs at night. Five fail. Thanks to the failure hook, each failure has a PNG, an HTML snapshot, and console messages, so the engineer discovers within minutes that a third-party analytics script logged a JavaScript error and the page showed a cookie banner that blocked the "Login" button.

**Scenario 2: Environment safety.** A `pytest_sessionstart` hook checks the `--env` option and aborts the whole run (`pytest.exit("Refusing to run destructive tests against production")`) if someone accidentally points the suite at a production URL.

**Scenario 3: Quarantine.** A team marks unstable tests with `@pytest.mark.flaky_known`. A `pytest_collection_modifyitems` hook deselects them on the main CI job but includes them on a separate "quarantine" job, so they never block merging but are still monitored. (Retries are the subject of a later lesson today.)

**Scenario 4: Clean test data.** Every test that creates an order through the UI registers the order ID in a list. An autouse fixture's teardown deletes them through an API call, so the shared QA environment does not fill up with junk.

---

## Common Pitfalls and Best Practices

**Pitfalls**

1. **Forgetting `yield` in a hookwrapper.** A `hookwrapper=True` hook that never yields raises an error. A wrapper must yield exactly once.
2. **Not calling `outcome.get_result()` safely.** In a hookwrapper, if you skip the `yield`, you never get the report. If you use the new-style wrapper (`wrapper=True`) you must `return` the result.
3. **Reading `rep_call` when it does not exist.** If setup failed, there is no call phase. Always use `getattr(item, "rep_call", None)`.
4. **Autouse fixtures that quietly start browsers.** An autouse fixture with `page` as a parameter starts a page for all tests in its scope. Keep it in the UI folder's `conftest.py`.
5. **Teardown-order surprises.** An autouse evidence fixture that does not depend on `page` may be torn down *after* `page` is closed. Make the dependency explicit.
6. **Swallowing failures in hooks.** Wrapping your hook body in `try: ... except Exception: pass` hides bugs in your framework. If evidence capture fails, at least `print` the exception.
7. **Heavy work in hooks.** A hook that does network calls on every test slows the suite down. Do slow things only on failure or once per session.
8. **Putting `pytest_addoption` in a nested `conftest.py`.** It is not honoured reliably; keep it in the root.
9. **Using `time.sleep` in setup to wait for things.** Use Playwright's auto-waiting (`expect(...)`, `wait_for_url`).
10. **Hooks that depend on test order.** Each test must succeed alone, in any order. Hooks should prepare *independent* state.

**Best practices**

- Prefer **fixtures** for anything a test conceptually *needs*; prefer **plug-in hooks** for things that *react to the run*.
- Keep hook functions small and named clearly; delegate real work to helper functions in a `utils/` module.
- Put one-time environment setup in session fixtures, not in every test's first lines.
- Log which environment, browser, and base URL each run used (`pytest_report_header`).
- Let the built-in `--screenshot`, `--video`, `--tracing` options do the common cases, and write custom hooks only for what they cannot do.
- Test your hooks: deliberately make a test fail and check that the evidence appears.

---

## Mini Practice Exercises

**Exercise 1: observe the order.**
Create `conftest.py` with `pytest_sessionstart`, `pytest_runtest_setup`, `pytest_runtest_makereport` (hookwrapper, printing `report.when` and `report.outcome`), and `pytest_sessionfinish`, each printing a line. Add a fixture with `yield` and print statements. Run `pytest -s` with two tests and draw the order of lines you see.
*Hint:* each test produces three reports: setup, call, teardown.

**Exercise 2: before/after each.**
Write an autouse yield fixture in `conftest.py` that prints "START <test name>" before and "END <test name>" after each test. Run with `-s`.
*Solution sketch:*
```python
@pytest.fixture(autouse=True)
def boundaries(request):
    print(f"\nSTART {request.node.name}")
    yield
    print(f"END {request.node.name}")
```

**Exercise 3: failure screenshot.**
Implement the `page_with_evidence` fixture. Write a test that fails on purpose (`assert page.title() == "Wrong Title"`). Confirm that a PNG, HTML and log file appear. Then delete the failing line and confirm nothing is written.

**Exercise 4: custom option.**
Add `--user` (choices `standard_user`, `problem_user`) via `pytest_addoption`. Create a session fixture `username` returning it, and use it in a login test. Run with `pytest --user problem_user`.

**Exercise 5: dynamic marker.**
Use `pytest_collection_modifyitems` to add the marker `smoke` to every test whose name starts with `test_smoke_`. Verify with `pytest -m smoke --collect-only -q`.

**Exercise 6 (Project 1 link):** Add a failure-evidence hook to your Project 1 repository and commit a screenshot of a deliberately failing test's evidence folder (remove the failing test afterwards). Add the folder to `.gitignore`.

---

## Summary / Key Takeaways

- A **hook** is a place to attach code to a moment in the test lifecycle. Two families exist: **setup/teardown code you write** (fixtures, xunit-style) and **plug-in hooks pytest calls** (`pytest_*` functions).
- In pytest, "beforeEach/afterEach" is a **function-scoped `yield` fixture**; "beforeAll/afterAll" is a **session- or module-scoped** one. `autouse=True` applies it automatically.
- xunit-style (`setup_method`, `setup_class`, `setup_module`) works but is less flexible; use it mainly for legacy code.
- Important plug-in hooks: `pytest_addoption`, `pytest_configure`, `pytest_collection_modifyitems`, `pytest_runtest_setup`, `pytest_runtest_makereport`, `pytest_sessionstart`, `pytest_sessionfinish`, `pytest_report_header`.
- `pytest_runtest_makereport` as a **hookwrapper** is the standard way to learn whether a test failed, and to attach evidence (screenshots, HTML, console logs).
- Teardown happens in **reverse order**; make evidence fixtures depend on `page` so the page is still open.
- Built-in `--screenshot`, `--video`, and `--tracing` flags cover common cases; custom hooks cover the rest.

---

## External Resources

- pytest documentation, "Writing hook functions": https://docs.pytest.org/en/stable/how-to/writing_hook_functions.html
- pytest documentation, "API Reference: Hooks": https://docs.pytest.org/en/stable/reference/reference.html#hooks
- Playwright for Python, "Pytest plugin reference": https://playwright.dev/python/docs/test-runners
