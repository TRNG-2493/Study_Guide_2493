# Pair Project: The Locator Catalog

**Week 4, Day 4 (Thursday) | Web Locators & Playwright Introduction | Project 1: QE Foundations**
**Mode:** Collaborative Pair Programming (Driver / Navigator) | **Time:** 3 hours | **Level:** beginner

> Instructors: the CMA Log calls this file `exercise-web-locators-playwright-introduction.md`. It is an identical copy of this README.

---

## 1. The Scenario

Your team lead has asked the Project 1 automation squad for a **UI locator catalog**: one trusted table that lists every important element of the practice site, with a CSS selector, an XPath selector, how many elements each should match, and how stable the selector is. Tomorrow's Playwright tests (Friday, individual) will be built from this catalog, so a wrong or fragile row today costs everybody time tomorrow.

Catalogs rot. So you will not just write a table: you will **verify it with an automated PyTest suite** and produce an HTML report that anyone can open to see whether the catalog is still true. That is a mini version of a real test framework, and it uses everything from this week.

**Practice site:** SauceDemo (`https://www.saucedemo.com`, login `standard_user` / `secret_sauce`).
**Offline copy:** `starter_code/site/practice_page.html` is a local page with the same ids, classes and `data-test` attributes. It is the **default** (no network needed, never changes). Switch to the real site with `SITE=live`. The real site is third-party and may differ slightly: if a row passes locally but fails live, that is a finding to record in `docs/CATALOG.md`, not a disaster.

## 2. Learning Objectives

By the end you can:

1. Find an element with a **CSS selector and an XPath**, check both in DevTools, and make them agree.
2. **Rank selectors by stability** and defend your choice in one sentence.
3. Use combinators (`>`, `+`), attribute operators (`^= *=`), `:not()`, `:nth-child`, `:has()`, and XPath `contains()`, `starts-with()`, `ancestor::`, `following-sibling::`.
4. Explain and use the Playwright object model: `Playwright > Browser > BrowserContext > Page > Locator` (and that a locator is lazy).
5. Build a small, clean PyTest project: markers, `parametrize` with ids, fixtures and `conftest.py`, a custom assertion, exception tests, and an HTML report.
6. Work as a **pair**: driver and navigator roles, swapping on a clock, one shared repo, a short retrospective.

## 3. How This Pulls Together the Whole Week

| Day | Skill from that day | Where you use it today |
|-----|---------------------|------------------------|
| Mon: PyTest fundamentals | test functions, `assert`, markers, `-m` / `-k` | `smoke`/`css`/`xpath`/`data` markers, `--strict-markers`, running subsets |
| Tue: PyTest advanced | fixtures, scopes, `parametrize`, `conftest.py` | `site_browser` (session) and per-test page fixtures; one test per catalog row |
| Wed: Framework and reporting | custom assertions, exception testing, data-driven design, HTML report | `assert_locator_count`, `pytest.raises`, the catalog as data, `report.html` |
| Thu: Locators and Playwright | CSS, XPath, stability, Playwright objects | the catalog rows and the browser fixtures |

## 4. Prerequisites

* Read this week's written lessons, especially Thursday's seven.
* Python 3.10+ and VS Code, Git installed, Chrome with DevTools.
* Both partners have access to the same machine **or** the same Git remote (see Setup).
* Everything is solvable from Monday-Thursday material. **Do not use** `get_by_role`, `get_by_text`, `expect()`, `codegen` or the Inspector: those are Friday. If you already know them, still use selectors today; that is the objective.

## 5. Pair Programming Rules

**Roles**

* **Driver:** the only person typing. Says aloud what they are typing and why. Does not decide the strategy alone.
* **Navigator:** does not touch the keyboard. Watches for typos and wrong counts, looks things up in the lessons, runs the DevTools experiments on a second screen/window when possible, and keeps the big picture ("are we still on Task 3?").
* **Swap every 30 minutes** (set a phone timer). Before swapping, the departing driver commits: `swap N: <what we finished>`. The new driver starts by reading the last commit and the TODOs aloud.
* Disagree with evidence: run it in DevTools or PyTest. Opinions lose to counts.
* Stuck for more than 10 minutes? Ask the other pair next to you, then the instructor. Never silently split into two solo halves: that fails the activity.
* Equal airtime: if the navigator has said nothing for 5 minutes, the driver asks "what do you see?".

**One shared repo**

* Create **one** repo from the starter and use the branch `pair/<namea>-<nameb>`. Both partners must be able to commit (shared machine, or both push to the same remote branch; pull before you start each block).
* Commits alternate between you; use `Co-authored-by:` for the person who was navigating. The Git log is evidence of your swaps.

## 6. Setup (about 10 minutes, together)

```bash
cd starter_code
python -m venv .venv
# Windows:  .venv\Scripts\activate        macOS/Linux:  source .venv/bin/activate
pip install -r requirements.txt
playwright install chromium
git init && git checkout -b pair/<namea>-<nameb> && git add . && git commit -m "starter"

python -m pytest -q
```

Run options (environment variables):

| Goal | bash | PowerShell |
|------|------|-----------|
| Offline page (default) | `python -m pytest` | `python -m pytest` |
| Real SauceDemo | `SITE=live python -m pytest` | `$env:SITE="live"; python -m pytest` |
| Watch the browser | `HEADLESS=0 SLOW_MO=300 python -m pytest` | `$env:HEADLESS="0"; $env:SLOW_MO="300"; python -m pytest` |
| Only the quick catalog tests | `python -m pytest -m data` | same |
| Report | `python -m pytest --html=docs/report.html --self-contained-html` | same |

**Expected state of the untouched starter:** 3 pass, 13 fail, 4 error, 3 skipped. The failures say `TODO` or `NotImplementedError` on purpose. Your job is to turn them green *honestly* (no deleting tests, no weakening checks).

### What is in the starter

```
starter_code/
  pytest.ini, requirements.txt, .gitignore
  conftest.py                  fixtures: site_browser (provided), login_page (provided), error_page + inventory_page (TODO)
  site/practice_page.html      offline practice site
  locator_catalog/
    config.py                  SITE / HEADLESS / URLs (provided)
    pages.py                   open_login(), login(), failed_login() (provided)
    catalog.py                 CatalogRow + CATALOG (3 example rows; TODO the rest), get_row (TODO)
    assertions.py              assert_locator_count / assert_locator_text (TODO)
  tests/
    params.py                  catalog_params(page)  (TODO: ids + smoke marks)
    test_00_environment.py     two smoke tests (provided; they pass)
    test_catalog_data.py       no-browser checks on the catalog (TODO)
    test_catalog_login.py      CSS/XPath verification, login page (partly provided)
    test_catalog_inventory.py  CSS/XPath verification, product page (TODO)
    test_context_isolation.py  Browser vs BrowserContext (TODO)
    test_fragility.py          stretch S1 (skipped)
  docs/ CATALOG.md, PAIR_LOG.md, RETROSPECTIVE.md   templates to fill in
```

## 7. Core Tasks (step by step)

Suggested driver in brackets; the clock decides the swaps, not the task boundaries.

### Task 1 - Explore and plan (Block 1) [A drives]

1. Open the site (local page via `File > Open`, or live) and DevTools (F12). Log in. Use `$$('selector').length` in the Console to test every selector **before** it goes into Python.
2. Fill the first draft of `docs/CATALOG.md` with at least 16 elements (see "The rows you must cover" below). For each, find a CSS and an XPath that give the same count.
3. Read the three example rows in `locator_catalog/catalog.py` and run `python -m pytest -m data -q` to see the current state.

### Task 2 - Login-page rows (Block 2) [B drives]

Add the login-page and `login_error` rows to `CATALOG` in `catalog.py` (name, page, css, xpath, expected, technique, stability, why; add `expected_text` where it makes sense). Choose the `technique` label that best describes your selector (`TECHNIQUES` lists them).

### Task 3 - Inventory rows and the data tests (Blocks 2-3) [B then A]

1. Add the inventory rows.
2. Implement every `TODO` in `tests/test_catalog_data.py` **except** the exception tests: they check the catalog's own rules (unique names, at least 16 rows, at least 7 techniques, XPath starts with `//`, stability rules, fragile rows explain themselves...). They run in milliseconds with no browser. Each failure message must say what to fix.

### Task 4 - Verify the catalog in a real browser (Blocks 3-4) [A then B]

1. `locator_catalog/assertions.py`: write `assert_locator_count` and `assert_locator_text` (custom assertions: `__tracebackhide__`, and a message that contains the label, expected, actual, selector and page URL).
2. `conftest.py`: implement `error_page` (login page after a failed login) and `inventory_page` (logged in), using `locator_catalog/pages.py`.
3. Complete the test files: copy the shape of the provided `test_login_css`. Every row is tested **twice** (once for CSS, once for XPath, with the `xpath=` prefix) so a failure tells you which language is wrong.
4. Break one row on purpose, read the failure message, decide if a stranger could fix it from the message alone. Then fix the row.

### Task 5 - Exception tests (Block 4) [B drives]

1. In `catalog.py`, make `CatalogRow.__post_init__` reject bad rows with `ValueError`, and make `get_row` raise `KeyError` for unknown names (messages must contain the phrases listed in the TODO comments).
2. In `test_catalog_data.py`, test those with `pytest.raises(..., match=...)`. The five bad-row cases belong in **one** parametrized test with ids.

### Task 6 - Markers, readability and the report (Blocks 4-5) [B then A]

1. `tests/params.py`: readable ids (the row name) and `@pytest.mark.smoke` on rows flagged `smoke=True`.
2. Run `python -m pytest -m smoke`, `-m "css and not xpath"`, `-m data`, `-k onesie`. Write the number of tests each selects in `docs/PAIR_LOG.md`.
3. Generate `docs/report.html` (`--html=docs/report.html --self-contained-html`). Open it and check that failing rows are easy to find.

### Task 7 - Playwright architecture test (Block 5) [A drives]

Implement `tests/test_context_isolation.py` following the numbered TODO. It proves: sessions are shared inside a `BrowserContext` and isolated between contexts. Explain to each other in one sentence why the test suite uses one `Browser` per run but one `BrowserContext` per test.

### Task 8 - Try it live and close out (Block 5) [both]

1. If the network allows, run `SITE=live python -m pytest -m "not stretch"`. Record any failing row in the second table in `docs/CATALOG.md` and diagnose it with the debug checklist from `dynamic-selectors.md`.
2. Finish `docs/PAIR_LOG.md` and write `docs/RETROSPECTIVE.md` together (15 min, see below).
3. Final commit, push, submit.

### The rows you must cover

At least **16 rows** in total, including **all** of these (choose the selectors yourselves; the example rows already cover three of the page areas):

| Page | Target | Expected | Must demonstrate |
|------|--------|----------|------------------|
| login | the "Swag Labs" logo (text check) | 1 | semantic class (example row) |
| login | username box by its `placeholder` | 1 | attribute selector |
| login | password box by `type` | 1 | attribute selector |
| login | login button by its `value` | 1 | attribute selector |
| login | both text-style inputs by a shared class | 2 | XPath `contains()` |
| login | every input that carries a `data-test` attribute | 3 | `[attr]` / `@attr` |
| login_error | the error message after a bad login (text check) | 1 | `data-test` (example row) |
| login_error | the same message as a direct child of its container | 1 | child combinator `>` |
| inventory | the page heading by `data-test` (text "Products") | 1 | `data-test` + text |
| inventory | the product descriptions | 6 | class selector |
| inventory | Add-to-cart buttons for the five "Sauce Labs" products only | 5 | `^=` / `starts-with()` |
| inventory | Add-to-cart buttons of the two T-shirts | 2 | `*=` / `contains()` |
| inventory | all Add-to-cart buttons **except** the Backpack | 5 | `:not()` / `not()` |
| inventory | each product's description that directly follows its name link | 6 | sibling combinator `+` / `following-sibling::` |
| inventory | the price of the Sauce Labs Onesie (text `$7.99`) | 1 | `:has()` / `ancestor::` (anchored on the name) |
| inventory | the name of the 2nd product (text check) | 1 | `:nth-child` / `(...)[2]`, rank 7, explain why it is fragile |

You also need at least **7 different `technique` labels**, at least **3 rows with `expected_text`**, and the stability numbers must follow the rules in `basic-and-attribute-selectors.md` Part 3.

## 8. Stretch Tasks (only after Definition of Done is met)

* **S1 - Prove fragility (about 20 min).** Make `site/practice_page_reordered.html` (copy the page, move one whole product card in the editor). In `tests/test_fragility.py` show that a name-anchored row still passes and the position-based row breaks. Remove the `skip` markers.
* **S2 - Bad selector error.** Write a test that passes a syntactically invalid selector (for example `"[["`) to `page.locator(...).count()` and asserts that Playwright raises an error. (Hint: `from playwright.sync_api import Error`.) What does that tell you about when the search really happens?
* **S3 - Live-only marker.** Use `pytest.mark.skipif` on `config.SITE` to mark any row that only exists on the live site (for example the sort dropdown, burger menu, or the cart page) and add three such rows.
* **S4 - Report polish.** Add a hook in `conftest.py` that sets the report title and shows the site (local/live) in the report (Wednesday: HTML reporting).
* **S5 - Dedupe.** Add a data test that fails if two rows have the same CSS string.

## 9. Deliverables

Submit **one** per pair:

1. The Git repo (or zip including `.git`) with branch `pair/<namea>-<nameb>`, containing all files from `starter_code/` completed.
2. `docs/CATALOG.md`: the human-readable catalog (table filled in from `catalog.py`) plus the live-vs-local findings table.
3. `docs/report.html`: HTML report of a full run (self-contained).
4. `docs/PAIR_LOG.md`: one row per block with driver/navigator names.
5. `docs/RETROSPECTIVE.md`: completed, including each person's separate reflection.

## 10. Definition of Done and Rubric (100 points)

| # | Criterion | Points | Done when |
|---|-----------|--------|-----------|
| 1 | Catalog content | 25 | at least 16 rows; every row has CSS **and** XPath; all "must cover" targets present; counts and texts are right |
| 2 | Verification | 20 | every row verified for CSS and XPath in a browser (local); full run green; failure message names label, expected, actual, selector, URL |
| 3 | Selector quality | 10 | at least 7 techniques; stability ranks correct; every rank 6-7 row explains why it is acceptable |
| 4 | PyTest craft | 15 | markers registered and used (`-m smoke`, `-m data` work); `parametrize` with ids; fixtures with sensible scopes; custom assertion; exception tests with `pytest.raises` |
| 5 | Playwright understanding | 10 | context-isolation test passes and both partners can explain Browser vs BrowserContext vs Page vs Locator (instructor asks each person one question) |
| 6 | Pair process | 15 | at least 5 alternating commits; complete pair log; retrospective written together; each partner can explain any line of code on request |
| 7 | Report and hygiene | 5 | `docs/report.html` present; no dead code or leftover `TODO`; no `time.sleep` |

**Minimum to pass: 70.** Stretch tasks add up to 10 bonus points (2 each).
**Automatic checks the instructor will run:** `python -m pytest -m data -q` (must be all green, none skipped except stretch) and `python -m pytest -m "not stretch" --html=r.html --self-contained-html`.

## 11. Hints (read only when stuck)

1. **A selector returns a list.** In DevTools use `$$('...').length`; in XPath use `$x('...').length`.
2. **Count right, wrong element?** That is why `expected_text` exists: check `inner_text()`.
3. `.inventory_item_name` sits **inside** an `<a>`, so it is not a sibling of `.inventory_item_desc`; the `<a>` is.
4. XPath is 1-based. `(//div[@class='inventory_item'])[2]` with the parentheses means "second in the whole page"; without them it means "second within each parent".
5. `//div[contains(@class,'inventory_item')]` also matches `inventory_item_name`, `_price`, `_img`... (substring trap). Use `@class='...'` when you want the exact class.
6. CSS `:has()` goes "up": `.inventory_item:has(.inventory_item_name:text-is('Sauce Labs Onesie')) .inventory_item_price`. `:text-is()` and `:has-text()` are Playwright-only: they work inside `page.locator()` but not in DevTools `$$()`. In DevTools use XPath `//div[text()='...']`.
7. XPath for "go up": `//div[text()='Sauce Labs Onesie']/ancestor::div[@class='inventory_item']//div[@class='inventory_item_price']`.
8. A parametrized test needs the fixture name in its arguments *and* the parameter name; `pytest.param(value, id="...", marks=pytest.mark.x)` gives one test a readable name and a marker.
9. A custom assertion that fails should read like a bug report: what, expected, actual, where.
10. `with pytest.raises(KeyError, match="..."):` : `match` is a regular expression searched in the message. `KeyError` messages are shown with quotes; escape or choose a distinctive word.
11. `Unknown marker` error? That is `--strict-markers` doing its job: register the marker in `pytest.ini`.
12. Count is 0 right after a click on the live site? `count()` does not wait. `pages.login()` already waits for the new URL once; that is all the waiting you need today.

## 12. Time Plan (3 hours)

| Clock | Block | Driver | Focus |
|-------|-------|--------|-------|
| 0:00-0:10 | Setup | both | repo, venv, `playwright install`, read the README, sign the roles |
| 0:10-0:40 | 1 | A | Task 1: DevTools exploration, draft catalog |
| 0:40-1:10 | 2 | B | Task 2 login rows; start Task 3 |
| 1:10-1:40 | 3 | A | Task 3 inventory rows and data tests; start Task 4 |
| 1:40-1:50 | Break | | stretch legs; navigator of the next block re-reads the TODOs |
| 1:50-2:20 | 4 | B | Task 4 assertions, fixtures, tests; Task 5 exception tests |
| 2:20-2:50 | 5 | A | Tasks 6-8: markers, report, context test, live run, stretch if ahead |
| 2:50-3:00 | Close | both | retrospective, final commit, submit |

Core tasks need about 2 h 30 min of work; the rest is break, setup and retrospective. If you are behind at 1:40, drop Task 7 and S-tasks, never the catalog or the verification.

## 13. Project 1 - QE Foundations milestone

> **Note for instructors:** no Project 1 specification was available when this exercise was written. The milestone below is a sensible definition consistent with the weekly CMA Log ("Project 1 gets automated tests each day") and with Thursday's demo. **Adjust it to the real Project 1 deliverables** (target application, file locations, naming).

**Milestone for Day 4 (Thursday): the first verified UI locator catalog for Project 1.**

* A catalog of at least 16 elements of the practice application, each with CSS **and** XPath, expected count, text where relevant, and a stability rank with a reason.
* The catalog is **code-verified**: a PyTest suite checks every row in a real browser and a self-contained HTML report is produced.
* This repository (or its `locator_catalog/` package and `tests/`) becomes the **starting point of the Project 1 UI test layer**. On Friday, each trainee builds three UI scenarios on top of it, taking selectors from `catalog.py` instead of retyping them.
* Fold in Wednesday's Project 1 framework conventions: marker names, `pytest.ini`, `conftest.py` layout and report naming should match your Project 1 repo. If the pair's catalog repo differs from the team's Project 1 repo, copy the package across and keep the tests passing there.
* Evidence for the Project 1 log: link to the branch, the report file, and a 3-line note on what you would change if the application's markup changed.

## 14. Submission Instructions

1. `python -m pytest -m "not stretch" --html=docs/report.html --self-contained-html` and confirm it is green (local).
2. `git add -A && git commit -m "final: locator catalog" && git push origin pair/<namea>-<nameb>` (or zip the folder including `.git`, named `week4-thu-<namea>-<nameb>.zip`).
3. Submit the repo link (or zip) to the instructor channel, with the pair names in the message.
4. Do **not** include `.venv/`, `__pycache__/` or `.pytest_cache/`.
5. Both partners individually fill in the reflection line in `docs/RETROSPECTIVE.md` before leaving.

## 15. Short Retrospective Template

Use `docs/RETROSPECTIVE.md` (copy included in the starter). Sections: what went well, what was hard, roles, one technical learning each for locators / Playwright / PyTest, separate individual reflections, and one change for tomorrow. Maximum one page; write it together in the last 15 minutes, not after the day.
