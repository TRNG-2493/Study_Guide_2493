# Introduction to Unit Testing

## Learning Objectives

By the end of this lesson you will be able to:

- Define a **unit test** and explain how it differs from manual testing, integration tests and system (end-to-end) tests.
- Explain *why* teams write automated unit tests and the benefits (fast feedback, safety net for change, living documentation).
- Describe the **Arrange-Act-Assert** structure and the qualities of a good unit test (the **FIRST** principles).
- Write test cases using Python's built-in **`unittest`** framework: `TestCase` classes, `test_` methods, and the most common assertion methods.
- Test **expected exceptions** with `assertRaises`, floating-point values with `assertAlmostEqual`, and many inputs with `subTest`.
- Use **fixtures**: `setUp`, `tearDown`, `setUpClass`, `tearDownClass` and `addCleanup` to give each test a clean start.
- Run tests from the command line (`python -m unittest`, test discovery, verbose mode, selecting tests with `-k`), and **read the output** for passed, failed, errored and skipped tests.
- Choose what to test: normal cases, boundary values, invalid input and error handling.
- Organise test files and apply a simple **red-green-refactor** workflow to fix a bug and keep it fixed.

---

## Why This Matters

On Tuesday, you wrote `assert` statements. Earlier today you learned how to find bugs (debugging) and record what a program does (logging). Unit testing is the next, and arguably most important, step in "hardening" your Python: it is how you **prove**, repeatedly and automatically, that your code does what you claim and keeps doing it as it changes.

For a **Test Automation Engineer**, this lesson matters on two levels:

1. **You test other people's software.** Your job is to build automated checks. Unit tests are the most basic automated check, and the concepts (test case, assertion, fixture, test runner, report) are exactly the same ones you will meet in every testing framework and tool you use later in your career, including those for APIs and user interfaces.
2. **You write code too.** Your test utilities, data loaders, helpers and framework code are real software. If your *test code* has bugs, you either miss real defects (false passes) or waste time chasing phantom ones (false failures). Unit-testing your own helpers is how you make a test framework trustworthy.

It also connects to the **Weekly Epic**: "Trainees harden their Python with modules, exceptions, files, debugging and unit testing". Today's Project 1 milestone and exercise will have you debug a module, add logging and write unit tests for it; this lesson gives you the tools to do so.

> **Scope note.** This lesson uses `unittest`, which ships with Python, so you need to install nothing. A very popular third-party framework called **pytest** has a lighter syntax; we will cover it in depth in later weeks. All the *ideas* you learn today (arrange/act/assert, fixtures, test discovery, expected exceptions) transfer directly to it.

---

## The Concept

### 1. What is a unit test?

A **unit** is the smallest testable piece of code, typically one function or one method. A **unit test** is a small automated program that:

1. calls a unit with specific **inputs**,
2. compares the **actual result** with the **expected result**, and
3. reports **pass** or **fail**.

A collection of unit tests is a **test suite**. The program that finds and runs tests and reports results is a **test runner**.

**Analogy.** Imagine you manufacture bicycles. A *unit test* checks one part on its own: does this brake lever spring back? Does this bolt hold the specified torque? An *integration test* checks that parts work together: do the brakes stop the wheel? A *system test* rides the finished bike down a hill. When a brake lever fails the bench test you know exactly where to look; when the finished bike crashes you have many suspects.

### 2. Where unit tests fit: a brief map of test types

| Level | What it checks | Speed | When it fails you know... |
|---|---|---|---|
| **Unit** | One function/class in isolation | Milliseconds | Exactly which piece is broken |
| **Integration** | Several pieces (or the code plus a database/service) working together | Seconds | Which interaction is broken |
| **System / end-to-end** | The whole application through its real interface | Seconds to minutes | *Something* is broken |

Healthy projects have **many** fast unit tests, **fewer** integration tests and **few** end-to-end tests. In this programme you will meet the higher levels later; today we focus on the base.

### 3. Why write automated unit tests?

- **Fast feedback.** Run hundreds of tests in a second after every change instead of re-checking by hand.
- **Safety net for change.** If you restructure code and the tests still pass, you have strong evidence you did not break anything (this is called *regression protection*).
- **Bugs stay fixed.** When you fix a defect, you add a test that would have caught it. It can never silently return.
- **Living documentation.** A test shows precisely how a function is meant to be used and what it returns for edge cases.
- **Better design.** Code that is easy to test tends to be small, focused and loosely coupled.
- **Confidence and speed.** Teams that trust their tests release more often and with less fear.

Manual testing remains valuable for exploration, but anything you would repeat should be automated.

### 4. Anatomy of a good test: Arrange, Act, Assert

Most unit tests have three phases:

1. **Arrange**: prepare the inputs and the state the unit needs.
2. **Act**: call the unit being tested (usually one call).
3. **Assert**: check the outcome against the expectation.

```python
def test_adds_two_numbers(self):
    a, b = 2, 3                 # Arrange
    result = add(a, b)          # Act
    self.assertEqual(result, 5) # Assert
```

#### The FIRST principles

| Letter | Principle | Meaning |
|---|---|---|
| **F** | Fast | Tests should run in milliseconds so people run them constantly |
| **I** | Independent / Isolated | A test must not depend on another test or on execution order (recall the shared-state problems from the scope and mutability lessons) |
| **R** | Repeatable | Same result every run, on any machine, with no reliance on time, randomness, network, or leftover files |
| **S** | Self-validating | The test itself decides pass or fail (an assertion); no human reading output |
| **T** | Timely | Written close in time to the code (ideally just before or alongside it) |

Further good habits: **one behaviour per test**, a **descriptive name** (`test_divide_by_zero_raises` rather than `test1`), and a failure message that tells you what went wrong without opening the code.

### 5. Your first test with `unittest`

#### 5.1 The code under test

```python
# calculator.py
"""A tiny module we want to test."""


def add(a, b):
    return a + b


def divide(a, b):
    if b == 0:
        raise ZeroDivisionError("cannot divide by zero")
    return a / b


def is_even(n):
    return n % 2 == 0


def pass_rate(results):
    """Percentage of 'pass' outcomes (case-insensitive); 0.0 for an empty list."""
    if not results:
        return 0.0
    passed = sum(1 for outcome in results if outcome.lower() == "pass")
    return passed / len(results) * 100
```

(`pass_rate` is the corrected function from the debugging lesson.)

#### 5.2 The test module

```python
# test_calculator.py
import unittest

from calculator import add, divide, is_even, pass_rate


class TestAdd(unittest.TestCase):
    def test_adds_two_positive_numbers(self):
        self.assertEqual(add(2, 3), 5)

    def test_adds_negative_numbers(self):
        self.assertEqual(add(-2, -3), -5)

    def test_adds_floats_approximately(self):
        self.assertAlmostEqual(add(0.1, 0.2), 0.3)


class TestDivide(unittest.TestCase):
    def test_divides_evenly(self):
        self.assertEqual(divide(10, 2), 5)

    def test_divide_by_zero_raises(self):
        with self.assertRaises(ZeroDivisionError):
            divide(1, 0)

    def test_divide_by_zero_message(self):
        with self.assertRaises(ZeroDivisionError) as ctx:
            divide(1, 0)
        self.assertIn("zero", str(ctx.exception))


class TestIsEven(unittest.TestCase):
    def test_many_values(self):
        cases = [(0, True), (1, False), (2, True), (-3, False)]
        for number, expected in cases:
            with self.subTest(number=number):
                self.assertEqual(is_even(number), expected)


class TestPassRate(unittest.TestCase):
    def setUp(self):
        self.mixed = ["pass", "fail", "pass", "pass"]

    def test_mixed_results(self):
        self.assertEqual(pass_rate(self.mixed), 75.0)

    def test_case_insensitive(self):
        self.assertEqual(pass_rate(["PASS", "Pass", "pass"]), 100.0)

    def test_empty_list_returns_zero(self):
        self.assertEqual(pass_rate([]), 0.0)

    @unittest.skip("demonstration of skipping")
    def test_skipped(self):
        self.fail("never runs")


if __name__ == "__main__":
    unittest.main()
```

#### 5.3 Explaining the code line by line

- `import unittest` loads the standard library testing framework.
- `from calculator import ...` imports the units under test. This is the module/import skill from Monday: the test file lives next to (or in a `tests` folder beside) the code and imports it like any other module.
- `class TestAdd(unittest.TestCase):` A **test case class**. Inheriting from `unittest.TestCase` gives you the assertion methods (`self.assertEqual`, ...) and tells the runner "this class contains tests".
- Methods whose names **start with `test`** are discovered and run automatically as individual tests. Other methods (like `setUp` or a helper) are not tests. Each test method runs **independently**, and one failing does not stop the others.
- `self.assertEqual(add(2, 3), 5)` is the assertion: `assertEqual(actual, expected)` (the usual convention puts the actual value first). If they differ, the test **fails** and the output shows both values.
- `assertAlmostEqual(a, b)` compares numbers after rounding to 7 decimal places by default, which solves the floating-point problem (`0.1 + 0.2 != 0.3`) from the built-in functions lesson.
- `with self.assertRaises(ZeroDivisionError):` asserts that the code inside the `with` block **raises** that exception; if it does not raise, or raises something else, the test fails. This is the context-manager syntax you learned on Tuesday, applied to exceptions. Using `as ctx` lets you inspect `ctx.exception` afterwards (its message, attributes).
- `self.subTest(number=number)` runs the body once for each input, reporting each failing input separately instead of stopping at the first. Great for table-driven data.
- `setUp(self)` runs **before every test method** in the class, giving each test its own fresh `self.mixed` list (isolation!).
- `@unittest.skip("reason")` marks a test as intentionally not run; it is reported as *skipped* rather than silently ignored.
- `if __name__ == "__main__": unittest.main()` lets you run the file directly with `python test_calculator.py`.

### 6. Running tests and reading the results

From the folder that contains both files:

```
python -m unittest
```

Output:

```
..........s
----------------------------------------------------------------------
Ran 11 tests in 0.000s

OK (skipped=1)
```

Each character is one test: `.` pass, `F` failure, `E` error, `s` skipped (and `x` expected failure, `u` unexpected success). Add `-v` for names:

```
python -m unittest -v
```

```
test_adds_floats_approximately (test_calculator.TestAdd.test_adds_floats_approximately) ... ok
test_adds_negative_numbers (test_calculator.TestAdd.test_adds_negative_numbers) ... ok
test_adds_two_positive_numbers (test_calculator.TestAdd.test_adds_two_positive_numbers) ... ok
test_divide_by_zero_message (test_calculator.TestDivide.test_divide_by_zero_message) ... ok
test_divide_by_zero_raises (test_calculator.TestDivide.test_divide_by_zero_raises) ... ok
test_divides_evenly (test_calculator.TestDivide.test_divides_evenly) ... ok
test_many_values (test_calculator.TestIsEven.test_many_values) ... ok
test_case_insensitive (test_calculator.TestPassRate.test_case_insensitive) ... ok
test_empty_list_returns_zero (test_calculator.TestPassRate.test_empty_list_returns_zero) ... ok
test_mixed_results (test_calculator.TestPassRate.test_mixed_results) ... ok
test_skipped (test_calculator.TestPassRate.test_skipped) ... skipped 'demonstration of skipping'

----------------------------------------------------------------------
Ran 11 tests in 0.001s

OK (skipped=1)
```

(Within a class, tests run in alphabetical order; never rely on it, since tests must be independent.)

Handy command-line options:

| Command | Effect |
|---|---|
| `python -m unittest` | **Discover** and run all tests: files named `test*.py` in the current directory tree |
| `python -m unittest discover -s tests -p "test_*.py"` | Discover with an explicit start folder and file pattern |
| `python -m unittest test_calculator` | Run one module |
| `python -m unittest test_calculator.TestAdd` | Run one class |
| `python -m unittest test_calculator.TestAdd.test_adds_negative_numbers` | Run a single test |
| `python -m unittest -k divide` | Run tests whose names contain the text `divide` |
| `python -m unittest -f` | **Fail fast**: stop at the first failure |
| `python -m unittest -b` | **Buffer** output: show prints only for failing tests |
| `python -m unittest -v` | Verbose names |

Run the commands from the project's top directory so imports like `from calculator import add` work.

#### What a failing test looks like

Suppose someone "breaks" `add` so that it subtracts (`return a - b`). Running the tests now gives:

```
FFF.......s
======================================================================
FAIL: test_adds_floats_approximately (test_calculator.TestAdd.test_adds_floats_approximately)
----------------------------------------------------------------------
Traceback (most recent call last):
  File "test_calculator.py", line 14, in test_adds_floats_approximately
    self.assertAlmostEqual(add(0.1, 0.2), 0.3)
    ~~~~~~~~~~~~~~~~~~~~~~^^^^^^^^^^^^^^^^^^^^
AssertionError: -0.1 != 0.3 within 7 places (0.4 difference)

======================================================================
FAIL: test_adds_negative_numbers (test_calculator.TestAdd.test_adds_negative_numbers)
----------------------------------------------------------------------
Traceback (most recent call last):
  File "test_calculator.py", line 11, in test_adds_negative_numbers
    self.assertEqual(add(-2, -3), -5)
    ~~~~~~~~~~~~~~~~^^^^^^^^^^^^^^^^^
AssertionError: 1 != -5

======================================================================
FAIL: test_adds_two_positive_numbers (test_calculator.TestAdd.test_adds_two_positive_numbers)
----------------------------------------------------------------------
Traceback (most recent call last):
  File "test_calculator.py", line 8, in test_adds_two_positive_numbers
    self.assertEqual(add(2, 3), 5)
    ~~~~~~~~~~~~~~~~^^^^^^^^^^^^^^
AssertionError: -1 != 5

----------------------------------------------------------------------
Ran 11 tests in 0.002s

FAILED (failures=3, skipped=1)
```

Read it with the traceback skills from the debugging lesson: each block names the failing test, the line of the assertion, and the *actual versus expected* values (`-1 != 5`). That is the benefit of automation: three failures pointing directly at `add`, in two milliseconds.

#### Failure versus error

| Result | Meaning | Typical cause |
|---|---|---|
| **FAIL** | An assertion was **false** | The code ran but gave the wrong answer (or the test's expectation is wrong) |
| **ERROR** | The test raised an **unexpected exception** (not an assertion) | Crash in the code or in the test: `KeyError`, `TypeError`, bad setup |
| **skipped** | Deliberately not run (`@unittest.skip`) | Feature not ready, platform-specific, etc. |
| **expected failure** | Marked with `@unittest.expectedFailure`; known bug | Documents a known defect without breaking the build |

An example showing different outcomes together:

```python
import unittest

class T(unittest.TestCase):
    def test_error(self):
        {}["x"]                                  # unexpected exception -> ERROR
    @unittest.expectedFailure
    def test_known(self):
        self.assertEqual(1, 2)                   # fails as expected -> "x"
    def test_list(self):
        self.assertEqual([1, 2, 3], [1, 2, 4])   # FAIL with a helpful diff
    def test_true(self):
        self.assertTrue(0)                       # FAIL: "0 is not true"
```

```
ExFF
======================================================================
ERROR: test_error (test_err.T.test_error)
...
KeyError: 'x'
======================================================================
FAIL: test_list (test_err.T.test_list)
...
AssertionError: Lists differ: [1, 2, 3] != [1, 2, 4]

First differing element 2:
3
4

- [1, 2, 3]
?        ^

+ [1, 2, 4]
?        ^
...
FAILED (failures=2, errors=1, expected failures=1)
```

Notice how `assertEqual` on lists shows *which element* differs. This is a big reason to prefer `assertEqual(a, b)` over the plain `assert a == b` when using `unittest`.

### 7. The most useful assertion methods

| Method | Passes when | Use it for |
|---|---|---|
| `assertEqual(a, b)` / `assertNotEqual(a, b)` | `a == b` / `a != b` | Most value comparisons (numbers, strings, lists, dicts) |
| `assertTrue(x)` / `assertFalse(x)` | `bool(x)` is `True` / `False` | Conditions (prefer a more specific assertion if one exists) |
| `assertIs(a, b)` / `assertIsNot(a, b)` | `a is b` / `a is not b` | Identity checks (see the *Mutability* lesson) |
| `assertIsNone(x)` / `assertIsNotNone(x)` | `x is None` / not `None` | Checking for `None` |
| `assertIn(a, b)` / `assertNotIn(a, b)` | `a in b` / not in | Membership: items in lists, keys in dicts, substrings |
| `assertIsInstance(obj, cls)` | `isinstance(obj, cls)` | Type checks |
| `assertAlmostEqual(a, b, places=7)` | Equal after rounding (also `delta=`) | **Floating point numbers** |
| `assertGreater(a, b)`, `assertLess(a, b)`, `assertGreaterEqual`, `assertLessEqual` | Ordering | Ranges, durations, counts |
| `assertListEqual`, `assertDictEqual`, `assertSetEqual`, `assertTupleEqual` | Same, with better diffs | Collections |
| `assertCountEqual(a, b)` | Same elements regardless of order | Unordered results |
| `assertRaises(Exc)` | Block raises `Exc` | Expected errors |
| `assertRaisesRegex(Exc, pattern)` | Raises and message matches regex | Checking error text |
| `assertLogs(logger, level)` | Block emits a log message | Verifying logging (see the *Logging* lesson) |
| `fail(msg)` | Always fails | Marking code paths that must not be reached |

Every assertion accepts an optional `msg` argument to add context: `self.assertEqual(actual, expected, msg=f"order {order_id}")`.

**Which value is "expected"?** By convention in `unittest`, `assertEqual(first, second)` puts the *actual* value first and the *expected* value second. Pick a convention and keep it consistent in your team so failure messages read naturally.

### 8. Fixtures: preparing and cleaning up

A **fixture** is everything a test needs in place before it runs (and the cleanup afterwards): data, files, objects, connections. `unittest` provides hooks:

| Hook | Runs | Typical use |
|---|---|---|
| `setUp()` | Before **each** test method | Create fresh objects/data for isolation |
| `tearDown()` | After **each** test method (even if the test failed) | Clean up files, close connections |
| `setUpClass()` (a `@classmethod`) | **Once** before all tests in the class | Expensive one-time setup (start a server, open a DB) |
| `tearDownClass()` (`@classmethod`) | Once after all tests in the class | Release the expensive resource |
| `addCleanup(func, *args)` | Registers cleanup to run after the test (in reverse order) | Safe, flexible cleanup placed next to the setup it undoes |

Here is a complete example that tests a CSV loader using a temporary file, tying together Tuesday's file handling and fixtures:

```python
# loader.py
import csv


def load_scores(path):
    """Return a list of ints from the 'score' column of a CSV file."""
    scores = []
    with open(path, newline="", encoding="utf-8") as fh:
        for row in csv.DictReader(fh):
            scores.append(int(row["score"]))
    return scores
```

```python
# test_loader.py
import os
import tempfile
import unittest

from loader import load_scores


class TestLoadScores(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        print("\n[setUpClass] once before all tests in this class")

    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)          # guaranteed cleanup
        self.path = os.path.join(self.tmp.name, "scores.csv")
        print("[setUp] fresh temp dir")

    def write(self, text):
        with open(self.path, "w", newline="", encoding="utf-8") as fh:
            fh.write(text)

    def test_loads_scores(self):
        self.write("name,score\nann,90\nbob,75\n")
        self.assertEqual(load_scores(self.path), [90, 75])

    def test_header_only_gives_empty_list(self):
        self.write("name,score\n")
        self.assertEqual(load_scores(self.path), [])

    def test_bad_number_raises_value_error(self):
        self.write("name,score\nann,abc\n")
        with self.assertRaises(ValueError):
            load_scores(self.path)

    def test_missing_file_raises(self):
        with self.assertRaises(FileNotFoundError):
            load_scores(os.path.join(self.tmp.name, "nope.csv"))

    def tearDown(self):
        print("[tearDown]")

    @classmethod
    def tearDownClass(cls):
        print("[tearDownClass] once after all tests")


if __name__ == "__main__":
    unittest.main()
```

Running `python -m unittest test_loader -v` shows the order of the hooks:

```
[setUpClass] once before all tests in this class
test_bad_number_raises_value_error (test_loader.TestLoadScores.test_bad_number_raises_value_error) ... [setUp] fresh temp dir
[tearDown]
ok
test_header_only_gives_empty_list (test_loader.TestLoadScores.test_header_only_gives_empty_list) ... [setUp] fresh temp dir
[tearDown]
ok
test_loads_scores (test_loader.TestLoadScores.test_loads_scores) ... [setUp] fresh temp dir
[tearDown]
ok
test_missing_file_raises (test_loader.TestLoadScores.test_missing_file_raises) ... [setUp] fresh temp dir
[tearDown]
ok
[tearDownClass] once after all tests

----------------------------------------------------------------------
Ran 4 tests in 0.005s

OK
```

Why this design is good:

- **Isolation.** Every test gets its own brand-new temporary directory; no test can see another's file. The test never touches your real files.
- **Cleanup.** `TemporaryDirectory` plus `addCleanup` removes the files even if the test fails.
- **Positive and negative cases.** It tests normal data, an edge case (header only), invalid data (`"abc"`), and a missing file, each with one clear expectation.
- **The helper `write`** removes repetition. It does not begin with `test`, so it is not run as a test.

### 9. Table-driven tests with `subTest`

When the same logic must be verified for many inputs, loop over a table and wrap each iteration in `self.subTest(...)`. Without `subTest`, the first failing input would abort the test and hide the rest. With it, every failing input is reported with its parameters:

```python
import unittest
from calculator import is_even

class T(unittest.TestCase):
    def test_m(self):
        for n, e in [(0, True), (1, True), (2, False)]:   # two deliberately wrong expectations
            with self.subTest(n=n):
                self.assertEqual(is_even(n), e)
```

```
FF
======================================================================
FAIL: test_m (__main__.T.test_m) (n=1)
----------------------------------------------------------------------
AssertionError: False != True

======================================================================
FAIL: test_m (__main__.T.test_m) (n=2)
----------------------------------------------------------------------
AssertionError: True != False
```

(The test-case expectations were purposely wrong to show the report. Each failure is labelled with its `n`.)

### 10. Deciding what to test

A function with no tests for its edge cases is barely tested. For each unit, think of categories:

| Category | Examples for `pass_rate(results)` |
|---|---|
| **Typical / happy path** | `["pass", "fail", "pass", "pass"]` gives `75.0` |
| **Boundaries** | All pass (100.0), all fail (0.0), exactly one element |
| **Empty / minimal input** | `[]` gives `0.0` (this was the `ZeroDivisionError` bug) |
| **Variations of valid input** | `"PASS"`, `"Pass"` (the case-sensitivity bug) |
| **Invalid input** | `None` instead of a list, non-string items: what *should* happen? Decide and test it |
| **Error handling** | Does it raise the exception your design promised? |

Two good habits:

- **Test behaviour, not implementation.** Assert on what the function returns or raises, not on how it does it internally. Then you can refactor freely.
- **Each bug gets a test.** The tests for `pass_rate` above are exactly the three problems found during the debugging lesson, now frozen as permanent regression tests.

### 11. A simple workflow: red, green, refactor

A popular discipline called **Test-Driven Development (TDD)** uses a short cycle:

1. **Red.** Write a test for the behaviour you want; run it; watch it **fail**. (A test you have never seen fail may not test anything.)
2. **Green.** Write the simplest code that makes the test pass.
3. **Refactor.** Clean up the code (and tests), re-running the tests to ensure they still pass.

Even if you do not practise full TDD, use the **bug-fix variant**: when you find a bug, first write a failing test that reproduces it (this is your *minimal reproducible example* from the debugging lesson), then fix the code until it passes.

### 12. Organising tests

A typical small project layout:

```
project/
|-- calculator.py
|-- loader.py
`-- tests/
    |-- __init__.py
    |-- test_calculator.py
    `-- test_loader.py
```

- Name test files `test_<module>.py` so discovery finds them.
- Run from the project root: `python -m unittest discover -s tests -t .` (the `-t .` sets the top-level directory so imports of `calculator` work).
- Keep tests next to the thing they test conceptually: one test module per code module, one `TestCase` class per function/class under test.
- Never leave print/`breakpoint()` statements in committed tests. If you need to see output, run with `-b` off or use logging.
- Use a `.gitignore` to keep `__pycache__/` out of version control. (Stale compiled caches can occasionally make an old version of a module appear to run; if edits seem to be ignored, delete `__pycache__`.)

### 13. Common mistakes to avoid

| Mistake | Why it hurts | Better |
|---|---|---|
| Tests that depend on each other or on run order | Break when run alone or in parallel | Each test sets up its own data (`setUp`) |
| One giant test with many assertions | First failure hides the rest; unclear cause | One behaviour per test (or use `subTest`) |
| Tests with no assertion | Always pass; verify nothing | Always assert something |
| Asserting on floats with `==` | Rounding noise | `assertAlmostEqual` |
| Copying the implementation into the test | Test passes even when logic is wrong | Hard-code known-correct expected values |
| Using real network/time/random in unit tests | Slow, flaky, not repeatable | Isolate or replace (later we will see *mocking*; `unittest.mock` is part of the standard library) |
| Catching exceptions inside a test to "make it pass" | Hides real errors | Use `assertRaises` when an error is expected; let others fail |
| Changing the expected value just to turn a test green | Hides a real defect | First prove which side is wrong |

---

## Code Examples

### Example A: Testing a validation helper, including error handling

```python
# validators.py
def validate_age(value):
    """Return age as int; raise ValueError for non-numbers or ages outside 0-120."""
    try:
        age = int(value)
    except (ValueError, TypeError):
        raise ValueError(f"age must be a whole number, got {value!r}") from None
    if not 0 <= age <= 120:
        raise ValueError(f"age out of range: {age}")
    return age
```

```python
# test_validators.py
import unittest
from validators import validate_age


class TestValidateAge(unittest.TestCase):
    def test_valid_text_is_converted(self):
        self.assertEqual(validate_age("42"), 42)

    def test_lower_boundary_is_valid(self):
        self.assertEqual(validate_age(0), 0)

    def test_upper_boundary_is_valid(self):
        self.assertEqual(validate_age(120), 120)

    def test_just_above_upper_boundary_is_invalid(self):
        with self.assertRaises(ValueError):
            validate_age(121)

    def test_negative_is_invalid(self):
        with self.assertRaises(ValueError):
            validate_age(-1)

    def test_non_numeric_text_message(self):
        with self.assertRaisesRegex(ValueError, "whole number"):
            validate_age("4x")

    def test_none_is_invalid(self):
        with self.assertRaises(ValueError):
            validate_age(None)


if __name__ == "__main__":
    unittest.main()
```

What this demonstrates:

- **Boundary value analysis**: the values *on* and *just beyond* each limit (0, -1, 120, 121) are where bugs hide. This is a core technique in software testing.
- The test names read like a specification.
- `assertRaisesRegex` checks both the exception type *and* part of its message.
- It uses the exception-handling ideas from Tuesday (`raise ... from None` hides the internal chained traceback).

### Example B: Testing that a message was logged

```python
import logging
import unittest

logger = logging.getLogger("qa.parser")

def parse_age(text):
    try:
        return int(text)
    except (ValueError, TypeError):
        logger.warning("Invalid age value: %r", text)
        return None


class TestParseAge(unittest.TestCase):
    def test_valid(self):
        self.assertEqual(parse_age("42"), 42)

    def test_invalid_logs_warning_and_returns_none(self):
        with self.assertLogs("qa.parser", level="WARNING") as captured:
            result = parse_age("4x")
        self.assertIsNone(result)
        self.assertEqual(captured.output, ["WARNING:qa.parser:Invalid age value: '4x'"])


if __name__ == "__main__":
    unittest.main()
```

`assertLogs` captures log records emitted inside the `with` block (and fails the test if none arrive); `captured.output` is a list of formatted lines. This closes the loop with the logging lesson: log messages are behaviour too.

### Example C: From failing test to fix (red, green)

1. Red: you discover that `average([])` crashes. Write the test first.

```python
import unittest

def average(values):
    return sum(values) / len(values)          # current (buggy) implementation


class TestAverage(unittest.TestCase):
    def test_average_of_numbers(self):
        self.assertEqual(average([2, 4, 6]), 4)

    def test_average_of_empty_list_is_none(self):
        self.assertIsNone(average([]))         # desired behaviour (decided with the team)
```

Running it shows `ERROR: test_average_of_empty_list_is_none ... ZeroDivisionError: division by zero`. The test is **red**.

2. Green: fix the function.

```python
def average(values):
    if not values:
        return None
    return sum(values) / len(values)
```

Both tests now pass. The defect can never return unnoticed.

---

## Summary / Key Takeaways

- A **unit test** automatically checks one small piece of code by comparing the actual result with an expected result. A group of tests is a **test suite**; the **test runner** executes them and reports.
- Unit tests give fast feedback, protect against regressions, document behaviour and let you change code with confidence.
- Structure tests as **Arrange, Act, Assert**, and follow **FIRST**: Fast, Isolated, Repeatable, Self-validating, Timely.
- In `unittest`: subclass `unittest.TestCase`, name methods `test_*`, and use `self.assertEqual`, `assertTrue`, `assertIn`, `assertIsNone`, `assertAlmostEqual`, and `with self.assertRaises(...)`.
- **Fixtures**: `setUp`/`tearDown` (per test), `setUpClass`/`tearDownClass` (once per class), `addCleanup` (reliable cleanup). Use them to give every test its own clean data.
- `subTest` reports each failing input of a table-driven test separately.
- Run with `python -m unittest` (add `-v`, `-k`, `-f`, `-b`; or `discover -s tests`). Dots mean pass; `F` is a failed assertion; `E` is an unexpected exception; `s` skipped.
- Test normal cases, boundaries, empty and invalid input, and error handling. Test behaviour rather than implementation, one behaviour per test.
- Turn every bug into a regression test: write the failing test first (red), fix (green), tidy (refactor).
- `pytest` offers a lighter syntax and richer features, and will be covered in depth in later weeks; today's concepts carry over directly.

---

## Practice Questions and Mini-Exercises

**Q1.** Explain in your own words the difference between a unit test, an integration test and a system test.

**Q2.** What do the letters `. F E s` mean in unittest's compact output? What is the difference between a *failure* and an *error*?

**Q3.** Why must each test method be independent from the others? What feature of `unittest` helps you achieve this?

**Q4.** Rewrite this test so it is safe for floating-point numbers:

```python
def test_total(self):
    self.assertEqual(0.1 + 0.2, 0.3)
```

**Q5.** Which assertion would you use to check each? (a) a function returns `None` (b) the string `"error"` appears in a message (c) calling `parse("")` raises `ValueError` (d) two lists have the same items in any order (e) a duration is below 2 seconds.

**Q6.** What is wrong with this test suite design, and how would you fix it?

```python
class TestCart(unittest.TestCase):
    cart = []                       # class-level, shared by all tests

    def test_add_item(self):
        self.cart.append("pen")
        self.assertEqual(len(self.cart), 1)

    def test_cart_starts_empty(self):
        self.assertEqual(len(self.cart), 0)
```

**Q7 (mini-exercise).** Write a function `fizzbuzz(n)` returning `"Fizz"` for multiples of 3, `"Buzz"` for multiples of 5, `"FizzBuzz"` for multiples of both, otherwise the number as a string. Write a `TestFizzBuzz` class using `subTest` over a table of at least six cases, and run it.

**Q8 (mini-exercise).** Write `is_valid_username(name)`: valid if 3 to 12 characters, letters/digits/underscore only. Using boundary-value thinking, write at least eight tests (including 2, 3, 12 and 13 characters, an empty string, and a name with a space).

**Q9 (mini-exercise).** Add a test to `test_loader.py` so that a file with a blank `score` cell (`ann,`) is confirmed to raise `ValueError`. Run the suite. Then ask: is `ValueError` the *desired* behaviour? Discuss what a better design could be.

**Q10.** You change a function and three tests fail. The code is right and the *old test expectations* are outdated. Describe the process you should follow before editing the tests.

### Answers

**A1.** A *unit test* checks one small piece (a function or method) in isolation; it is fast and pinpoints the defect. An *integration test* checks that several units (or the code with a database/service) work together. A *system (end-to-end) test* exercises the whole application through its real interface; it is slower and a failure has many possible causes.

**A2.** `.` = a test passed; `F` = failure; `E` = error; `s` = skipped. A **failure** means an assertion evaluated false (the code ran but gave the wrong result). An **error** means an unexpected exception was raised in the test or the code under test (such as `KeyError`), so the check never completed.

**A3.** If tests share state or depend on order, one test can change what another sees, so results vary by run order and tests cannot be run singly or in parallel (the root of flaky tests; see the scope and mutability lessons). `setUp` (and `addCleanup`/`tearDown`) create fresh objects for every test.

**A4.**

```python
def test_total(self):
    self.assertAlmostEqual(0.1 + 0.2, 0.3)
```

**A5.** (a) `assertIsNone(result)`. (b) `assertIn("error", message)`. (c) `with self.assertRaises(ValueError): parse("")`. (d) `assertCountEqual(a, b)`. (e) `assertLess(duration, 2)`.

**A6.** `cart = []` is a class-level mutable object shared by every test (the mutability lesson in action). Because `unittest` runs methods alphabetically, `test_add_item` runs first and leaves `"pen"` in the shared list, so `test_cart_starts_empty` then fails; rename the tests and the outcome changes, which is exactly what "order-dependent" means. Fix: create the list in `setUp`: `def setUp(self): self.cart = []`.

**A7.** One possible answer:

```python
# fizzbuzz.py
def fizzbuzz(n):
    if n % 15 == 0:
        return "FizzBuzz"
    if n % 3 == 0:
        return "Fizz"
    if n % 5 == 0:
        return "Buzz"
    return str(n)
```

```python
# test_fizzbuzz.py
import unittest
from fizzbuzz import fizzbuzz

class TestFizzBuzz(unittest.TestCase):
    def test_table(self):
        cases = [(1, "1"), (3, "Fizz"), (5, "Buzz"), (15, "FizzBuzz"),
                 (7, "7"), (30, "FizzBuzz"), (9, "Fizz"), (10, "Buzz")]
        for number, expected in cases:
            with self.subTest(number=number):
                self.assertEqual(fizzbuzz(number), expected)

if __name__ == "__main__":
    unittest.main()
```

**A8.** One possible answer:

```python
# username.py
import re

def is_valid_username(name):
    return bool(re.fullmatch(r"[A-Za-z0-9_]{3,12}", name))
```

```python
# test_username.py
import unittest
from username import is_valid_username

class TestUsername(unittest.TestCase):
    def test_boundaries_and_invalid(self):
        cases = [
            ("ab", False),            # 2 chars: just below minimum
            ("abc", True),            # 3 chars: minimum
            ("a" * 12, True),         # 12 chars: maximum
            ("a" * 13, False),        # 13 chars: just above maximum
            ("", False),              # empty
            ("has space", False),     # space not allowed
            ("ok_name1", True),       # underscore and digit allowed
            ("bad-name", False),      # hyphen not allowed
        ]
        for name, expected in cases:
            with self.subTest(name=name):
                self.assertEqual(is_valid_username(name), expected)

if __name__ == "__main__":
    unittest.main()
```

(The `re` module is a standard library module for regular expressions; here it is just a convenient way to implement the rule. The learning point is the test design.)

**A9.**

```python
    def test_blank_score_raises_value_error(self):
        self.write("name,score\nann,\n")
        with self.assertRaises(ValueError):
            load_scores(self.path)
```

`int("")` raises `ValueError`, so it passes with the current code. Whether that is *desirable* is a design decision: a more helpful loader might raise a custom exception naming the row, or skip bad rows and report them (using the custom-exception and logging ideas from this week). Write the test for the behaviour you decide on.

**A10.** First prove which side is wrong: re-read the requirement/specification (or ask the owner), reproduce the behaviour manually, and check that the new behaviour is truly intended. Only then update the expectations, ideally in a separate commit with a clear message explaining the intentional behaviour change. Never edit expected values merely to turn the build green.

---

## Additional Resources

- Python Standard Library, `unittest` (Unit testing framework): https://docs.python.org/3/library/unittest.html
- Python Tutorial, "Brief Tour of the Standard Library - Quality Control" (doctest and unittest overview): https://docs.python.org/3/tutorial/stdlib.html#quality-control
- Python Standard Library, `unittest.mock` (mock object library, for later study): https://docs.python.org/3/library/unittest.mock.html
