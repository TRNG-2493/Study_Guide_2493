# Assertions and Assertion Introspection

## Learning Objectives

By the end of this lesson you will be able to:

- Explain what an assertion is and how Python's `assert` statement behaves.
- Write assertions for equality, comparison, membership, identity, truthiness, strings, collections, and floating-point numbers.
- Explain **assertion introspection** (how PyTest rewrites `assert` to show detailed failure information) and read its output fluently.
- Add custom failure messages the right way.
- Use `pytest.approx` for floating-point comparisons.
- Use `pytest.raises` (including `match` and `excinfo`) to verify exceptions, and `pytest.warns` for warnings.
- Avoid the classic assertion traps (tuples, `is` vs `==`, running Python with `-O`).

---

## Why This Matters

A test without an assertion is just a script that runs code. The **assertion is the test**: it is where the expected result from your manual test case becomes an automated check. The quality of your assertions determines:

- **Whether bugs are caught.** Weak assertions (`assert result`) let wrong answers through.
- **How fast bugs are diagnosed.** When a test fails in the nightly build, the failure message is often all the information you have. PyTest's introspection can turn a 20-minute debugging session into a 20-second glance.

In **Project 1: QE Foundations**, you are building a reusable automated suite. Assertions you write today will be reused in Wednesday's custom assertions lesson and in Friday's browser tests (where Playwright adds its own web-first assertions). Understanding PyTest's core assertion behaviour is the foundation for all of them.

---

## The Concept

### 1. What is an assertion?

An **assertion** is a statement that says "this must be true here". If it is true, execution continues. If it is false, an `AssertionError` is raised, and PyTest marks the test as failed.

Python syntax:

```python
assert <condition>
assert <condition>, <optional message>
```

Important: `assert` is a **statement**, not a function. Do not write `assert(condition, "message")`; see Common Mistakes.

### 2. The big idea: use plain `assert`

In `unittest`, you learn a family of methods (`assertEqual`, `assertNotEqual`, `assertIn`, `assertIsNone`, `assertGreater`...). In PyTest you use plain `assert` with normal Python expressions:

| Intent | `unittest` style | PyTest style |
|---|---|---|
| Equal | `self.assertEqual(a, b)` | `assert a == b` |
| Not equal | `self.assertNotEqual(a, b)` | `assert a != b` |
| True | `self.assertTrue(x)` | `assert x` |
| False | `self.assertFalse(x)` | `assert not x` |
| Is None | `self.assertIsNone(x)` | `assert x is None` |
| In | `self.assertIn(a, b)` | `assert a in b` |
| Greater | `self.assertGreater(a, b)` | `assert a > b` |
| Raises | `with self.assertRaises(E):` | `with pytest.raises(E):` |

So how can a plain `assert` give nice messages, when Python's own `assert` just says `AssertionError` with no details? That is the next section.

### 3. Assertion introspection (assertion rewriting)

**Assertion introspection** is PyTest's feature of showing the values of sub-expressions when an assertion fails.

#### How it works

When PyTest imports your test modules, it **rewrites** the compiled code of each `assert` statement (via an import hook, working on the AST, the Abstract Syntax Tree of your code). The rewritten assertion saves intermediate values of the expression into temporary variables and, if the assertion fails, builds a descriptive message from them. You never see this rewriting; you only see its benefits. Details worth knowing:

- Rewriting applies to **test modules**, `conftest.py` files, and plugins. It does **not** apply to ordinary helper modules that you import, unless you register them with `pytest.register_assert_rewrite("helper_module")` (an advanced option you will meet when you build custom assertion helpers on Wednesday).
- Rewritten bytecode is cached in `__pycache__` with a `-pytest-<version>` tag.
- Disable with `--assert=plain` (rarely useful).

#### What you see

Example test:

```python
def test_price_total():
    prices = [10, 20, 30]
    assert sum(prices) == 70
```

Failure output (trimmed):

```
    def test_price_total():
        prices = [10, 20, 30]
>       assert sum(prices) == 70
E       assert 60 == 70
E        +  where 60 = sum([10, 20, 30])
```

Notice what PyTest did for you:

- `>` marks the failing line.
- `E` lines (error lines) show the evaluated comparison `60 == 70`.
- `where 60 = sum([10, 20, 30])` shows exactly which sub-expression produced 60, **including the arguments**.

With plain Python you would only see `AssertionError`, and you would have to add `print` statements. PyTest saves that work.

#### Introspection for different types

**Strings** show a diff pointing to the first difference:

```python
def test_greeting():
    assert "Hello, World" == "Hello, Word"
```

```
E       AssertionError: assert 'Hello, World' == 'Hello, Word'
E         - Hello, Word
E         + Hello, World
E         ?            +
```

The `?` line uses a marker to point at what differs (here, an extra `l`). `-` and `+` lines show expected-versus-actual style diffs (the exact orientation of `-` and `+` is as printed by PyTest's diff of right and left sides).

**Lists** report the first differing index and the length differences:

```python
def test_lists():
    assert [1, 2, 3, 4] == [1, 2, 9, 4]
```

```
E       assert [1, 2, 3, 4] == [1, 2, 9, 4]
E         At index 2 diff: 3 != 9
E         Use -v to get more diff
```

**Dictionaries** list the differing items:

```python
def test_dicts():
    actual = {"name": "Asha", "role": "QA", "level": 1}
    expected = {"name": "Asha", "role": "QE", "level": 1}
    assert actual == expected
```

```
E       AssertionError: assert {'level': 1, 'name': 'Asha', 'role': 'QA'} == {'level': 1, 'name': 'Asha', 'role': 'QE'}
E         Differing items:
E         {'role': 'QA'} != {'role': 'QE'}
E         Use -v to get more diff
```

**Membership** shows the container:

```python
def test_membership():
    assert "admin" in ["guest", "user"]
```

```
E       AssertionError: assert 'admin' in ['guest', 'user']
```

Adding `-v` (verbose) to the command increases how much detail the diffs show; `-vv` shows full diffs for very long items.

### 4. Custom assertion messages

You can attach a message after a comma:

```python
def test_user_is_active():
    status = "disabled"
    assert status == "active", f"Expected user to be active, got {status!r}"
```

Output:

```
E       AssertionError: Expected user to be active, got 'disabled'
E       assert 'disabled' == 'active'
E         - active
E         + disabled
```

PyTest shows your message **and** the introspected detail. Guidelines:

- Add a message when the context is not obvious from the values: `assert response_code == 200, f"Login failed for {username}"`.
- Do not add messages that merely repeat the expression; introspection already does that.
- `!r` in an f-string means "use `repr()`", which shows quotes around strings, making whitespace and type problems visible (`'5'` vs `5`).

### 5. Assertion patterns for everyday checks

#### 5.1 Equality and inequality

```python
assert result == 5
assert name != ""
```

#### 5.2 Comparisons

```python
assert age >= 18
assert 0 <= score <= 100        # chained comparison
```

Python allows chains like `0 <= score <= 100`, a readable boundary check. (PyTest's failure output evaluates it correctly.)

#### 5.3 Truthiness

```python
assert items                     # non-empty list is truthy
assert not errors                # empty list is falsy
```

Truthy/falsy checks are concise but **loose**: `assert result` also passes for `5`, `"x"`, or `[0]`. When you expect exactly `True`, write `assert result is True`.

#### 5.4 Identity: `is` versus `==`

- `==` asks "do they have equal values?"
- `is` asks "are they the exact same object?"

Use `is` only for singletons: `None`, `True`, `False`.

```python
assert value is None
assert flag is True
```

Never use `is` to compare numbers or strings. `assert x is 5` may work by accident in one Python build and fail in another (Python even gives a SyntaxWarning).

#### 5.5 Membership

```python
assert "@" in email
assert "error" not in log_text.lower()
assert 3 in {1, 2, 3}
```

#### 5.6 Strings

```python
assert text.startswith("Order")
assert text.endswith(".csv")
assert "total" in text.lower()
assert len(text) == 8
```

#### 5.7 Collections

```python
assert len(users) == 3
assert sorted(names) == ["Asha", "Ben", "Chen"]   # order-independent check
assert set(a) == set(b)                           # same members, ignoring order and duplicates
assert all(price > 0 for price in prices)         # every item satisfies a rule
assert any(u["role"] == "admin" for u in users)   # at least one satisfies
```

`all(...)` and `any(...)` take a generator expression. Be aware that on failure, PyTest's introspection of `all` and `any` is richer than a plain `assert` would give, but for large collections a loop with a message for the offending item can be clearer:

```python
for price in prices:
    assert price > 0, f"Invalid price found: {price}"
```

#### 5.8 Types

```python
assert isinstance(result, int)
assert type(result) is int      # stricter: excludes subclasses such as bool
```

Note that `isinstance(True, int)` is `True` because `bool` is a subclass of `int`. That surprises many beginners.

### 6. Floating-point numbers and `pytest.approx`

Binary floating point cannot represent most decimals exactly:

```python
>>> 0.1 + 0.2
0.30000000000000004
>>> 0.1 + 0.2 == 0.3
False
```

Use `pytest.approx`:

```python
import pytest

def test_float_sum():
    assert 0.1 + 0.2 == pytest.approx(0.3)
```

Customising tolerances:

```python
assert 100.0 == pytest.approx(100.4, rel=0.01)     # within 1% relative tolerance
assert 100.0 == pytest.approx(100.4, abs=0.5)      # within 0.5 absolute
```

- `rel` is relative tolerance (a fraction of the expected value).
- `abs` is absolute tolerance.
- If neither is given, defaults are `rel=1e-6` and `abs=1e-12`.

It also works for lists, tuples, and dictionaries of numbers:

```python
assert [0.1 + 0.2, 0.2 + 0.4] == pytest.approx([0.3, 0.6])
assert {"a": 0.1 + 0.2} == pytest.approx({"a": 0.3})
```

For money, consider Python's `decimal.Decimal` instead of floats; that is a design decision outside today's scope.

### 7. Testing exceptions with `pytest.raises`

Sometimes the **correct** behaviour is an error. `pytest.raises` verifies that a specific exception is raised.

#### Basic form

```python
import pytest

def test_int_conversion_error():
    with pytest.raises(ValueError):
        int("not a number")
```

The test passes only if a `ValueError` (or subclass) is raised inside the `with` block. If no exception occurs, PyTest fails the test with `DID NOT RAISE`.

#### Checking the message with `match`

```python
def test_error_message():
    with pytest.raises(ValueError, match=r"invalid literal for int\(\)"):
        int("abc")
```

`match` is a **regular expression** searched in the string form of the exception (`re.search`). Because regular expressions treat `(` and `)` specially, we escape them with backslashes and use a raw string (`r"..."`). For a literal match of arbitrary text, use `re.escape()`:

```python
import re
with pytest.raises(ValueError, match=re.escape("cost (USD) invalid")):
    ...
```

#### Inspecting the exception with `excinfo`

```python
def test_error_details():
    with pytest.raises(KeyError) as excinfo:
        {"a": 1}["b"]

    assert excinfo.type is KeyError
    assert "b" in str(excinfo.value)
```

`excinfo` is an `ExceptionInfo` object with:

- `excinfo.type`: the exception class.
- `excinfo.value`: the exception instance.
- `excinfo.traceback`: the traceback.

**Important:** access `excinfo` *after* the `with` block ends, not inside it.

#### Multiple acceptable types

```python
with pytest.raises((TypeError, ValueError)):
    int(None)
```

Pass a tuple when more than one exception type is acceptable (use sparingly; precise tests are better).

#### Checking that no exception occurs

You do not need a special construct; if the code raises, the test fails with the exception's traceback, which is exactly what you want.

(We will go deeper into exception testing, including custom exceptions and exception chains, on Wednesday in *Exception Testing*.)

### 8. Testing warnings with `pytest.warns`

```python
import warnings
import pytest

def old_function():
    warnings.warn("old_function is deprecated", DeprecationWarning)
    return 1

def test_deprecation_warning():
    with pytest.warns(DeprecationWarning, match="deprecated"):
        assert old_function() == 1
```

### 9. Soft versus hard assertions

PyTest assertions are **hard**: at the first failure the test stops. Anything after it in that test is not executed. This is another reason for small tests. (If you really need to check several independent things and see all failures, split into multiple tests, or later in the week learn about parametrization.) Third-party plugins such as `pytest-check` provide soft assertions, but they are out of scope for now.

---

## Code Examples with Line-by-Line Explanations

### Example 1: A gallery of assertions

```python
import pytest


def test_assertion_gallery():
    # equality and inequality
    assert 3 + 4 == 7
    assert "qa" != "QA"

    # comparisons
    assert 5 > 3
    assert 0 <= 50 <= 100

    # truthiness
    assert [1]
    assert not []

    # identity, only for None/True/False
    nothing = None
    assert nothing is None

    # membership
    assert "ana" in "banana"
    assert 4 not in [1, 2, 3]

    # strings
    assert "report.csv".endswith(".csv")

    # collections
    assert sorted([3, 1, 2]) == [1, 2, 3]
    assert set("hello") == set("olleh")
    assert all(n > 0 for n in [1, 2, 3])
    assert any(n % 2 == 0 for n in [1, 2, 3])

    # floats
    assert 0.1 + 0.2 == pytest.approx(0.3)

    # types
    assert isinstance(3.5, float)
```

Explanation of key lines:

- `assert 0 <= 50 <= 100` is a chained comparison, equivalent to `0 <= 50 and 50 <= 100`.
- `assert [1]` passes because a non-empty list is truthy; `assert not []` passes because an empty list is falsy.
- `"ana" in "banana"` is a substring check for strings.
- `set("hello") == set("olleh")` turns strings into sets of characters; sets ignore order and duplicates.
- `all(n > 0 for n in [...])` uses a generator expression; `all` returns `True` only if every element is truthy.

*Teaching note:* In real tests, split a gallery like this into small tests. It is combined here for demonstration only.

### Example 2: Reading a failure

Make this test fail on purpose:

```python
def test_inventory_counts():
    inventory = {"apples": 5, "pears": 2}
    expected = {"apples": 5, "pears": 3}
    assert inventory == expected
```

Run `python -m pytest -v` and read the output: PyTest lists `Differing items: {'pears': 2} != {'pears': 3}`. Reading approach:

1. Find the `>` line (the failing assertion).
2. Read the `E` lines from top to bottom.
3. Identify actual versus expected.
4. Decide: is the code wrong, or the test's expectation wrong?

Step 4 matters: a failing test is not automatically a code bug; sometimes the requirement changed and the test needs updating.

### Example 3: Custom message with context

```python
def test_all_prices_are_positive():
    prices = {"pen": 10, "book": -5, "bag": 40}
    for item, price in prices.items():
        assert price > 0, f"Price for {item!r} must be positive, got {price}"
```

Explanation: the loop checks each item. On failure, the message names the exact item (`'book'`) and its value (`-5`). With a bare `all(...)` you would only learn that *some* price was bad.

### Example 4: `pytest.raises` with `match` and `excinfo`

```python
import pytest


def withdraw(balance, amount):
    if amount <= 0:
        raise ValueError("Withdrawal amount must be positive")
    if amount > balance:
        raise ValueError(f"Insufficient funds: balance {balance}, requested {amount}")
    return balance - amount


def test_withdraw_valid_amount():
    assert withdraw(100, 30) == 70


def test_withdraw_negative_amount_raises():
    with pytest.raises(ValueError, match="must be positive"):
        withdraw(100, -5)


def test_withdraw_too_much_reports_details():
    with pytest.raises(ValueError) as excinfo:
        withdraw(50, 80)

    message = str(excinfo.value)
    assert "Insufficient funds" in message
    assert "50" in message and "80" in message
```

Explanation:

- `withdraw` validates inputs, then computes. Two different failure reasons raise the same exception type with different messages, which is why checking the message matters. Checking only the type could pass for the wrong reason.
- In the second test, `match="must be positive"` is a regex; plain words work as-is.
- In the third, `as excinfo` stores details; `str(excinfo.value)` gives the message text. The assertions run **after** the `with` block.

### Example 5: Comparing numbers in a calculation

```python
import pytest


def average(numbers):
    return sum(numbers) / len(numbers)


def test_average_of_floats():
    assert average([0.1, 0.2, 0.3]) == pytest.approx(0.2)


def test_average_with_loose_tolerance():
    assert average([1, 2, 2]) == pytest.approx(1.67, abs=0.01)
```

The exact average of `[1, 2, 2]` is `1.6666...`; the absolute tolerance of `0.01` accepts `1.67`.

---

## Real-World Scenarios

1. **Overnight failure triage.** A nightly build fails with `assert 'Pending' == 'Shipped'` plus `where 'Pending' = order.status`. The engineer immediately knows the order never advanced, without rerunning anything.
2. **Financial totals.** A cart total is `19.99 * 3`. In floating point this is `59.97` or `59.969999999999995`. Teams assert with `pytest.approx(59.97)` (or use `Decimal`) so tests do not fail for meaningless rounding noise.
3. **Validation rules.** An API must reject empty usernames with a specific message. Tests use `pytest.raises(..., match=...)` to ensure users see a helpful message, not just any error.
4. **Data quality.** After an import, `assert len(rows) == expected_count, f"Imported {len(rows)} rows from {filename}"` provides context for non-obvious failures.

---

## Common Mistakes

| Mistake | Why it is wrong | Fix |
|---|---|---|
| `assert(x == 1, "message")` | A non-empty tuple is always truthy; the assertion never fails (Python warns) | `assert x == 1, "message"` |
| `assert result` when you mean exactly `True` | Passes for any truthy value | `assert result is True` |
| `assert x is 5` or `is "abc"` | `is` checks identity, not value | Use `==` |
| `assert a == b` for floats | Rounding noise | `pytest.approx` |
| Reading `excinfo` inside the `with` block | It is not populated until the block exits | Read it after the block |
| `pytest.raises(Exception)` | Too broad; hides the wrong error | Use the most specific exception class and a `match` |
| Messages that repeat the code | Noise | Add context, not repetition |
| Forgetting to escape regex characters in `match` | `match="price (USD)"` treats parentheses as a group | Use `re.escape` or a raw string with backslashes |
| Putting assertions in helper functions in non-test modules and expecting rich output | Helper modules are not rewritten by default | Keep asserts in test files, or use `pytest.register_assert_rewrite` (Wednesday) |
| Running Python with `-O` | Asserts are stripped out entirely | Do not use `-O` when running tests |
| One giant test with many assertions | Stops at first failure | Split into focused tests |

---

## Practice Exercises

### Exercise 1: Choose the right assertion
Write one assertion for each statement:

1. The variable `username` is not an empty string.
2. The list `errors` is empty.
3. `response` is `None`.
4. The value `score` is between 0 and 100 inclusive.
5. The string `email` contains an `@`.
6. `0.7 + 0.1` equals `0.8` (floating point safe).

**Solution:**

```python
assert username != ""          # or: assert username
assert not errors              # or: assert errors == []
assert response is None
assert 0 <= score <= 100
assert "@" in email
assert 0.7 + 0.1 == pytest.approx(0.8)
```

### Exercise 2: Read the failure
Write this test, run it, and answer the questions below from the output alone.

```python
def test_report():
    expected = ["login", "search", "checkout"]
    actual = ["login", "serch", "checkout"]
    assert actual == expected
```

1. At which index do the lists differ?
2. Which side contains the typo?

*Answer:* index 1; the `actual` (left) side has `'serch'`.

### Exercise 3: Exceptions
Write `def safe_sqrt(x)` that raises `ValueError("cannot take square root of a negative number")` when `x < 0` and otherwise returns `x ** 0.5`. Write tests:

1. `safe_sqrt(9)` is `3.0`.
2. `safe_sqrt(2)` is approximately `1.41421356`.
3. `safe_sqrt(-1)` raises `ValueError` with a message containing "negative".

### Exercise 4: Improve a weak test
This test is weak. Improve it using stronger assertions and a helpful message.

```python
def test_get_users():
    users = get_users()
    assert users
```

*Hint (one improved version):*

```python
def test_get_users_returns_list_of_dicts_with_names():
    users = get_users()
    assert isinstance(users, list)
    assert len(users) > 0, "Expected at least one user"
    assert all("name" in user for user in users)
```

### Exercise 5: Warnings
Write a function that issues a `UserWarning("low balance")` when balance is below 10, and a test with `pytest.warns` verifying it.

### Exercise 6: Trap detection
Without running it, explain why this test cannot fail, then fix it.

```python
def test_trap():
    total = 2 + 2
    assert (total == 5, "total should be 5")
```

*Answer:* it asserts a two-item tuple, which is always truthy. Fix: `assert total == 5, "total should be 5"` (which will then correctly fail).

### Exercise 7 (challenge): Project 1 assertions
For two Project 1 utilities, write at least six assertions that use at least four different assertion styles from this lesson (equality, membership, approx, raises, isinstance, all/any). Deliberately break one and paste the introspected failure output into your notes, annotating what each `E` line tells you.

---

## Summary

- An assertion checks that something is true; a false assertion raises `AssertionError` and the test fails.
- PyTest uses **plain `assert`** with ordinary Python expressions: no special methods to memorise.
- **Assertion introspection** rewrites asserts at import time so failures show evaluated sub-expressions, string diffs, list index differences, and dictionary item differences; use `-v` or `-vv` for more detail.
- Add messages for context (`assert x, f"..."`), not repetition; never wrap the condition and message in parentheses together.
- Use `is` only for `None`/`True`/`False`; use `==` for values; use `pytest.approx` for floats.
- Use `pytest.raises` (with `match`, and `excinfo` read after the block) to test expected exceptions, and `pytest.warns` for warnings.
- Assertions are hard: the first failure stops the test, so keep tests small and focused.
- Wednesday's *Custom Assertions* and *Exception Testing* lessons build on these ideas.

---

## Additional Resources

- PyTest: How to write and report assertions in tests: https://docs.pytest.org/en/stable/how-to/assert.html
- PyTest API reference (`pytest.raises`, `pytest.approx`, `pytest.warns`): https://docs.pytest.org/en/stable/reference/reference.html
- Python docs: the `assert` statement: https://docs.python.org/3/reference/simple_stmts.html#the-assert-statement
