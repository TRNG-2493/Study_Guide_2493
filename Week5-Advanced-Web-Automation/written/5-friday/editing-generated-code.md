# Editing Generated Code: From Raw Recording to Maintainable Cypress Tests

## Learning Objectives

By the end of this lesson you will be able to:

- Review a recorded (generated) Cypress test and list its typical weaknesses using a repeatable checklist.
- Replace fragile recorded selectors with stable ones (`data-*` test attributes, `cy.contains` with context, scoping with `within`/`find`), and explain the trade-offs.
- Remove redundant recorded steps (extra clicks, duplicate queries, viewport noise) without changing behaviour.
- Add meaningful **assertions** at the right places: state checks, URL checks, content checks, negative checks, and network assertions with `cy.intercept` aliases.
- Replace arbitrary waits and "hopeful" timing with deterministic synchronisation.
- Extract repeated steps into **custom commands** (`Cypress.Commands.add`), including parent, child and overwritten commands, and speed up login with `cy.session()`.
- Move test data and secrets out of the spec into **fixtures** and **environment variables**.
- Organise a spec with `describe`, `beforeEach` and clearly named `it` blocks, and verify stability by running the refactored test repeatedly.
- Explain the difference between refactoring (changing structure, keeping behaviour) and extending (changing behaviour), and keep them in separate steps.

---

## Why This Matters

In the previous lesson you learned to *record* user actions with Cypress Studio and the Chrome DevTools Recorder. We ended with an important warning: **a recording is a draft**. It captures what you *did*, not what you *meant*. It has no assertions, uses whatever selector the tool found first, repeats itself and says nothing about why the test exists.

This week's epic is to graduate from "I can make a script work" to "I can build structured, maintainable automation". Wednesday's Playwright lessons (fixtures, hooks, Page Object Model, data-driven tests) were about structure; Thursday's Cypress lessons were about writing and locating; today we combine them by taking raw, generated code and applying everything you have learned.

For **Project 1: QE Foundations**, the final UI deliverable will be judged on more than "does it pass?". Reviewers will ask: Are the selectors stable? Are there real assertions? Is the login duplicated in every test? Are credentials hard-coded? Can another engineer read this test and understand the requirement? These are exactly the questions this lesson teaches you to answer.

There is also a professional reality: in many teams, the cost of an automated test is *not* writing it, it is *maintaining* it for years. Every shortcut you leave in a generated test is paid for later, with interest, by someone (often you).

---

## The Concept

### 1. A starting point: a realistic raw recording

Throughout this lesson we refactor one test. Imagine a teammate recorded a complete purchase on https://www.saucedemo.com with the Chrome DevTools Recorder, exported it and converted it with `@cypress/chrome-recorder`. The result (lightly formatted) is:

```js
describe('checkout', () => {
  it('tests checkout', () => {
    cy.viewport(1440, 900);
    cy.visit('https://www.saucedemo.com/');
    cy.get('div:nth-child(1) > .form_group > .input_error').click();
    cy.get('div:nth-child(1) > .form_group > .input_error').type('standard_user');
    cy.get('#password').click();
    cy.get('#password').type('secret_sauce');
    cy.get('#login-button').click();
    cy.get('.inventory_item:nth-child(1) .btn_inventory').click();
    cy.get('.inventory_item:nth-child(2) .btn_inventory').click();
    cy.get('.shopping_cart_link').click();
    cy.get('#checkout').click();
    cy.get('#first-name').click();
    cy.get('#first-name').type('Ada');
    cy.get('#last-name').click();
    cy.get('#last-name').type('Lovelace');
    cy.get('#postal-code').click();
    cy.get('#postal-code').type('12345');
    cy.get('#continue').click();
    cy.get('#finish').click();
  });
});
```

(Exact selectors depend on the tool and site version; the shape of the problem is what matters.) We will go through a **ten-step refactoring process** and arrive at a clean, maintainable test.

### 2. The review checklist

Before changing anything, read the generated code with this checklist. Each item becomes a section below.

1. **Does it pass reliably right now?** (Run it first; refactoring a broken test is guesswork.)
2. **Names:** Do `describe` and `it` describe business behaviour?
3. **Noise:** Redundant clicks, repeated queries, viewport, scrolls?
4. **Selectors:** Stable and readable, or structural and brittle?
5. **Assertions:** What does this test actually verify?
6. **Synchronisation:** Any fixed waits or reliance on luck?
7. **Data:** Hard-coded values and credentials?
8. **Duplication:** Steps that every test will repeat (login, navigation)?
9. **Structure:** Hooks, grouping, one behaviour per test?
10. **Stability:** Does it pass 10 times in a row, headless?

### 3. Step 1: Run it first, and freeze the behaviour

Always begin by running the raw test, in `cypress open` and in `cypress run`:

```bash
npx cypress run --spec cypress/e2e/checkout.cy.js
```

If it passes, you have a **safety net**: you can refactor in small steps and re-run after each step. If it fails, fix that first (perhaps a stale selector). Never mix "fixing" and "refactoring" in the same step, because when something breaks you will not know which change caused it. This discipline is the heart of safe refactoring: *small change, run, commit.*

### 4. Step 2: Name things after behaviour

`describe('checkout')` and `it('tests checkout')` carry no information. A good test name is a short sentence stating the *rule* being verified:

- `describe('Checkout')`
- `it('lets a standard user buy two products and see the order confirmation')`

Why it matters: when the test fails in CI, the name is the first thing people read in the report. A name like "tests checkout" forces them to open the code to understand the impact; a behavioural name tells them immediately what business capability is broken.

Tip: use the "Given/When/Then" style mentally: *Given* a logged-in user with two products in the cart, *when* they complete checkout with valid details, *then* they see an order confirmation.

### 5. Step 3: Remove noise

Recorders emit what they saw, including:

- `cy.viewport(1440, 900)`: usually belongs in `cypress.config.js` (`viewportWidth`, `viewportHeight`) or a shared `beforeEach`, not in each test. Keep it *only* if the test is specifically about that screen size.
- `.click()` immediately before `.type()` on the same input: `.type()` already focuses (clicks) the element. The extra click is harmless but is noise. Remove it unless focus behaviour is part of what you test.
- Repeated `cy.get(sel)` calls for the same element: you can chain (`cy.get(sel).type(...)`) or alias the element.
- Absolute URLs: replace with relative ones and set `baseUrl` in config (`cy.visit('/')`).

Removing noise should **not change behaviour**. After each deletion, re-run.

### 6. Step 4: Fix the selectors

Selector quality is the single biggest factor in how long a test lives. You studied this on Thursday ("Element location"). Apply the hierarchy:

| Quality | Selector style | Example | Why |
|---|---|---|---|
| Best | Dedicated test attribute | `[data-test="login-button"]`, `[data-cy="submit"]` | A deliberate contract with developers; survives restyling and rewording. |
| Good | Semantic/accessible hooks | `cy.contains('button', 'Checkout')`, `[aria-label="Close"]`, a role-based query from Testing Library | Reflects what users see; may break if wording changes or is translated. |
| Acceptable | Stable `id` | `#checkout` | OK if ids are controlled; some frameworks generate them. |
| Weak | Classes | `.btn_inventory` | Styling classes change with redesigns. |
| Worst | Structure/position | `div:nth-child(1) > .form_group > .input_error` | Breaks when the layout changes; also unreadable. |

Practical techniques while editing:

1. **Ask for test attributes.** If the application has none, raise it with developers; adding `data-test` is cheap and benefits everyone. In our site, they exist, so we use them.
2. **Scope with `within` or `find`.** To click "Add to cart" for a *specific* product without `nth-child`, find the product card by its name and search inside it:

```js
cy.contains('[data-test="inventory-item"]', 'Sauce Labs Backpack')
  .find('button')
  .click();
```

`cy.contains(selector, text)` finds the first element matching the selector that *contains* the text. `.find('button')` searches only within that card. This works even if the product order changes.

3. **Prefer `cy.contains` for visible text** when the text is itself the requirement (for example, a button label), but be aware of copy changes and localisation.
4. **Use the Selector Playground** to test candidates and see the match count (you want exactly one).
5. **Avoid dynamic values** in selectors (auto-generated ids such as `#react-select-3-input` or class names such as `.css-1x2y3z`).

### 7. Step 5: Add assertions

Now the most important step: giving the test a *purpose*. Think of assertions in four layers:

1. **Progress assertions (guards):** confirm each major step *worked* before proceeding. These make failures point to the right place and also act as synchronisation: Cypress retries them until true.
   - After login: `cy.url().should('include', '/inventory.html')`.
2. **State assertions:** verify intermediate state that matters.
   - After adding two items: `cy.get('[data-test="shopping-cart-badge"]').should('have.text', '2')`.
3. **Outcome assertions:** verify the business result.
   - After finishing: `cy.get('[data-test="complete-header"]').should('have.text', 'Thank you for your order!')`.
4. **Negative and side-effect assertions:** verify what should *not* be there or what changed elsewhere.
   - After the order: the cart badge no longer exists (`should('not.exist')`).
   - Network: the request was sent with the right payload and returned the right status.

Good assertion habits:

- Assert **one meaningful thing per assertion**, with a clear expected value.
- Prefer built-in, retry-able assertions on Cypress queries (`cy.get(...).should(...)`) over manual checks in `.then()` callbacks, because `.should()` retries and `.then()` does not.
- Use `.should('be.visible')` before clicking critical controls if animation is involved; Cypress already waits for actionability, so use it when *visibility itself* is a requirement.
- Do not assert implementation details (CSS class names, internal ids) unless the class *is* the contract.
- Do not over-assert: ten assertions about unrelated text make the test brittle. Assert what the scenario promises.

Network assertions use `cy.intercept` with an alias:

```js
cy.intercept('POST', '**/api/orders').as('createOrder');
// ...user clicks "Finish"...
cy.wait('@createOrder').its('response.statusCode').should('eq', 201);
```

This is both an assertion (the API returned 201) and *deterministic synchronisation* (the test waits for the real request instead of an arbitrary time). Sauce Demo has no such API, but real Project 1 applications often do.

### 8. Step 6: Replace waits with conditions

Recorded tests rarely contain waits, but people add `cy.wait(2000)` when a recorded test is flaky. Replace it with a condition:

| Instead of | Use |
|---|---|
| `cy.wait(2000)` before clicking a button | `cy.get('button').should('be.visible')` (and let actionability do its job) |
| `cy.wait(3000)` after submitting a form | `cy.url().should('include', '/success')` or `cy.wait('@submit')` for an aliased request |
| `cy.wait(1000)` for a spinner | `cy.get('[data-test="spinner"]').should('not.exist')` |

Rule: **wait for an event or a state, never for time.**

### 9. Step 7: Move data and secrets out of the spec

Hard-coded names and passwords make tests inflexible and unsafe.

**Fixtures** are JSON (or other) files in `cypress/fixtures/` holding test data, loaded with `cy.fixture()` or imported. Example `cypress/fixtures/users.json`:

```json
{
  "standard": { "username": "standard_user" },
  "customer": { "firstName": "Ada", "lastName": "Lovelace", "postalCode": "12345" }
}
```

**Secrets** such as passwords should come from the environment: a git-ignored `cypress.env.json` file, or environment variables prefixed with `CYPRESS_` (for example `CYPRESS_SAUCE_PASSWORD=secret_sauce`), read in tests with `Cypress.env('SAUCE_PASSWORD')`. In CI, these come from the pipeline's secret store. (Sauce Demo's password is public, so this is practice; in your own project, treat real credentials as secrets.)

Note on versions: Cypress is evolving how it distinguishes secret environment values from public configuration values in recent releases. `Cypress.env()` remains the widely used approach in Cypress 13 and 14; check the current documentation if you use a very recent version.

### 10. Step 8: Remove duplication with custom commands and `cy.session`

Every test in your suite will log in. If the recording repeated those five lines in every test, one change to the login page means editing every test. Extract them.

#### 10.1 Custom commands

`Cypress.Commands.add(name, callback)` registers a new `cy.name()` command, usually in `cypress/support/commands.js` (loaded by `cypress/support/e2e.js`). Kinds:

- **Parent command:** starts a chain, e.g. `cy.login()`.
- **Child command:** needs a previous subject, declared with `{ prevSubject: true }` or a validated type such as `'element'`, `'document'` or `'window'`, e.g. `cy.get('input').fillWith('x')`.
- **Dual command:** works with or without a previous subject (`prevSubject: 'optional'`).
- **Overwrite:** `Cypress.Commands.overwrite('visit', (originalFn, url, options) => ...)` changes an existing command (use sparingly).

Rules of thumb for good custom commands:

1. Name them after *user intent* (`login`, `addProductToCart`), not mechanics.
2. Keep them small and single-purpose.
3. Do not hide assertions that tests should state explicitly (a command that "adds to cart and asserts the badge" is surprising; keep checks visible in the test, or name the command accordingly, e.g. `addProductAndVerifyBadge`).
4. Do not turn *everything* into commands; for page-specific structure you may prefer the Page Object Model you learned on Wednesday (in Cypress, plain classes or helper modules also work well). The Cypress team's own guidance favours custom commands for cross-cutting actions such as login, and helper functions or small page-object modules for page-specific interactions.

#### 10.2 `cy.session`

Logging in through the UI in every test is slow. `cy.session(id, setupFn, options)` runs your login once, caches cookies, `localStorage` and `sessionStorage` under the given `id`, and **restores** them in later tests, which is much faster. Key points:

- `id`: a string or array (or serialisable value) that identifies the session. Different users need different ids.
- `setupFn`: the function that performs the login.
- `options.validate`: a function that runs after restoring to confirm the session is still valid; if validation fails, Cypress re-runs the setup.
- `options.cacheAcrossSpecs`: if `true`, the cached session is shared across spec files.
- `cy.session` works together with **test isolation** (`testIsolation`, which is on by default in Cypress 12 and later). When it is enabled, Cypress clears the page and the browser state before the session is set up or restored, so each test starts clean. After `cy.session()` the page is blank, so you must still `cy.visit()` the page you want. (With `testIsolation: false` the page is not cleared; avoid that unless you know why you need it.)
- In the Command Log, the `session` row shows one of three statuses: **created** (no cached session existed, so your setup ran), **restored** (a cached session was reused) or **recreated** (a cached session existed but `validate` failed, so setup ran again).
- `cacheAcrossSpecs` was added in Cypress 10.9.0.

#### 10.3 Page helper modules (an alternative)

For page-specific code, keep plain JavaScript modules:

```js
// cypress/support/pages/checkoutPage.js
export const checkoutPage = {
  fillCustomer({ firstName, lastName, postalCode }) { /* ... */ },
};
```

You will likely compare this to the POM from Wednesday; the principles are identical.

### 11. Step 9: Structure with hooks and small tests

- Put shared setup in `beforeEach` (login, visit starting page).
- Keep each `it` to **one behaviour** where practical. A 40-step "mega test" is hard to debug; but in end-to-end testing, a single "happy path" journey that covers many steps may be intentional and acceptable. Balance: *few* long journeys for smoke coverage, *many* small tests for specific rules.
- Do not rely on test order. With test isolation, each test starts clean; tests that depend on a previous test's leftovers will break (and are the enemy of parallel execution).
- Use `context`/`describe` blocks to group.

### 12. Step 10: Prove stability

A test that passes once is not necessarily stable. Check:

1. Run it 10 times in a row, headless: in Cypress you can generate repeats using lodash (bundled as `Cypress._`):

```js
Cypress._.times(10, (i) => {
  it(`stability run ${i + 1}`, () => { /* body */ });
});
```

   (Use temporarily; do not commit.)
2. Run in a different browser (`--browser chrome`, `--browser firefox`) if your project supports them.
3. Run in your CI environment, not only locally.
4. Use test retries (`retries: { runMode: 1 }`) as a safety net but not as a cure; investigate every retry that fires.

### 13. Refactoring versus extending

When you move steps into a command, you *refactor*: the behaviour stays the same. When you add assertions, you *extend*: you may discover bugs, and the test may fail for good reason. Separate them into different commits ("Refactor: extract login command" and "Add order confirmation assertions") so a failure points at the right change.

---

## Code Examples

### Example 1: The refactored test (final result)

`cypress/e2e/checkout.cy.js`:

```js
describe('Checkout', () => {
  beforeEach(() => {
    cy.login();
    cy.visit('/inventory.html');
  });

  it('lets a standard user buy two products and see the order confirmation', () => {
    cy.fixture('users').then(({ customer }) => {
      cy.addProductToCart('Sauce Labs Backpack');
      cy.addProductToCart('Sauce Labs Bike Light');

      cy.get('[data-test="shopping-cart-badge"]').should('have.text', '2');

      cy.get('[data-test="shopping-cart-link"]').click();
      cy.url().should('include', '/cart.html');
      cy.get('[data-test="inventory-item"]').should('have.length', 2);

      cy.get('[data-test="checkout"]').click();
      cy.get('[data-test="firstName"]').type(customer.firstName);
      cy.get('[data-test="lastName"]').type(customer.lastName);
      cy.get('[data-test="postalCode"]').type(customer.postalCode);
      cy.get('[data-test="continue"]').click();

      cy.get('[data-test="subtotal-label"]').should('contain.text', '$39.98');

      cy.get('[data-test="finish"]').click();
      cy.get('[data-test="complete-header"]').should('have.text', 'Thank you for your order!');
      cy.get('[data-test="shopping-cart-badge"]').should('not.exist');
    });
  });
});
```

**Line-by-line explanation**

1. `describe('Checkout', ...)` groups tests about the checkout feature. The name is short and business-oriented.
2. `beforeEach(() => { ... })` runs before each test in the group.
3. `cy.login()` is our custom command (defined below). It uses `cy.session`, so the login UI steps run once and are restored afterwards.
4. `cy.visit('/inventory.html')` loads the page we want. We must do this explicitly because `cy.session` leaves the browser on a blank page. The relative URL relies on `baseUrl` in the config.
5. `it('lets a standard user buy two products and see the order confirmation', ...)` names the behaviour precisely.
6. `cy.fixture('users').then(({ customer }) => { ... })` loads `cypress/fixtures/users.json`. The `.then` callback receives the parsed JSON; we use **destructuring** (`{ customer }`) to take the `customer` property. Everything that uses `customer` is placed inside the callback so it is queued in the right order.
7. `cy.addProductToCart('Sauce Labs Backpack')` and the next call use another custom command: the product is found by *name*, not by position.
8. `cy.get('[data-test="shopping-cart-badge"]').should('have.text', '2')` is a **state assertion**: two items were added. It also serves as a guard before moving on.
9. Clicking the cart link followed by `cy.url().should('include', '/cart.html')` verifies the navigation (guard).
10. `cy.get('[data-test="inventory-item"]').should('have.length', 2)` verifies the cart page lists two items (Sauce Demo reuses the `inventory-item` test attribute for cart rows).
11. The checkout steps type the customer data from the fixture into the three fields and click Continue. We removed the redundant `.click()` calls before each `.type()`.
12. `should('contain.text', '$39.98')` checks the subtotal (29.99 + 9.99) on the overview page. `contain.text` is a substring match, tolerant of the "Item total: " prefix.
13. `cy.get('[data-test="finish"]').click()` completes the order.
14. The **outcome assertion** `should('have.text', 'Thank you for your order!')` is the business result: the confirmation message.
15. The **negative assertion** `should('not.exist')` verifies the cart badge is gone, since the cart is emptied after an order.

### Example 2: The custom commands

`cypress/support/commands.js`:

```js
Cypress.Commands.add('login', (username = Cypress.env('SAUCE_USER') || 'standard_user') => {
  const password = Cypress.env('SAUCE_PASSWORD');

  cy.session(
    ['sauce-login', username],
    () => {
      cy.visit('/');
      cy.get('[data-test="username"]').type(username);
      cy.get('[data-test="password"]').type(password, { log: false });
      cy.get('[data-test="login-button"]').click();
      cy.url().should('include', '/inventory.html');
    },
    {
      validate() {
        cy.getCookie('session-username').should('exist');
      },
      cacheAcrossSpecs: true,
    }
  );
});

Cypress.Commands.add('addProductToCart', (productName) => {
  cy.contains('[data-test="inventory-item"]', productName)
    .find('button')
    .contains('Add to cart')
    .click();
});
```

**Line-by-line explanation**

1. `Cypress.Commands.add('login', (username = ...) => {...})` defines `cy.login()`. The parameter has a **default value**: it takes `SAUCE_USER` from the environment if present, else `'standard_user'`. Default parameters let you call `cy.login()` with no arguments in the common case, or `cy.login('problem_user')` for another account.
2. `const password = Cypress.env('SAUCE_PASSWORD');` reads the secret from environment configuration (for this site, put `{ "SAUCE_PASSWORD": "secret_sauce" }` in a git-ignored `cypress.env.json`).
3. `cy.session(id, setup, options)`: the `id` array `['sauce-login', username]` makes a distinct cached session per username.
4. The setup function visits the login page, types the username, types the password with `{ log: false }` so the Command Log does not display it, clicks Login, and asserts that the URL changed. That final assertion makes sure the setup really logged in; otherwise `cy.session` would cache a failed login.
5. `validate()` runs after the session is restored from cache. We check that the `session-username` cookie exists (the cookie Sauce Demo sets after login; confirm by looking in your browser's Application tab). If validation fails, Cypress throws away the cache and runs the setup again, so stale sessions heal automatically.
6. `cacheAcrossSpecs: true` shares the session between spec files, saving even more time. If your tests mutate server state that depends on the user, think carefully before sharing.
7. `cy.addProductToCart` takes a product name.
8. `cy.contains('[data-test="inventory-item"]', productName)` finds the product card whose text contains the name.
9. `.find('button')` searches within the card; `.contains('Add to cart')` narrows to the button with that text (so we do not click "Remove" by mistake if the item is already in the cart; instead the command fails loudly, which is what we want).
10. `.click()` performs the click.

### Example 3: Config and env file

`cypress.config.js`:

```js
const { defineConfig } = require('cypress');

module.exports = defineConfig({
  e2e: {
    baseUrl: 'https://www.saucedemo.com',
    viewportWidth: 1440,
    viewportHeight: 900,
    retries: { runMode: 1, openMode: 0 },
  },
});
```

`cypress.env.json` (add to `.gitignore`):

```json
{
  "SAUCE_USER": "standard_user",
  "SAUCE_PASSWORD": "secret_sauce"
}
```

`cypress/support/e2e.js`:

```js
import './commands';
```

**Explanation:** `baseUrl` replaces the long URL; the viewport moves from the test into the config (noise removal); `retries` provide a safety net in CI. The env file keeps credentials out of source control. The support file imports the commands so every spec can use them.

### Example 4: Child command, and overwriting `type` to hide secrets

```js
// Child command: needs an element subject
Cypress.Commands.add('fillAddress', { prevSubject: 'element' }, ($form, address) => {
  cy.wrap($form).within(() => {
    cy.get('[data-test="firstName"]').type(address.firstName);
    cy.get('[data-test="lastName"]').type(address.lastName);
    cy.get('[data-test="postalCode"]').type(address.postalCode);
  });
});

// Usage:
// cy.get('form').fillAddress({ firstName: 'Ada', lastName: 'Lovelace', postalCode: '12345' });
```

**Line-by-line explanation**

1. `{ prevSubject: 'element' }` declares a **child command**: it must be chained off a command that yields a DOM element. Cypress passes that element as the first argument (`$form`, a jQuery object).
2. The callback takes `$form` and our own argument `address`.
3. `cy.wrap($form).within(() => {...})` re-wraps the jQuery element as a Cypress subject and uses `within` to *scope* all queries inside to that form.
4. Inside, three `cy.get().type()` calls fill the fields; because we are scoped, they will not accidentally match elements outside the form.
5. The usage comment shows the chain: `cy.get('form')` yields the form, `.fillAddress(...)` receives it.

### Example 5: A network assertion added during refactor

```js
it('submits the order and receives a created response', () => {
  cy.intercept('POST', '**/api/orders').as('createOrder');

  cy.get('[data-test="finish"]').click();

  cy.wait('@createOrder').then(({ request, response }) => {
    expect(request.body).to.have.property('items').that.has.length(2);
    expect(response.statusCode).to.eq(201);
  });
});
```

**Line-by-line explanation**

1. `cy.intercept('POST', '**/api/orders')` registers a spy on matching requests. `**` is a glob wildcard. The pattern is hypothetical for Sauce Demo (which has no such endpoint); adapt it to your Project 1 API.
2. `.as('createOrder')` gives the intercept an alias.
3. We click Finish, which triggers the request.
4. `cy.wait('@createOrder')` pauses *until* that request happens (default timeout 5 seconds for requests) and yields the interception object.
5. The `.then` callback destructures `request` and `response`.
6. `expect(request.body)...` is a Chai assertion on the request payload: it must have an `items` array of length 2.
7. `expect(response.statusCode).to.eq(201)` asserts the status.

### Example 6: Stability check with repeats (temporary)

```js
describe('Checkout stability (temporary, do not commit)', () => {
  Cypress._.times(10, (i) => {
    it(`passes on repeat ${i + 1}`, () => {
      cy.login();
      cy.visit('/inventory.html');
      cy.addProductToCart('Sauce Labs Backpack');
      cy.get('[data-test="shopping-cart-badge"]').should('have.text', '1');
    });
  });
});
```

**Explanation:** `Cypress._` exposes lodash; `_.times(10, fn)` calls `fn` ten times with the index. Each call defines one `it`, so the Command Log shows ten tests. If any fail, you have a flake to investigate. Delete this block when done.

### Example 7: Adding type hints for IntelliSense in a JavaScript project

`cypress/support/index.d.ts`:

```ts
declare namespace Cypress {
  interface Chainable {
    login(username?: string): Chainable<void>;
    addProductToCart(productName: string): Chainable<void>;
  }
}
```

**Explanation:** Even in a JavaScript project, a `.d.ts` file lets editors such as VS Code auto-complete your custom commands and show their parameters. It is a declaration file, not test code. Using it is optional and the tests stay in JavaScript.

---

## Real-World Scenarios

### Scenario 1: The redesign that broke 150 tests, and the one that broke 3

Team A kept raw recorded selectors such as `div:nth-child(2) > .form_group > input`. A small redesign moved the form's container and 150 tests failed. Team B had refactored selectors to `data-test` attributes and wrapped login in `cy.login()`. After the same redesign, only 3 tests failed (where developers had accidentally removed an attribute), and the fix was a single-line change in a command. Same change, ten-fold difference in cost.

### Scenario 2: Speeding up the pipeline with `cy.session`

A suite of 120 tests each logged in through the UI, costing about 4 seconds per test, i.e. 8 minutes per run on login alone. Introducing `cy.session` reduced it to about one real login per user per run (plus fast restores), saving roughly 7 minutes per pipeline. Over hundreds of pipelines, that is real money and faster feedback.

### Scenario 3: A review finds a "green but useless" test

During code review of a recorded test, a senior engineer asks: "What does this verify?" The author realises the test had no assertions: it would pass even if the checkout page showed an error. Adding the confirmation-header assertion and the subtotal check immediately caught a real tax-calculation bug in the application. Assertions are where tests earn their keep.

### Scenario 4: Data-driven variations

The refactored test moves the customer into a fixture. QA adds `customers.json` with three customers (long name, special characters, non-ASCII). Looping over them with `Cypress._.each` (or defining one `it` per row) creates three tests without copying code. This connects directly to Wednesday's data-driven testing lesson: the principle is the same in every tool.

---

## Common Pitfalls and Best Practices

1. **Refactoring without a safety net.** Run the raw test first; run after every small change.
2. **Mixing refactoring and behaviour changes in one commit.** Separate them.
3. **Replacing `nth-child` with another fragile selector.** Check that the new selector survives reordering, wording changes and resizing.
4. **Too many abstractions.** A command named `doEverything()` hides intent. Keep commands small and named for user intent.
5. **Hidden assertions in commands.** If a command asserts something, say so in its name or documentation, or keep assertions in the test.
6. **Forgetting `cy.visit()` after `cy.session()`.** The page is blank after the session is restored.
7. **Sharing sessions between tests that change user state.** If one test mutates the account (changes the password, empties a wallet), others may break. Use separate users or reset state through the API.
8. **Mutating the cached session without validation.** Provide `validate` so stale sessions refresh.
9. **Storing secrets in the repo.** Use `cypress.env.json` (ignored) or CI secrets.
10. **Using `.then()` for assertions that need retrying.** `.then()` does not retry; use `.should()`.
11. **Leaving `cy.wait(ms)`.** Replace with conditions or aliased requests.
12. **Not rerunning in CI conditions.** A test that passes in headed Chrome on your laptop can fail headless on a smaller viewport.
13. **Deleting assertions to make a test pass.** If the assertion is right and the test fails, you may have found a bug.
14. **Forgetting to add comments for unusual choices.** If you used `{ force: true }` or `{ log: false }`, say why in a brief comment.
15. **Committing temporary stability loops or `cy.pause()` calls.**

---

## Mini Practice Exercises

### Exercise 1: Rename and trim

Take the raw recording from section 1. Without changing selectors yet, (a) rename the suite and test, (b) remove the viewport and the redundant clicks, and (c) convert URLs to relative. Run the test after each change.

*Solution sketch:* suite `Checkout`, test `lets a standard user buy two products`; delete `cy.viewport`, delete every `.click()` that is immediately followed by `.type()` on the same selector; `cy.visit('/')` with `baseUrl` set.

### Exercise 2: Selector upgrade table

Complete the table by writing a stable selector for each fragile one on Sauce Demo:

| Fragile | Stable |
|---|---|
| `#login-button` | ? |
| `.inventory_item:nth-child(1) .btn_inventory` | ? |
| `.shopping_cart_link` | ? |
| `#first-name` | ? |

*Solution:* `[data-test="login-button"]`; `cy.contains('[data-test="inventory-item"]', 'Sauce Labs Backpack').find('button')`; `[data-test="shopping-cart-link"]`; `[data-test="firstName"]`.

### Exercise 3: Add four layers of assertions

Add at least one assertion of each kind: guard, state, outcome, negative. Identify which is which.

*Hint:* use the cart badge, the URL, the confirmation header and the cart badge disappearing.

### Exercise 4: Build `cy.login` with `cy.session`

Create the `login` command. Prove it works by running two tests in the same spec and watching the Command Log: the second test should show the session being *restored* rather than the login steps being repeated. What do you see in the Command Log for a restored session?

*Hint:* look at the `session` row: it reports **created** on the first call and **restored** on later calls (and **recreated** if `validate` fails).

### Exercise 5: Parameterise

Create `cypress/fixtures/customers.json` with three customers and generate one test per customer.

*Solution sketch:*

```js
import customers from '../fixtures/customers.json';

customers.forEach((customer) => {
  it(`completes checkout for ${customer.firstName}`, () => {
    // use customer.* in the type() calls
  });
});
```

(Importing JSON works because Cypress's bundler supports it; alternatively use `cy.fixture` per test.)

### Exercise 6: Review a colleague's generated test (written)

Write a five-point review comment for the raw recording, in the tone you would use on a pull request: kind, specific and actionable.

*Hint:* start with something positive ("Nice that the happy path is covered"), then list: no assertions, fragile selectors, duplicate login, hard-coded data, test name.

---

## Summary / Key Takeaways

- A generated test is a **draft**: it records actions, not intent, and usually has no assertions.
- Use the **checklist**: run it, name it, remove noise, fix selectors, add assertions, remove waits, externalise data, extract duplication, structure with hooks, prove stability.
- Prefer **test attributes** (`data-test`, `data-cy`), scope with `cy.contains(selector, text)` plus `.find()` or `within()`, and avoid positional or style-based selectors.
- Add four layers of assertions: **guards, state, outcome, negative**; and use `cy.intercept` with aliases for network checks and synchronisation.
- Replace `cy.wait(ms)` with conditions; wait for events and states, not time.
- Extract repeated steps into **custom commands**, speed up authentication with **`cy.session`** (remember to `cy.visit` afterwards and provide `validate`), and keep secrets in env files/CI secrets.
- Refactor in **small steps with a passing test** as a safety net, and keep refactoring commits separate from behaviour changes.
- Verify stability by repeated runs in conditions like CI.

---

## External Resources

- Cypress documentation, Custom Commands: https://docs.cypress.io/api/cypress-api/custom-commands
- Cypress documentation, `cy.session()`: https://docs.cypress.io/api/commands/session
- Cypress documentation, Best Practices (selectors, state, waiting): https://docs.cypress.io/app/core-concepts/best-practices
