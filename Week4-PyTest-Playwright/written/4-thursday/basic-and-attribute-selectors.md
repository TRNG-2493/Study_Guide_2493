# Basic and Attribute Selectors

## Learning Objectives

By the end of this lesson you will be able to:

- Write type (tag), ID, class, and universal selectors.
- Combine selectors to target elements precisely (compound selectors).
- Use attribute selectors in all common forms: presence, exact match, contains, starts-with, ends-with, whitespace-separated word, and case-insensitive matching.
- Group selectors with commas.
- Choose the best attribute for a locator (`data-test`, `id`, `name`, `type`, `aria-label`, etc.).
- Validate selectors in DevTools and use them in Playwright Python with `page.locator()`.

## Why This Matters

Our weekly epic is turning manual test design into automation. A manual tester says "click the Log in button". An automated test must say it in a language the browser understands. The selectors you learn here are the sentences of that language. About 80% of the locators you will write for Project 1 come from the ideas in this one lesson: a tag, an id, a class, or an attribute.

Yesterday you learned how to make PyTest tests organised and data-driven. Now you will learn how to point those tests at a real page. In the exercise this afternoon, your pair will build a **locator catalog**: a table listing every important element of a practice site with a verified selector. Mastery of this lesson is what makes that catalog fast and correct.

If you have not yet read *CSS fundamentals* from earlier today, read it first: it explains the DOM, the notion that a selector returns a list, and how to test selectors in DevTools.

---

## The Concept

We will use this HTML throughout the lesson. Save it as `shop.html` and open it in Chrome so you can test every selector as you read.

```html
<!DOCTYPE html>
<html lang="en">
<head><meta charset="UTF-8"><title>Shop Demo</title></head>
<body>
  <header id="top-bar" class="bar">
    <a href="/home" class="logo">ShopDemo</a>
    <a href="/cart" class="cart-link" aria-label="Shopping cart">Cart</a>
  </header>

  <form id="login-form" class="form card" action="#">
    <input id="username" name="user-name" type="text" placeholder="Username" data-test="username" required>
    <input id="password" name="password" type="password" placeholder="Password" data-test="password" required>
    <input type="checkbox" id="remember" name="remember" checked>
    <button id="login-button" class="btn btn-primary large" type="submit" data-test="login-button">Log in</button>
    <button class="btn btn-secondary" type="reset" disabled>Reset</button>
  </form>

  <section class="products">
    <div class="product" data-sku="BP-001" data-test="product-backpack">
      <h2 class="product-name">Sauce Labs Backpack</h2>
      <a href="/img/backpack.png" class="product-image">View image</a>
      <a href="https://example.com/spec.pdf" class="doc-link">Spec sheet</a>
      <button class="btn add" data-test="add-backpack">Add to cart</button>
    </div>
    <div class="product" data-sku="BL-002" data-test="product-bike-light">
      <h2 class="product-name">Sauce Labs Bike Light</h2>
      <a href="/img/light.jpg" class="product-image">View image</a>
      <a href="https://example.com/light.pdf" class="doc-link">Spec sheet</a>
      <button class="btn add" data-test="add-bike-light">Add to cart</button>
    </div>
  </section>
</body>
</html>
```

### Part 1: Basic Selectors

#### 1.1 Type selector (tag name)

Matches every element with that tag name. No prefix symbol.

```css
button      /* all 4 buttons: login, reset, and the two "Add to cart" buttons */
h2          /* both product names */
a           /* every link (6 in this page) */
```

**When to use:** rarely alone, because pages have many of the same tags. Excellent as part of a compound selector (`button.add`) or to state intent (`input[type="password"]`).

#### 1.2 ID selector: `#`

Matches the element whose `id` attribute equals the value.

```css
#login-button
#username
#top-bar
```

IDs are *supposed* to be unique per page, so an ID selector is usually the strongest and fastest locator. But beware:

- Some frameworks generate IDs dynamically (`id="input-84721"`), which change on every load. These are useless as locators (see *Dynamic selectors*).
- If an ID contains special characters (e.g. a colon in `id="user:name"`), you must escape them: `#user\:name`. Using `[id="user:name"]` is easier.
- An ID that begins with a digit must also be escaped (`#\31 23`). Again `[id="123"]` is simpler.

#### 1.3 Class selector: `.`

Matches elements that include that class in their `class` attribute. An element can have many classes, separated by spaces.

```css
.btn            /* login, reset, 2 add buttons */
.btn-primary    /* login button only */
.product        /* the two product divs */
.large          /* login button only */
```

The login button has `class="btn btn-primary large"`. Each of `.btn`, `.btn-primary`, and `.large` matches it independently.

**Multiple classes on one element (no space):**

```css
.btn.btn-primary        /* an element with BOTH btn and btn-primary */
button.btn.large        /* a <button> with both classes */
```

**Space means something else.** `.card .btn` means "any `.btn` *inside* a `.card`". Do not add accidental spaces.

#### 1.4 Universal selector: `*`

Matches every element.

```css
*              /* every element on the page */
.product *     /* every element anywhere inside .product */
```

It is rarely used in tests, but handy for counting children or debugging.

#### 1.5 Compound selectors

Writing simple selectors together *with no spaces* creates a compound selector in which all parts must match the **same** element.

```css
button#login-button.btn-primary     /* a <button> with that id AND that class */
input[type="password"]#password     /* an input with type=password and id=password */
```

Read left to right: the tag (if any) comes first; then ids, classes, attributes in any order.

#### 1.6 Selector lists (grouping with commas)

A comma means "OR". The result is the union of all matches.

```css
h2, .product-image     /* all h2s plus all links with product-image */
#username, #password   /* both fields */
```

In Playwright, a comma-separated list is a valid CSS locator, but think twice: a locator that matches different kinds of things is unusual in tests, and strict mode will complain if you try to `click()` on multiple matches.

### Part 2: Attribute Selectors

An attribute selector filters elements by the **attributes** they have. They go inside square brackets. They are the most powerful tool in a tester's belt because HTML attributes carry meaning (type, name, placeholder, href, data-test, aria-label, and more).

#### 2.1 Presence: `[attr]`

Matches elements that *have* the attribute, regardless of value.

```css
[required]       /* username and password inputs */
[disabled]       /* the Reset button */
[checked]        /* the Remember me checkbox (initial state) */
[data-test]      /* every element with a data-test attribute */
```

Boolean attributes such as `required`, `disabled`, and `checked` have no value in HTML. Presence is the correct way to test them.

> Note: `[checked]` reflects the HTML attribute (the *initial* state). After the user clicks the checkbox, the attribute does not change, but the live property does. For the current state use the `:checked` pseudo-class (see *Pseudo-classes*).

#### 2.2 Exact value: `[attr="value"]`

Matches elements whose attribute equals the value exactly.

```css
[type="password"]
[data-test="login-button"]
[name="user-name"]
input[type="text"]
a[href="/cart"]
```

Always put the value in quotes. Quotes are required if the value contains spaces or special characters, and they are always safe.

#### 2.3 Starts with: `[attr^="value"]`

The caret `^` means "begins with".

```css
a[href^="https"]       /* external links beginning with https */
[data-test^="add-"]    /* add-backpack, add-bike-light */
[data-sku^="BP"]       /* backpack SKU */
```

Mnemonic: `^` is the "start" anchor in regular expressions.

#### 2.4 Ends with: `[attr$="value"]`

The dollar sign `$` means "ends with".

```css
a[href$=".pdf"]        /* spec sheets */
a[href$=".png"]        /* backpack image link */
[data-test$="-backpack"]  /* values ending in "-backpack": product-backpack and add-backpack */
```

Mnemonic: `$` is the "end" anchor in regular expressions.

#### 2.5 Contains substring: `[attr*="value"]`

The asterisk `*` means "contains anywhere".

```css
a[href*="example.com"]     /* both doc links */
[data-test*="bike"]        /* product-bike-light, add-bike-light */
[class*="btn-"]            /* btn-primary, btn-secondary */
```

**Caution:** substring matches are broad. `[class*="btn"]` would also match `.my-btn-hidden`, `.btn-group`, etc. Use it when you accept that risk, typically for *dynamic* values.

#### 2.6 Whitespace-separated word: `[attr~="value"]`

Matches when the attribute contains the value as one whole word in a space-separated list. This is how `.class` works behind the scenes.

```css
[class~="large"]       /* same as .large */
```

You will rarely use it directly, but it clarifies the difference: `[class~="btn"]` matches `class="btn large"` but NOT `class="btn-primary"`, whereas `[class*="btn"]` matches both.

#### 2.7 Hyphen prefix: `[attr|="value"]`

Matches the value exactly or followed by a hyphen, mainly for language codes (`lang|="en"` matches `en` and `en-US`). Rarely needed in testing.

#### 2.8 Case-insensitive flag: `[attr="value" i]`

Add ` i` before the closing bracket to ignore case.

```css
[data-test="LOGIN-BUTTON" i]   /* matches login-button */
a[href$=".PDF" i]
```

Attribute values are normally case-sensitive for most attributes. The `i` flag is a useful guard when the case of generated values varies.

#### 2.9 Chaining attributes

Several attribute selectors in a row mean AND:

```css
input[type="checkbox"][checked]
a[href^="https"][href$=".pdf"]
button[type="submit"][data-test="login-button"]
```

### Part 3: Which Attribute Should I Choose?

Not all attributes are equal. A rough ranking for test stability:

| Rank | Attribute | Why |
|------|-----------|-----|
| 1 | `data-test`, `data-testid`, `data-qa` | Created *for* testing; developers know not to casually change them |
| 2 | `id` (if static and meaningful) | Unique and fast, but check it is not auto-generated |
| 3 | `name` (inputs) | Tied to form submission, so changes are rare |
| 4 | `type`, `placeholder`, `aria-label`, `title`, `alt`, `href` | Meaningful, but copy changes alter them |
| 5 | Semantic class (`.product-name`) | Moderately stable |
| 6 | Style/utility class (`.mt-4`, `.col-md-6`) | Fragile: changes with styling |
| 7 | Position (`:nth-child(3)`) or long DOM path | Most fragile |

If your application has no `data-test` attributes, **ask the developers to add them**. This is one of the most valuable "shift-left" contributions a QE can make.

### Part 4: Using Selectors in Playwright Python

Playwright accepts CSS in `page.locator()`:

```python
page.locator("#login-button")
page.locator('[data-test="login-button"]')
page.locator("button.btn-primary")
```

There is also an explicit engine prefix, `css=`, which is optional: `page.locator("css=#login-button")`.

Playwright's CSS engine is slightly enhanced (for example, it pierces open shadow DOM by default), but everything in this lesson works the same. Playwright also offers *built-in* locators (`get_by_role`, `get_by_text`, `get_by_test_id`), which we cover in depth on Friday. For now, focus on CSS because it is the foundation, and many companies' existing test suites use it.

---

## Code Examples

### Example 1: DevTools console quick-check

```js
$$('#login-button').length                // 1
$$('.btn').length                          // 4 (login, reset, 2 add buttons)
$$('[data-test]').length                   // counts all elements with data-test
$$('a[href^="https"]').map(a => a.href)    // external links
$$('[data-sku]').map(e => e.dataset.sku)   // ["BP-001","BL-002"]
```

**Explanation:** `$$()` is Chrome's console helper equal to `document.querySelectorAll` but returning a real array (so `.map` works). `e.dataset.sku` reads the `data-sku` attribute through the DOM's `dataset` object. The `.btn` count is 4 because the login, reset, and two add buttons all carry the class.

### Example 2: A tested Python script that uses all selector types

Save as `selectors_demo.py` next to `shop.html`. (Install Playwright first as described in the *Playwright architecture and setup* lesson; or just read it for now.)

```python
from pathlib import Path
from playwright.sync_api import sync_playwright

PAGE_URL = Path("shop.html").resolve().as_uri()

# A dictionary maps a human-friendly name to (selector, expected_count)
LOCATOR_CATALOG = {
    "login button by id":            ("#login-button", 1),
    "login button by data-test":     ('[data-test="login-button"]', 1),
    "all buttons":                   ("button", 4),
    "primary button (compound)":     ("button.btn.btn-primary", 1),
    "required inputs":               ("input[required]", 2),
    "password field by type":        ('input[type="password"]', 1),
    "external links":                ('a[href^="https"]', 2),
    "pdf links":                     ('a[href$=".pdf"]', 2),
    "bike related test hooks":       ('[data-test*="bike"]', 2),
    "disabled controls":             ("[disabled]", 1),
    "add buttons (starts-with)":     ('[data-test^="add-"]', 2),
}

with sync_playwright() as p:
    browser = p.chromium.launch()
    page = browser.new_page()
    page.goto(PAGE_URL)

    for name, (selector, expected) in LOCATOR_CATALOG.items():
        actual = page.locator(selector).count()
        status = "OK  " if actual == expected else "FAIL"
        print(f"{status} {name:30} {selector:35} expected={expected} actual={actual}")

    browser.close()
```

**Line-by-line explanation:**

1. `from pathlib import Path` gives an object-oriented way to handle file paths.
2. `PAGE_URL = Path("shop.html").resolve().as_uri()` finds the absolute path of the HTML file and converts it to a `file:///...` URL, which the browser needs.
3. `LOCATOR_CATALOG` is a dictionary. Each key is a readable name; each value is a *tuple* containing the selector and how many matches we expect. This is a miniature version of today's exercise deliverable.
4. `with sync_playwright() as p:` opens and automatically closes Playwright, even if an error occurs.
5. `browser = p.chromium.launch()` starts headless Chromium. `page = browser.new_page()` creates a tab.
6. `page.goto(PAGE_URL)` loads the page.
7. The `for` loop unpacks `name` and the `(selector, expected)` tuple. `page.locator(selector).count()` returns how many elements match, **without** failing on 0 or many.
8. We print `OK` or `FAIL`. The format specifiers `:30` and `:35` pad text into aligned columns.
9. `browser.close()` frees resources.

Expected output (all OK) proves each selector matches what we claim. Notice the design: *verifying selectors with a counted catalog is a cheap, powerful habit.*

### Example 3: Turning the catalog into a PyTest parametrized test

You learned parametrization on Tuesday. Here is the same idea applied to selectors. This uses only features you have already seen, plus a plain Playwright script structure (the dedicated pytest-playwright plugin comes tomorrow, in depth).

```python
# test_selector_catalog.py
from pathlib import Path
import pytest
from playwright.sync_api import sync_playwright

PAGE_URL = Path("shop.html").resolve().as_uri()

CASES = [
    ("#login-button", 1),
    ("button.btn-primary", 1),
    ('input[type="password"]', 1),
    ('a[href$=".pdf"]', 2),
    ('[data-test^="add-"]', 2),
    ("[disabled]", 1),
]

@pytest.fixture(scope="module")
def page():
    with sync_playwright() as p:
        browser = p.chromium.launch()
        page = browser.new_page()
        page.goto(PAGE_URL)
        yield page
        browser.close()

@pytest.mark.parametrize("selector, expected", CASES)
def test_selector_matches_expected_count(page, selector, expected):
    assert page.locator(selector).count() == expected
```

**Explanation:** The fixture has `scope="module"` so the browser starts once for all test cases (recall *Fixture scopes*). Code before `yield` is setup; after `yield` is teardown. `@pytest.mark.parametrize` generates one test per `(selector, expected)` pair, so failures show exactly which selector broke.

---

## Real-World Scenarios

**Scenario 1: Finding all external download links.** The compliance team wants to check that every PDF link on a product page responds. You use `a[href$=".pdf"]` to collect them, loop over `.get_attribute("href")`, and test each URL. A single attribute selector replaced a manual hunt.

**Scenario 2: Add-to-cart buttons.** A page lists 30 products. Each add button has `data-test="add-<product-name>"`. To add one specific product, you use `[data-test="add-bike-light"]`. To add all, you use `[data-test^="add-"]` and loop. The same naming convention supports both uses.

**Scenario 3: Form validation tests.** The requirement says "all required fields show an error when empty". You select `input[required]` to discover the fields automatically, so your test stays correct when new required fields are added.

**Scenario 4: Disabled state.** A checkout button should stay disabled until the form is valid. `button[disabled]` present means disabled; absent means enabled. (Playwright also offers `to_be_disabled()` assertions, which we cover on Friday.)

---

## Common Mistakes

1. **Missing quotes in attribute values.** `[data-test=login-button]` works in some cases, but fails when the value contains a hyphen followed by a digit or special characters. Always quote.
2. **Mixing up `^`, `$`, `*`.** Remember: `^` start, `$` end, `*` contains.
3. **Using `[class="btn"]` to match a class.** This matches only when the whole `class` attribute is exactly `btn`. `.btn` is almost always what you mean.
4. **Using auto-generated IDs.** `#ember1234` or `#react-select-3-input` change between runs.
5. **Over-broad substring selectors.** `[href*="a"]` matches nearly everything.
6. **Space vs. no space.** `div .product` and `div.product` are different selectors.
7. **Forgetting that `[checked]` is initial state.** Use `:checked` or Playwright's `is_checked()` for the live state.
8. **Expecting one match without checking.** Always confirm the count.
9. **Putting a tag you are unsure of.** Writing `input#login-button` when it is actually a `<button>` matches nothing. If unsure, drop the tag.

---

## Practice Exercises

Use `shop.html`.

**Exercise 1: Basic selectors.** Write a selector for each, and the expected number of matches.

1. All `h2` headings
2. The `header` using its id
3. All elements with class `product`
4. Every link with class `product-image`

*Solutions:* `h2` (2); `#top-bar` (1); `.product` (2); `a.product-image` (2).

**Exercise 2: Attribute selectors.** Write selectors for:

1. The checkbox that is checked initially
2. The username input using `name`
3. Links whose `href` ends with `.jpg`
4. Elements whose `data-test` contains `backpack`
5. The cart link using its `aria-label`

*Solutions:* `input[type="checkbox"][checked]`; `input[name="user-name"]`; `a[href$=".jpg"]`; `[data-test*="backpack"]` (2 matches: product-backpack and add-backpack); `[aria-label="Shopping cart"]`.

**Exercise 3: Predict the count.**

| Selector | Your prediction |
|----------|-----------------|
| `.btn` | ? |
| `.btn.add` | ? |
| `.btn, .logo` | ? |
| `[class*="btn-"]` | ? |
| `a` | ? |

*Solutions:* 4; 2; 5 (4 buttons + 1 logo); 2 (btn-primary on login and btn-secondary on reset); 6 (logo, cart link, and 2 per product = 4, total 6).

**Exercise 4: Fix the broken selectors.** Each selector below is wrong. Say why and fix it.

1. `login-button`
2. `.btn-primary.btn-secondary`
3. `[data-test=add-backpack` 
4. `input#login-button`
5. `[class="btn"]`

*Solutions:* 1) missing `#`; 2) no element has both classes: use one; 3) missing closing bracket and quotes: `[data-test="add-backpack"]`; 4) it is a `button`, not an `input`: `button#login-button`; 5) matches nothing because every button has other classes: use `.btn`.

**Exercise 5: Catalog task.** Extend `LOCATOR_CATALOG` in Example 2 with three entries of your own (e.g., the Remember me checkbox, the first product's SKU, the Spec sheet links). Run it and make sure each prints `OK`.

**Exercise 6 (challenge).** Open https://www.saucedemo.com in Chrome (a public practice site). Using DevTools only, write selectors for the username field, password field, and the login button. Report which attribute you used and why you preferred it. (Hint: look for `data-test`.)

---

## Summary

- **Type** selectors use the tag (`button`), **ID** uses `#`, **class** uses `.`, and `*` matches everything.
- No space between simple selectors forms a **compound** selector where all parts apply to the same element. A comma forms a **group** (OR).
- **Attribute selectors** use brackets: `[attr]`, `[attr="v"]`, `[attr^="v"]`, `[attr$="v"]`, `[attr*="v"]`, `[attr~="v"]`, `[attr="v" i]`.
- Prefer attributes designed for testing (`data-test`), then stable IDs and names; avoid style classes and positions.
- Always verify the match count in DevTools before using a selector, and use `page.locator(selector)` in Playwright.
- Next: *Pseudo-classes*, which let you select by state and position (`:checked`, `:first-child`, `:not()`).

---

## Additional Resources

- MDN, Attribute selectors: https://developer.mozilla.org/en-US/docs/Web/CSS/Attribute_selectors
- MDN, Type, class, and ID selectors: https://developer.mozilla.org/en-US/docs/Learn_web_development/Core/Styling_basics/Type_class_and_ID_selectors
- Playwright Python, Other locators (CSS): https://playwright.dev/python/docs/other-locators
