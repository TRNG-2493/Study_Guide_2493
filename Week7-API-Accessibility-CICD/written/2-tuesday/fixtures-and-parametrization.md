# Fixtures and Parametrization

## Learning Objectives

By the end of this lesson you will be able to:

- Explain what a PyTest **fixture** is, what problem it solves, and how PyTest injects it by argument name.
- Write fixtures with `@pytest.fixture`, return values, and use `yield` for teardown that runs even when a test fails.
- Choose a fixture **scope** (`function`, `class`, `module`, `session`), predict setup and teardown order, and diagnose a `ScopeMismatch`.
- Share fixtures with `conftest.py` and chain fixtures that depend on one another.
- Build the Project 2 toolkit: `base_url`, a shared `client`, an auth token, an authenticated client, self-cleaning test-data fixtures, and a **factory fixture**.
- Use `autouse` sparingly, the built-ins `tmp_path`, `monkeypatch`, `capsys`, `request`, and debug with `pytest --fixtures` and `--setup-show`.
- Avoid scope mismatch, mutable shared state, leaked data, and calling fixtures directly.
- Use `@pytest.mark.parametrize` with literal lists: multiple parameters, readable `ids`, stacked decorators, and `pytest.param(..., marks=...)` for per-case `xfail`/`skip`; recognise indirect parametrization.

---

## Why This Matters

Imagine you have written ten API tests this week. Look at the top of each one. Chances are every test creates a client, sets a timeout, maybe logs in to get a token, maybe creates a record to work on, and then (if you remembered) deletes that record at the end. The "real" test, the one or two lines that call an endpoint and assert something, is buried under plumbing. Worse, the plumbing is copy-pasted. When the login endpoint changes from `/login` to `/auth/token`, you edit ten files. When one test forgets its cleanup, a stray record stays on the server and a different test, an hour later, fails with a confusing "expected 100 items, got 101".

PyTest's answer is the **fixture**: a named, reusable piece of setup (and optionally teardown) that PyTest runs for you and hands to any test that asks for it. Tests state *what they need* (`client`, `created_post`) rather than *how to build it*, and cleanup lives next to setup in one place.

The second half addresses a different duplication problem: checking that four invalid IDs all return `404` by copy-pasting four tests. **Parametrization** writes the test once, feeds it many inputs, and reports each input as its own test.

Fixtures and parametrization matter because real API frameworks are mostly fixtures plus thin tests, flaky tests are very often caused by leaked data or shared state, logging in once instead of per test can cut a suite from minutes to seconds, parametrization is the cheapest way to add boundary and negative cases, and pipelines on Friday run unattended, so tests must set up and clean up their own world.

This lesson builds directly on earlier work this week: the `requests` library, the structure of a PyTest API project, status code and JSON validation, and headers and authentication. Everything today reuses those pieces; fixtures are how you package them so every test gets them for free.

A note on the examples: they use a small `ApiClient` wrapper around `requests.Session` like the one from earlier this week (shown in section 8). Because the public practice API JSONPlaceholder does not save writes and has no login endpoint, **every output block here was produced against a local mock server that mimics its shape, stores data, and supports `/login` and `/me`.** Where real-service behaviour would differ, the text says so.

---

## The Concept

### 1. The Problem Fixtures Solve

Start with a concrete, realistic scenario. You are testing a blog API. You want a test that updates a post. To do that, the test needs:

1. An HTTP client pointed at the right server.
2. A post that exists (so there is something to update).
3. Cleanup afterwards so the server is left as you found it.

Without fixtures, the test looks like this:

```python
# tests/test_posts_no_fixtures.py  (the "before" picture)
from api.client import ApiClient

BASE_URL = "http://127.0.0.1:8911"


def test_update_post():
    client = ApiClient(BASE_URL)                                   # plumbing 1
    created = client.post("/posts", json={"title": "T", "body": "B", "userId": 1})
    assert created.status_code == 201                              # plumbing 2
    post = created.json()

    response = client.put(f"/posts/{post['id']}", json={**post, "title": "Updated"})
    assert response.status_code == 200                             # the actual test
    assert response.json()["title"] == "Updated"

    client.delete(f"/posts/{post['id']}")                          # plumbing 3
```

Count the lines: only three express the test's purpose. The rest is setup and cleanup. Now ask what goes wrong:

- **Duplication.** Every test that needs a post repeats lines 1 to 3. Change the payload shape and you edit every test.
- **Cleanup is skipped on failure.** If the `assert response.status_code == 200` line fails, Python raises `AssertionError` and **the final `client.delete(...)` never runs.** The post leaks. Failing tests are exactly when you most need tidy cleanup, and plain code gives you the least.
- **Noise hides intent.** A reviewer must read all the lines to find the one that matters.

You could wrap the test in `try/finally`, but that adds noise. A fixture solves all three problems.

### 2. What Is a Fixture?

A **fixture** is a function, marked with `@pytest.fixture`, that prepares something a test needs (data, a client, a logged-in session, a temporary folder) and, optionally, cleans it up afterwards. A test **requests** a fixture simply by naming it as a parameter. PyTest runs the fixture and passes its result into the test.

**Analogy.** Picture a cooking class. Before students arrive, an assistant lays out ingredients and equipment at every station (setup). After the class, the assistant washes everything and clears the benches (teardown). The students never think about this; they just cook. Fixtures are the assistant. Tests are the students. And just as a different class might need different equipment, different tests request different fixtures.

The technical term for this mechanism is **dependency injection**: a test does not construct its own dependencies; they are *injected* from outside by the framework. The name of the parameter is the lookup key.

### 3. Your First Fixture, Step by Step

Start with the smallest possible example, with no network at all, so you can focus purely on the mechanism.

```python
# tests/test_a_basics.py
import pytest


@pytest.fixture
def greeting():
    print("  [setup greeting]")
    return "hello"


def test_greeting_is_lowercase(greeting):
    assert greeting == greeting.lower()
```

Line by line:

- `import pytest`: gives you the `pytest.fixture` decorator.
- `@pytest.fixture`: a **decorator** (a function that wraps another function). It registers the function below it in PyTest's fixture registry under the function's name, here `greeting`. It does not run the function yet.
- `def greeting():`: the fixture function. Its name is the name tests will use to request it.
- `print("  [setup greeting]")`: a visible marker so you can see when PyTest runs the fixture.
- `return "hello"`: the value that will be handed to the test.
- `def test_greeting_is_lowercase(greeting):`: a normal test function, except it has a parameter named `greeting`. PyTest looks at every test's parameter names. If a parameter name matches a registered fixture, PyTest runs that fixture first and passes its return value in as the argument.
- `assert greeting == greeting.lower()`: inside the test, `greeting` is the string `"hello"`, not a function.

In short: PyTest inspects the test's signature, finds the fixture named `greeting`, runs it, and injects the return value as the argument.

Run it with `-s` (do not capture print output) to see the ordering:

```bash
pytest tests/test_a_basics.py -v -s -k greeting
```

Output (local run, trimmed):

```text
tests/test_a_basics.py::test_greeting_is_lowercase   [setup greeting]
PASSED
```

The "setup" print appears before the PASSED result, proving the fixture ran before the test finished. You never called `greeting()` yourself. **Never call a fixture directly**; PyTest raises an error if you try (section 20).

### 4. Setup and Teardown With `yield`

`return` ends a function. That is fine when there is nothing to clean up. When there is, use `yield` instead. Everything **before** `yield` is setup. The yielded value is what the test receives. Everything **after** `yield` is teardown, and PyTest runs it after the test finishes, **whether the test passed or failed.**

```python
@pytest.fixture
def numbers():
    print("  [setup numbers]")
    data = [1, 2, 3]
    yield data
    print("  [teardown numbers]")


def test_sum(numbers):
    assert sum(numbers) == 6


def test_failing_still_tears_down(numbers):
    assert len(numbers) == 99      # deliberately wrong
```

Run it:

```bash
pytest tests/test_a_basics.py -v -s -k "sum or failing"
```

Output (local run):

```text
tests/test_a_basics.py::test_sum   [setup numbers]
PASSED  [teardown numbers]

tests/test_a_basics.py::test_failing_still_tears_down   [setup numbers]
FAILED  [teardown numbers]
```

Study the second case: the test **failed**, yet teardown still printed. That is the point: teardown is guaranteed, which the "before" example in section 1 could not promise. Mentally, a `yield` fixture is a generator: PyTest runs it to the `yield`, pauses it, runs the test, then resumes it.

**Error versus failure.** Look at what happens when the *fixture* itself raises:

```python
@pytest.fixture
def broken():
    raise RuntimeError("setup exploded")


def test_uses_broken(broken):
    assert True
```

Output (local run):

```text
tests/test_a_basics.py::test_uses_broken ERROR

______________________ ERROR at setup of test_uses_broken ______________________
E       RuntimeError: setup exploded
```

PyTest labels this **ERROR at setup**, not FAILED. The distinction matters when triaging a pipeline:

- **FAILED** means the test ran and an assertion (or exception) in the test body said the product misbehaved. That is a candidate product bug.
- **ERROR** means the test could not even start because its setup (or teardown) broke. That is usually an environment, data, or framework problem, not a product defect.

If you see forty ERRORs in a row after one deploy, suspect the shared setup (for example login), not forty separate bugs.

**A safer teardown pattern.** If your setup has several steps and the second step fails, code after `yield` never runs, because the generator never reached the `yield`. The first step's resources would leak. Protect against this with `try/finally`, recording what has been created as you go:

```python
@pytest.fixture
def post_with_extras(client):
    created = []                                   # ids we must delete later
    try:
        post = client.post("/posts", json={"title": "t", "body": "b", "userId": 1}).json()
        created.append(post["id"])                 # record immediately after creating
        # ... a second setup step that might fail would go here ...
        yield post
    finally:                                       # runs on success, failure, or setup error
        for post_id in created:
            client.delete(f"/posts/{post_id}")
```

The key idea: **record each resource the instant it exists**, and delete from that record in `finally`. For simple one-step fixtures the plain `yield` form is enough. Older code uses `request.addfinalizer(function)` to register cleanup after each setup step; both work, but prefer `yield` for readability.

### 5. Where Fixtures Can Live

A fixture is available to a test depending on where it is defined:

- The same module: tests in that file only.
- A test class: tests in that class only.
- `conftest.py`: every test in that folder and below.
- PyTest or a plugin: every test (built-ins like `tmp_path`).

If two files need a fixture, move it to `conftest.py`.

#### 5.1 `conftest.py`

PyTest automatically loads any file named exactly **`conftest.py`**. You do **not** import fixtures from it; PyTest wires them in. This is the single most useful organising feature for an API framework.

```text
project2-api-tests/
├── pytest.ini
├── conftest.py              # fixtures available to every test
├── api/
│   ├── __init__.py
│   └── client.py            # ApiClient wrapper
└── tests/
    ├── conftest.py          # optional: fixtures only for tests/ below
    ├── test_users.py
    ├── test_posts.py
    └── orders/
        ├── conftest.py      # optional: fixtures only for tests/orders/
        └── test_orders.py
```

Name the file exactly `conftest.py`, put widely shared fixtures at the root and narrow ones beside their tests, and never `import` from it (PyTest injects; importing can load it twice).

#### 5.2 Which fixture wins? Overriding by proximity

If the same fixture name appears at several levels, PyTest uses the one **closest to the test**: test module beats nearest `conftest.py`, which beats a parent `conftest.py`, which beats plugins. This lets a sub-folder customise a global fixture. A fixture can even request the parent fixture of the same name:

```python
# tests/orders/conftest.py
import pytest


@pytest.fixture
def client(client):
    """Override: same name, but wraps the parent fixture and tweaks it."""
    client.session.headers["X-Suite"] = "orders"
    yield client
    client.session.headers.pop("X-Suite", None)
```

The parameter `client` here receives the **parent** fixture's value (from the root `conftest.py`), and the new function replaces it for tests under `tests/orders/`. Two tests confirmed it (local run: `2 passed`): tests under `tests/orders/` see the `X-Suite` header, others do not. The override *undoes* its change in teardown, which matters because the underlying client is session-scoped and shared (see pitfalls, section 18).

### 6. Fixture Scopes

By default a fixture runs again for **every test** that requests it. That is safe, because every test gets fresh data, but it can be slow if the setup is expensive (for example, logging in over the network). The `scope` argument controls how long a fixture's value lives before PyTest discards it and (if requested again) rebuilds it.

| Scope | Created | Torn down | Good for |
|-------|---------|-----------|----------|
| `function` (default) | Before each test that requests it | After that test | Test data a test may modify |
| `class` | Once per test class | After the class's last test | A group of related tests in a class |
| `module` | Once per `.py` file | After the file's last test | Data shared read-only across one file |
| `session` | Once per whole `pytest` run | At the very end | Expensive, read-only setup: base URL, config, login token, connection pool |

There is also a `package` scope (once per package directory); it is rarely needed in beginner suites, so we will not use it.

You write the scope in the decorator:

```python
@pytest.fixture(scope="session")
def auth_token(client):
    ...
```

#### 6.1 Seeing scopes in action

Here is a file with one fixture at each scope, a class with two tests, and one test outside the class:

```python
# tests/test_d_scopes.py
import pytest


@pytest.fixture(scope="session")
def s_fix():
    yield "session"


@pytest.fixture(scope="module")
def m_fix():
    yield "module"


@pytest.fixture(scope="class")
def c_fix():
    yield "class"


@pytest.fixture
def f_fix():
    yield "function"


class TestGroup:
    def test_one(self, s_fix, m_fix, c_fix, f_fix):
        pass

    def test_two(self, s_fix, m_fix, c_fix, f_fix):
        pass


def test_outside_class(s_fix, m_fix, f_fix):
    pass
```

Run with `--setup-show`, which prints every setup and teardown with its scope letter (`S`, `M`, `C`, `F`):

```bash
pytest tests/test_d_scopes.py --setup-show -q
```

Output (local run):

```text
SETUP    S s_fix
    SETUP    M m_fix
      SETUP    C c_fix
        SETUP    F f_fix
        tests/test_d_scopes.py::TestGroup::test_one (fixtures used: c_fix, f_fix, m_fix, s_fix) .
        TEARDOWN F f_fix
        SETUP    F f_fix
        tests/test_d_scopes.py::TestGroup::test_two (fixtures used: c_fix, f_fix, m_fix, s_fix) .
        TEARDOWN F f_fix
      TEARDOWN C c_fix
        SETUP    F f_fix
        tests/test_d_scopes.py::test_outside_class (fixtures used: f_fix, m_fix, s_fix) .
        TEARDOWN F f_fix
    TEARDOWN M m_fix
TEARDOWN S s_fix
3 passed in 0.01s
```

Read it like a tree (indentation is nesting depth): `s_fix` is set up once and torn down last; `m_fix` once per file; `c_fix` around `TestGroup` only (`test_outside_class` never uses it); `f_fix` around **each** test, twice in the class and once outside.

**Teardown happens in reverse order of setup** (last in, first out), like unstacking plates. This guarantees that a resource is never destroyed while something that depends on it is still alive.

Note also that a fixture is built **lazily**: only when the first test requests it. A session fixture nobody requests never runs.

#### 6.2 How to choose a scope

Ask two questions:

1. **Is it expensive to create?** Network logins, database connections, and starting servers are. Creating a dict is not.
2. **Can a test change it?** If any test might modify the value (a record, a header, a list), sharing it makes tests depend on each other.

Cheap setup: use `function`. Expensive and read-only: `session` (or `module`). Expensive and mutable: share the expensive *connection* widely, but create the *mutable data* per test.

Examples from an API suite:

- `base_url`: read-only string, session scope.
- `auth_token`: a string obtained once, session scope.
- `client` (a `requests.Session`): shared connection pool, session scope, **provided no test changes its headers** (see the pitfalls).
- `created_post`: a record tests may edit, function scope.

**Rule of thumb:** use the *narrowest* scope that is fast enough. Widen only when profiling shows setup time hurts, and only for state tests do not mutate.

#### 6.3 The scope-mismatch rule

A fixture may only depend on fixtures of the **same or wider** scope. A session fixture cannot request a function fixture, because the function fixture would be created and destroyed per test, while the session fixture must outlive all tests. PyTest refuses:

```python
# tests/test_e_mismatch.py
import pytest


@pytest.fixture
def per_test_value():          # function scope (default)
    return 42


@pytest.fixture(scope="session")
def long_lived(per_test_value):    # session asks for function: not allowed
    return per_test_value + 1


def test_it(long_lived):
    assert long_lived == 43
```

Output (local run):

```text
__________________________ ERROR at setup of test_it ___________________________
ScopeMismatch: You tried to access the function scoped fixture per_test_value with a session scoped request object. Requesting fixture stack:
tests/test_e_mismatch.py:9:  def long_lived(per_test_value)
Requested fixture:
tests/test_e_mismatch.py:4:  def per_test_value()
```

How to read it: the message names the offender (`per_test_value`, function scoped), the requester (a session-scoped request), and the stack that led there. The fix is either to widen `per_test_value` to `scope="session"`, or to narrow `long_lived` to function scope. Which one depends on question 2 above.

Remember the direction: **wide fixtures cannot depend on narrow ones; narrow can depend on wide.** A function-scoped `auth_client` may request the session-scoped `auth_token`. The reverse is forbidden.

### 7. Fixture Chaining (Composition)

Fixtures can request other fixtures exactly as tests do, by naming them as parameters. This is **chaining** or **composition**, and it lets you build complex setups from small, single-purpose pieces.

```python
# tests/test_g_chain_autouse.py
import pytest


@pytest.fixture
def user_payload():
    return {"name": "Ada", "email": "ada@example.test"}


@pytest.fixture
def saved_user(user_payload):
    print("  [saved_user setup]")
    return {**user_payload, "id": 7}


@pytest.fixture
def user_summary(saved_user):
    return f"{saved_user['id']}:{saved_user['name']}"


def test_chain(user_summary):
    assert user_summary == "7:Ada"
```

The test asks only for `user_summary`. PyTest builds the whole chain behind the scenes: `user_summary` needs `saved_user`, which needs `user_payload`. Running with `--setup-show` makes it visible:

```text
        SETUP    F user_payload
        SETUP    F saved_user (fixtures used: user_payload)
        SETUP    F user_summary (fixtures used: saved_user)
        tests/test_g_chain_autouse.py::test_chain (fixtures used: ..., saved_user, user_payload, user_summary) PASSED
        TEARDOWN F user_summary
        TEARDOWN F saved_user
        TEARDOWN F user_payload
```

(The real output also lists an autouse fixture from section 11; it is omitted here for clarity.) Dependencies are set up **first** and torn down **last**. A fixture is built once per scope instance and **shared by everything that requests it in that test**: if both the test and `saved_user` request `user_payload`, they receive the *same* object, not two copies. That is useful (consistent data) and occasionally surprising (a mutation in one place is visible in the other).

Small fixtures are reusable and make `--setup-show` meaningful; real API chains look like `base_url -> client -> auth_token -> auth_client -> created_order`.

### 8. Fixtures for API Testing: The Project 2 Toolkit

Now apply everything to the fixtures a real API framework uses. First, the wrapper class. This is a minimal version of the `ApiClient` from earlier this week; yours may differ in details, which is fine.

```python
# api/client.py
import requests


class ApiClient:
    """Thin wrapper around requests.Session with a base URL and a default timeout."""

    def __init__(self, base_url, timeout=10):
        self.base_url = base_url.rstrip("/")
        self.timeout = timeout
        self.session = requests.Session()

    def request(self, method, path, **kwargs):
        kwargs.setdefault("timeout", self.timeout)
        return self.session.request(method, self.base_url + path, **kwargs)

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

Key points: `base_url.rstrip("/")` prevents a double slash; `kwargs.setdefault("timeout", ...)` ensures every call has a timeout (a request with no timeout can hang a pipeline forever); a `requests.Session` reuses the TCP connection and carries headers and cookies between calls.

Now the root `conftest.py`:

```python
# conftest.py  (project root)
import os

import pytest

from api.client import ApiClient


@pytest.fixture(scope="session")
def base_url():
    """Root URL of the API under test (override with API_BASE_URL)."""
    return os.environ.get("API_BASE_URL", "https://jsonplaceholder.typicode.com")


@pytest.fixture(scope="session")
def client(base_url):
    """One shared, unauthenticated client for the whole run."""
    c = ApiClient(base_url)
    yield c
    c.close()


@pytest.fixture(scope="session")
def auth_token(client):
    """Log in once per run and hand out the token string."""
    response = client.post(
        "/login",
        json={
            "username": os.environ.get("API_USER", "qa"),
            "password": os.environ.get("API_PASSWORD", "secret"),
        },
    )
    assert response.status_code == 200, f"Login failed: {response.status_code}"
    return response.json()["token"]


@pytest.fixture
def auth_client(base_url, auth_token):
    """A fresh client per test that already carries the Bearer token."""
    c = ApiClient(base_url)
    c.session.headers["Authorization"] = f"Bearer {auth_token}"
    yield c
    c.close()
```

Why each fixture looks the way it does:

- **`base_url` (session).** Reads `API_BASE_URL` with a fallback, so the same tests run against local, staging and CI with no code change. It is read-only and cheap, but a fixture means nobody hard-codes URLs.
- **`client` (session, `yield`).** One shared `ApiClient`; teardown calls `close()` to release the connection pool, guaranteed at the end of the run.
- **`auth_token` (session).** Logs in **once** and returns only the token string: the classic "expensive, read-only" case. Credentials come from environment variables, never source code. The defaults (`qa`, `secret`) exist only for the local mock; in a real project give secrets no default. The message on the `assert` turns a bad login into one clear setup ERROR (`Login failed: 401`) instead of forty puzzling `401`s. Never print or commit tokens.
- **`auth_client` (function).** A *new* `ApiClient` per test with the header already set. Setting the header on the shared `client` would leak into every other test (proved in section 18). Creating an object makes no network call, so this is cheap, and a narrow fixture depending on the wide `auth_token` is allowed.

Use them:

```python
# tests/test_b_api.py (excerpt)
def test_get_user(client):
    r = client.get("/users/1")
    assert r.status_code == 200


def test_me_requires_token(client, auth_client):
    assert client.get("/me").status_code == 401
    assert auth_client.get("/me").status_code == 200
```

The second test pairs the same endpoint with and without credentials and **reads like the requirement**.

> **Practice-API note.** JSONPlaceholder has no `/login` or `/me`. The auth fixtures above run against the course's local mock (and will run against whichever authenticated API your Project 2 targets); against pure JSONPlaceholder you would skip `auth_token`/`auth_client`. The *pattern* (log in once, inject the token) is what you are learning.

#### 8.1 A test-data fixture that cleans up

```python
# conftest.py (continued)
@pytest.fixture
def created_post(client):
    """Create a post, give it to the test, delete it afterwards."""
    response = client.post("/posts", json={"title": "Fixture post", "body": "Created by fixture", "userId": 1})
    assert response.status_code == 201, "Setup failed: could not create post"
    post = response.json()

    yield post

    client.delete(f"/posts/{post['id']}")
```

Line by line:

- `def created_post(client):` the fixture requests the session `client`: chaining in action.
- `client.post(...)` creates the record through the API. Creating data through the **public API** (rather than poking a database) tests the same path real users take and keeps your framework independent of the database.
- `assert response.status_code == 201, "Setup failed..."`: a light sanity check. The rule from the pitfalls list is that *fixtures prepare and tests judge*, but verifying that setup worked is acceptable and gives a precise error message. If it fails you get `ERROR at setup`, which tells triagers it was a setup problem, not the feature under test.
- `post = response.json()`: save the created record, including the server-assigned `id`.
- `yield post`: pause. The test runs now and receives `post`.
- `client.delete(f"/posts/{post['id']}")`: teardown. It reads the id from the same dictionary the test received, so it assumes the test never changes `post['id']`; if a test did, cleanup would target the wrong record (see mistake 6 in section 20 for the safer pattern).

Use it:

```python
def test_update_post(client, created_post):
    r = client.put(f"/posts/{created_post['id']}", json={**created_post, "title": "Updated"})
    assert r.status_code == 200
    assert r.json()["title"] == "Updated"
```

`{**created_post, "title": "Updated"}` copies the dictionary and overrides one key, leaving the original untouched. The test contains no creation and no deletion code, only the behaviour under test.

#### 8.2 Proving that cleanup works

A fixture that claims to clean up should be *checked*. Here is a "leak detector", a test that asserts the server holds exactly the seed data (100 posts in our mock):

```python
# tests/test_c_cleanup_check.py
def test_no_leftover_posts(client):
    posts = client.get("/posts").json()
    assert len(posts) == 100, f"leaked {len(posts) - 100} posts"
```

Run after the well-behaved fixtures:

```text
tests/test_b_api.py ......
tests/test_c_cleanup_check.py .                                          [100%]
6 passed in 0.04s
```

Now see what a fixture **without** teardown does:

```python
# tests/test_j_leak.py
import pytest


@pytest.fixture
def leaky_post(client):
    r = client.post("/posts", json={"title": "leak", "body": "b", "userId": 1})
    return r.json()          # no cleanup!


def test_one(leaky_post):
    assert leaky_post["id"]


def test_two(leaky_post):
    assert leaky_post["id"]
```

Running `test_j_leak.py` followed by the leak detector gives:

```text
E       AssertionError: leaked 2 posts
E       assert 102 == 100
...
FAILED tests/test_c_cleanup_check.py::test_no_leftover_posts - AssertionError...
1 failed, 2 passed in 0.03s
```

Both "leaky" tests pass. The damage shows up in an *unrelated* test, later, which is exactly why leaked data is so hard to diagnose in real suites. In shared environments such as staging, leaked records accumulate across runs until some count, uniqueness, or pagination check breaks.

> **Real-service note (representative).** The public JSONPlaceholder acknowledges `POST` with `201` and a new `id` (typically `101`) but does **not** save it, so a later `GET /posts/101` returns `404` and `DELETE` returns `200` regardless. Fixtures still work, but you cannot demonstrate "created then deleted" end to end against it. On your own API you can, and you should.

### 9. Factory Fixtures: Creating Many Items on Demand

`created_post` gives exactly one post, always with the same content. What if a test needs three posts, or a post with a particular title? A **factory fixture** returns a *function* that creates items on demand, and remembers every item so it can clean up all of them.

```python
# conftest.py (continued)
@pytest.fixture
def post_factory(client):
    """Return a function that creates posts; delete every one at teardown."""
    created_ids = []

    def make_post(**overrides):
        payload = {"title": "Default", "body": "Body", "userId": 1, **overrides}
        response = client.post("/posts", json=payload)
        assert response.status_code == 201
        post = response.json()
        created_ids.append(post["id"])
        return post

    yield make_post

    for post_id in created_ids:
        client.delete(f"/posts/{post_id}")
```

Line by line: `created_ids = []` is the "shopping receipt" of everything created. `**overrides` collects keyword arguments (`title="One"` becomes `{"title": "One"}`), and because later keys win in a dictionary literal, they replace the defaults. `created_ids.append(...)` **records every creation** so teardown knows what to delete. `yield make_post` makes the fixture's value the *function itself*, which tests call; the loop after `yield` deletes everything created, however many items and however the test ended.

```python
def test_two_posts_have_different_ids(post_factory):
    first = post_factory(title="One")
    second = post_factory(title="Two")
    assert first["id"] != second["id"]
```

Run with `--setup-show` (local run):

```text
        SETUP    F post_factory (fixtures used: client)
        tests/test_b_api.py::test_two_posts_have_different_ids (...) PASSED
        TEARDOWN F post_factory
```

One fixture, two posts created, both deleted in the single teardown. The leak detector passes afterwards.

Use a plain fixture for exactly one standard record, a factory for several records or custom values per test, and parametrization (section 13) for a table of cases, optionally with a factory.

### 10. Built-in Fixtures You Get for Free

PyTest ships with fixtures you can request in any test. You met `request` implicitly already. Four are worth knowing now.

- **`tmp_path`**: a `pathlib.Path` to a per-test temporary directory, cleaned up by PyTest (reports without polluting the repo).
- **`monkeypatch`**: temporary changes to environment variables, attributes, dictionaries, automatically undone.
- **`capsys`**: captures what code prints to stdout and stderr.
- **`request`**: information about the requesting test; `request.param` in parametrized fixtures.

All four are shown in one verified file:

```python
# tests/test_h_builtins.py
import json
import os


def save_report(folder, data):
    path = folder / "report.json"
    path.write_text(json.dumps(data))
    return path


def test_tmp_path_is_unique_and_real(tmp_path):
    path = save_report(tmp_path, {"passed": 3})
    assert path.exists()
    assert json.loads(path.read_text()) == {"passed": 3}


def get_base_url():
    return os.environ.get("API_BASE_URL", "https://jsonplaceholder.typicode.com")


def test_monkeypatch_env(monkeypatch):
    monkeypatch.setenv("API_BASE_URL", "https://staging.example.test")
    assert get_base_url() == "https://staging.example.test"


def test_monkeypatch_missing_env(monkeypatch):
    monkeypatch.delenv("API_BASE_URL", raising=False)
    assert get_base_url() == "https://jsonplaceholder.typicode.com"


def print_summary(passed, failed):
    print(f"passed={passed} failed={failed}")


def test_capsys(capsys):
    print_summary(3, 1)
    captured = capsys.readouterr()
    assert captured.out == "passed=3 failed=1\n"
    assert captured.err == ""


def test_env_restored_after_monkeypatch():
    assert os.environ["API_BASE_URL"].startswith("http://127.0.0.1")
```

Output (local run): `5 passed in 0.02s`.

Notes: `folder / "report.json"` uses `pathlib`'s `/` operator, and the file lands in a throwaway directory unique to each test. `monkeypatch.setenv` changes the variable for this test only; the last test proves PyTest restored it. `raising=False` means "do not complain if it was not set". `capsys.readouterr()` returns `.out` and `.err`.

Caution: `monkeypatch` only changes things read at **call time**. A value captured at import time (`BASE_URL = os.environ[...]` at module top) is already fixed, so read config inside functions or fixtures, as `get_base_url()` does.

### 11. Autouse Fixtures and `usefixtures`

Normally a fixture runs only when a test requests it. Setting `autouse=True` makes it run for **every test in its scope** with no request needed.

```python
# tests/test_g_chain_autouse.py (continued)
import time


@pytest.fixture(autouse=True)
def log_test_name(request):
    print(f"\n--- starting {request.node.name} ---")
    started = time.perf_counter()
    yield
    print(f"--- finished {request.node.name} in {time.perf_counter() - started:.3f}s ---")


def test_a():
    assert True
```

`request.node.name` is the running test's name, and `time.perf_counter()` is a high-resolution clock. Nothing in `test_a` mentions `log_test_name`, yet it ran (output with `-s`; the stray `.` is PyTest's progress dot):

```text
--- starting test_a ---
.--- finished test_a in 0.000s ---
```

Where does an autouse fixture apply? To every test in its **definition scope**: in a module, to that module's tests; in a class, to that class; in `conftest.py`, to every test below it. A root-level autouse fixture therefore touches *every* test in the project.

Good for logging, timing, or restoring global state every test needs. Bad for anything that creates data or makes network calls (a reader cannot see it, and a cleanup bug becomes global) and for anything only some tests need.

A middle path is `@pytest.mark.usefixtures("name")`, which requests a fixture **without taking its value as a parameter**. It is visible in the test's decoration, but does not clutter the signature. Use it when you need the *side effect* only:

```python
@pytest.mark.usefixtures("saved_user")
def test_requested_without_using_value():
    assert True
```

### 12. Debugging Fixtures: `--fixtures` and `--setup-show`

Two flags answer "where does this fixture come from?" and "in what order do things run?".

**`pytest --fixtures`** lists every fixture available to the given path, grouped by where it is defined, with its scope, source file and line, and first docstring line. Write docstrings on shared fixtures; they become your documentation:

```bash
pytest --fixtures tests/test_b_api.py
```

Output (local run, trimmed):

```text
------------------------ fixtures defined from conftest ------------------------
client [session scope] -- conftest.py:15
    One shared, unauthenticated client for the whole run.

created_post -- conftest.py:46
    Create a post, give it to the test, delete it afterwards.
...
```

A fixture with no scope label is function scoped. Your built-in and plugin list will differ from ours.

**`pytest --setup-show`** prints each fixture's setup and teardown as tests run, with scope letters `S`, `M`, `C`, `F` (and `P` for package). In our API toolkit run (`pytest tests/test_b_api.py tests/test_c_cleanup_check.py -v --setup-show`, local) it showed `SETUP S base_url` and `SETUP S client` once at the first test, `SETUP F created_post` / `TEARDOWN F created_post` around each test that used it, `auth_token` created lazily at its first user, and the session teardowns last in reverse order (`auth_token`, `client`, `base_url`). Combine it with `pytest -v` (full test IDs) and `-k name` (run matching tests) to isolate and watch one misbehaving test.

### 13. Parametrization: One Test, Many Inputs

Fixtures reduce duplicated *setup*. **Parametrization** reduces duplicated *tests*. Suppose you want to confirm that four different nonexistent IDs all return `404`. The copy-paste approach gives four near-identical functions. With `@pytest.mark.parametrize`, you write one:

```python
# tests/test_i_param.py
import pytest


@pytest.mark.parametrize("post_id", [99999, 0, -1, 100000])
def test_nonexistent_post_returns_404(client, post_id):
    r = client.get(f"/posts/{post_id}")
    assert r.status_code == 404
```

Anatomy:

- `@pytest.mark.parametrize(argnames, argvalues)`: a decorator that tells PyTest to generate several tests from this function.
- `"post_id"`: the **name** of the test parameter to fill. It must match a parameter in the function signature exactly.
- `[99999, 0, -1, 100000]`: the **values**, one per generated test.
- The function receives `post_id` as an ordinary argument and also still receives the `client` fixture. **Fixtures and parameters mix freely** in the same signature.

PyTest creates one independent test per value:

```text
tests/test_i_param.py::test_nonexistent_post_returns_404[99999] PASSED   [  3%]
tests/test_i_param.py::test_nonexistent_post_returns_404[0] PASSED       [  6%]
tests/test_i_param.py::test_nonexistent_post_returns_404[-1] PASSED      [  9%]
tests/test_i_param.py::test_nonexistent_post_returns_404[100000] PASSED  [ 12%]
```

(local run). The text in square brackets is the **test ID**, built from the value. Each case:

- passes or fails **independently**: a failing `[0]` does not stop `[-1]` from running;
- can be run alone: `pytest "tests/test_i_param.py::test_nonexistent_post_returns_404[0]"`;
- appears separately in reports, which is what stakeholders and CI dashboards count.

**Important:** these are *boundary-value* inputs (non-existent, zero, negative, just past the maximum). Parametrization is the natural way to cover them without writing the same test four times.

#### 13.1 Multiple parameters with expected results

Often the input and the expected output travel together. Pass the names as one comma-separated string and the cases as a list of tuples:

```python
@pytest.mark.parametrize(
    "user_id, expected_name",
    [
        (1, "Leanne Graham"),
        (2, "Ervin Howell"),
        (3, "Clementine Bauch"),
    ],
)
def test_user_names(client, user_id, expected_name):
    r = client.get(f"/users/{user_id}")
    assert r.status_code == 200
    assert r.json()["name"] == expected_name
```

Each tuple is unpacked positionally: the first element fills `user_id`, the second `expected_name`. The count of names in the string must equal the count of elements in every tuple; a mismatch raises an error at collection time, not mid-run. The generated IDs join values with a dash: `test_user_names[1-Leanne Graham]`.

What a failure looks like: with the second expected name changed to `"Wrong Name"`, PyTest reports only `FAILED test_user_names[2-Wrong Name]` (`assert 'Ervin Howell' == 'Wrong Name'`) and `1 failed, 2 passed`. A single `for` loop inside one test would have stopped at the first failure and hidden the rest.

#### 13.2 Readable test IDs

Auto-generated IDs are fine for numbers and short strings. For dictionaries and long values PyTest falls back to names like `payload0`, which are meaningless. Give cases descriptive IDs with `pytest.param(..., id="...")`:

```python
@pytest.mark.parametrize(
    "payload, expected_status",
    [
        pytest.param({"title": "ok", "body": "b", "userId": 1}, 201, id="valid"),
        pytest.param({}, 201, id="empty-body-practice-api-accepts"),
        pytest.param({"title": "x" * 5000, "body": "b", "userId": 1}, 201, id="very-long-title"),
    ],
)
def test_create_post_status(client, payload, expected_status):
    r = client.post("/posts", json=payload)
    assert r.status_code == expected_status
    client.delete(f"/posts/{r.json()['id']}")
```

Output:

```text
tests/test_i_param.py::test_create_post_status[valid] PASSED
tests/test_i_param.py::test_create_post_status[empty-body-practice-api-accepts] PASSED
tests/test_i_param.py::test_create_post_status[very-long-title] PASSED
```

`pytest.param(value1, value2, id="name")` wraps one case: the positional arguments are the values for that case (matching the parameter names), and `id` is its label. Choose IDs that read like a sentence in a bug report: `[empty-body-practice-api-accepts]` tells a reader everything.

Two notes. A *real* API should usually answer `400` or `422` for an empty body; the practice API is permissive, so these expectations describe the **fake service**; base real expectations on the documented contract. And this test cleans up in its body, so a failed assertion would skip the cleanup; a `post_factory` would be safer (section 15).

#### 13.3 The same check across many endpoints

```python
@pytest.mark.parametrize("path", ["/posts", "/comments", "/albums", "/photos", "/todos", "/users"])
def test_collections_return_200_and_a_list(client, path):
    r = client.get(path)
    assert r.status_code == 200
    assert isinstance(r.json(), list)
```

Six endpoints, one test body: the classic smoke test over a list of endpoints.

#### 13.4 Stacking decorators: all combinations

Stack two `parametrize` decorators and PyTest runs the **cartesian product**, every combination of one value from each:

```python
@pytest.mark.parametrize("user_id", [1, 2])
@pytest.mark.parametrize("limit", [1, 3, 5])
def test_posts_filter_and_limit(client, user_id, limit):
    r = client.get("/posts", params={"userId": user_id, "_limit": limit})
    posts = r.json()
    assert len(posts) == limit
    assert all(p["userId"] == user_id for p in posts)
```

Output (local run):

```text
test_posts_filter_and_limit[1-1] PASSED
test_posts_filter_and_limit[1-2] PASSED
test_posts_filter_and_limit[3-1] PASSED
test_posts_filter_and_limit[3-2] PASSED
test_posts_filter_and_limit[5-1] PASSED
test_posts_filter_and_limit[5-2] PASSED
```

2 x 3 = 6 tests. Two details beginners miss: (1) **ID segments follow the decorators from bottom to top**: in `[3-1]` the `3` is `limit` (nearest the function) and the `1` is `user_id`; (2) **combinations multiply fast** (three parameters of five values make 125 tests), so stack only when every combination is meaningful, otherwise use one `parametrize` with tuples.

The test body also shows a good assertion habit: `all(p["userId"] == user_id for p in posts)` checks **every** item, not just the first.

#### 13.5 Marking individual cases: `xfail` and `skip`

Sometimes one case in a list is known to be broken or not ready. You do not want to delete it (the knowledge would be lost) or let it turn the whole run red. `pytest.param` accepts a `marks=` argument to attach marks to a single case:

```python
@pytest.mark.parametrize(
    "bad_id",
    [
        "abc",
        pytest.param("-5", id="negative"),
        pytest.param("007", marks=pytest.mark.xfail(reason="BUG-123: API accepts leading zeros", strict=True)),
        pytest.param("0", marks=pytest.mark.skip(reason="pending decision on id 0")),
    ],
)
def test_invalid_post_id_is_rejected(client, bad_id):
    assert client.get(f"/posts/{bad_id}").status_code in (400, 404)
```

Run with `-rxs` (report xfail and skip reasons):

```text
test_invalid_post_id_is_rejected[abc] PASSED
test_invalid_post_id_is_rejected[negative] PASSED
test_invalid_post_id_is_rejected[007] XFAIL (...)
test_invalid_post_id_is_rejected[0] SKIPPED (...)

XFAIL tests/test_i_param.py::test_invalid_post_id_is_rejected[007] - BUG-123: API accepts leading zeros
SKIPPED [1] tests/test_i_param.py:54: pending decision on id 0
=================== 30 passed, 1 skipped, 1 xfailed in 0.11s ===================
```

(The "30 passed" counts every test in the file, not only these four.) The vocabulary:

- **`skip`**: do not run this case at all. Use when it cannot or should not run yet.
- **`xfail`** ("expected failure"): run it, expect it to fail. If it fails, the result is `XFAIL` and the run stays green. If it unexpectedly **passes**, with `strict=True` PyTest reports it as a failure (`XPASS(strict)`), signalling "the bug was fixed; remove this mark". That makes `xfail(strict=True)` an excellent way to document a **known defect** with its ticket number in `reason`, and to be notified automatically when it is fixed.
- The ID for the `007` case is `007` (auto) because we did not give an `id`; you can combine `id=` and `marks=` in the same `pytest.param`.

(The bug number `BUG-123` and the leading-zero behaviour are fictional, used here only to demonstrate the mechanism on our mock server.)

### 14. Parametrized Fixtures and Indirect Parametrization (Brief)

Two related features appear in real codebases; here is just enough to recognise them.

**Fixtures can take parameters.** Give `@pytest.fixture` a `params` list; every test that uses the fixture runs once per value, and the current value is `request.param`:

```python
@pytest.fixture(params=["application/json", "application/json; charset=utf-8"])
def accept_header(request):
    return request.param


def test_accept_variants(client, accept_header):
    r = client.get("/posts/1", headers={"Accept": accept_header})
    assert r.status_code == 200
```

Output (local run): two tests, `test_accept_variants[application/json]` and `test_accept_variants[application/json; charset=utf-8]`, both passing. Use it when the *same variation* should apply to many tests.

**Indirect parametrization** (`@pytest.mark.parametrize("user", [1, 2], indirect=True)`) routes each value through the fixture of the same name, arriving as `request.param`, so the fixture can turn a short key (a user ID) into a heavier object for the test. It is an advanced tool; a factory fixture inside an ordinary parametrized test does the same more readably. We verified it locally (two passing tests) but will not use it further.

> **Coming Wednesday.** Wednesday's lessons on data-driven API testing and CSV/JSON parametrization cover loading test cases from external files, plus mocking and test isolation. Today you only need literal lists written inside the test file.

### 15. Combining Fixtures and Parametrization

The real power comes from using both in one test: **fixtures supply the world, parameters supply the variations.**

```python
# tests/test_q_solutions.py (excerpt)
@pytest.mark.parametrize("title", ["Hello", "x" * 200, "Ünïcödé ✓"], ids=["short", "long-200", "unicode"])
def test_created_title_round_trips(post_factory, client, title):
    post = post_factory(title=title)
    fetched = client.get(f"/posts/{post['id']}")
    assert fetched.status_code == 200
    assert fetched.json()["title"] == title
```

For the `[unicode]` case PyTest sets `title`, builds the session `client` (if needed) and the function-scoped `post_factory`; the test creates a post, fetches it, and asserts the title survived the round trip (a useful check for encoding bugs); then the factory's teardown deletes the post even if an assertion failed.

Three parameter values, three independent tests, three created posts, three cleanups, written once. The leak detector afterwards still passes (local run: `20 passed`, including the detector). This is the combination to reach for on Project 2: **a factory for data, parametrize for variations, a shared client for transport.**

### 16. A Complete Real-World Scenario

Put it together as you would for Project 2. Requirement: *"Users can create, read and delete posts; invalid IDs return 404; unauthenticated `/me` returns 401."* The root `conftest.py` from sections 8 to 9 holds the fixtures; register custom marks (`smoke`, `regression`, `negative`) under `markers =` in `pytest.ini` so PyTest does not warn about them. The tests are short because the fixtures carry the plumbing:

```python
# tests/test_posts_crud.py
import pytest


@pytest.mark.smoke
def test_list_posts(client):
    assert client.get("/posts").status_code == 200


@pytest.mark.regression
def test_created_post_has_expected_fields(created_post):
    assert {"id", "title", "body", "userId"} <= created_post.keys()


@pytest.mark.regression
def test_delete_post(client, post_factory):
    post = post_factory(title="to delete")
    assert client.delete(f"/posts/{post['id']}").status_code == 200
    assert client.get(f"/posts/{post['id']}").status_code == 404
```

`{"id", "title", "body", "userId"} <= created_post.keys()` uses `<=` as "is a subset of", so it says "all four fields are present". `test_delete_post` shows a subtle overlap: the test deletes the post itself, then the factory's teardown deletes it again and gets `404`. Our factory ignores the response, so nothing breaks (local run: passed, leak detector clean). **Make cleanup tolerant of "already gone", and never assert inside teardown.**

Select by mark: `pytest -m smoke`, `pytest -m "not negative"`, `pytest -m regression -v`. If login moves to `/auth/token`, you edit one fixture, not every test. That is the payoff of this lesson.

### 17. Design Guidelines for Good Fixtures

1. **One responsibility per fixture;** compose them.
2. **Name fixtures as nouns** (`created_post`, `auth_client`).
3. **Write a one-line docstring** on shared fixtures; `pytest --fixtures` displays it.
4. **Fixtures prepare; tests judge.** Light "setup worked" assertions are fine.
5. **Make teardown tolerant:** no status-code assertions, no failure if the record is already gone.
6. **Narrow scope by default; widen with evidence,** only for expensive, read-only values.
7. **Read configuration from the environment inside fixtures,** never at import time. On Friday a GitLab pipeline will inject `API_BASE_URL` and credentials this way, and guaranteed teardown matters because nobody watches a pipeline.

### 18. Pitfall 1: Mutable Shared State

**If a fixture's value is shared and a test changes it, every later test sees the change.** Results then depend on run order, the root of many flaky suites.

```python
# tests/test_f_shared.py
import pytest


@pytest.fixture(scope="module")
def shared_cart():
    return []


def test_add_item(shared_cart):
    shared_cart.append("book")
    assert shared_cart == ["book"]


def test_cart_starts_empty(shared_cart):
    assert shared_cart == []
```

Output (local run):

```text
.F                                                                       [100%]
shared_cart = ['book']

>       assert shared_cart == []
E       AssertionError: assert ['book'] == []
E         Left contains one more item: 'book'

FAILED tests/test_f_shared.py::test_cart_starts_empty - AssertionError: asser...
1 failed, 1 passed in 0.02s
```

`test_add_item` mutated the module-wide list, so the second test inherited `['book']`. Run `test_cart_starts_empty` alone (`pytest -k starts_empty`) and it passes. **Passes alone, fails in the suite** is the signature of shared state.

The same trap with a real client. A session-scoped `client` is shared; one test sets a header on it:

```python
# tests/test_n_hdr.py
def test_a_logs_in_by_mutating(client):
    client.session.headers["Authorization"] = "Bearer tok-abc-123"
    assert client.get("/me").status_code == 200


def test_b_expects_anonymous(client):
    assert client.get("/me").status_code == 401
```

```text
FAILED tests/test_n_hdr.py::test_b_expects_anonymous - AssertionError: assert...
1 failed, 1 passed in 0.03s
```

`test_a` left its header on the shared session, so `test_b`'s "anonymous" request was silently authenticated. That is why section 8's `auth_client` builds a **new** client per test. Fixes, in order of preference: (1) function-scoped fixtures or factories for anything mutable; (2) share only immutable values (strings, numbers) at wide scope; (3) undo changes in teardown; (4) pass per-request `headers=` instead of mutating the session. If two fixtures hand the **same** dictionary to different consumers, a change by one is visible to the other; use `{**original}` or `copy.deepcopy(...)` for independence.

### 19. Pitfall 2: Scope Mismatch, Leaks, Order Dependence

Scope mismatch (section 6.3) appears when you widen a fixture whose dependencies are narrow. Leaked data (section 8.2) hides in forgotten teardown or cleanup at the end of a test body. Order dependence also arises when a test relies on data another test created ("update post 101"): every test should **create its own data**. A failing teardown gives `ERROR at teardown` even if the test passed, so keep it simple and assertion-free. When a fixture misbehaves: read the first error line (`not found` = naming, `ScopeMismatch` = scope, `ERROR at setup` = fixture bug, `FAILED` = test), run the test alone, then add `--setup-show` and `--fixtures`.

### 20. Common Mistakes (With Fixes)

1. **Calling a fixture like a function.** `created_thing()` inside a test fails (local output):

   ```text
   _______________________________ test_direct_call _______________________________
   Fixture "created_thing" called directly. Fixtures are not meant to be called directly,
   but are created automatically when test functions request them as parameters.
   ```

   Fix: request it as a parameter, or write a factory fixture (section 9) if you need a callable.

2. **Misspelling the fixture name.** For `def test_typo(created_thng)` (local output, trimmed):

   ```text
   ERROR at setup of test_typo
   E       fixture 'created_thng' not found
   >       available fixtures: anyio_backend, ..., auth_client, auth_token, base_url, ..., client, created_post, created_thing, ...
   ```

   PyTest lists every available fixture; compare your spelling. (Your list differs with installed plugins.)

3. **Wide scope on mutable data.** See section 18. Default to function scope.
4. **Product assertions inside fixtures.** A failure shows as ERROR instead of FAILED and blurs triage.
5. **Parametrize names that do not match the signature.** Local output: `function uses no argument 'user'` at collection time.
6. **Teardown that trusts a value the test may have changed.** Save what teardown needs in a separate variable before `yield` (`post_id = post["id"]`).
7. **Cleanup at the end of the test body** instead of a `yield` fixture; it is skipped when an assertion fails first.
8. **Importing from `conftest.py`** (`from conftest import client`). Let PyTest inject.
9. **Autouse for everything.** Readers cannot see what happens.
10. **Reading environment variables at import time,** which `monkeypatch` cannot change. Read inside functions or fixtures.
11. **Stacking many `parametrize` decorators;** combinations multiply (section 13.4).
12. **Hard-coded real credentials.** Read from the environment; this lesson's throwaway defaults exist only for the local mock.

### 21. Practice Exercises (With Solutions)

Try each yourself first. Solutions ran against the local mock server unless stated.

**Exercise 1: Move plumbing into `conftest.py`.** Put `base_url` (session) and `client` (session, `yield` + `close()`) from section 8 into a root `conftest.py` and refactor an earlier test to request `client`. Verify with `--setup-show` that `SETUP S client` appears once at the start and `TEARDOWN S client` at the end.

**Exercise 2: A cleanup fixture.** Write `created_post` (section 8.1), use it in two tests, and run `--setup-show`. Expected: two `SETUP F created_post` / `TEARDOWN F created_post` pairs (function scope) while `client` is set up once. Add the leak detector to confirm no leftovers.

**Exercise 3: Parametrize over IDs.** Parametrize a test over post IDs 1 to 5 and check each post's `userId` is between 1 and 10.

*Solution.*

```python
@pytest.mark.parametrize("post_id", [1, 2, 3, 4, 5])
def test_post_user_id_in_range(client, post_id):
    post = client.get(f"/posts/{post_id}").json()
    assert 1 <= post["userId"] <= 10
```

`1 <= x <= 10` is a valid chained comparison (inclusive). Local result: five tests `[1]` to `[5]`, all passed.

**Exercise 4: Use the factory.** Create three posts titled `"A"`, `"B"`, `"C"` with `post_factory`; assert the IDs are distinct and titles stored in order.

*Solution.*

```python
def test_factory_three_posts(post_factory):
    posts = [post_factory(title=t) for t in ("A", "B", "C")]
    ids = [p["id"] for p in posts]
    assert len(set(ids)) == 3
    assert [p["title"] for p in posts] == ["A", "B", "C"]
```

`set(ids)` removes duplicates, so length 3 proves all IDs differ. One teardown deletes all three. Passed locally; the leak detector stayed clean.

**Exercise 5: Negative boundary table.** Parametrize a negative test for `GET /users/{id}` with six invalid IDs (letters, negative, zero, huge, encoded space, special characters), with readable IDs. Record what your API returns for each.

*Solution.*

```python
@pytest.mark.negative
@pytest.mark.parametrize(
    "bad_id",
    [
        pytest.param("abc", id="letters"),
        pytest.param("-1", id="negative"),
        pytest.param("0", id="zero"),
        pytest.param("99999999999", id="huge"),
        pytest.param("%20", id="space-encoded"),
        pytest.param("%3Cscript%3E", id="special-chars"),
    ],
)
def test_user_invalid_ids(client, bad_id):
    assert client.get(f"/users/{bad_id}").status_code == 404
```

The local mock returned `404` for all six. A different API may return `400` for malformed IDs (`abc`) and `404` for well-formed-but-missing ones; *record* real behaviour and compare it with the documentation, because a mismatch is a defect to report. `%3Cscript%3E` is a URL-encoded `<script>` probe.

**Exercise 6: Scope in your own words.** When would you choose `session` over `function`?

*Model answer.* `session` when the fixture is **expensive** and tests never modify it (a token, a base URL); `function` when tests may change it, so each starts clean. When in doubt, use `function` and widen only if the suite is measurably slow.

**Exercise 7: Find and fix two bugs** without running the code first.

```python
@pytest.fixture(scope="session")
def admin_client(auth_client):
    auth_client.session.headers["X-Role"] = "admin"
    return auth_client
```

*Solution.* (a) `admin_client` is session scoped but requests the function-scoped `auth_client`: `ScopeMismatch`. (b) It mutates a client's headers; if the scope were widened to make it legal, every test would share the "admin" header. Fix: function scope and a new client.

```python
@pytest.fixture
def admin_client(base_url, auth_token):
    c = ApiClient(base_url)
    c.session.headers["Authorization"] = f"Bearer {auth_token}"
    c.session.headers["X-Role"] = "admin"
    yield c
    c.close()
```

**Exercise 8: Marks on one case.** Add a case to Exercise 5 that you believe is a bug, mark it `xfail(strict=True)` with a ticket-style reason, and confirm the run stays green and the reason prints with `-rx`.

*Solution.* Add `pytest.param("007", marks=pytest.mark.xfail(reason="BUG-123: leading zeros accepted", strict=True), id="leading-zeros")` and run `pytest -rx`: you should see an `XFAIL` line with the reason, and `strict=True` will flag the case if the API is fixed.

### 22. Self-Check Quiz

Answer without looking back, then check underneath.

1. A test has a parameter called `client`. What does PyTest do?
2. When does code after `yield` run, and does it run if the test fails?
3. What is the difference between `ERROR at setup` and `FAILED`?
4. A `session` fixture requests a `function` fixture. What happens?
5. Where must a fixture live so every test can use it with no imports?
6. What does `@pytest.mark.parametrize("a, b", [(1, 2), (3, 4)])` produce?
7. Stacking `parametrize("x", [1,2,3])` over `parametrize("y", [10,20])` runs how many tests?
8. What is a factory fixture, and what makes its teardown reliable?
9. What does `--setup-show` print, and what do `S` and `F` mean?
10. Why avoid `autouse=True` on data-creating fixtures?
11. How do you mark one parametrized case as a known bug without turning the run red?

**Answers.**

1. It finds the fixture named `client`, runs it (dependencies first), and passes its returned or yielded value to the test.
2. After the test; yes, even on failure (but not if setup raised before the `yield`; use `try/finally` for multi-step setup).
3. `ERROR at setup` means a fixture raised and the test never ran: usually an environment problem. `FAILED` means the test ran and the behaviour was wrong: a candidate product defect.
4. `ScopeMismatch`. Wide fixtures can depend only on equal-or-wider fixtures.
5. In a `conftest.py` at or above the tests' directory, such as the project root. Do not import from it.
6. Two tests, `a=1, b=2` and `a=3, b=4`, with IDs `[1-2]` and `[3-4]`.
7. Six (3 x 2).
8. A fixture that returns a function creating items on demand. It records every created ID in a list and deletes them all after the `yield`.
9. Each fixture's setup and teardown in order, indented by nesting. `S` is session scope, `F` function (`M` module, `C` class).
10. It runs invisibly for every test and a cleanup bug leaks data everywhere; request data fixtures explicitly.
11. `pytest.param(value, marks=pytest.mark.xfail(reason="BUG-123: ...", strict=True))`.

### 23. Glossary

- **Fixture**: a function decorated with `@pytest.fixture` that provides setup (and optional teardown) and is requested by naming it as a test parameter.
- **Dependency injection**: receiving what you need from outside instead of building it; PyTest injects fixtures by parameter name.
- **Setup / teardown**: preparation before a test and cleanup after it; the code before and after `yield`.
- **Scope**: how long a fixture's value lives: `function`, `class`, `module`, `session` (and `package`).
- **`conftest.py`**: a specially named file whose fixtures reach every test in its directory tree, without imports.
- **Factory fixture**: a fixture returning a function so a test can create many items, all cleaned up at teardown.
- **`autouse`** runs a fixture for every test in scope without a request; **`usefixtures`** requests one for its side effect only.
- **`request`**: built-in fixture exposing the requesting test (`request.node`) and the current parameter (`request.param`).
- **ScopeMismatch**: the error when a wider-scoped fixture depends on a narrower one.
- **Parametrization**: running one test with several input values, each reported as its own test. A **test ID** is its bracketed label (`[1-Leanne Graham]`), set by `id=` or `ids=`.
- **`pytest.param`**: wraps one case so you can attach an `id` and `marks`.
- **Cartesian product**: every combination of values from stacked `parametrize` decorators.
- **`xfail` / `skip`**: "expected to fail" (run, tolerate failure) and "do not run".
- **Indirect parametrization**: sending a parametrized value through a fixture (`indirect=True`).
- **Mutable shared state / order dependence / flaky test**: a changeable shared object, causing results that depend on what ran earlier.
- **Leak**: a record or resource created by a test and never removed.

---

## Summary

- A **fixture** is reusable setup (and teardown via `yield`) that PyTest injects into a test by matching the parameter name. Never call fixtures yourself.
- Teardown after `yield` runs even when the test fails. A fixture that raises reports as **ERROR**, a failing assertion as **FAILED**; use that difference to triage.
- **Scopes** (`function`, `class`, `module`, `session`) control how often a fixture is rebuilt. Use the narrowest practical scope; widen only for expensive, read-only values. Wide fixtures cannot depend on narrower ones (`ScopeMismatch`). Teardown runs in reverse order of setup.
- `conftest.py` shares fixtures automatically; the closest definition wins; fixtures chain by requesting other fixtures.
- The API toolkit for Project 2: `base_url`, a shared `client`, a session `auth_token`, a per-test `auth_client`, a self-cleaning `created_post`, and a `post_factory` that records and deletes everything it creates.
- Built-ins: `tmp_path`, `monkeypatch` (auto-undone), `capsys`, `request`. Debug with `pytest --fixtures` and `pytest --setup-show`.
- Avoid hidden `autouse`, shared mutable state, leaked data, calling fixtures directly, and import-time configuration.
- `@pytest.mark.parametrize` runs one test body over literal inputs: tuples for multiple parameters, `pytest.param(..., id=...)` for readable names, stacking for combinations, `marks=` for per-case `xfail`/`skip`.
- Fixtures prepare, tests judge; each test creates its own data and cleans up.
- Wednesday covers data-driven API testing with external CSV/JSON files, plus mocking and test isolation.

## Additional Resources

- PyTest documentation, *About fixtures*: https://docs.pytest.org/en/stable/explanation/fixtures.html
- PyTest documentation, *How to use fixtures* (scopes, teardown, factories, autouse, `conftest.py`): https://docs.pytest.org/en/stable/how-to/fixtures.html
- PyTest documentation, *How to parametrize fixtures and test functions*: https://docs.pytest.org/en/stable/how-to/parametrize.html
- PyTest documentation, *Fixtures reference* (every fixture option and the built-in fixtures list): https://docs.pytest.org/en/stable/reference/fixtures.html
- PyTest documentation, *How to use temporary directories and files in tests* (`tmp_path`): https://docs.pytest.org/en/stable/how-to/tmp_path.html
- PyTest documentation, *How to monkeypatch/mock modules and environments*: https://docs.pytest.org/en/stable/how-to/monkeypatch.html
- PyTest documentation, *How to use skip and xfail*: https://docs.pytest.org/en/stable/how-to/skipping.html
