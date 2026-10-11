# Lab: Make the Cypress Suite Diagnosable, Documented and Visually Protected (5-friday)

**Week 5: Advanced Web Automation | Day 5: Cypress Advanced and Visual Testing**
**Mode:** A (Implementation, Code Lab) | **Format:** individual (Friday is not a pair day) | **Time:** 2 to 3 hours
**Project link:** Project 1 - QE Foundations, UI deliverable (final milestone, see the last major section)

**Theory you are applying** (in `written/5-friday/`): `[TTD]` trace-time-travel-debugging.md, `[SSV]` screenshots-and-video.md, `[LOG]` logging.md, `[REC]` recording-user-actions.md, `[EGC]` editing-generated-code.md, `[VIS]` visual-testing.md.
**Demo you watched:** `demos/5-friday/Instructor_Demo.md` and its code. This lab repeats the same techniques on a different app, so you cannot copy-paste your way through.

---

## 1. Scenario

Your team's UI tests exist. Today a reviewer says: "I cannot tell *why* a test failed, nobody knows what the recorded test does, and last month a CSS change turned every button orange and every test stayed green."

You are given **QE Shop**, a small local web app (login, product list, cart, checkout), a Cypress project skeleton full of `TODO`s, and one raw recorded test. You will:

1. Capture evidence (screenshots and video) and log usefully,
2. Turn the recorded test into a maintainable one,
3. Add visual regression checks that mask dynamic content and use a sensible threshold,
4. Trigger a visual difference on purpose and diagnose it,
5. Apply the same finishing steps to your **Project 1 UI deliverable** and submit it.

> **Assumption flag (Project 1):** the Project 1 application and its exact scope are defined by your Project 1 brief, which this lab does not contain. The Project 1 section below is therefore written generically ("your application under test", "your UI suite"). If your brief says something different, the brief wins.

> **Verification flag:** the Cypress specs in `solution/` were **not executed** by the author, because the Cypress binary could not be downloaded in the authoring environment. They were checked with `node --check`, by loading `cypress.config.js`, by running the plugin's compare function offline, and by driving every flow in a real browser outside Cypress. If a starter or solution detail behaves differently on your machine, tell your instructor; do not silently change thresholds to make it pass.

---

## 2. What is in this folder

```
exercise/5-friday/
  README.md                 <- this file
  starter_code/             <- you work here
    app/                    <- QE Shop (static HTML/CSS/JS). Do not edit, except to READ it
    server.js               <- zero-dependency local server (npm start / npm run start:diff)
    package.json            <- Cypress ^15.21.1 and cypress-visual-regression 5.3.0 (same pins as the demo)
    cypress.config.js       <- TODOs 2.1, 2.2, 3.1, 5.2
    cypress/support/        <- e2e.js (TODOs 4.1, 5.3), commands.js (TODOs 3.2, 4.5; stabilise is given)
    cypress/e2e/            <- smoke.cy.js (given), checkout.cy.js, logging.cy.js, visual.cy.js (starters)
    cypress/recorded/       <- raw-checkout.cy.js (given, "before" picture, do not edit)
    cypress/fixtures/users.json
    tools/threshold-check.js <- offline threshold experiment (Task 5.1)
    docs/DIAGNOSIS.md       <- template for Task 6
    project1/               <- README.template.md and FINAL_CHECKLIST.md for the Project 1 milestone
  solution/                 <- instructor only. Do not open before you have tried each task
```

### Prerequisites

- Node.js 20 or newer, npm, Chrome (recommended; Electron also works if you use it for *both* baseline and compare).
- Two terminals open in `starter_code/`.
- Cypress binary download allowed on your machine (first `npm install` downloads it).

---

## 3. Setup (about 10 minutes)

```bash
cd exercise/5-friday/starter_code
npm install                       # installs cypress ^15.21.1 and cypress-visual-regression 5.3.0
npm run check                     # node --check on every JS file: must print no errors
npm start                         # terminal 1: QE Shop on http://localhost:4173 (leave running)
```

Open http://localhost:4173 in a browser, log in with `standard_user` / `secret_sauce` (practice data), add a product, go to the cart, check out. Notice two things that change **by design** on the product page: a ticking "Prices updated" clock and a random "Visitors online" number. They are your masking targets.

In terminal 2:

```bash
npx cypress --version             # note the version in your notes (Studio steps differ by version, [REC] 3.1)
npx cypress run --spec cypress/e2e/smoke.cy.js
```

The smoke spec must pass before you touch anything else. If the app is on another port, set `PORT` for the server and change `baseUrl` in `cypress.config.js`.

**Notes file:** create `NOTES.md` in `starter_code/` now. You will record answers to the "write down" prompts in it.

---

## 4. Staged tasks

Time estimates are for a focused trainee; the total is in the table at the end.

### Task 1: Look before you leap (10 min)

1. Run `npx cypress open`, choose E2E, pick Chrome, open `recorded/raw-checkout.cy.js`.
2. **Time travel** `[TTD]` s.4-5: hover each row in the Command Log, then **pin** the click on `#finish`. Check the Before/After snapshot and the URL.
3. Open `cypress/e2e/smoke.cy.js` and note how the command log differs between a hover and a pin.

**Write down (NOTES.md):** (a) Which fields did the raw test fill and which assertions does it contain? (b) Name three weaknesses you can already see (use the `[EGC]` s.2 checklist).

*Hints:* `[TTD]` s.2 (Command Log), s.4 (hover), s.5 (pin).

### Task 2: Screenshots and video configuration (15 min)

Edit `cypress.config.js` (TODOs 2.1 and 2.2).

- **2.1** Set `screenshotsFolder` to `cypress/snapshots/actual`, `screenshotOnRunFailure: true`, `trashAssetsBeforeRuns: true`, `videosFolder: 'cypress/videos'`, `video: true`, `videoCompression: 32`.
- **2.2** Add an `after:spec` handler that deletes the video when no attempt of any test failed. Remember to `require('fs')` (uncomment it).
- **2.3 Prove it works.**
  - `npx cypress run --spec cypress/e2e/smoke.cy.js --env demoFailure=true` -> find the failure screenshot (named `... (failed).png`, in a folder under `cypress/snapshots/actual/`) and the **kept** video in `cypress/videos/`.
  - `npx cypress run --spec cypress/e2e/smoke.cy.js` -> the video must be **gone** (spec passed).
- **2.4** Evidence screenshot: once Task 4 is done, add one `cy.screenshot('evidence/order-confirmation', { capture: 'viewport', blackout: [...] })` to the end of your checkout test, blacking out the order number.

**Write down:** Why are baselines kept in `cypress/snapshots/base` while screenshots go to `cypress/snapshots/actual`? What would `trashAssetsBeforeRuns` do to them otherwise? What does a `capture: 'runner'` screenshot show that `viewport` does not, and why is it wrong as a visual baseline?

*Hints:* `[SSV]` s.6 (failure screenshots, `cypress run` only), s.7 (folders and trash), s.8 (video defaults, off since Cypress 13), s.10 + Example 4 (`after:spec`), Example 2 (`blackout`). `[VIS]` pitfall 5 (baselines wiped).

### Task 3: Logging that helps you at 2 a.m. (20 min)

- **3.1** In `cypress.config.js` add `on('task', { log, logToFile })`. `log` prints a timestamped line to the terminal; `logToFile` appends to `cypress/logs/<file>` (default `cypress-run.log`). **Both must `return null`.**
- **3.2** In `cypress/support/commands.js` write `sanitize()` (recursive, masks `password`, `token`, `authorization`, `cardNumber`), expose it as `Cypress.sanitize`, and build `cy.step(title)` and `cy.logInfo(message, data)`. Each writes to the Command Log **and** the terminal (through `cy.task`, with `{ log: false }`).
- **3.3** Complete `cypress/e2e/logging.cy.js`: (a) a test that proves the queue order is A, C, B; (b) a test for `Cypress.sanitize`; (c) *optional*: a test that calls `cy.logInfo` with a password, writes a line with `logToFile`, and reads `cypress/logs/cypress-run.log` back with `cy.readFile`.
- **3.4** Run it headless. In the **terminal** you should see your `STEP:` lines and the timestamped info line, with the password shown as `***`.

**Write down:** In which of the four places (Command Log, browser console, terminal, file) does a plain `console.log` appear during `cypress run`? Why did the "wrong count" in `[LOG]` Example 2 print 0?

*Hints:* `[LOG]` s.1 (four places), s.2 (queue trap), s.7 + Example 3 (`cy.task`, return null), Example 4 (`logInfo`, `step`), Exercise 1 and Exercise 4.

### Task 4: Clean a recorded test (30 min)

`cypress/recorded/raw-checkout.cy.js` is what a recorder produces. Do **not** edit it. Create the cleaned version in `cypress/e2e/checkout.cy.js`.

1. **Freeze the behaviour:** run the raw spec first and note what it does (`[EGC]` s.3).
2. **Commands first (TODO 4.5)** in `commands.js`: `cy.login()` (UI login once, cached with `cy.session`, validate the `session-username` cookie, password from `Cypress.env('APP_PASSWORD')` typed with `{ log: false }`), `cy.addProductToCart(name)` (find the card by product **name**), and `cy.openApp(path)` (a `cy.visit` that appends `?diff=on` when `Cypress.env('appDiff')` is set; you need it in Task 6).
3. **Rewrite the test** following the checklist at the top of the starter file. Required result:
   - behaviour-style `describe`/`it` names, no `cy.viewport`, no full URL, no `cy.wait(2000)`;
   - `data-test` selectors only (set the Selector Playground priority in `support/e2e.js`, TODO 4.1);
   - customer data from the fixture, password from env;
   - **four assertion layers:** guard (URL), state (badge `2`, two cart rows, item total `$39.98`), outcome (confirmation header text), negative (cart badge no longer exists);
   - `cy.step()` headings;
   - `beforeEach` with `cy.login()` + `cy.openApp('/inventory.html')`, and a readiness assertion instead of a wait.
4. **Add one negative test:** an empty first name shows `Error: First Name is required` and the URL still contains `/checkout.html`.
5. **Prove stability** `[EGC]` s.12: run the spec three times in a row, all green. (Do **not** commit a `_.times` loop.)

**Write down:** a before/after table with at least five rows (what was wrong in the recording, what you did, which `[EGC]` step it belongs to). Version note: if you also try Cypress Studio (stretch), record your Cypress version and whether `experimentalStudio` was needed (needed on 10.7 to 14.x, removed in 15.4.0, `[REC]` s.3.1).

*Hints:* `[EGC]` s.4 (names), s.5 (noise), s.6 (selectors, scoping by name), s.7 (assertion layers), s.8 (waits), s.9 (data), s.10 + Example 2 (`cy.session`, commands), s.11 (hooks). `[REC]` Example 2 (selector priority), s.6 (record, review, refine).

### Task 5: Visual regression checks (35 min)

#### 5.1 Know your unit first (5 min)

```bash
npm run check:threshold
```

The script compares two synthetic 400 x 250 images that differ in a 15 x 15 square (225 of 100,000 pixels = 0.225 percent) with several `errorThreshold` values. **Predict before you run:** which thresholds fail? Then read the output.

Demo finding you must apply: in `cypress-visual-regression` **5.3.0** the plugin computes `mismatched / width / height`, a **fraction** from 0 to 1, and compares it directly with `errorThreshold`. So `errorThreshold: 0.1` means **10 percent**, not 0.1 percent, whatever `[VIS]` Step 3 says. You will convert with a one-line helper (5.3).

**Write down:** which thresholds failed, and why `0.5` and `0.005` both pass here even though they differ by 100x.

*Hints:* `[VIS]` s.4 (pixel arithmetic), Exercise 1; demo `tools/offline-visual-check.js`.

#### 5.2 Configure the plugin (5 min)

In `cypress.config.js` (TODO 5.2): import `configureVisualRegression`, call it as the **first line** of `setupNodeEvents`, and add the five `visualRegression*` entries to `env` (type `regression`, base dir `cypress/snapshots/base`, diff dir `cypress/snapshots/diff`, generate diff `fail`, fail silently `false`). *Hint:* `[VIS]` Step 2.

#### 5.3 Register the command (5 min)

In `cypress/support/e2e.js` (TODO 5.3): `Cypress.pct = (percent) => percent / 100;` then `addCompareSnapshotCommand({ capture: 'viewport', errorThreshold: Cypress.pct(0.1) })`. *Hint:* `[VIS]` Step 3.

#### 5.4 Write the visual spec (15 min)

Complete `cypress/e2e/visual.cy.js` (remove each `.skip`). Required:

| Snapshot name | Scope | Masking | Threshold |
|---|---|---|---|
| `login-page` | viewport | none | global default (0.1 %) |
| `inventory-viewport` | viewport | `blackout` on the clock **and** the visitor counter | 0.1 % |
| `inventory-list` | element `[data-test="inventory-list"]` | none needed (explain why) | 0.05 % |
| `inventory-card-first` | element, first product card | none | 0.05 % |
| `order-complete` | viewport after a full checkout | `blackout` on the order number | 0.1 % |

Rules: fixed `cy.viewport(1280, 800)`, a readiness assertion and `cy.stabilise()` **before every snapshot**, thresholds always written as `Cypress.pct(...)`, and a short **threshold policy comment** above the tests. `cy.stabilise()` is given: in NOTES.md explain what its three parts fix.

*Hints:* `[VIS]` s.7 (scope: broad to narrow), s.8 (determinism, causes 1-8), s.9 (masking, mask the minimum), Step 5, pitfall 7 (the mask must be present when the baseline is created). `[SSV]` Example 2.

#### 5.5 Generate and review baselines, then compare (5 min)

```bash
npm run visual:base         # creates baselines (tests pass because there is nothing to compare)
```

Open `cypress/snapshots/base/cypress/e2e/visual.cy.js/` (baselines are stored **per spec path**, so the spec file path is part of the folder) and **look at every PNG**: is anything half-loaded? Are the clock and visitor counter black boxes?

```bash
npm run visual:compare      # must be green. Run it twice.
```

#### 5.6 Experiment: what does the mask buy you? (5 min, do not commit)

Temporarily remove the `blackout` from `inventory-viewport` **and** set its threshold to `0`; re-run `visual:compare` twice, waiting a few seconds between runs. Expect a failure with a mismatch of tens of pixels (just the changed digits). Then restore your solution.

**Write down:** Why would a 0.1 % threshold hide this noise, and why is that *also* a risk (what real change could hide in the same budget)? State your rule for choosing mask versus threshold.

*Hints:* `[VIS]` s.8 cause 7 ("thresholds are the last tool"), Exercise 4, Scenario 3.

### Task 6: Trigger and diagnose an intentional visual difference (15 min)

The app has a deliberate-diff toggle that simulates an unreviewed "rebrand" CSS change.

```bash
npm run visual:diff         # same server; adds ?diff=on to each page via cy.openApp
```

(Alternative: stop the server and run `npm run start:diff`, then `npm run visual:compare`.)

1. The visual spec must now **fail**. Open `cypress/snapshots/diff/cypress/e2e/visual.cy.js/` and look at the diff images.
2. Fill in `docs/DIAGNOSIS.md`: which snapshots failed, mismatch numbers (the failure message rounds the fraction to two decimals, so also read the numbers in the Command Log "compareScreenshots" console props), a plain-words description of **what** changed and **where**, and a classification (regression, intentional change or noise) with evidence.
3. **Approve it deliberately:** pretend the product owner confirmed the rebrand. Regenerate baselines for **this spec only** with the diff on (`npx cypress run --spec cypress/e2e/visual.cy.js --env visualRegressionType=base,appDiff=on --config video=false`), review the changed PNGs, then confirm `npx cypress run --spec cypress/e2e/visual.cy.js --env appDiff=on --config video=false` is green **against the new app look** (and that `npm run visual:compare` on the normal app is now red). Finally restore the original baselines with `npm run visual:base` on the normal app and confirm green again. Record the commands in the diagnosis file.
4. Keep the failing diff images and a copy of the failure screenshot under `evidence/`.

**Write down:** one sentence on why "a visual test that cannot fail is worthless" and one on why re-baselining without review defeats the purpose.

*Hints:* `[VIS]` Steps 7-9, s.10 (baseline management in a team), pitfall 5. Demo `Instructor_Demo.md` Phase 5.

### Stretch tasks (optional, in any order)

- **S1 Stub instead of mask (20 min).** In a second visual test of the inventory page, freeze the clock with `cy.clock(...)` and stub `Math.random` through `cy.visit(..., { onBeforeLoad })` so the page is **identical every load**, then snapshot **without** `blackout`. Compare the trade-offs with masking. `[VIS]` s.8 cause 5, "Freezing time".
- **S2 Record with a recorder (20 min).** Record "log in, log out" with Cypress Studio **or** the Chrome DevTools Recorder, then clean it with the Task 4 steps. Note your version and the Studio flag rule. `[REC]` s.3-4, `[EGC]`.
- **S3 CI sketch (15 min).** Write `.github/workflows/cypress.yml`-style YAML (not executed) that starts the app, runs the suite and uploads `cypress/snapshots/diff`, `cypress/screenshots` and `cypress/videos` on failure. `[SSV]` s.11, `[VIS]` Step 11.
- **S4 Debuggable custom command (15 min).** Rewrite `cy.addProductToCart` with `Cypress.log` plus before/after snapshots so it shows up properly in time travel. `[TTD]` Example 3, Exercise 3.
- **S5 Failing on purpose (10 min).** Use `.debug()` and `cy.pause()` once to inspect the cart, then remove them. `[TTD]` s.8, pitfall 3.

---

## 5. Definition of Done

You are done with the lab when **all** of these are true:

- [ ] `npm run check` passes; the smoke spec passes.
- [ ] `cypress.config.js` sets screenshots/video as in Task 2; a failing run keeps screenshot **and** video, a passing run deletes the video (shown in `evidence/`).
- [ ] `cy.step` and `cy.logInfo` exist; the terminal shows `STEP:` lines and a masked password; `logging.cy.js` has no `.skip` and passes.
- [ ] `checkout.cy.js` is the cleaned test: no `cy.wait(<number>)`, no `.skip`, no hard-coded URL/viewport/password, data-test selectors only, four assertion layers, one negative test; green three runs in a row.
- [ ] `visual.cy.js` has the five snapshots of the table, masks on the two dynamic elements and the order number, thresholds via `Cypress.pct`, a threshold policy comment; `visual:compare` green twice in a row.
- [ ] Baselines are committed under `cypress/snapshots/base/` and you looked at each PNG.
- [ ] Task 6 done: visual spec fails with the deliberate diff, `docs/DIAGNOSIS.md` completed, original baselines restored and green.
- [ ] `NOTES.md` contains every "Write down" answer.
- [ ] Project 1 milestone checklist (section 6) complete.
- [ ] No `node_modules`, secrets, videos or `actual/` folders committed.

---

## 6. Project 1 - QE Foundations milestone: finalize the UI deliverable

**Why today:** Friday closes the UI half of Project 1. You finish the deliverable so that another engineer can run it, trust it, and see what it protects.

**What you finalize** (assumption: your Project 1 brief defines the application under test, the user journeys and whether the main UI suite is Playwright, Cypress or both; adapt the words, keep the structure):

1. **Apply Friday's techniques to your Project 1 UI tests** in the Cypress project you built on Thursday (the three ported tests):
   - screenshot/video configuration and an evidence screenshot,
   - `cy.step` logging in the longest test,
   - any recorded or copied test cleaned (no waits, stable selectors, four assertion layers),
   - **at least two visual checks** on your own application: one whole-page and one element, each with dynamic content masked or stubbed, thresholds written with the unit your plugin version expects, baselines reviewed and committed.
2. **Prove the visual checks can fail** on your application: introduce a harmless CSS change in a *local copy* or via browser override, capture the diff image, revert, and save both under `evidence/`.
3. **If your main Project 1 suite is Playwright**, keep it in the repo, make sure it also passes and is documented, and state in the README which suite covers which journeys. Cypress is the home of Friday's visual checks.
4. **Write the deliverable README** using `starter_code/project1/README.template.md`.
5. **Tick every line** of `starter_code/project1/FINAL_CHECKLIST.md`. Summary of the checklist:

| Area | Final checks |
|---|---|
| README | purpose, exact versions, install/run, test inventory, visual policy (with the unit), artifacts table, latest result, honest limitations |
| Run instructions | verified from a **fresh clone** by you, ideally by a classmate; app start command documented; no secrets in git |
| Passing suite | `cy:run` exit code 0 twice in a row; `visual:compare` green; no `.skip`, `.only`, `cy.pause`, `.debug`, `cy.wait(number)` |
| Artifacts | committed baselines; failure screenshot + video + diff image + run log in `evidence/`; completed `docs/DIAGNOSIS.md`; pasted final run summary |
| Hygiene | `.gitignore`, no `node_modules`, tidy history, final commit tagged or noted `project1-ui-final` |

**Time:** 30 to 40 minutes if your Thursday work is in good shape. If something in Project 1 is not finished, finish the *smallest* defensible scope and list the rest under "Known limitations" in the README. An honest limitation beats a hidden gap.

---

## 7. Submission

Submit **one Git repository or branch** (or a ZIP without `node_modules`) containing:

1. Your completed `starter_code/` (renamed or not), including `NOTES.md`, `docs/DIAGNOSIS.md` and the `evidence/` folder.
2. Your Project 1 UI deliverable repository link or branch, with the README and ticked `FINAL_CHECKLIST.md`.
3. A 5 to 8 sentence reflection (in the checklist): what Friday changed in how you debug, document and protect a UI.

Pre-submit commands: `npm run check`, `npm run cy:run` (twice), `npm run visual:compare`, `git status` (nothing unwanted staged).

---

## 8. Rubric (100 points)

| Area | Points | Full marks look like |
|---|---|---|
| Screenshots, video, config (Task 2) | 10 | All config keys correct; failure keeps screenshot + video; pass deletes video; baseline/actual separation explained |
| Logging (Task 3) | 10 | Tasks return null; `step`/`logInfo` log to Command Log and terminal; secrets masked; both logging specs prove behaviour |
| Cleaned recorded test (Task 4) | 20 | All checklist items; four assertion layers; commands + session; negative test; three green runs; strong before/after table |
| Visual regression (Task 5) | 25 | Correct fraction/percent handling; five snapshots; right scope; minimal masks present at baseline time; sensible thresholds with policy; baselines reviewed; green twice; clear mask-vs-threshold reasoning |
| Intentional diff diagnosis (Task 6) | 10 | Fails for the right reason; diagnosis precise and classified with evidence; deliberate approve/restore cycle done safely |
| Project 1 milestone (section 6) | 20 | README usable from a fresh clone; suite green; artifacts present; visual checks on own app can fail; honest limitations |
| Craft and submission | 5 | Clean repo, no secrets/node_modules, NOTES complete, reflection thoughtful |

Deductions: committed `cy.pause`/`.only`/`.skip`/number waits (-2 each, max -6); thresholds raised to make a failing test pass without diagnosis (-5); baselines never viewed (-5).
Stretch tasks earn up to **+5 bonus** (not above 100).

---

## 9. Time estimates

| Part | Minutes |
|---|---|
| Setup and Task 1 | 20 |
| Task 2 Screenshots/video | 15 |
| Task 3 Logging | 20 |
| Task 4 Clean recorded test | 30 |
| Task 5 Visual regression | 35 |
| Task 6 Diff and diagnosis | 15 |
| Project 1 milestone and submission | 35 |
| **Core total** | **170 (about 2 h 50 min)** |

If you are slower than this: do Tasks 1-5 and Task 6 steps 1-2, then the Project 1 milestone with the *minimum* of two visual checks. Skip all stretch tasks. If you are faster, take S1 and S2.

## 10. Troubleshooting

| Symptom | Likely cause |
|---|---|
| `cy.compareSnapshot is not a function` | Task 5.3 not done (or support file not loaded) |
| "Base screenshot not found at ..." | no baselines yet for this spec path; run `npm run visual:base`; renamed or moved the spec |
| `ECONNREFUSED` / blank page | `npm start` not running or wrong port in `baseUrl` |
| Visual test passes after a deliberate change | threshold is a fraction: `0.1` is 10 percent. Use `Cypress.pct(0.1)` |
| Failure message says `0.00` but test fails | message rounds the fraction to 2 decimals; read the real numbers in the console props |
| Baselines vanished after a run | they were stored in the `screenshotsFolder`; keep them in `snapshots/base` |
| Task "undefined" error from `cy.task` | handler returned `undefined`; return `null` |
| Stale diff images confuse you | `cypress/snapshots/diff` is not auto-cleaned; delete it before a fresh run |
| Studio button missing | version path differs: flag needed on 10.7-14.x, removed in 15.4.0; Studio is Beta, rely on what your version shows |
| Visual test flaky between machines | different OS/browser/fonts; generate and compare in the same environment (`[VIS]` s.8 cause 1) |
