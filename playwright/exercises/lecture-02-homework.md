# Lecture 2: Homework

**Time:** 45–60 minutes
**Goal:** practise built-in locators, filtering and chaining.

## Setup

1. Copy `locators_practice.html` from the Lecture 2 demo into your `homework/` folder.
2. Create `homework/test_lecture02_homework.py` with the starter code below.
3. Open `locators_practice.html` in your browser so you can see the page while you work. Right-click → **Inspect** to look at the HTML.

## Starter code

```python
from pathlib import Path

import pytest
from playwright.sync_api import Page, expect

PRACTICE_PAGE = Path(__file__).parent / "locators_practice.html"


@pytest.fixture
def store(page: Page) -> Page:
    page.goto(PRACTICE_PAGE.as_uri())
    return page


# ================= PART 1: Built-in locators =================
# Rule: use ONLY get_by_role, get_by_label, get_by_placeholder,
#       get_by_text, get_by_alt_text, get_by_title or get_by_test_id.
#       No page.locator() in Part 1!

def test_01_products_link(store: Page):
    # TODO: the "Products" LINK in the navigation is visible
    pass


def test_02_recent_orders_heading(store: Page):
    # TODO: the "Recent orders" heading is visible
    pass


def test_03_password_by_label(store: Page):
    # TODO: find the Password field by its label; check it is empty
    # Hint: expect(...).to_be_empty()
    pass


def test_04_email_by_placeholder(store: Page):
    # TODO: find the Email field by its placeholder; check it is visible
    pass


def test_05_remember_me_checkbox(store: Page):
    # TODO: the "Remember me" checkbox is NOT checked
    # Hint: expect(...).not_to_be_checked()
    pass


def test_06_logo_by_alt_text(store: Page):
    # TODO: find the logo image by its alt text; check it is attached
    # Hint: expect(...).to_be_attached()
    pass


def test_07_shipping_icon_by_title(store: Page):
    # TODO: find the shipping icon by its title; check it is visible
    pass


def test_08_checkout_by_test_id(store: Page):
    # TODO: find the Checkout button by its test id; check it is visible
    pass


def test_09_copyright_text(store: Page):
    # TODO: the footer text "2026 Practice Store" is visible
    pass


def test_10_privacy_link(store: Page):
    # TODO: the "Privacy policy" link is visible
    pass


# ================= PART 2: Filtering and chaining =================
# You may use page.locator(".product") as a starting point here.

def test_a_tshirt_price(store: Page):
    # TODO: in the T-Shirt product card, the price is "$15.99"
    # Hint: filter(has_text=...) then find ".price" inside it
    pass


def test_b_in_stock_count(store: Page):
    # TODO: exactly 3 products are "In stock"
    # Hint: expect(...).to_have_count(3)
    pass


def test_c_order_status(store: Page):
    # TODO: in the orders table, Ben Carter's order status is "Pending"
    # Hint: find the row, then the cells inside it. Which nth() is Status?
    pass


def test_d_first_and_last(store: Page):
    # TODO: the LAST product name is "Jacket"
    # TODO: the FIRST product price is "$29.99"
    pass


def test_e_bike_light_disabled(store: Page):
    # TODO: the Bike Light's "Add to cart" button is disabled
    # Hint: expect(...).to_be_disabled()
    pass


# ================= PART 2 QUESTION =================
# Answer as a comment:
# What happens if you run
#     store.get_by_role("button", name="Add to cart").click()
# and how would you change it to click ONLY the Jacket's button?
```

---

## Part 1: Built-in locators (required)

Complete tests 01–10 using **only built-in locators**. Run:

```bash
pytest homework -v -k "test_0 or test_10"
```

All 10 should pass.

> **Tip:** if a test fails with "strict mode violation", your locator matches more than one element. Make it more specific, for example by using `get_by_role` with a `name`, or `exact=True`.

---

## Part 2: Filtering and chaining (required)

Complete tests a–e and answer the question at the bottom of the file. Run:

```bash
pytest homework -v
```

All 15 tests should pass.

---

## Part 3: Bonus (optional) — a live website

Create `homework/test_lecture02_bonus.py` and write tests for **the-internet.herokuapp.com**:

1. On `/login`: the **Username** and **Password** fields (find them by label) and the **Login** button (by role) are visible.
2. On `/tables`: in the first table (`#table1`), the row for **Doe** has the email **jdoe@hotmail.com**.
   *Hint:* find the table, then the row with `filter`, then the cell with `nth`.
3. On `/tables`: the first table has **4** rows in its body.

---

## Submission checklist

- [ ] Part 1: 10 passing tests, built-in locators only
- [ ] Part 2: 5 passing tests
- [ ] Part 2 question answered as a comment
- [ ] (Optional) Part 3 bonus tests
