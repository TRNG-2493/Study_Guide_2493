# Creating and Importing Modules

## Learning Objectives

By the end of this lesson you will be able to:

- Explain what a Python module is and why splitting code into modules is a professional habit.
- Create your own module (a `.py` file) and import it from another file.
- Use the four main import styles (`import x`, `from x import y`, `import x as z`, `from x import *`) and know when each one is appropriate.
- Explain how Python finds modules (the module search path, `sys.path`) and why "ModuleNotFoundError" happens.
- Use the `if __name__ == "__main__":` guard so a file can be both a reusable module and a runnable script.
- Understand what happens when a module is imported (executed once, cached in `sys.modules`) and how to avoid circular imports.
- Document a module with a docstring and control its public surface with `__all__`.

---

## Why This Matters

This week's epic is about hardening your Python: modules, exceptions, files, debugging and unit testing, then SQL for data validation and collaborative Git. Everything else in the week assumes you can organise code across multiple files. Tomorrow you will build a data-loading module with error handling; Wednesday you will write unit tests that `import` the code they test; and your Project 1 (QE Foundations) capstone will be a multi-file project, not a single script.

Think about a real test automation framework. It is never one 5,000-line file. It has:

- a file that knows how to read test data,
- a file with helper functions for validating responses,
- a file that handles configuration,
- a file with the actual tests.

If everything lived in one file, then finding a bug, reusing a helper in a second project, or letting a teammate work on one part without colliding with you would all be painful. Modules solve that. A module is the smallest unit of code organisation in Python, and the very first tool a QE engineer uses to keep a growing automation suite maintainable.

A good analogy is a toolbox. A single messy drawer holding every screwdriver, nail and spanner works if you own five tools. When you own five hundred, you want labelled drawers: "electrical", "plumbing", "woodwork". Each Python module is one labelled drawer, and `import` is how you open the drawer you need.

---

## The Concept

### 1. What Is a Module?

**Definition.** A *module* is a single Python file (ending in `.py`) that contains Python definitions and statements: functions, classes, variables, and possibly some runnable code. The name of the module is the file name without the `.py`.

So a file called `validators.py` is a module called `validators`.

You have already been *using* modules. Every time you wrote `import math` or `import random`, you were loading a module someone else wrote. Today you learn to write your own.

**Why modules exist (the "why"):**

1. **Organisation.** Group related code together (all string validation in one place).
2. **Reuse.** Write a function once, import it everywhere. No copy-paste.
3. **Namespace separation.** Two modules can both define a function called `load()` without clashing, because each module is its own namespace (its own "box" of names). You call them as `csv_loader.load()` and `json_loader.load()`.
4. **Collaboration.** Different people can edit different files with fewer merge conflicts (a topic you will meet in Git on Wednesday).
5. **Testability.** Small, focused modules are far easier to unit test.

### 2. Creating Your First Module

Let us build a tiny utility for QA work. We will use the following project layout throughout this lesson. Create a new folder anywhere on your machine (say `modules_lab`) and put files inside it:

```
modules_lab/
├── validators.py
├── main.py
```

#### Step 1: Write the module

Create `validators.py`:

```python
"""validators.py - small helper functions for validating test data.

These helpers are used to check values that come back from an application
under test (for example an API response or a form field).
"""

MAX_USERNAME_LENGTH = 20


def is_valid_username(name):
    """Return True if name is a non-empty string of letters/digits/underscores
    that is not longer than MAX_USERNAME_LENGTH."""
    if not isinstance(name, str) or name == "":
        return False
    if len(name) > MAX_USERNAME_LENGTH:
        return False
    return name.replace("_", "").isalnum()


def is_valid_email(email):
    """A deliberately simple email check: one '@' with text on both sides and
    a '.' somewhere after the '@'. (Real-world email validation is harder.)"""
    if not isinstance(email, str) or email.count("@") != 1:
        return False
    local, domain = email.split("@")
    return bool(local) and "." in domain and not domain.startswith(".") and not domain.endswith(".")


def is_positive_int(value):
    """Return True only for real ints greater than zero (bool is excluded)."""
    return isinstance(value, int) and not isinstance(value, bool) and value > 0
```

**Line-by-line explanation:**

- The triple-quoted string at the very top is a **module docstring**. It must be the first statement in the file. Tools (and `help(validators)`) read it to describe the module.
- `MAX_USERNAME_LENGTH = 20` is a **module-level variable** (a constant by convention; Python does not enforce constants, but UPPER_CASE signals "do not change this").
- `def is_valid_username(name):` defines a function. The docstring right under it describes what it does.
- `isinstance(name, str)` checks the type. We check this first because calling `.replace` on `None` or a number would crash.
- `name.replace("_", "").isalnum()` removes underscores, then `isalnum()` is `True` if what remains is only letters and digits. So `"qa_user_1"` is valid, `"qa-user"` is not.
- In `is_valid_email`, `email.count("@") != 1` rejects strings with zero or several `@` symbols. `email.split("@")` then splits into exactly two parts, which we unpack into `local` and `domain`.
- `bool(local)` is `False` for an empty string, so `"@example.com"` fails.
- In `is_positive_int`, `isinstance(True, int)` is actually `True` in Python (because `bool` is a subclass of `int`), so we explicitly exclude booleans. This is a classic gotcha that matters in QA, when a JSON API returns `true` where you expected a number.

#### Step 2: Import and use the module

Create `main.py` in the **same folder**:

```python
import validators

print(validators.is_valid_username("qa_user_1"))   # True
print(validators.is_valid_username("qa-user"))     # False
print(validators.is_valid_email("tester@example.com"))  # True
print(validators.is_positive_int(5))               # True
print(validators.is_positive_int(True))            # False
print(validators.MAX_USERNAME_LENGTH)              # 20
```

Run it from inside the folder:

```bash
python main.py
```

Expected output:

```
True
False
True
True
False
20
```

**What happened?** When Python reached `import validators`, it:

1. Searched for something named `validators` (more on *where* shortly).
2. Found `validators.py` in the current folder.
3. Executed the whole file from top to bottom, creating the function objects and the constant.
4. Created a **module object** named `validators` and bound it to the name `validators` in `main.py`.

After that, `validators.is_valid_username` means "the name `is_valid_username` that lives inside the `validators` module namespace". The dot is how you reach inside a module.

> **Windows note:** On Windows you may need `py main.py` or `python main.py` depending on your install. On macOS/Linux you may need `python3 main.py`. This lesson writes `python`; use whichever works on your machine.

### 3. The Four Import Styles

Python gives you several ways to bring names in. They all do the same underlying work (load the module), but they differ in *which names appear in your file*.

#### Style 1: `import module`

```python
import validators
validators.is_valid_email("a@b.com")
```

- You bring in the module object only. You always prefix with the module name.
- **Pros:** It is always obvious where a function came from. No name clashes.
- **Cons:** Slightly more typing.
- **When to use:** The default choice. Prefer this when in doubt.

#### Style 2: `from module import name`

```python
from validators import is_valid_email, is_positive_int

is_valid_email("a@b.com")      # no prefix needed
is_positive_int(3)
```

- You bring in only the specific names you list, directly into your file's namespace.
- **Pros:** Shorter calls; clear list of what you depend on at the top of the file.
- **Cons:** If you import two functions with the same name from two modules, the second silently replaces the first. The origin of the name is less obvious while reading the code.
- **When to use:** When you use a few names repeatedly and the names are unambiguous.

You can wrap long import lists in parentheses:

```python
from validators import (
    is_valid_email,
    is_valid_username,
    is_positive_int,
)
```

#### Style 3: `import module as alias`

```python
import validators as v

v.is_valid_username("qa_user")
```

- Gives the module a shorter nickname.
- **When to use:** For long module names or well-known community conventions (for example `import numpy as np`, which you may see later). Do not invent cryptic aliases like `v` for your own project's modules, since readability is more important than saving keystrokes.

You can alias a single name too:

```python
from validators import is_valid_email as check_email
```

This is handy to resolve a name clash:

```python
from csv_loader import load as load_csv
from json_loader import load as load_json
```

#### Style 4: `from module import *` (avoid it)

```python
from validators import *
```

- Imports every public name from the module into your namespace.
- **Why it is discouraged:** You can no longer tell where a name came from, it can silently overwrite your own variables, and linters cannot warn you about undefined names. It makes code hard to debug.
- **When it is acceptable:** Interactive experiments in the Python shell, and rarely in `__init__.py` files (you will see this in the next lesson on packages).

#### Quick comparison

| Style | What lands in your namespace | Call looks like | Recommended? |
|-------|------------------------------|-----------------|--------------|
| `import validators` | `validators` | `validators.is_valid_email(x)` | Yes (default) |
| `from validators import is_valid_email` | `is_valid_email` | `is_valid_email(x)` | Yes, in moderation |
| `import validators as v` | `v` | `v.is_valid_email(x)` | For long names/conventions |
| `from validators import *` | every public name | `is_valid_email(x)` | Avoid |

#### PEP 8 import conventions

PEP 8 is the official Python style guide. For imports it says:

1. Put imports at the **top** of the file (after the module docstring).
2. Put each import on its own line (`import os` newline `import sys`, not `import os, sys`).
3. Group imports in this order, with a blank line between groups: (a) standard library, (b) third-party libraries (installed with pip, which you will learn this week), (c) your own project's modules.

```python
import json
import os

import requests          # third-party (installed via pip)

import validators        # your own module
```

### 4. How Python Finds Modules: `sys.path`

A very common beginner error is:

```
ModuleNotFoundError: No module named 'validators'
```

To understand it, you need to know how Python searches. When you write `import validators`, Python looks in this order:

1. **`sys.modules`**: a dictionary cache of modules already imported in this run. If it is there, Python reuses it.
2. **Built-in modules** compiled into the interpreter (like `sys`).
3. **Each folder listed in `sys.path`**, in order, looking for `validators.py` (or a package folder named `validators`).

`sys.path` is just a Python list of strings. You can print it:

```python
import sys

for entry in sys.path:
    print(entry)
```

Typical contents (yours will differ):

- The folder that contains the script you ran (the first entry; this is why `import validators` works when `main.py` and `validators.py` sit side by side).
- The standard library folder(s).
- The `site-packages` folder of the current Python or virtual environment (where `pip install` puts third-party code; you will study this in the pip and virtual environments lessons).
- Any folders listed in the `PYTHONPATH` environment variable.

**Why you get ModuleNotFoundError:**

| Cause | Fix |
|-------|-----|
| Typo in the module name (`validater`) | Fix the spelling; names are case-sensitive on Linux/macOS |
| The file is in a different folder not on `sys.path` | Move it, or run from the right folder, or organise as a package (next lesson) |
| It is a third-party library you have not installed | `pip install <name>` inside your active environment |
| You installed the library into a different Python than the one running your script | Use a virtual environment and check `python -m pip` / `which python` |
| The file name contains a hyphen or space (`my-validators.py`) | Use letters, digits and underscores only: `my_validators.py` |

You can add a folder temporarily at run time:

```python
import sys
sys.path.append("/path/to/my/shared/helpers")
import something_there
```

This works but is a **last resort**. In real projects you structure packages properly or install your code instead of editing `sys.path` by hand.

#### The shadowing trap

Never name your own file the same as a standard library or installed module. If you create `random.py` or `json.py` in your project folder, then `import random` will load *your* file (the script folder is first on `sys.path`), and standard code will break in confusing ways such as `AttributeError: module 'random' has no attribute 'randint'`. Likewise avoid `test.py`, `email.py`, `csv.py`, `logging.py`, and `types.py`.

### 5. Importing Runs the Module (Once)

Importing is not just "making names available"; it **executes the module's top-level code**. Create `noisy.py`:

```python
print("noisy.py is being executed")

def hello():
    return "hello"
```

And `use_noisy.py`:

```python
import noisy
import noisy      # second import: nothing printed

print(noisy.hello())
```

Output:

```
noisy.py is being executed
hello
```

The message appears **once**, not twice. After the first import, Python stores the module object in the `sys.modules` dictionary. Later `import noisy` statements (anywhere in the program) simply fetch the cached object. You can prove it:

```python
import sys
import noisy

print("noisy" in sys.modules)   # True
```

**Consequences for you as a QE:**

- Any module-level state (a list, a counter, an open connection) is **shared** by every file that imports that module. This is useful (a single shared configuration) but can cause bugs in tests if one test changes shared state and another test is unknowingly affected.
- Do not put slow or side-effecting code (calling an API, deleting files, connecting to a database) at the top level of a module. Put it inside functions that are only called deliberately. Otherwise just importing your helper triggers it.

If you edit a module while a Python session is running, the new code is not picked up automatically. In an interactive session you can force a reload:

```python
import importlib
import validators
importlib.reload(validators)
```

(In normal scripts you simply re-run the program.)

### 6. The `if __name__ == "__main__":` Guard

This is one of the most useful and most confusing idioms for beginners, so let us walk through it slowly.

Every module has a built-in variable called `__name__`.

- When a file is **imported**, `__name__` is set to the module's name (for example `"validators"`).
- When a file is **run directly** (`python validators.py`), `__name__` is set to the special string `"__main__"`.

Add this to the bottom of `validators.py`:

```python
if __name__ == "__main__":
    # This block only runs when you do:  python validators.py
    print("Running quick self-check...")
    assert is_valid_username("qa_user_1") is True
    assert is_valid_username("") is False
    assert is_valid_email("a@b.com") is True
    assert is_valid_email("nope") is False
    assert is_positive_int(1) is True
    assert is_positive_int(0) is False
    print("All checks passed.")
```

Now:

- `python validators.py` prints `Running quick self-check...` and `All checks passed.`
- `import validators` from `main.py` does **not** run that block. Only the definitions are loaded.

You can see the mechanism with a tiny experiment, `whoami.py`:

```python
print("My __name__ is:", __name__)
```

```bash
python whoami.py          # My __name__ is: __main__
python -c "import whoami" # My __name__ is: whoami
```

**Why it matters:** the same file can act as a *library* (importable without side effects) and as a *program* (runnable from the command line). The professional pattern is to wrap script behaviour in a `main()` function:

```python
def main():
    print("Doing the real work")


if __name__ == "__main__":
    main()
```

Test frameworks (including `unittest` and `pytest` that you will meet later) import your modules to test them. If your module ran its whole workflow on import, tests would trigger it every time. The guard prevents that.

> **Aside - `assert`:** We used `assert` above as a quick check: `assert condition` does nothing when the condition is true and raises `AssertionError` when false. We cover assertions properly on Tuesday; for now treat it as "shout if this is not true".

### 7. Inspecting a Module

Python gives you tools to look inside a module, useful when exploring unfamiliar code:

```python
import validators

print(validators.__name__)     # validators
print(validators.__file__)     # full path to validators.py
print(validators.__doc__)      # the module docstring
print(dir(validators))         # list of names defined in the module
help(validators)               # formatted documentation
```

`dir(validators)` returns a list that includes your three functions, `MAX_USERNAME_LENGTH`, and several built-in "dunder" (double-underscore) names such as `__name__` and `__file__`.

### 8. Controlling What Is Public: Naming Conventions and `__all__`

Python has no true "private" keyword, but there are conventions:

- A name starting with a single underscore, like `_normalise`, means "internal helper; do not rely on it from outside".
- `from module import *` skips names that start with an underscore.

You can be explicit with a list called `__all__`, which defines the module's public API, which is exactly the set of names that `from module import *` will import:

```python
__all__ = ["is_valid_username", "is_valid_email", "is_positive_int"]

def _strip(text):
    return text.strip()
```

Even with `__all__`, `validators._strip(...)` still works; `__all__` only affects star-imports and signals intent to readers and documentation tools.

### 9. Circular Imports (and How to Avoid Them)

A **circular import** happens when module A imports module B and module B imports module A.

`a.py`:

```python
import b

def func_a():
    return "A"
```

`b.py`:

```python
import a

def func_b():
    return a.func_a() + "B"
```

Often this seems to work with `import x` style, but with `from a import func_a` style at the top of both files you get an error such as:

```
ImportError: cannot import name 'func_a' from partially initialized module 'a' (most likely due to a circular import)
```

Why? Python starts executing `a.py`, hits `import b`, pauses `a`, starts executing `b.py`, which tries to get something from `a` that has not been defined yet (because `a` is paused halfway).

**How to fix or avoid:**

1. **Redesign.** The best fix. If A and B need each other, the shared piece probably belongs in a third module C that both import (A -> C <- B).
2. Import inside the function that needs it (a local import) as a short-term workaround.
3. Use `import module` rather than `from module import name` where possible, since attribute lookups happen later at call time.

Rule of thumb: keep dependencies flowing in **one direction**, e.g. `tests -> framework helpers -> utilities`. Utilities should never import tests.

### 10. Real-World QA Scenario: Splitting a Script into Modules

Imagine you inherit a single script, `smoke_check.py`, which does four things in one 300-line file: reads a config, builds test users, validates responses, and prints a report. Here is a miniature version:

```python
# smoke_check.py  (before - everything in one file)
BASE_URL = "https://staging.example.com"
TIMEOUT = 5

def build_user(i):
    return {"username": f"qa_user_{i}", "email": f"qa_user_{i}@example.com"}

def is_valid_email(email):
    return email.count("@") == 1 and "." in email.split("@")[1]

def report(results):
    for name, ok in results.items():
        print(f"{'PASS' if ok else 'FAIL'}: {name}")

users = [build_user(i) for i in range(3)]
results = {u["username"]: is_valid_email(u["email"]) for u in users}
report(results)
```

Refactor into modules, each with a single responsibility:

```
smoke_project/
├── config.py       # BASE_URL, TIMEOUT
├── users.py        # build_user
├── validators.py   # is_valid_email
├── reporting.py    # report
└── smoke_check.py  # imports the above and runs the flow
```

`smoke_check.py` after refactoring:

```python
from users import build_user
from validators import is_valid_email
from reporting import report


def main():
    users = [build_user(i) for i in range(3)]
    results = {u["username"]: is_valid_email(u["email"]) for u in users}
    report(results)


if __name__ == "__main__":
    main()
```

Benefits you can feel immediately: a change in how reports are printed touches only `reporting.py`; `validators.py` can be unit tested without running the whole smoke check; another project can copy `validators.py` (and next lesson, share it as a package).

On Monday's demo and exercise you will do exactly this kind of split and then turn it into a package.

### 11. Common Mistakes and How to Fix Them

| Mistake | Symptom | Fix |
|---------|---------|-----|
| Naming a file after a standard module (`random.py`) | Strange `AttributeError`s | Rename your file; delete stale `__pycache__` folder |
| Using `from x import *` everywhere | Unknown names, overwritten variables | Import explicit names |
| Running code at import time | Slow tests, side effects | Move into functions, guard with `__main__` |
| Circular imports | `ImportError ... partially initialized module` | Move shared code to a third module |
| Running a script from the wrong folder | `ModuleNotFoundError` | `cd` into the project root, or use packages |
| File named with hyphen (`my-module.py`) | `SyntaxError` on import | Use underscores |
| Editing a module in an interactive session and expecting auto-update | Old behaviour persists | Restart or `importlib.reload` |

**About `__pycache__`:** after you import a module, you will notice a folder named `__pycache__` appear containing `.pyc` files. These are compiled bytecode caches that make later imports faster. They are safe to delete and should be listed in `.gitignore` (so you never commit them to Git).

---

## Code Examples

### Example 1: A complete, runnable mini-project

Create a folder `qa_demo` with these two files.

`qa_demo/test_data.py`:

```python
"""test_data.py - generates predictable test data."""

import random

DEFAULT_DOMAIN = "example.com"


def make_username(index):
    """Return a predictable username such as 'qa_user_3'."""
    return f"qa_user_{index}"


def make_email(index, domain=DEFAULT_DOMAIN):
    """Return an email address for the given index."""
    return f"{make_username(index)}@{domain}"


def random_age(minimum=18, maximum=65, seed=None):
    """Return a random age; pass a seed for repeatable results."""
    rng = random.Random(seed)
    return rng.randint(minimum, maximum)


if __name__ == "__main__":
    print(make_username(1), make_email(1), random_age(seed=42))
```

`qa_demo/run_demo.py`:

```python
import test_data
from test_data import make_email as email_for


def main():
    print(test_data.make_username(7))        # qa_user_7
    print(email_for(7))                      # qa_user_7@example.com
    print(email_for(7, domain="qa.test"))    # qa_user_7@qa.test
    print(test_data.random_age(seed=1) == test_data.random_age(seed=1))  # True


if __name__ == "__main__":
    main()
```

Run `python run_demo.py`. The last line prints `True` because using the same seed produces the same number every time, which is exactly the kind of repeatability test data needs.

**Notes on the code:**

- `random.Random(seed)` creates its own random-number generator object so that seeded results do not interfere with other code (more on `random` in the built-in modules lesson).
- `domain=DEFAULT_DOMAIN` is a **default argument** that uses the module-level constant. Callers can override it.
- Naming the module `test_data.py` is fine here, but note that many test runners treat files beginning with `test_` as test files. Later in the week when you learn about testing, you will want helper modules to have names that do not begin with `test_`, e.g. `data_factory.py`. (A good habit to adopt early.)

### Example 2: Seeing `sys.modules` and `__name__` in action

```python
import sys
import validators

print(validators.__name__)           # validators
print("validators" in sys.modules)   # True
print(sys.modules["validators"] is validators)   # True: same object
```

### Example 3: Resolving a name clash with aliases

```python
from csv import reader as csv_reader      # standard library csv module
from json import load as json_load        # standard library json module

# Both are clearly named; neither hides the other.
print(csv_reader, json_load)
```

(You will use `csv` and `json` heavily tomorrow.)

---

## Practice Questions and Mini-Exercises

Try each one yourself before looking at the answers at the bottom.

**Q1 (concept).** What is the difference between a *module* and a *script*? Can one file be both?

**Q2 (predict the output).** Given `greet.py`:

```python
print("loading greet")

def hello():
    return "hi"

if __name__ == "__main__":
    print("running directly")
```

and `app.py`:

```python
import greet
import greet
print(greet.hello())
```

What does `python app.py` print? What does `python greet.py` print?

**Q3 (fix the bug).** A teammate named their helper file `random.py` and now `import random; random.randint(1, 5)` crashes. Why? How do you fix it?

**Q4 (write code).** Create a module `string_tools.py` with a function `slugify(text)` that lowercases text, strips whitespace and replaces spaces with hyphens. Add a `__main__` guard that prints `slugify("  Login Page Test ")`. Then import and use it from another file with both `import string_tools` and `from string_tools import slugify`.

**Q5 (choose the style).** Which import style would you choose in each case, and why?
(a) You need one function once, from a module with a very long name.
(b) You use two modules that both define `load()`.
(c) You are typing in the interactive shell to explore.

**Q6 (debug).** `ModuleNotFoundError: No module named 'helpers'` occurs when running `python tests/run_tests.py`, but `helpers.py` is in the project root. Give two possible fixes. (Hint: think about what `sys.path[0]` is.)

**Q7 (design).** Module `a.py` has `from b import f` and module `b.py` has `from a import g`. Explain the failure and propose a redesign.

**Q8 (challenge).** Add `__all__` to `string_tools.py` containing only `slugify`, and a private helper `_collapse_spaces`. Show how `from string_tools import *` behaves.

---

### Answers

**A1.** A *module* is any `.py` file considered as something to import; a *script* is a file you run directly. One file can be both: use the `if __name__ == "__main__":` guard so the same file is importable without side effects and runnable from the command line.

**A2.** `python app.py` prints `loading greet` once (second import uses the cache), then `hi`. `python greet.py` prints `loading greet` and `running directly`.

**A3.** The script's own folder is first on `sys.path`, so `import random` finds the local `random.py` instead of the standard library one, which has no `randint`. Rename the file (for example `random_helpers.py`) and delete the `__pycache__` folder (stale compiled file).

**A4.** One solution:

```python
# string_tools.py
def slugify(text):
    """Turn 'Login Page Test' into 'login-page-test'."""
    return "-".join(text.strip().lower().split())


if __name__ == "__main__":
    print(slugify("  Login Page Test "))   # login-page-test
```

`"-".join(text.strip().lower().split())` also collapses multiple spaces, because `split()` with no argument splits on any run of whitespace. Using it:

```python
import string_tools
print(string_tools.slugify("A B"))

from string_tools import slugify
print(slugify("A B"))
```

**A5.** (a) `from long_module_name import the_function` (or `import long_module_name as lmn`). (b) `import csv_loader` and `import json_loader` and call `csv_loader.load()` / `json_loader.load()`, or alias with `as`. (c) `from module import *` is tolerable in the shell for convenience, but plain `import` is still fine.

**A6.** When you run `python tests/run_tests.py`, `sys.path[0]` is the `tests` folder, not the project root, so `helpers` is not found. Fixes: run it as a module from the root with `python -m tests.run_tests` (requires `tests` to be importable as a package; see the next lesson); move `helpers.py` next to the script; or (last resort) append the root folder to `sys.path`; or (best in the long term) make the code an installable package.

**A7.** When `a` is run, it begins importing `b`, which immediately tries to import `g` from `a` before `a` has finished, so `g` does not exist yet and an `ImportError` occurs. Redesign: move shared code (`f`, `g` or whatever they both need) into a third module `c.py` and have both import from it.

**A8.**

```python
__all__ = ["slugify"]

def _collapse_spaces(text):
    return " ".join(text.split())

def slugify(text):
    return _collapse_spaces(text).lower().replace(" ", "-")
```

`from string_tools import *` brings in only `slugify`. `string_tools._collapse_spaces` still works if accessed with the module prefix.

---

## Summary / Key Takeaways

- A **module** is a `.py` file; the module name is the file name without `.py`. Modules give you organisation, reuse, namespaces, collaboration and testability.
- Import with `import module` (default), `from module import name` (for a few unambiguous names), or `import module as alias`. Avoid `from module import *`.
- Python finds modules via `sys.modules` (cache), built-ins, then each entry in `sys.path`. `ModuleNotFoundError` means the name was not found on that path.
- Never name your files after standard library modules.
- Importing **executes** the module once; the result is cached in `sys.modules` and shared.
- Use `if __name__ == "__main__":` so a file can be both importable and runnable; keep top-level code free of side effects.
- Use docstrings, underscore-prefixed helper names and `__all__` to communicate a module's public interface.
- Avoid circular imports by keeping dependencies one-directional and extracting shared code into another module.
- Next lesson: **Python packages**, which are folders of modules.

---

## Additional Resources

- Python Tutorial - Modules: https://docs.python.org/3/tutorial/modules.html
- The Python Language Reference - The import system: https://docs.python.org/3/reference/import.html
- PEP 8 - Style Guide for Python Code (Imports section): https://peps.python.org/pep-0008/#imports
