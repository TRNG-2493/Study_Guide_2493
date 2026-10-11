# HTTP Messages

## Learning Objectives

By the end of this lesson you will be able to:

- Explain what HTTP and HTTPS are, why they exist, and why nearly every modern application depends on them.
- Describe in plain language how TLS protects an HTTPS conversation, and what a certificate is.
- Describe the client-server model and walk through the full request-response cycle, including DNS, connection, request, response and close.
- Break any URL into its scheme, host, port, path, query string and fragment, and explain what each part is used for.
- Read and write the parts of an HTTP **request**: the request line, the headers, the blank line and the body.
- Read and write the parts of an HTTP **response**: the status line, the headers and the body.
- Recognise all five status code families and recall many individual status codes, what each one means, and when a real server produces it.
- Explain, at an awareness level, how HTTP/1.1, HTTP/2 and HTTP/3 differ and why the *message* you read stays the same.
- Explain what "stateless" means, and describe how cookies and tokens give a stateless protocol the appearance of memory.
- Recognise common content types and body encodings, such as JSON, form data, multipart and plain text, and match each to its `Content-Type` header.
- Explain "safe" and "idempotent" methods as a preview of the lessons that follow later today.
- Use `curl` with the options `-v`, `-i`, `-I`, `-X`, `-H` and `-d` to send requests and inspect the raw messages that come back.
- Type a raw HTTP request by hand into a network connection and read the raw reply.
- Diagnose failing exchanges by reading the messages, and avoid the most common beginner mistakes.

---

## Why This Matters

This week's epic is to extend your Project 2 Test Automation Framework with **API testing** (Postman today, Python `requests` tomorrow, mocking on Wednesday), then accessibility and MCP testing on Thursday, and finally a **CI/CD pipeline** on Friday. Every one of those activities rests on the same foundation. An API test is nothing more than a program that sends an HTTP message and checks the HTTP message that returns. A pipeline that runs your API tests is nothing more than a machine that does this automatically, over and over, every time someone changes the code.

Think of HTTP messages as the letters that applications mail to each other. Postman, Python scripts, browsers, mobile apps and CI jobs all do the same thing underneath: they write a letter (a **request**), address it to a place (a **URL**), and read the reply (a **response**). If you cannot read the letter, you cannot tell why the reply was wrong. When you can read it, most bugs reveal themselves immediately.

Here are three examples of how this plays out in real testing work:

A test fails with the message "expected 200 but got 401". If you understand status codes you know at once that the server rejected the credentials, so you look at the `Authorization` header you sent and not at the database.

A test fails with "JSONDecodeError: Expecting value". If you understand that the `Content-Type` of the response tells you the format of the body, you check that header, discover it says `text/html`, open the body, and find an HTML error page from a reverse proxy. The problem was never the JSON parsing; the server was unreachable behind the proxy.

A tester reports a defect saying "login is broken". A tester who can read HTTP attaches the raw request and response to the defect report. The developer sees immediately that the request body was sent with the wrong `Content-Type`, and the defect is fixed in ten minutes rather than a day.

This is why we begin on Monday with messages, before opening any tool. Tools such as Postman hide the raw text behind friendly buttons. They are wonderful, but when something goes wrong you must be able to see through the buttons to the message beneath. Today's first lesson gives you that x-ray vision. The lessons after it (REST fundamentals, the individual methods, Postman collections, query parameters, headers and Postman variables) will each zoom in on one part of what you learn here. In this lesson we paint the whole picture, and where a later lesson will go deeper we say so and keep our own explanation short.

---

## The Concept

### 1. What Is HTTP?

**HTTP** stands for **HyperText Transfer Protocol**. A *protocol* is an agreed set of rules for communication. Humans use protocols all the time without thinking about it. When you answer a phone you say "Hello", the caller says who they are, they ask for something, you reply, and eventually both say goodbye. If one side broke these rules, for example by hanging up mid-sentence or speaking before the other picked up, the conversation would be confusing. HTTP is the same kind of agreement between two programs: it defines how one program asks another for something over a network, and how the second program must format its answer so the first program can understand it.

HTTP was invented around 1990 by Tim Berners-Lee at CERN to fetch linked text documents ("hypertext", which is where the "HyperText" in the name comes from). Those documents were the first web pages. Over time people noticed that the same simple "ask and answer" rules could carry any kind of data, not just pages, so HTTP grew into the general-purpose messaging language of the internet. Today HTTP carries JSON for mobile apps, images, video segments, payment confirmations, login tokens, weather forecasts, and the conversations that happen between the many small services inside a large company. When this course says "API testing", it almost always means testing a program that speaks HTTP.

Three properties of HTTP are worth memorising, because they explain almost everything else in this lesson.

First, HTTP is **text based** (in its classic form). You can write an HTTP request with a keyboard, and you can read an HTTP response with your eyes. This is unusual for a network protocol and is exactly why it is so friendly for learning and for debugging. (Newer versions encode the same messages in a compact binary form on the wire, but tools translate this back to the same readable structure for you, as we explain in section 12.)

Second, HTTP is **request-response**. One side asks, the other side answers. The answering side never speaks first.

Third, HTTP is **stateless**. Each request stands alone. We will spend a full section on this because it affects how every test you write must be designed.

HTTP normally runs on top of another protocol called **TCP**, which makes sure the bytes of the conversation arrive complete and in order. You do not need to understand TCP deeply, only to know that before any HTTP messages are sent, the client first opens a TCP connection to the server, a bit like dialling a phone number and waiting for the other side to pick up.

### 2. What Is HTTPS, and What Is TLS?

**HTTPS** is HTTP plus protection. The final "S" stands for *Secure*. Every HTTPS message is exactly the same text structure as an HTTP message, but before it travels across the network it is **encrypted**, so that anyone listening on the network (for example, other people on the same café Wi-Fi) sees only scrambled bytes. The encryption is provided by a separate protocol called **TLS** (Transport Layer Security). You may also hear the older name **SSL**; SSL is the obsolete predecessor, and people still say "SSL" out of habit, but modern systems use TLS.

TLS gives you three separate guarantees, and it is worth keeping them distinct because testers meet each of them in different kinds of failures:

1. **Confidentiality.** Nobody in the middle can read the messages. The data is encrypted.
2. **Integrity.** Nobody in the middle can alter the messages without being detected. If a single byte is changed in transit, the receiver notices.
3. **Authentication of the server.** The client can verify that it really is talking to `api.example.com` and not to an impostor pretending to be that server.

The third guarantee is delivered by a **certificate**. A certificate is a small digital document, issued to the server by an organisation called a **Certificate Authority** (CA), which says, in effect, "I have checked, and this public key really belongs to `api.example.com`". Your operating system and browser come with a built-in list of CAs that they trust. When a server presents its certificate, the client checks that a trusted CA signed it, that the certificate is for the right host name, and that it has not expired.

Here is the TLS handshake in plain language, at awareness level. After the TCP connection is open and *before* any HTTP message is sent, the client says "hello, here are the encryption methods I support". The server replies with its choice and its certificate. The client checks the certificate. Both sides then use some clever mathematics to agree on a shared secret key without ever sending the key itself over the wire. From that moment, everything flows encrypted with that key. Only then does the client send its first HTTP request, now protected. All of this typically takes a few milliseconds and happens invisibly.

**Why testers care about TLS.** You will meet TLS in practice in the following ways:

- Test environments sometimes use *self-signed* certificates, which no trusted CA has vouched for. Your tool will refuse to connect and report a certificate error, such as `curl: (60) SSL certificate problem: self-signed certificate`. The proper fix is to install the test CA certificate on the test machine. Many beginners "fix" it by turning verification off (`curl -k`), which is acceptable for a throwaway local experiment but dangerous as a habit, because it removes the third guarantee entirely and would hide a real attack. In an automated suite, disabling verification should always be a deliberate, documented decision for one specific test environment and never the default.
- Certificates expire. A surprising number of real production outages, and of mysterious "all tests suddenly fail overnight" mornings, are caused by an expired certificate.
- The scheme in the URL matters. `http://` goes to port 80 and is unencrypted. `https://` goes to port 443 and is encrypted. Sending an HTTPS request to an HTTP-only port (or vice versa) produces confusing errors.

In the rest of this lesson we show messages as plain text. Remember that over HTTPS the text is the same; it is simply encrypted in transit and decrypted at each end. Tools such as `curl -v` and Postman show you the decrypted text, which is why you can read it.

### 3. The Client-Server Model

HTTP involves two roles:

- A **client** is the program that *starts* the conversation by asking for something. Examples: a web browser, Postman, a mobile app, a Python test script, a CI job running `curl`.
- A **server** is the program that *waits* for incoming requests, does the work, and sends back an answer. Examples: the back end of an online shop, a payments service, a weather API.

Note that "client" and "server" describe *roles in one conversation*, not types of machine. The very same program can be a server in one conversation and a client in another. For example, when you load your bank's web page, the bank's web server may itself act as a *client* and send a request to an internal accounts service to fetch your balance. Chains like this are very common in modern systems, and they matter for testing: a failure that you see in one response may have started in a second conversation you cannot see.

**Analogy: a restaurant.** You (the client) read the menu and tell the waiter what you want. The waiter carries the order to the kitchen (the server). The kitchen prepares the food and the waiter brings back the result. You never walk into the kitchen yourself; you interact only through the agreed process of ordering. If you ask for something not on the menu, the waiter returns with a polite refusal rather than a meal. That refusal is the equivalent of an HTTP error response.

As a test automation engineer you are *pretending to be the client* so you can check whether the kitchen behaves correctly, including the unhappy cases: ordering a dish that does not exist, ordering with no money, ordering in a language the waiter does not speak. An API tester spends at least as much time on these unhappy cases as on the happy ones.

### 4. The Request-Response Cycle in Detail

Every HTTP interaction is a pair of messages. The client sends one **request**; the server replies with one **response**. Let us follow one complete cycle slowly, because each step is a place where something can go wrong and a place where a test can detect it. Suppose you type `https://jsonplaceholder.typicode.com/users/1` into a client.

**Step 1: DNS lookup.** Computers find each other using numeric addresses called IP addresses, such as `104.21.0.10`. Humans prefer names. The **Domain Name System (DNS)** is the global phone book that converts a name like `jsonplaceholder.typicode.com` into one or more IP addresses. If DNS fails, you get an error such as `curl: (6) Could not resolve host`. No HTTP message has been sent at all at this point. This is a common beginner confusion: a typo in the host name is *not* an HTTP error.

**Step 2: TCP connection.** The client opens a connection to that IP address on the right port (443 for HTTPS). If the server is down or a firewall blocks the port, you get an error such as `Connection refused` or `Connection timed out`. Again, no HTTP message was exchanged yet.

**Step 3: TLS handshake (HTTPS only).** As described in section 2, the two sides agree on encryption. Certificate problems appear here.

**Step 4: The request is sent.** Now the client writes its HTTP request message and sends it.

**Step 5: The server processes the request.** The server reads the request, decides what is being asked, checks permissions, perhaps reads or writes a database, and builds a response.

**Step 6: The response is returned.** The server sends back exactly one response message. A response is *always* returned if the server is alive and reachable, even when the answer is "something went wrong". That is what status codes are for.

**Step 7: The connection is closed or reused.** In the oldest versions of HTTP the connection was closed after each response. Modern versions keep it open for a while so that further requests can reuse it, which is much faster. You will see this as the header `Connection: keep-alive` in HTTP/1.1.

A simple diagram of the heart of it:

```
 Client                                        Server
   |                                              |
   |  ---------- 1. HTTP Request ------------->   |
   |                                              |  (look up data, apply rules,
   |                                              |   read or write database)
   |  <--------- 2. HTTP Response -------------   |
   |                                              |
```

Notice three consequences that will guide everything you do as a tester.

There is **exactly one response per request**. If your test sent one request, it will receive one response (or a network failure, which is a different kind of problem to the one we are studying). An "error" such as 404 is still a complete, valid response.

The **server never speaks first**. A server cannot push a response unless the client asked. (Technologies for server-initiated messages, such as WebSockets, exist, but they are outside this week's scope.)

The **client controls what it asks for**, and therefore a tester controls the whole experiment. You decide the method, the address, the headers and the body. If you want to find out what the server does when a required field is missing, you simply omit it. This total control is what makes API testing so powerful and so repeatable compared with clicking through a user interface.

### 5. URLs: The Address in Every Request

A **URL** (Uniform Resource Locator) is the address that tells the client where to send a request and what it wants there. Understanding each part of a URL is essential because you will construct URLs by hand in Postman, in `curl` and in code all week. Take this full example:

```
https://api.example.com:8443/v1/users/42/orders?status=open&limit=10#summary
\___/   \_____________/ \__/ \_______________/ \_______________/ \______/
scheme       host       port       path             query         fragment
```

**Scheme (`https`).** This is everything before `://`. It names the protocol to use. For this course it will be `http` or `https`. The scheme also implies a default port.

**Host (`api.example.com`).** The name of the server to contact. DNS turns it into an IP address. The host is also sent *inside* the request as the `Host` header, because a single machine may serve many websites, and the server needs to know which one you meant.

**Port (`8443`).** The numbered "door" on the server machine to knock on. If you leave it out, the default applies: 80 for `http` and 443 for `https`. Development and test servers very often use other ports, such as `3000`, `5000` or `8080`, so you will often type the port explicitly, as in `http://localhost:5000/api/users`.

**Path (`/v1/users/42/orders`).** Identifies *which resource* on the server you want. It looks like a folder path. In a well-designed API the path is made of nouns, and a number in the path often identifies one specific item, so `/v1/users/42/orders` reads naturally as "the orders belonging to user 42, in version 1 of the API". Paths are case-sensitive on most servers, so `/Users/42` and `/users/42` can be different addresses. Later today, the lessons on REST fundamentals and on query parameters and path variables go much deeper into designing and using paths.

**Query string (`status=open&limit=10`).** Everything after the `?` and before any `#`. It is a list of `name=value` pairs joined by `&`. Query strings are typically used to filter, sort, search or page through results. In this example the client asks for orders whose status is open, limited to ten of them. The query string is part of the request target and the server does see it.

**Fragment (`summary`).** Everything after `#`. The fragment is used only by browsers (for example, to scroll to a heading on a page). It is **never sent to the server**. This surprises many beginners: if your test puts important information after a `#`, the server will never receive it.

**Special characters and percent-encoding.** URLs may only contain a limited set of characters. A space, for example, is not allowed. Characters outside the safe set must be written as a percent sign followed by two hexadecimal digits, which is called **percent-encoding** or URL encoding. A space becomes `%20`, an ampersand becomes `%26`, a plus sign becomes `%2B`, and a slash inside a value becomes `%2F`. So searching for the phrase `fish & chips` would be written as `?q=fish%20%26%20chips`. If you forget to encode an ampersand inside a value, the server will think it marks the start of a new parameter, and your test will behave strangely. Good tools encode for you; raw `curl` does not always.

### 6. Anatomy of an HTTP Request

A request has up to four parts, always in this order: the **request line**, the **headers**, a **blank line**, and an optional **body**. Here is a real request that asks for to-do item number 1 from JSONPlaceholder, a free public practice API:

```http
GET /todos/1 HTTP/1.1
Host: jsonplaceholder.typicode.com
Accept: application/json
User-Agent: qea-training/1.0

```

Here is what each line does.

`GET /todos/1 HTTP/1.1` is the request line. It says what the client wants to do (`GET`, meaning read), to which resource (`/todos/1`), and which version of the HTTP rules it is using (`HTTP/1.1`).

`Host: jsonplaceholder.typicode.com` names the server being addressed. In HTTP/1.1 this header is mandatory. A request without it is rejected, normally with `400 Bad Request`.

`Accept: application/json` tells the server which formats the client is willing to receive. Here the client says it wants JSON.

`User-Agent: qea-training/1.0` says what kind of client is calling. Servers use it for logging and sometimes for statistics. Some servers also block requests with no `User-Agent`.

The final empty line is part of the message. It signals "headers finished". This empty line is required even for a request with no body.

#### 6.1 The Request Line

The request line has exactly three pieces separated by single spaces:

```
GET /todos/1 HTTP/1.1
```

The **method** is the action requested. The five you will use constantly are `GET` (read), `POST` (create or submit), `PUT` (replace), `PATCH` (partially change) and `DELETE` (remove). Others exist, such as `HEAD` (like `GET` but returning headers only) and `OPTIONS` (asking what is allowed). Method names are case-sensitive and are written in capitals. The lesson "GET, POST, PUT and DELETE" later today explains each in full, so here we only need to know that the method tells the server what to *do* to the resource.

The **request target** is normally the path plus the query string, such as `/todos?userId=1`. Notice that the scheme and host are not repeated here, because the host goes in the `Host` header.

The **HTTP version** is `HTTP/1.1` in the plain-text examples in this lesson.

#### 6.2 Request Headers

Headers are `Name: value` pairs, one per line. They carry **metadata**: information *about* the request, as opposed to the data itself. Header names are case-insensitive (`Content-Type` and `content-type` mean the same thing), though traditional capitalisation is used for readability. A few you will see in almost every request:

`Host` says which server is being addressed. `Accept` says which response formats the client can handle. `Content-Type` says the format of the body being sent. `Content-Length` says how many bytes of body follow. `Authorization` carries credentials. `User-Agent` identifies the client program. `Cookie` returns cookies the server previously issued.

A full lesson on headers follows later today, so for now remember the guiding sentence: *headers describe the message and control how it is handled*.

#### 6.3 The Blank Line

After the last header there is one empty line. Technically it is the two characters carriage return and line feed (written `\r\n`) appearing twice in a row, once to end the last header line and once to make the empty line. This blank line is how the server knows exactly where the headers end and the body begins. When you type raw requests by hand, as we do in section 15, forgetting this blank line makes the server wait forever, believing you have more headers to send. Many beginners are puzzled by a raw request that "hangs"; this is the usual reason.

#### 6.4 The Request Body

The body is the data being sent to the server. A `GET` request normally has no body, because you are only asking to read something. A `POST` request, which creates something, carries its data in the body:

```http
POST /posts HTTP/1.1
Host: jsonplaceholder.typicode.com
Content-Type: application/json
Content-Length: 51

{"title":"Hello","body":"My first post","userId":1}
```

The new header `Content-Type: application/json` tells the server how to interpret the body: as JSON. Without it, the server may not know how to read the data and may reject the request or, worse, misread it. The header `Content-Length: 51` says that exactly 51 bytes of body follow, which is the number of characters in the JSON text shown (you can count them with `wc -c`). The server uses this number to know when the body ends, so that it neither stops reading early nor waits for more. Most tools calculate `Content-Length` for you; you only need to calculate it yourself when typing a raw request.

### 7. Anatomy of an HTTP Response

The server replies with its own message made of three parts: a **status line**, **headers**, and an optional **body**, again separated by a blank line between the headers and the body. Here is a realistic response from JSONPlaceholder (headers abbreviated to the most useful):

```http
HTTP/1.1 200 OK
Content-Type: application/json; charset=utf-8
Content-Length: 83
Cache-Control: max-age=43200

{
  "userId": 1,
  "id": 1,
  "title": "delectus aut autem",
  "completed": false
}
```

#### 7.1 The Status Line

```
HTTP/1.1 200 OK
```

The status line has three pieces. The **HTTP version** (`HTTP/1.1`) says which rules the server is following. The **status code** (`200`) is a three-digit number that summarises the outcome. The **reason phrase** (`OK`) is a short human-readable label. Automated tests should always check the numeric code and never the phrase: the phrase is purely informational, can differ between servers (for example, `200 OK` versus `200 Success`), and in HTTP/2 and HTTP/3 it is not transmitted at all. That is why `curl -v` shows only `HTTP/2 200` for an HTTP/2 response.

#### 7.2 Response Headers

Response headers describe the response. `Content-Type: application/json; charset=utf-8` says the body is JSON text encoded as UTF-8. `Content-Length` gives the body size in bytes. `Cache-Control` says how long the response may be reused without asking again. Many others appear in real responses: `Date`, `Server`, `Set-Cookie`, `Location`, `ETag`, `Retry-After`, `Access-Control-Allow-Origin` and so on. The response headers are often where the real clue to a bug lies, so never ignore them.

#### 7.3 The Response Body

The body is the actual data being returned: here, a JSON object describing a to-do item. Bodies may also be HTML (a web page), XML, plain text, images, PDF files, or empty. For example, a successful delete often returns an empty body, and a response with status `204 No Content` is not allowed to have a body at all.

### 8. Status Codes: The Complete Picture

The status code is the single most important summary of what happened, so we spend a long section on it. The first digit tells you the **family**; the remaining two digits give the specific meaning. Memorise the families first, because even if you meet a code you have never seen, its family tells you who is at fault and what kind of action is expected.

| Range | Family | Plain meaning |
|-------|--------|---------------|
| 1xx | Informational | "I received it; keep going." |
| 2xx | Success | "It worked." |
| 3xx | Redirection | "Look somewhere else." |
| 4xx | Client error | "You made a mistake." |
| 5xx | Server error | "I failed." |

Tester's rule of thumb: a 4xx usually means the problem is in the *request* you sent, while a 5xx usually means the problem is in the *server*. A well-built API should never return 500 for bad user input; it should detect the bad input and return a clean 4xx. Finding an input that provokes a 500 is a classic and valuable testing win, because it proves the server did not handle the situation gracefully.

We now walk through each family with its most important codes. Later in the week ("Status code validation", Tuesday) you will learn how to assert on these in automated tests; today we only learn to recognise them.

#### 8.1 1xx: Informational

These are interim responses. As a tester you will rarely see them, because tools handle them for you, but you should know they exist.

**100 Continue.** A client that is about to upload a large body can first send the headers with `Expect: 100-continue` and wait. If the server is willing to accept the upload, it answers `100 Continue` and the client then sends the body. This avoids wasting bandwidth uploading a huge file that the server would reject anyway for, say, missing credentials.

**101 Switching Protocols.** The server agrees to change to a different protocol on the same connection. The most common case is the upgrade from HTTP to WebSocket for real-time features such as chat.

**103 Early Hints.** The server sends a preliminary hint (for example, a list of files the browser will soon need) before the final response is ready. This is a performance feature and mostly of interest to browsers.

#### 8.2 2xx: Success

The request was received, understood and accepted. But "success" comes in several flavours, and a good test checks the *specific* code, not merely "some 2xx".

**200 OK.** The general-purpose success. For `GET` it means "here is what you asked for, in the body". For other methods it means the action worked and the body describes the result. Example: `GET /users/1`.

**201 Created.** A new resource was created as the result of the request. This is the correct response to a successful `POST` that adds a record. Servers commonly also send a `Location` header giving the address of the new resource, and often include the created item in the body. Example: `POST /posts` on JSONPlaceholder returns 201 with the new item and an `id` of `101`.

**202 Accepted.** The request was accepted for processing, but the work is not finished yet. This is used for slow background jobs, such as generating a large report. The client is typically given a way to check progress later. A tester must not assume the work is complete when they see 202.

**204 No Content.** The action succeeded, and there is deliberately nothing to send back. It is common for successful `DELETE` and some `PUT` operations. The body must be empty, so a test that tries to parse JSON from a 204 response will crash; this is a classic beginner mistake.

**206 Partial Content.** The server is returning only a slice of the resource because the client asked for a byte range using a `Range` header. Video players and download managers use this to resume downloads or to jump to a point in a file.

#### 8.3 3xx: Redirection

The resource is not at the address you used, or you can save effort by using a copy you already have. The server normally tells you where to go in a `Location` header, and many clients (browsers, `curl -L`, Python `requests`) follow redirects automatically. A test must therefore be conscious of whether it wants to follow a redirect or to assert that the redirect happened.

**301 Moved Permanently.** The resource now lives permanently at the address in `Location`. Search engines and clients may update their records. Typical case: a site moving from `http://` to `https://`, or from an old domain to a new one.

**302 Found.** A temporary redirect. The resource is at a different address *for now*; keep using the original address in future. This is very common after logins ("now go to your dashboard") and in many hand-written servers. Historically, clients changed a `POST` into a `GET` when following a 302, which is why more precise codes were created.

**303 See Other.** After processing your request, the server tells you to fetch a different resource using `GET`. This is often used after a `POST` form submission so that refreshing the result page does not resubmit the form.

**304 Not Modified.** This one is special. The client previously received a copy of the resource with a validator such as an `ETag`, and now asks "has it changed?" using `If-None-Match`. If nothing changed, the server answers 304 with no body, meaning "use your saved copy". It saves bandwidth. Testers see it when caching is involved and are sometimes surprised to receive no body.

**307 Temporary Redirect** and **308 Permanent Redirect.** These are the strict versions of 302 and 301. They require the client to repeat the *same method and body* at the new address. A `POST` redirected with 307 stays a `POST`. APIs prefer these precise codes.

#### 8.4 4xx: Client Errors

The request has a problem and repeating it unchanged will not help. These are the codes API testers meet most, because negative testing means deliberately provoking them.

**400 Bad Request.** The server cannot understand the request because it is malformed or invalid: broken JSON, a missing required field, a value of the wrong type. It is the catch-all for "your request is not acceptable as written". Example: sending `{"name": ` with a missing closing brace.

**401 Unauthorized.** Despite its name, this really means *unauthenticated*: the server does not know who you are, because credentials were missing, expired or wrong. The usual fix is to log in or supply a valid token. A response normally includes a `WWW-Authenticate` header describing what kind of credentials it will accept.

**403 Forbidden.** The server knows exactly who you are, and you are not allowed to do this. The credentials are valid, but the permissions are insufficient. Example: a normal user trying to call an admin-only endpoint. Remember the difference: 401 means "who are you?"; 403 means "I know who you are, and no".

**404 Not Found.** There is nothing at this address. It may be a typo in the path, or an item that does not exist, such as `GET /users/99999`. Some APIs also deliberately return 404 instead of 403 to avoid revealing that a protected resource exists.

**405 Method Not Allowed.** The address exists, but not for that method. For example, sending `DELETE` to an endpoint that only supports `GET`. The response should include an `Allow` header listing the methods that do work.

**406 Not Acceptable.** The server cannot produce a response in any format the client listed in `Accept`. For example, asking for `Accept: application/xml` from an API that only produces JSON.

**408 Request Timeout.** The server gave up waiting for the client to finish sending its request.

**409 Conflict.** The request is valid but conflicts with the current state of the resource. Classic examples: creating a user with an email address that already exists, or editing a record that someone else changed in the meantime.

**410 Gone.** Like 404, but deliberate and permanent: the resource used to exist and has been removed for good.

**413 Content Too Large** (historically *Payload Too Large*). The body exceeds the size the server accepts, such as an oversized file upload.

**415 Unsupported Media Type.** The server does not support the format of the body you sent, usually because of a wrong or missing `Content-Type`. You will use this as a diagnosis in section 19.

**422 Unprocessable Content** (historically *Unprocessable Entity*). The request is syntactically well-formed and the server understood its format, but the *meaning* is invalid. For example, valid JSON where the `email` field does not look like an email address, or an end date earlier than the start date. Many APIs use 422 for validation errors and reserve 400 for requests that cannot even be parsed, though some APIs use 400 for both. Check the API's documentation to learn its convention.

**429 Too Many Requests.** You have been rate-limited: you sent too many requests in a given time. The response often includes a `Retry-After` header telling you how many seconds to wait. This often catches automated tests that run too fast, and it is a classic cause of tests that pass individually but fail when run together in a pipeline.

#### 8.5 5xx: Server Errors

The request may well have been valid, but the server failed to fulfil it. These are usually defects, or infrastructure problems, and are worth reporting.

**500 Internal Server Error.** The generic "something unexpected broke on the server". Typically caused by an unhandled exception in the server code. This is the number-one status code for a defect report.

**501 Not Implemented.** The server does not support the functionality required to fulfil the request, such as an unknown method.

**502 Bad Gateway.** A server acting as a gateway or proxy received an invalid response from the server behind it. In modern systems this usually means the real application has crashed or is restarting while the front-door proxy is still up.

**503 Service Unavailable.** The server cannot handle requests right now, usually because it is overloaded or down for maintenance. A `Retry-After` header may say when to try again. You will see this in test environments that are still starting up when your pipeline begins testing.

**504 Gateway Timeout.** A gateway or proxy did not receive a response from the server behind it in time. It often points to a very slow back-end operation.

#### 8.6 A Fun One You Can Try: 418

**418 I'm a teapot** is a joke status code from an April Fools' specification, but the free testing service httpbin implements it. Calling `https://httpbin.org/status/418` returns it, which is a safe, handy way to see any status code on demand, because `https://httpbin.org/status/<code>` returns whatever code you ask for. You will use this trick in the practice exercises.

### 9. HTTP Versions at an Awareness Level

You do not need to implement any HTTP version, but you should recognise the names, because they appear in tool output and in discussions about performance.

**HTTP/1.1** (1997, refined in later revisions) is the classic version we have been showing. Messages are plain text. It is still extremely common, especially inside company networks, in development servers and in hand-written examples. It keeps connections open for reuse (`keep-alive`), requires the `Host` header, and processes requests on one connection essentially one after another. A slow response can therefore hold up the ones queued behind it.

**HTTP/2** (2015) keeps the same concepts (methods, status codes, headers, bodies) but changes how they are carried. Messages are encoded in a compact **binary** format instead of text, headers are compressed, and many requests can be sent at the same time over one connection (called **multiplexing**), which removes the queueing problem. In practice browsers use it for almost all HTTPS traffic. In HTTP/2, header names are lowercase, and there is no reason phrase, which is why `curl -v` shows `HTTP/2 200` and `content-type: ...` in lowercase.

**HTTP/3** (2022) again keeps the same message concepts but replaces TCP with a newer transport called **QUIC**, which runs over UDP. It recovers faster from lost network packets and from switching networks (for example, a phone moving from Wi-Fi to mobile data).

The reassuring truth for a tester is this: **the semantics are identical across all three versions**. A `GET` is a `GET`, a 404 is a 404, `Content-Type` is `Content-Type`. Only the wire encoding changes. Your tools negotiate the best version automatically. That is why we can teach with plain-text HTTP/1.1 examples: they show the concepts perfectly, and everything you learn carries across.

### 10. HTTP Is Stateless

HTTP is **stateless**: each request is independent, and the server does not automatically remember anything about earlier ones. If you log in with one request and then ask for your profile with the next, the server has no built-in memory that you logged in. It treats the second request as if it arrived from a stranger.

**Analogy.** Imagine a bank teller with no short-term memory. Every time you come to the window you must show your identification again and state your request afresh. The teller does not hold a grudge or a favour from the previous visit; they simply deal with whatever is in front of them. That is HTTP.

**Why was it designed this way?** Statelessness makes servers simple and scalable. If every request carries everything needed to process it, then any one of a hundred identical servers can answer it, and a server can crash and restart without losing anyone's conversation. This is a huge benefit for large systems.

**But real applications need memory.** A shopping site must know that you are logged in and what is in your basket. The workaround is simple and clever: the *client* carries the memory and presents it with each request. There are two main forms.

**Cookies.** A cookie is a small piece of text the server asks the client to store. The server sends it in a response header called `Set-Cookie`, for example `Set-Cookie: session_id=abc123; HttpOnly; Secure`. From then on, the client automatically adds a `Cookie: session_id=abc123` header to every later request to that server. The server looks up `abc123` in its own records and recognises you. Browsers do this automatically. The memory ultimately lives on the server (the session record), but the key to it travels in each request.

**Tokens.** In API work, a very common alternative is a **token**: a string the server gives you after you log in, which you then send in an `Authorization` header with each request, such as `Authorization: Bearer eyJhbGciOi...`. Some tokens (for example, JSON Web Tokens) carry the information inside the token itself, so the server needs no lookup at all. The details of authentication belong to the lessons that follow (we meet the `Authorization` header in the headers lesson today, and authentication in automated tests on Tuesday); what you must grasp right now is the principle: *the proof of identity travels in every request*.

**What statelessness means for your tests:**

Each test request must carry everything it needs: credentials, identifiers, headers. You cannot rely on "the previous call logged me in" unless your test explicitly stores the token from that call and attaches it to the next one.

Tests can be made independent of each other, which makes them reliable and able to run in any order or in parallel. Wednesday's lesson on test isolation builds on this.

Where state *does* exist, it lives on the server side, in databases and sessions. A record that your `POST` created really does exist afterwards. Your tests must therefore set that data up deliberately and clean it up afterwards. Statelessness is a property of the protocol, not of the application's data.

### 11. Content Types and Body Encodings

A body is just a sequence of bytes. For the receiver to interpret them correctly, the sender must say what kind of data they are. That is the job of the `Content-Type` header, whose value is a **media type** (also called a MIME type) made of a *type* and a *subtype* separated by a slash, optionally followed by parameters such as a character set. Examples include `application/json; charset=utf-8`.

The most important content types for API testing:

**`application/json`.** Structured data in JSON (JavaScript Object Notation), the dominant format of modern APIs. Example body: `{"name":"Priya","role":"tester"}`. JSON is built from objects in curly braces, arrays in square brackets, and values that are strings, numbers, `true`, `false` or `null`. Strings must use double quotes; single quotes are not valid JSON, a very common cause of 400 errors.

**`application/x-www-form-urlencoded`.** The classic format of simple HTML forms: `name=Priya&role=tester`, with special characters percent-encoded. Parameters are joined with `&`, just like a query string, but placed in the body. Servers that expect form data and receive JSON, or the reverse, commonly report 400 or 415 errors.

**`multipart/form-data`.** Used when sending files, and mixed fields and files, in one request. The body is divided into **parts**, each with its own small headers, separated by a boundary string that the sender declares in the header: `Content-Type: multipart/form-data; boundary=----X123`. You do not write these by hand; tools such as `curl -F` build them.

**`text/plain`.** Plain unformatted text.

**`text/html`.** A web page. If you expected JSON and receive this, an error page or login page has probably replaced your real response.

**`application/xml` or `text/xml`.** XML, an older structured format, still common in enterprise and SOAP services.

**`application/octet-stream`.** Arbitrary binary data, such as a downloaded file with no more specific type.

**`image/png`, `image/jpeg`, `application/pdf`** and so on for the obvious file types.

Two headers work as a pair. The **`Content-Type`** header says what the body you are *sending* contains. The **`Accept`** header says what formats you are *willing to receive*. In a conversation these are directions in a single exchange: the request may say "I send you JSON and I would like JSON back", and the response `Content-Type` says what actually came back.

**Character encoding.** The `charset=utf-8` parameter says that text characters are converted to bytes using UTF-8, the near-universal encoding that can represent every language. If the encoding is wrong, accented or non-Latin characters turn into garbled symbols. Testers deliberately include names such as `Zoë`, `Müller` and `李雷` in test data to find such problems.

**Transfer-level encodings.** You may also see `Content-Encoding: gzip`, meaning the body bytes were compressed to save bandwidth. Tools such as `curl --compressed` and Python decompress it for you. And you may see `Transfer-Encoding: chunked`, meaning the body is sent in pieces because the server does not know the total size in advance; in that case there is no `Content-Length`. These are details of delivery, not of meaning, and good tools hide them.

### 12. Safe and Idempotent Methods: A Short Preview

Two vocabulary words describe how methods behave, and testers use them constantly. We introduce them now and the lesson "GET, POST, PUT and DELETE" will examine them in depth.

A method is **safe** if it is meant only to *read*, and not to change anything on the server. `GET` and `HEAD` are safe. It is always acceptable to call them repeatedly while exploring.

A method is **idempotent** if sending the same request many times has the *same effect on the server* as sending it once. `GET`, `PUT` and `DELETE` are idempotent. If you delete item 5 and then delete item 5 again, the end state is identical: item 5 is gone (the second call may return 404, but the server's state did not change further). `POST` is generally *not* idempotent: posting the same new order twice may create two orders. This explains why a double-clicked "Pay" button can charge a customer twice, and why testers check for it.

Keep these two words in mind as you read the next sections; they will make the later lessons feel familiar.

### 13. Hands-On with `curl`

`curl` is a command-line tool that sends HTTP requests and prints the results. It is installed by default on current versions of Windows 10 and 11, macOS and most Linux systems. Because it shows everything, it is the best tool for learning the raw messages. We will use JSONPlaceholder (`jsonplaceholder.typicode.com`) and httpbin (`httpbin.org`), two free public services created for practice. They are shared by many people, so please be considerate and do not send huge numbers of requests. Note that JSONPlaceholder *pretends* to create, update and delete data but does not actually save changes, so every learner sees the same stable data.

> **Windows PowerShell note.** In Windows PowerShell, `curl` can be an alias for a different command, `Invoke-WebRequest`. Type `curl.exe` instead of `curl` to run the real tool, or run the commands in Git Bash. Also, PowerShell treats quotes differently; if a JSON body causes trouble, use Git Bash or put the JSON in a file and use `-d @body.json`. The line-continuation character in the examples below is a backslash (`\`), which works in Bash and Git Bash; in PowerShell use a backtick, and in Windows `cmd.exe` use a caret (`^`).

#### 13.1 The simplest request

```bash
curl https://jsonplaceholder.typicode.com/todos/1
```

```json
{
  "userId": 1,
  "id": 1,
  "title": "delectus aut autem",
  "completed": false
}
```

With no options, `curl` sends a `GET` and prints only the **response body**. This is useful to see the data, but it hides the status code and the headers, which, as we have learned, are the parts that most often explain a failure.

#### 13.2 `-i`: include the response headers

```bash
curl -i https://jsonplaceholder.typicode.com/todos/1
```

Representative output (some headers are omitted, and values such as dates and identifiers will differ):

```
HTTP/2 200
date: Sun, 11 Oct 2026 09:30:12 GMT
content-type: application/json; charset=utf-8
cache-control: max-age=43200
etag: W/"53-hfEnumeNh6YirfjyjaujcOPPT+s"

{
  "userId": 1,
  "id": 1,
  "title": "delectus aut autem",
  "completed": false
}
```

The `-i` option tells `curl` to print the **status line and response headers** followed by the body. Look at the first line, `HTTP/2 200`: that is the status line, showing the protocol version and the status code. Then come the response headers, one per line, each in `name: value` form (lowercase because this is HTTP/2). After the blank line is the body. This is the quickest way to see the headline status code and the `Content-Type` together. Header values such as `date` and `etag` will differ when you run it.

#### 13.3 `-I`: headers only (a HEAD request)

```bash
curl -I https://jsonplaceholder.typicode.com/todos/1
```

```
HTTP/2 200
content-type: application/json; charset=utf-8
cache-control: max-age=43200
```

A capital `-I` sends a **`HEAD`** request instead of `GET`. `HEAD` is exactly like `GET` except that the server must return the headers only, with no body. This is handy for a quick check such as "does this resource exist, and what type is it?" without downloading the whole thing. Be careful to distinguish the two letters: lowercase `-i` means *include headers in the output of a normal request*, while uppercase `-I` means *send a HEAD request*. Some servers handle `HEAD` incorrectly, so if `-I` returns a strange result where `GET` works, that itself is worth noting.

#### 13.4 `-v`: verbose, see both messages

```bash
curl -v https://jsonplaceholder.typicode.com/todos/1
```

Representative output (shortened; the lines beginning with `*` describe connection and TLS steps and vary between machines):

```
*   Trying 104.21.0.10:443...
* Connected to jsonplaceholder.typicode.com (104.21.0.10) port 443
* ALPN: curl offers h2,http/1.1
* TLSv1.3 (OUT), TLS handshake, Client hello (1):
* TLSv1.3 (IN), TLS handshake, Server hello (2):
* SSL connection using TLSv1.3 / TLS_AES_256_GCM_SHA384
* Server certificate:
*  subject: CN=typicode.com
*  SSL certificate verify ok.
* using HTTP/2
> GET /todos/1 HTTP/2
> Host: jsonplaceholder.typicode.com
> User-Agent: curl/8.4.0
> Accept: */*
>
< HTTP/2 200
< content-type: application/json; charset=utf-8
< cache-control: max-age=43200
<
{
  "userId": 1,
  "id": 1,
  "title": "delectus aut autem",
  "completed": false
}
```

The `-v` option is the most educational. Read it in three zones.

Lines beginning with `*` are `curl`'s own commentary about the journey: finding the server, connecting to port 443, negotiating TLS 1.3 and verifying the certificate (`SSL connection using TLSv1.3` and `SSL certificate verify ok` are the lines to look for if you suspect a TLS problem). These correspond to steps 1 to 3 of the request-response cycle in section 4.

Lines beginning with `>` are the **request that `curl` sent**. You can see the request line (`GET /todos/1 HTTP/2`), the `Host` header, a `User-Agent` that `curl` added automatically, and an `Accept: */*` header meaning "I accept any format". The lone `>` is the blank line that ends the request headers.

Lines beginning with `<` are the **response received**. The first is the status line with the status code, followed by the response headers, and the lone `<` is the blank line ending them. Everything after that, without a prefix, is the body.

Memorise this reading rule: **`>` is outgoing, `<` is incoming, `*` is curl talking.** To see HTTP/1.1 text instead of HTTP/2, add `--http1.1` to the command, and the first line becomes `> GET /todos/1 HTTP/1.1`.

If your terminal is noisy, use `curl -sv URL` (silent progress plus verbose) or send the verbose output to a file with `2> verbose.txt`, because `curl` writes verbose information to the error stream.

#### 13.5 `-X`: choose the method

By default `curl` uses `GET`, or `POST` when you provide data with `-d`. The `-X` option states the method explicitly. For example, to delete a post on JSONPlaceholder:

```bash
curl -i -X DELETE https://jsonplaceholder.typicode.com/posts/1
```

```
HTTP/2 200
content-type: application/json; charset=utf-8

{}
```

`-X DELETE` makes `curl` send `DELETE /posts/1`. JSONPlaceholder responds with 200 and an empty JSON object, because it only simulates the deletion. A real API would more typically answer 200 or 204. Notice also what is *not* needed: because there is no body, we send no `Content-Type`. Use `-X` for `PUT`, `PATCH` and `DELETE`; you rarely need it for `GET` and normally need not combine `-X POST` with `-d`, because `-d` already switches to `POST`. (Stating it anyway, as we do below, is harmless and makes the command easier to read.)

#### 13.6 `-H` and `-d`: add a header and send a body

```bash
curl -i -X POST https://jsonplaceholder.typicode.com/posts \
  -H "Content-Type: application/json" \
  -d '{"title":"Hello","body":"My first post","userId":1}'
```

```
HTTP/2 201
content-type: application/json; charset=utf-8
location: https://jsonplaceholder.typicode.com/posts/101

{
  "title": "Hello",
  "body": "My first post",
  "userId": 1,
  "id": 101
}
```

Let us explain each part.

`-i` prints the status line and headers so we can see the status code.

`-X POST` sets the method to `POST`, meaning "create a new item".

`https://jsonplaceholder.typicode.com/posts` is the collection address. We post to the collection, not to a single item, because the server decides the new item's `id`.

`-H "Content-Type: application/json"` adds a request header. Each `-H` adds one header; use several `-H` options for several headers. This header tells the server that the body is JSON.

`-d '{"title":...}'` provides the body. The single quotes protect the inner double quotes from the shell. Notice that `curl` automatically adds a `Content-Length: 51` header and, if you do not specify one, sets `Content-Type: application/x-www-form-urlencoded`, which is why we override it.

The response status is **201 Created**, the correct success code for creation. The server echoes our data back and adds a new `id` of `101`, and a `Location` header pointing at the new item (headers shown are representative). Because JSONPlaceholder is a simulation, requesting `/posts/101` afterwards would return 404; the item was not really stored. This is a good reminder that an API's response says what the server *claims* happened, and real testing verifies the claim by reading the data back.

#### 13.7 Putting it together: three useful extras

`curl -L URL` follows redirects automatically; without `-L`, `curl` stops at the 3xx response and shows it, which is what you want when testing that a redirect occurs.

`curl -s URL` is silent mode, hiding the progress meter, useful in scripts.

`curl -d @body.json URL` reads the body from a file called `body.json`, ideal for long JSON bodies and for avoiding quoting problems on Windows.

### 14. Reading Raw Messages: A Short Practice Guide

Whenever you receive a request/response pair, read it in this fixed order. This routine is what experienced testers do without thinking.

First, read the **status line** of the response. Which family is the code in? That tells you whose problem it likely is.

Second, read the **request line** of the request. Is the method correct? Is the path correct and complete? Is there a stray space or a typo?

Third, scan the **request headers**. Is `Content-Type` present if there is a body? Does it match the body format? Is `Authorization` present if the endpoint is protected? Is `Accept` asking for a format the API provides?

Fourth, read the **request body**. Is it valid JSON? Are the field names exactly right, including capitalisation? Are required fields present, and values of the correct type (a number, not a string)?

Fifth, read the **response headers**. `Content-Type` tells you the true format of the body. `Location`, `Retry-After`, `WWW-Authenticate` and `Allow` often carry the explanation.

Sixth, read the **response body**. Well-designed APIs include an error message or code. If the body is HTML where you expected JSON, suspect a proxy, gateway or crash page in front of the API.

Practise this routine on every exchange for the rest of the week, and soon it will feel automatic.

### 15. A Raw Exchange With `nc` and `telnet`

To prove that HTTP really is just text, we can type a request by hand into a network connection, with no HTTP library at all. The tools `telnet` and `nc` (netcat) open a raw TCP connection and let you type into it. We use plain HTTP on port 80 here because it is unencrypted and therefore readable by hand. (Typing into an HTTPS connection would require TLS first; for that you can use `openssl s_client`, which is beyond our needs.)

`httpbin.org` serves plain HTTP on port 80 for this kind of experiment. (If a service redirects `http://` to `https://`, you will see a 301 instead of the page, which is itself a good lesson.) Open a terminal and run:

```bash
nc httpbin.org 80
```

The cursor now waits. You are connected. Type the following lines exactly, pressing Enter at the end of each line, and then press Enter **one extra time** to send the blank line that ends the headers:

```
GET /get HTTP/1.1
Host: httpbin.org
Accept: application/json
Connection: close

```

The server replies with something like:

```
HTTP/1.1 200 OK
Date: Sun, 11 Oct 2026 09:41:07 GMT
Content-Type: application/json
Content-Length: 205
Connection: close
Server: gunicorn/19.9.0

{
  "args": {},
  "headers": {
    "Accept": "application/json",
    "Host": "httpbin.org"
  },
  "origin": "203.0.113.25",
  "url": "http://httpbin.org/get"
}
```

(The exact headers, byte count and origin address will differ, and httpbin adds a few headers of its own to the echo.)

Explanation of what happened. You typed the request line `GET /get HTTP/1.1`, asking for the `/get` path. The `Host` header is mandatory in HTTP/1.1, and the server uses it to decide which site you mean. `Accept` tells httpbin you want JSON. `Connection: close` asks the server to close the connection after replying, so the exchange ends cleanly instead of waiting for more requests. The final empty line is what told the server "I am done with the headers". The server's answer has the same shape as every response we have studied: a status line, headers, a blank line, then the body. The body here is a JSON description of the request that httpbin received, which is why httpbin is so useful for testers: it *echoes your request back to you*, showing exactly what the server saw.

If you use `telnet` the effect is identical, with the command `telnet httpbin.org 80`. (On Windows, telnet may need enabling under "Turn Windows features on or off"; Git Bash users can use `nc` if it is installed.) For a request with a body, you must include `Content-Type` and a correct `Content-Length`, and the body goes after the blank line:

```
POST /post HTTP/1.1
Host: httpbin.org
Content-Type: application/json
Content-Length: 16
Connection: close

{"name":"Priya"}
```

The number 16 is the exact byte length of `{"name":"Priya"}`. If you typed 10, the server would read only the first ten bytes, `{"name":"P`, and then behave as though the body ended there, probably replying 400 because that is invalid JSON. If you typed 30, the server would wait for 14 more bytes that never arrive, and the request would hang until a timeout. This small experiment explains a great deal about why tools compute `Content-Length` for you and what goes wrong when a proxy or a test script gets it wrong.

### 16. A Walkthrough of Redirects and Cookies With httpbin

Two more experiments illustrate ideas from earlier sections using only `curl`.

**Redirect.** The path `/redirect/1` on httpbin answers with a redirect:

```bash
curl -i https://httpbin.org/redirect/1
```

```
HTTP/2 302
location: /get
content-length: 0
```

Here the status is 302 and there is no body. The `Location: /get` header says where to go next. Now add `-L` so `curl` follows it:

```bash
curl -L -i https://httpbin.org/redirect/1
```

You will see the 302 response followed by a second response, a 200 from `/get`. `curl` automatically issued a second request for the `Location` address. This shows that a redirect is really *two* request-response cycles stitched together.

**Cookie.** httpbin can set a cookie for us:

```bash
curl -i "https://httpbin.org/cookies/set?session=abc123"
```

```
HTTP/2 302
location: /cookies
set-cookie: session=abc123; Path=/
content-length: 0
```

The server asked the client to remember a cookie via `Set-Cookie`. If we now make a *separate* plain request, the server has forgotten everything, which demonstrates statelessness:

```bash
curl https://httpbin.org/cookies
```

```json
{
  "cookies": {}
}
```

The cookies list is empty, because this new `curl` command did not send the cookie back. To carry the "memory", we must send it ourselves in a `Cookie` header:

```bash
curl -H "Cookie: session=abc123" https://httpbin.org/cookies
```

```json
{
  "cookies": {
    "session": "abc123"
  }
}
```

Now the server "recognises" us, because the client presented the proof. `curl` can also store and replay cookies automatically with the options `-c cookies.txt` (save) and `-b cookies.txt` (send), which is how Postman and browsers behave by default. This is the statelessness workaround from section 10, shown in four commands.

### 17. Debugging Walkthroughs

Here are four complete diagnoses. In each, you will see what the symptom is, the messages, and the reasoning that leads to the fix. Try to find the cause yourself before reading the explanation.

#### 17.1 Debugging walkthrough A: the 415

A colleague reports that "the create-user call is broken". They send you this request and response:

```http
POST /users HTTP/1.1
Host: api.example.com
Content-Type: text/plain
Content-Length: 16

{"name":"Priya"}
```

```http
HTTP/1.1 415 Unsupported Media Type
Content-Type: application/json

{"error":"Content-Type must be application/json"}
```

The first clue is the status code. 415 sits in the 4xx family, so the request is at fault, not the server. The reason phrase and the error body both point at the body format. Looking back at the request, the body is clearly JSON, but the `Content-Type` header declares `text/plain`. The server believed the header, not its own guess about the body, and rejected the request. The fix is to change the request header to `Content-Type: application/json`. No debugger and no source code were needed; reading two messages was enough.

#### 17.2 Debugging walkthrough B: the 401 that was really a typo

A test calls a protected endpoint and gets:

```http
GET /api/orders HTTP/1.1
Host: shop.example.com
Authorisation: Bearer abc123.def456

```

```http
HTTP/1.1 401 Unauthorized
WWW-Authenticate: Bearer realm="shop"
Content-Type: application/json

{"error":"missing credentials"}
```

The token itself looks fine, yet the server says the credentials are *missing*. Read the request headers character by character: the header is spelled `Authorisation` (British spelling, with an "s"), but the standard header is `Authorization` (with a "z"). To the server this is an unknown header, so it was ignored, and the server concluded that no credentials were sent. The response header `WWW-Authenticate: Bearer` confirms that a bearer token is what it wanted. The fix is the spelling. Lessons: header names must match exactly (apart from letter case), and the error text "missing credentials" is more informative than the status code alone.

#### 17.3 Debugging walkthrough C: JSON parsing fails on a "successful" call

An automated test expects JSON from `GET /api/products` and fails with a parse error. Running `curl -i` shows:

```
HTTP/1.1 200 OK
Content-Type: text/html; charset=utf-8
Content-Length: 1245

<!DOCTYPE html>
<html><head><title>Sign in</title></head>
...
```

The status is a perfectly happy 200, which is why it is confusing. But the `Content-Type` is `text/html`, and the body is a login page. What happened? The API gateway redirected the unauthenticated request to a login page, and the test tool followed the redirect and received the HTML page with a 200. The parse error is a *symptom*. The root cause is missing authentication. The diagnostic principle: **a 200 status does not guarantee the response is what you expected; check `Content-Type` and the body as well.** Many real tests have asserted only "status is 200" and passed while the page returned was an error page.

#### 17.4 Debugging walkthrough D: the intermittent 503 in the pipeline

A suite passes on a tester's laptop but fails in the first minute of every pipeline run, with `503 Service Unavailable` on the first few requests, after which everything passes if re-run. Reading the 503 response shows `Retry-After: 5`. The 5xx family says the server is at fault or not ready, and `Retry-After` says "try again in five seconds". The reasonable conclusion is that the test environment is still starting up when the first tests fire. The fix lives in the pipeline and the test design: add a *readiness check* that polls a health endpoint until it returns 200 before running the suite, rather than adding random sleeps or ignoring the failures. (Pipelines are covered on Friday; the point today is that the response told us the diagnosis.)

### 18. Worked Real-World Scenarios

The following scenarios show how this knowledge shows up in daily testing. Each includes the situation, what the tester does with HTTP messages, and what is learned.

#### Scenario 1: The online shop checkout (create and verify)

A shopping API has `POST /orders` to place an order. A tester wants to confirm that a valid order is created. They send a `POST` with `Content-Type: application/json` and a body listing the product and quantity. They expect **201 Created**, a body containing a new `id`, and ideally a `Location` header. They do *not* accept 200 as equivalent, because 200 would suggest that the server treated this as a plain success and not as the creation of a resource; if the API's contract says 201, the difference is a legitimate defect. They then send `GET /orders/{id}` using the returned `id` and expect 200 with matching data, which verifies the server really stored the order instead of merely claiming to. **Lesson:** a complete API test often takes two messages: one to act and one to verify.

#### Scenario 2: The expired token (401 versus 403)

A mobile banking app calls `GET /accounts` with a token. A tester has two test accounts: one with an expired token, one valid but belonging to a user with no permission to view another customer's accounts. The first call returns **401** with `WWW-Authenticate`, because the server cannot establish identity. The second call, `GET /customers/99/accounts` using user 42's valid token, should return **403** (or 404 if the bank chooses to hide existence). If instead it returns 200 with the other customer's data, that is a severe security defect: broken access control. **Lesson:** 401 and 403 are different tests, and the difference between "who are you" and "you may not" is a core security check.

#### Scenario 3: The rate limit that only fails in the pipeline (429)

A tester's suite has 300 API tests that pass in a minute on a laptop with a single run. In the shared pipeline, many branches run suites at once and the same API key makes hundreds of requests per minute. Some tests fail with **429 Too Many Requests**, and `Retry-After: 30`. Reading the headers shows also `X-RateLimit-Limit: 100` and `X-RateLimit-Remaining: 0` (common conventions, though the exact names vary by API). The team responds by reducing unnecessary calls, using separate keys per pipeline, and adding a polite retry that honours `Retry-After`. **Lesson:** response headers are operational information, not decoration.

#### Scenario 4: The payment service that returns 500 for bad input

A tester sends `POST /payments` with the amount field as `"abc"` instead of a number. The server returns **500 Internal Server Error** and a stack trace in the body. A well-behaved API would detect the invalid amount and return **400** or **422** with a clear message. The 500 proves an unhandled exception, and the stack trace leaks internal details, which is also a security concern. The tester files a defect, attaching the raw request and the full response. **Lesson:** negative tests often find the most valuable defects, and 500 on invalid input is the textbook example.

#### Scenario 5: The double-click that charged twice (idempotency)

A tester notices that if the "Place order" request is sent twice in quick succession (simulating a double click or a retry after a network timeout), two orders are created and the customer is charged twice. `POST` is not idempotent, so the application must protect itself, for example with an `Idempotency-Key` header that a server uses to recognise a repeat. The tester designs a test that sends the same `POST` twice with the same key and expects only one order; and, without the key, documents the behaviour. **Lesson:** knowing which methods are safe or idempotent tells you which test cases to invent.

#### Scenario 6: The redirect that changed a POST into a GET (301 vs 307/308)

A company moves its API from `http://` to `https://` and configures a 301 redirect. After the migration, a tester's `POST /orders` calls over `http://` appear to succeed but no orders are created. Reading the raw messages with `curl -v -L` reveals that after the 301 the client re-sent the request as a `GET` with no body, silently losing the data. The fix is to update the base URL to `https://`, and for the server to use 308 (which preserves the method and body) for API redirects. **Lesson:** knowing the difference between the 3xx codes explains behaviour that looks like magic.

#### Scenario 7: Caching and the unexpected 304

A tester's script requests a product list and keeps getting an empty body. The status line says **304 Not Modified**. The script was sending an `If-None-Match` header with an old `ETag` copied from a previous run, so the server correctly replied that nothing had changed and sent no body. Removing the stale conditional header restored the full 200 response. **Lesson:** some "empty" responses are correct, and the fix is in the request.

### 19. Common Beginner Mistakes (and Why They Happen)

**Forgetting `Content-Type` on a `POST` or `PUT` with a JSON body.** The server cannot guess the format reliably, so it either rejects the request (415 or 400) or misreads the body. Tools like `curl` will happily default to form encoding, which is the wrong guess for JSON. Always set `Content-Type: application/json` when sending JSON.

**Checking the reason phrase instead of the number.** The phrase is advisory text, can vary or be absent (in HTTP/2 it never appears), and can be localised or customised. Always assert on the three-digit code.

**Assuming the server remembers previous requests.** Because HTTP is stateless, a call that works in a browser session (with cookies) may fail in a script that sends no cookie or token. The cure is to explicitly capture and send the token or cookie.

**Treating "any 2xx" as the same.** 200, 201, 202 and 204 mean different things, and the API contract usually specifies exactly one. A test that merely checks "success" can miss real defects such as creation returning 200.

**Trying to parse JSON from a 204 or an error page.** A 204 has no body, and an HTML error page is not JSON. Check status and `Content-Type` before parsing.

**Confusing 4xx and 5xx when classifying defects.** A 4xx usually means the request was wrong and the server correctly rejected it; the test, not the server, may be at fault. A 5xx signals a server-side failure. Mixing them sends the bug report to the wrong team.

**Confusing 401 and 403.** 401 is about identity, 403 about permission. Using the wrong expectation produces false failures and hides access-control defects.

**Forgetting that fragments are not sent.** Anything after `#` stays in the client. If a test depends on it, it will behave differently from what is expected.

**Not encoding special characters in URLs.** An unencoded `&` or space in a query value breaks the parameter list or the request line. Let the tool encode, or encode by hand with `%26` and `%20`.

**Disabling certificate verification "to make it work".** This hides the problem and removes TLS's protection. Fix the certificate trust instead, and where disabling is truly necessary, confine it to one named test environment.

**Ignoring response headers.** Valuable clues sit in `Content-Type`, `Location`, `Retry-After`, `Set-Cookie`, `WWW-Authenticate`, `Allow`. Many defects are visible only there.

**Typing a raw request without the blank line or with a wrong `Content-Length`.** The server hangs waiting for more or truncates the body. Count the bytes, or let a tool do it.

**Believing a successful response proves the data was stored.** Simulators like JSONPlaceholder and also buggy real servers can claim success without persisting. Verify with a follow-up `GET` where the scenario calls for it.

### 20. Practice Exercises With Full Worked Solutions

Try each exercise yourself *before* reading the solution. Where an exercise uses a public service, the outputs are representative; some header values will differ on your machine, and the services occasionally change. The goal is to practise the method of reading, not to match every character.

#### Exercise 1: Label the parts of a request

Label the numbered parts of this request.

```
POST /v1/users?notify=true HTTP/1.1      (1)
Host: api.example.com                     (2)
Content-Type: application/json            (3)
Content-Length: 30                        (4)
                                          (5)
{"name":"Priya","role":"qa"}              (6)
```

**Solution.** Part (1) is the **request line**: method `POST`, request target `/v1/users?notify=true` (path `/v1/users` with query `notify=true`), version `HTTP/1.1`. Parts (2), (3) and (4) are **headers**: the host being addressed, the body's format, and the body's length in bytes. Part (5) is the **blank line** that ends the headers. Part (6) is the **body**. A careful reader might also notice that the body `{"name":"Priya","role":"qa"}` is 28 characters, not 30, so the stated `Content-Length: 30` is wrong, which would make a server wait for two more bytes. This is the kind of detail that raw reading catches and a quick glance does not.

#### Exercise 2: Classify the status codes

For each status code, state the family, who is probably at fault, and one situation where it appears: `201`, `304`, `403`, `404`, `429`, `502`.

**Solution.** `201` is in the 2xx family (success); nobody is at fault; it appears when `POST` creates a record. `304` is 3xx (redirection family, though no redirect happens); nobody is at fault; it appears when a conditional request with `If-None-Match` finds the resource unchanged. `403` is 4xx; the client is at fault, because the user lacks permission; it appears when a normal user calls an admin endpoint. `404` is 4xx; the client, via a wrong address or missing item; it appears for `GET /users/99999`. `429` is 4xx; the client is sending too fast; it appears when a rate limit is exceeded, usually with `Retry-After`. `502` is 5xx; the server side, specifically a gateway that got a bad reply from the application behind it; it appears when the app has crashed but the proxy is still running.

#### Exercise 3: Your first `curl -v`

Run `curl -v https://jsonplaceholder.typicode.com/posts/1` and identify the method, the path, the status code, the version, and the response `Content-Type`.

**Solution.** In the output, the line `> GET /posts/1 HTTP/2` gives the method `GET`, the path `/posts/1` and the protocol version HTTP/2 (if `--http1.1` is used you will see `HTTP/1.1`). The first `<` line, `< HTTP/2 200`, gives the status code `200`. The line `< content-type: application/json; charset=utf-8` gives the response type: JSON in UTF-8. The body is a JSON object with keys `userId`, `id`, `title` and `body`, where `id` is `1`. An important sub-step is to notice which lines are the request (`>`) and which the response (`<`).

#### Exercise 4: Make a server return any status code on demand

Use httpbin to see the exact output for the codes `200`, `404`, `500` and `418`, then explain what you can and cannot learn from the body.

```bash
curl -i https://httpbin.org/status/404
curl -i https://httpbin.org/status/500
curl -i https://httpbin.org/status/418
```

**Solution.** For `404` you will see `HTTP/2 404` followed by headers and usually an empty body. For `500`, `HTTP/2 500` and also an empty body. For `418`, `HTTP/2 418` and a body containing an ASCII picture of a teapot with the words "I'm a teapot". The lesson: the status line alone tells you the outcome; the body is optional extra information, and in this deliberate case the servers are not describing a real error, only demonstrating the code. You can also see that the path segment after `/status/` is exactly what controlled the answer. This service is a safe playground for learning how a test tool will behave when it meets each code, which is what you will do in Postman later today.

#### Exercise 5: Create, then verify (and discover the simulation)

Use `curl` to `POST` a new post to JSONPlaceholder, note the returned `id`, then try to `GET` that `id`. Explain what you see.

```bash
curl -i -X POST https://jsonplaceholder.typicode.com/posts \
  -H "Content-Type: application/json" \
  -d '{"title":"qea","body":"practice","userId":1}'

curl -i https://jsonplaceholder.typicode.com/posts/101
```

**Solution.** The `POST` returns `HTTP/2 201` and a body such as `{"title":"qea","body":"practice","userId":1,"id":101}`. The follow-up `GET /posts/101` returns `HTTP/2 404` with body `{}`. The explanation: JSONPlaceholder is a *fake* API that accepts writes but does not store them, so the item never exists. This exercise teaches two lessons: first, that `201` is the appropriate response to creation, and second, that a "create then verify by reading back" test would *fail* against this simulator even though the create call looked successful. Against a real API, you would expect the `GET` to return 200 with matching data, and a failure there would be a genuine defect (the server claimed success without persisting).

#### Exercise 6: Prove HTTP is stateless

Using httpbin, set a cookie, then show that a separate request does not remember it, then show how to make it remember.

**Solution.** First run `curl -i "https://httpbin.org/cookies/set?name=Priya"` and observe `HTTP/2 302` with a `set-cookie: name=Priya; Path=/` header. Then run `curl https://httpbin.org/cookies`, which returns `{"cookies": {}}`, because this new command did not send the cookie back: the server remembered nothing about the previous request. Finally run `curl -H "Cookie: name=Priya" https://httpbin.org/cookies`, which returns `{"cookies": {"name": "Priya"}}`. Alternatively, use a cookie jar: `curl -c jar.txt -L https://httpbin.org/cookies/set?name=Priya` followed by `curl -b jar.txt https://httpbin.org/cookies`, which has `curl` do the remembering. In all versions, the memory is held by the *client* and presented with each request, and that is the essence of statelessness.

#### Exercise 7: Fix the broken request

This request fails with `400 Bad Request` from a server that expects JSON. Find all the problems and write the corrected request.

```http
POST /products HTTP/1.1
Content-Type: application/json

{'name': 'Laptop', 'price': 999,}
```

**Solution.** There are four problems. First, the `Host` header is missing, and it is mandatory in HTTP/1.1; add `Host: api.example.com`. Second, the JSON uses single quotes around keys and strings; JSON requires double quotes. Third, there is a trailing comma after `999`; JSON does not allow trailing commas. Finally, when typing the request by hand, a correct `Content-Length` should be added. The corrected request is:

```http
POST /products HTTP/1.1
Host: api.example.com
Content-Type: application/json
Content-Length: 29

{"name":"Laptop","price":999}
```

(The corrected body `{"name":"Laptop","price":999}` is 29 characters, so 29 is the right `Content-Length`; always count bytes with a tool rather than by eye.) With the corrected header and body the server can parse the request.

#### Exercise 7b: Correct the length

Using the corrected body from Exercise 7, compute the correct `Content-Length` by command and write the final request.

**Solution.** Run `printf '%s' '{"name":"Laptop","price":999}' | wc -c`, which prints `29`. So the final request is as above with `Content-Length: 29`. `printf '%s'` is used instead of `echo` because `echo` adds a newline character, which would make the count one too high.

#### Exercise 8: Redirect hunting

Request `https://httpbin.org/redirect/2` with and without `-L`, and explain how many request-response cycles occur in each case.

**Solution.** Without `-L`, `curl -i https://httpbin.org/redirect/2` shows one response: `HTTP/2 302` with `location: /relative-redirect/1`. Only one cycle occurs, and `curl` stops. With `-L`, `curl` follows the chain: the first 302 points to `/relative-redirect/1`, whose response is another 302 pointing to `/get`, whose response is 200. That is **three** request-response cycles, with the final 200 being what you see at the end. To count them, use `curl -sIL https://httpbin.org/redirect/2 | grep -i '^HTTP'`, which prints three status lines. The lesson is that when a test tool "follows redirects", several exchanges occur and only the last one is shown to your assertions unless you configure otherwise.

#### Exercise 9: Content negotiation

Ask httpbin for the JSON and XML representations from `/json` and `/xml`, then check the `Content-Type` of each and explain how you would assert that an API returns the correct type.

```bash
curl -i https://httpbin.org/json
curl -i https://httpbin.org/xml
```

**Solution.** The first response contains `content-type: application/json` and a JSON body (a sample "slideshow" document). The second has `content-type: application/xml` and an XML body. The point is that the **`Content-Type` header, not the shape of the body, is the declared format**, and a robust test asserts the header first and parses the body second. A test for an API that must return JSON would assert that `Content-Type` starts with `application/json` (using "starts with" or "contains" because a `; charset=utf-8` suffix is usually present) and then parse the body. Asserting exact equality with `application/json` would fail when the suffix is present.

#### Exercise 10: Read a raw exchange and write the defect report

Here is a captured exchange. Decide whether it is a defect, state the evidence, and write a short report.

```http
GET /api/users/abc HTTP/1.1
Host: api.example.com
Accept: application/json

```

```http
HTTP/1.1 500 Internal Server Error
Content-Type: text/html

<html><body><pre>NumberFormatException: For input string: "abc"
    at com.example.UserController.get(UserController.java:42)</pre></body></html>
```

**Solution.** Yes, this is a defect. The client sent a syntactically valid request but with a nonsense identifier (`abc` where a number is expected). A robust API should detect this and respond with a clean `400 Bad Request` (or `404 Not Found`) and a JSON error. Instead it returns `500`, which signals an unhandled exception, and an HTML page (`text/html`) even though the client asked for `application/json` via `Accept`. In addition, the body exposes internal class names and line numbers, which is an information disclosure risk. A short report:

*Title:* GET /api/users/{id} returns 500 with a stack trace for a non-numeric id.
*Steps:* Send `GET /api/users/abc` with `Accept: application/json`.
*Expected:* `400` (or `404`) with a JSON error body.
*Actual:* `500 Internal Server Error`, `Content-Type: text/html`, stack trace including `UserController.java:42`.
*Evidence:* the full raw request and response above.
*Severity:* Medium (unhandled error plus information disclosure).

### 21. Mini-Quiz: Self-Check Questions

Answer these from memory, then compare with the answers that follow.

1. What are the three parts of a request line?
2. What is the purpose of the blank line in an HTTP message?
3. Which part of a URL is never sent to the server?
4. What is the difference between `curl -i` and `curl -I`?
5. A response says `403 Forbidden`. How does that differ from `401 Unauthorized`?
6. Why should automated tests assert the numeric status code and not the reason phrase?
7. Which status code is the correct response to a `POST` that successfully creates a resource, and which header often accompanies it?
8. What does "stateless" mean, and name two ways clients supply "memory" to a stateless protocol.
9. What does TLS guarantee, and what is a certificate for?
10. A test receives `200 OK` with `Content-Type: text/html` where JSON was expected. What is the most likely cause?
11. What is the difference between `Content-Type` and `Accept`?
12. Why can a `204 No Content` response break a test that tries to parse the body as JSON?
13. In `curl -v` output, what do the prefixes `>`, `<` and `*` mean?
14. Name the family of each: `301`, `422`, `503`, `100`.
15. Which of `GET`, `POST`, `PUT`, `DELETE` are idempotent?

**Answers.**

1. The method (for example `GET`), the request target (path and query, for example `/todos/1`), and the HTTP version (for example `HTTP/1.1`).
2. It marks the end of the headers and the beginning of the body. Without it, the receiver cannot tell where the headers stop.
3. The fragment, the part after `#`. It is used only by the browser.
4. Lowercase `-i` includes the response headers in the output of a normal request. Uppercase `-I` sends a `HEAD` request, so the server returns only headers.
5. `401` means the server does not know who you are (missing or invalid credentials). `403` means the server knows who you are but you do not have permission.
6. The reason phrase is informational, may vary between servers, and is not transmitted in HTTP/2 and HTTP/3. The numeric code is the reliable, standard value.
7. `201 Created`, often accompanied by a `Location` header giving the address of the new resource.
8. Each request is independent and the server keeps no automatic memory of earlier requests. Clients supply memory with cookies (`Set-Cookie` then `Cookie`) or tokens (the `Authorization` header).
9. Confidentiality (data is encrypted), integrity (tampering is detected), and authentication of the server. A certificate, signed by a trusted authority, proves that a public key belongs to the named server.
10. Something other than the API produced the response, such as a login page, a proxy error page or a gateway page, often because authentication failed and the request was redirected.
11. `Content-Type` describes the format of the body being sent in this message. `Accept` states which formats the client is willing to receive in the response.
12. A 204 response must not have a body, so there is nothing to parse, and a JSON parser raises an error on empty input.
13. `>` lines are the request sent, `<` lines are the response received, and `*` lines are curl's own notes about connection and TLS.
14. `301` is 3xx (redirection), `422` is 4xx (client error), `503` is 5xx (server error), `100` is 1xx (informational).
15. `GET`, `PUT` and `DELETE` are idempotent. `POST` generally is not.

### 22. Glossary

**API (Application Programming Interface).** A defined way for one program to ask another program to do something. In this course, an API is a set of HTTP addresses and rules you can call.

**Body.** The data part of a request or response, after the blank line.

**Client.** The program that starts a conversation by sending a request.

**Cookie.** A small piece of text a server asks a client to store and send back on later requests, used to give a stateless protocol memory.

**Certificate.** A digital document, signed by a trusted authority, that proves a public key belongs to a named server.

**DNS.** The Domain Name System, which converts host names to IP addresses.

**Fragment.** The part of a URL after `#`, used by browsers and not sent to the server.

**Header.** A `Name: value` line carrying metadata about a message.

**HTTP.** HyperText Transfer Protocol, the request-response rules for exchanging messages between clients and servers.

**HTTPS.** HTTP carried over TLS encryption.

**Idempotent.** Describes a method whose repeated identical requests have the same effect on the server as a single one.

**JSON.** JavaScript Object Notation, a text format for structured data.

**Media type (MIME type).** A label such as `application/json` identifying the format of a body.

**Method.** The action word of a request, such as `GET` or `POST`.

**Path.** The part of a URL after the host and port that identifies the resource.

**Percent-encoding.** Writing a special character as `%` followed by two hexadecimal digits so it can appear in a URL.

**Port.** The numbered door on a server a client connects to; 80 is the default for HTTP and 443 for HTTPS.

**Protocol.** An agreed set of rules for communication.

**Query string.** The `name=value` pairs after `?` in a URL, used for filtering and options.

**Reason phrase.** The short human-readable text after the status code, such as `OK`.

**Request.** The message a client sends to a server.

**Response.** The message a server sends back to a client.

**Safe method.** A method intended only for reading, which does not change server state.

**Server.** The program that waits for requests and returns responses.

**Stateless.** Describes a protocol in which each request is independent and the server keeps no automatic memory of earlier ones.

**Status code.** A three-digit number in the response summarising the outcome.

**TCP.** The transport protocol that delivers HTTP bytes reliably and in order.

**TLS.** Transport Layer Security, the encryption protocol behind HTTPS.

**Token.** A string issued by a server after login and sent with later requests as proof of identity.

**URL.** Uniform Resource Locator, the address of a resource.

---

## Summary

HTTP is the set of rules clients and servers use to exchange messages, and HTTPS is the same protocol protected by TLS encryption, which gives confidentiality, integrity and server authentication through certificates. Every interaction is one request followed by one response, after the client has found the server through DNS, connected over TCP and, for HTTPS, completed a TLS handshake. A URL names the scheme, host, port, path, query and fragment, and special characters inside it must be percent-encoded.

A request consists of a request line (method, target and version), headers, a blank line and an optional body. A response consists of a status line (version, status code and reason phrase), headers, a blank line and an optional body. The `Content-Type` header says what format a body is in, and the `Accept` header says what format the client wants back. Common bodies are JSON, form data, multipart data, text, HTML and XML.

Status codes fall into five families: 1xx informational, 2xx success, 3xx redirection, 4xx client error and 5xx server error. Each family tells you quickly who is likely at fault, and individual codes such as 200, 201, 204, 301, 304, 400, 401, 403, 404, 409, 415, 422, 429, 500, 502 and 503 each have a specific meaning that a good test asserts exactly. HTTP/1.1, HTTP/2 and HTTP/3 carry the same messages in different ways, so everything you learn about message meaning applies to all of them.

HTTP is stateless, so the client must send proof of identity and context with every request, using cookies or tokens, and every test request must be self-contained. Safe methods only read, and idempotent methods can be repeated without extra effect; these ideas will be developed in "GET, POST, PUT and DELETE" later today.

With `curl` you can see all of this directly: `-i` includes response headers, `-I` sends a `HEAD` request, `-v` shows the request (`>`) and the response (`<`), `-X` chooses the method, `-H` adds a header and `-d` sends a body. You can even type a request by hand into `nc` or `telnet`. The reading routine is always the same: status line, request line, request headers, request body, response headers, response body. This skill, reading raw messages, is the foundation under Postman today, Python tomorrow, and every pipeline on Friday.

## Additional Resources

- MDN Web Docs, *An overview of HTTP*: https://developer.mozilla.org/en-US/docs/Web/HTTP/Overview
- MDN Web Docs, *HTTP messages*: https://developer.mozilla.org/en-US/docs/Web/HTTP/Messages
- MDN Web Docs, *HTTP response status codes*: https://developer.mozilla.org/en-US/docs/Web/HTTP/Status
- MDN Web Docs, *HTTP request methods*: https://developer.mozilla.org/en-US/docs/Web/HTTP/Methods
- The curl project, *Everything curl* (free online book): https://everything.curl.dev/
- IETF RFC 9110, *HTTP Semantics* (the official specification): https://www.rfc-editor.org/rfc/rfc9110
- httpbin, a free HTTP request and response service for practice: https://httpbin.org/
- JSONPlaceholder, a free fake REST API for testing: https://jsonplaceholder.typicode.com/
