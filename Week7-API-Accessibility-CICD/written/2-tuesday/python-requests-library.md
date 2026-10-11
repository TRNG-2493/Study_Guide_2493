# Python Requests Library

## Learning Objectives

By the end of this lesson you will be able to:

- Explain what the `requests` library is, why testers use it instead of Postman alone, and how it relates to the HTTP messages and methods you studied on Monday.
- Create a virtual environment, install `requests`, pin the dependency, and confirm the installation from Python.
- Send `GET`, `POST`, `PUT`, `PATCH`, and `DELETE` requests with `requests.get()`, `requests.post()`, `requests.put()`, `requests.patch()`, and `requests.delete()`, and explain every argument in each call.
- Pass query parameters with `params=`, JSON bodies with `json=`, form bodies with `data=`, and custom headers with `headers=`, and describe exactly what bytes each one puts on the wire.
- Inspect a `Response` object: `status_code`, `reason`, `ok`, `text`, `content`, `json()`, `headers`, `elapsed`, `url`, `history`, `cookies`, `encoding`, and `request`.
- Explain why `requests` never times out by default, set `timeout=` correctly (including the connect/read tuple), and predict which exception each failure raises.
- Use `raise_for_status()` and the exception hierarchy (`RequestException`, `ConnectionError`, `Timeout`, `HTTPError`, `JSONDecodeError`, `TooManyRedirects`, `SSLError`) in `try`/`except` blocks.
- Use a `requests.Session` to share headers, cookies, and connections, and explain its one big gotcha (no default timeout).
- Control redirects with `allow_redirects` and `history`, understand `verify=` and TLS certificates, and describe the idea behind retries with backoff.
- Use `Request`, `PreparedRequest`, and `response.request` to see exactly what was sent, and translate a Postman request into equivalent Python.

---

## Why This Matters

Yesterday you learned to explore APIs by hand. You read raw HTTP messages, you met the methods `GET`, `POST`, `PUT`, `PATCH`, and `DELETE`, you added query parameters and path parameters, you controlled headers, and you saved base URLs and tokens in Postman variables. That manual work is exactly how a good tester builds understanding: you can see everything, you can poke at the API, and you get instant feedback.

But manual work has hard limits. A person cannot click "Send" at 2 a.m. when a release pipeline runs. A person cannot send ten thousand different inputs in a lunch break. A person cannot attach a reviewable, version-controlled history to a click. And a person cannot easily combine "send request A, take the `id` from its answer, use it in request B, and then compare the two answers" without doing a lot of copying and pasting.

Code removes every one of those limits. This week's epic is to deliver a **pipeline-ready API test framework for Project 2**. The word "pipeline" matters: a CI/CD pipeline (continuous integration and continuous delivery, covered on Friday) can only run things that a machine can start and judge without a human. A Postman click cannot do that. A Python function that sends a request and asserts on the answer can. The `requests` library is the engine of the API layer in that framework: every test you write from today forward will, at its core, call `requests.get(...)` or `requests.post(...)`, or call a small helper built on top of them, and then check what came back.

There is a second reason to learn `requests` properly instead of copying a three-line example. When a test fails in a pipeline, nobody is watching. You cannot open Postman and look at the raw response. You only have your code's output and logs. If your code did not set a timeout, the pipeline may hang for hours until someone cancels it. If your code did not print the response body on failure, you are guessing. If your code confused `json=` with `data=`, the API will answer `415` or `400` and you will chase a "bug" that is really your request. If your code called `raise_for_status()` in a test that was supposed to expect a `404`, the test will crash instead of pass. Every one of those mistakes is a story that happens to real testers in their first month, and every one is easy to avoid once you understand what `requests` does under the hood.

Finally, the skills transfer directly. Everything you did in Postman has a one-to-one Python equivalent, and this lesson shows each mapping. Later today you will wrap these calls in PyTest tests, assert on status codes and JSON content, add authentication headers, and share setup with fixtures; those lessons each have their own page. Here you will build the foundation they all stand on. On Wednesday you will feed many data rows through the same calls, on Thursday you will look at accessibility testing, and on Friday you will run it all in a pipeline. All of it starts with one call: `requests.get(url)`.

---

## The Concept

### 1. What Is `requests`, and Why Use It?

`requests` is a third-party Python library for sending HTTP requests. "Third-party" means it is not part of Python's standard library: you must install it. Its tagline is "HTTP for Humans", and the name fits.

Python does include a built-in way to send HTTP requests (`urllib.request`, and below that `http.client`). It works, but it is low-level. With it, you build the request object yourself, encode the body yourself, decode the answer yourself, and handle redirects, cookies, and compression yourself. `requests` does all of that for you with sensible defaults:

`requests` is also the library you will find in almost every Python API test project, tutorial, and job description. Learning it once pays off for your entire career.

**What `requests` is not.** It is not a browser. It does not run JavaScript, render pages, or click buttons. It sends one HTTP message and gives you the HTTP message that came back. That is exactly what you want for API testing, because APIs are machine-to-machine conversations.

**How it relates to Monday.** On Monday you learned that an HTTP exchange is a request message (start line, headers, blank line, optional body) and a response message (status line, headers, blank line, optional body). Every part of that structure has a home in `requests`:

| HTTP message part | Where it lives in `requests` |
|-------------------|------------------------------|
| Method | The function name: `requests.get`, `requests.post`, ... |
| URL, path, query string | First argument and `params=` |
| Request headers | `headers=` |
| Request body | `json=`, `data=`, `files=` |
| Status code | `response.status_code` |
| Response headers | `response.headers` |
| Response body | `response.text`, `response.content`, `response.json()` |

Keep that table in mind. Whenever you are unsure how to do something in `requests`, ask "which part of the HTTP message is this?" and the answer is usually obvious.

### 2. Setting Up: Virtual Environment and Installation

#### 2.1 Why a virtual environment?

Python packages are installed into a Python installation. If you install everything into the one global Python on your machine, two projects that need different versions of the same library will fight each other. A **virtual environment** (venv) is a private folder that holds its own copy of the Python interpreter link and its own installed packages. Each project gets one. Activating it tells your terminal "use the Python and packages from this folder, not the global ones".

#### 2.2 The commands, step by step

```bash
# 1. Create the virtual environment in a folder named .venv
python -m venv .venv

# 2. Activate it
#   Windows (PowerShell):
.venv\Scripts\Activate.ps1
#   Windows (cmd):
.venv\Scripts\activate.bat
#   macOS / Linux:
source .venv/bin/activate

# 3. Install requests
pip install requests

# 4. Record the dependency so teammates (and CI) can reproduce it
pip freeze > requirements.txt
```

Line by line:

- `python -m venv .venv` runs Python's built-in `venv` module (`-m` means "run this module as a script") and tells it to create an environment in a folder called `.venv`. The leading dot is a convention that hides the folder on macOS and Linux and signals "tooling, not source code". On some systems the command is `python3` instead of `python`.
- The activation command differs per operating system. After it succeeds, your prompt usually shows `(.venv)` at the start. If you do not see that, you are not inside the environment and `pip install` will go to the wrong place.
- `pip install requests` downloads `requests` and the small libraries it depends on (`urllib3`, `idna`, `certifi`, `charset-normalizer`) from the Python Package Index (PyPI) into the active environment.
- `pip freeze > requirements.txt` lists every installed package with its exact version and writes the list to a file. The `>` is a shell redirect that sends the output into the file. Anyone, including a CI server, can later run `pip install -r requirements.txt` and get the same versions. On Friday you will see exactly why a pipeline needs that file.

#### 2.3 Check that it worked

```python
import requests
print(requests.__version__)
```

Line by line: `import requests` loads the library into your program, and `requests.__version__` is a string attribute holding the installed version. If you see `ModuleNotFoundError: No module named 'requests'`, the library is not installed in the Python you are running. That nearly always means the virtual environment is not active, or your editor is using a different interpreter than your terminal. Representative output:

```
2.34.2
```

Your version number may differ. That is fine; the core API in this lesson has been stable for many years.

### 3. Your First Request

Here is the smallest useful program:

```python
import requests

response = requests.get("https://jsonplaceholder.typicode.com/posts/1", timeout=5)

print(response.status_code)
print(response.json())
```

Line by line:

1. `import requests` loads the library.
2. `requests.get(url, timeout=5)` sends an HTTP `GET` request to that URL. Python **pauses** at this line until the response arrives (or the timeout expires). It returns a `Response` object, which we store in the variable `response`. The `timeout=5` argument means "if the server does not respond within five seconds, give up". You will see why that matters in section 10.
3. `response.status_code` is an integer such as `200`.
4. `response.json()` reads the body, parses it as JSON, and returns native Python data. JSON objects become `dict`, JSON arrays become `list`, strings stay `str`, numbers become `int` or `float`, `true` and `false` become `True` and `False`, and `null` becomes `None`.

Representative output (the practice API is on an external host, so this is what you should expect to see when you run it):

```
200
{'userId': 1, 'id': 1, 'title': 'sunt aut facere repellat provident occaecati excepturi optio reprehenderit', 'body': 'quia et suscipit\nsuscipit recusandae consequuntur ...'}
```

**About the practice API.** This lesson uses **JSONPlaceholder** (`https://jsonplaceholder.typicode.com`), a free fake REST API built for learning. It has `/posts` (100 posts), `/comments`, `/albums`, `/photos`, `/todos`, and `/users`. It accepts `POST`, `PUT`, `PATCH`, and `DELETE`, and it answers as if they worked, but it **does not actually save your changes**. That is perfect for practice: you can never break anything, but you must remember that creating a post and then fetching it will not find it. You saw this behaviour in Postman on Monday.

**A note on the code in this lesson.** We tested every code snippet in this lesson against a small local mock server that imitates JSONPlaceholder's behaviour. Where a snippet's output comes from the real JSONPlaceholder, we label it "representative output", because the exact text (for example, post titles, header values, and timings) can differ slightly from what you see.

### 4. The Five Methods in Python

Every HTTP method you met on Monday has a function with the same name:

```python
import requests

BASE_URL = "https://jsonplaceholder.typicode.com"

r = requests.get(f"{BASE_URL}/posts/1", timeout=5)
r = requests.post(f"{BASE_URL}/posts",
                  json={"title": "Hi", "body": "B", "userId": 1}, timeout=5)
r = requests.put(f"{BASE_URL}/posts/1",
                 json={"id": 1, "title": "New", "body": "B", "userId": 1}, timeout=5)
r = requests.patch(f"{BASE_URL}/posts/1", json={"title": "Only title"}, timeout=5)
r = requests.delete(f"{BASE_URL}/posts/1", timeout=5)
```

Line by line:

- `BASE_URL = "..."` stores the common part of every URL in one variable. Constants in Python are written in `UPPER_CASE` by convention. This is the code equivalent of the Postman variable `{{baseUrl}}` from Monday. If the API moves from a test server to a staging server, you change one line.
- `f"{BASE_URL}/posts/1"` is an **f-string**. The `f` before the opening quote tells Python to replace anything inside `{}` with the value of that expression. The result is `https://jsonplaceholder.typicode.com/posts/1`.
- `requests.get(...)` reads a resource. It has no body.
- `requests.post(..., json={...})` creates a resource. The `json=` keyword sends a body (details in section 6).
- `requests.put(...)` replaces a resource completely. That is why the body includes all the fields, including `id`.
- `requests.patch(...)` changes only the fields you send.
- `requests.delete(...)` removes a resource. No body needed.
- Each call ends with `timeout=5`. Get into the habit now.

Notice that a real, well-behaved API might answer `204 No Content` to a `DELETE`, and JSONPlaceholder answers `200` with `{}`. Always check what *your* API's documentation promises. Do not assume.

### 5. Query Parameters with `params=`

Recall from Monday that a query string is the part of a URL after `?`, written as `key=value` pairs joined by `&`. You can build it by hand, but this is fragile:

```python
# Fragile: you must encode special characters yourself
r = requests.get(f"{BASE_URL}/posts?userId=1&_limit=3", timeout=5)
```

Better, pass a dictionary:

```python
params = {"userId": 1, "_limit": 3}
r = requests.get(f"{BASE_URL}/posts", params=params, timeout=5)

print(r.url)
print(len(r.json()))
```

Line by line:

- `params = {"userId": 1, "_limit": 3}` defines the query parameters as a Python dictionary. Values can be numbers; `requests` converts them to text.
- `params=params` hands the dictionary to the call. `requests` builds `?userId=1&_limit=3`, appends it to the URL, and percent-encodes anything that needs it.
- `r.url` shows the final URL that was actually requested. Printing it is the quickest way to debug a query-string problem.
- `len(r.json())` counts the items in the list returned. `_limit` is a JSONPlaceholder feature that caps the number of results.

Run against our local mock, the output was:

```
http://127.0.0.1:8099/posts?userId=1&_limit=3
3
```

Against JSONPlaceholder the URL would start with `https://jsonplaceholder.typicode.com/posts?userId=1&_limit=3` and the count would again be `3`.

**Encoding special characters.** This is where `params=` really helps. Consider values with spaces, ampersands, or a list:

```python
r = requests.get(f"{BASE_URL}/posts",
                 params={"q": "a b&c", "tag": ["x", "y"], "skip": None},
                 timeout=5)
print(r.url)
```

Output (verified):

```
http://127.0.0.1:8099/posts?q=a+b%26c&tag=x&tag=y
```

Three useful behaviours are visible here:

1. The space became `+` and the `&` inside the value became `%26`. Had you built the string by hand, that `&` would have been read as the start of a new parameter and silently broken your request.
2. A list value becomes a repeated key: `tag=x&tag=y`. That is the most common convention for "multiple values", but APIs differ, so check the documentation.
3. A value of `None` is **dropped** from the query string. This is handy for optional filters: you can pass `None` to mean "do not filter on this".

**Path parameters** (for example `/posts/1`) are not handled by `params=`. They are part of the path, so you build them with an f-string: `f"{BASE_URL}/posts/{post_id}"`.

### 6. Sending a Body: `json=` versus `data=`

This is the single most important section of the lesson for avoiding silent mistakes. A request body can be sent in different encodings, and the `Content-Type` header tells the server which one you used. `requests` offers a different keyword for each.

#### 6.1 `json=`: send JSON

```python
payload = {"title": "Learning requests", "body": "It is easy", "userId": 1}
r = requests.post(f"{BASE_URL}/posts", json=payload, timeout=5)
```

`json=payload` does three things:

1. Converts the Python dictionary to JSON text (using `json.dumps` internally).
2. Sets the header `Content-Type: application/json`, unless you set it yourself.
3. Sends the text as the request body.

This is the equivalent of Postman's *Body > raw > JSON*.

#### 6.2 `data=`: send a form (or raw text)

```python
r = requests.post(f"{BASE_URL}/echo", data={"username": "qa", "role": "tester"}, timeout=5)
```

When `data=` receives a **dictionary**, `requests` encodes it as an HTML-form body (`username=qa&role=tester`) and sets `Content-Type: application/x-www-form-urlencoded`. That is the equivalent of Postman's *Body > x-www-form-urlencoded*. When `data=` receives a **string or bytes**, it sends those bytes exactly as they are and sets **no** `Content-Type` at all.

#### 6.3 See the difference without any network

You can see precisely what each keyword produces without sending anything, by building a request and *preparing* it (we explain `Request` and `prepare()` fully in section 16):

```python
import requests

for kwargs in ({"json": {"a": 1, "b": "x y"}},
               {"data": {"a": 1, "b": "x y"}},
               {"data": '{"a":1}'}):
    prepared = requests.Request("POST", "http://example.test/echo", **kwargs).prepare()
    print(prepared.headers.get("Content-Type"), "|", prepared.body)
```

Line by line:

- The `for` loop runs three times, once per dictionary in the tuple.
- `**kwargs` unpacks the dictionary into keyword arguments, so the first loop is the same as writing `requests.Request("POST", url, json={"a": 1, "b": "x y"})`.
- `requests.Request(...)` describes a request but sends nothing. `.prepare()` converts it into the exact message that would be sent.
- `prepared.headers.get("Content-Type")` reads the header (it returns `None` if absent). `prepared.body` shows the body.

Output (verified, and the same on every machine because nothing is sent):

```
application/json | b'{"a": 1, "b": "x y"}'
application/x-www-form-urlencoded | a=1&b=x+y
None | {"a":1}
```

Read the three lines carefully. The first is a JSON body with the right header. The second is a form body, with the space encoded as `+`. The third is a JSON-looking string sent through `data=`: the text arrives intact, but there is **no `Content-Type`**, so a strict API may reject it with `415 Unsupported Media Type` or treat it as plain bytes.

#### 6.4 Which one do I use?

| API documentation says... | Use |
|---------------------------|-----|
| Body is JSON (`application/json`) | `json=` |
| Body is an HTML form (`application/x-www-form-urlencoded`) | `data=` with a dict |
| Body is a file upload (`multipart/form-data`) | `files=` (optionally with `data=`) |
| Body is XML or plain text | `data="<xml>..."` plus an explicit `headers={"Content-Type": ...}` |

Most modern REST APIs, including the ones you will test in Project 2, use JSON, so `json=` is your default. The classic beginner error is writing `data=payload` with a dictionary against a JSON API. The server receives `title=Hi&userId=1`, cannot parse it as JSON, and answers `400 Bad Request` or `415 Unsupported Media Type`. If you see those two codes right after you wrote your first POST, check `json=` versus `data=` before anything else.

### 7. Request Headers with `headers=`

Monday's headers lesson explained what `Accept`, `Content-Type`, `Authorization`, and others do. In `requests`, you pass headers as a dictionary:

```python
headers = {
    "Accept": "application/json",
    "X-Request-Source": "qea-training",
}
r = requests.get(f"{BASE_URL}/users/1", headers=headers, timeout=5)
```

Line by line: the dictionary keys are header names and the values are header values (both strings). `X-Request-Source` is a made-up custom header, shown to illustrate that you may send any header you like. Header names are case-insensitive, so `accept` and `Accept` are the same.

**What does `requests` send when you pass no headers?** It sends sensible defaults: `User-Agent: python-requests/<version>`, `Accept-Encoding: gzip, deflate` (so the server may compress the answer and `requests` decompresses it automatically), `Accept: */*` ("I accept anything"), and `Connection: keep-alive`. Here is how to see them:

```python
r = requests.get(f"{BASE_URL}/posts", params={"userId": 2}, timeout=5)
print(dict(r.request.headers))
```

Output (verified):

```
{'User-Agent': 'python-requests/2.34.2', 'Accept-Encoding': 'gzip, deflate', 'Accept': '*/*', 'Connection': 'keep-alive'}
```

On a machine with optional compression libraries installed, `Accept-Encoding` may list more codings such as `br` or `zstd`. That is normal.

Two practical points. First, a **default `User-Agent` of `python-requests/x.y`** is announced to every server. Some APIs and web-application firewalls block or rate-limit it, because it looks like a script. If a request works in Postman but returns `403` from Python, comparing the `User-Agent` and `Accept` headers is a smart first step. Second, you can **remove** a default header for one call by setting its value to `None`, for example `headers={"Accept-Encoding": None}`.

Headers that carry credentials (the `Authorization` header and API keys) are covered in the Tuesday lesson on headers and authentication. For now, just know they are sent through this same `headers=` argument.

### 8. The `Response` Object

Every call returns a `Response`. Think of it as the whole HTTP response message, unpacked into convenient attributes. Spend time here: you will use these attributes in every test you write.

```python
r = requests.get(f"{BASE_URL}/users/1", timeout=5)

print("Status code :", r.status_code)
print("Reason      :", r.reason)
print("OK?         :", r.ok)
print("URL         :", r.url)
print("Time taken  :", r.elapsed.total_seconds(), "seconds")
print("Content-Type:", r.headers["Content-Type"])
print("Encoding    :", r.encoding)
print("Raw text    :", r.text[:60], "...")
print("Bytes       :", len(r.content), "bytes")
print("Parsed JSON :", r.json()["name"])
print("History     :", r.history)
print("Cookies     :", r.cookies.get_dict())
```

Line by line:

- `r.status_code` is the integer code, for example `200`.
- `r.reason` is the text phrase that came with the status line (`OK`). Compare the number, never the phrase: servers may change phrases, and HTTP/2 does not even transmit them.
- `r.ok` is `True` when the status code is **below 400** (so `200`, `201`, `204`, and also `301` or `302` are all "ok"). It is `False` for `4xx` and `5xx`. Do not use `ok` to mean "success" in a test; assert the exact code you expect.
- `r.url` is the final URL, including the query string and after any redirects.
- `r.elapsed` is a `timedelta`: the time between sending the request and receiving the response headers. `.total_seconds()` converts it to a float. It is useful for a rough performance check, but not a real benchmark (it ignores time spent reading a large body).
- `r.headers["Content-Type"]` reads one response header. `r.headers` is a **case-insensitive dictionary**, so `r.headers["content-type"]` works too.
- `r.encoding` is the character encoding `requests` will use to turn bytes into text. It is guessed from the `Content-Type` header (`charset=utf-8`).
- `r.text[:60]` is the body decoded as a `str`; `[:60]` slices off the first 60 characters so the output stays short.
- `r.content` is the body as raw `bytes`. Use it for images, PDFs, or when you do not want decoding.
- `r.json()["name"]` parses the body as JSON and then reads the key `name` from the resulting dictionary.
- `r.history` is a list of earlier responses if redirects were followed (empty here).
- `r.cookies.get_dict()` returns cookies the server set, as a normal dictionary (empty here).

Output when run against the local mock (verified; against JSONPlaceholder, expect the same shape with representative values such as `Content-Type: application/json; charset=utf-8`, a name of `Leanne Graham`, and a response time of tens to hundreds of milliseconds depending on your network):

```
Status code : 200
Reason      : OK
OK?         : True
URL         : http://127.0.0.1:8099/users/1
Time taken  : 0.001379 seconds
Content-Type: application/json; charset=utf-8
Encoding    : utf-8
Raw text    : {"id": 1, "name": "Leanne Graham", "email": "Sincere@april.bi ...
Bytes       : 64 bytes
Parsed JSON : Leanne Graham
History     : []
Cookies     : {}
```

A summary table you can keep beside you:

| Attribute | Type | What it gives you |
|-----------|------|-------------------|
| `status_code` | `int` | `200`, `404`, ... |
| `reason` | `str` | `OK`, `Not Found` (do not assert on it) |
| `ok` | `bool` | `True` if status is below 400 |
| `headers` | case-insensitive dict | Response headers |
| `text` | `str` | Body decoded to text |
| `content` | `bytes` | Raw body |
| `json()` | `dict`/`list`/... | Parsed JSON body; raises `JSONDecodeError` if the body is not valid JSON |
| `elapsed` | `timedelta` | Time to receive the response headers |
| `url` | `str` | Final URL, after redirects |
| `history` | `list` | Redirect responses that were followed |
| `cookies` | cookie jar | Cookies the server set |
| `encoding` | `str` | Encoding used for `.text` |
| `request` | `PreparedRequest` | The exact request that was sent |
| `is_redirect` | `bool` | `True` if this response is a redirect |

**`headers` is not a plain dict.** `type(r.headers)` is `requests.structures.CaseInsensitiveDict`. It behaves like a dictionary but ignores case on lookups. Use `dict(r.headers)` if you want an ordinary dictionary for printing. Here is the verified output of that conversion (the mock server's own values):

```
{'Server': 'BaseHTTP/0.6 Python/3.13.16', 'Date': 'Sun, 11 Oct 2026 13:42:42 GMT', 'Content-Type': 'application/json; charset=utf-8', 'Content-Length': '64'}
```

**Reading JSON safely.** `response.json()` raises an error if the body is not JSON. This happens more often than you expect: a gateway may return an HTML error page, an endpoint may return an empty body (for example `204 No Content`), or an authentication failure may return plain text. In a test, check the status code first and then parse. When the parse fails, print `response.text`; the HTML or message there usually explains the problem. We show the exception in section 11.

### 9. Status Codes and `raise_for_status()`

Unlike some tools, `requests` does **not** raise an exception just because the server answered `404` or `500`. From HTTP's point of view, a `404` is a perfectly good response: the exchange worked, and the server said "that does not exist". `requests` hands it to you as a normal `Response`, and you decide what it means.

```python
r = requests.get(f"{BASE_URL}/posts/99999", timeout=5)
print(r.status_code)

try:
    r.raise_for_status()
except requests.exceptions.HTTPError as err:
    print(type(err).__name__, "->", err)
    print("status from the exception:", err.response.status_code)
```

Line by line:

- The first call asks for a post that does not exist. We print the code (`404`).
- `try:` begins a block in which an exception may happen. If one does, Python jumps to the matching `except`.
- `r.raise_for_status()` checks the status. For any `4xx` or `5xx` it raises `requests.exceptions.HTTPError`. For anything else it does nothing and returns `None`.
- `except requests.exceptions.HTTPError as err:` catches only that exception type and names it `err`.
- `type(err).__name__` is the class name as text. `str(err)` (printed by `print(..., err)`) has the status, reason, and URL.
- `err.response` gives the `Response` that caused the error, so you can still read its status code or body in the handler.

Output (verified on the local mock):

```
404
HTTPError -> 404 Client Error: Not Found for url: http://127.0.0.1:8099/posts/99999
status from the exception: 404
```

Notice also that `raise_for_status()` does **not** raise for `3xx` codes and does not complain about `1xx` codes. It only looks at 4xx and 5xx.

#### When to use `raise_for_status()` and when not to

This is a design decision you will make in every project:

- **In setup, teardown, and helper code**, call it. If a fixture that creates test data gets a `500`, the test has no business continuing. A loud failure at the true point of the problem saves debugging time.
- **Inside the test itself, usually do not**. A test about `404` *wants* a `404`. If you call `raise_for_status()` first, the test crashes with an exception instead of passing. Assert the exact expected code instead: `assert response.status_code == 404`. Tuesday's lesson on status-code validation covers this in depth.

A useful rule of thumb: *`raise_for_status()` says "this must have worked". `assert status_code == X` says "this must have produced exactly X".*

### 10. Timeouts: Never Wait Forever

This is the most important safety habit in the lesson. **By default `requests` waits forever.** If you write `requests.get(url)` with no timeout and the server accepts your connection but never answers, your program freezes. In a test suite that means a hung job. In a CI pipeline that means a runner is blocked until a global job limit (often 60 minutes or more) kills it, and nobody learns why.

The fix is a one-keyword habit: always pass `timeout=`.

```python
r = requests.get(f"{BASE_URL}/posts/1", timeout=5)
```

`timeout=5` means "five seconds". The number applies to two separate phases, and it is important to understand which:

- **Connect timeout**: how long to wait while establishing the TCP connection to the server.
- **Read timeout**: how long to wait *between bytes* from the server once connected (specifically: how long to wait for the server to send data after you sent the request). It is **not** a limit on the total download time.

A single number sets both. A tuple sets them separately:

```python
r = requests.get(f"{BASE_URL}/posts/1", timeout=(3, 10))   # connect 3 s, read 10 s
```

Why separate? A connection should be established quickly (a few seconds at most). A slow report endpoint might legitimately need ten seconds to think. Separate values let you be strict about one and generous about the other.

Let us watch a timeout happen. Our local mock has a `/slow` endpoint that waits two seconds before answering:

```python
try:
    requests.get(f"{BASE_URL}/slow?s=2", timeout=0.5)
except requests.exceptions.Timeout as e:
    print(type(e).__name__)
```

Line by line: we ask for an answer within half a second, but the server needs two. After 0.5 seconds `requests` abandons the call and raises an exception. We catch the general `Timeout` class (the parent of both `ConnectTimeout` and `ReadTimeout`) and print which one it actually was. Output (verified locally):

```
ReadTimeout
```

It is `ReadTimeout` because the connection succeeded instantly; it was the *answer* that was too slow. A `ConnectTimeout` would appear if the server's address was unreachable (for example a firewall silently dropping packets).

**Choosing values.** `timeout=5` or `timeout=10` is a common team default. Set it in one place so you never forget it, and do not set it so low that a healthy but slow environment fails randomly.

### 11. Exceptions and What Raises Them

When `requests` cannot produce a `Response`, or when you ask it to be strict, it raises an exception. They all inherit from `requests.exceptions.RequestException`, so catching that one class catches everything the library can raise. Here is the family tree:

```
RequestException
 |-- HTTPError            raised by raise_for_status() for 4xx/5xx
 |-- ConnectionError      cannot reach the server (DNS, refused, reset)
 |    |-- SSLError        TLS/certificate problem
 |    |-- ConnectTimeout  (also a Timeout) connect phase too slow
 |-- Timeout
 |    |-- ConnectTimeout
 |    |-- ReadTimeout     server too slow to send data
 |-- TooManyRedirects     redirect loop (default limit 30)
 |-- InvalidURL, MissingSchema, InvalidSchema   malformed URLs
 |-- JSONDecodeError      response.json() on a non-JSON body
```

A few observations that confuse beginners and that we verified in code:

- `ConnectTimeout` is a subclass of **both** `ConnectionError` and `Timeout`. So `except ConnectionError` will also catch a connect timeout. Order your `except` clauses from most specific to least specific.
- `requests.exceptions.JSONDecodeError` inherits from `RequestException` **and** from Python's built-in `ValueError`, so either `except ValueError` or `except RequestException` will catch it.
- A plain `404` is **not** an exception, unless you call `raise_for_status()`.

Putting it together, here is a pattern that handles each case separately:

```python
import requests

def fetch(url):
    try:
        response = requests.get(url, timeout=3)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.Timeout:
        print("Timed out: server too slow")
    except requests.exceptions.ConnectionError as e:
        print("Could not connect:", type(e).__name__)
    except requests.exceptions.HTTPError as e:
        print("Bad status:", e.response.status_code)
    except requests.exceptions.JSONDecodeError:
        print("Answer was not JSON")
    except requests.exceptions.RequestException as e:
        print("Some other requests problem:", e)
    return None
```

Line by line:

- `def fetch(url):` defines a reusable function that takes the URL.
- The `try` block does the happy path: send, check status, parse JSON, and `return` the data. If everything works, none of the `except` blocks runs.
- Python checks `except` clauses **in order** and runs the first match. `Timeout` comes first so a timeout is not swallowed by the more general clauses. `ConnectionError` comes before `RequestException`. The last clause, `RequestException`, is a safety net for anything not covered above (for example an invalid URL).
- `return None` after the `try` statement is reached only if an exception was handled: the function then returns `None` to signal "no data".

We ran this against the local mock: a missing post printed `Bad status: 404`, an HTML body printed `Answer was not JSON`, an unused port printed `Could not connect: ConnectionError`, and a slow endpoint printed `Timed out: server too slow`; each call returned `None`.

#### Catching the empty-body mistake

A frequent surprise is a `204 No Content` response. It has no body, so `.json()` raises `JSONDecodeError`. Guard against it:

```python
r = requests.delete(f"{BASE_URL}/posts/1", timeout=5)
data = r.json() if r.text else None
```

Line by line: `r.text` is an empty string (falsy) when there is no body, so the conditional expression returns `None` instead of calling `.json()`. JSONPlaceholder answers this particular `DELETE` with `{}`, so `data` is `{}`; a stricter API that returns `204` would give `None`.

### 12. Sessions: Reuse Settings, Cookies, and Connections

Every call to `requests.get(...)` on its own is independent: it opens a connection, sends one request, reads one response, and forgets everything. Real conversations are not like that. You log in, then you make ten more calls that all need the same headers, and perhaps a cookie the server gave you. A `requests.Session` is an object that **remembers** settings between calls and **reuses** the underlying network connection (called connection pooling or keep-alive), which is faster.

```python
with requests.Session() as session:
    session.headers.update({"Accept": "application/json", "User-Agent": "qea-tests/1.0"})

    r1 = session.get(f"{BASE_URL}/whoami", timeout=5)
    r2 = session.get(f"{BASE_URL}/whoami", headers={"Accept": "text/plain"}, timeout=5)
    print(r1.json())
    print(r2.json())
```

Line by line:

- `with requests.Session() as session:` creates a session and guarantees it is closed when the block ends, even if an error happens. This is called a **context manager**.
- `session.headers.update({...})` sets default headers for **every** call made through this session. `session.headers` is a dictionary-like object; `update` adds or overwrites keys.
- `session.get(...)` is used exactly like `requests.get(...)`, and so are `post`, `put`, `patch`, and `delete`.
- The second call passes its own `headers={"Accept": "text/plain"}`. Per-request headers are **merged** with the session headers, and the per-request value wins when both set the same name.

Our local mock has a `/whoami` endpoint that echoes the headers it received. Output (verified):

```
{'cookie': None, 'ua': 'qea-tests/1.0', 'accept': 'application/json'}
{'cookie': None, 'ua': 'qea-tests/1.0', 'accept': 'text/plain'}
```

Both calls carried the session's `User-Agent`, and the second overrode `Accept`.

#### Sessions remember cookies

```python
with requests.Session() as s:
    s.get(f"{BASE_URL}/setcookie", timeout=5)      # server replies with Set-Cookie
    print(s.cookies.get_dict())
    print(s.get(f"{BASE_URL}/whoami", timeout=5).json()["cookie"])

print(requests.get(f"{BASE_URL}/whoami", timeout=5).json()["cookie"])
```

The first call receives a `Set-Cookie` header; the session stores it. The next call through the same session automatically sends it back as a `Cookie` header, just as a browser does. A plain `requests.get()` at the end has no memory, so it sends no cookie. Output (verified):

```
{'sid': 'abc123'}
sid=abc123
None
```

This is how session-cookie logins work: log in once, and every later call is authenticated. Token-based APIs use a header instead, and you will put that token in `session.headers` in the authentication lesson.

#### The big gotcha: sessions have no default timeout

Setting `session.timeout = 5` does **nothing**: the attribute is ignored. You must pass `timeout=` on every call, or centralise it. A tidy way is a small subclass that injects a default:

```python
class TimeoutSession(requests.Session):
    def __init__(self, default_timeout=5):
        super().__init__()
        self.default_timeout = default_timeout

    def request(self, method, url, **kwargs):
        kwargs.setdefault("timeout", self.default_timeout)
        return super().request(method, url, **kwargs)
```

Line by line: the class inherits everything from `Session`. `__init__` runs when you create one, calls the parent's setup with `super().__init__()`, and stores a default. Every helper (`get`, `post`, ...) passes through `request`, so we override it: `kwargs.setdefault("timeout", ...)` adds a timeout **only if the caller did not provide one**, then hands over to the original `request`. Now `TimeoutSession().get(url)` can never hang. Pass an explicit `timeout=` to override, as you would for the slow endpoint.

**Session isolation in tests.** A session keeps state, so keep sessions short-lived and do not let one test's cookies or headers leak into the next.

### 13. Redirects: `allow_redirects`, `history`, and Loops

Recall from Monday that `3xx` responses with a `Location` header tell the client to go somewhere else. By default, `requests` **follows redirects automatically** for every method except `HEAD`, and gives you the final response. The earlier hops are kept in `response.history`.

Our mock has `/redirect`, which answers `301` with `Location: /posts/1`:

```python
r = requests.get(f"{BASE_URL}/redirect", timeout=5)
print(r.status_code, r.url)
print([h.status_code for h in r.history])
print(r.history[0].headers["Location"])
```

Line by line: the final response has status `200` and its `url` is where we ended up, not where we started. `r.history` is a list of `Response` objects for each intermediate redirect, oldest first. We print their status codes in a list comprehension and read the `Location` header of the first hop. Output (verified):

```
200 http://127.0.0.1:8099/posts/1
[301]
/posts/1
```

Now turn following off, which is what you want when the **redirect itself** is the thing under test (for example, "the old URL must answer `301` pointing at the new one"):

```python
r = requests.get(f"{BASE_URL}/redirect", allow_redirects=False, timeout=5)
print(r.status_code, r.url, r.headers["Location"], r.is_redirect)
```

`allow_redirects=False` stops at the first response. Output (verified):

```
301 http://127.0.0.1:8099/redirect /posts/1 True
```

`is_redirect` is `True` for a redirect response that carries a `Location`. Note that `Location` can be a relative path, as here; `requests` resolves it for you when following.

**Redirect loops.** If two URLs redirect to each other forever, `requests` stops after 30 hops and raises `requests.exceptions.TooManyRedirects` ("Exceeded 30 redirects."). You can lower the limit with `session.max_redirects`.

### 14. HTTPS, Certificates, and `verify=`

When you call an `https://` URL, `requests` performs a TLS handshake and checks the server's certificate: is it issued by a trusted authority, does the name match the host, and is it unexpired? By default `verify=True`, and `requests` uses the certificate bundle from the `certifi` package. If a check fails, you get `requests.exceptions.SSLError` (a kind of `ConnectionError`).

We can see this safely by calling an HTTPS URL on a server that only speaks HTTP:

```python
try:
    requests.get("https://127.0.0.1:8099/", timeout=3)
except requests.exceptions.SSLError as e:
    print("SSLError, parent:", type(e).__mro__[1].__name__)
```

Output (verified):

```
SSLError, parent: ConnectionError
```

Three ways people deal with certificate problems, from worst to best:

| Approach | Code | Verdict |
|----------|------|---------|
| Turn verification off | `requests.get(url, verify=False)` | Only for a throwaway local experiment. It makes the connection open to impersonation, and `urllib3` prints a warning on every call. Never commit it to shared test code. |
| Point to a custom CA file | `requests.get(url, verify="/path/company-ca.pem")` | Correct for company test environments with an internal certificate authority. |
| Use the system or env bundle | Set the `REQUESTS_CA_BUNDLE` environment variable | Correct for corporate proxies that re-sign traffic; keeps code clean. |

A tester's rule: **an `SSLError` is a finding about the environment, not a reason to disable security.** Ask who owns the certificate. If a staging server has an expired certificate, report it. If your company proxy inserts its own certificate, use the bundle approach. Never ship `verify=False` into a pipeline: it hides exactly the kind of misconfiguration that tests should catch.

### 15. Retries: The Idea

Networks and servers fail in short, transient ways: a `503` while a service restarts, a connection reset, a momentary timeout. A **retry** sends the request again after a short wait. Done well, it makes pipelines more stable. Done badly, it hides real defects or hammers a struggling server.

Principles:

1. **Retry only transient failures**: connection errors, timeouts, and `502`/`503`/`504`. Never retry `400`, `401`, `403`, or `404`; they will fail the same way every time.
2. **Retry only safe (idempotent) requests** by default: `GET`, `HEAD`, `PUT`, `DELETE`. Retrying a `POST` can create duplicates, because the first attempt may have succeeded before the connection dropped.
3. **Back off**: wait longer after each failure (for example 1 s, 2 s, 4 s) so you do not pile onto a server in trouble. Respect a `Retry-After` header if the server sends one.
4. **Limit attempts**: give up after a small number and fail loudly.
5. **Record it**: log each retry. A test that passes only on the third try is a warning sign, not a success.

A manual version, to see the logic with nothing hidden:

```python
import time
import requests

def get_with_retry(url, attempts=3, delay=0.1):
    last = None
    for n in range(1, attempts + 1):
        try:
            r = requests.get(url, timeout=2)
            if r.status_code < 500:
                return r
            last = r
        except (requests.exceptions.ConnectionError, requests.exceptions.Timeout) as e:
            last = e
        time.sleep(delay * n)
    raise RuntimeError(f"gave up after {attempts} attempts: {last!r}")
```

Line by line:

- The `for` loop counts attempts from `1` to `attempts`.
- Inside `try`, we send the request. A status below `500` (success, redirect, or client error) is returned immediately: a `404` is a real answer, not a transient fault.
- A `5xx` is remembered in `last` and we loop again.
- A connection error or timeout is also remembered in `last` (note the tuple of exception classes in `except`).
- `time.sleep(delay * n)` waits longer each round (linear backoff: 0.1 s, 0.2 s, 0.3 s here; use bigger numbers for real APIs).
- After the loop ends with no success, `raise RuntimeError(...)` fails loudly. `{last!r}` inserts the `repr` of the last problem.

Against the mock's `/status/500` endpoint, which always fails, the output (verified) is:

```
gave up after 3 attempts: <Response [500]>
```

The library can do this for you with `urllib3`'s `Retry` and a transport adapter:

```python
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

retry = Retry(total=3, backoff_factor=0.5,
              status_forcelist=[502, 503, 504],
              allowed_methods=["GET", "HEAD"])

with requests.Session() as s:
    s.mount("https://", HTTPAdapter(max_retries=retry))
    s.mount("http://", HTTPAdapter(max_retries=retry))
    r = s.get(f"{BASE_URL}/flaky", timeout=5)
    print(r.status_code)
```

Line by line:

- `Retry(total=3, ...)` describes the policy: at most three retries. `backoff_factor=0.5` makes the waits grow (roughly 0.5 s, 1 s, 2 s, ...). `status_forcelist` lists the status codes that count as "try again". `allowed_methods` limits retries to safe methods.
- `s.mount(prefix, adapter)` attaches a transport adapter to a session for every URL starting with that prefix. We mount for both `https://` and `http://`.
- `HTTPAdapter(max_retries=retry)` is the object that actually sends requests and applies the policy.
- The call to `/flaky` fails twice with `503` (the mock also sends `Retry-After: 1`, which `Retry` honours by default) and succeeds on the third try. Output (verified): `200`. The run is therefore a little slower than a normal call.

Keep one thing in mind for testing: **retries inside the test client can hide real flakiness in the API under test.** Many teams retry only in setup code and let the assertions themselves run once. Pipeline-level retry policy is covered on Friday.

### 16. Looking Under the Hood: `PreparedRequest`

When you call `requests.get(...)`, the library goes through these steps: it builds a `Request` object from your arguments, merges in session defaults, converts that into a **`PreparedRequest`** (the final method, URL, headers, and body bytes), sends it, and wraps the answer in a `Response`. Seeing the prepared request answers the question every tester asks sooner or later: *"What exactly did my code send?"*

**After the fact**: every response keeps its request.

```python
r = requests.get(f"{BASE_URL}/posts", params={"userId": 2}, timeout=5)
print(r.request.method)
print(r.request.url)
print(dict(r.request.headers))
print(r.request.body)
```

`r.request` is the `PreparedRequest`. Output (verified):

```
GET
http://127.0.0.1:8099/posts?userId=2
{'User-Agent': 'python-requests/2.34.2', 'Accept-Encoding': 'gzip, deflate', 'Accept': '*/*', 'Connection': 'keep-alive'}
None
```

The body is `None` because a `GET` has none.

**Before sending**: build and inspect without a network at all.

```python
req = requests.Request("GET", f"{BASE_URL}/posts",
                       params={"userId": 2},
                       headers={"Accept": "application/json"})
prepared = req.prepare()
print(prepared.method, prepared.url)
print(dict(prepared.headers))

with requests.Session() as s:
    prepared = s.prepare_request(req)    # merges the session's defaults
    response = s.send(prepared, timeout=5)
    print(response.status_code)
```

Line by line:

- `requests.Request(method, url, ...)` is a plain description. Nothing is sent and no defaults are added.
- `.prepare()` produces the final message. Output (verified): `GET http://127.0.0.1:8099/posts?userId=2` and `{'Accept': 'application/json'}`. Notice that no `User-Agent` appears: the bare `Request` has not been merged with session defaults.
- `s.prepare_request(req)` does the merge, including session headers and cookies.
- `s.send(prepared, timeout=5)` actually transmits it. Output (verified): `200`.

Use this when you want to assert on what your *own code builds* (for instance, that a helper adds the right header, or that `json=` produced a `Content-Type`) without needing a live server. It is also how section 6.3 proved the difference between `json=` and `data=`.

### 17. From Postman to Python, and a Small Reusable Client

#### 17.1 Side-by-side translation

Postman request (from Monday): `POST {{baseUrl}}/posts`, Body *raw JSON*, header `Accept: application/json`, and a test that the status is `201`.

```python
import requests

BASE_URL = "https://jsonplaceholder.typicode.com"

def test_create_post_returns_201():
    response = requests.post(
        f"{BASE_URL}/posts",
        json={"title": "From Python", "body": "Same call", "userId": 1},
        headers={"Accept": "application/json"},
        timeout=5,
    )
    assert response.status_code == 201
```

Postman-to-Python mapping:

| Postman | Python |
|---------|--------|
| `{{baseUrl}}` variable | `BASE_URL` constant (or config) |
| Params tab | `params={...}` |
| Headers tab | `headers={...}` |
| Body > raw > JSON | `json={...}` |
| Body > x-www-form-urlencoded | `data={...}` |
| Test: `pm.response.to.have.status(201)` | `assert response.status_code == 201` |
| `pm.response.json()` | `response.json()` |
| `pm.environment.set("id", x)` | a Python variable, or a fixture later |
| Collection runner | a PyTest run |
| Setting a timeout in settings | `timeout=` on every call |

The function name starts with `test_` and the check is an `assert`: that is the shape PyTest recognises. The PyTest lesson later today builds on it, so do not worry about running it with PyTest yet.

#### 17.2 A reusable client class

Repeating the base URL, timeout, and headers in every call is where mistakes creep in. A small wrapper removes the repetition. This is a simplified preview of what your Project 2 API layer will look like:

```python
import requests

class ApiClient:
    def __init__(self, base_url, timeout=5):
        self.base_url = base_url.rstrip("/")
        self.timeout = timeout
        self.session = requests.Session()
        self.session.headers.update({"Accept": "application/json"})

    def request(self, method, path, **kwargs):
        kwargs.setdefault("timeout", self.timeout)
        return self.session.request(method, f"{self.base_url}{path}", **kwargs)

    def get(self, path, **kwargs):
        return self.request("GET", path, **kwargs)

    def post(self, path, **kwargs):
        return self.request("POST", path, **kwargs)

    def close(self):
        self.session.close()

client = ApiClient("https://jsonplaceholder.typicode.com/")
r = client.get("/posts/1")
print(r.status_code, r.request.url)
client.close()
```

Line by line:

- `__init__` stores the base URL (with any trailing `/` removed by `rstrip("/")` so we never produce a double slash), the default timeout, and a `Session` with a default `Accept` header.
- `request` is the one place every call goes through. `kwargs.setdefault("timeout", ...)` guarantees a timeout, and `self.session.request(method, url, **kwargs)` sends it. `**kwargs` forwards anything extra, such as `params=` or `json=`.
- `get` and `post` are thin shortcuts. You would add `put`, `patch`, and `delete` the same way.
- `close` releases the session.
- The last four lines use the client. Verified locally, the output is `200 http://127.0.0.1:8099/posts/1`; against JSONPlaceholder it prints `200 https://jsonplaceholder.typicode.com/posts/1`.

Later in the week you will make a client like this into a PyTest **fixture** so every test receives a ready-to-use client; see the fixtures lesson later today.

### 18. Debugging Checklist

When a request does not behave, work through these in order:

1. **Print `response.status_code` and `response.text`** (not `.json()`) first. The text often holds the real error message.
2. **Print `response.request.url`, `.headers`, and `.body`** to see what was actually sent. Compare it character by character with a request that works in Postman.
3. **Check `json=` versus `data=`** if you got `400` or `415`.
4. **Check the URL**: wrong base, double slash, missing `/`, or a `params=` value that was dropped because it was `None`.
5. **Check headers** (`Accept`, `Content-Type`, `User-Agent`) if Postman works but Python gets `403` or `406`.
6. **Read the exception name** if there is no response at all.
7. **Look at `response.history`** if the final URL is not the one you called.
8. **Look at `response.elapsed`** if the test is slow or flaky.

### 19. Common Beginner Mistakes

1. **Forgetting `timeout=`.** The program can hang forever. Always set it, or use a client wrapper that does.
2. **Using `data=` where `json=` is needed** (or the reverse). Causes `400` and `415`.
3. **Calling `.json()` on an empty or non-JSON body**, for example `204 No Content` or an HTML error page.
4. **Comparing `status_code == "200"`** (a string) instead of `200` (an integer). The comparison is always `False`.
5. **Treating `response.ok` as success.** It is `True` for `3xx` as well. Assert the exact expected code.
6. **Calling `raise_for_status()` in a negative test**, which crashes a test that expects `404` or `400`.
7. **Hard-coding the base URL** in every call instead of using one constant or configuration.
8. **Building query strings by hand**, which breaks on spaces and `&`.
9. **Installing packages globally** rather than in a virtual environment, and forgetting `requirements.txt`.
10. **Retrying `POST` blindly**, creating duplicate records.
11. **Naming a file `requests.py`.** Python imports your file instead of the library, and you get a confusing `AttributeError`. Never name a script after a library.

### 20. Practice Exercises

Run these against JSONPlaceholder. Write your own answer first, then compare with the solution. Every solution was run against the local mock.

**Exercise 1.** Fetch `/users/1` and print the user's `name` and `email`.

**Exercise 2.** Fetch `/posts` with `params={"userId": 3}` and print how many posts there are and the `id` of the first.

**Exercise 3.** Request `/posts/99999`, print the status code, then use `raise_for_status()` inside `try`/`except` to catch the `HTTPError` and print a friendly message.

**Exercise 4.** Without sending anything, use `requests.Request(...).prepare()` to show that `json=` and `data=` produce different `Content-Type` headers and bodies for `{"title": "Hi", "userId": 1}`.

**Exercise 5.** Write `get_json(url)` that returns parsed JSON, returns `None` for a `404`, and raises `RuntimeError` for any other non-2xx status or for non-JSON text. Use a timeout.

#### Solutions

**Solution 1.**

```python
import requests

BASE_URL = "https://jsonplaceholder.typicode.com"

r = requests.get(f"{BASE_URL}/users/1", timeout=5)
user = r.json()
print(user["name"], user["email"])
```

`r.json()` turns the body into a dictionary, and we read two keys. Output (verified locally, and the same values appear on JSONPlaceholder): `Leanne Graham Sincere@april.biz`.

**Solution 2.**

```python
r = requests.get(f"{BASE_URL}/posts", params={"userId": 3}, timeout=5)
posts = r.json()
print(len(posts), posts[0]["id"])
```

The response is a list of dictionaries. `len(posts)` is the count and `posts[0]` is the first item. Representative output from JSONPlaceholder: `10 21`. (Each user has ten posts and user 3 owns ids 21 to 30.)

**Solution 3.**

```python
r = requests.get(f"{BASE_URL}/posts/99999", timeout=5)
print(r.status_code)
try:
    r.raise_for_status()
except requests.exceptions.HTTPError as err:
    print("Expected failure, server said:", err.response.status_code)
```

Output: `404` then `Expected failure, server said: 404`.

**Solution 4.**

```python
payload = {"title": "Hi", "userId": 1}
for label, kwargs in (("json", {"json": payload}), ("data", {"data": payload})):
    p = requests.Request("POST", f"{BASE_URL}/posts", **kwargs).prepare()
    print(label, "->", p.headers["Content-Type"], "|", p.body)
```

Output (verified): `json -> application/json | b'{"title": "Hi", "userId": 1}'` then `data -> application/x-www-form-urlencoded | title=Hi&userId=1`. The loop pairs a label with each set of keyword arguments, and `**kwargs` passes it through.

**Solution 5.**

```python
def get_json(url):
    r = requests.get(url, timeout=5)
    if r.status_code == 404:
        return None
    if not r.ok:
        raise RuntimeError(f"Unexpected status {r.status_code} for {url}")
    try:
        return r.json()
    except requests.exceptions.JSONDecodeError:
        raise RuntimeError(f"Not JSON: {r.text[:80]!r}")
```

The function handles the three outcomes in order. A `404` is an expected "not found" and returns `None`. Any other `4xx` or `5xx` is a surprise, so we raise. For a success status we try to parse, and convert a parse failure into a clear message that includes the first 80 characters of the body. We checked `get_json(f"{BASE_URL}/posts/1")` returns a dictionary, `get_json(f"{BASE_URL}/posts/99999")` returns `None`, `get_json(f"{BASE_URL}/status/500")` raises `Unexpected status 500`, and `get_json(f"{BASE_URL}/html")` raises `Not JSON: '<html>oops</html>'`.

### 21. Self-Check Quiz

Answer without looking back, then check the key.

1. What happens if you call `requests.get(url)` with no `timeout` and the server never responds?
2. `requests.post(url, data={"a": 1})` sends which `Content-Type`?
3. A server returns `404`. Does `requests.get()` raise an exception?
4. What does `response.ok` return for a `302`?
5. Which two phases does a `timeout=(3, 10)` tuple control?
6. Which exception is raised when DNS fails or the connection is refused?
7. You set `session.timeout = 5`. Does that protect your calls?
8. How do you prevent `requests` from following a redirect, and how do you see the hops it did follow?
9. What do `params={"tag": ["x", "y"], "skip": None}` produce?
10. When is `verify=False` acceptable, and why is it dangerous otherwise?
11. Which HTTP methods are safe to retry automatically by default, and why not `POST`?
12. How can you see exactly what a request will send without sending it?

**Answer key.**

1. It waits forever: the program, test, or pipeline job hangs. Always set `timeout=`.
2. `application/x-www-form-urlencoded`, with the body `a=1`.
3. No. `404` is a normal `Response`. An exception appears only if you call `raise_for_status()`.
4. `True`, because `ok` means "status below 400". Assert the exact code instead.
5. The connect timeout (3 s) and the read timeout (10 s).
6. `requests.exceptions.ConnectionError` (a timeout during connect is `ConnectTimeout`, which is also a `ConnectionError`).
7. No. The attribute is ignored. Pass `timeout=` on each call or inject it in a subclass or client wrapper.
8. `allow_redirects=False` stops at the first response; `response.history` lists the hops that were followed.
9. The query string `?tag=x&tag=y`. `None` values are dropped.
10. Only for a local throwaway experiment. Otherwise it disables certificate checking, allowing impersonation and hiding real environment faults. Use `verify="/path/ca.pem"` or `REQUESTS_CA_BUNDLE`.
11. `GET`, `HEAD`, `PUT`, `DELETE`, because repeating them has the same effect. A `POST` may have already created a record before the connection dropped, so a retry can duplicate it.
12. Build a `requests.Request(...)` and call `.prepare()`, then print its `method`, `url`, `headers`, and `body`.

### 22. Glossary

| Term | Meaning |
|------|---------|
| **requests** | The third-party Python library for sending HTTP requests. |
| **virtual environment (venv)** | An isolated folder of Python packages for one project. |
| **pip** | Python's package installer. |
| **Response** | The object `requests` returns, holding status, headers, and body. |
| **status_code** | The integer HTTP status in the response, such as `200`. |
| **ok** | `True` when the status code is below 400. |
| **json()** | Method that parses the response body as JSON into Python data. |
| **params** | A dictionary that `requests` turns into a percent-encoded query string. |
| **json= / data=** | Keyword arguments for a JSON body / a form body (or raw bytes). |
| **headers** | A dictionary of request headers (and the case-insensitive dictionary of response headers). |
| **timeout** | The maximum seconds to wait; by default there is none. |
| **connect timeout / read timeout** | The time limits for establishing the connection and for waiting on data. |
| **RequestException** | The base class of every exception `requests` raises. |
| **ConnectionError** | Exception for network failures: DNS error, refused or reset connection. |
| **HTTPError** | Exception raised by `raise_for_status()` for 4xx and 5xx. |
| **raise_for_status()** | Method that raises `HTTPError` for an error status. |
| **Session** | An object that persists headers, cookies, and connections across calls. |
| **redirect / history** | A `3xx` instruction to go elsewhere / the list of redirect responses followed. |
| **TLS / certificate** | The encryption protocol behind HTTPS and the document that proves a server's identity. |
| **verify** | The argument controlling certificate checking (`True`, `False`, or a CA file path). |
| **retry / backoff** | Resending a failed request, with growing waits between attempts. |
| **idempotent** | A request that has the same effect whether sent once or many times (`GET`, `PUT`, `DELETE`). |
| **PreparedRequest** | The final, ready-to-send form of a request (method, URL, headers, body). |
| **JSONPlaceholder** | A free fake REST API for practice; it does not save changes. |

---

## Summary

- `requests` is the standard Python library for HTTP. Install it inside a virtual environment and record it in `requirements.txt`.
- Each method has a function: `get`, `post`, `put`, `patch`, `delete`. Use `params=` for query strings, `json=` for JSON bodies, `data=` for form bodies, and `headers=` for headers.
- The `Response` object carries `status_code`, `ok`, `headers`, `text`, `content`, `json()`, `elapsed`, `url`, `history`, `cookies`, and the `request` that was sent.
- `requests` does not raise on `4xx` and `5xx`. `raise_for_status()` does. Use it in setup code; assert exact status codes inside tests.
- Always pass `timeout=`, because the default is to wait forever. Know `ConnectionError`, `Timeout`, `HTTPError`, `JSONDecodeError`, and `TooManyRedirects`.
- A `Session` shares headers, cookies, and connections, but has no default timeout.
- Redirects are followed by default; use `allow_redirects=False` and `history` to inspect them. Treat an `SSLError` as an environment finding and avoid `verify=False`.
- Retry only transient failures, only safe methods, with backoff and a limit.
- `Request(...).prepare()` and `response.request` show exactly what is sent.
- Wrap these calls in a small client so base URL, headers, and timeout live in one place.
- Coming up: the PyTest structure, status-code validation, JSON validation, authentication headers, and fixtures and parametrization each have their own lesson later today. Data-driven testing and mocking are covered on Wednesday, accessibility testing on Thursday, and running everything in CI/CD on Friday.

## Additional Resources

- Requests documentation, *Quickstart* (passing parameters, response content, headers, cookies, timeouts, redirects): https://requests.readthedocs.io/en/latest/user/quickstart/
- Requests documentation, *Advanced Usage* (Sessions, prepared requests, SSL verification, transport adapters): https://requests.readthedocs.io/en/latest/user/advanced/
- Requests documentation, *API reference* (`Response`, `Session`, exceptions): https://requests.readthedocs.io/en/latest/api/
- urllib3 documentation, *Retrying requests* (`Retry` options): https://urllib3.readthedocs.io/en/stable/reference/urllib3.util.html#urllib3.util.Retry
- Python documentation, *Virtual environments and packages*: https://docs.python.org/3/tutorial/venv.html
- MDN Web Docs, *HTTP redirections*: https://developer.mozilla.org/en-US/docs/Web/HTTP/Guides/Redirections
- JSONPlaceholder, the practice API and its guide: https://jsonplaceholder.typicode.com/guide/
