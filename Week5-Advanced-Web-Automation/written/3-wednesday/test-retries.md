# Test Retries

## Learning Objectives

By the end of this lesson you will be able to:

- Define a **flaky test** and explain the common root causes in UI automation (timing, shared state, test data, environment, network, third-party scripts).
- Explain what a **retry** (a "rerun") is, what it can and cannot fix, and the risks of using it as a crutch.
- Install and use **`pytest-rerunfailures`**: the `--reruns` and `--reruns-delay` command-line options, the `@pytest.mark.flaky` marker, and the `--only-rerun` / `--rerun-except` filters.
- Configure retries in `pytest.ini` so they apply consistently locally and in CI.
- Understand how fixtures, Playwright artifacts (traces, screenshots, videos), and reports behave when a test is re-run.
- Detect, in code, whether the current run is a retry (`execution_count`), and use that to capture extra diagnostics on retries.
- Apply **targeted retries** at smaller levels (a single action or a polling loop) when re-running the whole test is wasteful.
- Build a **flaky test management process**: identify, quarantine, fix, and track.
- Avoid the biggest anti-pattern: using retries to hide real defects or to paper over bad waits.

---

## Why This Matters

Anyone who has maintained a UI test suite has seen this: the suite fails overnight; you re-run it in the morning and it passes. Nothing in the application changed. That is a **flaky test**, a test that sometimes passes and sometimes fails on the *same code*. Flakiness is poison for a test suite. Once developers see random red builds, they stop trusting the results; they start re-running pipelines "just in case", and genuine defects hide among the noise.

This week's epic is about structuring Playwright tests so they are reliable and maintainable. You have covered fixtures, hooks, the Page Object Model, and data-driven tests. Retries are the **last line of defence** in that structure: a pragmatic mechanism that gives a test a second (or third) chance when it fails for a transient reason, so that a single network hiccup does not fail a 40-minute pipeline.

But retries are also dangerous. A careless team that turns on `--reruns 5` globally can end up with a suite that "always passes" while it silently contains broken behaviour, or one that takes three times longer because everything is retried. In a professional environment you must be able to say, with evidence, *why* a retry exists and *what is being done about the underlying cause*.

This matters for **Project 1 - QE Foundations** too. A UI test suite that runs reliably in CI is a stronger portfolio piece than one that works "most of the time on my laptop". Your Project 1 reviewer is likely to run your suite on a different machine; sensible retry configuration, documented in your README, protects you from environmental flakiness while demonstrating professional judgement. And you will see retries interact with the reporting you build in the next lesson: a test that passed on the second attempt must be visible in the report as "rerun", not hidden.

---

## The Concept

### 1. What is a flaky test?

A **flaky test** produces different results (pass/fail) for the same code and the same test, with no intentional change. The word comes from "flaky" in the sense of unreliable.

It is crucial to understand that flakiness always has a **cause**; it is never "random magic". Typical causes in browser automation:

| Category | Example | Typical fix |
|---|---|---|
| **Timing / synchronisation** | Clicking before the element is ready; reading text before it updates; `time.sleep(2)` that is sometimes too short | Use Playwright's auto-waiting actions and web-first `expect(...)` assertions; wait for the specific condition (`wait_for_url`, `expect(...).to_be_visible()`) |
| **Shared state** | Test B relies on a cart left over from Test A; tests run in a different order | Isolate with fixtures (new context per test), clean up with teardown |
| **Test data** | Two parallel tests use the same user account; a record is already "taken" | Create unique data per test; use separate accounts |
| **Environment** | Staging server slow or restarting; CI machine under load | Retries for infrastructure blips; increase timeouts; dedicate resources |
| **Network / third parties** | An analytics script or ad iframe fails to load and shifts the layout | Block or mock third-party calls (`page.route(...)`) |
| **Animations / overlays** | A cookie banner or loading spinner covers the target | Wait for overlay to disappear; disable animations in test environments |
| **Non-determinism in the app** | Random ordering, time-dependent values, A/B experiments | Control via test hooks, seeded data, feature flags |
| **Browser differences** | A bug only appears in WebKit under certain timing | Reproduce with `--browser webkit --headed --slowmo 500`; fix root cause |

On SauceDemo, `performance_glitch_user` is a built-in example: login deliberately takes a few seconds longer. A test written with a hard `sleep(1)` after login is flaky for this user; a test using `expect(page).to_have_url(...)` (which retries up to the timeout) is not. That is the first, best "retry" mechanism: **Playwright's own built-in auto-waiting and web-first assertions**. Always exhaust those before reaching for test-level retries.

### 2. Layers of retry (know which one you are using)

Retries can occur at several layers, from the smallest scope to the largest:

1. **Inside Playwright actions:** `locator.click()` auto-waits for the element to be visible, stable, enabled, and receiving events; it retries internally until the timeout. You get this for free.
2. **Inside web-first assertions:** `expect(locator).to_have_text("x")` re-checks repeatedly until it passes or times out (default 5 seconds). Also free.
3. **Inside your own helper:** a small polling or "retry this action" function for a specific unstable step (Section 8).
4. **Whole-test retries:** re-running the entire test when it fails. That is what `pytest-rerunfailures` provides and what this lesson focuses on.
5. **Pipeline-level retries:** the CI system re-running a failed job. Avoid relying on this; it is blunt and hides the cause.

The principle: **retry at the lowest layer that fixes the problem.** Whole-test retries are the highest-cost layer because they repeat everything (login, navigation, all steps).

> **Cross-tool note.** The Playwright Test runner for JavaScript has a built-in `retries` setting, and other tools such as Cypress also offer test retries (Cypress is covered in depth on Thursday). In Python, the standard mechanism is the pytest plug-in described here. The ideas (when to retry, risks, how to track flakiness) are identical.

### 3. Installing and first use of `pytest-rerunfailures`

```bash
pip install pytest-rerunfailures
```

The plug-in is auto-detected. Re-run failed tests up to 2 times:

```bash
pytest --reruns 2
```

What happens: when a test fails, pytest discards that attempt's result, tears down the test's fixtures, and **runs the test again from scratch**. If any attempt passes, the final result is *passed*, but the report records that reruns happened. If all attempts fail, the final result is *failed*. With `--reruns 2` there are at most **three attempts** (the first run plus two reruns).

Add a pause between attempts, which helps with transient infrastructure problems (a service restarting, rate limiting):

```bash
pytest --reruns 2 --reruns-delay 3     # wait 3 seconds before each rerun
```

Console output marks reruns with an `R` and a summary:

```
tests/test_login.py::test_login_works RR.                        [100%]
=========== 1 passed, 2 rerun in 14.32s ===========
```

Reading it: the test failed twice (`R`, `R`) and passed on the third attempt (`.`).

### 4. A deliberately flaky demonstration

To feel retries working, create a test whose result changes between runs. We will use a counter file so it is deterministic enough to teach with: it fails the first two attempts and passes the third.

```python
# tests/test_retry_demo.py
from pathlib import Path

COUNTER = Path("retry_counter.txt")


def test_passes_on_third_attempt():
    attempts = int(COUNTER.read_text()) if COUNTER.exists() else 0
    attempts += 1
    COUNTER.write_text(str(attempts))

    if attempts < 3:
        raise AssertionError(f"simulated transient failure on attempt {attempts}")

    COUNTER.unlink()          # clean up so the demo can be repeated
```

Line by line:

- `Path("retry_counter.txt")` represents a file in the current directory that survives between attempts (variables in the test would be reset).
- `int(COUNTER.read_text()) if COUNTER.exists() else 0` reads the previous attempt number if the file exists, else starts at zero. This is a conditional expression.
- `COUNTER.write_text(str(attempts))` stores the new count; `write_text` needs a string.
- `if attempts < 3: raise AssertionError(...)` fails the first two attempts.
- `COUNTER.unlink()` deletes the file after success so the next demo starts fresh.

Run `pytest tests/test_retry_demo.py --reruns 2 -v` and observe `RERUN` entries followed by `PASSED`. Run with `--reruns 1` and observe the final failure. (If a demo run is interrupted, delete `retry_counter.txt` manually.)

### 5. The `@pytest.mark.flaky` marker: per-test control

The command-line option applies to every test. Often you want retries only for specific, known-unstable tests, or different counts for different tests. The plug-in provides a marker (named `flaky`):

```python
import pytest


@pytest.mark.flaky(reruns=3, reruns_delay=2)
def test_checkout_with_slow_payment_widget(inventory_page):
    ...
```

- `reruns=3` allows three reruns (four attempts in total).
- `reruns_delay=2` waits two seconds between attempts.
- A marker on a test overrides the command-line value for that test. A marker on a class or module (`pytestmark = pytest.mark.flaky(reruns=1)`) applies to every test inside.
- You can apply it with a condition: `@pytest.mark.flaky(reruns=2, condition=sys.platform.startswith("win"))` retries only when the condition is true.

**Important design point:** Tag known flaky tests with an *accompanying comment and defect id*:

```python
# BUG-902: payment iframe sometimes loads late in CI. Remove when fixed.
@pytest.mark.flaky(reruns=2, reruns_delay=1)
def test_pay_with_card(...):
    ...
```

An unexplained `flaky` marker is technical debt without an owner.

### 6. Filtering *which* failures are retried

Not every failure deserves a retry. An assertion failure that says "expected Products, got Cart" is likely a real defect; a `TimeoutError` or a connection reset is more likely transient. The plug-in lets you choose by exception text.

```bash
# Retry only when the failure text matches one of these regular expressions
pytest --reruns 2 --only-rerun "TimeoutError" --only-rerun "net::ERR_"

# Retry everything except assertion failures
pytest --reruns 2 --rerun-except AssertionError
```

- `--only-rerun REGEX` (repeatable): a failed test is rerun only if its error output matches at least one expression.
- `--rerun-except REGEX` (repeatable): a failed test is **not** rerun when the error output matches.
- The marker has equivalents: `@pytest.mark.flaky(reruns=2, only_rerun=["TimeoutError"])` and `rerun_except=[...]`.

A regular expression ("regex") is a pattern language for matching text; for our purposes a plain word such as `TimeoutError` matches exactly itself.

Playwright for Python raises `playwright._impl._errors.TimeoutError` (imported publicly as `playwright.sync_api.TimeoutError`) when an action times out; the plain word `TimeoutError` therefore matches. Assertion failures from `expect(...)` are `AssertionError`, and they also contain timeout information in their message, so choose your patterns by looking at *your* real failure outputs.

**Why filter?** Because retrying a deterministic failure just wastes time: three attempts at a genuinely broken login still fail three times, tripling the cost and delaying feedback. A tight filter keeps retries for failures that retrying might actually fix.

### 7. Configuration in `pytest.ini` (consistent everywhere)

Rather than remembering command-line flags, put defaults in the project config:

```ini
# pytest.ini
[pytest]
addopts = --reruns 1 --reruns-delay 1 --only-rerun TimeoutError --only-rerun "net::ERR_"
markers =
    smoke: quick checks
    regression: full coverage
```

- `addopts` lists options automatically added to every pytest command.
- Locally you can override: `pytest --reruns 0` runs with no retries, which is **how you should debug a failing test** (see best practices).
- A common pattern is *zero retries locally, a small number in CI*, set via a CI-specific command or environment variable (`PYTEST_ADDOPTS="--reruns 2"`), so developers see raw failures while the pipeline absorbs infrastructure noise.

### 8. What happens to fixtures, state, and Playwright artifacts on rerun?

Understanding this prevents confusing results.

- **Function-scoped fixtures** (like `page`, `context`, and your page-object fixtures) are torn down after the failed attempt and set up again for the rerun. That is *good*: each attempt starts with a brand-new browser context. This is why Playwright's context-per-test isolation and test retries fit together so well.
- **Higher-scoped fixtures** (session, module) are generally **not** recreated for a rerun of a test. (Class-scoped fixtures are re-set-up for reruns in recent plug-in versions, and this behaviour has differed between versions; check the plug-in's changelog if you depend on it.) Session fixtures that hold mutable state, such as a shared cart, can therefore carry stale state into the retry, another reason to keep mutable state function-scoped.
- **External state is not reset.** If the failed attempt created an order in the backend, the rerun creates another unless your teardown removed it. Make tests **idempotent** (safe to run twice) or clean up in fixtures with `yield`.
- **Playwright artifacts:** with `--tracing retain-on-failure`, `--screenshot only-on-failure`, or `--video retain-on-failure`, pytest-playwright produces artifacts per attempt, so you can compare a failed first attempt with the passing second. Artifacts are written to the output folder (`test-results/` by default, changeable with `--output`). If you want a trace for **every** attempt, including passing ones, use `--tracing on`. (Details in the Reporting lesson.)
- **Reports:** a rerun is a separate outcome in the log. In JUnit XML and pytest-html the earlier attempts appear as "rerun" entries and the final attempt as passed or failed. This is how flaky tests become *visible* rather than hidden.

### 9. Detecting a rerun inside the test

The plug-in records the attempt number on the test item as `execution_count` (1 for the first attempt, 2 for the first rerun, and so on). You can read it, for instance to collect extra diagnostics only when a retry happens.

```python
# conftest.py
import pytest


@pytest.fixture
def attempt(request) -> int:
    """1 on the first run, 2 on the first rerun, ..."""
    return getattr(request.node, "execution_count", 1)


@pytest.fixture(autouse=True)
def verbose_on_retry(page, attempt):
    if attempt > 1:
        page.on("console", lambda msg: print(f"[retry console:{msg.type}] {msg.text}"))
        page.on("requestfailed", lambda req: print(f"[retry network failed] {req.url}"))
    yield
```

Line by line:

- `getattr(request.node, "execution_count", 1)` safely reads the attribute; without the plug-in (or on the first attempt in some versions) it falls back to `1`. We use `getattr` with a default because the attribute may not exist when the plug-in is not active.
- `attempt > 1` means "this is a rerun".
- `page.on("console", handler)` and `page.on("requestfailed", handler)` register event listeners for browser console messages and failed network requests. `req.url` is the failed request's URL.
- The fixture is `autouse`, so it applies to every test, but it only prints on retries, so a normal run stays quiet. (Remember the caution from the Hooks lesson: an autouse fixture that requests `page` creates a page for all tests in scope. Keep this one in your UI tests' `conftest.py`.)

This pattern turns a retry from a blind second chance into **extra evidence**: the extra output tells you *why* the first attempt failed.

### 10. Retrying at a smaller scope: a targeted helper

Suppose one step is unstable (for example, a third-party widget that sometimes needs a second click). Re-running a 3-minute checkout test for that is wasteful. Write a narrow retry:

```python
# utils/retry.py
import time
from typing import Callable, TypeVar

T = TypeVar("T")


def retry(action: Callable[[], T], attempts: int = 3, delay: float = 0.5,
          exceptions: tuple = (Exception,)) -> T:
    """Call `action` up to `attempts` times, waiting `delay` seconds between tries."""
    last_error = None
    for attempt_number in range(1, attempts + 1):
        try:
            return action()
        except exceptions as error:
            last_error = error
            if attempt_number < attempts:
                time.sleep(delay)
    raise last_error
```

Usage:

```python
from playwright.sync_api import TimeoutError as PlaywrightTimeout
from utils.retry import retry

def open_payment_widget(page):
    retry(lambda: page.get_by_role("button", name="Pay now").click(timeout=2000),
          attempts=3, delay=1, exceptions=(PlaywrightTimeout,))
```

Line by line:

- `Callable[[], T]` is a type hint for "a function that takes no arguments and returns something of type `T`". `TypeVar` lets the return type of `retry` match the action's return type.
- `for attempt_number in range(1, attempts + 1)` loops 1, 2, 3.
- `try: return action()` calls the action; if it returns normally we are done.
- `except exceptions as error:` catches only the exception types listed, so genuine logic bugs (a `KeyError`) are not retried.
- `time.sleep(delay)` pauses *between attempts*. Using `sleep` here is acceptable: this is a deliberate back-off between retries, not a guess about when the page is ready.
- After the loop, `raise last_error` re-raises the final exception so the failure is not hidden.
- `click(timeout=2000)` shortens the single-attempt timeout (milliseconds), so each attempt fails fast.

Before writing a helper like this, check whether Playwright already offers the behaviour: `expect(...).to_be_visible()` retries; `locator.wait_for()` waits; `page.wait_for_function(...)` polls a condition; `expect.poll(...)` in some language bindings. Prefer built-ins.

### 11. Timeouts: the other half of the story

A retry is only useful if each attempt is given a *realistic* chance. If the environment is slow, an attempt may fail simply because 5 seconds was not enough. Playwright exposes timeouts at several levels:

```python
page.set_default_timeout(10_000)                  # actions, waits: 10 s
page.set_default_navigation_timeout(30_000)       # goto, reload, etc.: 30 s
locator.click(timeout=3_000)                      # just this action
expect(locator).to_be_visible(timeout=15_000)     # just this assertion
```

If an overall test is hanging, the `pytest-timeout` plug-in (`pytest --timeout 120`) fails the test after a total time limit; combined with reruns it prevents an endless hang. Note that a timeout on a hung browser may need a robust teardown; keep timeouts generous enough to avoid false failures.

### 12. Managing flaky tests as a process

Tools are only half the answer. Mature teams run a *lifecycle*:

1. **Detect.** Look for tests with "rerun" outcomes in reports; track the flake rate (percentage of runs needing a retry). Run suspects repeatedly to measure: a simple shell loop (`for i in {1..20}; do pytest tests/test_x.py -q; done`) or the `pytest-repeat` plug-in (`pytest --count=20`).
2. **Triage.** Is it the test (bad wait), the data, the environment, or a real intermittent product bug? A trace of the failed attempt answers this quickly.
3. **Quarantine** if needed. Mark the test (`@pytest.mark.quarantine`) and exclude it from the gating run (`-m "not quarantine"`), while a separate non-blocking job keeps running it, so it neither blocks releases nor disappears.
4. **Fix** the root cause: replace sleeps with web-first assertions, isolate data, stabilise the environment.
5. **Remove** the retry marker and quarantine once the test is stable for N consecutive runs.
6. **Report.** Show the team a "top flaky tests" list weekly.

A team rule of thumb: **a test that needs a retry to pass is a defect in the test suite, and it gets a ticket.**

A real intermittent *product* bug (a race condition in the app) also shows up as a flaky test. If you retry it away, you ship the bug. This is why you read the failure of a retried test at least once before deciding "it is just flaky".

---

## Code Examples

### Example A: Complete retry configuration for the SauceDemo framework

**`pytest.ini`**

```ini
[pytest]
base_url = https://www.saucedemo.com
pythonpath = .
testpaths = tests
addopts = --reruns 1 --reruns-delay 1 --only-rerun TimeoutError --only-rerun "net::ERR_" --tracing retain-on-failure --screenshot only-on-failure
markers =
    smoke: quick checks that run on every commit
    regression: full coverage tests
    quarantine: known-flaky tests excluded from the gating run
```

Explanation of each option:

- `--reruns 1 --reruns-delay 1`: at most one rerun, after a one-second pause.
- `--only-rerun TimeoutError --only-rerun "net::ERR_"`: retry only on Playwright timeouts and Chromium-style network errors (the `net::ERR_...` text appears in navigation error messages). Quotes protect the characters from the shell.
- `--tracing retain-on-failure --screenshot only-on-failure`: keep diagnostics only for failing attempts.
- Marker declarations make `--strict-markers` safe and document intent.

Local debugging without retries:

```bash
pytest tests/test_login_data_driven.py -k "wrong-password" --reruns 0 --headed
```

### Example B: A test with a known unstable dependency

```python
import pytest
from playwright.sync_api import expect


# BUG-1187: performance_glitch_user login is occasionally slower than 5s in CI.
# Retry twice with a short delay. Remove once the environment is upgraded.
@pytest.mark.flaky(reruns=2, reruns_delay=2, only_rerun=["TimeoutError", "AssertionError"])
def test_performance_glitch_user_can_log_in(login_page):
    login_page.login_as("performance_glitch_user", "secret_sauce")
    expect(login_page.page).to_have_url("**/inventory.html", timeout=15_000)
```

Notes:

- The explicit `timeout=15_000` is the **first** fix (give the assertion more patience). The retry is a second safety net.
- Including `AssertionError` in `only_rerun` is deliberate here because a timed-out `expect` raises `AssertionError`. Choose patterns based on what your failures *actually* contain.
- The comment names a defect id and an exit condition.

### Example C: Quarantine workflow

```python
@pytest.mark.quarantine
def test_flaky_cart_badge_animation(inventory_page):
    ...
```

Gating run in CI (must be green to merge):

```bash
pytest -m "not quarantine" --reruns 1
```

Non-blocking monitoring job:

```bash
pytest -m quarantine --reruns 0 || true
```

`|| true` makes the shell treat the command as successful regardless of the test result, so the job reports but does not block. The list of quarantined tests is reviewed weekly and each one has an owner.

### Example D: Quick experiment to measure flakiness

```bash
for i in $(seq 1 20); do
  pytest tests/test_login_data_driven.py -q --reruns 0 -p no:cacheprovider || echo "FAIL on run $i"
done
```

- `for i in $(seq 1 20)` repeats the command 20 times (Bash on macOS/Linux/Git Bash).
- `--reruns 0` disables retries so that flakiness is **not hidden** during measurement.
- `-p no:cacheprovider` disables pytest's cache plug-in so results are independent.
- `|| echo "FAIL on run $i"` prints which iteration failed.

If a test fails 3 times out of 20, its flake rate is 15%, a clear signal to investigate.

---

## Real-World Scenarios

**Scenario 1: Infrastructure blip.** A nightly pipeline runs 600 UI tests against a shared staging server. At 02:10 the server restarts for 40 seconds; 12 tests fail with connection errors. With `--reruns 2 --reruns-delay 30 --only-rerun "net::ERR_"` those tests pass on retry, the build is green, and the report shows 12 "rerun" events, which the engineer notices in the morning and raises with the platform team. Without the retry the whole build would have been red, and the team would have wasted a morning investigating a non-product issue.

**Scenario 2: The retry that hid a bug.** A team sets `--reruns 3` for everything. Over months, a test for coupon codes passes only on its third attempt, because the app has a genuine race condition between applying a coupon and recalculating the total. Customers occasionally see wrong totals in production. The retries had masked a real product defect; trend reporting on reruns would have exposed it. Lesson: monitor the *rate* of reruns.

**Scenario 3: Parallel runs.** With `pytest-xdist` (`pytest -n 4`), tests run in parallel processes. Two tests both use the same shared user and occasionally log each other out. Retries make the symptoms disappear; the real fix is giving each worker its own user account (a fixture keyed on `worker_id`).

**Scenario 4: Slow CI runner.** A trace of a retried failure shows the page was still loading when the test acted. The fix: wait for a *specific* condition (`expect(page.get_by_test_id("inventory-item").first).to_be_visible()`) instead of assuming the page is ready after `goto`. The retry stays for infrastructure noise; the root cause is fixed.

---

## Common Pitfalls and Best Practices

**Pitfalls**

1. **Using retries instead of fixing waits.** The number one anti-pattern. If a test needs a retry because it clicked too early, fix the wait.
2. **Global high retry counts.** `--reruns 5` across the board can multiply suite duration and hide serious problems.
3. **Retrying deterministic failures.** Assertion failures from real defects waste time. Use `--only-rerun` or `--rerun-except`.
4. **Not looking at rerun statistics.** A suite that always "passes on retry" is not healthy.
5. **Non-idempotent tests.** If the first attempt created an order and the retry creates another, the data is corrupted or the retry fails for a new reason. Clean up in fixtures.
6. **Reruns with session-scoped mutable fixtures.** Stale state leaks into the retry.
7. **Debugging with retries on.** You see only the final attempt's success and never the failure. Use `--reruns 0` when investigating.
8. **Ignoring unittest limitation.** The plug-in does not support tests written as `unittest.TestCase` subclasses; use plain pytest functions/classes.
9. **Assuming retry logs are unnecessary.** Capture the *first* failure's trace/screenshot; it is the evidence of the problem.
10. **Hard `sleep`s as "retry".** `time.sleep(5)` before every click is not a retry strategy; it slows everything and still fails sometimes.
11. **No ownership.** Flaky markers without a ticket or owner stay forever.
12. **Pipeline-level blanket re-runs.** "Re-run failed jobs" in CI without recording what failed discards information.

**Best practices**

- Follow the order of defence: **auto-waiting and web-first assertions, then explicit waits and timeouts, then targeted retry helpers, then test-level reruns.**
- Keep retry counts small (1 or 2) and apply them selectively with `only_rerun`.
- Make every test **independent and idempotent**: fresh context, unique data, cleanup in teardown.
- Record retries in reports and review them regularly.
- Document your retry policy in the README (what is retried, why, and how to disable).
- Use `--reruns 0` locally; moderate reruns in CI.
- Keep traces for failed attempts (`--tracing retain-on-failure`) and read them before dismissing a flake.
- Treat the flake rate like a quality metric with a target (for example, under 1%).

---

## Mini Practice Exercises

**Exercise 1: observe a rerun.**
Create the counter-file demo test from Section 4. Run it with `--reruns 0`, `--reruns 1`, and `--reruns 2`. Record the outcome and summary line for each.
*Expected:* fails with 0 and 1 reruns; passes with 2 (the third attempt succeeds).

**Exercise 2: marker precedence.**
Put `@pytest.mark.flaky(reruns=1)` on the demo test and run `pytest --reruns 3`. How many attempts happen? *Answer:* The marker overrides the command line for that test: at most 2 attempts.

**Exercise 3: filter.**
Write two failing tests, one raising `AssertionError`, one raising `TimeoutError("simulated")`. Run `pytest --reruns 2 --only-rerun TimeoutError` and verify only one is retried (the summary shows `2 rerun`).

**Exercise 4: fix instead of retry.**
Write a deliberately flaky SauceDemo test using `page.wait_for_timeout(500)` after login and then `assert page.url.endswith("/inventory.html")` for `performance_glitch_user`. Run it 10 times with `--reruns 0` and count failures. Rewrite it with `expect(page).to_have_url(...)` and repeat.
*Hint:* The point is that the fix removes the flakiness without any retry.

**Exercise 5: retry diagnostics.**
Implement the `attempt` fixture and the `verbose_on_retry` autouse fixture from Section 9. Use the counter-file test to confirm that the retry-only message appears on attempts 2 and 3 only.

**Exercise 6: helper.**
Write the `retry` helper and a unit test for it (no browser): a function that raises `ValueError` twice then returns `"ok"`. Assert that `retry(...)` returns `"ok"` with `attempts=3`, and raises with `attempts=2`.
*Solution sketch:*
```python
def test_retry_succeeds_on_third_try():
    calls = {"n": 0}
    def flaky():
        calls["n"] += 1
        if calls["n"] < 3:
            raise ValueError("boom")
        return "ok"
    assert retry(flaky, attempts=3, delay=0, exceptions=(ValueError,)) == "ok"
```

**Exercise 7 (Project 1 link):** Add a "Retry policy" section to your Project 1 README: what is retried, how many times, the `pytest.ini` options, how to disable retries locally, and your plan for tracking flaky tests. Configure `pytest.ini` accordingly and run the suite once to verify.

---

## Summary / Key Takeaways

- A **flaky test** passes and fails on the same code; it always has a root cause (timing, shared state, data, environment, network, non-determinism).
- Retry at the **lowest effective layer**: Playwright auto-waiting and web-first assertions first; targeted helpers next; whole-test reruns last.
- **`pytest-rerunfailures`** provides `--reruns N`, `--reruns-delay S`, `@pytest.mark.flaky(reruns=..., reruns_delay=...)`, and filters `--only-rerun` / `--rerun-except`.
- A rerun re-creates function-scoped fixtures (fresh browser context and page) but does not undo external side effects: make tests idempotent.
- Keep traces and screenshots from failed attempts; read them before dismissing a flake. Reruns appear in reports, so make them visible.
- Use `execution_count` to collect extra diagnostics on retries.
- Manage flakiness as a process: detect, triage, quarantine, fix, remove the retry, and track the flake rate.
- Retries are a safety net, **not a fix**. Never use them to hide real defects.

---

## External Resources

- pytest-rerunfailures project page and documentation (PyPI): https://pypi.org/project/pytest-rerunfailures/
- pytest-rerunfailures source repository and changelog: https://github.com/pytest-dev/pytest-rerunfailures
- Playwright for Python, "Auto-waiting" (actionability checks) and "Assertions": https://playwright.dev/python/docs/actionability
