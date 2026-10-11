# Default and Variable-Length Arguments

## Learning Objectives

By the end of this lesson you will be able to:

- Give function parameters **default values** and explain when defaults are used.
- Follow the ordering rule for parameters with and without defaults.
- Explain and avoid the **mutable default argument** trap.
- Write functions that accept any number of positional arguments with `*args`.
- Write functions that accept any number of keyword arguments with `**kwargs`.
- Combine regular parameters, defaults, `*args` and `**kwargs` in the correct order.
- Use `*` and `**` when **calling** a function to unpack lists, tuples and dictionaries into arguments.
- Define keyword-only parameters for clearer function calls.
- Choose when optional and variable-length arguments make a function better.

---

## Why This Matters

In the previous lesson, every parameter was **required**: call the function with the wrong number of arguments and Python raises a `TypeError`. Real-world functions need more flexibility:

- A function that logs a message usually has a sensible default level (`INFO`) but sometimes needs `ERROR`.
- A function that creates a test user should work with just a username, but allow an optional role, an optional timeout and extra options.
- A function that checks many items shouldn't force you to build a list first when you only have three values to hand over.

You have already used this flexibility in built-in functions without noticing:

```python
print("a", "b", "c", sep="-", end="!")     # any number of values, plus optional sep and end
sorted(numbers, reverse=True)               # reverse is optional
round(3.14159, 2)                           # the 2 is optional: round(3.14159) works too
```

`print` accepts *any number* of positional values, and `sep` and `end` are optional keyword arguments with defaults. Today you learn how to build functions that behave like that. The test-utility library in today's exercise will use these features for things like test-data generators with sensible defaults and configurable options.

---

## The Concept

### 1. Default Parameter Values

A **default value** is assigned to a parameter in the `def` line with `=`. If the caller doesn't supply that argument, Python uses the default.

```python
def greet(name, greeting="Hello"):
    return f"{greeting}, {name}!"

print(greet("Priya"))                 # Hello, Priya!        -> default used
print(greet("Priya", "Welcome"))      # Welcome, Priya!      -> default overridden
print(greet("Priya", greeting="Hi"))  # Hi, Priya!           -> keyword form
```

- `name` has no default, so it is **required**.
- `greeting` has a default, so it is **optional**.

Defaults make the *common case* short and still allow the *special case*.

#### A realistic example

```python
def make_test_id(number, prefix="TC", width=3):
    return f"{prefix}-{number:0{width}d}"

print(make_test_id(7))                    # TC-007
print(make_test_id(7, "API"))             # API-007
print(make_test_id(7, width=5))           # TC-00007
print(make_test_id(7, prefix="UI", width=2))   # UI-07
```

(`{number:0{width}d}` is an f-string whose *width* comes from another variable, nested in braces.)

Notice how **keyword arguments let you override just one default** and leave the other alone (`width=5` without touching `prefix`). That is the main reason keyword arguments matter.

#### Another: a configurable pass-rate check

```python
def meets_threshold(passed, total, threshold=90.0):
    if total == 0:
        return False
    return passed / total * 100 >= threshold

print(meets_threshold(46, 50))                  # True  (92% >= 90%)
print(meets_threshold(46, 50, threshold=95))    # False (92% < 95%)
```

---

### 2. The Ordering Rule

**Parameters without defaults must come before parameters with defaults.**

```python
def broken(greeting="Hello", name):     # SyntaxError
    ...
```

```text
SyntaxError: non-default argument follows default argument
```

Why? When you call `broken("Priya")`, Python assigns positionally and would not know whether `"Priya"` is the greeting or the name. The rule keeps calls unambiguous:

```python
def fine(name, greeting="Hello"):
    ...
```

When *calling*, positional arguments come first, then keyword arguments, as you learned in the last lesson.

---

### 3. When Are Defaults Evaluated? The Mutable Default Trap

This is one of Python's best-known gotchas, and it matters for test data.

**Default values are created once, when the function is defined, not each time it is called.** For immutable defaults (numbers, strings, `None`, tuples) that doesn't matter. For **mutable** defaults (lists, dictionaries, sets) it causes bizarre bugs:

```python
def add_result(result, results=[]):      # DANGEROUS
    results.append(result)
    return results

print(add_result("PASS"))        # ['PASS']
print(add_result("FAIL"))        # ['PASS', 'FAIL']   <- expected ['FAIL']!
print(add_result("SKIP"))        # ['PASS', 'FAIL', 'SKIP']
```

The same list object, created once at definition time, is shared by every call that doesn't pass its own list. Imagine two unrelated tests accidentally sharing results. Such bugs are hard to spot.

**The fix: use `None` as the default and create the list inside the function:**

```python
def add_result(result, results=None):
    if results is None:
        results = []
    results.append(result)
    return results

print(add_result("PASS"))        # ['PASS']
print(add_result("FAIL"))        # ['FAIL']    <- correct, a fresh list each time
```

**Rule:** never use `[]`, `{}` or `set()` as a default value. Use `None` and create the object inside. (The `is None` check is the idiom from Tuesday.)

---

### 4. Variable-Length Positional Arguments: `*args`

Sometimes you don't know in advance how many arguments the caller will supply. Put a `*` before a parameter name, conventionally `args`, and Python gathers **all extra positional arguments into a tuple**.

```python
def add_all(*numbers):
    print(numbers)            # shows the tuple
    total = 0
    for n in numbers:
        total += n
    return total

print(add_all(1, 2))              # prints (1, 2)    then 3
print(add_all(5, 10, 15, 20))     # prints (5, 10, 15, 20)    then 50
print(add_all())                  # prints ()    then 0
```

Key points:

- The name after `*` is up to you (`*numbers`, `*ids`, `*messages`); `*args` is the convention when the meaning is generic.
- Inside the function it is an ordinary **tuple**: you can loop over it, `len()` it, index it.
- Zero arguments is allowed; the tuple is just empty.

A testing example: a logger that takes any number of message parts:

```python
def log(*parts, level="INFO"):
    message = " ".join(str(p) for p in parts)
    print(f"[{level}] {message}")

log("Starting test", "TC-001")                  # [INFO] Starting test TC-001
log("Status code:", 404, level="ERROR")         # [ERROR] Status code: 404
```

(The `str(p) for p in parts` inside `join` is a compact loop that converts every part to text; it will be explained in a later lesson on comprehensions. You could also write the loop out by hand.)

Notice `level` comes **after** `*parts`, so it can only be given as a keyword argument; see section 7.

#### Combining required parameters with `*args`

```python
def run_suite(suite_name, *test_ids):
    print(f"Suite {suite_name} has {len(test_ids)} tests:")
    for test_id in test_ids:
        print(f"  - {test_id}")

run_suite("Smoke", "TC-001", "TC-002", "TC-003")
```

```text
Suite Smoke has 3 tests:
  - TC-001
  - TC-002
  - TC-003
```

The first argument fills `suite_name`; everything else goes into `test_ids`.

---

### 5. Variable-Length Keyword Arguments: `**kwargs`

Put **two** stars before a parameter name, conventionally `kwargs` (keyword arguments), and Python gathers all extra **keyword** arguments into a **dictionary**.

```python
def show_options(**options):
    print(options)
    for key, value in options.items():
        print(f"  {key} = {value}")

show_options(browser="Chrome", headless=True, timeout=30)
```

```text
{'browser': 'Chrome', 'headless': True, 'timeout': 30}
  browser = Chrome
  headless = True
  timeout = 30
```

Inside the function, `options` is a plain dictionary (yesterday's skills apply: `.items()`, `.get()`, `in`...).

A practical use: build a test-user record with a few required fields and any number of extras:

```python
def create_user(username, role="viewer", **extra):
    user = {"username": username, "role": role}
    user.update(extra)               # merge extra fields (from yesterday)
    return user

print(create_user("alice"))
print(create_user("bob", role="admin", email="bob@example.com", active=True))
```

```text
{'username': 'alice', 'role': 'viewer'}
{'username': 'bob', 'role': 'admin', 'email': 'bob@example.com', 'active': True}
```

`**kwargs` is great for configuration-style functions where the set of options may grow over time, and also for "pass-through" functions that forward options to another function (you'll see this in the decorators lesson).

**A caution:** `**kwargs` hides which options are valid, so typos pass silently (`create_user("bob", rol="admin")` just adds a key called `rol`). Use it when flexibility is truly needed; otherwise prefer explicit parameters.

---

### 6. The Full Parameter Order

When a function uses all the kinds, they must appear in this order:

```python
def function(required, default="x", *args, keyword_only=None, **kwargs):
    ...
```

| Position | Kind | Example |
|---|---|---|
| 1 | Required positional | `required` |
| 2 | Parameters with defaults | `default="x"` |
| 3 | `*args` | `*args` |
| 4 | Keyword-only (after `*args` or a bare `*`) | `keyword_only=None` |
| 5 | `**kwargs` | `**kwargs` |

You rarely need all of them together, but when you read documentation (such as the signature of `print` or `sorted`) you will see these patterns.

A demonstration:

```python
def demo(a, b=2, *args, c=3, **kwargs):
    print(f"a={a}, b={b}, args={args}, c={c}, kwargs={kwargs}")

demo(1)                          # a=1, b=2, args=(), c=3, kwargs={}
demo(1, 20)                      # a=1, b=20, args=(), c=3, kwargs={}
demo(1, 20, 30, 40)              # a=1, b=20, args=(30, 40), c=3, kwargs={}
demo(1, c=99, x="extra")         # a=1, b=2, args=(), c=99, kwargs={'x': 'extra'}
```

---

### 7. Keyword-Only Parameters

A bare `*` in the parameter list means "everything after this must be passed by keyword":

```python
def create_session(username, *, browser="Chrome", headless=False):
    return f"{username} using {browser} (headless={headless})"

print(create_session("alice", browser="Firefox"))      # OK
print(create_session("alice", "Firefox"))              # TypeError
```

```text
TypeError: create_session() takes 1 positional argument but 2 were given
```

This protects against calls like `create_session("alice", "Firefox", True)` where nobody can tell what `True` means. Forcing the keyword makes calls read clearly: `headless=True`. It is a good habit for options and flags. (Python also has *positional-only* parameters, using `/`, which is rarely needed for now.)

---

### 8. Unpacking Arguments When Calling: `*` and `**`

The stars have a second use: when **calling** a function, they *unpack* a collection into separate arguments.

**`*` unpacks a list or tuple into positional arguments:**

```python
def make_test_id(number, prefix="TC", width=3):
    return f"{prefix}-{number:0{width}d}"

values = (7, "API", 4)
print(make_test_id(*values))       # same as make_test_id(7, "API", 4) -> API-0007
```

```python
numbers = [3, 8, 11]
print(add_all(*numbers))           # same as add_all(3, 8, 11) -> 22
```

**`**` unpacks a dictionary into keyword arguments:**

```python
config = {"prefix": "UI", "width": 2}
print(make_test_id(5, **config))   # same as make_test_id(5, prefix="UI", width=2) -> UI-05
```

This is wonderful for data-driven tests: your test data can live in a list or dictionary and be fed straight into a function:

```python
users = [
    {"username": "alice", "role": "admin"},
    {"username": "bob", "role": "viewer"},
]

for user_data in users:
    print(create_user(**user_data))
```

The dictionary keys must match the parameter names.

You can also use `*` to combine collections: `[*first_list, *second_list]` builds a new list with all items, and `{**defaults, **overrides}` builds a merged dictionary (overrides win), a neat alternative to `.copy()` plus `.update()`:

```python
defaults = {"browser": "Chrome", "timeout": 30}
overrides = {"timeout": 60}

settings = {**defaults, **overrides}
print(settings)       # {'browser': 'Chrome', 'timeout': 60}
```

---

### 9. Designing Good Signatures

A function's **signature** is its name plus its parameters. Good signatures make functions pleasant to use.

| Guideline | Why |
|---|---|
| Put the most important required parameters first | Natural call order |
| Give options sensible defaults | The common case is short |
| Use `None` as the default for mutable options | Avoids the shared-list trap |
| Use keyword-only parameters for flags and options | Calls read clearly |
| Use `*args` when "any number of the same thing" makes sense | e.g. `max(1, 2, 3)` |
| Use `**kwargs` sparingly | Flexible, but hides valid options |
| Avoid more than about five parameters | Too many: pass a dictionary or group them |

Examples of well-designed signatures from Python itself: `print(*objects, sep=' ', end='\n')`, `sorted(iterable, *, key=None, reverse=False)`.

---

### 10. Working Example: A Flexible Test-Data Generator

```python
import random

def generate_test_user(username=None, *, role="viewer", domain="example.com", **extra):
    """Return a dictionary describing a test user.

    username: if omitted, a random name like 'user4821' is generated
    role: user role (keyword-only)
    domain: email domain (keyword-only)
    extra: any additional fields to include
    """
    if username is None:
        username = f"user{random.randint(1000, 9999)}"

    user = {
        "username": username,
        "email": f"{username}@{domain}",
        "role": role,
    }
    user.update(extra)
    return user

print(generate_test_user("alice", role="admin"))
print(generate_test_user(active=False, locale="en-GB"))
```

Sample output (random number varies):

```text
{'username': 'alice', 'email': 'alice@example.com', 'role': 'admin'}
{'username': 'user4821', 'email': 'user4821@example.com', 'role': 'viewer', 'active': False, 'locale': 'en-GB'}
```

This function uses defaults, `None` as a safe default, keyword-only parameters, `**extra`, a docstring and the `random` module. Calling it with no arguments at all works too, which is what makes it so convenient for quickly generating test data. (We'll look at data generators more closely in the last lesson of the day.)

---

### 11. Common Mistakes

| Mistake | Example | Fix |
|---|---|---|
| Non-default parameter after a default one | `def f(a=1, b)` | Put required parameters first |
| Mutable default value | `def f(items=[])` | `items=None`, create inside |
| Forgetting the `*` when calling with a list | `add_all([1, 2, 3])` gives one argument (a list) | `add_all(*[1, 2, 3])` |
| Forgetting `**` for a dictionary | Passes the dict as one argument | `f(**my_dict)` |
| Expecting `*args` to be a list | It is a tuple | `list(args)` if you need to modify it |
| Passing a keyword-only parameter positionally | `TypeError` | Use `name=value` |
| Misspelled option swallowed by `**kwargs` | Silent mistake | Use explicit parameters when possible |
| Too many parameters | Hard to call correctly | Group data or split the function |
| Same keyword passed twice | `f(1, a=1)` where `a` is first parameter | Pass each argument once |

---

### 12. Practice Activities

1. **Default greeting.** Write `greet(name, greeting="Hello")`. Call it with and without the second argument, and with a keyword.
2. **Test ID.** Write `make_test_id(number, prefix="TC", width=3)`. Produce `TC-005`, `API-005` and `TC-0005` using as few arguments as possible.
3. **Threshold.** Write `meets_threshold(passed, total, threshold=90)`. Test it with the default and with a custom threshold.
4. **Mutable trap.** Reproduce the shared-list bug with `results=[]`. Then fix it with `None`. Explain in your own words why the first version misbehaves.
5. **Sum all.** Write `add_all(*numbers)` returning the total. Call it with 0, 1 and 5 arguments, and with `*` unpacking a list.
6. **Average.** Write `average(*numbers)` that returns `0` when called with no arguments (watch out for dividing by zero).
7. **Logger.** Write `log(*parts, level="INFO")` that prints `[LEVEL] part1 part2 ...`. Test with different levels.
8. **Options.** Write `show_options(**options)` that prints each option on its own line, sorted by key. Call it with three options.
9. **User builder.** Write `create_user(username, role="viewer", **extra)`. Create three users, including one built from a dictionary with `**`.
10. **Keyword-only.** Write `open_page(url, *, new_tab=False, wait=5)` and show that `open_page("a.com", True)` fails but `open_page("a.com", new_tab=True)` works.
11. **Merge.** Merge two configuration dictionaries using `{**a, **b}` and show that the second wins on conflicts.
12. **Signature design.** For a function that "creates a test report file", list which parameters you would make required, which optional with defaults, and which keyword-only, and explain why.

---

## Summary

- **Default values** (`def f(a, b=10)`) make parameters optional; the common case becomes short, and keywords let you override just one option.
- Parameters without defaults must come **before** those with defaults.
- Defaults are evaluated **once**, so never use a mutable default like `[]`; use `None` and create the object inside.
- **`*args`** collects extra positional arguments into a **tuple**; **`**kwargs`** collects extra keyword arguments into a **dictionary**.
- Parameter order: required, defaults, `*args`, keyword-only, `**kwargs`.
- A bare `*` makes the following parameters **keyword-only**, which keeps calls readable.
- When **calling**, `*sequence` unpacks into positional arguments and `**dictionary` unpacks into keyword arguments; `{**a, **b}` merges dictionaries.
- Good signatures are simple: sensible defaults, keyword options and few parameters; use `**kwargs` sparingly.
- Next: **lambda functions**, tiny anonymous functions for quick, one-line jobs such as sorting rules.

---

## Additional Resources

- Python Tutorial: More on Defining Functions (default values, keyword arguments, arbitrary argument lists): https://docs.python.org/3/tutorial/controlflow.html#more-on-defining-functions
- Python documentation: Function definitions (parameter reference): https://docs.python.org/3/reference/compound_stmts.html#function-definitions
- Real Python: Python args and kwargs: Demystified: https://realpython.com/python-kwargs-and-args/
