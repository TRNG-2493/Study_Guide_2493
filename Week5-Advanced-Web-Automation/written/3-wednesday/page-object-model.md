# Page Object Model

## Learning Objectives

By the end of this lesson you will be able to:

- Explain what the Page Object Model (POM) is, the problems it solves, and the principles behind it (separation of concerns, DRY, single place to change).
- Recognise the pain of a "flat script" that mixes locators, actions, and assertions, and describe why it breaks down as a suite grows.
- Design a page class in Python for Playwright: locators defined once in `__init__`, methods that represent *user intentions*, and no raw selectors in the tests.
- Build a `BasePage` that shares behaviour among all page classes (navigation, common waits, title/URL helpers).
- Decide where assertions belong and use the common conventions (verification helpers vs. assertions in tests).
- Model page **components** (header, cart badge, product card) as their own small classes.
- Use **fluent navigation**: methods that return the next page object.
- Deliver page objects to tests through pytest fixtures.
- Do a complete **before/after**: a flat SauceDemo login and inventory script, and the same behaviour as a POM-based test suite.
- Avoid the classic anti-patterns (God page, assertion-heavy pages, locators leaking into tests, sleeping).

---

## Why This Matters

This week's epic is about turning individual Playwright scripts into a **structured, maintainable framework**. The Page Object Model is the single most important structural pattern in UI test automation. It is the reason a team can own thousands of UI tests and still ship changes to the front end without spending every sprint repairing selectors.

Think about what happens in a real company. The product team redesigns the login screen. The `id` of the username box changes from `user-name` to `email`. If 120 tests each contain `page.locator("#user-name")`, you now have 120 edits and 120 chances to make a typo. If one `LoginPage` class owns that locator, you make **one** edit and all 120 tests are fixed.

POM matters for your career as well. When interviewers ask "how have you structured a test framework?", the Page Object Model is nearly always the expected first answer. Test frameworks you see in job descriptions (Selenium, Playwright, Cypress, Appium) all use it or a close cousin.

It is also central to **Project 1 - QE Foundations**. Your Project 1 UI deliverable will be reviewed not only on "do tests pass?" but on "can another engineer read and extend them?". Today's exercise asks you to refactor your Project 1 UI tests into POM with data-driven JSON; this lesson gives you the design, and the next lesson ("Converting scripts to POM") gives you a step-by-step refactoring procedure.

You will use everything from the first two days of this week: the locators, actions, and waits you practised on Monday (form controls, keyboard and mouse) and Tuesday (frames, tables, dynamic elements, navigation) become the *building blocks inside* your page classes. You will use fixtures (earlier today) to hand page objects to tests.

> **Cross-tool note.** The Page Object Model is tool-independent. You will meet it again when we look at Cypress; we cover Cypress in depth on Thursday and Friday.

---

## The Concept

### 1. Start with the problem: the flat script

A **flat script** is a test that contains everything directly: the URL, the selectors, the typed values, the clicks, and the assertions, all in one function. It is where almost everyone starts, and it is perfectly fine for a quick experiment. Here is our running example, a flat test that logs into SauceDemo (`https://www.saucedemo.com`), checks the inventory, adds an item to the cart, and sorts the products.

```python
# tests/test_flat_shopping.py   (BEFORE: flat script)
from playwright.sync_api import Page, expect


def test_login_and_add_backpack(page: Page):
    page.goto("https://www.saucedemo.com")
    page.locator("#user-name").fill("standard_user")
    page.locator("#password").fill("secret_sauce")
    page.locator("#login-button").click()
    expect(page).to_have_url("https://www.saucedemo.com/inventory.html")
    expect(page.locator(".title")).to_have_text("Products")

    page.locator("#add-to-cart-sauce-labs-backpack").click()
    expect(page.locator(".shopping_cart_badge")).to_have_text("1")


def test_login_and_sort_by_price_low_to_high(page: Page):
    page.goto("https://www.saucedemo.com")
    page.locator("#user-name").fill("standard_user")
    page.locator("#password").fill("secret_sauce")
    page.locator("#login-button").click()
    expect(page).to_have_url("https://www.saucedemo.com/inventory.html")

    page.locator(".product_sort_container").select_option("lohi")
    prices = page.locator(".inventory_item_price").all_inner_texts()
    numbers = [float(p.replace("$", "")) for p in prices]
    assert numbers == sorted(numbers)


def test_locked_out_user_cannot_log_in(page: Page):
    page.goto("https://www.saucedemo.com")
    page.locator("#user-name").fill("locked_out_user")
    page.locator("#password").fill("secret_sauce")
    page.locator("#login-button").click()
    expect(page.locator("[data-test='error']")).to_contain_text("locked out")
```

Read it as if you were joining the team next week. What is wrong?

1. **Duplication.** The three-line login block appears three times. In a real suite it appears hundreds of times.
2. **Selectors scattered everywhere.** `#user-name` is in three tests; `#login-button` too. When one changes, you hunt through the repo.
3. **Low-level noise.** The reader must mentally translate `page.locator("#add-to-cart-sauce-labs-backpack").click()` into "add the backpack". The intention is hidden by the mechanics.
4. **Hard-coded values.** The URL, user names, and the password appear inside tests.
5. **Poor reuse.** To write a checkout test you copy-paste login lines again.
6. **Fragile.** The cost of any UI change is proportional to the number of tests.

These problems have a name: the test is doing **too many jobs**. It describes *what* to verify (the business intention), *how* to drive the UI (the mechanics), and *where* things are on the page (the locators). Good design gives each job its own home.

### 2. The idea of the Page Object Model

The Page Object Model says:

> **Represent each page (or significant part) of the application as a class. The class owns the locators for that page and exposes methods that represent what a user can do there. Tests use those methods and never touch raw locators.**

That gives you three clean layers:

```
┌──────────────────────────────────────────┐
│  TESTS         "what do we verify?"      │   test_login.py, test_inventory.py
│  login_page.login_as("standard_user")    │
├──────────────────────────────────────────┤
│  PAGE OBJECTS  "what can a user do here?"│   pages/login_page.py ...
│  fill username, click button, read error │
├──────────────────────────────────────────┤
│  PLAYWRIGHT    "how is the browser driven?"   Page, Locator, expect
└──────────────────────────────────────────┘
```

An analogy: a TV remote. You press "Volume up" (a business-level action). You do not need to know which circuit or infrared pattern is used. If the manufacturer changes the internals, the button on the remote still means "volume up". The page object is the remote for a page.

The name "Page Object **Model**" comes from the fact that the classes form a *model* of the application's UI: one class per page, one method per user action.

### 3. The five core principles

1. **One class per page (or per major component).** `LoginPage`, `InventoryPage`, `CartPage`, `CheckoutPage`.
2. **Locators live inside the page class, defined once.** Tests never contain selectors.
3. **Methods describe user intentions, not UI mechanics.** `login_as(...)`, `add_product_to_cart("Sauce Labs Backpack")`, `sort_by("Price (low to high)")`. Not `click_button_3()`.
4. **Tests contain the assertions that express expected behaviour** (the recommended convention), while page objects expose *state queries* (`get_error_message()`, `cart_count()`). More on this debate below.
5. **Page methods that navigate return the next page object**, so the code reads like a user journey.

### 4. Designing a page class in Python, step by step

We will build `LoginPage`. Follow each step.

**Step 1: create the class and accept a `Page`.**

```python
# pages/login_page.py
from playwright.sync_api import Page, expect


class LoginPage:
    URL = "/"

    def __init__(self, page: Page):
        self.page = page
```

- `class LoginPage:` defines a class, a blueprint for objects. By convention class names are `CapitalisedWords`.
- `URL = "/"` is a **class attribute**: a value shared by all instances. It is a path relative to `base_url` (set in `pytest.ini`, see the Fixtures lesson).
- `def __init__(self, page: Page):` is the **constructor**; Python runs it when you write `LoginPage(page)`. `self` is the object being created. The `page` argument is the Playwright `Page` the object will drive.
- `self.page = page` stores it as an **instance attribute** so other methods can use `self.page`.

This pattern is called **dependency injection**: the page object does not create its own browser; it is given one. That is what lets a fixture control the browser lifecycle.

**Step 2: define locators once, in the constructor.**

```python
    def __init__(self, page: Page):
        self.page = page
        self.username_input = page.get_by_test_id("username")
        self.password_input = page.get_by_test_id("password")
        self.login_button = page.get_by_test_id("login-button")
        self.error_message = page.get_by_test_id("error")
```

Important detail: a Playwright **`Locator` is lazy**. Creating `page.get_by_test_id("username")` does *not* look for the element; it stores *how to find it*. The element is searched for at the moment you act on it (`.fill()`, `.click()`) or assert on it (`expect(...)`), and Playwright's auto-waiting and retry apply then. That is why it is safe to create all locators up front in `__init__`, even for elements that are not yet on the page or that get re-rendered. (This is a major difference from older Selenium-style page objects that held stale element references.)

`get_by_test_id("username")` finds `<input data-test="username">`. SauceDemo uses `data-test` rather than Playwright's default `data-testid`, so the conftest from the Fixtures lesson calls `playwright.selectors.set_test_id_attribute("data-test")`. Prefer test ids and role-based locators (`get_by_role`, `get_by_label`, `get_by_placeholder`) over brittle CSS or XPath.

**Step 3: add action methods named after user intent.**

```python
    def open(self) -> "LoginPage":
        self.page.goto(self.URL)
        expect(self.login_button).to_be_visible()
        return self

    def login_as(self, username: str, password: str) -> None:
        self.username_input.fill(username)
        self.password_input.fill(password)
        self.login_button.click()
```

- `open()` navigates, then waits for a sign the page is ready (the login button being visible), and returns `self`, so you can write `LoginPage(page).open().login_as(...)` (a **fluent interface**: method chaining).
- `-> "LoginPage"` is a return-type hint. Quotes are used because the class is not fully defined yet at that point in the file.
- `login_as(...)` hides three UI steps behind one verb. Tests will read `login_page.login_as("standard_user", "secret_sauce")`.
- Each method does **one coherent user task**.

**Step 4: add "state query" methods that tests can assert on.**

```python
    def get_error_message(self) -> str:
        return self.error_message.inner_text()
```

The page object reports *what it sees*; the test decides whether it is right.

**Step 5: return the next page when navigation occurs.**

```python
    def login_successfully(self, username: str, password: str) -> "InventoryPage":
        self.login_as(username, password)
        return InventoryPage(self.page)
```

(This requires `from pages.inventory_page import InventoryPage`.) The return type documents the user journey: after a successful login you are on the inventory page.

### 5. A `BasePage` for shared behaviour

Every page shares some behaviour: reading the title, getting the current URL, and waiting for a URL. Put them in a base class and let others **inherit**.

```python
# pages/base_page.py
from playwright.sync_api import Page, expect


class BasePage:
    def __init__(self, page: Page):
        self.page = page

    def navigate(self, path: str = "/") -> None:
        self.page.goto(path)

    @property
    def title(self) -> str:
        return self.page.title()

    @property
    def current_url(self) -> str:
        return self.page.url

    def wait_for_url_contains(self, fragment: str) -> None:
        self.page.wait_for_url(f"**{fragment}**")

    def expect_on_page(self, fragment: str) -> None:
        expect(self.page).to_have_url(f"**{fragment}")
```

- `class BasePage:` is the parent. Child classes write `class LoginPage(BasePage):` and **inherit** everything.
- `@property` is a decorator that lets you read a method like an attribute: `page_object.title` rather than `page_object.title()`.
- `f"**{fragment}**"` builds a glob pattern: `**` matches any characters, so `wait_for_url_contains("/inventory")` matches `https://www.saucedemo.com/inventory.html`.
- A child constructor calls `super().__init__(page)` to run the parent's constructor first.

Keep `BasePage` **small and generic**. If it becomes a dumping ground it turns into a hidden God class. Methods used by only one page belong on that page.

### 6. Where should assertions live?

This is the most debated question in POM, so understand the options.

**Option A: no assertions in page objects (recommended for this course).** Page objects expose *actions* and *state*; tests assert. Benefits: page objects stay reusable (a page method that asserts "title is Products" cannot be reused in a test that expects a different title), and the test reads like a specification:

```python
assert login_page.get_error_message() == "Epic sadface: Sorry, this user has been locked out."
```

**Option B: verification helpers inside page objects**, e.g. `inventory_page.expect_loaded()`, which wraps `expect(self.title).to_have_text("Products")`. This is acceptable for *readiness checks* that confirm "we really arrived on this page". Many teams allow `expect_*` helper methods named clearly so that a reader knows they assert.

**Option C: assertion-heavy page objects** where every action also verifies results. Avoid it; it hides test logic inside infrastructure and makes failures hard to interpret.

A practical rule: **page objects may *wait* for readiness; tests *decide* what is correct.** Use `expect(...)` (web-first assertions with auto-retry) in either place rather than raw `assert` on a value read earlier, because a raw `assert` on `inner_text()` reads once and cannot retry while the UI settles.

### 7. Components: reusable parts of pages

The SauceDemo header (shopping cart icon and its badge, burger menu) appears on every page after login. Instead of duplicating its locators in `InventoryPage`, `CartPage`, and `CheckoutPage`, make a **component class** and compose it.

```python
# pages/components/header.py
from playwright.sync_api import Page


class Header:
    def __init__(self, page: Page):
        self.page = page
        self.cart_link = page.get_by_test_id("shopping-cart-link")
        self.cart_badge = page.get_by_test_id("shopping-cart-badge")
        self.menu_button = page.get_by_role("button", name="Open Menu")

    def cart_count(self) -> int:
        if self.cart_badge.count() == 0:       # badge disappears when cart is empty
            return 0
        return int(self.cart_badge.inner_text())

    def open_cart(self) -> None:
        self.cart_link.click()
```

- `self.cart_badge.count()` returns how many elements match right now (no waiting), here 0 or 1. SauceDemo hides the badge when the cart is empty; `inner_text()` would otherwise wait and time out.
- `int(...)` converts the text `"1"` to the number 1.

Then pages *contain* a header: `self.header = Header(page)`. **Composition** ("has a") often beats inheritance ("is a") for components.

You can apply the same idea to a **product card** (a repeating component that scopes locators to one container) and to a table row; recall scoping with `locator.filter()` and chained locators from Tuesday's web tables lesson.

### 8. Handling lists and repeating items

The inventory has six products. We want `add_product_to_cart("Sauce Labs Backpack")` without hard-coding each button's id.

```python
    def _card(self, product_name: str):
        return self.page.get_by_test_id("inventory-item").filter(has_text=product_name)

    def add_product_to_cart(self, product_name: str) -> None:
        self._card(product_name).get_by_role("button", name="Add to cart").click()
```

- `_card` (leading underscore) is a Python convention for "private helper; not for tests".
- `.filter(has_text=...)` narrows the list of product cards to the one containing the product name.
- `.get_by_role("button", name="Add to cart")` finds the button *inside* that card (chained locators are scoped to the parent).
- Parametrising by product *name* instead of id-in-a-selector means tests speak the language of the business.

### 9. Delivering page objects with fixtures

Tests should not write `LoginPage(page)` over and over; they should *receive* ready objects from fixtures.

```python
# conftest.py (excerpt)
import pytest
from pages.login_page import LoginPage
from pages.inventory_page import InventoryPage


@pytest.fixture
def login_page(page):
    return LoginPage(page).open()


@pytest.fixture
def inventory_page(login_page):
    return login_page.login_successfully("standard_user", "secret_sauce")
```

A test now asks for exactly the starting point it needs:

```python
def test_sort(inventory_page):
    inventory_page.sort_by("Price (low to high)")
    ...
```

Fixtures decide *how we get there*; page objects decide *how to act*; tests decide *what to verify*. This three-way split is the heart of a good framework.

### 10. The POM folder structure

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
│   ├── checkout_page.py
│   └── components/
│       ├── __init__.py
│       └── header.py
├── data/               (JSON test data, a later lesson)
└── tests/
    ├── test_login.py
    └── test_inventory.py
```

`__init__.py` files (can be empty) mark folders as Python **packages** so you can `from pages.login_page import LoginPage`. Run pytest from the project root so imports resolve; adding `pythonpath = .` in `pytest.ini` makes that explicit and robust.

---

## Code Examples

### The complete AFTER: the same behaviour as a POM suite

Below is the full refactor of the three flat tests from Section 1. Read the code, then the explanation.

**`pages/base_page.py`**

```python
from playwright.sync_api import Page


class BasePage:
    def __init__(self, page: Page):
        self.page = page

    @property
    def current_url(self) -> str:
        return self.page.url
```

**`pages/components/header.py`** (as in Section 7)

**`pages/login_page.py`**

```python
from playwright.sync_api import Page, expect

from pages.base_page import BasePage
from pages.inventory_page import InventoryPage


class LoginPage(BasePage):
    URL = "/"

    def __init__(self, page: Page):
        super().__init__(page)
        self.username_input = page.get_by_test_id("username")
        self.password_input = page.get_by_test_id("password")
        self.login_button = page.get_by_test_id("login-button")
        self.error_message = page.get_by_test_id("error")

    def open(self) -> "LoginPage":
        self.page.goto(self.URL)
        expect(self.login_button).to_be_visible()
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

**`pages/inventory_page.py`**

```python
from playwright.sync_api import Page, expect

from pages.base_page import BasePage
from pages.components.header import Header


class InventoryPage(BasePage):
    def __init__(self, page: Page):
        super().__init__(page)
        self.header = Header(page)
        self.title = page.get_by_test_id("title")
        self.items = page.get_by_test_id("inventory-item")
        self.prices = page.get_by_test_id("inventory-item-price")
        self.sort_dropdown = page.get_by_test_id("product-sort-container")

    def expect_loaded(self) -> None:
        expect(self.page).to_have_url("**/inventory.html")
        expect(self.title).to_have_text("Products")

    def _card(self, product_name: str):
        return self.items.filter(has_text=product_name)

    def add_product_to_cart(self, product_name: str) -> None:
        self._card(product_name).get_by_role("button", name="Add to cart").click()

    def remove_product_from_cart(self, product_name: str) -> None:
        self._card(product_name).get_by_role("button", name="Remove").click()

    def sort_by(self, option_value: str) -> None:
        self.sort_dropdown.select_option(option_value)

    def get_prices(self) -> list[float]:
        texts = self.prices.all_inner_texts()
        return [float(t.replace("$", "")) for t in texts]

    def product_count(self) -> int:
        return self.items.count()
```

**`conftest.py`** (relevant excerpt)

```python
import pytest

from pages.login_page import LoginPage


@pytest.fixture(scope="session", autouse=True)
def configure_test_id(playwright):
    playwright.selectors.set_test_id_attribute("data-test")


@pytest.fixture
def login_page(page):
    return LoginPage(page).open()


@pytest.fixture
def inventory_page(login_page):
    return login_page.login_successfully("standard_user", "secret_sauce")
```

**`tests/test_shopping.py`**

```python
from playwright.sync_api import expect


def test_add_backpack_updates_cart_badge(inventory_page):
    inventory_page.add_product_to_cart("Sauce Labs Backpack")
    expect(inventory_page.header.cart_badge).to_have_text("1")


def test_sort_by_price_low_to_high(inventory_page):
    inventory_page.sort_by("lohi")
    prices = inventory_page.get_prices()
    assert prices == sorted(prices)


def test_inventory_has_six_products(inventory_page):
    assert inventory_page.product_count() == 6
```

**`tests/test_login.py`**

```python
def test_locked_out_user_sees_error(login_page):
    login_page.login_as("locked_out_user", "secret_sauce")
    assert "locked out" in login_page.get_error_message()


def test_valid_login_lands_on_inventory(login_page):
    inventory = login_page.login_successfully("standard_user", "secret_sauce")
    assert inventory.product_count() == 6
```

#### Explanation, line by line

- **`class LoginPage(BasePage):`**: inherits from `BasePage`. The parentheses name the parent class.
- **`super().__init__(page)`**: calls the parent constructor, which sets `self.page`. Forgetting this is a classic bug (`AttributeError: 'LoginPage' object has no attribute 'page'`).
- **Locator attributes in `__init__`**: each is a lazy `Locator`, as described earlier.
- **`login_successfully(...) -> InventoryPage`**: performs the login, constructs the next page object, calls `expect_loaded()` as a *readiness check* (a deliberate, clearly named wait), and returns it. The test therefore never needs sleeps; the readiness check uses auto-retrying `expect`.
- **`from pages.inventory_page import InventoryPage`**: be aware of circular imports. `LoginPage` imports `InventoryPage`; `InventoryPage` must **not** import `LoginPage` at module level. If you need a "logout returns to the login page" method later, import inside the method (`from pages.login_page import LoginPage` within `logout()`), a standard fix.
- **`list[float]`** is a type hint using built-in generics (Python 3.9+).
- **`[float(t.replace("$", "")) for t in texts]`** is a **list comprehension**: for each text such as `"$29.99"`, strip the dollar sign and convert to a number. We compare numbers, not strings, because `"$9.99" > "$29.99"` alphabetically (strings compare character by character) and would give wrong results.
- **`sorted(prices)`** returns a new sorted list; if the page's order equals it, the sort works.
- **Tests**: each is 2-4 lines and reads like a requirement. No selector appears. No URL appears. The credentials appear only in the fixture (a later lesson will move them into JSON data).
- **`expect(inventory_page.header.cart_badge).to_have_text("1")`**: tests may use a page object's locator for an `expect` assertion because `expect` is web-first. (Some teams prefer a method such as `header.expect_cart_count(1)`. Both are valid; be consistent within your project.)

#### What did we gain?

| Concern | BEFORE (flat) | AFTER (POM) |
|---|---|---|
| Change `#user-name` | edit every test | edit `LoginPage.__init__` once |
| Readability | read selectors | read intentions |
| Add a checkout test | copy-paste login | request `inventory_page` fixture |
| Lines per test | 8 to 12 | 2 to 4 |
| Where is login logic | everywhere | `LoginPage.login_as` |

And what did we pay? More files, an extra layer, and the need to understand classes. That cost is small compared with the maintenance saved, but it is real: for a three-test throw-away script, POM is overkill. POM pays off as soon as a second test touches the same page.

---

## Real-World Scenarios

**Scenario 1: The redesign.** A retail team's login page is redesigned. The username field moves from `#user-name` to a label "Email". With POM, one line in `LoginPage` changes (`get_by_label("Email")`) and 140 tests continue to pass.

**Scenario 2: Parallel feature work.** Two engineers add tests at once. One owns `CartPage`, the other `CheckoutPage`. Because pages are separate files, merge conflicts are rare. Without POM both would edit a giant test file.

**Scenario 3: Onboarding.** A new teammate reads `test_checkout.py` and understands the journey in a minute, because it reads `login -> add product -> open cart -> checkout -> verify`. They do not have to understand CSS.

**Scenario 4: Multi-product, multi-brand sites.** A company runs three brands with the same checkout flow but different branding. A shared `CheckoutPage` with brand-specific subclasses overrides only the locators that differ.

---

## Common Pitfalls and Best Practices

**Pitfalls (anti-patterns)**

1. **Locators leaking into tests.** If a test contains `page.locator(...)`, the page object is incomplete. Add a method.
2. **The God page.** One `AppPage` with 80 methods. Split by page and by component.
3. **Assertion-heavy page objects.** `login()` that also asserts the URL. Reuse suffers; failures are confusing.
4. **Methods named after mechanics.** `click_submit()` instead of `submit_order()`. Name for *intent*.
5. **`time.sleep()` in page methods.** Use auto-waiting actions and `expect(...)`. A sleep is either too short (flaky) or too long (slow).
6. **Page objects that create browsers.** They should receive `page`, not launch Playwright.
7. **Forgetting `super().__init__(page)`.**
8. **Circular imports.** Page A imports page B which imports page A. Import inside the method or restructure.
9. **Over-engineering on day one.** Do not build a 6-level inheritance tree before you have two tests. Start small and refactor.
10. **Static state.** Using class-level mutable attributes (like a shared list) in page objects leaks data between tests.
11. **Treating returned state as live.** `inner_text()` returns a snapshot string. If the UI may still be updating, assert with `expect(locator)` instead, which retries.

**Best practices**

- Prefer **user-facing locators** (`get_by_role`, `get_by_label`, `get_by_test_id`) over long CSS/XPath chains.
- One page class per file; filename in `snake_case`, class in `PascalCase`.
- Methods do one thing; return `self` or the next page for chaining.
- Keep test data (usernames, products) **out** of page classes; pass it in as arguments (the JSON lesson shows how to supply it).
- Use **type hints** and short **docstrings** on public methods.
- Provide page objects through **fixtures**.
- Review rule of thumb: *if a UI change touches more than one file, the design needs another look.*

---

## Mini Practice Exercises

**Exercise 1: spot the smells.**
Look at the flat script in Section 1 and list at least five problems. *Answer key:* duplicated login, scattered selectors, hard-coded URL/credentials, low-level noise, no reuse, selectors in assertions.

**Exercise 2: build `CartPage`.**
SauceDemo's cart (`/cart.html`) lists items (`data-test="inventory-item"`), each with a name (`data-test="inventory-item-name"`), and has "Continue Shopping" and "Checkout" buttons (`data-test="continue-shopping"`, `data-test="checkout"`). Write a `CartPage` with `get_item_names() -> list[str]`, `remove(product_name)`, and `proceed_to_checkout()`.
*Hint:* `self.items.get_by_test_id("inventory-item-name").all_inner_texts()` gives the names. Verify the data-test values by opening DevTools.

**Exercise 3: component.**
Create a `ProductCard` component class that wraps one product card locator and exposes `name`, `price`, `add_to_cart()`. Update `InventoryPage` to return a `ProductCard` from `product(name)`.
*Hint:* `ProductCard.__init__(self, root: Locator)` and build children with `root.get_by_test_id(...)`.

**Exercise 4: fluent journey.**
Make `add_product_to_cart` return `self` and write a single-expression test that adds two products, then reads the cart count.
*Solution sketch:*
```python
inventory_page.add_product_to_cart("Sauce Labs Backpack").add_product_to_cart("Sauce Labs Bike Light")
assert inventory_page.header.cart_count() == 2
```

**Exercise 5: change-impact experiment.**
Temporarily break the `username_input` locator (use `get_by_test_id("user")`). Run the suite. Count how many tests fail and how many files you must edit to fix it. Repeat the experiment on the flat script. Compare.

**Exercise 6 (Project 1 link):** Choose one page from your Project 1 application and create its page class. Replace at least two tests' direct locators with page methods. The next lesson shows the full conversion procedure.

---

## Summary / Key Takeaways

- A **flat script** mixes *what*, *how*, and *where*. It is quick to write but expensive to maintain.
- The **Page Object Model** models each page (or component) as a class that owns its locators and exposes **user-intent methods**; tests use the methods and assert on outcomes.
- Playwright `Locator`s are lazy, so defining them once in `__init__` is safe and idiomatic.
- Use a small `BasePage`, **composition** for components such as a header, and **fluent navigation** (return the next page).
- Put assertions in tests (preferred) and use clearly named `expect_*` helpers only for readiness checks.
- Provide page objects through **pytest fixtures**; keep data out of pages.
- Avoid God pages, selectors in tests, sleeps, and assertion-heavy page objects.
- POM pays off as soon as more than one test touches the same page.

---

## External Resources

- Playwright for Python, "Page object models": https://playwright.dev/python/docs/pom
- Playwright for Python, "Locators": https://playwright.dev/python/docs/locators
- Martin Fowler, "PageObject" (the original pattern description): https://martinfowler.com/bliki/PageObject.html
