# HTML Reporting

## Learning Objectives

By the end of this lesson you will be able to:

- Explain why test reports matter and who reads them.
- Read and interpret PyTest's built-in terminal report (outcomes, summaries, `-ra`, `-v`, `-q`, tracebacks).
- Install `pytest-html` and generate an HTML report with `--html`.
- Produce a **self-contained** single-file report that can be emailed or attached to a ticket.
- Open and navigate the report: summary, environment table, filters, results table, expandable details.
- Customise the report: title, environment metadata, extra columns, extra content (text, JSON, URLs, images), and collapsed rows.
- Generate machine-readable reports (JUnit XML) for CI tools and know when to use each format.
- Organise report output into a `reports/` folder with timestamped filenames, and add reporting options to `pytest.ini`.
- Troubleshoot common reporting problems.

---

## Why This Matters

The weekly epic is to build up from PyTest basics to a **reporting framework** for Project 1 – QE Foundations. Writing and running tests is only half of a tester's job; the other half is **communicating results**.

Think about who needs your results:

- **You**, to find out what failed and why.
- **Teammates and developers**, to reproduce a defect.
- **Managers and product owners**, who do not read code but need to know "Is this build safe to release?"
- **Auditors and clients**, who sometimes require evidence that testing took place.
- **CI/CD pipelines**, which need a machine-readable result to decide whether to continue deploying.

A terminal full of dots scrolls away. A shareable, well-formed HTML report is a *deliverable*. In Project 1 you will hand over not only tests, but proof of their results. A manager can open `report.html` in a browser, see "48 passed, 2 failed", click the two failures and read the exact error, without installing Python.

---

## The Concept

### 1. PyTest's built-in terminal report

Before adding any plugin, learn what PyTest already prints. Suppose you have the following file, `test_demo_report.py`:

```python
import pytest


def test_passes():
    assert 1 + 1 == 2


def test_fails():
    assert "apple".upper() == "Apple"


@pytest.mark.skip(reason="feature not built yet")
def test_skipped():
    assert False


@pytest.mark.xfail(reason="known bug BUG-7")
def test_expected_failure():
    assert 2 * 2 == 5


@pytest.fixture
def broken_fixture():
    raise RuntimeError("setup exploded")


def test_error_in_setup(broken_fixture):
    assert True
```

Run `pytest`:

```
============================= test session starts ==============================
platform linux -- Python 3.12.3, pytest-8.3.2, pluggy-1.5.0
rootdir: /home/user/project1
configfile: pytest.ini
collected 5 items

test_demo_report.py .Fsx E                                               [100%]

=================================== ERRORS ====================================
...
=================================== FAILURES ===================================
...
=========================== short test summary info ============================
FAILED test_demo_report.py::test_fails - AssertionError: assert 'APPLE' == 'Apple'
ERROR test_demo_report.py::test_error_in_setup - RuntimeError: setup exploded
=== 1 failed, 1 passed, 1 skipped, 1 xfailed, 1 error in 0.05s ===
```

**Reading it:**

- **Header**: platform, Python and PyTest versions, `rootdir` and `configfile` (where PyTest found `pytest.ini`), and the number of collected tests.
- **Progress line**: one character per test: `.` pass, `F` fail, `s` skip, `x` xfail (expected failure), `X` xpass (unexpected pass), `E` error.
- **Failure details**: the code, the assertion introspection, and the traceback.
- **Short summary**: one line per non-pass (shown thanks to `-ra`).
- **Final line**: totals and elapsed time.

**Important vocabulary: fail vs error.** A **failure (F)** means the test body ran and an assertion (or other exception) failed. An **error (E)** means something went wrong *outside* the test body, usually in fixture setup or teardown. Distinguishing the two tells you whether the *product* misbehaved or the *test environment* is broken.

Useful flags:

| Flag | Effect |
|------|--------|
| `-v` | verbose: one line per test with its name and result |
| `-q` | quiet: shorter output |
| `-ra` | at the end, summarise all outcomes except passes (`-rA` includes passes) |
| `--tb=short` / `--tb=line` / `--tb=no` | traceback style |
| `-x` | stop at first failure |
| `--durations=5` | list the 5 slowest tests (more in the *Performance profiling* lesson) |

The terminal report is excellent for developers; the HTML report is for **everyone else**.

### 2. Installing `pytest-html`

`pytest-html` is a third-party **plugin**: an add-on package that PyTest discovers automatically once installed. It is maintained under the pytest-dev organisation.

```bash
# Activate your virtual environment first
python -m pip install pytest-html

# Check
python -m pip show pytest-html
pytest --version
```

If installation worked, `pytest --help` will list an option group containing `--html=path`. Add the dependency to `requirements.txt` so teammates get it too:

```
pytest>=8.0
pytest-html>=4.0
```

(Using `python -m pip` rather than bare `pip` guarantees the package is installed into the same Python you are running.)

### 3. Generating your first report

```bash
pytest --html=reports/report.html
```

- `--html=PATH` tells the plugin where to write the file. Parent folders (`reports/`) are created if needed.
- Open `reports/report.html` by double-clicking it or dragging it into a browser.

By default, the report references a separate CSS stylesheet and assets located in an `assets/` folder next to the HTML file. If you email only the `.html`, the formatting will be lost. The fix is the next flag.

### 4. The self-contained report

```bash
pytest --html=reports/report.html --self-contained-html
```

`--self-contained-html` embeds CSS, JavaScript and images **inside the single HTML file**. Use it whenever you:

- attach the report to an email, Jira ticket or chat,
- store it as a CI artifact,
- hand it to someone who is not on your network.

### 5. Anatomy of the report

When you open the HTML you will see (layout varies slightly between versions):

1. **Title and generation time**: `report.html` and a timestamp.
2. **Environment table**: Python version, platform, installed packages and plugins, and extra metadata you add.
3. **Summary**: counts per outcome with checkboxes to **filter** (Passed, Failed, Skipped, XFailed, XPassed, Errors).
4. **Results table**: one row per test: Result, Test (node ID such as `tests/unit/test_pricing.py::test_apply_discount[ten-percent]`), Duration, Links.
5. **Expandable details**: click a row to show the log, traceback and any extras (captured output, screenshots, links).
6. Sorting: click a column header to sort, for example by Duration to find slow tests.

Spend a few minutes clicking around the first time; most trainee questions ("where do I see why it failed?") are answered by clicking the row.

### 6. Organising reports: folders and timestamped names

Overwriting `report.html` every run loses history. Two common approaches:

#### Approach A: Shell-level timestamp

Windows PowerShell:

```powershell
$ts = Get-Date -Format "yyyyMMdd_HHmmss"
pytest --html="reports/report_$ts.html" --self-contained-html
```

macOS / Linux:

```bash
pytest --html="reports/report_$(date +%Y%m%d_%H%M%S).html" --self-contained-html
```

#### Approach B: Generate the name inside `conftest.py`

PyTest lets you modify configuration as it starts using the `pytest_configure` hook. Because it is a *hook*, the function name and parameter must match exactly:

```python
# conftest.py
from datetime import datetime
from pathlib import Path


def pytest_configure(config):
    # Only if the user did not pass --html explicitly and the plugin is present
    if hasattr(config.option, "htmlpath") and not config.option.htmlpath:
        reports = Path(__file__).parent / "reports"
        reports.mkdir(exist_ok=True)
        stamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        config.option.htmlpath = reports / f"report_{stamp}.html"
        config.option.self_contained_html = True
```

**Line-by-line:**

- `pytest_configure(config)` is called once at start-up.
- `config.option` holds parsed command-line options; the `pytest-html` plugin stores the output path under `htmlpath`.
- `hasattr(...)` guards against the plugin not being installed.
- `datetime.now().strftime("%Y%m%d_%H%M%S")` formats the current time such as `20250115_143005`; sortable and filesystem-safe (no colons).
- `Path.mkdir(exist_ok=True)` creates the folder if absent without error if it exists.
- Setting `self_contained_html` makes the report a single file.

Use Approach A for simplicity or when teammates have different needs; use Approach B for a consistent policy. Whichever you choose, add `reports/` to `.gitignore`.

### 7. Putting options in `pytest.ini`

Typing long commands is error-prone. Use `addopts` (introduced in the previous lesson):

```ini
[pytest]
testpaths = tests
addopts = -ra --strict-markers --html=reports/report.html --self-contained-html
```

Now plain `pytest` produces a report every run. The downside is that every local run also writes a report. Many teams leave reports out of `addopts` and add them in the CI script, so local runs are not slowed or cluttered. Choose based on your team's preference and document it in the README.

### 8. Customising the report title

`pytest-html` 4.x provides hooks you can implement in `conftest.py`. Hooks are special functions that plugins call; you simply define them.

```python
# conftest.py
def pytest_html_report_title(report):
    report.title = "Project 1 - QE Foundations: Automated Test Report"
```

Reload the report and the heading changes.

### 9. Adding environment metadata

The *Environment* table is populated by the companion package `pytest-metadata` (installed automatically with `pytest-html`). Add your own rows in `pytest_configure`:

```python
# conftest.py
import pytest
from pytest_metadata.plugin import metadata_key


def pytest_configure(config):
    config.stash[metadata_key]["Project"] = "Project 1 - QE Foundations"
    config.stash[metadata_key]["Tester"] = "Your Name"
    config.stash[metadata_key]["Environment"] = "QA"
    # Remove noisy or sensitive entries
    config.stash[metadata_key].pop("Packages", None)
    config.stash[metadata_key].pop("Plugins", None)
```

- `config.stash` is PyTest's typed storage area for plugins; `metadata_key` identifies the metadata dictionary.
- You can also pass values on the command line: `pytest --metadata Build 1.4.2 --metadata Branch main`.
- **Security tip:** never place passwords, API keys or tokens in metadata; reports get shared. (pytest-html 4 also redacts some information, but do not rely on it.)
- If you previously saw examples that use `config._metadata`, that is the older (pytest-metadata < 2) spelling; use `config.stash[metadata_key]` with current versions.

### 10. Adding a "Description" column

Make reports friendlier by showing each test's docstring in a new column. This uses three hooks together:

```python
# conftest.py
import pytest


def pytest_html_results_table_header(cells):
    cells.insert(2, "<th>Description</th>")


def pytest_html_results_table_row(report, cells):
    cells.insert(2, f"<td>{getattr(report, 'description', '')}</td>")


@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item, call):
    outcome = yield
    report = outcome.get_result()
    doc = item.function.__doc__ if hasattr(item, "function") else None
    report.description = (doc or "").strip()
```

And in a test:

```python
def test_apply_discount_typical():
    """Ten percent off 100 must give 90."""
    assert apply_discount(100.0, 10) == 90.0
```

**Explanation:**

- `pytest_html_results_table_header(cells)`: `cells` is a list of header cell HTML strings; we insert one at position 2 (third column).
- `pytest_html_results_table_row(report, cells)`: for each result row we insert the matching `<td>`. The number of cells in the header and in every row **must match**, or the table misaligns.
- `pytest_runtest_makereport` is the hook PyTest calls to create the result of each test phase. `@pytest.hookimpl(hookwrapper=True)` makes ours a **wrapper**: code before `yield` runs before PyTest's own implementation; `outcome = yield` pauses until it finishes; then `outcome.get_result()` gives the report object, to which we attach `description`.
- `item.function.__doc__` reads the test's docstring.
- Docstrings may contain characters like `<` or `&`; for production use consider escaping with `html.escape(...)`.

This pattern (attach data to `report` in `makereport`, display it in the table hooks) is the foundation of most report customisation. You do not need to memorise it; keep it as a snippet.

### 11. Adding extra content to a test's details

Extras let you attach text, JSON, URLs and images to a particular test's expandable area:

```python
# conftest.py
import pytest
import pytest_html


@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item, call):
    outcome = yield
    report = outcome.get_result()
    extras = getattr(report, "extras", [])

    if report.when == "call":
        # Attach information to every executed test; here only to failures
        if report.failed:
            extras.append(pytest_html.extras.text("Captured by conftest hook", name="Note"))
            extras.append(pytest_html.extras.url("https://example.com/bug-tracker", name="Bug tracker"))
        report.extras = extras
```

Available extra types in `pytest_html.extras` include `text`, `json`, `url`, `html`, `image`, `png`, `jpg`, `svg`, `mp4`. Tests can also add extras by using the `extras` fixture provided by the plugin:

```python
import pytest_html


def test_with_extra(extras):
    extras.append(pytest_html.extras.json({"user": "ana", "role": "tester"}, name="Payload"))
    assert True
```

- `report.when` is `"setup"`, `"call"` or `"teardown"` since a single test has three phases; we act on `"call"` (the test body itself).
- Screenshots are the most popular use of extras in UI automation: after a failed browser test you attach a PNG so the report shows what the page looked like. We will cover browser automation in depth on Thursday and Friday; the same mechanism will then let your Project 1 report show screenshots.

(The `extras` fixture and `pytest_html.extras` API are the pytest-html 4.x forms. If your installed version differs, check the "User guide" in the plugin documentation for the version you have.)

### 12. Controlling which rows are expanded

By default, pytest-html collapses passing tests and expands failing ones so the important rows are visible. Control this in `pytest.ini`:

```ini
[pytest]
render_collapsed = failed,error
```

- `render_collapsed = all` collapses everything; the value `failed,error` collapses only those; leaving it unset applies the default.
- Use this to tune how the report opens for your audience.

### 13. Other options: CSS, sorting, and capturing logs

- `--css=path/to/custom.css` adds your own stylesheet, for example a company colour scheme (repeat the option for multiple files).
- Captured output: PyTest captures `print` output and log messages for each test and pytest-html shows them in the details area for failures. Enable richer logs with `log_cli = true` or `--log-level=INFO` (see the PyTest logging documentation).
- Report from a subset of tests: `pytest -m smoke --html=reports/smoke.html --self-contained-html` produces a focused report.

### 14. Machine-readable reports: JUnit XML

HTML is for humans. CI/CD servers (Jenkins, GitLab CI, GitHub Actions, Azure DevOps) can consume **JUnit XML**, a standard format they display as test dashboards and trend charts. PyTest produces it **without any plugin**:

```bash
pytest --junitxml=reports/junit.xml
```

You can produce both at once:

```bash
pytest --html=reports/report.html --self-contained-html --junitxml=reports/junit.xml
```

Which format should you use?

| Format | Audience | Pros | Cons |
|--------|----------|------|------|
| Terminal | Developer running tests | instant, no setup | disappears |
| HTML (`pytest-html`) | People: testers, managers, clients | readable, shareable, screenshots | not easily machine-parsed |
| JUnit XML | CI tools | standard, trends, integrations | unreadable for humans |
| Allure and others (awareness) | Larger teams wanting rich dashboards | trends, history, attachments | more setup; separate server/CLI |

For Project 1 you need terminal + HTML (and optionally JUnit XML).

### 15. A complete worked example

Project layout:

```
reporting-demo/
├── pytest.ini
├── conftest.py
├── reports/            (created automatically)
└── tests/
    └── test_calculator.py
```

`pytest.ini`:

```ini
[pytest]
testpaths = tests
addopts = -ra --strict-markers
markers =
    smoke: quick sanity checks
```

`tests/test_calculator.py`:

```python
import pytest


def add(a, b):
    return a + b


def divide(a, b):
    return a / b


@pytest.mark.smoke
def test_add_positive_numbers():
    """Adding two positive numbers returns their sum."""
    assert add(2, 3) == 5


def test_add_deliberate_failure():
    """Demonstration failure: wrong expected value."""
    assert add(2, 2) == 5


def test_divide_by_zero_raises():
    """Division by zero must raise ZeroDivisionError."""
    with pytest.raises(ZeroDivisionError):
        divide(1, 0)


@pytest.mark.skip(reason="not implemented")
def test_modulo():
    """Modulo operation (skipped)."""
    assert False
```

`conftest.py`:

```python
import html
import pytest
from pytest_metadata.plugin import metadata_key


def pytest_configure(config):
    config.stash[metadata_key]["Project"] = "Reporting demo"
    config.stash[metadata_key]["Environment"] = "Local"


def pytest_html_report_title(report):
    report.title = "Calculator Test Report"


def pytest_html_results_table_header(cells):
    cells.insert(2, "<th>Description</th>")


def pytest_html_results_table_row(report, cells):
    cells.insert(2, f"<td>{html.escape(getattr(report, 'description', ''))}</td>")


@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item, call):
    outcome = yield
    report = outcome.get_result()
    func = getattr(item, "function", None)
    report.description = ((func.__doc__ if func else "") or "").strip()
```

Run:

```bash
pytest --html=reports/calculator_report.html --self-contained-html
```

Open `reports/calculator_report.html`. You should see title "Calculator Test Report", the Project/Environment entries, 2 passed / 1 failed / 1 skipped, a Description column, and the failing test expanded with its traceback and `assert 4 == 5`.

### 16. Reading a report like a professional tester

When you open a report, ask in this order:

1. **Is the overall result acceptable?** Compare totals with the previous run.
2. **Errors first** (E): environment/setup problems may hide many tests.
3. **Failures**: group by the same error message; one root cause often explains several failures.
4. **Skipped/xfailed**: are they intentional and documented? A growing skip count is a warning sign.
5. **Slow tests**: sort by Duration (more in the *Performance profiling* lesson).
6. **Flaky patterns**: does a test pass on re-run? Report it; do not hide it.

### 17. Troubleshooting

| Symptom | Likely cause | Fix |
|---------|--------------|-----|
| `unrecognized arguments: --html=...` | Plugin not installed in the active environment | `python -m pip install pytest-html`; check the virtual environment is active |
| Report has no styling when emailed | Missing `--self-contained-html` | Add the flag |
| `ModuleNotFoundError: pytest_metadata` | Installed plugin partially/incorrectly | Reinstall `pytest-html` (it brings `pytest-metadata`) |
| Columns misaligned | Header/row cell counts differ | Insert the same number of cells in both hooks |
| Report file not created | Run aborted at collection (syntax/import error) | Fix the collection error shown in the terminal |
| Old API in tutorials (`pytest_html_results_table_html`, `config._metadata`) fails | Tutorials written for pytest-html 3.x | Use the 4.x hook names shown here |
| Report overwritten each run | Fixed file name | Timestamp the name |

---

## Real-World Scenarios

1. **Daily smoke-test report.** A CI job runs `pytest -m smoke --html=reports/smoke.html --self-contained-html` after each deployment and posts the file as a pipeline artifact. Release managers open it before approving promotion.
2. **Client evidence.** For a regulated client, the QE team archives timestamped HTML reports per release, with environment metadata (build number, branch) stored in the Environment table.
3. **Triage meeting.** On Monday the team opens the weekend regression report, filters to *Failed*, sorts by test name and groups failures by error message to assign owners.
4. **UI test reports later this week.** Reports for browser tests include screenshots on failure. We will cover the browser tooling in depth on Thursday and Friday and reuse today's reporting hooks.

---

## Common Mistakes

| Mistake | Why it is a problem | Better approach |
|---------|--------------------|-----------------|
| Sharing only the `.html` without `--self-contained-html` | Broken formatting | Use the flag |
| Committing reports to git | Repository bloat and merge conflicts | `.gitignore` the `reports/` folder |
| Putting secrets in metadata | Reports are shared widely | Never include credentials |
| Treating HTML as the only report | CI cannot parse it | Also emit JUnit XML |
| Ignoring skips and xfails in the summary | Hidden risk | Review them with `-ra` |
| Copy-pasting hooks from old tutorials | API changed in 4.x | Check plugin version and docs |
| Different header/row cell counts | Broken table | Keep hook insertions symmetrical |
| Generating a report from a partial run and presenting it as the full suite | Misleading | Name reports clearly (`smoke`, `full`) |

---

## Practice Exercises

### Exercise 1: First report

Install `pytest-html`, create `test_demo_report.py` from section 1, and generate `reports/first.html` with the self-contained option. Identify the fail, error, skip and xfail rows. In one sentence each, explain how a failure differs from an error.

<details>
<summary>Hint</summary>
The failing row comes from `test_fails`; the error from `test_error_in_setup`, because the exception happened in a fixture, not in the test body.
</details>

### Exercise 2: Metadata and title

Change the title to include your name and add three metadata entries (Project, Environment, Build). Remove the "Plugins" and "Packages" entries. Regenerate and verify.

### Exercise 3: Timestamped filenames

Implement both approaches from section 6 (a shell command and the `pytest_configure` hook). Run PyTest three times and confirm three distinct files are produced.

### Exercise 4: Description column

Add the Description column from section 10 using the docstrings of your Monday tests. Add docstrings where they are missing. Escape the text with `html.escape`.

<details>
<summary>Solution check</summary>
Header and row hooks must each insert exactly one cell at the same index. If rows look shifted, compare the two insert indexes.
</details>

### Exercise 5: Filtered reports

Create three reports from your Project 1 tests: all tests, only `smoke`, and everything except `slow`. Use `-m` expressions. Compare the totals in the Summary section with `pytest --collect-only -q -m smoke`.

### Exercise 6: JUnit XML

Generate `reports/junit.xml`. Open it in a text editor and find the `tests`, `failures`, `errors` and `skipped` attributes. Explain which tool in a CI pipeline would use this file.

### Exercise 7: Project 1 deliverable

Produce a final self-contained HTML report for the full Project 1 PyTest suite, with a custom title, environment metadata (including build/date), and a Description column. Save it in `reports/`. Write a three-sentence summary a manager could understand: total tests, pass rate, and the most important failure (if any).

---

## Summary

- Reports serve different audiences: the terminal for developers, HTML for people, JUnit XML for machines.
- Learn the terminal report first: outcomes (`.`, `F`, `s`, `x`, `X`, `E`), failure vs error, `-ra`, `--tb`.
- Install `pytest-html` and run `pytest --html=reports/report.html --self-contained-html`.
- The report contains an environment table, summary filters, a sortable results table and expandable details.
- Customise through hooks in `conftest.py`: title, metadata via `config.stash[metadata_key]`, extra columns, extras (text, JSON, URL, images).
- Timestamp report files, keep them in `reports/`, and ignore them in version control.
- Use `--junitxml` for CI tooling; keep secrets out of reports; always read the report in a structured way.

---

## Additional Resources

- PyTest documentation - Plugin list (find `pytest-html` and its project page): https://docs.pytest.org/en/stable/reference/plugin_list.html
- PyTest documentation - Managing PyTest's output and JUnit XML (`--junitxml`): https://docs.pytest.org/en/stable/how-to/output.html
- PyTest documentation - Writing hook functions and plugins: https://docs.pytest.org/en/stable/how-to/writing_hook_functions.html
