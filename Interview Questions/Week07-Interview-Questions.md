# API & QE Automation – Interview Questions

111 questions, grouped by topic and ordered by how often they come up in interviews. Each question is tagged:

- **[Concept]** – explain an idea in your own words.
- **[Code]** – write, read or predict code, commands or config.
- **[Scenario]** – something has gone wrong, or a decision is needed. What do you do?

Each topic is rated:

- **★★★ Core** – expect these in almost any API or automation interview.
- **★★ Important** – often asked, depending on the role.
- **★ Good to know** – newer or specialist topics.

For a short practice interview, start with the ★★★ topics. Try to answer out loud before opening the answer.

| Topic | Rating | Questions |
|---|---|---|
| [API & HTTP Fundamentals](#api--http-fundamentals) | ★★★ Core | Q1–Q12 |
| [Request Details & Authentication](#request-details--authentication) | ★★★ Core | Q13–Q20 |
| [Python `requests` & PyTest](#python-requests--pytest) | ★★★ Core | Q21–Q34 |
| [Response & Contract Validation](#response--contract-validation) | ★★★ Core | Q35–Q41 |
| [Mocking & Test Doubles](#mocking--test-doubles) | ★★★ Core | Q42–Q49 |
| [Framework Design](#framework-design) | ★★★ Core | Q50–Q54 |
| [Test Data, Isolation & Flaky Tests](#test-data-isolation--flaky-tests) | ★★★ Core | Q55–Q61 |
| [CI/CD Concepts](#cicd-concepts) | ★★★ Core | Q62–Q66 |
| [Secrets & Configuration](#secrets--configuration) | ★★★ Core | Q67–Q70 |
| [Running Tests in GitLab Pipelines](#running-tests-in-gitlab-pipelines) | ★★ Important | Q71–Q80 |
| [Accessibility Testing](#accessibility-testing) | ★★ Important | Q81–Q103 |
| [Postman](#postman) | ★★ Important | Q104–Q107 |
| [MCP Server Testing](#mcp-server-testing) | ★ Good to know | Q108–Q111 |

---

## API & HTTP Fundamentals

**★★★ Core** – Almost every API-testing interview starts here.

**Q1. [Concept] Why test at the API layer rather than only through the UI? Where do API tests sit in the test pyramid?**

<details>
<summary>Answer</summary>

API tests sit in the **middle** of the pyramid: many unit tests at the bottom, a good number of API (service or integration) tests in the middle, and a few UI end-to-end tests at the top.

Compared with UI tests, API tests are:

- **Faster**: milliseconds per request, no browser.
- **More stable**: no locators, animations or rendering timing.
- **Earlier**: they can run before the UI exists.
- **More precise**: a failure points to one endpoint, and you can test cases the UI never sends (missing fields, wrong types, no token).

UI tests are still needed for real user journeys, but most business rules are cheaper to cover at the API layer.

</details>

**Q2. [Concept] What are the parts of an HTTP request and an HTTP response?**

<details>
<summary>Answer</summary>

| Request | Response |
|---|---|
| Request line: method, path, version (`GET /posts/1 HTTP/1.1`) | Status line: version, code, reason (`HTTP/1.1 200 OK`) |
| Headers (`Host`, `Accept`, `Content-Type`…) | Headers (`Content-Type`, `Content-Length`…) |
| Blank line | Blank line |
| Optional body (e.g. JSON for a POST) | Optional body (e.g. the JSON you asked for) |

</details>

**Q3. [Code] What is the difference between `curl URL`, `curl -i URL` and `curl -v URL`? In `-v` output, what do lines starting with `>` and `<` mean?**

<details>
<summary>Answer</summary>

- `curl URL` prints only the response body.
- `-i` also prints the status line and the response headers.
- `-v` (verbose) also shows the request that was sent, plus connection details.

In `-v` output, `>` lines were **sent** by you (the request), and `<` lines **came back** from the server (the response).

</details>

**Q4. [Concept] What do "safe" and "idempotent" mean? Classify GET, POST, PUT, PATCH and DELETE.**

<details>
<summary>Answer</summary>

- **Safe:** the request does not change server state (read-only).
- **Idempotent:** sending the same request once or many times leaves the server in the same state.

| Method | Safe | Idempotent |
|---|---|---|
| GET | ✅ | ✅ |
| POST | ❌ | ❌ (each call can create a new item) |
| PUT | ❌ | ✅ |
| PATCH | ❌ | ❌ usually (e.g. "add 1 to counter") |
| DELETE | ❌ | ✅ |

Idempotent methods are safe to **retry** after a timeout. Retrying a POST can create duplicates.

</details>

**Q5. [Concept] What is the difference between PUT and PATCH? What happens if you send a PUT with only the `title` field?**

<details>
<summary>Answer</summary>

PUT **replaces the whole resource**. PATCH **changes only the fields you send**.

On a strict API, a PUT with only `title` replaces the resource with an object that has only `title`, so the other fields are lost or set to defaults. Some APIs instead reject it with `400` or `422`. To change one field, use PATCH.

</details>

**Q6. [Scenario] You send `DELETE /posts/5` twice. The first call returns `200` and the second returns `404`. A colleague says DELETE is therefore not idempotent. Are they right?**

<details>
<summary>Answer</summary>

No. Idempotency is about **server state**, not identical responses. After the first call, post 5 is gone. After the second call, post 5 is still gone, so the state is the same. A different status code on the repeat call is normal and allowed.

</details>

**Q7. [Code] Write a curl command that creates a post with `title`, `body` and a numeric `userId` as JSON. Then write the HTTPie version.**

<details>
<summary>Answer</summary>

```bash
curl -s -X POST https://jsonplaceholder.typicode.com/posts \
  -H "Content-Type: application/json" \
  -d '{"title": "hello", "body": "world", "userId": 1}'
```

```bash
http POST https://jsonplaceholder.typicode.com/posts title=hello body=world userId:=1
```

In HTTPie, `=` sends a JSON string and `:=` sends raw JSON, so `userId:=1` is the number `1`, not the string `"1"`. HTTPie sends JSON and sets `Content-Type: application/json` by default.

</details>

**Q8. [Concept] What does it mean that REST is stateless, and why does it matter to a tester?**

<details>
<summary>Answer</summary>

Each request carries everything the server needs to process it (authentication, ids, parameters). The server keeps no session memory between calls.

For testers this means:

- Any request can be reproduced on its own, for example with curl or Postman.
- Tests can run in any order or in parallel, as long as they don't share data.
- Authentication must be sent on **every** request, which is why a token goes on a session or into a header.

</details>

**Q9. [Concept] What do the status code families mean? Which codes should a tester expect for bad input, and which for a server fault?**

<details>
<summary>Answer</summary>

| Family | Meaning | Examples |
|---|---|---|
| 2xx | Success | `200 OK`, `201 Created`, `204 No Content` |
| 3xx | Redirection | `301`, `302`, `304 Not Modified` |
| 4xx | The **client** made a mistake | `400`, `401`, `403`, `404`, `409`, `422`, `429` |
| 5xx | The **server** failed | `500`, `502`, `503`, `504` |

For bad input, expect a **4xx** with a body that explains which field is wrong: `400 Bad Request` (malformed or invalid), `422 Unprocessable Entity` (valid JSON but fails validation rules), `409 Conflict` (e.g. a duplicate email).

A **5xx in response to bad input is a defect**: the server should validate input, not crash. `5xx` is only acceptable for real server-side faults, such as a downstream service being unavailable (`503`).

</details>

**Q10. [Scenario] On JSONPlaceholder, `POST /posts` returns `201` with `"id": 101`, but `GET /posts/101` then returns `404`. Is this a bug?**

<details>
<summary>Answer</summary>

Not in the test or the API. JSONPlaceholder is a **fake** API: it simulates writes and returns a believable response, but it never stores anything. A test against it must check each response on its own and must not rely on the data persisting. On a real API, the same result would be a defect.

</details>

**Q11. [Scenario] An API returns `200 OK` with body `{"error": "User not found"}`. What is wrong, and how would your tests catch it?**

<details>
<summary>Answer</summary>

The status code contradicts the body. A missing resource should return `404`. Clients and monitoring tools look at the status code, so they would treat this failure as a success.

Tests catch it by checking **both** the status code and the body, e.g. asserting `404` for an unknown id, and checking that a `200` body has the expected fields (or matches a schema). This is why "assert only 200" is an anti-pattern.

</details>

**Q12. [Scenario] You are given a new endpoint, `POST /users`. What test cases would you write?**

<details>
<summary>Answer</summary>

Group them so nothing is missed:

- **Positive:** valid payload returns `201`, the body echoes the input plus an `id`, and a follow-up `GET /users/{id}` returns the same data.
- **Negative:** missing required fields, wrong types, invalid formats (bad email), empty body, malformed JSON → `400` or `422` with a clear error, never `500`.
- **Boundary:** minimum and maximum lengths, just inside and just outside each limit, empty strings, Unicode.
- **Business rules:** duplicate email → `409`; forbidden values rejected.
- **Auth:** no token → `401`; valid token without permission → `403`.
- **Contract:** response matches the schema; correct `Content-Type`; `Location` header if the API uses it.
- **Non-functional basics:** a reasonable response time; sensitive data (passwords) never returned.
- **Cleanup:** delete created users, and use unique data so tests can run in parallel.

</details>

---

## Request Details & Authentication

**★★★ Core** – Parameters, headers and auth come up in nearly every interview.

**Q13. [Concept] When do you use a path variable and when do you use a query parameter? Classify: order id, sort direction, search text, page number.**

<details>
<summary>Answer</summary>

A **path variable** identifies *which* resource (`/orders/42`). A **query parameter** changes *how* you get it: filter, search, sort or page (`/orders?sort=desc`).

- Order id → path
- Sort direction → query
- Search text → query
- Page number → query

</details>

**Q14. [Scenario] `GET /posts?userId=999` returns `200` with `[]`. A tester raises a bug saying it should be `404`. Do you agree?**

<details>
<summary>Answer</summary>

No. The collection `/posts` exists, and the filter simply matched nothing, so `200` with an empty list is correct. `404` means the resource itself doesn't exist, e.g. `/posts/999` or a wrong path. (Always check the API documentation, but this is the common convention.)

</details>

**Q15. [Concept] An endpoint has 95 items and a page size of 20. How many pages are there, how many items are on the last page, and what is the offset of page 3?**

<details>
<summary>Answer</summary>

- Pages: 95 ÷ 20 rounded up = **5**.
- Last page: 95 − 4 × 20 = **15** items.
- Offset of page 3: (3 − 1) × 20 = **40**.

</details>

**Q16. [Concept] Match each status code to the header most likely at fault: `401`, `406`, `415`.**

<details>
<summary>Answer</summary>

- `401 Unauthorized` → `Authorization` (missing or invalid credentials).
- `406 Not Acceptable` → `Accept` (the client asked for a format the server can't produce).
- `415 Unsupported Media Type` → `Content-Type` (the request body is in a format the server doesn't accept).

</details>

**Q17. [Code] You see `Authorization: Basic dXNlcjpwYXNzd2Q=` in a log. What does it contain, and is Basic auth secure?**

<details>
<summary>Answer</summary>

```bash
echo "dXNlcjpwYXNzd2Q=" | base64 -d     # user:passwd
```

It is `username:password` in Base64. Base64 is **encoding, not encryption**, so anyone who sees the header has the password. Basic auth is acceptable only over HTTPS, and the header should never appear in logs. This one should be treated as leaked and the password changed.

</details>

**Q18. [Concept] What is the difference between `401` and `403`? Give an example of each.**

<details>
<summary>Answer</summary>

- `401 Unauthorized` is about **authentication** (who are you?): the token is missing, malformed, wrong or expired.
- `403 Forbidden` is about **authorization** (what may you do?): the token is valid, but this user lacks permission, e.g. a "viewer" calling an admin endpoint.

</details>

**Q19. [Code] Write code that reads a bearer token from the environment and sends it on every request in a session.**

<details>
<summary>Answer</summary>

```python
import os
import requests

TOKEN = os.environ["API_TOKEN"]          # fails fast with KeyError if missing

session = requests.Session()
session.headers.update({"Authorization": f"Bearer {TOKEN}"})

r = session.get("https://httpbin.org/bearer", timeout=10)
```

Every call made with `session` now carries the header, and the token never appears in the source code.

</details>

**Q20. [Concept] What are the three parts of a JWT? Can a test trust the claims after Base64-decoding the payload?**

<details>
<summary>Answer</summary>

`header.payload.signature`, each Base64URL-encoded. Decoding the payload is fine for **inspecting** claims such as `sub`, `role` and `exp` in a test. But anyone can create a token with any payload, so the claims can only be **trusted** after the signature is verified with the right key. That verification is the server's job.

</details>

---

## Python `requests` & PyTest

**★★★ Core** – Expect live coding or code-reading on these.

**Q21. [Concept] What is the default timeout in `requests`, and why must tests always pass `timeout=`?**

<details>
<summary>Answer</summary>

There is **no default timeout**: `requests` waits forever. If a server stops responding, the test (and the whole CI job) hangs until the runner kills it. Passing `timeout=5` (or a configured value) turns a hang into a fast, clear `Timeout` exception.

</details>

**Q22. [Code] What is the difference between `requests.post(url, json=payload)` and `requests.post(url, data=payload)` when `payload` is a dict?**

<details>
<summary>Answer</summary>

- `json=payload` serialises the dict to JSON and sets `Content-Type: application/json`.
- `data=payload` sends it as a **form** (`title=x&userId=1`) with `Content-Type: application/x-www-form-urlencoded`.

A JSON API usually rejects form data (often `400` or `415`) or receives the values as strings.

</details>

**Q23. [Code] What happens when this runs, and what is printed?**

```python
r = requests.get("https://jsonplaceholder.typicode.com/posts/9999", timeout=5)
print(r.status_code, r.ok)
r.raise_for_status()
```

<details>
<summary>Answer</summary>

`requests.get` does **not** raise for a `404`, so it prints `404 False`. Then `raise_for_status()` raises `requests.HTTPError: 404 Client Error: Not Found for url: ...`.

`requests` only raises on its own for network problems (timeouts, connection errors), not for `4xx` or `5xx` responses.

</details>

**Q24. [Concept] Explain `ConnectTimeout`, `ReadTimeout` and `ConnectionError`.**

<details>
<summary>Answer</summary>

- `ConnectTimeout`: the connection couldn't be made in time (host unreachable, firewall).
- `ReadTimeout`: the connection was made, but the server answered too slowly.
- `ConnectionError`: the connection failed outright (DNS failure, connection refused).

Both timeouts are subclasses of `requests.Timeout`, and all of them are subclasses of `requests.RequestException`.

</details>

**Q25. [Concept] How does PyTest discover tests by default? Which of these files are collected: `test_posts.py`, `posts_test.py`, `tests.py`, `check_posts.py`?**

<details>
<summary>Answer</summary>

Default rules:

- Files named `test_*.py` **or** `*_test.py`
- Functions named `test_*` (module level or inside a class)
- Classes named `Test*` that have no `__init__`

Collected: `test_posts.py` and `posts_test.py`. Not collected: `tests.py` and `check_posts.py`. The rules can be changed with `python_files`, `python_functions` and `python_classes` in `pytest.ini`.

</details>

**Q26. [Concept] What is the Arrange–Act–Assert pattern? Why should an API test usually have only one "Act"?**

<details>
<summary>Answer</summary>

- **Arrange:** prepare data, URLs and headers.
- **Act:** send the request.
- **Assert:** check the status, headers and body.

With one Act, a failure points to exactly one request, and the test name can describe one behaviour. Several actions in one test make failures harder to diagnose, and later steps never run if an early one fails.

</details>

**Q27. [Code] How do you run only some tests with PyTest?**

<details>
<summary>Answer</summary>

```bash
pytest tests/test_posts.py                       # one file
pytest tests/test_posts.py::test_get_post        # one test (node id)
pytest -k "auth and not slow"                    # by name expression
pytest -m smoke                                  # by marker
pytest -m "smoke or regression"                  # marker expression
pytest -x                                        # stop at the first failure
pytest --lf                                      # rerun only the tests that failed last time
pytest --collect-only -q                         # list what would run, without running it
```

</details>

**Q28. [Scenario] Your run prints `PytestUnknownMarkWarning: Unknown pytest.mark.smok`. What happened, and how do you stop this from slipping through?**

<details>
<summary>Answer</summary>

The marker `smok` (a typo of `smoke`) is not registered. PyTest only warns, so the test runs but is **not** selected by `-m smoke`.

Fix: register markers in `pytest.ini`, and add `--strict-markers` to `addopts`, which turns an unknown marker into an error:

```ini
[pytest]
addopts = --strict-markers
markers =
    smoke: quick health checks
```

</details>

**Q29. [Concept] What is `conftest.py`, and how does PyTest find the fixtures in it?**

<details>
<summary>Answer</summary>

`conftest.py` is a special file for shared fixtures and hooks. PyTest loads it automatically, so tests **don't import** it. They just name a fixture as an argument.

A `conftest.py` applies to tests in its own folder and all subfolders, so you can have a root one for shared fixtures (HTTP session, base URL, token) and deeper ones for fixtures only one area needs. If two define the same fixture name, the one closest to the test wins.

Keep reusable logic (API clients, helpers) in normal modules, and use `conftest.py` to wire it into tests.

</details>

**Q30. [Concept] Explain the fixture scopes `function`, `module` and `session`. When does code after `yield` run?**

<details>
<summary>Answer</summary>

- `function` (default): a new instance for every test. Good for data a test may change.
- `module`: one per test file. Good for expensive, read-only setup.
- `session`: one per whole run. Good for an HTTP session or an auth token.

Code after `yield` is **teardown**. It runs when the scope ends, **even if the test failed**, which makes it the right place for cleanup.

</details>

**Q31. [Scenario] You get `ScopeMismatch: You tried to access the function scoped fixture token with a session scoped request object`. Explain it and fix it.**

<details>
<summary>Answer</summary>

A session-scoped fixture (e.g. `auth_http`) depends on a function-scoped fixture (`token`). The session object would outlive the value it was built from, so PyTest refuses. A fixture can only use fixtures with the **same or a wider** scope.

Fix: give `token` `scope="session"`, or make `auth_http` function-scoped.

</details>

**Q32. [Code] How many tests does this generate, and what do the ids look like?**

```python
@pytest.mark.parametrize("user_id", [1, 2, 3])
@pytest.mark.parametrize("resource", ["posts", "albums", "todos", "comments"])
def test_nested(user_id, resource): ...
```

<details>
<summary>Answer</summary>

Stacked decorators multiply: 3 × 4 = **12** tests. Ids look like `test_nested[posts-1]`, `test_nested[posts-2]`, …, `test_nested[comments-3]`. (The decorator closest to the function supplies the first part of the id.)

</details>

**Q33. [Code] One row of a parametrized test fails because of a known, ticketed bug. How do you keep the row without breaking the build? How is `xfail` different from `skip`?**

<details>
<summary>Answer</summary>

```python
@pytest.mark.parametrize("post_id, expected", [
    (1, 200),
    pytest.param(-1, 400, marks=pytest.mark.xfail(reason="BUG-123: returns 404")),
])
def test_status(post_id, expected): ...
```

- `skip`: the test **does not run**.
- `xfail`: the test **runs** and is expected to fail. If it unexpectedly passes, it is reported as `XPASS`. With `strict=True`, an `XPASS` fails the run, which tells you the bug is fixed and the marker can be removed.

</details>

**Q34. [Code] Write an `assert_status(response, expected)` helper. Why is it better than `assert r.ok`?**

<details>
<summary>Answer</summary>

```python
def assert_status(response, expected):
    req = response.request
    assert response.status_code == expected, (
        f"{req.method} {req.url} → expected {expected}, "
        f"got {response.status_code}. Body: {response.text[:200]}"
    )
```

`r.ok` is true for **any** code below 400, so it passes for `204` or `302` when you expected `201`. And when it fails, it says only `assert False`. The helper checks the exact code and prints the method, URL, actual code and body, so you can debug without rerunning.

</details>

---

## Response & Contract Validation

**★★★ Core** – Shows whether you test beyond the status code.

**Q35. [Concept] A response is `200 OK`. What else should a test check, layer by layer?**

<details>
<summary>Answer</summary>

1. The body is JSON (`Content-Type` header, and `r.json()` doesn't fail).
2. Required fields are **present**.
3. Fields have the right **type**.
4. **Values** are correct: formats, ranges, enums, and that they match what was sent (echo check).
5. For lists: length, that every item matches (`all`), that at least one matches (`any`), uniqueness.

A JSON Schema can capture layers 2–4 once and be reused.

</details>

**Q36. [Code] Why does this check pass when `id` is `true`? How do you fix it?**

```python
assert isinstance(user["id"], int)
```

<details>
<summary>Answer</summary>

In Python, `bool` is a subclass of `int`, so `isinstance(True, int)` is `True`. Fix:

```python
assert isinstance(user["id"], int) and not isinstance(user["id"], bool)
```

A JSON Schema `"type": "integer"` already rejects booleans.

</details>

**Q37. [Code] After a POST, why is `assert payload.items() <= body.items()` better than `assert body == payload`?**

<details>
<summary>Answer</summary>

The server adds fields such as `id` and `createdAt`, so `body == payload` fails even when everything is correct. `payload.items() <= body.items()` checks that **everything you sent came back unchanged**, while allowing extra fields. (It works when the values are hashable, such as strings and numbers.)

</details>

**Q38. [Concept] What is "API drift", and how does contract (schema) validation catch it?**

<details>
<summary>Answer</summary>

API drift is when an API's shape changes without warning: a field is renamed or removed, a type changes (`1` becomes `"1"`), or a new enum value appears. Clients break, often silently.

Contract validation compares every request and response against the agreed contract (a JSON Schema or a typed model). Any drift fails the test with the exact path, e.g. `['title']: 1 is not of type 'string'`, before users are affected.

</details>

**Q39. [Code] What does `"additionalProperties": false` do in a JSON Schema? When should you use it?**

<details>
<summary>Answer</summary>

It makes any field not listed under `properties` an error, which catches misspelled or unexpected fields.

Use it when the contract really forbids extra fields, such as your own API or request payloads. Avoid it for third-party responses: providers often add fields, and your tests would break even though nothing you rely on changed. The default (`true`) is usually safer there.

</details>

**Q40. [Code] What is the difference between `jsonschema.validate(...)` and `Draft202012Validator(schema).iter_errors(instance)`?**

<details>
<summary>Answer</summary>

`validate()` raises on the **first** error only. `iter_errors()` returns **all** errors, so one failure message can list every problem:

```python
errors = sorted(Draft202012Validator(schema).iter_errors(body), key=str)
assert not errors, "\n".join(f"{list(e.path)}: {e.message}" for e in errors)
```

</details>

**Q41. [Concept] JSON Schema vs Pydantic for response validation: when would you choose each?**

<details>
<summary>Answer</summary>

- **JSON Schema** is language-neutral. One file can be shared with developers, other teams and tools, and it is often generated from OpenAPI.
- **Pydantic** gives typed Python objects with autocompletion (`post.userId`) and can convert values. It suits a Python framework where tests work with the data.

Many teams use both: a schema as the shared contract, and models inside the Python framework.

</details>

---

## Mocking & Test Doubles

**★★★ Core** – A favourite for mid-level roles.

**Q42. [Concept] Explain stub, mock, fake and spy.**

<details>
<summary>Answer</summary>

- **Stub:** returns a canned answer.
- **Mock:** a stub that also checks **how** it was called (arguments, number of calls).
- **Fake:** a simple working replacement, e.g. an in-memory database.
- **Spy:** wraps the real thing and records the calls made to it.

</details>

**Q43. [Concept] Why mock HTTP calls in tests? What should you *not* mock?**

<details>
<summary>Answer</summary>

Mocking makes tests fast, deterministic and offline, avoids cost and side effects (payments, emails), and lets you produce rare cases on demand (`500`, `429`, timeouts).

Don't mock **the API you are actually testing** in end-to-end or contract tests. Mock its *dependencies*. Keep a few real contract or smoke tests against real third parties, so you notice when mocks drift from reality.

</details>

**Q44. [Code] Using the `responses` library, write tests showing that `get_username(1)` raises on a `500` and on a network failure.**

<details>
<summary>Answer</summary>

```python
import pytest
import requests
import responses
import user_client

URL = "https://api.example.com/users/1"


@responses.activate
def test_server_error_raises():
    responses.add(responses.GET, URL, status=500)
    with pytest.raises(requests.HTTPError):
        user_client.get_username(1)


@responses.activate
def test_network_down_raises():
    responses.add(responses.GET, URL, body=requests.ConnectionError("down"))
    with pytest.raises(requests.ConnectionError):
        user_client.get_username(1)
```

</details>

**Q45. [Scenario] `user_client.py` does `from requests import get`. Your test does `patch("requests.get")`, but real HTTP calls still happen. Why?**

<details>
<summary>Answer</summary>

`from requests import get` copies a reference to the function into `user_client` at import time. Patching `requests.get` afterwards changes the name in the `requests` module, but `user_client.get` still points to the original. **Patch where the name is looked up:** `patch("user_client.get")`. If the module does `import requests`, patch `user_client.requests.get`.

</details>

**Q46. [Scenario] A `responses` test fails with `ConnectionError: Connection refused by Responses`. What are the usual causes?**

<details>
<summary>Answer</summary>

The code called a URL or request that doesn't match anything registered. Check:

- A trailing slash, http vs https, or a different host or path.
- Query parameters or headers that don't satisfy a registered `matcher`.
- A different HTTP method (GET vs POST).
- A forgotten `responses.add` for an extra call the code makes.

This failure is useful: an unexpected call fails loudly instead of quietly going to the internet.

</details>

**Q47. [Concept] What is "mock drift", and how do you protect against it?**

<details>
<summary>Answer</summary>

The real API changes (e.g. `name` becomes `fullName`), but your mocks still return the old shape. The mocked tests stay green while production breaks.

Protection: build mock payloads from **recorded real responses**, validate those payloads against the same **schema** the real API is tested against, and run a small set of **contract or smoke tests against the real service** on a schedule.

</details>

**Q48. [Code] A client retries after a `429` and sleeps for `Retry-After` seconds. How do you test the retry without the test actually waiting?**

<details>
<summary>Answer</summary>

Inject the sleep function (dependency injection), then pass a fake that records the calls:

```python
class RatesClient:
    def __init__(self, base_url, api_key, sleep=time.sleep): ...


sleeps = []
client = RatesClient(URL, "key", sleep=sleeps.append)
# register a 429 (Retry-After: 3) and then a 200 with responses
assert client.latest("USD") == {"EUR": 0.9}
assert sleeps == [3]
```

The test runs instantly and still proves the client waited the right amount.

</details>

**Q49. [Code] With `max_retries=2`, the API returns `429` three times in a row. What should happen, and how many calls are made?**

<details>
<summary>Answer</summary>

Three calls: the first try plus 2 retries. The third `429` is not retried, so `raise_for_status()` raises `requests.HTTPError`. The recorded sleeps are `[3, 3]` (two waits).

```python
with pytest.raises(requests.HTTPError):
    rates_client.latest("USD")
assert len(rates_mock.calls) == 3
```

</details>

---

## Framework Design

**★★★ Core** – Often the deciding question for senior roles.

**Q50. [Scenario] You join a team with no API automation. How would you design the framework?**

<details>
<summary>Answer</summary>

Start small, with clear layers:

1. **Stack:** Python, `requests`, PyTest, `jsonschema` or Pydantic, `responses` for mocks, `pytest-html` and JUnit XML for reports.
2. **Config:** one `settings` module that reads environment variables (base URL, timeouts, tokens). No hard-coded environments or secrets.
3. **Client:** one `ApiClient` with a session, timeouts and base URL. It returns raw responses and never asserts.
4. **Service classes:** one per resource (`UsersApi.create(...)`), so tests never build URLs.
5. **Models and schemas:** to validate responses and catch contract drift.
6. **Fixtures:** in `conftest.py` for clients, auth and self-cleaning test data.
7. **Tests:** short, readable, independent, tagged with markers (`smoke`, `regression`).
8. **Test data:** builders and data files for data-driven cases, with unique values.
9. **Mocks:** for third-party dependencies, with a switch to run offline.
10. **CI:** smoke on every merge request, full regression on `main` and nightly, reports published as artifacts.

Then grow it: start with smoke tests for the most critical endpoints and add coverage over time.

</details>

**Q51. [Concept] Why should a shared `ApiClient` never assert, and never call `raise_for_status()`?**

<details>
<summary>Answer</summary>

The client's job is to send requests and return the raw response. The **test** decides what is correct. If the client raised on every `4xx`, a negative test that *expects* `404` or `401` could not be written. Keeping assertions in tests also keeps failure messages in the test report, where they belong.

</details>

**Q52. [Concept] Why build `ApiClient` in its own module instead of putting the request logic directly in `conftest.py`?**

<details>
<summary>Answer</summary>

They do different jobs. The client decides **how** to talk to the API (base URL, timeout, headers). A `conftest.py` fixture decides **who gets one and for how long** (setup, teardown, scope).

A separate module can be imported by scripts and tools outside PyTest (`conftest.py` cannot be imported that way), keeps `conftest.py` small, and makes the client a layer you can swap or mock. The usual pattern is both: the class in `api_client.py`, and a session-scoped fixture in `conftest.py` that creates it.

</details>

**Q53. [Concept] Describe the layers of a reusable API test framework and the one job of each.**

<details>
<summary>Answer</summary>

| Layer | Job |
|---|---|
| `config/settings.py` | Reads environment variables (base URL, timeout, mock switch) in one place |
| `api/client.py` | Sends requests: session, base URL, timeout. Never asserts |
| `api/<resource>.py` | One class per resource (`PostsApi.get(1)`). Builds paths |
| `models/` | Pydantic models that describe and validate data |
| `mocks/` | A fake API for offline runs |
| `conftest.py` | Fixtures that wire the layers together |
| `tests/` | Only test logic, written in business language |
| `pytest.ini` | Markers and reports (JUnit, HTML) |

An API change is then fixed in **one** place, not in every test.

</details>

**Q54. [Scenario] A test does `os.environ["USE_MOCK"] = "1"` at its start, but the suite still calls the live API. Why?**

<details>
<summary>Answer</summary>

`settings = Settings()` reads the environment **at import time**, when `conftest.py` first imports it, which is before any test runs. Changing the variable inside a test is too late. Set it before starting PyTest (`USE_MOCK=1 pytest`), or read settings lazily, e.g. inside a fixture.

</details>

---

## Test Data, Isolation & Flaky Tests

**★★★ Core** – Every team has flaky tests; interviewers want to know how you handle them.

**Q55. [Concept] What is data-driven testing? What does a "builder" (factory) add to a data table?**

<details>
<summary>Answer</summary>

DDT separates **test logic** (send, then check) from **test data** (inputs and expected results). One test function runs once per row, so a new scenario is a new row, not a new function. Each row needs a readable id so a failure names the case.

A builder fills in valid defaults, so each row lists only what is **different** about it:

```python
def make_post(**overrides):
    payload = {"title": "default", "body": "default", "userId": 1}
    payload.update(overrides)
    return payload
```

</details>

**Q56. [Scenario] A CSV-driven test fails with `assert 201 == '201'`. What is wrong?**

<details>
<summary>Answer</summary>

`csv.DictReader` reads **every value as a string**. The expected status `'201'` must be converted: `int(row["status"])`. The same applies to ids and numbers sent in payloads, e.g. `int(row["user_id"])`. JSON data files don't have this problem, because they keep real types.

</details>

**Q57. [Scenario] Tests that load `data/cases.json` pass when run from the project folder, but fail with `FileNotFoundError` in CI. Why, and what is the fix?**

<details>
<summary>Answer</summary>

The path is relative to the **current working directory**, which differs between your terminal and CI. Build it from the file's own location instead:

```python
from pathlib import Path
DATA_DIR = Path(__file__).resolve().parent / "data"
```

</details>

**Q58. [Scenario] A test passes when run alone but fails in the full suite. What do you check first?**

<details>
<summary>Answer</summary>

It is coupled to another test through shared state. Check:

1. Module-level or global variables, or class attributes, that another test changes.
2. Leftover data on the server or in files from an earlier test (e.g. a hard-coded name such as `"test_user"`).
3. Environment variables or wide-scope (session or module) fixtures that a test modifies.

Use `pytest-randomly` to expose it, and `--randomly-seed=<n>` to reproduce the failing order. Fix it with function-scoped fixtures, unique names (`uuid4`), cleanup after `yield`, `monkeypatch` and `tmp_path`.

</details>

**Q59. [Code] Why use `monkeypatch.setenv` and `tmp_path` instead of setting `os.environ` and writing files directly in a test?**

<details>
<summary>Answer</summary>

Both are undone or isolated automatically:

- `monkeypatch.setenv("BASE_URL", "...")` is **reverted after the test**, so no later test sees the changed value. Setting `os.environ` directly leaks into every later test.
- `tmp_path` gives each test a **fresh, unique folder**, so tests can't collide on file names or read each other's leftovers.

```python
def test_report(tmp_path, monkeypatch):
    monkeypatch.setenv("REPORT_DIR", str(tmp_path))
    ...
```

</details>

**Q60. [Concept] What makes API tests flaky? Give the common causes and how to fix each.**

<details>
<summary>Answer</summary>

| Cause | Fix |
|---|---|
| Shared state or test-order dependence | Function-scoped fixtures, unique data (`uuid4`), cleanup after `yield` |
| Unstable shared environment or data | Create your own data; don't assert on totals other people change |
| Timing: async processing, eventual consistency | Poll with a bounded wait instead of a fixed `sleep` |
| Tight performance thresholds | Use generous thresholds; keep real performance testing separate |
| Third-party services | Mock them in functional tests; check the real service in a few contract tests |
| No timeouts, or rate limits (`429`) | Always set `timeout=`; respect `Retry-After` with bounded retries |
| Parallel runs colliding | Isolate data per test; make tests safe for `pytest -n auto` |

Use `pytest-randomly` to expose order dependence, and track flaky tests with a ticket instead of blanket retries.

</details>

**Q61. [Scenario] A test fails randomly about 1 run in 20. A teammate suggests adding `retry: 2` to the job. What do you say?**

<details>
<summary>Answer</summary>

A flaky test is dangerous because people learn to ignore red builds and just rerun, so **real** failures get ignored too, and trust in the quality gate disappears. Blanket retries hide the problem, and they can hide an intermittent product bug.

Better: quarantine the test (a marker plus a ticket, run outside the gate), find the cause (shared state, timing, test order, external dependency) and fix it. `retry:` is acceptable only for known **infrastructure** failures, e.g. `retry: {max: 1, when: runner_system_failure}`, and retries should be tracked.

</details>

---

## CI/CD Concepts

**★★★ Core** – Asked of every automation engineer.

**Q62. [Concept] Explain Continuous Integration, Continuous Delivery and Continuous Deployment.**

<details>
<summary>Answer</summary>

- **Continuous Integration:** developers merge small changes often, at least daily. Each change is automatically built and tested.
- **Continuous Delivery:** every change that passes the pipeline **can** be released, and a person decides when.
- **Continuous Deployment:** every change that passes is released to production **automatically**, with no manual step.

A bank might choose Delivery because of regulatory approval, audits or fixed release windows.

</details>

**Q63. [Concept] What are the four DORA metrics, and which direction is "good" for each?**

<details>
<summary>Answer</summary>

| Metric | Good direction |
|---|---|
| Deployment frequency | Higher |
| Lead time for changes (commit → production) | Shorter |
| Change failure rate (% of deployments causing a failure) | Lower |
| Time to restore service (recently renamed *failed deployment recovery time*) | Shorter |

The first two measure speed, and the last two measure stability. Good teams improve both together.

</details>

**Q64. [Concept] What does "build once, deploy many" mean? Why is rebuilding for each environment risky?**

<details>
<summary>Answer</summary>

Build **one versioned artifact** (e.g. a Docker image tagged `1.4.2+a1b2c3d`) and promote that exact artifact through dev → staging → production. Configuration changes per environment through variables, not code.

Rebuilding per environment can pick up different dependency versions or base images, so production would run something that was never tested.

</details>

**Q65. [Scenario] Choose a deployment strategy for: (a) an internal tool where 10 minutes of downtime is fine, (b) a payment API, (c) a new UI you want 5% of users to try.**

<details>
<summary>Answer</summary>

- (a) **Recreate**: simplest, and the downtime is acceptable.
- (b) **Blue-green**: switch traffic between two environments, with instant rollback.
- (c) **Canary** (route 5% of traffic) or a **feature flag** (deploy switched off, enable for 5% of users).

</details>

**Q66. [Code] Why does a post-deploy health-check script end with `sys.exit(0 if healthy else 1)`? What else should it do?**

<details>
<summary>Answer</summary>

A pipeline decides pass or fail **by exit code**: `0` means success, and anything else fails the job and stops the pipeline. A script that only prints "unhealthy" would let a broken deployment through.

It should also:

- Use a **timeout** on every request so it never hangs.
- **Retry a bounded number of times** with a delay, because services take a moment to start.
- Read the target from environment variables, so the same script checks every environment.

</details>

---

## Secrets & Configuration

**★★★ Core** – Short questions, but a wrong answer is a red flag.

**Q67. [Concept] What is the difference between configuration and a secret? What do GitLab's *Masked* and *Protected* variable flags do?**

<details>
<summary>Answer</summary>

**Configuration** changes between environments (base URL, timeouts, feature flags). Defaults can live in the repo. A **secret** grants access (tokens, passwords, keys) and must never be in the repo.

- **Masked:** the value is replaced with `[MASKED]` in job logs. (It must meet GitLab's rules: at least 8 characters, a limited character set, one line.)
- **Protected:** the variable is only given to pipelines on **protected** branches and tags, such as `main`.

</details>

**Q68. [Scenario] A teammate committed `API_TOKEN=live-123` last week and deleted it today. What do you do, in order?**

<details>
<summary>Answer</summary>

1. **Rotate or revoke the token immediately.** Deleting the file doesn't help: it is still in Git history and may already be copied.
2. Check access logs for misuse.
3. Store the new token as a masked, protected CI/CD variable.
4. Remove it from history if your policy requires it (e.g. `git filter-repo`), knowing that clones may still have it.
5. Prevent a repeat: secret detection in CI, a pre-commit hook such as gitleaks, and `.env` in `.gitignore`.

</details>

**Q69. [Scenario] `check-config` passes on `main`, but on a feature branch it fails with `RuntimeError: Missing required setting: API_TOKEN`. Why?**

<details>
<summary>Answer</summary>

`API_TOKEN` is a **Protected** variable, and feature branches are not protected, so the job gets an empty value. `settings.py` fails fast as designed.

Options: limit the job to the default branch with `rules:`; use a separate, unprotected, low-privilege test token for branches; or protect the branch pattern. Don't simply un-protect the production token.

</details>

**Q70. [Code] Write a `settings.py` that loads `.env` locally, fails fast when `API_TOKEN` is missing, and can log the token safely.**

<details>
<summary>Answer</summary>

```python
import os
from dotenv import load_dotenv

load_dotenv()      # reads .env locally; does nothing in CI, where there is no .env


def require(name):
    value = os.getenv(name)
    if not value:
        raise RuntimeError(f"Missing required setting: {name}")
    return value


def masked(value):
    return value[:4] + "***" if value else "<empty>"


BASE_URL = os.getenv("BASE_URL", "https://jsonplaceholder.typicode.com")
API_TOKEN = require("API_TOKEN")
```

Failing fast gives one clear message, instead of dozens of confusing `401` failures later.

</details>

---

## Running Tests in GitLab Pipelines

**★★ Important** – Tool-specific, but the ideas apply to any CI system.

**Q71. [Concept] In GitLab CI, how do stages and jobs run? What happens when a job fails?**

<details>
<summary>Answer</summary>

Stages run **in order**. Jobs **inside a stage run in parallel**. A stage starts only when the previous stage has succeeded.

When a job fails, the other jobs in that stage still finish, but later stages don't start, and the pipeline is marked failed. The exception is `allow_failure: true`, which shows a warning and lets the pipeline continue. A job fails when any `script` command exits with a non-zero code.

</details>

**Q72. [Code] What does this do, and why is it useful?**

```yaml
build:
  stage: build
  needs: [lint, smoke]
  script:
    - echo "Building..."
```

<details>
<summary>Answer</summary>

`needs:` turns the pipeline into a **DAG**. `build` starts as soon as `lint` and `smoke` succeed, without waiting for every other job in the `test` stage (such as a slow regression job). It also downloads artifacts only from those two jobs. The result is faster feedback and a shorter pipeline.

Pitfall: if a needed job may be skipped by `rules`, add `optional: true`, or the pipeline is invalid.

</details>

**Q73. [Code] Write `rules:` so that a job runs only on merge requests, and another runs only on the default branch as a manual job.**

<details>
<summary>Answer</summary>

```yaml
test:smoke:
  script: pytest -q -m smoke
  rules:
    - if: $CI_PIPELINE_SOURCE == "merge_request_event"

deploy-staging:
  script: echo "Deploying $CI_COMMIT_SHORT_SHA"
  rules:
    - if: $CI_COMMIT_BRANCH == $CI_DEFAULT_BRANCH
      when: manual
```

Don't mix `only`/`except` with `rules` in the same job. A typo in a variable name (`$CI_COMMIT_BRANH`) silently evaluates to false, so the job never runs.

</details>

**Q74. [Scenario] A job shows "This job is stuck". Another fails with `pytest: command not found`. A third passes locally but fails in CI. Give the likely cause of each.**

<details>
<summary>Answer</summary>

1. **Stuck:** no runner is available. Enable shared runners (**Settings → CI/CD → Runners**), or check that the job's `tags` match a runner.
2. **`pytest: command not found`:** `pytest` is missing from `requirements.txt`, or `before_script` doesn't install it.
3. **Passes locally, fails in CI:** CI uses a clean image. Look for a different Python version, a file that is git-ignored or never committed, a missing environment variable, or something installed only on your machine.

</details>

**Q75. [Concept] Which tests would you run on a merge request, on `main`, and on a nightly schedule? Why?**

<details>
<summary>Answer</summary>

| Trigger | Run | Why |
|---|---|---|
| Merge request | Smoke tests (`-m smoke`), lint, maybe accessibility | Fast feedback, in minutes |
| Push to `main` | Full regression plus accessibility | Protects what will be released |
| Nightly schedule | Full regression (often against real services) | Catches drift in dependencies and data without slowing developers |

</details>

**Q76. [Concept] What do `pytest --maxfail=3` and `pytest -n auto` do, and why are they useful in CI?**

<details>
<summary>Answer</summary>

- `--maxfail=3` stops after three failures. If the API is down, you get a quick, readable failure instead of 400 identical errors and a long wait.
- `-n auto` (pytest-xdist) runs tests in parallel, one worker per CPU core, which shortens the job. It only works safely if the tests are **isolated**.

</details>

**Q77. [Code] A CI job must start a small web site and then run accessibility tests against it. Write the script, and explain why `sleep 30` is a poor choice.**

<details>
<summary>Answer</summary>

```yaml
test:a11y:
  image: mcr.microsoft.com/playwright/python:v1.49.0-jammy
  variables:
    SITE_URL: "http://localhost:8000"
  script:
    - pip install -r requirements.txt
    - python -m http.server 8000 --directory site &
    - |
      for i in $(seq 1 15); do
        curl -fs "$SITE_URL/index.html" > /dev/null && break
        echo "waiting for site..."; sleep 1
      done
    - pytest -q -m accessibility
```

`sleep 30` wastes 30 seconds when the site is ready in 1, and is still too short when the site is slow. A **health-wait loop** continues as soon as the site responds, with a bounded maximum.

</details>

**Q78. [Scenario] The accessibility job fails with `Executable doesn't exist at /ms-playwright/chromium-...`. What happened?**

<details>
<summary>Answer</summary>

The Playwright Python package version doesn't match the browsers in the Docker image. For example, `requirements.txt` installs `playwright==1.50.0`, but the image is `playwright/python:v1.49.0`, so the package looks for a browser build that isn't there.

Fix: keep them identical. Pin `playwright==1.49.0`, or change the image to `v1.50.0-jammy`.

</details>

**Q79. [Concept] What is the difference between artifacts and cache in GitLab? Why use `when: always` on test-report artifacts?**

<details>
<summary>Answer</summary>

| | Artifact | Cache |
|---|---|---|
| Purpose | Keep job **outputs** (reports, packages) | Speed up job **inputs** (pip downloads) |
| Reliability | Guaranteed until `expire_in` | Best effort; may be empty |
| Passed to later jobs | Yes (`needs` / `dependencies`) | No guarantee |

The default is `when: on_success`, so a failing test job would discard its reports, exactly when you need them. `when: always` keeps them.

</details>

**Q80. [Scenario] After adding reporting, the pipeline's Tests tab is empty, and Deploy → Pages shows nothing. What do you check?**

<details>
<summary>Answer</summary>

**Empty Tests tab:**

- `artifacts:reports:junit` must point to the same path as `--junitxml` in `pytest.ini` (e.g. `reports/junit.xml`).
- The artifact needs `when: always`, or the file is lost when tests fail.
- The path must be inside the project folder.

**No Pages site:**

- The job must be named `pages` and must publish a `public/` folder as an artifact.
- It only runs on the default branch (because of its `rules:`), so a branch push won't create it.
- `needs: [test:regression]` means it is skipped if regression fails.
- After the `pages:deploy` job runs, the URL appears under **Deploy → Pages**. The first deployment can take a few minutes. On a private project, only members can open the site unless Pages access is set to Everyone.

</details>

---

## Accessibility Testing

**★★ Important** – Increasingly asked, especially for web, public-sector and enterprise roles. Expect both principles and hands-on testing questions.

**Q81. [Concept] What does POUR stand for? Give one testable check for each principle.**

<details>
<summary>Answer</summary>

- **Perceivable:** images have meaningful `alt` text, and text contrast is at least 4.5:1 (1.4.3).
- **Operable:** everything works with the keyboard alone (2.1.1), and focus is visible (2.4.7).
- **Understandable:** the page language is set (3.1.1), and form errors explain how to fix them (3.3.x).
- **Robust:** controls expose a name, role and state to assistive technology (4.1.2).

</details>

**Q82. [Concept] What are WCAG levels A, AA and AAA? Which level do most teams and laws target?**

<details>
<summary>Answer</summary>

They are conformance levels for the success criteria: **A** is the minimum, **AA** is the standard target, and **AAA** is enhanced (not required for whole sites, because some content can't meet it). Most laws and policies (ADA case law, Section 508, the European Accessibility Act via EN 301 549) point to **WCAG 2.x level AA**.

</details>

**Q83. [Concept] Who benefits from accessibility, and why does a business care about it?**

<details>
<summary>Answer</summary>

About 1.3 billion people (around 1 in 6) live with a significant disability, and accessibility also helps people with:

- **Permanent** limits: blindness, deafness, limited motor control, cognitive disabilities.
- **Temporary** limits: a broken arm, an eye infection.
- **Situational** limits: bright sunlight, a noisy train, holding a baby in one arm.
- **Changing abilities:** older users with declining vision, hearing or dexterity.

Businesses care because of **legal risk** (ADA lawsuits, Section 508, the European Accessibility Act), **market reach** (more customers can buy), and **quality**: accessible sites are usually better structured, easier to automate and better for SEO.

</details>

**Q84. [Concept] What is the "first rule of ARIA"? Why is `<div role="button">` still worse than `<button>`?**

<details>
<summary>Answer</summary>

Don't use ARIA if a native HTML element can do the job. ARIA only changes what assistive technology is **told**, not how the element **behaves**.

`<div role="button">` announces "button", but it isn't focusable and doesn't respond to Enter or Space. You would have to add `tabindex="0"`, key handlers and disabled-state handling yourself. `<button>` gives you all of that for free.

</details>

**Q85. [Concept] What is an element's "accessible name"? Where does it come from, and how do you check it?**

<details>
<summary>Answer</summary>

The accessible name is what assistive technology announces for an element, e.g. "Email, edit" or "Submit, button". Browsers compute it in roughly this order:

1. `aria-labelledby` (text of the referenced element)
2. `aria-label`
3. Native labelling: `<label for>`, `alt` on images, `<caption>`, `<legend>`
4. The element's own text content (for buttons and links)
5. `title` or `placeholder`, as a weak last resort

Check it in DevTools: **Elements → Accessibility** shows the computed name and role. In Playwright, `page.get_by_role("button", name="Submit")` only finds the element if the name is right, which makes it a useful test.

</details>

**Q86. [Concept] Why do headings and landmarks matter, and how do you test them?**

<details>
<summary>Answer</summary>

Screen reader users rarely read a page top to bottom. They jump by **headings** (`H` in NVDA) and **landmarks** (`D` in NVDA), the way sighted users scan. Without them, every page is one long wall of content (1.3.1 Info and Relationships, 2.4.6 Headings and Labels).

Check:

- Exactly one `<h1>` that describes the page, and a logical outline (`h2` sections, `h3` subsections). Skipping levels is a best-practice issue rather than a strict WCAG failure.
- Real heading elements, not styled `<div>`s.
- Landmarks: `<header>`, `<nav>`, `<main>` (exactly one), `<footer>`, and all content inside a landmark.
- Tools: the NVDA elements list (`Insert+F7`), a headings browser extension, and axe rules such as `page-has-heading-one`, `landmark-one-main` and `region`.

</details>

**Q87. [Concept] Write appropriate `alt` text for: (a) a logo that links to the home page, (b) a decorative divider, (c) a chart showing sales up 20%.**

<details>
<summary>Answer</summary>

- (a) Describe what the link does: `alt="Demo Co home"`.
- (b) Decorative: `alt=""`, so screen readers skip it. (Don't leave `alt` off: a missing `alt` makes many screen readers read the file name.)
- (c) Give the key message: `alt="Sales rose 20% from Q1 to Q2"`, or a short `alt` plus a nearby data table for the detail.

</details>

**Q88. [Concept] What are the WCAG AA contrast ratios? Does grey `#aaaaaa` text on white pass?**

<details>
<summary>Answer</summary>

- Normal text: at least **4.5:1** (1.4.3).
- Large text (18pt, or 14pt bold, and up): at least **3:1**.
- UI components and meaningful graphics: at least **3:1** (1.4.11).

`#aaaaaa` on white is about **2.3:1**, so it fails. `#595959` is about 7:1 and passes AA and AAA.

</details>

**Q89. [Code] What is wrong with this form field, and how do you fix it?**

```html
<input type="email" placeholder="Email">
<span style="color:red">Invalid email</span>
```

<details>
<summary>Answer</summary>

- The placeholder is not a label: it disappears while typing, is often low contrast, and isn't reliably announced (1.3.1, 3.3.2).
- The error is shown **only by colour** (1.4.1 Use of Color) and isn't connected to the field, so a screen reader user doesn't hear it (3.3.1 Error Identification).

```html
<label for="email">Email</label>
<input id="email" type="email" autocomplete="email"
       aria-invalid="true" aria-describedby="email-error">
<p id="email-error">Error: enter an email address like name@example.com</p>
```

The label names the field, `aria-describedby` makes the screen reader read the error with the field, `aria-invalid` marks the state, and the error text says how to fix it.

</details>

**Q90. [Concept] What is an `aria-live` region? When would you use `polite` vs `assertive`, and how do you test it?**

<details>
<summary>Answer</summary>

A live region tells assistive technology to **announce content that changes without a page load**, such as "Item added to cart" or "3 results found". This covers WCAG 4.1.3 Status Messages (AA).

- `aria-live="polite"` (or `role="status"`): announced when the user is idle. Use it for most updates.
- `aria-live="assertive"` (or `role="alert"`): interrupts immediately. Use it only for urgent errors.

Test with a screen reader: trigger the update and confirm it is announced **without moving focus**. A common bug is adding the live region at the same moment as its text. The region must already exist in the page before its content changes.

</details>

**Q91. [Concept] What is required for video and audio content?**

<details>
<summary>Answer</summary>

| Need | For whom | WCAG |
|---|---|---|
| **Captions** (synchronised text of speech and important sounds) for prerecorded video | Deaf and hard-of-hearing users | 1.2.2 (A) |
| **Captions** for live video | Same | 1.2.4 (AA) |
| **Audio description** of important visual information | Blind users | 1.2.5 (AA) |
| **Transcript** for audio-only content (e.g. a podcast) | Deaf users | 1.2.1 (A) |

Also check that media doesn't autoplay sound for more than 3 seconds without a way to stop it (1.4.2), and that player controls work with the keyboard.

</details>

**Q92. [Concept] What do `tabindex="0"`, `tabindex="-1"` and `tabindex="3"` do? Which is a defect?**

<details>
<summary>Answer</summary>

- `0`: adds the element to the natural Tab order.
- `-1`: focusable by script only (e.g. the target of a skip link or a dialog heading), not by Tab.
- A **positive** value (`3`) jumps the element ahead of the natural order. This is a defect, because the focus order stops matching the visual order (2.4.3 Focus Order).

</details>

**Q93. [Scenario] You are asked to keyboard-test a sign-up form. What is your checklist?**

<details>
<summary>Answer</summary>

Start from the address bar and **don't touch the mouse**.

1. Tab reaches every interactive element, in an order that matches the visual order.
2. Focus is **always visible**.
3. Enter or Space activates buttons and links, and arrow keys work inside widgets.
4. There is no **keyboard trap**: you can always Tab or Esc out.
5. A skip link moves focus to the main content.
6. Errors are announced, and focus moves to them sensibly.
7. Modals keep focus inside while open, Esc closes them, and focus returns to the trigger.

Record each finding as steps, expected, actual and WCAG criterion.

</details>

**Q94. [Scenario] You are testing a modal dialog. What should you check?**

<details>
<summary>Answer</summary>

- **Opening:** focus moves into the dialog (its heading or first field).
- **Inside:** Tab and Shift+Tab cycle only within the dialog; the page behind can't be reached or read.
- **Closing:** Esc closes it, a visible close button works by keyboard, and focus returns to the element that opened it.
- **Semantics:** `role="dialog"` (or a native `<dialog>` opened with `showModal()`), `aria-modal="true"`, and an accessible name via `aria-labelledby` pointing to its heading.
- **Screen reader:** it announces the dialog name and role when it opens.

A common bug is a dialog that looks modal but lets Tab escape into the page behind it.

</details>

**Q95. [Scenario] A page looks fine at 100%, but at 200% zoom text overlaps, and on a narrow phone screen users must scroll sideways to read. Which WCAG criteria apply, and how do you test them?**

<details>
<summary>Answer</summary>

- **1.4.4 Resize Text (AA):** text can be enlarged to 200% without losing content or function.
- **1.4.10 Reflow (AA):** at a width of 320 CSS pixels (e.g. 400% zoom on a 1280px screen), content reflows into one column with no horizontal scrolling (except things like maps and data tables).
- Related: **1.4.12 Text Spacing**, where content must survive larger line, letter and word spacing.

Test by zooming the browser to 200% and 400%, or by setting a 320px viewport in DevTools or Playwright (`page.set_viewport_size({"width": 320, "height": 800})`), and checking that nothing is cut off, overlapping or only reachable by sideways scrolling.

</details>

**Q96. [Scenario] The axe scan is green, but a keyboard user cannot reach the Submit control, which is a `<div onclick>`. How is that possible, and what does it mean for your test strategy?**

<details>
<summary>Answer</summary>

Automated scanners only check machine-detectable rules and catch an estimated **30–40%** of issues. axe can't tell that a plain `div` with a click handler should be a button. It also can't judge focus order, meaningful `alt` text or screen-reader experience.

Strategy: treat the scan as a **smoke alarm**, not a certificate. Combine automated scans (fast, in CI) with manual keyboard and screen-reader testing. Also review axe's `incomplete` results by hand, and add regression tests for defects you find manually.

</details>

**Q97. [Code] Write a PyTest test that scans a local page with axe, limited to WCAG A/AA rules, and fails with a readable report.**

<details>
<summary>Answer</summary>

```python
from axe_playwright_python.sync_playwright import Axe

WCAG_TAGS = ["wcag2a", "wcag2aa", "wcag21a", "wcag21aa", "wcag22aa"]
OPTIONS = {"runOnly": {"type": "tag", "values": WCAG_TAGS}}


def test_home_is_accessible(page):                 # `page` comes from pytest-playwright
    page.goto("http://localhost:8000/index.html")
    results = Axe().run(page, options=OPTIONS)
    assert results.violations_count == 0, results.generate_report()
```

</details>

**Q98. [Code] Your team wants the accessibility gate to block only `serious` and `critical` violations for now. Write the check.**

<details>
<summary>Answer</summary>

```python
from axe_playwright_python.sync_playwright import Axe

BLOCKING = {"critical", "serious"}


def test_no_blocking_violations(page):
    page.goto("http://localhost:8000/index.html")
    results = Axe().run(page, options={"runOnly": {"type": "tag", "values": ["wcag2a", "wcag2aa"]}})
    blocking = [v for v in results.response["violations"] if v["impact"] in BLOCKING]
    summary = [f'{v["id"]} ({v["impact"]}): {len(v["nodes"])} nodes' for v in blocking]
    assert not blocking, "\n".join(summary)
```

Report the `moderate` and `minor` ones (e.g. in the saved JSON) and ticket them, so they are not forgotten. Tighten the gate over time.

</details>

**Q99. [Code] Write a Playwright test, needing no web server, that proves the Submit button is reachable with the keyboard.**

<details>
<summary>Answer</summary>

```python
FIXED = """
<html lang="en"><body><main>
  <label for="email">Email</label><input id="email" type="email">
  <button type="submit">Submit</button>
</main></body></html>
"""


def test_submit_is_keyboard_operable(page):
    page.set_content(FIXED)
    page.keyboard.press("Tab")      # email
    page.keyboard.press("Tab")      # submit
    focused = page.evaluate(
        "document.activeElement.tagName + ':' + document.activeElement.textContent")
    assert focused == "BUTTON:Submit"
```

If the button is replaced by `<div class="btn">Submit</div>`, the test fails, which proves it can catch the regression.

</details>

**Q100. [Scenario] An axe report shows `color-contrast` on 37 nodes, all `.btn-secondary` elements, across 12 pages. How many tickets do you open?**

<details>
<summary>Answer</summary>

**One.** The root cause is a single shared style (contrast/design in `.btn-secondary`), so one fix resolves all 37 nodes. List the affected pages and the node count as evidence. One ticket per node creates noise and hides the real fix.

</details>

**Q101. [Concept] What is the difference between severity and priority? Give an example where they differ.**

<details>
<summary>Answer</summary>

**Severity** is the impact on users. **Priority** is how soon the fix happens, decided with the product owner.

Example: low contrast on checkout fine print is **minor** severity, but the checkout page is used by every customer and a legal audit is next week, so priority is **high**. The reverse also happens: a blocker on a page about to be retired may get low priority.

</details>

**Q102. [Concept] What should a good accessibility bug report contain?**

<details>
<summary>Answer</summary>

- A title that names the control, the criterion and the impact (`[A11y][Blocker] Sign-up "Submit" not operable by keyboard – WCAG 2.1.1`).
- Environment: browser, OS, assistive technology and version, page.
- Steps to reproduce, expected result and actual result (including what was announced).
- Users affected and severity.
- WCAG criterion and level.
- Root cause and a suggested fix.
- Evidence: screenshot, recording, axe rule id.

</details>

**Q103. [Scenario] Your manager asks you to set up accessibility testing for a product that has none. What is your strategy?**

<details>
<summary>Answer</summary>

1. **Agree the target:** WCAG 2.2 AA, and which key user journeys matter most (sign-up, search, checkout).
2. **Shift left:** accessibility checks in design reviews (contrast, focus states, headings) and in code review (semantic HTML, labels).
3. **Automate:** axe scans in CI for key pages and states. Start with a **baseline** (no new violations) and block `serious`/`critical` first.
4. **Test manually** each release: keyboard pass and screen-reader pass (e.g. NVDA + Chrome, VoiceOver + Safari) on the key journeys, plus zoom and reflow checks.
5. **Triage:** group findings by root cause, rate severity, and add a regression test when a defect is fixed.
6. **Measure:** violations per page over time, open defects by severity, and the percentage of journeys that pass the manual checklist.
7. **Include real users:** usability sessions with people who use assistive technology, because tools and checklists miss real-world problems.

</details>

---

## Postman

**★★ Important** – Common for manual-to-automation and junior roles.

**Q104. [Code] Write a Postman post-response script that checks the status is `200` and that `title` is a non-empty string.**

<details>
<summary>Answer</summary>

```javascript
pm.test("Status code is 200", function () {
    pm.response.to.have.status(200);
});

pm.test("Title is a non-empty string", function () {
    const post = pm.response.json();
    pm.expect(post.title).to.be.a("string").and.not.be.empty;
});
```

</details>

**Q105. [Concept] List Postman variable scopes from narrowest to widest. If `baseUrl` exists as both an environment and a collection variable, which one is used?**

<details>
<summary>Answer</summary>

From narrowest (wins) to widest: **local → data → environment → collection → global**.

The **environment** value is used, because the narrower scope wins.

</details>

**Q106. [Code] Request A returns a post. Request B must fetch that post's author. Show how to chain them in Postman.**

<details>
<summary>Answer</summary>

Request A (`{{baseUrl}}/posts/1`), post-response script:

```javascript
const post = pm.response.json();
pm.environment.set("userId", post.userId);
```

Request B URL:

```
{{baseUrl}}/users/{{userId}}
```

Run them in order with the Collection Runner.

</details>

**Q107. [Scenario] A teammate runs your collection and every request fails with `Invalid URL`. `{{baseUrl}}` appears in red. What are the likely causes?**

<details>
<summary>Answer</summary>

1. No environment is selected in the top-right dropdown ("No environment").
2. The variable name has a typo or different case (`{{baseURL}}` vs `{{baseUrl}}`, which are different names).
3. The value is only in **your** current value, and the shared initial value is empty, so on their machine the variable has no value.

</details>

---

## MCP Server Testing

**★ Good to know** – A newer topic; good for standing out, less often asked.

**Q108. [Concept] In MCP, what are the host, client and server? What are tools, resources and prompts?**

<details>
<summary>Answer</summary>

- **Host:** the AI application (e.g. a chat app or IDE).
- **Client:** runs inside the host and keeps one connection to a server.
- **Server:** exposes capabilities to the client.

A server can expose:

- **Tools:** functions the model can call (e.g. `add`, `search_tickets`).
- **Resources:** readable data identified by a URI (e.g. `greeting://Ana`, a file).
- **Prompts:** reusable prompt templates.

Messages are JSON-RPC 2.0, sent over stdio or streamable HTTP.

</details>

**Q109. [Concept] Describe the layers for testing an MCP server. Where should most tests sit?**

<details>
<summary>Answer</summary>

1. **Tool logic:** unit-test the plain Python functions.
2. **Contract:** `tools/list` returns the expected names, descriptions and input schemas.
3. **Protocol and errors:** calls return the right content; failures return `isError: true`; the server survives them.
4. **Resources and prompts.**
5. **End-to-end:** a real subprocess over stdio, or HTTP.

Most tests belong in layers 1–4: they are fast and run in memory. Keep a few end-to-end tests.

</details>

**Q110. [Code] Write an in-memory test proving that `divide(1, 0)` returns an error result and that the server still works afterwards.**

<details>
<summary>Answer</summary>

```python
import pytest
from mcp.shared.memory import create_connected_server_and_client_session as connect
from calc_server import mcp


@pytest.mark.asyncio
async def test_divide_error_keeps_server_alive():
    async with connect(mcp._mcp_server) as session:
        bad = await session.call_tool("divide", {"a": 1, "b": 0})
        assert bad.isError is True
        good = await session.call_tool("add", {"a": 2, "b": 2})
        assert good.content[0].text == "4"
```

The session is opened inside the test. Yielding an open session from a fixture causes "exit cancel scope in a different task" errors.

</details>

**Q111. [Scenario] You add `print("debug:", a, b)` inside a tool of a stdio MCP server, and clients start failing with parse errors. Why?**

<details>
<summary>Answer</summary>

In the stdio transport, **stdout carries the JSON-RPC messages**. The print inserts non-JSON text into the protocol stream and corrupts it. Log to **stderr** instead (`print(..., file=sys.stderr)` or the `logging` module).

</details>
