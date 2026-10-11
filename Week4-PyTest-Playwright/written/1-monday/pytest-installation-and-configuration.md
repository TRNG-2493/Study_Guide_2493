# PyTest Installation and Configuration

## Learning Objectives

By the end of this lesson you will be able to:

- Explain what PyTest is, what problem it solves, and how it differs from Python's built-in `unittest` module.
- Create and activate an isolated Python virtual environment for a test project.
- Install PyTest with `pip`, verify the installation, and pin a version in `requirements.txt`.
- Run PyTest in two ways (`pytest` and `python -m pytest`) and explain the difference.
- Create a PyTest configuration file (`pytest.ini` or `pyproject.toml`) and explain the most important options: `testpaths`, `addopts`, `markers`, `minversion`, `python_files`, and `pythonpath`.
- Explain how PyTest decides which configuration file to use (rootdir and inifile detection).
- Lay out a clean, beginner-friendly project structure for the Project 1 test suite.
- Diagnose the most common installation and configuration problems.

---

## Why This Matters

This week is about converting the manual test design you have been practising into **automated tests**. The weekly epic is: PyTest from basics to a reporting framework, then CSS/XPath locators and Playwright core automation. Every single thing you build this week, including the Playwright browser tests on Thursday and Friday, runs on top of PyTest. If PyTest is not installed correctly, or if your project is not configured in a predictable way, every later step becomes harder.

In **Project 1: QE Foundations**, you will automate tests each day. Today's milestone is to automate the Project 1 utility tests (small, pure Python functions that are easy to test) with PyTest. A solid setup means:

- Your teammates can clone your repository, run **one command**, and get the same result you got.
- Your tests run the same way on your laptop and on a build server (a CI pipeline). Real companies will not accept "it works on my machine".
- You do not have to retype long command-line options every time, because they live in a configuration file.

Think of this lesson as setting up your workshop before building furniture. It is not the exciting part, but a well-organised workshop prevents hours of frustration later.

---

## The Concept

### 1. What is PyTest?

**PyTest** is an open-source testing framework for Python. A *testing framework* is a tool that:

1. **Finds** your tests automatically.
2. **Runs** them.
3. **Reports** which ones passed and which ones failed, and **why**.

Python already ships with a testing module called `unittest`. So why do almost all modern Python teams use PyTest instead? Here is a comparison.

| Feature | `unittest` (built in) | PyTest |
|---|---|---|
| Test is written as | A method inside a class that inherits from `unittest.TestCase` | A plain function (class optional) |
| Assertions | Special methods: `assertEqual`, `assertTrue`, `assertIn`... | The plain Python `assert` statement |
| Boilerplate | More (imports, class, `self`) | Very little |
| Failure messages | Good | Excellent (shows values of every part of the expression) |
| Plugins | Few | Hundreds (HTML reports, parallel runs, Playwright, coverage...) |
| Can run `unittest` tests? | Yes | Yes. PyTest can run existing `unittest` tests too |

The main reason is **simplicity**. Compare these two tests, which check the same thing:

```python
# unittest style
import unittest

class TestMath(unittest.TestCase):
    def test_add(self):
        self.assertEqual(2 + 3, 5)

if __name__ == "__main__":
    unittest.main()
```

```python
# PyTest style
def test_add():
    assert 2 + 3 == 5
```

The PyTest version has 2 lines. Beginners can read it without learning anything new, because `assert` is plain Python. You will explore this in depth in the lesson *Assertions and Assertion Introspection* later today.

### 2. Prerequisites

You need:

- **Python 3.9 or newer.** PyTest 8.x supports modern Python 3 versions; recent 8.x releases dropped Python 3.8, so 3.9+ is the safe baseline (Python 3.11 or 3.12 is a good choice). Check with:

```bash
python --version
```

On some systems the command is `python3 --version` (macOS and Linux) or `py --version` (the Windows launcher).

- **pip**, Python's package installer, which comes with Python. Check with:

```bash
python -m pip --version
```

- A **code editor**. VS Code or PyCharm are both excellent.

### 3. Virtual Environments: Why and How

#### What is a virtual environment?

A **virtual environment** (venv) is a private, isolated folder that holds its own copy of the Python interpreter settings and its own installed packages. Everything you `pip install` while the environment is active goes **into that folder only**, not into your system-wide Python.

#### Why do we need one?

Imagine you have two projects. Project A needs PyTest 7 and Project B needs PyTest 8. If you install packages globally, one project will break the other. With virtual environments each project has its own packages. Other benefits:

- Your global Python stays clean.
- You can reproduce the exact set of packages later (`pip freeze`).
- You avoid permission errors that happen when installing globally.

**Analogy:** A virtual environment is a separate toolbox for each project. You would not mix the screwdrivers for a watch repair with the tools for fixing a car.

#### Creating the environment (step by step)

1. Create a project folder and move into it:

```bash
mkdir qe-foundations-tests
cd qe-foundations-tests
```

2. Create the virtual environment. By convention we name it `.venv`:

```bash
python -m venv .venv
```

Line by line: `python` runs the interpreter, `-m venv` says "run the standard-library module called `venv`", and `.venv` is the folder name to create.

3. Activate it. The command depends on your operating system and shell:

| OS / shell | Activation command |
|---|---|
| Windows (Command Prompt) | `.venv\Scripts\activate.bat` |
| Windows (PowerShell) | `.venv\Scripts\Activate.ps1` |
| macOS / Linux (bash, zsh) | `source .venv/bin/activate` |

When activation works, your terminal prompt starts with `(.venv)`. That is the signal that you are "inside" the environment.

> **Windows PowerShell tip:** If you see an error about "running scripts is disabled on this system", run `Set-ExecutionPolicy -Scope CurrentUser RemoteSigned` once, then try again. Alternatively use Command Prompt.

4. To leave the environment later, type `deactivate`.

> **Important:** Never commit the `.venv` folder to Git. Add it to `.gitignore`. Other people will rebuild it from `requirements.txt`.

### 4. Installing PyTest

With the environment active:

```bash
python -m pip install pytest
```

PyTest and its small dependencies (such as `pluggy`, `iniconfig`, and `packaging`) are downloaded from **PyPI** (the Python Package Index) and installed into `.venv`.

#### Verify the installation

```bash
pytest --version
```

Expected output looks like:

```
pytest 8.3.4
```

(Your exact version number will differ; any `8.x` is correct for this course.)

You can also run:

```bash
python -m pip show pytest
```

which prints the version, location, and what it requires.

#### Installing a specific version

Sometimes a team needs everyone on exactly the same version:

```bash
python -m pip install "pytest==8.3.4"          # exact version
python -m pip install "pytest>=8.0,<9.0"       # any 8.x
python -m pip install --upgrade pytest         # upgrade to latest
```

The quotes protect the `<` and `>` characters from being interpreted by the shell as redirection.

### 5. Recording Dependencies in `requirements.txt`

A `requirements.txt` file is a plain text list of the packages your project needs. Create it in the project root:

```text
pytest>=8.0,<9.0
```

Anyone can now recreate your environment with:

```bash
python -m pip install -r requirements.txt
```

Later this week you will add more lines (for example an HTML-report plugin on Wednesday and Playwright on Thursday). `pip freeze > requirements.txt` captures **every** installed package with exact versions. This is precise but noisy; for learning projects, a short hand-written list is easier to maintain.

### 6. Running PyTest: `pytest` vs `python -m pytest`

There are two ways to start PyTest:

```bash
pytest
python -m pytest
```

They are almost identical. The difference: `python -m pytest` also adds the **current working directory** to `sys.path` (the list of folders Python searches when you write `import something`). This matters when your tests import code from your project folder, which is exactly what you will do in Project 1. If you see `ModuleNotFoundError` for your own code when using plain `pytest`, try `python -m pytest`, or configure `pythonpath` (shown below). Another benefit: `python -m pytest` guarantees you use the PyTest installed for *that exact* `python`, which avoids "wrong interpreter" confusion.

**Recommendation for this course:** use `python -m pytest` until you are comfortable.

### 7. Your First Test (to prove everything works)

Create a file named `test_smoke.py` in your project folder:

```python
def test_python_is_working():
    assert 1 + 1 == 2
```

Run:

```bash
python -m pytest
```

Output (approximately):

```
============================= test session starts =============================
platform win32 -- Python 3.12.1, pytest-8.3.4, pluggy-1.5.0
rootdir: C:\work\qe-foundations-tests
collected 1 item

test_smoke.py .                                                          [100%]

============================== 1 passed in 0.02s ==============================
```

Reading the output:

- `platform ... Python ... pytest ...`: your environment details.
- `rootdir`: the folder PyTest treats as the project root (more on this in a moment).
- `collected 1 item`: PyTest found 1 test. *Collection* is the discovery phase. We study it in the next lesson.
- `test_smoke.py .`: one dot means one passed test. `F` means failed, `E` means error, `s` skipped, `x` expected failure.
- Final line: summary and duration.

### 8. Configuration Files

#### Why configure PyTest at all?

PyTest works with zero configuration, but real projects always add some. Configuration lets you:

- Tell PyTest where your tests live (`testpaths`).
- Set default command-line options so nobody has to remember them (`addopts`).
- Register custom markers (`markers`). We cover markers in a later lesson today.
- Make sure your project's own code can be imported (`pythonpath`).
- Enforce a minimum PyTest version (`minversion`).

#### Where can configuration live?

PyTest looks for these files, in this order of priority (first match wins for deciding the config file):

1. `pytest.ini`: dedicated PyTest file. It always wins if present, even if empty.
2. `pyproject.toml`: used if it contains a `[tool.pytest.ini_options]` table.
3. `tox.ini`: used if it contains a `[pytest]` section.
4. `setup.cfg`: used if it contains a `[tool:pytest]` section.

Beginners should pick **`pytest.ini`**, because it is the simplest and the least surprising. Teams that already use `pyproject.toml` for other tools often put the settings there instead. Both are shown below.

#### A first `pytest.ini`

```ini
[pytest]
minversion = 8.0
testpaths = tests
addopts = -ra -q
```

Line by line:

| Line | Meaning |
|---|---|
| `[pytest]` | Section header. In `pytest.ini` it must be exactly `[pytest]`. |
| `minversion = 8.0` | If the installed PyTest is older than 8.0, stop with a clear error instead of behaving strangely. |
| `testpaths = tests` | When you run `pytest` with no arguments, look only in the `tests` folder. This also makes collection faster. |
| `addopts = -ra -q` | "Add options". These are inserted into every command line automatically. `-r a` prints a short summary of **a**ll non-passing outcomes at the end, and `-q` means quiet (less verbose header). |

The same settings in `pyproject.toml`:

```toml
[tool.pytest.ini_options]
minversion = "8.0"
testpaths = ["tests"]
addopts = "-ra -q"
```

Note the TOML differences: strings are quoted, and lists use square brackets.

#### More useful options

```ini
[pytest]
minversion = 8.0
testpaths = tests
pythonpath = .
python_files = test_*.py *_test.py
addopts = -ra --strict-markers --strict-config
markers =
    smoke: quick sanity checks that should always pass
    regression: broader checks run before a release
```

| Option | What it does |
|---|---|
| `pythonpath = .` | Adds the project root to `sys.path` (a built-in option since PyTest 7). Lets `from src.utils import ...` work with plain `pytest`. You can list several folders on separate lines. |
| `python_files` | Filename patterns that PyTest treats as test files. The default is `test_*.py` and `*_test.py`. You will see how to change naming rules in the next lesson. |
| `--strict-markers` | A marker not registered under `markers` becomes an **error** rather than a warning. This catches typos like `@pytest.mark.smoek`. |
| `--strict-config` | Unknown configuration keys raise an error instead of being silently ignored. This catches typos in the config file itself. |
| `markers` | Registers custom marker names with a description. Multi-line value: each marker is on its own indented line, in the form `name: description`. |

#### How PyTest finds the configuration: rootdir and inifile

When you run PyTest it determines two things:

- **inifile**: the configuration file it will use.
- **rootdir**: the base folder used for things like the cache directory and test IDs.

It looks at the arguments you passed (or the current directory), then walks **upward** through parent folders looking for `pytest.ini`, `pyproject.toml`, `tox.ini`, or `setup.cfg`. The first folder containing a match becomes the rootdir. You can see both in the header:

```
rootdir: C:\work\qe-foundations-tests
configfile: pytest.ini
testpaths: tests
```

Practical lesson: **always run PyTest from the project root** (where `pytest.ini` lives) so you never wonder which file is being used. If PyTest does not print a `configfile:` line, it is using none.

#### Overriding and ignoring configuration

```bash
python -m pytest -o addopts=""        # override an ini value for one run
python -m pytest -c other.ini         # use a different config file
python -m pytest --rootdir=.          # force the rootdir
```

### 9. A Recommended Project Layout

Here is a simple layout for the Project 1 utility tests:

```
qe-foundations-tests/
├── .venv/                  # virtual environment (NOT committed)
├── .gitignore
├── pytest.ini
├── requirements.txt
├── src/
│   ├── __init__.py
│   └── utils.py            # the code under test
└── tests/
    ├── __init__.py
    └── test_utils.py       # the tests
```

Separating **source code** (`src`) from **tests** (`tests`) is a widely used convention. The `__init__.py` files (they may be empty) make the folders into Python packages, which keeps imports predictable. You will study the naming and discovery rules that apply to this layout in the next lesson, *Test Discovery and Organization*.

A matching `.gitignore` (minimum):

```gitignore
.venv/
__pycache__/
.pytest_cache/
*.pyc
```

`.pytest_cache/` is a folder PyTest creates to remember things between runs (for example, which tests failed last time, enabling `--lf`, which you will learn in *Test Execution and Filtering*).

---

## Code Examples with Line-by-Line Explanations

### Example 1: A tiny utility and its tests

`src/utils.py`:

```python
def add(a, b):
    """Return the sum of two numbers."""
    return a + b


def is_even(number):
    """Return True when number is divisible by 2."""
    return number % 2 == 0
```

`tests/test_utils.py`:

```python
from src.utils import add, is_even


def test_add_two_positive_numbers():
    assert add(2, 3) == 5


def test_is_even_returns_true_for_four():
    assert is_even(4) is True
```

`pytest.ini`:

```ini
[pytest]
minversion = 8.0
testpaths = tests
pythonpath = .
addopts = -ra
```

Explanation:

1. `from src.utils import add, is_even`: imports the functions we want to test. This only works because `pythonpath = .` put the project root on `sys.path`, so `src` is importable.
2. `def test_add_two_positive_numbers():` is a test function. PyTest collects it because the name starts with `test_` and the file name starts with `test_`.
3. `assert add(2, 3) == 5`: calls the function and asserts the result. If it is not `5`, the test fails.
4. `is True`: `is_even` should return exactly the boolean `True`. For booleans, comparing with `is` is precise.

Run it:

```bash
python -m pytest
```

Expected: `2 passed`.

### Example 2: Proving configuration works with a typo catch

Add a test using an unregistered marker:

```python
import pytest

@pytest.mark.smoek      # typo on purpose
def test_add_zero():
    assert add(5, 0) == 5
```

With `--strict-markers` in `addopts` and no `smoek` registered, PyTest stops with an error such as `'smoek' not found in markers configuration option`. Without strict mode it would only warn, and you might not notice that your filtering never selects the test. This is a good habit: **make typos loud**.

### Example 3: The same configuration in `pyproject.toml`

```toml
[tool.pytest.ini_options]
minversion = "8.0"
testpaths = ["tests"]
pythonpath = ["."]
addopts = "-ra --strict-markers"
markers = [
    "smoke: quick sanity checks that should always pass",
    "regression: broader checks run before a release",
]
```

Notice `pythonpath` is a list here, and `markers` is a list of strings.

---

## Real-World Scenarios

1. **New team member onboarding.** A new QA engineer joins. The README says: clone, create venv, `pip install -r requirements.txt`, `python -m pytest`. Five minutes later they see a green run. The pinned `requirements.txt` and shared `pytest.ini` are why this works.
2. **CI pipeline.** A build server (GitHub Actions, Jenkins) creates a fresh virtual environment on every build and runs the same command. Since `addopts` lives in `pytest.ini`, the pipeline needs no special flags.
3. **Upgrading safely.** When PyTest 9 is released, the team bumps the pin in a branch, runs the suite, and fixes anything that breaks, instead of discovering it mid-release.

---

## Common Mistakes

| Mistake | Symptom | Fix |
|---|---|---|
| Installing PyTest globally and forgetting to activate the venv | `pytest: command not found`, or tests use the wrong packages | Activate `.venv` (prompt shows `(.venv)`). Use `python -m pytest`. |
| `ModuleNotFoundError: No module named 'src'` | Test file cannot import project code | Run `python -m pytest` or set `pythonpath = .` and make sure you run from the project root. |
| Wrong section header, e.g. `[tool:pytest]` inside `pytest.ini` | Settings silently ignored | In `pytest.ini` use `[pytest]`; `[tool:pytest]` is only for `setup.cfg`. |
| Misspelled option names | Silently ignored | Add `--strict-config` to `addopts`. |
| Putting `pytest.ini` in the wrong folder | No `configfile:` line in output | Place it in the project root and run from there. |
| Committing `.venv` | Huge repository | Add to `.gitignore`. |
| Naming your own file `pytest.py` | Weird import errors | Never name a file after an installed package. |
| Forgetting quotes around version specifiers | `>` creates a file named `=8.0` in the shell | Always quote: `"pytest>=8.0"`. |

---

## Practice Exercises

### Exercise 1: Environment and installation
1. Create a folder `week4-practice`. Create and activate a virtual environment.
2. Install PyTest and run `pytest --version`.
3. Write the version number you see in a text file called `my-version.txt`.

*Hint:* `python -m venv .venv`, then activate, then `python -m pip install pytest`.

### Exercise 2: Smoke test
Create `test_smoke.py` with a test that asserts `"qe".upper() == "QE"`. Run it with both `pytest` and `python -m pytest`. Confirm both pass.

### Exercise 3: Configuration file
Create a `pytest.ini` that:
- requires PyTest 8.0 or newer,
- searches only the `tests` folder,
- prints a summary of all non-passing tests,
- adds the project root to the import path.

**Solution:**

```ini
[pytest]
minversion = 8.0
testpaths = tests
pythonpath = .
addopts = -ra
```

### Exercise 4: Strict markers
Register a marker called `smoke`. Write a test decorated with `@pytest.mark.smoke`. Then misspell the decorator as `@pytest.mark.smok` and confirm that `--strict-markers` turns the typo into an error.

*Hint:* use the multi-line `markers =` syntax shown earlier.

### Exercise 5: Reproducible environment
Create `requirements.txt` containing only PyTest at version 8.x. Delete `.venv`, recreate it, and install from the file. Verify the tests still pass.

### Exercise 6 (challenge): Find the config file
Create two folders, `a` and `a/b`, with a `pytest.ini` in `a`. Run `python -m pytest` from inside `a/b` and read the `rootdir` and `configfile` lines. Explain in two sentences how PyTest found the file.

*Answer:* PyTest started in `a/b`, found no config there, then walked up to `a`, found `pytest.ini`, and set `a` as the rootdir.

---

## Summary

- **PyTest** is a Python testing framework that finds, runs, and reports tests, using plain functions and plain `assert`.
- Always use a **virtual environment** (`python -m venv .venv`) so project packages stay isolated.
- Install with `python -m pip install pytest`; verify with `pytest --version`; record it in `requirements.txt`.
- `python -m pytest` adds the current folder to `sys.path`; this is the safest way to run tests for your own code.
- A configuration file (`pytest.ini` is simplest, `pyproject.toml` is common) stores defaults: `testpaths`, `addopts`, `markers`, `minversion`, `pythonpath`.
- Use `--strict-markers` and `--strict-config` to turn silent typos into clear errors.
- PyTest finds the config by walking up from your run location; run from the project root to stay predictable.
- Next up: how PyTest **discovers** which files and functions are tests.

---

## Additional Resources

- PyTest Getting Started: https://docs.pytest.org/en/stable/getting-started.html
- PyTest Configuration (ini options, rootdir, inifile): https://docs.pytest.org/en/stable/reference/customize.html
- Python `venv` documentation: https://docs.python.org/3/library/venv.html
