# GET, POST, PUT and DELETE

## Learning Objectives

By the end of this lesson you will be able to:

- Explain, in your own words, what an HTTP method is and why a request needs one.
- Describe the purpose, wire format, parameters, body rules, and success and failure status codes of `GET`, `POST`, `PUT`, and `DELETE`.
- Define **safe**, **idempotent**, and **cacheable**, classify every method, and prove the classification with a small experiment.
- Explain the difference between `PUT` (replace) and `PATCH` (partial update) and predict what each does to a resource.
- Recognise `HEAD` and `OPTIONS`, explain `405 Method Not Allowed` and the `Allow` header, and describe method override tricks, idempotency keys, and conditional requests (`ETag` and `If-Match`) at an awareness level.
- Send every method with `curl`, read the raw request and raw response, and predict the output before you run the command.
- Design positive, negative, boundary, and security-minded test cases for each method, and recognise what a defect in each method looks like.
- Run and explain a complete CRUD lifecycle test, and map each request to the Postman interface you will use later today.

---

## Why This Matters

This week's epic is to build a pipeline-ready Test Automation Framework (Project 2) that tests an API, then tests accessibility, then runs everything automatically in CI/CD. Every one of those steps starts with the skill you are learning right now: sending the right kind of request to an API and knowing exactly what a correct answer looks like.

If REST is the grammar of an API, HTTP methods are the **verbs**. A sentence such as "the client *deletes* order 42" needs a verb, and HTTP gives you a small, fixed vocabulary of them. Each verb makes a **promise** about what it will and will not do. `GET` promises it will never change data. `PUT` promises that sending it twice is the same as sending it once. `DELETE` promises that the resource is gone afterwards. As a tester, your job is largely to check whether those promises hold. A defect in this area is rarely a cosmetic glitch. It is a customer charged twice because a `POST` was retried, a database wiped because a search-engine crawler followed a `GET /deleteUser?id=7` link, or an account taken over because a `PUT` accepted a field it should have ignored.

Later today you will build a Postman collection for the Project 2 API. Every request in that collection will use one of the methods in this lesson, and every assertion you write will check a status code, a body, or a follow-up state that this lesson teaches you to expect. Tomorrow you will automate the same requests with Python. The thinking you practise today, "what should this verb do, and how do I prove it did?", is the foundation for all of it.

You already met the general shape of an HTTP request and response in the *HTTP messages* lesson, and you saw the REST ideas of resources and URLs in the *REST API fundamentals* lesson. This lesson takes the **method** part of the request line, which you only glimpsed there, and studies it in depth.

---

## The Concept

### 1. What Is an HTTP Method and Why Does It Exist?

Every HTTP request begins with a **request line** made of three parts: the method, the target, and the protocol version.

```http
GET /posts/1 HTTP/1.1
```

**Plain-language explanation:** The word `GET` is the method. `/posts/1` is the target, meaning which resource the request is about. `HTTP/1.1` is the protocol version. Together the line says, "Please *get* me the resource at `/posts/1`, and let us speak HTTP version 1.1."

The method tells the server **what action the client wants to perform on the resource**. Without it, a URL alone would be ambiguous. The URL `/posts/1` could mean "show me post 1", "delete post 1", or "replace post 1", and the server could not tell which. By separating the *noun* (the URL identifies the resource) from the *verb* (the method says what to do with it), HTTP lets one URL support several different operations. This is a central REST idea: **one resource, one URL, several verbs.**

The four verbs in this lesson map neatly onto the four basic things you can do with stored data, known by the acronym **CRUD**:

| CRUD action | Meaning | HTTP method |
|-------------|---------|-------------|
| **C**reate | Make something new | `POST` |
| **R**ead | Look at something that exists | `GET` |
| **U**pdate | Change something that exists | `PUT` (replace) or `PATCH` (partial change) |
| **D**elete | Remove something | `DELETE` |

**Plain-language explanation of the table:** CRUD is a way of describing what almost every application does with its data. An online shop creates orders, reads product lists, updates addresses, and deletes items from a cart. The table shows which HTTP verb carries each of those four intentions. The mapping is a convention rather than a law, and you will see in this lesson that `POST` in particular is sometimes used for other purposes.

### 2. Three Properties You Must Understand: Safe, Idempotent, Cacheable

Before studying the verbs one by one, learn three vocabulary words. API specifications use them constantly, and a good tester turns each one into a test.

**Safe.** A method is **safe** when it is defined as read-only. A safe request does not ask the server to change anything. Calling a safe method one time, or one thousand times, should leave the stored data exactly as it was. Safe does not mean the server does *nothing*. The server may still write a line in a log file or update a "visits" counter, but the client is not asking for a change, and the client is not responsible for any change that happens as a side effect.

**Idempotent.** A method is **idempotent** when making the same request many times has the same **effect on the server's state** as making it once. The key words are *effect on state*. The *response* may differ between calls. For example, the first `DELETE` of an order returns a success code, and the second `DELETE` of the same order may return `404 Not Found`, because the order no longer exists. The responses differ, but the **state of the server** after one call and after two calls is identical: the order is gone. That is idempotency.

**Cacheable.** A response is **cacheable** when a browser, proxy, or content delivery network is allowed to store a copy and reuse it for later identical requests without bothering the server again. By definition, `GET` and `HEAD` responses are cacheable by default. `POST` responses can be cacheable only in rare, explicitly marked cases, and in practice you should treat them as not cacheable.

**Analogies to make these stick.**

Safe is like **looking at a menu in a restaurant**. You can read it all day and the kitchen does not cook anything. Ordering a meal is not safe, because it changes what the kitchen does.

Idempotent is like a **lift button**. Pressing the "5th floor" button ten times has the same effect as pressing it once, because the lift is going to the 5th floor either way. A **volume-up button** is not idempotent, because pressing it ten times gives a different volume than pressing it once. Another analogy is setting a thermostat to 21 degrees (idempotent, because "set to 21" repeated is still 21) versus pressing "increase by one degree" (not idempotent).

Cacheable is like a **printed bus timetable at a bus stop**. You do not phone the transport company each time you want to know when the next bus leaves. You look at the copy you already have. That is quick and saves the company work, but if the timetable changed yesterday you may read a stale copy, which is why caches have expiry rules.

Here is the classification you should memorise:

| Method | Safe? | Idempotent? | Cacheable? | Has a request body? |
|--------|-------|-------------|------------|---------------------|
| `GET` | Yes | Yes | Yes | No |
| `HEAD` | Yes | Yes | Yes | No |
| `OPTIONS` | Yes | Yes | No | Usually no |
| `POST` | No | **No** | Rarely | Yes |
| `PUT` | No | Yes | No | Yes |
| `PATCH` | No | Not guaranteed | Rarely | Yes |
| `DELETE` | No | Yes | No | Usually no |

**Plain-language explanation of the table:** Read each row as a set of promises. A safe method cannot be used to change data. An idempotent method is safe to retry after a failure. A method with a body expects you to describe the data in the request. Notice that every safe method is also idempotent (doing nothing repeatedly has the same effect as doing it once), but not every idempotent method is safe: `PUT` and `DELETE` change data, yet repeating them does no additional harm.

**Why testers care.** Imagine your phone loses signal after you tap "Pay". The app does not know whether the request reached the server. If the request was a `PUT` that sets an order status to "paid", the app can safely retry, because a second `PUT` leaves the order "paid". If the request was a `POST` that creates a payment, a blind retry might create a second payment and charge you twice. Retry behaviour, caching behaviour, and the safety of browser pre-fetching all depend on these properties. If an API breaks its promise (a `GET` that modifies data, a `PUT` that behaves differently the second time), automated tools, browsers, and other developers will be surprised in painful ways.

### 3. How to Read the Examples: Our Practice APIs and a Curl Primer

In this lesson you will use two free public practice services.

**JSONPlaceholder** (`https://jsonplaceholder.typicode.com`) is a fake REST API that serves sample posts, comments, users, and todos. It has an important quirk that you **must** understand: **JSONPlaceholder fakes its write operations.** When you send a `POST`, `PUT`, `PATCH`, or `DELETE`, it responds as though the operation succeeded, returning the status code and body a real API would return, but **it does not actually save, change, or delete anything**. The data you read afterwards is always the original sample data. This is deliberate, because thousands of learners share the service and nobody wants one person deleting everyone's posts. The consequence for you is that on JSONPlaceholder, a "create then read back" test will fail with a `404`, even though the `POST` returned `201`. Do not mistake that for a bug in your test. On a real API, the read-back would succeed, and in this lesson we will mark every place where the fake behaviour differs from real behaviour.

**httpbin** (`https://httpbin.org`) is a service built for people learning HTTP. It does not store anything. Instead, it *echoes back* what you sent, so it is perfect for seeing exactly what a request looks like to a server. It also accepts any method on its `/anything` endpoint, and it provides endpoints such as `/status/404` that return whatever status code you ask for.

**A curl primer.** `curl` is a command-line program that sends HTTP requests. You will use these options throughout the lesson:

| Option | Meaning |
|--------|---------|
| `-X METHOD` | Choose the method, for example `-X DELETE`. If you omit it, curl uses `GET` (or `POST` when you give a body). |
| `-i` | Include the **response headers** in the output, in addition to the body. |
| `-v` | **Verbose.** Shows the **raw request** curl sends (lines beginning `>`) and the raw response headers (lines beginning `<`). |
| `-I` | Send a `HEAD` request and show only headers. |
| `-H "Name: value"` | Add a request header. |
| `-d 'text'` | Send `text` as the request body. |
| `-s` | Silent mode. Hides the progress meter. |

Use `-v` whenever you want to see what is truly on the wire.

### 4. GET: Read Data

#### 4.1 Definition and purpose

`GET` **retrieves a representation of a resource**, which is the data a server holds, written in a format such as JSON. It is the most common method on the web. Every time you type an address into a browser, the browser sends a `GET`. In an API, `GET` is used to fetch a single item (`/users/3`) or a collection of items (`/users`). `GET` is **safe, idempotent, and cacheable**.

#### 4.2 How it works step by step on the wire

1. The client builds a request line containing `GET`, the path, and the protocol version, plus headers such as `Host` and `Accept`. There is **no body**.
2. The client sends the request over the network connection to the server.
3. The server finds the resource identified by the path. It does not change it.
4. The server builds a response: a status line, headers, a blank line, and then a body containing the representation.
5. The client reads the status code first to learn whether it worked, then reads the body.

**Raw request** (what `curl -v https://jsonplaceholder.typicode.com/todos/5` sends):

```http
GET /todos/5 HTTP/1.1
Host: jsonplaceholder.typicode.com
User-Agent: curl/8.4.0
Accept: */*

```

**Plain-language explanation:** The first line asks for todo number 5. `Host` names the server, which is required because many websites can share one machine. `User-Agent` says which program is asking. `Accept: */*` says "I will take any format." The blank line at the end marks the end of the headers. There is no body, so nothing follows.

**Raw response:**

```http
HTTP/1.1 200 OK
Content-Type: application/json; charset=utf-8
Cache-Control: max-age=43200
ETag: W/"5f-..."

{
  "userId": 1,
  "id": 5,
  "title": "laboriosam mollitia et enim quasi adipisci quia provident illum",
  "completed": false
}
```

**Plain-language explanation:** `200 OK` means success. `Content-Type` tells the client the body is JSON. `Cache-Control: max-age=43200` allows a copy to be reused for 43,200 seconds (12 hours), which shows the cacheable property in action. The `ETag` is a version label for the data, a topic we return to in the conditional-requests section. The body is the todo itself. (Some headers are shortened here and exact values vary, but the structure is accurate.)

#### 4.3 When and where to use it

Use `GET` whenever the goal is to **look at** data without changing it. In a user-management system, you use it to list users or view one profile. In a shop, you use it to list products or check an order's status. In a todo app, you use it to show the tasks on screen. Never use `GET` for an action that changes data. The reason is practical: browsers pre-fetch links, search engines crawl them, and monitoring tools call them repeatedly, all assuming `GET` is harmless.

#### 4.4 Body, parameters, and where information goes

A `GET` request has **no body**. The HTTP standard does not forbid one, but servers, proxies, and caches handle it inconsistently, so you should treat a `GET` body as a mistake. All the information that narrows the request goes in the URL. A **path segment** identifies the resource (`/todos/5`), and a **query string** filters or controls a collection (`/todos?userId=1`). The next lessons today cover both in detail. For now, just recognise that everything a `GET` needs lives in the URL and the headers.

#### 4.5 Expected status codes

| Situation | Status | Reason |
|-----------|--------|--------|
| Resource found | `200 OK` | The standard success for a read. |
| Resource exists but nothing to show (rare for single items) | `204 No Content` | Success with an empty body. |
| ID does not exist | `404 Not Found` | There is no resource at this address. |
| Client did not log in | `401 Unauthorized` | The server does not know who you are. |
| Logged in but not permitted | `403 Forbidden` | The server knows who you are and says no. |
| Malformed request (for example `/users/abc` where a number is required) | `400 Bad Request` (or `404`) | The request cannot be understood. Either is defensible if documented; `500` is not. |
| Server crashed | `500 Internal Server Error` | The server's own fault. If your test can trigger this with bad input, that is a defect. |

A collection that matches nothing, such as `/todos?userId=9999`, normally returns `200 OK` with an **empty array** `[]`, because the request was valid and simply found no matches. A `404` here would be a questionable design.

#### 4.6 Proving it is safe, idempotent, and cacheable (experiment)

**Experiment:** read the same resource twice and compare, then confirm a read did not change anything.

```bash
curl -s https://jsonplaceholder.typicode.com/todos/5 > first.json
curl -s https://jsonplaceholder.typicode.com/todos/5 > second.json
diff first.json second.json && echo "IDENTICAL: GET did not change the resource"
```

**Plain-language explanation:** The first two lines save the response body into two files. `diff` compares them. The `&&` operator means "only run the next command if the previous one succeeded", and `diff` succeeds only when the files match. If you see the message, the two reads returned identical data, which is consistent with safe and idempotent behaviour. To check the cacheable property, run `curl -i https://jsonplaceholder.typicode.com/todos/5` and look for a `Cache-Control` or `ETag` header, because these are the signals that tell caches the copy may be reused.

#### 4.7 Three realistic scenarios

1. **Online shop:** A product page calls `GET /products/118` to show the price and stock count. A good test confirms the price field is a number, the stock is not negative, and an unknown product ID returns `404` rather than an empty page.
2. **User management:** An admin screen calls `GET /users` to list accounts. A test confirms the response is an array, that sensitive fields such as `password` are **never** present, and that a normal user receives `403` while an admin receives `200`.
3. **Todo app:** The app calls `GET /todos?completed=false` to show open tasks. A test confirms every item returned has `completed` equal to `false`, so the filter really works.

#### 4.8 Full curl walkthrough

```bash
curl -i https://jsonplaceholder.typicode.com/users/3
```

**Plain-language explanation:** This asks for user number 3 and prints the headers (`-i`) followed by the body.

**Expected output (abbreviated):**

```http
HTTP/2 200
content-type: application/json; charset=utf-8
cache-control: max-age=43200

{
  "id": 3,
  "name": "Clementine Bauch",
  "username": "Samantha",
  "email": "Nathan@yesenia.net",
  "address": { "street": "Douglas Extension", "city": "McKenziehaven", ... },
  "phone": "1-463-123-4447",
  "company": { "name": "Romaguera-Jacobson", ... }
}
```

**Plain-language explanation:** The status is `200`. The body is a JSON object with simple fields (`id`, `name`, `email`) and nested objects (`address`, `company`). When you test, you check the status first, then that required fields exist and have the right types. Now a failure case:

```bash
curl -i https://jsonplaceholder.typicode.com/users/9999
```

**Expected output:**

```http
HTTP/2 404
content-type: application/json; charset=utf-8

{}
```

**Plain-language explanation:** There is no user 9999, so the server returns `404`. JSONPlaceholder sends an empty object `{}` as the body. A more informative real API would send a message such as `{"error":"User not found"}`, which you would also assert on.

#### 4.9 Test-case design for GET

| Type | Test case | Input | Expected result |
|------|-----------|-------|-----------------|
| Positive | Fetch existing resource | `GET /users/3` | `200`, JSON, `id` equals 3, required fields present |
| Positive | Fetch collection | `GET /users` | `200`, JSON array, length greater than 0 |
| Positive | Repeatable | Call `GET /users/3` twice | Identical bodies (safety) |
| Negative | Unknown ID | `GET /users/9999` | `404` |
| Negative | Wrong type of ID | `GET /users/abc` | Clean `4xx`, never `500` |
| Negative | Wrong method on endpoint | `DELETE /users/3` where unsupported | `405` and `Allow` header |
| Boundary | Smallest and largest valid ID | `GET /users/1`, `GET /users/10` | `200` for both |
| Boundary | Just outside range | `GET /users/0`, `GET /users/11` | `404` for both |
| Boundary | Negative and huge numbers | `GET /users/-1`, `GET /users/99999999999999999999` | Clean `4xx`, never `500` |
| Security | No credentials on a protected endpoint | `GET /admin/users` with no token | `401` |
| Security | Another user's data | Logged in as user A, `GET /users/B/orders` | `403` or `404`, never B's data |
| Security | Injection in the URL | `GET /users/1'%20OR%20'1'='1` | Clean `4xx`, no database error text |
| Security | Sensitive data exposure | `GET /users/3` | No `password`, token, or internal fields in the body |

**Plain-language explanation of the table:** Positive tests prove the feature works. Negative tests prove it fails gracefully. Boundary tests probe the edges of valid input, where off-by-one mistakes hide. Security-minded tests ask whether someone could see data they should not. A good suite for even a simple `GET` contains all four kinds.

#### 4.10 What a GET defect looks like

A defective `GET` often shows one of these symptoms: it returns `200` with an error message in the body instead of a proper `4xx`; it returns `500` and a stack trace when given an odd ID; it exposes fields it should hide; it changes data (for example a "mark as read" that happens simply by fetching a message); it ignores authorisation so one user can read another's records (a flaw often called an insecure direct object reference); or it returns different data on identical calls with no reason.

### 5. POST: Create Data

#### 5.1 Definition and purpose

`POST` **submits data to the server so that it processes it**, most commonly by **creating a new resource** inside a collection. The client sends the data; the server decides the new resource's ID and address. `POST` is **not safe and not idempotent**, because every call may create something new.

#### 5.2 How it works step by step on the wire

1. The client builds the request line with `POST` and the **collection** path (`/posts`), not a specific item.
2. The client adds a `Content-Type` header declaring the body's format, and usually a `Content-Length` header giving its size in bytes.
3. After the blank line, the client places the body, for example JSON.
4. The server reads `Content-Type` to decide how to parse the body, validates the data, creates the resource, and assigns a new ID.
5. The server replies with `201 Created`, a `Location` header giving the new resource's address, and often the created resource in the body.

**Raw request:**

```http
POST /posts HTTP/1.1
Host: jsonplaceholder.typicode.com
Content-Type: application/json
Content-Length: 54

{"title":"My post","body":"Hello","userId":1}
```

**Plain-language explanation:** The request line targets the collection `/posts`. `Content-Type: application/json` warns the server that the body is JSON. `Content-Length` counts the body's bytes so the server knows where it ends. After the blank line, the body holds the data for the new post. Note that the body does **not** contain an `id`. The client does not choose it.

**Raw response:**

```http
HTTP/1.1 201 Created
Content-Type: application/json; charset=utf-8
Location: https://jsonplaceholder.typicode.com/posts/101

{
  "title": "My post",
  "body": "Hello",
  "userId": 1,
  "id": 101
}
```

**Plain-language explanation:** `201 Created` is more precise than `200 OK`, because it says a new resource now exists. The `Location` header is the address where that new resource lives. The body echoes the data with the **server-assigned `id`** added. (Real JSONPlaceholder responses include `Location` on some deployments and not others, and the `id` is always `101` because it has 100 sample posts. The structure is what matters.)

#### 5.3 When and where to use it

Use `POST` when the **server decides** where the new thing lives: registering a user, placing an order, adding a comment, uploading a file. Because it is the most flexible method, `POST` is also used for operations that do not fit the other verbs, such as `POST /login`, `POST /orders/42/cancel`, or `POST /search` with a complex filter. These are legitimate, but a tester should recognise that such endpoints are "actions" rather than pure creation, and that they inherit `POST`'s non-idempotent nature.

#### 5.4 Body and parameters

`POST` normally **has a body**, and the body must match the declared `Content-Type`. The common formats are:

| Content-Type | Looks like | Typical use |
|--------------|-----------|-------------|
| `application/json` | `{"name":"Ada"}` | Almost all modern APIs |
| `application/x-www-form-urlencoded` | `name=Ada&age=36` | Classic HTML forms |
| `multipart/form-data` | Multiple parts with boundaries | File uploads |

Headers are covered in depth in a later lesson today, but you must already know that **a missing or wrong `Content-Type` is one of the most common reasons a `POST` fails**. The server may treat your JSON as plain text and reject it.

#### 5.5 Expected status codes

| Situation | Status | Reason |
|-----------|--------|--------|
| Resource created | `201 Created` | The ideal answer. Some APIs return `200 OK`, which is acceptable only if documented. |
| Accepted for later processing | `202 Accepted` | Work was queued, not yet done. |
| Missing or malformed field, invalid JSON | `400 Bad Request` | The server cannot process the request as sent. |
| Well-formed but semantically invalid (age of `-5`) | `422 Unprocessable Entity` | Syntax is fine, the meaning is not. |
| Duplicate of a unique value (email already registered) | `409 Conflict` | The request clashes with current state. |
| Wrong `Content-Type` | `415 Unsupported Media Type` | The server does not accept that format. |
| Not logged in or not allowed | `401` / `403` | Authentication or authorisation failure. |
| Body too large | `413 Payload Too Large` | Exceeds the server's limit. |

#### 5.6 Proving it is NOT idempotent (experiment)

On a **real** API, send the identical `POST` twice and compare:

```bash
curl -s -X POST https://api.example.test/orders -H "Content-Type: application/json" -d '{"item":"pen","qty":1}'
curl -s -X POST https://api.example.test/orders -H "Content-Type: application/json" -d '{"item":"pen","qty":1}'
```

**Plain-language explanation:** `api.example.test` is a placeholder for any real API that stores data. You would see two **different** IDs, for example `{"id":501,...}` and `{"id":502,...}`, and a `GET /orders` would show two pen orders. The same request, repeated, produced a different state. That is the definition of non-idempotent.

You can also see the effect on JSONPlaceholder, though only partly, because it fakes writes. Run the same `POST /posts` twice: both responses return `"id": 101`, because the fake server always numbers the next post as 101 and never really stores it. This is not real idempotency. It is a side effect of faking, so use httpbin to observe the exact bytes and a real API (or your Project 2 API) to observe the real duplicate behaviour.

#### 5.7 Three realistic scenarios

1. **Online shop:** `POST /orders` with a cart creates an order. Tests check `201`, a new order number, a total equal to the sum of the line items, and that submitting an empty cart returns `400` or `422`.
2. **User management:** `POST /users` registers an account. Tests check `201`, that the password is **not** returned in the response, that registering the same email twice returns `409`, and that an invalid email format is rejected.
3. **Todo app:** `POST /todos` with `{"title":"Buy milk","completed":false}` creates a task. Tests check `201`, that `completed` defaults to `false` when omitted, and that a later `GET /todos/{id}` returns the same title.

#### 5.8 Full curl walkthrough

```bash
curl -i -X POST https://jsonplaceholder.typicode.com/todos \
  -H "Content-Type: application/json" \
  -d '{"title":"Learn HTTP","completed":false,"userId":1}'
```

**Plain-language explanation:** `-i` shows the response headers. `-X POST` chooses the method. `-H` adds the `Content-Type` header. `-d` supplies the JSON body in single quotes so that the shell does not interfere with the double quotes inside. The backslashes at the end of lines tell the shell the command continues on the next line.

**Expected output:**

```http
HTTP/2 201
content-type: application/json; charset=utf-8
location: https://jsonplaceholder.typicode.com/todos/201

{
  "title": "Learn HTTP",
  "completed": false,
  "userId": 1,
  "id": 201
}
```

**Plain-language explanation:** The status is `201`, the body contains your data plus the new `id` of `201` (JSONPlaceholder has 200 todos). Now try to read it back:

```bash
curl -i https://jsonplaceholder.typicode.com/todos/201
```

On JSONPlaceholder this returns `404 Not Found`, because **the write was faked**. On a real API it would return `200` with your data. The mismatch is a useful lesson in itself: **a `201` status alone proves the server said it created something, not that it actually stored it.** Always verify with a follow-up read when the API is real.

To see exactly what your request looked like, send it to httpbin, which echoes everything back:

```bash
curl -s -X POST https://httpbin.org/anything \
  -H "Content-Type: application/json" \
  -d '{"title":"Learn HTTP"}'
```

The response includes fields such as `"method": "POST"`, `"headers": {"Content-Type": "application/json", ...}`, and `"json": {"title": "Learn HTTP"}`. Plain-language explanation: httpbin shows you the method it received, the headers it received, and the body it parsed, which confirms your request was built correctly. Try removing the `-H` line and watch `"json"` become `null` while `"data"` still holds the text, which demonstrates how the `Content-Type` header controls parsing.

#### 5.9 Test-case design for POST

| Type | Test case | Input | Expected result |
|------|-----------|-------|-----------------|
| Positive | Valid payload | Full valid JSON | `201`, body has new `id`, `Location` header present |
| Positive | Read-back | `GET` the new `id` | `200`, data equals what was posted |
| Positive | Optional field omitted | Leave out an optional field | `201`, sensible default applied |
| Negative | Missing required field | No `title` | `400` or `422`, message names the field |
| Negative | Wrong type | `"userId":"abc"` | `400` or `422` |
| Negative | Invalid JSON | `{"title":` (broken) | `400`, not `500` |
| Negative | Wrong Content-Type | Send JSON as `text/plain` | `415` or `400` |
| Negative | Duplicate unique value | Same email twice | `409` |
| Boundary | Shortest and longest allowed string | Title of 1 character, and of exactly the maximum length | `201` for both |
| Boundary | One beyond the limit | Maximum length plus 1 | `400` or `422` |
| Boundary | Numeric limits | `qty` of 0, 1, maximum, maximum plus 1, and -1 | Valid ones `201`, others rejected |
| Boundary | Empty body or `{}` | No data at all | `400` or `422` |
| Security | Special characters | `<script>alert(1)</script>`, quotes, emoji | Stored safely or rejected, never executed or causing `500` |
| Security | Injection text | `'; DROP TABLE users;--` | Treated as plain text, no database error |
| Security | Mass assignment | Add `"role":"admin"` or `"id":1` to the body | Extra privileged fields ignored or rejected |
| Security | No credentials | Omit token on a protected endpoint | `401` |
| Security | Oversized body | Several megabytes | `413`, server stays responsive |

**Plain-language explanation of the table:** "Mass assignment" means a server blindly copies every field you send into the new record. A tester who adds `"role":"admin"` to a registration request is checking whether the server wrongly obeys it. Boundary rows target the exact edge of each rule in the specification, because defects cluster at edges.

#### 5.10 What a POST defect looks like

Typical defects are: returning `200` with `{"success": false}` for a failure, so a naive check passes; returning `201` but not saving the data; creating duplicates on every retry with no protection; accepting a missing required field and storing `null`; returning `500` for broken JSON; echoing the password or a hidden field in the response; accepting privileged fields supplied by the client; and a `Location` header pointing to an address that returns `404`.

### 6. PUT: Replace Data

#### 6.1 Definition and purpose

`PUT` **replaces the entire resource at a known address with the representation you send.** The word to remember is *replace*. The server takes your body and makes the resource look exactly like it, discarding what was there before. `PUT` is **idempotent and not safe**.

#### 6.2 How it works step by step on the wire

1. The client builds a request line with `PUT` and the **specific resource** path (`/posts/1`).
2. The client adds `Content-Type` and a **complete** body describing the whole resource.
3. The server locates the resource at that address.
4. The server overwrites its stored version with the one in the body.
5. The server replies with `200 OK` and the new representation, or `204 No Content` with no body.

**Raw request:**

```http
PUT /posts/1 HTTP/1.1
Host: jsonplaceholder.typicode.com
Content-Type: application/json
Content-Length: 78

{"id":1,"title":"Updated title","body":"Updated body","userId":1}
```

**Plain-language explanation:** The path names post 1. The body is the full replacement, containing every field the resource should have. If the original post had four fields, the body supplies all four.

**Raw response:**

```http
HTTP/1.1 200 OK
Content-Type: application/json; charset=utf-8

{
  "id": 1,
  "title": "Updated title",
  "body": "Updated body",
  "userId": 1
}
```

**Plain-language explanation:** `200 OK` plus the new state of the resource. A real API might instead return `204 No Content` with an empty body, meaning "done, nothing more to say".

#### 6.3 When and where to use it

Use `PUT` when the client knows the resource's address and wants to set its complete state: saving an edited profile form, replacing a product's full details, or storing a configuration file. A secondary use is "create or replace at a client-chosen address", for example `PUT /files/report.pdf`, where the server creates the resource if it does not exist and responds `201 Created`. Many APIs do not support that, so check the documentation.

#### 6.4 Body and parameters

`PUT` has a **body** with the complete representation. The resource is identified by the **path**, not by a query string. The important behavioural rule: **fields you leave out are treated as "should be empty or default"**, so a partial `PUT` can wipe data. This is the single most common surprise for newcomers, and the reason `PATCH` exists.

#### 6.5 Expected status codes

| Situation | Status | Reason |
|-----------|--------|--------|
| Updated, new state returned | `200 OK` | Standard success. |
| Updated, no body returned | `204 No Content` | Success with nothing to send back. |
| Resource did not exist and was created | `201 Created` | Only in APIs that allow create-by-PUT. |
| Resource does not exist (creation not allowed) | `404 Not Found` | Nothing to replace. |
| Invalid body | `400` / `422` | Data fails validation. |
| ID in body disagrees with ID in URL | `400` or `409` | Conflicting instructions. |
| Not permitted | `401` / `403` | Auth failure. |

#### 6.6 Proving it is idempotent (experiment)

On a real API, send the same `PUT` three times and read after each:

```bash
for i in 1 2 3; do
  curl -s -X PUT https://api.example.test/todos/5 \
    -H "Content-Type: application/json" \
    -d '{"id":5,"title":"Water plants","completed":true,"userId":1}' > /dev/null
  curl -s https://api.example.test/todos/5
  echo
done
```

**Plain-language explanation:** The loop runs three times. Each time it sends the identical `PUT` (output thrown away with `> /dev/null`), then reads the resource and prints it. You expect three identical lines showing "Water plants" with `completed` true. The state after the third call equals the state after the first. That is idempotency. Compare with `POST`, which would give three different records.

On JSONPlaceholder the experiment is meaningless for state (nothing is stored), but every `PUT` returns the same response, so you can still practise the commands.

#### 6.7 Three realistic scenarios

1. **Online shop:** `PUT /products/118` replaces a product's name, price, description, and stock in one operation from an admin form. A test sends a full body, then reads back and confirms every field. A second test sends the same body again and confirms nothing else changes.
2. **User management:** `PUT /users/7` saves the "Edit profile" form. A test omits the `phone` field and checks whether the phone number is cleared, documenting the replace behaviour. Another test tries to change `role` as a normal user and confirms it is rejected.
3. **Todo app:** `PUT /todos/5` replaces the task text and completion flag. A test confirms that updating a todo that belongs to another user returns `403` or `404`.

#### 6.8 Full curl walkthrough

```bash
curl -i -X PUT https://jsonplaceholder.typicode.com/posts/1 \
  -H "Content-Type: application/json" \
  -d '{"id":1,"title":"Updated title","body":"Updated body","userId":1}'
```

**Plain-language explanation:** Same shape as the `POST` command, but the method is `PUT` and the path ends in an ID, because we are replacing a specific resource.

**Expected output:**

```http
HTTP/2 200
content-type: application/json; charset=utf-8

{
  "id": 1,
  "title": "Updated title",
  "body": "Updated body",
  "userId": 1
}
```

**Plain-language explanation:** The response echoes the replacement. On JSONPlaceholder, a follow-up `GET /posts/1` returns the **original** title, because the write was not stored. On a real API it would return "Updated title". Also note that JSONPlaceholder's behaviour for a `PUT` to a non-existent ID, such as `/posts/9999`, is not a clean `404`. It may return a `500` error, which is a quirk of the fake server and a reminder that a well-built real API should return `404` there.

#### 6.9 Test-case design for PUT

| Type | Test case | Input | Expected result |
|------|-----------|-------|-----------------|
| Positive | Full update | Complete valid body | `200` or `204` |
| Positive | Read-back | `GET` the same ID | New values visible |
| Positive | Idempotency | Send identical `PUT` twice | Same final state, same status |
| Negative | Non-existent ID | `PUT /posts/9999` | `404` |
| Negative | Invalid field value | `"userId":"abc"` | `400` or `422` |
| Negative | Wrong Content-Type | `text/plain` | `415` |
| Negative | ID mismatch | URL `/posts/1`, body `"id":2` | `400` or `409`, or body ID ignored (documented) |
| Boundary | Maximum-length title | Exactly the limit | `200` |
| Boundary | Beyond the limit | Limit plus 1 | `400` / `422` |
| Boundary | Empty string for a required field | `"title":""` | `400` / `422` |
| Boundary | Missing optional fields | Omit them | Reset to default (documents replace behaviour) |
| Security | Another user's resource | User A updates user B's profile | `403` or `404` |
| Security | Read-only field change | Set `"id"`, `"createdAt"`, `"role"` | Ignored or rejected |
| Security | No credentials | No token | `401` |

**Plain-language explanation of the table:** The "missing optional fields" test is a documentation test. It records what the API does with omitted fields so that everyone knows `PUT` has replace semantics. The "another user's resource" test checks authorisation, which is separate from checking that the data is valid.

#### 6.10 What a PUT defect looks like

Defects include: a `PUT` that behaves like a partial update (missing fields survive) when documented as replace, or the reverse; returning `200` but not saving; a second identical `PUT` changing something, such as incrementing a "version" or "updatedBy" in an unexpected way, or creating a duplicate; accepting changes to read-only fields; letting one user overwrite another's data; and returning `500` for an unknown ID rather than `404`.

### 7. PATCH vs PUT in Depth

`PATCH` **applies a partial modification** to a resource: you send only the fields that change, and everything else is left untouched. It was added to HTTP later precisely because replacing a whole resource just to change one field is wasteful and risky.

**Analogy:** Imagine a printed form already filled in. `PUT` is like **throwing the form away and handing over a brand-new complete form**. If you forget to fill in one box on the new form, that box is now blank. `PATCH` is like **using correction fluid on just one box** and leaving the rest alone.

**Worked example.** Suppose the server holds this user:

```json
{"id": 7, "name": "Ada Lovelace", "email": "ada@example.com", "phone": "555-0100"}
```

**Plain-language explanation:** This is the starting state, with four fields.

Now we send a `PUT` with a partial body:

```bash
curl -i -X PUT https://api.example.test/users/7 \
  -H "Content-Type: application/json" \
  -d '{"name":"Ada King"}'
```

A strict `PUT` implementation replaces the resource with the body, so the new state is `{"id":7,"name":"Ada King"}` (or the server rejects the request with `400` because required fields are missing). The email and phone are **gone**. Now the same intention with `PATCH`:

```bash
curl -i -X PATCH https://api.example.test/users/7 \
  -H "Content-Type: application/json" \
  -d '{"name":"Ada King"}'
```

The new state is `{"id":7,"name":"Ada King","email":"ada@example.com","phone":"555-0100"}`. **Only the name changed.**

**Plain-language explanation of both commands:** They are identical except for the method, yet they leave the server in different states. That difference is exactly what a tester must check when the specification says which one an endpoint uses.

On the wire a `PATCH` looks like this:

```http
PATCH /users/7 HTTP/1.1
Host: api.example.test
Content-Type: application/json

{"name":"Ada King"}
```

**Plain-language explanation:** Short body, specific resource path. Typical responses are `200 OK` with the updated resource or `204 No Content`.

| Aspect | `PUT` | `PATCH` |
|--------|-------|---------|
| Body contains | The complete resource | Only the changes |
| Omitted fields | Reset or removed | Left unchanged |
| Idempotent | Yes, by definition | Not guaranteed |
| Request size | Larger | Smaller |
| Risk | Accidentally wiping fields | Concurrent edits, ambiguous semantics |
| Typical use | "Save the whole form" | "Change just the email" or "mark complete" |

**Why PATCH is not guaranteed idempotent.** A patch like `{"completed": true}` is idempotent, since repeating it keeps `completed` true. But some patch formats describe *operations*, such as "add 1 to the counter" or "append this item to the list". Repeating those changes the result each time. Because the method itself does not forbid such operations, the standard does not promise idempotency. When you test a `PATCH`, read the API documentation to find out which kind the endpoint accepts, and test repeat behaviour explicitly.

**Two patch formats (awareness only).** Most APIs accept a simple JSON object of fields to change (called a *merge patch*, as above). A more formal alternative, *JSON Patch*, sends a list of operations such as `[{"op":"replace","path":"/name","value":"Ada King"}]`. You will rarely need to construct the second form in this course, but you should recognise it.

**Test ideas for PATCH:** send one field and confirm the others are unchanged after a read-back; send an unknown field; send an empty `{}` body; patch a non-existent ID (`404`); and patch a read-only field. Many teams also add one test that proves the same endpoint's `PUT` and `PATCH` differ in the way the specification says.

### 8. DELETE: Remove Data

#### 8.1 Definition and purpose

`DELETE` **removes the resource at the given address.** It is **not safe, but it is idempotent**: after the first successful delete the resource is gone, and deleting it again leaves the server in the same state, which is "gone".

#### 8.2 How it works step by step on the wire

1. The client builds a request line with `DELETE` and the specific resource path.
2. There is usually no body and therefore no `Content-Type`. Authentication headers are common.
3. The server checks the caller is allowed to delete this resource.
4. The server removes the resource (permanently, or by marking it deleted, a "soft delete").
5. The server replies with `204 No Content`, or `200 OK` with a confirmation body.

**Raw request:**

```http
DELETE /posts/1 HTTP/1.1
Host: jsonplaceholder.typicode.com

```

**Plain-language explanation:** Just a request line, a `Host` header, and a blank line. There is no body, because the URL already says what to remove.

**Raw response:**

```http
HTTP/1.1 200 OK
Content-Type: application/json; charset=utf-8

{}
```

**Plain-language explanation:** JSONPlaceholder answers `200` with an empty object. A typical real API answers `204 No Content` with no body at all. Both mean "it is done".

#### 8.3 When and where to use it

Use `DELETE` to remove a resource the client can name: delete a cart item, remove a user account, cancel a draft. Some systems prefer **soft deletes**, where the record is flagged as deleted rather than erased, so that it can be restored or kept for audit. The visible behaviour is the same: a later `GET` returns `404`.

#### 8.4 Body and parameters

`DELETE` normally has **no body**. The resource is identified by the path. Some APIs accept query parameters for options, such as `?force=true`. Treat a body on `DELETE` as unusual.

#### 8.5 Expected status codes

| Situation | Status | Reason |
|-----------|--------|--------|
| Deleted, nothing to return | `204 No Content` | The most common success. |
| Deleted, confirmation returned | `200 OK` | Success with a message body. |
| Accepted, will be deleted later | `202 Accepted` | Asynchronous deletion. |
| Already deleted or never existed | `404 Not Found` | Nothing at that address. Acceptable on repeat. |
| Not logged in / not allowed | `401` / `403` | Auth failure. |
| Other records depend on it | `409 Conflict` | Deleting would break references (for example a user who still has orders). |
| Wrong method for the collection | `405` | Deleting a whole collection is not offered. |

**A subtle point about repeated deletes.** Some APIs return `204` even on the second delete, treating "make sure it is gone" as satisfied; others return `404`. Both are idempotent in the sense that matters, because the **state** is identical. A test should assert whichever the documentation says, and should never treat the repeat's `404` as an error in the API.

#### 8.6 Proving it is idempotent (experiment)

On a real API:

```bash
curl -s -o /dev/null -w "first delete:  %{http_code}\n" -X DELETE https://api.example.test/todos/5
curl -s -o /dev/null -w "second delete: %{http_code}\n" -X DELETE https://api.example.test/todos/5
curl -s -o /dev/null -w "read after:    %{http_code}\n" https://api.example.test/todos/5
```

**Plain-language explanation:** `-o /dev/null` discards the body. `-w` prints a custom message after the transfer, where `%{http_code}` is replaced by the status. Expected output is `204`, then `404` (or `204`), then `404`. The responses differ, but the final state, "todo 5 does not exist", is the same after one delete or two. That is idempotent state, even though the status codes are not identical.

#### 8.7 Three realistic scenarios

1. **Online shop:** `DELETE /cart/items/9` removes an item. A test deletes it, then reads the cart and confirms the item is absent and the total has been recalculated.
2. **User management:** `DELETE /users/7` removes an account. Tests confirm that a normal user receives `403` when deleting someone else, that an admin succeeds, and that the user's orders are either deleted, kept, or the request refused with `409`, exactly as the specification says.
3. **Todo app:** `DELETE /todos/5` removes a task. A test confirms the task no longer appears in `GET /todos` and that `GET /todos/5` returns `404`.

#### 8.8 Full curl walkthrough

```bash
curl -i -X DELETE https://jsonplaceholder.typicode.com/posts/1
```

**Plain-language explanation:** Delete post 1 and show headers.

**Expected output:**

```http
HTTP/2 200
content-type: application/json; charset=utf-8

{}
```

**Plain-language explanation:** `200` with `{}`. Because the delete is faked, `curl https://jsonplaceholder.typicode.com/posts/1` afterwards still returns the post with `200`. On a real API you would expect `404`. This is the second place where you must remember the fake behaviour: **do not "fix" your expectation to match the fake; write the test for the real behaviour and run it against your real Project 2 API.**

To explore `DELETE` against something that truthfully reports what it received, use httpbin:

```bash
curl -i -X DELETE https://httpbin.org/delete
```

It returns `200` and a JSON echo of your request, confirming the method received was `DELETE`. Trying `curl -i -X DELETE https://httpbin.org/get` returns `405 Method Not Allowed`, which previews the next section.

#### 8.9 Test-case design for DELETE

| Type | Test case | Input | Expected result |
|------|-----------|-------|-----------------|
| Positive | Delete existing | `DELETE /todos/5` | `204` (or `200`) |
| Positive | Confirm removal | `GET /todos/5` afterwards | `404` |
| Positive | Collection updated | `GET /todos` afterwards | ID 5 absent, count reduced by 1 |
| Negative | Delete twice | Second `DELETE /todos/5` | `404` (or `204`), no `500` |
| Negative | Unknown ID | `DELETE /todos/9999` | `404` |
| Negative | Malformed ID | `DELETE /todos/abc` | `400` or `404` |
| Negative | Delete whole collection | `DELETE /todos` | `405`, and no data lost |
| Boundary | Delete the last remaining item | Only one todo left | `204`, collection returns `[]` |
| Boundary | Delete the first and highest IDs | `/todos/1`, `/todos/200` | Both work normally |
| Security | No credentials | No token | `401`, resource still exists |
| Security | Another user's resource | User A deletes user B's todo | `403` or `404`, resource still exists |
| Security | Dependent data | Delete a user with orders | `409` or documented cascade |
| Security | Delete via GET | `GET /todos/5/delete` or `GET /deleteTodo?id=5` | Must not delete anything |

**Plain-language explanation of the table:** In several security rows the key assertion is that the resource **still exists** afterwards. A rejected delete is only truly rejected if the data survives, so always follow with a `GET`.

#### 8.10 What a DELETE defect looks like

Defects include: returning `204` but not deleting; deleting by `GET`; returning `500` on the second delete; allowing any user to delete any record; deleting a parent but leaving orphaned children that now cause errors; permitting a `DELETE` on a whole collection; and returning `200` with an error message in the body when the delete failed.

### 9. HEAD and OPTIONS

**`HEAD`** is exactly like `GET`, except the server sends back **only the status line and headers, with no body**. It is safe, idempotent, and cacheable. It is useful for cheap checks: does the resource exist (`200` versus `404`)? How large is it (`Content-Length`)? Has it changed (`ETag`, `Last-Modified`)?

```bash
curl -I https://jsonplaceholder.typicode.com/posts/1
```

**Plain-language explanation:** The capital `-I` tells curl to send a `HEAD` request. The output is headers only, such as `HTTP/2 200` and `content-type: application/json`. Because the server runs the same logic as `GET` but omits the body, the status and headers must match what a `GET` would produce. A test can compare them: if `HEAD` says `200` but `GET` says `404`, one of them is defective.

**`OPTIONS`** asks the server **which methods and features a URL supports.** A well-behaved server answers `200 OK` or `204 No Content` with an `Allow` header listing the methods.

```bash
curl -i -X OPTIONS https://httpbin.org/anything
```

**Plain-language explanation:** This sends the `OPTIONS` method. The response typically includes `Allow: GET, POST, PUT, PATCH, DELETE, HEAD, OPTIONS` (the exact list depends on the server). That tells you which verbs the endpoint accepts, which is excellent information for deciding what to test and what should return `405`.

`OPTIONS` has a second, very important job in browsers: **CORS preflight**. When a web page from one website tries to call an API on a different website, the browser first sends an automatic `OPTIONS` request to ask whether this is allowed, and looks for headers such as `Access-Control-Allow-Origin` in the answer. You will not test this in depth today. The point is that if you ever see `OPTIONS` requests in a browser's network tab, you did not send them. The browser did.

### 10. 405 Method Not Allowed and the Allow Header

Every URL supports only certain methods. A collection such as `/users` usually supports `GET` (list) and `POST` (create), but not `PUT` or `DELETE`. A single resource such as `/users/7` usually supports `GET`, `PUT`, `PATCH`, and `DELETE`, but not `POST`. When a client uses a method the endpoint does not support, a correct server replies **`405 Method Not Allowed`** and **must** include an **`Allow`** header naming the methods that *are* supported.

```http
DELETE /users HTTP/1.1
Host: api.example.test
```

```http
HTTP/1.1 405 Method Not Allowed
Allow: GET, POST
Content-Type: application/json

{"error":"Method DELETE is not allowed on /users"}
```

**Plain-language explanation:** The first block is the offending request, an attempt to delete the whole collection. The second block is the correct response: `405`, an `Allow` header saying only `GET` and `POST` are permitted, and an explanatory message. The header turns an error into guidance, because the client can read it and learn what to do instead.

You can see a real `405` on httpbin:

```bash
curl -i -X POST https://httpbin.org/get
```

**Expected output:**

```http
HTTP/2 405
allow: GET, HEAD, OPTIONS
content-type: text/html

<!doctype html>...<title>405 Method Not Allowed</title>...
```

**Plain-language explanation:** `/get` only accepts `GET` (plus `HEAD` and `OPTIONS`), so a `POST` is refused, and the `allow` header lists what would have worked.

**Do not confuse 405 with similar codes.** `404 Not Found` means "there is nothing at that URL." `405` means "there is something at that URL, but not for that verb." `403 Forbidden` means "I understand and the verb is generally supported, but you are not allowed." `501 Not Implemented` means "the server does not recognise that method at all."

**Test ideas:** for each endpoint, deliberately send each verb it should *not* support and assert `405` plus a correct `Allow` header. Pay special attention to destructive verbs: `DELETE /users` must never delete every user, and `PUT /users` must never overwrite the entire user table. **Defect appearance:** the unsupported verb returns `200` and does something unexpected, returns `500`, or returns `405` without an `Allow` header (a specification violation).

### 11. Method Override Tricks (Awareness Level)

Some older browsers, proxies, and firewalls only allow `GET` and `POST`. To work around this, some frameworks let a client send a `POST` but include a header or field that says "treat this as another method." The widely used header is `X-HTTP-Method-Override`:

```http
POST /users/7 HTTP/1.1
X-HTTP-Method-Override: DELETE
```

**Plain-language explanation:** On the wire this is a `POST`, but a server with override support treats it as a `DELETE` of user 7. A similar trick is a hidden form field named `_method`.

**Why a tester should care.** Override is a **security risk** when it is enabled unexpectedly. Suppose a firewall rule blocks `DELETE /users/*` from the internet. An attacker sends `POST` with the override header, the firewall sees an innocent `POST`, and the server performs the delete. A security-minded test sends override headers to endpoints where they should not work and confirms the server ignores them. Beyond this awareness, you will not need to build override requests in this course.

### 12. Idempotency Keys for POST (Awareness Level)

Recall the payment problem: a `POST` that charges a card may time out, and retrying it may charge twice. Since `POST` is not idempotent by nature, many serious APIs (payment services especially) let the client **make a particular `POST` safe to retry** by attaching a unique value called an **idempotency key**:

```http
POST /payments HTTP/1.1
Idempotency-Key: 7c9e6679-7425-40de-944b-e07fc1f90ae7
Content-Type: application/json

{"amount": 2500, "currency": "USD"}
```

**Plain-language explanation:** The client invents a unique random string for this one payment attempt and sends it in a header. (The exact header name, commonly `Idempotency-Key`, varies by API.) The server records the key along with the result. If the same key arrives again, the server does **not** create a second payment. It returns the **saved result of the first one**. Different keys mean different payments.

**What you would test:** send the identical request with the same key twice and confirm only one payment exists and both responses report the same payment ID; then send the same body with a *different* key and confirm a second payment is created; and send the same key with a *different* body and expect an error such as `409` or `422`. Not every API has this feature, so only test it if the specification includes it.

### 13. Conditional Requests: ETag and If-Match (Awareness Level)

Imagine two people open the same product record. Alice changes the price and saves. Bob, who still has the old copy on screen, changes the description and saves a full `PUT`. Bob's save silently **overwrites Alice's price change**, because his copy contained the old price. This is the **lost update** problem.

HTTP offers a solution. The server labels each version of a resource with an **ETag** (an entity tag, a short string that changes whenever the data changes):

```http
HTTP/1.1 200 OK
ETag: "v7"
```

When the client updates the resource, it sends that tag back in an **`If-Match`** header, meaning "only apply my change if the resource is still version v7":

```http
PUT /products/118 HTTP/1.1
If-Match: "v7"
Content-Type: application/json

{"name":"Pen","price":150}
```

**Plain-language explanation:** If nobody changed the product, the tags match and the update succeeds. If Alice already changed it, the current tag is `"v8"`, the condition fails, and the server replies **`412 Precondition Failed`** without changing anything. Bob's application can then reload and merge. A related header, `If-None-Match`, is used with `GET` so the server can answer `304 Not Modified` (no body) if the client's cached copy is still current, which saves bandwidth. You will not build these today, but if the Project 2 API specification mentions ETags, a good test sends a stale `If-Match` and expects `412`.

### 14. The Full CRUD Lifecycle Test

The most valuable API test pattern is the **lifecycle test**: it follows one resource from birth to death, using every verb in order. It is valuable because it checks not just individual endpoints but whether they **cooperate**, in other words, whether data written by one call is really visible to the next.

Below are the six steps as they would run against a **real** API with a `/todos` resource. After the list, every step is explained.

```bash
# Step 1: CREATE
curl -i -X POST https://api.example.test/todos \
  -H "Content-Type: application/json" \
  -d '{"title":"Water plants","completed":false,"userId":1}'

# Step 2: READ (use the id returned in step 1; assume 201)
curl -i https://api.example.test/todos/201

# Step 3: UPDATE (replace)
curl -i -X PUT https://api.example.test/todos/201 \
  -H "Content-Type: application/json" \
  -d '{"id":201,"title":"Water plants","completed":true,"userId":1}'

# Step 4: READ again
curl -i https://api.example.test/todos/201

# Step 5: DELETE
curl -i -X DELETE https://api.example.test/todos/201

# Step 6: READ one last time
curl -i https://api.example.test/todos/201
```

**Plain-language explanation of the commands:** These are six separate requests against the same resource. The ID `201` stands for whichever ID the server returned in step 1. You must copy it by hand, which leads to an important point below.

**Step-by-step meaning.**

**Step 1, create (`POST`).** We ask the server to make a todo. We expect `201 Created`, a body containing the new `id` (say `201`), the same title we sent, and `completed` equal to `false`. We write the `id` down, because every later step needs it. What this proves: creation works and the server assigns identifiers.

**Step 2, read (`GET`).** We fetch the todo by the new ID. We expect `200 OK` and a body equal to what we posted. What this proves: **the data was really saved**. This is the check that catches a server that says `201` but stores nothing.

**Step 3, update (`PUT`).** We replace the todo with a version where `completed` is `true`. We expect `200` (or `204`). Notice we resend the complete body, including `title` and `userId`, because `PUT` replaces everything. What this proves: update is accepted.

**Step 4, read again (`GET`).** We expect `200` and `completed` now `true`, with the title unchanged. What this proves: **the update was really saved** and nothing else was accidentally altered.

**Step 5, delete (`DELETE`).** We expect `204` (or `200`). What this proves: the server accepts removal.

**Step 6, read a final time (`GET`).** We expect `404 Not Found`. What this proves: **the resource is truly gone**. Here, `404` is the *passing* result, and a `200` would be a failure.

**Why HTTP statelessness matters here.** The server does not remember your conversation. Each request is independent, which is why step 1's `id` has to be carried into the later steps explicitly. In Postman, later today, you will save the ID into a variable and reuse it. Tomorrow you will do the same with variables in Python code.

**Cleaning up.** A lifecycle test creates its own data and deletes it at the end, so it leaves nothing behind and can be run again and again. This property, being repeatable regardless of what ran before, is valuable for automation and is the start of an idea called test isolation that we will return to on Wednesday.

**Running it on JSONPlaceholder.** If you run the same six commands against `https://jsonplaceholder.typicode.com`, steps 1, 3, and 5 return the expected statuses (`201`, `200`, `200`), but steps 2, 4, and 6 do not behave like a real server: step 2 returns `404` (the todo was never stored), step 4 also returns `404`, and step 6 returns `404`, which accidentally "passes" for the wrong reason. This is a perfect illustration of why the practice service cannot validate a lifecycle test, and why your real Project 2 API can. Use JSONPlaceholder to learn the commands, and use a service that truly stores data to learn the behaviour.

### 15. How This Maps to Postman

Postman is a graphical API client you will use in the lessons that follow today. Everything in this lesson transfers directly, and here is exactly where each piece lives in its interface.

**The request builder.** At the top of a request tab you see one row with a **method dropdown** on the left, a **URL field** in the middle, and a **Send** button on the right. The dropdown lists `GET`, `POST`, `PUT`, `PATCH`, `DELETE`, `HEAD`, `OPTIONS` and others. Choosing a method there is the same as `curl -X`.

**The tabs below the URL.** Directly beneath the URL row you see tabs named **Params**, **Authorization**, **Headers**, **Body**, **Scripts** (earlier versions: Pre-request Script and Tests), and **Settings**. The ones that matter today:

The **Params** tab shows the query string as a table of keys and values, a topic of the lesson after this one. The **Headers** tab is a table where you add headers such as `Content-Type`, the equivalent of `curl -H`. The **Body** tab is where you supply data for `POST`, `PUT`, and `PATCH`. For JSON, choose the radio button **raw**, then in the small dropdown that appears at the right choose **JSON**, and paste your JSON text. This is the equivalent of `curl -d`. When you do this, Postman automatically adds `Content-Type: application/json` for you, which you can see in the Headers tab by clicking the "hidden" headers toggle. For `GET` and `DELETE`, leave Body set to **none**.

**The response area.** After you click **Send**, the lower half of the window shows the response. At the top-right of that area you see the **Status** (for example `201 Created`), the **Time** in milliseconds, and the **Size**. The response area has tabs: **Body** (with Pretty, Raw, and Preview views, where *Pretty* formats JSON nicely and *Raw* shows the exact text), **Cookies**, **Headers** (the response headers such as `Location` and `Allow`), and **Test Results**. This is the same information `curl -i` printed, in a friendlier layout.

**Seeing the raw request.** To see exactly what Postman sent, open the **Postman Console** (from the **View** menu, or the Console button at the bottom of the window). It logs each request line, headers, and body, equivalent to `curl -v`.

**Mapping the six lifecycle steps.** You will create six requests in a collection, named for example "01 Create todo" (`POST`), "02 Read todo" (`GET`), "03 Replace todo" (`PUT`), "04 Read todo after update" (`GET`), "05 Delete todo" (`DELETE`), and "06 Read todo after delete" (`GET`). In the **Tests** area of each request you will add checks such as "status code is 201". Passing the ID from request 1 to the others uses Postman variables, a topic with its own lesson later today, so for now just note that this is the tool Postman uses to solve the "carry the ID forward" problem described above. Collections, which group these requests, also have a dedicated lesson.

### 16. Common Mistakes (and Why They Matter)

**Using `POST` for everything.** Some poorly designed APIs send every operation through `POST`, including reads and deletes. This hides intent, prevents caching, and loses the retry guarantees of `GET`, `PUT`, and `DELETE`. As a tester, you will still test such an API, but note it as a design smell and be extra careful about retries.

**Sending a partial `PUT` and expecting a partial update.** Because `PUT` replaces, missing fields may be erased or rejected. The reason this hurts is that the data loss is silent: the response is `200`. If you only want to change one field, use `PATCH`, or send the full body.

**Trusting the status code alone.** A `201` or `200` only tells you what the server *claimed*. The verification that matters is the follow-up `GET`. Servers can return success and fail to save due to a bug, a rolled-back transaction, or (as with JSONPlaceholder) deliberate faking.

**Treating `404` on the second `DELETE` as a failure.** For an idempotent method, what matters is the state, not the code. The resource is gone, so the system is in the correct state. Writing a test that fails here creates false alarms and wastes time.

**Forgetting `Content-Type` on a body.** Without it, many servers cannot parse the body, and return `400` or `415`, or silently see an empty body. This is the number one cause of "my POST does not work" for beginners.

**Expecting a body from `DELETE` or `204`.** By definition `204 No Content` has no body, so an assertion that parses JSON from it will crash. Check the status first, and only then decide whether to read a body.

**Retrying `POST` blindly.** Because `POST` is not idempotent, a test framework that automatically retries failed requests can create duplicate data and pollute later tests. Retry `GET`, `PUT`, and `DELETE`, but think hard before retrying `POST`.

**Using `GET` for something that changes data.** It is dangerous because browsers, crawlers, link previewers, and caches assume it is safe and may call it without anyone intending the action.

**Using a real production URL for destructive experiments.** Always practise writes against a training service or a dedicated test environment. This is a professional habit, not just a safety tip.

### 17. Practice Exercises

Work through these using `curl -i` and the practice services. Attempt each yourself before reading the worked solution that follows it. Remember that JSONPlaceholder fakes writes.

---

**Exercise 1: Read a resource and inspect its anatomy.**
Send `GET /todos/5` to JSONPlaceholder. Report the status code, the `Content-Type`, and the names and data types of the fields in the body.

**Solution 1.**

```bash
curl -i https://jsonplaceholder.typicode.com/todos/5
```

**Plain-language explanation:** This requests todo 5 with headers shown. The status is `200`, the `content-type` is `application/json; charset=utf-8`, and the body has four fields: `userId` (number, 1), `id` (number, 5), `title` (string, some text), and `completed` (boolean, `false`). Recording types matters because assertions in your later Postman and Python tests check types, not just presence.

---

**Exercise 2: Provoke a 404 and compare it with an empty result.**
Send `GET /todos/9999`, and then `GET /todos?userId=9999`. Explain why the two responses differ.

**Solution 2.**

```bash
curl -i https://jsonplaceholder.typicode.com/todos/9999
curl -i "https://jsonplaceholder.typicode.com/todos?userId=9999"
```

**Plain-language explanation:** The first asks for one specific resource that does not exist, so it returns `404` with `{}`. The second asks the collection to filter by an owner who has no todos. The request itself is valid, so the answer is `200 OK` with an empty array `[]`. The quotes around the second URL stop the shell from misreading the `?`. The lesson: "there is no such thing" (`404`) and "the search found nothing" (`200` plus `[]`) are different situations.

---

**Exercise 3: Create a todo and interpret the response.**
`POST` `{"title":"Learn HTTP","completed":false,"userId":1}` to `/todos`. What is the status, the new `id`, and does the `GET` of that id work? Explain.

**Solution 3.**

```bash
curl -i -X POST https://jsonplaceholder.typicode.com/todos \
  -H "Content-Type: application/json" \
  -d '{"title":"Learn HTTP","completed":false,"userId":1}'
curl -i https://jsonplaceholder.typicode.com/todos/201
```

**Plain-language explanation:** The `POST` returns `201` and the body includes `"id": 201`. The `GET` of `/todos/201` returns `404`, because JSONPlaceholder faked the write and stored nothing. On a real API the `GET` would return `200` with your data. The correct conclusion is that the `POST` response is realistic, while the read-back cannot be validated on this service.

---

**Exercise 4: See why Content-Type matters.**
Use httpbin to send the same JSON body twice, once with the JSON `Content-Type` and once with none, and compare the `json` and `data` fields in the echo.

**Solution 4.**

```bash
curl -s -X POST https://httpbin.org/anything \
  -H "Content-Type: application/json" -d '{"a":1}'
curl -s -X POST https://httpbin.org/anything \
  -H "Content-Type:" -d '{"a":1}'
```

**Plain-language explanation:** In the first response, `"json"` is `{"a": 1}`, so httpbin understood the body. In the second, `-H "Content-Type:"` with an empty value removes the header, so `"json"` is `null` while `"data"` still contains the raw text `{"a":1}`. The server received the bytes but did not know how to interpret them. (Without the removal, `curl -d` would add a form `Content-Type` by default, which is also not JSON, so the lesson is the same.)

---

**Exercise 5: Compare PUT and PATCH.**
Send a `PUT` to `/todos/5` containing all four fields with `completed` set to `true`, then a `PATCH` containing only `{"completed":true}`. Compare the responses.

**Solution 5.**

```bash
curl -i -X PUT https://jsonplaceholder.typicode.com/todos/5 \
  -H "Content-Type: application/json" \
  -d '{"id":5,"title":"Replaced","completed":true,"userId":1}'

curl -i -X PATCH https://jsonplaceholder.typicode.com/todos/5 \
  -H "Content-Type: application/json" \
  -d '{"completed":true}'
```

**Plain-language explanation:** Both return `200`. The `PUT` response contains exactly the four fields you sent (title is "Replaced"). The `PATCH` response contains the **original** title merged with your change, so the fields you did not send are still present and unchanged, and only `completed` is `true`. That visible difference in the responses is the practical meaning of replace versus partial update. (JSONPlaceholder does this merge in the response even though nothing is stored.)

---

**Exercise 6: Delete and reason about idempotency.**
Run `DELETE /todos/5` twice and then `GET /todos/5`. Predict the three results on a real API, then record what JSONPlaceholder does.

**Solution 6.**

```bash
curl -s -o /dev/null -w "%{http_code}\n" -X DELETE https://jsonplaceholder.typicode.com/todos/5
curl -s -o /dev/null -w "%{http_code}\n" -X DELETE https://jsonplaceholder.typicode.com/todos/5
curl -s -o /dev/null -w "%{http_code}\n" https://jsonplaceholder.typicode.com/todos/5
```

**Plain-language explanation:** On JSONPlaceholder you will see `200`, `200`, `200`, because nothing is ever removed. On a real API, the prediction is `204`, then `404` (or `204`), then `404`. The state after the first and second delete is the same (the todo is absent), which proves the idempotent-state idea, even though the second status may differ.

---

**Exercise 7: Trigger a 405 and read the Allow header.**
Send `POST` to `https://httpbin.org/get` and `DELETE` to `https://httpbin.org/get`. Identify the status and the allowed methods.

**Solution 7.**

```bash
curl -i -X POST https://httpbin.org/get
curl -i -X DELETE https://httpbin.org/get
```

**Plain-language explanation:** Both return `405 Method Not Allowed`, and the `allow` header lists `GET, HEAD, OPTIONS`. The endpoint exists (so it is not `404`) but does not accept those verbs. A test for a destructive verb on a collection should look exactly like this: assert `405` and assert the `Allow` header does not contain `DELETE`.

---

**Exercise 8: Use HEAD and OPTIONS.**
Run `HEAD` on `/posts/1` and `OPTIONS` on `https://httpbin.org/anything`. State what each tells you and why neither returns a normal body.

**Solution 8.**

```bash
curl -I https://jsonplaceholder.typicode.com/posts/1
curl -i -X OPTIONS https://httpbin.org/anything
```

**Plain-language explanation:** The `HEAD` response shows `200` and headers such as `content-type` and `content-length`, but no body, because `HEAD` by definition returns only headers. The `OPTIONS` response carries an `allow` header listing the supported methods and no meaningful body, because its job is to describe capabilities. Both are safe: neither changes any data.

---

**Exercise 9: Design a test table.**
For `POST /users` with required fields `name` (1 to 50 characters) and `email` (unique, valid format), write at least eight test cases covering positive, negative, boundary, and security categories.

**Solution 9.**

| # | Category | Input | Expected |
|---|----------|-------|----------|
| 1 | Positive | `name` "Ada", unique valid `email` | `201`, `id` returned, no password in body |
| 2 | Positive | Read-back of the new `id` | `200`, same name and email |
| 3 | Negative | `name` missing | `400` / `422` naming `name` |
| 4 | Negative | `email` "not-an-email" | `400` / `422` |
| 5 | Negative | Same `email` as an existing user | `409` |
| 6 | Boundary | `name` of 1 character | `201` |
| 7 | Boundary | `name` of exactly 50 characters | `201` |
| 8 | Boundary | `name` of 51 characters | `400` / `422` |
| 9 | Boundary | `name` empty string | `400` / `422` |
| 10 | Security | `name` `<script>alert(1)</script>` | Stored as text or rejected, no `500` |
| 11 | Security | Extra field `"role":"admin"` | Ignored or rejected; read-back shows normal role |

**Plain-language explanation:** Rows 6 to 9 test the edges of the length rule, 1 and 50 as the valid extremes and 0 and 51 as the first invalid values. Row 5 tests the uniqueness rule. Rows 10 and 11 are the security-minded checks for script injection and mass assignment. A strong answer includes at least one case from each category, and each case states an exact expected result rather than "works".

---

**Exercise 10: Write the full lifecycle plan with assertions.**
Write the six-step lifecycle for `/todos` as a table of method, URL, body, and assertions.

**Solution 10.**

| Step | Request | Body | Assertions |
|------|---------|------|------------|
| 1 | `POST /todos` | `{"title":"Water plants","completed":false,"userId":1}` | Status `201`; body has `id`; title equals "Water plants"; save `id` |
| 2 | `GET /todos/{id}` | none | Status `200`; title equals "Water plants"; `completed` is `false` |
| 3 | `PUT /todos/{id}` | `{"id":{id},"title":"Water plants","completed":true,"userId":1}` | Status `200` or `204` |
| 4 | `GET /todos/{id}` | none | Status `200`; `completed` is `true`; title unchanged |
| 5 | `DELETE /todos/{id}` | none | Status `204` or `200` |
| 6 | `GET /todos/{id}` | none | Status `404` |

**Plain-language explanation:** The `{id}` placeholder is the value saved in step 1 and reused. Every write is followed by a read that confirms the effect, and the final `404` is the passing outcome. Because the test deletes what it creates, it can be re-run without leaving data behind.

---

**Exercise 11: Spot the defect.**
A tester reports: "`POST /orders` with an empty cart returned `200` and `{"success": false, "message": "Cart empty"}`." Then: "`GET /users/3` returns a field `passwordHash`." Then: "`DELETE /users/3` returned `204`, but `GET /users/3` still returns `200`." Classify each and state the expected behaviour.

**Solution 11.** The first is a **wrong status code** defect. A failed validation should return `400` or `422`, so the `200` fools any client or test that only checks the status. The second is a **sensitive data exposure** defect: the API must never return password material, even hashed, and the field should be removed from the response. The third is a **false success** defect: the server claimed the delete worked but kept the data, so either the delete is not applied or a cache is serving stale data, and the expected result is `404`. **Plain-language explanation:** In each case the symptom points to a broken promise (status codes must reflect reality, responses must hide secrets, and a successful delete must remove the resource), and the follow-up `GET` is what exposed the third.

---

**Exercise 12: Decide the right method.**
Choose the method and expected success code: (a) change only a customer's phone number; (b) register a new customer; (c) fetch an invoice; (d) replace the whole address book entry; (e) remove a coupon; (f) check whether an image exists without downloading it.

**Solution 12.** (a) `PATCH`, `200` or `204`, since only one field changes. (b) `POST` to the collection, `201`. (c) `GET`, `200`. (d) `PUT`, `200` or `204`, since the whole record is replaced. (e) `DELETE`, `204`. (f) `HEAD`, `200` if it exists or `404` if not. **Plain-language explanation:** The reasoning is to ask what the intent is (read, create, replace, partially change, remove, or inspect metadata), then pick the verb whose promise matches.

---

**Reflection question.** Which of the calls above would be dangerous to retry blindly after a network timeout, and why? **Answer:** The `POST`, because it is not idempotent. If the first attempt actually succeeded, a retry creates a duplicate. The `GET`, `PUT`, and `DELETE` are safe to retry because repeating them leaves the same state.

### 18. Self-Check Quiz

Answer each question before checking the key.

1. Which method is defined as both safe and idempotent: `POST`, `PUT`, `GET`, or `PATCH`?
2. You send the same `POST /orders` three times to a real API. How many orders do you expect, and why?
3. After a successful `DELETE`, what should a `GET` of the same resource return?
4. What is the difference between `PUT` and `PATCH` when the body contains only one field?
5. What is the difference between `404` and `405`?
6. Which header must accompany a `405` response, and what does it contain?
7. A `POST` returns `201`. Why is that not enough proof that the data was saved?
8. Why does JSONPlaceholder not let you verify a create-then-read test?
9. What is an idempotency key for?
10. What does `If-Match` with a stale `ETag` cause the server to return?
11. Why is `DELETE /users` (the whole collection) a valuable negative test?
12. What is the purpose of `HEAD`, and what is missing from its response?

**Answer key.**

1. `GET`. It reads only, so it changes nothing, and repeating it has no further effect.
2. Three separate orders (usually with three IDs), because `POST` is not idempotent and each call creates a new resource.
3. `404 Not Found`, because the resource no longer exists. A `200` would indicate a defect.
4. `PUT` replaces the resource, so the omitted fields are reset or removed (or the request is rejected). `PATCH` changes only the given field and leaves the rest untouched.
5. `404` means nothing exists at that URL. `405` means the URL exists but does not support the method used.
6. The `Allow` header, listing the methods the endpoint does support, for example `Allow: GET, POST`.
7. Because `201` is the server's claim. A bug, a rolled-back transaction, or fake behaviour could mean nothing was stored. Only a follow-up `GET` proves it.
8. Because it fakes writes: it returns realistic success responses but never stores anything, so the read-back returns `404` or the original data.
9. It makes a non-idempotent `POST` safe to retry. The server uses the unique key to return the saved result of the first attempt instead of creating a duplicate.
10. `412 Precondition Failed`, with no change made, because the stored version no longer matches the version the client based its change on.
11. Because a correct API should refuse it with `405`. If it succeeds, it could erase all data, so the test guards against a catastrophic defect.
12. `HEAD` gives the status and headers of a `GET` cheaply, for example to check existence or size. The response has no body.

### 19. Glossary

**API (Application Programming Interface):** A defined way for programs to talk to each other, here over HTTP.

**Cacheable:** A response that a browser or intermediary may store and reuse for later identical requests.

**CRUD:** Create, Read, Update, Delete, the four basic data operations.

**Content-Type:** A header describing the format of the message body, such as `application/json`.

**ETag:** A label identifying a particular version of a resource, used for caching and for conditional requests.

**Idempotent:** Describes a method whose repeated identical calls leave the server in the same state as a single call.

**Idempotency key:** A unique client-generated value that lets a server recognise a retried request and avoid repeating its effect.

**Lifecycle test:** A test that creates, reads, updates, and deletes one resource in order to verify all operations cooperate.

**Location header:** A response header giving the address of a newly created resource.

**Mass assignment:** A flaw where a server copies every client-supplied field into a record, including fields the client should not control.

**Method (verb):** The word at the start of a request, such as `GET`, naming the requested action.

**Method override:** A trick that lets a `POST` request ask the server to treat it as another method.

**Payload / body:** The data carried in a request or response message.

**Preflight:** An automatic `OPTIONS` request a browser sends before certain cross-origin calls.

**Representation:** The data format in which a resource is shown, usually JSON.

**Resource:** Any thing an API exposes at a URL, such as a user, order, or todo.

**Safe method:** A method defined as read-only, which does not ask the server to change anything.

**Soft delete:** Marking a record as deleted without physically erasing it.

**Stateless:** Each request is independent, and the server does not remember earlier requests.

**Status code:** The three-digit number in a response that summarises the outcome.

---

## Summary

- An HTTP method is the verb that tells the server what to do with the resource named by the URL. `GET` reads, `POST` creates, `PUT` replaces, `PATCH` partially updates, and `DELETE` removes.
- **Safe** means read-only, **idempotent** means repeating has the same effect on state as doing it once, and **cacheable** means a response may be stored and reused. `GET` is safe, idempotent, and cacheable. `PUT` and `DELETE` are idempotent. `POST` is neither safe nor idempotent. `PATCH` is not guaranteed idempotent.
- Typical success codes are `200` for reads and updates, `201` for creation, and `204` for success without a body. Typical failures are `400` or `422` for bad input, `401` or `403` for authentication and permission problems, `404` for missing resources, `405` for the wrong method, `409` for conflicts, and `415` for the wrong content type. A `500` caused by bad input is always a defect.
- `PUT` replaces the whole resource and can wipe omitted fields, while `PATCH` changes only what you send.
- `HEAD` returns headers only, `OPTIONS` reports what is allowed, and `405` must carry an `Allow` header.
- Method override and idempotency keys are advanced ideas to recognise: override is a security risk, and idempotency keys make `POST` safe to retry. `ETag` with `If-Match` prevents lost updates by returning `412`.
- A status code alone is never enough: confirm with a follow-up `GET`. The CRUD lifecycle test, create, read, update, read, delete, read, is the foundational API test pattern, and you will build it in Postman later today and in Python tomorrow.
- JSONPlaceholder fakes writes, so use it to learn commands and use a real, storing API to validate behaviour.

## Additional Resources

- MDN Web Docs, *HTTP request methods*: https://developer.mozilla.org/en-US/docs/Web/HTTP/Methods
- MDN Web Docs, *Idempotent (glossary)*: https://developer.mozilla.org/en-US/docs/Glossary/Idempotent
- MDN Web Docs, *HTTP response status codes*: https://developer.mozilla.org/en-US/docs/Web/HTTP/Status
- RFC 9110, *HTTP Semantics* (the official definition of methods, safe, idempotent, and status codes): https://www.rfc-editor.org/rfc/rfc9110
- JSONPlaceholder guide: https://jsonplaceholder.typicode.com/guide/
- httpbin, an HTTP request and response service: https://httpbin.org/
- curl documentation: https://curl.se/docs/manpage.html
- Postman Learning Center, *Send your first request*: https://learning.postman.com/docs/getting-started/first-steps/sending-the-first-request/
