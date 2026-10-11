# Data-Driven API Testing

## Learning Objectives

By the end of this lesson you will be able to:

- Define **data-driven testing (DDT)** and explain how it differs from hard-coded, one-function-per-scenario tests.
- Separate **test logic** from **test data** and decide what belongs in each.
- Name the common data sources (inline lists, files, databases) and choose between them.
- Design a test data table with inputs, expected outputs and readable case names.
- Build positive, negative and boundary data sets for an API endpoint.
- Apply `pytest.mark.parametrize` to real API calls using `ids`, `pytest.param` and per-row `marks`.
- Write a small test data builder (factory) to keep rows short.
- Read a PyTest report and tell exactly which data row failed.
- Recognise the main pitfalls: too many rows, hidden coupling and shared mutable data.

---

## Why This Matters

This week you are building a professional API test suite: API testing on Wednesday, accessibility checks on Thursday and CI/CD automation on Friday. Every one of those pieces depends on tests that are cheap to extend and easy to read. A CI pipeline that runs your tests on every commit is only useful if a red result tells a developer *what* broke within seconds.

On Monday and Tuesday you sent requests with `requests`, validated status codes and JSON, and used `parametrize` inline for small lists. Real endpoints have many fields, each with rules (required, type, range, format). Covering them means dozens of input combinations. If you write one test function per combination, you get a wall of near-duplicate code, and changing one URL means editing fifty functions.

Data-driven testing fixes that: you write the logic **once** and feed it **many rows**. Adding a scenario becomes adding one line of data. That is how a small team gets broad coverage from a small suite, and it is the foundation for the reusable framework you will assemble later today.

---

## The Concept

### 1. What Is Data-Driven Testing?

**Data-driven testing** runs the same test procedure many times with different inputs and expected results, where the data is kept apart from the procedure.

**Analogy:** A teacher writes one marking guide ("compare the student's answer with the right answer; award a point on a match") and applies it to thirty students. She does not write thirty guides. The guide is your test logic. The students' answers are your data.

#### The hard-coded way

Imagine you want to check that `GET /posts/{id}` returns the right status for several ids on JSONPlaceholder (a free fake REST API at `https://jsonplaceholder.typicode.com`):

```python
import requests

BASE_URL = "https://jsonplaceholder.typicode.com"


def test_post_1_exists():
    response = requests.get(f"{BASE_URL}/posts/1", timeout=10)
    assert response.status_code == 200


def test_post_100_exists():
    response = requests.get(f"{BASE_URL}/posts/100", timeout=10)
    assert response.status_code == 200


def test_post_101_missing():
    response = requests.get(f"{BASE_URL}/posts/101", timeout=10)
    assert response.status_code == 404
```

Line by line:

- `import requests` loads the HTTP library you used on Monday.
- `BASE_URL = ...` stores the API root in one place so it is not repeated in every call.
- Each `def test_...` is a separate PyTest test, discovered because its name starts with `test_`.
- `requests.get(..., timeout=10)` sends a GET request; the timeout stops a hung server from freezing your run.
- `assert response.status_code == ...` is the check. PyTest reports a failure if it is false.

Three functions, three copies of the same two lines. Now imagine twenty ids, or the base URL changing to a staging server. This does not scale.

#### The data-driven way

```python
import pytest
import requests

BASE_URL = "https://jsonplaceholder.typicode.com"


@pytest.mark.parametrize(
    "post_id, expected_status",
    [
        (1, 200),
        (100, 200),
        (101, 404),
    ],
)
def test_get_post_status(post_id, expected_status):
    response = requests.get(f"{BASE_URL}/posts/{post_id}", timeout=10)
    assert response.status_code == expected_status
```

Line by line:

- `@pytest.mark.parametrize(...)` is the decorator you met on Tuesday. It tells PyTest to run the function once per row.
- `"post_id, expected_status"` is a comma-separated string naming the function arguments that receive each row's values.
- The list of tuples is the **data**. Each tuple is one test case: `(1, 200)` means "id 1 should give 200".
- `def test_get_post_status(post_id, expected_status)` is the **logic**. Its parameter names match the names in the string.
- The f-string builds the URL from the row's `post_id`, and the assert compares against the row's `expected_status`.

PyTest generates three separate tests from one function. A new scenario costs one line.

#### Benefits versus hard-coded tests

| Benefit | Why it helps |
|---------|--------------|
| Less duplication | One place to fix when the URL, header or auth changes |
| Broader coverage | Adding a case is trivial, so you actually add them |
| Readability | The table shows at a glance what is covered |
| Clear reports | Each row is its own pass/fail result |
| Collaboration | Non-programmers can review (and later edit) data |

#### When *not* to use it

DDT suits tests where the **steps are identical** and only values differ. If each scenario needs different steps (log in, create, update, delete in unique orders), write separate tests. Forcing different workflows into one parametrized function creates `if` branches inside the test, which is a warning sign (see Pitfalls).

**Common mistake:** Parametrizing everything by reflex. Ask: "Is the logic really the same for every row?" If not, split the tests.

---

### 2. Separating Test Logic from Test Data

**Test logic** is *how* you test: which endpoint and method, the arrange-act-assert steps, how you compare results. **Test data** is *what* you test with: values sent and values expected.

| Belongs in logic (code) | Belongs in data (rows) |
|-------------------------|------------------------|
| Endpoint and HTTP method | Input values (ids, payload fields, query params) |
| Steps: arrange, act, assert | Expected status code |
| How to compare actual and expected | Expected field values or error text |
| Setup and cleanup (fixtures) | A descriptive name for each case |
| Shared helpers | Category of the row (positive, negative, boundary) |

**A practical test of your separation:** could a manual tester add a new scenario without understanding Python? If the answer is "yes, they add a row", your design is good. The next Wednesday lesson shows how to move rows into CSV and JSON files so that this is literally true.

**Real-world scenario:** A team tests a `/products` search endpoint. Early on, a developer hard-codes 40 tests. When the endpoint adds an `api-version` header, someone must edit 40 functions, and two get forgotten, so they silently hit the old version. With one parametrized function, the header is added in one line.

**Common mistake:** Leaking data into logic, for example `if payload.get("age") == -1:` inside the test, or hard-coding `assert status == 400` while the table also holds a status column. Logic should *use* the row, never *guess* about it.

---

### 3. Data Sources Overview

Where can the rows live?

| Source | Example | Strengths | Weaknesses | Use when |
|--------|---------|-----------|------------|----------|
| **Inline list** in the test file | `CASES = [...]` | Simplest; visible beside the test; no file I/O | Gets long; editing needs code changes | Under roughly 15 rows; today's focus |
| **Files** (CSV, JSON, YAML) | `cases.csv` | Non-programmers can edit; reusable across tests; easy to diff | Needs loading code; typing can be lost (CSV is all text) | Larger or shared tables (next lesson) |
| **Database** | `SELECT ... FROM test_cases` | Live data; very large sets; real production-like values | Setup, credentials, state drift, slow | Rarely, for verifying API results against stored records |
| **Generated** in code | `itertools.product(...)` | Compact for combinations | Harder to read; must stay deterministic | Matrices of roles x actions, boundary values |

Guidance for beginners: start inline. Move to files when the list outgrows the test file or others need to edit it. Reach for a database only when you genuinely need to compare an API response to stored data. A database also adds a dependency: if the DB is down, your API tests fail for the wrong reason.

**File-based loading is the next lesson.** Here we stay with inline data so we can focus on design and PyTest mechanics.

---

### 4. Designing a Test Data Table

Before writing code, sketch the table. Each row should have:

1. **A case ID** that says what is being tested (`user-not-found`).
2. **Inputs**: what you send.
3. **Expected outputs**: at minimum a status code, ideally a key field or message.
4. **Optionally**: a tag, a bug reference or a note.

Example for `GET /posts` filtering on JSONPlaceholder:

| case_id | query params | expected_status | expected_count |
|---------|--------------|-----------------|----------------|
| limit-five | `_limit=5` | 200 | 5 |
| limit-one | `_limit=1` | 200 | 1 |
| by-user-1 | `userId=1` | 200 | 10 |
| unknown-user | `userId=9999` | 200 | 0 |

Notice that "unknown user" returns `200` with an empty list, not an error. That is a *design decision* of the API that your table documents. Always decide expected values from the **specification** (or the documented behaviour), not by copying whatever the API returned. Copying actual output into the expected column makes a test that can never catch a regression.

**Tip on expected outputs:** Prefer a few *meaningful* expectations over many trivial ones. A status code plus one business field (`userId`, `title`, count) beats comparing the entire JSON blob, which breaks on irrelevant changes.

---

### 5. Positive, Negative and Boundary Data Sets

A balanced data set has three kinds of rows.

**Positive data** is valid input where success is expected. It proves the feature works at all.

**Negative data** is invalid or unexpected input where a clean failure is expected: not found, bad request, unauthorised. It proves the API refuses bad input gracefully instead of crashing (a `500` is nearly always a bug).

**Boundary data** sits at the edge of a valid range, where off-by-one mistakes (`<` versus `<=`) hide. For a valid range 1-100, test `0, 1, 2, 99, 100, 101`.

#### Equivalence partitioning in one minute

Split inputs into groups the system should treat identically, then pick one representative from each group. For `/posts/{id}` with 100 posts:

| Partition | Example | Expected |
|-----------|---------|----------|
| Valid id | `50` | 200 |
| Above the range | `500` | 404 |
| Zero or negative | `0`, `-1` | 404 |
| Wrong type | `abc` | 404 on JSONPlaceholder (a real API might return 400) |

Combine with boundaries (`1`, `100`, `101`) and you have strong coverage from about eight rows, not 500.

#### A boundary helper

```python
def boundary_values(low, high):
    return [low - 1, low, low + 1, high - 1, high, high + 1]


print(boundary_values(1, 100))   # [0, 1, 2, 99, 100, 101]
```

Line by line:

- `def boundary_values(low, high)` takes the smallest and largest valid values.
- The returned list contains the value just below the range, the lower edge, just inside it, just inside the upper edge, the upper edge, and just above.
- The `print` call shows the result for 1-100; it is for learning, not part of a test.

**Other categories that deserve a row:** empty strings, very long strings, special characters (`O'Brien`, `<b>`, accented letters, emoji), type confusion (`"5"` versus `5`), and duplicates.

**Common mistake:** Testing only happy paths, or adding 40 random "valid" values that all hit the same partition. More rows is not more coverage; different *kinds* of rows are.

---

### 6. `parametrize` Applied to API Calls

You already know the basics. Now let us use the full toolbox: a shared base URL fixture, `ids`, `pytest.param` and `marks`.

#### Step 1: a fixture for the base URL

```python
import pytest
import requests


@pytest.fixture(scope="session")
def base_url():
    return "https://jsonplaceholder.typicode.com"
```

- `@pytest.fixture(scope="session")` creates the value once for the whole run (fixtures were covered Tuesday).
- The function returns the URL; any test that lists `base_url` as a parameter receives it.

#### Step 2: a table of rows with `pytest.param`

```python
POST_LOOKUP_CASES = [
    pytest.param(1,   200, id="first-post"),
    pytest.param(2,   200, id="second-post"),
    pytest.param(100, 200, id="last-valid-post"),
    pytest.param(101, 404, id="one-past-last"),
    pytest.param(0,   404, id="zero-id"),
    pytest.param(-1,  404, id="negative-id"),
]
```

- Each `pytest.param(...)` wraps one row. The positional values map to the parameter names in order.
- `id="..."` gives the row a readable name. Without it PyTest makes names such as `1-200`, which tell you nothing.
- The list is a module-level constant, named in capitals by convention, placed above the test so the data is easy to find.

#### Step 3: the test logic

```python
@pytest.mark.parametrize("post_id, expected_status", POST_LOOKUP_CASES)
def test_get_post_by_id_status(base_url, post_id, expected_status):
    # Act
    response = requests.get(f"{base_url}/posts/{post_id}", timeout=10)

    # Assert
    assert response.status_code == expected_status, (
        f"GET /posts/{post_id}: expected {expected_status}, "
        f"got {response.status_code}"
    )
```

- Parameters from the fixture (`base_url`) and from parametrize (`post_id`, `expected_status`) mix freely in the signature.
- The `# Act` and `# Assert` comments mark the arrange-act-assert structure from Tuesday.
- The text after the comma in `assert` is a custom failure message. It names the endpoint, the expectation and the actual result so you do not have to rerun to debug.

Representative output:

```
test_posts.py::test_get_post_by_id_status[first-post] PASSED
test_posts.py::test_get_post_by_id_status[second-post] PASSED
test_posts.py::test_get_post_by_id_status[last-valid-post] PASSED
test_posts.py::test_get_post_by_id_status[one-past-last] PASSED
test_posts.py::test_get_post_by_id_status[zero-id] PASSED
test_posts.py::test_get_post_by_id_status[negative-id] PASSED
```

#### Checking content, not just status

Status codes alone are shallow. Add expected content to each row:

```python
USER_CASES = [
    pytest.param(1, "Leanne Graham", "Bret", id="user-1"),
    pytest.param(2, "Ervin Howell", "Antonette", id="user-2"),
    pytest.param(3, "Clementine Bauch", "Samantha", id="user-3"),
]


@pytest.mark.parametrize("user_id, expected_name, expected_username", USER_CASES)
def test_user_details(base_url, user_id, expected_name, expected_username):
    response = requests.get(f"{base_url}/users/{user_id}", timeout=10)

    assert response.status_code == 200
    body = response.json()
    assert body["name"] == expected_name
    assert body["username"] == expected_username
```

- Three data columns feed three assertions; the logic stays four lines.
- `response.json()` parses the body into a Python dict (Monday topic).
- Separate asserts give a precise failure: you learn whether the name or the username mismatched.

#### Parametrizing query parameters

For filters, pass the params dict as data:

```python
FILTER_CASES = [
    pytest.param({"userId": 1},      10, id="user-1-has-10-posts"),
    pytest.param({"_limit": 5},       5, id="limit-5"),
    pytest.param({"userId": 9999},    0, id="unknown-user-empty"),
]


@pytest.mark.parametrize("params, expected_count", FILTER_CASES)
def test_posts_filter_count(base_url, params, expected_count):
    response = requests.get(f"{base_url}/posts", params=params, timeout=10)

    assert response.status_code == 200
    assert len(response.json()) == expected_count
```

- `params=params` lets `requests` build the query string (`?userId=1`) and handle encoding for you.
- `len(response.json())` counts items in the returned list.

#### Row-level marks: skip and xfail

`pytest.param` accepts `marks=` so one row can be treated specially.

```python
MIXED_CASES = [
    pytest.param(1, 200, id="normal"),
    pytest.param(
        "abc", 400, id="text-id-should-be-400",
        marks=pytest.mark.xfail(reason="BUG-482: API returns 404, spec says 400"),
    ),
    pytest.param(
        101, 404, id="needs-staging-only",
        marks=pytest.mark.skip(reason="Only valid on staging data"),
    ),
]
```

- `xfail` means "expected to fail". The row runs, but a failure is reported as XFAIL rather than breaking the build. If the bug gets fixed, the row reports XPASS, which alerts you to remove the mark. Use it for **known defects with a tracking id**.
- `skip` means "do not run". Use it for temporarily irrelevant rows, always with a reason.
- You can also apply a custom marker you registered earlier, such as `marks=pytest.mark.smoke`, to include just that row in a fast run (`pytest -m smoke`).

**Common mistakes with `parametrize`:**

- Parameter names in the string do not match the function arguments: PyTest errors at collection time.
- A tuple of the wrong length: `(1, 200, "extra")` for two names.
- Duplicate `id` values: PyTest silently adds suffixes such as `normal0`, `normal1`, which hurts readability.
- Using `xfail` without a reason, so nobody remembers why.

**Where does the ID come from if I do not give one?** PyTest builds it from the values. Simple types become `1-200`; objects like dicts become `params0`. Always set `id` yourself for anything non-trivial.

---

### 7. Test Data Builders and Factories

As payloads grow, rows become long and noisy. A **builder** (or factory) is a small function that returns a valid default object and lets each row override just what matters.

```python
def make_post(**overrides):
    base = {
        "title": "Quality matters",
        "body": "Automated checks catch regressions early.",
        "userId": 1,
    }
    return {**base, **overrides}
```

Line by line:

- `def make_post(**overrides)` collects any keyword arguments into a dict called `overrides`.
- `base` is a complete, valid payload: your "known good" baseline.
- `{**base, **overrides}` builds a new dict: first all base keys, then the overrides on top, so an override replaces the matching default.
- Returning a **new** dict every call means rows cannot accidentally modify each other (see shared mutable data below).

Using it in rows:

```python
CREATE_POST_CASES = [
    pytest.param(make_post(),                      id="valid-baseline"),
    pytest.param(make_post(title=""),              id="empty-title"),
    pytest.param(make_post(title="x" * 500),       id="very-long-title"),
    pytest.param(make_post(userId=999),            id="unknown-user-id"),
    pytest.param(make_post(title="Café \U0001F600"), id="unicode-title"),
]


@pytest.mark.parametrize("payload", CREATE_POST_CASES)
def test_create_post_echoes_title(base_url, payload):
    response = requests.post(f"{base_url}/posts", json=payload, timeout=10)

    assert response.status_code == 201
    assert response.json()["title"] == payload["title"]
```

- Every row differs from the baseline by **one** thing, so a failure points straight at the cause.
- `json=payload` serialises the dict and sets the JSON content type.
- JSONPlaceholder returns `201` and echoes the sent data back with a fake new id (representative: `{"title": "...", "body": "...", "userId": 1, "id": 101}`). It does **not** save anything.

**Important honesty note about this practice API:** JSONPlaceholder does not validate input. A "missing title" or "empty title" payload will still get `201`. That makes it ideal for learning the *mechanics* of DDT, but when you test your own API (or the Project 2 target), your negative rows will expect `400` or `422`. When practising here, record what the API really does and note that a real service would reject those payloads.

**Builders for random data:** The `Faker` library generates realistic names and emails. If you use it, set a seed (`Faker.seed(1234)`) so the "random" values are identical on every run. A failure you cannot reproduce is worthless.

**Generating combinations:** `itertools.product` produces every pairing from several lists:

```python
import itertools

user_ids = [1, 5, 10]
limits = [1, 3]

COMBOS = [
    pytest.param(uid, lim, id=f"user{uid}-limit{lim}")
    for uid, lim in itertools.product(user_ids, limits)
]
```

- `itertools.product(user_ids, limits)` yields `(1, 1), (1, 3), (5, 1), ...`: 3 x 2 = 6 pairs.
- The list comprehension wraps each pair in `pytest.param` with an id built by an f-string.
- Keep generated data deterministic (no `random` without a seed, no current time) so the same rows exist on every run.

---

### 8. Keeping Data Readable and Maintainable

| Practice | Reason |
|----------|--------|
| Give every row a meaningful `id` | The report reads like a list of scenarios |
| Name data constants clearly (`POST_LOOKUP_CASES`) | Easy to find and reason about |
| Put the table directly above its test | Data and logic are viewed together |
| One behaviour per test function | A failure points at one thing |
| Use builders for large payloads | Short rows, one visible difference per row |
| Group rows with blank lines or comments (`# positive`, `# boundary`) | Reviewers see the coverage categories |
| Keep expected values derived from the spec | Tests catch regressions instead of copying them |
| Review data like code | A wrong expected value creates a false pass or false fail |
| Keep logic out of rows | Rows are data, not programs |

**Maintenance scenario:** The product team renames the field `userId` to `authorId`. With a builder, you change one line in `make_post`. With 60 inline dicts, you change 60 lines and probably miss one.

**Separate positive and negative tests where assertions differ.** Positive rows often check body content; negative rows check error codes. Two parametrized functions (`test_create_post_ok`, `test_create_post_rejected`) are clearer than one function with an `if expected_status == 201:` branch.

---

### 9. Reporting Which Data Row Failed

When one function becomes dozens of tests, the report must tell you *which row* failed. PyTest helps in four ways.

**1. The row ID is in the test name.** A failure looks like:

```
FAILED test_posts.py::test_get_post_by_id_status[one-past-last]
```

Representative output; you immediately know the scenario is "one past last".

**2. The failure message shows the values.** With the custom assert message from section 6:

```
AssertionError: GET /posts/101: expected 404, got 200
```

**3. Select or rerun a single row.** Copy the ID into `-k` or use the full node id:

```
pytest -k "one-past-last" -v
pytest "test_posts.py::test_get_post_by_id_status[one-past-last]"
```

**4. Reports in CI keep the IDs.** JUnit XML and HTML reports (relevant to Friday's CI/CD lesson) list each row as its own test case, so dashboards show "which scenarios broke" without opening logs.

Without good IDs, you get `test_get_post_by_id_status[101-404]`, which a colleague who did not write the test cannot interpret. With IDs, even a manager reading the report understands the failure.

**Tip:** Also put identifying details inside assertion messages (endpoint, payload summary, response body excerpt such as `response.text[:200]`). Limit the excerpt so a giant HTML error page does not flood the log.

---

### 10. Pitfalls

#### Pitfall 1: too many rows

Ten thousand rows means ten thousand HTTP calls. A suite that takes an hour will stop being run. Choose rows by **partition and boundary**, not brute force. If you need huge volume, that is a performance test, not a functional one. Mark slower sets (`marks=pytest.mark.slow`) so they run nightly rather than on every commit.

#### Pitfall 2: hidden coupling between rows

Rows must not depend on each other. Example of a trap:

```python
CASES = [
    pytest.param({"title": "first"},  201, id="create"),
    pytest.param({"id": 101},        200, id="fetch-the-created-one"),  # depends on previous row!
]
```

PyTest may run rows in a different order (or in parallel, with plugins), and a skipped or failed row breaks the next. Each row must **set up what it needs** itself (see "Test isolation" later today). A related coupling is between data and environment: a row that assumes "user 7 has exactly 3 orders" fails whenever someone changes that record.

#### Pitfall 3: shared mutable data

This is a classic Python trap:

```python
BASE_PAYLOAD = {"title": "Quality", "body": "text", "userId": 1}

CASES = [
    pytest.param(BASE_PAYLOAD, id="baseline"),
    pytest.param(BASE_PAYLOAD, id="same-object-again"),
]


def test_bad(base_url):
    payload = BASE_PAYLOAD
    payload["title"] = ""          # mutates the shared dict for EVERY later test
```

If a test modifies a dict that other rows also reference, later tests see changed data. Whether they pass then depends on execution order. Fixes:

- Use a **builder** that returns a fresh dict each call (section 7).
- If a test must modify data, copy first: `payload = dict(payload)` (or `copy.deepcopy(payload)` for nested data).
- Treat table data as read-only.

#### Pitfall 4: logic creeping into the test

If the test body fills with `if row_type == "negative":` branches, you are forcing different behaviours into one function. Split it.

#### Pitfall 5: expected values copied from the actual output

If you run the API, paste its response into the table and call it expected, you have a test that confirms the API equals itself. Take expectations from requirements, then verify them against the API.

#### Pitfall 6: forgetting dependencies on external state

JSONPlaceholder's data is stable, which is why we use it. A real API's data changes. Prefer tests that create their own data, or assert on properties (status, schema, field types) rather than exact values from a shared database.

---

### 11. Practice Exercises

Use JSONPlaceholder. Write answers in a file such as `test_ddt_practice.py`; for each exercise, run `pytest -v` and read the row IDs.

#### Exercise 1: boundary ids

Test `GET /users/{id}` (JSONPlaceholder has 10 users). Use `boundary_values(1, 10)` to generate the ids. Build rows with `pytest.param` and an `id` for each, expecting `200` inside the range and `404` outside it.

**Solution**

```python
import pytest
import requests

BASE_URL = "https://jsonplaceholder.typicode.com"


def boundary_values(low, high):
    return [low - 1, low, low + 1, high - 1, high, high + 1]


USER_BOUNDARY_CASES = [
    pytest.param(uid, 200 if 1 <= uid <= 10 else 404, id=f"user-id-{uid}")
    for uid in boundary_values(1, 10)
]


@pytest.mark.parametrize("user_id, expected_status", USER_BOUNDARY_CASES)
def test_user_id_boundaries(user_id, expected_status):
    response = requests.get(f"{BASE_URL}/users/{user_id}", timeout=10)
    assert response.status_code == expected_status
```

Explanation: the list comprehension turns each boundary value into a row. The conditional expression `200 if 1 <= uid <= 10 else 404` computes the expectation **while building the data**, not inside the test, so the test logic stays simple. Representative result: ids `1, 2, 9, 10` pass with 200; ids `0` and `11` give 404. (The conditional in the data generator is derived from the spec "valid ids are 1-10", not from the API's output.)

#### Exercise 2: filter table with content checks

Create at least four rows for `GET /comments` using the `postId` query parameter: two valid post ids, one id with no comments (for example `9999`), and one boundary id (`100`). Check both status and the number of comments, recording the real count from the API for the valid rows.

**Solution**

```python
COMMENT_CASES = [
    pytest.param(1,    5, id="post-1"),
    pytest.param(2,    5, id="post-2"),
    pytest.param(100,  5, id="last-post"),
    pytest.param(9999, 0, id="no-such-post"),
]


@pytest.mark.parametrize("post_id, expected_count", COMMENT_CASES)
def test_comments_per_post(post_id, expected_count):
    response = requests.get(
        f"{BASE_URL}/comments", params={"postId": post_id}, timeout=10
    )
    assert response.status_code == 200
    comments = response.json()
    assert len(comments) == expected_count
    assert all(c["postId"] == post_id for c in comments)
```

Explanation: the last assertion verifies **every** returned comment belongs to the requested post, a content check beyond counting. For an empty list `all(...)` is `True`, so it passes harmlessly. Counts are representative of JSONPlaceholder (five comments per post); record what you observe and note that an unknown post id returns an empty list with status 200 rather than an error.

#### Exercise 3: builder and one-change-per-row

Write `make_post(**overrides)` as in the lesson, then create six `POST /posts` rows where each changes exactly one field (empty title, 500-character title, missing body via `body=None`, unicode title, huge `userId`, negative `userId`). Assert `201` and that the response echoes `title`. Then add a comment above the table explaining what a *real* API should probably do for the rows you consider invalid.

**Solution**

```python
def make_post(**overrides):
    base = {"title": "Quality matters", "body": "Checks catch regressions.", "userId": 1}
    return {**base, **overrides}


# JSONPlaceholder accepts everything. A real API should likely return 400/422
# for: empty-title, null-body, negative-user-id.
POST_ROWS = [
    pytest.param(make_post(title=""),            id="empty-title"),
    pytest.param(make_post(title="x" * 500),     id="long-title"),
    pytest.param(make_post(body=None),           id="null-body"),
    pytest.param(make_post(title="Café"),   id="unicode-title"),
    pytest.param(make_post(userId=10**9),        id="huge-user-id"),
    pytest.param(make_post(userId=-1),           id="negative-user-id"),
]


@pytest.mark.parametrize("payload", POST_ROWS)
def test_create_post_echoes_title(payload):
    response = requests.post(f"{BASE_URL}/posts", json=payload, timeout=10)
    assert response.status_code == 201
    assert response.json()["title"] == payload["title"]
```

Explanation: each row alters exactly one key from the valid baseline. The comment records the real-world expectation, which is the first step toward converting these rows into `xfail` or negative tests when you meet an API that validates input.

#### Exercise 4: positive, negative and an xfail row

Parametrize `GET /todos/{id}` with a positive row, a negative row (not found), and a row you mark `xfail` with a bug-style reason, such as expecting `400` for the text id `"abc"` (which JSONPlaceholder answers with `404`). Run and explain the report symbols.

**Solution**

```python
TODO_CASES = [
    pytest.param(1,     200, id="positive-existing"),
    pytest.param(99999, 404, id="negative-not-found"),
    pytest.param(
        "abc", 400, id="text-id-expected-400",
        marks=pytest.mark.xfail(reason="BUG-101: spec says 400, API returns 404"),
    ),
]


@pytest.mark.parametrize("todo_id, expected_status", TODO_CASES)
def test_get_todo_status(todo_id, expected_status):
    response = requests.get(f"{BASE_URL}/todos/{todo_id}", timeout=10)
    assert response.status_code == expected_status
```

Explanation: running `pytest -v` should show two `PASSED` and one `XFAIL` (representative). If the API were fixed to return 400, the third row would show `XPASS`, telling you to remove the mark. The positive/negative labels in the ids make coverage categories visible in the report.

---

### 12. Self-Check Quiz

**Q1.** Which of these belongs in test *data* rather than test *logic*?
a) The HTTP method  b) The expected status code for each case  c) The assertion operator  d) The timeout value

**Q2.** Why should you set `id=` on each `pytest.param`?
a) It makes tests run faster  b) It is required by PyTest  c) It gives readable names so you can see which row failed  d) It disables other markers

**Q3.** For a valid range of 1-50, which set is the best boundary-value choice?
a) `10, 20, 30`  b) `0, 1, 2, 49, 50, 51`  c) `1, 50`  d) `-100, 100`

**Q4.** Why does a builder like `make_post(**overrides)` return a **new** dict each time?
a) To make tests slower  b) So that one row or test cannot accidentally modify data used by another  c) Because dicts cannot be reused in Python  d) To avoid using JSON

**Q5.** What does an `xfail` mark on a single row communicate?
a) The row is skipped  b) The row is expected to fail because of a known defect, and an unexpected pass will be flagged  c) The whole suite should stop  d) The row passed

**Answers**

1. **b.** Expected values are data; method, operator and timeout are logic/configuration.
2. **c.** IDs show up in the report, for example `[one-past-last]`.
3. **b.** Test each edge and the value just beside it.
4. **b.** Returning a fresh dict prevents shared mutable data bugs.
5. **b.** The row runs; failure is tolerated and tracked, and an XPASS tells you the bug may be fixed.

---

### 13. Glossary

| Term | Meaning |
|------|---------|
| **Data-driven testing (DDT)** | Running one test procedure against many rows of input and expected output |
| **Test logic** | The steps and assertions of a test: the *how* |
| **Test data** | The inputs and expected results: the *what* |
| **Parametrize** | PyTest feature that runs a test once per data row |
| **`pytest.param`** | Wrapper for one row that lets you add an `id` and `marks` |
| **Test ID** | Readable name for a row shown in reports |
| **Positive / negative data** | Valid input expecting success / invalid input expecting a clean failure |
| **Boundary value** | A value at or next to the edge of an allowed range |
| **Equivalence partition** | A group of inputs the system should treat the same |
| **Builder / factory** | Function that returns a valid default object with optional overrides |
| **`xfail` / `skip`** | Marks for expected failure and for not running a row |
| **Shared mutable data** | A modifiable object referenced by multiple tests, a source of order-dependent failures |

---

## Summary

- Data-driven testing writes the test logic once and feeds it many rows, replacing duplicated functions with a table.
- Keep logic (steps, endpoint, assertions) separate from data (inputs, expected outputs, case names).
- Start with inline lists; files (next lesson on CSV and JSON parametrization) and databases are options as data grows.
- Design tables with case IDs, inputs and expected results, taken from the specification.
- Mix positive, negative and boundary rows, using equivalence partitioning to avoid redundant cases.
- Use `pytest.param` with `id` and `marks` (`xfail`, `skip`, custom) to make rows readable and controllable.
- Builders and generators keep rows short and every negative row one change away from a valid baseline.
- Good IDs and assertion messages show exactly which row failed, in the console and in CI reports.
- Avoid too many rows, hidden coupling between rows and shared mutable data.
- Related Wednesday topics: HTTP mocking, mocking external APIs, test isolation, request/response validation and building the reusable framework each have their own lesson. Accessibility testing is covered on Thursday; CI/CD on Friday.

## Additional Resources

- PyTest documentation, *How to parametrize fixtures and test functions*: https://docs.pytest.org/en/stable/how-to/parametrize.html
- PyTest documentation, *Skip and xfail*: https://docs.pytest.org/en/stable/how-to/skipping.html
- Requests documentation, *Quickstart* (params, JSON bodies, timeouts): https://requests.readthedocs.io/en/latest/user/quickstart/
- Python documentation, `itertools.product`: https://docs.python.org/3/library/itertools.html#itertools.product
- JSONPlaceholder (practice API) guide: https://jsonplaceholder.typicode.com/guide/
- Faker documentation (seeded fake data): https://faker.readthedocs.io/en/master/
