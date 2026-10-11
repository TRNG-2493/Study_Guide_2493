# Filtering and Chaining Locators

## Learning Objectives

By the end of this lesson you will be able to:

- Explain why one locator is often not specific enough and how strict mode relates to that.
- Narrow a locator by chaining (`locator.locator()`, `get_by_*` on a locator).
- Filter locators using `filter(has_text=..., has_not_text=..., has=..., has_not=...)`.
- Combine locators with `and_()` and `or_()`.
- Select by position with `first`, `last` and `nth()`, and know when that is a bad idea.
- Work with lists: `count()`, `all()`, `all_inner_texts()`, `all_text_contents()`.
- Apply these techniques to real patterns: product cards, table rows, list items.

---

## Why This Matters

Real pages repeat the same structure many times: six product cards each with an "Add to cart" button, a table with fifty rows each with a "Delete" link, a list of search results each with a "View" button. A locator such as `get_by_role("button", name="Add to cart")` matches *all* of them. A beginner solution is `.first` or `.nth(3)`, but that is fragile: if the product order changes, the test now clicks the wrong item.

The professional approach is to say what a human says: "the **Sauce Labs Backpack** card's **Add to cart** button." That is *filtering and chaining*. It makes tests accurate, readable and resilient, which is essential for the UI scenarios you automate in Project 1: QE Foundations (searching, adding to cart, editing and deleting records). It continues this week's epic of turning manual test design into automation that can be trusted.

---

## The Concept

### 1. Strict mode revisited

Playwright locators are **strict**: if an action needs exactly one element but the locator matches several, Playwright raises an error, such as:

```
Error: strict mode violation: get_by_role("button", name="Add to cart") resolved to 6 elements
```

This is deliberately helpful. It prevents silently clicking the wrong element. Your response should be to **make the locator more specific**, not to silence the error with `.first`.

Note that *assertions on counts* (such as `to_have_count`) and list methods work with multiple elements; strictness only applies to actions and single-element assertions.

### 2. Chaining: searching within a locator

Every locator offers the same search methods as `page`. Searching on a locator limits the search to **inside** the matched element.

```python
card = page.locator(".inventory_item")            # all product cards (6)
```

A single card containing "Backpack" is what we want. We can chain:

```python
page.locator(".inventory_item").get_by_role("button", name="Add to cart")
```

That is still six buttons (one in each card). We need to select the right card first, which requires filtering.

Chaining example with a narrower parent:

```python
dialog = page.get_by_role("dialog")
dialog.get_by_role("button", name="Confirm").click()
```

The Confirm button is found only inside the dialog. If the page also has a "Confirm" button elsewhere, there is no ambiguity.

Two equivalent ways to chain:

```python
page.locator("#cart").locator(".item")        # CSS inside CSS
page.locator("#cart .item")                   # single CSS selector (same result)
```

Chaining several `locator()` calls reads naturally and mixes engines: `page.locator("form").get_by_label("Email")`.

### 3. Filtering: `locator.filter()`

`filter()` narrows a locator that matches many elements down to those that satisfy a condition. Signature (Python):

```python
locator.filter(
    has_text=...,        # element contains this text
    has_not_text=...,    # element does NOT contain this text
    has=...,             # element contains a descendant matching this locator
    has_not=...,         # element does NOT contain such a descendant
)
```

#### 3.1 `has_text`

```python
page.locator(".inventory_item").filter(has_text="Sauce Labs Backpack")
```

This reads: "from all product cards, keep those whose text includes *Sauce Labs Backpack*". Matching is a case-insensitive substring match; you can pass a regular expression:

```python
page.locator(".inventory_item").filter(has_text=re.compile(r"Backpack|Bike Light"))
```

Now chain to the button inside that card:

```python
(page.locator(".inventory_item")
     .filter(has_text="Sauce Labs Backpack")
     .get_by_role("button", name="Add to cart")
     .click())
```

Python tip: wrapping a long chain in parentheses lets you split it across lines without backslashes.

#### 3.2 `has_not_text`

```python
page.locator(".inventory_item").filter(has_not_text="Backpack")
```

Cards that do **not** mention backpack (5 of them).

#### 3.3 `has`

Filter by a descendant locator. The inner locator is evaluated **relative to the outer element**, not the whole page.

```python
page.get_by_role("listitem").filter(has=page.get_by_role("heading", name="Product 2"))
```

Reads: "the list items which contain a heading named Product 2". Use `has` when the distinguishing feature is another element (a badge, a heading, a particular button) rather than raw text.

Example: rows that contain a "Sold out" badge:

```python
rows = page.get_by_role("row")
sold_out = rows.filter(has=page.get_by_text("Sold out"))
```

#### 3.4 `has_not`

```python
page.get_by_role("listitem").filter(has_not=page.get_by_role("button", name="Remove"))
```

Items that have no Remove button.

#### 3.5 Several filters together

Filters can be chained, and every filter must be satisfied:

```python
page.get_by_role("row") \
    .filter(has_text="Jane") \
    .filter(has_not_text="Inactive") \
    .get_by_role("button", name="Edit")
```

### 4. Matching two conditions: `and_()`

`locator.and_(other)` matches elements that satisfy **both** locators (an AND on the *same element*). Example: a button that is also a "primary" button:

```python
button = page.get_by_role("button")
primary = page.locator(".btn-primary")
button.and_(primary)
```

Compare with filter(has=...), which tests *descendants*. `and_` tests the element itself.

Another use: combine a role and a title:

```python
page.get_by_role("button").and_(page.get_by_title("Subscribe"))
```

### 5. Matching either condition: `or_()`

`locator.or_(other)` matches elements that satisfy **either** locator. A very practical use is handling optional UI such as a cookie banner or a variable confirmation:

```python
new_email = page.get_by_role("button", name="New")
dialog = page.get_by_text("Confirm security settings")
expect(new_email.or_(dialog).first).to_be_visible()
```

Reads: "wait until either the New button or the security dialog appears". Be careful: if both appear, the locator matches two elements and strict mode will complain on single-element actions, which is why we used `.first` here.

Use `or_()` sparingly. A test that does not know what state the app is in can hide defects. Prefer deterministic setup (for example, set a cookie so the banner never appears).

### 6. Positional selection

```python
items = page.locator(".inventory_item")
items.first            # first match
items.last             # last match
items.nth(2)           # third match (zero-based index: 0, 1, 2)
```

When is it acceptable?

- When the **position itself is the requirement** ("the first search result is the most relevant", "newest item is at the top").
- When the elements are truly identical and order is guaranteed.

When is it a mistake? When you pick an element by position only because you lack a better locator, and the order can change (sorting, new data, parallel tests). In that case filter by text or a unique descendant.

### 7. Working with lists of elements

```python
names = page.locator(".inventory_item_name")

names.count()                 # int, evaluated now (snapshot)
names.all()                   # list of Locator objects, one per element (snapshot)
names.all_inner_texts()       # list of visible text strings
names.all_text_contents()     # list of textContent strings
```

Important warnings:

- These are **snapshots**; they do not wait for the list to finish loading. First assert something that confirms the list is ready, such as `expect(names).to_have_count(6)`.
- Then collect data. Example: verifying sorting.

```python
expect(names).to_have_count(6)
texts = names.all_inner_texts()
assert texts == sorted(texts)
```

Python's `sorted()` (docs.python.org) returns a new sorted list; comparing it with the original shows whether the page list is sorted alphabetically.

Iterating:

```python
for item in page.locator(".inventory_item").all():
    print(item.locator(".inventory_item_name").inner_text())
```

Each `item` is a Locator pinned to one element at the time `.all()` ran; inside we chain a child locator.

You can also assert on a whole list:

```python
expect(names).to_have_text([
    "Sauce Labs Backpack",
    "Sauce Labs Bike Light",
    "Sauce Labs Bolt T-Shirt",
    "Sauce Labs Fleece Jacket",
    "Sauce Labs Onesie",
    "Test.allTheThings() T-Shirt (Red)",
])
```

Passing a list to `to_have_text` asserts the exact texts *in order* and also the count, and it retries until true. This is better than reading texts into Python and comparing, because it waits.

### 8. Tables: rows and cells

HTML:

```html
<table>
  <tr><th>Name</th><th>Role</th><th>Actions</th></tr>
  <tr><td>Jane</td><td>Admin</td><td><button>Edit</button><button>Delete</button></td></tr>
  <tr><td>Raj</td><td>Tester</td><td><button>Edit</button><button>Delete</button></td></tr>
</table>
```

Delete Raj's row:

```python
row = page.get_by_role("row").filter(has_text="Raj")
row.get_by_role("button", name="Delete").click()
expect(page.get_by_role("row").filter(has_text="Raj")).to_have_count(0)
```

Read a cell:

```python
role = row.get_by_role("cell").nth(1)       # position within a known structure is fine
expect(role).to_have_text("Tester")
```

Here `nth(1)` is acceptable because the column order is part of the table's structure.

### 9. A step-by-step method for building a precise locator

1. Identify the target ("Add to cart button for the Backpack").
2. Find the repeated container (`.inventory_item`).
3. Find what uniquely identifies the container (its title text).
4. Filter the container by that identity.
5. Chain the target inside the container.
6. Verify uniqueness with `expect(locator).to_have_count(1)` while developing.
7. Optionally assign the container to a variable with a descriptive name for readability and reuse.

```python
backpack = page.locator(".inventory_item").filter(has_text="Sauce Labs Backpack")
backpack.get_by_role("button", name="Add to cart").click()
expect(backpack.get_by_role("button", name="Remove")).to_be_visible()
```

Variables for containers keep subsequent steps short, and because locators are lazy, `backpack` is re-evaluated each time: after the click, the button changes to "Remove" and the `backpack` card is still found.

### 10. Dealing with `get_by_text` ambiguity

If the text appears in many places (a navigation link and a heading both say "Products"), restrict with a container:

```python
page.get_by_role("navigation").get_by_text("Products")
page.get_by_role("main").get_by_text("Products")
```

---

## Code Examples

### Example 1: Add a specific product to the cart (SauceDemo)

```python
import re
from playwright.sync_api import Page, expect


def login(page: Page):
    page.goto("https://www.saucedemo.com/")
    page.get_by_placeholder("Username").fill("standard_user")
    page.get_by_placeholder("Password").fill("secret_sauce")
    page.get_by_role("button", name="Login").click()
    expect(page).to_have_url(re.compile("inventory"))


def test_add_specific_product(page: Page):
    login(page)

    backpack = page.locator(".inventory_item").filter(has_text="Sauce Labs Backpack")
    backpack.get_by_role("button", name="Add to cart").click()

    expect(backpack.get_by_role("button", name="Remove")).to_be_visible()
    expect(page.locator(".shopping_cart_badge")).to_have_text("1")
```

**Explanation:**

- `login()` is a plain helper function (no `test_` prefix, so PyTest does not run it as a test).
- `page.locator(".inventory_item")` matches six cards.
- `.filter(has_text="Sauce Labs Backpack")` narrows it to one.
- `.get_by_role("button", name="Add to cart")` searches inside that card only: exactly one button, so no strict-mode error.
- After clicking, the same button becomes "Remove". We assert it inside the same card, confirming that we affected the right product.

### Example 2: Add several products using a loop and parametrization

```python
import pytest

PRODUCTS = ["Sauce Labs Backpack", "Sauce Labs Bike Light", "Sauce Labs Onesie"]


def test_add_multiple_products(page: Page):
    login(page)
    for name in PRODUCTS:
        card = page.locator(".inventory_item").filter(has_text=name)
        card.get_by_role("button", name="Add to cart").click()

    expect(page.locator(".shopping_cart_badge")).to_have_text(str(len(PRODUCTS)))
```

**Explanation:** the loop uses Python data (Monday's lists), and the locator is rebuilt for each name. `str(len(PRODUCTS))` converts 3 to "3", because `to_have_text` compares strings.

### Example 3: `has` with a descendant locator

```python
def test_filter_by_descendant(page: Page):
    login(page)
    cards_with_bike = page.locator(".inventory_item").filter(
        has=page.get_by_text("Sauce Labs Bike Light")
    )
    expect(cards_with_bike).to_have_count(1)
    cards_without_bike = page.locator(".inventory_item").filter(
        has_not=page.get_by_text("Sauce Labs Bike Light")
    )
    expect(cards_without_bike).to_have_count(5)
```

**Explanation:** `has=` takes a locator. Playwright evaluates it *inside each card*. Note that you pass `page.get_by_text(...)`; Playwright treats it relative to the card automatically, so you do not need to chain.

### Example 4: A self-contained table with `and_` and `or_`

```python
TABLE_HTML = """
<table>
  <tr><th>Name</th><th>Status</th><th>Actions</th></tr>
  <tr><td>Jane</td><td>Active</td><td><button>Edit</button><button>Delete</button></td></tr>
  <tr><td>Raj</td><td>Inactive</td><td><button>Edit</button><button>Delete</button></td></tr>
  <tr><td>Mei</td><td>Active</td><td><button>Edit</button><button>Delete</button></td></tr>
</table>
<button id="primary" class="btn-primary">Save</button>
<button class="btn-secondary">Cancel</button>
"""


def test_table_filters(page: Page):
    page.set_content(TABLE_HTML)
    rows = page.get_by_role("row")

    # header row + 3 data rows
    expect(rows).to_have_count(4)

    active = rows.filter(has_text="Active").filter(has_not_text="Inactive")
    expect(active).to_have_count(2)

    # Pick Raj's Delete button
    raj_delete = rows.filter(has_text="Raj").get_by_role("button", name="Delete")
    expect(raj_delete).to_have_count(1)

    # and_: a button that is also primary
    primary_button = page.get_by_role("button").and_(page.locator(".btn-primary"))
    expect(primary_button).to_have_text("Save")

    # or_: either Save or Cancel
    either = page.get_by_role("button", name="Save").or_(page.get_by_role("button", name="Cancel"))
    expect(either).to_have_count(2)
```

**Explanation:** "Active" is a substring of "Inactive" (case-insensitive!), so `filter(has_text="Active")` alone would match Raj too; adding `.filter(has_not_text="Inactive")` fixes it. This is a classic pitfall: substring matching. `and_` and `or_` examples show element-level combination.

### Example 5: Asserting a list and sort order

```python
def test_sort_by_name_z_to_a(page: Page):
    login(page)
    page.locator("[data-test='product-sort-container']").select_option("za")

    names = page.locator(".inventory_item_name")
    expect(names).to_have_count(6)
    texts = names.all_inner_texts()
    assert texts == sorted(texts, reverse=True)
```

**Explanation:** `select_option("za")` chooses the dropdown option whose value is `za` (Name Z to A). We first assert the count (waits for the list), then read all names and compare with a reverse-sorted copy. Sorting uses Python's `sorted(..., reverse=True)`.

---

## Real-World Scenarios

1. **Shopping cart tests.** A QE adds specific products by name rather than "the first button", so tests remain valid when marketing reorders the catalogue.
2. **Admin tables.** "Delete user Raj" is automated by filtering the row by name and clicking Delete inside it. Without chaining, the test would need brittle XPath like `(//tr)[3]//button[2]`.
3. **Search results validation.** After searching "laptop", the test collects all result titles with `all_inner_texts()` and verifies each contains the term, a real data check on the UI.
4. **Dynamic banners.** A site sometimes shows a promotional modal. `or_()` can wait for "either the dashboard or the modal", then the test dismisses the modal if present, keeping the test stable while the team works on a proper fix.

---

## Common Mistakes

1. **Using `.first` or `.nth()` to bypass strict mode** when text or structure could identify the element precisely.
2. **Forgetting that `has_text` is a case-insensitive substring match** ("Active" matches "Inactive"). Use `re.compile(r"^Active$")`, `exact` approaches, or `has_not_text` to disambiguate.
3. **Reading `count()` or `all_inner_texts()` before the page has loaded.** They are snapshots; first use `expect(...).to_have_count(...)` to wait.
4. **Confusing `has=` (descendant) with `and_()` (same element).**
5. **Passing a locator created from a different frame/page to `has=`.** The inner locator must belong to the same frame as the outer.
6. **Writing the inner locator for `has=` with an absolute CSS path from the document root.** It is matched relative to the outer element; keep it simple.
7. **Overusing `or_()`** to hide uncertain test state.
8. **Long one-liner chains that no one can read.** Break into variables with meaningful names (`backpack`, `row`).
9. **Looping over `.all()` and clicking items that change the list** (for example deleting rows). The pinned locators may then point to removed elements. Re-query on each iteration, or work from the bottom up.

---

## Practice Exercises

**Exercise 1.** On SauceDemo, write a test that adds "Sauce Labs Bolt T-Shirt" to the cart, using `filter(has_text=...)`. Assert the corresponding button changes to "Remove".

**Exercise 2.** Write a test that counts how many products do NOT contain the word "Sauce". *(Answer: 1, the "Test.allTheThings() T-Shirt (Red)".)* Use `has_not_text`.

**Exercise 3.** Use the table from Example 4. Write a test that clicks Edit for Mei only, then asserts that no other row was affected (you can add an `onclick` to the Edit button that adds a class `edited` to its row, then use `has=`/class checks).

*Hint:* use `page.locator("tr.edited")` and assert `to_have_count(1)` and `to_contain_text("Mei")`.

**Exercise 4.** Write a test that verifies the product prices on SauceDemo, collected using `.inventory_item_price`, are all positive numbers: strip the `$`, convert with `float()` and assert each is greater than zero.

*Solution sketch:*

```python
prices = page.locator(".inventory_item_price")
expect(prices).to_have_count(6)
values = [float(t.replace("$", "")) for t in prices.all_inner_texts()]
assert all(v > 0 for v in values)
```

**Exercise 5.** Using `expect(names).to_have_text([...])` with a list, verify the default product order after login. Then sort low-to-high by price (`select_option("lohi")`) and verify the new first product is "Sauce Labs Onesie".

**Exercise 6 (Project 1).** For one Project 1 scenario that touches a list or table (e.g. add item, delete record), write the locator chain using at least one `filter()` and explain in a comment why position-based selection would be risky.

---

## Summary

- A locator matching several elements causes a strict-mode error on actions; fix it by being more specific, not by blindly using `.first`.
- **Chaining** (`locator.locator()`, `locator.get_by_*()`) searches inside a parent.
- **`filter()`** narrows by `has_text`, `has_not_text`, `has` and `has_not`.
- **`and_()`** means both conditions on the same element; **`or_()`** means either.
- `first`, `last` and `nth()` select by position and are best used only when position is meaningful.
- `count()`, `all()`, `all_inner_texts()` are snapshots; wait first with `expect(...).to_have_count()`.
- Name container locators (`backpack`, `row`) and chain inside them for readable, maintainable tests.

---

## Additional Resources

- Playwright for Python: Locators (filtering and chaining): https://playwright.dev/python/docs/locators#filtering-locators
- Playwright for Python: Locator API reference: https://playwright.dev/python/docs/api/class-locator
- Python documentation: Built-in functions (`sorted`, `all`): https://docs.python.org/3/library/functions.html
