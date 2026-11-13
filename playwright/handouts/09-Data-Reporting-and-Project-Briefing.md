# 09 — Data, Reporting and Project Briefing

> **Before you start**
>
> - **By the end you can:** run one test with many inputs, load test data from JSON, explain flaky tests and retries, produce an HTML report with failure screenshots, and put all your settings in `pytest.ini`.
> - **Practice site:** Swag Labs — <https://www.saucedemo.com/> (password `secret_sauce` for every user).
> - **Create:** a folder `lecture09/` by copying your whole `lecture08/` folder (`pages/`, `tests/`, `conftest.py`, `pytest.ini`). Then add two empty folders: `test_data/` and `utils/` (with an empty `__init__.py`).
> - **Check the two plugins are installed:** `pip install pytest-html pytest-rerunfailures`
> - **Start each new test file with:**
>
> ```python
> import re
> import pytest
> from playwright.sync_api import expect
> ```
>
> - **Run tests with:** `pytest -v` from inside `lecture09/`

---

## Topic 1 — `parametrize`

### Definition

`@pytest.mark.parametrize` runs **one test function many times with different data**. Each set of values becomes a separate test with its own pass/fail result.

### Key ideas

- One parameter: `parametrize("name", [a, b, c])`.
- Several: `parametrize("option, first_product", [(x, y), ...])` — a list of **tuples**.
- `ids=[...]` gives readable test names.
- `pytest.param(..., id=..., marks=pytest.mark.skip(...))` customises one case.
- If one case fails, the others still run.

### Worked example — products and sorting

**Step 1.** One parameter — every product can be added (`tests/test_01_parametrize.py`):

```python
PRODUCTS = [
    "Sauce Labs Backpack", "Sauce Labs Bike Light", "Sauce Labs Bolt T-Shirt",
    "Sauce Labs Fleece Jacket", "Sauce Labs Onesie", "Test.allTheThings() T-Shirt (Red)",
]


@pytest.mark.parametrize("name", PRODUCTS)
def test_each_product_can_be_added(products_page, name):
    products_page.add_to_cart(name)
    expect(products_page.cart_badge).to_have_text("1")
```

**Step 2.** Run it with `-v`. Count the tests.

**Step 3.** Two parameters — sorting:

```python
@pytest.mark.parametrize(
    "option, first_product",
    [
        ("Name (A to Z)", "Sauce Labs Backpack"),
        ("Name (Z to A)", "Test.allTheThings() T-Shirt (Red)"),
        ("Price (low to high)", "Sauce Labs Onesie"),
        ("Price (high to low)", "Sauce Labs Fleece Jacket"),
    ],
)
def test_sorting(products_page, option, first_product):
    products_page.sort_by(option)
    expect(products_page.product_names.first).to_have_text(first_product)
```

**Step 4.** Add readable names with `ids`:

```python
@pytest.mark.parametrize(
    "items, expected_count",
    [(["Sauce Labs Backpack"], "1"), (["Sauce Labs Backpack", "Sauce Labs Onesie"], "2")],
    ids=["one item", "two items"],
)
def test_cart_count(products_page, items, expected_count):
    products_page.add_to_cart(*items)
    expect(products_page.cart_badge).to_have_text(expected_count)
```

> **Predict:** what will the test names look like **without** `ids` in Step 4?

### Checkpoint

```
test_each_product_can_be_added[chromium-Sauce Labs Backpack] PASSED
...
test_cart_count[chromium-one item] PASSED
test_cart_count[chromium-two items] PASSED
```

### Your turn

1. Add an "everything" case (all 6 products) to `test_cart_count`.
2. Skip one sorting case with `pytest.param(..., marks=pytest.mark.skip(reason="..."))`.
3. Change one expected value to be wrong. Do the other cases still pass?

### Common errors

| Error | Fix |
|---|---|
| `function uses no argument 'option'` | Names in the decorator must match the function's arguments |
| Wrong number of values | Each case must be a tuple with one value per name |

---

## Topic 2 — Test data in JSON

### Definition

For more than a handful of cases, keep test data in **JSON files** under `test_data/` and load it with a small helper. Non-programmers can add cases, data can be reused, and tests stay short.

### Key ideas

| JSON | Python |
|---|---|
| `[ ... ]` / `{ "key": value }` | `list` / `dict` |
| `"text"`, `29.99` | `str`, `float` |
| `true` / `false` / `null` | `True` / `False` / `None` |

- JSON needs **double quotes** and **no trailing commas**.
- Build file paths from `__file__` so they work from any folder.
- A JSON **object** → parametrize with `.items()`.

### Worked example — login cases from a file

**Step 1.** Create `test_data/login_data.json`:

```json
[
  { "id": "valid user",     "username": "standard_user",   "password": "secret_sauce", "error": null },
  { "id": "wrong password", "username": "standard_user",   "password": "wrong",        "error": "do not match any user" },
  { "id": "locked user",    "username": "locked_out_user", "password": "secret_sauce", "error": "has been locked out" }
]
```

**Step 2.** Create `utils/data_loader.py`:

```python
import json
from pathlib import Path

DATA_DIR = Path(__file__).parent.parent / "test_data"


def load_json(file_name):
    with open(DATA_DIR / file_name, encoding="utf-8") as f:
        return json.load(f)
```

**Step 3.** Load the cases in `tests/test_02_data_from_json.py`:

```python
from utils.data_loader import load_json

LOGIN_CASES = load_json("login_data.json")
```

**Step 4.** One test, every case:

```python
@pytest.mark.parametrize("case", LOGIN_CASES, ids=[c["id"] for c in LOGIN_CASES])
def test_login(login_page, case):
    login_page.login(case["username"], case["password"])

    if case["error"] is None:
        expect(login_page.page).to_have_url(re.compile("inventory.html"))
    else:
        expect(login_page.error_message).to_contain_text(case["error"])
```

> **Predict:** to add an "empty password" case, which file do you change?

### Checkpoint

```
test_login[chromium-valid user] PASSED
test_login[chromium-wrong password] PASSED
test_login[chromium-locked user] PASSED
```

### Your turn

1. Add "empty username" and "empty password" cases to the JSON. Run again with no Python changes.
   *Hint: the errors say "Username is required" / "Password is required".*
2. Create `test_data/products.json` with each product's price (e.g. `{"Sauce Labs Backpack": 29.99, ...}`). Add a `price_of(name)` method to `ProductsPage` and check every price with `.items()`.
   *Hint: `f"${price:.2f}"` formats `7.99` as `$7.99`.*
3. Add a trailing comma to the JSON and read the error.

### Common errors

| Error | Fix |
|---|---|
| `FileNotFoundError` | Build the path from `__file__`, not `"test_data/..."` |
| `JSONDecodeError` | Double quotes only; no trailing commas |
| `ModuleNotFoundError: utils` | Add `utils/__init__.py`; run from `lecture09/` |

---

## Topic 3 — Flaky tests and retries

### Definition

A **flaky test** sometimes passes and sometimes fails **without any code changing**. `pytest-rerunfailures` can retry failures automatically — but a retry hides the problem; it doesn't fix it.

### Key ideas

- Causes: slow servers, animations, timing assumptions, tests that depend on each other.
- One test: `@pytest.mark.flaky(reruns=3)`. All tests: `pytest --reruns 2 --reruns-delay 1`.
- A rerun shows as `R` in the output.
- **Find and fix the cause first**; keep retry counts small (1–2).

### Worked example — the slow user

Swag Labs' `performance_glitch_user` takes around 5 seconds to log in — right at the edge of `expect`'s 5-second default.

**Step 1.** Write the test in `tests/test_03_retries.py`:

```python
def test_slow_login(login_page):
    login_page.login("performance_glitch_user", "secret_sauce")
    expect(login_page.page).to_have_url(re.compile("inventory.html"))
```

**Step 2.** Run it 4 times. Record pass/fail each time.

**Step 3.** Add retries:

```python
@pytest.mark.flaky(reruns=3)
def test_slow_login_with_retries(login_page):
    login_page.login("performance_glitch_user", "secret_sauce")
    expect(login_page.page).to_have_url(re.compile("inventory.html"))
```

**Step 4.** Fix the real cause instead:

```python
def test_slow_login_fixed(login_page):
    login_page.login("performance_glitch_user", "secret_sauce")
    expect(login_page.page).to_have_url(re.compile("inventory.html"), timeout=15_000)
```

> **Predict:** which of the three tests could still fail, and why?

### Checkpoint

Step 1 may fail some or all of the time; Step 3 may show `R` then pass; Step 4 passes every time.

### Your turn

1. Run the whole folder with `pytest --reruns 2`. Find any `R` in the output.
2. Give two reasons why `--reruns 5` on every run is a bad idea.
3. Log in as `problem_user` and sort by "Price (low to high)". Is that test flaky or genuinely failing? Should a retry be added?

---

## Topic 4 — HTML reports with failure screenshots

### Definition

**pytest-html** writes a single HTML report of the run. A **pytest hook** in `conftest.py` (`pytest_runtest_makereport`) adds a screenshot and the page URL to every failed test in that report.

### Key ideas

- `--html=reports/report.html --self-contained-html` — one file you can email.
- The hook is the same in every project: **copy it, don't memorise it.**
- `report.when == "call" and report.failed` → only failures in the test body.

### Worked example — add the hook, break a test, read the report

**Step 1.** Paste this at the bottom of `conftest.py`:

```python
import base64
from playwright.sync_api import Page


def _find_page(item):
    for value in item.funcargs.values():
        if isinstance(value, Page):
            return value
        if isinstance(getattr(value, "page", None), Page):
            return value.page
    return None


@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item, call):
    outcome = yield
    report = outcome.get_result()
    if report.when == "call" and report.failed:
        page = _find_page(item)
        pytest_html = item.config.pluginmanager.getplugin("html")
        if page and pytest_html:
            screenshot = base64.b64encode(page.screenshot()).decode()
            extras = getattr(report, "extras", [])
            extras.append(pytest_html.extras.png(screenshot, "Screenshot at failure"))
            extras.append(pytest_html.extras.url(page.url, "Page URL"))
            report.extras = extras
```

**Step 2.** Break one test on purpose — change an expected value in `test_sorting`.

**Step 3.** Run with a report:

```bash
pytest --html=reports/report.html --self-contained-html
```

**Step 4.** Open `reports/report.html` in your browser. Filter to **Failed** and expand the failure.

> **Predict:** without `--self-contained-html`, what happens if you email the report to a teammate?

### Checkpoint

The report shows the summary, and the failed test has a **screenshot** of the Swag Labs page and a **Page URL** link under its error.

### Your turn

1. Fix the test and run again. Does the screenshot still appear?
2. Add `--junitxml=reports/report.xml` and open the XML file. Who would read this format?
3. In your own words, explain what `hookwrapper=True` + `yield` does.

### Common errors

| Error | Fix |
|---|---|
| No screenshot in report | Missing `--self-contained-html`, or `pytest-html` not installed |
| `--html` not recognised | `pip install pytest-html` |

---

## Topic 5 — Built-in recording and `pytest.ini`

### Definition

pytest-playwright can record **screenshots, videos and traces** for each test. Putting these and every other option from the course into **`pytest.ini`** means a plain `pytest` does everything.

### Key ideas

| Option | Recommended value |
|---|---|
| `--screenshot` | `only-on-failure` |
| `--tracing` | `retain-on-failure` |
| `--video` | `retain-on-failure` (when you need it) |
| `--output` | Folder (default `test-results`) |

- Add `reports/` and `test-results/` to `.gitignore`.

### Worked example — one file for everything

**Step 1.** Open `pytest.ini` and add `testpaths` under the base URL:

```ini
[pytest]
base_url = https://www.saucedemo.com
testpaths = tests
```

**Step 2.** Add the browser and retries:

```ini
addopts =
    --browser chromium
    --reruns 1
```

**Step 3.** Add recording:

```ini
    --screenshot only-on-failure
    --tracing retain-on-failure
```

**Step 4.** Add the report:

```ini
    --html=reports/report.html
    --self-contained-html
```

**Step 5.** Run just `pytest`, with one test still broken.

### Checkpoint

`reports/report.html` exists, and `test-results/` contains a folder for the failed test only, holding a screenshot and a `trace.zip`.

### Your turn

1. Open the trace with `playwright show-trace test-results/<folder>/trace.zip`.
2. Add `--video retain-on-failure` and find the video.
3. Create a `.gitignore` with the two output folders.

---

## Final project — what to look at in the brief

Your instructor will hand out **`final-project-brief.md`**. The project uses **Swag Labs** — the site you've used all through the course. As you read the brief, find:

1. **The requirements:** POM, fixtures, JSON data, `expect`, `pytest.ini`, HTML report, README.
2. **The suggested structure:** the same as Lectures 8–9.
3. **The grading checklist.**
4. **The deadline and how to submit.**

Your Lecture 8–9 folder is a strong starting point — but the brief's checklist decides what "done" means.

---

## Stretch challenge

Write `test_data/orders.json` with three complete checkout scenarios (items, customer name, postcode, expected total) and one parametrized test that runs each scenario end to end with your page objects.
*Hint: Backpack + Fleece Jacket = `Total: $86.38` (8% tax).*

## Exit ticket

1. What is the difference between `parametrize` with a list of values and with a list of tuples?
2. Why build the JSON path from `__file__`?
3. Why are retries not a real fix for a flaky test?

## Cheat sheet

| Code / command | Purpose |
|---|---|
| `@pytest.mark.parametrize("x", [1, 2])` | One parameter |
| `@pytest.mark.parametrize("a, b", [(1, 2), (3, 4)])` | Several parameters |
| `ids=[...]` | Readable test names |
| `pytest.param(..., id=..., marks=...)` | Customise one case |
| `json.load(f)` + `Path(__file__).parent` | Load test data |
| `parametrize("name, price", data.items())` | From a JSON object |
| `@pytest.mark.flaky(reruns=3)` | Retry one test |
| `pytest --reruns 2 --reruns-delay 1` | Retry all tests |
| `pytest --html=reports/report.html --self-contained-html` | HTML report |
| `pytest_runtest_makereport` hook | Screenshot on failure in report |
| `--screenshot only-on-failure --tracing retain-on-failure` | Evidence for failures |
| `--junitxml=report.xml` | Report for CI tools |
| `pytest.ini` → `base_url`, `testpaths`, `addopts` | Save everything |
