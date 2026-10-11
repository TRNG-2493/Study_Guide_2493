# Status Code Validation

## Learning Objectives

By the end of this lesson you will be able to:

- Explain what an HTTP status code is, how it is built (three digits, five classes), and why it is the first assertion in every API test.
- Explain the purpose, a typical trigger, a tester's check, and a common misuse of each code testers must know: `200`, `201`, `202`, `204`, `301`, `302`, `304`, `400`, `401`, `403`, `404`, `405`, `409`, `415`, `422`, `429`, `500`, `502`, `503`, `504`.
- Distinguish **positive** tests from **negative** tests and design a negative-test table for any endpoint.
- Choose between asserting an exact code, a short list of acceptable codes, and a whole class, and justify the choice.
- Explain the difference between `response.ok`, `response.status_code`, and `response.raise_for_status()`, and say when each belongs in test code.
- Validate the status code **and** the body together, including a documented error-response contract.
- Handle `429 Too Many Requests` and the `Retry-After` header without making tests flaky.
- Write helpful assertion messages and a reusable `assert_status` helper that reports method, URL, code, and body when a test fails.
- Recognise and avoid the common anti-patterns, above all "assert only `200`".

---

## Why This Matters

This week's epic is a pipeline-ready API test framework for Project 2, and a pipeline is only worth running if its failures are trustworthy and quick to read. The status code is where trust begins: before you inspect a single body field, it tells you whether the server believes the request succeeded, blames you, or blames itself. A test that skips or fumbles this check is built on sand.

Here are three real-world situations that show how much depends on one three-digit number.

**Situation 1: the polite lie.** A team ships a registration endpoint. When a user submits an invalid email, the server returns `200 OK` with the body `{"success": false, "error": "invalid email"}`. The mobile app was written to check the status code only, so it shows "Welcome!" to a user who was never created. Support tickets pile up. A test that asserted `status_code == 422` (or `400`) for invalid input would have failed on day one. A test that asserted only `200` would have passed and blessed the bug.

**Situation 2: the crash that looks like a miss.** `GET /orders/abc` makes the server fail to convert `abc` to a number and return `500`. A `500` means "I broke"; the right answer is `400` or `404`. Only an exact-code assertion reveals it.

**Situation 3: the open door.** A protected admin endpoint is supposed to return `401` to anonymous callers and `403` to normal users. After a refactor it returns `200` to everyone. Only a test that deliberately calls it without credentials, and asserts `401`, will notice. This is a security defect, and the entire proof of it is one status code.

On Monday you met HTTP messages and headers; today you learn to assert the status line correctly in Python, and later this week your pipeline will run these checks on every commit, so the quality of your assertion messages decides whether a red build takes two minutes or two hours to understand.

A note on the examples: every snippet was run against a small local mock server that returns exactly the codes under discussion (outputs labelled **mock server output**). Output from public services such as JSONPlaceholder or httpbin is labelled **representative**: typical, not guaranteed byte for byte.

For all examples, `client` is a pytest fixture that wraps a `requests.Session` and prepends a base URL (built in the fixtures lesson, also today).

---

## The Concept

### 1. What Is a Status Code?

Every HTTP response begins with a **status line**:

```http
HTTP/1.1 404 Not Found
```

There are three parts: the protocol version (`HTTP/1.1`), the **status code** (`404`), and the **reason phrase** (`Not Found`). The status code is a three-digit integer. The reason phrase is a human-readable label. In HTTP/2 and HTTP/3 the reason phrase is not even transmitted; libraries such as `requests` fill it in from a lookup table or from what the server sent. That is the first rule of this lesson:

> **Assert the number, never the text.** The code is the contract. The reason phrase is decoration that can differ between servers.

A status code answers one question: **"How did the server interpret and handle my request?"** Specifically, it tells the client whether the request succeeded, whether the client should do something else (follow a redirect, log in, wait), or whether the request failed and, crucially, whose fault the failure is.

#### Why it exists

HTTP was designed so that machines can talk to machines. A browser, a mobile app, a proxy, a cache, a search-engine crawler, and your test script all need to decide quickly what to do next. They cannot read English error messages reliably, but they can compare an integer. If the code is `200`, use the body. If it is `301`, go to the new address. If it is `401`, ask the user to log in. If it is `503`, wait and retry. The code is the machine-readable summary that drives all of this behaviour.

#### How a tester sees it

In `requests`, the status code lives on the response object:

```python
response = client.get("/posts/1")
print(response.status_code)   # 200  (an int)
print(response.reason)        # 'OK' (a str; informational only)
```

Mock server output:

```text
200
OK
```

`status_code` is an `int`. Compare it with an `int`: `== 200`, never `== "200"`. A string never equals an integer in Python, so `200 == "200"` is `False`, and a test written that way fails for the wrong reason.

### 2. The Five Classes

The first digit is the **class**. It tells you the category before you even look at the other two digits. This is the most useful thing to memorise, because a client that does not recognise a specific code is required to treat it as the `x00` code of its class (an unknown `418` is handled like `400`).

| Class | Name | Plain meaning | Who is "at fault"? |
|-------|------|---------------|--------------------|
| `1xx` | Informational | "Got it, keep going." An interim message; the final response follows. | Nobody |
| `2xx` | Success | "Your request was received, understood, and accepted." | Nobody |
| `3xx` | Redirection | "You need to take another step, usually go to a different URL." | Nobody (usually) |
| `4xx` | Client error | "The request is wrong, so repeating it unchanged will not help." | The client |
| `5xx` | Server error | "The request looks valid, but I failed to handle it." | The server |

Memory aid: **2 = good, 3 = go elsewhere, 4 = you messed up, 5 = I messed up.**

#### 1xx Informational

You will almost never assert a `1xx` code, because libraries hide these interim responses. Know two: `100 Continue` ("go ahead and send the body", after `Expect: 100-continue`) and `101 Switching Protocols` (an upgrade such as HTTP to WebSocket). `2xx` means success (the specific code says *how*), `3xx` means the client must take another step (section 3.6 shows how to test it), and `4xx` is the heart of negative testing.

#### 5xx Server Error

The server failed to complete a request that appeared valid. Two key points for testers:

1. A `5xx` in response to **your bad input** is almost always a defect. A well-built server validates input and answers `4xx`. A `500` usually means an unhandled exception.
2. A `5xx` caused by **real infrastructure trouble** (a database outage, a deploy in progress) is not a defect in the endpoint's logic, but it is still something a pipeline should report loudly and, for certain codes, retry (see section 9).

### 3. The Codes Testers Must Know

For each code below you will find what it means, a typical trigger, what to test, and a common misuse. The examples use the local mock server; adapt the path to your own API.

#### 3.1 `200 OK`

**Meaning:** The request succeeded and the response carries the result.

**Typical use:** `GET` (the body is the resource), `PUT` and `PATCH` (the body is the updated resource), and sometimes `DELETE` or `POST` when the API chooses to return a body.

**What to test:** The code, plus the body's shape and values. A `200` proves only that the server *claims* success.

**Common misuse:** Returning `200` for everything, including errors, with the real outcome buried in the body (`{"success": false}`). This is the polite lie from Situation 1. It breaks every client that trusts the status line, and it is a defect worth reporting.

```python
def test_get_existing_post_returns_200(client):
    response = client.get("/posts/1")
    assert response.status_code == 200
    assert response.json()["id"] == 1
```

#### 3.2 `201 Created`

**Meaning:** The request succeeded **and a new resource was created**.

**Typical use:** `POST` that creates a record.

**What to test:** The code; a `Location` header pointing to the new resource; a body that contains the new `id`; and (where the API actually persists data) that a follow-up `GET` on the `Location` returns the resource.

**Common misuse:** Returning `200` for a creation (acceptable to some teams, but inconsistent with the specification), or returning `201` without a `Location` or id, leaving the client unable to find what was created.

```python
def test_create_post_returns_201_and_location(client):
    response = client.post(
        "/posts",
        json={"title": "New", "body": "b"},
        headers={"Authorization": "Bearer user-token"},
    )
    assert response.status_code == 201
    new_id = response.json()["id"]
    assert response.headers["Location"] == f"/posts/{new_id}"
    # prove it really exists:
    assert client.get(response.headers["Location"]).status_code == 200
```

Mock server output: the test passes (the server answers `201` with `Location: /posts/2`, and a follow-up `GET` returns `200`).

#### 3.3 `202 Accepted`

**Meaning:** The request was accepted for processing, but the processing is **not finished**. Think of dropping a letter in a post box: it has been accepted; it has not been delivered.

**Typical use:** Long-running work such as report generation, video encoding, bulk import, or sending email. The server usually returns a `Location` header (or a body field) pointing to a **status resource** the client can poll.

**What to test:** The `202`; the presence of the status URL; and that polling eventually reaches a terminal state such as `done` or `failed`.

**Common misuse:** Returning `200` with `{"state": "queued"}` (ambiguous), or returning `202` and never offering a way to learn the result.

```python
import time
import pytest

def test_report_is_accepted_then_completes(client):
    response = client.post("/reports", json={"type": "monthly"})
    assert response.status_code == 202
    status_url = response.headers["Location"]

    for _ in range(10):                      # poll up to 10 times
        state = client.get(status_url).json()["state"]
        if state == "done":
            break
        time.sleep(0.05)                     # short pause between polls
    else:
        pytest.fail("report did not reach 'done' in time")
```

Line by line: the test asserts `202` (immediate success is not expected), reads the `Location` header to learn where to poll, then polls up to ten times. The `for ... else` idiom runs the `else` branch only if the loop ended without `break`, so a job that never finishes triggers `pytest.fail`. Always cap the attempts so a stuck job cannot hang the pipeline.

Mock server output: the mock reports `running` twice and then `done`, so the test passes on the third poll.

#### 3.4 `204 No Content`

**Meaning:** The request succeeded and there is deliberately **no body**.

**Typical use:** `DELETE` (nothing left to show), and `PUT` or `PATCH` when the API chooses not to echo the resource.

**What to test:** The `204`, and that the body is actually empty. A `204` with a body violates the specification.

**The classic trap:** `response.json()` on an empty body raises an exception. If you write a shared helper that always calls `.json()`, every `DELETE` test will crash:

```python
import pytest
import requests

def test_delete_returns_204_with_empty_body(client):
    response = client.delete("/posts/1", headers={"Authorization": "Bearer user-token"})
    assert response.status_code == 204
    assert response.text == ""                 # no body at all
    with pytest.raises(requests.exceptions.JSONDecodeError):
        response.json()                        # proves .json() cannot be used here
```

Mock server output: the test passes. The last two lines document the trap on purpose: you should know that `.json()` is the wrong tool for a `204`.

#### 3.5 `3xx` Redirection overview

A `3xx` response almost always comes with a `Location` header holding the new URL. The most important members are below.

- `301` Moved Permanently: new permanent URL. `302` Found: temporary redirect.
- `307` Temporary Redirect and `308` Permanent Redirect: like `302` and `301`, but the method and body **must not change**.
- `304` Not Modified: not a redirect; "your cached copy is still valid".

Why `307` and `308` exist: historically, many clients turned a redirected `POST` into a `GET`, which was ambiguous. The newer codes make the intent explicit.

#### 3.6 `301` and `302`: Testing the Redirect Itself

By default `requests` follows redirects for you. The final response is a `200` and the `301` disappears from view. To assert the redirect, tell `requests` not to follow it:

```python
def test_old_path_redirects_permanently(client):
    response = client.get("/old", allow_redirects=False)
    assert response.status_code == 301
    assert response.headers["Location"] == "/new"


def test_following_the_redirect_ends_on_200(client):
    response = client.get("/old")                  # follows redirects (default)
    assert response.status_code == 200
    assert response.history[0].status_code == 301  # the hop that was followed
    assert response.json() == {"page": "new"}
```

`allow_redirects=False` makes the first response the one you receive. `response.history` is a list of the intermediate redirect responses that `requests` followed, oldest first. It is empty when there were no redirects. Test both views: "does the redirect exist and is it the right kind?" and "does following it land somewhere valid?".

Choosing correctly matters: browsers and search engines cache `301` aggressively, so a `301` used for something temporary can trap users on the old target for months.

#### 3.7 `304 Not Modified`

**Meaning:** The client already has the current version. This answers a **conditional request**. When the client first fetches a resource, the server returns an `ETag` header (a version fingerprint). On the next request the client sends `If-None-Match: <that ETag>`. If nothing changed, the server replies `304` with **no body**, saving bandwidth. You met `ETag` and `If-None-Match` in Monday's lesson on headers.

```python
def test_conditional_get_returns_304(client):
    first = client.get("/cached")
    assert first.status_code == 200
    etag = first.headers["ETag"]

    second = client.get("/cached", headers={"If-None-Match": etag})
    assert second.status_code == 304
    assert second.content == b""            # 304 has no body
```

Note that `requests` does not cache anything by itself, so `304` appears only when your test sends the conditional header explicitly. A frequent defect is an API that ignores `If-None-Match` and resends the full body (`200`).

#### 3.8 `400 Bad Request`

**Meaning:** The server cannot or will not process the request because of something that looks like a client error: malformed syntax, an invalid parameter, or a body that cannot be parsed.

**Typical triggers:** Broken JSON, a wrong data type, a malformed id (`/posts/abc`), a missing required query parameter.

**What to test:** The code and an error body that explains *what* was wrong.

**Common misuse:** Using `400` as a catch-all for every failure, including authentication and missing resources. That removes the information that distinguishes problems.

```python
def test_malformed_json_returns_400(client):
    response = client.post(
        "/posts",
        data='{"title": "x"',                     # missing closing brace
        headers={"Authorization": "Bearer user-token",
                 "Content-Type": "application/json"},
    )
    assert response.status_code == 400
```

Note the use of `data=` (raw string) instead of `json=`. The `json=` argument serialises a valid Python object, so it can never produce broken JSON. To send broken JSON on purpose you must send raw text and set `Content-Type` yourself.

#### 3.9 `401 Unauthorized` versus `403 Forbidden`

The names are the biggest trap in the HTTP vocabulary. Despite its name, `401 Unauthorized` really means **unauthenticated**: "I do not know who you are" (no credentials, or invalid or expired ones). `403 Forbidden` means **unauthorised in the everyday sense**: "I know who you are, and you are not allowed to do this."

| Question the server asks | Answer | Code |
|--------------------------|--------|------|
| Did the request carry valid credentials? | No | `401` |
| Valid credentials, but is this identity permitted? | No | `403` |

Memory aid: **401 = "Who are you?"**, **403 = "I know who you are, and no."** A `401` should include a `WWW-Authenticate` header telling the client how to authenticate (for example `Bearer realm="api"`).

The correct way to test the pair is to use **several** different callers against the same protected endpoint. One caller is not enough, because you cannot tell which of the two failure modes you hit:

```python
USER = {"Authorization": "Bearer user-token"}     # valid, but a normal user
ADMIN = {"Authorization": "Bearer admin-token"}   # valid admin


def test_admin_endpoint_access_matrix(client):
    # 1. No credentials: not authenticated
    anonymous = client.get("/admin/stats")
    assert anonymous.status_code == 401
    assert anonymous.headers["WWW-Authenticate"].startswith("Bearer")

    # 2. Invalid credentials: still not authenticated
    bad_token = client.get("/admin/stats", headers={"Authorization": "Bearer nope"})
    assert bad_token.status_code == 401

    # 3. Valid but insufficient role: authenticated, forbidden
    normal_user = client.get("/admin/stats", headers=USER)
    assert normal_user.status_code == 403

    # 4. Correct role: success
    admin = client.get("/admin/stats", headers=ADMIN)
    assert admin.status_code == 200
```

Line by line: step 1 sends no `Authorization` header (`401`, plus a `WWW-Authenticate` check). Step 2 sends an unrecognised token, still an authentication failure. Step 3 sends a genuine user token that lacks the role (`403`). Step 4 is the positive control; without it, an endpoint that rejects everyone would pass steps 1 to 3.

Common defects: `403` for anonymous callers (clients cannot tell they should log in), `401` for a logged-in user lacking a role (login loops), and `200` with no credentials (a severe security hole). Token mechanics are in the headers and authentication lesson (also today).

#### 3.10 `404 Not Found` versus `400 Bad Request`

Both appear when a request involves a bad identifier, so people mix them up. The distinction:

- **`404`**: the request is well-formed, but **no resource exists** at that address. `GET /posts/99999` (a valid integer that matches nothing).
- **`400`**: the request is **malformed** in a way that makes it impossible to even look. `GET /posts/abc` (not an integer, so no lookup can happen).

```python
def test_missing_resource_is_404_malformed_is_400(client):
    missing = client.get("/posts/99999")   # valid shape, does not exist
    assert missing.status_code == 404

    malformed = client.get("/posts/abc")   # invalid shape
    assert malformed.status_code == 400
```

Two nuances. Many real APIs return `404` for both, so the specification must pick one and your tests must assert the documented choice. And `404` is sometimes deliberately returned instead of `403` to hide that a resource exists (another tenant's order); that is legitimate if documented.

The failure to hunt for is `500` where `400` or `404` belongs: an unhandled exception on odd input. Any test that feeds odd identifiers and finds a `5xx` has found a defect.

#### 3.11 `405 Method Not Allowed`

**Meaning:** The path exists, but not for this HTTP method. A `405` response must include an `Allow` header listing the methods that *are* permitted.

```python
def test_delete_on_collection_is_405_with_allow(client):
    response = client.delete("/posts")           # deleting the whole collection
    assert response.status_code == 405
    assert response.headers["Allow"] == "GET, POST"
```

Mock server output: passes; the server answered `405` with `Allow: GET, POST`.

Common misuse: returning `404` for a wrong method, which wrongly suggests the path itself does not exist. Some public sandbox APIs do this; if your target API does, report it or record it as a documented deviation rather than quietly accepting it.

#### 3.12 `409 Conflict`

**Meaning:** The request is valid on its own but conflicts with the **current state** of the resource.

**Typical triggers:** Creating a record with a value that must be unique (duplicate email or title), editing a resource that someone else changed (version conflict), deleting a resource that others depend on.

```python
def test_duplicate_title_returns_409(client):
    # "First" already exists in the mock server's data
    response = client.post(
        "/posts",
        json={"title": "First"},
        headers={"Authorization": "Bearer user-token"},
    )
    assert response.status_code == 409
```

The difference from `400`/`422`: those say the **data itself** is wrong. `409` says the data is fine but **the situation** forbids it. The same payload could succeed on a different day.

#### 3.13 `415 Unsupported Media Type`

**Meaning:** The server cannot handle the body's `Content-Type`. Send form data or plain text to a JSON-only endpoint and you get this.

```python
def test_wrong_content_type_returns_415(client):
    response = client.post(
        "/posts",
        data="title=x",
        headers={"Authorization": "Bearer user-token",
                 "Content-Type": "text/plain"},
    )
    assert response.status_code == 415
```

The sibling `406 Not Acceptable` is the mirror image: it concerns the `Accept` header (what the client wants back), whereas `415` concerns `Content-Type` (what the client sent). A handy way to remember: **415 is about what you gave, 406 is about what you asked for.**

#### 3.14 `422 Unprocessable Content`

**Meaning:** The request is syntactically valid (the JSON parsed fine) but **semantically invalid**: a required field is missing, an age is negative, a date is in the wrong format. (The older name, still widespread, is "Unprocessable Entity".)

**`400` versus `422`:** Both signal bad input. A common convention is that `400` means "I could not parse it" and `422` means "I parsed it, but it breaks the rules". Not every API follows this. Some use `400` for everything. The rule for testers: read the API's specification, assert what it promises, and keep the assertion consistent across tests.

```python
def test_missing_required_field_returns_422(client):
    response = client.post(
        "/posts",
        json={"body": "no title here"},
        headers={"Authorization": "Bearer user-token"},
    )
    assert response.status_code == 422
```

`422` pairs naturally with a body that lists *which* fields failed, which we test in section 7.4.

#### 3.15 `429 Too Many Requests`

**Meaning:** The client has sent too many requests in a given period (rate limiting). The response often includes `Retry-After`, telling the client how long to wait, either as a number of seconds (`Retry-After: 120`) or as an HTTP date (`Retry-After: Wed, 21 Oct 2026 07:28:00 GMT`). Section 9 covers this in depth, since it is where many automated suites become flaky.

#### 3.16 `500 Internal Server Error`

**Meaning:** A generic "the server failed" for an unexpected condition. In practice, an unhandled exception.

**Tester's reflex:** If your *test input* provoked a `500`, you found a bug. Report it, even if the "right" answer is debatable, because no input should be able to crash a server.

#### 3.17 `502 Bad Gateway`, `503 Service Unavailable`, `504 Gateway Timeout`

These three usually come from the infrastructure around the application: load balancers, reverse proxies, and API gateways.

- `502`: a gateway got an invalid reply from the application (crash, restart). Retrying briefly often helps.
- `503`: overloaded, deploying, or in maintenance; may carry `Retry-After`. Retry after the wait.
- `504`: the gateway timed out waiting for the application (slow database or upstream). Investigate.

Distinguish them from `500`: with `500` the application itself reported failure; with `502`/`503`/`504` the layer in front of it reports a problem reaching or waiting for it. In a pipeline, a burst of `502`/`503` right after a deploy is usually "the environment is still starting", while a steady `500` on one endpoint is "the code is broken". Telling these apart saves hours.

### 4. Positive Versus Negative Testing

#### What they are

- A **positive test** (also called a happy-path test) sends a valid request and asserts that the API succeeds and returns the right data. It answers: "does the feature work when used correctly?"
- A **negative test** sends an invalid, unauthorised, malformed, or otherwise problematic request and asserts that the API **fails correctly**: the right `4xx` code, an informative error body, no crash, and no side effects. It answers: "does the feature protect itself and guide the user when used incorrectly?"

#### Why both matter

Real users and attackers do not stay on the happy path: users mistype, apps send stale tokens, scripts hammer endpoints. Happy-path-only testing re-checks what developers already tried by hand, while defects hide in failure paths.

The status code is the main tool of negative testing. A well-behaved failure is characterised by **a precise `4xx` code**. A badly behaved one is a `200` with an error body, a `5xx` crash, or (worst) a `2xx` that actually performed the forbidden action.

#### How to design negative tests: a repeatable recipe

For each endpoint, walk down this checklist and write one test per applicable row:

1. **Authentication:** no credentials, malformed credentials, expired credentials. Expect `401`.
2. **Authorisation:** valid credentials with too few rights; another user's resource. Expect `403` (or a documented `404`).
3. **Existence:** an id that does not exist. Expect `404`.
4. **Malformed input:** broken JSON, wrong types, malformed ids. Expect `400`.
5. **Semantic validation:** missing required fields, out-of-range values, bad formats. Expect `422` (or `400`, per spec).
6. **State conflicts:** duplicates, stale versions. Expect `409`.
7. **Content negotiation:** wrong `Content-Type`; unsupported `Accept`. Expect `415`/`406`.
8. **Method:** unsupported method on the path. Expect `405`.
9. **Rate:** bursts. Expect `429` where limiting exists.
10. **Safety net:** whatever you send, never `5xx`.

#### Writing the whole table as one test

Writing nine near-identical functions is tedious and hard to maintain. `pytest.mark.parametrize` turns a table into data and runs one test body per row. (The lesson on fixtures and parametrization, also today, explains it in depth; here is a preview of how directly it maps onto the table.) The `assert_error_response` helper is built in section 7.4.

```python
import pytest
from assertions import assert_error_response

USER = {"Authorization": "Bearer user-token"}

NEGATIVE_CASES = [
    pytest.param("GET", "/posts/99999", {}, 404, "not_found", id="missing-post"),
    pytest.param("GET", "/posts/abc", {}, 400, "invalid_id", id="malformed-id"),
    pytest.param("GET", "/admin/stats", {"headers": USER}, 403, "forbidden", id="wrong-role"),
    pytest.param("GET", "/admin/stats", {}, 401, "unauthenticated", id="no-token"),
    pytest.param("POST", "/posts", {"headers": USER, "json": {"body": "x"}},
                 422, "validation_failed", id="no-title"),
    pytest.param("POST", "/posts", {"headers": USER, "json": {"title": "First"}},
                 409, "duplicate", id="duplicate"),
    pytest.param("POST", "/posts",
                 {"headers": {**USER, "Content-Type": "text/plain"}, "data": "x"},
                 415, "unsupported_media_type", id="wrong-type"),
    pytest.param("POST", "/posts",
                 {"headers": {**USER, "Content-Type": "application/json"}, "data": "{oops"},
                 400, "invalid_json", id="bad-json"),
    pytest.param("DELETE", "/posts", {}, 405, "method_not_allowed", id="wrong-method"),
]


@pytest.mark.parametrize("method,path,kwargs,status,code", NEGATIVE_CASES)
def test_negative_matrix(client, method, path, kwargs, status, code):
    response = client.request(method, path, **kwargs)
    assert_error_response(response, status, code)
```

Mock server output: all nine cases passed, each reported under its readable id (for example `test_negative_matrix[wrong-role]`). Note that this table has no positive-control row; always add one (a valid request expecting `201`) so that "everything is rejected" cannot masquerade as "negative tests pass".

Each `pytest.param` is one table row; `id=` gives it a readable name; `**kwargs` expands into the request; `{**USER, "Content-Type": "text/plain"}` builds a new dictionary without altering `USER`. Adding a scenario is now one line, not a new function.

### 5. Exact Codes, Lists, and Ranges

You have three ways to assert a status code. Choosing well keeps tests strict enough to catch regressions and flexible enough to avoid pointless failures.

#### 5.1 Exact code (the default)

```python
assert response.status_code == 201
```

Use this whenever the specification names one code. If a refactor changes `201` to `200`, you want the test to fail, because clients may depend on the difference.

#### 5.2 One of several acceptable codes

```python
assert response.status_code in (200, 204)
```

Use this **only** when the specification truly allows more than one, for example a `DELETE` that may return `200` with a confirmation body or `204` with none. Do not use it to paper over uncertainty about what the API does. Find out and write the exact value. A loose list hides regressions.

#### 5.3 A whole class

```python
assert 200 <= response.status_code < 300, "expected a 2xx success"
assert 400 <= response.status_code < 500, "expected a 4xx client error"
assert response.status_code // 100 == 4    # integer-division version
```

Class checks fit only a few situations: **safety-net assertions** in broad negative tests ("whatever I send, never `5xx`": `assert response.status_code < 500`), cleanup code, and smoke tests (any `2xx`).

Do **not** use `400 <= code < 500` as the main assertion of a negative test. A missing resource returning `401`, `405`, or `429` is a different failure, and a class check would hide it.

A useful pattern is a precise test for each designed case plus a class check as a safety net for odd inputs:

```python
import pytest

@pytest.mark.parametrize("bad_id", ["abc", "-1", "0", "1.5", "%00", "9" * 40])
def test_odd_ids_never_crash_the_server(client, bad_id):
    response = client.get(f"/posts/{bad_id}")
    assert response.status_code < 500, f"{bad_id!r}: {response.status_code} {response.text[:200]}"
```

The safety net does not decide whether each odd id is `400` or `404`; it only insists on "no crash".

### 6. `response.ok`, `status_code`, and `raise_for_status()`

`requests` gives you three related tools. Mixing them up is a very common beginner mistake.

#### 6.1 `response.status_code`

The raw integer. It is precise and never raises an exception. It is the right tool for **assertions** in tests, because you want to say exactly which code you expect.

#### 6.2 `response.ok`

A boolean that is `True` for any status **below 400**. That means `200`, `201`, `204`, **and `301`, `302`, and `304`** are all "ok". Try it:

```python
r = client.get("/status/302", allow_redirects=False)
print(r.status_code, r.ok)      # 302 True   <- a redirect is "ok"

r = client.get("/status/404")
print(r.status_code, r.ok)      # 404 False
```

Mock server output:

```text
302 True
404 False
```

`ok` is **too loose** for test assertions: `assert response.ok` passes for a `301` when you expected `200`, and fails with the unhelpful `assert False`. Reserve it for quick "non-error?" logic in helpers.

#### 6.3 `response.raise_for_status()`

A method that does nothing for codes below 400, and **raises** `requests.HTTPError` for any `4xx` or `5xx`:

```python
import pytest
import requests

r = client.get("/status/404")
with pytest.raises(requests.HTTPError) as excinfo:
    r.raise_for_status()
print(excinfo.value)

r = client.get("/status/500")
with pytest.raises(requests.HTTPError) as excinfo:
    r.raise_for_status()
print(excinfo.value)
```

Mock server output:

```text
404 Client Error: Not Found for url: http://127.0.0.1:37267/status/404
500 Server Error: Internal Server Error for url: http://127.0.0.1:37267/status/500
```

(The port changes on each run.) `raise_for_status` suits **setup, fixtures, and production code**, where any error should stop everything and the message already names the code and URL. It is **not** a primary assertion: when you *expect* a `404` an exception is the wrong shape, and when you expect `201` it will not notice a `200` (both are below 400). Rule of thumb: **setup raises, the test asserts**. In a fixture, call `response.raise_for_status()` after the creating `POST`; then a broken setup shows as a pytest *error* (environment or design problem), not a *failure* (feature problem).

### 7. Validating Status and Body Together

A status code alone is a promise. The body is the proof. Real defects often live in the gap between the two.

#### 7.2 Positive example: code plus content

```python
def test_get_post_returns_correct_resource(client):
    response = client.get("/posts/1")
    assert response.status_code == 200
    assert response.headers["Content-Type"].startswith("application/json")
    body = response.json()
    assert body["id"] == 1
    assert isinstance(body["title"], str) and body["title"]
```

Line by line: the first assertion proves the server claimed success; the `Content-Type` check makes `.json()` safe (`startswith`, because the real value is usually `application/json; charset=utf-8`); the last lines check the body is the resource we asked for.

Order matters: check the status **first**. If you call `.json()` before asserting the code and the server returned an HTML `502` page, you get a confusing `JSONDecodeError` instead of "expected 200 but got 502".

#### 7.3 Catching the polite lie

This is how to catch the "200 with an error" defect from Situation 1:

```python
def test_response_is_not_a_disguised_failure(client):
    response = client.get("/fake-success")
    assert response.status_code == 200
    body = response.json()
    assert body.get("success") is not False, f"200 but body says failure: {body}"
```

Mock server output (this test fails, correctly, against the deliberately defective endpoint):

```text
E       AssertionError: 200 but body says failure: {'success': False, 'error': 'title required'}
E       assert False is not False
```

The failure message includes the whole body, so the reviewer sees at once what went wrong. The right fix is on the server (return `422`), and the test should then be tightened to expect that.

#### 7.4 The error-response contract

Well-designed APIs return errors in a **consistent, documented shape**, called an *error-response contract*. For example:

```json
{
  "error": {
    "code": "validation_failed",
    "message": "invalid fields",
    "details": [{"field": "title", "problem": "required"}]
  }
}
```

The status code gives the category; `error.code` gives a stable machine-readable reason; `message` is for humans; `details` lists field-level problems. Contract tests should check:

Contract tests should check:

1. The status code is the documented one.
2. The `Content-Type` is JSON (not an HTML page from a proxy or framework).
3. The `error` object exists with `code` and a non-empty `message`.
4. The `code` matches the documented value.
5. For validation errors, `details` identifies the offending field.
6. The body does **not** leak internals (stack traces, SQL fragments, file paths, framework versions).

Capture steps 1 to 4 in a helper:

```python
# api/assertions.py  (excerpt)
def assert_error_response(response, status, code):
    """Status AND error-contract check."""
    assert_status(response, status)
    assert response.headers.get("Content-Type", "").startswith("application/json"), \
        f"error body is not JSON: {response.headers.get('Content-Type')}"
    err = response.json().get("error")
    assert err is not None, f"missing 'error' object: {response.text[:200]}"
    assert err.get("code") == code, f"error.code was {err.get('code')!r}, expected {code!r}"
    assert err.get("message"), "error.message must be non-empty"
    return err
```

Line by line: it reuses `assert_status` (section 10) for the code, verifies the response is JSON before calling `.json()`, uses `.get("error")` so an absent key becomes a readable failure instead of a `KeyError`, and prints values with `!r` so `None` versus `'None'` is visible. It returns `err` so callers can assert more (step 5).

Use it like this:

```python
def test_validation_error_names_the_field(client):
    r = client.post("/posts", json={"body": "x"},
                    headers={"Authorization": "Bearer user-token"})
    err = assert_error_response(r, 422, "validation_failed")
    assert err["details"] == [{"field": "title", "problem": "required"}]
```

Mock server output (the returned `err` dictionary):

```text
{'code': 'validation_failed', 'message': 'invalid fields', 'details': [{'field': 'title', 'problem': 'required'}]}
```

An error that merely says "something went wrong" and gives no field names is a usability defect. Deeper structural checks of response bodies (schemas, nested objects, types) are the subject of the lesson on JSON response validation (also today).

### 8. Idempotency: Repeating `PUT` and `DELETE`

#### What idempotent means

An operation is **idempotent** if performing it several times has the **same effect on the server's state** as performing it once. Note the wording: it is about the *resulting state*, not the *response*. This matters when clients retry after a timeout without knowing whether the first attempt arrived. Retrying an idempotent operation is safe; retrying a non-idempotent one may duplicate work. You met these method properties on Monday.

`GET`, `PUT` ("make the resource exactly this"), and `DELETE` (gone stays gone) are idempotent. `POST` normally is not (each call creates another resource), and `PATCH` depends on the change (`title = X` is idempotent; `views + 1` is not).

#### Repeated `PUT`

Sending the same `PUT` twice leaves the same state and normally returns the same success code both times:

```python
def test_put_twice_gives_same_state_and_code(client):
    first = client.put("/posts/1", json={"title": "Same"})
    second = client.put("/posts/1", json={"title": "Same"})
    assert first.status_code == second.status_code == 200
    assert first.json() == second.json()
```

A `PUT` on a resource that does not exist may validly return `201` (created) or `404` (no creation by `PUT`); check the specification.

#### Repeated `DELETE`: the surprise

Here beginners are often confused. `DELETE` is idempotent in **state** (the resource is gone after one call or ten), but the **status code** is allowed to differ:

- First `DELETE`: `204` (or `200`).
- Second `DELETE`: `404`, because there is nothing left to delete.

Some APIs return `204` on every call; others return `404` the second time. Both are legitimate. `500`, or a second call that changes other data, is not.

```python
def test_delete_twice(client):
    auth = {"Authorization": "Bearer user-token"}
    first = client.delete("/posts/1", headers=auth)
    assert first.status_code == 204

    second = client.delete("/posts/1", headers=auth)
    assert second.status_code == 404           # this API's documented behaviour

    # and the state is the same either way: the resource is gone
    assert client.get("/posts/1").status_code == 404
```

Mock server output: passes. Pick the code the specification documents and say so in a comment, so nobody "fixes" the test to `204` later. The final `GET` verifies what idempotency actually promises: the resulting state. Also check that deleting `/posts/1` twice does not remove `/posts/2`.

### 9. Rate Limiting: `429` and `Retry-After`

#### What and why

A **rate limit** caps how many requests a client may send per time window, for example 100 per minute. APIs do this to protect themselves from abuse and overload and to share capacity fairly. When you exceed it, the server answers `429 Too Many Requests`, usually with a `Retry-After` header.

For testers rate limiting matters twice: it is something to **test** (does the limit exist, trigger at the documented threshold, and answer `429` with `Retry-After`?), and something that **breaks your suite** (parallel pipeline jobs on a shared environment can trip the limit and cause random `429` failures).

#### Reading `Retry-After`

`Retry-After` has two legal forms:

1. A non-negative integer: seconds to wait (`Retry-After: 120`).
2. An HTTP date: the moment after which to retry (`Retry-After: Wed, 21 Oct 2026 07:28:00 GMT`).

A robust helper handles both:

```python
import datetime
import email.utils


def retry_after_seconds(response, default=1.0):
    """Return how many seconds the server asked us to wait."""
    value = response.headers.get("Retry-After")
    if value is None:
        return default
    if value.isdigit():
        return int(value)
    when = email.utils.parsedate_to_datetime(value)
    now = datetime.datetime.now(datetime.timezone.utc)
    return max(0.0, (when - now).total_seconds())
```

Line by line: `response.headers.get("Retry-After")` returns `None` when absent (and `requests` treats the header name case-insensitively). If absent, we fall back to a safe default. If the value consists only of digits it is the seconds form. Otherwise it is a date; `email.utils.parsedate_to_datetime` is the standard-library parser for HTTP dates. We subtract the current time and use `max(0.0, ...)` so a date already in the past never yields a negative sleep.

#### Testing that the limit exists

```python
def test_burst_triggers_429_with_retry_after(client):
    # the mock allows 3 requests, then limits
    codes = [client.get("/limited").status_code for _ in range(5)]
    assert codes == [200, 200, 200, 429, 429]

    limited = client.get("/limited")
    assert limited.status_code == 429
    assert int(limited.headers["Retry-After"]) >= 1
```

The list comprehension sends five rapid requests and collects the codes, so the assertion documents the exact threshold: three allowed, then limited. Asserting the whole list gives a precise, readable failure (`[200, 200, 429, ...]` is not `[200, 200, 200, 429, 429]`). Mock server output: passes.

#### Handling `429` politely in a suite

If your tests may hit a limit, do not just sleep a random time and hope. Wait as long as the server says, cap the wait so a bad header cannot freeze the pipeline, and give up after a few tries:

```python
import time
import pytest


def get_with_backoff(client, path, max_tries=5, max_wait=30):
    for attempt in range(1, max_tries + 1):
        response = client.get(path)
        if response.status_code != 429:
            return response
        time.sleep(min(retry_after_seconds(response), max_wait))
    pytest.fail(f"still rate limited after {max_tries} tries: GET {path}")
```

Mock server output (with the mock's counter and a patched `time.sleep`, so nothing actually waited): the helper slept `[1, 1]` seconds, then returned `200`. Use backoff only for incidental calls (setup, cleanup). When rate limiting is the thing under test, you want to *see* the `429`, not hide it.

Retrying is only safe for idempotent methods. Automatically retrying a `POST` after a `429` or `503` can create duplicates if the first attempt partly succeeded. Retry policies built into HTTP clients (`requests` can do this with an `HTTPAdapter`) are an advanced topic; for today, remember to treat retries as a deliberate decision.

### 10. Helpful Assertion Messages and a Reusable `assert_status`

#### 10.1 The problem with a bare assert

Here is what a plain failing assertion looks like. This was run against the mock server:

```python
def test_bare(client):
    r = client.get("/posts/99999")
    assert r.status_code == 200
```

Mock server output:

```text
>       assert r.status_code == 200
E       assert 404 == 200
E        +  where 404 = <Response [404]>.status_code
```

pytest's assertion rewriting shows a `404` arrived where a `200` was expected. But at 3 a.m., in a pipeline log, you do not know **which URL**, **which method**, or **what the server said**; the error body often holds the real cause ("token expired").

#### 10.2 A message after the comma

Python's `assert condition, message` lets you attach text. Use an f-string:

```python
def test_bare_msg(client):
    r = client.get("/posts/99999")
    assert r.status_code == 200, f"GET {r.url} -> {r.status_code}: {r.text[:200]}"
```

Mock server output:

```text
E       AssertionError: GET http://127.0.0.1:35277/posts/99999 -> 404: {"error": {"code": "not_found", "message": "post 99999 not found"}}
E       assert 404 == 200
```

The message now names the URL and the start of the body. Slice the body (`[:200]`) so a huge HTML error page does not flood the log.

### 10.3 The reusable helper

Repeating that f-string in hundreds of tests is error-prone, so centralise it:

```python
# api/assertions.py
def _describe(response):
    req = response.request
    return f"{req.method} {response.url}"


def assert_status(response, expected, *, context=""):
    """Assert the status code is one of `expected` (an int or an iterable of ints)."""
    allowed = (expected,) if isinstance(expected, int) else tuple(expected)
    if response.status_code in allowed:
        return
    body = response.text[:300] or "<empty body>"
    prefix = f"{context}: " if context else ""
    raise AssertionError(
        f"{prefix}expected {' or '.join(map(str, allowed))} "
        f"but got {response.status_code} {response.reason} "
        f"for {_describe(response)}\n"
        f"Content-Type: {response.headers.get('Content-Type', '<none>')}\n"
        f"Body: {body}"
    )
```

Line by line: `_describe` builds `"GET http://.../posts/99999"` from `response.request`, which `requests` keeps on every response. The bare `*` makes `context` keyword-only. `allowed` normalises a single code into a one-element tuple so ints and lists are handled identically. A passing call returns silently. On failure the message carries the context prefix, expected codes, actual code and reason, method and URL, `Content-Type`, and the first 300 characters of the body (or `<empty body>`). It raises `AssertionError` explicitly, so the message is exactly what we wrote and still works under `python -O`.

Mock server output with `context="read missing post"` and `expected=200`:

```text
read missing post: expected 200 but got 404 Not Found for GET http://127.0.0.1:37267/posts/99999
Content-Type: application/json; charset=utf-8
Body: {"error": {"code": "not_found", "message": "post 99999 not found"}}
```

Typical usage:

```python
from api.assertions import assert_status


def test_create_post(client):
    r = client.post("/posts", json={"title": "Hello"},
                    headers={"Authorization": "Bearer user-token"})
    assert_status(r, 201, context="create post")


def test_delete_post_accepts_200_or_204(client):
    r = client.delete("/posts/1", headers={"Authorization": "Bearer user-token"})
    assert_status(r, (200, 204))
```

Tip: add `__tracebackhide__ = True` as the first line of `assert_status` so pytest's report points at the calling test line.

**Never put secrets in messages.** Do not print `Authorization` headers or tokens in a failure message that ends up in a shared CI log. The helper above prints the URL, status, content type, and a truncated body. If bodies may contain personal or secret data, truncate more aggressively or redact. How pipelines store and mask secrets is covered on Friday.

### 11. Common Mistakes and Anti-Patterns

Each entry gives the symptom, why it hurts, and the fix.

#### Anti-pattern 1: asserting only `200`

```python
# BAD
def test_get_user(client):
    response = client.get("/users/1")
    assert response.status_code == 200
```

On its own this proves that the endpoint answered with success, and nothing else. It does not prove that the correct user came back. It does not prove that unauthorised callers are refused. It does not prove that a missing user returns `404`. If your whole suite looks like this, you are testing that the server is switched on. **Fix:** pair every positive status assertion with a body assertion, and for each endpoint add the negative tests from section 4.

#### Anti-pattern 2: using `response.ok` or `< 400` as the main check

`assert response.ok` passes for `301`, `204` when you wanted `200`, and any other sub-400 code. It also fails with the unhelpful `assert False`. **Fix:** assert the exact code with a message or `assert_status`.

#### Anti-pattern 3: loosening an assertion until it passes

A test fails with `201 != 200`. The tempting "fix" is `in (200, 201)`. Sometimes that is right (the specification allows both); too often it is a way to silence a real regression. **Fix:** ask what the specification says. If it says `201`, the API is wrong and you have found a bug.

#### Anti-pattern 4: testing only the happy path

A suite with fifty `200`/`201` assertions and no `4xx` assertions leaves the API's input validation and security completely unchecked. **Fix:** use the recipe in section 4 for every endpoint.

#### Anti-pattern 5: negative test with the wrong cause

A test meant to check `404` accidentally lacks a token and gets `401`. **Fix:** change **one** thing at a time from a known-good request.

### 12. Practice Exercises

These use the local mock server pattern, but you can adapt them to JSONPlaceholder (`https://jsonplaceholder.typicode.com`) and httpbin (`https://httpbin.org/status/<code>`, which returns whatever code you request). If you use external hosts, expect their behaviour to differ in places; results quoted from them are **representative**.

#### Exercise 1: The first assertion

Write a test for `GET /posts/1` that asserts a `200`, checks the `Content-Type` starts with `application/json`, and checks that `id` equals `1`.

#### Exercise 2: The missing resource

Write a test for `GET /posts/99999` that asserts `404`, and a second for `GET /posts/abc` that asserts `400`. Then write one sentence explaining why `404` and `400` differ.

#### Exercise 3: One test per code

Using a `/status/<code>` endpoint (the mock provides one; httpbin provides the same), write a single parametrized test covering `200, 201, 202, 204, 400, 401, 403, 404, 405, 409, 415, 422, 429, 500, 502, 503, 504`. Assert that each returns exactly the requested code. Then add an assertion that the **class** is right (`code // 100`).

#### Exercise 4: Redirects

Write two tests: one that checks `GET /old` with `allow_redirects=False` gives `301` and `Location: /new`; and one that follows the redirect and asserts the final code is `200` and that `response.history` holds exactly one hop.

#### Exercise 5: 401 versus 403

For `GET /admin/stats`, write one test containing four calls: no token, invalid token, a normal user's token, and an admin's token. State the expected code for each before running.

#### Exercise 6: Idempotency

Delete `/posts/1` twice using a valid token. State what each call returns on this API, then verify that a final `GET` returns `404`. Write a comment explaining why the second `DELETE` is still considered idempotent.

#### Exercise 7: The error contract

Write `assert_error_response(response, status, code)` from section 7.4 (you may type it from the lesson, then explain each line in a comment). Use it to verify that `POST /posts` without a `title` returns `422` with `error.code == "validation_failed"` and a `details` entry naming `title`.

#### Exercise 8: Rate limit

Call `GET /limited` five times. Assert the exact sequence of codes. Then write `retry_after_seconds` and test it with three fake responses: a header of `"120"`, an HTTP date in the future, and no header at all.

#### Exercise 9: Hunt the defects

For each observation, say whether it is a defect and what the correct code probably is:

1. `GET /users/abc` returns `500`.
2. `POST /users` with a missing email returns `200` and `{"success": false}`.
3. `GET /admin/stats` with no token returns `403`.
4. `DELETE /posts/1` returns `204` the first time and `404` the second time.
5. `POST /orders` returns `201` with no `Location` header and an empty body.
6. `DELETE /posts` returns `404`.

### Exercise Solutions

#### Solution 1

Assert `status_code == 200` first (with a message such as `f"GET {response.url}: {response.text[:200]}"`), then `headers["Content-Type"].startswith("application/json")`, then `response.json()["id"] == 1`. Status first, so `.json()` is safe.

#### Solution 2

`client.get("/posts/99999").status_code == 404` and `client.get("/posts/abc").status_code == 400`. `99999` is a valid identifier shape that matches no record (not found); `abc` cannot be a valid identifier at all (malformed). If your API returns `404` for both, assert what its specification documents.

#### Solution 3

```python
import pytest

CODES = [200, 201, 202, 204, 400, 401, 403, 404, 405, 409, 415, 422, 429, 500, 502, 503, 504]

@pytest.mark.parametrize("code", CODES)
def test_status_endpoint_returns_requested_code(client, code):
    response = client.get(f"/status/{code}")
    assert response.status_code == code
    assert response.status_code // 100 == code // 100
```

Mock server output: 17 parametrized cases passed. (httpbin gives the same codes; that output is **representative**.)

#### Solution 4

Same as section 3.6: `allow_redirects=False` gives `301` and `Location == "/new"`; the default call gives `200`, with `len(response.history) == 1` and `response.history[0].status_code == 301`.

#### Solution 5

Four calls to `/admin/stats` with expected codes `401` (no token), `401` (invalid token), `403` (valid user token), `200` (admin token), exactly as in section 3.9. Both of the first two callers are unidentified; only the third is identified but refused.

#### Solution 6

```python
def test_delete_is_idempotent_in_state(client):
    auth = {"Authorization": "Bearer user-token"}
    assert client.delete("/posts/1", headers=auth).status_code == 204
    assert client.delete("/posts/1", headers=auth).status_code == 404  # documented: nothing left to delete
    assert client.get("/posts/1").status_code == 404                   # state: still gone
```

Explanation: idempotency concerns the **server state** after the call. After one delete or two, the resource is absent. The response code may differ (`204` then `404`) without breaking idempotency, because nothing else changed.

#### Solution 7

The helper is exactly the one in section 7.4 (each line explained there). The test:

```python
def test_missing_title_is_422(client):
    r = client.post("/posts", json={"body": "x"},
                    headers={"Authorization": "Bearer user-token"})
    err = assert_error_response(r, 422, "validation_failed")
    assert {"field": "title", "problem": "required"} in err["details"]
```

#### Solution 8

```python
def test_rate_limit_sequence(client):
    codes = [client.get("/limited").status_code for _ in range(5)]
    assert codes == [200, 200, 200, 429, 429]


class FakeResponse:
    def __init__(self, headers):
        self.headers = headers


def test_retry_after_parsing():
    assert retry_after_seconds(FakeResponse({"Retry-After": "120"})) == 120
    future = FakeResponse({"Retry-After": "Wed, 21 Oct 2099 07:28:00 GMT"})
    assert retry_after_seconds(future) > 1000
    assert retry_after_seconds(FakeResponse({})) == 1.0
```

Mock server output: both tests passed. `FakeResponse` is a minimal stand-in; replacing real objects like this is the idea behind mocking, covered on Wednesday.

#### Solution 9

1. **Defect.** `500` for malformed input. Expected `400` (or `404`).
2. **Defect.** `200` for a failure. Expected `422` (or `400`) with the error contract.
3. **Defect.** Unauthenticated callers should get `401`, not `403` (and ideally a `WWW-Authenticate` header).
4. **Not a defect.** Second delete returning `404` is acceptable and idempotent in state, provided the specification documents it.
5. **Defect.** A creation response needs a `Location` header and/or the new `id` in a body, otherwise clients cannot find what was created.
6. **Likely a defect.** `405` with an `Allow` header is correct for a method not supported on the collection. A `404` suggests the route does not exist; some public sandboxes do this and it should be recorded as a deviation, not accepted silently.

---

### Self-Check Quiz

Answer without looking back, then compare with the answers below.

**Q1.** A `POST /users` request carries a valid token, but the user's role may not create users. Which code?

- A) `400`
- B) `401`
- C) `403`
- D) `404`

**Q2.** Which assertion is **best** for a test that creates a record?

- A) `assert response.ok`
- B) `assert response.status_code == 201`
- C) `assert str(response.status_code).startswith("2")`
- D) `assert response.reason == "Created"`

**Q3.** `GET /orders/xyz` (the id must be an integer) returns `500` with a stack trace. What is the right classification?

- A) Correct behaviour
- B) A defect: should be `400` (or `404`), and the stack trace is also a leak
- C) A defect only in production
- D) Not testable

**Q4.** What does `response.ok` return for a `302` response?

- A) `False`
- B) `True`
- C) It raises
- D) `None`

**Q5.** A `DELETE /items/5` returns `204` the first time and `404` the second. Is `DELETE` still idempotent?

- A) No, because the codes differ
- B) Yes, because the server state after both calls is the same
- C) Only if the second returns `204`
- D) Only if the second returns `500`

**Q6.** Which two codes concern the request's `Content-Type` and the request's `Accept` header, respectively?

- A) `400` and `422`
- B) `415` and `406`
- C) `405` and `404`
- D) `409` and `429`

**Q7.** A `429` response contains `Retry-After: 30`. What should a polite automated client do?

- A) Retry immediately
- B) Wait about 30 seconds, then retry (within a capped number of tries)
- C) Stop the test run forever
- D) Treat it as a `5xx` defect

**Q8.** Why should the body (including `error.code`) be asserted in a negative test, not only the status?

- A) The status code is unreliable
- B) Different error causes can share a status code; the body proves the right reason and contract
- C) `.json()` is faster than `status_code`
- D) It is a pytest requirement

### Quiz Answers

1. **C.** The caller is identified but not permitted: `403`. (`401` would mean no or invalid credentials.)
2. **B.** The exact documented code. `ok` is too loose; a `2xx` prefix check accepts `200`; the reason phrase is not the contract.
3. **B.** A `5xx` from client input is a defect, and exposing a stack trace is an information leak.
4. **B.** `True`. Anything below 400 is "ok", including redirects.
5. **B.** Idempotency is about the resulting **state**, and the resource is gone either way. The status code may legitimately differ.
6. **B.** `415 Unsupported Media Type` concerns what you **sent** (`Content-Type`); `406 Not Acceptable` concerns what you **asked for** (`Accept`).
7. **B.** Respect `Retry-After`, cap the wait, and limit the number of retries.
8. **B.** Several different errors can return the same `4xx` code. The body (and `error.code`) proves the correct cause and a consistent contract.

---

### Glossary

#### Status code
A three-digit integer in the first line of an HTTP response summarising the result of the request. Always compare it as an `int`.

#### Status class
The first digit of the code: `1xx` informational, `2xx` success, `3xx` redirection, `4xx` client error, `5xx` server error. A client must treat an unknown code like the `x00` code of its class.

#### Positive control
A valid request included inside a negative-test group, proving the endpoint works at all, so that "everything is rejected" cannot masquerade as "negative tests pass".

#### Idempotent
An operation whose repeated execution leaves the server's state the same as executing it once. `GET`, `PUT`, `DELETE` are idempotent; `POST` normally is not. The *response code* may still differ between calls.

#### `Retry-After`
A response header (with `429`, `503`, and some redirects) that says how long to wait before trying again, as seconds or as an HTTP date.

#### `response.ok`
A boolean that is `True` for any status below 400, redirects included. Too loose for primary assertions.

#### `raise_for_status()`
Raises `requests.HTTPError` for `4xx` and `5xx`. Best for setup and production code, not for asserting an expected error.

#### Negative test
A test that sends an invalid, unauthorised, or abnormal request and checks the API fails correctly: the right `4xx`, a clear error body, no side effects.

#### Redirect
A `3xx` response with a `Location` header. `requests` follows it by default; `allow_redirects=False` disables that.

#### Gateway
A server between client and application (load balancer, reverse proxy, API gateway). It, rather than the application, usually produces `502`, `503`, and `504`.

---

## Summary

- A status code is the server's machine-readable verdict. Compare **integers**, never reason phrases. The first digit is the class: `2xx` success, `3xx` go elsewhere, `4xx` the client erred, `5xx` the server erred.
- Know the key codes: `200`, `201` (check `Location`), `202` (poll), `204` (empty body, no `.json()`), `301`/`302` (`allow_redirects=False`), `304` (conditional `GET`), `400`, `401`, `403`, `404`, `405` (check `Allow`), `409`, `415`, `422`, `429` (`Retry-After`), `500`, `502`, `503`, `504`.
- `401` means "who are you?"; `403` means "I know you, and no". `404` means "valid request, nothing there"; `400` means "malformed request". Test with several callers, include a positive control, and follow the documented specification.
- Every endpoint deserves positive **and** negative tests, plus a `< 500` safety net. Assert exact codes by default; accept several only when the specification allows; use class checks for safety nets.
- `response.ok` is `True` below 400, so it is too loose to assert with. Use `status_code` for assertions and `raise_for_status()` for setup.
- Validate status **and** body together, including the error contract. A `200` carrying an error, or a `5xx` caused by client input, is a defect.
- Idempotent `DELETE` and `PUT` guarantee the same **state**, not the same code.
- Handle `429` by reading `Retry-After`, capping waits and retries, and never hiding the `429` when rate limiting is the thing under test.
- Centralise rich failure messages (method, URL, code, content type, body excerpt) in `assert_status`, and never include secrets. The biggest anti-pattern is asserting only `200`.

## Additional Resources

- MDN Web Docs, *HTTP response status codes*: https://developer.mozilla.org/en-US/docs/Web/HTTP/Status
- RFC 9110, *HTTP Semantics* (Section 15, Status Codes): https://www.rfc-editor.org/rfc/rfc9110.html#name-status-codes
- RFC 9110, *Idempotent Methods* (Section 9.2.2): https://www.rfc-editor.org/rfc/rfc9110.html#name-idempotent-methods
- MDN Web Docs, *Retry-After header*: https://developer.mozilla.org/en-US/docs/Web/HTTP/Headers/Retry-After
- MDN Web Docs, *429 Too Many Requests*: https://developer.mozilla.org/en-US/docs/Web/HTTP/Status/429
- Requests documentation, *Response objects and `raise_for_status`*: https://requests.readthedocs.io/en/latest/api/#requests.Response.raise_for_status
- Requests documentation, *Redirection and history*: https://requests.readthedocs.io/en/latest/user/quickstart/#redirection-and-history
- pytest documentation, *How to parametrize fixtures and test functions*: https://docs.pytest.org/en/stable/how-to/parametrize.html
- httpbin, *Status codes*: https://httpbin.org/#/Status_codes
