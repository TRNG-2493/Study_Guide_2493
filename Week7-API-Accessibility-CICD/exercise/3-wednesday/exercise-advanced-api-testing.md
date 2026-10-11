# Wednesday Exercise: Advanced API Testing (Reusable and Isolated)

**Week 7, Day 3 | Time box: 2 to 3 hours | Individual | Project 2 milestone included**

## Objectives
By the end you can:
- Reproduce and explain order-dependence and shared-state failures with `pytest-randomly` and `pytest-xdist`.
- Refactor a flat API suite into layers: config, `ApiClient`, service classes, models, data, fixtures.
- Drive tests from CSV and JSON files with `parametrize` and readable ids.
- Validate responses with `jsonschema` and Pydantic.
- Isolate tests with unique data and cleanup fixtures.
- Test code that calls an external API using `responses` (success, 500, timeout, 429 retry), with a mock/live switch.

## Scenario
On Tuesday your API suite passed. Your team lead ran it again this morning and sent you this message: *"It fails when I run it in random order, it fails when two people run it at once, and when the staging API was down we got a wall of red with no explanation. Also, the pricing team wants tests for the `PriceService` that calls the external tax/currency API, and we cannot call that API from CI."*

The suite you inherit (`starter_code/tests/api/`) is a "works-but-messy" baseline. Your job is to make it reusable, isolated and mock-capable without losing coverage. This is the base of your Project 2 framework.

## Setup (10 minutes)
```bash
cd starter_code
pip install -r requirements.txt          # add --break-system-packages only on a locked-down system Python
python project2_api_server.py 8000       # terminal 1; restart it whenever you want a clean slate
python -m pytest -p no:randomly          # terminal 2: baseline passes (23 passed, 2 skipped)
```
The server keeps its data in memory. Restart it between experiments. If `pytest` and `pip` use different Pythons on your machine, always run `python -m pytest`.

Read `1-monday/starter_code/api-contract.md` for the API contract and `app/price_service.py` (docstring at the top) for the behaviour of the external API client. **Do not edit `app/price_service.py`**; it is the code under test.

## Rules
- Work in `starter_code/` (or copy it into your own repo). Keep the baseline files until Stage 7, then delete them.
- Only the libraries in `requirements.txt` are needed. No real network calls to anything except the local stand-in API.
- Commit after every stage. Small commits are how you will find the regression you introduce.

## Core tasks

### Stage 1: Observe the brittleness (20 minutes)
1. Run `python -m pytest -p no:randomly` and note the result.
2. Restart the server. Run `python -m pytest -p randomly --randomly-seed=1`. Repeat with seeds 2 and 3, restarting the server each time.
3. Restart the server and run `python -m pytest -n 2`.
4. Stop the server and run the suite once more.
5. Write `FINDINGS.md` (max 15 lines): for each failure pattern, which test failed, why, and which of these categories it belongs to: *order dependence, shared state, hard-coded data, no config, no timeout, duplication*. Find at least **five** distinct problems in the code by reading it.

Checkpoint: you can explain why `test_02_get_created_item` fails under some seeds and why `test_list_has_five_items` fails even when it is "correct".

### Stage 2: Layers, config and environment (30 minutes)
Create this structure (names are suggestions; keep the idea):
```
config/        settings read from environment variables, with local defaults
clients/       ApiClient wrapping requests.Session
services/      ItemsApi (and optionally AuthApi): one method per endpoint
```
Requirements:
- `ApiClient` takes a base URL and timeout, sends a default timeout on every call, can log in and then add the `Authorization` header automatically, and exposes `get/post/put/patch/delete`.
- `ItemsApi` receives a client and knows the paths. After this stage **no test contains `http://` or `/items` as a string**.
- Settings (base URL, credentials, timeout) come from environment variables. `BASE_URL=http://127.0.0.1:8123 pytest` must work.
- Fixtures in `conftest.py` provide `settings`, a logged-in `user_client`, a logged-in `admin_client`, and `items_api`. Log in **once per session**, not once per test.

Checkpoint: `pytest -p no:randomly` still passes, and you deleted at least 80 percent of the duplicated URL and login lines.

### Stage 3: Data-driven tests (25 minutes)
- Create `data/items.csv` (the five seed items) and `data/payloads.json` (valid and invalid create bodies with an `id` and the expected bad field).
- Write a small loader in `utils/` using `pathlib` (do not rely on the current working directory).
- Replace the repeated `test_get_item_1/2/3`, `test_filter_*` and `test_create_*_422` tests with parametrized tests. Every parameter set needs a readable id (`ids=` or `pytest.param(..., id=...)`).
- Add a test that checks the data files themselves (no missing columns, no duplicate ids).

Checkpoint: `pytest --collect-only -q` shows meaningful ids, not `case0`, `case1`.

### Stage 4: Models and schema checks (20 minutes)
- Add a Pydantic `Item` request model and an `ItemOut` response model (with `id`). Constrain price, category and stock exactly as the contract says.
- Let `ItemsApi` return parsed models where it helps (for example a `create_ok` helper), and keep raw responses available for negative tests.
- Reuse the JSON schema from Tuesday (`2-tuesday/solution/schemas.py`) for the list and single-item responses, so both validators run.
- Add a negative test for each validator: feed it bad data and assert that it raises. A validator that never fails proves nothing.

### Stage 5: Isolation (30 minutes)
Make the suite pass in any order and in parallel:
- Every test that creates data uses a unique name (`uuid`) and never a hard-coded one.
- Creation goes through a **factory fixture** that records what it created and deletes it in teardown, even when the test fails.
- No module-level mutable state, no numbered test names that rely on file order. A test that needs an item gets it from a fixture.
- Replace exact assertions on shared collections (`total == 5`, `total == 2`) with assertions that cannot be broken by someone else's data (a lower bound, or a filter on your own unique name).
- Never call `/admin/reset` from a test; it destroys everyone's data.
- If the API is unreachable, API tests must be **skipped with one clear reason** (a fixture or hook), and an environment variable of your choice (for example `REQUIRE_API=1`) turns that skip into a failure for CI.

Checkpoint: three different random seeds pass, and `-n 2` passes, without restarting the server in between.

### Stage 6: Mock tests for `PriceService` (35 minutes)
Write `tests/unit/test_price_service.py` using the `responses` library. No real HTTP, no real sleeping (the class accepts a `sleep` function; inject a fake that records its argument). Cover at least:
1. `get_tax_rate` success (and that the country code is upper-cased in the request).
2. `price_with_tax` with three parametrized price/rate combinations, including rounding.
3. `convert` success, and a response that has no rate for the target currency.
4. HTTP 500: raises `PriceServiceError`, and the service made **exactly one** request.
5. A timeout: raises `PriceServiceTimeout`.
6. HTTP 429 followed by 200: succeeds, made two requests, and slept for the `Retry-After` value.
7. HTTP 429 every time: raises `RateLimitError` after the configured retries (assert the request count).
8. A negative price raises `ValueError` and makes no HTTP call.

Checkpoint: the whole file runs in well under a second with the network disabled.

### Stage 7: Mock/live switch and final runs (20 minutes)
- Add markers `live` (needs the stand-in API) and `mock` (fully offline), registered in `pytest.ini` (the config uses `--strict-markers`).
- Add an environment switch (for example `API_MODE=mock`) so that `live` tests are skipped and the mock tests still run.
- Final proof, all in your README as copy-paste commands with the pass counts:
  1. `pytest` (random order is automatic with pytest-randomly) against a running server, with three different seeds.
  2. `pytest -n 2`.
  3. `API_MODE=mock pytest` with the server stopped.
  4. `pytest` with the server stopped: a clean skip message, not a wall of errors.
- Delete the messy baseline files. Run the suite once more.

## Stretch goals
- Mock tests for your `ApiClient` (default timeout applied, bearer header sent, a timeout propagates).
- Use `unittest.mock.patch` or `monkeypatch` to replace the sleep function or a service method in one test, and explain when you would choose it over `responses`.
- Add a `-m smoke` run that finishes in under 2 seconds.
- A `pytest.fixture(params=[...])` that runs the same CRUD test as user and as admin where the contract allows it.
- A coverage report for `app/` showing every branch of `PriceService` is exercised.

## Deliverables
1. `FINDINGS.md` from Stage 1.
2. The refactored framework (layers, `data/`, fixtures) with no baseline files left.
3. `tests/unit/test_price_service.py` and the mock/live switch.
4. `README.md` with setup, run commands (live, mock, random, parallel) and the folder map.
5. Terminal output (pasted into README or a screenshot) for the four runs in Stage 7.
6. Git history with at least one commit per stage.

## Definition of Done
- [ ] FINDINGS.md lists at least five concrete problems with test names.
- [ ] No test contains a URL, a login call, or a hard-coded credential.
- [ ] Configuration comes from environment variables with local defaults.
- [ ] `ApiClient` (Session, timeout, token) and `ItemsApi` exist and are used by every API test.
- [ ] Test data lives in `data/items.csv` and `data/payloads.json`; every parameter set has an id.
- [ ] Pydantic models and JSON schema both validate responses, each with a negative test.
- [ ] All created data is unique and cleaned up; no globals; no ordering assumptions.
- [ ] Passes with three random seeds and with `-n 2`, without restarting the server.
- [ ] `PriceService` mock tests cover success, 500, timeout, 429-then-200, 429-forever and a no-network guard.
- [ ] `API_MODE=mock` runs offline; API down gives a clear skip.
- [ ] No `__pycache__`, `.pytest_cache` or secrets committed.

## Grading rubric (100 points)
| Area | Excellent (full marks) | Partial | Missing | Points |
|---|---|---|---|---|
| Diagnosis (FINDINGS.md) | 5+ problems, each tied to a test and a cause | 3-4 problems or vague causes | Under 3 | 10 |
| Layering and config | Client, service, config in place; tests free of URLs/logins | Layers exist but leak URLs or credentials | Flat suite | 20 |
| Data-driven tests | CSV and JSON, loader, readable ids, duplicates removed | One format only or poor ids | Inline lists | 15 |
| Models and schemas | Pydantic and jsonschema, with negative tests | Only one, or no negative tests | None | 10 |
| Isolation | Random seeds and `-n 2` pass; unique data; teardown | Passes in order only, or leaks data | Fails randomly | 20 |
| Mock tests | All scenarios, instant, call counts asserted | Happy path plus one error | None | 15 |
| Switch, README, hygiene | Mock/live works, clean skip, README proofs | One of these missing | None | 10 |

## Hints (no solutions)
- Run with `-p randomly --randomly-seed=N` to reproduce a failure; the seed is printed in the pytest header.
- A function-scoped fixture that `yield`s gives you setup and teardown in one place; teardown runs even when the test fails.
- Session-scoped fixtures are created before function-scoped ones, even autouse ones. Where you check "is the API up" matters.
- `responses` serves several responses registered for the same URL in order; use that for "429 then 200". To simulate a timeout, give the registered response a `body=` that is an exception instance.
- `responses.calls` holds every request made: use it for call counts and for the `Retry-After` assertion.
- With `-n 2` there is still **one** server. Anything that depends on the exact contents of a shared collection is unsafe.
- `pytest.param(value, id="name")` is the clean way to attach ids to data loaded from files.
- Use `pathlib.Path(__file__)` to locate `data/`, not a relative path.
- Pydantic `Literal[...]` is a convenient way to model an enum such as category.
- If you catch yourself writing `time.sleep` in a test, stop: inject or mock it.

## Project 2 milestone
**Goal: your Project 2 repository has a reusable, isolated API test framework.** Apply this exercise to your own team API (or the stand-in if your API is not ready) in your Project 2 repo:
- A layered tree: `config/`, `clients/`, `services/`, `models/`, `data/`, `utils/`, `tests/api/`, `tests/unit/`, plus `conftest.py` and `pytest.ini` with registered markers.
- At least two service classes for your real resources, with all paths in one place.
- A `data/` folder with at least one CSV and one JSON file driving parametrized tests.
- Mock tests (`responses`) for at least one external dependency or for your `ApiClient`.
- Passing runs in random order and with `-n 2`, with the mock/live switch documented.
- `README.md` with setup, run commands and the folder map, written so a teammate can run it in five minutes.

Tell your trainer which parts of today's refactor you adapted, and which you could not. Thursday and Friday build on this repo, so a clean tree now saves you time later.
