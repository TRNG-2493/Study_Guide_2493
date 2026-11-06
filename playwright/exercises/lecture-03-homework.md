# Lecture 3: Homework

**Time:** 60 minutes
**Goal:** practise actions, `expect` assertions and auto-waiting, and try codegen and Trace Viewer.

## Setup

1. Copy `actions_practice.html` from the Lecture 3 demo into your `homework/` folder.
2. Create `homework/test_lecture03_homework.py` with the starter code below.
3. Open `actions_practice.html` in your browser and try each section by hand first.

**Correct login:** username `student`, password `secret123`.

**Rules for this homework:**

- No `time.sleep()` or `wait_for_timeout()`
- Use `expect` for every check on the page
- Use built-in locators where possible (`page.locator("#id")` is fine for message paragraphs with no label or role)

## Starter code

```python
import re
from pathlib import Path

import pytest
from playwright.sync_api import Page, expect

PRACTICE_PAGE = Path(__file__).parent / "actions_practice.html"


@pytest.fixture
def store(page: Page) -> Page:
    page.goto(PRACTICE_PAGE.as_uri())
    return page


# ================= PART 1: Actions and assertions =================

def test_01_successful_login(store: Page):
    # TODO: log in with student / secret123
    # TODO: the message (#login-message) says "Welcome, student!"
    # TODO: the message has the class "success"
    # TODO: the URL contains "#dashboard"
    pass


def test_02_failed_login(store: Page):
    # TODO: log in with student / a wrong password
    # TODO: the message says "Invalid username or password"
    # TODO: the message has the class "error"
    # TODO: the URL does NOT contain "#dashboard"
    pass


def test_03_empty_login(store: Page):
    # TODO: click "Log in" without filling anything
    # TODO: the error message appears
    pass


def test_04_search_with_enter(store: Page):
    # TODO: search for "bike light" and press Enter
    # TODO: #search-result says "Results for: bike light"
    pass


def test_05_add_five_items(store: Page):
    # TODO: click "Add item" 5 times (use a loop)
    # TODO: #cart-count says "Items: 5"
    pass


def test_06_terms_toggle(store: Page):
    # TODO: "Continue" is disabled
    # TODO: tick "I agree to the terms" -> "Continue" is enabled
    # TODO: untick it -> "Continue" is disabled again
    pass


# ================= PART 2: Dynamic elements =================

def test_07_load_products(store: Page):
    # TODO: click "Load products"
    # TODO: "Loading..." is visible, then hidden
    # TODO: exactly 3 products are listed (#product-list li)
    # TODO: the last product is "Jacket"
    pass


def test_08_process_order(store: Page):
    # TODO: click "Process order"
    # TODO: #order-status eventually says "Complete"
    pass


def test_09_slow_report(store: Page):
    # TODO: click "Generate report"
    # TODO: #report-result says "Report ready"
    # Hint: this takes 7 seconds. What does expect need?
    pass
```

---

## Part 1: Actions and assertions (required)

Complete tests 01–06.

```bash
pytest homework -v -k "test_0"
```

> **Hint for test 02:** check the message **before** checking the URL. Think about why the order matters.

---

## Part 2: Dynamic elements (required)

Complete tests 07–09.

```bash
pytest homework -v
```

All 9 tests should pass. The whole run takes about 20 seconds because of the page's delays.

---

## Part 3: Codegen (required)

1. Open `actions_practice.html` in a browser and copy the URL (it starts with `file:///`).
2. Run:

   ```bash
   playwright codegen --target python-pytest -o homework/test_recorded.py "<the file:/// URL>"
   ```

3. In the browser: log in as `student` / `secret123`, then search for "jacket" and press Enter.
4. Close the browser. Open `homework/test_recorded.py`.

Answer as comments at the top of `test_recorded.py`:

1. Which locators did codegen choose for the username, password and Log in button?
2. Which generated lines are unnecessary?
3. What important thing is missing from the recorded test?
4. What would you change before using this as a real test?

---

## Part 4: Trace Viewer (required)

1. Run your successful login test with tracing:

   ```bash
   pytest homework -k successful_login --tracing on
   ```

2. Open the trace (find the exact folder name in `test-results/`):

   ```bash
   playwright show-trace test-results/<folder>/trace.zip
   ```

Answer as comments at the bottom of `test_lecture03_homework.py`:

1. How many actions are listed?
2. Click the **Log in** click action and open the **After** tab. What does the message say at that moment?
3. Click your `to_have_text` assertion. Roughly how long did it wait?

---

## Part 5: Bonus (optional) — fix a flaky test

This test sometimes passes and sometimes fails. Add it to your file, run it, and then fix it.

```python
import time


def test_flaky_login(page: Page):
    page.goto(PRACTICE_PAGE.as_uri())
    page.locator("#username").fill("student")
    page.locator("#password").fill("secret123")
    page.locator("#login-button").click()
    time.sleep(1)
    assert page.locator("#login-message").text_content() == "Welcome, student!"
```

1. Explain in a comment what's wrong with it (there are at least 2 problems).
2. Write a fixed version called `test_fixed_flaky_login`.

---

## Submission checklist

- [ ] `test_lecture03_homework.py`: 9 passing tests, no `sleep`
- [ ] `test_recorded.py` with the 4 codegen answers
- [ ] 3 Trace Viewer answers
- [ ] (Optional) Part 5: explanation and fixed test
