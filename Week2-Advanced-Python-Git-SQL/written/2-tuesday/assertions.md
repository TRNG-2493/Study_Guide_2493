# Assertions

## Learning Objectives

By the end of this lesson you will be able to:

- Explain what an **assertion** is and what the `assert` statement does.
- Write assertions with and without a custom failure message.
- Describe what happens when an assertion fails (`AssertionError`) and read the resulting traceback.
- Explain the difference between **assertions** and **exceptions**, and choose correctly between them.
- Explain why assertions can be **disabled** (the `-O` flag) and why this means they must never be used for input validation or security.
- Avoid common pitfalls, such as asserting on a tuple (which is always true) and putting side effects inside an assertion.
- Use assertions for preconditions, postconditions, invariants, and as lightweight "self-checking" tests.
- Recognise how the **assert-based checking** you learn today connects to test automation, where the central idea is "compare actual vs expected".

---

## Why This Matters

Everything in testing boils down to one sentence: **"I expected X; did I actually get X?"**

Whether you test a login page, an API response or a SQL query, you state an expectation and compare it with reality. When they differ, you have found something worth reporting. The Python statement that expresses this idea in its simplest form is `assert`.

In the QE Foundations project this week, you are building toward a small but real toolkit: data loaders, validators and, later, tests. The `assert` statement is the **entry point to automated checking**:

- It lets you embed "this must be true" statements directly in your code and scripts.
- It stops a program immediately and loudly when a hidden assumption turns out to be false, instead of letting bad data silently corrupt later steps.
- It is the same idea that test frameworks use (the popular `pytest` framework, for instance, builds on plain `assert` statements). On Wednesday you will start with `unittest`, which provides its own `assert...` methods. The concept you learn here transfers directly. (We will cover unit testing in depth on Wednesday, so for today we focus on the Python language statement itself.)

Last lesson, you learned how to raise exceptions to **reject bad input**. Assertions are a *different* tool for a *different* purpose, and understanding the difference is a mark of a mature Python programmer.

---

## The Concept

### 1. What Is an Assertion?

An **assertion** is a statement that declares: *"At this point in the program, this condition must be true."*

If the condition is true, nothing happens and the program continues. If it is false, Python raises an `AssertionError` and (unless handled) the program stops.

Analogy: A pilot's pre-flight checklist. "Fuel level above minimum?" If yes, continue. If not, **stop everything**; something is fundamentally wrong, and it would be dangerous to proceed on the assumption that it is fine.

### 2. Basic Syntax

```python
assert condition
assert condition, "optional message"
```

A first example:

```python
total_tests = 10
passed_tests = 8

assert passed_tests <= total_tests
print("Counts look sane")
```

Output:

```
Counts look sane
```

Now make the condition false:

```python
total_tests = 10
passed_tests = 12

assert passed_tests <= total_tests
print("This line is never reached")
```

Output:

```
Traceback (most recent call last):
  File "example.py", line 4, in <module>
    assert passed_tests <= total_tests
AssertionError
```

**Step by step:**

1. Python evaluates the expression `passed_tests <= total_tests`.
2. If the result is **truthy** (`True`, or any value Python considers true), execution simply continues.
3. If it is **falsy** (`False`, `0`, `None`, an empty list or string, and so on), Python raises `AssertionError`.

The bare `AssertionError` with no message tells you *where* but not *why*. That leads to the next feature.

### 3. Adding a Failure Message

The part after the comma is the message that goes inside the `AssertionError`:

```python
passed_tests = 12
total_tests = 10

assert passed_tests <= total_tests, (
    f"passed ({passed_tests}) cannot exceed total ({total_tests})"
)
```

Output:

```
Traceback (most recent call last):
  File "example.py", line 4, in <module>
    assert passed_tests <= total_tests, (
AssertionError: passed (12) cannot exceed total (10)
```

A good message states **what was expected** and **what was found**. Compare how quickly you can act on each:

| Message | Usefulness |
|---------|------------|
| *(none)* | You must open the code to find out what failed |
| `"bad value"` | Slightly better, but which value? |
| `"expected status 200 but got 500 for /login"` | Immediately actionable |

The message is only evaluated if the assertion **fails**, so it is fine to build it with an f-string (no performance cost on success).

### 4. Equivalent Meaning

`assert condition, message` is roughly equivalent to:

```python
if __debug__:
    if not condition:
        raise AssertionError(message)
```

The special built-in constant `__debug__` is `True` in a normal run and `False` when Python is started in optimised mode. This brings us to the most important property of assertions.

### 5. Assertions Can Be Turned Off

When you run Python with the `-O` flag, **all assert statements are removed**:

```
python script.py        # asserts are active
python -O script.py     # asserts are skipped completely
```

Test it yourself with this file (`demo_O.py`):

```python
print("__debug__ is", __debug__)
assert 1 == 2, "this should fail"
print("Reached the end")
```

```
$ python demo_O.py
__debug__ is True
Traceback (most recent call last):
  File "demo_O.py", line 2, in <module>
    assert 1 == 2, "this should fail"
AssertionError: this should fail

$ python -O demo_O.py
__debug__ is False
Reached the end
```

This is not a bug; it is a deliberate feature. Assertions are meant as **developer aids** for finding programming mistakes, which production code can skip for speed. But it has a crucial consequence:

> **Never use `assert` to validate user input, external data, file contents, or anything related to security. If asserts are disabled, those checks vanish and the bad data walks straight through.**

For those jobs, use `if` plus `raise` (the previous lesson). We will examine the distinction in detail below.

### 6. Assertions vs Exceptions: Which One Do I Use?

This is the most common point of confusion, so let us be precise.

| Question | Assertion (`assert`) | Exception (`raise`) |
|----------|----------------------|---------------------|
| What does a failure mean? | **A bug in our own code** (a broken assumption) | **A problem in the outside world** (bad input, missing file, network failure) |
| Who is at fault? | The programmer | The user, the data, or the environment |
| Should it be handled by `except`? | Normally **no**: the program is in an unexpected state | **Yes**: often handled and recovered from |
| Can it be disabled? | Yes (`python -O`) | No, always active |
| Typical use | Internal sanity checks, invariants, quick tests | Validating input, reporting expected failures |

Rules of thumb:

- If the situation **can legitimately happen** (a file might be missing; a user might type "abc"), use an **exception**.
- If the situation **should be impossible if the code is correct**, use an **assertion**.
- If removing the check would let bad external data into your program, it is validation. Use an exception.

Examples side by side:

```python
def average(numbers):
    # VALIDATION of what the caller gives us -> exception
    if not numbers:
        raise ValueError("cannot average an empty list")

    total = sum(numbers)
    result = total / len(numbers)

    # INTERNAL SANITY CHECK of our own logic -> assertion
    assert min(numbers) <= result <= max(numbers), "average out of range: logic error"
    return result
```

If someone passes an empty list, that is a caller mistake that can happen at any time, so we raise `ValueError`. After computing, the average must lie between the minimum and maximum. If it does not, **our code** is wrong, so we assert.

### 7. Where Assertions Are Useful

**Preconditions:** conditions that must hold when a function starts (for internal helpers whose callers are your own code):

```python
def _percentage(part, whole):
    assert whole > 0, "whole must be positive (caller bug)"
    return part / whole * 100
```

**Postconditions:** conditions that must hold when a function finishes:

```python
def normalise(scores):
    total = sum(scores)
    result = [s / total for s in scores]
    assert abs(sum(result) - 1.0) < 1e-9, "normalised scores must add up to 1"
    return result
```

(Why `abs(... ) < 1e-9`? Floating-point arithmetic is slightly inexact, so we compare with a tolerance instead of using `==`. For example, `0.1 + 0.2 == 0.3` is `False` in Python!)

**Invariants:** facts that must remain true throughout a process, for example "the number of passed plus failed plus skipped tests equals the total".

**Documentation that executes:** an assertion tells the next reader what you assumed. `assert isinstance(rows, list)` documents your expectation, and fails loudly if you or a teammate break it.

**Quick self-checks and scripts:** when you write a small utility, a few asserts at the bottom serve as a smoke test.

```python
def is_even(n):
    return n % 2 == 0

assert is_even(4)
assert not is_even(7)
assert is_even(0)
print("is_even passed all checks")
```

**Debugging aid:** while hunting a bug you can add assertions to confirm hypotheses. (We will explore systematic debugging on Wednesday.)

### 8. Where Assertions Do NOT Belong

1. **Validating user input or file data.**

```python
# BAD: disappears under python -O
assert age >= 0, "age must be non-negative"

# GOOD
if age < 0:
    raise ValueError("age must be non-negative")
```

2. **Checks with side effects.** The expression inside `assert` vanishes when assertions are disabled, so any action in it vanishes too:

```python
# BAD: the pop() is skipped under python -O, changing program behaviour!
assert queue.pop() == "first"

# GOOD: do the action, then assert on the result
item = queue.pop()
assert item == "first"
```

3. **Handling expected runtime errors** (files, network, database). Use `try`/`except`.
4. **Security checks**, such as "is the user an administrator?". Never.

### 9. Common Pitfalls

**Pitfall 1: asserting on a tuple.** Putting parentheses around both the condition and the message makes a tuple, and a non-empty tuple is always truthy:

```python
assert (1 == 2, "this message never appears")   # always passes!
```

Python warns about this (`SyntaxWarning: assertion is always true, perhaps remove parentheses?`). Write it without parentheses around the pair:

```python
assert 1 == 2, "this message appears"           # correct
```

You may put parentheses around the *message only*, to wrap a long line (as in section 3).

**Pitfall 2: comparing floats with `==`.**

```python
assert 0.1 + 0.2 == 0.3                         # AssertionError!
assert abs((0.1 + 0.2) - 0.3) < 1e-9            # correct
```

The standard library also offers `math.isclose(a, b)`:

```python
import math
assert math.isclose(0.1 + 0.2, 0.3)             # passes
```

**Pitfall 3: a vague or missing message.** Always say what was expected and what was found.

**Pitfall 4: catching `AssertionError` to "keep going".** Occasionally acceptable in a test runner (that is, in fact, what test frameworks do), but in ordinary program code, a failed assertion should mean "stop and fix the bug".

**Pitfall 5: too many assertions.** Asserting every trivial thing clutters the code. Assert the *important assumptions* and the *non-obvious invariants*.

### 10. Writing Better Assertions: Practical Patterns

**Checking membership:**

```python
status = "pass"
assert status in ("pass", "fail", "skip"), f"unknown status {status!r}"
```

**Checking types:**

```python
rows = [1, 2, 3]
assert isinstance(rows, list), f"expected list, got {type(rows).__name__}"
```

**Checking collection sizes:**

```python
results = ["a", "b", "c"]
assert len(results) == 3, f"expected 3 results, got {len(results)}"
```

**Checking multiple things clearly,** use separate asserts rather than one large expression so the failure points to the exact problem:

```python
user = {"id": 7, "name": "Ada", "active": True}

assert "id" in user, "user is missing 'id'"
assert user["id"] > 0, f"id must be positive, got {user['id']}"
assert user["active"] is True, "user should be active"
```

**Checking dictionaries and lists for equality:**

```python
expected = {"status": "ok", "count": 3}
actual = {"status": "ok", "count": 3}
assert actual == expected, f"expected {expected} but got {actual}"
```

Note the habit of putting the **actual vs expected** values in the message. Test frameworks automate this for you, but you should understand what they are doing.

### 11. Assertions as the Heart of a Test

A test is, at its simplest, a function that runs some code and asserts about the result:

```python
def add(a, b):
    return a + b


def test_add_positive_numbers():
    assert add(2, 3) == 5

def test_add_negative_numbers():
    assert add(-2, -3) == -5

def test_add_zero():
    assert add(0, 7) == 7
```

You can run these yourself in a few lines:

```python
tests = [test_add_positive_numbers, test_add_negative_numbers, test_add_zero]

for test in tests:
    try:
        test()
    except AssertionError as error:
        print(f"FAIL {test.__name__}: {error}")
    else:
        print(f"PASS {test.__name__}")
```

Output:

```
PASS test_add_positive_numbers
PASS test_add_negative_numbers
PASS test_add_zero
```

This 10-line loop is, in miniature, what a test framework does: call each test function, catch `AssertionError` as a **failure** (the code under test did not meet the expectation), and report. It also shows why the assertion/exception distinction matters: in a test, an `AssertionError` means "the product code is wrong", whereas any *other* exception (like `KeyError`) means "something unexpected broke". Real frameworks report these two categories differently (usually "failures" vs "errors"). On Wednesday you will use `unittest` for exactly this, and we will go through its assert methods then.

---

## Real-World QA Scenarios

### Scenario 1: Sanity checks on test-run results

After a test run, a summary dictionary is produced. Before publishing the report, assert that the numbers are consistent. If they are not, your *reporting code* has a bug, and you do not want to publish nonsense.

```python
def build_summary(results):
    summary = {"pass": 0, "fail": 0, "skip": 0}
    for status in results:
        summary[status] += 1

    # invariant: every result is counted exactly once
    assert sum(summary.values()) == len(results), (
        f"counted {sum(summary.values())} results but received {len(results)}"
    )
    return summary


print(build_summary(["pass", "pass", "fail", "skip", "pass"]))
```

Output:

```
{'pass': 3, 'fail': 1, 'skip': 1}
```

(Notice that a status other than `pass`, `fail`, `skip` would raise `KeyError` here: an *exception* about unexpected external data. The assertion is about our own counting logic.)

### Scenario 2: Checking an API-style response in a script

```python
response = {
    "status_code": 200,
    "body": {"id": 42, "name": "Laptop", "price": 999.99},
}

assert response["status_code"] == 200, (
    f"expected status 200 but got {response['status_code']}"
)
assert "id" in response["body"], "response body has no 'id'"
assert response["body"]["price"] > 0, "price must be positive"
assert isinstance(response["body"]["name"], str), "name must be text"
print("Response checks passed")
```

Output:

```
Response checks passed
```

This is the shape of most automated API checks: obtain a response, then make a series of assertions about it. Here `assert` is used as a *test check* (the response is the thing under test) rather than program validation.

### Scenario 3: Data-integrity check before processing

Suppose a loader function should always return a list of dictionaries, each having an `id`. As a developer you assert this contract immediately after loading, so a later bug elsewhere is detected at once:

```python
def load_users():
    # imagine this reads a file; here we simulate the result
    return [{"id": 1, "name": "Ada"}, {"id": 2, "name": "Grace"}]


users = load_users()

assert isinstance(users, list), "load_users() must return a list"
assert all("id" in u for u in users), "every user must have an 'id'"
assert len({u["id"] for u in users}) == len(users), "user ids must be unique"
print(f"{len(users)} users passed integrity checks")
```

Output:

```
2 users passed integrity checks
```

**Explanation of the new pieces:**

- `all(iterable)` returns `True` only if every item in the iterable is truthy. Here the generator `("id" in u for u in users)` yields `True` or `False` for each user.
- `{u["id"] for u in users}` is a **set comprehension**: it builds a set of ids. Sets cannot contain duplicates, so if the set is smaller than the list, there were duplicate ids.

### Scenario 4: A guard that is a validation (use an exception, not an assertion)

```python
def load_config_timeout(config):
    timeout = config.get("timeout")
    if not isinstance(timeout, int) or timeout <= 0:
        raise ValueError(f"timeout must be a positive integer, got {timeout!r}")
    return timeout
```

Contrast this with an assertion: the config comes from outside the program (a file someone edited), so wrong values are *expected* to occur sometimes. That is validation, and it must work even under `python -O`.

---

## Code Examples: Putting It All Together

A self-contained script that mixes validation (exceptions) with internal checks (assertions), and a mini test runner. Save as `assert_demo.py`.

```python
"""assert_demo.py - Validation with exceptions, sanity checks with assertions."""


def pass_rate(passed, total):
    """Return the pass percentage rounded to 1 decimal place."""
    # Validation of external input -> exceptions
    if not isinstance(passed, int) or not isinstance(total, int):
        raise TypeError("passed and total must be integers")
    if total <= 0:
        raise ValueError("total must be positive")
    if not 0 <= passed <= total:
        raise ValueError("passed must be between 0 and total")

    rate = round(passed / total * 100, 1)

    # Internal sanity check of our own logic -> assertion
    assert 0.0 <= rate <= 100.0, f"rate {rate} escaped 0..100 (logic error)"
    return rate


def test_all_pass():
    assert pass_rate(10, 10) == 100.0

def test_none_pass():
    assert pass_rate(0, 10) == 0.0

def test_partial():
    assert pass_rate(1, 3) == 33.3

def test_deliberately_wrong():
    assert pass_rate(1, 4) == 30.0, "expected 30.0 (this check is wrong on purpose)"

def test_invalid_input_raises():
    try:
        pass_rate(5, 0)
    except ValueError:
        return                      # the error we wanted
    raise AssertionError("expected ValueError for total=0")


for test in (test_all_pass, test_none_pass, test_partial,
             test_deliberately_wrong, test_invalid_input_raises):
    try:
        test()
    except AssertionError as error:
        print(f"FAIL  {test.__name__}: {error}")
    except Exception as error:
        print(f"ERROR {test.__name__}: {type(error).__name__}: {error}")
    else:
        print(f"PASS  {test.__name__}")
```

Output:

```
PASS  test_all_pass
PASS  test_none_pass
PASS  test_partial
FAIL  test_deliberately_wrong: expected 30.0 (this check is wrong on purpose)
PASS  test_invalid_input_raises
```

**Walkthrough:**

1. `pass_rate` first **validates** its inputs using `raise` (types and ranges). These errors are the caller's problem and must always be active.
2. After computing, it asserts that the result lies in `0..100`. If our maths were wrong, the assertion would reveal it immediately.
3. The `test_...` functions are tiny checks built on `assert`.
4. `test_deliberately_wrong` expects `30.0`, but the true result is `25.0`, so it fails. The failing message is displayed. Seeing a **FAIL** is how you know your checks can actually catch problems (a test that can never fail is worthless).
5. `test_invalid_input_raises` demonstrates how to check that a function *does* raise: call it in `try`, `return` if the expected exception appears, otherwise `raise AssertionError`. (Test frameworks give a neater tool for this, which you will meet on Wednesday.)
6. The runner distinguishes `AssertionError` (**FAIL**: the code under test misbehaved) from any other exception (**ERROR**: something unexpected broke).

---

## Practice Exercises

**Exercise 1: Predict.** Which of these lines raises `AssertionError`?

```python
assert 5 > 3
assert []
assert "hello"
assert 0.1 + 0.2 == 0.3
assert (False, "msg")
assert None is None
```

**Exercise 2: Add messages.** Rewrite each of these assertions so that the message shows both the expected and actual values.

```python
assert len(items) == 5
assert response_code == 200
assert name.startswith("Mr")
```

**Exercise 3: Assertion or exception?** For each situation, say which tool you would use and why:

1. A function receives a filename typed by a user.
2. After sorting a list, you want to confirm each item is `<=` the next one.
3. A CSV file's `price` column contains a negative number.
4. A helper (only called by your own code) requires that its argument is not `None`.

**Exercise 4: Fix the code.** What is wrong with each?

```python
assert (x > 0, "x must be positive")

assert user_input.isdigit(), "please enter digits only"

assert open("data.txt").read() != ""
```

**Exercise 5: Write your own.** Write `is_sorted(values)` returning `True` if the list is in ascending order. Then write at least five `assert` statements checking it, including an empty list and a one-item list.

**Exercise 6: Invariant.** Write `split_even_odd(numbers)` returning `(evens, odds)`. Add an assertion proving no number was lost or duplicated, and another proving all numbers in `evens` are even.

### Answers

**Exercise 1:** Raising `AssertionError`: `assert []` (empty list is falsy) and `assert 0.1 + 0.2 == 0.3` (floating-point inexactness). `assert (False, "msg")` does **not** raise: a non-empty tuple is truthy (and Python gives a SyntaxWarning). The rest pass.

**Exercise 2:**

```python
assert len(items) == 5, f"expected 5 items, got {len(items)}"
assert response_code == 200, f"expected 200, got {response_code}"
assert name.startswith("Mr"), f"expected name starting with 'Mr', got {name!r}"
```

**Exercise 3:** (1) Exception: user input is external, and the check must always run (for example `FileNotFoundError` handling or a `ValueError`). (2) Assertion: it is an internal postcondition about your own sorting logic. (3) Exception: file data is external and a negative price can legitimately occur; raise `ValueError` or a custom validation error. (4) Assertion is acceptable: it documents a rule about internal callers (but an exception is also fine if the helper is public).

**Exercise 4:** First: the tuple makes the assertion always true; remove the parentheses around the pair. Second: user input is external, so validation must use `if`/`raise`; asserts can be disabled with `-O`. Third: the assertion contains a side effect (opening a file) which disappears when assertions are disabled, and it also leaves the file unclosed. Read the file separately (using `with`, which you will learn shortly in this very day) and then assert on the content.

**Exercise 5:**

```python
def is_sorted(values):
    return all(values[i] <= values[i + 1] for i in range(len(values) - 1))

assert is_sorted([]), "empty list is sorted"
assert is_sorted([5]), "single item is sorted"
assert is_sorted([1, 2, 2, 3]), "duplicates allowed"
assert not is_sorted([3, 1, 2]), "unsorted list detected"
assert not is_sorted([1, 3, 2]), "late disorder detected"
print("is_sorted checks passed")
```

**Exercise 6:**

```python
def split_even_odd(numbers):
    evens = [n for n in numbers if n % 2 == 0]
    odds = [n for n in numbers if n % 2 != 0]

    assert len(evens) + len(odds) == len(numbers), "numbers were lost or duplicated"
    assert all(n % 2 == 0 for n in evens), "evens contains an odd number"
    return evens, odds

print(split_even_odd([1, 2, 3, 4, 5, 6]))    # ([2, 4, 6], [1, 3, 5])
```

---

## Summary / Key Takeaways

- `assert condition, message` raises `AssertionError` when the condition is false. When it is true, nothing happens.
- Assertions express **"this must be true here"**. A failing assertion means there is a **bug in the code** (a broken assumption), not bad input.
- Assertions can be **disabled** with `python -O`. Therefore never use them for validating user/file/API data, for security, or for anything with side effects.
- Use **exceptions** for things that can legitimately go wrong in the outside world; use **assertions** for things that should be impossible when the code is correct.
- Write messages that show expected and actual values. Avoid the always-true tuple form, and compare floating-point values with a tolerance (`math.isclose`).
- Tests are, at heart, functions full of assertions; a test runner catches `AssertionError` as a FAIL. You now understand the foundation of automated checking. We will build on it with the unit testing framework on Wednesday.

---

## Additional Resources

- Python Language Reference, "The assert statement": https://docs.python.org/3/reference/simple_stmts.html#the-assert-statement
- Python Tutorial, "Errors and Exceptions": https://docs.python.org/3/tutorial/errors.html
- Python Library Reference, `math.isclose`: https://docs.python.org/3/library/math.html#math.isclose
