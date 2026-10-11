# Exercise: API Testing Fundamentals with Postman

**Week 7, Monday** | Time box: 2-3 hours | Individual work | Tool: Postman (desktop or web), Python 3 for the server

## Objectives
By the end you can:
1. Explore an unfamiliar REST API and document what you find.
2. Build an organised Postman collection (folders Auth, Items, Negative).
3. Use environment variables, pre-request and post-response scripts to chain requests (login token, created item id).
4. Write `pm.test` assertions on status, body, headers and response time.
5. Cover negative cases (400, 401, 403, 404, 409, 422) and run everything with the Collection Runner.
6. Report defects and observations with evidence.

## Prerequisites and setup
- Postman installed and signed in (or Postman web with the desktop agent).
- Python 3.9+.
1. Copy the `starter_code/` folder to your working directory.
2. Start the server: `python project2_api_server.py` (listens on `http://127.0.0.1:8000`). Check `http://127.0.0.1:8000/health` in a browser.
3. In Postman: Import `project2-local.postman_environment.json` and `collection-skeleton.postman_collection.json`. Select the "Project2 Local" environment (top right).
4. Read `api-contract.md`. Restarting the server (or `POST /admin/reset` as admin) restores the seed data.

## Scenario
You have joined the QA team of an online stationery shop. Its inventory API is ready for testing, but there are no automated checks yet. Your job is to produce a Postman collection the team can run before every release. This server is a stand-in for your Project 2 API; the same skills apply there (see the Project 2 milestone below).

## Stage 1: Explore (about 25 min)
1. Send `GET /health`. Note status, headers (especially `Content-Type`, `X-Request-Id`) and body.
2. Send `GET /items`, then add query params `category`, `q`, `page`, `limit`. Record what each does and what happens with `limit=0`.
3. Send `GET /items/1` (path variable) and `GET /items/9999`.
4. Log in with `POST /auth/login` using a JSON body. Inspect the Postman Console (View > Show Postman Console) to see the raw request and response.
5. Try an item `POST` without a token, then with one. Write down three questions or surprises in your notes file.

## Stage 2: Build the collection (about 30 min)
1. Use the skeleton collection. Keep the folders **Auth**, **Items**, **Negative**; rename the collection "Project 2 API".
2. Auth: health check, login as tester, login as admin.
3. Items: create, get by id, list with query parameters, full update (PUT), partial update (PATCH), delete (admin), get-after-delete.
4. Negative: one request per error condition (stage 5).
5. Give requests clear names (`METHOD - purpose`), and add a short description to each folder. Set `Content-Type` headers for bodies.

## Stage 3: Variables, environments and chaining (about 30 min)
1. Replace every hard-coded host with `{{baseUrl}}`. Use `{{username}}` and `{{password}}` in the login body.
2. In the login request's **Tests** (post-response) script, save the token to the environment variable `token`. Send protected requests with an `Authorization: Bearer ...` header built from it.
3. Do the same for the admin login with a second variable (suggested: `adminToken`), used only for DELETE.
4. In Create item, save the new item's `id` into `itemId`; use `{{itemId}}` in get, update, patch, delete and get-after-delete requests.
5. Make the Create body unique on every run using a dynamic variable so the collection is re-runnable without restarting the server.
6. Prove the chain: clear `token` and `itemId`, run Auth then Items, and observe them being set in the environment quick-look.

## Stage 4: Assertions in the Tests tab (about 35 min)
Add `pm.test` blocks to every request. As a minimum, across the collection, cover:
- **Status code** (exact, not a range).
- **Body**: required fields and types, values you sent are echoed, list responses have the pagination envelope, filters really filter.
- **Headers**: `Content-Type` is JSON; `Location` on create; `X-Request-Id` present.
- **Response time** under a threshold you justify (state it in your notes).
- **204 handling**: an empty body for delete.
Each test needs a descriptive name that reads like a requirement. Break one test on purpose to see it fail, then fix it.

## Stage 5: Negative cases (about 25 min)
Add requests in the Negative folder that provoke each of the following, asserting both status code and the error body shape:

| Code | Condition to provoke |
|---|---|
| 400 | malformed paging input |
| 401 | protected call without a token; login with wrong credentials |
| 403 | a valid but non-privileged user attempting an admin action |
| 404 | resource that does not exist |
| 409 | creating something that already exists |
| 422 | well-formed JSON with invalid field values (try several bad fields in one request and read the `details`) |

## Stage 6: Run and export (about 15 min)
1. Run the whole collection in the **Collection Runner** with the Project2 Local environment. Everything should pass. Run it twice in a row; it must still pass.
2. Export the collection (v2.1) and the environment (after a run; remove any value you consider sensitive).
3. Write your notes file.

## Stretch goals
- Add a collection-level pre-request script that logs in automatically when `token` is empty.
- Parameterise the Negative 422 request with a Runner data file (CSV/JSON) of at least five invalid bodies.
- Verify idempotency: show that repeating a PUT is safe and repeating a POST is not.
- Check `HEAD` and `OPTIONS` on `/items`, and wrong methods (405).
- Use a collection variable for the response-time threshold.

## Deliverables
Submit in a folder `week7-monday-<yourname>/`:
1. `project2.postman_collection.json` (exported v2.1).
2. `project2-local.postman_environment.json`.
3. `NOTES.md`: **three bugs or observations** about the API. For each give: request, expected vs actual, evidence (status/body), and your severity. Add the response-time threshold you chose and one thing that was harder than expected.
4. A screenshot of the Collection Runner result (all green).

## Definition of Done
- [ ] Server started; environment imported and selected
- [ ] Collection has folders Auth, Items, Negative with named requests
- [ ] No hard-coded host, token or id in any request
- [ ] `token` is saved by a script; `itemId` is chained from the create request
- [ ] Every request has at least two meaningful `pm.test` assertions; at least one on body, header and response time overall
- [ ] Negative cases for 400, 401, 403, 404, 409 and 422 all pass
- [ ] Collection passes in the Runner twice in a row without restarting the server
- [ ] Collection and environment exported; JSON opens as valid
- [ ] Notes contain three bugs/observations with evidence

## Grading rubric (100 points)
| Criterion | Weight | Full marks when |
|---|---|---|
| Collection structure and naming | 15 | folders, clear names, descriptions, correct methods, headers and bodies |
| Variables and environments | 20 | `baseUrl`, saved `token`, chained `itemId`, no hard-coding, re-runnable |
| Assertions quality | 25 | status plus body, header and timing checks; descriptive names; not tautological |
| Negative testing | 15 | all six codes covered, asserting status and error body |
| Runner run and exports | 10 | green run, valid exported files, screenshot |
| Bug/observation notes | 10 | three evidenced, reproducible findings |
| Professional habits | 5 | tidy, reasoned thresholds, clear notes |

## Common pitfalls and hints
- Environment values are strings. When comparing `itemId` with a number in a test, convert it.
- A fixed item name will give 409 on the second run. Think about which dynamic variables exist.
- Request returns 401 right after a server restart? Tokens are held in memory; log in again.
- Scripts in the **Tests** tab run after the response; **Pre-request** runs before sending. Choose the right one for saving values.
- Run the Auth folder before Items, or the Runner order will break chaining. Order matters.
- Console (View > Show Postman Console) is the quickest way to debug a script; `console.log(pm.response.json())`.
- A 204 has no body: `pm.response.json()` throws. Test it differently.
- Check that the environment is *selected*, not just imported.
- An assertion that cannot fail (`pm.expect(true)`) is worth nothing.

## Reference: where to look (no solutions)
| Need | Look at |
|---|---|
| Read a response in a script | the `pm.response` object (`code`, `json()`, `text()`, `headers`, `responseTime`) |
| Store or read a variable | `pm.environment`, `pm.collectionVariables`; use `{{name}}` in URLs, headers and bodies |
| Make a value unique per run | Postman dynamic variables (`{{$...}}`) |
| Assert | `pm.test("name", fn)` with `pm.expect(...)` (Chai-style) or `pm.response.to.have...` |
| Order of execution | requests run top to bottom in folder order in the Runner |
| Inspect what was sent | Postman Console, and the Code snippet panel |

## Suggested working order and checkpoints
1. After stage 2, every request sends manually and returns what you expect.
2. After stage 3, running Auth then Items needs no manual copying of anything.
3. After stage 4, deliberately change one expected value; the Runner must go red and name the failing test.
4. After stage 5, restart the server and run the entire collection from the top: it must pass from a clean state.
Ask for help after 15 minutes stuck, with the Console output ready.

## How to write your notes
A good observation is specific and reproducible: "PUT /items/6 without `stock` leaves the old value; expected the default of 0 for a full replace (see api-contract.md)". Distinguish a **bug** (contradicts the contract or HTTP semantics) from an **observation** (legal but surprising, or a design question). Include the exact request and the response you got. Compare behaviour with what the written material on methods says about PUT and PATCH, 401 versus 403, and 404 versus 405.

## Project 2 milestone
> This section is graded as part of the Project 2 Test Automation Framework, not the Monday exercise.

Apply the same approach to your **real Project 2 API** (or the stand-in until it is available):
1. Create `api-tests/postman/` in your Project 2 repository.
2. Commit the exported collection (`*.postman_collection.json`) and environment (`*.postman_environment.json`, no real secrets) there. Cover at least login, one create/read/update/delete lifecycle, and the 401, 403, 404 and 422 negative cases.
3. Add `api-tests/postman/README.md` explaining: prerequisites, how to start the API, how to import the files, how to run the collection in the Runner, expected result (number of requests, passing assertions), and how to switch `baseUrl` to another environment.
4. Commit with a descriptive message and show your instructor a green Runner result. Later in the week these files can be reused for command-line runs and the CI/CD pipeline.
