# Logging in Cypress: `cy.log`, `Cypress.log`, the Console and `cy.task`

## Learning Objectives

By the end of this lesson you will be able to:

- Explain why logging in test automation is different from logging in a normal program, and why Cypress has **four distinct "places" where logs can go**.
- Use `cy.log()` to add readable, queued messages to the Command Log, and explain why it is queued rather than immediate.
- Use plain `console.log()` correctly in Cypress specs, and explain the **asynchronous queue trap** that makes `console.log` print "too early".
- Create rich, structured log entries with `Cypress.log()` (`name`, `displayName`, `message`, `$el`, `consoleProps`, `type`, `autoEnd`, `snapshot`, `end`, `error`), especially inside custom commands.
- Use `cy.task()` to send messages from the browser to the **Node.js process**, so they appear in the terminal and CI logs, and write them to files.
- Build a small, reusable **logger helper** with levels (`info`, `warn`, `error`, `debug`) that is safe for secrets.
- Choose the right logging technique for local debugging versus CI, and know where each type of log is visible.
- Control the noise: `{ log: false }`, log levels, and the main third-party and built-in options (`DEBUG=cypress:*`, plugins such as `cypress-terminal-report`).

---

## Why This Matters

This week's epic is about moving from "I can automate a form" to "I can build and maintain reliable automation". Reliability is largely about **observability**: when a test fails, can you tell what it was doing, what data it used and what the system returned?

In **Project 1: QE Foundations** you are producing UI automation that other people (reviewers, teammates, CI pipelines) must be able to trust and diagnose. A test that fails with only "expected true to be false" is a problem for everybody. A test that leaves a trail such as "Logging in as standard_user", "Added 'Sauce Labs Backpack' to cart", "Cart badge shows 1" is self-documenting. When it fails at the third line, you know where you are before you even open the video.

Cypress is a little unusual here. Because its commands are **queued and run asynchronously**, and because the test code runs in the **browser** while the CI log shows the **Node process**, the question "where did my log go?" has several answers. Many beginners put `console.log` in their spec, run `cypress run` in CI, and see nothing in the terminal. Today you will learn exactly why and what to do about it.

In earlier days you saw Playwright's `console` listeners and Python/JavaScript logging. The Cypress picture is different enough that it deserves its own lesson.

---

## The Concept

### 1. Four places a log can go

Before we write any code, understand the four destinations, because most confusion comes from mixing them up.

| Destination | How you write to it | Who sees it | Visible in `cypress run` terminal? |
|---|---|---|---|
| **Command Log** (the Test Runner panel) | `cy.log()`, `Cypress.log()` | Anyone with the Test Runner open; shown in screenshots of the runner and in videos | No (it is UI only; failure screenshots and videos of the runner show it) |
| **Browser DevTools Console** | `console.log()`, `console.table()`, `consoleProps` of pinned log rows, `.debug()` | You, if DevTools is open | No (the browser console is not forwarded to the terminal) |
| **Terminal / CI log** (the Node.js process) | `cy.task('log', ...)` which runs `console.log` in Node | Everyone reading the CI output | **Yes** |
| **Files on disk** | `cy.task(...)` that uses Node's `fs`, or `cy.writeFile()` | Anyone who downloads the file or artifact | Not directly (you may upload the file) |

Keep this table in mind: it answers 90 percent of "where is my log?" questions.

### 2. Why Cypress logs are different: the command queue

This is the most important idea in the lesson. When you write:

```js
it('shows the queue', () => {
  console.log('A');
  cy.log('B');
  console.log('C');
});
```

Many learners expect `A`, `B`, `C` in order. What actually happens:

1. Cypress runs your test function from top to bottom **synchronously**. During that pass, plain JavaScript lines (`console.log`) run immediately, and every `cy.*` call only **adds a command to a queue**. It does *not* execute it yet.
2. So the browser console shows `A` then `C` almost instantly.
3. *After* the function finishes, Cypress executes the queue: `cy.log('B')` runs now, and `B` appears in the Command Log.

So the observable order is **A, C, then B**. This is not a bug; it is how Cypress achieves automatic retry-ability and clean chaining. The practical lesson: **to log a value at the right moment in the command sequence, you must put the log inside the queue**, typically with `.then()`:

```js
cy.get('[data-test="shopping-cart-badge"]').then(($badge) => {
  console.log('Cart badge text is:', $badge.text());
});
```

Everything inside `.then(...)` runs at the correct time, in order with the other commands.

### 3. `cy.log()`: messages in the Command Log

`cy.log(message, ...args)` prints a row in the Command Log. It is queued like any other command, so it appears *in sequence* between the commands around it.

Basic use:

```js
cy.log('Logging in as a standard user');
```

You can pass additional arguments. Cypress joins the message and every extra argument into a single line, separated by a comma and a space, and shows that line in the Command Log:

```js
cy.log('User details', 'standard_user', 42);
// Command Log row: User details, standard_user, 42
```

The Command Log renders **inline Markdown** across the displayed line (for example `**bold**`, `_italic_` and `` `code` ``). HTML tags are shown as plain text. Another subtle point from the official docs: a variable that an earlier command changes still holds its *old* value at the moment it is handed to `cy.log()`, because the arguments are evaluated while the queue is being built (the same queue trap explained in the next section). For objects, prefer `JSON.stringify(obj)` inside a `.then()` so you get a readable line.

Properties of `cy.log`:

- It **yields `null`** (it does not pass a subject down the chain), so don't chain `.click()` after it.
- It does not retry, assert or interact with the page.
- It appears in screenshots and videos of the runner, which makes it very useful as **section headings** in a long test: `cy.log('--- Step 3: Checkout ---')`.
- If you need a value that is only known at run time, use `.then()` or `cy.wrap()` and build the message inside it, as in section 2.

You can switch off the log rows of other commands to reduce noise (`cy.get('.x', { log: false })`), but keep your own `cy.log` lines, which are, after all, there to communicate intent.

### 4. `console.log()`: the browser console

Specs run in the browser, so `console.log()` writes to the browser DevTools console. Use it when:

- You are developing locally with DevTools open.
- You want to inspect a complex object interactively (the console lets you expand it).
- You use `console.table(rows)` to see an array of objects as a table.

Do not rely on it for CI: it will not show up in the terminal. (Failure screenshots of the runner show only the Command Log, not the console.)

Tips:

- `console.log` inside `.then()` runs in order with commands.
- `console.log` outside a command callback runs *during* the queue-building phase (see section 2).
- Remember that **Cypress itself prints details to the console when you pin/click a log row**. Often you do not need your own `console.log`, because clicking the command row prints its subject and yield.

### 5. `.debug()` and `cy.pause()` as logging cousins

These were introduced on Thursday and extended in the debugging lesson earlier today. For logging purposes:

- `.debug()` prints the current subject to the console and triggers the debugger if DevTools is open. It is a "log this value and pause" tool.
- `cy.pause()` is a manual breakpoint in the command queue.

They are interactive tools. Use `cy.log`/`cy.task` for logging that has to survive in CI.

### 6. `Cypress.log()`: custom, structured Command Log entries

`cy.log` is a *command* and it is simple. `Cypress.log()` is a *lower-level API* that lets you create log rows with the same richness as Cypress's own commands. You use it mainly inside **custom commands** so that `cy.login(...)`, `cy.addToCart(...)` and similar helpers show up as one tidy, meaningful row with detail on click.

It is a function that takes an options object and returns a **Log** object:

| Option | Meaning |
|---|---|
| `name` | Internal command name (shown in the log; for Cypress's own commands this is `get`, `click`, ...). |
| `displayName` | A shorter label shown instead of `name` in the Command Log (good for custom commands). |
| `message` | Text displayed next to the name. By default it is the command's arguments. |
| `$el` | A jQuery element. When the row is hovered or pinned, that element is highlighted in the app preview. |
| `consoleProps` | A **function** returning an object. Its properties are printed to the browser console when the row is clicked. Put debug data here. |
| `type` | `'parent'` (default) or `'child'`; a child row is indented under its parent. |
| `autoEnd` | `true` by default: Cypress finishes the row for you. Set to `false` when your command does asynchronous work, and call `end()` yourself. |
| `end` | If `true`, the row is marked finished immediately. |

The returned Log object has methods:

- `log.snapshot(name?)` captures a DOM snapshot for time-travel (named snapshots such as `'before'`/`'after'` show as tabs when pinned).
- `log.set(key, value)` or `log.set({ ... })` updates attributes later, for example setting `consoleProps` once an asynchronous result arrives.
- `log.get()` / `log.get('message')` reads attributes.
- `log.end()` marks the row as complete and passed.
- `log.error(err)` marks the row as failed and attaches an error. **It does not fail the test by itself**; you must also throw the error.
- `log.finish()` is used internally; the docs recommend `end()` in your own commands.

### 7. `cy.task()`: logging to the terminal and to files

Because specs run in the browser, they cannot write to the terminal or the file system directly. But Cypress has a bridge to the **Node.js process** that launched it: `cy.task(eventName, arg)`.

How it works:

1. In `cypress.config.js`, inside `setupNodeEvents`, you register handlers with `on('task', { ... })`. Each key is an event name; each value is a function that runs in **Node** and can use `console.log`, `fs`, databases, and so on.
2. In a spec, `cy.task('log', 'hello')` serialises the argument, sends it to Node, runs the handler, and yields whatever the handler returns.

Rules you must remember:

- A task handler **must return something other than `undefined`**. Return `null` if you have nothing to return. If it returns `undefined`, Cypress fails the command (this catches typos in event names and forgotten returns). The handler may return a promise.
- A task takes **one argument**, which must be serialisable (strings, numbers, booleans, arrays and plain objects). Functions, regular expressions and symbols become `null`. To pass several values, pass an object. Dates arrive as strings.
- Tasks have a timeout (`taskTimeout`, 60 seconds by default). Do not start servers or never-ending processes in tasks.
- `cy.task` is itself a queued command, so ordering is preserved. It also creates a row in the Command Log, which you can suppress with `{ log: false }`.

A task named `log` is the standard "print to the CI terminal" pattern.

### 8. Designing a log helper

Calling `cy.task('log', ...)` everywhere is verbose. Wrap it in a custom command that does *both*: a row in the Command Log and a line in the terminal, with a level and a timestamp. Include sanitising of secrets. We build this below.

### 9. Where logs go during `cypress run` (summary)

- **Reporters:** `cypress run` prints the Mocha "spec" reporter output (test names and pass/fail) in the terminal. You can change the reporter in the config (`reporter: 'junit'`, `'mocha-junit-reporter'`, `'mochawesome'`, or a custom one). Test reports are about results, not about your intermediate logs.
- **`cy.task('log')`** output appears in the terminal *interleaved* with test progress.
- **Browser console output** can be seen by Cypress's own log of "console errors" only in specific cases; otherwise it is not in the terminal. A plugin (see below) can forward it.
- **Debug logs of Cypress itself:** set the `DEBUG` environment variable, for example `DEBUG=cypress:server:video npx cypress run`, or `DEBUG=cypress:* npx cypress run` for everything (very verbose). These are for diagnosing Cypress itself, such as a plugin failing to load or video encoding, not for test intent.

### 10. Community plugin: `cypress-terminal-report`

The widely used open-source plugin `cypress-terminal-report` prints Cypress commands (and optionally `console` output) to the terminal and can write them to files after tests, which is a convenient way to get a "Command Log in the terminal" in CI. It is installed from npm and registered both in `setupNodeEvents` (`require('cypress-terminal-report/src/installLogsPrinter')(on)`) and in the support file (`require('cypress-terminal-report/src/installLogsCollector')()`). Always check its README for the setup that matches your Cypress version, because plugin configuration formats change.

### 11. Logging etiquette

- Log **intent** (what the test is trying to do) and **key data** (IDs, usernames), not every keystroke. Cypress already logs commands.
- Never log passwords, tokens, personal data or card numbers.
- Do not log inside tight loops without reason.
- Prefer meaningful sentences to cryptic codes: `cy.log('Add backpack to cart')`, not `cy.log('step 4')`.
- Keep a consistent format across the team.

---

## Code Examples

### Example 1: `cy.log` as section headings

```js
describe('Checkout flow logging', () => {
  it('logs each phase of the purchase', () => {
    cy.log('**Phase 1: Login**');
    cy.visit('https://www.saucedemo.com');
    cy.get('[data-test="username"]').type('standard_user');
    cy.get('[data-test="password"]').type('secret_sauce');
    cy.get('[data-test="login-button"]').click();

    cy.log('**Phase 2: Add to cart**');
    cy.get('[data-test="add-to-cart-sauce-labs-backpack"]').click();
    cy.get('[data-test="shopping-cart-badge"]').should('have.text', '1');

    cy.log('**Phase 3: Open cart**');
    cy.get('[data-test="shopping-cart-link"]').click();
    cy.url().should('include', '/cart.html');
  });
});
```

**Line-by-line explanation**

1. `describe`/`it` create the suite and test.
2. `cy.log('**Phase 1: Login**')` adds a row to the Command Log. The double asterisks are inline Markdown for bold, which the Command Log renders.
3. The `visit`, `get`, `type`, `click` lines perform the login.
4. A second `cy.log` marks the start of the cart phase. Because it is queued, it appears *between* the login `click` and the next `get`.
5. `cy.get(...).should('have.text', '1')` verifies the cart badge text equals `1`.
6. The third `cy.log` marks the navigation to the cart.
7. `cy.url().should('include', '/cart.html')` asserts the navigation worked.

When you watch the test, the Command Log reads like an outline of the scenario. In a failure screenshot (which captures the runner), the nearest `cy.log` heading tells you which phase failed.

### Example 2: The queue trap, demonstrated and fixed

```js
it('shows the order of execution', () => {
  cy.visit('https://www.saucedemo.com');
  cy.get('[data-test="username"]').type('standard_user');
  cy.get('[data-test="password"]').type('secret_sauce');
  cy.get('[data-test="login-button"]').click();

  // WRONG: runs immediately while the queue is being built
  const count = Cypress.$('[data-test="inventory-item"]').length;
  console.log('WRONG count (probably 0):', count);

  // RIGHT: runs in order, after the click has completed
  cy.get('[data-test="inventory-item"]').then(($items) => {
    console.log('RIGHT count:', $items.length);
    cy.log(`Products on the page: ${$items.length}`);
  });
});
```

**Line-by-line explanation**

1. The first block logs in. Remember none of those commands has *executed* yet at the moment the next lines run; they are only queued.
2. `Cypress.$('[data-test="inventory-item"]')` is a direct jQuery query of the current document. At queue-building time, the browser is still on the login page, so the count is `0`. This is a classic bug source: mixing synchronous jQuery with queued commands.
3. `console.log('WRONG count ...')` therefore prints `0` almost instantly.
4. `cy.get(...)` is queued. When it runs (after the login click completed), it yields the product elements.
5. `.then(($items) => { ... })` receives them. `$items` is a jQuery collection; `.length` is the count (6 on this site).
6. `console.log('RIGHT count:', ...)` prints to the browser console in correct order.
7. `cy.log(...)` *inside* the `.then` adds a Command Log row. Calling a Cypress command inside `.then` is allowed and the new command is queued right after the current one.
8. The template literal `` `Products on the page: ${$items.length}` `` builds the message from the value, which is why this log must be inside the callback.

### Example 3: `cy.task` for terminal logging, with a safe task handler

`cypress.config.js`:

```js
const { defineConfig } = require('cypress');
const fs = require('fs');
const path = require('path');

module.exports = defineConfig({
  e2e: {
    setupNodeEvents(on, config) {
      on('task', {
        log({ level = 'info', message }) {
          const line = `[${new Date().toISOString()}] [${level.toUpperCase()}] ${message}`;
          console.log(line);
          return null;
        },

        logToFile({ file = 'cypress-run.log', message }) {
          const target = path.join('cypress', 'logs', file);
          fs.mkdirSync(path.dirname(target), { recursive: true });
          fs.appendFileSync(target, message + '\n');
          return null;
        },
      });

      return config;
    },
  },
});
```

**Line-by-line explanation**

1. `defineConfig`, `fs` and `path` are imported. `fs` writes files; `path` builds portable file paths.
2. `setupNodeEvents(on, config)` runs in Node when Cypress starts. `on` registers event listeners.
3. `on('task', { ... })` registers an object of task handlers. The **keys** (`log`, `logToFile`) are the names used by `cy.task('log', ...)`.
4. `log({ level = 'info', message })` uses **destructuring** with a default value: the single argument must be an object; `level` defaults to `'info'`. Remember tasks accept one argument, which is why we pass an object.
5. The `line` constant builds a timestamped string: `new Date().toISOString()` gives a UTC timestamp like `2026-10-08T09:30:00.000Z`; `level.toUpperCase()` normalises the level.
6. `console.log(line)` prints in the **Node process**, i.e. the terminal or the CI log. This is the key difference from a spec's `console.log`.
7. `return null;` is mandatory. Returning `undefined` would make the command fail.
8. `logToFile(...)` builds a path under `cypress/logs/`, creates the folder if needed (`recursive: true`), appends the message with a newline, and returns `null`. `appendFileSync` is synchronous, which is fine for small log lines; for very high volume, use a stream.
9. `return config;` hands the configuration back to Cypress.

### Example 4: A custom `cy.step()` / `cy.logInfo()` command that logs everywhere

`cypress/support/commands.js`:

```js
const SENSITIVE_KEYS = ['password', 'token', 'authorization', 'cardNumber'];

function sanitize(value) {
  if (value && typeof value === 'object') {
    return Object.fromEntries(
      Object.entries(value).map(([k, v]) =>
        SENSITIVE_KEYS.includes(k) ? [k, '***'] : [k, sanitize(v)]
      )
    );
  }
  return value;
}

Cypress.Commands.add('logInfo', (message, data) => {
  const safeData = data === undefined ? undefined : sanitize(data);
  const text = safeData === undefined ? message : `${message} ${JSON.stringify(safeData)}`;

  const log = Cypress.log({
    name: 'info',
    displayName: 'INFO',
    message: text,
    consoleProps: () => ({ message, data: safeData }),
  });

  cy.task('log', { level: 'info', message: text }, { log: false });
});
```

**Line-by-line explanation**

1. `SENSITIVE_KEYS` is a list of property names that must never appear in logs.
2. `sanitize(value)` is a recursive function. If `value` is an object (and not `null`), it converts it to entries (`[key, value]` pairs), maps each pair, replacing sensitive values by `'***'` and recursing into other values, then rebuilds an object with `Object.fromEntries`. Non-object values (strings, numbers) are returned untouched.
3. `Cypress.Commands.add('logInfo', (message, data) => { ... })` defines `cy.logInfo('text', { optional: 'data' })`.
4. `safeData` is the sanitised data, or `undefined` if none was given.
5. `text` is a single string: the message, plus the JSON of the safe data when present.
6. `Cypress.log({...})` creates the Command Log row: `displayName: 'INFO'` is what you see; `message: text` is next to it; `consoleProps` returns an object printed to the DevTools console when the row is pinned. Because `autoEnd` is not set to `false`, Cypress closes the row automatically. (Remember: for purely synchronous commands like this one, auto-ending is correct.)
7. `cy.task('log', { level: 'info', message: text }, { log: false })` sends the same message to the Node process (so it shows in the terminal). The third argument `{ log: false }` hides the `task` row from the Command Log, so the user sees one clean `INFO` row instead of two.

Usage:

```js
cy.logInfo('Logging in', { username: 'standard_user', password: 'secret_sauce' });
// Command Log: INFO Logging in {"username":"standard_user","password":"***"}
// Terminal:    [2026-10-08T09:30:00.000Z] [INFO] Logging in {"username":"standard_user","password":"***"}
```

### Example 5: `Cypress.log` with an element and an asynchronous command

```js
Cypress.Commands.add('clickAndLog', (selector) => {
  const log = Cypress.log({
    name: 'clickAndLog',
    message: selector,
    autoEnd: false,
  });

  return cy
    .get(selector, { log: false })
    .then(($el) => {
      log.set({ $el });
      log.set({ consoleProps: () => ({ selector, matched: $el.length, text: $el.text().trim() }) });
      log.snapshot('before');
    })
    .click({ log: false })
    .then(() => {
      log.snapshot('after').end();
    });
});
```

**Line-by-line explanation**

1. The command takes a selector.
2. `Cypress.log({... autoEnd: false})` creates the row but tells Cypress *not* to end it; we will end it ourselves because the work is asynchronous.
3. `cy.get(selector, { log: false })` finds the element but suppresses its own row.
4. `.then(($el) => { ... })` runs when the element has been found. `log.set({ $el })` attaches the element to the log so it is highlighted when you hover over the row. The second `set` stores `consoleProps` (a function), so when you pin the row, the console prints the selector, the number of matches and the element text. `log.snapshot('before')` saves a named snapshot.
5. `.click({ log: false })` performs the click, again without a separate row.
6. The last `.then` takes the "after" snapshot and calls `.end()`, which marks the row passed.
7. Because everything is chained on `cy`, Cypress waits for each step in order.

### Example 6: Listening to all log rows with events (advanced)

```js
// cypress/support/e2e.js
Cypress.on('log:added', (attrs) => {
  if (attrs.name === 'assert') {
    // Runs in the browser; forward assertion messages to the terminal
    cy.task('log', { level: 'debug', message: `ASSERT: ${attrs.message}` }, { log: false });
  }
});
```

**Explanation**

- `Cypress.on('log:added', callback)` fires whenever Cypress adds a new Command Log row. `attrs` contains the row's attributes (`name`, `message`, `type`, and others).
- We filter for assertions and forward them to the terminal with `cy.task`.
- **Caveat:** calling Cypress commands from inside Cypress event handlers can cause surprising behaviour (commands queued at awkward moments, or logs that trigger further logs). Treat this as an advanced technique, test it carefully, and prefer a library such as `cypress-terminal-report` if you need this globally.

### Example 7: Running with debug output

```bash
# Print Cypress internals related to video encoding
DEBUG=cypress:server:video npx cypress run

# Windows PowerShell equivalent
$env:DEBUG="cypress:server:video"; npx cypress run
```

**Explanation**

- `DEBUG` is read by the `debug` Node module that Cypress uses internally. The value is a namespace pattern. Use it to troubleshoot Cypress itself (plugin load errors, video encoding, proxy issues), not your tests.

---

## Real-World Scenarios

### Scenario 1: CI log is empty, what happened?

A teammate adds `console.log('user:', user)` in a spec and wonders why the Jenkins console shows nothing. You explain: spec code runs in the browser, so the output went to the browser's console, which in headless CI nobody sees. You replace it with `cy.logInfo('user', user)` that also calls `cy.task('log')`. Now the CI log shows the line, with a timestamp.

### Scenario 2: A long checkout test

The checkout test has 60 commands. When it fails, the failure screenshot shows the runner with the error but you cannot immediately tell which *business step* failed. You add `cy.log('**Step N: ...**')` headings for each business step. Next failure, the screenshot's Command Log shows the last heading just above the red row. Triage time drops from minutes to seconds.

### Scenario 3: Auditable test data

A test creates an order through an API. You log the order ID using `cy.logInfo('Order created', { orderId })`. When someone later investigates a strange order in the database, the ID in the CI log lets them find which test created it.

### Scenario 4: Audit file for compliance

For a regulated client, every automated run must keep a record of which accounts were used. The `logToFile` task appends account IDs (never passwords) to `cypress/logs/run.log`, and the CI pipeline uploads that file as an artifact, with retention aligned to company policy.

---

## Common Pitfalls and Best Practices

1. **The queue trap.** `console.log` and direct jQuery lines run before queued commands. Put dependent logic inside `.then()`.
2. **Assuming `console.log` reaches CI.** It does not. Use `cy.task` (or a plugin) for the terminal.
3. **Returning `undefined` from a task.** Always `return null` (or a value). This is the most frequent task error.
4. **Passing more than one argument to `cy.task`.** Only one serialisable argument is supported; wrap values in an object.
5. **Logging secrets.** Sanitise. Never log passwords, tokens, or personal data; also remember that Cypress's own `type` log row shows the typed text. For secrets, pass `{ log: false }` to `.type()` (as in the custom-command example in the time-travel lesson) so the value is not echoed in the Command Log; password-type inputs are additionally masked in the app preview.
6. **Over-logging.** Log intent and key data. Hundreds of rows make the Command Log harder to read.
7. **Using `log.error()` and expecting the test to fail.** It only marks the row. Throw an error as well.
8. **Forgetting `autoEnd: false` in async custom commands.** If you do not set it, the row ends before the work is done; if you set it and forget `end()`, the row spins forever.
9. **Writing to files without making directories.** `fs.appendFileSync` fails if the folder does not exist; create it with `mkdirSync(..., { recursive: true })`.
10. **Tasks that never return.** A task has a timeout; do not start long-lived processes.
11. **Mixing logging helpers inconsistently.** Pick one team convention (`cy.logInfo`, `cy.step`, ...) and document it.
12. **Calling commands in event handlers without care.** `Cypress.on` handlers run outside the normal flow; keep them tiny or use a vetted plugin.

---

## Mini Practice Exercises

### Exercise 1: Fix the order

Predict the order of output of:

```js
it('order', () => {
  console.log('1');
  cy.log('2');
  cy.then(() => console.log('3'));
  console.log('4');
});
```

*Solution:* the browser console prints `1`, `4`, then `3`; the Command Log shows `2` as a row. `cy.log('2')` and `cy.then` are queued; the plain `console.log` calls run first.

### Exercise 2: Add a `log` task

Add a `log` task to your `cypress.config.js` and call `cy.task('log', { level: 'warn', message: 'Hello from the spec' })` in a test. Run with `npx cypress run` and find the line in your terminal.

*Hint:* look at Example 3. Remember `return null`.

### Exercise 3: Make a `cy.step`

Create a custom command `cy.step('Add backpack')` that (a) adds a `cy.log` heading with `**STEP**`, and (b) sends the same text to the terminal through `cy.task`. Use it three times in a test.

*Solution sketch:*

```js
Cypress.Commands.add('step', (title) => {
  cy.log(`**STEP: ${title}**`);
  cy.task('log', { level: 'info', message: `STEP: ${title}` }, { log: false });
});
```

### Exercise 4: Sanitiser test

Write a small unit test (a plain `it` without visiting a page) that calls `sanitize({ user: 'a', password: 'b', nested: { token: 'c' } })` and asserts the result equals `{ user: 'a', password: '***', nested: { token: '***' } }`.

*Hint:* use `expect(result).to.deep.equal({...})`. Export or copy the function into the spec.

### Exercise 5: Where did it go?

For each, say which destination (Command Log, browser console, terminal, file) receives the output: (a) `cy.log('x')`, (b) `console.table(items)` inside `.then`, (c) `cy.task('log', 'x')`, (d) `cy.writeFile('out.txt', 'x')`, (e) pinning a command row.

*Solution:* (a) Command Log; (b) browser console; (c) terminal; (d) file on disk (written by Cypress through Node); (e) browser console (details printed).

---

## Summary / Key Takeaways

- There are **four destinations** for logs: the Command Log, the browser console, the Node terminal and files. Know which you are using.
- `cy.log()` adds queued rows to the Command Log and is great for **section headings** and intent.
- `console.log()` goes to the browser console only, and **runs immediately** unless placed inside `.then()` (the queue trap).
- `Cypress.log()` builds rich custom entries with `displayName`, `message`, `$el`, `consoleProps` and snapshots; use `autoEnd: false` plus `end()` for asynchronous commands.
- `cy.task()` bridges the browser to Node so you can print to CI logs and write files; handlers must return a non-`undefined` value and accept a single serialisable argument.
- Build a small logging helper with levels and secret sanitisation, and keep logs meaningful.
- Use `DEBUG=cypress:*` for diagnosing Cypress itself, and consider `cypress-terminal-report` for terminal command logs.

---

## External Resources

- Cypress documentation, `cy.log()`: https://docs.cypress.io/api/commands/log
- Cypress documentation, `Cypress.log()` API: https://docs.cypress.io/api/cypress-api/cypress-log
- Cypress documentation, `cy.task()`: https://docs.cypress.io/api/commands/task
