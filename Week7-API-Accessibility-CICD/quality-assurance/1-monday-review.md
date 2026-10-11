# QA Review & Interview Questions: Week 7 Monday - API & Postman Fundamentals

## Part A: Artifact Review

Day: **1-monday - API & Postman Fundamentals**

### Written content
| Lesson | Words | Required sections | Fences balanced | Resource links | Later-day mentions |
|---|---|---|---|---|---|
| http-messages.md | 14,873 | yes | yes | 8 | 8 |
| rest-api-fundamentals.md | 13,485 | yes | yes | 7 | 5 |
| get-post-put-and-delete.md | 13,801 | yes | yes | 8 | 1 |
| postman-collections.md | 11,373 | yes | yes | 5 | 12 |
| query-parameters-and-path-variables.md | 13,347 | yes | yes | 5 | 4 |
| headers.md | 12,665 | yes | yes | 7 | 2 |
| postman-variables-and-environments.md | 12,479 | yes | yes | 5 | 12 |

### Demo
| Item | Status |
|---|---|
| demos/1-monday/code/demo_api_postman_fundamentals.md | present |
| demos/1-monday/demo-script.md | present |
| demos/1-monday/diagrams/*.mermaid | 2 file(s) |

### Exercise
| Item | Status |
|---|---|
| exercise/1-monday/exercise-api-postman-fundamentals.md | present |
| starter_code/ | present |
| solution/ | present |
| 'Project 2 milestone' section | yes |

### Quiz
| Item | Status |
|---|---|
| quiz/1-monday/quiz-api-postman-fundamentals.md | present |
| Questions | 57 |
| Hidden-solution blocks | 57 |

### Issues found by the audit
- None

### Reviewer notes and open items for human sign-off

1. **Completeness.** All 7 written lessons, the demo (script, code `.md`, Postman collection and environment JSON, 2 diagrams), the exercise (brief, `starter_code`, `solution`) and the quiz are present. The quiz has 57 questions, more than the log's 8-10, by the user's instruction.
2. **Lesson length.** Each written lesson is 11-15k words, far above the log's "10-20 min read" guide, because the user required the depth standard. Suggest instructors assign the lessons as reference or pre-read, and use the Summary and Practice sections for a 10-20 minute read.
3. **Outputs not captured live; dry-run needed.** The curl and Postman outputs in the lessons are "representative", not captured live, because the build environment could not reach JSONPlaceholder or httpbin. The Postman `pm.test` scripts and the demo collection were never executed in Postman. Dry-run once: demo requests 3.2-3.5 use httpbin for 401 and bad-JSON cases, and request 3.5 fails on purpose.
4. **Diagrams.** The Mermaid diagrams were not rendered; render-check them.
5. **QA fix applied.** Monday lessons previously said Newman would be "covered Friday", but Friday does not teach it. The wording now says it is outside this week's lessons (`postman-collections.md`, `postman-variables-and-environments.md`).
6. **Stand-in Project 2 API.** The real Project 2 API spec was not provided, so Monday's exercise uses a stand-in server (`exercise/1-monday/starter_code/project2_api_server.py`). Swap in the real API and re-check `api-contract.md`.
7. **No spoilers.** Later-day mentions in Monday lessons are forward pointers only (verified by grep).

**Verdict:** Complete against the log; pending human dry-run items listed above.

---

## Part B: Interview Question Bank

## Beginner (Foundational)

### Q1: What is the difference between HTTP and HTTPS?
**Keywords:** HTTP, HTTPS, TLS, certificate, encryption
<details>
<summary>Click to Reveal Answer</summary>

HTTP is the set of rules clients and servers use to exchange messages. HTTPS is the same protocol protected by TLS encryption, which gives confidentiality, integrity and server authentication through certificates. The messages themselves are unchanged; they are just carried over a secured connection.
</details>

---

### Q2: What are the parts of an HTTP request message?
**Keywords:** request line, headers, blank line, body, method
<details>
<summary>Click to Reveal Answer</summary>

A request has a request line (method, target and version), headers, a blank line, and an optional body. A response mirrors this with a status line (version, status code, reason phrase), headers, a blank line and an optional body.
</details>

---

### Q3: What do the five families of HTTP status codes mean?
**Keywords:** 1xx, 2xx, 3xx, 4xx, 5xx
<details>
<summary>Click to Reveal Answer</summary>

1xx is informational, 2xx is success, 3xx is redirection, 4xx is a client error and 5xx is a server error. The family tells you quickly who is likely at fault. A good test also asserts the exact code, for example 201 for a creation rather than just any 2xx.
</details>

---

### Q4: What is the difference between the Content-Type and Accept headers?
**Keywords:** Content-Type, Accept, body format, negotiation
<details>
<summary>Click to Reveal Answer</summary>

`Content-Type` says what format the body of the message is in, for example `application/json`. `Accept` says what format the client wants back. Together with `Accept-Language` and `Accept-Encoding` they form content negotiation: a failed negotiation gives `406`, while a wrongly labelled body gives `415`.
</details>

---

### Q5: What does REST stand for in practice, and what is a resource?
**Keywords:** REST, resource, URL, representation, Fielding
<details>
<summary>Click to Reveal Answer</summary>

REST is an architectural style described by Roy Fielding in 2000. It is organised around resources identified by URLs and manipulated through representations, such as JSON. The HTTP method supplies the verb, so URLs name things (nouns) rather than actions.
</details>

---

### Q6: Name the REST constraints and explain what statelessness means for a tester.
**Keywords:** stateless, client-server, cacheable, uniform interface, layered
<details>
<summary>Click to Reveal Answer</summary>

The six constraints are client-server, stateless, cacheable, uniform interface, layered system and optional code on demand. Stateless means each request must carry everything the server needs, so the server keeps no client session between requests. For testers this means each test request should be self-contained and tests should be independent of one another.
</details>

---

### Q7: What makes a good REST URL?
**Keywords:** plural nouns, path ID, lowercase, hyphens, base URL
<details>
<summary>Click to Reveal Answer</summary>

Use plural nouns for collections, a path ID to identify one item (`/users/3`), shallow nesting, lowercase letters and hyphens. Do not put verbs in the path because the HTTP method is the verb. The base URL identifies the API root and should be stored in a variable.
</details>

---

### Q8: How do the HTTP methods map to CRUD, and what does each of GET, POST, PUT and DELETE do?
**Keywords:** CRUD, GET, POST, PUT, DELETE
<details>
<summary>Click to Reveal Answer</summary>

`POST` creates, `GET` reads, `PUT` (and `PATCH`) update, and `DELETE` removes. `GET` retrieves a representation of a resource, `POST` submits data for the server to process (usually creating a resource, with the server choosing the ID), `PUT` replaces the whole resource at a known address, and `DELETE` removes it.
</details>

---

### Q9: Define a safe method and an idempotent method. Which of GET, POST, PUT and DELETE are which?
**Keywords:** safe, idempotent, GET, POST, state
<details>
<summary>Click to Reveal Answer</summary>

A safe method is read-only and cannot be used to change data. An idempotent method has the same effect on server state when repeated as when sent once. `GET` is safe and idempotent; `PUT` and `DELETE` are idempotent but not safe; `POST` is neither. Every safe method is idempotent, but not every idempotent method is safe.
</details>

---

### Q10: What is a Postman collection and how do you organise one?
**Keywords:** collection, folders, naming convention, ordering, description
<details>
<summary>Click to Reveal Answer</summary>

A collection is a saved binder of requests. Organise it with folders and sub-folders, a `METHOD - Scenario` naming convention, deliberate ordering and Markdown descriptions. Authorization and scripts set at collection or folder level are inherited by the requests below, and the nearest explicit setting wins.
</details>

---

### Q11: What is the difference between a path variable and a query parameter?
**Keywords:** path variable, query parameter, ?, &, filter
<details>
<summary>Click to Reveal Answer</summary>

A path variable is a segment of the URL path that identifies a specific resource (`/users/42`) and is normally required. A query parameter is a `name=value` pair after `?`, joined with `&`, that filters, searches, sorts, pages or shapes a result and is normally optional. The fragment after `#` never reaches the server.
</details>

---

### Q12: What is a header, and what do the Authorization and User-Agent headers do?
**Keywords:** header, Name: value, Authorization, Bearer, User-Agent
<details>
<summary>Click to Reveal Answer</summary>

A header is a `Name: value` line of metadata; names are case-insensitive. `Authorization` carries credentials as Basic (Base64 of `user:password`, trivially decoded), a Bearer token, or a custom API key header, and the server's `WWW-Authenticate` is the challenge on a `401`. `User-Agent` identifies the client software making the request.
</details>

---

### Q13: What are Postman variables and environments, and why use them?
**Keywords:** {{name}}, environment, Dev/Test/Staging, baseUrl, initial value
<details>
<summary>Click to Reveal Answer</summary>

Variables replace hard-coded hosts, tokens, ids and emails with `{{name}}` placeholders that Postman resolves just before sending. Environments (Dev, Test, Staging) hold per-target values under the same variable names, so you switch with the dropdown instead of editing requests. Initial values sync and may be exported, while current values stay local, so real secrets belong in current values.
</details>

---

## Intermediate (Application)

### Q14: You send the same PUT three times and the same POST three times to an API that stores data. What do you expect to see, and why does it matter for retrying after a timeout?
**Keywords:** PUT, POST, idempotent, duplicate, retry
**Hint:** Think about what the server's state looks like after each call.
<details>
<summary>Click to Reveal Answer</summary>

The three identical `PUT` calls leave the server in the same state as one call, because `PUT` replaces the resource. The three `POST` calls usually create three separate records with different IDs, because `POST` is not idempotent. So after a network timeout it is generally safe to retry `GET`, `PUT` and `DELETE`, but a blind `POST` retry may create a duplicate, such as a double charge.
</details>

---

### Q15: A test deletes todo 5 twice. The first DELETE returns 204 and the second returns 404. Is this a bug?
**Keywords:** DELETE, idempotent, 404, state, assertion
**Hint:** Compare the state after the first and second call, not the responses.
<details>
<summary>Click to Reveal Answer</summary>

No. Idempotency concerns the server's state, not the response code: after one delete or two, the resource is gone. Some APIs return `204` again and others return `404`; both are valid. The test should assert whichever the documentation says and should not treat the repeat's `404` as a defect.
</details>

---

### Q16: A GET /users?role=admin request matches no users, while GET /users/9999 refers to a user that does not exist. What should each return, and how would you choose between a path variable and a query parameter here?
**Keywords:** 200, [], 404, filter, path variable
**Hint:** One is a filtered view of a collection; the other names a single resource.
<details>
<summary>Click to Reveal Answer</summary>

A filter with no matches should return `200` with an empty list `[]`, while a missing single resource should return `404`. Use a path variable when the value identifies the resource (`/users/9999`) and a query parameter when it changes the view of a collection (`?role=admin`). Tests should check the response data, not just the status code.
</details>

---

### Q17: A request uses {{team}}, which is defined in the collection, the active environment and a local script variable. Which value is used, and how would you confirm it? What if a post-response script sets a variable that the same request uses?
**Keywords:** scope, precedence, Local, Environment, pm.variables.get
**Hint:** Wide scopes give defaults, narrow scopes give overrides.
<details>
<summary>Click to Reveal Answer</summary>

The narrowest scope wins: Local > Data > Environment > Collection > Global, so the local value is used. You can confirm what actually resolves with `pm.variables.get`, or by hovering over the variable or using the Console. A post-response script runs after the request is sent, so the variable it sets only affects the next request; a pre-request script runs before substitution and can affect the current one.
</details>

---

## Advanced (Deep Dive)

### Q18: Design a portable, secure Postman setup for a team testing an API in Dev and Staging: what goes in variables, scopes, scripts and exported files, and how do you chain requests such as login then create then delete?
**Keywords:** baseUrl, secret, initial/current value, chaining, authToken
**Hint:** Think about portability, secrets, and what a script can and cannot change in the current request.
<details>
<summary>Click to Reveal Answer</summary>

Use `{{baseUrl}}` in every request and keep the same variable names in the Dev and Staging environments, switching by dropdown. Put placeholders in initial values and real secrets in current values with the type set to secret, and scrub exports before sharing because collections export as JSON that may be version-controlled. Capture ids and tokens in post-response scripts so the next request can use them, set collection-level authorization with `{{authToken}}` so requests inherit it, and remember that unresolved names are sent as literal text, so watch for red variable names. Because each request must be self-contained, make setup explicit in the collection order rather than relying on hidden state.
</details>

---
