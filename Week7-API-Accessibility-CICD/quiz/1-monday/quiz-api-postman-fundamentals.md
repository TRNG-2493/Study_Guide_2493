# Daily Knowledge Check: Week 7 Monday - API & Postman Fundamentals

This check covers HTTP messages, REST API fundamentals, GET/POST/PUT/DELETE, Postman collections, query parameters and path variables, headers, and Postman variables and environments. Try each question on your own first, then open the solution to check your reasoning.

---

## Part 1: Multiple Choice

### 1. What is the best description of an API in this course?

- [ ] A) A graphical tool for drawing screens
- [ ] B) A defined contract that lets one piece of software talk to another
- [ ] C) A database engine that stores records
- [ ] D) A file format for exporting Postman collections

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** B) A defined contract that lets one piece of software talk to another

**Explanation:** An API is a contract for software-to-software communication; a web API does this over HTTP.
- **Why others are wrong:**
  - A) That describes a UI design tool, not a contract between programs.
  - C) A server may use a database behind its API, but the API itself is the contract, not the storage.
  - D) Collection v2.1 JSON is an export format; it is not what an API is.

</details>

### 2. Why do the lessons call API testing the 'sweet spot' of the test pyramid?

- [ ] A) It replaces the need for unit tests
- [ ] B) It is the only layer that checks visual layout
- [ ] C) It needs no running server
- [ ] D) It offers a good balance of speed, stability and coverage of business rules

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** D) It offers a good balance of speed, stability and coverage of business rules

**Explanation:** The pyramid recommends many unit tests, a solid layer of API tests and a few UI tests; the API layer is where most business rules can be tested quickly and reliably.
- **Why others are wrong:**
  - A) The pyramid still wants many unit tests at the base.
  - B) Visual layout is a UI concern, which sits at the top of the pyramid.
  - C) API tests send real requests to a running service.

</details>

### 3. Which REST constraint is the reason each API test can be written to be independent of the others?

- [ ] A) Stateless
- [ ] B) Cacheable
- [ ] C) Layered system
- [ ] D) Code on demand

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** A) Stateless

**Explanation:** Statelessness means every request carries everything the server needs, so a test does not depend on an earlier call having set up a session.
- **Why others are wrong:**
  - B) Cacheable is about responses stating whether they may be reused, not about test independence.
  - C) This concerns intermediaries such as proxies and gateways between client and server.
  - D) This is the optional constraint where a server may send executable code to the client.

</details>

### 4. Which URL follows the REST naming conventions taught in the lesson (plural nouns, lowercase, hyphens, no verbs, no trailing slash)?

- [ ] A) `/getOrderItem?id=42`
- [ ] B) `/OrderItems/42`
- [ ] C) `/order-items/42`
- [ ] D) `/order_items/42/`

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** C) `/order-items/42`

**Explanation:** Lowercase, hyphen-separated, plural noun with the id in the path, and the HTTP method supplies the verb.
- **Why others are wrong:**
  - A) Puts a verb in the URL and uses a query string to identify an item instead of a path id.
  - B) Mixed case can cause accidental 404s because paths may be case-sensitive.
  - D) Underscores are not the common convention, and the trailing slash creates a second address for the same resource.

</details>

### 5. A request is sent to `GET /v2/users/42`. Which API versioning strategy is this?

- [ ] A) Header versioning
- [ ] B) Media type versioning
- [ ] C) Query parameter versioning
- [ ] D) URL path versioning

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** D) URL path versioning

**Explanation:** The version is part of the path (`/v1/`, `/v2/`), which is by far the most common strategy and the one used in the course.
- **Why others are wrong:**
  - A) That would use a header such as `X-API-Version: 2` and leave the URL unchanged.
  - B) That would use `Accept: application/vnd.shop.v2+json`.
  - C) That would look like `/users/42?version=2`.

</details>

### 6. In a raw HTTP request, what separates the headers from the optional body?

- [ ] A) A blank line
- [ ] B) A semicolon after the last header
- [ ] C) The `Content-Length` header
- [ ] D) The status line

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** A) A blank line

**Explanation:** A request is a request line, headers, a blank line and then an optional body (a response has the same shape with a status line first).
- **Why others are wrong:**
  - B) HTTP does not use a semicolon to end the header block.
  - C) It describes the size of the body but it is just another header line, not a separator.
  - D) A status line begins a response; it does not separate headers from body.

</details>

### 7. Which three items make up the first line (status line) of an HTTP response?

- [ ] A) Method, target and version
- [ ] B) Version, status code and reason phrase
- [ ] C) Status code, headers and body
- [ ] D) Scheme, host and path

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** B) Version, status code and reason phrase

**Explanation:** For example `HTTP/1.1 404 Not Found`.
- **Why others are wrong:**
  - A) That is the request line.
  - C) Headers and body come after the status line.
  - D) These are parts of a URL, not of a status line.

</details>

### 8. A user with a valid login for a normal account calls an admin-only endpoint. Which status should the API return?

- [ ] A) 401 Unauthorized
- [ ] B) 405 Method Not Allowed
- [ ] C) 403 Forbidden
- [ ] D) 422 Unprocessable Content

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** C) 403 Forbidden

**Explanation:** The server knows who the user is (authenticated) but the permissions are insufficient, which is 403.
- **Why others are wrong:**
  - A) In practice 401 means unauthenticated: credentials missing, expired or wrong.
  - B) That means the URL exists but not for that method.
  - D) That is for well-formed requests whose meaning is invalid, not permission problems.

</details>

### 9. When a request lacks valid credentials, which response header tells the client which authentication schemes it may use?

- [ ] A) `WWW-Authenticate`
- [ ] B) `Authorization`
- [ ] C) `Allow`
- [ ] D) `Retry-After`

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** A) `WWW-Authenticate`

**Explanation:** The server replies 401 and sends `WWW-Authenticate` as its challenge, for example `Bearer realm="reports"`.
- **Why others are wrong:**
  - B) That is the request header the client uses to send credentials.
  - C) It lists supported methods and goes with 405.
  - D) It says how long to wait after 429 or 503.

</details>

### 10. Tests pass one by one on a laptop but fail in the pipeline with `429 Too Many Requests`. Which response header tells you how long to wait before retrying?

- [ ] A) `Location`
- [ ] B) `ETag`
- [ ] C) `Allow`
- [ ] D) `Retry-After`

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** D) `Retry-After`

**Explanation:** `Retry-After` gives the wait either in seconds or as a date; the `X-RateLimit-*` headers describe the allowance.
- **Why others are wrong:**
  - A) It gives the address of a new resource or a redirect target.
  - B) It labels a version of a resource for caching and conditional requests.
  - C) It lists the methods a resource supports.

</details>

### 11. A client sends `If-None-Match` with a saved ETag and the resource has not changed. What does the server return?

- [ ] A) `200 OK` with an empty JSON object
- [ ] B) `204 No Content`
- [ ] C) `304 Not Modified` with no body
- [ ] D) `412 Precondition Failed`

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** C) `304 Not Modified` with no body

**Explanation:** A 304 means 'use your saved copy' and carries no body, saving bandwidth.
- **Why others are wrong:**
  - A) A 200 would resend a representation; the point of 304 is to avoid that.
  - B) 204 is a success with deliberately nothing to send, typical of DELETE, not a cache validation answer.
  - D) 412 is what `If-Match` triggers when the version no longer matches.

</details>

### 12. `POST /users` with an email address that is already registered should return which status?

- [ ] A) 415 Unsupported Media Type
- [ ] B) 409 Conflict
- [ ] C) 405 Method Not Allowed
- [ ] D) 202 Accepted

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** B) 409 Conflict

**Explanation:** The request is valid but clashes with the current state (a unique value already exists).
- **Why others are wrong:**
  - A) That is for a body in a format the server does not accept.
  - C) POST is supported on the collection; the problem is the data.
  - D) That means work was queued for later, not a clash.

</details>

### 13. Which HTTP method is neither safe nor idempotent?

- [ ] A) POST
- [ ] B) GET
- [ ] C) PUT
- [ ] D) DELETE

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** A) POST

**Explanation:** Sending POST twice usually creates two records, and it is not read-only.
- **Why others are wrong:**
  - B) GET is safe, idempotent and cacheable.
  - C) PUT changes data, but repeating it leaves the same state, so it is idempotent.
  - D) DELETE changes data, but the state after one or many calls is the same: the item is gone.

</details>

### 14. A phone loses signal right after the user taps 'Pay' and the app cannot tell whether the server received the request. Which request can be retried blindly with the least risk?

- [ ] A) `POST /payments` that creates a new payment
- [ ] B) `POST /orders` that creates a new order
- [ ] C) A PATCH whose body says to add 1 to a counter
- [ ] D) `PUT /orders/9` that sets the status to "paid"

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** D) `PUT /orders/9` that sets the status to "paid"

**Explanation:** Repeating a PUT leaves the order "paid", so a retry is safe. A POST that creates a payment may charge twice.
- **Why others are wrong:**
  - A) POST is not idempotent, so a blind retry may create a second payment.
  - B) Another POST: a retry may duplicate the order.
  - C) PATCH is not guaranteed idempotent, and an add-one operation changes the result each time.

</details>

### 15. A user record is `{"id":7,"name":"Ada Lovelace","email":"ada@example.com","phone":"555-0100"}`. A strict server receives `PUT /users/7` with body `{"name":"Ada King"}`. What is the main risk?

- [ ] A) Only the name changes and everything else is kept
- [ ] B) Fields that were omitted (email and phone) can be wiped because PUT replaces the whole resource
- [ ] C) The server must return 201 because the user is new
- [ ] D) The request is not idempotent, so it can never be repeated

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** B) Fields that were omitted (email and phone) can be wiped because PUT replaces the whole resource

**Explanation:** PUT replaces the resource with the body; the server may also reject it with 400 for missing fields. PATCH is the method for changing only one field.
- **Why others are wrong:**
  - A) That describes PATCH behaviour, not a strict PUT.
  - C) 201 applies only to create-by-PUT of a resource that did not exist.
  - D) PUT is idempotent by definition; the issue is lost data, not repeatability.

</details>

### 16. A `DELETE` succeeds and the API has nothing to send back. Which status is the most common choice?

- [ ] A) 201 Created
- [ ] B) 206 Partial Content
- [ ] C) 204 No Content
- [ ] D) 304 Not Modified

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** C) 204 No Content

**Explanation:** 204 means success with deliberately nothing to send, and the body must be empty.
- **Why others are wrong:**
  - A) That is for creating a resource.
  - B) That is for a byte-range slice of a resource.
  - D) That answers a conditional GET, not a delete.

</details>

### 17. A client sends `DELETE /users`, but that collection only supports GET and POST. What is the correct reply?

- [ ] A) `405 Method Not Allowed` with `Allow: GET, POST`
- [ ] B) `404 Not Found`
- [ ] C) `403 Forbidden`
- [ ] D) `501 Not Implemented`

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** A) `405 Method Not Allowed` with `Allow: GET, POST`

**Explanation:** The address exists but not for that verb, and a 405 must name the supported methods in `Allow`.
- **Why others are wrong:**
  - B) 404 means nothing exists at that address, but `/users` does exist.
  - C) 403 means the verb is generally supported but this caller is not permitted.
  - D) 501 means the server does not recognise the method at all; DELETE is well known.

</details>

### 18. Alice and Bob both loaded product v7. Alice saved first, so the current ETag is "v8". Bob's `PUT` carries `If-Match: "v7"`. What happens?

- [ ] A) The server silently overwrites Alice's change
- [ ] B) The server replies `304 Not Modified`
- [ ] C) The server replies `412 Precondition Failed` and changes nothing
- [ ] D) The server replies `405 Method Not Allowed`

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** C) The server replies `412 Precondition Failed` and changes nothing

**Explanation:** `If-Match` means 'only apply if the resource is still this version', which prevents the lost update.
- **Why others are wrong:**
  - A) That is the lost update problem that If-Match prevents.
  - B) 304 belongs to If-None-Match on a GET.
  - D) PUT is allowed on the resource; the failure is the version precondition.

</details>

### 19. A client POSTs a JSON body and wants an XML representation back. Which header pair is correct?

- [ ] A) `Content-Type: application/xml` and `Accept: application/json`
- [ ] B) `Content-Type: application/json` and `Accept: application/xml`
- [ ] C) `Accept: application/json` only
- [ ] D) `Content-Type: application/json` only

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** B) `Content-Type: application/json` and `Accept: application/xml`

**Explanation:** `Content-Type` describes the body being sent; `Accept` describes the response wanted.
- **Why others are wrong:**
  - A) The two are swapped relative to the scenario.
  - C) It would not label the request body, and it asks for JSON back, not XML.
  - D) It labels the body but does not ask for XML in the reply.

</details>

### 20. An API that strictly honours `Accept` only produces JSON. A client sends `Accept: application/xml`. Which status is correct?

- [ ] A) 415 Unsupported Media Type
- [ ] B) 400 Bad Request
- [ ] C) 404 Not Found
- [ ] D) 406 Not Acceptable

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** D) 406 Not Acceptable

**Explanation:** Content negotiation failed: the server cannot produce any format the client listed.
- **Why others are wrong:**
  - A) 415 is for a wrongly labelled or unsupported request body.
  - B) The request is well formed; only the requested format is unavailable.
  - C) The resource exists; its representation just is not available in XML.

</details>

### 21. Why is `Authorization: Basic cWFfdGVzdGVyOlNwcmluZzIwMjYh` dangerous in a screenshot or log?

- [ ] A) Base64 is encoding, not encryption, so anyone can decode it to the real username and password
- [ ] B) Base64 is encrypted with a key the server keeps secret
- [ ] C) Basic credentials can only be sent over plain HTTP
- [ ] D) The word `Basic` is a password hint

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** A) Base64 is encoding, not encryption, so anyone can decode it to the real username and password

**Explanation:** Basic is the Base64 of `username:password`; decoding takes a second and needs no key.
- **Why others are wrong:**
  - B) There is no key in Base64.
  - C) Basic is acceptable only over HTTPS; the risk here is the trivial decoding.
  - D) `Basic` is just the scheme name.

</details>

### 22. In Postman you choose Body > raw > JSON. What else does this choice do, and why does it matter?

- [ ] A) It adds an `Authorization` header automatically
- [ ] B) It turns the request method into PUT
- [ ] C) It sets the `Content-Type` header to JSON so the server parses the body correctly
- [ ] D) It saves the request into a collection

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** C) It sets the `Content-Type` header to JSON so the server parses the body correctly

**Explanation:** Choosing raw JSON matters because it sets the right `Content-Type`; without it a server may reply 415.
- **Why others are wrong:**
  - A) Authorization is configured separately in the Authorization tab.
  - B) The method is chosen separately in the request builder.
  - D) Saving is a separate action.

</details>

### 23. A collection has Bearer authorization with `{{token}}`. The folder `Public endpoints` is set to No Auth, and a request inside it is set to Inherit. What does that request send?

- [ ] A) The collection's Bearer token
- [ ] B) No token, because it inherits from the nearest explicit setting, the folder
- [ ] C) Both No Auth and the Bearer token
- [ ] D) Nothing, because the request fails to send

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** B) No token, because it inherits from the nearest explicit setting, the folder

**Explanation:** The nearest explicit setting wins: requests inside a folder inherit from the folder, not the collection.
- **Why others are wrong:**
  - A) The folder's explicit No Auth is nearer than the collection.
  - C) A request has one effective authorization setting.
  - D) Postman sends the request; it simply has no auth header.

</details>

### 24. Collection, folder and request each have a pre-request script. In which order do they run?

- [ ] A) Request, then folder, then collection
- [ ] B) Folder, then collection, then request
- [ ] C) All three at the same time
- [ ] D) Collection, then folder, then request

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** D) Collection, then folder, then request

**Explanation:** Scripts run from the outside in, and the same ordering applies to post-response scripts as described in the lesson on collections.
- **Why others are wrong:**
  - A) This is the reverse of the stated order.
  - B) The collection script always runs first.
  - C) They run in sequence.

</details>

### 25. `baseUrl` is defined in Global, Collection and the selected Environment, each with a different value, and no data file is used. Which value is used when the request is sent?

- [ ] A) The Global value
- [ ] B) The Collection value
- [ ] C) The Environment value
- [ ] D) Whichever was created first

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** C) The Environment value

**Explanation:** Precedence is Local > Data > Environment > Collection > Global; the narrower scope wins.
- **Why others are wrong:**
  - A) Global is the widest and lowest-priority scope.
  - B) Environment is narrower than Collection.
  - D) Creation order does not matter; scope precedence does.

</details>

### 26. Where should a real password go so it is not shared with teammates in a shared workspace?

- [ ] A) A placeholder in the Initial value and the real password in the Current value
- [ ] B) The real password in the Initial value
- [ ] C) The real password in both columns
- [ ] D) Nowhere; Postman cannot send passwords

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** A) A placeholder in the Initial value and the real password in the Current value

**Explanation:** Initial values sync to the cloud and may be exported, while current values stay on your local app.
- **Why others are wrong:**
  - B) Initial values sync to teammates, so the secret would be shared.
  - C) Both columns carry the same exposure problem; the initial value syncs.
  - D) Postman uses the current value when sending, so a local value works.

</details>

### 27. A tester calls `GET /posts?userId=999`, where no posts match. What should a correct API return?

- [ ] A) `404 Not Found`
- [ ] B) `200 OK` with an empty list `[]`
- [ ] C) `204 No Content`
- [ ] D) `400 Bad Request`

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** B) `200 OK` with an empty list `[]`

**Explanation:** The collection `/posts` exists and simply has no matches, so the right answer is 200 and `[]`. A missing single resource such as `/posts/9999` gives 404.
- **Why others are wrong:**
  - A) 404 fits a missing single resource, not an empty filter result.
  - C) The expected answer is a 200 with an empty list.
  - D) `userId=999` is a well-formed filter, not a bad request.

</details>

### 28. A `POST /items` returns `201` with header `Location: /items/57` and body `{"id":57}`. Which post-response script and next-request URL correctly chain a following GET using the environment?

- [ ] A) `pm.environment.get("itemId", 57);` and then `GET {{baseUrl}}/items/itemId`
- [ ] B) `pm.response.to.have.header("itemId");` and then `GET {{baseUrl}}/items/:itemId`
- [ ] C) `pm.test("itemId", 57);` and then `GET {{baseUrl}}/items/{{itemId}}`
- [ ] D) `pm.environment.set("itemId", pm.response.json().id);` and then `GET {{baseUrl}}/items/{{itemId}}`

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** D) `pm.environment.set("itemId", pm.response.json().id);` and then `GET {{baseUrl}}/items/{{itemId}}`

**Explanation:** A post-response script can read the body with `pm.response.json()`, store the id with `pm.environment.set`, and later requests reference it with `{{itemId}}`. A value set this way only affects the next request.
- **Why others are wrong:**
  - A) `get` reads a variable and does not store one, and the URL is missing the double curly braces.
  - B) `to.have.header` only asserts a header exists; it stores nothing, and `:itemId` is a Postman path variable that would still need a value.
  - C) `pm.test` defines a named test and does not create a variable.

</details>

---

## Part 2: True/False

### 29. True or False: HTTP/2 and HTTP/3 change the meaning of status codes such as 404 and 201.

- [ ] True
- [ ] False

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** False

**Explanation:** HTTP/1.1, HTTP/2 and HTTP/3 carry the same messages in different ways, so what you learn about message meaning applies to all of them.

</details>

### 30. True or False: A `500` response to clearly invalid user input is acceptable as long as the input was invalid.

- [ ] True
- [ ] False

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** False

**Explanation:** A 500 caused by bad input is always a defect. The API should detect the bad input and return a clean 4xx such as 400 or 422.

</details>

### 31. True or False: Every safe HTTP method is also idempotent, but not every idempotent method is safe.

- [ ] True
- [ ] False

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** True

**Explanation:** Safe methods do nothing to state, so repeating them has no extra effect. PUT and DELETE are idempotent yet change data, so they are not safe.

</details>

### 32. True or False: If the first `DELETE /orders/5` returns 204 and the second returns 404, the API is not idempotent.

- [ ] True
- [ ] False

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** False

**Explanation:** Idempotency is about server state, not identical responses. After one or many deletes the order is gone either way, and a test should assert whichever the documentation says.

</details>

### 33. True or False: A `401` response means the server knows who you are but you lack permission.

- [ ] True
- [ ] False

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** False

**Explanation:** That is 403. Despite its name, 401 really means unauthenticated: credentials were missing, expired or wrong.

</details>

### 34. True or False: The fragment after `#` in a URL is sent to the server along with the path and query string.

- [ ] True
- [ ] False

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** False

**Explanation:** The fragment is used by the client only and never reaches the server.

</details>

### 35. True or False: Because HTTP and REST are stateless, an API can never store data in a database.

- [ ] True
- [ ] False

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** False

**Explanation:** Stateless describes the conversation, not storage. A POST really does create a record that exists afterwards; there is just no hidden memory of previous requests.

</details>

### 36. True or False: Base64 in a Basic `Authorization` header protects the password with encryption.

- [ ] True
- [ ] False

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** False

**Explanation:** Base64 is an encoding with no key. Anyone who sees the header can decode it, so Basic is acceptable only over HTTPS.

</details>

### 37. True or False: In a shared workspace, a Postman variable's current value is synced to teammates, while its initial value stays local.

- [ ] True
- [ ] False

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** False

**Explanation:** It is the opposite: initial values sync (and may be exported) while current values stay on your local app.

</details>

### 38. True or False: If a `{{name}}` in a request matches no variable in any scope, Postman stops and refuses to send the request.

- [ ] True
- [ ] False

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** False

**Explanation:** Postman leaves it as literal text and sends the request anyway, for example `https://{{baseUrl}}/users`, so the server or DNS fails. Red variable names in the editor warn you.

</details>

---

## Part 3: Code and Message Prediction

### 39. A server accepts only JSON bodies. Without changing the body, a tester sends this request. Which status is the most likely reply and what is the cause?

```http
POST /users HTTP/1.1
Host: api.example.test
Content-Type: text/plain

{"name":"Ana","email":"ana@example.com"}
```

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** `415 Unsupported Media Type`. The body looks like JSON but is labelled `text/plain`, and a wrongly labelled body is a 415.

**Explanation:** The `Content-Type` header tells the receiver how to parse the body; the server does not accept that declared format.

</details>

### 40. What does this command return and what does the response tell you?

```bash
curl -i -X POST https://httpbin.org/get
```

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** A `405 Method Not Allowed` with an `allow: GET, HEAD, OPTIONS` header.

**Explanation:** `/get` only accepts GET (plus HEAD and OPTIONS), so POST is refused and the `Allow` header lists what would have worked.

</details>

### 41. Identify (a) the path variable value, (b) the query parameters and (c) the part the server never sees:

```
https://api.example.test/v1/users/42/orders?status=shipped&_limit=5#top
```

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** (a) `42` (the user id; `v1` is the version segment and `orders` the sub-collection), (b) `status=shipped` and `_limit=5`, (c) `#top`.

**Explanation:** The query string runs from `?` to any `#` and is split on `&` and `=`; the fragment is for the client only.

</details>

### 42. JSONPlaceholder has 100 posts with ids 1 to 100 in order. (a) Which ids does `GET /posts?_page=3&_limit=10` return? (b) An API has 95 items and `limit=20`: how many pages exist and how many items are on the last page?

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** (a) ids 21 to 30. (b) 5 pages, and the last page holds 15 items.

**Explanation:** `offset = (3 - 1) * 10 = 20`, so items 21 to 30. `totalPages = ceil(95 / 20) = ceil(4.75) = 5`; pages 1 to 4 hold 80 items, leaving 95 - 80 = 15.

</details>

### 43. A Postman test script is run against a response of `200 OK` that includes a `Location` header. Which tests pass?

```javascript
pm.test("Created", function () {
    pm.response.to.have.status(201);
});
pm.test("Has Location", function () {
    pm.response.to.have.header("Location");
});
```

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** "Created" fails and "Has Location" passes.

**Explanation:** A test passes if its function finishes without an assertion throwing. The status is 200, not 201, so the first assertion throws; the header exists, so the second does not.

</details>

### 44. What is printed by this snippet?

```javascript
pm.collectionVariables.set("ids", JSON.stringify([1, 2, 3]));
const raw = pm.collectionVariables.get("ids");
const ids = JSON.parse(raw);
console.log(typeof raw, ids.length);
```

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** `string 3`

**Explanation:** Variables are stored as text, so the array is stringified before storing (`raw` is a string) and parsed back into a real array whose length is 3.

</details>

### 45. Global scope has `baseUrl = https://global.test`, the selected Environment has `baseUrl = https://dev.test`, and a pre-request script runs `pm.variables.set("baseUrl", "https://local.test");`. What do `pm.variables.get("baseUrl")` and `pm.environment.get("baseUrl")` return afterwards?

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** `pm.variables.get` returns `https://local.test`; `pm.environment.get` returns `https://dev.test`.

**Explanation:** `pm.variables.set` writes a local variable, and local has the highest precedence, so `pm.variables.get` sees it. The environment's own value is untouched.

</details>

### 46. `itemName` is `Widget` and `quantity` is `5`. What exactly is sent for this body template and is it valid JSON?

```json
{ "name": {{itemName}}, "quantity": "{{quantity}}" }
```

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** `{ "name": Widget, "quantity": "5" }`, which is invalid JSON because `Widget` is unquoted, and `quantity` is sent as the string "5" not a number.

**Explanation:** Postman substitutes the text exactly and does not add or remove quotation marks, so the author must put quotes where JSON requires them: strings quoted, numbers not.

</details>

---

## Part 4: Fill-in-the-Blank

### 47. The ___ header tells the server the format of the request body.

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** `Content-Type`

**Explanation:** It labels the body with a media type such as `application/json` so the receiver knows how to parse it. `Accept` is the request header for the response format wanted.

</details>

### 48. The ___ request header lists the media types the client is able to handle in the response.

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** `Accept`

**Explanation:** It drives content negotiation; if no representation matches, a strict server replies 406.

</details>

### 49. In Postman, a path variable is written with a ___ before its name, for example `/users/:userId`.

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** colon (`:`)

**Explanation:** Postman then shows a Path Variables table. If its value is left empty, the literal text `:userId` is sent and the server typically returns an error.

</details>

### 50. A successful `POST` that creates a resource should normally return status ___.

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** `201` (Created)

**Explanation:** Servers commonly add a `Location` header with the address of the new resource.

</details>

### 51. A literal `&` inside a query parameter value must be percent-encoded as ___.

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** `%26`

**Explanation:** An unencoded `&` would be read as the separator between two parameters. A literal `%` itself becomes `%25`.

</details>

### 52. In Postman, a variable named `baseUrl` is referenced in a request as ___.

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** `{{baseUrl}}`

**Explanation:** Double curly braces mark the variable, and Postman replaces them with the resolved value just before the request is sent.

</details>

### 53. The pagination formula is `offset = (page - 1) * ___`.

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** `limit`

**Explanation:** With `page=3` and `limit=10` the offset is 20, so the page starts at the 21st item.

</details>

### 54. Of the six REST constraints, the only optional one is ___.

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** code on demand

**Explanation:** A server may send executable code such as JavaScript to the client; a design can still be called RESTful without it.

</details>

---

## Part 5: Matching

### 55. Match each status code (1-5) to its meaning (A-E).

| # | Item | | Option | Meaning |
|---|------|---|--------|---------|
| 1 | `204` | | A | Syntactically valid request whose meaning is invalid |
| 2 | `304` | | B | Service unavailable, for example overloaded or in maintenance |
| 3 | `406` | | C | Success with deliberately no body |
| 4 | `422` | | D | Server cannot produce a format listed in `Accept` |
| 5 | `503` | | E | Not modified: use your saved copy, no body |

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** 1-C, 2-E, 3-D, 4-A, 5-B

**Explanation:** `204` is success with no body; `304` is the bodyless cache answer to `If-None-Match`; `406` is failed content negotiation; `422` is well-formed but semantically invalid; `503` means the service cannot handle requests right now (a `Retry-After` header may say when to retry).

</details>

### 56. Match each header (1-5) to its purpose (A-E).

| # | Item | | Option | Meaning |
|---|------|---|--------|---------|
| 1 | `Allow` | | A | Labels a version of a resource, used for caching and `If-Match` |
| 2 | `Retry-After` | | B | Server's challenge listing accepted credentials on a 401 |
| 3 | `Location` | | C | Lists the methods a resource supports, required with 405 |
| 4 | `WWW-Authenticate` | | D | Address of a new resource (201) or a redirect target |
| 5 | `ETag` | | E | How long to wait after a 429 or 503 |

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** 1-C, 2-E, 3-D, 4-B, 5-A

**Explanation:** `Allow` accompanies 405 and answers OPTIONS; `Retry-After` is seconds or a date; `Location` goes with 201 and redirects; `WWW-Authenticate` is the 401 challenge; `ETag` labels a version of the resource.

</details>

### 57. Match each Postman expression (1-5) to what it does (A-E).

| # | Item | | Option | Meaning |
|---|------|---|--------|---------|
| 1 | `pm.response.json()` | | A | Returns true or false depending on whether the environment holds that name |
| 2 | `pm.response.code` | | B | Returns one response header's value as text |
| 3 | `pm.variables.set("x", 1)` | | C | Writes a local-scope variable |
| 4 | `pm.environment.has("authToken")` | | D | The numeric status code, such as 201 |
| 5 | `pm.response.headers.get("Location")` | | E | Parses the response body into a JavaScript object |

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** 1-E, 2-D, 3-C, 4-A, 5-B

**Explanation:** `json()` parses the body (and throws if it is not valid JSON); `code` is the number; `pm.variables.set` writes at local scope; `has` returns a boolean; `headers.get` returns a header's value.

</details>
