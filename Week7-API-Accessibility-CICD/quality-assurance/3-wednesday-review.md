# QA Review & Interview Questions: Week 7 Wednesday - Advanced API Testing

## Part A: Artifact Review

Day: **3-wednesday - Advanced API Testing**

### Written content
| Lesson | Words | Required sections | Fences balanced | Resource links | Later-day mentions |
|---|---|---|---|---|---|
| data-driven-api-testing.md | 5,196 | yes | yes | 6 | 5 |
| csv-json-parametrization.md | 5,480 | yes | yes | 6 | 1 |
| http-mocking.md | 5,430 | yes | yes | 5 | 2 |
| mocking-external-apis.md | 4,053 | yes | yes | 6 | 2 |
| test-isolation.md | 5,468 | yes | yes | 6 | 2 |
| request-response-validation.md | 5,421 | yes | yes | 6 | 0 |
| reusable-api-test-framework.md | 4,150 | yes | yes | 6 | 2 |

### Demo
| Item | Status |
|---|---|
| demos/3-wednesday/code/demo_advanced_api_testing.py | present |
| demos/3-wednesday/demo-script.md | present |
| demos/3-wednesday/diagrams/*.mermaid | 2 file(s) |

### Exercise
| Item | Status |
|---|---|
| exercise/3-wednesday/exercise-advanced-api-testing.md | present |
| starter_code/ | present |
| solution/ | present |
| 'Project 2 milestone' section | yes |

### Quiz
| Item | Status |
|---|---|
| quiz/3-wednesday/quiz-advanced-api-testing.md | present |
| Questions | 62 |
| Hidden-solution blocks | 62 |

### Issues found by the audit
- None

### Reviewer notes and open items for human sign-off

1. **Completeness.** All 7 written lessons, the demo (script, runnable PyTest file, CSV/JSON data, requirements, `pytest.ini`, 2 diagrams), the exercise (brief, `starter_code` with a deliberately messy baseline, `solution`) and the quiz (62 questions) are present.
2. **Lesson length.** Lessons are 4-5.5k words (about 20-28 minutes of reading at a normal pace), slightly over the log's 10-20 minute guide, because of the depth standard. Suggest assigning them as pre-reading, with the Summary and Practice sections as the short path.
3. **Verified by running.** Demo suite: 28 passed, 2 skipped, 2 xfailed, 1 xpassed, stable under `pytest-randomly`. Exercise solution: 56 tests pass under random order and with `-n 2`; the baseline fails under random order and when the API is down, as the brief claims. Lesson snippets for `responses` and `unittest.mock` were run offline (21 tests); the jsonschema and Pydantic snippets were run. **Not executed:** the exercise solutions in http-mocking, the `freezegun` and `responses` examples in test-isolation, the pytest and `schema_for` helpers in request-response-validation, and the `wraps=` spy example. Spot-check these before class.
4. **Demo "break it on purpose" moments.** Moments 1-3 and 6 are described but untested. The demo's deliberate order-dependent test may XPASS or XFAIL depending on the shuffle (documented).
5. **Diagrams.** The Mermaid diagrams were not rendered; render-check them.
6. **Stand-in API.** The exercise uses a stand-in Project 2 API server; swap in the real API before delivery.
7. **Forward mentions.** Mentions of Thursday and Friday topics are one-line pointers (verified).

**Verdict:** Approved for instructor use, conditional on the spot-checks in items 3-5 and the API swap in item 6.

---

## Part B: Interview Question Bank

## Beginner (Foundational)

### Q1: What is data-driven API testing, and what problem does it solve?

**Keywords:** data-driven, parametrize, test logic, data table

<details>
<summary>Click to Reveal Answer</summary>

Data-driven testing writes the test logic once and feeds it many rows of data, replacing many near-identical hard-coded test functions with a single function and a table. The logic (steps, endpoint, assertions) stays separate from the data (inputs, expected outputs, case names). This cuts duplication, makes adding a case a one-line change, and keeps tests easy to review.

</details>

---

### Q2: How do you design a good test data table, and which kinds of rows should it contain?

**Keywords:** case ID, positive, negative, boundary, equivalence partitioning

<details>
<summary>Click to Reveal Answer</summary>

Each row should have a case ID, the inputs and the expected result, taken from the specification. Mix positive, negative and boundary rows, and use equivalence partitioning to pick one representative per class so you avoid redundant cases. Builders and generators keep rows short, so every negative row is one change away from a valid baseline.

</details>

---

### Q3: What does `pytest.param` add to a parametrized API test?

**Keywords:** pytest.param, id, marks, xfail, skip

<details>
<summary>Click to Reveal Answer</summary>

`pytest.param` wraps a row so you can give it a readable `id` and attach `marks` such as `xfail`, `skip` or a custom marker to that row only. Good ids show exactly which row failed in the console and in CI reports. Without it, failing rows appear as opaque generated names.

</details>

---

### Q4: Why should test code locate data files with `Path(__file__).resolve().parent` instead of a relative path?

**Keywords:** pathlib, __file__, working directory, data folder

<details>
<summary>Click to Reveal Answer</summary>

Relative paths depend on the directory pytest is launched from, so tests pass locally and fail in CI or from another folder. Anchoring on `Path(__file__).resolve().parent` ties the data location to the test file itself. A small loader module can then centralise this, along with encoding and column checks.

</details>

---

### Q5: `csv.DictReader` returns every value as a string. What does that mean for your tests, and how does `json.load` differ?

**Keywords:** DictReader, strings, type conversion, json.load

<details>
<summary>Click to Reveal Answer</summary>

With CSV every cell is text, so you must convert types explicitly with named helpers and document what a blank cell means, since `''` is not `None`. `json.load` preserves numbers, booleans, `null` and nested lists. That is why JSON suits request bodies and CSV suits flat tables.

</details>

---

### Q6: When would you choose CSV versus JSON for test data?

**Keywords:** CSV, JSON, flat table, nested payload

<details>
<summary>Click to Reveal Answer</summary>

Use CSV for a flat table of scalar values such as IDs, boundaries and status codes, which non-programmers can edit in Excel and which diffs one line per case. Use JSON for nested payloads or when types matter. Avoid putting JSON strings inside CSV cells because every quote must be doubled; switch to JSON instead.

</details>

---

### Q7: What are common pitfalls when loading CSV test data, such as Excel and encoding problems?

**Keywords:** utf-8-sig, BOM, Excel formatting, empty parameter set

<details>
<summary>Click to Reveal Answer</summary>

Excel's UTF-8 CSV adds a BOM, so read with `utf-8-sig`; a legacy code page can show text like `CafÃ©`. Excel can also turn `007` into `7` or reformat dates, so format columns as Text or use JSON. Rows of only commas are real rows of empty strings. If a loader returns an empty list, pytest skips the test rather than failing, so validate the data files themselves.

</details>

---

### Q8: What are stubs, mocks, fakes and spies?

**Keywords:** test double, stub, mock, fake, spy

<details>
<summary>Click to Reveal Answer</summary>

A test double is any stand-in for a real component. A stub returns canned answers, a mock answers and records calls so you can verify interaction, a fake is a simplified working implementation such as an in-memory store, and a spy wraps the real thing while recording usage. Casually people call all of them mocks.

</details>

---

### Q9: Why mock HTTP in tests, and what should you not mock?

**Keywords:** deterministic, fast, failure simulation, system under test

<details>
<summary>Click to Reveal Answer</summary>

Mocking external HTTP makes tests fast, deterministic and free of side effects, and lets you simulate failures and rate limits that real servers cannot produce on demand. You should not mock the API you are testing. Mock the outgoing calls made by the code you are testing.

</details>

---

### Q10: How does the `responses` library work, and where do you patch with `unittest.mock`?

**Keywords:** responses.activate, responses.add, requests, patch where used

<details>
<summary>Click to Reveal Answer</summary>

`@responses.activate` intercepts calls made through `requests`, and `responses.add` registers a stub by URL, status and body; you can match on query, JSON body and headers, and inspect `responses.calls`. Passing an exception instance as the body simulates timeouts or `ConnectionError`. With `unittest.mock.patch`, patch the name where it is used, not where it is defined.

</details>

---

### Q11: What is test isolation, and what are the symptoms of coupled tests?

**Keywords:** isolation, order-independent, shared state, passes alone

<details>
<summary>Click to Reveal Answer</summary>

An isolated test is independent, order-independent and repeatable, relying only on its own setup. Coupling shows up as tests that pass alone but fail in the suite, failures after reordering, or failures only on a second run or in parallel. Typical hidden shared state is module globals, class attributes, singletons, environment variables, files, server-side data and tokens.

</details>

---

### Q12: What is a contract, and what does a contract test do?

**Keywords:** contract, contract test, schema, drift

<details>
<summary>Click to Reveal Answer</summary>

A contract defines what a correct request or response looks like. Contract tests check real requests and responses against it, so drift between client and API is caught early. JSON Schema is one common way to express the contract.

</details>

---

### Q13: What does the layered architecture of a reusable API test framework look like, and what is its key rule?

**Keywords:** layers, client, service, dependencies downward, conftest

<details>
<summary>Click to Reveal Answer</summary>

Each layer has one job: tests say what to verify, `conftest.py` wires fixtures, service classes own operations, the client owns HTTP concerns, with config, response wrapper, models and data below. The rule is that dependencies point downwards, so the client never imports services or tests. If a lower layer imports something above it, a responsibility is in the wrong layer.

</details>

---

## Intermediate (Application)

### Q14: How do you mock a third-party API well, including retries, backoff and 429 responses?

**Keywords:** client wrapper, dependency injection, retries, 429 Retry-After

**Hint:** Think about what you inject into the client, such as the sleep function.

<details>
<summary>Click to Reveal Answer</summary>

Put all HTTP in a client wrapper with injected `base_url`, `session`, token and `sleep`, so failure tests run fast without real waiting. Mock the far side of the network to produce what real services cannot on demand: 4xx/5xx, timeouts, retries with backoff, 429 with `Retry-After`, pagination and auth expiry. Build payloads from recorded real responses, and assert the outbound request (headers, body) as well as the result.

</details>

---

### Q15: How do you prove and enforce test isolation, and how do you handle flaky tests?

**Keywords:** pytest-randomly, pytest-xdist, seed, quarantine

**Hint:** Consider how you replay a failing random order.

<details>
<summary>Click to Reveal Answer</summary>

Use function-scoped fixtures with `yield` cleanup tolerant of 404, unique data via `uuid`, and assertions on your own records rather than global counts. Prove isolation with `pytest-randomly` (replay with `--randomly-seed`), `pytest-xdist` (`-n auto`, where session fixtures run per worker) and `pytest-repeat`. For flaky tests, capture the seed, reproduce, run alone and bisect; never fix with sleeps. Classify by cause and quarantine with a marker, ticket, owner and expiry.

</details>

---

### Q16: When would you choose JSON Schema versus Pydantic for response validation, and how does OpenAPI fit?

**Keywords:** JSON Schema, Pydantic, OpenAPI, strict mode

**Hint:** Think about who shares the contract and who writes the tests.

<details>
<summary>Click to Reveal Answer</summary>

JSON Schema is language-neutral, shareable with other teams and works directly with OpenAPI; Pydantic gives typed attribute access and easy cross-field validators but is Python-only and coerces unless strict. Many teams use schema files for the contract check and Pydantic for readable access, but should not validate every response twice. OpenAPI describes `paths`, `components/schemas` and `responses`, and tools like openapi-core and Schemathesis can test against it.

</details>

---

### Q17: How do you configure a reusable framework so it works across dev, stage and CI, and how does the mock/live switch fit in?

**Keywords:** environment variables, ApiClient, ApiResponse, TEST_MODE

**Hint:** Think about which layer owns timeouts, retries and assertions.

<details>
<summary>Click to Reveal Answer</summary>

Configuration comes from environment variables with safe defaults, so environments differ only in settings. `ApiClient` owns timeouts, retries on idempotent calls, logging and auth injection, services own operations and tests own assertions. `ApiResponse` helpers and Pydantic models turn failures into readable messages, fixtures wire everything, markers slice the suite, and `TEST_MODE` switches between mock and live.

</details>

---

## Advanced (Deep Dive)

### Q18: What risks come with mocking, and how do you keep mocks honest and avoid over-mocking?

**Keywords:** mock drift, contract checks, vcrpy, over-mocking

**Hint:** Consider what a mock cannot tell you about the real service.

<details>
<summary>Click to Reveal Answer</summary>

Mocks can drift from the real contract and give false confidence. Keep them honest with fixture contract checks, scheduled live tests, a few real-API tests and optionally `vcrpy`. Avoid over-mocking by asserting on behaviour rather than internals, and prefer real test databases for your own storage. Use mocks for what real services cannot do on demand.

</details>

---
