# Cypress Class Handout 02

> **For:** students who completed part 01 and already know Playwright.
> **Covers:** 7. Fixtures & Custom Fixtures · 8. Test Selection · 9. Debugging Actions · 10. Time-Travel Debugging · 11. Logging · 12. Screenshots & Video
>
> **How to use this handout:** each topic has a **definition**, a few **key ideas**, a **worked example** we build together **step by step**, a **checkpoint** that shows what you should see, and a **Your turn** exercise.


---

## Before Class

- Use the **`cypress-class`** project from part 01.
- `cypress.config.js` should have `baseUrl: 'https://www.saucedemo.com'`.
- Open the test browser's **DevTools** (F12) during topics 9 and 10.
- Remember: after changing `cypress.config.js` (including `setupNodeEvents`), **restart Cypress**.

**Practice app login (saucedemo):** `standard_user` · `locked_out_user` · `problem_user`, all with password `secret_sauce`

---

# Topic 7: Fixtures and Custom Fixtures

### Definition

A **fixture** in Cypress is a **static test data file** (usually JSON) in `cypress/fixtures/`.
**"Custom fixtures"** in the Playwright sense (reusable setup injected into tests) don't exist as a feature. You build them with **custom commands**, **hooks**, **`cy.session()`** and **`cy.task()`**.

### Key ideas

1. ⚠️ In **Playwright and pytest**, a fixture is *setup code*. In **Cypress**, a fixture is a *data file*.
2. Load data with `import` (synchronous) or `cy.fixture()` (queued).
3. To generate **one test per data row**, use `import`, because `cy.fixture()` runs too late.
4. Reusable setup goes in `cypress/support/commands.js` as **custom commands**.

### Worked example A: log in with data from a fixture

**Step 1: Create `cypress/fixtures/users.json`**

```json
{
  "standard": { "username": "standard_user", "password": "secret_sauce" },
  "locked": { "username": "locked_out_user", "password": "secret_sauce" }
}
```

**Step 2: Create `cypress/e2e/fixture-login.cy.js` and import the file.** The path is relative to the spec file.

```js
import users from '../fixtures/users.json';
```

**Step 3: Use the data in a test**

```js
describe('Login with fixture data', () => {
  it('logs in as the standard user', () => {
    cy.visit('/');
    cy.get('[data-test=username]').type(users.standard.username);
    cy.get('[data-test=password]').type(users.standard.password, { log: false });
    cy.get('[data-test=login-button]').click();
    cy.url().should('include', '/inventory.html');
  });
});
```

**Step 4: Load the same file with `cy.fixture()` instead.** Add this test:

```js
  it('shows an error for the locked user', () => {
    cy.fixture('users').then((data) => {
      cy.visit('/');
      cy.get('[data-test=username]').type(data.locked.username);
      cy.get('[data-test=password]').type(data.locked.password, { log: false });
      cy.get('[data-test=login-button]').click();
    });
    cy.get('[data-test=error]').should('contain', 'locked out');
  });
```

### Worked example B: one test per data row

**Step 1: Create `cypress/fixtures/login-cases.json`**

```json
[
  { "title": "valid user", "username": "standard_user", "password": "secret_sauce", "expectUrl": "/inventory.html" },
  { "title": "locked user", "username": "locked_out_user", "password": "secret_sauce", "expectError": "locked out" },
  { "title": "wrong password", "username": "standard_user", "password": "nope", "expectError": "do not match" }
]
```

**Step 2: Create `cypress/e2e/data-driven.cy.js` and loop over the rows to create tests**

```js
import cases from '../fixtures/login-cases.json';

describe('Login (data-driven)', () => {
  cases.forEach((c) => {
    it(`login: ${c.title}`, () => {
      cy.visit('/');
      cy.get('[data-test=username]').type(c.username);
      cy.get('[data-test=password]').type(c.password, { log: false });
      cy.get('[data-test=login-button]').click();

      if (c.expectUrl) {
        cy.url().should('include', c.expectUrl);
      } else {
        cy.get('[data-test=error]').should('contain', c.expectError);
      }
    });
  });
});
```

### Worked example C: a "custom fixture" with a custom command

**Step 1: Add a login command to `cypress/support/commands.js`**

```js
Cypress.Commands.add('login', (userKey = 'standard') => {
  cy.fixture('users').then((users) => {
    const user = users[userKey];
    cy.session(user.username, () => {
      cy.visit('/');
      cy.get('[data-test=username]').type(user.username);
      cy.get('[data-test=password]').type(user.password, { log: false });
      cy.get('[data-test=login-button]').click();
      cy.url().should('include', '/inventory.html');
    });
  });
  cy.visit('/inventory.html', { failOnStatusCode: false });
});
```

**Step 2: Check that `cypress/support/e2e.js` loads the commands**

```js
import './commands';
```

**Step 3: Use it like a Playwright `loggedInPage` fixture.** Create `cypress/e2e/with-login.cy.js`:

```js
describe('Inventory', () => {
  beforeEach(() => {
    cy.login();
  });

  it('shows 6 products', () => {
    cy.get('.inventory_item').should('have.length', 6);
  });
});
```

### ✅ Checkpoint

- `data-driven.cy.js` shows **three separate tests** in the runner.
- In `with-login.cy.js`, the Command Log shows a `session` entry, and the test starts on the products page.

### 💡 Playwright tip

`test.extend({ loggedInPage })` → `Cypress.Commands.add('login', ...)` + `cy.login()` in `beforeEach`

### ✏️ Your turn

1. Create `checkout.json` (`firstName`, `lastName`, `postalCode`) and use it to fill the checkout form.
2. Add a `cy.addToCart(name)` command that does `cy.contains('.inventory_item', name).find('button').click()`, and use it twice in a test.
3. Add a fourth row to `login-cases.json` for an empty password (expected error: `Password is required`). Hint: `.type('')` throws an error, so skip typing when the value is empty.

---

# Topic 8: Test Selection

### Definition

**Test selection** is choosing **which tests run**: one spec, a folder, tests whose title matches a word, or tests with a tag such as `@smoke`. Cypress selects **spec files** with `--spec`, tests **inside a file** with `.only` / `.skip`, and tests **across files by title or tag** with the official **`@cypress/grep`** plugin.

### Key ideas

| Want to run… | Use |
|---|---|
| One file | `--spec cypress/e2e/auth/login.cy.js` |
| A folder | `--spec "cypress/e2e/auth/**/*.cy.js"` (keep the quotes) |
| One test while developing | `it.only(...)` (that file only) |
| Tagged tests | `--env grepTags=@smoke` (needs `@cypress/grep`) |
| Tests by title | `--env grep="locked"` |

Grep syntax: **space** = OR · **`+`** = AND · **`-`** = NOT

### Worked example: tag tests and run a smoke suite

**Step 1: Organize specs into folders**

```
cypress/e2e/
├── auth/login.cy.js
└── inventory/sorting.cy.js
```

**Step 2: Run one folder with `--spec`**

```bash
npx cypress run --spec "cypress/e2e/auth/**/*.cy.js"
```

**Step 3: Install `@cypress/grep`**

```bash
npm i -D @cypress/grep
```

**Step 4: Register it in two places** (this is the setup for recent versions; check the plugin's README for the version you installed)

```js
// cypress/support/e2e.js
import './commands';
import { register as registerCypressGrep } from '@cypress/grep';
registerCypressGrep();
```

```js
// cypress.config.js
const { defineConfig } = require('cypress');
const { plugin: cypressGrepPlugin } = require('@cypress/grep/plugin');

module.exports = defineConfig({
  e2e: {
    baseUrl: 'https://www.saucedemo.com',
    setupNodeEvents(on, config) {
      cypressGrepPlugin(config);
      return config;
    },
  },
});
```

**Step 5: Tag tests in `cypress/e2e/auth/login.cy.js`**

```js
describe('Login', { tags: '@auth' }, () => {
  beforeEach(() => cy.visit('/'));

  it('valid user', { tags: ['@smoke', '@regression'] }, () => {
    cy.get('[data-test=username]').type('standard_user');
    cy.get('[data-test=password]').type('secret_sauce{enter}');
    cy.url().should('include', '/inventory.html');
  });

  it('locked user', { tags: '@regression' }, () => {
    cy.get('[data-test=username]').type('locked_out_user');
    cy.get('[data-test=password]').type('secret_sauce{enter}');
    cy.get('[data-test=error]').should('contain', 'locked out');
  });
});
```

**Step 6: Run by tag and by title**

```bash
npx cypress run --env grepTags=@smoke
npx cypress run --env grepTags=@regression+-@smoke    # regression but NOT smoke
npx cypress run --env grep="locked"
```

**Step 7: Make it fast and save it as an npm script**

```json
"scripts": {
  "cy:smoke": "cypress run --env grepTags=@smoke,grepFilterSpecs=true,grepOmitFiltered=true"
}
```

```bash
npm run cy:smoke
```

### ✅ Checkpoint

- `grepTags=@smoke` runs only **valid user**. The other tests are skipped or hidden.
- `grep="locked"` runs only **locked user**.

### 💡 Playwright tip

`npx playwright test --grep @smoke` → `npx cypress run --env grepTags=@smoke`

### ✏️ Your turn

1. Create `inventory/sorting.cy.js` with two sort tests. Tag one `@smoke` and one `@slow`.
2. Run every test **except** `@slow`.
3. Run your sorting test 5 times in a row: `--env grep="<test title>",burn=5`.
4. Add a `cy:regression` npm script and run it.

---

# Topic 9: Cypress Debugging Actions

### Definition

**Debugging actions** are the commands and techniques for **stopping a test, stepping through it, and inspecting values** when it doesn't behave as expected. Cypress runs inside the browser, so you combine its commands (`cy.pause()`, `.debug()`) with the browser's **DevTools**.

### Key ideas

| Tool | Does |
|---|---|
| `cy.pause()` | Pauses the runner. **Next** steps one command at a time |
| `.debug()` | Pauses DevTools, and `subject` holds the current element(s) |
| `debugger` | JS breakpoint. Works only **inside `.then()`** |
| `cy.log()` / `console.log()` | Print to the Command Log / to DevTools |
| Selector Playground | Check that a selector matches exactly one element |

### Worked example: pause, inspect and read errors

**Step 1: Create `cypress/e2e/debugging.cy.js` with a pause after login**

```js
describe('Debugging', () => {
  beforeEach(() => {
    cy.visit('/');
    cy.get('[data-test=username]').type('standard_user');
    cy.get('[data-test=password]').type('secret_sauce{enter}');
  });

  it('pauses and steps', () => {
    cy.pause();
    cy.get('[data-test=add-to-cart-sauce-labs-backpack]').click();
    cy.get('.shopping_cart_badge').should('have.text', '1');
  });
```

Run it. When it pauses, click **Next** (⏭) to run one command at a time, then **Resume** (▶).

**Step 2: Inspect elements with `.debug()`.** Open DevTools first (F12), then add:

```js
  it('inspects prices in DevTools', () => {
    cy.get('.inventory_item_price').debug();
  });
```

In the DevTools **Console**, type `subject.length`, then `subject[0].innerText`.

**Step 3: Put a breakpoint in the right place**

```js
  it('stops at a breakpoint', () => {
    cy.get('.inventory_item_name').first().then(($name) => {
      debugger;           // ✅ inside .then(), so it runs at the right time
      console.log($name.text());
    });
  });
});
```

**Step 4: Practice reading errors.** Create `cypress/e2e/read-errors.cy.js`. These tests **fail on purpose**:

```js
describe('Read the errors', () => {
  beforeEach(() => cy.visit('/'));

  it('1. wrong selector', () => {
    cy.get('[data-test=user-name]').type('standard_user');
  });

  it('2. wrong expected value', () => {
    cy.get('[data-test=login-button]').should('have.value', 'Log in');
  });
});
```

For each failure: read the **error message**, click the **red command**, and fix the test.

### ✅ Checkpoint

- You stepped through a test with **Next**.
- In DevTools, `subject.length` showed `6`.
- You fixed both failing tests: the selector is `[data-test=username]`, and the value is `Login`.

### 💡 Playwright tip

`await page.pause()` → `cy.pause()`. Playwright's "Pick locator" → the **Selector Playground** (crosshair icon).

### ✏️ Your turn

1. Move a `debugger` **outside** `.then()` and see when it fires. Explain why.
2. Use the Selector Playground to find a selector for the **cart icon**, and check how many elements it matches.
3. Break your checkout test on purpose (wrong user) and use the debugging routine to find the cause: read the error → click the red command → check earlier commands.

---

# Topic 10: Trace / Time-Travel Debugging

### Definition

**Time-travel debugging** means Cypress takes a **DOM snapshot for every command**. **Hover** over a command in the Command Log to see the page at that moment, or **click** it to pin the snapshot. It's Cypress's version of **Playwright's Trace Viewer**, but live in the runner. For CI runs, the equivalent is **Test Replay** in Cypress Cloud.

### Key ideas

1. **Hover** = preview the snapshot. **Click** = pin it (click again or press Esc to unpin).
2. Pinned actions have a **Before / After** toggle and a **red dot** where the click landed.
3. With DevTools open, clicking a command shows its **details** (yielded value, elements, expected and actual).
4. Snapshots exist only in **`cypress open`**, not in headless runs.

### Worked example: travel through a checkout

**Step 1: Create `cypress/e2e/time-travel.cy.js`**

```js
it('checkout (explore me)', () => {
  cy.visit('/');
  cy.get('[data-test=username]').type('standard_user');
  cy.get('[data-test=password]').type('secret_sauce');
  cy.get('[data-test=login-button]').click();
  cy.get('[data-test=add-to-cart-sauce-labs-backpack]').click();
  cy.get('.shopping_cart_badge').should('have.text', '1');
  cy.get('.shopping_cart_link').click();
  cy.get('[data-test=checkout]').click();
  cy.get('[data-test=firstName]').type('Jasdhir');
  cy.get('[data-test=lastName]').type('Singh');
  cy.get('[data-test=postalCode]').type('10001');
  cy.get('[data-test=continue]').click();
  cy.get('[data-test=finish]').click();
  cy.get('.complete-header').should('have.text', 'Thank you for your order!');
});
```

**Step 2: Run it in `cypress open` with DevTools open, then explore**

| # | Do this | You should see |
|---|---|---|
| 1 | Hover over `type standard_user` | The login page with the username filled in |
| 2 | Hover over the login `click` | A **red dot** on the Login button |
| 3 | **Click** the add-to-cart `click` | The snapshot is pinned, with **Before / After** at the bottom |
| 4 | Switch Before ↔ After | The button changes from **Add to cart** to **Remove** |
| 5 | Look at the DevTools Console | `Command: click`, `Applied To`, `Elements: 1` |
| 6 | Click the badge assertion | `Expected` and `Actual` values in the console |

### Worked example: find the real cause of a failure

**Step 1: Create `cypress/e2e/time-travel-failure.cy.js`.** This test **fails on purpose**:

```js
it('fails: the add-to-cart button is never found', () => {
  cy.visit('/');
  cy.get('[data-test=username]').type('locked_out_user');
  cy.get('[data-test=password]').type('secret_sauce');
  cy.get('[data-test=login-button]').click();
  cy.get('[data-test=add-to-cart-sauce-labs-backpack]').click();
});
```

**Step 2: Click the failed command.** What page does the snapshot show?

**Step 3: Click the commands before it,** one by one, until you find the first step where the page isn't what you expected.

### ✅ Checkpoint

- You can explain the failure in one sentence: *"The locked-out user can't log in, so the products page (and its button) never appears."*
- You understand that the **failing** command is often not the **wrong** command.

### 💡 Playwright tip

Trace Viewer's action list and DOM snapshots → the Command Log, with hover and click.

### ✏️ Your turn

1. Pin the **Continue** click on the checkout page and compare Before and After.
2. In `time-travel.cy.js`, add `{ log: false }` to one `cy.get()` and see what disappears from the Command Log.
3. Change the expected badge text to `'2'`, run it, and use only time travel to explain the failure.

---

# Topic 11: Logging

### Definition

**Logging** is recording what a test did and found, so you can understand a run afterwards, especially in CI. Logs go to three places: the **Command Log** (`cy.log()`), the **browser console** (`console.log()`), and the **terminal** (`cy.task()` running in Node).

### Key ideas

| Want output in… | Use |
|---|---|
| Command Log (runner) | `cy.log('**Step 1:** ...')` (supports **bold**) |
| Browser DevTools | `console.log(...)` inside `.then()` |
| Terminal / CI logs | `cy.task('log', message)` |

⚠️ `cy.log()` and `console.log()` **don't** print to the terminal.

### Worked example: log steps, then print to the terminal

**Step 1: Create `cypress/e2e/logging.cy.js` and log readable steps**

```js
it('logs its steps and values', () => {
  cy.log('**Step 1:** open the login page');
  cy.visit('/');

  cy.log('**Step 2:** log in');
  cy.get('[data-test=username]').type('standard_user');
  cy.get('[data-test=password]').type('secret_sauce{enter}', { log: false });

  cy.log('**Step 3:** read the first product');
  cy.get('.inventory_item_name').first().invoke('text').then((name) => {
    cy.log(`First product: ${name}`);
  });
});
```

**Step 2: Register terminal tasks in `cypress.config.js`** (keep the grep plugin line if you added it in Topic 8)

```js
setupNodeEvents(on, config) {
  on('task', {
    log(message) {
      console.log(`    [log] ${message}`);
      return null;               // a task must return a value or null
    },
    table(rows) {
      console.table(rows);
      return null;
    },
  });
  return config;
},
```

Restart Cypress.

**Step 3: Send data to the terminal.** Add to the end of the test:

```js
  cy.get('.inventory_item').then(($items) => {
    const rows = [...$items].map((item) => ({
      name: item.querySelector('.inventory_item_name').innerText,
      price: item.querySelector('.inventory_item_price').innerText,
    }));
    cy.task('table', rows);
  });
```

**Step 4: Run it headless and look at the terminal**

```bash
npx cypress run --spec cypress/e2e/logging.cy.js
```

### ✅ Checkpoint

- In `cypress open`, the Command Log shows **bold** step labels and the first product's name.
- In `cypress run`, the terminal prints a **table** of six products and prices.

### 💡 Playwright tip

In Playwright, `console.log` in a test prints to the terminal. In Cypress it goes to the **browser**, so use `cy.task('log')` for the terminal.

### ✏️ Your turn

1. Add `cy.log('**Step N:** ...')` lines to your checkout test so it reads like a manual test case.
2. Print the **item total** from checkout step two to the terminal with `cy.task('log', ...)`.
3. Catch app errors: in `cy.visit('/', { onBeforeLoad(win) { cy.spy(win.console, 'error').as('err'); } })`, then at the end assert `cy.get('@err').should('not.have.been.called')`.

---

# Topic 12: Screenshots and Video

### Definition

**Screenshots** and **videos** are visual evidence of a run. Cypress takes a screenshot **automatically when a test fails** in `cypress run`, takes screenshots **on demand** with `cy.screenshot()`, and can record a **video of each spec file** (off by default).

### Key ideas

| Feature | Default | Mode |
|---|---|---|
| Failure screenshot | On (`screenshotOnRunFailure: true`) | `cypress run` only |
| `cy.screenshot('name')` | Full page | `open` and `run` |
| Video | **Off** (`video: false`) | `cypress run` only, one video per spec |

Files are saved to `cypress/screenshots/` and `cypress/videos/`.

### Worked example: capture evidence

**Step 1: Create `cypress/e2e/media.cy.js` with one test that fails on purpose**

```js
describe('Screenshots', () => {
  it('fails on purpose', () => {
    cy.visit('/');
    cy.get('[data-test=username]').type('standard_user');
    cy.get('[data-test=password]').type('wrong{enter}');
    cy.url().should('include', '/inventory.html');
  });
```

**Step 2: Add on-demand screenshots**

```js
  it('takes screenshots on demand', () => {
    cy.visit('/');
    cy.get('[data-test=username]').type('standard_user');
    cy.get('[data-test=password]').type('secret_sauce{enter}');

    cy.screenshot('inventory-full');                               // whole page
    cy.screenshot('inventory-viewport', { capture: 'viewport' });  // visible area only
    cy.contains('.inventory_item', 'Sauce Labs Backpack')
      .screenshot('backpack-card');                                // one element
    cy.screenshot('inventory-no-prices', { blackout: ['.inventory_item_price'] });
  });
});
```

**Step 3: Turn on video in `cypress.config.js`**

```js
e2e: {
  baseUrl: 'https://www.saucedemo.com',
  video: true,
  // ...setupNodeEvents
}
```

**Step 4: Run headless**

```bash
npx cypress run --spec cypress/e2e/media.cy.js --browser chrome
```

**Step 5: Open the files**

```
cypress/screenshots/media.cy.js/
├── Screenshots -- fails on purpose (failed).png   ← automatic
├── inventory-full.png
├── inventory-viewport.png
├── backpack-card.png
└── inventory-no-prices.png
cypress/videos/media.cy.js.mp4
```

**Step 6: Keep videos only for failing specs.** Add this to `setupNodeEvents` (and `const fs = require('fs');` at the top of the file):

```js
on('after:spec', (spec, results) => {
  if (results && results.video) {
    const failed = results.tests.some((t) => t.attempts.some((a) => a.state === 'failed'));
    if (!failed) fs.unlinkSync(results.video);
  }
});
```

### ✅ Checkpoint

- The automatic failure screenshot shows the **Command Log with the error** next to the app.
- The four on-demand screenshots differ: full page, viewport, one card, and prices blacked out.
- The video plays both tests.

### 💡 Playwright tip

`screenshot: 'only-on-failure'` is already the Cypress default. `video: 'retain-on-failure'` → `video: true` + the `after:spec` hook from Step 6.

### ✏️ Your turn

1. Screenshot the checkout overview page with all prices blacked out.
2. Add `cypress/screenshots/` and `cypress/videos/` to `.gitignore`.
3. Run one passing spec and one failing spec with the Step 6 hook, and check that only the failing spec's video is kept.

---

## End of Class Checklist

Tick each item you can do without looking at the notes:

- [ ] Explain the difference between a Cypress fixture and a Playwright fixture
- [ ] Load test data with `import` and with `cy.fixture()`
- [ ] Generate one test per row of a JSON file
- [ ] Write a custom command (such as `cy.login()`) and use it in `beforeEach`
- [ ] Run one spec, a folder, and a single test with `.only`
- [ ] Tag tests and run them with `@cypress/grep` (`grepTags`, `grep`, AND/OR/NOT)
- [ ] Pause a test and step through it with `cy.pause()`
- [ ] Inspect elements with `.debug()`, and use `debugger` inside `.then()`
- [ ] Use time travel (hover, pin, Before/After) to find the real cause of a failure
- [ ] Log steps with `cy.log()`, and print to the terminal with `cy.task()`
- [ ] Take full-page, viewport and element screenshots, with `blackout`
- [ ] Turn on video and keep it only for failing specs


