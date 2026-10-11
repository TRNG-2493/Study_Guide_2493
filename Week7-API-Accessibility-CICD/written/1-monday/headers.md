# Headers

## Learning Objectives

By the end of this lesson you will be able to:

- Explain what an HTTP header is, read its anatomy (name, colon, value), and describe how names, multiple values, and custom `X-` headers behave.
- Classify headers as request, response, representation, or general headers, and say why that classification helps when debugging.
- Explain the purpose, typical values, sender, common failure, and a test idea for each important header: `Content-Type`, `Accept`, `Accept-Language`, `Accept-Encoding`, `Content-Encoding`, `Authorization`, `WWW-Authenticate`, `User-Agent`, `Host`, `Origin`, `Referer`, `Content-Length`, `Transfer-Encoding`, `Cache-Control`, `ETag`, `Last-Modified`, `If-None-Match`, `Location`, `Set-Cookie`, `Cookie`, `Retry-After`, `Allow`, the CORS family, the security family, `Server`, `X-Powered-By`, `X-Request-Id`, and `traceparent`.
- Decode a Basic authentication header by hand and recognise Bearer tokens and API key headers.
- Add, change, hide, and inspect headers using `curl` and Postman, and predict what each command prints.
- Write Postman test scripts that verify headers and explain every line.
- Build header-based negative test tables and diagnose real failures (`401`, `403`, `406`, `415`, `429`, `304`, and a CORS error) by reading headers.
- Handle secrets that travel in headers safely.

---

## Why This Matters

This week's epic is to build a pipeline-ready API test framework for Project 2. Every API test you write this week, in Postman today and in Python from tomorrow, is really a conversation made of requests and responses. In the previous lesson on HTTP messages you saw that each message has a start line, headers, a blank line, and an optional body. The body usually gets all the attention because it contains the data. The headers, however, decide whether the conversation works at all.

Headers are the control panel of an HTTP message. They tell the server which format your body is in, which format you want back, who you are, whether you are allowed in, whether the answer may be stored and reused, which server name you intended, how big the body is, and where a newly created resource lives. When the server answers, headers tell you how long to wait before retrying, where to go next, which cookies to remember, how to trace the request in the server's logs, and which security rules the browser must enforce.

A large share of "mysterious" API failures are header problems. A request returns `415 Unsupported Media Type` because `Content-Type` was missing. A request returns `401 Unauthorized` because an `Authorization` header had a typo. A request returns `406 Not Acceptable` because `Accept` asked for a format the API never produces. A front-end developer reports "the API is broken" when the real problem is a missing CORS header. A tester who can read headers fluently resolves these problems in minutes, while a tester who only looks at the body can lose hours.

Headers are also test targets in their own right. A well-written API test asserts that the response carries the correct `Content-Type`, that a created resource comes with a `Location`, that sensitive responses are marked `no-store`, and that the server does not leak its software version. These checks are cheap to write and catch real defects.

Tomorrow you will send these same headers from Python code, including authentication, and on Friday you will see how a CI/CD pipeline stores secrets so they can be placed in headers safely. Today the goal is to understand the headers themselves, using only `curl` and Postman, so that when you automate them you already know what you are automating.

---

## The Concept

### 1. What Is a Header?

An HTTP header is a single line of metadata attached to a request or a response. "Metadata" means data about data: the body is the data, and the headers describe it and describe how the exchange should be handled.

Think of a parcel delivered to your door. The parcel's contents are the body. The label on the outside carries the address, the sender, a "fragile" sticker, a weight, a tracking number, and perhaps a "signature required" instruction. The courier reads the label without opening the box and decides how to handle it. HTTP software does the same with headers: proxies, caches, load balancers, browsers, and servers read headers to decide what to do before (or without) looking at the body.

Here is a complete request and response so that you can see where headers sit:

```http
POST /posts HTTP/1.1
Host: jsonplaceholder.typicode.com
Content-Type: application/json
Accept: application/json
Content-Length: 43

{"title":"Hello","body":"World","userId":1}
```

```http
HTTP/1.1 201 Created
Content-Type: application/json; charset=utf-8
Content-Length: 65
Location: https://jsonplaceholder.typicode.com/posts/101
Cache-Control: no-cache

{"title":"Hello","body":"World","userId":1,"id":101}
```

The first block is a request. Its first line is the request line (method, path, protocol version). The four lines that follow, up to the blank line, are headers. After the blank line comes the body. The second block is a response. Its first line is the status line (version, status code, reason phrase), followed by four headers, a blank line, and the body. The blank line is not decoration. It is the signal that tells the receiver "the headers have ended, the body starts now."

### 2. Anatomy of a Header

Every header follows the same pattern:

```
Header-Name: header value
```

There are three parts: the **name**, a **colon**, and the **value**. Let us look at the rules for each.

**The name.** Header names are case-insensitive. `Content-Type`, `content-type`, and `CONTENT-TYPE` are the same header. In HTTP/2 and HTTP/3, names are actually transmitted in lowercase, so tools often show `content-type` even when you typed `Content-Type`. This matters for test code: if you compare header names with exact string matching, your test may fail for no good reason. Good test tools, including Postman's `pm.response.headers.get()` and Python's `requests`, look up names case-insensitively. Conventionally names are written in Title-Case with hyphens, and they cannot contain spaces.

**The colon and spacing.** A single colon separates the name from the value. Optional whitespace after the colon is ignored, so `Accept:application/json` and `Accept:   application/json` mean the same thing. There must be no space between the name and the colon.

**The value.** Header values are case-sensitive or not depending on the header. The media type in `Content-Type: application/json` is compared case-insensitively, but values such as a bearer token or an `ETag` are compared exactly, so changing one letter produces a different token. Never assume; check what the header means.

**Multiple values.** Some headers carry several values separated by commas. For example:

```
Accept: application/json, text/html;q=0.8, */*;q=0.1
Cache-Control: no-cache, no-store, must-revalidate
```

If a header appears on separate lines more than once, such as two `Accept` lines, the receiver is allowed to treat them as one comma-joined list. The notable exception is `Set-Cookie`, which must stay on separate lines because cookie dates contain commas.

**Parameters.** A value may carry parameters after a semicolon, such as `charset=utf-8` in `Content-Type: application/json; charset=utf-8` or `q=0.8` in the `Accept` example. The part before the semicolon is the main value, and the parameters refine it.

**Line folding.** Old versions of the HTTP specification allowed a long value to continue on the next line if that line began with a space or tab. This is called obsolete line folding. Modern clients and servers must not produce it, and many servers reject it because folded lines have been used in attacks. You will rarely meet it, but if a very old system sends folded headers, a parser may read the continuation as a new header and misbehave. That is a good reason to treat odd, malformed headers as a negative-test idea.

**Custom headers and the `X-` convention.** Anyone can invent a header. For many years, custom headers were given an `X-` prefix (for "extension") to avoid clashing with official ones, which is why you see `X-API-Key`, `X-Request-Id`, `X-RateLimit-Remaining`, and `X-Powered-By`. In 2012 this convention was formally deprecated (RFC 6648), because headers that became popular, such as `X-Forwarded-For`, were stuck with the `X-` forever, and standardising them meant either renaming them or living with the prefix. The modern convention is to use a clear, descriptive name without the prefix, ideally one that includes your product or organisation name if the header is specific to you, for example `Acme-Correlation-Id`. You will still see `X-` headers everywhere in real APIs, so recognise both styles. As a tester, the important point is that a custom header is part of the API contract just like a field in the body: document it, test that it is present when it should be, and test what happens when it is missing.

**Practical limits.** Servers limit the total size of headers (often 8 KB to 16 KB) and the size of any single header. Exceeding the limit usually produces `431 Request Header Fields Too Large` or `400 Bad Request`. This is a useful boundary test.

### 3. The Families of Headers

The HTTP specification groups headers by what they describe. Knowing the group tells you who normally sends the header and where to look when you debug.

| Family | Describes | Direction | Examples |
|--------|-----------|-----------|----------|
| **Request headers** | The request itself and the client making it | Client to server | `Accept`, `Authorization`, `User-Agent`, `Host`, `Origin`, `Cookie`, `If-None-Match` |
| **Response headers** | The response itself and the server producing it | Server to client | `Set-Cookie`, `Location`, `Retry-After`, `WWW-Authenticate`, `Server`, `Allow` |
| **Representation headers** | The body (the "representation" of the resource) | Either direction | `Content-Type`, `Content-Length`, `Content-Encoding`, `Content-Language` |
| **General headers** | The message as a whole, not the body | Either direction | `Cache-Control`, `Connection`, `Date`, `Via` |

Here is a simple way to remember them: request headers are the client's instructions and credentials, response headers are the server's instructions and status notes, representation headers are the label on the body, and general headers do not fit neatly anywhere else. Note that the categories are a teaching aid. The same header name can behave differently by direction. `Cache-Control` appears in both requests and responses with different meanings, and `Content-Type` describes a request body when sent by the client and a response body when sent by the server.

When you read a failing exchange, ask three questions in order. Did the client send the right request headers? Did the server send the right response headers? Do the representation headers truthfully describe the bodies? Most header bugs are answered by one of these three.

### 4. Content-Type: "What Is in the Body?"

`Content-Type` declares the media type of the body in the message that carries it. A media type (also called a MIME type) has the form `type/subtype`, such as `text/html` or `application/json`.

| Value | Meaning |
|-------|---------|
| `application/json` | JSON text, the most common API format |
| `application/xml` or `text/xml` | XML text |
| `text/plain` | Plain text with no structure |
| `text/html` | An HTML page |
| `application/x-www-form-urlencoded` | HTML-form style `key=value&key2=value2` |
| `multipart/form-data` | File uploads and mixed form data |
| `application/octet-stream` | Arbitrary binary data |
| `application/pdf`, `image/png` | A PDF document, a PNG image |

**Sent by:** the client on requests that have a body (`POST`, `PUT`, `PATCH`), and the server on any response that has a body.

**Purpose:** the receiver must know how to parse the bytes. A JSON parser fed form data fails, and a form parser fed JSON finds no fields. Without the header, the receiver may guess or refuse.

**Charset.** Text formats may state a character encoding as a parameter: `Content-Type: application/json; charset=utf-8`. Characters such as `é`, `ñ`, or `€` are turned into bytes using an encoding, and `utf-8` is the standard. For JSON, UTF-8 is the required encoding, so the charset parameter is optional and some servers omit it. For `text/*` types it matters more. If a response declares `charset=iso-8859-1` but contains UTF-8 bytes, accented characters appear garbled (a bug called mojibake). A test idea is to send a name such as `José Müller` and check that it comes back unchanged.

**Boundary for multipart.** A `multipart/form-data` body contains several parts, for example a text field and a file. The parts are separated by a delimiter string called the boundary, which must appear in the header so the receiver can split the body:

```http
POST /upload HTTP/1.1
Host: api.example.com
Content-Type: multipart/form-data; boundary=----QAboundary7MA4YWxk

------QAboundary7MA4YWxk
Content-Disposition: form-data; name="description"

Quarterly report
------QAboundary7MA4YWxk
Content-Disposition: form-data; name="file"; filename="report.csv"
Content-Type: text/csv

id,total
1,250
------QAboundary7MA4YWxk--
```

The header's `boundary` value defines the separator. Each part begins with `--` followed by the boundary, each part has its own small header block (`Content-Disposition` names the field, and an inner `Content-Type` types the file), and the final boundary ends with two extra dashes. Notice that you never write the boundary yourself in Postman or `curl`; the tool generates it. This is why you should never type a `Content-Type: multipart/form-data` header by hand in a tool: without the matching boundary the server cannot split the body, and you will receive `400` or `415`. Let the tool add it when you choose form-data.

**`application/json` versus `+json`.** Some APIs use more specific media types that still contain JSON. The suffix `+json` says "this is JSON, with a more specific meaning." Examples include `application/problem+json` (a standard format for error details), `application/vnd.github+json` (a vendor-specific type), and `application/hal+json` (hypermedia). A test that checks for exactly `application/json` will fail on `application/problem+json`, even though it is valid JSON. When you write assertions, decide whether you mean "is exactly `application/json`" or "is some JSON type," and write the check accordingly (for example, check that the value includes `json`).

**What goes wrong:**

- Missing `Content-Type` on a `POST`: the server returns `415` or `400`, or silently treats the body as empty.
- Wrong `Content-Type` (declaring `text/plain` for a JSON body): `415`, or a parse failure.
- Declaring JSON but sending invalid JSON: `400 Bad Request` with a parse error message.
- A response that should be JSON arrives as `text/html`, typically because a gateway or error page replaced the real answer, even with status `200`.

**Test idea:** For every endpoint, assert the response `Content-Type` as well as the status. Also send a request with a deliberately wrong `Content-Type` and assert a clean `415`, not a `500`.

### 5. Accept and Content Negotiation

`Accept` is sent by the client to say which media types it is able to handle in the response:

```
Accept: application/json
```

**Sent by:** the client. **Purpose:** to let one URL offer several formats. The same `/users/1` might be available as JSON, XML, or CSV, and the client picks one with `Accept`. This process, in which client and server agree on the best representation, is called **content negotiation**.

**Q-values.** A client can list several types and rank them with a quality value, or q-value, a number from 0 to 1 written as `q=`. A higher q means a stronger preference, and a missing q means 1.0:

```
Accept: application/json, application/xml;q=0.8, */*;q=0.1
```

This says: "I prefer JSON (1.0). If you cannot do JSON, XML is acceptable (0.8). Anything else is a last resort (0.1)." The `*/*` is a wildcard meaning any type, and `text/*` would mean any text type. `q=0` means "not acceptable at all."

**The server's side.** The server compares the client's list with what it can produce and returns the best match, stating the choice in the response `Content-Type`. If there is no match, the correct response is `406 Not Acceptable`. In practice many APIs ignore `Accept` and always return JSON, which is permitted by the specification (the server may disregard it) but means that `406` tests will not behave as you expect against those APIs. Always read the API's documentation or test and record the actual behaviour.

**Do not confuse the pair.** `Content-Type` describes the body that is being sent. `Accept` describes the response that is wanted. When you `POST` JSON and want JSON back, you send both. When you `GET` there is no request body, so there is normally no request `Content-Type`, but you still can send `Accept`.

| Header | Sent in | Question answered | Example |
|--------|---------|-------------------|---------|
| `Content-Type` | Request or response | "What is in this body?" | `application/json` |
| `Accept` | Request only | "What can I read in the reply?" | `application/json` |

**Other negotiation headers.**

`Accept-Language` states preferred human languages: `Accept-Language: fr-CA, fr;q=0.9, en;q=0.5`. The server may answer in French (Canadian preferred) and report the choice in `Content-Language: fr-CA`. A test idea is to request each supported language and check that error messages or labels change.

`Accept-Encoding` states which compression algorithms the client can decompress: `Accept-Encoding: gzip, deflate, br`. If the server compresses the body, it says so in the response header `Content-Encoding: gzip`. The `Content-Length` then refers to the compressed size, and the client must decompress before reading the body. Browsers, Postman, and Python's `requests` handle this automatically. With `curl`, add `--compressed`, which sends `Accept-Encoding` for you and decompresses the result. Without `--compressed`, `curl` shows raw unreadable bytes if the server compresses anyway. Test ideas: check that a large JSON response is compressed when the client allows it (smaller payload, faster mobile experience), and check that the API still works when the client sends `Accept-Encoding: identity` (meaning "no compression please").

**What goes wrong:** A tester sets `Accept: application/xml`, receives JSON with `200`, and wrongly reports a defect, while the API simply ignores `Accept`. Or the reverse: the API correctly returns `406` and the tester's script crashes because it assumed JSON. Always check the contract first.

### 6. Authorization: "Who Am I?"

HTTP is stateless: each request stands alone, and the server remembers nothing between requests. Therefore the client must prove its identity on every request, and the standard place is the `Authorization` request header. The format is always `Authorization: <scheme> <credentials>`, where the scheme names the method.

**Basic authentication.** The credentials are `username:password` joined with a colon and then encoded with Base64. Let us decode a real example step by step. Suppose a tester receives this header:

```
Authorization: Basic cWFfdGVzdGVyOlNwcmluZzIwMjYh
```

Step 1: Remove the scheme word `Basic` and the space. The credential string is `cWFfdGVzdGVyOlNwcmluZzIwMjYh`.

Step 2: Understand Base64. It turns every 3 bytes of data into 4 printable characters, using an alphabet of 64 symbols: `A` to `Z` are values 0 to 25, `a` to `z` are 26 to 51, `0` to `9` are 52 to 61, `+` is 62, and `/` is 63. Each character therefore stands for 6 bits.

Step 3: Decode the first four characters, `cWFf`. Their values are `c` = 28, `W` = 22, `F` = 5, `f` = 31. In 6-bit binary these are `011100`, `010110`, `000101`, `011111`.

Step 4: Join the 24 bits and regroup them as 8-bit bytes: `011100010110000101011111` becomes `01110001`, `01100001`, `01011111`. In decimal these are 113, 97, 95, which are the ASCII codes for `q`, `a`, `_`. So the first three characters are `qa_`.

Step 5: Repeat for each group of four characters. Doing the whole string (or running `echo 'cWFfdGVzdGVyOlNwcmluZzIwMjYh' | base64 -d` in a terminal) gives:

```
qa_tester:Spring2026!
```

Step 6: Split at the first colon. The username is `qa_tester` and the password is `Spring2026!`.

To create such a header yourself, run `printf 'qa_tester:Spring2026!' | base64`. Use `printf` rather than `echo` so that no hidden newline is added to the text, because a trailing newline changes the result and breaks the login. A trailing newline in the encoded text is a classic reason for a "correct" password being rejected. Note that `=` signs at the end of a Base64 string are padding that appears when the data length is not a multiple of three bytes, as in `QWxhZGRpbjpvcGVuIHNlc2FtZQ==`.

The big lesson is that Base64 is encoding, not encryption. There is no key, and anyone who sees the header can decode it in a second. Basic authentication is therefore only acceptable over HTTPS, and any screenshot or log containing a Basic header exposes the real password. `curl -u username:password` builds this header for you, and Postman's Authorization tab does the same.

**Bearer tokens.** A bearer token is a string issued to the client after it proves its identity, for example by logging in. It is then sent on later requests:

```
Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIxMjMiLCJyb2xlIjoicWEifQ.sig
```

"Bearer" means "whoever bears (carries) this token is let in," exactly like a concert ticket: nobody checks your name, they check the ticket. That is why a stolen token is as dangerous as a stolen password until it expires. Many bearer tokens are JWTs (JSON Web Tokens), which have three parts separated by dots: a header, a payload of claims such as user id and expiry, and a signature. The first two parts are only Base64URL-encoded, not encrypted, so you can paste a token into a decoder to read its claims, which is a useful testing technique (for example, to see why a token was rejected as expired) but also a reminder never to place secrets inside a JWT payload. The exact way tokens are obtained and refreshed is covered when you automate authentication tomorrow; today you only need to recognise the format and send a token you were given.

**API key headers.** Many APIs identify the calling application with a key rather than a user login. There is no standard header name; common choices are `X-API-Key: 12345abcde`, `Api-Key: ...`, or a vendor-specific name. Some APIs accept the key in a query string instead, which is weaker because URLs are logged by proxies and stored in browser history, whereas headers are logged less often. Always follow the API's documentation to learn the exact name.

**`WWW-Authenticate`: the server's challenge.** When a request lacks valid credentials, the server replies `401 Unauthorized` and includes a `WWW-Authenticate` response header that tells the client which schemes it may use:

```
HTTP/1.1 401 Unauthorized
WWW-Authenticate: Basic realm="Project2 API", charset="UTF-8"
```

```
HTTP/1.1 401 Unauthorized
WWW-Authenticate: Bearer realm="reports", error="invalid_token", error_description="The access token expired"
```

The first line tells you to use Basic, and the second shows a Bearer challenge that even explains the failure (an expired token). The `realm` is a label for the protected area. For a tester, `WWW-Authenticate` is the quickest way to learn what an API expects. A well-behaved API always includes it with a `401`; a missing one is a minor compliance defect worth reporting.

**What goes wrong:** misspelled scheme (`Bearer` versus `Bearrer`), missing space after the scheme, the word `Bearer` repeated twice because a variable already contains it, a token with a trailing newline, an expired token, or credentials sent in the wrong header.

**Test idea:** Build a table of authentication variations (no header, empty value, wrong scheme, malformed Base64, expired token, valid token) and assert `401` for each broken case, with `WWW-Authenticate` present. Distinguish `401` (we do not know who you are) from `403` (we know who you are, but you may not do this).

### 7. User-Agent, Host, Origin, and Referer

**`User-Agent`** identifies the client software: `PostmanRuntime/7.37.0`, `curl/8.5.0`, `python-requests/2.32.0`, or a long browser string such as `Mozilla/5.0 (Windows NT 10.0; Win64; x64) ...`. It is sent by the client, usually set automatically. Servers use it for analytics, debugging, and sometimes blocking. Some firewalls reject the default agent of scripting tools, which produces a `403` for `curl` that does not occur in a browser. A test idea is to confirm the API behaves the same for different agents, and that custom agents such as `MyCompany-QA/1.0` are logged, which helps the operations team recognise test traffic.

**`Host`** names the server and port you want: `Host: api.example.com`. It is mandatory in HTTP/1.1 and is taken from the URL by every tool. It exists because one IP address can serve many websites (virtual hosting), and the server needs the name to choose the correct one. What goes wrong: a mismatched `Host` produces `404`, a default website, or `400`. Test idea: send the correct URL but override `Host` with a wrong name and confirm the system rejects it cleanly, since host header handling is also a security concern (host header injection can poison password reset links).

**`Origin`** is sent by browsers on cross-site requests and on some others (for example `POST`). It contains the scheme, host, and port of the page that started the request, such as `Origin: https://app.example.com`. It has no path. The server uses it to decide whether to allow the call (see CORS below). Non-browser tools such as Postman do not send `Origin` unless you add it, which is why an API can "work in Postman" and still fail in a browser.

**`Referer`** (the misspelling is historical and permanent) gives the full URL of the page that led to the request, for example `Referer: https://app.example.com/orders`. It is sent by browsers. Servers use it for analytics and, weakly, for security checks. Because it can reveal private URLs, a response policy header called `Referrer-Policy` limits what is sent. Neither `Origin` nor `Referer` can be trusted for security by itself, because non-browser clients can set any value they like.

### 8. Content-Length and Transfer-Encoding

`Content-Length` states the size of the body in bytes: `Content-Length: 43` for the 43-byte JSON in our first example. The receiver uses it to know where the body ends. Tools calculate it automatically, and you should almost never set it by hand. If the declared length is smaller than the real body, the server cuts the body off and the JSON becomes invalid. If it is larger, the server waits for bytes that never arrive, and the request hangs until a timeout. A response without a body, such as `204 No Content` or the answer to a `HEAD` request, either has no `Content-Length` or has the length that the full response would have had for `HEAD`. A related test is to confirm a `HEAD` request returns the same headers as `GET` but no body.

`Transfer-Encoding: chunked` is used when the sender does not know the total size in advance, for instance a streamed or dynamically generated report. Instead of a length, the body is sent as a series of chunks, each prefixed by its size in hexadecimal, ending with a zero-sized chunk:

```
HTTP/1.1 200 OK
Content-Type: application/json
Transfer-Encoding: chunked

1a
{"items":[1,2,3,4,5,6,
b
7,8,9,10]}
0
```

The first chunk is `1a` hex (26 bytes), the second is `b` (11 bytes), and the `0` chunk marks the end. A message uses `Transfer-Encoding: chunked` or `Content-Length`, not both. Tools reassemble chunks transparently so you rarely see this, but a response with chunked encoding and no length can explain why a progress bar or size check is impossible. Test ideas: check that large exports stream completely and that the final JSON is valid.

### 9. Caching: Cache-Control, ETag, Last-Modified, If-None-Match, and 304

Caching lets clients and intermediaries reuse a stored response instead of asking the server again. It makes systems faster and cheaper, but wrong caching headers cause stale data (users see old balances) or leaked data (a private page cached on a shared proxy).

**`Cache-Control`** is a general header whose directives state the rules. A response may use:

| Directive | Meaning |
|-----------|---------|
| `max-age=3600` | The response is fresh for 3600 seconds (one hour); reuse it without asking the server |
| `no-cache` | You may store it, but you must revalidate with the server before each reuse |
| `no-store` | Do not store this at all (use for sensitive data) |
| `private` | Only the end user's own cache may store it, not shared proxies |
| `public` | Any cache may store it |
| `must-revalidate` | Once stale, do not reuse without checking with the server |

A common confusion is that `no-cache` does not mean "do not cache"; it means "check before reuse." The directive that forbids storing is `no-store`.

**Validators.** When a cached copy becomes stale, the client can ask "has it changed?" using a validator. `ETag` is a response header carrying an opaque version identifier of the resource, such as `ETag: "v7-a91f"`. `Last-Modified` carries the time of the last change: `Last-Modified: Tue, 06 Oct 2026 08:00:00 GMT`. The client remembers them and, later, sends them back as `If-None-Match: "v7-a91f"` or `If-Modified-Since: Tue, 06 Oct 2026 08:00:00 GMT`.

**A worked sequence of the 304 flow.**

Request 1, nothing cached yet:

```http
GET /products/42 HTTP/1.1
Host: api.example.com
Accept: application/json
```

Response 1, a full answer with a validator:

```http
HTTP/1.1 200 OK
Content-Type: application/json
Cache-Control: max-age=60
ETag: "v7-a91f"
Content-Length: 58

{"id":42,"name":"Notebook","price":4.5,"stock":120}
```

The client stores the body together with the `ETag` and treats it as fresh for 60 seconds. During those 60 seconds, a browser would not even contact the server.

Request 2, five minutes later, so the copy is stale. The client asks conditionally:

```http
GET /products/42 HTTP/1.1
Host: api.example.com
Accept: application/json
If-None-Match: "v7-a91f"
```

Response 2, when the product has not changed:

```http
HTTP/1.1 304 Not Modified
ETag: "v7-a91f"
Cache-Control: max-age=60
```

There is no body, so it is tiny and fast, and the client reuses its stored copy and starts a fresh 60-second window.

Request 3, after someone changes the price. The client again sends `If-None-Match: "v7-a91f"`. The server sees that the current version is different and returns a full `200 OK` with the new body and `ETag: "v8-c3d2"`. The cycle repeats.

The practical points for a tester: a `304` is not an error but a success that means "use what you have"; a `304` response has no body, so a test that tries to parse JSON from it will crash; and Postman may send conditional headers automatically only if you add them. Test ideas: confirm `ETag` is present on a `GET`, send it back in `If-None-Match` and expect `304`, modify the resource and expect `200` with a new `ETag`, and confirm sensitive responses (profile, payment data) carry `Cache-Control: no-store`.

### 10. Location

`Location` is a response header holding a URL. It appears with `201 Created` to point to the new resource (`Location: /users/101`), and with redirects such as `301`, `302`, `303`, `307`, and `308` to point to where the client should go next. It may be an absolute URL or a relative one. After a creation, a good test takes the value, follows it with `GET`, and confirms the resource exists. What goes wrong: a missing `Location` on `201`, a `Location` that points to an internal host name such as `http://10.0.0.5:8080/users/101` which the client cannot reach, or a redirect loop. `curl` does not follow redirects unless you add `-L`, so a `301` simply prints its headers.

### 11. Cookies: Set-Cookie and Cookie

A cookie is a small piece of text the server asks the client to remember and send back, which is the classic way browser sessions work on top of stateless HTTP. The server sends a response header `Set-Cookie`, and the client returns the cookie in a request header `Cookie` on later requests to the same site.

```
Set-Cookie: sessionId=abc123; Path=/; Max-Age=3600; Secure; HttpOnly; SameSite=Strict
```

The first piece, `sessionId=abc123`, is the name and value. The rest are attributes that control behaviour:

| Attribute | Meaning | Why it matters |
|-----------|---------|----------------|
| `Expires=Wed, 21 Oct 2026 07:28:00 GMT` | Absolute date after which the cookie is discarded | Without it or `Max-Age`, the cookie lasts only for the browser session |
| `Max-Age=3600` | Lifetime in seconds from now; wins over `Expires` if both exist | Controls how long a login lasts |
| `Path=/` | The cookie is sent only for URLs under this path | Limits scope |
| `Domain=example.com` | The cookie is also sent to subdomains | Too broad a domain widens exposure |
| `Secure` | Send only over HTTPS | Prevents leaking over plain HTTP |
| `HttpOnly` | Not readable by JavaScript on the page | Stops theft of session cookies through script injection (XSS) |
| `SameSite=Strict/Lax/None` | Controls whether the cookie is sent on cross-site requests | Protects against cross-site request forgery (CSRF); `None` requires `Secure` |

The follow-up request looks like this:

```
Cookie: sessionId=abc123; theme=dark
```

The client sends only the name-value pairs, not the attributes, and joins several cookies with semicolons. Tester's view: a session cookie should have `Secure`, `HttpOnly`, and a sensible `SameSite`; a login that sets a session cookie without `HttpOnly` is a security finding. Also test that logging out invalidates the cookie, that an expired cookie is rejected, and that a tampered value is rejected. `curl` can store and send cookies with `-c cookies.txt` (write to a jar) and `-b cookies.txt` (read from a jar), and Postman has a cookie jar that you open from the **Cookies** link under the Send button.

### 12. Rate Limiting: Retry-After and RateLimit Headers

To protect themselves from overload and abuse, APIs limit how many requests a client may send in a time window. When you exceed the limit, the server answers `429 Too Many Requests`. Headers explain the situation:

```http
HTTP/1.1 429 Too Many Requests
Retry-After: 30
X-RateLimit-Limit: 100
X-RateLimit-Remaining: 0
X-RateLimit-Reset: 1791709200
Content-Type: application/json

{"error":"Rate limit exceeded"}
```

`Retry-After` tells the client how long to wait, either as seconds (`30`) or as a date. The `X-RateLimit-*` names are a widespread convention rather than a standard, so check the documentation. `Limit` is the allowance per window, `Remaining` is what is left, and `Reset` says when the window resets, often as a Unix timestamp. A newer standardised family drops the `X-` prefix (`RateLimit-Limit`, `RateLimit-Remaining`, `RateLimit-Reset`). The same `Retry-After` header also appears with `503 Service Unavailable` during maintenance. Tests: confirm `Remaining` decreases by one per call, confirm the limit triggers `429` with `Retry-After`, and confirm the API works again after the wait. Be careful not to hammer a shared environment; rate-limit tests should run against a safe test instance.

### 13. Allow

`Allow` is a response header that lists the methods a resource supports: `Allow: GET, POST, OPTIONS`. It is required with `405 Method Not Allowed`, so that the client knows what to use instead, and it appears in answers to `OPTIONS`. A test sends `DELETE` to a read-only resource and asserts `405` plus an `Allow` header that does not include `DELETE`. What goes wrong is a `405` without `Allow`, or a `404` returned where `405` is correct.

### 14. CORS: Awareness for Testers

Browsers enforce the **same-origin policy**: a script on `https://app.example.com` may not freely read responses from `https://api.example.com`, because those are different origins (an origin is scheme plus host plus port). **CORS** (Cross-Origin Resource Sharing) is the mechanism by which the API server says, through response headers, "this other origin is allowed." CORS is enforced by the browser, not by the server and not by Postman. That single fact explains a famous puzzle: the API works perfectly in Postman and `curl` but fails in the web application.

The key response headers are:

| Header | Meaning | Example |
|--------|---------|---------|
| `Access-Control-Allow-Origin` | Which origin may read the response | `https://app.example.com` (or `*`) |
| `Access-Control-Allow-Methods` | Methods allowed for cross-origin calls | `GET, POST, PUT, DELETE` |
| `Access-Control-Allow-Headers` | Request headers the client may send | `Content-Type, Authorization` |
| `Access-Control-Allow-Credentials` | May cookies or auth be included | `true` |
| `Access-Control-Max-Age` | How long the browser may cache the preflight answer | `600` |

**Preflight.** For requests that could have side effects, such as a `PUT`, or a `POST` with `Content-Type: application/json`, or one with an `Authorization` header, the browser first sends an automatic `OPTIONS` request, the preflight, asking permission:

```http
OPTIONS /orders HTTP/1.1
Host: api.example.com
Origin: https://app.example.com
Access-Control-Request-Method: POST
Access-Control-Request-Headers: content-type, authorization
```

```http
HTTP/1.1 204 No Content
Access-Control-Allow-Origin: https://app.example.com
Access-Control-Allow-Methods: GET, POST, PUT, DELETE
Access-Control-Allow-Headers: Content-Type, Authorization
Access-Control-Max-Age: 600
```

If the answer permits the origin, method, and headers, the browser sends the real request. If not, the browser blocks it and prints a CORS error in its console, even though the server may have handled the request. Rules to remember: `Access-Control-Allow-Origin: *` cannot be combined with `Access-Control-Allow-Credentials: true`; the allowed origin must be an exact, trusted value; and a wildcard on an API that uses cookies is a security finding.

**Why it matters to testers.** You can test CORS without a browser by sending the `Origin` header yourself with `curl` or Postman and checking the response headers. A permissive `*` on a sensitive API, a reflected arbitrary `Origin`, or a missing header for a legitimate front end are all defects. This is awareness-level knowledge; full browser-based testing of front ends is outside today's scope.

### 15. Security Response Headers

These headers instruct browsers to apply protections. They matter most for web pages, but APIs that serve any content should still send sensible ones.

| Header | Example | Purpose |
|--------|---------|---------|
| `Strict-Transport-Security` (HSTS) | `max-age=31536000; includeSubDomains` | Tells the browser to use HTTPS only for this host for the next year, blocking downgrade attacks |
| `Content-Security-Policy` (CSP) | `default-src 'self'` | Restricts where scripts, images, and other resources may load from, which limits the damage of injected scripts |
| `X-Content-Type-Options` | `nosniff` | Stops the browser from guessing a different content type than declared, which prevents some script-injection tricks |
| `X-Frame-Options` | `DENY` | Forbids showing the page inside a frame, preventing clickjacking (modern sites also use the CSP `frame-ancestors` directive) |

A test idea is to assert that these headers exist on key responses. A missing `X-Content-Type-Options: nosniff` is a cheap, valid finding, and its worth grows when an API returns user-supplied content.

### 16. Information Disclosure: Server and X-Powered-By

`Server: Apache/2.4.41 (Ubuntu)` and `X-Powered-By: PHP/7.2.1` or `Express` reveal software and often exact versions. An attacker can look up known vulnerabilities for that version. The best practice is to remove `X-Powered-By` and to make `Server` generic or absent. Testers report these as low-severity information-disclosure findings. The assertion is simple: the header must not exist, or must not contain a version number.

### 17. Request Tracing: X-Request-Id and traceparent

In a system of many services, one user action may pass through a gateway, several microservices, and a database. To follow it, requests carry an identifier. `X-Request-Id: 7f3a9c12-4b1e-4c88-9a21-0d5e8b7a6c11` is a common convention: the client or gateway creates a unique value, every service logs it, and the response returns it. The standardised W3C Trace Context header is `traceparent: 00-4bf92f3577b34da6a3ce929d0e0e4736-00f067aa0ba902b7-01`, with four dash-separated fields: version, trace id, parent span id, and flags. Tracing tools use it to draw the whole journey of a request.

Why this matters to you: when you report a defect, include the request id from the response header. The developer can then find your exact request in the logs in seconds. A good test sends your own `X-Request-Id` and asserts the same value is echoed in the response, and checks that a missing one causes the server to generate a fresh one.

### 18. Hands-On with curl

`curl` is a command-line tool that sends HTTP requests. The flags relevant to headers are:

| Flag | Effect |
|------|--------|
| `-i` | Include response headers in the output, above the body |
| `-I` | Send a `HEAD` request, so you see only the response headers |
| `-H "Name: value"` | Add or override a request header; repeat it for several headers |
| `-v` | Verbose: print the request headers (lines starting with `>`) and response headers (lines starting with `<`), plus connection details |
| `--compressed` | Send `Accept-Encoding` and decompress the answer automatically |
| `-u user:pass` | Build a Basic `Authorization` header |
| `-b file` / `-c file` | Read cookies from a file / save cookies to a file |
| `-L` | Follow redirects |

**Example 1: see response headers.**

```bash
curl -i https://jsonplaceholder.typicode.com/posts/1
```

Expected output (values vary slightly):

```
HTTP/2 200
date: Sun, 11 Oct 2026 09:30:12 GMT
content-type: application/json; charset=utf-8
content-length: 292
cache-control: max-age=43200
etag: W/"124-yiKdLzqO5gfBrJFrcdJ8Yq0LGnU"
access-control-allow-origin: *

{
  "userId": 1,
  "id": 1,
  "title": "sunt aut facere ...",
  "body": "quia et suscipit ..."
}
```

The `-i` flag prints the status line and all response headers before the body. Notice the lowercase names, because HTTP/2 transmits them lowercase. We can read that the response is JSON in UTF-8, that it is fresh for 12 hours, that it has an `ETag` (the `W/` prefix marks a weak validator, meaning "semantically equivalent"), and that any origin may read it (`access-control-allow-origin: *`).

**Example 2: headers only.**

```bash
curl -I https://jsonplaceholder.typicode.com/posts/1
```

This sends `HEAD`, so you get the same status line and headers but no body. It is a fast way to inspect `Content-Type`, `Content-Length`, and cache headers without downloading data. Note that a few servers do not implement `HEAD` correctly and return `405` or different headers, so treat a `HEAD` result as a hint and confirm with `GET`.

**Example 3: custom headers on a POST.**

```bash
curl -i -X POST https://jsonplaceholder.typicode.com/posts \
  -H "Content-Type: application/json" \
  -H "Accept: application/json" \
  -d '{"title":"H","body":"B","userId":1}'
```

Expected output (abridged):

```
HTTP/2 201
content-type: application/json; charset=utf-8
location: https://jsonplaceholder.typicode.com/posts/101

{
  "title": "H",
  "body": "B",
  "userId": 1,
  "id": 101
}
```

`-X POST` sets the method, each `-H` adds one header, and `-d` supplies the body. The backslash at the end of a line continues the command on the next line. The response `201` with a `location` header confirms creation. (When you use `-d` without `-H "Content-Type..."`, `curl` quietly adds `application/x-www-form-urlencoded`, which is a classic reason for a JSON body being misread. Always declare `Content-Type` yourself.)

**Example 4: see exactly what was sent, with `-v`.**

```bash
curl -v https://jsonplaceholder.typicode.com/users/1 -H "Accept: application/json"
```

Expected output (abridged):

```
> GET /users/1 HTTP/2
> Host: jsonplaceholder.typicode.com
> User-Agent: curl/8.5.0
> Accept: application/json
>
< HTTP/2 200
< content-type: application/json; charset=utf-8
< cache-control: max-age=43200
```

Lines starting with `>` are what `curl` sent, and lines starting with `<` are what the server returned. This view reveals headers you did not type, such as `Host` and `User-Agent`, and is the best tool for answering "what did my client really send?"

**Example 5: Basic authentication and Bearer tokens.**

```bash
curl -i -u qa_tester:Spring2026! https://api.example.com/profile
curl -i https://api.example.com/profile -H "Authorization: Bearer my-test-token"
```

The first command makes `curl` build `Authorization: Basic cWFfdGVzdGVyOlNwcmluZzIwMjYh` from the credentials (the same string you decoded earlier). The second sends a Bearer header you wrote yourself. Both addresses and credentials here are placeholders, so the real server would not recognise them; use your course test API for real calls. In the shell, quote any password that contains `!` or `$` using single quotes so the shell does not interpret them.

**Example 6: compression.**

```bash
curl -i --compressed https://jsonplaceholder.typicode.com/posts
```

With `--compressed`, `curl` sends `Accept-Encoding: gzip, deflate, br` and decompresses the reply. In the headers you may see `content-encoding: gzip`, while the body appears as normal readable JSON.

**Example 7: cookies.**

```bash
curl -i -c cookies.txt -X POST https://api.example.com/login \
  -H "Content-Type: application/json" -d '{"user":"qa","pass":"x"}'
curl -i -b cookies.txt https://api.example.com/account
```

The first command saves any `Set-Cookie` values to `cookies.txt` (the "jar"). The second reads the jar and sends a `Cookie` header automatically, proving the session works. The domain is again a placeholder.

### 19. Hands-On with Postman

Follow these steps to practise every header idea in Postman.

**Step 1: create the request.** Click **New**, then **HTTP**. Set the method to `GET` and the URL to `https://jsonplaceholder.typicode.com/posts/1`. Click **Send**. You should receive `200 OK` and a JSON body.

**Step 2: read response headers.** In the lower response pane, click the **Headers** tab next to **Body**. A table lists every response header: `Content-Type`, `Cache-Control`, `ETag`, and so on. Hover over a header name, and Postman shows a short description.

**Step 3: add a request header.** In the upper request pane, click the **Headers** tab. Type `Accept` in the first empty Key cell (autocomplete suggests names) and `application/json` in the Value cell. A tick in the checkbox on the left means the header is enabled. Send again and compare.

**Step 4: see the auto-generated headers.** Click the **hidden** link (labelled "n hidden", or use the eye icon in newer versions) above the headers table. Postman shows headers it adds on its own: `User-Agent` (for example `PostmanRuntime/7.37.0`), `Accept: */*`, `Postman-Token` (a unique id), `Host`, `Accept-Encoding: gzip, deflate, br`, and `Connection: keep-alive`. For a `POST` with a raw JSON body you will also see `Content-Type: application/json` and `Content-Length`. Open the **Postman Console** (View, then Show Postman Console, or the Console button at the bottom) and send the request; the console shows the exact request headers that went over the wire, which is Postman's equivalent of `curl -v`.

**Step 5: override an automatic header.** If you add your own row with the same key as an auto-generated header (for example `User-Agent: MyCompany-QA/1.0`), yours replaces the automatic one. This is how you test agent-specific behaviour.

**Step 6: disable a header.** Create a `POST` request to `https://jsonplaceholder.typicode.com/posts`. On the **Body** tab choose **raw** and, in the dropdown at the right, choose **JSON**. Enter `{"title":"H","body":"B","userId":1}`. Postman automatically adds `Content-Type: application/json`. To test the missing-header case, open the **Headers** tab, show hidden headers, and untick the `Content-Type` row (or add your own `Content-Type` row and untick it, or change the body type to **Text** to see a `text/plain` header). Send and compare the response with the original. Note that a very forgiving test API such as this one may still accept the request, whereas a strict API returns `415`; record what you actually see.

**Step 7: use presets and the Authorization tab.** Postman used to offer header **presets** (saved groups of headers). The feature is still available in some versions under the Headers tab's **Presets** option, and you can also save a common header set as variables or in a collection (covered in the variables lesson). For authentication, open the **Authorization** tab, choose a **Type** from the dropdown, and Postman will build the header for you: **Basic Auth** shows Username and Password fields and produces `Authorization: Basic ...`; **Bearer Token** shows a Token field and produces `Authorization: Bearer ...`; **API Key** lets you choose the key name, value, and whether it is added to the header or to the query string. Open the hidden headers or the Console to confirm the final header, which is a good habit. You can also set the Authorization once on a collection, and requests inherit it by selecting **Inherit auth from parent**. Never type a real secret into a shared collection; the next lesson shows how to use variables instead.

**Step 8: inspect cookies.** Click **Cookies** (below the Send button) to open the cookie manager, which lists domains and the cookies saved from `Set-Cookie` headers, with their attributes.

### 20. Postman Test Scripts for Headers

Postman lets you write JavaScript in the **Tests** tab. It runs after the response arrives. Here are four common header tests:

```javascript
pm.test("Content-Type is JSON", function () {
    pm.response.to.have.header("Content-Type");
    pm.expect(pm.response.headers.get("Content-Type")).to.include("application/json");
});

pm.test("Location header present on creation", function () {
    pm.response.to.have.status(201);
    pm.response.to.have.header("Location");
});

pm.test("Sensitive data is not cached", function () {
    pm.expect(pm.response.headers.get("Cache-Control")).to.include("no-store");
});

pm.test("Server does not disclose a version", function () {
    pm.expect(pm.response.headers.has("X-Powered-By")).to.be.false;
    const server = pm.response.headers.get("Server") || "";
    pm.expect(server).to.not.match(/\d+\.\d+/);
});
```

Explanation line by line. `pm` is the Postman object that gives access to the request and response. `pm.test("name", function () {...})` defines one named test; Postman shows it as passed or failed, and the function holds the assertions. `pm.response.to.have.header("Content-Type")` asserts that a header with that name exists (the lookup ignores case). `pm.response.headers.get("Content-Type")` returns the header's value as a string, or `undefined` if it is absent. `pm.expect(value)` begins a Chai-style assertion, and `.to.include("application/json")` passes if the string contains that text; we use `include` rather than exact equality because the real value is often `application/json; charset=utf-8`. In the second test, `pm.response.to.have.status(201)` checks the status code, and then we confirm `Location` exists. In the third test, we require `no-store` inside the `Cache-Control` value. In the fourth test, `pm.response.headers.has("X-Powered-By")` returns true or false for existence, and `.to.be.false` asserts it is absent. `|| ""` supplies an empty string if `Server` is missing, so `.match` does not crash on `undefined`, and `.to.not.match(/\d+\.\d+/)` uses a regular expression that looks for a digit group, a dot, and another digit group, as in `2.4`, meaning a version number.

A fifth, more advanced test covers the tracing header:

```javascript
const sentId = pm.request.headers.get("X-Request-Id");
pm.test("Server echoes X-Request-Id", function () {
    pm.expect(pm.response.headers.get("X-Request-Id")).to.eql(sentId);
});

pm.test("Retry-After is a positive number on 429", function () {
    if (pm.response.code === 429) {
        const wait = Number(pm.response.headers.get("Retry-After"));
        pm.expect(wait).to.be.above(0);
    }
});
```

`pm.request.headers.get(...)` reads a header from the request you sent, here the id you set earlier, and we store it in a constant named `sentId`. `.to.eql(sentId)` performs an equality check between the echoed id and the sent one. In the second test, `pm.response.code` is the numeric status code, and the `if` makes the check apply only when the response is `429`, so the test passes silently on other responses. `Number(...)` converts the header text to a number, and `.to.be.above(0)` asserts it is greater than zero.

### 21. Header-Based Negative Test Tables

A negative test deliberately supplies bad input and verifies that the system fails safely. Header-based negative tests are cheap because you only change one header at a time.

**Content-Type and Accept**

| Test | How | Expected result |
|------|-----|-----------------|
| Missing `Content-Type` on `POST` with a JSON body | Disable the header | `400` or `415`, never `500` |
| Wrong `Content-Type` (`text/plain`) | Change the value | `415` |
| `Content-Type` says JSON but the body is broken | Send `{"a":` | `400` with a helpful message |
| Impossible `Accept` (`application/pdf`) | Change the value | `406` (or documented default) |
| `Accept` with `q=0` for the only format | `application/json;q=0` | `406` |
| Unsupported charset | `charset=utf-16` with UTF-8 bytes | `400` or `415` |

**Authorization**

| Test | How | Expected result |
|------|-----|-----------------|
| No `Authorization` on a protected endpoint | Disable the header | `401` plus `WWW-Authenticate` |
| Empty value | `Authorization:` | `401` |
| Wrong scheme | `Token abc` where Bearer is required | `401` |
| Bearer with no token | `Authorization: Bearer` | `401` |
| Corrupted token | Change one character | `401` |
| Expired token | Use an old token | `401` with an expiry hint |
| Valid token, low permission | Use a basic user on an admin endpoint | `403` |
| Valid token used on another user's data | Request another user's id | `403` or `404` |

**Size and structure**

| Test | How | Expected result |
|------|-----|-----------------|
| Very long header value | 10,000 characters | `431` or a clean `4xx` |
| Header with illegal characters | Control characters in the value | `400` |
| Wrong `Content-Length` | Use `curl -H "Content-Length: 5"` with a longer body | Truncated parse failure or `400` |
| Wrong `Host` | Override `Host` | `400` or `404`, not another tenant's data |

**Rate and conditional requests**

| Test | How | Expected result |
|------|-----|-----------------|
| Exceed the limit | Send repeated requests in the test instance | `429` plus `Retry-After` |
| Stale `If-None-Match` | Use an old `ETag` | `200` with new data |
| Matching `If-None-Match` | Use the current `ETag` | `304` with no body |

For each row you should check both the status and that the error response is clean: no stack trace, no software version, and a sensible `Content-Type`.

### 22. Diagnosing Real Failures from Headers

The best way to learn to read headers is to work through failures. For each case study, read the evidence first, then the diagnosis.

**Case study 1: 401 Unauthorized.**

Request and response:

```http
GET /v1/reports HTTP/1.1
Host: api.example.com
Accept: application/json

HTTP/1.1 401 Unauthorized
WWW-Authenticate: Bearer realm="reports"
Content-Type: application/json

{"error":"Missing credentials"}
```

Diagnosis: the request has no `Authorization` header at all. `401` means "unauthenticated," and `WWW-Authenticate: Bearer` says the server wants a bearer token. The fix is to add `Authorization: Bearer <token>`. If the header had been present and the challenge had included `error="invalid_token"`, the diagnosis would be a bad or expired token instead.

**Case study 2: 403 Forbidden.**

```http
DELETE /v1/users/7 HTTP/1.1
Host: api.example.com
Authorization: Bearer eyJhbGciOi...valid...

HTTP/1.1 403 Forbidden
Content-Type: application/json

{"error":"Insufficient permissions: admin role required"}
```

Diagnosis: the request carried credentials and the server accepted them (otherwise it would have said `401`), but the identified user lacks permission. There is no `WWW-Authenticate`, because sending the same credentials again would not help. The fix is to use an account with the right role, or, if the role was supposed to work, to report a defect in authorisation. The `401` versus `403` distinction is the one interviewers love: `401` is "who are you?" and `403` is "I know who you are, and no."

**Case study 3: 406 Not Acceptable.**

```http
GET /v1/users/1 HTTP/1.1
Host: api.example.com
Accept: application/xml

HTTP/1.1 406 Not Acceptable
Content-Type: application/json

{"error":"Supported types: application/json"}
```

Diagnosis: the client asked for XML only; the API only produces JSON. The error body even tells you the supported types, which is good API design. The fix is to send `Accept: application/json` (or `*/*`). A tester might also report the case where the API silently returns JSON despite asking for XML, if the contract promises `406`.

**Case study 4: 415 Unsupported Media Type.**

```http
POST /v1/users HTTP/1.1
Host: api.example.com
Content-Type: text/plain
Content-Length: 31

{"name":"Ana","email":"a@b.com"}

HTTP/1.1 415 Unsupported Media Type
Accept-Post: application/json
Content-Type: application/json

{"error":"Content-Type must be application/json"}
```

Diagnosis: the body is valid JSON, but the header declares `text/plain`, so the server refuses to parse it. The response's `Accept-Post` header even lists accepted types. The fix is to change the `Content-Type` header to `application/json`. In Postman this commonly happens when the body mode is Text, not JSON, or when a manually entered header overrides the automatic one. In `curl` it happens when `-d` is used without `-H`.

**Case study 5: 429 Too Many Requests.**

```http
GET /v1/search?q=notebook HTTP/1.1
Host: api.example.com

HTTP/1.1 429 Too Many Requests
Retry-After: 30
X-RateLimit-Limit: 100
X-RateLimit-Remaining: 0
Content-Type: application/json

{"error":"Rate limit exceeded"}
```

Diagnosis: the client sent more than 100 requests in the window. `Remaining: 0` confirms the budget is spent, and `Retry-After: 30` says to wait 30 seconds. The fix for a test suite is to slow down, wait the stated time, spread tests across more than one test account, or ask for a higher test limit. A test framework should never retry in a tight loop, because that makes the situation worse; it should honour `Retry-After`.

**Case study 6: 304 Not Modified that looks like a "broken" response.**

```http
GET /v1/products/42 HTTP/1.1
Host: api.example.com
If-None-Match: "v7-a91f"

HTTP/1.1 304 Not Modified
ETag: "v7-a91f"
Cache-Control: max-age=60
```

Diagnosis: the tester's script failed with "Unexpected end of JSON input," believing the API returned an empty body. In truth, the request carried `If-None-Match`, which was left over in a saved collection header, so the server correctly said "nothing changed" and sent no body. The fix is to remove the conditional header when you want the full resource, or to treat `304` as a valid outcome in the test. This case shows that a status in the `3xx` range can be correct behaviour, and the headers on the request explain it.

**Case study 7: a CORS error that "works in Postman."**

Browser console message:

```
Access to fetch at 'https://api.example.com/orders' from origin 'https://app.example.com'
has been blocked by CORS policy: Response to preflight request doesn't pass access control
check: No 'Access-Control-Allow-Origin' header is present on the requested resource.
```

The tester reproduces the preflight with `curl`:

```bash
curl -i -X OPTIONS https://api.example.com/orders \
  -H "Origin: https://app.example.com" \
  -H "Access-Control-Request-Method: POST" \
  -H "Access-Control-Request-Headers: content-type, authorization"
```

```
HTTP/2 404
content-type: application/json
```

Diagnosis: the API server does not handle `OPTIONS` for `/orders` and returns `404` without any `Access-Control-Allow-*` headers. The browser therefore refuses to send the real `POST`. The same `POST` works in Postman because Postman never enforces CORS or sends a preflight. The defect belongs to the API configuration (it needs to answer `OPTIONS` with the allow headers), not to the front-end code, and the evidence is the missing headers in the `curl` output. A later fix would return `204` with `Access-Control-Allow-Origin: https://app.example.com`, `Access-Control-Allow-Methods`, and `Access-Control-Allow-Headers`.

### 23. Handling Secrets in Headers Safely

Headers such as `Authorization`, `X-API-Key`, and `Cookie` carry secrets. Leaking one can let an attacker act as a real user or service, so build safe habits from your first day.

First, never commit a real token, password, or key to Git, and never paste one into a collection you share. Use variables for them, which you will learn in the next lesson, and keep the real values in a private local environment that you do not export. Second, never paste a full `Authorization` header into a bug report, chat message, or screenshot. Show `Authorization: Bearer ****` or keep only the last four characters. Be especially careful with `curl -v` output and Postman Console output, which print the whole header. Third, remember that `curl -u user:pass` places the password in your shell history and in the process list while the command runs, so use test-only credentials, or read the password from an environment variable. Fourth, use short-lived tokens and test-only accounts with the least permission necessary, so that a leak has limited impact. Fifth, if a real secret does leak, rotate it immediately, which means revoking it and issuing a new one, because deleting the chat message does not undo the exposure. Sixth, prefer headers to query strings for secrets, because URLs end up in logs and browser history. On Friday you will see how a CI/CD system stores secrets so they never appear in the repository or the printed logs.

### 24. Realistic Scenarios

**Scenario 1: the new endpoint returns HTML.** A teammate adds `/v2/orders`. Your Postman test for `Content-Type` fails because the value is `text/html`, although the status is `200`. You open the body and find a login page. A reverse proxy is redirecting unauthenticated calls to a web login. The header assertion exposed a defect that a status-only check would have passed. You report that the API gateway should return `401` JSON, not an HTML page.

**Scenario 2: the cached balance.** A banking test environment shows a customer an old balance after a transfer. You inspect the `GET /accounts/9` response: `Cache-Control: max-age=600` with no `no-store`. A shared proxy cached private financial data for ten minutes. You raise a high-severity defect and add a permanent test asserting `no-store` on every account endpoint.

**Scenario 3: the upload that will not parse.** Your colleague hand-typed `Content-Type: multipart/form-data` in Postman for a file upload and gets `400 Bad Request`. The generated header would have contained a `boundary` parameter. You explain that the body mode **form-data** should create the header automatically, they delete the manual header, and the upload works.

**Scenario 4: the load test that gets blocked.** A test suite sends 500 requests in a minute against a staging API and begins to receive `429`. Instead of increasing the delay at random, you read `Retry-After: 60` and `X-RateLimit-Limit: 100`, calculate that the suite needs to slow to under 100 per minute, and add a pause. You also notice that one test hits the limit more than others and move it to a separate account.

**Scenario 5: "It works for me in Postman."** A front-end developer cannot call the API from the browser. You confirm with `curl` that a request with `Origin: https://app.example.com` gets no `Access-Control-Allow-Origin` in the reply. The cause is that the staging API allows only the production origin. Adding the staging origin to the allow-list fixes it. You write a regression test that sends each approved `Origin` and asserts the matching header.

**Scenario 6: the expired token confusion.** After a weekend, every test returns `401`. The `WWW-Authenticate` header reads `Bearer error="invalid_token", error_description="expired"`. Instead of debugging the code, you refresh the token and the whole suite passes, and you add a token-expiry check to your setup steps.

### 25. Common Mistakes and Why They Happen

**Confusing `Accept` with `Content-Type`.** The words sound similar, and both mention formats. Remember that `Content-Type` labels what you are sending, and `Accept` states what you want to get. A `GET` normally has no body, so no `Content-Type`.

**Hand-typing a `Content-Type` that a tool generates.** For `multipart/form-data` the boundary is generated, so a typed header lacks it and the server cannot split the body. Let the tool add it.

**Forgetting `Content-Type` in `curl -d`.** `curl` defaults to the form type, so a JSON body is misread. Always add `-H "Content-Type: application/json"`.

**Checking an exact header string.** Values often contain extras such as `; charset=utf-8`. Use `include`, a regular expression, or a parsed value instead of exact equality, or your test breaks when the server adds a charset.

**Treating header names as case-sensitive.** HTTP/2 lowercases names. Use tool methods that ignore case.

**Typing the Bearer token with `Bearer` twice or with a missing space.** The scheme is followed by exactly one space and then the token. If an environment variable already includes the word `Bearer`, adding it again yields `Bearer Bearer abc`, which is rejected.

**Treating `401` and `403` as interchangeable.** They signal different problems (unauthenticated versus unauthorised) and need different fixes. Reporting the wrong one wastes the developer's time.

**Treating Base64 as security.** It is reversible by anyone. Never assume a Basic header is hidden.

**Treating `no-cache` as "do not store."** It means "revalidate before reuse." The directive that forbids storage is `no-store`.

**Parsing the body of a `304` or a `204`.** These responses have no body. A test that always calls the JSON parser fails. Check the status first.

**Sharing screenshots with visible tokens.** The Postman Console, `curl -v`, and the headers tab expose secrets. Redact before sharing.

**Believing CORS errors are server crashes.** The server often responded fine; the browser blocked the result. Reproduce with `Origin` and `OPTIONS` to see the real headers.

**Hammering rate-limited APIs.** Ignoring `Retry-After` and retrying instantly deepens the lockout. Honour the header.

### 26. Practice Exercises

Try each exercise yourself before reading the solution. Where output depends on the live service, your values will differ slightly, so compare the shape and meaning, not the exact characters.

**Exercise 1: read response headers.** Run `curl -i https://jsonplaceholder.typicode.com/users/1`. List five response headers and say what each means.

*Solution.* A typical result contains: `content-type: application/json; charset=utf-8` (the body is JSON encoded in UTF-8); `content-length` or `transfer-encoding` (how the body size is communicated, the first for a known size, the second for chunked streaming); `cache-control: max-age=43200` (clients may reuse the response for 12 hours without asking); `etag: W/"..."` (a version identifier used for conditional requests, weak because of the `W/`); `access-control-allow-origin: *` (any browser origin may read the response); and `date` (when the server produced it). You may also see `server` or a CDN header; the exact set varies. The skill being practised is to give each header a purpose, not to memorise the values.

**Exercise 2: content negotiation.** Run `curl -i -H "Accept: application/xml" https://jsonplaceholder.typicode.com/users/1`. Does the API honour the request? How do you know?

*Solution.* Look at the response `content-type`. JSONPlaceholder ignores `Accept` and replies `200` with `content-type: application/json`, and the body is JSON, so it does not honour the request. The evidence is the response header, not the status code alone. Under a strict reading, the API could have returned `406`, but ignoring `Accept` is allowed by the specification. The right test note is "API ignores Accept; no 406 behaviour exists," not "defect," unless the project contract says otherwise.

**Exercise 3: missing Content-Type in Postman.** In Postman, `POST` to `https://jsonplaceholder.typicode.com/posts` with a raw JSON body, then disable the `Content-Type` header. Compare the responses.

*Solution.* Step 1: set Body to raw JSON with `{"title":"H","body":"B","userId":1}` and send. The hidden headers show `Content-Type: application/json`; the response is `201` with an `id`. Step 2: change the body type to Text (so the header becomes `text/plain`) or override the header with your own row and untick the checkbox, then send again. JSONPlaceholder is forgiving and still returns `201`, but its echoed body may lack the fields you sent (only the `id` appears, because the body was not parsed as JSON). A strict API would return `415`. The lesson: the header changes how the server interprets the body, and the response shows whether the parse succeeded. Record the observed behaviour in your notes.

**Exercise 4: write a header assertion.** Write a Postman test asserting that the response `Content-Type` includes `application/json`.

*Solution.*

```javascript
pm.test("Content-Type includes application/json", function () {
    pm.response.to.have.header("Content-Type");
    pm.expect(pm.response.headers.get("Content-Type")).to.include("application/json");
});
```

The first assertion proves the header exists, so a missing header gives a clear failure message ("expected response to have header Content-Type") instead of a confusing error on `undefined`. The second reads the value and checks that the string contains the media type. We use `include` because the value may carry `; charset=utf-8`.

**Exercise 5: explain Accept versus Content-Type.** In your own words, explain the difference, with one example request.

*Solution.* `Content-Type` is a label on the body being sent: "the bytes I am giving you are JSON." `Accept` is a wish about the reply: "please answer me in JSON." In `POST /posts` with `Content-Type: application/json` and `Accept: application/json`, the client says it is sending JSON and wants JSON back. In a `GET` request there is no body, so only `Accept` is meaningful. The server's response then carries its own `Content-Type`, which is the server's answer to the negotiation.

**Exercise 6: decode a Basic header.** A log shows `Authorization: Basic dGVzdDp0ZXN0MTIz`. Decode it, state the username and password, and explain whether the log is a security problem.

*Solution.* Run `echo 'dGVzdDp0ZXN0MTIz' | base64 -d`, which prints `test:test123`. Splitting at the first colon gives username `test` and password `test123`. Yes, it is a security problem, because Base64 is reversible without a key, so anyone with the log has the credentials. The fix is to mask the `Authorization` header in logs and to rotate the password if it was real. If you decode by hand, the first four characters `dGVz` give values 29, 6, 21, 51, which are bits `011101 000110 010101 110011` and regroup into bytes `01110100 01100101 01110011`, the letters `t`, `e`, `s`.

**Exercise 7: build and decode a Basic header.** Create the header for user `admin` and password `p@ss:word`, and explain why the colon in the password is not a problem.

*Solution.* Run `printf 'admin:p@ss:word' | base64`, which gives `YWRtaW46cEBzczp3b3Jk`. The header is `Authorization: Basic YWRtaW46cEBzczp3b3Jk`. A decoder splits at the first colon only, so the username is `admin` and everything after it, `p@ss:word`, is the password. The rule that usernames may not contain colons, while passwords may, is part of the Basic specification. We used `printf` rather than `echo` to avoid a trailing newline in the encoded text.

**Exercise 8: the 304 flow.** Using `curl -i https://jsonplaceholder.typicode.com/posts/1`, copy the `etag` value, and then send a conditional request. What do you expect, and what do you do if the API never returns 304?

*Solution.* Run `curl -i https://jsonplaceholder.typicode.com/posts/1 -H 'If-None-Match: W/"124-yiKdLzqO5gfBrJFrcdJ8Yq0LGnU"'`, substituting the real value you saw. If the resource has not changed and the server supports validation, the status is `304 Not Modified` with no body. Some servers or CDNs vary or do not honour the validator, in which case you receive `200` with a full body, and you note that revalidation is not supported. If you want to prove the logic of a changing resource, change one character in the tag; the server then returns a full `200`, since your tag no longer matches.

**Exercise 9: write a negative-test table.** For `GET /v1/orders` that requires a Bearer token and returns JSON, write six header-based negative tests with expected results.

*Solution.* (1) No `Authorization`: `401` with `WWW-Authenticate: Bearer`. (2) `Authorization: Bearer` with no token: `401`. (3) `Authorization: Basic abc` where Bearer is required: `401`. (4) Valid token with one character altered: `401` (invalid signature). (5) Valid token for a user without the orders permission: `403`. (6) `Accept: application/pdf` with a valid token: `406` or documented JSON fallback. For each, also assert the response `Content-Type` is JSON, there is no stack trace in the body, and no `X-Powered-By` header.

**Exercise 10: diagnose from headers.** You send `POST /v1/users` with a JSON body from curl: `curl -i -X POST https://api.example.com/v1/users -d '{"name":"Ana"}'` and receive `415`. Explain the cause and the fix.

*Solution.* Because `-d` was used with no `-H`, `curl` sent `Content-Type: application/x-www-form-urlencoded`, which the API does not accept for this endpoint. Run the command again with `-v` to verify this: you will see the `>` line `Content-Type: application/x-www-form-urlencoded`. The fix is to add `-H "Content-Type: application/json"`. Add a Postman assertion on the status and keep the header in your saved request.

**Exercise 11: CORS check without a browser.** Write a `curl` command that tests whether `https://api.example.com/orders` permits the origin `https://evil.example` to read it, and say what result is a defect.

*Solution.* `curl -i https://api.example.com/orders -H "Origin: https://evil.example" -H "Authorization: Bearer <test-token>"`. Read the response headers. If the API returns `Access-Control-Allow-Origin: https://evil.example` (reflecting an arbitrary origin) or `*` on an endpoint that uses credentials, that is a security defect. A correct API either omits the header for unknown origins or returns only its approved origins. For a preflight check, use `-X OPTIONS` with `Access-Control-Request-Method` as in case study 7.

**Exercise 12: write a security-header test.** Write a Postman test that fails when `X-Content-Type-Options` is not `nosniff` and when `Server` reveals a version.

*Solution.*

```javascript
pm.test("X-Content-Type-Options is nosniff", function () {
    pm.expect(pm.response.headers.get("X-Content-Type-Options")).to.eql("nosniff");
});

pm.test("Server header has no version number", function () {
    const server = pm.response.headers.get("Server") || "";
    pm.expect(server).to.not.match(/\d/);
});
```

The first test reads the value and requires exactly `nosniff`. If the header is missing, `get` returns `undefined`, so the equality fails and the report shows the problem. The second test falls back to an empty string when `Server` is absent (which passes, since nothing is disclosed) and fails if any digit appears in the value, which would usually indicate a version.

### 27. Self-Check Quiz

1. What separates the headers from the body in an HTTP message?
2. Is `content-type` the same header as `Content-Type`?
3. Which header says what format the client wants back?
4. A server returns `application/problem+json`. Does a check for exactly `application/json` pass?
5. What does `Accept: application/json, application/xml;q=0.5` express?
6. What status should an API return if no acceptable format exists?
7. Why is Base64 in a Basic header not secure?
8. Which status code means "we do not know who you are," and which means "we know, but you are not allowed"?
9. What does `no-cache` actually mean?
10. What does a `304` response contain, and what must the request have contained to get it?
11. Name two cookie attributes that protect a session cookie, and what each does.
12. Why can an API work in Postman and fail in a browser?
13. Which header tells a client how long to wait after a `429`?
14. What is `traceparent` used for?
15. Why should you not hand-type `Content-Type: multipart/form-data`?

**Answers.**

1. A blank line separates them: the headers end, and the body begins after it.
2. Yes. Header names are case-insensitive, and HTTP/2 transmits them in lowercase.
3. `Accept`.
4. No. A strict equality check fails, though the content is JSON. Use `include("json")` or a pattern if any JSON type is acceptable.
5. "I prefer JSON (q defaults to 1), and XML is acceptable at a lower preference of 0.5."
6. `406 Not Acceptable` (although some APIs ignore `Accept` and return their default type).
7. Base64 is an encoding with no key. Anyone can decode it, so the header must only travel over HTTPS and must be masked in logs.
8. `401` means unauthenticated ("who are you?"), and `403` means authenticated but forbidden.
9. It means a cache may store the response but must check with the server before each reuse. `no-store` is the directive that forbids storing.
10. A `304` has headers (such as `ETag`) but no body. The request had to include a validator such as `If-None-Match` or `If-Modified-Since` that matched the current version.
11. `HttpOnly` prevents JavaScript from reading the cookie, which limits theft through XSS; `Secure` sends it only over HTTPS. (`SameSite` is also correct: it limits cross-site sending and helps against CSRF.)
12. Browsers enforce CORS, and Postman does not. The server may be missing `Access-Control-Allow-*` headers that the browser requires.
13. `Retry-After`.
14. It carries a W3C trace id and span id so that one request can be followed through many services and logs.
15. The header needs a `boundary` parameter that matches the generated body. The tool creates both, and a handwritten header lacks the boundary, so the server cannot split the parts.

### 28. Glossary

**Header**: a `Name: value` line of metadata in an HTTP message.

**Request header**: a header sent by the client that describes the request or client.

**Response header**: a header sent by the server that describes the response or server.

**Representation header**: a header that describes the body, such as `Content-Type`.

**Media type (MIME type)**: a `type/subtype` label for a data format, such as `application/json`.

**Charset**: the character encoding that turns text into bytes, such as UTF-8.

**Boundary**: the delimiter string that separates the parts of a multipart body.

**Content negotiation**: the process in which client and server choose a representation using headers such as `Accept`.

**Q-value**: a preference weight from 0 to 1 in headers like `Accept`.

**Base64**: a reversible encoding that represents bytes using 64 printable characters; it is not encryption.

**Bearer token**: a credential that grants access to whoever presents it.

**JWT**: JSON Web Token, a bearer token made of a header, payload, and signature.

**Challenge**: the `WWW-Authenticate` response telling the client how to authenticate.

**Cache**: a stored copy of a response reused to save time and bandwidth.

**Validator**: an `ETag` or `Last-Modified` value used to check whether a cached copy is still current.

**Conditional request**: a request containing a header such as `If-None-Match` that makes the answer depend on the validator.

**Cookie**: a small piece of data stored by the client and returned on later requests.

**Preflight**: an automatic `OPTIONS` request that a browser sends to ask whether a cross-origin request is allowed.

**Origin**: the combination of scheme, host, and port.

**CORS**: Cross-Origin Resource Sharing, the header-based system that lets servers permit cross-origin reads.

**HSTS**: HTTP Strict Transport Security, which forces HTTPS for a host.

**Information disclosure**: unintended revealing of internal details, such as software versions.

**Trace id**: an identifier that ties together all work done for one request across systems.

---

## Summary

- A header is a `Name: value` line of metadata. Names are case-insensitive, values may be lists with parameters, and custom headers once used `X-`, a convention that is now discouraged but still common.
- Headers belong to families: request, response, representation, and general. Knowing who sends a header and what it describes speeds up debugging.
- `Content-Type` labels the body (with charset and, for multipart, a boundary), and `Accept` states what the client wants back. Together with `Accept-Language` and `Accept-Encoding` they form content negotiation, and a failed negotiation is `406`, while a wrongly labelled body is `415`.
- `Authorization` carries credentials as Basic (Base64 of `user:password`, trivially decoded), Bearer tokens, or custom API key headers, and `WWW-Authenticate` is the server's challenge on a `401`.
- `User-Agent`, `Host`, `Origin`, and `Referer` identify the client and target, and `Content-Length` and `Transfer-Encoding` describe the size and delivery of the body.
- Caching uses `Cache-Control`, `ETag`, `Last-Modified`, and `If-None-Match`, producing a bodyless `304` when nothing changed.
- `Location`, `Set-Cookie`/`Cookie`, `Retry-After`, and `Allow` carry the navigation, session, rate-limit, and method information that clients need.
- CORS headers are enforced by browsers and explain why an API can work in Postman yet fail on a web page. Security headers and the absence of `Server` and `X-Powered-By` version leaks are cheap, valuable checks. `X-Request-Id` and `traceparent` make defects traceable.
- In `curl`, use `-i`, `-I`, `-H`, `-v`, `--compressed`, `-u`, and `-b`/`-c`. In Postman, use the Headers tab, hidden headers, the Console, and the Authorization tab. Write Postman tests with `pm.response.headers.get`, `.has`, and `to.have.header`.
- Treat credential headers as secrets: do not commit, screenshot, or log them, prefer test-only short-lived credentials, and rotate leaks.

## Additional Resources

- MDN Web Docs, *HTTP headers*: https://developer.mozilla.org/en-US/docs/Web/HTTP/Headers
- MDN Web Docs, *HTTP authentication*: https://developer.mozilla.org/en-US/docs/Web/HTTP/Authentication
- MDN Web Docs, *HTTP caching*: https://developer.mozilla.org/en-US/docs/Web/HTTP/Caching
- MDN Web Docs, *Cross-Origin Resource Sharing (CORS)*: https://developer.mozilla.org/en-US/docs/Web/HTTP/CORS
- RFC 9110, *HTTP Semantics*: https://www.rfc-editor.org/rfc/rfc9110
- Postman Docs, *Send API requests* (headers and authorization): https://learning.postman.com/docs/sending-requests/create-requests/request-basics/
- curl documentation, *Everything curl*: https://everything.curl.dev/
