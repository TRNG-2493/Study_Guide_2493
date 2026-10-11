# Test Isolation

## Learning Objectives

By the end of this lesson you will be able to:

- Define **test isolation** and explain its three properties: independent, order-independent, and repeatable.
- Recognise the symptoms of coupled tests, such as "passes alone, fails in the suite".
- Name the common sources of shared state: module globals, class attributes, singletons, environment variables, files, server-side data, and sessions or tokens.
- Choose the right fixture scope and write `yield` fixtures and finalizers that clean up reliably.
- Generate unique test data (`uuid`, timestamps) so tests can share one API server safely.
- Use `pytest-randomly`, `pytest-xdist`, and `pytest-repeat` to expose hidden coupling and flakiness.
- Use `tmp_path`, `monkeypatch`, and mocks to isolate files, environment variables, and external services.
- Debug an order-dependent failure systematically and quarantine a flaky test without hiding it.

---

## Why This Matters

This is the Week 7 epic: you are building an API test suite that is **reusable, data-driven, and ready to run unattended in a pipeline**. Such a suite only works if you can trust it. When a test goes red, the team must be able to say "the product is broken". They must never have to say "maybe an earlier test left something behind".

Monday and Tuesday gave you reusable clients and fixtures. Earlier today you made tests data-driven (CSV and JSON) and learned to mock external services. Each of those techniques multiplies the number of tests you run, and the more tests you run, the more any hidden coupling between them hurts. Typical pain looks like this:

- A test passes on your laptop but fails on a teammate's machine.
- A test passes alone but fails in the full run (or the reverse).
- A red build turns green on re-run, so the team learns to ignore red builds.
- Someone tries to speed the suite up by running tests in parallel, and everything collides.

Isolation is the discipline that prevents all four. Friday's pipeline lesson covers running the suite in CI, including parallel jobs. Today you make sure the suite is ready for that by proving it can run in any order, in parallel, and repeatedly.

---

## The Concept

### 1. What Is Test Isolation?

A test is **isolated** when its result depends only on what the test itself sets up. It does not depend on which tests ran before it, which tests run alongside it, or what a previous run left behind.

Three properties define it:

| Property | Meaning | How you check it |
|----------|---------|------------------|
| **Independent** | The test creates (or mocks) everything it needs and does not rely on another test's output | Run it alone |
| **Order-independent** | Any ordering of the suite gives the same results | Random ordering |
| **Repeatable** | Running it twice, or a hundred times, gives the same result | Repeat it; run it twice in a row |

A fourth property follows naturally: **parallel-safe**. Tests that are independent and order-independent usually survive parallel execution, provided they also avoid colliding on shared external data (section 7).

**Analogy:** Each cooking competitor gets a clean station and their own ingredients. If they share one pan and leave scraps behind, the results become unfair and unpredictable. The golden rule for tests is: **arrange your own world, act in it, clean it up.**

### 2. Symptoms of Coupled Tests

Coupling shows up in recognisable ways. Learn the symptoms, because you will meet them in real suites.

| Symptom | Likely cause |
|---------|--------------|
| Passes alone, fails in the full suite | An earlier test changed shared state (a header, a global, a record) |
| Fails alone, passes in the full suite | The test relies on data or setup that another test provides |
| Fails after random reordering | Hidden order dependency |
| Fails on the second run, passes on a fresh environment | Leftover data (the record already exists) |
| Fails only when run in parallel | Two tests use the same record, file, or port |
| Fails "sometimes" with no code change | Time, randomness, or a race condition |

If you see one of these, suspect isolation before you suspect the product.

### 3. Sources of Shared State

Shared state is anything that lives **longer than one test** and that more than one test can touch. Here are the usual hiding places, each with a short example and a cure.

#### 3.1 Module-level globals

```python
created_id = None            # lives as long as the module is imported

def test_create_user(client):
    global created_id
    created_id = client.post("/users", json={"name": "Ana"}).json()["id"]

def test_get_user(client):
    assert client.get(f"/users/{created_id}").status_code == 200   # depends on the test above
```

*What this does:* the first test stores an ID in a global, and the second test reads it. *Why it is bad:* run `pytest -k test_get_user` and `created_id` is `None`. If the first test fails, the second fails too (a cascade). Under random order or parallel runs it breaks unpredictably. *Cure:* a fixture gives each test its own user (section 5).

#### 3.2 Class attributes

```python
class TestCart:
    items = []                         # ONE list shared by every test in the class

    def test_add_item(self):
        self.items.append("apple")
        assert len(self.items) == 1

    def test_add_two(self):
        self.items.append("pear")
        assert len(self.items) == 1    # fails if test_add_item ran first
```

A mutable class attribute is created once and shared. *Cure:* create state per test, in a fixture or in `setup_method`, never as a mutable class attribute.

#### 3.3 Singletons and cached objects

A "singleton" is an object that exists once for the whole process: a shared `ApiClient`, a config object, or a cached `requests.Session`. If a test modifies it (adds a header, changes a base URL), every later test inherits the change. The same applies to values cached with `functools.lru_cache`. *Cure:* build the object in a function-scoped fixture, or reset it in teardown.

#### 3.4 Environment variables

`os.environ` is process-wide. If a test sets `os.environ["API_BASE_URL"] = "https://staging..."` and fails before restoring it, every later test talks to staging. *Cure:* `monkeypatch.setenv` (section 10).

#### 3.5 Files and directories

Tests that write `output.json` or `cache.csv` in the current directory overwrite each other and leave debris. *Cure:* `tmp_path` (section 9).

#### 3.6 Data on a shared API server or database

This is the biggest source in API testing. Your tests send real requests to a server that holds data from every other test (and every other tester). Hard-coded emails collide, global counts change, and a previous run's leftovers break the next run. *Cure:* unique data per test and guaranteed cleanup (sections 5 and 7).

#### 3.7 Sessions and tokens

A shared `requests.Session` that stores cookies or an `Authorization` header leaks identity between tests:

```python
def test_admin_can_delete(client):
    client.session.headers["Authorization"] = admin_token       # mutates the SHARED client
    assert client.delete("/users/1").status_code == 204

def test_anonymous_is_rejected(client):
    assert client.delete("/users/1").status_code == 401         # still carries the admin header
```

*Cure:* one fixture per identity, each building a fresh client:

```python
@pytest.fixture
def anonymous_client(base_url):
    return ApiClient(base_url)

@pytest.fixture
def admin_client(base_url, admin_token):
    c = ApiClient(base_url)
    c.session.headers["Authorization"] = f"Bearer {admin_token}"
    return c
```

A token fetched once per session is fine **if it is read-only** (nobody changes or revokes it). A token that a test logs out, rotates, or expires is mutable shared state, so give that test its own.

### 4. Fixture Scope: Fresh State by Default

You met fixtures on Tuesday. The `scope` parameter decides **how long a fixture's value lives**:

| Scope | Created | Isolation risk | Use it for |
|-------|---------|----------------|------------|
| `function` (default) | Once per test | Lowest | Anything a test reads **or modifies**: records, clients, payloads |
| `class` | Once per class | Medium | Read-only data shared by a class |
| `module` | Once per file | Medium | Read-only data shared by a file |
| `session` | Once per run | Highest | Immutable, expensive things: config, a read-only token |

A small demonstration shows why a wider scope is dangerous with mutable values:

```python
import pytest

@pytest.fixture(scope="module")
def cart():
    return []                       # ONE list for the whole file

def test_a(cart):
    cart.append("apple")
    assert cart == ["apple"]

def test_b(cart):
    assert cart == []               # fails if test_a ran first

@pytest.fixture                     # function scope: a fresh list every time
def fresh_cart():
    return []

def test_c(fresh_cart):
    fresh_cart.append("apple")
    assert fresh_cart == ["apple"]

def test_d(fresh_cart):
    assert fresh_cart == []         # always passes
```

*Line by line:* `scope="module"` makes pytest call `cart()` once and hand the same list to every test in the file. `test_a` mutates it, so `test_b` sees the change. `fresh_cart` uses the default function scope, so pytest calls it again for each test and each test gets a brand-new list.

**When to widen scope:** only when setup is expensive (for example logging in) **and** the value is never modified. If in doubt, stay at function scope and optimise later.

**Common mistake:** a `session`-scoped fixture that returns a user record. One test edits the user's name, and every other test now sees a surprise.

### 5. Setup and Teardown That Always Clean Up

#### 5.1 `yield` fixtures

Code before `yield` is setup. Code after it is teardown, and pytest runs it **even when the test fails**.

```python
import pytest
from utils.data_factory import user_payload

@pytest.fixture
def user(client):
    r = client.post("/users", json=user_payload())          # 1. setup
    assert r.status_code == 201, f"Setup failed: {r.status_code} {r.text}"
    created = r.json()

    yield created                                           # 2. the test runs here

    resp = client.delete(f"/users/{created['id']}")         # 3. teardown
    assert resp.status_code in (200, 204, 404), f"Cleanup failed: {resp.status_code}"
```

*Line by line:*

1. The POST creates a user with unique data (section 7) and the assert fails loudly if setup did not work.
2. `yield created` hands the dictionary to the test. The test body runs now.
3. After the test, the DELETE removes the user. Accepting `404` means a test that already deleted the user (to verify deletion) will not break the cleanup.

**Rule:** if setup fails *before* the `yield`, teardown does not run, which is correct because there is nothing to clean up yet.

#### 5.2 Several items: track what you create

When one test creates several records, a plain `yield` fixture is awkward. Use a **factory fixture** that remembers everything it created:

```python
@pytest.fixture
def make_user(client):
    created = []

    def _make(**overrides):
        r = client.post("/users", json=user_payload(**overrides))
        assert r.status_code == 201
        user = r.json()
        created.append(user["id"])
        return user

    yield _make

    for user_id in reversed(created):                        # newest first
        client.delete(f"/users/{user_id}")
```

*Why `reversed`:* children are usually created after parents. Deleting in reverse order removes orders before the customers that own them and avoids foreign-key errors.

#### 5.3 Finalizers with `request.addfinalizer`

A finalizer is a function registered for cleanup. It is useful when cleanup steps are registered **as you go**, so a failure halfway through setup still cleans what already exists:

```python
@pytest.fixture
def order_with_customer(client, request):
    cust = client.post("/customers", json={"name": "Ana"}).json()
    request.addfinalizer(lambda: client.delete(f"/customers/{cust['id']}"))

    order = client.post("/orders", json={"customerId": cust["id"]}).json()
    request.addfinalizer(lambda: client.delete(f"/orders/{order['id']}"))

    return order
```

Finalizers run in **reverse registration order**: the order is deleted first, then the customer. If the order POST raises an exception, the customer finalizer is already registered and still runs. With a plain `yield` fixture that same failure would leave the customer behind, because the code after `yield` is never reached when setup raises before it.

**Choosing:** `yield` for the common case, a factory for many items, `addfinalizer` when setup has several stages that each need cleanup.

#### 5.4 Defensive cleanup of leftovers

A crashed run (a killed laptop, a cancelled pipeline) can leave records behind. A session fixture can purge records with your test prefix before the run starts:

```python
@pytest.fixture(scope="session", autouse=True)
def purge_stale_test_data(client):
    for u in client.get("/users", params={"email_prefix": "autotest-"}).json():
        client.delete(f"/users/{u['id']}")
    yield
```

Use this **only on a dedicated test environment**, and only with a prefix that real data can never have. Never run it against shared or production data. Remember that under xdist this runs once per worker (section 8.3), so make sure one worker's purge cannot delete another worker's live records. A safer variant is to purge only records older than a few hours.

### 6. Common Mistakes With Cleanup

| Mistake | Why it hurts | Fix |
|---------|--------------|-----|
| Cleanup at the end of the test body | Skipped when an assertion fails | Put it after `yield` or in a finalizer |
| Teardown asserts `204` only | Fails if the test already deleted the item | Accept `404` |
| Cleaning only the "main" record | Child records pile up | Track every id; delete in reverse |
| Cleanup that raises an error hiding the real failure | You see the teardown error, not the product bug | Keep teardown simple and tolerant |

### 7. Unique Test Data for Shared APIs

Never hard-code values that must be unique (emails, usernames, order numbers). Generate them.

```python
# utils/data_factory.py
import time
import uuid


def unique_suffix():
    return uuid.uuid4().hex[:8]


def unique_email(prefix="autotest"):
    return f"{prefix}.{unique_suffix()}@example.com"


def user_payload(**overrides):
    base = {"name": f"QA User {unique_suffix()}", "email": unique_email(), "age": 30}
    return {**base, **overrides}


def timestamped_name(label):
    return f"{label}-{int(time.time())}-{unique_suffix()}"
```

*Line by line:* `uuid.uuid4()` creates a random 128-bit identifier, and `.hex[:8]` keeps the first eight hexadecimal characters. That is short enough to read in logs and long enough (over four billion combinations) to avoid collisions in test runs. `user_payload` builds a valid body and lets a test override any field, for example `user_payload(age=-1)` for a negative test. `timestamped_name` adds the current Unix time so humans can see *when* a record was created, but it also adds a UUID piece because **a timestamp alone is not unique**: two parallel workers can hit the same second.

**Why a prefix:** values like `autotest.` or `qa.` let humans and cleanup scripts recognise test data on shared systems.

**Which to use:**

| Choice | Pros | Cons |
|--------|------|------|
| `uuid` | Collision-proof, safe in parallel | Not sortable by time |
| Timestamp only | Readable, sortable | Collides when two tests run in the same second |
| Timestamp + uuid | Readable and safe | Slightly longer |
| Counter (`1, 2, 3`) | Short | Breaks across parallel workers and across runs |

**Real-world scenario.** A QA team ran `POST /users` with the hard-coded email `test@example.com`. It passed in the morning. A second tester ran the same suite on the same server in the afternoon and got `409 Conflict` on every create test. The fix was one line: `unique_email()`. Nothing in the product had changed.

**Assert on your data, not on global counts:**

```python
# BAD: breaks whenever anyone else adds a user
assert len(client.get("/users").json()) == 10

# GOOD: only checks the record this test created
found = client.get("/users", params={"email": payload["email"]}).json()
assert len(found) == 1
```

### 8. Proving Isolation: The Tools

Reading code is not enough. Isolation is proven by **experiments**. All four tools below are plugins: install once with pip, and pytest picks them up.

```bash
pip install pytest-randomly pytest-xdist pytest-repeat
```

#### 8.1 Run a test alone

```bash
pytest tests/test_users.py::test_get_user -v
```

If it passes alone but fails in the suite (or the reverse), isolation is broken. This is the cheapest experiment, so always try it first.

#### 8.2 `pytest-randomly`: random order

Once installed, `pytest-randomly` is **active automatically**. It shuffles modules, then classes, then functions, and prints a seed in the header. It also reseeds `random.seed()` (and Faker or NumPy if installed) at the start of every test, so random data is reproducible too.

```bash
pytest                              # random order, new seed each run
pytest -p randomly --randomly-seed=12345   # replay an order exactly
pytest --randomly-seed=12345        # same thing (the plugin is already active)
pytest -p no:randomly               # disable the plugin entirely
pytest --randomly-dont-shuffle-modules      # keep module order, shuffle inside
```

Representative output (your seed will differ):

```
============================= test session starts =============================
Using --randomly-seed=1849302211
collected 6 items

tests/test_cart.py::test_b FAILED
tests/test_cart.py::test_a .
```

*What to do with this:* when a run fails, copy the seed from the header and re-run with `--randomly-seed=<that number>` to get the **same order** again. Reproducibility is what turns "it failed once" into a bug you can fix. Note the difference between the two forms: `-p randomly` explicitly loads the plugin (harmless when already active), and `-p no:randomly` unloads it so the original file order returns.

#### 8.3 `pytest-xdist`: parallel workers

```bash
pytest -n 4          # four worker processes
pytest -n auto       # one worker per CPU core
```

Parallel runs expose shared-data collisions immediately, because two tests now genuinely run at the same moment. Rules for a **worker-safe design**:

1. **Unique data everywhere.** Two workers creating `test@example.com` at once will conflict.
2. **No shared files.** Use `tmp_path` (each test gets its own directory).
3. **No assumptions about global counts.** Another worker is writing too.
4. **Do not rely on fixed ports or fixed file names.**

**Session fixtures run once per worker, not once overall.** Under `-n 4`, a `scope="session"` fixture executes four times, once in each worker process. That is fine for "read the config file" or "log in and get a token". It is a bug for "seed the database" or "purge all test data", because every worker repeats it, and a worker may delete data another worker just created. xdist provides a `worker_id` fixture (`"gw0"`, `"gw1"`, ... or `"master"` when not parallel), useful to give each worker its own namespace:

```python
@pytest.fixture(scope="session")
def run_prefix(worker_id):
    return f"autotest-{worker_id}-{uuid.uuid4().hex[:6]}"
```

*Reading it:* each worker builds one prefix for its whole session, for example `autotest-gw2-1f3a9c`. Records created by that worker carry its prefix, so cleanup can target only its own data.

A suite that passes serially and fails under `-n` is **telling you the truth**: the tests were never isolated. (How to run the suite in parallel inside a CI pipeline is covered in Friday's lesson.)

#### 8.4 `pytest-repeat`: catching flakiness

```bash
pytest tests/test_users.py::test_create_user --count=20
```

`--count=20` runs the selected test 20 times. A test that passes once but fails on repeat is not repeatable (for instance, because `ana@example.com` already exists after the first run). You can also mark a single test:

```python
@pytest.mark.repeat(50)
def test_create_user_is_unique(client):
    ...
```

Combine the tools for a thorough check:

```bash
pytest -n auto --count=5 -p randomly
```

If a suite survives five repetitions, in parallel, in random order, it is genuinely isolated.

### 9. Isolating Files and Environment: `tmp_path` and `monkeypatch`

#### 9.1 `tmp_path`

`tmp_path` is a built-in fixture that gives each test its own empty temporary directory (a `pathlib.Path`). Pytest deletes old ones later. Use it for any file a test writes.

```python
import json

def test_report_is_written(tmp_path):
    out = tmp_path / "report.json"                 # a unique path for THIS test
    out.write_text(json.dumps({"passed": 3}))
    assert json.loads(out.read_text())["passed"] == 3
```

Two tests that both write `report.json` no longer collide, even in parallel, because each has a different `tmp_path`. This is also the right place for downloaded files in API tests.

#### 9.2 `monkeypatch`

`monkeypatch` changes something for the duration of **one test** and restores it afterwards, even if the test fails.

```python
def test_uses_staging_url(monkeypatch):
    monkeypatch.setenv("API_BASE_URL", "https://staging.example.com")
    monkeypatch.delenv("API_TOKEN", raising=False)       # remove it, don't fail if absent
    ...                                                  # after the test both are restored

def test_default_url():
    import os
    assert os.environ.get("API_BASE_URL") != "https://staging.example.com"
```

Useful methods: `setenv`, `delenv`, `setattr` (replace a function or attribute), `setitem` (change a dict entry), and `chdir`.

```python
import config

def test_timeout_is_short(monkeypatch):
    monkeypatch.setattr(config, "TIMEOUT", 0.5)          # restored automatically
```

**Common mistake:** writing `os.environ["API_BASE_URL"] = "..."` directly. If the test fails midway, the value stays set for every later test, which is a coupling bug that is hard to see.

### 10. Isolating With Mocks

Using the mocking approach from earlier today, remove invisible dependencies on services you do not control: a payment sandbox, an email provider, a third-party API with rate limits. Two rules keep the mocks themselves isolated:

- Use **function-scoped** mock fixtures so each test registers its own responses.
- Keep mock registration **inside the test or fixture**, never in module-level code that mutates global state.

```python
import responses
import requests

@pytest.fixture
def mocked_rates():
    with responses.RequestsMock() as rsps:               # new mock per test, removed afterwards
        rsps.add(responses.GET, "https://rates.example.com/usd",
                 json={"EUR": 0.9}, status=200)
        yield rsps

def test_convert_uses_rate(mocked_rates):
    r = requests.get("https://rates.example.com/usd")
    assert r.json()["EUR"] == 0.9
```

*Reading it:* the `with` block activates the mock when the fixture starts, and leaving the block (after `yield`) deactivates it. A mock that is patched globally and never removed would leak into later tests and cause confusing "why is this real call being faked?" failures.

**Time and randomness** are also shared state. Do not assert exact timestamps. Assert ranges ("created within the last minute") or compare against times you measured around the call. For code that depends on "now", inject the clock or use a library such as `freezegun`. `pytest-randomly` already seeds `random` per test; if you use Faker, call `Faker.seed(1234)`.

### 11. Debugging Order-Dependent Failures

Follow this procedure every time, in order:

1. **Capture the seed.** Copy `Using --randomly-seed=...` from the failing run's header.
2. **Reproduce.** Run `pytest --randomly-seed=<seed>`. If it fails the same way, you have a stable reproduction.
3. **Run the failing test alone.** `pytest path::test_name`. If it passes alone, it depends on something an earlier test left behind.
4. **Take randomness out.** Run `pytest -p no:randomly path::test_fails` with the original order to confirm the result is order-related.
5. **Bisect.** Run the failing test with the first half of the tests that ran before it. If it still fails, the culprit is in that half; if not, in the other half. Repeat until one polluter remains.

```bash
pytest -p no:randomly tests/test_a.py tests/test_b.py::test_fails     # a pair
pytest -p no:randomly tests/test_a.py::test_x tests/test_b.py::test_fails   # a single suspect
```

6. **Find the shared state.** Search the polluter for globals, class attributes, singleton changes, header mutations, `os.environ`, files, and records it creates without cleaning.
7. **Fix the cause.** Give the test its own data or a function-scoped fixture, or add the missing cleanup.
8. **Prove it.** Re-run with several seeds, in parallel, and with `--count`.

**Do not fix flakiness with `time.sleep()`** or with automatic reruns (`pytest-rerunfailures`) except as a short, documented stopgap. Both hide the real defect and make the suite slower.

**Real-world scenario.** A suite failed in CI with `test_anonymous_is_rejected` returning `200`. It passed locally. The CI log showed `--randomly-seed=77841`. Running the same seed locally reproduced the failure. Bisecting found that `test_admin_can_delete` set an `Authorization` header on a shared client. The fix was two function-scoped client fixtures (section 3.7). Total time: 20 minutes, because the seed made the failure reproducible. Without it, the team would have re-run the pipeline and hoped.

### 12. Flaky Tests: Taxonomy and Quarantine

A **flaky test** passes and fails on the same code. Isolation problems cause many of them, but not all. Knowing the category tells you the fix.

| Category | Cause | Typical fix |
|----------|-------|-------------|
| **Order dependence** | Test relies on another test's state | Own data; random order to detect |
| **Shared state / data collision** | Hard-coded values, shared records, parallel overlap | Unique data, per-test fixtures |
| **Leftover data** | Previous run did not clean up | Guaranteed teardown, purge on dedicated envs |
| **Time and date** | Midnight, time zones, month ends, expiry | Control or inject the clock; assert ranges |
| **Async and timing** | Asserting before the server finished (eventual consistency) | Poll with a timeout; never a blind `sleep` |
| **External dependency** | Third-party outage or rate limit | Mock it, or isolate in a separate suite |
| **Resource limits** | Port in use, rate limit hit, low disk | Unique ports, `tmp_path`, throttling |
| **Environment drift** | Different config or versions between machines | Pin versions; use `monkeypatch` for config |

#### Quarantining a flaky test

Sometimes a flaky test cannot be fixed immediately, and leaving it in the main suite trains people to ignore red. **Quarantine** it: move it out of the blocking run, but keep it visible and owned.

Register a marker in `pytest.ini`:

```ini
[pytest]
markers =
    quarantine: known flaky test, excluded from the blocking run (must link a ticket)
```

Mark the test, and always record the reason:

```python
@pytest.mark.quarantine(reason="QA-412: intermittent 409 on parallel create")
def test_create_order_parallel(client):
    ...
```

Run the blocking suite without it, and run the quarantined tests separately:

```bash
pytest -m "not quarantine"       # the gate: must be green
pytest -m quarantine             # the watch list: run separately, investigate
```

Quarantine rules:

- Every quarantined test has a **ticket** and an **owner**.
- It has an **expiry**: fix it or delete it within an agreed time (for example two sprints).
- Quarantine is **not deletion**. The test still runs somewhere, so you see whether it recovers.

### 13. A Before-and-After Example

**Before** (non-isolated):

```python
def test_create_order(client):
    r = client.post("/orders", json={"customerId": 1, "items": [{"sku": "A1", "qty": 2}]})
    assert r.status_code == 201

def test_orders_count(client):
    assert len(client.get("/orders").json()) == 1       # assumes the previous test ran, and nothing else exists
```

**After** (isolated):

```python
@pytest.fixture
def customer(make_user_customer):
    return make_user_customer()                         # a brand-new customer per test

@pytest.fixture
def order(client, customer):
    r = client.post("/orders", json={"customerId": customer["id"],
                                     "items": [{"sku": "A1", "qty": 2}]})
    assert r.status_code == 201
    created = r.json()
    yield created
    client.delete(f"/orders/{created['id']}")

def test_order_appears_in_customers_orders(client, customer, order):
    orders = client.get(f"/customers/{customer['id']}/orders").json()
    assert [o["id"] for o in orders] == [order["id"]]       # exactly our order for our customer
```

The customer is brand new, so its order list can only contain what this test created. The assertion is safe in any order and any number of workers.

### 14. Checklist for Every New API Test

- [ ] Does it create (or mock) all the data it needs?
- [ ] Are unique fields generated, not hard-coded?
- [ ] Does it clean up, even on failure?
- [ ] Does it avoid assertions on global totals or other people's data?
- [ ] Does it avoid modifying shared objects, headers, or environment variables?
- [ ] Do fixtures that return mutable data use function scope?
- [ ] Does it pass when run alone, in random order, in parallel, and twice in a row?
- [ ] Are third-party services mocked?

### 15. Glossary

### Isolation
A test's result depends only on its own setup.

### Order dependence
A test that passes or fails depending on which tests ran before it.

### Shared state
Anything that outlives one test and can be touched by several (globals, files, server data, tokens).

### Fixture scope
How long a fixture's value lives: function, class, module, or session.

### Teardown / finalizer
Cleanup code that pytest runs after a test, even when it fails.

### Flaky test
A test that gives different results on the same code.

### Seed
A number that fixes the "random" order and values so a run can be replayed.

### Worker
One of the parallel processes started by `pytest-xdist`.

### Quarantine
A temporary, tracked exclusion of a flaky test from the blocking run.

---

### 16. Practice Exercises

#### Exercise 1: Fix the chain

The three chained tests from section 3.1 (`created_id` global) fail when run alone. Refactor them with a `user` fixture and prove they pass alone.

**Solution:**

```python
@pytest.fixture
def user(client):
    r = client.post("/users", json=user_payload())
    assert r.status_code == 201
    created = r.json()
    yield created
    client.delete(f"/users/{created['id']}")          # tolerant: ignore the status

def test_create_user(client):
    r = client.post("/users", json=user_payload())
    assert r.status_code == 201
    client.delete(f"/users/{r.json()['id']}")

def test_get_user(client, user):
    assert client.get(f"/users/{user['id']}").status_code == 200

def test_delete_user(client, user):
    assert client.delete(f"/users/{user['id']}").status_code == 204
```

Prove it with `pytest -k test_get_user`, then `pytest -k test_delete_user`, then `pytest -p randomly` a few times. `test_delete_user` deletes the user that teardown deletes again; the teardown ignores the `404`, so nothing breaks. All three pass in any order.

#### Exercise 2: Repeatable creation

Write `unique_email()` and run a create-user test 20 times. Show that nothing collides.

**Solution:**

```python
# utils/data_factory.py
import uuid

def unique_email(prefix="autotest"):
    return f"{prefix}.{uuid.uuid4().hex[:8]}@example.com"

# tests/test_users.py
def test_create_user(make_user):
    user = make_user()
    assert "@example.com" in user["email"]
```

Run `pytest tests/test_users.py::test_create_user --count=20`. All 20 pass because each run builds a different email. To see the failure you are preventing, temporarily replace `unique_email()` with the fixed string `"ana@example.com"`: run 1 passes, run 2 returns `409`. That second-run failure is exactly what "not repeatable" means.

#### Exercise 3: Break and fix on purpose

Create a deliberate isolation bug with a mutable class attribute, make it fail under random order, then fix it.

**Solution:**

```python
# tests/test_cart_bug.py
class TestCart:
    items = []                                 # the bug: shared mutable class attribute

    def test_add_apple(self):
        self.items.append("apple")
        assert self.items == ["apple"]

    def test_add_pear(self):
        self.items.append("pear")
        assert self.items == ["pear"]
```

Run `pytest -p no:randomly` and it fails on the second test (the list holds both). Run `pytest -p randomly --randomly-seed=1` and `--randomly-seed=2` to see the order change which test fails. Because both orders fail on whichever test runs second, copy the seed from a failing run and replay it to confirm. **Fix:**

```python
import pytest

@pytest.fixture
def items():
    return []                                  # fresh list for each test

class TestCart:
    def test_add_apple(self, items):
        items.append("apple")
        assert items == ["apple"]

    def test_add_pear(self, items):
        items.append("pear")
        assert items == ["pear"]
```

Re-run with several seeds and `-n 2`: all pass.

#### Exercise 4: Environment and file isolation

Write a test that sets an environment variable and writes a file, without leaking either.

**Solution:**

```python
import os

def test_env_and_file_are_restored(monkeypatch, tmp_path):
    monkeypatch.setenv("REPORT_DIR", str(tmp_path))
    target = tmp_path / "out.txt"
    target.write_text("hello")
    assert os.environ["REPORT_DIR"] == str(tmp_path)
    assert target.read_text() == "hello"

def test_env_is_gone_afterwards():
    assert "REPORT_DIR" not in os.environ          # passes in any order
```

`monkeypatch` removes `REPORT_DIR` when the first test ends, and `tmp_path` gives the file a private directory. Under random order and `-n 2` the second test always passes. If you replaced `monkeypatch.setenv` with `os.environ["REPORT_DIR"] = ...`, the second test would fail whenever it ran after the first.

---

### 17. Quiz

**Question 1.** A test passes with `pytest tests/test_a.py::test_x` but fails in the full run. What is the most likely cause?

- A) The product has a bug
- B) An earlier test changed shared state
- C) pytest is out of date
- D) The test has too few assertions

**Question 2.** Under `pytest -n 4`, how many times does a `scope="session"` fixture run?

- A) Once overall
- B) Once per test
- C) Once per worker (four times)
- D) Never

**Question 3.** Which command replays the exact order from a previous random run?

- A) `pytest -p no:randomly`
- B) `pytest --randomly-seed=12345`
- C) `pytest --count=12345`
- D) `pytest -n 12345`

**Question 4.** Why is a timestamp alone a weak unique-data strategy for parallel runs?

- A) Timestamps are too long
- B) Two workers can generate the same timestamp in the same second
- C) APIs reject numbers
- D) Timestamps cannot be read in logs

**Question 5.** What is the right way to handle a flaky test you cannot fix this sprint?

- A) Delete it
- B) Add `time.sleep(5)`
- C) Quarantine it with a ticket, an owner, and an expiry, and run it separately
- D) Rerun it until it goes green

**Answers**

1. **B.** Passing alone and failing in the suite points to state left by an earlier test. If the product were broken it would fail in both cases.
2. **C.** Each xdist worker is a separate process with its own session, so session fixtures run once per worker. Design them to be safe to run several times.
3. **B.** `--randomly-seed=<number>` reproduces the shuffle. (`-p no:randomly` disables random ordering instead.)
4. **B.** Timestamps have limited resolution. Combine them with a `uuid` piece (or use only a `uuid`) so parallel workers cannot collide.
5. **C.** Quarantine keeps the test visible and owned without blocking the pipeline. Deleting hides the problem, and sleeps and reruns mask it.

---

## Summary

- An isolated test is independent, order-independent, and repeatable; it depends only on its own setup.
- Coupling shows as "passes alone, fails in the suite", failures after reordering, or failures only on the second run or in parallel.
- Shared state hides in module globals, class attributes, singletons, environment variables, files, server-side data, and sessions or tokens.
- Use function-scoped fixtures by default; widen scope only for read-only, expensive resources.
- Clean up with `yield` fixtures, factory fixtures, and finalizers. Make teardown tolerant of `404`.
- Generate unique data with `uuid` (add a timestamp for readability) and assert on your own records, not global counts.
- Prove isolation with `pytest-randomly` (replay with `--randomly-seed`), `pytest-xdist` (`-n auto`; session fixtures run per worker), and `pytest-repeat` (`--count`).
- Use `tmp_path` for files, `monkeypatch` for environment and attributes, and function-scoped mocks for external services.
- Debug by capturing the seed, reproducing, running alone, and bisecting; never fix flakiness with sleeps.
- Classify flaky tests by cause and quarantine with a marker, a ticket, an owner, and an expiry.

## Additional Resources

- pytest documentation, *Fixtures: teardown and cleanup (finalization)*: https://docs.pytest.org/en/stable/how-to/fixtures.html#teardown-cleanup-aka-fixture-finalization
- pytest documentation, *How to monkeypatch / mock modules and environments*: https://docs.pytest.org/en/stable/how-to/monkeypatch.html
- pytest documentation, *How to use temporary directories and files (`tmp_path`)*: https://docs.pytest.org/en/stable/how-to/tmp_path.html
- pytest-xdist documentation: https://pytest-xdist.readthedocs.io/en/stable/
- pytest-randomly on GitHub: https://github.com/pytest-dev/pytest-randomly
- Martin Fowler, *Eradicating Non-Determinism in Tests*: https://martinfowler.com/articles/nonDeterminism.html
