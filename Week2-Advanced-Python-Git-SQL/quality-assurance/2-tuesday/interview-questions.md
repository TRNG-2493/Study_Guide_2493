# Interview Questions: Week 2 — Tuesday: Exception Handling & File Processing

**Scope:** try/except/else/finally, raising and creating custom exceptions, assertions, reading and writing files, CSV/JSON/XML and context managers (`with`).
**Total:** 20 questions (14 Beginner, 5 Intermediate, 1 Advanced).

---

## Beginner (Foundational)

### Q1: What is the difference between a syntax error and an exception, and how do you read a traceback?
**Keywords:** syntax error, runtime, exception object, call stack, bottom up
<details>
<summary>Click to Reveal Answer</summary>

A syntax error happens before the program runs: Python cannot understand the code, so it refuses to start and you fix the code itself. An exception happens while the program is running; the code is valid, but something goes wrong, for example `int("abc")`. An exception is an object Python creates to describe the problem, and if nothing catches it the program stops and prints a traceback. Read a traceback from the bottom up: the last line gives the exception type and message, and the entries above it show the call stack, with the bottom entry being where the error actually happened.

```python
number = int("abc")   # valid syntax, raises ValueError at runtime
```
</details>

*Source:* `try-except-else-and-finally.md`

---

### Q2: In a `try` statement, when does each of `except`, `else` and `finally` run?
**Keywords:** except, else, finally, no exception, cleanup
<details>
<summary>Click to Reveal Answer</summary>

`try` holds the risky code. `except` runs only if a matching exception was raised in the `try` block. `else` runs only if the `try` block finished without raising any exception, and it must come after all `except` blocks. `finally` runs no matter what (success, handled exception, unhandled exception, or even a `return`), so it is used for cleanup such as closing files or connections. Putting follow-up logic in `else` rather than at the end of `try` means errors in that logic are not mistaken for the error you are catching.

```python
try:
    number = int("10")
except ValueError:
    print("not a number")
else:
    print("converted", number)
finally:
    print("always runs")
```
</details>

*Source:* `try-except-else-and-finally.md`

---

### Q3: Why does the order of `except` blocks matter, and why is a bare `except:` considered bad practice?
**Keywords:** exception hierarchy, parent class, specific first, bare except, KeyboardInterrupt
<details>
<summary>Click to Reveal Answer</summary>

Exceptions form a hierarchy, and an `except` for a parent class also catches all of its children (`OSError` catches `FileNotFoundError` and `PermissionError`). Python runs the first matching block from top to bottom, so specific handlers must come before general ones; otherwise the specific block is unreachable. A bare `except:` catches everything, including `KeyboardInterrupt` and `SystemExit`, and it hides bugs such as a `NameError` caused by a typo. Catch the specific exceptions you expect and know how to handle.

```python
try:
    open("missing.txt")
except FileNotFoundError:      # specific first
    print("no such file")
except OSError:                # general afterwards
    print("other OS problem")
```
</details>

*Source:* `try-except-else-and-finally.md`

---

### Q4: Why should a function raise an exception instead of returning a "magic" error value such as `-1`?
**Keywords:** raise, magic value, ambiguity, fail fast, propagate
<details>
<summary>Click to Reveal Answer</summary>

A magic value is ambiguous: `divide(-10, 10)` legitimately returns `-1.0`, so the caller cannot tell an error from a valid result. If the caller forgets to check, the bad value flows onward and causes a confusing failure far from the real cause. An exception cannot be ignored by accident (the program stops loudly if nobody handles it), keeps the return value meaning what it says, carries a type and message, and propagates automatically to code that knows what to do. The rule of thumb is to fail fast and fail loudly.

```python
def set_age(age):
    if age < 0:
        raise ValueError("Age cannot be negative")
    return age
```
</details>

*Source:* `raising-and-creating-custom-exceptions.md`

---

### Q5: How do you create a custom exception, and what must you remember when you add extra attributes?
**Keywords:** inherit from Exception, `Error` suffix, `__init__`, `super().__init__`, attributes
<details>
<summary>Click to Reveal Answer</summary>

A custom exception is a class that inherits from `Exception` (never `BaseException`), conventionally named with an `Error` suffix and given a docstring. To carry structured data such as a row number, override `__init__`, store the values as attributes and call `super().__init__(message)` so that `str(error)` and the traceback show your message. Forgetting that `super()` call is a common mistake. Handlers can then read the attributes instead of parsing message text, because messages are for humans and types are for code.

```python
class InvalidRecordError(Exception):
    def __init__(self, row_number, reason):
        self.row_number = row_number
        self.reason = reason
        super().__init__(f"Row {row_number}: {reason}")
```
</details>

*Source:* `raising-and-creating-custom-exceptions.md`

---

### Q6: What is the difference between a bare `raise`, `raise NewError(...) from original` and `raise NewError(...) from None`?
**Keywords:** re-raise, chaining, `__cause__`, original traceback, suppress
<details>
<summary>Click to Reveal Answer</summary>

Inside an `except` block, a bare `raise` re-throws the exception being handled with its original traceback, which is useful when you want to observe a failure but let the caller decide the outcome. `raise NewError(...) from original` creates an explicit chain: you get a friendly high-level message and the real low-level cause, available as `error.__cause__`, and the traceback says "the direct cause of". `raise NewError(...) from None` deliberately suppresses the chain so only the new exception shows; use it rarely, only to hide noisy internal detail.

```python
try:
    int("abc")
except ValueError as original:
    raise ValueError("Invalid quantity: 'abc'") from original
```
</details>

*Source:* `raising-and-creating-custom-exceptions.md`

---

### Q7: What does the `assert` statement do, and what happens to assertions when Python runs with `-O`?
**Keywords:** assert, AssertionError, `-O`, `__debug__`, programmer bug
<details>
<summary>Click to Reveal Answer</summary>

`assert condition, message` declares that the condition must be true at that point; if it is falsy, Python raises `AssertionError` (with the optional message), and otherwise nothing happens. A failing assertion signals a bug in our own code, a broken assumption. When Python runs with `python -O`, every `assert` statement is removed, and `__debug__` becomes `False`. That is why assertions must never be used for validating user input, file data or security, and why the expression must have no side effects.

```python
passed, total = 12, 10
assert passed <= total, f"passed ({passed}) cannot exceed total ({total})"
```
</details>

*Source:* `assertions.md`

---

### Q8: Compare the file modes `"r"`, `"w"`, `"a"` and `"x"`. Which one is dangerous, and why?
**Keywords:** read, write erases, append, exclusive create, FileExistsError
<details>
<summary>Click to Reveal Answer</summary>

`"r"` (the default) reads text and raises `FileNotFoundError` if the file does not exist. `"w"` writes text, creating the file if needed but erasing all existing content the instant it is opened. `"a"` appends to the end, keeping existing content and creating the file if needed. `"x"` creates a new file and raises `FileExistsError` if it already exists, which protects against accidental overwriting. Mode `"w"` is the dangerous one: if you mean to add to a results file, use `"a"`, and if you must never overwrite, use `"x"`.
</details>

*Source:* `reading-and-writing-files.md`

---

### Q9: What are the different ways to read a text file in Python, and which should you use for a very large log file?
**Keywords:** `read()`, `readline()`, `readlines()`, iterate, memory
<details>
<summary>Click to Reveal Answer</summary>

`read()` returns the whole file as one string, `readline()` returns one line (including its trailing `\n`), and `readlines()` returns a list of all lines; `read()` and `readlines()` load everything into memory. A file object is iterable, so `for line in f:` reads lazily one line at a time and uses very little memory, which makes it the default choice and the right one for a multi-gigabyte log. Use `line.strip()` to remove the trailing newline.

```python
errors = 0
with open("server.log", encoding="utf-8") as f:
    for line in f:
        if "ERROR" in line:
            errors += 1
```
</details>

*Source:* `reading-and-writing-files.md`

---

### Q10: Why should you always pass `encoding="utf-8"` to `open()` and use a `with` statement?
**Keywords:** platform default, UTF-8, close, flush buffer, `with`
<details>
<summary>Click to Reveal Answer</summary>

If you omit `encoding`, Python uses a platform-dependent default, so a file written on one machine may fail to decode or show garbled characters on another; UTF-8 is the universal standard, so state it explicitly (`utf-8-sig` removes the BOM from spreadsheet exports). Files must be closed because buffered data is only flushed to disk on close, operating-system handles are limited, and open files can be locked. A `with` block closes the file automatically even if an error occurs, so it is the recommended way to work with files.

```python
with open("results.txt", "w", encoding="utf-8") as f:
    f.write("hello\n")
```
</details>

*Source:* `reading-and-writing-files.md`

---

### Q11: Why use the `csv` module instead of `line.split(",")`, and what is the difference between `csv.reader` and `csv.DictReader`?
**Keywords:** quoting, `newline=""`, DictReader, header, strings
<details>
<summary>Click to Reveal Answer</summary>

`split(",")` breaks when a value contains a comma, because CSV handles such values by quoting them (and doubling a literal quote), and quoted values can even contain line breaks; the `csv` module understands all these rules. `csv.reader` yields each row as a list of strings, so you access columns by position, which is fragile if a column is inserted. `csv.DictReader` uses the header row to give each row as a dictionary keyed by column name. Open CSV files with `newline=""`, and remember every value is a string, so you must convert types yourself.

```python
import csv
with open("users.csv", newline="", encoding="utf-8") as f:
    for row in csv.DictReader(f):
        print(row["name"], int(row["age"]))
```
</details>

*Source:* `csv-json-and-xml.md`

---

### Q12: What is the difference between `json.load`, `json.loads`, `json.dump` and `json.dumps`, and how do JSON types map to Python?
**Keywords:** file vs string, `load`/`loads`, `dump`/`dumps`, dict, None
<details>
<summary>Click to Reveal Answer</summary>

`load` and `dump` work with file objects, while `loads` and `dumps` work with strings (the "s" stands for string). Parsing turns a JSON object into a `dict`, an array into a `list`, a string into `str`, a number into `int` or `float`, `true`/`false` into `True`/`False`, and `null` into `None`. JSON syntax is strict: double quotes only, no trailing commas and no comments. Options such as `indent=2` and `sort_keys=True` make the output readable and stable.

```python
import json
data = json.loads('{"id": 1, "active": true, "manager": null}')
print(data["active"], data["manager"])   # True None
```
</details>

*Source:* `csv-json-and-xml.md`

---

### Q13: What is a context manager, and what happens when a `with` block starts and ends, including when it ends with an exception?
**Keywords:** `__enter__`, `__exit__`, setup, cleanup, suppress
<details>
<summary>Click to Reveal Answer</summary>

A context manager is any object with `__enter__` and `__exit__` methods that packages setup plus guaranteed cleanup. When `with` starts, Python calls `__enter__()` and assigns its return value to the `as` variable. When the block ends, `__exit__` is always called: with `(None, None, None)` after normal completion, or with the exception type, value and traceback if the block raised. If `__exit__` returns a true value the exception is suppressed; if it returns `False` or `None` the exception continues to propagate after cleanup.
</details>

*Source:* `context-managers.md`

---

### Q14: When would you write a context manager as a class, and when with `@contextlib.contextmanager`?
**Keywords:** class, generator, `yield`, try/finally, `__exit__` return value
<details>
<summary>Click to Reveal Answer</summary>

Use a class when the manager has meaningful state or several methods, or when you need fine control over what `__exit__` returns. Use `@contextmanager` when the logic is simply "setup, yield, cleanup" and you want the shortest readable code: code before `yield` is setup, the value after `yield` becomes the `as` variable, and code after it is teardown. Always wrap the `yield` in `try`/`finally`, otherwise an exception in the block skips your cleanup.

```python
from contextlib import contextmanager

@contextmanager
def announce(name):
    print("start", name)
    try:
        yield
    finally:
        print("end", name)
```
</details>

*Source:* `context-managers.md`

---

## Intermediate (Application)

### Q15: A test pipeline receives a JSON test-data file that may be missing or malformed. How would you handle this so the failure is clear to whoever owns the data?
**Keywords:** `JSONDecodeError`, `FileNotFoundError`, line/column, custom exception, `raise ... from`
**Hint:** Think about two separate failures, and what information the decode error object gives you.
<details>
<summary>Click to Reveal Answer</summary>

Catch the two failures separately: `FileNotFoundError` for a missing file and `json.JSONDecodeError` (a subclass of `ValueError`) for malformed content. The decode error exposes `msg`, `lineno` and `colno`, so you can tell the data owner exactly where the file is broken. In a reusable loader, translate these into your own exception (for example `TestDataError`) using `raise ... from error`, so callers get a consistent type and the original cause is kept in `__cause__`. A function that raises is easier to reuse and test than one that prints and returns `None`.

```python
import json

class TestDataError(Exception):
    """Test data is missing or invalid."""

def load_json(path):
    try:
        with open(path, encoding="utf-8") as f:
            return json.load(f)
    except FileNotFoundError as error:
        raise TestDataError(f"File not found: {path}") from error
    except json.JSONDecodeError as error:
        raise TestDataError(
            f"Invalid JSON in {path}: {error.msg} (line {error.lineno}, column {error.colno})"
        ) from error
```
</details>

*Source:* `csv-json-and-xml.md`, `raising-and-creating-custom-exceptions.md`

---

### Q16: When should you use `assert` and when should you use `raise`? Give a QA example of each.
**Keywords:** external data, internal invariant, `-O`, ValueError, AssertionError
**Hint:** Ask whether the situation can legitimately happen, and whether removing the check would let bad external data through.
<details>
<summary>Click to Reveal Answer</summary>

Use `raise` (an exception) for anything that can legitimately go wrong in the outside world: user input, file contents, API data, missing files. It is always active and is often handled and recovered from. Use `assert` for things that should be impossible if your own code is correct, such as internal invariants and postconditions, since a failure means a bug and assertions can be disabled with `-O`. For example, a negative `price` read from a CSV is external data, so raise `ValueError`; a check that `passed + failed + skipped == total` after you counted results is your own logic, so assert.

```python
if price < 0:                                  # external data -> exception
    raise ValueError(f"price must not be negative, got {price}")

assert sum(summary.values()) == len(results)   # internal invariant -> assertion
```
</details>

*Source:* `assertions.md`

---

### Q17: You load a CSV of 500 test users and some rows have a non-numeric age, a blank cell or a missing column. Should one bad row stop the whole load? How would you design the loader?
**Keywords:** collect errors, row number, `DictReader`, structural vs row-level, continue
**Hint:** Compare problems with the file's structure to problems with individual rows.
<details>
<summary>Click to Reveal Answer</summary>

Separate structural problems from row-level problems. A missing required column makes the whole file unusable, so check `reader.fieldnames` first and raise an error. A bad value in one row should not discard the other good rows, so wrap only the conversion in `try`/`except` (for `ValueError`, `TypeError`), record a message with the line number and error type, and carry on. Return both the good records and the list of problems so the report shows every issue instead of a crash on the first one. Remember that `DictReader` gives `None` for cells missing from a short row, and that every value arrives as a string.

```python
good, errors = [], []
for line_no, row in enumerate(reader, start=2):   # line 1 is the header
    try:
        good.append({"id": int(row["id"]), "age": int(row["age"])})
    except (ValueError, TypeError) as error:
        errors.append(f"line {line_no}: {type(error).__name__}")
```
</details>

*Source:* `csv-json-and-xml.md`, `try-except-else-and-finally.md`

---

### Q18: Your test creates a temporary data file, and if the test fails midway the leftover file breaks the next run. How would you guarantee cleanup?
**Keywords:** `finally`, context manager, `tempfile`, isolation, `yield`
**Hint:** There are two or three tools from today's lessons that guarantee cleanup.
<details>
<summary>Click to Reveal Answer</summary>

Put the cleanup where it always runs. The basic option is `try`/`finally`, with the removal in `finally`. A reusable option is a `@contextmanager` function that creates the file, yields its path inside `try`, and removes the file in `finally`, which is the pattern behind test fixtures. If you only need a scratch area, `tempfile.TemporaryDirectory()` as a context manager deletes the folder and its contents automatically on exit, even after an error. This prevents leftover state, which causes flaky tests that depend on what ran before.

```python
import os
from contextlib import contextmanager

@contextmanager
def temp_file(path, text):
    with open(path, "w", encoding="utf-8") as f:
        f.write(text)
    try:
        yield path
    finally:
        os.remove(path)
```
</details>

*Source:* `context-managers.md`, `try-except-else-and-finally.md`

---

### Q19: You must summarise a JUnit-style XML test report (count failed tests and list their messages). How would you do it with `ElementTree`, and what pitfalls would you watch for?
**Keywords:** `ET.parse`, `findall`, `find` returns None, `is not None`, `ParseError`
**Hint:** What does `find()` return when the element is absent, and what does `if element:` do for an element with no children?
<details>
<summary>Click to Reveal Answer</summary>

Parse with `ET.parse(path).getroot()` (or `ET.fromstring` for a string), loop over `root.findall("testcase")`, and check each case for a `failure` child. `find()` returns `None` when nothing matches, so calling `.text` on it raises `AttributeError`; test with `is not None` (an element with no children is falsy, so `if element:` is wrong) or use `findtext` with a default. Attribute values are strings, so convert numbers such as `time` with `float()`. Wrap the parse in `except ET.ParseError` so a malformed report is reported clearly, and treat untrusted XML with caution.

```python
import xml.etree.ElementTree as ET

root = ET.fromstring('<s><testcase name="a"/><testcase name="b"><failure message="boom"/></testcase></s>')
for case in root.findall("testcase"):
    failure = case.find("failure")
    if failure is not None:
        print(case.get("name"), failure.get("message"))
```
</details>

*Source:* `csv-json-and-xml.md`

---

## Advanced (Deep Dive)

### Q20: A `with` block raises an exception. Describe step by step what happens for a class-based manager, how the outcome changes if `__exit__` returns `True`, and what is different for a `@contextmanager` function that has no `try`/`finally` around its `yield`.
**Keywords:** `__exit__` arguments, suppress, propagate, re-raised at `yield`, skipped cleanup
**Hint:** Where, exactly, does the generator-based manager see the exception?
<details>
<summary>Click to Reveal Answer</summary>

Python calls `__enter__`, runs the block, and the block raises; the block is abandoned at that line and `__exit__(exc_type, exc_value, traceback)` is called with the exception details. If `__exit__` returns `False` or `None`, the exception continues to propagate after cleanup; if it returns `True`, the exception is swallowed and execution continues after the `with` block (the skipped lines of the block still never run). With `@contextmanager`, the exception is re-raised inside the generator at the `yield` line. If `yield` is not wrapped in `try`/`finally`, the exception leaves the generator immediately and the code after `yield` (the cleanup) never runs, leaking the resource.

```python
from contextlib import contextmanager

@contextmanager
def broken():
    print("setup")
    yield
    print("cleanup")        # skipped when the block raises

try:
    with broken():
        raise ValueError("boom")
except ValueError:
    print("caught; 'cleanup' never printed")
```
</details>

*Source:* `context-managers.md`

---

## How to use this bank

This bank is for self-quizzing, so do not read the answers first.

1. Read a question and cover the answer (keep the `<details>` block closed).
2. Say your answer aloud as if you were in an interview, in 30 to 60 seconds. Use the hint only if you are stuck.
3. Open the answer and check that every **keyword** appeared in what you said. If you missed one, repeat the question until you can include it naturally.
4. Work through Beginner first until you can answer without notes, then attempt Intermediate (talk through the scenario step by step), then the Advanced question.
5. If you struggle with a topic, re-read the lesson named in the *Source* line and try again the next day.
