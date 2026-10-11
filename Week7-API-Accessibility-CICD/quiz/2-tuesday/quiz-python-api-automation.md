# Daily Knowledge Check: Week 7 Tuesday - Python API Automation

This quiz covers today's Python API automation topics: the `requests` library, PyTest API test structure, sending HTTP requests from automated tests, status code validation, JSON response validation, headers and authentication, and fixtures and parametrization. Try each question on your own first, then open the solution to check your reasoning. Every solution is hidden inside a collapsible block so you are not tempted to peek.

## Part 1: Multiple Choice

### 1. What is the default timeout of a `requests.get(url)` call when you do not pass `timeout=`?

- [ ] A) There is no timeout: `requests` can wait forever
- [ ] B) 30 seconds, then it raises `Timeout`
- [ ] C) 10 seconds, then it returns `None`
- [ ] D) The value of the `REQUESTS_TIMEOUT` environment variable

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** A) There is no timeout: `requests` can wait forever

**Explanation:** `requests` has no built-in default timeout, so a stalled server can hang your test run. Always pass `timeout=`.
- **Why others are wrong:**
  - B) There is no 30-second default.
  - C) No default exists, and `requests` never returns `None` for a timeout.
  - D) The library does not read such a variable; you must set `timeout=` yourself.
</details>

### 2. Which call sends a Python dict as a JSON body and sets `Content-Type: application/json` automatically?

- [ ] A) `requests.post(url, data=payload)`
- [ ] B) `requests.post(url, params=payload)`
- [ ] C) `requests.post(url, json=payload)`
- [ ] D) `requests.post(url, headers=payload)`

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** C) `requests.post(url, json=payload)`

**Explanation:** `json=` serialises the dict and sets the Content-Type header. `data=` with a dict sends a form body instead.
- **Why others are wrong:**
  - A) `data=` with a dict sends form-encoded data (`a=1`), not JSON.
  - B) `params=` builds the query string of the URL, not a body.
  - D) `headers=` sets request headers; it does not create a body.
</details>

### 3. What does `response.raise_for_status()` do for a `404` response?

- [ ] A) Returns `False`
- [ ] B) Raises `requests.exceptions.HTTPError`
- [ ] C) Retries the request once
- [ ] D) Raises `ConnectionError`

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** B) Raises `requests.exceptions.HTTPError`

**Explanation:** `raise_for_status()` raises `HTTPError` for 4xx and 5xx responses and does nothing for success codes.
- **Why others are wrong:**
  - A) It does not return a flag; `response.ok` is the boolean check.
  - C) `requests` never retries on its own.
  - D) The server was reached, so there is no connection problem; the exception is `HTTPError`.
</details>

### 4. A server accepts the connection but is too slow to send data back before the `timeout` expires. Which exception is raised?

- [ ] A) `requests.exceptions.HTTPError`
- [ ] B) `requests.exceptions.TooManyRedirects`
- [ ] C) `requests.exceptions.InvalidURL`
- [ ] D) `requests.exceptions.ReadTimeout`

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** D) `requests.exceptions.ReadTimeout`

**Explanation:** `ReadTimeout` means the server was reached but too slow to send data. `ConnectTimeout` is the connect phase.
- **Why others are wrong:**
  - A) `HTTPError` comes from `raise_for_status()` on 4xx/5xx, not from slowness.
  - B) That is raised on a redirect loop (default limit 30).
  - C) That signals a malformed URL, and the URL here was fine.
</details>

### 5. You create `s = requests.Session()` and call `s.get(url)`. What is true about timeouts?

- [ ] A) The session applies a 30-second timeout automatically
- [ ] B) The session has no default timeout, so you must still pass `timeout=` (or set it in your own client)
- [ ] C) The first request sets a timeout that later calls inherit
- [ ] D) Timeouts are not needed once a session reuses connections

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** B) The session has no default timeout, so you must still pass `timeout=` (or set it in your own client)

**Explanation:** A `Session` shares headers, cookies and connections, but not a timeout. This is a well-known gotcha.
- **Why others are wrong:**
  - A) Sessions have no default timeout.
  - C) Nothing like this exists; timeouts are per call unless you add them yourself.
  - D) A reused connection can still hang, so every request needs a timeout.
</details>

### 6. Which file or function names will PyTest's default discovery collect as tests?

- [ ] A) `test_login.py` containing `def test_valid_login():`
- [ ] B) `login_test.py` containing `def check_valid_login():`
- [ ] C) `api_tests.py` containing `def valid_login_test():`
- [ ] D) `test_login.py` containing `class TestLogin:` that defines `__init__`

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** A) `test_login.py` containing `def test_valid_login():`

**Explanation:** PyTest discovers by name: `test_*.py` files, `test_*` functions, and `Test*` classes without `__init__`.
- **Why others are wrong:**
  - B) Neither the file nor the function name matches the discovery patterns.
  - C) The names do not start with `test_`, so nothing is collected.
  - D) A `Test*` class with an `__init__` method is not collected.
</details>

### 7. In the Arrange-Act-Assert pattern for an API test, what belongs in the Act step?

- [ ] A) Building the payload and unique test data
- [ ] B) Checking the status code and body
- [ ] C) Making the single request under test
- [ ] D) Deleting the record that was created

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** C) Making the single request under test

**Explanation:** Arrange prepares data, Act makes one request, Assert checks the outcome. One request in Act keeps a failure easy to locate.
- **Why others are wrong:**
  - A) That is the Arrange step.
  - B) Those checks belong to Assert.
  - D) Cleanup is a separate concern, usually in a fixture's teardown or `finally` block.
</details>

### 8. What does PyTest's assertion rewriting give you when a plain `assert response.status_code == 201` fails?

- [ ] A) An automatic retry of the request
- [ ] B) A failure message that shows the values involved, such as the actual status code
- [ ] C) A skipped test instead of a failure
- [ ] D) A mandatory need to use `self.assertEqual`

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** B) A failure message that shows the values involved, such as the actual status code

**Explanation:** Assertion rewriting lets you use plain `assert` and still see the compared values. You can add a custom message for extra context such as the response body.
- **Why others are wrong:**
  - A) PyTest never re-sends requests.
  - C) A failed assert is reported as FAILED, not skipped.
  - D) Plain `assert` is enough in PyTest; no `unittest` methods are required.
</details>

### 9. What does `--strict-markers` (set in `addopts` of `pytest.ini`) protect you from?

- [ ] A) Tests running in random order
- [ ] B) Slow tests exceeding a time limit
- [ ] C) Fixtures with the wrong scope
- [ ] D) A typo like `@pytest.mark.smoek` silently creating a new marker that `-m smoke` never selects

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** D) A typo like `@pytest.mark.smoek` silently creating a new marker that `-m smoke` never selects

**Explanation:** With `--strict-markers`, an unregistered marker name becomes an error instead of a warning.
- **Why others are wrong:**
  - A) Ordering is not controlled by this option.
  - B) It has nothing to do with timing.
  - C) Scope errors are reported as `ScopeMismatch`; markers are a separate concern.
</details>

### 10. A test is marked `@pytest.mark.xfail(reason="BUG-123", strict=True)`, and the bug gets fixed so the test now passes. What does PyTest report?

- [ ] A) A failure (`XPASS(strict)`), forcing someone to remove the `xfail` marker
- [ ] B) A normal pass, with no remark
- [ ] C) A skipped test
- [ ] D) An ERROR at setup

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** A) A failure (`XPASS(strict)`), forcing someone to remove the `xfail` marker

**Explanation:** With `strict=True`, an unexpected pass is a failure. Without `strict` it shows only as `XPASS`, which is easy to overlook.
- **Why others are wrong:**
  - B) Without `strict` it would show only as `XPASS`; strict mode escalates it to a failure.
  - C) Skipping is done with `skip`/`skipif`, not by a passing xfail.
  - D) Nothing went wrong in setup; the unexpected pass itself is reported as FAILED.
</details>

### 11. Which command runs only the tests labelled with the registered `smoke` marker?

- [ ] A) `pytest -k smoke`
- [ ] B) `pytest -s smoke`
- [ ] C) `pytest -x smoke`
- [ ] D) `pytest -m smoke`

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** D) `pytest -m smoke`

**Explanation:** `-m` selects by marker; `-k` matches substrings of test names and is meant for ad hoc selection.
- **Why others are wrong:**
  - A) `-k` matches substrings of test names, so it misses marked tests whose names lack 'smoke'; use `-m` for planned categories.
  - B) `-s` shows print output; it does not select tests.
  - C) `-x` stops at the first failure; `smoke` would be treated as a path.
</details>

### 12. An API call is made with a valid, logged-in user token, but the user's role is not allowed to delete orders. Which status code is the correct result?

- [ ] A) `401 Unauthorized`
- [ ] B) `403 Forbidden`
- [ ] C) `404 Not Found`
- [ ] D) `400 Bad Request`

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** B) `403 Forbidden`

**Explanation:** `401` means "who are you?" (authentication). `403` means "I know you, and no" (authorization).
- **Why others are wrong:**
  - A) `401` is for missing or invalid credentials; this caller is identified.
  - C) The resource exists; the issue is permission, not existence.
  - D) The request is well formed; it is the permission that fails.
</details>

### 13. Why is `assert response.ok` generally a poor assertion for a create test?

- [ ] A) `ok` raises an exception when the status is 201
- [ ] B) `ok` is only `True` for code 200
- [ ] C) `ok` is `True` for any code below 400, so `200`, `204`, and `302` would all pass when only `201` is correct
- [ ] D) `ok` reads the response body, which may be empty

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** C) `ok` is `True` for any code below 400, so `200`, `204`, and `302` would all pass when only `201` is correct

**Explanation:** Assert exact codes with `status_code`. `response.ok` is too loose, and `raise_for_status()` is better for setup code.
- **Why others are wrong:**
  - A) `ok` is a plain boolean property and never raises.
  - B) It is `True` for anything below 400, which is exactly the problem.
  - D) `ok` depends only on the status code.
</details>

### 14. Which statement is correct for a `204 No Content` response?

- [ ] A) The body contains `{}`, which `.json()` parses to an empty dict
- [ ] B) It means the resource was created and its `Location` header must be checked
- [ ] C) It means the server accepted the request and you should poll a status URL
- [ ] D) The body is empty, so you should not call `.json()` on it

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** D) The body is empty, so you should not call `.json()` on it

**Explanation:** A `204` carries no body. Calling `.json()` on an empty body raises `JSONDecodeError`.
- **Why others are wrong:**
  - A) A `204` has no body at all, not even `{}`.
  - B) That describes `201 Created`.
  - C) That describes `202 Accepted`.
</details>

### 15. After a `POST` returns `201 Created`, which header should a thorough test check?

- [ ] A) `Location`, which points to the new resource
- [ ] B) `Retry-After`
- [ ] C) `Allow`
- [ ] D) `WWW-Authenticate: Basic`

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** A) `Location`, which points to the new resource

**Explanation:** A `201` normally comes with a `Location` header and a body containing the new id, so a follow-up `GET` can confirm it.
- **Why others are wrong:**
  - B) That belongs to `429` (and some `503`) responses.
  - C) `Allow` is checked on `405 Method Not Allowed`.
  - D) That relates to authentication challenges, not creation.
</details>

### 16. A rate-limited API answers `429 Too Many Requests`. What should a well-behaved test helper read to decide how long to wait?

- [ ] A) The `Content-Length` header
- [ ] B) The `Retry-After` header, capping the wait and the number of retries
- [ ] C) The `Location` header
- [ ] D) Nothing: always sleep a fixed 60 seconds

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** B) The `Retry-After` header, capping the wait and the number of retries

**Explanation:** Handle `429` by reading `Retry-After`, capping waits and retries, and never hiding the `429` when rate limiting is the thing under test.
- **Why others are wrong:**
  - A) It gives the body size, not a waiting time.
  - C) That is for new resources and redirects.
  - D) A fixed sleep ignores what the server told you and makes tests slow or flaky.
</details>

### 17. Which statement about HTTP Basic authentication with `auth=("user", "pass")` is correct?

- [ ] A) The password is encrypted with AES before sending
- [ ] B) The credentials are sent in the URL query string
- [ ] C) The header is `Authorization: Basic <Base64>`, and Base64 is encoding, not encryption
- [ ] D) It requires first calling a login endpoint to get a token

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** C) The header is `Authorization: Basic <Base64>`, and Base64 is encoding, not encryption

**Explanation:** Anyone who sees the header can decode it. Secrets must therefore not be committed or logged.
- **Why others are wrong:**
  - A) Base64 is a reversible encoding, not encryption.
  - B) They travel in the `Authorization` header.
  - D) That is the bearer token flow; Basic sends credentials with each request.
</details>

### 18. How is a bearer token normally sent with a request?

- [ ] A) `Authorization: Basic <token>`
- [ ] B) `Authorization: Bearer <token>`
- [ ] C) `X-Bearer: <token>` in the URL
- [ ] D) `Content-Type: Bearer <token>`

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** B) `Authorization: Bearer <token>`

**Explanation:** The token comes from a login call and travels in the `Authorization` header. Keeping it on a `Session` lets one login serve the whole run.
- **Why others are wrong:**
  - A) `Basic` carries Base64 `user:password`, not a token.
  - C) Tokens belong in the `Authorization` header with the `Bearer` scheme, not in a URL.
  - D) `Content-Type` describes the body format, not identity.
</details>

### 19. A JWT consists of which three parts?

- [ ] A) `header.payload.signature`
- [ ] B) `user.password.salt`
- [ ] C) `key.value.expiry`
- [ ] D) `public.private.certificate`

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** A) `header.payload.signature`

**Explanation:** The parts are readable by anyone but tamper-evident, and the expiry lives in the `exp` claim. Decode only to inspect, not to trust.
- **Why others are wrong:**
  - B) A JWT contains no password or salt.
  - C) Those are not the JWT parts; expiry is a claim inside the payload.
  - D) No key pairs are embedded in the token.
</details>

### 20. A fixture contains `setup; yield value; cleanup`. The test using it fails on an assertion. When does `cleanup` run?

- [ ] A) After the test, even though it failed
- [ ] B) Never, because the failure aborts the fixture
- [ ] C) Before the test starts
- [ ] D) Only when the test passes

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** A) After the test, even though it failed

**Explanation:** Code after `yield` is teardown, and PyTest runs it whether the test passed or failed. This keeps test data from leaking.
- **Why others are wrong:**
  - B) Teardown still runs after a failed test.
  - C) Code before `yield` is setup; code after it is teardown.
  - D) Teardown does not depend on the verdict.
</details>

### 21. Which fixture scope is the best fit for a login token that is expensive to obtain and read-only for all tests?

- [ ] A) `function`
- [ ] B) `class`
- [ ] C) `module` only if every test file shares one
- [ ] D) `session`

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** D) `session`

**Explanation:** A `session` fixture is built once per whole `pytest` run, which suits expensive, read-only setup such as base URL, config, login token and connection pool.
- **Why others are wrong:**
  - A) It would log in again before every test, which is slow.
  - B) It would log in once per test class, repeating work needlessly for module-wide use.
  - C) A `module` fixture is rebuilt for each file; `session` is the scope that gives one login for the whole run.
</details>

### 22. A `session`-scoped fixture requests a `function`-scoped fixture as a dependency. What happens?

- [ ] A) The function fixture silently becomes session-scoped
- [ ] B) PyTest raises `ScopeMismatch`
- [ ] C) The test runs twice
- [ ] D) The session fixture is rebuilt for each test

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** B) PyTest raises `ScopeMismatch`

**Explanation:** Wider-scoped fixtures cannot depend on narrower ones, because the narrow value would be discarded while the wide one lives on.
- **Why others are wrong:**
  - A) PyTest does not change scopes; it raises an error.
  - C) Nothing is duplicated; the setup fails with a scope error.
  - D) It would be rebuilt only if its own scope was `function`.
</details>

### 23. SCENARIO: A suite of 80 API tests each need an authenticated call, and each login takes 1 second. Which design from today's toolkit fits best?

- [ ] A) Log in inside every test body
- [ ] B) Hard-code the token string in `conftest.py`
- [ ] C) A `session`-scoped `auth_token` fixture plus a per-test `auth_client` fixture that uses it
- [ ] D) Call the fixture function directly like `auth_token()` in each test

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** C) A `session`-scoped `auth_token` fixture plus a per-test `auth_client` fixture that uses it

**Explanation:** Log in once per run for the token, and give each test its own client so headers and state do not leak between tests.
- **Why others are wrong:**
  - A) That costs 80 logins and duplicates code.
  - B) Tokens expire and secrets do not belong in code; use environment variables and a login fixture.
  - D) Fixtures must never be called directly; PyTest injects them by parameter name.
</details>

### 24. SCENARIO: `GET /users/99` returns status `200` with the body `{"error": "User not found"}`. A test only asserts `status_code == 200` and passes. What is the best assessment?

- [ ] A) The test is too weak: a `200` carrying an error is a defect, so status and body must be validated together
- [ ] B) The API is correct because `200` means success
- [ ] C) The test is correct; bodies are never checked in API tests
- [ ] D) The test should assert `status_code == 500` instead

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** A) The test is too weak: a `200` carrying an error is a defect, so status and body must be validated together

**Explanation:** The status code only says the server responded. The body shows whether the response is correct, and the error contract should be checked too.
- **Why others are wrong:**
  - B) A not-found condition should not be reported as `200` with an error body.
  - C) Today's lessons validate status, headers, and body in layers.
  - D) A missing user is not a server fault; the documented code would more likely be `404`.
</details>

## Part 2: True/False

### 25. `requests` raises an exception by default when a server responds with `404`.

- [ ] True
- [ ] False

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** False

**Explanation:** `requests` does not raise on 4xx and 5xx. Only `raise_for_status()` raises `HTTPError`. Exceptions such as `ConnectionError` or `Timeout` occur when no response arrives.
</details>

### 26. Using `requests.Session()` automatically gives every request a default timeout.

- [ ] True
- [ ] False

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** False

**Explanation:** A `Session` shares headers, cookies and connections but has no default timeout; pass `timeout=` or centralise it in your client.
</details>

### 27. The Base64 string in a Basic `Authorization` header is encrypted, so it is safe to log.

- [ ] True
- [ ] False

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** False

**Explanation:** Base64 is encoding, not encryption. Anyone can decode it, so secrets must be kept out of logs and code.
</details>

### 28. Teardown code after `yield` in a fixture still runs when the test fails.

- [ ] True
- [ ] False

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** True

**Explanation:** PyTest runs the teardown whether the test passed or failed, which is why `yield` fixtures are the right tool for cleaning up test data.
</details>

### 29. `isinstance(True, int)` is `True`, so checking only `isinstance(value, int)` would accept a boolean where a number is expected.

- [ ] True
- [ ] False

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** True

**Explanation:** Booleans are integers in Python. When the type matters, also reject `bool` explicitly. A type check is the only way to catch a number delivered as text such as `"1"`.
</details>

### 30. A `401` response means the caller is known but is not permitted to do the action.

- [ ] True
- [ ] False

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** False

**Explanation:** That describes `403`. `401` means the server does not know who you are (missing, invalid, or expired credentials).
</details>

### 31. You should call a fixture directly in a test, for example `client = client()`, instead of requesting it as a parameter.

- [ ] True
- [ ] False

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** False

**Explanation:** Never call fixtures yourself. PyTest injects them by matching the parameter name.
</details>

### 32. Sending `requests.post(url, data={"a": 1})` posts the JSON `{"a": 1}` with `Content-Type: application/json`.

- [ ] True
- [ ] False

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** False

**Explanation:** `data=` with a dict sends a form body (`a=1`) with `application/x-www-form-urlencoded`. Use `json=` for JSON APIs.
</details>

### 33. An idempotent `DELETE` guarantees the same status code every time it is repeated.

- [ ] True
- [ ] False

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** False

**Explanation:** Idempotency guarantees the same resulting **state**, not the same code: the first `DELETE` may return `200`/`204` and a repeat may return `404`.
</details>

### 34. A well-written test may rely on running after another test that creates its data, as long as the file names sort correctly.

- [ ] True
- [ ] False

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** False

**Explanation:** Tests must be independent: never rely on order or on state left by another test. Each test should create its own data and clean up, and you can verify by running a test alone.
</details>

## Part 3: Code Prediction

### 35. A local server returns `404` with a JSON body for `/missing`. What does this print?

```python
import requests
r = requests.get(BASE + "/missing", timeout=3)
print(r.status_code, r.ok)
```

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** `404 False`

**Explanation:** No exception is raised for a 404. `status_code` is `404` and `ok` is `False` because 404 is not below 400.
</details>

### 36. The same server returns `204` with an empty body for `/empty`. What does this print?

```python
import requests
r = requests.get(BASE + "/empty", timeout=3)
print(r.status_code, repr(r.text))
try:
    r.json()
except ValueError as e:
    print("ValueError", type(e).__name__)
```

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** ```
204 ''
ValueError JSONDecodeError
```

**Explanation:** The body is empty, so `.json()` raises `requests.exceptions.JSONDecodeError`, which inherits from the built-in `ValueError` and is therefore caught by `except ValueError`.
</details>

### 37. The `/slow` endpoint sleeps 2 seconds before answering. What does this print?

```python
import requests
try:
    requests.get(BASE + "/slow", timeout=0.5)
except requests.exceptions.Timeout as e:
    print(type(e).__name__, isinstance(e, requests.exceptions.ConnectionError))
```

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** `ReadTimeout False`

**Explanation:** The connection succeeded but data arrived too late, so `ReadTimeout` is raised. A `ReadTimeout` is not a `ConnectionError`; only `ConnectTimeout` is a subclass of both `ConnectionError` and `Timeout`.
</details>

### 38. `/user` returns `{"id": 1, "name": "Ann", "email": null}`. What does this print?

```python
d = requests.get(BASE + "/user", timeout=3).json()
print(d.get("phone"), d.get("email"), "email" in d, "phone" in d)
```

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** `None None True False`

**Explanation:** `.get()` returns `None` for a missing key (`phone`) and for a key that is present with `null` (`email`). The `in` operator tells them apart: `email` exists, `phone` does not.
</details>

### 39. What does this print? (No network access happens.)

```python
import requests
s = requests.Session()
s.headers.update({"Accept": "application/json", "X-Env": "qa"})
req = requests.Request("POST", "http://x.test/a",
                       headers={"X-Env": "prod"}, json={"a": 1})
p = s.prepare_request(req)
print(p.headers["Accept"], p.headers["X-Env"], p.headers["Content-Type"])
```

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** `application/json prod application/json`

**Explanation:** Session headers are merged into each request, and a per-call header overrides the session value (`X-Env` is `prod`). `json=` set `Content-Type` automatically.
</details>

### 40. What does this print? (No network access happens.)

```python
import requests
p1 = requests.Request("POST", "http://x.test/a", data={"a": 1}).prepare()
p2 = requests.Request("POST", "http://x.test/a", json={"a": 1}).prepare()
print(p1.headers["Content-Type"], p1.body)
print(p2.headers["Content-Type"], p2.body)
```

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** ```
application/x-www-form-urlencoded a=1
application/json b'{"a": 1}'
```

**Explanation:** `data=` with a dict builds a form body, while `json=` serialises JSON and sets the JSON content type. Note the JSON body is bytes.
</details>

### 41. What is the value of the `Authorization` header this request will send? (`dXNlcjpwYXNz` is the Base64 of `user:pass`.)

```python
import requests
p = requests.Request("GET", "http://x.test/me", auth=("user", "pass")).prepare()
print(p.headers["Authorization"])
```

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** `Basic dXNlcjpwYXNz`

**Explanation:** `auth=(user, password)` produces `Authorization: Basic <Base64(user:password)>`.
</details>

### 42. What does this print, using the `jsonschema` library?

```python
from jsonschema import validate, ValidationError
schema = {"type": "object", "required": ["id", "name"],
          "properties": {"id": {"type": "integer"}, "name": {"type": "string"}}}
print(validate({"id": 1, "name": "A"}, schema))
for inst in ({"id": "1", "name": "A"}, {"id": 1}):
    try:
        validate(inst, schema)
        print("ok")
    except ValidationError as e:
        print("invalid:", e.validator)
```

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** ```
None
invalid: type
invalid: required
```

**Explanation:** A valid instance makes `validate` return `None`. `"1"` is a string, so the `type` rule fails. The second instance lacks `name`, so `required` fails.
</details>

### 43. Run with `pytest -s -q`. In what order are the lines printed for the single test?

```python
import pytest

@pytest.fixture
def a():
    print("setup a"); yield "A"; print("teardown a")

@pytest.fixture
def b(a):
    print("setup b"); yield a + "B"; print("teardown b")

def test_x(b):
    print("test", b)
```

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** ```
setup a
setup b
test AB
teardown b
teardown a
```

**Explanation:** Fixture `b` depends on `a`, so `a` is set up first. Teardown runs in reverse order of setup: `b` before `a`.
</details>

### 44. Run with `pytest -s -q`. How many times is each of `[login]` and `[fn]` printed?

```python
import pytest

@pytest.fixture(scope="module")
def tok():
    print("[login]"); return "t"

@pytest.fixture
def fn():
    print("[fn]"); return 1

def test_1(tok, fn): pass
def test_2(tok, fn): pass
def test_3(tok, fn): pass
```

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** `[login]` once, `[fn]` three times

**Explanation:** A `module`-scoped fixture is built once per file, while the default `function` scope rebuilds the fixture for every test that requests it.
</details>

### 45. How many tests are collected, and which ID does the third `test_p` case get?

```python
import pytest

@pytest.mark.parametrize("code,ok", [
    (200, True),
    (404, False),
    pytest.param(500, False, id="server"),
])
def test_p(code, ok):
    assert (code < 400) == ok
```

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** 3 tests; the third is `test_p[server]` (the others are `test_p[200-True]` and `test_p[404-False]`)

**Explanation:** Each tuple becomes a test. Automatic IDs join the values with a dash, while `pytest.param(..., id="server")` replaces the generated name with a readable one.
</details>

### 46. Stacked decorators. How many tests are collected, and which of these IDs exists: `test_s[1-a]` or `test_s[a-1]`?

```python
import pytest

@pytest.mark.parametrize("x", [1, 2])
@pytest.mark.parametrize("y", ["a", "b"])
def test_s(x, y):
    pass
```

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** 4 tests (all combinations); the ID `test_s[a-1]` exists, `test_s[1-a]` does not

**Explanation:** Stacking creates every combination (2 x 2 = 4). The decorator closest to the function (`y`) comes first in the ID, giving `a-1`, `b-1`, `a-2`, `b-2`.
</details>

### 47. Run with plain `pytest -q`. What is the summary line?

```python
import pytest

def test_float():
    assert 0.1 + 0.2 == 0.3

def test_approx():
    assert 0.1 + 0.2 == pytest.approx(0.3)

@pytest.mark.xfail(reason="known bug")
def test_bug():
    assert 1 == 2
```

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** `1 failed, 1 passed, 1 xfailed`

**Explanation:** Computed floats should not be compared with `==` (the first test fails); `pytest.approx` passes. The failing `xfail` test is reported as expected failure (xfailed), not as a failure.
</details>

### 48. Run with `pytest -q`. What is the summary line, and what is the difference between the two outcomes?

```python
import pytest

@pytest.fixture
def boom():
    raise RuntimeError("x")

def test_err(boom):
    pass

def test_fail():
    assert 1 == 2
```

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** `1 failed, 1 error`

**Explanation:** A fixture that raises is reported as ERROR (the problem is in the setup), while a failing assertion in the test is FAILED. This difference helps triage where the bug is.
</details>

## Part 4: Fill-in-the-Blank

### 49. To make a `requests` call raise `HTTPError` for 4xx/5xx responses, call `response.______()`.

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** `raise_for_status`

**Explanation:** It is best used in setup code, while tests assert exact status codes.
</details>

### 50. A bearer token is sent as `Authorization: ______ <token>`.

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** `Bearer`

**Explanation:** The scheme name `Bearer` tells the server the credential is a token obtained from a login call.
</details>

### 51. A valid user who lacks permission receives status ______, while an unauthenticated one receives status ______.

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** `403`, then `401`

**Explanation:** `403` means "I know you, and no"; `401` means "who are you?".
</details>

### 52. In a `jsonschema` schema, the keyword listing the keys that must be present is `______`.

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** `required`

**Explanation:** `type`, `required` and `properties` together describe the shape of an object.
</details>

### 53. A fixture that must clean up after the test uses the `______` keyword instead of `return`.

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** `yield`

**Explanation:** Everything before `yield` is setup; everything after is teardown and runs even if the test fails.
</details>

### 54. The PyTest option `-______ smoke` selects tests by marker.

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** `m`

**Explanation:** `-m` selects by marker, `-k` by a keyword in the name.
</details>

### 55. After a `429` response, read the ______ header to know how long to wait.

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** `Retry-After`

**Explanation:** Cap the wait and the number of retries, and never hide the `429` when rate limiting is what you are testing.
</details>

### 56. Calling `response.json()` on an HTML page raises `______`, which is also a subclass of Python's built-in `ValueError`.

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** `JSONDecodeError` (`requests.exceptions.JSONDecodeError`)

**Explanation:** Wrap parsing in a helper such as `safe_json` that reports status, content type and the start of the body.
</details>

## Part 5: Matching

### 57. Match each status code (1-5) with the best testing guidance (A-E).

| # | Left | | Right |
|---|------|-|-------|
| 1 | `201` | A | Check the `Retry-After` header |
| 2 | `204` | B | Check the `Allow` header |
| 3 | `304` | C | Empty body: do not call `.json()` |
| 4 | `405` | D | Check the `Location` header and the new id |
| 5 | `429` | E | Result of a conditional `GET` |

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** 1 -> D, 2 -> C, 3 -> E, 4 -> B, 5 -> A

**Explanation:** `201`: check `Location`. `204`: empty body, no `.json()`. `304`: conditional `GET`. `405`: check `Allow`. `429`: `Retry-After`.
</details>

### 58. Match each fixture scope (1-4) with when its value is created and discarded (A-D).

| # | Left | | Right |
|---|------|-|-------|
| 1 | `function` | A | Once per test class |
| 2 | `class` | B | Once per `.py` file |
| 3 | `module` | C | Once per whole `pytest` run |
| 4 | `session` | D | Before each test that requests it |

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** 1 -> D, 2 -> A, 3 -> B, 4 -> C

**Explanation:** The default `function` scope rebuilds per test; `class` per test class; `module` per file; `session` once per run, which suits expensive read-only setup like a login token.
</details>

### 59. Match each `requests` exception (1-5) with its cause (A-E).

| # | Left | | Right |
|---|------|-|-------|
| 1 | `HTTPError` | A | A redirect loop (default limit 30) |
| 2 | `ConnectionError` | B | `response.json()` called on a non-JSON body |
| 3 | `ReadTimeout` | C | The server was too slow to send data |
| 4 | `TooManyRedirects` | D | Raised by `raise_for_status()` on 4xx/5xx |
| 5 | `JSONDecodeError` | E | The server cannot be reached (DNS, refused, reset) |

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** 1 -> D, 2 -> E, 3 -> C, 4 -> A, 5 -> B

**Explanation:** These are the exception family members from the `requests` lesson; all inherit from `RequestException`.
</details>
