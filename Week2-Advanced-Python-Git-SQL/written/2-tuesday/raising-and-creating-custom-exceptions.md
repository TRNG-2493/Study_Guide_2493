# Raising and Creating Custom Exceptions

## Learning Objectives

By the end of this lesson you will be able to:

- Use the `raise` statement to signal an error from your own code.
- Choose the most appropriate built-in exception for a situation.
- Explain **why** a function should raise an exception rather than return a "magic" error value.
- Re-raise an exception with a bare `raise`, and **chain** exceptions using `raise ... from ...`.
- Create your own **custom exception classes** by inheriting from `Exception`.
- Design a small **exception hierarchy** for a project (a base class plus specific children).
- Add extra information (attributes, formatted messages) to a custom exception.
- Catch custom exceptions at different levels of generality.
- Apply naming and design conventions used by professional Python code.

---

## Why This Matters

In the previous lesson you learned how to **catch** exceptions raised by Python. In this lesson you learn the other half of the story: how to **raise** them yourself.

Why would you ever want to create an error on purpose? Because in the QE Foundations project you are building, your own code is making decisions that Python itself knows nothing about:

- Python does not know that a test-data row with `age = -5` is invalid. *You* know that.
- Python does not know that your test-data file must contain an `email` column. *Your project* knows that.
- Python does not know that a configuration file with `"browser": "netscape"` is unsupported.

When your code detects a problem like this, it needs a clear, standard way to say "stop, this is wrong, and here is exactly why". That way is raising an exception.

Custom exceptions are especially valuable for QEs. A test framework must distinguish between:

- `TestDataError`: "the input data was bad" (probably the data owner's problem),
- `EnvironmentError`-style problems: "the server is not reachable" (probably an infrastructure issue), and
- a genuine product defect (a bug to be logged).

With well-named exceptions you can write handlers that route each kind of problem to the right person or process. Instead of every failure being a vague `Exception: something broke`, you get names like `MissingColumnError` or `InvalidRecordError` that explain themselves in a report or a CI log.

Today's demo and exercise ask you to build a robust file reader with custom exceptions and a data-ingestion module for Project 1. This lesson provides the foundation.

---

## The Concept

### 1. The `raise` Statement

`raise` creates an exception and immediately starts the exception-propagation process, exactly as if Python had raised it.

Basic syntax:

```python
raise ExceptionType("A helpful message")
```

Example:

```python
def set_age(age):
    if age < 0:
        raise ValueError("Age cannot be negative")
    return age


print(set_age(30))     # 30
print(set_age(-5))     # raises ValueError
```

Output:

```
30
Traceback (most recent call last):
  File "example.py", line 7, in <module>
    print(set_age(-5))
  File "example.py", line 3, in set_age
    raise ValueError("Age cannot be negative")
ValueError: Age cannot be negative
```

**What happens, step by step:**

1. `ValueError("Age cannot be negative")` **creates** an exception object, storing your message.
2. `raise` **throws** it. The current function stops immediately; nothing after the `raise` line in `set_age` runs.
3. Python searches the calling code for a matching `except`. Finding none, the program ends with a traceback, which shows your message.

You can (and should) catch it like any other:

```python
try:
    set_age(-5)
except ValueError as error:
    print("Rejected:", error)
```

```
Rejected: Age cannot be negative
```

You can also `raise` an exception *class* without parentheses (`raise ValueError`); Python creates the object for you with no message. Always include a message: an error without context wastes everyone's time.

### 2. Why Raise Instead of Returning an Error Value?

A beginner might write:

```python
def divide(a, b):
    if b == 0:
        return -1          # "-1 means error"
    return a / b
```

This is a design trap. Consider what happens:

```python
result = divide(10, 0)
print(result + 100)        # 99, silently wrong!
```

and what about `divide(-10, 10)`, which legitimately returns `-1.0`? The caller cannot tell "error" from "valid result". Worse, if the caller forgets to check, the bad value flows onward and causes a confusing failure far away from the real cause.

Exceptions solve this:

- They **cannot be ignored by accident**. If nobody handles them, the program stops loudly.
- They separate the **normal path** from the **error path**, so the return value always means what it says.
- They carry a **message and type** describing the problem.
- They **propagate automatically** up to the code that knows what to do.

The rule of thumb is: **fail fast and fail loudly**. If a function cannot do its job properly, raise an exception.

### 3. Choosing the Right Built-in Exception

Before inventing a new exception, check whether a built-in one fits. Using standard types makes your code predictable for other Python developers.

| Situation | Suggested exception |
|-----------|---------------------|
| Argument has the right type but an unacceptable value (negative age, empty name) | `ValueError` |
| Argument has the wrong type (string given where a number is needed) | `TypeError` |
| A required key is missing from a mapping | `KeyError` |
| A required file does not exist | `FileNotFoundError` |
| An operation is not allowed in the current state | `RuntimeError` |
| A feature is not written yet (placeholder) | `NotImplementedError` |
| Value outside an allowed range | `ValueError` (or `OverflowError` for numeric overflow) |

Examples:

```python
def set_browser(name):
    if not isinstance(name, str):
        raise TypeError(f"browser name must be a string, got {type(name).__name__}")
    if name.lower() not in ("chrome", "firefox", "edge"):
        raise ValueError(f"unsupported browser: {name!r}")
    return name.lower()


class ReportExporter:
    def export(self):
        raise NotImplementedError("Subclasses must implement export()")
```

**Line-by-line:**

- `isinstance(name, str)` tests whether `name` is a string. A non-string is a **type** problem, so `TypeError`.
- `type(name).__name__` gets the class name (like `'int'`) to make the message precise.
- `name.lower() not in (...)` tests the **value**; a string that is not a known browser is a **value** problem, so `ValueError`.
- `{name!r}` in an f-string prints the value with quotes (its `repr`), which makes whitespace and empty strings visible: `unsupported browser: ''` is much clearer than `unsupported browser: `.
- `NotImplementedError` is the conventional way to say "child classes must fill this in".

### 4. Re-raising: the Bare `raise`

Inside an `except` block, a bare `raise` (no argument) re-throws the exception currently being handled, with its original traceback intact:

```python
def load_config(path):
    try:
        with open(path) as f:
            return f.read()
    except FileNotFoundError:
        print(f"[config] Missing configuration file: {path}")
        raise                      # let the caller decide what to do next
```

Use this pattern when you want to *observe* (record, print, annotate) a failure but not *decide* its outcome. The caller still receives the original `FileNotFoundError`.

### 5. Exception Chaining: `raise ... from ...`

Often you catch a low-level exception and want to raise a higher-level, more meaningful one, without losing the original cause.

```python
def parse_quantity(text):
    try:
        return int(text)
    except ValueError as original:
        raise ValueError(f"Invalid quantity: {text!r}") from original


parse_quantity("abc")
```

Output:

```
Traceback (most recent call last):
  File "chain.py", line 3, in parse_quantity
    return int(text)
ValueError: invalid literal for int() with base 10: 'abc'

The above exception was the direct cause of the following exception:

Traceback (most recent call last):
  File "chain.py", line 8, in <module>
    parse_quantity("abc")
  File "chain.py", line 5, in parse_quantity
    raise ValueError(f"Invalid quantity: {text!r}") from original
ValueError: Invalid quantity: 'abc'
```

Both tracebacks appear, joined by "The above exception was the direct cause of..." This is invaluable for debugging because you see *what you meant* (the high-level message) and *what actually happened* (the low-level cause).

Three related behaviours:

| Syntax | Meaning | Traceback shows |
|--------|---------|-----------------|
| `raise NewError() from original` | Explicit chain: "NewError was caused by original" | "...was the direct cause of..." |
| `raise NewError()` inside an `except` block | Implicit chain: another error happened *while* handling | "During handling of the above exception, another exception occurred" |
| `raise NewError() from None` | Suppress the chain on purpose | Only the new exception |

The exception that was chained is available as `error.__cause__` (explicit) or `error.__context__` (implicit):

```python
try:
    parse_quantity("abc")
except ValueError as error:
    print("High-level message:", error)
    print("Original cause   :", repr(error.__cause__))
```

```
High-level message: Invalid quantity: 'abc'
Original cause   : ValueError("invalid literal for int() with base 10: 'abc'")
```

Use `from None` rarely, and only to hide a noisy internal detail that would confuse the reader.

### 6. Creating Custom Exceptions

A custom exception is simply a **class** that inherits from `Exception` (or from another exception class). If you have not yet met classes in depth, treat the following as a recipe; the key idea is "a new named kind of error".

The minimal version:

```python
class TestDataError(Exception):
    """Raised when test data is missing or invalid."""
```

That is it. The docstring is enough as the class body. Your new exception already behaves like any built-in one:

```python
try:
    raise TestDataError("users.csv has no rows")
except TestDataError as error:
    print("Caught:", error)
```

```
Caught: users.csv has no rows
```

**Explanation:**

- `class TestDataError(Exception):` defines a new class named `TestDataError`. The `(Exception)` part means "inherit from `Exception`", so the new class automatically gets all the machinery of an exception: a message, a traceback, the ability to be raised and caught.
- The triple-quoted string right below is a **docstring** describing when this exception is used.
- Names conventionally end in `Error` (for failures) or sometimes `Exception`/`Warning`, and use CapWords style.

Always inherit from `Exception`, **not** from `BaseException`. `BaseException` is reserved for things like `KeyboardInterrupt` and `SystemExit`; inheriting from it would make your errors escape ordinary `except Exception` handlers.

> **Note:** A class that you define in a file with a name starting with `Test` can be mistaken for a test class by some test-discovery tools. We will meet test frameworks on Wednesday. To avoid any confusion later, many teams name such exceptions `DataValidationError` or `InvalidTestDataError`. The examples in this lesson use `TestDataError` for readability; feel free to choose a different name in your own projects.

### 7. Why Bother? Specific Names Make Handlers Precise

Compare:

```python
# Hard to use: callers must parse the message text to know what happened
raise Exception("Missing column: email")
```

with:

```python
class MissingColumnError(Exception):
    pass

raise MissingColumnError("email")
```

Callers can now write:

```python
try:
    load_users("users.csv")
except MissingColumnError:
    print("Fix the file header")
except FileNotFoundError:
    print("Wrong path")
```

Never depend on string-matching error messages. Messages are for humans; **types** are for code.

### 8. Adding Information to a Custom Exception

Frequently you want an exception to carry structured data (which file, which row, which field) so that handlers and reports can use it. Override `__init__` and store the values as attributes:

```python
class InvalidRecordError(Exception):
    """A single record failed validation."""

    def __init__(self, row_number, field, value, reason):
        self.row_number = row_number
        self.field = field
        self.value = value
        self.reason = reason
        message = (
            f"Row {row_number}: field {field!r} has invalid value "
            f"{value!r} ({reason})"
        )
        super().__init__(message)
```

Usage:

```python
try:
    raise InvalidRecordError(17, "age", "-5", "must not be negative")
except InvalidRecordError as error:
    print(error)
    print("row   =", error.row_number)
    print("field =", error.field)
```

```
Row 17: field 'age' has invalid value '-5' (must not be negative)
row   = 17
field = age
```

**Line-by-line explanation:**

- `def __init__(self, row_number, field, value, reason):` is the **constructor**. Python calls it when you write `InvalidRecordError(17, "age", ...)`. `self` refers to the exception object being created.
- `self.row_number = row_number` (and the next three lines) store the details as **attributes** on the object so that handler code can read them later.
- We build a readable `message` string using an f-string.
- `super().__init__(message)` calls the parent class (`Exception`) constructor so that the standard behaviour works: `str(error)` and the traceback print our message. **Forgetting this call is a common mistake**; without it, the printed message may be empty or show only the raw arguments.

Because the exception carries structured data, a report generator can build a table of `(row_number, field, reason)` without parsing strings.

Another approach for simple cases is to give the class a default message:

```python
class ConfigError(Exception):
    """Raised when the configuration is invalid."""

    def __init__(self, message="Configuration is invalid"):
        super().__init__(message)


raise ConfigError()                       # uses default message
raise ConfigError("browser is missing")   # custom message
```

### 9. Building an Exception Hierarchy

For a real project, define one **base exception** for your whole library or module and derive specific errors from it. This is the standard professional pattern (the `requests` and `sqlalchemy` libraries use it).

```python
class DataIngestionError(Exception):
    """Base class for every error raised by the ingestion module."""


class SourceNotFoundError(DataIngestionError):
    """The input file could not be found."""


class UnsupportedFormatError(DataIngestionError):
    """The file extension / format is not supported."""


class ValidationError(DataIngestionError):
    """A record failed validation."""


class MissingFieldError(ValidationError):
    """A required field is absent from a record."""
```

The family tree:

```
Exception
 └── DataIngestionError
      ├── SourceNotFoundError
      ├── UnsupportedFormatError
      └── ValidationError
           └── MissingFieldError
```

This gives callers **choice of granularity**:

```python
try:
    ingest("orders.csv")
except MissingFieldError:           # very specific
    print("A required column is absent")
except ValidationError:             # a whole category
    print("Some record is invalid")
except DataIngestionError:          # everything from this module
    print("Ingestion failed for some other reason")
```

Remember the lesson from the previous topic: an `except` for a parent catches all its children, and specific handlers must come first.

The callers' view of "everything that can go wrong in the ingestion module" is now a single name: `DataIngestionError`. That makes it easy to write a safe top-level wrapper without resorting to `except Exception`, which would also swallow genuine programming bugs like `NameError`.

### 10. Wrapping Low-Level Errors in Your Own Exceptions

A good module translates low-level exceptions into its own vocabulary (using chaining so nothing is lost):

```python
def read_source(path):
    try:
        with open(path, encoding="utf-8") as f:
            return f.read()
    except FileNotFoundError as error:
        raise SourceNotFoundError(f"No such file: {path}") from error
    except PermissionError as error:
        raise DataIngestionError(f"Cannot read file: {path}") from error
```

Callers of `read_source` need to know only about `DataIngestionError` and its children; they do not need to know the module uses files internally. If you later change the implementation to read from a database, the exceptions callers see remain the same. This is **abstraction** applied to errors.

### 11. Where to Put Custom Exceptions

For a growing project, keep them in one dedicated module, `exceptions.py` (or `errors.py`), inside your package. Other modules do:

```python
from ingestion.exceptions import ValidationError
```

This ties directly to Monday's lessons on modules and packages: one well-named module, imported where needed, avoids circular imports and gives everyone a single place to look.

### 12. Design Guidelines

1. **Inherit from `Exception`**, never `BaseException`.
2. **Name with an `Error` suffix** and be descriptive.
3. **Create a base class** for each library/module so callers can catch everything from it.
4. **Keep them small.** A class with a docstring is often enough; add attributes only when handlers will use them.
5. **Do not create too many.** If callers would never handle two situations differently, one exception class is enough. Prefer standard exceptions when they fit.
6. **Write messages for humans:** what happened, to which value, and (if possible) what to do about it.
7. **Raise early**: validate inputs at the start of a function ("guard clauses") rather than letting bad data travel deep into the program.
8. **Do not use exceptions for ordinary control flow** (like ending a loop) when a simple `if` is clearer. They are for exceptional situations.

### 13. Guard Clauses

A guard clause is an early check that raises when preconditions are violated:

```python
def calculate_discount(price, percent):
    if not isinstance(price, (int, float)):
        raise TypeError("price must be a number")
    if price < 0:
        raise ValueError("price must not be negative")
    if not 0 <= percent <= 100:
        raise ValueError("percent must be between 0 and 100")

    return price * (1 - percent / 100)
```

Notice how the "happy path" (the last line) is un-indented and easy to read; all the error conditions are dealt with first. (In the next lesson you will see how *assertions* differ from this: they are for checking internal assumptions, while exceptions are for validating input.)

---

## Real-World QA Scenarios

### Scenario 1: A configuration validator for a test framework

Test suites rely on config values (browser, base URL, timeout). Catching a bad config **before** a 2-hour run begins saves a lot of time.

```python
class ConfigError(Exception):
    """Base class for configuration problems."""


class MissingSettingError(ConfigError):
    def __init__(self, name):
        self.name = name
        super().__init__(f"Required setting {name!r} is missing")


class InvalidSettingError(ConfigError):
    def __init__(self, name, value, expected):
        self.name = name
        self.value = value
        self.expected = expected
        super().__init__(
            f"Setting {name!r} has invalid value {value!r}; expected {expected}"
        )


SUPPORTED_BROWSERS = ("chrome", "firefox", "edge")


def validate_config(config):
    for required in ("browser", "base_url", "timeout"):
        if required not in config:
            raise MissingSettingError(required)

    if config["browser"] not in SUPPORTED_BROWSERS:
        raise InvalidSettingError(
            "browser", config["browser"], f"one of {SUPPORTED_BROWSERS}"
        )

    if not isinstance(config["timeout"], int) or config["timeout"] <= 0:
        raise InvalidSettingError(
            "timeout", config["timeout"], "a positive integer (seconds)"
        )

    return config


configs = [
    {"browser": "chrome", "base_url": "https://example.test", "timeout": 30},
    {"browser": "chrome", "timeout": 30},
    {"browser": "netscape", "base_url": "https://example.test", "timeout": 30},
    {"browser": "edge", "base_url": "https://example.test", "timeout": -1},
]

for number, cfg in enumerate(configs, start=1):
    try:
        validate_config(cfg)
    except ConfigError as error:
        print(f"Config {number}: INVALID -> {error}")
    else:
        print(f"Config {number}: OK")
```

Output:

```
Config 1: OK
Config 2: INVALID -> Required setting 'base_url' is missing
Config 3: INVALID -> Setting 'browser' has invalid value 'netscape'; expected one of ('chrome', 'firefox', 'edge')
Config 4: INVALID -> Setting 'timeout' has invalid value -1; expected a positive integer (seconds)
```

Notice how the single `except ConfigError` handles both specific types, yet the message tells exactly what is wrong. A handler could equally check `error.name` to look up a fix.

### Scenario 2: Distinguishing "bad data" from "environment" failures

```python
class TestRunError(Exception):
    """Base for failures in the test run itself (not product bugs)."""

class BadInputDataError(TestRunError):
    pass

class EnvironmentUnavailableError(TestRunError):
    pass


def run_case(case):
    if case.get("server_up") is False:
        raise EnvironmentUnavailableError("Test server is down")
    if "expected" not in case:
        raise BadInputDataError(f"Case {case['id']} has no expected value")
    return case["actual"] == case["expected"]


cases = [
    {"id": "TC1", "server_up": True, "expected": 5, "actual": 5},
    {"id": "TC2", "server_up": True, "actual": 5},
    {"id": "TC3", "server_up": False},
    {"id": "TC4", "server_up": True, "expected": 5, "actual": 6},
]

for case in cases:
    try:
        passed = run_case(case)
    except BadInputDataError as error:
        print(case["id"], "-> BLOCKED (fix the data):", error)
    except EnvironmentUnavailableError as error:
        print(case["id"], "-> BLOCKED (check the environment):", error)
    else:
        print(case["id"], "->", "PASS" if passed else "FAIL (possible product defect)")
```

Output:

```
TC1 -> PASS
TC2 -> BLOCKED (fix the data): Case TC2 has no expected value
TC3 -> BLOCKED (check the environment): Test server is down
TC4 -> FAIL (possible product defect)
```

This is precisely the distinction a QE needs: only `FAIL` suggests a bug in the product; the `BLOCKED` results point at your data or environment.

### Scenario 3: Translating a low-level error with chaining

```python
import json


class PayloadError(Exception):
    """The response payload could not be understood."""


def parse_payload(text):
    try:
        return json.loads(text)
    except json.JSONDecodeError as error:
        raise PayloadError("Response is not valid JSON") from error


try:
    parse_payload("{not json")
except PayloadError as error:
    print("Error :", error)
    print("Cause :", type(error.__cause__).__name__, "-", error.__cause__)
```

Output:

```
Error : Response is not valid JSON
Cause : JSONDecodeError - Expecting property name enclosed in double quotes: line 1 column 2 (char 1)
```

(You will meet the `json` module properly later today in *CSV, JSON and XML*.)

---

## Code Examples: Putting It All Together

A tiny but realistic "record validator" that uses a base exception, rich attributes, guard clauses, and a summary report. Save as `validator.py` and run it.

```python
"""validator.py - Validate user records and report every problem found."""


class ValidationError(Exception):
    """Base class for validation problems."""


class MissingFieldError(ValidationError):
    def __init__(self, row, field):
        self.row = row
        self.field = field
        super().__init__(f"Row {row}: missing required field {field!r}")


class OutOfRangeError(ValidationError):
    def __init__(self, row, field, value, low, high):
        self.row = row
        self.field = field
        self.value = value
        super().__init__(
            f"Row {row}: {field}={value!r} is outside {low}..{high}"
        )


def validate_user(row, user):
    for field in ("name", "age"):
        if field not in user:
            raise MissingFieldError(row, field)

    age = user["age"]
    if not 0 <= age <= 120:
        raise OutOfRangeError(row, "age", age, 0, 120)

    return user


users = [
    {"name": "Ada", "age": 36},
    {"name": "Grace"},
    {"name": "Linus", "age": 400},
    {"name": "Alan", "age": 41},
]

good, bad = [], []
for row, user in enumerate(users, start=1):
    try:
        good.append(validate_user(row, user))
    except ValidationError as error:
        bad.append(error)

print(f"{len(good)} valid, {len(bad)} invalid")
for error in bad:
    print(" -", error)
```

Output:

```
2 valid, 2 invalid
 - Row 2: missing required field 'age'
 - Row 3: age=400 is outside 0..120
```

Row 2 (`{"name": "Grace"}`) has a name but no age, so the loop over `("name", "age")` reports the first field that is absent: `'age'`.

**Walkthrough:**

1. `ValidationError` is the base class, so one `except ValidationError` in the loop handles every validator error.
2. Each child stores structured attributes (`row`, `field`, `value`) *and* builds a readable message via `super().__init__`.
3. `validate_user` uses guard clauses and raises as soon as it finds a problem.
4. The loop collects errors instead of stopping, then prints a summary: the pattern you will use in the data-ingestion milestone.

---

## Practice Exercises

**Exercise 1.** Write `withdraw(balance, amount)` that returns the new balance. It must raise `TypeError` if either argument is not a number, `ValueError` if `amount` is not positive, and `ValueError` with a clear message if `amount` exceeds the balance. Test each case with `try`/`except`.

**Exercise 2.** Create a custom exception `EmptyFileError` (inheriting from `Exception`). Write `check_not_empty(text)` that raises it when `text.strip()` is empty. Catch it and print a message.

**Exercise 3.** Build this hierarchy: `ReportError` (base) -> `ReportFormatError`, `ReportPermissionError`. Write a function that raises each depending on an argument, and a loop that catches (a) `ReportFormatError` individually and (b) everything else under `ReportError`.

**Exercise 4.** Create `InvalidStatusError` that stores `status` and `allowed` (a tuple) as attributes and builds the message `Status 'xyz' is not one of ('pass', 'fail', 'skip')`. Raise it from `set_status(value)`.

**Exercise 5.** Use `raise ... from ...` to wrap `KeyError` as `MissingSettingError("timeout")` in a `get_setting(config, name)` function. Show that `error.__cause__` holds the original `KeyError`.

**Exercise 6.** *Think and explain:* A teammate writes `except Exception as e: raise Exception(str(e))` to "clean up" errors. List at least two things lost by this approach.

### Answers

**Exercise 1:**

```python
def withdraw(balance, amount):
    if not isinstance(balance, (int, float)) or not isinstance(amount, (int, float)):
        raise TypeError("balance and amount must be numbers")
    if amount <= 0:
        raise ValueError("amount must be positive")
    if amount > balance:
        raise ValueError(f"insufficient funds: balance {balance}, requested {amount}")
    return balance - amount


for args in [(100, 30), ("100", 30), (100, -5), (100, 500)]:
    try:
        print(withdraw(*args))
    except (TypeError, ValueError) as error:
        print(type(error).__name__ + ":", error)
```

Output:

```
70
TypeError: balance and amount must be numbers
ValueError: amount must be positive
ValueError: insufficient funds: balance 100, requested 500
```

**Exercise 2:**

```python
class EmptyFileError(Exception):
    """File content is empty or whitespace only."""

def check_not_empty(text):
    if not text.strip():
        raise EmptyFileError("File contains no data")
    return text

try:
    check_not_empty("   \n")
except EmptyFileError as error:
    print("Caught:", error)
```

**Exercise 3:**

```python
class ReportError(Exception): pass
class ReportFormatError(ReportError): pass
class ReportPermissionError(ReportError): pass

def make_report(kind):
    if kind == "format":
        raise ReportFormatError("Bad layout")
    if kind == "perm":
        raise ReportPermissionError("Not allowed")
    return "ok"

for kind in ("format", "perm", "fine"):
    try:
        print(make_report(kind))
    except ReportFormatError as error:
        print("Format problem:", error)
    except ReportError as error:
        print("Other report problem:", error)
```

**Exercise 4:**

```python
class InvalidStatusError(Exception):
    def __init__(self, status, allowed):
        self.status = status
        self.allowed = allowed
        super().__init__(f"Status {status!r} is not one of {allowed}")

def set_status(value):
    allowed = ("pass", "fail", "skip")
    if value not in allowed:
        raise InvalidStatusError(value, allowed)
    return value

try:
    set_status("xyz")
except InvalidStatusError as error:
    print(error)    # Status 'xyz' is not one of ('pass', 'fail', 'skip')
```

**Exercise 5:**

```python
class MissingSettingError(Exception):
    pass

def get_setting(config, name):
    try:
        return config[name]
    except KeyError as original:
        raise MissingSettingError(f"Missing setting {name!r}") from original

try:
    get_setting({}, "timeout")
except MissingSettingError as error:
    print(error)                      # Missing setting 'timeout'
    print(repr(error.__cause__))      # KeyError('timeout')
```

**Exercise 6:** The original exception *type* is lost (everything becomes a plain `Exception`, so callers cannot catch it selectively); the original traceback and chain (what line failed, and why) is replaced by a new one pointing at the handler; attributes such as `.filename` or `.row_number` are lost; and catching `Exception` here would also catch unrelated bugs. A better approach is a bare `raise`, or `raise SpecificError(...) from e`.

---

## Summary / Key Takeaways

- `raise ExceptionType("message")` signals an error from your own code; execution of the current function stops immediately.
- Prefer exceptions over magic return values: they cannot be silently ignored and keep normal results unambiguous. **Fail fast, fail loudly.**
- Use the most fitting **built-in** exception first: `ValueError` for bad values, `TypeError` for wrong types, `NotImplementedError` for placeholders, and so on.
- A bare `raise` re-raises the current exception; `raise New(...) from original` **chains** exceptions so you keep both the friendly message and the real cause.
- A **custom exception** is a class that inherits from `Exception`. Give it an `Error` suffix, a docstring, and (when useful) attributes set in `__init__`, remembering to call `super().__init__(message)`.
- Create a **base exception** per module, with specific children, so callers can catch at the right level of detail. Store them in a dedicated `exceptions.py`.
- In QA code, distinct exception types separate bad test data and broken environments from genuine product failures.
- Next up: **assertions**, a different tool for checking things that "must always be true".

---

## Additional Resources

- Python Tutorial, "Raising Exceptions", "Exception Chaining" and "User-defined Exceptions": https://docs.python.org/3/tutorial/errors.html
- Python Language Reference, "The raise statement": https://docs.python.org/3/reference/simple_stmts.html#the-raise-statement
- Python Library Reference, "Built-in Exceptions": https://docs.python.org/3/library/exceptions.html
