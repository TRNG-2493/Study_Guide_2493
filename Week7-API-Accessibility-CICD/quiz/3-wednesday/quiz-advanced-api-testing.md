# Daily Knowledge Check: Week 7 Wednesday - Advanced API Testing

This practice quiz covers Wednesday's topics: data-driven API testing, CSV/JSON parametrization, HTTP mocking (`responses` and `unittest.mock`), mocking external APIs, test isolation, request/response validation (JSON Schema and Pydantic) and building a reusable API test framework. Try each question before opening the solution. Part 3 snippets were run offline with pytest, `responses`, `jsonschema` and Pydantic v2, so the printed results are real.

## Part 1: Multiple Choice

### 1. What is data-driven testing?

- [ ] A) Running one test procedure against many rows of input and expected output
- [ ] B) Generating tests automatically by reading the API's source code
- [ ] C) Running each test against the production database so the data is real
- [ ] D) Recording a user's clicks and replaying them

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** A) Running one test procedure against many rows of input and expected output

**Explanation:** The logic is written once and a data table supplies the many cases, replacing near-duplicate test functions.
- **Why others are wrong:**
  - **B) is wrong:** The rows are designed by people from the specification; nothing is generated from source.
  - **C) is wrong:** Data-driven testing is about where inputs come from, not about using production data.
  - **D) is wrong:** That is record-and-replay UI automation, not table-driven testing.
</details>

### 2. In data-driven testing, which split between test logic and test data is correct?

- [ ] A) Logic is the inputs and expected results; data is the assertions
- [ ] B) Both belong inside the test body so the test is self-contained
- [ ] C) Logic is the how (steps, endpoint, assertions); data is the what (inputs and expected results)
- [ ] D) Data means only the pytest fixtures

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** C) Logic is the how (steps, endpoint, assertions); data is the what (inputs and expected results)

**Explanation:** Keeping them separate lets you add cases without touching the steps.
- **Why others are wrong:**
  - **A) is wrong:** This reverses the two terms.
  - **B) is wrong:** Mixing them is exactly what leads to duplicated hard-coded tests.
  - **D) is wrong:** Fixtures supply setup objects; the data is the inputs and expected outputs.
</details>

### 3. An id field is valid for the range 1-100. Which row set follows the boundary-value rule?

- [ ] A) 1, 50, 100
- [ ] B) 0, 1, 2, 99, 100, 101
- [ ] C) All integers from 1 to 100
- [ ] D) 0, 50, 101

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** B) 0, 1, 2, 99, 100, 101

**Explanation:** Boundary data sits at the edges of the valid range, where off-by-one mistakes (`<` versus `<=`) hide.
- **Why others are wrong:**
  - **A) is wrong:** It misses the values just outside the range (0 and 101).
  - **C) is wrong:** That is brute force; the lesson says to choose rows by partition and boundary.
  - **D) is wrong:** It skips the first and last valid values, 1 and 100.
</details>

### 4. Your data table has 10,000 rows, so the suite takes an hour and nobody runs it. What does the lesson recommend?

- [ ] A) Keep all rows and run them on every commit
- [ ] B) Delete the negative rows because they add little
- [ ] C) Randomly sample rows on every run without any marks
- [ ] D) Choose rows by equivalence partition and boundary; treat huge volume as performance testing and mark slow sets so they run nightly

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** D) Choose rows by equivalence partition and boundary; treat huge volume as performance testing and mark slow sets so they run nightly

**Explanation:** Each row is a real HTTP call, so row count must be deliberate.
- **Why others are wrong:**
  - **A) is wrong:** The suite would stop being run, which defeats its purpose.
  - **B) is wrong:** Negative and boundary rows are the most valuable ones.
  - **C) is wrong:** Random sampling loses coverage; partitions and boundaries give strong coverage from about eight rows.
</details>

### 5. What types do the values have after `csv.DictReader` reads a row such as `1,200`?

- [ ] A) Both are strings: `'1'` and `'200'`
- [ ] B) `1` and `200` are integers because they look numeric
- [ ] C) Integers for the first column, strings for the rest
- [ ] D) Floats, because CSV numbers are decimal by default

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** A) Both are strings: `'1'` and `'200'`

**Explanation:** CSV has no types; every cell arrives as text and you convert with named helpers such as `to_int`.
- **Why others are wrong:**
  - **B) is wrong:** DictReader never guesses types.
  - **C) is wrong:** There is no per-column typing.
  - **D) is wrong:** No numeric conversion happens at all.
</details>

### 6. Your request body has nested objects, a list and a `null` value. Which data file format fits best?

- [ ] A) CSV with JSON strings inside the cells
- [ ] B) CSV, because spreadsheets are easier to review
- [ ] C) JSON, because it preserves numbers, booleans, `null`, lists and nesting
- [ ] D) A plain text file with one value per line

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** C) JSON, because it preserves numbers, booleans, `null`, lists and nesting

**Explanation:** The lesson's rule: flat table of scalars is CSV; nested payloads or types that matter are JSON.
- **Why others are wrong:**
  - **A) is wrong:** Every quote must be doubled and it is miserable to edit; switch to JSON instead.
  - **B) is wrong:** CSV is flat and all text, so nesting and `null` get lost.
  - **D) is wrong:** It has no structure for nested data.
</details>

### 7. An Excel-exported "CSV UTF-8" file makes your first header read as `\ufeffid`. What is the fix?

- [ ] A) Rename the column in the loader every time
- [ ] B) Open the file with `encoding='utf-8-sig'`
- [ ] C) Convert every value with `int()`
- [ ] D) Switch to `json.load` for the same file

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** B) Open the file with `encoding='utf-8-sig'`

**Explanation:** Excel adds a byte order mark (BOM) at the start; `utf-8-sig` strips it.
- **Why others are wrong:**
  - **A) is wrong:** It hides the symptom; the encoding is the cause.
  - **C) is wrong:** Type conversion does not affect the header's invisible character.
  - **D) is wrong:** `json.load` reads JSON, not CSV.
</details>

### 8. Your team needs to tell "field is missing" apart from "field is an empty string" in a CSV test. What does the lesson suggest?

- [ ] A) Always treat a blank cell as an empty string
- [ ] B) Always treat a blank cell as `None`
- [ ] C) Put the value in a JSON string inside the cell
- [ ] D) Use an explicit marker such as `<EMPTY>` and translate it in the loader

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** D) Use an explicit marker such as `<EMPTY>` and translate it in the loader

**Explanation:** Without a marker the two scenarios are indistinguishable, yet they need different expected API behaviour.
- **Why others are wrong:**
  - **A) is wrong:** Then "field missing" can never be tested.
  - **B) is wrong:** Then "empty string" can never be tested.
  - **C) is wrong:** The lesson warns against JSON-in-CSV cells.
</details>

### 9. Which statement about test doubles is accurate?

- [ ] A) A stub records how it was called; a mock only returns canned data
- [ ] B) A stub returns canned answers; a mock also records calls so interactions can be verified
- [ ] C) A fake is the real object, wrapped so that calls are recorded
- [ ] D) A spy is a simplified but working in-memory implementation

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** B) A stub returns canned answers; a mock also records calls so interactions can be verified

**Explanation:** A quick memory aid: a stub answers, a mock answers and remembers.
- **Why others are wrong:**
  - **A) is wrong:** This swaps the two definitions.
  - **C) is wrong:** That describes a spy.
  - **D) is wrong:** That describes a fake.
</details>

### 10. `billing.py` contains `from payments import charge` and calls `charge()`. Which patch target replaces it for tests of `billing`?

- [ ] A) `payments.charge`
- [ ] B) `charge`
- [ ] C) `billing.charge`
- [ ] D) `billing.payments`

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** C) `billing.charge`

**Explanation:** Patch the name in the namespace where the code under test looks it up, not where it was defined.
- **Why others are wrong:**
  - **A) is wrong:** `billing` already holds its own reference to the original, so patching the definition site does not affect it.
  - **B) is wrong:** `patch` needs a dotted `module.name` path.
  - **D) is wrong:** `billing` has no attribute `payments` when it uses `from payments import charge`.
</details>

### 11. With `responses`, you register the same URL three times: 503, 503, then 200. What happens when your code calls the URL?

- [ ] A) The replies are served in order: 503, 503, 200
- [ ] B) All three calls get the first stub, 503
- [ ] C) `responses` raises an error for duplicate registrations
- [ ] D) The calls are answered at random

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** A) The replies are served in order: 503, 503, 200

**Explanation:** Repeated registrations form a sequence, which makes retry logic easy to test.
- **Why others are wrong:**
  - **B) is wrong:** The first match is removed when another match remains, so the sequence advances.
  - **C) is wrong:** Duplicates are the documented way to build a sequence.
  - **D) is wrong:** The order is deterministic.
</details>

### 12. What does `responses.RequestsMock()` as a context manager do by default that the plain `@responses.activate` decorator does not?

- [ ] A) It lets real requests through when no stub matches
- [ ] B) It records no calls
- [ ] C) It makes every response return 200
- [ ] D) It fails at the end of the `with` block if a registered stub was never called

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** D) It fails at the end of the `with` block if a registered stub was never called

**Explanation:** `assert_all_requests_are_fired=True` catches tests where the code took a different path than you set up.
- **Why others are wrong:**
  - **A) is wrong:** An unmatched request raises `ConnectionError`; it is not sent to the network.
  - **B) is wrong:** Calls are recorded and visible via `calls`.
  - **C) is wrong:** Status codes come from the stubs you register.
</details>

### 13. Your helper must be tested for what happens on a request timeout. How do you make `responses` simulate it?

- [ ] A) Register `status=408` and nothing else
- [ ] B) Pass an exception instance such as `ConnectTimeout("msg")` as `body`
- [ ] C) Use `time.sleep(60)` inside the test
- [ ] D) Pass the exception class, `ConnectTimeout`, as `body`

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** B) Pass an exception instance such as `ConnectTimeout("msg")` as `body`

**Explanation:** Passing an exception object makes `responses` raise it; passing the class instead is a listed mistake.
- **Why others are wrong:**
  - **A) is wrong:** That returns an HTTP reply, not a raised timeout exception.
  - **C) is wrong:** The test becomes slow and still does not raise `requests`' exception.
  - **D) is wrong:** The common mistake: use an instance, not the class.
</details>

### 14. Which client behaviour should a mocked error-handling test confirm?

- [ ] A) Retry every error, including 400
- [ ] B) Never retry anything
- [ ] C) Retry on 5xx, 429 and timeouts, but do not retry a 404 or 400
- [ ] D) Retry only 404 responses

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** C) Retry on 5xx, 429 and timeouts, but do not retry a 404 or 400

**Explanation:** A 4xx is the caller's mistake; retrying it only spams the provider.
- **Why others are wrong:**
  - **A) is wrong:** The lesson lists "retrying every error" as a mistake.
  - **B) is wrong:** Transient 5xx, 429 and timeouts are exactly what retries are for.
  - **D) is wrong:** A 404 will not change on retry.
</details>

### 15. Which scenario is a case where mocking is the WRONG choice?

- [ ] A) A smoke test after a deploy that must confirm the real system is alive
- [ ] B) Testing how your code reacts to a 503 from a payment provider
- [ ] C) Avoiding a rate-limited third-party quota in a nightly suite
- [ ] D) Sending a welcome email without actually emailing anyone

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** A) A smoke test after a deploy that must confirm the real system is alive

**Explanation:** A mock cannot tell you anything about real systems; the same is true when verifying the real contract.
- **Why others are wrong:**
  - **B) is wrong:** Simulating failures is a prime reason to mock.
  - **C) is wrong:** Mocks remove quota usage.
  - **D) is wrong:** Mocking prevents real side effects.
</details>

### 16. Your mocked tests are all green, but production breaks because the real API renamed `name` to `full_name`. What is this called and what is the best defence?

- [ ] A) Flaky tests; add `time.sleep` before assertions
- [ ] B) Over-mocking; mock even more of your own code
- [ ] C) Order dependence; run the suite with `pytest-randomly`
- [ ] D) Contract drift; keep a few scheduled real-API contract tests and build mocks from recorded real responses

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** D) Contract drift; keep a few scheduled real-API contract tests and build mocks from recorded real responses

**Explanation:** A mock is an unverified claim about the real API; only a live check or schema check against reality catches the change.
- **Why others are wrong:**
  - **A) is wrong:** Sleeping hides defects and has nothing to do with a renamed field.
  - **B) is wrong:** Mocking more makes the false confidence worse.
  - **C) is wrong:** Random order does not compare mocks with the real API.
</details>

### 17. A test fails only when the whole suite runs. Which tool lets you replay the exact failing order?

- [ ] A) `pytest-repeat` with `--count=20`
- [ ] B) `pytest-randomly` with `--randomly-seed=<seed from the failed run>`
- [ ] C) `pytest -n auto`
- [ ] D) `tmp_path`

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** B) `pytest-randomly` with `--randomly-seed=<seed from the failed run>`

**Explanation:** The seed in the run header reproduces the same order, turning "it failed once" into a fixable bug.
- **Why others are wrong:**
  - **A) is wrong:** It repeats a test; it does not reproduce an order.
  - **C) is wrong:** That runs tests in parallel workers; it does not replay an order.
  - **D) is wrong:** It gives each test its own directory and has no ordering role.
</details>

### 18. You run `pytest -n 4` and your suite has a `scope="session"` fixture that seeds the database. What happens?

- [ ] A) It runs once overall because it is session-scoped
- [ ] B) It is skipped because workers cannot use fixtures
- [ ] C) The fixture runs once in each of the four workers, so the seeding repeats
- [ ] D) It runs once per test

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** C) The fixture runs once in each of the four workers, so the seeding repeats

**Explanation:** Session fixtures run once per worker, not once overall, which is a bug for seeding or purging.
- **Why others are wrong:**
  - **A) is wrong:** With xdist, "session" means once per worker process.
  - **B) is wrong:** Workers use fixtures normally.
  - **D) is wrong:** That is function scope, not session scope.
</details>

### 19. Where should cleanup code go so it still runs when an assertion fails?

- [ ] A) After the `yield` in a fixture (or in a finalizer)
- [ ] B) At the last line of the test body
- [ ] C) In a comment that tells the next developer to clean up
- [ ] D) Only in a separate nightly job

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** A) After the `yield` in a fixture (or in a finalizer)

**Explanation:** Cleanup at the end of a test body is skipped when an assertion raises first.
- **Why others are wrong:**
  - **B) is wrong:** An earlier failed assertion skips it.
  - **C) is wrong:** Nothing guarantees it runs.
  - **D) is wrong:** Leftover data would corrupt the tests in between.
</details>

### 20. Many tests create users on a shared API server. Which practice follows the lesson?

- [ ] A) Hard-code `test@example.com` so results are predictable
- [ ] B) Assert that the total number of users equals 10
- [ ] C) Use a session-scoped user fixture that every test edits
- [ ] D) Generate unique data (for example with `uuid`) and assert on the records your test created, not on global counts

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** D) Generate unique data (for example with `uuid`) and assert on the records your test created, not on global counts

**Explanation:** Other tests and parallel workers also write to the server, so shared counts and fixed emails collide.
- **Why others are wrong:**
  - **A) is wrong:** Two runs or workers creating it at once will conflict.
  - **B) is wrong:** "Breaks whenever anyone else adds a user" is the lesson's BAD example.
  - **C) is wrong:** Shared mutable session data is the highest isolation risk.
</details>

### 21. A JSON Schema has `properties` for `id`, `name` and `email` but no `required` keyword. Which input does it accept?

- [ ] A) Nothing; every property is mandatory by default
- [ ] B) `{}`, an empty object
- [ ] C) Only objects with all three keys
- [ ] D) Only arrays of objects

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** B) `{}`, an empty object

**Explanation:** `properties` only constrains keys that are present; `required` is what forces them.
- **Why others are wrong:**
  - **A) is wrong:** The most commonly misunderstood point: properties alone do not make a field required.
  - **C) is wrong:** That would need `required`.
  - **D) is wrong:** `type` was not set to array.
</details>

### 22. Your schema says `"email": {"type": "string", "format": "email"}`, yet `"not-an-email"` passes validation. Why?

- [ ] A) `format` is only valid inside `oneOf`
- [ ] B) `Draft202012Validator` does not support strings
- [ ] C) In `jsonschema`, `format` is only an annotation unless you pass a `format_checker`
- [ ] D) The value is a valid email in JSON

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** C) In `jsonschema`, `format` is only an annotation unless you pass a `format_checker`

**Explanation:** Always test a schema with a deliberately bad value to confirm the format is really enforced.
- **Why others are wrong:**
  - **A) is wrong:** `format` works anywhere; it just is not checked by default.
  - **B) is wrong:** Strings are supported; the format keyword is the issue.
  - **D) is wrong:** It is not; the checker is simply off.
</details>

### 23. Which API change is backward compatible for existing consumers?

- [ ] A) Adding a new optional field to a response
- [ ] B) Renaming a response field from `name` to `full_name`
- [ ] C) Changing `id` from integer to string
- [ ] D) Making an optional request field required

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** A) Adding a new optional field to a response

**Explanation:** Removing or renaming a field, changing a type, or making an optional request field required are breaking changes.
- **Why others are wrong:**
  - **B) is wrong:** A rename breaks consumers that read the old key.
  - **C) is wrong:** A type change is breaking.
  - **D) is wrong:** Existing requests without it would now fail.
</details>

### 24. In a layered API test framework, which rule keeps responsibilities honest?

- [ ] A) The client should call `assert` on status codes so tests are shorter
- [ ] B) One big client class should hold every endpoint method
- [ ] C) Tests should build their own `requests.Session` objects
- [ ] D) Dependencies point downwards: tests use services, services use the client, and the client never imports tests or services

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** D) Dependencies point downwards: tests use services, services use the client, and the client never imports tests or services

**Explanation:** If the client imports something from above, a responsibility sits in the wrong layer.
- **Why others are wrong:**
  - **A) is wrong:** Test logic in the client blocks negative tests where a 404 is expected.
  - **B) is wrong:** That is the God client anti-pattern.
  - **C) is wrong:** That duplicates infrastructure the client layer owns.
</details>

### 25. A framework runs with `TEST_MODE=mock` by default. What is the main reason for defaulting to mock?

- [ ] A) Live mode is always forbidden in a team
- [ ] B) A new colleague's first run succeeds offline, and runs are fast and deterministic
- [ ] C) Mocks prove the real API is correct
- [ ] D) Tests must be rewritten for each mode

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** B) A new colleague's first run succeeds offline, and runs are fast and deterministic

**Explanation:** `TEST_MODE=live` is for release checks and for confirming the mock still matches reality.
- **Why others are wrong:**
  - **A) is wrong:** Live mode is used before release and to detect drift.
  - **C) is wrong:** They prove nothing about the real service.
  - **D) is wrong:** The tests are identical in both modes.
</details>


## Part 2: True / False

### 26. A green suite of mocked tests proves that the real API works.

- [ ] True
- [ ] False

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** False

**Explanation:** A mock is an unverified claim about the real API; it can drift while tests stay green, so a few real contract tests are still needed.
</details>

### 27. Rows in a parametrized table may safely depend on each other, such as a "fetch the created one" row after a "create" row.

- [ ] True
- [ ] False

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** False

**Explanation:** Rows must set up what they need; order can change, rows can be skipped or run in parallel, and a failed row breaks the next.
</details>

### 28. `json.load` preserves numbers, booleans and `null` as Python `int`, `bool` and `None`.

- [ ] True
- [ ] False

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** True

**Explanation:** Unlike CSV, JSON keeps types and nesting.
</details>

### 29. Setting `additionalProperties: false` on every schema is best practice because it makes tests stricter.

- [ ] True
- [ ] False

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** False

**Explanation:** It makes every test fail when the backend adds a harmless field; reserve it for cases where an extra field would be a real problem.
</details>

### 30. Pydantic's default lax mode may convert `"5"` to `5`, which is risky for contract tests.

- [ ] True
- [ ] False

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** True

**Explanation:** Coercion helps applications but can hide wrong types; use strict mode for contract checks.
</details>

### 31. When you are testing the real API itself, replacing it with a mock still gives a meaningful result.

- [ ] True
- [ ] False

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** False

**Explanation:** A mocked API test proves nothing about the service; mock the outgoing calls made by the code under test, not the system under test.
</details>

### 32. A `session`-scoped fixture that returns a mutable user record is safe as long as the tests run quickly.

- [ ] True
- [ ] False

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** False

**Explanation:** One test editing the record changes it for every later test; wide scopes are for immutable, expensive resources.
</details>

### 33. A flaky test is best fixed by adding `time.sleep()` or automatic reruns.

- [ ] True
- [ ] False

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** False

**Explanation:** Both hide the real defect and slow the suite; find the shared state, fix the cause and prove it with seeds, parallel runs and repeats.
</details>

### 34. `@responses.activate` is lenient about unused stubs, while `responses.RequestsMock()` is strict by default.

- [ ] True
- [ ] False

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** True

**Explanation:** The context manager fails at exit if a registered stub was never fired.
</details>

### 35. The right way to build expected values is to run the API once and paste its response into the table.

- [ ] True
- [ ] False

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** False

**Explanation:** That confirms the API equals itself; expectations come from requirements and are then verified against the API.
</details>


## Part 3: Code Prediction

### 36. What does this print?

```python
import csv, io
rows = list(csv.DictReader(io.StringIO("id,expected\n1,200\n101,404\n")))
print(rows[0]["expected"] == 200, type(rows[0]["id"]).__name__, rows[1]["id"] + "!")
```

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** `False str 101!`

**Explanation:** `DictReader` yields strings, so `'200' == 200` is `False`, the id is `str`, and `+ "!"` concatenates text.
</details>

### 37. What does this print?

```python
import json
case = json.loads('{"id": 5, "active": true, "note": null, "tags": ["a"]}')
print(type(case["id"]).__name__, type(case["active"]).__name__, case["note"], type(case["tags"]).__name__)
```

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** `int bool None list`

**Explanation:** `json.loads` keeps JSON types: number to `int`, `true` to `bool`, `null` to `None`, array to `list`.
</details>

### 38. What is printed?

```python
import requests, responses
@responses.activate
def run():
    u = "https://api.example.com/x"
    responses.add(responses.GET, u, status=503)
    responses.add(responses.GET, u, status=503)
    responses.add(responses.GET, u, json={"ok": True}, status=200)
    codes = [requests.get(u, timeout=5).status_code for _ in range(5)]
    print(codes, len(responses.calls))
run()
```

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** `[503, 503, 200, 200, 200] 5`

**Explanation:** Registered replies are served in order and the last one keeps being returned; every call, five in total, is recorded in `responses.calls`.
</details>

### 39. What is printed?

```python
import requests, responses
@responses.activate
def run():
    u = "https://api.example.com/x"
    responses.add(responses.GET, u, body=requests.exceptions.ConnectTimeout("slow"))
    try:
        requests.get(u, timeout=5)
    except requests.exceptions.Timeout as e:
        print("caught", type(e).__name__, len(responses.calls))
run()
```

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** `caught ConnectTimeout 1`

**Explanation:** The exception instance passed as `body` is raised; `ConnectTimeout` is a subclass of `Timeout`, so it is caught, and the attempted call is still recorded once.
</details>

### 40. What does this print?

```python
from unittest.mock import Mock
svc = Mock()
svc.fetch.side_effect = [ConnectionError("down"), {"ok": True}]
out = []
for _ in range(2):
    try:
        out.append(svc.fetch())
    except ConnectionError:
        out.append("err")
    except StopIteration:
        out.append("stop")
print(out, svc.fetch.call_count)
```

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** `['err', {'ok': True}] 2`

**Explanation:** A list `side_effect` is consumed one item per call: the first raises `ConnectionError`, the second returns the dict. `call_count` is 2.
</details>

### 41. `lib.py` defines `fetch()` returning `"real"`. `client.py` has `from lib import fetch` and `def run(): return fetch()`. What does `main.py` print?

```python
from unittest.mock import patch
import client

with patch("lib.fetch", return_value="fake"):
    a = client.run()
with patch("client.fetch", return_value="fake"):
    b = client.run()
print(a, b, client.run())
```

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** `real fake real`

**Explanation:** `client` holds its own reference created by `from lib import fetch`, so patching `lib.fetch` (where it is defined) has no effect; patching `client.fetch` (where it is used) does. After each `with` block the patch is undone.
</details>

### 42. pytest runs the tests in file order. What is the summary line?

```python
import pytest
@pytest.fixture(scope="module")
def cart():
    return []
def test_a(cart):
    cart.append("apple")
    assert cart == ["apple"]
def test_b(cart):
    assert cart == []
def test_c(cart):
    assert len(cart) == 1
```

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** `1 failed, 2 passed` (`test_b` fails)

**Explanation:** The module-scoped `cart` is one shared list: `test_a` appends, `test_b` expects it empty and fails, and `test_c` sees one item and passes.
</details>

### 43. pytest runs the tests in file order. What is the summary line?

```python
import pytest
@pytest.fixture
def user():
    return {"name": "Ana"}
def test_rename(user):
    user["name"] = "Bob"
    assert user["name"] == "Bob"
def test_default(user):
    assert user["name"] == "Ana"
```

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** `2 passed`

**Explanation:** The default function scope builds a new dict for each test, so renaming in `test_rename` cannot leak into `test_default`.
</details>

### 44. What does this print?

```python
from jsonschema import Draft202012Validator
s = {"type":"object","properties":{"id":{"type":"integer"},"email":{"type":"string","format":"email"}}}
v = Draft202012Validator(s)
print(v.is_valid({}), v.is_valid({"email":"not-an-email"}), v.is_valid({"id":"5"}))
```

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** `True True False`

**Explanation:** Without `required`, `{}` is valid; `format` is only an annotation without a format checker, so the bad email passes; `"5"` is not an integer, so the third call is `False`.
</details>

### 45. What does this print?

```python
from jsonschema import Draft202012Validator
s = {"type":"object","required":["id","name"],"properties":{"id":{"type":"integer"},"name":{"type":"string"}},"additionalProperties":False}
errs = Draft202012Validator(s).iter_errors({"id":"5","extra":1})
print(sorted(e.validator for e in errs))
```

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** `['additionalProperties', 'required', 'type']`

**Explanation:** `iter_errors` reports every violation: `id` has the wrong type, `name` is missing, and `extra` is not allowed.
</details>

### 46. What does this print?

```python
from pydantic import BaseModel, ConfigDict, ValidationError
class A(BaseModel):
    id: int
class B(BaseModel):
    model_config = ConfigDict(strict=True)
    id: int
a = A.model_validate({"id": "5"})
print(repr(a.id), type(a.id).__name__)
try:
    B.model_validate({"id": "5"})
except ValidationError as e:
    print("strict fails:", e.errors()[0]["type"])
try:
    A.model_validate({"id": "five"})
except ValidationError as e:
    print("lax fails:", e.errors()[0]["type"])
```

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** `5 int`, then `strict fails: int_type`, then `lax fails: int_parsing`

**Explanation:** Lax mode coerces `"5"` to the integer 5, strict mode rejects a string for an int, and `"five"` cannot be parsed even in lax mode.
</details>

### 47. What is the pytest summary line?

```python
import pytest
CASES = [
    pytest.param(1, id="ok"),
    pytest.param(0, id="known-bug", marks=pytest.mark.xfail(reason="bug")),
    pytest.param(2, id="strict-fixed", marks=pytest.mark.xfail(strict=True)),
]
@pytest.mark.parametrize("n", CASES)
def test_n(n):
    assert n != 0
```

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** `1 failed, 1 passed, 1 xfailed`

**Explanation:** `ok` passes; `known-bug` fails as expected so it is xfailed; `strict-fixed` passes unexpectedly, and with `strict=True` an unexpected pass is reported as a failure.
</details>

### 48. What does pytest report for this file?

```python
import pytest
def load():
    return []
@pytest.mark.parametrize("row", load())
def test_rows(row):
    assert False
```

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** `1 skipped`

**Explanation:** An empty parameter set makes pytest skip the test ("got empty parameter set") instead of failing, so a broken data file can hide behind a green run.
</details>

### 49. What does this print?

```python
import requests, responses
@responses.activate
def run():
    responses.add(responses.GET, "https://api.example.com/users", json=[])
    try:
        requests.get("https://api.example.com/users/", timeout=5)
        print("matched")
    except requests.exceptions.ConnectionError:
        print("ConnectionError")
run()
```

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** `ConnectionError`

**Explanation:** The registered URL has no trailing slash, so the request does not match any stub and `responses` raises `ConnectionError`.
</details>

### 50. What does this print?

```python
from unittest.mock import Mock
m = Mock()
m.send("a"); m.send("b")
m.send.assert_called_with("b")
try:
    m.send.assert_called_once_with("b")
except AssertionError:
    print("not once")
print(m.send.call_count)
```

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** `not once`, then `2`

**Explanation:** `assert_called_with` checks only the last call, so it passes, but `assert_called_once_with` fails because `send` was called twice; use `call_count` when the number of calls matters.
</details>

### 51. What does this print?

```python
import requests, responses
@responses.activate
def run():
    responses.add(responses.GET, "https://api.example.com/a", json={"n": 1})
    responses.add(responses.GET, "https://api.example.com/b", json={"n": 2})
    requests.get("https://api.example.com/a", timeout=5)
    requests.get("https://api.example.com/a", timeout=5)
    responses.assert_call_count("https://api.example.com/a", 2)
    print(len(responses.calls), responses.calls[1].request.url.endswith("/a"))
    with responses.RequestsMock() as r:
        r.add(responses.GET, "https://x.test/", json={})
try:
    run()
except AssertionError as e:
    print("strict mock failed")
```

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** `2 True`, then `strict mock failed`

**Explanation:** The decorator is lenient about the unused `/b` stub, and `assert_call_count` passes for two calls to `/a`. The `RequestsMock()` context manager registers a stub that is never called and raises `AssertionError` when the block exits.
</details>


## Part 4: Fill in the Blank

### 52. The standard-library reader that yields each CSV row as a dictionary keyed by the header names is `csv.________`.

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** `DictReader`

**Explanation:** It returns strings only, so you convert types yourself.
</details>

### 53. To read an Excel-exported CSV that starts with a BOM, open the file with `encoding="________"`.

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** `utf-8-sig`

**Explanation:** It removes the invisible byte order mark so the first header is clean.
</details>

### 54. The JSON Schema keyword that lists keys which must be present is `________`; `properties` alone does not do this.

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** `required`

**Explanation:** Without it, a schema accepts `{}`.
</details>

### 55. To give one data row its own readable id and marks such as `xfail`, wrap it in `pytest.________(...)`.

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** `param`

**Explanation:** `pytest.param(..., id="...", marks=...)` makes failures show which row broke.
</details>

### 56. To check how many times one URL was called in `responses`, use `responses.________(url, count)`.

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** `assert_call_count`

**Explanation:** Its failure message states the expected and actual numbers.
</details>

### 57. To simulate a network timeout in `responses`, pass an exception ________ (not the class) as `body`.

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** instance (object)

**Explanation:** Passing the exception object makes `responses` raise it.
</details>

### 58. To replay the exact order of a failed random run, use `pytest --randomly-________=12345`.

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** `seed`

**Explanation:** `pytest-randomly` prints the seed in the header; reusing it reproduces the same order.
</details>

### 59. In Pydantic v2, `ConfigDict(extra="________")` rejects keys not declared on the model.

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** `forbid`

**Explanation:** It is the model counterpart of `additionalProperties: false` in JSON Schema.
</details>


## Part 5: Matching

### 60. Match each test double to its description. Write your answers as 1-X, 2-X, 3-X, 4-X.

| # | Item | | Letter | Description |
|---|------|---|--------|-------------|
| 1 | Stub | | A | Wraps the real thing, records calls and still does the real work |
| 2 | Mock | | B | A simplified but working implementation, such as an in-memory dictionary acting as a database |
| 3 | Fake | | C | Returns canned answers with no checking logic |
| 4 | Spy | | D | Answers and records calls so interactions can be verified |

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** 1-C, 2-D, 3-B, 4-A

**Explanation:** A stub answers, a mock answers and remembers, a fake actually works in a simplified way, and a spy is the real object being watched.
</details>

### 61. Match each JSON Schema or Pydantic feature to its purpose. Write your answers as 1-X, 2-X, 3-X, 4-X, 5-X.

| # | Item | | Letter | Description |
|---|------|---|--------|-------------|
| 1 | `oneOf` | | A | Lists every violation instead of stopping at the first |
| 2 | `anyOf` | | B | Data must match all sub-schemas |
| 3 | `allOf` | | C | Data must match at least one sub-schema |
| 4 | `additionalProperties: false` | | D | Rejects keys that are not listed in `properties` |
| 5 | `iter_errors` | | E | Data must match exactly one sub-schema; matching two fails |

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** 1-E, 2-C, 3-B, 4-D, 5-A

**Explanation:** `oneOf` is exactly one, `anyOf` at least one, `allOf` all of them; `additionalProperties: false` bans unlisted keys and `iter_errors` reports all problems.
</details>

### 62. Match each isolation tool to what it does. Write your answers as 1-X, 2-X, 3-X, 4-X, 5-X.

| # | Item | | Letter | Description |
|---|------|---|--------|-------------|
| 1 | `pytest-randomly` | | A | Gives each test its own temporary directory |
| 2 | `pytest-xdist` | | B | Runs the selected test many times with `--count` |
| 3 | `pytest-repeat` | | C | Shuffles test order and prints a seed to replay it |
| 4 | `tmp_path` | | D | Sets environment variables or attributes and undoes them after the test |
| 5 | `monkeypatch` | | E | Runs tests in parallel worker processes with `-n` |

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** 1-C, 2-E, 3-B, 4-A, 5-D

**Explanation:** Together they prove isolation: random order, parallel workers and repeats, with `tmp_path` and `monkeypatch` isolating files and environment.
</details>
