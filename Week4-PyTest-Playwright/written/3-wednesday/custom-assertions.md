# Custom Assertions

## Learning Objectives

By the end of this lesson you will be able to:

- Explain why plain `assert` is sometimes not enough and when a **custom assertion** helps.
- Write reusable assertion helper functions that produce clear, actionable failure messages.
- Use `__tracebackhide__ = True` so failures point at the test, not at your helper.
- Write assertions with custom messages, and understand how they interact with PyTest's assertion introspection.
- Compare floating point numbers safely with `pytest.approx`.
- Build domain-specific assertions (for example `assert_valid_email`, `assert_response_ok`, `assert_dict_subset`).
- Collect several checks into one report using a "soft assertion" pattern, and understand its trade-offs.
- Use `pytest_assertrepr_compare` in `conftest.py` to customise how PyTest explains a failed comparison.

---

## Why This Matters

This week's epic is to grow from PyTest basics to a **reporting framework** for Project 1 – QE Foundations. A framework is more than a pile of tests; it is a set of shared building blocks that make tests short, consistent and easy to diagnose.

Think about what happens at 6 p.m. when a nightly run fails. The person looking at the report may not be the one who wrote the test. A message such as:

```
AssertionError: assert False
```

tells them nothing. A message such as:

```
AssertionError: Email 'bob@@example.com' is invalid: contains more than one '@'
```

tells them what was wrong and probably where to look. Custom assertions are the tool that turns *"it failed"* into *"here is exactly what and why"*, and they also eliminate duplicated checking code across your test suite.

---

## The Concept

### 1. A quick recap: PyTest's `assert`

On Monday you learned *Assertions and assertion introspection*. In short:

- You write a normal Python `assert` statement: `assert actual == expected`.
- PyTest rewrites your test modules at import time so that when an assertion fails, it displays the values of sub-expressions, diffs for lists/dicts/strings, and so on.

```python
def test_sum():
    values = [1, 2, 3]
    assert sum(values) == 7
```

Failure output (abridged):

```
>       assert sum(values) == 7
E       assert 6 == 7
E        +  where 6 = sum([1, 2, 3])
```

That is already helpful. So **when do we need more?**

1. The same multi-line check appears in many tests (duplication).
2. The check has a business meaning that deserves a name (`assert_valid_email`).
3. The built-in message does not explain *why* the check failed (for example `assert is_valid(x)` just shows `False`).
4. You are comparing objects PyTest cannot explain well (custom classes).
5. Floating point numbers or other "approximately equal" values.

### 2. Assertion messages: the simplest customization

Python's `assert` accepts an optional message after a comma:

```python
assert condition, "message shown if the condition is false"
```

```python
def test_age_is_adult():
    age = 17
    assert age >= 18, f"Expected an adult but age was {age}"
```

Failure output:

```
E       AssertionError: Expected an adult but age was 17
E       assert 17 >= 18
```

**Line-by-line:**

- `assert age >= 18` is the condition.
- `, f"..."` is an *f-string*: a string where `{age}` is replaced by the variable's value.
- PyTest shows your message **and** its own introspection.

**Important gotcha: never put the message in parentheses with the condition.**

```python
assert (age >= 18, "message")   # WRONG: a non-empty tuple is always truthy!
```

This assertion can never fail. Python even raises a `SyntaxWarning` for it. Always write `assert condition, "message"`.

### 3. Writing a helper function that asserts

A **custom assertion** is simply a function whose name starts with `assert_` (convention) that raises `AssertionError` when something is wrong. No framework magic is required.

```python
# helpers/assertions.py
import re

EMAIL_PATTERN = re.compile(r"^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}$")


def assert_valid_email(value):
    """Fail with a clear message unless value looks like an email address."""
    assert isinstance(value, str), f"Email must be a str, got {type(value).__name__}"
    assert EMAIL_PATTERN.match(value), f"'{value}' is not a valid email address"
```

Using it:

```python
# test_signup.py
from helpers.assertions import assert_valid_email


def test_generated_email_is_valid():
    generated = "alice@example.com"
    assert_valid_email(generated)
```

**Explanation:**

- `re.compile(...)` pre-builds a regular expression. `^` means "start of the string"; `[A-Za-z0-9._%+-]+` means "one or more of these characters"; `@` is a literal at sign; `\.` is a literal dot; `[A-Za-z]{2,}$` means "two or more letters until the end". This is deliberately a simplified pattern for teaching; real-world email validation is more complex.
- `isinstance(value, str)` checks the type first, because calling `.match` on `None` would raise a confusing `TypeError` rather than a clear failure.
- Two small asserts give two clear messages; the first check protects the second.

Create an empty `helpers/__init__.py`, or better, place helpers where your `pythonpath` setting can find them (covered in *Test organization and reusable templates*).

### 4. Hiding the helper from the traceback with `__tracebackhide__`

When a helper function fails, PyTest's traceback shows lines from the helper first, which makes the reader dig. PyTest supports a special local variable:

```python
def assert_valid_email(value):
    __tracebackhide__ = True
    assert isinstance(value, str), f"Email must be a str, got {type(value).__name__}"
    assert EMAIL_PATTERN.match(value), f"'{value}' is not a valid email address"
```

Setting `__tracebackhide__ = True` tells PyTest to omit this frame from failure reports, so the traceback points at the **line in the test** that called the helper. It does not affect correctness, only readability. Use it in every assertion helper.

Compare the outputs:

Without it:

```
test_signup.py:6: in test_bad_email
    assert_valid_email("bob@@example.com")
helpers/assertions.py:9: in assert_valid_email
    assert EMAIL_PATTERN.match(value), ...
E   AssertionError: 'bob@@example.com' is not a valid email address
```

With it:

```
test_signup.py:6: in test_bad_email
    assert_valid_email("bob@@example.com")
E   AssertionError: 'bob@@example.com' is not a valid email address
```

### 5. Important: assertion rewriting in helper modules

PyTest's introspection (the nice `where 6 = sum(...)` output) works by *rewriting* test modules, `conftest.py` files, and plugins. Plain helper modules imported by tests are **not** rewritten by default, so a bare `assert x == y` inside `helpers/assertions.py` would show only `AssertionError` without details.

You have two options:

1. Include explicit messages in helper asserts (as we did above). This is the simplest and most reliable approach.
2. Ask PyTest to rewrite your helper module by calling `pytest.register_assert_rewrite("helpers.assertions")` **before** the module is imported, usually at the top of the root `conftest.py`:

```python
# conftest.py
import pytest

pytest.register_assert_rewrite("helpers.assertions")
```

Option 2 gives you rich introspection inside helpers. Many frameworks do both: rewrite helpers and add custom messages for domain context.

### 6. Raising `pytest.fail` instead of `assert`

`assert` can be disabled when Python runs with the `-O` flag, and it is limited to a boolean check. For helper functions that perform complex checks, `pytest.fail(msg)` is an explicit alternative that always fails the test:

```python
import pytest


def assert_no_duplicates(items):
    __tracebackhide__ = True
    seen = set()
    duplicates = []
    for item in items:
        if item in seen:
            duplicates.append(item)
        seen.add(item)
    if duplicates:
        pytest.fail(f"Duplicate items found: {sorted(set(duplicates))}", pytrace=False)
```

- `pytest.fail(reason)` immediately fails the test with the given message.
- `pytrace=False` removes the Python traceback and prints only the message; this is neat for domain-level failures. Omit it if you want the trace.
- The loop collects *all* duplicates rather than stopping at the first, which makes the message more useful.

### 7. Comparing floats with `pytest.approx`

Computers store decimals in binary, so some numbers cannot be stored exactly:

```python
>>> 0.1 + 0.2
0.30000000000000004
>>> 0.1 + 0.2 == 0.3
False
```

A test written as `assert 0.1 + 0.2 == 0.3` would fail for a reason unrelated to your code. PyTest provides `approx`:

```python
import pytest


def test_float_addition():
    assert 0.1 + 0.2 == pytest.approx(0.3)


def test_with_custom_tolerance():
    assert 100.04 == pytest.approx(100.0, abs=0.05)      # absolute tolerance
    assert 1050 == pytest.approx(1000, rel=0.05)         # relative tolerance (5 percent)


def test_approx_works_on_collections():
    assert [0.1 + 0.2, 0.2 + 0.4] == pytest.approx([0.3, 0.6])
    assert {"a": 0.1 + 0.2} == pytest.approx({"a": 0.3})
```

- By default `approx` uses a relative tolerance of 1e-6 (and an absolute tolerance of 1e-12). `abs=` and `rel=` override them.
- Works on numbers, lists, tuples, dicts and NumPy arrays.
- **Use `approx` for money calculations only if you are using floats**; for exact money maths prefer Python's `decimal.Decimal`.

You can build a custom assertion on top of it:

```python
import pytest


def assert_price_close(actual, expected, cents=1):
    __tracebackhide__ = True
    tolerance = cents / 100
    assert actual == pytest.approx(expected, abs=tolerance), (
        f"Price {actual} differs from {expected} by more than {tolerance:.2f}"
    )
```

### 8. Domain-specific assertions

Domain assertions encode business rules once. Imagine Project 1 has a "user record" represented as a dictionary:

```python
# helpers/assertions.py (continued)
def assert_dict_subset(actual: dict, expected_subset: dict):
    """Every key/value in expected_subset must be present in actual."""
    __tracebackhide__ = True
    missing = [k for k in expected_subset if k not in actual]
    assert not missing, f"Missing keys: {missing}. Actual keys: {sorted(actual)}"

    mismatches = {
        k: (actual[k], v)
        for k, v in expected_subset.items()
        if actual[k] != v
    }
    assert not mismatches, (
        "Value mismatches (actual, expected): "
        + ", ".join(f"{k}={pair}" for k, pair in mismatches.items())
    )
```

```python
def test_user_record():
    user = {"id": 7, "name": "Ana", "role": "tester", "created": "2025-01-01"}
    assert_dict_subset(user, {"name": "Ana", "role": "tester"})
```

**Explanation of the comprehension syntax:**

- `[k for k in expected_subset if k not in actual]` builds a list of keys that are expected but absent.
- `{k: (actual[k], v) for k, v in expected_subset.items() if actual[k] != v}` builds a dict of keys whose values differ, storing a tuple of both values.
- The test does not care about the other keys (`id`, `created`), which is why it is called a *subset* assertion. This is helpful because things like IDs and timestamps change between runs.

Another popular example is an API-response assertion. We simulate the response with a small class so no network is needed:

```python
from dataclasses import dataclass, field


@dataclass
class FakeResponse:
    status_code: int
    body: dict = field(default_factory=dict)
    elapsed_ms: int = 0


def assert_response_ok(response, max_ms=500):
    __tracebackhide__ = True
    assert response.status_code == 200, (
        f"Expected status 200 but got {response.status_code}; body={response.body}"
    )
    assert response.elapsed_ms <= max_ms, (
        f"Response took {response.elapsed_ms} ms, limit is {max_ms} ms"
    )


def test_response_ok():
    assert_response_ok(FakeResponse(200, {"ok": True}, elapsed_ms=120))
```

Because the helper includes the body in the message, a failing nightly run already contains the server's error text; nobody needs to re-run the test to find out.

### 9. Designing good custom assertions: a checklist

1. **Name it by behaviour:** `assert_user_is_active`, not `check1`.
2. **Do one logical thing.** A helper checking six unrelated things hides which one failed.
3. **Include actual and expected values** in the message.
4. **Fail early on wrong types** with clear messages instead of obscure `TypeError`s.
5. **Set `__tracebackhide__ = True`.**
6. **Do not swallow exceptions.** Do not wrap the check in `try/except` and return `False`; an assertion helper should raise.
7. **Keep helpers pure.** No hidden network calls, sleeps, or global state.
8. **Test the helper itself** (see section 12). Helpers are code, and code has bugs.

### 10. Soft assertions: collecting multiple failures

A normal `assert` stops the test at the first failure. Sometimes (for example, validating twelve fields on a form) you would prefer to **see all failures at once**. A *soft assertion* collects failures and reports them together at the end.

PyTest has no built-in soft assert, but a tiny context-based helper is easy to write using a fixture (you learned fixtures on Tuesday):

```python
# conftest.py
import pytest


class SoftAssert:
    def __init__(self):
        self._errors = []

    def check(self, condition, message):
        if not condition:
            self._errors.append(message)

    def equal(self, actual, expected, label=""):
        if actual != expected:
            self._errors.append(f"{label}: expected {expected!r}, got {actual!r}")

    def assert_all(self):
        __tracebackhide__ = True
        if self._errors:
            joined = "\n  - ".join(self._errors)
            pytest.fail(f"{len(self._errors)} soft assertion(s) failed:\n  - {joined}", pytrace=False)


@pytest.fixture
def soft():
    s = SoftAssert()
    yield s            # the test runs here
    s.assert_all()     # teardown: raise if anything failed
```

```python
# test_soft.py
def test_profile_fields(soft):
    profile = {"name": "Ana", "age": 30, "country": "PT"}
    soft.equal(profile["name"], "Ana", "name")
    soft.equal(profile["age"], 31, "age")           # will fail
    soft.equal(profile["country"], "ES", "country")  # will fail too
```

Output (abridged):

```
E   Failed: 2 soft assertion(s) failed:
E     - age: expected 31, got 30
E     - country: expected 'ES', got 'PT'
```

**Explanation:**

- `class SoftAssert` stores errors in a list instead of raising immediately.
- The fixture uses `yield`: code before `yield` is setup, code after is teardown. `soft.assert_all()` runs *after* the test body and raises the combined failure.
- `{expected!r}` formats using `repr()`, which shows quotes around strings so `'30'` and `30` are distinguishable.

**Trade-offs:** if a failure occurs in teardown, PyTest reports it as an *error* rather than a *failure* in some reports, which can confuse people. An alternative is to call `soft.assert_all()` explicitly as the last line of the test. Also, do not use soft assertions where later steps depend on earlier ones (if login failed, checking the dashboard is pointless). A well-known plugin, `pytest-check`, offers a polished version of this idea; you may explore it as extra reading.

### 11. Customizing PyTest's failure explanation: `pytest_assertrepr_compare`

If you compare instances of your own class with `==`, PyTest shows only their default `repr`. PyTest provides a hook that lets you add explanation lines. Place it in `conftest.py`:

```python
# conftest.py
from dataclasses import dataclass


@dataclass
class Money:
    amount: int      # in cents
    currency: str


def pytest_assertrepr_compare(op, left, right):
    if isinstance(left, Money) and isinstance(right, Money) and op == "==":
        return [
            "Money objects differ:",
            f"   amount:   {left.amount} != {right.amount}",
            f"   currency: {left.currency} != {right.currency}",
        ]
```

Now a failing test:

```python
def test_money_equal():
    assert Money(500, "USD") == Money(500, "EUR")
```

produces:

```
E       assert Money objects differ:
E            amount:   500 != 500
E            currency: USD != EUR
```

**Explanation:**

- `pytest_assertrepr_compare` is a *hook*: PyTest calls a function with this exact name if it exists in a `conftest.py` or plugin. (Hooks are an advanced PyTest topic; for now just remember that the name and parameters must match exactly.)
- `op` is the operator as a string (`"=="`, `"!="`, `"in"`...), `left` and `right` are the compared objects.
- It returns a list of strings, the first being a summary, or returns `None` to let PyTest explain as usual.
- In real projects you would import `Money` from your application code instead of defining it in `conftest.py`; we define it here only to keep the example runnable in one file.

### 12. Testing your assertion helpers

A custom assertion that never fails is worse than none. Verify it both ways:

```python
# test_assertion_helpers.py
import pytest
from helpers.assertions import assert_valid_email, assert_dict_subset


def test_valid_email_passes():
    assert_valid_email("alice@example.com")  # should not raise


@pytest.mark.parametrize("bad", ["", "no-at-sign", "bob@@example.com", "a@b"])
def test_invalid_email_fails(bad):
    with pytest.raises(AssertionError, match="not a valid email"):
        assert_valid_email(bad)


def test_dict_subset_reports_missing_key():
    with pytest.raises(AssertionError, match="Missing keys"):
        assert_dict_subset({"a": 1}, {"b": 2})
```

`pytest.raises(AssertionError, match=...)` is the exception-testing tool we will study in detail in the next lesson, *Exception testing*. For now: the `with` block passes only if the code inside raises the stated exception whose message matches the regular expression.

---

## Real-World Scenarios

1. **E-commerce checkout.** A team writes `assert_order_total(order, expected_total)` that checks line items, discounts, tax and shipping. Fifty tests use it; when the tax rules change, one helper is edited.
2. **API regression suite.** `assert_response_ok` always includes status, body and response time in its failure message, so on-call engineers can triage from the CI log alone.
3. **Data migration verification.** A soft-assertion helper compares 30 columns of a migrated record and lists every mismatching column in one report instead of making the tester re-run 30 times.
4. **Browser tests (later this week).** UI frameworks add helpers such as `assert_element_visible`. We will cover browser automation in depth on Thursday and Friday; Playwright also ships its own assertions, which you will meet then.

---

## Common Mistakes

| Mistake | Explanation | Fix |
|---------|-------------|-----|
| `assert (cond, "msg")` | A non-empty tuple is always true; the check never runs | `assert cond, "msg"` |
| Using `==` for floats | Binary rounding errors | `pytest.approx` |
| Forgetting `__tracebackhide__` | Reports point at helper internals | Add it as the first line |
| Helper returns `True`/`False` and test forgets to assert | Test passes silently | Make helpers raise, named `assert_...` |
| Over-broad helpers | One helper checks everything; hard to diagnose | Several small, named helpers |
| Messages without values | "Invalid value" | Include actual and expected values |
| Never testing the helper | Helper bug hides real bugs | Positive and negative tests for the helper |
| Soft assertions for dependent steps | Cascading meaningless failures | Use normal asserts when steps depend on each other |
| Expecting rich introspection inside non-rewritten helpers | Only `AssertionError` shown | `pytest.register_assert_rewrite` or explicit messages |

---

## Practice Exercises

### Exercise 1: Message practice

Rewrite the following so that a failure explains itself, using an f-string:

```python
def test_cart_total():
    total = compute_total([10, 20, 30])
    assert total == 70
```

<details>
<summary>Solution</summary>

```python
def compute_total(items):
    return sum(items)


def test_cart_total():
    items = [10, 20, 30]
    total = compute_total(items)
    assert total == 70, f"Total for {items} was {total}, expected 70"
```
(The test fails on purpose because the real total is 60; check that the message is readable, then fix the expected value.)
</details>

### Exercise 2: Build `assert_between`

Write `assert_between(value, low, high)` that passes when `low <= value <= high` and otherwise fails with a message like `Value 12 is not between 1 and 10`. Include `__tracebackhide__`. Add tests for the pass case, the lower boundary, the upper boundary and both sides of failure.

<details>
<summary>Solution</summary>

```python
import pytest


def assert_between(value, low, high):
    __tracebackhide__ = True
    assert low <= value <= high, f"Value {value} is not between {low} and {high}"


@pytest.mark.parametrize("v", [1, 5, 10])
def test_between_passes(v):
    assert_between(v, 1, 10)


@pytest.mark.parametrize("v", [0, 11, -3])
def test_between_fails(v):
    with pytest.raises(AssertionError, match="is not between"):
        assert_between(v, 1, 10)
```
</details>

### Exercise 3: Floating point

Write a test that checks the average of `[0.1, 0.2, 0.3]` equals `0.2` using `pytest.approx`. Then demonstrate that the same test with `==` fails or is fragile (try it in a Python shell first).

*Hint:* `sum([0.1, 0.2, 0.3]) / 3`.

### Exercise 4: Soft assertion

Using the `soft` fixture from section 10, write a test that validates four fields of a dictionary and deliberately has two wrong expectations. Confirm that both failures appear in one report.

### Exercise 5: Project 1 helper

Pick a rule from your Project 1 test plan (for example "password must contain a digit and an uppercase letter"). Write `assert_strong_password(pw)` that reports **which** rule(s) failed in its message. Write one parametrized positive test and one parametrized negative test for the helper itself.

*Hint:* build a list of failed rules, then `assert not failed, f"Password failed: {failed}"`.

---

## Summary

- Plain `assert` plus PyTest introspection is great; custom assertions add **reuse, naming and richer messages**.
- Add a message with `assert condition, "message"`; never wrap the pair in parentheses.
- Set `__tracebackhide__ = True` in helpers so reports point at the test.
- Helper modules are not rewritten by default; use explicit messages or `pytest.register_assert_rewrite`.
- Use `pytest.approx` for floats, and `pytest.fail` for explicit failures.
- Domain helpers (`assert_valid_email`, `assert_dict_subset`, `assert_response_ok`) encode business rules once.
- Soft assertions report multiple failures at once but are inappropriate for dependent steps.
- `pytest_assertrepr_compare` customises failure explanations for your own types.
- Always test your helpers.

---

## Additional Resources

- PyTest documentation - Assertions: https://docs.pytest.org/en/stable/how-to/assert.html
- PyTest API reference - `pytest.approx`, `pytest.fail`, `pytest.register_assert_rewrite`: https://docs.pytest.org/en/stable/reference/reference.html
- Python documentation - The `assert` statement: https://docs.python.org/3/reference/simple_stmts.html#the-assert-statement
