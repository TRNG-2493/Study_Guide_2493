# Context Managers

## Learning Objectives

By the end of this lesson you will be able to:

- Explain what a **context manager** is and the problem it solves (reliable setup and cleanup).
- Use the `with` statement confidently, including with several resources at once.
- Describe exactly what happens when a `with` block starts, ends normally, and ends because of an exception.
- Compare `with` to the equivalent `try`/`finally` code.
- Write your own context manager as a **class** using `__enter__` and `__exit__`.
- Write your own context manager as a **generator function** using `contextlib.contextmanager`.
- Use useful ready-made tools from `contextlib` (`suppress`, `redirect_stdout`, `ExitStack`, `closing`) and from the standard library (temporary files and directories, `os.chdir` patterns).
- Decide whether an `__exit__` method should swallow or propagate an exception.
- Apply context managers to realistic QA tasks: timing a test, creating and cleaning up test data, temporarily changing environment variables, and capturing output.

---

## Why This Matters

A recurring theme of this week's epic is writing code that stays correct *when things go wrong*. Many operations in test automation follow the same three-part pattern:

1. **Set up** something (open a file, connect to a database, start a mock server, create temporary test data, start a timer).
2. **Use** it (do the actual work, which might fail).
3. **Tear it down** (close, disconnect, stop, delete, record the time), **no matter what happened in step 2**.

If step 3 is skipped when step 2 fails, you leak resources and leave your environment dirty: files stay open, temporary data pollutes the next test run, a browser process stays alive in the background, an environment variable stays changed and makes an unrelated test fail. These "leaks" produce the worst kind of test problem: **flaky tests whose result depends on what ran before them**.

You have already met two tools that help:

- `try`/`finally` (earlier today), which guarantees cleanup.
- `with open(...) as f:` (in the file-handling lesson), which closes files automatically.

A **context manager** is the general mechanism behind `with`. Once you understand it, you can make *anything* clean up after itself. Test frameworks use exactly this idea to manage test setup and teardown, and you will see it throughout professional Python code.

---

## The Concept

### 1. The Problem: Cleanup That Is Easy to Forget

Recall file handling without `with`:

```python
f = open("data.txt", "w", encoding="utf-8")
f.write("important results\n")
# ... imagine 30 lines of code here, and an exception occurs ...
f.close()          # never reached if an exception happens above
```

You can fix it with `try`/`finally`:

```python
f = open("data.txt", "w", encoding="utf-8")
try:
    f.write("important results\n")
finally:
    f.close()
```

That is correct, but it must be written every single time, and it is easy to forget or get wrong. Programmers want a way to package "setup + cleanup" once and reuse it. That is precisely what a context manager is.

### 2. The `with` Statement

```python
with open("data.txt", "w", encoding="utf-8") as f:
    f.write("important results\n")
```

Breaking down the syntax:

```
with  <expression>  as  <name>:
    <indented block>
```

- `<expression>` produces a **context manager** object (here, the file object returned by `open`).
- `as <name>` is optional; it binds the value produced when entering the context.
- The indented **block** is the "use" step.
- When the block finishes, in **any** way, cleanup happens automatically.

Roughly speaking, the `with` statement above behaves like:

```python
manager = open("data.txt", "w", encoding="utf-8")
f = manager.__enter__()          # setup; the result is what 'as' receives
try:
    f.write("important results\n")
finally:
    manager.__exit__(None, None, None)   # cleanup (arguments describe any exception)
```

(The real implementation is a little more precise about exceptions, as we will see.) The important insight: **a context manager is any object with two special methods, `__enter__` and `__exit__`.** The special methods with double underscores (nicknamed "dunder" methods) are ones Python calls for you at specific moments.

### 3. What Exactly Happens, Step by Step

Consider:

```python
with SomeManager() as value:
    do_work()
```

1. `SomeManager()` is evaluated, creating the manager object.
2. Python calls `manager.__enter__()`. Whatever it **returns** is assigned to `value`.
3. The block `do_work()` runs.
4. **Whatever happens next, `manager.__exit__(...)` is called:**
   - If the block finished normally: `__exit__(None, None, None)`.
   - If the block raised an exception: `__exit__(exc_type, exc_value, traceback)` is called with details of the exception. If `__exit__` returns a **true** value, the exception is **suppressed** (swallowed). If it returns false/`None`, the exception **continues propagating** after cleanup.
   - If the block executes `return`, `break` or `continue`: `__exit__` is still called.

We can watch this with a tiny custom class, which also gives us our first look at writing one.

### 4. Your First Custom Context Manager (Class-Based)

```python
class Announcer:
    """A context manager that prints when it starts and stops."""

    def __init__(self, name):
        self.name = name

    def __enter__(self):
        print(f"[enter] {self.name} starting")
        return self                      # this becomes the 'as' variable

    def __exit__(self, exc_type, exc_value, traceback):
        if exc_type is None:
            print(f"[exit]  {self.name} finished cleanly")
        else:
            print(f"[exit]  {self.name} failed with {exc_type.__name__}: {exc_value}")
        return False                     # do not swallow exceptions


with Announcer("demo task") as a:
    print("  working inside the block, a.name =", a.name)

print()

try:
    with Announcer("risky task"):
        print("  about to fail")
        raise ValueError("something broke")
        print("  this line is never reached")
except ValueError as error:
    print("Caught outside the with block:", error)
```

Output:

```
[enter] demo task starting
  working inside the block, a.name = demo task
[exit]  demo task finished cleanly

[enter] risky task starting
  about to fail
[exit]  risky task failed with ValueError: something broke
Caught outside the with block: something broke
```

**Explanation:**

- `__init__` runs when `Announcer("demo task")` creates the object, and stores the name.
- `__enter__(self)` runs as the block starts; it prints a message and returns `self`, so `a` in `as a` is the manager itself. (Often `__enter__` returns some *other* useful resource instead, such as an open connection.)
- `__exit__(self, exc_type, exc_value, traceback)` always takes these three extra parameters:
  - `exc_type`: the exception class (e.g. `ValueError`), or `None` if no error.
  - `exc_value`: the exception instance, or `None`.
  - `traceback`: the traceback object, or `None`.
- Returning `False` (or nothing, which is `None`) means "I did my cleanup; let the exception continue." The `ValueError` therefore reached our outer `except`.
- In the failing case the cleanup message still printed *before* the outer handler ran. Cleanup is guaranteed.

### 5. Suppressing Exceptions from `__exit__`

If `__exit__` returns `True`, the exception is swallowed and execution continues after the `with` block as if nothing had happened:

```python
class IgnoreKeyErrors:
    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        if exc_type is KeyError:
            print("(ignoring a missing key:", exc_value, ")")
            return True          # swallow KeyError only
        return False             # everything else propagates


data = {"a": 1}
with IgnoreKeyErrors():
    print(data["a"])
    print(data["b"])             # KeyError -> swallowed
    print("not reached")

print("execution continues here")
```

Output:

```
1
(ignoring a missing key: 'b' )
execution continues here
```

Notice that `"not reached"` is never printed: the block is abandoned at the point of failure; only the exception is swallowed, not the skipped code.

**A strong word of caution.** Swallowing exceptions is dangerous for the same reasons that a bare `except: pass` is (see the first lesson today). Only suppress a **specific, expected** exception type, and only when ignoring it is truly correct. Return `False` otherwise.

### 6. Context Managers as Generator Functions: `contextlib.contextmanager`

Writing a class with two methods for every little task is heavy. The standard library module `contextlib` offers a shortcut: write a **generator function** with a single `yield`, and decorate it with `@contextmanager`.

```python
from contextlib import contextmanager

@contextmanager
def announce(name):
    print(f"[enter] {name} starting")      # setup: runs before the block
    try:
        yield                               # the 'with' block runs here
    finally:
        print(f"[exit]  {name} finished")  # cleanup: always runs


with announce("generator-based task"):
    print("  working...")
```

Output:

```
[enter] generator-based task starting
  working...
[exit]  generator-based task finished
```

**How it works:**

- Code **before** `yield` is the setup (the `__enter__` part).
- The `yield` statement hands control to the `with` block. A value placed after `yield` becomes the `as` variable (`yield resource`).
- Code **after** `yield` is the teardown (the `__exit__` part).
- If the block raises an exception, it is re-raised **at the `yield` line**, so wrap the `yield` in `try`/`finally` (for guaranteed cleanup) or `try`/`except` (to handle it).

> A **generator** is a function that uses `yield` to produce values one at a time and pause between them. You do not need to understand generators in general to use `@contextmanager`; just follow the pattern: *setup, `try: yield`, `finally: cleanup`.*

Returning a value to the `as` variable:

```python
from contextlib import contextmanager

@contextmanager
def opened_for_append(path):
    f = open(path, "a", encoding="utf-8")
    try:
        yield f                 # 'as' variable receives the open file
    finally:
        f.close()
        print(f"(closed {path})")

with opened_for_append("log.txt") as log:
    log.write("one more line\n")
```

```
(closed log.txt)
```

The mistake to avoid: forgetting `try`/`finally` around the `yield`. Without it, an exception in the block would skip your cleanup code:

```python
@contextmanager
def broken_cleanup():
    print("setup")
    yield
    print("cleanup")        # skipped if the with-block raises!
```

**Which style should I use?**

| Use a class when... | Use `@contextmanager` when... |
|---------------------|-------------------------------|
| The manager has meaningful state or several methods | The logic is "setup, yield, cleanup" |
| You want it reusable/inspectable as an object | You want the shortest readable code |
| You need fine control over `__exit__`'s return value | The default (propagate errors) is what you want |

### 7. Multiple Context Managers in One `with`

Separate them with commas; they are entered left to right and exited in **reverse** order (like nested blocks):

```python
with open("in.txt", encoding="utf-8") as src, open("out.txt", "w", encoding="utf-8") as dst:
    for line in src:
        dst.write(line.upper())
```

Equivalent nested form:

```python
with open("in.txt", encoding="utf-8") as src:
    with open("out.txt", "w", encoding="utf-8") as dst:
        for line in src:
            dst.write(line.upper())
```

Wrapping the whole list in parentheses lets you spread it over lines (officially supported from Python 3.10, and works in 3.9 in practice):

```python
with (
    open("in.txt", encoding="utf-8") as src,
    open("out.txt", "w", encoding="utf-8") as dst,
):
    dst.write(src.read())
```

Demonstration of ordering:

```python
with announce("outer"), announce("inner"):
    print("  inside both")
```

```
[enter] outer starting
[enter] inner starting
  inside both
[exit]  inner finished
[exit]  outer finished
```

(using the `announce` function defined earlier). The last resource opened is the first closed, which is the safe order for dependencies.

### 8. Ready-Made Context Managers You Will Use

**Files:** `open()` returns a context manager (shown throughout).

**`contextlib.suppress`:** a clean way to ignore specific exceptions:

```python
import os
from contextlib import suppress

with suppress(FileNotFoundError):
    os.remove("maybe_missing.tmp")      # fine if it does not exist
print("done")
```

This replaces:

```python
try:
    os.remove("maybe_missing.tmp")
except FileNotFoundError:
    pass
```

and is more readable, and it names the one exception that is acceptable. Use it only for situations where ignoring the error is genuinely right.

**`contextlib.redirect_stdout`:** capture what code prints (useful for checking output):

```python
import io
from contextlib import redirect_stdout

buffer = io.StringIO()
with redirect_stdout(buffer):
    print("this goes into the buffer, not the screen")

print("Captured:", repr(buffer.getvalue()))
```

```
Captured: 'this goes into the buffer, not the screen\n'
```

**`tempfile.TemporaryDirectory` and `tempfile.NamedTemporaryFile`:** create temporary working areas that vanish afterwards, perfect for tests that must not leave files behind:

```python
import tempfile
from pathlib import Path

with tempfile.TemporaryDirectory() as folder:
    work_file = Path(folder) / "scratch.txt"
    work_file.write_text("temporary content", encoding="utf-8")
    print("exists inside:", work_file.exists())

print("exists after :", work_file.exists())
```

```
exists inside: True
exists after : False
```

The directory and everything in it are deleted automatically when the block exits, even after an error.

**`contextlib.closing`:** gives `with` support to an object that has a `.close()` method but is not itself a context manager:

```python
from contextlib import closing

class OldStyleConnection:
    def close(self):
        print("connection closed")

with closing(OldStyleConnection()) as conn:
    print("using", conn.__class__.__name__)
```

```
using OldStyleConnection
connection closed
```

**`contextlib.ExitStack`:** manages a *variable number* of context managers:

```python
from contextlib import ExitStack
import tempfile, os

paths = []
with tempfile.TemporaryDirectory() as folder:
    for name in ("a.txt", "b.txt", "c.txt"):
        paths.append(os.path.join(folder, name))
        with open(paths[-1], "w", encoding="utf-8") as f:
            f.write(name)

    with ExitStack() as stack:
        files = [stack.enter_context(open(p, encoding="utf-8")) for p in paths]
        print([f.read() for f in files])
    print("all closed:", all(f.closed for f in files))
```

```
['a.txt', 'b.txt', 'c.txt']
all closed: True
```

`ExitStack` is how you open "however many files the test needs" while still guaranteeing every one is closed.

(Other managers you will meet later: database connections and transactions, locks, and test-framework helpers for checking that code raises a particular exception. We will cover the unit-testing framework in depth on Wednesday.)

### 9. Why Not Just Use `try`/`finally`?

You can; `with` is simply *`try`/`finally` packaged for reuse*. Advantages:

- **Reuse:** write the cleanup logic once, use it everywhere.
- **Readability:** the intent ("with this resource, do that") is clear, and cleanup is not buried at the end of a long function.
- **Fewer mistakes:** callers cannot forget the cleanup.
- **Composability:** several resources combine naturally.

### 10. Best Practices

1. **Always use `with` for files**, connections, locks and other resources that must be released.
2. **Keep the `with` block focused:** do only the work that needs the resource inside it. Process results after the block so the resource is released sooner.
3. In `@contextmanager` functions, **put `yield` inside `try`/`finally`.**
4. In `__exit__`, **return `True` only for specific exceptions you deliberately handle.** Never swallow everything.
5. Make `__exit__` itself **robust**: avoid raising new exceptions from cleanup code if you can, since they would hide the original error.
6. **Name your managers clearly** (`temporary_environment`, `timer`, `database_session`) so the `with` line reads like a sentence.
7. Remember the variable after `as` **remains accessible after the block** (the file object, for example, is merely closed, not deleted): `f.closed` is `True`.

---

## Real-World QA Scenarios

### Scenario 1: A reusable timer for test steps

```python
import time
from contextlib import contextmanager

@contextmanager
def timer(label):
    start = time.perf_counter()
    try:
        yield
    finally:
        elapsed = time.perf_counter() - start
        print(f"{label} took {elapsed:.2f}s")


with timer("simulated page load"):
    time.sleep(0.25)
```

Possible output:

```
simulated page load took 0.25s
```

`time.perf_counter()` is a high-resolution clock for measuring durations. Because the report is in `finally`, you still get a timing even if the step fails, which is exactly when you want the data. (`time` and `datetime` serve different purposes: `perf_counter` is for measuring intervals, not telling the date.)

### Scenario 2: Temporarily changing an environment variable

Tests often need `BASE_URL=https://staging...` for a moment, then everything restored, so the next test is unaffected.

```python
import os
from contextlib import contextmanager

@contextmanager
def temporary_env(name, value):
    original = os.environ.get(name)         # None if it was not set
    os.environ[name] = value
    try:
        yield
    finally:
        if original is None:
            del os.environ[name]
        else:
            os.environ[name] = original


print("before:", os.environ.get("BASE_URL"))
with temporary_env("BASE_URL", "https://staging.example.test"):
    print("inside:", os.environ.get("BASE_URL"))
print("after :", os.environ.get("BASE_URL"))
```

Output (assuming `BASE_URL` was not set beforehand):

```
before: None
inside: https://staging.example.test
after : None
```

Without a context manager, a test failing in the middle would leave the variable modified and corrupt later tests. This protects test isolation.

### Scenario 3: Self-cleaning test data

```python
import json
import os
from contextlib import contextmanager

@contextmanager
def temp_json_file(path, data):
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f)
    print(f"[setup] created {path}")
    try:
        yield path
    finally:
        os.remove(path)
        print(f"[teardown] removed {path}")


with temp_json_file("fixture_users.json", [{"id": 1}, {"id": 2}]) as path:
    with open(path, encoding="utf-8") as f:
        print("loaded", len(json.load(f)), "users")

print("file still exists?", os.path.exists("fixture_users.json"))
```

Output:

```
[setup] created fixture_users.json
loaded 2 users
[teardown] removed fixture_users.json
file still exists? False
```

This is the pattern behind test **fixtures**: create what the test needs, hand it over, and *always* clean up.

### Scenario 4: A transaction-like manager (class based)

This models a database-style "commit if all went well, roll back otherwise" idea, with a fake in-memory store so it runs anywhere. (We will begin working with real databases and SQL on Thursday.)

```python
class FakeTransaction:
    """Applies changes to a dict only if the block finishes without error."""

    def __init__(self, store):
        self.store = store
        self.pending = {}

    def __enter__(self):
        return self.pending                  # the block writes into 'pending'

    def __exit__(self, exc_type, exc_value, traceback):
        if exc_type is None:
            self.store.update(self.pending)  # commit
            print("committed", self.pending)
        else:
            print("rolled back because of", exc_type.__name__)
        return False                         # never hide the error


database = {"stock": 10}

with FakeTransaction(database) as tx:
    tx["stock"] = 9
    tx["last_order"] = "A100"

try:
    with FakeTransaction(database) as tx:
        tx["stock"] = 0
        raise RuntimeError("payment failed")
except RuntimeError:
    pass

print(database)
```

Output:

```
committed {'stock': 9, 'last_order': 'A100'}
rolled back because of RuntimeError
{'stock': 9, 'last_order': 'A100'}
```

The second transaction's change (`stock = 0`) never reached the store. Real database libraries use exactly this approach.

---

## Code Examples: Putting It All Together

A complete script: a context manager that creates a scratch workspace, a second that times a step, and a robust file reader combining them with exception handling. Save as `cm_demo.py`.

```python
"""cm_demo.py - Context managers for workspace setup, timing and safe reading."""

import json
import shutil
import tempfile
import time
from contextlib import contextmanager
from pathlib import Path


@contextmanager
def workspace(prefix="qa_"):
    """Create a temporary folder, yield its Path, always delete it afterwards."""
    folder = Path(tempfile.mkdtemp(prefix=prefix))
    print(f"[workspace] created {folder.name}")
    try:
        yield folder
    finally:
        shutil.rmtree(folder, ignore_errors=True)
        print(f"[workspace] removed {folder.name}")


@contextmanager
def timed(label):
    start = time.perf_counter()
    try:
        yield
    finally:
        print(f"[timed] {label}: {time.perf_counter() - start:.3f}s")


def read_json_or_none(path):
    try:
        with open(path, encoding="utf-8") as f:
            return json.load(f)
    except FileNotFoundError:
        print("  missing file:", path.name)
    except json.JSONDecodeError as error:
        print(f"  invalid JSON in {path.name}: {error.msg}")
    return None


with workspace() as folder, timed("whole scenario"):
    good = folder / "good.json"
    bad = folder / "bad.json"
    good.write_text('{"ok": true}', encoding="utf-8")
    bad.write_text('{"ok": tru', encoding="utf-8")

    for p in (good, bad, folder / "absent.json"):
        print(p.name, "->", read_json_or_none(p))

print("folder still exists?", folder.exists())
```

Output (folder name and time vary):

```
[workspace] created qa_x8h2k1
good.json -> {'ok': True}
  invalid JSON in bad.json: Expecting value
bad.json -> None
  missing file: absent.json
absent.json -> None
[timed] whole scenario: 0.001s
[workspace] removed qa_x8h2k1
folder still exists? False
```

**Walkthrough:**

1. `workspace()` uses `tempfile.mkdtemp` to create a unique folder, yields its path, and in `finally` removes it with `shutil.rmtree`, so no mess remains even after an error.
2. `timed()` measures the duration and prints in `finally`.
3. One `with` statement enters both managers; they exit in reverse order (timer first, then workspace deletion), as the output shows.
4. `read_json_or_none` uses nested `with open(...)` and specific `except` clauses (previous lessons combined).
5. After the block, the folder is gone: proof that cleanup is dependable.

---

## Practice Exercises

**Exercise 1: Predict.** What is printed?

```python
class Demo:
    def __enter__(self):
        print("A")
        return 42
    def __exit__(self, *args):
        print("C")

with Demo() as value:
    print("B", value)
```

**Exercise 2: Class-based.** Write a class `CountingBlock` whose `__enter__` prints `"start"` and whose `__exit__` prints `"end"` followed by how many seconds the block took. Use `time.perf_counter()`.

**Exercise 3: Generator-based.** Rewrite Exercise 2 using `@contextmanager`.

**Exercise 4: Directory switcher.** Write a context manager `working_directory(path)` that uses `os.chdir` to change the current directory inside the block and always changes back afterward. Prove it works by printing `os.getcwd()` before, inside, and after. (Hint: use `tempfile.gettempdir()` as a destination.)

**Exercise 5: Suppression.** Write a function `try_delete(path)` using `contextlib.suppress` that deletes a file if present and does nothing if it is missing.

**Exercise 6: Exception swallowing.** Write a class-based manager `Retryable` whose `__exit__` swallows `ConnectionError` (printing "network blip ignored") but lets all other exceptions through. Test with `ConnectionError` and `ValueError`.

**Exercise 7: Think.** Why is this `@contextmanager` function buggy? How do you fix it?

```python
@contextmanager
def open_resource():
    r = acquire()
    yield r
    release(r)
```

### Answers

**Exercise 1:**

```
A
B 42
C
```

`__enter__` returns 42, which `as value` receives; `__exit__` runs after the block.

**Exercise 2:**

```python
import time

class CountingBlock:
    def __enter__(self):
        print("start")
        self.begin = time.perf_counter()
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        print(f"end ({time.perf_counter() - self.begin:.2f}s)")
        return False

with CountingBlock():
    time.sleep(0.1)
```

**Exercise 3:**

```python
import time
from contextlib import contextmanager

@contextmanager
def counting_block():
    print("start")
    begin = time.perf_counter()
    try:
        yield
    finally:
        print(f"end ({time.perf_counter() - begin:.2f}s)")

with counting_block():
    time.sleep(0.1)
```

**Exercise 4:**

```python
import os
import tempfile
from contextlib import contextmanager

@contextmanager
def working_directory(path):
    previous = os.getcwd()
    os.chdir(path)
    try:
        yield
    finally:
        os.chdir(previous)

print("before:", os.getcwd())
with working_directory(tempfile.gettempdir()):
    print("inside:", os.getcwd())
print("after :", os.getcwd())
```

**Exercise 5:**

```python
import os
from contextlib import suppress

def try_delete(path):
    with suppress(FileNotFoundError):
        os.remove(path)
```

**Exercise 6:**

```python
class Retryable:
    def __enter__(self):
        return self
    def __exit__(self, exc_type, exc_value, traceback):
        if exc_type is not None and issubclass(exc_type, ConnectionError):
            print("network blip ignored")
            return True
        return False

with Retryable():
    raise ConnectionError("dropped")
print("continued after ConnectionError")

try:
    with Retryable():
        raise ValueError("real bug")
except ValueError as error:
    print("ValueError escaped:", error)
```

**Exercise 7:** The `release(r)` line is skipped when the `with` block raises an exception, because the exception is re-raised at the `yield`. Wrap in `try`/`finally`:

```python
@contextmanager
def open_resource():
    r = acquire()
    try:
        yield r
    finally:
        release(r)
```

---

## Summary / Key Takeaways

- A **context manager** packages *setup + guaranteed cleanup*. The `with` statement is how you use one: `with manager as name:`.
- Technically, a context manager is an object with `__enter__` (setup; its return value feeds `as`) and `__exit__(exc_type, exc_value, traceback)` (cleanup; runs on success, on exceptions, and on `return`/`break`).
- `__exit__` returning `True` **suppresses** the exception; returning `False`/`None` lets it propagate. Suppress only specific, expected exceptions.
- `@contextlib.contextmanager` turns a generator into a context manager: code before `yield` is setup, code after is teardown. Always wrap `yield` in `try`/`finally`.
- Multiple managers can share one `with` line (exited in reverse order). `ExitStack` handles a variable number.
- Handy tools: `open`, `tempfile.TemporaryDirectory`, `contextlib.suppress`, `redirect_stdout`, `closing`.
- For QEs, context managers are the key to **clean, isolated, repeatable tests**: timing steps, temporary files, changed environment variables and any resource that must never be left dangling.

---

## Additional Resources

- Python Language Reference, "The with statement": https://docs.python.org/3/reference/compound_stmts.html#the-with-statement
- Python Library Reference, `contextlib`: https://docs.python.org/3/library/contextlib.html
- Python Language Reference, "With Statement Context Managers" (the `__enter__` / `__exit__` protocol): https://docs.python.org/3/reference/datamodel.html#with-statement-context-managers
