# Mocking External APIs

## Learning Objectives

By the end of this lesson you will be able to:

- Decide which external (third-party) services to mock and which to keep real.
- Write a small **client wrapper class** that accepts `base_url` and a `requests.Session` through dependency injection, so it is easy to test.
- Build realistic mock payloads from **recorded real responses** stored as JSON fixtures.
- Create a reusable **mock-server fixture** in `conftest.py` with the `responses` library.
- Test error handling, **retries with backoff**, timeouts, **pagination**, **429 rate limits with `Retry-After`**, and **auth-token expiry** without touching the network.
- Assert that your code sends the **correct outbound request** (headers and body), not just that it handles the reply.
- Keep mocks in sync with the real API (contract tests, recording tools) and avoid over-mocking.

---

## Why This Matters

This is Week 7, where your suite stops being "a set of scripts" and becomes a framework that has to run unattended in a pipeline. Pipelines have no patience for flaky tests, and the biggest source of flakiness is **other people's servers**.

Picture the real situations you will meet on a QEA team:

- Your app creates GitHub issues, charges cards through a payment provider, or checks the weather before quoting a delivery price. The provider's sandbox goes down at 2 a.m. and your build turns red although *your* code is fine.
- You need to know what your app does when the provider answers `429 Too Many Requests`, or when the login token expires halfway through a job. You cannot make a real provider do that on demand.
- Real calls are slow, may cost money, and may send real emails or create real data.

On Monday and Tuesday you learned to send requests and validate responses. Earlier today you learned basic HTTP mocking with `responses` and data-driven tests. This lesson is the **applied** step: a realistic client, realistic payloads, and the hard scenarios (retries, 429, expiry) that mocks make easy. Test isolation, validation helpers, and framework structure come in the next lessons today; on Friday you will run all of this in CI, which is exactly why deterministic tests matter.

---

## The Concept

### 1. What, Why, When: Mocking at the Boundary

A **mock** (more precisely a *test double*) replaces a real dependency with something you control. For HTTP, the best place to do it is the **network boundary**: your real code runs, builds a real request, and the mock answers instead of the internet.

Ask of every arrow in your system: *do we own and control this?*

| Dependency | Mock it? | Why |
|-----------|----------|-----|
| Third-party SaaS (payments, email, maps, GitHub) | Yes | Cost, side effects, no control over its behaviour |
| Another team's service | Often | Availability and speed; or use a shared test environment |
| Your own database | Usually no | You own it; use a test database for real behaviour |
| The system under test | Never | That is what you are testing |

**When mocking is the right tool:** you must simulate failures, the provider is slow/costly/unavailable, or you need identical results on every run.
**When it is not enough:** you need to know the real provider still behaves as you assume. That job belongs to contract tests (section 11).

### 2. The Scenario: A GitHub-Style Issue Tool

We will test a small tool that talks to a GitHub-style REST API: fetch a repository, list its issues (paginated), and create an issue. The same ideas apply to a payment API (`POST /charges`) or a weather API (`GET /current`); only the paths change.

Project layout used in this lesson:

```
clients/api_client.py
clients/triage.py
tests/conftest.py
tests/fixtures/repo_200.json
tests/test_client.py
```

### 3. The Client Wrapper With Dependency Injection

Calling `requests.get("https://api...")` scattered across your code makes testing painful. Instead, put all HTTP in one **client class** and *inject* the things that vary: the base URL, the session, the token, and even the `sleep` function.

```python
# clients/api_client.py
import time
import requests


class ApiError(Exception):
    def __init__(self, status, message=""):
        super().__init__(f"{status}: {message}")
        self.status = status


class RateLimited(ApiError):
    def __init__(self, retry_after):
        super().__init__(429, f"retry after {retry_after}s")
        self.retry_after = retry_after


class ApiClient:
    def __init__(self, base_url, session=None, token=None, refresh=None,
                 max_retries=3, backoff=0.5, timeout=5, sleep=time.sleep):
        self.base_url = base_url.rstrip("/")
        self.session = session or requests.Session()
        self.token = token
        self.refresh = refresh          # callable returning a new token
        self.max_retries = max_retries
        self.backoff = backoff
        self.timeout = timeout
        self.sleep = sleep

    def _request(self, method, path, **kwargs):
        url = path if path.startswith("http") else self.base_url + path
        refreshed = False
        for attempt in range(self.max_retries + 1):
            last = attempt == self.max_retries
            delay = self.backoff * (2 ** attempt)
            headers = {"Authorization": f"Bearer {self.token}",
                       "Accept": "application/json"}
            try:
                r = self.session.request(method, url, headers=headers,
                                         timeout=self.timeout, **kwargs)
            except (requests.Timeout, requests.ConnectionError) as exc:
                if last:
                    raise ApiError(0, f"unreachable: {exc}") from exc
                self.sleep(delay)
                continue

            if r.status_code == 401 and self.refresh and not refreshed:
                self.token = self.refresh()
                refreshed = True
                continue
            if r.status_code == 429:
                wait = float(r.headers.get("Retry-After", delay))
                if last:
                    raise RateLimited(wait)
                self.sleep(wait)
                continue
            if r.status_code >= 500:
                if last:
                    raise ApiError(r.status_code, "server error")
                self.sleep(delay)
                continue
            if r.status_code >= 400:
                raise ApiError(r.status_code, r.text)
            return r

    def get_repo(self, repo):
        return self._request("GET", f"/repos/{repo}").json()

    def create_issue(self, repo, title, body):
        r = self._request("POST", f"/repos/{repo}/issues",
                          json={"title": title, "body": body})
        return r.json()

    def list_issues(self, repo, per_page=2):
        r = self._request("GET", f"/repos/{repo}/issues",
                          params={"per_page": per_page})
        while True:
            yield from r.json()
            nxt = r.links.get("next")
            if not nxt:
                break
            r = self._request("GET", nxt["url"])
```

**Line-by-line, the parts that matter:**

- `session=None ... or requests.Session()`: production code gets a default session; a test (or a future caller) can pass its own, for example one with extra headers. This is **dependency injection**: the class does not hard-wire its collaborators.
- `base_url`: the same class works against production, staging, or a mock URL. You never edit code to change environment.
- `sleep=time.sleep`: backoff means waiting. In tests we inject a fake `sleep` that records the delay instead of waiting, so a "retry three times with 30-second waits" test takes milliseconds.
- `delay = backoff * 2 ** attempt`: **exponential backoff** (0.5s, 1s, 2s, ...). Waiting longer each time avoids hammering a struggling server.
- The `try/except`: timeouts and connection failures are retried, and after the last attempt they become one clear `ApiError(0, ...)`.
- `401` with `refresh`: refresh the token **once**, then retry. The `refreshed` flag prevents an infinite loop if the new token is also rejected.
- `429`: obey the server's `Retry-After` header when present; otherwise fall back to backoff.
- `5xx` is retried (the server may recover); other `4xx` is **not** retried (your request is wrong, repeating it will not help).
- `r.links`: `requests` parses the `Link` header, which is how GitHub-style APIs announce the next page.

### 4. Realistic Payloads From Recorded Responses

Mocks invented from memory drift from reality. Instead, **record** a real response once (with Postman, `curl`, or a tiny script), strip secrets and personal data, and save it as a fixture.

```json
{
  "id": 1296269,
  "full_name": "acme/app",
  "private": false,
  "owner": {"login": "acme", "id": 583231},
  "default_branch": "main",
  "open_issues_count": 3,
  "created_at": "2024-02-11T09:30:00Z"
}
```

Save it as `tests/fixtures/repo_200.json`. Now your mock returns the same field names, types, and nesting the real API uses, including fields your code ignores today but may need tomorrow. Keep a short note in each fixture folder: where it was recorded, on what date, and from which endpoint.

### 5. A Reusable Mock-Server Fixture

Here is the shared plumbing. A small `FakeApi` helper wraps `responses` so every test reads clearly, and fixtures build a client wired for testing.

```python
# tests/conftest.py
import json
import pathlib
import pytest
import responses
from clients.api_client import ApiClient

BASE = "https://api.example-git.test"
FIXTURES = pathlib.Path(__file__).parent / "fixtures"


def load_fixture(name):
    return json.loads((FIXTURES / name).read_text())


class FakeApi:
    """Thin wrapper: registers canned responses for the fake provider."""

    def __init__(self, rsps):
        self.rsps = rsps

    def add(self, method, path, fixture=None, **kwargs):
        if fixture:
            kwargs["json"] = load_fixture(fixture)
        url = path if path.startswith("http") else BASE + path
        self.rsps.add(method, url, **kwargs)

    @property
    def calls(self):
        return self.rsps.calls


@pytest.fixture
def fake_api():
    with responses.RequestsMock() as rsps:     # fresh mock per test
        yield FakeApi(rsps)


@pytest.fixture
def sleeps():
    return []                                   # records requested waits


@pytest.fixture
def client(fake_api, sleeps):
    return ApiClient(BASE, token="tok_old", refresh=lambda: "tok_new",
                     sleep=sleeps.append, backoff=0.5)
```

What each piece does:

- `responses.RequestsMock()` as a context manager intercepts every `requests` call made while the test runs, and **fails the test at the end** if you registered a response that was never used (`assert_all_requests_are_fired` defaults to `True`). That catches tests that silently stop exercising what you think they do.
- `yield` inside `with` means the mock is active during the test and cleaned up afterwards. Each test gets its own, so nothing leaks between tests (the later lesson on test isolation goes deeper).
- `sleeps` is a plain list. Passing `sleeps.append` as `sleep` means "when the client wants to wait N seconds, append N to this list". Tests then assert on the list.
- Any request that matches **no** registered response raises `requests.ConnectionError`. This is a feature: your suite can never accidentally reach the real internet.

### 6. Happy Path and Outbound Request Correctness

Most beginners only check what comes *back*. Check what goes *out* too: a wrong header or body is a real production bug that a mock will happily answer anyway.

```python
# tests/test_client.py
import json
import pytest
import responses
from clients.api_client import ApiError, RateLimited


def test_get_repo_parses_recorded_payload(client, fake_api):
    fake_api.add(responses.GET, "/repos/acme/app", fixture="repo_200.json")

    repo = client.get_repo("acme/app")

    assert repo["full_name"] == "acme/app"
    assert repo["owner"]["login"] == "acme"


def test_create_issue_sends_correct_headers_and_body(client, fake_api):
    fake_api.add(responses.POST, "/repos/acme/app/issues",
                 json={"number": 7}, status=201)

    result = client.create_issue("acme/app", "Crash on login", "Steps: ...")

    sent = fake_api.calls[0].request
    assert result["number"] == 7
    assert sent.headers["Authorization"] == "Bearer tok_old"
    assert sent.headers["Accept"] == "application/json"
    assert json.loads(sent.body) == {"title": "Crash on login", "body": "Steps: ..."}
```

Explanation: `fake_api.calls[0].request` is the exact request your code produced. `sent.body` is raw bytes/text, so we parse it with `json.loads` before comparing; that avoids fragile string comparison where key order or spacing differs. For a payment API this is where you would assert the amount in cents and an `Idempotency-Key` header (Monday's idempotency discussion).

### 7. Error Handling: Client Errors and Server Errors

```python
def test_404_raises_without_retrying(client, fake_api, sleeps):
    fake_api.add(responses.GET, "/repos/acme/missing",
                 json={"message": "Not Found"}, status=404)

    with pytest.raises(ApiError) as err:
        client.get_repo("acme/missing")

    assert err.value.status == 404
    assert len(fake_api.calls) == 1      # a 4xx is our mistake: do not retry
    assert sleeps == []                  # and never waited
```

The `sleeps` fixture is the list our fake `sleep` appends to, so an empty list proves the client never waited.

### 8. Retries and Backoff

```python
def test_retries_503_then_succeeds(client, fake_api, sleeps):
    fake_api.add(responses.GET, "/repos/acme/app", status=503)
    fake_api.add(responses.GET, "/repos/acme/app", status=503)
    fake_api.add(responses.GET, "/repos/acme/app", fixture="repo_200.json")

    repo = client.get_repo("acme/app")

    assert repo["full_name"] == "acme/app"
    assert len(fake_api.calls) == 3
    assert sleeps == [0.5, 1.0]          # exponential backoff


def test_gives_up_after_max_retries(client, fake_api):
    fake_api.add(responses.GET, "/repos/acme/app", status=500)

    with pytest.raises(ApiError) as err:
        client.get_repo("acme/app")

    assert err.value.status == 500
    assert len(fake_api.calls) == 4      # 1 try + 3 retries
```

How it works: when you register several responses for the same URL, `responses` serves them **in order**, and keeps repeating the last one. So three registrations mean "fail, fail, succeed", and a single `500` means "always fail". The assertion on `sleeps == [0.5, 1.0]` proves backoff doubles, without waiting for real.

### 9. Timeouts

You cannot make the real internet time out on demand, but a mock can raise the same exception `requests` would:

```python
import requests


def test_timeout_is_retried_then_reported(client, fake_api):
    fake_api.add(responses.GET, "/repos/acme/app",
                 body=requests.exceptions.ConnectTimeout("simulated"))

    with pytest.raises(ApiError) as err:
        client.get_repo("acme/app")

    assert err.value.status == 0         # our convention: 0 means "no response"
    assert len(fake_api.calls) == 4
```

Passing an **exception object** as `body` makes `responses` raise it. Also test that your code passes a `timeout=` at all: a missing timeout means a hung provider can hang your whole program. A quick assertion is `fake_api.calls[0].request.req_kwargs["timeout"] == 5`.

### 10. Rate Limits, Pagination, and Auth Expiry

**Rate limit (429 with `Retry-After`).** Providers tell you how long to wait. Your client must obey it, not guess.

```python
def test_429_waits_for_retry_after(client, fake_api, sleeps):
    fake_api.add(responses.GET, "/repos/acme/app",
                 status=429, headers={"Retry-After": "30"})
    fake_api.add(responses.GET, "/repos/acme/app", fixture="repo_200.json")

    client.get_repo("acme/app")

    assert sleeps == [30.0]              # waited exactly what the server asked


def test_429_every_time_raises_rate_limited(client, fake_api):
    fake_api.add(responses.GET, "/repos/acme/app",
                 status=429, headers={"Retry-After": "5"})

    with pytest.raises(RateLimited) as err:
        client.get_repo("acme/app")

    assert err.value.retry_after == 5.0
```

**Pagination.** A list endpoint returns one page plus a `Link: <...>; rel="next"` header. The bug you are hunting is "we only read page 1". Use a **query-parameter matcher** so each page registers separately:

```python
from responses import matchers


def test_list_issues_follows_next_links(client, fake_api):
    page2 = "https://api.example-git.test/repos/acme/app/issues?page=2&per_page=2"
    fake_api.add(responses.GET, "/repos/acme/app/issues",
                 json=[{"number": 1}, {"number": 2}],
                 headers={"Link": f'<{page2}>; rel="next"'},
                 match=[matchers.query_param_matcher({"per_page": "2"})])
    fake_api.add(responses.GET, page2,
                 json=[{"number": 3}],
                 match=[matchers.query_param_matcher({"page": "2", "per_page": "2"})])

    numbers = [i["number"] for i in client.list_issues("acme/app")]

    assert numbers == [1, 2, 3]
```

Explanation: the first page carries a `Link` header pointing at page 2; the client follows it until no `next` link remains. Also test the edge cases in your own time: an **empty** first page, and a **single** page with no `Link` header.

**Auth expiry.** Tokens expire mid-session. The provider answers `401`; the client should refresh once and retry.

```python
def test_expired_token_is_refreshed_once(client, fake_api):
    fake_api.add(responses.GET, "/repos/acme/app", status=401)
    fake_api.add(responses.GET, "/repos/acme/app", fixture="repo_200.json")

    client.get_repo("acme/app")

    first, second = (c.request for c in fake_api.calls)
    assert first.headers["Authorization"] == "Bearer tok_old"
    assert second.headers["Authorization"] == "Bearer tok_new"


def test_refresh_that_still_gets_401_gives_up(client, fake_api):
    fake_api.add(responses.GET, "/repos/acme/app", status=401)

    with pytest.raises(ApiError) as err:
        client.get_repo("acme/app")

    assert err.value.status == 401
    assert len(fake_api.calls) == 2      # original + one retry, no loop
```

The second test guards against the classic infinite-refresh bug.

### 11. Keeping Mocks in Sync With the Real API

A mock is a **claim** about the real service. If the provider renames `full_name` to `name`, your mock keeps passing while production breaks. Defences, from cheapest to heaviest:

1. **Record, do not invent** (section 4), and date your fixtures.
2. **Fixture contract check.** A tiny test that every recorded fixture still contains the fields your code relies on:

```python
REQUIRED = {"id", "full_name", "owner", "default_branch"}


def test_repo_fixture_has_required_fields():
    from tests.conftest import load_fixture
    assert REQUIRED <= set(load_fixture("repo_200.json"))
```

   For larger payloads, use a JSON Schema check, as in Tuesday's validation lesson.
3. **A scheduled live contract test.** One or two tests marked `@pytest.mark.live` call the real sandbox (nightly, not on every commit) and compare the real response with the same `REQUIRED` fields. If it fails, re-record the fixture and fix the code. Exclude it from the fast run with `pytest -m "not live"` and register the marker in `pytest.ini`.
4. **Recording tools.** Libraries such as `vcrpy` (or `pytest-recording`) record real HTTP exchanges into "cassette" files on the first run and replay them afterwards. They save typing but can hide stale data, so you still need item 3.
5. **OpenAPI examples.** If the provider publishes an OpenAPI spec, its `examples` are an official source of payloads and a basis for schema checks (pointer only; you will meet OpenAPI properly in later material).

### 12. Avoiding Over-Mocking

Mocks are powerful, so beginners overuse them. Warning signs and fixes:

- **Mocking your own code.** If you patch `client.get_repo` to test a function that calls it, you test nothing about the client. Mock the HTTP boundary and let your code run.
- **Mocks that contain logic.** A mock that computes prices or filters data duplicates the provider and can contain its own bugs. Return fixed canned data per scenario.
- **Asserting on internals.** "Was `_request` called twice?" breaks on every refactor. Assert on behaviour: results, raised errors, outbound requests.
- **Everything mocked, nothing real.** A suite that passes while the real integration is broken gives false confidence. Keep a few real, marked contract tests (section 11).
- **Mocking things you own.** Use a real test database or a locally running copy of your own API; mock only what you cannot control.

A good rule of thumb: *mock the far side of the network, run everything on the near side for real.*

### 13. Real-World Scenarios and Choosing a Mock Style

Three situations where this approach pays for itself:

- **Payment outage.** A card provider returns `503` for ten minutes during a sale. With mocks you can prove the checkout shows "try again later", does not create a second charge, and reuses the same `Idempotency-Key` on retry. You would never be allowed to provoke that against a live provider.
- **Weather or maps quota.** A free tier allows 60 calls per minute. A `429` test with `Retry-After` shows your batch job slows down instead of crashing or, worse, being banned.
- **Token expiry in a long job.** A nightly sync runs for an hour but tokens last 30 minutes. The auth-expiry test proves the job refreshes once and carries on, which you would otherwise discover at 3 a.m.

Choosing a mock style:

| Style | Use when | Example |
|-------|----------|---------|
| In-process (`responses`) | Your Python test calls Python code using `requests` | This lesson |
| Standalone mock server | Another process (browser, mobile app, other service) is the caller | Postman mock server, WireMock, a tiny Flask app |
| Recorded cassettes | You want fast replay of a long real conversation | `vcrpy` |

Start with in-process mocks; they are fastest and easiest to read. Only move to a standalone server when something outside Python needs to reach the fake.

### 14. Common Mistakes

| Mistake | What happens | Fix |
|--------|--------------|-----|
| Real `time.sleep` in retry code under test | A 3-retry test takes 7+ seconds | Inject `sleep` and record it |
| Forgetting the URL does not match (typo, trailing slash) | `ConnectionError`, which the client **retries**, so the failure looks like "unreachable" | Read the error text; check the URL registered |
| Registering a response that is never used | Test fails with "not all requests fired" | Good: remove it or fix the test |
| Only asserting the response | Wrong headers/bodies go unnoticed | Assert `calls[0].request` |
| Comparing `request.body` as a string | Fails on key order or spacing | `json.loads` first |
| Retrying every error | A 400 is retried 3 times and spams the provider | Retry only 5xx, 429, timeouts |
| Sharing one mock across tests | Order-dependent failures | Fixture per test |
| Mock uses a fixture nobody dated | Silent drift | Add a recorded-on note and a contract test |

### 15. A Small End-to-End Example

Combine everything: a function that reads all open issues (two pages, with a rate limit in the middle) and files a summary issue.

```python
# clients/triage.py
def triage(client, repo):
    titles = [i["title"] for i in client.list_issues(repo) if i["state"] == "open"]
    return client.create_issue(repo, "Triage report", "\n".join(titles))
```

```python
# tests/test_client.py
from clients.triage import triage


def test_triage_end_to_end(client, fake_api, sleeps):
    page2 = "https://api.example-git.test/repos/acme/app/issues?page=2&per_page=2"
    fake_api.add(responses.GET, "/repos/acme/app/issues",
                 json=[{"title": "A", "state": "open"}, {"title": "B", "state": "closed"}],
                 headers={"Link": f'<{page2}>; rel="next"'},
                 match=[matchers.query_param_matcher({"per_page": "2"})])
    m = [matchers.query_param_matcher({"page": "2", "per_page": "2"})]
    fake_api.add(responses.GET, page2, status=429, headers={"Retry-After": "10"}, match=m)
    fake_api.add(responses.GET, page2, json=[{"title": "C", "state": "open"}], match=m)
    fake_api.add(responses.POST, "/repos/acme/app/issues", json={"number": 99}, status=201)

    result = triage(client, "acme/app")

    assert result["number"] == 99
    assert sleeps == [10.0]
    assert json.loads(fake_api.calls[-1].request.body)["body"] == "A\nC"
```

Walk through it: page 1 returns A (open) and B (closed) plus a next link; page 2 first answers `429`, the client waits 10 seconds (recorded, not slept), page 2 then succeeds with C; `triage` keeps open issues A and C; the final `POST` carries `"A\nC"`. One test covered pagination, rate limiting, filtering, and the outbound body, in milliseconds, with no network. A last pointer: the CI pipeline work on Friday will run exactly this kind of test on every push.

### 16. Practice Exercises

**Exercise 1.** Add a test where `create_issue` receives `422 Unprocessable Entity` with a JSON error body. Assert that it raises `ApiError` with status 422, makes exactly one call, and the error message contains the provider's text.

**Exercise 2.** Write a test proving `list_issues` works when the API returns a single page with **no** `Link` header and when the first page is an empty list.

**Exercise 3.** Add a second recorded fixture `repo_404.json` (`{"message": "Not Found", "documentation_url": "..."}`) and use it, via `fixture=`, in the 404 test from section 7.

**Exercise 4.** Parametrize one test so that statuses `500`, `502`, `503`, `504` are all retried and eventually succeed (combine with data-driven testing from earlier today).

<details><summary>Solutions</summary>

```python
# Exercise 1
def test_422_is_reported_without_retry(client, fake_api):
    fake_api.add(responses.POST, "/repos/acme/app/issues",
                 json={"message": "Title is required"}, status=422)
    with pytest.raises(ApiError) as err:
        client.create_issue("acme/app", "", "x")
    assert err.value.status == 422
    assert "Title is required" in str(err.value)
    assert len(fake_api.calls) == 1


# Exercise 2
def test_single_page_and_empty_page(client, fake_api):
    fake_api.add(responses.GET, "/repos/acme/app/issues",
                 json=[{"number": 1}])
    assert [i["number"] for i in client.list_issues("acme/app")] == [1]


def test_empty_first_page(client, fake_api):
    fake_api.add(responses.GET, "/repos/acme/app/issues", json=[])
    assert list(client.list_issues("acme/app")) == []


# Exercise 3 (file tests/fixtures/repo_404.json holds the JSON body)
def test_404_uses_recorded_error_body(client, fake_api):
    fake_api.add(responses.GET, "/repos/acme/missing",
                 fixture="repo_404.json", status=404)
    with pytest.raises(ApiError) as err:
        client.get_repo("acme/missing")
    assert err.value.status == 404


# Exercise 4
@pytest.mark.parametrize("status", [500, 502, 503, 504])
def test_5xx_statuses_are_retried(client, fake_api, status):
    fake_api.add(responses.GET, "/repos/acme/app", status=status)
    fake_api.add(responses.GET, "/repos/acme/app", json={"full_name": "acme/app"})
    assert client.get_repo("acme/app")["full_name"] == "acme/app"
```

Notes: in Exercise 2, a single registration is reused for any matching request, so one `add` is enough. In Exercise 3, create the JSON file first. In Exercise 4, `parametrize` gives each status its own report line.

</details>

### 17. Knowledge Check

1. Why do we inject `sleep` into the client instead of calling `time.sleep` directly?
2. A request goes to a URL you did not register in the mock. What happens, and why is that useful?
3. Which statuses should the client retry, and which should it not?
4. What does `Retry-After: 30` tell the client, and how do you test that it is obeyed?
5. Why keep at least one test that hits the real sandbox, even if it runs only nightly?

<details><summary>Answers</summary>

1. So tests can record delays instead of waiting; a retry test then runs in milliseconds and can assert the exact backoff values.
2. `responses` raises `requests.ConnectionError`, so the test can never silently reach the real internet; it also reveals URL typos.
3. Retry 5xx, 429, and timeouts/connection errors (temporary). Do not retry other 4xx (401 aside, which triggers one token refresh), because repeating a wrong request will not fix it.
4. It says to wait 30 seconds before trying again. Register a 429 with that header followed by a 200, and assert the injected `sleeps` list equals `[30.0]`.
5. Mocks only prove your code matches your *assumptions*. A real contract test detects when the provider changes so recorded fixtures can be updated.

</details>

### 18. Glossary

#### Mock / Test Double
A stand-in for a real dependency that returns canned answers.

#### Fixture (pytest)
Reusable setup code that tests request by name, such as `client` or `fake_api`.

#### Recorded Response (Fixture File)
A real API response saved as JSON and reused to build realistic mocks.

#### Dependency Injection
Passing a class's collaborators (`base_url`, `session`, `sleep`) in from outside rather than hard-coding them.

#### Exponential Backoff
Waiting longer between each retry (0.5s, 1s, 2s, ...) to avoid overloading a struggling server.

#### Retry-After
A response header telling the client how many seconds to wait before retrying.

#### Pagination
Splitting a long list across several responses, usually linked by a `Link: rel="next"` header or a page parameter.

#### Contract Test
A test that checks the real service still matches the shape your code and mocks assume.

#### Cassette
A file of recorded HTTP exchanges used by tools such as `vcrpy` for replay.

#### Over-Mocking
Replacing so much (including your own code) that tests pass without proving anything real.

---

## Summary

- Mock the **far side of the network** for third-party services; never mock the system under test, and prefer real test databases for your own storage.
- Put all HTTP in a **client wrapper** with injected `base_url`, `session`, token, and `sleep`; this makes failure testing fast and clean.
- Build mock payloads from **recorded real responses**, dated and stored as fixtures.
- A reusable **fake-API fixture** gives each test a fresh mock, blocks accidental real calls, and fails on unused mocks.
- Use mocks for what real services cannot do on demand: 4xx/5xx, timeouts, **retries with backoff**, **429 with Retry-After**, **pagination**, and **auth expiry**.
- Assert the **outbound request** (headers, body) as well as the result.
- Keep mocks honest with fixture contract checks, scheduled live tests, and optionally `vcrpy`; avoid over-mocking by asserting on behaviour, not internals.

## Additional Resources

- `responses` library documentation: https://github.com/getsentry/responses
- Requests documentation, *Quickstart* (timeouts, errors) and *Advanced Usage* (sessions): https://requests.readthedocs.io/en/latest/
- pytest documentation, *Fixtures*: https://docs.pytest.org/en/stable/how-to/fixtures.html
- MDN, `Retry-After` header: https://developer.mozilla.org/en-US/docs/Web/HTTP/Headers/Retry-After
- Martin Fowler, *Test Double*: https://martinfowler.com/bliki/TestDouble.html
- vcrpy documentation: https://vcrpy.readthedocs.io/
