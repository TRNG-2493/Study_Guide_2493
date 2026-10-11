# Playwright Reporting

## Learning Objectives

By the end of this lesson you will be able to:

- Explain why test reporting matters and name the different audiences for a report (the engineer who fixes failures, the team lead who tracks health, the stakeholder who wants a go/no-go).
- Read pytest's **console output** effectively: verbosity flags, the short test summary (`-r` options), `--durations`, and exit codes.
- Generate machine-readable results with **JUnit XML** (`--junitxml`) for CI systems.
- Install and use **`pytest-html`** to create a shareable HTML report, including `--self-contained-html`, report title, metadata, extra columns, and embedded **screenshots on failure** through the `pytest_runtest_makereport` hook.
- Use the **pytest-playwright artifact options**: `--screenshot`, `--video`, `--tracing`, `--output`, and understand where files are written.
- Open and navigate a **Playwright trace** (the Trace Viewer): actions, snapshots, network, console, and source.
- Record traces manually with the `context.tracing` API for special cases.
- Understand how **reruns**, parametrised tests, and parallel runs appear in reports.
- Compare reporting options (pytest-html, JUnit XML consumers, Allure) and decide what to use.
- Publish reports and artifacts in CI and write a short **failure triage routine** that uses them.

---

## Why This Matters

A test that no one can understand when it fails has little value. Imagine your suite of 300 UI tests finishes at 03:00 and 14 are red. The engineer who opens the pipeline at 09:00 needs to answer quickly: *Which tests failed? On which browser? What did the page look like? What was the error? Is it a product bug, a test bug, or the environment? Did it fail before? Was it retried?* Reporting is how you answer those questions in minutes instead of hours.

Reporting is the final topic in this week's structure-and-framework theme. Fixtures give you reliable setup; hooks capture evidence; the Page Object Model and JSON data keep tests maintainable; retries absorb transient noise. **Reports are where all of that becomes visible** to the team and to management. A framework without reporting is invisible; a framework with clear reports builds trust.

There is a direct Project 1 connection. **Project 1 - QE Foundations** is a portfolio deliverable: a hiring manager or instructor may never run your suite, but they will open your report. A clean HTML report with screenshots of a deliberately failing test, a trace file for debugging, and a README explaining how to generate them show that you think about *consumers* of test results, which is a hallmark of a professional QE. The Wednesday exercise asks you to refactor Project 1 UI tests into POM with data-driven JSON; adding a generated report to that repository is the natural finishing touch.

We build on earlier topics: the failure-evidence hook (Hooks lesson) feeds pytest-html; readable parametrised test ids (Data-driven lesson) become readable rows in the report; the "rerun" outcomes (Retries lesson) show up as statuses.

> **Important accuracy note.** If you have read about the "Playwright HTML reporter" (`npx playwright show-report`), that belongs to the **Playwright Test runner for Node.js/TypeScript**. In Python we use **pytest** as the runner, so reporting comes from pytest and its plug-ins plus Playwright's own *artifacts* (screenshots, videos, traces). The concepts are the same; the tools differ.

---

## The Concept

### 1. The reporting stack in Python Playwright

Think of reporting as four layers, each building on the one below:

```
┌───────────────────────────────────────────────┐
│ 4. Dashboards / trend tools (Allure, CI UI)   │  history, trends, flake rates
├───────────────────────────────────────────────┤
│ 3. Shareable reports (pytest-html)            │  one file you can email
├───────────────────────────────────────────────┤
│ 2. Machine-readable results (JUnit XML)       │  CI systems parse these
├───────────────────────────────────────────────┤
│ 1. Console output + exit codes (pytest)       │  immediate feedback
└───────────────────────────────────────────────┘
          plus: Playwright artifacts (screenshots, video, traces)
```

You will use layers 1 to 3 plus the artifacts in this lesson, and learn how layer 4 fits in.

### 2. Layer 1: Console output and exit codes

The terminal is the first report. Learn to read it.

```bash
pytest                    # dots and letters: . pass, F fail, E error, s skip, x xfail, R rerun
pytest -v                 # one line per test with its full node id and result
pytest -q                 # quiet: fewer lines
pytest -ra                # after the run, show a summary of ALL non-passing outcomes ("a" = all except pass)
pytest -rA                # summary of everything including passes
pytest --durations=10     # list the 10 slowest tests (setup, call, teardown phases)
pytest -x                 # stop at first failure
pytest --lf               # re-run only tests that failed last time
pytest --tb=short         # shorter tracebacks (also: long, line, no)
pytest -s                 # do not capture print output (see prints live)
```

An example summary:

```
=========================== short test summary info ============================
FAILED tests/test_login_data_driven.py::test_invalid_login_shows_error[wrong-password] - AssertionError: ...
RERUN  tests/test_checkout_data_driven.py::test_checkout_validation[missing-first-name]
========= 1 failed, 11 passed, 1 rerun in 48.12s =========
```

Because you used `ids` in your parametrised tests, the failing scenario is named: `[wrong-password]`. That is the payoff of good ids.

**Exit codes** matter to CI. pytest exits with `0` when all tests pass, `1` when some failed, `2` when interrupted by the user, `3` internal error, `4` command-line usage error, `5` no tests collected. A CI pipeline treats any non-zero code as failure. If you need to publish reports even when tests fail, make the "publish" step run regardless (Section 11).

**Live logging.** To see Python `logging` output as tests run, add to `pytest.ini`:

```ini
log_cli = true
log_cli_level = INFO
```

Using the `logging` module (`import logging; log = logging.getLogger(__name__); log.info("Logged in as %s", user)`) inside page objects makes the console and report tell the story of each step. Logs are captured and attached to failures automatically ("Captured log call" in the failure section and in pytest-html).

### 3. Layer 2: JUnit XML

**JUnit XML** is a de-facto standard format for test results, originally from the Java world. Almost every CI tool (Jenkins, GitHub Actions summaries, Azure DevOps, GitLab, TeamCity) can read it to display test counts, trends, and failures natively.

```bash
pytest --junitxml=reports/junit.xml
```

A trimmed example of the file:

```xml
<testsuites>
  <testsuite name="pytest" errors="0" failures="1" skipped="0" tests="12" time="48.1">
    <testcase classname="tests.test_login_data_driven" name="test_invalid_login_shows_error[wrong-password]" time="2.4">
      <failure message="AssertionError: ...">...stack trace...</failure>
    </testcase>
    ...
  </testsuite>
</testsuites>
```

Notes:

- Each `<testcase>` is one test; `<failure>` or `<error>` or `<skipped>` children record non-passing results.
- Add metadata with the built-in `record_property` fixture: `record_property("browser", browser_name)` adds a `<property>` element for the test.
- Add `junit_family=xunit2` in `pytest.ini` (`junit_family = xunit2`) for the modern schema; it avoids deprecation warnings and keeps property support consistent.
- Treat JUnit XML as **input for tools**, not as something humans read.

### 4. Layer 3: `pytest-html`, a shareable HTML report

**`pytest-html`** is a plug-in that produces a single HTML file summarising a run: counts, a filterable results table, durations, error details, captured output, environment metadata, and attached extras such as screenshots.

Install and run:

```bash
pip install pytest-html
pytest --html=reports/report.html --self-contained-html
```

- `--html=PATH` selects the output file (folders are created if needed).
- `--self-contained-html` embeds CSS and assets (including images as base64) into that one file, so you can email it or upload it as an artifact without worrying about missing folders. **Always use it** for reports you plan to share.

Open `reports/report.html` in a browser. You will see:

- A summary with counts of passed, failed, skipped, xfailed, xpassed, error, and rerun, and toggles to show/hide each category.
- An **Environment** table (Python version, platform, plug-in versions, and anything you add).
- A results table: result, test node id, duration, and a "Links" column for extras. Click a row to expand details such as the traceback and captured stdout/stderr/log.

You can set the options once in `pytest.ini`:

```ini
[pytest]
addopts = --html=reports/report.html --self-contained-html
```

### 5. Customising the pytest-html report with hooks

pytest-html is customised with ordinary pytest hooks in `conftest.py`. Here are the most useful. (These use the current major version, pytest-html 4.x. Hook details changed between major versions; if a hook does not behave as shown, check which version you have with `pip show pytest-html` and read its documentation.)

**5.1 Report title**

```python
# conftest.py
def pytest_html_report_title(report):
    report.title = "SauceDemo UI Regression - Playwright + pytest"
```

**5.2 Environment metadata**

```python
import pytest
from pytest_metadata.plugin import metadata_key


def pytest_configure(config):
    config.stash[metadata_key]["Application"] = "SauceDemo"
    config.stash[metadata_key]["Base URL"] = config.getoption("--base-url") or config.getini("base_url")
    config.stash[metadata_key]["Tester"] = "Your Name"
```

- `pytest-metadata` is a dependency of pytest-html; it collects environment details.
- `config.stash[metadata_key]` is a dictionary; each key/value you add appears in the Environment table.
- `config.getoption("--base-url")` reads the command-line option (or `None`); `config.getini("base_url")` reads the ini value. The `or` operator picks the first non-empty one.

(An older style, `config._metadata[...]`, appears in older tutorials. Prefer the `stash` approach with current versions.)

**5.3 Add a "Description" column from test docstrings**

```python
import pytest


@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item, call):
    outcome = yield
    report = outcome.get_result()
    report.description = (item.function.__doc__ or "").strip()


def pytest_html_results_table_header(cells):
    cells.insert(2, "<th>Description</th>")


def pytest_html_results_table_row(report, cells):
    cells.insert(2, f"<td>{getattr(report, 'description', '')}</td>")
```

Line by line:

- The hook wrapper (from the Hooks lesson) stores the test function's **docstring** on the report object. `item.function.__doc__` is the text in triple quotes below `def`. `or ""` guards against `None` when there is no docstring.
- `pytest_html_results_table_header(cells)` receives the list of header cells (HTML strings); `insert(2, ...)` puts a new column at index 2.
- `pytest_html_results_table_row(report, cells)` does the same for each row. The row hook must insert a cell at the *same index* as the header, or the table misaligns.
- Result: write a one-line docstring in each test and it becomes a readable description in the report. For example: `"""Locked-out users must see the lock-out message."""`.

**5.4 Screenshot on failure inside the report**

This combines the failure-evidence idea from the Hooks lesson with pytest-html's `extras`.

```python
# conftest.py
import base64

import pytest
from pytest_html import extras


@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item, call):
    outcome = yield
    report = outcome.get_result()
    report.description = (item.function.__doc__ or "").strip()
    setattr(item, f"rep_{report.when}", report)

    # Attach evidence when the test body (the "call" phase) fails
    if report.when == "call" and report.failed:
        page = item.funcargs.get("page")
        if page is not None and not page.is_closed():
            png_bytes = page.screenshot(full_page=True)
            encoded = base64.b64encode(png_bytes).decode("utf-8")
            report_extras = getattr(report, "extras", [])
            report_extras.append(extras.png(encoded, name="Failure screenshot"))
            report_extras.append(extras.url(page.url, name="Page URL at failure"))
            report.extras = report_extras
```

Line by line:

- `from pytest_html import extras` imports helper constructors (`extras.png`, `extras.url`, `extras.text`, `extras.html`, `extras.json`, `extras.image`).
- `report.when == "call" and report.failed` restricts to a failing test body (not setup or teardown).
- `item.funcargs.get("page")` fetches the `page` fixture value if the test used one.
- `not page.is_closed()` avoids an error if something already closed the page. At the time `makereport` runs for the `call` phase, fixture teardown has **not** happened yet, so the page is open, which is exactly why this hook is a good place to screenshot.
- `page.screenshot(full_page=True)` returns PNG **bytes** (no `path` argument).
- `base64.b64encode(...).decode("utf-8")` converts bytes to a base64 text string. pytest-html expects image content as base64 when the report is self-contained.
- `extras.png(encoded, name="Failure screenshot")` creates an image attachment; `extras.url(...)` adds a clickable link.
- `report.extras = ...` stores the list for pytest-html to render in the row's expanded section.

> **Parametrised tests and extras:** the same hook handles all rows, so each failing row gets its own screenshot. This is another reason the data-driven lesson insisted on good ids.

### 6. Playwright's own artifacts: screenshots, video, traces

`pytest-playwright` can record artifacts without any hook code. They are controlled by command-line options (or `addopts` in `pytest.ini`).

| Option | Values | Meaning |
|---|---|---|
| `--screenshot` | `on`, `off`, `only-on-failure` | Take a screenshot at the end of each test (or only if it failed). |
| `--video` | `on`, `off`, `retain-on-failure` | Record a video of each test; with `retain-on-failure`, videos of passing tests are deleted. |
| `--tracing` | `on`, `off`, `retain-on-failure` | Record a Playwright trace; keep only for failures if requested. |
| `--output` | folder path | Where artifacts go (default `test-results`). |
| `--full-page-screenshot` | flag (recent versions) | Capture the full scrollable page rather than the viewport. |

Example:

```bash
pytest --screenshot only-on-failure --video retain-on-failure --tracing retain-on-failure --output test-results
```

Result structure after a failure (names are derived from the test's node id):

```
test-results/
└── tests-test-login-data-driven-py-test-invalid-login-shows-error-wrong-password-chromium/
    ├── test-failed-1.png
    ├── video.webm
    └── trace.zip
```

Notes:

- Artifacts are per test **and per browser** (the browser name is part of the folder name), which matters when running `--browser chromium --browser firefox`.
- The default output folder is deleted and recreated at the start of every run, so do not store anything precious there. Add `test-results/` and `reports/` to `.gitignore`.
- Recording video and traces has a performance cost. The usual professional compromise is **`retain-on-failure` in CI** and **`on` only when debugging**.

### 7. The Trace Viewer: your best debugging tool

A **trace** is a recording of everything Playwright did in a test: every action, with before/after DOM snapshots, screenshots, network requests, console messages, and the source line that triggered each action. Opening it is like a time machine for the test.

Open a trace file:

```bash
playwright show-trace test-results/<test-folder>/trace.zip
```

or drag the `trace.zip` file onto the web viewer at **https://trace.playwright.dev**. (The web viewer runs entirely in your browser; the file is not uploaded.)

What you will see:

1. **Actions list (left):** each Playwright call (`Locator.fill`, `Locator.click`, `expect.to_have_url`, ...) with its duration. A red marker shows the failing step.
2. **Timeline (top):** a filmstrip of screenshots over time. Hover to scrub.
3. **Snapshot panel (centre):** the page at the selected moment, with tabs for **Before**, **Action** (where the click happened is highlighted) and **After**. You can interact with the DOM snapshot and inspect elements with DevTools-like tools.
4. **Details panel (right/bottom):** tabs for **Call** (parameters, locator resolution, timing and the "waiting for..." log), **Log**, **Errors**, **Console**, **Network** (every request/response with timing), **Source** (your test code with the failing line highlighted), and **Attachments**.

How to use it to triage a failure:

- Click the red failing action. Read the **Errors** tab, then the **Call log** which shows what Playwright was waiting for (for example, "waiting for locator ... element is not visible").
- Look at the **Before** snapshot: was the page in the state you expected? Was an overlay or cookie banner present?
- Check **Network**: did an API return 500? Did a request never complete?
- Check **Console**: JavaScript errors often explain missing elements.
- Compare with the trace of a passing attempt (if the test was retried).

**Recording traces manually.** Besides `--tracing`, you can control tracing in code, for example to trace only a risky section or to create traces in non-pytest scripts:

```python
def test_checkout_with_manual_trace(context, page):
    context.tracing.start(screenshots=True, snapshots=True, sources=True)

    page.goto("/")
    # ... steps ...

    context.tracing.stop(path="reports/traces/checkout.zip")
```

- `screenshots=True` captures a filmstrip, `snapshots=True` records DOM snapshots (needed for the clickable page view), `sources=True` includes your source code.
- `context.tracing.stop(path=...)` writes the zip file. If you use `--tracing on` as well, pytest-playwright already manages tracing for the context; avoid starting a second trace on the same context. A fixture-based approach with `tracing.start_chunk()` / `stop_chunk()` is available for splitting traces by phase, covered in the official trace viewer docs.

### 8. Reruns, parametrisation, and parallel runs in reports

- **Reruns:** with `pytest-rerunfailures`, earlier failed attempts are reported as **rerun** and the final attempt as passed or failed. pytest-html shows a "rerun" filter checkbox; JUnit shows additional testcase entries. A good practice is to look at the count of reruns on every report; a rising count signals growing flakiness.
- **Parametrised tests:** each row is its own result with its own id, duration, and extras.
- **Multiple browsers:** with `--browser chromium --browser firefox --browser webkit` every test runs once per browser, appearing as separate results with the browser suffix in the id (for example `test_x[chromium]`).
- **Parallel runs:** with `pytest-xdist` (`pip install pytest-xdist`, `pytest -n auto`), tests are distributed across processes. pytest-html and JUnit work with xdist and merge results into one report. Make sure artifacts do not collide; pytest-playwright's per-test output folders already handle this.

### 9. Other reporting tools (awareness)

| Tool | What it adds | When to consider it |
|---|---|---|
| **pytest-html** | Simple single-file HTML report | Default for course work, quick sharing, small teams |
| **JUnit XML + CI UI** | Native display in CI dashboards | Always generate it in CI |
| **Allure Report** (`allure-pytest`) | Rich dashboard: steps, history, trends, categories, attachments | Teams that need historical trend analysis; requires the Allure command-line tool to generate the HTML |
| **pytest-json-report** | JSON output for custom dashboards | When you build custom analytics |
| **Cloud dashboards** | Hosted history and analytics | Large organisations |

This course uses pytest-html and Playwright traces as the primary tools. Allure is mentioned for awareness; you may meet it in industry projects.

### 10. Making reports effective: what to include

A report is only useful if it helps someone *decide* or *fix*. Aim for:

1. **Identity:** application, environment URL, build number or commit SHA, browser(s), date/time. (Use metadata.)
2. **Clear test names:** descriptive function names and ids; docstrings as descriptions.
3. **Evidence on failure:** screenshot, URL, trace file path, console log, request failures.
4. **Context on retries:** count of reruns.
5. **Timing:** durations and the slowest tests (`--durations`).
6. **Traceability:** markers like `@pytest.mark.smoke`; optionally requirement ids stored via `record_property("requirement", "REQ-12")` for JUnit.
7. **Stable location:** artifacts saved under predictable paths (`reports/`, `test-results/`) so that CI can upload them.

### 11. Reports in CI (GitHub Actions example)

On a CI server, no one is watching the browser. The report and artifacts are the only evidence, so publish them, **even when tests fail**.

```yaml
# .github/workflows/ui-tests.yml
name: UI tests
on: [push, pull_request]

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v5
        with:
          python-version: "3.12"
      - run: pip install -r requirements.txt
      - run: playwright install --with-deps chromium
      - name: Run tests
        run: pytest --html=reports/report.html --self-contained-html --junitxml=reports/junit.xml --tracing retain-on-failure --screenshot only-on-failure --reruns 1
      - name: Upload reports and traces
        if: always()
        uses: actions/upload-artifact@v4
        with:
          name: test-reports
          path: |
            reports/
            test-results/
```

Explanation:

- `playwright install --with-deps chromium` installs the browser and the operating-system libraries it needs on a Linux runner.
- The test step runs with reports enabled.
- `if: always()` on the upload step is critical: by default a step is skipped when a previous step failed, which would throw away exactly the evidence you need.
- `path:` lists the folders to bundle into a downloadable artifact named `test-reports`.
- Download the artifact from the workflow run page, open `report.html`, and open `trace.zip` files with `playwright show-trace`.

(Pipeline syntax differs per CI vendor; the principles are identical. Pipelines are explored further in later weeks of the programme.)

### 12. A failure-triage routine using the report

1. Open the report; filter to **Failed** and **Error**. Note any **Rerun** entries.
2. For each failure, read the **error message** and **screenshot** to classify: *product bug*, *test bug*, *data*, *environment*.
3. Open the **trace** for any failure whose cause is not obvious.
4. Reproduce locally with `--reruns 0 --headed --slowmo 300` if needed.
5. File a defect (product bug) with the screenshot and trace attached, or fix the test (and note the root cause in the commit message).
6. Rerun only the failed tests: `pytest --lf`.

---

## Code Examples

### Example A: A complete reporting setup for the SauceDemo framework

**`pytest.ini`**

```ini
[pytest]
base_url = https://www.saucedemo.com
pythonpath = .
testpaths = tests
junit_family = xunit2
addopts =
    --html=reports/report.html
    --self-contained-html
    --junitxml=reports/junit.xml
    --screenshot only-on-failure
    --video retain-on-failure
    --tracing retain-on-failure
    --output test-results
    -ra
```

`addopts` can be written across multiple lines (indented continuation). `-ra` appends a summary of non-passing outcomes to the console output.

**`conftest.py`** (reporting portion)

```python
import base64

import pytest
from pytest_html import extras
from pytest_metadata.plugin import metadata_key


# ---- Report header and metadata ----
def pytest_html_report_title(report):
    report.title = "SauceDemo UI Regression"


def pytest_configure(config):
    config.stash[metadata_key]["Application"] = "SauceDemo"
    config.stash[metadata_key]["Base URL"] = config.getini("base_url")


# ---- Extra "Description" column ----
def pytest_html_results_table_header(cells):
    cells.insert(2, "<th>Description</th>")


def pytest_html_results_table_row(report, cells):
    cells.insert(2, f"<td>{getattr(report, 'description', '')}</td>")


# ---- Evidence on failure ----
@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item, call):
    outcome = yield
    report = outcome.get_result()
    report.description = (item.function.__doc__ or "").strip()

    if report.when == "call" and report.failed:
        page = item.funcargs.get("page")
        if page is not None and not page.is_closed():
            encoded = base64.b64encode(page.screenshot(full_page=True)).decode("utf-8")
            report_extras = getattr(report, "extras", [])
            report_extras.append(extras.png(encoded, name="Failure screenshot"))
            report_extras.append(extras.url(page.url, name="URL at failure"))
            report.extras = report_extras
```

Walkthrough: this file combines Section 5's four customisations. Notice there are no `print` statements or manual file saving; everything is pushed into the report. Reading `getattr(report, 'description', '')` with a default makes the row hook safe even for reports (such as setup errors) where no description was set.

**A test with a docstring**

```python
def test_invalid_login_shows_error(login_page, case):
    """Invalid credentials must show the documented error and keep the user on the login page."""
    login_page.login_as(case["username"], case["password"])
    expect(login_page.error_message).to_have_text(case["expected_error"])
```

### Example B: Making a failure on purpose to see the whole chain

```python
def test_demo_failure_for_report(login_page):
    """DELIBERATE FAILURE: used to check that evidence appears in the report."""
    login_page.login_as("standard_user", "secret_sauce")
    assert login_page.page.title() == "This Is Wrong On Purpose"
```

Run:

```bash
pytest tests/test_demo_failure.py
```

Then:

1. Open `reports/report.html`; expand the row; confirm the screenshot and URL extras appear.
2. Find `test-results/<folder>/trace.zip` and open it with `playwright show-trace`.
3. In the viewer, find the final `title()` call, read the error, and compare the **Before** snapshot with the expectation.
4. Delete the demo test (or tag it `@pytest.mark.skip` with a reason) before committing.

### Example C: Adding structured data to JUnit with `record_property`

```python
def test_checkout_complete(inventory_page, record_property, browser_name):
    record_property("requirement", "REQ-CHECKOUT-01")
    record_property("browser", browser_name)
    ...
```

- `record_property` is a built-in pytest fixture; each call adds a `<property name=... value=...>` element to the test's JUnit entry.
- Many CI/test-management tools can read these properties for traceability.

### Example D: Logging steps inside page objects for richer reports

```python
import logging

log = logging.getLogger(__name__)


class LoginPage(BasePage):
    def login_as(self, username: str, password: str) -> None:
        log.info("Logging in as %s", username)
        self.username_input.fill(username)
        self.password_input.fill(password)
        self.login_button.click()
```

- `logging.getLogger(__name__)` creates a logger named after the module.
- `"%s"` with a separate argument is the recommended logging style (the string is only formatted if the message is emitted).
- Never log passwords. Notice we log only the username.
- With `log_cli = true` you see steps live; failing tests display "Captured log call" in the console and in the pytest-html row, giving a narrative of what the test did before it failed.

---

## Real-World Scenarios

**Scenario 1: The 09:00 stand-up.** The lead opens the nightly `report.html` on the projector. Filters show 6 failures and 11 reruns. One failing screenshot shows a "503 Service Unavailable" page; the team immediately knows it is environmental and pings the platform team, rather than spending the stand-up debating.

**Scenario 2: Release sign-off.** A release manager needs evidence. The team archives `report.html`, `junit.xml` and the commit SHA as the sign-off artifact. Months later, an auditor can see exactly which tests ran and passed for release 4.2.

**Scenario 3: Remote debugging.** A test fails only in CI, not on a developer laptop. The developer downloads `trace.zip`, opens the Trace Viewer, and sees the **Network** tab showing a request to a feature-flag service timing out in CI. No need to reproduce on a CI machine.

**Scenario 4: Flake review.** Every Friday the QE team lists tests with a "rerun" outcome from the last five reports. Two tests appear four times; they are assigned for root-cause fixes. The reports make flakiness measurable.

**Scenario 5: Cross-browser report.** The report for `--browser chromium --browser webkit` shows that `test_sort_by_price[webkit]` fails alone. The screenshot reveals the dropdown rendering differently; the team discovers a genuine WebKit CSS bug.

---

## Common Pitfalls and Best Practices

**Pitfalls**

1. **Forgetting `--self-contained-html`.** The report depends on side files and breaks when moved or emailed.
2. **Not uploading reports when tests fail** in CI (missing `if: always()`).
3. **Artifacts overwritten or deleted.** The `test-results/` folder is recreated every run; copy what you need before the next run or let CI upload it.
4. **Committing reports and traces to Git.** They are large and change every run. Add `reports/`, `test-results/`, and `.auth/` to `.gitignore`.
5. **Recording video/trace for everything** on large suites, consuming disk and slowing runs. Use `retain-on-failure`.
6. **Taking screenshots after the page is closed** (in fixture teardown that ran too late). The `makereport` hook runs before fixture teardown for the `call` phase, so it is safe; just check `page.is_closed()`.
7. **Mismatched table hooks.** Header and row hooks must insert at the same index.
8. **Relying on tutorials for old pytest-html versions.** APIs changed (for example, `extra` vs. `extras`, `config._metadata` vs. `stash`). Check the installed version.
9. **Putting secrets in the report.** Screenshots, traces, HTML dumps, and console logs can include tokens, personal data, or credentials. Treat artifacts as sensitive and avoid logging passwords.
10. **Hard-to-read reports** because tests lack names/docstrings. A report full of `test_1`, `test_2` helps nobody.
11. **Using the Node.js reporter instructions** (`npx playwright show-report`, `--reporter=html`) for a Python project. They do not apply.
12. **Ignoring the report's rerun counts.** A "green" build with many reruns is unhealthy.

**Best practices**

- Always produce **both** an HTML report (humans) and JUnit XML (machines) in CI.
- Standardise output locations (`reports/`, `test-results/`) in `pytest.ini`.
- Capture evidence **only on failure** by default; switch to `on` when debugging.
- Add environment and build metadata to every report (commit SHA, URL, browser).
- Write meaningful test names, ids, and one-line docstrings.
- Keep the Trace Viewer in your daily routine: *open the trace before guessing*.
- Review reports as a team, not just when something is red.
- Document in the README: how to run, where reports go, how to open a trace.

---

## Mini Practice Exercises

**Exercise 1: console literacy.**
Run your suite with `-v`, then `-ra`, then `--durations=5`. Write down: how many tests ran, which are the three slowest, and which outcomes appear in the `-ra` summary.

**Exercise 2: first HTML report.**
Install `pytest-html`, run `pytest --html=reports/report.html --self-contained-html`, open the file, use the filters, and expand a test row. Take a screenshot of the report summary for your Project 1 notes.

**Exercise 3: title and metadata.**
Add `pytest_html_report_title` and `pytest_configure` metadata hooks. Regenerate the report and confirm that your title and "Application" row appear in the Environment table.

**Exercise 4: deliberate failure.**
Create the failing test from Example B. Verify the screenshot and URL extras show up in the report. Then fix it so it passes and confirm the extras disappear.
*Hint:* extras are only added when `report.failed` is true in the `call` phase.

**Exercise 5: Trace Viewer tour.**
Run `pytest --tracing on tests/test_login_data_driven.py -k wrong-password`. Open the trace and answer: (a) How many actions did the test perform? (b) Which request loaded the page? (c) What did the DOM look like *before* clicking "Login"? (d) On which line of your source did `to_have_text` run?

**Exercise 6: description column.**
Add the Description column hooks and a docstring to three tests. Confirm the column appears and is aligned.

**Exercise 7: CI artifact.**
Write the GitHub Actions workflow from Section 11 for your repository. Push a branch with a failing test and confirm the artifact is available for download even though the test step failed.

**Exercise 8 (Project 1 link):** Generate a final HTML report and a trace for your refactored Project 1 UI suite. Add a "Reporting" section to your README describing the commands, output folders, and how a reviewer can open the trace. Commit a *sample* `docs/sample-report.html` (self-contained) if your instructor requests it, but keep generated folders in `.gitignore`.

---

## Summary / Key Takeaways

- Reports serve different audiences: engineers need **evidence**, leads need **trends**, stakeholders need **status**.
- In Python Playwright the runner is **pytest**; reporting comes from pytest output, **JUnit XML**, **pytest-html**, and Playwright's artifacts: **screenshots, video, and traces**.
- Use `pytest --html=reports/report.html --self-contained-html` for a shareable report; customise title, metadata, columns, and attach **failure screenshots** using hooks and `extras`.
- Control artifacts with `--screenshot`, `--video`, `--tracing` (prefer `retain-on-failure`) and `--output`.
- The **Trace Viewer** (`playwright show-trace trace.zip` or trace.playwright.dev) shows actions, DOM snapshots, network, console, and source; open it *before* guessing at causes.
- Reruns, parametrised ids, browsers, and parallel workers all appear as distinct results; watch the rerun count as a health metric.
- In CI, always upload reports and artifacts with `if: always()`.
- Keep artifacts out of Git, keep secrets out of artifacts, and document how to read the reports.

---

## External Resources

- Playwright for Python, "Trace Viewer": https://playwright.dev/python/docs/trace-viewer
- Playwright for Python, "Pytest plugin reference" (artifact options `--screenshot`, `--video`, `--tracing`, `--output`): https://playwright.dev/python/docs/test-runners
- pytest-html documentation: https://pytest-html.readthedocs.io/en/latest/
