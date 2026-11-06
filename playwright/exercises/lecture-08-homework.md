# Lecture 8: Homework

**Time:** 60–75 minutes
**Goal:** extend page objects, write tests with them, and convert script-style tests to POM.

## Setup

1. Copy the whole `lecture_08/` folder and rename the copy `homework_08/`.
2. Delete the test files inside `homework_08/tests/` (keep the folder).
3. Create two files in `homework_08/tests/`:
   - `test_scripts_to_convert.py` (code below; for Part 3)
   - `test_lecture08_homework.py` (your tests)

```
homework_08/
├── conftest.py
├── site/
├── pages/                         ← you'll ADD methods here
└── tests/
    ├── test_scripts_to_convert.py
    └── test_lecture08_homework.py
```

> **Always run your homework on its own:** `pytest homework_08`. Running it together with `lecture_08` mixes up the two `pages` folders.

**Logins:** `student` / `secret123`, `locked` / `secret123`.

---

## Part 1: Extend the page objects (required)

Add these methods. Each should be a few lines.

| File | Method | What it does |
|---|---|---|
| `base_page.py` | `cart_count() -> int` | Reads the header link "Cart (3)" and returns `3` |
| `products_page.py` | `add_all_to_cart()` | Adds **every** product shown on the page (don't hard-code the names) |
| `cart_page.py` | `continue_shopping()` | Clicks **Continue shopping** |
| `cart_page.py` | `get_subtotal() -> float` | Reads "Subtotal: $79.98" and returns `79.98` |

---

## Part 2: Write tests with page objects (required)

In `test_lecture08_homework.py`, use the fixtures from `conftest.py` (`login_page`, `products_page`, `cart_page`, `checkout_page`).

**Rule: no locators in the test file.** Everything comes from page objects.

| Test | Steps and checks |
|---|---|
| `test_01_add_everything` | Add all products → header says "Cart (5)" and `cart_count()` is 5 → go to the cart → 5 rows, `get_subtotal()` is 113.95 |
| `test_02_sort_price_high_to_low` | Sort "Price (high to low)" → first product is "Jacket", prices are in descending order |
| `test_03_postcode_required` | Onesie in cart → checkout → enter first and last name but no postcode → "Postcode is required" |
| `test_04_last_name_required` | Same, but no last name → "Last name is required" |
| `test_05_order_one_onesie` | Same, all details → item total $7.99, tax $0.64, total $8.63 → place order → "Thank you for your order!" |
| `test_06_continue_shopping` | Go to the cart → Continue shopping → the Products heading is visible |

> **Hint:** tests 03–05 all start the same way. Write a fixture (e.g. `checkout_with_onesie`) that adds the Onesie, goes to the cart, clicks Checkout, and returns the `CheckoutPage`.

---

## Part 3: Convert scripts to POM (required)

Copy this into `tests/test_scripts_to_convert.py` and run it. Both tests pass.

```python
import re

from playwright.sync_api import Page, expect


def test_locked_user_script(page: Page):
    page.goto("/login.html")
    page.get_by_label("Username").fill("locked")
    page.get_by_label("Password").fill("secret123")
    page.get_by_role("button", name="Log in").click()
    expect(page.get_by_role("alert")).to_have_text("Sorry, this user has been locked out")
    expect(page).to_have_url(re.compile("login.html"))


def test_remove_one_of_three_script(page: Page):
    page.goto("/login.html")
    page.get_by_label("Username").fill("student")
    page.get_by_label("Password").fill("secret123")
    page.get_by_role("button", name="Log in").click()
    for name in ["Backpack", "Bike Light", "T-Shirt"]:
        page.locator(".product").filter(has_text=name).get_by_role("button", name="Add to cart").click()
    page.get_by_role("link", name="Cart").click()
    page.get_by_role("row").filter(has_text="Bike Light").get_by_role("button", name="Remove").click()
    expect(page.locator("tbody tr")).to_have_count(2)
    expect(page.locator("#subtotal")).to_have_text("Subtotal: $45.98")
```

Rewrite them in `test_lecture08_homework.py` as:

- `test_07_locked_user_stays_on_login`
- `test_08_remove_one_of_three` (also check the remaining items are `["Backpack", "T-Shirt"]`)

Use page objects and fixtures, with **no locators** in the tests.

---

## Part 4: Questions (required)

Answer as comments at the bottom of `test_lecture08_homework.py`:

1. If the button text "Add to cart" changed to "Add", which lines in your project would you need to change?
2. Why does `get_subtotal()` return a `float` instead of the text "Subtotal: $79.98"?
3. Why are there no `expect(...)` calls inside the page classes?

---

## Bonus (optional)

Make logging in return the next page, so a test can be written as one chain:

```python
products = LoginPage(page).open().login_successfully("student", "secret123")
products.add_to_cart("Jacket")
```

Add a method `login_successfully(username, password)` that logs in, waits for the products page, and returns a `ProductsPage`.

*Think about:* why is it better to add a new method than to change `login()` itself?

---

## Submission checklist

- [ ] 4 new page-object methods
- [ ] `test_lecture08_homework.py`: 8 passing tests, no locators
- [ ] 3 answers to Part 4
- [ ] (Optional) Bonus
