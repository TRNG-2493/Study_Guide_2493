# Exercise: Refactor a Flat UI Suite into POM with Data-Driven JSON

**Week 5, Wednesday (3-wednesday)** | **Mode A: Implementation (code lab)** | **Individual** | **Time: 2-3 hours**
**Project lane:** Project 1 - QE Foundations | **Needs:** Monday, Tuesday and today's reading + demo only (no Cypress)

---

## Scenario

You have inherited a working but messy UI test suite for a small online shop. Seven tests, all green, all copy-pasted: the login block appears in every test, selectors and URLs are hard-coded, credentials and expected messages are inline, and four of the tests differ only in their data. A reviewer would call this "it works, but I would not want to maintain it".

Your job is to **refactor, not rewrite**. Behaviour must not change; only the structure does. You will turn the flat suite into a small framework:

```
flat script  ->  page objects  ->  fixtures + hooks  ->  JSON-driven tests  ->  retries  ->  HTML report
```

At the end you do the same thing to **your own Project 1 UI tests** (see "Project 1 - QE Foundations milestone").

You can also see this as a rehearsal: today's demo refactored a similar suite live. Here you do it on your own, on a different app.

> **No internet needed.** The app under test is a tiny local shop (`starter_code/app/mock_shop.py`). `conftest.py` starts it for you on `http://127.0.0.1:8791` whenever you run `pytest`. It is a training stand-in, not something you test or edit.

---

## Learning goals

By the end you can:

1. Run a refactor safely: green baseline, small steps, commit after each step.
2. Replace duplicated locators with **page objects** (`BasePage`, a `Header` component, one class per page) where navigation returns the next page.
3. Deliver pages through **custom fixtures** and use an autouse fixture and a plugin **hook**.
4. Turn copy-pasted tests into **JSON-driven parametrized** tests with readable ids.
5. Configure **retries** that hide infrastructure noise but never real bugs.
6. Produce a self-contained **HTML report** with failure evidence.

---

## Setup (about 10 minutes)

```bash
cd starter_code
python -m venv .venv && source .venv/bin/activate      # Windows: .venv\Scripts\activate
pip install -r requirements.txt
playwright install chromium
pytest
```

**Expected result:** `7 passed, 2 deselected`. The 2 deselected tests are demo helpers you will use in Tasks 6 and 7. If you do not see 7 passed, fix your setup before touching any code.

Then run `git init && git add -A && git commit -m "Baseline: flat suite"` (or use your own repo). This commit is your **"before" hash** for the submission.

### What is in `starter_code/`

| Path | State | What it is |
|---|---|---|
| `tests/test_shop_flat.py` | **given, messy** | The 7-test flat suite. This is what you refactor. |
| `app/mock_shop.py`, top of `conftest.py` | **given, do not edit** | The local app and the fixture that starts it. |
| `tests/test_retry_demo.py`, `tests/test_report_failure_demo.py` | **given** | Deliberate flaky and deliberate failing test for Tasks 6 and 7. Skipped by default. |
| `pytest.ini` | stub | `pythonpath`, `base_url`, markers. You extend it in Tasks 6 and 7. |
| `conftest.py` (below the marked line) | TODO list | Your fixtures and hooks. |
| `pages/*.py`, `pages/components/header.py` | TODO stubs | Comments say what each class must hold. |
| `utils/data_loader.py` | TODO stub | Your JSON helpers. |
| `data/users.json`, `data/checkout.json` | one example row each | You grow them in Task 4. |
| `requirements.txt` | given | pytest, pytest-playwright, pytest-rerunfailures, pytest-html, pytest-metadata |

---

## Staged tasks

**Golden rule:** after every sub-step run `pytest`, and commit only when it is green. If a step turns it red, undo the last change and take a smaller step (lesson `converting-scripts-to-pom.md` s.1, s.3).

### Task 1 - Analyse the flat suite (15 min)

Before you move any code, read `tests/test_shop_flat.py` and create a short `NOTES.md` with:

1. A table of the **pages** you can see (URL path and what a user does there) and the **components** shared by several pages.
2. Five concrete **smells** you found, each with a line count or example (for example "login block copied N times").
3. Which tests differ **only in data** (these become parametrized tests in Task 5).
4. For each of: a CSS selector, a username, a retry count, an assertion on the cart total, name the layer where it will live after the refactor (page / JSON / `pytest.ini` / test).

**Done when:** `NOTES.md` exists with all four parts.

### Task 2 - Extract page objects (40 min)

Replace the locators inside the tests with page objects, one page at a time, running the suite after each step. Do not touch the assertions' meaning.

- **2a. `LoginPage` (10 min).** Fill in `pages/login_page.py` with `username_input`, `password_input`, `login_button`, `error_message`, `open()`, `login_as()`. Use `page.get_by_test_id(...)`. This app uses the attribute `data-test`, so first add the `configure_test_id` session fixture to `conftest.py` (Task 2a in the file). Edit **only the login lines** of the flat tests to use `LoginPage(page)`. Run, commit.
- **2b. Remaining pages and the `Header` component (15 min).** Fill in the `InventoryPage`, `CartPage`, `CheckoutInfoPage`, `CheckoutOverviewPage`, `CheckoutCompletePage` stubs and `pages/components/header.py` (cart link and badge). Pages **compose** a `Header`; they do not inherit from it.
- **2c. `BasePage` and "navigation returns the next page" (15 min).** Create `BasePage` with `PATH` and `expect_loaded()`. Give each page its `PATH`. Make `login_successfully()` return an `InventoryPage`, `open_cart()` a `CartPage`, and so on, so a test can read as one chain. The `to_have_url` assertions from the flat tests **move into `expect_loaded()`**; they are not deleted.

**Rules:** locators exist only in `pages/`; no `assert` inside page methods (the readiness check in `expect_loaded` is the one deliberate exception); import only *forward* along the user journey (otherwise: circular imports).

**Done when:** all 7 original behaviours still pass using page objects, and no `[data-test=...]` string remains in `tests/`.

### Task 3 - Custom fixtures and hooks (30 min)

Move the repeated setup out of the tests. Fill in the TODO list in `conftest.py`:

- **3a.** `login_page(page)` returns `LoginPage(page).open()`. `inventory_page(login_page, users)` depends on it (composition) and returns a logged-in `InventoryPage`.
- **3b.** Session fixtures `users` and `customer`. Use inline dicts for now; Task 4 swaps in JSON.
- **3c.** Override `browser_context_args` to set a 1280x720 viewport. **Extend** the built-in value with `{**browser_context_args, ...}`; do not replace it.
- **3d.** Autouse fixture `log_test_boundaries(request)`: print `[setup ]` before `yield` and `[teardown]` after. Run `pytest -s -v -k purchase`, then `pytest --setup-show -k purchase`, and **write two sentences in `NOTES.md`** describing the order you see and why `inventory_page` is function-scoped, not session-scoped.
- **3e.** Hook `pytest_runtest_makereport` (hookwrapper): on a failed test **body** (`report.when == "call"`), take a screenshot into `reports/screenshots/`. You will see it work in Task 7.

**Done when:** the purchase test starts from `inventory_page` and `customer` fixtures; no test calls `page.goto` or logs in by hand.

### Task 4 - JSON test data (30 min)

1. Implement `utils/data_loader.py`: `DATA_DIR` built with `pathlib` from `__file__` (works from any working directory), `load_json(filename)`, and `cases(filename, key)` that wraps each row in `pytest.param(row, id=...)`.
2. Grow `data/users.json` to **3 valid users** and **4 invalid logins** (`locked-out-user`, `wrong-password`, `empty-username`, `empty-password`), each invalid row with `id`, `username`, `password`, `expected_error`.
3. Grow `data/checkout.json` to **3 validation cases** (missing first name, last name, postal code) and **4 sort cases** (name A-Z, Z-A, price low-high, price high-low).
4. Point the `users` and `customer` fixtures at the JSON files.

You can read the exact messages and sort results by running the flat tests, or by trying the app in a browser at `http://127.0.0.1:8791` while it runs (`python -m app.mock_shop`). Expected error strings include the prefix `Epic sadface: ` for login errors.

**Done when:** JSON files parse (no trailing commas), every row has a unique id, and no username, password or expected message is left in a test file.

### Task 5 - Slim down the tests with parametrization (20 min)

Rewrite the test files so the flat file disappears:

| New file | Contents |
|---|---|
| `tests/test_login.py` | `test_valid_users_reach_inventory` and `test_invalid_logins_show_error`, both parametrized from `users.json` |
| `tests/test_purchase.py` | the purchase journey as one readable chain (about 12 lines) |
| `tests/test_checkout_validation.py` | one test body parametrized over `validation_cases` |
| `tests/test_sorting.py` | one test body parametrized over `sort_cases` |

Add markers: `@pytest.mark.smoke` on the purchase test and the valid-login test, `@pytest.mark.regression` on the rest. Delete `tests/test_shop_flat.py` only when the new files cover every original behaviour.

**Done when:** `pytest -v` shows readable ids such as `test_invalid_logins_show_error[chromium-wrong-password]`, and `pytest -k wrong-password` runs exactly one test.

**Payoff check (do this):** add a new row to `users.json` (for example a whitespace-only username) **without editing any Python**. A new test must appear. Revert or keep it, but note in `NOTES.md` what the expected error was.

### Task 6 - Retries (15 min)

1. In `pytest.ini`, add to `addopts` (as one indented multi-line block): `--reruns 1 --reruns-delay 1 --only-rerun TimeoutError --only-rerun "net::ERR_"` (keep the existing `-m` expression).
2. Run the provided flaky test: `pytest -m retry_demo -v -rR`. You should see `RERUN` then `PASSED`.
3. Prove the filter works: temporarily make the flaky test raise `AssertionError("real bug")` on attempt 1 and show it is **not** retried, then revert it.
4. Debug mode: `pytest --reruns 0` runs without retries.
5. In `NOTES.md` answer: *a test passes on the second attempt every night; is it healthy, and what do you do?*

**Done when:** you can show the RERUN line, and an `AssertionError` is not rerun.

### Task 7 - HTML report with failure evidence (15 min)

1. Add `--html=reports/report.html --self-contained-html --junitxml=reports/junit.xml` to `addopts`.
2. In `conftest.py` add `pytest_html_report_title` (title: "QE Foundations - UI Regression Report") and a `pytest_configure` that adds `Project` and `Base URL` to the report metadata (`config.stash[metadata_key]` from `pytest_metadata.plugin`).
3. Run `pytest`, then open `reports/report.html`. Confirm the title, the metadata and the passing tests.
4. Run `pytest -m fails_on_purpose`. Open the report: the failing test must show an **embedded screenshot**, and `reports/screenshots/` must contain the PNG. Confirm it was **not** retried.
5. Take a screenshot of the report (one with the green run, one with the failure evidence) and put both in `docs/` for the submission. `reports/` itself stays out of Git (it is in `.gitignore`).

**Done when:** the HTML report opens offline with the title, metadata, and a screenshot attached to the deliberate failure.

---

## Stretch tasks (optional)

- **S1. Second component.** Add a `ProductCard` component (name, price, add button) on `InventoryPage` and use it in `add_product_to_cart`. Keep the tests unchanged.
- **S2. More data, no code.** Add three more rows (one per file) that each exercise a different error message, without editing Python. Then explain why ids matter when two rows share a name.
- **S3. Smoke subset.** Make `pytest -m smoke` finish in under 10 seconds and print the count.
- **S4. Traces.** Run `pytest --tracing retain-on-failure -m fails_on_purpose` and open the resulting trace with `playwright show-trace`. Describe in `NOTES.md` what the trace shows that the screenshot does not.
- **S5. Retarget the app.** Start a second copy of the app on another port and run `pytest --base-url http://127.0.0.1:9000` against it, without editing any page object. Explain why that works, and why real secrets never belong in JSON.
- **S6. Page-object critique.** Pick the one page method you are least sure about and write three sentences on whether it should return `self`, the next page, or a value.

---

## Hints (with lesson sections)

| If you are stuck on... | Read |
|---|---|
| Order of the refactor, "green after every step" | `converting-scripts-to-pom.md` s.1 (what is refactoring), s.3 (Step 0: green baseline), s.12 (checklist) |
| Finding pages and components in a flat script | `converting-scripts-to-pom.md` s.4 (Step 1) |
| Extracting locators and actions into classes | `converting-scripts-to-pom.md` s.5 (Step 2) |
| `BasePage` and the `Header` component | `converting-scripts-to-pom.md` s.6 (Step 3) |
| Methods that return the next page | `converting-scripts-to-pom.md` s.7 (Step 4) |
| Delivering pages through fixtures | `converting-scripts-to-pom.md` s.8 (Step 5); `fixtures-and-custom-fixtures.md` (scopes, `yield`, composition, overriding built-ins) |
| Removing magic values | `converting-scripts-to-pom.md` s.9 (Step 6) |
| Autouse fixture vs plugin hook, `pytest_runtest_makereport` | `hooks.md` (the two meanings of "hook") |
| `parametrize`, `pytest.param(id=...)`, loading JSON | `data-driven-testing-with-json.md` |
| `--reruns`, `--only-rerun`, the `flaky` marker | `test-retries.md` |
| `--html`, `--self-contained-html`, screenshots in reports | `playwright-reporting.md` |

(Note for the content team: only `converting-scripts-to-pom.md` was on disk when this exercise was written. Section numbers for the other lessons follow the instructor demo's references; titles are stable, so trainees can search by name.)

**Common pitfalls (read the error, then check here):**

- `fixture 'login_page' not found`: the fixture is not in a `conftest.py` that applies to your tests, or the name differs.
- `ModuleNotFoundError: pages`: `pythonpath = .` is missing in `pytest.ini`.
- `AttributeError: 'NoneType' object has no attribute ...`: a page method forgot to `return self` or return the next page.
- `get_by_test_id` finds nothing: `configure_test_id` fixture is missing (this app uses `data-test`).
- **`expect_loaded` never matches:** with `base_url` set, Playwright joins a *relative glob* such as `f"**{PATH}"` onto the base URL, so it can never match (the error message prints the odd expected URL: read it). The lesson's example uses that glob; use a compiled regex instead: `re.compile(rf"{re.escape(self.PATH)}$")`.
- Circular imports: only import pages that come *later* in the journey.
- `json.decoder.JSONDecodeError`: trailing comma or a comment in a JSON file.
- `unrecognized arguments: --reruns`: `pytest-rerunfailures` not installed in the active virtual environment.
- Report picture missing: the hook must be named exactly `pytest_runtest_makereport` (a typo is silently ignored).
- Port already in use: another process owns 8791. Stop it, or run with `--base-url` pointing at your own copy and change `APP_PORT` in `conftest.py`.

---

## Project 1 - QE Foundations milestone

**Do the same refactor on your own Project 1 UI tests.** Treat Tasks 2 to 7 as a checklist you now apply to real code.

> **Assumption (flag if wrong):** the curriculum has not yet fixed what the Project 1 application is, so this brief is deliberately generic. "Your app" means whichever web UI your Project 1 tests drive. If your Project 1 currently has no UI tests, build the 3-page version below against whatever UI you chose, or ask your instructor which public demo site to use.

**Minimum milestone (commit this):**

1. A "before" commit of your existing Project 1 UI tests, run green once. Record the hash.
2. **At least 3 page classes** plus a `BasePage`, with locators only in `pages/`.
3. **One shared `conftest.py`** with at least one custom page fixture and one autouse fixture or hook.
4. **One JSON file with 3 or more rows** feeding at least one parametrized test (login variants, search terms, form validation...).
5. **Retries configured in `pytest.ini`**, filtered so assertion failures are not retried.
6. An **HTML report** generated by a normal `pytest` run. Add a screenshot of it to your repo's README.
7. An "after" commit; same behaviour, better structure. Record both hashes.

**Suggested order for your own app (about 60-90 min of the 2-3 h, depending on how many tests you have):**
list pages and shared components -> `LoginPage`/entry page first -> remaining pages -> fixtures -> pull out the 3 most repetitive data sets into JSON -> retries -> report.

**Self-check before you submit:**

- Which of my tests differ only in input values? (They should be parametrized.)
- Do any test files still contain a selector or a hard-coded URL?
- Are there any secrets in JSON? (There must not be: use environment variables for real credentials.)
- Would a teammate know where to add a new page, a new data row, and a new fixture?

If your Project 1 is finished early, the lab in `starter_code/` is complete enough to submit on its own; the milestone then stays as your homework for the day.

---

## Definition of Done

**Lab (`starter_code/` refactored):**

- [ ] Baseline commit exists and showed `7 passed` before any change.
- [ ] `tests/test_shop_flat.py` is gone; every original behaviour is still checked.
- [ ] `pages/` has `BasePage`, a `Header` component and 6 page classes; navigation methods return the next page; no assertions in page methods (except `expect_loaded`).
- [ ] No selector, URL, credential or expected message appears in any file under `tests/`.
- [ ] `conftest.py` holds `configure_test_id`, `login_page`, `inventory_page`, `users`, `customer`, an extended `browser_context_args`, `log_test_boundaries`, and `pytest_runtest_makereport`.
- [ ] Data lives in JSON with unique ids; `pytest` shows at least **15 passing tests** and `pytest -k wrong-password` selects one.
- [ ] `pytest.ini` has retries (filtered) and report options; `pytest -m retry_demo -rR` shows a RERUN; `pytest -m fails_on_purpose` fails once, is **not** rerun, and the report shows a screenshot.
- [ ] `pytest` runs headless and green from a fresh clone after `pip install -r requirements.txt`.
- [ ] `NOTES.md` answers Tasks 1, 3d, 5 (payoff check) and 6.

**Project 1 milestone:** items 1 to 7 above.

---

## Submission

Submit a link to your repository (or a zip) containing:

1. The refactored `starter_code/` folder (without `.venv/`, `reports/`, `__pycache__/`).
2. `NOTES.md`.
3. `docs/report-green.png` and `docs/report-failure.png`.
4. A `SUBMISSION.md` with: the **before and after commit hashes** for the lab, the same two hashes for Project 1, the exact command you used to run everything, and the output summary line of your final `pytest`.
5. Your Project 1 refactor (same repository on a branch, or a link to it).

Do not commit secrets. Do not commit `reports/`.

---

## Rubric (100 points)

| Area | Points | Full marks when |
|---|---|---|
| Safe refactor process | 10 | Baseline commit, small green commits visible in history, behaviour unchanged |
| Page objects | 20 | `BasePage`, `Header` component, 6 pages; locators only in `pages/`; navigation returns next page; no stray assertions |
| Fixtures and hooks | 15 | Composition fixtures, correct scopes, extended (not replaced) `browser_context_args`, autouse `yield`, working `makereport` hook |
| JSON data-driven tests | 15 | Loader works from any cwd, unique readable ids, no data left in tests, payoff check done |
| Retries | 10 | Filtered reruns, RERUN demonstrated, assertion failure shown **not** retried, written answer |
| Report | 10 | Self-contained HTML with title/metadata and an embedded failure screenshot; JUnit XML produced |
| Project 1 milestone | 15 | All 7 minimum items; before/after hashes; applied to real tests |
| Communication | 5 | Clear `NOTES.md` and `SUBMISSION.md`; commit messages describe each step |
| **Stretch (bonus)** | up to +10 | Up to 2 points per completed stretch, capped at 10 |

---

## Time estimates

| Part | Minutes |
|---|---|
| Setup and baseline | 10 |
| Task 1: analysis | 15 |
| Task 2: page objects | 40 |
| Task 3: fixtures and hooks | 30 |
| Task 4: JSON data | 30 |
| Task 5: parametrize and slim tests | 20 |
| Task 6: retries | 15 |
| Task 7: report | 15 |
| **Lab subtotal** | **175 min budget (about 2 h 55 min); the demo covered the same moves, so many trainees will be faster** |
| Project 1 milestone | 60-90 (use the lab's remaining time, or finish as homework) |

If you are behind at the 2-hour mark, skip Task 1 point 2 and all stretch tasks, and move on to the Project 1 milestone with whatever you have working.

---

## Instructor notes

- `solution/` is a complete reference refactor; run `pytest` there (15 passed, 2 deselected). See `solution/README.md` for the mapping from flat tests to the new layout and for marking notes.
- The app is a local mock, so no network is required. Port 8791 is fixed; change `APP_PORT` in `conftest.py` and `base_url` in `pytest.ini` together if it clashes.
- Cypress is intentionally not used; it is tomorrow's topic.
