# Pytest Beginner Interview Guide

## Questions, suggested answers, and coding solutions

This guide is designed for beginner-level candidates who know basic
Python and are starting with Pytest. Answers are interviewer reference
points: candidates do not need to use the exact wording, but they should
demonstrate the same understanding.



## Quick navigation

- [Conceptual Pytest questions](#1-introduction-to-pytest)
- [Scenario-based Pytest questions (20 scenarios)](#scenario-based-questions)
- [Difficulty classification](#question-by-question-difficulty-classification)


------------------------------------------------------------------------

## 1. Introduction to Pytest

### 1. What is Pytest, and why do we use it in automation testing?

<details>
<summary>Answer (click to reveal)</summary>

Pytest is a popular Python testing framework used to write, organize,
and run automated tests. It supports simple test functions, fixtures for
setup and cleanup, parameterization, markers, and detailed assertion
reporting.

It is commonly used for unit, integration, API, and UI automation tests.
It can also work with tools such as Playwright.

</details>

### 2. What are the advantages of Pytest over Python's built-in `unittest` framework?

<details>
<summary>Answer (click to reveal)</summary>

-   Pytest has a concise syntax: ordinary Python `assert` statements can
    be used.
-   It provides fixtures for reusable setup and teardown.
-   It supports parameterized tests through `@pytest.mark.parametrize`.
-   It offers flexible test selection using command-line options and
    markers.
-   It has a large plugin ecosystem for reporting, coverage, parallel
    execution, and other capabilities.

`unittest` is also useful and is included in Python's standard library.
Pytest can run many `unittest`-style tests as well.

</details>

### 3. How does Pytest identify test files and test functions during test execution?

<details>
<summary>Answer (click to reveal)</summary>

By default, Pytest discovers files matching patterns such as `test_*.py`
or `*_test.py`. Inside those files, it looks for functions whose names
begin with `test_`. It also collects test methods beginning with `test_`
from classes whose names typically begin with `Test`.

Discovery rules can be customized in the Pytest configuration file.

</details>

### 4. What naming conventions should we follow for Pytest test files and test functions?

<details>
<summary>Answer (click to reveal)</summary>

Common defaults are: - Files: `test_login.py` or `login_test.py` -
Functions and methods: `test_valid_login` - Test classes: `TestLogin`

Test classes should generally not define an `__init__` method, because
that can interfere with collection.

</details>

------------------------------------------------------------------------

## 2. Test Discovery and Organization

### 5. How does test discovery work in Pytest?

<details>
<summary>Answer (click to reveal)</summary>

When Pytest is run, it searches the specified path (or the current
directory by default), identifies files matching its configured
patterns, and collects test functions and methods matching its naming
rules. It then executes the collected tests.

Useful commands:

``` bash
pytest
pytest tests/
pytest tests/test_login.py
```

</details>

### 6. What are the naming conventions for test files, test classes, and test methods?

<details>
<summary>Answer (click to reveal)</summary>

The default conventions are `test_*.py` and `*_test.py` for files,
`Test...` for classes, and `test_...` for functions or methods. These
can be changed in `pytest.ini`, `pyproject.toml`, or another supported
configuration file.

</details>

### 7. How would you organize test cases in a Pytest project?

<details>
<summary>Answer (click to reveal)</summary>

A small project might use this structure:

``` text
project/
├── app/
│   └── calculator.py
├── tests/
│   ├── conftest.py
│   ├── test_calculator.py
│   └── test_login.py
├── pytest.ini
└── requirements.txt
```

Tests can be grouped by feature or component. Shared fixtures belong in
an appropriate `conftest.py`; reusable application or test helper code
can live in separate Python modules.

</details>

### 8. What is the difference between writing test cases as standalone functions and organizing them inside classes?

<details>
<summary>Answer (click to reveal)</summary>

Standalone functions are simple and are often sufficient. Classes can
group related tests and allow class-scoped fixtures or shared
class-level organization. Pytest does not require tests to be placed in
classes, and test classes do not need to inherit from a special Pytest
base class.

</details>

### 9. Can we write test cases inside a Python class without inheriting from any base class?

<details>
<summary>Answer (click to reveal)</summary>

Yes. A class named according to Pytest's collection convention, such as
`TestLogin`, can contain methods beginning with `test_`. It does not
need to inherit from a base class.

``` python
class TestLogin:
    def test_valid_username(self):
        assert "admin".startswith("ad")
```

</details>

------------------------------------------------------------------------

## 3. Assertions in Pytest

### 10. What are assertions in Pytest, and why are they important?

<details>
<summary>Answer (click to reveal)</summary>

Assertions verify that actual behavior matches the expected behavior. If
an assertion is false, the test fails and Pytest reports the failure,
including useful details about the expression.

``` python
def test_total():
    actual = 2 + 3
    expected = 5
    assert actual == expected
```

</details>

### 11. How do you verify whether an actual result matches the expected result?

<details>
<summary>Answer (click to reveal)</summary>

Use a Python `assert` statement with the appropriate comparison:

``` python
assert actual == expected
assert status_code == 200
assert "Welcome" in page_title
```

</details>

### 12. What happens when an assertion fails during test execution?

<details>
<summary>Answer (click to reveal)</summary>

The current test is marked as failed. Pytest displays the assertion
location and comparison details where available. By default, other tests
continue to run unless execution is stopped by an option such as `-x` or
another interruption.

</details>

### 13. How do you perform multiple validations within a single test case?

<details>
<summary>Answer (click to reveal)</summary>

Use multiple assertions when they validate related outcomes from the
same test scenario:

``` python
def test_profile():
    profile = {"name": "Asha", "active": True}
    assert profile["name"] == "Asha"
    assert profile["active"] is True
```

If an assertion fails, normal execution of that test function stops at
that point. For independent checks, separate tests are often easier to
diagnose.

</details>

### 14. Can you explain the difference between built-in Python assertions and custom assertions?

<details>
<summary>Answer (click to reveal)</summary>

Pytest uses Python's built-in `assert` statement and enhances its
failure output through assertion rewriting. A "custom assertion" usually
means a helper function or reusable validation that a team writes for a
domain-specific check. It is not a separate built-in assertion syntax in
Pytest.

``` python
def assert_user_is_active(user):
    assert user["active"] is True, "Expected user to be active"
```

</details>

------------------------------------------------------------------------

## 4. Pytest Markers

### 15. What are Pytest markers, and why do we use them?

<details>
<summary>Answer (click to reveal)</summary>

Markers attach metadata to tests. They can be used to categorize tests,
control execution, or describe expected behavior. Common built-in
markers include `skip`, `skipif`, `xfail`, and `parametrize`. Teams can
also define custom markers such as `smoke` and `regression`.

</details>

### 16. How do you mark a test case as a smoke test or regression test?

<details>
<summary>Answer (click to reveal)</summary>

Use custom markers and register them in the Pytest configuration to
avoid unknown-marker warnings.

``` python
import pytest

@pytest.mark.smoke
def test_homepage_loads():
    assert True

@pytest.mark.regression
def test_order_history():
    assert 1 + 1 == 2
```

Example `pytest.ini`:

``` ini
[pytest]
markers =
    smoke: quick checks for critical functionality
    regression: broader regression test cases
```

</details>

### 17. What is the purpose of the `skip` and `skipif` markers?

<details>
<summary>Answer (click to reveal)</summary>

`skip` always skips a test. `skipif` skips it only when its condition is
true.

``` python
import pytest

@pytest.mark.skip(reason="Feature is not ready")
def test_new_feature():
    assert True

@pytest.mark.skipif(
    True,
    reason="This environment does not support the feature"
)
def test_platform_feature():
    assert True
```

</details>

### 18. What is the difference between `skip` and `xfail`?

<details>
<summary>Answer (click to reveal)</summary>

A skipped test is not run. An `xfail` test is run but is expected to
fail. If an `xfail` test fails as expected, Pytest reports it as
xfailed; if it unexpectedly passes, it is reported as xpassed.
`strict=True` can make an unexpected pass fail the test run.

``` python
@pytest.mark.xfail(reason="Known bug", strict=True)
def test_known_bug():
    assert 1 == 2
```

</details>

### 19. How can you execute test cases based on a particular marker?

<details>
<summary>Answer (click to reveal)</summary>

Use `-m` followed by the marker expression:

``` bash
pytest -m smoke
pytest -m regression
pytest -m "smoke or regression"
pytest -m "not slow"
```

</details>

------------------------------------------------------------------------

## 5. Test Execution

### 20. How do you execute all test cases in a Pytest project?

<details>
<summary>Answer (click to reveal)</summary>

Run this from the project directory:

``` bash
pytest
```

Pytest starts discovery from the current directory unless a path is
supplied.

</details>

### 21. How would you execute a single test file?

<details>
<summary>Answer (click to reveal)</summary>

Pass the file path:

``` bash
pytest tests/test_login.py
```

</details>

### 22. How can you execute a specific test function from a test file?

<details>
<summary>Answer (click to reveal)</summary>

Use the node ID, which is the file path followed by `::` and the test
name:

``` bash
pytest tests/test_login.py::test_valid_login
```

</details>

### 23. How do you execute a particular test method inside a test class?

<details>
<summary>Answer (click to reveal)</summary>

Include the class name and method name in the node ID:

``` bash
pytest tests/test_login.py::TestLogin::test_valid_login
```

</details>

### 24. How can you execute only test cases marked with a specific marker?

<details>
<summary>Answer (click to reveal)</summary>

Use marker selection:

``` bash
pytest -m smoke
```

The marker must be applied to the test or inherited from a containing
class/module, as appropriate.

</details>

### 25. What is the purpose of the `-v`, `-s`, and `-k` command-line options?

<details>
<summary>Answer (click to reveal)</summary>

-   `-v` / `--verbose`: displays more detailed test names and outcomes.
-   `-s`: disables output capture, so print statements and standard
    output are shown.
-   `-k`: selects tests whose names or other collected keywords match an
    expression.

Examples:

``` bash
pytest -v
pytest -s
pytest -k "login"
pytest -k "login and not invalid"
```

Other useful options include `-q` for quieter output, `-x` to stop after
the first failure, and `--maxfail=2` to stop after two failures.

</details>

------------------------------------------------------------------------

## 6. Fixtures in Pytest

### 26. What is a fixture in Pytest, and why do we use it?

<details>
<summary>Answer (click to reveal)</summary>

A fixture provides data, objects, or setup needed by tests. Fixtures
help avoid repeating setup code and can also perform cleanup. Examples
include creating a test user, opening a database connection, or starting
a browser page.

</details>

### 27. How do you create and use a fixture in a test case?

<details>
<summary>Answer (click to reveal)</summary>

Decorate a function with `@pytest.fixture`, then request it as an
argument in the test. Pytest resolves the fixture by its name.

``` python
import pytest

@pytest.fixture
def sample_user():
    return {"username": "asha", "active": True}

def test_user_is_active(sample_user):
    assert sample_user["active"] is True
```

</details>

### 28. What is the purpose of the `@pytest.fixture` decorator?

<details>
<summary>Answer (click to reveal)</summary>

It tells Pytest that the function is a fixture. Pytest can then provide
its return value (or yielded value) to tests or other fixtures that
request it by name.

</details>

### 29. What are fixture scopes in Pytest?

<details>
<summary>Answer (click to reveal)</summary>

Scope controls how often a fixture is created and how long its value is
reused: - `function`: once per test function (default). - `class`: once
per test class. - `module`: once per test module. - `package`: once per
package. - `session`: once per test session.

A broader scope can reduce setup cost, but shared state must be managed
carefully.

</details>

### 30. Can you explain the difference between function, class, module, and session scopes?

<details>
<summary>Answer (click to reveal)</summary>

A function-scoped fixture is created separately for each test function.
A class-scoped fixture is shared by tests in a class. A module-scoped
fixture is shared within one test module. A session-scoped fixture is
shared for the whole test session. Package scope shares within a
package.

</details>

### 31. What happens if we don't specify a fixture scope?

<details>
<summary>Answer (click to reveal)</summary>

The default scope is `function`, so Pytest creates a fresh fixture
instance for each test function that requests it.

</details>

### 32. How can one test case use multiple fixtures?

<details>
<summary>Answer (click to reveal)</summary>

List each fixture as a test function argument. Pytest supplies each one
by name.

``` python
@pytest.fixture
def username():
    return "asha"

@pytest.fixture
def password():
    return "safe-password"

def test_credentials(username, password):
    assert username
    assert len(password) >= 8
```

</details>

### 33. What is the purpose of the `autouse=True` parameter in fixtures?

<details>
<summary>Answer (click to reveal)</summary>

An autouse fixture is automatically applied to tests within its
applicable scope, without each test needing to request it by name. Use
it for genuinely common setup or cleanup; avoid hiding important
dependencies unnecessarily.

``` python
@pytest.fixture(autouse=True)
def announce_test():
    print("Starting a test")
```

</details>

### 34. What is the use of the `yield` keyword inside a fixture?

<details>
<summary>Answer (click to reveal)</summary>

Code before `yield` performs setup. The yielded value is made available
to the test. Code after `yield` performs teardown after the test (or
dependent fixture usage) finishes.

``` python
@pytest.fixture
def resource():
    print("Setup")
    item = {"ready": True}
    yield item
    print("Cleanup")
    item.clear()

def test_resource(resource):
    assert resource["ready"] is True
```

If setup fails before reaching `yield`, the post-yield teardown portion
does not run for that fixture.

</details>

------------------------------------------------------------------------

## 7. Parameterization

### 35. What is parameterization in Pytest, and why is it useful?

<details>
<summary>Answer (click to reveal)</summary>

Parameterization runs the same test logic with multiple input sets. It
reduces duplicated test code and makes it easier to cover different
values and scenarios.

</details>

### 36. How do you execute the same test case with multiple sets of input data?

<details>
<summary>Answer (click to reveal)</summary>

Use `@pytest.mark.parametrize`:

``` python
import pytest

@pytest.mark.parametrize(
    "number, expected",
    [(1, 2), (2, 4), (3, 6)]
)
def test_double(number, expected):
    assert number * 2 == expected
```

Pytest collects this as three test cases.

</details>

### 37. What is the purpose of `@pytest.mark.parametrize`?

<details>
<summary>Answer (click to reveal)</summary>

It supplies multiple values to a test function, creating a separate test
invocation for each parameter set. Each invocation has its own result in
the report.

</details>

### 38. How can you pass multiple parameters to a single test function?

<details>
<summary>Answer (click to reveal)</summary>

Provide a comma-separated list of argument names and a sequence of
tuples (or other supported parameter sets):

``` python
@pytest.mark.parametrize(
    "username, password, expected",
    [
        ("valid_user", "valid_pass", True),
        ("valid_user", "wrong_pass", False),
    ],
)
def test_login_validation(username, password, expected):
    result = bool(username == "valid_user" and password == "valid_pass")
    assert result is expected
```

</details>

### 39. Can we combine fixtures with parameterization? If yes, how?

<details>
<summary>Answer (click to reveal)</summary>

Yes. A test can request fixtures and also receive parameterized values.
To parameterize a fixture itself, use `params=` in `@pytest.fixture`.

``` python
import pytest

@pytest.fixture(params=["chrome", "firefox"])
def browser_name(request):
    return request.param

def test_browser_name(browser_name):
    assert browser_name in ["chrome", "firefox"]
```

This test runs once for each fixture parameter.

</details>

### 40. What is the difference between parameterizing a test function and parameterizing a fixture?

<details>
<summary>Answer (click to reveal)</summary>

Function parameterization supplies data directly to a particular test
function using `@pytest.mark.parametrize`. Fixture parameterization
supplies different values through a fixture, which can be reused by
multiple tests that request that fixture. Fixture parameterization is
useful when the same setup variations apply to several tests.

</details>

------------------------------------------------------------------------

## 8. `conftest.py`

### 41. What is `conftest.py` in Pytest?

<details>
<summary>Answer (click to reveal)</summary>

`conftest.py` is a special Pytest file used to define fixtures and
certain test configuration or hooks that can be shared by tests in its
directory tree. It is automatically discovered by Pytest and is not
imported directly by test files.

</details>

### 42. Why do we use `conftest.py` instead of defining all fixtures inside individual test files?

<details>
<summary>Answer (click to reveal)</summary>

It avoids duplicating common fixtures and keeps test files focused on
test behavior. For example, a shared login or database fixture can be
defined once and used by multiple test modules in the relevant directory
tree.

</details>

### 43. How can fixtures defined in `conftest.py` be accessed by multiple test files?

<details>
<summary>Answer (click to reveal)</summary>

Place `conftest.py` in a directory that is an ancestor of those test
files. Tests can request its fixtures by argument name; they do not need
to import the fixture.

Example:

``` text
tests/
├── conftest.py
├── test_login.py
└── test_profile.py
```

</details>

### 44. Can we define multiple fixtures in a single `conftest.py` file?

<details>
<summary>Answer (click to reveal)</summary>

Yes. A `conftest.py` file can contain multiple fixtures and relevant
hooks. For maintainability, related fixtures can be grouped logically.

</details>

### 45. Can we have multiple `conftest.py` files in a Pytest project?

<details>
<summary>Answer (click to reveal)</summary>

Yes. Different test directories can have their own `conftest.py` files.
Fixtures in a nearer `conftest.py` are available to tests in that
directory tree, while parent-level fixtures can be shared more broadly.
Organize them carefully to avoid confusing fixture visibility.

</details>

------------------------------------------------------------------------

## 9. Mocking

### 46. What is mocking in Python testing, and why do we use it?

<details>
<summary>Answer (click to reveal)</summary>

Mocking replaces a real dependency with a controlled test double. It is
useful when a test should not call a real API, send an email, access an
external service, or depend on a slow or unreliable system. It also lets
a test verify how a dependency was called.

Python's standard `unittest.mock` module provides `Mock`, `MagicMock`,
and `patch`.

</details>

### 47. What is the difference between `Mock` and `MagicMock`?

<details>
<summary>Answer (click to reveal)</summary>

Both create mock objects and allow attributes and methods to be
configured. `MagicMock` also pre-creates support for many Python magic
or special methods, such as `__len__`, `__iter__`, and item access. Use
`Mock` for ordinary method/attribute behavior and `MagicMock` when
special methods need to be mocked.

</details>

### 48. Can you explain a scenario where mocking would be useful in automation testing?

<details>
<summary>Answer (click to reveal)</summary>

Suppose a registration flow sends a welcome email. A UI or service test
should not send a real email every time. The email sender can be mocked,
and the test can verify that it was called with the expected address.
Another example is replacing a third-party payment service with a
controlled response.

</details>

### 49. How can you mock an API response or an external dependency during testing?

<details>
<summary>Answer (click to reveal)</summary>

Patch the dependency where the code under test looks it up, configure
the mock's return value, and assert the expected behavior. For
HTTP-level tests, a dedicated HTTP mocking library may also be
appropriate.

```python
# service.py
import requests

def get_user(user_id):
    response = requests.get(f"https://example.test/users/{user_id}")
    response.raise_for_status()
    return response.json()
```

```python
# test_service.py
from unittest.mock import patch
from service import get_user

@patch("service.requests.get")
def test_get_user(mock_get):
    mock_get.return_value.json.return_value = {
        "id": 7,
        "name": "Asha",
    }
    mock_get.return_value.raise_for_status.return_value = None

    result = get_user(7)

    assert result["name"] == "Asha"
    mock_get.assert_called_once_with("https://example.test/users/7")
```

The patch target is `service.requests.get` because that is where the
function under test looks up `requests.get`.

</details>

------------------------------------------------------------------------

## 10. Data-Driven Testing

### 50. What is data-driven testing?

<details>
<summary>Answer (click to reveal)</summary>

Data-driven testing is an approach where the same test logic is executed
with different input data sets. It is useful for validating many
combinations without writing a separate test function for each one.

</details>

### 51. How can you implement data-driven testing using Pytest?

<details>
<summary>Answer (click to reveal)</summary>

A common approach is `@pytest.mark.parametrize`. Test data can also be
loaded from JSON, CSV, or other sources and then supplied to a test.
Keep test data readable and make failures easy to identify.

</details>

### 52. What is the difference between data-driven testing and parameterization?

<details>
<summary>Answer (click to reveal)</summary>

Data-driven testing is the broader testing approach: drive test
execution using multiple data sets. Parameterization is one technique
for implementing it. In Pytest, `@pytest.mark.parametrize` is a common
way to do this.

</details>

### 53. How would you test a login functionality with multiple sets of valid and invalid credentials?

<details>
<summary>Answer (click to reveal)</summary>

Prepare several username/password/expected-result combinations and
parameterize the test. In a real application test, call the login
function or UI workflow and assert the actual result, rather than
calculating the expected result in the test itself.

``` python
import pytest

@pytest.mark.parametrize(
    "username, password, expected_message",
    [
        ("valid_user", "correct_password", "Welcome"),
        ("valid_user", "wrong_password", "Invalid credentials"),
        ("unknown_user", "any_password", "Invalid credentials"),
        ("", "", "Username is required"),
    ],
    ids=["valid-login", "wrong-password", "unknown-user", "empty-input"],
)
def test_login(username, password, expected_message):
    # Replace this call with the application's real login operation.
    actual_message = login(username, password)
    assert actual_message == expected_message
```

`login()` is an application function and must be implemented or imported
from the system under test.

</details>

------------------------------------------------------------------------

## 11. Performance Profiling and Reporting

### 54. How can you generate an HTML test execution report in Pytest?

<details>
<summary>Answer (click to reveal)</summary>

One common option is the `pytest-html` plugin.

Install and run:

``` bash
pip install pytest-html
pytest --html=report.html --self-contained-html
```

The report contains test outcomes and other execution details. Exact
contents depend on plugin configuration and version.

</details>

### 55. What information can we obtain from a Pytest execution report?

<details>
<summary>Answer (click to reveal)</summary>

A report commonly includes passed, failed, skipped, and error counts;
test names; execution details; durations; and failure tracebacks.
Additional metadata, logs, or screenshots can be added through plugins
or hooks.

</details>

### 56. What is performance profiling in Python?

<details>
<summary>Answer (click to reveal)</summary>

Performance profiling measures where a program spends time or other
resources. It helps identify slow functions or bottlenecks. Profiling is
different from simply checking whether a test passes or fails.

</details>

### 57. How can you identify which part of your test execution is taking the most time?

<details>
<summary>Answer (click to reveal)</summary>

Pytest's `--durations` option reports the slowest test durations:

``` bash
pytest --durations=10
```

For function-level profiling, Python's `cProfile` can be used. A
benchmark plugin such as `pytest-benchmark` can help measure and compare
code performance. Be careful to distinguish application performance from
test-framework, browser startup, network, and environment overhead.

</details>

### 58. Have you worked with any Pytest reporting or profiling plugins?

<details>
<summary>Answer (click to reveal)</summary>

A beginner might mention: - `pytest-html` for HTML reports. -
`pytest-cov` for code coverage. - `pytest-xdist` for parallel test
execution. - `pytest-benchmark` for benchmarking. -
`pytest-rerunfailures` for rerunning failures (useful in some
environments, but not a substitute for fixing flaky tests).

A strong candidate should explain what a plugin does and when they would
use it, rather than only listing names.

</details>

------------------------------------------------------------------------

# Practical Coding Exercises with Solutions

These exercises can be given during the interview. Each solution is
self-contained unless noted.

## Exercise 1: Write a basic test to verify that two numbers are equal

**What to ask**

Write a Pytest test that adds two numbers and verifies that the result
is correct.

<details>
<summary>Answer / solution (click to reveal)</summary>

``` python
def test_addition():
    actual = 10 + 5
    expected = 15

    assert actual == expected
```

**Run**

``` bash
pytest -v test_math.py
```

**Evaluate:** test naming, basic Python, and use of `assert`.

</details>

## Exercise 2: Create a fixture and use it in a test

**What to ask**

Create a fixture that returns a sample user and use it to verify the
user's name.

<details>
<summary>Answer / solution (click to reveal)</summary>

``` python
import pytest

@pytest.fixture
def user():
    return {
        "name": "Asha",
        "role": "tester",
    }

def test_user_name(user):
    assert user["name"] == "Asha"
```

**Evaluate:** fixture decorator, fixture naming, and dependency
injection by argument name.

</details>

## Exercise 3: Demonstrate setup and teardown using `yield`

**What to ask**

Create a fixture that prints a setup message before the test and a
cleanup message after the test.

<details>
<summary>Answer / solution (click to reveal)</summary>

``` python
import pytest

@pytest.fixture
def sample_resource():
    print("Setting up resource")
    resource = {"connected": True}

    yield resource

    print("Cleaning up resource")
    resource["connected"] = False

def test_resource_connection(sample_resource):
    assert sample_resource["connected"] is True
```

**Run**

``` bash
pytest -s -v
```

**Evaluate:** understanding of setup, yield, teardown, and output
capture.

</details>

## Exercise 4: Write a parameterized test for multiple login inputs

**What to ask**

Use three or more sets of credentials to test a simple login-validation
function.

<details>
<summary>Answer / solution (click to reveal)</summary>

``` python
import pytest

def validate_login(username, password):
    return username == "admin" and password == "secret"

@pytest.mark.parametrize(
    "username, password, expected",
    [
        ("admin", "secret", True),
        ("admin", "wrong", False),
        ("guest", "secret", False),
    ],
)
def test_validate_login(username, password, expected):
    assert validate_login(username, password) is expected
```

**Evaluate:** parameter names, test data, and expected-result
assertions.

</details>

## Exercise 5: Create and execute smoke tests using a marker

**What to ask**

Mark one test as smoke and another as regression. Explain how to execute
only smoke tests.

<details>
<summary>Answer / solution (click to reveal)</summary>

``` python
import pytest

@pytest.mark.smoke
def test_homepage():
    assert 200 == 200

@pytest.mark.regression
def test_order_history():
    assert "order" in "order history"
```

<details>
<summary>Answer / solution (click to reveal)</summary>

``` ini
[pytest]
markers =
    smoke: critical quick checks
    regression: broader regression checks
```

**Run only smoke tests**

``` bash
pytest -m smoke -v
```

**Evaluate:** marker syntax, registration, and command-line selection.

</details>

## Exercise 6: Move a fixture into `conftest.py`

**What to ask**

Create a shared fixture in `conftest.py` and use it from two test files
without importing it.

**Project structure**

``` text
project/
└── tests/
    ├── conftest.py
    ├── test_user.py
    └── test_admin.py
```

<details>
<summary>Answer / solution (click to reveal)</summary>

``` python
import pytest

@pytest.fixture
def sample_user():
    return {"username": "asha", "role": "user"}
```

<details>
<summary>Answer / solution (click to reveal)</summary>

``` python
def test_username(sample_user):
    assert sample_user["username"] == "asha"
```

<details>
<summary>Answer / solution (click to reveal)</summary>

``` python
def test_user_role(sample_user):
    assert sample_user["role"] == "user"
```

**Run**

``` bash
pytest tests/ -v
```

**Evaluate:** shared fixture discovery and understanding that
`conftest.py` fixtures are not imported directly.

</details>

## Exercise 7: Use two fixtures in one test

**What to ask**

Create separate fixtures for a username and password, then use both in
one test.

<details>
<summary>Answer / solution (click to reveal)</summary>

``` python
import pytest

@pytest.fixture
def username():
    return "admin"

@pytest.fixture
def password():
    return "secret"

def test_credentials_are_present(username, password):
    assert username != ""
    assert password != ""
```

**Evaluate:** requesting multiple fixtures by argument name.

</details>

## Exercise 8: Mock a function that returns a user ID

**What to ask**

Mock a dependency that fetches a user ID. Verify the returned value and
that the dependency was called.

<details>
<summary>Answer / solution (click to reveal)</summary>

``` python

</details>

# user_service.py
def fetch_user_id():
    # Imagine this calls an external service.
    return 100

def get_current_user_id():
    return fetch_user_id()
```

``` python

</details>

# test_user_service.py
from unittest.mock import patch
from user_service import get_current_user_id

@patch("user_service.fetch_user_id")
def test_get_current_user_id(mock_fetch):
    mock_fetch.return_value = 501

    result = get_current_user_id()

    assert result == 501
    mock_fetch.assert_called_once_with()
```

**Evaluate:** mock return values, patch target, and call assertions.

</details>

------------------------------------------------------------------------

</details>

# Additional Useful Interview Exercises

## Exercise 9: Select a test by its node ID

**What to ask**

Given a test file named `test_calculator.py` with a function named
`test_addition`, how would you run only that test?

<details>
<summary>Answer (click to reveal)</summary>

``` bash
pytest tests/test_calculator.py::test_addition -v
```

</details>

## Exercise 10: Demonstrate fixture scopes

**What to ask**

Write a module-scoped fixture and explain how many times it is created
when three tests in the same module use it.

<details>
<summary>Answer / solution (click to reveal)</summary>

``` python
import pytest

@pytest.fixture(scope="module")
def shared_data():
    print("Creating module data")
    return {"environment": "test"}

def test_environment(shared_data):
    assert shared_data["environment"] == "test"

def test_environment_again(shared_data):
    assert shared_data["environment"] == "test"

def test_environment_third_time(shared_data):
    assert shared_data["environment"] == "test"
```

**Expected explanation:** The fixture is created once for that test
module and reused by the three tests, assuming they execute in the same
test session and no other fixture behavior changes its lifetime.

</details>

## Exercise 11: Use `skip` and `xfail`

**What to ask**

Show how to skip a test and how to mark a test as an expected failure.

<details>
<summary>Answer / solution (click to reveal)</summary>

``` python
import pytest

@pytest.mark.skip(reason="Not implemented yet")
def test_future_feature():
    assert True

@pytest.mark.xfail(reason="Known defect")
def test_known_defect():
    assert 1 == 2
```

</details>

## Exercise 12: Generate an HTML report

**What to ask**

Explain how to install the HTML reporting plugin and generate a report.

**Expected commands**

``` bash
pip install pytest-html
pytest --html=report.html --self-contained-html
```

## Exercise 13: Identify the slowest tests

**What to ask**

How would you display the five slowest tests?

**Expected command**

``` bash
pytest --durations=5
```

------------------------------------------------------------------------

# Quick Reference: Common Pytest Commands

  -----------------------------------------------------------------------------------------------
  Goal                                Command
  ----------------------------------- -----------------------------------------------------------
  Run all tests                       `pytest`

  Run a folder                        `pytest tests/`

  Run one file                        `pytest tests/test_login.py`

  Run one test function               `pytest tests/test_login.py::test_login`

  Run one class method                `pytest tests/test_login.py::TestLogin::test_valid_login`

  Run tests matching a keyword        `pytest -k "login"`

  Run a marker group                  `pytest -m smoke`

  Verbose output                      `pytest -v`

  Show print output                   `pytest -s`

  Stop after first failure            `pytest -x`

  Stop after two failures             `pytest --maxfail=2`

  Show five slowest tests             `pytest --durations=5`

  Generate HTML report                `pytest --html=report.html --self-contained-html`
  -----------------------------------------------------------------------------------------------

# Suggested Beginner Interview Evaluation

Use this as a lightweight scoring guide. Adjust the weighting based on
the role and interview duration.

  ------------------------------------------------------------------------
  Area                              Suggested weight What to look for
  --------------------- ---------------------------- ---------------------
  Pytest fundamentals                            20% Discovery,
                                                     organization,
                                                     assertions, execution

  Fixtures and                                   25% Fixture creation,
  `conftest.py`                                      scopes,
                                                     setup/teardown, reuse

  Markers and                                    20% Selection, test data,
  parameterization                                   readable test cases

  Mocking and                                    15% Basic test doubles
  data-driven testing                                and multiple input
                                                     sets

  Practical coding and                           20% Can write, run, and
  debugging                                          explain a small test
  ------------------------------------------------------------------------

## Interviewer tips

-   Ask the candidate to explain their approach while coding.
-   Give a small hint if they get stuck; evaluate how they use it.
-   Ask what happens when the assertion fails or the fixture is reused.
-   Prefer a correct, understandable solution over memorized
    terminology.
-   For beginners, focus on fundamentals rather than obscure plugin
    options.
-   In UI automation interviews, connect Pytest questions to browser
    setup, test data, cleanup, and reporting---but assess
    Playwright-specific skills separately.

## Version and environment note

The examples use standard, commonly available Pytest features and
Python's standard-library `unittest.mock`. Install Pytest with
`pip install pytest`. Plugin examples require their respective packages.
Exact command output and plugin report contents can vary by installed
version.

---

<a id="scenario-based-questions"></a>

# Scenario-Based Pytest Interview Questions

These scenarios focus on Pytest framework concepts. They are not specific to Playwright or Cypress. They are intended to assess whether a beginner can apply Pytest concepts in practical situations.

## 1. Test Execution and Assertions

### Scenario 1: One test fails, but the remaining tests should continue

**Question:** You have 20 test cases in a test file. One test case fails, but you want the remaining test cases to continue executing. How would you handle this in Pytest?

<details>
<summary>Answer / solution (click to reveal)</summary>

Pytest continues executing other tests by default. It marks the failing test as failed and proceeds with the remaining tests. Avoid options such as `-x` when you want the full suite to continue.

</details>

### Scenario 2: Validate multiple outcomes in one test

**Question:** You have a test case that validates login functionality. You need to verify the page title, username, and login status. How would you write assertions for all three validations?

<details>
<summary>Answer / solution (click to reveal)</summary>

```python
def test_login():
    page_title = "Dashboard"
    username = "admin"
    login_status = True

    assert page_title == "Dashboard"
    assert username == "admin"
    assert login_status is True
```

**Expected answer:** Use separate assertions for each expected outcome. If an assertion fails, execution of that test function stops at that assertion; other tests still run by default.

</details>

### Scenario 3: Run only login-related tests

**Question:** You have 100 test cases, but you want to execute only the login-related test cases. How would you achieve this?

<details>
<summary>Answer / solution (click to reveal)</summary>

Use the `-k` option to select tests whose names or collected keywords match an expression.

```bash
pytest -k "login"
```

</details>

## 2. Fixtures and Fixture Scopes

### Scenario 4: Reuse login setup across tests

**Question:** You have five test cases that require a login operation before execution. Would you write the login code in every test case or use a fixture? Explain your approach.

<details>
<summary>Answer / solution (click to reveal)</summary>

```python
import pytest

@pytest.fixture
def login():
    print("Performing login")
    return True

def test_profile(login):
    assert login is True

def test_dashboard(login):
    assert login is True
```

**Expected answer:** Use a fixture to centralize reusable setup and avoid duplication. In a real UI test, the fixture could perform the login steps and yield or return the required page or authenticated state.

</details>

### Scenario 5: Share a database connection within a module

**Question:** You have 10 test cases in a module, and all of them need the same database connection. You don't want to create a new connection for every test. Which fixture scope would you use?

<details>
<summary>Answer / solution (click to reveal)</summary>

```python
import pytest

@pytest.fixture(scope="module")
def database_connection():
    print("Connecting to database")
    connection = "DB Connection"

    yield connection

    print("Closing database connection")
```

**Expected answer:** Use `scope="module"` if sharing one connection across tests in that module is safe. The fixture is created once for the module and its teardown runs after the module's tests finish. Ensure tests do not interfere with one another through shared connection state.

</details>

### Scenario 6: Run setup and cleanup around every test

**Question:** You need to execute setup code before every test and cleanup code after every test. How would you implement this using fixtures?

<details>
<summary>Answer / solution (click to reveal)</summary>

```python
import pytest

@pytest.fixture
def setup():
    print("Before test")
    yield
    print("After test")
```

**Expected answer:** Use a function-scoped fixture with `yield`. Code before `yield` is setup; code after it is teardown.

</details>

### Scenario 7: Share a fixture across test files

**Question:** You have a fixture defined in `test_login.py`, but now you want to reuse it in `test_profile.py` and `test_dashboard.py`. What would you do?

<details>
<summary>Answer / solution (click to reveal)</summary>

Move the fixture into a `conftest.py` file in a parent directory that contains or is an ancestor of all the test files. Pytest discovers the fixture automatically; tests do not need to import it.

</details>

## 3. Parameterization and Data-Driven Testing

### Scenario 8: Test login with multiple credential combinations

**Question:** You need to test a login page with five different username and password combinations. Would you create five separate test cases? How would you simplify this?

<details>
<summary>Answer / solution (click to reveal)</summary>

```python
import pytest

@pytest.mark.parametrize(
    "username, password",
    [
        ("admin", "admin123"),
        ("user1", "pass123"),
        ("user2", "pass456"),
        ("invalid", "wrong"),
        ("", ""),
    ],
)
def test_login_inputs_are_provided(username, password):
    # Illustrative input validation only; this does not perform a real login.
    assert bool(username) and bool(password)
```

**Expected answer:** Use `@pytest.mark.parametrize` to run the same test logic with multiple data sets. A real login test should call the application's login functionality and assert the actual success or error result, rather than merely checking whether the input strings are non-empty.

</details>

### Scenario 9: Run tests across Chrome and Firefox configurations

**Question:** You have multiple test functions that need to run against Chrome and Firefox. How would you avoid duplicating the browser setup?

<details>
<summary>Answer / solution (click to reveal)</summary>

```python
import pytest

@pytest.fixture(params=["chrome", "firefox"])
def browser_name(request):
    print(f"Preparing {request.param}")
    return request.param

def test_homepage(browser_name):
    assert browser_name in ["chrome", "firefox"]

def test_login(browser_name):
    assert browser_name in ["chrome", "firefox"]
```

**Expected answer:** Use a parameterized fixture so each test that requests it runs for each configured browser value. In a real automation project, the fixture would launch and close the corresponding browser.

</details>

## 4. Markers and Test Selection

### Scenario 10: Separate smoke and regression tests

**Question:** Your project has 50 test cases. You want to execute 10 smoke tests during every build and all 50 tests during regression. How would you organize this?

<details>
<summary>Answer / solution (click to reveal)</summary>

```python
import pytest

@pytest.mark.smoke
def test_login():
    assert True

@pytest.mark.regression
def test_order_history():
    assert "order" in "order history"
```

Register the markers in `pytest.ini`:

```ini
[pytest]
markers =
    smoke: critical quick checks
    regression: broader regression checks
```

Run the groups:

```bash
pytest -m smoke
pytest -m regression
```

**Expected answer:** Apply custom markers to categorize tests, register them in the Pytest configuration, and use `-m` to select a group. To run all regression tests, ensure every test intended for that suite has the regression marker (or use an appropriate marker expression/organization).

</details>

### Scenario 11: Temporarily exclude an unfinished test

**Question:** A particular test case is temporarily failing because a feature is not yet implemented. You don't want it to affect the test execution results. What would you do?

<details>
<summary>Answer / solution (click to reveal)</summary>

```python
import pytest

@pytest.mark.skip(reason="Feature not implemented")
def test_new_feature():
    assert True
```

**Expected answer:** Use `skip` when the test should not run. Use `xfail` when the test should run but is expected to fail because of a known defect. The choice depends on whether running the test is useful at this stage.

</details>

## 5. Mocking

### Scenario 12: Avoid making a real payment during a test

**Question:** Your test case calls an external payment API. You don't want to make an actual payment every time you execute the test. How would you handle this?

<details>
<summary>Answer / solution (click to reveal)</summary>

```python
from unittest.mock import Mock

def test_payment():
    payment_api = Mock()
    payment_api.process_payment.return_value = "Success"

    result = payment_api.process_payment(100)

    assert result == "Success"
    payment_api.process_payment.assert_called_once_with(100)
```

**Expected answer:** Replace the external payment dependency with a mock that returns a controlled response. Verify both the result and the expected interaction. In application tests, patch the dependency where the code under test looks it up.

</details>

### Scenario 13: Prevent real emails from being sent

**Question:** Your application sends an email after successful registration. During automation testing, you don't want actual emails to be sent. What approach would you use?

<details>
<summary>Answer / solution (click to reveal)</summary>

Mock the email-sending function or service. Configure the mock as needed and verify it was called with the expected recipient and message. This keeps the test independent of the real email service.

</details>

## 6. Debugging and Reporting

### Scenario 14: Find the slowest tests

**Question:** Your Pytest execution is taking 15 minutes. You want to identify the slowest five test cases. How would you do this?

<details>
<summary>Answer / solution (click to reveal)</summary>

Use Pytest's duration reporting:

```bash
pytest --durations=5
```

This reports the five slowest test durations. It does not by itself explain why a test is slow; further profiling may be needed.

</details>

### Scenario 15: Share execution results as an HTML report

**Question:** Your test cases pass locally, but you want to share the execution results with your team in HTML format. How would you achieve this?

<details>
<summary>Answer / solution (click to reveal)</summary>

Install the `pytest-html` plugin and generate a report:

```bash
pip install pytest-html
pytest --html=report.html --self-contained-html
```

</details>

### Scenario 16: Resolve an unknown custom marker warning

**Question:** You are getting an error or warning that a custom marker is unknown. How would you resolve it?

<details>
<summary>Answer / solution (click to reveal)</summary>

Register the marker in the Pytest configuration file, for example:

```ini
[pytest]
markers =
    smoke: smoke test cases
    regression: regression test cases
```

Use the exact marker spelling in both the test code and configuration.

</details>

## 7. Additional Practical Scenarios

### Scenario 17: One fixture depends on another fixture

**Question:** A test requires two fixtures: one to create a user and another to authenticate that user. How would you manage fixture dependencies?

<details>
<summary>Answer / solution (click to reveal)</summary>

```python
import pytest

@pytest.fixture
def user():
    return {"username": "admin"}

@pytest.fixture
def authenticated_user(user):
    return {
        "username": user["username"],
        "authenticated": True,
    }

def test_dashboard(authenticated_user):
    assert authenticated_user["authenticated"] is True
```

**Expected answer:** A fixture can request another fixture by including its name as a function argument. Pytest resolves the dependency and provides the required value.

</details>

### Scenario 18: Always clean up a temporary file

**Question:** You have a test that creates a temporary file. If the test fails, the temporary file should still be deleted. How would you implement this?

<details>
<summary>Answer / solution (click to reveal)</summary>

```python
import pytest

@pytest.fixture
def temp_file(tmp_path):
    file_path = tmp_path / "test.txt"
    file_path.write_text("Test data")

    yield file_path

    if file_path.exists():
        file_path.unlink()

def test_file_content(temp_file):
    assert temp_file.read_text() == "Test data"
```

**Expected answer:** Put cleanup after `yield` in a fixture. Pytest runs fixture teardown even if the test fails after the fixture has yielded. The built-in `tmp_path` fixture also provides a temporary directory that Pytest manages and removes according to its retention settings, so explicit deletion is not always necessary in this example.

</details>

### Scenario 19: A test passes alone but fails in the full suite

**Question:** You have a test that passes when executed individually but fails when the entire test suite is executed. What could be the reason?

<details>
<summary>Answer / solution (click to reveal)</summary>

Possible causes include:
- Shared test data or application state modified by another test.
- An overly broad fixture scope or mutable shared fixture data.
- Tests depending on execution order.
- Incomplete cleanup or teardown.
- External services, timing, or environment differences.

A good solution is to make tests independent, isolate their data, use suitable fixture scopes, and ensure reliable cleanup. Avoid relying on test execution order.

</details>

### Scenario 20: Reuse test data across files

**Question:** You have 100 test cases, and some tests depend on the same test data. How would you avoid maintaining duplicate data in every test file?

<details>
<summary>Answer / solution (click to reveal)</summary>

Put reusable setup/data fixtures in an appropriately located `conftest.py`, use parameterization for multiple input sets, or store larger data sets in JSON or CSV files and load them through a helper or fixture. Choose the approach that keeps the data easy to maintain and the tests easy to understand.

---

</details>

## Suggested Scenario-Based Interview Selection

For a beginner-level interview, select around 8–10 scenarios rather than asking all 20. A balanced selection could include:

| Area | Suggested number |
|---|---:|
| Assertions and test execution | 2 |
| Fixtures and scopes | 2 |
| Parameterization | 1–2 |
| Markers | 1 |
| Mocking | 1 |
| Debugging/reporting | 1 |
| Test independence and cleanup | 1 |

**Interviewer tip:** Ask candidates to explain their reasoning while coding. Give a small hint if needed and assess whether they can apply it. For beginners, prioritize clear fundamentals and test independence over memorizing advanced plugin options.


---

# Question-by-Question Difficulty Classification

The earlier guide contained beginner and intermediate material, but did not label every question individually. This section classifies all 58 conceptual questions and all 20 scenario questions so an interviewer can select questions consistently.

**Meaning of the labels**
- **Beginner:** A candidate should be able to explain the concept or write a straightforward example.
- **Intermediate:** A candidate should be able to apply the concept, explain trade-offs, or troubleshoot a realistic issue.
- **Advanced basics:** A useful stretch question for a beginner interview; it should not normally be a pass/fail requirement for an entry-level candidate.

## Conceptual questions

| Question | Topic (short form) | Level |
|---:|---|---|
| 1 | What is Pytest and why use it? | Beginner |
| 2 | Pytest advantages over `unittest` | Beginner |
| 3 | Test discovery | Beginner |
| 4 | Naming conventions | Beginner |
| 5 | How discovery works | Beginner |
| 6 | File, class and method naming | Beginner |
| 7 | Organizing a Pytest project | Beginner |
| 8 | Test functions vs classes | Beginner |
| 9 | Tests in classes without inheritance | Beginner |
| 10 | Purpose of assertions | Beginner |
| 11 | Comparing actual and expected results | Beginner |
| 12 | What happens when an assertion fails? | Beginner |
| 13 | Multiple assertions in a test | Beginner |
| 14 | Built-in vs custom assertions | Intermediate |
| 15 | Pytest markers | Beginner |
| 16 | Smoke and regression markers | Beginner |
| 17 | `skip` and `skipif` | Beginner |
| 18 | `skip` vs `xfail` | Intermediate |
| 19 | Selecting tests by marker | Beginner |
| 20 | Running all tests | Beginner |
| 21 | Running one file | Beginner |
| 22 | Running one test function | Beginner |
| 23 | Running one class method | Beginner |
| 24 | Running tests by marker | Beginner |
| 25 | `-v`, `-s` and `-k` options | Beginner |
| 26 | What is a fixture? | Beginner |
| 27 | Creating and using a fixture | Beginner |
| 28 | `@pytest.fixture` | Beginner |
| 29 | Fixture scopes | Intermediate |
| 30 | Comparing fixture scopes | Intermediate |
| 31 | Default fixture scope | Beginner |
| 32 | Using multiple fixtures | Beginner |
| 33 | `autouse=True` | Intermediate |
| 34 | `yield` for teardown | Beginner |
| 35 | Parameterization | Beginner |
| 36 | Multiple data sets in one test | Beginner |
| 37 | `@pytest.mark.parametrize` | Beginner |
| 38 | Passing multiple parameters | Beginner |
| 39 | Combining fixtures and parameterization | Intermediate |
| 40 | Test vs fixture parameterization | Intermediate |
| 41 | What is `conftest.py`? | Beginner |
| 42 | Why use `conftest.py`? | Beginner |
| 43 | Sharing fixtures across files | Beginner |
| 44 | Multiple fixtures in `conftest.py` | Beginner |
| 45 | Multiple `conftest.py` files | Intermediate |
| 46 | Mocking and why use it? | Intermediate |
| 47 | `Mock` vs `MagicMock` | Intermediate |
| 48 | Mocking scenarios | Intermediate |
| 49 | Mocking API/external dependencies | Intermediate |
| 50 | Data-driven testing | Beginner |
| 51 | Implementing data-driven tests | Beginner |
| 52 | Data-driven testing vs parameterization | Intermediate |
| 53 | Login test with multiple data sets | Beginner |
| 54 | Generating an HTML report | Beginner |
| 55 | Information in a test report | Beginner |
| 56 | Performance profiling | Intermediate |
| 57 | Finding slow tests | Intermediate |
| 58 | Reporting/profiling plugins | Intermediate |

## Scenario-based questions

| Scenario | Topic (short form) | Level |
|---:|---|---|
| 1 | Continue after one test fails | Beginner |
| 2 | Multiple assertions for login | Beginner |
| 3 | Run only login-related tests | Beginner |
| 4 | Reuse login setup with a fixture | Beginner |
| 5 | Share a database connection | Intermediate |
| 6 | Setup and teardown with `yield` | Beginner |
| 7 | Share fixtures using `conftest.py` | Beginner |
| 8 | Login testing with multiple data sets | Beginner |
| 9 | Run tests against multiple browsers via fixture parameters | Intermediate |
| 10 | Smoke and regression execution | Beginner |
| 11 | Temporarily skip a test / expected failure | Beginner |
| 12 | Mock a payment API | Intermediate |
| 13 | Mock email sending | Intermediate |
| 14 | Identify the slowest tests | Beginner |
| 15 | Generate an HTML report | Beginner |
| 16 | Fix an unknown-marker warning | Beginner |
| 17 | Fixture depends on another fixture | Intermediate |
| 18 | Always clean up a temporary file | Intermediate |
| 19 | Test passes alone but fails in the suite | Intermediate |
| 20 | Reuse test data across files | Intermediate |

## Suggested selection by candidate experience

- **New to Pytest:** Focus on Beginner questions and ask the candidate to code a basic test, fixture, and parameterized test.
- **Some hands-on practice:** Mix Beginner and Intermediate questions; include fixture scope, `conftest.py`, mocking, and test-isolation scenarios.
- **Do not over-penalize beginners:** Mocking internals, package-level fixture scope, profiling tools, and complex fixture lifetimes are stretch topics rather than essential entry-level requirements.

