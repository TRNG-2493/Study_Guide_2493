# Interview Questions: Week 4 - PyTest-Playwright - Friday

Scope: Creating Playwright tests, the Playwright test runner, built-in locators, filtering and chaining locators, auto-waiting and synchronization, the Playwright Inspector, and record and playback. Every answer can be found in Friday's written lessons.

---

## Beginner (Foundational)

### Q1: In a `pytest-playwright` test, what does the `page` fixture give you, and why does it make tests reliable?
**Keywords:** page fixture, browser context, isolation, fresh per test
**Hint:** Think about what the plugin creates for each test before it hands you the page.
<details>
<summary>Click to Reveal Answer</summary>

The plugin starts a browser once per run (session scope), creates a brand-new browser context for each test (function scope), opens a new page (tab) in it, and closes the page and context afterwards. Because every test gets a fresh context, with fresh cookies, local storage and cache, tests do not leak state into each other. That built-in test isolation is a major reason Playwright tests are reliable. I do not write any browser setup or `close()` code, I just ask for `page` as a parameter, like any PyTest fixture.

```python
def test_title(page: Page):
    page.goto("https://playwright.dev/python/")
    expect(page).to_have_title(re.compile("Playwright"))
```
</details>

---

### Q2: What is the difference between a web-first assertion like `expect(locator).to_be_visible()` and `assert locator.is_visible()`?
**Keywords:** retry, web-first, snapshot, flaky, 5 seconds
<details>
<summary>Click to Reveal Answer</summary>

`expect(...)` is a web-first assertion: it re-queries the locator and re-checks the condition repeatedly until it passes or the timeout (5 seconds by default) expires. `is_visible()` is a snapshot that returns the answer at that single instant, so a plain `assert` on it does not retry. If the element appears 200 ms later, the plain `assert` fails and the test is flaky. The timeout is a ceiling, not a delay, so if the element shows up in 200 ms the test continues after 200 ms. I would use `expect()` for anything that depends on the page, and plain `assert` only for pure Python values I already extracted.
</details>

---

### Q3: What are the three responsibilities in the Playwright runner stack: PyTest, the `pytest-playwright` plugin and the Playwright library?
**Keywords:** discovery, fixtures, CLI options, artifacts, browser control
<details>
<summary>Click to Reveal Answer</summary>

Playwright for Python does not ship its own runner, it uses PyTest. PyTest finds and runs tests, handles fixtures, markers and parametrization, and reports pass or fail. The `pytest-playwright` plugin provides fixtures such as `page`, `context` and `browser`, adds command-line options such as `--headed` and `--browser`, and manages artifacts like screenshots, video and traces. The Playwright library is the part that actually controls the browser. So everything I know from PyTest, like `-k`, `-m` and node ids, still works.
</details>

---

### Q4: A test fails on a CI server that you cannot watch. Which Playwright artifacts can you capture, and which one is the most powerful?
**Keywords:** screenshot, video, trace, retain-on-failure, show-trace
**Hint:** There are three artifact types, each with its own command-line option.
<details>
<summary>Click to Reveal Answer</summary>

There are three: screenshots (`--screenshot only-on-failure`), videos (`--video retain-on-failure`) and traces (`--tracing retain-on-failure`). The trace is the most powerful. It is a `.zip` with a timeline of every action, a DOM snapshot before and after each action, network requests, console messages and the source line. I open it with `playwright show-trace trace.zip` and click through each step like time travel. A good team default is `--tracing retain-on-failure` plus `--screenshot only-on-failure`, which is cheap when tests pass and rich when they fail.
</details>

---

### Q5: What is the recommended priority order of Playwright locators, and why prefer built-in locators over CSS or XPath?
**Keywords:** get_by_role, user-facing, resilient, test id, last resort
<details>
<summary>Click to Reveal Answer</summary>

The order is roughly `get_by_role`, `get_by_label`, `get_by_placeholder`, `get_by_text`, `get_by_alt_text`, `get_by_title`, `get_by_test_id`, and finally CSS or XPath through `page.locator()` as a last resort. Built-in locators describe what the user sees, such as "the button named Login", while CSS and XPath describe how the page is built. A redesign that renames a CSS class breaks the CSS-based test but not the role-based one. Role locators also act as a light accessibility check, because if a role locator cannot find your button, a screen reader probably cannot either.
</details>

---

### Q6: What is the difference between `get_by_role("button", name="Sign in")` and the same call with `exact=True`?
**Keywords:** name, substring, case-insensitive, exact, strict mode
<details>
<summary>Click to Reveal Answer</summary>

By default `name` is a case-insensitive substring match on the accessible name. With a page that has "Sign in" and "Sign in with Google", the default locator matches both buttons, so clicking it would raise a strict mode error. Adding `exact=True` makes it match the whole string, case-sensitively, so only the first button matches. The substring default is deliberate because it makes tests less fragile to small wording changes, and I add `exact=True` when I need precision.

```python
page.get_by_role("button", name="Sign in")                # 2 matches
page.get_by_role("button", name="Sign in", exact=True)    # 1 match
```
</details>

---

### Q7: What actionability checks does Playwright perform before a `click()`, and what happens if one fails?
**Keywords:** attached, visible, stable, enabled, receives events
<details>
<summary>Click to Reveal Answer</summary>

Before a click, Playwright waits until the element is attached to the DOM, visible, stable (not moving, for example mid-animation), enabled, and able to receive events, meaning no overlay or modal covers the click point. `fill()` additionally needs the element to be editable, but it does not need stable or receives-events. If a check fails, Playwright keeps retrying until everything passes or the action timeout (30 seconds by default) expires, and only then raises a `TimeoutError`. That is why I do not need explicit waits before ordinary actions.
</details>

---

### Q8: What are the default timeouts for actions, navigation and `expect()` assertions, and in what unit are they set?
**Keywords:** 30 seconds, 5 seconds, milliseconds, set_default_timeout, per-call timeout
<details>
<summary>Click to Reveal Answer</summary>

Actions such as `click` and `fill` default to 30 seconds, navigation also to 30 seconds, and `expect()` assertions to only 5 seconds. All values are in milliseconds, so `timeout=5` is 5 ms, not 5 seconds, and `15_000` is the readable way to write 15 seconds. I can change them with `page.set_default_timeout()` and `page.set_default_navigation_timeout()`, or pass `timeout=` on a single call. I would raise a timeout only for genuinely slow operations, and never use a huge global timeout to hide a problem.
</details>

---

### Q9: Why is `time.sleep()` (or `page.wait_for_timeout()`) considered an anti-pattern in Playwright tests?
**Keywords:** fixed pause, flaky, slow, race condition, expect
<details>
<summary>Click to Reveal Answer</summary>

A fixed pause is either too short, so the test is still flaky because of the race between the script and the app, or too long, so the suite is slow. It always costs the full time even when the page was ready earlier. Playwright's documentation says `wait_for_timeout` is for debugging only. The fix is to wait for the real condition, which is usually an action's built-in auto-waiting or an `expect()` assertion that retries and proceeds the instant it is true.
</details>

---

### Q10: What is strict mode in Playwright locators, and how should you respond to a strict mode violation?
**Keywords:** strict mode, multiple elements, more specific, filter, first
<details>
<summary>Click to Reveal Answer</summary>

Locators are strict: if an action or single-element assertion needs exactly one element but the locator matches several, Playwright raises an error such as "strict mode violation ... resolved to 6 elements" instead of silently picking one. That prevents clicking the wrong element. The right response is to make the locator more specific, by chaining into a container or using `filter()`, not to silence it with `.first`. Count assertions like `to_have_count` and list methods do work with multiple elements.
</details>

---

### Q11: What is the difference between `filter(has=...)` and `and_()` on a locator?
**Keywords:** has, descendant, and_, same element, or_
<details>
<summary>Click to Reveal Answer</summary>

`filter(has=other)` keeps elements that **contain a descendant** matching the other locator, evaluated relative to the outer element. `and_(other)` keeps elements that satisfy **both** locators themselves, so it is an AND on the same element. For example, `page.get_by_role("listitem").filter(has=page.get_by_role("heading", name="Product 2"))` finds list items containing that heading, while `page.get_by_role("button").and_(page.locator(".btn-primary"))` finds buttons that are also primary. `or_()` is the either-condition counterpart, and I would use it sparingly because it can hide uncertain test state.
</details>

---

### Q12: How do you start the Playwright Inspector, and what do `PWDEBUG=1` and `page.pause()` each do?
**Keywords:** PWDEBUG, page.pause, headed, step over, timeouts disabled
**Hint:** One affects every Playwright action, the other stops at one point in the code.
<details>
<summary>Click to Reveal Answer</summary>

`PWDEBUG=1` runs all Playwright actions in debug mode: the browser is headed, timeouts are disabled and the Inspector opens paused at the first action. `page.pause()` stops execution at one line and opens the Inspector, which is great when steps 1 to 20 are fine and the problem is at step 21. `page.pause()` only has an effect when headed or with `PWDEBUG=1`, so in headless CI it is ignored, though I still remove it before committing. I also use `-s` so the output is not captured, and I run only one test at a time with a node id.
</details>

---

### Q13: What is the difference between the Playwright Inspector and the Trace Viewer, and when do you use each?
**Keywords:** live, post-mortem, PWDEBUG, show-trace, CI
<details>
<summary>Click to Reveal Answer</summary>

The Inspector is used **during** a run: it is live and interactive on my machine, started with `PWDEBUG=1` or `page.pause()`, for developing and debugging locally. The Trace Viewer is used **after** a run: it is a post-mortem tool, started with `playwright show-trace trace.zip`, and a trace produced on CI can be opened anywhere. So I use the Inspector to develop and the trace to diagnose failures I cannot reproduce live.
</details>

---

### Q14: What does `playwright codegen --target python-pytest` do, and why is a raw recording only a draft?
**Keywords:** codegen, python-pytest, no assertions, redundant clicks, refactor
<details>
<summary>Click to Reveal Answer</summary>

`playwright codegen` opens a browser plus the Inspector, watches what I do and writes real, editable Python code using the same modern locators I would write by hand. With `--target python-pytest` I get a test function that uses the `page` fixture, and `-o file.py` saves it to a file. A raw recording is only a draft because it contains no assertions, so it is a script rather than a test, uses a generic name like `test_example`, has redundant `click()` calls before `fill()`, repeats login in every test and hard-codes the data from my session.
</details>

---

## Intermediate (Application)

### Q15: Your team overrides `browser_context_args` in `conftest.py` to set a viewport, but after the change some plugin defaults seem lost. What went wrong and how do you fix it?
**Keywords:** browser_context_args, spread, **unpack, session scope, conftest
**Hint:** The fixture receives the original value as a parameter.
<details>
<summary>Click to Reveal Answer</summary>

Most likely the fixture returns a new dictionary containing only the viewport, so it throws away the plugin's default context options. The fix is to take the original `browser_context_args` as a parameter and unpack it with `**`, then add or override keys. Because the plugin passes this dictionary to `browser.new_context()`, I can also add things like `locale`, `timezone_id` for deterministic formatting. It is a session-scoped fixture in `conftest.py`.

```python
@pytest.fixture(scope="session")
def browser_context_args(browser_context_args):
    return {**browser_context_args, "viewport": {"width": 1280, "height": 720}}
```
</details>

---

### Q16: On an admin page you must delete user "Raj" from a table, but your `filter(has_text="Active")` for active users also returns Raj, whose status is "Inactive". How do you write robust locators for both needs?
**Keywords:** filter, has_text, has_not_text, substring, row, chaining
<details>
<summary>Click to Reveal Answer</summary>

`has_text` is a case-insensitive substring match, so "Active" matches "Inactive". For active users I chain `filter(has_text="Active").filter(has_not_text="Inactive")`, because every chained filter must be satisfied (a regex like `^Active$` also works). To delete Raj, I filter the row by name and chain the button inside it, rather than using a brittle position-based XPath. I would then assert the row is gone with `to_have_count(0)`.

```python
rows = page.get_by_role("row")
active = rows.filter(has_text="Active").filter(has_not_text="Inactive")
rows.filter(has_text="Raj").get_by_role("button", name="Delete").click()
expect(rows.filter(has_text="Raj")).to_have_count(0)
```
</details>

---

### Q17: A test passes on a developer laptop but fails on the slower CI server. The code has `time.sleep(2)` after clicking Login, and the failure log shows `Timeout 30000ms exceeded` with a call log line `<div class="modal"> intercepts pointer events`. How do you diagnose and fix both problems?
**Keywords:** sleep, expect, call log, intercepts pointer events, receives events
<details>
<summary>Click to Reveal Answer</summary>

These are two separate issues. The sleep is a race condition that happens to be long enough locally but not on CI, so I replace it with a retrying assertion on the real outcome, for example `expect(page.locator(".title")).to_have_text("Products")`. The timeout error should be read through its call log, which says why the wait never finished: here an overlay is covering the target, so the "receives events" actionability check never passed. The fix is to handle that modal properly (close it in setup, or have the environment disable it), not to raise the timeout. Increasing the timeout globally would only hide the cause and make failures slower.
</details>

---

### Q18: You need to verify that a search request returns HTTP 200 when the user types in the search box. How do you wait for the API response in Playwright, and what ordering mistake should you avoid?
**Keywords:** expect_response, with block, listener before action, predicate, status
<details>
<summary>Click to Reveal Answer</summary>

I use `page.expect_response()` as a context manager around the action that triggers the request. The `with` block starts listening first, runs the action inside, and then `response_info.value` waits for the response if it has not arrived yet. The mistake to avoid is creating the listener after the action, because a fast response could already have gone by. It accepts a URL pattern, a regex or a predicate function, and afterwards I use normal `expect()` for the UI result, for example the spinner being hidden.

```python
with page.expect_response(lambda r: "/api/search" in r.url and r.status == 200):
    page.get_by_placeholder("Search products").fill("laptop")
expect(page.locator(".spinner")).to_be_hidden()
```
</details>

---

### Q19: You recorded a checkout flow with codegen and your manager wants to commit it. What would you do first to turn it into a professional test?
**Keywords:** rename, assertions, fixture, locators, marker, docstring
<details>
<summary>Click to Reveal Answer</summary>

I would not commit the raw recording. I follow the refactoring checklist: rename the test to describe behavior (like `test_user_can_add_backpack_to_cart`), remove noise such as redundant clicks before `fill()`, and improve weak locators with role, label or filtered chains. Then I add at least one `expect()` per important outcome, extract repeated steps such as login into a fixture, extract data into constants or parametrization, and add a marker like `smoke` and a docstring linking the manual test case id. Finally I run it several times, and in different browsers, to check stability. I also make sure files such as `auth.json` with session tokens are never committed.
</details>

---

## Advanced (Deep Dive)

### Q20: You write `backpack = page.locator(".inventory_item").filter(has_text="Sauce Labs Backpack")`, click its "Add to cart" button, and then assert `backpack.get_by_role("button", name="Remove")` is visible. Why does this work even though the button's text changed, and why should you be careful with `count()` and `all()` on a list that is still loading?
**Keywords:** lazy locator, re-evaluated, snapshot, count, to_have_count
**Hint:** When does Playwright actually search the page?
<details>
<summary>Click to Reveal Answer</summary>

A locator is lazy: creating it does not touch the page, and Playwright only searches for the element when I perform an action or assertion on it. So `backpack` is re-evaluated each time it is used, and after the click the card is still found and the chained role locator now matches the "Remove" button. That is also why Playwright avoids classic stale-element errors. In contrast `count()`, `all()` and `all_inner_texts()` are snapshots that do not wait for the list to finish loading. I first assert something like `expect(names).to_have_count(6)`, which retries, and only then collect the data. The lesson also warns that looping over `.all()` while clicking items that change the list (such as deleting rows) can point at removed elements, so I would re-query on each iteration.

```python
names = page.locator(".inventory_item_name")
expect(names).to_have_count(6)       # waits
texts = names.all_inner_texts()      # snapshot, now safe
```
</details>

---

## Coverage Table

| Lesson | Question numbers |
|--------|------------------|
| Creating Playwright Tests | Q1, Q2, Q20 |
| Playwright Test Runner | Q3, Q4, Q15 |
| Built-in Locators | Q5, Q6 |
| Filtering and Chaining Locators | Q10, Q11, Q16, Q20 |
| Auto-Waiting and Synchronization | Q7, Q8, Q9, Q17, Q18 |
| Playwright Inspector | Q12, Q13 |
| Record and Playback | Q14, Q19 |

Distribution: 14 Beginner (Q1-Q14), 5 Intermediate (Q15-Q19), 1 Advanced (Q20).
