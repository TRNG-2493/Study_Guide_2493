# Record and Playback

## Learning Objectives

By the end of this lesson you will be able to:

- Explain what test recording (codegen) is and what its strengths and limits are.
- Launch `playwright codegen` with common options: target language, output file, device, viewport, color scheme, geolocation and saved login state.
- Record a login-and-search style flow and read the generated Python code.
- Use the recorder's assertion tools (visibility, text, value) and the Pick locator feature.
- Turn a raw recording into a clean, maintainable PyTest test (refactor, rename, add assertions, remove noise).
- Play back (run) the recorded script, and re-record parts of a test.
- Explain why a recorded test is a starting point, not a finished product.

---

## Why This Matters

Writing locators and actions by hand is slow when you are exploring a new page. Playwright's **codegen** tool watches you use a real browser and writes the Python code for what you do. For a Test Automation Engineer, it is a productivity booster: you can produce a first draft of a test in minutes, discover the best locators Playwright would suggest, and learn the API by seeing your own actions turned into code.

For this week's epic ("convert manual test design into automation") and Project 1: QE Foundations, codegen is a bridge: you take a manual test case, walk through its steps once in the browser, and get an automated skeleton. But a recording on its own is rarely good enough for a real suite, and understanding the **limits** and how to **clean it up** is the real skill. Teams that paste raw recordings into the repository end up with duplicated, brittle tests that nobody trusts.

---

## The Concept

### 1. What is record and playback?

- **Record**: You interact with a web application in a browser while a tool captures each interaction (click, fill, navigation) and writes it as code.
- **Playback**: You run that code and the tool re-performs the same actions automatically.

Older "record and playback" tools stored scripts in proprietary formats, and played back brittle coordinates or fragile selectors. Playwright's codegen is different: it generates **real, editable Python code** using the same modern locators that you have been writing (`get_by_role`, `get_by_label`, and so on), preferring resilient ones. Playback is just running the code with PyTest, as you do every day.

### 2. Starting codegen

```bash
playwright codegen https://www.saucedemo.com
```

Two windows open:

1. A **browser** where you act as a user.
2. The **Playwright Inspector** window (introduced in the previous lesson) with a code panel that fills as you act, plus recording controls.

Everything you do in the browser (typing, clicking, navigating) appears as code.

Choose the output language with `--target`:

| Target | Output |
|--------|--------|
| `python` | Sync Playwright script (`with sync_playwright()` style) |
| `python-pytest` | A PyTest test function using the `page` fixture (**best for us**) |
| `python-async` | Async version |
| `javascript`, `java`, `csharp` ... | Other languages (we do not use them) |

```bash
playwright codegen --target python-pytest https://www.saucedemo.com
```

You can also use the in-window language drop-down to switch the display. Because our framework is PyTest, **select `Pytest`** (or use `--target python-pytest`).

### 3. Useful command-line options

| Option | Purpose | Example |
|--------|---------|---------|
| `-o, --output` | Save the generated code to a file. | `-o tests/test_recorded.py` |
| `--target` | Language/flavor. | `--target python-pytest` |
| `--browser` or `-b` | `chromium`, `firefox`, `webkit`. | `-b firefox` |
| `--device` | Emulate a device. | `--device "iPhone 13"` |
| `--viewport-size` | Window size. | `--viewport-size "800,600"` |
| `--color-scheme` | `light` or `dark`. | `--color-scheme dark` |
| `--geolocation` | Fake GPS. | `--geolocation "41.89,12.49"` |
| `--lang` | Browser language. | `--lang "fr-FR"` |
| `--timezone` | Timezone id. | `--timezone "Europe/Rome"` |
| `--save-storage` | After the session, save cookies and local storage to a JSON file (login state). | `--save-storage auth.json` |
| `--load-storage` | Start the session with saved state (already logged in). | `--load-storage auth.json` |
| `--test-id-attribute` | Custom test id attribute. | `--test-id-attribute data-test` |

Run `playwright codegen --help` for the full list for your version.

Example: record on a mobile layout and save to a file:

```bash
playwright codegen --device "Pixel 5" --target python-pytest -o tests/test_mobile_recorded.py https://www.saucedemo.com
```

### 4. Recording step by step

Follow this procedure for a first recording on SauceDemo:

1. Run `playwright codegen --target python-pytest --test-id-attribute data-test -o test_recorded.py https://www.saucedemo.com`.
2. In the browser, click the Username field and type `standard_user`.
3. Click the Password field and type `secret_sauce`.
4. Click **Login**.
5. Click **Add to cart** on the first product.
6. Click the shopping cart icon.
7. In the Inspector toolbar, click **Stop** (the red record button toggles recording).
8. Close the browser. The file `test_recorded.py` is saved.

The recorder produces something like (exact output varies by version and by the locators it chooses):

```python
import re
from playwright.sync_api import Page, expect


def test_example(page: Page) -> None:
    page.goto("https://www.saucedemo.com/")
    page.get_by_placeholder("Username").click()
    page.get_by_placeholder("Username").fill("standard_user")
    page.get_by_placeholder("Password").click()
    page.get_by_placeholder("Password").fill("secret_sauce")
    page.get_by_role("button", name="Login").click()
    page.locator("[data-test=\"add-to-cart-sauce-labs-backpack\"]").click()
    page.locator("[data-test=\"shopping-cart-link\"]").click()
```

Observe how it:

- adds a redundant `click()` before each `fill()` (harmless, but noise);
- picks locators automatically using the same priority list you learned (placeholder, role, then test id);
- contains **no assertions** (unless you add them) and a generic name `test_example`.

### 5. Adding assertions while recording

In the Inspector toolbar are three assertion tools (names may vary slightly by version):

- **Assert visibility**: choose an element that should be visible.
- **Assert text**: choose an element and confirm its text.
- **Assert value**: for input fields.

Procedure: click the assertion icon, click the element in the browser, then confirm (for text, you can edit the expected text). The recorder inserts:

```python
expect(page.locator("[data-test=\"title\"]")).to_contain_text("Your Cart")
expect(page.get_by_text("Sauce Labs Backpack")).to_be_visible()
```

A recording with no assertions is only a *script*, not a *test*. A test needs a verdict.

### 6. Pick locator in codegen

The **Pick locator** button works as in the Inspector: hover to see the suggestion, click to place it in the Locator field and copy it. This is the most valuable part of codegen for many experts: they do not record whole tests, they use it as a locator finder.

### 7. Saving and reusing login state

Logging in at the start of every test is slow. Codegen can save the authenticated state:

```bash
playwright codegen --save-storage=auth.json https://www.saucedemo.com
# log in manually, close the browser: auth.json now contains cookies/localStorage

playwright codegen --load-storage=auth.json https://www.saucedemo.com/inventory.html
# the browser opens already logged in
```

In tests, use the same file through the context options:

```python
# conftest.py
import pytest

@pytest.fixture(scope="session")
def browser_context_args(browser_context_args):
    return {**browser_context_args, "storage_state": "auth.json"}
```

> **Security note:** `auth.json` contains session tokens; add it to `.gitignore` and never commit it. Using saved state for every test is a design decision with trade-offs (tests become dependent on the saved session); we will not go deeper today.

### 8. Playback: running the recorded code

Because the output is a normal PyTest file:

```bash
pytest test_recorded.py                 # headless
pytest test_recorded.py --headed        # watch it
pytest test_recorded.py --headed --slowmo 500
```

Debug failures with the Inspector (previous lesson) and traces (runner lesson).

A "record, then replay immediately" habit is wise: it confirms that the recording works before you refactor.

### 9. Recording into an existing test (the "Record" button)

When you debug with `PWDEBUG=1` or `page.pause()`, the Inspector has a **Record** toggle. Click it and your browser actions are *inserted at the cursor position* in the code, which allows you to extend an existing test: run to the point where the test pauses, press Record, perform the next few steps by hand, and copy the generated lines into your test. This is faster than recording a whole test from the start.

### 10. Limits of recording

| Limitation | Explanation |
|-----------|-------------|
| **No test design** | The recorder does not know what you want to verify; assertions are your job. |
| **Raw repetition** | Every test records its own login, navigation, etc. No reuse. |
| **Naming** | Generic names (`test_example`) and no markers or docstrings. |
| **Redundant steps** | Extra clicks before fills, duplicate navigations. |
| **Locators may still be weak** | If the app has no good roles/labels/test ids, the recorder falls back to CSS with positions or generated classes, which are brittle. |
| **Dynamic data** | Hard-coded values (names, dates, ids) from your recording session. |
| **Timing-related flows** | Hover menus, drag and drop, file uploads, multi-tab flows may need manual code. |
| **No data-driven design** | A recording is one path with one data set; you add parametrization (Tuesday). |

### 11. From recording to a professional test: the refactoring checklist

1. **Rename** the test to describe behavior: `test_user_can_add_backpack_to_cart`.
2. **Remove noise**: delete redundant `click()` before `fill()`.
3. **Improve locators**: replace position/class-based locators with role, label or filtered chains (previous two lessons).
4. **Add assertions**: at least one `expect()` per important outcome.
5. **Extract repeated steps** into fixtures (Tuesday), such as `logged_in_page`.
6. **Extract data** into constants or parametrization.
7. **Add markers** (`@pytest.mark.smoke`) and a docstring linking to the manual test case id (traceability to Project 1).
8. **Run it** several times (and in different browsers) to check stability.

### 12. When to use record and playback (and when not)

Good uses:

- Exploring a new page quickly and discovering locators.
- Creating a first draft of a long form flow.
- Learning the Playwright API by example.
- Reproducing a bug quickly to attach a runnable script to a defect report.

Poor uses:

- Building an entire regression suite purely from recordings.
- Testing highly dynamic or data-heavy flows without redesign.

---

## Code Examples

### Example 1: Raw recording and the cleaned-up version

Raw recording (what the tool generated):

```python
import re
from playwright.sync_api import Page, expect


def test_example(page: Page) -> None:
    page.goto("https://www.saucedemo.com/")
    page.get_by_placeholder("Username").click()
    page.get_by_placeholder("Username").fill("standard_user")
    page.get_by_placeholder("Password").click()
    page.get_by_placeholder("Password").fill("secret_sauce")
    page.get_by_role("button", name="Login").click()
    page.locator("[data-test=\"add-to-cart-sauce-labs-backpack\"]").click()
    page.locator("[data-test=\"shopping-cart-link\"]").click()
```

Refactored:

```python
import re
import pytest
from playwright.sync_api import Page, expect

BASE = "https://www.saucedemo.com/"


@pytest.fixture
def logged_in(page: Page) -> Page:
    page.goto(BASE)
    page.get_by_placeholder("Username").fill("standard_user")
    page.get_by_placeholder("Password").fill("secret_sauce")
    page.get_by_role("button", name="Login").click()
    expect(page).to_have_url(re.compile("inventory"))
    return page


@pytest.mark.smoke
def test_user_can_add_backpack_to_cart(logged_in: Page):
    """Manual case TC-CART-001: add a product to the cart and see it listed."""
    backpack = logged_in.locator(".inventory_item").filter(has_text="Sauce Labs Backpack")
    backpack.get_by_role("button", name="Add to cart").click()

    expect(logged_in.locator(".shopping_cart_badge")).to_have_text("1")

    logged_in.locator(".shopping_cart_link").click()
    expect(logged_in).to_have_url(re.compile("cart"))
    expect(logged_in.locator(".cart_item")).to_have_count(1)
    expect(logged_in.locator(".inventory_item_name")).to_have_text("Sauce Labs Backpack")
```

**What changed and why:**

- Login moved into a fixture (reuse; Tuesday).
- Redundant `click()` calls removed (`fill()` already focuses).
- The `[data-test=...]` locator for the product replaced with a filter chain by product name (more readable and independent of generated ids).
- Several `expect()` assertions added: the recording had none.
- A docstring links the automated test to a manual case id (Project 1 traceability), and a `smoke` marker added (Monday).
- The name describes behavior.

### Example 2: Recording a "search" flow on the Playwright docs site

Command:

```bash
playwright codegen --target python-pytest https://playwright.dev/python/
```

Actions: click the **Search** control, type `locators`, press Enter or click the first result. The generated code typically resembles:

```python
def test_example(page: Page) -> None:
    page.goto("https://playwright.dev/python/")
    page.get_by_label("Search").click()
    page.get_by_placeholder("Search docs").fill("locators")
    page.get_by_role("link", name="Locators", exact=True).click()
```

(Exact output depends on the current site markup.) A reviewed version:

```python
def test_search_finds_locators_page(page: Page):
    page.goto("https://playwright.dev/python/")
    page.get_by_label("Search").click()
    page.get_by_placeholder("Search docs").fill("locators")
    page.get_by_role("link", name="Locators", exact=True).first.click()
    expect(page).to_have_url(re.compile("locators"))
    expect(page.get_by_role("heading", name="Locators", level=1)).to_be_visible()
```

Where the page structure changes, regenerate the locator with Pick locator, which is the maintenance workflow.

### Example 3: Saved state in practice

```python
# conftest.py
import pytest
from playwright.sync_api import Browser, Page


@pytest.fixture
def authed_page(browser: Browser):
    context = browser.new_context(storage_state="auth.json")
    page = context.new_page()
    yield page
    context.close()
```

```python
def test_inventory_visible_when_logged_in(authed_page: Page):
    authed_page.goto("https://www.saucedemo.com/inventory.html")
    expect(authed_page.locator(".inventory_item")).to_have_count(6)
```

**Explanation:** `browser` is the plugin's session-scoped fixture. We create our own context with `storage_state` (the saved cookies and local storage), then `yield` the page (Tuesday's yield-fixture pattern), and close the context in teardown. Note SauceDemo stores its session in a cookie; this works for demonstration but behavior depends on the site.

### Example 4: Using the Record button while paused

```python
def test_extend_me(page: Page):
    page.goto("https://www.saucedemo.com/")
    page.get_by_placeholder("Username").fill("standard_user")
    page.get_by_placeholder("Password").fill("secret_sauce")
    page.get_by_role("button", name="Login").click()
    page.pause()          # run with --headed; press Record in the Inspector; perform steps; copy the code
```

Run `pytest -s --headed test_extend_me.py`. At the pause, press **Record**, click Add to cart on two items and open the cart, then copy the new lines into the test and tidy them.

### Example 5: A recorded bug reproduction

When a defect is found, record the steps and save the file (`-o bug_1234.py`). Attach it to the bug ticket. A developer can run `pytest bug_1234.py --headed` and see the problem instantly, no long written steps required. After the fix, the same file (cleaned) becomes a regression test.

---

## Real-World Scenarios

1. **Fast drafting of a long form.** A 25-field registration form is tedious to script. A QE records the happy path, then refactors the output into a parametrized test with many data sets.
2. **Exploring an unfamiliar legacy app.** The tester records exploratory sessions to learn which elements lack accessible names, and lists them as testability requests for developers.
3. **Hand-off to developers.** A recorded reproduction of a bug in Safari's engine (`-b webkit`) is attached to the ticket.
4. **Locator maintenance.** When a UI redesign breaks selectors, engineers open codegen on the new page and use Pick locator to repair each one quickly.

---

## Common Mistakes

1. **Committing raw recordings.** They have no assertions and poor structure. Always refactor.
2. **Believing a green recording equals a good test.** Without assertions, a test can pass even when the application is broken.
3. **Recording with real personal or production credentials.** Use test accounts. Never commit `auth.json`.
4. **Forgetting `--target python-pytest`** and getting a script with `sync_playwright()`, which does not use the `page` fixture. (It still works, but it does not fit our PyTest suite.)
5. **Hard-coding dynamic data** (dates, generated ids) captured during the recording.
6. **Trusting every generated locator.** Review them using the built-in locators priority list.
7. **Recording while the browser window is resized or with extensions interfering.** Use the clean browser codegen provides.
8. **Not re-running the recording.** If it fails on first replay, you will want to know before you refactor.
9. **Overwriting the output file by accident.** `-o` on an existing path overwrites it. Use new names or version control.

---

## Practice Exercises

**Exercise 1.** Run `playwright codegen --target python-pytest -o test_rec1.py https://www.saucedemo.com`. Record a successful login only. Stop, then run `pytest test_rec1.py --headed`. Does it pass? Does it assert anything?

**Exercise 2.** Extend Exercise 1: record again, this time adding two assertions with the recorder (visibility of the product list and text of the page title). Compare both generated files.

**Exercise 3.** Record the "invalid password" scenario. Refactor it into a test named `test_invalid_password_shows_error`, with an assertion on the error message, using `to_contain_text`.

**Exercise 4.** Take your recording from Exercise 2 and apply the eight-step refactoring checklist. Write down which steps you applied and where you needed to change locators.

**Exercise 5.** Save a login state with `--save-storage=auth.json`, load it with `--load-storage=auth.json` and verify you start on the inventory page without logging in. Add `auth.json` to `.gitignore`.

**Exercise 6.** Record the same login flow with `--device "iPhone 13"` and compare the generated code with the desktop version. (Hint: the code is mostly the same; the device settings apply when the test runs, via `--device` in PyTest too.)

**Exercise 7 (Project 1).** Choose three UI scenarios from Project 1. For each: record the scenario, refactor it into a clean PyTest test, add a docstring with the manual test case id, and add at least one marker. Commit only the refactored tests.

---

## Summary

- `playwright codegen` records your actions in a real browser and writes real, editable Python code.
- Use `--target python-pytest` and `-o file.py` to get a PyTest-ready file; other options handle devices, viewport, language and saved login state.
- The recorder can add simple assertions (visibility, text, value) and has a Pick locator for finding locators.
- Playback is just running the code with PyTest (headed, slow motion, with Inspector or traces).
- Recordings are drafts: refactor names, remove noise, improve locators, add assertions, reuse fixtures, parametrize data and add markers.
- Use record and playback to speed up exploration and drafting, not as a substitute for test design.

---

## Additional Resources

- Playwright for Python: Test generator (codegen): https://playwright.dev/python/docs/codegen
- Playwright for Python: Authentication (saved state): https://playwright.dev/python/docs/auth
- Playwright for Python: Debugging tests: https://playwright.dev/python/docs/debug
