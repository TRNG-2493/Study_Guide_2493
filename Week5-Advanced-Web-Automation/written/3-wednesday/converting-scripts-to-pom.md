# Converting Scripts to POM

## Learning Objectives

By the end of this lesson you will be able to:

- Follow a safe, repeatable **refactoring procedure** that converts a flat Playwright script into a Page Object Model (POM) framework without changing what the tests verify.
- Analyse a flat script and **identify pages, components, actions, and state queries** hidden inside it.
- Apply the conversion in small steps: (0) establish a green baseline, (1) extract locators, (2) extract actions, (3) group by page, (4) introduce a base page and components, (5) deliver pages through fixtures, (6) slim down the tests, (7) remove duplication and hard-coded values.
- Use refactoring safeguards: run tests after every step, commit frequently, and keep a "behaviour must not change" mindset.
- Convert scripts from earlier in the week (dialogs, frames, tables, tabs) into page-object methods.
- Recognise and fix typical conversion mistakes (locator duplication, over-abstraction, lost waits, circular imports).
- Plan a conversion of a real project's UI tests, including Project 1.

---

## Why This Matters

In the previous lesson you learned what a Page Object Model is and what a well-designed one looks like. In real life you rarely get to start from a clean sheet. Far more often you inherit, or you yourself wrote last week, a pile of flat scripts that already work. Your task is to **improve the structure without breaking anything**. That is *refactoring*: changing the internal design of code while keeping its external behaviour identical.

This is directly the day's practical goal. The Wednesday trainee exercise asks you to **refactor your Project 1 UI tests into POM with data-driven JSON**. Project 1 is your QE Foundations portfolio piece, and a reviewer will judge it on structure as well as on correctness. Showing a clean "before" commit and a clean "after" commit in your Git history is a convincing way to demonstrate engineering skill.

It connects to this week's epic (structured, maintainable Playwright tests) in a very concrete way. Over Monday and Tuesday you wrote many scripts that handled dialogs, forms, dropdowns, frames, tables, tabs, and file transfer. Those scripts are *knowledge you already have*. Today you learn how to organise that knowledge so that a team can reuse it.

Refactoring is also a safety skill. Many people have broken working tests by "tidying up" without a plan, then spent hours working out what they changed. The procedure here is deliberately incremental so that if something breaks, you know exactly which small step caused it.

---

## The Concept

### 1. What exactly is refactoring?

**Refactoring** means restructuring existing code to improve readability, reuse, and maintainability **without changing its observable behaviour**. For tests, "observable behaviour" means: the same user journey is performed and the same expectations are checked, so a test that passed before still passes, and a test that detected a defect before still detects it.

Two rules make refactoring safe:

1. **Always start from green.** If a test is failing before you start, you cannot tell whether your changes broke it. Fix or quarantine it first.
2. **Take small steps and re-run after each.** A step is small if you can describe it in one sentence ("move the login locators into a class") and verify it by running the tests.

There is one extra rule specific to test code: **refactoring must not weaken the test.** A common accident is to delete an assertion while "simplifying". Compare the checks (assertions) before and after.

### 2. The starting point: a realistic flat script

Our running example continues on SauceDemo (`https://www.saucedemo.com`). Here is a longer flat script: a full purchase journey. Read it carefully; we will convert it step by step.

```python
# tests/test_purchase_flat.py        (STARTING POINT)
from playwright.sync_api import Page, expect


def test_purchase_two_items(page: Page):
    # --- login ---
    page.goto("https://www.saucedemo.com")
    page.locator("[data-test='username']").fill("standard_user")
    page.locator("[data-test='password']").fill("secret_sauce")
    page.locator("[data-test='login-button']").click()
    expect(page).to_have_url("https://www.saucedemo.com/inventory.html")

    # --- add items ---
    page.locator("[data-test='add-to-cart-sauce-labs-backpack']").click()
    page.locator("[data-test='add-to-cart-sauce-labs-bike-light']").click()
    expect(page.locator("[data-test='shopping-cart-badge']")).to_have_text("2")

    # --- cart ---
    page.locator("[data-test='shopping-cart-link']").click()
    expect(page).to_have_url("https://www.saucedemo.com/cart.html")
    names = page.locator("[data-test='inventory-item-name']").all_inner_texts()
    assert names == ["Sauce Labs Backpack", "Sauce Labs Bike Light"]
    page.locator("[data-test='checkout']").click()

    # --- checkout step one ---
    page.locator("[data-test='firstName']").fill("Asha")
    page.locator("[data-test='lastName']").fill("Patel")
    page.locator("[data-test='postalCode']").fill("560001")
    page.locator("[data-test='continue']").click()

    # --- checkout overview ---
    expect(page).to_have_url("https://www.saucedemo.com/checkout-step-two.html")
    page.locator("[data-test='finish']").click()

    # --- confirmation ---
    expect(page.locator("[data-test='complete-header']")).to_have_text("Thank you for your order!")


def test_checkout_requires_first_name(page: Page):
    page.goto("https://www.saucedemo.com")
    page.locator("[data-test='username']").fill("standard_user")
    page.locator("[data-test='password']").fill("secret_sauce")
    page.locator("[data-test='login-button']").click()
    page.locator("[data-test='add-to-cart-sauce-labs-backpack']").click()
    page.locator("[data-test='shopping-cart-link']").click()
    page.locator("[data-test='checkout']").click()
    page.locator("[data-test='continue']").click()
    expect(page.locator("[data-test='error']")).to_contain_text("First Name is required")
```

(SauceDemo's `data-test` attributes were current when this lesson was written. Always inspect the live page, since public demo sites can change.)

Counting up the pain: the login block is duplicated; the product ids are hard-coded; URLs are full strings; the first test is a long monologue mixing six pages; and the second test is a copy of half of the first.

### 3. Step 0: Establish a green baseline and a safety net

Before changing a line:

1. Run the tests: `pytest tests/test_purchase_flat.py -v`. Everything must pass. If anything is red, stop and fix it (or mark it `xfail` with a reason).
2. Commit: `git add -A && git commit -m "Baseline: flat purchase tests (green)"`.
3. Run them a few times (`pytest --count`-style repetition is optional; running manually 2-3 times is enough) to make sure they are not already flaky. Refactoring a flaky test makes it impossible to judge your change.
4. Record the **assertions list**; this is your "do not lose these" checklist:
   - URL is inventory after login.
   - Cart badge shows 2.
   - Cart URL is `/cart.html`.
   - Cart item names equal the two product names in order.
   - Overview URL is checkout-step-two.
   - Confirmation header says "Thank you for your order!".
   - Missing first name shows an error containing "First Name is required".

Having the checklist means that at the end you can tick each item and be confident the tests are no weaker.

Also set up the project skeleton from the previous lesson: `pytest.ini` with `base_url`, `pages/` with `__init__.py`, and a `conftest.py` with the `data-test` configuration:

```ini
# pytest.ini
[pytest]
base_url = https://www.saucedemo.com
pythonpath = .
testpaths = tests
```

```python
# conftest.py (so far)
import pytest


@pytest.fixture(scope="session", autouse=True)
def configure_test_id(playwright):
    playwright.selectors.set_test_id_attribute("data-test")
```

Run the tests again; they still pass because nothing else changed (the flat script still uses CSS attribute selectors, which are unaffected). Commit.

### 4. Step 1: Analyse the script and map pages

Read the script and draw boundaries wherever the **page changes** or where a distinct **region** (header, form) is acted upon. Make a table:

| Script section | Page / component | Actions seen | State read |
|---|---|---|---|
| login | `LoginPage` | open, fill username, fill password, click login | error message |
| add items | `InventoryPage` | add product to cart | cart badge (in header) |
| cart | `CartPage` | open cart (from header), read items, checkout | item names, URL |
| checkout step one | `CheckoutInfoPage` | fill first/last/postal, continue | error message |
| overview | `CheckoutOverviewPage` | finish | URL |
| confirmation | `CheckoutCompletePage` | none | completion header |
| header (on many pages) | `Header` component | open cart | cart count |

This table is your **design**. Each row is a candidate class; each "action" is a candidate method; each "state read" a candidate query method. Do it on paper first. A design mistake is much cheaper to fix before code exists.

Naming tip: name pages by the **screen the user sees**, not by the URL. `CheckoutInfoPage` is better than `CheckoutStepOnePage` because "step one" depends on a number that could change.

### 5. Step 2: Extract locators into page classes (no behaviour change yet)

Take one page at a time, starting with the one at the **top of the journey** (login). Create the class with its locators and a minimal method, and *use it in the flat test*, replacing only the lines for that page. Run the tests.

```python
# pages/login_page.py (first version)
from playwright.sync_api import Page


class LoginPage:
    def __init__(self, page: Page):
        self.page = page
        self.username_input = page.get_by_test_id("username")
        self.password_input = page.get_by_test_id("password")
        self.login_button = page.get_by_test_id("login-button")
        self.error_message = page.get_by_test_id("error")

    def open(self):
        self.page.goto("/")

    def login_as(self, username, password):
        self.username_input.fill(username)
        self.password_input.fill(password)
        self.login_button.click()
```

Now edit **only the login portion** of the first test:

```python
from pages.login_page import LoginPage

def test_purchase_two_items(page: Page):
    # --- login ---
    login_page = LoginPage(page)
    login_page.open()
    login_page.login_as("standard_user", "secret_sauce")
    expect(page).to_have_url("https://www.saucedemo.com/inventory.html")
    # ... the rest unchanged ...
```

Run: `pytest tests/test_purchase_flat.py -v`. Green? Commit: "Extract LoginPage".

What did we do, exactly?

- We **moved** three locators and a method into a class (the body was copied verbatim, only the selector syntax changed from `locator("[data-test='username']")` to the equivalent `get_by_test_id("username")`).
- `page.goto("/")` relies on `base_url`. That is the one behavioural dependency we introduced, which is why the baseline step had us configure `pytest.ini` first.
- We did *not* touch the assertions.

Repeat the same micro-cycle for each page: create the class, replace the lines, run, commit. Do not convert everything at once. Here are the remaining classes:

```python
# pages/inventory_page.py
from playwright.sync_api import Page


class InventoryPage:
    def __init__(self, page: Page):
        self.page = page
        self.items = page.get_by_test_id("inventory-item")

    def add_product_to_cart(self, product_name: str):
        self.items.filter(has_text=product_name).get_by_role("button", name="Add to cart").click()
```

```python
# pages/components/header.py
from playwright.sync_api import Page


class Header:
    def __init__(self, page: Page):
        self.page = page
        self.cart_link = page.get_by_test_id("shopping-cart-link")
        self.cart_badge = page.get_by_test_id("shopping-cart-badge")

    def open_cart(self):
        self.cart_link.click()
```

```python
# pages/cart_page.py
from playwright.sync_api import Page


class CartPage:
    def __init__(self, page: Page):
        self.page = page
        self.item_names = page.get_by_test_id("inventory-item-name")
        self.checkout_button = page.get_by_test_id("checkout")

    def get_item_names(self) -> list[str]:
        return self.item_names.all_inner_texts()

    def proceed_to_checkout(self):
        self.checkout_button.click()
```

```python
# pages/checkout_info_page.py
from playwright.sync_api import Page


class CheckoutInfoPage:
    def __init__(self, page: Page):
        self.page = page
        self.first_name = page.get_by_test_id("firstName")
        self.last_name = page.get_by_test_id("lastName")
        self.postal_code = page.get_by_test_id("postalCode")
        self.continue_button = page.get_by_test_id("continue")
        self.error_message = page.get_by_test_id("error")

    def fill_details(self, first: str, last: str, postal: str):
        self.first_name.fill(first)
        self.last_name.fill(last)
        self.postal_code.fill(postal)

    def continue_to_overview(self):
        self.continue_button.click()
```

```python
# pages/checkout_overview_page.py
from playwright.sync_api import Page


class CheckoutOverviewPage:
    def __init__(self, page: Page):
        self.page = page
        self.finish_button = page.get_by_test_id("finish")

    def finish(self):
        self.finish_button.click()
```

```python
# pages/checkout_complete_page.py
from playwright.sync_api import Page


class CheckoutCompletePage:
    def __init__(self, page: Page):
        self.page = page
        self.header = page.get_by_test_id("complete-header")
```

After converting all pages (committing after each) the first test is:

```python
def test_purchase_two_items(page: Page):
    login_page = LoginPage(page)
    login_page.open()
    login_page.login_as("standard_user", "secret_sauce")
    expect(page).to_have_url("**/inventory.html")

    inventory = InventoryPage(page)
    inventory.add_product_to_cart("Sauce Labs Backpack")
    inventory.add_product_to_cart("Sauce Labs Bike Light")
    header = Header(page)
    expect(header.cart_badge).to_have_text("2")

    header.open_cart()
    expect(page).to_have_url("**/cart.html")
    cart = CartPage(page)
    assert cart.get_item_names() == ["Sauce Labs Backpack", "Sauce Labs Bike Light"]
    cart.proceed_to_checkout()

    info = CheckoutInfoPage(page)
    info.fill_details("Asha", "Patel", "560001")
    info.continue_to_overview()

    expect(page).to_have_url("**/checkout-step-two.html")
    CheckoutOverviewPage(page).finish()

    expect(CheckoutCompletePage(page).header).to_have_text("Thank you for your order!")
```

Notice that we changed URL assertions from full strings (`https://www.saucedemo.com/cart.html`) to globs (`**/cart.html`) so they no longer hard-code the host. That is a small *behavioural* change in strictness, though an intentional and safe one: the path is still verified. Be conscious whenever you do this.

All selectors are gone from the test. Still, the test is long and has a lot of "construct a page object" noise. Next steps remove it.

### 6. Step 3: Introduce a `BasePage` and compose components

Look for things every page class repeats: `self.page = page`. Also, every authenticated page contains the header. Create:

```python
# pages/base_page.py
from playwright.sync_api import Page, expect


class BasePage:
    PATH = ""     # each page overrides with its own URL path fragment

    def __init__(self, page: Page):
        self.page = page

    def expect_loaded(self) -> None:
        if self.PATH:
            expect(self.page).to_have_url(f"**{self.PATH}")
```

- `PATH = ""` is a class attribute; each child overrides it (`PATH = "/cart.html"`).
- `expect_loaded()` is a **readiness check** shared by all pages: when you construct a page after navigation, call it so the next step cannot begin on the wrong page. Defining it once in the base gives every page a verification of "we are where we think we are" for free.

Update the classes to inherit and set `PATH`. Example for `CartPage`:

```python
from pages.base_page import BasePage
from pages.components.header import Header


class CartPage(BasePage):
    PATH = "/cart.html"

    def __init__(self, page):
        super().__init__(page)
        self.header = Header(page)
        self.item_names = page.get_by_test_id("inventory-item-name")
        self.checkout_button = page.get_by_test_id("checkout")
```

- `class CartPage(BasePage):` inherits.
- `super().__init__(page)` runs `BasePage.__init__`.
- `self.header = Header(page)` composes the header component, so tests write `cart.header.cart_count()`.

Run the tests; commit. This step is "pure restructuring": no test line needs to change if you kept names the same.

### 7. Step 4: Make navigation methods return the next page

Currently the test has to know "after login I must construct `InventoryPage`". Move that knowledge into the page methods so the code reads like a journey. This is also where the readiness check pays off.

```python
# pages/login_page.py (final shape)
from pages.base_page import BasePage
from pages.inventory_page import InventoryPage


class LoginPage(BasePage):
    PATH = "/"

    def __init__(self, page):
        super().__init__(page)
        self.username_input = page.get_by_test_id("username")
        self.password_input = page.get_by_test_id("password")
        self.login_button = page.get_by_test_id("login-button")
        self.error_message = page.get_by_test_id("error")

    def open(self) -> "LoginPage":
        self.page.goto(self.PATH)
        return self

    def login_as(self, username: str, password: str) -> None:
        self.username_input.fill(username)
        self.password_input.fill(password)
        self.login_button.click()

    def login_successfully(self, username: str, password: str) -> InventoryPage:
        self.login_as(username, password)
        inventory = InventoryPage(self.page)
        inventory.expect_loaded()
        return inventory

    def get_error_message(self) -> str:
        return self.error_message.inner_text()
```

And the others, abbreviated:

```python
# InventoryPage
    def add_product_to_cart(self, product_name: str) -> "InventoryPage":
        self.items.filter(has_text=product_name).get_by_role("button", name="Add to cart").click()
        return self

    def open_cart(self) -> CartPage:
        self.header.open_cart()
        cart = CartPage(self.page)
        cart.expect_loaded()
        return cart

# CartPage
    def proceed_to_checkout(self) -> CheckoutInfoPage:
        self.checkout_button.click()
        info = CheckoutInfoPage(self.page)
        info.expect_loaded()
        return info

# CheckoutInfoPage
    def continue_to_overview(self) -> CheckoutOverviewPage:
        self.continue_button.click()
        overview = CheckoutOverviewPage(self.page)
        overview.expect_loaded()
        return overview

    def continue_expecting_error(self) -> "CheckoutInfoPage":
        self.continue_button.click()
        return self

# CheckoutOverviewPage
    def finish(self) -> CheckoutCompletePage:
        self.finish_button.click()
        complete = CheckoutCompletePage(self.page)
        complete.expect_loaded()
        return complete
```

For these readiness checks to work, every page class sets its `PATH`: `InventoryPage.PATH = "/inventory.html"`, `CartPage.PATH = "/cart.html"`, `CheckoutInfoPage.PATH = "/checkout-step-one.html"`, `CheckoutOverviewPage.PATH = "/checkout-step-two.html"`, and `CheckoutCompletePage.PATH = "/checkout-complete.html"`. Also change `CheckoutInfoPage.fill_details` to end with `return self`, so it can be chained.

Explanation of design choices:

- Methods that move to a new screen **return that screen's object** and call its readiness check. This replaces sprinkled `expect(page).to_have_url(...)` lines in tests with a single, consistent place.
- A method that stays on the same screen returns `self` (enabling chains) or `None`.
- `continue_expecting_error` is separate from `continue_to_overview` because the *outcome differs* (stay vs. navigate). Splitting by outcome is better than a method with a flag argument.
- Import cycles: `LoginPage` imports `InventoryPage`; `InventoryPage` imports `CartPage`; `CartPage` imports `CheckoutInfoPage`... all go *forward* along the journey, so no cycles arise. If a page needs to go *back* (for example `CartPage.continue_shopping()` returning `InventoryPage`), import inside the method body to avoid a loop, or accept `Page` and return a lazily imported class.

The purchase test now reads:

```python
def test_purchase_two_items(login_page):
    inventory = login_page.login_successfully("standard_user", "secret_sauce")
    inventory.add_product_to_cart("Sauce Labs Backpack").add_product_to_cart("Sauce Labs Bike Light")
    expect(inventory.header.cart_badge).to_have_text("2")

    cart = inventory.open_cart()
    assert cart.get_item_names() == ["Sauce Labs Backpack", "Sauce Labs Bike Light"]

    complete = (
        cart.proceed_to_checkout()
        .fill_details("Asha", "Patel", "560001")
        .continue_to_overview()
        .finish()
    )
    expect(complete.header).to_have_text("Thank you for your order!")
```

(This assumes `fill_details` returns `self`, so we can chain it.) The URL checks that used to be in the test (cart URL, overview URL) are now inside `expect_loaded()` calls: **the assertions are not lost; they moved.** This is exactly where the checklist from Step 0 matters: confirm each original check still happens somewhere.

The parentheses around the chain allow splitting a long expression over multiple lines without backslashes.

### 8. Step 5: Deliver pages with fixtures

The tests still start with `login_page` (a fixture). Create it, plus a ready-made logged-in starting point, in `conftest.py`:

```python
# conftest.py (final shape for this lesson)
import pytest

from pages.login_page import LoginPage


@pytest.fixture(scope="session", autouse=True)
def configure_test_id(playwright):
    playwright.selectors.set_test_id_attribute("data-test")


@pytest.fixture
def login_page(page) -> LoginPage:
    return LoginPage(page).open()


@pytest.fixture
def inventory_page(login_page):
    return login_page.login_successfully("standard_user", "secret_sauce")
```

Now the second test (missing first name) becomes:

```python
def test_checkout_requires_first_name(inventory_page):
    info = inventory_page.add_product_to_cart("Sauce Labs Backpack").open_cart().proceed_to_checkout()
    info.continue_expecting_error()
    expect(info.error_message).to_contain_text("First Name is required")
```

The entire login block disappeared from the test, replaced by the `inventory_page` fixture. If tomorrow the standard user changes, one fixture changes. (In the data-driven lesson we move the credentials to a JSON file.)

### 9. Step 6: Remove remaining duplication and magic values

Search for repeated strings and numbers:

- Product names: introduce constants or, better, read them from JSON (later lesson).
- Credentials: keep them in a `data/users.json`.
- Waiting: if you see `time.sleep`, replace with `expect` or `wait_for_url`.
- Repeated flows: if three tests all do `add backpack -> open cart -> checkout`, create a helper or fixture `checkout_info_page`.

```python
@pytest.fixture
def checkout_info_page(inventory_page):
    return inventory_page.add_product_to_cart("Sauce Labs Backpack").open_cart().proceed_to_checkout()
```

Now the second test shrinks again:

```python
def test_checkout_requires_first_name(checkout_info_page):
    checkout_info_page.continue_expecting_error()
    expect(checkout_info_page.error_message).to_contain_text("First Name is required")
```

### 10. Step 7: Review against the checklist

Open the Step 0 checklist and tick each assertion:

| Original check | Where it lives now |
|---|---|
| inventory URL after login | `LoginPage.login_successfully` -> `InventoryPage.expect_loaded()` |
| cart badge 2 | test, `expect(inventory.header.cart_badge)` |
| cart URL | `CartPage.expect_loaded()` via `open_cart()` |
| cart names | test, `assert cart.get_item_names() == [...]` |
| overview URL | `CheckoutOverviewPage.expect_loaded()` via `continue_to_overview()` |
| confirmation text | test, `expect(complete.header)` |
| first-name error | test, `expect(info.error_message)` |

Finally **mutation-test your refactor**: deliberately break the application expectation (e.g., change `"2"` to `"3"` in the badge check) and confirm the test fails for the right reason. A refactor that cannot fail is dangerous.

### 11. Converting other kinds of scripts

You also have scripts from Monday and Tuesday. The same method applies; here is how to think about each category.

| Earlier script type | How it becomes POM |
|---|---|
| **Dialog handling** (alerts, confirms) | A page method that registers the handler *before* the triggering click: `def delete_account(self, accept=True): self.page.once("dialog", lambda d: d.accept() if accept else d.dismiss()); self.delete_button.click()`. |
| **Form controls** (radio, checkbox, dropdown) | Intent methods: `choose_shipping("Express")`, `accept_terms()`. Hide `check()` / `select_option()` inside. |
| **Keyboard and mouse actions** | Methods named for outcomes: `reorder_item(from_index, to_index)` wrapping `drag_to`. |
| **Auto-suggest** | `search_for(term)`, `pick_suggestion(text)`; keep the wait for the list inside the method. |
| **Frames** | Store a `FrameLocator` in the page: `self.editor = page.frame_locator("#editor")`; methods use `self.editor.get_by_role(...)`. |
| **Web tables** | A `TableComponent` with `row_for(text)`, `cell(row, col_name)`; page methods use it. |
| **Date pickers** | `select_date(date_obj)` hides the calendar clicking. |
| **Multiple tabs** | A method that returns the **new page object**: `with self.page.context.expect_page() as new_tab: self.link.click()` then `return HelpPage(new_tab.value)`. |
| **Shadow DOM** | Playwright locators pierce open shadow roots automatically, so the page class is unchanged. |
| **File upload/download** | `upload_resume(path)`, `download_invoice() -> Path` using `expect_download()`. |

For the multi-tab example, notice how **the page object boundary follows the browser tab**: the new page gets its own `Page` instance and its own page class.

### 12. A conversion checklist you can reuse

1. Green baseline, committed. Assertions list written.
2. `pytest.ini` has `base_url`; `pythonpath = .`; `conftest.py` sets the test-id attribute.
3. Table of pages/components/actions/state written.
4. Convert page by page; run and commit after each.
5. Introduce `BasePage` once at least two pages share code.
6. Extract components for repeated regions (header, footer, modals, tables).
7. Navigation methods return the next page; readiness checks inside.
8. Fixtures provide starting points; tests do not construct page objects (except for secondary pages).
9. Remove hard-coded data (next lesson: JSON).
10. Ticks on the assertions list; mutation test.
11. Update documentation (`README`: how to run, structure, conventions).

---

## Code Examples

### The final structure after conversion

```
saucedemo_framework/
├── pytest.ini
├── conftest.py
├── pages/
│   ├── __init__.py
│   ├── base_page.py
│   ├── login_page.py
│   ├── inventory_page.py
│   ├── cart_page.py
│   ├── checkout_info_page.py
│   ├── checkout_overview_page.py
│   ├── checkout_complete_page.py
│   └── components/
│       ├── __init__.py
│       └── header.py
└── tests/
    ├── test_login.py
    └── test_purchase.py
```

### Final `tests/test_purchase.py`

```python
import pytest
from playwright.sync_api import expect


def test_purchase_two_items(inventory_page):
    inventory_page.add_product_to_cart("Sauce Labs Backpack").add_product_to_cart("Sauce Labs Bike Light")
    expect(inventory_page.header.cart_badge).to_have_text("2")

    cart = inventory_page.open_cart()
    assert cart.get_item_names() == ["Sauce Labs Backpack", "Sauce Labs Bike Light"]

    complete = (
        cart.proceed_to_checkout()
        .fill_details("Asha", "Patel", "560001")
        .continue_to_overview()
        .finish()
    )
    expect(complete.header).to_have_text("Thank you for your order!")


def test_checkout_requires_first_name(checkout_info_page):
    checkout_info_page.continue_expecting_error()
    expect(checkout_info_page.error_message).to_contain_text("First Name is required")
```

### Converting a dialog script (from Monday)

Flat:

```python
def test_remove_confirmation(page):
    page.goto("/settings")
    page.once("dialog", lambda dialog: dialog.accept())
    page.locator("#delete").click()
    expect(page.locator("#status")).to_have_text("Deleted")
```

POM:

```python
class SettingsPage(BasePage):
    PATH = "/settings"

    def __init__(self, page):
        super().__init__(page)
        self.delete_button = page.locator("#delete")
        self.status = page.locator("#status")

    def delete_account(self, accept: bool = True) -> "SettingsPage":
        self.page.once("dialog", lambda dialog: dialog.accept() if accept else dialog.dismiss())
        self.delete_button.click()
        return self
```

- `page.once("dialog", handler)` registers a one-time handler; it must be registered *before* the action that triggers the dialog, because Playwright auto-dismisses dialogs that have no handler.
- `dialog.accept() if accept else dialog.dismiss()` is a **conditional expression**: it accepts when `accept` is `True`, otherwise dismisses.
- The test now says `settings.delete_account()`; the dialog detail is invisible and reusable.

### Converting a new-tab script (from Tuesday)

```python
class FooterComponent:
    def __init__(self, page):
        self.page = page
        self.help_link = page.get_by_role("link", name="Help")

    def open_help(self) -> "HelpPage":
        with self.page.context.expect_page() as new_page_info:
            self.help_link.click()
        help_page = HelpPage(new_page_info.value)
        help_page.page.wait_for_load_state()
        return help_page
```

- `with ... as new_page_info:` is a **context manager**: it starts listening for a new page, runs the indented click, and finishes when the block exits.
- `new_page_info.value` is the new `Page`.
- The method returns a page object bound to the **new tab**, so subsequent calls drive that tab.

---

## Real-World Scenarios

**Scenario 1: Legacy suite rescue.** A company inherits 300 flat scripts recorded with a code-generation tool. The team converts login first (the highest duplication), saving thousands of lines in one week, then converts the other pages in order of how often they are used. They never stop running the suite while doing so, because each step is small and green.

**Scenario 2: Mid-sprint redesign.** The product team announces a new navigation bar. Because the header is a component class used by all pages, the QE team adjusts it in one file the same afternoon and ships the tests with the redesign.

**Scenario 3: Pull-request review.** A reviewer asks for a "before" and "after" in the PR description. The developer includes the checklist table from Step 7. The reviewer can approve quickly because the table proves that no assertion was lost.

**Scenario 4: Incremental adoption.** A team cannot afford a big-bang rewrite. They introduce the rule "any test you touch gets converted to POM", and the framework improves steadily over a quarter. This "boy scout rule" (leave the code cleaner than you found it) is how most real-world conversions succeed.

---

## Common Pitfalls and Best Practices

**Pitfalls**

1. **Big-bang rewrite.** Converting everything at once and only then running tests. When something fails you cannot tell why. Convert page by page.
2. **Refactoring on red.** Starting with failing tests. Establish green first.
3. **Silently dropping assertions.** Tick the checklist. Every original check must still exist (moved is fine, deleted is not).
4. **Copying selectors from the flat script but changing their meaning.** For example replacing `locator(".title")` with `get_by_test_id("title")` is only safe if both match the same element. Verify in the browser.
5. **Losing waits.** In flat scripts the explicit `expect(page).to_have_url(...)` after a click often doubles as a synchronisation point. If you move or remove it, the next action may run before the page is ready. Keep a readiness check (`expect_loaded()`) after navigation.
6. **Over-abstraction.** Creating `ClickableElement`, `InputBox`, and `ButtonWrapper` classes around single Playwright calls. Playwright's `Locator` is already a good abstraction.
7. **Method with boolean flags** (`continue_(expect_error=True)`). Prefer two intent-named methods.
8. **Circular imports** between pages. Navigate forward at module level; import lazily for back-navigation.
9. **Forgetting `super().__init__`.**
10. **Leaving the flat copy around.** Delete the old script once the POM version passes; stale duplicates rot and confuse reviewers.
11. **Hard-coding `base_url` in page objects.** Use relative paths and configure the host once.

**Best practices**

- **Commit after every green step**, using messages such as "Extract LoginPage", "Add Header component", "Return next page from login".
- Convert **top-down** along the journey (login, inventory, cart, checkout) so each new class has a known entry point.
- Keep **tests thin and page objects thick**, but keep *decisions* (assertions) in tests.
- Name methods in the **language of the business**.
- Use `pytest -x -q` (stop at first failure, quiet output) for quick feedback while refactoring, and `--lf` (last failed) to re-run only failures.
- Write the README section "How the framework is organised" as you go; the habit keeps design honest.

---

## Mini Practice Exercises

**Exercise 1: map the pages.**
Given this flat snippet, draw the page/action table (Step 1): login, open a product's detail page by clicking its name, click "Add to cart", click "Back to products". *Hint:* there is a `ProductDetailPage` with `add_to_cart()` and `back_to_products()` that returns `InventoryPage`.

**Exercise 2: convert in three commits.**
Take the flat `test_login_and_sort_by_price_low_to_high` test from the previous lesson and convert it in three separate commits: (1) `LoginPage`, (2) `InventoryPage` with `sort_by` and `get_prices`, (3) fixtures. Run the tests after each commit.
*Solution outline:* Compare with the "AFTER" code in the Page Object Model lesson.

**Exercise 3: the assertion ledger.**
Write the assertions checklist for a flat script of your own (from Monday or Tuesday) and, after converting, fill a "where it lives now" column. Peer-review a classmate's table.

**Exercise 4: back-navigation.**
Add `continue_shopping()` to `CartPage` that returns an `InventoryPage` without causing a circular import.
*Solution:*
```python
def continue_shopping(self):
    from pages.inventory_page import InventoryPage   # imported here to avoid a cycle
    self.page.get_by_test_id("continue-shopping").click()
    inventory = InventoryPage(self.page)
    inventory.expect_loaded()
    return inventory
```

**Exercise 5: mutation test.**
After your refactor, change one expected value in the test (for example, expected cart count from 2 to 3). Confirm the failure message points to the right line, then revert.

**Exercise 6 (Project 1 link):** Pick the two longest UI tests in your Project 1 repository. Apply the checklist. Submit a short note (5-8 lines) in your repository's `docs/refactoring-notes.md` describing the "before" line count, the "after" line count, and which assertions moved where.

---

## Summary / Key Takeaways

- **Refactoring** changes structure, not behaviour. Always start green, use small steps, commit often, and never weaken assertions.
- Convert by **analysing the script into pages, components, actions, and state queries**, then extracting one page at a time.
- The standard sequence: baseline, design table, extract locators and actions per page, add `BasePage` and components, return next pages from navigation methods, deliver starting points through fixtures, remove magic values, verify against the assertion checklist.
- Assertions are **moved**, often into readiness checks (`expect_loaded`), not deleted.
- Earlier skills (dialogs, frames, tables, tabs, file transfer) fit naturally into page-object methods.
- Avoid big-bang rewrites, over-abstraction, circular imports, and lost waits.
- A converted suite is shorter, more readable, and cheaper to maintain, which is exactly the Project 1 quality bar.

---

## External Resources

- Playwright for Python, "Page object models": https://playwright.dev/python/docs/pom
- Playwright for Python, "Writing tests" and "Auto-waiting" (why readiness checks work): https://playwright.dev/python/docs/actionability
- Martin Fowler, "Refactoring" (catalogue and principles): https://refactoring.com/
