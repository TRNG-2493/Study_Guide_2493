# Writing Reusable Utility Functions

## Learning Objectives

By the end of this lesson you will be able to:

- Explain what a utility function is and what makes a function genuinely reusable.
- Apply design principles: single responsibility, clear names, no hidden dependencies, return instead of print.
- Organise related functions into a **module** (a `.py` file) and import them from another file.
- Use `if __name__ == "__main__":` so a file can be both a library and a script.
- Write a small **utility library** for test automation containing validators, data generators, formatters and a timing decorator.
- Generate random but **reproducible** test data with the `random` module and a seed.
- Check your own functions quickly using `assert` statements.
- Collaborate effectively on a shared codebase using **pair programming** (driver/navigator) and Git.

---

## Why This Matters

Everything you learned today comes together here. The goal of a test engineer is not just to write one script that works, but to build **tools that other people can use**. Imagine your team's test suite needs to:

- generate a unique test user for every run,
- validate that an ID looks right before using it,
- convert 125 seconds into `2m 5s` for a report,
- time every slow helper function.

If each engineer writes their own version of these helpers in each test file, you get duplicated code, inconsistent behaviour and bugs fixed in one place but not in another. A shared, well-designed **utility library** solves this: write it once, test it once, import it everywhere.

Today's exercise is **pair programming**: you and a partner will build a reusable test-utility library with validators, data generators and a timing decorator. This lesson gives you the design principles, the structure and the working practices to do it well.

---

## The Concept

### 1. What Is a Utility Function?

A **utility function** (or *helper*) is a small, general-purpose function that does one useful job and doesn't depend on a particular program. Typical examples:

- `is_valid_email(text)`
- `format_duration(seconds)`
- `generate_username()`
- `percent(part, whole)`
- `clean_text(text)`

Utility functions are the "screwdrivers and spanners" of a project: simple tools used everywhere.

---

### 2. Principles of Good, Reusable Functions

#### 2.1 One function, one job (single responsibility)

A function should do **one thing**, and its name should say what that is. If you describe it with the word "and", it's probably two functions.

```python
# Does too much: validates AND prints AND formats
def process(test_id):
    ...

# Better: separate jobs that can be reused and tested independently
def is_valid_test_id(test_id): ...
def format_test_id(number): ...
def print_test_id(test_id): ...
```

#### 2.2 Clear, descriptive names

- Use **verbs** for actions: `generate_username`, `format_duration`, `calculate_pass_rate`.
- Use **`is_` / `has_` / `can_`** for functions returning booleans: `is_valid_email`.
- Avoid vague names (`do_stuff`, `helper`, `process`, `data`) and cryptic abbreviations.

#### 2.3 Return values; don't print them

Return the result and let the caller decide what to do with it. A function that `print`s can only serve the console; one that `return`s can feed a report, a file, a comparison or another function.

```python
# Hard to reuse
def format_duration(seconds):
    print(f"{seconds // 60}m {seconds % 60}s")

# Reusable
def format_duration(seconds):
    return f"{seconds // 60}m {seconds % 60}s"
```

#### 2.4 Depend on parameters, not on hidden state

A reusable function gets everything it needs through its **parameters** and gives results through its **return value**. Avoid reading or changing global variables inside it. The same inputs should give the same outputs, which is what makes behaviour predictable and testable. (Functions like that are called **pure**.)

```python
THRESHOLD = 90                       # global

def passes(rate):                    # hidden dependency on THRESHOLD
    return rate >= THRESHOLD

def passes(rate, threshold=90):      # dependency is visible and adjustable
    return rate >= threshold
```

#### 2.5 Don't change the caller's data unexpectedly

Prefer returning a new list or dictionary instead of modifying the one passed in (see the earlier lesson on mutable arguments). If a function *does* modify its input, say so in its name and docstring.

#### 2.6 Sensible defaults and keyword options

Make the common call short and the unusual call possible: `generate_username(prefix="user", length=6)`. Use `None` for optional mutable defaults and keyword-only parameters for flags.

#### 2.7 Document with a docstring and type hints

Say what it does, what the parameters mean, what it returns, and any special cases.

```python
def percent(part: float, whole: float) -> float:
    """Return part as a percentage of whole.

    Returns 0.0 when whole is 0 to avoid division by zero.
    """
    if whole == 0:
        return 0.0
    return part / whole * 100
```

#### 2.8 Handle edge cases deliberately

Ask "what could go wrong?" for each function: empty input, zero, negative numbers, extra spaces, upper/lower case. Decide on a behaviour and document it. For a tester, thinking about edge cases is second nature; apply the same eye to your own functions.

#### 2.9 Keep them small

If a function exceeds about 20 lines, check whether it can be split. Small functions are easier to name, test and reuse.

---

### 3. Organising Utilities in a Module

When you have several related functions, put them in their own file, a **module**. You used modules on Wednesday (`collections`); now you can create your own.

Suppose your project folder looks like this:

```text
test-utils/
├── test_utils.py        <- the library: your reusable functions
├── demo.py              <- a script that uses the library
└── README.md
```

Inside `test_utils.py`:

```python
"""Reusable helper functions for test automation."""

def percent(part, whole):
    """Return part as a percentage of whole (0.0 if whole is 0)."""
    if whole == 0:
        return 0.0
    return part / whole * 100

def format_duration(seconds):
    """Return a duration in seconds as text such as '2m 5s'."""
    minutes, secs = divmod(int(seconds), 60)
    return f"{minutes}m {secs}s"
```

(`divmod(a, b)` returns the pair `(a // b, a % b)`, the whole-number quotient and the remainder, in one call, and we unpack them.)

The text at the very top is a **module docstring**, describing the file.

In `demo.py`, bring the functions in with `import`:

```python
import test_utils

print(test_utils.percent(22, 25))             # 88.0
print(test_utils.format_duration(125))        # 2m 5s
```

or import only what you need:

```python
from test_utils import percent, format_duration

print(percent(22, 25))
print(format_duration(125))
```

or import everything under a short alias:

```python
import test_utils as tu

print(tu.percent(1, 4))
```

**Important rules:**

- The two files must be in the **same folder** (or the module must be on Python's search path). Run the script from that folder.
- The file name (without `.py`) is the module name: `test_utils.py` is imported as `test_utils`. Use lowercase with underscores, no spaces or hyphens.
- **Don't name your module after a standard-library module** (`random.py`, `time.py`, `collections.py`), or you'll shadow it and cause confusing errors.
- Avoid `from module import *`: it hides where names come from.

When a module is imported for the first time, Python runs it from top to bottom, and creates a `__pycache__` folder with compiled versions. That folder is exactly the type of file you ignore with `.gitignore`.

---

### 4. `if __name__ == "__main__":` Explained

Every Python file has a built-in variable `__name__`.

- When you **run** a file directly (`python test_utils.py`), `__name__` is the text `"__main__"`.
- When the file is **imported** by another file, `__name__` is the module's name (`"test_utils"`).

So this block runs only when the file is executed directly, not when it is imported:

```python
def percent(part, whole):
    ...

if __name__ == "__main__":
    # quick self-check, or a demo, which won't run on import
    print(percent(1, 4))       # 25.0
```

This lets one file serve two purposes: **a library** (when imported) and **a script** (when run). It also stops demo code from executing every time someone imports your module. You will see this idiom in nearly every Python project, which is why we introduced `main()` earlier today:

```python
def main():
    print("Running demo")
    print(percent(22, 25))

if __name__ == "__main__":
    main()
```

---

### 5. Building a Test-Utility Library

Let's build the kind of library you will create in the exercise. We'll write it in four groups: **validators**, **data generators**, **formatters** and **decorators**.

#### 5.1 Validators: "Is this acceptable?"

Validators take a value and return `True` or `False`.

```python
def is_valid_test_id(test_id, prefix="TC", digits=3):
    """Return True for IDs like 'TC-007'."""
    expected_start = f"{prefix}-"
    if not test_id.startswith(expected_start):
        return False
    number_part = test_id[len(expected_start):]
    return number_part.isdigit() and len(number_part) == digits

def is_valid_email(email):
    """Return True if email looks like name@domain.tld (simple check)."""
    if email.count("@") != 1:
        return False
    name, domain = email.split("@")
    if not name or "." not in domain:
        return False
    return not domain.startswith(".") and not domain.endswith(".")

def is_in_range(value, low, high):
    """Return True if low <= value <= high."""
    return low <= value <= high

def is_valid_status_code(code):
    """Return True for HTTP status codes from 100 to 599."""
    return is_in_range(code, 100, 599)
```

Notice that `is_valid_status_code` **reuses** `is_in_range`: small functions combine into bigger ones. (Real-world email validation is much more complicated; this is a deliberately simple teaching version. Say so in the docstring.)

Edge cases to consider: `"TC-007 "` with a trailing space, an empty string `""`, uppercase/lowercase prefix. Decide: should `"tc-007"` be valid? Whatever you choose, document it and make it consistent.

#### 5.2 Data generators: "Give me some test data"

Tests need data: usernames, emails, IDs, passwords. The standard library's **`random`** module generates it.

```python
import random
import string

def generate_username(prefix="user", length=4):
    """Return a username like 'user4821'."""
    digits = "".join(random.choice(string.digits) for _ in range(length))
    return f"{prefix}{digits}"

def generate_email(domain="example.com", username=None):
    """Return a test email address."""
    if username is None:
        username = generate_username()
    return f"{username}@{domain}"

def generate_password(length=12):
    """Return a random password with letters and digits."""
    characters = string.ascii_letters + string.digits
    return "".join(random.choice(characters) for _ in range(length))

def generate_test_id(number, prefix="TC", digits=3):
    """Return an ID like 'TC-007' from a number."""
    return f"{prefix}-{number:0{digits}d}"
```

Useful pieces:

| Tool | What it does |
|---|---|
| `random.randint(a, b)` | Random whole number from `a` to `b` **inclusive** |
| `random.choice(sequence)` | One random item |
| `random.sample(sequence, k)` | `k` unique random items |
| `random.shuffle(list)` | Shuffle a list **in place** |
| `random.random()` | Random float from 0.0 up to 1.0 |
| `string.ascii_letters`, `string.digits` | Handy character collections |

(The `"".join(... for _ in range(length))` construct is a generator expression, a compact loop inside the brackets that you'll study in a later lesson. It repeats `random.choice(...)` `length` times and joins the results into one string.)

**Security note:** `random` is fine for *test* data but is **not secure** for real passwords. Never use these generated passwords for anything real.

**Reproducible randomness with a seed.** A test that uses random data can fail "sometimes" and be impossible to reproduce. A **seed** makes the "random" sequence repeatable:

```python
import random

random.seed(42)
print(random.randint(1, 100), random.randint(1, 100))    # same two numbers every run

random.seed(42)
print(random.randint(1, 100), random.randint(1, 100))    # identical to the line above
```

Good practice: when a test fails with random data, you need to be able to rerun with the **same data**. Log the seed you used, or let the caller pass one in:

```python
def generate_usernames(count, seed=None):
    """Return `count` usernames; pass a seed for repeatable output."""
    rng = random.Random(seed)             # a private random generator
    return [f"user{rng.randint(1000, 9999)}" for _ in range(count)]

print(generate_usernames(3, seed=7))      # always the same three
```

`random.Random(seed)` creates a separate generator object so your function doesn't interfere with the global one. Using a seeded generator is a professional habit worth building early.

#### 5.3 Formatters: "Make it readable"

```python
def format_duration(seconds):
    """Return a duration as text: 45 -> '45s', 125 -> '2m 5s', 3725 -> '1h 2m 5s'."""
    seconds = int(seconds)
    hours, remainder = divmod(seconds, 3600)
    minutes, secs = divmod(remainder, 60)
    if hours:
        return f"{hours}h {minutes}m {secs}s"
    if minutes:
        return f"{minutes}m {secs}s"
    return f"{secs}s"

def format_result_line(test_id, status, seconds):
    """Return one aligned report line."""
    return f"{test_id:<10}{status:<6}{format_duration(seconds):>8}"

def clean_text(text):
    """Return text stripped and with repeated spaces collapsed to one."""
    return " ".join(text.split())

def percent(part, whole):
    """Return part as a percentage of whole (0.0 if whole is 0)."""
    if whole == 0:
        return 0.0
    return part / whole * 100
```

Check mentally: `format_duration(3725)`: `divmod(3725, 3600)` gives `(1, 125)`; `divmod(125, 60)` gives `(2, 5)`; so `"1h 2m 5s"`. `"  hello   world ".split()` gives `['hello', 'world']`, which `" ".join` turns into `"hello world"`.

#### 5.4 Decorators: reusable behaviour

Include the timing decorator from the previous lesson:

```python
import time
from functools import wraps

def timer(func):
    """Decorator: print how long the function takes."""
    @wraps(func)
    def wrapper(*args, **kwargs):
        start = time.perf_counter()
        result = func(*args, **kwargs)
        elapsed = time.perf_counter() - start
        print(f"[timer] {func.__name__} took {elapsed:.4f}s")
        return result
    return wrapper
```

Anyone on the team can now write `from test_utils import timer` and add `@timer` above a slow function.

---

### 6. Checking Your Functions with `assert`

How do you know your utilities work? **Test them.** (You are, after all, becoming test engineers.) A quick way, before you meet testing frameworks, is the **`assert`** statement:

```python
assert condition
assert condition, "message shown if it fails"
```

If the condition is `True`, nothing happens. If it's `False`, Python raises an **`AssertionError`** and stops, showing your message.

```python
assert percent(1, 4) == 25.0
assert percent(0, 0) == 0.0
assert format_duration(125) == "2m 5s"
assert is_valid_test_id("TC-007")
assert not is_valid_test_id("TC-7"), "short numbers must be rejected"
```

Run silently = everything passes. Change one expected value to see a failure:

```text
AssertionError: short numbers must be rejected
```

A tidy way to organise this is a checking function in the same module, run only when the file is executed directly:

```python
def run_self_checks():
    """Run quick assertions on the utilities in this file."""
    assert percent(1, 4) == 25.0
    assert percent(0, 0) == 0.0
    assert format_duration(45) == "45s"
    assert format_duration(125) == "2m 5s"
    assert format_duration(3725) == "1h 2m 5s"
    assert is_valid_test_id("TC-007")
    assert not is_valid_test_id("TC-7")
    assert not is_valid_test_id("XX-007")
    assert not is_valid_test_id("")
    assert is_valid_email("a@b.com")
    assert not is_valid_email("a@@b.com")
    assert not is_valid_email("ab.com")
    print("All self-checks passed")

if __name__ == "__main__":
    run_self_checks()
```

Think like a tester when choosing the cases: the normal case, the **boundaries** (0, the highest and lowest valid values), **invalid** inputs and **empty** inputs. Professional testing frameworks (introduced later in the program) build on this same idea with better reporting, but the habit of writing checks alongside the code starts now.

**Tip:** when you find a bug, add an `assert` that captures it *before* you fix it, so it can never return silently.

---

### 7. Documenting the Library

A library nobody understands is not reusable. Provide:

1. **A module docstring** at the top of each file.
2. **A docstring and type hints for every function.**
3. **A README.md** in the project with: what the library is, how to import it, a short example of each function and how to run the self-checks.

A short README section might look like this:

````markdown
# test-utils

Reusable helpers for test automation.

## Usage

```python
from test_utils import is_valid_test_id, generate_username, timer

print(is_valid_test_id("TC-007"))   # True
print(generate_username())          # user4821
```

## Run the self-checks

    python test_utils.py
````

---

### 8. Working as a Pair

Today's exercise is **pair programming**: two people, one shared project. It is a common professional practice, and it works best when you follow the roles.

| Role | Responsibility |
|---|---|
| **Driver** | Has the keyboard. Writes the code, thinks about the *immediate* line or function. |
| **Navigator** | Reviews each line as it's typed, thinks about the *bigger picture*: design, edge cases, naming, what to do next, and looks things up. |

**Rules for the exercise:**

- **Swap roles every 30 minutes.** Use a timer. Swap even if you are "in the middle of something"; this keeps both people engaged.
- The navigator **speaks in intentions** ("let's add a function that checks the prefix") rather than dictating characters.
- The driver asks questions and says what they're doing out loud.
- Disagree politely, and try the suggestion before dismissing it; the code settles arguments.
- Both people must **understand** every line. If you don't, ask.

**Git workflow for a pair:**

1. One person creates the repository (or a feature branch) and pushes it; the other **clones** it.
2. Agree on **one shared repository and branch**, and share the work through it (the exercise requires each pair to submit one shared repo/branch).
3. At each role swap: the current driver **commits and pushes**, and the new driver runs **`git pull`** before typing a single line. This avoids conflicts.
4. Commit in **small steps** with clear messages: `Add is_valid_test_id with prefix option`, `Add username generator`, `Add timer decorator`.
5. Add a `.gitignore` (with `__pycache__/`) at the start.
6. Optionally credit your partner in a commit message: add a line `Co-authored-by: Partner Name <partner@example.com>` in the commit body.
7. If you hit a merge conflict, resolve it **together**, as practised on Wednesday.

**Short retrospective.** At the end, write a brief reflection in the repository (for example `RETROSPECTIVE.md`). Useful prompts:

- What went well in how we worked together?
- What was difficult, technically and as a team?
- What did each of us learn from the other?
- What would we do differently next time?
- Which functions are we most proud of, and which need improvement?

---

### 9. A Complete Mini Library

Here is a compact version you can use as a reference for structure (not something to copy blindly; your pair will design its own):

```python
"""test_utils: reusable helpers for test automation."""

import random
import string
import time
from functools import wraps


# ---------- validators ----------
def is_valid_test_id(test_id, prefix="TC", digits=3):
    """Return True for IDs like 'TC-007'."""
    start = f"{prefix}-"
    if not test_id.startswith(start):
        return False
    number = test_id[len(start):]
    return number.isdigit() and len(number) == digits


# ---------- generators ----------
def generate_username(prefix="user", length=4, seed=None):
    """Return a username like 'user4821' (pass a seed for repeatable output)."""
    rng = random.Random(seed)
    digits = "".join(rng.choice(string.digits) for _ in range(length))
    return f"{prefix}{digits}"


# ---------- formatters ----------
def format_duration(seconds):
    """Return a duration like '2m 5s'."""
    minutes, secs = divmod(int(seconds), 60)
    return f"{minutes}m {secs}s" if minutes else f"{secs}s"


# ---------- decorators ----------
def timer(func):
    """Decorator: print how long the function takes."""
    @wraps(func)
    def wrapper(*args, **kwargs):
        start = time.perf_counter()
        result = func(*args, **kwargs)
        print(f"[timer] {func.__name__} took {time.perf_counter() - start:.4f}s")
        return result
    return wrapper


# ---------- self-checks ----------
def run_self_checks():
    assert is_valid_test_id("TC-007")
    assert not is_valid_test_id("TC-7")
    assert generate_username(seed=1) == generate_username(seed=1)
    assert format_duration(125) == "2m 5s"
    assert format_duration(45) == "45s"
    print("All self-checks passed")


if __name__ == "__main__":
    run_self_checks()
```

Run it: `python test_utils.py` prints `All self-checks passed`. Import it from another file in the same folder: `from test_utils import generate_username`.

---

### 10. Common Mistakes

| Mistake | Example | Fix |
|---|---|---|
| Printing instead of returning | `print(result)` inside the helper | `return result` |
| Doing several jobs in one function | Validate + print + save | Split into separate functions |
| Depending on global variables | Hidden inputs | Pass values as parameters |
| Mutable default arguments | `def f(items=[])` | `None` and create inside |
| Unclear names | `def f(x)` | `def format_duration(seconds)` |
| No docstrings | Nobody knows what it does | Add one-line docstrings |
| Module name matches a standard library | `random.py` | Rename your file |
| Importing from the wrong folder | `ModuleNotFoundError` | Run from the folder containing the module |
| Demo code runs on import | Unwanted output | Use `if __name__ == "__main__":` |
| Not handling edge cases | Division by zero, empty text | Decide and test the behaviour |
| Randomness without seeds | Failures can't be reproduced | Accept or log a seed |
| Role swaps skipped in pair programming | One person dominates | Use a timer and honour it |
| Forgetting to `git pull` after a swap | Conflicts | Pull before typing |
| Committing `__pycache__` | Noisy repository | Add to `.gitignore` |

---

### 11. Practice Activities

Start a small project (individually first, then continue as a pair in the exercise).

1. **Project setup.** Create a folder `test-utils`, initialise Git, add a `.gitignore` containing `__pycache__/`, and make a first commit.
2. **Module.** Create `test_utils.py` with a module docstring and `percent(part, whole)`. Create `demo.py` that imports and uses it. Run the demo.
3. **Validators.** Write `is_valid_test_id`, `is_valid_email`, `is_in_range` and `is_valid_status_code` with docstrings. List at least three edge cases for each.
4. **Generators.** Write `generate_username`, `generate_email` and `generate_password`. Check that two runs give different values and that a seed makes them identical.
5. **Formatters.** Write `format_duration` handling seconds, minutes and hours, and `clean_text`.
6. **Decorator.** Add `timer` to the library and use it in `demo.py` on a function that sleeps for a moment.
7. **Self-checks.** Write at least 10 `assert` statements covering normal, boundary and invalid cases, wrapped in `run_self_checks()` and called under `if __name__ == "__main__":`.
8. **Main guard.** Prove to yourself what the guard does: put a `print("loaded")` outside the guard and another inside; run the file directly and import it from `demo.py`, and compare.
9. **Refactor.** Review your functions against the principles in section 2. Which one violates "return, don't print"? Which has a hidden dependency? Fix them.
10. **README.** Write a README with usage examples for each function.
11. **Commit history.** Make sure you have at least five meaningful commits, one per feature. View them with `git log --oneline`.
12. **Pair rehearsal.** With a partner, practice the driver/navigator routine for 10 minutes on a tiny function. Swap roles, and do `git pull` after the swap.
13. **Retrospective.** After the pair exercise, write down three things that worked well and three things to improve.

---

## Summary

- A **utility function** is a small, general helper that does one job; reusable functions have **one responsibility**, **clear names**, **parameters for inputs**, **return values for outputs**, **sensible defaults**, **docstrings** and deliberate **edge-case handling**.
- Prefer **returning** over printing, avoid hidden global dependencies, and avoid unexpected mutation of arguments.
- Put related functions in a **module** (`test_utils.py`) and bring them in with `import`, `from ... import ...` or an alias; run scripts from the module's folder and never name a module after a standard-library one.
- **`if __name__ == "__main__":`** makes a file work as both a library and a script.
- A test-utility library typically has **validators** (return booleans), **data generators** (use `random`, with **seeds** for reproducibility), **formatters** and **decorators** such as `timer`.
- Use **`assert`** statements to check your functions: normal values, boundaries, invalid and empty input.
- Document with docstrings, type hints and a README.
- In **pair programming**, the driver types and the navigator reviews; swap every 30 minutes, **commit, push and pull** at each swap, share one repository/branch, resolve conflicts together and finish with a short retrospective.
- Tomorrow: **classes and objects** let you bundle related data and functions together, the next step toward a real test framework.

---

## Additional Resources

- Python Tutorial: Modules: https://docs.python.org/3/tutorial/modules.html
- Python documentation: `random`, generate pseudo-random numbers: https://docs.python.org/3/library/random.html
- Real Python: Python Modules and Packages, An Introduction: https://realpython.com/python-modules-packages/
