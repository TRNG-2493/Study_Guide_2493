# JSON Response Validation

## Learning Objectives

By the end of this lesson you will be able to:

- Explain why a `200 OK` status code is not proof that an API response is correct, and describe the layers of checking that come after the status code.
- Convert a response into Python data with `response.json()`, explain how JSON types map to Python types, and recognise the JSON mistakes (single quotes, trailing commas, empty bodies) that break parsing.
- Catch and explain `JSONDecodeError`, and write a `safe_json` helper that turns an obscure parsing crash into a clear test failure.
- Navigate nested objects and lists, and diagnose `KeyError`, `IndexError`, and `TypeError` when a path is wrong.
- Write field-level assertions for presence, type, value, format, and range, including the `bool`-is-an-`int` trap.
- Tell apart a missing key, `null`, an empty string, an empty list, and `0`, and handle each with `dict.get()` and explicit `is None` checks.
- Validate lists: exact length, "every item satisfies a rule", "at least one item satisfies a rule", uniqueness, and ordering, and produce failure messages that name the offending items.
- Compare a response with expected data using full equality, partial dictionary comparison, and "echo" checks after a `POST`.
- Avoid floating-point and ordering traps with `pytest.approx`, integer cents, `Decimal`, and order-insensitive comparisons.
- Use the `jsonschema` library at a basic level: `validate()`, `ValidationError`, and a simple schema built from `type`, `required`, and `properties`.
- Build a small, readable JSON-validation test module that you can reuse in your Project 2 framework.

---

## Why This Matters

Picture this. A mobile banking team releases a new version of their API on a Friday afternoon. The automated test suite is green. Every test does the same thing: it sends a request and asserts `response.status_code == 200`. All of them pass, and the release goes out.

On Saturday morning, support is flooded with complaints. The account balance screen shows `NaN`. The transactions list is empty for some customers and crashes the app for others. What went wrong? The server was returning `200 OK` for every request, exactly as the tests demanded. But inside the response bodies:

- The balance had changed from a number (`1520.75`) to a string (`"1520.75"`), and the app's arithmetic broke.
- For customers with no transactions, the `transactions` field was now `null` instead of an empty list `[]`, and the app tried to loop over `null`.
- One endpoint, under load, returned an HTML "Bad Gateway" page with a `200` status from a misconfigured proxy, and the app's JSON parser threw an exception.

Every one of those defects was invisible to a status-code check. Every one of them could have been caught by a few lines of body validation.

That is the lesson in a sentence: **a status code tells you the server answered; the body tells you whether the answer is correct.** In the previous lesson on status codes you learned to verify the first half. Today you learn the second half.

Why does this matter so much for API testing in particular?

1. **APIs have no screen.** A human testing a website would notice a missing price or a garbled name immediately. An API response is just text. If your automated test does not look at the content, nobody does.
2. **Clients depend on the exact shape.** Mobile apps, web front ends, and other services were written against a specific structure: these field names, these types, this nesting. A small change in shape is a breaking change, even when the status code is still `200`.
3. **Data defects are expensive.** A wrong price, a duplicated record, or a leaked internal field can cost money or damage trust in ways a crashed server never does.
4. **It makes your tests precise.** When a test fails with the message `'7' is not of type 'integer'` at path `['id']`, the developer knows exactly where to look. That is the difference between a useful test suite and a noisy one.

In your Project 2 framework, JSON validation is the layer that sits on top of the HTTP plumbing you built in the earlier lessons (the `requests` library, the test structure, fixtures, and header handling). By the end of today you will have a toolbox of assertion patterns, a safe parsing helper, and a first schema-based check that you can drop into that framework.

> **Scope note.** This lesson teaches how to check what comes back in a response body, using plain Python assertions and the basics of the `jsonschema` library. Deeper request and response validation is covered on Wednesday. Today we stay with the fundamentals so that you have a solid base.

---

## The Concept

### 1. What "Validating a Response" Really Means

Validation is not one check. It is a stack of checks, and each layer protects you from a different kind of failure. Think of it as security screening at an airport: your ticket, your passport, your bag scan, and your boarding pass are all checked, and passing one does not skip the others.

| Layer | Question | Example failure | Where it is taught |
|-------|----------|-----------------|--------------------|
| 1. Transport | Did we get a response at all? | Timeout, connection refused | Earlier this week |
| 2. Status and headers | Is the status code and `Content-Type` right? | `500` instead of `200` | Status code lesson, headers lesson |
| 3. Parsing | Is the body valid JSON? | HTML error page, empty body, truncated text | **Today, sections 3 to 4** |
| 4. Shape | Does it have the right fields, types, and nesting? | `price` is a string | **Today, sections 5, 6, 10** |
| 5. Content | Are the values correct? | Wrong user returned | **Today, sections 5 to 9** |
| 6. Consistency | Do the values agree with each other and with what we sent? | `total` does not equal the sum of line items | **Today, sections 8, 9** |

A good API test touches several layers in order. You always check the cheap, general things first (status, parsing) because if they fail, the deeper checks make no sense. There is no point asserting that `body["name"] == "Ann"` when the body is an HTML error page.

#### The practice lab used in this lesson

Most public practice APIs live on the internet, and their outputs change over time (and may be blocked on some networks). So that every example in this lesson is reproducible on your own machine, we use a tiny local API called the **lab server**. It imitates the popular JSONPlaceholder data (users, posts, comments, todos) and adds an `orders` and `products` endpoint, plus some deliberately broken endpoints that we use to demonstrate failures. All outputs shown in this lesson were produced against this lab server.

Save this as `lab_server.py` and run it in a separate terminal with `python lab_server.py`. It uses only Python's standard library, so there is nothing to install.

```python
"""lab_server.py - a tiny local API for practising JSON validation.
Run:  python lab_server.py     (listens on http://127.0.0.1:8000)
"""
import json
from http.server import BaseHTTPRequestHandler, HTTPServer
from urllib.parse import urlparse, parse_qs

USERS = [
    {"id": i, "name": f"User {i}", "username": f"user{i}", "email": f"user{i}@example.com",
     "phone": None if i % 2 == 0 else f"555-000{i}",
     "address": {"city": "Gwenborough", "geo": {"lat": "-37.3159", "lng": "81.1496"}},
     "company": {"name": "Romaguera-Crona"}}
    for i in range(1, 11)
]
POSTS = [{"userId": (i - 1) // 10 + 1, "id": i, "title": f"Post {i}", "body": "text"}
         for i in range(1, 31)]
COMMENTS = [{"postId": (i - 1) // 5 + 1, "id": i, "email": f"c{i}@example.com", "body": "hi"}
            for i in range(1, 16)]
PRODUCTS = [
    {"sku": "A1", "name": "Pen", "price": 1.1, "tags": ["office"]},
    {"sku": "B2", "name": "Book", "price": 2.2, "tags": []},
    {"sku": "C3", "name": "Bag", "price": 19.99, "tags": None},
]
ORDER = {"id": 1, "status": "shipped", "coupon": None, "note": "",
         "items": [{"sku": "A1", "qty": 2, "price": 1.1}, {"sku": "B2", "qty": 1, "price": 2.2}],
         "total": 4.4, "createdAt": "2026-10-11T09:30:00Z", "internalId": "x9"}

# Fixed JSON answers (some deliberately wrong, for the "bad response" demonstrations).
FIXED = {
    "/todos/1": (200, {"userId": 1, "id": 1, "title": "buy milk", "completed": False}),
    "/products": (200, PRODUCTS),
    "/orders/1": (200, ORDER),
    "/typo": (200, {"id": "1", "name": "Ann", "active": "true", "score": None}),
    "/bad-user": (200, {"id": "7", "name": "", "email": "not-an-email"}),
    "/dupes": (200, [{"id": 3}, {"id": 1}, {"id": 3}]),
}
# Raw bodies that are NOT valid JSON: (status, body text, content type)
RAW = {
    "/html": (502, "<html><body><h1>Bad Gateway</h1></body></html>", "text/html"),
    "/empty": (204, "", "application/json"),
    "/truncated": (200, '{"id": 1, "name": "Ann', "application/json"),
    "/pyrepr": (200, "{'id': 1}", "application/json"),
}


class Handler(BaseHTTPRequestHandler):
    def log_message(self, *args):          # keep the console quiet
        pass

    def reply(self, status, text, ctype="application/json"):
        data = text.encode()
        self.send_response(status)
        self.send_header("Content-Type", ctype)
        self.send_header("Content-Length", str(len(data)))
        self.end_headers()
        self.wfile.write(data)

    def do_GET(self):
        url = urlparse(self.path)
        path, query = url.path, parse_qs(url.query)
        if path in RAW:
            status, text, ctype = RAW[path]
            return self.reply(status, text, ctype)
        if path in FIXED:
            status, body = FIXED[path]
            return self.reply(status, json.dumps(body))
        if path == "/users":
            return self.reply(200, json.dumps(USERS))
        if path.startswith("/users/") and path[7:].isdigit() and 1 <= int(path[7:]) <= 10:
            return self.reply(200, json.dumps(USERS[int(path[7:]) - 1]))
        if path == "/posts":
            rows = POSTS
            if "userId" in query:
                rows = [p for p in rows if p["userId"] == int(query["userId"][0])]
            return self.reply(200, json.dumps(rows))
        if path == "/comments":
            rows = COMMENTS
            if "postId" in query:
                rows = [c for c in rows if c["postId"] == int(query["postId"][0])]
            return self.reply(200, json.dumps(rows))
        self.reply(404, json.dumps({"error": "not found"}))

    def do_POST(self):
        size = int(self.headers.get("Content-Length", 0))
        body = json.loads(self.rfile.read(size) or b"{}")
        if urlparse(self.path).path == "/posts":
            body["id"] = 101
            return self.reply(201, json.dumps(body))
        self.reply(404, json.dumps({"error": "not found"}))


if __name__ == "__main__":
    print("Lab server on http://127.0.0.1:8000  (Ctrl+C to stop)")
    HTTPServer(("127.0.0.1", 8000), Handler).serve_forever()
```

You do not need to study the server's internals; it is scaffolding. What matters is the list of endpoints it offers:

| Endpoint | What it returns | Why it exists |
|----------|-----------------|---------------|
| `GET /users`, `GET /users/{1..10}` | Users with nested `address`, `company`, and a `phone` that is `null` for even ids | Nested data and `null` handling |
| `GET /posts`, `GET /posts?userId=3` | 30 posts, filterable | Lists and filter checks |
| `GET /comments?postId=1` | 15 comments, filterable | Exercises |
| `POST /posts` | Echoes your JSON and adds `"id": 101` | Echo comparison |
| `GET /products` | Prices as floats; `tags` can be a list, empty, or `null` | Floats and `null` versus empty |
| `GET /orders/1` | An order with line items, a total, and an `internalId` field | Consistency and leak checks |
| `GET /todos/1` | A simple todo | Schema exercise |
| `GET /typo` | `id` as a string, `active` as the string `"true"` | Wrong-type defects |
| `GET /bad-user` | A user with several problems | Schema failures |
| `GET /dupes` | A list with a repeated id, unsorted | Uniqueness and ordering |
| `GET /html` | `502` with an HTML body | Non-JSON body |
| `GET /empty` | `204` with no body | Empty body |
| `GET /truncated` | Cut-off JSON | Corrupt JSON |
| `GET /pyrepr` | `{'id': 1}` with single quotes | Invalid JSON that looks valid |

Now the test project. You need `pytest`, `requests`, and `jsonschema`:

```bash
pip install pytest requests jsonschema
```

Create a `conftest.py` that gives every test a `client` fixture. This mirrors the structure you built in the test-structure and fixtures lessons. The class prepends the base URL and applies a default timeout so that a hung server cannot freeze your test run.

```python
# conftest.py
import pytest
import requests

BASE_URL = "http://127.0.0.1:8000"


class ApiClient:
    """Tiny wrapper: prepends the base URL and applies a default timeout."""

    def __init__(self, base_url):
        self.base_url = base_url
        self.session = requests.Session()

    def get(self, path, **kwargs):
        return self.session.get(self.base_url + path, timeout=10, **kwargs)

    def post(self, path, **kwargs):
        return self.session.post(self.base_url + path, timeout=10, **kwargs)


@pytest.fixture(scope="session")
def client():
    return ApiClient(BASE_URL)
```

Line by line:

- `BASE_URL = ...` is the root of the API. Changing environments (local, staging) means changing this one line, or reading it from an environment variable later in the week.
- `class ApiClient` bundles a `requests.Session` (which reuses connections and is faster) with the base URL.
- `def get(self, path, **kwargs)` accepts a path like `"/users/1"` and any extra `requests` options such as `params=` or `headers=`. `**kwargs` means "pass along whatever extra named arguments the caller gave".
- `timeout=10` is a safety net: if the server does not answer in 10 seconds, `requests` raises an error rather than waiting forever.
- `@pytest.fixture(scope="session")` creates one client for the whole test run and hands it to any test function that has a parameter named `client`.

Every example below that says `client.get(...)` uses this fixture. If you prefer plain scripts while experimenting, `requests.get("http://127.0.0.1:8000/users/1")` behaves identically.

---

### 2. JSON Refresher: What You Are Actually Parsing

**JSON** (JavaScript Object Notation) is a text format for structured data. It is the dominant format for REST APIs because it is compact, human-readable, and supported by every programming language. A JSON response is, at the HTTP level, just a string of characters. The `Content-Type: application/json` header says "this string is JSON", but the header is a claim, not a guarantee. Your tests must verify that the claim is true.

#### The six JSON types

JSON has exactly six kinds of value:

| JSON type | Example | Python type after `json.loads` | Notes |
|-----------|---------|--------------------------------|-------|
| object | `{"id": 1}` | `dict` | Keys must be strings in double quotes |
| array | `[1, 2, 3]` | `list` | Ordered |
| string | `"hello"` | `str` | Double quotes only |
| number | `42` or `19.99` | `int` or `float` | No separate int/float type in JSON; Python decides by the presence of `.` or `e` |
| boolean | `true`, `false` | `True`, `False` | Lowercase in JSON |
| null | `null` | `None` | "No value" |

Pay special attention to three things beginners trip over:

1. **The text `"true"` is a string, not a boolean.** `{"active": "true"}` parses to `{'active': 'true'}`, a string. Only the bare word `true` (no quotes) becomes `True`. This is one of the most common API defects.
2. **`"1"` is a string and `1` is a number.** Same thing. The quotes decide.
3. **`null` is a value.** `{"coupon": null}` means "the field exists and has no value". That is different from the field being absent. We return to this in section 6.

#### JSON syntax rules that cause real parse failures

JSON is stricter than Python dictionary syntax, even though they look alike. A body that looks right to a human can be invalid JSON:

| Mistake | Invalid JSON | Valid JSON |
|---------|--------------|------------|
| Single quotes | `{'id': 1}` | `{"id": 1}` |
| Trailing comma | `{"id": 1,}` | `{"id": 1}` |
| Unquoted key | `{id: 1}` | `{"id": 1}` |
| Comments | `{"id": 1} // note` | not allowed at all |
| Python constants | `{"ok": True, "x": None}` | `{"ok": true, "x": null}` |
| Truncated text | `{"id": 1, "name": "Ann` | complete the string and brace |

The `{'id': 1}` case is especially sneaky: it is what you get if a server developer accidentally prints a Python dictionary instead of serialising it to JSON. It looks plausible in a log, and the parser rejects it.

#### Two functions to know: `loads` and `dumps`

Python's built-in `json` module has two workhorse functions:

```python
import json

data = json.loads('{"a": 1, "b": [true, null]}')   # text  -> Python
print(data)

text = json.dumps({"a": 1, "b": None}, indent=2)   # Python -> text
print(text)
```

Output:

```text
{'a': 1, 'b': [True, None]}
{
  "a": 1,
  "b": null
}
```

Memory aid: the **s** in `loads` and `dumps` stands for **string**. `loads` = "load from string", `dumps` = "dump to string". (`load` and `dump` without the `s` work with files.) The `requests` library's `response.json()` is essentially `json.loads(response.text)` with some extra handling.

A few smaller facts worth knowing, all verified by running them:

- `json.loads("10")` gives an `int`, `json.loads("10.0")` gives a `float`, and `json.loads("1e3")` gives the float `1000.0`. Yet `10.0 == 10` is `True` in Python, so equality checks will not notice the difference; type checks will.
- If a JSON object repeats a key, such as `{"a":1,"a":2}`, Python silently keeps the last one (`{'a': 2}`). A duplicate-key bug in the server is therefore invisible after parsing.
- A valid JSON document does not have to be an object. `json.loads('"just a string"')`, `json.loads('null')`, and `json.loads('[]')` are all legal. This matters: your test should check that the top level is the kind of thing you expect (`dict` or `list`).

---

### 3. Parsing a Response: `response.json()` and `JSONDecodeError`

#### The happy path

```python
def test_parse_user(client):
    response = client.get("/users/1")
    body = response.json()
    print(type(body))
    print(body["name"])
```

Line by line:

- `response = client.get("/users/1")` sends the request and returns a `Response` object. At this moment the entire body has been downloaded.
- `response.json()` reads the body text, runs it through the JSON parser, and returns Python objects. For our user, that is a `dict`.
- `type(body)` confirms what we got. For `/users/1` it prints `<class 'dict'>`; for `/users` it prints `<class 'list'>`.
- `body["name"]` reads one key.

Related attributes of a `Response` you will use constantly:

| Attribute | What it is | When to use it |
|-----------|------------|----------------|
| `response.status_code` | Integer such as `200` | Always check first |
| `response.headers` | Case-insensitive dict-like of headers | Verify `Content-Type` |
| `response.text` | The body as a decoded string | Debugging, error messages |
| `response.content` | The body as raw bytes | Binary data (not JSON) |
| `response.json()` | Parsed Python data | Reading structured bodies |

#### When parsing fails

`response.json()` raises an exception when the body is not valid JSON. Here is what happens against the lab server's deliberately broken endpoints:

```python
import requests

for path in ["/html", "/empty", "/truncated", "/pyrepr"]:
    r = requests.get("http://127.0.0.1:8000" + path)
    try:
        r.json()
        print(path, "ok")
    except ValueError as e:
        print(path, "->", type(e).__name__, "|", e)
```

```text
/html -> JSONDecodeError | Expecting value: line 1 column 1 (char 0)
/empty -> JSONDecodeError | Expecting value: line 1 column 1 (char 0)
/truncated -> JSONDecodeError | Unterminated string starting at: line 1 column 19 (char 18)
/pyrepr -> JSONDecodeError | Expecting property name enclosed in double quotes: line 1 column 2 (char 1)
```

Notice that `/html` and `/empty` produce the identical message, `Expecting value: line 1 column 1 (char 0)`. The parser is saying "I expected the start of a JSON value at the very first character, and found something else (or nothing)". That message alone does not tell you whether you received an HTML page or an empty body. That is exactly why a plain `response.json()` makes a poor test: the failure points at the parser, not at the real problem.

The exception object carries structured detail you can inspect:

```python
r = requests.get("http://127.0.0.1:8000/truncated")
try:
    r.json()
except ValueError as e:
    print(e.msg)        # Unterminated string starting at
    print(e.lineno)     # 1
    print(e.colno)      # 19
    print(e.pos)        # 18
    print(repr(e.doc))  # '{"id": 1, "name": "Ann'
```

`e.pos` is the character index where parsing gave up, and `e.doc` is the text it was parsing. Those two together let you point at the problem.

#### Which exception should you catch?

The name `JSONDecodeError` appears in two places, which confuses people:

- `json.JSONDecodeError` from Python's standard library. It is a subclass of `ValueError`.
- `requests.exceptions.JSONDecodeError`, added in `requests` 2.27. It inherits from both the standard-library error and `requests.exceptions.RequestException`, so it is also catchable as `ValueError`.

The portable, version-proof choice is to catch **`ValueError`**, because both variants (and the older `simplejson` variant that some `requests` versions used) inherit from it. That is what the examples in this lesson do.

#### Why bodies are not JSON: the real-world causes

| Cause | What the body looks like | Typical status | Meaning |
|-------|--------------------------|----------------|---------|
| Gateway or proxy error | HTML page: `<html>...Bad Gateway...` | `502`, `503`, `504` | The app server is down; the gateway answered instead |
| Maintenance or login page | HTML, sometimes with `200` | `200` or `302`-then-`200` | A redirect landed on a web page, not the API |
| No content | Empty string | `204`, or buggy `200` | The endpoint legitimately returns nothing, or crashed silently |
| Server crash mid-response | Truncated JSON | `200` | Connection dropped after headers |
| Developer bug | Python-style `{'id': 1}` or `None` | `200` | Wrong serialisation |
| Wrong content type | Plain text, XML, CSV | any | You asked for the wrong thing or the endpoint changed |

Two of these deserve extra attention. First, **`204 No Content` is a legal, correct response** for operations like `DELETE`, and its body is empty. Calling `.json()` on it always raises. A test for a delete should check the status code and not parse a body at all. Second, notice that an HTML body can arrive with a `200` status, which is why "check the status code, then parse" is not a complete safety net: you should also guard the parse itself.

#### The `safe_json` helper

Create a file `json_helpers.py` in your project:

```python
# json_helpers.py
def safe_json(response):
    """Return response.json(), or fail with a message that explains what the body really was."""
    try:
        return response.json()
    except ValueError:  # JSONDecodeError is a subclass of ValueError
        raise AssertionError(
            f"Body is not valid JSON. status={response.status_code}, "
            f"Content-Type={response.headers.get('Content-Type')!r}, "
            f"first 200 chars={response.text[:200]!r}"
        ) from None
```

Line by line:

- `def safe_json(response):` takes any `requests` response.
- `try: return response.json()` is the normal path. If parsing works, the function returns the parsed data and nothing else happens.
- `except ValueError:` catches every JSON decoding failure (see the previous section for why `ValueError`).
- `raise AssertionError(...)` converts the crash into a test failure. pytest reports `AssertionError` as a failed test with your message, rather than as an "error" with a long parser traceback. That is the presentation you want: the test failed because the API misbehaved.
- `response.status_code` and `response.headers.get('Content-Type')` put the two most useful clues in the message. `.get()` is used on headers so that a missing header gives `None` instead of crashing the error message itself.
- `response.text[:200]` shows only the first 200 characters, so a giant HTML page does not flood your report. The slice `[:200]` means "characters from the start up to (not including) index 200"; if the text is shorter it simply returns all of it.
- `!r` inside an f-string means "use `repr()`", which shows quotes and escape characters (`''` for empty text), so you can tell an empty body from a body containing a space.
- `from None` hides the original parser exception from the chained traceback, because we already put everything useful in our own message. This keeps the report short.

Using it:

```python
from json_helpers import safe_json

def test_safe_json_explains_html(client):
    try:
        safe_json(client.get("/html"))
    except AssertionError as err:
        print(err)
```

Output from the lab server:

```text
Body is not valid JSON. status=502, Content-Type='text/html', first 200 chars='<html><body><h1>Bad Gateway</h1></body></html>'
```

Compare that to the raw `Expecting value: line 1 column 1 (char 0)`. With the helper, a developer reading the CI log immediately sees: the status was `502`, the type was HTML, and the content says "Bad Gateway". The diagnosis is already done.

For the other three broken endpoints the helper produces:

```text
Body is not valid JSON. status=204, Content-Type='application/json', first 200 chars=''
Body is not valid JSON. status=200, Content-Type='application/json', first 200 chars='{"id": 1, "name": "Ann'
Body is not valid JSON. status=200, Content-Type='application/json', first 200 chars="{'id': 1}"
```

Look at the last one: Python chose double quotes around the whole snippet because the snippet itself contains single quotes. This is `repr()` doing its job, and it is what makes the single-quote bug visible.

#### The golden order inside every test

Putting the layers together, a typical test follows this order:

```python
def test_get_user_1(client):
    response = client.get("/users/1")

    assert response.status_code == 200                                   # layer 2
    assert "application/json" in response.headers["Content-Type"]        # layer 2
    body = safe_json(response)                                           # layer 3
    assert isinstance(body, dict)                                        # layer 4
    assert body["id"] == 1                                               # layer 5
```

Checking the status first means that when the server returns `500`, your test fails with "`assert 500 == 200`", which is the real problem, instead of failing later with a confusing parse error.

---

### 4. Navigating Nested Data

Real responses are nested: objects inside objects, lists of objects, objects containing lists. Here is the lab server's user, abbreviated:

```json
{
  "id": 1,
  "name": "User 1",
  "email": "user1@example.com",
  "phone": "555-0001",
  "address": {
    "city": "Gwenborough",
    "geo": { "lat": "-37.3159", "lng": "81.1496" }
  },
  "company": { "name": "Romaguera-Crona" }
}
```

In Python, each level of nesting is one more pair of square brackets:

```python
body = safe_json(client.get("/users/1"))

body["name"]                      # 'User 1'
body["address"]["city"]           # 'Gwenborough'
body["address"]["geo"]["lat"]     # '-37.3159'   (a string, not a number!)
body["company"]["name"]           # 'Romaguera-Crona'
```

Read `body["address"]["geo"]["lat"]` from left to right as a path: "from the body, take `address`; from that, take `geo`; from that, take `lat`". Each step must succeed.

Notice that the latitude is a string. This is how the real JSONPlaceholder service defines it, and it illustrates why you should look at types rather than assuming them: `body["address"]["geo"]["lat"] > 0` would raise a `TypeError` in Python because you cannot compare a string with an integer.

For a list of objects, you combine index brackets and key brackets:

```python
users = safe_json(client.get("/users"))   # a list of 10 dicts

users[0]["name"]                 # first user's name  -> 'User 1'
users[-1]["id"]                  # last user's id     -> 10
[u["id"] for u in users]         # [1, 2, 3, ..., 10]
[u["address"]["city"] for u in users]
```

The expression `[u["id"] for u in users]` is a **list comprehension**: "build a new list by taking each `u` in `users` and recording `u["id"]`". You will use it everywhere in test code, because API validation is mostly "do something with every item".

#### The three errors a wrong path produces

When your path does not match the data, Python raises one of three exceptions. Learning to read them tells you instantly what is wrong with either your test or the API.

| Exception | Cause | Example | What it usually means |
|-----------|-------|---------|-----------------------|
| `KeyError: 'missing'` | The key is not in the dict | `order["missing"]` | The field is absent (API defect or typo in your test) |
| `IndexError: list index out of range` | The list is shorter than your index | `order["items"][5]` when there are 2 items | Fewer items than expected |
| `TypeError: ...` | You treated a value as something it is not | `len(None)`, or `None["x"]`, or `"abc"["x"]` | A `null` where an object or list was expected |

Real examples from the lab server:

```python
order = safe_json(client.get("/orders/1"))
order["items"][5]
# IndexError: list index out of range

products = safe_json(client.get("/products"))
len(products[2]["tags"])
# TypeError: object of type 'NoneType' has no len()
```

The second one is the banking bug from the start of this lesson: `tags` is `null` for the third product, and code that expects a list crashes. When you see `NoneType` in a `TypeError`, think "a `null` arrived where I expected something real".

A crash in the middle of a test is a failure, but a poor one. Section 5 shows how to assert explicitly so that the failure message names the problem. Rule of thumb: **navigate with `[...]` when the field must exist** (a `KeyError` is a legitimate, loud failure), and **use `.get()` when the field may legitimately be absent** (covered in section 6).

---

### 5. Validating Individual Fields

For each field you care about, there are five questions you can ask. Together they make up field-level validation.

| Check | Question | Typical assertion |
|-------|----------|-------------------|
| Presence | Is the field there? | `assert "email" in body` |
| Type | Is it the right kind of value? | `assert isinstance(body["id"], int)` |
| Value | Is it exactly what we expect? | `assert body["id"] == 1` |
| Format | Does the text have the right pattern? | `re.fullmatch(...)`, date parsing |
| Range | Is it within sensible limits? | `assert body["id"] > 0` |

#### 5.1 Presence

```python
def test_user_has_required_fields(client):
    body = safe_json(client.get("/users/1"))
    for field in ("id", "name", "username", "email", "address", "company"):
        assert field in body, f"Missing field: {field}"
```

Line by line:

- `for field in (...)` loops over the field names we require. A tuple (round brackets) is used because the list never changes.
- `field in body` is the Python test "is this key present in the dictionary?". It is `True` or `False` and never raises, and it checks keys only (not values).
- `, f"Missing field: {field}"` is the optional **assertion message**. If the assertion fails, pytest prints this text, so you know which field was missing instead of just `assert False`.

A subtle limitation: this loop stops at the first missing field. If three fields are missing, you learn about one, fix it, rerun, and discover the next. To report all at once, collect first and assert once:

```python
required = {"id", "name", "username", "email", "address", "company"}
missing = required - set(body)
assert not missing, f"Missing fields: {sorted(missing)}"
```

`required - set(body)` is **set subtraction**: "the names in `required` that are not in the body's keys". (`set(body)` turns the dictionary's keys into a set.) `sorted(missing)` makes the message stable and readable, e.g. `Missing fields: ['email', 'phone']`. This pattern, "compute the offenders, then assert the list of offenders is empty", appears throughout this lesson because it produces the best failure messages.

#### 5.2 Exact value

```python
assert body["id"] == 1
assert body["username"] == "user1"
```

Use exact value checks for data you control or that is stable: the id you requested, a seeded record, an enumerated status such as `"shipped"`. Do not hard-code values that legitimately change (timestamps, auto-generated ids, counters); test their type and format instead.

#### 5.3 Data type

```python
assert isinstance(body["id"], int)
assert isinstance(body["name"], str)
assert isinstance(body["address"], dict)
assert isinstance(users, list)
```

`isinstance(value, type)` returns `True` if `value` is that type. Type checks catch the classic defect of a number delivered as a string. Consider the lab server's broken `/typo` endpoint:

```python
t = safe_json(client.get("/typo"))
# {'id': '1', 'name': 'Ann', 'active': 'true', 'score': None}
assert t["id"] == 1
```

The result:

```text
>       assert t["id"] == 1
E       AssertionError: assert '1' == 1
```

pytest's rewritten assertion shows `'1'` with quotes next to `1` without them, so the type bug is visible even with no custom message. Add an explicit type check for a clearer statement of intent: `assert isinstance(t["id"], int), f"id should be int, got {type(t['id']).__name__}"`.

**The `bool` trap.** In Python, `bool` is a subclass of `int`, which leads to a surprise:

```python
isinstance(True, int)      # True   <-- surprising
type(True) == int          # False
type(1) == int             # True
```

So `isinstance(body["id"], int)` would accept `true` as an id. When a bool must not slip through, add an explicit exclusion:

```python
assert isinstance(body["id"], int) and not isinstance(body["id"], bool)
```

Another number subtlety: JSON has one "number" type. If the API returns `5.0` where you expect `5`, Python gives a `float`, and `isinstance(5.0, int)` is `False`, even though `5.0 == 5` is `True`. If your contract says "integer", a float is a defect worth catching, and the type check is the only way to catch it.

#### 5.4 Format

Some strings must follow a pattern: emails, dates, ids, phone numbers, URLs. For these, a type check is not enough because `"not-an-email"` is a perfectly good string.

```python
import re

assert re.fullmatch(r"[^@\s]+@[^@\s]+\.[A-Za-z]{2,}", body["email"]), \
    f"Email format is invalid: {body['email']!r}"
```

How to read that pattern: `[^@\s]+` means "one or more characters that are neither `@` nor whitespace", then a literal `@`, then the same again for the domain, then `\.` (a literal dot), then `[A-Za-z]{2,}` (two or more letters, the top-level domain such as `com`). `re.fullmatch` succeeds only if the **entire** string fits the pattern. A related function, `re.match`, only checks the beginning, so it would wrongly accept `"a@b.com garbage"`; prefer `fullmatch` for validation. The leading `r` before the quotes makes it a "raw string" so Python does not treat the backslashes as escape characters.

This pattern is a practical sanity check, not a complete email validator (real email rules are enormous). For tests, "looks like an email" is the right level.

For timestamps, parse them instead of using a regular expression:

```python
from datetime import datetime

created = datetime.fromisoformat(order["createdAt"])   # '2026-10-11T09:30:00Z'
print(created)                                         # 2026-10-11 09:30:00+00:00
```

`datetime.fromisoformat` raises `ValueError` for an impossible date, which is a free correctness check. For example, `datetime.fromisoformat("2026-13-45")` raises `ValueError: month must be in 1..12`. (In Python 3.11 and later, the trailing `Z` meaning UTC is accepted. On older versions replace it first: `value.replace("Z", "+00:00")`.) To assert a failing parse, wrap it with `pytest.raises(ValueError)`, or simply let the `ValueError` fail the test and read the message.

#### 5.5 Range and content rules

```python
assert body["id"] > 0
assert 1 <= len(body["name"]) <= 100
assert body["name"] == body["name"].strip(), "name has leading or trailing spaces"
assert body["email"] == body["email"].lower(), "email should be lower case"
```

`1 <= len(x) <= 100` is Python's chained comparison: both conditions must hold. These checks encode business rules from the requirements: names must not be empty, ids are positive, and so on. Ask "what would be nonsense here?" and assert that it does not happen. An empty name, a negative id, or a quantity of zero are all valid JSON and all wrong.

#### 5.6 A full field-level test, explained

```python
def test_user_has_expected_fields(client):
    response = client.get("/users/1")
    assert response.status_code == 200
    body = safe_json(response)
    assert isinstance(body, dict)
    for field in ("id", "name", "username", "email", "address", "company"):
        assert field in body, f"Missing field: {field}"
    assert body["id"] == 1
    assert isinstance(body["id"], int) and not isinstance(body["id"], bool)
    assert body["address"]["geo"]["lat"] == "-37.3159"
```

Reading it as a story: we get the user, confirm success, parse safely, confirm the top level is an object, confirm each required field exists, confirm the id is the one we asked for and is a real integer, and confirm a nested value. The order matters: presence before value, because reading a value from a missing field raises `KeyError` before your assertion can describe the problem.

---

### 6. `null`, Missing, Empty: Four Different Situations

Beginners often treat "no value" as one thing. APIs do not. Look at what an API can return for an optional field, `coupon`, on an order:

| Situation | JSON | Python after parsing | `"coupon" in order` | `order.get("coupon")` |
|-----------|------|----------------------|---------------------|-----------------------|
| Field absent | `{}` | `{}` | `False` | `None` |
| Field is `null` | `{"coupon": null}` | `{"coupon": None}` | `True` | `None` |
| Empty string | `{"coupon": ""}` | `{"coupon": ""}` | `True` | `""` |
| Zero | `{"coupon": 0}` | `{"coupon": 0}` | `True` | `0` |

Notice the last two columns: `.get()` returns `None` both when the field is absent and when it is explicitly `null`. If the difference matters (and in a contract test, it often does), use `in` to distinguish them.

Why do these differences matter? Because client code treats them differently. JavaScript code like `if (order.coupon)` treats `null`, `""`, `0`, and `undefined` all as false, but code like `order.coupon.length` crashes on `null` and `undefined` but works on `""`. A contract is what saves the client developer from guessing. Your tests enforce the contract.

#### `dict.get()` explained

`dict.get(key, default)` returns the value for `key`, or `default` if the key is absent. The default itself defaults to `None`.

```python
order = safe_json(client.get("/orders/1"))

order["coupon"]               # None  (present, null)
order.get("coupon")           # None
order.get("missing")          # None  (absent; no error)
order.get("missing", "N/A")   # 'N/A'
order["missing"]              # KeyError: 'missing'
```

These are real outputs from the lab server. When should you use each form?

- **`body["x"]`**: the field is required. If it is missing, you want a loud failure (`KeyError`).
- **`body.get("x")`**: the field is optional, and "absent" and "null" mean the same thing for this test.
- **`"x" in body`**: you care specifically whether the key exists, regardless of its value.
- **`body.get("x", sentinel)`**: you want to distinguish "absent" without a second lookup. A *sentinel* is a unique placeholder such as the string `"<missing>"` that cannot be a real value.

#### Asserting null correctly

Use `is None`, not `== None`, and not truthiness:

```python
assert order["coupon"] is None            # explicitly null
assert order["note"] == ""                # empty string, not null
assert order["coupon"] is None and "coupon" in order   # null AND present
```

Do not write `assert not order["note"]`, because that passes for `None`, `""`, `0`, `[]`, and `False` alike. It cannot tell a correct `""` from a defective `null`. Truthiness checks hide exactly the distinctions you are trying to test.

#### Null versus empty list: a classic defect

Look at the three products in the lab server:

```python
for p in safe_json(client.get("/products")):
    print(p["sku"], p["tags"], bool(p["tags"]), isinstance(p["tags"], list))
```

```text
A1 ['office'] True True
B2 [] False True
C3 None False False
```

Product `B2` has an empty list (correct for "no tags"). Product `C3` has `None`. Both are "falsy", so a truthiness check treats them the same, but `isinstance(..., list)` exposes the difference: `C3` is not a list. A client iterating `for tag in product.tags` works for `B2` and crashes for `C3`. So for a field the contract says is always a list, assert the type:

```python
for p in products:
    assert isinstance(p["tags"], list), f"{p['sku']}: tags is {p['tags']!r}, expected a list"
```

Failure message for the lab data: `C3: tags is None, expected a list`.

#### Nullable fields done right

Some fields are legitimately nullable. In the lab data, `phone` is a string for odd-numbered users and `null` for even ones. The right assertion accepts exactly those two possibilities:

```python
def test_phone_is_string_or_null(client):
    for user in safe_json(client.get("/users")):
        assert user["phone"] is None or isinstance(user["phone"], str), \
            f"user {user['id']}: phone has unexpected value {user['phone']!r}"
```

This passes for `None` and for strings, and fails for `5551234` (a number) or `[]`. Notice the `or` expresses the contract "string or null" precisely. Contrast with a lazy `assert user["phone"]`, which would fail on the legitimate nulls.

---

### 7. Validating Lists

Lists are where API data gets interesting: search results, feeds, transactions, orders. Every list has questions you can ask:

- How many items? (Exact count, minimum, maximum, or empty.)
- Does every item have the right shape and values?
- Does at least one item match some condition?
- Are the items unique?
- Are they in the right order?
- Did a filter really filter?

#### 7.1 Length

```python
users = safe_json(client.get("/users"))
assert isinstance(users, list)
assert len(users) == 10
```

Always check `isinstance(users, list)` first. If the API unexpectedly returns an object such as `{"error": "..."}`, `len()` would return the number of keys and give a confusing result.

Choose the right count assertion for the situation:

| Situation | Assertion |
|-----------|-----------|
| Seeded data with a known count | `len(items) == 10` |
| "There should be some" | `len(items) > 0` |
| Bounded page size | `len(items) <= page_size` |
| Search with no matches | `items == []` |

Avoid hard-coding counts for live data that changes. A test that says `len(users) == 10` against a production database breaks every time a user signs up. For changing data, assert relationships ("a page has at most `limit` items") instead of absolute numbers.

When a count assertion fails, pytest reports it like this (real output, with a deliberately wrong expectation of 12):

```text
>       assert len(users) == 12
E       AssertionError: assert 10 == 12
E        +  where 10 = len([{'id': 1, 'name': 'User 1', ...}, ...])
```

The first line gives the actual and expected counts, and the `where` line shows the data, abbreviated.

#### 7.2 Every item satisfies a rule: `all()`

```python
assert all("email" in u for u in users)
```

`all(condition for item in items)` is `True` only if the condition holds for **every** item. (It is also `True` for an empty list, which is worth remembering: `all(...)` over nothing is vacuously true. If you require at least one item, add a separate `len(items) > 0` assertion.)

The weakness of `all()` is the failure message: `assert False`. You do not learn which item broke the rule. The better habit is to collect the offenders:

```python
def test_filter_returns_only_matching_posts(client):
    posts = safe_json(client.get("/posts", params={"userId": 3}))
    assert len(posts) > 0, "filter returned no posts at all"
    wrong = [p["id"] for p in posts if p["userId"] != 3]
    assert wrong == [], f"posts with wrong userId: {wrong}"
```

Line by line:

- `params={"userId": 3}` is how `requests` builds the query string `?userId=3` (you met query parameters on Monday).
- `len(posts) > 0` guards against the vacuous-truth trap: a broken filter that returns nothing would otherwise pass the next check.
- `wrong = [p["id"] for p in posts if p["userId"] != 3]` builds a list of the ids of the posts that violate the rule. The `if` at the end of a list comprehension filters.
- `assert wrong == []` passes only when there are no offenders, and the message prints exactly which posts are wrong, for example `posts with wrong userId: [4, 17]`.

This "collect offenders, assert empty" pattern is the single most useful list-validation idiom. Memorise it.

#### 7.3 At least one item satisfies a rule: `any()`

```python
assert any(u["username"] == "user5" for u in users), "user5 not found in list"
```

`any(...)` is `True` if at least one item meets the condition. It is the right tool for "the created record appears in the list" or "the list contains an admin user".

#### 7.4 Uniqueness

```python
ids = [u["id"] for u in users]
assert len(ids) == len(set(ids)), "Duplicate ids found"
```

A `set` stores each value once, so if the set is smaller than the list, something repeated. To report which values repeat, use `collections.Counter`:

```python
from collections import Counter

ids = [x["id"] for x in safe_json(client.get("/dupes"))]   # [3, 1, 3]
dupes = [value for value, count in Counter(ids).items() if count > 1]
assert dupes == [], f"duplicate ids: {dupes}"
```

`Counter(ids)` counts occurrences (`Counter({3: 2, 1: 1})` for the lab data), and the comprehension keeps the values that occur more than once. The failure message would read `duplicate ids: [3]`.

#### 7.5 Ordering

```python
ids = [u["id"] for u in users]
assert ids == sorted(ids), "Users are not sorted by id ascending"
assert ids == sorted(ids, reverse=True), "Users are not sorted by id descending"
```

`sorted(ids)` returns a new sorted list; if the response is already in order, it equals the original. For lists of dicts, sort by a key function:

```python
names = [u["name"] for u in users]
assert names == sorted(names)

# or compare dicts using a key
assert users == sorted(users, key=lambda u: u["id"])
```

`lambda u: u["id"]` is a tiny unnamed function that says "to sort, look at each item's `id`". Only assert ordering when the API *promises* an order (documented sort, `?sort=` parameter). If the order is unspecified, a test that depends on it will fail randomly, which is called a *flaky* test. In that case, compare without regard to order, as described in section 9.

#### 7.6 Empty results are valid results

```python
def test_empty_result_is_empty_list(client):
    r = client.get("/posts", params={"userId": 999})
    assert r.status_code == 200
    assert safe_json(r) == []
```

A search that matches nothing should usually return `200` and `[]`, not `404`, and not `null`. (Some APIs use `404` for "this specific resource does not exist" but `200` with an empty list for "this collection is empty". Follow the API's documented contract.) The `== []` check also catches the `null` defect, because `None == []` is `False`.

#### 7.7 Lists inside objects

An order contains a list of items. Validate the container and then the contents:

```python
order = safe_json(client.get("/orders/1"))
items = order["items"]
assert isinstance(items, list) and len(items) == 2
for item in items:
    assert set(item) >= {"sku", "qty", "price"}, f"item missing fields: {item}"
    assert item["qty"] >= 1
```

`set(item) >= {...}` reads "the item's keys are a superset of (or equal to) the required keys". It is a compact presence check for several fields at once.

---

### 8. Comparing Dictionaries and Echo Checks

Sometimes you do not want to check fields individually; you want to compare a whole object with an expected object. There are three flavours.

#### 8.1 Full equality

```python
expected = {"userId": 1, "id": 1, "title": "buy milk", "completed": False}
assert safe_json(client.get("/todos/1")) == expected
```

Dict equality ignores key order (`{"a":1,"b":2} == {"b":2,"a":1}` is `True`) and compares nested structures deeply. It is simple and strict: any extra, missing, or different field fails. That strictness is a double-edged sword. If the API adds a new harmless field tomorrow, every full-equality test breaks. Reserve full equality for small, stable objects, such as error bodies with a fixed shape.

When full equality fails, pytest prints a diff of the two dicts, listing which keys differ, which is usually enough to see the problem.

#### 8.2 Partial comparison: "these fields, and I do not care about the rest"

For large objects, compare only the fields you care about. Two techniques:

```python
order = safe_json(client.get("/orders/1"))
expected = {"id": 1, "status": "shipped", "coupon": None}

# Technique A: project the response down to the expected keys, then compare.
actual = {key: order.get(key, "<missing>") for key in expected}
assert actual == expected

# Technique B: subset test using dict views.
assert expected.items() <= order.items()
```

Technique A, line by line: the dict comprehension builds a new dict containing, for each key in `expected`, the order's value for that key (or the sentinel `"<missing>"` if absent). Comparing this projection with `expected` yields a clear failure: pytest's dict diff will show, for example, `'status': 'shipped' != 'pending'`, or `'<missing>'` for an absent field.

Technique B uses the fact that `dict.items()` behaves like a set of `(key, value)` pairs, and `<=` means "is a subset of". It is concise, but its failure message is a bare `assert False` with no hint of which field differed. Prefer Technique A for its message quality.

#### 8.3 The "echo" check after a `POST`

After creating a resource, the response usually reflects what you sent, plus server-generated fields such as `id`. A good test verifies the echo and the generated field:

```python
def test_created_post_echoes_input(client):
    payload = {"title": "Check echo", "body": "Content", "userId": 2}
    r = client.post("/posts", json=payload)
    assert r.status_code == 201
    body = safe_json(r)
    for key, value in payload.items():
        assert body.get(key) == value, f"{key}: sent {value!r}, got {body.get(key)!r}"
    assert isinstance(body["id"], int)
```

Line by line:

- `json=payload` makes `requests` serialise the dict to JSON and set `Content-Type: application/json` for you.
- `r.status_code == 201` verifies "Created". (The right status for a successful creation was covered in the status code lesson.)
- `for key, value in payload.items()` walks every field we sent.
- `body.get(key) == value` checks that the server stored what we sent. We use `.get()` here so that a missing key gives `None` and a readable failure rather than a `KeyError`.
- The message uses `!r` so a type difference is visible: `userId: sent 2, got '2'` makes the string-versus-number defect obvious at a glance.
- `isinstance(body["id"], int)` checks the generated id exists and is an integer without hard-coding its value (the id is the server's decision).

Do not stop at the `POST` response. Real systems sometimes echo your input without saving it. A stronger test then does a `GET` on the new id and checks the stored data. (The lab server does not store anything, so we cannot demonstrate it here; you will build this pattern against a real stateful API in the framework project.)

#### 8.4 Fields that must NOT be present

Security-minded tests assert the absence of internal or sensitive data:

```python
def test_no_sensitive_fields(client):
    body = safe_json(client.get("/users/1"))
    leaked = [f for f in ("password", "passwordHash", "ssn", "token") if f in body]
    assert leaked == [], f"leaked: {leaked}"
```

The lab server's order contains an `internalId` field. You can detect that kind of leak by pattern:

```python
order = safe_json(client.get("/orders/1"))
internal = [k for k in order if k.lower().startswith("internal")]
assert internal == [], f"internal fields exposed: {internal}"
```

Run against the lab server, this assertion fails, and `internal` holds `['internalId']`. That is a real defect pattern: backend developers add a database column, the serialiser dumps every column, and an internal identifier (or worse, a password hash) is exposed to the public. A "must not appear" test is cheap insurance.

---

### 9. Floating-Point Numbers and Ordering Concerns

This section covers two families of flaky or wrong assertions: numbers that are not exactly what they look like, and collections whose order you should not depend on.

#### 9.1 Why `0.1 + 0.2 != 0.3`

Computers store decimal fractions like `0.1` in binary, where they cannot be represented exactly, much like `1/3` cannot be written exactly in decimal. Run this:

```python
print(0.1 + 0.2)          # 0.30000000000000004
print(0.1 + 0.2 == 0.3)   # False
print(1.1 * 3)            # 3.3000000000000003
```

This is not a Python bug; every language using standard floating point behaves this way. For API tests, it means that comparing floats from JSON with `==` can fail even though the numbers are "the same" to a human.

The classic scenario: an order has line items and a total, and you want to verify the total equals the sum.

```python
order = safe_json(client.get("/orders/1"))
computed = sum(i["qty"] * i["price"] for i in order["items"])   # 2*1.1 + 1*2.2
print(computed, order["total"])
```

Whether `computed == order["total"]` happens to be `True` depends on the specific numbers (for the lab order it happens to be `True`: both are `4.4`), which is the dangerous part: it works in your test today and can fail on a different order tomorrow. Do not rely on luck. Use a tolerance.

#### 9.2 Tolerant comparison with `pytest.approx`

```python
import pytest

assert computed == pytest.approx(order["total"])
assert 1.1 * 3 == pytest.approx(3.3)                           # passes
assert computed == pytest.approx(order["total"], abs=0.005)    # within half a cent
```

`pytest.approx(x)` creates an object that compares equal to any number "close enough" to `x`. By default it uses a relative tolerance of one in a million (`1e-6`). The `abs=0.005` form sets an absolute tolerance, which suits money: "within half a cent". Python's standard library offers an equivalent, `math.isclose(a, b, rel_tol=1e-9)`, if you are outside pytest.

Choose the tolerance deliberately. A tolerance that is too loose hides real errors (a total off by one dollar should fail), and one that is too tight brings back flakiness.

#### 9.3 Money: the right representation

Many APIs avoid the float problem at its root. Two common designs:

- **Integer minor units**: `"price": 1999` meaning 1999 cents. All arithmetic is exact integer arithmetic. (`19.99 * 100` in Python is `1998.9999999999998`, which shows how fragile floats are; converting with `round()` gives `1999`.)
- **Decimal strings**: `"price": "19.99"`. Exact, but now your test must convert before computing, using Python's `Decimal`.

```python
from decimal import Decimal

price = Decimal("19.99")
print(price * 3)        # 59.97   (exact)
```

Always build a `Decimal` from a **string**, not from a float. `Decimal(19.99)` captures the float's binary error, and `Decimal(19.99) == Decimal("19.99")` is `False`. If an API returns JSON numbers and you want exact arithmetic anyway, ask the parser to build `Decimal`s directly:

```python
import json
from decimal import Decimal

data = json.loads('{"price": 19.99}', parse_float=Decimal)
print(data)    # {'price': Decimal('19.99')}
```

Note that if the API returns money as a string `"19.99"`, a type check for "number" will fail. That is correct only if the contract said number. Match your assertion to the documented contract, not to your assumption.

#### 9.4 Other number traps

- **Large integers**: JSON itself does not limit size, but JavaScript clients lose precision above 2^53 (about 9 quadrillion). APIs that return huge ids often send them as strings for that reason. Python handles big ints exactly, so your test will not notice; check the documentation.
- **`NaN` and `Infinity`**: these are not valid JSON, yet Python's parser accepts them by default. A server that emits `NaN` will pass `response.json()` in Python but break in browsers. This is rare, but worth knowing about when a client app shows `NaN`.
- **`1` versus `1.0`**: equal in Python, but different types, as discussed in section 5.3.

#### 9.5 Ordering: lists have order, dicts and sets do not matter

| Structure | Is order significant in equality? | Example |
|-----------|----------------------------------|---------|
| `list` | Yes | `[1, 2] == [2, 1]` is `False` |
| `dict` (key order) | No | `{"a":1,"b":2} == {"b":2,"a":1}` is `True` |
| `set` | No | `{1, 2} == {2, 1}` is `True` |

Two consequences for your tests.

First, **JSON object key order is not meaningful.** JSON specifies objects as unordered collections. Never write a test that depends on the order in which fields appear in an object (for example by comparing `json.dumps(body)` with a fixed string). Compare parsed dicts instead, which ignore order.

Second, **list order is meaningful only if the API promises it.** If the API does not guarantee order (many search endpoints do not), then asserting `ids == [1, 2, 3]` creates a flaky test that passes on Monday and fails on Tuesday after a database re-index. To check "these items are present, in any order", compare sorted lists or sets:

```python
returned_ids = [p["id"] for p in posts]

assert sorted(returned_ids) == sorted(expected_ids)     # same items, any order, duplicates counted
assert set(returned_ids) == set(expected_ids)           # same distinct items, any order
```

Use `sorted(...)` equality when duplicates matter (the list `[1, 1, 2]` must not match `[1, 2]`), and `set` equality when you only care which distinct values appear. When items are dicts (unhashable, so not set-friendly), sort by a stable key before comparing:

```python
assert sorted(actual, key=lambda x: x["id"]) == sorted(expected, key=lambda x: x["id"])
```

When order **is** promised (a "newest first" feed), test it explicitly. The point is to decide deliberately whether order is part of the contract.

---

### 10. Validating Structure with the `jsonschema` Library (Basics)

So far you have written assertions one field at a time. That works, but a response with 20 fields and 3 levels of nesting needs a lot of assertion lines, and it is easy to forget a field. **JSON Schema** offers a different approach: instead of writing code that checks the data, you write a *description* of what valid data looks like, and a library checks the data against the description.

> Deeper schema design and specification-driven validation are covered on Wednesday. Today is only the foundation: `validate()`, `ValidationError`, and a simple schema using `type`, `required`, and `properties`.

#### 10.1 Installation and a first example

```bash
pip install jsonschema
```

A **schema** is itself a JSON document (in Python, a dict). Here is a small one that describes a user:

```python
schema = {
    "type": "object",
    "required": ["id", "name", "email"],
    "properties": {
        "id": {"type": "integer"},
        "name": {"type": "string"},
        "email": {"type": "string"},
    },
}
```

Reading it in plain English: "The value must be an object. It must contain the keys `id`, `name`, and `email`. If `id` is present, it must be an integer; if `name` is present, a string; if `email` is present, a string."

Using it:

```python
from jsonschema import validate, ValidationError

body = safe_json(client.get("/users/1"))
validate(instance=body, schema=schema)      # returns None if valid; raises if not
print("valid")
```

`validate(instance=..., schema=...)` has one simple contract:

- If the data conforms, it returns `None` and does nothing. The test continues.
- If the data does not conform, it raises `jsonschema.ValidationError`.

Because pytest treats any uncaught exception as a failed test, you can often call `validate()` as a bare line and let it fail naturally. The exception's text is informative, as you will see shortly.

#### 10.2 The three keywords you need today

| Keyword | Where it goes | Meaning |
|---------|---------------|---------|
| `type` | Any schema | The value's JSON type: `"object"`, `"array"`, `"string"`, `"integer"`, `"number"`, `"boolean"`, `"null"` |
| `required` | An object schema | A list of keys that **must be present** |
| `properties` | An object schema | A mapping from key name to a sub-schema that the key's value must satisfy |

Three critical behaviours that surprise beginners:

1. **`properties` does not make anything required.** It only says "*if* this key is present, its value must look like this". A response missing `email` entirely passes `properties` and is only caught by `required`. You almost always need both.
2. **Extra keys are allowed by default.** A response with an additional field `nickname` still passes the schema above. This is usually what you want (APIs gain fields over time); stricter control exists but belongs to Wednesday's lesson.
3. **`integer` versus `number`.** `"integer"` means a whole number; `"number"` means any number (integers included). A subtle case: the value `1.0` counts as an integer in `jsonschema`, because it is mathematically whole, while `1.5` does not. And booleans are **not** accepted as integers, even though Python considers `True` an `int`:

```python
validate(5, {"type": "number"})      # ok
validate(1.0, {"type": "integer"})   # ok (whole number)
validate(1.5, {"type": "integer"})   # ValidationError: 1.5 is not of type 'integer'
validate(True, {"type": "integer"})  # ValidationError: True is not of type 'integer'
```

That last line is one place where the schema library is *stricter and more correct* than Python's `isinstance` (see the `bool` trap in section 5.3).

#### 10.3 Nested objects and nullable fields

Nesting is just a schema inside `properties`:

```python
USER_SCHEMA = {
    "type": "object",
    "required": ["id", "name", "email", "address"],
    "properties": {
        "id": {"type": "integer"},
        "name": {"type": "string"},
        "email": {"type": "string"},
        "phone": {"type": ["string", "null"]},
        "address": {
            "type": "object",
            "required": ["city"],
            "properties": {"city": {"type": "string"}},
        },
    },
}
```

Two things to notice:

- `"address"` is itself a mini-schema with its own `type`, `required`, and `properties`. You can nest as deep as the data goes.
- `"phone": {"type": ["string", "null"]}` is how you say "a string **or** `null`". A list of types means "any one of these". Without `"null"` in the list, the lab server's even-numbered users (whose phone is `null`) would fail. Notice that `phone` is in `properties` but not in `required`, so the field may also be entirely absent. If it must always be present, even as `null`, add `"phone"` to `required`.

For a list response, describe the array and give the schema for its elements with `items`:

```python
USERS_SCHEMA = {"type": "array", "items": USER_SCHEMA}
```

`"items"` means "every element of the array must satisfy this schema". That single line replaces a whole `all(...)` loop for shape validation.

Put the schemas in their own module, `schemas.py`, so tests stay short and the contract has one home:

```python
# schemas.py
USER_SCHEMA = {
    "type": "object",
    "required": ["id", "name", "email", "address"],
    "properties": {
        "id": {"type": "integer"},
        "name": {"type": "string"},
        "email": {"type": "string"},
        "phone": {"type": ["string", "null"]},
        "address": {
            "type": "object",
            "required": ["city"],
            "properties": {"city": {"type": "string"}},
        },
    },
}

USERS_SCHEMA = {"type": "array", "items": USER_SCHEMA}
```

#### 10.4 Reading a `ValidationError`

When validation fails, the `ValidationError` carries several useful attributes. Using the lab server's broken `/bad-user` endpoint (body: `{"id": "7", "name": "", "email": "not-an-email"}`):

```python
from jsonschema import validate, ValidationError
from schemas import USER_SCHEMA

bad = safe_json(client.get("/bad-user"))
try:
    validate(instance=bad, schema=USER_SCHEMA)
except ValidationError as err:
    print(err.message)
    print(list(err.path))
    print(err.validator)
    print(err.validator_value)
    print(err.instance)
    print(list(err.schema_path))
```

Output from the lab server:

```text
'address' is a required property
[]
required
['id', 'name', 'email', 'address']
{'id': '7', 'name': '', 'email': 'not-an-email'}
['required']
```

What each attribute means:

| Attribute | Meaning | In this example |
|-----------|---------|-----------------|
| `err.message` | Human-readable description | `'address' is a required property` |
| `err.path` | Where in the **data** the problem is (a deque of keys/indexes; wrap with `list()`) | `[]` means "at the top level" |
| `err.validator` | The schema keyword that failed | `required` |
| `err.validator_value` | The keyword's value in the schema | the list of required keys |
| `err.instance` | The piece of data that failed | the whole body (top level) |
| `err.schema_path` | Where in the **schema** the failing rule lives | `['required']` |

For a failure deeper in the data, the path shows the route. If a schema demanded that `address` contain a `zip` key, validating `/users/1` gives `list(err.path) == ['address']` and the message `'zip' is a required property`: the path points at the object that lacks the key. If `address.city` were a number, you would see `['address', 'city']` and a message like `5 is not of type 'string'`.

#### 10.5 One error or all errors?

An important detail: `validate()` raises **one** error, even if the data has several problems. Our `/bad-user` body has two problems: `address` is missing, and `id` is a string. `validate()` reported only the first. Which one it reports is chosen by a "best match" heuristic and may not be the one you expect.

When you want every problem in one test run, create a validator object and iterate over all errors:

```python
from jsonschema import Draft202012Validator

validator = Draft202012Validator(USER_SCHEMA)
errors = sorted(validator.iter_errors(bad), key=lambda e: list(e.path))
for err in errors:
    print(list(err.path), err.message)
```

```text
[] 'address' is a required property
['id'] '7' is not of type 'integer'
```

`Draft202012Validator` is the class implementing a particular version ("draft") of the JSON Schema specification. `iter_errors(data)` yields every `ValidationError` instead of stopping at the first. `sorted(..., key=lambda e: list(e.path))` puts the errors in a stable, readable order.

A reusable helper turns this into a single, readable assertion:

```python
def assert_matches_schema(instance, schema):
    validator = Draft202012Validator(schema)
    errors = sorted(validator.iter_errors(instance), key=lambda e: list(e.path))
    assert not errors, "Schema violations:\n" + "\n".join(
        f"  at {list(e.path) or 'top level'}: {e.message}" for e in errors
    )
```

Line by line:

- It builds a validator for the given schema and collects every error into a list, sorted by location.
- `assert not errors` passes when the list is empty.
- The message joins one line per error: `at ['id']: '7' is not of type 'integer'`. `list(e.path) or 'top level'` substitutes the words "top level" when the path is empty (an empty list is falsy, so `or` picks the right-hand side).
- The `\n` characters put each violation on its own line in the pytest report.

Against `/bad-user` the failure report reads:

```text
AssertionError: Schema violations:
  at top level: 'address' is a required property
  at ['id']: '7' is not of type 'integer'
```

A developer reading that report knows everything wrong with the response without rerunning anything.

#### 10.6 Two kinds of errors: bad data versus a bad schema

If your **schema** is malformed (for example a typo like `"type": "strng"`), jsonschema raises `jsonschema.exceptions.SchemaError`, not `ValidationError`:

```python
from jsonschema import Draft202012Validator
Draft202012Validator.check_schema({"type": "strng"})
# SchemaError: 'strng' is not valid under any of the given schemas
```

This distinction matters in tests. A `ValidationError` means the API response is wrong. A `SchemaError` means your own test code is wrong. If you wrap `validate()` in `try/except Exception`, you could accidentally treat your own typo as an "API failure" or, worse, swallow it. Catch `ValidationError` specifically.

#### 10.7 A schema test in context

```python
from jsonschema import validate
from json_helpers import safe_json
from schemas import USER_SCHEMA, USERS_SCHEMA


def test_user_matches_schema(client):
    validate(instance=safe_json(client.get("/users/1")), schema=USER_SCHEMA)


def test_users_match_schema(client):
    validate(instance=safe_json(client.get("/users")), schema=USERS_SCHEMA)
```

Two tests, each one line of real logic, covering the structure of every field in every user. If one of the ten users were malformed, the second test would fail with the item's index in the path. For example, when we appended the incomplete user `{"id": "x"}` as an eleventh item, the error path was `[10]` and the message `'name' is a required property`: the first element of the path is the index of the offending item in the array.

#### 10.8 Schema or hand-written assertions? When to use which

| Use a schema when | Use plain assertions when |
|-------------------|---------------------------|
| Checking overall shape: fields, types, nesting | Checking specific business values (`status == "shipped"`) |
| The response is large | The rule involves several fields together (`total == sum(items)`) |
| You want one reusable "contract" for an endpoint | The rule involves the request (echo checks) |
| You want a complete list of structural problems | The check is a one-off |

They are complements. A solid test often does both: a schema call for the shape, then a few assertions for the values that matter to the scenario. A schema cannot say "total equals the sum of the items" in this basic form, and plain assertions are tedious for shape. Use each where it is strong.

---

### 11. Putting It Together: A Complete Test Module

Here is a compact module combining the patterns from this lesson. Save it as `test_json_validation.py` next to the files created earlier.

```python
# test_json_validation.py
import pytest
from jsonschema import validate, ValidationError
from json_helpers import safe_json
from schemas import USER_SCHEMA, USERS_SCHEMA


def test_user_has_expected_fields(client):
    response = client.get("/users/1")
    assert response.status_code == 200
    body = safe_json(response)
    assert isinstance(body, dict)
    for field in ("id", "name", "username", "email", "address", "company"):
        assert field in body, f"Missing field: {field}"
    assert body["id"] == 1
    assert isinstance(body["id"], int) and not isinstance(body["id"], bool)
    assert body["address"]["geo"]["lat"] == "-37.3159"


def test_phone_is_string_or_null(client):
    for user in safe_json(client.get("/users")):
        assert user["phone"] is None or isinstance(user["phone"], str), user["id"]


def test_users_list(client):
    users = safe_json(client.get("/users"))
    assert isinstance(users, list)
    assert len(users) == 10
    assert all("email" in u for u in users)
    ids = [u["id"] for u in users]
    assert len(ids) == len(set(ids)), "duplicate ids"
    assert ids == sorted(ids), "not sorted by id"


def test_filter_returns_only_matching_posts(client):
    posts = safe_json(client.get("/posts", params={"userId": 3}))
    assert len(posts) > 0
    wrong = [p["id"] for p in posts if p["userId"] != 3]
    assert wrong == [], f"posts with wrong userId: {wrong}"


def test_empty_result_is_empty_list(client):
    r = client.get("/posts", params={"userId": 999})
    assert r.status_code == 200
    assert safe_json(r) == []


def test_order_total_matches_items(client):
    order = safe_json(client.get("/orders/1"))
    computed = sum(i["qty"] * i["price"] for i in order["items"])
    assert computed == pytest.approx(order["total"])
    assert order["coupon"] is None


def test_order_partial_match(client):
    order = safe_json(client.get("/orders/1"))
    expected = {"id": 1, "status": "shipped", "coupon": None}
    actual = {k: order.get(k, "<missing>") for k in expected}
    assert actual == expected


def test_created_post_echoes_input(client):
    payload = {"title": "Check echo", "body": "Content", "userId": 2}
    r = client.post("/posts", json=payload)
    assert r.status_code == 201
    body = safe_json(r)
    for key, value in payload.items():
        assert body.get(key) == value, f"{key}: sent {value!r}, got {body.get(key)!r}"
    assert isinstance(body["id"], int)


def test_user_matches_schema(client):
    validate(instance=safe_json(client.get("/users/1")), schema=USER_SCHEMA)


def test_users_match_schema(client):
    validate(instance=safe_json(client.get("/users")), schema=USERS_SCHEMA)


def test_no_sensitive_fields(client):
    body = safe_json(client.get("/users/1"))
    leaked = [f for f in ("password", "passwordHash", "ssn", "token") if f in body]
    assert leaked == [], f"leaked: {leaked}"


def test_safe_json_explains_html(client):
    with pytest.raises(AssertionError) as info:
        safe_json(client.get("/html"))
    assert "text/html" in str(info.value)


def test_bad_user_fails_schema(client):
    with pytest.raises(ValidationError):
        validate(instance=safe_json(client.get("/bad-user")), schema=USER_SCHEMA)
```

Run it with the lab server active:

```bash
pytest -v
```

Output from the lab server (shortened to the summary line; `-v` also lists each test name):

```text
13 passed in 0.09s
```

The last two tests deserve explanation because they are a different kind of test: they prove that your validation can **fail**. `pytest.raises(ValidationError)` is a context manager that passes only if the code inside raises that exception. A validator that never fails is worthless, so for any important schema it is worth keeping at least one "negative" test that feeds known-bad data and confirms the rejection. This guards against the silent disaster where someone edits the schema into uselessness (for example an empty `{}` schema accepts everything).

---

### 12. Common Mistakes and How to Avoid Them

| # | Mistake | Why it hurts | Fix |
|---|---------|--------------|-----|
| 1 | Asserting only the status code | Wrong data, wrong types, and `null`s all pass | Always add at least one body check |
| 2 | Calling `.json()` before checking the status | A `502` HTML page raises a confusing parser error | Check status first, parse through `safe_json` |
| 3 | Calling `.json()` on a `204` or other empty-body response | `JSONDecodeError` on a perfectly correct response | Only parse bodies that should exist |
| 4 | Catching `Exception` or using a bare `except:` | Hides real bugs, including typos in your own test | Catch `ValueError` for parsing and `ValidationError` for schemas |
| 5 | `assert body["x"]` as a presence check | Fails for legitimate `0`, `""`, `False`, `null` | Use `"x" in body`, `is None`, or an explicit comparison |
| 6 | `assert not value` to test for "empty or null" | Cannot distinguish `null` from `[]` or `""` | Compare precisely: `== []`, `is None`, `== ""` |
| 7 | `==` on floats from computation | `0.1 + 0.2 == 0.3` is `False` | `pytest.approx`, or integer cents / `Decimal` |
| 8 | Depending on list order the API never promised | Flaky tests | Compare `sorted(...)` or `set(...)` |
| 9 | `all(...)` with no `len(...) > 0` guard | A broken filter that returns nothing passes | Assert non-empty first |
| 10 | `all(...)` with no offender report | Failure says only `assert False` | Collect offenders and assert the list is empty |
| 11 | `isinstance(x, int)` accepting `True` | Boolean passes as an id | Add `and not isinstance(x, bool)`, or use a schema |
| 12 | Full-dict equality on large, evolving objects | Breaks whenever the API adds an unrelated field | Compare only the fields that matter |
| 13 | Hard-coding values that change (timestamps, generated ids) | Always-failing or flaky tests | Check type and format instead |
| 14 | Treating schema `properties` as "required" | Missing fields slip through | Always pair `properties` with `required` |
| 15 | Forgetting `"null"` in the type list of a nullable field | False failures on legitimate nulls | `{"type": ["string", "null"]}` |
| 16 | A schema nobody ever sees fail | An accidentally permissive schema passes everything | Keep a negative test using known-bad data |
| 17 | Using `re.match` for validation | Matches only the start, so trailing garbage passes | Use `re.fullmatch` |
| 18 | No assertion messages on complex checks | Failures take minutes to diagnose | Include the offending values in the message |

---

### 13. Practice Exercises

Run the lab server first. Attempt each exercise before reading the solution. Every solution below was run against the lab server.

**Exercise 1: Navigating nested data.**
For `GET /users/3`, write a test asserting that the city is `"Gwenborough"`, the latitude is a string that converts to a negative number, and the company name is `"Romaguera-Crona"`.

**Exercise 2: Predicting parse failures.**
Without running them, predict what `safe_json` reports for `/html`, `/empty`, `/truncated`, and `/pyrepr`. Then write a parametrized test that confirms each one raises `AssertionError`, and print the messages.

**Exercise 3: Null handling.**
For `GET /users`, find the ids of users whose phone is `null`, assert they are exactly `[2, 4, 6, 8, 10]`, assert that every phone is a string or `null`, and assert that a field that does not exist (`fax`) reads as `None` through `.get()`.

**Exercise 4: List validation.**
For `GET /comments?postId=1`, assert there are 5 comments, every `postId` equals `1`, and every email contains `@`.

**Exercise 5: Floating point.**
Show that `1.1 * 3 == 3.3` is `False`, then make a robust assertion. Then verify that the order total in `/orders/1` equals the sum of `qty * price` using a half-cent tolerance.

**Exercise 6: Partial comparison and leaks.**
For `/orders/1`, assert that `id`, `status`, and `coupon` have the values `1`, `"shipped"`, `None` using a projection. Then write a check for fields whose names start with `internal`; what does it find?

**Exercise 7: A schema.**
Write a schema for `/todos/1` (`userId`, `id`, `title`, `completed`; all required). Validate the response. Then change `completed` to `"type": "string"`, validate again, and read the `ValidationError`.

**Exercise 8: Duplicates and ordering.**
For `GET /dupes`, find the duplicated id and show that the list is not sorted.

#### Solutions

```python
# test_exercises.py
from collections import Counter
import pytest
from jsonschema import validate, ValidationError
from json_helpers import safe_json


# Exercise 1
def test_ex1_navigation(client):
    user = client.get("/users/3").json()
    assert user["address"]["city"] == "Gwenborough"
    assert isinstance(user["address"]["geo"]["lat"], str)
    assert float(user["address"]["geo"]["lat"]) < 0
    assert user["company"]["name"] == "Romaguera-Crona"


# Exercise 2
@pytest.mark.parametrize("path", ["/html", "/empty", "/truncated", "/pyrepr"])
def test_ex2_non_json_bodies(client, path):
    with pytest.raises(AssertionError) as info:
        safe_json(client.get(path))
    print(path, "->", info.value)


# Exercise 3
def test_ex3_phone_nulls(client):
    users = client.get("/users").json()
    null_ids = [u["id"] for u in users if u["phone"] is None]
    assert null_ids == [2, 4, 6, 8, 10]
    assert all(u["phone"] is None or isinstance(u["phone"], str) for u in users)
    assert all(u.get("fax") is None for u in users)


# Exercise 4
def test_ex4_comments(client):
    comments = client.get("/comments", params={"postId": 1}).json()
    assert len(comments) == 5
    assert all(c["postId"] == 1 for c in comments)
    assert all("@" in c["email"] for c in comments)


# Exercise 5
def test_ex5_floats(client):
    assert 1.1 * 3 != 3.3
    assert 1.1 * 3 == pytest.approx(3.3)
    order = client.get("/orders/1").json()
    computed = sum(i["qty"] * i["price"] for i in order["items"])
    assert computed == pytest.approx(order["total"], abs=0.005)


# Exercise 6
def test_ex6_partial_and_internal_fields(client):
    order = client.get("/orders/1").json()
    expected = {"id": 1, "status": "shipped", "coupon": None}
    assert {k: order.get(k, "<missing>") for k in expected} == expected
    internal = [k for k in order if k.lower().startswith("internal")]
    assert internal == ["internalId"]      # the defect we are hunting: it is exposed


# Exercise 7
def test_ex7_todo_schema(client):
    schema = {"type": "object", "required": ["userId", "id", "title", "completed"],
              "properties": {"userId": {"type": "integer"}, "id": {"type": "integer"},
                             "title": {"type": "string"}, "completed": {"type": "boolean"}}}
    body = client.get("/todos/1").json()
    validate(instance=body, schema=schema)
    schema["properties"]["completed"]["type"] = "string"
    with pytest.raises(ValidationError) as info:
        validate(instance=body, schema=schema)
    assert list(info.value.path) == ["completed"]
    assert info.value.message == "False is not of type 'string'"


# Exercise 8
def test_ex8_dupes_and_order(client):
    ids = [x["id"] for x in client.get("/dupes").json()]
    dupes = [k for k, n in Counter(ids).items() if n > 1]
    assert dupes == [3]
    assert ids != sorted(ids)
```

Notes on the solutions:

- **Exercise 1.** `float("-37.3159") < 0` converts the string before comparing; comparing the string directly with `0` would raise `TypeError`.
- **Exercise 2.** Expected and observed messages: `/html` reports status `502` and `text/html`; `/empty` reports status `204` and an empty text `''`; `/truncated` shows the cut-off string `'{"id": 1, "name": "Ann'`; `/pyrepr` shows `"{'id': 1}"`, whose single-quoted contents explain the failure. In each case the message contains the evidence.
- **Exercise 3.** The `u.get("fax") is None` line passes because `.get()` returns `None` for absent keys, which also shows the limitation: it cannot tell "absent" from "null".
- **Exercise 5.** `1.1 * 3` evaluates to `3.3000000000000003`. The `abs=0.005` tolerance means "within half a cent", appropriate for currency.
- **Exercise 6.** The final assertion expects `["internalId"]` so the test passes, documenting the defect. In a real project you would write `assert internal == []` and the test would fail, correctly flagging the leak.
- **Exercise 7.** The error says `False is not of type 'string'` at path `['completed']`: the message names the value, the expected type, and the location.
- **Exercise 8.** `Counter` finds `3` appearing twice, and `[3, 1, 3]` is not equal to its sorted version `[1, 3, 3]`.

---

### 14. Self-Check Quiz

Try to answer from memory, then check the answers after the questions.

1. A request returns `200` and a body of `<html><body>Maintenance</body></html>`. What exception does `response.json()` raise, and which exception class should you catch to stay compatible across `requests` versions?
2. What is the Python value of `json.loads('{"active": "true"}')["active"]`, and why does it matter?
3. Which of these is a valid JSON body: `{'a': 1}`, `{"a": 1,}`, `{"a": 1}`, `{a: 1}`?
4. You call `order["items"][5]` and get `IndexError`. What does that tell you about the response?
5. You get `TypeError: object of type 'NoneType' has no len()` on `len(product["tags"])`. What is the likely cause?
6. What is the difference between `body.get("coupon")` returning `None` and `body["coupon"]` returning `None`? How would you tell "absent" from "null"?
7. Why is `assert not user["phone"]` a poor way to test that a phone is null?
8. Why does `all(p["userId"] == 3 for p in posts)` pass when `posts` is an empty list, and how do you protect against it?
9. Why should you avoid `assert computed_total == order["total"]` for floating-point values, and what should you use instead?
10. In `jsonschema`, what is the difference between `properties` and `required`?
11. What does `validate()` return when the data is valid, and what does it raise when it is not? Does it report all problems or one?
12. What is the difference between a `ValidationError` and a `SchemaError`?
13. How do you describe "a string or null" in a schema?
14. When is it appropriate to assert a list's order, and what do you do when order is unspecified?

**Answers**

1. A `JSONDecodeError` with a message like `Expecting value: line 1 column 1 (char 0)`. Catch `ValueError`, which every variant of `JSONDecodeError` inherits from.
2. The string `'true'`, not the boolean `True`, because it is in quotes. Clients that expect a boolean would misbehave, so a type check (`isinstance(x, bool)`) catches the defect.
3. Only `{"a": 1}`. The first uses single quotes, the second has a trailing comma, and the fourth has an unquoted key.
4. The list has fewer than six items. Either the API returned fewer items than expected or your index is wrong.
5. The `tags` field is `null` (`None`) where a list was expected, so the contract of "always a list" is broken.
6. `.get()` returns `None` for both absent and `null`, while `[...]` raises `KeyError` for absent. Use `"coupon" in body` to tell whether the key exists.
7. Because it is also true for `""`, `0`, `[]`, and `False`; it cannot distinguish a correct empty value from a defective one. Use `is None`.
8. `all()` over an empty sequence is vacuously `True`. Add `assert len(posts) > 0` first.
9. Binary floating point cannot represent most decimals exactly (`0.1 + 0.2` is `0.30000000000000004`). Use `pytest.approx(expected)`, or work in integer cents or `Decimal`.
10. `properties` describes what each key's value must look like *if the key is present*; `required` lists keys that must be present. You usually need both.
11. It returns `None` when valid and raises `ValidationError` when invalid. It raises only one error (the best match); use `iter_errors` on a validator object to see all problems.
12. A `ValidationError` means the data violates the schema (the API is wrong). A `SchemaError` means the schema itself is malformed (your test is wrong).
13. `{"type": ["string", "null"]}`.
14. Only when the API documents an order (for example, sorted by id, newest first). When order is unspecified, compare `sorted(...)` or `set(...)` of the values so the test does not become flaky.

---

### Glossary

#### JSON

JavaScript Object Notation: a text format for structured data using objects, arrays, strings, numbers, booleans, and `null`. It is the standard body format of REST APIs.

#### Parsing

Converting text into data structures a program can work with. `response.json()` parses JSON text into Python `dict`, `list`, `str`, `int`, `float`, `bool`, and `None`.

#### `JSONDecodeError`

The exception raised when text is not valid JSON. It is a subclass of `ValueError`, carries `msg`, `lineno`, `colno`, `pos`, and `doc` attributes, and exists in both `json` and `requests.exceptions`.

#### Serialisation

The reverse of parsing: turning Python data into JSON text (`json.dumps`). A server bug in this step produces bodies such as `{'id': 1}`.

#### Assertion

A statement in a test that must be true. If it is false, the test fails. Assertions can carry a message to explain the failure.

#### Nested structure

Data containing other data: an object inside an object, or a list of objects. You reach inner values by chaining brackets, for example `body["address"]["city"]`.

#### `null` / `None`

The JSON value meaning "no value", parsed to Python `None`. It differs from a missing key, an empty string, an empty list, and zero.

#### Sentinel

A unique placeholder value, such as `"<missing>"`, used to distinguish "key absent" from a legitimate value like `None`.

#### `dict.get()`

A dictionary method that returns the value for a key, or a default (`None` unless you specify one) if the key is absent, without raising `KeyError`.

#### Truthiness

How Python treats a value in a boolean context. `None`, `0`, `""`, `[]`, `{}`, and `False` are all "falsy", which is why truthiness checks blur distinctions that API tests need to preserve.

#### List comprehension

A compact way to build a list: `[u["id"] for u in users if u["active"]]`. The workhorse of "extract this field from every item".

#### Vacuous truth

The logical fact that a rule about "every item" is true for an empty collection. `all(...)` over an empty list returns `True`.

#### Partial comparison

Comparing only selected fields of a response with expected values, ignoring other fields.

#### Echo check

A test that verifies a response reflects the data you sent in the request, typically after a `POST` or `PUT`.

#### Floating-point error

The tiny inaccuracies from storing decimal fractions in binary. `0.1 + 0.2` yields `0.30000000000000004`.

#### `pytest.approx`

A pytest helper that compares numbers within a tolerance: `assert x == pytest.approx(y)`.

#### Minor units

Representing money as integers of the smallest currency unit (cents), avoiding float errors.

#### `Decimal`

A Python type for exact decimal arithmetic, created from strings (`Decimal("19.99")`).

#### Flaky test

A test that sometimes passes and sometimes fails without any change to the code, commonly caused by relying on unspecified ordering or exact float equality.

#### JSON Schema

A JSON document that describes the allowed structure of other JSON documents: types, required keys, and per-key rules.

#### `jsonschema`

The Python library that checks data against a JSON Schema. Its main function is `validate(instance=..., schema=...)`.

#### `ValidationError`

The exception `jsonschema` raises when data does not satisfy a schema. Its `message`, `path`, `validator`, `instance`, and `schema_path` attributes explain what failed and where.

#### `SchemaError`

The exception raised when the schema itself is invalid (for example a misspelled type name). It signals a bug in your test, not in the API.

#### `type`, `required`, `properties`

The three basic schema keywords: `type` fixes the JSON type, `required` lists mandatory keys, and `properties` gives rules for individual keys that are present.

#### Contract

The agreed description of what an API accepts and returns: fields, types, rules, and behaviours. Validation tests enforce the contract.

#### Lab server

The small local API used in this lesson so every example can be reproduced offline.

---

## Summary

- A status code says the server responded; only the body shows whether the response is correct. Validate in layers: transport, status and headers, parsing, shape, content, and consistency, cheapest first.
- `response.json()` turns JSON into Python `dict`, `list`, `str`, `int`, `float`, `bool`, and `None`. It raises `JSONDecodeError` (a `ValueError`) for HTML pages, empty bodies, truncated text, and Python-style quoting. Wrap it in a `safe_json` helper that reports status, content type, and the start of the body.
- Navigate nested data with chained brackets. `KeyError` means a missing field, `IndexError` a shorter list than expected, and a `NoneType` `TypeError` means a `null` where a value was expected.
- Validate fields by presence, type, value, format, and range. Remember that `"true"` and `"1"` are strings, that `isinstance(True, int)` is `True`, and that a type check is the only way to catch a number delivered as text.
- Distinguish a missing key, `null`, `""`, `[]`, and `0`. Use `dict.get()` for optional fields, `in` for existence, and `is None` for null; avoid truthiness checks.
- For lists, check the container type, length, every-item rules with `all()` (guarded by a non-empty check), existence with `any()`, uniqueness with `set` or `Counter`, and order only when the API promises it. Collect offenders and assert the list is empty for the best failure messages.
- Compare dictionaries fully only when they are small and stable; otherwise project to the fields that matter. Verify echoes after a `POST`, and verify that sensitive or internal fields are absent.
- Never compare computed floats with `==`: use `pytest.approx`, integer minor units, or `Decimal`. Never depend on list order unless it is documented; JSON object key order never matters.
- With `jsonschema`, `validate(instance, schema)` returns `None` or raises one `ValidationError`; a schema built from `type`, `required`, and `properties` describes shape; `iter_errors` reports all problems; a `SchemaError` means your own schema is broken. Keep a negative test so that you know the schema can fail.
- Wednesday's lesson goes deeper into request and response validation; today's tools are the foundation.

## Additional Resources

- JSON Schema, *Understanding JSON Schema* (official guide to types, required, properties, and more): https://json-schema.org/understanding-json-schema/
- JSON Schema, home page and specification index: https://json-schema.org/
- `jsonschema` library documentation (`validate`, `ValidationError`, validators): https://python-jsonschema.readthedocs.io/en/stable/
- `jsonschema` error handling reference (`best_match`, `iter_errors`, error attributes): https://python-jsonschema.readthedocs.io/en/stable/errors/
- Python documentation, *json: JSON encoder and decoder*: https://docs.python.org/3/library/json.html
- Python documentation, *Built-in Types: mapping types (dict, `dict.get`)*: https://docs.python.org/3/library/stdtypes.html#mapping-types-dict
- pytest documentation, *`pytest.approx`*: https://docs.pytest.org/en/stable/reference/reference.html#pytest-approx
- Requests documentation, *JSON response content*: https://requests.readthedocs.io/en/latest/user/quickstart/#json-response-content
