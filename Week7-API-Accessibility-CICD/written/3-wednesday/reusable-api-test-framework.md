# Building a Reusable API Test Framework

## Learning Objectives

By the end of this lesson you will be able to:

- Explain what a reusable test framework is and what it costs a team when one is missing.
- Design a layered architecture (config, client, endpoints, models, data, tests, utils) and lay out its project tree.
- Configure base URL, timeouts and environments (dev, stage) through environment variables.
- Build an `ApiClient` around `requests.Session` with timeouts, retries, logging and auth injection.
- Write service classes (`UsersApi`, `PostsApi`) and a response wrapper with helper assertions.
- Integrate Pydantic validation, CSV data-driven tests, fixtures, markers and a mock/live switch.
- Produce JUnit and HTML reports, write a README, and recognise framework anti-patterns.

---

## Why This Matters

This is the capstone of Week 7's epic: turning a pile of API tests into a **pipeline-ready framework**. Over Monday, Tuesday and the earlier Wednesday lessons you collected the parts: raw `requests` calls, status-code and header checks, authentication, schema validation, test isolation, data-driven tests and mocks. Today you assemble them.

Picture the alternative. A team has 200 API tests. Each one builds its own URL, sets its own headers, logs in by itself and checks the body in its own style. Then the API moves from `/users` to `/v2/users` and adds a mandatory header. Someone must edit 200 places, misses eleven, and a red build now means "maybe the test is wrong". A new hire copies the oldest test they can find, so old mistakes spread. After a few months nobody trusts the suite and people stop running it.

A framework fixes this by giving every concern **one home**. A URL change is a one-line edit. A new test is five lines of intent. Switching from dev to stage is one environment variable. Friday's lesson runs this same suite in a CI pipeline; today we build something that is ready for it.

---

## The Concept

### What a reusable framework is

A **test framework** is not a library you install. It is the agreed arrangement of folders, classes, fixtures and conventions your team uses so that tests stay small and infrastructure stays in one place.

*Why bother?* Because test code is code. It has to be read, changed and debugged, usually by someone who did not write it. The qualities you want:

| Quality | What it means | Sign you have it |
|---|---|---|
| Reusable | Many tests share one component | No copy-pasted request code |
| Maintainable | Each concern changes in one place | URL change touches one file |
| Readable | Tests state intent | A manual tester can follow a test |
| Configurable | Environment comes from settings | Same code runs on dev, stage, CI |
| Isolated | Tests do not depend on each other | Random order passes |
| Observable | Failures are diagnosable | Logs and reports explain what happened |
| Extensible | New endpoints are cheap | A new service class takes minutes |

*When to build it:* from the start, but only the layers you need today. Two endpoints do not need ten classes. Grow the structure when the second or third endpoint shows you a pattern.

### The layered architecture

Each layer has **one job** and only talks to the layer beneath it.

```
tests/        WHAT to verify      (scenarios, business language)
conftest.py   HOW it is wired     (fixtures, hooks)
api/endpoints WHICH operations    (UsersApi, PostsApi)
api/client    HOW to talk HTTP    (session, retry, logging, auth)
api/response  HOW to judge a reply (helper assertions)
models/       WHAT shape is valid (Pydantic schemas)
config/       WHERE to talk to    (base URL, timeouts, environments)
data/ utils/  WITH what inputs    (CSV files, loaders, mock server)
```

The rule that keeps this honest: **dependencies point downwards**. A test may use a service; a service may use the client; the client must never import a test or a service. If you find the client importing something from above, a responsibility is in the wrong layer.

### The project tree

```
jsonplaceholder-framework/
├── README.md
├── requirements.txt
├── pytest.ini
├── conftest.py
├── config/
│   ├── __init__.py
│   └── settings.py
├── api/
│   ├── __init__.py
│   ├── client.py
│   ├── response.py
│   └── endpoints/
│       ├── __init__.py
│       ├── users.py
│       └── posts.py
├── models/
│   ├── __init__.py
│   └── schemas.py
├── data/
│   └── posts_create.csv
├── utils/
│   ├── __init__.py
│   ├── data_loader.py
│   └── mock_server.py
├── tests/
│   ├── test_users.py
│   ├── test_posts.py
│   └── test_client.py
└── reports/              (generated, git-ignored)
```

Naming conventions follow from the tree: one module per resource, `test_<resource>.py` for tests, `<Resource>Api` for service classes, `snake_case` functions, and test names that read as sentences (`test_unknown_post_returns_404`).

### Layer 1: configuration

*What:* every value that differs between machines or environments. *Why:* so you never edit code to change where tests point. *How:* read environment variables, fall back to safe defaults.

```python
import os
from dataclasses import dataclass

ENVIRONMENTS = {
    "dev": "https://jsonplaceholder.typicode.com",
    "stage": "https://stage.example.com",
}


@dataclass(frozen=True)
class Settings:
    env: str
    base_url: str
    timeout: float
    retries: int
    mode: str
    token: str | None


def load_settings() -> Settings:
    env = os.getenv("TEST_ENV", "dev")
    if env not in ENVIRONMENTS:
        raise ValueError(f"Unknown TEST_ENV '{env}'. Use one of {sorted(ENVIRONMENTS)}")
    return Settings(
        env=env,
        base_url=os.getenv("API_BASE_URL", ENVIRONMENTS[env]),
        timeout=float(os.getenv("API_TIMEOUT", "5")),
        retries=int(os.getenv("API_RETRIES", "0")),
        mode=os.getenv("TEST_MODE", "mock"),
        token=os.getenv("API_TOKEN") or None,
    )


settings = load_settings()
```

Line by line: `ENVIRONMENTS` maps a friendly name to a URL. `@dataclass(frozen=True)` creates a read-only bag of named values, so a test cannot quietly change configuration (that would be hidden state). `os.getenv(name, default)` returns the variable or the default. Unknown environments fail immediately with a helpful message instead of a confusing connection error later. The token comes only from the environment, never from code. The bottom line builds one shared `settings` object at import time.

### Layer 2: the client

*What:* the only place that knows about HTTP mechanics. *Why:* so timeouts, logging and auth are written once. *How:* wrap a `requests.Session` (Monday's lesson: a session reuses connections and carries default headers).

```python
import logging
import time

import requests

from api.response import ApiResponse

log = logging.getLogger("api")
RETRY_STATUSES = {502, 503, 504}
IDEMPOTENT = {"GET", "HEAD", "PUT", "DELETE", "OPTIONS"}


class ApiClient:
    def __init__(self, base_url, timeout=5.0, retries=0, token=None, backoff=0.2):
        self.base_url = base_url.rstrip("/")
        self.timeout = timeout
        self.retries = retries
        self.backoff = backoff
        self.session = requests.Session()
        self.session.headers["Accept"] = "application/json"
        if token:
            self.session.headers["Authorization"] = f"Bearer {token}"

    def request(self, method, path, **kwargs):
        method = method.upper()
        url = f"{self.base_url}/{path.lstrip('/')}"
        kwargs.setdefault("timeout", self.timeout)
        attempts = 1 + (self.retries if method in IDEMPOTENT else 0)

        for attempt in range(1, attempts + 1):
            log.info("%s %s params=%s json=%s", method, url,
                     kwargs.get("params"), kwargs.get("json"))
            try:
                raw = self.session.request(method, url, **kwargs)
            except (requests.ConnectionError, requests.Timeout) as exc:
                log.warning("attempt %d/%d failed: %s", attempt, attempts, exc)
                if attempt == attempts:
                    raise
                time.sleep(self.backoff * attempt)
                continue
            log.info("-> %s", raw.status_code)
            if raw.status_code in RETRY_STATUSES and attempt < attempts:
                log.warning("retrying after %s (attempt %d/%d)", raw.status_code, attempt, attempts)
                time.sleep(self.backoff * attempt)
                continue
            return ApiResponse(raw)

    def get(self, path, **kw):    return self.request("GET", path, **kw)
    def post(self, path, **kw):   return self.request("POST", path, **kw)
    def put(self, path, **kw):    return self.request("PUT", path, **kw)
    def delete(self, path, **kw): return self.request("DELETE", path, **kw)
```

Walkthrough:

- `__init__` stores settings and creates the session. If a token is given, the `Authorization` header is **injected once** into the session, so every later call carries it. No test ever builds an auth header.
- `base_url.rstrip("/")` and `path.lstrip('/')` make `"/users"` and `"users"` both work and avoid `//` in URLs.
- `kwargs.setdefault("timeout", ...)` guarantees every call has a timeout. Without one, `requests` can wait forever and a hung API hangs your whole pipeline.
- `attempts` is `1 + retries`, but **only for idempotent methods** (Monday: repeating a `GET` is harmless; repeating a `POST` can create duplicates, so POST never retries).
- The `try/except` retries network-level failures; the status check retries temporary gateway errors (502/503/504). Real client errors like 400 or 404 are never retried: they are answers, not glitches.
- Every retry is **logged as a warning**. A silent retry would hide a flaky server.
- The method returns `ApiResponse`, our wrapper, instead of the raw object.
- The four one-line helpers keep service classes tidy.

**Scenario.** Stage is deployed while your suite runs, and one `GET /users/1` returns 503 for two seconds. With `API_RETRIES=2` the test passes and the log shows two warnings, so you can still tell the team stage was shaky. With retries off by default, local runs stay strict.

### Layer 3: service (endpoint) classes

*What:* one small class per resource, with one method per operation. *Why:* tests should speak in business actions (`posts.create(...)`), not URL strings. This is the API twin of the Page Object Model from UI testing.

```python
class PostsApi:
    PATH = "/posts"

    def __init__(self, client):
        self.client = client

    def list(self, **params):
        return self.client.get(self.PATH, params=params or None)

    def get(self, post_id):
        return self.client.get(f"{self.PATH}/{post_id}")

    def create(self, payload):
        return self.client.post(self.PATH, json=payload)
```

`PATH` is the single place the resource address lives. The client arrives through the constructor (**composition**: the service *has a* client, it does not *inherit from* one). `list(**params)` turns keyword arguments into a query string, so `posts.list(userId=1)` means `GET /posts?userId=1`. `params or None` avoids sending an empty query.

Notice what is **absent**: no `assert`, no status checks. Services perform operations and return responses. Tests decide what is correct.

### The response wrapper

*What:* a thin class around `requests.Response` that adds readable assertions. *Why:* a good failure message saves minutes every time a test fails, and the message is written once.

```python
from pydantic import ValidationError


class ApiResponse:
    def __init__(self, raw):
        self.raw = raw

    @property
    def status_code(self):
        return self.raw.status_code

    def json(self):
        return self.raw.json()

    def assert_status(self, expected):
        assert self.status_code == expected, (
            f"Expected {expected} but got {self.status_code} for "
            f"{self.raw.request.method} {self.raw.url}\nBody: {self.raw.text[:300]}"
        )
        return self

    def assert_header_contains(self, name, text):
        value = self.raw.headers.get(name, "")
        assert text in value, f"Header {name}='{value}' does not contain '{text}'"
        return self

    def parse(self, model):
        try:
            return model.model_validate(self.json())
        except ValidationError as exc:
            raise AssertionError(f"Response does not match {model.__name__}:\n{exc}") from exc

    def parse_list(self, model):
        return [self._one(model, item) for item in self.json()]

    @staticmethod
    def _one(model, item):
        try:
            return model.model_validate(item)
        except ValidationError as exc:
            raise AssertionError(f"Item does not match {model.__name__}:\n{exc}") from exc
```

Key idea: `assert_status` **returns `self`**, so checks chain: `posts.get(1).assert_status(200).parse(Post)`. The failure message includes method, URL and the first 300 characters of the body, which is usually all you need to diagnose a failure without re-running. `parse` converts a Pydantic `ValidationError` into an `AssertionError` so pytest reports it as a test failure with a readable list of violations, not as a crash.

### Models and schema validation

*What:* Pydantic classes that describe the shape of valid data. *Why:* one `parse(User)` call checks field presence and types, replacing dozens of hand-written asserts, and the models are reusable for building payloads too.

```python
from pydantic import BaseModel


class User(BaseModel):
    id: int
    name: str
    username: str
    email: str


class Post(BaseModel):
    userId: int
    id: int
    title: str
    body: str
```

Fields are required unless given a default; a wrong type (`id` arriving as `"abc"`) fails validation. Extra fields the API adds later are ignored by default, which suits tolerant contract checks. *Common choice:* use JSON Schema files if other tools consume them, Pydantic if the models are Python-only. Either way, keep them in `models/` so tests never define shapes inline.

### Data-driven tests and the data folder

Test inputs live in files, not inside tests. A small loader keeps this uniform:

```python
import csv
from pathlib import Path

DATA_DIR = Path(__file__).resolve().parent.parent / "data"


def load_csv(name):
    with open(DATA_DIR / name, newline="", encoding="utf-8") as f:
        return list(csv.DictReader(f))
```

`Path(__file__)` anchors the folder to the code, not to wherever pytest was launched, so the suite works from any directory. `csv.DictReader` yields one dictionary per row, keyed by the header. Adding a case becomes adding a line to a CSV, which a non-programmer can do.

### Fixtures and `conftest.py`

Fixtures wire layers together so tests simply ask for what they need. Keep `session` scope for **read-only, shared** things (settings, the client). Anything that creates data stays `function`-scoped, the isolation rule from earlier this week.

A `conftest.py` in the project root is picked up by every test below it. Keep it short: it should only assemble objects, never contain test logic.

### Markers and `pytest.ini`

Markers label tests so you can run slices: `smoke` (a minute, answers "is it alive?"), `regression` (full coverage), `mocked` (needs the mock server). `--strict-markers` turns a typo like `@pytest.mark.smok` into an error instead of a silently unselected test.

### The mock/live switch

Mocking (earlier this week) lets tests run without a network. The framework turns it into a **switch**: `TEST_MODE=mock` (default) intercepts HTTP with the `responses` library and serves canned answers; `TEST_MODE=live` lets requests go to the real API. The tests are identical in both modes. That gives you fast, deterministic runs on a laptop and the same tests as a real check against dev or stage.

*Why default to mock?* A new colleague's first run must succeed offline. *When to use live:* before release, and to confirm that your mock still matches reality (a mock that drifts from the real API gives false confidence).

### Reporting and logging basics

- `--junitxml=reports/junit.xml` writes machine-readable results that CI tools parse.
- `pytest-html` adds `--html=reports/report.html --self-contained-html`, a single human-friendly page.
- `log_file` and `log_file_level = DEBUG` save the client's request/response log for every run, while the console stays quiet. When a test fails, open the log: it shows exactly which calls were sent.

Running this suite in a CI pipeline and publishing these files is covered Friday.

### Anti-patterns

1. **The God client.** One class with `get_user`, `create_post`, `delete_comment` and hundreds more methods. It changes for every reason and nobody can find anything. *Fix:* the client knows HTTP; one service class per resource knows operations.
2. **Test logic in the client.** `client.get_user()` that asserts the status or fails the test itself. Now the client decides what "correct" means and cannot be used for negative tests (where a 404 is the *expected* result). *Fix:* clients and services return responses; tests assert.
3. **Hidden state.** Module-level variables like `LAST_CREATED_ID`, a client that remembers the last response, or a test that relies on data another test made. Failures then depend on order. *Fix:* pass data through fixtures and return values; keep shared objects read-only (`frozen=True`).
4. **Inheritance towers** (`BaseClient > AuthClient > AdminClient`). *Fix:* composition and a token argument.
5. **Silent retries** that make flaky servers look healthy. *Fix:* log every retry, default to zero.
6. **Over-engineering** before you have two examples of a pattern.

### Extensibility without duplication

Adding an endpoint, say `CommentsApi`, should touch **no existing class**:

1. Add a model in `models/schemas.py`.
2. Add `api/endpoints/comments.py` with `CommentsApi`.
3. Add a `comments` fixture in `conftest.py`.
4. Add data files under `data/` if needed.
5. Write `tests/test_comments.py` with markers.

If step 2 forces edits to `ApiClient`, the client is doing too much. Duplication also hides in tests: when you paste the same three lines into a third test, move them into a fixture or a service helper.

### README and onboarding

The README is the framework's front door. Measure it by one question: can a new engineer run a passing test in ten minutes using only this page? Include:

- **Quick start:** create venv, `pip install -r requirements.txt`, `pytest -m smoke`.
- **Configuration table:** every environment variable, default and meaning (`TEST_ENV`, `TEST_MODE`, `API_BASE_URL`, `API_TIMEOUT`, `API_RETRIES`, `API_TOKEN`).
- **Common commands:** `pytest`, `pytest -m smoke`, `TEST_MODE=live pytest`, `TEST_ENV=stage pytest`.
- **Structure:** one line per folder.
- **How to add a test / endpoint:** the five steps above.
- **Conventions and reports:** naming, markers, where reports land.

### Glossary

- **Framework:** shared structure and conventions for writing tests.
- **Layer:** a group of code with one responsibility.
- **Service / endpoint class:** a class with one method per API operation of a resource.
- **Client:** the object that performs HTTP calls.
- **Session:** a `requests` object reusing connections and default headers.
- **Idempotent:** repeating the call has the same effect as making it once (GET, PUT, DELETE).
- **Fixture:** a pytest function that supplies setup objects to tests.
- **Marker:** a label on a test used to select or group it.
- **Mock:** a stand-in that returns canned responses instead of calling the real service.
- **Contract / schema:** the agreed shape of a request or response.
- **Composition:** building behaviour by holding other objects rather than inheriting.
- **Artifact:** a file produced by a run, such as a report.

---

## Worked Example: A Complete Small Framework for JSONPlaceholder

Below is the whole thing. Files already shown above (`settings.py`, `client.py`, `response.py`, `PostsApi`, models, loader) are used exactly as written, saved at the paths in the tree. The remaining files follow.

**`requirements.txt`**

```
pytest
requests
responses
pydantic>=2
pytest-html
```

**`pytest.ini`**

```ini
[pytest]
testpaths = tests
addopts = -ra --strict-markers --tb=short --junitxml=reports/junit.xml --html=reports/report.html --self-contained-html
markers =
    smoke: quick health checks
    regression: full functional coverage
    mocked: tests that need the mock server
log_file = reports/test.log
log_file_level = DEBUG
```

**`api/endpoints/users.py`**

```python
class UsersApi:
    PATH = "/users"

    def __init__(self, client):
        self.client = client

    def list(self):
        return self.client.get(self.PATH)

    def get(self, user_id):
        return self.client.get(f"{self.PATH}/{user_id}")
```

**`data/posts_create.csv`**

```
title,body,user_id
First post,Hello world,1
Accent é title,Body with unicode ✓,2
Long body,Lorem ipsum dolor sit amet,3
```

**`utils/mock_server.py`**

```python
import json
import re
from urllib.parse import parse_qs, urlparse

import responses

USERS = {i: {"id": i, "name": f"User {i}", "username": f"user{i}",
             "email": f"user{i}@example.com"} for i in range(1, 11)}
POSTS = [
    {"userId": 1, "id": 1, "title": "first", "body": "b1"},
    {"userId": 1, "id": 2, "title": "second", "body": "b2"},
    {"userId": 2, "id": 3, "title": "third", "body": "b3"},
]


def _reply(status, body):
    return status, {"Content-Type": "application/json"}, json.dumps(body)


def install(rsps, base):
    b = re.escape(base)

    def user_by_id(request):
        uid = int(urlparse(request.url).path.rsplit("/", 1)[1])
        return _reply(200, USERS[uid]) if uid in USERS else _reply(404, {})

    def post_by_id(request):
        pid = int(urlparse(request.url).path.rsplit("/", 1)[1])
        found = [p for p in POSTS if p["id"] == pid]
        return _reply(200, found[0]) if found else _reply(404, {})

    def list_posts(request):
        query = parse_qs(urlparse(request.url).query)
        items = POSTS
        if "userId" in query:
            items = [p for p in POSTS if str(p["userId"]) == query["userId"][0]]
        return _reply(200, items)

    def create_post(request):
        return _reply(201, {**json.loads(request.body), "id": 101})

    rsps.add_callback(responses.GET, re.compile(rf"{b}/users(\?.*)?$"),
                      callback=lambda r: _reply(200, list(USERS.values())))
    rsps.add_callback(responses.GET, re.compile(rf"{b}/users/\d+$"), callback=user_by_id)
    rsps.add_callback(responses.GET, re.compile(rf"{b}/posts(\?.*)?$"), callback=list_posts)
    rsps.add_callback(responses.GET, re.compile(rf"{b}/posts/\d+$"), callback=post_by_id)
    rsps.add_callback(responses.POST, re.compile(rf"{b}/posts$"), callback=create_post)
```

Each `add_callback` says "when a request matches this method and URL pattern, call this function and use the `(status, headers, body)` tuple it returns". The regexes `(\?.*)?$` allow an optional query string. `re.escape(base)` stops the dots in the host name being treated as wildcards.

**`conftest.py`**

```python
import pytest
import responses

from api.client import ApiClient
from api.endpoints.posts import PostsApi
from api.endpoints.users import UsersApi
from config.settings import settings
from utils.mock_server import install


@pytest.fixture(scope="session", autouse=True)
def mock_api():
    if settings.mode != "mock":
        yield None
        return
    with responses.RequestsMock(assert_all_requests_are_fired=False) as rsps:
        install(rsps, settings.base_url)
        yield rsps


@pytest.fixture(scope="session")
def client(mock_api):
    return ApiClient(settings.base_url, settings.timeout, settings.retries, settings.token)


@pytest.fixture
def users(client):
    return UsersApi(client)


@pytest.fixture
def posts(client):
    return PostsApi(client)
```

How it works: `mock_api` is `autouse`, so it runs before any test. In mock mode the `with` block activates the interceptor for the whole session; the `yield` hands it to tests that want to inspect calls; leaving the block removes it. In live mode it yields `None` and nothing is intercepted. `client` depends on `mock_api` so ordering is guaranteed. `users` and `posts` are cheap, function-scoped service objects.

**`tests/test_users.py`**

```python
import pytest

from models.schemas import User


@pytest.mark.smoke
def test_user_1_matches_schema(users):
    user = users.get(1).assert_status(200).parse(User)
    assert user.id == 1


@pytest.mark.regression
def test_user_list_has_ten_valid_users(users):
    items = users.list().assert_status(200).parse_list(User)
    assert len(items) == 10
```

**`tests/test_posts.py`**

```python
import pytest

from models.schemas import Post
from utils.data_loader import load_csv

CASES = load_csv("posts_create.csv")


@pytest.mark.smoke
def test_posts_can_be_filtered_by_user(posts):
    items = posts.list(userId=1).assert_status(200).parse_list(Post)
    assert items and all(p.userId == 1 for p in items)


@pytest.mark.regression
def test_unknown_post_returns_404(posts):
    posts.get(9999).assert_status(404)


@pytest.mark.regression
@pytest.mark.parametrize("case", CASES, ids=[c["title"] for c in CASES])
def test_create_post_echoes_payload(posts, case):
    payload = {"title": case["title"], "body": case["body"], "userId": int(case["user_id"])}
    created = posts.create(payload).assert_status(201).parse(Post)
    assert created.title == case["title"]
```

**`tests/test_client.py`**

```python
import pytest
import responses

from api.client import ApiClient
from config.settings import settings


@pytest.fixture
def mocked(mock_api):
    if mock_api is None:
        pytest.skip("needs TEST_MODE=mock")
    return mock_api


@pytest.mark.mocked
def test_token_is_injected_into_every_request(mocked):
    ApiClient(settings.base_url, token="abc123").get("/users/1")
    assert mocked.calls[-1].request.headers["Authorization"] == "Bearer abc123"


@pytest.mark.mocked
def test_get_retries_on_503_then_succeeds(mocked):
    url = f"{settings.base_url}/flaky"
    mocked.add(responses.GET, url, status=503)
    mocked.add(responses.GET, url, status=503)
    mocked.add(responses.GET, url, json={"ok": True}, status=200)

    ApiClient(settings.base_url, retries=2, backoff=0).get("/flaky").assert_status(200)

    assert [c.request.url for c in mocked.calls].count(url) == 3
```

The second test registers three answers for the same URL; `responses` serves them in order. The client sees 503, 503, then 200 and must have made exactly three calls.

**Running it**

```
pip install -r requirements.txt
pytest                        # mock mode, no network needed
pytest -m smoke               # fast slice
TEST_MODE=live pytest -m "not mocked"   # real jsonplaceholder
TEST_ENV=stage TEST_MODE=live pytest    # another environment
```

Representative output (mock mode):

```
tests/test_client.py ..          [ 22%]
tests/test_posts.py .....        [ 77%]
tests/test_users.py ..           [100%]
9 passed in 0.1s
```

---

## Common Mistakes

1. **Hard-coding a URL in a test.** One slip and that test ignores `TEST_ENV`. Search your tests for `http` as a review habit.
2. **Forgetting `__init__.py`** in packages, or running pytest from the wrong directory, giving `ModuleNotFoundError`. Run from the project root.
3. **Session-scoped data fixtures.** Shared mutable data brings back hidden state.
4. **Letting the mock drift.** Run `TEST_MODE=live` now and then.
5. **Forgetting `--strict-markers`**, so mistyped markers silently select nothing.
6. **Committing secrets.** `.env` and `reports/` go in `.gitignore`; document variables, never values.
7. **Logging tokens.** If you log headers, mask `Authorization` first.

## Practice Exercises

**Exercise 1: Add the stage environment check.** Make `TEST_ENV=prod` fail with a clear message, and show `TEST_ENV=stage` changes `settings.base_url`.

*Solution.* The `load_settings` shown above already raises `ValueError` for unknown names. Verify with:

```python
import os
os.environ["TEST_ENV"] = "stage"
from config.settings import load_settings
assert load_settings().base_url == "https://stage.example.com"
```

Then run `TEST_ENV=prod pytest`; collection stops with `Unknown TEST_ENV 'prod'`. The check lives in configuration, not scattered through tests.

**Exercise 2: Add `CommentsApi`.** JSONPlaceholder serves `/comments?postId=1`. Add a service, a fixture, and one test.

*Solution.*

```python
# api/endpoints/comments.py
class CommentsApi:
    PATH = "/comments"

    def __init__(self, client):
        self.client = client

    def for_post(self, post_id):
        return self.client.get(self.PATH, params={"postId": post_id})
```

```python
# conftest.py (add)
from api.endpoints.comments import CommentsApi

@pytest.fixture
def comments(client):
    return CommentsApi(client)
```

```python
# tests/test_comments.py
import pytest

@pytest.mark.regression
@pytest.mark.skipif(settings.mode == "mock", reason="no mock handler yet")
def test_comments_belong_to_post(comments):
    items = comments.for_post(1).assert_status(200).json()
    assert items and all(c["postId"] == 1 for c in items)
```

(Add `from config.settings import settings` at the top.) No existing class changed, which is the extensibility goal. Adding a comments handler to `mock_server.py` would let the skip go away.

**Exercise 3: Add a response helper.** Add `assert_json_field(name, expected)` to `ApiResponse` and use it.

*Solution.*

```python
def assert_json_field(self, name, expected):
    actual = self.json().get(name)
    assert actual == expected, f"Field '{name}': expected {expected!r}, got {actual!r}"
    return self
```

Use: `users.get(1).assert_status(200).assert_json_field("id", 1)`. Returning `self` keeps the chain working, and the message names the field, which a bare `assert` would not.

**Exercise 4: Prove POST is never retried.** Write a mocked test where `POST /posts` returns 503 and `retries=3`; show only one call is made.

*Solution.*

```python
@pytest.mark.mocked
def test_post_is_not_retried(mocked):
    url = f"{settings.base_url}/boom"
    mocked.add(responses.POST, url, status=503)

    ApiClient(settings.base_url, retries=3, backoff=0).post("/boom", json={}).assert_status(503)

    assert [c.request.url for c in mocked.calls].count(url) == 1
```

`POST` is not in `IDEMPOTENT`, so `attempts` is 1 regardless of `retries`. The returned 503 is handed to the test unchanged, so `assert_status(503)` passes.

## Quiz

1. Which layer should know how to attach the `Authorization` header?
2. Why does `assert_status` return `self`?
3. Why does the client default to zero retries and never retry POST?
4. A test needs a user that exists. Where should it come from, and with what scope?
5. What does `--strict-markers` protect you from?

**Answers**

1. The client. It injects the header once, in its session, so tests and services never touch auth.
2. So assertions chain (`get(1).assert_status(200).parse(User)`), keeping tests short and readable.
3. Retries hide real flakiness, and repeating a non-idempotent POST can create duplicates. Retries are opt-in and every one is logged.
4. From a function-scoped fixture that creates (and cleans up) its own data, so tests stay isolated.
5. Typos in marker names: an unregistered marker becomes an error rather than a test silently left out of `-m smoke`.

---

## Summary

- A framework gives each concern one home: config, client, services, response wrapper, models, data, fixtures, tests.
- Dependencies point downwards; the client never imports services or tests.
- Configuration comes from environment variables with safe defaults, so dev, stage and CI differ only in settings.
- `ApiClient` owns timeouts, retries on idempotent calls, logging and auth injection; services own operations; tests own assertions.
- `ApiResponse` helpers and Pydantic models turn failures into readable messages.
- CSV files drive data-driven tests; fixtures wire everything; markers slice the suite; `TEST_MODE` switches between mock and live.
- Avoid the God client, test logic in the client, and hidden state.
- A README that gets a newcomer running in ten minutes is part of the framework.

## Additional Resources

- pytest, *Good Integration Practices*: https://docs.pytest.org/en/stable/explanation/goodpractices.html
- pytest, *Fixtures reference*: https://docs.pytest.org/en/stable/reference/fixtures.html
- Requests, *Session objects*: https://requests.readthedocs.io/en/latest/user/advanced/#session-objects
- Pydantic, *Models*: https://docs.pydantic.dev/latest/concepts/models/
- `responses` library: https://github.com/getsentry/responses
- Martin Fowler, *PageObject* (the idea behind service classes): https://martinfowler.com/bliki/PageObject.html
