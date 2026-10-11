# Weekly Knowledge Check: Playwright Core Automation (Friday)

**Week 4: PyTest & Playwright | Day 5 (Friday)**

## Topics Covered

- Creating Playwright tests (`pytest-playwright`, the `page` fixture, `expect()`, Arrange-Act-Assert)
- The Playwright test runner (CLI options, artifacts and traces, `pytest.ini`, `conftest.py`, parallel runs and retries)
- Auto-waiting and synchronization (actionability, web-first assertions, explicit waits, timeouts, reading call logs)
- Built-in locators (`get_by_role`, `get_by_label`, `get_by_placeholder`, `get_by_text`, `get_by_test_id`, `exact`)
- Filtering and chaining locators (`filter`, `and_`, `or_`, `first`/`last`/`nth`, list methods)
- The Playwright Inspector (`PWDEBUG=1`, `page.pause()`, Pick locator, Inspector vs Trace Viewer)
- Record and playback (`playwright codegen`, saved login state, refactoring a recording)

## Instructions

1. Read each question and decide on your answer **before** opening the solution.
2. Tick the box (`- [x]`) of the option you choose, or write your answer for True/False and Fill-in-the-Blank questions.
3. Click **Click for Solution** to reveal the correct answer, the explanation and, for multiple choice and code prediction questions, why the other options are wrong.
4. For every question you miss, re-read the matching lesson before moving on.
5. The code prediction snippets assume a Playwright `page` is available (as in a PyTest test) and `from playwright.sync_api import expect`.

---

## Part 1: Creating Playwright Tests

### 1. [MCQ] What does the `pytest-playwright` plugin do for you so that a test only needs to name `page` as a parameter?
- [ ] A) It replaces PyTest with its own separate test runner
- [ ] B) It converts every test function into an `async` function automatically
- [ ] C) It records your manual clicks and writes the test for you
- [ ] D) It provides fixtures that create the Browser, Browser Context and Page for you

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** D) It provides fixtures that create the Browser, Browser Context and Page for you

**Explanation:** The plugin supplies fixtures (`page`, `context`, `browser`, ...) that launch the browser, create a context and a page, and clean up afterwards.

- **Why others are wrong:**
  - A) Playwright for Python uses PyTest as its runner; the plugin adds fixtures and options to PyTest.
  - B) Our tests use the sync API; nothing is converted to `async`.
  - C) Recording is a different feature (`playwright codegen`), not what the plugin's fixtures do.
</details>

---

### 2. [MCQ] Which pair of commands installs Playwright's PyTest plugin AND downloads the browsers it controls?
- [ ] A) `pip install pytest-playwright` only
- [ ] B) `pip install pytest-playwright` followed by `playwright install`
- [ ] C) `playwright install` only
- [ ] D) `pip install pytest` followed by `pytest --install-browsers`

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** B) `pip install pytest-playwright` followed by `playwright install`

**Explanation:** `pip install pytest-playwright` installs the plugin (and the `playwright` package); `playwright install` downloads the Chromium, Firefox and WebKit binaries.

- **Why others are wrong:**
  - A) Without `playwright install` the browsers are missing and you get an error like "Executable doesn't exist".
  - C) This downloads browsers but does not install the plugin or the Python package that provides the `page` fixture.
  - D) This is not the installation step shown in the lesson; browsers are downloaded with `playwright install`.
</details>

---

### 3. [True/False] True or False: Because the `page` fixture is function-scoped, a cookie set during one test is still available in the next test.
- [ ] True
- [ ] False

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** False

**Explanation:** Each test gets a brand-new browser context with fresh cookies, local storage and cache, so state does not leak between tests.

</details>

---

### 4. [Code Prediction] Two tests run in this order (file order). What do the two `print` calls output?
```python
def test_a(page):
    page.context.add_cookies([{"name": "s", "value": "1", "url": "https://example.com"}])
    print("A:", len(page.context.cookies()))

def test_b(page):
    print("B:", len(page.context.cookies()))
```
- [ ] A) `A: 1` then `B: 0`
- [ ] B) `A: 1` then `B: 1`
- [ ] C) `A: 0` then `B: 0`
- [ ] D) `A: 0` then `B: 1`

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** A) `A: 1` then `B: 0`

**Explanation:** Test A adds one cookie to its own context. Test B receives a fresh context with no cookies, so test isolation gives 0.

- **Why others are wrong:**
  - B) That would mean the cookie leaked into test B, which is exactly what the per-test context prevents.
  - C) Test A just added a cookie to its context, so its count is 1, not 0.
  - D) Reverses the behaviour: the count is 1 where the cookie was added, and nothing carries into the next test.
</details>

---

### 5. [MCQ] Which statement correctly describes the scopes behind the `page` fixture?
- [ ] A) A new browser is launched for every test, and all tests share one context
- [ ] B) One browser, one context and one page are shared by every test in the run
- [ ] C) The browser is started once per test run (session scope); each test gets a new context and page (function scope)
- [ ] D) The browser is session scoped, but the context is created once per file and shared by its tests

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** C) The browser is started once per test run (session scope); each test gets a new context and page (function scope)

**Explanation:** The `browser` fixture is session-scoped, while the `context` and `page` are created fresh for each test, which gives built-in isolation.

- **Why others are wrong:**
  - A) The browser launches once per run, and contexts are not shared.
  - B) Sharing everything would make tests leak state into each other, the opposite of what the plugin does.
  - D) The context is function-scoped (per test), not per file.
</details>

---

### 6. [MCQ] When does Playwright actually search the page for the element described by `page.locator("#login-button")`?
- [ ] A) Immediately, at the moment the locator is created
- [ ] B) Only when you perform an action or assertion on it, because locators are lazy
- [ ] C) Once, at page load, and the result is cached for the whole test
- [ ] D) Only when the test finishes, during teardown

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** B) Only when you perform an action or assertion on it, because locators are lazy

**Explanation:** A locator is a recipe, not a found element; it is evaluated freshly each time it is used, which also avoids "stale element" errors.

- **Why others are wrong:**
  - A) Creating a locator does not touch the page.
  - C) Caching would bring back stale elements; Playwright re-queries at use time.
  - D) Evaluation happens at action/assertion time, not at teardown.
</details>

---

### 7. [MCQ] Why is `assert page.locator(".title").is_visible()` a poor choice for checking that a heading appears after a login click?
- [ ] A) It only works in headed mode
- [ ] B) `is_visible()` always returns `False` for headings
- [ ] C) It checks only once, immediately, with no retry, so it can fail if the element appears slightly later
- [ ] D) Plain `assert` cannot be used inside PyTest tests

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** C) It checks only once, immediately, with no retry, so it can fail if the element appears slightly later

**Explanation:** `is_visible()` returns the answer at that instant; `expect(locator).to_be_visible()` keeps retrying (up to 5 seconds by default).

- **Why others are wrong:**
  - A) Headed or headless does not change that `is_visible()` is an instant check.
  - B) `is_visible()` returns the real state at that moment; the problem is timing, not heading elements.
  - D) Plain `assert` is fine for pure Python values; it is just wrong for page state that needs waiting.
</details>

---

### 8. [Fill-in-the-Blank] To assert that an element does NOT exist on the page, the lesson uses `expect(locator).to_have_count(____)`.
Your answer: `________`

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** `0`

**Explanation:** `to_have_count(0)` waits until no elements match, which is the correct way to assert that an element does not exist (for example, an empty cart badge).

</details>

---

### 9. [MCQ] A trainee saves `test_login.py` containing `def check_login(page):` and runs `pytest`. What happens?
- [ ] A) It runs normally, because the file name starts with `test_`
- [ ] B) PyTest collects it but marks it as skipped
- [ ] C) PyTest raises an error asking you to register the function in `pytest.ini`
- [ ] D) The function is not collected as a test, because test functions must be named `test_*`

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** D) The function is not collected as a test, because test functions must be named `test_*`

**Explanation:** The lesson's common mistake: a function such as `check_login()` is not collected; use `test_*.py` files and `test_*` function names.

- **Why others are wrong:**
  - A) The file name is fine, but the function name `check_login` does not start with `test_`, so it never runs.
  - B) PyTest does not skip it; it simply never collects it.
  - C) No registration is needed; discovery is by naming convention.
</details>

---

### 10. [MCQ] Why does the lesson recommend using `--base-url` and writing `page.goto("/")`?
- [ ] A) The same tests can run against development, staging and other environments by changing one command-line option instead of editing code
- [ ] B) It makes the page load faster than a full URL
- [ ] C) It is required for `page.goto()` to work at all
- [ ] D) It disables auto-waiting for navigation

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** A) The same tests can run against development, staging and other environments by changing one command-line option instead of editing code

**Explanation:** A base URL lets relative paths resolve against whatever environment you pass in, so environment switching is a single setting.

- **Why others are wrong:**
  - B) Speed is not the reason; the benefit is portability across environments.
  - C) Full URLs work fine; the base URL is optional.
  - D) Auto-waiting is unrelated; `goto` still waits for the page to load.
</details>

---

### 11. [MCQ] In the Arrange-Act-Assert pattern, which phase is `page.locator("#login-button").click()` in a login test?
- [ ] A) Arrange, because it prepares a known starting state
- [ ] B) Act, because it performs the behavior under test
- [ ] C) Assert, because it verifies the outcome
- [ ] D) None of them; a click is not part of the pattern

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** B) Act, because it performs the behavior under test

**Explanation:** Arrange gets to a known state (open the page), Act performs the behavior (fill, click), Assert verifies the observable outcome (`expect`).

- **Why others are wrong:**
  - A) Arranging is opening the page or preparing data, such as `page.goto(...)`.
  - C) Verification is done with `expect()` assertions.
  - D) Clicks and fills are the Act phase of the pattern.
</details>

---

## Part 2: The Playwright Test Runner

### 12. [MCQ] Which component finds the tests, runs them, and handles fixtures, markers and parametrization in a Playwright for Python project?
- [ ] A) PyTest
- [ ] B) The `pytest-playwright` plugin
- [ ] C) A built-in Playwright runner
- [ ] D) The browser itself

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** A) PyTest

**Explanation:** Playwright for Python does not ship its own runner; PyTest does discovery and running, while the plugin adds fixtures, CLI options and artifact handling.

- **Why others are wrong:**
  - B) The plugin provides fixtures, options and artifacts, but PyTest discovers and runs tests.
  - C) The lesson states Playwright for Python does not ship its own separate runner.
  - D) The browser is controlled by the Playwright library; it does not discover or run tests.
</details>

---

### 13. [MCQ] Which command runs your whole suite in Firefox?
- [ ] A) `pytest --firefox`
- [ ] B) `pytest --browser-channel firefox`
- [ ] C) `pytest --headed firefox`
- [ ] D) `pytest --browser firefox`

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** D) `pytest --browser firefox`

**Explanation:** `--browser` chooses `chromium`, `firefox` or `webkit` and can be repeated to run in several browsers.

- **Why others are wrong:**
  - A) There is no `--firefox` flag in the plugin's option table.
  - B) `--browser-channel` is for installed branded browsers such as `chrome` or `msedge`.
  - C) `--headed` only shows the window; it does not select a browser.
</details>

---

### 14. [Code Prediction] A file contains four tests, shown below. Which tests are selected by `pytest -k "login and not locked"`?
```python
def test_valid_login(): ...
def test_locked_login(): ...
def test_login_empty(): ...
def test_cart(): ...
```
- [ ] A) `test_valid_login`, `test_locked_login` and `test_login_empty`
- [ ] B) Only `test_locked_login`
- [ ] C) `test_valid_login` and `test_login_empty`
- [ ] D) All four tests

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** C) `test_valid_login` and `test_login_empty`

**Explanation:** `-k` matches names: `login` must appear and `locked` must not. `test_cart` has no `login`, and `test_locked_login` contains `locked`.

- **Why others are wrong:**
  - A) `test_locked_login` is excluded by `not locked`.
  - B) `-k` with `not locked` removes the locked test; it does not select it.
  - D) `-k` filters by name expression, so `test_cart` is deselected too.
</details>

---

### 15. [Fill-in-the-Blank] After a run with `--tracing on`, you open the trace with `playwright ____-trace test-results/<folder>/trace.zip`.
Your answer: `________`

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** `show`

**Explanation:** The command is `playwright show-trace`; the Trace Viewer lets you click through every action with DOM snapshots, network, console and source.

</details>

---

### 16. [MCQ] Which combination does the lesson recommend as a cheap-when-passing, rich-when-failing team default for debugging artifacts?
- [ ] A) `--video on --tracing on --screenshot on` for every test
- [ ] B) `--slowmo 1000 --headed` in `addopts`
- [ ] C) `--output test-results` only
- [ ] D) `--tracing retain-on-failure` plus `--screenshot only-on-failure`

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** D) `--tracing retain-on-failure` plus `--screenshot only-on-failure`

**Explanation:** Retaining artifacts only on failure costs little when everything passes and gives plenty of evidence when something breaks.

- **Why others are wrong:**
  - A) Keeping everything is for investigating something odd, and it is not cheap.
  - B) Slow motion and headed mode are local debugging aids and would break or slow CI.
  - C) `--output` only changes the artifact folder; it does not capture artifacts.
</details>

---

### 17. [True/False] True or False: It is a good idea to put `--headed` in `addopts` in `pytest.ini`, because it helps everyone see what the tests do, including on the CI server.
- [ ] True
- [ ] False

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** False

**Explanation:** CI servers usually have no display, so `--headed` in `addopts` can break CI; keep defaults headless and add `--headed` only locally.

</details>

---

### 18. [MCQ] In `conftest.py` you override `browser_context_args` and write `return {"viewport": {"width": 1280, "height": 720}}`. What is the problem?
- [ ] A) A fixture named `browser_context_args` cannot be overridden
- [ ] B) The viewport key must be written as `window_size`
- [ ] C) You lose the plugin's default context options because the original dictionary was not spread with `**browser_context_args`
- [ ] D) It will run only in Chromium

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** C) You lose the plugin's default context options because the original dictionary was not spread with `**browser_context_args`

**Explanation:** Start from the plugin's dictionary (`{**browser_context_args, ...}`) and then add or override keys.

- **Why others are wrong:**
  - A) The lesson shows exactly how to override it in `conftest.py`.
  - B) The lesson uses `viewport` as the key.
  - D) Context options are not tied to a single browser.
</details>

---

### 19. [MCQ] What is needed to run tests in parallel with `pytest -n auto`?
- [ ] A) The general PyTest plugin `pytest-xdist` (installed with pip)
- [ ] B) Playwright's built-in `--parallel` flag
- [ ] C) The `pytest-rerunfailures` plugin
- [ ] D) Nothing; PyTest runs in parallel by default

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** A) The general PyTest plugin `pytest-xdist` (installed with pip)

**Explanation:** `pytest-xdist` provides `-n`; `-n auto` starts one worker per CPU core. Tests must not share external state.

- **Why others are wrong:**
  - B) The lesson does not describe a Playwright `--parallel` flag; parallelism comes from xdist.
  - C) `pytest-rerunfailures` re-runs failing tests; it does not parallelize.
  - D) PyTest runs tests serially unless you add a plugin such as xdist.
</details>

---

### 20. [MCQ] A test only passes when you use `pytest --reruns 3`. What does the lesson say this means?
- [ ] A) The test is healthy because it eventually passes
- [ ] B) The test is flaky; retries are a safety net and a signal, so find the root cause (often bad waits or shared state)
- [ ] C) You should raise `--reruns` to 10 to be safe
- [ ] D) You should switch to `--slowmo` in CI

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** B) The test is flaky; retries are a safety net and a signal, so find the root cause (often bad waits or shared state)

**Explanation:** Retries come from `pytest-rerunfailures`; they must not be used to hide flakiness.

- **Why others are wrong:**
  - A) A test that passes only on retry is flaky and should be investigated.
  - C) More retries just hide the problem further.
  - D) `--slowmo` is a debugging aid and should not be used in CI.
</details>

---

### 21. [True/False] True or False: If `pytest.ini` has `addopts = --tracing retain-on-failure` and you run `pytest --headed`, the `--headed` flag still works.
- [ ] True
- [ ] False

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** True

**Explanation:** `addopts` adds options to every run, and a command-line option given at run time still works (it overrides the ini value where they conflict).

</details>

---

## Part 3: Auto-Waiting and Synchronization

### 22. [MCQ] What is a "race condition" in UI testing?
- [ ] A) Two browsers racing to open the same URL
- [ ] B) A test that is always slower than the application
- [ ] C) The script runs faster than the application, so the test checks before the page is ready; sometimes it wins and sometimes it loses
- [ ] D) A failure caused by a typo in a locator

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** C) The script runs faster than the application, so the test checks before the page is ready; sometimes it wins and sometimes it loses

**Explanation:** A script that clicks and then immediately looks for a result races the server and JavaScript; the outcome varies, which is flakiness.

- **Why others are wrong:**
  - A) The lesson defines it as a race between test and application, not between browsers.
  - B) The problem is the test being too fast, not too slow.
  - D) A typo fails every time; a race fails only sometimes.
</details>

---

### 23. [MCQ] Before performing `click()`, which set of actionability checks does Playwright wait for?
- [ ] A) Visible, stable, receives events and enabled
- [ ] B) Visible and editable only
- [ ] C) Stable and editable only
- [ ] D) No checks; `click()` fires immediately

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** A) Visible, stable, receives events and enabled

**Explanation:** According to the table, `click()` needs visible, stable, receives events and enabled (editable is not required).

- **Why others are wrong:**
  - B) Editable applies to `fill()`, and `click()` needs more than visibility.
  - C) Editable is not one of the click checks, and visible is required.
  - D) Auto-waiting is exactly the checks performed before actions.
</details>

---

### 24. [True/False] True or False: `hover()` waits for the element to be enabled before moving the mouse over it.
- [ ] True
- [ ] False

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** False

**Explanation:** In the actionability table, `hover()` requires visible, stable and receives events, but not enabled.

</details>

---

### 25. [MCQ] What does the default 5-second `expect()` timeout mean?
- [ ] A) Every `expect()` always waits the full 5 seconds
- [ ] B) It is a ceiling: the test continues the moment the assertion passes, so a page ready in 200 ms costs about 200 ms
- [ ] C) `expect()` fails if the page takes longer than 5 seconds to load
- [ ] D) It is the delay inserted before each click

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** B) It is a ceiling: the test continues the moment the assertion passes, so a page ready in 200 ms costs about 200 ms

**Explanation:** Timeouts are ceilings, not delays; Playwright re-checks and proceeds as soon as the condition holds.

- **Why others are wrong:**
  - A) That would be a fixed sleep, which is the anti-pattern.
  - C) It limits how long that assertion retries, not page load.
  - D) Click waiting is governed by the action timeout (30 seconds), and it is a ceiling too.
</details>

---

### 26. [Code Prediction] A button click schedules `<p id="msg">` to appear 500 ms later. What does this print?
```python
page.locator("#go").click()
first = page.locator("#msg").count()
expect(page.locator("#msg")).to_have_count(1)
print(first, page.locator("#msg").count())
```
- [ ] A) `1 1`
- [ ] B) `0 0`
- [ ] C) `1 0`
- [ ] D) `0 1`

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** D) `0 1`

**Explanation:** `count()` is a snapshot taken right after the click (the paragraph is not there yet). The `expect` retries until the element exists, so the later count is 1.

- **Why others are wrong:**
  - A) The snapshot count runs before the element appears, so it is not 1.
  - B) After the `expect` passes the element exists, so the second count is 1.
  - C) The element only gets added, never removed, so the order cannot be 1 then 0.
</details>

---

### 27. [MCQ] You want to verify the response of the API call triggered by typing in a search box. How should you use `expect_response`?
- [ ] A) Call `page.expect_response(...)` after the action finishes
- [ ] B) Call `time.sleep(2)` and then read the response
- [ ] C) Wrap the triggering action in `with page.expect_response(...)`, so the listener is set up before the action happens
- [ ] D) Use `page.wait_for_function` with the response status

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** C) Wrap the triggering action in `with page.expect_response(...)`, so the listener is set up before the action happens

**Explanation:** The `with` block starts listening first, then runs the action; creating the listener afterwards could miss a fast response.

- **Why others are wrong:**
  - A) A response that already arrived may be missed; this is a listed common mistake.
  - B) A fixed sleep is the anti-pattern the lesson warns against.
  - D) `wait_for_function` waits for a JavaScript condition and is a last-resort tool, not the way to catch a network response.
</details>

---

### 28. [MCQ] Why does the lesson discourage using `wait_for_load_state("networkidle")` as the default readiness check?
- [ ] A) It only works in Firefox
- [ ] B) It waits for exactly 5 seconds every time
- [ ] C) It is deprecated and removed from Playwright
- [ ] D) Modern pages (analytics, polling, websockets) may never be idle or may be idle before content renders; assert on the element the user cares about instead

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** D) Modern pages (analytics, polling, websockets) may never be idle or may be idle before content renders; assert on the element the user cares about instead

**Explanation:** `networkidle` means no network connections for at least 500 ms, which is not a reliable sign that the page is ready.

- **Why others are wrong:**
  - A) It is not browser-specific.
  - B) It is based on network activity, not a fixed 5 seconds.
  - C) It is not removed; Playwright's documentation just discourages relying on it.
</details>

---

### 29. [Code Prediction] What do the two `print` calls output (the element does not exist; the text is wrong)?
```python
page.set_content("<p>Hello</p>")
try:
    page.locator("#missing").click(timeout=500)
except Exception as e:
    print(type(e).__name__)
try:
    expect(page.locator("p")).to_have_text("Bye", timeout=500)
except Exception as e:
    print(type(e).__name__)
```
- [ ] A) `TimeoutError` then `AssertionError`
- [ ] B) `AssertionError` then `TimeoutError`
- [ ] C) `TimeoutError` then `TimeoutError`
- [ ] D) Nothing is printed because Playwright never raises errors

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** A) `TimeoutError` then `AssertionError`

**Explanation:** A failed action raises a `TimeoutError` ("waiting for locator" in the call log), while a failed `expect` raises an `AssertionError` showing expected and actual values.

- **Why others are wrong:**
  - B) The order is reversed: the action fails with `TimeoutError`, the assertion with `AssertionError`.
  - C) The `expect` failure is an `AssertionError`, as the lesson's example shows.
  - D) Both failures raise errors; they are caught here and their type names printed.
</details>

---

### 30. [MCQ] A failing click shows `Timeout 30000ms exceeded.` and a call log that ends with `waiting for locator("#login-buton")`. What is the most likely cause?
- [ ] A) An overlay is intercepting pointer events
- [ ] B) A typo in the selector, so the element never appeared
- [ ] C) The element is disabled
- [ ] D) The element is still animating

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** B) A typo in the selector, so the element never appeared

**Explanation:** The call log says Playwright was still waiting for the locator, meaning no matching element was found.

- **Why others are wrong:**
  - A) That cause would show `<div ...> intercepts pointer events` in the log.
  - C) A disabled element would show `element is not enabled`.
  - D) Animation would show `waiting for element to be stable`.
</details>

---

### 31. [MCQ] A test uses `page.locator("#x").click(timeout=5)` hoping for a 5-second limit. What actually happens?
- [ ] A) The limit is 5 milliseconds, because all Playwright timeouts are in milliseconds; use `5_000` for 5 seconds
- [ ] B) It waits 5 seconds as intended
- [ ] C) It waits 5 minutes
- [ ] D) Playwright rejects the value with a syntax error

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** A) The limit is 5 milliseconds, because all Playwright timeouts are in milliseconds; use `5_000` for 5 seconds

**Explanation:** Timeouts are in milliseconds, and Python's underscore syntax such as `15_000` keeps them readable.

- **Why others are wrong:**
  - B) That is the common mistake: 5 is 5 ms.
  - C) The unit is milliseconds, not minutes.
  - D) `timeout=5` is a valid number, just a tiny one.
</details>

---

### 32. [Fill-in-the-Blank] To wait until a spinner disappears, use `spinner.wait_for(state="______")`.
Your answer: `________`

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** `hidden`

**Explanation:** Valid states are `attached`, `detached`, `visible` and `hidden`; `expect(spinner).to_be_hidden()` often reads better and does the same job.

</details>

---

### 33. [MCQ] Which is the web-first (retrying) equivalent of the snapshot call `page.title()`?
- [ ] A) `expect(page).to_have_url(...)`
- [ ] B) `page.wait_for_timeout(...)`
- [ ] C) `expect(page).to_have_title(...)`
- [ ] D) `assert page.title() == ...`

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** C) `expect(page).to_have_title(...)`

**Explanation:** The lesson pairs snapshot methods with retrying assertions: `page.title()` goes with `expect(page).to_have_title(...)`, and `page.url` with `to_have_url`.

- **Why others are wrong:**
  - A) `to_have_url` is the equivalent of `page.url`, not of the title.
  - B) `wait_for_timeout` is a hard pause for debugging only, not an assertion.
  - D) A plain `assert` on a snapshot checks once with no retry.
</details>

---

## Part 4: Built-in Locators

### 34. [MCQ] According to Playwright's recommended priority, which locator should you try first?
- [ ] A) `get_by_test_id()`
- [ ] B) `page.locator()` with CSS
- [ ] C) `get_by_title()`
- [ ] D) `get_by_role()`

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** D) `get_by_role()`

**Explanation:** The order is role, label, placeholder, text, alt text, title, test id, then CSS/XPath as a last resort.

- **Why others are wrong:**
  - A) Test id is the seventh choice, used when nothing user-facing is stable.
  - B) CSS/XPath is last on the list.
  - C) Title is sixth.
</details>

---

### 35. [MCQ] By default, how does `get_by_role("button", name="Sign in")` match the accessible name?
- [ ] A) As an exact, case-sensitive match
- [ ] B) As a case-insensitive substring match
- [ ] C) As a regular expression always
- [ ] D) As a prefix match only

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** B) As a case-insensitive substring match

**Explanation:** Substring matching makes tests less fragile to small wording changes; add `exact=True` for precision.

- **Why others are wrong:**
  - A) Exact, case-sensitive matching only happens with `exact=True`.
  - C) A regex is only used if you pass a compiled regex.
  - D) It matches anywhere in the name, not only at the start.
</details>

---

### 36. [Code Prediction] Given two buttons, `Sign in` and `Sign in with Google`, what does this print?
```python
page.set_content("<button>Sign in</button><button>Sign in with Google</button>")
a = page.get_by_role("button", name="Sign in").count()
b = page.get_by_role("button", name="Sign in", exact=True).count()
print(a, b)
```
- [ ] A) `1 1`
- [ ] B) `2 2`
- [ ] C) `1 2`
- [ ] D) `2 1`

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** D) `2 1`

**Explanation:** Without `exact=True` the name is a substring match, so both buttons match; with `exact=True` only the full name "Sign in" does.

- **Why others are wrong:**
  - A) The first locator matches both buttons, not one.
  - B) `exact=True` narrows to one button.
  - C) Exact matching cannot match more than the default.
</details>

---

### 37. [MCQ] What is the implicit ARIA role of a `<select>` element?
- [ ] A) `combobox`
- [ ] B) `listbox`
- [ ] C) `textbox`
- [ ] D) `menu`

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** A) `combobox`

**Explanation:** From the role table: `<select>` maps to `combobox`, `<input type="text">` to `textbox`, and `<a href>` to `link`.

- **Why others are wrong:**
  - B) The lesson maps `<select>` to `combobox`.
  - C) `textbox` is the role of text and email inputs.
  - D) `menu` is not the role of a `<select>` in the lesson's table.
</details>

---

### 38. [Code Prediction] What does this print? (One labelled input and one input with only a placeholder.)
```python
page.set_content('''
<label for="a">Email</label><input id="a" placeholder="you@x.com">
<input id="b" placeholder="Email">''')
print(page.get_by_label("Email").get_attribute("id"),
      page.get_by_placeholder("Email").get_attribute("id"))
```
- [ ] A) `b a`
- [ ] B) `a a`
- [ ] C) `a b`
- [ ] D) `b b`

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** C) `a b`

**Explanation:** `get_by_label` uses the linked label text (input `a`), while `get_by_placeholder` uses the placeholder attribute (input `b`); label and placeholder are different attributes.

- **Why others are wrong:**
  - A) The label is linked to `a`, and the placeholder `Email` belongs to `b`; the order is not reversed.
  - B) The placeholder `Email` is on input `b`, not `a`.
  - D) `get_by_label` does not match placeholders, so it cannot return `b`.
</details>

---

### 39. [MCQ] SauceDemo marks elements with `data-test="login-button"`. How do you make `get_by_test_id("login-button")` work?
- [ ] A) Nothing; `get_by_test_id` always reads `data-test`
- [ ] B) Call `playwright.selectors.set_test_id_attribute("data-test")` once, in a session-level fixture
- [ ] C) Pass `data-test` as a second argument on every call
- [ ] D) Set the attribute inside each test after creating the locators

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** B) Call `playwright.selectors.set_test_id_attribute("data-test")` once, in a session-level fixture

**Explanation:** By default Playwright looks for `data-testid`; configure another attribute once (for example in `conftest.py`).

- **Why others are wrong:**
  - A) The default attribute is `data-testid`.
  - C) The lesson configures the attribute once, not per call.
  - D) Setting it after locators exist is a listed common mistake.
</details>

---

### 40. [Fill-in-the-Blank] By default, `get_by_test_id()` looks for the attribute `________`.
Your answer: `________`

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** `data-testid`

**Explanation:** Applications that use another attribute (like SauceDemo's `data-test`) require `set_test_id_attribute`.

</details>

---

### 41. [MCQ] A trainee uses `get_by_role("textbox", name="Password")` and finds nothing. What does the lesson suggest?
- [ ] A) Add `exact=True`
- [ ] B) Use `get_by_role("password")`
- [ ] C) Use `time.sleep()` before the locator
- [ ] D) Password inputs do not expose the `textbox` role, so use `get_by_label` or `get_by_placeholder`

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** D) Password inputs do not expose the `textbox` role, so use `get_by_label` or `get_by_placeholder`

**Explanation:** This is a listed common mistake; label or placeholder locators work for password fields.

- **Why others are wrong:**
  - A) `exact` does not change the role of the element.
  - B) `password` is not a role in the lesson's role table.
  - C) Waiting does not change the role an element exposes.
</details>

---

### 42. [Code Prediction] What does this print for the toggle-button and heading HTML?
```python
page.set_content('''
<button aria-pressed="true">Bold</button>
<button aria-pressed="false">Italic</button>
<button disabled>Save</button>
<h2>Section</h2><h3>Sub-section</h3>''')
print(page.get_by_role("button", name="Bold", pressed=True).count(),
      page.get_by_role("button", name="Italic", pressed=True).count(),
      page.get_by_role("button", disabled=True).count(),
      page.get_by_role("heading", level=3).count())
```
- [ ] A) `1 0 1 1`
- [ ] B) `1 1 1 1`
- [ ] C) `1 0 0 2`
- [ ] D) `0 0 1 1`

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** A) `1 0 1 1`

**Explanation:** Only Bold is pressed; Italic has `aria-pressed="false"`; only Save is disabled; only the `<h3>` has level 3.

- **Why others are wrong:**
  - B) Italic is not pressed, so its count is 0.
  - C) Only Save is disabled, and `level=3` matches just one heading.
  - D) Bold is pressed, so the first count is 1, not 0.
</details>

---

### 43. [Fill-in-the-Blank] `get_by_role("button", name="Sign in", ____=True)` matches only the full, case-sensitive name "Sign in", not "Sign in with Google".
Your answer: `________`

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** `exact`

**Explanation:** `exact=True` makes the `name` match the whole string, case-sensitively.

</details>

---

### 44. [True/False] True or False: A failing `get_by_role("button", name="Save")` can sometimes reveal a real accessibility defect, such as an icon-only button with no accessible name.
- [ ] True
- [ ] False

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** True

**Explanation:** Role/name locators use the browser's accessibility tree, so a missing role or label can point to a defect worth reporting.

</details>

---

## Part 5: Filtering and Chaining Locators

### 45. [MCQ] `page.get_by_role("button", name="Add to cart").click()` raises `strict mode violation ... resolved to 6 elements`. What is the recommended response?
- [ ] A) Add `.first` everywhere so the error disappears
- [ ] B) Increase the action timeout to 60 seconds
- [ ] C) Make the locator more specific, for example filter to the product card and chain the button inside it
- [ ] D) Replace `click()` with `time.sleep()`

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** C) Make the locator more specific, for example filter to the product card and chain the button inside it

**Explanation:** Strict mode prevents clicking the wrong element; fix it by being specific (`filter(has_text=...)` then chain), not by silencing it.

- **Why others are wrong:**
  - A) Using `.first` to bypass strict mode is a listed common mistake; the order can change.
  - B) A timeout does not change how many elements match.
  - D) Sleeping does not help; the locator is ambiguous.
</details>

---

### 46. [Code Prediction] A table has rows Jane/Active, Raj/Inactive and Mei/Active (plus a header row). What does this print?
```python
rows = page.get_by_role("row")
a = rows.filter(has_text="Active").count()
b = rows.filter(has_text="Active").filter(has_not_text="Inactive").count()
print(a, b)
```
- [ ] A) `2 2`
- [ ] B) `3 2`
- [ ] C) `3 3`
- [ ] D) `2 1`

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** B) `3 2`

**Explanation:** `has_text` is a case-insensitive substring match, so "Active" also matches "Inactive" (3 rows); excluding "Inactive" leaves 2.

- **Why others are wrong:**
  - A) The Inactive row also contains the substring "active", so the first count is 3.
  - C) The second filter removes Raj's row, so the second count is 2.
  - D) Jane and Mei remain after the filter, which is 2 rows, not 1.
</details>

---

### 47. [MCQ] What is the difference between `filter(has=...)` and `and_()`?
- [ ] A) `has=` tests a descendant inside the element, while `and_()` requires both locators to match the same element
- [ ] B) They are identical
- [ ] C) `has=` matches either locator, while `and_()` matches a descendant
- [ ] D) `and_()` searches the whole page and ignores the outer locator

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** A) `has=` tests a descendant inside the element, while `and_()` requires both locators to match the same element

**Explanation:** Confusing `has=` (descendant) with `and_()` (same element) is a listed common mistake.

- **Why others are wrong:**
  - B) They answer different questions.
  - C) `or_()` is the one that matches either condition.
  - D) `and_()` combines two locators on the same element.
</details>

---

### 48. [Code Prediction] For a page with two buttons (`Save` with class `btn-primary`, and `Cancel`), what does this print?
```python
both = page.get_by_role("button").and_(page.locator(".btn-primary")).count()
either = page.get_by_role("button", name="Save").or_(page.get_by_role("button", name="Cancel")).count()
print(both, either)
```
- [ ] A) `2 1`
- [ ] B) `1 1`
- [ ] C) `1 2`
- [ ] D) `2 2`

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** C) `1 2`

**Explanation:** `and_` keeps only elements matching both locators (just Save); `or_` matches either, so Save and Cancel are both found.

- **Why others are wrong:**
  - A) Only one button is both a button and `.btn-primary`.
  - B) `or_` matches both buttons, so its count is 2.
  - D) `and_` narrows to the primary button only.
</details>

---

### 49. [MCQ] Why does the lesson use `.first` in `expect(new_email.or_(dialog).first).to_be_visible()`?
- [ ] A) `or_()` only works when followed by `.first`
- [ ] B) `.first` makes the assertion wait longer
- [ ] C) `.first` converts the locator into a CSS selector
- [ ] D) If both elements appear, the combined locator matches two elements and strict mode would complain about a single-element check

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** D) If both elements appear, the combined locator matches two elements and strict mode would complain about a single-element check

**Explanation:** `or_()` can match two elements; `.first` picks one so the visibility check is not ambiguous.

- **Why others are wrong:**
  - A) `or_()` works without it; `.first` handles the both-appear case.
  - B) `.first` does not change waiting time.
  - C) It stays a Playwright locator.
</details>

---

### 50. [Code Prediction] For `<ul><li>a</li><li>b</li><li>c</li><li>d</li></ul>`, what does this print?
```python
items = page.locator("li")
print(items.first.inner_text(), items.last.inner_text(),
      items.nth(1).inner_text(), items.nth(2).inner_text())
```
- [ ] A) `a d a b`
- [ ] B) `a d b c`
- [ ] C) `a d c d`
- [ ] D) `b c b c`

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** B) `a d b c`

**Explanation:** `nth()` is zero-based: `nth(0)` is the first element, so `nth(1)` is the second (b) and `nth(2)` the third (c).

- **Why others are wrong:**
  - A) `nth(1)` is the second item, not the first.
  - C) `nth(1)` is b and `nth(2)` is c, not c and d.
  - D) `first` is a and `last` is d.
</details>

---

### 51. [MCQ] When is selecting by position, such as `row.get_by_role("cell").nth(1)`, acceptable?
- [ ] A) Whenever the locator is hard to write
- [ ] B) Only inside a loop
- [ ] C) Never; `nth()` is deprecated
- [ ] D) When the position is part of the requirement or structure, such as a known column order in a table

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** D) When the position is part of the requirement or structure, such as a known column order in a table

**Explanation:** Position is a mistake when used only because you lack a better locator and the order can change; it is fine when position is guaranteed.

- **Why others are wrong:**
  - A) That is the mistake case, because sorting or new data can change the order.
  - B) Loops are not the criterion.
  - C) `nth()` is not deprecated; it is simply to be used carefully.
</details>

---

### 52. [MCQ] Why should you write `expect(names).to_have_count(6)` before calling `names.all_inner_texts()`?
- [ ] A) `all_inner_texts()` is a snapshot that does not wait for the list to load, so the count assertion confirms the list is ready first
- [ ] B) `all_inner_texts()` raises an error unless a count assertion exists
- [ ] C) `to_have_count` converts the list into strings
- [ ] D) It makes `all_inner_texts()` retry for 30 seconds

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** A) `all_inner_texts()` is a snapshot that does not wait for the list to load, so the count assertion confirms the list is ready first

**Explanation:** `count()`, `all()` and `all_inner_texts()` are snapshots; assert something that proves the page is ready, then collect data.

- **Why others are wrong:**
  - B) It does not raise an error; it just returns whatever is there at that moment.
  - C) `to_have_count` only asserts how many elements match.
  - D) The snapshot methods do not retry.
</details>

---

### 53. [Code Prediction] A list shows Zebra, Apple, Mango in that order. What does this print?
```python
texts = page.locator("li").all_inner_texts()
print(texts == sorted(texts))
```
- [ ] A) `True`
- [ ] B) `False`
- [ ] C) `['Apple', 'Mango', 'Zebra']`
- [ ] D) A `TimeoutError`

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** B) `False`

**Explanation:** The page order is Zebra, Apple, Mango, while `sorted(texts)` is Apple, Mango, Zebra, so the comparison is False; this is how the sorting check works.

- **Why others are wrong:**
  - A) The list is not alphabetically sorted.
  - C) The `print` shows the result of `==`, a boolean, not a list.
  - D) `all_inner_texts()` returns immediately with the current texts; no timeout is involved.
</details>

---

### 54. [MCQ] What does `expect(names).to_have_text(["Sauce Labs Backpack", "Sauce Labs Bike Light", ...])` assert when given a list?
- [ ] A) Only that the first text appears somewhere
- [ ] B) That each text appears in any order, without waiting
- [ ] C) The exact texts in order and the count, with retrying until true
- [ ] D) Only the number of elements

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** C) The exact texts in order and the count, with retrying until true

**Explanation:** A list passed to `to_have_text` asserts the texts in order and the count, and it waits, which is better than reading texts into Python.

- **Why others are wrong:**
  - A) It checks every item, not just the first.
  - B) Order matters, and the assertion retries.
  - D) It checks the texts as well as the count.
</details>

---

### 55. [Fill-in-the-Blank] To keep only elements that do NOT contain the word Backpack, write `.filter(________="Backpack")`.
Your answer: `________`

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** `has_not_text`

**Explanation:** `has_not_text` keeps elements without the text; `has_text` keeps those with it, and `has` / `has_not` filter by descendant locators.

</details>

---

## Part 6: The Playwright Inspector

### 56. [MCQ] What happens when you run `PWDEBUG=1 pytest -s tests/test_login.py`?
- [ ] A) The test runs headless at double speed
- [ ] B) Only failing tests are re-run with traces
- [ ] C) A video of the run is saved
- [ ] D) The browser runs headed, timeouts are disabled and the Inspector opens paused at the first Playwright action

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** D) The browser runs headed, timeouts are disabled and the Inspector opens paused at the first Playwright action

**Explanation:** `PWDEBUG=1` runs Playwright actions in debug mode; reset it afterwards or every later run opens the Inspector.

- **Why others are wrong:**
  - A) Debug mode is headed and interactive, not faster.
  - B) Re-running failures with traces is not what it does.
  - C) Videos belong to `--video`.
</details>

---

### 57. [MCQ] How does `page.pause()` behave?
- [ ] A) It sleeps for 30 seconds
- [ ] B) It stops execution and opens the Inspector in headed mode (or with `PWDEBUG=1`); in headless mode it is ignored
- [ ] C) It always opens the Inspector, even in headless CI
- [ ] D) It is equivalent to `time.sleep()`

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** B) It stops execution and opens the Inspector in headed mode (or with `PWDEBUG=1`); in headless mode it is ignored

**Explanation:** `page.pause()` is useful when the first steps are fine and the problem is later; remove it before committing.

- **Why others are wrong:**
  - A) It stops until you resume; it is not a timer.
  - C) In headless mode it is ignored, so a forgotten `pause()` will not hang CI.
  - D) It is not a fixed sleep; it hands control to you.
</details>

---

### 58. [True/False] True or False: A forgotten `page.pause()` in a test will hang the CI pipeline, which runs headless.
- [ ] True
- [ ] False

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** False

**Explanation:** In headless mode `page.pause()` is ignored, but you should still remove it before committing.

</details>

---

### 59. [MCQ] A test failed on the CI server and you cannot reproduce it locally. Which tool fits best?
- [ ] A) The Inspector, because it works after the run finishes
- [ ] B) `--slowmo`, because it records the CI run
- [ ] C) The Trace Viewer, because a trace produced on CI can be opened anywhere after the run
- [ ] D) `playwright open`, which replays CI traces

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** C) The Trace Viewer, because a trace produced on CI can be opened anywhere after the run

**Explanation:** The Inspector is for live, local debugging; the Trace Viewer is post-mortem and works with traces from anywhere.

- **Why others are wrong:**
  - A) The Inspector works during a run, on your machine.
  - B) `--slowmo` only delays operations; it records nothing.
  - D) `playwright open` just opens a browser to explore.
</details>

---

### 60. [True/False] True or False: `PWDEBUG=1` disables timeouts, so a test that passes in debug mode may still time out in a normal run.
- [ ] True
- [ ] False

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** True

**Explanation:** Debug mode disables timeouts so you can think as long as you like; always re-run normally afterwards.

</details>

---

### 61. [Fill-in-the-Blank] Before running the Inspector in macOS/Linux you set the environment variable `______=1`.
Your answer: `________`

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** `PWDEBUG`

**Explanation:** `PWDEBUG=1` starts debug mode. Unset it afterwards so later runs do not keep pausing.

</details>

---

### 62. [MCQ] In the browser's DevTools console (debug mode), which call matches the Playwright console API?
- [ ] A) `playwright.getByRole('button', { name: 'Login' })`
- [ ] B) `playwright.get_by_role("button", name="Login")`
- [ ] C) `page.get_by_role("button", name="Login")`
- [ ] D) `pytest.getByRole('button')`

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** A) `playwright.getByRole('button', { name: 'Login' })`

**Explanation:** The console uses JavaScript syntax such as `getByRole`; translate to Python's `get_by_role` in your tests.

- **Why others are wrong:**
  - B) Python names are a listed mistake in the console.
  - C) `page` is the Python object, not the console API.
  - D) `pytest` is not part of the console API.
</details>

---

## Part 7: Record and Playback (Codegen)

### 63. [MCQ] Which command records a test as a PyTest function that uses the `page` fixture and saves it to a file?
- [ ] A) `playwright codegen https://www.saucedemo.com --save test_recorded.py`
- [ ] B) `pytest --codegen test_recorded.py`
- [ ] C) `playwright record --pytest test_recorded.py`
- [ ] D) `playwright codegen --target python-pytest -o test_recorded.py https://www.saucedemo.com`

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** D) `playwright codegen --target python-pytest -o test_recorded.py https://www.saucedemo.com`

**Explanation:** `--target python-pytest` generates PyTest style code and `-o` saves it to a file.

- **Why others are wrong:**
  - A) The option for saving code is `-o/--output`, not `--save`.
  - B) Codegen is a Playwright CLI command, not a PyTest option.
  - C) The command is `playwright codegen`, not `playwright record`.
</details>

---

### 64. [Fill-in-the-Blank] To save the cookies and local storage after logging in during codegen, run `playwright codegen --________-storage=auth.json <url>`.
Your answer: `________`

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** `save`

**Explanation:** `--save-storage` writes the login state to a JSON file and `--load-storage` starts a session with it; keep it out of git.

</details>

---

### 65. [MCQ] You record a flow and replay it: it passes, but the file contains no `expect()`. How should it be described?
- [ ] A) A complete test, because it passed
- [ ] B) A smoke suite
- [ ] C) A script, not a test, because a test needs a verdict (assertions)
- [ ] D) An async test

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** C) A script, not a test, because a test needs a verdict (assertions)

**Explanation:** A recording with no assertions can pass even when the application is broken.

- **Why others are wrong:**
  - A) A green recording does not equal a good test.
  - B) Smoke is a marker you add; nothing here makes it a suite.
  - D) Nothing in the code makes it async; `--target python-pytest` generates sync code.
</details>

---

### 66. [MCQ] Which is the first item on the refactoring checklist for a raw recording?
- [ ] A) Rename the test to describe behavior, such as `test_user_can_add_backpack_to_cart`
- [ ] B) Commit it so the team can see it
- [ ] C) Add `time.sleep(2)` after each step
- [ ] D) Switch all locators to XPath

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** A) Rename the test to describe behavior, such as `test_user_can_add_backpack_to_cart`

**Explanation:** The checklist: rename, remove noise, improve locators, add assertions, extract fixtures, extract data, add markers/docstring, run repeatedly.

- **Why others are wrong:**
  - B) Committing raw recordings is a listed common mistake.
  - C) Sleeps are an anti-pattern.
  - D) XPath is the last resort; you improve locators towards role, label and filtered chains.
</details>

---

### 67. [MCQ] While debugging with `page.pause()`, how can you extend an existing test by recording?
- [ ] A) Re-run `playwright codegen` and overwrite the file
- [ ] B) Press Record in the Inspector; your actions are inserted at the cursor position in the code, and you copy them into the test
- [ ] C) Record only works before any test code exists
- [ ] D) Press Step over repeatedly until the code is written

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** B) Press Record in the Inspector; your actions are inserted at the cursor position in the code, and you copy them into the test

**Explanation:** The Record toggle inserts actions at the cursor, so you can extend a test from the point where it pauses.

- **Why others are wrong:**
  - A) That would overwrite the output file; the lesson warns that `-o` on an existing path overwrites it.
  - C) The Record button works while paused inside an existing test.
  - D) Step over executes existing calls; it does not generate code.
</details>

---

### 68. [True/False] True or False: Playwright's codegen stores recordings in a proprietary format that can only be replayed inside the Playwright tool.
- [ ] True
- [ ] False

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** False

**Explanation:** Codegen generates real, editable Python code; playback is just running it with PyTest.

</details>

---

### 69. [True/False] True or False: It is fine to commit `auth.json` (saved login state) as long as the tests use it.
- [ ] True
- [ ] False

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** False

**Explanation:** `auth.json` contains session tokens; add it to `.gitignore` and never commit it.

</details>

---

### 70. [MCQ] Which is a poor use of record and playback?
- [ ] A) Exploring a new page to discover locators
- [ ] B) Creating a first draft of a long form flow
- [ ] C) Building an entire regression suite purely from raw recordings
- [ ] D) Attaching a runnable reproduction to a bug report

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** C) Building an entire regression suite purely from raw recordings

**Explanation:** Recordings are drafts; teams that paste raw recordings end up with duplicated, brittle tests.

- **Why others are wrong:**
  - A) Quick exploration and locator discovery is a good use.
  - B) A first draft is a good use; refactor afterwards.
  - D) Reproducing a bug quickly is a listed good use.
</details>

---

## Topic Coverage

| Topic | Question numbers |
|-------|------------------|
| Creating Playwright tests | 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11 (11) |
| Playwright test runner | 12, 13, 14, 15, 16, 17, 18, 19, 20, 21 (10) |
| Auto-waiting and synchronization | 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32, 33 (12) |
| Built-in locators | 34, 35, 36, 37, 38, 39, 40, 41, 42, 43, 44 (11) |
| Filtering and chaining locators | 45, 46, 47, 48, 49, 50, 51, 52, 53, 54, 55 (11) |
| Playwright Inspector | 56, 57, 58, 59, 60, 61, 62 (7) |
| Record and playback | 63, 64, 65, 66, 67, 68, 69, 70 (8) |

**Total questions:** 70
