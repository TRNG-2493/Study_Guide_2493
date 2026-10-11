# Fixtures and Custom Fixtures in Cypress

## Learning Objectives

By the end of this lesson you will be able to:

- Explain what a **Cypress fixture** is (a static data file) and how it differs from a **Playwright fixture** (a dependency-injection mechanism), so you do not confuse the two.
- Create files in the `cypress/fixtures` folder (JSON, CSV-as-text, images, and others) and load them with `cy.fixture()`.
- Use fixture data in tests with `.then()`, with aliases (`.as()` plus `this.alias` or `cy.get('@alias')`), and in `beforeEach` hooks.
- Use fixtures to **stub network responses** with `cy.intercept` (`{ fixture: 'file.json' }`).
- Use fixtures for **data-driven tests** that generate one `it` per data row, and understand the load-time vs run-time limitation.
- Upload a fixture file with `.selectFile()`.
- Write **custom commands** with `Cypress.Commands.add()` (parent, child, and dual commands), overwrite built-in commands, and use `Cypress.Commands.addQuery`.
- Build the Cypress equivalent of "custom fixtures": reusable setup via custom commands, `cy.session()`, tasks, and hooks in the support file.
- Compare these mechanisms with Playwright/pytest fixtures from Wednesday.

---

## Why This Matters

Two problems appear in every serious test suite:

1. **Test data.** Where do usernames, product lists, API response shapes, and uploaded files come from? Hard-coding strings in every test makes maintenance painful (change one password and you edit forty files) and makes tests hard to read.
2. **Reusable setup.** Almost every test needs to "log in", "create a customer", or "open the cart". Copy-pasting those steps creates duplication and drift.

On Wednesday you solved both problems in Playwright with **fixtures** (pytest-style functions that create and clean up resources and are *injected by name* into tests), **hooks**, and **JSON data-driven testing**. In Cypress, the words are the same but the meanings overlap only partly:

| Need | Playwright / pytest (Wednesday) | Cypress (today) |
|---|---|---|
| Static test data | JSON file read in code or a parametrize list | **Fixture file** in `cypress/fixtures`, loaded by `cy.fixture()` |
| Reusable setup/teardown, dependency injection | **Fixture** functions (`@pytest.fixture`, `conftest.py`) | No injection system. Use **custom commands**, `beforeEach` hooks, `cy.session`, and tasks |
| Cached login | `storage_state` | `cy.session()` |
| Page helpers | Page Object classes | Custom commands or Page Objects (JavaScript classes/modules) |

**This is the single most common point of confusion on Thursday: "fixtures" in Cypress are *data files*. Playwright "fixtures" are *a way to build and share test resources*.** In this lesson we cover both halves: Cypress fixtures proper (data) and the Cypress features that fill the role of Playwright's "custom fixtures" (custom commands and friends).

For Project 1 (QE Foundations), the data-driven JSON approach you used in Playwright translates directly to Cypress fixtures, which will make porting your three tests quick.

---

## The Concept

### Part A - Cypress fixtures (data files)

#### 1. What is a fixture?

A **fixture** is a file containing static data you want your test to use: a list of users, an API response, an image to upload. By convention fixtures live in `cypress/fixtures/` (configurable with `fixturesFolder`).

Why separate data from tests?

- **Readability** - tests describe behaviour; data files describe examples.
- **Reuse** - many tests share one data file.
- **Maintainability** - change a value in one place.
- **Collaboration** - testers or product people can edit JSON without touching test code.
- **Realistic stubbing** - copy a real API response into a fixture and use it to stub the network.

#### 2. Creating a fixture

Create `cypress/fixtures/users.json`:

```json
{
  "standard": {
    "username": "standard_user",
    "password": "secret_sauce"
  },
  "locked": {
    "username": "locked_out_user",
    "password": "secret_sauce",
    "error": "Sorry, this user has been locked out."
  },
  "invalidPassword": {
    "username": "standard_user",
    "password": "wrong_password",
    "error": "Username and password do not match"
  }
}
```

Important JSON rules for beginners: keys and strings use **double quotes**; no trailing commas; no comments. A syntax error here gives a confusing parse error when the fixture loads.

Another fixture, `cypress/fixtures/products.json` (an array):

```json
[
  { "id": 1, "name": "Sauce Labs Backpack", "price": 29.99 },
  { "id": 2, "name": "Sauce Labs Bike Light", "price": 9.99 },
  { "id": 3, "name": "Sauce Labs Onesie", "price": 7.99 }
]
```

#### 3. Loading fixtures with `cy.fixture()`

```js
cy.fixture('users').then((users) => {
  cy.get('[data-test="username"]').type(users.standard.username);
  cy.get('[data-test="password"]').type(users.standard.password);
});
```

**Line by line:**

1. `cy.fixture('users')` reads `cypress/fixtures/users.json`. The extension is optional for JSON (Cypress looks for `users`, `users.json`, `users.js` etc.). It yields the **parsed object**.
2. `.then((users) => { ... })` receives the object.
3. We use dot notation to read `users.standard.username`.

Encodings and other file types:

```js
cy.fixture('logo.png', 'base64').then((b64) => { /* ... */ });   // image as base64 string
cy.fixture('notes.txt').then((text) => { /* string */ });
cy.fixture('data.csv', 'utf8').then((csv) => { /* raw text, parse yourself */ });
```

- JSON files are parsed automatically.
- Images are yielded as a **base64** string by default.
- For other files pass an encoding such as `'utf8'`, `'ascii'`, `'binary'`, or `null` (Buffer).
- Subfolders work: `cy.fixture('api/orders.json')`.

**Caching note:** Cypress may cache fixture data in a run, so mutating the yielded object can affect later reads of the same fixture. When you plan to modify data, clone it first (`structuredClone(users)` or `Cypress._.cloneDeep(users)`), or treat fixtures as read-only.

#### 4. Making fixture data available to several tests

**Option 1 - Alias in `beforeEach` plus `cy.get('@alias')`:**

```js
describe('Login with fixture data', () => {
  beforeEach(() => {
    cy.fixture('users').as('users');   // alias the fixture
    cy.visit('/');
  });

  it('logs in a standard user', () => {
    cy.get('@users').then((users) => {
      cy.get('[data-test="username"]').type(users.standard.username);
      cy.get('[data-test="password"]').type(users.standard.password);
      cy.get('[data-test="login-button"]').click();
      cy.url().should('include', '/inventory.html');
    });
  });
});
```

`cy.fixture('users').as('users')` stores the data under the alias `users`; `cy.get('@users')` retrieves it. Works with arrow functions.

**Option 2 - `this.users` (Mocha context) with `function ()`:**

```js
describe('Login with this context', () => {
  beforeEach(function () {
    cy.fixture('users').as('users');
    cy.visit('/');
  });

  it('shows the locked-out error', function () {
    cy.get('[data-test="username"]').type(this.users.locked.username);
    cy.get('[data-test="password"]').type(this.users.locked.password);
    cy.get('[data-test="login-button"]').click();
    cy.get('[data-test="error"]').should('contain.text', this.users.locked.error);
  });
});
```

When a fixture is aliased, Cypress also exposes it as `this.users` in **non-arrow** functions. This reads more cleanly but requires `function () {}` in both hook and test.

**Option 3 - load once with `before` and store in a variable:**

```js
let users;

before(() => {
  cy.fixture('users').then((data) => {
    users = data;
  });
});

it('uses users', () => {
  cy.get('[data-test="username"]').type(users.standard.username);
});
```

This works because `before` finishes (with the command queue resolved) before any test body runs. It avoids re-reading the fixture per test. Choose whichever style your team prefers; consistency matters more than the choice.

#### 5. Fixtures for stubbing network responses

This is one of the most powerful uses. `cy.intercept` can respond with a fixture file instead of hitting the server:

```js
it('shows products from a stubbed API', () => {
  cy.intercept('GET', '**/api/products', { fixture: 'products.json' }).as('getProducts');
  cy.visit('/shop');
  cy.wait('@getProducts');
  cy.get('.product').should('have.length', 3);
});
```

**Line by line:**

1. `cy.intercept(method, url, staticResponse)` - the third argument can be an object with `fixture`, `statusCode`, `body`, `headers`, `delay`.
2. `{ fixture: 'products.json' }` - respond with the file's contents; the content type is inferred from the extension.
3. `.as('getProducts')` - alias to wait on.
4. `cy.visit` triggers the app to request `/api/products`; Cypress intercepts and replies with the fixture; the real server is never called.
5. `cy.wait('@getProducts')` waits for the request, then we assert on the rendered DOM.

Error and edge states become trivial: a fixture `products-empty.json` containing `[]`, or an inline stub `{ statusCode: 500, body: { message: 'Server error' } }`.

To modify a fixture response dynamically:

```js
cy.intercept('GET', '**/api/products', (req) => {
  req.reply((res) => {
    res.send({ fixture: 'products.json' });
  });
});
```

This form lets you decide at run time (for example, inspect `req.headers`) which fixture to return.

#### 6. Data-driven tests with fixtures

**Problem:** `cy.fixture()` is asynchronous (a Cypress command), but `describe`/`it` blocks are registered *synchronously at load time*. You cannot do:

```js
// WRONG: cy.fixture cannot be used at the top level of describe
cy.fixture('users').then((users) => {
  users.forEach(...)    // it() blocks created here are created too late
});
```

**Two solutions.**

**A. Import the JSON with `require`/`import`** (bundled at load time):

```js
const loginCases = require('../fixtures/login-cases.json');

describe('Login - data driven', () => {
  loginCases.forEach(({ title, username, password, expectedError }) => {
    it(title, () => {
      cy.visit('/');
      if (username) cy.get('[data-test="username"]').type(username);
      if (password) cy.get('[data-test="password"]').type(password);
      cy.get('[data-test="login-button"]').click();
      cy.get('[data-test="error"]').should('contain.text', expectedError);
    });
  });
});
```

`cypress/fixtures/login-cases.json`:

```json
[
  { "title": "empty username", "username": "", "password": "secret_sauce", "expectedError": "Username is required" },
  { "title": "empty password", "username": "standard_user", "password": "", "expectedError": "Password is required" },
  { "title": "locked user", "username": "locked_out_user", "password": "secret_sauce", "expectedError": "locked out" }
]
```

Line by line: `require('../fixtures/login-cases.json')` loads and parses the JSON at spec load (Cypress's bundler handles JSON imports); `forEach` with destructuring creates one `it` per row; test titles come from the data; the `if` guards avoid `type('')`, which throws an error.

This is the direct equivalent of your Wednesday "data-driven testing with JSON" lesson (`json.load` + `pytest.mark.parametrize`).

**B. Loop *inside* a single test with `cy.fixture`:**

```js
it('checks every product page opens', () => {
  cy.fixture('products').then((products) => {
    products.forEach((p) => {
      cy.visit('/inventory.html');
      cy.contains('[data-test="inventory-item-name"]', p.name).click();
      cy.get('[data-test="inventory-item-price"]').should('have.text', `$${p.price}`);
    });
  });
});
```

Here a single test loops; failures are not reported per row. Use A when each row deserves its own result.

#### 7. Uploading a fixture file

Since Cypress 9.3, `.selectFile()` is built in:

```js
cy.get('input[type="file"]').selectFile('cypress/fixtures/example.json');
cy.get('input[type="file"]').selectFile({
  contents: 'cypress/fixtures/avatar.png',
  fileName: 'my-avatar.png',
  mimeType: 'image/png',
});
cy.get('.dropzone').selectFile('cypress/fixtures/example.json', { action: 'drag-drop' });
```

Notes: paths are relative to the project root; you can also pass `@alias`; `action: 'drag-drop'` simulates dropping onto a drop zone. This parallels the file upload lesson from Tuesday (`set_input_files` in Playwright).

---

### Part B - The Cypress equivalent of "custom fixtures": custom commands and reusable setup

Playwright fixtures can *provide* a logged-in page, a created user, or a Page Object, and *clean up* afterwards. Cypress has no `test.extend`, but you can achieve the same goals with the following building blocks.

#### 8. Custom commands: `Cypress.Commands.add()`

A **custom command** is a function you register once and call anywhere as `cy.yourCommand()`. They are defined in `cypress/support/commands.js`, which is imported by `cypress/support/e2e.js`.

```js
// cypress/support/commands.js
Cypress.Commands.add('loginViaUi', (username, password) => {
  cy.visit('/');
  cy.get('[data-test="username"]').type(username);
  cy.get('[data-test="password"]').type(password, { log: false });
  cy.get('[data-test="login-button"]').click();
  cy.url().should('include', '/inventory.html');
});
```

Usage in any spec:

```js
cy.loginViaUi('standard_user', 'secret_sauce');
```

**Line by line:**

1. `Cypress.Commands.add(name, callback)` registers `cy.<name>`.
2. The callback receives whatever arguments the caller passes.
3. Inside, you use ordinary `cy` commands; they are queued as part of the caller's chain.
4. `{ log: false }` on the password hides it from the Command Log.

#### 8.1 Parent, child, and dual commands

```js
// Parent command (default): starts a chain
Cypress.Commands.add('getByTest', (value) => cy.get(`[data-test="${value}"]`));

// Child command: requires a previous subject
Cypress.Commands.add('typeAndEnter', { prevSubject: 'element' }, (subject, text) => {
  cy.wrap(subject).type(`${text}{enter}`);
});

// Dual command: works with or without a subject
Cypress.Commands.add('findByText', { prevSubject: 'optional' }, (subject, text) => {
  return subject ? cy.wrap(subject).contains(text) : cy.contains(text);
});
```

Usage:

```js
cy.getByTest('username').typeAndEnter('standard_user');   // child on the element
cy.findByText('Products');                                // parent use
cy.get('.inventory_list').findByText('Backpack');         // child use
```

`prevSubject` options: `true`, `'element'`, `'document'`, `'window'`, `'optional'`, or an array of these. `subject` is the first callback argument.

Returning values: a custom command's yield is the result of the last Cypress command inside, or the value you `return`. Do **not** mix returning a value and queuing Cypress commands inconsistently; return the `cy.` chain you want to yield.

#### 8.2 A realistic "fixture-like" login command with `cy.session`

```js
Cypress.Commands.add('login', (username = 'standard_user', password = 'secret_sauce') => {
  cy.session(
    [username, password],
    () => {
      cy.visit('/');
      cy.get('[data-test="username"]').type(username);
      cy.get('[data-test="password"]').type(password, { log: false });
      cy.get('[data-test="login-button"]').click();
      cy.url().should('include', '/inventory.html');
    },
    { cacheAcrossSpecs: true }
  );
});
```

- Default parameters (`username = 'standard_user'`) let you call `cy.login()` with no arguments.
- `cy.session` caches the logged-in browser state per user.
- `cacheAcrossSpecs: true` reuses the session across spec files in the same run (instead of only within a spec).

This replaces what in Playwright you would do with a `logged_in_page` fixture and `storage_state`.

#### 8.3 Combining fixture data and commands

```js
Cypress.Commands.add('loginAs', (role) => {
  cy.fixture('users').then((users) => {
    const { username, password } = users[role];
    cy.login(username, password);
  });
});
```

Usage: `cy.loginAs('standard');`. Test code is now free of credentials and mechanics: that is the heart of a reusable, readable suite.

#### 8.4 Overwriting built-in commands

```js
Cypress.Commands.overwrite('visit', (originalFn, url, options) => {
  cy.log(`Visiting ${url}`);
  return originalFn(url, options);
});
```

`overwrite` replaces a command's behaviour while allowing you to call the original (`originalFn`). Use sparingly; surprising overrides confuse teammates. A frequent legitimate use is masking sensitive values in `type`.

#### 8.5 Custom queries

Since Cypress 12, `Cypress.Commands.addQuery(name, fn)` defines a **retryable query**, like `cy.get`. Custom queries are an advanced topic; for most teams a normal command wrapping `cy.get` (like `getByTest`) is sufficient. The key rule is that a query's callback must be synchronous and must return a function that Cypress re-runs on each retry. Because the exact pattern is subtle, read the official "Custom Queries" documentation before writing one; most tests never need it.

#### 9. TypeScript support for custom commands

If you use TypeScript, declare the command so autocomplete and compile checks work:

```ts
// cypress/support/index.d.ts (or in commands.ts)
declare global {
  namespace Cypress {
    interface Chainable {
      login(username?: string, password?: string): Chainable<void>;
      getByTest(value: string): Chainable<JQuery<HTMLElement>>;
    }
  }
}
export {};
```

JavaScript users can add JSDoc or ignore this step.

#### 10. Other reusable-setup tools

| Tool | What it does | Playwright analogue |
|---|---|---|
| `beforeEach`/`before` in a spec | Per-suite setup | pytest fixture with scope function/module |
| Global hooks in `cypress/support/e2e.js` | Run before every spec | `autouse=True` fixtures in `conftest.py` |
| `cy.session()` | Cache login state | `storage_state` / auth fixture |
| `cy.task()` + `setupNodeEvents` | Run Node code: seed database, reset data | Fixtures that talk to the DB with Python |
| `cy.request()` | Seed data through API | API-based fixture |
| Page Objects (classes/modules) | Group selectors and actions | Page Object Model (Wednesday) |
| `Cypress.env()` / `cypress.env.json` | Environment-specific data | `pytest.ini`, env vars |

Example: database seeding with a task.

```js
// cypress.config.js
setupNodeEvents(on, config) {
  on('task', {
    resetDatabase() {
      // run your Node DB script here
      return null;
    },
    seedUser({ name }) {
      // insert into DB and return the created record
      return { id: 1, name };
    },
  });
  return config;
},
```

```js
// in a spec
beforeEach(() => {
  cy.task('resetDatabase');
  cy.task('seedUser', { name: 'Ada' }).then((user) => {
    cy.wrap(user).as('user');
  });
});
```

This is the closest thing to a Playwright fixture that creates and *later* removes a resource. Because Cypress does not guarantee after-hooks, the design is to **reset at the start** (`resetDatabase` in `beforeEach`).

#### 11. A simple Page Object in Cypress (brief)

You built Page Objects on Wednesday. They work the same way in Cypress, but methods *queue* commands and usually return `this` or nothing:

```js
// cypress/support/pages/LoginPage.js
class LoginPage {
  visit() { cy.visit('/'); return this; }
  username() { return cy.get('[data-test="username"]'); }
  password() { return cy.get('[data-test="password"]'); }
  submit() { cy.get('[data-test="login-button"]').click(); return this; }
  loginAs(user, pass) {
    this.username().type(user);
    this.password().type(pass, { log: false });
    return this.submit();
  }
}
export default new LoginPage();
```

```js
import loginPage from '../support/pages/LoginPage';
it('logs in', () => {
  loginPage.visit().loginAs('standard_user', 'secret_sauce');
  cy.url().should('include', '/inventory');
});
```

Cypress's own guidance leans toward custom commands and `cy.session` over heavy Page Objects, but both are accepted; choose what your team reads best.

---

## Code Examples

### Example 1: Complete data-driven login with fixtures and custom command

`cypress/fixtures/users.json` (as above)

`cypress/support/commands.js`:

```js
Cypress.Commands.add('loginAs', (role) => {
  cy.fixture('users').then((users) => {
    const { username, password } = users[role];
    cy.get('[data-test="username"]').type(username);
    cy.get('[data-test="password"]').type(password, { log: false });
    cy.get('[data-test="login-button"]').click();
  });
});
```

`cypress/e2e/login-fixture.cy.js`:

```js
describe('Login using fixtures', () => {
  beforeEach(() => cy.visit('/'));

  it('standard user reaches the inventory', () => {
    cy.loginAs('standard');
    cy.url().should('include', '/inventory.html');
  });

  it('locked user sees an error', () => {
    cy.loginAs('locked');
    cy.fixture('users').then((users) => {
      cy.get('[data-test="error"]').should('contain.text', users.locked.error);
    });
  });
});
```

**Explanation:**

- The custom command hides credential handling. `users[role]` uses bracket notation to pick `standard` or `locked`.
- Destructuring `const { username, password } = users[role];` extracts the two properties into variables.
- The test then reads the same fixture to compare the error text with the expected one stored in the file; the expected message lives in data, not in the test.
- `beforeEach` visits the page each time (test isolation).

### Example 2: Stub empty and error states

```js
describe('Products list states', () => {
  it('shows an empty-state message when there are no products', () => {
    cy.intercept('GET', '**/api/products', { body: [] }).as('empty');
    cy.visit('/shop');
    cy.wait('@empty');
    cy.contains('No products found').should('be.visible');
  });

  it('shows an error banner on a server error', () => {
    cy.intercept('GET', '**/api/products', { statusCode: 500, body: { message: 'Boom' } }).as('fail');
    cy.visit('/shop');
    cy.wait('@fail');
    cy.get('[data-test="error-banner"]').should('be.visible');
  });
});
```

(The `/shop` page and its texts are illustrative; adapt to your app or the mock server you use in Project 1.)

**Explanation:** inline `body` stubs avoid creating a file for trivial responses; larger payloads belong in fixtures. Both tests make a *deterministic* UI check that would be impractical against a real backend.

### Example 3: Fixture upload

```js
it('uploads a profile photo', () => {
  cy.visit('/profile');
  cy.get('input[type="file"]').selectFile('cypress/fixtures/avatar.png');
  cy.get('[data-test="upload-success"]').should('contain.text', 'avatar.png');
});
```

**Explanation:** `selectFile` attaches the file to the input as if the user picked it. The path begins from the project root, not from the spec. (`/profile` is illustrative.)

### Example 4: Playwright (Python) fixture vs Cypress command side by side

Playwright with pytest (Wednesday style):

```python
# conftest.py
import pytest

@pytest.fixture
def logged_in_page(page):
    page.goto("https://www.saucedemo.com")
    page.get_by_placeholder("Username").fill("standard_user")
    page.get_by_placeholder("Password").fill("secret_sauce")
    page.get_by_role("button", name="Login").click()
    yield page           # the test runs here
    # teardown code could run after yield

def test_inventory_loads(logged_in_page):
    assert "inventory" in logged_in_page.url
```

Cypress:

```js
// support/commands.js
Cypress.Commands.add('login', () => { /* cy.session version above */ });

// spec
beforeEach(() => {
  cy.login();
  cy.visit('/inventory.html');
});

it('inventory loads', () => {
  cy.url().should('include', 'inventory');
});
```

Differences to discuss in your note:

- Playwright's fixture is **requested by name** as a test argument (dependency injection), and has built-in teardown after `yield`.
- Cypress calls a command explicitly in a hook; teardown is by resetting at the beginning, because after-hooks are not guaranteed.
- The Playwright fixture can also create *different objects* (a `page`, an API client); Cypress commands only queue actions on the one global `cy`.

---

## Real-World Scenarios

1. **Realistic stubs.** The backend for an order-history page is not ready. The front-end team saves an agreed API response as `orders.json` and the tests run against it with `cy.intercept`. When the backend is delivered, only the `intercept` line is removed.
2. **Role-based tests.** An admin console has Admin, Editor, and Viewer roles. A `users.json` fixture holds credentials for each and `cy.loginAs('editor')` makes role tests one line.
3. **Edge-case catalogue.** QE collects tricky inputs (emoji names, 255-character addresses, SQL-like strings) in `edge-cases.json` and generates one test per entry.
4. **File upload regression.** `fixtures/` holds a 1 KB valid PDF, a 20 MB file for the "too large" case, and a `.exe` for the "unsupported type" case.
5. **Shared login for hundreds of tests.** A single `cy.login()` custom command with `cy.session` shaves 3 seconds from each of 300 tests, saving 15 minutes per run.

---

## Common Pitfalls and Best Practices

**Pitfall 1: Mixing up Cypress and Playwright "fixtures."** In Cypress, a fixture is a data file. Do not search for `test.extend` or fixture injection; use commands and hooks.

**Pitfall 2: Using `cy.fixture` at the top level of `describe`.** Data-driven tests need `require`/`import` for load-time data.

**Pitfall 3: `this.users` with arrow functions.** `this` is not bound. Use `function () {}` or `cy.get('@users')`.

**Pitfall 4: Invalid JSON.** A trailing comma or single quotes yields errors. Validate with an editor or `JSON.parse`.

**Pitfall 5: Mutating cached fixture data.** Clone before changing.

**Pitfall 6: Storing real secrets in fixtures.** Fixtures are committed to git. Put real passwords in `cypress.env.json` or CI secrets; fixtures hold only test-safe data.

**Pitfall 7: Over-engineering commands.** A custom command that hides ten steps and four branches is hard to debug. Keep commands small, named by intent, and with clear logging.

**Pitfall 8: Relying on after-hooks to clean up.** Reset state in `before`/`beforeEach` instead.

**Pitfall 9: Forgetting to import commands.** `cypress/support/e2e.js` must import `./commands` (the default scaffold does). If `cy.login is not a function`, check the import.

**Pitfall 10: Returning inconsistent values from commands.** Return the final `cy` chain, or use `.then()`; do not `return` a plain value while also queuing commands.

**Best practices**

- Treat fixtures as read-only data; name them by purpose (`users.json`, `products-empty.json`).
- Keep one concept per fixture file.
- Prefer commands for *actions*, fixtures for *data*, and `cy.session` for authentication.
- Document each custom command with a JSDoc comment.
- Keep selectors in one place (commands or page objects).
- Reset data at the start of tests.

---

## Mini Practice Exercises

**Exercise 1 - Vocabulary check.**
In two sentences, explain to a classmate the difference between a Playwright fixture and a Cypress fixture.

*Sample answer:* "A Playwright fixture is a function that prepares (and cleans up) resources and is injected into tests by parameter name. A Cypress fixture is a static data file in `cypress/fixtures`, read with `cy.fixture()`."

**Exercise 2 - Load and use.**
Create `cypress/fixtures/credentials.json` with a valid and an invalid user. Write a test that uses `cy.fixture` and `.then()` to log in as the valid user.

**Exercise 3 - Alias and `this`.**
Rewrite Exercise 2 twice: once with `.as()` plus `cy.get('@alias')` in arrow functions, once with `this.alias` in regular functions.

**Exercise 4 - Data-driven.**
Create `login-cases.json` with five rows (including empty username and a locked-out user). Generate one test per row using `require`. Observe the five separate results in the runner.

**Exercise 5 - Stub.**
Visit `https://example.cypress.io/commands/network-requests`, which has a button that fetches a comment from `/comments/1`. Save a fake comment object as `cypress/fixtures/comment.json`, intercept `GET **/comments/*` with `{ fixture: 'comment.json' }`, click the "Get Comment" button, and assert that the page shows your fake data. *Hint:* intercepts only affect requests made by the page, not `cy.request`; register the intercept before the click.

**Exercise 6 - Custom command.**
Write a custom command `cy.addToCart(productName)` that locates the product card by name and clicks its button. Use it in a test that adds two products and asserts the badge shows `2`.

*Solution sketch:*

```js
Cypress.Commands.add('addToCart', (productName) => {
  cy.contains('[data-test="inventory-item"]', productName).find('button').click();
});
```

**Exercise 7 - Compare.**
Re-read your Wednesday Playwright fixture or `conftest.py`. List what you would use in Cypress for each of its responsibilities (login, test data, teardown). Add the list to your comparison note.

---

## Summary / Key Takeaways

- A **Cypress fixture** is a static **data file** in `cypress/fixtures`, loaded by `cy.fixture()`. A **Playwright fixture** is a **dependency-injection mechanism** for setup and teardown. They share a name, not a meaning.
- Load fixtures with `.then()`, aliases, `this.alias` (non-arrow functions), or a `before` hook. Treat them as read-only; clone before modifying.
- Fixtures are ideal for **stubbing network responses** (`cy.intercept(..., { fixture })`), **data-driven tests** (use `require`/`import` for load-time data), and **file uploads** (`.selectFile()`).
- The Cypress counterpart of "custom fixtures" is built from **custom commands** (`Cypress.Commands.add`, parent/child/dual), **`cy.session()`**, **hooks**, **tasks**, and optionally Page Objects.
- Reset state at the start of tests; do not rely on after-hooks.
- Keep secrets out of fixtures; keep commands small and well-named.
- Detailed debugging of command sequences and captured evidence is **covered in depth on Friday**.

---

## External Resources

- Cypress Documentation - `cy.fixture()`: https://docs.cypress.io/api/commands/fixture
- Cypress Documentation - Custom Commands: https://docs.cypress.io/api/cypress-api/custom-commands
- Cypress Documentation - `cy.intercept()`: https://docs.cypress.io/api/commands/intercept
