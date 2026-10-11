# Mocking with unittest.mock

## Learning Objectives

By the end of this lesson you will be able to:

- Explain what test doubles are (dummy, stub, fake, mock, spy) and why we replace real dependencies in tests.
- Use `Mock` and `MagicMock` to create stand-in objects, configure return values and exceptions, and inspect how they were called.
- Use `patch` (as decorator, context manager, and via `patch.object`) to temporarily replace things in the code under test.
- Apply the golden rule "patch where the name is looked up, not where it is defined".
- Verify interactions with `assert_called_once_with`, `call_args`, `call_count`, and related helpers.
- Use `side_effect` for sequences and errors, and `spec` / `autospec` for safer mocks.
- Combine mocks with PyTest fixtures and `monkeypatch`, and know when not to mock.

## Why This Matters

The weekly epic is to convert manual test design into automation that is **fast, repeatable, and reliable**. Real systems contain things that are slow, costly, random, or outside your control: network calls, payment gateways, email servers, the current time, a flaky third-party API. A test that calls a real weather service fails when your Wi-Fi drops or the service is down, and a failure then tells you nothing about *your* code.

Mocking lets you replace those dependencies with controllable stand-ins so you can test *your* logic in isolation, including difficult scenarios (timeouts, server errors) that are almost impossible to provoke on demand. In **Project 1 (QE Foundations)** you will refactor tests to isolate utilities from external calls. Later, when automating UI flows with Playwright (we will cover this in depth on Thursday and Friday), you will occasionally mock network traffic as well, though with Playwright's own tooling rather than `unittest.mock`.

`unittest.mock` is part of Python's standard library: nothing to install. You should recall the previous lessons today: *Fixtures* (and `yield`), *Parametrization*, and *conftest.py*, because mocks are commonly provided via fixtures.

## The Concept

### 1. Test doubles: the vocabulary

A **test double** is any object that stands in for a real dependency during a test (like a stunt double in a film). Common kinds:

| Type | What it does | Example |
|------|--------------|---------|
| **Dummy** | Just fills a parameter; never really used | Passing `None` as an unused logger |
| **Stub** | Returns canned answers | `get_price()` always returns `9.99` |
| **Fake** | A simplified working implementation | An in-memory dictionary instead of a database |
| **Mock** | Records how it was used, so you can verify calls | "Was `send_email` called once with the right address?" |
| **Spy** | A real object wrapped to record calls | Wrapping the real function but watching it |

In everyday conversation people say "mock" for all of these, and `unittest.mock.Mock` can play the stub, mock, and spy roles.

### 2. Why mock? The decision checklist

Mock a dependency when it is:

- **Slow** (network, database, file system at scale).
- **Non-deterministic** (random numbers, current time).
- **Unavailable** (service not built yet, or only in production).
- **Costly or dangerous** (sending real emails, charging real cards).
- **Hard to put in a specific state** (simulate a 500 error or a timeout).

Do **not** mock the thing you are testing, and do not mock so much that the test only proves your mock works. Balance: unit tests mock boundaries; a few integration tests use real components.

### 3. The code under test

We will use this small module throughout, saved as `weather_service.py`. It calls an external HTTP API through the `requests` library (which you may need to install with `pip install requests`; our tests never perform a real network call, which is the point of this lesson).

```python
# weather_service.py
import requests

API_URL = "https://api.example-weather.test/v1/current"

def fetch_temperature(city):
    """Return the current temperature in Celsius for a city."""
    response = requests.get(API_URL, params={"city": city}, timeout=5)
    response.raise_for_status()
    data = response.json()
    return data["temp_c"]

def describe_weather(city):
    """Return a human readable description."""
    try:
        temp = fetch_temperature(city)
    except requests.RequestException:
        return "Weather unavailable"
    if temp < 10:
        return f"Cold ({temp} C)"
    if temp < 25:
        return f"Mild ({temp} C)"
    return f"Hot ({temp} C)"
```

(The URL ends in `.test`, a reserved top-level domain that never resolves, so even by accident a test cannot reach a real server.)

We want to test `describe_weather` without touching the network.

### 4. `Mock` and `MagicMock` basics

```python
from unittest.mock import Mock, MagicMock

m = Mock()
m.greet.return_value = "hello"
print(m.greet("Asha"))              # hello
print(m.greet.call_args)            # call('Asha')
print(m.greet.call_count)           # 1
```

**Explanation**

- `Mock()` creates an object that **accepts any attribute access and any call**. `m.greet` automatically becomes a child mock.
- `.return_value` is what calling the mock returns.
- `.call_args` records the last call's arguments; `.call_count` counts calls.

`MagicMock` is a `Mock` that also supports Python's *magic methods* (`__len__`, `__iter__`, `__enter__`, `__getitem__`, ...), so it can act as a context manager or container:

```python
mm = MagicMock()
mm.__len__.return_value = 3
print(len(mm))        # 3

with MagicMock() as ctx:     # works because MagicMock supports __enter__/__exit__
    pass
```

`patch` creates a `MagicMock` by default, so you will mostly use `MagicMock` without naming it.

**Configuring in the constructor:**

```python
fake_response = Mock(status_code=200)
fake_response.json.return_value = {"temp_c": 18}
```

- `Mock(status_code=200)` sets an attribute at creation.
- `fake_response.json.return_value = {...}` makes `fake_response.json()` return that dict.

### 5. `side_effect`: errors and sequences

`return_value` always returns the same thing. `side_effect` is more flexible:

```python
from unittest.mock import Mock

# 1. Raise an exception when called
boom = Mock(side_effect=ConnectionError("network down"))
# boom()  -> raises ConnectionError

# 2. Return a different value each call (an iterable)
seq = Mock(side_effect=[1, 2, 3])
print(seq(), seq(), seq())      # 1 2 3
# a fourth call raises StopIteration

# 3. Compute the result with a function
doubler = Mock(side_effect=lambda x: x * 2)
print(doubler(21))              # 42
```

If an item in an iterable `side_effect` is an exception class or instance, that exception is raised at that call, which is perfect for "fail twice then succeed" retry tests.

### 6. Verifying calls

Mocks remember interactions. Common assertions:

```python
from unittest.mock import Mock, call

notifier = Mock()
notifier.send("a@x.com", "Hi")
notifier.send("b@x.com", "Hi")

notifier.send.assert_called()                         # at least once
assert notifier.send.call_count == 2
notifier.send.assert_any_call("a@x.com", "Hi")        # at least one call matched
notifier.send.assert_called_with("b@x.com", "Hi")     # the LAST call
notifier.send.assert_has_calls(
    [call("a@x.com", "Hi"), call("b@x.com", "Hi")]    # in this order
)
notifier.other.assert_not_called()                     # 'other' was never called
```

Always include the parentheses on assertion methods; without them nothing is checked. Helpers:

| Assertion | Meaning |
|-----------|---------|
| `assert_called_once()` | Called exactly once |
| `assert_called_once_with(*args, **kwargs)` | Called exactly once, with those arguments |
| `assert_called_with(...)` | The most recent call used these arguments |
| `assert_any_call(...)` | Some call used these arguments |
| `assert_has_calls([...])` | These calls occurred, in order |
| `assert_not_called()` | Never called |
| `call_args`, `call_args_list` | Inspect arguments |
| `reset_mock()` | Clear history |

One important gotcha: **a typo in an assertion name** (`assert_called_onced`) on a plain `Mock` is treated as a normal attribute and silently does nothing in old versions; modern Python raises `AttributeError` for names starting with `assert` or `assret`. Still, spell carefully.

### 7. `patch`: replacing things in place

Creating a mock is not enough; you must make the **code under test use it**. `patch` temporarily replaces an object with a mock and **restores the original** afterwards.

```python
from unittest.mock import patch, Mock
import requests
from weather_service import describe_weather

def test_describe_weather_mild():
    fake_response = Mock()
    fake_response.json.return_value = {"temp_c": 18}
    fake_response.raise_for_status.return_value = None

    with patch("weather_service.requests.get", return_value=fake_response) as mock_get:
        result = describe_weather("Pune")

    assert result == "Mild (18 C)"
    mock_get.assert_called_once()
    args, kwargs = mock_get.call_args
    assert kwargs["params"] == {"city": "Pune"}
    assert kwargs["timeout"] == 5
```

**Line-by-line explanation**

- `patch("weather_service.requests.get", ...)` - the string is the **import path of the thing to replace**. Python looks up `weather_service`, then its attribute `requests`, then `get`, and swaps it for a `MagicMock` during the `with` block.
- `return_value=fake_response` - when `requests.get(...)` is called, it returns our fake response.
- `as mock_get` - gives us the mock for later assertions.
- Outside the `with` block, the real `requests.get` is back automatically.
- `mock_get.call_args` is a tuple of positional args and a dict of keyword args. `fetch_temperature` called `requests.get(API_URL, params=..., timeout=5)`, so `params` and `timeout` are in `kwargs`.

**As a decorator.** The mock is passed as an extra argument:

```python
from unittest.mock import patch, Mock

@patch("weather_service.requests.get")
def test_hot(mock_get):
    mock_get.return_value = Mock(
        **{"json.return_value": {"temp_c": 35}, "raise_for_status.return_value": None}
    )
    assert describe_weather("Delhi") == "Hot (35 C)"
```

`Mock(**{"json.return_value": ...})` shows that dotted attribute names can be configured through keyword arguments. Alternatively, set attributes on separate lines as before. With stacked `@patch` decorators the **bottom decorator's mock arrives first** in the argument list. Another PyTest-specific warning: when you use `@patch` with PyTest fixtures in the same signature, patch-provided mocks come first positionally; fixtures are matched by name afterwards. Many teams avoid confusion by using the context manager or fixtures.

### 8. THE golden rule: patch where it is looked up

This is the number-one source of "my mock does nothing!" confusion.

Suppose a module does `from requests import get` and then calls `get(...)`. The name `get` now lives *inside that module's namespace*. Patching `requests.get` changes the original, but the module still holds its **own reference** to the real function.

```python
# module_a.py
from requests import get      # name "get" now exists inside module_a

def load():
    return get("https://x.test")
```

To mock this you must patch the name **in module_a**: `patch("module_a.get")`, not `patch("requests.get")`.

Versus our `weather_service.py`, which does `import requests` and calls `requests.get(...)`. There, the attribute lookup happens at call time on the shared `requests` module object, so `patch("weather_service.requests.get")` and `patch("requests.get")` both work (they change the same attribute on the same module object). The safest rule:

> **Patch the name in the namespace of the code under test.**

### 9. `patch.object`, `patch.dict`, and `monkeypatch`

`patch.object(target, "attribute")` avoids strings:

```python
from unittest.mock import patch
import weather_service

def test_with_patch_object():
    with patch.object(weather_service, "fetch_temperature", return_value=5):
        assert weather_service.describe_weather("Oslo") == "Cold (5 C)"
```

We replaced the *helper function* `fetch_temperature` inside `weather_service`. Because `describe_weather` looks up `fetch_temperature` in the module's globals at call time, it uses the mock. That is a faster, simpler way to test `describe_weather`'s branching logic with no HTTP details at all.

`patch.dict` temporarily alters a dictionary such as `os.environ`:

```python
import os
from unittest.mock import patch

def test_env():
    with patch.dict(os.environ, {"API_KEY": "secret"}):
        assert os.environ["API_KEY"] == "secret"
    assert "API_KEY" not in os.environ
```

PyTest's own `monkeypatch` fixture does similar jobs (`setattr`, `setenv`, `setitem`) and cleans up automatically. Use `monkeypatch` for simple replacement with plain values or functions; use `unittest.mock` when you need **call recording and assertions** or configurable behaviours.

### 10. Error scenarios

The great strength of mocks is simulating failures:

```python
import requests
from unittest.mock import patch
from weather_service import describe_weather

def test_network_failure_is_handled():
    with patch("weather_service.requests.get",
               side_effect=requests.ConnectionError("down")):
        assert describe_weather("Pune") == "Weather unavailable"

def test_http_error_is_handled():
    from unittest.mock import Mock
    bad = Mock()
    bad.raise_for_status.side_effect = requests.HTTPError("500 Server Error")
    with patch("weather_service.requests.get", return_value=bad):
        assert describe_weather("Pune") == "Weather unavailable"
```

`requests.ConnectionError` and `requests.HTTPError` both inherit from `requests.RequestException`, so our `except requests.RequestException` catches them. Try getting a real service to produce an HTTP 500 on demand; with a mock it takes two lines.

### 11. `spec` and `autospec`: mocks that cannot lie

A plain `Mock` accepts any attribute or call, so a typo like `mock.sned(...)` passes silently, and a mock can drift from the real API. `spec` restricts a mock to the attributes of a real object; `autospec=True` also checks call signatures.

```python
from unittest.mock import Mock, create_autospec, patch

class Mailer:
    def send(self, to, subject):
        ...

m = Mock(spec=Mailer)
m.send("a@x.com", "Hi")      # fine
# m.sned("a@x.com", "Hi")   # AttributeError: Mock object has no attribute 'sned'

auto = create_autospec(Mailer, instance=True)
auto.send("a@x.com", "Hi")   # fine
# auto.send("a@x.com")       # TypeError: missing a required argument: 'subject'
```

And with patch: `patch("module.Mailer", autospec=True)`. Prefer `autospec` whenever practical; it catches tests that pass while the real call would crash.

### 12. Mocks as PyTest fixtures

Wrap `patch` in a fixture so tests share it and cleanup is automatic:

```python
# conftest.py or the test file
import pytest
from unittest.mock import patch, Mock

@pytest.fixture
def mock_get():
    with patch("weather_service.requests.get") as m:
        response = Mock()
        response.raise_for_status.return_value = None
        response.json.return_value = {"temp_c": 20}
        m.return_value = response
        yield m
```

```python
from weather_service import fetch_temperature

def test_fetch_temperature(mock_get):
    assert fetch_temperature("Pune") == 20
    mock_get.assert_called_once()
```

**Explanation:** the `with patch(...)` block wraps the `yield`, so the patch is active while the test runs and removed in teardown, whether the test passes or fails. This uses the `yield` fixture pattern from the *Fixtures* lesson. Keep fixtures like this in `conftest.py` if many tests need them.

### 13. Parametrize with mocks

Combine with *Parametrization* for a clean table of temperatures:

```python
import pytest
from unittest.mock import patch
from weather_service import describe_weather

@pytest.mark.parametrize("temp, expected", [
    (-5, "Cold (-5 C)"),
    (9, "Cold (9 C)"),
    (10, "Mild (10 C)"),
    (24, "Mild (24 C)"),
    (25, "Hot (25 C)"),
    (40, "Hot (40 C)"),
])
def test_describe_weather_boundaries(temp, expected):
    with patch("weather_service.fetch_temperature", return_value=temp):
        assert describe_weather("Anywhere") == expected
```

Boundary values 9/10 and 24/25 map to the manual test-design technique from earlier weeks.

### 14. Mocking time and randomness

Dependencies are not only network: current time and randomness are classic sources of flakiness.

```python
# greeting.py
import datetime

def greeting():
    hour = datetime.datetime.now().hour
    return "Good morning" if hour < 12 else "Good afternoon"
```

`datetime.datetime` is a built-in type whose attributes cannot be patched directly. Patch the whole name in your module instead:

```python
from unittest.mock import patch, Mock
import greeting as g

def test_morning():
    fake_dt = Mock()
    fake_dt.datetime.now.return_value = Mock(hour=8)
    with patch.object(g, "datetime", fake_dt):
        assert g.greeting() == "Good morning"

def test_afternoon():
    fake_dt = Mock()
    fake_dt.datetime.now.return_value = Mock(hour=15)
    with patch.object(g, "datetime", fake_dt):
        assert g.greeting() == "Good afternoon"
```

**Explanation:** the module did `import datetime` and calls `datetime.datetime.now()`. We replace the module-level name `datetime` inside `greeting` with `fake_dt`, whose `datetime.now()` returns an object with `.hour`. Other approaches include passing the clock in as a parameter (dependency injection) or using the third-party `freezegun` library; passing dependencies in is usually the cleanest design.

### 15. When mocking goes wrong (and design hints)

- **Over-mocking:** a test with six patches mirrors the implementation line by line. When someone refactors, the test breaks though behaviour is unchanged. Test behaviour and outcomes where possible.
- **Mocking what you do not own:** patching deep library internals ties tests to library details. Wrap external libraries in a small adapter class that *you* own, and mock the adapter.
- **Mock never verified:** if you configure a mock but never assert on the result or the call, the test may prove nothing.
- **Tests that pass trivially:** `assert mock.return_value == 5` after setting it to 5 tests nothing.
- If code is **hard to mock**, it is probably hard to test because of hidden dependencies. Passing collaborators as parameters (dependency injection) is often the better fix.

## Code Examples: a Project 1 scenario

Suppose Project 1's utilities include a notification service that emails a summary if any test failed. The email gateway is external.

```python
# notifier.py
class EmailGateway:
    def send(self, to, subject, body):
        raise RuntimeError("real gateway not available in tests")

def notify_failures(results, gateway, recipient="qa-team@example.test"):
    """results: list of dicts like {'name': 'login', 'status': 'fail'}.
    Sends one email if there are failures. Returns number of failures."""
    failures = [r["name"] for r in results if r["status"] == "fail"]
    if failures:
        gateway.send(
            recipient,
            f"{len(failures)} test(s) failed",
            "Failed: " + ", ".join(failures),
        )
    return len(failures)
```

```python
# test_notifier.py
import pytest
from unittest.mock import create_autospec
from notifier import EmailGateway, notify_failures

@pytest.fixture
def gateway():
    return create_autospec(EmailGateway, instance=True)

def test_sends_email_when_failures(gateway):
    results = [
        {"name": "login", "status": "pass"},
        {"name": "search", "status": "fail"},
        {"name": "checkout", "status": "fail"},
    ]

    count = notify_failures(results, gateway)

    assert count == 2
    gateway.send.assert_called_once_with(
        "qa-team@example.test",
        "2 test(s) failed",
        "Failed: search, checkout",
    )

def test_no_email_when_all_pass(gateway):
    results = [{"name": "login", "status": "pass"}]
    assert notify_failures(results, gateway) == 0
    gateway.send.assert_not_called()

def test_gateway_error_bubbles_up(gateway):
    gateway.send.side_effect = RuntimeError("smtp down")
    with pytest.raises(RuntimeError, match="smtp down"):
        notify_failures([{"name": "x", "status": "fail"}], gateway)
```

**Explanation**

- `create_autospec(EmailGateway, instance=True)` builds a mock whose `send` has the same signature as the real method. Calling it with a wrong number of arguments raises `TypeError`, so the test cannot drift away from reality.
- The `gateway` fixture gives each test a fresh mock (function scope), so call counts never leak.
- Test 1 verifies *interaction* (the mail was sent once with exact content). Test 2 verifies *absence* of interaction. Test 3 uses `side_effect` to simulate a failure and verifies error propagation.
- No real email is ever sent, and the tests run in milliseconds. Note this design passes the gateway in as a parameter; no `patch` was needed at all. When you can, prefer this.

## Real-World Scenarios

1. **Payments:** mock the gateway to simulate approved, declined, and timeout responses.
2. **Third-party APIs:** simulate rate limiting (HTTP 429) and retry logic with `side_effect=[error, error, success]`.
3. **Time-based features:** freeze "now" to test expiry or business-hour rules.
4. **Email/SMS:** assert the message was sent with the right content without sending.
5. **Feature isolation in UI automation:** keep unit-level helpers isolated; use Playwright's network routing for browser-level interception (we will cover this in depth on Friday and beyond).

## Common Mistakes

1. **Patching the wrong namespace** (defined-in vs looked-up-in). If the mock "does nothing", check how the code imports the name.
2. **Forgetting that `patch` as a decorator injects an argument** and then getting `TypeError: takes 0 positional arguments but 1 was given`.
3. **Stacked decorator order confusion:** the bottom decorator maps to the first mock argument.
4. **Misspelling attribute names on unspecced mocks**, producing tests that pass wrongly. Use `spec`/`autospec`.
5. **Not asserting anything on the mock.**
6. **Configuring `return_value` on the wrong level** (e.g., setting `mock_get.json.return_value` instead of `mock_get.return_value.json.return_value`). Remember: calling `requests.get(...)` returns `mock_get.return_value`, and *that* object's `.json()` is configured on it.
7. **Leaking patches** by starting them manually (`patcher.start()`) and never calling `stop()`. Prefer `with` blocks or fixtures.
8. **Over-mocking** until tests only mirror the implementation.
9. **Mocking the code under test itself.**
10. **Using real network "just this once".** Always make accidental real calls impossible, for example with an unresolvable `.test` domain.

## Practice Exercises

**Exercise 1.** Create `m = Mock()`, set `m.compute.return_value = 42`, call it with `(1, 2)`, and assert both the returned value and `m.compute.assert_called_once_with(1, 2)`.

*Solution:*

```python
from unittest.mock import Mock

def test_basic_mock():
    m = Mock()
    m.compute.return_value = 42
    assert m.compute(1, 2) == 42
    m.compute.assert_called_once_with(1, 2)
```

**Exercise 2.** Write a mock with `side_effect=[10, 20, ConnectionError("lost")]`. Call it three times, asserting the first two return values and that the third raises with `pytest.raises`.

**Exercise 3.** Test `describe_weather` for "Weather unavailable" by patching `weather_service.fetch_temperature` with `side_effect=requests.Timeout`. (Hint: `requests.Timeout` subclasses `RequestException`.)

**Exercise 4.** Create a fixture `mock_get` as in section 12 and add a test checking that `fetch_temperature("Mumbai")` makes the request with `params={"city": "Mumbai"}`.

*Hint:* `mock_get.call_args.kwargs["params"]`. (`call_args.kwargs` is available in Python 3.8+.)

**Exercise 5.** Write a function `read_config(path)` that opens a file and returns its stripped contents. Test it without a real file by patching `builtins.open` using `unittest.mock.mock_open(read_data="  value \n")`.

*Solution:*

```python
from unittest.mock import patch, mock_open

def read_config(path):
    with open(path) as f:
        return f.read().strip()

def test_read_config():
    with patch("builtins.open", mock_open(read_data="  value \n")):
        assert read_config("anything.cfg") == "value"
```

**Exercise 6.** Parametrize the weather boundaries test from section 13 yourself, adding two more boundary values.

**Exercise 7.** Use `create_autospec` to build a mock of a class with a method `charge(amount, currency)`, then demonstrate (in a test using `pytest.raises(TypeError)`) that calling `charge(5)` fails.

**Exercise 8 (reflection).** Find a place in your code where a function creates its own dependency internally (such as constructing a client). Rewrite it to accept the dependency as a parameter, and compare how the test changes (no `patch` needed).

**Exercise 9 (Project 1 link).** Pick one Project 1 utility that touches something external (file system, time, or a service). Write at least three tests for it using mocks: success, failure (via `side_effect`), and a call verification. Record which one you would also like to cover in an integration test with the real dependency.

## Summary

- Test doubles replace slow, random, costly, or unavailable dependencies; mocks also record how they were used.
- `Mock`/`MagicMock` accept any call; configure with `return_value` and `side_effect` (errors, sequences, functions).
- Verify interactions with `assert_called_once_with`, `assert_not_called`, `call_args`, and friends.
- `patch` replaces a name temporarily; patch where the name is **looked up**, not where it is defined.
- Use `patch.object`, `patch.dict`, `monkeypatch`, and `mock_open` for specific jobs.
- Prefer `spec`/`autospec` so mocks cannot drift from reality.
- Wrap patches in fixtures (with `yield`) for clean sharing and teardown; combine with parametrization.
- Design for injection where possible, avoid over-mocking, and keep some real integration tests.

## Additional Resources

- `unittest.mock` library reference: https://docs.python.org/3/library/unittest.mock.html
- `unittest.mock` getting started guide: https://docs.python.org/3/library/unittest.mock-examples.html
- PyTest `monkeypatch` documentation: https://docs.pytest.org/en/stable/how-to/monkeypatch.html
