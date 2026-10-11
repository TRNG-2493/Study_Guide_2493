# Weekly Knowledge Check: [Week5-Advanced-Web-Automation] - Thursday: Cypress

**Scope:** Cypress architecture and setup, browser management, writing Cypress tests, element location, assertions and annotations, test selection, fixtures and custom commands, element interaction, and debugging actions. Several questions compare Cypress with the Playwright (Python) work from Monday to Wednesday.

**How to use this quiz:** Try each question before opening the solution. Every question has a hidden solution block with the correct answer and the reasoning.

- Part 1: Multiple Choice (Questions 1-28)
- Part 2: True/False on Common Misconceptions (Questions 29-40)
- Part 3: Code Prediction (Questions 41-54)
- Part 4: Fill-in-the-Blank (Questions 55-66)

---

## Part 1: Multiple Choice

### 1. Where does Cypress test code run, compared with Playwright?
- [ ] A) Outside the browser, in a separate Node process that sends commands over a network protocol, exactly like Playwright
- [ ] B) Only in a Node.js process, which controls the browser through the WebDriver protocol
- [ ] C) Inside the browser, in an iframe next to the application under test, with a separate Node process for file-system and system-level work
- [ ] D) On Cypress Cloud servers, which stream each command to your local browser

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** C) Inside the browser, in an iframe next to the application under test, with a separate Node process for file-system and system-level work

**Explanation:** Cypress has two cooperating halves: a Node.js process (config, proxy, files, tasks) and the browser page, where your spec iframe and the application iframe share the same run loop. Playwright, by contrast, runs outside the browser and remote-controls it.
- **Why others are wrong:**
  - A) That describes Playwright, not Cypress.
  - B) Spec code runs in the browser, not in Node, and the lesson does not describe Cypress as a WebDriver tool.
  - D) Cypress Cloud is an optional paid product for recording and parallelisation; tests still run in your own browser.
</details>

---

### 2. Which file runs automatically before every spec file and is the usual place for global hooks and plugin imports?
- [ ] A) `cypress/support/e2e.js`
- [ ] B) `cypress/fixtures/example.json`
- [ ] C) `cypress.config.js`
- [ ] D) `cypress/e2e/first.cy.js`

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** A) `cypress/support/e2e.js`

**Explanation:** The support file (`supportFile` in config, `cypress/support/e2e.js` by default) is loaded before each spec, so global `beforeEach` hooks and imports such as `./commands` belong there.
- **Why others are wrong:**
  - B) A fixture is a static data file; it is only loaded when a test calls `cy.fixture()`.
  - C) The config file is read once by the Node process at startup; it is not executed in the browser before each spec.
  - D) A spec file is one of the tests themselves, not shared setup.
</details>

---

### 3. A test needs a freshly seeded user in a database, but spec code runs inside the browser and cannot talk to the database directly. What is the Cypress-idiomatic solution?
- [ ] A) `require` a Node database client at the top of the spec, because specs run in Node anyway
- [ ] B) Use `await cy.get(...)` to read the database through the page
- [ ] C) Seed the data by hand, because Cypress can never reach a database
- [ ] D) Register a task in `setupNodeEvents` that uses the Node DB client, then call it from the spec with `cy.task('seedUser', {...})`

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** D) Register a task in `setupNodeEvents` that uses the Node DB client, then call it from the spec with `cy.task('seedUser', {...})`

**Explanation:** `setupNodeEvents` runs in Node, so tasks registered there can do anything Node can; `cy.task()` is the bridge from the browser-side spec to that Node code.
- **Why others are wrong:**
  - A) Specs run in the browser, not in Node, so a Node database client is not available there.
  - B) Cypress commands are not Promises, and `cy.get` queries the DOM, not a database.
  - C) The Node side of Cypress can reach a database; that is exactly what tasks are for.
</details>

---

### 4. A link has `target="_blank"` and opens a new tab. Cypress cannot control a second tab. What is a lesson-approved workaround?
- [ ] A) Call `cy.switchToTab(1)` to move to the new tab
- [ ] B) Remove the `target` attribute (`cy.get('a').invoke('removeAttr', 'target').click()`) or read the `href` and `cy.visit()` it
- [ ] C) Use `context.expect_page()` just like in Playwright
- [ ] D) Add `{ force: true }` to the click so Cypress follows the new tab

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** B) Remove the `target` attribute (`cy.get('a').invoke('removeAttr', 'target').click()`) or read the `href` and `cy.visit()` it

**Explanation:** Because the test runs inside the single tab it controls, the usual workaround is to make the link open in the same tab, or to visit its URL directly.
- **Why others are wrong:**
  - A) There is no tab-switching command in Cypress; multi-tab is a stated limitation.
  - C) `expect_page` is a Playwright API and has no direct Cypress equivalent.
  - D) `force` only skips actionability checks; it does not give Cypress control of another tab.
</details>

---

### 5. Which browser is bundled inside Cypress itself and is used by default for `cypress run`?
- [ ] A) Chrome
- [ ] B) Firefox
- [ ] C) WebKit
- [ ] D) Electron

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** D) Electron

**Explanation:** Electron ships inside the Cypress binary, needs no separate installation, and is the default headless browser for `cypress run`.
- **Why others are wrong:**
  - A) Chrome must already be installed on the machine; Cypress does not download it.
  - B) Firefox must also be installed on the machine.
  - C) WebKit support is experimental, needs `experimentalWebKitSupport: true` plus the `playwright-webkit` package, and is not the default.
</details>

---

### 6. How does Cypress obtain browsers, compared with Playwright?
- [ ] A) Cypress downloads its own patched Chromium, Firefox, and WebKit, just like `playwright install`
- [ ] B) Cypress downloads Chrome automatically the first time you run `cypress open`
- [ ] C) Cypress uses browsers already installed on your machine (plus bundled Electron), whereas Playwright downloads its own browser builds
- [ ] D) Cypress only ever runs in Electron

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** C) Cypress uses browsers already installed on your machine (plus bundled Electron), whereas Playwright downloads its own browser builds

**Explanation:** When you run `cypress open`, Cypress scans the machine for installed browsers; this is why the Chrome version on a laptop can differ from CI. Playwright's downloaded builds behave the same everywhere.
- **Why others are wrong:**
  - A) That is Playwright's model.
  - B) Cypress never downloads Chrome; if Chrome is not installed it simply will not appear in the list.
  - D) Cypress also supports Chrome, Chromium, Edge, and Firefox when they are installed.
</details>

---

### 7. A test passes in `cypress open` but fails in CI with `cypress run`. Which command is the best way to reproduce the CI failure locally?
- [ ] A) `npx cypress run --browser chrome --headed --no-exit --spec "cypress/e2e/cart/cart.cy.js" --config retries=0`
- [ ] B) `npx cypress open`, then rerun the test until it fails
- [ ] C) Add `cy.wait(5000)` before every command and push again
- [ ] D) Switch the CI job to `cypress open` so it behaves like the local run

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** A) `npx cypress run --browser chrome --headed --no-exit --spec "cypress/e2e/cart/cart.cy.js" --config retries=0`

**Explanation:** This uses `run` mode with the same browser as CI, shows the window, keeps it open at the end (`--no-exit`), targets only the failing spec, and turns off retries so the first failure is not masked.
- **Why others are wrong:**
  - B) `open` mode differs from `run` (watch mode, different retry defaults), so it may never reproduce the failure.
  - C) Fixed sleeps are an anti-pattern and do not help you investigate.
  - D) `cypress open` needs a display and a human, so it does not work in CI.
</details>

---

### 8. Why does `const btn = cy.get('#login-button'); btn.click();` not give you the DOM element in `btn`?
- [ ] A) Because element variables must start with `$` to hold a jQuery object
- [ ] B) Because `cy.get` does not run immediately: it adds a command to a queue and returns a chainable, not the element
- [ ] C) Because `cy.get` returns a Promise that you must `await`
- [ ] D) Because `cy.get` returns the selector string until `.click()` is called

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** B) Because `cy.get` does not run immediately: it adds a command to a queue and returns a chainable, not the element

**Explanation:** Cypress commands are enqueued while the test body runs and executed afterwards, one at a time. To work with the real value you use `.then()`, an alias, or an assertion.
- **Why others are wrong:**
  - A) The `$` prefix is only a naming convention for jQuery objects.
  - C) A Chainable looks like a promise but is not one; using `async/await` with Cypress commands does not work as expected.
  - D) `cy.get` yields DOM elements to the next command; it does not return a selector string.
</details>

---

### 9. A page loads its product list from `/api/products`. Which approach best waits for the data before asserting on the list?
- [ ] A) `cy.wait(5000)` and then assert
- [ ] B) Register `cy.intercept(...)` after `cy.visit()` and then wait on it
- [ ] C) Register `cy.intercept('GET', '**/api/products*').as('getProducts')` before triggering the request, then `cy.wait('@getProducts')`
- [ ] D) Mark the test `async` and `await` the request

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** C) Register `cy.intercept('GET', '**/api/products*').as('getProducts')` before triggering the request, then `cy.wait('@getProducts')`

**Explanation:** Waiting on a network alias waits for the real event rather than a guessed duration. The intercept must be registered before the action that triggers the request.
- **Why others are wrong:**
  - A) A fixed sleep slows every run and is still flaky if the app is slower than expected.
  - B) If the intercept is registered after the request has already been made, the request is gone and the wait would time out.
  - D) Cypress commands are not Promises, so `async/await` is not the right tool.
</details>

---

### 10. What does `cy.session()` do, and which Playwright feature is its closest analogue?
- [ ] A) It records a video of the test run; analogous to Playwright's video recording
- [ ] B) It keeps the same page open between tests; analogous to reusing a `Page` object
- [ ] C) It turns off test isolation for the whole project; analogous to `--workers=1`
- [ ] D) It caches cookies, localStorage, and sessionStorage after a first login and restores them in later tests; analogous to Playwright's `storage_state`

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** D) It caches cookies, localStorage, and sessionStorage after a first login and restores them in later tests; analogous to Playwright's `storage_state`

**Explanation:** `cy.session(id, setup, options)` runs the setup (a login) once per cache key and restores the saved browser state afterwards, skipping the UI login. Cypress clears the page after it, so each test still calls `cy.visit()`.
- **Why others are wrong:**
  - A) Video recording is a separate feature (covered Friday).
  - B) The page is not kept open; test isolation still resets it to `about:blank`.
  - C) `cy.session` works with test isolation on; it restores state rather than disabling isolation.
</details>

---

### 11. Which selector is the most resilient to styling and copy changes?
- [ ] A) `.btn.btn-lg.btn-primary`
- [ ] B) `[data-test="submit"]`
- [ ] C) `div > div:nth-child(3) > span`
- [ ] D) `button`

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** B) `[data-test="submit"]`

**Explanation:** Dedicated test attributes exist only for automation, so styling, layout, and wording changes do not affect them. The Cypress best-practices guide recommends `data-cy`, `data-test`, or `data-testid`.
- **Why others are wrong:**
  - A) Classes serve styling and change often (or are hashed by CSS-in-JS).
  - C) Positional chains break at the first layout change.
  - D) A bare tag name is ambiguous and usually matches many elements.
</details>

---

### 12. What does `cy.contains('li', 'Apple')` yield?
- [ ] A) The `li` element that contains the text "Apple" (the element matching the selector)
- [ ] B) The deepest descendant of any `li` that contains the text, such as a nested `span`
- [ ] C) Every `li` on the page
- [ ] D) The string "Apple"

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** A) The `li` element that contains the text "Apple" (the element matching the selector)

**Explanation:** With a selector plus text, `cy.contains` yields the matching element of that selector, which makes it ideal for rows and cards. Without a selector it yields the deepest element containing the text.
- **Why others are wrong:**
  - B) That is the behaviour of `cy.contains('Apple')` without a selector.
  - C) `cy.contains` yields the first matching element, not every element.
  - D) It yields a DOM element, not a string.
</details>

---

### 13. How do Playwright and Cypress differ in handling open Shadow DOM?
- [ ] A) Both pierce shadow roots by default
- [ ] B) Cypress pierces by default, while Playwright needs an option
- [ ] C) Playwright locators pierce open shadow roots by default; Cypress needs `includeShadowDom: true` or `.shadow()`
- [ ] D) Neither tool can reach into a shadow root

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** C) Playwright locators pierce open shadow roots by default; Cypress needs `includeShadowDom: true` or `.shadow()`

**Explanation:** By default Cypress does not search inside shadow roots. You can use `.shadow()` per command, `{ includeShadowDom: true }` per command, or `includeShadowDom: true` globally in the config.
- **Why others are wrong:**
  - A) Cypress does not pierce by default.
  - B) This reverses the two tools.
  - D) Both can; Cypress just needs an explicit option.
</details>

---

### 14. You liked Playwright's `get_by_role("button", name="Login")`. What is the Cypress equivalent?
- [ ] A) A built-in `cy.getByRole('button', { name: 'Login' })`
- [ ] B) `cy.contains('role=button')`
- [ ] C) `cy.get('@button')`
- [ ] D) There is no built-in role locator; the `@testing-library/cypress` plugin provides `cy.findByRole('button', { name: /login/i })`

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** D) There is no built-in role locator; the `@testing-library/cypress` plugin provides `cy.findByRole('button', { name: /login/i })`

**Explanation:** Cypress's core queries are CSS-based (`cy.get`) and text-based (`cy.contains`). Role and label locators come from the Testing Library plugin after `import '@testing-library/cypress/add-commands'`.
- **Why others are wrong:**
  - A) `cy.getByRole` is not a built-in command.
  - B) `cy.contains` matches text, not Playwright-style `role=` selectors.
  - C) `cy.get('@name')` retrieves an alias, not an element by role.
</details>

---

### 15. Which of these assertions is retried until it passes or the timeout is reached?
- [ ] A) `cy.get('.count').then(($el) => { expect($el.text()).to.equal('5'); })`
- [ ] B) `cy.get('.count').then(($el) => { assert.equal($el.text(), '5'); })`
- [ ] C) `cy.get('.count').should('have.text', '5')`
- [ ] D) `expect(total).to.equal(15)` on a plain variable

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** C) `cy.get('.count').should('have.text', '5')`

**Explanation:** Implicit assertions chained with `.should()` retry together with the preceding query. Explicit assertions (`expect`, `assert`) run once.
- **Why others are wrong:**
  - A) An `expect` inside `.then()` runs once, when the callback executes.
  - B) `assert` is also an explicit assertion and does not retry.
  - D) A plain-value `expect` has nothing to re-query; it simply runs once.
</details>

---

### 16. A spinner should disappear after a save. Which assertion is correct?
- [ ] A) `cy.get('.spinner').should('not.be.visible')`
- [ ] B) `cy.get('.spinner').should('not.exist')`
- [ ] C) `cy.get('.spinner').should('have.length', 1)`
- [ ] D) `cy.wait(2000)` followed by `cy.get('.spinner')`

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** B) `cy.get('.spinner').should('not.exist')`

**Explanation:** `should('not.exist')` retries until the element is gone from the DOM. `not.be.visible` is meant for elements that are still in the DOM but hidden.
- **Why others are wrong:**
  - A) `not.be.visible` fails if the element does not exist in the DOM, which is exactly the end state you want.
  - C) That asserts the spinner is still there, the opposite of the goal.
  - D) A fixed wait is an anti-pattern, and a bare `cy.get` would then fail if the spinner is gone.
</details>

---

### 17. Which statement about `before()` and test isolation is correct?
- [ ] A) A login performed in `before()` persists into every test of the suite
- [ ] B) Cypress throws an error because `before()` cannot contain `cy` commands
- [ ] C) State from `before()` persists only if you write the hook as an arrow function
- [ ] D) With test isolation (default since Cypress 12), cookies, storage, and the page are reset before each test, so per-test browser setup belongs in `beforeEach` or `cy.session`

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** D) With test isolation (default since Cypress 12), cookies, storage, and the page are reset before each test, so per-test browser setup belongs in `beforeEach` or `cy.session`

**Explanation:** Because Cypress clears cookies, localStorage, sessionStorage, and navigates to `about:blank` before each `it`, a login or `cy.visit` done once in `before` will not carry into the tests.
- **Why others are wrong:**
  - A) That was the pre-12 expectation; with isolation on, state does not persist.
  - B) `before()` may use `cy` commands; the problem is persistence, not syntax.
  - C) Arrow versus regular function affects only `this`, not browser state.
</details>

---

### 18. What does this line do? `it('supports gift wrapping');`
- [ ] A) Declares a pending test (a placeholder with no callback) that is reported as pending
- [ ] B) Causes a syntax error because `it` needs a function
- [ ] C) Creates a test that passes because it contains no failing command
- [ ] D) Creates a test that fails because it has no assertions

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** A) Declares a pending test (a placeholder with no callback) that is reported as pending

**Explanation:** In Mocha, a test with no function is pending. Teams use this as a visible to-do list of planned tests.
- **Why others are wrong:**
  - B) It is valid Mocha syntax.
  - C) It is not executed at all, so it is reported pending rather than passing.
  - D) Nothing runs, so nothing fails.
</details>

---

### 19. Which command runs exactly two spec files with the `--spec` flag?
- [ ] A) `npx cypress run --spec "cypress/e2e/login.cy.js cypress/e2e/checkout.cy.js"`
- [ ] B) `npx cypress run --spec "cypress/e2e/login.cy.js; cypress/e2e/checkout.cy.js"`
- [ ] C) `npx cypress run --spec "cypress/e2e/login.cy.js,cypress/e2e/checkout.cy.js"`
- [ ] D) `npx cypress run --spec cypress/e2e/login.cy.js + cypress/e2e/checkout.cy.js`

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** C) `npx cypress run --spec "cypress/e2e/login.cy.js,cypress/e2e/checkout.cy.js"`

**Explanation:** Multiple specs are separated by a comma inside a single quoted string; quoting also stops the shell from expanding globs.
- **Why others are wrong:**
  - A) Space-separated paths are not the documented format.
  - B) A semicolon separator is used by `grep` title filters, not by `--spec`.
  - D) The `+` symbol is for AND in `grepTags`, and the paths are unquoted.
</details>

---

### 20. What does `npx cypress run --env grepTags=@smoke+-@slow` select (with `@cypress/grep`)?
- [ ] A) Tests tagged `@smoke` or not tagged `@slow`
- [ ] B) Tests tagged `@smoke` that are not tagged `@slow`
- [ ] C) Tests tagged `@smoke` or tagged `@slow`
- [ ] D) Every test except those tagged `@smoke` or `@slow`

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** B) Tests tagged `@smoke` that are not tagged `@slow`

**Explanation:** In `grepTags`, `+` means AND, `-` means NOT, and a space means OR. So `@smoke+-@slow` is "smoke AND NOT slow".
- **Why others are wrong:**
  - A) That would need an OR, which is written with a space.
  - C) OR between the two tags would be `"@smoke @slow"`.
  - D) Excluding both would be a different expression; here `@smoke` is required.
</details>

---

### 21. `npx cypress run --env grep="adds an item",burn=20` is closest to which Playwright feature?
- [ ] A) `--retries 20`, because both rerun failing tests
- [ ] B) `--headed`, because both show the browser
- [ ] C) `-k "adds an item"` only, because `burn` is ignored
- [ ] D) `--repeat-each 20`, because both repeat the matching test many times to expose flakiness

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** D) `--repeat-each 20`, because both repeat the matching test many times to expose flakiness

**Explanation:** `burn=N` repeats each matching test N times. If any repetition fails you have evidence of flakiness.
- **Why others are wrong:**
  - A) Retries only rerun a test after it fails; `burn` repeats tests regardless of outcome.
  - B) `--headed` controls visibility and has nothing to do with repeating.
  - C) The `grep` part resembles `-k`, but `burn` is a real option, not ignored.
</details>

---

### 22. In Cypress, what is a "fixture"?
- [ ] A) A static data file in `cypress/fixtures`, loaded with `cy.fixture()`
- [ ] B) A function injected into tests by parameter name, with teardown after `yield`
- [ ] C) An isolated browser context created for each test
- [ ] D) A custom command registered with `Cypress.Commands.add`

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** A) A static data file in `cypress/fixtures`, loaded with `cy.fixture()`

**Explanation:** A Cypress fixture is data (JSON, images, CSV text). The Playwright/pytest meaning of "fixture" is a dependency-injection mechanism; Cypress has no such injection system.
- **Why others are wrong:**
  - B) That describes a Playwright/pytest fixture.
  - C) That describes Playwright's `BrowserContext`, which Cypress replaces with test isolation.
  - D) Custom commands are the Cypress tool that fills the role of Playwright's custom fixtures, not the fixtures themselves.
</details>

---

### 23. You want one `it` generated per row of a JSON file of login cases. Which approach works?
- [ ] A) Call `cy.fixture('login-cases')` at the top level of `describe` and create `it` blocks inside `.then()`
- [ ] B) Call `cy.fixture` inside `beforeEach` and register new `it` blocks there
- [ ] C) `require('../fixtures/login-cases.json')` at the top of the spec and loop with `forEach` to call `it(...)` for each row
- [ ] D) Wrap the JSON in `cy.wrap()` and call `it` inside `.then()`

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** C) `require('../fixtures/login-cases.json')` at the top of the spec and loop with `forEach` to call `it(...)` for each row

**Explanation:** `describe`/`it` blocks are registered synchronously at load time, so the data must also be available synchronously. `require` or `import` loads JSON at that moment. `cy.fixture()` is a queued command that resolves too late.
- **Why others are wrong:**
  - A) `cy.fixture` is asynchronous, so the `it` blocks would be created too late.
  - B) Tests cannot be registered from inside a hook at run time.
  - D) `cy.wrap` is also a queued command, so the same timing problem applies.
</details>

---

### 24. Which definition creates a custom command that **requires** a previous DOM element subject (a child command)?
- [ ] A) `Cypress.Commands.add('typeAndEnter', (text) => { ... })`
- [ ] B) `Cypress.Commands.overwrite('typeAndEnter', (originalFn, text) => { ... })`
- [ ] C) `Cypress.Commands.add('typeAndEnter', { prevSubject: 'optional' }, (subject, text) => { ... })`
- [ ] D) `Cypress.Commands.add('typeAndEnter', { prevSubject: 'element' }, (subject, text) => { ... })`

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** D) `Cypress.Commands.add('typeAndEnter', { prevSubject: 'element' }, (subject, text) => { ... })`

**Explanation:** `prevSubject: 'element'` makes the command a child command that must be chained off a DOM element; the subject arrives as the first callback argument.
- **Why others are wrong:**
  - A) With no options the command is a parent command that starts a chain.
  - B) `overwrite` replaces an existing command's behaviour; it does not define a new child command.
  - C) `'optional'` creates a dual command that works with or without a previous subject.
</details>

---

### 25. What does `{ force: true }` do on `.click()`?
- [ ] A) It makes Cypress retry the click until it works, ignoring the timeout
- [ ] B) It skips actionability checks (visible, covered, disabled, animating) and fires the event immediately
- [ ] C) It turns off the default command timeout for the whole test
- [ ] D) It disables test isolation for that click

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** B) It skips actionability checks (visible, covered, disabled, animating) and fires the event immediately

**Explanation:** `force: true` is useful for legitimately hidden-but-functional inputs and as a diagnostic, but it can hide real usability bugs, since a user cannot click a covered button. Use it rarely, with a comment.
- **Why others are wrong:**
  - A) It does the opposite of waiting: it skips the waiting checks.
  - C) The timeout setting is unrelated.
  - D) Test isolation concerns state between tests, not individual actions.
</details>

---

### 26. A navigation menu opens only on CSS `:hover`. Cypress has no `.hover()` command. Which statement is correct?
- [ ] A) `.trigger('mouseover')` will not activate CSS `:hover`; use `cypress-real-events` (`realHover()`, Chromium-based browsers only), or reveal the menu with `.invoke('show')`, or use `{ force: true }` on the hidden item
- [ ] B) Use the built-in `.hover()` command added in Cypress 12
- [ ] C) `.trigger('mouseover')` always activates CSS `:hover` because it fires a real mouse event
- [ ] D) `.rightclick()` triggers `:hover` as a side effect

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** A) `.trigger('mouseover')` will not activate CSS `:hover`; use `cypress-real-events` (`realHover()`, Chromium-based browsers only), or reveal the menu with `.invoke('show')`, or use `{ force: true }` on the hidden item

**Explanation:** Cypress dispatches events from inside the page, and dispatched events cannot trigger the browser's CSS `:hover` pseudo-class. `cypress-real-events` sends real events through the Chrome DevTools Protocol, so it behaves like Playwright's `hover()` but only in Chromium-based browsers.
- **Why others are wrong:**
  - B) Cypress deliberately has no `.hover()` command.
  - C) `trigger('mouseover')` works only when the app listens for JavaScript mouse events, not for CSS `:hover`.
  - D) A right click dispatches a `contextmenu` event and has no effect on `:hover`.
</details>

---

### 27. You want to pause in DevTools at the point where an element has been found. Where should the `debugger;` statement go?
- [ ] A) At the top of the `it` body, before the first `cy` command
- [ ] B) Inside `cypress.config.js`
- [ ] C) On its own line right after `cy.get('.item');` in the test body
- [ ] D) Inside a `.then()` callback chained after the `cy.get`

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** D) Inside a `.then()` callback chained after the `cy.get`

**Explanation:** Plain JavaScript runs while Cypress is still queuing commands, so a `debugger` in the test body fires before any command has executed. Inside `.then()` it runs in sequence, after the element was found.
- **Why others are wrong:**
  - A) The page has not even loaded when this runs; the commands are only queued.
  - B) The config file runs in Node at startup, not in the test's timeline.
  - C) A statement in the test body runs immediately, before the `cy.get` has executed.
</details>

---

### 28. During `cypress run` in CI you want a message to appear in the terminal log. What should you use?
- [ ] A) `cy.log('message')`
- [ ] B) `console.log('message')` in the spec
- [ ] C) `cy.task('log', 'message')` with a `log` task registered in `setupNodeEvents`
- [ ] D) `cy.debug()`

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** C) `cy.task('log', 'message')` with a `log` task registered in `setupNodeEvents`

**Explanation:** Tasks run in Node, so `console.log` inside the task writes to the terminal where Cypress is running, which is the only output you see in CI.
- **Why others are wrong:**
  - A) `cy.log` writes to the Command Log only; it does not appear in terminal output.
  - B) A spec's `console.log` goes to the browser console (DevTools), not the terminal.
  - D) `.debug()` logs the subject and can pause in DevTools; it is not a terminal logger.
</details>

---

## Part 2: True/False on Common Misconceptions

### 29. True or False: Cypress can drive a second browser tab opened by a `target="_blank"` link, just as Playwright can with `expect_page()`.
- [ ] A) True
- [ ] B) False

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** B) False

**Explanation:** Cypress runs inside the single tab it controls, so multi-tab and multi-window testing is not supported. The workarounds are removing the `target` attribute or visiting the link's `href`; Playwright's `context.expect_page()` has no direct Cypress equivalent.
</details>

---

### 30. True or False: Since Cypress 12, test isolation is on by default, so before each test Cypress clears cookies, localStorage, and sessionStorage and navigates the browser to `about:blank`.
- [ ] A) True
- [ ] B) False

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** A) True

**Explanation:** `testIsolation: true` is the default. This is why every `it` needs its own `cy.visit()` (or `cy.session()` plus a visit), and it plays the same role as Playwright's per-test `BrowserContext`.
</details>

---

### 31. True or False: Electron is Chromium-based, so a passing run in Electron gives you little extra cross-browser confidence beyond what a Chrome run already gives.
- [ ] A) True
- [ ] B) False

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** A) True

**Explanation:** Electron is a Chromium-family browser, so it is a convenient default but not a substitute for running in Firefox (or testing Safari/WebKit elsewhere). Treating Electron as "a different browser" is a listed pitfall.
</details>

---

### 32. True or False: An `expect()` assertion inside a `.then()` callback is retried until it passes or times out, exactly like `.should()`.
- [ ] A) True
- [ ] B) False

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** B) False

**Explanation:** Explicit assertions (`expect`, `assert`) inside `.then()` run once. Only implicit assertions chained with `.should()` or `.and()` (and the callback form of `.should()`) are retried with the query before them. This is the classic cause of a flaky "total price" test.
</details>

---

### 33. True or False: A Cypress fixture is a function that is injected into your test by parameter name, just like a Playwright/pytest fixture.
- [ ] A) True
- [ ] B) False

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** B) False

**Explanation:** A Cypress fixture is a static data file in `cypress/fixtures` loaded with `cy.fixture()`. Cypress has no dependency-injection system; the roles of Playwright fixtures are filled by custom commands, hooks, `cy.session()`, and tasks.
</details>

---

### 34. True or False: `.check()` is idempotent, so calling it on a checkbox that is already checked does nothing and does not fail the test.
- [ ] A) True
- [ ] B) False

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** A) True

**Explanation:** `.check()` only checks boxes that are unchecked, which makes the test robust to the starting state. (`.uncheck()` works on checkboxes only; radios are changed by checking another radio.)
</details>

---

### 35. True or False: `cy.log('Reached checkout')` prints the message to the terminal output of `cypress run`.
- [ ] A) True
- [ ] B) False

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** B) False

**Explanation:** `cy.log` adds a line to the Command Log in the Test Runner only. To print to the terminal you need a task, for example `cy.task('log', 'Reached checkout')`, because tasks run in Node.
</details>

---

### 36. True or False: If one test calls `cy.viewport('iphone-x')`, the following tests in the file also start with that viewport.
- [ ] A) True
- [ ] B) False

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** B) False

**Explanation:** `cy.viewport` resets for each test; the next test starts again with the configured default (`viewportWidth`/`viewportHeight`, built-in default 1000 x 660). Call it in a `beforeEach` if every test needs it.
</details>

---

### 37. True or False: With `@cypress/grep`, a tag placed on a `describe` block is inherited by every test inside it.
- [ ] A) True
- [ ] B) False

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** A) True

**Explanation:** For example, `describe('Login', { tags: '@auth' }, ...)` gives every test inside the `@auth` tag, in addition to any tags on the individual `it`.
</details>

---

### 38. True or False: `cy.contains()` is case-sensitive by default, and you need `{ matchCase: false }` to ignore case.
- [ ] A) True
- [ ] B) False

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** A) True

**Explanation:** `matchCase` defaults to `true`. `cy.contains('add to cart', { matchCase: false })` matches regardless of case. Whitespace is normalised, and partial text matches unless you use an anchored regex.
</details>

---

### 39. True or False: `.select()` can be used on any dropdown, including custom ones built from `div` and `ul` elements.
- [ ] A) True
- [ ] B) False

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** B) False

**Explanation:** `.select()` works only on native `<select>` elements. Custom dropdowns are handled like ordinary elements: click to open, then click the option (for example `cy.contains('[role="option"]', 'Canada').click()`).
</details>

---

### 40. True or False: `cy.pause()` is intended for `cypress open`, where a person can click Next or Resume, and should be removed before committing.
- [ ] A) True
- [ ] B) False

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** A) True

**Explanation:** In headless `cypress run` nobody is there to resume, so a forgotten `cy.pause()` is a hazard. Treat it like `.only`, and consider a lint rule or CI grep for it.
</details>

---

## Part 3: Code Prediction

### 41. What happens when this test runs?
```js
it('order', () => {
  console.log('1');
  cy.log('2');
  console.log('3');
  cy.log('4');
});
```
- [ ] A) The browser console prints 1, 2, 3, 4 in that order
- [ ] B) The browser console prints 2 and 4 first, then 1 and 3
- [ ] C) The test errors, because plain JavaScript cannot be mixed with `cy` commands
- [ ] D) The console prints 1 then 3 while the test body runs; the Command Log shows the two `log` commands (2, then 4) afterwards

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** D) The console prints 1 then 3 while the test body runs; the Command Log shows the two `log` commands (2, then 4) afterwards

**Explanation:** `cy.log` only enqueues a command, so the plain `console.log` calls run first during the synchronous body. Cypress then executes the queue; `cy.log` writes to the Command Log, not to the console.
- **Why others are wrong:**
  - A) `cy.log` does not print to the browser console, and the commands run after the body, not interleaved with it.
  - B) The order is reversed: the plain JavaScript runs first.
  - C) Mixing is allowed; it just produces surprising ordering unless you wrap the JavaScript in `.then()`.
</details>

---

### 42. Assume the page has 6 `.inventory_item` elements. What is logged to the browser console?
```js
let count = 0;
cy.get('.inventory_item').its('length').then((n) => { count = n; });
console.log('A:', count);
cy.then(() => console.log('B:', count));
```
- [ ] A) `A: 6` then `B: 6`
- [ ] B) `A: 0` then `B: 6`
- [ ] C) `A: undefined` then `B: 6`
- [ ] D) `A: 0` then `B: 0`

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** B) `A: 0` then `B: 6`

**Explanation:** The `console.log('A:')` line runs immediately while the body executes, before the queued `cy.get` has assigned `count`, so it prints the initial `0`. The `cy.then` callback is queued after the assignment, so it sees 6. Assign inside a callback, read inside a later callback.
- **Why others are wrong:**
  - A) Line A runs before the assignment happens.
  - C) `count` was initialised to `0`, so it is not `undefined`.
  - D) The later `cy.then` runs after `count = n`, so B is 6.
</details>

---

### 43. What is the order of the letters printed to the browser console?
```js
console.log('A');
cy.then(() => console.log('B'));
console.log('C');
cy.then(() => console.log('D'));
console.log('E');
```
- [ ] A) `ABCDE`
- [ ] B) `BDACE`
- [ ] C) `ACEBD`
- [ ] D) `ACBED`

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** C) `ACEBD`

**Explanation:** The three plain `console.log` calls (A, C, E) run during the synchronous test body. The two `cy.then` callbacks (B, D) are queued and run afterwards, in order. (Verified with a small queue simulation in Node.)
- **Why others are wrong:**
  - A) This is the written order, which would be true only if everything ran immediately.
  - B) The queued callbacks do not run before the plain JavaScript.
  - D) B cannot run until the whole body has finished, so it cannot appear between C and E.
</details>

---

### 44. The `.count` element shows `4` at first and changes to `5` after about one second. The two snippets below are run as separate tests with the default 4-second timeout. What happens?
```js
// Snippet 1
cy.get('.count').then(($el) => {
  expect($el.text()).to.equal('5');
});

// Snippet 2
cy.get('.count').should('have.text', '5');
```
- [ ] A) Snippet 1 fails immediately; Snippet 2 passes after retrying
- [ ] B) Both pass
- [ ] C) Both fail
- [ ] D) Snippet 1 passes; Snippet 2 fails

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** A) Snippet 1 fails immediately; Snippet 2 passes after retrying

**Explanation:** `cy.get` finds the element straight away, and the `.then()` callback runs once, seeing `4`, so the `expect` fails. In Snippet 2 the query and `.should()` are retried together until the text becomes `5` (within 4 seconds).
- **Why others are wrong:**
  - B) The assertion in `.then()` is not retried, so it cannot wait for the update.
  - C) The retried `.should()` has enough time (about 1 second of a 4-second budget).
  - D) This reverses the retry behaviour.
</details>

---

### 45. Which lines throw an assertion error? (Chai assertions)
```js
expect(0).to.be.false;                          // line 1
expect(0).to.not.be.ok;                         // line 2
expect([1, 2, 3]).to.have.members([3, 2, 1]);   // line 3
expect([1, 2, 3]).to.deep.equal([3, 2, 1]);     // line 4
```
- [ ] A) Only line 1
- [ ] B) Lines 1 and 3
- [ ] C) Lines 2 and 4
- [ ] D) Lines 1 and 4

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** D) Lines 1 and 4

**Explanation:** `.to.be.false` is strict: `0` is falsy but is not the boolean `false`, so line 1 fails (use `.to.not.be.ok` for falsy, as in line 2). `have.members` ignores order, so line 3 passes; `deep.equal` on arrays is order-sensitive, so line 4 fails. (Verified with Chai in Node.)
- **Why others are wrong:**
  - A) Line 4 also fails because array order differs.
  - B) Line 3 passes because `members` compares contents in any order.
  - C) Line 2 passes (0 is not truthy), and line 1 fails, so this misses line 1.
</details>

---

### 46. What is the result of this check?
```js
const prices = ['$29.99', '$9.99', '$7.99'].map((s) => Number(s.replace('$', '')));
const sorted = [...prices].sort((a, b) => a - b);
expect(prices).to.deep.equal(sorted);
```
- [ ] A) It passes, because the prices are already in a valid order
- [ ] B) It throws a `TypeError` because spreading an array is not allowed
- [ ] C) It fails: `prices` is `[29.99, 9.99, 7.99]` but `sorted` is `[7.99, 9.99, 29.99]`
- [ ] D) It fails because `sort` mutated `prices` into a different order than `sorted`

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** C) It fails: `prices` is `[29.99, 9.99, 7.99]` but `sorted` is `[7.99, 9.99, 29.99]`

**Explanation:** The numeric map produces `[29.99, 9.99, 7.99]`. Sorting a copy ascending gives `[7.99, 9.99, 29.99]`, and `deep.equal` is order-sensitive, so the assertion fails. This is the pattern used to check "low to high" sorting: the list is only valid if it equals its own sorted copy. (Verified in Node.)
- **Why others are wrong:**
  - A) The original order is descending, not ascending.
  - B) Spreading into a new array is valid and is used to avoid mutation.
  - D) `[...prices]` is a copy, so `prices` is never mutated; the two arrays differ because of the data, not mutation.
</details>

---

### 47. A suite has these tests and tags. Which tests does `npx cypress run --env grepTags=@smoke+-@slow` run?
```js
it('A', { tags: ['@smoke', '@fast'] }, () => {});
it('B', { tags: ['@smoke', '@slow'] }, () => {});
it('C', { tags: '@regression' }, () => {});
it('D', { tags: '@smoke' }, () => {});
it('E', () => {});            // untagged
```
- [ ] A) A, B, and D (anything tagged `@smoke`)
- [ ] B) A and D
- [ ] C) C and E
- [ ] D) Only A

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** B) A and D

**Explanation:** The expression means "has `@smoke` AND does not have `@slow`". A and D have `@smoke` and no `@slow`; B is excluded by `@slow`; C and E have no `@smoke`. (Filter logic checked in Node.)
- **Why others are wrong:**
  - A) This ignores the `-@slow` part, so B would wrongly be included.
  - C) These are the tests that are not smoke at all.
  - D) `@fast` is not part of the expression, so D also qualifies.
</details>

---

### 48. How does Mocha see the tests generated by this spec?
```js
const cases = [
  { user: 'standard_user', pass: 'secret_sauce' },
  { user: '', pass: 'secret_sauce' },
  { user: 'locked_out_user', pass: 'secret_sauce' },
  { user: 'standard_user', pass: '' },
];

describe('Login', () => {
  cases.forEach(({ user, pass }) => {
    it(`tries "${user}" / "${pass}"`, () => { /* steps */ });
  });
  it('shows the logo');
});
```
- [ ] A) 5 tests are registered: 4 generated runnable tests, plus 1 pending test (no callback)
- [ ] B) 4 tests are registered; the last `it` is a syntax error
- [ ] C) 1 test is registered, because `forEach` is a single command
- [ ] D) 0 tests are registered until a fixture has loaded

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** A) 5 tests are registered: 4 generated runnable tests, plus 1 pending test (no callback)

**Explanation:** Plain JavaScript loops run synchronously at load time, so `forEach` registers one `it` per case. The final `it` without a function is a pending placeholder. (Verified with Mocha in Node.)
- **Why others are wrong:**
  - B) A test without a callback is valid pending syntax.
  - C) `forEach` is ordinary JavaScript, not a queued Cypress command, so it creates one test per element.
  - D) The data is an in-file array; no fixture load is involved.
</details>

---

### 49. The input `#name` already contains `Wrong`. What does it contain after this runs?
```js
cy.get('#name').type('{selectall}Ada{backspace}');
```
- [ ] A) `WrongAd`
- [ ] B) `Ada`
- [ ] C) `Wrong`
- [ ] D) `Ad`

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** D) `Ad`

**Explanation:** `{selectall}` selects the existing text, typing `Ada` replaces it, and `{backspace}` deletes the last character, leaving `Ad`.
- **Why others are wrong:**
  - A) That would happen only if `{selectall}` did not select the existing text.
  - B) This forgets the final `{backspace}`.
  - C) The typed characters do replace the old value.
</details>

---

### 50. What does the final assertion see on the page under test (the result element shows "You clicked: Ok" or "You clicked: Cancel")?
```js
cy.on('window:confirm', () => false);
cy.get('#confirm-button').click();
cy.get('#result').should('have.text', 'You clicked: Cancel');
```
- [ ] A) The assertion fails, because Cypress always auto-accepts confirms
- [ ] B) The test hangs, waiting for a human to answer the confirm
- [ ] C) The assertion passes: returning `false` from the `window:confirm` listener cancels the dialog
- [ ] D) The test throws, because a confirm listener must call `dialog.dismiss()`

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** C) The assertion passes: returning `false` from the `window:confirm` listener cancels the dialog

**Explanation:** By default Cypress auto-accepts alerts and confirms. For a confirm, the listener's return value decides the choice: `false` clicks Cancel; returning nothing or `true` accepts.
- **Why others are wrong:**
  - A) Auto-accept is only the default; the listener's `false` overrides it.
  - B) Cypress never waits for a human; by default it answers the dialog for you (unlike a Playwright dialog handler, where you must accept or dismiss yourself).
  - D) There is no `dialog` object to dismiss in Cypress; you return a boolean.
</details>

---

### 51. The `#terms` checkbox starts unchecked. What is the outcome?
```js
cy.get('#terms').check();
cy.get('#terms').check();
cy.get('#terms').should('be.checked');
```
- [ ] A) The test passes; the second `.check()` does nothing
- [ ] B) The second `.check()` unchecks the box, so the assertion fails
- [ ] C) The test fails with an "already checked" error on the second call
- [ ] D) The test fails because `.check()` can only be called once per test

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** A) The test passes; the second `.check()` does nothing

**Explanation:** `.check()` is idempotent. It only changes unchecked boxes, which is why it is robust to starting state.
- **Why others are wrong:**
  - B) Toggling is what a raw `.click()` would do; `.check()` never unchecks.
  - C) Cypress does not raise an error for an already-checked box.
  - D) There is no limit on how many times it can be called.
</details>

---

### 52. You open DevTools and the test reaches the `debugger` statement. What is the state of the page and the test at that moment?
```js
it('debug', () => {
  cy.visit('/');
  cy.get('[data-test="username"]').type('standard_user');
  debugger;
});
```
- [ ] A) The page has loaded and the username has been typed
- [ ] B) None of the Cypress commands have run yet; they are only queued, so the application page is still blank
- [ ] C) `cy.visit` has finished, but the username has not been typed yet
- [ ] D) Cypress ignores `debugger` statements in spec files

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** B) None of the Cypress commands have run yet; they are only queued, so the application page is still blank

**Explanation:** The test body executes synchronously and only registers commands; the queue runs after it finishes. To pause with a live page, put `debugger` inside a `.then()` after the `cy.get`, or use `cy.pause()`.
- **Why others are wrong:**
  - A) That would require the commands to have executed, which happens only after the body completes.
  - C) `cy.visit` is also just queued at this point.
  - D) The `debugger` statement is honoured when DevTools is open; the problem is its timing.
</details>

---

### 53. Given this markup, what does the chain yield?
```html
<ul class="list">
  <li class="a">Apple</li>
  <li class="b" id="target">Banana</li>
  <li class="c">Cherry</li>
</ul>
```
```js
cy.get('.list').find('li').eq(-1).invoke('text')
```
- [ ] A) `Apple`
- [ ] B) `Banana`
- [ ] C) `Cherry`
- [ ] D) An error, because `.eq()` does not accept negative indexes

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** C) `Cherry`

**Explanation:** `.find('li')` yields all three `li` elements and `.eq(-1)` counts from the end, selecting the last one. `.invoke('text')` then yields its text.
- **Why others are wrong:**
  - A) `Apple` is `.eq(0)` or `.first()`.
  - B) `Banana` is `.eq(1)`.
  - D) Negative indexes are supported; `.eq(-1)` is the last element.
</details>

---

### 54. In what order are the messages printed for this whole spec?
```js
before(() => console.log('B1'));
beforeEach(() => console.log('BE1'));

describe('suite', () => {
  before(() => console.log('B2'));
  beforeEach(() => console.log('BE2'));
  afterEach(() => console.log('AE2'));
  after(() => console.log('A2'));

  it('A', () => console.log('T-A'));
  it('B', () => console.log('T-B'));
});
```
- [ ] A) B1, BE1, B2, BE2, T-A, AE2, B1, BE1, B2, BE2, T-B, AE2, A2
- [ ] B) B2, B1, BE2, BE1, T-A, AE2, BE2, BE1, T-B, AE2, A2
- [ ] C) B1, B2, BE1, BE2, T-A, T-B, AE2, A2
- [ ] D) B1, B2, BE1, BE2, T-A, AE2, BE1, BE2, T-B, AE2, A2

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** D) B1, B2, BE1, BE2, T-A, AE2, BE1, BE2, T-B, AE2, A2

**Explanation:** `before` hooks run once, outer to inner. For each test, `beforeEach` hooks run outer to inner, then the test, then `afterEach`. `after` runs once at the end. (Verified with Mocha in Node, using `console.log` in place of `cy.log`.)
- **Why others are wrong:**
  - A) `before` hooks do not run again for the second test, and the outer `beforeEach` runs after both `before` hooks.
  - B) Outer hooks run before inner hooks on the way in.
  - C) `beforeEach` and `afterEach` wrap every test, not the whole suite.
</details>

---

## Part 4: Fill-in-the-Blank

### 55. In `cypress.config.js`, the option `_____` sets the app's root URL so that `cy.visit('/')` and `cy.visit('/inventory.html')` resolve relative to it.

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** `baseUrl`

**Explanation:** `baseUrl` (inside the `e2e` block) avoids hard-coding the domain in every `cy.visit`. It is the Cypress counterpart of `base_url` / `baseURL` in Playwright's configuration, and Cypress also checks that the server is reachable before starting.
</details>

---

### 56. To run all specs from the command line without a graphical interface (the mode used in CI), you run `npx cypress _____`.

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** `run`

**Explanation:** `cypress run` is headless by default (Electron unless `--browser` is given), prints results to the terminal, and exits with a status code that CI uses to pass or fail the build. `cypress open` is the interactive, headed runner for development.
</details>

---

### 57. Inside a test, `cy._____(375, 667)` sets the browser viewport to a phone-sized width and height; the setting resets for the next test.

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** `viewport`

**Explanation:** `cy.viewport(width, height)` (or a preset such as `cy.viewport('iphone-x')`) changes the viewport for the current test. Call it before `cy.visit()` so the page lays out at that size from the start.
</details>

---

### 58. To give a yielded value a name, chain `._____('firstItem')` and later retrieve it with `cy.get('@firstItem')`.

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** `as`

**Explanation:** `.as('name')` creates an alias; the `@` prefix is used with `cy.get('@name')` to retrieve it. For DOM elements, the alias stores the query so Cypress can re-run it, and aliases are reset between tests.
</details>

---

### 59. Playwright's `page.get_by_text("Add to cart")` corresponds to the Cypress command `cy._____('Add to cart')`.

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** `contains`

**Explanation:** `cy.contains(text)` locates an element by its visible text (case-sensitive by default, whitespace-normalised). Pass a selector first, as in `cy.contains('button', 'Add to cart')`, to scope the match to a particular kind of element.
</details>

---

### 60. To run only one folder or file of specs, add the flag `_____` followed by a quoted glob, for example `npx cypress run _____ "cypress/e2e/cart/**/*.cy.js"`.

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** `--spec`

**Explanation:** `--spec` selects spec files by glob. Always quote the pattern so the shell does not expand it, and separate multiple specs with commas inside one quoted string. This is the Cypress counterpart of passing a path to `pytest`.
</details>

---

### 61. With the `@cypress/grep` plugin, you run only tests tagged `@smoke` using `npx cypress run --env _____=@smoke`.

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** `grepTags`

**Explanation:** `grepTags` selects by tag (space = OR, `+` = AND, `-` = NOT), while `grep` selects by title text. It is the Cypress parallel of `pytest -m smoke`.
</details>

---

### 62. `Cypress.Commands._____('login', (username, password) => { ... })` registers a custom command that you can call as `cy.login(...)`.

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** `add`

**Explanation:** `Cypress.Commands.add(name, callback)` defines a reusable command, normally in `cypress/support/commands.js` (imported by `e2e.js`). This, together with `cy.session()` and hooks, fills the role Playwright fixtures play for reusable setup.
</details>

---

### 63. Playwright's `locator.set_input_files(path)` corresponds to the Cypress command `.______(path)`, for example `cy.get('input[type="file"]').______('cypress/fixtures/report.pdf')`.

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** `selectFile`

**Explanation:** `.selectFile()` is built into Cypress (since 9.3). Paths are relative to the project root, and `{ action: 'drag-drop' }` simulates dropping the file onto a drop zone.
</details>

---

### 64. Calling `.type('')` throws an error in Cypress. To empty a field, use `._____()`, which is an alias for `.type('{selectall}{backspace}')`.

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** `clear`

**Explanation:** `.clear()` focuses the element, selects all of its text, and deletes it, and it chains naturally into a replacement, as in `.clear().type('90210')`. This is why earlier examples guard with `if (value)` before typing.
</details>

---

### 65. `cy._____()` halts a running test and shows Resume and Next buttons in the Command Log so you can step through one command at a time.

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** `pause`

**Explanation:** `cy.pause()` is a temporary debugging aid for `cypress open`. **Next** runs only the next command and pauses again; **Resume** continues to the next pause or the end of the test. Remove it before committing.
</details>

---

### 66. To print a message from a test to the terminal, register a task named `log` in `setupNodeEvents` and call `cy._____('log', 'message')`.

<details>
<summary><b>🔎 Click for Solution</b></summary>

**Correct Answer:** `task`

**Explanation:** Tasks run in the Node process, so their `console.log` appears in the terminal where Cypress is running. Remember that task handlers must return a value or `null`, never `undefined`.
</details>

---

*End of quiz: 66 questions. Review any you missed against the Thursday lessons, then compare your answers with the Cypress and Playwright comparison tables in each lesson.*

