# Interview Questions: Week 2 — Wednesday: Python Debugging & Testing Foundations

**Scope:** scope and namespaces, mutability and memory, built-in Python functions, debugging techniques, logging, introduction to unit testing (`unittest`) and Git merge conflicts and resolution.
**Total:** 20 questions (14 Beginner, 5 Intermediate, 1 Advanced).

---

## Beginner (Foundational)

### Q1: What is the difference between a namespace and a scope, and what is the LEGB rule?
**Keywords:** namespace, scope, Local, Enclosing, Global, Built-in
<details>
<summary>Click to Reveal Answer</summary>

A namespace is where names are stored (think of a dictionary mapping names to objects), while a scope is the region of the program text in which a namespace can be reached directly without a prefix. When Python meets a name it searches in the order Local, Enclosing, Global, Built-in (LEGB) and stops at the first match; if nothing matches it raises `NameError`. Scope is decided by where the code is written (lexical scoping), not by who calls the function.

```python
base_url = "https://staging.example.com"   # Global
def outer():
    version = "v1"                          # Enclosing for inner()
    def inner():
        return base_url + "/" + version + "/" + str(len("x"))   # len is Built-in
    return inner
```
</details>

*Source:* `scope-and-namespaces.md`

---

### Q2: A function does `passed += 1` on a module-level counter and raises `UnboundLocalError`. Why, and how do `global` and `nonlocal` fix this kind of problem?
**Keywords:** assignment makes local, `UnboundLocalError`, `global`, `nonlocal`, rebinding
<details>
<summary>Click to Reveal Answer</summary>

If a function assigns to a name anywhere in its body, Python treats that name as local to the whole function, decided when the function is compiled. `passed += 1` means "read `passed`, add one, assign it", so the read happens before any local value exists and `UnboundLocalError` is raised. `global passed` makes the function rebind the module-level variable, and `nonlocal count` does the same for a variable in the nearest enclosing function (which must already exist). Usually the better fix is to return the new value or keep state in a closure or object, because global mutable state makes tests hard to isolate.

```python
def make_counter():
    count = 0
    def increment():
        nonlocal count
        count += 1
        return count
    return increment
```
</details>

*Source:* `scope-and-namespaces.md`

---

### Q3: What does it mean to "shadow" a built-in name, and what can go wrong?
**Keywords:** built-in scope, shadowing, `list`, `TypeError`, `del`, descriptive names
<details>
<summary>Click to Reveal Answer</summary>

Built-ins live in the last scope searched (the "B" in LEGB), so a Local, Enclosing or Global variable with the same name is found first and hides the built-in. For example, after `list = [1, 2]`, calling `list((1, 2))` raises `TypeError: 'list' object is not callable`. The real built-in is not destroyed, and `del list` lets the lookup fall through to it again. Avoid the problem by using descriptive names such as `items`, `user_id` or `max_value` instead of `list`, `id` or `max`.
</details>

*Source:* `scope-and-namespaces.md`

---

### Q4: What is the difference between `is` and `==`, and when should you use each?
**Keywords:** identity, equality, same object, `None`, `id()`
<details>
<summary>Click to Reveal Answer</summary>

`==` asks whether two objects have the same value, while `is` asks whether two names point at the exact same object (like comparing `id()` values). Two separate lists `[1, 2]` are `==` but not `is`. Use `==` for values, including in test assertions, and use `is` only for singletons such as `None`, for example `if result is None:`. Never use `is` for numbers or strings: small-integer caching in CPython is an implementation detail that will fail you on a value like 257.
</details>

*Source:* `mutability-and-memory.md`

---

### Q5: What is the difference between a shallow copy and a deep copy, and why does it matter for test data?
**Keywords:** shallow, deep, nested objects, `copy.deepcopy`, shared references
<details>
<summary>Click to Reveal Answer</summary>

Assignment never copies an object; it only attaches another label. A shallow copy (`.copy()`, `list()`, slicing, `copy.copy`) builds a new outer container but its nested objects are still shared with the original. A deep copy (`copy.deepcopy`) recursively copies everything, giving a fully independent structure. For nested test data such as a base user with a `roles` list, a shallow copy lets one test change the original, so use `copy.deepcopy` at the start of each test or fixture.

```python
orig = {"user": {"roles": ["x"]}}
shallow = orig.copy()
shallow["user"]["roles"].append("y")
print(orig)    # {'user': {'roles': ['x', 'y']}}  <- original changed
```
</details>

*Source:* `mutability-and-memory.md`

---

### Q6: Why does `int("3.7")` fail while `int(3.7)` works, and what do `bool("False")` and `bool([0])` return?
**Keywords:** `ValueError`, truncation, truthiness, non-empty, `int(float())`
<details>
<summary>Click to Reveal Answer</summary>

`int()` on a string requires text that looks exactly like an integer, so `int("3.7")` raises `ValueError`, whereas `int(3.7)` truncates toward zero to `3`. If you mean "convert the text to a float then truncate", write `int(float("3.7"))`. In `bool()`, empty containers, `0`, `None` and `""` are falsy and almost everything else is truthy, so both `bool("False")` (a non-empty string) and `bool([0])` (a non-empty list) are `True`. When reading booleans from CSV or JSON, compare against explicit text such as `value.lower() == "true"`.
</details>

*Source:* `built-in-python-functions.md`

---

### Q7: What does `zip` do when its inputs have different lengths, and how can you make a mismatch visible when comparing expected and actual lists?
**Keywords:** `zip`, shortest input, silent, `strict=True`, `ValueError`
<details>
<summary>Click to Reveal Answer</summary>

`zip` pairs items in step and stops silently at the shortest input, so extra items in the longer list are dropped and missing data can go unnoticed. Since Python 3.10 you can pass `strict=True`, which raises `ValueError` when the lengths differ. This is ideal for comparing an expected list with an actual list in a test. `itertools.zip_longest` is the alternative if you want the shorter input padded instead.

```python
list(zip([1, 2, 3], "ab"))                 # [(1, 'a'), (2, 'b')]  -> 3 is lost silently
list(zip([1, 2, 3], "ab", strict=True))    # raises ValueError
```
</details>

*Source:* `built-in-python-functions.md`

---

### Q8: How do you read a Python traceback, and why is the line that crashed not always the defect?
**Keywords:** bottom-up, exception type, call chain, root cause, data
<details>
<summary>Click to Reveal Answer</summary>

Read it from the bottom up: the last line gives the exception type and message (the "what"), the frame just above it gives the file, line and function (the "where"), and the frames above that show the chain of calls that led there (the "how we got here"). The crashing line may be perfectly correct code. In the lesson's cart example the `KeyError: 'discount'` is raised on a correct line, and the real culprit is the data, a cart item with no `discount` key. Debugging means finding that root cause, not just silencing the symptom.
</details>

*Source:* `debugging-techniques.md`

---

### Q9: In `pdb`, what is the difference between `n` and `s`, and how do you stop only when a specific condition is true?
**Keywords:** `breakpoint()`, step over, step into, conditional breakpoint, `p`
<details>
<summary>Click to Reveal Answer</summary>

`breakpoint()` (Python 3.7+) pauses the program at that line and opens the `(Pdb)` prompt. `n` (next) runs the current line and steps over function calls, while `s` (step) steps into a called function and stops on its first line, so use `s` when you suspect the called function. `p expr` prints a value, `c` continues, and `r` runs until the current function returns. A conditional breakpoint such as `b 12, user_id == 4242` pauses only when the condition is true, so you do not press `c` thousands of times.
</details>

*Source:* `debugging-techniques.md`

---

### Q10: Name the five standard log levels in order. What is the default threshold, and what does that mean for `logging.info("...")` out of the box?
**Keywords:** DEBUG, INFO, WARNING, ERROR, CRITICAL, threshold
<details>
<summary>Click to Reveal Answer</summary>

From least to most severe the levels are `DEBUG` (10), `INFO` (20), `WARNING` (30), `ERROR` (40) and `CRITICAL` (50). A logger has a threshold: messages below it are ignored and messages at or above it are processed. The default threshold is `WARNING`, so out of the box `logging.info(...)` prints nothing. Changing the level (for example with `basicConfig(level=logging.DEBUG)`) turns detail up or down without touching the code that writes the messages.

```python
import logging
logging.debug("d"); logging.info("i"); logging.warning("w"); logging.error("e")
# WARNING:root:w
# ERROR:root:e
```
</details>

*Source:* `logging.md`

---

### Q11: Why is `logging` preferred over `print()` for diagnostics, and how should you log a caught exception?
**Keywords:** levels, timestamps, `logger.exception`, traceback, lazy formatting
<details>
<summary>Click to Reveal Answer</summary>

Unlike `print`, logging has severity levels you can filter without editing code, automatic timestamps and module names, handlers that send output to console and file at once, and it is safe to leave in production code. Inside an `except` block, `logger.exception("what we were doing")` logs at `ERROR` level and appends the full traceback (equivalent to `logger.error(..., exc_info=True)`). Pass values lazily, as in `logger.info("user %s logged in", username)`, so the string is only built if the message will be emitted. `print` is still right for a program's intended output; logging is for diagnostics.
</details>

*Source:* `logging.md`

---

### Q12: What is a unit test, and what do Arrange-Act-Assert and the FIRST principles mean?
**Keywords:** unit, Arrange-Act-Assert, FIRST, isolated, repeatable
<details>
<summary>Click to Reveal Answer</summary>

A unit is the smallest testable piece of code (one function or method), and a unit test is a small automated program that calls it with specific inputs, compares the actual result with the expected result and reports pass or fail. A good test follows Arrange (prepare inputs and state), Act (call the unit, usually once) and Assert (check the outcome). FIRST stands for Fast, Independent/Isolated, Repeatable, Self-validating and Timely. Independence matters most for QA: a test must not depend on another test or on execution order.
</details>

*Source:* `introduction-to-unit-testing.md`

---

### Q13: In `unittest`, what is the difference between a FAIL and an ERROR, and what do `setUp` and `tearDown` do?
**Keywords:** FAIL, ERROR, assertion, `setUp`, `tearDown`, fresh state
<details>
<summary>Click to Reveal Answer</summary>

A FAIL means an assertion was false: the code ran but gave the wrong answer (or the test's expectation is wrong). An ERROR means the test raised an unexpected exception that is not an assertion, such as a `KeyError` in the code or in the test's setup. `setUp()` runs before each test method to give every test fresh objects or data (isolation), and `tearDown()` runs after each test, even a failed one, to clean up. `setUpClass` and `tearDownClass` run once per class for expensive resources.
</details>

*Source:* `introduction-to-unit-testing.md`

---

### Q14: What causes a Git merge conflict, and how do you read the conflict markers?
**Keywords:** three-way merge, same lines, `<<<<<<< HEAD`, `=======`, ours and theirs
<details>
<summary>Click to Reveal Answer</summary>

Git does a three-way merge using the merge base (the common ancestor), our version and their version. Changes in different areas merge automatically, but when both sides changed the same lines (or adjacent lines) differently, Git cannot guess and stops with `CONFLICT`. Between `<<<<<<< HEAD` and `=======` is the version from your current branch (ours), and between `=======` and `>>>>>>> branch` is the version from the branch being merged in (theirs). The markers are just text in the file, so you resolve by editing until exactly the content you want remains and no marker lines are left.

```text
<<<<<<< HEAD
TIMEOUT = 20
=======
TIMEOUT = 30
>>>>>>> origin/main
```
</details>

*Source:* `git-merge-conflicts-and-resolution.md`

---

## Intermediate (Application)

### Q15: A teammate writes `assert all(r["ok"] for r in results)` to verify that every API result is valid, and the test goes green even though the API returned nothing. What happened, and how do you fix it?
**Keywords:** `all([])`, empty, vacuous truth, guard, `assert results`
**Hint:** What does `all()` return for an empty input?
<details>
<summary>Click to Reveal Answer</summary>

`all([])` is `True` because no counter-examples were found, so an empty result set passes silently and nothing was actually verified. Add a guard before the check, such as `assert results` or `assert len(results) > 0`, with a message explaining that an empty response is a defect. A better assertion message would also list the offending rows so a failure explains itself.

```python
results = []
print(all(r["ok"] for r in results), any(r["ok"] for r in results))   # True False
assert results, "API returned no results"                              # fails, as it should
```
</details>

*Source:* `built-in-python-functions.md`

---

### Q16: A test passes when run alone but fails when the whole suite runs. How do you investigate, and what are the likely causes?
**Keywords:** shared state, mutable default argument, isolation, reproduce, order dependence
**Hint:** Think about what the scope and mutability lessons said about state that survives between tests.
<details>
<summary>Click to Reveal Answer</summary>

First reproduce the failure reliably, rerun the test in isolation and compare the passing and failing cases, because a test that depends on what ran before it points to shared state. Likely causes are a global variable changed by an earlier test, a mutable default argument such as `errors=[]` that accumulates across calls, a "constant" test-data dictionary that was mutated (fix with `copy.deepcopy` per test), or leftover files and order dependence. The fix is to give each test its own fresh data in `setUp` and avoid hidden global state. Do not loosen the expected value to turn the test green, and do not just rerun until it passes, because flaky tests are bugs.
</details>

*Source:* `debugging-techniques.md`

---

### Q17: Your test framework logs a run. Which level would you choose for each event: (a) "Test test_login started", (b) the full request payload, (c) a response that took 4.2s against a 2s limit, (d) a failed assertion on the order total, (e) the database connection lost so the whole run aborts?
**Keywords:** INFO, DEBUG, WARNING, ERROR, CRITICAL
**Hint:** Match each event to what the level is meant for: milestone, detail, "unexpected but continuing", failed operation, run in trouble.
<details>
<summary>Click to Reveal Answer</summary>

(a) `INFO`, the high-level story and milestones. (b) `DEBUG`, detailed diagnostics such as payloads and values, fine to be chatty. (c) `WARNING`, because something is off but the program continues. (d) `ERROR`, because an operation failed and probably a test failed. (e) `CRITICAL`, a severe problem where the run may be unable to continue. A typical setup keeps the console at `INFO` and writes the file at `DEBUG`. Logging everything as `INFO` or everything as `ERROR` defeats the purpose of levels, which exist so readers and tools can filter.
</details>

*Source:* `logging.md`

---

### Q18: Your colleague's test `self.assertEqual(add(0.1, 0.2), 0.3)` fails with `0.30000000000000004 != 0.3`, and they propose changing the expected value to `0.30000000000000004`. What do you recommend?
**Keywords:** floating point, `assertAlmostEqual`, binary, do not loosen, expected value
**Hint:** Is the product wrong, or is the comparison wrong?
<details>
<summary>Click to Reveal Answer</summary>

Neither the code nor the expected value is wrong; floats are stored in binary and `0.1` and `0.2` cannot be represented exactly, so `==` on calculated floats is the wrong comparison. Use `assertAlmostEqual(add(0.1, 0.2), 0.3)`, which compares after rounding to 7 decimal places by default (or `delta=` for a tolerance); outside `unittest`, `math.isclose` does the same job. Changing the expected value to the noisy number would bake rounding noise into the test. In general, change a test's expectation only after you have proven which side is wrong.

```python
import unittest
class T(unittest.TestCase):
    def test_add_floats(self):
        self.assertAlmostEqual(0.1 + 0.2, 0.3)   # passes
```
</details>

*Source:* `introduction-to-unit-testing.md`

---

### Q19: You and a teammate both changed `settings.py` (a shared test config). You change `TIMEOUT = 20` and `BROWSER = "firefox"`; they push first with `TIMEOUT = 30` and `RETRIES = 5`. Your `git pull` stops with a conflict. Walk through how you resolve it and finish.
**Keywords:** `git status`, markers, decide per line, `git add`, `git commit`, run tests
**Hint:** Resolve line by line, ask the author when unsure, and remember the file must work afterwards.
<details>
<summary>Click to Reveal Answer</summary>

Run `git status` to see `both modified: settings.py`, then open the file and read the markers (above `=======` is yours, below is theirs; the end marker may show a commit id because `pull` merged the fetched commit). Decide line by line, because adjacent changes land in one conflict block: keep `TIMEOUT = 30` and `RETRIES = 5` (needed for their slow CI server, confirm with them if unsure) and `BROWSER = "firefox"` (only you changed it intentionally). Delete every marker line and check with `git diff --check`, run the tests or the code, then `git add settings.py` to mark it resolved and `git commit` to complete the merge, and finally `git push`. If you get lost, `git merge --abort` returns you to the state before the pull.

```python
TIMEOUT = 30
RETRIES = 5
BROWSER = "firefox"
```
</details>

*Source:* `git-merge-conflicts-and-resolution.md`

---

## Advanced (Deep Dive)

### Q20: What does this code print, and what is happening under the hood? How do you fix it?
```python
def add_item(item, bucket=[]):
    bucket.append(item)
    return bucket

print(add_item(1))
print(add_item(2))
```
**Keywords:** default evaluated once, shared list, `__defaults__`, `None` sentinel, mutation
**Hint:** When is a default value evaluated: on every call, or when the `def` statement runs?
<details>
<summary>Click to Reveal Answer</summary>

It prints `[1]` and then `[1, 2]`. Default values are evaluated once, when the `def` statement runs, not on each call, so every call that uses the default shares the same list object, which you can see in `add_item.__defaults__` (it shows `([1, 2],)` after the two calls). `append` mutates that object, so earlier calls leak into later ones, exactly how a helper like `collect_errors(message, errors=[])` makes test B see test A's errors. The standard fix is a `None` sentinel with a fresh list created inside the function, so each call gets its own list.

```python
def add_item(item, bucket=None):
    if bucket is None:
        bucket = []
    bucket.append(item)
    return bucket

print(add_item(1))   # [1]
print(add_item(2))   # [2]
```
</details>

*Source:* `mutability-and-memory.md`

---

## How to use this bank

This bank is for self-quizzing, so do not read the answers first.

1. Read a question and cover the answer (keep the `<details>` block closed).
2. Say your answer aloud as if you were in an interview, in 30 to 60 seconds. Use the hint only if you are stuck.
3. Open the answer and check that every **keyword** appeared in what you said. If you missed one, repeat the question until you can include it naturally.
4. Work through Beginner first until you can answer without notes, then attempt Intermediate (talk through the scenario step by step), then the Advanced question.
5. If you struggle with a topic, re-read the lesson named in the *Source* line and try again the next day.
