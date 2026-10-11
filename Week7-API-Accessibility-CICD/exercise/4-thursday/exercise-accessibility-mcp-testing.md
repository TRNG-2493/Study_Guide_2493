# Thursday Pair Project: Audit ShopFront for Accessibility, Automate the Scan, Meet MCP

**Week 7 / Day 4 | Collaborative pair programming | 2-3 hours | Deliverable: one shared repo/branch + defect reports + a short retrospective**

## 1. Objectives
By the end of this session your pair will have:
1. Audited a page by hand (keyboard-only and screen-reader passes) and logged findings.
2. Added an automated axe scan to the Project 2 framework as pytest tests (marker `a11y`), parametrized over page states, with a baseline of known issues.
3. Turned raw findings into 5+ professional defect reports, de-duplicated by root cause, each mapped to a WCAG success criterion and POUR principle.
4. Fixed 3+ defects in a copy of the page and proved it with before/after scan counts.
5. Written your first MCP server tests (4 tests, pytest-asyncio).

This project **synthesises the week**: API mocking (Mon-Wed), the layered Project 2 framework (Wednesday), accessibility and MCP (Thursday). Everything you need is in Monday-Thursday material. (Friday teaser: tomorrow this repo goes into a GitLab CI pipeline, so keep your tests deterministic and offline.)

## 2. Time box and swap schedule (3 hours; trim blocks 5-6 for a 2-hour session)
Swap **driver** and **navigator** every 30 minutes. A timer is the navigator's job to start, the new driver's job to say "swapping" out loud. Commit before every swap.

| Block | Clock | Driver | Navigator | Focus |
|---|---|---|---|---|
| 1 | 0:00-0:30 | A | B | Setup (15 min), then task 1 keyboard pass |
| 2 | 0:30-1:00 | B | A | Task 1 screen-reader pass; finish the findings log |
| 3 | 1:00-1:30 | A | B | Task 2 axe scan tests and baseline |
| 4 | 1:30-2:00 | B | A | Task 3 defect reports (5+) |
| 5 | 2:00-2:30 | A | B | Task 4 fixes + re-scan |
| 6 | 2:30-3:00 | B | A | Task 5 MCP tests, retrospective, final push |

For 2 hours: do setup, tasks 1-3 and a 3-fix task 4 in four blocks; task 5 becomes a stretch.

## 3. Pair roles and communication norms
| | Driver | Navigator |
|---|---|---|
| Hands | Only person typing, clicking and running the screen reader | Hands off the keyboard |
| Job | Implements; thinks out loud; asks when stuck | Reviews each step, watches the bigger picture, looks things up (WCAG, axe docs, written lessons), keeps the timer and the task list |
| Checks | "Does this compile/run?" | "Does this match the task and the test I would write first?" |

Rules:
- **Swap on time**, even mid-task. Leave a one-line `TODO(next):` comment so the new driver can continue.
- The driver may not code silently; the navigator may not dictate characters. Say intent ("assert the rule ids per state"), not keystrokes.
- Disagree with evidence (run it, read the docs), not volume. If stuck for 10 minutes, ask the instructor together.
- Both names appear in `git log` (alternate commits, or use `Co-authored-by:`). Commit message: `a11y: add baseline test (driver A / nav B)`.
- Each block ends with a 1-minute check-in: what is done, what is next, is the navigator still engaged?

## 4. Setup (block 1, 15 minutes)
```
cd starter_code
pip install -r requirements.txt --break-system-packages   # lab image; Chromium already installed, do NOT run `playwright install`
pytest -q                                                 # expect: all tests SKIPPED, no errors
```
Create ONE shared repo/branch (`git init`, branch `thursday/<pairname>`), commit the starter, and push. Open `storefront/index.html` in a browser.

The starter is an **overlay on your Wednesday framework** (see section 12). It stands alone for today so that you can work even if your Wednesday repo is incomplete. Key rules:
- Do **not** add a `conftest.py` under `tests/a11y/`; the `page` fixture lives in `tests/a11y/a11y_helpers.py` (a second conftest would shadow your framework's root conftest).
- Tests never need a running server: the browser request to the API is intercepted with `page.route()`, the same mocking idea as Wednesday. `project2_api_server.py` (port 8000) is included for the stretch goals and the MCP server's real data source.
- Do not run `playwright install`. If Chromium is somewhere unusual, set `CHROMIUM_PATH`.

## 5. Scenario: ShopFront
ShopFront is a small storefront. It lists the products from the Project 2 API (`GET /items`), lets the user add items to a cart, enter a promo code, search, and subscribe to a newsletter. The page was built in a hurry and ships with **planted accessibility defects**. Your client wants (a) a human audit, (b) an automated guard so it never gets worse, (c) a prioritised defect list, (d) the worst problems fixed, and (e) a first look at exposing the same items to AI agents through MCP.

Three UI states exist for scanning: `loaded` (products shown), `form-error` (invalid newsletter submit), `api-down` (the API failed). Helper `open_state(page, variant, state)` puts the page in each of them.

## 6. Tasks

### Task 1: Manual audit (60 min, blocks 1-2)
**1a. Keyboard-only pass (Tab, Shift+Tab, Enter, Space, Esc; put the mouse away).** For each state, check: can you reach and operate every control? Is the focus order logical? Is focus always visible? Can you always leave a control? Does anything happen that a keyboard user cannot trigger?

**1b. Screen-reader pass (NVDA on Windows or VoiceOver on macOS).** Listen to the page top to bottom, then navigate by headings, landmarks and form fields. Ask: does every image/control have a name? Is the page title and language announced? Are the form fields labelled? When you submit bad data, do you hear what went wrong? (No screen reader available? Use the browser's accessibility tree in DevTools and Chromium's "Elements > Accessibility" pane, and say so in the retrospective.)

Record every finding in `templates/findings-log.csv` (copy it to `findings-log.csv` at the repo root). **Do not run axe yet**: the point is to learn what only a human can find. Minimum: 8 findings, at least 3 keyboard and 3 screen-reader.

### Task 2: Automated axe scan as pytest tests (45 min, block 3)
Implement `tests/a11y/test_axe_scan.py` (replace the TODOs; use Playwright for Python and `axe-playwright-python`):
1. `scan(page)` returns axe violations; `save_report(name, violations)` writes JSON to `reports/a11y/`.
2. `test_bad_page_has_known_violations`, parametrized over the three states, asserting the rule ids you expect in each. Some rules differ per state: find out which and why.
3. A **baseline** (`tests/a11y/baseline.json`: rule id to max node count). `test_no_new_violations_vs_baseline` passes on today's known issues and fails on anything **new or worse**.
4. `test_baseline_catches_a_regression`: inject a new violation with `page.evaluate` and prove the baseline check catches it.
5. Mark everything `@pytest.mark.a11y` and run with `pytest -m a11y`.

Then compare with your findings log: add a column value in `axe_flagged` (yes / no) for each finding. Which of *your* findings did axe miss?

### Task 3: Defect analysis (30 min, block 4)
Write **5+ defect reports** in `defects/DR-001.md ...` from `templates/defect-report-template.md`. Each needs: WCAG success criterion and level, POUR principle, severity with a justification (impact x frequency x workaround), numbered steps, expected vs actual, evidence, and a concrete fix. Rules:
- **De-duplicate by root cause.** Six `image-alt` nodes with one cause in the same render function are ONE report listing six nodes.
- At least **two** reports must come from findings axe did **not** report.
- Do not copy axe's help text as the title; name the user impact ("Add to cart cannot be reached by keyboard").

### Task 4: Fix and prove (30 min, block 5)
Copy the page: `cp -r storefront storefront_fixed` (never edit the original). Fix **at least 3** defects (more is welcome). In `test_axe_scan.py` add `test_fixed_page_has_zero_violations` for the rules you fixed (parametrized over states) and `test_before_after_counts`, which writes `reports/a11y/summary.json` with the node counts for `bad` vs `fixed`. Re-test manually the defects that axe cannot prove (keyboard, announcements).

### Task 5: MCP intro (30 min, block 6)
The skeleton `mcp_server/items_mcp_server.py` exposes the Project 2 items to AI clients through the MCP Python SDK 1.x (`mcp<2`). It has an injectable data source, so tests never need the real API.
1. Implement the three TODOs: tool `get_item(item_id: int)`, tool `search_items(category)`, resource `items://catalog`.
2. In `tests/mcp/test_items_mcp.py` write **4 tests** with pytest-asyncio: (1) `tools/list` schema (names, description, `item_id` is a required integer; validate a good and a bad payload with `jsonschema`), (2) a successful `get_item` call, (3) an error call (unknown id) which must come back as an `isError` result rather than a raised exception, (4) reading the `items://catalog` resource.
3. Never `print()` in a stdio server.

### Stretch goals
- Automate the keyboard findings in `tests/a11y/test_keyboard.py` (trap, div-button, focus visibility, announced errors) so each proves the defect on the bad page and the fix on the fixed page.
- Add a test using the real `ApiItemsSource` against `project2_api_server.py` (marker `live`, skipped when the API is down).
- Add `search_items` tests (filter by category) and an MCP prompt.
- Add a colour-contrast check at 200% zoom / forced-colors emulation, and review another pair's defect reports.

## 7. Deliverables
1. **Shared repo/branch** (`thursday/<pairname>`) with commits from both partners, containing: `storefront_fixed/`, `tests/a11y/`, `tests/mcp/`, `mcp_server/`, `reports/a11y/`, `findings-log.csv`.
2. **Defect reports** `defects/DR-001.md ...` (5+).
3. **Retrospective** `RETROSPECTIVE.md` from `templates/retrospective-template.md` (one per pair, both names).

## 8. Definition of Done
- [ ] `pytest -q` passes from a clean checkout with no server running and no network; `pytest -m a11y` and `pytest -m mcp` both select tests.
- [ ] Findings log has 8+ findings from both passes; none of them copied from axe output.
- [ ] Baseline test passes on the bad page and demonstrably fails on a new violation.
- [ ] 5+ defect reports complete and de-duplicated; 2+ are manual-only findings.
- [ ] 3+ defects fixed in a copy; `summary.json` shows before > after; fixed page scans clean for the fixed rules.
- [ ] 4 MCP tests pass (schema, success, error, resource).
- [ ] Both partners drove at least 3 blocks (swap log in the retrospective).
- [ ] No `__pycache__`, `.pytest_cache` or secrets committed.

## 9. Grading rubric (100 points)
| Criterion | Excellent | Adequate | Weak | Pts |
|---|---|---|---|---|
| Manual audit (task 1) | 8+ specific, reproducible findings from both passes, correct AT noted | 5-7 findings, some vague | Few or copied from a tool | 15 |
| Automated scan (task 2) | Parametrized by state, baseline detects new/worse, reports saved, deterministic | Scan works but no baseline or one state | Asserts nothing meaningful | 20 |
| Defect analysis (task 3) | Correct SC + POUR, justified severity, de-duplicated, clear steps and fix | Mostly right, thin justification | Duplicates, wrong SC, "fix: make accessible" | 20 |
| Fix and proof (task 4) | 3+ fixes, before/after numbers, manual re-check recorded | 3 fixes, counts only | Edits original page / no proof | 15 |
| MCP tests (task 5) | 4 tests, error as `isError`, injected source, schema validated | 3-4 tests, minor gaps | Tests hit real API or skip errors | 10 |
| Code quality and Project 2 fit | Marker `a11y`, layering respected, no hard-coded paths, clean repo | Minor mess | Does not run from clean checkout | 5 |
| Collaboration | Swaps on time, both commit, roles respected, specific retrospective evidence | Swaps late or one person dominates | Solo work, no retrospective | 15 |

## 10. Hints (no solutions)
- Waiting matters: scan only after `.add-btn` exists, or your counts depend on timing. `open_state` already waits for you; when you inject elements yourself, wait too.
- axe reports **violations** (definite failures), but also has "incomplete" and "passes". Read the structure: `id`, `impact`, `nodes[].target`.
- Compare the `label` rule's node count with how many inputs you found by hand. Why do they differ?
- A defect is not "an axe rule". One rule may map to several defects, several rules to one. Ask "what single code change fixes all of these?"
- Keyboard defects are provable from Playwright: `page.keyboard.press("Tab")`, `document.activeElement`, `getComputedStyle(...).outlineStyle`.
- Fix order that pays off: language/title/landmarks (cheap, many nodes), alt text, labels, then interactive controls.
- Tool errors in MCP are **results** with `isError=True`. If your test expects an exception, re-read the written lesson's "errors" section.
- Reuse Wednesday's idea: inject the data source, do not call the network from unit-level tests.
- Written lessons: *Accessibility Principles*, *Keyboard and Screen-reader Testing*, *Automated Scanning*, *Accessibility Defect Analysis*, *Introduction to MCP Testing*. Demo code: `demos/4-thursday/code`.

## 11. Project 2 milestone (marked deliverable of the Project 2 framework)
Thursday adds an accessibility layer to your **Project 2 Test Automation Framework**:
- A pytest marker **`a11y`** registered in `pytest.ini` (and `mcp`), so `pytest -m a11y` runs only the scan.
- The axe scan tests in `tests/a11y/` with a committed baseline.
- Scan output saved to **`reports/a11y/`** (JSON per page/state plus `summary.json`).
- Defect reports in `defects/`.
Friday's pipeline will run `pytest -m a11y` as a job and publish `reports/a11y/` as an artifact; nothing else needs to change.

## 12. Merging into your Wednesday repo
Copy `storefront/`, `storefront_fixed/`, `mcp_server/`, `tests/a11y/`, `tests/mcp/`, `reports/` and the added lines of `requirements.txt` into the framework. In `pytest.ini` add the markers `a11y` and `mcp` and `asyncio_mode = strict`. Run `pytest` once: Wednesday's tests and Thursday's must still pass together.
