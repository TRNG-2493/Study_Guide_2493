# Handout 03 – From Requests to PyTest

> **How to use this handout:** each topic is a small, self-contained example in its own folder. Nothing carries over from one topic to the next. You will combine everything in **Handout 11 (Week 7 Mini-Project)**.

**Before class – set up once**

```bash
mkdir week7-demos && cd week7-demos
python -m venv .venv
# Windows: .venv\Scripts\activate    macOS/Linux: source .venv/bin/activate
pip install requests pytest
```

Practice API: `https://jsonplaceholder.typicode.com` (free, no login, **fakes** writes).

---

## Topic 1 – Python Requests Library

📁 Folder: `03-1-requests/`

### Definition

`requests` is the most popular Python library for sending HTTP requests. It turns everything you did in curl and Postman into Python code: `requests.get(url)` sends a GET and returns a **`Response` object**. That object holds the status code, headers and body, so your code can make decisions and assertions about them. Unlike Postman, code can loop, branch, read files and run in CI. One important rule: `requests` **never times out by default**, so always pass `timeout=`.

### Key ideas

| You want to send | Use | Example |
|---|---|---|
| Query parameters | `params=` | `params={"userId": 1}` |
| A JSON body (also sets `Content-Type`) | `json=` | `json={"title": "x"}` |
| A form body | `data=` | `data={"user": "ana"}` |
| Headers | `headers=` | `headers={"Accept": "application/json"}` |

| You want to read | Use |
|---|---|
| Status | `r.status_code`, `r.ok`, `r.reason` |
| Body | `r.json()`, `r.text` |
| Headers / timing / final URL | `r.headers["Content-Type"]`, `r.elapsed`, `r.url` |

### Worked example – Exploring an API from Python

Create `explore.py`. Add each step and run `python explore.py` after each one.

**Step 1 – Send a GET.**

```python
import requests

BASE = "https://jsonplaceholder.typicode.com"

r = requests.get(f"{BASE}/posts/1", timeout=5)
print(r.status_code, r.reason)
```

**Step 2 – Read the headers and body.**

```python
print(r.headers["Content-Type"])
post = r.json()
print(post["title"])
```

**Step 3 – Pass query parameters.**

```python
r = requests.get(f"{BASE}/posts", params={"userId": 2}, timeout=5)
print(r.url)
print(len(r.json()))
```

**Step 4 – POST a JSON body.**

```python
r = requests.post(f"{BASE}/posts",
                  json={"title": "from python", "body": "hi", "userId": 1},
                  timeout=5)
print(r.status_code, r.json())
```

**Step 5 – Handle failures with exceptions.**

```python
try:
    r = requests.get(f"{BASE}/posts/9999", timeout=5)
    r.raise_for_status()
except requests.HTTPError as e:
    print("HTTP error:", e)
except requests.Timeout:
    print("Server too slow")
```

### Final code

**`explore.py`**

```python
import requests

BASE = "https://jsonplaceholder.typicode.com"

# Step 1 – send a GET
r = requests.get(f"{BASE}/posts/1", timeout=5)
print(r.status_code, r.reason)

# Step 2 – read the headers and body
print(r.headers["Content-Type"])
post = r.json()
print(post["title"])

# Step 3 – pass query parameters
r = requests.get(f"{BASE}/posts", params={"userId": 2}, timeout=5)
print(r.url)
print(len(r.json()))

# Step 4 – POST a JSON body
r = requests.post(f"{BASE}/posts",
                  json={"title": "from python", "body": "hi", "userId": 1},
                  timeout=5)
print(r.status_code, r.json())

# Step 5 – handle failures with exceptions
try:
    r = requests.get(f"{BASE}/posts/9999", timeout=5)
    r.raise_for_status()
except requests.HTTPError as e:
    print("HTTP error:", e)
except requests.Timeout:
    print("Server too slow")
```

### How to run

```bash
cd week7-demos/03-1-requests
python explore.py
```

### Checkpoint

```
200 OK
application/json; charset=utf-8
sunt aut facere repellat provident occaecati excepturi optio reprehenderit
https://jsonplaceholder.typicode.com/posts?userId=2
10
201 {'title': 'from python', 'body': 'hi', 'userId': 1, 'id': 101}
HTTP error: 404 Client Error: Not Found for url: https://jsonplaceholder.typicode.com/posts/9999
```

### Your turn

1. Send a `PUT` to `/posts/1` with a full body and print the status code and the returned `title`.
2. Use a `requests.Session()` to set `Accept: application/json` once, then make two GETs with it.
3. Call `https://httpbin.org/delay/3` with `timeout=1`. Which exception is raised?
4. Print `r.request.method`, `r.request.url` and `r.request.headers` for your POST from Step 4. What `Content-Type` did `json=` set?

### Common errors

- **No `timeout=`.** A slow server makes your script hang forever. Always pass a timeout.
- **`data=` vs `json=`.** `data={"a": 1}` sends form data, not JSON. Use `json=` for JSON APIs.
- **Calling `r.json()` on an HTML error page.** It raises `JSONDecodeError`. Check the status code and `Content-Type` first.

---

## Topic 2 – PyTest API Test Structure

📁 Folder: `03-2-pytest/`

### Definition

**PyTest** is a Python test runner. It **discovers** test files and functions by name, **runs** them, and **reports** the results. A test is an ordinary function named `test_...` that uses a plain `assert`. When an assertion fails, PyTest shows the values involved (this is called *assertion introspection*). A clear folder layout, the **Arrange–Act–Assert** pattern and **markers** keep a test suite readable as it grows.

### Key ideas

```
03-2-pytest/
├── pytest.ini         # PyTest settings and markers
└── tests/
    └── test_posts.py  # file names start with test_
```

- **Discovery rules:** files `test_*.py`, functions `test_*`, classes `Test*` (with no `__init__`).
- **AAA:** *Arrange* (prepare data) → *Act* (send one request) → *Assert* (check the result).
- **Useful flags:** `-v` (verbose), `-q` (quiet), `-k name` (filter by name), `-m smoke` (filter by marker), `-x` (stop at the first failure), `--collect-only`.

### Worked example – Your first API test file

**Step 1 – Create `pytest.ini` and register markers.**

```ini
[pytest]
testpaths = tests
markers =
    smoke: quick health checks
    regression: full functional coverage
```

**Step 2 – Create `tests/test_posts.py` with one test in AAA form.**

```python
import pytest
import requests

BASE = "https://jsonplaceholder.typicode.com"


def test_get_post_returns_200():
    # Arrange
    url = f"{BASE}/posts/1"
    # Act
    response = requests.get(url, timeout=5)
    # Assert
    assert response.status_code == 200
```

**Step 3 – Run it.**

```bash
pytest -v
```

**Step 4 – Add a second test with a marker and a helpful failure message.**

```python
@pytest.mark.smoke
def test_post_has_expected_id():
    response = requests.get(f"{BASE}/posts/1", timeout=5)
    body = response.json()
    assert body["id"] == 1, f"Unexpected body: {body}"
```

**Step 5 – Run only the smoke tests.**

```bash
pytest -v -m smoke
```

### Final code

**`pytest.ini`**

```ini
[pytest]
testpaths = tests
markers =
    smoke: quick health checks
    regression: full functional coverage
```

**`tests/test_posts.py`**

```python
import pytest
import requests

BASE = "https://jsonplaceholder.typicode.com"


def test_get_post_returns_200():
    # Arrange
    url = f"{BASE}/posts/1"
    # Act
    response = requests.get(url, timeout=5)
    # Assert
    assert response.status_code == 200


@pytest.mark.smoke
def test_post_has_expected_id():
    response = requests.get(f"{BASE}/posts/1", timeout=5)
    body = response.json()
    assert body["id"] == 1, f"Unexpected body: {body}"
```

### How to run

```bash
cd week7-demos/03-2-pytest
pytest -v              # all tests
pytest -v -m smoke     # only the smoke tests
```

### Checkpoint

```
tests/test_posts.py::test_get_post_returns_200 PASSED      [ 50%]
tests/test_posts.py::test_post_has_expected_id PASSED      [100%]
============== 2 passed in 0.6s ==============
```

With `-m smoke`, you should see `1 passed, 1 deselected`.

### Your turn

1. Change the expected id in `test_post_has_expected_id` to `2` and run it. Read the failure output: what does introspection show you?
2. Add a test for `GET /users` that asserts there are 10 users, and mark it `regression`.
3. Rename a test to `check_users()` and run `pytest --collect-only`. What happens, and why?
4. Add `@pytest.mark.skip(reason="API not ready")` to one test and run `pytest -rA`. Where is the reason shown?

### Common errors

- **`PytestUnknownMarkWarning`.** You used a marker that is not registered in `pytest.ini`.
- **The test file is named `posts_test.py` or `tests.py`.** PyTest does not discover it. Use `test_*.py`.
- **Tests that depend on each other's order.** Every test must be able to run alone.

---

## Topic 3 – HTTP Requests from Automated Tests

📁 Folder: `03-3-client/`

### Definition

Automated tests send requests **from code**, which brings new responsibilities. The base URL and timeouts should come from **environment variables**, so the same tests can run against dev, test or staging. A small **`ApiClient`** class wraps a `requests.Session`: it adds a timeout to every call and builds full URLs, so the tests stay short. Tests that create data must also **clean it up**, and they must never depend on running in a particular order.

### Key ideas

- **Config from the environment:** `os.getenv("BASE_URL", "https://jsonplaceholder.typicode.com")`.
- **Exceptions to know:** `ConnectTimeout` (the server could not be reached in time), `ReadTimeout` (the server connected but answered too slowly), `ConnectionError` (DNS failure or connection refused).
- **The client never asserts.** It returns the raw response, so a test can still *expect* a `404`.
- **JSONPlaceholder fakes writes**, so a CRUD test should check each response on its own and not rely on the data persisting.

### Worked example – A tiny client and a CRUD test

```
03-3-client/
├── api_client.py
└── test_crud.py
```

**Step 1 – Read the config from the environment** (`api_client.py`).

```python
import os
import requests

BASE_URL = os.getenv("BASE_URL", "https://jsonplaceholder.typicode.com")
TIMEOUT = float(os.getenv("API_TIMEOUT", "5"))
```

**Step 2 – Create the client class.**

```python
class ApiClient:
    def __init__(self, base_url=BASE_URL, timeout=TIMEOUT):
        self.base_url = base_url.rstrip("/")
        self.timeout = timeout
        self.session = requests.Session()
        self.session.headers.update({"Accept": "application/json"})
```

**Step 3 – Add one method that sends every request, plus shortcuts.**

```python
    def request(self, method, path, **kwargs):
        kwargs.setdefault("timeout", self.timeout)
        url = f"{self.base_url}/{path.lstrip('/')}"
        return self.session.request(method, url, **kwargs)

    def get(self, path, **kw):    return self.request("GET", path, **kw)
    def post(self, path, **kw):   return self.request("POST", path, **kw)
    def put(self, path, **kw):    return self.request("PUT", path, **kw)
    def delete(self, path, **kw): return self.request("DELETE", path, **kw)
```

**Step 4 – Write a CRUD test that uses the client** (`test_crud.py`).

```python
from api_client import ApiClient

api = ApiClient()


def test_post_crud_flow():
    created = api.post("/posts", json={"title": "t", "body": "b", "userId": 1})
    assert created.status_code == 201
    assert created.json()["id"]

    updated = api.put("/posts/1", json={"id": 1, "title": "t2", "body": "b", "userId": 1})
    assert updated.status_code == 200
    assert updated.json()["title"] == "t2"

    deleted = api.delete("/posts/1")
    assert deleted.status_code in (200, 204)
```

### Final code

**`api_client.py`**

```python
import os
import requests

BASE_URL = os.getenv("BASE_URL", "https://jsonplaceholder.typicode.com")
TIMEOUT = float(os.getenv("API_TIMEOUT", "5"))


class ApiClient:
    def __init__(self, base_url=BASE_URL, timeout=TIMEOUT):
        self.base_url = base_url.rstrip("/")
        self.timeout = timeout
        self.session = requests.Session()
        self.session.headers.update({"Accept": "application/json"})

    def request(self, method, path, **kwargs):
        kwargs.setdefault("timeout", self.timeout)
        url = f"{self.base_url}/{path.lstrip('/')}"
        return self.session.request(method, url, **kwargs)

    def get(self, path, **kw):    return self.request("GET", path, **kw)
    def post(self, path, **kw):   return self.request("POST", path, **kw)
    def put(self, path, **kw):    return self.request("PUT", path, **kw)
    def delete(self, path, **kw): return self.request("DELETE", path, **kw)
```

**`test_crud.py`**

```python
from api_client import ApiClient

api = ApiClient()


def test_post_crud_flow():
    created = api.post("/posts", json={"title": "t", "body": "b", "userId": 1})
    assert created.status_code == 201
    assert created.json()["id"]

    updated = api.put("/posts/1", json={"id": 1, "title": "t2", "body": "b", "userId": 1})
    assert updated.status_code == 200
    assert updated.json()["title"] == "t2"

    deleted = api.delete("/posts/1")
    assert deleted.status_code in (200, 204)
```

### How to run

```bash
cd week7-demos/03-3-client
pytest -v test_crud.py
```

Then point the test at an unreachable host to see the timeout work:

```bash
# bash
BASE_URL=http://10.255.255.1 API_TIMEOUT=2 pytest -q test_crud.py
# PowerShell
$env:BASE_URL="http://10.255.255.1"; $env:API_TIMEOUT="2"; pytest -q test_crud.py
```

(In PowerShell, clear the variables afterwards with `Remove-Item Env:BASE_URL, Env:API_TIMEOUT`.)

### Checkpoint

The first command shows:

```
test_crud.py::test_post_crud_flow PASSED   [100%]
```

With the unreachable host, the test fails **fast** instead of hanging: you should see `ConnectTimeout` within about 2 seconds.

### Your turn

1. Add a `patch()` method to `ApiClient` and write a test that PATCHes `/posts/1` with a new title.
2. Write a test that sends `params={"userId": 3}` through `api.get` and asserts that every post has `userId == 3`.
3. Add a response-time assertion: `assert r.elapsed.total_seconds() < 2`. Why is a generous threshold better than a tight one?
4. Explain in one sentence why the client must not call `raise_for_status()` itself.

---

## Topic 4 – Status Code Validation

📁 Folder: `03-4-status/`

### Definition

The **status code** is the server's three-digit verdict on a request, and it is usually the **first assertion** in an API test. Testers check both **positive** cases (valid input gives the documented success code) and **negative** cases (bad input gives the documented error code). A good assertion is **exact** where the specification is exact, and its failure message includes enough context (method, URL, body) to debug without rerunning. Remember that `200` alone does not prove the response is correct, so the body must be checked too.

### Key ideas

| Code | Meaning | A tester checks |
|------|---------|-----------------|
| 200 / 201 / 204 | OK / Created / No Content | 201 for POST; 204 has an **empty** body |
| 400 / 422 | Bad input | The error body explains which field |
| 401 / 403 | Not authenticated / Not allowed | No data is leaked in the body |
| 404 | Not found | A wrong id gives 404, not 500 |
| 429 | Too many requests | A `Retry-After` header is present |
| 500 / 503 | Server error | Never acceptable for client mistakes |

- **`r.ok`** is true for any code below 400. It is too loose for a test assertion.
- **The "assert only 200" anti-pattern:** a test that passes on any `200`, even when the body is wrong.

### Worked example – A reusable `assert_status` helper

```
03-4-status/
├── assertions.py
└── test_status.py
```

**Step 1 – Start with a plain exact assertion** (`test_status.py`).

```python
import requests

BASE = "https://jsonplaceholder.typicode.com"


def test_get_post_ok():
    r = requests.get(f"{BASE}/posts/1", timeout=5)
    assert r.status_code == 200
```

**Step 2 – Create `assertions.py` with a helper that explains failures.**

```python
def assert_status(response, expected):
    req = response.request
    assert response.status_code == expected, (
        f"{req.method} {req.url} → expected {expected}, "
        f"got {response.status_code}. Body: {response.text[:200]}"
    )
```

**Step 3 – Use the helper in a positive test.**

```python
from assertions import assert_status


def test_create_post_returns_201():
    r = requests.post(f"{BASE}/posts", json={"title": "t", "body": "b", "userId": 1}, timeout=5)
    assert_status(r, 201)
```

**Step 4 – Add negative tests.**

```python
def test_missing_post_returns_404():
    assert_status(requests.get(f"{BASE}/posts/9999", timeout=5), 404)


def test_unknown_route_returns_404():
    assert_status(requests.get(f"{BASE}/not-a-resource", timeout=5), 404)
```

**Step 5 – Break one test on purpose** (expect `200` for `/posts/9999`) and read the message.

### Final code

**`assertions.py`**

```python
def assert_status(response, expected):
    req = response.request
    assert response.status_code == expected, (
        f"{req.method} {req.url} → expected {expected}, "
        f"got {response.status_code}. Body: {response.text[:200]}"
    )
```

**`test_status.py`**

```python
import requests
from assertions import assert_status

BASE = "https://jsonplaceholder.typicode.com"


def test_get_post_ok():
    r = requests.get(f"{BASE}/posts/1", timeout=5)
    assert r.status_code == 200


def test_create_post_returns_201():
    r = requests.post(f"{BASE}/posts", json={"title": "t", "body": "b", "userId": 1}, timeout=5)
    assert_status(r, 201)


def test_missing_post_returns_404():
    assert_status(requests.get(f"{BASE}/posts/9999", timeout=5), 404)


def test_unknown_route_returns_404():
    assert_status(requests.get(f"{BASE}/not-a-resource", timeout=5), 404)
```

### How to run

```bash
cd week7-demos/03-4-status
pytest -q
```

To see the helper's message (Step 5), change `404` to `200` in `test_missing_post_returns_404`, run `pytest -q` again, then change it back.

### Checkpoint

The broken test prints a message you can act on without rerunning:

```
AssertionError: GET https://jsonplaceholder.typicode.com/posts/9999 → expected 200, got 404. Body: {}
```

Fix it again, and `pytest -q` shows `4 passed`.

### Your turn

1. Write a negative-test table (input, expected code) for `POST /posts` on a **real** API: missing title, wrong type, empty body, no auth.
2. Add an `assert_status_in(response, allowed)` helper that accepts a list, and use it for `DELETE` (`200` or `204`).
3. Explain the difference between `r.ok`, `r.status_code == 200` and `r.raise_for_status()`, and say which one belongs in a test assertion.
4. Your test gets `429` with `Retry-After: 2`. Describe how a test should react without becoming flaky.

### Common errors

- **`assert r.ok`.** It passes for `204` and `302`, and on a `500` it fails with a message that tells you nothing about what went wrong.
- **Checking only the status code.** Always add at least one body check, which is the next lecture's topic.
- **Expecting `404` from JSONPlaceholder's fake writes.** Reading `/posts/101` after a POST returns `404` because writes are faked. That is not a defect in your test.

---

## Answers

<details>
<summary><strong>Topic 1 – Python Requests Library</strong></summary>

1. ```python
   r = requests.put(f"{BASE}/posts/1",
                    json={"id": 1, "title": "new", "body": "b", "userId": 1}, timeout=5)
   print(r.status_code, r.json()["title"])   # 200 new
   ```
2. ```python
   s = requests.Session()
   s.headers.update({"Accept": "application/json"})
   print(s.get(f"{BASE}/posts/1", timeout=5).status_code)
   print(s.get(f"{BASE}/users/1", timeout=5).status_code)
   ```
3. `requests.exceptions.ReadTimeout` (a subclass of `Timeout`).
4. `json=` set `Content-Type: application/json`.

</details>

<details>
<summary><strong>Topic 2 – PyTest API Test Structure</strong></summary>

1. PyTest shows `assert 1 == 2`, the custom message with the full body, and the source line that failed.
2. ```python
   @pytest.mark.regression
   def test_users_count():
       r = requests.get(f"{BASE}/users", timeout=5)
       assert len(r.json()) == 10
   ```
3. It is not collected, because the name does not start with `test_`. It silently never runs.
4. In the short test summary, the `SKIPPED` line shows the reason.

</details>

<details>
<summary><strong>Topic 3 – HTTP Requests from Automated Tests</strong></summary>

1. ```python
   def patch(self, path, **kw): return self.request("PATCH", path, **kw)

   def test_patch_title():
       r = api.patch("/posts/1", json={"title": "patched"})
       assert r.status_code == 200
       assert r.json()["title"] == "patched"
   ```
2. ```python
   def test_filter_by_user():
       r = api.get("/posts", params={"userId": 3})
       assert r.status_code == 200
       assert r.json(), "expected at least one post"
       assert all(p["userId"] == 3 for p in r.json())
   ```
3. Network speed varies, especially in CI. A tight threshold makes the test fail randomly (flaky). A generous one still catches a real slowdown.
4. If the client raised on every `4xx`, a test that *expects* `404` could not work.

</details>

<details>
<summary><strong>Topic 4 – Status Code Validation</strong></summary>

1. | Input | Expected |
   |---|---|
   | Missing `title` | 400 or 422 |
   | `userId: "abc"` | 400 or 422 |
   | Empty body | 400 |
   | No `Authorization` header | 401 |
2. ```python
   def assert_status_in(response, allowed):
       assert response.status_code in allowed, (
           f"{response.request.method} {response.request.url} → expected one of "
           f"{allowed}, got {response.status_code}")

   def test_delete():
       assert_status_in(requests.delete(f"{BASE}/posts/1", timeout=5), (200, 204))
   ```
3. `r.ok` is true for any code below 400 (too loose). `r.status_code == 200` is an exact check (use this in assertions). `raise_for_status()` raises an exception for `4xx` and `5xx`, which suits scripts but not negative tests.
4. Wait for `Retry-After` seconds and retry a **bounded** number of times (for example twice). If it still fails, fail with a clear message. Never retry forever, and never hide the 429.

</details>
