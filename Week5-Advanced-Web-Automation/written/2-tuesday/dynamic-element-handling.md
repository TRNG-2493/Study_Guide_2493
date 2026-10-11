# Dynamic Element Handling

## Learning Objectives

By the end of this lesson you will be able to:

- Define what makes an element "dynamic": delayed appearance, changing text, changing attributes or IDs, re-rendering, animation, and overlays.
- Explain Playwright's **auto-waiting** and the **actionability checks** (attached, visible, stable, receives events, enabled, editable) performed before an action.
- Explain **web-first assertions** (`expect(...)`) and how they retry until a condition holds or a timeout expires.
- Use `locator.wait_for(state=...)` for the cases where there is no action or assertion to wait on.
- Choose and write **stable locators** that survive changing IDs and class names (role, label, text, test id, partial attribute selectors, `filter`).
- Handle loading spinners, skeleton screens, toasts, lazy-loaded lists, infinite scroll, and elements that appear/disappear.
- Handle re-rendering ("stale element" problems in other tools) and understand why Playwright's lazy locators avoid them.
- Use `page.add_locator_handler()` to deal with unpredictable overlays such as cookie banners and promotional pop-ups.
- Adjust timeouts correctly (per action, per assertion, per page/context) and explain why fixed sleeps are an anti-pattern.
- Wait for network activity (`expect_response`) and custom conditions (`wait_for_function`) when the UI offers no visible signal.
- Diagnose flaky tests using traces and debugging tools.

---

## Why This Matters

Static web pages, where all content is present the moment the page loads, are the exception. Today's applications are built with JavaScript frameworks that continually fetch data, update parts of the page, show loading indicators, animate transitions, and re-render components. The element you want to click might not exist yet; it might exist but be hidden; it might exist but be covered by an animation; or it might exist and then be replaced by an identical-looking new one a moment later.

**Flaky tests**, tests that pass sometimes and fail sometimes with no code change, are the number one productivity killer in test automation. Teams that suffer from flakiness stop trusting their test suites, ignore red builds, and eventually abandon automation. In nearly every case, the root cause is a **timing assumption**: the test acts before the application is ready, or asserts before the application has updated.

This lesson sits at the centre of the Week 5 epic, *complex UI interactions*, because everything else you do today (frames, tables, date pickers, tabs, shadow DOM, files, navigation) depends on handling dynamic behaviour correctly. It is also directly relevant to **Project 1 - QE Foundations**: reviewers of your UI test suite will judge it on reliability. A suite that passes ten runs in a row on a CI server is far more valuable than a larger suite that fails randomly. Monday's lesson on auto-suggestions already showed that results appear *after* you type; this lesson gives you the general toolkit for all such situations.

---

## The Concept

### 1. What "dynamic" means

| Kind of dynamic behaviour | Example | Typical symptom in a test |
| --- | --- | --- |
| **Delayed appearance** | Search results appear after an API call | Element not found; count is 0 |
| **Loading states** | Spinner or skeleton screen replaces content briefly | Test reads placeholder text instead of real data |
| **Changing text or values** | Counters, timers, "Saved 3 seconds ago" | Assertion on exact text fails intermittently |
| **Changing attributes or IDs** | `id="btn-8f3a2"` regenerated on every build | Selector stops matching after a deploy |
| **Re-rendering** | List re-sorts, framework replaces DOM nodes | "Stale element" errors in other tools |
| **Animation** | Dialog slides in; menu expands | Click lands on moving element or misses |
| **Overlays** | Cookie banner, modal, "chat with us" bubble | Click is intercepted by another element |
| **Conditional elements** | Error toast appears and disappears after 3 s | Missed because the test was too slow |
| **Lazy loading / infinite scroll** | More items load as you scroll | Item is not yet in the DOM |

### 2. The golden rule: wait for conditions, never for time

A **fixed wait** (`time.sleep(5)` or `page.wait_for_timeout(5000)`) is the wrong tool almost every time:

- If the app is ready after 0.3 s, you waste 4.7 s on every run. Multiply by hundreds of tests and you have a slow suite.
- If the app takes 6 s on a slow CI machine, the test fails anyway.

A **conditional wait** waits *exactly as long as necessary*: it proceeds the instant the condition is true and fails only if the maximum timeout passes. Playwright is built around conditional waiting, and most of the time you do not have to write any waits yourself.

> Analogy: Do not set an alarm for "exactly 20 minutes" and then open the oven. Look through the oven window and take the bread out when it is golden.

### 3. Auto-waiting and actionability

Before Playwright performs an action such as `click()`, `fill()`, `check()`, or `select_option()`, it automatically waits for the element to be **actionable**. Which checks apply depends on the action:

| Check | Meaning | `click` | `fill` | `check` | `hover` | `select_option` |
| --- | --- | --- | --- | --- | --- | --- |
| **Attached** | Element is in the DOM | yes | yes | yes | yes | yes |
| **Visible** | Non-empty bounding box and not `visibility:hidden` | yes | yes | yes | yes | yes |
| **Stable** | Same bounding box for two consecutive animation frames (not animating) | yes | | yes | yes | |
| **Receives Events** | Hit target at the click point is the element itself (not covered) | yes | | yes | yes | |
| **Enabled** | Not `disabled` | yes | yes | yes | | yes |
| **Editable** | Not `readonly` and enabled | | yes | | | |

(Table simplified; see "Actionability" in the docs for the exact matrix.)

If the checks do not pass within the timeout (30 seconds by default for actions), Playwright raises a `TimeoutError` with a **call log** describing which check failed:

```
Locator.click: Timeout 30000ms exceeded.
Call log:
  - waiting for get_by_role("button", name="Pay")
  -   locator resolved to <button disabled>Pay</button>
  -   element is not enabled - waiting...
```

Learning to read the call log is a superpower: it tells you exactly *why* Playwright is waiting (not visible? covered by `<div class="modal-backdrop">`? still animating? disabled?).

**You do not need to add a wait before an action.** This is the single most important concept of the lesson. Writing

```python
page.wait_for_selector("#submit")      # unnecessary
page.click("#submit")
```

is redundant. Just write `page.get_by_role("button", name="Submit").click()`.

### 4. Web-first assertions

Assertions made with `expect()` **retry automatically**:

```python
from playwright.sync_api import expect
expect(page.get_by_role("alert")).to_have_text("Saved successfully")
```

This polls the element until its text equals the expected value or the assertion timeout (5 seconds by default) expires. Compare with a "manual" assertion:

```python
assert page.get_by_role("alert").inner_text() == "Saved successfully"   # reads once; fails if toast is not there yet
```

`inner_text()` reads *once*, right now. If the toast has not appeared, you get a timeout (waiting for the element), or a stale value (reading the old text). **Prefer `expect(locator)` over `assert locator.some_method()`** whenever the value can change over time.

Common web-first assertions:

| Assertion | Waits until... |
| --- | --- |
| `to_be_visible()` / `to_be_hidden()` | element is visible / not visible (or absent) |
| `to_be_enabled()` / `to_be_disabled()` | enabled / disabled |
| `to_have_text("...")` / `to_contain_text("...")` | text matches (full / substring) |
| `to_have_value("...")` | an input has the value |
| `to_have_attribute("name", "value")` | attribute equals |
| `to_have_class(...)` | class attribute matches |
| `to_have_count(n)` | the locator matches exactly n elements |
| `to_be_checked()` | checkbox/radio is checked |
| `to_have_url(...)` / `to_have_title(...)` | page URL / title matches |

Every assertion also has a negated form (`not_to_...`) that waits for the *opposite* condition, e.g. `expect(spinner).not_to_be_visible()` (or the equivalent `to_be_hidden()`).

You can change timeouts for a single assertion: `expect(locator).to_be_visible(timeout=10_000)`.

### 5. Explicit waiting: `locator.wait_for()`

Sometimes you need to wait for a state without performing an action or assertion, for instance to synchronise with a spinner before reading a number:

```python
spinner = page.get_by_test_id("spinner")
spinner.wait_for(state="hidden")        # waits until spinner is not visible (or removed)
```

States:

| State | Meaning |
| --- | --- |
| `"visible"` (default) | Attached **and** visible |
| `"hidden"` | Not visible *or* not in the DOM |
| `"attached"` | Present in the DOM (maybe invisible) |
| `"detached"` | Removed from the DOM |

In practice, `expect(spinner).to_be_hidden()` is usually more readable. `wait_for` is handy in helper functions or when you want a specific `TimeoutError` rather than an `AssertionError`.

### 6. Stable locators for changing pages

Resilient tests locate elements by **what they are to a user**, not by incidental implementation details. In order of preference:

1. **Role + accessible name:** `get_by_role("button", name="Submit")`. Robust, reflects accessibility.
2. **Label / placeholder / text:** `get_by_label("Email")`, `get_by_placeholder("Search")`, `get_by_text("Welcome back")`.
3. **Test id:** `get_by_test_id("checkout-submit")` using `data-testid`. Excellent when roles are ambiguous; needs developer cooperation.
4. **Stable CSS:** `#checkout-form .submit` where classes are semantic and stable.
5. **Partial attribute matching** for generated IDs: when IDs look like `btn-8f3a2`, match the constant part:

```python
page.locator("[id^='btn-']")           # starts with
page.locator("[id$='-submit']")        # ends with
page.locator("[id*='submit']")         # contains
page.locator("[data-qa='save']")       # custom attribute
```

6. **Filtering and relationships:** `page.get_by_role("listitem").filter(has_text="Order 1042").get_by_role("button", name="Cancel")`.
7. **Positional locators** (`nth`, `first`, `last`) only as a last resort.

Avoid long, structure-dependent selectors like `div > div:nth-child(3) > span > a`: any layout change breaks them, and they communicate nothing.

**Text that changes:** use regular expressions or `to_contain_text` for the stable part: `expect(page.get_by_text(re.compile(r"Saved \d+ seconds? ago"))).to_be_visible()`.

### 7. Stale elements and re-rendering

In older tools (Selenium), a "found element" is a reference to a DOM node. If the framework replaces that node with a new identical one (typical in React/Vue/Angular), your reference becomes **stale**, and using it raises `StaleElementReferenceException`.

Playwright avoids the problem because **a Locator is not a reference to a node; it is a recipe** (a description of how to find the element). Every action and assertion re-runs the recipe at the moment of use. If the DOM is re-rendered between two lines of your test, the second line just finds the new node.

```python
save = page.get_by_role("button", name="Save")     # recipe, no DOM lookup yet
save.click()                                       # looks up now, acts
save.click()                                       # looks up again; always the current element
```

The exceptions are `ElementHandle` objects (returned by the deprecated `query_selector`) which *are* references. This is a key reason Playwright's documentation steers you away from `ElementHandle`s and `page.query_selector()` toward Locators.

### 8. Loading indicators and skeletons

Pattern: "wait for the loading indicator to go away, then check the data."

```python
page.get_by_role("button", name="Load report").click()
expect(page.get_by_test_id("spinner")).to_be_hidden()
expect(page.get_by_role("row")).to_have_count(11)    # header + 10 rows
```

Even better, skip the spinner and assert on the *outcome*: if what you actually care about is the data, `expect(rows).to_have_count(11)` is enough (it waits as long as needed), and the test does not break if the spinner implementation changes. Use the spinner check when the spinner *itself* is part of the requirement (it must show during loading) or when there is no other observable signal:

```python
expect(spinner).to_be_visible()      # may be flaky if loading is super fast!
```

Caution: asserting that a very short-lived spinner *is visible* can race: it may appear and disappear between polls. Slow the network down with routing (see below) if you need to test that behaviour reliably.

### 9. Toasts, snackbars, and auto-dismissing messages

A toast that vanishes after three seconds is easy to miss if your test is busy doing something else. Assert on it *immediately* after the triggering action:

```python
page.get_by_role("button", name="Save").click()
expect(page.get_by_role("status")).to_contain_text("Saved")
```

Do not do a long series of unrelated steps between the action and the assertion. If you need extra time, you can slow down the dismissal in the test environment (configuration flag) or intercept the timer using `page.clock` (introduced in the Date Pickers lesson).

### 10. Lazy loading and infinite scroll

Content that loads as you scroll requires you to *trigger* the loading:

```python
items = page.locator(".feed-item")
before = items.count()
page.mouse.wheel(0, 3000)                  # scroll down 3000 pixels
expect(items).not_to_have_count(before)    # wait until more items appear
```

(`page.mouse.wheel(delta_x, delta_y)` was introduced with Monday's mouse actions; remember `not_to_have_count` waits until the count is *different*.) Another trick: `locator.scroll_into_view_if_needed()` on the last item triggers the next page, and `locator.press("End")` after focusing the page body scrolls to the bottom. Loop with a cap, as in the pagination pattern from the Web Tables lesson.

Playwright's actions also scroll elements into view automatically, so for most lazy-rendered *virtual lists* you simply act on the element and Playwright scrolls to it, provided the element is already in the DOM.

### 11. Overlays and unpredictable pop-ups: `add_locator_handler`

Cookie banners, newsletter pop-ups, and survey prompts can appear at any moment and block clicks. The **receives events** check then waits indefinitely because another element is covering the target. Playwright offers `page.add_locator_handler()` to register "if this thing appears, run this handler":

```python
def dismiss_newsletter():
    page.get_by_role("button", name="No thanks").click()

page.add_locator_handler(page.get_by_text("Subscribe to our newsletter"), dismiss_newsletter)
```

Whenever Playwright is waiting on an actionability check (for instance, it cannot click because something is in the way) and the registered locator becomes visible, it runs your handler, then retries. The handler should remove the overlay (click a close button); by default Playwright waits for the overlay to disappear after the handler runs. Options include `times=` to limit how often it runs, and `no_wait_after=True` to skip the "wait until hidden" step. You can remove a handler with `page.remove_locator_handler(locator)`.

This API is available in Playwright 1.42 and later. It supersedes older patterns such as wrapping everything in try/except or dismissing banners at fixed points in the test. Use it for *genuinely unpredictable* interruptions. For a banner that always appears on first visit, dismiss it deterministically in setup, or pre-set the consent cookie.

### 12. Timeouts

| Where | How | Default |
| --- | --- | --- |
| One action | `locator.click(timeout=5000)` | 30 s |
| One assertion | `expect(loc).to_be_visible(timeout=10000)` | 5 s |
| All actions on a page | `page.set_default_timeout(15000)` | 30 s |
| Navigations on a page | `page.set_default_navigation_timeout(60000)` | 30 s |
| All pages in a context | `context.set_default_timeout(15000)` | 30 s |
| All assertions globally | `expect.set_options(timeout=10_000)` | 5 s |

Increase a timeout when something is *legitimately slow* (a report that takes 20 seconds to generate). Do not raise global timeouts to hide flakiness; investigate the cause.

### 13. Waiting for network responses and custom conditions

Sometimes the UI gives no clear visible signal, but a network call does:

```python
with page.expect_response(lambda r: "/api/search" in r.url and r.status == 200) as resp_info:
    page.get_by_placeholder("Search").fill("laptop")
data = resp_info.value.json()
```

This is the "register first, then act" pattern from the Tabs lesson applied to responses. `expect_response` accepts a URL glob, a regular expression, or a predicate function.

For arbitrary JavaScript conditions:

```python
page.wait_for_function("() => window.appReady === true")
page.wait_for_function("count => document.querySelectorAll('.item').length >= count", arg=5)
```

`wait_for_function` polls a JavaScript predicate in the page until it is truthy. Use sparingly; prefer visible, user-facing conditions.

### 14. Making flakiness visible: traces and slow motion

- **Trace Viewer:** `context.tracing.start(screenshots=True, snapshots=True)` ... `context.tracing.stop(path="trace.zip")`, then `playwright show-trace trace.zip`. It shows each action with a DOM snapshot before/after, network calls, and console logs. Excellent for understanding what the page looked like when a step failed.
- **Inspector:** `PWDEBUG=1 python test.py`, or `page.pause()`, steps through the test with a live locator picker.
- **Slow motion:** `p.chromium.launch(headless=False, slow_mo=500)` pauses 500 ms between operations, useful when *watching* a test, never as a fix.
- **Repetition:** run the suspicious test many times (e.g. in a loop or with a pytest repeat plugin) to expose flakiness.

---

## Code Examples

The examples use a small, self-contained "dynamic" page created with `set_content()`. JavaScript timers simulate network latency.

### The sample application

```python
from playwright.sync_api import sync_playwright, expect
import re

HTML = """
<h1>Dynamic demo</h1>

<!-- 1. Delayed content with spinner -->
<button id="load">Load users</button>
<div id="spinner" hidden>Loading...</div>
<ul id="users"></ul>

<!-- 2. Toast that auto-dismisses -->
<button id="save">Save</button>
<div id="toast" role="status" hidden></div>

<!-- 3. Button that becomes enabled after 1.5 s -->
<button id="later" disabled>Continue</button>

<!-- 4. Element with a random id -->
<button id="btn-REPLACED">Generated</button>

<!-- 5. Re-rendering list -->
<button id="shuffle">Re-render</button>
<ul id="items"><li>Alpha</li><li>Beta</li><li>Gamma</li></ul>

<script>
  // 1) Load users after 1 second
  document.getElementById('load').onclick = () => {
    const sp = document.getElementById('spinner');
    sp.hidden = false;
    setTimeout(() => {
      sp.hidden = true;
      document.getElementById('users').innerHTML =
        '<li>Maria</li><li>John</li><li>Ann</li>';
    }, 1000);
  };

  // 2) Toast: appears 300ms after click and disappears 3s later
  document.getElementById('save').onclick = () => {
    const t = document.getElementById('toast');
    setTimeout(() => { t.textContent = 'Saved at ' + Date.now(); t.hidden = false; }, 300);
    setTimeout(() => { t.hidden = true; }, 3300);
  };

  // 3) Enable after 1.5 seconds
  setTimeout(() => { document.getElementById('later').disabled = false; }, 1500);

  // 4) Random id
  document.getElementById('btn-REPLACED').id = 'btn-' + Math.random().toString(36).slice(2, 8);

  // 5) Re-render replaces every li with new nodes
  document.getElementById('shuffle').onclick = () => {
    const ul = document.getElementById('items');
    ul.innerHTML = '';
    ['Alpha', 'Beta', 'Gamma'].forEach(t => {
      const li = document.createElement('li'); li.textContent = t; ul.appendChild(li);
    });
  };
</script>
"""
```

The page has five behaviours that mirror the types in the table in Section 1. The JavaScript is intentionally simple: `setTimeout(fn, ms)` runs `fn` after `ms` milliseconds, which simulates server delay.

### Example 1: Auto-wait plus web-first assertion (delayed content)

```python
with sync_playwright() as p:
    browser = p.chromium.launch()
    page = browser.new_page()
    page.set_content(HTML)

    page.get_by_role("button", name="Load users").click()
    expect(page.locator("#spinner")).to_be_visible()
    expect(page.locator("#spinner")).to_be_hidden()
    expect(page.locator("#users li")).to_have_count(3)
    expect(page.locator("#users li")).to_have_text(["Maria", "John", "Ann"])
    browser.close()
```

**Line-by-line**

- `click()` waits for the button to be attached, visible, stable, enabled, and not covered, then clicks. No explicit wait is needed.
- `expect(spinner).to_be_visible()` passes quickly because `hidden = false` is set immediately on click. (If this check were against a very fast operation it could miss the spinner; here it is 1 second long.)
- `expect(spinner).to_be_hidden()` polls until the spinner disappears (about 1 s later), well within the 5 s default.
- `to_have_count(3)` ensures the list has exactly three items, and `to_have_text([...])` verifies their texts in order. For multi-element locators, `to_have_text` accepts a list.
- No `sleep`, no timeouts, no loops. The code reads the way a user would describe the behaviour.

### Example 2: The anti-pattern, and why it fails

```python
page.get_by_role("button", name="Load users").click()
names = page.locator("#users li").all_inner_texts()
print(names)         # [] -> data not loaded yet!
```

- `all_inner_texts()` does not wait; it returns whatever exists *now*, which is an empty list.
- Fix 1: wait for the outcome first: `expect(page.locator("#users li")).to_have_count(3)`; then read.
- Fix 2: use an assertion directly on the list as in Example 1.

```python
# Anti-pattern: fixed sleep
import time
time.sleep(1.2)              # too short on a slow machine, too long on a fast one
```

Never use `time.sleep()` in Playwright tests: it blocks the whole Python thread and is not coordinated with the browser at all.

### Example 3: Elements that become enabled

```python
page.get_by_role("button", name="Continue").click()      # waits up to 30 s for "enabled"
```

- `click()` auto-waits for the Enabled check. After about 1.5 seconds the button becomes enabled and the click happens. You can verify this with the call log by running with `DEBUG=pw:api`.
- To assert the *state transition* explicitly:

```python
btn = page.get_by_role("button", name="Continue")
expect(btn).to_be_enabled()           # waits for the transition
```

- To prove it is disabled at first, assert *immediately after load*: `expect(btn).to_be_disabled()` must run before 1.5 seconds pass. Tests like this are timing-sensitive; use `page.clock` to control time if you need to guarantee ordering.

### Example 4: Toasts

```python
page.get_by_role("button", name="Save").click()
toast = page.get_by_role("status")
expect(toast).to_contain_text("Saved at")        # waits ~300 ms for it to appear
expect(toast).to_be_hidden()                     # default 5 s timeout covers the 3 s display time
```

- The toast appears 300 ms after the click and disappears 3 s later. `to_contain_text` checks a stable substring because the full text contains a timestamp. Asserting the exact text would be wrong since it changes every run.
- `to_be_hidden()` waits (up to 5 s) for it to vanish: 3 s is within limits, but if the toast stayed 8 s you would pass `timeout=10_000`.

### Example 5: Changing IDs

```python
# Brittle: id changes on every load
# page.locator("#btn-x7k2p9").click()

# Stable options
page.get_by_role("button", name="Generated").click()
page.locator("[id^='btn-']").click()     # prefix match: works for any suffix
```

- `get_by_role("button", name="Generated")` identifies the button by its visible label.
- `[id^='btn-']` is a CSS attribute selector meaning "id *starts with* `btn-`". In our page this also matches only one element; always check uniqueness with `count()` before trusting a pattern selector. (`$=` is ends-with, `*=` is contains.)

### Example 6: Re-rendered DOM and lazy locators

```python
items = page.locator("#items li")
first = items.first                         # a recipe, not a node
print(first.inner_text())                   # Alpha

page.get_by_role("button", name="Re-render").click()   # all <li> nodes are replaced
print(first.inner_text())                   # Alpha, no stale element error
expect(items).to_have_text(["Alpha", "Beta", "Gamma"])
```

- `first` is a locator pointing at "the first `li` under `#items`". After re-render, the old node is gone, but the recipe finds the new one. In Selenium the equivalent code would raise a stale-element exception.
- If you want to see the problem that other tools have, use an `ElementHandle`: `handle = page.query_selector("#items li")` followed by a re-render. The handle keeps pointing at the *old, detached* node: reading from it (`inner_text()`) quietly returns stale text, and acting on it (`handle.click()`) fails with "Element is not attached to the DOM". Handles are discouraged for this reason.

### Example 7: Cookie banner with `add_locator_handler`

```python
BANNER_HTML = """
<button id="buy" style="position:fixed;top:10px;left:10px">Buy now</button>
<div id="banner" style="position:fixed;inset:0;background:rgba(0,0,0,.6);display:none;z-index:10">
  <div style="background:white;margin:60px auto;padding:20px;width:300px">
    <p>Subscribe to our newsletter!</p>
    <button id="no">No thanks</button>
  </div>
</div>
<p id="bought"></p>
<script>
  // The banner appears unpredictably after 500 ms
  setTimeout(() => { document.getElementById('banner').style.display = 'block'; }, 500);
  document.getElementById('no').onclick = () => { document.getElementById('banner').remove(); };
  document.getElementById('buy').onclick = () => { document.getElementById('bought').textContent = 'Bought!'; };
</script>
"""
page.set_content(BANNER_HTML)

page.add_locator_handler(
    page.get_by_text("Subscribe to our newsletter!"),
    lambda: page.get_by_role("button", name="No thanks").click(),
)

page.wait_for_timeout(700)                        # demo only: ensure the banner is up and covering the button
page.get_by_role("button", name="Buy now").click()
expect(page.locator("#bought")).to_have_text("Bought!")
```

**Explanation**

- The page shows a full-screen overlay half a second after load, covering the Buy button.
- `add_locator_handler(locator, handler)`: when Playwright runs into trouble because this locator is visible, it runs the handler, then retries. We pass a `lambda` that clicks "No thanks".
- Without the handler, `click()` would keep waiting because "another element intercepts pointer events" and finally time out.
- `page.wait_for_timeout(700)` is used here *only to force the overlay to be present* for demonstration. In a real test you would not need it; the handler runs whenever the overlay appears during any action.

### Example 8: Waiting on a network response

```python
HTML_NET = """
<input id="q" placeholder="Search">
<ul id="results"></ul>
<script>
  document.getElementById('q').addEventListener('input', async e => {
    const r = await fetch('/api/search?q=' + encodeURIComponent(e.target.value));
    const items = await r.json();
    document.getElementById('results').innerHTML = items.map(i => '<li>' + i + '</li>').join('');
  });
</script>
"""

def fake_api(route):
    import json
    route.fulfill(status=200, content_type="application/json",
                  body=json.dumps(["Laptop", "Laptop bag"]))

context = browser.new_context()
context.route("http://test.local/api/**", fake_api)
context.route("http://test.local/", lambda r: r.fulfill(status=200, content_type="text/html", body=HTML_NET))
page = context.new_page()
page.goto("http://test.local/")

with page.expect_response("**/api/search*") as resp:
    page.get_by_placeholder("Search").fill("laptop")
assert resp.value.ok
assert resp.value.json() == ["Laptop", "Laptop bag"]
expect(page.locator("#results li")).to_have_count(2)
```

- The page calls `/api/search` on each `input` event. `context.route(...)` replaces the real API with canned data (mocking is a big topic; here it simply gives us a runnable demo).
- `page.expect_response("**/api/search*")` registers interest in a response whose URL matches the glob; we then trigger it with `fill`.
- `resp.value` is a `Response`; `.ok` is True for 2xx status; `.json()` parses the body.
- The final `expect` waits for the UI to *render* the data. The response arriving does not mean the DOM has updated yet, so always assert on the DOM as well.

### Example 9: Infinite scroll loop (pattern)

```python
def load_all_items(page, item_selector=".feed-item", max_rounds=20):
    items = page.locator(item_selector)
    last = 0
    for _ in range(max_rounds):
        count = items.count()
        if count == last:
            break                        # no more items appeared
        last = count
        items.last.scroll_into_view_if_needed()
        page.wait_for_timeout(300)       # small settle; better: wait for a loading indicator to appear/disappear
    return last
```

- The loop scrolls the last item into view, which triggers loading more, and stops when the count stops growing.
- The short `wait_for_timeout` is a pragmatic compromise; a better approach is `expect(items).not_to_have_count(count)` inside a `try/except` for the final round. Always bound loops with `max_rounds`.

---

## Real-World Scenarios

### Scenario 1: Search with auto-complete (building on Monday)

Typing triggers a debounced API call. Without waiting for results, a test clicks a suggestion that is about to be replaced.

```python
box = page.get_by_role("combobox", name="Search")
box.press_sequentially("lapt", delay=50)
option = page.get_by_role("option", name="Laptop bag")
expect(option).to_be_visible()       # waits for the (final) suggestion list
option.click()
```

Because Playwright re-resolves the locator on each action, and the click waits for the element to be *stable*, you avoid clicking an option mid-update in most cases. If the list re-renders between visibility and click, Playwright retries.

### Scenario 2: Order status that updates by polling

An order page polls the server every 5 seconds until the status becomes "Shipped". Your test should wait up to, say, 20 seconds:

```python
expect(page.get_by_test_id("order-status")).to_have_text("Shipped", timeout=20_000)
```

One assertion with a generous but explicit timeout: no sleeps and no manual loops. Document *why* the timeout is long.

### Scenario 3: A dashboard with live-updating numbers

A visitor counter changes every second. Do not assert exact values. Assert properties:

```python
value = int(page.get_by_test_id("visitors").inner_text().replace(",", ""))
assert value > 0
```

or assert format: `expect(page.get_by_test_id("visitors")).to_have_text(re.compile(r"^[\d,]+$"))`. Or freeze time/data in a test environment.

### Scenario 4: Slow third-party widget

A page includes a chat bubble that loads late and sometimes overlays the footer's Submit button. Register `add_locator_handler` for the bubble's "close" control at the start of the test or in a shared setup (fixtures on Wednesday), instead of sprinkling `try/except` blocks everywhere.

---

## Common Pitfalls and Best Practices

1. **Fixed sleeps.** `time.sleep()` and `wait_for_timeout()` as a "fix" produce slow and flaky tests. Replace them with assertions and auto-waiting. (Legitimate uses are rare: proving a negative, as in the Tabs lesson, or a deliberate demonstration.)
2. **Reading values before they exist.** `inner_text()`, `count()`, `all_inner_texts()`, `is_visible()`, and `is_checked()` are *instant* snapshots. Use `expect(...)` for anything that may change.
3. **`is_visible()` as a wait.** `if page.get_by_text("Done").is_visible():` does **not** wait. It returns immediately. Use `expect(...).to_be_visible()` or `wait_for`.
4. **Strict mode violations.** Dynamic lists often contain duplicates. Narrow your locator rather than adding `.first` blindly.
5. **Over-reliance on `force=True`.** It skips actionability checks, so it can click covered or disabled elements, hiding real defects. Use only when you have proven the check is wrong for that control.
6. **Assertions on exact text that contains volatile parts.** Use `to_contain_text`, regular expressions, or compute expectations.
7. **Raising global timeouts.** It masks real slowness. Fix the cause or set a targeted timeout.
8. **Relying on `networkidle`.** `wait_for_load_state("networkidle")` waits for network silence, which never happens on pages with polling, analytics, or websockets. Playwright's docs discourage it; assert on UI instead.
9. **`ElementHandle` usage.** Handles go stale; use Locators.
10. **Not reading the call log.** The timeout message tells you which actionability check is failing.
11. **Animations.** Playwright's *stable* check handles most, but if an animation never settles (a pulsing button), pass `animations="disabled"` for screenshots or use `click(force=True)` only after analysis; better, ask developers for a reduced-motion option in test builds. You can emulate it: `browser.new_context(reduced_motion="reduce")`.
12. **Tests depending on each other's timing.** Isolate tests and set up state explicitly (fixtures are covered in depth on Wednesday).

**Best practices:** wait for outcomes, not for time; choose resilient locators; scope locators; keep assertions close to actions; use the trace viewer to debug; treat any flaky test as a bug to investigate, not a nuisance to retry. (Automatic test retries are a framework feature covered in depth on Wednesday; they are a safety net, not a fix.)

---

## Mini Practice Exercises

### Exercise 1: Replace the sleep

Rewrite this flaky snippet without any sleeps:

```python
page.click("#load")
time.sleep(2)
assert page.inner_text("#users") == "MariaJohnAnn"
```

<details>
<summary>Solution</summary>

```python
page.get_by_role("button", name="Load users").click()
expect(page.locator("#users li")).to_have_text(["Maria", "John", "Ann"])
```
</details>

### Exercise 2: Spinner discipline

Using the sample page, write a test that verifies: after clicking Load users the spinner appears, then disappears, and exactly three users are listed. Explain what could go wrong with the "spinner appears" check on a very fast network. *Hint:* the spinner might vanish before the assertion polls.

### Exercise 3: Volatile text

Write a test for the toast that does not hard-code the timestamp: assert text matches `Saved at \d+` using a regular expression with `to_have_text(re.compile(...))`.

<details>
<summary>Solution</summary>

```python
page.get_by_role("button", name="Save").click()
expect(page.get_by_role("status")).to_have_text(re.compile(r"^Saved at \d+$"))
```
</details>

### Exercise 4: Resilient locator

Add a second button with a random id and the label "Generated 2". Write two different stable locators for it and verify each matches exactly one element with `to_have_count(1)`.

### Exercise 5: Re-render

Prove, using the `items` list, that a Locator survives re-render while an `ElementHandle` from `page.query_selector()` does not. Show that `handle.is_visible()` is `False` after the re-render and that `handle.click(timeout=1500)` raises an error saying the element is not attached; print that message.

### Exercise 6: Overlay handler

Modify Example 7 so the banner appears *twice* (500 ms and 1500 ms). Use `times=2` in `add_locator_handler` or leave it unlimited, and prove the Buy click works in both cases.

*Hint:* `page.add_locator_handler(locator, handler, times=2)`.

### Exercise 7: Practice site

On `https://the-internet.herokuapp.com/dynamic_loading/1` (element hidden, then shown) and `/dynamic_loading/2` (element rendered after the fact), click Start and assert "Hello World!" appears. Notice that the same assertion works for both: `expect(page.locator("#finish")).to_have_text("Hello World!")`. Explain why Playwright needs no separate handling for "hidden" versus "not yet in the DOM".

*Answer:* `expect` retries until the locator resolves *and* the text matches; whether the element was hidden or absent beforehand, the condition is simply "not yet true".

### Exercise 8 (stretch): Diagnose with the call log

Create a button covered by a transparent overlay (a `div` with `position: fixed; inset: 0`). Call `click(timeout=2000)`, catch the `TimeoutError`, print it, and identify the line in the log that names the intercepting element.

---

## Summary / Key Takeaways

- Dynamic pages are the norm. Flaky tests come from timing assumptions; the cure is conditional waiting.
- Playwright **auto-waits** before actions (attached, visible, stable, receives events, enabled, editable) and **retries `expect` assertions** until they pass or time out. Do not add waits before actions.
- Prefer `expect(locator)...` over reading a value and asserting in plain Python for anything that changes.
- Use `locator.wait_for(state=...)` and `page.wait_for_function()` only when no action or assertion is available.
- Locators are lazy recipes, so re-rendering does not produce stale elements. Avoid `ElementHandle`.
- Choose locators by role, label, text, or test id; use prefix/suffix attribute selectors for generated ids; avoid positional and deeply structural selectors.
- `add_locator_handler` handles unpredictable overlays; `expect_response` synchronises with the network; targeted timeouts handle legitimately slow operations.
- Read the call log, use the Trace Viewer, and never "fix" a flaky test with a sleep. Reusable waiting helpers and framework-level retry settings are covered in depth on Wednesday.

---

## External Resources

- Playwright Python docs, Auto-waiting (actionability): https://playwright.dev/python/docs/actionability
- Playwright Python docs, Assertions: https://playwright.dev/python/docs/test-assertions
- Playwright Python docs, Locators: https://playwright.dev/python/docs/locators
- Playwright Python API reference, `page.add_locator_handler`: https://playwright.dev/python/docs/api/class-page#page-add-locator-handler
- Playwright Python docs, Trace Viewer: https://playwright.dev/python/docs/trace-viewer
