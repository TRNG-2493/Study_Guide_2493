# Handout 06 – Mocking & the Reusable Framework

> **How to use this handout:** each topic is a small, self-contained example in its own folder inside `week7-demos/`. Nothing carries over from one topic to the next. You will combine everything in **Handout 11 (Week 7 Mini-Project)**.

**Before class**

- Activate your `week7-demos` virtual environment and run: `pip install requests pytest responses pydantic pytest-html`

---

## Topic 5 – HTTP Mocking

### Definition

**HTTP mocking** replaces a real HTTP call with a fake response that your test controls, so the code under test never touches the network. Tests that call real services are slow, can fail randomly (flaky), may cause real side effects, and cannot easily produce rare cases such as a `500` or a timeout. The `responses` library intercepts every call made with `requests` and returns the response you **registered**. Python's built-in `unittest.mock` can replace any function or object, not only HTTP calls.

### Key ideas

| Test double | What it does |
|-------------|--------------|
| **Stub** | Returns a canned answer |
| **Mock** | A stub that also checks *how* it was called |
| **Fake** | A simple working replacement (for example, an in-memory database) |
| **Spy** | Wraps the real thing and records the calls |

- `responses.add(method, url, json=..., status=...)` registers a reply. Passing an exception as `body=` simulates a network failure.
- `responses.calls` records every intercepted request, so you can assert on what was sent.
- **"Patch where it is used":** patch `user_client.requests.get`, not `requests.get`.
- **Don't mock** the API that you are actually testing in end-to-end tests. Mock the things it *depends on*.

### Worked example – Mocking a tiny client

📁 Folder: `06-5-mocking/`, files `user_client.py` and `test_mocking.py`

**Step 1 – Write the code under test** (`user_client.py`).

```python
import requests

BASE = "https://api.example.com"


def get_username(user_id):
    r = requests.get(f"{BASE}/users/{user_id}", timeout=5)
    r.raise_for_status()
    return r.json()["name"]
```

**Step 2 – Write a stubbed happy path** (`test_mocking.py`).

```python
import pytest
import requests
import responses
import user_client


@responses.activate
def test_get_username_returns_name():
    responses.add(responses.GET, "https://api.example.com/users/1",
                  json={"id": 1, "name": "Ana"}, status=200)
    assert user_client.get_username(1) == "Ana"
```

**Step 3 – Check what was sent.** Add these lines to the same test.

```python
    assert len(responses.calls) == 1
    assert responses.calls[0].request.url == "https://api.example.com/users/1"
```

**Step 4 – Simulate a server error and a network failure.**

```python
@responses.activate
def test_server_error_raises():
    responses.add(responses.GET, "https://api.example.com/users/1", status=500)
    with pytest.raises(requests.HTTPError):
        user_client.get_username(1)


@responses.activate
def test_network_down_raises():
    responses.add(responses.GET, "https://api.example.com/users/1",
                  body=requests.ConnectionError("network down"))
    with pytest.raises(requests.ConnectionError):
        user_client.get_username(1)
```

**Step 5 – Do the same with `unittest.mock.patch`.**

```python
from unittest.mock import patch, Mock


def test_with_unittest_mock():
    fake = Mock(status_code=200)
    fake.json.return_value = {"name": "Bo"}
    with patch("user_client.requests.get", return_value=fake) as mocked:
        assert user_client.get_username(7) == "Bo"
    mocked.assert_called_once_with("https://api.example.com/users/7", timeout=5)
```

### Final code

**`user_client.py`**

```python
import requests

BASE = "https://api.example.com"


def get_username(user_id):
    r = requests.get(f"{BASE}/users/{user_id}", timeout=5)
    r.raise_for_status()
    return r.json()["name"]
```

**`test_mocking.py`**

```python
from unittest.mock import patch, Mock

import pytest
import requests
import responses
import user_client


@responses.activate
def test_get_username_returns_name():
    responses.add(responses.GET, "https://api.example.com/users/1",
                  json={"id": 1, "name": "Ana"}, status=200)
    assert user_client.get_username(1) == "Ana"
    assert len(responses.calls) == 1
    assert responses.calls[0].request.url == "https://api.example.com/users/1"


@responses.activate
def test_server_error_raises():
    responses.add(responses.GET, "https://api.example.com/users/1", status=500)
    with pytest.raises(requests.HTTPError):
        user_client.get_username(1)


@responses.activate
def test_network_down_raises():
    responses.add(responses.GET, "https://api.example.com/users/1",
                  body=requests.ConnectionError("network down"))
    with pytest.raises(requests.ConnectionError):
        user_client.get_username(1)


def test_with_unittest_mock():
    fake = Mock(status_code=200)
    fake.json.return_value = {"name": "Bo"}
    with patch("user_client.requests.get", return_value=fake) as mocked:
        assert user_client.get_username(7) == "Bo"
    mocked.assert_called_once_with("https://api.example.com/users/7", timeout=5)
```

### How to run

```bash
cd week7-demos/06-5-mocking
pytest -v test_mocking.py
```

### Checkpoint

```
test_get_username_returns_name PASSED
test_server_error_raises PASSED
test_network_down_raises PASSED
test_with_unittest_mock PASSED
============ 4 passed in 0.1s ============
```

The tests pass even with Wi-Fi turned off. Try it.

### Your turn

1. Register **two** responses for the same URL (a `503` and then a `200`) and call `requests.get` twice. What does each call return?
2. Remove `responses.add` from the happy-path test but keep `@responses.activate`. What error do you get, and why is that useful?
3. Use `side_effect=requests.Timeout` with `patch` to simulate a timeout.
4. Patch `requests.get` instead of `user_client.requests.get`, and import `get` with `from requests import get` inside `user_client.py`. Does the patch still work? Explain.

### Common errors

- **`ConnectionError: Connection refused by Responses`.** The URL you registered does not exactly match the one called (check for a trailing slash, the query string, or http vs https).
- **Patching in the wrong place.** Patch the name where the code under test *looks it up*.
- **Mocks drifting from reality.** Your mock says `name`, but the real API now says `fullName`. Use contract tests (schema validation) to catch this.

---

## Topic 6 – Mocking External APIs

### Definition

Real applications call **third-party services**, such as payment, weather, email or exchange-rate APIs, that you do not control. In tests you **mock** these so you can test *your* handling of their responses, including errors, timeouts, rate limits (`429`) and pagination, without cost or side effects. The client code should accept its `base_url` and `session` through **dependency injection**, which makes it easy to point at a mock. Mock payloads should come from **recorded real responses**, and tests should also check the **outbound request** your code sends, not only how it handles the reply.

### Key ideas

- **Mock it:** paid services, services with side effects (email, payment), and slow or unreliable services.
- **Keep it real:** your own API under test, plus a few contract or smoke tests against the real third party.
- A **mock-server fixture** in `conftest.py` (built with `responses.RequestsMock`) keeps every test's setup to one line.
- **Inject anything slow**, such as `sleep`, so retry tests run instantly.

### Worked example – An exchange-rate client with retries

📁 Folder: `06-6-rates/`

```
06-6-rates/
├── data/recorded/rates_usd.json
├── rates_client.py
├── conftest.py
└── test_rates.py
```

**Step 1 – Write a client that uses dependency injection** (`rates_client.py`).

```python
import time
import requests


class RatesClient:
    def __init__(self, base_url, api_key, session=None, max_retries=2, sleep=time.sleep):
        self.base_url = base_url.rstrip("/")
        self.api_key = api_key
        self.session = session or requests.Session()
        self.max_retries = max_retries
        self.sleep = sleep
```

**Step 2 – Add a method that retries on `429`.**

```python
    def latest(self, base):
        for attempt in range(self.max_retries + 1):
            r = self.session.get(f"{self.base_url}/latest", params={"base": base},
                                 headers={"X-API-Key": self.api_key}, timeout=5)
            if r.status_code == 429 and attempt < self.max_retries:
                self.sleep(int(r.headers.get("Retry-After", "1")))
                continue
            r.raise_for_status()
            return r.json()["rates"]
```

**Step 3 – Save a recorded response** as `data/recorded/rates_usd.json`.

```json
{"base": "USD", "date": "2026-11-18", "rates": {"EUR": 0.92, "GBP": 0.79}}
```

**Step 4 – Add a mock-server fixture and a client fixture** in `conftest.py`.

```python
from pathlib import Path
import pytest
import responses

from rates_client import RatesClient

RATES_URL = "https://rates.example.com"
RECORDED = Path(__file__).parent / "data" / "recorded"


@pytest.fixture
def rates_mock():
    with responses.RequestsMock() as rsps:
        yield rsps


@pytest.fixture
def rates_client():
    sleeps = []
    client = RatesClient(RATES_URL, api_key="test-key", sleep=sleeps.append)
    client.sleeps = sleeps          # lets the test see the waits without really waiting
    return client
```

**Step 5 – Test the happy path and the outbound request** (`test_rates.py`).

```python
import json
from responses import matchers
from conftest import RATES_URL, RECORDED


def test_latest_returns_rates(rates_mock, rates_client):
    payload = json.loads((RECORDED / "rates_usd.json").read_text())
    rates_mock.add("GET", f"{RATES_URL}/latest", json=payload,
                   match=[matchers.query_param_matcher({"base": "USD"}),
                          matchers.header_matcher({"X-API-Key": "test-key"})])
    assert rates_client.latest("USD")["EUR"] == 0.92
```

**Step 6 – Test the rate-limit retry.**

```python
def test_retries_after_429(rates_mock, rates_client):
    rates_mock.add("GET", f"{RATES_URL}/latest", status=429, headers={"Retry-After": "3"})
    rates_mock.add("GET", f"{RATES_URL}/latest", json={"rates": {"EUR": 0.9}})
    assert rates_client.latest("USD") == {"EUR": 0.9}
    assert rates_client.sleeps == [3]
    assert len(rates_mock.calls) == 2
```

### Final code

**`rates_client.py`**

```python
import time
import requests


class RatesClient:
    def __init__(self, base_url, api_key, session=None, max_retries=2, sleep=time.sleep):
        self.base_url = base_url.rstrip("/")
        self.api_key = api_key
        self.session = session or requests.Session()
        self.max_retries = max_retries
        self.sleep = sleep

    def latest(self, base):
        for attempt in range(self.max_retries + 1):
            r = self.session.get(f"{self.base_url}/latest", params={"base": base},
                                 headers={"X-API-Key": self.api_key}, timeout=5)
            if r.status_code == 429 and attempt < self.max_retries:
                self.sleep(int(r.headers.get("Retry-After", "1")))
                continue
            r.raise_for_status()
            return r.json()["rates"]
```

**`data/recorded/rates_usd.json`**

```json
{"base": "USD", "date": "2026-11-18", "rates": {"EUR": 0.92, "GBP": 0.79}}
```

**`conftest.py`**

```python
from pathlib import Path
import pytest
import responses

from rates_client import RatesClient

RATES_URL = "https://rates.example.com"
RECORDED = Path(__file__).parent / "data" / "recorded"


@pytest.fixture
def rates_mock():
    with responses.RequestsMock() as rsps:
        yield rsps


@pytest.fixture
def rates_client():
    sleeps = []
    client = RatesClient(RATES_URL, api_key="test-key", sleep=sleeps.append)
    client.sleeps = sleeps          # lets the test see the waits without really waiting
    return client
```

**`test_rates.py`**

```python
import json
from responses import matchers
from conftest import RATES_URL, RECORDED


def test_latest_returns_rates(rates_mock, rates_client):
    payload = json.loads((RECORDED / "rates_usd.json").read_text())
    rates_mock.add("GET", f"{RATES_URL}/latest", json=payload,
                   match=[matchers.query_param_matcher({"base": "USD"}),
                          matchers.header_matcher({"X-API-Key": "test-key"})])
    assert rates_client.latest("USD")["EUR"] == 0.92


def test_retries_after_429(rates_mock, rates_client):
    rates_mock.add("GET", f"{RATES_URL}/latest", status=429, headers={"Retry-After": "3"})
    rates_mock.add("GET", f"{RATES_URL}/latest", json={"rates": {"EUR": 0.9}})
    assert rates_client.latest("USD") == {"EUR": 0.9}
    assert rates_client.sleeps == [3]
    assert len(rates_mock.calls) == 2
```

### How to run

```bash
cd week7-demos/06-6-rates
pytest -v test_rates.py
```

### Checkpoint

```
test_latest_returns_rates PASSED
test_retries_after_429 PASSED
============ 2 passed in 0.1s ============
```

The run takes well under a second, even though the "server" asked you to wait 3 seconds.

### Your turn

1. Write a test where the API returns `429` three times in a row. With `max_retries=2`, what should happen, and how many calls are made?
2. Change the expected API key in the `header_matcher` to `wrong-key`. What error does the test show? What bug would this catch in real code?
3. Simulate a timeout (`body=requests.Timeout()`) and assert that `latest` raises it.
4. Name one test you would still run against the **real** exchange-rate service, and say how often.

---

## Topic 7 – Reusable API Test Framework

📁 Folder: `06-7-framework/`

### Definition

A **reusable API test framework** is the shared structure that every test in a project builds on. It contains configuration, an HTTP client, endpoint (service) classes, data models, fixtures and reporting, each in its own **layer**. Without a framework, every test repeats URLs, headers, timeouts and parsing, so one API change means editing hundreds of files. With a framework, tests read like business steps (`posts.get(1)`), and a change is made in **one** place. This example is deliberately tiny, so you can see every layer at once.

### Key ideas

```
06-7-framework/
├── pytest.ini              # markers + JUnit/HTML reports
├── conftest.py             # fixtures wiring the layers together
├── config/settings.py      # env vars: BASE_URL, TIMEOUT, USE_MOCK
├── api/client.py           # ApiClient (Session + timeout)
├── api/posts.py            # PostsApi – one class per resource
├── models/post.py          # Pydantic model of a post
├── mocks/mock_server.py    # responses-based fake API
└── tests/test_posts_api.py # only test logic lives here
```

- **Each layer has one job.** Tests never build URLs themselves, and the client never asserts.
- **Mock/live switch:** `USE_MOCK=1` runs the whole suite offline, which is fast and good for pull requests. `USE_MOCK=0` runs against a real environment.
- **Reports:** JUnit XML is for CI, and HTML is for people to read.

### Worked example – Building the layers

Create the folders, plus an empty `__init__.py` in `config/`, `api/`, `models/` and `mocks/`.

**Step 1 – Put settings in one place** (`config/settings.py`).

```python
import os
from dataclasses import dataclass


@dataclass(frozen=True)
class Settings:
    base_url: str = os.getenv("BASE_URL", "https://jsonplaceholder.typicode.com")
    timeout: float = float(os.getenv("API_TIMEOUT", "5"))
    use_mock: bool = os.getenv("USE_MOCK", "0") == "1"


settings = Settings()
```

**Step 2 – Add the client and one service class** (`api/client.py` and `api/posts.py`).

```python
# api/client.py
import requests


class ApiClient:
    def __init__(self, base_url, timeout):
        self.base_url, self.timeout = base_url.rstrip("/"), timeout
        self.session = requests.Session()

    def request(self, method, path, **kw):
        kw.setdefault("timeout", self.timeout)
        return self.session.request(method, f"{self.base_url}{path}", **kw)
```

```python
# api/posts.py
class PostsApi:
    PATH = "/posts"

    def __init__(self, client):
        self.client = client

    def get(self, post_id):
        return self.client.request("GET", f"{self.PATH}/{post_id}")

    def create(self, **fields):
        return self.client.request("POST", self.PATH, json=fields)
```

**Step 3 – Add a model and a small mock server** (`models/post.py` and `mocks/mock_server.py`).

```python
# models/post.py
from pydantic import BaseModel


class Post(BaseModel):
    id: int
    userId: int
    title: str
    body: str
```

```python
# mocks/mock_server.py
import responses


def install(rsps, base):
    rsps.add(responses.GET, f"{base}/posts/1",
             json={"id": 1, "userId": 1, "title": "mock title", "body": "b"})
    rsps.add(responses.POST, f"{base}/posts", status=201,
             json={"id": 101, "userId": 1, "title": "t", "body": "b"})
```

**Step 4 – Wire the layers in `conftest.py`, with a mock/live switch.**

```python
import pytest
import responses

from api.client import ApiClient
from api.posts import PostsApi
from config.settings import settings
from mocks.mock_server import install


@pytest.fixture(scope="session")
def client():
    c = ApiClient(settings.base_url, settings.timeout)
    if settings.use_mock:
        with responses.RequestsMock(assert_all_requests_are_fired=False) as rsps:
            install(rsps, settings.base_url)
            yield c
    else:
        yield c


@pytest.fixture
def posts(client):
    return PostsApi(client)
```

**Step 5 – Write tests in business language** (`tests/test_posts_api.py`).

```python
import pytest
from models.post import Post


@pytest.mark.smoke
def test_get_post(posts):
    r = posts.get(1)
    assert r.status_code == 200
    Post.model_validate(r.json())


def test_create_post(posts):
    r = posts.create(title="t", body="b", userId=1)
    assert r.status_code == 201
```

**Step 6 – Turn on reports** in `pytest.ini`.

```ini
[pytest]
pythonpath = .
testpaths = tests
markers =
    smoke: quick health checks
addopts = -ra --strict-markers --junitxml=reports/junit.xml --html=reports/report.html --self-contained-html
```

### Final code

Each file in Steps 1–6 is already complete. Check that your folder looks like this, including the four empty `__init__.py` files:

**`06-7-framework/`**

```
06-7-framework/
├── pytest.ini
├── conftest.py
├── config/
│   ├── __init__.py          (empty)
│   └── settings.py
├── api/
│   ├── __init__.py          (empty)
│   ├── client.py
│   └── posts.py
├── models/
│   ├── __init__.py          (empty)
│   └── post.py
├── mocks/
│   ├── __init__.py          (empty)
│   └── mock_server.py
└── tests/
    └── test_posts_api.py
```

### How to run

```bash
cd week7-demos/06-7-framework

# offline, using the mock server
# bash
USE_MOCK=1 pytest -v
# PowerShell
$env:USE_MOCK="1"; pytest -v

# live, against JSONPlaceholder (needs internet)
# bash
USE_MOCK=0 pytest -v
# PowerShell
$env:USE_MOCK="0"; pytest -v
```

Then open `reports/report.html` in a browser.

### Checkpoint

With `USE_MOCK=1`:

```
tests/test_posts_api.py::test_get_post PASSED
tests/test_posts_api.py::test_create_post PASSED
--- generated xml file: .../reports/junit.xml ---
--- Generated html report: file:///.../reports/report.html ---
```

`reports/report.html` opens in a browser and lists both tests. With `USE_MOCK=0`, the same two tests pass against the live API.

### Your turn

1. Add a `UsersApi` class with `list()` and `get(user_id)`, a `users` fixture, and one test for each. (Remember to add the mock responses too.)
2. Add a `@pytest.mark.mocked` test that only makes sense offline (for example, a `500` from `/posts/2`), and skip it automatically when `USE_MOCK=0`.
3. Write a 5-line `README.md` for the framework: how to install it, run it offline, run it live, and find the reports.
4. Name two anti-patterns that this structure prevents.

### Common errors

- **`ModuleNotFoundError: api`.** An `__init__.py` is missing, or `pythonpath = .` is missing from `pytest.ini`.
- **Tests that build URLs themselves**, such as `client.request("GET", "/posts/1")` inside a test. Add a method to the service class instead.
- **Settings read at import time.** Set the environment variables *before* running PyTest, not inside a test.

---

## Answers

<details>
<summary><strong>Topic 5 – HTTP Mocking</strong></summary>

1. The first call returns `503` and the second returns `200`. Responses registered for the same URL are returned in order (the last one repeats).
2. `requests.exceptions.ConnectionError: Connection refused by Responses ...`. This is useful because an unexpected or unregistered call fails loudly instead of quietly reaching the internet.
3. ```python
   def test_timeout():
       with patch("user_client.requests.get", side_effect=requests.Timeout):
           with pytest.raises(requests.Timeout):
               user_client.get_username(1)
   ```
4. No. `from requests import get` copies the name into `user_client` at import time, so patching `requests.get` afterwards does not change `user_client.get`. You would need to patch `user_client.get` instead.

</details>

<details>
<summary><strong>Topic 6 – Mocking External APIs</strong></summary>

1. Three calls are made (the first try plus 2 retries). The third `429` is not retried, so `raise_for_status()` raises `requests.HTTPError`. `sleeps == [3, 3]`.
   ```python
   def test_gives_up_after_retries(rates_mock, rates_client):
       for _ in range(3):
           rates_mock.add("GET", f"{RATES_URL}/latest", status=429, headers={"Retry-After": "3"})
       with pytest.raises(requests.HTTPError):
           rates_client.latest("USD")
       assert len(rates_mock.calls) == 3
   ```
2. `ConnectionError: Connection refused by Responses ... Headers do not match`. It catches the client sending the wrong or missing API key.
3. ```python
   def test_timeout(rates_mock, rates_client):
       rates_mock.add("GET", f"{RATES_URL}/latest", body=requests.Timeout())
       with pytest.raises(requests.Timeout):
           rates_client.latest("USD")
   ```
4. A contract or smoke test that calls `/latest?base=USD` and validates the schema. Run it nightly or before a release, not on every commit.

</details>

<details>
<summary><strong>Topic 7 – Reusable API Test Framework</strong></summary>

1. ```python
   # api/users.py
   class UsersApi:
       PATH = "/users"
       def __init__(self, client): self.client = client
       def list(self): return self.client.request("GET", self.PATH)
       def get(self, user_id): return self.client.request("GET", f"{self.PATH}/{user_id}")

   # conftest.py
   @pytest.fixture
   def users(client): return UsersApi(client)

   # tests/test_users_api.py
   def test_list_users(users): assert users.list().status_code == 200
   def test_get_user(users): assert users.get(1).json()["id"] == 1
   ```
   In `install`, also add `rsps.add(responses.GET, f"{base}/users", json=[{"id": 1}])` and `rsps.add(responses.GET, f"{base}/users/1", json={"id": 1})`.
2. ```python
   from config.settings import settings

   @pytest.mark.mocked
   @pytest.mark.skipif(not settings.use_mock, reason="needs mock server")
   def test_server_error(posts):
       assert posts.get(2).status_code == 500
   ```
   Add `rsps.add(responses.GET, f"{base}/posts/2", status=500)` to `install`, and register `mocked` under `markers` in `pytest.ini`.
3. ```
   pip install requests pytest responses pydantic pytest-html
   USE_MOCK=1 pytest          # offline
   USE_MOCK=0 pytest          # live (set BASE_URL to change target)
   pytest -m smoke            # quick check
   Reports: reports/report.html, reports/junit.xml
   ```
4. Any two of: URLs and headers copied into every test, assertions inside the client, no timeout, hard-coded environments, and test data mixed into test logic.

</details>
