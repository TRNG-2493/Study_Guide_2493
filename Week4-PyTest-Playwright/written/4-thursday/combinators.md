# CSS Combinators

## Learning Objectives

By the end of this lesson you will be able to:

- Define a combinator and name the four CSS combinators: descendant (space), child (`>`), adjacent sibling (`+`), and general sibling (`~`).
- Read a selector as a path through the DOM family tree (parent, child, ancestor, descendant, sibling).
- Pick the right combinator for tasks such as "the button inside this row" or "the error message right after this input".
- Chain combinators with classes, attributes, and pseudo-classes to anchor a locator to a stable parent.
- Understand scoping in Playwright: chaining `locator()` calls and how it relates to combinators.
- Avoid over-long, brittle selector chains.

## Why This Matters

Real pages repeat the same widgets many times: ten "Add to cart" buttons, twenty "Delete" icons, a table full of "Edit" links. A selector like `button.add` matches all of them. The question a tester must answer is *which one?* Usually the answer is relational: "the Add button **inside** the Backpack card", or "the error message **after** the email field".

Combinators are how CSS expresses relationships. They let you anchor on something stable and unique (a product name, a row title) and walk to the element you really want. This supports the weekly epic: manual test steps such as "delete the user named Alice" become repeatable automation that does not break when Alice moves to a different row. For Project 1: QE Foundations, this is how you will target the right button in lists and tables.

You should already be comfortable with the basic, attribute, and pseudo-class selectors from earlier today.

---

## The Concept

### 1. The DOM Family Tree (Vocabulary)

Consider this HTML:

```html
<div class="card" id="card-1">
  <h2>Backpack</h2>
  <p class="price">$29.99</p>
  <div class="actions">
    <button class="add">Add</button>
    <button class="info">Info</button>
  </div>
</div>
```

| Term | Example in the above |
|------|----------------------|
| **Parent** | `.card` is the parent of `h2`, `p`, and `.actions` |
| **Child** | `h2`, `p`, `.actions` are children of `.card` |
| **Ancestor** | `.card` is an ancestor of `button.add` (grandparent, great-grandparent...) |
| **Descendant** | `button.add` is a descendant of `.card` (child, grandchild...) |
| **Sibling** | `h2` and `p` share a parent, so they are siblings |
| **Adjacent sibling** | `p.price` immediately follows `h2` (no element in between) |

A **combinator** is a symbol placed between two selectors that states how the elements matched by them are related.

```
selectorA  <combinator>  selectorB
```

The *subject* of the whole selector is always the **right-most** part. In `.card button`, the returned elements are the buttons, not the cards. The left parts are only filters ("context").

### 2. Descendant Combinator (a single space)

```css
.card button
```

Matches any `button` that is **anywhere inside** an element with class `card`, at any depth.

In the sample, `.card button` matches both `button.add` and `button.info`, even though they are two levels deep (card > actions > button).

- **Strength:** flexible; it survives wrappers being added (like a new `div` for layout).
- **Weakness:** it may match *more* than you expect, including elements in nested components.

Whitespace is meaningful. `.card button` (descendant) is not the same as `.card.button` (one element with both classes).

### 3. Child Combinator (`>`)

```css
.card > p
.card > .actions > button
```

Matches only **direct children** (one level down).

- `.card > p` matches the price paragraph, which is directly under `.card`.
- `.card > button` would match nothing, since buttons are grandchildren.
- `.card > .actions > button` matches both buttons by listing every level.

Spaces around `>` are optional (`.card>p`), but readable code uses them.

- **Strength:** precise; ignores deeply nested look-alikes.
- **Weakness:** brittle against wrappers. If a developer inserts another `div` between, your selector breaks. Use `>` when direct parentage is the real meaning (menus, `ul > li`), and the space when you just need "somewhere inside".

### 4. Adjacent Sibling Combinator (`+`)

```css
h2 + p
```

Matches a `p` that **immediately follows** an `h2` and shares the same parent. "Immediately" means no other *element* between them (text nodes do not count). Only one element can match per `h2`: the very next one.

A classic use is form validation messages:

```html
<label for="email">Email</label>
<input id="email" type="email">
<span class="error">Please enter a valid email</span>
```

```css
#email + .error      /* the error message right after the email input */
```

### 5. General Sibling Combinator (`~`)

```css
h2 ~ button
```

Matches any `button` that **comes later** among the same parent's children (not necessarily immediately). Both siblings must share the same parent, and the target must appear **after** the first in document order. CSS cannot look backward.

```html
<div class="row">
  <input id="a">
  <span>hint</span>
  <span class="error">Bad</span>
</div>
```

```css
#a ~ .error     /* matches, even though 'hint' sits between */
#a + .error     /* does NOT match, as .error is not immediately after */
```

### 6. Summary Table

| Combinator | Symbol | Reads as | Example | Matches |
|------------|--------|----------|---------|---------|
| Descendant | (space) | "inside, any depth" | `form input` | all inputs in the form |
| Child | `>` | "direct child of" | `ul > li` | list items directly under ul |
| Adjacent sibling | `+` | "immediately after" | `label + input` | input right after a label |
| General sibling | `~` | "somewhere after, same parent" | `h2 ~ p` | all later p siblings |

### 7. Combining with Everything Else

Combinators work with any simple selector, pseudo-class, or attribute:

```css
form#login > div.field > input[type="password"]
ul.menu > li:not(.disabled) > a
table#results tbody tr:nth-child(2) > td:last-child
.card:has(h2) button.add
```

You can chain as many as needed, but see "Strategy" below: the shorter the better.

### 8. Anchoring Strategy: Stable Anchor, Short Path

A robust relational locator has two parts:

1. **An anchor**: something unique and stable (a `data-test`, a specific text, an id).
2. **A short path** from the anchor to the target.

```css
[data-test="product-backpack"] button.add
```

Here the anchor is `data-test="product-backpack"`, and the path is "any `button.add` inside it".

Avoid the opposite, the **absolute path** that DevTools can copy for you:

```css
body > div:nth-child(2) > div > div:nth-child(1) > ul > li:nth-child(3) > button
```

It starts from `body`, depends on positions, and will break at the first layout change.

### 9. Going "Up": Combinators Cannot, `:has()` Can

CSS combinators move **down** (parent to child) and **forward** (previous to next sibling). They cannot go to a parent or a previous sibling. To say "the row that contains Alice", use `:has()` from the pseudo-class lesson:

```css
tr:has(td:text-is("Alice")) button.delete       /* Playwright; uses :text-is */
tr:has(td[data-name="Alice"]) button.delete     /* standard CSS */
```

Read it as: "find a `tr` that has a cell for Alice; then, inside that row, the delete button."

### 10. Combinators vs. Chained Locators in Playwright

Playwright lets you build the same relationship by **chaining** `locator()` calls, where each call searches *inside* the previous one:

```python
page.locator(".card").locator("button.add")
# similar in meaning to
page.locator(".card button.add")
```

Chaining is usually preferred in longer code because each step has a name, can be reused (`card = page.locator(".card")`), and can be narrowed with `filter()` (Friday's lesson). Understanding combinators remains vital because (a) you will read existing selector strings, (b) you will use them in DevTools, (c) they are the right tool for compact single-string locators.

One subtle difference: `page.locator(".card").locator("> button")` is allowed in Playwright for direct child; and a plain CSS string cannot start with a combinator elsewhere. That is an advanced detail; we will revisit chaining on Friday.

---

## Code Examples

We use this page. Save as `combinators.html`.

```html
<!DOCTYPE html>
<html lang="en">
<head><meta charset="UTF-8"><title>Combinators Practice</title></head>
<body>
  <div class="card" data-test="card-backpack">
    <h2>Backpack</h2>
    <p class="price">$29.99</p>
    <div class="actions">
      <button class="add">Add</button>
      <button class="info">Info</button>
    </div>
  </div>

  <div class="card" data-test="card-light">
    <h2>Bike Light</h2>
    <p class="price">$9.99</p>
    <div class="actions">
      <button class="add">Add</button>
      <button class="info">Info</button>
    </div>
  </div>

  <form id="signup">
    <div class="field">
      <label for="email">Email</label>
      <input id="email" type="email">
      <span class="hint">We never share it</span>
      <span class="error">Invalid email</span>
    </div>
  </form>

  <ul class="menu">
    <li><a href="/home">Home</a></li>
    <li>
      <a href="/products">Products</a>
      <ul class="submenu">
        <li><a href="/products/bags">Bags</a></li>
        <li><a href="/products/lights">Lights</a></li>
      </ul>
    </li>
    <li><a href="/about">About</a></li>
  </ul>

  <table id="users">
    <tbody>
      <tr><td>Alice</td><td>admin</td><td><button class="delete">Delete</button></td></tr>
      <tr><td>Bob</td><td>user</td><td><button class="delete">Delete</button></td></tr>
    </tbody>
  </table>
</body>
</html>
```

### Example 1: Predict and test in DevTools

```js
$$('.card button').length                  // 4  (descendant)
$$('.card > button').length                // 0  (buttons are grandchildren)
$$('.card > .actions > button.add').length // 2
$$('h2 + p').map(p => p.textContent)       // ["$29.99","$9.99"]
$$('#email + .error').length               // 0  (hint sits between)
$$('#email ~ .error').length               // 1
$$('.menu > li').length                    // 3  (top level only)
$$('.menu li').length                      // 5  (includes submenu items)
$$('.menu > li > a').length                // 3
```

**Explanation of the interesting ones:**

- `.menu li` is 5: Home, Products, About, plus Bags and Lights nested in the submenu. The descendant combinator reaches any depth.
- `.menu > li` is 3 because only direct children count.
- `#email + .error` is 0 because `.hint` is the element immediately after the input; `~` skips over it.

### Example 2: Playwright with combinators

```python
from pathlib import Path
from playwright.sync_api import sync_playwright

url = Path("combinators.html").resolve().as_uri()

with sync_playwright() as p:
    browser = p.chromium.launch()
    page = browser.new_page()
    page.goto(url)

    # 1. The price of the Bike Light card: anchor on data-test, then walk to .price
    price = page.locator('[data-test="card-light"] > .price').inner_text()
    print("Bike light price:", price)                       # $9.99

    # 2. The Info button of the Backpack card only
    info_btn = page.locator('[data-test="card-backpack"] button.info')
    print("Info buttons found:", info_btn.count())          # 1

    # 3. Sibling relationship: error message after email
    err = page.locator("#email ~ .error")
    print("Error text:", err.inner_text())                  # Invalid email (hidden? see note)

    # 4. Top-level menu entries only
    top = page.locator(".menu > li > a").all_inner_texts()
    print("Top menu:", top)                                 # ['Home', 'Products', 'About']

    # 5. The delete button in Bob's row (has + descendant)
    bob_delete = page.locator("#users tr:has(td:first-child:text-is('Bob')) button.delete")
    print("Bob delete buttons:", bob_delete.count())        # 1

    browser.close()
```

**Line-by-line:**

1. `'[data-test="card-light"] > .price'`: starts at a unique anchor, then uses `>` because `.price` is a direct child of the card. The Python string uses single quotes outside so the double quotes inside the attribute selector need no escaping.
2. `'[data-test="card-backpack"] button.info'`: the descendant space, since the button is two levels deep. It returns 1 because only the Backpack card is inside the anchor.
3. `#email ~ .error`: general sibling. `.inner_text()` works here because the span is displayed by default (in a real page it might be hidden until validation fails, and `inner_text()` would then wait/time out; we will study that on Friday).
4. `.menu > li > a`: only the three top-level anchors; the submenu links are excluded because their `li` is not a direct child of `.menu`. `.all_inner_texts()` returns the list.
5. The row anchor: `tr:has(td:first-child:text-is('Bob'))` selects the row whose first cell is exactly Bob; then ` button.delete` finds the button inside it. Note the single quotes inside a double-quoted Python string. This uses Playwright's `:text-is()` extension, so it will not run in DevTools.

### Example 3: A reusable helper function

```python
def delete_button_for(page, user_name: str):
    """Return a locator for the Delete button in the row of the given user."""
    return page.locator(
        f"#users tr:has(td:first-child:text-is('{user_name}')) button.delete"
    )

# Usage inside a test
delete_button_for(page, "Alice").click()
```

**Explanation:** `f"...{user_name}..."` is a Python f-string that inserts the argument into the selector. Wrapping the pattern in a function gives the tests a descriptive vocabulary (`delete_button_for(page, "Alice")`) and keeps the fragile selector string in one place. If the table markup changes, you fix it once. (This is the seed of the Page Object pattern you will meet later in the programme; for now, think of it as a helper.)

**Caution:** if `user_name` can contain a single quote (e.g. `O'Brien`), the selector breaks. In production code, use Playwright's filter-based approach (Friday).

---

## Real-World Scenarios

1. **Shopping list.** In an e-commerce site, each product card has an identical "Add to cart" button. The tester anchors on the product's `data-test` or name and uses a descendant combinator to reach the right button.
2. **Admin tables.** "Delete the user Bob" becomes `tr:has(...) button.delete`. The test remains valid when users are sorted or paginated.
3. **Form errors.** An `input + .error` or `input ~ .error` pattern asserts that the validation message belongs to the right field, rather than any error anywhere on the page.
4. **Navigation menus.** `.menu > li > a` verifies only the top-level entries; `.submenu a` verifies the dropdown links. Without `>`, a test for "3 top-level items" would count 5.
5. **Dropdown components.** A select widget renders options in a separate container at the end of `body`. A relational selector from the trigger will not reach it; you instead anchor on the options container. Knowing the DOM structure (via DevTools) tells you which approach works.

---

## Common Mistakes

1. **Believing the first part is returned.** `.card button` returns buttons, not cards.
2. **Using `>` when there are wrapper elements.** It matches nothing, and you waste time wondering why.
3. **Using a space when `>` is intended.** `.menu li` also catches nested submenu items.
4. **Using `+` where `~` is needed** (or vice versa). `+` needs *immediate* adjacency.
5. **Trying to go up or backward.** `.error - input` or "parent of" does not exist; use `:has()`.
6. **Long absolute chains from `body`.** Fragile, hard to read.
7. **Forgetting that combinators work on elements, not text nodes.** Plain text between two tags does not break adjacency.
8. **Ignoring quotes in f-strings.** Mixed quotes and special characters in names cause syntax errors.
9. **Assuming identical markup everywhere.** A sibling-based selector that works in the login form may fail in the registration form if the order differs.

---

## Practice Exercises

Use `combinators.html`.

**Exercise 1.** Write a selector for the "Add" button inside the Bike Light card, anchored on its data-test. *Solution:* `[data-test="card-light"] button.add`.

**Exercise 2.** Predict the counts.

| Selector | Count |
|----------|-------|
| `.card h2` | ? |
| `.card > h2` | ? |
| `.actions > button` | ? |
| `.submenu > li` | ? |
| `ul ul a` | ? |

*Solutions:* 2; 2; 4; 2; 2.

**Exercise 3.** Select "the submenu links under Products only" in two different ways. *Solutions:* `.submenu a` and `.menu > li > .submenu > li > a`. Which is more robust? (The first: shorter, less coupled to structure.)

**Exercise 4.** Using a sibling combinator, select the hint span next to the email input, and then the error span. *Solutions:* `#email + .hint`, `#email + .hint + .error` (or `#email ~ .error`).

**Exercise 5.** Select the price for the Backpack card using the child combinator, and again using `:has()` anchored on the heading text (Playwright). *Solutions:* `[data-test="card-backpack"] > .price`; `.card:has(h2:text-is("Backpack")) > .price`.

**Exercise 6.** Write `click_delete(page, name)` that clicks the delete button of a user and prints how many rows remain (use `page.locator("#users tbody tr").count()`). Run it for Alice. Expected: after the click nothing is removed (the demo has no JS), so the count stays 2. Explain why. *Answer:* the page has no behaviour attached to the button; locators only find elements, they do not guarantee application behaviour.

**Exercise 7 (challenge).** On https://www.saucedemo.com (log in with `standard_user` / `secret_sauce`), write one selector that finds the "Add to cart" button for the "Sauce Labs Backpack" product. *Hint:* in DevTools, find the container of the item (a class such as `inventory_item`), and use `:has()` with the product name. Verify "1 of 1".

---

## Summary

- A **combinator** states the relationship between two selectors; the right-most part is the element you get.
- **Descendant** (space): any depth. **Child** (`>`): direct children. **Adjacent sibling** (`+`): immediate next sibling. **General sibling** (`~`): any later sibling with the same parent.
- Combinators move down and forward only; use `:has()` to reason about parents.
- A good locator has a **stable anchor** and a **short path**; avoid absolute `body > div > div...` chains.
- Playwright's chaining (`locator(...).locator(...)`) expresses the same ideas step by step; we deepen this on Friday.
- Next: *Dynamic selectors*, where IDs and classes change between runs and we must adapt.

---

## Additional Resources

- MDN, Combinators: https://developer.mozilla.org/en-US/docs/Web/CSS/CSS_selectors/Selectors_and_combinators
- W3C Selectors Level 4, Combinators: https://www.w3.org/TR/selectors-4/#combinators
- Playwright Python, Other locators: https://playwright.dev/python/docs/other-locators
