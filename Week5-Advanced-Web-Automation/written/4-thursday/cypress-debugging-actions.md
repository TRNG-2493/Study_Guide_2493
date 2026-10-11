# Cypress Debugging Actions

## Learning Objectives

By the end of this lesson you will be able to:

- Explain why debugging Cypress code is different from debugging ordinary JavaScript (because of the command queue), and how to avoid the classic traps.
- Read the **Command Log**, understand its color-coded statuses, and interpret a Cypress error message and code frame.
- Use `cy.pause()` to step through a test one command at a time, and `cy.debug()` / `.debug()` to inspect the current subject.
- Use the JavaScript `debugger` statement correctly inside `.then()` callbacks, and use `console.log` safely (ordering!).
- Print values to the console with `.then(console.log)` and `.should(console.log)`, and use "Print to console" by clicking commands in the Command Log.
- Add breadcrumbs with `cy.log()` and send messages to the terminal with `cy.task('log')` (a brief introduction; the logging topic is covered fully on Friday).
- Open DevTools, use the Selector Playground, and re-run a single test during development.
- Reproduce a `cypress run` failure with `--headed --no-exit`, use `.only`, and turn off retries while debugging.
- Apply a repeatable debugging checklist to common failure types: element not found, covered element, detached DOM, timeout, assertion mismatch, network issues.
- Compare Cypress's debugging tools with Playwright's `page.pause()`, Inspector, and `PWDEBUG` workflow from earlier in the week.

---

## Why This Matters

No test engineer writes a test correctly on the first try every time. Real-world automation involves spending a large share of your day *investigating why something failed*: was it the application, the test, the data, or the environment? A beginner who cannot debug is stuck after the first red test; an engineer who debugs methodically becomes the person the team relies on.

Cypress is famous for its debugging experience because the tests run **inside the browser alongside your application**, so you can use the browser's own DevTools, pause mid-test, and see snapshots of the app. This ties directly to the Week 5 epic: you have now learned Playwright's debugging (inspector, `page.pause()`, trace viewer) and you will compare it to Cypress's in your Project 1 note.

On Thursday we focus on the **debugging actions**: commands and techniques you *write* or *invoke* (`cy.pause`, `cy.debug`, `debugger`, `console.log`, `cy.log`, the Command Log). On Friday we go deeper on **time-travel debugging** (the snapshot and DOM replay experience), **screenshots and video**, and **logging** - those are **covered in depth on Friday**, so today we only touch them briefly.

### Playwright (Python) to Cypress comparison

| Goal | Playwright (Python) | Cypress |
|---|---|---|
| Pause and inspect | `page.pause()` opens the Inspector | `cy.pause()` pauses the runner; step with Next |
| Run slowly and visibly | `--headed --slowmo 500` | `cypress open` (headed by default); `{ delay }` on type |
| Debug UI | Inspector, `PWDEBUG=1` | Test Runner, DevTools |
| Print a value | `print(...)` in Python | `cy.log(...)`, `console.log(...)` inside `.then()` |
| Break in code | `breakpoint()` (pdb) | `debugger` inside `.then()` |
| Past-state inspection | Trace viewer (after the run) | Snapshots in the Command Log (during the run); more Friday |
| Locator exploration | `codegen`, Inspector pick locator | Selector Playground |
| Failure evidence | Screenshot, video, trace | Screenshot, video (Friday) |

---

## The Concept

### 1. Why debugging Cypress needs a different mindset

Recall the central idea from the first lesson: **Cypress commands are queued and run later; plain JavaScript runs immediately.** This creates debugging traps:

```js
it('shows the trap', () => {
  cy.visit('/');
  console.log('A: I run immediately, before the page has even loaded');
  debugger;                              // pauses BEFORE any Cypress command has run
  cy.get('[data-test="username"]').type('standard_user');
});
```

When you hit that `debugger`, the browser has only *registered* the commands; none has executed. If you expected to inspect the page, you will find it is blank. The fix is to place debugging code **inside the command chain** using `.then()`:

```js
it('debugs at the right moment', () => {
  cy.visit('/');
  cy.get('[data-test="username"]').then(($el) => {
    console.log('B: runs after the element is found', $el);
    debugger;                            // now the page is loaded and $el is real
  });
});
```

Memorise this rule: **if you want to stop or print "at this point in the test," do it inside `.then()` (or use `cy.pause()`/`.debug()`).**

### 2. The Command Log: your first debugging tool

In `cypress open`, the left panel is the **Command Log** (also called the "reporter"). It lists every command executed, in order:

- **Test name** at the top; hooks (before each) are grouped.
- Each command shows its name and arguments: `get [data-test="username"]`, `type standard_user`, `click`, `assert expected ... to have text ...`.
- **Assertions** are listed with a pass (green check) or fail (red cross). Passing assertions include both expected and actual values, which is very informative.
- **Network requests** (XHR/fetch) appear as entries (`(xhr) GET 200 /api/products`), both stubbed and real, if intercepted or tracked.
- **Colors and icons**: green = passed, red = failed, blue/pending dot = currently running, grey = skipped/pending, an orange border sometimes marks retried or "pinned" items.

**Interactions with the Command Log:**

1. **Hover** over a command: the app preview on the right shows a snapshot of the page at that moment and highlights the target element.
2. **Click** a command to *pin* it: the snapshot stays; the console prints details of the command (subject, yielded value, options, elements). Click again to unpin.
3. For action commands, use the **before/after** toggle to see the page before and after the action. For a `click`, you will see a red hit-point marker showing exactly where Cypress clicked.
4. **Open DevTools** (F12 or Ctrl/Cmd+Shift+I) while a command is pinned and look at the console: Cypress has printed "Command", "Elements", "Yielded", and more. For a `get`, `Yielded` shows the real DOM node(s), which you can click to jump to them in the Elements tab.

This hover-pin-inspect cycle is part of what Cypress calls time travel; the deeper treatment (how snapshots work, DOM state replay, tips for CI) is **covered in depth on Friday**. Today it is enough to use it as the first step in diagnosing any failure.

### 3. Reading a Cypress failure message

A failing test shows a red error block. Learn its anatomy.

```
AssertionError: Timed out retrying after 4000ms: Expected to find element: `[data-test="error"]`, but never found it.

cypress/e2e/login.cy.js:12:30
  10 |     cy.get('[data-test="password"]').type('wrong');
  11 |     cy.get('[data-test="login-button"]').click();
> 12 |     cy.get('[data-test="error"]').should('be.visible');
     |        ^
  13 |   });
```

How to read it:

1. **Error type**: `AssertionError` (a check failed), `CypressError` (Cypress itself could not do something), or a regular JavaScript error (`TypeError: Cannot read properties of undefined`, often from your own code or the app).
2. **Message**: "Timed out retrying after 4000ms" means Cypress *tried repeatedly* and gave up. "Expected to find element ... but never found it" tells you the selector matched nothing.
3. **Code frame**: the file, line, and column in your spec, with surrounding lines and an arrow. Click it (in the runner) to **Open in IDE** if you have configured your editor.
4. **Print to console** button under the error: prints the full error object in DevTools.
5. **Stack trace** (collapsible): shows internal frames; usually you can ignore all but the first user frame.

#### 3.1 Common error messages and the usual causes

| Message (abridged) | Usual cause | First things to check |
|---|---|---|
| `Expected to find element: X, but never found it` | Wrong selector, element not yet rendered, inside iframe/shadow DOM, previous step failed silently | Pin the previous command; test selector in Selector Playground; check shadow DOM/iframe |
| `cy.click() failed because this element is not visible` | Hidden by CSS, collapsed menu, off-screen | Is a menu closed? Is the viewport too small? |
| `...is being covered by another element` | Modal backdrop, sticky header, cookie banner | Close the overlay; scroll offset |
| `...is disabled` | Button disabled until validation passes | Fill required fields first; assert enabled |
| `...can only be called on a single element. Your subject contained N elements` | Selector too broad | Narrow selector; `.first()`; `{ multiple: true }` |
| `...element is detached from the DOM` | App re-rendered between query and action | Re-query; avoid saving elements in variables |
| `expected X to equal Y` / `expected <div> to have text 'A', but the text was 'B'` | Genuine app difference, stale data, timing | Compare actual vs expected; check test data |
| `Timed out waiting for cy.wait() ... no request ever occurred` | Intercept registered too late/wrong URL pattern | Register before the action; log the real URL |
| `cy.visit() failed trying to load: ... status code 404/500` | Wrong baseUrl, server down | Open the URL in a normal browser |
| `The following error originated from your application code, not from Cypress` | App threw an uncaught JS exception | Check browser console; fix app or handle with `uncaught:exception` |
| `cy.task('x') failed ... must return a value or null` | Task returned `undefined` | Return `null` |
| `Cypress detected a cross-origin error` | Navigated to another origin | Use `cy.origin()` |

### 4. `cy.pause()`: stop and step

```js
it('pauses the test', () => {
  cy.visit('/');
  cy.get('[data-test="username"]').type('standard_user');
  cy.pause();                                       // test stops here
  cy.get('[data-test="password"]').type('secret_sauce');
  cy.get('[data-test="login-button"]').click();
});
```

When the runner reaches `cy.pause()`:

- The test halts, the **Command Log** shows a "Paused" banner with **Resume** (play) and **Next** (step) buttons.
- **Next** executes the next command only, then pauses again - classic *step-through* debugging.
- **Resume** continues until the next `cy.pause()` or the end of the test.
- While paused, you can interact with the app manually, open DevTools, inspect the DOM, or use the Selector Playground to check selectors for the upcoming steps.

You can also pause **on a specific element's subject** by chaining: `cy.get('form').pause()`. The subject is passed through.

`cy.pause()` is **only meaningful in `cypress open`**, where a person can click Next or Resume. In headless `cypress run` there is nobody to resume, so you should **remove pauses before committing** and certainly before CI. Treat it like `.only`: a temporary tool. (A linter rule or a CI grep for `cy.pause` is cheap insurance.)

Comparison: Playwright's `page.pause()` opens the Inspector with step-over and locator picking; `cy.pause()` is simpler, but the Command Log and DevTools supply the rest.

### 5. `cy.debug()` and `.debug()`

```js
cy.get('.inventory_item').debug();               // chained: prints the subject
cy.get('.inventory_item').first().debug();
cy.debug();                                      // as a parent: logs the previous subject chain
```

When executed, `.debug()`:

1. Logs a **Command** entry in the Command Log.
2. In the DevTools console, prints the **subject**, and then triggers the JavaScript **`debugger`** statement, so execution *pauses inside DevTools if DevTools is open*. While paused, the subject is available in the debugger's scope under the name `subject`.
3. Yields the same subject to the next command, so it can be inserted in the middle of a chain without changing behaviour.

Use it when you want to know "what exactly did `.first()` give me?". With DevTools open and paused, type `subject` into the console to examine it; use `$(subject)` or `subject[0]` to inspect the DOM node.

If DevTools is closed, `.debug()` just logs; the pause only occurs when DevTools is open.

### 6. The JavaScript `debugger` statement

`debugger;` is a standard JavaScript keyword that pauses execution *if DevTools is open*. In Cypress, put it **inside `.then()`**:

```js
cy.get('[data-test="inventory-item-price"]').then(($prices) => {
  debugger;                          // pause here; inspect $prices in the Scope panel
  const total = [...$prices].reduce((sum, el) => sum + Number(el.innerText.slice(1)), 0);
  expect(total).to.be.greaterThan(0);
});
```

How to use it:

1. Open the spec in `cypress open`, open DevTools (F12) **before** the test reaches the `debugger` line.
2. Re-run the test. Execution pauses; the Sources panel shows your code.
3. Inspect variables in **Scope**, hover over `$prices`, step with F10 (over) / F11 (into) / F8 (resume).
4. Remove the `debugger` afterwards (lint rule `no-debugger` helps).

A subtle point: Cypress runs the spec through a bundler, so the code in DevTools may appear in a "webpack://" source tree; the line numbers match with source maps enabled by default.

### 7. Printing values: `console.log`, `.then(console.log)`, `.should(console.log)`

Quick ways to see data:

```js
cy.get('.title').then(($el) => console.log('title element:', $el));
cy.get('.title').invoke('text').then(console.log);        // passes the text directly
cy.url().then(console.log);                               // prints the URL
cy.window().its('localStorage').then(console.log);
cy.request('/api/products').its('body').then(console.log);
```

- `.then(console.log)` passes the yielded value as the argument. It prints in the **browser** console (DevTools), not the terminal.
- `.should(console.log)` also prints, but **may print multiple times** because `.should` callbacks are retried; this can be useful to see how a value changes while waiting:

```js
cy.get('.count').should(($el) => {
  console.log('count currently:', $el.text());    // prints each retry
  expect($el.text()).to.eq('5');
});
```

- Remember the ordering trap: `console.log('x')` directly in the test body prints **before** commands run. Use `cy.then(() => console.log('x'))` or place it in a callback.

Another way to inspect any command's output without writing code: **click the command in the Command Log** and read the DevTools console ("Print to console" behaviour).

### 8. Breadcrumbs: `cy.log()` (brief)

```js
cy.log('Starting checkout for user', username);
cy.log('**bold** text and `code`');           // limited markdown
```

`cy.log(message)` adds a line to the Command Log, in order with other commands. It is useful as a "section marker" when a test is long or when a helper function runs several commands: the Command Log gets a readable story. It does not appear in the terminal output of `cypress run`. Logging strategies (custom `Cypress.log`, log levels, sending logs to the terminal) are **covered in depth on Friday**.

To print from the test to the **terminal** now, use a task:

```js
// cypress.config.js
setupNodeEvents(on, config) {
  on('task', {
    log(message) {
      console.log(message);
      return null;
    },
  });
  return config;
}
```

```js
cy.task('log', 'Reached checkout step two');
```

Tasks run in Node, so the message appears in the terminal where Cypress is running, which is the only place you will see output in CI.

### 9. Taking evidence (brief)

Cypress can capture screenshots and video:

```js
cy.screenshot('after-login');          // saves cypress/screenshots/<spec>/after-login.png
```

By default, `cypress run` takes a **screenshot automatically when a test fails**. Video recording is off by default in Cypress 13 and can be turned on with `video: true`. The full treatment of screenshots and video is **covered in depth on Friday**; for debugging today, just know that CI evidence exists and where it lands (`cypress/screenshots`, `cypress/videos`).

### 10. DevTools and the Selector Playground

Because Cypress runs in a normal browser, all the DevTools you know work:

- **Elements**: inspect the real DOM of your app inside the app iframe. (Right-click an element in the app preview and choose Inspect.)
- **Console**: run `document.querySelectorAll('[data-test="x"]').length` to test a selector. Note: the console's context drop-down must be set to **"Your project: <name>"** (the app iframe) rather than "top" to access the app's `document` and `window`. This surprises many people: if your `document.querySelector` returns null, check the context.
- **Network**: see all requests; confirm the URLs you need for `cy.intercept` patterns.
- **Sources**: place breakpoints in the spec code.
- **Selector Playground** (target icon in the app toolbar): click an element and Cypress proposes a selector and shows match counts (covered in "Element location").

### 11. Debug-friendly workflow habits

1. **Focus**: add `.only` to the failing test (remove before commit).
2. **Reproduce in `open`**: watch it fail; hover commands to find the last good state.
3. **Slow down the interesting part**: `cy.pause()` before the failing command.
4. **Inspect**: pin the failing command; read "Yielded", "Elements", and "Options" in the console.
5. **Reproduce `run` failures**: `npx cypress run --headed --no-exit --browser chrome --spec "path/to/spec.cy.js"`. Because `run` mode enables retries, set `--config retries=0` while debugging so the first failure is visible:

```bash
npx cypress run --spec "cypress/e2e/cart.cy.js" --headed --no-exit --config retries=0
```

6. **Isolate variables**: is it the selector, the data, the timing, or the app? Change one thing at a time.
7. **Check the network**: look for the XHR rows in the Command Log; a 401 or 500 often explains a missing element.
8. **Compare with a manual run**: do the same steps by hand in a normal browser window.
9. **Verify the environment**: base URL, test data, feature flags, viewport, browser, Cypress version.
10. **Write down the fix** in the test (comment) or a ticket when it exposes a product bug.

### 12. Debug environment variables (advanced, for CI problems)

When Cypress itself misbehaves (binary will not start, proxy errors), enable verbose logs:

```bash
DEBUG=cypress:* npx cypress run          # Linux/macOS: very verbose Cypress internals
DEBUG=cypress:server:browsers npx cypress run   # narrower scope
```

On Windows PowerShell: `$env:DEBUG="cypress:*"; npx cypress run`. The output is large; narrow the namespace. Also, `npx cypress verify` and `npx cypress info` diagnose installation problems.

---

## Code Examples

### Example 1: Step through a login with `cy.pause`

```js
describe('Debugging a login', () => {
  it('pauses before the click to inspect the form', () => {
    cy.visit('/');
    cy.get('[data-test="username"]').type('standard_user');
    cy.get('[data-test="password"]').type('secret_sauce');
    cy.pause();                                         // inspect the filled form
    cy.get('[data-test="login-button"]').click();
    cy.url().should('include', '/inventory.html');
  });
});
```

**Explanation:**

1. The first three commands run normally.
2. At `cy.pause()`, the test stops with the form filled. In the app preview you can manually look at the page.
3. Click **Next** to run `click()`, then **Next** again for `url().should(...)`; or **Resume** to finish.
4. Remove `cy.pause()` when done.

### Example 2: Inspect an element with `.debug()`

```js
it('inspects a product card', () => {
  cy.login();
  cy.visit('/inventory.html');
  cy.get('[data-test="inventory-item"]')
    .first()
    .debug()                                        // open DevTools, then check `subject`
    .find('[data-test="inventory-item-price"]')
    .should('contain.text', '$');
});
```

**Explanation:** `.debug()` sits between `.first()` and `.find()`, passing the subject through unchanged. With DevTools open, execution pauses and you can examine the first card's DOM. When resumed, the test continues to `find` the price.

### Example 3: `debugger` inside `.then()` and printing

```js
it('computes the total of all prices', () => {
  cy.login();
  cy.visit('/inventory.html');
  cy.get('[data-test="inventory-item-price"]').then(($prices) => {
    const values = [...$prices].map((el) => Number(el.innerText.replace('$', '')));
    console.log('prices:', values);                  // prints an array in DevTools
    debugger;                                        // optional breakpoint
    const total = values.reduce((sum, n) => sum + n, 0);
    cy.log(`Total of all items: ${total.toFixed(2)}`);
    expect(total).to.be.greaterThan(0);
  });
});
```

**Line-by-line:**

1. `cy.get(...).then(($prices) => { ... })` runs the callback after the elements are found.
2. `[...$prices]` converts the jQuery collection to an array of DOM nodes; `.map` extracts numbers.
3. `console.log('prices:', values)` writes to the **browser console**.
4. `debugger;` pauses if DevTools is open.
5. `reduce` sums the array (start value `0`).
6. `cy.log(...)` adds a line to the Command Log (a Cypress command, allowed inside `.then()`); `.toFixed(2)` formats with two decimals.
7. `expect(total)...` is a Chai assertion.

### Example 4: Watching a value change during retries

```js
it('shows how the badge text evolves while Cypress retries', () => {
  cy.login();
  cy.visit('/inventory.html');
  cy.get('[data-test="add-to-cart-sauce-labs-backpack"]').click();
  cy.get('[data-test="shopping-cart-badge"]').should(($badge) => {
    console.log('badge text now:', $badge.text());      // may print several times
    expect($badge.text()).to.eq('1');
  });
});
```

**Explanation:** Because `.should(callback)` re-runs until it passes or times out, you see each attempt in the console, a good way to understand timing problems.

### Example 5: Debugging a network issue

```js
it('diagnoses a missing product list', () => {
  cy.intercept('GET', '**/api/products*').as('getProducts');
  cy.visit('/shop');                                   // illustrative page
  cy.wait('@getProducts').then((interception) => {
    console.log('request:', interception.request.url);
    console.log('status:', interception.response.statusCode);
    console.log('body:', interception.response.body);
  });
  cy.get('.product').should('have.length.greaterThan', 0);
});
```

**Explanation:** the interception object contains the request and response, which tells you whether the UI failure is caused by the data (an empty body, 500 status) rather than by the selector. If `cy.wait` itself times out, either the URL pattern is wrong or the app never made the call; log the real URL in the Network tab and adjust the glob.

### Example 6: Reproducing a CI failure locally

```bash
npx cypress run \
  --browser chrome \
  --headed \
  --no-exit \
  --spec "cypress/e2e/cart/cart.cy.js" \
  --config retries=0,viewportWidth=1280,viewportHeight=720
```

**Explanation:** matches CI's browser and viewport, shows the window, keeps it open at the end, runs only the failing spec, and disables retries so the first failure is not masked. The backslashes are Linux/macOS line continuations; on Windows use `^` (cmd) or a backtick (PowerShell), or put it all on one line.

---

## Real-World Scenarios

1. **The "it works on my machine" failure.** A test passes locally but fails in CI with "element not visible." The engineer reproduces with `--headed --no-exit --config viewportWidth=1000` and discovers the CI viewport is narrower, collapsing the menu. The fix is a `cy.viewport` and a config default.
2. **Intermittent detached element.** The dashboard re-renders when data arrives. The test failed once in twenty runs. Using `.should(callback)` with `console.log` showed the value flipping between "Loading" and "42". The fix: assert the final state with `.should('have.text', '42')`, and wait for the network alias before interacting.
3. **A 500 hidden behind a missing element.** `cy.get('.order-row')` never appears. The Command Log shows `(xhr) GET 500 /api/orders`. The bug is in the backend, not the selector; the engineer attaches the Command Log screenshot to the bug report.
4. **Stuck in the queue.** A junior engineer put `debugger;` at the top of the test and found a blank page. Moving it inside `.then()` after the `get` gave the live DOM.
5. **A forgotten `cy.pause()`.** CI hung (or in some setups, exited unexpectedly) because a `cy.pause()` was committed. The team added a lint check for `cy.pause`, `.only`, and `debugger`.

---

## Common Pitfalls and Best Practices

**Pitfall 1: Placing `debugger`/`console.log` in the test body.** They run before the commands. Use `.then()`.

**Pitfall 2: Forgetting DevTools context.** The console defaults to the "top" frame (the Cypress runner), not your app. Switch to "Your project".

**Pitfall 3: Leaving `cy.pause()`, `.debug()`, `debugger`, or `.only` in committed code.** Lint for them.

**Pitfall 4: Chasing flaky failures with `cy.wait(5000)`.** Instead, find what the app is waiting for (a request, a render) and wait for that.

**Pitfall 5: Reading only the last line of the error.** Read the whole message and the code frame; the first line usually states the cause.

**Pitfall 6: Debugging with retries on.** In `run` mode, a test that fails the first time and passes on retry may look green. Set `retries=0` while investigating, and keep a list of tests that needed retries.

**Pitfall 7: Assuming `cy.log` prints to the terminal.** It does not. Use `cy.task('log')`.

**Pitfall 8: Changing many things at once.** Alter one variable per run; otherwise you will not know what fixed it.

**Pitfall 9: Treating `{ force: true }` as a debugging fix.** It can hide a real defect; use it only to diagnose, then find the true cause.

**Best practices**

- Start with the Command Log and snapshots; they answer most "what happened?" questions.
- Use `cy.pause()` for stepping, `.debug()` for subjects, `debugger` for code, `.then(console.log)` for quick values.
- Keep debug aids out of commits (lint rules).
- Reproduce CI failures with the same browser, viewport, and spec.
- Record what you learned in the test as a comment, or in the defect report.
- When you suspect the app, check the browser console and the network tab before touching the test.

---

## Mini Practice Exercises

**Exercise 1 - Command Log tour.**
Run any passing spec in `cypress open`. Hover over each command, then click one to pin it. Open DevTools and read the console output. Write down three pieces of information you can see (for example the Yielded element, the hit point of a click, the subject).

**Exercise 2 - Step through.**
Add `cy.pause()` before the click in a login test. Step with **Next**, then **Resume**. What is the difference?

*Answer:* Next runs one command and pauses again; Resume runs until the next pause or the end.

**Exercise 3 - Put it in the right place.**
Fix this code so the `debugger` pauses after the element is found:

```js
cy.get('.inventory_item');
debugger;
```

*Solution:*

```js
cy.get('.inventory_item').then(($items) => {
  debugger;
});
```

**Exercise 4 - Break it on purpose.**
Change a selector to something wrong (`[data-test="usrname"]`). Run and read the full error. Identify: error type, message, selector, line number. Fix it using the Selector Playground.

**Exercise 5 - Network detective.**
Using `https://example.cypress.io/commands/network-requests`, intercept `GET **/comments/*`, click the "Get Comment" button, and `console.log` the response status and body from the interception object.

**Exercise 6 - Terminal log.**
Add a `log` task to `cypress.config.js` and call it from a test. Run with `cypress run` and confirm the message appears in your terminal but not in the browser console.

**Exercise 7 - Compare.**
For one failure in your Project 1 Playwright suite (or a deliberately broken test), write down how you would debug it in Playwright (Inspector, trace) and how you would debug the same failure in Cypress. Which steps are similar? Add your answer to the comparison note.

---

## Summary / Key Takeaways

- Debugging Cypress means respecting the **command queue**: plain JavaScript runs immediately, commands run later. Put debugging code in `.then()` or use Cypress's own tools.
- The **Command Log** is the first stop: hover for snapshots, click to pin and print command details in DevTools.
- Read errors fully: type, message, selector, code frame. Many messages tell you exactly which actionability check failed.
- `cy.pause()` stops the test with Next/Resume stepping; `.debug()` prints the subject and pauses if DevTools is open; `debugger` inside `.then()` gives breakpoint debugging; `.then(console.log)` prints values.
- `cy.log()` writes to the Command Log; `cy.task('log')` writes to the terminal. A fuller treatment of logging is **covered in depth on Friday**.
- Screenshots and video exist as evidence, and time-travel snapshots are the heart of the Cypress debugging story; both are **covered in depth on Friday**.
- Reproduce CI failures with `--headed --no-exit`, the same browser and viewport, and `retries=0`.
- Remove `cy.pause()`, `.debug()`, `debugger`, and `.only` before committing.
- The same investigative mindset applies in Playwright and Cypress: reproduce, isolate, inspect, change one thing at a time.

---

## External Resources

- Cypress Documentation - Debugging: https://docs.cypress.io/app/guides/debugging
- Cypress Documentation - `cy.pause()`: https://docs.cypress.io/api/commands/pause
- Cypress Documentation - `.debug()`: https://docs.cypress.io/api/commands/debug
