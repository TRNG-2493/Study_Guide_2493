# Interview Questions: Week 4 - PyTest-Playwright - Monday

Topic: PyTest Fundamentals. Click each answer only after you have tried to answer out loud, as you would in a real interview.

## Beginner (Foundational)

### Q1: What is PyTest, and how does it differ from Python's built-in `unittest`?
**Keywords:** Testing framework, Plain `assert`, Functions, Plugins, `TestCase`
**Hint:** Think about what a test looks like in each one.

<details>
<summary>Click to Reveal Answer</summary>

PyTest is an open-source Python testing framework that finds your tests, runs them, and reports which passed or failed and why. With `unittest` a test is a method inside a class that inherits from `unittest.TestCase`, and you use special methods such as `assertEqual`. With PyTest a test is a plain function and you use the plain Python `assert` statement, so there is much less boilerplate. PyTest also gives richer failure messages, has hundreds of plugins (HTML reports, Playwright, coverage), and can still run existing `unittest` tests.

```python
def test_add():
    assert 2 + 3 == 5
```
</details>

---

### Q2: Why do we create a virtual environment for a test project, and how do you create and activate one?
**Keywords:** Isolation, Dependencies, `python -m venv .venv`, Activate, `.gitignore`
**Hint:** Imagine one project needs PyTest 7 and another needs PyTest 8.

<details>
<summary>Click to Reveal Answer</summary>

A virtual environment is a private, isolated folder with its own installed packages, so projects with different dependency versions do not break each other and the global Python stays clean. You create it with `python -m venv .venv` and activate it with `source .venv/bin/activate` on macOS/Linux or `.venv\Scripts\activate.bat` (Command Prompt) or `.venv\Scripts\Activate.ps1` (PowerShell) on Windows. The prompt then starts with `(.venv)`. You never commit the `.venv` folder; it goes into `.gitignore`, and teammates rebuild it from `requirements.txt`.
</details>

---

### Q3: What is the difference between running `pytest` and `python -m pytest`?
**Keywords:** `sys.path`, Current working directory, Import, Interpreter, `ModuleNotFoundError`

<details>
<summary>Click to Reveal Answer</summary>

They are almost identical, but `python -m pytest` also adds the current working directory to `sys.path`, the list of folders Python searches on `import`. That matters when tests import your own project code, for example `from src.utils import add`. If plain `pytest` gives `ModuleNotFoundError` for your own code, either use `python -m pytest` or set `pythonpath = .` in the config. A second benefit is that `python -m pytest` guarantees you use the PyTest installed for that exact `python`, which avoids wrong-interpreter confusion.
</details>

---

### Q4: What do `testpaths`, `addopts`, `minversion`, and `pythonpath` do in a `pytest.ini` file?
**Keywords:** `testpaths`, `addopts`, `minversion`, `pythonpath`, `[pytest]`

<details>
<summary>Click to Reveal Answer</summary>

`testpaths` tells PyTest where to look when you run it with no arguments, which also speeds up collection. `addopts` inserts default command-line options into every run, such as `-ra --strict-markers`, so nobody has to retype them. `minversion` stops the run with a clear error if the installed PyTest is older than the stated version. `pythonpath` adds folders such as the project root to `sys.path` so imports like `from src.utils import ...` work. In `pytest.ini` the section header must be exactly `[pytest]`.

```ini
[pytest]
minversion = 8.0
testpaths = tests
pythonpath = .
addopts = -ra
```
</details>

---

### Q5: How does PyTest decide which configuration file to use, and what are `rootdir` and `inifile`?
**Keywords:** `pytest.ini`, Priority, Walks upward, `rootdir`, `configfile`
**Hint:** Look at the header lines PyTest prints at the start of a run.

<details>
<summary>Click to Reveal Answer</summary>

The `inifile` is the configuration file PyTest uses, and the `rootdir` is the base folder used for things like the cache directory and test IDs. PyTest starts from the arguments (or the current directory) and walks upward through parent folders looking for a config file. The priority is `pytest.ini` first (it always wins if present, even if empty), then `pyproject.toml` with a `[tool.pytest.ini_options]` table, then `tox.ini` with `[pytest]`, then `setup.cfg` with `[tool:pytest]`. The folder where the first match is found becomes the rootdir. If the output has no `configfile:` line, no config is being used, so always run from the project root.
</details>

---

### Q6: What are PyTest's default naming rules for test files, functions, classes, and methods?
**Keywords:** `test_*.py`, `*_test.py`, Prefix `test`, Prefix `Test`, No `__init__`

<details>
<summary>Click to Reveal Answer</summary>

A test file must match `test_*.py` or `*_test.py`. Test functions and test methods must have names starting with `test`. Test classes must start with `Test` (capital T) and must not define an `__init__` method. So `login_tests.py`, `tests.py`, `check_add()` and a class called `LoginTests` are all not collected, while `test_login.py`, `test_add()` and `TestLogin` are. You can change the rules with `python_files`, `python_classes` and `python_functions`, but the standard names are what every PyTest developer expects.
</details>

---

### Q7: What is test collection, and what does `--collect-only` tell you?
**Keywords:** Collection, Import modules, Node ID, `--collect-only`, Before running

<details>
<summary>Click to Reveal Answer</summary>

Collection is the discovery phase that happens before any test runs. PyTest decides where to look, walks the folders, picks test files by name pattern, imports each as a module, picks test items inside, and builds a list of items each with a unique node ID such as `tests/test_utils.py::TestMath::test_add`. If a file has a syntax or import error, you get a collection error and none of its tests run. `python -m pytest --collect-only -q` prints what was found without running anything, so it is the first thing I check when a test seems to be missing.
</details>

---

### Q8: Explain the difference between `--ignore` and `--deselect`.
**Keywords:** `--ignore`, `--deselect`, Import, Collected, Node ID

<details>
<summary>Click to Reveal Answer</summary>

`--ignore` stops PyTest from looking at a file or folder at all, so it is not even imported. `--deselect` still collects the test but removes it from the run, and it takes a node ID. A deselected test shows up in the summary as `deselected`. I use `--ignore` for things like a legacy folder that cannot even be imported, and `--deselect` to drop one specific slow or broken test for a single run. A permanent folder exclusion can be set with `norecursedirs` in the config, remembering that it replaces PyTest's defaults.

```bash
python -m pytest --ignore=tests/legacy
python -m pytest --deselect tests/test_utils.py::test_slow_one
```
</details>

---

### Q9: When does a PyTest test pass, fail, or error? What does Arrange-Act-Assert mean?
**Keywords:** No exception, `AssertionError`, Error, Arrange, Act, Assert

<details>
<summary>Click to Reveal Answer</summary>

A test passes if the function finishes without any exception escaping, and fails if an `assert` is false (an `AssertionError`) or another exception escapes the test body. An error means something went wrong outside the test body, such as during setup or collection. Arrange-Act-Assert is the shape of a good test: arrange the inputs and objects, act by performing the one action under test, and assert on the result. Related good habits are one behaviour per test and descriptive names such as `test_<thing>_<condition>_<expected>`.
</details>

---

### Q10: How does PyTest instantiate a test class, and why does that matter?
**Keywords:** New instance, Each test method, `self`, Independence, No shared state

<details>
<summary>Click to Reveal Answer</summary>

For each test method PyTest creates a brand new instance of the class, calls that one method, and throws the instance away. This is deliberate so tests stay independent. It matters because data stored on `self` in one test is not visible in another, so you must never rely on one test setting something for the next. The same reason explains why a test class cannot have an `__init__`.

```python
class TestInstanceIsolation:
    def test_a(self):
        self.token = "abc"
    def test_b(self):
        assert not hasattr(self, "token")   # passes in any order
```
</details>

---

### Q11: What is assertion introspection in PyTest, and how does it work?
**Keywords:** Assertion rewriting, Import hook, AST, Sub-expressions, `E` lines

<details>
<summary>Click to Reveal Answer</summary>

Assertion introspection is PyTest's feature of showing the values of the sub-expressions when an assert fails. When PyTest imports your test modules, an import hook rewrites the compiled `assert` statements (working on the AST) so intermediate values are saved and a descriptive message can be built on failure. For example `assert sum(prices) == 70` fails with `assert 60 == 70` and `where 60 = sum([10, 20, 30])`. Plain Python would only say `AssertionError`. That is why we can use plain `assert` instead of `assertEqual` methods.
</details>

---

### Q12: What is the difference between `==` and `is` in assertions, and how do you compare floats safely?
**Keywords:** Value equality, Identity, `None`/`True`/`False`, `pytest.approx`, Tolerance

<details>
<summary>Click to Reveal Answer</summary>

`==` checks whether two values are equal, while `is` checks whether they are the exact same object. Use `is` only for the singletons `None`, `True` and `False`, for example `assert value is None`; never use it for numbers or strings. For floats, `0.1 + 0.2 == 0.3` is `False` because of binary floating point, so use `pytest.approx`, which compares within a tolerance (defaults `rel=1e-6`, `abs=1e-12`) and can be tuned with `rel` or `abs`.

```python
assert 0.1 + 0.2 == pytest.approx(0.3)
```
</details>

---

### Q13: What is the difference between the `skip` and `xfail` markers, and when do you use each?
**Keywords:** `skip`, `xfail`, Runs, `XPASS`, `strict=True`

<details>
<summary>Click to Reveal Answer</summary>

`skip` means the test never runs because it cannot or should not run right now; `skipif` skips only when a condition is true. `xfail` means the test is expected to fail because of a known problem, and PyTest still runs it. If it fails it is reported as `XFAIL` and does not break the build; if it unexpectedly passes it is `XPASS`, and with `strict=True` that unexpected pass fails the suite. For a known bug I prefer `xfail(reason="BUG-204", strict=True)` over `skip`, because I find out when the bug gets fixed. Always give a reason.
</details>

---

### Q14: What is the difference between `-k` and `-m` for selecting tests?
**Keywords:** `-k`, `-m`, Name substring, Marker name, Quote the expression

<details>
<summary>Click to Reveal Answer</summary>

`-k` matches an expression against test names (file, class, function) as case-insensitive substrings, so `-k add` also matches `test_address`. `-m` matches marker names exactly, for example `-m smoke` or `-m "regression and not slow"`. `-k` needs no setup and is good for quick ad-hoc runs; `-m` is better for stable categories, with markers registered and `--strict-markers` on. Both accept `and`, `or`, `not` and parentheses, you should quote the expression, and if you give both a test must satisfy both filters.
</details>

---

## Intermediate (Application)

### Q15: A teammate wrote 12 tests in `tests/login_tests.py` and the pipeline has been green for months. Later you discover none of them ever ran. What happened, and how do you fix and prevent it?
**Keywords:** Naming pattern, `test_*.py`, `--collect-only`, `python_files`, Silent hole
**Hint:** Look at the file name against the default pattern.

<details>
<summary>Click to Reveal Answer</summary>

The file name `login_tests.py` matches neither `test_*.py` nor `*_test.py`, so PyTest never collected it and there was no failure to turn the build red. The best fix is to rename it to `test_login.py`. The alternative is adding the pattern to `python_files` in `pytest.ini`, but renaming follows the standard everyone expects. To prevent it, after adding any new test file I run `python -m pytest --collect-only -q` and confirm the new tests appear, ideally as part of code review.
</details>

---

### Q16: Your smoke suite is run with `-m smoke`, but one important smoke test never runs and nobody notices. A teammate wrote `@pytest.mark.smoek`. How did this happen and how do you stop it happening again?
**Keywords:** Unregistered marker, Warning, `--strict-markers`, `markers`, `addopts`

<details>
<summary>Click to Reveal Answer</summary>

Without strictness an unknown marker only produces a `PytestUnknownMarkWarning`, and `smoek` quietly becomes a new marker, so `-m smoke` never selects the test. The fix is to register the markers under `markers` in `pytest.ini` and put `--strict-markers` in `addopts`. Then the typo becomes a collection error, `'smoek' not found in markers configuration option`, and is fixed immediately. Registering also documents each marker's meaning for the team.

```ini
[pytest]
addopts = -ra --strict-markers
markers =
    smoke: quick sanity checks
    regression: broad pre-release checks
```
</details>

---

### Q17: A `withdraw(balance, amount)` function raises `ValueError` both for non-positive amounts and for insufficient funds. How would you write tests that prove each case raises for the right reason?
**Keywords:** `pytest.raises`, `match`, `excinfo`, After the `with` block, Specific exception
**Hint:** Checking only the exception type could pass for the wrong reason.

<details>
<summary>Click to Reveal Answer</summary>

I would use `pytest.raises(ValueError, match=...)` so the test checks the message too, since both cases raise the same type. `match` is a regular expression searched in the exception's string. For more detail I use `as excinfo` and inspect `excinfo.value` after the `with` block ends, because it is not populated inside it. I would also avoid `pytest.raises(Exception)` because it is too broad.

```python
def test_negative_amount_raises():
    with pytest.raises(ValueError, match="must be positive"):
        withdraw(100, -5)

def test_too_much_reports_details():
    with pytest.raises(ValueError) as excinfo:
        withdraw(50, 80)
    assert "Insufficient funds" in str(excinfo.value)
```
</details>

---

### Q18: Your CI job runs `python -m pytest -k "logn"` (a typo) and the build looks green in the log. What should happen, and how do you make sure CI catches it?
**Keywords:** Exit code 5, No tests collected, Exit code 0, `--collect-only`, CI

<details>
<summary>Click to Reveal Answer</summary>

PyTest should return exit code 5, meaning no tests were collected, because a filter that matches nothing is not a pass. CI tools decide pass or fail from the exit code, not from the printed text, so the pipeline must treat any non-zero code, including 5, as a failure. If a script only reads the output it can pass silently. The full table is 0 all passed, 1 some failed, 2 interrupted, 3 internal error, 4 usage error, 5 no tests collected. Before using a new filter in a pipeline, I dry-run it with `--collect-only -q` to see which tests it selects.
</details>

---

### Q19: A test class has `test_login` that sets `self.token = "abc"`, and `test_use_token` that reads `self.token`. It fails with `AttributeError`. What is wrong and how do you fix it?
**Keywords:** Fresh instance, Independent tests, `self`, Order dependence, Build data in each test

<details>
<summary>Click to Reveal Answer</summary>

PyTest creates a new instance of the class for every test method, so the attribute set on `self` in the first test does not exist in the second. The failure is correctly flagging a bad design: tests must be independent and must not rely on running order or on side effects of another test. The fix is to build the data inside each test (and, from Tuesday, share setup properly). I would also avoid mutable class-level attributes such as lists, because those are shared across instances and leak state between tests.
</details>

---

## Advanced (Deep Dive)

### Q20: A test calls a helper `check_equal(a, b)` that contains `assert a == b` in a regular `helpers.py` module, and the failure shows only a bare `AssertionError` with no values. Why, and what are your options?
**Keywords:** Assertion rewriting, Import hook, Test modules only, `pytest.register_assert_rewrite`, `conftest.py`
**Hint:** Remember when and where PyTest rewrites `assert` statements.

<details>
<summary>Click to Reveal Answer</summary>

PyTest's rich output comes from rewriting `assert` statements through an import hook when modules are imported, and that rewriting applies only to test modules, `conftest.py` files and plugins. An ordinary helper module you import is not rewritten, so its `assert` behaves like plain Python and just raises `AssertionError`. The options are to keep assertions in the test files, or to register the helper with `pytest.register_assert_rewrite("helpers")` before it is imported, which is the approach used when building custom assertion helpers. Adding an explicit message such as `assert a == b, f"{a!r} != {b!r}"` also helps. I confirmed this behaviour by running a small example.

```python
# conftest.py (or a plugin), before helpers is imported
import pytest
pytest.register_assert_rewrite("helpers")
```
</details>

---

## Coverage Table

| Lesson | Question numbers |
|---|---|
| PyTest Installation and Configuration | Q1, Q2, Q3, Q4, Q5 |
| Test Discovery and Organization | Q6, Q7, Q8, Q15 |
| Test Functions and Classes | Q9, Q10, Q19 |
| Assertions and Assertion Introspection | Q11, Q12, Q17, Q20 |
| Markers | Q13, Q16 |
| Test Execution and Filtering | Q8, Q14, Q18 |

Distribution: 14 Beginner (Q1-Q14), 5 Intermediate (Q15-Q19), 1 Advanced (Q20) = 20 questions.
