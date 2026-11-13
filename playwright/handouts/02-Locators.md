# 02 — Locators

> **Before you start**
>
> - **By the end you can:** write CSS/XPath selectors, use the built-in `get_by_...` locators, fix strict mode errors, and narrow matches with `filter()`, chaining, `nth()`, `first` and `last`.
> - **Practice site:** Swag Labs — <https://www.saucedemo.com/> (`standard_user` / `secret_sauce`).
> - **Create** a folder `lecture02/` with three files:
>
> `pytest.ini`
>
> ```ini
> [pytest]
> base_url = https://www.saucedemo.com
> ```
>
> `conftest.py` — lets `get_by_test_id()` read this site's `data-test` attributes (fixtures are explained in Lecture 7; just copy it):
>
> ```python
> import pytest
>
> @pytest.fixture(scope="session", autouse=True)
> def use_data_test_attribute(playwright):
>     playwright.selectors.set_test_id_attribute("data-test")
> ```
>
> `test_locators.py`
>
> ```python
> from playwright.sync_api import Page, expect
>
>
> def log_in(page):
>     page.goto("/")
>     page.get_by_placeholder("Username").fill("standard_user")
>     page.get_by_placeholder("Password").fill("secret_sauce")
>     page.get_by_role("button", name="Login").click()
> ```
>
> - **Run tests with:** `pytest -s` (add `--headed` to watch)

---

## Topic 1 — What a locator is (and CSS / XPath)

### Definition

A **locator** describes *how to find* an element on the page. Creating a locator does not search the page; Playwright searches each time you **use** it (click, fill, `expect`). `page.locator()` accepts a CSS selector or an XPath expression.

### Key ideas

- **Lazy:** a locator searches only when used, so it still works after the page changes.
- **Strict:** an action needs **exactly one** match, or Playwright stops with an error.
- CSS and XPath depend on page **structure** (ids, classes, nesting), so they break more often than built-in locators.

| CSS | XPath | Finds |
|---|---|---|
| `#user-name` | `//input[@id='user-name']` | The element with id `user-name` |
| `.inventory_item` | `//div[@class='inventory_item']` | Elements with that class |
| `[data-test='title']` | `//*[@data-test='title']` | By attribute |
| `.inventory_item .inventory_item_price` | `//div[@class='inventory_item_price']` | Descendant |

### Worked example — count products with CSS and XPath

**Step 1.** Log in:

```python
def test_css_and_xpath(page: Page):
    log_in(page)
```

**Step 2.** Create a CSS locator for all product cards and count them:

```python
    products = page.locator(".inventory_item")
    print("Products:", products.count())
```

**Step 3.** Find the page heading with an attribute selector:

```python
    title = page.locator("[data-test='title']")
    print("Title:", title.text_content())
```

**Step 4.** Turn the prints into checks:

```python
    expect(products).to_have_count(6)
    expect(title).to_have_text("Products")
```

> **Predict:** at which line does Playwright actually search the page for `.inventory_item` — Step 2's first line or its second?

### Checkpoint

```
Products: 6
Title: Products
.
1 passed
```

### Your turn

1. On the login page (before logging in), locate the username input with CSS by id, and again with XPath. Print `.count()` for both.
2. Locate the password input using an attribute selector.
   *Hint: `input[type='...']`.*
3. After logging in, count all prices with `.inventory_item_price`.

---

## Topic 2 — Built-in locators

### Definition

Built-in locators find elements the way a **user** does: by role, label, placeholder or visible text. They read like plain English and survive changes to ids, classes and layout.

### Key ideas

Try them in this order and use the first one that works:

| # | Locator | Swag Labs example |
|---|---|---|
| 1 | `get_by_role()` | `get_by_role("button", name="Login")` |
| 2 | `get_by_label()` | *(no `<label>`s on this site — see below)* |
| 3 | `get_by_placeholder()` | `get_by_placeholder("Username")` |
| 4 | `get_by_text()` | `get_by_text("Products")` |
| 5 | `get_by_alt_text()` / `get_by_title()` | `get_by_alt_text("Sauce Labs Backpack")` |
| 6 | `get_by_test_id()` | `get_by_test_id("login-button")` |
| 7 | `locator("css or xpath")` | Last resort |

- `name=` and `get_by_text` match **partially and ignore case** by default. Add `exact=True` to tighten.
- Swag Labs inputs have **no labels**, so `get_by_label` finds nothing — use `get_by_placeholder`.
- Common roles: `button`, `link`, `heading`, `textbox`, `checkbox`, `combobox`, `img`, `alert`.

### Worked example — a failed login, with built-in locators

**Step 1.** Open the login page and find the button by role:

```python
def test_failed_login(page: Page):
    page.goto("/")
    expect(page.get_by_role("button", name="Login")).to_be_visible()
```

**Step 2.** Show that `get_by_label` finds nothing here:

```python
    print("By label:", page.get_by_label("Username").count())
```

**Step 3.** Fill the fields by placeholder, with a wrong password:

```python
    page.get_by_placeholder("Username").fill("standard_user")
    page.get_by_placeholder("Password").fill("wrong")
    page.get_by_role("button", name="Login").click()
```

**Step 4.** The error message has the role `alert`:

```python
    expect(page.get_by_role("alert")).to_contain_text(
        "Username and password do not match"
    )
```

**Step 5.** The same message by test id:

```python
    expect(page.get_by_test_id("error")).to_be_visible()
```

> **Predict:** would `page.get_by_text("login")` find only the button? Try it with `.count()`.

### Checkpoint

```
By label: 0
.
1 passed
```

### Your turn

1. Log in, then locate the Backpack image with `get_by_alt_text` and check it is visible.
2. Locate the sort dropdown with `get_by_role("combobox")` and print its value with `.input_value()`.
3. Locate the cart icon with `get_by_test_id("shopping-cart-link")`.
4. Log in as `locked_out_user` and check the alert text says the user is locked out.

### Common errors

| Error | Fix |
|---|---|
| `get_by_label` finds nothing | The page has no `<label>`; use `get_by_placeholder` |
| `get_by_test_id` finds nothing | `conftest.py` missing — this site uses `data-test`, not `data-testid` |
| Long DevTools selector like `div > div:nth-child(3) > span` | Replace with a built-in locator |

---

## Topic 3 — Strict mode

### Definition

Strict mode means an action (`click`, `fill`, …) or a single-element check (`to_be_visible`, `to_have_value`, …) must match **exactly one** element. If several match, Playwright stops with an error instead of guessing.

### Key ideas

- The error message says `resolved to N elements` and lists them — read it, it tells you what matched.
- Group checks are allowed: `expect(locator).to_have_count(6)`.
- The fix is always to make the locator **more specific** (Topics 4 and 5).

### Worked example — trigger and read a strict mode error

**Step 1.** Locate all "Add to cart" buttons:

```python
def test_strict_mode(page: Page):
    log_in(page)
    add_buttons = page.get_by_role("button", name="Add to cart")
```

**Step 2.** A group check is fine:

```python
    expect(add_buttons).to_have_count(6)
```

**Step 3.** Now try to click — this fails:

```python
    add_buttons.click()
```

> **Predict:** how many elements will the error say it resolved to?

**Step 4.** Run it and read the error. Then replace Step 3 with a specific button:

```python
    add_buttons.first.click()
    expect(page.get_by_test_id("shopping-cart-badge")).to_have_text("1")
```

### Checkpoint

First run:

```
Error: strict mode violation: get_by_role("button", name="Add to cart") resolved to 6 elements
```

After the fix: `1 passed`.

### Your turn

1. Try `page.get_by_role("link", name="Sauce Labs Backpack").click()`. Why does it resolve to **2** elements?
   *Hint: the product image is a link too, and its name comes from the alt text.*
2. Fix it with `exact=True`? Does that help? Then fix it another way.
3. Is `expect(page.get_by_role("button")).to_be_visible()` a strict-mode check? Try it.

---

## Topic 4 — Filtering locators

### Definition

`filter()` keeps only the matches of a locator that meet a condition: containing some text (`has_text`), not containing it (`has_not_text`), or containing another locator (`has` / `has_not`).

### Key ideas

| Filter | Example |
|---|---|
| `has_text="Backpack"` | Product cards that mention Backpack |
| `has_not_text="T-Shirt"` | Cards that don't mention T-Shirt |
| `has=page.get_by_role("button", name="Remove")` | Cards already in the cart |
| `has_text="$15.99"` | Cards with that price |

### Worked example — filter the product cards

**Step 1.** Start from all product cards:

```python
def test_filter_products(page: Page):
    log_in(page)
    products = page.locator(".inventory_item")
```

**Step 2.** Keep the ones that aren't T-shirts:

```python
    not_shirts = products.filter(has_not_text="T-Shirt")
    expect(not_shirts).to_have_count(4)
```

**Step 3.** Add the Backpack, then find cards by what they **contain**:

```python
    products.filter(has_text="Backpack").get_by_role("button").click()
    in_cart = products.filter(has=page.get_by_role("button", name="Remove"))
    expect(in_cart).to_have_count(1)
    expect(in_cart).to_contain_text("Sauce Labs Backpack")
```

**Step 4.** Filter by price:

```python
    expect(products.filter(has_text="$15.99")).to_have_count(2)
```

> **Predict:** what would `products.filter(has_text="backpack")` (lowercase) return?

### Checkpoint

`1 passed` with counts 4, 1 and 2.

### Your turn

1. Find the card for the **Onesie** with `has_text` and print its price.
2. Add two products, then count cards that still have an **Add to cart** button.
   *Hint: `has=page.get_by_role("button", name="Add to cart")`.*
3. Find the card that mentions "T-Shirt" **and** costs `$15.99`. How many are there?
   *Hint: you can call `filter()` twice.*

---

## Topic 5 — Chaining, `nth()`, `first` and `last`

### Definition

**Chaining** calls a locator method on another locator to search only **inside** it. `first`, `last` and `nth(i)` pick a match by position, counting from 0.

### Key ideas

- The usual strict-mode fix: **find the container first, then the element inside it.**
- `nth(1)` is the **second** match.
- Prefer `filter(has_text=...)` over position — if the order changes (e.g. after sorting), `nth(2)` silently picks a different element.
- For all matches: `.count()`, `.all()`, `.all_text_contents()`.

### Worked example — add the Fleece Jacket and read the list

**Step 1.** Find the Fleece Jacket card:

```python
def test_chaining(page: Page):
    log_in(page)
    jacket = page.locator(".inventory_item").filter(has_text="Fleece Jacket")
```

**Step 2.** Chain to its button and click:

```python
    jacket.get_by_role("button", name="Add to cart").click()
    expect(jacket.get_by_role("button")).to_have_text("Remove")
```

**Step 3.** Read all product names:

```python
    names = page.locator(".inventory_item_name")
    print(names.all_text_contents())
```

**Step 4.** Pick by position:

```python
    expect(names.first).to_have_text("Sauce Labs Backpack")
    expect(names.nth(1)).to_have_text("Sauce Labs Bike Light")
    expect(names.last).to_have_text("Test.allTheThings() T-Shirt (Red)")
```

**Step 5.** Read one price by chaining card → price:

```python
    print("Jacket price:", jacket.locator(".inventory_item_price").text_content())
```

> **Predict:** what does `names.nth(6)` give you?

### Checkpoint

```
['Sauce Labs Backpack', 'Sauce Labs Bike Light', 'Sauce Labs Bolt T-Shirt', 'Sauce Labs Fleece Jacket', 'Sauce Labs Onesie', 'Test.allTheThings() T-Shirt (Red)']
Jacket price: $49.99
.
1 passed
```

### Your turn

1. Find the description text inside the Onesie card by chaining.
2. Loop over `names.all()` and print each name with its index.
3. Sort by "Price (low to high)" with `page.get_by_role("combobox").select_option(label="Price (low to high)")`. What is `names.first` now?
4. Rewrite `names.nth(3)` using `filter` so it no longer depends on order.

### Common errors

| Error | Fix |
|---|---|
| `nth(1)` expecting the first element | `nth` counts from 0; use `nth(0)` or `.first` |
| Searching on `page` instead of the card | Call the locator method on the card locator |
| Test passes but clicks the wrong item after sorting | You relied on position; use `filter` |

---

## Stretch challenge

Without using `nth`, `first` or `last`, write a test that adds every product under $20 to the cart, then checks the cart badge shows the right number.
*Hint: loop over `.all()` of the cards, read each price, convert it to a number.*

## Exit ticket

1. What does "locators are lazy" mean?
2. What is the recommended fix for "resolved to 6 elements"?
3. Why doesn't `get_by_label("Username")` work on Swag Labs, and what do you use instead?

## Cheat sheet

| Code | Purpose |
|---|---|
| `page.locator("css")` / `page.locator("//xpath")` | CSS / XPath locator |
| `page.get_by_role("button", name="X", exact=True)` | By role and accessible name |
| `page.get_by_label("Email")` | By form label |
| `page.get_by_placeholder("Username")` | By placeholder |
| `page.get_by_text("...", exact=True)` | By visible text |
| `page.get_by_alt_text(...)` / `get_by_title(...)` | Images / tooltips |
| `page.get_by_test_id("...")` | By test id (`data-test` here, set in `conftest.py`) |
| `loc.filter(has_text=..., has_not_text=...)` | Filter by text |
| `loc.filter(has=..., has_not=...)` | Filter by contained element |
| `container.get_by_role(...)` | Chain: search inside |
| `.first` / `.last` / `.nth(i)` | Pick by position (from 0) |
| `.count()` / `.all()` / `.all_text_contents()` | Work with all matches |
| `.highlight()` | Outline a match in `--headed` mode |
