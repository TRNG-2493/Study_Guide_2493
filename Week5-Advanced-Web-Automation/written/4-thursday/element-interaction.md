# Element Interaction in Cypress

## Learning Objectives

By the end of this lesson you will be able to:

- Explain Cypress's **actionability** checks (visible, enabled, not detached, not covered, scrolled into view, not animating) and why they remove most explicit waits.
- Perform mouse interactions: `.click()`, `.dblclick()`, `.rightclick()`, click positions, modifier keys, and multiple clicks.
- Type and edit text with `.type()`, `.clear()`, special key sequences (`{enter}`, `{selectall}`, `{backspace}`, `{shift}`), and understand the `delay` and `parseSpecialCharSequences` options.
- Work with checkboxes and radio buttons using `.check()` and `.uncheck()`, and dropdowns using `.select()` (single and multiple).
- Use `.focus()`, `.blur()`, `.submit()`, `.scrollIntoView()`, `.scrollTo()`, and `.trigger()` for lower-level events (including a workaround for hover).
- Handle alerts, confirms, and prompts using Cypress events and stubs.
- Upload files with `.selectFile()` and simulate drag and drop.
- Know when `{ force: true }` is appropriate (rarely) and what it skips.
- Map each Cypress interaction to the Playwright (Python) interaction you learned on Monday and Tuesday.

---

## Why This Matters

Test automation is, at heart, "do something the way a user would, then check the result." Clicking, typing, choosing from a dropdown, and ticking a box are the verbs of your tests. If those verbs are unreliable, the tests are unreliable.

On Monday you covered alerts and dialogs, radio buttons and checkboxes, dropdowns and multi-selects, keyboard and mouse actions, and auto-suggestions in Playwright; on Tuesday you covered file upload and other advanced interactions. This lesson shows the same categories in Cypress so you can port your Project 1 tests confidently. The key differences you should be able to explain to a hiring manager are:

1. Cypress simulates user events **by dispatching events in the page** (with careful emulation of the real sequence a browser would fire), while Playwright sends **real input events through the browser protocol**. Both are "realistic" for nearly all apps; the differences appear in edge cases such as hover menus or native pickers.
2. Cypress's **actionability** waits are similar to Playwright's auto-waiting, but the rules and error messages differ.
3. Cypress has no `fill()` shortcut; `.type()` types characters one by one (you can set values directly with `.invoke('val', ...)` plus a trigger when speed matters).

### Playwright (Python) to Cypress cheat sheet

| Action | Playwright (Python) | Cypress |
|---|---|---|
| Click | `locator.click()` | `.click()` |
| Double click | `locator.dblclick()` | `.dblclick()` |
| Right click | `locator.click(button="right")` | `.rightclick()` |
| Type / fill | `locator.fill("x")` / `press_sequentially("x")` | `.type('x')` |
| Clear | `locator.clear()` | `.clear()` |
| Press a key | `locator.press("Enter")` | `.type('{enter}')` |
| Check/uncheck | `locator.check()` / `.uncheck()` | `.check()` / `.uncheck()` |
| Select option | `locator.select_option("lohi")` | `.select('lohi')` |
| Hover | `locator.hover()` | No native hover; `.trigger('mouseover')` or `cypress-real-events` `realHover()` |
| Focus / blur | `locator.focus()` / `.blur()` | `.focus()` / `.blur()` |
| Scroll into view | `locator.scroll_into_view_if_needed()` | `.scrollIntoView()` |
| Upload | `locator.set_input_files(path)` | `.selectFile(path)` |
| Drag and drop | `source.drag_to(target)` | `.trigger()` sequence or plugin |
| Dialog handling | `page.on("dialog", handler)` | `cy.on('window:alert', ...)`, `cy.on('window:confirm', ...)` |
| Force action | `click(force=True)` | `.click({ force: true })` |

---

## The Concept

### 1. Actionability: what Cypress checks before acting

Before an **action command** such as `.click()` or `.type()`, Cypress performs a sequence of checks and waits (up to `defaultCommandTimeout`, 4 seconds by default) for them to pass. This behaviour is called **actionability**. The checks are:

| Check | What it means |
|---|---|
| **Element exists** | Found by the preceding query. |
| **Not detached** | The element is still attached to the DOM (not removed by a re-render). |
| **Visible** | It has non-zero size, is not `display: none`, not `visibility: hidden`, and is not clipped by an `overflow: hidden` ancestor. (Options exist for `opacity: 0` handling, which counts as visible for actions but not for `be.visible` assertions.) |
| **Not disabled** | A `disabled` form element cannot be clicked or typed into. |
| **Not read-only** | `.type()` requires the field to accept input. |
| **Not animating** | The element's position is stable across frames (so a moving button is not clicked mid-flight). |
| **Not covered** | After scrolling to the element, Cypress checks which element is at the click coordinates; if another element (a modal backdrop, sticky header) covers it, the action waits and eventually fails. |
| **Scrolled into view** | Cypress scrolls the element into view before the action. |

The consequence is important: you rarely need `cy.wait(...)` before an interaction. If a button becomes enabled after validation, `.click()` waits for it.

Failure messages tell you exactly which check failed, for example:

```
cy.click() failed because this element is being covered by another element:
<div class="modal-backdrop">...</div>
```

Read these messages carefully; they are among the best in test tooling.

#### 1.1 `{ force: true }`

```js
cy.get('#hidden-input').click({ force: true });
```

`force: true` **skips the actionability checks** (visibility, covered, disabled, animating) and fires the event immediately. It is useful for elements that are legitimately hidden but still functional (a visually-hidden file input or custom checkbox input), and as a *diagnostic*: if a test passes with force and fails without, you have learned that something is covering or hiding the element. But it is also a trap: a user cannot click a covered button, so a test with `force: true` can pass while the real feature is broken. Use it rarely, with a comment.

The same idea exists in Playwright (`force=True`).

### 2. Mouse interactions

#### 2.1 `.click()`

```js
cy.get('[data-test="login-button"]').click();                // centre of the element
cy.get('canvas').click(30, 50);                              // x, y offset from top-left
cy.get('.card').click('topRight');                           // named position
cy.get('li').click({ multiple: true });                      // click every matched element
cy.get('a.download').click({ ctrlKey: true });               // with a modifier key
cy.get('button').click({ force: true });                     // skip actionability
cy.get('button').click({ timeout: 10000 });                  // extend wait
```

Named positions: `'topLeft'`, `'top'`, `'topRight'`, `'left'`, `'center'` (default), `'right'`, `'bottomLeft'`, `'bottom'`, `'bottomRight'`.

Key facts:

1. `.click()` requires a **single** element unless `{ multiple: true }` is passed. If your selector matches 3 buttons, Cypress will report: "can only be called on a single element."
2. Cypress fires the full sequence of events a browser would: `pointerdown`, `mousedown`, `pointerup`, `mouseup`, `click` (and `focus` as appropriate), at the exact coordinates.
3. Clicking a link triggers navigation as normal. A link with `target="_blank"` opens a new tab, which Cypress cannot control; remove the attribute first (`cy.get('a').invoke('removeAttr', 'target').click()`) or visit the `href`.
4. `.click()` yields the same subject, so you can keep chaining.

#### 2.2 `.dblclick()` and `.rightclick()`

```js
cy.get('.editable-cell').dblclick();         // fires two click sequences and a dblclick event
cy.get('.file-row').rightclick();            // fires contextmenu event
```

`rightclick` dispatches the `contextmenu` event so your app's custom context menu appears, but the **browser's native** context menu cannot be seen or controlled.

#### 2.3 Hover

Cypress deliberately has **no `.hover()` command**, because simulating a real mouse cursor position is not reliably possible from inside the page. Options:

```js
// Option 1: trigger the events your app listens to
cy.get('.menu').trigger('mouseover');           // or 'mouseenter'

// Option 2: reveal hidden content directly (when it is CSS-only hover)
cy.get('.submenu').invoke('show');              // sets display via jQuery show()

// Option 3: skip visibility with force
cy.get('.submenu a').click({ force: true });

// Option 4: install cypress-real-events and use real browser events (Chromium-based)
cy.get('.menu').realHover();
```

Option 1 works only if the app uses JavaScript mouse events, not the CSS `:hover` pseudo-class. CSS `:hover` cannot be triggered by dispatched events; for those, use option 2, 3, or 4. The `cypress-real-events` plugin sends events through the Chrome DevTools Protocol, so it behaves like Playwright's `hover()`, but works only in Chromium-based browsers.

### 3. Typing

#### 3.1 `.type()`

```js
cy.get('[data-test="username"]').type('standard_user');
cy.get('textarea').type('Line one{enter}Line two');
cy.get('input').type('hello', { delay: 100 });         // 100 ms between keystrokes (default 10)
cy.get('input').type('password', { log: false });       // hide from the Command Log
```

**What it does:** `.type()` first **clicks** the element to focus it (unless already focused), then fires keyboard events (`keydown`, `keypress`, `beforeinput`, `input`, `keyup`) for each character. It requires a typeable element: `input`, `textarea`, `contenteditable`, or the `body`/document for global shortcuts.

**Special characters** are written inside curly braces:

| Sequence | Key |
|---|---|
| `{enter}` | Enter |
| `{esc}` | Escape |
| `{backspace}` | Backspace |
| `{del}` | Delete |
| `{selectall}` | Select all text in the field |
| `{movetostart}`, `{movetoend}` | Move cursor to start / end |
| `{leftarrow}`, `{rightarrow}`, `{uparrow}`, `{downarrow}` | Arrow keys |
| `{home}`, `{end}`, `{pageup}`, `{pagedown}` | Navigation keys |
| `{shift}`, `{ctrl}`, `{alt}`, `{meta}` | Modifier keys (held until the end of the `type` call or released by `{release}`) |
| `{{}` | A literal `{` character |

Examples:

```js
cy.get('input').type('abc{backspace}');                 // result "ab"
cy.get('input').type('{selectall}new value');          // replaces existing text
cy.get('input').type('search term{enter}');             // submits a search form
cy.get('body').type('{ctrl}k');                        // keyboard shortcut (if the app listens)
cy.get('input').type('text with {{}braces}');           // literal braces
```

If you need to type a literal string that contains `{`, either escape it with `{{}` or disable special parsing:

```js
cy.get('input').type('{"a":1}', { parseSpecialCharSequences: false });
```

**Date and time inputs** accept formatted strings:

```js
cy.get('input[type="date"]').type('2026-05-14');
cy.get('input[type="time"]').type('13:30');
```

**Empty string error:** `.type('')` throws an error. Use `.clear()` to empty a field. This is why the earlier lessons used `if (value)` guards.

#### 3.2 `.clear()`

```js
cy.get('[data-test="postal-code"]').clear();
cy.get('[data-test="postal-code"]').clear().type('90210');
```

`.clear()` is an alias for `.type('{selectall}{backspace}')`: it focuses the element, selects all, and deletes. It chains naturally into a replacement `.type()`.

#### 3.3 Setting a value quickly

When a field takes a long string and keystroke simulation is slow or triggers autocomplete you want to skip:

```js
cy.get('textarea').invoke('val', 'A very long paragraph ...').trigger('input');
```

- `.invoke('val', text)` calls jQuery's `.val(text)`, setting the DOM value.
- `.trigger('input')` fires the event frameworks (React, Vue) listen to; without it, the framework's internal state may not update, and the app behaves as if nothing was typed. This is a pragmatic shortcut, not the first choice; real typing is closer to user behaviour. Playwright's `fill()` does set values directly and triggers events for you, which is why it is often faster.

#### 3.4 Typing with autocomplete (auto-suggestions)

You studied auto-suggestions on Monday. The Cypress pattern:

```js
cy.get('[data-test="city"]').type('Lon');                     // type a partial string
cy.get('.suggestions li').should('have.length.greaterThan', 0); // wait for suggestions
cy.contains('.suggestions li', 'London').click();             // pick one
cy.get('[data-test="city"]').should('have.value', 'London');  // verify
```

Wait for the suggestions through an **assertion** (or network alias), not a sleep. If the suggestions API is slow or flaky, stub it with `cy.intercept` so the test is deterministic.

### 4. Checkboxes and radio buttons: `.check()` and `.uncheck()`

```js
cy.get('input[type="checkbox"]').check();                      // check all matched (multiple allowed)
cy.get('#terms').check();                                      // single checkbox
cy.get('#newsletter').uncheck();                               // uncheck
cy.get('input[type="radio"]').check('express');                // check the radio with value="express"
cy.get('input[type="checkbox"]').check(['news', 'offers']);    // check boxes by value
cy.get('#terms').check({ force: true });                       // if the real input is visually hidden
```

Rules:

1. `.check()` only works on `input[type=checkbox]` and `input[type=radio]`. For a styled custom control, target the *underlying input*, which may be visually hidden (needing `force: true`) or the label that toggles it (`cy.contains('label', 'Terms').click()`).
2. `.check()` is **idempotent**: if the box is already checked, nothing happens, so the test is robust to starting state.
3. `.uncheck()` works on checkboxes only (you cannot "uncheck" a radio button; select another radio instead).
4. Verify with `.should('be.checked')` or `.should('not.be.checked')`.
5. For radio groups, `.check('value')` selects the radio in the matched group with that value.

Example flow:

```js
cy.get('[type="radio"][value="express"]').check().should('be.checked');
cy.get('[type="radio"][value="standard"]').should('not.be.checked');
```

### 5. Dropdowns: `.select()`

For **native** `<select>` elements:

```js
cy.get('select').select('Price (low to high)');      // by visible text
cy.get('select').select('lohi');                     // by value attribute
cy.get('select').select(2);                          // by zero-based index
cy.get('select').should('have.value', 'lohi');       // verify the selected value
cy.get('select[multiple]').select(['apple', 'banana']); // multi-select, by text or value
```

Notes:

1. `.select()` works **only on `<select>`**. Its argument is matched first against the option's value, then its text, or the index if a number.
2. For multi-selects, pass an array. Selecting again adds/replaces according to browser behaviour; to reset, `.invoke('val', [])` then `.trigger('change')` is a pragmatic approach.
3. Verifying a multi-select: `cy.get('select[multiple]').invoke('val').should('deep.equal', ['apple', 'banana'])`.
4. The selected option text can be asserted with `cy.get('select option:selected').should('have.text', 'Apple')`.

For **custom dropdowns** (built with `div`/`ul`, as most UI libraries do), `.select()` will fail with "cy.select() can only be called on a `<select>`". Treat them as ordinary elements:

```js
cy.get('[data-test="country-dropdown"]').click();           // open
cy.contains('[role="option"]', 'Canada').click();           // choose
cy.get('[data-test="country-dropdown"]').should('contain.text', 'Canada');
```

(Monday's Playwright dropdown lesson made the same distinction between `select_option` for native selects and click-based approaches for custom ones.)

### 6. Focus, blur, submit

```js
cy.get('input#email').focus().should('have.focus');
cy.get('input#email').blur();
cy.get('form').submit();     // submits a form element (must be a <form>)
```

- `.focus()` and `.blur()` are used to trigger validation that fires on blur.
- `.submit()` bypasses the submit button; prefer clicking the real button or typing `{enter}` in an input, because that mimics a user.

### 7. Scrolling

```js
cy.get('footer').scrollIntoView();                               // bring element into the viewport
cy.scrollTo('bottom');                                           // scroll the window
cy.get('.list').scrollTo(0, 500);                                // scroll an element by x,y pixels
cy.get('.list').scrollTo('bottom', { duration: 500 });           // animated
```

Cypress scrolls to elements automatically before actions, so you rarely need `scrollIntoView` for clicking. It is helpful for **lazy-loaded (infinite scroll)** pages: scroll to the bottom, then assert that more items appear.

### 8. `.trigger()`: custom DOM events

```js
cy.get('.slider').trigger('mousedown', { which: 1 })
                 .trigger('mousemove', { clientX: 200 })
                 .trigger('mouseup');

cy.get('.item').trigger('dragstart');
cy.get('.zone').trigger('drop');
```

`.trigger(eventName, options)` dispatches any DOM event. It also performs actionability checks. This is a low-level tool, useful for:

- Sliders, range inputs, canvases.
- Hover events (`mouseover`, `mouseenter`) on JavaScript-driven menus.
- HTML5 drag-and-drop, where you must dispatch `dragstart`, `dragenter`, `dragover`, `drop`, and `dragend` with a `dataTransfer` object:

```js
const dataTransfer = new DataTransfer();
cy.get('#draggable').trigger('dragstart', { dataTransfer });
cy.get('#dropzone').trigger('dragover', { dataTransfer }).trigger('drop', { dataTransfer });
cy.get('#draggable').trigger('dragend');
```

Libraries like `@4tw/cypress-drag-drop` wrap this in `.drag('#target')`. Playwright's `drag_to` handles many cases in one call; in Cypress, expect to spend more time on drag-and-drop.

### 9. Alerts, confirms, and prompts

When the application calls `window.alert`, `window.confirm`, or `window.prompt`, Cypress **automatically accepts** alerts and confirms (clicks OK) so tests do not hang, and it fires events you can listen to:

```js
it('shows an alert message', () => {
  const alertStub = cy.stub().as('alertStub');
  cy.on('window:alert', alertStub);              // capture the alert
  cy.get('#alert-button').click();
  cy.get('@alertStub').should('have.been.calledOnceWith', 'I am a JS Alert');
});

it('cancels a confirm dialog', () => {
  cy.on('window:confirm', () => false);          // return false = click Cancel
  cy.get('#confirm-button').click();
  cy.get('#result').should('have.text', 'You clicked: Cancel');
});

it('answers a prompt', () => {
  cy.window().then((win) => cy.stub(win, 'prompt').returns('Ada'));
  cy.get('#prompt-button').click();
  cy.get('#result').should('contain.text', 'Ada');
});
```

**Explanation:**

1. `cy.stub()` creates a Sinon stub (a fake function that records calls); `.as('alertStub')` aliases it for later assertions.
2. `cy.on('window:alert', handler)` registers an event listener on Cypress's event bus; it fires with the alert text as an argument.
3. For confirm, the **return value** of the listener decides the user's choice: `false` cancels; returning nothing or `true` accepts.
4. `window.prompt` has no Cypress event, so stub the function on the `window` object and `.returns()` the text. Stubbing must happen **before** the click (or use `onBeforeLoad` in `cy.visit` if the page uses the dialog on load).

Contrast with Playwright: you register `page.on("dialog", lambda d: d.accept())` and *you* must accept or dismiss, otherwise the action hangs. In Cypress, the default is auto-accept; you override only when testing the cancel path.

Authentication pop-ups (`http://user:pass@host`) use `cy.visit(url, { auth: { username, password } })`.

### 10. File upload: `.selectFile()`

```js
cy.get('input[type="file"]').selectFile('cypress/fixtures/report.pdf');
cy.get('input[type="file"]').selectFile(['file1.png', 'file2.png']);        // multiple files
cy.get('input[type="file"]').selectFile({
  contents: Cypress.Buffer.from('file contents'),
  fileName: 'notes.txt',
  mimeType: 'text/plain',
  lastModified: Date.now(),
});
cy.get('.dropzone').selectFile('cypress/fixtures/report.pdf', { action: 'drag-drop' });
cy.get('input[type="file"]').selectFile('cypress/fixtures/report.pdf', { force: true });
```

- Paths are relative to the project root.
- Passing an object with `contents` creates a file on the fly, so you do not need a fixture file.
- `{ action: 'drag-drop' }` simulates dropping the file on a drop zone; default `'select'` attaches it to an input.
- For downloads, configure `downloadsFolder`, click the link, then `cy.readFile('cypress/downloads/report.pdf')` to verify; `cy.readFile` retries until the file exists.

### 11. Interaction best practices: acting like a user

1. **Interact with what the user sees.** Click the visible button or label, not hidden internals.
2. **Do not force unless necessary.** Treat `force: true` as a code smell requiring a comment.
3. **Assert after interactions.** Each action should be followed by an assertion on its outcome, so failures point to the right step.
4. **Wait for the app, not the clock.** After typing, wait on a rendered state (`should`) or an intercept alias.
5. **Be deterministic.** Stub unreliable third-party services.
6. **Interact with a single element.** Narrow the selector.
7. **Prefer the real event path.** `.type('{enter}')` in the field is closer to the user than `.submit()`.

---

## Code Examples

### Example 1: A full checkout form interaction

```js
describe('Checkout information form', () => {
  beforeEach(() => {
    cy.login();                                  // custom command with cy.session
    cy.visit('/inventory.html');
    cy.get('[data-test="add-to-cart-sauce-labs-backpack"]').click();
    cy.get('[data-test="shopping-cart-link"]').click();
    cy.get('[data-test="checkout"]').click();
  });

  it('fills the form and continues', () => {
    cy.get('[data-test="firstName"]').type('Ada');
    cy.get('[data-test="lastName"]').type('Lovelace');
    cy.get('[data-test="postalCode"]').type('12345');
    cy.get('[data-test="continue"]').click();
    cy.url().should('include', '/checkout-step-two.html');
    cy.get('[data-test="inventory-item-name"]').should('have.text', 'Sauce Labs Backpack');
  });

  it('shows an error when the first name is missing', () => {
    cy.get('[data-test="lastName"]').type('Lovelace');
    cy.get('[data-test="postalCode"]').type('12345');
    cy.get('[data-test="continue"]').click();
    cy.get('[data-test="error"]').should('contain.text', 'First Name is required');
  });

  it('can clear and retype a field', () => {
    cy.get('[data-test="firstName"]').type('Wrong').clear().type('Ada');
    cy.get('[data-test="firstName"]').should('have.value', 'Ada');
  });
});
```

**Explanation:**

- `beforeEach` uses a login command, adds an item, opens the cart, and begins checkout, so each test starts at the form.
- `type` fills each field; the `data-test` attributes on this practice site (`firstName`, `lastName`, `postalCode`, `continue`, `checkout`) are stable hooks.
- Test 1 asserts navigation and that the right product appears in the summary.
- Test 2 omits a field and asserts the validation message.
- Test 3 chains `.type().clear().type()` and then asserts the final value with `have.value`.

### Example 2: Sorting dropdown and verifying order

```js
it('sorts by price high to low', () => {
  cy.login();
  cy.visit('/inventory.html');
  cy.get('[data-test="product-sort-container"]').select('Price (high to low)');
  cy.get('[data-test="product-sort-container"]').should('have.value', 'hilo');
  cy.get('[data-test="inventory-item-price"]').first().should('have.text', '$49.99');
});
```

**Explanation:** `.select('Price (high to low)')` chooses by visible text; `have.value` verifies the underlying value `hilo`; the first price should be the most expensive one (`$49.99` on this demo site; adjust if the data differs).

### Example 3: Checkboxes and radios on a practice page

```js
it('handles form controls', () => {
  cy.visit('https://example.cypress.io/commands/actions');
  cy.get('.action-checkboxes [type="checkbox"]').not('[disabled]').check().should('be.checked');
  cy.get('.action-radios [type="radio"]').not('[disabled]').check('radio1').should('be.checked');
  cy.get('.action-select').select('apples').should('have.value', 'fr-apples');
  cy.get('.action-select-multiple').select(['apples', 'oranges']);
});
```

**Explanation:** `.not('[disabled]')` filters out disabled inputs so `check()` does not error; `.check('radio1')` picks the radio with that value; `.select('apples')` matches by visible text and the resulting `value` is `fr-apples` on that page; the multi-select takes an array. (Cypress's kitchen-sink site is designed for practising these commands.)

### Example 4: Dialogs

```js
it('handles alert, confirm and prompt', () => {
  cy.visit('https://the-internet.herokuapp.com/javascript_alerts');

  // alert
  const onAlert = cy.stub().as('onAlert');
  cy.on('window:alert', onAlert);
  cy.contains('button', 'Click for JS Alert').click();
  cy.get('@onAlert').should('have.been.calledWith', 'I am a JS Alert');
  cy.get('#result').should('have.text', 'You successfully clicked an alert');

  // confirm: cancel
  cy.on('window:confirm', () => false);
  cy.contains('button', 'Click for JS Confirm').click();
  cy.get('#result').should('have.text', 'You clicked: Cancel');

  // prompt
  cy.window().then((win) => cy.stub(win, 'prompt').returns('Cypress'));
  cy.contains('button', 'Click for JS Prompt').click();
  cy.get('#result').should('have.text', 'You entered: Cypress');
});
```

**Explanation:** The same page you may have used on Monday for Playwright dialogs. `cy.on` listeners stay active until the end of the test. The prompt is stubbed because no event exists for it.

---

## Real-World Scenarios

1. **Sticky header covers a button.** A test fails with "element is being covered by another element: `<header class="sticky">`". Rather than `{ force: true }`, the team fixes the test with `.scrollIntoView({ offset: { top: -100, left: 0 } })` and, separately, files a UX bug since real users have the same problem.
2. **Hover menu.** A navigation menu opens on CSS `:hover`. `trigger('mouseover')` does nothing because there is no JavaScript. The team installs `cypress-real-events` and uses `realHover()`, restricting those tests to Chromium browsers via `{ browser: '!firefox' }`.
3. **Date picker.** For native date inputs, `.type('2026-05-14')` is enough. For a custom calendar widget, the team clicks the field, selects month and day cells by text within the calendar container (as in Tuesday's date pickers lesson).
4. **Fast form fill in bulk tests.** A 40-field insurance form is filled in every test; the team uses `invoke('val').trigger('input')` through a custom command for the fields not under test, and `.type` for the field being verified.
5. **File upload validation.** Tests upload a PDF, an oversized file, and a `.exe`; each time, `selectFile` plus an assertion on the displayed message verify server-side rules.

---

## Common Pitfalls and Best Practices

**Pitfall 1: Multiple matches.** `.click()` on a selector that matches several elements fails. Narrow the selector or use `{ multiple: true }` intentionally.

**Pitfall 2: Using `.type('')`.** Throws. Use `.clear()`.

**Pitfall 3: Expecting `.select()` to work on custom dropdowns.** It works only on `<select>`.

**Pitfall 4: Overusing `force: true`.** It hides real usability bugs.

**Pitfall 5: Expecting `.hover()`.** It does not exist; choose the right alternative for your app.

**Pitfall 6: Setting values with `.invoke('val')` without triggering events.** Frameworks may not notice. Follow with `.trigger('input')` or `.trigger('change')`.

**Pitfall 7: Dialog listener registered too late.** Register `cy.on('window:alert', ...)` before the click that opens the alert.

**Pitfall 8: Targeting the wrong element for checkboxes.** If `.check()` says the element is not visible, find the actual input or click the label.

**Pitfall 9: Typing special characters.** `{` triggers special parsing; escape or disable.

**Pitfall 10: Ignoring detach errors.** If the app re-renders between query and action, Cypress 12+ re-queries automatically for chained queries; if you used `.then($el)` and then `cy.wrap($el).click()`, the element may be stale. Re-query instead.

**Best practices**

- Always follow an interaction with an assertion.
- Prefer visible user paths over shortcuts.
- Wrap repeated interaction sequences in custom commands.
- Stub dialogs and third-party widgets for determinism.
- Comment every `force: true`.
- Keep interactions inside `data-test` driven selectors.

---

## Mini Practice Exercises

**Exercise 1 - Actionability.**
Write a test against `https://example.cypress.io/commands/actions` that clicks a button that is covered or disabled (inspect the page) and read the failure message. Then fix it properly.

**Exercise 2 - Type with specials.**
Type `"Hello World"` into the `.action-email` field, use `{backspace}` five times to remove "World", and assert the value is `Hello `. *Hint:* `.type('Hello World{backspace}{backspace}{backspace}{backspace}{backspace}')`.

**Exercise 3 - Radio and checkbox.**
On Sauce Demo, there are none; use the kitchen-sink page. Check two checkboxes by value, then uncheck one, and assert states.

**Exercise 4 - Select.**
Sort Sauce Demo products by name Z to A and assert the first product is "Test.allTheThings() T-Shirt (Red)".

*Solution:*

```js
cy.get('[data-test="product-sort-container"]').select('Name (Z to A)');
cy.get('[data-test="inventory-item-name"]').first().should('have.text', 'Test.allTheThings() T-Shirt (Red)');
```

**Exercise 5 - Dialogs.**
Using `the-internet.herokuapp.com/javascript_alerts`, write three tests (alert, confirm accept, confirm cancel) and verify the result text each time.

**Exercise 6 - Upload.**
Create a text file fixture, upload it to `https://the-internet.herokuapp.com/upload`, click Upload, and assert that the page shows the file name.

**Exercise 7 - Compare.**
Choose three interactions from your Project 1 Playwright tests (for example fill, select, dialog). Write the Cypress equivalent and list one behavioural difference you notice for each.

---

## Summary / Key Takeaways

- Cypress performs **actionability checks** (exists, not detached, visible, enabled, not animating, not covered, scrolled into view) and waits for them before actions, which removes most explicit waits.
- Core actions: `.click()`, `.dblclick()`, `.rightclick()`, `.type()`, `.clear()`, `.check()`, `.uncheck()`, `.select()`, `.focus()`, `.blur()`, `.scrollIntoView()`, `.scrollTo()`, `.trigger()`, `.selectFile()`.
- `.type()` supports special sequences in braces (`{enter}`, `{selectall}`, `{backspace}`, modifiers) and cannot take an empty string.
- `.select()` is for native `<select>` only; custom dropdowns are clicked like any other element.
- There is no `.hover()`; use `.trigger()`, `invoke('show')`, or `cypress-real-events`.
- Alerts and confirms are auto-accepted; listen with `cy.on('window:alert' / 'window:confirm')`; stub `window.prompt`.
- `{ force: true }` skips checks; use sparingly and comment why.
- Compared with Playwright, Cypress interactions are event-simulated and have no `fill()`; expect more manual work with hover, drag-and-drop, and multi-tab flows.
- Using the Command Log and snapshots to see what each interaction did is introduced in the **next lesson**; the full time-travel deep dive is **covered on Friday**.

---

## External Resources

- Cypress Documentation - Interacting with Elements (actionability): https://docs.cypress.io/app/core-concepts/interacting-with-elements
- Cypress Documentation - `.type()`: https://docs.cypress.io/api/commands/type
- Cypress Documentation - `.selectFile()`: https://docs.cypress.io/api/commands/selectfile
