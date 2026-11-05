# Playwright Locator Practice: CSS & XPath

Practice locating elements on the **Practice Store** page (`practice_store.html`) using `page.locator()` with CSS selectors and XPath. Each question includes the `expect` assertion your locator must pass.

---

### Tips

- Playwright treats a selector starting with `//` as XPath. If it starts with `(`, add `xpath=` in front, e.g. `page.locator("xpath=(//li)[2]")`.
- If a locator matches more than one element, actions like `.click()` will fail in strict mode. Use `.count()`, `.nth(i)`, `.first` or `.last`.
- `to_have_text("...")` needs the element's whole text to match, ignoring extra spaces around it. `to_contain_text("...")` only needs part of the text to match.
- Passing a list to `to_have_text([...])` checks the number of matches, their text and their order all in one assertion.
- `expect` keeps retrying for up to 5 seconds before it fails, so you don't need to add waits yourself.

---

## Part A: CSS selectors

| # | Locate… | Assertion |
|---|---|---|
| 1 | The main page heading | `expect(loc).to_have_text("Practice Store")` |
| 2 | The email input, using its id | `expect(loc).to_have_attribute("type", "email")` |
| 3 | The password input, using its `type` attribute | `expect(loc).to_have_attribute("placeholder", "Enter password")` |
| 4 | The "Remember me" checkbox, using its id | `expect(loc).not_to_be_checked()` |
| 5 | The Sign in button, using its `type` attribute | `expect(loc).to_have_text("Sign in")` |
| 6 | The logo image, using its `alt` attribute | `expect(loc).to_have_attribute("src", "logo.png")` |
| 7 | All links inside the navigation bar | `expect(loc).to_have_text(["Home", "Products", "Contact us"])` |
| 8 | The "Contact us" link, using its `href` | `expect(loc).to_have_text("Contact us")` |
| 9 | The 🚚 icon, using a partial match on its `title` (contains "shipping") | `expect(loc).to_have_attribute("title", "Free shipping on orders over $50")` |
| 10 | The Checkout button, using its `data-testid` | `expect(loc).to_have_text("Checkout")` |
| 11 | All product items | `expect(loc).to_have_count(4)` |
| 12 | All product prices | `expect(loc).to_have_text(["$29.99", "$9.99", "$15.99", "$49.99"])` |
| 13 | The disabled "Add to cart" button | `expect(loc).to_be_disabled()` |
| 14 | All "Add to cart" buttons that are **not** disabled | `expect(loc).to_have_count(3)` |
| 15 | The name of the **first** product | `expect(loc).to_have_text("Backpack")` |
| 16 | The price of the **third** product | `expect(loc).to_have_text("$15.99")` |
| 17 | The stock status of the **last** product | `expect(loc).to_have_text("In stock")` |
| 18 | All `h2` headings that are direct children of a `section` | `expect(loc).to_have_text(["Sign in", "Products", "Recent orders"])` |
| 19 | All rows in the orders table body (not the header row) | `expect(loc).to_have_count(4)` |
| 20 | The status cell of the **second** order row | `expect(loc).to_have_text("Pending")` |

**Bonus (CSS 4):** call `loc.check()`, then assert `expect(loc).to_be_checked()`.

---

## Part B: XPath

| # | Locate… | Assertion |
|---|---|---|
| 1 | The third link in the nav, by position | `expect(loc).to_have_text("Contact us")` |
| 2 | The password input, using its `id` attribute | `expect(loc).to_have_attribute("type", "password")` |
| 3 | The email input, using its `placeholder` | `expect(loc).to_be_empty()` |
| 4 | The "Home" link, using its exact text | `expect(loc).to_have_attribute("href", "#home")` |
| 5 | The "Forgot password?" link, using partial text ("Forgot") | `expect(loc).to_have_text("Forgot password?")` |
| 6 | The Sign in **button** (not the heading), using its text | `expect(loc).to_have_attribute("type", "submit")` |
| 7 | The checkbox inside the label that contains "Remember me" | `expect(loc).to_have_id("remember")` |
| 8 | The Checkout button, using its text | `expect(loc).to_have_attribute("data-testid", "checkout-button")` |
| 9 | All product `li` elements, using the `class` attribute | `expect(loc).to_have_count(4)` |
| 10 | The product heading with the text "Jacket" | `expect(loc).to_be_visible()` |
| 11 | The price of "Bike Light", starting from its heading (use a sibling axis) | `expect(loc).to_have_text("$9.99")` |
| 12 | The name of the product that is "Out of stock" (go up to the parent, then down) | `expect(loc).to_have_text("Bike Light")` |
| 13 | The "Add to cart" button of the "T-Shirt" product | `expect(loc).to_be_enabled()` |
| 14 | All buttons that have the `disabled` attribute | `expect(loc).to_have_count(1)` |
| 15 | The heading of the **second** product, using `( … )[n]` indexing | `expect(loc).to_have_text("Bike Light")` |
| 16 | The **last** price on the page, using `last()` | `expect(loc).to_have_text("$49.99")` |
| 17 | All stock paragraphs whose text is exactly "In stock" | `expect(loc).to_have_count(3)` |
| 18 | The status of the order placed by "Chen Wei" | `expect(loc).to_have_text("Shipped")` |
| 19 | The order number of the "Pending" order (use a preceding-sibling axis) | `expect(loc).to_have_text("1002")` |
| 20 | The total of the "Cancelled" order | `expect(loc).to_have_text("$15.99")` |

---

## Example - CSS

### CSS 2. The email input, using its id

```python
loc = page.locator("#email")
expect(loc).to_have_attribute("type", "email")
```

## Example - Xpath

### XPath 1. The third link in the nav, by position

```python
loc = page.locator("//nav/a[3]")
expect(loc).to_have_text("Contact us")
```