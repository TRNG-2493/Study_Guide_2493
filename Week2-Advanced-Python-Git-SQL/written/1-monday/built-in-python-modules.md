# Built-in Python Modules

## Learning Objectives

By the end of this lesson you will be able to:

- Explain what the Python **standard library** is ("batteries included") and how to explore it.
- Use the `os` module to work with the file system, paths and environment variables.
- Use `pathlib` as a modern, object-oriented alternative for paths.
- Use the `sys` module for command-line arguments, exit codes, the module search path and platform information.
- Use the `datetime` module to create, format, parse and calculate with dates, times and durations.
- Use the `random` module to generate repeatable and non-repeatable test data.
- Use a few other everyday helpers (`time`, `math`, `platform`) and know where to look for others.
- Apply these modules to realistic QA tasks: test data generation, timestamped report names, environment-aware configuration and timing checks.

---

## Why This Matters

Everything in the previous lessons (modules, packages, pip, virtual environments) is about *bringing code into your project*. This lesson is about the code you already have, **for free**, the moment Python is installed: the **standard library**. No `pip install`, no versions to pin, no extra dependency to maintain, and it runs on every machine that has Python.

For a QE engineer these modules are everyday tools:

- `os` and `pathlib` locate test data files, create output folders and read environment variables such as the target environment (`STAGING` or `QA`).
- `sys` reads command-line arguments and sets the exit code that tells a CI pipeline whether your script passed.
- `datetime` stamps reports, checks token expiry and validates date fields returned by an application.
- `random` generates varied but reproducible test inputs.

This supports this week's epic (hardening your Python and starting the QE Foundations capstone): in Project 1 you will use several of these in your utility library. Tomorrow's lessons (file reading/writing, CSV/JSON/XML) build directly on `os`/`pathlib`, and Wednesday's debugging and logging lessons rely on `sys` and `datetime` concepts you meet here.

An analogy: the standard library is the **toolkit that comes inside the box** when you buy a piece of furniture: basic screwdriver, Allen key, a few screws. You can build a lot with it before buying anything extra from the hardware store (PyPI).

---

## The Concept

### 1. The Standard Library: "Batteries Included"

Python's **standard library** is a large collection of modules installed with Python itself. Examples you will see during this course:

| Area | Modules |
|------|---------|
| Operating system and files | `os`, `pathlib`, `shutil`, `tempfile`, `glob` |
| Python runtime | `sys`, `platform`, `importlib` |
| Dates and time | `datetime`, `time`, `zoneinfo`, `calendar` |
| Randomness and math | `random`, `math`, `statistics`, `secrets` |
| Data formats | `json`, `csv`, `xml.etree.ElementTree`, `sqlite3` |
| Text | `re`, `string`, `textwrap` |
| Collections and functional tools | `collections`, `itertools`, `functools` |
| Command line | `argparse`, `subprocess` |
| Diagnostics and testing | `logging`, `unittest`, `pdb`, `timeit` |
| Networking | `urllib`, `http`, `socket` |

Several of these (file handling, `json`/`csv`/`xml`, `logging`, `unittest`, `pdb`) are scheduled for the coming days; we will cover them in depth when we get there. Today's focus is **`os`, `sys`, `datetime` and `random`**, with short looks at `pathlib`, `time`, `math` and `platform`.

#### How to explore a module

You do not have to memorise anything. Python can document itself:

```python
import math

print(dir(math))            # list of names inside the module
help(math.ceil)             # documentation for one function
print(math.__doc__)         # module docstring
```

Or in the terminal: `python -m pydoc math` (documentation) or `python -m pydoc -k keyword` (search). The official reference is at docs.python.org/3/library/ (linked at the end).

#### Is it a standard module or a third-party one?

```python
import sys
print(sorted(sys.stdlib_module_names)[:10])   # Python 3.10+ : names of all standard modules
```

If `import something` works on a fresh Python with no pip installs, it is part of the standard library.

---

### 2. The `os` Module: Talking to the Operating System

`os` ("operating system") provides portable access to operating-system features: the current directory, files and folders, environment variables, and so on. "Portable" means the same code runs on Windows, macOS and Linux (which use different path separators and conventions).

```python
import os
```

#### 2.1 Working directory and listing files

```python
print(os.getcwd())            # current working directory (where the script was RUN from)
print(os.listdir("."))        # names of entries in the current directory (a list of strings)
```

- `os.getcwd()` returns the **current working directory**, the folder Python considers "here" for relative paths. Important: it is where you *ran* Python from, not necessarily where the script file lives. Many "FileNotFoundError" bugs come from forgetting this difference.
- `os.listdir(path)` returns names only (not full paths) and in arbitrary order; use `sorted(...)` when you need stable output.
- `os.chdir(path)` changes the working directory. Use it sparingly; it affects the whole program.

#### 2.2 Building paths safely with `os.path`

Never join paths with `+ "/" +`: Windows uses `\` and others use `/`. `os.path.join` picks the right separator:

```python
import os

path = os.path.join("data", "users", "users.csv")
print(path)    # data/users/users.csv  (on Windows: data\users\users.csv)
```

Other useful `os.path` helpers:

```python
import os

p = "/projects/qe/data/report.final.html"
print(os.path.basename(p))        # report.final.html   (the file name)
print(os.path.dirname(p))         # /projects/qe/data   (the folder)
print(os.path.splitext(p))        # ('/projects/qe/data/report.final', '.html')
print(os.path.exists("nothing.txt"))   # False
print(os.path.isfile("main.py"))       # True if it is an existing file
print(os.path.isdir("data"))           # True if it is an existing directory
print(os.path.abspath("data"))         # full path based on the working directory
print(os.path.getsize("main.py"))      # size in bytes (raises an error if missing)
```

`splitext` splits at the **last** dot: `report.final.html` becomes `report.final` and `.html`.

#### 2.3 Creating, renaming and deleting

```python
import os

os.makedirs("output/reports", exist_ok=True)    # creates all missing folders; no error if it already exists
os.rename("old_name.txt", "new_name.txt")        # rename or move a file
os.remove("temp.txt")                            # delete a FILE (error if missing)
os.rmdir("empty_folder")                         # delete an EMPTY folder
```

- `os.makedirs(path, exist_ok=True)` is the idiom for "make sure this folder exists". Without `exist_ok=True` it raises `FileExistsError` if the folder is already there. `os.mkdir` creates just one level.
- Deleting is **permanent**. There is no recycle bin. To delete a folder with contents use `shutil.rmtree` from the `shutil` module, and be extremely careful with the path you pass.

#### 2.4 Walking through a folder tree

```python
import os

for folder, subfolders, files in os.walk("tests"):
    for name in files:
        if name.endswith(".py"):
            print(os.path.join(folder, name))
```

`os.walk` visits every folder below the starting point, yielding a 3-tuple each time: the current folder path, a list of its subfolder names, and a list of its file names. This is the classic tool for "find all test files" or "find every `.json` fixture".

#### 2.5 Environment variables

An **environment variable** is a named value stored by the operating system and inherited by the programs you start. They are the standard way to configure a program *without changing its code*, for example to select the target environment or supply a secret.

```python
import os

home = os.environ.get("HOME")                      # returns None if not set
env_name = os.environ.get("TEST_ENV", "qa")        # second argument = default value
print(env_name)

os.environ["TEST_ENV"] = "staging"                 # set it for this program (and child processes) only
print(os.getenv("TEST_ENV"))                       # os.getenv(name, default) is a shortcut for environ.get
```

- `os.environ` behaves like a dictionary of strings (always strings, so convert numbers yourself: `int(os.environ.get("TIMEOUT", "30"))`).
- Prefer `.get(name, default)` over `os.environ[name]`: the square-bracket form raises `KeyError` if the variable is missing.
- Changes made with `os.environ[...] = ...` affect only your running program, not your terminal.

Setting a variable for a single run from the terminal:

```bash
# macOS/Linux/Git Bash
TEST_ENV=staging python run_tests.py

# Windows PowerShell
$env:TEST_ENV = "staging"; python run_tests.py
```

**QA scenario:** your test suite reads `BASE_URL` from the environment; the CI server sets it to the staging URL, while on your laptop it defaults to a local one. The same code, no edits. And secrets such as passwords stay out of Git (see the virtual environments lesson).

#### 2.6 Other handy `os` items

```python
import os

print(os.name)        # 'posix' (macOS/Linux) or 'nt' (Windows)
print(os.sep)         # path separator: '/' or '\\'
print(os.linesep)     # line ending used by the platform
print(os.cpu_count()) # number of CPUs (may be None)
print(os.getpid())    # this process's ID
```

---

### 3. `pathlib`: A Modern Way to Work with Paths

`os.path` works with plain strings. The newer **`pathlib`** module represents paths as **objects** with methods and a friendly `/` operator. Many teams prefer it for new code.

```python
from pathlib import Path

base = Path("data")
users = base / "users" / "users.csv"      # '/' joins path parts
print(users)                  # data/users/users.csv
print(users.name)             # users.csv
print(users.stem)             # users
print(users.suffix)           # .csv
print(users.parent)           # data/users
print(users.exists())         # False unless it exists
print(Path.cwd())             # current working directory
print(Path(__file__).resolve().parent)   # the folder that contains THIS script
```

The last line is a very useful idiom: `__file__` is the path of the current script (a module attribute you met earlier); `.resolve()` makes it absolute and `.parent` is its folder. Using it makes your code find data files **relative to the script** instead of relative to wherever you ran Python from.

More operations:

```python
from pathlib import Path

out = Path("output") / "reports"
out.mkdir(parents=True, exist_ok=True)         # like os.makedirs(..., exist_ok=True)

for csv_file in sorted(Path("data").glob("*.csv")):   # pattern matching
    print(csv_file.name)

for py_file in Path("tests").rglob("*.py"):           # recursive search
    print(py_file)

report = out / "summary.txt"
report.write_text("0 failures\n", encoding="utf-8")   # quick write (we cover files in depth tomorrow)
print(report.read_text(encoding="utf-8"))
```

**`os.path` vs `pathlib`:** both are fine. `pathlib` reads more naturally; `os` is widely used in older code, so you must be able to read both. Choose one style per project.

---

### 4. The `sys` Module: Talking to the Python Interpreter

Where `os` talks to the operating system, **`sys`** talks to the Python interpreter itself.

```python
import sys
```

#### 4.1 Command-line arguments: `sys.argv`

`sys.argv` is a list of strings: the script name followed by the arguments typed on the command line.

```python
# args_demo.py
import sys

print(sys.argv)
if len(sys.argv) > 1:
    print("First argument:", sys.argv[1])
else:
    print("No arguments given")
```

```bash
python args_demo.py smoke --verbose
```

Output:

```
['args_demo.py', 'smoke', '--verbose']
First argument: smoke
```

`sys.argv[0]` is the script name; real arguments start at index 1. All values are strings. For anything more than two or three simple arguments, the standard library's `argparse` module provides help text, validation and flags; you can explore it from the documentation when needed.

#### 4.2 Exit codes: `sys.exit`

When a program ends, it reports a numeric **exit code** to the operating system: `0` means success and any non-zero value means failure. CI systems (and shell scripts using `&&`) rely on this.

```python
import sys

def main():
    failures = 2
    if failures:
        print(f"{failures} checks failed")
        return 1
    print("All checks passed")
    return 0

if __name__ == "__main__":
    sys.exit(main())
```

After running, check the code: `echo $?` on macOS/Linux, `echo %ERRORLEVEL%` in Windows cmd, or `$LASTEXITCODE` in PowerShell. Here it would be `1`.

`sys.exit("some message")` prints the message to standard error and exits with code 1.

#### 4.3 Standard streams

```python
import sys

print("normal output")                       # goes to sys.stdout
print("something went wrong", file=sys.stderr)   # goes to sys.stderr
```

`stdout` (normal output) and `stderr` (errors/diagnostics) are separate channels, so a CI system or a user can redirect one without the other (`python script.py > out.txt` captures only stdout).

#### 4.4 Interpreter and platform information

```python
import sys

print(sys.version)             # full version string
print(sys.version_info)        # named tuple: major, minor, micro, ...
print(sys.version_info >= (3, 9))   # True/False - compare versions with tuples
print(sys.platform)            # 'win32', 'linux', 'darwin' (macOS)
print(sys.executable)          # which Python is running
```

A QA use: skip or adapt a check depending on the platform:

```python
if sys.platform == "win32":
    browser_path = r"C:\Program Files\Browser\browser.exe"
else:
    browser_path = "/usr/bin/browser"
```

(The `r"..."` prefix makes a **raw string** so backslashes are not treated as escape characters.)

#### 4.5 `sys.path` and `sys.modules`

As covered in the first lesson of today, `sys.path` is the list of folders Python searches for imports and `sys.modules` caches imported modules.

---

### 5. The `datetime` Module: Dates, Times and Durations

Testing is full of time: report timestamps, "created at" fields, session expiry, scheduling features, date filters. Python's `datetime` module handles them.

```python
import datetime
```

(You will also often see `from datetime import datetime, date, timedelta`. Be careful: the module is called `datetime` *and* contains a class called `datetime`. Writing `import datetime as dt` avoids confusion, and we will use that.)

```python
import datetime as dt
```

#### 5.1 The main classes

| Class | Represents | Example |
|-------|------------|---------|
| `dt.date` | A calendar date (year, month, day) | `dt.date(2025, 3, 14)` |
| `dt.time` | A time of day | `dt.time(9, 30)` |
| `dt.datetime` | Date and time together | `dt.datetime(2025, 3, 14, 9, 30, 15)` |
| `dt.timedelta` | A **duration** (difference between two points in time) | `dt.timedelta(days=30, hours=2)` |
| `dt.timezone` | A fixed UTC offset | `dt.timezone.utc` |

#### 5.2 Creating values

```python
import datetime as dt

d = dt.date(2025, 3, 14)
print(d)                      # 2025-03-14
print(d.year, d.month, d.day) # 2025 3 14
print(d.weekday())            # 4  (Monday = 0 ... Sunday = 6, so 4 = Friday)
print(d.isoformat())          # 2025-03-14

t = dt.datetime(2025, 3, 14, 9, 30, 15)
print(t)                      # 2025-03-14 09:30:15
print(t.hour, t.minute, t.second)

today = dt.date.today()               # today's date
now = dt.datetime.now()               # current local date and time
utc_now = dt.datetime.now(dt.timezone.utc)   # current time in UTC (timezone-aware)
```

#### 5.3 Formatting: `strftime` (value to text)

`strftime` ("string format time") turns a date/time into text using **format codes**:

| Code | Meaning | Example |
|------|---------|---------|
| `%Y` | 4-digit year | 2025 |
| `%m` | Month number (01-12) | 03 |
| `%d` | Day of month (01-31) | 14 |
| `%H` | Hour, 24-hour clock (00-23) | 09 |
| `%M` | Minute | 30 |
| `%S` | Second | 15 |
| `%A` | Weekday name | Friday |
| `%B` | Month name | March |
| `%b` | Short month name | Mar |
| `%y` | 2-digit year | 25 |
| `%p` | AM/PM (locale dependent) | AM |

```python
t = dt.datetime(2025, 3, 14, 9, 30, 15)
print(t.strftime("%Y-%m-%d %H:%M:%S"))   # 2025-03-14 09:30:15
print(t.strftime("%d/%m/%Y"))            # 14/03/2025
print(t.strftime("%A, %B %d"))           # Friday, March 14
print(t.strftime("report_%Y%m%d_%H%M%S.html"))   # report_20250314_093015.html
```

The last line shows the most common QE use: **timestamped file names** so each test run's report gets a unique, sortable name (year first so alphabetical order equals chronological order).

#### 5.4 Parsing: `strptime` and `fromisoformat` (text to value)

```python
parsed = dt.datetime.strptime("2025-03-14 09:30", "%Y-%m-%d %H:%M")
print(parsed)                         # 2025-03-14 09:30:00

iso = dt.datetime.fromisoformat("2025-03-14T09:30:15")
print(iso)                            # 2025-03-14 09:30:15
```

- `strptime` ("string parse time") needs a format string that matches the text *exactly*; otherwise it raises `ValueError`.
- `fromisoformat` reads ISO 8601 text (`YYYY-MM-DDTHH:MM:SS`), the style used by most web APIs. Newer Python versions accept more ISO variants than older ones (for example a trailing `Z`); if you need to support older versions, normalise the text first.

**QA use:** an API returns `"created_at": "2025-03-14T09:30:15"`. You parse it, and assert that it is within the last minute, rather than comparing brittle strings.

#### 5.5 Arithmetic with `timedelta`

```python
t = dt.datetime(2025, 3, 14, 9, 30, 15)

later = t + dt.timedelta(days=30, hours=2)
print(later)                          # 2025-04-13 11:30:15

diff = dt.date(2025, 12, 25) - dt.date(2025, 3, 14)
print(diff)                           # 286 days, 0:00:00
print(diff.days)                      # 286

print(dt.timedelta(hours=1, minutes=30).total_seconds())   # 5400.0
```

Subtracting two dates/datetimes gives a `timedelta`. Adding or subtracting a `timedelta` to a date/datetime gives a new date/datetime. Note that `dt.timedelta` supports `days`, `seconds`, `microseconds`, `milliseconds`, `minutes`, `hours` and `weeks`, but **not** months or years (those have varying lengths).

#### 5.6 Comparing and replacing

```python
a = dt.datetime(2025, 3, 14, 9, 0)
b = dt.datetime(2025, 3, 14, 17, 0)
print(a < b)                           # True; datetimes are comparable
print(b - a)                           # 8:00:00
print(b.replace(hour=0, minute=0))     # 2025-03-14 00:00:00  (replace returns a NEW object)
```

Date/time objects are **immutable**: `replace` and arithmetic create new objects rather than changing the original.

#### 5.7 Time zones: a note of caution

A **naive** datetime has no timezone information (`datetime.now()` returns local time without saying so). An **aware** datetime knows its offset. Comparing or subtracting a naive and an aware datetime raises `TypeError`.

Practical rules for test automation:

1. Store and compare timestamps in **UTC** (`dt.datetime.now(dt.timezone.utc)`) whenever you can; convert to local time only for display.
2. Know whether the system under test returns naive or aware timestamps before you compare them.
3. For named time zones (such as `America/New_York`) with daylight saving, use the standard `zoneinfo` module (Python 3.9+; on Windows it may need the `tzdata` package installed with pip).
4. Be careful with tests that run near midnight or across daylight-saving changes: they can fail only on certain days. This is a classic source of "flaky" tests.

---

### 6. The `random` Module: Generating Varied (and Repeatable) Data

`random` produces **pseudo-random** numbers: values that look random but come from a deterministic algorithm. That determinism is actually a gift for testing: if you start the generator from the same **seed**, you get the same sequence every time.

```python
import random
```

#### 6.1 The core functions

```python
random.random()               # float from 0.0 up to (not including) 1.0
random.uniform(1.5, 4.5)      # float between the two numbers
random.randint(1, 6)          # integer from 1 to 6, BOTH ends included
random.randrange(0, 10, 2)    # like range(): 0,2,4,6,8 (end excluded)
random.choice(["chrome", "firefox", "edge"])    # one random item from a sequence
random.choices(["PASS", "FAIL"], weights=[90, 10], k=5)  # k picks WITH replacement, optionally weighted
random.sample(range(1, 11), 3)     # 3 DIFFERENT items (no repeats) from a population
items = [1, 2, 3, 4, 5]
random.shuffle(items)         # shuffles the list IN PLACE (returns None)
```

Easy mistakes to avoid:

- `randint(a, b)` includes `b`; `randrange(a, b)` does not.
- `shuffle` changes the list you give it and returns `None`; `sample` returns a new list.
- `choice` on an empty sequence raises `IndexError`.

#### 6.2 Seeds: making random data repeatable

```python
import random

random.seed(42)
print(random.randint(1, 100), random.randint(1, 100))   # 82 15

random.seed(42)                                         # reset to the same starting point
print(random.randint(1, 100), random.randint(1, 100))   # 82 15 again
```

With the same seed, the same calls produce the same values. (These specific numbers are what current Python 3 releases produce; the exact numbers are not guaranteed to be identical across very different Python versions, so do not hard-code expected values in tests that depend on a seed from a different version.)

**Why seeds matter for QE:**

- A test that uses random data and fails once in a hundred runs is useless if you cannot reproduce the failure. Good practice: **generate a seed at the start of the run, print/log it, and allow passing it in** so any failing run can be replayed exactly.
- Tests that must be deterministic (most of them) should use a fixed seed.

#### 6.3 A private generator: `random.Random`

The module-level functions share one global generator, so separate parts of your code can disturb each other's sequences. Create independent generators when this matters:

```python
import random

rng = random.Random(123)
print(rng.randint(1, 100))      # same methods as the module-level functions
```

(You met this in the first lesson of today.)

#### 6.4 Not for security

`random` is **not** secure. Never use it for passwords, tokens or anything an attacker should not guess. The standard library has a separate `secrets` module for that. For *test data* it is exactly right.

---

### 7. A Few More Standard Modules Worth Knowing Today

#### `time`

```python
import time

start = time.perf_counter()        # high-resolution timer for measuring durations
time.sleep(0.2)                    # pause for 0.2 seconds
elapsed = time.perf_counter() - start
print(f"Took {elapsed:.2f} seconds")     # Took 0.20 seconds
print(time.time())                 # seconds since the 'epoch' (1 Jan 1970 UTC), as a float
```

Use `perf_counter()` for measuring how long something takes (for example a response-time check), not `datetime.now()` subtraction. Use `time.sleep` carefully in tests: fixed sleeps make suites slow and flaky; polling with a timeout is usually better (you will see this idea in later automation topics).

#### `math`

```python
import math

print(math.ceil(2.1), math.floor(2.9))   # 3 2
print(math.sqrt(16))                     # 4.0
print(0.1 + 0.2 == 0.3)                  # False! floating-point rounding
print(math.isclose(0.1 + 0.2, 0.3))      # True  - the right way to compare floats
```

This last pair matters a great deal in testing: never compare floating-point results with `==`; use `math.isclose` (or a tolerance).

#### `platform`

```python
import platform

print(platform.system())      # 'Windows', 'Linux' or 'Darwin'
print(platform.python_version())
```

A clean way to log which operating system and Python a test run used.

#### `shutil`, `glob`, `tempfile` (awareness)

- `shutil.copy`, `shutil.copytree`, `shutil.rmtree`, `shutil.move` copy, move and delete files/folders.
- `glob.glob("data/*.json")` finds files by pattern.
- `tempfile.TemporaryDirectory()` creates a throwaway folder deleted automatically, which is excellent for tests that write files.

We will use files heavily from tomorrow.

---

## Code Examples

### Example 1: Timestamped report folder (`os`/`pathlib` + `datetime`)

```python
"""make_report_dir.py - create a unique, timestamped folder for test artefacts."""

import datetime as dt
from pathlib import Path


def make_report_dir(base="reports"):
    """Create and return a Path like reports/run_20250314_093015."""
    stamp = dt.datetime.now().strftime("%Y%m%d_%H%M%S")
    folder = Path(base) / f"run_{stamp}"
    folder.mkdir(parents=True, exist_ok=True)
    return folder


if __name__ == "__main__":
    folder = make_report_dir()
    print("Created:", folder)
    (folder / "summary.txt").write_text("0 failures\n", encoding="utf-8")
    print("Files in folder:", [p.name for p in folder.iterdir()])
```

**Explanation:**

- `dt.datetime.now().strftime(...)` builds a sortable timestamp such as `20250314_093015`.
- `Path(base) / f"run_{stamp}"` joins path parts safely for any operating system.
- `folder.mkdir(parents=True, exist_ok=True)` creates intermediate folders (`parents=True`) and does not fail if the folder exists.
- `write_text` creates a small file inside; `iterdir()` lists folder contents as `Path` objects, and the list comprehension extracts each `.name`.
- The function **returns** the folder so callers can put artefacts into it, and the `__main__` guard (lesson 1) keeps the demo from running on import.

### Example 2: Reproducible random test users (`random`)

```python
"""random_users.py - generate reproducible random test users."""

import random

FIRST_NAMES = ["Asha", "Ben", "Carla", "Dev", "Elena", "Farid"]
ROLES = ["viewer", "editor", "admin"]


def make_users(count, seed=None):
    """Return a list of user dictionaries.

    Passing the same seed always returns the same users."""
    rng = random.Random(seed)
    users = []
    for i in range(1, count + 1):
        name = rng.choice(FIRST_NAMES)
        users.append({
            "id": i,
            "name": name,
            "email": f"{name.lower()}{i}@example.com",
            "age": rng.randint(18, 65),
            "role": rng.choices(ROLES, weights=[70, 25, 5])[0],
        })
    return users


if __name__ == "__main__":
    first = make_users(3, seed=2025)
    second = make_users(3, seed=2025)
    for user in first:
        print(user)
    print("Same seed gives same data:", first == second)
```

**Explanation:**

- A private `random.Random(seed)` generator keeps this function from disturbing any other random use in the program.
- `rng.choices(ROLES, weights=[70, 25, 5])[0]` makes `viewer` most likely and `admin` rare, like a realistic user population. `choices` returns a *list*, so we take element `[0]`.
- The email includes the index so every address is unique, a common requirement for test accounts.
- The final comparison prints `True`: lists of dictionaries compare equal when their contents are equal. When `seed=None`, results differ per run.

### Example 3: Checking a timestamp returned by an application (`datetime`)

```python
"""check_timestamp.py - verify that a 'created_at' value is recent."""

import datetime as dt


def is_recent(created_at_text, max_age_seconds=60, now=None):
    """True if the ISO timestamp is no more than max_age_seconds old
    (and not in the future)."""
    now = now or dt.datetime.now(dt.timezone.utc)
    created = dt.datetime.fromisoformat(created_at_text)
    if created.tzinfo is None:                 # naive -> assume it is UTC
        created = created.replace(tzinfo=dt.timezone.utc)
    age = now - created
    return dt.timedelta(0) <= age <= dt.timedelta(seconds=max_age_seconds)


if __name__ == "__main__":
    fixed_now = dt.datetime(2025, 3, 14, 9, 31, 0, tzinfo=dt.timezone.utc)
    print(is_recent("2025-03-14T09:30:30", now=fixed_now))   # True  (30 s old)
    print(is_recent("2025-03-14T09:20:00", now=fixed_now))   # False (11 min old)
    print(is_recent("2025-03-14T09:45:00", now=fixed_now))   # False (in the future)
```

**Explanation:**

- The `now` parameter lets a test **inject a fixed "current time"**, which makes the function deterministic and testable (you will see why when you learn unit testing on Wednesday).
- `created.replace(tzinfo=dt.timezone.utc)` converts a naive datetime into an aware one (by assuming UTC) so that subtracting works without `TypeError`.
- `dt.timedelta(0) <= age <= dt.timedelta(seconds=max_age_seconds)` is a **chained comparison**: true only if the age is between zero and the maximum.

### Example 4: Environment-aware configuration and exit code (`os` + `sys`)

```python
"""config_check.py - read configuration from the environment and exit properly."""

import os
import sys

REQUIRED = ["BASE_URL"]


def main():
    base_url = os.environ.get("BASE_URL")
    timeout = int(os.environ.get("TIMEOUT", "30"))
    env_name = os.environ.get("TEST_ENV", "qa")

    missing = [name for name in REQUIRED if not os.environ.get(name)]
    if missing:
        print(f"Missing environment variables: {', '.join(missing)}", file=sys.stderr)
        return 1

    print(f"Running against {env_name}: {base_url} (timeout {timeout}s)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
```

Try it:

```bash
python config_check.py                                  # error message, exit code 1
BASE_URL=https://qa.example.com python config_check.py  # works (macOS/Linux/Git Bash)
```

**Explanation:** missing configuration is reported on `stderr` and returned as exit code `1`, so a CI pipeline marks the step as failed. `', '.join(missing)` formats the list nicely. Note that `int(...)` will raise `ValueError` if `TIMEOUT` is not numeric; handling such errors is the topic of tomorrow's exception lessons.

### Example 5: Timing a check (`time`)

```python
import time

def timed(label, func, *args):
    start = time.perf_counter()
    result = func(*args)
    elapsed = time.perf_counter() - start
    print(f"{label}: {elapsed * 1000:.1f} ms")
    return result

total = timed("sum of squares", lambda n: sum(i * i for i in range(n)), 1_000_000)
print(total)
```

`*args` collects any extra positional arguments and passes them on to `func`. Multiplying by 1000 converts seconds to milliseconds; `:.1f` formats with one decimal place. Numbers like `1_000_000` use underscores purely for readability.

---

## Practice Questions and Mini-Exercises

**Q1.** What is the Python standard library? Name three standard modules and one thing each is used for.

**Q2.** Why should you use `os.path.join("data", "x.csv")` rather than `"data" + "/" + "x.csv"`?

**Q3.** What is the difference between `os.makedirs("a/b", exist_ok=True)` and `os.mkdir("a/b")`?

**Q4.** Write code that prints the full path of every `.json` file under a folder called `fixtures`, including subfolders. Give one version with `os.walk` and one with `pathlib`.

**Q5.** Your script is run as `python check.py staging 5`. What are `sys.argv[0]`, `sys.argv[1]` and `sys.argv[2]`, and what type is `sys.argv[2]`? How would you use it as a number?

**Q6.** What does `sys.exit(2)` do and why would a CI system care?

**Q7.** Given `t = datetime.datetime(2025, 1, 31, 23, 59, 0)`, write expressions for (a) the timestamp text `20250131_235900`, (b) the datetime 90 minutes later, (c) whether `t` falls on a weekend.

**Q8.** What happens with `dt.datetime.strptime("14-03-2025", "%Y-%m-%d")`? Fix it.

**Q9.** Why is `random.seed(...)` valuable for a QE engineer? What would you log at the start of a randomised test run?

**Q10.** Predict which lines raise errors: (a) `random.randint(5, 1)` (b) `random.choice([])` (c) `random.sample([1, 2], 3)` (d) `random.shuffle((1, 2, 3))`.

**Q11 (hands-on).** Write `password_policy_data.py` containing a function `random_usernames(count, seed)` that returns `count` unique usernames of the form `qa_<4 random digits>` (use `random.Random(seed)` and a set to guarantee uniqueness). Print them for seed 10 twice to show repeatability.

**Q12 (challenge).** Write `days_until.py` that takes a date in `YYYY-MM-DD` form from `sys.argv[1]`, prints how many days remain until then (or "That date has passed"), and exits with code 2 and an error message on `stderr` if no argument or an invalid date is given. (You may use `try/except ValueError` for the invalid date: it simply means "if parsing fails, do this".)

---

### Answers

**A1.** The standard library is the set of modules shipped with Python (no installation needed). Examples: `os` (file system and environment), `datetime` (dates and times), `random` (random test data), `sys` (interpreter details and exit codes), and others.

**A2.** `os.path.join` uses the correct separator for the operating system (`\` on Windows, `/` elsewhere) and avoids doubled or missing separators, so the code is portable.

**A3.** `makedirs` creates all missing intermediate folders (`a` and `a/b`), and with `exist_ok=True` does not fail if the folder already exists. `mkdir` creates only the last level (it fails if `a` does not exist) and raises `FileExistsError` if `a/b` already exists.

**A4.**

```python
# os.walk version
import os
for folder, _subfolders, files in os.walk("fixtures"):
    for name in files:
        if name.endswith(".json"):
            print(os.path.abspath(os.path.join(folder, name)))

# pathlib version
from pathlib import Path
for path in Path("fixtures").rglob("*.json"):
    print(path.resolve())
```

**A5.** `sys.argv[0]` is `"check.py"`, `sys.argv[1]` is `"staging"`, `sys.argv[2]` is `"5"`, a **string**. Convert with `int(sys.argv[2])`.

**A6.** It ends the program with exit code 2. CI systems and shell scripts treat any non-zero code as failure, so the pipeline step is marked failed (and subsequent steps can be skipped); zero means success.

**A7.**

```python
import datetime as dt
t = dt.datetime(2025, 1, 31, 23, 59, 0)
print(t.strftime("%Y%m%d_%H%M%S"))              # (a) 20250131_235900
print(t + dt.timedelta(minutes=90))              # (b) 2025-02-01 01:29:00
print(t.weekday() >= 5)                          # (c) 31 Jan 2025 is a Friday (weekday 4) -> False
```

**A8.** It raises `ValueError` because the text is day-month-year but the format expects year-month-day. Fix the format to match: `strptime("14-03-2025", "%d-%m-%Y")`.

**A9.** Seeds make random sequences repeatable, so a failing randomised run can be reproduced exactly. Log the seed (and ideally the Python/OS versions) at the start of each run, and support passing the seed in to replay a failure.

**A10.** (a) raises `ValueError` (empty range: the low value is bigger than the high one). (b) raises `IndexError`. (c) raises `ValueError` (sample larger than population). (d) raises `TypeError` (tuples are immutable, so they cannot be shuffled in place).

**A11.**

```python
import random

def random_usernames(count, seed=None):
    rng = random.Random(seed)
    names = set()
    while len(names) < count:
        names.add(f"qa_{rng.randint(0, 9999):04d}")
    return sorted(names)

print(random_usernames(5, seed=10))
print(random_usernames(5, seed=10))   # identical to the line above
```

`:04d` pads the number with leading zeros to four digits. Using a `set` ignores duplicates, and the `while` loop keeps going until enough unique names exist (so `count` must not exceed 10,000).

**A12.**

```python
import datetime as dt
import sys


def main():
    if len(sys.argv) != 2:
        print("Usage: python days_until.py YYYY-MM-DD", file=sys.stderr)
        return 2
    try:
        target = dt.date.fromisoformat(sys.argv[1])
    except ValueError:
        print(f"Invalid date: {sys.argv[1]!r}", file=sys.stderr)
        return 2
    days = (target - dt.date.today()).days
    if days < 0:
        print("That date has passed")
    else:
        print(f"{days} days remaining")
    return 0


if __name__ == "__main__":
    sys.exit(main())
```

---

## Summary / Key Takeaways

- The **standard library** ships with Python: no pip needed, no version to pin. Explore it with `dir()`, `help()` and the official docs.
- **`os`** and **`pathlib`** handle paths, folders, files and environment variables portably. Build paths with `os.path.join` or `/`; create folders with `makedirs`/`mkdir(..., exist_ok=True)`; read configuration with `os.environ.get(name, default)`.
- **`sys`** gives you command-line arguments (`sys.argv`), exit codes (`sys.exit`), standard streams, version and platform data, plus `sys.path`/`sys.modules`.
- **`datetime`** provides `date`, `datetime`, `timedelta` and `timezone`. Format with `strftime`, parse with `strptime`/`fromisoformat`, calculate with `timedelta`. Prefer UTC and be wary of naive vs aware datetimes.
- **`random`** produces pseudo-random data; **seeding** makes it repeatable, which is vital for reproducing test failures. It is not for security.
- Handy extras: `time.perf_counter` for timing, `math.isclose` for float comparison, `platform` for OS details.
- Next lesson: **Collaborative Git workflow (fetch, pull and push)**, where you will move the code you have just organised into a shared repository.

---

## Additional Resources

- The Python Standard Library (index of all modules): https://docs.python.org/3/library/
- `datetime` module reference: https://docs.python.org/3/library/datetime.html
- `os` module reference: https://docs.python.org/3/library/os.html
