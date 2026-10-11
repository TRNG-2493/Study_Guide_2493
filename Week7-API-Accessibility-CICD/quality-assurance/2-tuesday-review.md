# QA Review & Interview Questions: Week 7 Tuesday - Python API Automation

## Part A: Artifact Review

Day: **2-tuesday - Python API Automation**

### Written content
| Lesson | Words | Required sections | Fences balanced | Resource links | Later-day mentions |
|---|---|---|---|---|---|
| python-requests-library.md | 9,314 | yes | yes | 7 | 9 |
| pytest-api-test-structure.md | 11,324 | yes | yes | 10 | 12 |
| http-requests-from-automated-tests.md | 10,121 | yes | yes | 8 | 6 |
| status-code-validation.md | 9,264 | yes | yes | 9 | 2 |
| json-response-validation.md | 14,057 | yes | yes | 8 | 5 |
| headers-and-authentication.md | 9,606 | yes | yes | 10 | 4 |
| fixtures-and-parametrization.md | 8,986 | yes | yes | 7 | 5 |

### Demo
| Item | Status |
|---|---|
| demos/2-tuesday/code/demo_python_api_automation.py | present |
| demos/2-tuesday/demo-script.md | present |
| demos/2-tuesday/diagrams/*.mermaid | 2 file(s) |

### Exercise
| Item | Status |
|---|---|
| exercise/2-tuesday/exercise-python-api-automation.md | present |
| starter_code/ | present |
| solution/ | present |
| 'Project 2 milestone' section | yes |

### Quiz
| Item | Status |
|---|---|
| quiz/2-tuesday/quiz-python-api-automation.md | present |
| Questions | 59 |
| Hidden-solution blocks | 59 |

### Issues found by the audit
- None

### Reviewer notes and open items for human sign-off

1. **Completeness.** All 7 written lessons, the demo (script, runnable PyTest file, `requirements.txt`, `pytest.ini`, 2 diagrams), the exercise (brief, `starter_code`, `solution`) and the quiz are present. The quiz has 59 questions; the log asked for 8-10 and the user asked for 50+.
2. **Lesson length.** Each written lesson is 9-14k words, far above the log's "10-20 min read" guide, because the user required the depth standard. Use the lessons as reference, and use the Summary and Practice sections for a timed read.
3. **Outputs not captured live.** Code in the lessons, demo and solution was run against local mock servers (demo suite: 13 passed, 3 deselected, 1 xfailed; exercise solution: 68 tests; starter: 21 TODO skips). Outputs attributed to the real JSONPlaceholder or httpbin are "representative". The 3 demo tests marked `external` (httpbin) were not run: dry-run them once online.
4. **Demo file name.** The demo file is named `demo_python_api_automation.py` (the log's name), so `pytest.ini` sets `python_files = demo_*.py`. This is also a planned "break it" moment.
5. **Diagrams.** The Mermaid diagrams were not rendered; render-check them.
6. **Stand-in Project 2 API.** The real Project 2 API spec was not provided, so the exercise uses the stand-in server. Swap in the real API and re-check.
7. **No spoilers.** Forward mentions of Wednesday-Friday in Tuesday lessons are pointers only (verified by grep).

**Verdict:** Complete against the log; pending human dry-run items listed above.

---

## Part B: Interview Question Bank

## Beginner (Foundational)

### Q1: What does the `requests` library do, and which keyword arguments send query strings, JSON bodies, form bodies and headers?

**Keywords:** requests, params, json, data, headers

<details>
<summary>Click to Reveal Answer</summary>

`requests` is the standard Python library for making HTTP calls, with one function per method such as `get`, `post`, `put`, `patch` and `delete`. Use `params=` for query strings, `json=` for JSON bodies, `data=` for form bodies and `headers=` for headers. You install it in a virtual environment and record it in `requirements.txt`.

</details>

---

### Q2: Why must every `requests` call in a test have a `timeout=`?

**Keywords:** timeout, hang, default, ConnectTimeout, ReadTimeout

<details>
<summary>Click to Reveal Answer</summary>

The default is to wait forever, so one unresponsive server can hang the whole test run. A timeout turns a hang into an explicit failure you can report. It is worth knowing `ConnectTimeout` (could not connect), `ReadTimeout` (server too slow to reply) and `ConnectionError` apart, because they point to different causes.

</details>

---

### Q3: Does `requests` raise an exception when the server returns 404 or 500? What does `raise_for_status()` do?

**Keywords:** raise_for_status, 4xx, 5xx, HTTPError, assert

<details>
<summary>Click to Reveal Answer</summary>

No. `requests` does not raise on `4xx` and `5xx`; you get a normal `Response` object. `raise_for_status()` raises `HTTPError` for those codes, and it suits setup code. Inside a test, assert the exact status code instead, so the test states what it expects.

</details>

---

### Q4: What is a `Session` in `requests`, and what does it not do by default?

**Keywords:** Session, shared headers, cookies, connections, timeout

<details>
<summary>Click to Reveal Answer</summary>

A `Session` shares headers, cookies and connections across calls, so you set things like an auth header once. It has no default timeout, so you still need to pass `timeout=` on each call, or have your client wrapper add it. Wrapping a Session in a small client keeps the base URL, headers and timeout in one place.

</details>

---

### Q5: How does PyTest discover tests, and what project layout does the lesson recommend?

**Keywords:** discovery, test_*.py, Test* class, conftest.py, pytest.ini

<details>
<summary>Click to Reveal Answer</summary>

PyTest discovers tests by name: files named `test_*.py`, functions named `test_*`, and `Test*` classes without an `__init__`. The recommended layout uses `tests/` for tests, `utils/` for config and the API client, `conftest.py` for shared fixtures, `pytest.ini` for settings and `requirements.txt` for dependencies. PyTest also returns an exit code that a pipeline can use.

</details>

---

### Q6: What is the Arrange-Act-Assert pattern, and why should tests be independent?

**Keywords:** Arrange, Act, Assert, independent, order

<details>
<summary>Click to Reveal Answer</summary>

Arrange prepares the data, Act makes one request, and Assert checks the outcome. Plain `assert` statements are enough because PyTest's assertion rewriting prints the values involved. Tests must never rely on order or on state left by another test; you can verify this by running a test alone.

</details>

---

### Q7: What are PyTest markers, and how do `smoke` and `--strict-markers` fit in?

**Keywords:** markers, smoke, regression, register, --strict-markers

<details>
<summary>Click to Reveal Answer</summary>

Markers label tests by purpose, for example `smoke`, `regression` or `slow`, and you select them with `-m`. You register them in `pytest.ini`, and `--strict-markers` turns an unregistered or mistyped marker into an error. `skip`, `skipif` and `xfail(strict=True)` cover tests that cannot or should not currently pass.

</details>

---

### Q8: How do you write a CRUD test from code: what should a create (POST) test check?

**Keywords:** json=, 201, POST, response body, unique data

<details>
<summary>Click to Reveal Answer</summary>

Send the body with `json=`, assert the expected status such as `201`, then check the response body echoes what you sent and carries the new id. Generate unique, recognisable test data and clean up what you create. JSONPlaceholder fakes writes, so run each response check against it and run the full create-read-update-delete journey only against a persisting API.

</details>

---

### Q9: What is the difference between a 401 and a 403 status code?

**Keywords:** 401, 403, authentication, authorization, who are you

<details>
<summary>Click to Reveal Answer</summary>

`401` means the server does not know who you are: credentials are missing or invalid. `403` means the server knows you and the answer is still no, so you lack permission. Test with several callers and include a positive control, and follow the documented specification.

</details>

---

### Q10: Why is `response.ok` too loose for a test assertion, and what should you assert instead?

**Keywords:** response.ok, status_code, exact code, 200 vs 201, assert_status

<details>
<summary>Click to Reveal Answer</summary>

`response.ok` is `True` for anything below 400, so `200`, `201` and a redirect all pass. Assert the integer `status_code` against the exact documented code instead, never the reason phrase. The biggest anti-pattern is asserting only `200`, so cover negative cases as well.

</details>

---

### Q11: What does `response.json()` return, and what happens when the body is not valid JSON?

**Keywords:** response.json(), dict, list, JSONDecodeError, safe_json

<details>
<summary>Click to Reveal Answer</summary>

It converts the JSON body into Python `dict`, `list`, `str`, `int`, `float`, `bool` and `None`. If the body is an HTML page, empty, truncated or uses Python-style quoting, it raises `JSONDecodeError`, which is a `ValueError`. A small `safe_json` helper that reports the status, content type and start of the body makes that failure readable.

</details>

---

### Q12: What do `Content-Type` and `Accept` mean, and how do you send Basic auth and a Bearer token in `requests`?

**Keywords:** Content-Type, Accept, auth=, Authorization: Bearer, Basic

<details>
<summary>Click to Reveal Answer</summary>

`Content-Type` describes the body you send (`json=` sets it, `data=` does not) and `Accept` describes what you want back; mistakes give `415` and `406`. Basic auth is `auth=("user", "pass")`, whose header is Base64, which is encoding and not encryption. A Bearer token is sent as `Authorization: Bearer <token>`, ideally kept on a `Session`. API keys belong in a header, not in a URL.

</details>

---

### Q13: What is a PyTest fixture, and what does `yield` do inside one?

**Keywords:** fixture, yield, teardown, injection, conftest.py

<details>
<summary>Click to Reveal Answer</summary>

A fixture is reusable setup that PyTest injects into a test by matching the parameter name; you never call it yourself. Code after `yield` is teardown and runs even when the test fails. Shared fixtures go in `conftest.py`, and a fixture that raises reports as ERROR while a failed assertion reports as FAILED.

</details>

---

## Intermediate (Application)

### Q14: Compare the fixture scopes `function`, `class`, `module` and `session`. How do you choose, and what is `ScopeMismatch`?

**Keywords:** scope, function, session, ScopeMismatch, teardown order

**Hint:** Think about cost versus safety of sharing.

<details>
<summary>Click to Reveal Answer</summary>

The scope controls how often a fixture is rebuilt. Use the narrowest practical scope and widen it only for expensive, read-only values, such as a session-scoped `auth_token`. A wide-scoped fixture cannot depend on a narrower one, which raises `ScopeMismatch`. Teardown runs in reverse order of setup.

</details>

---

### Q15: How do you run one API test body over many inputs with `@pytest.mark.parametrize`, and how do `pytest.param` and `marks=` help?

**Keywords:** parametrize, pytest.param, id=, marks=, xfail

**Hint:** Think about readable test names and one bad case among many.

<details>
<summary>Click to Reveal Answer</summary>

`@pytest.mark.parametrize` runs one test body over literal inputs, using tuples for multiple parameters, and stacking decorators gives combinations. `pytest.param(..., id=...)` gives each case a readable name in the report. `marks=` attaches `xfail` or `skip` to a single case, so one known problem does not hide the others.

</details>

---

### Q16: A login call returns a JWT. How would you use it in tests, what does a JWT contain, and which authentication failures should you test?

**Keywords:** JWT, Bearer, exp, 401 vs 403, session fixture

**Hint:** Think about the three parts of the token and where expiry lives.

<details>
<summary>Click to Reveal Answer</summary>

Get the token from a login call, ideally in a session-scoped fixture, and send it as `Authorization: Bearer <token>` on a `Session` so one login serves the run. A JWT is `header.payload.signature`: readable by anyone, tamper-evident, with expiry in `exp`, so decode it only to inspect. Test every gate: missing, malformed, invalid, tampered and expired tokens give `401`, a wrong role gives `403`, and login failures should reveal nothing. Keep secrets in environment variables or a git-ignored `.env`.

</details>

---

### Q17: How does `jsonschema` fit into JSON response validation, and how should you layer your checks?

**Keywords:** jsonschema, validate, ValidationError, iter_errors, negative test

**Hint:** Think about cheapest checks first, then shape, then content.

<details>
<summary>Click to Reveal Answer</summary>

A status code says only that the server responded, so validate the body in layers: transport, status and headers, parsing, shape, content and consistency, cheapest first. `validate(instance, schema)` returns `None` or raises one `ValidationError`, using a schema built from `type`, `required` and `properties`. `iter_errors` reports all problems, and a `SchemaError` means your own schema is broken. Keep a negative test so you know the schema can fail.

</details>

---

## Advanced (Deep Dive)

### Q18: Design a robust API test layer for a team: how do the client, timeouts, config, fixtures and teardown fit together, and what pitfalls would you avoid?

**Keywords:** ApiClient, Session, fixtures, timeouts, autouse

**Hint:** Combine the lessons: config in one place, one client, self-cleaning data.

<details>
<summary>Click to Reveal Answer</summary>

Read the base URL, timeouts and thresholds from environment variables in one settings module, and send every request through one `ApiClient` built on a `requests.Session` that always applies a timeout. Expose it through fixtures in `conftest.py`: `base_url`, a shared `client`, a session `auth_token`, a per-test `auth_client`, and a self-cleaning `created_post` or `post_factory` that deletes what it creates. Tests assert exact status codes, content type and body, and attach a rich failure message that never includes secrets. Avoid hidden `autouse` fixtures, shared mutable state, leaked data, calling fixtures directly, order dependence and retries on non-idempotent methods.

</details>
