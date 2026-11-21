# Handout 04 – Validating, Authenticating & Reusing

> **How to use this handout:** each topic is a small, self-contained example in its own folder inside `week7-demos/`. Nothing carries over from one topic to the next. You will combine everything in **Handout 11 (Week 7 Mini-Project)**.

**Before class**

- Activate your `week7-demos` virtual environment and run: `pip install requests pytest jsonschema python-dotenv`
- Practice APIs: `https://jsonplaceholder.typicode.com` and `https://httpbin.org`.

---

## Topic 5 – JSON Response Validation

📁 Folder: `04-5-json/`, file `test_json.py`

### Definition

A `200 OK` only means the server *answered*. It does not mean the answer is *correct*. **JSON response validation** checks the body itself, layer by layer: Is it valid JSON? Are the fields **present**? Do they have the right **type**? Are the **values**, formats and ranges correct? `response.json()` turns the body into Python dicts and lists, so plain `assert` statements can check any part of it. A **JSON Schema** describes the expected shape once, so it can be reused in many tests.

### Key ideas

| JSON | Python | Watch out for |
|------|--------|---------------|
| object `{}` | `dict` | A missing key raises `KeyError`, so use `.get()` when the field is optional |
| array `[]` | `list` | An empty list is a valid answer |
| `true`/`false` | `True`/`False` | `isinstance(True, int)` is **True** |
| `null` | `None` | Check with `is None`, not `== ""` |
| number | `int` / `float` | Compare floats with `pytest.approx` |

- **Checking lists:** test the length, that *every* item matches (`all(...)`), that *at least one* matches (`any(...)`), and uniqueness.
- **Echo check:** after a POST, check that the response contains what you sent.

### Worked example – Validating a user and a list of posts

**Step 1 – Check that the body is JSON and the fields are present.**

```python
import requests

BASE = "https://jsonplaceholder.typicode.com"


def test_user_has_required_fields():
    r = requests.get(f"{BASE}/users/1", timeout=5)
    assert r.headers["Content-Type"].startswith("application/json")
    user = r.json()
    for field in ("id", "name", "email", "address"):
        assert field in user, f"missing {field}"
```

**Step 2 – Check types and formats.** Add these lines to the same test.

```python
    assert isinstance(user["id"], int) and not isinstance(user["id"], bool)
    assert isinstance(user["name"], str) and user["name"]
    assert "@" in user["email"]
```

**Step 3 – Check nested values.**

```python
    geo = user["address"]["geo"]
    assert -90 <= float(geo["lat"]) <= 90
```

**Step 4 – Check a list.**

```python
def test_posts_for_user():
    posts = requests.get(f"{BASE}/posts", params={"userId": 1}, timeout=5).json()
    assert len(posts) == 10
    assert all(p["userId"] == 1 for p in posts)
    ids = [p["id"] for p in posts]
    assert len(ids) == len(set(ids)), "duplicate ids"
```

**Step 5 – Do an echo check, then validate against a schema.**

```python
from jsonschema import validate

POST_SCHEMA = {
    "type": "object",
    "required": ["id", "title", "body", "userId"],
    "properties": {
        "id": {"type": "integer"},
        "title": {"type": "string"},
        "body": {"type": "string"},
        "userId": {"type": "integer"},
    },
}


def test_create_post_echo_and_schema():
    payload = {"title": "t", "body": "b", "userId": 1}
    body = requests.post(f"{BASE}/posts", json=payload, timeout=5).json()
    assert payload.items() <= body.items()      # everything we sent came back
    validate(instance=body, schema=POST_SCHEMA)
```

### Final code

**`test_json.py`**

```python
import requests
from jsonschema import validate

BASE = "https://jsonplaceholder.typicode.com"

POST_SCHEMA = {
    "type": "object",
    "required": ["id", "title", "body", "userId"],
    "properties": {
        "id": {"type": "integer"},
        "title": {"type": "string"},
        "body": {"type": "string"},
        "userId": {"type": "integer"},
    },
}


def test_user_has_required_fields():
    r = requests.get(f"{BASE}/users/1", timeout=5)
    assert r.headers["Content-Type"].startswith("application/json")
    user = r.json()
    for field in ("id", "name", "email", "address"):
        assert field in user, f"missing {field}"

    assert isinstance(user["id"], int) and not isinstance(user["id"], bool)
    assert isinstance(user["name"], str) and user["name"]
    assert "@" in user["email"]

    geo = user["address"]["geo"]
    assert -90 <= float(geo["lat"]) <= 90


def test_posts_for_user():
    posts = requests.get(f"{BASE}/posts", params={"userId": 1}, timeout=5).json()
    assert len(posts) == 10
    assert all(p["userId"] == 1 for p in posts)
    ids = [p["id"] for p in posts]
    assert len(ids) == len(set(ids)), "duplicate ids"


def test_create_post_echo_and_schema():
    payload = {"title": "t", "body": "b", "userId": 1}
    body = requests.post(f"{BASE}/posts", json=payload, timeout=5).json()
    assert payload.items() <= body.items()      # everything we sent came back
    validate(instance=body, schema=POST_SCHEMA)
```

### How to run

```bash
cd week7-demos/04-5-json
pytest -v test_json.py
```

### Checkpoint

```
test_json.py::test_user_has_required_fields PASSED
test_json.py::test_posts_for_user PASSED
test_json.py::test_create_post_echo_and_schema PASSED
============== 3 passed ==============
```

### Your turn

1. Change `"userId": {"type": "integer"}` to `"string"` in the schema. Run the test and copy the first line of the `ValidationError`.
2. Write a test for `/comments?postId=1` that checks every comment has an email containing `@`, and that at least one `name` contains more than three words.
3. Write a `safe_json(response)` helper that turns a `JSONDecodeError` into a clear `AssertionError` that includes the status code and the first 200 characters of the body.
4. Why does `assert user.get("phone") is not None` give a better message than `assert user["phone"]` when the key is missing?

### Common errors

- **`KeyError: 'name'`.** The path is wrong or the field is missing. Print `r.json()` once to see the real structure.
- **`TypeError: list indices must be integers`.** You treated a list like a dict. `/users` returns a list, so use `[0]["name"]`.
- **`assert body == expected` on a large object.** It fails on any extra field. Prefer a partial comparison (`items() <=`) or a schema.

---

## Topic 6 – Headers and Authentication

📁 Folder: `04-6-auth/`, file `test_auth.py`

### Definition

**Authentication** answers "who are you?", and failing it gives `401 Unauthorized`. **Authorization** answers "what are you allowed to do?", and failing it gives `403 Forbidden`. APIs usually authenticate with **Basic auth** (username and password in Base64), an **API key** in a header, or a **Bearer token** such as a JWT that you get from a login call. In `requests` you can send headers per call or set them once on a `Session`. Secrets must come from **environment variables**, never from source code.

### Key ideas

| Scheme | `requests` code | Header on the wire |
|--------|-----------------|--------------------|
| Basic | `auth=HTTPBasicAuth("user", "pw")` | `Authorization: Basic dXNlcjpwdw==` |
| API key | `headers={"X-API-Key": key}` | `X-API-Key: abc123` |
| Bearer | `headers={"Authorization": f"Bearer {token}"}` | `Authorization: Bearer eyJ...` |

- **Token flow:** log in once → store the token on a `Session` → every later call sends it automatically.
- **A JWT** has three parts, `header.payload.signature`. You can Base64-decode the payload to inspect it (for example `exp`), but never trust it without verifying the signature.
- **Negative auth tests:** missing, malformed, wrong and expired credentials should give `401`; the wrong role should give `403`.

### Worked example – Basic and Bearer auth with httpbin

**Step 1 – Send a custom header and confirm it arrived.**

```python
import os
import requests
from requests.auth import HTTPBasicAuth

HB = "https://httpbin.org"


def test_custom_header_is_sent():
    r = requests.get(f"{HB}/headers", headers={"X-Request-Id": "qe-1"}, timeout=10)
    assert r.json()["headers"]["X-Request-Id"] == "qe-1"
```

**Step 2 – Test Basic auth, positive and negative.**

```python
def test_basic_auth_ok():
    r = requests.get(f"{HB}/basic-auth/user/passwd",
                     auth=HTTPBasicAuth("user", "passwd"), timeout=10)
    assert r.status_code == 200
    assert r.json() == {"authenticated": True, "user": "user"}


def test_basic_auth_wrong_password():
    r = requests.get(f"{HB}/basic-auth/user/passwd",
                     auth=HTTPBasicAuth("user", "WRONG"), timeout=10)
    assert r.status_code == 401
```

**Step 3 – Read the token from the environment.** Never type it into code.

```python
TOKEN = os.getenv("API_TOKEN", "dev-token-123")
```

**Step 4 – Store the token on a session and reuse it.**

```python
def test_bearer_token_on_session():
    s = requests.Session()
    s.headers.update({"Authorization": f"Bearer {TOKEN}"})
    r = s.get(f"{HB}/bearer", timeout=10)
    assert r.status_code == 200
    assert r.json()["authenticated"] is True
```

**Step 5 – Check that a request with no token is rejected.**

```python
def test_bearer_missing_token():
    r = requests.get(f"{HB}/bearer", timeout=10)
    assert r.status_code == 401
```

### Final code

**`test_auth.py`**

```python
import os
import requests
from requests.auth import HTTPBasicAuth

HB = "https://httpbin.org"
TOKEN = os.getenv("API_TOKEN", "dev-token-123")


def test_custom_header_is_sent():
    r = requests.get(f"{HB}/headers", headers={"X-Request-Id": "qe-1"}, timeout=10)
    assert r.json()["headers"]["X-Request-Id"] == "qe-1"


def test_basic_auth_ok():
    r = requests.get(f"{HB}/basic-auth/user/passwd",
                     auth=HTTPBasicAuth("user", "passwd"), timeout=10)
    assert r.status_code == 200
    assert r.json() == {"authenticated": True, "user": "user"}


def test_basic_auth_wrong_password():
    r = requests.get(f"{HB}/basic-auth/user/passwd",
                     auth=HTTPBasicAuth("user", "WRONG"), timeout=10)
    assert r.status_code == 401


def test_bearer_token_on_session():
    s = requests.Session()
    s.headers.update({"Authorization": f"Bearer {TOKEN}"})
    r = s.get(f"{HB}/bearer", timeout=10)
    assert r.status_code == 200
    assert r.json()["authenticated"] is True


def test_bearer_missing_token():
    r = requests.get(f"{HB}/bearer", timeout=10)
    assert r.status_code == 401
```

### How to run

```bash
cd week7-demos/04-6-auth
# bash
API_TOKEN=my-secret pytest -v test_auth.py
# PowerShell
$env:API_TOKEN="my-secret"; pytest -v test_auth.py
```

### Checkpoint

```
test_auth.py::test_custom_header_is_sent PASSED
test_auth.py::test_basic_auth_ok PASSED
test_auth.py::test_basic_auth_wrong_password PASSED
test_auth.py::test_bearer_token_on_session PASSED
test_auth.py::test_bearer_missing_token PASSED
============== 5 passed ==============
```

Run it once more with `-s` and `print(r.json())` added in Step 4. You should see `"token": "my-secret"`, which proves the value came from the environment.

### Your turn

1. Add a test that sends `Authorization: Bearer` with an **empty** token and records what httpbin returns. Is that what a real API should do?
2. Create a `.env` file with `API_TOKEN=...`, add `.env` to `.gitignore`, and load it with `python-dotenv` (`load_dotenv()`).
3. Decode the middle part of this JWT payload: `eyJzdWIiOiJhbmEiLCJyb2xlIjoicWEifQ`. (Hint: add `==` padding and use `base64.urlsafe_b64decode`.)
4. Write a table of five negative auth tests (input → expected code) for a real login-protected API.

### Common errors

- **A hard-coded token in a test file.** It ends up in Git history forever, so rotate it and switch to an environment variable.
- **Logging `r.request.headers`.** The token appears in CI logs. Mask it, for example by printing `token[:4] + "***"`.
- **Expecting `403` when the token is missing.** A missing or invalid token gives `401`. A valid token with too little permission gives `403`.

---

## Topic 7 – Fixtures and Parametrization

📁 Folder: `04-7-fixtures/`, files `conftest.py` and `test_fixtures.py`

### Definition

A **fixture** is a function marked with `@pytest.fixture` that prepares something a test needs, such as an HTTP session, a token or test data. PyTest **injects** it into any test that names it as an argument. Code after `yield` in a fixture is **teardown**, and it runs even when the test fails. **Scope** (`function`, `module`, `session`) controls how often the fixture is rebuilt. **Parametrization** (`@pytest.mark.parametrize`) runs one test function many times with different inputs, so each row becomes its own test.

### Key ideas

| Scope | Created | Good for |
|-------|---------|----------|
| `function` (default) | Once per test | Test data that a test may change |
| `module` | Once per file | Expensive read-only setup |
| `session` | Once per run | An HTTP session, an auth token |

- Put shared fixtures in **`conftest.py`**. PyTest finds them automatically, with no import needed.
- A fixture can depend on other fixtures, for example `auth_http` uses `token`.
- `ids=` gives readable test names. `pytest.param(..., marks=pytest.mark.xfail)` marks one row as an expected failure.
- Debug fixtures with `pytest --setup-show` and `pytest --fixtures`.

### Worked example – A small fixture set and a parametrized test

**Step 1 – Create `conftest.py` with configuration fixtures.**

```python
import os
import pytest
import requests


@pytest.fixture(scope="session")
def base_url():
    return os.getenv("BASE_URL", "https://jsonplaceholder.typicode.com")


@pytest.fixture(scope="session")
def token():
    return os.getenv("API_TOKEN", "dev-token-123")
```

**Step 2 – Add a shared HTTP session, with teardown.**

```python
@pytest.fixture(scope="session")
def http():
    s = requests.Session()
    s.headers["Accept"] = "application/json"
    yield s
    s.close()
```

**Step 3 – Chain fixtures, and add a self-cleaning data fixture.**

```python
@pytest.fixture(scope="session")
def auth_http(token):
    s = requests.Session()                      # its own session, so others stay anonymous
    s.headers["Authorization"] = f"Bearer {token}"
    yield s
    s.close()


@pytest.fixture
def new_post(http, base_url):
    post = http.post(f"{base_url}/posts", json={"title": "fixture", "body": "b", "userId": 1},
                     timeout=5).json()
    yield post
    http.delete(f"{base_url}/posts/{post['id']}", timeout=5)   # runs even if the test fails
```

**Step 4 – Use the fixtures** (`test_fixtures.py`).

```python
import pytest


def test_new_post_has_id(new_post):
    assert new_post["id"] == 101


def test_auth_header_is_set(auth_http):
    assert auth_http.headers["Authorization"].startswith("Bearer ")
```

**Step 5 – Parametrize a test with readable ids.**

```python
@pytest.mark.parametrize("user_id, expected_name", [
    (1, "Leanne Graham"),
    (2, "Ervin Howell"),
    (3, "Clementine Bauch"),
], ids=["user-1", "user-2", "user-3"])
def test_user_names(http, base_url, user_id, expected_name):
    assert http.get(f"{base_url}/users/{user_id}", timeout=5).json()["name"] == expected_name
```

**Step 6 – Add negative rows, with one known failure marked.**

```python
@pytest.mark.parametrize("post_id, expected", [
    (1, 200),
    (100, 200),
    (101, 404),
    (0, 404),
    pytest.param(-1, 400, marks=pytest.mark.xfail(reason="API returns 404, not 400")),
])
def test_post_status_by_id(http, base_url, post_id, expected):
    assert http.get(f"{base_url}/posts/{post_id}", timeout=5).status_code == expected
```

### Final code

**`conftest.py`**

```python
import os
import pytest
import requests


@pytest.fixture(scope="session")
def base_url():
    return os.getenv("BASE_URL", "https://jsonplaceholder.typicode.com")


@pytest.fixture(scope="session")
def token():
    return os.getenv("API_TOKEN", "dev-token-123")


@pytest.fixture(scope="session")
def http():
    s = requests.Session()
    s.headers["Accept"] = "application/json"
    yield s
    s.close()


@pytest.fixture(scope="session")
def auth_http(token):
    s = requests.Session()                      # its own session, so others stay anonymous
    s.headers["Authorization"] = f"Bearer {token}"
    yield s
    s.close()


@pytest.fixture
def new_post(http, base_url):
    post = http.post(f"{base_url}/posts", json={"title": "fixture", "body": "b", "userId": 1},
                     timeout=5).json()
    yield post
    http.delete(f"{base_url}/posts/{post['id']}", timeout=5)   # runs even if the test fails
```

**`test_fixtures.py`**

```python
import pytest


def test_new_post_has_id(new_post):
    assert new_post["id"] == 101


def test_auth_header_is_set(auth_http):
    assert auth_http.headers["Authorization"].startswith("Bearer ")


@pytest.mark.parametrize("user_id, expected_name", [
    (1, "Leanne Graham"),
    (2, "Ervin Howell"),
    (3, "Clementine Bauch"),
], ids=["user-1", "user-2", "user-3"])
def test_user_names(http, base_url, user_id, expected_name):
    assert http.get(f"{base_url}/users/{user_id}", timeout=5).json()["name"] == expected_name


@pytest.mark.parametrize("post_id, expected", [
    (1, 200),
    (100, 200),
    (101, 404),
    (0, 404),
    pytest.param(-1, 400, marks=pytest.mark.xfail(reason="API returns 404, not 400")),
])
def test_post_status_by_id(http, base_url, post_id, expected):
    assert http.get(f"{base_url}/posts/{post_id}", timeout=5).status_code == expected
```

### How to run

```bash
cd week7-demos/04-7-fixtures
pytest -v
pytest --setup-show test_fixtures.py::test_new_post_has_id
```

### Checkpoint

```
test_fixtures.py::test_new_post_has_id PASSED
test_fixtures.py::test_auth_header_is_set PASSED
test_fixtures.py::test_user_names[user-1] PASSED
test_fixtures.py::test_user_names[user-2] PASSED
test_fixtures.py::test_user_names[user-3] PASSED
test_fixtures.py::test_post_status_by_id[1-200] PASSED
...
test_fixtures.py::test_post_status_by_id[-1-400] XFAIL (API returns 404, not 400)
============ 9 passed, 1 xfailed ============
```

In the `--setup-show` output, look for `SETUP F new_post` and `TEARDOWN F new_post`.

### Your turn

1. Remove `scope="session"` from the `token` fixture (so it becomes function-scoped) and run the tests. What error does `auth_http` cause, and why?
2. Parametrize a test over `/posts`, `/users`, `/comments` and `/albums` that asserts each returns `200` and a non-empty list.
3. Stack two `parametrize` decorators (`user_id` in `[1, 2]` × `resource` in `["posts", "albums"]`) to test `/users/{id}/{resource}`. How many tests are generated?
4. Write a `post_factory` fixture that returns a function, so a test can call `post_factory(title="x")` several times.

### Common errors

- **`ScopeMismatch`.** A wide-scope fixture (session) cannot use a narrow one (function).
- **Calling a fixture directly**, as in `new_post()`. That is an error. Ask for it as a test argument instead.
- **Changing a shared session-scoped object** (for example, adding an auth header to `http`). Every later test then sends that header. Give each purpose its own fixture.

---

## Answers

<details>
<summary><strong>Topic 5 – JSON Response Validation</strong></summary>

1. `jsonschema.exceptions.ValidationError: 1 is not of type 'string'`.
2. ```python
   def test_comments():
       comments = requests.get(f"{BASE}/comments", params={"postId": 1}, timeout=5).json()
       assert all("@" in c["email"] for c in comments)
       assert any(len(c["name"].split()) > 3 for c in comments)
   ```
3. ```python
   import json

   def safe_json(response):
       try:
           return response.json()
       except json.JSONDecodeError:
           raise AssertionError(
               f"Not JSON (status {response.status_code}): {response.text[:200]}")
   ```
4. `user["phone"]` raises `KeyError` with no context. The `.get()` version fails as an assertion, so PyTest shows `assert None is not None` along with your message.

</details>

<details>
<summary><strong>Topic 6 – Headers and Authentication</strong></summary>

1. httpbin returns `401`. That is correct: an empty token is a missing credential, and a real API should also return `401`.
2. ```python
   from dotenv import load_dotenv
   load_dotenv()                        # reads .env into os.environ
   TOKEN = os.environ["API_TOKEN"]      # fails fast if it is missing
   ```
3. `{"sub":"ana","role":"qa"}`.
4. | Input | Expected |
   |---|---|
   | No `Authorization` header | 401 |
   | `Bearer` with garbage token | 401 |
   | Expired token | 401 |
   | Token signature tampered | 401 |
   | Valid "viewer" token calling an admin endpoint | 403 |

</details>

<details>
<summary><strong>Topic 7 – Fixtures and Parametrization</strong></summary>

1. `ScopeMismatch: You tried to access the function scoped fixture token with a session scoped request object.` The session-scoped `auth_http` cannot depend on a fixture that is torn down after every test. A fixture can only use fixtures with the same scope or a wider one.
2. ```python
   @pytest.mark.parametrize("path", ["/posts", "/users", "/comments", "/albums"])
   def test_collections(http, base_url, path):
       r = http.get(f"{base_url}{path}", timeout=5)
       assert r.status_code == 200 and len(r.json()) > 0
   ```
3. 2 × 2 = **4** tests.
4. ```python
   @pytest.fixture
   def post_factory(http, base_url):
       def _make(title="t", body="b", user_id=1):
           return http.post(f"{base_url}/posts",
                            json={"title": title, "body": body, "userId": user_id},
                            timeout=5).json()
       return _make
   ```

</details>
