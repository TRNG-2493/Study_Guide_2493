# Assertions and Annotations in Cypress

## Learning Objectives

By the end of this lesson you will be able to:

- Explain what an assertion is and why a test without assertions is not a test.
- Distinguish between Cypress's three assertion styles: **implicit** (`.should()` / `.and()`), **BDD explicit** (`expect`), and **TDD explicit** (`assert`), and know when each is appropriate.
- Use the most common Chai, Chai-jQuery, and Sinon-Chai assertions for text, values, attributes, CSS, visibility, existence, lengths, classes, and URLs.
- Use `.should()` with a **callback function** to write custom, retried assertions.
- Describe which commands have **built-in (default) assertions** and why `cy.get()` already "asserts" existence.
- Explain how assertions interact with **retry-ability**, and why assertions inside `.then()` do not retry.
- Use Mocha's **annotations**: `describe`, `context`, `it`, `specify`, `.only`, `.skip`, pending tests, and the four hooks `before`, `beforeEach`, `afterEach`, `after`, including execution order and scope.
- Use per-test configuration objects (for example `retries`, `defaultCommandTimeout`, `browser`) as lightweight annotations.
- Compare Cypress assertions and hooks with Playwright's `expect` web-first assertions and pytest fixtures/markers from earlier this week.

---

## Why This Matters

A test that only clicks around and never checks anything will pass even if the application is completely broken. **Assertions are what turn a script into a test.** Every automated check you write answers one question: "Is the application doing what it should?" The assertion is where that question is asked.

*Annotations* (the keywords and structures such as `describe`, `it`, `before`, and `.skip`) are how you organise tests: group them, label them, set up common state, and decide which ones run. Good organisation is the difference between a suite you can maintain for years and one that the team abandons after six months.

In the Week 5 epic you structured Playwright tests with fixtures and hooks (Wednesday) and learned Playwright's `expect` with auto-retrying assertions. Cypress solves the same problems with a different vocabulary. In your Project 1 comparison note you will be able to say precisely how:

| Concept | Playwright (Python, pytest) | Cypress |
|---|---|---|
| Assertion | `expect(locator).to_have_text("x")` (web-first, auto-retrying) | `cy.get(...).should('have.text', 'x')` (auto-retrying) |
| Plain assertion | `assert x == 1` | `expect(x).to.equal(1)` |
| Group of tests | Test module / class | `describe()` / `context()` |
| One test | `def test_login(page):` | `it('logs in', () => {...})` |
| Setup before each | fixture / `setup_method` | `beforeEach()` |
| Setup once | session/module fixture | `before()` |
| Teardown | fixture `yield` code | `afterEach()` / `after()` (with caveats) |
| Skip a test | `@pytest.mark.skip` | `it.skip()` |
| Run only one | `-k name` / `pytest -k` | `it.only()` |
| Soft assertions (continue after a failure) | Not part of the Python API; collect failures manually | Not built in; use a plugin or collect failures manually |

---

## The Concept

### 1. What is an assertion?

An **assertion** is a statement that a condition must be true. If it is true, the test continues. If it is false, the test fails and reports *what was expected and what actually happened*.

Think of an assertion as a bouncer at a club: the test can proceed past that point only if the condition holds. A good assertion message tells you at a glance what went wrong: "expected `<h1>` to have text 'Products' but the text was 'Login'."

Cypress bundles these assertion libraries (you do not install them):

1. **Chai** - the core library (`expect`, `assert`, `should`) with natural-language chains like `to.equal`, `to.be.true`, `to.include`.
2. **Chai-jQuery** - adds assertions for DOM elements: `have.text`, `have.attr`, `have.class`, `be.visible`, `exist`.
3. **Sinon-Chai** - assertions for spies and stubs: `be.calledOnce`, `be.calledWith`.

### 2. The three styles

#### 2.1 Implicit assertions: `.should()` and `.and()`

These are **chained onto Cypress commands**. They are called "implicit" because the subject is passed in automatically from the previous command.

```js
cy.get('[data-test="title"]').should('have.text', 'Products');
cy.get('[data-test="title"]')
  .should('be.visible')
  .and('contain.text', 'Prod');
```

- `.should('have.text', 'Products')` - first argument is the *assertion name* (Chai chain written with dots), second and later are the arguments.
- `.and()` is an alias of `.should()`; use it to chain extra assertions about the same subject for readability ("should be visible **and** contain text...").
- **These assertions retry** along with the preceding query until they pass or the timeout expires. This is why Cypress tests rarely need explicit waits.

This is the recommended style for anything involving the DOM, URL, titles, cookies, or request responses.

#### 2.2 Explicit BDD assertions: `expect`

`expect(value)` is Chai's BDD style. It asserts on a **value you already have**, with a chain of natural language. It is typically used **inside `.then()`** or on plain JavaScript values.

```js
cy.get('[data-test="inventory-item"]').then(($items) => {
  expect($items).to.have.length(6);
  expect($items.first()).to.contain.text('Sauce');
});

const total = 10 + 5;
expect(total).to.equal(15);
expect([1, 2, 3]).to.include(2);
expect({ a: 1, b: 2 }).to.deep.equal({ a: 1, b: 2 });
```

- `expect(...)` receives the value (a jQuery object in the first example).
- `.to.have.length(6)` is a *chain*: `to`, `have` are filler words that make the sentence readable; `length(6)` is the real assertion.
- Explicit assertions **do not retry**. They run once, at the moment the `.then` callback executes.

#### 2.3 Explicit TDD assertions: `assert`

```js
assert.equal(3, 3, 'values should match');
assert.isTrue(true);
assert.deepEqual({ x: 1 }, { x: 1 });
assert.include('hello world', 'world');
assert.isAbove(10, 5);
```

`assert` is Chai's TDD style (a function-call style, like `assertEquals` in Java/JUnit). Functionally equivalent to `expect`; choose one style and be consistent. Most Cypress codebases standardise on `expect` plus `.should()`.

| Style | Syntax | Retries? | Best for |
|---|---|---|---|
| Implicit | `.should('...')`, `.and('...')` | Yes (with the query) | DOM, URL, network results |
| BDD explicit | `expect(x).to...` | No | Values inside `.then()`; computed data |
| TDD explicit | `assert.equal(...)` | No | Same as BDD, if your team prefers it |

### 3. Assertion catalogue

Below is a practical reference. In `.should()` strings, chain parts are joined with dots (`'have.length'`, `'not.be.empty'`, `'to.eq'` is written `'eq'`; the filler words `to` and `be` are optional for implicit assertions).

#### 3.1 Existence and visibility

| Purpose | Example |
|---|---|
| Element exists in DOM | `cy.get('.item').should('exist')` |
| Element does not exist | `cy.get('.spinner').should('not.exist')` |
| Visible | `cy.get('#modal').should('be.visible')` |
| Not visible (hidden but in DOM) | `cy.get('#modal').should('not.be.visible')` |
| Element is enabled/disabled | `cy.get('button').should('be.enabled')` / `'be.disabled'` |
| Checked / selected / focused | `.should('be.checked')`, `.should('be.selected')`, `.should('be.focused')` |
| Empty | `cy.get('input').should('be.empty')` (no value/children, depending on element type) |

Beware: `should('not.be.visible')` **fails if the element does not exist**. Use `should('not.exist')` for absent elements and `'not.be.visible'` only when the element is in the DOM but hidden. (Recent Cypress versions are stricter here than older ones.)

#### 3.2 Text and values

| Purpose | Example |
|---|---|
| Exact text | `.should('have.text', 'Products')` |
| Contains text | `.should('contain.text', 'Prod')` or `.should('contain', 'Prod')` |
| Matches regex | `.invoke('text').should('match', /prod/i)` |
| Input value | `.should('have.value', 'standard_user')` |
| HTML | `.should('have.html', '<b>Hi</b>')` |
| Text is not X | `.should('not.have.text', 'Error')` |

`have.text` compares the element's **full** text *exactly*, including whitespace inside; `contain.text` checks a substring.

#### 3.3 Attributes, properties, CSS, classes

| Purpose | Example |
|---|---|
| Attribute value | `.should('have.attr', 'href', '/inventory.html')` |
| Attribute exists | `.should('have.attr', 'disabled')` |
| Property | `.should('have.prop', 'checked', true)` |
| CSS value | `.should('have.css', 'color', 'rgb(255, 0, 0)')` |
| Class | `.should('have.class', 'active')` |
| Data attribute | `.should('have.data', 'id', 5)` |
| ID | `.should('have.id', 'login-button')` |

CSS values are computed values in `rgb()` form, not the hex or named colour you wrote in a stylesheet.

#### 3.4 Counts and collections

```js
cy.get('li').should('have.length', 5);
cy.get('li').should('have.length.greaterThan', 2);
cy.get('li').should('have.length.at.least', 1);
cy.get('li').should('have.length.lessThan', 10);
```

#### 3.5 Page-level assertions

```js
cy.url().should('include', '/inventory');
cy.url().should('eq', 'https://www.saucedemo.com/inventory.html');
cy.location('pathname').should('eq', '/inventory.html');
cy.title().should('eq', 'Swag Labs');
cy.getCookie('session-username').should('have.property', 'value', 'standard_user');
cy.window().its('localStorage').should('have.property', 'theme', 'dark'); // if present
cy.document().should('have.property', 'charset').and('eq', 'UTF-8');
```

#### 3.6 Values, objects, and arrays (Chai core)

```js
expect(5).to.be.a('number');
expect('hello').to.have.lengthOf(5);
expect([1, 2, 3]).to.have.members([3, 2, 1]);     // same members, any order
expect({ a: 1 }).to.have.property('a', 1);
expect({ a: { b: 2 } }).to.have.nested.property('a.b', 2);
expect(null).to.be.null;
expect(undefined).to.be.undefined;
expect(0).to.not.be.ok;                             // "ok" means truthy; 0 is falsy
expect(7).to.be.within(5, 10);
expect(3.14159).to.be.closeTo(3.14, 0.01);
expect('abc').to.match(/^a/);
expect(() => { throw new Error('x'); }).to.throw('x');
```

Note that Chai's `.to.be.true` and `.to.be.false` are *strict*: `expect(0).to.be.false` fails because `0` is not the boolean `false`. Use `.to.be.ok` / `.to.not.be.ok` for truthy/falsy checks. Property-style assertions such as `.to.be.true` and `.to.be.null` have no parentheses; Chai's proxy support throws an error if you misspell one (for example `.to.be.tru`), so a typo will not silently pass.

#### 3.7 Negation

Add `not` to flip any assertion: `.should('not.have.class', 'disabled')`, `expect(x).to.not.equal(y)`. Be careful with negative assertions: `cy.get('.x').should('not.have.text', 'abc')` passes immediately if the element has *any* other text, even before the app finishes updating. Prefer **positive** assertions on the final state whenever you can, e.g. `.should('have.text', 'Done')`.

#### 3.8 Custom messages

`expect(value, 'cart total should be positive').to.be.greaterThan(0)` – the first argument customises the failure message. Cypress prints it in the Command Log, which helps reviewers.

### 4. `.should()` with a callback

When no built-in assertion expresses your rule, pass a **function**:

```js
cy.get('[data-test="inventory-item-price"]').should(($prices) => {
  const numbers = [...$prices].map((el) => Number(el.innerText.replace('$', '')));
  expect(numbers).to.have.length(6);
  numbers.forEach((n) => expect(n).to.be.within(1, 100));
});
```

**Explanation:**

1. `.should(callback)` calls the function with the subject (a jQuery collection of price elements).
2. Inside, we convert to numbers and use `expect`.
3. **The whole callback is retried** until it stops throwing or times out. That is the key difference from `.then()`: it keeps trying while the page updates.
4. **Rules for the callback:** do not use `cy` commands inside, do not mutate state, and keep it free of side effects (it may run many times).

Compare to Playwright: you would normally compute a list with `all_inner_texts()` and use plain `assert` (which does *not* auto-retry), or use `expect.poll`. Cypress's callback-should retries the entire function, which is helpful for dynamic pages.

### 5. Built-in (default) assertions

Cypress commands carry **implicit expectations** even without `.should()`:

| Command | Built-in expectation |
|---|---|
| `cy.get()`, `cy.contains()`, `.find()` | The element must **exist** in the DOM |
| `cy.visit()` | The server must respond with `2xx` (unless `failOnStatusCode: false`) and the page must load |
| `.click()`, `.type()`, `.check()` | The element must be **actionable** (visible, enabled, not covered, not detached) |
| `cy.request()` | Must receive a response; non-2xx/3xx status fails unless `failOnStatusCode: false` |
| `cy.wait('@alias')` | Request must occur |

That is why `cy.get('#login-button').click()` is already a mini-test: if the button is missing or covered, the test fails.

### 6. Assertions, retries, and `.then()`

Revisit the central rule:

> **Assertions chained with `.should()` retry along with the query before them. Assertions inside `.then()` run once.**

Bad (race condition):

```js
cy.get('.count').then(($el) => {
  expect($el.text()).to.equal('5');   // fails immediately if the text is still "4"
});
```

Good:

```js
cy.get('.count').should('have.text', '5');   // retries until it is "5" or times out
```

Another subtle trap: assertions retry the **last query only**. In `cy.get('.list').find('li').should('have.length', 3)`, both `get` and `find` are queries in Cypress 12+, so the chain is re-run. In an older style, using a *command* such as `.click()` earlier will not be repeated.

### 7. Testing the negative and absence correctly

| Intent | Right | Wrong |
|---|---|---|
| Element disappears (spinner) | `.should('not.exist')` | `.should('not.be.visible')` (fails if gone) |
| Element hidden by CSS | `.should('not.be.visible')` | `.should('not.exist')` |
| Error shown | `.should('be.visible').and('contain.text', 'Epic sadface')` | `cy.contains('Epic sadface')` alone (it only checks existence) |

### 8. Annotations: the Mocha structure

Cypress uses **Mocha's BDD interface**. These keywords are all globals.

#### 8.1 `describe` and `context`

```js
describe('Checkout', () => {
  context('with items in the cart', () => {
    it('shows the order total', () => { /* ... */ });
  });

  context('with an empty cart', () => {
    it('blocks the checkout button', () => { /* ... */ });
  });
});
```

- `describe(name, fn)` creates a suite. `context` is an **alias** used when describing a *condition or state*. They behave identically.
- Suites can nest. Reports show the hierarchy (`Checkout > with items in the cart > shows the order total`).
- Use arrow functions for `describe`; they do not need `this`.

#### 8.2 `it` and `specify`

`it(name, fn)` (alias `specify`) defines a test. The name should describe behaviour.

A test with **no function** is a **pending** test (a placeholder, visible in the report as "pending"):

```js
it('supports gift wrapping');   // to-do; shows as pending
```

This is a convenient way to list planned tests.

#### 8.3 `.only` and `.skip`

```js
it.only('runs just this test', () => {});
it.skip('is temporarily disabled', () => {});
describe.only('runs only this suite', () => {});
describe.skip('skips every test inside', () => {});
context.skip(...);
```

- `.only` tells Mocha to run **only** that test (or suite) in the spec file and skip everything else in it.
- `.skip` marks the test as **pending**: it appears in the results, labelled skipped, but does not run.
- **Commit hygiene:** never merge a stray `.only` into the main branch; it silently disables the rest of the spec. Many teams add a lint rule (`eslint-plugin-mocha` rule `no-exclusive-tests`) to block it. We explore selection techniques in the next lesson ("Test selection").
- Dynamic skipping: inside a `function` test, call `this.skip()`.

#### 8.4 Hooks

Hooks are functions Mocha runs automatically around tests.

| Hook | Runs | Typical use |
|---|---|---|
| `before(fn)` | **Once** before all tests in the suite | Seed data, one-time setup |
| `beforeEach(fn)` | Before **every** test in the suite | `cy.visit`, login, reset state |
| `afterEach(fn)` | After **every** test | Logging, optional cleanup |
| `after(fn)` | **Once** after all tests | One-time cleanup |

Order for nested suites (outer to inner on the way in; inner to outer on the way out):

```js
before(() => cy.log('1. root before'));
beforeEach(() => cy.log('2. root beforeEach'));

describe('inner', () => {
  before(() => cy.log('3. inner before'));
  beforeEach(() => cy.log('4. inner beforeEach'));

  it('test A', () => cy.log('5. test A'));
  it('test B', () => cy.log('7. test B'));

  afterEach(() => cy.log('6/8. inner afterEach'));
  after(() => cy.log('9. inner after'));
});

afterEach(() => cy.log('root afterEach'));
after(() => cy.log('root after'));
```

For test A the order is: root `before` -> inner `before` -> root `beforeEach` -> inner `beforeEach` -> test A -> inner `afterEach` -> root `afterEach`. For test B, the `before` hooks do not run again.

Rules to remember:

1. `before`/`after` hooks run **once per suite**, but since Cypress 12 with **test isolation**, the browser state (cookies, storage, page) is cleared before each test regardless. So a login or `cy.visit` done in `before` **will not persist** into the tests. Put per-test browser setup in `beforeEach`, or use `cy.session`.
2. If a `beforeEach` fails, all remaining tests in that suite are skipped; Cypress treats it as a suite-level failure.
3. **Do not rely on `after`/`afterEach` for critical cleanup**. If the browser crashes or a test is stopped from the Test Runner, they may not run. Cypress's own guidance is to **clean up in `before`/`beforeEach` (reset to a known state at the start)** rather than at the end.
4. Hooks can be defined in `cypress/support/e2e.js` to apply to **every spec**:

```js
// cypress/support/e2e.js
beforeEach(() => {
  cy.log(`Starting: ${Cypress.currentTest.title}`);
});
```

- `Cypress.currentTest.title` and `Cypress.currentTest.titlePath` give the current test name.

#### 8.5 Sharing data between hooks and tests: `this` and aliases

Mocha's context object (`this`) is shared between hooks and the test, when you use a regular `function () {}` (not an arrow):

```js
describe('with this context', () => {
  beforeEach(function () {
    cy.fixture('users').then((users) => {
      this.users = users;       // store on the Mocha context
    });
  });

  it('uses the stored data', function () {
    expect(this.users.standard.username).to.equal('standard_user');
  });
});
```

- Arrow functions do **not** bind `this`, so `this.users` would be undefined. Use `function () {}` when you use `this`.
- Aliases (`.as('users')`) plus `cy.get('@users')` work in arrow functions and are the preferred approach in most teams; both are covered in the fixtures lesson.

#### 8.6 Test configuration objects (annotations as metadata)

You can pass a configuration object as the second argument of `describe` or `it` to override settings for **that suite or test only**:

```js
describe('Slow reports', { defaultCommandTimeout: 15000, retries: 1 }, () => {
  it('generates a monthly report', () => { /* ... */ });
});

it('is mobile-only', { viewportWidth: 375, viewportHeight: 667 }, () => { /* ... */ });

it('runs only in Chrome', { browser: 'chrome' }, () => { /* ... */ });

it('has two retries', { retries: { runMode: 2, openMode: 0 } }, () => { /* ... */ });
```

- `retries` - how many times to re-run a failing test.
- `defaultCommandTimeout`, `requestTimeout`, `responseTimeout` - per-test timeouts.
- `viewportWidth` / `viewportHeight` - per-test viewport (applied automatically, unlike `cy.viewport` which you call inside).
- `browser` - run only in matching browsers (negate with `!`).
- `env` - override environment variables for the test.
- `testIsolation` - at the `describe` level, can disable isolation (an advanced and discouraged option).

This resembles pytest *markers* and Playwright's `test.use` options. Tags for selecting tests (like `@smoke`) are not part of core Cypress; they come from the `@cypress/grep` package, described in the next lesson.

### 9. Handling uncaught exceptions

By default, Cypress **fails the test** if the *application* throws an unhandled JavaScript error. Sometimes third-party scripts (analytics, ads) throw harmless errors. You can choose to ignore specific ones:

```js
Cypress.on('uncaught:exception', (err, runnable) => {
  if (err.message.includes('ResizeObserver loop')) {
    return false;     // returning false tells Cypress not to fail the test
  }
  // otherwise let Cypress fail the test
});
```

Use narrowly; ignoring all exceptions hides real bugs. In Playwright, page errors are not failures unless you listen for the `pageerror` event and decide so; Cypress is stricter by default.

### 10. Assertion-writing guidelines

1. **Assert the outcome the user cares about**, not the implementation: "the cart badge shows 2," not "a `<span>` has class `badge-2`".
2. **One concept per `it`**, but multiple related assertions are fine.
3. **Prefer retryable `.should()`** over `.then()` + `expect` for page state.
4. **Assert on the final state** to avoid racing the application.
5. **Include a "negative" test** for each important rule (invalid input rejected).
6. **Write failure messages for humans**: custom messages or test names that make the failure obvious.
7. **No assertion = no test.** Even `cy.get(...).click()` alone only proves the click was possible.

---

## Code Examples

### Example 1: Full spec with hooks and assertions

```js
describe('Sauce Demo inventory', () => {
  before(() => {
    cy.log('Starting inventory suite');
  });

  beforeEach(() => {
    cy.login('standard_user', 'secret_sauce');   // custom command using cy.session
    cy.visit('/inventory.html');
  });

  it('shows the products page title', () => {
    cy.get('[data-test="title"]').should('have.text', 'Products');
  });

  it('lists six products with names and prices', () => {
    cy.get('[data-test="inventory-item"]').should('have.length', 6);
    cy.get('[data-test="inventory-item-name"]').each(($name) => {
      expect($name.text().trim()).to.not.be.empty;
    });
    cy.get('[data-test="inventory-item-price"]').each(($price) => {
      expect($price.text()).to.match(/^\$\d+\.\d{2}$/);
    });
  });

  it.skip('supports wish lists', () => {
    // feature not built yet
  });

  afterEach(() => {
    cy.log(`Finished: ${Cypress.currentTest.title}`);
  });
});
```

**Line-by-line explanation:**

1. `describe('Sauce Demo inventory', () => {` starts a suite.
2. `before(...)` runs once; `cy.log` prints to the Command Log.
3. `beforeEach(...)` runs before each test: log in using a cached session and visit the page (needed because test isolation clears the page).
4. First test uses `.should('have.text', 'Products')` (implicit, retries). The element `[data-test="title"]` is the "Products" heading on this site.
5. Second test: `have.length` verifies six items. `.each(callback)` loops over each element, passing a jQuery-wrapped element. Inside, `expect` checks that trimmed text is not empty and that each price matches a regex. `.each` is a Cypress command; the `expect` calls inside run once per element and do not retry.
6. `it.skip(...)` marks the third test pending.
7. `afterEach` logs the finished test title using `Cypress.currentTest.title`.

### Example 2: Custom retried assertion for sorted order

```js
it('lists products in alphabetical order by default', () => {
  cy.get('[data-test="inventory-item-name"]').should(($els) => {
    const names = [...$els].map((el) => el.innerText);
    const sorted = [...names].sort((a, b) => a.localeCompare(b));
    expect(names, 'names are A-Z').to.deep.equal(sorted);
  });
});
```

**Explanation:** The callback receives all name elements; `map` extracts text; a copy is sorted with `localeCompare` (locale-aware string comparison); `expect(names, 'names are A-Z')` includes a custom message; `deep.equal` compares arrays by value. Because it is inside `.should`, the callback retries if the data is not ready.

### Example 3: Explicit assertion on API response

```js
it('GET /posts/1 returns the expected shape', () => {
  cy.request('https://jsonplaceholder.typicode.com/posts/1').then((res) => {
    expect(res.status).to.eq(200);
    expect(res.headers['content-type']).to.include('application/json');
    expect(res.body).to.have.all.keys('userId', 'id', 'title', 'body');
    expect(res.body.id).to.be.a('number');
  });
});
```

**Explanation:** `res.status` is the HTTP code; `res.headers` keys are lower-case; `have.all.keys` checks the object has *exactly* those keys; `a('number')` checks type. Explicit style fits because we are examining a plain object that exists right now.

### Example 4: Spying with Sinon-Chai assertions

```js
it('calls window.alert when the user clicks Alert', () => {
  cy.visit('https://example.cypress.io/commands/actions');
  cy.window().then((win) => cy.stub(win, 'alert').as('alert'));
  // trigger the code that would call alert
  cy.window().then((win) => win.alert('Hello'));
  cy.get('@alert').should('have.been.calledOnceWith', 'Hello');
});
```

**Explanation:** `cy.stub(win, 'alert')` replaces `window.alert` with a Sinon stub that records calls and does not open a real dialog; `.as('alert')` aliases it; `have.been.calledOnceWith` is a Sinon-Chai assertion. (Compare Monday's Playwright dialog handling with `page.on("dialog", ...)`: Cypress auto-accepts alerts and exposes them as events, so stubbing is the tool of choice.)

---

## Real-World Scenarios

1. **Flaky "total price" test.** A test used `.then(($el) => expect($el.text()).to.equal('$59.98'))`. It failed one run in ten because the total updates after an API call. Switching to `.should('have.text', '$59.98')` retried for up to four seconds and the flake disappeared.
2. **Accidental `.only`.** A developer committed `it.only(...)`. CI reported 100% pass, with just one test running. The team added `eslint-plugin-mocha`'s `no-exclusive-tests` rule and a CI step that fails on the string `.only(`.
3. **Pending tests as a to-do list.** Before a sprint, QA writes `it('rejects expired coupons')` with no body for every acceptance criterion. The report shows "pending" counts, giving the team a visible backlog.
4. **Shared setup.** Every spec in the shop app needs a cached login. The login is defined once in `support/commands.js` and called in `beforeEach` of each suite; if the login mechanism changes, one file changes.
5. **Third-party script noise.** A marketing script throws a harmless error that fails every test. A narrow `uncaught:exception` handler ignores that one message while still failing the test on genuine application errors.

---

## Common Pitfalls and Best Practices

**Pitfall 1: Using `expect` in `.then()` for page state.** It will not retry; use `.should()`.

**Pitfall 2: `should('not.be.visible')` for an element that does not exist.** Use `should('not.exist')`.

**Pitfall 3: Arrow functions with `this`.** `this.users` is undefined in arrow functions; use `function () {}` or aliases.

**Pitfall 4: Assuming `before` setup persists into every test.** Test isolation clears cookies and storage before each test. Use `beforeEach` or `cy.session`.

**Pitfall 5: Cleanup in `after`.** Hooks may not run if a run is aborted; reset state at the start of tests.

**Pitfall 6: Committed `.only` or forgotten `.skip`.** Lint for them and review PRs for them.

**Pitfall 7: Negative assertions that pass too early.** `should('not.have.text', 'Loading')` passes before the page has even begun loading; assert the final positive state first.

**Pitfall 8: Putting `cy` commands inside a `.should(callback)`.** The callback may run several times; use `.then` for commands.

**Pitfall 9: Assertion overload in one test.** Twenty unrelated assertions make failures hard to diagnose. Group by behaviour.

**Best practices**

- Prefer implicit `.should()` for the DOM and explicit `expect` for computed values.
- Choose one explicit style (`expect`) and stay consistent.
- Name tests as behaviours; use `context` for conditions.
- Put universal hooks in `support/e2e.js`, suite-specific hooks in the spec.
- Reset to a known state at the start; do not depend on end-of-test cleanup.
- Never commit `.only`.

---

## Mini Practice Exercises

**Exercise 1 - Identify the style.**
Classify each as implicit, BDD explicit, or TDD explicit:
a) `cy.get('h1').should('be.visible')`
b) `expect(items).to.have.length(3)`
c) `assert.equal(a, b)`
*Answer:* a) implicit, b) BDD, c) TDD.

**Exercise 2 - Fix the race.**
Rewrite this so it retries:

```js
cy.get('.status').then(($s) => { expect($s.text()).to.eq('Done'); });
```

*Solution:* `cy.get('.status').should('have.text', 'Done');`

**Exercise 3 - Write a callback assertion.**
On the inventory page, write a test that asserts every price is greater than zero and no price exceeds 100, using `.should(callback)`.

*Hint:* map elements to numbers, then loop with `expect(n).to.be.within(0.01, 100)`.

**Exercise 4 - Hook order.**
Without running it, write down the order of log messages for a suite with `before`, `beforeEach`, `afterEach`, `after`, and two tests. Then run it and compare.

**Exercise 5 - Pending list.**
Create a spec that lists five pending tests for a checkout feature (coupon, address validation, empty cart, payment failure, order confirmation). Run it and observe how Cypress reports them.

**Exercise 6 - Per-test configuration.**
Write one test that runs only in Firefox and with a viewport of 375 x 667. Which two properties do you pass in the config object?

*Answer:* `{ browser: 'firefox', viewportWidth: 375, viewportHeight: 667 }`.

**Exercise 7 - Compare.**
Take one Playwright `expect(...)` you wrote this week. Write the Cypress `.should()` equivalent, and add a sentence to your comparison note on how each tool retries.

---

## Summary / Key Takeaways

- An **assertion** states what must be true; without assertions a script is not a test.
- Cypress offers **implicit** assertions (`.should`, `.and`) that **retry**, and **explicit** assertions (`expect`, `assert`) that run once, typically in `.then()`.
- Chai, Chai-jQuery, and Sinon-Chai ship with Cypress. Learn the families: existence/visibility, text/value, attributes/CSS/class, length, URL/title/cookies.
- `.should(callback)` creates custom retried assertions; keep the callback pure and free of `cy` commands.
- Commands such as `get`, `visit`, `click`, and `request` have **built-in assertions** (existence, status, actionability).
- Mocha annotations: `describe`/`context`, `it`/`specify`, pending tests (no callback), `.only`, `.skip`, and the hooks `before`, `beforeEach`, `afterEach`, `after`. With test isolation on, browser state is reset before every test, so use `beforeEach` or `cy.session`.
- Test configuration objects override settings per suite or test (`retries`, `browser`, viewport, timeouts).
- Do not leave `.only` in committed code; do not rely on `after` hooks for critical cleanup.
- Selecting tests by tag or file is covered in the **next lesson (Test selection)**; screenshot and video evidence on failures is **covered in depth on Friday**.

---

## External Resources

- Cypress Documentation - Assertions (including the list of chai/chai-jQuery/sinon-chai assertions): https://docs.cypress.io/app/references/assertions
- Cypress Documentation - Writing and Organizing Tests (Mocha structure, hooks, `.only`, `.skip`): https://docs.cypress.io/app/core-concepts/writing-and-organizing-tests
- Chai Assertion Library - BDD/TDD API reference: https://www.chaijs.com/api/
