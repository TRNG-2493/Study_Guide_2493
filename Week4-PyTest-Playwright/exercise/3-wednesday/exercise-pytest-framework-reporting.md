# Exercise: Complete the Project 1 PyTest Framework and Take the PyTest Skills Assessment

**Week 4 (PyTest and Playwright) | Day 3, Wednesday: PyTest Framework and Reporting**
**Mode:** A (code lab), **individual** work | **Time:** 2 to 3 hours (plan below: about 2 h 45 min)
**Project:** Project 1 - QE Foundations

---

## 1. The scenario

Your QE team keeps a small shared library, `qe_utils`, with three utility functions that other teams rely on:

| Module | Function(s) | What it does |
|--------|-------------|--------------|
| `shipping.py` | `shipping_cost(weight_kg, zone)` | Parcel price from weight and zone |
| `usernames.py` | `normalize_username`, `is_valid_username` | Cleans and validates usernames |
| `temperature.py` | `celsius_to_fahrenheit(c)` | Temperature conversion |

Monday you wrote basic tests. Tuesday you used fixtures and parametrization. Today you assemble the **test framework**: a clean layout, data-driven tests whose data lives in files, reusable custom assertions, exception tests, an HTML report and a speed check. The result is the PyTest half of your Project 1 deliverable.

The team lead has one extra request: **the specifications (the docstring at the top of each module in `src/qe_utils/`) are the truth. If the code disagrees with the spec, that is a bug and you must report it, not "fix" the test to match the code.**

In the afternoon you take the **PyTest skills assessment** (practice assessment in the written lesson) under time pressure, as a check on the whole week so far.

## 2. Learning objectives

By the end you can:

1. Configure a project with `pytest.ini` (paths, registered markers, strict options).
2. Organize code under test, helpers, data and tests into a clean layout.
3. Drive tests from JSON, CSV and inline data using `pytest.param` with readable IDs.
4. Write custom assertion helpers with helpful failure messages (`__tracebackhide__`, `pytest.approx`).
5. Test error paths with `pytest.raises(..., match=...)`.
6. Mark a known defect with `xfail(strict=True)` and write a short bug report.
7. Produce a customized HTML report (title, metadata, Description column).
8. Find the slowest tests with `--durations` and enforce a time budget.
9. Solve a timed PyTest assessment and score yourself honestly.

## 3. Prerequisites (all taught up to and including today)

- Monday: installing PyTest, naming and discovery, `assert`, markers, `-k` / `-m`.
- Tuesday: fixtures, `conftest.py`, parametrization.
- Wednesday written lessons: *data-driven test design*, *custom assertions*, *exception testing*, *test organization and reusable templates*, *HTML reporting*, *performance profiling*, *PyTest skills assessment*.
- Python 3.10 or newer, a terminal, a code editor.

Keep the lessons open. Everything you need is in them or in the instructor demo you saw today (the demo used different functions: pricing and validators; **you** are testing shipping, usernames and temperature).

## 4. Setup (10 minutes)

```bash
cd starter_code
python -m venv .venv
# Windows:      .venv\Scripts\activate
# macOS/Linux:  source .venv/bin/activate
pip install -r requirements.txt
python -m pytest
```

**Expected starter result:** `4 passed, 1 skipped, 8 failed` (the 8 failures are the `TODO` tests waiting for you; the skip is the CSV test waiting for your loader). The starter must RUN; it just is not finished. If you see a collection error, stop and fix the setup (ask the instructor).

> Playwright is not used today, so no browsers or websites are needed. Tomorrow's pair project and Friday's lab use the browser.

Starter layout:

```
starter_code/
├── pytest.ini              Task 1
├── conftest.py             Task 6 (report hooks)
├── requirements.txt
├── NOTES.md                Tasks 3c, 7, 8, 9 (your written answers)
├── reports/                HTML report goes here
├── src/qe_utils/           code under test: DO NOT EDIT
├── tests/
│   ├── data/               shipping_cases.json, username_cases.csv  (Task 3)
│   ├── helpers/            assertions.py (Task 4), data_loader.py (Task 3b)
│   └── unit/               test_shipping / test_usernames / test_temperature / test_suite_speed
```

**Rule: do not edit anything under `src/`.** You are the tester.

## 5. Core tasks (required)

Search for `TODO` in the project (`Ctrl+Shift+F` in VS Code) to see everything left to do.

### Task 1: Configure the project (10 min)
Open `pytest.ini`. Register the markers `regression`, `boundary` and `slow` (one line each, with a description). Then add `@pytest.mark.slow` to the two tests in `test_suite_speed.py`.
**Check:** `python -m pytest --markers` lists all four markers; `python -m pytest -m slow` selects two tests.

### Task 2: Read the specifications (5 min, no code)
Read the docstring at the top of each file in `src/qe_utils/`. In `NOTES.md` you do not need to write anything yet, but for each function think of: one normal case, one boundary and one invalid input. You will need them in Tasks 3 to 5.

### Task 3: Data-driven tests (30 min)
- **3a. JSON data.** `shipping_cases.json` has 3 rows. Add **at least 7 more**, covering every zone with a light and a heavy parcel and the boundaries just either side of 5 kg (4.99 and 5.01), the minimum (0.01) and the maximum (30). Every row needs a unique, readable `id`. Run `python -m pytest -v` and confirm the IDs show in the output.
- **3b. CSV data.** In `tests/helpers/data_loader.py` implement `load_csv_cases`. Then add **at least 8 more rows** to `username_cases.csv` (lengths 3 and 15 and 16, starts with a digit or underscore, contains a space or dash, upper-case, surrounding spaces, digits inside). The CSV test must go from SKIPPED to running.
- **3c. Boundary and the planted defect.** Write `test_shipping_cost_exactly_5kg_is_light_rate` (5 kg, national, expected 6.50). Run it. **It will fail.** Read the spec again: are you sure the test is right? If yes, you found a real bug. Do **not** change `src/`. Instead mark the test `@pytest.mark.boundary` and `@pytest.mark.xfail(reason="BUG-001: ...", strict=True)`, then fill in the bug report in `NOTES.md` (steps, expected vs actual, where you think the defect is).
- **3d. Inline data.** In `test_temperature.py` parametrize at least 5 rows with `pytest.param(..., id=...)` (freezing, boiling, body, -40, absolute zero). Use the helper from Task 4b to compare.

### Task 4: Custom assertions (20 min)
In `tests/helpers/assertions.py` (use `assert_between` as the model):
- **4a.** Implement `assert_valid_username` with a **different message for each reason** (not a string, wrong length, bad first character, forbidden characters) and use it in the test.
- **4b.** Implement `assert_close` (no `==` on floats). Use it in the temperature test.
- **4c.** Prove a message is useful: call `assert_valid_username("9lives")` inside `pytest.raises(AssertionError, match=...)` and match a word from your message.
Both helpers must start with `__tracebackhide__ = True`.

### Task 5: Exception testing (15 min)
- **5a.** Replace the body of `test_shipping_cost_invalid_input_raises` with a parametrized `pytest.raises(exc_type, match=message)` test with **at least 6 rows**, each with an `id`. Cover wrong types (text, `True`, `None`), out of range (0 and 30.01), an unknown zone and a non-string zone.
- **5b.** Test `normalize_username` for normal input and `TypeError` on non-strings.
- **5c.** Test `celsius_to_fahrenheit` raises `TypeError` and `ValueError` as specified.
Always include `match=`: a test that only checks the type can pass for the wrong reason.

### Task 6: HTML report (20 min)
In `conftest.py` implement:
- **6a.** a custom report title that mentions Project 1;
- **6b.** Environment table rows: `Project`, `Tester` (your name), `Environment` (and nothing secret);
- **6c.** a **Description** column showing each test's docstring.
Then run:
```bash
python -m pytest --html=reports/report.html --self-contained-html
```
Open the file in a browser. Expand a failing or xfailed row. Take a screenshot of the report summary (Deliverable D3).

### Task 7: Performance check (10 min)
Run `python -m pytest --durations=3`. Paste the output in `NOTES.md` and say in two or three sentences which test is slowest and whether that is expected. Then implement `test_shipping_cost_stays_within_budget`: time 10,000 calls with `time.perf_counter()` and assert `< 1.0` second, with the measured time in the failure message.

### Task 8: PyTest skills assessment (45 min, time-boxed)
Open the written lesson **PyTest skills assessment** and use its *Practice Assessment*. Put your work in a new folder `assessment/` next to `starter_code/` (the lesson gives the scenario files).
1. Set a 45-minute timer. **Do not look at the model solutions yet.**
2. Required: **Tasks 1, 2, 3 and 7** (Configuration, data-driven discounts, custom assertion, debug the broken file: 50 points).
3. When the timer rings, stop. Compare with the model solutions, mark yourself using the lesson's self-scoring table, and record the scores in `NOTES.md`.
4. Finish tasks 4 to 6 and 8 of the assessment later if you want the other 50 points (optional, see stretch S4).

### Task 9: Wrap up (10 min)
Fill in the reflection in `NOTES.md`, run the full suite once more and check the Definition of Done (section 8).

## 6. Stretch tasks (optional)

- **S1. Known bugs in the data.** Extend `load_cases` so a JSON row with `"known_bug": "BUG-001"` is turned into `pytest.param(..., marks=pytest.mark.xfail(reason=..., strict=True))`. Add the 5 kg row to the JSON and delete the separate test.
- **S2. Soft assertions.** Add a `SoftAssert` class and a `soft` fixture (see the custom assertions lesson, section on soft assertions) and use it to check three fields of a "sign-up form" in one test.
- **S3. Timestamped reports and JUnit XML.** Name the report `reports/report_YYYYMMDD_HHMMSS.html` automatically and also write `reports/junit.xml`.
- **S4. Finish the assessment.** Complete the remaining assessment tasks (4, 5, 6, 8) and total all 100 points.
- **S5. Timeout safety net.** Add `pytest-timeout` (`timeout = 5` in `pytest.ini`) and prove it with a test that sleeps for 10 s marked `@pytest.mark.timeout(1)` and expected to fail (xfail).
- **S6. Description for failures.** Add the test's marker names as a second extra column in the report.

## 7. Deliverables

Submit **one folder** (zip or Git branch) containing:

| ID | Deliverable |
|----|-------------|
| D1 | `starter_code/` completed: `pytest.ini`, `conftest.py`, `src/` (unchanged), `tests/` (data, helpers, unit) |
| D2 | `python -m pytest` run with **no failures** (only the one expected xfail, plus any xfails you document) |
| D3 | `reports/report.html` **and** a screenshot of its summary |
| D4 | `NOTES.md` complete: bug report, `--durations` output and comment, assessment self-score, reflection |
| D5 | `assessment/` folder with your work on assessment Tasks 1, 2, 3, 7 |

## 8. Definition of Done and rubric (100 points)

| Area | Points | "Done" means |
|------|--------|--------------|
| Configuration | 10 | `pytest.ini` registers `smoke`, `regression`, `boundary`, `slow`; `--strict-markers` works; `pytest --markers` is clean |
| Data-driven design | 25 | JSON with 10+ rows, CSV with 10+ rows, inline temperature data; every row has a readable `id`; boundaries covered; test logic is not duplicated |
| Custom assertions | 15 | Two helpers with `__tracebackhide__`, distinct helpful messages, `approx`/tolerance used; one test proves a message |
| Exception testing | 10 | At least 6 shipping raises rows plus username and temperature tests, all with `match=` |
| Defect handling | 10 | Exact-5 kg test fails for the right reason, is `xfail(strict=True)` with a reason, `src/` untouched, bug report complete and clear |
| Report and performance | 15 | Custom title, 3 metadata rows, Description column, screenshot; `--durations` pasted and explained; budget test works |
| Skills assessment | 10 | Tasks 1, 2, 3, 7 attempted in 45 min; honest self-score recorded |
| Quality | 5 | Clear names, docstrings on tests, no unused code, no `print` debugging |

**Pass mark:** 70. **Automatic checks the instructor will run:** `python -m pytest` (green or expected xfail), `python -m pytest -m smoke`, `python -m pytest --markers`.

## 9. Hints (open only if stuck)

- `ModuleNotFoundError: qe_utils` means you ran PyTest from the wrong folder, or `pythonpath` is missing from `pytest.ini`. Run from `starter_code/`.
- `'boundary' not found in markers` means you forgot to register it (Task 1).
- Empty-parameter-set skip means your loader returned `[]`.
- CSV values are always text: `"true"` is not `True`.
- A failing helper shows the wrong line? You forgot `__tracebackhide__ = True`.
- `pytest.raises` passes even if the wrong message is raised unless you add `match=`.
- `strict=True` xfail turns into a failure if the test starts passing: that is the point, it tells you the bug was fixed.
- The report table is misaligned: the header and row hooks must insert the same number of cells.
- Assessment stuck? Re-read the lesson's competency checklist; do not peek at the solution before the 45 minutes are over.

## 10. Suggested time plan (about 2 h 45 min)

| Time | Activity |
|------|----------|
| 0:00 - 0:10 | Setup, run the starter |
| 0:10 - 0:25 | Task 1 and Task 2 (configure, read specs) |
| 0:25 - 0:55 | Task 3 (data-driven, bug found) |
| 0:55 - 1:15 | Task 4 (custom assertions) |
| 1:15 - 1:30 | Task 5 (exceptions) |
| 1:30 - 1:50 | Task 6 (report) |
| 1:50 - 2:00 | Task 7 (performance) |
| 2:00 - 2:45 | Task 8 (timed skills assessment) |
| 2:45 - 2:55 | Task 9 and submission |

If you are behind, finish Tasks 1, 3, 4 and 5 first, then 6, 7 and 8. Stretch tasks go beyond 3 hours: skip them if the clock is tight.

## 11. Project 1 - QE Foundations milestone

> **Instructor note:** no Project 1 specification was available when this exercise was written. The milestone below is a sensible proposal consistent with the week plan. **Please adjust it to your actual Project 1 requirements** (for example, replace the three sample utilities with the real Project 1 utility functions).

**Milestone (end of Wednesday, "PyTest framework complete"):** the Project 1 utility functions have an automated, data-driven PyTest suite that anyone on the team can run with one command and read in one HTML report.

| Milestone item | Evidence |
|----------------|----------|
| Framework layout (`src/`, `tests/{helpers,data,unit}`, `conftest.py`, `pytest.ini`) | D1 |
| Data-driven tests from JSON, CSV and inline data | D1 |
| At least two reusable custom assertions | D1 |
| Exception tests for every invalid-input rule in the specs | D1 |
| Defects found are documented (bug report plus strict xfail) | D4 |
| Green run and a customized HTML report | D2, D3 |
| PyTest skills assessment completed and self-scored | D4, D5 |

**Where this goes next:** Thursday you and a partner build a locator catalog for a practice website (Playwright), and Friday you automate three Project 1 UI scenarios. The same `pytest.ini`, `conftest.py` and report setup you build today will carry the browser tests, so keep your framework tidy.

## 12. Submission instructions

1. Delete `.venv/`, `__pycache__/` and `.pytest_cache/` (the `.gitignore` already ignores them).
2. Name the folder `P1-W4-D3-<yourname>` (or push to a branch of the same name).
3. Include the report file and screenshot under `reports/`.
4. Submit as your instructor directs (LMS upload or pull request) **before the end of the day**.
5. Be ready to explain, in two minutes, one bug you found and how you proved it.

---
*Instructor-only reference solution: `solution/` (see `solution/README_INSTRUCTOR.md`). Do not share it before submissions close.*
