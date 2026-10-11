# Lab: Automate a Complex Form Flow (Playwright Web Interactions)

**Week 5, Day 1 (Monday) | Mode A: Code Lab | INDIVIDUAL | Estimated time: 2 h 35 min core + Project 1 milestone (optional stretch: +30 to 45 min)**

Language and tools: Python, Playwright sync API, pytest-playwright, Chromium. The app under test is a local static page served by a tiny Python helper, so the lab works **offline** and behaves the same on every machine.

---

## 1. Scenario

You are the QE on the **QE Summit 2026** conference team. The registration form is the money page: if it breaks, tickets are not sold. It is also a nightmare to test by hand, because it combines almost everything real forms do:

| Form feature | Where it appears |
|---|---|
| JS `alert`, `confirm`, `prompt` | "Need help?", "Add dietary request", "Reset form", "Register" |
| Radios | Ticket type (Standard / Workshop / VIP) |
| Checkboxes with conditional enabling | Add-ons (kit needs Workshop/VIP, gala needs VIP), terms gate the Register button |
| Native single `<select>` | T-shirt size |
| Native multi `<select multiple>` | Sessions |
| Custom (non-`<select>`) dropdown | Country |
| Keyboard-driven field | Promo code (applies only when you press **Enter**; Escape removes it) |
| Hover / drag elements | Price tooltip (hover), donation slider (drag) |
| Autosuggest | City (keyup-driven, 250 ms debounce, minimum 2 characters) |

Your job: write a reliable automated suite for this flow, then repeat the same approach on **your own Project 1 application** (section 9).

## 2. Learning objectives

By the end you can:

1. Register dialog handlers **before** the triggering action and assert on both the page outcome and the dialog itself (type and message), including a prompt answer and Cancel-versus-empty text.
2. Drive radios and checkboxes by **state** (`check()`, `uncheck()`) and assert conditional-enabling rules before and after.
3. Choose between `select_option()` (native single/multi) and open-then-click (custom dropdowns).
4. Use keyboard keys, hover and the low-level mouse (`page.mouse`) for Enter-to-apply fields, tooltips and drag sliders.
5. Test an autosuggest by typing like a user, waiting on **content not time**, and picking by click and by keyboard.
6. Combine all of it into one end-to-end test with a negative path and a happy path.

## 3. Prerequisites

- Written lessons read: `alerts-dialogs-and-pop-ups`, `radio-buttons-and-checkboxes`, `dropdowns-and-multi-selects`, `keyboard-and-mouse-actions`, `auto-suggestions` (all in `written/1-monday/`).
- The instructor demo has been run in class (`demos/1-monday/`).
- Python 3.10+ and `pip`. Week 1-4 skills: locators (`get_by_role`, `get_by_label`, CSS), `expect` assertions, running pytest.
- A Project 1 repository you can commit to (section 9).

**Not needed today (do not use):** frames, tables, tabs/popups, file upload, fixtures, Page Object Model, JSON data files. They come Tuesday and Wednesday. A provided `conftest.py` starts the app for you; treat it as "the app is already running".

## 4. Setup (about 10 minutes)

```bash
cd starter_code
python -m venv .venv
source .venv/bin/activate            # Windows: .venv\Scripts\activate
pip install -r requirements.txt
playwright install chromium

pytest                               # sanity check
```

You should see `1 passed, 18 failed, 6 skipped`. Every failure reads `TODO: implement ...`. That is the starting point, not a broken install.

Explore the app by hand before writing any test (this is part of the lab: 3 minutes of exploring saves 20 of debugging):

```bash
python serve.py                      # open http://127.0.0.1:8765/   (Ctrl+C to stop)
```

Try: pick each ticket type and watch the add-ons; hover the blue **i**; type `QE2026` and press Enter; drag the donation handle; type `Ha` in City; click every button and read the dialog text.

Useful commands while building:

```bash
pytest -k test_01 --headed --slowmo 400      # one test, visible, slowed down
pytest tests/test_form_flow.py -x            # stop at first failure
PWDEBUG=1 pytest -k test_14                  # Playwright Inspector (Windows PowerShell: $env:PWDEBUG=1)
```

Ground rules: `time.sleep()` and `page.wait_for_timeout()` are not allowed; every action is followed by an assertion; prefer role/label locators over brittle CSS; do **not** edit `app/index.html` or `tests/conftest.py`.

## 5. Core tasks (work in `starter_code/tests/test_form_flow.py`)

For every test: read the TODO comments, implement them, **delete the `pytest.fail("TODO ...")` line**, run the test. Test `test_00` is a finished worked example showing the expected style.

### Stage 1: Dialogs (about 25 min), tests 01 to 05
| Test | What you prove |
|---|---|
| 01 | `alert`: record `(type, message)`, answer it, assert the recorded dialog |
| 02 | `prompt`: accept with text; page shows the text |
| 03 | `prompt`: **Cancel** (null) and **OK with empty text** give different outcomes |
| 04 | `confirm`: dismiss keeps the data; assert the confirm text |
| 05 | `confirm`: accept clears the form and resets the total |

### Stage 2: Radios and checkboxes (about 15 min), tests 06 to 08
Assert the initial rules (no default ticket, no pre-ticked consent, disabled add-ons), then the conditional rules as you change the ticket type, then the terms gate on **Register**. Use `check()`/`uncheck()`, never a blind `click()`.

### Stage 3: Dropdowns (about 15 min), tests 09 to 11
Native `<select>` by `value`, `label` and `index`; multi-select replace-and-clear semantics; the custom Country dropdown (open, assert `aria-expanded`, click the option).

### Stage 4: Keyboard and mouse (about 25 min), tests 12 to 14
Promo code with the **Enter** key (valid and invalid), hover tooltip (assert before and after), drag the donation slider with `page.mouse` to 50.

### Stage 5: Autosuggest (about 20 min), tests 15 to 17
Prove `fill()` does not trigger it; use `press_sequentially` and wait on content; select by click and by `ArrowDown`+`Enter`.

### Stage 6: End-to-end (about 15 min), test 18
One test: fill the entire form, assert the total (**$290.00**), prove the **negative path** (Cancel the confirmation: nothing is registered), then the **happy path** (confirm and alert in a row, receipt with 12 fields checked).

> Stage times total 115 minutes; with setup (10) and the Project 1 milestone (30) the day is **2 h 35 min**. Your pace will vary, which is why the stretch tasks are optional.

## 6. Stretch tasks (optional, `tests/test_stretch.py`, +30 to 45 min)

Each starts as `pytest.skip(...)`; delete that line to attempt it.

- **S1** Validation errors on an empty form, and prove **no dialog** was raised.
- **S2** Operate the slider with the keyboard (ArrowRight x3, End, Home).
- **S3** Promo is case-insensitive; Escape removes the discount.
- **S4** Autosuggest edge cases: minimum characters, "No results" is not an option, case-insensitive, Escape keeps text.
- **S5** Price matrix with a plain `for` loop over ticket types.
- **S6** Two different dialogs answered by **one** `page.on` handler that branches on `dialog.type`.

## 7. Hints (read only when stuck, by lesson and section)

| Problem | Where to look |
|---|---|
| Test hangs on a click | The handler never answered. `[DLG s2, s3]` every code path must call `accept()` or `dismiss()` |
| `seen_dialogs` is empty | Handler registered after the click. `[DLG s6]` listen first |
| Need to prove the dialog text | `[DLG s8]` and Example 4: record in the handler, assert in the test body |
| Cancel versus OK-with-empty text | `[DLG s7]` last paragraph |
| Two dialogs in one click (confirm then alert) | `[DLG s5]` `on` vs `once`; two `once` calls both fire for the **first** dialog, so use one `page.on` handler and remove it in `finally`. Example 5 |
| Strict-mode violation on a checkbox | `[CHK s4]` narrower role/name, or `exact=True` |
| `check()` times out | The control is disabled: satisfy the rule that enables it first. `[CHK s7]` |
| How do I count checked radios? | `[CHK s5, s6]` `:checked` locator with `to_have_count` |
| `select_option` fails on Country | It is not a `<select>`. `[DDN s8]` open it, then click the option |
| Multi-select kept the old values? | It replaces, it does not add. `[DDN s3]` |
| Option count is wrong / matches too much | Native `<option>` elements have role `option` too. Scope to the list: `page.locator("#city-list").get_by_role("option")` |
| `Unknown key "enter"` | `[KBM s3]` key names are case-sensitive: `Enter`, `ArrowDown` |
| Promo not applied after `fill()` | By design: the app waits for the Enter keydown. `[KBM s2, s3]` |
| Slider does not move | `[KBM s7, s8]` hover the handle, `mouse.down()`, `mouse.move(x, y, steps=15)`, `mouse.up()`; `bounding_box()` is viewport-relative and can be `None` |
| Suggestions never appear | `fill()` fires no `keyup`. `[SUG s3]` use `press_sequentially` |
| Clicked the wrong suggestion | `[SUG s4, s5]` wait for the list content with `to_have_text([...])`, not for time |
| Which option is highlighted? | `[SUG s7, s8]` `get_by_role("option", selected=True)` |
| Flaky test | Re-read the failure: `expect` prints the actual page content. Run with `--headed --slowmo 400` |

## 8. Definition of Done

- [ ] `pytest` in your submission folder shows **18 core tests passing**, none failing, none still containing `pytest.fail("TODO`.
- [ ] No `time.sleep`, no `wait_for_timeout`, no `force=True`, and `app/index.html` and `conftest.py` are unchanged.
- [ ] Every dialog handler is registered **before** its trigger; every handler answers on every code path; persistent `page.on` listeners are removed in `finally`.
- [ ] Each test asserts the **outcome** (page state) and, for dialogs, the dialog's **type and message**.
- [ ] Tests use role/label/id locators; `check()`/`uncheck()` for radios and checkboxes; `select_option` only on native selects.
- [ ] Test 18 covers both a negative path (cancel) and a happy path (confirm + alert + receipt fields).
- [ ] Project 1 milestone (section 9) committed and pushed to your Project 1 repository, with at least 3 passing tests.
- [ ] A short `NOTES.md` (5 to 10 lines): the one hardest thing, and one flaky/brittle point you found and how you fixed it.

## 9. Project 1 - QE Foundations milestone

> **Assumption (instructors, please confirm):** the curriculum does not specify which application Project 1 tests. The milestone below is therefore written generically: *apply today's techniques to the main form flow of your Project 1 application* (for example registration, login, checkout, or a booking/contact form, whichever is the richest form in your app). If your Project 1 application has no form with these controls, use its closest equivalent and note it in `NOTES.md`.

**What you add to your Project 1 UI test suite today (about 30 min):**

Create `tests/ui/test_<your_form>_flow.py` (or the folder your Project 1 repo already uses) containing **at least 3 passing Playwright tests** for your app's main form flow:

1. **Happy path**: fill the form end to end and assert the final outcome (success message, data shown, or URL/state change).
2. **Negative path**: submit with a required field empty or a rule broken and assert the specific validation message or Cancel/dismiss behaviour.
3. **Conditional rule**: assert one "X is disabled/hidden until Y" rule **before and after** satisfying it.

Across the three tests you must use **at least three** of today's techniques where your app has the matching control: a dialog handler (assert type + message), `check()`/`select_option()`, keyboard (`press`/`press_sequentially`), hover/mouse, autosuggest with content-based waiting. Where the app lacks a control, say so in `NOTES.md` rather than inventing one.

A starter file is provided: `starter_code/project1_milestone/test_project1_ui_form_flow_TEMPLATE.py`. It reads your app's URL from the `P1_BASE_URL` environment variable and **skips itself when the variable is not set**, so it never breaks anyone's pipeline. Replace each `# TODO` with locators for your app.

**How to submit the milestone:**

1. Copy the template into your Project 1 repository, rename it, implement the tests, run them (`pytest tests/ui -k <your_form>`).
2. Commit on a branch named `week5-mon-ui-form-flow` with a message like `Add UI form flow tests (Week 5 Monday)` and push.
3. Add a 3-line section to your Project 1 README or `NOTES.md`: the form flow you automated, the techniques used, and how to run the tests.
4. Open a pull request (or share the branch link) per your cohort's instructions.

Later this week (Wednesday) you will restructure these same tests into a Page Object Model, so keep them short and readable today; do not build a framework now.

## 10. Submission

1. Exercise: submit the whole `starter_code/` folder (excluding `.venv/`) as a Git repository/branch link or a zip, with your `NOTES.md`.
2. Project 1 milestone: branch or PR link from section 9.
3. Before submitting run `pytest` one last time and paste the final summary line into `NOTES.md`.

## 11. Rubric (100 points)

| Area | Points | Full marks when |
|---|---|---|
| Dialogs (tests 01 to 05) | 20 | Handlers registered first, always answered, dialog type and message asserted, Cancel vs empty proven |
| Radios, checkboxes, conditional rules (06 to 08) | 12 | State-based `check()`, rules asserted before and after, no blind `click()` |
| Dropdowns (09 to 11) | 12 | Correct tool per control; replace semantics shown; custom dropdown opened and clicked with scoped locator |
| Keyboard and mouse (12 to 14) | 15 | Enter key, before/after hover assertion, slider drag with `steps` and a guarded `bounding_box()` |
| Autosuggest (15 to 17) | 12 | Waits on content, scoped option locator, click and keyboard selection |
| End-to-end test (18) | 9 | Negative then happy path, two dialogs handled correctly, all receipt fields asserted |
| Test quality | 5 | Readable names, no sleeps, no forced actions, stable locators |
| Project 1 milestone | 12 | 3+ passing tests on your app, 3+ techniques, pushed with the README note |
| NOTES.md | 3 | Specific, honest reflection |
| **Total** | **100** | Stretch tasks: up to +5 bonus (not counted above 100) |

## 12. Time estimate

| Activity | Minutes |
|---|---|
| Setup and exploring the app | 10 |
| Stage 1 Dialogs | 25 |
| Stage 2 Radios and checkboxes | 15 |
| Stage 3 Dropdowns | 15 |
| Stage 4 Keyboard and mouse | 25 |
| Stage 5 Autosuggest | 20 |
| Stage 6 End-to-end | 15 |
| Project 1 milestone and NOTES.md | 30 |
| **Core total** | **155 (2 h 35 min)** |
| Stretch tasks (optional) | +30 to 45 |

## 13. Folder map

```
exercise/1-monday/
  README.md                  this file
  starter_code/              what trainees receive (app, helper server, TODO tests, Project 1 template)
  solution/                  INSTRUCTOR ONLY: completed tests (same app) - do not distribute before the deadline
```
