# HTTP Requests from Automated Tests

## Learning Objectives

By the end of this lesson you will be able to:

- Explain how sending a request from test code differs from sending it in Postman, and what that changes about how tests are written.
- Describe JSONPlaceholder, including the fact that it **fakes** writes, and design tests that stay honest about it.
- Configure the base URL, timeouts, and thresholds from **environment variables**.
- Build an `ApiClient` around a `requests.Session` and explain every line of it.
- Set **timeouts** so a test can never hang, and tell `ConnectTimeout`, `ReadTimeout`, and `ConnectionError` apart.
- Build payloads, query parameters, path parameters, and headers correctly from Python.
- Assert on response basics (status, content type, body, headers, elapsed time) with self-explaining failure messages.
- Write a full create-read-update-delete (CRUD) flow that works on both fake and persisting APIs.
- Create and clean up test data with `try/finally` and `yield` fixtures, and explain idempotency and why tests must not depend on order.
- Log requests and responses for debugging, write sensible response-time assertions, and handle a flaky network with retries and bounded polling.

---

## Why This Matters

This week's epic is to build a pipeline-ready API test framework for Project 2. On Monday you learned what HTTP messages, methods, headers, and parameters are, and you exercised them by hand in Postman. A pipeline cannot click "Send" and judge the result by eye. Every check you performed manually has to become code that sends the request, waits a sensible time, judges the response, and reports clearly when something is wrong.

That move changes what can go wrong. In Postman a hanging request is something you cancel; in an unattended pipeline it can freeze a build for an hour. In Postman a network blip means you resend; in a pipeline it turns the build red, and a team that sees false alarms soon ignores real ones. In Postman the base URL is a dropdown; in code it must come from configuration, or you edit forty files to change servers.

Today's lesson is therefore about the habits that make HTTP calls from tests **safe, repeatable, and diagnosable**: configuration from the environment, a timeout on every call, one shared session, deliberate payloads, data that is created and cleaned up, tests that do not depend on each other, logs that tell the story of a failure, and a calm strategy for network trouble.

Where this sits in the week: Monday supplied the vocabulary you use here. The other Tuesday lessons go deeper on single pieces (the `requests` library itself, authentication headers, status codes, JSON validation, PyTest structure, fixtures); this lesson shows how they come together when *sending* requests. Data-driven inputs, mocking, and the pipeline come later in the week and are not needed today.

---

## The Concept

### 1. From Postman to Python: What Actually Changes

When you click "Send" in Postman you are the test runner. You supply the intelligence: you notice that the response took suspiciously long, that the status is `500`, that the body looks odd, that the server seems to be down. Automated tests have no such intelligence. They do exactly three things: **send** a request, **check** what comes back, and **report**. Everything a human would notice must be turned into an explicit instruction.

In short, code must supply the base URL from configuration, a **timeout** on every call, a deliberate **retry** decision, explicit **assertions**, tracking and **cleanup** of created data, **logs** as evidence, and tests that work in **any order**. The rest of the lesson takes each in turn.

You will use three tools together:

- **`requests`** sends the HTTP call. It is the standard Python HTTP library and you met its basics in the `requests` library lesson earlier today.
- **PyTest** discovers and runs the tests and reports results. (The PyTest structure lesson covers file layout in depth.)
- **A target API.** For practice that is JSONPlaceholder; for your project it is the Project 2 system.

### 2. Meet the Practice Target: JSONPlaceholder

JSONPlaceholder (`https://jsonplaceholder.typicode.com`) is a free public API that returns realistic fake data. It offers `/posts`, `/comments`, `/albums`, `/photos`, `/todos`, and `/users`, for example `GET /posts` (all 100 posts), `GET /posts/1`, `GET /posts?userId=1` (a query-parameter filter), `GET /posts/1/comments` (a nested resource), plus `POST`, `PUT`, `PATCH`, and `DELETE` on `/posts`.

The catch: **JSONPlaceholder fakes writes.** A `POST /posts` replies `201 Created` with your data and a new `id` (always `101`), but nothing is stored, so `GET /posts/101` returns `404`. `PUT`, `PATCH`, and `DELETE` likewise answer with success and change nothing. That is safe for thousands of students, but it means you must be careful about **what a test can honestly claim**. A test that creates a record and reads it back passes on a real API and fails here, and neither result says anything is wrong. Section 12 handles both situations explicitly.

> **How the examples were verified.** Snippets and outputs were run against a small server on `127.0.0.1` that imitates JSONPlaceholder (fake writes included) and can switch to a "persisting" mode where writes are really stored. Output from it is labelled **local mock**. Numbers for the real public host are labelled **representative** (typical, not exact). Ports and timings are specific to that setup.

### 3. Project Layout and Setup

A small, tidy layout keeps requests, configuration, and tests separate:

```text
api-tests/
  pytest.ini
  config/
    __init__.py
    settings.py        <- reads environment variables
  api/
    __init__.py
    client.py          <- ApiClient: one place that sends requests
  helpers/
    __init__.py
    waiting.py         <- wait_until, describe
  tests/
    conftest.py        <- the shared `api` fixture
    test_posts_crud.py <- the tests themselves
```

Install the libraries inside a virtual environment:

```bash
python -m venv .venv
source .venv/bin/activate          # Windows PowerShell: .venv\Scripts\Activate.ps1
pip install requests pytest
```

And a minimal `pytest.ini` so that `import api` and `import config` work from the tests:

```ini
[pytest]
pythonpath = .
log_level = DEBUG
log_format = %(asctime)s %(levelname)s %(name)s: %(message)s
```

Line by line: `pythonpath = .` adds the project root to Python's import path; without it `from api.client import ApiClient` inside `tests/` fails with `ModuleNotFoundError: No module named 'api'` (a common first-day error). `log_level = DEBUG` captures records of every level for each test; they are shown only when a test fails or when you ask, so green runs stay quiet. `log_format` sets how each line looks: time, level, logger name, message.

### 4. Configuration From Environment Variables

Never type a server address into a test. Put it in one place and let the environment override it.

```python
# config/settings.py
import os

BASE_URL = os.getenv("API_BASE_URL", "https://jsonplaceholder.typicode.com").rstrip("/")
CONNECT_TIMEOUT = float(os.getenv("API_CONNECT_TIMEOUT", "3.05"))
READ_TIMEOUT = float(os.getenv("API_READ_TIMEOUT", "10"))
MAX_RESPONSE_MS = int(os.getenv("API_MAX_RESPONSE_MS", "2000"))
RETRIES = int(os.getenv("API_RETRIES", "2"))
PERSISTS_WRITES = os.getenv("API_PERSISTS_WRITES", "false").lower() in ("1", "true", "yes")
```

Line by line:

- `os.getenv("API_BASE_URL", "...")` reads the variable; the second argument is the **default** when it is unset, so beginners get a working setup and a pipeline can override it.
- `.rstrip("/")` removes a trailing slash, because a doubled slash (`//posts`) after joining can cause surprising `404`s.
- `float(...)`, `int(...)`: environment variables are always **text**, so numbers must be converted or a later comparison raises `TypeError`. The odd `3.05` follows a `requests` documentation convention (just above a multiple of three seconds, the default TCP retransmission window).
- `MAX_RESPONSE_MS` and `RETRIES` feed sections 16 and 17; making them configurable lets a slow environment get looser limits without editing tests.
- `PERSISTS_WRITES` records whether the target really stores writes; `.lower() in ("1", "true", "yes")` turns friendly text into a real `bool`. It selects between the fake-API and real-API CRUD tests.

To change a value for one run, set it in the shell that launches PyTest.

```bash
# macOS / Linux / Git Bash
API_BASE_URL=http://localhost:8000 pytest
```

```powershell
# Windows PowerShell
$env:API_BASE_URL = "http://localhost:8000"
pytest
```

In a CI pipeline you set the same variables in the pipeline configuration (covered in Friday's lessons on configuration and secrets). The tests do not change; only the environment does.

> **Never put secrets in settings defaults.** A base URL or timeout is harmless to commit; a password or token is not (see the headers and authentication lesson today).

### 5. The ApiClient: One Door Through Which Every Request Passes

By the second test you will notice that every request repeats the same ingredients: base URL, `Accept` header, timeout, logging. A small wrapper class removes that repetition.

```python
# api/client.py
import logging
import uuid

import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

logger = logging.getLogger("api")


class ApiClient:
    """A thin wrapper around requests.Session for one API."""

    def __init__(self, base_url, timeout=(3.05, 10), retries=0):
        self.base_url = base_url.rstrip("/")
        self.timeout = timeout
        self.session = requests.Session()
        self.session.headers.update({
            "Accept": "application/json",
            "User-Agent": "qea-api-tests/1.0",
        })
        if retries:
            retry = Retry(
                total=retries,
                backoff_factor=0.2,
                status_forcelist=[502, 503, 504],
                allowed_methods=frozenset(["GET", "HEAD", "OPTIONS", "PUT", "DELETE"]),
                respect_retry_after_header=True,
                raise_on_status=False,
            )
            adapter = HTTPAdapter(max_retries=retry)
            self.session.mount("http://", adapter)
            self.session.mount("https://", adapter)

    def _url(self, path):
        return f"{self.base_url}/{path.lstrip('/')}"

    def request(self, method, path, **kwargs):
        kwargs.setdefault("timeout", self.timeout)
        headers = dict(kwargs.pop("headers", None) or {})
        headers.setdefault("X-Request-Id", str(uuid.uuid4()))
        url = self._url(path)

        logger.info("-> %s %s params=%s json=%s", method, url,
                    kwargs.get("params"), kwargs.get("json"))
        try:
            response = self.session.request(method, url, headers=headers, **kwargs)
        except requests.exceptions.RequestException as exc:
            logger.error("!! %s %s failed: %s: %s", method, url,
                         type(exc).__name__, exc)
            raise

        logger.info("<- %s in %.0f ms", response.status_code,
                    response.elapsed.total_seconds() * 1000)
        logger.debug("   body: %.500s", response.text)
        return response

    def get(self, path, **kw):    return self.request("GET", path, **kw)
    def post(self, path, **kw):   return self.request("POST", path, **kw)
    def put(self, path, **kw):    return self.request("PUT", path, **kw)
    def patch(self, path, **kw):  return self.request("PATCH", path, **kw)
    def delete(self, path, **kw): return self.request("DELETE", path, **kw)
```

This is the longest snippet of the lesson, so take it slowly. (Run against the local mock, a version of this exact class passes the full test file shown later.)

**Imports and logger**

- `HTTPAdapter` and `Retry` enable optional retries (section 17).
- `logger = logging.getLogger("api")` creates a named logger. Every message is tagged `api`, so you can tune it independently of other libraries.

**The constructor `__init__`**

- `class ApiClient:` bundles data with behaviour. `__init__` runs when you write `ApiClient(...)`; `self` is the object being built.
- `timeout=(3.05, 10)` is the default: 3.05 s to **connect**, 10 s to **read** (section 6).
- `requests.Session()` creates a **session**: an object that keeps the underlying connection open and reuses it for several requests (faster: handshakes are paid once) and remembers default headers and cookies.
- `self.session.headers.update({...})` sets headers that will accompany *every* request. `Accept` says "I want JSON back"; `User-Agent` names your test traffic so a server team can recognise it.
- The `if retries:` block installs retries and is skipped when `retries` is `0`.

**`_url`**

- `f"{self.base_url}/{path.lstrip('/')}"` joins base and path with exactly one slash, whether or not the caller wrote a leading slash (`"/posts"` or `"posts"`).

**`request`: the heart of the client**

- `**kwargs` collects extra named arguments (`json=`, `params=`, `headers=`) and forwards them to `requests`.
- `kwargs.setdefault("timeout", self.timeout)` guarantees a timeout on every call, **unless** the caller passes its own. This is the single most important line in the file (section 6).
- `headers = dict(kwargs.pop("headers", None) or {})` removes any caller-supplied `headers` from `kwargs`, copies them into a fresh dictionary (so the caller's is never modified), and falls back to an empty one.
- `headers.setdefault("X-Request-Id", str(uuid.uuid4()))` adds a unique request ID unless the caller supplied one. If the server logs it, you can find exactly this call in the server logs when a test fails (Monday's headers lesson introduced `X-Request-Id`).
- The first `logger.info` records the outgoing request; `%s` placeholders are filled lazily, the recommended logging style.
- The `try / except requests.exceptions.RequestException` wraps the call. `RequestException` is the parent of every `requests` error (timeouts, connection failures, and so on). We **log and re-raise** with a bare `raise`: the client records the evidence, but it does not hide the error, because the test must still fail.
- `response.elapsed` is a `timedelta`; `.total_seconds() * 1000` converts it to milliseconds.
- `logger.debug("   body: %.500s", response.text)` records the first 500 characters of the body at DEBUG level. `%.500s` truncates so huge bodies cannot flood the log.
- `return response` hands the untouched `Response` back. The client does **not** call `raise_for_status()` and does **not** assert anything. Whether a `404` is a failure or the expected result depends on the test, so judging is the test's job.

**Convenience methods**

- `get`, `post`, `put`, `patch`, `delete` call `request` with the right verb so tests read naturally: `api.get("/posts/1")`.

### 6. Timeouts: A Test Must Never Hang

By default, `requests` waits **forever**. A call such as `requests.get(url)` with no `timeout` blocks indefinitely if the server accepts the connection and then goes silent. On a laptop you press Ctrl+C; in a pipeline nobody is there, and the job sits until the CI system kills it an hour later.

The rule is therefore simple: **every request gets a timeout, with no exceptions.** Our client enforces this by always supplying one.

The timeout can be given as a single number or as a pair:

```python
requests.get(url, timeout=5)          # same limit for connect and for read
requests.get(url, timeout=(3.05, 10)) # (connect timeout, read timeout)
```

- The **connect timeout** is how long to wait while *establishing* the connection (DNS lookup, TCP handshake, TLS). If the host is unreachable or firewalled, this is the clock that expires. Keep it short (a few seconds): a healthy server connects in milliseconds.
- The **read timeout** is how long to wait *between bytes* once connected, most importantly for the first byte of the response. It must allow for real server work, so it is normally larger.

Two subtleties that surprise people:

1. The read timeout is **not a limit on total download time.** It is the maximum gap between received bytes. A server dribbling one byte every few seconds can keep a call alive far longer, so do not read the number as "the whole call takes at most this long".
2. When retries are on (section 17), each *attempt* gets the timeout, so the worst case is roughly `(retries + 1) x timeout` plus waits between attempts. Choose numbers with that multiplication in mind.

#### What a timeout looks like when it fires

Here is a test that proves the client really does give up. The local mock has a `/slow` endpoint that sleeps for the number of seconds you pass:

```python
def test_timeout_raises_instead_of_hanging():
    client = ApiClient(settings.BASE_URL, timeout=(1, 0.5))
    with pytest.raises(requests.exceptions.ReadTimeout):
        client.get("/slow", params={"delay": 2})
```

Line by line:

- A fresh client is built with a deliberately tiny read timeout of half a second.
- `/slow?delay=2` makes the server wait two seconds before answering, which is longer than the client will wait.
- `pytest.raises(requests.exceptions.ReadTimeout)` is a context manager that says "the code inside **must** raise this exception; if it does, the test passes; if it does not, the test fails." This is how you assert that an error happens.

Local mock output when the exception is logged by the client:

```text
ERROR api: !! GET http://127.0.0.1:8802/slow failed: ReadTimeout: HTTPConnectionPool(host='127.0.0.1', port=8802): Read timed out. (read timeout=0.5)
```

The test ended in about half a second with a clear message rather than a frozen terminal.

#### Telling the exceptions apart

`requests` raises different exceptions for different problems, and knowing them tells you where to look:

| Exception | Meaning | Typical cause |
|-----------|---------|---------------|
| `requests.exceptions.ConnectTimeout` | Could not establish a connection in time | Host unreachable, firewall dropping packets, VPN off |
| `requests.exceptions.ReadTimeout` | Connected, but the server did not answer in time | Server overloaded, slow query, deadlock |
| `requests.exceptions.ConnectionError` | Connection refused or dropped | Server not running, wrong port, DNS failure, connection reset |
| `requests.exceptions.RequestException` | The parent of all of the above | Use it to catch "anything from requests" |

Both timeout classes inherit from `Timeout`, and `Timeout` and `ConnectionError` inherit from `RequestException` (confirmed on the local mock). A connection to a port where nothing listens produced:

```text
ConnectionError: HTTPConnectionPool(host='127.0.0.1', port=9): Max retries exceeded with url: /x (Caused by NewConnectionError("... [Errno 111] Connection refused"))
```

"Max retries exceeded" is urllib3's wording and appears even with no retries configured; the useful part is at the end: `Connection refused`.

A timeout or connection error usually means the **environment** is unhealthy, not that the feature is wrong, and a clearly named exception makes that obvious, instead of a confusing `KeyError` three lines later.

### 7. Building Request Payloads

A **payload** (or request body) is the data you send with `POST`, `PUT`, and `PATCH`. With `requests` there are two common ways to supply it:

```python
api.post("/posts", json={"title": "hello", "body": "world", "userId": 1})   # JSON body
api.post("/login", data={"username": "qa", "password": "not-a-real-secret"})  # form body
```

- `json=` takes a Python dictionary, converts it to JSON text, **and** sets the header `Content-Type: application/json` for you. Use this for JSON APIs.
- `data=` with a dictionary sends **form-encoded** text (`username=qa&password=...`) with `Content-Type: application/x-www-form-urlencoded`. Use it only when the API expects a form.

We can verify what `json=` really puts on the wire by preparing a request without sending it (local mock environment, but no network is needed for this one):

```python
>>> import requests
>>> req = requests.Request("POST", "http://127.0.0.1:8802/posts",
...                        json={"a": 1}, params={"q": "v w"}).prepare()
>>> req.method, req.url
('POST', 'http://127.0.0.1:8802/posts?q=v+w')
>>> req.headers
{'Content-Length': '8', 'Content-Type': 'application/json'}
>>> req.body
b'{"a": 1}'
```

Three useful observations: the space in `"v w"` was encoded as `+`; `Content-Type` and `Content-Length` were set automatically; the body is the JSON text as bytes.

#### The classic mistake: `data=` with a dictionary for a JSON API

```python
api.post("/posts", data={"title": "hello"})   # sends title=hello  (a FORM, not JSON)
```

The server receives `title=hello` labelled as a form. A strict JSON API answers `400 Bad Request` or `415 Unsupported Media Type`; a lenient one may silently ignore your fields. The request "worked" in the sense that something was sent, which makes this bug maddening. If the API speaks JSON, use `json=`.

A related trap: do **not** set `Content-Type` by hand when using `json=`. `requests` already did, and a hand-written value that disagrees with the body (say `text/plain`) causes the confusion you were avoiding.

#### Keep payloads honest and unique

Rather than copy a dictionary into every test, build payloads with a small function that has sensible defaults and lets each test override just the field it cares about:

```python
import uuid


def make_post_payload(**overrides):
    payload = {
        "title": f"qea-{uuid.uuid4().hex[:8]}",
        "body": "created by an automated test",
        "userId": 1,
    }
    payload.update(overrides)
    return payload
```

Line by line:

- `**overrides` accepts any keyword arguments; `make_post_payload(title="Edge case")` replaces the title and keeps the rest.
- `uuid.uuid4().hex[:8]` yields eight random hex characters such as `3fa9c1d2`, so each payload gets a **unique title**. Unique data prevents tests from colliding when run twice, in parallel, or against a shared server that still contains yesterday's leftovers.
- The `qea-` prefix marks data as created by tests. If cleanup ever fails, a person (or a sweeper script) can recognise and remove it: "delete everything whose title starts with `qea-`".
- `payload.update(overrides)` merges the overrides over the defaults, and the function returns a **new** dictionary each time, so one test cannot accidentally change another's data (a classic bug when people share a module-level dictionary).

> **Non-ASCII text.** `requests` serialises with `json.dumps`, which escapes non-ASCII characters as `\uXXXX` (we saw `"é"` become `"é"` on the wire). That is valid JSON and servers decode it correctly. Just do not be alarmed when you see escapes in logs.

### 8. Query Parameters and Path Parameters

Monday's lesson distinguished the two; here is how each looks in code. **Query parameters** filter or shape a collection. Pass a dictionary to `params=` rather than building `?a=b&c=d` yourself:

```python
def test_list_with_query_params(api):
    response = api.get("/posts", params={"userId": 1, "_limit": 5})
    assert response.status_code == 200
    posts = response.json()
    assert len(posts) == 5
    assert all(p["userId"] == 1 for p in posts)
```

- `params={"userId": 1, "_limit": 5}` becomes `?userId=1&_limit=5`, and `requests` **URL-encodes** values for you (spaces, `&`, accents). Hand-built strings break the day someone searches for `"R&D"`. (`_limit` is a JSONPlaceholder convention; your API has its own names.)
- `response.json()` parses the body; a JSON array becomes a `list`.
- `len(posts) == 5` checks the limit was honoured.
- `all(p["userId"] == 1 for p in posts)` checks **every** item, not just the first; a filter that ignored half the data would otherwise slip through.

A list value is repeated (`params={"id": [1, 2]}` gives `?id=1&id=2`); whether the API understands that is its own choice, so check the docs.

**Path parameters** identify one resource and are part of the path. Build them with an f-string, `api.get(f"/posts/{post_id}")`, and keep three habits: take IDs from created data or configuration instead of magic numbers (`/users/5` may not exist elsewhere); encode IDs containing special characters with `urllib.parse.quote(value, safe="")`; and test absence too:

```python
def test_missing_post_is_404(api):
    assert api.get("/posts/999999").status_code == 404
```

### 9. Headers in Tests

Monday explained what headers mean. In test code you meet them in three places.

- **Session-level headers** apply to every request; the client sets `Accept` and `User-Agent` once.
- **Per-request headers** are merged over the session's, and the per-request value wins on a clash: `api.get("/posts/1", headers={"Accept": "application/xml"})` replaces `Accept` for that call only. This is how you test content negotiation (an unsupported format usually earns `406 Not Acceptable`). Pass `None` as a value to remove a session header for one call.
- **Inspecting what was actually sent** is the best move when a header problem is suspected. `response.request.headers` and `response.request.url` show the final merged headers and encoded URL. The local mock also has an `/echo-headers` endpoint that returns the headers it received (httpbin.org's `/headers` is a public equivalent):

```python
def test_every_request_carries_headers(api):
    sent = api.get("/echo-headers").json()
    assert sent["Accept"] == "application/json"
    assert sent["X-Request-Id"]
    assert sent["User-Agent"].startswith("qea-api-tests")
```

The endpoint returns a JSON object of header names and values; the test confirms the session default arrived, that the client generated a non-empty request ID, and that `User-Agent` starts with our name (without hard-coding a version). Header **names** are case-insensitive, so `response.headers["content-type"]` works. Authentication headers (`Authorization: Bearer ...`) are set the same way, but the credential must come from configuration and never be logged; the headers and authentication lesson covers this, and the session is the natural place to attach it once.

### 10. Asserting on Response Basics

An **assertion** is a statement that must be true for the test to pass. PyTest uses Python's plain `assert` keyword and, when one fails, rewrites the message to show both sides. The **basics** worth checking on nearly every response are:

1. The **status code** (did the call succeed, or fail in the expected way?).
2. The **content type** (is it really JSON?).
3. That the body **parses** and has the fields you care about.
4. A few meaningful **headers**.
5. That the **response time** is acceptable (section 16).

```python
def test_read_existing_post(api):
    response = api.get("/posts/1")

    assert response.status_code == 200
    assert response.headers["Content-Type"].startswith("application/json")

    body = response.json()
    assert body["id"] == 1
    assert isinstance(body["title"], str) and body["title"]
```

Line by line:

- `response.status_code` is an integer; compare with an integer, not a string.
- `Content-Type` is usually `application/json; charset=utf-8`, so equality with `"application/json"` would fail; use `startswith`.
- `response.json()` parses the body; if it is not valid JSON (an HTML error page from a proxy, say) this raises, which is itself informative.
- `body["id"] == 1` verifies the server returned the resource we asked for, catching endpoints that ignore the path parameter.
- `isinstance(body["title"], str) and body["title"]` checks the title is text *and* non-empty.

Resist the temptation to assert "everything". Assertions on volatile values (timestamps, generated IDs, ordering of unordered lists) create brittle tests. Assert what the API **promises**.

The next lessons today go deeper on status assertions and JSON validation.

#### Make failures explain themselves

A bare `assert response.status_code == 200` fails with `assert 404 == 200`. That tells you nothing about *which* request, *what* URL, or *what* the server said. Add a message built from the request and response:

```python
# helpers/waiting.py  (the describe helper lives beside wait_until)
def describe(response):
    """One readable string for assertion messages."""
    req = response.request
    return (f"{req.method} {req.url} -> {response.status_code} "
            f"in {response.elapsed.total_seconds() * 1000:.0f} ms\n"
            f"body: {response.text[:300]}")
```

And use it as the second part of an `assert`:

```python
def test_deliberate_failure(api):
    response = api.get("/posts/999999")
    assert response.status_code == 200, describe(response)
```

The report on the local mock (trimmed):

```text
>       assert response.status_code == 200, describe(response)
E       AssertionError: GET http://127.0.0.1:8802/posts/999999 -> 404 in 1 ms
E         body: {}
E       assert 404 == 200
E        +  where 404 = <Response [404]>.status_code
```

Line by line of the helper:

- `response.request` is the request that produced the response, carrying `.method` and `.url` (with query string).
- `response.text[:300]` shows the first 300 characters of the body, where servers often explain the error ("title is required"), without a huge HTML page burying the report.

### 11. A Session Fixture, Fixture-Light

A **fixture** is a PyTest function that prepares something tests need and hands it over by name. The fixtures lesson later today covers them in full; today you need just enough to share one client across tests instead of building a new one per test or in a global variable.

```python
# tests/conftest.py
import pytest

from api.client import ApiClient
from config import settings


@pytest.fixture(scope="session")
def api():
    client = ApiClient(
        settings.BASE_URL,
        timeout=(settings.CONNECT_TIMEOUT, settings.READ_TIMEOUT),
        retries=settings.RETRIES,
    )
    yield client
    client.session.close()
```

Line by line:

- `conftest.py` is loaded automatically by PyTest; its fixtures are available to every test file beside it with no import.
- `scope="session"` runs the fixture **once per run**, so all tests share one `requests.Session` and its pooled connections.
- Everything before `yield` is **setup**, the yielded value is what tests receive, and everything after is **teardown**, run after the last test (here, closing the session).

A test simply names the fixture as a parameter and PyTest passes it in:

```python
def test_read_existing_post(api):      # `api` is the client from conftest.py
    ...
```

Sharing one session is safe for read-only defaults. The risk is *mutating* it inside a test (`api.session.headers["Authorization"] = ...`), which leaks into every later test; pass per-request headers or build a separate client, as the timeout test did.

### 12. The Full CRUD Flow

CRUD stands for **C**reate, **R**ead, **U**pdate, **D**elete, the four things you can do to a record. It maps onto HTTP like this:

| Operation | HTTP method | Typical success status |
|-----------|-------------|------------------------|
| Create | `POST /posts` | `201 Created` |
| Read | `GET /posts/{id}` | `200 OK` |
| Update | `PUT /posts/{id}` (replace) or `PATCH /posts/{id}` (partial) | `200 OK` |
| Delete | `DELETE /posts/{id}` | `200 OK` or `204 No Content` |

Testing the whole lifecycle matters because defects hide in the *connections*: a record created correctly but stored with the wrong owner, an update that silently fails to save, a delete that leaves a stale record readable. Single-call tests rarely catch these.

There are two honest ways to test CRUD, and which applies depends on the target.

#### Step 1: Contract tests that work on any API, including fake ones

Each operation is tested on its own, checking what the **response** promises:

```python
def test_create_post_echoes_payload(api):
    payload = make_post_payload()
    response = api.post("/posts", json=payload)
    assert response.status_code == 201, describe(response)
    created = response.json()
    assert isinstance(created["id"], int)
    assert {k: created[k] for k in payload} == payload


def test_update_post_with_put(api):
    payload = {"id": 1, "title": "new title", "body": "b", "userId": 1}
    response = api.put("/posts/1", json=payload)
    assert response.status_code == 200
    assert response.json()["title"] == "new title"


def test_partial_update_with_patch(api):
    response = api.patch("/posts/1", json={"title": "patched"})
    assert response.status_code == 200
    assert response.json()["title"] == "patched"


def test_delete_post(api):
    assert api.delete("/posts/1").status_code in (200, 204)
```

Line by line, focusing on the new ideas:

- In the create test, `isinstance(created["id"], int)` checks the server assigned an integer ID without caring which one (we cannot predict it).
- `{k: created[k] for k in payload} == payload` is a **dictionary comprehension**: it builds a new dictionary containing only the keys we sent, with the values the server returned, and compares it to what we sent. In words: "everything I sent came back unchanged". The server may add extra fields such as `id`; those are ignored by this comparison, which is exactly what we want.
- `PUT` replaces the whole record, so the payload carries every field. `PATCH` changes only what is listed, so it sends just `title`.
- `in (200, 204)` accepts either success status for delete, because APIs differ. Once you know your API's contract, tighten this to one value; a vague assertion is a weak one.

Against JSONPlaceholder (and our fake-mode mock) these four pass, because they only check what the response says.

#### Step 2: The lifecycle test for APIs that really store data

When the target persists writes (your Project 2 system should), test the **journey**, because that is where integration defects live:

```python
@pytest.mark.skipif(not settings.PERSISTS_WRITES, reason="API does not store writes")
def test_full_crud_flow(api, created_post):
    post_id = created_post["id"]

    # READ: the created record can be fetched
    assert api.get(f"/posts/{post_id}").json()["title"] == "temp post"

    # UPDATE: change it, then confirm the change was stored
    updated = api.put(f"/posts/{post_id}",
                      json={**created_post, "title": "edited"})
    assert updated.status_code == 200
    assert api.get(f"/posts/{post_id}").json()["title"] == "edited"

    # DELETE: remove it, then confirm it is really gone
    assert api.delete(f"/posts/{post_id}").status_code in (200, 204)
    assert api.get(f"/posts/{post_id}").status_code == 404
```

Line by line:

- `@pytest.mark.skipif(condition, reason=...)` makes PyTest **skip** the test (reported as `s`, not as a failure) when the condition is true. Here the condition is "the API does not persist writes", driven by the `API_PERSISTS_WRITES` setting. The skip is an honest statement: "this check is meaningless against a fake API". It is better than deleting the test or letting it fail for a reason unrelated to quality.
- The test takes a second fixture, `created_post`. PyTest builds it first: it **creates** the post (the "C" of CRUD) and yields the record. You will see its code in section 13, and notice the test body never has to create or clean up.
- The first `GET` proves the create actually stored the record with the right title (the "R").
- `{**created_post, "title": "edited"}` builds a new dictionary containing everything from `created_post` but with the title replaced. The `**` unpacks the dictionary into the new one, and later keys win.
- The `PUT` and the `GET` after it are the "U": it is not enough that `PUT` said `200`; we re-read to confirm the change was stored. A server that returns `200` and discards the update is a real kind of bug.
- The `DELETE` and the final `GET` expecting `404` are the "D": we confirm the record is gone, not merely that delete answered `200`.

Why the `skipif` rather than two different tests? Because one flow, written once, adapts to both worlds through configuration. You will see this idea again in the framework lesson later in the week.

#### What running it looks like

Local mock, fake-writes server (`API_PERSISTS_WRITES` unset):

```text
.......s....                                                             [100%]
SKIPPED [1] tests/test_posts_crud.py:53: API does not store writes
11 passed, 1 skipped in 0.94s
```

Local mock, persisting server (`API_PERSISTS_WRITES=true`), with the same test files:

```text
............                                                             [100%]
12 passed in 0.95s
```

The single `s` in the first run is the lifecycle test being skipped; in the second run it executes and passes. (Run against the real public JSONPlaceholder, you should see the same pattern as the first run, with times typically a few hundred milliseconds per test: **representative**, as network conditions vary.)

The practical answer is **both**: a few journey tests as a smoke check (if step 2 fails you never learn about steps 3 and 4), and many independent tests for detail (a failure points to exactly one behaviour).

### 13. Creating Test Data and Cleaning It Up

Most failures in suites that "worked yesterday" trace back to leftover data. A test that creates a record and fails halfway leaves the record behind; the next run finds it and trips. Disciplined data handling avoids this.

Three rules:

1. **Each test creates the data it needs.** It does not rely on a record "that should already be there".
2. **Each test removes what it created**, even when it fails.
3. **Data is uniquely named** (the `qea-` prefix plus random characters from section 7) so nothing collides and leftovers are identifiable.

(How tests are isolated from one another more broadly is covered on Wednesday; today is about the personal discipline of creating and cleaning.)

#### Cleanup with try/finally

```python
@pytest.mark.skipif(not settings.PERSISTS_WRITES, reason="needs a persisting API")
def test_update_changes_title_and_cleans_up(api):
    created = api.post("/posts", json=make_post_payload()).json()
    post_id = created["id"]
    try:
        response = api.put(f"/posts/{post_id}",
                           json={**created, "title": "New title"})
        assert response.status_code == 200
        assert response.json()["title"] == "New title"
    finally:
        api.delete(f"/posts/{post_id}")
```

The `skipif` line is there because this test updates a record it just created. On the real JSONPlaceholder, `PUT /posts/101` fails (it answers `500`, since post 101 does not really exist), and our fake-writes mock reproduces that. The pattern is for APIs that persist data.

How it works: Python runs the code in `try`; whether it finishes normally or an assertion raises, the `finally` block **always** runs afterwards. So the post is deleted whether the test passed or failed.

It works, but you can see the cost: every test that creates data wraps itself in the same four lines, and one forgotten `finally` leaves debris.

#### Cleanup with a fixture that yields

A fixture removes the repetition. This is the `created_post` fixture used by the lifecycle test:

```python
# tests/conftest.py (continued)
@pytest.fixture
def created_post(api):
    payload = {"title": "temp post", "body": "created by a test", "userId": 1}
    response = api.post("/posts", json=payload)
    assert response.status_code == 201, response.text
    post = response.json()
    yield post
    api.delete(f"/posts/{post['id']}")
```

Line by line:

- No `scope` argument means the default, `function`: a **fresh** post is created for each test that asks for it, and removed afterwards.
- The assertion right after the `POST` makes a failure in setup obvious: "could not create the post" is a very different diagnosis from "the update is broken".
- `yield post` hands the record to the test. Everything after `yield` is teardown, and PyTest runs it **even if the test failed**, just like `finally`.
- The `DELETE` removes the record. Tests simply write `def test_x(api, created_post):` and forget about cleanup.

#### A factory fixture for tests that need several records

Sometimes a test needs two or three posts, or posts with specific titles. Rather than writing a fixture per case, hand the test a **function** that creates records on demand and remembers them for cleanup:

```python
import logging

import pytest
import requests

from helpers.waiting import describe

logger = logging.getLogger("api")


@pytest.fixture
def post_factory(api):
    created_ids = []

    def make(**overrides):
        payload = {"title": "temp", "body": "b", "userId": 1, **overrides}
        response = api.post("/posts", json=payload)
        assert response.status_code == 201, describe(response)
        post = response.json()
        created_ids.append(post["id"])
        return post

    yield make

    for post_id in reversed(created_ids):
        try:
            api.delete(f"/posts/{post_id}")
        except requests.RequestException as exc:
            logger.warning("cleanup of post %s failed: %s", post_id, exc)
```

Line by line:

- `created_ids = []` is a list that lives as long as the fixture and records every ID the factory makes.
- `make(**overrides)` is a function defined *inside* the fixture (a **closure**): it can see `api` and `created_ids`. Each call creates one post, remembers its ID, and returns the record. `{..., **overrides}` merges the caller's values over the defaults.
- `yield make` gives the test the function itself, not data.
- After the test, the loop deletes every recorded ID. `reversed(...)` deletes in the opposite order of creation, which matters when later records depend on earlier ones (comments depend on posts; delete children first).
- The `try/except` makes cleanup **best-effort**: if one delete fails because the network blipped, we log a warning and carry on deleting the rest rather than aborting halfway. A cleanup failure should never mask the real test result.

A test using it:

```python
def test_factory(api, post_factory):
    a = post_factory(title="A")
    b = post_factory(title="B")
    assert a["id"] != b["id"]
```

On the persisting local mock this passed, and afterwards both posts were removed.

#### When cleanup itself fails

Log it, do not raise it (as above), so the test's verdict reflects what it was checking. Name data so leftovers are findable (the `qea-` prefix) and consider a periodic sweeper (Exercise 4). Never clean up with a blanket query such as "delete every post"; delete only what *you* created. Some real APIs forbid deletion and "archive" instead, so ask the API's owners how test data is meant to be removed.

### 14. Idempotency and Test Ordering

#### What idempotent means

An operation is **idempotent** if doing it once or doing it many times in a row leaves the system in the same state. (Idempotent, pronounced "eye-dem-POH-tent", comes from Latin for "the same power".) The everyday analogy is an elevator button: pressing "Floor 5" once, or ten times, results in the same thing, the elevator goes to floor 5. Compare a vending machine: pressing "buy" ten times buys ten snacks.

HTTP assigns these properties by method:

| Method | Idempotent? | Why |
|--------|-------------|-----|
| `GET` | Yes | Reading changes nothing |
| `PUT` | Yes | "Make the record look like this" gives the same result however often it is applied |
| `DELETE` | Yes (in effect) | After the first delete the record is gone; later ones leave it gone (though the *status* may differ: `200`/`204` first, then maybe `404`) |
| `POST` | **No** | Each call typically creates another new record |
| `PATCH` | Not guaranteed | Depends on the change ("set title" is repeatable; "increase count by one" is not) |

Here is the difference on the persisting local mock, calling the client twice in a row:

```text
POST 102
POST 103
PUT  {'title': 'same', 'id': 5}
PUT  {'title': 'same', 'id': 5}
DELETE 200
DELETE 200
GET after delete 404
```

Two identical `POST`s created **two different records** (IDs 102 and 103). Two identical `PUT`s returned the **same** result. Two `DELETE`s both answered `200` on this mock, and the record was gone afterwards. (A real API might answer `404` to the second delete; both behaviours are common, which is why a robust cleanup does not insist on a particular status.)

#### Why testers care

1. **Retrying a non-idempotent call can do harm.** If a `POST` times out you do not know whether the record was created; resending might duplicate an order or a charge. That is why section 17 retries only `GET`, `HEAD`, `OPTIONS`, `PUT`, and `DELETE`.
2. **The promise itself is testable.** "Two identical `PUT`s give the same record" is a valuable test, as is "two `POST`s create two records" (or one, if the API promises de-duplication with an idempotency key).
3. **Re-runnable tests need idempotent setup.** A fixed email in setup fails on the second run with "already exists"; unique data (section 7) fixes it.

#### Test ordering: never depend on it

PyTest normally runs tests in the order they appear in the file, and beginners are tempted to exploit this:

```python
# DON'T: test_b depends on test_a having run first
created_id = None

def test_a_create(api):
    global created_id
    created_id = api.post("/posts", json=make_post_payload()).json()["id"]

def test_b_read(api):
    assert api.get(f"/posts/{created_id}").status_code == 200   # breaks if test_a is skipped
```

Why this is fragile: run `test_b_read` alone and it fails (`created_id` is `None`); if `test_a_create` fails, `test_b_read` fails too, giving two red tests for one defect; and tools that run tests in **parallel** or **random order** (common in CI to expose hidden dependencies) break the suite unpredictably.

The remedy is the one you already know: each test creates its own data (via a fixture) and cleans it up. If you genuinely want a multi-step journey, write it as **one** test (section 12, step 2) so the dependency is explicit and contained.

A quick independence check: run one test by name (`pytest -k name`), run in shuffled order (the `pytest-randomly` plugin), and run the file twice. If any fails while a normal run passes, you have a hidden dependency.

### 15. Logging Requests and Responses for Debugging

When a test fails at 2 a.m. in a pipeline, the report is all you have. A good report answers: what was sent, to where, what came back, and how long it took. Our client already logs this at `INFO` level (request, then response) and at `DEBUG` level (the first 500 characters of the body).

Sample output from the client (local mock):

```text
INFO api: -> GET http://127.0.0.1:8802/posts params={'userId': 1, '_limit': 2} json=None
INFO api: <- 200 in 2 ms
INFO api: -> POST http://127.0.0.1:8802/posts params=None json={'title': 'x', 'body': 'y', 'userId': 1}
INFO api: <- 201 in 1 ms
```

Read each line as a sentence: `->` is the outgoing request (method, full URL, query parameters, JSON body); `<-` is the response (status and elapsed milliseconds). On the real public host, expect the numbers to be larger (tens to a few hundred ms is **representative**).

#### Where the logs appear

- By default PyTest **captures** logging output and shows it in a "Captured log call" section **only for tests that fail**. Passing tests stay quiet, so you get detail exactly when you need it. You saw this in the failure report: in the deliberate failure above, PyTest printed

```text
------------------------------ Captured log call -------------------------------
09:44:12 INFO api: -> GET http://127.0.0.1:8802/posts/999999 params=None json=None
09:44:12 INFO api: <- 404 in 1 ms
```

- To watch logs live while tests run (useful while developing), run `pytest -o log_cli=true --log-cli-level=INFO`. Here `-o` overrides a configuration option for this run only.
- To save logs to a file that a pipeline can keep as an artifact, use `--log-file=test.log --log-file-level=DEBUG`. (Friday's lessons on artifacts explain how pipelines keep such files.)
- A noisy library can be quieted without silencing yours: `logging.getLogger("urllib3").setLevel(logging.WARNING)`. At `DEBUG` level `urllib3` logs every connection event, which is occasionally exactly what you need for a flaky-network mystery and usually clutter otherwise.

`print` output is unlabelled, unleveled, and cannot be redirected; `logging` gives levels, timestamps, names, and one-setting file output, and it is what `requests` and `urllib3` already use.

#### Four logging habits

1. **Log both directions**; a request with no logged response looks identical to a hang.
2. **Log failures at `ERROR` with the exception name** (`ReadTimeout` versus `ConnectionError` tells you where to look).
3. **Include the request ID** in the request line so a developer can search the server's logs.
4. **Never log secrets.** Authorization headers, passwords, tokens, and personal data can live in logs for months. Our client logs only `params` and `json`, never headers; mask sensitive payload fields.

### 16. Response-Time Assertions

Sometimes the requirement is "fast enough", not just "correct". `response.elapsed` is the time from sending the request until the response headers were parsed (not the download of a large body, nor DNS before sending; for small JSON responses that distinction is academic).

```python
def test_fast_enough(api):
    response = api.get("/posts/1")
    elapsed_ms = response.elapsed.total_seconds() * 1000
    assert elapsed_ms < settings.MAX_RESPONSE_MS, f"took {elapsed_ms:.0f} ms"
```

`.total_seconds() * 1000` converts the `timedelta` to milliseconds; the threshold comes from settings (default 2000), so a slow environment can be given a looser limit without editing code; the message after the comma appears only on failure.

The default is deliberately generous because a single measurement is **noisy**: a pause on a shared CI runner, a cold connection, or a network spike can make one call several times slower than usual, and a tight threshold on one sample produces flaky failures. To keep timing assertions meaningful:

- **Set thresholds from requirements**, not from the fastest run you have seen. If the agreement is "95% under 500 ms", then a 2000 ms functional check catches only disasters, which is the right job for it.
- **Use the median of several samples** when you need tighter checks:

```python
import statistics

def test_median_latency(api):
    samples = [api.get("/posts/1").elapsed.total_seconds() * 1000 for _ in range(5)]
    assert statistics.median(samples) < 2000, f"samples (ms): {samples}"
```

The list comprehension makes five requests and records each time; `statistics.median` returns the middle value and ignores one-off spikes. (Passed on the local mock.)

- **Keep timeout and threshold separate.** The timeout stops a call hanging; the assertion judges a call that completed. A 10 s timeout with a 2 s assertion is sensible.
- **Do not confuse this with performance testing**, which uses specialised tools, concurrent load, and percentiles. A timing assertion is a cheap sanity alarm, not a benchmark.

### 17. Handling a Flaky Network

A **flaky** test sometimes passes and sometimes fails with no change to the code. Network calls are a leading cause. Typical moments of flakiness: a load balancer answers `503 Service Unavailable` while a server restarts, a gateway returns `502`/`504` for a few seconds, a TCP connection is reset, a DNS lookup hiccups, a public API throttles you.

First, separate two very different situations:

- A **transient infrastructure failure**: the same request would succeed a moment later. Retrying is reasonable.
- A **genuine defect**: the API consistently returns the wrong thing. Retrying would only waste time or, worse, hide the bug.

A retry policy must target the first kind and never mask the second.

#### Retrying with the session

The client's constructor installs a retry policy using `urllib3`'s `Retry`, mounted on the session through an adapter. Here is that block again, with the meaning of each setting:

```python
retry = Retry(
    total=retries,                       # at most this many retries per request
    backoff_factor=0.2,                  # growing pause between attempts
    status_forcelist=[502, 503, 504],    # retry when the server answers these
    allowed_methods=frozenset(["GET", "HEAD", "OPTIONS", "PUT", "DELETE"]),
    respect_retry_after_header=True,     # obey the server's Retry-After header
    raise_on_status=False,               # after the last try, return the response
)
adapter = HTTPAdapter(max_retries=retry)
self.session.mount("http://", adapter)
self.session.mount("https://", adapter)
```

- `total=retries` caps retries; with `RETRIES=2` a request is tried at most three times.
- `backoff_factor=0.2` makes pauses grow exponentially (with `urllib3` 2.x: 0 s, 0.4 s, 0.8 s, 1.6 s, and so on; exact behaviour varies by version). **Backoff** gives a struggling server breathing room.
- `status_forcelist=[502, 503, 504]` lists the **server-side, probably temporary** statuses. `400`, `401`, `404`, and `500` are absent on purpose: a `404` stays a `404`, and a `500` is more often a real bug than a hiccup.
- `allowed_methods` limits retries to **idempotent** methods (section 14); `POST` is excluded so a retried create cannot duplicate.
- `respect_retry_after_header=True` obeys a server's `Retry-After` header (from Monday's lesson).
- `raise_on_status=False` matters for testing: without it, once retries run out `urllib3` raises a `RetryError` that hides the last response. With it you receive the final `503` as an ordinary `Response` to assert on or log.
- `session.mount(prefix, adapter)` attaches the adapter to every URL with that prefix; mounting both schemes covers all targets.

The local mock's `/flaky` endpoint answers `503` for its first N calls and `200` afterwards, so we can prove the policy works:

```python
def test_retry_recovers_from_503():
    client = ApiClient(settings.BASE_URL, retries=3)
    client.get("/flaky/reset")
    response = client.get("/flaky", params={"fails": 2})
    assert response.status_code == 200
    assert response.json()["attempt"] == 3
```

A client with up to three retries is built; `/flaky/reset` clears the mock's counter; the call fails twice with `503` and succeeds on the third attempt (`attempt: 3`). The test passed on the local mock, and never saw the two `503`s.

Two cautions:

- **Retries are a bandage for infrastructure, not a cure for bugs.** If the suite needs them regularly, find out why the environment is unstable; 2 or 3 retries are plenty.
- **Keep retries visible.** `urllib3` logs a `WARNING` per retry; a green run that needed retries should still be noticed.

#### Polling instead of sleeping

Another source of flakiness is **timing**: the test checks for a result before the server has finished producing it (for instance, after starting a background job). The wrong fix is `time.sleep(5)` everywhere: too short and the test is still flaky, too long and the suite is slow. The right fix is to **poll with a limit**: check repeatedly, succeed the moment the condition holds, and give up after a deadline.

```python
# helpers/waiting.py
import time


def wait_until(check, timeout=10.0, interval=0.5):
    """Call check() until it returns something truthy or timeout expires."""
    deadline = time.monotonic() + timeout
    while True:
        result = check()
        if result:
            return result
        if time.monotonic() >= deadline:
            return None
        time.sleep(interval)
```

Line by line:

- `check` is a **function** passed in as an argument (functions are values in Python). The helper calls it repeatedly.
- `time.monotonic()` is a clock that only moves forward, unlike `time.time()`, which can jump if the system clock is adjusted. It is the correct clock for measuring durations.
- `deadline` is the moment to stop.
- The loop calls `check()`. A truthy result is returned immediately, so the test proceeds as fast as the server allows. If time is up, it returns `None`, which is falsy. Otherwise it sleeps for `interval` and tries again.
- Checking *before* sleeping means an already-true condition costs no wait at all.

Using it (a hypothetical jobs endpoint, so illustrative only):

```python
job_id = api.post("/jobs", json={"type": "export"}).json()["id"]
finished = wait_until(
    lambda: api.get(f"/jobs/{job_id}").json()["status"] == "done",
    timeout=15,
    interval=1,
)
assert finished, "job did not finish within 15 seconds"
```

`lambda: ...` is a tiny nameless function: "fetch the job and report whether its status is `done`". The helper asks until the answer is yes or 15 seconds pass. We tested the helper itself on the local mock: a condition true on its third call returned quickly, and one never true returned `None` after the limit.

#### Other flakiness habits

- Run a cheap health check at the start of a run so an unhealthy environment fails once, clearly (Exercise 3).
- Do not depend on external services you do not control; replacing them with stand-ins is mocking, covered on Wednesday.
- Treat automatic rerun plugins (such as `pytest-rerunfailures`) with care: they can hide real intermittent bugs. Track flaky tests and fix or quarantine them.

### 18. Common Mistakes and How to Avoid Them

| Mistake | What happens | Better habit |
|---------|--------------|--------------|
| No `timeout` on a call | A silent server freezes the run | Set a (connect, read) timeout in the client |
| `data=` instead of `json=` for a JSON API | Form-encoded body; `400`/`415` or ignored fields | Use `json=` |
| Hand-built query strings | Unescaped `&` or spaces break the request | Pass a dictionary to `params=` |
| Hard-coded base URL | Changing environment means editing many files | One settings module reading env vars |
| Parsing the body before checking status | A `404` HTML page raises a confusing `JSONDecodeError` | Assert status first |
| Expecting read-back after `POST` on JSONPlaceholder | `404`, because writes are faked | Know the target; use `skipif` or a persisting API |
| Magic IDs (`/users/5`) | Breaks when data changes | Create data or take IDs from a fixture |
| Tests that share data or depend on order | Cascading failures; parallel runs break | Each test creates and cleans its own data |
| Cleanup only on the happy path | A failed test leaves debris | `try/finally` or `yield` fixture |
| Retrying `POST`, or retrying every status | Duplicates; hidden bugs | Retry only idempotent methods and `502/503/504` |
| `time.sleep(5)` to wait for a job | Slow or flaky | `wait_until` with a deadline |
| Tight timing threshold on one sample | Random failures | Generous threshold or the median |
| Logging secrets | Credentials persist in CI logs | Log safe fields only |
| Bare `assert status == 200` | Failure lacks URL and body | Add `describe(response)` |

### 19. Practice Exercises

Each exercise has a full solution after it. Try it yourself first; run everything with the local mock or with the public JSONPlaceholder host. The persisting-mode exercises need an API that really stores data (your Project 2 system, or any API you control); on JSONPlaceholder, read their solutions and reason about the expected outcome instead.

#### Exercise 1: Filter by query parameter and verify every item

Write a test that requests the posts written by user 3 and asserts that exactly ten posts are returned and each belongs to user 3.

**Solution.**

```python
def test_posts_for_user_3(api):
    response = api.get("/posts", params={"userId": 3})
    assert response.status_code == 200, describe(response)
    posts = response.json()
    assert len(posts) == 10
    assert {p["userId"] for p in posts} == {3}
```

Explanation: `{p["userId"] for p in posts}` is a **set comprehension**: it collects the distinct `userId` values. If every post belongs to user 3 the set is exactly `{3}`. If the filter leaked a post from another user, the set would contain a second number and the assertion would show it. This is a compact way to say "all items satisfy X". (This passed on the local mock, whose data mimics JSONPlaceholder's ten posts per user.)

#### Exercise 2: Prove idempotency in tests

Write one test showing that two identical `PUT` requests give identical results, and one showing that two identical `POST` requests create two different records. Use the persisting target for the `POST` test.

**Solution.**

```python
def test_put_is_idempotent(api):
    body = {"id": 1, "title": "same every time", "body": "b", "userId": 1}
    first = api.put("/posts/1", json=body)
    second = api.put("/posts/1", json=body)
    assert first.status_code == second.status_code == 200
    assert first.json() == second.json()


@pytest.mark.skipif(not settings.PERSISTS_WRITES, reason="needs a persisting API")
def test_post_is_not_idempotent(api, post_factory):
    payload = make_post_payload()
    first = post_factory(**payload)
    second = post_factory(**payload)
    assert first["id"] != second["id"]
```

Explanation: `first.status_code == second.status_code == 200` is a chained comparison: all three values must be equal. For `POST` we reuse the factory fixture so both created records are deleted afterwards. If your API supports an idempotency key header, the second test is where you would verify that the same key produces **one** record. On the persisting local mock both tests passed; the `PUT` test also passes on the fake-writes mock because it only compares responses.

#### Exercise 3: Fail fast when the API is down

If the API is unreachable, a suite of 200 tests would produce 200 slow errors. Add a session-wide check that stops the run immediately with one clear message.

**Solution.**

```python
# tests/conftest.py (add)
import requests


@pytest.fixture(scope="session", autouse=True)
def api_is_up(api):
    try:
        api.get("/posts/1", timeout=(2, 3))
    except requests.exceptions.RequestException as exc:
        pytest.exit(f"API unreachable at {settings.BASE_URL}: {exc}", returncode=2)
```

Explanation: `autouse=True` makes PyTest run the fixture for every session without any test naming it. It makes one cheap request with a short timeout. If that raises any `requests` exception, `pytest.exit(...)` aborts the entire run at once with a one-line explanation and exit code 2, instead of letting every test fail separately. Note that this check is only about **reachability**; a `404` from the health request still counts as "the server answered".

#### Exercise 4: A sweeper for leftover test data

Imagine a failed run left posts titled `qea-...` behind on a shared server. Write a function that deletes every post whose title starts with `qea-`, touching nothing else. (Use a persisting API.)

**Solution.**

```python
def sweep_test_posts(api):
    posts = api.get("/posts").json()
    leftovers = [p for p in posts if p["title"].startswith("qea-")]
    for post in leftovers:
        api.delete(f"/posts/{post['id']}")
    return len(leftovers)
```

Explanation: it lists the posts, keeps only those carrying the test prefix (a list comprehension with a condition), deletes each, and returns the count so a script can report "removed 3 leftover posts". The prefix we put on generated data in section 7 is exactly what makes this safe: it can never match a real person's post. In a real system you would also restrict by age or owner and require a confirmation flag before running against anything but a test environment. (On the persisting local mock, creating two `qea-` posts and running the function returned `2` and left the other posts untouched.)

### 20. Self-Check Quiz

Try to answer without looking back, then compare with the answers below.

1. What happens if you call `requests.get(url)` with no `timeout`, and the server accepts the connection but never replies?
2. In `timeout=(3.05, 10)`, what do the two numbers mean?
3. You `POST` a new post to JSONPlaceholder, receive `201` and `id: 101`, then `GET /posts/101` and receive `404`. Is JSONPlaceholder broken?
4. Why does the client's retry policy leave `POST` out of `allowed_methods`?
5. Why is `finally` (or a `yield` fixture) better than putting the delete call at the end of the test body?
6. Why is `assert elapsed_ms < 200` on a single request a risky test?
7. Two tests share a global variable: the first sets it, the second reads it. Name two ways this goes wrong.

**Answers**

1. It waits indefinitely. Without a timeout `requests` never gives up, so an unattended pipeline could hang until the CI system kills the job. Always pass a timeout.
2. The first number is the **connect** timeout (time allowed to establish the connection). The second is the **read** timeout (time allowed to wait for the server's data, in practice the first byte of the response and each later gap between bytes).
3. No. JSONPlaceholder deliberately **fakes** writes: it answers as if the record were created but stores nothing. Tests for a read-after-create flow belong against an API that persists data, or should be skipped with a stated reason.
4. `POST` is not idempotent. If a `POST` times out, the server may already have created the record; a retry could create a duplicate. Idempotent methods (`GET`, `PUT`, `DELETE`, and so on) are safe to repeat.
5. Code after a failed assertion never runs, because the assertion raises an exception and leaves the test. `finally` and fixture teardown run regardless of pass or fail, so cleanup always happens.
6. One sample is noisy; a slow moment on a shared runner, a cold connection, or a network spike would fail the test with no real defect. Use generous thresholds from requirements, or the median of several samples.
7. (Any two.) Running the second test alone fails because the variable is empty; if the first test fails the second fails too, giving two red tests for one cause; parallel or randomised ordering breaks it unpredictably; renaming or reordering changes behaviour silently.

### 21. Glossary

- **API client** - a class (here `ApiClient`) that is the single place requests are built and sent.
- **Assertion** - a statement that must be true for a test to pass (`assert`).
- **Backoff** - a growing pause between retries.
- **Base URL** - the fixed first part of every request URL.
- **Closure** - a function defined inside another that can use the outer function's variables.
- **Connect timeout / read timeout** - the maximum wait to establish a connection / to receive data once connected.
- **Correlation ID (request ID)** - a unique value such as `X-Request-Id` that lets one call be found in logs on both sides.
- **CRUD** - Create, Read, Update, Delete.
- **Environment variable** - a named text value supplied by the operating system or pipeline, read with `os.getenv`.
- **Factory fixture** - a fixture that yields a function for creating test data on demand and cleans up afterwards.
- **Fixture** - a PyTest function that prepares (and tears down) something tests need, injected by parameter name.
- **Flaky test** - a test that sometimes passes and sometimes fails with no code change.
- **Idempotent** - leaving the system in the same state whether performed once or many times.
- **Payload** - the data sent in a request body.
- **Persisting API** - one that really stores what you write, unlike JSONPlaceholder.
- **Polling** - checking a condition repeatedly until it holds or a deadline passes.
- **Session (`requests.Session`)** - an object that reuses connections and carries default headers across requests.
- **Teardown** - code that undoes what a test created; in a `yield` fixture, the code after `yield`.
- **Transient failure** - a temporary fault (such as a brief `503`) that disappears on retry.

---

## Summary

- Automated tests replace the human judgement you used in Postman, so a hang, a failure, a slow reply, and the wrong server must all become explicit code.
- Read the base URL, timeouts, and thresholds from environment variables in one settings module.
- Send every request through one `ApiClient` built on a `requests.Session`.
- **Every request needs a timeout**; know `ConnectTimeout`, `ReadTimeout`, and `ConnectionError` apart.
- Use `json=`, `params=`, and f-strings for bodies, query strings, and path parameters; generate unique, recognisable test data.
- Assert on status, content type, body, key headers, and elapsed time, and attach `describe(response)` to failures.
- JSONPlaceholder fakes writes: test each response everywhere, and test the full CRUD journey against a persisting API with `skipif`.
- Create and clean up your own data (`try/finally` or `yield` fixtures); never depend on order; retry only idempotent methods.
- Log both directions of each call, never secrets; keep timing assertions generous; poll with a deadline instead of sleeping.

Covered on Wednesday: running tests over many inputs from files, mocking external services, and test isolation. Covered on Friday: running these tests in a CI/CD pipeline and managing secrets there.

## Additional Resources

- Requests documentation, *Quickstart* (timeouts, JSON, params, headers): https://requests.readthedocs.io/en/latest/user/quickstart/
- Requests documentation, *Advanced Usage* (sessions, timeouts, transport adapters): https://requests.readthedocs.io/en/latest/user/advanced/
- urllib3 documentation, *Retry utility*: https://urllib3.readthedocs.io/en/stable/reference/urllib3.util.html#urllib3.util.Retry
- PyTest documentation, *How to use fixtures*: https://docs.pytest.org/en/stable/how-to/fixtures.html
- PyTest documentation, *How to manage logging*: https://docs.pytest.org/en/stable/how-to/logging.html
- Python documentation, *Logging HOWTO*: https://docs.python.org/3/howto/logging.html
- MDN Web Docs, *Idempotent*: https://developer.mozilla.org/en-US/docs/Glossary/Idempotent
- JSONPlaceholder guide (resources and routes): https://jsonplaceholder.typicode.com/guide/
