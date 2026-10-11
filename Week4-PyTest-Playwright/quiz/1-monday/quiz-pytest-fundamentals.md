# Weekly Knowledge Check: Day 1 (Monday) PyTest Fundamentals

**Week 4: PyTest & Playwright | Quiz: `quiz-pytest-fundamentals.md`**

## Topics Covered Today

1. PyTest installation and configuration (virtual environments, `pip`, `requirements.txt`, `pytest.ini`, `pyproject.toml`, `testpaths`, `addopts`, `pythonpath`, strict options, rootdir/inifile)
2. Test discovery and organization (naming rules, `--collect-only`, node IDs, `__init__.py`, `--ignore`, `norecursedirs`)
3. Test functions and classes (Arrange-Act-Assert, naming, F.I.R.S.T., fresh instance per test, `skip`/`xfail` first look)
4. Assertions and assertion introspection (plain `assert`, rewriting, `pytest.approx`, `pytest.raises`, `pytest.warns`, common traps)
5. Markers (`skip`, `skipif`, `xfail`, custom markers, `--strict-markers`, `pytestmark`, `-m`)
6. Test execution and filtering (`-v`, `-s`, `--tb`, `-k` vs `-m`, `--lf`, `-x`, exit codes)

## Instructions

- This quiz has **66 questions** in four parts: Multiple Choice, True/False, Code Prediction and Fill in the Blank.
- Read each question and decide on your answer **before** opening the solution.
- Tick your choice by editing the checkbox (`- [x]`), or just note it down, then click **Click for Solution** to check yourself.
- Read the explanation even when you were right: it explains *why*, and (for multiple choice) why each wrong option is wrong.
- Code Prediction answers were verified by running the snippets with `python -m pytest`.
- If you miss several questions on a topic, re-read that lesson and try the practice exercises again.

---

## Part 1: Multiple Choice

### 1. According to the lesson, what is the main reason most modern Python teams choose PyTest over the built-in `unittest` module?
- [ ] A) PyTest cannot run `unittest` tests, so teams migrate away from them
- [ ] B) PyTest requires every test to inherit from `unittest.TestCase`
- [ ] C) PyTest replaces `assert` with methods such as `assertEqual`
- [ ] D) Simplicity: tests are plain functions that use the plain `assert` statement

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** D) Simplicity: tests are plain functions that use the plain `assert` statement

**Explanation:** PyTest needs very little boilerplate; a test can be a 2-line function with plain `assert`, whereas `unittest` needs a class, `self` and special assert methods.

- **Why others are wrong:**
  - A) The lesson states PyTest can also run existing `unittest` tests.
  - B) Inheriting from `TestCase` is the `unittest` style; PyTest tests are plain functions (class optional).
  - C) Those methods are the `unittest` family; PyTest uses the plain Python `assert` statement.
</details>

---

### 2. Which command creates a virtual environment in a folder named `.venv`?
- [ ] A) `python -m pip install venv .venv`
- [ ] B) `python -m venv .venv`
- [ ] C) `python .venv create`
- [ ] D) `source .venv/bin/activate`

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** B) `python -m venv .venv`

**Explanation:** `-m venv` runs the standard-library `venv` module and `.venv` is the folder name to create.

- **Why others are wrong:**
  - A) `venv` is a standard-library module that is run with `-m`; it is not installed with pip like PyTest.
  - C) This would try to run a script called `.venv`; it is not how the `venv` module is invoked.
  - D) This *activates* an existing environment on macOS/Linux; it does not create one.
</details>

---

### 3. What is the difference between `pytest` and `python -m pytest`?
- [ ] A) `python -m pytest` also adds the current working directory to `sys.path`
- [ ] B) `python -m pytest` installs PyTest first, then runs it
- [ ] C) `pytest` ignores `pytest.ini` while `python -m pytest` reads it
- [ ] D) `python -m pytest` runs tests in parallel

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** A) `python -m pytest` also adds the current working directory to `sys.path`

**Explanation:** Adding the current folder to `sys.path` helps tests import your own project code, and it also guarantees the PyTest of that exact `python` is used.

- **Why others are wrong:**
  - B) Neither command installs anything; installation is done with `pip install`.
  - C) Both read the same configuration file.
  - D) The lesson does not describe any parallel behaviour; the difference is only the `sys.path` handling.
</details>

---

### 4. A project contains both a `pytest.ini` and a `pyproject.toml` that has a `[tool.pytest.ini_options]` table. Which file does PyTest use?
- [ ] A) `pyproject.toml`, because it is the modern standard
- [ ] B) Both are merged, and `pyproject.toml` values override `pytest.ini`
- [ ] C) `pytest.ini`, because it always wins if present, even if empty
- [ ] D) Whichever file was edited most recently

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** C) `pytest.ini`, because it always wins if present, even if empty

**Explanation:** The priority order is `pytest.ini`, then `pyproject.toml`, then `tox.ini`, then `setup.cfg`.

- **Why others are wrong:**
  - A) It is second in priority and only used when no `pytest.ini` exists.
  - B) PyTest picks a single config file; it does not merge them.
  - D) Modification time is irrelevant; a fixed priority order decides.
</details>

---

### 5. What does `pythonpath = .` in `pytest.ini` do?
- [ ] A) Tells PyTest to search only the current folder for tests
- [ ] B) Adds the project root to `sys.path`, so `from src.utils import ...` works with plain `pytest`
- [ ] C) Installs the project into the virtual environment
- [ ] D) Sets the folder where `.venv` is created

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** B) Adds the project root to `sys.path`, so `from src.utils import ...` works with plain `pytest`

**Explanation:** It is a built-in option since PyTest 7 that makes your own code importable from tests.

- **Why others are wrong:**
  - A) Choosing where tests live is the job of `testpaths`, not `pythonpath`.
  - C) It only changes the import search path; nothing is installed.
  - D) Virtual environments are created with `python -m venv`; `pythonpath` is unrelated.
</details>

---

### 6. With default settings, which of these file names is collected as a test file?
- [ ] A) `tests.py`
- [ ] B) `testlogin.py`
- [ ] C) `login_test.py`
- [ ] D) `check_login.py`

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** C) `login_test.py`

**Explanation:** The default patterns are `test_*.py` or `*_test.py`, and `login_test.py` matches `*_test.py`.

- **Why others are wrong:**
  - A) It has neither a `test_` prefix nor a `_test` suffix on the file name stem.
  - B) The prefix must be `test_` with an underscore for files (the underscore is not needed for function names).
  - D) `check_*.py` is only collected if you add it to `python_files`.
</details>

---

### 7. Why does PyTest skip a test class that defines `__init__` (and print a warning)?
- [ ] A) `__init__` is a reserved name that Python forbids in classes
- [ ] B) Classes with `__init__` must be run with the `-s` option
- [ ] C) Only classes ending in `Tests` may define `__init__`
- [ ] D) PyTest creates a fresh instance of the class for every test method, so it does not support constructors

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** D) PyTest creates a fresh instance of the class for every test method, so it does not support constructors

**Explanation:** The lesson recommends setup features (covered on Tuesday) instead of `__init__`.

- **Why others are wrong:**
  - A) `__init__` is an ordinary Python constructor; the limitation is specific to PyTest test classes.
  - B) No such option exists for this; the class is simply not collected.
  - C) Class naming has nothing to do with it; the rule is that a `Test*` class must have no `__init__`.
</details>

---

### 8. What is the difference between `--ignore` and `--deselect`?
- [ ] A) `--ignore` prevents even importing the path; `--deselect` collects the test but removes it from the run
- [ ] B) `--ignore` deletes the files from disk; `--deselect` only hides them
- [ ] C) They are aliases for the same option
- [ ] D) `--ignore` works on markers; `--deselect` works on folders

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** A) `--ignore` prevents even importing the path; `--deselect` collects the test but removes it from the run

**Explanation:** `--ignore=tests/legacy` skips the folder or file entirely, while `--deselect` takes a specific node ID out after collection.

- **Why others are wrong:**
  - B) Neither option touches files on disk.
  - C) They behave differently: one acts before import, the other after collection.
  - D) `--ignore` takes paths and `--deselect` takes node IDs; markers are selected with `-m`.
</details>

---

### 9. `tests/api/test_login.py` and `tests/ui/test_login.py` both exist and no `__init__.py` files exist. PyTest reports `import file mismatch`. What is the recommended scalable fix?
- [ ] A) Add `--ignore=tests/ui` permanently to `addopts`
- [ ] B) Add an `__init__.py` file to the test folders (or rename one file to a unique name)
- [ ] C) Delete the `.pytest_cache` folder only
- [ ] D) Run PyTest with `-s` so the imports are shown

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** B) Add an `__init__.py` file to the test folders (or rename one file to a unique name)

**Explanation:** With `__init__.py` files PyTest imports `tests.api.test_login` and `tests.ui.test_login` as different dotted names, so the clash disappears.

- **Why others are wrong:**
  - A) That hides all UI tests, so they would never run.
  - C) The cache is not the cause; two bare module names `test_login` clash on `sys.path`.
  - D) `-s` only controls output capture; it does not change how modules are imported.
</details>

---

### 10. A team sets `norecursedirs = legacy` in `pytest.ini`. What important side effect does the lesson warn about?
- [ ] A) It replaces PyTest's default list, so any defaults you still want must be listed again
- [ ] B) It also deletes the `legacy` folder
- [ ] C) It adds `legacy` to the default list and keeps the others
- [ ] D) It only takes effect when `--strict-config` is set

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** A) It replaces PyTest's default list, so any defaults you still want must be listed again

**Explanation:** Defaults such as `.*`, `build`, `dist`, `venv` and `node_modules` are no longer applied unless you include them.

- **Why others are wrong:**
  - B) It only stops PyTest from descending into the folder; nothing is deleted.
  - C) The lesson says the setting **replaces** the defaults rather than extending them.
  - D) `--strict-config` just rejects unknown config keys; `norecursedirs` works without it.
</details>

---

### 11. In the Arrange-Act-Assert pattern, which part performs the single action being tested?
- [ ] A) Arrange
- [ ] B) Assert
- [ ] C) Verify
- [ ] D) Act

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** D) Act

**Explanation:** Arrange prepares inputs and objects, Act performs the one action under test, and Assert checks the result.

- **Why others are wrong:**
  - A) Arrange is only for preparing inputs, objects and test data (the manual-test precondition).
  - B) Assert checks the outcome after the action has happened.
  - C) There is no 'Verify' stage in AAA; the three parts are Arrange, Act, Assert.
</details>

---

### 12. Which test name best follows the lesson's naming pattern `test_<thing>_<condition>_<expected result>`?
- [ ] A) `test1`
- [ ] B) `test_works`
- [ ] C) `test_reverse_text_with_empty_string_returns_empty_string`
- [ ] D) `test_stuff`

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** C) `test_reverse_text_with_empty_string_returns_empty_string`

**Explanation:** It names the thing (`reverse_text`), the condition (`with_empty_string`) and the expected result (`returns_empty_string`).

- **Why others are wrong:**
  - A) It carries no information in a failure report.
  - B) It names no thing, condition or expected result.
  - D) It is vague; the lesson lists `test_stuff` among the bad names.
</details>

---

### 13. Why does PyTest create a brand new instance of a test class for every test method?
- [ ] A) Because creating instances is faster than reusing one
- [ ] B) Because each method needs its own `__init__` to run
- [ ] C) Because classes in PyTest are always inherited from `unittest.TestCase`
- [ ] D) To keep tests independent, so they cannot pass state to each other through `self`

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** D) To keep tests independent, so they cannot pass state to each other through `self`

**Explanation:** This is deliberate: data set on `self` in one test is not visible in another.

- **Why others are wrong:**
  - A) The reason is independence, not speed.
  - B) Test classes must not have `__init__` at all.
  - C) PyTest test classes are plain classes and do not need a base class.
</details>

---

### 14. Which situation is the best fit for `xfail` rather than `skip`?
- [ ] A) A test for a feature the developers have not started
- [ ] B) A test that should never run on any machine
- [ ] C) A test that fails because of a logged bug, where you want to be told when it starts passing
- [ ] D) A test that is too slow

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** C) A test that fails because of a logged bug, where you want to be told when it starts passing

**Explanation:** `xfail` still runs the test, so an unexpected pass (XPASS, or a failure with `strict=True`) signals the bug may be fixed.

- **Why others are wrong:**
  - A) The lesson treats a test that cannot meaningfully run as a case for `skip`.
  - B) `skip` is for tests that should not run; `xfail` runs the test.
  - D) Slowness is handled with a marker such as `slow`, not `xfail`.
</details>

---

### 15. According to the lesson, when is it reasonable to group tests in a class instead of writing plain functions?
- [ ] A) When there is a clear group, for example all tests for one function with five or more tests
- [ ] B) Whenever you want faster execution
- [ ] C) Always, because PyTest requires tests to be inside classes
- [ ] D) Only when you need to inherit from `unittest.TestCase`

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** A) When there is a clear group, for example all tests for one function with five or more tests

**Explanation:** Classes give organisation, shared marking and namespacing; there is no other technical advantage.

- **Why others are wrong:**
  - B) Classes bring no speed advantage; the lesson says grouping is their only benefit.
  - C) Plain functions are perfectly fine and preferred by many users.
  - D) Test classes in this lesson explicitly do not inherit from `unittest.TestCase`.
</details>

---

### 16. How does PyTest show detailed values such as `where 60 = sum([10, 20, 30])` for a plain `assert`?
- [ ] A) It replaces `assert` with `unittest`'s `assertEqual` at runtime
- [ ] B) It rewrites the `assert` statements in test modules at import time (via an import hook working on the AST)
- [ ] C) It re-runs the failing test with debug logging turned on
- [ ] D) It reads the source file after the failure and guesses the values

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** B) It rewrites the `assert` statements in test modules at import time (via an import hook working on the AST)

**Explanation:** The rewritten assertion stores intermediate values and builds a descriptive message only if the check fails.

- **Why others are wrong:**
  - A) PyTest keeps plain `assert`; the rewriting is internal and invisible.
  - C) No re-run takes place; the details are captured during the first run.
  - D) The values are saved in temporary variables by the rewritten code, not guessed.
</details>

---

### 17. What is wrong with `assert(total == 5, "total should be 5")`?
- [ ] A) `assert` cannot take a message
- [ ] B) `assert` must be called with exactly one argument
- [ ] C) It asserts a non-empty tuple, which is always truthy, so the assertion can never fail
- [ ] D) The message must be an f-string

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** C) It asserts a non-empty tuple, which is always truthy, so the assertion can never fail

**Explanation:** Write `assert total == 5, "total should be 5"` with no parentheses around the condition and message together.

- **Why others are wrong:**
  - A) A message after a comma is allowed: `assert <condition>, <message>`.
  - B) `assert` is a statement, not a function, which is why the parentheses create a tuple.
  - D) The message can be any expression; the problem is the tuple.
</details>

---

### 18. How should you check that a variable `x` equals the number 5 in an assertion?
- [ ] A) `assert x == 5`; reserve `is` for `None`, `True` and `False`
- [ ] B) Use `is`, because it is stricter than `==`
- [ ] C) Use `is` for strings and `==` for numbers
- [ ] D) Use `in`, because it works for every type

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** A) `assert x == 5`; reserve `is` for `None`, `True` and `False`

**Explanation:** `is` checks identity, not value, and `x is 5` may work by accident in one Python build and fail in another.

- **Why others are wrong:**
  - B) Stricter does not mean better here; identity of numbers is not guaranteed.
  - C) `is` should not be used for strings either.
  - D) `in` is a membership check, not a value comparison.
</details>

---

### 19. What is `match` in `pytest.raises(ValueError, match="must be positive")`?
- [ ] A) An exact string that must equal the whole exception message
- [ ] B) A regular expression searched (with `re.search`) in the string form of the exception
- [ ] C) The exception class that is expected
- [ ] D) A custom failure message printed if nothing is raised

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** B) A regular expression searched (with `re.search`) in the string form of the exception

**Explanation:** Because it is a regex, special characters such as parentheses must be escaped (raw string or `re.escape`).

- **Why others are wrong:**
  - A) `match` uses `re.search`, so a partial pattern can match.
  - C) The class is the first argument; `match` checks the message.
  - D) `match` does not set a failure message; `DID NOT RAISE` is the built-in failure.
</details>

---

### 20. Where should you read `excinfo` after `with pytest.raises(KeyError) as excinfo:`?
- [ ] A) Inside the `with` block, on the line after the failing call
- [ ] B) In a separate test function
- [ ] C) It can be read anywhere, including before the `with` statement
- [ ] D) After the `with` block has ended

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** D) After the `with` block has ended

**Explanation:** `excinfo` is not populated until the block exits, so check `excinfo.type` and `excinfo.value` after the block.

- **Why others are wrong:**
  - A) Code after the raising line inside the block never runs, and `excinfo` is not populated there.
  - B) It is a local variable of the test that holds it.
  - C) It exists only after the block completes.
</details>

---

### 21. What is the difference between `skip` and `xfail`, in one sentence?
- [ ] A) `skip` runs the test but ignores the result; `xfail` never runs it
- [ ] B) They are identical; `xfail` is just the older name
- [ ] C) `skip` is for tests that cannot or should not run; `xfail` runs the test, which is known to fail, so you notice when it starts passing
- [ ] D) `xfail` is for slow tests and `skip` is for fast tests

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** C) `skip` is for tests that cannot or should not run; `xfail` runs the test, which is known to fail, so you notice when it starts passing

**Explanation:** This is the lesson's one-sentence rule, and it is why known bugs belong under `xfail`.

- **Why others are wrong:**
  - A) It is the other way round: `skip` never runs and `xfail` does run.
  - B) They have different behaviour and different report symbols (`s` versus `x`).
  - D) Neither marker has anything to do with speed.
</details>

---

### 22. Which module-level variable name applies a marker to every test in a file?
- [ ] A) `pytest_mark`
- [ ] B) `markers`
- [ ] C) `pytest.mark`
- [ ] D) `pytestmark`

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** D) `pytestmark`

**Explanation:** For example `pytestmark = pytest.mark.regression`, or a list of several markers.

- **Why others are wrong:**
  - A) The lesson lists this misspelling as a mistake; the marker is silently not applied.
  - B) `markers` is the ini option that registers markers, not a module variable.
  - C) `pytest.mark` is the decorator namespace, not a module-level variable name.
</details>

---

### 23. What does `@pytest.mark.xfail(strict=True)` change when the test unexpectedly passes?
- [ ] A) The unexpected pass (`XPASS(strict)`) fails the suite, forcing you to remove the marker
- [ ] B) Nothing; the test is reported as XPASS and the build stays green
- [ ] C) The test is skipped the next time
- [ ] D) PyTest deletes the marker automatically

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** A) The unexpected pass (`XPASS(strict)`) fails the suite, forcing you to remove the marker

**Explanation:** Without `strict=True`, an XPASS does not fail the build.

- **Why others are wrong:**
  - B) That is the non-strict behaviour; strict mode turns XPASS into a failure.
  - C) Strict mode does not skip anything.
  - D) PyTest never edits your files; you remove the marker yourself.
</details>

---

### 24. Why does the lesson say you should register custom markers and use `--strict-markers`?
- [ ] A) Because unregistered markers make tests run slower
- [ ] B) Because a typo such as `@pytest.mark.smok` would otherwise quietly create a new marker and the test would never be selected by `-m smoke`
- [ ] C) Because PyTest refuses to run any test that has a custom marker
- [ ] D) Because `-m` can only select built-in markers

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** B) Because a typo such as `@pytest.mark.smok` would otherwise quietly create a new marker and the test would never be selected by `-m smoke`

**Explanation:** Registering also documents each marker's meaning for the team.

- **Why others are wrong:**
  - A) Speed is not mentioned; the risk is silent mis-selection.
  - C) Unregistered markers run with a warning (`PytestUnknownMarkWarning`) unless strict mode is on.
  - D) `-m` selects custom markers by name; registration is for documentation and typo protection.
</details>

---

### 25. Which command selects tests that are marked `regression` but not marked `slow`?
- [ ] A) `python -m pytest -m regression -m not slow`
- [ ] B) `python -m pytest -m "regression and not slow"`
- [ ] C) `python -m pytest -k regression and not slow`
- [ ] D) `python -m pytest --markers regression`

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** B) `python -m pytest -m "regression and not slow"`

**Explanation:** `-m` accepts `and`, `or`, `not` and parentheses, and the expression should be quoted.

- **Why others are wrong:**
  - A) A single quoted expression is needed; the shell would split the words.
  - C) Unquoted, the shell splits the words, and `-m` is the explicit, exact way to select by marker; `-k` matches names.
  - D) `--markers` only lists registered markers; it does not select tests.
</details>

---

### 26. What is the key difference between `-k` and `-m`?
- [ ] A) `-k` selects markers and `-m` selects names
- [ ] B) `-k` needs registered markers; `-m` needs no setup
- [ ] C) Both match only exact, case-sensitive names
- [ ] D) `-k` matches names (file, class, function) as case-insensitive substrings; `-m` matches marker names exactly

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** D) `-k` matches names (file, class, function) as case-insensitive substrings; `-m` matches marker names exactly

**Explanation:** Use `-m` for stable categories such as smoke and regression, and `-k` for quick ad-hoc runs.

- **Why others are wrong:**
  - A) It is the other way round.
  - B) The setup requirement belongs to `-m` (registered markers), not `-k`.
  - C) `-k` is substring-based and case-insensitive.
</details>

---

### 27. A run ends with `no tests ran` because a `-k` expression matched nothing. What exit code does PyTest return?
- [ ] A) 0
- [ ] B) 1
- [ ] C) 5
- [ ] D) 4

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** C) 5

**Explanation:** Exit code 5 means no tests were collected, which helps CI notice a typo in a filter.

- **Why others are wrong:**
  - A) 0 means all tests passed; a filter that matches nothing is not reported as green.
  - B) 1 means some tests failed.
  - D) 4 is a command-line usage error such as a bad option.
</details>

---

### 28. Your passing test contains `print("calculating...")` but you see no output. Which option shows prints live?
- [ ] A) `-s` (shorthand for `--capture=no`)
- [ ] B) `-q`
- [ ] C) `--tb=long`
- [ ] D) `-x`

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** A) `-s` (shorthand for `--capture=no`)

**Explanation:** By default PyTest captures output and shows it only when a test fails.

- **Why others are wrong:**
  - B) `-q` makes the output quieter, not more detailed.
  - C) `--tb` changes the traceback style for failures; it does not affect captured prints of passing tests.
  - D) `-x` stops after the first failure; it does not change capture.
</details>

---

### 29. What does `python -m pytest --lf` do?
- [ ] A) Runs all tests but puts the failed ones first
- [ ] B) Stops at the first failure and resumes there next time
- [ ] C) Lists the tests without running them
- [ ] D) Runs only the tests that failed in the previous run

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** D) Runs only the tests that failed in the previous run

**Explanation:** PyTest remembers results in `.pytest_cache`; if nothing failed last time, `--lf` runs everything by default.

- **Why others are wrong:**
  - A) That is `--ff` (`--failed-first`).
  - B) That is `--sw` (`--stepwise`).
  - C) That is `--collect-only`.
</details>

---

### 30. Why can `-k add` select more tests than you expected?
- [ ] A) Matching is by substring, so names such as `test_address` also contain `add`
- [ ] B) Because `-k` also runs all deselected tests at the end
- [ ] C) Because `-k` ignores the `not` operator
- [ ] D) Because `-k` matches only file names

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** A) Matching is by substring, so names such as `test_address` also contain `add`

**Explanation:** Be more specific (for example `-k "test_add_"`) or use markers when you need exact categories.

- **Why others are wrong:**
  - B) Deselected tests stay deselected.
  - C) `-k` supports `and`, `or`, `not` and parentheses.
  - D) It matches file, class and function name parts.
</details>

---

## Part 2: True or False (Misconceptions)

### 31. A `pytest.ini` file that starts with the header `[tool:pytest]` is read correctly by PyTest.
- [ ] A) True
- [ ] B) False

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** B) False

**Explanation:** In `pytest.ini` the header must be exactly `[pytest]`; `[tool:pytest]` is only for `setup.cfg`, and a wrong header means the settings are silently ignored.
</details>

---

### 32. `pip freeze > requirements.txt` captures every installed package with exact versions, which is precise but can be noisy.
- [ ] A) True
- [ ] B) False

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** A) True

**Explanation:** The lesson notes this precision versus noise trade-off and says a short hand-written list is easier to maintain for learning projects.
</details>

---

### 33. A test function named `testadd` (no underscore after `test`) is collected by default.
- [ ] A) True
- [ ] B) False

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** A) True

**Explanation:** For functions the default rule is simply that the name starts with `test`, so no underscore is required. (Files do need `test_` or `_test`.)
</details>

---

### 34. A class named `LoginTests` that contains methods named `test_valid_user` is collected, because its methods start with `test`.
- [ ] A) True
- [ ] B) False

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** B) False

**Explanation:** The class name must start with `Test` (capital T). `LoginTests` does not, so its methods are never discovered.
</details>

---

### 35. A PyTest test passes when the function finishes without raising an exception.
- [ ] A) True
- [ ] B) False

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** A) True

**Explanation:** Passing is defined by the absence of an escaping exception; a failed `assert` raises `AssertionError`, which makes the test fail.
</details>

---

### 36. Test classes in PyTest must inherit from `unittest.TestCase` to be collected.
- [ ] A) True
- [ ] B) False

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** B) False

**Explanation:** They are plain Python classes named `Test...` with no `__init__`; inheriting from `unittest.TestCase` is a different style that PyTest can also run.
</details>

---

### 37. `isinstance(True, int)` is `True`, because `bool` is a subclass of `int`.
- [ ] A) True
- [ ] B) False

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** A) True

**Explanation:** That surprises many beginners; `type(result) is int` is the stricter check that excludes subclasses such as `bool`.
</details>

---

### 38. PyTest's assertion rewriting automatically applies to every helper module your tests import.
- [ ] A) True
- [ ] B) False

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** B) False

**Explanation:** Rewriting applies to test modules, `conftest.py` files and plugins; helper modules need `pytest.register_assert_rewrite("helper_module")`.
</details>

---

### 39. Adding `@pytest.mark.smoke` to a test makes it run faster or earlier than unmarked tests.
- [ ] A) True
- [ ] B) False

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** B) False

**Explanation:** A custom marker is only a label that helps you select tests with `-m`; it changes neither speed nor order.
</details>

---

### 40. A marker placed on a test class applies to every test method inside that class.
- [ ] A) True
- [ ] B) False

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** A) True

**Explanation:** For example `@pytest.mark.regression` above `class TestDivide:` gives both methods the `regression` marker.
</details>

---

### 41. When you use both `-m smoke` and `-k divide`, a test must satisfy both filters to run.
- [ ] A) True
- [ ] B) False

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** A) True

**Explanation:** The filters combine as AND; in the lesson's suite only `TestDivide::test_divide_evenly` is both smoke and has `divide` in its name.
</details>

---

### 42. If no test failed in the previous run, `python -m pytest --lf` runs no tests at all.
- [ ] A) True
- [ ] B) False

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** B) False

**Explanation:** By default `--lf` then runs everything; use `--lfnf=none` if you want it to run nothing.
</details>

---

## Part 3: Code Prediction

### 43. A project has this `pytest.ini` and one test file `test_a.py`. The marker `smoke` is registered, but the test uses a misspelled marker.

```ini
[pytest]
addopts = --strict-markers
markers =
    smoke: quick sanity checks
```

```python
import pytest

@pytest.mark.smoek
def test_add_zero():
    assert 5 + 0 == 5
```

What happens when you run `python -m pytest`?
- [ ] A) `1 passed`, because the assertion is true
- [ ] B) Collection stops with an error saying `'smoek' not found in markers configuration option`; no test runs
- [ ] C) `1 passed, 1 warning`
- [ ] D) `1 skipped`, because the marker is unknown

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** B) Collection stops with an error saying `'smoek' not found in markers configuration option`; no test runs

**Explanation:** `--strict-markers` turns an unregistered marker into an error. (Verified by running: `1 error during collection`, exit code 2.)

- **Why others are wrong:**
  - A) Without `--strict-markers` it would run (with a warning), but strict mode makes the typo an error before any test runs.
  - C) A warning is what you get *without* `--strict-markers`; with it the typo is an error.
  - D) An unknown marker does not skip a test; it either warns or (in strict mode) errors.
</details>

---

### 44. Project layout and config:

```text
project/
├── pytest.ini          # [pytest]  testpaths = tests
├── test_root.py        # contains one passing test
└── tests/
    └── test_inside.py  # contains one passing test
```

You run `python -m pytest` with no arguments from `project/`. What is the summary?
- [ ] A) `2 passed`
- [ ] B) `1 passed` from `test_root.py` only
- [ ] C) `1 passed`
- [ ] D) `no tests ran`

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** C) `1 passed`

**Explanation:** With no arguments PyTest uses `testpaths = tests`, so only `tests/test_inside.py` is collected. (Verified by running.)

- **Why others are wrong:**
  - A) `test_root.py` lies outside `testpaths`, so it is not collected when no arguments are given.
  - B) The reverse is true: `testpaths` limits the search to the `tests` folder.
  - D) The `tests` folder holds a valid test file, so one test is collected and passes.
</details>

---

### 45. This file is `test_naming_demo.py`. How many tests does `python -m pytest --collect-only -q` collect?

```python
def test_collected_function():
    assert True

def testcollected_without_underscore():
    assert True

def check_not_collected():
    assert True

class TestCollectedClass:
    def test_method_is_collected(self):
        assert True
    def helper_not_collected(self):
        return 42

class NotATestClass:
    def test_ignored_because_class_name(self):
        assert True

class TestWithInit:
    def __init__(self):
        self.value = 1
    def test_skipped_class(self):
        assert True
```
- [ ] A) 3
- [ ] B) 2
- [ ] C) 5
- [ ] D) 7

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** A) 3

**Explanation:** Collected: `test_collected_function`, `testcollected_without_underscore`, `TestCollectedClass::test_method_is_collected`. (Verified by running: `3 tests collected`.)

- **Why others are wrong:**
  - B) Both module-level functions starting with `test` count, plus the method of `TestCollectedClass`; that makes 3, not 2.
  - C) `NotATestClass` and `TestWithInit` are not collected, and neither are `check_not_collected` or `helper_not_collected`.
  - D) 7 is the number of `def` lines; only those matching the naming rules and class rules are collected.
</details>

---

### 46. This file contains a class with a constructor and one ordinary test function:

```python
class TestWithInit:
    def __init__(self):
        self.value = 1

    def test_a(self):
        assert True


def test_ok():
    assert True
```

What is the final summary line of `python -m pytest`?
- [ ] A) `2 passed`
- [ ] B) `1 passed, 1 failed`
- [ ] C) `1 error`
- [ ] D) `1 passed, 1 warning`

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** D) `1 passed, 1 warning`

**Explanation:** `test_ok` is collected and passes; the class with `__init__` is not collected and PyTest emits a `PytestCollectionWarning`. (Verified by running.)

- **Why others are wrong:**
  - A) `TestWithInit::test_a` is not collected because the class defines `__init__`.
  - B) The skipped class does not cause a failure; it only produces a warning.
  - C) A class with `__init__` is not a collection error; PyTest warns and continues.
</details>

---

### 47. What is the result of running this file with `python -m pytest`?

```python
class TestInstanceIsolation:
    def test_a_sets_attribute(self):
        self.token = "abc"
        assert self.token == "abc"

    def test_b_does_not_see_it(self):
        assert not hasattr(self, "token")
```
- [ ] A) `1 passed, 1 failed`
- [ ] B) `2 passed`
- [ ] C) `1 passed, 1 error`
- [ ] D) `2 failed`

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** B) `2 passed`

**Explanation:** Each method runs on a new instance, so `token` set in the first test does not exist in the second, which is exactly what the second test asserts. (Verified by running.)

- **Why others are wrong:**
  - A) The second test passes because `hasattr(self, 'token')` is `False` on a fresh instance.
  - C) No exception occurs outside the test body, so there is no error.
  - D) Both assertions are true, so neither test fails.
</details>

---

### 48. What is the result of running this test?

```python
import pytest

def test_wrong_exception():
    with pytest.raises(ValueError):
        1 / 0
```
- [ ] A) `1 passed`, because an exception was raised
- [ ] B) `1 xfailed`
- [ ] C) `1 skipped`
- [ ] D) `1 failed` (a `ZeroDivisionError` escapes)

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** D) `1 failed` (a `ZeroDivisionError` escapes)

**Explanation:** `pytest.raises` passes only when the expected type is raised; a different exception type makes the test fail. (Verified by running.)

- **Why others are wrong:**
  - A) The raised exception must be the expected type (`ValueError`), not just any exception.
  - B) Nothing marks this test as an expected failure.
  - C) Nothing skips the test; it runs and fails.
</details>

---

### 49. What does `python -m pytest` report for this file?

```python
def test_trap():
    total = 2 + 2
    assert (total == 5, "total should be 5")
```
- [ ] A) `1 failed`, because `2 + 2` is not 5
- [ ] B) `1 error`, because of a syntax error
- [ ] C) `1 passed` (with a warning that the assertion is always true)
- [ ] D) `1 skipped`

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** C) `1 passed` (with a warning that the assertion is always true)

**Explanation:** The parentheses create a two-item tuple, which is truthy, so the assert cannot fail. (Verified by running: `1 passed, 1 warning`.)

- **Why others are wrong:**
  - A) The asserted expression is a tuple, not the comparison, so the comparison is never evaluated as a condition.
  - B) The code is valid Python; it only triggers a `PytestAssertRewriteWarning`.
  - D) Nothing skips the test.
</details>

---

### 50. What is the summary after running this file?

```python
import pytest

def test_plain_float():
    assert 0.1 + 0.2 == 0.3

def test_approx_float():
    assert 0.1 + 0.2 == pytest.approx(0.3)
```
- [ ] A) `1 failed, 1 passed`
- [ ] B) `2 passed`
- [ ] C) `2 failed`
- [ ] D) `1 passed, 1 error`

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** A) `1 failed, 1 passed`

**Explanation:** `0.1 + 0.2` is `0.30000000000000004`, so plain `==` fails, while `pytest.approx` allows a small tolerance. (Verified by running.)

- **Why others are wrong:**
  - B) Plain `==` on these floats is `False`.
  - C) `pytest.approx(0.3)` accepts values within the default tolerance, so the second test passes.
  - D) A failed comparison is a `failed` result, not an `error` (errors occur outside the test body).
</details>

---

### 51. All markers below are registered in `pytest.ini`. What is the summary after `python -m pytest -m "regression and not slow"`?

```python
@pytest.mark.regression
def test_a(): assert True

@pytest.mark.regression
@pytest.mark.slow
def test_b(): assert True

@pytest.mark.smoke
def test_c(): assert True

@pytest.mark.slow
def test_d(): assert True
```
- [ ] A) `2 passed, 2 deselected`
- [ ] B) `3 passed, 1 deselected`
- [ ] C) `4 passed`
- [ ] D) `1 passed, 3 deselected`

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** D) `1 passed, 3 deselected`

**Explanation:** Only `test_a` is regression and not slow; the other three are deselected. (Verified by running; the lesson's Exercise 2 gives the same answer.)

- **Why others are wrong:**
  - A) `test_b` also carries `slow`, so `not slow` excludes it.
  - B) `test_c` is not regression and `test_d` is not regression, so they cannot be selected.
  - C) Without a marker expression everything runs; with `-m`, non-matching tests are deselected.
</details>

---

### 52. What happens when you run this file with `python -m pytest`?

```python
import pytest

@pytest.mark.xfail(strict=True, reason="BUG-1")
def test_fixed_already():
    assert 1 + 1 == 2
```
- [ ] A) `1 failed` (reported as `XPASS(strict)`)
- [ ] B) `1 xfailed`
- [ ] C) `1 passed`
- [ ] D) `1 skipped`

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** A) `1 failed` (reported as `XPASS(strict)`)

**Explanation:** The test passes unexpectedly and strict mode turns that into a failure. (Verified by running.)

- **Why others are wrong:**
  - B) XFAIL means the test failed as expected; this test passes.
  - C) With `strict=True` an unexpected pass is not reported as a normal pass.
  - D) `xfail` runs the test; it does not skip it.
</details>

---

### 53. A suite has four tests: `test_add_positive` (smoke), `test_add_negative` (regression), `TestDivide::test_divide_evenly` (smoke) and `TestDivide::test_divide_by_zero_raises` (regression), all passing. What is the summary of `python -m pytest -k "TestDivide and not zero"`?
- [ ] A) `2 passed, 2 deselected`
- [ ] B) `1 passed, 3 deselected`
- [ ] C) `3 passed, 1 deselected`
- [ ] D) `4 passed`

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** B) `1 passed, 3 deselected`

**Explanation:** `TestDivide` matches the class name and `not zero` removes the method with `zero` in its name, so only `test_divide_evenly` runs. (Verified by running.)

- **Why others are wrong:**
  - A) `test_divide_by_zero_raises` contains `zero`, so `not zero` excludes it.
  - C) Only tests that match `TestDivide` and do not contain `zero` are selected; the two add tests are not in `TestDivide`.
  - D) A `-k` expression filters tests; deselected tests are not run.
</details>

---

### 54. You run the following on Linux and then check the exit code:

```bash
python -m pytest -k "nothing_matches_this"; echo $?
```

What number is printed after the PyTest output?
- [ ] A) 0
- [ ] B) 1
- [ ] C) 5
- [ ] D) 2

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** C) 5

**Explanation:** No tests were selected, which is exit code 5 (`no tests ran`). (Verified by running.)

- **Why others are wrong:**
  - A) Skipped or xfailed results keep exit code 0, but here nothing ran at all.
  - B) 1 would mean at least one test failed.
  - D) 2 means the run was interrupted by the user.
</details>

---

## Part 4: Fill in the Blank

### 55. To print the installed PyTest version, run `pytest ________`.
- [ ] Your answer: `__________`

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** `--version`

**Explanation:** `pytest --version` prints something like `pytest 8.3.4`; `python -m pip show pytest` is the other way.
</details>

---

### 56. Inside `pytest.ini`, the option `________ = tests` tells PyTest to look only in the `tests` folder when you run `pytest` with no arguments.
- [ ] Your answer: `__________`

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** `testpaths`

**Explanation:** `testpaths` defines the default search location, and it also makes collection faster.
</details>

---

### 57. To change which class names PyTest treats as test classes, set the ini option `________`.
- [ ] Your answer: `__________`

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** `python_classes`

**Explanation:** `python_files`, `python_classes` and `python_functions` customise the naming rules, though the lesson advises keeping the standard names.
</details>

---

### 58. The command `python -m pytest ________` lists the tests PyTest found without running any of them.
- [ ] Your answer: `__________`

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** `--collect-only`

**Explanation:** `--collect-only` (alias `--co`) is a free dry run; use `-q` to print just the node IDs.
</details>

---

### 59. In the F.I.R.S.T. qualities of a good test, the letter I stands for ________: a test does not rely on another test's result or order.
- [ ] Your answer: `__________`

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** Independent

**Explanation:** Independent tests can run alone or in any order; the other letters are Fast, Repeatable, Self-validating and Timely.
</details>

---

### 60. The three parts of a well-structured test are Arrange, Act and ________.
- [ ] Your answer: `__________`

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** Assert

**Explanation:** Arrange prepares, Act performs the action, and Assert checks the result.
</details>

---

### 61. To check that a variable is `None`, write `assert value ____ None`.
- [ ] Your answer: `__________`

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** `is`

**Explanation:** `is` is the right choice for singletons `None`, `True` and `False`; use `==` for values.
</details>

---

### 62. To verify that a deprecation warning is issued, use `with pytest.________(DeprecationWarning):`.
- [ ] Your answer: `__________`

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** `warns`

**Explanation:** `pytest.warns` is the warning counterpart of `pytest.raises`.
</details>

---

### 63. To list all built-in and registered markers with descriptions, run `python -m pytest ________`.
- [ ] Your answer: `__________`

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** `--markers`

**Explanation:** `--markers` is the quick way to see which markers exist and what they mean.
</details>

---

### 64. Setting `________ = true` in `pytest.ini` makes every `xfail` strict by default.
- [ ] Your answer: `__________`

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** `xfail_strict`

**Explanation:** With `xfail_strict = true` an unexpected pass fails the run unless a test overrides it.
</details>

---

### 65. `python -m pytest --________=3` stops the run after three failures.
- [ ] Your answer: `__________`

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** `maxfail`

**Explanation:** `--maxfail=N` stops after N failures; `-x` is the same idea with N equal to 1.
</details>

---

### 66. In `-ra`, the letter `a` asks the short summary to show all outcomes except ________.
- [ ] Your answer: `__________`

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** passed

**Explanation:** `-ra` lists failed, errors, skipped, xfailed and xpassed outcomes; use `-rA` to include passed too.
</details>

---

## Topic Coverage

| Topic | Question numbers | Count |
|---|---|---|
| PyTest installation and configuration | 1, 2, 3, 4, 5, 31, 32, 43, 44, 55, 56 | 11 |
| Test discovery and organization | 6, 7, 8, 9, 10, 33, 34, 45, 46, 57, 58 | 11 |
| Test functions and classes | 11, 12, 13, 14, 15, 35, 36, 47, 48, 59, 60 | 11 |
| Assertions and assertion introspection | 16, 17, 18, 19, 20, 37, 38, 49, 50, 61, 62 | 11 |
| Markers | 21, 22, 23, 24, 25, 39, 40, 51, 52, 63, 64 | 11 |
| Test execution and filtering | 26, 27, 28, 29, 30, 41, 42, 53, 54, 65, 66 | 11 |
| **Total** | 1 to 66 | **66** |
