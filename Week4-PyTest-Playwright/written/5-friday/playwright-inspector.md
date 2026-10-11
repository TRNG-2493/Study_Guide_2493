# Playwright Inspector

## Learning Objectives

By the end of this lesson you will be able to:

- Explain what the Playwright Inspector is and when to use it.
- Launch the Inspector with `PWDEBUG=1`, with `page.pause()`, and from codegen.
- Use the Inspector's controls: Resume, Step over, Pick locator, Record, and the Actionability log.
- Use "Pick locator" to find and verify locators, and test locator candidates live.
- Debug a failing test step by step and diagnose why it failed.
- Use the Playwright-provided object in the browser console for experimenting.
- Compare the Inspector with the Trace Viewer, and choose the right tool.

---

## Why This Matters

Writing automation is only half of the job; the other half is **debugging**. A trainee who can write ten tests but cannot work out why the eleventh fails is not yet productive. Engineers frequently spend more time diagnosing failing tests than writing new ones.

The **Playwright Inspector** is a graphical debugging tool that lets you pause a test, run it one step at a time while watching the real browser, and test locators interactively. For this week's epic and Project 1: QE Foundations, it is the tool that will turn "my test times out and I do not know why" into "the button is covered by a cookie banner" within a minute. It also makes learning locators fun: you click an element and Playwright tells you the recommended locator for it (you saw the principles in the Built-in locators lesson today).

---

## The Concept

### 1. What is the Inspector?

The Inspector is a separate small window that opens alongside the browser while your test or script runs in **debug mode**. It shows:

- Your test source code with the current line highlighted.
- Buttons to **resume**, **step over** and (in some modes) **record**.
- A **Pick locator** tool to hover over page elements and see locators.
- A **Locator** field in which you can type a locator and see matches highlighted in the page.
- A **Log** tab showing what Playwright is doing step by step (including actionability waits).

It is bundled with Playwright; no extra installation is needed.

> **Analogy.** Running a test normally is like watching a film at normal speed. The Inspector gives you a remote control: pause, frame-by-frame, and the director's commentary on each frame.

### 2. Ways to start the Inspector

#### 2.1 Environment variable `PWDEBUG=1`

Setting `PWDEBUG=1` runs all Playwright actions in debug mode: the browser is **headed**, timeouts are disabled (so you can think as long as you like), and the Inspector opens, paused at the first Playwright action.

macOS / Linux:

```bash
PWDEBUG=1 pytest -s tests/test_login.py
```

Windows PowerShell:

```powershell
$env:PWDEBUG=1
pytest -s tests/test_login.py
```

Windows Command Prompt:

```cmd
set PWDEBUG=1
pytest -s tests/test_login.py
```

(Reset it afterwards: PowerShell `Remove-Item Env:PWDEBUG`, cmd `set PWDEBUG=`, bash `unset PWDEBUG`, otherwise every later run opens the Inspector.)

Notes:

- `-s` (PyTest's "no capture" option, from Monday) is recommended so print output and the debugger do not fight over the terminal.
- Run **one** test at a time when debugging; use a node id like `file.py::test_name`.
- You can combine with `--browser chromium`. The Inspector works with all Playwright browsers, but Chromium is the usual choice.

#### 2.2 `page.pause()` in code

If you only care about a certain point in the test, insert one line:

```python
def test_checkout(page):
    page.goto("https://www.saucedemo.com/")
    ...
    page.pause()          # execution stops here and the Inspector opens
    ...
```

Run in headed mode:

```bash
pytest -s --headed tests/test_checkout.py::test_checkout
```

`page.pause()` only has an effect in headed mode (or with `PWDEBUG=1`); in headless mode it is ignored, so a forgotten `pause()` will not hang your CI, but remove it before committing anyway.

This approach is great when the first 20 steps are fine and the problem is in step 21: run to the pause, then investigate, **using the live browser state**.

#### 2.3 Codegen

The `playwright codegen` command (see the next lesson, Record and playback) also opens an Inspector-style window, where the code you generate is shown, and where the Pick locator button is available.

```bash
playwright codegen https://www.saucedemo.com
```

#### 2.4 VS Code extension

The official Playwright extension for Visual Studio Code lets you run tests, set breakpoints and use "Pick locator" inside the editor. It is optional; the concepts are the same as in the Inspector.

### 3. A tour of the Inspector window

| Area | What it does |
|------|--------------|
| **Resume** (play icon, F8) | Runs the test until the next `page.pause()` or the end. |
| **Step over** (F10) | Executes **one** Playwright call, then pauses again. |
| **Record** | Toggles recording; actions you perform in the browser are appended to the script as code (more in the next lesson). |
| **Pick locator** | Click it, then hover over elements in the browser: a tooltip shows the suggested locator. Click an element to place the locator in the Locator field. |
| **Locator field** | Type or paste a locator; matching elements are highlighted, and the count appears. Edit and re-test until perfect. |
| **Copy / Copy as** | Copies the locator (language selectable). |
| **Source panel** | Your code with the current action highlighted. |
| **Actionability log (Log tab)** | Shows Playwright's actions and waits ("waiting for element to be visible", "element is not enabled", etc.). |

(The layout is refined in each Playwright release; names and icons may differ slightly, but the functions remain.)

### 4. A standard debugging workflow

1. **Reproduce.** Run only the failing test (`pytest path::test_name`).
2. **Read the error and call log.** Often this already tells you the answer (see Auto-waiting lesson).
3. **Open the Inspector** with `PWDEBUG=1` (or insert `page.pause()` just before the failing step).
4. **Step over** action by action. Watch the browser. When the step before the failing one completes, look carefully at the page: Is the element there? Is a modal open? Is the page on the expected URL?
5. **Use Pick locator** to see what Playwright thinks the element's locator should be, and **compare** with your code.
6. **Edit the locator** in the Locator field until it highlights exactly one element.
7. **Fix the test** (or report a bug if the application is wrong).
8. **Remove debug code** (`page.pause()`, `PWDEBUG` env variable), re-run normally.

This workflow is a skill worth repeating until it becomes habit.

### 5. Using Pick locator effectively

Click **Pick locator**, then hover. The suggestion follows Playwright's priority list (role, label, text, test id, and finally CSS/XPath if nothing better exists). Examples of what you might see:

```
get_by_role("button", name="Login")
get_by_placeholder("Username")
get_by_test_id("shopping-cart-link")
locator("#react-burger-menu-btn")
```

Evaluate the suggestion rather than blindly copy:

- Is the text likely to change (price, date)? Then prefer a test id or role without text.
- Does it match exactly **one** element? The highlight and the count tell you.
- Could it be filtered more clearly (see the previous lesson)? Rewrite as a chain.

### 6. The console API: `playwright.$()` and friends

In debug mode, the browser's DevTools console has a `playwright` object. For example, in Chromium DevTools:

```javascript
playwright.locator('text=Login')
playwright.getByRole('button', { name: 'Login' })
playwright.inspect('...')
```

Calling `playwright.locator(...)` highlights matching elements, and `playwright.selector(element)` returns a selector for an element selected in the Elements panel. This is a convenient way to experiment with locator syntax. (Note the console API uses JavaScript syntax such as `getByRole`; translate it to Python's `get_by_role` in your tests. The Inspector's Locator field is language-aware and may be easier for Python learners.)

### 7. Debugging selectors vs debugging logic

The Inspector helps most with *UI* issues: wrong locator, timing, covered elements, unexpected page state. For *Python logic* issues (a wrong variable, a bad loop), use Python tools you know:

- `print()` and `pytest -s`
- `pytest --pdb` (drops into Python's debugger on failure; docs.pytest.org)
- `breakpoint()` in code
- An IDE debugger with breakpoints

You can combine them: put `breakpoint()` for Python and `page.pause()` for browser inspection.

### 8. Inspector vs Trace Viewer

| | Inspector | Trace Viewer |
|-|-----------|--------------|
| When | **During** a run (live, interactive) | **After** a run (post-mortem) |
| Where | Your machine | Anywhere: you can open a trace produced on CI |
| Use for | Developing and debugging locally | Diagnosing failures you cannot reproduce live |
| How | `PWDEBUG=1`, `page.pause()` | `--tracing on`, `playwright show-trace trace.zip` |

Use both: the Inspector to develop, traces to investigate CI failures (see the Playwright test runner lesson today).

### 9. Slow motion as a lightweight alternative

Sometimes you only want to **watch**, not step:

```bash
pytest --headed --slowmo 1000 tests/test_login.py::test_valid_login
```

Each operation is delayed by one second. It does not give you locator picking or stepping, but it is the fastest way to see "what is the test doing?".

---

## Code Examples

### Example 1: A deliberately broken test to debug

```python
# test_debug_me.py
import re
from playwright.sync_api import Page, expect


def test_login_flow(page: Page):
    page.goto("https://www.saucedemo.com/")
    page.get_by_placeholder("User name").fill("standard_user")      # BUG 1: placeholder text is "Username"
    page.get_by_placeholder("Password").fill("secret_sauce")
    page.get_by_role("button", name="Log in").click()                # BUG 2: the button says "Login"
    expect(page).to_have_url(re.compile("inventory"))
```

Run:

```bash
PWDEBUG=1 pytest -s test_debug_me.py        # use the set/$env syntax for your shell
```

What to do in the Inspector:

1. The Inspector opens, paused before `goto`. Click **Step over**; the page loads.
2. Click **Step over** on the first `fill`. Without timeouts the step waits forever on "waiting for get_by_placeholder('User name')". Look at the Log tab. It says it is waiting. (In debug mode timeouts are disabled; in normal mode you would see a 30 second TimeoutError with the same message.)
3. Click **Pick locator** and hover over the username box: the suggestion is `get_by_placeholder("Username")`. Stop the test, correct the string.
4. Repeat for the button: the Pick locator suggests `get_by_role("button", name="Login")`.

**Explanation:** Both bugs are tiny text mismatches, typical in real life. The Inspector shows you the truth of the page immediately.

### Example 2: Pausing at a particular point

```python
def test_checkout_overview(page: Page):
    page.goto("https://www.saucedemo.com/")
    page.get_by_placeholder("Username").fill("standard_user")
    page.get_by_placeholder("Password").fill("secret_sauce")
    page.get_by_role("button", name="Login").click()

    page.locator(".inventory_item").filter(has_text="Backpack") \
        .get_by_role("button", name="Add to cart").click()
    page.locator(".shopping_cart_link").click()

    page.pause()      # <-- inspect the cart page, try locators for the Checkout button

    page.get_by_role("button", name="Checkout").click()
```

Run headed:

```bash
pytest -s --headed test_checkout_overview.py
```

When the pause is reached, use **Pick locator** to find locators for the Checkout button, the item name and the "Continue Shopping" button. Type `get_by_role("button", name="Checkout")` into the Locator field and confirm it highlights one element. Click **Resume** to continue.

### Example 3: Testing a locator against a self-contained page

```python
def test_playground(page: Page):
    page.set_content("""
      <h1>Locator Lab</h1>
      <button>Save</button>
      <button>Save as draft</button>
      <input placeholder="Search"><input aria-label="Email">
    """)
    page.pause()
```

In the Inspector, type each locator and watch the count:

- `get_by_role("button", name="Save")` shows **2** matches (substring).
- `get_by_role("button", name="Save", exact=True)` shows **1**.
- `get_by_label("Email")` shows **1**.

This is an excellent no-risk playground for experiments.

### Example 4: Combining Python debugging and Inspector

```python
def test_prices_sorted(page: Page):
    ...  # login
    prices = page.locator(".inventory_item_price").all_inner_texts()
    print(prices)           # visible with pytest -s
    breakpoint()            # Python's debugger: inspect variables
    page.pause()            # Playwright inspector: inspect the page
```

Explain: `breakpoint()` stops Python in your terminal (type `p prices` to print, `c` to continue); `page.pause()` then stops for browser inspection. Use whichever matches the type of problem.

### Example 5: Opening the Inspector from the CLI without a test

```bash
playwright open https://www.saucedemo.com          # a browser to explore
playwright codegen https://www.saucedemo.com       # a browser plus code generator + inspector
```

`playwright open` just opens a browser (useful to explore a site manually under Playwright). `codegen` adds recording.

---

## Real-World Scenarios

1. **Intermittent overlay.** A test fails with "element intercepts pointer events". Using the Inspector, the engineer sees a newsletter pop-up appearing 2 seconds after load. The fix: close the pop-up in the test setup, or request the application team to disable popups in the test environment.
2. **Pairing session.** Two engineers pair on Thursday's pair-programming exercise: the navigator uses Pick locator to suggest candidate locators while the driver types the code. The Inspector turns locator discussions into evidence.
3. **Onboarding a new application.** A QE new to a legacy application uses `playwright open` and the Pick locator to explore the structure and identify whether elements have test ids or accessible names, then reports gaps to developers.

---

## Common Mistakes

1. **Leaving `PWDEBUG=1` set** in the terminal, so every test run suddenly pauses. Unset it.
2. **Debugging a whole suite at once.** Always run a single test in debug mode.
3. **Committing `page.pause()` into source control.** Search your code for `pause()` before committing; consider a pre-commit check.
4. **Copy-pasting suggested locators without evaluation.** A suggestion that contains a dynamic id (`#input-83921`) or index-based CSS will not survive. Improve it.
5. **Forgetting `-s`.** Without it, PyTest captures output and the terminal debugging experience suffers.
6. **Believing timeouts apply in debug mode.** `PWDEBUG=1` disables timeouts; a test that passes there may still time out normally. Always re-run normally afterwards.
7. **Using the console API with Python names.** In the browser console, use JavaScript syntax (`getByRole`), not `get_by_role`.
8. **Debugging in headless mode.** You cannot see anything. Use `--headed` or `PWDEBUG=1`.

---

## Practice Exercises

**Exercise 1.** Launch `playwright open https://www.saucedemo.com`. With no code at all, explore the site and write down three things you learn about its structure.

**Exercise 2.** Run Example 1 under the Inspector, fix both bugs using Pick locator, and confirm that the test passes in normal mode. Record how many seconds the original failing version took in normal mode (it should be about 30 seconds, the default timeout) and explain why.

**Exercise 3.** Insert `page.pause()` into one of your Friday tests right after login. Use the Locator field to try five locators for the shopping cart link. Which are unique? Which would you choose and why?

**Exercise 4.** In Example 3's playground, write a locator that matches only the "Save as draft" button, in two different ways. *(Solutions: `get_by_role("button", name="Save as draft")` and `get_by_role("button", name="Save").filter(has_text="draft")`.)*

**Exercise 5.** Compare debugging with the Inspector and with a trace for the same failure: break a locator, run with `--tracing on`, open `playwright show-trace`, then run with `PWDEBUG=1`. Write four sentences about the advantages of each.

**Exercise 6 (Project 1).** Pick a Project 1 UI scenario. Use the Inspector to list the recommended locator for every element involved, noting any that fall to CSS/XPath, and share the list with your pair or team as the start of a locator catalog.

---

## Summary

- The Playwright Inspector is a live debugging tool: pause, step, pick and test locators.
- Start it with `PWDEBUG=1`, with `page.pause()` (headed), or by using codegen.
- Core controls: Resume, Step over, Pick locator, Locator field, Record and the Log.
- Debug by reproducing in isolation, stepping to the failure, inspecting the real page state and fixing the locator or timing.
- Debug mode disables timeouts; always re-run normally. Remove `pause()` before committing.
- Use the Inspector locally while developing and traces for failures in CI.

---

## Additional Resources

- Playwright for Python: Debugging tests: https://playwright.dev/python/docs/debug
- Playwright for Python: Trace Viewer: https://playwright.dev/python/docs/trace-viewer
- Pytest documentation: Using pdb: https://docs.pytest.org/en/stable/how-to/failures.html
