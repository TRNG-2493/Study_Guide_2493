# Exception Testing

## Learning Objectives

By the end of this lesson you will be able to:

- Explain what an exception is and why *negative testing* (checking that code fails correctly) is as important as checking that it succeeds.
- Use `pytest.raises` as a context manager to assert that code raises a specific exception.
- Verify exception messages with `match=` and inspect the exception object through `excinfo`.
- Test exception hierarchies, custom exception classes, and exceptions with extra attributes.
- Use `pytest.warns` to test warnings, and `pytest.fail` / `pytest.xfail` correctly.
- Parametrize exception tests, including the "returns a value *or* raises" pattern, cleanly.
- Test exception chaining (`raise ... from ...`) and `ExceptionGroup` basics.
- Avoid the common mistakes: too-broad `Exception`, code after the raising line, `try/except` in tests.

---

## Why This Matters

This week's epic is to move from writing a few PyTest tests to building a **framework** for Project 1 – QE Foundations. A real product spends most of its life handling *unexpected* things: empty forms, negative amounts, missing files, bad credentials. A product that works only for perfect input is not a finished product.

When you wrote manual test cases in Project 1 you included **negative test cases** such as "enter an age of -5 and verify an error is shown". Exception testing is how you automate those negative cases for code. It proves that:

- the system *rejects* bad input rather than silently producing wrong results,
- the failure is the *right kind* of failure (a `ValueError`, not a crash with `TypeError` from an unrelated bug),
- the error message helps users and developers.

Industry teams routinely measure not only line coverage but whether error paths are tested, because production incidents commonly hide in error handling code that no one ever executed.

---

## The Concept

### 1. What is an exception?

When Python hits a problem it cannot continue past (dividing by zero, converting `"abc"` to an integer, reading a missing file) it creates an **exception** object and *raises* it. The normal flow stops, and Python looks "up the call stack" for a `try/except` that handles it. If nothing handles it, the program stops and prints a traceback.

```python
>>> int("abc")
ValueError: invalid literal for int() with base 10: 'abc'
>>> 10 / 0
ZeroDivisionError: division by zero
>>> {"a": 1}["b"]
KeyError: 'b'
>>> open("missing.txt")
FileNotFoundError: [Errno 2] No such file or directory: 'missing.txt'
```

Common built-in exceptions you will meet:

| Exception | Typical cause |
|-----------|---------------|
| `ValueError` | Right type but unacceptable value (`int("abc")`, negative age) |
| `TypeError` | Wrong type (`"a" + 1`) |
| `KeyError` | Missing dictionary key |
| `IndexError` | List index out of range |
| `ZeroDivisionError` | Division by zero |
| `FileNotFoundError` | File does not exist |
| `PermissionError` | No permission to access resource |
| `AttributeError` | Missing attribute/method |
| `RuntimeError` | Generic runtime problem |

All of them inherit (directly or indirectly) from `Exception`, which inherits from `BaseException`. This **inheritance hierarchy** matters for testing, as we see below.

Developers *raise* their own exceptions deliberately to signal invalid use:

```python
def withdraw(balance: float, amount: float) -> float:
    if amount <= 0:
        raise ValueError("amount must be positive")
    if amount > balance:
        raise InsufficientFundsError(balance, amount)
    return balance - amount
```

### 2. Why not just use `try/except` in tests?

A beginner's first attempt might look like this:

```python
def test_withdraw_negative():
    try:
        withdraw(100, -5)
    except ValueError:
        pass   # good, we expected it
```

**This test can never fail.** If `withdraw` stops raising an error, the `try` block simply finishes and the test passes. We have written a test that passes in both the correct and the broken world, which is useless.

A fix would require remembering to add `else: assert False`, which is clumsy. PyTest offers a purpose-built tool.

### 3. `pytest.raises` as a context manager

```python
import pytest


def test_withdraw_negative_amount_raises():
    with pytest.raises(ValueError):
        withdraw(100, -5)
```

**How it works, step by step:**

1. `with pytest.raises(ValueError):` opens a *context manager*, a block with special entry and exit behaviour.
2. The code inside the `with` block runs.
3. If a `ValueError` (or a subclass) is raised, `pytest.raises` **catches it** and the test continues past the block.
4. If *no* exception is raised, `pytest.raises` makes the test **fail** with `Failed: DID NOT RAISE <class 'ValueError'>`.
5. If a *different* exception type is raised (say `TypeError`), it propagates and the test fails/errors with that exception.

So the test passes **only** if exactly the expected kind of exception happens. That is the behaviour we wanted.

Let's create a runnable module to practise with. Save as `bank.py`:

```python
# bank.py
class BankError(Exception):
    """Base class for all errors raised by this module."""


class InsufficientFundsError(BankError):
    def __init__(self, balance: float, amount: float):
        self.balance = balance
        self.amount = amount
        super().__init__(f"Cannot withdraw {amount}: balance is only {balance}")


def withdraw(balance: float, amount: float) -> float:
    if not isinstance(amount, (int, float)):
        raise TypeError("amount must be a number")
    if amount <= 0:
        raise ValueError("amount must be positive")
    if amount > balance:
        raise InsufficientFundsError(balance, amount)
    return balance - amount
```

**Line-by-line:**

- `class BankError(Exception):` creates our own exception type by inheriting from `Exception`. The docstring is enough as a body.
- `class InsufficientFundsError(BankError):` is a more specific error. It stores `balance` and `amount` as attributes so callers (and tests) can inspect them.
- `super().__init__(message)` calls the parent initialiser so `str(error)` returns the message.
- `withdraw` validates in order: type, positive, sufficient funds. Each failure raises a *different, meaningful* exception.

Now the tests:

```python
# test_bank.py
import pytest
from bank import withdraw, InsufficientFundsError, BankError


def test_withdraw_success():
    assert withdraw(100, 30) == 70


def test_non_positive_amount():
    with pytest.raises(ValueError):
        withdraw(100, 0)


def test_wrong_type():
    with pytest.raises(TypeError):
        withdraw(100, "ten")


def test_insufficient_funds():
    with pytest.raises(InsufficientFundsError):
        withdraw(50, 80)
```

### 4. Checking the message with `match`

Catching the right *type* is good; catching the right *message* is better, because the same type can be raised for many reasons.

```python
def test_message_mentions_positive():
    with pytest.raises(ValueError, match="must be positive"):
        withdraw(100, -1)
```

- `match` takes a **regular expression** and uses `re.search` on `str(exception)`. A plain phrase usually works because most ordinary text matches itself.
- Special regex characters such as `.`, `(`, `)`, `[`, `$`, `+`, `?` need escaping. Use `re.escape` when the message contains them:

```python
import re


def test_message_with_special_characters():
    with pytest.raises(InsufficientFundsError, match=re.escape("balance is only 50")):
        withdraw(50, 80)
```

- Anchor with `^` and `$` for exact matches: `match=r"^amount must be positive$"`.

### 5. Inspecting the exception with `excinfo`

Use `as` to capture an **ExceptionInfo** object:

```python
def test_exception_details():
    with pytest.raises(InsufficientFundsError) as excinfo:
        withdraw(50, 80)

    err = excinfo.value          # the actual exception instance
    assert err.balance == 50
    assert err.amount == 80
    assert "80" in str(err)
    assert excinfo.type is InsufficientFundsError
```

- `excinfo.value` is the exception instance, so you can read custom attributes (`balance`, `amount`).
- `excinfo.type` is the class; `excinfo.typename` is its name as text; `excinfo.traceback` is the stack.
- **Place assertions about `excinfo` OUTSIDE the `with` block.** `excinfo` is only filled once the block has exited; and any code *after* the raising line **inside** the block never runs (see mistakes).

In PyTest 8 you can also combine `match` with extra checks using `check=`, which accepts a function that receives the exception and returns a boolean:

```python
def test_with_check_callable():
    with pytest.raises(
        InsufficientFundsError,
        check=lambda e: e.amount > e.balance,
    ):
        withdraw(10, 20)
```

(`check` was added in PyTest 8.4; if you are on an older 8.x release, use `excinfo.value` as shown above. You can see your version with `pytest --version`.)

### 6. Exception hierarchies: catching base classes

`pytest.raises(BankError)` passes for `InsufficientFundsError` too, because it is a subclass:

```python
def test_catches_subclass_via_base():
    with pytest.raises(BankError):
        withdraw(10, 100)
```

Be deliberate. Prefer the **most specific** type that expresses the contract. Use the base class only when the contract really is "some error from this module". Never write `pytest.raises(Exception)` unless you truly do not care: it will also pass when your code has an unrelated bug such as `NameError` or `AttributeError`, hiding real defects. If you must use a broad type, pair it with a strict `match`.

You can also accept several types by passing a tuple:

```python
def test_bad_input_types():
    with pytest.raises((TypeError, ValueError)):
        withdraw(100, None)
```

### 7. Parametrizing exception tests

You already know parametrization (Tuesday) and data-driven design (earlier today). They combine well with exceptions:

```python
import pytest
from bank import withdraw


@pytest.mark.parametrize(
    "balance, amount, exc_type, message",
    [
        pytest.param(100, 0, ValueError, "positive", id="zero-amount"),
        pytest.param(100, -10, ValueError, "positive", id="negative-amount"),
        pytest.param(100, "5", TypeError, "number", id="string-amount"),
        pytest.param(100, None, TypeError, "number", id="none-amount"),
    ],
)
def test_withdraw_rejects_bad_amounts(balance, amount, exc_type, message):
    with pytest.raises(exc_type, match=message):
        withdraw(balance, amount)
```

#### The "value or exception" pattern

Sometimes you want one table containing both successful and failing rows. A neat trick is a *context manager that does nothing*: `contextlib.nullcontext`:

```python
from contextlib import nullcontext as does_not_raise

import pytest
from bank import withdraw


@pytest.mark.parametrize(
    "balance, amount, expected, expectation",
    [
        (100, 30, 70, does_not_raise()),
        (100, 100, 0, does_not_raise()),
        (100, 101, None, pytest.raises(Exception, match="Cannot withdraw")),
        (100, -1, None, pytest.raises(ValueError)),
    ],
)
def test_withdraw_table(balance, amount, expected, expectation):
    with expectation:
        assert withdraw(balance, amount) == expected
```

Here each row carries its own context manager: either "nothing special" or "must raise X". This avoids `if/else` in the test body. The documentation of PyTest shows this exact idiom. Use it when the table is small and readable; for larger suites split positive and negative tests, which is easier to read.

(Note the `pytest.raises(Exception, ...)` with a strict `match` in the third row, to show the "broad type plus strict message" compromise.)

### 8. Testing custom exceptions thoroughly

A custom exception is part of your public contract. Test that:

1. it is raised in the right situation,
2. it inherits from the expected base (so callers' `except BankError` works),
3. it carries the right data and message.

```python
def test_insufficient_funds_inherits_from_bank_error():
    assert issubclass(InsufficientFundsError, BankError)


def test_insufficient_funds_str():
    error = InsufficientFundsError(10, 25)
    assert str(error) == "Cannot withdraw 25: balance is only 10"
```

`issubclass(A, B)` returns `True` if class `A` is `B` or inherits from it.

### 9. Exception chaining (`raise ... from ...`)

Python lets you wrap a low-level exception in a higher-level one while keeping the original as the **cause**:

```python
# config_loader.py
import json


class ConfigError(Exception):
    pass


def load_config(text: str) -> dict:
    try:
        return json.loads(text)
    except json.JSONDecodeError as exc:
        raise ConfigError("Config is not valid JSON") from exc
```

```python
# test_config_loader.py
import json
import pytest
from config_loader import load_config, ConfigError


def test_invalid_json_wraps_original_error():
    with pytest.raises(ConfigError, match="not valid JSON") as excinfo:
        load_config("{bad json")

    assert isinstance(excinfo.value.__cause__, json.JSONDecodeError)
```

- `raise NewError(...) from exc` stores `exc` in `NewError.__cause__`.
- This is useful because users see a friendly error while engineers still see the original problem in the traceback.
- A good test confirms both the friendly error *and* the cause.

### 10. Testing that **no** exception is raised

You do not need a special tool. If code raises unexpectedly, PyTest already fails the test with the traceback. Simply call the code:

```python
def test_valid_withdrawal_does_not_raise():
    result = withdraw(100, 20)
    assert result == 80
```

Writing `try: ... except: pytest.fail()` is unnecessary noise.

### 11. Testing warnings with `pytest.warns`

A **warning** is a softer signal than an exception: the program continues but the developer is advised of something (for example, a deprecated function). Python's `warnings` module issues them.

```python
# legacy.py
import warnings


def old_total(items):
    warnings.warn("old_total() is deprecated, use sum()", DeprecationWarning, stacklevel=2)
    return sum(items)
```

```python
# test_legacy.py
import pytest
from legacy import old_total


def test_old_total_warns():
    with pytest.warns(DeprecationWarning, match="deprecated"):
        result = old_total([1, 2, 3])
    assert result == 6
```

- `pytest.warns(Type, match=...)` passes only if a matching warning is issued inside the block.
- `stacklevel=2` makes the warning point to the *caller's* line rather than inside the function.
- To assert *no* warnings are emitted, use `warnings.catch_warnings` with `simplefilter("error")`, or run with `-W error` to turn warnings into failures across your suite.

### 12. `pytest.fail`, `pytest.skip`, `pytest.xfail`

These functions act on the *test outcome*, not on the code under test. They themselves work by raising special exceptions, which is why the `pytest.raises(Exception)` caution above also matters (PyTest's outcome exceptions derive from `BaseException`, so a broad `except Exception` will not accidentally swallow them).

```python
import sys
import pytest


def test_explicit_fail():
    if 1 + 1 != 2:
        pytest.fail("Mathematics is broken")


def test_skip_at_runtime():
    if sys.version_info < (3, 9):
        pytest.skip("requires Python 3.9+")


def test_xfail_at_runtime():
    pytest.xfail("known defect BUG-42")   # stops the test and marks it xfailed
```

- `pytest.skip(reason)` stops the test and records it as *skipped*; handy when you only know at runtime that conditions are not met.
- `pytest.xfail(reason)` stops immediately and marks as *expected failure*. Prefer the decorator `@pytest.mark.xfail` when the condition is known up front (Monday's Markers lesson).

### 13. `ExceptionGroup` and `pytest.RaisesGroup` (awareness)

Python 3.11 added `ExceptionGroup`, which bundles several exceptions raised concurrently (for example by `asyncio.TaskGroup`). PyTest 8.4 added `pytest.RaisesGroup` to test these. As a beginner you will rarely need it; just know it exists:

```python
# Requires Python 3.11+ and PyTest 8.4+
import pytest


def test_exception_group():
    with pytest.RaisesGroup(ValueError, TypeError):
        raise ExceptionGroup("multiple", [ValueError("a"), TypeError("b")])
```

If your environment is older, skip this section; nothing else depends on it.

### 14. Testing code that handles exceptions internally

Sometimes the function catches the error and returns a fallback value. Then the test is about the **return value**, not about raising:

```python
# safe_math.py
def safe_divide(a, b, default=None):
    try:
        return a / b
    except ZeroDivisionError:
        return default
```

```python
# test_safe_math.py
from safe_math import safe_divide


def test_divide_normal():
    assert safe_divide(10, 2) == 5


def test_divide_by_zero_returns_default():
    assert safe_divide(10, 0, default=-1) == -1
```

To force exceptions from dependencies you cannot easily break (a network call, a file read), use the mocking techniques from Tuesday: `unittest.mock.patch(..., side_effect=SomeError)` makes a patched function raise on demand.

```python
from unittest.mock import patch
import pytest


def read_user(path):
    with open(path) as f:
        return f.read()


def test_read_user_propagates_permission_error():
    with patch("builtins.open", side_effect=PermissionError("denied")):
        with pytest.raises(PermissionError, match="denied"):
            read_user("/secret/file.txt")
```

---

## Real-World Scenarios

1. **Login service.** Tests assert that a wrong password raises `AuthenticationError`, a locked account raises `AccountLockedError`, and neither leaks whether the username exists in its message (a security requirement verified with `match`).
2. **File importer.** A CSV import tool must raise `ImportError_` with the row number when a line is malformed. A parametrized exception test feeds ten malformed files and checks the row number in each message through `excinfo.value`.
3. **Payment gateway wrapper.** Using `side_effect=TimeoutError`, tests prove the wrapper retries and finally raises `PaymentUnavailableError`, without ever calling the real gateway.
4. **UI tests (later this week).** Browser automation also produces timeouts and errors; we will cover how Playwright reports them in depth on Thursday and Friday.

---

## Common Mistakes

| Mistake | Problem | Fix |
|---------|---------|-----|
| Using `try/except` in the test | Test passes even if no exception occurs | Use `pytest.raises` |
| `pytest.raises(Exception)` with no `match` | Passes on unrelated bugs | Use the specific type and/or `match` |
| Code after the raising line inside `with` | It never runs because the block exits at the raise | Put follow-up assertions after the `with` block |
| Asserting on `excinfo` inside the block | `excinfo` is not populated yet | Check it after the block |
| Regex special characters in `match` | Pattern fails unexpectedly | `re.escape(message)` |
| Several risky statements in one `with` block | You cannot tell which one raised | Keep only the single call that should raise |
| Forgetting that messages can change | Brittle tests | Match on stable key words |
| Testing implementation details of error text | Tests break on rephrasing | Test type and key data; use messages sparingly |
| Not testing the "happy path" beside the error path | Code might always raise | Keep positive tests too |

### The "one call in the block" rule illustrated

```python
# Bad: which line raised?
with pytest.raises(ValueError):
    account = create_account(name="Ann")
    withdraw(account.balance, -5)

# Good: the setup is outside, one action inside
account = create_account(name="Ann")
with pytest.raises(ValueError):
    withdraw(account.balance, -5)
```

---

## Practice Exercises

### Exercise 1: First negative test

Given:

```python
def parse_age(text: str) -> int:
    age = int(text)
    if age < 0 or age > 150:
        raise ValueError(f"age out of range: {age}")
    return age
```

Write tests for: `"25"` returns 25; `"abc"` raises `ValueError`; `"-1"` raises `ValueError` with message containing `out of range`; `"151"` likewise.

<details>
<summary>Solution</summary>

```python
import pytest


def parse_age(text: str) -> int:
    age = int(text)
    if age < 0 or age > 150:
        raise ValueError(f"age out of range: {age}")
    return age


def test_valid_age():
    assert parse_age("25") == 25


def test_not_a_number():
    with pytest.raises(ValueError):
        parse_age("abc")


@pytest.mark.parametrize("text", ["-1", "151"])
def test_out_of_range(text):
    with pytest.raises(ValueError, match="out of range"):
        parse_age(text)
```
Note: `"abc"` also raises `ValueError` (from `int`), but its message differs ("invalid literal"), which is why the out-of-range test uses `match`.
</details>

### Exercise 2: Inspect the exception

Write a custom exception `ValidationError(field, reason)` that stores both attributes and builds a message `"<field>: <reason>"`. Write a function `validate_username(name)` that raises it when the name is empty or longer than 20 characters. Test the `field` and `reason` attributes through `excinfo.value`.

<details>
<summary>Hint</summary>
Follow the structure of `InsufficientFundsError`: set `self.field`, `self.reason`, then call `super().__init__(f"{field}: {reason}")`.
</details>

### Exercise 3: Value-or-exception table

Using `nullcontext` as shown in section 7, write a single parametrized test for `parse_age` with two successful rows and two failing rows.

### Exercise 4: Fix the broken test

What is wrong with this test, and how do you fix it?

```python
def test_divide_by_zero():
    with pytest.raises(ZeroDivisionError):
        result = 10 / 0
        assert result == 0
```

<details>
<summary>Answer</summary>
The `assert` line never runs because `10 / 0` raises first. It is dead code and misleading. Remove it. If you wanted to examine the exception, use `as excinfo` and assert after the block.
</details>

### Exercise 5: Chaining

Write `load_int(text)` that wraps `int(text)` and raises a custom `InputError("not an integer") from exc` on failure. Test that the error message matches and that `__cause__` is a `ValueError`.

### Exercise 6: Project 1 negative cases

Take three negative test cases from your Project 1 manual test plan that involve a utility function (invalid input, boundary overflow, wrong type). Automate each with `pytest.raises`, using `match` for at least one and `excinfo` for at least one.

---

## Summary

- Exceptions are Python's way of signalling that something went wrong; negative testing checks that bad input is rejected *correctly*.
- Never use `try/except` in a test to expect an error; use `with pytest.raises(ExpectedError):`.
- Use `match=` (a regex searched in the message) and `excinfo.value` to check the details; assert on `excinfo` after the block.
- Be specific with the exception type; avoid bare `Exception`.
- Parametrize error cases, and use `nullcontext` for tables that mix success and failure.
- Test custom exceptions: raising, inheritance, attributes, and chaining via `__cause__`.
- Use `pytest.warns` for warnings and `mock.patch(side_effect=...)` to force errors from dependencies.
- Keep only the single raising call inside the `with` block.

---

## Additional Resources

- PyTest documentation - Assertions about expected exceptions and warnings: https://docs.pytest.org/en/stable/how-to/assert.html#assertions-about-expected-exceptions
- PyTest documentation - How to capture warnings: https://docs.pytest.org/en/stable/how-to/capture-warnings.html
- Python documentation - Errors and exceptions tutorial: https://docs.python.org/3/tutorial/errors.html
