# Exercise: Python API Automation with requests and PyTest

**Week 7, Tuesday** | Time box: 2-3 hours | Individual work | Tools: Python 3.9+, `requests`, `pytest`, `jsonschema`

## Objectives
By the end you can:
1. Lay out a PyTest API project (`conftest.py`, `pytest.ini`, `tests/api/`).
2. Build `base_url`, `session` and authentication fixtures, with setup and cleanup using `yield`.
3. Automate CRUD calls with `requests` and assert on status codes, headers and JSON bodies.
4. Test negative paths and tell **401** (not authenticated) from **403** (not allowed), plus 404, 409 and 422.
5. Validate response structure with a JSON schema (`jsonschema`).
6. Use `@pytest.mark.parametrize` with literal lists and readable `ids`.
7. Test pagination and filter query parameters, tag tests `smoke` / `regression`, and leave no test data behind.

## Setup
1. Copy `starter_code/` to your working directory and open a terminal there.
2. Create and activate a virtual environment, then install:
   ```
   python -m venv .venv
   source .venv/bin/activate        # Windows: .venv\Scripts\activate
   pip install -r requirements.txt
   ```
3. Start the stand-in API in a second terminal: `python project2_api_server.py` (listens on `http://127.0.0.1:8000`). Restart it, or call `POST /admin/reset` as admin, to restore seed data.
4. Confirm the starter is healthy: `pytest` should report every test as **skipped (TODO)** with no errors.
5. Keep `api-contract.md` from Monday open. It is your specification.

## Scenario
On Monday you explored the stationery inventory API by hand in Postman. The team now wants the same checks to run automatically on every build. You will turn that exploration into a PyTest suite that is fast, independent of test order, and clean after itself. This server stands in for your Project 2 API; the milestone at the end moves the suite to your own repository.

## Core tasks

### Stage 1: Project skeleton (about 10 min)
1. Inspect the starter layout (see `starter_code/README.md`). Read `pytest.ini`: note `--strict-markers` and the two markers.
2. Run `pytest --collect-only -q` and `pytest -rs`. Explain to yourself why the tests are skipped rather than failing.

### Stage 2: Fixtures in `conftest.py` (about 25 min)
1. `base_url` (session scope): read `BASE_URL` from the environment, default `http://127.0.0.1:8000`.
2. `session` (session scope): a `requests.Session`; close it after the run using `yield`.
3. `user_token` and `admin_token` (session scope): log in through `POST /auth/login`. Read usernames and passwords from environment variables (with stand-in defaults). Assert the login succeeded so a failure is obvious.
4. `auth_headers` and `admin_headers`: a `Bearer` header dictionary.
5. `item_payload`: a valid body with a unique name on every call.
6. `created_item`: create an item, `yield` it, delete it afterwards as admin. It must not fail when the test already deleted the item.
7. Check with `pytest --setup-show` that setup and teardown run in the order you expect.

### Stage 3: CRUD tests, `tests/api/test_items_crud.py` (about 25 min)
Implement the skeletons for health, create, get by id, PUT, PATCH, and delete-then-get. For create, check the status, the `Location` header, every field you sent, and that a follow-up `GET` returns the same item. Rely on fixtures for setup; do not repeat login code in tests.

### Stage 4: Status codes and negative tests (about 30 min)
Implement `test_auth.py` and `test_status_codes.py`:
- 401: write without a token, with a garbage token, and a failed login.
- 403: a normal user calls `DELETE /items/{id}` or `POST /admin/reset`. Assert the item still exists afterwards.
- 404: missing item for GET, PUT, PATCH, DELETE (as admin), and an unknown route.
- 409: duplicate name on create (try a different letter case).
- 422: invalid bodies. Also check that the `details` object names the offending field.
- 400: malformed JSON.
Write a one-line comment above each 401/403 test saying which one it is and why.

### Stage 5: JSON schema validation, `test_schemas.py` (about 20 min)
1. In `schemas.py`, write `ITEM_SCHEMA` (required fields, types, allowed categories, no extra properties) and `ITEM_LIST_SCHEMA` (`total`, `page`, `limit`, `items` array of items).
2. Validate `GET /items` and `GET /items/{id}` with `jsonschema.validate`.
3. Prove the schema can fail: add one test that feeds it deliberately wrong data and expects `ValidationError`.

### Stage 6: Parametrization (about 20 min)
Turn repeated tests into data-driven ones with **literal lists** inside the test file. Required: bad credentials (4 cases), invalid create bodies (at least 6), seed item ids for the schema test. Give every case an `ids=` label so failures read like `test_invalid_create_is_422[negative-price]`.

### Stage 7: Pagination and filters, `test_query_params.py` (about 20 min)
Test default paging, `page`/`limit` combinations (including a partial last page and a page beyond the end), invalid paging (400), `category` filter, case-insensitive `q` search, and combined filters. Assert `total` as well as the length of `items`.

### Stage 8: Markers (about 10 min)
Mark roughly 5 to 8 fast, high-value tests `smoke` (health, login, list, create) and the rest `regression`. Run `pytest -m smoke`, `pytest -m regression`, and `pytest -m "not smoke"` and compare the counts.

### Stage 9: Cleanup and independence (about 15 min)
1. Run the suite three times in a row, then `pytest --tb=short -x` with the files named in reverse order (`pytest tests/api/test_schemas.py tests/api/test_query_params.py tests/api/test_items_crud.py`). It must pass every time.
2. Call `GET /items` after a run: `total` must be back to 5. If not, find the test that leaks data.
3. Optional: add the `make_item` factory fixture for tests that need several items.

## Stretch goals
- Add a response-time assertion (for example under 1 second) to the smoke tests.
- Check that `X-Request-Id` is present and different on two calls.
- Add `--tb=short` and `-ra` defaults to `addopts` and explain what each does.
- Write a test documenting a quirk you found (see Monday's notes) and mark it clearly in a comment.
- Verify that a token created by one test class still works in another (token reuse) and discuss the trade-off versus logging in per test.

## Deliverables
- Your working directory (or repository) with `conftest.py`, `pytest.ini`, `schemas.py`, `tests/api/*.py`, `requirements.txt`.
- A terminal screenshot or pasted output of `pytest -v` showing all tests passing, and of `pytest -m smoke`.
- A short `NOTES.md` (5-10 lines): one flaky or surprising behaviour you hit, and one thing you would automate next.

## Definition of Done
- [ ] `pip install -r requirements.txt` then `pytest` passes on a fresh virtual environment with the server running.
- [ ] No credentials or URLs are hard-coded inside test functions (fixtures and env vars only).
- [ ] No TODO or `pytest.skip('TODO')` left.
- [ ] Every status code in Stage 4 is covered, with 401 and 403 correctly distinguished.
- [ ] Both schemas are validated, and one test proves the schema can fail.
- [ ] At least 3 parametrized tests with `ids`.
- [ ] `smoke` and `regression` markers work under `--strict-markers`.
- [ ] The suite passes three runs in a row; `GET /items` shows `total` 5 afterwards.
- [ ] Tests are independent: any single test passes when run alone (`pytest path::test_name`).

## Grading rubric (100 points)
| Criterion | Points | Full marks when |
|---|---|---|
| Project structure and config | 10 | Layout, `pytest.ini`, markers registered, requirements complete |
| Fixtures and auth | 20 | base_url/session/token fixtures, `yield` cleanup, env-driven credentials, no duplication |
| CRUD coverage | 15 | All five operations verified with status, body and a follow-up read |
| Negative and status-code tests | 20 | 400/401/403/404/409/422 covered; 401 vs 403 correct |
| JSON schema validation | 10 | Both schemas strict and meaningful; negative proof test |
| Parametrization | 10 | Literal lists, readable ids, no copy-pasted tests |
| Query params and markers | 10 | Pagination, filters, smoke/regression selection works |
| Cleanliness and independence | 5 | No leaked data, order-independent, readable names |

## Hints (no solutions)
- A fixture that yields runs its teardown even when the test fails; code after `yield` is your cleanup.
- Use `session.post(url, json=body, headers=headers)`. For malformed JSON, send `data="{oops"` with a `Content-Type: application/json` header instead of `json=`.
- `uuid.uuid4().hex[:8]` makes a short unique suffix.
- 401 means "who are you?"; 403 means "I know who you are, and no". Decide which one each scenario is before you write the assert.
- `ids=` can be a list of strings, one per case, or a function.
- `jsonschema.validate(instance=..., schema=...)` raises `ValidationError` on a mismatch. Set `"additionalProperties": False` to catch surprise fields.
- `pytest -k name`, `-x`, `-rs`, `--setup-show` and `--fixtures` are your debugging friends.
- Query parameters: `session.get(url, params={"page": 2, "limit": 2})`.
- Seed data (5 items) is the baseline for pagination tests. If numbers look wrong, restart the server and find what leaked.

## Project 2 milestone
**Goal: an automated API suite living in your Project 2 repository.** Use the same skills against your own Project 2 API (or keep the stand-in as a fallback target if your API is not ready; tell your trainer which one you used).

Required by end of Week 7 (start today, finish after Wednesday):
1. Folder `tests/api/` in the Project 2 repo with test modules grouped by resource, and a `conftest.py` with base_url, session and auth fixtures.
2. `pytest.ini` registering `smoke` and `regression` markers with `--strict-markers`.
3. A `README.md` section (or `tests/api/README.md`) with: prerequisites, how to start the API, environment variables table, the run command, and how to run only smoke tests.
4. **One command runs everything**, for example `pytest tests/api` (after `pip install -r requirements.txt`). Write that command in the README.
5. **Authentication handled with environment variables**, not hard-coded: `BASE_URL`, `API_USER`, `API_PASSWORD` (and admin equivalents if needed). Commit a `.env.example` with placeholder values; never commit real secrets. Tests fail with a clear message if a variable is missing.
6. At least 15 tests covering auth (401/403), CRUD, validation (422), schema checks and one pagination/filter scenario, with cleanup of created data.
7. Commit with meaningful messages. Wednesday's data-driven and isolated tests and Friday's pipeline will build on this folder.

Evidence for your trainer: link to the repo folder and a pasted `pytest` summary line.
