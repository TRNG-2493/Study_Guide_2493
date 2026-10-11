# PyTest API Test Structure

## Learning Objectives

By the end of this lesson you will be able to:

- Explain what PyTest is, why teams choose it over a plain script or `unittest`, and what happens in each phase of a test run (collection, execution, reporting).
- Lay out an API test project with `tests/`, `utils/`, `conftest.py`, `pytest.ini`, and `requirements.txt`, and justify the purpose of every file.
- Apply PyTest's discovery rules (file, function, class, and method names) and diagnose "my test did not run" problems.
- Choose between plain test functions and test classes, and know which class pitfalls to avoid.
- Write every API test in the **Arrange-Act-Assert (AAA)** pattern and explain what belongs in each phase.
- Use plain `assert` statements, read PyTest's assertion introspection output, and write failure messages that explain themselves.
- Register and use markers (`smoke`, `regression`, `slow`) and the built-in `skip`, `skipif`, and `xfail` markers, including `strict` mode.
- Run subsets of the suite with `-k`, `-m`, node IDs, `-x`, `--maxfail`, `-v`, `-q`, `-s`, `-rA`, `--tb`, `--lf`, and `--collect-only`, and predict what each command prints.
- Centralise the base URL and timeout in one config module and build a small reusable `ApiClient` helper.
- Keep tests independent (no shared state, no required order) and name tests so that a failure is readable in a one-line summary.

---

## Why This Matters

This week's epic is to turn a handful of API checks into a **pipeline-ready API test framework** for Project 2. On Monday you learned to read HTTP messages, status codes, and headers by hand, using `curl` and Postman. Those are excellent tools for exploring an API, but they do not scale. Nobody wants to click through 300 Postman requests before every release, and a CI server cannot click at all. The skill you are starting today is turning your manual knowledge into code that runs by itself, every time, in any environment.

A script that sends requests and prints results is not a test suite. A **test suite** has structure. Each test is independent, clearly named, discovered automatically, and reports a pass or a fail without a human reading output. That structure is what allows 500 tests to run in a pipeline on Friday and answer one question in one line: is it safe to release?

Structure also decides how painful your life will be in the weeks after this one. Teams that start with a tangle of copy-pasted scripts spend months untangling them. Teams that start with a clean layout (one place for the base URL, one place for the HTTP helper, one naming convention, markers to select fast versus slow tests) can add hundreds of tests without the project becoming unreadable. The folder you design in this lesson is the skeleton for everything else this week:

- Later today you will add the `requests` library details, status-code and JSON checks, authentication, and fixtures and parametrization. Each of those lessons plugs into the layout you build here.
- Wednesday's data-driven, mocking, and schema-validation work will add new test files and helper modules to this same project.
- Thursday's accessibility testing and Friday's CI/CD pipeline will *run* this suite. Friday's pipeline will call a command such as `pytest -m smoke` that you will understand completely by the end of today.

Everything in this lesson uses **JSONPlaceholder** (`https://jsonplaceholder.typicode.com`), a free, public practice API. It is a "fake" API: it accepts your `POST`, `PUT`, and `DELETE` requests and answers realistically, but it does not actually save anything, so you cannot break it and everyone sees the same data.

> **A note on verification.** Every code snippet and every command in this lesson was run against a local stand-in server that imitates JSONPlaceholder's routes (`/posts`, `/posts/1`, `/users/1`, and so on), because the course build environment cannot reach external hosts. The PyTest output shown below is real output from those runs, and the code is identical to what you will run against the real API. Exact timings, file paths, and object memory addresses will differ on your machine. Where an output is what you would see from a real internet call, it is labelled **representative**.

---

## The Concept

### 1. What Is PyTest and Why Do We Use It?

PyTest is a Python framework for writing, finding, running, and reporting on tests. It is an open-source project, it is the most widely used Python test framework, and it is the framework behind most Python QA job descriptions you will see.

To appreciate what it gives you, imagine the alternative. Suppose you write this script:

```python
import requests

r = requests.get("https://jsonplaceholder.typicode.com/posts/1", timeout=10)
print(r.status_code)
```

You run it and see `200`. Is that a pass? You have to remember that `200` means pass. If you have 200 such scripts, you have to read 200 numbers. If one of them crashes halfway, the rest do not run. There is no summary, no way to run only the important ones, no exit code a CI server can read. A framework solves all of this.

PyTest provides:

- **Automatic discovery.** You do not list your tests anywhere. You follow naming rules and PyTest finds them.
- **A pass/fail verdict per test** and a summary at the end, plus an **exit code** (0 means everything passed, non-zero means something failed). The exit code is what a CI pipeline uses to decide whether to continue.
- **Plain `assert` statements** with detailed failure explanations (covered in section 8).
- **Isolation.** One failing test does not stop the others (unless you ask it to).
- **Markers** to label tests and select subsets.
- **Fixtures and parametrization** for sharing set-up code and running one test with many inputs (a separate lesson later today).
- **Plugins** for reports, parallel execution, coverage, and more (Friday).

PyTest versus Python's built-in `unittest`: `unittest` also works and you will see it in older projects, but it requires every test to live inside a class that inherits from `unittest.TestCase`, and it uses special methods such as `self.assertEqual(a, b)`. PyTest lets you write a plain function and a plain `assert a == b`. Less ceremony means tests that are faster to write and easier for a beginner to read.

#### Installing PyTest

Create an isolated environment first. A **virtual environment** is a private copy of Python's package folder for one project, so that this project's libraries do not clash with those of another project.

```bash
python -m venv .venv
source .venv/bin/activate        # macOS / Linux
.venv\Scripts\activate           # Windows (PowerShell or cmd)
pip install pytest requests
pip freeze > requirements.txt
pytest --version
```

Line by line:

- `python -m venv .venv` asks Python to create a virtual environment in a folder named `.venv` inside your project.
- `source .venv/bin/activate` (or the Windows equivalent) *activates* it. Your terminal prompt usually gains a `(.venv)` prefix. From now on `pip` and `python` refer to this private copy.
- `pip install pytest requests` downloads and installs PyTest and the `requests` HTTP library into the environment. (How to use `requests` in depth is the subject of its own lesson today; here we only use its basics.)
- `pip freeze > requirements.txt` writes the exact installed package versions into a file so teammates and the CI server can install the same versions with `pip install -r requirements.txt`.
- `pytest --version` confirms the install. Representative output: `pytest 9.1.1` (your version number may differ).

**Should you commit `.venv`?** Never. Add `.venv/` to `.gitignore`. Commit `requirements.txt` instead.

---

### 2. A First API Test, and What Actually Happens When You Run It

Create a file named `test_first.py`:

```python
import requests

BASE_URL = "https://jsonplaceholder.typicode.com"


def test_get_post_returns_200():
    response = requests.get(f"{BASE_URL}/posts/1", timeout=10)
    assert response.status_code == 200
```

Line by line:

- `import requests` loads the HTTP library.
- `BASE_URL = "..."` stores the root address of the API in a constant. (Section 7 will improve on where this lives.)
- `def test_get_post_returns_200():` defines a function whose name starts with `test_`. That prefix is the signal that tells PyTest "this is a test".
- `requests.get(..., timeout=10)` sends an HTTP `GET` to `https://jsonplaceholder.typicode.com/posts/1` and waits at most 10 seconds. A **timeout** is a time limit; without one, a hung server can freeze your test run forever.
- `assert response.status_code == 200` states the expectation. If the status code is `200`, nothing happens and the test passes. If it is anything else, Python raises an `AssertionError`, and PyTest marks the test as failed.

Run it:

```bash
pytest
```

Representative output (against the real API; the time will vary):

```text
============================= test session starts ==============================
platform linux -- Python 3.13.16, pytest-9.1.1, pluggy-1.6.0
rootdir: /home/you/qea-api-tests
collected 1 item

test_first.py .                                                          [100%]

============================== 1 passed in 0.41s ===============================
```

Reading the output: `rootdir` is the folder PyTest treats as the project root. `collected 1 item` means one test was discovered. The line `test_first.py .` lists the file followed by one character per test: `.` for pass, `F` for fail, `E` for error, `s` for skipped, `x` for expected failure, `X` for unexpectedly passed. `[100%]` is progress. The last line is the verdict.

#### The three phases of a run

Knowing the phases helps you debug.

1. **Collection.** PyTest walks the folders, imports each matching file, and builds a list of tests ("items"). Import errors in a file show up here as `ERROR collecting ...`. Nothing is run yet.
2. **Execution.** PyTest runs each collected test, one by one, recording pass, fail, error, or skip.
3. **Reporting.** PyTest prints failures with details, the short summary, and the totals, then exits with a code.

A test **fails** when an assertion is false. A test has an **error** when something goes wrong outside the test body, typically while setting up a fixture. The difference matters when you read a report: a failure says "the API (or your expectation) is wrong", an error says "the test could not even start properly".

---

### 3. Project Layout: Where Everything Lives

A single file is fine for a first test. A real framework needs a layout. Here is the one we will build and use for the rest of the lesson, and which we recommend for Project 2:

```text
qea-api-tests/
├── pytest.ini                 # PyTest configuration (markers, defaults)
├── requirements.txt           # pinned dependencies
├── .gitignore                 # ignores .venv/, __pycache__/, .pytest_cache/
├── conftest.py                # shared fixtures, visible to every test below it
├── utils/
│   ├── __init__.py            # makes utils a Python package (can be empty)
│   ├── config.py              # base URL, timeout, one place to change them
│   └── api_client.py          # a small helper class that wraps requests
└── tests/
    ├── test_posts_smoke.py    # fast "is it alive?" checks
    ├── test_posts_crud.py     # create / read / update / delete checks
    ├── test_users.py          # tests about the /users resource
    ├── test_independent.py    # tests that build their own data
    └── test_markers_demo.py   # examples of skip and xfail
```

Why is it organised this way? Think of a well-run kitchen. Ingredients (config) are in one pantry, tools (the client helper) are on one rack, and recipes (tests) are in a recipe book organised by dish. If you keep the salt in six different cupboards, nobody can find it and everyone buys more.

| Item | Purpose | What goes wrong without it |
|------|---------|----------------------------|
| `tests/` | Holds only test files. | Tests mixed with helpers; discovery confusion; hard to run "all tests". |
| `utils/` (some teams call it `helpers/`, `clients/`, or `api/`) | Reusable non-test code: config and the API client. | The same `requests.get(f"{BASE_URL}...", timeout=10)` copy-pasted in every test. When the URL changes you edit 200 places. |
| `conftest.py` | Special PyTest file. Shared fixtures and hooks, picked up automatically. | Every test file re-creates the client itself. |
| `pytest.ini` | Project-wide PyTest settings: registered markers, default options, where tests live. | Every developer remembers different command-line flags. CI and laptops behave differently. |
| `requirements.txt` | Dependency list. | "It works on my machine." |
| `__init__.py` in `utils/` | Marks `utils` as an importable package. | `from utils.api_client import ApiClient` may fail on some Python setups. |

#### The special role of `conftest.py`

`conftest.py` is not imported by you. PyTest finds it by itself and makes whatever it defines available to every test in the same folder and all folders below it. That is why it is the traditional home of shared **fixtures**: reusable set-up objects such as an API client. Fixtures have their own lesson later today, so for now just remember the effect: *if a fixture is defined in `conftest.py`, any test can request it by naming it as a parameter.* A `conftest.py` in the project root serves the whole suite. You may add a second `conftest.py` inside `tests/admin/` to hold things only the admin tests need.

#### `pytest.ini` versus `pyproject.toml` versus others

PyTest looks for configuration in this order: `pytest.ini`, `pyproject.toml` (in a `[tool.pytest.ini_options]` table), `tox.ini`, and `setup.cfg`. The first one it finds that has PyTest settings wins. Use `pytest.ini` when you want a dedicated, obvious file (our choice for this course, because it is the simplest to read). Use `pyproject.toml` if your project already has one for packaging or formatting tools. The same kind of settings in `pyproject.toml` look like this:

```toml
[tool.pytest.ini_options]
testpaths = ["tests"]
markers = [
    "smoke: fast checks that prove the API is alive",
]
```

Our `pytest.ini`:

```ini
[pytest]
testpaths = tests
pythonpath = .
addopts = -ra --strict-markers
markers =
    smoke: fast checks that prove the API is alive and basically correct
    regression: broader checks run before a release
    slow: tests that take more than a couple of seconds
```

Line by line:

- `[pytest]` is the section header that PyTest looks for in an `.ini` file.
- `testpaths = tests` tells PyTest "when I run `pytest` with no arguments, look only inside `tests/`". This stops it from scanning your `.venv` or helper folders.
- `pythonpath = .` adds the project root to Python's import search path. This is what makes `from utils.api_client import ApiClient` work from inside `tests/` and `conftest.py` no matter how you launch PyTest.
- `addopts = -ra --strict-markers` lists command-line options that are added to every run automatically. `-r` means "show an extra summary of results" and `a` means "for all outcomes except passes"; so skipped and xfailed tests are listed with their reasons. `--strict-markers` turns an unknown marker name into an error (section 10 shows why that is valuable).
- `markers =` followed by indented lines **registers** marker names. Each line is `name: description`. Registering tells PyTest these are intentional labels, and the descriptions appear in `pytest --markers`.

#### Do I need `tests/__init__.py`?

Beginners meet this question often. With PyTest's default import mode, test files are imported by their *file name*, and without `__init__.py` files PyTest needs those names to be unique across the whole project. That means `tests/a/test_users.py` and `tests/b/test_users.py` would collide ("import file mismatch" error) unless both folders contain an `__init__.py`. The simplest rule: **use unique test file names**, and add `__init__.py` files only when you deliberately have duplicate names in different folders. Our project uses unique names, so `tests/` has no `__init__.py`.

---

### 4. Discovery Rules: How PyTest Finds Your Tests

PyTest decides what is a test purely by name. You do not register tests. The defaults:

| What | Rule | Example that is collected | Example that is NOT collected |
|------|------|---------------------------|--------------------------------|
| File | `test_*.py` or `*_test.py` | `test_posts.py`, `posts_test.py` | `posts_check.py`, `testposts.py` |
| Function (at module level) | name starts with `test` | `test_get_post` | `check_get_post`, `verify_post` |
| Class | name starts with `Test`, with **no** `__init__` method | `TestCreatePost` | `Checks`, `PostTests` |
| Method (inside a collected class) | name starts with `test` | `test_returns_201` | `helper_make_payload` |

Here is a real run proving it. We created `tests/posts_check.py` and a `tests/test_names.py` containing a function called `verify_post`, a class called `Checks`, a class with an `__init__`, and a valid `test_visible`:

```python
def verify_post():
    assert True

def test_visible():
    assert True

class Checks:
    def test_in_wrong_class(self):
        assert True

class TestWithInit:
    def __init__(self):
        pass
    def test_x(self):
        assert True
```

Running `pytest --collect-only -q` (which lists what PyTest found without running anything) found only `test_visible` from this file, and `posts_check.py` contributed nothing at all. PyTest also printed this warning:

```text
PytestCollectionWarning: cannot collect test class 'TestWithInit' because it has a __init__ constructor
```

This is the most dangerous kind of bug in a test suite: **a test that silently does not run is worse than a test that fails**, because a failure is visible and a missing test looks like success. The suite says "all green" while a whole area of the API is unchecked.

Defences:

1. Run `pytest --collect-only -q` after adding files and confirm the number of tests matches your expectation.
2. Treat warnings as signals. Never ignore `PytestCollectionWarning`.
3. Keep naming consistent so a mistake stands out.
4. Watch the count in the summary line. If it drops from 120 to 95 after a refactor, investigate.

You can customise discovery in `pytest.ini` (for example `python_files = check_*.py`), but the defaults are a convention that every PyTest developer knows. Customising makes your project harder for newcomers, so avoid it unless you have a reason.

---

### 5. Test Functions or Test Classes?

PyTest lets you write both. Here is the same content in each form:

```python
# Style 1: plain functions
def test_create_post_returns_201(api):
    response = api.post("/posts", json={"title": "t", "body": "b", "userId": 1})
    assert response.status_code == 201


# Style 2: a class that groups related tests
class TestCreatePost:
    def test_create_post_returns_201(self, api):
        response = api.post("/posts", json={"title": "t", "body": "b", "userId": 1})
        assert response.status_code == 201

    def test_create_post_echoes_title(self, api):
        response = api.post("/posts", json={"title": "t", "body": "b", "userId": 1})
        assert response.json()["title"] == "t"
```

(The `api` parameter is a fixture from `conftest.py`, introduced in section 13. For now read it as "a ready-to-use API client that PyTest hands to the test".)

What is different in the class version?

- The class name begins with `Test` and it has no `__init__`. It is only a container. PyTest creates a **fresh instance of the class for every test method**, so `self.something = 5` set in one test is *not* visible in the next. This surprises people who expect classes to hold shared state; PyTest deliberately prevents it to keep tests independent.
- Each method takes `self` as the first parameter, as in every Python class. PyTest supplies it. You do not.
- A marker placed on the class applies to every method inside it (section 10).
- The test's identity (its **node ID**) includes the class: `tests/test_posts_crud.py::TestCreatePost::test_create_post_returns_201`.

When to prefer which:

| Use plain functions when | Use a class when |
|--------------------------|------------------|
| The test stands alone. | Several tests belong to one feature and you want them visibly grouped. |
| You want the least code. | You want one marker (`@pytest.mark.regression`) on a whole group. |
| You are a beginner (this is the default recommendation). | You want to run a group by name, as in `pytest -k TestCreatePost`. |

Most real projects use mostly functions and a few classes for grouping. The grouping role is organisational only. Do not use classes to share data between tests (see section 9).

**Common beginner mistakes with classes:** forgetting `self`; naming the class `PostTests` (not collected); adding an `__init__` (not collected, with a warning); and storing state on `self` and expecting the next test to see it.

---

### 6. The Arrange-Act-Assert Pattern

A test that mixes everything together is hard to read. The **Arrange-Act-Assert (AAA)** pattern gives every test the same three-part shape:

1. **Arrange**: prepare everything the test needs: input data, the endpoint, the client, any state that must exist beforehand.
2. **Act**: perform the one action under test: usually exactly one API call.
3. **Assert**: check the outcome: status code, body fields, headers.

Why does this help? Because when a test fails at 2 a.m. in a CI log, a colleague must understand it in seconds. If every test has the same shape, they know where to look. If the "Act" is a single obvious line, they know exactly which request was responsible. Another reason is focus: a test that makes five API calls in the middle and asserts after each one is really five tests glued together, and when it fails you do not know which behaviour broke.

An analogy: a science experiment. *Arrange* is setting up the apparatus. *Act* is pressing the button. *Assert* is reading the result and comparing to your hypothesis. You would not take readings while still setting up the equipment.

Here is our smoke test written with explicit AAA comments:

```python
import pytest


@pytest.mark.smoke
def test_get_single_post_returns_200(api):
    # Arrange
    path = "/posts/1"

    # Act
    response = api.get(path)

    # Assert
    assert response.status_code == 200
```

Line by line:

- `import pytest` makes the `pytest` module available for the marker on the next line.
- `@pytest.mark.smoke` labels this test as a smoke test. (Section 10 explains markers fully.)
- `def test_get_single_post_returns_200(api):` is the test. The name follows the discovery rule and says what is being tested. `api` is the shared client.
- `# Arrange` then `path = "/posts/1"`: the only preparation is choosing which resource to request. Naming it makes the Act line self-explanatory.
- `# Act` then `response = api.get(path)`: the single action under test. One line, one request.
- `# Assert` then `assert response.status_code == 200`: the single expectation.

Now a slightly richer example, where Arrange does real work:

```python
@pytest.mark.regression
def test_create_post_echoes_title(api):
    # Arrange: build the request body
    payload = {"title": "QA lesson", "body": "hello", "userId": 1}

    # Act: send it
    response = api.post("/posts", json=payload)

    # Assert: the API returns what we sent, plus an id
    assert response.status_code == 201
    body = response.json()
    assert body["title"] == payload["title"]
    assert "id" in body
```

Line by line:

- `payload = {...}` is the Arrange phase. It is a plain Python dictionary describing the new post. Building it first, rather than inline in the call, lets us compare against it later without retyping values.
- `api.post("/posts", json=payload)` is the Act. The `json=` argument tells `requests` to convert the dictionary to JSON text and set `Content-Type: application/json` (the header you studied on Monday).
- `assert response.status_code == 201` checks that the API reported "Created", the correct status for a successful `POST` that creates a resource (you studied the 2xx family on Monday; status-code validation gets its own lesson later today).
- `body = response.json()` converts the JSON response text into a Python dictionary. This is a *setup for assertions*, not a second action, so we keep it in the Assert phase.
- `assert body["title"] == payload["title"]` compares the echoed title with what we sent.
- `assert "id" in body` checks that the server assigned an identifier.

Multiple `assert` lines in one test are fine when they all verify the outcome of *one* action. The anti-pattern is multiple Acts.

**What about cleanup?** Some tests create real data that must be removed afterwards. This is sometimes called a fourth phase, *Teardown* or "Cleanup". JSONPlaceholder never saves anything, so you do not need it today. Fixtures are the right tool for set-up and teardown and have their own lesson.

**Common AAA mistakes:**

- Putting the Act inside the Arrange (for example, sending a request in the setup and then another in the Act, so you cannot tell which one the failing assertion refers to).
- Asserting inside a loop of Acts.
- Writing a test with *no* assert. It will "pass" even when the API is on fire, because nothing is checked. A test without assertions is a lie.
- Writing comment headers mechanically with nothing under them. In tiny tests the comments are optional; the *blank lines between the three phases* are what matter.

---

### 7. A Small API Client Helper (and the Shared Base URL)

Imagine the team needs to change the API address from the staging server to the pre-production server. If every test contains `requests.get("https://jsonplaceholder.typicode.com/posts/1", timeout=10)`, you must edit every test and you will miss some. The fix is to keep the base URL in **one** place and to wrap `requests` in a small helper. Two files do it.

**`utils/config.py`**

```python
import os

BASE_URL = os.getenv("API_BASE_URL", "https://jsonplaceholder.typicode.com")
TIMEOUT = float(os.getenv("API_TIMEOUT", "10"))
```

Line by line:

- `import os` loads Python's operating-system module, which gives access to environment variables.
- `os.getenv("API_BASE_URL", "https://...")` reads an **environment variable** named `API_BASE_URL`. An environment variable is a named value that lives outside your code, set in the terminal or by a CI server. If the variable is not set, `getenv` returns the second argument, the default.
- The result is stored in `BASE_URL`. By default the tests hit JSONPlaceholder. Running `API_BASE_URL=https://staging.example.com pytest` (macOS/Linux) points the same tests at staging without touching any code. Friday's pipeline will set such variables for you; today you only need to know the idea.
- `TIMEOUT = float(os.getenv("API_TIMEOUT", "10"))` does the same for the timeout. Environment variables are always text, so `float(...)` converts `"10"` to the number `10.0`. The default value is given as a string `"10"` for the same reason.

Why environment variables? Because configuration should *vary by environment* (laptop, staging, CI) while code stays identical. It is also where secrets such as API keys will eventually live, never in the code (the authentication lesson later today builds on this).

**`utils/api_client.py`**

```python
import requests

from utils.config import BASE_URL, TIMEOUT


class ApiClient:
    """A thin wrapper around requests.Session for one API."""

    def __init__(self, base_url=BASE_URL, timeout=TIMEOUT):
        self.base_url = base_url.rstrip("/")
        self.timeout = timeout
        self.session = requests.Session()
        self.session.headers.update({"Accept": "application/json"})

    def _url(self, path):
        return f"{self.base_url}/{path.lstrip('/')}"

    def request(self, method, path, **kwargs):
        kwargs.setdefault("timeout", self.timeout)
        return self.session.request(method, self._url(path), **kwargs)

    def get(self, path, **kwargs):
        return self.request("GET", path, **kwargs)

    def post(self, path, **kwargs):
        return self.request("POST", path, **kwargs)

    def put(self, path, **kwargs):
        return self.request("PUT", path, **kwargs)

    def delete(self, path, **kwargs):
        return self.request("DELETE", path, **kwargs)

    def close(self):
        self.session.close()
```

Line by line:

- `import requests` and `from utils.config import BASE_URL, TIMEOUT` bring in the HTTP library and our two settings.
- `class ApiClient:` defines a class, a blueprint for objects. The triple-quoted string below is a **docstring**, a description Python tools can display.
- `def __init__(self, base_url=BASE_URL, timeout=TIMEOUT):` is the constructor, the method that runs when you write `ApiClient()`. The default arguments mean `ApiClient()` uses the configured values, while `ApiClient("http://localhost:8000")` overrides them (handy when testing the client itself).
- `self.base_url = base_url.rstrip("/")` stores the address and removes any trailing slash, so `https://x.com/` and `https://x.com` behave the same. This tiny normalisation prevents the classic `https://x.com//posts` double-slash bug.
- `self.session = requests.Session()` creates a **session**: a `requests` object that reuses the underlying network connection and remembers settings such as default headers between calls. Reusing connections makes a big suite noticeably faster.
- `self.session.headers.update({"Accept": "application/json"})` sets a default `Accept` header (Monday's headers lesson: the header that says "I want JSON back") on every request this session sends.
- `def _url(self, path):` builds the full URL. The leading underscore is a Python convention meaning "internal helper; not for outside use". `path.lstrip('/')` removes a leading slash so `"/posts/1"` and `"posts/1"` both work; the f-string then joins base and path with exactly one slash.
- `def request(self, method, path, **kwargs):` is the one method that really sends HTTP. `**kwargs` collects any extra keyword arguments (such as `json=`, `params=`, `headers=`) so they can be passed along untouched.
- `kwargs.setdefault("timeout", self.timeout)` adds a timeout *unless the caller supplied one*. This guarantees that no test can accidentally hang forever, which is the most common reason a CI job runs for hours.
- `return self.session.request(method, self._url(path), **kwargs)` performs the call and returns the `requests` `Response` object unchanged. Returning the raw response is deliberate: tests need access to the status code, headers, and body.
- The `get`, `post`, `put`, and `delete` methods are readable shortcuts that call `request` with the right verb. Tests then say `api.get("/posts/1")`, which reads almost like English.
- `close()` closes the session's connections. It will be called once at the end of the run.

What this client intentionally does **not** do: it does not assert anything and does not hide errors. Assertions belong in tests so that a failing test shows the assertion. A client that "helpfully" raised exceptions on a `404` would make it impossible to write a test that *expects* a `404`.

Authentication headers, logging of requests, and retry logic are natural later additions, and by isolating all HTTP detail here you add them in one file. How the `requests` library itself works (parameters, sessions, response objects) is covered in the requests-library lesson today; this class is built only on its basics.

---

### 8. Plain `assert`, Assertion Rewriting, and Failure Messages

PyTest tests use Python's normal `assert` statement:

```python
assert response.status_code == 200
assert "title" in response.json()
assert len(posts) > 0
assert response.headers["Content-Type"].startswith("application/json")
```

An `assert` evaluates an expression. If it is true, execution continues. If it is false, Python raises `AssertionError`, and PyTest records the failure.

A plain `assert` in ordinary Python only says `AssertionError` with no explanation. PyTest improves this with **assertion rewriting**: when it imports your test files, it quietly rewrites the `assert` statements so that when one fails, PyTest knows the values of every sub-expression and prints them. This is why you do not need `assertEqual` helpers. Here is the real output for a deliberately wrong test:

```python
def test_wrong_status(api):
    response = api.get("/posts/1")
    assert response.status_code == 201
```

```text
    def test_wrong_status(api):
        response = api.get("/posts/1")
>       assert response.status_code == 201
E       assert 200 == 201
E        +  where 200 = <Response [200]>.status_code

tests/test_fail_demo.py:6: AssertionError
```

How to read it: the `>` marks the exact line that failed. Lines starting with `E` are the explanation. `assert 200 == 201` shows the actual value on the left and the expected value on the right. `where 200 = <Response [200]>.status_code` shows where the left value came from. You did not write any of that; PyTest worked it out.

Here is a failing comparison of two dictionaries:

```python
def test_wrong_body(api):
    response = api.get("/posts/1")
    expected = {"id": 1, "userId": 1, "title": "hello"}
    assert response.json() == expected
```

```text
E       AssertionError: assert {'userId': 1,...dy': 'body 1'} == {'id': 1, 'us...tle': 'hello'}
E
E         Omitting 2 identical items, use -vv to show
E         Differing items:
E         {'title': 'title 1'} != {'title': 'hello'}
E         Left contains 1 more item:
E         {'body': 'body 1'}
E         Use -v to get more diff
```

PyTest compared the two dictionaries key by key, told you that two items matched, that `title` differs, and that the actual response has an extra `body` key. Without writing any diff code you can see exactly what is different. If the shortened output hides the detail you need, run with `-vv` for the full comparison.

#### Writing your own failure messages

Everything after a comma in an `assert` is the failure message:

```python
def test_with_message(api):
    response = api.get("/posts/1")
    assert response.status_code == 404, (
        f"GET /posts/1 expected 404 but got {response.status_code}"
    )
```

```text
E       AssertionError: GET /posts/1 expected 404 but got 200
E       assert 200 == 404
E        +  where 200 = <Response [200]>.status_code
```

Line by line: the parentheses allow the message to continue onto the next line. The message is an f-string, so `{response.status_code}` is replaced by the actual value. PyTest prints your message first and its own introspection after it.

When is a custom message worth writing? PyTest's default output is already very good for simple comparisons. Add a message when it supplies information PyTest cannot know: *which* request was made, *why* the expectation exists, or the response body for debugging. A very useful pattern for API tests is to include the response text:

```python
assert response.status_code == 201, f"Unexpected status. Body: {response.text}"
```

A failure in CI then shows what the server actually said (often an error message explaining the real problem) without anyone re-running the test locally.

#### Assertion habits that make tests better

- **One logical expectation per assertion, written directly.** Prefer `assert response.status_code == 200` to `assert response.ok`, because `.ok` is true for *any* status below 400, including `204` or `301`, which may not be what you meant.
- **Do not compare entire large bodies with `==` when you only care about parts.** Assert the fields that matter.
- **Never write `assert True`** or an assert that cannot fail.
- **Do not wrap `assert` in `try/except`** to "keep going"; you will hide failures. If you need to check several things and see all failures at once, write separate tests.
- **Never put the condition and message together in parentheses**, like `assert (cond, "message")`. That asserts a non-empty tuple, which is always true, so the check silently never fails. Write `assert cond, "message"`.

The status-code lesson and the JSON-validation lesson later today go deeper into *what* to assert about an API response. This lesson only covers *how* assertions behave in PyTest.

---

### 9. Test Independence: Why Order Must Not Matter

Each test must be able to run **alone**, in **any order**, and **repeatedly**, and give the same answer. This is called test independence and it is the single most important structural rule after naming.

Why? Because you will constantly run subsets: only the failing test you are debugging, only smoke tests, only tests matching a keyword. In CI, tests may run in parallel or in random order. If test B quietly depends on something test A did, then running B alone fails for reasons that have nothing to do with the API, and you spend an afternoon chasing a ghost.

Here is a real example of the mistake. These two tests share a module-level dictionary:

```python
created = {}

def test_create(api):
    created["id"] = api.post("/posts", json={"title": "t"}).json()["id"]

def test_read_created():
    assert created["id"] == 101
```

Running the whole file works:

```text
..                                                                       [100%]
2 passed in 0.01s
```

But running only the second test, which is exactly what you do when debugging, fails:

```text
>       assert created["id"] == 101
               ^^^^^^^^^^^^^
E       KeyError: 'id'

FAILED tests/test_dependent.py::test_read_created - KeyError: 'id'
1 failed, 1 deselected in 0.02s
```

`test_read_created` is not wrong because of the API; it is wrong because it assumed `test_create` ran before it. The suite is "green" only by luck of file order.

**The fix:** every test arranges what it needs by itself. If a test needs an existing post, it either uses data that always exists (JSONPlaceholder always has posts 1 to 100) or creates one inside its own Arrange phase:

```python
def _create_post(api):
    response = api.post("/posts", json={"title": "t", "body": "b", "userId": 1})
    assert response.status_code == 201
    return response.json()["id"]


def test_create_then_id_is_returned(api):
    assert _create_post(api) == 101
```

Line by line: `_create_post` is a helper function (note the leading underscore and the absence of `test_` in the name, so PyTest does not collect it). It performs the create call, asserts the call succeeded so a failure in set-up is reported clearly, and returns the new id. Any test that needs a post calls it. (Why `101`? JSONPlaceholder always answers a create request with id `101`, which is part of how it fakes persistence. A real API would give a different id each time, and you would use the returned id rather than comparing to a fixed number.)

A checklist for independence:

- No test reads a global variable that another test writes.
- No test requires another test to have run first. PyTest happens to run in file order, but a plugin or a `-k` filter can change that, so never rely on it.
- If your tests create real data in a real API, each test creates its own data with unique values and removes it afterwards (fixtures, later today).
- Tests may *share read-only* things: the client, the base URL, constants.

**Why a shared session client is fine.** Our `api` fixture is created once per run and shared. That is safe only because the client has no per-test state: it does not remember responses between calls. If you ever add a login token to the client, be careful that one test changing the token does not affect the next.

---

### 10. Markers: Labelling Tests

A **marker** is a label you attach to a test with the `@pytest.mark.<name>` decorator. A decorator is a line starting with `@` placed above a function that adds behaviour or metadata to it. Custom markers do not change what a test does; they let you *select* tests by label.

Why do we need them? Because tests differ in purpose and cost:

- **Smoke tests** are a handful of fast, critical checks: is the API up, can I read the main resource? They run after every deployment and answer "is it completely broken?" in seconds.
- **Regression tests** are the broad set that checks previously working behaviour has not been broken. They run before a release or nightly and may take minutes.
- **Slow tests** are tests that take long (large downloads, rate-limit waits) and that you want to exclude from quick runs.

Real-world scenario: a developer fixes a typo in the API and deploys at 4:55 p.m. Friday. Nobody wants to wait twenty minutes. The pipeline runs `pytest -m smoke`, which takes 8 seconds and proves the service is alive and the main read paths work. The full regression suite runs overnight. Markers are the mechanism that makes the same code serve both needs.

#### Registering markers

We registered `smoke`, `regression`, and `slow` in `pytest.ini` above. If you use an unregistered name, PyTest by default only *warns*, and a typo such as `@pytest.mark.smoek` silently creates a new marker that no `-m smoke` command will ever select, so that test never runs in the smoke stage. We prevent this with `--strict-markers` in `addopts`. Here is what happens when a test uses `@pytest.mark.smokee`:

```text
ERROR collecting tests/test_fail_demo.py
'smokee' not found in `markers` configuration option
!!!!!!!!!!!!!!!!!!!! Interrupted: 1 error during collection !!!!!!!!!!!!!!!!!!!!
```

The whole run stops with a clear message. This is exactly what you want: a typo is caught in seconds instead of silently excluding a test for months.

#### Applying markers

On a function:

```python
@pytest.mark.smoke
def test_get_post_list_is_not_empty(api):
    response = api.get("/posts")

    assert response.status_code == 200
    assert len(response.json()) > 0
```

On a class (applies to every test method inside):

```python
@pytest.mark.regression
class TestCreatePost:
    def test_create_post_returns_201(self, api):
        ...
```

On a whole file, by assigning the special variable `pytestmark` at the top of the module:

```python
import pytest

pytestmark = pytest.mark.regression
```

Several markers can be stacked on one test:

```python
@pytest.mark.smoke
@pytest.mark.regression
def test_get_single_post_returns_200(api):
    ...
```

A test that is a smoke test is usually also part of regression. Many teams define it that way so `-m regression` runs everything important, and `-m smoke` picks the fast subset.

Line by line for the first example: `@pytest.mark.smoke` labels the function. The test name follows the discovery rules. The Act `api.get("/posts")` requests the whole collection. The first assert checks the status; the second checks that the list contains something, because a `200` with an empty list would be a defect for this endpoint.

To list the registered markers and their descriptions, run `pytest --markers`. Representative output:

```text
@pytest.mark.smoke: fast checks that prove the API is alive and basically correct

@pytest.mark.regression: broader checks run before a release

@pytest.mark.slow: tests that take more than a couple of seconds
```

(The command also lists PyTest's built-in markers such as `skip`, `skipif`, `xfail`, `parametrize`, and `usefixtures`.)

**Naming markers well.** Choose markers that describe *purpose or cost*, not file names: `smoke`, `regression`, `slow`, `auth`, `negative`. Keep the list short (five to eight) and documented in `pytest.ini`.

---

### 11. Built-in Markers: `skip`, `skipif`, and `xfail`

Sometimes a test should not run, or should be expected to fail. PyTest has three built-in markers for this. They need no registration.

#### `skip`: do not run this test

```python
@pytest.mark.skip(reason="feature not built yet")
def test_pagination_links():
    assert False
```

The test is collected but never executed. The `reason` text appears in the summary (because of `-ra`): `SKIPPED [1] tests/test_markers_demo.py:4: feature not built yet`. When to use: a feature is planned but not available, or a test is temporarily unsuitable. Always give a reason. A skip with no reason becomes a permanent blind spot nobody remembers.

#### `skipif`: skip under a condition

```python
import os

@pytest.mark.skipif(not os.getenv("RUN_SLOW"), reason="set RUN_SLOW=1 to run")
@pytest.mark.slow
def test_slow_thing():
    pass
```

Line by line: `os.getenv("RUN_SLOW")` returns `None` if the environment variable is not set, so `not None` is `True` and the test is skipped. Setting `RUN_SLOW=1` before running `pytest` makes the condition false and the test runs. The condition is evaluated when the module is imported. Typical uses: skip a test that only works on one operating system, or on one environment (for example, tests that need a real database that exists only in staging).

#### `xfail`: expected failure

```python
@pytest.mark.xfail(reason="BUG-123: API returns 200 for empty title", strict=True)
def test_create_post_rejects_empty_title(api):
    response = api.post("/posts", json={"title": "", "body": "x", "userId": 1})
    assert response.status_code == 400
```

This is a **known bug** documented as a test. The test describes correct behaviour (an empty title should be rejected with `400`) but the API currently misbehaves. Marking it `xfail` means:

- While the bug exists, the test fails, but PyTest reports it as `x` (expected failure, `XFAIL`) and the run is **not** red. The suite stays usable, and the bug is not forgotten, because it is listed in every report.
- When developers fix the bug, the test starts passing. With `strict=True`, an unexpected pass is reported as a **failure**, which forces someone to remove the `xfail` marker and turn the test into a normal, protecting regression test. Without `strict`, the pass shows only as `XPASS` and is easy to overlook.

Real output for a strict xfail whose bug has been fixed (the test body simply asserts something true):

```text
F                                                                        [100%]
_________________________________ test_bug_fixed _________________________________
[XPASS(strict)] BUG-1
FAILED tests/test_strict.py::test_bug_fixed - [XPASS(strict)] BUG-1
```

Compare the three markers:

| Marker | Test runs? | Reported as | Use when |
|--------|-----------|-------------|----------|
| `skip` | No | `s` SKIPPED | The test is not applicable now. |
| `skipif` | Only if the condition is false | `s` SKIPPED | It depends on environment or configuration. |
| `xfail` | Yes | `x` XFAIL (or `X` XPASS) | You know a bug exists and want the test to document it. |

**Common mistake:** using `skip` to hide a failing test you cannot be bothered to fix. A skipped test never reports again; an `xfail` test keeps running and tells you when the bug is fixed. For a known bug, prefer `xfail` with a ticket number in the reason.

Our real run of the project, with the demo markers, ended with:

```text
SKIPPED [1] tests/test_markers_demo.py:4: feature not built yet
SKIPPED [1] tests/test_markers_demo.py:15: set RUN_SLOW=1
XFAIL tests/test_markers_demo.py::test_create_post_rejects_empty_title - BUG-123: API returns 200 for empty title
10 passed, 2 skipped, 1 xfailed in 0.04s
```

---

### 12. Running Subsets of Tests

The real power of structure appears at the command line. Run all of these from the project root (the folder containing `pytest.ini`).

#### Everything

```bash
pytest
```

Thanks to `testpaths = tests`, this runs everything under `tests/`.

#### A folder, a file, or a single test (node IDs)

```bash
pytest tests/test_users.py
pytest tests/test_posts_crud.py::TestCreatePost
pytest "tests/test_posts_crud.py::TestCreatePost::test_create_post_returns_201"
```

The text after `::` selects a class and then a method (or just a function in a file). This string is the **node ID**. Failure summaries print node IDs, so you can copy one straight into the command line to re-run exactly that test. Use quotes if your shell would otherwise misinterpret characters.

#### `-v` (verbose) and `-q` (quiet)

`-v` prints one line per test with its full node ID and result:

```bash
pytest -v tests/test_users.py
```

```text
collecting ... collected 2 items

tests/test_users.py::test_get_user_1_returns_200_and_name PASSED         [ 50%]
tests/test_users.py::test_posts_filtered_by_user_belong_to_that_user PASSED [100%]

============================== 2 passed in 0.01s ===============================
```

`-q` (quiet) shrinks the output to dots and a last line. Use `-v` when learning or debugging and `-q` when you only care about the verdict. You can pass `-vv` for even more detail (for example, complete dictionary diffs).

#### `-m`: select by marker

```bash
pytest -m smoke
pytest -m "smoke or regression"
pytest -m "regression and not slow"
pytest -m "not slow"
```

The expression after `-m` is quoted and uses the words `and`, `or`, and `not`, with parentheses allowed. In our project, `pytest -m smoke` selected exactly three tests (`pytest --collect-only -q -m smoke` prints `3/13 tests collected (10 deselected)`):

```text
tests/test_posts_smoke.py::test_get_single_post_returns_200
tests/test_posts_smoke.py::test_get_post_list_is_not_empty
tests/test_users.py::test_get_user_1_returns_200_and_name
```

"Deselected" in the summary means the test was collected but filtered out. It is not an error.

#### `-k`: select by keyword in the name

`-k` matches a substring (case-insensitively) against test names, class names, and file names:

```bash
pytest -k create
pytest -k "create and not echoes"
pytest -k TestCreatePost
pytest -k "wrong and not body" -v
```

The last command, run on our demo, selected one of four tests:

```text
collected 4 items / 3 deselected / 1 selected

tests/test_fail_demo.py::test_wrong_status FAILED                        [100%]
```

When to use which? `-m` is for *planned* categories you decided in advance (smoke, regression). `-k` is for *ad hoc* selection while you work ("run everything about posts") and it relies on your naming being consistent. This is the practical reason test names matter (section 14).

#### Combining filters

Filters combine. `-m regression -k create` runs tests that match both. In our project:

```bash
pytest -m "regression and not slow" -k create -v
```

selected three tests: the two in `TestCreatePost` and `test_create_then_id_is_returned`.

#### `-x` and `--maxfail`: stop early

```bash
pytest -x
pytest --maxfail=2
```

`-x` stops the run after the first failure. `--maxfail=N` stops after N. Use them while developing (no point running 300 tests when the very first reveals the API is down) and in a pipeline stage where a failing smoke test should abort the job. Real output for `-x` on our demo (three failing tests):

```text
FAILED tests/test_fail_demo.py::test_wrong_status - assert 200 == 201
!!!!!!!!!!!!!!!!!!!!!!!!!! stopping after 1 failures !!!!!!!!!!!!!!!!!!!!!!!!!!!
1 failed in 0.02s
```

#### `-s`: show `print` output

By default PyTest **captures** anything your tests print, and shows it only for failing tests. That keeps passing runs clean. When you need to see print output live, for debugging, add `-s` (which means "do not capture"):

```bash
pytest -k test_ok -s -v
```

```text
tests/test_fail_demo.py::test_ok debug: about to call API
PASSED
```

The `debug: ...` text came from a `print()` inside the test, and appeared in the middle of the line because output is not captured. Do not leave `print` statements in committed tests; use assertion messages or logging.

#### `--tb`: control traceback style

A **traceback** is the stack of code lines Python shows when an error occurs. PyTest offers several styles:

| Option | What you get |
|--------|--------------|
| `--tb=auto` | Default. Long form for the first and last failures, short for the others. |
| `--tb=long` | Full detail for every failure. |
| `--tb=short` | Shorter: one line of source per frame. |
| `--tb=line` | One line per failure. |
| `--tb=no` | No tracebacks, only the summary. |

Real `--tb=short` output:

```text
______________________________ test_wrong_status _______________________________
tests/test_fail_demo.py:6: in test_wrong_status
    assert response.status_code == 201
E   assert 200 == 201
E    +  where 200 = <Response [200]>.status_code
```

Use `--tb=short` in CI logs where space matters, and `--tb=no -q` for a quick pass/fail overview.

#### `-r`: choose the extra summary

`-r` followed by letters selects which outcomes appear in the "short test summary info" block: `f` failed, `E` error, `s` skipped, `x` xfailed, `X` xpassed, `p` passed, `a` all except passed, `A` all. We set `-ra` in `addopts`. Running `pytest -rA` also lists every passed test, useful when you want proof that a particular test ran.

#### `--lf` and `--ff`: re-run failures

PyTest remembers failures in a `.pytest_cache` folder. `pytest --lf` ("last failed") runs only the tests that failed last time, and `pytest --ff` ("failed first") runs them first and then the rest. This is a very quick loop when fixing a bug: run everything, then `--lf` repeatedly until green.

#### `--collect-only`: see what would run

```bash
pytest --collect-only -q
```

lists the tests that would run, without running anything. Use it to verify discovery (section 4) and to check what a `-m` or `-k` expression will select before you run a long suite.

#### Other useful options

- `--durations=5` lists the five slowest tests, a good way to find candidates for the `slow` marker.
- `--junitxml=report.xml` writes results in a standard XML format that CI servers read. (Friday's CI/CD lesson uses it; today you only need to know it exists.)
- `-p no:cacheprovider` disables the `.pytest_cache` folder if you do not want it.

Exit codes: PyTest returns `0` when all tests pass, `1` when some fail, `2` if the run was interrupted, `3` for an internal error, `4` for a command-line usage error, and `5` when no tests were collected. A pipeline stops when it sees a non-zero code. Note the last one: a valid marker that matches no tests, for example `pytest -k nonexistent_name`, collects zero tests and exits with `5`, which a CI job treats as failure, a helpful alarm that your selection matched nothing.

---

### 13. Wiring It Together: `conftest.py` and the Shared Client

Now the glue. Our `conftest.py`:

```python
import pytest

from utils.api_client import ApiClient


@pytest.fixture(scope="session")
def api():
    client = ApiClient()
    yield client
    client.close()
```

Line by line:

- `import pytest` and `from utils.api_client import ApiClient` load PyTest and our helper. This import works because `pythonpath = .` in `pytest.ini` put the project root on the import path.
- `@pytest.fixture(scope="session")` declares that the function below is a **fixture**: a function PyTest calls to produce a value that tests can request. `scope="session"` means "create it once for the whole test run, and share it", which saves reconnecting for every test.
- `def api():` the function name becomes the fixture's name. Any test that lists a parameter called `api` receives the value this function yields.
- `client = ApiClient()` builds the helper with default config (the base URL from the environment or JSONPlaceholder).
- `yield client` hands the client to the tests. Everything *before* `yield` is set-up. Everything *after* it is teardown.
- `client.close()` runs once after the final test finished, closing the connections.

You have not yet seen fixtures in depth: scopes, teardown ordering, fixture dependencies, and parametrized fixtures are the subject of the fixtures and parametrization lesson later today. For structure purposes the point is just this: a test that needs an API client writes `def test_something(api):` and PyTest supplies it. No test needs to know the base URL, the timeout, or how connections are made.

Now a complete test module using everything so far, `tests/test_users.py`:

```python
import pytest


@pytest.mark.smoke
def test_get_user_1_returns_200_and_name(api):
    # Arrange
    path = "/users/1"

    # Act
    response = api.get(path)

    # Assert
    assert response.status_code == 200
    assert "name" in response.json()


@pytest.mark.regression
def test_posts_filtered_by_user_belong_to_that_user(api):
    response = api.get("/posts", params={"userId": 1})

    assert response.status_code == 200
    posts = response.json()
    assert len(posts) > 0
    for post in posts:
        assert post["userId"] == 1, f"post {post['id']} belongs to user {post['userId']}"
```

Line by line for the second test:

- `api.get("/posts", params={"userId": 1})`: `params=` makes `requests` append `?userId=1` to the URL, producing `GET /posts?userId=1`. JSONPlaceholder filters posts by author when given that query parameter (query strings were part of Monday's URL anatomy).
- `assert response.status_code == 200` checks the call worked.
- `posts = response.json()` parses the list. The name `posts` makes the loop readable.
- `assert len(posts) > 0` guards against the loop silently doing nothing: an empty list would make the `for` loop pass without checking anything, a classic false pass.
- `for post in posts:` walks every post and `assert post["userId"] == 1, f"..."` checks each one. The custom message names the offending post, so a failure explains itself: the default message would only say `assert 2 == 1`, without telling you which post.

Running the whole project against our stand-in server gave:

```text
collected 13 items
...
10 passed, 2 skipped, 1 xfailed in 0.04s
```

---

### 14. Test Naming Conventions

Test names are documentation that is printed on screen at the exact moment something breaks. Compare these two lines from a failing CI run:

```text
FAILED tests/test_posts.py::test_1
FAILED tests/test_posts.py::test_get_missing_post_returns_404
```

The second tells you what behaviour broke before you open a single file. Good names make failures self-explanatory, make `-k` searches productive, and let a non-programmer read the report.

A reliable pattern: **`test_<action>_<condition>_<expected result>`**, in lower case with underscores (the Python convention for function names).

| Poor name | Better name | Why |
|-----------|-------------|-----|
| `test1` / `test_1` | `test_get_single_post_returns_200` | Says what and what is expected. |
| `test_posts` | `test_get_post_list_is_not_empty` | One behaviour per name. |
| `test_error` | `test_get_missing_post_returns_404` | States the condition and outcome. |
| `test_create` | `test_create_post_echoes_title` | Describes the specific assertion. |
| `testCreatePostWorks` | `test_create_post_returns_201` | Not collected! Must be `test_` with underscore, lower case. |

More conventions:

- **File names:** one file per resource or feature: `test_posts_smoke.py`, `test_posts_crud.py`, `test_users.py`. Not `test_misc.py`, which becomes a junk drawer.
- **Class names:** `Test` plus the feature in CamelCase: `TestCreatePost`.
- **Name length:** long is fine. Nobody types a test name; they read it. A 60-character descriptive name is better than a 15-character cryptic one.
- **If the name needs "and", split the test.** `test_create_post_returns_201_and_echoes_title_and_sets_location` is three tests. (Multiple asserts about *one* response are fine; the point is one behaviour per test.)
- **Negative tests say so:** `test_get_missing_post_returns_404`, `test_create_post_rejects_empty_title`. Monday's status-code families (4xx for client errors) tell you what negative tests exist.
- **Be consistent about verbs.** Choose `returns` or `should_return`, `rejects` or `fails`, and keep it everywhere. Consistency is what makes `pytest -k returns_404` find all your 404 tests.

Docstrings are optional: a good name usually replaces them. When a test needs *why* context (a link to the bug ticket, an unusual precondition), add a one-line docstring or a comment.

---

### 15. Common Mistakes (A Collected List)

| Mistake | Symptom | Fix |
|---------|---------|-----|
| File named `posts_check.py` or function `check_post` | Test never runs, no error | Follow `test_*.py` / `test_*`; check with `--collect-only`. |
| Class with `__init__` | `PytestCollectionWarning`, tests skipped silently | Remove the constructor; use fixtures for set-up. |
| Class not starting with `Test` | Methods not collected | Rename to `TestSomething`. |
| `assert` missing in a test | Always passes | Every test must assert an outcome. |
| Test depends on another test | Passes in a full run, fails alone | Arrange your own data (section 9). |
| Base URL hard-coded in every test | One URL change = many edits | Central config (section 7). |
| No `timeout=` on requests | Run hangs forever on a stuck server | Set it once in the client. |
| Unregistered marker, no `--strict-markers` | Typo marker never selected | Register markers and use `--strict-markers`. |
| `assert (cond, "msg")` | Always passes (tuple) | Write `assert cond, "msg"`. |
| `skip` used for a known bug | Bug disappears from reports | Use `xfail(strict=True)` with a ticket id. |
| Duplicate test file names without `__init__.py` | `import file mismatch` | Unique names or add `__init__.py`. |
| Running `pytest` from the wrong folder | Config not found, imports fail | Run from the project root (where `pytest.ini` is). |
| Everything is slow and nobody knows why | Suite takes forever | Use `--durations`, mark `slow`, keep smoke small. |
| Printing instead of asserting | Run is green but nothing is checked | Print is for debugging, assert is for testing. |

Another subtle mistake is leaving **order-dependent leftovers** after you refactor: a test passes in the full run for months and breaks only when someone runs it alone. Make a habit of running a new test by itself (`pytest path::test_name`) before committing.

---

### 16. Practice Exercises (with Solutions)

Work in the `qea-api-tests` project you built. Try each exercise before opening its solution. If you cannot reach JSONPlaceholder, use any local server that mimics it.

#### Exercise 1: Discovery detective

A teammate adds `tests/comments_test_file.py` and `tests/test_comments.py`:

```python
# tests/test_comments.py
def check_comments_for_post(api):
    response = api.get("/posts/1/comments")
    assert response.status_code == 200

class CommentTests:
    def test_comments_have_email(self, api):
        response = api.get("/posts/1/comments")
        assert all("@" in c["email"] for c in response.json())
```

They report "all green, 100%". Explain what is wrong and fix it so both checks run.

**Solution.** Nothing in the file is collected. `check_comments_for_post` does not start with `test`, and `CommentTests` does not start with `Test` (the class prefix must come first). The other file, `comments_test_file.py`, matches neither `test_*.py` nor `*_test.py`, so PyTest ignores it entirely. Fixing the names:

```python
# tests/test_comments.py
def test_comments_for_post_return_200(api):
    response = api.get("/posts/1/comments")
    assert response.status_code == 200


class TestComments:
    def test_comments_have_email(self, api):
        response = api.get("/posts/1/comments")
        assert all("@" in c["email"] for c in response.json())
```

Verify with `pytest --collect-only -q`: you should see both tests listed. The statement `all("@" in c["email"] for c in ...)` is true only if every comment's `email` contains an `@`. (The empty-list false-pass trap from section 13 applies here too, because `all()` of an empty list is `True`; a stricter test would also assert the list is not empty.)

#### Exercise 2: Write an AAA test

Write a test `test_get_user_1_returns_200_and_name` for `GET /users/1` in the AAA pattern, marked as `smoke`. It must check the status code and that the response has a `name` field.

**Solution.**

```python
import pytest


@pytest.mark.smoke
def test_get_user_1_returns_200_and_name(api):
    # Arrange
    path = "/users/1"

    # Act
    response = api.get(path)

    # Assert
    assert response.status_code == 200
    assert "name" in response.json()
```

Explanation: Arrange chooses the resource, Act makes exactly one request, Assert checks two aspects of that single response. Run it with `pytest -v -m smoke`. Expected result: the test shows `PASSED` alongside the other smoke tests.

#### Exercise 3: Make the dependent tests independent

Fix this pair so each test passes when run alone:

```python
state = {}

def test_create_post(api):
    r = api.post("/posts", json={"title": "x", "body": "y", "userId": 1})
    state["id"] = r.json()["id"]

def test_post_has_title():
    assert state["id"] is not None
```

**Solution.** The second test must not depend on the first. Decide what it really wants to verify. If it is "a created post echoes its title", put everything in one test:

```python
def test_created_post_echoes_title(api):
    # Arrange
    payload = {"title": "x", "body": "y", "userId": 1}

    # Act
    response = api.post("/posts", json=payload)

    # Assert
    assert response.status_code == 201
    assert response.json()["title"] == "x"
```

If you want a reusable creation step, extract a helper (`_create_post(api)` from section 9) and call it inside each test that needs a post. Check independence by running each test alone using its node ID.

#### Exercise 4: Marker subsets

Your project has these markers: `test_a` (`smoke`), `test_b` (`smoke` and `regression`), `test_c` (`regression`), `test_d` (`regression` and `slow`), `test_e` (no marker). Which tests does each command select?

1. `pytest -m smoke`
2. `pytest -m "regression and not slow"`
3. `pytest -m "smoke or slow"`
4. `pytest -m "not smoke"`

**Solution.**

1. `test_a`, `test_b`.
2. `test_b`, `test_c`. (`test_d` is excluded by `not slow`.)
3. `test_a`, `test_b`, `test_d`.
4. `test_c`, `test_d`, `test_e`. Note that unmarked tests are included by a `not` expression, a common surprise.

Confirm any of these with `--collect-only -q`.

#### Exercise 5: Document a known bug

JSONPlaceholder answers `POST /posts` with an empty title by returning `201`, but your requirements say it should return `400`. Write a test that documents the bug without turning the suite red, and explain what happens when the API is fixed.

**Solution.**

```python
import pytest


@pytest.mark.xfail(reason="BUG-123: API accepts an empty title", strict=True)
def test_create_post_rejects_empty_title(api):
    # Arrange
    payload = {"title": "", "body": "x", "userId": 1}

    # Act
    response = api.post("/posts", json=payload)

    # Assert
    assert response.status_code == 400
```

While the bug exists the assertion fails, and PyTest reports `XFAIL` with the reason, so the run stays green. When the API is fixed, the assertion passes, and because `strict=True` the run **fails** with `[XPASS(strict)]`, which tells the team to delete the marker and keep the test as a permanent guard.

#### Exercise 6: Central config

Make the suite point at a different server without editing any test or config file. Show two ways.

**Solution.** The base URL comes from `utils/config.py`, which reads the `API_BASE_URL` environment variable. So, in one terminal command:

```bash
API_BASE_URL=http://localhost:8765 pytest -m smoke        # macOS / Linux
```

```powershell
$env:API_BASE_URL = "http://localhost:8765"; pytest -m smoke   # Windows PowerShell
```

A second way is to construct a client explicitly: `ApiClient(base_url="http://localhost:8765")`. This overrides the default for that client only, which is useful when testing the client class itself. No test file changes in either case.

#### Exercise 7: Choose the command

Write the command for each situation.

1. Re-run only the tests that failed in the last run.
2. Run only tests whose names contain `404`, showing each test name, and stop at the first failure.
3. List which tests the smoke stage would execute without running them.
4. Run everything but show only a one-line failure summary per failing test, without tracebacks.

**Solution.**

1. `pytest --lf`
2. `pytest -k 404 -v -x`
3. `pytest -m smoke --collect-only -q`
4. `pytest --tb=no` (add `-q` for shorter output)

---

### 17. Self-Check Quiz

Answer from memory, then check against the key below.

1. Which of these functions will PyTest collect by default? (a) `check_login` (b) `test_login` (c) `loginTest` (d) `Test_login`.
2. A class named `PostTests` with methods starting with `test_` is in `test_posts.py`. Will its methods run?
3. What is the purpose of `testpaths` in `pytest.ini`?
4. Name the three phases of AAA and say what the Act phase should contain.
5. What does `--strict-markers` do and what problem does it prevent?
6. What is the difference between `skip` and `xfail`?
7. What does `strict=True` on `xfail` change?
8. You run `pytest -m "regression and not slow"`. A test has no markers at all. Does it run?
9. What does `pytest -x` do? What does `--maxfail=3` do?
10. Why does PyTest hide `print` output by default, and which flag shows it?
11. A test passes in a full run but fails when run alone. What is the likely cause?
12. Why does `assert (response.status_code == 200, "bad status")` never fail?
13. What exit code does PyTest return when it collected no tests?
14. Why should the base URL live in one config file or environment variable?
15. In what file and with what decorator do you usually define a shared client fixture?

**Answer key.**

1. Only (b) `test_login`. Function names must start with `test`. `Test_login` starts with a capital `T`, and matching is case-sensitive.
2. No. The class name must start with `Test`. `PostTests` does not, so it is not collected.
3. It tells PyTest where to look for tests when run without arguments, avoiding scanning irrelevant folders like `.venv`.
4. Arrange (prepare data and preconditions), Act (perform the single operation under test, usually one API call), Assert (check the outcome).
5. It makes an unregistered marker name an error. It prevents a typo such as `smoek` from silently creating a new label that no `-m` filter ever selects.
6. `skip` never runs the test. `xfail` runs it and expects it to fail, so it can notice when the bug is fixed.
7. If the test unexpectedly passes, the run reports a failure (`XPASS(strict)`) instead of a quiet `XPASS`, forcing someone to remove the marker.
8. No. The expression requires the `regression` marker, and an unmarked test does not have it. (The same unmarked test would run under `-m "not slow"`.)
9. `-x` stops after the first failure; `--maxfail=3` stops after three failures.
10. Capturing keeps passing output clean; output is shown only for failures. `-s` turns off capture.
11. A hidden dependency on another test (shared state or execution order).
12. The parentheses create a two-element tuple, which is always truthy. Write `assert cond, "msg"`.
13. Exit code `5`.
14. One place to change; the same tests run against any environment; secrets and environment differences stay out of code.
15. `conftest.py`, with `@pytest.fixture` (commonly `scope="session"` for a shared client).

---

### 18. Glossary

- **API client (helper):** a small class that wraps the HTTP library so tests call `api.get(...)` instead of building URLs and timeouts by hand.
- **Arrange-Act-Assert (AAA):** a three-phase test shape: prepare, perform one action, check the result.
- **Assertion:** a statement that must be true for a test to pass; in PyTest, a plain `assert`.
- **Assertion rewriting:** PyTest's behaviour of transforming `assert` statements at import time so that failures show the values involved.
- **Base URL:** the common beginning of all endpoint addresses, for example `https://jsonplaceholder.typicode.com`.
- **Collection:** the phase where PyTest discovers and imports tests before running any of them.
- **`conftest.py`:** a special PyTest file whose fixtures and hooks apply automatically to tests at and below its folder.
- **Decorator:** a line beginning with `@` above a function that adds behaviour or metadata, such as a marker.
- **Deselected:** collected but filtered out by `-k` or `-m`; not run and not a failure.
- **Discovery:** the name-based rules PyTest uses to find tests.
- **Environment variable:** a named value set outside the code, used to vary configuration by environment.
- **Exit code:** the number a program returns to the operating system; `0` means success.
- **Fixture:** a reusable set-up function whose result PyTest passes to tests that ask for it by name (detailed lesson later today).
- **Marker:** a label on a test, applied with `@pytest.mark.<name>`, used to select or modify tests.
- **Node ID:** the unique address of a test: `path/to/file.py::Class::test_name`.
- **Regression test:** a test that checks previously working behaviour has not broken.
- **Smoke test:** a small, fast test of the most critical functionality, used to decide if deeper testing is worthwhile.
- **Test independence:** each test can run alone, in any order, and give the same result.
- **Timeout:** the maximum time a request may take before it is abandoned.
- **Traceback:** the list of code locations shown when an error occurs.
- **Virtual environment:** an isolated Python environment with its own installed packages for one project.
- **`xfail`:** a marker declaring that a test is expected to fail because of a known bug.

---

## Summary

- PyTest turns scripts into a suite: it discovers tests by **name** (`test_*.py`, `test_*` functions, `Test*` classes without `__init__`), runs each independently, prints a verdict, and returns an exit code that a pipeline can use.
- A good project has a clear home for every concern: `tests/` for tests, `utils/` for config and the API client, `conftest.py` for shared fixtures, `pytest.ini` for settings, and `requirements.txt` for dependencies.
- Write each test as **Arrange-Act-Assert**: prepare data, make one request, check the outcome. Plain `assert` statements are enough, because PyTest's assertion rewriting prints the values involved; add messages when you can add useful context, such as the response body.
- Keep tests **independent**. Never rely on order or on state left by another test, and verify by running a test alone.
- Use **markers** to label tests by purpose (`smoke`, `regression`, `slow`), register them, and enforce them with `--strict-markers`. Use `skip`, `skipif`, and `xfail(strict=True)` for tests that cannot or should not currently pass.
- Select what to run with `-m` (planned categories), `-k` (ad hoc names), node IDs (one exact test), and control output with `-v`, `-q`, `-s`, `-rA`, `--tb`, `-x`, `--maxfail`, `--lf`, and `--collect-only`.
- Put the base URL and timeout in one config module read from environment variables, and wrap `requests` in a small `ApiClient`; that is the single point for later additions such as authentication.
- Name tests `test_<action>_<condition>_<expected result>` so a failure explains itself in one line and `-k` selection works.
- Later this week the same layout carries data-driven tests, mocking, and schema validation (covered Wednesday), accessibility scans (covered Thursday), and the CI/CD pipeline that runs your markers automatically (covered Friday).

---

## Additional Resources

- PyTest documentation, "Get Started": https://docs.pytest.org/en/stable/getting-started.html
- PyTest documentation, "Good Integration Practices" (project layout, discovery, import modes): https://docs.pytest.org/en/stable/explanation/goodpractices.html
- PyTest documentation, "Changing standard (Python) test discovery": https://docs.pytest.org/en/stable/example/pythoncollection.html
- PyTest documentation, "How to write and report assertions": https://docs.pytest.org/en/stable/how-to/assert.html
- PyTest documentation, "Working with custom markers": https://docs.pytest.org/en/stable/example/markers.html
- PyTest documentation, "How to use skip and xfail": https://docs.pytest.org/en/stable/how-to/skipping.html
- PyTest documentation, "Configuration" (`pytest.ini`, `pyproject.toml`): https://docs.pytest.org/en/stable/reference/customize.html
- PyTest documentation, "Command-line flags" reference: https://docs.pytest.org/en/stable/reference/reference.html#command-line-flags
- Requests documentation, "Quickstart": https://requests.readthedocs.io/en/latest/user/quickstart/
- JSONPlaceholder (practice API) guide: https://jsonplaceholder.typicode.com/guide/
