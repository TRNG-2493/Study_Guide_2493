# Exercise: Automate Table, Frame and Tab Scenarios (Week 5, Tuesday)

**Mode:** A (code lab) | **Format:** Individual | **Time:** 2-3 hours | **Language:** Python, Playwright sync API, pytest as the test runner

**Project lane:** Project 1 - QE Foundations (see "Project 1 - QE Foundations milestone" below)

---

## 1. Scenario

You have just joined the QE team of **QE Practice Shop**, a small order-management site. Support is complaining about
regressions in five areas: the **orders table**, the **checkout payment form** (an iframe inside an iframe), the
**Terms and Help windows**, the **delivery date picker** and the new **fulfilment board** (web components). Finance also
wants the **CSV export** and **CSV import** verified.

Your job is to write reliable Playwright tests for each area, finishing with one end-to-end business flow that
combines several of them. The site runs locally from the standard library, so everything works offline and is
deterministic. This is the same kind of work you will do against your Project 1 application.

## 2. What you will practise

| Lesson (written/2-tuesday/) | Where you use it |
| --- | --- |
| `web-tables.md` | Task 1 |
| `frames-and-nested-frames.md` | Task 2, Task 7 |
| `multiple-tabs-and-windows.md` | Task 3, Task 7 |
| `date-pickers.md` | Task 4 |
| `shadow-dom.md` | Task 5 |
| `file-upload-and-download.md` | Task 1a, Task 6 |
| `dynamic-element-handling.md` | every task (condition-based waits, web-first assertions) |
| `navigation-events.md` | Task 3 (same-tab link, `wait_for_url`) |

Everything you need is in Monday's and Tuesday's written lessons and in the instructor demo
(`demos/2-tuesday/`). There is **nothing from Wednesday or later**: no fixtures, no `conftest.py`, no Page Object
classes, no JSON-driven tests, no Cypress.

## 3. Prerequisites

- Python 3.10 or newer.
- You attended the Tuesday demo and read the eight Tuesday lessons (or at least the sections cited in the hints).
- Monday skills: role/label/text locators, `expect(...)` assertions, `fill`, `click`, dialogs.

## 4. Setup (about 10 min)

```bash
cd exercise/2-tuesday/starter_code
python -m venv .venv
# macOS/Linux:  source .venv/bin/activate        Windows:  .venv\Scripts\activate
pip install -r requirements.txt
playwright install chromium
```

Explore the app once by hand (optional but recommended, 5 min):

```bash
python app.py            # open http://127.0.0.1:8000/ and click through every page; Ctrl+C to stop
```

Run the tests:

```bash
pytest -v                 # everything
pytest -v -k test_1a      # one test
pytest -x -v              # stop on the first failure
```

**Expected result of the unmodified starter:** `9 failed, 4 skipped`. Every failure is `NotImplementedError: TODO: ...`;
that is by design. The four skipped tests are the stretch tasks. Your goal is `9 passed` (core) and then, if you
have time, `13 passed`.

Watching the browser: in `support.py` temporarily change `p.chromium.launch()` to
`p.chromium.launch(headless=False, slow_mo=300)`. Change it back before you submit.

### Files in `starter_code/`

| File | Purpose | Edit? |
| --- | --- | --- |
| `app.py` | the practice site (the application under test) | no |
| `support.py` | `open_page()` helper: starts the app, opens a fresh headless browser context | no |
| `test_tuesday_lab.py` | skeleton tests and helper-function stubs with TODOs | **yes** |
| `PROJECT1_MILESTONE.md` | worksheet for the milestone | **yes** |
| `requirements.txt` | dependencies | no |

### Pages of the practice site

| Path | Contents |
| --- | --- |
| `/orders` | table of 12 orders, 5 per page, sortable headers, search box, **Refund** row action, summary line, **Export CSV** download |
| `/checkout` | **Terms of Service** link (new tab), **Help** button (popup), card form **iframe** that contains a **nested** bank-verification iframe (added about half a second later), **Place order** button |
| `/delivery` | native date input (**Invoice date**) and custom calendar (**Delivery date**) that reads "today" from the browser clock |
| `/components` | `<order-card>` web components (open shadow DOM) and an `<audit-badge>` (closed shadow DOM, stretch) |
| `/import` | CSV upload input (`accept=".csv"`) plus a button that creates a file input on demand (stretch) |

Facts worth knowing: the OTP code that the bank frame accepts is `123456`; a valid card number is 16 digits (spaces allowed).
The table headers are `<th scope="col">`, so `get_by_role("columnheader", ...)` works (see demo Appendix A, item 1).
Data on `/orders` lives in the browser, so reloading the page resets a Refund.

## 5. Ground rules

1. Plain `def test_...()` functions and plain helper functions only.
2. **No `time.sleep`, no `page.wait_for_timeout`.** Wait for conditions.
3. No positional selectors (`tr[3]/td[2]`, `nth(2)` on rows). `nth(i)` is fine for iterating over a list you have already counted.
4. Prefer `get_by_role`, `get_by_label`, `get_by_text`, `get_by_placeholder`; CSS only where the lessons allow it (shadow hosts, table header cells).
5. Every test asserts something about the outcome, not only that clicks did not crash.
6. Keep the "register first, then act" pattern for popups, downloads, responses and file choosers.

---

## 6. Core tasks (about 2 h 20 min)

Work in order; each task builds on the habits of the previous one. Time estimates include reading the hints.

### Task 1 - Web tables (30 min) - `/orders`

Skeleton: `read_visible_rows`, `collect_all_rows`, `download_orders_csv`, `test_1a`, `test_1b`, `test_1c`.

**1a (15 min) The UI must equal the export.**
Read every row of the paginated table into a list of dictionaries, download the CSV, and prove they match. Then
recompute the "pending" summary yourself.

Acceptance criteria:
- The test waits for the first page to be rendered (5 body rows) before reading.
- 12 rows are collected across 3 pages and all 12 order numbers are distinct (so no page was read twice).
- UI rows equal CSV rows (same order, same values).
- The summary text equals the Python-computed `"<n> pending orders, total <amount>"`, using `Decimal`.

**1b (10 min) Sorting.** Sort by Customer and by Total (descending) and verify the order of **all 12** rows, not only page 1.
Customer names use the same case-insensitive rule as the UI; totals are compared as numbers.

**1c (10 min) Search and a row action.** Search for `ann` (it matches "Ann Lee" and "Joanna Kim"), refund exactly one
row, and verify the row changed. Include the empty-search message.

Hints:
- `web-tables.md`, Concept 3 (three levels of locators), Concept 4 (tables to dictionaries), Concept 5 (waiting for table data), Concept 6 (sorting), Concept 7 (filtering), Concept 8 (pagination), Concept 9 (row actions), Example 4 (the "Ann" problem), Example 8 (pagination pattern).
- `count()`, `all_inner_texts()` and `inner_text()` read **once**; gate them with `expect(...).to_have_count(...)`.
- **Pitfall from the demo (Appendix A, item 2):** after clicking Next, do **not** wait with `expect(first_row).not_to_have_text(first_row.inner_text())`. For multi-cell rows this passes instantly. Compare a single cell (for example the first `td`).
- **Pitfall (Appendix A, item 1):** use `get_by_role("columnheader", name=...)` only because these headers have `scope="col"`; on bare `<th>` Chromium may report role `cell`.
- The body rows exclude the header row if you use `tbody tr`; `get_by_role("row")` includes it.
- Demo reference: `code/demo_playwright_advanced_interactions.py`, sections 2c, 2e, 2f, 2g.
- Download hints: `file-upload-and-download.md`, Concept 7 (download basics), Concept 8 (verify content), Example 4 and Example 7 (UI vs export).

### Task 2 - Frames and nested frames (20 min) - `/checkout`

Skeleton: `pay_in_frames`, `test_2_nested_frames_payment`.

The card number field is inside an iframe; the one-time-code field is in a second iframe **inside the first**, and
appears about half a second after you click Continue.

Acceptance criteria:
- A page-level locator for "Card number" finds nothing (count 0), proving you understand why.
- Negative path: an invalid card shows "Invalid card number" **inside the frame**.
- A wrong one-time code shows "Wrong code" and leaves the main page at "Payment: not started".
- A correct code results in "Verified card ending 4242" in the card frame **and** "Payment: approved" on the main page.
- No `time.sleep`, no `switch_to`-style thinking: every locator names its own frame chain.

Hints:
- `frames-and-nested-frames.md`: Concept 2 (why page locators cannot see in), Concept 3 (`frame_locator`), Concept 4 (choose the iframe selector, prefer `title`), Concept 5 (nested), Pitfall about frames appearing late (Scenario 4).
- Chain `frame_locator(...).frame_locator(...)`; do not use `page.frame(...)` for the late iframe because it is evaluated immediately and returns `None`.
- Demo reference: section 1b, 1c, 1e.

### Task 3 - Multi-tab and popup flow (15 min) - `/checkout`

Skeleton: `accept_terms`, `test_3_terms_tab_and_popups`.

Acceptance criteria:
- The Terms link has `target="_blank"` (attribute assertion, no click needed).
- The Help popup (opened with `window.open`) is captured, asserted, and closed; the opener page remains usable; the context page count is 2 while it is open.
- In the Terms tab, "I agree" closes the tab; the opener shows "Terms: accepted"; one page remains.
- The "View orders" link opens in the **same** tab: you wait for the URL and never wrap it in `expect_popup`.

Hints:
- `multiple-tabs-and-windows.md`: Concept 1 (browser, context, page), Concept 2 (no "switch to window"), Concept 3 (register first, then act), Concept 4 (`expect_popup` vs `expect_page`), Concept 9 (pop-up that closes itself: `popup.expect_event("close")`), Concept 10 (same-tab vs new-tab).
- `page.context.pages` lists every tab in the context.
- `navigation-events.md`, Concept 4 (`wait_for_url`).
- Demo reference: section 4a, 4b, 4d, 4e.

### Task 4 - Date picker (15 min) - `/delivery`

Skeleton: `pick_delivery_date`, `test_4_date_pickers`.

Acceptance criteria:
- The browser clock is fixed at 14 March 2025 **before** the page loads, and the page says "Today is 2025-03-14".
- The native "Invoice date" input is filled with an ISO date; an impossible date (`2025-02-30`) raises a Playwright error containing "Malformed value".
- `pick_delivery_date` can move **forward** (June 2025) and **backward** (April 2025) and clicks the right day (day 2 must not click day 20 or 12).
- March 13, 2025 is disabled and March 14, 2025 is enabled.

Hints:
- `date-pickers.md`: Concept 1 (three kinds), Concept 2 (native `fill` with ISO), Concept 4 (custom calendar, month arithmetic), Concept 6 (disabled dates), Concept 9 (`page.clock`), Example 3 (reusable helper), Example 5 (clock).
- Build the accessible name with `target.day`, not `%d` (zero-padding), and use `exact=True`.
- `pytest.raises(PlaywrightError, match="...")` is already imported for you.
- Demo reference: section 3a, 3b, 3d, 3e.

### Task 5 - Shadow DOM (10 min) - `/components`

Skeleton: `test_5_shadow_dom_cards`.

Acceptance criteria:
- You demonstrate the boundary: the browser's `querySelector` returns `None`, Playwright's CSS locator counts 3, XPath counts 0.
- You act on **one** card by scoping to its host element (filter by its text), then assert that only that card changed.

Hints:
- `shadow-dom.md`: Concept 1 (light DOM, shadow DOM, iframe), Concept 4 (why Playwright pierces), Concept 5 (what does not pierce), Example 1 and Example 5.
- Role locators work inside open shadow roots; the problem is the three identical "Mark shipped" buttons, so filter the host first.
- Demo reference: section 5a, 5b, 5d.

### Task 6 - File download and upload round trip (15 min) - `/orders` then `/import`

Skeleton: `test_6_export_then_import_round_trip`.

Acceptance criteria:
- Export the CSV (12 rows) and keep the saved file.
- Upload that same file; the server answers HTTP 200 and the page says "Imported 12 orders from orders.csv". Register the response wait **before** the upload action.
- Negative: an in-memory `malware.exe` is rejected by the **server** (HTTP 415, "Rejected: only .csv files are accepted") even though the input says `accept=".csv"`.

Hints:
- `file-upload-and-download.md`: Concept 2 (`set_input_files`), Concept 3 (in-memory files), Concept 6 (verify the upload), Concept 7-8 (downloads), Concept 11 (security: `accept` is not validation), Example 8 (upload with server confirmation), Example 9 (validation test).
- In-memory file: `{"name": ..., "mimeType": ..., "buffer": b"..."}`.
- `tempfile.TemporaryDirectory()` is already imported; never hard-code absolute paths.
- Demo reference: section 8a, 8c, 8f.

### Task 7 - Project 1 milestone: one end-to-end flow (15 min) - `/checkout`

Skeleton: `test_7_milestone_checkout_end_to_end` (reuses your `accept_terms` and `pay_in_frames` helpers).

Business story: *"A customer accepts the terms in a new tab, pays through the nested card frames, and places the
order. The order must not be placeable before both are done."*

Acceptance criteria:
- "Place order" starts disabled, stays disabled after terms only, and becomes enabled after payment.
- Clicking it triggers `POST /api/place-order`; you assert HTTP 201 and read the order id from the JSON.
- The UI shows "Order confirmed: <that same id>" (the response is not enough; assert the DOM too).
- The test reads top to bottom as a business story; waits are all condition-based.

Hints: `dynamic-element-handling.md` Concept 4 (web-first assertions), Concept 13 (`expect_response`, then assert the DOM);
demo Phase 9 (capstone) and `section_9_capstone`.

### Task 8 - Milestone worksheet (10 min) - `PROJECT1_MILESTONE.md`

See the next section.

---

## 7. Project 1 - QE Foundations milestone

> **ASSUMPTION (flag for the instructor):** the CMA log requires the day's Project 1 milestone to be in the
> exercise brief, but it does not describe what the Project 1 application is. The milestone below is therefore
> phrased generically so it works whether Project 1 is a web app, an API with a UI, or something else. Replace
> "my app" with your Project 1 system under test. If your Project 1 has no browser UI, do the worksheet anyway and
> describe the closest UI-like surface you can test, or ask your instructor.

**Today's milestone: "UI interaction coverage plan plus two automated flows".**

1. **Inventory (worksheet section 1).** For each of today's six topics (tables, frames, new tabs/popups, date pickers,
   shadow DOM, file upload/download), name the page in *your* Project 1 app where it appears, the locator strategy you
   would use, and the condition you would wait for.
2. **Independent oracles (worksheet section 2).** For two flows, name a source of truth that is not the screen
   (export file, API response, database row, Python calculation). Task 1a and Task 6 are your models.
3. **Two tests for your own app (worksheet section 3).** If your Project 1 app is reachable now, implement and run two
   small tests using today's techniques (for example "table total equals export" and "policy link opens a new tab"). Keep
   them as plain functions in a `project1/` folder next to this exercise. If your app is not reachable yet, write each
   test as a numbered step list in the worksheet and mark it "not yet automated".
4. **Linkage.** Tomorrow (Wednesday) you will refactor these flat tests into fixtures and Page Objects, so keep them
   small and runnable.

Deliverables for the milestone: the filled-in `PROJECT1_MILESTONE.md` (required) plus the two tests (required if the app is reachable).

---

## 8. Stretch tasks (optional, up to 30 min; all are skipped in the starter)

| ID | Task | Lesson |
| --- | --- | --- |
| S1 | Closed shadow root on `<audit-badge>`: show `shadowRoot` is `None`, click the host, then use `add_init_script` to force roots open and click the real button | `shadow-dom.md` Concept 9, Example 7 |
| S2 | `expect_file_chooser` for the "Pick file..." button; assert `is_multiple()` is `False` | `file-upload-and-download.md` Concept 4, Example 3 |
| S3 | Ctrl/Cmd+Click the Terms link and capture the background tab with `context.expect_page()` | `multiple-tabs-and-windows.md` Concept 4, Example 3 |
| S4 | Upload an in-memory CSV with the wrong header and assert HTTP 422 | `file-upload-and-download.md` Example 9 |

Remove the `@pytest.mark.skip` line when you start one.

## 9. Common problems

| Symptom | Likely cause | Fix |
| --- | --- | --- |
| `TimeoutError ... get_by_label("Card number")` | The field is inside an iframe | `frame_locator(...)` |
| Strict mode violation on "Mark shipped" | Three identical buttons | filter the `order-card` host first |
| Pagination loop reads the same rows twice | Waited on whole-row text | compare one cell, see Task 1 hints |
| `expect_popup` times out on "View orders" | That link opens in the same tab | `wait_for_url` |
| Terms tab URL is `about:blank` | Read `.url` too early | `expect(tab).to_have_title(...)` or `to_have_url(...)` |
| Calendar clicks the wrong day | Substring name match | `exact=True`, build the label with `target.day` |
| Clock fix has no effect | Set after `goto` | call `page.clock.set_fixed_time` **before** `goto` |
| Download file missing | Context closed, temp folder gone | `save_as` before leaving the `with` block |

## 10. Definition of Done

- [ ] `pytest -v` in `starter_code/` shows **9 core tests passed** (stretch optional: up to 13).
- [ ] Runs headless from a clean checkout with only `pip install -r requirements.txt` and `playwright install chromium`.
- [ ] No `time.sleep`, no `wait_for_timeout`, no positional selectors, no fixtures/conftest/Page Objects.
- [ ] Every helper has a one-line docstring explaining what it does; every test asserts an outcome (including at least one negative path in Tasks 2, 4 and 6).
- [ ] `support.py` and `app.py` unchanged (and `headless` restored if you changed it).
- [ ] `PROJECT1_MILESTONE.md` completed; Project 1 tests added if your app is reachable.
- [ ] You can explain, in two sentences each: why `frame_locator` replaces "switching", why we register `expect_popup` before the click, and why `accept=".csv"` is not security.

## 11. Submission

1. Commit your work on a branch named `week5-tuesday-<yourname>` containing `starter_code/test_tuesday_lab.py`, `starter_code/PROJECT1_MILESTONE.md` (and `project1/` if used).
2. Paste the final `pytest -v` output (or a screenshot) into the pull request description.
3. In the PR description add three lines: what was hardest, one flaky-test risk you avoided, one thing you would ask a developer to add (for example a `data-testid`).
4. Do not commit `.venv/` or downloaded files.

## 12. Rubric (100 points)

| Criterion | Points | Full marks when |
| --- | --- | --- |
| Tables (Task 1) | 20 | gated reads, all 12 rows across pages, UI equals export, correct sorting checks, exact-cell row action |
| Frames (Task 2) | 12 | chained `frame_locator`, negative path, no stale/`None` frame objects |
| Tabs and popups (Task 3) | 12 | register first, popup closed, `close` event handled, same-tab link not wrapped in `expect_popup` |
| Date picker (Task 4) | 10 | clock before `goto`, ISO `fill`, forward/backward helper with `exact=True`, disabled dates checked |
| Shadow DOM (Task 5) | 6 | scoped by host, other cards asserted unchanged |
| Files (Task 6) | 10 | register-first, round trip, server-side rejection tested |
| Milestone flow (Task 7) | 10 | story-like test, status code plus DOM assertion |
| Wait discipline and locator quality | 10 | zero sleeps, role-first locators, no positional selectors |
| Project 1 worksheet | 10 | complete, specific to the trainee's app, oracles named |
| Stretch | bonus up to +10 | 2.5 points per passing stretch test |

Grading bands: 90+ excellent, 75-89 meets expectations, 60-74 needs another pass, below 60 repeat with a mentor.

## 13. Time estimate

| Block | Minutes |
| --- | --- |
| Setup and tour of the app | 10 |
| Task 1 Tables | 30 |
| Task 2 Frames | 20 |
| Task 3 Tabs and popups | 15 |
| Task 4 Date picker | 15 |
| Task 5 Shadow DOM | 10 |
| Task 6 Files | 15 |
| Task 7 Milestone flow | 15 |
| Task 8 Worksheet (+ optional Project 1 tests) | 10 |
| **Core total** | **140 (2 h 20 min)** |
| Stretch (optional) | up to 30 |
| **Maximum** | **170 (2 h 50 min)** |

Project 1 tests against your own app, if you write them, are expected to fit in the stretch window.

## 14. Instructor notes (not for trainees)

- Solution: `solution/test_tuesday_lab.py` (run with `pytest solution -v` from this folder; it imports the app from `starter_code/`) and an example worksheet `solution/PROJECT1_MILESTONE_example.md`.
- Withhold `solution/` from trainees until the review.
- The app uses `rel="opener"` on the Terms link because browsers apply `noopener` to `target="_blank"` links, which would stop the tab from messaging its opener.
