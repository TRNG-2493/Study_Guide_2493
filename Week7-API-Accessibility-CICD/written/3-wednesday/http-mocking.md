# HTTP Mocking

## Learning Objectives

By the end of this lesson you will be able to:

- Explain why tests that call real HTTP services are slow, flaky, risky, and unable to simulate failures, and how mocking fixes this.
- Define the **test double** vocabulary: stub, mock, fake, and spy, and recognise which one you are writing.
- Use the `responses` library with `@responses.activate` and `responses.add` to intercept `requests` calls.
- Match requests by URL, query string, JSON body, and headers, and compute replies with `add_callback`.
- Return several different responses in sequence, and verify calls with `responses.calls` and `assert_call_count`.
- Simulate `4xx` and `5xx` responses, timeouts, and `ConnectionError` by passing an exception as `body`.
- Use `unittest.mock` (`Mock`, `MagicMock`, `patch`, `return_value`, `side_effect`, `assert_called_with`) and apply the rule "patch where it is used".
- Wrap mocks in pytest fixtures, and recognise the risk of mocks drifting away from the real API and when **not** to mock.

---

## Why This Matters

This is the Week 7 epic: taking your API tests from "works on my laptop" to a professional pipeline that runs on every push. A pipeline has demands that a learning exercise does not. It must be **fast** (nobody waits 20 minutes for feedback), **deterministic** (a red build must mean a real bug), and **safe** (a test must never email a real customer or charge a real card).

Until now, every request you wrote travelled over the internet to a real server. That was the right way to learn, and it is still the right way to test a real API (more on that near the end). But as soon as you write code that *calls* an API, such as an `ApiClient` class, a login helper, or a retry wrapper in your framework, real calls become a liability:

| Problem with real calls | Example |
|-------------------------|---------|
| **Slow** | 300 ms per call x 2,000 tests = 10 minutes of waiting |
| **Flaky** | A network blip or third-party outage fails your build for no fault of your code |
| **Expensive or limited** | A payment API charges per call; an SMS API rate-limits you after 100 requests |
| **Side effects** | A test sends a real email, creates a real order, or deletes real data |
| **Cannot reproduce rare conditions** | How do you make a healthy server return `503` exactly twice, then `200`? |
| **Unavailable** | The other team's API is not built yet, or CI has no network access |

Mocking replaces the real server with a controlled imitation that answers exactly how you tell it to. Today you learn the tools. The next Wednesday lesson ("Mocking external APIs") applies them to a realistic third-party scenario, and later lessons cover test isolation and validation in depth. Thursday and Friday build on this when you run suites in CI.

---

## The Concept

### 1. Why Mock? Five Concrete Reasons

**Speed.** A mocked call is a Python function call that returns in microseconds. A suite of 500 mocked tests runs in about a second. The same suite against a real server might take minutes. Fast suites get run often, and tests that get run often catch bugs sooner.

**Determinism.** A deterministic test gives the same result every time for the same code. Real services return changing data (timestamps, counters, other people's records), go down for maintenance, and respond slowly under load. A mock returns the same bytes forever.

**No side effects.** Imagine testing a "send welcome email" feature. Against the real email provider, each run sends a real email. With a mock, nothing leaves your machine, and you can still assert "the provider was called once with this recipient".

**Simulating failures.** Your code must handle `500`, `503`, malformed bodies, dropped connections, and timeouts. You cannot ask a healthy production server to fail on cue. A mock fails whenever you say so.

**Rate limits and quotas.** Many APIs allow only N calls per minute or per month. A test suite that runs 50 times a day can burn through a quota. Worse, you may want to test how your code behaves when it *receives* a `429 Too Many Requests`. With a mock you can send that reply on demand without actually being rate-limited.

**Real-world scenario.** Your team's framework has a `get_with_retry` helper that should retry on `503`. How do you test it? You need a server that fails twice and then succeeds. No real server will do that reliably. A mock does it in four lines.

### 2. Test Double Vocabulary

A **test double** is any stand-in for a real component, like a stunt double in a film. People casually call all of them "mocks", but the precise terms are useful when you read documentation or discuss design.

| Term | What it does | Everyday example |
|------|--------------|------------------|
| **Stub** | Returns canned answers. No logic, no checking. | "When asked for user 1, return this JSON." |
| **Mock** | Has pre-programmed expectations and **records calls** so you can verify interaction. | "Assert the email service was called exactly once with `ana@example.com`." |
| **Fake** | A simplified but *working* implementation. | An in-memory dictionary acting as a database; a callback that computes replies. |
| **Spy** | Wraps the **real** thing and records how it was used, while still doing the real work. | A real function plus a call history. |

A quick way to remember: a **stub** answers, a **mock** answers and remembers, a **fake** actually works (in a simplified way), a **spy** is the real object being watched.

In this lesson, `responses.add(...)` creates a stub; reading `responses.calls` adds the "mock" part (verifying interaction); `add_callback` builds a small fake; and `unittest.mock.patch(..., wraps=...)` can create a spy.

### 3. Where Mocking Fits in API Testing

Two situations are often confused:

1. **Testing the real API (black box).** Your test calls the actual service to check *its* behaviour. You do **not** mock the API under test. If you did, you would only be testing your own mock.
2. **Testing code that *calls* an HTTP API.** Examples: an `ApiClient` wrapper, a login helper, a service that depends on a payment provider. Here you **mock the outgoing HTTP call** so the test checks *your code's reaction* to whatever the server says.

Everything in this lesson is about situation 2.

### 4. The `responses` Library

`responses` intercepts calls made with the `requests` library, so the request never leaves your machine. Install it:

```bash
pip install responses
pip freeze > requirements.txt
```

#### 4.1 A first mock

Imagine the function under test lives in `user_client.py`:

```python
# user_client.py
import requests

BASE_URL = "https://api.example.com"


def get_username(user_id):
    r = requests.get(f"{BASE_URL}/users/{user_id}", timeout=5)
    r.raise_for_status()
    return r.json()["name"]
```

And the test:

```python
# test_user_client.py
import responses
import user_client


@responses.activate
def test_get_username_returns_name():
    # Arrange: register a stub response
    responses.add(
        responses.GET,
        "https://api.example.com/users/1",
        json={"id": 1, "name": "Ana"},
        status=200,
    )

    # Act: this call never touches the network
    name = user_client.get_username(1)

    # Assert
    assert name == "Ana"
```

Line by line:

- `import responses`: the library. It exposes HTTP method constants (`responses.GET`, `responses.POST`, ...).
- `@responses.activate`: a decorator that switches interception **on** while the test function runs, and **off** again afterwards. Without it, the stub is never installed and the real `requests` runs.
- `responses.add(responses.GET, url, json=..., status=200)`: registers a stub. When any `requests` call uses `GET` on exactly that URL, it receives a response with status 200 and the given JSON. `json=` also sets `Content-Type: application/json` for you.
- `user_client.get_username(1)`: your real code runs unchanged, including the real `requests` machinery (URL building, `raise_for_status`, `.json()`).
- The domain `api.example.com` does not exist. The test still passes with Wi-Fi off, which proves the network is not used.

An important safety feature: when `@responses.activate` is on and your code calls a URL you have **not** registered, `responses` raises `requests.exceptions.ConnectionError` with a message beginning "Connection refused by Responses". That is helpful, not annoying: it guarantees your test cannot accidentally reach the real internet.

#### 4.2 Simulating 4xx and 5xx responses

Your code should react correctly to bad news. Test each case separately:

```python
import pytest
import requests
import responses
import user_client


@responses.activate
def test_missing_user_raises_http_error():
    responses.add(
        responses.GET,
        "https://api.example.com/users/999",
        json={"error": "not found"},
        status=404,
    )

    with pytest.raises(requests.exceptions.HTTPError):
        user_client.get_username(999)


@responses.activate
def test_server_error_raises_http_error():
    responses.add(
        responses.GET,
        "https://api.example.com/users/1",
        json={"error": "boom"},
        status=500,
    )

    with pytest.raises(requests.exceptions.HTTPError):
        user_client.get_username(1)
```

Explanation: `status=404` and `status=500` make the stub answer with those codes. `raise_for_status()` inside `get_username` turns a `4xx`/`5xx` into an `HTTPError`, and `pytest.raises` asserts it happened. Without mocking you would need a real server that produces a `500` on demand.

Other useful failure shapes:

```python
# Unauthorised, with a header the real server would send
responses.add(responses.GET, "https://api.example.com/private",
              status=401, headers={"WWW-Authenticate": 'Bearer realm="api"'})

# Rate limited: tells the client to wait 30 seconds
responses.add(responses.GET, "https://api.example.com/search",
              status=429, headers={"Retry-After": "30"})

# A gateway returns HTML instead of JSON (a classic real-world surprise)
responses.add(responses.GET, "https://api.example.com/users/1",
              body="<html>Bad Gateway</html>", status=502,
              content_type="text/html")

# A non-JSON success body, e.g. a CSV export
responses.add(responses.GET, "https://api.example.com/report",
              body="id,name\n1,Ana\n", status=200, content_type="text/csv")
```

Use `json=` for JSON and `body=` for any other text. The HTML example lets you check that your code does not crash on `.json()` when a proxy returns a web page (recall the `safe_json` idea from earlier in the week).

#### 4.3 Simulating timeouts and ConnectionError

If you pass an **exception instance** as `body`, `responses` raises it instead of returning a response:

```python
import pytest
import requests
import responses
import user_client


@responses.activate
def test_timeout_propagates():
    responses.add(
        responses.GET,
        "https://api.example.com/users/1",
        body=requests.exceptions.ConnectTimeout("simulated timeout"),
    )

    with pytest.raises(requests.exceptions.ConnectTimeout):
        user_client.get_username(1)


@responses.activate
def test_connection_error_propagates():
    responses.add(
        responses.GET,
        "https://api.example.com/users/1",
        body=requests.exceptions.ConnectionError("network down"),
    )

    with pytest.raises(requests.exceptions.ConnectionError):
        user_client.get_username(1)
```

Line by line: `body=` receives an *instance* (note the parentheses and the message). When `requests.get` runs, `responses` raises that exception at exactly the place a real network failure would. The test finishes instantly; a real timeout test would wait for the full timeout period. Timeouts and dropped connections are nearly impossible to trigger on demand against a real server, which makes this one of the strongest reasons to mock.

#### 4.4 Several responses in sequence (retry logic)

Register the **same URL more than once** and `responses` hands the replies out in order. When only one remains, it keeps being returned for any further calls.

First, the code under test:

```python
# retry_client.py
import time
import requests


def get_with_retry(url, attempts=3, delay=0.0):
    last = None
    for _ in range(attempts):
        last = requests.get(url, timeout=5)
        if last.status_code < 500:
            return last
        time.sleep(delay)
    return last
```

Now the test:

```python
import responses
from retry_client import get_with_retry


@responses.activate
def test_retry_succeeds_on_third_attempt():
    url = "https://api.example.com/flaky"
    responses.add(responses.GET, url, status=503)
    responses.add(responses.GET, url, status=503)
    responses.add(responses.GET, url, json={"ok": True}, status=200)

    result = get_with_retry(url, attempts=3)

    assert result.status_code == 200
    assert len(responses.calls) == 3
```

Explanation: the first call gets `503`, the second gets `503`, the third gets `200`. `len(responses.calls) == 3` proves the helper really tried three times. Note the `delay=0.0` default: tests should not sleep. If your helper sleeps, make the delay a parameter so tests can pass `0`.

#### 4.5 Matching requests precisely

By default a stub matches on method and URL. That tells you the call *happened*, but not that your code sent the *right* data. Matchers tighten the stub. If a request does not satisfy the matcher, `responses` treats the stub as non-matching and raises `ConnectionError` listing what was tried.

```python
from responses import matchers
```

**Query parameters:**

```python
responses.add(
    responses.GET,
    "https://api.example.com/users",
    match=[matchers.query_param_matcher({"role": "admin", "page": "2"})],
    json=[{"id": 7}],
)
```

The stub answers only when the query string is exactly `?role=admin&page=2` (order does not matter). Values are strings. By default the match is strict: an extra, unexpected parameter makes it fail. Pass `strict_match=False` to allow extras.

**JSON body:**

```python
responses.add(
    responses.POST,
    "https://api.example.com/users",
    match=[matchers.json_params_matcher({"name": "Ana", "email": "ana@example.com"})],
    json={"id": 101},
    status=201,
)
```

If your code sends a different body (a typo in a field name, a missing field), the stub does not match and the test fails. This is exactly what you want when the purpose is to validate the request your code builds.

**Headers:**

```python
responses.add(
    responses.GET,
    "https://api.example.com/profile",
    match=[matchers.header_matcher({"Authorization": "Bearer abc123"})],
    json={"id": 1},
)
```

If the header is missing or different, the mock refuses the call, simulating an authenticated endpoint. Other helpers include `urlencoded_params_matcher` (form bodies) and `query_string_matcher`. You can combine several matchers in the `match=[...]` list; all must pass.

#### 4.6 Dynamic replies with `add_callback`

Sometimes the reply depends on the request. A **callback** receives the request and returns a tuple `(status, headers, body_string)`:

```python
import json
import requests
import responses


def create_user_callback(request):
    payload = json.loads(request.body)
    if "email" not in payload:
        return (400, {}, json.dumps({"error": "email required"}))
    return (201, {}, json.dumps({"id": 55, **payload}))


@responses.activate
def test_callback_behaves_like_a_tiny_server():
    responses.add_callback(
        responses.POST,
        "https://api.example.com/users",
        callback=create_user_callback,
        content_type="application/json",
    )

    bad = requests.post("https://api.example.com/users", json={"name": "Ana"}, timeout=5)
    good = requests.post("https://api.example.com/users",
                         json={"name": "Ana", "email": "a@x.com"}, timeout=5)

    assert bad.status_code == 400
    assert good.status_code == 201
    assert good.json()["id"] == 55
```

Line by line: `request.body` holds the bytes your code sent; `json.loads` turns it into a dict. The callback returns a status, a headers dict, and a **string** body (so we `json.dumps`). `content_type` tells `requests` how to read it. The callback has turned the mock into a small **fake** of the real endpoint. Keep callbacks tiny: a mock that copies all the server's logic becomes a second system you must maintain.

#### 4.7 Verifying calls: `calls`, `assert_call_count`

A mock that answers is half the story; you often need to check what your code *sent*. Every intercepted request is recorded in `responses.calls`.

```python
import requests
import responses


@responses.activate
def test_client_sends_auth_header():
    responses.add(responses.GET, "https://api.example.com/profile", json={"id": 1})

    session = requests.Session()
    session.headers["Authorization"] = "Bearer abc"
    session.get("https://api.example.com/profile", timeout=5)

    assert len(responses.calls) == 1
    sent = responses.calls[0].request
    assert sent.headers["Authorization"] == "Bearer abc"
    assert sent.url == "https://api.example.com/profile"
    assert sent.method == "GET"
    assert responses.calls[0].response.status_code == 200
```

Each entry in `responses.calls` has `.request` (what your code sent: `url`, `method`, `headers`, `body`) and `.response` (what the mock returned). Use `calls[0]`, `calls[1]` to inspect calls in order.

To count calls to one specific URL, use `assert_call_count`:

```python
@responses.activate
def test_cache_avoids_second_request():
    url = "https://api.example.com/config"
    responses.add(responses.GET, url, json={"mode": "fast"})

    requests.get(url, timeout=5)
    requests.get(url, timeout=5)

    responses.assert_call_count(url, 2)   # raises AssertionError if the count differs
```

`assert_call_count(url, count)` is more readable than counting list entries, and its failure message states the expected and actual numbers.

#### 4.8 Registries: how `responses` picks a stub

When several stubs could match a call, a **registry** decides which one is used. The default (`FirstMatchRegistry`) behaves as in 4.4: the first match is used, and it is removed if another match remains, so repeated registrations form a sequence.

If you want to require a strict **order across different URLs** (for example "login, then fetch profile, then logout"), use the `OrderedRegistry`:

```python
import requests
import responses
from responses.registries import OrderedRegistry


@responses.activate(registry=OrderedRegistry)
def test_calls_must_happen_in_order():
    responses.add(responses.POST, "https://api.example.com/login", json={"token": "t"})
    responses.add(responses.GET, "https://api.example.com/profile", json={"id": 1})

    requests.post("https://api.example.com/login", timeout=5)
    requests.get("https://api.example.com/profile", timeout=5)
```

With `OrderedRegistry`, calling `/profile` *first* raises an error, because the next expected request is the login. Most tests do not need this; reach for it when the *sequence* is the thing you are verifying.

#### 4.9 Context-manager form and strictness

The decorator is convenient, but `RequestsMock` is more explicit and is the basis for a fixture:

```python
import requests
import responses


def test_with_context_manager():
    with responses.RequestsMock() as rsps:
        rsps.add(responses.GET, "https://api.example.com/health", json={"status": "ok"})
        assert requests.get("https://api.example.com/health", timeout=5).json()["status"] == "ok"
```

`RequestsMock()` is **strict by default** (`assert_all_requests_are_fired=True`): when the `with` block ends, the test fails if a registered stub was never called. That catches tests where you set up a mock but your code took a different path. (The plain `@responses.activate` decorator is lenient and does not complain about unused stubs.)

### 5. `unittest.mock`: Replacing Python Objects

`responses` works at the **HTTP level**. Python's built-in `unittest.mock` works at the **object level**: it swaps a function or object inside your code for a fake one. It is useful when HTTP is hidden behind your own functions, or when the dependency is not HTTP at all (a clock, a file, a database).

#### 5.1 The building blocks

- `Mock()`: an object that accepts any attribute access and any call, and records them.
- `MagicMock()`: a `Mock` that also supports Python's "magic" methods (`len()`, `with`, indexing, iteration). Use it when your code treats the object like a container or context manager. For simple "response" objects, plain `Mock` is fine.
- `return_value`: what a mock returns when called.
- `side_effect`: more flexible than `return_value`. Give it an **exception** (it is raised), a **list** (each call returns the next item, and exceptions in the list are raised), or a **function** (it computes the result).
- `patch("target")`: temporarily replaces the object at the dotted path `target`, and restores it afterwards. It creates a `MagicMock` unless you supply your own.
- Assertions: `assert_called_once()`, `assert_called_with(...)` (checks the **last** call), `assert_called_once_with(...)`, `assert_not_called()`, and `call_count`.

#### 5.2 Patching `requests.get`

```python
from unittest.mock import Mock, patch
import user_client


def test_get_username_with_patch():
    fake_response = Mock()
    fake_response.json.return_value = {"name": "Ana"}

    with patch("user_client.requests.get", return_value=fake_response) as fake_get:
        assert user_client.get_username(1) == "Ana"

    fake_get.assert_called_once_with("https://api.example.com/users/1", timeout=5)
```

Line by line:

- `fake_response = Mock()` creates the stand-in for the `Response` object.
- `fake_response.json.return_value = {...}` says "when `.json()` is called, return this dict". Because `Mock` accepts any call, `raise_for_status()` also works and does nothing (it returns another `Mock`).
- `patch("user_client.requests.get", return_value=fake_response)` replaces `get` for the length of the `with` block. Every call to it returns `fake_response`. `as fake_get` gives you the replacement so you can inspect it.
- `fake_get.assert_called_once_with(url, timeout=5)` verifies *how* your code called `requests.get`: this is the **mock** behaviour (recording interaction). It must match arguments exactly, including keyword arguments.

Trade-off: `raise_for_status` "works" only because `Mock` swallows it, so this test would **not** catch a `404`. `responses` is usually better for HTTP because it runs the real `requests` code path.

#### 5.3 `side_effect` for failures and sequences

```python
import pytest
import requests
from unittest.mock import patch
import user_client


def test_timeout_with_side_effect():
    with patch("user_client.requests.get", side_effect=requests.exceptions.Timeout("slow")):
        with pytest.raises(requests.exceptions.Timeout):
            user_client.get_username(1)

```

A list works too, as a sequence of outcomes:


```python
from unittest.mock import Mock

service = Mock()
service.fetch.side_effect = [ConnectionError("down"), {"ok": True}]

try:
    service.fetch()
except ConnectionError:
    pass
assert service.fetch() == {"ok": True}
assert service.fetch.call_count == 2
```

Each call to `service.fetch()` consumes the next item of the list: the first raises, the second returns the dict. This mirrors the `responses` sequence from 4.4 but at the Python object level.

#### 5.4 Where to patch: patch where it is used

This is the most common `unittest.mock` stumble. The rule: **patch the name in the namespace where the code under test looks it up**, not where the object was originally defined.

Compare two ways your code can import `get`:

```python
# client_a.py
import requests

def fetch(url):
    return requests.get(url, timeout=5).status_code
```

```python
# client_b.py
from requests import get

def fetch(url):
    return get(url, timeout=5).status_code
```

In `client_a`, the lookup happens at call time through the `requests` module, so `patch("requests.get")` (or `patch("client_a.requests.get")`) works. In `client_b`, `from requests import get` copied the reference into `client_b`'s own namespace at import time. Patching `requests.get` changes the original, but `client_b.get` still points to the old real function. You must patch `"client_b.get"`:

```python
from unittest.mock import Mock, patch
import client_b

def test_patch_where_used():
    with patch("client_b.get", return_value=Mock(status_code=200)):
        assert client_b.fetch("https://api.example.com/x") == 200
```

Rule of thumb: look at the `import` line in the file under test and patch `"<that module>.<name as written there>"`. If you patch the wrong place, the symptom is a real network call (or a `ConnectionError` if you are also using `responses`) and an assertion on the mock that says "not called".

#### 5.5 The `@patch` decorator and pytest's `monkeypatch`

`patch` can also be a decorator. The mock is passed as an extra argument:

```python
from unittest.mock import patch, Mock
import user_client

@patch("user_client.requests.get")
def test_with_decorator(fake_get):
    fake_get.return_value = Mock(json=Mock(return_value={"name": "Ana"}))
    assert user_client.get_username(1) == "Ana"
```

pytest's built-in `monkeypatch` fixture does a similar job and undoes itself automatically:

```python
def test_with_monkeypatch(monkeypatch):
    fake = Mock(json=Mock(return_value={"name": "Ana"}))
    monkeypatch.setattr("user_client.requests.get", lambda *a, **k: fake)
    assert user_client.get_username(1) == "Ana"
```

`monkeypatch` has no built-in call recording; use `Mock` as the replacement if you need to assert on calls.

#### 5.6 Spy: wrap the real thing

```python
from unittest.mock import patch
import user_client

def test_spy_records_but_runs_real_code():
    with patch("user_client.requests.get", wraps=requests.get) as spy:
        ...  # real code still runs, so stub the HTTP with responses too
```

`wraps=` forwards calls to the real object while recording them: a **spy**. Use it sparingly, and combine it with `responses` so the HTTP is still stubbed.

#### 5.7 Choosing between `responses` and `unittest.mock`

| Situation | Better tool |
|-----------|-------------|
| Code uses `requests`, and you care about status codes, headers, JSON, retries | `responses` |
| You need to match the exact request (query, body, headers) | `responses` |
| Dependency is not HTTP (time, files, database, a Python SDK) | `unittest.mock` |
| You want to assert on how an internal function was called | `unittest.mock` |
| Code uses `httpx` or `aiohttp` | A library for that client (for example `respx` for `httpx`) or `unittest.mock` |

### 6. Pytest Fixtures Wrapping Mocks

Repeating the same `responses.add` in twenty tests is noise. A fixture centralises the setup and cleanup:

```python
# conftest.py
import pytest
import responses as responses_lib


@pytest.fixture
def mocked_api():
    with responses_lib.RequestsMock() as rsps:
        yield rsps


@pytest.fixture
def user_endpoint(mocked_api):
    mocked_api.add(
        responses_lib.GET,
        "https://api.example.com/users/1",
        json={"id": 1, "name": "Ana"},
    )
    return mocked_api
```

```python
# test_with_fixtures.py
import user_client


def test_get_username_uses_fixture(user_endpoint):
    assert user_client.get_username(1) == "Ana"
    assert len(user_endpoint.calls) == 1
```

Line by line:

- `with RequestsMock() as rsps: yield rsps`: the mock activates when the test starts and is cleaned up (and verified) when it ends, even if the test fails. Everything before `yield` is setup, everything after is teardown.
- `user_endpoint` depends on `mocked_api` (fixtures can request other fixtures) and registers the common stub.
- The test just names the fixture. The shared setup is in one place, and the test body reads like a story.
- Because the strict `RequestsMock` fails if a stub is unused, requesting `user_endpoint` but never calling it makes the test fail. That is a feature; it keeps your fixtures honest.

A fixture that wraps `unittest.mock.patch` looks similar:

```python
@pytest.fixture
def fake_get():
    with patch("user_client.requests.get") as m:
        yield m
```

### 7. The Contract Drift Risk

A mock is a **claim about the real API**: "the server returns this JSON with this status." Nothing verifies that claim. If the real API renames `name` to `full_name`, your mocked tests keep passing while production breaks. This is **contract drift**, and it is the main danger of mocking.

Ways to reduce it:

- **Build mocks from the real contract**: an OpenAPI spec, or responses captured from the real service (save a real response to a JSON file and load it in your mock).
- **Keep a small set of real-API tests** (smoke or contract tests) that run on a schedule or before release, to confirm the real shape still matches.
- **Keep mocks minimal**: mock only the fields your code uses, but make them realistic (types, nesting, status codes).
- **Review mocks when the API changes**: treat mock data as test code that needs maintenance.

A balanced strategy follows the test pyramid idea: many fast mocked tests for logic and error handling, plus a smaller number of real-service tests for true end-to-end confidence. (Later Wednesday lessons on validation return to checking real responses against a schema.)

### 8. When NOT to Mock

Mocking is a tool, not a religion. Avoid it when:

| Situation | Why a mock is the wrong choice |
|-----------|--------------------------------|
| You are **testing the real API itself** | A mocked API test proves nothing about the service |
| You want to verify the real **contract** (schemas, status codes, headers) | Only the real server can tell you |
| You are doing **smoke tests** after a deploy | The point is checking real systems are alive |
| You would have to mock **everything** | The test becomes a rehearsal of your own assumptions |
| The mock replicates **complex server logic** | You now maintain a second, unreliable server; use a real test instance or a contract test |
| The dependency is **cheap, fast, and safe** (for example a local in-memory database) | Using the real thing is simpler and more faithful |

### 9. Common Mistakes

1. **Forgetting `@responses.activate`.** The stub is never installed, so the real request goes out. Symptom: a real network call (or a DNS error) in a "mocked" test.
2. **Mocking the wrong URL.** A trailing slash, a different host, or `http` versus `https` means no stub matches, and you get `ConnectionError: Connection refused by Responses`. Read the error: it lists the registered URLs.
3. **Query strings inside the URL.** Write the query with `matchers.query_param_matcher` instead of embedding `?a=1` in the registered URL.
4. **Passing the exception class, not an instance, as `body`.** Use `ConnectTimeout("msg")`, not `ConnectTimeout`.
5. **Patching where the object is defined, not where it is used** (section 5.4).
6. **`assert_called_with` checks only the last call.** Use `call_count` or `assert_called_once_with` when the number of calls matters.
7. **A typo on a `Mock` attribute silently passes.** `mock.assert_called_onec()` on a plain `Mock` may just create another mock and assert nothing. Newer Python versions guard against common typos, but use `Mock(spec=...)` or `create_autospec` for stricter mocks.
8. **Using `time.sleep` in code under test.** Tests become slow. Make delays configurable and pass `0` in tests.
9. **Asserting nothing.** A test that sets up a mock and never asserts on the result or the calls only proves the code does not crash.
10. **Mocking so much that the test verifies the mock.** If the test passes no matter what the code does, it is not testing anything.

### 10. Glossary

### Test double
Any object that stands in for a real dependency during a test.

### Stub
A double that returns canned data and has no checking logic.

### Mock
A double that records how it was called so a test can verify interactions. Also used loosely for all doubles.

### Fake
A simplified but working implementation of a dependency (for example an in-memory database or a callback-driven endpoint).

### Spy
A wrapper around the real object that records calls while still delegating to the real behaviour.

### Interception
Replacing the real network call with a stand-in at the moment the request is made. `responses` intercepts at the `requests` adapter level.

### Determinism
The property that a test gives the same result on every run for the same code.

### Patch target
The dotted path (`module.name`) that `unittest.mock.patch` replaces. It must be the place where the code under test *looks the name up*.

### Contract drift
The mock's idea of the API diverging from what the real API now does.

### Registry
In `responses`, the strategy that decides which registered stub answers a request (`FirstMatchRegistry` by default, `OrderedRegistry` for strict order).

### 11. Practice Exercises

**Exercise 1.** Write `get_user_email(user_id)` that calls `GET https://api.example.com/users/{id}` and returns the `"email"` field, raising on `4xx`/`5xx`. Write three `responses` tests: a success with your own JSON, a `404`, and a `500`. Turn Wi-Fi off and confirm they pass.

**Exercise 2.** Write a `create_user(name, email)` function that sends `POST /users` with a JSON body and returns the new id. Write a test where `json_params_matcher` requires the exact body, and check with `responses.calls[0].request.body` what was sent. Then change `"email"` to `"mail"` in your function and observe the failure.

**Exercise 3.** Using the `get_with_retry` helper from 4.4, write a test where the server returns `503`, `503`, then `200`, and assert three calls with `assert_call_count`. Add a second test where every response is `503` and assert that the helper gives up after `attempts` tries and returns the final `503`.

**Exercise 4.** Re-do the timeout test from 4.3 using `unittest.mock.patch` with `side_effect`. Then write `client_c.py` using `from requests import get`, and show (a) a test patching `requests.get` that fails to intercept, and (b) the corrected test patching `client_c.get`. Explain in a comment why.

#### Solutions

**Solution 1.**

```python
# user_email.py
import requests


def get_user_email(user_id):
    r = requests.get(f"https://api.example.com/users/{user_id}", timeout=5)
    r.raise_for_status()
    return r.json()["email"]
```

```python
# test_user_email.py
import pytest
import requests
import responses
from user_email import get_user_email

URL = "https://api.example.com/users/1"


@responses.activate
def test_success():
    responses.add(responses.GET, URL, json={"id": 1, "email": "ana@example.com"})
    assert get_user_email(1) == "ana@example.com"


@responses.activate
def test_not_found():
    responses.add(responses.GET, URL, json={"error": "nope"}, status=404)
    with pytest.raises(requests.exceptions.HTTPError):
        get_user_email(1)


@responses.activate
def test_server_error():
    responses.add(responses.GET, URL, status=500)
    with pytest.raises(requests.exceptions.HTTPError):
        get_user_email(1)
```

Each test registers exactly one stub and checks one behaviour. `status=500` with no body is fine: `raise_for_status` only needs the status.

**Solution 2.**

```python
# user_create.py
import requests


def create_user(name, email):
    r = requests.post("https://api.example.com/users",
                      json={"name": name, "email": email}, timeout=5)
    r.raise_for_status()
    return r.json()["id"]
```

```python
# test_user_create.py
import json
import responses
from responses import matchers
from user_create import create_user


@responses.activate
def test_create_user_sends_expected_body():
    responses.add(
        responses.POST,
        "https://api.example.com/users",
        match=[matchers.json_params_matcher({"name": "Ana", "email": "ana@example.com"})],
        json={"id": 101},
        status=201,
    )

    assert create_user("Ana", "ana@example.com") == 101
    sent = json.loads(responses.calls[0].request.body)
    assert sent == {"name": "Ana", "email": "ana@example.com"}
```

If you rename the key to `"mail"`, the matcher no longer matches, so `responses` raises `ConnectionError` and the test fails. That failure is the proof the matcher is protecting you.

**Solution 3.**

```python
import responses
from retry_client import get_with_retry

URL = "https://api.example.com/flaky"


@responses.activate
def test_succeeds_on_third_try():
    responses.add(responses.GET, URL, status=503)
    responses.add(responses.GET, URL, status=503)
    responses.add(responses.GET, URL, json={"ok": True})

    result = get_with_retry(URL, attempts=3)

    assert result.status_code == 200
    responses.assert_call_count(URL, 3)


@responses.activate
def test_gives_up_after_all_attempts():
    responses.add(responses.GET, URL, status=503)   # last stub repeats forever

    result = get_with_retry(URL, attempts=3)

    assert result.status_code == 503
    responses.assert_call_count(URL, 3)
```

In the second test one stub is enough: when only one match remains, `responses` keeps returning it, so all three attempts see `503`.

**Solution 4.**

```python
# test_timeout_patch.py
import pytest
import requests
from unittest.mock import patch
import user_client


def test_timeout_with_patch():
    with patch("user_client.requests.get",
               side_effect=requests.exceptions.Timeout("slow")):
        with pytest.raises(requests.exceptions.Timeout):
            user_client.get_username(1)
```

```python
# client_c.py
from requests import get


def fetch(url):
    return get(url, timeout=5).status_code
```

```python
# test_client_c.py
import requests
from unittest.mock import Mock, patch
import client_c


def test_wrong_target_does_not_change_client_c():
    # client_c.get was bound at import time, so patching requests.get leaves it alone
    with patch("requests.get", return_value=Mock(status_code=200)):
        assert client_c.get is not requests.get


def test_patch_where_it_is_used():
    with patch("client_c.get", return_value=Mock(status_code=200)) as fake:
        assert client_c.fetch("https://api.example.com/x") == 200
    fake.assert_called_once_with("https://api.example.com/x", timeout=5)
```

The comment to write: `from requests import get` binds the name `get` inside `client_c` at import time, so patching `requests.get` later does not change `client_c.get`. Patch the name where it is used.

### 12. Knowledge Check (5 questions)

**Q1.** Which test double records how it was called so the test can verify the interaction?
a) Stub  b) Mock  c) Fake  d) Dummy

**Q2.** What happens when `@responses.activate` is on and your code calls a URL that you did not register?
a) The real request goes through  b) It returns `None`  c) `ConnectionError` is raised  d) The test is skipped

**Q3.** How do you make `responses` simulate a timeout?
a) `status=408`  b) `body=requests.exceptions.ConnectTimeout("msg")`  c) `timeout=0`  d) `responses.sleep(30)`

**Q4.** Your module does `from requests import get`. What should you patch?
a) `requests.get`  b) `requests.api.get`  c) `your_module.get`  d) `builtins.get`

**Q5.** Which is the main risk of relying only on mocked tests?
a) They run too fast  b) Contract drift: the real API changes but the mocks still pass  c) They need a network  d) They cannot check headers

#### Answers

1. **b) Mock.** A stub only answers; a mock also records calls for verification.
2. **c) `ConnectionError`.** `responses` blocks unregistered requests, which stops accidental real traffic.
3. **b).** An exception instance passed as `body` is raised instead of returning a response.
4. **c) `your_module.get`.** The name was copied into your module at import; patch it where it is used.
5. **b) Contract drift.** Mocks assert what you *believe* the API does; only real-service tests confirm it.

---

## Summary

- Mock external HTTP to make tests fast, deterministic, free of side effects, and able to simulate failures and rate limits.
- Test doubles: a **stub** answers, a **mock** answers and records, a **fake** is a simplified working version, a **spy** wraps the real thing.
- Do not mock the API you are testing; mock the outgoing calls **made by** the code you are testing.
- `responses` (`@responses.activate`, `responses.add`, `add_callback`) intercepts `requests`. Match on URL, query, JSON body, and headers; register several replies for a sequence; inspect `responses.calls` and use `assert_call_count`; use `OrderedRegistry` when order across URLs matters.
- Pass an exception instance as `body` to simulate timeouts and `ConnectionError`; use `status=` for `4xx`/`5xx`.
- `unittest.mock` (`Mock`, `MagicMock`, `patch`, `return_value`, `side_effect`, `assert_called_with`) replaces Python objects. **Patch where the name is used**, not where it is defined.
- Wrap mocks in pytest fixtures for reuse and automatic cleanup.
- Mocks can drift from the real contract; keep a few real-API tests and know when not to mock.

## Additional Resources

- `responses` documentation and source (Sentry): https://github.com/getsentry/responses
- Python docs, *unittest.mock: mock object library*: https://docs.python.org/3/library/unittest.mock.html
- Python docs, *unittest.mock - getting started* (includes "where to patch"): https://docs.python.org/3/library/unittest.mock-examples.html
- pytest documentation, *How to monkeypatch/mock modules and environments*: https://docs.pytest.org/en/stable/how-to/monkeypatch.html
- Martin Fowler, *Mocks Aren't Stubs*: https://martinfowler.com/articles/mocksArentStubs.html
