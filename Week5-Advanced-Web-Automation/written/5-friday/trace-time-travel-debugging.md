# Trace and Time-Travel Debugging in Cypress

## Learning Objectives

By the end of this lesson you will be able to:

- Describe the main parts of the Cypress Test Runner (Command Log, app preview, spec list, Selector Playground) and explain what each one is for.
- Explain what a **snapshot** is in Cypress and how hovering over a command in the Command Log "travels back in time" to show you the page as it looked at that moment.
- **Pin** a command, switch between its **Before** and **After** snapshots, and use the pinned state to print rich details to the browser DevTools console.
- Read a failing Cypress test from top to bottom: identify the failing command, the failing assertion, the retry behaviour and the error message.
- Use `.debug()`, `cy.pause()`, the Selector Playground and `cypress open` together as a repeatable debugging workflow.
- Explain what Cypress does and does **not** offer as a "trace" (there is no `trace.zip` file like in Playwright), and identify **Cypress Cloud Test Replay** as the nearest equivalent for CI failures.
- Contrast Cypress time-travel debugging with the **Playwright Trace Viewer** and choose the right tool for a given debugging situation.
- Flag which behaviours depend on the Cypress version, the run mode (`open` vs `run`) and the browser.

---

## Why This Matters

This week's epic is to master complex UI interactions in Playwright, structure tests with fixtures, hooks and the Page Object Model, and then learn Cypress for a cross-tool perspective and visual testing. On Thursday you wrote your first Cypress tests, learned how Cypress locates and interacts with elements, and met `.debug()` and `cy.pause()`. Today we go deeper into the single feature that makes many engineers fall in love with Cypress: **you can see what your test did, step by step, and rewind it.**

Why does that matter for **Project 1: QE Foundations**? Because writing a UI test is only half of the job. The other half is *keeping it healthy*:

- A test fails in CI at 2 a.m. Was it a real product bug, a changed selector, a slow API or a flaky timing issue? You need evidence.
- A teammate asks, "Why did the login test fail?" and you need to show them, not just describe it.
- When you finalise your Project 1 UI deliverable, a reviewer will expect that you can diagnose failures quickly, not just produce green tests on a good day.

A quality engineer who can debug fast is far more valuable than one who writes tests fast but cannot explain why they break. Time-travel debugging shortens the "why did this fail?" loop from tens of minutes to a few seconds.

You already saw a similar idea earlier in the course with Playwright's tooling (its Trace Viewer, which records a full run and lets you inspect it afterwards). This lesson will show you Cypress's own approach so you can compare the two with confidence, which is exactly the "cross-tool perspective" the week is aiming for.

---

## The Concept

### 1. A quick map of the Cypress Test Runner

When you start Cypress in interactive mode with:

```bash
npx cypress open
```

you choose **E2E Testing**, pick a browser (Chrome, Edge, Firefox, Electron, or WebKit if you have enabled the experimental support), and then click a spec file. Cypress opens a browser window that contains the **Test Runner**. Understanding its layout is the foundation of everything else in this lesson.

The window is split into regions:

1. **The spec/test side panel (left).** It shows the test you are running, the suites (`describe` blocks) and tests (`it` blocks), their pass/fail status, and, below each test, the **Command Log**.
2. **The Command Log.** A vertical list of everything Cypress did: each `cy.*` command, each assertion, each network request that was stubbed or spied on, each `cy.log()` message. Each entry has a number, a name (such as `visit`, `get`, `click`, `assert`) and a message (such as the selector or URL).
3. **The app preview (right).** The application under test is rendered inside an `iframe` in this area. This is a *live* application while commands run, and a *frozen reconstruction* of earlier moments when you hover over or pin commands.
4. **The header bar above the preview.** It shows the current URL, the viewport size (width x height), and tools: the **Selector Playground** (a crosshair or target icon), and in newer versions a **Studio** button, which we will meet in the "Recording user actions" lesson.
5. **The browser DevTools** (F12 or right-click then Inspect). Because the Test Runner is just a web page running in a real browser, you have the entire DevTools available: Elements, Console, Network, Sources and so on.

> Analogy: imagine a cooking show. The Command Log is the recipe being read out step by step. The app preview is the kitchen camera. Time-travel debugging is like having a DVR: you can click on any recipe step and the camera shows you what the kitchen looked like at that exact moment.

### 2. The Command Log, in detail

Every Cypress command that runs adds a row to the Command Log. Consider this test (we will use the public Sauce Demo practice site, which has stable `data-test` attributes):

```js
it('logs in with a valid user', () => {
  cy.visit('https://www.saucedemo.com');
  cy.get('[data-test="username"]').type('standard_user');
  cy.get('[data-test="password"]').type('secret_sauce');
  cy.get('[data-test="login-button"]').click();
  cy.url().should('include', '/inventory.html');
});
```

In the Command Log you will see, roughly:

| # | Command | Message |
|---|---------|---------|
| 1 | visit | https://www.saucedemo.com |
| 2 | get | [data-test="username"] |
| 3 | type | standard_user |
| 4 | get | [data-test="password"] |
| 5 | type | secret_sauce |
| 6 | get | [data-test="login-button"] |
| 7 | click | |
| 8 | url | |
| 9 | assert | expected https://www.saucedemo.com/inventory.html to include /inventory.html |

Things worth noticing:

- **Commands and assertions are separate rows.** `.should()` creates an `assert` row with a human-readable sentence. When an assertion fails, the sentence tells you the *expected* and *actual* values. Read it carefully, because it is often the whole diagnosis.
- **Child commands are indented or grouped under their parents** in many cases. `type` acts on the element yielded by `get`.
- **Status icons** show whether each step passed (green), is pending/running (spinner), or failed (red). A failed step stops the test (unless it is inside a retry situation, see below).
- **Retries are invisible by default but meaningful.** If an assertion does not immediately pass, Cypress keeps re-querying and re-asserting until the `defaultCommandTimeout` (4000 ms by default) expires. The Command Log shows the *final* outcome of that retry loop as a single row. This is why you rarely need `cy.wait(1000)` in Cypress.
- **Aliased network calls** (`cy.intercept(...).as('login')`) appear as rows too, labelled with the alias, so you can verify that a request really happened and what it returned.

You can also *filter mentally*: sort of "which rows are my actions, which are my checks, which are the app's network traffic?" With practice, you will read the Command Log like a story.

### 3. Snapshots: the secret behind time travel

How does Cypress show you the page "as it was" at step 4 when the test is already at step 9? The answer is **snapshots**.

A **snapshot** is a saved copy of the page's DOM (the document structure) and its styles, captured by Cypress around the time a command runs. Specifically:

- For **action commands** (`click`, `type`, `check`, `select`, `dblclick`, and so on), Cypress takes **two** snapshots: **Before** (just before the action) and **After** (just after).
- For **query/assertion commands** (`get`, `contains`, `should`), Cypress typically takes a single snapshot.

Important facts that beginners often get wrong:

1. **A snapshot is a static copy, not the live page.** It is like a photograph of the page, rebuilt from the saved DOM and CSS. JavaScript is *not* running inside a snapshot, so you cannot interact with it (for example, a dropdown will not open when you click it in a snapshot). It is for *looking*, not for *using*.
2. **Snapshots are kept in memory** while the Test Runner is open. The configuration option `numTestsKeptInMemory` controls how many tests' worth of snapshots are retained (default `50` in `cypress open`; in `cypress run` it is `0`, meaning snapshots are not retained for finished tests, because nobody is sitting there to hover over them). Reducing this number lowers memory use on big spec files; raising it is rarely needed.
3. **Things the DOM cannot capture are not in the snapshot.** The content of a `<canvas>` bitmap, the state of a video, an in-progress CSS animation frame, or JavaScript variables are not faithfully "rewound". If a bug lives in one of these, use screenshots/video (next lesson) or the console.
4. **Snapshots are taken at the moment of the command**, which means they show you *what the page looked like when Cypress acted*, not what the page looked like a few hundred milliseconds later. That is precisely what you want when asking, "Was the button already visible when we clicked?"

### 4. Time travel by hovering

The simplest time-travel move: **move your mouse over a row in the Command Log**. The app preview immediately re-renders to show the snapshot for that command. Move down the list and you watch the page change step by step, like scrubbing through a video timeline. Move your mouse away and the preview returns to the final (current) state.

What you can learn by hovering:

- After `type` into the password field, is the field actually filled? (Passwords show as dots.)
- After `click` on the login button, did an error banner appear ("Epic sadface: ...")?
- For a `get` row: **which element did the selector match?** Cypress *highlights* the matched elements on the snapshot. If your selector matched three elements instead of one, you see three highlights immediately.
- For a `click` row: Cypress overlays a **hitbox**, a small coloured dot at the exact coordinates where it clicked. If the dot sits on an element that is not the one you intended (for example, a cookie banner covering the button), you have found your bug.

### 5. Pinning: freezing a moment

Hovering is temporary. If you want to *keep* a snapshot on screen so you can study it, **click the row** in the Command Log. That is called **pinning**.

When a command is pinned:

- The row stays highlighted and the app preview stays frozen on that snapshot even when you move the mouse away (a "pinned" indicator appears in the preview).
- For action commands, **Before** and **After** buttons or tabs appear so you can flip between the two snapshots. This answers the question, "What changed because of this click?" in one glance.
- Cypress prints details about the command to the **browser DevTools Console**. Open the Console (F12) and you will see structured output such as the command name, the **Elements** it acted on (clickable and inspectable), the **Selector**, and what it **Yielded**. For a `request` or `intercept`-related row you may also see the full request/response data. For a failed assertion you can see the actual and expected values.
- You can then **right-click and inspect the elements in the frozen snapshot** using the browser's Elements panel. Because the snapshot is real DOM, you can check classes, attributes, computed styles and sizes, which helps a lot when you are wondering "why does `cy.get('.btn')` find two things?".

To un-pin, click the same row again, click the "Unpin" control, or click another row.

### 6. Reading a failure

When a test fails, Cypress does several helpful things at once:

1. The test is marked red and the **failing command row is red**.
2. An **error card** appears under the failing command with the error name, the message and a **code frame** that points to the exact line in your spec file. In recent versions the file path is clickable and opens in your editor if configured.
3. The **Before/After snapshots** of the failing step are available to hover or pin. Because the failing step is the last thing that happened, its snapshot shows what Cypress saw when it gave up.
4. The Console receives the error stack as well when you click the row.

Typical failure messages and what they usually mean:

| Message (shortened) | Usual meaning | First thing to check |
|---|---|---|
| `Timed out retrying after 4000ms: Expected to find element: '.x', but never found it.` | The selector never matched in time. | Hover on the previous step: is the page in the state you expect? Is the selector right (use Selector Playground)? |
| `... is being covered by another element: <div class="modal">` | Cypress refuses to click through an overlay. | Pin the click and inspect the hitbox and the covering element. |
| `... is not visible because its CSS property: display is none` | Element exists but is hidden. | Did a previous step (menu open, tab switch) fail to happen? |
| `Timed out retrying: expected '<h1>' to have text 'X', but the text was 'Y'` | The assertion's actual value differs. | The message shows both values; compare to the snapshot. |
| `cy.visit() failed trying to load: ...` | The server is down or the URL is wrong. | Check `baseUrl` and the server. |
| `The following error originated from your application code, not from Cypress.` | The app threw an uncaught exception. | See the console; decide whether to fix the app or handle with `Cypress.on('uncaught:exception', ...)` carefully. |

### 7. Selector Playground

The **Selector Playground** is a small tool inside the Test Runner (the crosshair icon in the preview header). When active, hovering over elements in the preview highlights them and shows the selector Cypress would suggest, ordered by a configurable priority (by default `data-cy`, `data-test`, `data-testid`, `id`, `class`, `tag`, `attributes`, `nth-child`). Clicking an element prints the suggested `cy.get(...)` (or `cy.contains(...)`) expression and lets you copy it. You can also type your own selector into the Playground field and see how many elements match ("1 of 1" is what you want).

This is a debugging tool, not just a locator-creation tool: if a `get` step fails, open the Playground, paste the selector, and see whether it matches anything on the live page.

### 8. Pausing and stepping: `.debug()` and `cy.pause()` (a recap with more depth)

On Thursday you saw these two. Here is how they fit into time-travel debugging:

- `cy.pause()` stops the test at that point. The Command Log shows **Resume** and **Next** controls. **Next** executes one command at a time. After each step you can hover back over previous rows, pin them, and inspect the live app. This is "step debugging" for Cypress commands.
- `.debug()` is chained to a command, for example `cy.get('.item').debug()`. It logs the subject (the yielded element(s)) to the DevTools console and, **if DevTools is open**, triggers a JavaScript `debugger` statement so the browser pauses. The yielded subject is exposed to you in the console (look for the `subject` variable in the log output).

Use `cy.pause()` when you want to look at the *application*; use `.debug()` when you want to look at a *specific value*.

### 9. Run modes: where time-travel works and where it does not

| Mode | Command | Time travel? |
|------|---------|--------------|
| Open (interactive) | `npx cypress open` | Yes. Full Command Log, hover, pin, Selector Playground. |
| Headed run | `npx cypress run --headed --no-exit` | You see the browser, and the runner stays open at the end so you can look. Snapshot behaviour is limited in run mode because `numTestsKeptInMemory` defaults to `0`. |
| Headless run (CI) | `npx cypress run` | No interactive time travel. You rely on terminal output, failure screenshots, optional video, and (if you record to Cypress Cloud) **Test Replay**. |

The practical consequence: **reproduce locally in `cypress open`** whenever possible. It is by far the most pleasant place to debug.

### 10. Is there a Cypress "trace"?

This is a very common point of confusion for people coming from Playwright.

In Playwright, a **trace** is a *file* (`trace.zip`) that records the whole run: actions, DOM snapshots before/after each action, network requests, console messages and source code. You can generate it in CI, download it as an artifact, and open it later on any machine with `npx playwright show-trace trace.zip` (or in the hosted viewer at trace.playwright.dev). This is the **Playwright Trace Viewer**.

**Cypress has no equivalent open-source `trace.zip` file.** Cypress's open-source time-travel is a *live* feature of the interactive Test Runner. The snapshots live in the browser's memory during your session.

What Cypress offers instead, depending on the situation:

1. **Interactive time travel** in `cypress open` (everything described above), free and local.
2. **Screenshots on failure and optional video** in `cypress run` (next lesson). These are artifacts you can download from CI, but they are pictures, not interactive.
3. **Cypress Cloud Test Replay.** When you record your CI runs to Cypress Cloud (`cypress run --record`), Test Replay captures the test run, including commands, network requests, console logs, JavaScript errors and the rendered DOM/CSS, and lets you open an interactive replay in the browser with a Command Log and DevTools-like panels, *as if you had been running it locally*. Version and environment notes (please check the current docs because this is a commercial, evolving feature):
   - Requires recording the run with **Cypress 13 or later**.
   - Requires a **Chromium-based browser** (Chrome, Edge, or Electron). Firefox and WebKit recordings are not supported.
   - It is a Cypress Cloud feature (included in Cloud plans, subject to usage limits), not part of the free open-source runner.
   - It does not capture everything (for example, cookies/localStorage and some traffic types are not in the replay), and the docs recommend you disable video when Test Replay is on to reduce overhead.
4. **Custom `Cypress.log()` entries with snapshots** (we cover this in the Logging lesson) that let *your own* custom commands participate in time travel.

### 11. Cypress time-travel vs Playwright Trace Viewer

| Aspect | Cypress Test Runner (open source) | Cypress Cloud Test Replay | Playwright Trace Viewer |
|---|---|---|---|
| What it is | Live UI during `cypress open` | Hosted replay of a recorded CI run | Offline viewer for a `trace.zip` file |
| Needs a file artifact? | No (in-memory snapshots) | No (uploaded to the Cloud) | Yes, `trace.zip` |
| Works for CI failures? | Only if you reproduce locally | Yes | Yes (download artifact, open locally) |
| Cost | Free | Part of Cloud plans | Free |
| DOM snapshots | Before/After for actions | Yes (rendered DOM, CSS) | Before/Action/After per action |
| Network and console | Via DevTools / pinned log | Built into the replay UI | Built-in Network and Console tabs |
| Source code view | Code frame on errors | Yes | Source tab |
| How to enable | Nothing, it is on in `open` | `cypress run --record` with Cloud | `trace: 'on-first-retry'` (or `'on'`) in `playwright.config`, or `--trace on` |
| Typical use | Developing and debugging locally | Investigating flaky CI failures | Investigating CI failures with zero vendor dependency |

How to choose: if you are *writing* tests, the Cypress runner's time travel is arguably the most immediate feedback loop of any tool. If you are *triaging CI failures* and you do not use Cypress Cloud, Cypress gives you only screenshots and video, while Playwright's trace would give you more. That is a real, honest trade-off to mention when you write the comparison note for your Project 1 retrospective.

---

## Code Examples

### Example 1: A spec designed for debugging practice

Create `cypress/e2e/debugging-demo.cy.js`:

```js
describe('Time-travel debugging demo', () => {
  beforeEach(() => {
    cy.visit('https://www.saucedemo.com');
  });

  it('logs in and adds an item to the cart', () => {
    cy.get('[data-test="username"]').type('standard_user');
    cy.get('[data-test="password"]').type('secret_sauce');
    cy.get('[data-test="login-button"]').click();

    cy.url().should('include', '/inventory.html');

    cy.get('[data-test="inventory-item"]').should('have.length', 6);

    cy.get('[data-test="add-to-cart-sauce-labs-backpack"]').click();

    cy.get('[data-test="shopping-cart-badge"]')
      .should('be.visible')
      .and('have.text', '1');
  });
});
```

**Line-by-line explanation**

1. `describe('Time-travel debugging demo', () => { ... })` groups tests. `describe` is Mocha's suite function, which Cypress bundles. The string is the suite name displayed in the runner.
2. `beforeEach(() => { cy.visit(...) })` is a Mocha hook that runs before every `it`. Visiting in `beforeEach` gives each test a fresh start, which matches Cypress's default *test isolation* (browser state such as cookies and local storage is cleared between tests in Cypress 12 and later).
3. `cy.visit('https://www.saucedemo.com')` loads the page. In the Command Log this is a `visit` row. Hover over it later to see the login page as it was first loaded.
4. `it('logs in and adds an item to the cart', () => { ... })` defines one test.
5. `cy.get('[data-test="username"]')` queries the DOM for an element with a `data-test` attribute equal to `username`. `cy.get` retries until it finds it or times out. Hover on its row and you will see the username input highlighted in the snapshot.
6. `.type('standard_user')` types characters into the yielded element. Because `type` is an action, it has Before and After snapshots: Before shows an empty field, After shows the typed text.
7. The next two lines do the same for the password field. Notice how the After snapshot shows dots, not letters.
8. `.click()` clicks the login button. Pin this row and look at the **hitbox** to see exactly where the click occurred.
9. `cy.url().should('include', '/inventory.html')` reads the current URL and asserts it contains the inventory path. This produces an `url` row and an `assert` row. If login failed, this is the row that goes red, and its message would show the actual URL.
10. `cy.get('[data-test="inventory-item"]').should('have.length', 6)` asserts there are exactly 6 products on the page. When it passes, hover on the `get` row: six elements are highlighted at once.
11. `cy.get('[data-test="add-to-cart-sauce-labs-backpack"]').click()` adds the backpack. The After snapshot shows the button text change to "Remove".
12. The final chain gets the cart badge and chains two assertions with `.should('be.visible').and('have.text', '1')`. `.and()` is an alias of `.should()` and reads better for the second assertion. Both create `assert` rows.

**How to use it for debugging practice:** change `'have.length', 6` to `'have.length', 5`. Run the spec in `cypress open`. The test fails. Practise reading the message (`expected [ <div.inventory_item> x 6 ] to have a length of 5 but got 6`), hover the failed row to see the six highlighted products, and pin it to inspect them in DevTools.

### Example 2: Using `.debug()` and `cy.pause()`

```js
it('inspects the product list', () => {
  cy.get('[data-test="username"]').type('standard_user');
  cy.get('[data-test="password"]').type('secret_sauce');
  cy.get('[data-test="login-button"]').click();

  cy.get('[data-test="inventory-item"]').debug();

  cy.pause();

  cy.get('[data-test="inventory-item-name"]')
    .first()
    .should('contain.text', 'Backpack');
});
```

**Line-by-line explanation**

1. The first three lines log in, exactly as before.
2. `cy.get('[data-test="inventory-item"]').debug();` fetches the product cards and then calls `.debug()`. If your DevTools is open, the browser stops on a `debugger` line; you can type `subject` in the Console to inspect the yielded jQuery object. Cypress also prints the subject in the Console output. `.debug()` does **not** change the subject: the chain continues with the same elements.
3. `cy.pause();` halts the test. In the Command Log header you will see **Resume** and **Next** buttons. Click **Next** to run only the next command. After each step you can hover or pin earlier rows. Remove `cy.pause()` before committing code. It is meant for interactive sessions; leaving it in shared code is sloppy and can confuse teammates and CI runs, so treat it like a leftover `debugger` statement.
4. `cy.get('[data-test="inventory-item-name"]').first().should('contain.text', 'Backpack')` finds all product names, takes the first, and asserts its text contains "Backpack". `.first()` narrows many elements to one.

### Example 3: Making a custom command appear properly in the log (with snapshots)

Cypress lets *your* custom commands create log rows that participate in time travel. We will explore `Cypress.log` in depth in the Logging lesson; here is the debugging-relevant part.

In `cypress/support/commands.js`:

```js
Cypress.Commands.add('login', (username, password) => {
  const log = Cypress.log({
    name: 'login',
    displayName: 'LOGIN',
    message: `${username} / ${'*'.repeat(password.length)}`,
    autoEnd: false,
    consoleProps: () => ({ username, passwordLength: password.length }),
  });

  log.snapshot('before');

  cy.get('[data-test="username"]', { log: false }).type(username, { log: false });
  cy.get('[data-test="password"]', { log: false }).type(password, { log: false });
  cy.get('[data-test="login-button"]', { log: false }).click({ log: false });

  cy.then(() => {
    log.snapshot('after').end();
  });
});
```

**Line-by-line explanation**

1. `Cypress.Commands.add('login', (username, password) => { ... })` registers a new command, `cy.login(...)`, that you can call from any spec.
2. `Cypress.log({...})` creates one row in the Command Log. `name` is the internal name, `displayName` is the label shown in the log, and `message` is the text next to it. We deliberately show the password as asterisks (`'*'.repeat(...)`) so secrets never appear in the log.
3. `autoEnd: false` tells Cypress that *we* will end this log row ourselves (needed because the work inside is asynchronous).
4. `consoleProps` is a function that returns an object. When you pin this row, those properties print to the DevTools Console. We expose the username and the *length* of the password, never the password.
5. `log.snapshot('before')` captures a named snapshot. When you pin the `LOGIN` row, "before" appears as a tab.
6. The three `cy.get(...).type/click(...)` lines perform the actual login. We pass `{ log: false }` to each so they do not add their own noisy rows, leaving a single clean `LOGIN` row. (Trade-off: if something fails inside, you lose the fine-grained rows. Use `log: false` only for stable, well-tested helpers.)
7. `cy.then(() => { log.snapshot('after').end(); })` runs *after* the preceding commands are done (Cypress commands are queued, so a plain statement placed here would run too early). It captures the "after" snapshot and ends the log row as passed.

### Example 4: Configuration that influences debugging

In `cypress.config.js`:

```js
const { defineConfig } = require('cypress');

module.exports = defineConfig({
  e2e: {
    baseUrl: 'https://www.saucedemo.com',
    defaultCommandTimeout: 6000,
    numTestsKeptInMemory: 20,
    video: false,
    screenshotOnRunFailure: true,
    retries: { runMode: 1, openMode: 0 },
  },
});
```

**Explanation**

1. `defineConfig` is a helper that gives editors autocompletion and validation. We `require` it because this is a CommonJS config file.
2. `baseUrl` lets you write `cy.visit('/')`. It also tells Cypress which origin your tests are expected to run on.
3. `defaultCommandTimeout: 6000` raises the retry window for most commands from 4 seconds to 6. Do this only when your app is genuinely slow; do not use it to hide flakiness.
4. `numTestsKeptInMemory: 20` limits how many tests' snapshots are held in memory in open mode. Lower it if a spec with hundreds of tests slows the browser.
5. `video: false` and `screenshotOnRunFailure: true` are covered in the next lesson.
6. `retries: { runMode: 1, openMode: 0 }` retries failing tests once in `cypress run` and never in `cypress open`. In open mode, you want to see the failure immediately. In the Command Log, retried attempts are listed so you can compare attempt 1 and attempt 2.

### Example 5: Running with Test Replay (conceptual commands)

```bash
# Locally: interactive time travel
npx cypress open

# CI: record to Cypress Cloud so Test Replay is available for failures
npx cypress run --record --key <your-record-key> --browser chrome
```

**Explanation**

- `--record` uploads the run to Cypress Cloud. `--key` is the secret record key from your Cloud project (store it as a CI secret, never in the repository; it can also be supplied via the `CYPRESS_RECORD_KEY` environment variable).
- `--browser chrome` is important: Test Replay needs a Chromium-based browser.
- The project's `projectId` is set in the Cypress config after you connect the project to Cypress Cloud.

---

## Real-World Scenarios

### Scenario 1: "The click does nothing"

A teammate's test clicks "Checkout" and then asserts the URL, but the assertion fails. They add three `cy.wait(2000)` calls and it still fails. You open the test in `cypress open`, pin the `click` row and look at the After snapshot: nothing changed. The hitbox shows the click landed on a cookie-consent banner that overlays the bottom of the page. The fix is not a wait: it is to dismiss the banner in the test (or set the consent cookie in `beforeEach`). Time travel found the answer in ten seconds.

### Scenario 2: "It passes locally, fails in CI"

A test passes in `cypress open` and fails in `cypress run` on the CI server. Without any replay artifact, you start with the **failure screenshot** (next lesson) and the terminal error message. You notice the viewport in CI differs: the screenshot shows the mobile menu instead of the desktop navigation. The root cause is that the default `cypress run` viewport is 1000x660, while your local spec ran with a wider window. You fix it by setting `viewportWidth` and `viewportHeight` in the config. If the team used Test Replay, you could have opened the replay directly and seen the layout without guessing.

### Scenario 3: Flaky assertion on a list

`cy.get('.results li').should('have.length', 10)` sometimes fails with "got 3". Hover on the failed `assert` row: the snapshot shows the list *still loading*, with a spinner. The assertion retried for 4 seconds but the API took longer. You add `cy.intercept('GET', '/api/results*').as('results')` and `cy.wait('@results')` before the assertion, so the test waits for the real event (the response) rather than an arbitrary time. The Command Log shows the aliased request as a row so you can verify the alias works.

---

## Common Pitfalls and Best Practices

1. **Treating a snapshot as the live app.** You cannot click things inside a snapshot. If you need to interact with the real page, use `cy.pause()` and work with the live preview.
2. **Debugging in `cypress run` when you could reproduce in `cypress open`.** Always try to reproduce interactively first; it is faster.
3. **Leaving `cy.pause()` and `.debug()` in committed code.** Add a lint rule or a code-review checklist item.
4. **Ignoring the assertion message.** Cypress writes very readable messages; read the expected/actual values before touching the code.
5. **Hiding too much with `{ log: false }`.** It makes tests tidy but removes debugging evidence. Use it for helper commands that are already proven, and keep default logging in the main test body.
6. **Assuming memory is unlimited.** With very large specs, lower `numTestsKeptInMemory` or split the spec.
7. **Assuming Test Replay works everywhere.** It needs Cypress 13+, a Chromium-based browser, recording to Cypress Cloud and a plan that includes it. Always verify against the current documentation.
8. **Over-relying on `cy.wait(ms)`.** Time travel often reveals what the page was actually waiting for; wait for *that* (an alias, a visible element, a URL) instead.
9. **Forgetting that DOM snapshots are not pixel-perfect.** If you suspect a visual issue (overlap, wrong colour), take a real screenshot (next lesson) or use visual testing (later today).
10. **Not documenting the debugging finding.** When you fix a flaky test, write one sentence in the PR explaining the root cause. Your future self (and your Project 1 reviewers) will appreciate it.

---

## Mini Practice Exercises

### Exercise 1: Find the covered click

1. In `cypress open`, run the Example 1 spec.
2. Pin the `click` row of the login button and switch between Before and After.
3. Write down: what is the URL in the Before snapshot? In the After snapshot?

*Hint:* the URL appears in the preview header, and it changes as the snapshot changes.

*Solution:* Before shows `https://www.saucedemo.com/` (the login page). After typically shows the inventory page (`.../inventory.html`) because the click triggers navigation; if timing makes the After snapshot still show the login page, hover the later `url` assertion row to see the settled state. The exact moment of capture can vary, which is itself a useful lesson about snapshots.

### Exercise 2: Break it on purpose

1. Change one `data-test` selector to a wrong value, for example `[data-test="user-name"]`.
2. Run the test and read the error.
3. Open the Selector Playground, click the real username field, and copy the suggested selector.
4. Fix the test.

*Hint:* the error will say `Expected to find element: [data-test="user-name"], but never found it.` The Playground suggests `[data-test="username"]`.

### Exercise 3: Build a debuggable command

Create a `cy.addToCart(productSlug)` command that uses `Cypress.log` with a `message` showing the slug, a `consoleProps` function with the selector used, and a `before`/`after` snapshot. Use it in a test and pin its row.

*Solution sketch:*

```js
Cypress.Commands.add('addToCart', (slug) => {
  const selector = `[data-test="add-to-cart-${slug}"]`;
  const log = Cypress.log({
    name: 'addToCart',
    message: slug,
    autoEnd: false,
    consoleProps: () => ({ slug, selector }),
  });
  log.snapshot('before');
  cy.get(selector, { log: false }).click({ log: false });
  cy.then(() => log.snapshot('after').end());
});
```

### Exercise 4: Compare tools (written reflection)

In 5-8 sentences, answer: "If a Cypress test fails only in CI and my team has no Cypress Cloud subscription, what evidence will I have, and how would that differ with a Playwright test using `trace: 'on-first-retry'`?"

*Hint:* think about screenshots, video, terminal output, and what a downloadable artifact allows.

---

## Summary / Key Takeaways

- The Cypress Test Runner shows a **Command Log** of every command, assertion and (aliased) network request, next to a live **app preview**.
- **Snapshots** are saved DOM and CSS copies captured around each command; actions get **Before** and **After** snapshots.
- **Hover** to time-travel; **click to pin**. Pinned rows print detailed output to the DevTools Console and let you inspect the frozen DOM.
- Read failures carefully: the failing row, the assertion sentence, the code frame and the snapshot together nearly always tell you why.
- Use the **Selector Playground**, `.debug()` and `cy.pause()` alongside time travel.
- Open-source Cypress has **no `trace.zip`**. Interactive time travel works in `cypress open`; for CI, you have screenshots, video and (with Cypress Cloud, Cypress 13+, Chromium browsers) **Test Replay**.
- The **Playwright Trace Viewer** is file-based and portable; Cypress's time travel is live and in-memory. Each has a role, and knowing the difference is part of being a cross-tool quality engineer.
- Always reproduce locally in `cypress open` first, and avoid fixing failures with arbitrary waits.

---

## External Resources

- Cypress documentation, Debugging guide: https://docs.cypress.io/app/guides/debugging
- Cypress documentation, Test Replay (Cypress Cloud): https://docs.cypress.io/cloud/features/test-replay
- Playwright documentation, Trace Viewer (for the comparison): https://playwright.dev/docs/trace-viewer
