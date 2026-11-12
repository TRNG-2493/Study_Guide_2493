# Cypress Class Handout 01

> **For:** students who already know Playwright and are new to Cypress.
> **Covers:** 1. Architecture & Setup · 2. Browser Management · 3. Writing Tests · 4. Locating Elements · 5. Interaction · 6. Assertions & Annotations
>
> **How to use this handout:** each topic has a **definition**, a few **key ideas**, a **worked example** we build together **step by step**, a **checkpoint** that shows what you should see, and a **Your turn** exercise.

---

## Before Class

You need:

- **Node.js** (LTS version) and **npm**: check with `node -v` and `npm -v`
- **VS Code** (or any editor)
- **Chrome** and **Firefox** installed
- Internet access to `https://www.saucedemo.com`, `https://example.cypress.io` and `https://the-internet.herokuapp.com`

**Practice app login (saucedemo):** user `standard_user` · password `secret_sauce`

---

# Topic 1: Cypress Architecture and Setup

### Definition

**Cypress** is a JavaScript end-to-end testing framework. Your test code runs **inside the browser**, in the same run loop as the application under test. A **Node.js server** behind it handles network proxying, files, screenshots and videos.

### Key ideas

```
┌──────────────────────────────────────────────────────────────┐
│                         BROWSER                              │
│  ┌──────────────────────────┐   ┌──────────────────────────┐ │
│  │   Cypress Runner UI      │   │   Application Under Test │ │
│  │  (Command Log, spec      │◄─►│   (loaded in an iframe)  │ │
│  │   iframe runs YOUR test) │   │   same run loop, direct  │ │
│  └────────────┬─────────────┘   │   access to DOM/window   │ │
│               │                 └────────────▲─────────────┘ │
└───────────────┼──────────────────────────────┼───────────────┘
                │ WebSocket                    │ HTTP(S)
┌───────────────▼──────────────────────────────┴───────────────┐
│                  CYPRESS NODE.JS SERVER                      │
│  • Proxy: every request/response passes through it           │
│    (enables cy.intercept, cookie handling, header rewrites)  │
│  • Runs cy.task(), reads/writes files (cy.readFile/fixture)  │
│  • Launches & controls the browser, takes screenshots/video  │
│  • Loads cypress.config.js and plugins (setupNodeEvents)     │
└──────────────────────────────────────────────────────────────┘
                                │
                                ▼
                       Your web server / APIs
```

1. Playwright drives the browser **from outside**. Cypress runs **inside** it.
2. `cy` commands are **queued**, not awaited. **No `async`/`await`.**
3. Queries and assertions **retry automatically** (4 seconds by default), so you rarely need waits.

### Worked example: set up a project and run your first test

**Step 1: Create the project and install Cypress**

```bash
mkdir cypress-class && cd cypress-class
npm init -y
npm install cypress --save-dev
```

**Step 2: Open Cypress**

```bash
npx cypress open
```

In the window that opens: **E2E Testing** → **Continue** → choose **Chrome** → **Start E2E Testing** → **Create new spec**.

**Step 3: Look at what Cypress created**

```
cypress/
├── e2e/          ← your tests go here (*.cy.js)
├── fixtures/     ← test data
└── support/      ← custom commands and global setup
cypress.config.js ← configuration
```

**Step 4: Set the `baseUrl`.** Replace the contents of `cypress.config.js`:

```js
const { defineConfig } = require('cypress');

module.exports = defineConfig({
  e2e: {
    baseUrl: 'https://www.saucedemo.com',
  },
});
```

Close the Cypress window and run `npx cypress open` again. **Config changes need a restart.**

**Step 5: Write the first test.** Create `cypress/e2e/first.cy.js`:

```js
describe('My first test', () => {
  it('opens the saucedemo login page', () => {
    cy.visit('/');                      // baseUrl + '/'
    cy.title().should('eq', 'Swag Labs');
  });
});
```

**Step 6: Run it, two ways**

```bash
npx cypress open    # click first.cy.js in the list
npx cypress run --spec cypress/e2e/first.cy.js
```

### ✅ Checkpoint

- In `open` mode the test turns **green**, and the **Command Log** on the left shows `visit` and `title`.
- In `run` mode the terminal shows `1 passing`.

### 💡 Playwright tip

There's no `page` object and no `await`. `cy` is a global, and you write commands one after another.

### ✏️ Your turn

1. Add a second test to `first.cy.js` that checks the login button is visible: `cy.get('[data-test=login-button]').should('be.visible')`.
2. Run only your spec in **Firefox**: `npx cypress run --spec cypress/e2e/first.cy.js --browser firefox`.

---

# Topic 2: Browser Management

### Definition

**Browser management** covers which browser runs your tests, how it's launched, what state (cookies, storage) carries over between tests, and how tests handle viewports, tabs and dialogs. Cypress runs **one browser with one tab**, and clears state **before every test**.

### Key ideas

1. Choose a browser with `--browser chrome | firefox | edge | electron`. Electron is the default.
2. **Test isolation:** cookies and storage are cleared before each test, like a new Playwright context.
3. `cy.session()` caches a login, like Playwright's `storageState`.
4. New tabs aren't supported, and alerts are accepted automatically.

### Worked example A: cache the login with `cy.session()`

**Step 1: Create `cypress/e2e/session.cy.js` with a login helper**

```js
const login = (user) => {
  cy.session(user, () => {
    cy.visit('/');
    cy.get('[data-test=username]').type(user);
    cy.get('[data-test=password]').type('secret_sauce');
    cy.get('[data-test=login-button]').click();
    cy.url().should('include', '/inventory.html');
  });
};
```

**Step 2: Use it in `beforeEach`, then visit the page.** `cy.session` leaves you on a blank page, so `cy.visit` must come after it.

```js
describe('Inventory', () => {
  beforeEach(() => {
    login('standard_user');
    cy.visit('/inventory.html', { failOnStatusCode: false });
  });

  it('shows the Products title', () => {
    cy.get('.title').should('have.text', 'Products');
  });

  it('shows 6 products', () => {
    cy.get('.inventory_item').should('have.length', 6);
  });
});
```

**Step 3: Run it and expand `session` in the Command Log for each test.**

### ✅ Checkpoint

- Test 1: the session is **created** (the login steps run).
- Test 2: the session is **restored** (no login steps), so it's faster.

### Worked example B: handle a confirm dialog

**Step 1: Create `cypress/e2e/dialogs.cy.js`**

```js
it('cancels a confirm dialog', () => {
  cy.visit('https://the-internet.herokuapp.com/javascript_alerts');
```

**Step 2: Tell Cypress to click "Cancel" *before* the dialog appears.** Returning `false` means Cancel.

```js
  cy.on('window:confirm', () => false);
```

**Step 3: Trigger the dialog and check the result**

```js
  cy.contains('button', 'Click for JS Confirm').click();
  cy.get('#result').should('have.text', 'You clicked: Cancel');
});
```

### 💡 Playwright tip

`page.on('dialog', d => d.dismiss())` → `cy.on('window:confirm', () => false)`

### ✏️ Your turn

1. In `dialogs.cy.js`, add a test that checks the **alert** text is `I am a JS Alert`:
   `cy.on('window:alert', (text) => expect(text).to.eq('I am a JS Alert'))`
2. Add a test that shrinks the viewport with `cy.viewport('iphone-x')` on saucedemo's login page and checks the login button is still visible.
3. Run `session.cy.js` in Chrome and in Firefox.

---

# Topic 3: Writing Cypress Tests

### Definition

A **Cypress test** is a `*.cy.js` file in `cypress/e2e/`. It uses **Mocha** for structure (`describe`, `it`, hooks), the global **`cy`** to queue commands, and **Chai** assertions that retry. Each test follows **Arrange → Act → Assert**.

### Key ideas

| Cypress | Playwright |
|---|---|
| `describe()` / `it()` | `test.describe()` / `test()` |
| `before` / `beforeEach` / `afterEach` / `after` | `beforeAll` / `beforeEach` / `afterEach` / `afterAll` |
| `it.only` / `it.skip` | `test.only` / `test.skip` |

### Worked example: build a login test step by step

**Step 1: Create `cypress/e2e/login.cy.js` with an empty structure**

```js
describe('Login', () => {
  it('logs in with valid credentials', () => {
    // Arrange
    // Act
    // Assert
  });
});
```

**Step 2: Arrange (go to the login page)**

```js
    cy.visit('/');
```

**Step 3: Act (fill in the form and submit)**

```js
    cy.get('[data-test=username]').type('standard_user');
    cy.get('[data-test=password]').type('secret_sauce');
    cy.get('[data-test=login-button]').click();
```

**Step 4: Assert (check that we landed on the products page)**

```js
    cy.url().should('include', '/inventory.html');
    cy.get('.title').should('have.text', 'Products');
```

Run it. ✅ It should pass.

**Step 5: Add a negative test.** Add this inside the same `describe`:

```js
  it('shows an error for a wrong password', () => {
    cy.visit('/');
    cy.get('[data-test=username]').type('standard_user');
    cy.get('[data-test=password]').type('wrong');
    cy.get('[data-test=login-button]').click();
    cy.get('[data-test=error]').should('contain', 'do not match');
  });
```

**Step 6: Remove the duplication.** Both tests start with `cy.visit('/')`, so move it into `beforeEach`:

```js
describe('Login', () => {
  beforeEach(() => {
    cy.visit('/');
  });

  it('logs in with valid credentials', () => {
    cy.get('[data-test=username]').type('standard_user');
    cy.get('[data-test=password]').type('secret_sauce');
    cy.get('[data-test=login-button]').click();
    cy.url().should('include', '/inventory.html');
  });

  it('shows an error for a wrong password', () => {
    cy.get('[data-test=username]').type('standard_user');
    cy.get('[data-test=password]').type('wrong');
    cy.get('[data-test=login-button]').click();
    cy.get('[data-test=error]').should('contain', 'do not match');
  });
});
```

**Step 7: See the command queue for yourself.** Add this line at the end of the first test, run it, and open DevTools (F12 → Console):

```js
    console.log('Does this print first or last?');
```

### ✅ Checkpoint

- Both tests pass.
- The `console.log` message prints **before** the Cypress commands run, because `cy` commands are queued.

### ⚠️ Common errors

| Error | Fix |
|---|---|
| Spec isn't in the list | Save it in `cypress/e2e/` with a name ending in `.cy.js` |
| `cy.visit('/')` opens the wrong site | Check `baseUrl` and restart Cypress |
| "Expected to find element…" | Check the selector, and click the failing command to see the page at that moment |

### ✏️ Your turn

1. Add a test for the **locked-out user** (`locked_out_user`). The error contains `locked out`.
2. Add a test that clicks **Login** with empty fields. The error contains `Username is required`.
3. Write `logout.cy.js`: log in, click the menu (`#react-burger-menu-btn`), click **Logout** (`#logout_sidebar_link`), and assert the login button is visible again.

---

# Topic 4: Element Location and Selection

### Definition

**Element location** is how a test finds the DOM elements it acts on or checks. **Queries** such as `cy.get()` (CSS selector) and `cy.contains()` (text) find elements. **Traversal** commands such as `.find()`, `.eq()` and `.within()` narrow them down.

### Key ideas

| Command | Returns |
|---|---|
| `cy.get('selector')` | **All** matching elements |
| `cy.contains('text')` / `cy.contains('selector', 'text')` | The **first** element containing the text |
| `.find('selector')` | Matching elements **inside** the current one |
| `.first()` / `.last()` / `.eq(i)` | One element by position |
| `.within(() => {...})` | Scopes every query inside one element |

**Choose selectors in this order:** `[data-test=…]` → visible text → `#id` → *avoid* classes and positions.

### Worked example: add a product by its name

**Step 1: Create `cypress/e2e/locate.cy.js` and log in in `beforeEach`**

```js
describe('Locating products', () => {
  beforeEach(() => {
    cy.visit('/');
    cy.get('[data-test=username]').type('standard_user');
    cy.get('[data-test=password]').type('secret_sauce');
    cy.get('[data-test=login-button]').click();
  });
```

**Step 2: Try `cy.get()`. How many products are there?**

```js
  it('counts the products', () => {
    cy.get('.inventory_item').should('have.length', 6);
  });
```

**Step 3: Try `cy.get('button')`. Why is it a bad choice for clicking?**

```js
  it('shows why a broad selector is risky', () => {
    cy.get('.inventory_item button').should('have.length', 6); // 6 buttons, so which one?
  });
```

**Step 4: Find the card by its product name, then the button inside it**

```js
  it('adds the Bolt T-Shirt by name', () => {
    cy.contains('.inventory_item', 'Sauce Labs Bolt T-Shirt') // the card with this text
      .find('button')                                          // the button inside that card
      .click();

    cy.get('.shopping_cart_badge').should('have.text', '1');
  });
});
```

**Step 5: Use the Selector Playground.** In the runner, click the **crosshair icon**, then click any product name. Cypress suggests a selector. Compare it with yours.

### ✅ Checkpoint

- All three tests pass, and the cart badge shows `1`.
- Clicking `contains` in the Command Log **highlights the right card**.

### Worked example: find a value in a table row

```js
it('finds Jason Doe\'s email', () => {
  cy.visit('https://the-internet.herokuapp.com/tables');
  cy.contains('#table2 tbody tr', 'Doe')   // step 1: the row that contains "Doe"
    .find('.email')                        // step 2: the email cell in that row
    .should('have.text', 'jdoe@hotmail.com');
});
```

### 💡 Playwright tip

`page.locator('.card').filter({ hasText: 'X' }).locator('button')` → `cy.contains('.card', 'X').find('button')`

### ✏️ Your turn

1. Add *Sauce Labs Onesie* **and** *Sauce Labs Fleece Jacket* by name and check that the badge shows `2`.
2. On `/tables`, find **Frank**'s row in `#table1` and check that his email is `fbach@yahoo.com`. (Hint: `cy.contains('#table1 tbody tr', 'Frank').within(...)`. Email is the 3rd column, `eq(2)`.)
3. On `https://the-internet.herokuapp.com/dynamic_loading/2`, click **Start** and check that `#finish` shows `Hello World!`. It takes about 5 seconds, so use `{ timeout: 10000 }`.

---

# Topic 5: Element Interaction

### Definition

**Element interaction** means simulating what a user does (clicking, typing, choosing options, uploading files) with **action commands** chained onto a query. Before acting, Cypress waits until the element is **actionable**: visible, enabled, not covered and not animating.

### Key ideas

| Action | Example |
|---|---|
| Click | `.click()` · `.dblclick()` · `.rightclick()` |
| Type | `.type('text')` (**adds** to the text) · `.clear()` · `.type('{enter}')` |
| Dropdown (`<select>`) | `.select('Visible text')` or `.select('value')` |
| Checkbox / radio | `.check()` · `.uncheck()` |
| File | `.selectFile(...)` |
| Hide sensitive text in the log | `.type('secret', { log: false })` |

### Worked example: sort products, then check out

**Step 1: Create `cypress/e2e/interact.cy.js` and log in by pressing Enter**

```js
describe('Interaction', () => {
  beforeEach(() => {
    cy.visit('/');
    cy.get('[data-test=username]').type('standard_user');
    cy.get('[data-test=password]').type('secret_sauce{enter}', { log: false }); // Enter submits
  });
```

**Step 2: Choose an option from the sort dropdown**

```js
  it('sorts by price, low to high', () => {
    cy.get('[data-test=product-sort-container]').select('Price (low to high)');
    cy.get('.inventory_item_price').first().should('have.text', '$7.99');
  });
```

**Step 3: Click to add a product and open the cart**

```js
  it('checks out one product', () => {
    cy.get('[data-test=add-to-cart-sauce-labs-backpack]').click();
    cy.get('.shopping_cart_link').click();
    cy.get('[data-test=checkout]').click();
```

**Step 4: Type into the form fields**

```js
    cy.get('[data-test=firstName]').type('Jasdhir');
    cy.get('[data-test=lastName]').type('Singh');
    cy.get('[data-test=postalCode]').type('10001');
    cy.get('[data-test=continue]').click();
```

**Step 5: Finish and check the confirmation**

```js
    cy.get('[data-test=finish]').click();
    cy.get('.complete-header').should('have.text', 'Thank you for your order!');
  });
});
```

**Step 6: See `.type()` add to existing text.** Add this test and see why it fails:

```js
it('shows that type() appends', () => {
  cy.visit('/');
  cy.get('[data-test=username]').type('standard').type('_user');
  cy.get('[data-test=username]').should('have.value', 'standard_user');   // passes: text was added
  cy.get('[data-test=username]').type('abc');
  cy.get('[data-test=username]').should('have.value', 'abc');             // fails! value is 'standard_userabc'
});
```

Fix it with `.clear().type('abc')`.

### ✅ Checkpoint

- The sort test shows `$7.99` first.
- The checkout test ends on **Thank you for your order!**
- You know why the last test failed, and how to fix it.

### Worked example: upload a file without a file on disk

```js
it('uploads a file', () => {
  cy.visit('https://the-internet.herokuapp.com/upload');
  cy.get('#file-upload').selectFile({
    contents: Cypress.Buffer.from('Hello from Cypress'),   // file content created in memory
    fileName: 'hello.txt',
  });
  cy.get('#file-submit').click();
  cy.get('#uploaded-files').should('contain', 'hello.txt');
});
```

### 💡 Playwright tip

`fill('x')` replaces text, but Cypress `.type('x')` adds to it. Use `.clear().type('x')` when you need to replace.

### ✏️ Your turn

1. Sort by **Name (Z to A)** and check that the first product is *Test.allTheThings() T-Shirt (Red)*.
2. In the checkout test, submit the information form by typing `{enter}` in the postal code field instead of clicking **Continue**.
3. On `https://the-internet.herokuapp.com/checkboxes`, check the first box, uncheck the second, and assert both states.
4. On `https://the-internet.herokuapp.com/dropdown`, select **Option 2** and check that `#dropdown` has the value `2`.

---

# Topic 6: Assertions and Annotations

### Definition

An **assertion** checks that the application is in the expected state. **Implicit** assertions (`.should()`, `.and()`) **retry**. **Explicit** assertions (`expect`) run **once**, usually inside `.then()`.
An **annotation** is behavior attached to a test: focus it, skip it, retry it, give it more time, or limit it to a browser.

### Key ideas

| Check | Code |
|---|---|
| Visible / exists / removed | `be.visible` · `exist` · `not.exist` |
| Text | `have.text` (exact) · `contain` (partial) |
| Value / attribute | `have.value` · `have.attr` |
| Count | `have.length` |
| State | `be.enabled` · `be.disabled` · `be.checked` |
| URL | `cy.url().should('include', '/x')` |

| Annotation | Code |
|---|---|
| Run only this test | `it.only(...)` |
| Skip | `it.skip(...)` |
| Skip based on a condition | `this.skip()` inside `function () {}` |
| Retry | `it('x', { retries: 2 }, () => {...})` |
| More time | `it('x', { defaultCommandTimeout: 15000 }, () => {...})` |
| One browser only | `it('x', { browser: 'chrome' }, () => {...})` |

### Worked example: check that sorting really works

**Step 1: Create `cypress/e2e/assert.cy.js` and log in**

```js
describe('Assertions', () => {
  beforeEach(() => {
    cy.visit('/');
    cy.get('[data-test=username]').type('standard_user');
    cy.get('[data-test=password]').type('secret_sauce{enter}');
  });
```

**Step 2: Chain implicit assertions with `.should()` and `.and()`**

```js
  it('checks the page state', () => {
    cy.url().should('include', '/inventory.html');
    cy.get('.title').should('be.visible').and('have.text', 'Products');
    cy.get('.inventory_item').should('have.length', 6);
    cy.get('.shopping_cart_badge').should('not.exist');   // not in the DOM yet
  });
```

**Step 3: Sort, then check only the first price.** Is that enough to prove the sort worked?

```js
  it('sorts prices low to high', () => {
    cy.get('[data-test=product-sort-container]').select('lohi');
    cy.get('.inventory_item_price').first().should('have.text', '$7.99');
```

**Step 4: Check every price with a `.should()` callback.** It retries until it passes.

```js
    cy.get('.inventory_item_price').should(($prices) => {
      const values = [...$prices].map((el) => Number(el.innerText.replace('$', '')));
      const sorted = [...values].sort((a, b) => a - b);
      expect(values, 'prices ascending').to.deep.equal(sorted);
    });
  });
```

**Step 5: Add annotations to control how tests run**

```js
  it('retries and has more time', { retries: 2, defaultCommandTimeout: 10000 }, () => {
    cy.get('.inventory_item').should('have.length', 6);
  });

  it('is skipped on Firefox', function () {          // function() so `this` works
    if (Cypress.isBrowser('firefox')) this.skip();
    cy.get('.title').should('have.text', 'Products');
  });

  it('TODO: check the About link');                  // no body = pending
});
```

**Step 6: Try `.only`.** Change one `it(` to `it.only(`, run the spec, then change it back.

### ✅ Checkpoint

- The Command Log shows **green assertions**, and the custom message `prices ascending` appears in it.
- In Firefox, the conditional test shows as **skipped**, and the TODO test shows as **pending**.

### 💡 Playwright tip

`await expect(loc).toHaveText('x')` → `cy.get(sel).should('have.text', 'x')`, with no `await`, and it retries the same way.

### ⚠️ Common errors

| Mistake | Fix |
|---|---|
| `expect` inside `.then()` fails while the page is still loading | Use `.should()`, which retries |
| `should('not.be.visible')` on an element that's been removed | Use `should('not.exist')` |
| `this.skip()` says `this` is undefined | Use `function () {}`, not `() => {}` |
| `.only` left in the code | Remove it before you commit |

### ✏️ Your turn

1. Sort by **Price (high to low)** and use a `.should()` callback to check the prices are in **descending** order.
2. Add the Backpack ($29.99) and the Onesie ($7.99), go to checkout step two, and check that the item total is `$37.98`: `cy.get('.summary_subtotal_label').should('contain', '37.98')`.
3. Write a test that runs only in **Chrome** and has `retries: 1`.

---

## End of Class Checklist

Tick each item you can do without looking at the notes:

- [ ] Create a Cypress project, set `baseUrl`, and run a spec in `open` and `run` mode
- [ ] Run a spec in a specific browser
- [ ] Explain why `cy` commands don't use `await`
- [ ] Write a test with `describe`, `it` and `beforeEach` using Arrange → Act → Assert
- [ ] Locate an element with `cy.get`, `cy.contains` and `.find`
- [ ] Find an element inside a card or table row by its text
- [ ] Click, type, select from a dropdown and upload a file
- [ ] Explain why `.type()` needs `.clear()` to replace text
- [ ] Write implicit (`.should`) and explicit (`expect`) assertions
- [ ] Explain the difference between `not.exist` and `not.be.visible`
- [ ] Skip, focus, retry and time-limit a test with annotations
- [ ] Cache a login with `cy.session()`


