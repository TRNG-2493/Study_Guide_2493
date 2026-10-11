# Test Discovery and Organization

## Learning Objectives

By the end of this lesson you will be able to:

- Explain what *test discovery* (collection) is and the phases PyTest goes through.
- State the default naming rules for test files, test functions, test classes, and test methods.
- Customize those rules with `python_files`, `python_classes`, and `python_functions`.
- Explain how `rootdir`, `testpaths`, `__init__.py`, and `conftest.py` affect discovery and imports.
- Understand the "rootdir/conftest" import modes at a beginner level, and why duplicate test file names can cause errors.
- Use `--collect-only` to see exactly what PyTest found, and `--ignore` / `norecursedirs` to exclude folders.
- Organize tests into folders by feature and by test type for the Project 1 suite.

---

## Why This Matters

The weekly epic asks you to convert manual test designs into an automated, maintainable suite. A suite with 10 tests can live in one file. A suite with 500 tests, written by a team over a year, cannot. How you **name** and **place** your tests decides whether:

- PyTest can find every test automatically (a test that is never discovered is a test that never runs, which is a silent hole in your safety net);
- a failing test can be traced back to a feature in seconds;
- teammates can add new tests without asking where they go.

In **Project 1: QE Foundations**, you will have utility tests today, then data-driven and UI tests later in the week. Organising them well now saves you from a painful reorganisation on Wednesday, when you build the reporting framework.

---

## The Concept

### 1. What does "discovery" mean?

When you type `python -m pytest`, PyTest does not simply run one file. It first performs **collection**, a process that works like this:

1. **Decide where to look.** Starting points are the arguments you gave (files or folders); if none, it uses `testpaths` from the config, or the current directory.
2. **Walk the folders** recursively, skipping some automatically (hidden folders starting with `.`, `venv`-like folders, `node_modules`, and others listed in `norecursedirs`).
3. **Pick test files** by name pattern.
4. **Import each test file** as a Python module.
5. **Pick test items** inside by name pattern: functions, classes, and methods.
6. Build a list of **test items** (each has a unique ID called a *node ID*), then **run** them.

Collection happens *before* any test runs. If a test file has a syntax error or a failing import, PyTest reports a **collection error** for that file; no tests from it run, and (by default) the whole session is interrupted with an error count.

### 2. The default naming rules

| What | Default rule | Examples that ARE collected | Examples that are NOT |
|---|---|---|---|
| Test file | `test_*.py` or `*_test.py` | `test_login.py`, `login_test.py` | `login.py`, `tests.py`, `testlogin.py` |
| Test function (module level) | name starts with `test` | `test_add`, `test_`, `testadd` | `check_add`, `add_test` |
| Test class | name starts with `Test`, and has **no `__init__` method** | `TestLogin`, `Test_Login` | `LoginTests`, `TestHelper` with `__init__` |
| Test method (inside a Test class) | name starts with `test` | `test_valid_user` | `verify_user` |

Common surprises for beginners:

- **`tests.py` is NOT discovered.** The pattern requires `test_` at the start or `_test` at the end of the filename stem. `tests.py` has neither.
- **`LoginTests` class is NOT discovered.** The class prefix must be `Test`, capital T, at the start.
- **A class with `__init__` is skipped** (PyTest emits a warning). PyTest creates a fresh instance of the class for every test method, so it does not support constructors. Use setup features (covered on Tuesday) instead.
- Helper functions with any other name are simply ignored, so you can write helpers freely.

Case matters on most systems: `Test_Login.py` is not matched by `test_*.py` on Linux. Keep file names lowercase with underscores.

### 3. Customizing the naming rules

If your company uses different conventions, change them in `pytest.ini`:

```ini
[pytest]
python_files = test_*.py check_*.py
python_classes = Test* Check*
python_functions = test_* verify_*
```

Each value is a space-separated list of glob-style patterns:

- `python_files`: matched against file names.
- `python_classes`: matched against class names (a prefix pattern or glob).
- `python_functions`: matched against function and method names.

With the config above, a function `verify_login()` inside `check_auth.py` is now a test. **Advice:** do not customise unless you must. Standard names are what every PyTest developer expects.

### 4. Choosing what to run: arguments and `testpaths`

```bash
python -m pytest                              # uses testpaths, or current directory
python -m pytest tests/                       # a folder
python -m pytest tests/test_utils.py          # a file
python -m pytest tests/test_utils.py::test_add            # one function
python -m pytest tests/test_utils.py::TestMath::test_add  # one method in a class
```

The `file::function` and `file::Class::method` notation is called the **node ID**. It is the unique address of a test. You will use node IDs constantly when re-running one failing test; Friday's `--collect-only` and the reports you build on Wednesday also display them.

### 5. Seeing what PyTest found: `--collect-only`

The single most useful discovery tool:

```bash
python -m pytest --collect-only
```

Sample output:

```
<Dir qe-foundations-tests>
  <Dir tests>
    <Module test_utils.py>
      <Function test_add_two_positive_numbers>
      <Function test_is_even_returns_true_for_four>
```

If a test you wrote is missing from this tree, the name patterns are the first suspect. A quieter version prints just node IDs:

```bash
python -m pytest --collect-only -q
```

```
tests/test_utils.py::test_add_two_positive_numbers
tests/test_utils.py::test_is_even_returns_true_for_four

2 tests collected in 0.01s
```

### 6. Excluding things from discovery

Some folders hold code that looks like tests but is not (old drafts, helper scripts, generated files).

Option A: command line

```bash
python -m pytest --ignore=tests/legacy
python -m pytest --ignore=tests/legacy/test_old.py
python -m pytest --deselect tests/test_utils.py::test_slow_one
```

`--ignore` prevents even *importing* the path. `--deselect` collects the test but removes it from the run.

Option B: configuration

```ini
[pytest]
norecursedirs = legacy build dist .git node_modules *.egg
```

Be aware: setting `norecursedirs` **replaces** PyTest's defaults (which already skip `.*`, `build`, `dist`, `venv`, `node_modules`, `*.egg`, `__pycache__`-like entries), so include any defaults you still want.

### 7. Packages, `__init__.py`, and import modes

To run a test file, PyTest must *import* it as a Python module. To import, it must know the module's name and add the right folder to `sys.path`. By default (the `prepend` import mode) PyTest does this:

- **If the test folder has NO `__init__.py`:** PyTest inserts that folder into `sys.path` and imports the file by its bare name (e.g. `test_utils`). Consequence: **two test files in different folders cannot share the same file name.** For example `tests/api/test_login.py` and `tests/ui/test_login.py` collide, and PyTest reports "import file mismatch".
- **If the folder HAS `__init__.py`:** PyTest walks up to the first folder *without* `__init__.py`, inserts that into `sys.path`, and imports with a dotted name like `tests.api.test_login`. The same file name in two different packages is fine.

Practical guidance for beginners (the rule used in this course):

> **Either** give every test folder an `__init__.py` file, **or** make every test file name unique. Using `__init__.py` is the more scalable choice.

PyTest also offers `--import-mode=importlib`, which does not modify `sys.path` and allows duplicate names. It is the recommended mode for new projects in the official documentation, but it has trade-offs (test files cannot import each other as plain modules). For now, know that it exists:

```ini
[pytest]
addopts = --import-mode=importlib
```

### 8. `conftest.py`: a first look

A file named exactly `conftest.py` is special: PyTest imports it automatically, before the tests in its folder and sub-folders. Its main purpose is to share fixtures and hooks. **We will cover fixtures and `conftest.py` in depth on Tuesday**, so today just remember two things:

- Never name a *test* file `conftest.py`.
- A `conftest.py` is not collected as tests, but its presence changes how PyTest sets up `sys.path`, so it appears in the discovery diagrams of bigger projects.

### 9. How to organize a growing suite

There are two common strategies, and teams often mix them.

**Strategy A: by feature (mirrors the application)**

```
tests/
├── __init__.py
├── string_utils/
│   ├── __init__.py
│   └── test_formatting.py
├── math_utils/
│   ├── __init__.py
│   └── test_calculations.py
└── validators/
    ├── __init__.py
    └── test_email_validator.py
```

**Strategy B: by test type**

```
tests/
├── __init__.py
├── unit/
│   ├── __init__.py
│   └── test_utils.py
├── integration/
│   ├── __init__.py
│   └── test_api.py
└── ui/
    ├── __init__.py
    └── test_login.py
```

Rules of thumb:

1. **One test file per module under test** (`utils.py` is tested by `test_utils.py`). It makes failing tests easy to locate.
2. **Group related tests** in one file or one class. A file with 300 unrelated tests is hard to navigate.
3. **Name tests as sentences** that describe behaviour: `test_is_even_returns_false_for_odd_number` beats `test1`.
4. **Keep test code independent**: a test must not depend on another test having run first. PyTest runs tests in file order by default, but you must never rely on it.
5. **Separate slow tests** from fast ones (we will use markers for this later today).

---

## Code Examples with Line-by-Line Explanations

### Example 1: What is and is not collected

Create `tests/test_naming_demo.py`:

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

Run:

```bash
python -m pytest tests/test_naming_demo.py --collect-only -q
```

Expected collected items:

```
tests/test_naming_demo.py::test_collected_function
tests/test_naming_demo.py::testcollected_without_underscore
tests/test_naming_demo.py::TestCollectedClass::test_method_is_collected
```

Explanation:

| Code | Collected? | Reason |
|---|---|---|
| `test_collected_function` | Yes | Name starts with `test`. |
| `testcollected_without_underscore` | Yes | Default rule is the prefix `test`, with no underscore required. |
| `check_not_collected` | No | Wrong prefix. |
| `TestCollectedClass.test_method_is_collected` | Yes | Class starts with `Test`, method with `test`. |
| `TestCollectedClass.helper_not_collected` | No | Method name does not start with `test`. |
| `NotATestClass.test_ignored...` | No | Class name does not start with `Test`. |
| `TestWithInit` | No | It defines `__init__`; PyTest warns "cannot collect test class because it has a `__init__` constructor". |

### Example 2: A duplicate file name problem

```
tests/
├── api/
│   └── test_login.py
└── ui/
    └── test_login.py
```

With no `__init__.py` files, `python -m pytest` reports an error similar to:

```
import file mismatch:
imported module 'test_login' has this __file__ attribute: ...api/test_login.py
which is not the same as the test file we want to collect: ...ui/test_login.py
HINT: remove __pycache__ / .pyc files and/or use a unique basename for your test file modules
```

Two ways to fix it:

```
tests/
├── __init__.py
├── api/
│   ├── __init__.py       <- add these
│   └── test_login.py
└── ui/
    ├── __init__.py       <- add these
    └── test_login.py
```

or rename one file to `test_login_ui.py`. Both work; packages scale better.

### Example 3: Organising Project 1 utility tests

`src/string_utils.py`:

```python
def reverse_text(text):
    return text[::-1]


def is_palindrome(text):
    cleaned = "".join(ch.lower() for ch in text if ch.isalnum())
    return cleaned == cleaned[::-1]
```

`tests/string_utils/test_text_functions.py`:

```python
from src.string_utils import reverse_text, is_palindrome


class TestReverseText:
    def test_reverses_simple_word(self):
        assert reverse_text("abc") == "cba"

    def test_empty_string_stays_empty(self):
        assert reverse_text("") == ""


class TestIsPalindrome:
    def test_detects_simple_palindrome(self):
        assert is_palindrome("level") is True

    def test_ignores_case_and_punctuation(self):
        assert is_palindrome("A man, a plan, a canal: Panama") is True

    def test_rejects_non_palindrome(self):
        assert is_palindrome("python") is False
```

Explanation of the code:

1. `text[::-1]` is Python slice syntax (start:stop:step) with step `-1`, which walks the string backwards, so it reverses it.
2. In `is_palindrome`, the generator expression keeps only letters and digits (`ch.isalnum()`), lowercases them, and `"".join(...)` turns them back into a string. Then it compares the string with its reverse.
3. Each class groups tests for one function. The class names start with `Test`; the methods start with `test_`; none define `__init__`.
4. `self` is required as the first parameter of a method; PyTest supplies it. We study classes fully in the next lesson.

Check what PyTest sees:

```bash
python -m pytest tests/string_utils --collect-only -q
```

```
tests/string_utils/test_text_functions.py::TestReverseText::test_reverses_simple_word
tests/string_utils/test_text_functions.py::TestReverseText::test_empty_string_stays_empty
tests/string_utils/test_text_functions.py::TestIsPalindrome::test_detects_simple_palindrome
tests/string_utils/test_text_functions.py::TestIsPalindrome::test_ignores_case_and_punctuation
tests/string_utils/test_text_functions.py::TestIsPalindrome::test_rejects_non_palindrome
```

(For `from src.string_utils import ...` to work, make sure `pythonpath = .` is in `pytest.ini`, as covered in the previous lesson.)

---

## Real-World Scenarios

1. **The test that never ran.** A tester writes `tests/login_tests.py` with 12 good tests. The pipeline is green for months because the file name matches neither `test_*.py` nor `*_test.py`, so nothing in it ran. A `--collect-only` check in code review would have caught it. Lesson: after adding a file, always confirm the new tests show up in the collection.
2. **Merging two teams' work.** The API team and UI team each have a `test_login.py`. When merged, CI fails with "import file mismatch". Adding `__init__.py` files to both folders fixes it.
3. **Running only a feature.** A developer changes the validators and runs `python -m pytest tests/validators` for fast feedback before pushing, rather than waiting for the full suite.
4. **Legacy scripts.** An old `tests/legacy` folder contains scripts that need a retired server. The team adds `norecursedirs = legacy` so PyTest skips them without deleting history.

---

## Common Mistakes

| Mistake | Why it fails | Fix |
|---|---|---|
| File named `tests.py` or `login_tests.py` | Does not match `test_*.py` / `*_test.py` | Rename to `test_login.py`. |
| Function named `check_login()` or `login_test()` | Must *start* with `test` | Rename to `test_login()`. |
| Class named `LoginTests` | Must start with `Test` | Rename to `TestLogin`. |
| `__init__` in a test class | Class is skipped with a warning | Remove it; use Tuesday's setup techniques. |
| Same file name in two folders, no `__init__.py` | Import mismatch | Add `__init__.py` or rename. |
| Collection error ignored because some tests passed | A broken file contributes no tests | Read the "ERRORS" section at the top of output; fix imports first. |
| Running from the wrong folder | `testpaths` and relative paths resolve unexpectedly | Run from the project root. |
| Stale `__pycache__` after renaming files | Strange mismatch errors | Delete `__pycache__` folders and `.pytest_cache`. |
| Test depends on another test's side effects | Fails when run alone or in a different order | Make every test self-contained. |

---

## Practice Exercises

### Exercise 1: Predict, then verify
For each name, decide: collected or not, using default rules.

1. `test_login.py` (file)
2. `loginTest.py` (file)
3. `def Test_add():` (function)
4. `def test_add():` inside `class Calculator:`
5. `def test_add(self):` inside `class TestCalculator:`

Write your predictions, create the files, and run `--collect-only` to check.

**Answers:** 1 yes. 2 no. 3 no (case-sensitive: `Test_add` does not start with lowercase `test`). 4 no (class name must start with `Test`). 5 yes.

### Exercise 2: Fix the invisible tests
You inherit `tests/auth_tests.py` containing `def test_valid_login(): assert True`. Make PyTest run it in two different ways: (a) rename the file; (b) change `python_files` in `pytest.ini`. Which would you choose in a real project and why?

*Hint for (b):* `python_files = test_*.py *_test.py auth_tests.py`. Renaming is better because it follows the standard that everyone expects.

### Exercise 3: Resolve the collision
Create `tests/api/test_login.py` and `tests/ui/test_login.py`, each with one passing test. Reproduce the import mismatch, then fix it with `__init__.py` files.

### Exercise 4: Organise Project 1
Take any two utility functions (for example `add` and `is_even`, or the string utilities above). Create a `src` folder, a `tests` folder with sub-folders per feature, and test classes per function. Show the output of `python -m pytest --collect-only -q`.

### Exercise 5: Exclude a folder
Create `tests/drafts/test_wip.py` with a failing assertion. Run the suite with `--ignore=tests/drafts`, then achieve the same result permanently using `norecursedirs` in the config file.

### Exercise 6: Single-test addresses
Using node IDs, write the exact commands to run: (a) just one method in a class; (b) every test in one class; (c) two specific functions in one command.

**Answer:**

```bash
python -m pytest tests/string_utils/test_text_functions.py::TestIsPalindrome::test_rejects_non_palindrome
python -m pytest tests/string_utils/test_text_functions.py::TestIsPalindrome
python -m pytest tests/test_utils.py::test_add_two_positive_numbers tests/test_utils.py::test_is_even_returns_true_for_four
```

---

## Summary

- PyTest **collects** tests first (find files, import them, find items), then runs them.
- Defaults: files `test_*.py` or `*_test.py`; functions and methods starting with `test`; classes starting with `Test` and **without** `__init__`.
- Customise with `python_files`, `python_classes`, `python_functions`, but prefer the standard names.
- Use `--collect-only -q` to verify discovery; use node IDs (`file::Class::method`) to run exact tests.
- Exclude with `--ignore`, `--deselect`, or `norecursedirs`.
- Give test folders `__init__.py` (or use unique file names) to avoid import mismatches.
- Organise by feature or by test type; keep one test file per module under test, descriptive names, and independent tests.
- `conftest.py` is special; we will cover it in depth on Tuesday.

---

## Additional Resources

- PyTest: Good Integration Practices (layouts, discovery, import modes): https://docs.pytest.org/en/stable/explanation/goodpractices.html
- PyTest: Changing standard (Python) test discovery: https://docs.pytest.org/en/stable/example/pythoncollection.html
- PyTest: Pytest import mechanisms and `sys.path`: https://docs.pytest.org/en/stable/explanation/pythonpath.html
