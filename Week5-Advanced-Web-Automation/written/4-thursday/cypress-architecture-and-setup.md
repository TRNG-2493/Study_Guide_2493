# Cypress Architecture and Setup

## Learning Objectives

By the end of this lesson you will be able to:

- Explain what Cypress is, who builds it, and what kinds of testing it supports (end-to-end and component testing).
- Describe, in your own words, how Cypress is architecturally different from Playwright, which you used Monday through Wednesday.
- Explain why Cypress commands are *queued and asynchronous* even though they look like ordinary synchronous lines of code, and why you cannot use `async/await` with them the way you did in other tools.
- Install Cypress in a new Node.js project, open it for the first time, and run a first spec from both the interactive Test Runner and the command line.
- Read and modify `cypress.config.js`, and explain the purpose of `baseUrl`, `specPattern`, `supportFile`, `fixturesFolder`, `viewportWidth`, `viewportHeight`, `defaultCommandTimeout`, `retries`, and `setupNodeEvents`.
- Navigate the default Cypress folder structure (`cypress/e2e`, `cypress/fixtures`, `cypress/support`) and explain what belongs in each folder.
- List Cypress's main limitations (single-origin tab model, JavaScript/TypeScript only, no multi-tab) and the workarounds provided (`cy.origin`, `cy.task`).

---

## Why This Matters

This week's epic is to master complex UI interactions in Playwright, structure tests with fixtures, hooks and the Page Object Model, and then learn **Cypress for cross-tool perspective** and visual testing. Thursday is the day where the "cross-tool perspective" begins.

Why would a professional test automation engineer learn two tools that appear to do the same job? There are three honest reasons.

1. **Teams use different tools.** Many front-end-heavy product teams, especially those whose developers write React, Vue, or Angular all day, already use Cypress. When you join such a team, "we use Cypress" is a very common answer. If the only thing you can say is "I only know Playwright," you have narrowed your options.
2. **Comparing tools makes you a better engineer.** Once you can say *why* a tool behaves as it does, you stop memorising commands and start understanding testing itself: waiting, retries, selectors, isolation, reporting. Those ideas are portable.
3. **Project 1 (QE Foundations) benefits.** In Project 1 you are building a UI test suite. Today's exercise asks you to port three of your Project 1 tests to Cypress and write a comparison note. That comparison note is a genuine professional deliverable: engineering managers regularly ask, "Which tool should we use for this project and why?" and you will have first-hand evidence.

### Quick contrast with Playwright

| Aspect | Playwright (Mon-Wed) | Cypress (today) |
|---|---|---|
| Where your test code runs | In a separate Node/Python process; it *remotely controls* the browser | Inside the browser itself, in the same run loop as the application |
| Language | Python, JavaScript/TypeScript, Java, .NET | JavaScript and TypeScript only |
| Browsers | Chromium, Firefox, WebKit (bundled, all first-class) | Chrome-family, Edge, Firefox, Electron; WebKit is experimental |
| Multi-tab / multi-window | Supported (`context.pages`, `expect_page`) | Not supported (single tab); workaround: remove `target="_blank"` or test the URL |
| Test runner | Playwright Test or pytest plugin | Built-in Mocha-based runner with a rich GUI |
| Auto-waiting | Auto-waits for actionability before actions | Retries queries and assertions, plus actionability checks before actions |
| Async model | `await page.click(...)` (Python: sync API or `await` in async API) | No `await`; commands are enqueued and run later |
| Debugging | Trace viewer, inspector, codegen | Interactive runner, time-travel snapshots (deep dive on Friday) |

Do not worry if some rows are unfamiliar. By the end of this lesson, and the other eight lessons today, each row will make sense.

---

## The Concept

### 1. What is Cypress?

**Cypress** is an open-source (the test runner is MIT licensed) front-end testing tool built for the modern web. It is maintained by Cypress.io and was first released in 2017. It lets you write tests in JavaScript or TypeScript that:

- Visit pages and click, type, select, and otherwise interact with them.
- Make assertions about what the page shows.
- Spy on, stub, and control network requests (`cy.intercept`).
- Run in a real browser while you *watch* the test execute.

Cypress supports two kinds of testing:

1. **End-to-end (E2E) testing** - the app runs as a user would see it, and Cypress drives it through a browser. This is what we focus on this week, and it is what Playwright's page-based tests were doing.
2. **Component testing** - individual UI components (for example, a React `<Button />`) are mounted in isolation and tested in a real browser. This is a Cypress strength but is outside our scope today.

Cypress also has a paid cloud product (Cypress Cloud, formerly Cypress Dashboard) for recording runs, parallelisation, and analytics. You do **not** need it for anything this week.

### 2. The architecture: how Cypress is different

Here is the single most important idea of this lesson.

> **Playwright runs *outside* the browser and sends commands to it. Cypress runs *inside* the browser, next to your application.**

Think about a puppet show. In Playwright, a puppeteer stands outside the stage, pulling strings (a network protocol) to make the puppet move. In Cypress, the puppeteer is *on the stage*, standing beside the puppet and moving it directly. The second arrangement is faster and gives very detailed visibility into what the puppet is doing, but the puppeteer can only work on one stage at a time.

#### 2.1 The two halves of Cypress

Cypress has two cooperating parts:

1. **A Node.js process (the "backend" or "server" side).** It starts when you run `cypress open` or `cypress run`. It reads your configuration, starts a proxy server, launches the browser, manages files (screenshots, videos, fixtures, downloads), and can do anything Node can do: read the file system, query a database, call external services. Your test code cannot call these directly, because it is not running in Node. Instead you ask the Node process to do work using `cy.task()`, `cy.readFile()`, `cy.writeFile()`, and `cy.exec()`.
2. **The browser side (the "Test Runner").** Cypress opens a browser page containing the Cypress runner UI. Inside that page are two important iframes: one that contains **your spec code** and one that loads **your application under test (AUT)**. Because your spec code and your application run in the same browser, on the same event loop and under the same origin (Cypress works to make that so), your test code can reach directly into the application. For instance `cy.window()` gives you the real `window` object of the app, and `cy.stub(win, 'alert')` can replace a real browser function.

Between them sits a **proxy**. All HTTP(S) traffic from the browser passes through Cypress's proxy, which is how Cypress can modify responses, inject its helper scripts, and implement `cy.intercept()` for network spying and stubbing.

Simplified diagram:

```
 +-------------------------+          +--------------------------------------+
 |  Node.js process        |          |  Browser (Chrome / Edge / Firefox /  |
 |  (Cypress "server")     |          |  Electron)                           |
 |                         |          |                                      |
 |  - reads cypress.config |          |  +---------------+  +--------------+ |
 |  - runs plugins/tasks   |<-------->|  | Spec iframe   |  | App under    | |
 |  - proxy server  -------+----------+->| (your tests,  |  | test iframe  | |
 |  - file system access   | WebSocket|  |  Mocha+Chai)  |  | (your site)  | |
 |  - screenshots, video   |  + HTTP  |  +---------------+  +--------------+ |
 +-------------------------+          +--------------------------------------+
```

Do not memorise the diagram; understand the consequence.

#### 2.2 Consequences of running in the browser

**Benefits**

- *Speed and consistency.* There is no network round trip between your test and the browser for each command, so Cypress tests tend to feel snappy and deterministic.
- *Deep visibility.* Because Cypress is in the page, it can take a DOM snapshot before and after every command. You can hover over a command in the Command Log and see exactly what the page looked like at that moment. This is the foundation of "time-travel debugging", which is covered in depth on Friday.
- *Direct access to the app.* You can read `window.localStorage`, call application functions through `cy.window()`, stub `fetch`, and so on.
- *Automatic reloading.* In `cypress open`, saving a spec file re-runs it instantly.

**Limitations**

- *One tab, one browser window.* Because the test runs inside the browser tab it controls, Cypress cannot drive a second tab or window. If you recall Tuesday's lesson on multiple tabs and windows in Playwright (`context.expect_page()`), there is no direct equivalent in Cypress. Common workarounds: remove the `target` attribute (`cy.get('a').invoke('removeAttr', 'target').click()`) so the link opens in the same tab, or read the `href` and `cy.visit()` it.
- *Same-origin restrictions, relaxed by `cy.origin`.* Browsers enforce a "same-origin policy". Historically, Cypress could not visit two different superdomains in a single test. Since Cypress 12, the **`cy.origin()`** command allows you to run a block of commands against a second origin (for example, a login page on an identity provider) within the same test.
- *JavaScript and TypeScript only.* You cannot write Cypress tests in Python or Java. This is a real difference from Playwright, which is why today's code is JavaScript, and why your Playwright examples earlier this week used Python.
- *Browser coverage.* Cypress supports Chrome, Chromium, Edge, Firefox, and Electron. WebKit (Safari engine) support exists in an experimental form. We cover this in the next lesson (Browser management).
- *Not a general-purpose browser driver.* You cannot use Cypress to automate arbitrary non-test tasks across the web as you might with a scripting library; it is designed for testing your own applications.

### 3. Commands are queued, not executed immediately

This is the concept that surprises almost every beginner, so we will go slowly.

Look at this snippet:

```js
cy.visit('https://www.saucedemo.com');
cy.get('#user-name').type('standard_user');
cy.get('#password').type('secret_sauce');
cy.get('#login-button').click();
```

It reads like four ordinary statements executed in order. But what actually happens in JavaScript is quite different:

1. Mocha runs your `it()` callback.
2. As the callback executes, each `cy.*` call does **not** perform its action. Instead, it adds a *command* to an internal **queue** and returns immediately.
3. After the callback finishes (all four commands are queued), Cypress begins executing the queue **one command at a time**, waiting for each to finish (or retry, or time out) before starting the next.

So the *JavaScript* runs synchronously and fast (it just queues commands), while the *Cypress commands* run later, asynchronously.

#### 3.1 Why this matters: no `async/await`

Because `cy.get()` returns a *Chainable* (a queue-aware object that looks like a promise but is not one), the following common pattern **does not work as you might expect**:

```js
// WRONG: this does not do what it looks like
const button = cy.get('#login-button');   // button is NOT the DOM element
button.click();                           // may still work, but patterns like the next line do not

const text = cy.get('.title').text();     // ERROR: there is no .text() method
```

and neither does this:

```js
// WRONG: do not use async/await with Cypress commands
it('logs in', async () => {
  const el = await cy.get('#login-button'); // Cypress commands are not real Promises
});
```

Compare with Playwright (Python sync API), where you might write:

```python
title = page.locator(".title").inner_text()   # runs immediately and returns a string
```

In Cypress, you access a value with `.then()` (or an assertion), because the value will only exist *when the command runs*:

```js
cy.get('.title').then(($el) => {
  const text = $el.text();       // $el is a jQuery-wrapped element; now we can use it
  cy.log(`Title was: ${text}`);
});
```

Think of it like ordering at a restaurant: you give the waiter your whole order first (queueing); the kitchen then prepares dishes one at a time. You cannot taste the soup at the moment you wrote it on the order slip.

#### 3.2 Mixing normal JavaScript and Cypress commands

Because normal JavaScript runs *immediately* and Cypress commands run *later*, ordering bugs appear when you mix them:

```js
it('shows a surprising order', () => {
  cy.log('A: first Cypress command');
  console.log('B: plain JavaScript');
  cy.log('C: second Cypress command');
});
```

The browser console prints `B: plain JavaScript` **first**, because the three `cy.log` calls were only queued at that moment. The Command Log shows A and then C afterwards. If you need plain JavaScript to run in order with commands, put it inside `.then()`:

```js
it('keeps order with then', () => {
  cy.log('A');
  cy.then(() => console.log('B'));   // runs in sequence, after A
  cy.log('C');
});
```

#### 3.3 Retry-ability: Cypress's version of auto-wait

Playwright auto-waits for an element to be *actionable* (visible, enabled, stable) before clicking. Cypress does something similar but frames it differently:

- **Queries** (such as `cy.get()`, `cy.contains()`, `.find()`, `.first()`) are *retried* until the element exists or the timeout (default **4 seconds**, `defaultCommandTimeout`) elapses. Since Cypress 12, queries are retried *as a whole chain*, so if a re-render replaces an element, Cypress re-queries instead of failing with a "detached from the DOM" error.
- **Assertions** (such as `.should('be.visible')`) are retried together with the query that precedes them.
- **Actions** (such as `.click()`, `.type()`) run *once* after performing **actionability checks**: the element must be visible, not disabled, not detached, not covered by another element, and scrolled into view. Cypress waits (up to the timeout) for those conditions before acting. Actions themselves are **not** retried after they happen.

This retry system is the main reason you rarely write `cy.wait(2000)` in Cypress. We will discuss it again in "Writing Cypress tests" and "Element interaction".

### 4. System requirements and installation

#### 4.1 Prerequisites

- **Node.js** (current Cypress 13+/14 requires a modern LTS such as 18, 20, or 22; check the "System requirements" page for the exact supported list). Verify with `node --version`.
- **npm** (bundled with Node) or yarn/pnpm.
- A code editor (VS Code recommended). A typical Linux machine may also need system libraries for running the browser; the Cypress docs list them (for example `libgtk`, `libnss3`, `xvfb`).

#### 4.2 Step-by-step setup

Open a terminal and run these commands.

```bash
mkdir cypress-demo
cd cypress-demo
npm init -y
npm install cypress --save-dev
```

**Line by line:**

- `mkdir cypress-demo` creates a new folder for the project.
- `cd cypress-demo` moves into it. All following commands run inside this folder.
- `npm init -y` creates a `package.json` file with default values (`-y` answers "yes" to every prompt). `package.json` records your project's dependencies and scripts.
- `npm install cypress --save-dev` downloads the Cypress npm package and adds it to `devDependencies` (tools used for development, not production). The first time you install, Cypress also downloads its **binary** (the actual runner application, a couple of hundred megabytes) and caches it in a global location (for example `~/.cache/Cypress` on Linux/macOS or `%LOCALAPPDATA%\Cypress\Cache` on Windows). Subsequent projects reuse that cached binary if the version matches.

Then open Cypress for the first time:

```bash
npx cypress open
```

- `npx` runs a locally installed package binary without installing it globally.
- `cypress open` launches the **Launchpad**, the welcome screen. The Launchpad detects that this is a new project and offers a choice: **E2E Testing** or **Component Testing**.

Choose **E2E Testing**. Cypress will then:

1. Show the configuration files it will create (`cypress.config.js`, `cypress/support/e2e.js`, `cypress/support/commands.js`, and `cypress/fixtures/example.json`). Click **Continue**.
2. Ask you to pick a browser (Chrome, Edge, Firefox, Electron, whichever it detected on your machine).
3. Offer to **Create new spec** or **Scaffold example specs**. Choose "Create new spec" and name it `cypress/e2e/first.cy.js`.

#### 4.3 Your first spec

Replace the contents of `cypress/e2e/first.cy.js` with:

```js
describe('My first Cypress test', () => {
  it('visits the Cypress example site and finds a heading', () => {
    cy.visit('https://example.cypress.io');
    cy.contains('type').click();
    cy.url().should('include', '/commands/actions');
    cy.get('.action-email')
      .type('fake@email.com')
      .should('have.value', 'fake@email.com');
  });
});
```

**Line-by-line explanation:**

1. `describe('My first Cypress test', () => { ... })` - A **Mocha** function that groups related tests. The first argument is a label shown in the Test Runner; the second is a function containing the tests. `describe`, `it`, `before`, `beforeEach`, `after`, and `afterEach` are global; no import is needed.
2. `it('visits ...', () => { ... })` - Defines a single **test case**. The title describes the expected behaviour; it appears in the reports and Command Log.
3. `cy.visit('https://example.cypress.io')` - Loads the URL in the browser. `cy` is the global Cypress object. `visit` waits for the page's `load` event before the next command runs (up to `pageLoadTimeout`, default 60 seconds).
4. `cy.contains('type').click()` - `cy.contains` finds the first element that contains the text "type" (here, a link in the left-hand navigation). `.click()` clicks it after actionability checks.
5. `cy.url().should('include', '/commands/actions')` - `cy.url()` yields the current URL string. `.should('include', ...)` asserts it contains the given text. If it does not at first, Cypress retries until the 4-second timeout.
6. `cy.get('.action-email')` - Finds an element by CSS selector.
7. `.type('fake@email.com')` - Types characters into the field one at a time, with a small delay (10ms by default), firing the real keyboard events.
8. `.should('have.value', 'fake@email.com')` - Asserts the input's value equals the typed text. `have.value` is a Chai-jQuery assertion.

Notice the **chaining**: each command receives the *subject* yielded by the previous command. `cy.get()` yields an element; `.type()` acts on it and yields the same element; `.should()` asserts on it.

Save the file. In the Test Runner, click the spec name and watch it run. The left panel is the **Command Log** and the right is the app. You can hover over each command to see a snapshot.

#### 4.4 Running from the command line

`cypress open` is for development. `cypress run` is for automation and CI:

```bash
npx cypress run
```

By default, `cypress run` is **headless** (no visible browser window) and uses the built-in **Electron** browser. It runs every spec under `cypress/e2e`, prints results to the terminal, and by default (v13+) does **not** record video (video recording became off by default in Cypress 13) though failing tests can still capture screenshots. The next lesson covers choosing browsers and the headed/headless flags.

Add convenient npm scripts to `package.json`:

```json
{
  "scripts": {
    "cy:open": "cypress open",
    "cy:run": "cypress run",
    "cy:chrome": "cypress run --browser chrome"
  }
}
```

Now `npm run cy:open` launches the interactive runner. The `scripts` block is a map of friendly names to shell commands, so teammates never need to remember the exact flags.

### 5. The default folder structure

After the first launch, your project looks like this:

```
cypress-demo/
  cypress.config.js
  package.json
  cypress/
    e2e/
      first.cy.js
    fixtures/
      example.json
    support/
      commands.js
      e2e.js
```

| Path | Purpose |
|---|---|
| `cypress.config.js` | The central configuration file (replaces the old `cypress.json` used before Cypress 10). |
| `cypress/e2e/` | Your end-to-end spec files. Files matching `*.cy.js` (or `.cy.ts`, `.cy.jsx`, `.cy.tsx`) are discovered. |
| `cypress/fixtures/` | Static test data (JSON, images, CSV, etc.) loaded with `cy.fixture()`. See the lesson "Fixtures and custom fixtures". |
| `cypress/support/e2e.js` | Runs automatically **before every spec file**. Put global hooks, imports of plugins, and global behaviour here. |
| `cypress/support/commands.js` | Convenient place for your **custom commands** (`Cypress.Commands.add`). It is usually imported by `e2e.js`. |
| `cypress/screenshots/`, `cypress/videos/`, `cypress/downloads/` | Created on demand to store artifacts. Typically git-ignored. (Screenshots/video are covered Friday.) |

Add these generated folders to `.gitignore`:

```
node_modules
cypress/screenshots
cypress/videos
cypress/downloads
```

### 6. Understanding `cypress.config.js`

Here is a realistic configuration file for an E2E project:

```js
const { defineConfig } = require('cypress');

module.exports = defineConfig({
  e2e: {
    baseUrl: 'https://www.saucedemo.com',
    specPattern: 'cypress/e2e/**/*.cy.{js,jsx,ts,tsx}',
    supportFile: 'cypress/support/e2e.js',
    fixturesFolder: 'cypress/fixtures',
    viewportWidth: 1280,
    viewportHeight: 720,
    defaultCommandTimeout: 6000,
    retries: {
      runMode: 2,
      openMode: 0,
    },
    setupNodeEvents(on, config) {
      on('task', {
        log(message) {
          console.log(message);
          return null;
        },
      });
      return config;
    },
  },
});
```

**Line-by-line explanation:**

1. `const { defineConfig } = require('cypress');` - Imports the helper `defineConfig`. It does nothing at runtime except provide editor auto-complete and type hints; it returns the object you pass in. (If your project uses ES modules, the equivalent is `import { defineConfig } from 'cypress'` and `export default defineConfig({...})`.)
2. `module.exports = defineConfig({ ... });` - Exports the configuration so Cypress can read it.
3. `e2e: { ... }` - Options for E2E testing. Component testing has its own `component: { ... }` block. Options placed at the top level apply to both.
4. `baseUrl: 'https://www.saucedemo.com'` - The root URL of the app. After setting it, `cy.visit('/')` and `cy.visit('/inventory.html')` resolve relative to it. It also makes Cypress verify the server is reachable before starting. This is similar to `base_url` in pytest-playwright or `baseURL` in the Playwright config.
5. `specPattern` - A glob telling Cypress which files are specs. The default is `cypress/e2e/**/*.cy.{js,jsx,ts,tsx}`.
6. `supportFile` - The file that runs before every spec. Set it to `false` to disable.
7. `fixturesFolder` - Where `cy.fixture()` looks. Set to `false` to disable.
8. `viewportWidth` and `viewportHeight` - Default browser viewport size in pixels. The built-in default is 1000x660. (See "Browser management".)
9. `defaultCommandTimeout: 6000` - How long (in ms) query commands (`get`, `contains`, etc.) and assertions retry before failing. Default is 4000.
10. `retries: { runMode: 2, openMode: 0 }` - Re-run a failing test up to 2 additional times during `cypress run`, and none during `cypress open`. This is analogous to the "test retries" you learned for Playwright on Wednesday, though Cypress configures it differently. You can also set `retries: 2` as a single number.
11. `setupNodeEvents(on, config) { ... }` - A function that runs in **Node** when Cypress starts. It receives `on` (to register event handlers) and `config` (the resolved configuration, which you may modify). This is where you register **tasks** (Node functions your tests can call) and plugins.
12. `on('task', { log(message) {...} })` - Registers a task named `log`. Inside a test, `cy.task('log', 'hello')` sends `'hello'` to Node, which prints it in the terminal. Tasks **must return a value or `null`**, never `undefined`, or Cypress will report an error.
13. `return config;` - Returns the (possibly modified) configuration to Cypress.

Cypress documentation lists every option under "Configuration"; the ones above cover most day-to-day work. **Environment-specific values** (usernames, API URLs) go in the `env` block or in `cypress.env.json` (git-ignored), read in tests with `Cypress.env('KEY')`.

### 7. Mocha and Chai: what Cypress bundles

Cypress does not invent its own syntax for `describe`/`it`. It **bundles**:

- **Mocha** - the test framework providing `describe`, `context`, `it`, `before`, `beforeEach`, `after`, `afterEach`.
- **Chai** (plus **Chai-jQuery** and **Sinon-Chai**) - the assertion library behind `.should()` and `expect()`.
- **Sinon** - spies, stubs, and clocks (`cy.spy`, `cy.stub`, `cy.clock`).
- **jQuery** - elements yielded by `cy.get()` are jQuery objects, so `.then(($el) => $el.text())` works.
- **Lodash** (`Cypress._`), **Moment/Day.js-like helpers** (`Cypress.dayjs` in recent versions), and **Bluebird** (`Cypress.Promise`).

If you used Jest or Mocha before, you will feel at home. If you used `pytest` with Playwright, the analogy is: `describe` blocks are like test classes, `it` blocks are like test functions, and `beforeEach` plays the role of a pytest fixture with `autouse=True`. The assertion library is different; we cover it in the "Assertions and annotations" lesson.

### 8. Test isolation

Since Cypress 12, **test isolation is on by default** (`testIsolation: true`). Before each `it`, Cypress:

- Clears cookies, local storage, and session storage.
- Navigates the browser to `about:blank` (so the previous test's page is gone).

This means every `it` must call `cy.visit()` itself (or use `cy.session()`, discussed in "Writing Cypress tests"). The benefit is the same one you enjoyed with Playwright's per-test `BrowserContext`: tests do not leak state into each other.

---

## Code Examples

### Example 1: A complete config plus first spec for the practice app

`cypress.config.js`:

```js
const { defineConfig } = require('cypress');

module.exports = defineConfig({
  e2e: {
    baseUrl: 'https://www.saucedemo.com',
    viewportWidth: 1280,
    viewportHeight: 720,
  },
});
```

`cypress/e2e/login.cy.js`:

```js
describe('Login page', () => {
  beforeEach(() => {
    cy.visit('/');
  });

  it('logs in with valid credentials', () => {
    cy.get('[data-test="username"]').type('standard_user');
    cy.get('[data-test="password"]').type('secret_sauce');
    cy.get('[data-test="login-button"]').click();
    cy.url().should('include', '/inventory.html');
  });

  it('shows an error for a locked-out user', () => {
    cy.get('[data-test="username"]').type('locked_out_user');
    cy.get('[data-test="password"]').type('secret_sauce');
    cy.get('[data-test="login-button"]').click();
    cy.get('[data-test="error"]').should('contain.text', 'locked out');
  });
});
```

**Explanation:**

- `beforeEach(() => { cy.visit('/'); })` - A Mocha hook that runs before every `it` in this `describe`. Because `baseUrl` is set, `'/'` resolves to `https://www.saucedemo.com/`.
- Each `cy.get('[data-test="..."]')` uses an *attribute selector*. The practice site marks elements with `data-test` attributes, which are stable hooks for automation. (Selector strategy is the focus of the "Element location" lesson.)
- `.type('standard_user')` types into the username field.
- `.click()` presses the login button.
- `cy.url().should('include', '/inventory.html')` verifies the redirect after successful login.
- `.should('contain.text', 'locked out')` verifies that the error message includes the phrase. The check is *retried* until it passes or times out.

### Example 2: The same login test in Playwright (Python) for comparison

```python
import re
from playwright.sync_api import Page, expect

def test_login_valid(page: Page):
    page.goto("https://www.saucedemo.com")
    page.locator('[data-test="username"]').fill("standard_user")
    page.locator('[data-test="password"]').fill("secret_sauce")
    page.locator('[data-test="login-button"]').click()
    expect(page).to_have_url(re.compile(r".*/inventory.html"))
```

Observations that you will reuse in your Project 1 comparison note:

- Playwright's `page` is *passed in* (a fixture); Cypress's `cy` is *global*.
- Playwright uses `fill()` (sets the value at once); Cypress uses `type()` (simulates keystrokes). Cypress also has `.invoke('val', ...)` for quick setting, but `type` is idiomatic.
- Playwright's `expect(...).to_have_url` is the analogue of Cypress's `cy.url().should(...)`.

### Example 3: Using a task to log from Node

```js
// cypress.config.js (inside setupNodeEvents)
on('task', {
  log(message) {
    console.log(message);
    return null;
  },
});

// in a spec
it('reports a message to the terminal', () => {
  cy.task('log', 'Reached the login test');
});
```

**Explanation:** The spec runs in the browser, which cannot print to your terminal. `cy.task('log', ...)` sends a message over the Cypress connection to the Node process, which executes the `log` function and prints. This shows the two halves of the architecture cooperating.

### Example 4: Demonstrating queue order

```js
it('demonstrates the command queue', () => {
  console.log('1. JavaScript line one');
  cy.log('2. Cypress command one');
  console.log('3. JavaScript line two');
  cy.log('4. Cypress command two');
});
```

Open DevTools (F12) in the runner browser. You will see in the console: "1" then "3" (plain JS runs while the test body executes) and, after, the Cypress commands appear in the Command Log: "2" then "4". That demonstrates the queue.

---

## Real-World Scenarios

1. **Joining a React team.** The developers already run Cypress against their component library and want QA to write E2E flows. Understanding `cypress.config.js`, `baseUrl`, and the support file lets you read their repository on day one and contribute within hours.
2. **A CI pipeline.** A pull request triggers `npx cypress run --browser chrome`. The pipeline needs system libraries and the binary cache; understanding the Node process vs. browser split explains why CI errors say things like "Cypress failed to verify" (the binary cannot start) rather than "browser not found".
3. **Testing a payment flow that redirects to a third-party page.** In Playwright you would simply keep driving the same page. In Cypress, the redirect crosses origins, so you wrap the third-party steps in `cy.origin('https://pay.example.com', () => { ... })`. Knowing the same-origin reason helps you remember this.
4. **Reading a database value for test setup.** The test needs a freshly created user. A Cypress spec cannot connect to a database directly because it runs in the browser. You register a task in `setupNodeEvents` that uses a Node DB client, and the spec calls `cy.task('seedUser', {...})`.

---

## Common Pitfalls and Best Practices

**Pitfall 1: Using `async/await` with `cy` commands.**
Do not write `await cy.get(...)`. Use `.then()`, aliases (`.as()`), or `cy.wrap()` to work with values. A common correct pattern:

```js
cy.get('.price').invoke('text').then((text) => {
  const price = parseFloat(text.replace('$', ''));
  expect(price).to.be.greaterThan(0);
});
```

**Pitfall 2: Assigning a command result to a variable.**
`const el = cy.get('x')` does not give you an element. Use `.then()` or an alias.

**Pitfall 3: Forgetting that each test starts at a blank page.**
With test isolation, if the first command of an `it` is `cy.get()`, it fails because there is no page. Add `cy.visit()` in a `beforeEach`.

**Pitfall 4: Putting secrets in `cypress.config.js`.**
Config files are committed to git. Put credentials in `cypress.env.json` (git-ignored) or CI environment variables prefixed with `CYPRESS_` (e.g. `CYPRESS_PASSWORD`), then read them with `Cypress.env('PASSWORD')`.

**Pitfall 5: Returning `undefined` from a task.**
Always return a value or `null` from `on('task')` handlers.

**Pitfall 6: Mismatched binary and package versions.**
If `cypress verify` complains, run `npx cypress install` (or `npx cypress install --force`) to re-download the matching binary. `npx cypress info` and `npx cypress verify` are your diagnostic commands.

**Best practices**

- Pin the Cypress version in `package.json` and commit the lock file.
- Set `baseUrl` instead of hard-coding the domain in every `cy.visit`.
- Keep specs small and focused (one feature area per file).
- Use `npm run` scripts so everyone uses the same flags.
- Keep configuration for different environments in separate files and pass them with `--config-file` or `--env`.

---

## Mini Practice Exercises

**Exercise 1 - Install and run.**
Create a new folder, install Cypress, open it in E2E mode, scaffold a spec called `smoke.cy.js`, and make it visit `https://example.cypress.io` and assert that the page title (`cy.title()`) contains "Kitchen Sink".

*Solution:*

```js
describe('Smoke', () => {
  it('loads the home page', () => {
    cy.visit('https://example.cypress.io');
    cy.title().should('include', 'Kitchen Sink');
  });
});
```

**Exercise 2 - Configure.**
Update `cypress.config.js` so that `baseUrl` is `https://example.cypress.io`, the viewport is 1366x768, and the default command timeout is 8 seconds. Change `smoke.cy.js` to use `cy.visit('/')`.

*Hint:* Look at the `e2e` block in Section 6. Remember times are in milliseconds.

**Exercise 3 - The queue.**
Predict the order of console output and Command Log for the spec in Example 4 *before* running it. Then run it and check. Rewrite it so that the `console.log` lines appear in the same order as the `cy.log` lines.

*Hint:* wrap each `console.log` in `cy.then(() => ...)`.

**Exercise 4 - Compare.**
Take one test you wrote on Monday in Playwright (Python) and write a two-column note: left column your Playwright line, right column the Cypress equivalent. Do not worry about getting every command right yet; focus on the shape. You will refine it as you learn the later lessons today.

**Exercise 5 - A task.**
Add a `cy.task('log', ...)` call to your smoke test and confirm the message prints in the terminal when you run `npx cypress run`. Why does it *not* appear in the browser console?

*Answer:* because tasks execute in Node, not in the browser.

---

## Summary / Key Takeaways

- Cypress is a JavaScript/TypeScript testing tool for E2E and component testing that runs **inside the browser** alongside your application, with a Node process providing file and system access.
- Compared with Playwright, this brings speed and rich visibility but also limits: one tab, JavaScript/TypeScript only, and same-origin considerations (relaxed by `cy.origin`).
- Cypress commands are **queued**; do not use `await` with them. Use `.then()`, aliases, and assertions to work with yielded values.
- Queries and assertions **retry** automatically (default 4 seconds). Actions wait for actionability.
- Install with `npm install cypress --save-dev`; use `npx cypress open` for the interactive runner and `npx cypress run` for headless automation.
- `cypress.config.js` (using `defineConfig`) holds `baseUrl`, `specPattern`, viewport, timeouts, retries, and the `setupNodeEvents` function where Node tasks live.
- The folders `cypress/e2e`, `cypress/fixtures`, and `cypress/support` hold specs, data, and shared code. Test isolation (default on) resets browser state between tests.
- Bundled tools: Mocha, Chai, Sinon, jQuery, Lodash.
- Topics deliberately left for later: the next lessons cover browsers, writing tests, selectors, assertions, selection, fixtures, interaction and debugging actions. Detailed time-travel debugging, screenshots, and video are **covered in depth on Friday**.

---

## External Resources

- Cypress Documentation - Getting Started / Installing Cypress: https://docs.cypress.io/app/get-started/install-cypress
- Cypress Documentation - Key Differences (how Cypress works and its trade-offs): https://docs.cypress.io/app/references/trade-offs
- Cypress Documentation - Configuration reference: https://docs.cypress.io/app/references/configuration
