# Handout 01 – HTTP & REST Foundations (curl)


> **How to use this handout:** each topic is a small, self-contained example. Start each one fresh, and don't reuse anything from another topic. You will combine everything in **Handout 11 (Week 7 Mini-Project)**.

**Before class**

- A terminal (on Windows use **Git Bash**, or PowerShell with `curl.exe`).
- Python 3 installed (we use `python -m json.tool` to pretty-print JSON).
- Practice API: `https://jsonplaceholder.typicode.com` (free and needs no login; it **fakes** writes).

**Installing curl and HTTPie (one time)**

| Tool | Windows | macOS | Linux | Check it works |
|------|---------|-------|-------|----------------|
| **curl** | Already installed on Windows 10/11 (type `curl.exe` in PowerShell). Git Bash also includes it. | Already installed | Usually installed; otherwise `sudo apt install curl` | `curl --version` |
| **HTTPie** | `pip install httpie` | `brew install httpie` or `pip install httpie` | `sudo apt install httpie` or `pip install httpie` | `http --version` |

If Windows says `http` is not recognized after installing, Python's Scripts folder is not on your PATH. Run `python -m httpie` instead of `http`.

> **HTTPie in 30 seconds:** `http URL` prints the status, headers and body. Add `-b` for the body only and `-v` to see the request too. `name=value` adds a JSON string field, `name:=1` adds a JSON number or boolean, `name==value` adds a query parameter, and `Name:value` adds a header. Always type the full `https://` URL, because HTTPie uses `http://` when you leave the scheme out.

> All commands use bash syntax. In PowerShell, `curl` is an alias for a different command, so type `curl.exe`. Every curl example has an HTTPie version below it, so you can try both.

---

## Topic 1 – HTTP Messages

### Definition

HTTP (HyperText Transfer Protocol) is the set of rules a **client** and a **server** follow to talk to each other. Every conversation is one **request** sent by the client followed by one **response** sent back by the server. Both are plain-text **messages** with a fixed layout: a first line, some headers, a blank line, and an optional body. HTTPS is the same messages sent through an encrypted TLS connection. As a tester, reading these messages is how you find out what really happened.

### Key ideas

| Request | Response |
|---------|----------|
| **Request line:** `GET /posts/1 HTTP/1.1` (method, path, version) | **Status line:** `HTTP/1.1 200 OK` (version, code, reason) |
| **Headers:** `Host`, `Accept`, `Content-Type`... | **Headers:** `Content-Type`, `Content-Length`, `Cache-Control`... |
| Blank line | Blank line |
| **Body** (optional, e.g. JSON for POST) | **Body** (e.g. the JSON you asked for) |

- **Status code families:** `1xx` info · `2xx` success · `3xx` redirect · `4xx` client error (your request is wrong) · `5xx` server error (the server broke).
- **URL anatomy:** `https://jsonplaceholder.typicode.com:443/posts?userId=1#top` has scheme `https`, host, port `443`, path `/posts`, query `userId=1`, and fragment `#top`. The fragment is never sent to the server.
- **Stateless:** the server remembers nothing between requests, so every request must carry everything it needs (for example a token in a header).

### Worked example – Reading a real exchange with curl

**Step 1 – Ask for one post and see only the body.**

```bash
curl https://jsonplaceholder.typicode.com/posts/1
```

*HTTPie version:*

```bash
http -b https://jsonplaceholder.typicode.com/posts/1
```

**Step 2 – Add `-i` to include the status line and response headers.**

```bash
curl -i https://jsonplaceholder.typicode.com/posts/1
```

*HTTPie version:*

```bash
http https://jsonplaceholder.typicode.com/posts/1
```

HTTPie shows the status line and headers by default, so no flag is needed.

**Step 3 – Switch to `-v` (verbose) to see the request too.** Lines starting with `>` were sent by you and lines starting with `<` came back from the server.

```bash
curl -v https://jsonplaceholder.typicode.com/posts/1
```

*HTTPie version:*

```bash
http -v https://jsonplaceholder.typicode.com/posts/1
```

HTTPie prints the request first and then the response, without the `>` and `<` markers.

**Step 4 – Ask for something that does not exist and compare.**

```bash
curl -i https://jsonplaceholder.typicode.com/posts/9999
```

*HTTPie version:*

```bash
http https://jsonplaceholder.typicode.com/posts/9999
```

### Checkpoint

Step 3 should show something like this (some headers are trimmed):

```
> GET /posts/1 HTTP/2
> Host: jsonplaceholder.typicode.com
> User-Agent: curl/8.x
> Accept: */*
>
< HTTP/2 200
< content-type: application/json; charset=utf-8
...
{
  "userId": 1,
  "id": 1,
  "title": "sunt aut facere repellat provident occaecati ...",
  "body": "quia et suscipit ..."
}
```

Step 4 should return `HTTP/2 404` and an empty body `{}`.

With HTTPie, the output is coloured, the request line reads `GET /posts/1 HTTP/1.1`, `User-Agent` is `HTTPie/3.x`, and the responses start with `HTTP/1.1 200 OK` and `HTTP/1.1 404 Not Found`. HTTPie speaks HTTP/1.1, but the message parts are the same.

### Your turn

1. Request `/users/1` with `-i`. What is the exact value of the `Content-Type` header?
2. Run `curl -I https://jsonplaceholder.typicode.com/posts/1` (capital I), or `http HEAD https://jsonplaceholder.typicode.com/posts/1` in HTTPie. What is missing from the output compared with `-i`, and why?
3. Break this URL into scheme, host, path, query and fragment: `https://api.example.com/v1/orders?status=open&page=2#summary`. Which part does the server never receive?
4. Run `curl -i https://httpbin.org/status/503` (HTTPie: `http https://httpbin.org/status/503`). Which status family is this, and is the problem on the client side or the server side?

### Common errors

- **PowerShell prints odd objects instead of headers.** You ran the PowerShell alias. Use `curl.exe` or Git Bash.
- **A URL with `&` breaks the command.** Wrap the URL in quotes: `curl "https://...?a=1&b=2"`.
- **Mixing up `-i` and `-I`.** Lowercase `-i` means include headers. Uppercase `-I` sends a HEAD request, which returns headers only.
- **HTTPie: `http jsonplaceholder.typicode.com/...` without `https://`.** HTTPie then uses plain `http://`. Always type the full `https://` URL.

---

## Topic 2 – REST API Fundamentals

### Definition

An **API** (Application Programming Interface) is a contract that lets one program ask another program for data or actions. A **web API** does this over HTTP. **REST** (Representational State Transfer) is an architectural style, not a protocol, described by Roy Fielding. In REST everything is a **resource** with its own URL, and you act on it with standard HTTP methods. Most REST APIs send and receive **JSON**.

### Key ideas

| Term | Example | Meaning |
|------|---------|---------|
| Base URL | `https://jsonplaceholder.typicode.com` | Where the API lives |
| Collection | `/users` | A list of resources |
| Resource | `/users/1` | One item, identified by its id |
| Sub-resource | `/users/1/posts` | Items that belong to a resource |

- **CRUD maps to methods:** Create = POST · Read = GET · Update = PUT/PATCH · Delete = DELETE.
- **Good URLs use nouns, not verbs:** `/users/5` is good, while `/getUser?id=5` and `/users/delete/5` are poor designs, because the method should say what the action is.
- **JSON types:** string `"Ana"`, number `42`, boolean `true`, `null`, object `{...}`, array `[...]`. Keys must use double quotes.
- **Six REST constraints (awareness level):** client-server, stateless, cacheable, uniform interface, layered system, code-on-demand (optional).

### Worked example – Exploring a REST API

**Step 1 – Read the collection.** Pipe the output into Python to make it readable.

```bash
curl -s https://jsonplaceholder.typicode.com/users | python -m json.tool | head -20
```

*HTTPie version:*

```bash
http -b --pretty=format https://jsonplaceholder.typicode.com/users | head -20
```

When its output is piped, HTTPie prints plain JSON. `--pretty=format` keeps it indented.

**Step 2 – Read one resource by id.**

```bash
curl -s https://jsonplaceholder.typicode.com/users/1 | python -m json.tool
```

*HTTPie version:*

```bash
http -b https://jsonplaceholder.typicode.com/users/1
```

**Step 3 – Navigate the nested JSON.** Find `address` → `geo` → `lat` in the output. This is an object inside an object inside an object.

**Step 4 – Follow a sub-resource and count the results.**

```bash
curl -s https://jsonplaceholder.typicode.com/users/1/posts \
  | python -c "import sys, json; print(len(json.load(sys.stdin)))"
```

*HTTPie version:*

```bash
http -b https://jsonplaceholder.typicode.com/users/1/posts \
  | python -c "import sys, json; print(len(json.load(sys.stdin)))"
```

### Checkpoint

- Step 1 shows a JSON **array** that starts with `[` and contains 10 users.
- Step 2 shows a single **object** that starts with `{` and includes `"name": "Leanne Graham"`.
- Step 4 prints `10`.

### Your turn

1. For each URL, name the base URL, the resource type, and the id (if there is one): `/posts`, `/posts/7`, `/posts/7/comments`, `/albums/3/photos`.
2. Rewrite these poor URLs as RESTful ones (method plus path): `/getAllOrders`, `/createOrder`, `/orders/delete?id=9`.
3. Write a valid JSON object for a new user with `name`, `email`, `active` (boolean) and a nested `address` that has `city` and `zip`.
4. Find the three errors in this JSON: `{'name': "Ana", "age": 30, "tags": ["qa", "api",], }`

### Common errors

- **Single quotes in JSON.** JSON only allows double quotes, so `'name'` is invalid.
- **Trailing commas.** `["a", "b",]` is invalid JSON, even though Python and JavaScript accept it.
- **Treating REST as a protocol.** HTTP is the protocol. REST is the style that tells you how to design the URLs and how to use the methods.

---

## Topic 3 – GET, POST, PUT and DELETE

### Definition

An **HTTP method** (also called a verb) tells the server what you want to do with a resource. `GET` reads, `POST` creates, `PUT` replaces, `PATCH` partially updates, and `DELETE` removes. A method is **safe** if it does not change data, and **idempotent** if sending it once or ten times leaves the server in the same state. These properties tell a tester what is safe to retry and what a defect looks like.

### Key ideas

| Method | Purpose | Body? | Typical success | Safe | Idempotent |
|--------|---------|-------|-----------------|:----:|:----------:|
| GET | Read | No | 200 OK | ✅ | ✅ |
| POST | Create | Yes | 201 Created | ❌ | ❌ |
| PUT | Replace whole resource | Yes | 200 OK / 204 | ❌ | ✅ |
| PATCH | Change some fields | Yes | 200 OK | ❌ | ❌ (usually) |
| DELETE | Remove | No | 200 / 204 | ❌ | ✅ |

- `405 Method Not Allowed` means the URL exists but does not support that method.
- When you send a JSON body, also send `Content-Type: application/json` so the server knows how to read it.

### Worked example – A full CRUD lifecycle

**Step 1 – Read (GET).**

```bash
curl -i https://jsonplaceholder.typicode.com/posts/1
```

*HTTPie version:*

```bash
http https://jsonplaceholder.typicode.com/posts/1
```

**Step 2 – Create (POST).** Add the method, a content-type header and a JSON body.

```bash
curl -i -X POST https://jsonplaceholder.typicode.com/posts \
  -H "Content-Type: application/json" \
  -d '{"title": "QE week 7", "body": "hello", "userId": 1}'
```

*HTTPie version:*

```bash
http POST https://jsonplaceholder.typicode.com/posts title="QE week 7" body=hello userId:=1
```

HTTPie sends the fields as JSON and sets `Content-Type: application/json` for you. `userId:=1` sends `1` as a number, not the string `"1"`.

**Step 3 – Replace (PUT).** Send the whole object, including `id`.

```bash
curl -i -X PUT https://jsonplaceholder.typicode.com/posts/1 \
  -H "Content-Type: application/json" \
  -d '{"id": 1, "title": "replaced", "body": "new body", "userId": 1}'
```

*HTTPie version:*

```bash
http PUT https://jsonplaceholder.typicode.com/posts/1 id:=1 title=replaced body="new body" userId:=1
```

**Step 4 – Partial update (PATCH).** Send only the field that changes.

```bash
curl -i -X PATCH https://jsonplaceholder.typicode.com/posts/1 \
  -H "Content-Type: application/json" \
  -d '{"title": "patched only"}'
```

*HTTPie version:*

```bash
http PATCH https://jsonplaceholder.typicode.com/posts/1 title="patched only"
```

**Step 5 – Delete.**

```bash
curl -i -X DELETE https://jsonplaceholder.typicode.com/posts/1
```

*HTTPie version:*

```bash
http DELETE https://jsonplaceholder.typicode.com/posts/1
```

### Checkpoint

| Step | Status | Body shows |
|------|--------|-----------|
| 1 | `200` | the original post |
| 2 | `201` | your fields plus `"id": 101` |
| 3 | `200` | `"title": "replaced"` |
| 4 | `200` | the original `body` with `"title": "patched only"` |
| 5 | `200` | `{}` |

> ⚠️ JSONPlaceholder **fakes** writes. Running `GET /posts/101` afterwards returns `404`, because nothing was really saved. A real API would return your new post.

### Your turn

1. Without running anything, predict which of these are idempotent: `GET /posts/1`, `POST /posts`, `DELETE /posts/1`, `PUT /posts/1`. Then explain why calling `POST` twice is risky.
2. Repeat Step 2 **without** the `-H "Content-Type..."` line (in HTTPie, add `--form` and write `userId=1` instead of `userId:=1`). What changes in the response body?
3. Send `DELETE /posts/1` twice. What status does a real API normally return on the second call, and what does JSONPlaceholder return?
4. Write three negative test ideas for `POST /posts` (for example, a missing field).

### Common errors

- **Using `-d` without `-X`.** curl switches to POST automatically when you add `-d`. Write `-X POST` anyway so the command is clear.
- **Using PUT with only some fields.** PUT replaces the whole resource, so missing fields may be wiped. Use PATCH for partial changes.
- **JSON quoting in PowerShell.** Inner double quotes must be escaped. Git Bash with single quotes around the JSON is easier.

---

## Answers

<details>
<summary><strong>Topic 1 – HTTP Messages</strong></summary>

1. `application/json; charset=utf-8`.
2. `-I` sends a **HEAD** request, so there is no body. HEAD asks for the same headers a GET would return, but without the body.
3. Scheme `https`, host `api.example.com`, path `/v1/orders`, query `status=open&page=2`, fragment `summary`. The **fragment** is never sent to the server.
4. `503 Service Unavailable` is in the **5xx** family, so the problem is on the server side.

</details>

<details>
<summary><strong>Topic 2 – REST API Fundamentals</strong></summary>

1. All use base URL `https://jsonplaceholder.typicode.com`. `/posts` is the posts collection (no id). `/posts/7` is post id 7. `/posts/7/comments` is the comments sub-resource of post 7. `/albums/3/photos` is the photos sub-resource of album 3.
2. `GET /orders`, `POST /orders`, `DELETE /orders/9`.
3. Example:
   ```json
   {
     "name": "Ana Silva",
     "email": "ana@example.com",
     "active": true,
     "address": { "city": "Reston", "zip": "20190" }
   }
   ```
4. (a) `'name'` uses single quotes, (b) there is a trailing comma after `"api"`, (c) there is a trailing comma before `}`.

</details>

<details>
<summary><strong>Topic 3 – GET, POST, PUT and DELETE</strong></summary>

1. Idempotent: GET, DELETE, PUT. Not idempotent: POST. Each POST can create a new resource, so a retried POST can create duplicates, such as two orders.
2. curl sends the body as `application/x-www-form-urlencoded`, so the server does not parse your JSON fields as intended. The echoed body does not contain your `title`, `body` and `userId` as separate fields. HTTPie with `--form` also sends form data, but encodes it properly as `title=QE+week+7&body=hello&userId=1`. The server reads those as fields, but `userId` comes back as the string `"1"` instead of the number `1`, because form data has no types.
3. A real API usually returns `404 Not Found` the second time (some return `204`). Either way the server state is the same, which is why DELETE is still idempotent. JSONPlaceholder fakes the delete, so it returns `200` with `{}` both times.
4. Examples: missing `title` → expect `400`. `userId` as a string `"abc"` → expect `400`/`422`. An empty body → expect `400`. A body that is not JSON → expect `400`/`415`.

</details>
