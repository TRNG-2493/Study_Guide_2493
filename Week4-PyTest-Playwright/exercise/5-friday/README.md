# Friday Exercise: Automate 3 Project 1 UI Scenarios with Playwright

**Week 4 (PyTest & Playwright), Day 5 (Friday) | Individual exercise | Time: 2 to 3 hours**
**Mode:** A (code lab) | **Project 1 - QE Foundations milestone included below**

> Log filename: `exercise-playwright-core-automation.md` (identical copy of this README).

---

## 1. Scenario

You are the new QE on **GadgetHub**, a small online gadget shop. The team's manual test suite (your Project 1 test cases) has three UI cases that are run before every release and everybody is tired of clicking through them:

| Manual case | Scenario |
|-------------|----------|
| TC-UI-01 | A registered customer signs in successfully |
| TC-UI-02 | Wrong, empty or locked-out credentials are rejected with a clear message |
| TC-UI-03 | A customer searches for a product and sees the right results |

Your job today: automate these three scenarios (plus a few supporting checks) as clean, fast, **non-flaky** Playwright tests that run under PyTest, and learn to debug and record tests with the Inspector and codegen.

## 2. Learning objectives

By the end you can:
1. Write Playwright tests with the `page` fixture using Arrange-Act-Assert.
2. Use **built-in locators** (`get_by_role`, `get_by_label`, `get_by_placeholder`, `get_by_text`, `get_by_test_id`) in the recommended priority order.
3. Rely on **auto-waiting and web-first assertions** (`expect(...)`) instead of `time.sleep`.
4. **Filter and chain** locators to act on one product card out of many.
5. Combine today's tools with this week's PyTest skills: fixtures, `conftest.py`, `parametrize`, markers.
6. Read a Playwright failure message, then use the **Inspector** and **codegen** to fix and speed up your work.

## 3. Prerequisites (what you may use)

Only this week's material: Monday (markers, `-k`, `-m`), Tuesday (fixtures, `conftest.py`, parametrize), Wednesday (test organisation, custom assertions, reports), Thursday (CSS and locator basics, Playwright architecture), and today's lessons in `written/5-friday/` (creating tests, runner, auto-waiting, built-in locators, filtering and chaining, Inspector, record and playback). The instructor demo (`demos/5-friday/`) shows similar patterns on a different practice site; **do not copy it, adapt it**.

## 4. Setup (15 min)

```bash
cd starter_code
python -m venv .venv
# Windows PowerShell:  .venv\Scripts\Activate.ps1      macOS/Linux: source .venv/bin/activate
python -m pip install -r requirements.txt
python -m playwright install chromium
python -m pytest -v
```

**Expected result of the first run:** `1 passed, 11 skipped, 3 deselected` (the smoke test passes; every TODO test is skipped; the 3 live tests are deselected on purpose). If the smoke test fails, fix your setup before doing anything else (see Hints).

Useful options (from the runner lesson): `--headed`, `--slowmo 500`, `--screenshot only-on-failure`, `--tracing retain-on-failure`, `-k name`, `-m marker`.

### The practice site: two options

| | Offline **GadgetHub** (core tasks) | Live **saucedemo.com** (stretch) |
|--|--|--|
| Needs internet | No. It is served from memory by `gadgethub.py` | Yes |
| Why | Reliable, deterministic, has a real search box with a deliberately slow (600 ms) server | Real public site; markup can change without notice |
| Where | `tests/test_01..04*.py` | `tests/test_live_saucedemo.py` (run with `-m live`) |

If your network blocks saucedemo.com (or the site changed), the offline site is enough to earn full core marks. **Do not edit `gadgethub.py`.**

**GadgetHub facts you need**
- Sign-in page title `GadgetHub - Sign in`; fields **Email**, **Password**; button **Sign in**; error message appears in an element with role `alert` (`data-testid="login-error"`).
- Accounts: `tester@gadgethub.test` / `Passw0rd!` (works). `locked@gadgethub.test` / `Passw0rd!` (locked: "Account locked. Contact support."). Anything else: "Invalid email or password". Empty email: "Email is required"; empty password (with an email): "Password is required". Passwords are case-sensitive.
- A successful sign-in goes to `/shop.html` (title `GadgetHub - Shop`). Opening `/shop.html` without signing in sends you back to the sign-in page.
- Shop page: heading **Shop**, `data-testid="welcome"` ("Signed in as <email>"), search box (role `searchbox`, label "Search gadgets", placeholder `Search gadgets...`), `Searching...` status while the server "thinks" (600 ms), message `No gadgets match your search.` when empty, 8 product cards (`<article class="card">` with an `h2` name, price, and an **Add to cart** / **Remove** button), cart counter `data-testid="cart-count"`, **Sign out** button.
- Products: USB-C Hub, USB-C Charger, Wireless Charger, Wireless Mouse, Mechanical Keyboard, Laptop Stand, HD Webcam, Noise-Cancelling Headphones (in that order). Search is case-insensitive "contains".

## 5. Core tasks (step by step)

Work in `starter_code/`. Each TODO test currently calls `pytest.skip(...)`: delete that line when you implement the test. Commit after each task.

### Task 1: Explore the site and run the smoke test (15 min)
1. Run `python -m pytest tests/test_00_smoke.py --headed --slowmo 700 -v` and watch the browser.
2. Using the Inspector (`PWDEBUG=1`; PowerShell: `$env:PWDEBUG=1`) on the smoke test OR your own browser's DevTools, list **3 locators you would use** for the Email field, the Sign in button and the search box. Note them down on paper; Task 2 uses them.

### Task 2: Fixture and Scenario 1, valid login (25 min)
1. In `conftest.py` implement the `logged_in_page` fixture (TODO inside). Built-in locators only; wait with an assertion, not a sleep.
2. In `tests/test_01_login.py` implement `test_valid_login_reaches_shop`. Assert the URL, the **Shop** heading and the welcome text.
3. Run `python -m pytest -m project1 -v`. The valid-login test should pass.

### Task 3: Scenario 2, invalid and locked-out login (25 min)
1. Fill in the `parametrize` table of `test_invalid_login_shows_error` with **at least 5 cases** covering: wrong password, unknown user, locked-out user, empty email, empty password. Give every case a readable `id`.
2. Implement the test body (error message shown, still not on `/shop`).
3. Implement `test_protected_page_redirects_when_not_signed_in`.
4. Run it with `-k invalid -v` and read the test ids in the output.

### Task 4: Scenario 3, search (25 min)
1. Implement `test_search_finds_matching_products` (`usb` gives exactly the two USB-C products, in order).
2. Implement `test_search_with_no_match_shows_message` (`zzz`).
3. Fill in and implement `test_search_terms_parametrized` with at least 3 terms (include one UPPERCASE term).
4. **Rule:** no `time.sleep`, no `wait_for_timeout`, no `.count()` immediately after typing. Run the file with `--headed --slowmo 300` and notice the search is slow while your tests are still correct.

### Task 5: Filtering and chaining (20 min)
In `tests/test_03_cart_chaining.py` implement both tests: add only the Laptop Stand to the cart (and prove the Webcam was not added), and count cards containing "Wireless".

### Task 6: Debug three broken tests (20 min)
`tests/test_04_debug_me.py` has three tests whose **test code** is wrong. Once your `logged_in_page` fixture works they FAIL. For each: read the error, reproduce with `PWDEBUG=1 python -m pytest tests/test_04_debug_me.py -k bug_a --headed -s` (or put `page.pause()` in the test), find the cause with **Pick locator**, fix it, and record what was wrong in `NOTES.md` section 2.

### Task 7: Record and refactor (15 min)
Run `python -m playwright codegen` against any site with a login form (for example saucedemo.com if reachable; otherwise any public practice site, or use the Inspector on GadgetHub). Record the sign-in flow, paste the generated code into `NOTES.md` (or `recorded_login.py`), then list in section 3 **one thing you changed** and **one you kept**, with reasons (codegen writes actions; you must add assertions).

### Task 8: Finish the Project 1 milestone (10 min)
Fill in the traceability table in `NOTES.md` and run the final commands in "Deliverables".

## 6. Stretch tasks (optional)

1. **Live SauceDemo:** implement the three tests in `tests/test_live_saucedemo.py` (valid login, locked-out login, find "Sauce Labs Backpack" and assert its price). Run `python -m pytest -m live -v`. SauceDemo has no search box, so "find a product" means filter the card.
2. Add `--screenshot only-on-failure --tracing retain-on-failure` and open a trace of a deliberately failing test with `python -m playwright show-trace <trace.zip>`.
3. Add one more test: adding two products then removing one leaves cart count `1` (chain from cards).
4. Make a failing assertion produce a clearer message with a custom timeout, e.g. `expect(...).to_have_count(2, timeout=3000)`, and explain the difference in the output.
5. Run in a second browser: `--browser firefox` (after `playwright install firefox`) and note any difference.

## 7. Deliverables

Submit the whole `starter_code/` folder (without `.venv`) containing:
1. `conftest.py` and all four completed test files (no remaining `pytest.skip("TODO...")` in core tasks).
2. `NOTES.md` completed (traceability table, debugging log, codegen notes, reflection).
3. `results.txt`: output of `python -m pytest -v -m "not live" > results.txt`. (PowerShell: `python -m pytest -v -m "not live" | Out-File results.txt`.)
4. Optional: `report.html` if you add `--html=report.html --self-contained-html` (Wednesday's pytest-html, `pip install pytest-html`).

## 8. Project 1 - QE Foundations milestone

> **Instructor note:** no Project 1 specification was supplied when this exercise was written. The milestone below is a sensible default consistent with the Week 4 plan; **instructors should adjust it** to the real Project 1 brief (IDs, site and scenarios).

**Milestone for Friday: "First automated UI regression slice".** By the end of today your Project 1 repository contains **three Project 1 UI scenarios automated in Playwright**:

| # | Scenario | Manual case | Must be marked | Minimum evidence |
|---|----------|-------------|----------------|------------------|
| 1 | Valid login | TC-UI-01 | `@pytest.mark.project1` | passes, asserts URL + visible page content |
| 2 | Invalid / locked-out login | TC-UI-02 | `@pytest.mark.project1` | parametrized, at least 5 cases, each asserts the message |
| 3 | Search / find product | TC-UI-03 | `@pytest.mark.project1` | passes with no sleeps, covers a positive and a negative term |

Acceptance: `python -m pytest -m project1 -v` is green and collects at least 7 tests; `NOTES.md` traceability table is filled in. If your own Project 1 uses a different site, copy the same three scenarios onto it and keep the marker. Next week these tests become the base for the Page Object Model.

## 9. Definition of Done and rubric (100 points)

| Area | Points | Full marks when |
|------|-------:|-----------------|
| Setup and running | 5 | Starter installs, `python -m pytest` runs, `results.txt` included |
| Scenario 1: valid login + `logged_in_page` fixture | 15 | Fixture reused by later tests; web-first assertions; no sleeps |
| Scenario 2: invalid/locked login | 20 | At least 5 parametrized cases with readable ids; error text asserted; not on `/shop` |
| Scenario 3: search | 20 | Positive, negative and parametrized terms; list text asserted; relies on auto-waiting |
| Locator quality | 10 | Built-in locators first (role, label, placeholder, test id); CSS only where nothing better; `nth()` avoided where text filtering works |
| Filtering and chaining | 10 | Actions scoped to one card; asserts other card is unaffected |
| Debugging (Task 6) | 10 | All 3 fixed and explained correctly in `NOTES.md` |
| Inspector / codegen notes | 5 | One changed and one kept item, with reasons |
| Milestone traceability + hygiene | 5 | Table filled, `project1` marker used, clear test names, no commented-out junk |

Automatic deductions: `time.sleep` / `wait_for_timeout` (-5 each, max -15), `.count()` or `.is_visible()` used as an assertion right after an action (-3 each), tests that depend on running in a certain order (-5). Stretch tasks add up to +10 bonus (cap 100).

**Definition of Done checklist**
- [ ] `python -m pytest -m "not live" -v`: everything passes, nothing left skipped with "TODO"
- [ ] `python -m pytest -m project1 -v`: green, at least 7 tests
- [ ] No sleeps, no hard-coded waits
- [ ] `NOTES.md` complete
- [ ] You can explain to a peer why `expect(...).to_have_count(2)` is safe and `locator.count() == 2` is not

## 10. Hints (try before reading)

<details><summary>Setup problems</summary>

- `playwright: command not found` / "Executable doesn't exist": activate the venv and run `python -m playwright install chromium`.
- Always use `python -m pytest` so pytest and the plugin come from the same Python.
- `unknown marker` error: you typed a marker not listed in `pytest.ini` (this is `--strict-markers` doing its job).
</details>

<details><summary>Locator hints</summary>

- A text field with a visible label: `get_by_label("Email")`. A button: `get_by_role("button", name="Sign in")`.
- The error: `get_by_role("alert")`. The search box: `get_by_role("searchbox", name="Search gadgets")` or `get_by_placeholder("Search gadgets...")`.
- Product names are level-2 headings: `get_by_role("heading", level=2)`.
- Cart counter: `get_by_test_id("cart-count")` (default attribute `data-testid`).
</details>

<details><summary>Waiting hints</summary>

- `expect(locator).to_have_count(n)` and `expect(locator).to_have_text([...])` retry until true or timeout; a plain `assert locator.count() == n` checks once.
- `expect(locator).to_be_hidden()` waits for a spinner or status to go away.
</details>

<details><summary>Chaining hints</summary>

`card = page.locator(".card").filter(has_text="Laptop Stand")`, then `card.get_by_role("button", name="Add to cart")`. A locator that matches 8 elements cannot be clicked ("strict mode violation"): Playwright refuses to guess.
</details>

<details><summary>Debugging hints (Task 6)</summary>

Bug A: read the timeout log, compare the name in the locator with the real button text. Bug B: the error says how many elements matched. Bug C: compare what `.count()` returns with what the page shows a moment later.
</details>

## 11. Time plan (2.5 h, up to 3 h with stretch)

| Time | Activity |
|------|----------|
| 0:00-0:15 | Task 1 setup and explore |
| 0:15-0:40 | Task 2 fixture + valid login |
| 0:40-1:05 | Task 3 invalid logins |
| 1:05-1:15 | Break |
| 1:15-1:40 | Task 4 search |
| 1:40-2:00 | Task 5 filter and chain |
| 2:00-2:20 | Task 6 debug |
| 2:20-2:35 | Task 7 codegen + Task 8 wrap-up |
| 2:35-3:00 | Stretch / buffer |

## 12. Submission instructions

1. Create a branch `week4-fri-<yourname>` in your Project 1 repository (or your course repo) and copy `starter_code/` content into `week4/friday/`.
2. Commit with clear messages (for example `Add valid login test`), push, and open a pull request titled `Week 4 Friday: Playwright core automation`, or zip the folder if instructed.
3. Post the PR link (or zip) in the course channel before the stated deadline, and be ready to demo `python -m pytest -m project1 --headed --slowmo 500` in the next session.

---
*Instructor material is in `solution/` (see `INSTRUCTOR_ONLY.md`). Do not distribute before the deadline.*
