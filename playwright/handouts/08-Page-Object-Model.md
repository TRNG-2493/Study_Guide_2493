# 08 — Page Object Model

> **Before you start**
>
> - **By the end you can:** explain why POM helps, organise a project into `pages/` and `tests/`, write page classes with a base page, convert a script-style test to POM, and get page objects from fixtures.
> - **Practice site:** Swag Labs — <https://www.saucedemo.com/> (`standard_user` / `secret_sauce`; `locked_out_user` is locked out).
> - **Create:** a folder `lecture08/` and copy in your Lecture 7 `pytest.ini` and `conftest.py` (base URL, `data-test` setting, `log_in`, `user_state`). Then add two empty folders: `pages/` (with an empty `__init__.py`) and `tests/`.
> - **Run tests with:** `pytest -v` from inside `lecture08/`

| Swag Labs page | URL | What's there |
|---|---|---|
| Login | `/` | Username, Password, **Login** |
| Products | `/inventory.html` | 6 products with **Add to cart**, a sort dropdown |
| Cart | `/cart.html` | Items, **Remove**, **Continue Shopping**, **Checkout** |
| Checkout | `/checkout-step-one.html` → `two` → `/checkout-complete.html` | Name + postcode → summary with 8% tax → "Thank you for your order!" |

Every page after login has a header with a **cart icon** (`shopping-cart-link`) and an **Open Menu** button containing **Logout**.

---

## Topic 1 — Why POM, and the base page

### Definition

The **Page Object Model (POM)** gives each page of the site its own class that knows **where things are** (locators) and **what you can do there** (methods). Tests then describe *what* happens; page classes handle *how*. Parts every page shares go in a **base page** class.

### Key ideas

| Script-style problem | POM fix |
|---|---|
| Login lines copied into every test | One `login()` method |
| "Login" renamed → edit every test | Fix one line in `LoginPage` |
| Must read locators to understand a test | Tests read like steps |

| Folder | Contains | Doesn't contain |
|---|---|---|
| `pages/` | Locators, actions | Assertions |
| `tests/` | Steps, assertions | Locators |

### Worked example — build the base page

**Step 1.** Create `pages/base_page.py` with the class and the `page`:

```python
from playwright.sync_api import Page


class BasePage:
    URL = "/"

    def __init__(self, page: Page):
        self.page = page
```

**Step 2.** Add the shared header locators:

```python
        self.cart_link = page.get_by_test_id("shopping-cart-link")
        self.cart_badge = page.get_by_test_id("shopping-cart-badge")
        self.menu_button = page.get_by_role("button", name="Open Menu")
        self.logout_link = page.get_by_role("link", name="Logout")
```

**Step 3.** Add `open()` — returning `self` lets you write `LoginPage(page).open()`:

```python
    def open(self):
        self.page.goto(self.URL)
        return self
```

**Step 4.** Add the shared actions:

```python
    def go_to_cart(self):
        self.cart_link.click()

    def log_out(self):
        self.menu_button.click()
        self.logout_link.click()
```

> **Predict:** the locators are created in `__init__`, before the page is opened. Why doesn't that cause an error?

### Checkpoint

`python -c "from pages.base_page import BasePage; print(BasePage.URL)"` (run from `lecture08/`) prints `/`.

### Your turn

1. Add a `reset_app_state()` method that opens the menu and clicks **Reset App State**.
2. List three things that should **not** go in `BasePage`.
   *Hint: only what every page shares.*

---

## Topic 2 — Building a page class

### Definition

A page class **inherits** from `BasePage`, sets its own `URL`, defines its locators in `__init__`, and adds action methods named with verbs. Assertions stay in the tests.

### Key ideas

- Always call `super().__init__(page)` first.
- Naming: class `LoginPage`, file `login_page.py`, locators `login_button`, actions `login()`.
- Page objects **expose** locators; tests **decide** what to expect.

### Worked example — `LoginPage`

**Step 1.** Create `pages/login_page.py`:

```python
from playwright.sync_api import Page

from pages.base_page import BasePage


class LoginPage(BasePage):
    URL = "/"
```

**Step 2.** Add the locators:

```python
    def __init__(self, page: Page):
        super().__init__(page)
        self.username_input = page.get_by_placeholder("Username")
        self.password_input = page.get_by_placeholder("Password")
        self.login_button = page.get_by_role("button", name="Login")
        self.error_message = page.get_by_role("alert")
```

**Step 3.** Add the action:

```python
    def login(self, username: str, password: str) -> None:
        self.username_input.fill(username)
        self.password_input.fill(password)
        self.login_button.click()
```

**Step 4.** Write `tests/test_login.py`:

```python
from playwright.sync_api import expect

from pages.login_page import LoginPage


def test_wrong_password(page):
    login_page = LoginPage(page).open()
    login_page.login("standard_user", "wrong")
    expect(login_page.error_message).to_contain_text(
        "Username and password do not match"
    )
```

> **Predict:** what breaks if you forget `super().__init__(page)`?

### Checkpoint

`tests/test_login.py::test_wrong_password PASSED`

### Your turn

1. Write `test_successful_login`: log in as `standard_user` and check the URL ends with `inventory.html`.
2. Write `test_locked_user` and check the error contains "locked out".
3. Why is `login_page.check_error_is_wrong_password()` a bad method to add?

### Common errors

| Error | Fix |
|---|---|
| `AttributeError: 'LoginPage' object has no attribute 'page'` | Add `super().__init__(page)` |
| `ModuleNotFoundError: No module named 'pages'` | Run from `lecture08/`; check `pages/__init__.py` exists |

---

## Topic 3 — Methods with parameters and methods that return data

### Definition

When a page has many similar elements (six products), write **one method that takes a parameter** instead of one locator per element. When tests need to calculate or compare, return **plain Python values** from a `get_...` method.

### Key ideas

- `product(name)` returns the card for any product.
- `*names` lets a method accept any number of arguments.
- `get_prices()` returns a list of floats the test can sort or sum.

### Worked example — `ProductsPage`

**Step 1.** Create `pages/products_page.py` with locators:

```python
from pages.base_page import BasePage


class ProductsPage(BasePage):
    URL = "/inventory.html"

    def __init__(self, page):
        super().__init__(page)
        self.products = page.get_by_test_id("inventory-item")
        self.product_names = page.get_by_test_id("inventory-item-name")
        self.product_prices = page.get_by_test_id("inventory-item-price")
        self.sort_dropdown = page.get_by_test_id("product-sort-container")
```

**Step 2.** One method for any product's card:

```python
    def product(self, name: str):
        return self.products.filter(has=self.page.get_by_text(name, exact=True))
```

**Step 3.** Add to cart, for any number of products:

```python
    def add_to_cart(self, *names: str) -> None:
        for name in names:
            self.product(name).get_by_role("button", name="Add to cart").click()
```

**Step 4.** Sort and read data:

```python
    def sort_by(self, option: str) -> None:
        self.sort_dropdown.select_option(label=option)

    def get_names(self) -> list[str]:
        return self.product_names.all_text_contents()

    def get_prices(self) -> list[float]:
        return [float(p.replace("$", "")) for p in self.product_prices.all_text_contents()]
```

**Step 5.** Test it in `tests/test_products.py`:

```python
from playwright.sync_api import expect

from pages.login_page import LoginPage
from pages.products_page import ProductsPage


def test_add_two_items(page):
    LoginPage(page).open().login("standard_user", "secret_sauce")
    products_page = ProductsPage(page)
    products_page.add_to_cart("Sauce Labs Backpack", "Sauce Labs Fleece Jacket")
    expect(products_page.cart_badge).to_have_text("2")
```

### Checkpoint

`test_add_two_items PASSED`

### Your turn

1. Add `remove_from_cart(*names)` and test it.
2. Test that sorting by "Price (low to high)" gives `sorted(get_prices())`.
3. Test that sorting by "Name (Z to A)" gives `sorted(get_names(), reverse=True)`.

---

## Topic 4 — Converting a script-style test to POM

### Definition

Converting to POM is **refactoring**: it changes the structure of a test, not its behaviour. Do it one test at a time and run after each change.

### Key ideas

1. Group the script's lines by page (comments).
2. Move each locator into its page class.
3. Turn groups of steps into methods.
4. Rewrite the test with the classes.
5. Run — it must still pass.

### Worked example — the checkout test

**Step 1.** Start from the script, grouped by page (`tests/test_before_pom.py`):

```python
from playwright.sync_api import expect


def test_checkout(page):
    # --- Login page ---
    page.goto("/")
    page.get_by_placeholder("Username").fill("standard_user")
    page.get_by_placeholder("Password").fill("secret_sauce")
    page.get_by_role("button", name="Login").click()
    # --- Products page ---
    page.get_by_test_id("add-to-cart-sauce-labs-backpack").click()
    page.get_by_test_id("add-to-cart-sauce-labs-fleece-jacket").click()
    page.get_by_test_id("shopping-cart-link").click()
    # --- Cart page ---
    page.get_by_role("button", name="Checkout").click()
    # --- Checkout page ---
    page.get_by_placeholder("First Name").fill("Asha")
    page.get_by_placeholder("Last Name").fill("Patel")
    page.get_by_placeholder("Zip/Postal Code").fill("10001")
    page.get_by_role("button", name="Continue").click()
    expect(page.get_by_test_id("total-label")).to_have_text("Total: $86.38")
```

**Step 2.** Create `pages/cart_page.py`:

```python
from pages.base_page import BasePage


class CartPage(BasePage):
    URL = "/cart.html"

    def __init__(self, page):
        super().__init__(page)
        self.items = page.get_by_test_id("inventory-item")
        self.checkout_button = page.get_by_role("button", name="Checkout")

    def checkout(self):
        self.checkout_button.click()
```

**Step 3.** Create `pages/checkout_page.py`:

```python
from pages.base_page import BasePage


class CheckoutPage(BasePage):
    URL = "/checkout-step-one.html"

    def __init__(self, page):
        super().__init__(page)
        self.first_name_input = page.get_by_placeholder("First Name")
        self.last_name_input = page.get_by_placeholder("Last Name")
        self.postcode_input = page.get_by_placeholder("Zip/Postal Code")
        self.continue_button = page.get_by_role("button", name="Continue")
        self.total = page.get_by_test_id("total-label")

    def enter_details(self, first, last, postcode):
        self.first_name_input.fill(first)
        self.last_name_input.fill(last)
        self.postcode_input.fill(postcode)
        self.continue_button.click()
```

**Step 4.** Rewrite the test in `tests/test_cart_and_checkout.py`:

```python
def test_checkout(page):
    LoginPage(page).open().login("standard_user", "secret_sauce")

    products_page = ProductsPage(page)
    products_page.add_to_cart("Sauce Labs Backpack", "Sauce Labs Fleece Jacket")
    products_page.go_to_cart()

    CartPage(page).checkout()

    checkout_page = CheckoutPage(page)
    checkout_page.enter_details("Asha", "Patel", "10001")
    expect(checkout_page.total).to_have_text("Total: $86.38")
```

(Add the imports for `expect` and the four page classes at the top.)

**Step 5.** Run both files.

> **Predict:** if the "Checkout" button is renamed "Buy now", how many files must change before and after POM?

### Checkpoint

Both `test_before_pom.py::test_checkout` and `test_cart_and_checkout.py::test_checkout` pass.

### Your turn

1. Add a `finish_button`, a `complete_header` (`get_by_test_id("complete-header")`) and `finish()` to `CheckoutPage`, and check "Thank you for your order!" appears.
2. Add `get_item_names()` to `CartPage` and check the cart holds the Backpack and the Fleece Jacket.
3. Click **Continue** with an empty form and check the error says "First Name is required". Which page class gets the `error_message` locator?

### Common errors

| Error | Fix |
|---|---|
| Locators left in tests | Move them into page classes |
| `login_as_standard_user_with_wrong_password()` | One general method with parameters |

---

## Topic 5 — Page objects through fixtures

### Definition

Fixtures in `conftest.py` can return **ready-to-use page objects** — already opened and already logged in — so tests start straight at the interesting part.

### Key ideas

- Combine with Lecture 7's saved login (`user_state`).
- Fixtures that share the same `logged_in_page` share **one browser tab**.
- Fixtures can build a starting state (e.g. a cart with two items).

### Worked example — fixtures for every page

**Step 1.** In `conftest.py`, import the page classes and add a login-page fixture:

```python
from pages.login_page import LoginPage
from pages.products_page import ProductsPage
from pages.cart_page import CartPage
from pages.checkout_page import CheckoutPage


@pytest.fixture
def login_page(page) -> LoginPage:
    return LoginPage(page).open()
```

**Step 2.** A logged-in tab (uses `user_state` from Lecture 7). Replace Lecture 7's `logged_in_page` with:

```python
@pytest.fixture
def logged_in_page(new_context, user_state):
    return new_context(storage_state=user_state).new_page()
```

**Step 3.** Page objects on that tab:

```python
@pytest.fixture
def products_page(logged_in_page) -> ProductsPage:
    return ProductsPage(logged_in_page).open()


@pytest.fixture
def cart_page(logged_in_page) -> CartPage:
    return CartPage(logged_in_page)


@pytest.fixture
def checkout_page(logged_in_page) -> CheckoutPage:
    return CheckoutPage(logged_in_page)
```

**Step 4.** A starting-state fixture:

```python
@pytest.fixture
def cart_with_two_items(products_page, cart_page) -> CartPage:
    products_page.add_to_cart("Sauce Labs Backpack", "Sauce Labs Fleece Jacket")
    products_page.go_to_cart()
    return cart_page
```

**Step 5.** The checkout test becomes three lines:

```python
def test_full_checkout(cart_with_two_items, checkout_page):
    cart_with_two_items.checkout()
    checkout_page.enter_details("Asha", "Patel", "10001")
    expect(checkout_page.total).to_have_text("Total: $86.38")
```

> **Predict:** `products_page` and `cart_page` are two fixtures — do they open two tabs?

### Checkpoint

`test_full_checkout PASSED`, and no test logs in through the UI.

### Your turn

1. Rewrite `test_add_two_items` from Topic 3 using the `products_page` fixture.
2. Write `test_remove_item(cart_with_two_items)` that removes the Fleece Jacket and checks one item remains.
3. Write `test_log_out(products_page)` that logs out and checks the **Login** button is visible again.

### Common errors

| Error | Fix |
|---|---|
| Two `pages/` folders in different projects clash | Run each folder separately |
| Fixture opens the wrong page | Check `URL` and that you called `.open()` |

---

## Stretch challenge

Add a `HeaderComponent` class (cart link, cart badge, menu, logout) and have `BasePage` create it as `self.header`. Update one test to use `products_page.header.go_to_cart()`. Discuss: is this better than putting the header in `BasePage` directly?

## Exit ticket

1. In POM, where do locators go and where do assertions go?
2. What does `return self` in `open()` let you write?
3. Why does `product(name)` beat six separate product locators?

## Cheat sheet

| Code | Purpose |
|---|---|
| `class BasePage:` with `URL`, `open()`, header | Shared parent |
| `class LoginPage(BasePage):` | Page class inherits base |
| `super().__init__(page)` | Set up `self.page` and header |
| `self.login_button = page.get_by_role(...)` | Locator attribute |
| `def login(self, username, password):` | Action method (verb) |
| `def product(self, name):` | Parameterised locator |
| `def add_to_cart(self, *names):` | Any number of arguments |
| `def get_prices(self) -> list[float]:` | Return data |
| `LoginPage(page).open().login(...)` | Chained use |
| `@pytest.fixture def products_page(logged_in_page):` | Ready-made page object |
| `pages/__init__.py` | Makes `pages` importable |
