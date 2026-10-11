# Test Functions and Classes

## Learning Objectives

By the end of this lesson you will be able to:

- Write well-structured PyTest test functions using the Arrange-Act-Assert pattern.
- Explain what makes a good test: small, focused, independent, repeatable, and descriptively named.
- Group related tests into plain Python classes, and explain how PyTest instantiates them.
- Decide when to use a function and when to use a class.
- Explain why each test gets a fresh class instance, and why tests must not share state through `self`.
- Skip, expect failure, and mark tests inline (an introduction; markers get a full lesson later today).
- Test for expected errors and unexpected outputs at a basic level.
- Apply these skills to the Project 1 utility functions.

---

## Why This Matters

The weekly epic is about turning manual test cases into automated ones. A manual test case has a title, preconditions, steps, and an expected result. A PyTest test function is the code form of exactly that:

| Manual test case | PyTest test |
|---|---|
| Title: "Reverse an empty string" | Function name: `test_reverse_empty_string_returns_empty_string` |
| Precondition / test data | **Arrange** section |
| Steps | **Act** section |
| Expected result | **Assert** section |

In **Project 1: QE Foundations**, the milestone for today is automating the utility tests. If you can translate each manual test case into one clear test function, and group related ones in a class, your suite becomes a living version of your test design document. Poorly written tests, on the other hand, become a maintenance burden that teams eventually delete.

---

## The Concept

### 1. The test function

A **test function** is an ordinary Python function whose name starts with `test`. PyTest calls it with no arguments (for now; on Tuesday you will learn how fixtures add arguments). The test **passes** if the function finishes without raising an exception. It **fails** if an `assert` statement is false, or if any exception escapes.

```python
def test_addition():
    assert 2 + 2 == 4
```

That is the entire contract. There is no `return value` check; PyTest even warns if a test returns something other than `None`, because a returned value is almost always a mistake (a missing `assert`).

#### Three possible results

| Result | Meaning | Symbol |
|---|---|---|
| **Passed** | Function completed with no exception | `.` |
| **Failed** | An `AssertionError` (a failed check) was raised | `F` |
| **Error** | An exception occurred outside the test body, such as during setup (Tuesday) or collection | `E` |

Other outcomes are **skipped** (`s`), **xfailed** (`x`, expected failure that did fail), and **xpassed** (`X`, expected failure that unexpectedly passed).

### 2. Arrange, Act, Assert (AAA)

Good tests follow a three-part shape:

1. **Arrange:** prepare inputs and any objects.
2. **Act:** perform the one action being tested.
3. **Assert:** check the result.

```python
def test_discount_applies_ten_percent():
    # Arrange
    price = 200.0
    discount_rate = 0.10

    # Act
    final_price = price - (price * discount_rate)

    # Assert
    assert final_price == 180.0
```

Using blank lines or comments between the three parts makes the test easy to scan. In very small tests the three parts collapse into one line, which is fine.

A related idea is **one behaviour per test**. A test named `test_utils` that checks 15 things will fail at the first wrong assertion and hide the other 14. Many small tests give precise failure reports.

### 3. Naming tests well

A test name is documentation, and it is what you see in the failure report at 6 pm on release day. Use the pattern:

```
test_<thing under test>_<condition>_<expected result>
```

Examples:

- `test_is_even_with_zero_returns_true`
- `test_divide_by_zero_raises_zero_division_error`
- `test_reverse_text_with_empty_string_returns_empty_string`

Bad names: `test1`, `test_function`, `test_works`, `test_stuff`.

### 4. Qualities of a good test (the F.I.R.S.T. idea)

| Quality | Meaning |
|---|---|
| **F**ast | Runs in milliseconds, so you run it often. |
| **I**ndependent | Does not rely on another test's result or order. |
| **R**epeatable | Same result every time, on every machine. Avoid randomness, the current time, and live network calls unless controlled. |
| **S**elf-validating | Decides pass/fail by itself with `assert`; nobody reads printed output. |
| **T**imely | Written close to the code it checks. |

### 5. Test classes

A **test class** is a plain Python class used to **group related tests**. Rules (recap from discovery):

- Name starts with `Test`.
- No `__init__` method.
- Test methods start with `test` and take `self` as the first parameter.
- It does **not** inherit from `unittest.TestCase` (although PyTest can also run those; that is a different style).

```python
class TestCalculator:
    def test_add(self):
        assert 1 + 1 == 2

    def test_subtract(self):
        assert 5 - 3 == 2
```

#### Why use classes?

1. **Organisation:** all tests for one function or feature are visibly together, both in the code and in reports (`TestIsPalindrome::test_...`).
2. **Shared configuration:** you can apply a marker to the whole class (next lessons) and, from Tuesday, share setup code for the class.
3. **Namespacing:** two methods named `test_empty` can exist in two different classes without clashing.

#### When should I use a function instead?

- For small suites and simple utilities, plain functions are perfectly fine and are preferred by many PyTest users.
- Use a class when you have a clear group (for example, "all tests for the `login` function") with five or more tests.

There is no technical advantage to classes beyond grouping, so do not use them just to look "object-oriented".

#### The most important class rule: a new instance for every test

For **each** test method, PyTest creates a **brand new instance** of the class, calls that one method, and throws the instance away. This is deliberate so tests stay independent.

```python
class TestCounterTrap:
    count = 0                      # class attribute (shared!)

    def test_first(self):
        self.value = 10            # set on THIS instance only
        assert self.value == 10

    def test_second(self):
        # self.value does not exist here; a new instance was created
        assert not hasattr(self, "value")
```

Because of this, **do not store data on `self` in one test hoping another test will see it**. Doing so makes tests order-dependent and is a classic beginner bug. (Class-level attributes shared by all instances behave differently; mutable class attributes like lists can leak state between tests, so avoid them.)

### 6. Testing functions that raise errors (introduction)

Sometimes the correct behaviour is to raise an exception. Use `pytest.raises` as a context manager:

```python
import pytest


def divide(a, b):
    return a / b


def test_divide_by_zero_raises_error():
    with pytest.raises(ZeroDivisionError):
        divide(10, 0)
```

The test **passes** only if the code inside the `with` block raises `ZeroDivisionError`. If nothing is raised, or a different exception type is raised, the test fails. We will examine `pytest.raises` fully in the next lesson, *Assertions and Assertion Introspection*, and Wednesday's *Exception Testing* goes further.

### 7. Skipping and expected failures (a first look)

Sometimes a test cannot or should not run right now.

```python
import sys
import pytest


@pytest.mark.skip(reason="feature not implemented yet")
def test_future_feature():
    assert False


@pytest.mark.skipif(sys.platform == "win32", reason="Linux-only behaviour")
def test_linux_only():
    assert True


@pytest.mark.xfail(reason="known bug #123: rounding error")
def test_known_bug():
    assert round(2.675, 2) == 2.68
```

- `skip`: never runs, reported as `s`. Honest and visible, unlike commenting the test out.
- `skipif`: skips only when the condition is true.
- `xfail`: "expected failure". Runs the test; if it fails, that is reported as `x` (not a red failure). If it unexpectedly passes, it shows `X` (xpass), a signal that the bug might be fixed.

These are **markers**, and we dedicate the lesson *Markers* to them. For now, know that they exist and that they are better than deleting or commenting out tests, because they keep the problem visible in reports.

### 8. Comparing floating-point numbers

Computers store decimals approximately. The classic example is `0.1 + 0.2 == 0.3`, which is `False` in Python (the left side is `0.30000000000000004`). Use `pytest.approx`:

```python
import pytest


def test_float_addition():
    assert 0.1 + 0.2 == pytest.approx(0.3)
```

`approx` compares within a small tolerance (default relative 1e-6). It is part of the assertion toolkit that the next lesson covers in detail.

### 9. Tests must be able to fail

A test that can never fail gives false confidence. Example of a useless test:

```python
def test_useless():
    result = add(2, 3)
    assert result or True     # always true!
```

A good habit is to **see a test fail once**: temporarily break the code, confirm the test goes red, then restore the code. This proves the test is checking something real.

---

## Code Examples with Line-by-Line Explanations

We will use the following Project 1 style utility module.

`src/utils.py`:

```python
def add(a, b):
    return a + b


def divide(a, b):
    if b == 0:
        raise ZeroDivisionError("Cannot divide by zero")
    return a / b


def is_even(number):
    return number % 2 == 0


def title_case(text):
    return " ".join(word.capitalize() for word in text.split())


def clamp(value, minimum, maximum):
    if minimum > maximum:
        raise ValueError("minimum cannot be greater than maximum")
    return max(minimum, min(value, maximum))
```

### Example 1: Function-style tests with AAA

`tests/test_utils_functions.py`:

```python
import pytest

from src.utils import add, divide, is_even, title_case, clamp


def test_add_two_positive_numbers_returns_their_sum():
    # Arrange
    first, second = 2, 3

    # Act
    result = add(first, second)

    # Assert
    assert result == 5


def test_add_negative_and_positive_returns_difference():
    assert add(-4, 10) == 6


def test_is_even_with_zero_returns_true():
    assert is_even(0) is True


def test_title_case_capitalises_each_word():
    assert title_case("quality engineering academy") == "Quality Engineering Academy"


def test_divide_returns_float():
    assert divide(9, 3) == pytest.approx(3.0)


def test_divide_by_zero_raises_zero_division_error():
    with pytest.raises(ZeroDivisionError):
        divide(1, 0)
```

Explanation:

1. `import pytest`: needed for `pytest.approx` and `pytest.raises`. Plain `assert` needs no import.
2. `first, second = 2, 3` is tuple unpacking: assigns `first = 2` and `second = 3` in one line.
3. The first test shows full AAA. The second shows the compact style for trivial cases.
4. `is_even(0) is True`: zero is even because `0 % 2` is `0`. A classic boundary value from your test design lessons.
5. `title_case` splits on whitespace, capitalises each word, and joins with single spaces.
6. `pytest.approx(3.0)`: the division gives `3.0`; the approx comparison is a safe habit for floats.
7. The last test uses `pytest.raises`. The test passes because `divide(1, 0)` raises the expected error.

### Example 2: The same suite grouped in classes

`tests/test_utils_classes.py`:

```python
import pytest

from src.utils import divide, clamp


class TestDivide:
    def test_divides_evenly(self):
        assert divide(10, 2) == 5

    def test_divides_with_fraction(self):
        assert divide(1, 4) == 0.25

    def test_zero_numerator_returns_zero(self):
        assert divide(0, 7) == 0

    def test_zero_denominator_raises_zero_division_error(self):
        with pytest.raises(ZeroDivisionError):
            divide(5, 0)


class TestClamp:
    def test_value_inside_range_is_unchanged(self):
        assert clamp(5, 0, 10) == 5

    def test_value_below_minimum_returns_minimum(self):
        assert clamp(-3, 0, 10) == 0

    def test_value_above_maximum_returns_maximum(self):
        assert clamp(99, 0, 10) == 10

    def test_value_equal_to_boundary_is_unchanged(self):
        assert clamp(10, 0, 10) == 10

    def test_invalid_range_raises_value_error(self):
        with pytest.raises(ValueError):
            clamp(5, 10, 0)
```

Explanation:

- `class TestDivide:` begins with `Test` and has no `__init__`, so it is collected.
- Every method takes `self`. We never use it here because these tests are stateless, and that is the best case.
- In the report, tests appear as `TestDivide::test_divides_evenly`, making the failing area obvious.
- The `clamp` tests apply **boundary value analysis**: below, inside, above, and exactly on the boundary (10), the same technique you used in manual test design.

Run it and inspect the grouped output:

```bash
python -m pytest tests/test_utils_classes.py -v
```

```
tests/test_utils_classes.py::TestDivide::test_divides_evenly PASSED
tests/test_utils_classes.py::TestDivide::test_divides_with_fraction PASSED
...
```

(`-v` is "verbose"; the next-but-one lessons detail command-line options.)

### Example 3: Demonstrating a fresh instance per test

```python
class TestInstanceIsolation:
    def test_a_sets_attribute(self):
        self.token = "abc"
        assert self.token == "abc"

    def test_b_does_not_see_it(self):
        assert not hasattr(self, "token")
```

Both tests pass **in any order**, proving each method runs on a new instance. If the second test expected `self.token`, it would fail with `AttributeError`, correctly flagging a bad design.

### Example 4: Skips and expected failure inside a class

```python
import pytest

from src.utils import title_case


class TestTitleCase:
    def test_single_word(self):
        assert title_case("python") == "Python"

    def test_extra_spaces_are_collapsed(self):
        assert title_case("  hello    world ") == "Hello World"

    @pytest.mark.skip(reason="acronym handling is not designed yet")
    def test_acronyms_stay_uppercase(self):
        assert title_case("use API now") == "Use API Now"

    @pytest.mark.xfail(reason="known limitation: apostrophes", strict=False)
    def test_apostrophe_word(self):
        assert title_case("don't stop") == "Don't Stop"
```

Explanation:

- `str.split()` with no argument splits on any run of whitespace and ignores leading/trailing whitespace, so extra spaces are collapsed.
- The skip test never runs and is displayed as skipped, with the reason.
- `title_case("don't stop")` actually returns `"Don't Stop"`, because `"don't".capitalize()` gives `"Don't"` (`capitalize` lowercases the rest of the word). So this `xfail` test unexpectedly **passes** and is reported as `XPASS`. This is a useful teaching point: a non-strict `xfail` that unexpectedly passes is flagged so you can notice and remove the stale marker. With `strict=True`, an unexpected pass would **fail** the suite.

---

## Real-World Scenarios

1. **Translating a manual test case.** Manual case TC-014: "Clamp a value above the maximum. Steps: call `clamp(99, 0, 10)`. Expected: 10." This becomes `test_value_above_maximum_returns_maximum` in `TestClamp`. Keeping one test per manual case allows traceability: the test name can even include the case ID, such as `test_tc014_...`.
2. **Bug reproduction.** A customer reports that `title_case("  hello  ")` crashed. The engineer first writes a failing test that reproduces it, then fixes the code until it turns green. The test stays forever as a regression guard.
3. **Reading CI output.** The report says `TestClamp::test_value_above_maximum_returns_maximum FAILED`. Without opening code, the on-call engineer already knows the upper-bound logic of `clamp` is suspect.

---

## Common Mistakes

| Mistake | Problem | Fix |
|---|---|---|
| Many unrelated assertions in one test | First failure hides the rest, unclear which behaviour broke | One behaviour per test (related asserts on one result are fine). |
| `test1`, `test2` names | No information in reports | Descriptive sentence-like names. |
| Forgetting `self` in a class method | `TypeError: ... takes 0 positional arguments but 1 was given` | Add `self` as the first parameter. |
| Adding `__init__` to a test class | Class not collected | Remove it. |
| Sharing data between tests via `self` or global lists | Order-dependent, flaky tests | Build the data inside each test. |
| `return` instead of `assert` | PyTest warns; test always passes | Use `assert`. |
| `assert add(2,3) == 5, "..."` message with parentheses on the assert: `assert(x, "msg")` | Asserting a non-empty tuple, always true (Python warns) | Write `assert x, "msg"` with no parentheses around both. |
| Comparing floats with `==` | Rounding errors | Use `pytest.approx`. |
| Commenting out failing tests | Hidden risk | Use `skip` / `xfail` with a reason. |
| Never seeing the test fail | May be a no-op test | Break the code temporarily to see red. |

---

## Practice Exercises

### Exercise 1: Translate manual cases
Given the function `is_even`, write function-style tests for these manual cases: zero, positive even, positive odd, negative even, negative odd. Use descriptive names.

**Solution:**

```python
from src.utils import is_even


def test_is_even_zero_returns_true():
    assert is_even(0) is True

def test_is_even_positive_even_returns_true():
    assert is_even(8) is True

def test_is_even_positive_odd_returns_false():
    assert is_even(7) is False

def test_is_even_negative_even_returns_true():
    assert is_even(-6) is True

def test_is_even_negative_odd_returns_false():
    assert is_even(-3) is False
```

(Python's `%` always returns a non-negative result for a positive divisor, so `-3 % 2 == 1`.)

### Exercise 2: Group in a class
Rewrite Exercise 1 as `class TestIsEven`, removing the repeated `is_even` prefix from method names where it adds nothing.

### Exercise 3: Write the function and the tests
Write `def absolute(n)` that returns the absolute value without using `abs()`. Then write tests for negative, positive, zero, and a float. Use `pytest.approx` for the float.

*Hint:* `return -n if n < 0 else n`.

### Exercise 4: Error handling
Write `def percentage(part, whole)` that raises `ValueError("whole must be positive")` if `whole <= 0`. Write three tests: a normal case, `part` equal to zero, and an invalid `whole` using `pytest.raises`.

### Exercise 5: Prove isolation
Create a class with two tests where the first appends to a **class-level list** and the second checks the list's length. Run them in both orders (use `-p no:randomly` if you have a random-order plugin installed, or simply rename methods). Explain what you observe and why it is dangerous.

*Explanation:* A class-level list is shared by all instances, so state leaks between tests, making results depend on order, unlike per-instance attributes.

### Exercise 6: See it fail
Pick any passing test from your suite. Change the function under test to return a wrong value, confirm the test fails with a useful message, then undo the change. Write one sentence on what you learned.

### Exercise 7 (challenge): Project 1 mini-suite
Choose three Project 1 utility functions. For each, write at least four tests covering a typical case, a boundary, an invalid input, and an edge case. Group each function's tests in its own class.

---

## Summary

- A PyTest test is a function (or method) named `test...`; it passes if no exception escapes, and fails on a false `assert`.
- Structure tests as **Arrange, Act, Assert** and keep to **one behaviour per test**.
- Give tests descriptive names: `test_<thing>_<condition>_<expected>`.
- Good tests are fast, independent, repeatable, and self-validating.
- Classes named `Test...` group related tests; they need no `__init__` and no base class.
- PyTest creates a **new instance per test method**, so never pass state between tests through `self`.
- Use `pytest.raises` for expected errors and `pytest.approx` for floats; use `skip`, `skipif`, and `xfail` instead of commenting tests out.
- Next lesson: a deep dive into assertions and how PyTest explains failures.

---

## Additional Resources

- PyTest: Get Started (first tests and grouping in classes): https://docs.pytest.org/en/stable/getting-started.html
- PyTest: How to write and report assertions: https://docs.pytest.org/en/stable/how-to/assert.html
- Python tutorial on classes: https://docs.python.org/3/tutorial/classes.html
