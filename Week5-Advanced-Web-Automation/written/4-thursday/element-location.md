# Element Location in Cypress

## Learning Objectives

By the end of this lesson you will be able to:

- Locate elements with `cy.get()` using CSS selectors (id, class, tag, attribute, combinations, and pseudo-selectors).
- Locate elements by visible text with `cy.contains()`, including regular expressions, selector-plus-text, and case sensitivity.
- Traverse the DOM using `.find()`, `.within()`, `.eq()`, `.first()`, `.last()`, `.parent()`, `.parents()`, `.closest()`, `.children()`, `.siblings()`, `.next()`, `.prev()`, `.filter()`, and `.not()`.
- Rank selector strategies from most to least resilient, and explain why Cypress recommends dedicated `data-*` attributes.
- Use the **Selector Playground** to generate and test selectors, and customise its priority order.
- Handle lists, tables, and repeated components using scoping.
- Reach into the Shadow DOM using `includeShadowDom` and `.shadow()`, and recognise the approach for iframes.
- Use the Testing Library plugin for role- and label-based queries (the Cypress equivalent of Playwright's `get_by_role`).
- Compare Cypress locators with the Playwright locators you used earlier in the week.

---

## Why This Matters

Test automation fails most often at the *selector* level. A test that is perfectly designed will break if it points at `div > div:nth-child(3) > span`, and a developer moves an element. Industry surveys of flaky tests repeatedly list "brittle locators" among the top causes. The skill of picking a selector that survives refactors is therefore one of the highest-value skills a test automation engineer can build.

Tie this to the Week 5 epic: Monday-Wednesday you learned Playwright's locator model (`get_by_role`, `get_by_text`, `locator(...).filter(...)`, chaining), and you saw how that supported complicated interactions (frames, tables, shadow DOM). Cypress has its own model, which is built around **jQuery-style selectors and DOM traversal**. In your Project 1 comparison note you will be asked to compare how each tool locates elements; this lesson gives you the vocabulary.

### Playwright (Python) vs Cypress locator cheat sheet

| Intent | Playwright (Python) | Cypress (JavaScript) |
|---|---|---|
| By CSS | `page.locator(".item")` | `cy.get('.item')` |
| By test id | `page.get_by_test_id("login")` | `cy.get('[data-test="login"]')` |
| By visible text | `page.get_by_text("Add to cart")` | `cy.contains('Add to cart')` |
| By role + name | `page.get_by_role("button", name="Login")` | `cy.findByRole('button', {name: 'Login'})` (Testing Library plugin) |
| By label | `page.get_by_label("Email")` | `cy.findByLabelText('Email')` (plugin) |
| By placeholder | `page.get_by_placeholder("Username")` | `cy.get('[placeholder="Username"]')` |
| Child within parent | `parent.locator("button")` | `cy.get('.parent').find('button')` |
| Nth element | `page.locator("li").nth(2)` | `cy.get('li').eq(2)` |
| First/last | `.first` / `.last` | `.first()` / `.last()` |
| Filter by text | `.filter(has_text="x")` | `cy.contains('li', 'x')` or `.filter(':contains("x")')` |
| XPath | `page.locator("xpath=//div")` | Not built in; plugin `cypress-xpath` |
| Shadow DOM | Pierced by default | `includeShadowDom: true` or `.shadow()` |

A crucial conceptual difference: Playwright `locator` objects are *lazy descriptions* that you can store and reuse; Cypress `cy.get()` is a *command in a queue*, which you re-issue when you need it again (or alias with `.as()`).

---

## The Concept

### 1. `cy.get()` and CSS selectors

`cy.get(selector)` finds DOM elements matching a **CSS selector** (or a jQuery selector) and yields them. It **retries** until at least one element is found (or the timeout passes) and the following assertions, if any, pass.

Quick CSS selector refresher (everything here works inside `cy.get`):

| Selector | Meaning | Example |
|---|---|---|
| `#id` | Element with that `id` | `cy.get('#login-button')` |
| `.class` | Element(s) with that class | `cy.get('.inventory_item')` |
| `tag` | Elements of that HTML tag | `cy.get('button')` |
| `[attr]` | Elements with that attribute | `cy.get('[disabled]')` |
| `[attr="value"]` | Attribute exactly equals value | `cy.get('[data-test="username"]')` |
| `[attr^="x"]` | Attribute starts with | `cy.get('[data-test^="add-to-cart"]')` |
| `[attr$="x"]` | Attribute ends with | `cy.get('[href$=".pdf"]')` |
| `[attr*="x"]` | Attribute contains | `cy.get('[class*="price"]')` |
| `a b` | `b` anywhere inside `a` (descendant) | `cy.get('ul li')` |
| `a > b` | `b` directly inside `a` (child) | `cy.get('ul > li')` |
| `a + b` | `b` immediately after `a` (adjacent sibling) | `cy.get('label + input')` |
| `a ~ b` | `b` any later sibling of `a` | `cy.get('h2 ~ p')` |
| `a, b` | Either `a` or `b` | `cy.get('h1, h2')` |
| `:first-child`, `:last-child`, `:nth-child(n)` | Structural pseudo-classes | `cy.get('li:nth-child(2)')` |
| `:not(x)` | Negation | `cy.get('input:not([disabled])')` |
| `:checked`, `:disabled`, `:enabled` | State pseudo-classes | `cy.get('input:checked')` |
| `:visible`, `:contains("text")`, `:eq(n)` | jQuery extensions (non-standard CSS, but supported by `cy.get`) | `cy.get('li:contains("Onesie")')` |

Example:

```js
cy.get('input[type="text"]:not([disabled])');
```

- `input` - the tag.
- `[type="text"]` - only inputs whose `type` attribute is `text`.
- `:not([disabled])` - exclude disabled inputs.
- The whole expression finds enabled text inputs.

**Options for `cy.get`:**

```js
cy.get('.slow-widget', { timeout: 10000 });           // wait up to 10 s
cy.get('.widget', { log: false });                    // do not log to the Command Log
cy.get('my-component .inner', { includeShadowDom: true }); // pierce shadow DOM
```

#### 1.1 When nothing is found

If no element matches within the timeout, Cypress fails the test with a message such as: `Timed out retrying after 4000ms: Expected to find element: '[data-test="oops"]', but never found it.` Reading this message is your first debugging step: either the selector is wrong, or the element appears later than the timeout, or it is inside an iframe or shadow DOM.

You can *assert absence* intentionally:

```js
cy.get('[data-test="shopping-cart-badge"]').should('not.exist');
```

Cypress knows that `should('not.exist')` means "retry until it is gone," so it does not fail on "never found".

### 2. `cy.contains()` - locating by text

```js
cy.contains('Sauce Labs Backpack');                      // first element containing this text
cy.contains('button', 'Add to cart');                    // selector + text
cy.contains(/^Add to cart$/);                            // regular expression, exact match
cy.contains('add to cart', { matchCase: false });        // case-insensitive
cy.get('.inventory_item').contains('Onesie');            // search only inside these elements
```

**Key behaviours:**

1. `cy.contains` yields the **deepest element** that contains the text, not the outermost. If a `<div>` contains `<button>Add</button>`, `cy.contains('Add')` yields the `<button>`.
2. It is **case-sensitive by default** (`matchCase: true`).
3. When several elements contain the text, it **prefers certain element types** in this order: `input[type='submit']`, `button`, `a`, `label` (so `cy.contains('Submit')` favours the button over a paragraph containing the same word); otherwise it yields the first match in document order.
4. It **normalises whitespace**: multiple spaces/newlines in the DOM collapse to a single space before matching.
5. It matches **partial text** unless you use a regex with anchors.
6. When used with a selector (`cy.contains('li', 'Apple')`), it yields the *matching element of that selector*, not the deepest descendant. This is the most useful form for rows and cards.

Using visible text as a locator mirrors how a human finds a thing, which makes tests readable; but it is sensitive to wording changes and to **localisation** (a French UI says "Ajouter au panier"). Use it for stable, user-facing labels, and prefer test attributes for elements whose text changes.

### 3. DOM traversal commands

Once you have one element, you often need its neighbours. Cypress provides jQuery's traversal commands. Understanding the family tree metaphor helps:

```
<ul class="list">                  <- parent of li
  <li class="a">Apple</li>        <- first child, sibling of the others
  <li class="b" id="target">Banana</li>
  <li class="c">Cherry</li>       <- next sibling
</ul>
```

| Command | What it does | Example |
|---|---|---|
| `.find(selector)` | Descendants (children, grandchildren, ...) matching selector | `cy.get('.list').find('li')` |
| `.children([selector])` | Direct children only | `cy.get('.list').children()` |
| `.parent()` | The direct parent | `cy.get('#target').parent()` |
| `.parents([selector])` | All ancestors, up to `html` | `cy.get('#target').parents('div')` |
| `.parentsUntil(selector)` | Ancestors up to (not including) a match | `cy.get('#target').parentsUntil('body')` |
| `.closest(selector)` | Nearest ancestor (including itself) matching selector | `cy.get('#target').closest('.card')` |
| `.siblings([selector])` | All siblings, excluding itself | `cy.get('#target').siblings()` |
| `.next([selector])` / `.prev()` | Immediately following / preceding sibling | `cy.get('#target').next()` |
| `.nextAll()` / `.prevAll()` | All following / preceding siblings | `cy.get('.a').nextAll()` |
| `.first()` / `.last()` | First / last in the collection | `cy.get('li').first()` |
| `.eq(index)` | The element at zero-based index; negative counts from the end | `cy.get('li').eq(1)`; `.eq(-1)` is last |
| `.filter(selector)` | Keep only those matching a selector or function | `cy.get('li').filter('.active')` |
| `.not(selector)` | Remove those matching | `cy.get('li').not('.disabled')` |
| `.within(callback)` | Scope all `cy.get` inside the callback to the subject | see below |

**Important distinction: `.find()` vs `.within()` vs `cy.get()`**

- `cy.get('.card').find('button')` - finds buttons **inside** each `.card`; yields the buttons.
- `cy.get('.card').within(() => { cy.get('button').click(); })` - inside the callback, `cy.get` searches only in the card. Good when you need several commands against the same container, such as filling a form section.
- `cy.get('button')` - searches the whole page.

`.within()` requires the subject to be a **single** element; if `.get` returns multiple, use `.first()` or `.eq()` first.

#### 3.1 Row-and-card scoping pattern

Most real UIs repeat a component many times: product cards, table rows, list items. The reliable method is "find the container by its text, then work *inside* it":

```js
cy.contains('[data-test="inventory-item"]', 'Sauce Labs Bike Light')
  .find('button')
  .click();
```

- `cy.contains(selector, text)` finds the **card** whose text includes the product name.
- `.find('button')` locates the button *inside that card*.
- `.click()` adds only that product to the cart.

Compare this with the brittle alternative `cy.get(':nth-child(3) button')`, which breaks when product order changes.

#### 3.2 Table example

```js
cy.get('table tbody tr')
  .contains('td', 'Alice')       // find the cell with the name
  .parent('tr')                  // go up to the row
  .within(() => {
    cy.get('td').eq(2).should('contain.text', 'Admin'); // third column is the role
  });
```

- `.contains('td', 'Alice')` finds the `<td>` containing "Alice" within the rows.
- `.parent('tr')` goes to its parent row (only if the parent is `tr`).
- `.within(...)` scopes subsequent `cy.get` to that row.
- `cy.get('td').eq(2)` selects the third cell (index 2).

Recall Tuesday's Playwright web tables lesson where you filtered rows with `locator("tr").filter(has_text="Alice")` and picked cells by index; the logic is identical, only the syntax differs.

### 4. Selector strategies: from most to least resilient

A **resilient selector** continues to work when the page is restyled or restructured. A **brittle selector** breaks easily. Cypress's official best-practices guide ranks selectors roughly as follows:

| Rank | Selector type | Example | Resilience |
|---|---|---|---|
| 1 (best) | Dedicated test attribute | `[data-cy="submit"]`, `[data-test="submit"]`, `[data-testid="submit"]` | Very high: exists only for tests; unaffected by styling or copy changes |
| 2 | ARIA role/name or label (Testing Library) | `findByRole('button', {name: /submit/i})` | High: tied to accessibility semantics |
| 3 | Visible text | `cy.contains('Submit')` | Medium: breaks when wording or language changes |
| 4 | Semantic attributes | `[name="email"]`, `[type="email"]`, `[aria-label="Close"]` | Medium |
| 5 | `id` | `#login-button` | Medium: ids can be generated or changed by devs |
| 6 | Class names | `.btn-primary` | Low: classes serve styling, change often, may be hashed (`.css-1x2y3z`) |
| 7 | Tag names | `button` | Low: ambiguous |
| 8 (worst) | Position / structure | `div > div:nth-child(3) > span` | Very low |

**Why `data-*` attributes?** Because their sole purpose is testing. A developer who sees `data-cy="submit"` knows removing it may break a test. Styles and copy can change freely. Cypress documentation recommends `data-cy`, `data-test`, or `data-testid`; the exact name does not matter, but the **team must agree on one**. The practice site we use, Sauce Demo, uses `data-test`.

If the application under test lacks such attributes, partnering with developers to add them is a high-leverage QA activity. In your Project 1 context, adding `data-test` hooks to the app you build is part of "designing for testability".

#### 4.1 Avoiding auto-generated and layout-based selectors

- Do not copy absolute XPath or "copy selector" output from DevTools without review; it often contains `nth-child` chains.
- Be wary of ids like `#react-select-3-input` that include counters; they may change by run.
- Do not rely on a CSS-in-JS class like `.css-1a2b3c`; the hash changes on each build.

#### 4.2 A helper for test attributes

Many teams add a tiny custom command so tests read well:

```js
// cypress/support/commands.js
Cypress.Commands.add('getByTest', (value, options) => {
  return cy.get(`[data-test="${value}"]`, options);
});
```

Usage: `cy.getByTest('username').type('standard_user');`.

Line by line: `Cypress.Commands.add(name, callback)` registers `cy.getByTest`; the callback receives the arguments you pass; template literals build the attribute selector; `return cy.get(...)` returns the chain so it can be followed by `.type()`, `.click()`, or `.should()`. (Custom commands are described in the Fixtures lesson.)

### 5. The Selector Playground

Cypress's runner has a built-in tool to help you discover selectors.

1. Open a spec in `cypress open`.
2. In the application preview toolbar, click the **target icon** ("Open Selector Playground").
3. Hover over elements in your app: Cypress highlights them and shows the **recommended selector**. Click an element to lock it.
4. Use the **Copy** button to copy the `cy.get(...)` command or **Print to console**.
5. Type your own selector into the playground to see how many elements it matches ("1 match" is ideal).

By default the playground prioritises, in order: `data-cy`, `data-test`, `data-testid`, `data-testing`, `id`, `class`, `tag`, `attributes`, `nth-child`. You can change the priority in your support file:

```js
// cypress/support/e2e.js
Cypress.SelectorPlayground.defaults({
  selectorPriority: ['data-test', 'data-cy', 'id', 'class', 'tag', 'attributes', 'nth-child'],
  onElement: ($el) => {
    // optionally return a custom selector string; return undefined to use default logic
    const testId = $el.attr('data-test');
    if (testId) return `[data-test="${testId}"]`;
  },
});
```

**Explanation:**

- `selectorPriority` is the ordered list the playground tries.
- `onElement` is a function invoked for each hovered element; returning a string overrides the suggested selector. Returning nothing falls back to the priority list.

(Related debugging: you can also use the browser DevTools console: `document.querySelectorAll('[data-test="x"]').length` to test a selector. Using the full interactive debugging experience, including time-travel snapshots, is **covered in depth on Friday**.)

### 6. Testing Library plugin: role- and label-based locators

If you liked Playwright's `get_by_role`, the community **Cypress Testing Library** brings the same philosophy.

Install and import:

```bash
npm install --save-dev @testing-library/cypress
```

```js
// cypress/support/commands.js
import '@testing-library/cypress/add-commands';
```

Then use:

```js
cy.findByRole('button', { name: /login/i }).click();
cy.findByLabelText('Email').type('ada@example.com');
cy.findByPlaceholderText('Username').type('standard_user');
cy.findByText('Products').should('be.visible');
cy.findByTestId('shopping-cart-link').click();     // uses data-testid by default
cy.findAllByRole('listitem').should('have.length', 6);
```

**Explanation:**

- `findByRole(role, {name})` finds one element by its ARIA role (implicit or explicit) and accessible name. If zero or multiple are found, it fails, which is good: it forces unambiguous locators.
- `findAllBy...` returns multiple elements.
- `findByTestId` uses `data-testid` by default. To use `data-test`, configure `configure({ testIdAttribute: 'data-test' })` from `@testing-library/cypress`.
- The plugin is not required; it is a trade-off. It encourages accessible markup (because roles and labels must exist) but adds a dependency.

### 7. Aliasing and re-querying

Because Cypress queries are re-run from scratch whenever they are retried, you can safely store a *query* by alias:

```js
cy.get('[data-test="inventory-item"]').as('items');
cy.get('@items').should('have.length.greaterThan', 2);
cy.get('@items').first().find('button').click();
```

`cy.get('@items')` re-runs the original query (since Cypress 12), so you do not get stale elements.

### 8. Elements that are not simple to find

#### 8.1 Elements that appear later

`cy.get` already retries, so most delays need no extra code. For slow components, increase the timeout for that one call: `cy.get('.report', { timeout: 15000 })`.

#### 8.2 Hidden elements

`cy.get` finds hidden elements too (it queries the DOM). Visibility checks occur when you *act* on them, or when you assert `.should('be.visible')`. If a menu item exists but is hidden until hover, `.click()` will fail with an "element is not visible" error. Solutions include triggering the visibility interaction first (`.trigger('mouseover')`), or `.click({ force: true })` as a last resort (see the "Element interaction" lesson).

#### 8.3 Multiple matches

`cy.get('li')` yields many; `.click()` on multiple fails by default ("can only be called on a single element") unless you use `{ multiple: true }`. Narrow with `.first()`, `.eq()`, `.filter()`, or better a more specific selector.

#### 8.4 Shadow DOM

A **shadow DOM** is an encapsulated sub-tree used by web components (you met it in Tuesday's Playwright lesson, where locators pierce open shadow roots by default). Cypress by default does **not** search inside shadow roots. Two ways:

```js
// Option A: per command
cy.get('my-widget').shadow().find('button').click();

// Option B: per command with option
cy.get('button.inner', { includeShadowDom: true }).click();

// Option C: globally in cypress.config.js
// e2e: { includeShadowDom: true }
```

- `.shadow()` yields the shadow root of the subject so you can `.find()` inside it.
- `includeShadowDom: true` makes `get`, `find`, `contains`, and `within` traverse shadow roots automatically. Setting it in config is the easiest for projects heavy in web components.

#### 8.5 iframes

Cypress does not have a built-in "switch to frame" like Playwright's `frame_locator`. The classic approach is to access the iframe's document and wrap its body:

```js
cy.get('iframe#editor')
  .its('0.contentDocument.body')      // the iframe's <body> element
  .should('not.be.empty')             // wait until the iframe content loaded
  .then(cy.wrap)                      // wrap the body so Cypress commands can be used on it
  .find('p.intro')
  .should('contain.text', 'Hello');
```

**Explanation:** `.its('0.contentDocument.body')` reads the first matched iframe element's `contentDocument.body` (works for same-origin frames). `.then(cy.wrap)` passes the raw element to `cy.wrap`, putting it back in the Cypress chain. The `cypress-iframe` plugin offers `cy.frameLoaded()` and `cy.iframe()` for tidier code. Cross-origin iframes are restricted by browsers; check documentation for `cy.origin` and the `chromeWebSecurity` setting when needed.

#### 8.6 New tabs

Cypress cannot control a second tab. Remove the `target` attribute (`cy.get('a').invoke('removeAttr', 'target').click()`) or follow the `href`.

### 9. Practical recipe: choosing a selector

Use this decision flow when writing a locator:

1. Is there a `data-*` test attribute? Use it.
2. If not, can I use role/label (Testing Library) or a semantic attribute such as `name`, `aria-label`, or `type`?
3. Is the visible text stable and unique? Use `cy.contains`, scoped to a container.
4. Is there an `id` that is human-written and stable? Use it.
5. If none apply, **ask the developers to add a test attribute**. Only as a last resort use structural selectors, and document why.

Then verify the selector matches **exactly the elements you intend**: in the Selector Playground, count of matches; in a test, `cy.get(selector).should('have.length', 1)` during development.

---

## Code Examples

### Example 1: Locating the login form elements

```js
describe('Locators on the login page', () => {
  beforeEach(() => cy.visit('/'));

  it('finds elements in several ways', () => {
    cy.get('[data-test="username"]').should('be.visible');     // test attribute
    cy.get('#password').should('have.attr', 'type', 'password'); // id
    cy.get('input[type="submit"]').should('have.value', 'Login'); // semantic attribute
    cy.contains('Accepted usernames are').should('be.visible'); // visible text
    cy.get('form').find('input').should('have.length', 3);      // descendants (2 fields + submit)
  });
});
```

**Explanation:**

- `beforeEach(() => cy.visit('/'))` - shorthand arrow function returning the chain (a single expression returns it implicitly).
- Line 1: attribute selector for a `data-test` attribute.
- Line 2: ID selector `#password`; `.should('have.attr', 'type', 'password')` verifies attribute name and value.
- Line 3: `input[type="submit"]` is a tag + attribute selector; `have.value` checks the input's value (for submit buttons this is the label text).
- Line 4: finds an element by text; the credentials hint on the page begins with "Accepted usernames are".
- Line 5: scoping with `.find('input')`; `have.length` checks the number of matches (verify in DevTools; the form has three `input` elements).

### Example 2: Working with a list by text

```js
it('removes the cart item for a specific product', () => {
  cy.login('standard_user', 'secret_sauce');           // custom command (cy.session)
  cy.visit('/inventory.html');
  cy.get('[data-test="add-to-cart-sauce-labs-bolt-t-shirt"]').click();
  cy.get('[data-test="shopping-cart-link"]').click();

  cy.contains('[data-test="inventory-item"]', 'Sauce Labs Bolt T-Shirt')
    .find('button')
    .click();

  cy.get('[data-test="inventory-item"]').should('not.exist');
});
```

**Explanation:** after adding one item and opening the cart, we locate its row by the product name, click the Remove button inside it, and confirm the cart is empty by asserting the rows no longer exist.

### Example 3: Traversal

```js
cy.get('[data-test="inventory-item-name"]')
  .first()
  .closest('[data-test="inventory-item"]')      // go up to the card
  .find('[data-test="inventory-item-price"]')   // go down to the price
  .invoke('text')                               // read the element's text as a string
  .should('match', /^\$\d+\.\d{2}$/);           // matches "$29.99" style text
```

**Explanation:** `closest` walks up the ancestors until it meets the card; `find` walks down to the price element; `.invoke('text')` converts the element into its text string so that Chai's `match` assertion can compare it with a regular expression (on a raw element, `match` would instead mean "matches this CSS selector"). Both illustrate the "up then down" navigation that is typical when the element you can identify (a name) is not the one you need (a price).

### Example 4: Custom command and Playwright comparison

Cypress:

```js
Cypress.Commands.add('getByTest', (id) => cy.get(`[data-test="${id}"]`));

cy.getByTest('username').type('standard_user');
cy.getByTest('login-button').click();
```

Playwright (Python) for the same job:

```python
page.get_by_test_id("username").fill("standard_user")
page.get_by_test_id("login-button").click()
```

In Playwright you configure `test_id_attribute` once (`playwright.selectors.set_test_id_attribute("data-test")`) and get a built-in method. Cypress has no built-in test-id locator; a one-line custom command achieves the same result.

---

## Real-World Scenarios

1. **Design refresh.** The product team replaces the CSS framework; every class name changes. Tests using `[data-test]` selectors pass without edits; tests using `.btn.btn-lg.btn-primary` all fail. The team spends a day fixing selectors and decides to adopt a `data-test` convention.
2. **Localised app.** A global company ships French and German UIs. Tests relying on `cy.contains('Add to cart')` fail in other locales; the team switches to `data-test` selectors for actions and keeps text-based assertions only in locale-specific tests.
3. **Data grids.** An admin console shows 50 users in a paged table. Tests locate the row via `cy.contains('tr', 'ada@example.com')` rather than by row number, so adding or sorting rows does not break them.
4. **Web components library.** A design system built with Lit uses shadow DOM heavily. Setting `includeShadowDom: true` in config lets existing selectors work without sprinkling `.shadow()` everywhere.
5. **Accessibility synergy.** Using Testing Library's `findByRole('button', {name: 'Pay now'})` surfaces a missing accessible name on an icon-only button; the test failure doubles as an accessibility defect.

---

## Common Pitfalls and Best Practices

**Pitfall 1: Selecting by position or long CSS chains.** `div:nth-child(2) > ul > li:nth-child(4)` breaks at the first layout change.

**Pitfall 2: Using auto-generated classes or ids.** CSS-in-JS class hashes and counters change between builds.

**Pitfall 3: Ambiguous selectors.** `cy.get('button')` matches many buttons; `.click()` fails or hits the wrong one. Aim for *one* match.

**Pitfall 4: Over-reliance on text.** Copy changes and translations break tests.

**Pitfall 5: Storing elements in variables.**

```js
const btn = cy.get('button');   // does not work like you expect
```

Use aliases (`.as('btn')`) and re-query with `cy.get('@btn')`.

**Pitfall 6: Forgetting `includeShadowDom`.** If `cy.get` never finds an element you can see in DevTools, check whether it is inside a shadow root or iframe.

**Pitfall 7: `.within()` on multiple elements.** It errors if the subject has more than one element; reduce to one with `.first()` or `.eq()`.

**Pitfall 8: Mixing `cy.get` inside `.then` and expecting retries.** Once inside a `.then`, DOM state you captured is a snapshot. Re-query when you need fresh state.

**Best practices**

- Agree a `data-*` attribute convention with developers and write it down.
- Wrap common lookups in custom commands (`cy.getByTest`).
- Scope: container first (`cy.contains('[data-test="row"]', 'Alice')`), then `.find()` inside.
- Use Selector Playground and DevTools to confirm one match.
- Keep selectors out of test bodies when they repeat (a selectors object or, later, a Page Object).
- Review selectors in code review the same way you review logic.

---

## Mini Practice Exercises

**Exercise 1 - Rank.**
Rank these selectors for a "Save" button from most to least resilient and explain your ranking: `button.css-9x8y7`, `[data-cy="save"]`, `div.form > div:nth-child(5) > button`, `cy.contains('button', 'Save')`.

*Answer:* `[data-cy="save"]` > `cy.contains('button', 'Save')` > `button.css-9x8y7` (generated class) > the `nth-child` chain.

**Exercise 2 - Find all.**
On Sauce Demo's inventory page, write a test that asserts there are exactly 6 products using `[data-test="inventory-item"]`. Then assert each product has a button inside.

*Hint:* `cy.get('[data-test="inventory-item"]').each(($item) => { cy.wrap($item).find('button').should('exist'); })` (`.each` iterates; `cy.wrap` re-enters Cypress).

**Exercise 3 - Contains.**
Write a test that adds only "Sauce Labs Fleece Jacket" to the cart using `cy.contains` scoped to the product card. Assert the cart badge shows `1`.

**Exercise 4 - Traversal.**
Starting at the product *name* "Test.allTheThings() T-Shirt (Red)", navigate to its price element using `closest` and `find`. Assert the price text is formatted as `$` followed by digits.

**Exercise 5 - Selector Playground.**
Open the Selector Playground. Hover over the login button. Record the suggested selector. Then change `Cypress.SelectorPlayground.defaults` so that `data-test` is the first priority and confirm the suggestion changes (restart the spec).

**Exercise 6 - Shadow DOM (research).**
On `https://example.cypress.io/commands/querying`, no shadow DOM is present. Visit a site with a known web component (search for "Shoelace" or Lit demo pages), set `includeShadowDom: true` in config, and click a shadow-rooted button. What changes if you do not set the option?

**Exercise 7 - Port.**
Port a Monday Playwright test that uses `get_by_role` and `get_by_label` into Cypress twice: once with plain `cy.get` and once with the Testing Library plugin. Compare readability and write two sentences in your comparison note.

---

## Summary / Key Takeaways

- `cy.get(selector)` finds elements by CSS (plus jQuery extensions) and retries until found; `cy.contains(text)` finds elements by visible text and yields the deepest match, or the selector's match when you pass a selector.
- Traversal commands (`find`, `parent`, `closest`, `children`, `siblings`, `next`, `prev`, `eq`, `first`, `last`, `filter`, `not`) move around the DOM tree; `.within()` scopes subsequent commands to one element.
- The most resilient selectors are dedicated **`data-*` test attributes**; then roles/labels, stable text, ids; the least resilient are classes and positional selectors.
- Use the **Selector Playground** to explore, and customise its priority list for your team's convention.
- Shadow DOM requires `.shadow()` or `includeShadowDom`; iframes need the `contentDocument.body` pattern or a plugin; a second tab is not controllable.
- Cypress has no built-in role/label locator; the `@testing-library/cypress` plugin provides Playwright-like `findByRole`, `findByLabelText`.
- Always aim for a selector that matches exactly one intended element and survives refactoring.
- The full time-travel and snapshot debugging experience for inspecting what selectors saw is **covered in depth on Friday**.

---

## External Resources

- Cypress Documentation - Best Practices (Selecting Elements): https://docs.cypress.io/app/core-concepts/best-practices#Selecting-Elements
- Cypress Documentation - `cy.get()`: https://docs.cypress.io/api/commands/get
- Cypress Documentation - `cy.contains()`: https://docs.cypress.io/api/commands/contains
