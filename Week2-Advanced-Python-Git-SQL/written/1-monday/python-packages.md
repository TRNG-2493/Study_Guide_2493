# Python Packages

## Learning Objectives

By the end of this lesson you will be able to:

- Define a Python package and explain how it differs from a single module.
- Create a package folder with an `__init__.py` file and import modules from it.
- Use absolute and relative imports correctly inside a package.
- Use `__init__.py` to build a clean public interface for your package.
- Create subpackages and understand dotted import paths such as `qa_toolkit.data.loaders`.
- Run a module inside a package with `python -m`, and make a package itself runnable with `__main__.py`.
- Recognise the difference between a *package* (code you import), a *distribution* (what you share/install) and a *project* (the repository), and know the basics of making a package installable with `pyproject.toml`.
- Structure a realistic QA utility library and avoid common packaging mistakes.

---

## Why This Matters

In the previous lesson you learned that one file equals one module. That is enough when you have three or four helpers. But a real test automation framework might have dozens of modules: API helpers, UI page objects, data factories, database checks, report formatters. Dumping them all in one folder becomes unmanageable, and name clashes become likely.

**Packages are how Python organises many modules into a hierarchy**, exactly like folders organise files on your computer. They are also how code gets shared: every library you will install with `pip` (such as `requests`, `pytest`, `selenium`) is a package. And in this week's Project 1 (QE Foundations), you will start a repository with a proper package structure so that later work (exception handling, data ingestion, unit tests, SQL validation helpers) has an organised home.

An analogy: a module is a **document**, and a package is a **filing cabinet drawer containing related documents, possibly with labelled folders (subpackages) inside**. `import` is you walking up and pulling out exactly the document you need by its filing path.

---

## The Concept

### 1. What Is a Package?

**Definition.** A *package* is a directory that contains Python modules (and optionally other directories of modules) and is importable as a unit. Traditionally, a directory is marked as a package by including a file named `__init__.py` inside it.

```
qa_toolkit/              <- the package (a folder)
├── __init__.py          <- marks it as a package; runs on import
├── validators.py        <- a module inside the package
└── formatters.py        <- another module
```

Importing from it:

```python
import qa_toolkit.validators
from qa_toolkit import formatters
from qa_toolkit.validators import is_valid_email
```

The **dotted path** mirrors the folder structure: `qa_toolkit.validators` means "the module `validators` inside the package `qa_toolkit`".

**Key vocabulary:**

| Term | Meaning |
|------|---------|
| Module | A single `.py` file |
| Package | A folder of modules, importable with dotted names |
| Subpackage | A package nested inside another package |
| `__init__.py` | The file that runs when the package is imported; marks the folder as a regular package |
| Namespace package | A folder without `__init__.py` that Python can still treat as a package (advanced; see note below) |

> **Regular vs namespace packages.** Since Python 3.3, a folder without `__init__.py` can still be imported as a so-called *namespace package*. That feature exists for special use cases (one logical package split across several locations). For your own projects, **always include `__init__.py`**. It makes your intent explicit, avoids surprises with tools, and gives you a place to define the package's public interface.

### 2. Building Your First Package, Step by Step

We will build a small QA utility library called `qa_toolkit`. Create a new working folder, for example `packages_lab`, and inside it:

```
packages_lab/
├── qa_toolkit/
│   ├── __init__.py
│   ├── validators.py
│   └── formatters.py
└── demo.py
```

#### Step 1: Create the folder and an empty `__init__.py`

On macOS/Linux:

```bash
mkdir -p packages_lab/qa_toolkit
cd packages_lab
touch qa_toolkit/__init__.py
```

On Windows PowerShell:

```powershell
mkdir packages_lab\qa_toolkit
cd packages_lab
New-Item qa_toolkit\__init__.py -ItemType File
```

An empty `__init__.py` is perfectly valid. It simply says "this folder is a package".

#### Step 2: Add modules

`qa_toolkit/validators.py`:

```python
"""Validation helpers."""


def is_valid_email(email):
    """Simple email check: one '@', text before it, a dot in the domain."""
    if not isinstance(email, str) or email.count("@") != 1:
        return False
    local, domain = email.split("@")
    return bool(local) and "." in domain and not domain.startswith(".") and not domain.endswith(".")


def is_non_empty(text):
    """True for strings that contain something other than whitespace."""
    return isinstance(text, str) and text.strip() != ""
```

`qa_toolkit/formatters.py`:

```python
"""Formatting helpers for test reports."""


def format_result(name, passed):
    """Return a single report line such as 'PASS  login works'."""
    status = "PASS" if passed else "FAIL"
    return f"{status}  {name}"


def format_summary(results):
    """Given a dict {test_name: bool}, return a multi-line summary string."""
    lines = [format_result(name, ok) for name, ok in results.items()]
    passed = sum(1 for ok in results.values() if ok)
    lines.append(f"{passed}/{len(results)} passed")
    return "\n".join(lines)
```

**Explanation of `format_summary`:**

- `results.items()` yields `(name, ok)` pairs from the dictionary.
- The list comprehension builds one formatted line per test.
- `sum(1 for ok in results.values() if ok)` counts how many values are `True` by adding 1 for each truthy value.
- `"\n".join(lines)` glues the lines with newline characters into one string.

#### Step 3: Use the package

`demo.py` (in `packages_lab`, **next to** the `qa_toolkit` folder, not inside it):

```python
from qa_toolkit import validators, formatters

results = {
    "valid email accepted": validators.is_valid_email("a@b.com"),
    "bad email rejected": not validators.is_valid_email("a@@b.com"),
    "empty string rejected": not validators.is_non_empty("   "),
}

print(formatters.format_summary(results))
```

Run from `packages_lab`:

```bash
python demo.py
```

Output:

```
PASS  valid email accepted
PASS  bad email rejected
PASS  empty string rejected
3/3 passed
```

**Why does this work?** The folder containing `demo.py` is `sys.path[0]` (see the modules lesson), and inside that folder Python finds a directory called `qa_toolkit` containing `__init__.py`, so it is a package. Then `validators` and `formatters` are found as modules inside it.

### 3. Three Ways to Import from a Package

```python
# (a) import the full dotted path; use the full dotted name
import qa_toolkit.validators
qa_toolkit.validators.is_valid_email("a@b.com")

# (b) import a module from the package; use module.function
from qa_toolkit import validators
validators.is_valid_email("a@b.com")

# (c) import a specific function; use it directly
from qa_toolkit.validators import is_valid_email
is_valid_email("a@b.com")
```

A subtle point about (a): `import qa_toolkit.validators` binds only the top-level name `qa_toolkit` in your file, so you must always write the full path when calling. `import qa_toolkit.validators as qv` gives you a shorter handle if you prefer.

### 4. What `__init__.py` Does

When you import a package, Python **runs its `__init__.py`** (once, like any module; see the modules lesson on caching). The names defined in `__init__.py` become attributes of the package. This gives you three uses:

#### Use 1: Mark the folder as a package (empty file)

The simplest and often sufficient.

#### Use 2: Package-level documentation and metadata

```python
"""qa_toolkit - small helpers for QA automation."""

__version__ = "0.1.0"
```

Now `import qa_toolkit; print(qa_toolkit.__version__)` prints `0.1.0`. Having a `__version__` string is a common convention.

#### Use 3: Re-export names to create a friendly public API

Users of your library should not need to remember which internal file holds which function. You can lift the important names up into the package namespace:

```python
"""qa_toolkit - small helpers for QA automation."""

from qa_toolkit.validators import is_valid_email, is_non_empty
from qa_toolkit.formatters import format_result, format_summary

__version__ = "0.1.0"

__all__ = [
    "is_valid_email",
    "is_non_empty",
    "format_result",
    "format_summary",
]
```

Now callers can write:

```python
import qa_toolkit

print(qa_toolkit.is_valid_email("a@b.com"))
print(qa_toolkit.format_result("smoke", True))
```

This is the pattern used by well-known libraries: you write `import requests; requests.get(...)`, not `requests.api.get(...)`, even though the function physically lives in an internal module.

**Guidelines for `__init__.py`:**

- Keep it **light**. Importing a package should be fast and have no side effects like network calls, or reading big files.
- Re-export deliberately, not with a blanket `from x import *`.
- Define `__all__` so tools know what is public.

### 5. Absolute vs Relative Imports

Inside a package, one module often needs to use another module in the same package. There are two ways to write that import.

**Absolute import:** spells out the full path from the top-level package.

```python
# inside qa_toolkit/formatters.py
from qa_toolkit.validators import is_non_empty
```

**Relative import:** uses dots to say "relative to my own location".

```python
# inside qa_toolkit/formatters.py
from .validators import is_non_empty       # one dot  = this package (same folder)
from . import validators                    # import a sibling module itself
from ..other_pkg import something           # two dots = parent package
```

| Dots | Meaning |
|------|---------|
| `.` | The current package (the folder this file is in) |
| `..` | The parent package (one folder up) |
| `...` | Grandparent (two levels up) |

**Which should you use?** PEP 8 recommends **absolute imports** as the default because they are explicit and readable, but accepts relative imports for complex package layouts, where absolute paths would be unwieldy. Relative imports have an advantage: if you rename the top-level package, they keep working. Either is acceptable; pick one style within a project and be consistent. In this course we favour absolute imports in application code and allow relative imports inside `__init__.py`.

**Important restriction:** relative imports work **only inside a package**, which means the file must be imported as part of the package (or run with `-m`). If you try to run a file that uses a relative import directly as a script:

```bash
python qa_toolkit/formatters.py
```

you get:

```
ImportError: attempted relative import with no known parent package
```

because when run directly, the file's `__name__` is `"__main__"`, not `"qa_toolkit.formatters"`, so Python does not know it belongs to a package. The fix is to run it as a module (next section).

### 6. Running Code Inside a Package: `python -m`

The `-m` flag tells Python: "treat this dotted name as a module and run it, with the **current directory** on `sys.path`."

```bash
# from packages_lab/ (the folder that CONTAINS qa_toolkit)
python -m qa_toolkit.formatters
```

Here Python imports `qa_toolkit.formatters` properly as part of its package (so relative imports work) and runs it with `__name__ == "__main__"`.

> **A harmless warning you may see.** If the package's `__init__.py` already imports that same module (as our final `qa_toolkit` does), Python prints a `RuntimeWarning: 'qa_toolkit.formatters' found in sys.modules after import of package...`. The code still runs. It is simply Python noting that the module was loaded once by `__init__.py` and then executed again as `__main__`. Running a *whole package* with `python -m qa_toolkit` (next subsection) does not have this issue. You will see `python -m pytest` and `python -m pip` later in the week, which use the same mechanism: running a module that lives inside an installed package.

#### Making a package itself runnable with `__main__.py`

If a package contains a file called `__main__.py`, then `python -m package_name` runs it. Create `qa_toolkit/__main__.py`:

```python
"""Allows:  python -m qa_toolkit"""

from qa_toolkit import __version__, format_summary


def main():
    sample = {"smoke test": True, "login test": False}
    print(f"qa_toolkit {__version__}")
    print(format_summary(sample))


if __name__ == "__main__":
    main()
```

Run:

```bash
python -m qa_toolkit
```

Output:

```
qa_toolkit 0.1.0
PASS  smoke test
FAIL  login test
1/2 passed
```

This is a neat way to give a package a command-line entry point, such as a "check my environment" tool, or a "run the data validator" utility.

### 7. Subpackages

As the library grows, group related modules into subpackages. Each subpackage folder also needs its own `__init__.py`.

```
qa_toolkit/
├── __init__.py
├── validators.py
├── formatters.py
├── data/
│   ├── __init__.py
│   ├── generators.py
│   └── loaders.py
└── api/
    ├── __init__.py
    └── checks.py
```

Importing across levels:

```python
from qa_toolkit.data.generators import make_user
from qa_toolkit.api import checks
import qa_toolkit.data.loaders as loaders
```

Inside `qa_toolkit/api/checks.py`, to reach a sibling at the top level:

```python
from qa_toolkit.validators import is_valid_email   # absolute (preferred)
from .. import validators                           # relative: go up one level
```

**Design tip:** do not nest too deeply. "Flat is better than nested" (from *The Zen of Python*; try `import this`). Two levels is plenty for most QE libraries. Group by **responsibility** (data, api, reporting), not by file type.

### 8. A Realistic QA Project Layout

Here is a professional layout you will begin using in Project 1. It separates the *importable library code* from tests, docs and configuration:

```
qe-foundations/                 <- repository root (Git repo)
├── README.md
├── .gitignore
├── requirements.txt            <- dependencies (see the pip lesson)
├── pyproject.toml              <- optional now; makes the project installable
├── src/
│   └── qa_toolkit/
│       ├── __init__.py
│       ├── validators.py
│       └── formatters.py
├── tests/
│   └── test_validators.py      <- unit tests (introduced Wednesday)
└── data/
    └── sample_users.csv
```

Why a `src/` folder? It is a widely recommended convention called the "src layout": because the package is not at the repository root, you cannot accidentally import it from the working directory without installing it. This ensures your tests exercise the same code that users will install. (A flat layout with `qa_toolkit/` directly at the root works for small learning projects and is what we use in the exercises; both are common.)

### 9. Making Your Package Installable (Basics)

So far you can import `qa_toolkit` only when you run Python from the folder that contains it. To use it from anywhere, in any project, you can **install** it into your environment. The modern, standard way is a `pyproject.toml` file at the project root. A minimal version (using the `setuptools` build tool):

```toml
[build-system]
requires = ["setuptools>=61"]
build-backend = "setuptools.build_meta"

[project]
name = "qa-toolkit"
version = "0.1.0"
description = "Small helpers for QA automation"
requires-python = ">=3.9"

[tool.setuptools.packages.find]
where = ["src"]
```

**Explanation:**

- `[build-system]` tells pip which tool builds the package.
- `[project]` holds metadata. Note the **distribution name** (`qa-toolkit`, used with `pip install`) can differ from the **import name** (`qa_toolkit`, used with `import`). Hyphens are allowed in distribution names; import names must be valid Python identifiers (underscores).
- `[tool.setuptools.packages.find]` with `where = ["src"]` tells setuptools to look for packages in the `src` folder.

Then, from the project root, with a **virtual environment active** (see the virtual environments lesson):

```bash
python -m pip install -e .
```

The `-e` means **editable** (also called development) mode: pip links to your source folder instead of copying it, so changes you make to the code are immediately visible with no reinstall. The `.` means "the project in the current directory". After this, `import qa_toolkit` works from any folder while that environment is active.

> You do not need to publish anything to a public index (PyPI) for any of this. Installing from a local folder is how teams share internal QA libraries: one repository holds the library; other projects install it with pip, or from a Git URL. Details of pip itself are in the next lessons, and building and publishing distributions is beyond what we need this week.

**Three words people mix up:**

| Word | Example | What it is |
|------|---------|-----------|
| Package (import package) | `qa_toolkit` | A folder you `import` |
| Distribution (installable package) | `qa-toolkit` 0.1.0 | The thing pip installs, built from your project, containing one or more import packages |
| Repository / project | `qe-foundations/` | The Git folder holding everything (code, tests, docs) |

### 10. Standard Files You Will Meet in Packages

| File / folder | Purpose |
|---------------|---------|
| `__init__.py` | Marks and initialises a package |
| `__main__.py` | Entry point for `python -m package` |
| `__pycache__/` | Compiled bytecode cache; auto-generated; do not commit |
| `*.egg-info/` or `*.dist-info/` | Metadata created when a package is installed/built; do not commit `egg-info` |
| `README.md` | Human documentation |
| `.gitignore` | Tells Git what not to track (`__pycache__/`, virtual env folders, etc.) |

A starter `.gitignore` for Python projects:

```
__pycache__/
*.pyc
.venv/
venv/
*.egg-info/
.pytest_cache/
```

### 11. Common Mistakes and Troubleshooting

| Problem | Likely cause | Fix |
|---------|-------------|-----|
| `ModuleNotFoundError: No module named 'qa_toolkit'` | Running from the wrong folder, or package not installed | `cd` to the folder containing `qa_toolkit/`, or `pip install -e .` |
| `ImportError: attempted relative import with no known parent package` | Running a package file directly as a script | Use `python -m package.module` |
| `ImportError: cannot import name 'x' from 'qa_toolkit'` | Name not defined or not re-exported in `__init__.py` | Import from the submodule or add it to `__init__.py` |
| Import works on your machine but not for a teammate | Missing `__init__.py` (some tools ignore namespace packages) or an unrecorded dependency | Add `__init__.py`; list dependencies in `requirements.txt` |
| Circular import between submodules | Two modules import each other | Move shared code to a third module |
| `qa-toolkit` import fails | Hyphen in import name | Folder name must use underscores |
| Package folder named like a stdlib module (`email/`, `test/`) | Shadowing | Rename |
| Code changes not visible after installing | Installed a copy, not editable | `pip install -e .` |

---

## Code Examples

### Example 1: Complete `qa_toolkit` package (copy, run, experiment)

Create this exact structure:

```
packages_lab/
├── qa_toolkit/
│   ├── __init__.py
│   ├── __main__.py
│   ├── validators.py
│   └── formatters.py
└── demo.py
```

`qa_toolkit/__init__.py`:

```python
"""qa_toolkit - small helpers for QA automation."""

from qa_toolkit.validators import is_valid_email, is_non_empty
from qa_toolkit.formatters import format_result, format_summary

__version__ = "0.1.0"
__all__ = ["is_valid_email", "is_non_empty", "format_result", "format_summary"]
```

`qa_toolkit/validators.py` and `qa_toolkit/formatters.py` as shown in section 2. Add this near the top of `formatters.py` to practise a relative import:

```python
from .validators import is_non_empty


def format_result(name, passed):
    """Return 'PASS  name' / 'FAIL  name'. Blank names are replaced."""
    label = name if is_non_empty(name) else "<unnamed test>"
    return f"{'PASS' if passed else 'FAIL'}  {label}"
```

(and keep `format_summary` unchanged below it.)

`demo.py`:

```python
import qa_toolkit

print(qa_toolkit.__version__)
print(qa_toolkit.format_result("   ", True))
print(qa_toolkit.format_summary({"a": True, "b": False}))
```

Output:

```
0.1.0
PASS  <unnamed test>
PASS  a
FAIL  b
1/2 passed
```

**Walk-through of the import chain when `demo.py` runs `import qa_toolkit`:**

1. Python finds the `qa_toolkit` folder and executes `__init__.py`.
2. The first line inside it imports `qa_toolkit.validators`, so `validators.py` runs and its functions are defined.
3. The second line imports `qa_toolkit.formatters`; *that* module in turn runs `from .validators import is_non_empty` and finds `validators` already cached in `sys.modules`; it is not executed a second time.
4. `__version__` and `__all__` are set. The package object is ready, with `is_valid_email` etc. as attributes.

### Example 2: Inspecting a package

```python
import qa_toolkit
import qa_toolkit.validators as v

print(qa_toolkit.__name__)     # qa_toolkit
print(qa_toolkit.__file__)     # .../qa_toolkit/__init__.py
print(qa_toolkit.__path__)     # list with the package folder; only packages have __path__
print(v.__name__)              # qa_toolkit.validators
print(v.__package__)           # qa_toolkit
```

`__path__` is the attribute that makes a module a package in Python's eyes: it is where Python looks for submodules.

### Example 3: Using `pkgutil` to list the modules in a package

```python
import pkgutil
import qa_toolkit

for info in pkgutil.iter_modules(qa_toolkit.__path__):
    print(info.name, "(package)" if info.ispkg else "(module)")
```

This prints each submodule name (for example `__main__`, `formatters`, `validators`), a handy trick when exploring an unfamiliar library.

### Example 4: Real-world scenario - sharing a library across two test projects

Your team has two repositories: `api-tests` and `ui-tests`. Both need the same `is_valid_email` and report formatting. Without packages, someone copies the files into both repos; a bug fix in one is forgotten in the other. With a package:

1. Move shared code into its own repo `qa-toolkit` with the layout above.
2. In each test repo's virtual environment, install it: `python -m pip install -e ../qa-toolkit` (local development) or later install a tagged release from Git.
3. Both repos now do `from qa_toolkit import is_valid_email`. A fix is made once and then picked up by both.

That is the story of nearly every internal QE framework: it starts as helper functions, grows into a package, and gets installed everywhere.

---

## Practice Questions and Mini-Exercises

**Q1.** In one or two sentences, explain the difference between a module and a package. What file traditionally marks a folder as a regular package?

**Q2.** Given the structure below, write three different valid import statements to get `make_user` into your code (from a script at the repository root).

```
shop_tests/
├── data/
│   ├── __init__.py
│   └── generators.py     # defines make_user()
└── run.py
```

**Q3.** Inside `qa_toolkit/api/checks.py`, write (a) an absolute import and (b) a relative import to use `is_valid_email` from `qa_toolkit/validators.py`.

**Q4.** You run `python qa_toolkit/formatters.py` and see `ImportError: attempted relative import with no known parent package`. Explain why and show the correct command.

**Q5.** What does `__all__` in `__init__.py` control? Does it prevent someone from importing a name that is not listed?

**Q6 (hands-on).** Build a package called `string_utils` with modules `case.py` (function `to_snake(text)` converting `"Login Page"` to `"login_page"`) and `clean.py` (function `squash(text)` collapsing repeated spaces). In `__init__.py`, re-export both functions. Write a script that imports from the package and prints the results. Add a `__main__.py` so that `python -m string_utils` prints a demonstration.

**Q7.** Why might a project use a `src/` directory? Name one benefit.

**Q8.** Explain the difference between `qa-toolkit` and `qa_toolkit`.

**Q9 (debugging).** A teammate's checkout of your repo fails with `ModuleNotFoundError: No module named 'qa_toolkit'` when running tests, although it works for you. List three things to check.

---

### Answers

**A1.** A module is a single `.py` file; a package is a directory of modules (and possibly subpackages) that is importable with dotted names. `__init__.py` marks it as a regular package.

**A2.**

```python
from data.generators import make_user
from data import generators          # then generators.make_user()
import data.generators                # then data.generators.make_user()
```

**A3.**

```python
# (a) absolute
from qa_toolkit.validators import is_valid_email
# (b) relative: .. goes from qa_toolkit.api up to qa_toolkit
from ..validators import is_valid_email
```

**A4.** Run directly, the file's `__name__` is `"__main__"` and Python has no idea it belongs to the package `qa_toolkit`, so the relative import has no parent to resolve against. Run it as a module from the folder that contains `qa_toolkit`: `python -m qa_toolkit.formatters`.

**A5.** `__all__` defines the names exported by `from package import *` and signals the public API. It does not prevent explicit imports: `from qa_toolkit.validators import something_unlisted` still works.

**A6.** One possible solution:

```
string_utils/
├── __init__.py
├── __main__.py
├── case.py
└── clean.py
```

```python
# case.py
def to_snake(text):
    return "_".join(text.strip().lower().split())
```

```python
# clean.py
def squash(text):
    return " ".join(text.split())
```

```python
# __init__.py
from string_utils.case import to_snake
from string_utils.clean import squash

__all__ = ["to_snake", "squash"]
```

```python
# __main__.py
from string_utils import to_snake, squash

print(to_snake("Login Page"))        # login_page
print(squash("too    many   spaces"))  # too many spaces
```

**A7.** The `src` layout prevents accidentally importing the in-repo code without installing it, so tests run against the installed package, and packaging mistakes (such as a missing file) show up early.

**A8.** `qa-toolkit` is the distribution name used with `pip install`; `qa_toolkit` is the import name (a valid Python identifier) used in `import` statements. They are often related but need not be identical.

**A9.** (1) Is the package installed in *their* active environment (`python -m pip list`)? They may need `pip install -e .`. (2) Are they running from the correct directory, with `qa_toolkit` visible on `sys.path`? (3) Is an `__init__.py` committed to Git (not ignored, not missing)? Also check that they activated the right virtual environment.

---

## Summary / Key Takeaways

- A **package** is a directory of modules, importable with dotted names that mirror the folder structure. Include an `__init__.py` in each package and subpackage.
- `__init__.py` runs on import; use it for documentation, `__version__`, and re-exporting a clean public API with `__all__`. Keep it lightweight.
- **Absolute imports** (`from qa_toolkit.validators import ...`) are the default; **relative imports** (`from .validators import ...`) work only inside a package.
- Run code inside a package with `python -m package.module`; add `__main__.py` to make a package runnable with `python -m package`.
- Keep layouts shallow and group by responsibility. A `src/` layout is a good professional habit.
- To use a package anywhere, make it installable with `pyproject.toml` and `pip install -e .` inside a virtual environment. Distribution names (`qa-toolkit`) and import names (`qa_toolkit`) can differ.
- Next lessons: how **pip** installs and manages packages, and how **virtual environments** keep each project's packages separate.

---

## Additional Resources

- Python Tutorial - Packages: https://docs.python.org/3/tutorial/modules.html#packages
- Python Packaging User Guide - Packaging Python Projects: https://packaging.python.org/en/latest/tutorials/packaging-projects/
- Python Reference - The import system (packages and relative imports): https://docs.python.org/3/reference/import.html#packages
