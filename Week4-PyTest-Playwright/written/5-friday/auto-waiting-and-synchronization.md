# Auto-Waiting and Synchronization

## Learning Objectives

By the end of this lesson you will be able to:

- Explain why web tests need synchronization and what a "race condition" is in UI testing.
- Describe Playwright's auto-waiting and list the actionability checks performed before each action.
- Use web-first assertions with `expect()` that retry until a condition is met.
- Choose correctly between `expect()`, `wait_for()`, `wait_for_url()`, `wait_for_load_state()`, `wait_for_response()` and `expect_*` context managers.
- Configure and understand timeouts at the action, assertion and navigation level.
- Explain why `time.sleep()` and `wait_for_timeout()` are anti-patterns, and replace them with proper waits.
- Diagnose a timeout error message.

---

## Why This Matters

The number one reason UI automation suites become untrustworthy is **flakiness**: a test that passes sometimes and fails other times without any change to the code. Flaky tests waste hours, teach teams to ignore red builds, and eventually get deleted. The most common root cause of flakiness is bad synchronization: the test script runs faster than the web application.

This week's epic is to convert manual test design into automation that the team can trust, and Project 1: QE Foundations needs automated UI tests that pass consistently. A human tester naturally "waits" for a page to look ready, then clicks. A script has no eyes. Playwright's headline feature is that it gives the script patience automatically. If you understand auto-waiting you will write less code, avoid sleeps, and produce stable tests from your first day.

---

## The Concept

### 1. The problem: scripts are fast, web pages are not

Think about what happens when you click "Login" on a real website:

1. The browser sends a request to the server.
2. The server checks credentials (takes, say, 400 ms).
3. The server responds; the browser updates the page or navigates.
4. JavaScript runs and draws new elements, sometimes with animations.

A script that fires `click()` and immediately looks for the welcome message is asking "is it there?" at step 1, before steps 2 to 4 are finished. That is a **race condition** between the test and the application. Sometimes the test wins (the app is fast on a quiet machine) and the test fails; sometimes the app wins and it passes. Result: flaky.

Older tools forced you to solve this manually with fixed pauses ("sleep 5 seconds") or explicit waits around every step. Fixed pauses are either too short (still flaky) or too long (slow suite). Playwright solves the problem at the framework level.

> **Analogy.** Imagine a waiter who delivers dishes. A bad waiter walks to the table at exactly 10 minutes after ordering, whether or not the food is ready (fixed sleep). A good waiter checks the kitchen pass and picks up the plate the instant it is ready (auto-waiting).

### 2. Auto-waiting: actionability checks

Before performing an action such as `click()`, Playwright automatically waits until the target element is actionable. The set of checks depends on the action, but the main ones are:

| Check | Meaning |
|-------|---------|
| **Attached** | The element is present in the DOM. |
| **Visible** | It has a non-empty bounding box and is not `visibility: hidden`. |
| **Stable** | It is not moving (for example, mid-animation). It must have the same position for two consecutive animation frames. |
| **Enabled** | It is not `disabled`. |
| **Editable** | For `fill()`: it is enabled and not read-only. |
| **Receives Events** | It is the element at the click point, not covered by another element such as an overlay or modal. |

Which actions use which checks (simplified):

| Action | Visible | Stable | Receives Events | Enabled | Editable |
|--------|:------:|:------:|:---------------:|:-------:|:--------:|
| `click()` | yes | yes | yes | yes | no |
| `fill()` | yes | no | no | yes | yes |
| `check()` | yes | yes | yes | yes | no |
| `hover()` | yes | yes | yes | no | no |
| `select_option()` | yes | no | no | yes | no |
| `text_content()`, `get_attribute()` | no | no | no | no | no |

(See the official "Actionability" page for the definitive table for your installed version.)

If any check fails, Playwright **keeps retrying** until all pass or the timeout (default 30 seconds) is reached. Only then does the action fail with a `TimeoutError`.

So this code needs no waiting statements at all:

```python
page.locator("#login-button").click()          # waits until the button is clickable
expect(page.locator(".title")).to_have_text("Products")   # waits for the text
```

### 3. Web-first assertions

`expect(...)` assertions retry until the condition holds or the timeout (default **5 seconds**) elapses.

```python
expect(page.locator(".title")).to_have_text("Products")
```

Internally Playwright re-queries the locator and re-checks the text repeatedly (with a short back-off between attempts). The test continues the moment the assertion passes, so a page that is ready in 200 ms costs you 200 ms, not 5 seconds. The timeout is a ceiling, not a delay.

Contrast with "snapshot" checks, which read a value once:

| Snapshot (no retry) | Web-first (retries) |
|---------------------|---------------------|
| `locator.is_visible()` | `expect(locator).to_be_visible()` |
| `locator.inner_text()` | `expect(locator).to_have_text(...)` |
| `locator.count()` | `expect(locator).to_have_count(...)` |
| `locator.get_attribute("x")` | `expect(locator).to_have_attribute("x", ...)` |
| `page.title()` | `expect(page).to_have_title(...)` |
| `page.url` | `expect(page).to_have_url(...)` |
| `locator.is_checked()` | `expect(locator).to_be_checked()` |

**Golden rule:** when asserting on the state of the page, use `expect()`. Snapshot methods have their legitimate uses (for example, reading text to compute something), but they do not wait for a specific condition (some, like `inner_text()`, wait for the element to exist but not for it to contain the right content).

Useful `expect` options:

```python
expect(locator).to_have_text("Done", timeout=15_000)    # custom timeout for this assertion
expect(locator).to_have_text("done", ignore_case=True)
expect(locator).to_have_text(re.compile(r"^Order #\d+$"))   # regex
expect(locator).not_to_be_visible()                      # waits until it disappears
```

Negative assertions (`not_to_...`) also retry: `not_to_be_visible()` waits until the element becomes hidden or disappears, which is exactly what you want for spinners and toasts.

### 4. Explicit waits (when auto-waiting is not enough)

Most of the time actions and `expect()` are all you need. Occasionally you must wait for something that is not an element on the page. Playwright provides targeted waits.

**4.1 Waiting for a locator state: `locator.wait_for()`**

```python
spinner = page.locator(".spinner")
spinner.wait_for(state="hidden")      # wait until the spinner disappears
page.locator("#result").wait_for(state="visible")
```

Valid states: `"attached"`, `"detached"`, `"visible"`, `"hidden"`. Often `expect(spinner).to_be_hidden()` reads better and does the same job.

**4.2 Waiting for a URL: `page.wait_for_url()`**

```python
page.locator("#login-button").click()
page.wait_for_url("**/inventory.html")      # glob pattern
page.wait_for_url(re.compile(r"inventory"))  # or regex
```

`expect(page).to_have_url(...)` is usually preferred, because it is an assertion with a clear failure message.

**4.3 Waiting for load states: `page.wait_for_load_state()`**

```python
page.wait_for_load_state("domcontentloaded")
page.wait_for_load_state("load")
page.wait_for_load_state("networkidle")   # discouraged for assertions
```

`networkidle` means "no network connections for at least 500 ms." Playwright's own documentation discourages it for deciding when a page is ready, because modern pages (analytics, polling, websockets) may never be idle, or may be idle before content renders. Prefer asserting on the actual element the user cares about.

**4.4 Waiting for a network response: `expect_response`**

When an action triggers an API call and you want to verify or wait for it:

```python
with page.expect_response("**/api/search*") as response_info:
    page.get_by_placeholder("Search").fill("laptop")
response = response_info.value
assert response.status == 200
```

How it works: the `with` block *starts listening* for a matching response, runs the code inside (the action that triggers the request), and when the block ends, `response_info.value` waits for the response (if it has not arrived). The listener must be set up **before** the action, otherwise a fast response could be missed. Related helpers: `page.expect_request(...)`, `page.expect_navigation()` (older; prefer `wait_for_url` or `expect(page).to_have_url`), `page.expect_popup()`, `page.expect_download()`, `page.expect_file_chooser()`.

**4.5 Waiting for a JavaScript condition: `page.wait_for_function()`**

```python
page.wait_for_function("document.querySelectorAll('.row').length >= 10")
```

A last-resort tool for custom conditions you cannot express with locators.

**4.6 `page.wait_for_timeout()` and `time.sleep()`**

```python
page.wait_for_timeout(3000)    # hard pause. Debug only!
```

Playwright's documentation explicitly says this should only be used for debugging. In test code it is an anti-pattern.

### 5. Timeouts explained

| Timeout | Default | Applies to | How to change |
|---------|---------|-----------|---------------|
| Action timeout | 30 000 ms (30 s) | `click`, `fill`, `check`, `wait_for` ... | `page.set_default_timeout(ms)` or `timeout=` on the call |
| Navigation timeout | 30 000 ms | `goto`, `reload`, `wait_for_url` ... | `page.set_default_navigation_timeout(ms)` |
| `expect` timeout | 5 000 ms (5 s) | all `expect()` assertions | `expect(..., timeout=)` per call |
| PyTest timeout | none by default | whole test | `pytest-timeout` plugin (optional) |

Notice the asymmetry: actions wait up to 30 s, assertions only 5 s. If an assertion needs longer (a report that takes 12 seconds), pass `timeout=15_000` for that assertion only. Do not inflate global values without a reason.

All timeouts are in **milliseconds**. Python's underscore number syntax (`15_000`) makes them readable.

### 6. Reading a timeout error

A typical failure looks like:

```
playwright._impl._errors.TimeoutError: Locator.click: Timeout 30000ms exceeded.
Call log:
  - waiting for locator("#login-buton")
```

How to read it: the action (`Locator.click`), the limit (30000 ms), and the **call log**, which explains what Playwright was doing: here it was still "waiting for locator" because the element never appeared. A typo in the selector! Other call-log lines might say:

- `element is not visible` : something hides the element.
- `element is not enabled` : the button is disabled (maybe a required field is empty).
- `<div class="modal"> intercepts pointer events` : an overlay covers the target.
- `waiting for element to be stable` : the element is still animating.

The call log tells you *why* the wait never finished. Learn to read it before reaching for a bigger timeout.

An `expect` failure looks like:

```
AssertionError: Locator expected to have text 'Products'
Actual value: Login
Call log:
  - Expect "to_have_text" with timeout 5000ms
  - waiting for locator(".title")
```

It shows the expected value, the actual value observed on the last attempt, and the timeout.

### 7. Strictness and waiting together

If a locator matches multiple elements, Playwright raises a strict-mode error instead of waiting forever or picking one randomly. This is related to synchronization: an unclear locator might match one element now and two later (after a list loads), so strictness catches ambiguous tests early.

### 8. Dynamic content patterns

**Spinner pattern**

```python
page.get_by_role("button", name="Search").click()
expect(page.locator(".spinner")).to_be_hidden()
expect(page.locator(".result-row")).to_have_count(10)
```

**Toast notification that disappears**

```python
page.get_by_role("button", name="Save").click()
expect(page.locator(".toast")).to_have_text("Saved successfully")
expect(page.locator(".toast")).to_be_hidden(timeout=10_000)
```

**Content that loads lazily** (infinite scroll)

```python
page.mouse.wheel(0, 3000)
expect(page.locator(".card")).to_have_count(20)
```

**Waiting for a list to *stop* changing** is hard; instead assert on the final expected state (count, text) which retries until correct.

### 9. Decision guide

1. Performing an action on an element? Just do it; auto-waiting handles readiness.
2. Verifying something about the page? Use `expect()`.
3. Waiting for navigation? `expect(page).to_have_url(...)`.
4. Need to wait for a specific network call? `page.expect_response(...)`.
5. Waiting for something truly custom? `page.wait_for_function(...)`.
6. Tempted to sleep? Stop and look for the real condition you are waiting for.

---

## Code Examples

### Example 1: No waits required

```python
from playwright.sync_api import Page, expect


def test_login_needs_no_sleep(page: Page):
    page.goto("https://www.saucedemo.com/")
    page.get_by_placeholder("Username").fill("standard_user")
    page.get_by_placeholder("Password").fill("secret_sauce")
    page.get_by_role("button", name="Login").click()

    expect(page).to_have_url("https://www.saucedemo.com/inventory.html")
    expect(page.locator(".inventory_item")).to_have_count(6)
```

**Explanation:** There is not a single wait statement, yet it is stable. `fill()` waits for the input to be visible, enabled and editable. `click()` waits for the button to be actionable. `to_have_url` and `to_have_count` retry until the navigation completes and the six products render.

### Example 2: The anti-pattern and its fix

Bad:

```python
import time

def test_bad(page):
    page.goto("https://www.saucedemo.com/")
    page.locator("#user-name").fill("standard_user")
    page.locator("#password").fill("secret_sauce")
    page.locator("#login-button").click()
    time.sleep(5)                                   # always wastes 5 s; may still be too short
    assert page.locator(".title").inner_text() == "Products"
```

Good:

```python
def test_good(page):
    page.goto("https://www.saucedemo.com/")
    page.locator("#user-name").fill("standard_user")
    page.locator("#password").fill("secret_sauce")
    page.locator("#login-button").click()
    expect(page.locator(".title")).to_have_text("Products")
```

The good version proceeds the instant the text appears, and tells you precisely what was expected if it does not.

### Example 3: Snapshot vs web-first, side by side

```python
# Snapshot: evaluates ONCE, may run before the app has updated
assert page.locator(".shopping_cart_badge").count() == 1      # risky

# Web-first: retries up to 5 s
expect(page.locator(".shopping_cart_badge")).to_have_count(1)  # reliable
```

### Example 4: Waiting for a spinner and an API response

SauceDemo is mostly static, so this example uses a generic pattern you will apply to your own app:

```python
def test_search_waits_for_api(page: Page):
    page.goto("/products")      # assumes base_url is configured

    with page.expect_response(lambda r: "/api/search" in r.url and r.status == 200):
        page.get_by_placeholder("Search products").fill("laptop")
        page.get_by_placeholder("Search products").press("Enter")

    expect(page.locator(".spinner")).to_be_hidden()
    expect(page.locator(".result-row").first).to_contain_text("laptop")
```

**Explanation:**

- `expect_response` accepts a URL pattern, a regex, or a **predicate function** (a `lambda` taking the response and returning True/False). Here we require the URL to contain `/api/search` and the status to be 200.
- Inside the `with`, we trigger the search. If the response never arrives within the timeout, the `with` block raises a TimeoutError.
- Afterwards we use normal `expect` for the UI result. Combining a network wait and a UI assertion gives a test that is both fast and accurate.

### Example 5: Demonstrating auto-wait on a delayed element

You can create a local page to *see* auto-waiting working:

```python
# test_autowait_demo.py
from playwright.sync_api import Page, expect

HTML = """
<button id="go" onclick="
    setTimeout(() => {
        const p = document.createElement('p');
        p.id = 'msg';
        p.textContent = 'Loaded!';
        document.body.appendChild(p);
    }, 2000)">Load</button>
"""


def test_element_appears_after_two_seconds(page: Page):
    page.set_content(HTML)
    page.locator("#go").click()
    expect(page.locator("#msg")).to_have_text("Loaded!", timeout=5000)
```

**Explanation:** `page.set_content()` loads HTML directly, so no website is needed. The button creates a paragraph two seconds after being clicked. The assertion waits (within 5 seconds) and passes after about two seconds. Run with `--headed` and time it. Then lower the timeout to `500` and read the failure message: it displays the call log with the expected text and the "waiting for locator" lines.

### Example 6: Custom timeouts

```python
def test_slow_report(page: Page):
    page.set_default_timeout(15_000)           # all actions on this page
    page.goto("/reports")
    page.get_by_role("button", name="Generate").click()
    expect(page.get_by_text("Report ready")).to_be_visible(timeout=20_000)  # just this one
```

---

## Real-World Scenarios

1. **The "works on my machine" flake.** A test passes on a developer's fast laptop and fails on the shared CI server, which is slower. The root cause is a `time.sleep(2)` that is enough locally but not in CI. Replacing it with `expect(...)` makes it pass everywhere.
2. **The disabled Submit button.** A form's Submit button stays disabled until client-side validation finishes. Without auto-waiting, a script clicks too early and nothing happens. Playwright waits for it to be enabled; and the call log "element is not enabled" would reveal if a required field was missed.
3. **A modal covers the page.** A cookie banner animates in and intercepts clicks. Playwright's "receives events" check waits for the overlay to go away or fails with a call log naming the intercepting element, leading you to handle the banner properly.

---

## Common Mistakes

1. **Using `time.sleep()` or `wait_for_timeout()` in tests.** Slow and unreliable. Replace with `expect()`.
2. **Using `assert locator.is_visible()`.** No retry. Use `expect(locator).to_be_visible()`.
3. **Extending timeouts globally to "fix" flakiness.** This hides the true cause and slows failures.
4. **Using `wait_for_load_state("networkidle")` as the default readiness check.** It is discouraged; assert on elements instead.
5. **Creating `expect_response` after the action.** The response may already have gone; set up the listener first (use the `with` block around the action).
6. **Misreading timeouts as milliseconds vs seconds.** `timeout=5` is 5 ms, not 5 seconds. Use `5_000`.
7. **Ignoring the call log.** It states why the wait failed. Read it before changing code.
8. **Asserting on the intermediate state.** If a counter goes 0 → 1 → 2 and you assert `1`, you create a race. Assert on the *final* state, or design the scenario around stable states.
9. **Waiting for an element with `count()` loops** (`while locator.count() == 0: ...`). That is hand-written, error-prone waiting; use `wait_for()` or `expect`.

---

## Practice Exercises

**Exercise 1.** Take the "bad" test in Example 2 and run it, timing it with `pytest --durations=3`. Then run the "good" version. Record the difference.

**Exercise 2.** Run Example 5 and change the delay in the HTML from `2000` to `7000` ms. What happens? Which two ways can you make it pass? *(Answer: raise the assertion timeout above 7 seconds, or reduce the delay; do the first only if a 7-second wait is a genuine business behavior.)*

**Exercise 3.** Modify Example 5 so that the message *disappears* after another second (use a second `setTimeout` that removes the element). Write assertions that verify it appears then disappears, using `to_be_visible` and `to_be_hidden`.

*Hint:* `p.remove()` removes the element; `expect(page.locator("#msg")).to_be_hidden()` passes for a removed element.

**Exercise 4.** On SauceDemo, click "Add to cart" for the backpack and use `expect` to verify the badge text becomes "1". Then click Remove and verify the badge is no longer present, using `to_have_count(0)`.

**Exercise 5.** Provoke each of these errors on purpose and write down the call log lines: (a) a wrong selector; (b) a strict mode violation (`page.locator(".inventory_item").click()`); (c) an assertion with the wrong expected text.

**Exercise 6 (Project 1).** Search your Project 1 manual cases for steps that include words like "wait", "after a few seconds", or "once loaded". For each, decide which Playwright technique from this lesson best replaces the human waiting.

---

## Summary

- Synchronization problems cause most flaky UI tests; the test and the application are in a race.
- Playwright auto-waits before actions for the element to be attached, visible, stable, enabled, editable and able to receive events.
- `expect()` assertions retry (5 seconds by default) until true; prefer them to snapshot methods.
- Use targeted explicit waits (`wait_for`, `wait_for_url`, `expect_response`, `wait_for_function`) only when there is a specific event to wait for.
- Never use fixed sleeps in tests; timeouts are ceilings, not delays.
- Read the call log in timeout errors: it tells you what Playwright was waiting for.

---

## Additional Resources

- Playwright for Python: Auto-waiting: https://playwright.dev/python/docs/actionability
- Playwright for Python: Assertions: https://playwright.dev/python/docs/test-assertions
- Playwright for Python: Events and network: https://playwright.dev/python/docs/network
