# Daily Knowledge Check: Week2-Advanced-Python-Git-SQL — Wednesday: Python Debugging & Testing Foundations

Try each question before opening the solution. Every question names the written lesson it comes from, so you can go back and re-read.

---

## Part 1: Multiple Choice

### 1. A test helper keeps a module-level counter and updates it like this. Calling `record_pass()` raises `UnboundLocalError`. Why?
```python
passed = 0

def record_pass():
    passed += 1
```
- [ ] A) Functions are not allowed to read module-level variables
- [ ] B) `passed += 1` assigns to `passed`, so Python treats `passed` as local to the whole function, and it has no value yet when the line reads it
- [ ] C) The `+=` operator cannot be used on integers
- [ ] D) A variable must be written in `UPPER_CASE` before a function may change it

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** B) `passed += 1` assigns to `passed`, so Python treats `passed` as local to the whole function, and it has no value yet when the line reads it

**Explanation:** If a function assigns to a name anywhere in its body, that name is local for the whole function. `passed += 1` means "read `passed`, add one, assign it", and the read happens before any local value exists. Fix it by returning the new value (preferred) or by declaring `global passed`.
- **Why others are wrong:**
  - A) Functions can read globals freely (for example `BASE_URL + "/login"`); only the assignment causes the problem.
  - C) `+=` works on integers; it builds a new int and rebinds the name.
  - D) `UPPER_CASE` is only a naming convention for constants and is not enforced by Python.

**Source:** `scope-and-namespaces.md`
</details>

---

### 2. A module sets `x = "global"`. Function `outer` sets `x = "enclosing"` and defines `inner()`, which contains only `print(x)` (it never assigns to `x`). What does `outer()` print after it calls `inner()`?
- [ ] A) `global`
- [ ] B) `enclosing`
- [ ] C) `NameError`
- [ ] D) `UnboundLocalError`

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** B) `enclosing`

**Explanation:** LEGB searches Local, then Enclosing, then Global, then Built-in, and stops at the first match. `inner` has no local `x`, so the enclosing function's `x` wins over the global one.
- **Why others are wrong:**
  - A) The Global scope is searched after Enclosing, and Python stops at the first match, so the module-level `x` is never reached.
  - C) `x` is found in the enclosing scope, so the lookup succeeds.
  - D) That error needs an assignment to `x` inside `inner`; with a plain read, `x` is not local.

**Source:** `scope-and-namespaces.md`
</details>

---

### 3. What happens when Python compiles this code?
```python
def outer():
    def inner():
        nonlocal total
        total = 1
    inner()
```
- [ ] A) A `SyntaxError`: no binding for nonlocal `'total'` found
- [ ] B) It runs, and `nonlocal` creates `total` as a new module-level variable, like `global` would
- [ ] C) It runs, and `total` becomes a new local variable of `inner`
- [ ] D) It compiles, then raises `NameError` only when `inner()` is called

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** A) A `SyntaxError`: no binding for nonlocal `'total'` found

**Explanation:** `nonlocal x` requires that `x` already exists in the nearest enclosing *function*; otherwise Python refuses to compile the code. This is the main difference from `global`, which does not need the name to exist.
- **Why others are wrong:**
  - B) `global` may create a module-level name on assignment, but `nonlocal` may not create anything.
  - C) `nonlocal` declares that the name is *not* local; it must already exist in an enclosing function.
  - D) The missing binding is detected when the function is compiled, before any line runs.

**Source:** `scope-and-namespaces.md`
</details>

---

### 4. A shared test-data dictionary contains a nested list: `DEFAULT_USER = {"name": "test_user", "roles": ["viewer"]}`. Which line gives a copy that you can safely modify (including `roles`) without changing `DEFAULT_USER`?
- [ ] A) `user = DEFAULT_USER.copy()`
- [ ] B) `user = DEFAULT_USER`
- [ ] C) `user = dict(DEFAULT_USER)`
- [ ] D) `user = copy.deepcopy(DEFAULT_USER)` (after `import copy`)

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** D) `user = copy.deepcopy(DEFAULT_USER)` (after `import copy`)

**Explanation:** `copy.deepcopy` recursively copies nested objects, so the new `roles` list is independent of the original. This is the safe pattern for per-test data.
- **Why others are wrong:**
  - A) `.copy()` is a shallow copy: it makes a new outer dict but shares the inner `roles` list.
  - B) This is not a copy at all; both names point to the same dict.
  - C) `dict(...)` is also a shallow copy and shares the inner list.

**Source:** `mutability-and-memory.md`
</details>

---

### 5. After this code runs, what is the value of `data`?
```python
data = [3, 1, 2]
data = data.sort()
```
- [ ] A) `[1, 2, 3]`
- [ ] B) `[3, 1, 2]`
- [ ] C) A `TypeError` is raised
- [ ] D) `None`

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** D) `None`

**Explanation:** In-place methods such as `list.sort`, `append` and `reverse` change the object and return `None`. Assigning that result back to `data` replaces the list with `None`, a very common beginner bug.
- **Why others are wrong:**
  - A) `sort()` does not return the sorted list; use `sorted(data)` if you want a new sorted list.
  - B) The old list was sorted in place, but the name `data` was then re-bound to the return value, so it no longer points at that list.
  - C) Nothing is raised: `sort()` is a perfectly valid call, it simply returns `None`.

**Source:** `mutability-and-memory.md`
</details>

---

### 6. Which pair of checks follows the recommended rules for identity (`is`) and equality (`==`)?
- [ ] A) `if result == None:` and `assert actual_rows is expected_rows`
- [ ] B) `if result is None:` and `assert actual_rows is expected_rows`
- [ ] C) `if result is None:` and `assert actual_rows == expected_rows`
- [ ] D) `if total is 257:` and `assert actual_rows == expected_rows`

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** C) `if result is None:` and `assert actual_rows == expected_rows`

**Explanation:** `==` compares values and is the right tool for assertions on data. `is` compares identity and is meant for singletons, mainly `None`, `True` and `False`.
- **Why others are wrong:**
  - A) Use `is` for the `None` singleton, and `==` for comparing contents; two separate lists with equal items are never the same object, so `is` would fail.
  - B) The first half is right, but `is` asks whether both names point at the very same list, which is almost never what a data assertion means.
  - D) The second half is right, but `is` must never be used to compare numbers or strings; small-integer caching makes it seem to work until a value like 257.

**Source:** `mutability-and-memory.md`
</details>

---

### 7. Why is `assert all(r["ok"] for r in results)` a risky check on its own in a test?
- [ ] A) If `results` is empty, `all(...)` returns `True`, so the test passes even though nothing was verified
- [ ] B) `all()` raises a `ValueError` when it receives an empty iterable
- [ ] C) `all()` only works with lists, not with generator expressions
- [ ] D) `all()` returns `None` when a result is missing the `"ok"` key

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** A) If `results` is empty, `all(...)` returns `True`, so the test passes even though nothing was verified

**Explanation:** `all([])` is `True` because no counter-example was found. Guard it with `assert results` (or `assert len(results) > 0`) when an empty result set would be a defect.
- **Why others are wrong:**
  - B) The empty-input `ValueError` belongs to `max([])`, not to `all`.
  - C) `all` accepts any iterable, and generator expressions are the recommended way to use it.
  - D) `all` always returns a `bool`; a missing key would raise `KeyError` inside the generator.

**Source:** `built-in-python-functions.md`
</details>

---

### 8. A failing test prints `Expected 'ok' but got ok`, and the two values look identical on screen. Which technique most directly reveals a hidden trailing space in the actual value?
- [ ] A) Printing `str(value)`
- [ ] B) Printing `type(value)`
- [ ] C) Printing `repr(value)`, or using `{value!r}` in an f-string
- [ ] D) Checking `isinstance(value, str)`

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** C) Printing `repr(value)`, or using `{value!r}` in an f-string

**Explanation:** `repr` shows quotes and escape characters, so `'ok '` makes the extra space visible. `str` is meant for humans and hides such details.
- **Why others are wrong:**
  - A) `str("ok ")` prints the same invisible trailing space.
  - B) `type(value)` only says `<class 'str'>`; it says nothing about the content.
  - D) `isinstance(value, str)` is `True` for both `'ok'` and `'ok '`.

**Source:** `built-in-python-functions.md`
</details>

---

### 9. `expected` holds 3 status codes but `actual` holds only 2. Which loop header makes the comparison fail loudly (with a `ValueError`) instead of silently ignoring the third code?
- [ ] A) `for exp, act in zip(expected, actual):`
- [ ] B) `for exp, act in enumerate(zip(expected, actual)):`
- [ ] C) `for exp, act in zip(expected, actual, strict=True):`
- [ ] D) `for exp, act in itertools.zip_longest(expected, actual):`

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** C) `for exp, act in zip(expected, actual, strict=True):`

**Explanation:** Since Python 3.10, `zip(..., strict=True)` raises `ValueError: zip() argument 2 is shorter than argument 1` when the lengths differ. That makes it ideal for comparing expected and actual lists in a test.
- **Why others are wrong:**
  - A) Plain `zip` stops at the shortest input without any warning, which hides the missing code.
  - B) `enumerate` only adds a counter (and would unpack the wrong values); the underlying `zip` still truncates silently.
  - D) `zip_longest` pads the shorter input with `None` instead of raising an error.

**Source:** `built-in-python-functions.md`
</details>

---

### 10. `scores` may be an empty list. Which expression returns the largest score, or `None` when the list is empty, without raising an error?
- [ ] A) `max(scores, default=None)`
- [ ] B) `max(scores)`
- [ ] C) `max(scores or 0)`
- [ ] D) `max(scores, 0)`

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** A) `max(scores, default=None)`

**Explanation:** `max` and `min` accept a keyword-only `default=` that is returned for empty input. It must be passed by name; a second positional argument is just another value to compare.
- **Why others are wrong:**
  - B) `max([])` raises `ValueError: max() iterable argument is empty`.
  - C) An empty list is falsy, so this becomes `max(0)`, which raises `TypeError` because an int is not iterable.
  - D) The `0` is treated as a second item to compare, so Python tries to compare a list with an int and raises `TypeError`; it is not a default value.

**Source:** `built-in-python-functions.md`
</details>

---

### 11. You are paused in `pdb` on the line `result = average(scores)`. You suspect the bug is inside `average`, and you want to look at its first line. Which command do you type?
- [ ] A) `n`
- [ ] B) `r`
- [ ] C) `c`
- [ ] D) `s`

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** D) `s`

**Explanation:** `s` (step) steps *into* the called function and stops on its first line. Use it when you suspect the called function; use `n` when you trust it.
- **Why others are wrong:**
  - A) `n` (next) runs the entire `average` call and stops on the next line of the current function, stepping over it.
  - B) `r` (return) runs until the current function returns, so you would skip past the code you want to inspect.
  - C) `c` (continue) runs until the next breakpoint or the end of the program.

**Source:** `debugging-techniques.md`
</details>

---

### 12. A script crashes with a traceback that ends in `KeyError: 'discount'`. What is the best way to read it?
- [ ] A) Start at the bottom: the last line gives the exception type and message, the frame just above gives the file, line and function, and the frames above that show the call chain
- [ ] B) Start at the first line, `Traceback (most recent call last):`, because it states the root cause
- [ ] C) Read only the top frame, because the first call in the chain is always where the defect lives
- [ ] D) Ignore it and add `print` statements everywhere before reading any message

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** A) Start at the bottom: the last line gives the exception type and message, the frame just above gives the file, line and function, and the frames above that show the call chain

**Explanation:** Tracebacks are read from the bottom up: *what* happened, then *where*, then *how we got there*. The crash line is not always the defect (in the lesson the data, a cart item with no `discount` key, was the real culprit).
- **Why others are wrong:**
  - B) That line is only a header; it contains no information about the error.
  - C) The top frame shows the outermost call (often `<module>`), not necessarily the cause.
  - D) Debugging starts by reading the evidence; changing code before understanding the error wastes time.

**Source:** `debugging-techniques.md`
</details>

---

### 13. A loop over 50,000 records has `if v < 0:` on line 4 of `loop.py`. You want `pdb` to pause only on records where `v < 0`. Which command do you type?
- [ ] A) `b 4`
- [ ] B) `b 4, v < 0`
- [ ] C) `tbreak 4`
- [ ] D) `unt 4`

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** B) `b 4, v < 0`

**Explanation:** `b 12, cond` is a conditional breakpoint: the program is paused only when `cond` is true. Then `p i, v` shows exactly which record triggered it.
- **Why others are wrong:**
  - A) An unconditional breakpoint stops on every iteration, so you would press `c` thousands of times.
  - C) A temporary breakpoint removes itself after the first hit, and it still has no condition.
  - D) `until` continues to a line greater than the current one (useful for leaving a loop); it does not test any condition.

**Source:** `debugging-techniques.md`
</details>

---

### 14. A function should return `90.0` for `[80, 90, 100]` but returns `89.0`, and no exception is raised. How is this problem classified, and why is it hard to find?
- [ ] A) A syntax error: Python found the mistake before running and ignored it
- [ ] B) A runtime error: an exception hidden in the traceback
- [ ] C) A rounding artefact of floating-point numbers, not a defect
- [ ] D) A logic error: Python cannot know what you meant, so only a check with an expected value (an assertion or a test) reveals it

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** D) A logic error: Python cannot know what you meant, so only a check with an expected value (an assertion or a test) reveals it

**Explanation:** The lesson's three families are syntax errors (before running), runtime errors (exceptions) and logic errors (silently wrong results). Logic errors are hardest because nothing crashes, which is why automated tests with expected values exist.
- **Why others are wrong:**
  - A) Syntax errors stop the program before it starts; here the program ran normally.
  - B) A runtime error raises an exception and prints a traceback; there is none here.
  - C) A floating-point difference would be tiny (like `0.30000000000000004`), not a full `1`; the cause is a wrong expression (`- 1`).

**Source:** `debugging-techniques.md`
</details>

---

### 15. A logger is built like this. What happens to `log.debug("config loaded")`?
```python
logger = logging.getLogger("qa")
logger.setLevel(logging.DEBUG)

console = logging.StreamHandler(sys.stdout)
console.setLevel(logging.INFO)

file_handler = logging.FileHandler("test_run.log")
file_handler.setLevel(logging.DEBUG)

logger.addHandler(console)
logger.addHandler(file_handler)
```
- [ ] A) It appears on the console and in the file
- [ ] B) It is dropped everywhere, because the default threshold is `WARNING`
- [ ] C) It is written only to `test_run.log`
- [ ] D) It appears only on the console

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** C) It is written only to `test_run.log`

**Explanation:** The logger's level is the first gate (`DEBUG` lets everything in) and each handler's level is a second gate. The console handler only passes `INFO` and above, while the file handler passes `DEBUG`.
- **Why others are wrong:**
  - A) The console handler is set to `INFO`, so it rejects the `DEBUG` record.
  - B) The default `WARNING` threshold is replaced here by `logger.setLevel(logging.DEBUG)`.
  - D) The console is the handler that filters `DEBUG` out, so the reverse is true.

**Source:** `logging.md`
</details>

---

### 16. Which log level best fits the message `Optional setting 'timeout' missing, using default 30`?
- [ ] A) `WARNING`
- [ ] B) `DEBUG`
- [ ] C) `ERROR`
- [ ] D) `CRITICAL`

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** A) `WARNING`

**Explanation:** `WARNING` means something unexpected happened or a problem is likely, but the program continues. Choosing levels honestly lets readers and tools filter the log.
- **Why others are wrong:**
  - B) `DEBUG` is for detailed diagnostics and is hidden by default; a missing setting is something a reader should notice.
  - C) `ERROR` means an operation failed; here the program continues normally with a default.
  - D) `CRITICAL` is for severe problems where the run may not be able to continue.

**Source:** `logging.md`
</details>

---

### 17. Every line in a test log appears twice. `build_logger()` calls `logging.getLogger("qa")` and then adds a `StreamHandler`, with no other checks, and two test modules each call `build_logger()`. What is the most likely cause and fix?
- [ ] A) Each `getLogger("qa")` call creates a brand-new logger, so there are two loggers; fix it by renaming one
- [ ] B) The default log format prints every record twice; fix it with a custom `format=`
- [ ] C) `getLogger("qa")` returns the same logger object both times, so a second handler is attached; fix it with a guard such as `if logger.handlers: return logger`
- [ ] D) `setLevel(logging.DEBUG)` makes each message be emitted at two levels; fix it by raising the level

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** C) `getLogger("qa")` returns the same logger object both times, so a second handler is attached; fix it with a guard such as `if logger.handlers: return logger`

**Explanation:** The classic duplicate-lines bug is adding handlers more than once to the same named logger. Guard with `if logger.handlers:` or clear handlers first. A second cause is a logger that has its own handler and also propagates to a root handler (`propagate = False` fixes that).
- **Why others are wrong:**
  - A) `getLogger` with the same name always returns the same object; that is exactly why the handler piles up.
  - B) The format only decides how a line looks, never how many lines are produced.
  - D) A record has one level; the level only decides whether it passes, not how often.

**Source:** `logging.md`
</details>

---

### 18. You want the console to show only `INFO` and above while a log file records everything down to `DEBUG`. Which setup does that?
- [ ] A) Logger level `INFO`, console handler level `INFO`, file handler level `DEBUG`
- [ ] B) Leave the logger at its default level and set only the console handler to `INFO`
- [ ] C) Call `basicConfig(level=INFO)` and then call `basicConfig(level=DEBUG)` for the file
- [ ] D) Logger level `DEBUG`, console handler level `INFO`, file handler level `DEBUG`

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** D) Logger level `DEBUG`, console handler level `INFO`, file handler level `DEBUG`

**Explanation:** The logger's level is the first gate and each handler's level is a second gate. To have different detail per destination, open the logger wide (`DEBUG`) and filter in each handler.
- **Why others are wrong:**
  - A) The logger is the first gate: a `DEBUG` record is stopped there and never reaches the file handler.
  - B) The default threshold is `WARNING`, so `INFO` and `DEBUG` are dropped before any handler sees them.
  - C) `basicConfig` is ignored once the root logger is configured (unless `force=True`), and it cannot give two destinations different levels.

**Source:** `logging.md`
</details>

---

### 19. In one `unittest` class, test A runs `{}["x"]` and test B runs `self.assertEqual(1, 2)`. How does the runner report them?
- [ ] A) Both are reported as FAIL
- [ ] B) Test A (unexpected `KeyError`) is an ERROR, and test B (false assertion) is a FAIL
- [ ] C) Test A is a FAIL, and test B is an ERROR
- [ ] D) Test A is skipped, and test B is a FAIL

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** B) Test A (unexpected `KeyError`) is an ERROR, and test B (false assertion) is a FAIL

**Explanation:** A FAIL (`F`) means an assertion was false. An ERROR (`E`) means the test raised an unexpected exception, so the check never completed.
- **Why others are wrong:**
  - A) The two outcomes are distinct: only the false assertion is a FAIL.
  - C) This reverses the definitions.
  - D) A test is skipped only when deliberately marked, for example with `@unittest.skip`.

**Source:** `introduction-to-unit-testing.md`
</details>

---

### 20. An API returns user ids as `[3, 1, 2]`, and the order is not guaranteed. The expected ids are `[1, 2, 3]`. Which assertion states the real requirement?
- [ ] A) `self.assertEqual(actual_ids, [1, 2, 3])`
- [ ] B) `self.assertCountEqual(actual_ids, [1, 2, 3])`
- [ ] C) `self.assertIn(actual_ids, [1, 2, 3])`
- [ ] D) `self.assertAlmostEqual(actual_ids, [1, 2, 3])`

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** B) `self.assertCountEqual(actual_ids, [1, 2, 3])`

**Explanation:** `assertCountEqual(a, b)` passes when both sequences contain the same elements regardless of order. Choose the assertion that expresses exactly what the requirement says.
- **Why others are wrong:**
  - A) `assertEqual` on lists also compares the order, so it would fail here.
  - C) `assertIn` checks whether one item is inside a container; it does not compare two lists.
  - D) `assertAlmostEqual` is for numbers rounded to a number of places, mainly floats, not for lists.

**Source:** `introduction-to-unit-testing.md`
</details>

---

### 21. A test class needs an expensive fake server started once, plus a fresh empty list for every test. Which pairing of hooks is correct?
- [ ] A) Create both in `setUp`
- [ ] B) Create both in `setUpClass`
- [ ] C) Start the server in `setUpClass` (a `@classmethod`) and create the list in `setUp`
- [ ] D) Start the server in `tearDown` and create the list in `setUp`

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** C) Start the server in `setUpClass` (a `@classmethod`) and create the list in `setUp`

**Explanation:** `setUpClass` runs once before all tests in the class (expensive, read-only resources) and `setUp` runs before every test (fresh, isolated data).
- **Why others are wrong:**
  - A) This works but restarts the expensive server before every single test, which breaks the 'Fast' principle.
  - B) The list would then be one shared mutable object, and tests would see each other's leftovers (order-dependent tests).
  - D) `tearDown` runs after each test and is meant for cleanup, not for starting resources.

**Source:** `introduction-to-unit-testing.md`
</details>

---

### 22. Which test breaks the "R" (Repeatable) rule of the FIRST principles?
- [ ] A) A test that asserts `get_greeting() == "Good morning"`, where `get_greeting()` reads the real system clock
- [ ] B) A test that builds its own input data inside `setUp`
- [ ] C) A test that finishes in a few milliseconds
- [ ] D) A test that compares a result with a hard-coded expected value using `assertEqual`

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** A) A test that asserts `get_greeting() == "Good morning"`, where `get_greeting()` reads the real system clock

**Explanation:** Repeatable means the same result on every run and machine, with no reliance on time, randomness, the network or leftover files. A test that depends on the current time passes in the morning and fails in the afternoon.
- **Why others are wrong:**
  - B) Fresh data created per test supports Independent and Repeatable tests; it is the recommended pattern.
  - C) Speed relates to the "F" (Fast) rule, not to repeatability.
  - D) Hard-coded expected values are recommended; they make the test Self-validating and repeatable.

**Source:** `introduction-to-unit-testing.md`
</details>

---

### 23. You are on `main` and run `git merge login-fix`. The file now contains the block below. Which statement is correct?
```
<<<<<<< HEAD
timeout = 15
=======
timeout = 45
>>>>>>> login-fix
```
- [ ] A) `timeout = 15` comes from `login-fix` and `timeout = 45` comes from `main`
- [ ] B) The upper part is the common ancestor and the lower part is the final merged result
- [ ] C) Both values come from `main`; the label only names the commit where the conflict began
- [ ] D) `timeout = 15` is "ours" (your current branch, `HEAD`) and `timeout = 45` is "theirs" (the branch being merged in, `login-fix`)

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** D) `timeout = 15` is "ours" (your current branch, `HEAD`) and `timeout = 45` is "theirs" (the branch being merged in, `login-fix`)

**Explanation:** Between `<<<<<<< HEAD` and `=======` is your current branch's version; between `=======` and `>>>>>>> login-fix` is the incoming branch's version. You resolve the conflict by editing the file so it contains the correct final content and no marker lines.
- **Why others are wrong:**
  - A) This reverses the two sides (and it would be reversed again during a rebase, which is why you must stay careful).
  - B) The base version is only shown in diff3 style, in a separate `|||||||` section.
  - C) The two sides are different versions, one from each branch.

**Source:** `git-merge-conflicts-and-resolution.md`
</details>

---

### 24. During `git rebase main` you fix a conflict in `app.py` and run `git add app.py`. Which command finishes this step of the rebase?
- [ ] A) `git commit`
- [ ] B) `git rebase --continue`
- [ ] C) `git rebase --abort`
- [ ] D) `git push --force`

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** B) `git rebase --continue`

**Explanation:** A rebase replays your commits one by one, so after resolving and adding you run `git rebase --continue` (or `--skip` / `--abort`). In a rebase "ours" and "theirs" are also swapped compared with a merge.
- **Why others are wrong:**
  - A) That is the finishing command for a merge; during a rebase you continue the rebase instead.
  - C) `--abort` cancels the whole rebase and returns you to the state before it started.
  - D) Pushing does not finish a rebase step, and force-pushing a shared branch can overwrite colleagues' commits.

**Source:** `git-merge-conflicts-and-resolution.md`
</details>

---

### 25. You are halfway through a conflicted merge, nothing has been committed, and you realise you merged the wrong branch. What is the safest way back?
- [ ] A) `git push --force`
- [ ] B) Delete the project folder and clone again
- [ ] C) Remove the markers quickly and run `git commit`
- [ ] D) `git merge --abort`

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** D) `git merge --abort`

**Explanation:** `git merge --abort` restores the state from before the merge started. It is your safety net while a conflict is unresolved, and you can start the merge again later.
- **Why others are wrong:**
  - A) That does not touch the local half-finished merge and could overwrite colleagues' commits on the remote.
  - B) You would lose any unpushed work; `git merge --abort` is the safe way out.
  - C) That would record a merge you did not want (and possibly a broken one) in history.

**Source:** `git-merge-conflicts-and-resolution.md`
</details>

---

### 26. Alice edits line 2 of `settings.py` on her branch, and Bob edits line 40 of the same file on his. Each commits, then Alice merges Bob's branch. What happens?
- [ ] A) A conflict, because both branches modified the same file
- [ ] B) Git keeps Alice's file and silently drops Bob's change
- [ ] C) Git merges automatically with no conflict, because the two changes are in different, non-adjacent regions
- [ ] D) A fast-forward, so no merge commit is created

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** C) Git merges automatically with no conflict, because the two changes are in different, non-adjacent regions

**Explanation:** In a three-way merge, a region changed by only one side is taken from that side. Only changes to the same (or adjacent) lines made differently by both sides produce a conflict.
- **Why others are wrong:**
  - A) Conflicts depend on overlapping lines, not on the file name; Git compares each region with the common ancestor.
  - B) Git applies a change that only one side made; it never drops it without telling you.
  - D) A fast-forward is possible only when one branch has no new commits; here both do, so it is a true three-way merge.

**Source:** `git-merge-conflicts-and-resolution.md`
</details>

---

### 27. After editing a conflicted file, which command reports any leftover marker lines such as `<<<<<<<` that you forgot to delete?
- [ ] A) `git diff --check`
- [ ] B) `git status -s`
- [ ] C) `git log --merge`
- [ ] D) `git ls-files -u`

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** A) `git diff --check`

**Explanation:** `git diff --check` warns about leftover conflict markers (and whitespace problems). A `grep` for `<<<<<<<` does the same job. Committing a file with markers inside puts broken code in the repository.
- **Why others are wrong:**
  - B) It keeps showing `UU` until you `git add` the file, whether or not markers are still inside.
  - C) It lists the commits involved in the conflict; it does not scan the file contents for markers.
  - D) It lists unmerged index entries (the base, ours and theirs versions), not leftover text in your working file.

**Source:** `git-merge-conflicts-and-resolution.md`
</details>

---

## Part 2: True / False

### 28. True or False: A function must declare `global results` before it can call `results.append(value)` on a module-level list.
- [ ] A) True
- [ ] B) False

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** B) False

**Explanation:** `append` mutates the existing list; it does not rebind the name `results`. `global` is only needed when you want to assign the name to a new object (for example `results = []`).

**Source:** `scope-and-namespaces.md`
</details>

---

### 29. True or False: After `squares = [n * n for n in range(3)]`, the name `n` is still available and equals `2`.
- [ ] A) True
- [ ] B) False

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** B) False

**Explanation:** Comprehensions have their own scope, so their loop variable does not leak and `print(n)` raises `NameError`. A plain `for` loop is different: its variable survives after the loop ends.

**Source:** `scope-and-namespaces.md`
</details>

---

### 30. True or False: A tuple that contains a list, such as `(1, [2, 3])`, cannot be used as a dictionary key.
- [ ] A) True
- [ ] B) False

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** A) True

**Explanation:** A dictionary key must be hashable, and a tuple is only hashable if everything inside it is. Because the list is mutable and unhashable, using the tuple as a key raises `TypeError: unhashable type: 'list'`.

**Source:** `mutability-and-memory.md`
</details>

---

### 31. True or False: `bool("False")` evaluates to `True`.
- [ ] A) True
- [ ] B) False

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** A) True

**Explanation:** Any non-empty string is truthy, regardless of what it says. When reading booleans from CSV or JSON text, compare explicitly, for example `value.lower() == "true"`.

**Source:** `built-in-python-functions.md`
</details>

---

### 32. True or False: `isinstance(True, int)` evaluates to `True`.
- [ ] A) True
- [ ] B) False

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** A) True

**Explanation:** `bool` is a subclass of `int`, so `True` counts as an integer. To reject booleans when validating a count, check `isinstance(x, int) and not isinstance(x, bool)`.

**Source:** `built-in-python-functions.md`
</details>

---

### 33. True or False: `assert` statements are a reliable way to validate user input, because they always run.
- [ ] A) True
- [ ] B) False

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** B) False

**Explanation:** Assertions can be switched off with `python -O`, so they must not be the only protection for user or file data. Use them to catch programmer mistakes and raise proper exceptions for input validation.

**Source:** `debugging-techniques.md`
</details>

---

### 34. True or False: With no logging configuration at all, `logging.info("started")` prints `INFO:root:started` to the console.
- [ ] A) True
- [ ] B) False

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** B) False

**Explanation:** The default threshold is `WARNING`, so `INFO` and `DEBUG` messages are dropped. Only `logging.warning(...)`, `logging.error(...)` and `logging.critical(...)` appear until you lower the level, for example with `logging.basicConfig(level=logging.INFO)`.

**Source:** `logging.md`
</details>

---

### 35. True or False: `logger.debug(f"payload={payload}")` avoids the cost of building the message when `DEBUG` is disabled.
- [ ] A) True
- [ ] B) False

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** B) False

**Explanation:** The f-string is evaluated before `debug` is even called, so the work is done regardless of the level. Lazy formatting works only when you pass arguments separately: `logger.debug("payload=%s", payload)`.

**Source:** `logging.md`
</details>

---

### 36. True or False: A `unittest` test method that contains no assertions still passes, so it verifies nothing.
- [ ] A) True
- [ ] B) False

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** A) True

**Explanation:** A test only fails when an assertion is false or an exception is raised. The lesson lists "tests with no assertion" as a common mistake: they always pass and check nothing, so every test must assert something.

**Source:** `introduction-to-unit-testing.md`
</details>

---

### 37. True or False: If one input inside a `subTest` loop fails, the remaining inputs in that loop are never checked.
- [ ] A) True
- [ ] B) False

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** B) False

**Explanation:** `subTest` exists precisely so that every input is checked and each failing input is reported separately with its parameters. Without `subTest`, the first failing assertion would abort the test method.

**Source:** `introduction-to-unit-testing.md`
</details>

---

### 38. True or False: When `git push` is rejected with `! [rejected] main -> main (fetch first)`, it means a merge conflict has already occurred and you must edit conflict markers in your files before doing anything else.
- [ ] A) True
- [ ] B) False

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** B) False

**Explanation:** A rejected push only means the histories have diverged: the remote has commits you do not have. Git is protecting the shared branch. You pull (merge), and only if that reports a `CONFLICT` do you resolve markers, then commit and push.

**Source:** `git-merge-conflicts-and-resolution.md`
</details>

---

### 39. True or False: During a rebase, "ours" refers to your own commit that is being replayed.
- [ ] A) True
- [ ] B) False

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** B) False

**Explanation:** It is the other way round: in a rebase "ours" (`HEAD`) is the branch you are rebasing onto, and "theirs" is your own commit being replayed. In a merge, "ours" is your current branch.

**Source:** `git-merge-conflicts-and-resolution.md`
</details>

---

## Part 3: Code Prediction

All outputs below were produced by running the code with Python 3 as a script (`python3 file.py`). Where a snippet logs messages, the log lines are written to the console.

### 40. What does this script print?
```python
checks = [lambda: i + 1 for i in range(3)]
print([check() for check in checks])

fixed = [lambda i=i: i + 1 for i in range(3)]
print([check() for check in fixed])
```
- [ ] A) `[1, 2, 3]` then `[1, 2, 3]`
- [ ] B) `[1, 2, 3]` then `[3, 3, 3]`
- [ ] C) `[3, 3, 3]` then `[1, 2, 3]`
- [ ] D) `[3, 3, 3]` then `[3, 3, 3]`

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** C) `[3, 3, 3]` then `[1, 2, 3]`

**Explanation:** Closures capture the variable `i`, not its value at creation time. When the first list of lambdas is called, the loop has finished and `i` is `2`, so each returns `3`. The default argument `i=i` is evaluated at definition time and freezes each value.
- **Why others are wrong:**
  - A) That would be correct only if the lambdas captured values, which they do not unless you use a default argument.
  - B) The two outputs are swapped.
  - D) The default argument `i=i` does freeze each value in the second list.

**Source:** `scope-and-namespaces.md`
</details>

---

### 41. What does this script print?
```python
def make_counter():
    count = 0

    def increment():
        nonlocal count
        count += 1
        return count

    return increment

a = make_counter()
b = make_counter()
print(a(), a(), b(), a())
```
- [ ] A) `1 2 3 4`
- [ ] B) `1 2 1 2`
- [ ] C) `1 1 1 1`
- [ ] D) `1 2 1 3`

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** D) `1 2 1 3`

**Explanation:** `a` and `b` are two independent closures, each with its own `count` cell. `a()` returns 1, 2, then (after `b()` returns 1) 3.
- **Why others are wrong:**
  - A) Each `make_counter()` call creates its own enclosing namespace, so `b` has a separate `count` and starts at `1`.
  - B) `a`'s count is not reset by the call to `b()`; its third call returns `3`.
  - C) Because of `nonlocal`, `count += 1` rebinds the enclosing variable, so the state persists between calls (without `nonlocal` you would get `UnboundLocalError`).

**Source:** `scope-and-namespaces.md`
</details>

---

### 42. What does this script print (one list per line)?
```python
def add_tag(tag, tags=[]):
    tags.append(tag)
    return tags

print(add_tag("a"))
print(add_tag("b"))
print(add_tag("c", []))
print(add_tag("d"))
```
- [ ] A) `['a']`, `['b']`, `['c']`, `['d']`
- [ ] B) `['a']`, `['a', 'b']`, `['a', 'b', 'c']`, `['a', 'b', 'c', 'd']`
- [ ] C) `['a']`, `['a', 'b']`, `['c']`, `['d']`
- [ ] D) `['a']`, `['a', 'b']`, `['c']`, `['a', 'b', 'd']`

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** D) `['a']`, `['a', 'b']`, `['c']`, `['a', 'b', 'd']`

**Explanation:** The default `[]` is created once, when `def` runs, and is shared by every call that omits `tags`. Calls 1, 2 and 4 all append to that same list. Call 3 passes its own fresh list, so the shared one is untouched.
- **Why others are wrong:**
  - A) That is what the `tags=None` fix would print; with a mutable default the calls leak into each other.
  - B) Call 3 supplies its own list, so `'c'` never goes into the shared default.
  - C) The last call uses the shared default again, which still holds `'a'` and `'b'`.

**Source:** `mutability-and-memory.md`
</details>

---

### 43. What does this script print (one list per line)?
```python
a = [1, 2, 3]
b = a
b += [4]
c = a
c = c + [5]
print(a)
print(b)
print(c)
```
- [ ] A) `[1, 2, 3, 4]`, `[1, 2, 3, 4]`, `[1, 2, 3, 4, 5]`
- [ ] B) `[1, 2, 3]`, `[1, 2, 3, 4]`, `[1, 2, 3, 4, 5]`
- [ ] C) `[1, 2, 3, 4, 5]`, `[1, 2, 3, 4, 5]`, `[1, 2, 3, 4, 5]`
- [ ] D) `[1, 2, 3, 4]`, `[1, 2, 3, 4]`, `[1, 2, 3, 5]`

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** A) `[1, 2, 3, 4]`, `[1, 2, 3, 4]`, `[1, 2, 3, 4, 5]`

**Explanation:** For lists, `b += [4]` is an in-place operation, so `a` and `b` (the same object) both see the `4`. `c = c + [5]` builds a new list and rebinds `c`, leaving `a` alone, but that new list was built from `[1, 2, 3, 4]`.
- **Why others are wrong:**
  - B) This treats `b += [4]` as if it created a new list; for mutable lists it modifies the shared one.
  - C) `c + [5]` creates a new list, so `a` and `b` never receive the `5`.
  - D) `c` starts as the already-extended list `[1, 2, 3, 4]`, so the new list is `[1, 2, 3, 4, 5]`.

**Source:** `mutability-and-memory.md`
</details>

---

### 44. What does this script print?
```python
t = (1, [2, 3])
try:
    t[1] += [5]
except TypeError as e:
    print(e)
print(t)
```
- [ ] A) `'tuple' object does not support item assignment`, then `(1, [2, 3, 5])`
- [ ] B) `'tuple' object does not support item assignment`, then `(1, [2, 3])`
- [ ] C) Only `(1, [2, 3, 5])`, with no error message
- [ ] D) `'tuple' object does not support item assignment`, then `(1, [2, 3, 5, 5])`

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** A) `'tuple' object does not support item assignment`, then `(1, [2, 3, 5])`

**Explanation:** `t[1] += [5]` first extends the inner list in place (this succeeds), then tries to store the result back into the tuple (this fails). The tuple's slots are immutable, but the list inside is not.
- **Why others are wrong:**
  - B) The list is extended in place first and stays extended; only the step that assigns the result back into the tuple slot fails.
  - C) `+=` on `t[1]` ends with an assignment into the tuple, which raises `TypeError`, so the message is printed.
  - D) The in-place extend runs only once; the failed assignment does not repeat it.

**Source:** `mutability-and-memory.md`
</details>

---

### 45. What does this script print?
```python
print(all([]), any([]))
print(round(2.5), round(3.5))
print(int(-7.9), bool("False"))
```
- [ ] A) `True False`, `3 4`, `-7 True`
- [ ] B) `True False`, `2 4`, `-7 True`
- [ ] C) `True False`, `2 4`, `-7 False`
- [ ] D) `False True`, `2 4`, `-8 True`

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** B) `True False`, `2 4`, `-7 True`

**Explanation:** `all([])` is `True` and `any([])` is `False`. `round` uses banker's rounding (exact halves go to the nearest even number), giving `2` and `4`. `int()` truncates toward zero, so `int(-7.9)` is `-7`, and `bool("False")` is `True` because the string is non-empty.
- **Why others are wrong:**
  - A) `round(2.5)` is `2`, not `3`; Python does not always round halves up.
  - C) A non-empty string is truthy, so `bool("False")` is `True`.
  - D) `all([])`/`any([])` are the other way round, and `int()` truncates toward zero rather than flooring.

**Source:** `built-in-python-functions.md`
</details>

---

### 46. What does this script print (one line per `print`)?
```python
m = map(str, [1, 2])
print(list(m))
print(list(m))
print(isinstance(True, int), type(True) == int)
print(max([], default=None), next(iter([]), "none"))
```
- [ ] A) `['1', '2']`, `['1', '2']`, `True True`, `None none`
- [ ] B) `['1', '2']`, `[]`, `True False`, `None none`
- [ ] C) `['1', '2']`, `[]`, `True False`, then a `ValueError` on the last line
- [ ] D) `[1, 2]`, `[]`, `False False`, `None none`

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** B) `['1', '2']`, `[]`, `True False`, `None none`

**Explanation:** `map` is lazy and can be consumed only once. `isinstance` respects inheritance (`bool` is an `int`) while `type(...) ==` does not. `max(..., default=...)` and `next(it, default)` both avoid errors on empty input.
- **Why others are wrong:**
  - A) `map` returns a one-shot iterator that is used up after the first `list`, and `type(True)` is `bool`, not `int`, so `type(True) == int` is `False`.
  - C) `default=None` prevents the `ValueError` from `max([])`, and `next(..., "none")` returns the default instead of raising `StopIteration`.
  - D) `map(str, ...)` yields strings, not ints, and `isinstance(True, int)` is `True` because `bool` subclasses `int`.

**Source:** `built-in-python-functions.md`
</details>

---

### 47. This function should double every number. What does the script print (one value per line)?
```python
def double_all(numbers):
    result = []
    for n in numbers:
        result.append(n * 2)
        return result

print(double_all([1, 2, 3]))
print(double_all([]))
```
- [ ] A) `[2, 4, 6]` then `[]`
- [ ] B) `[2]` then `None`
- [ ] C) `[2]` then `[]`
- [ ] D) `[2, 4, 6]` then `None`

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** B) `[2]` then `None`

**Explanation:** `return result` is indented inside the `for` loop, so the function returns after the first item (`[2]`). With an empty list the loop never runs and Python implicitly returns `None`. This is the lesson's `bug1.py` example.
- **Why others are wrong:**
  - A) That is what the function would print if `return result` were dedented to align with `for`.
  - C) For an empty list the loop body never runs, so the function reaches the end without a `return` and gives back `None`, not `[]`.
  - D) The `return` sits inside the loop, so the function exits after the first element.

**Source:** `debugging-techniques.md`
</details>

---

### 48. What appears on the console when this script runs?
```python
import logging

logging.basicConfig(level=logging.INFO, format="%(levelname)s:%(name)s:%(message)s")
logging.getLogger("qa").setLevel(logging.ERROR)

logging.getLogger("qa.api").info("one")
logging.getLogger("qa.api").error("two")
logging.getLogger("other").info("three")
logging.getLogger("other").debug("four")
```
- [ ] A) Only `ERROR:qa.api:two`
- [ ] B) `INFO:qa.api:one`, `ERROR:qa.api:two`, `INFO:other:three`
- [ ] C) `ERROR:qa.api:two` and `INFO:other:three`
- [ ] D) `ERROR:qa.api:two`, `INFO:other:three` and `DEBUG:other:four`

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** C) `ERROR:qa.api:two` and `INFO:other:three`

**Explanation:** `qa.api` has no level of its own, so it inherits `ERROR` from its parent `qa`: its `info` is dropped and its `error` is shown. `other` inherits `INFO` from the root logger, so `info` is shown and `debug` is dropped.
- **Why others are wrong:**
  - A) The `other` logger is not a child of `qa`; it uses the root's `INFO` threshold, so `three` is shown.
  - B) `INFO:qa.api:one` is silenced because `qa.api` inherits `ERROR` from `qa`.
  - D) `DEBUG` is below the root's `INFO` threshold, so `four` is dropped.

**Source:** `logging.md`
</details>

---

### 49. What appears on the console when this script runs?
```python
import logging

logging.basicConfig(level=logging.INFO, format="%(levelname)s:%(message)s")

class Big:
    def __repr__(self):
        print("(repr ran)")
        return "Big()"

log = logging.getLogger("x")
log.debug("v: %r", Big())
log.info("v: %r", Big())
```
- [ ] A) `(repr ran)` twice, followed by `INFO:v: Big()`
- [ ] B) Only `INFO:v: Big()`
- [ ] C) `(repr ran)` followed by `INFO:v: Big()`
- [ ] D) `(repr ran)`, `DEBUG:v: Big()` and `INFO:v: Big()`

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** C) `(repr ran)` followed by `INFO:v: Big()`

**Explanation:** Passing arguments separately (`"v: %r", Big()`) defers formatting. The `DEBUG` call is below the `INFO` threshold, so `__repr__` is not executed for it, but it runs once for the `INFO` call.
- **Why others are wrong:**
  - A) With lazy `%r` arguments the message is rendered only if the record is emitted; the disabled `DEBUG` call never calls `__repr__`.
  - B) To build the text of the emitted `INFO` message, Python must call `__repr__`, which prints `(repr ran)`.
  - D) The threshold is `INFO`, so the `DEBUG` record is dropped.

**Source:** `logging.md`
</details>

---

### 50. What appears on the console when this script runs (one line per message)?
```python
import logging

logging.warning("first")
logging.basicConfig(level=logging.DEBUG, format="%(levelname)s %(message)s")
logging.debug("a")
logging.basicConfig(level=logging.DEBUG, format="%(levelname)s %(message)s", force=True)
logging.debug("b")
logging.info("c")
```
- [ ] A) `WARNING:root:first`, `DEBUG b`, `INFO c`
- [ ] B) `WARNING:root:first`, `DEBUG a`, `DEBUG b`, `INFO c`
- [ ] C) `WARNING:root:first`, `DEBUG b`
- [ ] D) `WARNING first`, `DEBUG a`, `DEBUG b`, `INFO c`

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** A) `WARNING:root:first`, `DEBUG b`, `INFO c`

**Explanation:** A module-level call such as `logging.warning` auto-configures the root logger, so the first `basicConfig` silently does nothing. Only the call with `force=True` replaces the configuration.
- **Why others are wrong:**
  - B) The first `basicConfig` is ignored because `logging.warning(...)` already configured the root logger, so `a` is dropped.
  - C) After `force=True` the level is `DEBUG`, which also lets `INFO` through, so `c` is shown.
  - D) The first line was written by the automatic default setup, whose format is `LEVEL:NAME:MESSAGE`, and `a` is still dropped.

**Source:** `logging.md`
</details>

---

### 51. Tests in a class run in alphabetical order. What are the first line (the progress characters) and the last line printed by this script?
```python
import sys
import unittest

class T(unittest.TestCase):
    def test_a(self):
        self.assertEqual(1 + 1, 2)

    def test_b(self):
        {}["x"]

    def test_c(self):
        self.assertEqual([1, 2], [2, 1])

    @unittest.skip("later")
    def test_d(self):
        self.fail("never runs")

    @unittest.expectedFailure
    def test_e(self):
        self.assertEqual(1, 2)

suite = unittest.defaultTestLoader.loadTestsFromTestCase(T)
unittest.TextTestRunner(stream=sys.stdout, verbosity=1).run(suite)
```
- [ ] A) First line `.FEsx`, last line `FAILED (failures=1, errors=1, skipped=1, expected failures=1)`
- [ ] B) First line `.EFss`, last line `FAILED (failures=1, errors=1, skipped=1, expected failures=1)`
- [ ] C) First line `.EFsx`, last line `FAILED (failures=1, errors=1, skipped=1, expected failures=1)`
- [ ] D) First line `.EFsx`, last line `OK (skipped=1, expected failures=1)`

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** C) First line `.EFsx`, last line `FAILED (failures=1, errors=1, skipped=1, expected failures=1)`

**Explanation:** `.` passed (`test_a`), `E` error (`test_b`: unexpected `KeyError`), `F` failure (`test_c`: false assertion), `s` skipped (`test_d`), `x` expected failure (`test_e`). Any failure or error makes the final summary `FAILED`.
- **Why others are wrong:**
  - A) `F` and `E` are swapped: `test_b` raises an unexpected `KeyError` (E), and `test_c` has a false assertion (F).
  - B) An expected failure is shown as `x`; only `test_d`, marked `@unittest.skip`, is shown as `s`.
  - D) `OK` appears only when nothing failed or errored, but `test_b` errored and `test_c` failed.

**Source:** `introduction-to-unit-testing.md`
</details>

---

### 52. What does this script print, in order (one word per line, shown here separated by commas)?
```python
import io
import unittest

class T(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        print("class-up")

    def setUp(self):
        print("up")

    def tearDown(self):
        print("down")

    @classmethod
    def tearDownClass(cls):
        print("class-down")

    def test_a(self):
        print("A")

    def test_b(self):
        print("B")

suite = unittest.defaultTestLoader.loadTestsFromTestCase(T)
unittest.TextTestRunner(stream=io.StringIO()).run(suite)
```
- [ ] A) `up, A, down, up, B, down`
- [ ] B) `class-up, up, up, A, B, down, down, class-down`
- [ ] C) `class-up, up, A, B, down, class-down`
- [ ] D) `class-up, up, A, down, up, B, down, class-down`

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** D) `class-up, up, A, down, up, B, down, class-down`

**Explanation:** `setUpClass` and `tearDownClass` run once per class, while `setUp` and `tearDown` run around every test method (alphabetically `test_a` then `test_b`). This is how each test gets a fresh start.
- **Why others are wrong:**
  - A) The class-level hooks also run: `setUpClass` once before the first test and `tearDownClass` once after the last.
  - B) `setUp` and `tearDown` wrap each test method separately; they do not run twice in a row around all tests.
  - C) `setUp` and `tearDown` run once per test, not once per class.

**Source:** `introduction-to-unit-testing.md`
</details>

---

## Part 4: Fill-in-the-Blank

### 53. Inside a nested function, the statement `________ count` lets `count += 1` rebind the variable that belongs to the enclosing function instead of creating a new local.

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** `nonlocal`

**Explanation:** `nonlocal` refers to the nearest enclosing function's variable, which must already exist. Without it, `count += 1` raises `UnboundLocalError`.

**Source:** `scope-and-namespaces.md`
</details>

---

### 54. The standard fix for the mutable default argument bug is to write `def add_item(item, bucket=________):` and then create the list inside the function when `bucket` is that value.

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** `None`

**Explanation:** A default is evaluated once when `def` runs, so a `[]` default is shared by every call. A `None` sentinel plus `if bucket is None: bucket = []` gives each call a fresh list.

**Source:** `mutability-and-memory.md`
</details>

---

### 55. Because `0.1 + 0.2 == 0.3` is `False`, calculated floats should be compared with `math.________(0.1 + 0.2, 0.3)`, which returns `True`.

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** `isclose`

**Explanation:** Floats are stored in binary, so `0.1 + 0.2` is `0.30000000000000004`. `math.isclose` accepts values that are close enough (an alternative is `abs(a - b) < 1e-9`).

**Source:** `built-in-python-functions.md`
</details>

---

### 56. To debug a crash after the fact, run `python -m pdb -c ________ cart.py`. The program runs until it raises an uncaught exception, then `pdb` opens at the crash site with all variables still available (post-mortem debugging).

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** `continue`

**Explanation:** The `-c` option runs a `pdb` command at startup; `continue` lets the script run until it crashes, and then the debugger opens at the failing line so you can inspect values with `p`.

**Source:** `debugging-techniques.md`
</details>

---

### 57. At the `(Pdb)` prompt, typing `________` (short for "where") prints the call stack, showing how execution got to the current line.

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** `w`

**Explanation:** `w` shows the chain of calls (for example `<module>` to `main` to `average`). Then `u` moves up a frame and `d` moves back down so you can inspect the caller's variables.

**Source:** `debugging-techniques.md`
</details>

---

### 58. Inside an `except` block, calling `logger.________("calc failed")` logs the message at `ERROR` level and also appends the full traceback.

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** `exception` (that is, `logger.exception(...)`)

**Explanation:** `logger.exception` is equivalent to `logger.error("...", exc_info=True)`. It should be called only from inside an `except` block, where there is a current exception to record.

**Source:** `logging.md`
</details>

---

### 59. Floating-point results such as `0.1 + 0.2` should be checked in `unittest` with `self.________(add(0.1, 0.2), 0.3)`, which compares the values after rounding to 7 decimal places by default.

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** `assertAlmostEqual`

**Explanation:** `0.1 + 0.2` is `0.30000000000000004`, so `assertEqual` would fail because of floating-point rounding noise. `assertAlmostEqual` accepts values that match to 7 decimal places (or within `delta=`).

**Source:** `introduction-to-unit-testing.md`
</details>

---

### 60. To run only the unit tests whose names contain the text `divide`, use `python -m unittest ________ divide`.

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** `-k`

**Explanation:** The `-k` option selects tests by a name substring. Other useful options are `-v` (verbose), `-f` (fail fast) and `-b` (buffer output).

**Source:** `introduction-to-unit-testing.md`
</details>

---

## Part 5: Scenario-Based

### 61. A test helper builds configs like this. Test 1 appends `"c"` to `cfg["hosts"]`, and Test 2 (which should start clean) then sees `['a', 'b', 'c']`. What is the best fix?
```python
import copy

DEFAULT_CONFIG = {"retries": 3, "hosts": ["a", "b"]}

def make_config():
    cfg = DEFAULT_CONFIG.copy()
    return cfg
```
- [ ] A) Use `cfg = dict(DEFAULT_CONFIG)`
- [ ] B) Use `cfg = DEFAULT_CONFIG` and treat it as read-only by convention
- [ ] C) Reorder the tests so Test 2 runs before Test 1
- [ ] D) Use `cfg = copy.deepcopy(DEFAULT_CONFIG)` so the nested `hosts` list is copied as well

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** D) Use `cfg = copy.deepcopy(DEFAULT_CONFIG)` so the nested `hosts` list is copied as well

**Explanation:** `.copy()` makes a new outer dict but shares nested objects, so one test's change leaks into the next. `copy.deepcopy` gives each test fully independent data, the safe per-test pattern.
- **Why others are wrong:**
  - A) `dict(...)` is also a shallow copy, so the inner `hosts` list is still shared.
  - B) That is an alias, not a copy; the first test that mutates it corrupts the constant.
  - C) Reordering only hides the symptom; the tests stay order-dependent, which breaks test isolation.

**Source:** `mutability-and-memory.md`
</details>

---

### 62. After a teammate refactors `apply_discount`, your test `test_discount` fails with "expected 12.0, got 13.5". A colleague says: "Just change the expected value to 13.5 so the build goes green." What should you do first?
- [ ] A) Change the expected value to 13.5, since the code is the newest version
- [ ] B) Check the requirement (or ask its owner) and reproduce the calculation to prove whether the code or the test is wrong, then fix that side
- [ ] C) Wrap the assertion in `try/except AssertionError: pass`
- [ ] D) Re-run the test until it passes

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** B) Check the requirement (or ask its owner) and reproduce the calculation to prove whether the code or the test is wrong, then fix that side

**Explanation:** Debugging is evidence-based: reproduce, read the requirement, decide whether the product, the test, the data or the environment is at fault, and only then change code or expectations (ideally in a clearly described commit).
- **Why others are wrong:**
  - A) Changing an expectation just to turn a test green can hide a real defect; first prove which side is wrong.
  - C) Swallowing the failure removes the evidence and the check, so the defect would go unnoticed.
  - D) A deterministic failure will not go away by re-running; re-running until green is also the wrong response to flaky tests.

**Source:** `debugging-techniques.md`
</details>

---

### 63. Your team's `unittest` suite has these two tests. Run on its own, `test_cart_starts_empty` passes. Run as a whole file, it fails with `AssertionError: 1 != 0`. What is the root cause and the best fix?
```python
class TestCart(unittest.TestCase):
    cart = []                       # class-level attribute

    def test_add_item(self):
        self.cart.append("pen")
        self.assertEqual(len(self.cart), 1)

    def test_cart_starts_empty(self):
        self.assertEqual(len(self.cart), 0)
```
- [ ] A) Rename the tests so `test_cart_starts_empty` runs first
- [ ] B) Change the expected value in `test_cart_starts_empty` from `0` to `1`
- [ ] C) `cart` is one mutable list shared by every test; create it in `setUp` (`self.cart = []`) so each test starts clean
- [ ] D) Mark `test_cart_starts_empty` with `@unittest.skip` until the problem goes away

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** C) `cart` is one mutable list shared by every test; create it in `setUp` (`self.cart = []`) so each test starts clean

**Explanation:** Tests in a class run in alphabetical order, so `test_add_item` runs first and leaves `"pen"` in the shared list. Tests must be independent (the "I" in FIRST), and `setUp` runs before every test method to give each one fresh data. It is the same shared-state problem as the mutable default argument.
- **Why others are wrong:**
  - A) Renaming only changes which test runs first; the tests remain order-dependent, so the defect is hidden, not fixed.
  - B) Changing the expected value just to turn the test green hides the real defect; the test's expectation was right.
  - D) Skipping removes the check instead of fixing the shared state.

**Source:** `introduction-to-unit-testing.md`
</details>

---

### 64. You merged `origin/main` into your branch and the shared test-data file `users.json` now looks like this. Which resolution is correct?
```
[
  {"id": 1, "user": "ann"},
<<<<<<< HEAD
  {"id": 2, "user": "bob"}
=======
  {"id": 3, "user": "cara"}
>>>>>>> origin/main
]
```
- [ ] A) Delete only the three marker lines, leaving both objects with no comma between them
- [ ] B) Keep both objects, add a comma after the `bob` entry, remove all marker lines, then check the file loads with `json.load`
- [ ] C) Keep only the `bob` entry (`git checkout --ours`), because your side is always right
- [ ] D) Keep the markers in the file and commit, so teammates can see both versions

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** B) Keep both objects, add a comma after the `bob` entry, remove all marker lines, then check the file loads with `json.load`

**Explanation:** Both teammates added a different user, so both rows belong in the file. Because JSON needs commas between items, you must fix the punctuation yourself; loading the file with `json.load` raises `JSONDecodeError` if a comma is wrong. Then `git add`, `git commit`.
- **Why others are wrong:**
  - A) Without the comma the file is invalid JSON, and the loader will crash.
  - C) Taking one side blindly would erase `cara`, a colleague's work.
  - D) Committing marker lines puts broken content in the repository; use `git diff --check` to catch leftover markers.

**Source:** `git-merge-conflicts-and-resolution.md`
</details>

---

### 65. After `git pull`, `requirements.txt` has this conflict. Both sides pin `requests`. Which resolution is best?
```
<<<<<<< HEAD
requests==2.31.0
=======
requests==2.32.3
>>>>>>> origin/main
```
- [ ] A) Pick one version deliberately (after checking with the teammate), remove all marker lines, reinstall in a clean virtual environment, run the tests, then `git add` and `git commit`
- [ ] B) Keep both lines and delete only the marker lines
- [ ] C) Run `git checkout --theirs requirements.txt` without looking, because the remote is always newer
- [ ] D) Commit the file as it is so everyone can see both versions

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** A) Pick one version deliberately (after checking with the teammate), remove all marker lines, reinstall in a clean virtual environment, run the tests, then `git add` and `git commit`

**Explanation:** For `requirements.txt`, independent additions are usually both kept, but two pins of the *same* package require a deliberate choice. After resolving, rebuild the environment and run the tests, because a marker-free merge can still be broken.
- **Why others are wrong:**
  - B) Two different pins of the same package cannot both be installed, so installation would fail or be ambiguous.
  - C) Blindly taking one side can drop other changes in the file; read both sides and decide on purpose.
  - D) Marker lines inside `requirements.txt` make `pip install -r` fail, and broken content lands in the repository.

**Source:** `git-merge-conflicts-and-resolution.md`
</details>

---

## Answer Key

| Q# | Answer | Q# | Answer | Q# | Answer |
|----|--------|----|--------|----|--------|
| 1 | B | 23 | D | 45 | B |
| 2 | B | 24 | B | 46 | B |
| 3 | A | 25 | D | 47 | B |
| 4 | D | 26 | C | 48 | C |
| 5 | D | 27 | A | 49 | C |
| 6 | C | 28 | B (False) | 50 | A |
| 7 | A | 29 | B (False) | 51 | C |
| 8 | C | 30 | A (True) | 52 | D |
| 9 | C | 31 | A (True) | 53 | `nonlocal` |
| 10 | A | 32 | A (True) | 54 | `None` |
| 11 | D | 33 | B (False) | 55 | `isclose` |
| 12 | A | 34 | B (False) | 56 | `continue` |
| 13 | B | 35 | B (False) | 57 | `w` |
| 14 | D | 36 | A (True) | 58 | `exception` |
| 15 | C | 37 | B (False) | 59 | `assertAlmostEqual` |
| 16 | A | 38 | B (False) | 60 | `-k` |
| 17 | C | 39 | B (False) | 61 | D |
| 18 | D | 40 | C | 62 | B |
| 19 | B | 41 | D | 63 | C |
| 20 | B | 42 | D | 64 | B |
| 21 | C | 43 | A | 65 | A |
| 22 | A | 44 | A |  |  |
