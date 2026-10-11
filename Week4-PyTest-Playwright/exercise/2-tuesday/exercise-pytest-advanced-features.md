# Lab: Refactor the Project 1 Tests with Fixtures, Parametrization and Mocks

**Week 4 (PyTest & Playwright) | Day 2 (Tuesday) | Individual exercise | Mode A: Implementation (Code Lab)**
**Project 1 - QE Foundations | Time box: 2 to 3 hours | Network needed: none (everything runs offline)**

> Log task: *Trainee Exercise: PyTest Advanced Features - Refactor Project 1 tests with fixtures/parametrization/mocks (2-3 h)*.
> This file is also saved as `exercise-pytest-advanced-features.md` (the exact filename in the CMA Log). The two files are identical.

---

## 1. The scenario

Your Project 1 test suite grew fast. On Monday you wrote one test function per case, and now:

- `tests/test_utils.py` has 32 near-identical tests for the Project 1 utility functions. A reviewer says: *"Great coverage, unreadable suite. Make it maintainable."*
- The team is adding two new features: a **defect log** (`defect_log.py`) that stores bug reports from your manual testing, and a **price converter** (`pricing.py`) that asks an external exchange-rate service for rates. Both need tests.
- The rate service is owned by another company, is slow, costs money per call and is down every other Tuesday. Your tests must **never** call it.

Your job: refactor and extend the suite using only today's tools: **fixtures, scopes, parametrization, `conftest.py` and mocks**. The behaviour of the code under test must not change; you only edit files in `tests/`.

## 2. Learning objectives

By the end you can:

1. Replace copy-pasted setup with **fixtures**, including a fixture with `yield` teardown.
2. Choose a **scope** (`function`, `module`, `session`) and justify it with the isolation vs cost trade-off.
3. Collapse repeated tests into `@pytest.mark.parametrize` tables with readable `ids`.
4. Combine fixtures and parametrization, including `indirect`.
5. Move shared fixtures into **`conftest.py`** and use an **autouse** safety fixture.
6. **Mock** an external HTTP call with `unittest.mock.patch`, `return_value` and `side_effect`, **patching where the name is looked up**, and verify the calls.

## 3. Prerequisites (read or review first)

Today's lessons in `written/2-tuesday/`: `fixtures.md`, `fixture-scopes.md`, `parametrization.md`, `combining-fixtures-and-parametrization.md`, `conftest-py.md`, `sharing-fixtures-across-tests.md`, `mocking-with-unittest-mock.md`.
Monday's skills: test functions, `assert`, `pytest.raises`, markers, `-k` / `-m`, `pytest.ini`. Python 3.9 or newer.

## 4. Setup (10 minutes)

```bash
cd starter_code
python -m venv .venv
# Windows:  .venv\Scripts\activate        macOS/Linux:  source .venv/bin/activate
pip install -r requirements.txt
python -m pytest -q
```

**Expected first run:** about `4 failed, 32 passed, 28 skipped`.

- The **32 passed** are the copy-pasted Monday-style tests in `test_utils.py`; leave them green while you refactor.
- The **skipped** tests wait for fixtures you will write (the stubs in `tests/conftest.py` call `pytest.skip`) or are stretch tasks.
- The **failed** tests say `TODO`. Your goal is to turn the whole run green (stretch tests included if you do them).

Folder map:

```
starter_code/
  pytest.ini            <- already set (pythonpath=src, --strict-markers, markers registered)
  requirements.txt
  REFLECTION.md         <- Task 6 deliverable
  src/                  <- code under test. DO NOT EDIT.
    project1_utils.py   (Monday's functions)
    defect_log.py       (DefectLog class)
    exchange.py         (get_rate: calls the external HTTP API)
    pricing.py          (price_in / price_label: use get_rate)
  tests/                <- YOUR work happens here
    conftest.py         (fixture stubs + TODOs)
    test_utils.py       (Task 1)
    test_defect_log.py  (Tasks 2, 3, 4)
    test_pricing.py     (Task 5)
```

> Tip: if your Python environment also has plugins such as `pytest-playwright` or `pytest-html`, `--setup-show` lists extra fixtures you did not write (for example `base_url`). Ignore them or use a clean virtual environment.
> Offline note: no website is used today. Playwright and a real site (SauceDemo) arrive on Thursday and Friday, where `page` is itself a fixture, so today is the foundation.

## 5. Core tasks (about 2 h)

Work in order. Run the suite after every sub-step. Commit (or save a copy) after each task.

### Task 1 - Parametrize the Monday tests (25 min) - `tests/test_utils.py`

1. Run `python -m pytest tests/test_utils.py -q` and note the count.
2. Group the tests by function under test (`add`, `is_even`, `is_palindrome`, `reverse_string`, `apply_discount`, `average`, `divide`).
3. Replace each group with **one** `@pytest.mark.parametrize` test. Rules:
   - Use `ids=` or `pytest.param(..., id=...)` so every case has a readable name (`negative-price`, not `-1-10`).
   - Keep the existing markers (`smoke`, `boundary`) on the refactored tests. Check with `python -m pytest -m boundary --collect-only -q`.
   - Error cases (`pytest.raises`) may stay as a second parametrized test per function (for example valid vs invalid discount).
4. Delete `test_task1_not_done_yet`.

**Done when:** at most 12 `def test_` functions remain in the file, at least 32 test cases are still collected (`python -m pytest tests/test_utils.py --collect-only -q`), and every case is still green.

### Task 2 - Fixtures with setup and teardown (30 min) - `conftest.py` + `test_defect_log.py`

1. In `tests/conftest.py`, implement `empty_log`, `populated_log` and `export_file` (read the TODO text on each stub; replace the `pytest.skip` line).
   - `export_file` must use **`yield`** and delete the file in the teardown section.
2. Complete the nine tests in the "Task 2" section of `test_defect_log.py` (replace each `pytest.fail(...)`).
3. Convert the two `Task 2b` / `2c` tests into **parametrized** tests (four invalid inputs; one case per entry of `SEVERITIES`).
4. Prove the lifecycle: run `python -m pytest tests/test_defect_log.py -k export --setup-show` and **paste the SETUP/TEARDOWN lines you see into `REFLECTION.md`** (any 6 lines).

**Done when:** all Task 2 tests pass, `test_fixtures_are_isolated` passes, and you can say in one sentence *why* it passes.

### Task 3 - Choose scopes (20 min) - `conftest.py` + `test_defect_log.py`

1. Implement `qa_config` with **session** scope (read-only: use `types.MappingProxyType` so a write raises `TypeError`) and `setup_calls` with session scope (an empty list).
2. Implement `big_log` with **module** scope: 200 defects numbered 0 to 199, severity `"high"` when `number % 4 == 0`, otherwise `"low"`. Append `"big_log"` to `setup_calls` when built.
3. Complete the four Task 3 tests. The last one proves the fixture was built **once** even though three tests used it.
4. Confirm with `--setup-show` that `big_log` shows the letter `M` and `qa_config` the letter `S`.
5. Experiment (do not keep it): add a test that closes a defect in `big_log`, then run the file with `-p no:randomly` (or just reorder tests). Explain in `REFLECTION.md` Q2 what went wrong. Delete the experiment.

**Done when:** scopes are `S`, `M` and function (no letter) as intended, and the "built once" test passes.

### Task 4 - Fixtures meet parametrization: `indirect` (15 min) - `test_defect_log.py`

1. Implement the fixture `log_with_open_defects(request)`, which builds a log containing `request.param` open defects.
2. Complete `test_open_count_matches_built_log` using `indirect=["log_with_open_defects"]` for the first argument and a plain direct argument for `expected_open` (cases 0, 1, 5 with ids).
3. Complete `test_closing_everything_leaves_zero_open` with `indirect=True` (cases 2 and 3).

**Done when:** `python -m pytest tests/test_defect_log.py -v` shows readable ids like `[none-0]` or `[one-1]` and all pass.

### Task 5 - Mock the external service (35 min) - `conftest.py` + `test_pricing.py`

1. In `conftest.py`, add the **autouse** fixture `block_real_network(monkeypatch)` described in the TODO. From now on any accidental real connection fails with `RuntimeError`.
2. In `test_pricing.py`, implement `mock_get_rate` so it patches the correct name and yields the mock. **Decide the target string yourself.** Hint: open `src/pricing.py` and look at how it obtains `get_rate`.
3. Complete the ten tests. They cover: `return_value`, `assert_called_once_with`, `assert_not_called`, `side_effect` with exceptions (parametrized), a non-caught exception that must propagate, the **wrong-target demonstration**, and testing `get_rate` itself by patching `requests.get` as seen from `exchange`.
4. Run the suite with your wifi switched off. It must still be fully green.

**Done when:** no test needs the network, the wrong-target test demonstrates the failure on purpose, and every mock assertion checks the *arguments* (not just "was called").

### Task 6 - Reflection (10 min) - `REFLECTION.md`

Answer the seven short questions in `REFLECTION.md`. Two to four sentences each.

## 6. Stretch tasks (optional, +30 to 45 min)

- **A. Parametrized fixture:** a fixture with `params=[...severities...]` plus a test using it; compare the generated ids with the `parametrize` version.
- **B. `pytest.param` with marks:** a 500-character title as an `xfail(strict=True)` case; explain what `strict=True` changes.
- **C. `create_autospec` and `monkeypatch`:** show a wrong call signature raises `TypeError` with autospec; redo one test with `monkeypatch.setattr`.
- **D. Hook and nested conftest:** register a custom marker in `pytest_configure` and add a `tests/unit/conftest.py` that **overrides** one fixture for tests in that sub-folder only. Prove the override with `--setup-show`.
- **E. Fixture hygiene:** run `python -m pytest --fixtures -q` and add a one-line docstring to every fixture you wrote.

## 7. Time plan (2 h 30 min, plus stretch)

| Time | Activity |
|---|---|
| 0:00 - 0:10 | Setup, first run, read the `src/` files (5 minutes) and skim the lessons |
| 0:10 - 0:35 | Task 1 parametrize |
| 0:35 - 1:05 | Task 2 fixtures and teardown |
| 1:05 - 1:25 | Task 3 scopes |
| 1:25 - 1:40 | Task 4 indirect |
| 1:40 - 2:15 | Task 5 mocking |
| 2:15 - 2:30 | Task 6 reflection, final run, submission |
| 2:30 + | Stretch tasks |

If you fall more than 20 minutes behind, finish Tasks 1, 2 and 5 first (they carry the most marks), then return to 3 and 4.

## 8. Deliverables

1. The completed `starter_code/` folder, with these files changed: `tests/conftest.py`, `tests/test_utils.py`, `tests/test_defect_log.py`, `tests/test_pricing.py`, `REFLECTION.md`. **Do not change `src/` or `pytest.ini`** (adding a marker to `pytest.ini` is allowed for stretch D).
2. A text file `RESULT.txt` containing the output of `python -m pytest -v` (final run, everything green; stretch tests count if done).
3. Optional: a short note in `REFLECTION.md` listing which stretch tasks you completed.

## 9. Definition of Done and rubric (100 points)

| # | Criterion | Points |
|---|---|---|
| 1 | Task 1: parametrized tests, readable ids, markers kept, case count not reduced, placeholder removed | 15 |
| 2 | Task 2: three fixtures, `yield` teardown, no copy-pasted setup, isolation understood | 20 |
| 3 | Task 3: correct scopes (S / M / function), "built once" proven, read-only data | 15 |
| 4 | Task 4: `indirect` used correctly (both list form and `True`) | 10 |
| 5 | Task 5: correct patch target, side_effect scenarios, call assertions, autouse network blocker, wrong-target demo | 25 |
| 6 | Code quality: names say behaviour, one reason to fail per test, fixtures have docstrings, no `import conftest` | 5 |
| 7 | `REFLECTION.md` answered with understanding (not copied from the lessons) | 10 |
| | **Total** | **100** |
| | Stretch (bonus, max +10): A to E, 2 points each | +10 |

**Pass mark:** 70. **Automatic checks** (run by the instructor): `python -m pytest -q` is green offline, `--collect-only` shows at least 32 cases in `test_utils.py`, `src/` is unchanged, `-m smoke` and `-m boundary` still select tests.

## 10. Hints (try 10 minutes before opening one)

<details><summary>Task 1: how do I keep markers?</summary>
Put <code>@pytest.mark.boundary</code> above <code>@pytest.mark.parametrize</code>; the marker applies to every generated case. For a single case, use <code>pytest.param(..., marks=...)</code>.
</details>
<details><summary>Task 2: yield fixture shape</summary>
<code>path = tmp_path / "defects.csv"</code>, then <code>yield path</code>, then <code>path.unlink(missing_ok=True)</code>. Everything after <code>yield</code> is teardown.
</details>
<details><summary>Task 3: ScopeMismatch</summary>
A fixture may only depend on fixtures of the same or wider scope. <code>big_log</code> (module) may use <code>setup_calls</code> (session); never the other way round. Remember to add <code>scope=...</code> to the stubs in conftest, they currently use function scope.
</details>
<details><summary>Task 4: how does the fixture know the value?</summary>
Inside a fixture, <code>request.param</code> is the value the test's parametrize table supplied for that case.
</details>
<details><summary>Task 5: which string do I patch?</summary>
Patch the name <em>in the module that uses it</em>: <code>"module_that_calls.name_it_calls"</code>. Ask yourself: after <code>from exchange import get_rate</code>, which module owns a variable called <code>get_rate</code> that <code>price_in</code> reads?
</details>
<details><summary>Task 5: how do I fake <code>requests.get</code>?</summary>
Use <code>MagicMock()</code> for the response, set <code>response.json.return_value = {...}</code>, and patch <code>"exchange.requests.get"</code> with <code>return_value=response</code>. For errors, set <code>response.raise_for_status.side_effect = requests.HTTPError(...)</code>.
</details>
<details><summary>My tests pass alone but fail together</summary>
Look for a mutable object created at module scope or session scope that a test changes. Move it to function scope, or stop mutating it.
</details>

## 11. Project 1 - QE Foundations milestone

> **Instructor note:** no Project 1 specification was supplied when this exercise was written. The milestone below is a sensible default consistent with the CMA Log (Monday: automate the utility tests; Tuesday: refactor them with fixtures, parametrization and mocks). **Instructors should adjust names and acceptance criteria to the real Project 1 brief.**

**Milestone 2 of the Week 4 build-up: "A maintainable, offline-runnable PyTest suite."**

| Milestone item | Evidence in this exercise |
|---|---|
| The Project 1 utility tests from Monday are refactored into table-driven tests | Task 1 (`test_utils.py`) |
| Shared setup lives in fixtures and `conftest.py`, not in copy-paste | Tasks 2 and 3 |
| Test data for new features (defect log) is built by fixtures with sensible scopes | Tasks 2, 3, 4 |
| No test depends on an external service or the internet | Task 5 (mocks + autouse network blocker) |
| The suite is tagged (`smoke`, `boundary`, ...) and selectable with `-m` | Task 1 |

**How it carries forward:** Wednesday you add data-driven design, custom assertions and an HTML report to this same suite (take the finished folder with you). Thursday and Friday the Playwright `page` object is delivered *as a fixture* into the very same `conftest.py` pattern.
**Submit as the Project 1 milestone:** the folder from Section 8. Keep it in your Project 1 repository under `tests/` (copy `conftest.py`, `pytest.ini`, `requirements.txt` to the project root if your repo layout requires it).

## 12. Submission instructions

1. Run `python -m pytest -v > RESULT.txt` from `starter_code/` (everything green).
2. Make sure `src/` and `pytest.ini` are unchanged (`git diff --stat` if you use git).
3. Zip the folder without `.venv` and `__pycache__` (or push to your branch `week4-tuesday-<your-name>`), and upload/open the pull request as your instructor directs.
4. Be ready to explain in two minutes, at the Wednesday stand-up: *one test you are proud of, one thing you got stuck on*.

*(Instructor-only material is in `solution/`. Do not distribute it to trainees before the deadline.)*
