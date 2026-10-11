# Thursday Pair Project: Port 3 Tests from Playwright to Cypress and Compare the Tools

**Week 5 - Advanced Web Automation | Day 4 - Thursday | Mode: Collaborative (Pair Programming) | Time: 3 hours (2-3 h of work plus buffer)**
**Project lane:** Project 1 - QE Foundations

You work in a pair. One person **drives** (types), the other **navigates** (reads, researches, thinks ahead). You **swap every 30 minutes**. Together you port three Playwright (Python) UI tests to Cypress (JavaScript), run them, and write an evidence-based comparison note and a short retrospective.

> **Assumption (flagged):** the Project 1 application is not specified in the course material available to this exercise. The starter code therefore ships a small local web app called **ShopLite** (login, product list with sort, cart badge, checkout) and **three stand-in "Project 1" Playwright tests**. If your Project 1 app is reachable and your instructor agrees, port three tests from your own suite instead; keep the same "three different shapes" rule (see Task list) and note the choice in your comparison note.

---

## 1. Why this exercise (and what it synthesizes)

| Week topic | Where it shows up today |
|---|---|
| Mon: interactions (forms, dropdowns, selects, auto-suggest) | Login form, sort dropdown (`.select()`), typing rules |
| Tue: dynamic elements, waiting | Product list loads ~300 ms after the page does |
| Wed: fixtures, POM, data-driven JSON, hooks | `logged_in_page` fixture to `cy.login()`; shared `login-cases.json`; `beforeEach` |
| Thu: Cypress architecture, queries, assertions, debugging, test selection | All ports, plus running with `open`, `run`, `--spec` |
| Project 1 | Ported tests live in the Project 1 repo structure (see section 9) |

**Solvable from existing material only:** every task below cites the Thursday lessons (`written/4-thursday/`), the Thursday demo (`demos/4-thursday/`), or Mon-Wed Playwright knowledge.

---

## 2. Roles

| Role | Does | Does not |
|---|---|---|
| **Driver** | Types the agreed code, runs commands, thinks aloud | Decide silently, search alone for long periods |
| **Navigator** | Reads the Playwright test aloud, opens the lesson section, spots typos and risks, plans the next two steps, keeps the log and the clock | Take over the keyboard ("hands off until the Driver asks") |

Rules: talk constantly; disagree by trying the Navigator's idea for 5 minutes first; both partners must be able to explain every line before you commit.

## 3. Timeboxes and swap schedule

Set a visible 30-minute timer. At every swap: **commit, push, swap roles, update `templates/driver-navigator-log.md`.**
Pair member A drives odd blocks, B drives even blocks (A starts).

| Block | Time | Driver | Navigator | Work | Output |
|---|---|---|---|---|---|
| 0 | 0:00-0:15 | both | both | Setup (section 4), read this README, create branch | App running, Playwright green, `cypress open` launches |
| 1 | 0:15-0:45 | A | B | Task 1: port login test (data-driven) | `01-login-rejected.cy.js` green; commit |
| 2 | 0:45-1:15 | B | A | Task 2: port cart-badge test | `02-add-to-cart-badge.cy.js` green; commit |
| 3 | 1:15-1:45 | A | B | Task 3: port sort test (retry-ability) | `03-sort-price.cy.js` green; commit |
| 4 | 1:45-2:15 | B | A | Task 4: `cy.login()` with `cy.session`; run in `open` and `run`; `--spec` | Refactored, all green in both modes; commit |
| 5 | 2:15-2:45 | A | B | Task 5: comparison note (Navigator proposes the text, Driver types) | `comparison-note.md` complete |
| 6 | 2:45-3:00 | both | both | Retrospective, final run, submit (section 8) | `retrospective.md`, pushed branch |

Short breaks happen at swaps (2-3 minutes). If you run late, shrink Task 5, never the retrospective, and say so in the log. Finished early? Do the stretch tasks (section 6).

---

## 4. Setup (Block 0)

**Requirements:** Node.js 18+ and npm, Python 3.9+ with `pytest-playwright`, Chrome (or Edge/Firefox) installed, git.

```bash
# 1. One person creates the shared repo (or uses the Project 1 repo) and both clone it. Then:
git checkout -b pair/<nameA>-<nameB>

# 2. Copy the contents of starter_code/ into the repo root (keep the folder layout).

# 3. Terminal 1 - the app under test (leave it running)
npm run app                 # http://localhost:3100

# 4. Terminal 2 - prove the Playwright originals pass (your baseline)
pip install -r playwright/requirements.txt
playwright install chromium
npm run pw                  # expect: 6 passed (3 test functions, 4 login params)

# 5. Install Cypress and open it
npm install                 # downloads the Cypress binary too (about 200 MB, once)
npx cypress verify
npm run cy:open             # choose E2E, pick a browser
```

Expected baseline: `6 passed`. If `npm install` cannot download the Cypress binary (network policy), tell your instructor immediately; do not lose the block on it.
Lessons: cypress-architecture-and-setup s.4-6, browser-management s.1-3.

**Starter layout**

```
starter_code/
  app/server.js, app/public/*      local ShopLite app (do not edit)
  playwright/                      the 3 original tests (read only; run as your baseline)
    conftest.py                    logged_in_page fixture
    test_project1_ui.py            test_login_rejected, test_add_to_cart_updates_badge, test_sort_price_low_to_high
  cypress/e2e/0N-*.cy.js           TODO specs (you write these)
  cypress/support/commands.js      cy.getByTest provided; cy.login is a TODO
  cypress/fixtures/*.json          shared data (Playwright reads these too)
  cypress.config.js, package.json
```

---

## 5. Tasks (in order)

Port, do not redesign: keep each test's intent. Run each spec as soon as it is written (`npx cypress run --spec cypress/e2e/01-login-rejected.cy.js`, or in `open`).

### Task 1 - Port the data-driven login test (Block 1)
Port `test_login_rejected` (4 cases from `cypress/fixtures/login-cases.json`) to `01-login-rejected.cy.js`.
- Generate one `it()` per case; each visits `/`, fills the form, clicks Login, asserts the error text, asserts the URL does not contain `inventory`.
- **Hints:** loop over `require('../fixtures/login-cases.json')` (creating tests from data needs data at load time; `cy.fixture` is async) - fixtures-and-custom-fixtures Part A, writing-cypress-tests s.1-2. Typing an empty string throws in Cypress: guard it - element-interaction s.3. Find the button with `cy.contains('button', 'Login')` - element-location s.2. Text assertion: assertions-and-annotations s.3.2.

### Task 2 - Port the cart-badge test (Block 2)
Port `test_add_to_cart_updates_badge` to `02-add-to-cart-badge.cy.js`. Start with a plain `beforeEach` that logs in through the UI (Task 4 improves it).
- Badge absent first, then `1` after adding the backpack, and the Remove button visible.
- **Hints:** absence is `should('not.exist')`, and `not.be.visible` is the wrong check here - assertions-and-annotations s.7. Hooks: s.8.4. The button appears after ~300 ms: do not use `cy.wait(300)`; commands retry - writing-cypress-tests s.5, cypress-architecture-and-setup s.3.

### Task 3 - Port the sort test (Block 3)
Port `test_sort_price_low_to_high` to `03-sort-price.cy.js`.
- Wait for 6 items, select `lohi`, assert prices ascending.
- **Hints:** `.select()` - element-interaction s.5. Read values with `.should(callback)` so the check retries (the Playwright version used a plain `assert` that does not retry) - assertions-and-annotations s.4 and s.6, writing-cypress-tests s.4. Commands do not return values you can assign to variables - cypress-architecture-and-setup s.3.

### Task 4 - Reuse login, then run in both modes (Block 4)
- Create `cy.login(username, password)` in `cypress/support/commands.js` with `cy.session`, add its type to `cypress/support/index.d.ts`, and use it in the Task 2 and 3 specs (`cy.login(); cy.visit('/inventory.html')`).
- Run the whole suite with `npx cypress run`, then in `open`; then run one spec with `--spec`; then mark one test `it.only` and watch what happens (remove it afterwards).
- **Hints:** writing-cypress-tests s.7, fixtures-and-custom-fixtures Part B (s.8), test-selection s.2-3, browser-management s.2-3. Compare with the Playwright `logged_in_page` fixture in `conftest.py`.
- **Break it on purpose:** change one expected value so a test fails, and use the Command Log and `cy.pause()`/`.debug()` to find the cause - cypress-debugging-actions s.2-5. Record what you did in the note's Debugging row.

### Task 5 - Comparison note (Block 5)
Fill in `templates/comparison-note.md` (copy it into your repo as `docs/comparison-note.md`). Every table row needs evidence: a file/line, a command output, or an error message you really saw. Measure speed yourselves (same machine, same browser family, at least 3 runs, state how you measured).

### Task 6 - Retrospective and submit (Block 6)
Fill in `templates/retrospective.md` (both partners together) and `templates/driver-navigator-log.md`. Push the branch (section 8).

---

## 6. Stretch (only when Tasks 1-5 are done)

1. **Fourth port:** write a Playwright checkout test first (add to cart, cart page, checkout form, finish), then port it. Use `cypress/fixtures/checkout.json`.
2. **Tag and select:** add `@cypress/grep` tags `@smoke` / `@regression` to your specs and run only `@smoke` - test-selection s.6-7.
3. **Network control:** stub `/api/products` with `cy.intercept` and a fixture of three products; assert the list length is 3 - writing-cypress-tests s.9.
4. **Role-based locator:** add Testing Library for `findByRole('button', {name: 'Login'})` and compare - element-location s.6.

---

## 7. Definition of Done

- [ ] Three Cypress specs ported (`01`, `02`, `03`), preserving each Playwright test's intent, all green in `cypress run` and in `cypress open`.
- [ ] Login test is data-driven from `cypress/fixtures/login-cases.json`; no `cy.wait(<number>)` anywhere.
- [ ] `cy.login()` uses `cy.session` and is typed in `index.d.ts`; tests 2 and 3 use it.
- [ ] Playwright baseline still passes (`npm run pw`: 6 passed).
- [ ] `comparison-note.md` complete: ported-tests table, every comparison row filled with evidence, at least 2 surprises, a recommendation citing 3+ pieces of evidence.
- [ ] `retrospective.md` and `driver-navigator-log.md` complete (at least 5 swaps logged, with commits).
- [ ] One shared repo and branch `pair/<nameA>-<nameB>`, with commits from BOTH partners (use `Co-authored-by:` trailers when one machine is shared).
- [ ] Both partners can explain any line of the ported specs when asked.

## 8. Submission

Submit **one** per pair:
1. The link to the shared repo and branch `pair/<nameA>-<nameB>` containing: the Cypress project (`cypress/e2e`, `cypress/support`, `cypress/fixtures`, `cypress.config.js`, `package.json`), the unchanged Playwright originals, and `docs/` with `comparison-note.md`, `retrospective.md`, `driver-navigator-log.md`.
2. In the repo README or PR description: the exact commands to run the app, Playwright and Cypress.
3. Do not commit `node_modules/`, screenshots, or videos (the starter `.gitignore` handles this).

## 9. Project 1 - QE Foundations milestone

**Milestone:** the three ported Cypress tests become part of **Project 1's UI test deliverable**, giving the project a second-tool UI suite next to the Playwright suite and a documented tool comparison.
- Keep the Project 1 repo structure: specs under `cypress/e2e`, data under `cypress/fixtures`, helpers under `cypress/support`; the Playwright suite stays where Wednesday's POM refactor put it.
- Add the comparison note under the project's `docs/` and link it from the Project 1 README (tool-choice rationale).
- Friday finalizes the UI deliverable by adding visual checks, so keep your specs small and readable now.
- *(Assumption: the Project 1 specification was not available when writing this brief; if it requires a different folder layout or tests, follow the project spec and tell your instructor.)*

---

## 10. Rubric (100 points)

| Criterion | Points | Full marks look like |
|---|---|---|
| Ports are correct and faithful | 25 | 3 specs pass in `run` and `open`; same intent/assertions as the originals; data-driven loop works |
| Idiomatic Cypress | 15 | Retrying assertions, no fixed waits, `.should(cb)` for list checks, `cy.login` with `cy.session`, readable specs |
| Comparison note quality | 25 | All rows filled; evidence for each; speed measured with method; 2+ real surprises; recommendation cites 3+ evidence items |
| Pair process (log + commits) | 15 | Swaps roughly every 30 min logged; commits from both; Navigator contributions visible |
| Retrospective | 10 | Specific, honest, includes a concrete action |
| Repo hygiene and reproducibility | 10 | One branch, run commands documented, no junk files, fresh clone runs |

Individual accountability: each partner is asked one question about the code (instructor spot-check); a partner who cannot explain a line may lose up to 10 points of the pair score.

---

## 11. Common problems

| Symptom | Cause / fix |
|---|---|
| `cy.visit() failed trying to load: http://localhost:3100` | App not running: `npm run app` in another terminal |
| `cy.type() cannot accept an empty string` | Guard empty values with `if` (Task 1) |
| Page is blank after `cy.login()` | `cy.session` clears the page: add `cy.visit('/inventory.html')` |
| Test fails on `have.length` / flaky | List loads late: use a retrying assertion, not `cy.wait` |
| `const x = cy.get(...)` is not the element | Commands are queued; use `.then()` or `.should(cb)` |
| Playwright `assert 0 == 6` | `all_inner_texts()` does not wait; add `expect(...).to_have_count(6)` first (already in the starter) |
| Port already in use | `PORT=3200 npm run app`; update `baseUrl` in `cypress.config.js` and `playwright/pytest.ini` |

## 12. For the instructor

`solution/` holds the reference Cypress port (`cypress/e2e/01-03` plus a stretch checkout spec and its Playwright original), `cy.login` implementation, a sample comparison note and a sample retrospective. Do not hand out `solution/` before the debrief.
