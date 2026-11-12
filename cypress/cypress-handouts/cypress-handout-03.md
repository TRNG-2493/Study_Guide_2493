# Cypress Class Handout 03

> **For:** students who completed parts 01 and 02 and already know Playwright.
> **Covers:** 13. Recording User Actions · 14. Editing Generated Code · 15. Visual Testing
>
> **How to use this handout:** each topic has a **definition**, a few **key ideas**, a **worked example** we build together **step by step**, a **checkpoint** that shows what you should see, and a **Your turn** exercise.

---

## Before Class

- Use the **`cypress-class`** project from parts 01 and 02.
- You need the custom commands `cy.login()`, `cy.addToCart()` and `cy.fillCheckout()` and the fixtures `users.json` and `checkout.json` from part 02 (Topic 7).
- Install **Google Chrome** and the **Cypress Chrome Recorder** extension (Chrome Web Store).
- Commit your work to git before Topic 13, so you can see exactly what Studio adds with `git diff`.

**Practice app login (saucedemo):** `standard_user` · `problem_user`, both with password `secret_sauce`

> ⚠️ Recording tools and visual-testing plugins change between versions. If a button name or setting differs from this handout, your trainer will show the equivalent in your version.

---

# Topic 13: Recording User Actions

### Definition

**Recording user actions** means **using the app by hand while a tool writes the test code for you**. **Cypress Studio** records inside the Cypress runner and writes `cy.get(...).click()`, `.type()`, `.check()`, `.select()` and assertions **straight into your spec**. The **Chrome DevTools Recorder** records in normal Chrome and can export a Cypress test. A recording is a **first draft**, not a finished test.

### Key ideas

1. Studio is the Cypress version of **Playwright codegen**.
2. Turn it on with `experimentalStudio: true` (in most versions).
3. **Add New Test** (on a `describe`) or **Add Commands to Test** (on an `it`).
4. **Right-click → Add Assertion** to add checks while recording.
5. Studio records clicks, typing, checks and selects. It **doesn't** record hover, drag, scroll or special keys.

### Worked example A: record a new test with Studio

**Step 1: Turn on Studio in `cypress.config.js`**

```js
e2e: {
  baseUrl: 'https://www.saucedemo.com',
  experimentalStudio: true,
  // ...setupNodeEvents
}
```

Restart `npx cypress open`.

**Step 2: Create a starting spec, `cypress/e2e/studio/login.cy.js`**

```js
describe('Login (recorded)', () => {
  beforeEach(() => {
    cy.visit('/');
  });

  it('starting point', () => {
    cy.get('[data-test=login-button]').should('be.visible');
  });
});
```

Run it once so it passes.

**Step 3: Start recording.** Hover over the **describe** title in the Command Log → **Add New Test**.

**Step 4: Use the app by hand**

1. Click **Username**, then type `standard_user`.
2. Click **Password**, then type `secret_sauce`.
3. Click **Login**.

**Step 5: Add an assertion.** **Right-click** the **Products** title → **Add Assertion** → **have text** → `Products`.

**Step 6: Save.** Click **Save Commands** and name the test `logs in as standard_user`.

**Step 7: Look at the file.** Open `login.cy.js`. You should see a new test similar to:

```js
  /* ==== Test Created with Cypress Studio ==== */
  it('logs in as standard_user', function() {
    /* ==== Generated with Cypress Studio ==== */
    cy.get('[data-test="username"]').clear();
    cy.get('[data-test="username"]').type('standard_user');
    cy.get('[data-test="password"]').clear();
    cy.get('[data-test="password"]').type('secret_sauce');
    cy.get('[data-test="login-button"]').click();
    cy.get('[data-test="title"]').should('have.text', 'Products');
    /* ==== End Cypress Studio ==== */
  });
```

### Worked example B: add steps to the recorded test

**Step 1:** Hover over **`logs in as standard_user`** → **Add Commands to Test**.

**Step 2:** Studio replays the test. Then, by hand:

1. Click **Add to cart** on *Sauce Labs Backpack*.
2. Right-click the **cart badge** → **Add Assertion** → **have text** → `1`.

**Step 3:** **Save Commands**, then run `git diff` to see exactly what Studio added.

### Worked example C: record with Chrome DevTools Recorder

**Step 1:** Open `https://www.saucedemo.com` in **Chrome** → DevTools (F12) → **Recorder** (under **More tools** if you can't see it).

**Step 2:** **Create a new recording** → set **Selector attribute** to `data-test` → **Start recording**.

**Step 3:** Log in, add *Sauce Labs Bike Light*, and open the cart. Then **End recording**.

**Step 4:** **Export** → **Export as a Cypress Test** → save it as `cypress/e2e/recorded/bike-light.cy.js`.

**Step 5:** Run the exported test in Cypress.

### ✅ Checkpoint

- `login.cy.js` contains a Studio-generated test that passes.
- `git diff` shows the Studio comment markers and the generated commands.
- The Chrome Recorder export runs in Cypress.

### 💡 Playwright tip

`npx playwright codegen <url>` → Cypress Studio (**Add New Test** / **Add Commands to Test**), or Chrome Recorder → **Export as a Cypress Test**.

### ✏️ Your turn

1. Compare the Studio output and the Chrome Recorder output. List three differences (extra commands, selectors, assertions).
2. Use **Add Commands to Test** to continue your Studio test through checkout to **Thank you for your order!**, with at least two assertions.
3. Try to record a **hover** or a **scroll**. What happens?

---

# Topic 14: Editing Generated Code

### Definition

**Editing generated code** turns a **recorded draft** into a **maintainable test**: remove noise, replace fragile selectors, add assertions that prove the behavior, move data into fixtures, move repeated steps into custom commands, and give the test a clear name and structure. A recording captures **what you did**. Editing captures **what the test should prove**.

### Key ideas

| Recorded code problem | Edit |
|---|---|
| `.clear()` / `.click()` before every `.type()` | Delete them (keep `.clear()` only if the field has a default value) |
| `cy.viewport()` / full URLs in the test | Use config and `cy.visit('/')` |
| `:nth-child(3) > .btn` | `[data-test=...]` or `cy.contains('.card', 'Name').find('button')` |
| One assertion at the end | Assert after each important step |
| Hard-coded users and values | Fixtures |
| Login repeated in every test | `cy.login()` + `cy.session()` in `beforeEach` |
| `it('tests checkout')` | `it('completes an order for two products')` |

### Worked example: clean up a recorded checkout

**Step 1: Create `cypress/e2e/recorded/checkout-recorded.cy.js` with this "recorded" code**

```js
describe('saucedemo', () => {
  it('tests checkout', function() {
    /* ==== Generated with Cypress Studio ==== */
    cy.viewport(1280, 720);
    cy.visit('https://www.saucedemo.com/');
    cy.get('[data-test="username"]').click();
    cy.get('[data-test="username"]').clear();
    cy.get('[data-test="username"]').type('standard_user');
    cy.get('[data-test="password"]').click();
    cy.get('[data-test="password"]').clear();
    cy.get('[data-test="password"]').type('secret_sauce');
    cy.get('[data-test="login-button"]').click();
    cy.get(':nth-child(1) > .pricebar > .btn').click();
    cy.get(':nth-child(3) > .pricebar > .btn').click();
    cy.get('.shopping_cart_link').click();
    cy.get('[data-test="checkout"]').click();
    cy.get('[data-test="firstName"]').clear();
    cy.get('[data-test="firstName"]').type('Jasdhir');
    cy.get('[data-test="lastName"]').clear();
    cy.get('[data-test="lastName"]').type('Singh');
    cy.get('[data-test="postalCode"]').clear();
    cy.get('[data-test="postalCode"]').type('10001');
    cy.get('[data-test="continue"]').click();
    cy.get('[data-test="finish"]').click();
    cy.get('.complete-header').should('have.text', 'Thank you for your order!');
    /* ==== End Cypress Studio ==== */
  });
});
```

Run it. ✅ It passes. Now answer: **which products did it buy?** You can't tell from the code.

**Step 2: Remove noise.** Delete `cy.viewport`, the Studio markers, and every `.click()` / `.clear()` before `.type()`. Change the visit to `cy.visit('/')`.

```js
cy.visit('/');
cy.get('[data-test="username"]').type('standard_user');
cy.get('[data-test="password"]').type('secret_sauce');
cy.get('[data-test="login-button"]').click();
```

Run it again. ✅ Still passes.

**Step 3: Replace the position-based selectors.** Cards 1 and 3 are the Backpack and the Bolt T-Shirt:

```js
cy.contains('.inventory_item', 'Sauce Labs Backpack').find('button').click();
cy.contains('.inventory_item', 'Sauce Labs Bolt T-Shirt').find('button').click();
```

**Step 4: Add assertions after each important step**

```js
cy.url().should('include', '/inventory.html');                 // after login
cy.get('.shopping_cart_badge').should('have.text', '2');        // after adding
cy.get('.cart_item').should('have.length', 2);                  // in the cart
cy.get('.summary_subtotal_label').should('contain', '45.98');   // 29.99 + 15.99
```

**Step 5: Move the data into a fixture.** Create `cypress/fixtures/order.json`:

```json
{
  "products": ["Sauce Labs Backpack", "Sauce Labs Bolt T-Shirt"],
  "itemTotal": "45.98"
}
```

**Step 6: Rewrite it with custom commands, a clear name and a tag.** Create `cypress/e2e/checkout/checkout-two-products.cy.js`:

```js
import order from '../../fixtures/order.json';

describe('Checkout', { tags: '@checkout' }, () => {
  beforeEach(() => {
    cy.login();
  });

  it('completes an order for two products', { tags: '@smoke' }, () => {
    cy.addToCart(...order.products);
    cy.get('.shopping_cart_badge').should('have.text', String(order.products.length));

    cy.get('.shopping_cart_link').click();
    cy.get('.cart_item').should('have.length', order.products.length);

    cy.get('[data-test=checkout]').click();
    cy.fillCheckout();

    cy.url().should('include', '/checkout-step-two.html');
    cy.get('.summary_subtotal_label').should('contain', order.itemTotal);

    cy.get('[data-test=finish]').click();
    cy.get('.complete-header').should('have.text', 'Thank you for your order!');
  });
});
```

**Step 7: Check it's stable.** Run it five times:

```bash
npx cypress run --env grep="completes an order for two products",burn=5
```

### ✅ Checkpoint

- The edited test passes **5 times out of 5**.
- Reading the test tells you **which products**, **what total**, and **what success looks like**.
- It has no position-based selectors, no hard-coded user, and no Studio markers.

### Editing checklist

| # | Check |
|---|---|
| 1 | Noise removed: extra `.clear()`/`.click()`, `cy.viewport`, markers |
| 2 | `cy.visit('/')` with `baseUrl` |
| 3 | Stable selectors: `[data-test]`, `cy.contains()`, `#id` |
| 4 | Assertions after each important step |
| 5 | Shared setup: `beforeEach`, `cy.login()`, `cy.session()` |
| 6 | Data in fixtures or env vars, with no secrets in specs |
| 7 | One behavior per test |
| 8 | A clear test name |
| 9 | The right folder and tags |
| 10 | Passes with `burn=5` |

### 💡 Playwright tip

It's the same job as cleaning up codegen output: replace `nth-child` locators with test IDs or text, move login into `beforeEach`, and add assertions.

### ✏️ Your turn

1. Apply the checklist to the Studio test you recorded in Topic 13.
2. Record a checkout with an **empty last name**, then turn it into a **data-driven** spec that checks all three required fields (First Name, Last Name, Postal Code).
3. Record selecting **Price (low to high)**, then add a `.should()` callback that checks every price is in ascending order.

---

# Topic 15: Visual Testing

### Definition

**Visual testing** (visual regression testing) checks **what the page looks like**. It takes a screenshot, compares it with an approved **baseline** image, and fails when the difference is bigger than a **threshold**. It catches layout, CSS and image bugs that DOM assertions miss. **Cypress has no built-in visual comparison**, so you add a **plugin** or a **cloud service** (Percy, Applitools).

### Key ideas

```
First run:   screenshot ──────────────────────────────► saved as BASELINE
Later runs:  screenshot ──► compare with BASELINE ──► diff ≤ threshold → ✅ pass
                                                   └► diff > threshold → ❌ fail + diff image
Intended change?  → review the diff → update the baseline
```

1. Visual tests **add to** functional tests. They don't replace them.
2. Keep the environment **identical** (browser, OS, viewport) between the baseline and later runs.
3. Wait for the page to **settle**, and `blackout` dynamic content.
4. **Review** every new or updated baseline before committing it.

### Worked example A: see what functional tests miss

**Step 1: Create `cypress/e2e/visual/image-checks.cy.js`**

```js
['standard_user', 'problem_user'].forEach((user) => {
  it(`${user}: products page looks right?`, () => {
    cy.visit('/');
    cy.get('[data-test=username]').type(user);
    cy.get('[data-test=password]').type('secret_sauce{enter}');

    cy.get('.inventory_item').should('have.length', 6);
    cy.get('.inventory_item img').should('be.visible');
  });
});
```

**Step 2: Run it.** Both tests **pass**. Now log in as `problem_user` by hand and look at the images.

**Step 3: Add a check for unique images** to the end of the test:

```js
    cy.get('.inventory_item img').should(($imgs) => {
      const sources = [...$imgs].map((img) => img.getAttribute('src'));
      expect(new Set(sources).size, 'unique image sources').to.eq(sources.length);
    });
```

Run again. ❌ `problem_user` now fails. But you can't write a check like this for every possible visual bug.

### Worked example B: screenshot comparison with a plugin

**Step 1: Install**

```bash
npm i -D @simonsmith/cypress-image-snapshot
```

**Step 2: Register it in `cypress.config.js`** (keep your other `setupNodeEvents` code)

```js
const { addMatchImageSnapshotPlugin } = require('@simonsmith/cypress-image-snapshot/plugin');

// inside e2e: { ... }
viewportWidth: 1280,
viewportHeight: 720,
setupNodeEvents(on, config) {
  addMatchImageSnapshotPlugin(on);
  return config;
},
```

**Step 3: Register the command in `cypress/support/e2e.js`**

```js
import { addMatchImageSnapshotCommand } from '@simonsmith/cypress-image-snapshot/command';

addMatchImageSnapshotCommand({
  failureThreshold: 0.03,
  failureThresholdType: 'percent',
  capture: 'viewport',
});
```

Restart Cypress. (Check the plugin's README if your version's setup differs.)

**Step 4: Create `cypress/e2e/visual/visual.cy.js`**

```js
describe('Visual regression', { tags: '@visual' }, () => {
  it('login page', () => {
    cy.visit('/');
    cy.matchImageSnapshot('login-page');
  });

  it('inventory (standard_user)', () => {
    cy.visit('/');
    cy.get('[data-test=username]').type('standard_user');
    cy.get('[data-test=password]').type('secret_sauce{enter}');
    cy.get('.inventory_item img').should('be.visible');
    cy.matchImageSnapshot('inventory');
  });
});
```

**Step 5: First run creates the baselines**

```bash
npx cypress run --spec cypress/e2e/visual/visual.cy.js --browser chrome
```

Open `cypress/snapshots/visual.cy.js/` and **check** that `login-page.snap.png` and `inventory.snap.png` look right.

**Step 6: Catch the visual bug.** Add this test, which compares `problem_user` with the **same** baseline:

```js
  it('inventory (problem_user): compared with the standard baseline', () => {
    cy.visit('/');
    cy.get('[data-test=username]').type('problem_user');
    cy.get('[data-test=password]').type('secret_sauce{enter}');
    cy.get('.inventory_item img').should('be.visible');
    cy.matchImageSnapshot('inventory');
  });
```

Run again. ❌ It fails. Open `cypress/snapshots/visual.cy.js/__diff_output__/inventory.diff.png`.

**Step 7: Hide dynamic areas.** Snapshot without prices:

```js
cy.matchImageSnapshot('inventory-no-prices', { blackout: ['.inventory_item_price'] });
```

### ✅ Checkpoint

- Baseline images exist in `cypress/snapshots/`.
- The `problem_user` test fails, and the diff image **highlights the wrong product images**.
- You can explain why functional checks alone missed it.

### Cloud services (overview)

| Service | Command in the test | Run |
|---|---|---|
| **Percy** | `cy.percySnapshot('Name', { widths: [375, 1280] })` | `npx percy exec -- cypress run` (needs `PERCY_TOKEN`) |
| **Applitools** | `cy.eyesOpen(...)` → `cy.eyesCheckWindow('Name')` → `cy.eyesClose()` | `npx cypress run` (needs an API key) |

Both store baselines in a **web dashboard** where you approve or reject changes.

### 💡 Playwright tip

`await expect(page).toHaveScreenshot('inventory.png')` → `cy.matchImageSnapshot('inventory')` (plugin). `--update-snapshots` → `--env updateSnapshots=true`.

### ✏️ Your turn

1. Snapshot the **login error box** only: click **Login** with empty fields, then `cy.get('.login-box').matchImageSnapshot('login-error')`.
2. Snapshot the inventory page at **375px** and **1280px** wide, with different snapshot names.
3. Make a snapshot fail on purpose with `cy.get('.title').invoke('css', 'color', 'red')`, open the diff image, then remove the change so it passes again.
4. Run only visual tests: `npx cypress run --env grepTags=@visual`.

---

## End of Class Checklist

Tick each item you can do without looking at the notes:

- [ ] Turn on Cypress Studio and record a new test
- [ ] Add steps and assertions to an existing test with Studio
- [ ] Record a flow with the Chrome DevTools Recorder and export it as a Cypress test
- [ ] List what Studio can and can't record
- [ ] Remove noise from generated code (extra `.clear()`/`.click()`, `cy.viewport`, markers)
- [ ] Replace position-based selectors with `[data-test]` or `cy.contains()`
- [ ] Add assertions after each important step
- [ ] Move data into fixtures and repeated steps into custom commands
- [ ] Split a long recording into focused, well-named tests
- [ ] Explain what visual testing catches that functional tests miss
- [ ] Create baselines, read a diff image, and update baselines on purpose
- [ ] Make visual tests stable (same environment, fixed viewport, blackout, settled page)

