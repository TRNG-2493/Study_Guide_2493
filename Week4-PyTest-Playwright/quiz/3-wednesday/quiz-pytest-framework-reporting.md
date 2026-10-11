# Weekly Knowledge Check: Wednesday - PyTest Framework and Reporting

**Week 4 - PyTest & Playwright | Day 3 (Wednesday)** | 68 questions

## Topics Covered

- Data-Driven Test Design (inline/JSON/CSV data, `pytest.param`, boundary and equivalence data)
- Custom Assertions (messages, `__tracebackhide__`, `pytest.approx`, soft assertions, `pytest_assertrepr_compare`)
- Exception Testing (`pytest.raises`, `match`, `excinfo`, chaining, `nullcontext`)
- Test Organization and Reusable Templates (`pytest.ini`, layout, AAA, builders, factory fixtures)
- HTML Reporting (`pytest-html`, self-contained reports, hooks, JUnit XML)
- Performance Profiling (`--durations`, `perf_counter`, `timeit`, `cProfile`, `pytest-xdist`, `pytest-timeout`)
- PyTest Skills Assessment review (Monday to Wednesday skills, error decoder, strategy)

## Instructions

1. Try to answer each question yourself before opening the solution. Tick the box (or write your answer) first.
2. Click **Click for Solution** to reveal the correct answer, the explanation and, for multiple-choice questions, why each wrong option is wrong.
3. The questions are grouped by format: Multiple Choice, True/False, Code Prediction and Fill-in-the-Blank. Some concepts are asked again in a different style on purpose.
4. Code Prediction answers were checked by actually running the snippets. Note that the exact wording of a message can differ slightly between PyTest versions.
5. Aim to understand the reasoning, not to memorise letters. Re-read the written lesson for any topic where you miss two or more questions.

---

## Part 1: Multiple Choice

### 1. Which description best matches **data-driven testing (DDT)**?

- [ ] A) Every scenario gets its own copy-pasted test function so that failures stay isolated.
- [ ] B) The same test logic runs several times with different input and expected data, and the data is kept separate from the logic.
- [ ] C) A test that reads its data only from a database.
- [ ] D) A single test that loops over all rows and stops at the first failing row.


<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** B) The same test logic runs several times with different input and expected data, and the data is kept separate from the logic.

**Explanation:** That is the definition of DDT: one function, many rows of data. DDT separates test logic from test data, so adding a scenario means adding a row, not writing a new function.

- **Why others are wrong:**
  - A) That is the 'copy-paste smell' the lesson warns about; editing the logic then means editing every copy.
  - C) Data can live inline, in a Python module, in JSON, in CSV, in a database or elsewhere; the source is not what defines DDT.
  - D) Looping inside one test gives one result and hides later rows; parametrization gives a separate result per row.

</details>

---

### 2. Why does the lesson build data-file paths with `Path(__file__).parent / "test_data" / "cases.json"` instead of `open("test_data/cases.json")`?

- [ ] A) It makes `json.load` parse the file faster.
- [ ] B) It automatically converts the strings in the file to numbers and booleans.
- [ ] C) `json.load` refuses to open files given as plain strings.
- [ ] D) The file is found no matter which directory you launch `pytest` from.


<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** D) The file is found no matter which directory you launch `pytest` from.

**Explanation:** `__file__` is the path of the current test file, so the path is anchored to the file rather than to the current working directory. A relative path such as `open("test_data/cases.json")` only works when you run from one specific folder, which is a very common beginner bug.

- **Why others are wrong:**
  - A) Path building has no effect on parsing speed.
  - B) Type conversion is separate; CSV values in particular must be converted explicitly.
  - C) A plain relative string works only when the current folder happens to be the right one; that is the real problem, not a `json` restriction.

</details>

---

### 3. A `load_cases()` function that reads a JSON file is passed to `@pytest.mark.parametrize`. When does it run, and what happens if the JSON is broken?

- [ ] A) Just before each individual test; only that test fails.
- [ ] B) During teardown; the tests pass but a warning is printed.
- [ ] C) At collection time; the whole module fails to collect with a clear error before any test runs.
- [ ] D) Only when you run with `-v`; otherwise a broken file is ignored.


<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** C) At collection time; the whole module fails to collect with a clear error before any test runs.

**Explanation:** The decorator argument is evaluated when PyTest scans the files. The lesson calls this a feature because you learn about the problem before any test runs. `load_cases()` is called at collection time, so a broken data file is reported immediately and clearly.

- **Why others are wrong:**
  - A) The function runs once while the module is imported/collected, not per test.
  - B) Nothing about loading happens in teardown.
  - D) Loading is not tied to verbosity; a broken file stops collection.

</details>

---

### 4. The valid range for a discount percent is 0-100. Which set of inputs best applies **boundary value analysis**?

- [ ] A) -10, 25, 150
- [ ] B) 0, 50, 100 only
- [ ] C) 1, 2, 3, 4, 5
- [ ] D) -1, 0, 1, 99, 100, 101


<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** D) -1, 0, 1, 99, 100, 101

**Explanation:** Boundary analysis tests exactly at, just below and just above each boundary. Bugs love the edges, so test at, just below and just above each boundary: -1, 0, 1, 99, 100, 101.

- **Why others are wrong:**
  - A) That is equivalence partitioning: one representative per partition (below, in, above range). Useful, but it does not probe the edges.
  - B) It checks the two edges but never the values just outside the range, where off-by-one bugs live.
  - C) All values are in the valid range and far from the upper boundary; no edge is explored.

</details>

---

### 5. A data row is written as `pytest.param(19.995, 0, 20.0, id="rounding-bug-known", marks=pytest.mark.xfail(reason="BUG-1234", strict=False))`. If that row fails when the suite runs, how is it reported?

- [ ] A) As `failed`, and all the remaining rows are skipped.
- [ ] B) As `skipped`, because `xfail` and `skip` are the same.
- [ ] C) As an `error`, because the bug id is not registered.
- [ ] D) As `xfailed` (an expected failure); the other rows are unaffected.


<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** D) As `xfailed` (an expected failure); the other rows are unaffected.

**Explanation:** `xfail` on a `pytest.param` applies to that single row, and an expected failure is not counted as a failure. A single bad row can be marked without disabling the whole test; with `strict=True` an unexpected pass would become a failure.

- **Why others are wrong:**
  - A) Marks on `pytest.param` apply only to that row; other rows still run.
  - B) `skip` never runs the test; `xfail` runs it and expects it to fail.
  - C) The `reason` text is free text; it is not registered anywhere.

</details>

---

### 6. Why can the assertion `assert (age >= 18, "Expected an adult")` never fail?

- [ ] A) PyTest disables assertion rewriting whenever a message is present.
- [ ] B) Python raises a `SyntaxError`, so the test is never collected.
- [ ] C) The parentheses build a non-empty tuple, and a non-empty tuple is always truthy.
- [ ] D) `assert` accepts a message only through `pytest.fail`.


<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** C) The parentheses build a non-empty tuple, and a non-empty tuple is always truthy.

**Explanation:** The correct form is `assert condition, "message"` with a comma and no parentheses around the pair. Never put the message in parentheses with the condition; a non-empty tuple is always true.

- **Why others are wrong:**
  - A) Messages work normally; the problem is the tuple created by the parentheses.
  - B) Only a warning is produced (a `SyntaxWarning` in Python); the test still runs and passes.
  - D) `assert condition, "message"` is valid Python and PyTest shows the message with its own introspection.

</details>

---

### 7. What does setting `__tracebackhide__ = True` in an assertion helper do?

- [ ] A) It makes the helper run faster by skipping its checks.
- [ ] B) It hides the failure message so that the test passes quietly.
- [ ] C) It omits the helper's frame from failure reports, so the traceback points at the line in the test that called the helper.
- [ ] D) It tells PyTest to rewrite the helper module so it shows full introspection.


<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** C) It omits the helper's frame from failure reports, so the traceback points at the line in the test that called the helper.

**Explanation:** It only affects readability, not correctness. Use it in every assertion helper so reports show the test line instead of the helper internals.

- **Why others are wrong:**
  - A) The checks still run; only the report changes.
  - B) The test still fails and the message is still shown.
  - D) Rewriting helpers is done with `pytest.register_assert_rewrite`, not with this variable.

</details>

---

### 8. A plain helper module `helpers/assertions.py` contains a bare `assert x == y` with no message. Why is its failure output less detailed than in a test file?

- [ ] A) Helper modules run before PyTest starts, so the output is lost.
- [ ] B) `assert` statements are ignored outside files named `test_*.py`.
- [ ] C) Introspection only works when the values compared are strings.
- [ ] D) PyTest rewrites test modules, `conftest.py` files and plugins by default, but not plain helper modules, so only `AssertionError` is shown.


<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** D) PyTest rewrites test modules, `conftest.py` files and plugins by default, but not plain helper modules, so only `AssertionError` is shown.

**Explanation:** Fix it with explicit messages or by calling `pytest.register_assert_rewrite("helpers.assertions")` before the import. Either write explicit messages in helper asserts (simplest) or register the helper module for assertion rewriting.

- **Why others are wrong:**
  - A) Helpers run normally during the test; the issue is rewriting, not timing.
  - B) They still run and raise `AssertionError`; they just lack the rich introspection.
  - C) Introspection works for many kinds of values; it is the missing rewrite that matters here.

</details>

---

### 9. What does `assert 1050 == pytest.approx(1000, rel=0.05)` check, and does it pass?

- [ ] A) It allows a relative tolerance of 5 percent of the expected value, so 1050 is accepted and the assertion passes.
- [ ] B) It sets an absolute tolerance of 0.05, so 1050 is rejected and the assertion fails.
- [ ] C) It rounds both numbers to 5 decimal places and compares them, so it fails.
- [ ] D) It ignores `rel` for integers and uses the default tolerance of 1e-6, so it fails.


<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** A) It allows a relative tolerance of 5 percent of the expected value, so 1050 is accepted and the assertion passes.

**Explanation:** 5 percent of 1000 is 50, and 1050 is exactly within that distance. `pytest.approx` accepts `abs=` for absolute and `rel=` for relative tolerance, overriding the defaults (relative 1e-6, absolute 1e-12).

- **Why others are wrong:**
  - B) `abs=` sets an absolute tolerance; `rel=` sets a relative one.
  - C) `approx` does not round to decimal places; it uses tolerances.
  - D) `rel=` overrides the default relative tolerance of 1e-6 for any numbers.

</details>

---

### 10. In which situation does the lesson say a **soft assertion** is inappropriate?

- [ ] A) When validating twelve independent fields on a form.
- [ ] B) When later steps depend on earlier ones, for example checking the dashboard after the login already failed.
- [ ] C) When you want one report listing every mismatching column of a migrated record.
- [ ] D) Whenever the test uses a fixture.


<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** B) When later steps depend on earlier ones, for example checking the dashboard after the login already failed.

**Explanation:** Continuing after a dependent step fails produces cascading, meaningless failures. Use normal asserts when steps depend on each other; use soft assertions for independent checks.

- **Why others are wrong:**
  - A) That is exactly the case soft assertions are good for: you see all failures at once.
  - C) This is a listed real-world use of soft assertions.
  - D) The lesson's `soft` fixture is itself a fixture, so fixtures are not the problem.

</details>

---

### 11. A beginner writes `try: withdraw(100, -5)` / `except ValueError: pass` in a test. What is wrong with it?

- [ ] A) It passes even if `withdraw` stops raising, so it can never detect the regression.
- [ ] B) `ValueError` cannot be caught inside a test function.
- [ ] C) `pass` makes PyTest mark the test as skipped.
- [ ] D) It fails whenever `withdraw` raises the expected error.


<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** A) It passes even if `withdraw` stops raising, so it can never detect the regression.

**Explanation:** If no exception is raised the `try` block simply finishes and the test passes in both the correct and the broken world. Use `with pytest.raises(ValueError):`, which fails with `DID NOT RAISE` when nothing is raised.

- **Why others are wrong:**
  - B) Python catches it fine; that is why the test passes silently.
  - C) `pass` is an ordinary statement; the test is reported as passed.
  - D) The opposite is true: the expected error is swallowed and the test passes.

</details>

---

### 12. How does the `match=` argument of `pytest.raises` compare against the exception?

- [ ] A) It must equal the whole message exactly, character for character.
- [ ] B) It compares the exception class name, not the message.
- [ ] C) It is a regular expression searched in `str(exception)` with `re.search`.
- [ ] D) It is a plain substring test and special characters are always safe.


<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** C) It is a regular expression searched in `str(exception)` with `re.search`.

**Explanation:** Plain words usually match themselves, but regex special characters need escaping. `match` takes a regular expression and uses `re.search`; use `re.escape` when the message contains special characters.

- **Why others are wrong:**
  - A) Only if you anchor with `^` and `$`; by default it is a search.
  - B) The class is the first argument; `match` looks at the message.
  - D) It is a regex, so characters like `(`, `)` or `.` have special meaning; use `re.escape`.

</details>

---

### 13. Why does the lesson warn against `pytest.raises(Exception)` with no `match`?

- [ ] A) It is a syntax error in PyTest 8.
- [ ] B) It also passes when the code has an unrelated bug such as `NameError` or `AttributeError`, hiding real defects.
- [ ] C) It only works for exceptions defined in `bank.py`.
- [ ] D) It makes PyTest skip the test body.


<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** B) It also passes when the code has an unrelated bug such as `NameError` or `AttributeError`, hiding real defects.

**Explanation:** Prefer the most specific type, or pair a broad type with a strict `match`. A broad exception type turns the test into one that passes for the wrong reasons.

- **Why others are wrong:**
  - A) It is valid; it is just too permissive.
  - C) It accepts any ordinary exception, which is exactly the problem.
  - D) The body runs normally; the issue is what it accepts.

</details>

---

### 14. What is the purpose of `nullcontext` (imported as `does_not_raise`) in a parametrized exception table?

- [ ] A) It silences every exception raised in the test.
- [ ] B) It marks the row as `xfail`.
- [ ] C) It lets one table mix success rows and rows that must raise, because each row carries its own context manager and no `if/else` is needed in the test body.
- [ ] D) It makes PyTest run the row in a separate process.


<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** C) It lets one table mix success rows and rows that must raise, because each row carries its own context manager and no `if/else` is needed in the test body.

**Explanation:** Rows that succeed use `does_not_raise()`; rows that must fail use `pytest.raises(...)`. `nullcontext` is a context manager that does nothing, used for the 'no exception expected' rows.

- **Why others are wrong:**
  - A) It does nothing at all; it is simply a context manager that does not intervene.
  - B) Expected failures are marked with `pytest.mark.xfail`, a different mechanism.
  - D) It has nothing to do with process isolation.

</details>

---

### 15. `load_config` does `raise ConfigError("Config is not valid JSON") from exc`. How can a test confirm the original `json.JSONDecodeError` was preserved?

- [ ] A) Capture `excinfo` and assert that `excinfo.value.__cause__` is a `json.JSONDecodeError`.
- [ ] B) Check `excinfo.type` is `json.JSONDecodeError`.
- [ ] C) Use `pytest.warns(json.JSONDecodeError)`.
- [ ] D) Original exceptions are lost when you use `raise ... from ...`.


<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** A) Capture `excinfo` and assert that `excinfo.value.__cause__` is a `json.JSONDecodeError`.

**Explanation:** `raise NewError(...) from exc` stores `exc` in `NewError.__cause__`. A good test confirms both the friendly error and its cause.

- **Why others are wrong:**
  - B) `excinfo.type` is the outer `ConfigError`, the exception that actually escaped.
  - C) `pytest.warns` is for warnings, not exceptions.
  - D) The `from` clause is exactly what keeps the original as the cause.

</details>

---

### 16. What does `testpaths = tests` in `pytest.ini` do?

- [ ] A) It makes PyTest import every file in `tests` as a module named `tests`.
- [ ] B) It registers the `tests` folder as a custom marker.
- [ ] C) It restricts PyTest so that tests outside `tests` can never be run, even by file name.
- [ ] D) When you run plain `pytest` from the root, PyTest looks only in `tests`, so it does not scan `src/`, `reports/` or virtual environments.


<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** D) When you run plain `pytest` from the root, PyTest looks only in `tests`, so it does not scan `src/`, `reports/` or virtual environments.

**Explanation:** It tells PyTest where to look for tests by default. `testpaths` keeps discovery fast and focused.

- **Why others are wrong:**
  - A) It controls where to search, not how modules are named.
  - B) Markers are registered under `markers`.
  - C) It only sets the default search location for a plain `pytest` run.

</details>

---

### 17. What does `pythonpath = src tests` add to the project?

- [ ] A) It adds those folders to Python's import path, so tests can write `from qe_utils.pricing import ...` and `from helpers.assertions import ...` without installing the package or hacking `sys.path`.
- [ ] B) It tells PyTest which folders to delete after the run.
- [ ] C) It makes every file in those folders a test file.
- [ ] D) It installs the packages listed in `requirements.txt`.


<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** A) It adds those folders to Python's import path, so tests can write `from qe_utils.pricing import ...` and `from helpers.assertions import ...` without installing the package or hacking `sys.path`.

**Explanation:** It is available since PyTest 7. `pythonpath` makes imports from `src` and `tests/helpers` work consistently.

- **Why others are wrong:**
  - B) It has no cleanup role.
  - C) File discovery still follows `test_*.py` / `*_test.py`.
  - D) Installation is done with `pip`; `pythonpath` only changes where Python searches for imports.

</details>

---

### 18. Two files `tests/unit/test_login.py` and `tests/integration/test_login.py` exist without `__init__.py`, and PyTest reports an "import file mismatch" error. Which fix does the lesson give?

- [ ] A) Give the files unique names, add `__init__.py` to the test folders, or use `--import-mode=importlib`.
- [ ] B) Rename `pytest.ini` to `tox.ini`.
- [ ] C) Add `--strict-markers` to `addopts`.
- [ ] D) Mark one of the files with `@pytest.mark.skip`.


<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** A) Give the files unique names, add `__init__.py` to the test folders, or use `--import-mode=importlib`.

**Explanation:** With the default `prepend` import mode, duplicate basenames need one of these. A beginner-safe rule: unique test file names, or `__init__.py` in the test folders.

- **Why others are wrong:**
  - B) The config file name has no influence on this error.
  - C) That option is about marker typos.
  - D) Skipping happens after import; the collection error would remain.

</details>

---

### 19. What is the main benefit of a test-data builder such as `build_user(**overrides)`?

- [ ] A) It makes every user identical so that tests can share them.
- [ ] B) It replaces the need for fixtures completely.
- [ ] C) Each test states only the field it cares about (for example `active=False`), and when a new required field appears only the builder changes.
- [ ] D) It hides all Arrange, Act and Assert lines inside helpers.


<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** C) Each test states only the field it cares about (for example `active=False`), and when a new required field appears only the builder changes.

**Explanation:** The builder supplies sensible defaults and `user.update(overrides)` replaces only what the test overrides. Builders highlight intent and centralise defaults.

- **Why others are wrong:**
  - A) The builder creates unique ids and usernames with `itertools.count`.
  - B) Builders and fixtures work together; factory fixtures wrap builders when cleanup is needed.
  - D) The lesson warns that over-abstracting hurts readability; keep the Act and Assert lines visible.

</details>

---

### 20. What does `pytestmark = pytest.mark.unit` at the top of a test module do?

- [ ] A) It marks only the first test in the file.
- [ ] B) It registers the `unit` marker in `pytest.ini`.
- [ ] C) It makes the module run before all others.
- [ ] D) It applies the `unit` marker to every test in that module.


<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** D) It applies the `unit` marker to every test in that module.

**Explanation:** Use a list to apply several markers: `pytestmark = [pytest.mark.unit, pytest.mark.regression]`. `pytestmark` is a module-level variable PyTest reads to apply markers to all tests in the file.

- **Why others are wrong:**
  - A) A module-level `pytestmark` applies to all tests in the module.
  - B) Registration is done under `markers` in the config file.
  - C) Markers select tests; they do not set execution order.

</details>

---

### 21. What is a factory fixture, as shown with `make_user`?

- [ ] A) A fixture that runs automatically for every test in the project.
- [ ] B) A fixture that returns a function the test can call as many times as needed, with optional teardown after `yield`.
- [ ] C) A fixture that can only create one object per session.
- [ ] D) A fixture that must be imported from `conftest.py`.


<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** B) A fixture that returns a function the test can call as many times as needed, with optional teardown after `yield`.

**Explanation:** The test calls `make_user(username="ana")` and `make_user(username="ben")`. Factory fixtures return a function so tests can create several objects and teardown can clean them up.

- **Why others are wrong:**
  - A) That would be an autouse fixture; a factory fixture is only used when requested.
  - C) The returned function can be called repeatedly.
  - D) Fixtures are injected by name, not imported.

</details>

---

### 22. In the PyTest report, what is the difference between a **failure (F)** and an **error (E)**?

- [ ] A) A failure is a skipped test and an error is an expected failure.
- [ ] B) An error is a failure that was fixed on a re-run.
- [ ] C) A failure means the test body ran and an assertion or other exception failed; an error means something went wrong outside the test body, usually in fixture setup or teardown.
- [ ] D) There is no difference; both letters mean the assertion was false.


<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** C) A failure means the test body ran and an assertion or other exception failed; an error means something went wrong outside the test body, usually in fixture setup or teardown.

**Explanation:** The distinction tells you whether the product misbehaved or the test environment is broken. Fail versus error shows whether to look at the product or at the test environment.

- **Why others are wrong:**
  - A) Those are `s` (skipped) and `x` (xfailed).
  - B) Re-runs are not part of the definition.
  - D) An error is not an assertion problem; it is a setup/teardown problem.

</details>

---

### 23. Why add `--self-contained-html` when you attach a report to an email or a Jira ticket?

- [ ] A) It compresses the report into a zip file.
- [ ] B) It also generates the JUnit XML file.
- [ ] C) It embeds the CSS, JavaScript and images inside the single HTML file, so the formatting is not lost.
- [ ] D) It encrypts the report so only teammates can open it.


<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** C) It embeds the CSS, JavaScript and images inside the single HTML file, so the formatting is not lost.

**Explanation:** By default the report references an `assets/` folder next to the HTML file. Without the flag, a mailed `.html` would lose its styling.

- **Why others are wrong:**
  - A) The output is still a single `.html` file.
  - B) JUnit XML needs `--junitxml`.
  - D) Nothing is encrypted; the flag only bundles resources.

</details>

---

### 24. Which report format do CI servers such as Jenkins or GitHub Actions consume for dashboards and trend charts, and how is it produced?

- [ ] A) The `pytest-html` report, produced with `--html`.
- [ ] B) The terminal report, saved with `-q`.
- [ ] C) A JUnit XML file, which requires installing `pytest-html` first.
- [ ] D) JUnit XML, produced by PyTest itself with `--junitxml=reports/junit.xml` and no plugin.


<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** D) JUnit XML, produced by PyTest itself with `--junitxml=reports/junit.xml` and no plugin.

**Explanation:** HTML is for people; JUnit XML is for machines. Use `--junitxml` for CI tooling, and HTML for humans.

- **Why others are wrong:**
  - A) HTML is readable but not easily machine-parsed.
  - B) The terminal report disappears and is not a CI interchange format.
  - C) `--junitxml` is built into PyTest.

</details>

---

### 25. After adding a `Description` column, the HTML table looks misaligned. According to the lesson, what is the likely cause?

- [ ] A) The header hook and the row hook insert a different number of cells (or at different positions).
- [ ] B) The report was not created with `--self-contained-html`.
- [ ] C) `pytest-metadata` is missing.
- [ ] D) The test file names do not start with `test_`.


<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** A) The header hook and the row hook insert a different number of cells (or at different positions).

**Explanation:** They must stay symmetrical. Insert exactly one cell at the same index in both `pytest_html_results_table_header` and `pytest_html_results_table_row`.

- **Why others are wrong:**
  - B) That flag affects styling resources, not column alignment.
  - C) That would cause `ModuleNotFoundError`, not misalignment.
  - D) Such tests would not be collected at all.

</details>

---

### 26. Running `pytest --html=reports/report.html` prints `unrecognized arguments: --html=...`. What is the usual cause?

- [ ] A) The `reports/` folder does not exist yet.
- [ ] B) `pytest-html` is not installed in the active environment, for example because the virtual environment is not active.
- [ ] C) PyTest 8 removed the `--html` option.
- [ ] D) The report must be named `report.xml`.


<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** B) `pytest-html` is not installed in the active environment, for example because the virtual environment is not active.

**Explanation:** Fix it with `python -m pip install pytest-html`. The option appears only when the plugin is installed in the Python environment you are running.

- **Why others are wrong:**
  - A) Parent folders are created if needed.
  - C) The option comes from the plugin, not from PyTest itself.
  - D) The extension is not the issue.

</details>

---

### 27. The lesson describes two meanings of "performance" in testing. Which pair is correct?

- [ ] A) The speed of the test suite (why is my test run slow?) and the speed of the code under test (is it fast enough?).
- [ ] B) The memory used by the browser and the size of the report.
- [ ] C) The number of tests and the number of passed tests.
- [ ] D) Load testing with 1,000 users and unit testing.


<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** A) The speed of the test suite (why is my test run slow?) and the speed of the code under test (is it fast enough?).

**Explanation:** Different tools fit each question. Keep the two apart: suite health versus product behaviour.

- **Why others are wrong:**
  - B) These are not the two meanings given.
  - C) Counts are not speed measurements.
  - D) The lesson says real load testing belongs to dedicated tools; it is not one of the two meanings.

</details>

---

### 28. In `--durations` output you see `1.00s setup tests/test_slow.py::test_with_database`. What does a slow `setup` phase point to?

- [ ] A) A slow test body, so the assertions should be rewritten.
- [ ] B) A heavy fixture, not a slow test body; a wider fixture scope may help.
- [ ] C) A slow report generator.
- [ ] D) A collection problem caused by import errors.


<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** B) A heavy fixture, not a slow test body; a wider fixture scope may help.

**Explanation:** Each test has setup, call and teardown phases, listed separately. Read the phase label: setup is fixtures, call is the body, teardown is cleanup.

- **Why others are wrong:**
  - A) The test body is the `call` phase.
  - C) Reports are not part of the setup phase.
  - D) Collection is measured separately, e.g. with `--collect-only`.

</details>

---

### 29. In `cProfile` output, what is the difference between `tottime` and `cumtime`?

- [ ] A) `tottime` is time inside the function itself excluding sub-calls; `cumtime` includes the functions it calls.
- [ ] B) `tottime` is the total for the whole run and `cumtime` is the time for the last call only.
- [ ] C) `tottime` counts only setup and `cumtime` only teardown.
- [ ] D) They are always equal.


<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** A) `tottime` is time inside the function itself excluding sub-calls; `cumtime` includes the functions it calls.

**Explanation:** `-s cumulative` sorts by `cumtime`. `tottime` points at the function's own code; `cumtime` shows the cost of the whole call tree below it.

- **Why others are wrong:**
  - B) Both are per-function figures.
  - C) Those are pytest phases, not profiler columns.
  - D) They differ whenever a function calls other functions.

</details>

---

### 30. Why does the lesson recommend a **generous** budget (for example 5-10 times the typical time) in a time-budget test?

- [ ] A) A busy CI machine can make the same code several times slower, so tight budgets make flaky tests.
- [ ] B) `assert elapsed < 0.01` is a syntax error.
- [ ] C) Timing tests are skipped automatically on CI.
- [ ] D) A generous budget makes the code faster.


<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** A) A busy CI machine can make the same code several times slower, so tight budgets make flaky tests.

**Explanation:** Prefer relative comparisons and include the measured value in the failure message. Timing tests are among the flakiest tests, so budgets must allow for machine noise.

- **Why others are wrong:**
  - B) It is valid code; it is just fragile.
  - C) They run; that is why they can fail unexpectedly.
  - D) The budget only judges the result; it does not change speed.

</details>

---

### 31. What is `pytest-timeout` for?

- [ ] A) It measures how fast your code is and records the mean time.
- [ ] B) It runs tests in parallel on all CPU cores.
- [ ] C) It adds `time.sleep` to flaky tests.
- [ ] D) It stops hung tests: a test that exceeds the limit fails with a clear message instead of blocking the pipeline.


<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** D) It stops hung tests: a test that exceeds the limit fails with a clear message instead of blocking the pipeline.

**Explanation:** `timeout = 60` sets the default and `@pytest.mark.timeout(2)` overrides it per test. Do not confuse the timeout (a safety net) with a performance assertion.

- **Why others are wrong:**
  - A) That is the job of `pytest-benchmark`; the timeout is a safety net, not a measurement.
  - B) That is `pytest-xdist`.
  - C) Adding sleeps is listed as a mistake; the plugin does not add them.

</details>

---

### 32. In the broken file, the `cart` fixture has `scope="session"`, `test_cart_add` adds an item, and `test_cart_is_empty_again` then fails. Why, and what is the fix?

- [ ] A) The `Cart` class is broken; rewrite `add`.
- [ ] B) `pytest.approx` is missing; add it.
- [ ] C) The marker `smoek` caused a collection error.
- [ ] D) State leaks between tests because the same `Cart` object is shared; use the default function scope.


<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** D) State leaks between tests because the same `Cart` object is shared; use the default function scope.

**Explanation:** Wider scopes are safe only for read-only or resettable resources. Function-scoped fixtures give each test a fresh cart.

- **Why others are wrong:**
  - A) The class works; the shared fixture instance is the problem.
  - B) Floats are not involved in the failing emptiness check.
  - C) That is a separate problem (a misspelt marker) and does not explain the leaked item.

</details>

---

### 33. PyTest reports `'smoek' not found in markers configuration option`. What does it mean?

- [ ] A) A misspelt or unregistered marker was used while `--strict-markers` is enabled.
- [ ] B) The `smoke` fixture is missing from `conftest.py`.
- [ ] C) The test file name does not match `test_*.py`.
- [ ] D) `pytest-html` is not installed.


<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** A) A misspelt or unregistered marker was used while `--strict-markers` is enabled.

**Explanation:** Register the marker or fix the typo. The error decoder table maps this message to a marker typo or missing registration.

- **Why others are wrong:**
  - B) Markers are not fixtures.
  - C) That would give `collected 0 items`.
  - D) That would give `unrecognized arguments: --html`.

</details>

---

### 34. What causes a `ScopeMismatch` error?

- [ ] A) Two test files have the same name in different folders.
- [ ] B) A wide-scope fixture requests a narrower-scope fixture.
- [ ] C) A fixture function was called directly like a normal function.
- [ ] D) `parametrize` names do not match the function parameters.


<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** B) A wide-scope fixture requests a narrower-scope fixture.

**Explanation:** Widen the dependency's scope or narrow the dependent's. Match the message to its cause using the error-decoder table.

- **Why others are wrong:**
  - A) That produces `import file mismatch`.
  - C) That produces `fixture ... called directly`.
  - D) That produces `function uses no argument`.

</details>

---

### 35. `@pytest.mark.parametrize("price, percent", [(100, 10, 90)])` decorates `def test_discount_values(price, percent, expected)`. What is wrong?

- [ ] A) Nothing; PyTest fills `expected` automatically.
- [ ] B) Rows in `parametrize` must be dictionaries, not tuples.
- [ ] C) The test needs `@pytest.mark.smoke` to receive `expected`.
- [ ] D) The decorator names two parameters but each row has three values and the test needs `expected`; it should be `"price, percent, expected"`.


<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** D) The decorator names two parameters but each row has three values and the test needs `expected`; it should be `"price, percent, expected"`.

**Explanation:** Names in `parametrize` must align with the function parameters and the row values. Misaligned names and values is one of the five bugs in the debugging task.

- **Why others are wrong:**
  - A) PyTest has no such behaviour.
  - B) Tuples are fine.
  - C) Markers do not supply arguments.

</details>

---

### 36. Why does the model `checkout(cart, inventory, now=None)` accept `now` as a parameter?

- [ ] A) To make the function slower on purpose.
- [ ] B) Tests can pass a fixed time and check `placed_at` exactly; injecting the dependency makes the function easy to test.
- [ ] C) Because `datetime` cannot be imported in tests.
- [ ] D) So that `checkout` never needs an inventory client.


<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** B) Tests can pass a fixed time and check `placed_at` exactly; injecting the dependency makes the function easy to test.

**Explanation:** The lesson calls this dependency injection. Passing time in avoids depending on the real clock.

- **Why others are wrong:**
  - A) Speed is unrelated.
  - C) It can be imported; a fixed value just makes results predictable.
  - D) `inventory` is still required.

</details>

---

## Part 2: True / False

### 37. Writing an `if expected_error:` branch inside a data-driven test body is the recommended way to handle rows that should raise an exception.

- [ ] True
- [ ] False

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** False

**Explanation:** The lesson lists this as a mistake: the test becomes a mini-program. Split positive and negative cases into separate tests.

</details>

---

### 38. A test that computes `expected = a + b` and then asserts `a + b == expected` can never fail, because the expected value is computed with the same expression.

- [ ] True
- [ ] False

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** True

**Explanation:** This tautology proves nothing. Hard-code the expected value from the specification and call the real function under test.

</details>

---

### 39. `pytest_assertrepr_compare` is a hook placed in `conftest.py` or a plugin; it returns a list of strings (the first being a summary) or `None` to let PyTest explain the comparison as usual.

- [ ] True
- [ ] False

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** True

**Explanation:** The function name and parameters (`op`, `left`, `right`) must match exactly for PyTest to call it.

</details>

---

### 40. It is fine to place `assert` statements about `excinfo` inside the `with pytest.raises(...)` block, right after the raising line.

- [ ] True
- [ ] False

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** False

**Explanation:** Code after the raising line inside the block never runs, and `excinfo` is filled only once the block exits. Assert after the block.

</details>

---

### 41. Each test method in a `Test*` class gets a new instance of the class, so instance attributes do not carry over between tests.

- [ ] True
- [ ] False

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** True

**Explanation:** Never rely on sharing state through `self`; use fixtures for set-up instead.

</details>

---

### 42. You need to install `pytest-html` before PyTest can produce a JUnit XML report with `--junitxml`.

- [ ] True
- [ ] False

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** False

**Explanation:** JUnit XML is built into PyTest and needs no plugin; `pytest-html` is only for the HTML report.

</details>

---

### 43. `time.time()` is the best clock for measuring how long a block of code takes.

- [ ] True
- [ ] False

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** False

**Explanation:** It follows the system clock, which can jump. Use `time.perf_counter()`, which is monotonic and more precise.

</details>

---

### 44. When repeating a `timeit` measurement several times, taking the minimum is recommended because noise only ever makes things slower.

- [ ] True
- [ ] False

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** True

**Explanation:** Use `timeit.repeat(...)` and take the minimum for a more stable figure.

</details>

---

### 45. When debugging a failing test, read the error output from the bottom up: the last `E ...` lines say what went wrong and the lines above say where.

- [ ] True
- [ ] False

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** True

**Explanation:** This is one of the assessment strategy tips.

</details>

---

## Part 3: Code Prediction

### 46. A CSV row is read with `csv.DictReader`. What does this code print?

```python
import csv, io

data = "case_id,a,expected\nplus,5,true\n"
row = next(csv.DictReader(io.StringIO(data)))
print(row["a"] == 5, int(row["a"]) == 5, row["expected"].strip().lower() == "true")
```

- [ ] A) `True True True`
- [ ] B) `False True True`
- [ ] C) `False False True`
- [ ] D) `TypeError`


<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** B) `False True True`

**Explanation:** Everything read from a CSV is a string; numbers need `int()`/`float()` and booleans need explicit parsing such as `.strip().lower() == "true"`.

- **Why others are wrong:**
  - A) Values from a CSV are strings, so `"5" == 5` is `False` until you convert with `int()`.
  - C) After `int(row["a"])` the comparison with `5` is `True`.
  - D) Comparing a string with an int using `==` is allowed; it simply returns `False`.

*(Verified by running this snippet with pytest/python in the sandbox.)*

</details>

---

### 47. Which test IDs does PyTest generate for this parametrized test (shown by `pytest --collect-only -q`)?

```python
import pytest

@pytest.mark.parametrize(
    "price, percent, expected",
    [
        pytest.param(100.0, 10, 90.0, id="ten-percent"),
        (80.0, 50, 40.0),
        pytest.param(100.0, 0, 100.0, id="no-discount"),
    ],
)
def test_discount(price, percent, expected):
    assert price * (1 - percent / 100) == expected
```

- [ ] A) `test_discount[0]`, `test_discount[1]`, `test_discount[2]`
- [ ] B) `test_discount[100.0-10-90.0]`, `test_discount[80.0-50-40.0]`, `test_discount[100.0-0-100.0]`
- [ ] C) `test_discount[ten-percent]`, `test_discount[80.0-50-40.0]`, `test_discount[no-discount]`
- [ ] D) `test_discount[ten-percent]`, `test_discount[data1]`, `test_discount[no-discount]`


<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** C) `test_discount[ten-percent]`, `test_discount[80.0-50-40.0]`, `test_discount[no-discount]`

**Explanation:** Rows with `id=` get that name; a row without it gets an ID built from its values. All three tests pass.

- **Why others are wrong:**
  - A) PyTest builds IDs from the values for numbers, not plain indexes; rows with `id=` use that name.
  - B) `id=` replaces the generated value-based name for those two rows.
  - D) `data0`, `data1` appear for objects, dictionaries or long strings; plain numbers produce `80.0-50-40.0`.

*(Verified by running this snippet with pytest/python in the sandbox.)*

</details>

---

### 48. What is the result of running this test file?

```python
def test_age_is_adult():
    age = 17
    assert (age >= 18, "Expected an adult")
```

- [ ] A) 1 failed with `AssertionError: Expected an adult`
- [ ] B) 1 error: the file has a `SyntaxError` and is not collected
- [ ] C) 1 skipped because the message is a tuple
- [ ] D) 1 passed (with a warning about the assertion always being true)


<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** D) 1 passed (with a warning about the assertion always being true)

**Explanation:** `assert (cond, "msg")` asserts a non-empty tuple, which is always true. Write `assert cond, "msg"`.

- **Why others are wrong:**
  - A) A non-empty tuple is truthy, so the assertion cannot fail.
  - B) It is valid Python; only a warning is raised.
  - C) PyTest does not skip tests for this.

*(Verified by running this snippet with pytest/python in the sandbox.)*

</details>

---

### 49. What does PyTest report for this file?

```python
import pytest

def test_exact():
    assert 0.1 + 0.2 == 0.3

def test_approx():
    assert 0.1 + 0.2 == pytest.approx(0.3)
```

- [ ] A) 1 failed, 1 passed
- [ ] B) 2 passed
- [ ] C) 2 failed
- [ ] D) 1 passed, 1 error


<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** A) 1 failed, 1 passed

**Explanation:** Binary floating point makes `0.1 + 0.2 == 0.3` false; `pytest.approx` compares within a tolerance.

- **Why others are wrong:**
  - B) `0.1 + 0.2` is `0.30000000000000004`, so the exact comparison fails.
  - C) `pytest.approx(0.3)` accepts the tiny binary rounding difference.
  - D) The failing test fails in its body; an error would need a fixture problem.

*(Verified by running this snippet with pytest/python in the sandbox.)*

</details>

---

### 50. A `soft` fixture (like the lesson's) runs `pytest.fail(...)` after the `yield` because earlier soft checks failed, while the test body itself finishes normally. How does PyTest report this?

```python
import pytest

@pytest.fixture
def soft_check():
    yield
    pytest.fail("soft assertion(s) failed", pytrace=False)

def test_body_is_fine(soft_check):
    assert 1 + 1 == 2
```

- [ ] A) As a failure (F) of the test body
- [ ] B) As a skipped test (s)
- [ ] C) As an error (E) at teardown, not as a failure (F); the test body itself passed
- [ ] D) It is ignored and everything is green


<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** C) As an error (E) at teardown, not as a failure (F); the test body itself passed

**Explanation:** A failure in teardown is reported as an error, which can confuse readers; calling `soft.assert_all()` explicitly as the last line of the test is an alternative.

- **Why others are wrong:**
  - A) The failure happens in teardown, outside the test body, which is classified as an error.
  - B) `pytest.fail` never produces a skip.
  - D) PyTest does report a teardown failure.

*(Verified by running this snippet with pytest/python in the sandbox.)*

</details>

---

### 51. What is the outcome of this test?

```python
import pytest

def test_parse_rejects_text():
    with pytest.raises(ValueError):
        int("42")
```

- [ ] A) Passes, because `int` is a built-in
- [ ] B) Fails with `DID NOT RAISE`
- [ ] C) Fails with `ValueError: invalid literal for int()`
- [ ] D) Error during setup


<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** B) Fails with `DID NOT RAISE`

**Explanation:** If no exception is raised, `pytest.raises` makes the test fail with `Failed: DID NOT RAISE`.

- **Why others are wrong:**
  - A) `int("42")` succeeds, so nothing is raised and `pytest.raises` fails the test.
  - C) That message belongs to `int("abc")`; `"42"` converts fine.
  - D) There is no fixture; the failure happens in the test body.

*(Verified by running this snippet with pytest/python in the sandbox.)*

</details>

---

### 52. What happens when this test runs?

```python
import pytest

def test_msg_special():
    with pytest.raises(ValueError, match="cost (USD)"):
        raise ValueError("cost (USD)")
```

- [ ] A) It passes, because the text is identical to the message
- [ ] B) It fails: the regex pattern did not match, because the parentheses are regex special characters (use `re.escape`)
- [ ] C) It fails with `DID NOT RAISE`
- [ ] D) It passes with a warning


<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** B) It fails: the regex pattern did not match, because the parentheses are regex special characters (use `re.escape`)

**Explanation:** Special characters such as `(`, `)`, `.` need escaping; use `match=re.escape("cost (USD)")`. The test ran and failed with `Regex pattern did not match`.

- **Why others are wrong:**
  - A) `match` is a regular expression; `(USD)` is a group that matches `USD`, so the pattern looks for `cost USD`.
  - C) A `ValueError` is raised; the problem is only the pattern.
  - D) A non-matching `match` makes the test fail.

*(Verified by running this snippet with pytest/python in the sandbox.)*

</details>

---

### 53. Four rows use `does_not_raise()` or `pytest.raises(...)`. What does PyTest report?

```python
from contextlib import nullcontext as does_not_raise
import pytest

def withdraw(balance, amount):
    if amount <= 0:
        raise ValueError("amount must be positive")
    if amount > balance:
        raise RuntimeError("insufficient")
    return balance - amount

@pytest.mark.parametrize(
    "balance, amount, expected, expectation",
    [
        (100, 30, 70, does_not_raise()),
        (100, 101, None, pytest.raises(RuntimeError)),
        (100, -1, None, pytest.raises(ValueError)),
        (100, 0, None, pytest.raises(RuntimeError)),
    ],
)
def test_table(balance, amount, expected, expectation):
    with expectation:
        assert withdraw(balance, amount) == expected
```

- [ ] A) 4 passed
- [ ] B) 2 passed, 2 failed
- [ ] C) 3 passed, 1 failed
- [ ] D) 1 passed, 3 failed


<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** C) 3 passed, 1 failed

**Explanation:** A different exception type than the one expected propagates and fails the test; only the fourth row is wrong.

- **Why others are wrong:**
  - A) In the last row `withdraw(100, 0)` raises `ValueError`, not the expected `RuntimeError`, so that exception propagates and the row fails.
  - B) Only the last row has a mismatched exception type.
  - D) Rows 2 and 3 raise exactly the type they expect, so they pass.

*(Verified by running this snippet with pytest/python in the sandbox.)*

</details>

---

### 54. What does this code print?

```python
import itertools
_counter = itertools.count(1)

def build_user(**overrides):
    n = next(_counter)
    user = {"id": n, "username": f"user{n}", "email": f"user{n}@example.com",
            "age": 30, "active": True}
    user.update(overrides)
    return user

a = build_user()
b = build_user(active=False, username="ana")
print(a["username"], b["id"], b["username"], b["email"])
```

- [ ] A) `user1 1 ana user1@example.com`
- [ ] B) `user1 2 ana user2@example.com`
- [ ] C) `user1 2 user2 user2@example.com`
- [ ] D) `user0 1 ana user1@example.com`


<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** B) `user1 2 ana user2@example.com`

**Explanation:** Overrides replace only the named fields; the email is not overridden so it keeps the generated value built from `n`.

- **Why others are wrong:**
  - A) `next(_counter)` advances on every call, so the second user has id 2.
  - C) `username="ana"` is passed in `overrides` and replaces the default.
  - D) `itertools.count(1)` starts at 1, not 0.

*(Verified by running this snippet with pytest/python in the sandbox.)*

</details>

---

### 55. What is the final summary line for this file?

```python
import pytest

@pytest.fixture
def broken_fixture():
    raise RuntimeError("setup exploded")

def test_passes():
    assert 1 + 1 == 2

def test_fails():
    assert "apple".upper() == "Apple"

@pytest.mark.skip(reason="not built")
def test_skipped():
    assert False

@pytest.mark.xfail(reason="known bug")
def test_expected_failure():
    assert 2 * 2 == 5

def test_error_in_setup(broken_fixture):
    assert True
```

- [ ] A) 2 failed, 1 passed, 1 skipped, 1 xfailed
- [ ] B) 1 failed, 2 passed, 1 skipped, 1 error
- [ ] C) 1 failed, 1 passed, 1 skipped, 1 xfailed, 1 error
- [ ] D) 1 failed, 1 passed, 1 skipped, 1 xpassed, 1 error


<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** C) 1 failed, 1 passed, 1 skipped, 1 xfailed, 1 error

**Explanation:** The progress line is `.FsxE`: pass, fail, skip, xfail, error.

- **Why others are wrong:**
  - A) The setup problem is an error (E), not a failure.
  - B) An expected failure is reported as xfailed, not as passed.
  - D) `xpassed` would mean the xfail test unexpectedly passed, but `2 * 2 == 5` is false.

*(Verified by running this snippet with pytest/python in the sandbox.)*

</details>

---

### 56. What does this code print?

```python
from collections import Counter

def find_duplicates_fast(values):
    counts = Counter(values)
    return [value for value, count in counts.items() if count > 1]

print(find_duplicates_fast([1, 2, 2, 3, 3, 3, 4]))
```

- [ ] A) `[2, 2, 3, 3, 3]`
- [ ] B) `[3]`
- [ ] C) `[1, 4]`
- [ ] D) `[2, 3]`


<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** D) `[2, 3]`

**Explanation:** `Counter` counts occurrences in one pass, and the comprehension keeps values seen more than once.

- **Why others are wrong:**
  - A) The comprehension returns each repeated value once, not every occurrence.
  - B) A value is included if it appears more than once, not only the most frequent.
  - C) Those values appear once; the filter keeps counts greater than 1.

*(Verified by running this snippet with pytest/python in the sandbox.)*

</details>

---

### 57. What does PyTest report for this test?

```python
from unittest.mock import Mock

class InventoryClient:
    def stock_for(self, sku):
        raise RuntimeError("network")

def test_spec():
    inv = Mock(spec=InventoryClient)
    inv.stock_for.return_value = 10
    assert inv.stock_for("PEN") == 10
    inv.stok_for("PEN")
```

- [ ] A) It fails with `AttributeError`: the mock has no attribute `stok_for`
- [ ] B) It passes, because every mock method returns a Mock
- [ ] C) It fails on the `assert` line
- [ ] D) It passes with a warning about the typo


<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** A) It fails with `AttributeError`: the mock has no attribute `stok_for`

**Explanation:** `Mock(spec=...)` turns a misspelt method name into an `AttributeError`.

- **Why others are wrong:**
  - B) `spec=InventoryClient` restricts attributes to those that exist on the real class.
  - C) The assertion is true because `return_value` is 10.
  - D) A typo raises `AttributeError` instead of silently succeeding.

*(Verified by running this snippet with pytest/python in the sandbox.)*

</details>

---

## Part 4: Fill-in-the-Blank

### 58. Everything read from a CSV file is a `________`, so numbers must be converted with `int(...)` or `float(...)`.

**Your answer:** `____________`

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** string (`str`)

**Explanation:** The text `true` is not the boolean `True`, and `"5" == 5` is `False`; convert explicitly.

</details>

---

### 59. To get rich assertion introspection inside a helper module, call `pytest.________________("helpers.assertions")` before the module is imported, usually at the top of the root `conftest.py`.

**Your answer:** `____________`

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** `register_assert_rewrite`

**Explanation:** Without it, plain helper modules are not rewritten and only show `AssertionError` unless you add explicit messages.

</details>

---

### 60. In `with pytest.raises(InsufficientFundsError) as excinfo:`, the actual exception instance is available as `excinfo.________` (read it after the `with` block).

**Your answer:** `____________`

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** `value`

**Explanation:** `excinfo.type` is the class and `excinfo.value` is the instance, so you can read custom attributes such as `balance`.

</details>

---

### 61. In the Arrange-________-Assert pattern, the middle phase performs the one action under test.

**Your answer:** `____________`

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** Act

**Explanation:** A reader sees what is being tested from the Act line; tests that act many times usually test too much.

</details>

---

### 62. With `--strict-markers`, a typo such as `@pytest.mark.smoek` becomes an `________` instead of a quiet warning.

**Your answer:** `____________`

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** error

**Explanation:** Always enable it and register markers under `markers` in `pytest.ini`.

</details>

---

### 63. To embed CSS, JavaScript and images in a single HTML report, add the flag `--____________________` to `--html=reports/report.html`.

**Your answer:** `____________`

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** `--self-contained-html`

**Explanation:** Use it whenever the report is emailed, attached to a ticket or stored as a CI artifact.

</details>

---

### 64. In `conftest.py`, extra environment rows are added with `config.stash[________________]["Project"] = "Project 1"`, where the key is imported from `pytest_metadata.plugin`.

**Your answer:** `____________`

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** `metadata_key`

**Explanation:** `config._metadata` is the older spelling for pytest-metadata older than version 2.

</details>

---

### 65. PyTest can write a machine-readable report for CI tools, without any plugin, with `pytest --____________=reports/junit.xml`.

**Your answer:** `____________`

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** `--junitxml`

**Explanation:** JUnit XML is for CI tools; HTML is for people.

</details>

---

### 66. `pytest -n ____` starts one `pytest-xdist` worker per CPU core.

**Your answer:** `____________`

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** `auto`

**Explanation:** Parallel runs require independent tests; session-scoped fixtures run once per worker.

</details>

---

### 67. For measuring durations, use `time.________________()`, because it is monotonic and more precise than `time.time()`.

**Your answer:** `____________`

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** `perf_counter`

**Explanation:** Only the difference between two `perf_counter()` calls is meaningful.

</details>

---

### 68. The three-part formula for a short written explanation is What, Why, and `________`.

**Your answer:** `____________`

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** Trade-off

**Explanation:** Example: parametrize with `pytest.param` IDs; the trade-off is that very large tables become harder to read, so move them to JSON.

</details>

---

## Topic Coverage

| Topic (written lesson) | Question numbers | Count |
|---|---|---|
| Data-Driven Test Design | 1, 2, 3, 4, 5, 37, 38, 46, 47, 58 | 10 |
| Custom Assertions | 6, 7, 8, 9, 10, 39, 48, 49, 50, 59 | 10 |
| Exception Testing | 11, 12, 13, 14, 15, 40, 51, 52, 53, 60 | 10 |
| Test Organization and Reusable Templates | 16, 17, 18, 19, 20, 21, 41, 54, 61, 62 | 10 |
| HTML Reporting | 22, 23, 24, 25, 26, 42, 55, 63, 64, 65 | 10 |
| Performance Profiling | 27, 28, 29, 30, 31, 43, 44, 56, 66, 67 | 10 |
| PyTest Skills Assessment (Monday-Wednesday review) | 32, 33, 34, 35, 36, 45, 57, 68 | 8 |
| **Total** | 1-68 | **68** |
