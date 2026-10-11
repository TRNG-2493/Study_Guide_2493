# Try, Except, Else and Finally

## Learning Objectives

By the end of this lesson you will be able to:

- Explain what an **exception** is and how it differs from a syntax error.
- Read a Python **traceback** and locate the line, the function, and the exception type that caused a failure.
- Use `try` and `except` to catch errors and keep a program running.
- Catch **specific** exception types (and several at once) instead of using a dangerous "catch everything" handler.
- Use `as` to capture the exception object and read its message.
- Use the `else` clause for "only if nothing went wrong" logic and the `finally` clause for cleanup that must always run.
- Recognise the most common built-in exceptions you will meet in test automation (`ValueError`, `TypeError`, `KeyError`, `IndexError`, `FileNotFoundError`, `ZeroDivisionError`, and more).
- Understand the **exception hierarchy** and why the order of `except` blocks matters.
- Apply good practices: handle only what you can handle, never silence errors, and keep the `try` block small.
- Recognise common anti-patterns such as the bare `except:` and the "swallowed" exception.

---

## Why This Matters

This week's epic is to *harden* your Python: to move from scripts that work when everything goes perfectly to code that behaves sensibly when things go wrong. In the **QE Foundations** project you are building, things go wrong constantly:

- A test-data file that a colleague promised would be in a folder is missing.
- A CSV has a blank cell where a number should be.
- A JSON response from an API is missing a field your script expected.
- A network call times out.
- A test suite is half-way through 400 test cases when one case hits bad data.

If one bad row can crash your whole test run, you lose the results of the 399 good cases, and you spend your morning working out what happened. A well-designed error handler can instead record "row 17 was invalid, here is why", continue with the remaining rows, and give you a complete report.

There is a second, deeper reason this matters to a Quality Engineer. **Your job is to find and report failures.** To do that well you must be able to tell apart:

1. A failure in the **system under test** (a real bug you should report), and
2. A failure in **your own test code or environment** (a broken script, missing file, or bad data).

Exception handling is the tool that lets you separate and clearly label these two situations. Test frameworks you will meet later in the programme are built on exactly the ideas in this lesson.

Yesterday (Monday) you worked with modules, virtual environments and `pip`. Today's topics build on that: the code you split into modules must now also be *robust*, and the files you read will be handled safely.

---

## The Concept

### 1. Errors: Syntax Errors vs Exceptions

Python can fail in two broad ways.

**Syntax errors** happen *before* your program runs. Python reads your file, cannot understand it, and refuses to start:

```python
print("Hello"
```

```
  File "example.py", line 1
    print("Hello"
         ^
SyntaxError: '(' was never closed
```

You fix a syntax error by correcting the code. You do not "handle" it at runtime, because the program never starts.

**Exceptions** happen *while* the program is running. The code is grammatically valid, but something goes wrong when Python tries to execute it:

```python
number = int("abc")      # valid syntax, but "abc" is not a number
```

```
Traceback (most recent call last):
  File "example.py", line 1, in <module>
    number = int("abc")
ValueError: invalid literal for int() with base 10: 'abc'
```

An **exception** is an *object* that Python creates to describe a problem. When it is created and "thrown" we say the exception is **raised**. If nothing catches it, it travels up through the calling code until it reaches the top of the program, and the program stops and prints a traceback.

Think of it like a fire alarm in a building. A raised exception is the alarm going off. If nobody responds, the whole building is evacuated (the program ends). If a trained person (an `except` block) responds, they deal with the problem and normal work can continue.

### 2. Reading a Traceback

Before you can handle errors, you must be able to read them. Here is a slightly larger example:

```python
def parse_price(text):
    return float(text)

def total(prices):
    result = 0
    for p in prices:
        result += parse_price(p)
    return result

print(total(["10.5", "20", "abc"]))
```

Output:

```
Traceback (most recent call last):
  File "prices.py", line 10, in <module>
    print(total(["10.5", "20", "abc"]))
  File "prices.py", line 6, in total
    result += parse_price(p)
  File "prices.py", line 2, in parse_price
    return float(text)
ValueError: could not convert string to float: 'abc'
```

How to read it:

1. **Read from the bottom up.** The last line is the most important: the exception type (`ValueError`) and a human-readable message (`could not convert string to float: 'abc'`).
2. The lines above show the **call stack**: the chain of function calls that led to the failure. The *bottom* entry (`parse_price`, line 2) is where the error actually happened. The entry above it (`total`, line 6) is who called it, and so on up to the top (`<module>`, which means the main body of the script).
3. Each entry shows the file, line number, function name, and the line of code.

> **Tip:** When a test fails in your CI pipeline, the traceback is often all you have. Learning to read it quickly is one of the most valuable debugging skills. (We will cover systematic debugging in depth on Wednesday.)

### 3. The Basic `try` / `except`

The simplest form of exception handling looks like this:

```python
try:
    # code that might fail
except SomeError:
    # what to do if it fails
```

**How it works, step by step:**

1. Python starts running the code inside the `try` block, line by line.
2. If every line succeeds, the `except` block is **skipped** entirely.
3. If a line raises an exception, Python **immediately stops** running the rest of the `try` block (the remaining lines are never executed) and looks for an `except` block that matches the exception type.
4. If a matching `except` is found, its code runs, and then the program continues with the code *after* the whole `try` statement.
5. If no `except` matches, the exception keeps travelling upwards (to the calling function, and so on).

A first complete example:

```python
raw_value = "abc"

try:
    quantity = int(raw_value)
    print("Parsed quantity:", quantity)
except ValueError:
    print("Quantity must be a whole number, got:", raw_value)

print("Program keeps running")
```

Output:

```
Quantity must be a whole number, got: abc
Program keeps running
```

**Line-by-line explanation:**

| Line | What happens |
|------|--------------|
| `raw_value = "abc"` | A string that cannot be converted to a number. |
| `try:` | Starts a protected block. |
| `quantity = int(raw_value)` | `int("abc")` raises `ValueError`. Python jumps out of the `try` block here. |
| `print("Parsed quantity:", quantity)` | **Never runs**, because the previous line failed. |
| `except ValueError:` | The raised exception is a `ValueError`, so this block matches. |
| `print("Quantity must be...")` | Runs, reporting the problem to the user. |
| `print("Program keeps running")` | Runs normally, since the exception was handled. |

If you change `raw_value` to `"42"`, the output becomes:

```
Parsed quantity: 42
Program keeps running
```

and the `except` block is skipped.

### 4. Catching Specific Exceptions

Python has many built-in exception types. You should catch the **specific** ones you expect and know how to handle. Here are the ones QA engineers meet most often:

| Exception | When it occurs | Typical test-automation example |
|-----------|----------------|---------------------------------|
| `ValueError` | Right type, wrong value | `int("abc")` while parsing a CSV cell |
| `TypeError` | Operation on the wrong type | `"5" + 3`, or `len(None)` |
| `KeyError` | Dictionary key does not exist | A JSON field is missing: `user["email"]` |
| `IndexError` | List index out of range | `row[5]` when a CSV row has only 3 columns |
| `AttributeError` | Object has no such attribute/method | Calling `.strip()` on `None` |
| `ZeroDivisionError` | Division or modulo by zero | Calculating a pass rate when there are 0 tests |
| `FileNotFoundError` | File or folder does not exist | Test-data file is missing |
| `PermissionError` | OS refuses access | Trying to write to a read-only folder |
| `NameError` | Variable not defined | A typo in a variable name |
| `ImportError` / `ModuleNotFoundError` | Import fails | Forgetting to `pip install` a package in your virtual environment |
| `OSError` | Operating-system level problem (parent of several above) | Disk full, bad path, etc. |
| `TimeoutError` | An operation took too long | A network or device call timed out |
| `KeyboardInterrupt` | User pressed Ctrl+C | Aborting a long test run |

Let us see several of them triggered, so that you recognise them:

```python
# Each of these lines is run separately to show the exception it raises.
examples = {
    "ValueError": lambda: int("12.5"),
    "TypeError": lambda: "5" + 3,
    "KeyError": lambda: {"name": "Ada"}["email"],
    "IndexError": lambda: [1, 2, 3][10],
    "AttributeError": lambda: None.strip(),
    "ZeroDivisionError": lambda: 10 / 0,
    "FileNotFoundError": lambda: open("no_such_file.txt"),
}

for label, action in examples.items():
    try:
        action()
    except Exception as error:          # broad on purpose, only for this demo
        print(f"{label:18} -> {type(error).__name__}: {error}")
```

Output (messages can vary slightly between Python versions):

```
ValueError         -> ValueError: invalid literal for int() with base 10: '12.5'
TypeError          -> TypeError: can only concatenate str (not "int") to str
KeyError           -> KeyError: 'email'
IndexError         -> IndexError: list index out of range
AttributeError     -> AttributeError: 'NoneType' object has no attribute 'strip'
ZeroDivisionError  -> ZeroDivisionError: division by zero
FileNotFoundError  -> FileNotFoundError: [Errno 2] No such file or directory: 'no_such_file.txt'
```

(`lambda` is just a compact way of making a tiny function so we can run each failing expression inside our `try`. You do not need to master it today.)

### 5. Capturing the Exception Object with `as`

When you write `except ValueError as error:`, Python stores the exception object in the variable `error`. This object has useful information:

```python
try:
    int("abc")
except ValueError as error:
    print("Type   :", type(error).__name__)
    print("Message:", error)
    print("Args   :", error.args)
```

Output:

```
Type   : ValueError
Message: invalid literal for int() with base 10: 'abc'
Args   : ("invalid literal for int() with base 10: 'abc'",)
```

- `type(error).__name__` gives the exception's class name as a string.
- `str(error)` (or just printing it) gives the message.
- `error.args` is a tuple of the arguments the exception was created with.

Some exceptions carry extra, specific attributes. For example, `FileNotFoundError` (a kind of `OSError`) has `.filename` and `.strerror`:

```python
try:
    open("missing_data.csv")
except FileNotFoundError as error:
    print("Could not find:", error.filename)
    print("OS says      :", error.strerror)
```

```
Could not find: missing_data.csv
OS says      : No such file or directory
```

Note: the variable name after `as` (here `error`) only exists inside the `except` block. Python deletes it when the block ends, so do not try to use it afterwards.

### 6. Handling Multiple Exception Types

There are two ways to handle several different problems.

**Option A: separate `except` blocks**, when each problem needs a different response:

```python
def read_quantity(record):
    """Return the quantity from a dictionary record as an integer."""
    try:
        return int(record["quantity"])
    except KeyError:
        print("Record has no 'quantity' field:", record)
    except ValueError:
        print("Quantity is not a whole number:", record["quantity"])
    except TypeError:
        print("Quantity has an unusable type:", record["quantity"])
    return None


print(read_quantity({"quantity": "7"}))
print(read_quantity({"item": "mouse"}))
print(read_quantity({"quantity": "seven"}))
print(read_quantity({"quantity": None}))
```

Output:

```
7
Record has no 'quantity' field: {'item': 'mouse'}
None
Quantity is not a whole number: seven
None
Quantity has an unusable type: None
None
```

Python checks the `except` blocks **from top to bottom** and runs the **first** one that matches. Only one `except` block ever runs for a single exception.

**Option B: one `except` with a tuple**, when the response is the same:

```python
try:
    value = int(record["quantity"])
except (KeyError, ValueError, TypeError) as error:
    print("Bad record:", type(error).__name__, error)
    value = None
```

Note the parentheses: the exception types are grouped in a **tuple**. Writing `except KeyError, ValueError:` without parentheses is a different (and, in older Python versions, a misleading) construct, so always use parentheses when listing several types.

### 7. The Exception Hierarchy and Why Order Matters

Exceptions are organised as a family tree using **inheritance**. A simplified view of the most relevant branches:

```
BaseException
 ├── KeyboardInterrupt
 ├── SystemExit
 └── Exception
      ├── ArithmeticError
      │    └── ZeroDivisionError
      ├── LookupError
      │    ├── IndexError
      │    └── KeyError
      ├── OSError
      │    ├── FileNotFoundError
      │    ├── PermissionError
      │    └── TimeoutError
      ├── ValueError
      ├── TypeError
      ├── AttributeError
      └── ... many more
```

The key idea: **an `except` for a parent class also catches all of its children.** `except LookupError` catches both `KeyError` and `IndexError`. `except OSError` catches `FileNotFoundError` and `PermissionError`. `except Exception` catches almost everything.

This is why order matters. Put the **most specific** handlers first and the more general ones afterwards:

```python
try:
    open("/root/secret.txt")
except FileNotFoundError:
    print("File does not exist")
except PermissionError:
    print("File exists but you may not read it")
except OSError as error:
    print("Some other operating-system problem:", error)
```

If you reversed it and put `except OSError` first, it would catch everything and the more specific blocks below would be unreachable (they would never run). Python's tooling and linters often warn about this.

Why are `KeyboardInterrupt` and `SystemExit` outside `Exception`? So that a broad `except Exception:` does **not** accidentally stop a user from pressing Ctrl+C to abort the program. This is one reason `except Exception` is acceptable at the very top level of a program but a bare `except:` is not (see below).

### 8. The `else` Clause

`else` on a `try` statement means: "run this block **only if the `try` block finished without raising any exception**."

```python
try:
    stock = int("25")
except ValueError:
    print("Stock value is not a number")
else:
    print("Stock parsed successfully:", stock)
```

Output:

```
Stock parsed successfully: 25
```

You might ask: *why not just put the `print` at the end of the `try` block?* There are two good reasons.

1. **Precision.** The `try` block should contain only the statements you expect might raise the exception you are catching. If you put extra code inside `try`, an exception from *that* code could be caught by mistake, hiding a genuine bug.
2. **Readability.** `try` = "the risky thing", `except` = "what if it fails", `else` = "what to do when it worked".

Here is an example where the difference is real:

```python
def load_and_summarise(path):
    try:
        file = open(path)                 # the only risky step we are guarding
    except FileNotFoundError:
        print("Data file not found:", path)
        return None
    else:
        lines = file.read().splitlines()  # runs only if open() succeeded
        file.close()
        return len(lines)
```

Exceptions raised inside the `else` block are **not** caught by the `except` clauses of the same `try` statement. That is the point: errors in your follow-up logic are not mistaken for "file not found".

### 9. The `finally` Clause

`finally` contains code that runs **no matter what**: whether the `try` block succeeded, raised a handled exception, raised an unhandled exception, or even executed a `return`.

```python
def divide(a, b):
    try:
        result = a / b
    except ZeroDivisionError:
        print("Cannot divide by zero")
        return None
    else:
        return result
    finally:
        print("divide() finished")


print(divide(10, 2))
print(divide(10, 0))
```

Output:

```
divide() finished
5.0
Cannot divide by zero
divide() finished
None
```

Notice that `"divide() finished"` is printed **before** the return value is printed, and it is printed in both cases, even though both branches execute a `return`. The `finally` block runs on the way out of the function.

**What is `finally` for?** **Cleanup** that must happen regardless of success: closing files, closing database connections, quitting a browser, deleting temporary test data, releasing a lock, stopping a mock server.

```python
connection = open_database_connection()      # hypothetical function
try:
    run_validation_queries(connection)
except Exception as error:
    print("Validation failed:", error)
finally:
    connection.close()                        # always runs, even after errors
```

> **Preview:** On this very day you will also learn **context managers** and the `with` statement, which handle this kind of cleanup more elegantly for files and many other resources. `finally` is the fundamental mechanism behind them, so understanding it now will make `with` feel natural.

### 10. The Complete Form and Execution Order

You can combine all four parts:

```python
try:
    # 1. risky code
except SpecificError:
    # 2. runs if SpecificError was raised
else:
    # 3. runs only if NO exception was raised
finally:
    # 4. ALWAYS runs
```

Rules to remember:

- A `try` needs at least one `except` **or** a `finally`.
- `else` is only allowed if there is at least one `except`, and it must come after all `except` blocks.
- `finally` is always last.

Here is a complete demonstration that traces the order for three different inputs:

```python
def process(value):
    print(f"--- processing {value!r}")
    try:
        number = int(value)
        print("try: converted")
    except ValueError:
        print("except: not a number")
    else:
        print("else: conversion worked, number =", number)
    finally:
        print("finally: always runs")


process("10")
process("ten")
```

Output:

```
--- processing '10'
try: converted
else: conversion worked, number = 10
finally: always runs
--- processing 'ten'
except: not a number
finally: always runs
```

Summary of the three possible paths:

| Situation | try | except | else | finally |
|-----------|-----|--------|------|---------|
| No exception | runs fully | skipped | runs | runs |
| Exception, matching `except` | runs until the error | runs | skipped | runs |
| Exception, no match | runs until the error | skipped | skipped | runs, then exception continues upward |

### 11. Exceptions Travel Up the Call Stack

You do **not** have to handle an exception in the function where it happens. Often the better place is higher up, where you have enough context to decide what to do.

```python
def parse_price(text):
    return float(text)            # may raise ValueError, we do not handle it here


def parse_all(prices):
    parsed = []
    for text in prices:
        try:
            parsed.append(parse_price(text))
        except ValueError:
            print("Skipping invalid price:", repr(text))
    return parsed


print(parse_all(["10.5", "abc", "7"]))
```

Output:

```
Skipping invalid price: 'abc'
[10.5, 7.0]
```

The low-level function `parse_price` simply does its job and lets the error escape. The higher-level function `parse_all` has the *policy* ("skip bad prices"), so it handles the exception. A guideline: **handle an exception at the level that knows what to do about it.**

### 12. Re-raising and Exception Chaining (a first look)

Sometimes you want to do something (like print a note) and then let the exception continue. A bare `raise` inside an `except` block re-raises the same exception:

```python
try:
    int("abc")
except ValueError:
    print("Logging the problem, then letting it propagate")
    raise
```

You will learn more about `raise` itself, about raising your own exceptions, and about chaining with `raise ... from ...` in the next lesson, *Raising and Creating Custom Exceptions*. (We will cover proper *logging* in depth on Wednesday; for now `print` is fine.)

---

## Real-World QA Scenarios

### Scenario 1: A resilient test-data reader

You receive a list of strings from a data file. Some are valid ages, some are garbage. A fragile script crashes on the first bad one. A resilient one reports and carries on:

```python
raw_ages = ["34", "27", "", "abc", "-5", "41"]

valid_ages = []
errors = []

for index, raw in enumerate(raw_ages, start=1):
    try:
        age = int(raw)
    except ValueError:
        errors.append(f"Row {index}: {raw!r} is not a whole number")
    else:
        if age < 0:
            errors.append(f"Row {index}: age {age} is negative")
        else:
            valid_ages.append(age)

print("Valid:", valid_ages)
print("Problems:")
for message in errors:
    print("  -", message)
```

Output:

```
Valid: [34, 27, 41]
Problems:
  - Row 3: '' is not a whole number
  - Row 4: 'abc' is not a whole number
  - Row 5: age -5 is negative
```

Explanation: `enumerate(raw_ages, start=1)` gives us a human-friendly row number starting at 1. The conversion is the only statement in `try`. The range check (`age < 0`) lives in `else`, because it should only run when conversion succeeded. A report of *all* problems is far more useful to a tester than a crash on the first one. (Note that negative ages are not a Python error, they are a *business rule*. In the next lesson you will learn to raise your own exceptions for rules like this, and in the lesson after that, *assertions*.)

### Scenario 2: Safe dictionary access for API responses

API responses often omit optional fields. Compare two approaches:

```python
response = {"id": 101, "name": "Laptop"}     # no "price" key

# Approach 1: EAFP, "Easier to Ask Forgiveness than Permission"
try:
    price = response["price"]
except KeyError:
    price = 0.0

# Approach 2: LBYL, "Look Before You Leap"
if "price" in response:
    price = response["price"]
else:
    price = 0.0

# Approach 3: for this simple case, the idiomatic shortcut
price = response.get("price", 0.0)

print(price)
```

Python culture often prefers **EAFP** (try it, handle the failure), because it avoids race conditions (a file might vanish between "check exists" and "open it") and keeps the common path uncluttered. For simple dictionary defaults, `.get()` is best. Use the approach that makes your intent clearest.

### Scenario 3: Guaranteed cleanup after a test

Imagine a test that creates a temporary file of test data. Even if the test fails, the file must be removed so the next run starts clean:

```python
import os

temp_path = "temp_test_data.txt"

try:
    with open(temp_path, "w") as f:
        f.write("id,name\n1,Ada\n")
    # ... pretend a test runs here and something goes wrong ...
    raise RuntimeError("Simulated test failure")
except RuntimeError as error:
    print("Test failed:", error)
finally:
    if os.path.exists(temp_path):
        os.remove(temp_path)
        print("Cleaned up", temp_path)
```

Output:

```
Test failed: Simulated test failure
Cleaned up temp_test_data.txt
```

Here `finally` guarantees the clean-up. (`os` is one of the built-in modules you toured on Monday. `os.path.exists` returns `True` if the path exists, and `os.remove` deletes a file.)

### Scenario 4: Retry logic

Flaky, temporary failures (a slow service) are a daily reality in test automation. A simple retry loop uses `try`/`except`/`else`:

```python
import random

def flaky_operation():
    """Fails about 2 out of 3 times, to simulate an unstable service."""
    if random.random() < 0.66:
        raise ConnectionError("Service temporarily unavailable")
    return "OK"


max_attempts = 5
for attempt in range(1, max_attempts + 1):
    try:
        result = flaky_operation()
    except ConnectionError as error:
        print(f"Attempt {attempt} failed: {error}")
    else:
        print(f"Attempt {attempt} succeeded: {result}")
        break
else:
    print("All attempts failed")
```

(The final `else` belongs to the `for` loop, not to `try`: it runs only if the loop finished without hitting `break`. It is a lesser-known feature and is shown here only so you recognise it.) Output varies due to randomness; one possible run:

```
Attempt 1 failed: Service temporarily unavailable
Attempt 2 failed: Service temporarily unavailable
Attempt 3 succeeded: OK
```

---

## Best Practices and Common Mistakes

### Do: catch specific exceptions

```python
# Good
try:
    value = int(text)
except ValueError:
    value = 0
```

### Don't: use a bare `except:`

```python
# Bad
try:
    value = int(text)
except:
    value = 0
```

A bare `except:` catches **everything**, including `KeyboardInterrupt` (Ctrl+C) and `SystemExit`. It also hides typos: if you misspell a variable inside the `try`, the resulting `NameError` is silently swallowed and your code "works" but does the wrong thing. This is one of the worst habits you can form.

### Be careful with `except Exception:`

It is acceptable in a few places: at the very top of a program or test runner to log an unexpected failure and exit cleanly, or at a boundary where you deliberately isolate one task from the next. Even then, report the error; never ignore it.

### Don't swallow errors silently

```python
# Very bad: the problem vanishes with no trace
try:
    process(row)
except Exception:
    pass
```

If a failure is truly ignorable, add a comment explaining *why*. Otherwise, at minimum record it so someone can investigate later. In test automation, a swallowed exception can make a **failing test appear to pass**, which is the most damaging kind of bug for a QE.

### Keep the `try` block small

```python
# Hard to reason about: which line raised the ValueError?
try:
    data = read_file(path)
    rows = parse(data)
    total = compute(rows)
    save(total)
except ValueError:
    ...

# Better: guard only what can fail the way you expect
try:
    rows = parse(data)
except ValueError as error:
    ...
```

### Handle what you can handle

If you catch an exception and have no sensible recovery (nothing useful to do), let it propagate to a place that does. Catching merely to print a message and then continuing with invalid data creates a second, more confusing failure later.

### Do: include context in messages

`"Error"` is useless. `"Row 17: quantity 'abc' is not a whole number (file: orders.csv)"` can be acted on immediately.

### Use `finally` or a context manager for cleanup

Do not rely on code *after* the `try` statement to close resources, because it will not run if an unhandled exception occurs.

### A common beginner trap: `return` inside `finally`

A `return` inside `finally` overrides any exception in flight and discards it silently. Avoid it.

---

## Code Examples: Putting It All Together

The following complete, runnable script reads numeric test results from a list, tolerates bad data, and reports statistics. Save it as `safe_stats.py` and run it with `python safe_stats.py`.

```python
"""safe_stats.py - Compute a pass rate from messy test-result records."""


def parse_result(record):
    """Convert one record dict into a (name, passed) tuple.

    Raises KeyError if a field is missing, ValueError if 'passed'
    is not one of the accepted strings.
    """
    name = record["name"]
    text = record["passed"].strip().lower()
    if text in ("true", "yes", "pass"):
        return name, True
    if text in ("false", "no", "fail"):
        return name, False
    raise ValueError(f"unrecognised result value: {record['passed']!r}")


def pass_rate(records):
    passed = 0
    failed = 0
    problems = []

    for number, record in enumerate(records, start=1):
        try:
            name, ok = parse_result(record)
        except (KeyError, ValueError, AttributeError) as error:
            problems.append(f"Record {number}: {type(error).__name__}: {error}")
            continue                      # skip this record, go to the next
        if ok:
            passed += 1
        else:
            failed += 1

    total = passed + failed
    try:
        rate = passed / total * 100
    except ZeroDivisionError:
        rate = 0.0
    return rate, problems


records = [
    {"name": "login", "passed": "pass"},
    {"name": "logout", "passed": "FAIL"},
    {"name": "search"},                         # missing 'passed'
    {"name": "checkout", "passed": "maybe"},    # bad value
    {"name": "profile", "passed": None},        # None has no .strip()
    {"name": "cart", "passed": "yes"},
]

rate, problems = pass_rate(records)
print(f"Pass rate: {rate:.1f}%")
for line in problems:
    print(" ", line)

print("Empty input:", pass_rate([]))
```

Expected output:

```
Pass rate: 66.7%
  Record 3: KeyError: 'passed'
  Record 4: ValueError: unrecognised result value: 'maybe'
  Record 5: AttributeError: 'NoneType' object has no attribute 'strip'
Empty input: (0.0, [])
```

**Walkthrough:**

1. `parse_result` does one job. It **raises** problems rather than printing them, which makes it reusable and testable.
2. `pass_rate` is the *policy* layer. It catches three exception types in one tuple, records a descriptive message using `type(error).__name__`, and uses `continue` to skip to the next record.
3. A `ZeroDivisionError` can happen if no records were valid, so we guard just the division and fall back to `0.0`.
4. The main part builds sample data that deliberately includes three kinds of bad records and prints a clear report.

---

## Practice Exercises

Try each exercise on your own before looking at the answers at the bottom.

**Exercise 1: Predict the output.** What does this print?

```python
def check(x):
    try:
        print("A")
        result = 10 / x
        print("B")
    except ZeroDivisionError:
        print("C")
        return "zero"
    else:
        print("D")
        return result
    finally:
        print("E")

print(check(5))
print(check(0))
```

**Exercise 2: Fix the handler order.** This code never prints the specific message. Why, and how do you fix it?

```python
try:
    my_list = [1, 2, 3]
    print(my_list[10])
except LookupError:
    print("Some lookup problem")
except IndexError:
    print("Index is out of range")
```

**Exercise 3: Safe integer reader.** Write a function `to_int(text, default=0)` that returns `int(text)` or `default` if the text cannot be converted. It must also cope with `None` as input. Test it with `"12"`, `"x"`, `None`, `""`.

**Exercise 4: Dictionary field checker.** Write `get_email(user)` that returns `user["contact"]["email"]` or the string `"unknown"` if either key is missing. Use `try`/`except`. Test with `{"contact": {"email": "a@b.com"}}`, `{"contact": {}}`, and `{}`.

**Exercise 5: Spot the problems.** List at least three things that are wrong with this code:

```python
try:
    f = open("results.txt")
    data = f.read()
    total = int(data) / len(data.split())
    print(total)
except:
    pass
```

**Exercise 6: Cleanup guarantee.** Write code that opens `"scratch.txt"` for writing with `open()` (no `with`), writes a line inside a `try`, deliberately raises `ValueError`, catches it, and uses `finally` to close the file. Print `file.closed` at the end to prove it is closed.

### Answers

**Exercise 1:**

```
A
B
D
E
2.0
A
C
E
zero
```

For `check(5)`: `A`, `B` (no error), `else` prints `D` and returns 2.0, but `finally` still runs (`E`) before the value is returned and printed. For `check(0)`: `A`, then division fails so `B` is skipped, `except` prints `C` and returns `"zero"`, `finally` prints `E`, then `zero` is printed.

**Exercise 2:** `IndexError` is a subclass of `LookupError`, so `except LookupError` matches first and the `IndexError` handler is unreachable. Fix by putting the specific one first:

```python
try:
    my_list = [1, 2, 3]
    print(my_list[10])
except IndexError:
    print("Index is out of range")
except LookupError:
    print("Some lookup problem")
```

**Exercise 3:**

```python
def to_int(text, default=0):
    try:
        return int(text)
    except (ValueError, TypeError):
        return default

print(to_int("12"))   # 12
print(to_int("x"))    # 0
print(to_int(None))   # 0  (int(None) raises TypeError)
print(to_int(""))     # 0
```

**Exercise 4:**

```python
def get_email(user):
    try:
        return user["contact"]["email"]
    except KeyError:
        return "unknown"

print(get_email({"contact": {"email": "a@b.com"}}))  # a@b.com
print(get_email({"contact": {}}))                    # unknown
print(get_email({}))                                 # unknown
```

**Exercise 5:** (1) The bare `except:` catches everything including Ctrl+C. (2) `pass` swallows errors silently, so a missing file, a bad number, or a division by zero all look identical (nothing). (3) The file is never closed. (4) The `try` block is too large and mixes unrelated failures (`FileNotFoundError`, `ValueError`, `ZeroDivisionError`) that deserve different handling. (5) `int(data)` converts the *entire* file text, which is almost certainly not the intent, and `data.split()` may be empty. An improved version handles each specific failure with its own message.

**Exercise 6:**

```python
file = open("scratch.txt", "w")
try:
    file.write("first line\n")
    raise ValueError("simulated problem")
except ValueError as error:
    print("Caught:", error)
finally:
    file.close()

print("Closed?", file.closed)   # True
```

---

## Summary / Key Takeaways

- An **exception** is an object raised when something goes wrong at runtime; unhandled, it ends the program with a **traceback** (read it from the bottom up).
- `try` holds the risky code; `except` handles a failure; `else` runs only when no exception happened; `finally` **always** runs and is for cleanup.
- Catch **specific** exceptions. Use `as name` to access the message. Group types in a tuple when the response is identical.
- Exceptions form a **hierarchy**: a parent class catches its children, so list specific `except` blocks before general ones.
- Handle an exception at the level that knows what to do about it; let it propagate otherwise. A bare `raise` re-raises.
- Avoid bare `except:`, avoid swallowing errors with `pass`, keep `try` blocks small, and always give useful context.
- In QA work, solid exception handling turns "the script crashed" into "row 17 had a bad value", which is the difference between a mystery and a report.
- Coming up: the next lesson shows how to **raise** your own exceptions and build **custom exception classes**, followed by **assertions**, **file handling**, **CSV/JSON/XML**, and **context managers**.

---

## Additional Resources

- Python Tutorial, "Errors and Exceptions": https://docs.python.org/3/tutorial/errors.html
- Python Language Reference, "The try statement": https://docs.python.org/3/reference/compound_stmts.html#the-try-statement
- Python Library Reference, "Built-in Exceptions" (full hierarchy): https://docs.python.org/3/library/exceptions.html
