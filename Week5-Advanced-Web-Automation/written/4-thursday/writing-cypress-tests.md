# Writing Cypress Tests

## Learning Objectives

By the end of this lesson you will be able to:

- Structure a Cypress spec using `describe`, `context`, `it`, and hooks, and follow a clear naming convention.
- Explain the **Arrange - Act - Assert** pattern and apply it to Cypress tests.
- Chain commands correctly and understand what each command *yields* (its "subject") to the next command.
- Use `.then()`, aliases (`.as()`), `cy.wrap()`, and `.invoke()` to work with values without `async/await`.
- Explain Cypress's **retry-ability** and how it replaces most explicit waits; know when (rarely) to use `cy.wait()` and how to wait on a *network alias* instead of on time.
- Visit pages, set `baseUrl`, and handle login efficiently with `cy.session()`.
- Make API calls with `cy.request()` and control network traffic with `cy.intercept()` at a beginner level.
- Write a complete, readable E2E test (login, add to cart, verify) using the Sauce Demo practice site.
- Compare the structure of Cypress tests with the Playwright (Python) tests you wrote Monday through Wednesday.

---

## Why This Matters

Everything you will do with Cypress this week comes down to writing tests. Selectors, assertions, fixtures, and debugging all plug into the pattern you learn here. A test is more than "something that clicks buttons": it is executable documentation of how the product should behave, and it is code that a teammate must maintain at 5 p.m. on a Friday.

Tie this to the Week 5 epic: you have spent three days making Playwright tests more sophisticated and better structured (fixtures, hooks, Page Object Model). Now you are going to ask, "What does a well-structured test look like in a *different* tool?" For **Project 1: QE Foundations**, your Thursday exercise is to port three of your tests to Cypress. The skills in this lesson are exactly what you will need.

### Playwright (Python) versus Cypress at a glance

Playwright (pytest style, from earlier this week):

```python
import re
from playwright.sync_api import Page, expect

def test_login_success(page: Page):
    page.goto("https://www.saucedemo.com")
    page.get_by_placeholder("Username").fill("standard_user")
    page.get_by_placeholder("Password").fill("secret_sauce")
    page.get_by_role("button", name="Login").click()
    expect(page).to_have_url(re.compile("inventory"))
```

Cypress (JavaScript):

```js
describe('Login', () => {
  it('logs in successfully', () => {
    cy.visit('https://www.saucedemo.com');
    cy.get('[data-test="username"]').type('standard_user');
    cy.get('[data-test="password"]').type('secret_sauce');
    cy.get('[data-test="login-button"]').click();
    cy.url().should('include', 'inventory');
  });
});
```

The intent is identical. What changes is: test discovery (a `describe/it` tree versus a function name starting with `test_`), the global `cy` object versus a `page` fixture, `.should()` versus `expect(...)`, and the lack of `await` in Cypress.

---

## The Concept

### 1. Anatomy of a spec file

A **spec file** is a JavaScript (or TypeScript) file, named `something.cy.js` by default and placed inside `cypress/e2e/`. A spec contains one or more `describe` blocks, each containing `it` blocks (tests).

```js
describe('Shopping cart', () => {              // suite: group of related tests
  beforeEach(() => {                            // hook: runs before every test below
    cy.visit('/');
  });

  context('when logged in', () => {             // nested group; alias of describe
    it('adds an item', () => {                  // test case
      // ...
    });
  });
});
```

Vocabulary:

- **Spec** - one file.
- **Suite** - a `describe` (or `context`) block. `context` is simply an alias; use it to express "when ..." conditions.
- **Test** or **test case** - an `it` (or `specify`) block. It passes if no error is thrown and every command succeeds.
- **Hook** - code that Mocha runs automatically: `before`, `beforeEach`, `afterEach`, `after`. (Details in the "Assertions and annotations" lesson.)

#### 1.1 Naming conventions that pay off

- Name specs after features: `login.cy.js`, `cart.cy.js`, `checkout.cy.js`.
- `describe` names the *thing under test*: `'Login page'`, `'Shopping cart'`.
- `it` names a *behaviour*, ideally phrased as "should ..." or in plain present tense: `'shows an error when the password is wrong'`.
- Keep each test independent and able to pass when run alone.

A well-named failing test often tells you what broke without opening the code. Compare `it('test 3')` with `it('rejects an expired coupon code')`.

### 2. Arrange - Act - Assert

Good tests follow three phases:

1. **Arrange** - set up the world: visit the page, seed data, log in.
2. **Act** - perform the behaviour being tested: click, type, submit.
3. **Assert** - verify the outcome.

```js
it('adds a backpack to the cart', () => {
  // Arrange
  cy.visit('/');
  cy.get('[data-test="username"]').type('standard_user');
  cy.get('[data-test="password"]').type('secret_sauce');
  cy.get('[data-test="login-button"]').click();

  // Act
  cy.get('[data-test="add-to-cart-sauce-labs-backpack"]').click();

  // Assert
  cy.get('[data-test="shopping-cart-badge"]').should('have.text', '1');
});
```

**Line by line:**

1. `cy.visit('/')` loads the login page (using `baseUrl`).
2. The next three lines log in (we will extract these into `cy.session` or a custom command shortly).
3. `cy.get('[data-test="add-to-cart-sauce-labs-backpack"]').click()` is the **action** under test.
4. `cy.get('[data-test="shopping-cart-badge"]').should('have.text', '1')` is the **assertion**: the badge on the cart icon shows "1". If the badge doesn't appear, `.get` retries until it times out and then fails with a message like "Expected to find element...".

One test should generally verify one behaviour. Cypress tests tend to be a bit longer than unit tests because each `it` has a cost (page load, login). Cypress's own guidance is to include multiple assertions in one `it` when they describe a single flow, rather than splitting it artificially into many tiny tests that each reload the page.

### 3. Chaining and subjects

Cypress commands are *chained* to describe a sequence. The key idea: **each command yields a subject to the next**.

```js
cy.get('.inventory_item')     // yields: all matching elements
  .first()                    // yields: the first element
  .find('button')             // yields: the button inside it
  .click();                   // acts on the button; yields the same button
```

Rules to remember:

1. Some commands begin a chain and need no previous subject: `cy.visit`, `cy.get`, `cy.contains`, `cy.url`, `cy.request`, `cy.fixture`, `cy.wrap`, `cy.window`. These are called **parent commands**.
2. Some commands require a previous subject: `.click()`, `.type()`, `.find()`, `.should()`. These are **child commands**. You cannot call `cy.click()` directly.
3. Some commands can do either (**dual commands**): `cy.contains('Add')` or `cy.get('li').contains('Add')`.
4. A new `cy.` call starts a *new chain*. Subjects do not carry over:

```js
cy.get('#a').type('hello');
cy.get('#b').type('world');     // separate chain; #a is not involved
```

5. You can write chains over several lines for readability; indentation is for humans only.

#### 3.1 What do commands yield?

| Command | Yields |
|---|---|
| `cy.visit()` | The `window` object (rarely used) |
| `cy.get()`, `cy.contains()`, `.find()` | DOM element(s) as a jQuery object |
| `.click()`, `.type()`, `.check()` | The same subject it acted upon |
| `cy.url()` | A string |
| `cy.title()` | A string |
| `.invoke('text')` | The return value of the called method |
| `.its('length')` | The property value |
| `cy.request()` | A response object `{status, body, headers, ...}` |
| `.should()` | Usually the same subject it received (some chai assertions, such as `have.property` or `have.attr`, change the yielded subject to the value checked; see the docs) |

The Cypress documentation lists "Yields" for every command. Make a habit of checking it.

### 4. Working with values: `.then()`, `.invoke()`, `.its()`, `.as()`, `cy.wrap()`

Because you cannot assign command results to variables, Cypress gives you these tools.

#### 4.1 `.then()`

`.then(callback)` receives the previous subject as its argument and runs the callback *in order with other commands*.

```js
cy.get('[data-test="inventory-item-price"]').first().then(($price) => {
  const priceText = $price.text();           // e.g. "$29.99"
  const priceNumber = Number(priceText.replace('$', ''));
  expect(priceNumber).to.be.greaterThan(0);
});
```

- `$price` is a **jQuery-wrapped element** (the `$` prefix is a convention).
- `$price.text()` is jQuery's method to read text.
- `expect(...)` is a Chai assertion (BDD style) that throws if false. Note that assertions inside `.then()` are **not retried** (unlike `.should()`), which is why you prefer `.should()` for DOM state and use `.then()` for calculations.
- If the callback returns a Cypress command or a value, that becomes the new subject.

#### 4.2 `.invoke()` and `.its()`

These are shortcuts for common `.then()` patterns. Since Cypress 12 both are **queries**, which means they are retried together with the assertion that follows them (for example, `.invoke('text').should('eq', 'Products')` keeps re-reading the text until it matches or times out). Use them when reading a property or calling a function on the subject:

```js
cy.get('.title').invoke('text').should('eq', 'Products');   // call .text()
cy.get('input#name').invoke('val').should('be.empty');       // call .val()
cy.window().its('localStorage').invoke('getItem', 'cart-contents');
cy.get('ul li').its('length').should('be.gt', 3);            // read .length
```

- `.invoke('text')` calls the jQuery `.text()` function on the element and yields the string.
- `.its('length')` reads the property `length`.

#### 4.3 Aliases with `.as()`

An **alias** gives a name to a value so you can use it later (even in another hook or test within the same context).

```js
cy.get('[data-test="inventory-item"]').first().as('firstItem');
// ...later in the test
cy.get('@firstItem').find('button').click();
```

- `.as('firstItem')` stores the subject (and in the case of DOM elements, the *query* so Cypress can re-run it).
- `cy.get('@firstItem')` retrieves it. The `@` prefix identifies an alias.
- Aliases can store elements, fixtures, intercepted requests, and values via `cy.wrap(value).as('name')`.
- Aliases are reset between tests.

#### 4.4 `cy.wrap()`

`cy.wrap(value)` places any value into the Cypress chain so you can use `.should()` or `.then()` on it:

```js
cy.wrap({ name: 'Ada' }).its('name').should('eq', 'Ada');
cy.wrap([1, 2, 3]).should('have.length', 3);
```

It is also the tool for wrapping a jQuery element yielded to `.then()` back into the chain: `cy.wrap($el).click()`.

#### 4.5 Saving a value from one step for another

```js
let initialCount;   // normal JS variable, assigned inside a callback

cy.get('.shopping_cart_badge').should('not.exist');

cy.get('.inventory_item').its('length').then((count) => {
  initialCount = count;
  cy.log(`Products shown: ${count}`);
});

cy.get('[data-test^="add-to-cart"]').first().click();
cy.then(() => {
  expect(initialCount).to.be.greaterThan(0);   // runs later, so the variable is set
});
```

Take careful note of the pattern: assign inside `.then`, *read* inside a later `.then`. Reading the variable directly in the test body would see `undefined`, because the body runs before the commands (see the queue explanation in the architecture lesson).

### 5. Retry-ability and waiting

#### 5.1 What retries

When you write

```js
cy.get('[data-test="error"]').should('contain.text', 'locked out');
```

Cypress tries `cy.get` and the assertion repeatedly (every ~50 ms) until both succeed or `defaultCommandTimeout` (4 seconds) passes. If they never succeed, the test fails. You did not write any wait; the *query plus assertion* retried.

Only the **last query** and the **assertions** that follow it retry, plus (since Cypress 12) the whole chain of queries before it. Actions like `.click()` do not retry once they have run, and `cy.request`/`cy.task` run once.

#### 5.2 A subtle example

```js
cy.get('.todo-list li')       // query
  .should('have.length', 2)   // retried together with the query
  .first()                    // another query
  .should('contain', 'Pay bills');
```

If the list is initially empty and populated 1 second later, Cypress keeps re-querying until length is 2 (within 4 seconds), then continues.

#### 5.3 Do not use fixed sleeps

```js
cy.wait(5000);   // anti-pattern: slows every run, still flaky if the app takes 5.1 seconds
```

Better alternatives, in order of preference:

1. **Assert on the thing you are waiting for**: `cy.get('.spinner').should('not.exist')`, `cy.get('.results li').should('have.length.greaterThan', 0)`.
2. **Wait on a network call by alias**:

```js
cy.intercept('GET', '**/api/products*').as('getProducts');
cy.visit('/products');
cy.wait('@getProducts');                       // waits until the request completes
cy.get('.product').should('have.length.greaterThan', 0);
```

- `cy.intercept(method, urlPattern)` registers a spy/stub for matching requests. `**` is a glob wildcard.
- `.as('getProducts')` names the interception.
- `cy.wait('@getProducts')` waits for the *request* to occur and respond, up to `responseTimeout` and `requestTimeout`, not for a fixed time. It yields the interception object, which you can assert on:

```js
cy.wait('@getProducts').its('response.statusCode').should('eq', 200);
```

3. As a last resort, use `cy.wait(ms)` with a comment explaining why.

You will recognise this strategy from Playwright, where `page.wait_for_response` and web-first assertions play the same roles.

#### 5.4 Changing timeouts

Per command: `cy.get('.slow', { timeout: 10000 })`. Per test: `it('slow report', { defaultCommandTimeout: 10000 }, () => {...})`. Globally in `cypress.config.js`.

### 6. Visiting pages

```js
cy.visit('/');                              // relative to baseUrl
cy.visit('/inventory.html');
cy.visit('https://example.com');            // absolute
cy.visit('/search', { qs: { q: 'shoes' } }); // adds ?q=shoes
cy.visit('/', { onBeforeLoad(win) { win.localStorage.setItem('theme', 'dark'); } });
```

- `qs` builds the query string.
- `onBeforeLoad(win)` runs before the page's own scripts: good for stubbing `window` features or seeding storage.
- `cy.visit` fails if the server returns a 4xx/5xx status unless you pass `failOnStatusCode: false`.
- `cy.visit` waits for the `load` event. Apps that continue to load content after `load` need assertions to wait for it.

### 7. Reducing repeated login: `cy.session()`

Logging in through the UI before every test is slow. **`cy.session(id, setup, options)`** caches cookies, localStorage, and sessionStorage after the first login and restores them in later tests.

```js
Cypress.Commands.add('login', (username, password) => {
  cy.session(
    [username, password],            // cache key
    () => {                          // setup: runs only if no cached session
      cy.visit('/');
      cy.get('[data-test="username"]').type(username);
      cy.get('[data-test="password"]').type(password, { log: false });
      cy.get('[data-test="login-button"]').click();
      cy.url().should('include', '/inventory.html');
    },
    {
      validate() {                   // optional: confirm the session is still valid
        cy.getCookie('session-username').should('exist');
      },
    }
  );
});
```

**Explanation:**

1. `Cypress.Commands.add('login', fn)` defines a **custom command**, `cy.login(user, pass)`. (Custom commands are explored in the fixtures lesson.)
2. `cy.session` receives (a) a unique id or array so different users get different caches, (b) a setup function performing the login, and (c) options.
3. The first time, setup runs and Cypress saves the browser's cookies and storage. Subsequent calls with the same id **restore** the saved data and skip the UI login.
4. `validate` runs after restoration; if it fails, Cypress re-runs setup.
5. `{ log: false }` on `.type` hides the password from the Command Log.
6. Cypress clears the page after `cy.session` so each test must `cy.visit()` afterwards.
7. Sauce Demo stores a cookie named `session-username` on login (verify in DevTools; adapt for your own app).

Using it:

```js
beforeEach(() => {
  cy.login('standard_user', 'secret_sauce');
  cy.visit('/inventory.html');
});
```

This is the Cypress counterpart to Playwright's `storage_state` that you may have used (or will use) to reuse a logged-in state.

### 8. API calls with `cy.request()`

`cy.request()` sends an HTTP request *from Node-like context without the browser's CORS restrictions* and does not render anything. Uses: setting up data quickly, logging in via API, checking an endpoint.

```js
cy.request('GET', 'https://jsonplaceholder.typicode.com/posts/1').then((response) => {
  expect(response.status).to.eq(200);
  expect(response.body).to.have.property('userId', 1);
});

cy.request({
  method: 'POST',
  url: 'https://jsonplaceholder.typicode.com/posts',
  body: { title: 'foo', body: 'bar', userId: 1 },
}).its('status').should('eq', 201);
```

**Explanation:** The first call sends GET; `.then` receives the response object. Chai's `expect(...).to.eq` verifies status; `to.have.property('userId', 1)` verifies a field. The second sends a POST with a JSON body (objects are JSON-encoded automatically) and asserts the status via `.its('status')`. API testing in depth belongs to a different topic; here treat `cy.request` as a setup/verification tool for UI tests.

### 9. Intercepting UI traffic (beginner level)

`cy.intercept` can also *stub* a response so a UI test does not depend on a real backend:

```js
cy.intercept('GET', '**/api/products', {
  statusCode: 200,
  body: [{ id: 1, name: 'Test Backpack', price: 29.99 }],
}).as('stubProducts');
```

Stubbing a response lets you test empty states, errors (`statusCode: 500`), and slow responses (`delay: 2000`) that are hard to produce with a real server. (Fixtures and `cy.intercept` combine well; see the fixtures lesson.)

### 10. Putting it together: a complete spec

```js
describe('Sauce Demo - cart', () => {
  beforeEach(() => {
    cy.login('standard_user', 'secret_sauce');   // custom command using cy.session
    cy.visit('/inventory.html');
  });

  it('starts with an empty cart', () => {
    cy.get('[data-test="shopping-cart-badge"]').should('not.exist');
  });

  it('adds two items and shows the count', () => {
    cy.get('[data-test="add-to-cart-sauce-labs-backpack"]').click();
    cy.get('[data-test="add-to-cart-sauce-labs-bike-light"]').click();
    cy.get('[data-test="shopping-cart-badge"]').should('have.text', '2');
  });

  it('shows the added items in the cart page', () => {
    cy.get('[data-test="add-to-cart-sauce-labs-backpack"]').click();
    cy.get('[data-test="shopping-cart-link"]').click();
    cy.url().should('include', '/cart.html');
    cy.get('[data-test="inventory-item-name"]')
      .should('have.length', 1)
      .and('have.text', 'Sauce Labs Backpack');
  });
});
```

**Line-by-line:**

1. `describe('Sauce Demo - cart', ...)` groups three related tests.
2. `beforeEach` logs in via the cached session, then visits the inventory page, so each test starts from a known state (test isolation clears state between tests; `cy.session` restores the login).
3. Test 1 asserts the cart badge does not exist (`should('not.exist')` passes when no element matches).
4. Test 2 clicks two "Add to cart" buttons. The `data-test` values are derived from the product names on this practice site. It then asserts the badge text is `2`. `have.text` requires an *exact* match; `contain.text` would allow partial.
5. Test 3 adds an item, opens the cart through its link, asserts the URL, and asserts both the number of items and the name. `.and` is an alias of `.should` for readability and continues on the same subject.

---

## Code Examples

### Example 1: Reading and comparing values

```js
it('sorts products by price low to high', () => {
  cy.visit('/inventory.html');   // assume logged in via cy.session in beforeEach
  cy.get('[data-test="product-sort-container"]').select('lohi');
  cy.get('[data-test="inventory-item-price"]').then(($prices) => {
    const prices = [...$prices].map((el) => Number(el.innerText.replace('$', '')));
    const sorted = [...prices].sort((a, b) => a - b);
    expect(prices).to.deep.equal(sorted);
  });
});
```

**Explanation:**

- `.select('lohi')` chooses an `<option>` by its value or visible text; this site uses `lohi` for "Price (low to high)".
- `.then(($prices) => ...)` receives all price elements as a jQuery collection.
- `[...$prices]` spreads the jQuery collection into a regular array of DOM elements; `.map` converts each to a number by stripping `$`.
- `[...prices].sort(...)` makes a sorted copy so we do not mutate the original.
- `expect(prices).to.deep.equal(sorted)` compares the two arrays by value.

### Example 2: Waiting for a network call rather than time

```js
it('loads data after the page opens', () => {
  cy.intercept('GET', '**/posts*').as('getPosts');
  cy.visit('https://jsonplaceholder.typicode.com/');   // illustrative
  cy.wait('@getPosts').its('response.statusCode').should('be.oneOf', [200, 304]);
});
```

**Explanation:** `be.oneOf` is a Chai assertion that checks membership in an array; 304 is "Not Modified" (cached). The pattern (intercept first, then trigger, then wait) is essential: register the intercept **before** the action that triggers the request.

### Example 3: A test that uses `.within()` and `.contains()`

```js
it('adds a specific product by name', () => {
  cy.contains('[data-test="inventory-item"]', 'Sauce Labs Onesie')
    .within(() => {
      cy.get('button').click();
    });
  cy.get('[data-test="shopping-cart-badge"]').should('have.text', '1');
});
```

**Explanation:** `cy.contains(selector, text)` finds the element matching the selector that contains the text. `.within(callback)` *scopes* all `cy.get` calls inside the callback to that element. This is akin to chaining Playwright locators: `page.locator(".item").filter(has_text="Onesie").get_by_role("button")`.

### Example 4: Data-driven loop (generating tests)

```js
const invalidLogins = [
  { user: 'locked_out_user', pass: 'secret_sauce', message: 'locked out' },
  { user: 'standard_user', pass: 'wrong', message: 'do not match' },
  { user: '', pass: '', message: 'Username is required' },
];

describe('Invalid login attempts', () => {
  invalidLogins.forEach(({ user, pass, message }) => {
    it(`shows "${message}" for user "${user}"`, () => {
      cy.visit('/');
      if (user) cy.get('[data-test="username"]').type(user);
      if (pass) cy.get('[data-test="password"]').type(pass);
      cy.get('[data-test="login-button"]').click();
      cy.get('[data-test="error"]').should('contain.text', message);
    });
  });
});
```

**Explanation:** plain JavaScript `forEach` registers three `it` blocks at load time. Destructuring `({ user, pass, message })` pulls the properties out of each object. Template literals produce unique test titles. The `if (user)` guards avoid calling `.type('')`, since Cypress's `type` throws an error when given an empty string (use `.clear()` instead). In Playwright you might have used `pytest.mark.parametrize`; this is the Cypress equivalent. (Reading such data from a JSON file is covered in the fixtures lesson.)

---

## Real-World Scenarios

1. **Smoke test for a release.** A five-minute suite that logs in (via `cy.session`), loads the home page, adds to cart, and verifies the checkout page loads. Run on every deployment.
2. **Intermittent slow API.** A dashboard test used `cy.wait(3000)` and sometimes failed. The fix was to `cy.intercept('GET', '**/api/stats').as('stats')` and `cy.wait('@stats')`, cutting 2 seconds off every run and eliminating flakes.
3. **Setting up data through the API.** Instead of clicking through five screens to create a customer, the test uses `cy.request('POST', '/api/customers', body)` in `beforeEach`, then only the page under test is driven through the UI.
4. **Testing error states.** The team cannot make the real server return a 500 on demand, so the test stubs `/api/orders` with `statusCode: 500` and verifies that the UI shows a friendly error banner.
5. **Parallel contributions.** Several QEs add specs in the same repository. Consistent naming and the Arrange/Act/Assert layout let them read each other's tests quickly in code review.

---

## Common Pitfalls and Best Practices

**Pitfall 1: Using `async/await`.** Cypress commands are not Promises; use `.then`, aliases, and `cy.wrap`.

**Pitfall 2: Assertions inside `.then()` for DOM state.** They do not retry. Use `.should()` with a callback if you need custom retried logic:

```js
cy.get('.item').should(($items) => {
  expect($items).to.have.length.greaterThan(2);
});
```

Inside a `.should(callback)`, the callback itself is retried until it stops throwing. Do not put actions or `cy` commands inside it.

**Pitfall 3: Fixed waits (`cy.wait(5000)`).** Replace with assertions or `cy.wait('@alias')`.

**Pitfall 4: Depending on test order.** Cypress runs `it` blocks in file order, tempting you to build test 2 on test 1's state. With test isolation, state is cleared; each test must stand alone.

**Pitfall 5: Registering `cy.intercept` after triggering the request.** The request will already be gone.

**Pitfall 6: Conditional testing based on DOM state.** Writing `if (element exists) {...}` is brittle because the DOM changes asynchronously. Make the application state deterministic (stub data, seed via API) instead.

**Pitfall 7: Chaining off actions that change the DOM.** For example, `cy.get('button').click().should('have.class', 'active')` may hit a stale element if the app re-renders. Since Cypress 12, retrying the query handles most cases, but if you see "detached from DOM" errors on older code, re-query using a new `cy.get`.

**Pitfall 8: Long, many-purpose tests.** One `it` that tests login, cart, checkout, and profile is hard to debug. Group by flow, not everything.

**Best practices**

- Use `baseUrl` and relative `cy.visit`.
- Prefer `data-*` attributes for selectors (see the next lessons).
- Log in via `cy.session` or API, not through the UI in every test.
- Register intercepts before triggering the action and wait on aliases.
- Keep tests independent, readable (Arrange/Act/Assert), and named for behaviour.
- Hide secrets from the Command Log with `{ log: false }`.

---

## Mini Practice Exercises

**Exercise 1 - Structure.**
Rewrite the following flat sequence into a `describe` with a `beforeEach` and two `it` blocks, one for valid login and one for invalid login:

```js
cy.visit('/'); cy.get('[data-test="username"]').type('standard_user'); /* ... */
```

*Hint:* the visit goes in `beforeEach`, and each `it` types its own credentials.

**Exercise 2 - Alias.**
Write a test that finds the first product on the inventory page, stores its name text in an alias, clicks the product name link, and asserts that the product detail page shows the same name.

*Solution:*

```js
it('opens the same product that was clicked', () => {
  cy.visit('/inventory.html');   // after login via session
  cy.get('[data-test="inventory-item-name"]').first().invoke('text').as('name');
  cy.get('[data-test="inventory-item-name"]').first().click();
  cy.get('@name').then((name) => {
    cy.get('[data-test="inventory-item-name"]').should('have.text', name);
  });
});
```

**Exercise 3 - Replace a wait.**
Given `cy.get('#load').click(); cy.wait(4000); cy.get('.row').should('exist');`, rewrite it using an intercept alias. Assume the endpoint is `/api/rows`.

*Solution:*

```js
cy.intercept('GET', '**/api/rows').as('rows');
cy.get('#load').click();
cy.wait('@rows');
cy.get('.row').should('exist');
```

**Exercise 4 - Session.**
Convert your login into a `cy.session`-based custom command `cy.login`. Verify (by watching the Command Log) that the second test does not repeat the UI login.

**Exercise 5 - Port a Playwright test.**
Choose one test you wrote on Monday. Port it to Cypress and note in two or three lines: what was *shorter*, what was *longer*, and what you needed to do differently (for example, no `await`, `.type` vs `.fill`).

**Exercise 6 - Data driven.**
Extend Example 4 with a fourth case: a user with whitespace only in the username. What message does the application display? Record it and add the case.

---

## Summary / Key Takeaways

- A spec file contains `describe`/`context` suites and `it` tests, with `beforeEach` hooks for shared setup; name tests after behaviours.
- Follow **Arrange - Act - Assert**; keep tests independent and readable.
- Cypress commands form chains where each command yields a **subject** to the next; parent, child, and dual commands behave differently.
- You cannot `await` Cypress commands. Use `.then()`, `.invoke()`, `.its()`, `.as()` aliases, and `cy.wrap()`.
- **Retry-ability** (queries plus assertions) replaces most explicit waits. Use `cy.intercept(...).as()` and `cy.wait('@alias')` to wait for network events, never fixed sleeps.
- `cy.session()` caches login state; `cy.request()` calls APIs; `cy.intercept()` stubs or spies on network calls.
- Structure of Playwright and Cypress tests is conceptually the same; the differences are syntax, implicit globals, and the async model.
- Screenshots on failure, video, and the visual time-travel experience are **covered in depth on Friday**.

---

## External Resources

- Cypress Documentation - Writing Your First E2E Test: https://docs.cypress.io/app/end-to-end-testing/writing-your-first-end-to-end-test
- Cypress Documentation - Retry-ability: https://docs.cypress.io/app/core-concepts/retry-ability
- Cypress Documentation - `cy.session()`: https://docs.cypress.io/api/commands/session
