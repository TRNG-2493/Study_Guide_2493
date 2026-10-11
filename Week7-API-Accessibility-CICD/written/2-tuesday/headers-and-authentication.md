# Headers and Authentication

## Learning Objectives

By the end of this lesson you will be able to:

- Send custom request headers from Python with `requests`, per call and per `Session`, and explain which headers the library adds for you.
- Set and verify `Content-Type`, `Accept`, and `User-Agent` correctly, and diagnose the `415` and `406` failures that come from getting them wrong.
- Explain the difference between **authentication** (who are you?) and **authorization** (what may you do?), and map each to `401` and `403`.
- Use **Basic authentication** with `auth=HTTPBasicAuth(...)`, decode the header by hand, and explain why Base64 is encoding and not encryption.
- Use **API keys** in a header and in a query string, and explain why the header is the safer place.
- Use **Bearer tokens**, describe the three parts of a **JWT** (`header.payload.signature`), decode a payload for inspection only, and read the `exp` claim.
- Implement the **token login flow**: log in once, store the token on a `Session`, and reuse it on every later call.
- Explain **OAuth 2.0** conceptually: the four roles, the authorization code flow, the client credentials flow, scopes, and refresh tokens.
- Write a complete set of negative tests: missing, malformed, invalid, tampered, and expired credentials (`401`), wrong role (`403`), and bad logins.
- Keep secrets out of source code with environment variables and a git-ignored `.env` file, and mask secrets in logs.

---

## Why This Matters

Almost every real API is protected. Think about what an unprotected banking, healthcare, or shop API would allow: anyone on the internet could read other people's records, change prices, or delete accounts. Because of that, a large share of the endpoints you will test in Project 2 and in your future job sit behind some form of authentication. If your test suite cannot log in, it cannot test most of the API. If your test suite only ever logs in successfully, it is missing half of its job.

The important part is the second promise: a defect there is a **security defect**, and those are among the most expensive bugs a company can ship. Authentication tests are therefore high-value and cheap to write once you know the pattern.

On Monday you met the `Authorization` header and the other header families in Postman and `curl`. You learned what each header means and how to read it. Today you move from reading to **sending** headers from Python test code, and you learn the mechanics behind each common authentication style. The concepts are the same; what changes is that a script, not a person, does the typing, which means the process has to be repeatable, safe, and fast.

A third reason is **secrets**. A test suite needs real credentials, and credentials written into source code get committed, copied, and are very hard to take back. Learning the safe habit now costs almost nothing.

This afternoon's lesson on fixtures will show you how to share one logged-in client across a whole test run, and on Friday you will see how a CI/CD pipeline stores secrets so they never touch the repository. Today you build the pieces those lessons plug into.

### How the code was checked

Every snippet and output here was run against a local practice server implementing Basic, API key, Bearer (JWT), and OAuth-style checks, at `http://127.0.0.1:8923`. Replace that with your own base URL. All usernames, passwords, and keys (`qa_tester`, `s3cret!`, `qa-key-123`) are fake. Never put a real password in an example or a test file.

---

## The Concept

### 1. Sending Headers From Python

A header is a single line of metadata attached to a request. In `requests`, you pass headers as a dictionary through the `headers=` argument. Here is the smallest useful example. The practice server has an endpoint, `/echo-headers`, that sends back whatever headers it received, which makes it perfect for seeing exactly what your code transmitted.

```python
import requests

BASE_URL = "http://127.0.0.1:8923"

headers = {
    "Accept": "application/json",
    "User-Agent": "qea-tests/1.0",
    "X-Request-Id": "abc-123",
}
r = requests.get(f"{BASE_URL}/echo-headers", headers=headers, timeout=5)
print(r.json()["headers"])
```

Output:

```
{'Host': '127.0.0.1:8923', 'User-Agent': 'qea-tests/1.0', 'Accept-Encoding': 'gzip, deflate', 'Accept': 'application/json', 'Connection': 'keep-alive', 'X-Request-Id': 'abc-123'}
```

Line-by-line:

- `import requests` loads the HTTP library you met in the previous lesson.
- `BASE_URL = ...` holds the address once, so you do not repeat it in every call. Later you will read it from an environment variable.
- `headers = {...}` is an ordinary Python dictionary. Each key is a header name and each value is a header value. Values must be strings. If you put an integer there, `requests` raises an error, so write `"X-Retry": "3"`, not `3`.
- `requests.get(..., headers=headers, timeout=5)` sends the request with those headers added. The `timeout=5` means "give up after five seconds." You should always set one, because by default `requests` waits forever, and a hung test is worse than a failed test.
- `r.json()["headers"]` reads the server's echo of what it received.

Look closely at the output. You sent three headers, but the server received six. The extras, `Host`, `Accept-Encoding`, and `Connection`, were added by `requests` automatically. This is normal and helpful, but you should know what the library adds so that you are never surprised.

**Why does it matter what `requests` sends by default?** If you do nothing, here is what goes out:

```python
r = requests.get(f"{BASE_URL}/echo-headers", timeout=5)
print(r.request.headers)
```

Output:

```
{'User-Agent': 'python-requests/2.34.2', 'Accept-Encoding': 'gzip, deflate', 'Accept': '*/*', 'Connection': 'keep-alive'}
```

`r.request` is the request object that was actually sent, and `r.request.headers` shows its headers. This is your best debugging tool for header problems. When a test fails with `401` or `415`, do not guess. Print `r.request.headers` and compare what you sent against what the API documentation says it expects. (Note that `Host` is added at a lower level and does not appear in this print, but the server still receives it.)

#### Per-call headers and per-session headers

Passing `headers=` on every call is fine for a one-off experiment, but a test suite makes hundreds of calls that share the same headers. A `requests.Session` lets you set them once:

```python
session = requests.Session()
session.headers.update({
    "Accept": "application/json",
    "User-Agent": "qea-tests/1.0",
})

r = session.get(f"{BASE_URL}/echo-headers", timeout=5)
print(r.json()["headers"]["User-Agent"])     # qea-tests/1.0
```

`session.headers` behaves like a dictionary, so `.update()` adds or replaces several headers at once, and `session.headers["Name"] = "value"` sets one. Every request made through that session carries them. You can still pass `headers=` on an individual call, and the two are **merged**: the per-call value wins if both set the same name. This gives you a clean pattern: shared defaults on the session, special cases on the call.

A Session also reuses the network connection between calls, which makes a suite faster.

#### The three headers every test should control

Monday's lesson described dozens of headers. In day-to-day API testing from Python, three come up constantly: `Content-Type`, `Accept`, and `User-Agent`. Here is what each does and how it fails.

**`Content-Type`: "the body I am sending is in this format."** It describes the request body. The server uses it to decide how to parse what you sent. When you use the `json=` argument, `requests` serializes your dictionary to JSON *and* sets `Content-Type: application/json` for you:

```python
r = requests.post(f"{BASE_URL}/items", json={"n": 1}, timeout=5)
print(r.request.headers["Content-Type"], r.status_code)
```

```
application/json 201
```

But if you hand over a ready-made string with `data=`, `requests` does not guess:

```python
r = requests.post(f"{BASE_URL}/items", data='{"n": 1}', timeout=5)
print(r.request.headers.get("Content-Type"), r.status_code)
```

```
None 415
```

The body was perfectly valid JSON, but the request had no `Content-Type`, so the server answered `415 Unsupported Media Type`: "I do not know how to read this body." The fix is to declare the type yourself:

```python
r = requests.post(
    f"{BASE_URL}/items",
    data='{"n": 1}',
    headers={"Content-Type": "application/json"},
    timeout=5,
)
print(r.status_code)     # 201
```

This is one of the most common beginner mistakes, so remember the rule of thumb: **use `json=` for JSON bodies and let the library set the header; if you use `data=`, set `Content-Type` yourself.** It is also a great negative test: send the right body with the wrong `Content-Type` and assert that the API returns `415` rather than crashing with `500`.

**`Accept`: "I want the response in this format."** It describes the response you are prepared to receive. If the API cannot produce any of the formats you list, a well-behaved server answers `406 Not Acceptable`:

```python
r = requests.post(
    f"{BASE_URL}/items",
    json={"n": 1},
    headers={"Accept": "application/xml"},
    timeout=5,
)
print(r.status_code, r.json())
```

```
406 {'error': 'only json'}
```

Setting `Accept: application/json` on your session is a good default, because it makes your tests explicit about what they expect and protects them if a server can return several formats.

**`User-Agent`: "this is the software making the request."** By default it is `python-requests/2.34.2`. Some firewalls and bot filters block that value, and server operators often use `User-Agent` in logs to see who is calling. A custom value such as `qea-tests/1.0` helps the API team recognize your automated traffic and tell it apart from real users. Some companies even ask testers to include a team name or ticket number in it. It is a courtesy and a diagnostic aid, not a security control, because anyone can set any value.

#### Custom headers

APIs define their own headers, traditionally starting with `X-`: `X-Request-Id`, `X-Tenant-Id`, `X-Client-Version`. Send them like any other. A good habit is a unique `X-Request-Id` (for example `str(uuid.uuid4())`) on every test request, logged by the test, so a developer can search the server logs for that exact ID when the test fails.

#### Asserting on response headers

Response headers are test targets too. `r.headers` is **case-insensitive** (`r.headers["cache-control"]` works), and `r.headers.get("Name")` avoids a `KeyError` when the header may be absent:

```python
assert r.headers["Cache-Control"] == "no-store"
```

> Monday covered what each response header means. Today the focus is the request side and authentication; we return to `Cache-Control` and `WWW-Authenticate` where they appear in the auth tests below.

#### Common mistakes with headers

- Putting numbers in header values (use `"3"`, not `3`).
- Forgetting `Content-Type` when using `data=`.
- Comparing header names case-sensitively after converting `r.headers` to a plain dict.
- Setting `Content-Length` by hand; let `requests` compute it.
- Not printing `r.request.headers` when a request fails.
- Leaving out `timeout`.

---

### 2. Authentication Versus Authorization

These two words sound alike and are constantly confused, even by experienced developers. Understanding the difference is the foundation for every test in this lesson.

**Authentication (often shortened to AuthN)** answers: **"Who are you?"** The client proves its identity, usually with a password, a key, or a token. If the proof fails or is missing, the server answers `401 Unauthorized`.

**Authorization (AuthZ)** answers: **"What are you allowed to do?"** The server already knows who you are, and now decides whether *this identity* may perform *this action* on *this resource*. If the answer is no, the server answers `403 Forbidden`.

| Term | Question | Failure status | Typical cause |
|------|----------|----------------|---------------|
| Authentication | Who are you? | `401 Unauthorized` | No credentials, wrong password, bad or expired token |
| Authorization | What may you do? | `403 Forbidden` | Valid identity, but insufficient role or permission |

**Analogy.** At an airport, your passport at the check-in desk proves who you are: that is authentication. Your boarding pass decides which plane you may board and whether you may enter the business lounge: that is authorization. A passenger without a passport is turned away at the desk (`401`). A passenger with a valid passport and an economy ticket who walks into the lounge is stopped at the door (`403`). Notice that in the second case nobody doubts their identity; they are simply not allowed in.

**A naming trap.** The official name of `401` is "Unauthorized", but it really means "unauthenticated." The name is a historical accident. The status code you should expect for "you are not allowed" is `403`, not `401`. When you write test names, use the clear words: `test_missing_token_returns_401`, `test_reader_cannot_delete_returns_403`.

**A decision rule for testers.** Ask two questions in order:

1. Did the server manage to establish who sent the request? If not, expect `401`.
2. If yes, is that identity permitted to do this? If not, expect `403`.

**A wrinkle.** Some APIs answer `404` for another user's private resource so attackers cannot learn which IDs exist. If the documentation says so, accept `403` or `404` in that test and comment why.

#### Where the checks happen in the flow

Picture a request travelling through the server in stages:

```
Request arrives
   |
   v
[1] Is there a credential?            no  --> 401, WWW-Authenticate header
   |
   v
[2] Is the credential valid?          no  --> 401  (bad password, bad signature, expired)
   |
   v
[3] Is this identity allowed to do    no  --> 403
    this action on this resource?
   |
   v
[4] Run the real business logic       --> 200 / 201 / 204 / 4xx for other reasons
```

Your tests should aim at each gate separately. A test for gate 1 sends nothing. A test for gate 2 sends something broken. A test for gate 3 sends something perfectly valid but belonging to a user with too little power. That structure is exactly the negative-test table you will build near the end of this lesson.

---

### 3. Authentication Style 1: Basic Authentication

**What it is.** The simplest scheme in HTTP. The client sends the username and password with every request, joined by a colon and Base64-encoded, in the `Authorization` header:

```
Authorization: Basic cWFfdGVzdGVyOnMzY3JldCE=
```

**How the header is built.** Take `username:password`, convert it to bytes, Base64-encode it, and prefix the word `Basic` and a space. You can do the whole thing by hand in Python:

```python
import base64

credentials = base64.b64encode(b"qa_tester:s3cret!").decode()
print(credentials)
```

```
cWFfdGVzdGVyOnMzY3JldCE=
```

Line-by-line:

- `b"qa_tester:s3cret!"` is the username, a colon, and the password, written as bytes (the `b` prefix). A colon is the separator, which is why a username cannot contain one.
- `base64.b64encode(...)` converts those bytes to Base64 text, but returns bytes again.
- `.decode()` turns the result into a normal string.

**Why does Basic exist at all?** It needs no login step, no token storage, and no server state. For quick internal tools, simple scripts, and some legacy systems, it is enough.

**Using it from Python.** `requests` has built-in support, so you almost never build the header yourself:

```python
import requests
from requests.auth import HTTPBasicAuth

r = requests.get(
    f"{BASE_URL}/basic",
    auth=HTTPBasicAuth("qa_tester", "s3cret!"),
    timeout=5,
)
print(r.status_code, r.json())
print(r.request.headers["Authorization"])
```

```
200 {'authenticated': True, 'user': 'qa_tester'}
Basic cWFfdGVzdGVyOnMzY3JldCE=
```

Line-by-line:

- `from requests.auth import HTTPBasicAuth` imports the helper class that knows how to build the `Authorization: Basic ...` header.
- `auth=HTTPBasicAuth("qa_tester", "s3cret!")` tells `requests` to attach that header to this request.
- `r.request.headers["Authorization"]` proves what was sent. The value is identical to the one we built by hand.

A **shortcut** exists: passing a plain tuple, `auth=("qa_tester", "s3cret!")`, is treated as Basic auth. The two forms are equivalent; `HTTPBasicAuth` is more explicit, which helps readers who do not know the shortcut, and you will see both in real projects.

You can also use `auth` on a Session so every call is authenticated: `session.auth = ("qa_tester", "s3cret!")`.

**Base64 is encoding, not encryption.** This is the single most important thing to understand about Basic auth. Base64 is just a way to write bytes using only printable characters. It has no key and no secret. Anyone who sees the header can reverse it in one line:

```python
header = r.request.headers["Authorization"]          # "Basic cWFfdGVzdGVyOnMzY3JldCE="
print(base64.b64decode(header.split()[1]).decode())
```

```
qa_tester:s3cret!
```

The password is right there. That is why Basic authentication is acceptable **only over HTTPS**, where the whole request is encrypted in transit. Over plain `http://`, anyone on the network path can read the password. It is also why a Basic header pasted into a bug report or a chat message is a leaked password, even though it "looks like gibberish." Treat it exactly as you would the plain password.

> Vocabulary check: **encoding** changes the representation of data and can be reversed by anyone. **Encryption** scrambles data using a secret key so only the key holder can reverse it. **Hashing** produces a one-way fingerprint that cannot be reversed. Base64 is encoding.

**What a failure looks like.** The server answers `401` and includes a `WWW-Authenticate` header telling the client which scheme to use:

```python
r = requests.get(f"{BASE_URL}/basic", auth=("qa_tester", "nope"), timeout=5)
print(r.status_code, r.headers["WWW-Authenticate"])
```

```
401 Basic realm="api"
```

The `realm` is a label for the protected area. A browser shows a login popup when it sees this header; your test simply asserts on it.

The three tests (valid credentials returns `200`, wrong password returns `401`, no credentials returns `401`) are Exercise 1 below.

**When you will meet it.** Internal admin endpoints, CI tooling, and legacy systems. User-facing APIs are moving to tokens, because Basic sends the real password on every request and cannot express expiry or limited permissions. Never commit a `Basic cWFf...` string: it is a password.

---

### 4. Authentication Style 2: API Keys

**What it is.** An API key is a long random string issued to an application or developer account. It identifies the **calling application** rather than a human. You sign up for a developer portal, receive a key, and attach it to every request.

**Why it exists.** It is simple to issue, easy to revoke, and lets the provider track usage per key for billing and rate limits. A weather service, a maps service, and an internal reporting API might all use keys.

**Where the key goes.** There are two common places, and the choice matters.

**In a header (preferred).** The header name is chosen by the API provider, so read the documentation. Common names are `X-API-Key`, `Api-Key`, and `x-functions-key`.

```python
r = requests.get(
    f"{BASE_URL}/apikey-header",
    headers={"X-API-Key": "qa-key-123"},
    timeout=5,
)
print(r.status_code)      # 200
```

**In the query string (supported by some APIs).** The key becomes part of the URL:

```python
r = requests.get(f"{BASE_URL}/apikey-query", params={"api_key": "qa-key-123"}, timeout=5)
print(r.status_code, r.url)
```

```
200 http://127.0.0.1:8923/apikey-query?api_key=qa-key-123
```

Look at `r.url`: the key is visible in the address. That is exactly the problem. **URLs are recorded everywhere**: browser history, proxy logs, web server access logs, monitoring tools, and the `Referer` header sent to other sites. A key in a URL is therefore likely to leak. A header is not part of the URL and is much less likely to be logged. Use the header whenever the API gives you the choice, and if you must use the query form, treat the key as already semi-public and restrict what it can do.

**The failure case.** No key, or a wrong key, gives `401`:

```python
print(requests.get(f"{BASE_URL}/apikey-header", timeout=5).status_code)    # 401
```

Some APIs return `403` for an invalid key instead, since the key is recognized as a *format* but refused. Follow your API's documentation and assert the documented code.

**Common mistakes.** Putting keys in query strings in shared test files; assuming a key proves *which person* called (it identifies the application); using the production key in tests; reusing one key everywhere so a leak forces rotation everywhere.

---

### 5. Authentication Style 3: Bearer Tokens

**What it is.** The word "bearer" means "whoever holds this." A bearer token is a string that grants access to whoever presents it, like a cinema ticket: the usher does not check your name, only that the ticket is valid. It travels in the `Authorization` header with the scheme name `Bearer`:

```
Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...
```

This is the dominant style for modern REST APIs. The "do not lose the ticket" nature of bearer tokens is why they must be sent over HTTPS only and kept out of logs and reports.

**Why tokens instead of Basic.** With Basic, the password goes over the wire on every call. With tokens, the password is sent **once**, to a login endpoint. The server returns a token that:

- expires after a short time (minutes to hours), limiting damage if it leaks,
- can be revoked without changing the user's password,
- can carry the user's identity and role inside it.

#### The two-step flow

1. **Log in:** send credentials once to a login endpoint. The server returns a token.
2. **Use the token:** send `Authorization: Bearer <token>` on every later request.

Here is the whole flow against the practice server, with explanations:

```python
import requests

BASE_URL = "http://127.0.0.1:8923"

# Step 1: log in
login = requests.post(
    f"{BASE_URL}/auth/login",
    json={"username": "qa_tester", "password": "s3cret!"},
    timeout=5,
)
assert login.status_code == 200
token = login.json()["token"]

# Step 2: use the token
r = requests.get(
    f"{BASE_URL}/profile",
    headers={"Authorization": f"Bearer {token}"},
    timeout=5,
)
print(r.status_code, r.json())
```

```
200 {'user': 'qa_tester', 'role': 'admin'}
```

Line-by-line:

- The login call is a `POST` with the credentials in a JSON body (`json=` also sets `Content-Type`). Credentials go in the **body** and never in the URL.
- `assert login.status_code == 200` fails fast if login is broken. A failed login means the environment or credentials are wrong, which is a different problem from a failing feature test, and you want a clear message.
- `login.json()["token"]` extracts the token. The field name (`token`, `access_token`, `jwt`, `id_token`) varies by API; read the documentation or inspect the response once in Postman.
- `f"Bearer {token}"` builds the header value: the scheme word, one space, the token. Missing the space, or writing `bearer` with a typo such as `Bearer: ` with a colon, gives a confusing `401`.

#### What a JWT is

Most APIs issue tokens in the **JSON Web Token (JWT)** format, pronounced "jot." Here is the token the server just issued (shortened lines for reading):

```
eyJhbGciOiAiSFMyNTYiLCAidHlwIjogIkpXVCJ9
.eyJzdWIiOiAicWFfdGVzdGVyIiwgInJvbGUiOiAiYWRtaW4iLCAiaWF0IjogMTc5MTcyNjIxMCwgImV4cCI6IDE3OTE3Mjk4MTB9
.IsuChG3vvql27iPJiU2_O2wHjqfk7rTTobBT0Pmkc0k
```

It is three Base64URL-encoded pieces separated by dots:

```
header . payload . signature
```

1. **Header:** metadata about the token itself, mainly the signing algorithm (`alg`) and the type (`typ`).
2. **Payload:** the **claims**, which are statements about the user and the token.
3. **Signature:** a cryptographic seal computed from the header, the payload, and a secret key held by the server.

Decoding the first two parts shows the content:

```python
import base64
import json


def jwt_parts(token):
    """Return (header, payload) of a JWT. For INSPECTION ONLY: does not verify anything."""
    def decode(part):
        part += "=" * (-len(part) % 4)            # restore Base64 padding
        return json.loads(base64.urlsafe_b64decode(part))

    header_b64, payload_b64, _signature = token.split(".")
    return decode(header_b64), decode(payload_b64)


header, payload = jwt_parts(token)
print(header)
print(payload)
```

```
{'alg': 'HS256', 'typ': 'JWT'}
{'sub': 'qa_tester', 'role': 'admin', 'iat': 1791726210, 'exp': 1791729810}
```

Line-by-line:

- `token.split(".")` cuts the token into its three dotted pieces. The leading underscore on `_signature` signals "we do not use this."
- `part += "=" * (-len(part) % 4)` fixes **padding**. Base64 data must have a length that is a multiple of 4, using `=` as filler. JWTs remove that filler to be compact, so we restore it before decoding. The expression `-len(part) % 4` computes how many `=` characters are missing (0 to 3).
- `base64.urlsafe_b64decode` decodes the "URL-safe" Base64 alphabet that JWTs use (`-` and `_` instead of `+` and `/`). Using the plain `b64decode` can fail on some tokens.
- `json.loads` turns the decoded bytes into a Python dictionary.

Common claims you will see:

| Claim | Name | Meaning |
|-------|------|---------|
| `sub` | Subject | Who the token is about (user ID or username) |
| `iat` | Issued at | When the token was created (Unix timestamp, seconds) |
| `exp` | Expiration | When the token stops being valid (Unix timestamp) |
| `iss` | Issuer | Who created the token |
| `aud` | Audience | Which API the token is meant for |
| `role`, `scope` | (custom) | What the user may do |

**Reading `exp`.** The value `1791729810` is a Unix timestamp: seconds since 1 January 1970 UTC. To find the remaining lifetime in a test:

```python
import time

seconds_left = payload["exp"] - time.time()
print(round(seconds_left))      # 3600
```

The practice server issues one-hour tokens. A test can assert that lifetimes are sane: positive, and no longer than the policy allows. This is a real finding in security reviews: tokens valid for a year are a defect.

**Critical points about JWTs that every tester must understand:**

- **The payload is readable by anyone.** Base64URL is encoding, not encryption, exactly as with Basic auth. Never expect a JWT payload to hide anything. If you find a password, a national ID number, or a credit card in a payload, report it as a defect.
- **The signature prevents tampering, not reading.** The server recomputes the signature using its secret key. If you alter even one character of the header or payload, the signature no longer matches and the server rejects the token. You, as a tester without the key, cannot forge a valid one. That is precisely what makes tampering a good negative test.
- **Decoding is not verifying.** `jwt_parts` above tells you what the token *claims*. It does not prove the claims are genuine. Real verification needs the key and happens on the server. In tests, decode only to inspect (check `exp`, `role`, `sub`), never to decide that a token is trustworthy.
- **Not every bearer token is a JWT.** Some APIs issue opaque random strings that mean nothing to the client. Your code must never depend on being able to decode the token unless the API documents it. Try the inspection helper only when the token has two dots.

The site jwt.io (linked at the end) has a debugger that decodes tokens in the browser. Use it with test tokens only. Pasting a **production** token into a website is a leak.

#### Reusing the token with a Session

Sending the header by hand each time is tedious and easy to forget. Put the token on a `Session` once:

```python
session = requests.Session()
session.headers.update({"Accept": "application/json", "User-Agent": "qea-tests/1.0"})

token = requests.post(
    f"{BASE_URL}/auth/login",
    json={"username": "qa_tester", "password": "s3cret!"},
    timeout=5,
).json()["token"]

session.headers["Authorization"] = f"Bearer {token}"

print(session.get(f"{BASE_URL}/profile", timeout=5).json())
```

```
{'user': 'qa_tester', 'role': 'admin'}
```

From now on, every request made with `session` is authenticated. One login, many calls. This pattern is the heart of every API test framework, and it is the reason this lesson's last section wraps it in a client class.

#### Why log in once

Each login is a network call, may be rate-limited, and creates a new token on the server. Logging in 500 times for 500 tests is slow and can trigger brute-force protection. Log in once per run (or once per role). Exceptions are tests of login itself and of token expiry, which need their own fresh tokens.

#### Common mistakes with bearer tokens

- Forgetting the space (`f"Bearer{token}"`) or using the wrong scheme word (`Token`, `JWT`) when the API wants `Bearer`.
- Hard-coding a token that was valid yesterday; it will expire and the suite will fail at random. Obtain tokens at run time.
- Logging the full token, or sending it in a query string.

---

### 6. OAuth 2.0 (Concepts Only)

**What it is.** OAuth 2.0 is a **framework** (a set of rules) for letting one application get limited access to a user's data held by another service **without ever seeing the user's password**. It is the technology behind "Sign in with Google" and "Allow this app to read your calendar." The access it grants is a token, usually a bearer token. So OAuth does not replace bearer tokens; it describes **how you get one safely**.

**The problem it solves.** Imagine a photo-printing website that wants to print your pictures stored at a cloud service. Years ago it would have asked for your cloud password. That is dangerous: the printer would hold full access forever, and the only way to cut it off would be to change your password. OAuth 2.0 replaces this with "log in at the cloud service itself, say what the printer may do, and the printer receives a limited, expiring token."

#### The four roles

| Role | What it is | In the photo example |
|------|-----------|----------------------|
| **Resource owner** | The user who owns the data | You |
| **Client** | The application that wants access | The printing website |
| **Authorization server** | Authenticates the user and issues tokens | The cloud provider's login service |
| **Resource server** | The API that holds the data and accepts tokens | The cloud provider's photo API |

In many companies the authorization server and the resource server are different systems built by different teams. Your test client only talks to the first to obtain a token and the second to use it.

#### Scopes

A **scope** is a named permission that the client requests and the user approves, such as `photos:read` or `calendar:write`. The token carries the granted scopes, and the resource server checks them. This is authorization: a token with only `photos:read` that tries to delete a photo should receive `403`. When your tests request tokens, request only the scopes the test needs, and add a negative test that proves a narrow-scope token cannot do broader things.

#### Grant types (flows)

OAuth defines several **grant types**, which are different routes to a token. Two matter for a tester.

**Authorization code flow** (user present, browser involved):

```
1. Client sends the user's browser to the authorization server with the requested scopes.
2. The user logs in THERE and approves the request.
3. The authorization server redirects back to the client with a short-lived one-time CODE.
4. The client sends the code (plus its own secret) directly to the token endpoint.
5. The token endpoint returns an access token (and often a refresh token).
```

The important ideas are that the user's password never reaches the client, and that the code is exchanged for tokens in a direct server-to-server call. Because step 2 needs a real person in a browser, you rarely automate it through the UI in API tests. Instead, test environments usually provide a way to obtain a token directly (a test user with a password grant, a pre-issued token, or a mock authorization server). Which one your team uses is an environment question for the team lead.

**Client credentials flow** (no user; machine to machine):

The client authenticates as *itself* with a client ID and client secret and receives a token. There is no browser and no user. This is what automated tests, back-end services, and scheduled jobs use. Here it is against the practice server:

```python
r = requests.post(
    f"{BASE_URL}/oauth/token",
    data={
        "grant_type": "client_credentials",
        "client_id": "qa-client",
        "client_secret": "qa-secret",
        "scope": "read",
    },
    timeout=5,
)
print(r.status_code, {k: v for k, v in r.json().items() if k != "access_token"})
```

```
200 {'token_type': 'Bearer', 'expires_in': 300, 'scope': 'read'}
```

Line-by-line:

- The token endpoint expects a **form-encoded** body, so we use `data=` (which sends `application/x-www-form-urlencoded`), **not** `json=`. This is a very common point of confusion: the OAuth standard specifies form encoding, and many token endpoints reject JSON.
- `grant_type` states which flow we are using.
- `client_id` and `client_secret` identify the application. They are credentials, so they belong in environment variables, not in the file.
- The dictionary comprehension prints everything except the token, because we do not print tokens. The response tells us the token type, the lifetime in seconds (`expires_in`), and the granted `scope`.
- The `access_token` field (not shown) is then used as `Authorization: Bearer <access_token>`, exactly like the earlier login token.

A failed attempt returns an error in the standard shape:

```python
r = requests.post(f"{BASE_URL}/oauth/token", data={"grant_type": "client_credentials",
                  "client_id": "qa-client", "client_secret": "bad"}, timeout=5)
print(r.status_code, r.json())      # 401 {'error': 'invalid_client'}
```

#### Access tokens and refresh tokens

An **access token** is short-lived on purpose (minutes to an hour). If it leaks, the damage window is small. But making the user log in again every ten minutes would be unusable. So the authorization server often also issues a **refresh token**: a longer-lived credential whose only job is to obtain a new access token without asking the user again.

```
access token  : used on every API call, expires quickly
refresh token : kept private, sent only to the token endpoint, used to get a fresh access token
```

A refresh request posts `grant_type=refresh_token` plus the refresh token and client credentials to the same token endpoint (the practice server does not implement it). For testers, refresh tokens create their own cases: a valid refresh token returns a new access token; a reused, revoked, or expired refresh token is rejected; after logout the refresh token no longer works. Ask the developers which of these are in scope.

#### What OAuth means for your tests

Find out which flow your environment uses to give a test client a token, write one helper that obtains it, and from then on treat it as a Bearer token: same header, same tests. Interactive browser flows are out of scope this week.

---

### 7. Putting It Together: A Reusable Authenticated Client

In the previous lesson on the Requests library you saw a small client class that wraps a `Session` and a base URL. Authentication slots straight into it. The version below adds three things: default headers, a `login` method that stores the token on the session, and **masked logging**.

```python
# api/client.py
import logging
import requests

logger = logging.getLogger("api")
SENSITIVE = {"authorization", "x-api-key", "cookie", "set-cookie"}


def mask(headers):
    """Return a copy of the headers with secret values hidden."""
    return {k: ("***REDACTED***" if k.lower() in SENSITIVE else v) for k, v in headers.items()}


class ApiClient:
    def __init__(self, base_url, timeout=5):
        self.base_url = base_url.rstrip("/")
        self.timeout = timeout
        self.session = requests.Session()
        self.session.headers.update({"Accept": "application/json", "User-Agent": "qea-tests/1.0"})

    def request(self, method, path, **kwargs):
        kwargs.setdefault("timeout", self.timeout)
        url = f"{self.base_url}{path}"
        response = self.session.request(method, url, **kwargs)
        logger.info("%s %s -> %s | sent headers: %s",
                    method, url, response.status_code, mask(response.request.headers))
        return response

    def get(self, path, **kw):
        return self.request("GET", path, **kw)

    def post(self, path, **kw):
        return self.request("POST", path, **kw)

    def delete(self, path, **kw):
        return self.request("DELETE", path, **kw)


class AuthenticatedClient(ApiClient):
    def login(self, username, password, **extra):
        resp = self.post("/auth/login", json={"username": username, "password": password, **extra})
        resp.raise_for_status()                  # a failed login means a broken environment
        token = resp.json()["token"]
        self.session.headers["Authorization"] = f"Bearer {token}"
        return token

    def logout(self):
        self.session.headers.pop("Authorization", None)
```

Line-by-line, the parts that are new:

- `SENSITIVE` is a set of lowercase header names whose values must never be written to a log. `mask()` compares in lowercase so `Authorization`, `authorization`, and `AUTHORIZATION` are all caught.
- `kwargs.setdefault("timeout", self.timeout)` adds a timeout to every call unless the caller passed their own. A test can still override it.
- `self.session.request(method, url, **kwargs)` is the general form behind `session.get`, `session.post`, and so on.
- `response.request.headers` is what was actually sent, including the `Authorization` header that the session added. We pass it through `mask()` before logging.
- In `login`, `**extra` lets a test pass additional fields (we use it later for a short-lifetime token). `resp.raise_for_status()` raises an exception for a `4xx`/`5xx`, which makes a broken login stop the test run clearly.
- `self.session.headers["Authorization"] = ...` is the key line: from now on every call from this client is authenticated.
- `logout` removes the header, which is useful for a test that wants to prove the client is unauthenticated again.

**Why subclass?** `ApiClient` can make anonymous calls, which the negative tests need. `AuthenticatedClient` adds login. Keeping them separate means a test can choose the client that matches what it wants to prove.

---

### 8. Keeping Secrets Out of Code

**What counts as a secret?** Passwords, API keys, client secrets, access and refresh tokens, signing keys, database connection strings, and anything else that lets someone act as you or your system. Usernames are usually not secret, but are often treated that way.

**Why this matters so much.** A secret in source code is copied into every clone, every fork, every backup, every pull request, and the full Git history. Deleting it in a later commit does **not** remove it from history; anyone who has the repository can still find it. Automated bots scan public repositories for keys within minutes of a push. The only correct response to a leaked secret is to **revoke and replace it**, which is slow and disruptive. Prevention is far cheaper.

**The rule:** secrets live **outside** the repository and enter your code at run time.

#### Environment variables

An environment variable is a named value supplied by the operating system to every program it starts. Python reads them through `os.environ`:

```python
import os

API_USER = os.environ["API_USER"]                  # raises KeyError if missing: fails loudly
API_PASSWORD = os.environ["API_PASSWORD"]
API_KEY = os.getenv("API_KEY", "")                 # optional; default empty string
```

Use `os.environ["NAME"]` for values that **must** exist, because a missing one should stop the run with an error that names the variable. Use `os.getenv("NAME", default)` for optional settings. A friendlier version for required values:

```python
def require_env(name):
    value = os.environ.get(name)
    if not value:
        raise RuntimeError(f"Environment variable {name} is not set. See README, section 'Configuration'.")
    return value
```

Set them for your terminal session:

```bash
# macOS / Linux / Git Bash
export API_USER=qa_tester
export API_PASSWORD='s3cret!'

# Windows PowerShell
$env:API_USER = "qa_tester"
$env:API_PASSWORD = "s3cret!"
```

Use quotes in Bash when a value contains special characters such as `!`, `$`, or spaces; unquoted, the shell may interpret them. Variables set this way vanish when you close the terminal.

#### A `.env` file for local convenience

Typing exports every day is tedious. The common solution is a plain text file named `.env` in your project folder, loaded automatically by the `python-dotenv` package:

```bash
pip install python-dotenv
```

```
# .env  (NEVER commit this file)
API_BASE_URL=http://127.0.0.1:8923
API_USER=qa_tester
API_PASSWORD=s3cret!
READONLY_USER=reader
READONLY_PASSWORD=readpass
```

```python
# conftest.py (top of file)
from dotenv import load_dotenv

load_dotenv()          # copies the variables in .env into os.environ, if the file exists
```

Line-by-line: `.env` holds `NAME=value` lines (no spaces around `=`, no quotes needed unless the value has spaces). `load_dotenv()` reads it and adds each pair to `os.environ`, unless a variable of that name is already set in the real environment, in which case the real one wins. That last rule is what lets a CI system override local settings later.

**Then protect the file.** Create or edit `.gitignore` in the repository root:

```
# .gitignore
.env
.env.*
!.env.example
```

And provide a safe template for teammates, committed to Git, containing names but **no real values**:

```
# .env.example
API_BASE_URL=
API_USER=
API_PASSWORD=
READONLY_USER=
READONLY_PASSWORD=
```

A new teammate copies `.env.example` to `.env` and fills in their own values. Always check before committing:

```bash
git status            # .env must NOT appear in the list of files to be committed
git check-ignore -v .env    # prints the rule that ignores it, proving the protection works
```

**If you commit a secret by accident:** do not just delete it in the next commit. Tell your lead immediately, treat the secret as compromised, and have it revoked and replaced. Removing it from history is a separate, more advanced operation and does not undo the exposure.

> A pipeline cannot read your laptop's `.env` file. On Friday you will see how CI systems store these same variables as protected settings, so that the code you write today runs unchanged in the pipeline.

#### Other places secrets leak

Other places secrets leak: logs (mask `Authorization`), failure messages and `print()` debugging (never print a token), bug reports and screenshots (redact), pasted `curl` commands (use placeholders), and Postman exports (export without current values).

**Use dedicated test accounts.** Test credentials should belong to accounts that exist only for testing, with the minimum permissions needed, in a **non-production** environment. If a test secret leaks, the damage is then limited to a sandbox.

---

### 9. An Authentication Fixture (Preview)

Logging in once for the whole run is exactly what a pytest **fixture** is for. This afternoon's lesson explains fixtures fully. For now, read this as a preview of where the client from section 7 will be used:

```python
# conftest.py
import os
import pytest
from dotenv import load_dotenv

load_dotenv()

from api.client import ApiClient, AuthenticatedClient

BASE_URL = os.environ["API_BASE_URL"]


@pytest.fixture(scope="session")
def auth_client():
    client = AuthenticatedClient(BASE_URL)
    client.login(os.environ["API_USER"], os.environ["API_PASSWORD"])
    return client


@pytest.fixture(scope="session")
def readonly_client():
    client = AuthenticatedClient(BASE_URL)
    client.login(os.environ["READONLY_USER"], os.environ["READONLY_PASSWORD"])
    return client


@pytest.fixture
def anon_client():
    return ApiClient(BASE_URL)
```

- `scope="session"` means "create this once for the entire test run and share it." The login therefore happens **one time**, not before every test.
- `auth_client` is logged in as an administrator, `readonly_client` as a low-privilege user, and `anon_client` is not logged in at all. Each test chooses the identity it needs simply by naming the fixture as a parameter.
- `load_dotenv()` is called before reading variables, so local `.env` values are available.

Do not worry about the fixture mechanics yet; the next lesson covers them. What matters now is the idea: **identity is something a test asks for by name**.

---

### 10. Testing 401 and 403 (and Everything Around Them)

Now we use all of this to test what matters most: that the door really is locked. Create a standard set of cases for every protected endpoint.

| Test | Setup | Expected |
|------|-------|----------|
| Valid credentials | Correct token | `200` |
| No credentials | No `Authorization` header | `401` |
| Malformed header | `Authorization: Bearer` (no token) | `401` |
| Wrong scheme | `Authorization: Token abc` | `401` |
| Invalid token | A random string | `401` |
| Tampered token | Change one character of a real token | `401` |
| Expired token | A token past its `exp` | `401` |
| Wrong role | Reader's token calls an admin action | `403` |
| Another user's data | User A requests User B's private resource | `403` or `404` (per documentation) |
| Wrong password at login | Bad credentials | `401`, with no hint about which part was wrong |
| Brute force | Many failed logins | `429` or account lockout (if specified) |

#### The 401 tests, written compactly with parametrization

Most of the rows above are the same test with a different `Authorization` value. pytest's `parametrize` runs one test function once per value. (You will study `parametrize` in detail in the next lesson; the pattern is shown here because it fits so well.)

```python
import pytest


@pytest.mark.parametrize("auth_header", [
    None,
    "Bearer",
    "Token abc",
    "Bearer not-a-real-token",
    "Basic YTpi",
], ids=["missing", "no-token", "wrong-scheme", "garbage", "basic-instead"])
def test_profile_rejects_bad_credentials(anon_client, auth_header):
    headers = {"Authorization": auth_header} if auth_header else {}
    r = anon_client.get("/profile", headers=headers)
    assert r.status_code == 401
    assert "Bearer" in r.headers["WWW-Authenticate"]
```

Line-by-line:

- The list gives five different bad inputs: no header at all (`None`), the scheme word with no token, the wrong scheme word, a nonsense token, and a perfectly valid Basic header sent to a Bearer endpoint.
- `ids=[...]` gives each case a readable name in the test report, for example `test_profile_rejects_bad_credentials[wrong-scheme]`, instead of `[Token abc]`.
- `anon_client` is the unauthenticated client. Using the logged-in client here would send a *valid* token that overrides nothing and defeat the purpose.
- `headers = {...} if auth_header else {}` builds either one header or none.
- The last assertion checks `WWW-Authenticate`. A correct `401` tells the client which scheme to use (see Monday's headers lesson). This is a header test hiding inside an auth test.

#### Tampered and expired tokens

```python
def test_tampered_token_is_rejected(auth_client, anon_client):
    token = auth_client.session.headers["Authorization"].split()[1]
    header_b64, payload_b64, signature = token.split(".")
    flipped = "A" if payload_b64[-2] != "A" else "B"
    tampered = payload_b64[:-2] + flipped + payload_b64[-1]
    r = anon_client.get("/profile", headers={"Authorization": f"Bearer {header_b64}.{tampered}.{signature}"})
    assert r.status_code == 401
```

We take a real token, change a single character in the payload, and keep the old signature. The server recomputes the signature, sees the mismatch, and must reject it. The response says `{'error': 'bad signature'}` on the practice server. (We change the second-to-last character because the very last character of a Base64 string can contain unused padding bits and might not alter the decoded data.)

Expired tokens are harder, because you cannot wait an hour. The best option is to **ask the API for a short-lived token**; many test environments allow a lifetime parameter. Our practice server accepts `ttl_seconds` at login, and a negative value yields a token that is already expired:

```python
import os
import requests

def test_expired_token_is_rejected(anon_client):
    token = requests.post(f"{BASE_URL}/auth/login", timeout=5, json={
        "username": os.environ["API_USER"],
        "password": os.environ["API_PASSWORD"],
        "ttl_seconds": -10,
    }).json()["token"]

    r = anon_client.get("/profile", headers={"Authorization": f"Bearer {token}"})
    assert r.status_code == 401
    assert "expired" in r.json()["error"]
```

Output when run: `401 {'error': 'token expired'}`. Two alternatives: request a two-second token and `time.sleep(3)` (slow; keep to one test), or use a fixed, permanently expired token supplied by the developers and stored as a secret. Whichever you choose, an expired token must give `401` with a message that says why without revealing internals.

A useful positive test also checks the lifetime policy: with `_, payload = jwt_parts(token)`, assert `0 < payload["exp"] - time.time() <= 3600`.

#### The 403 test

```python
def test_reader_cannot_delete_users(readonly_client):
    r = readonly_client.delete("/users/1")
    assert r.status_code == 403


def test_admin_can_delete_users(auth_client):
    r = auth_client.delete("/users/1")
    assert r.status_code == 200
```

Always write both. The second test proves the endpoint works for someone who is allowed; without it, the `403` test could be passing for the wrong reason (for instance, the endpoint is broken for everybody). Pairs of "allowed" and "denied" tests are a core habit in security testing.

On the practice server the denial body is `{'error': 'admin role required'}`. A good `403` explains the rule but does not reveal internals.

#### Login tests

```python
def test_login_failures_do_not_reveal_which_part_was_wrong(anon_client):
    bad_password = anon_client.post("/auth/login", json={"username": "qa_tester", "password": "x"})
    bad_username = anon_client.post("/auth/login", json={"username": "nobody", "password": "x"})
    assert bad_password.status_code == bad_username.status_code == 401
    assert bad_password.json() == bad_username.json()
```

If the API answered "no such user" for one and "wrong password" for the other, an attacker could **enumerate** which usernames exist. Identical responses for both cases are the secure behavior.

#### A test that checks your masking works

```python
def test_secrets_are_masked_in_logs(auth_client, caplog):
    caplog.set_level("INFO", logger="api")
    auth_client.get("/profile")
    token = auth_client.session.headers["Authorization"].split()[1]
    assert token not in caplog.text
    assert "***REDACTED***" in caplog.text
```

`caplog` is a built-in pytest fixture that captures log output. This test proves your own tooling does not leak tokens, a bug that is easy to introduce and easy to miss.

Running the whole file against the practice server:

```
............
12 passed in 0.04s
```

#### What else to check in headers

Responses with personal data should carry `Cache-Control: no-store`; errors should not reveal software versions or stack traces; session cookies need `Secure`, `HttpOnly`, and `SameSite`.

Mocking authentication so tests do not depend on a live login service is a Wednesday topic; here, you are testing against the real thing.

---

### 11. A Real Scenario

A bookstore API documents: `POST /auth/login` (30-minute token); `GET /orders` (own orders, or any if role `support`); `DELETE /orders/{id}` (`admin` only). Plan:

1. **Identities:** request customer, support, and admin QA accounts; put them in `.env`, list names in `.env.example`.
2. **Client:** reuse `AuthenticatedClient` with one fixture per role plus an anonymous client.
3. **Happy paths:** customer reads orders (`200`); admin deletes (`200`/`204`).
4. **401 gates:** parametrized bad headers on `GET /orders` (missing, empty Bearer, wrong scheme, garbage, tampered, expired).
5. **403 gates:** customer deletes (`403`); customer A reads customer B's order (`403` or `404`); support deletes (`403`).
6. **What failures reveal:** `WWW-Authenticate` present? stack traces? identical login-failure messages?
7. **Protect the suite:** masked logs, no secrets in failure output, `.env` not staged.

The result is a small set of tests that documents the access rules and warns you if a change ever opens a door.

---

### 12. Debugging Authentication Failures

When a test gets an unexpected `401` or `403`, check in order:

1. **What was sent:** `print(r.request.headers)` (mask before sharing). Is `Authorization` present? A skipped fixture or new `Session` can lose it.
2. **Shape:** `Bearer`, one space, the token, no quotes or trailing newline. Tokens read from files often carry a newline: use `.strip()`.
3. **Scheme:** `Bearer`, `Token`, or `Basic`?
4. **Token contents:** decode (inspection only). Is `exp` in the past? Is the role right?
5. **Environment:** a staging token is rejected by production. Is `API_BASE_URL` what you think?
6. **Response:** the body and `WWW-Authenticate` often name the problem, for example `error="invalid_token"`.
7. **Reproduce in Postman or `curl`.** If it works there, compare headers line by line.

---

### 13. Practice Exercises

Use the practice server (or your own API). Solutions follow each exercise block; try each before reading.

**Exercise 1.** Call `/basic` with the correct credentials, then with a wrong password, then with none. Write three tests. For the failure cases, also assert the `WWW-Authenticate` header starts with `Basic`.

**Exercise 2.** Without using `auth=`, build the Basic header yourself with `base64` and send it with `headers=`. Confirm you get `200`.

**Exercise 3.** Write `jwt_parts(token)`, log in, and print the `sub`, `role`, and the seconds remaining until `exp`. Then decode this sample token by hand and say what its three claims mean:
`eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIxMjM0NSIsInJvbGUiOiJxYSIsImV4cCI6MTk5OTk5OTk5OX0.signature`

**Exercise 4.** Write a function `make_session(token)` returning a `Session` with `Accept`, `User-Agent`, and `Authorization` set. Use it to call `/profile`.

**Exercise 5.** Write a parametrized test that proves `/apikey-header` rejects a missing key and a wrong key, and accepts the right one.

**Exercise 6.** Write the negative-test table for `DELETE /users/{id}`: at least six rows, with the expected status codes.

**Exercise 7.** Move credentials into `.env`, load them with `python-dotenv`, and prove with `git check-ignore -v .env` that the file is ignored. (If your folder is not a repo, run `git init` first.)

**Exercise 8.** Write a test proving the `Authorization` value never appears in your client's log output.

#### Solutions

**Solution 1.**

```python
import requests

BASE_URL = "http://127.0.0.1:8923"


def test_basic_ok():
    r = requests.get(f"{BASE_URL}/basic", auth=("qa_tester", "s3cret!"), timeout=5)
    assert r.status_code == 200


def test_basic_wrong_password():
    r = requests.get(f"{BASE_URL}/basic", auth=("qa_tester", "WRONG"), timeout=5)
    assert r.status_code == 401
    assert r.headers["WWW-Authenticate"].startswith("Basic")


def test_basic_no_credentials():
    r = requests.get(f"{BASE_URL}/basic", timeout=5)
    assert r.status_code == 401
    assert r.headers["WWW-Authenticate"].startswith("Basic")
```

All three pass against the practice server. The first proves the happy path; the others prove the door is locked and that the server says which kind of key to use.

**Solution 2.**

```python
cred = base64.b64encode(b"qa_tester:s3cret!").decode()
r = requests.get(f"{BASE_URL}/basic", headers={"Authorization": f"Basic {cred}"}, timeout=5)
assert r.status_code == 200
```

`auth=` is only a convenience that builds exactly this header.

**Solution 3.** After logging in, `jwt_parts(token)` returns the payload; then:

```python
header, payload = jwt_parts(token)
print(payload["sub"], payload["role"], round(payload["exp"] - time.time()))
```

```
qa_tester admin 3600
```

For the sample token, decoding gives header `{'alg': 'HS256', 'typ': 'JWT'}` and payload `{'sub': '12345', 'role': 'qa', 'exp': 1999999999}`. So the subject is user `12345`, the role is `qa`, and the token expires at Unix time `1999999999`, which is 18 May 2033 at 03:33:19 UTC, far in the future. The signature part is the literal word `signature`, so this sample is **not** a real signed token; it is only for practising decoding.

**Solution 4.**

```python
def make_session(token):
    s = requests.Session()
    s.headers.update({"Accept": "application/json", "User-Agent": "qea-tests/1.0",
                      "Authorization": f"Bearer {token}"})
    return s
```

Calling `make_session(token).get(f"{BASE_URL}/profile", timeout=5).json()` returns `{'user': 'qa_tester', 'role': 'admin'}`.

**Solution 5.**

```python
import pytest


@pytest.mark.parametrize("headers, expected", [
    ({}, 401),
    ({"X-API-Key": "wrong"}, 401),
    ({"X-API-Key": "qa-key-123"}, 200),
], ids=["no-key", "wrong-key", "valid-key"])
def test_api_key_header(headers, expected):
    r = requests.get(f"{BASE_URL}/apikey-header", headers=headers, timeout=5)
    assert r.status_code == expected
```

Each tuple pairs the headers to send with the status to expect, so three scenarios live in one function.

**Solution 6.**

| # | Scenario | Setup | Expected |
|---|----------|-------|----------|
| 1 | Admin deletes a user | Admin token | `200` or `204` |
| 2 | No token | No header | `401` |
| 3 | Garbage token | `Bearer not-a-real-token` | `401` |
| 4 | Expired token | `ttl_seconds=-10` | `401` |
| 5 | Tampered token | Altered payload | `401` |
| 6 | Reader deletes | Reader token | `403` |
| 7 | Customer deletes another user | Customer token | `403` |
| 8 | Admin deletes a non-existent ID | Admin token, bad ID | `404` |
| 9 | Wrong scheme | `Basic ...` to a Bearer endpoint | `401` |

Rows 2 to 5 and 9 test authentication; 6 and 7 test authorization; 8 shows that a valid, authorized request can still fail for a business reason, so the status code alone does not tell you which gate failed.

**Solution 7.** Create `.env` with the names shown in section 8, `.gitignore` with `.env`, then:

```bash
git init
git check-ignore -v .env
```

Expected output: a line such as `.gitignore:1:.env	.env`, naming the rule that ignores the file. If the command prints nothing, the file is **not** ignored: fix `.gitignore` before any `git add`.

**Solution 8.** This is `test_secrets_are_masked_in_logs` from section 10. Both assertions are needed: the first proves no leak, the second proves logging happened (an empty log would otherwise pass).

---

### 14. Self-Check Quiz

Answer from memory, then check.

1. A request has a perfectly valid token for a read-only user and tries `DELETE /users/1`. What status do you expect, and is it an authentication or authorization failure?
2. You send `data='{"n": 1}'` to a JSON API and get `415`. What is the most likely cause?
3. Why is `Authorization: Basic cWFfdGVzdGVyOnMzY3JldCE=` as sensitive as the plain password?
4. A JWT has the parts `A.B.C`. Which part contains the claims, and which part prevents tampering?
5. Is it safe to put a user's national ID number in a JWT payload because the token is "encoded"? Why or why not?
6. Why is an API key in a query string riskier than one in a header?
7. You request an OAuth token and the server rejects your JSON body. What do you change?
8. Your test suite logs in once at the start. After 40 minutes every test fails with `401`. What is the most likely cause, and what are two fixes?

**Answers.**

1. `403`. The identity is established; the permission is missing, so it is authorization.
2. No `Content-Type: application/json` header. With `data=`, `requests` does not set it. Use `json=` or add the header.
3. Base64 is reversible by anyone in one line, so the header contains the password in recoverable form.
4. `B` (the middle part, the payload) holds the claims. `C` (the signature) prevents tampering. Both `A` and `B` are readable by anyone.
5. No. Encoding is not encryption; anyone who sees the token can decode it. Sensitive data must not be placed in the payload.
6. URLs are stored in browser history, server and proxy logs, and monitoring tools, and can be passed along in `Referer`. Headers are not normally logged like that.
7. Send the body as form data with `data=`, not `json=`. Token endpoints use `application/x-www-form-urlencoded`.
8. The token expired (for example a 30-minute lifetime). Fixes: have the client log in again and retry once when it receives a `401` for an expired token, or request a fresh token when the stored one is close to its `exp`. Check the lifetime so you know the policy.

---

### 15. Glossary

### Authentication (AuthN)
Proving who a caller is. Failure is usually `401`.

### Authorization (AuthZ)
Deciding what an identified caller may do. Failure is usually `403`.

### Basic authentication
An `Authorization` header holding `Basic ` plus the Base64 of `username:password`. Safe only over HTTPS.

### Base64 / Base64URL
A way to represent bytes as printable text. Reversible by anyone. Base64URL swaps `+` and `/` for `-` and `_` and often drops `=` padding; JWTs use it.

### API key
A long random string identifying a calling application, sent in a header (preferred) or a query string.

### Bearer token
A credential that grants access to whoever presents it, sent as `Authorization: Bearer <token>`. Must be protected like a password.

### JWT (JSON Web Token)
A token with three Base64URL parts, `header.payload.signature`. Readable by anyone, tamper-evident through its signature.

### `exp`
The claim holding the expiry time as a Unix timestamp in seconds.

### OAuth 2.0
A framework for obtaining limited access tokens without sharing passwords. It defines roles, grant types, and scopes.

### Resource owner, client, authorization server, resource server
The four OAuth roles: the data's owner, the app wanting access, the system issuing tokens, and the API holding the data.

### Authorization code flow
An OAuth flow where a user logs in at the authorization server in a browser and the client exchanges a one-time code for tokens.

### Client credentials flow
An OAuth flow where an application authenticates as itself with an ID and secret. Used by automated tests and services.

### Scope
A named permission that a token carries, such as `photos:read`.

### Secret
Any value that lets someone act as you or your system: passwords, keys, tokens, client secrets.

---

## Summary

- Send headers with `headers=` per call or on a `Session`; use `r.request.headers` to see what was truly sent.
- `Content-Type` describes your body (`json=` sets it, `data=` does not), `Accept` what you want back; mistakes give `415` and `406`.
- Authentication proves identity (`401`); authorization checks permission (`403`).
- Basic auth is `auth=("user", "pass")`; its header is Base64, which is **encoding, not encryption**. API keys belong in a header, not a URL.
- Bearer tokens come from a login call and travel as `Authorization: Bearer <token>`. A JWT is `header.payload.signature`: readable by all, tamper-evident, expiry in `exp`. Decode only to inspect. Keep the token on a `Session` so one login serves the run.
- OAuth 2.0 describes how tokens are obtained: four roles, scopes, authorization code (users), client credentials (machines), refresh tokens.
- Test every gate: missing, malformed, invalid, tampered, expired (`401`); wrong role (`403`); login failures that reveal nothing.
- Keep secrets in environment variables or a git-ignored `.env`, mask them in logs, use test accounts, and revoke anything that leaks. Friday covers CI secret handling.

## Additional Resources

- MDN Web Docs, *HTTP authentication*: https://developer.mozilla.org/en-US/docs/Web/HTTP/Authentication
- MDN Web Docs, *Authorization header*: https://developer.mozilla.org/en-US/docs/Web/HTTP/Headers/Authorization
- RFC 7617, *The "Basic" HTTP Authentication Scheme*: https://datatracker.ietf.org/doc/html/rfc7617
- RFC 6750, *The OAuth 2.0 Authorization Framework: Bearer Token Usage*: https://datatracker.ietf.org/doc/html/rfc6750
- RFC 6749, *The OAuth 2.0 Authorization Framework*: https://datatracker.ietf.org/doc/html/rfc6749
- RFC 7519, *JSON Web Token (JWT)*: https://datatracker.ietf.org/doc/html/rfc7519
- jwt.io, *Introduction to JSON Web Tokens*: https://jwt.io/introduction
- Requests documentation, *Authentication*: https://requests.readthedocs.io/en/latest/user/authentication/
- Requests documentation, *Advanced usage (Session objects)*: https://requests.readthedocs.io/en/latest/user/advanced/
- python-dotenv documentation: https://saurabh-kumar.com/python-dotenv/
