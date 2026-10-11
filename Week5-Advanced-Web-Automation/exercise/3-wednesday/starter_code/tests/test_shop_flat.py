"""STAGE 0 - the flat, messy suite you will refactor.

It WORKS (run `pytest` and you get 7 passed).  It is also full of the smells from the
lesson: login copy-pasted into every test, locators and URLs hard-coded everywhere,
credentials and expected texts inline, one test that walks six screens, and several
tests that differ only in their data.

Rule of the exercise: behaviour must NOT change; only the structure does.
Do not "fix" the tests; move them, one small step at a time, and stay green.
"""
from playwright.sync_api import Page, expect


def test_login_standard_user(page: Page):
    page.goto("http://127.0.0.1:8791/")
    page.locator("[data-test='username']").fill("standard_user")
    page.locator("[data-test='password']").fill("secret_sauce")
    page.locator("[data-test='login-button']").click()
    expect(page).to_have_url("http://127.0.0.1:8791/inventory.html")
    expect(page.locator("[data-test='inventory-item']").first).to_be_visible()


def test_login_locked_out_user(page: Page):
    page.goto("http://127.0.0.1:8791/")
    page.locator("[data-test='username']").fill("locked_out_user")
    page.locator("[data-test='password']").fill("secret_sauce")
    page.locator("[data-test='login-button']").click()
    expect(page.locator("[data-test='error']")).to_have_text(
        "Epic sadface: Sorry, this user has been locked out.")


def test_login_wrong_password(page: Page):
    page.goto("http://127.0.0.1:8791/")
    page.locator("[data-test='username']").fill("standard_user")
    page.locator("[data-test='password']").fill("not_the_password")
    page.locator("[data-test='login-button']").click()
    expect(page.locator("[data-test='error']")).to_have_text(
        "Epic sadface: Username and password do not match any user in this service")


def test_login_empty_username(page: Page):
    page.goto("http://127.0.0.1:8791/")
    page.locator("[data-test='password']").fill("secret_sauce")
    page.locator("[data-test='login-button']").click()
    expect(page.locator("[data-test='error']")).to_have_text("Epic sadface: Username is required")


def test_purchase_two_items(page: Page):
    # --- login (copy 5 of 7) ---
    page.goto("http://127.0.0.1:8791/")
    page.locator("[data-test='username']").fill("standard_user")
    page.locator("[data-test='password']").fill("secret_sauce")
    page.locator("[data-test='login-button']").click()
    expect(page).to_have_url("http://127.0.0.1:8791/inventory.html")

    # --- add items ---
    page.locator("[data-test='add-to-cart-sauce-labs-backpack']").click()
    page.locator("[data-test='add-to-cart-sauce-labs-bike-light']").click()
    expect(page.locator("[data-test='shopping-cart-badge']")).to_have_text("2")

    # --- cart ---
    page.locator("[data-test='shopping-cart-link']").click()
    expect(page).to_have_url("http://127.0.0.1:8791/cart.html")
    names = page.locator("[data-test='inventory-item-name']").all_inner_texts()
    assert names == ["Sauce Labs Backpack", "Sauce Labs Bike Light"]
    page.locator("[data-test='checkout']").click()

    # --- checkout step one ---
    page.locator("[data-test='firstName']").fill("Asha")
    page.locator("[data-test='lastName']").fill("Patel")
    page.locator("[data-test='postalCode']").fill("560001")
    page.locator("[data-test='continue']").click()

    # --- checkout overview ---
    expect(page).to_have_url("http://127.0.0.1:8791/checkout-step-two.html")
    page.locator("[data-test='finish']").click()

    # --- confirmation ---
    expect(page.locator("[data-test='complete-header']")).to_have_text("Thank you for your order!")


def test_checkout_requires_first_name(page: Page):
    page.goto("http://127.0.0.1:8791/")
    page.locator("[data-test='username']").fill("standard_user")
    page.locator("[data-test='password']").fill("secret_sauce")
    page.locator("[data-test='login-button']").click()
    page.locator("[data-test='add-to-cart-sauce-labs-backpack']").click()
    page.locator("[data-test='shopping-cart-link']").click()
    page.locator("[data-test='checkout']").click()
    page.locator("[data-test='lastName']").fill("Patel")
    page.locator("[data-test='postalCode']").fill("560001")
    page.locator("[data-test='continue']").click()
    expect(page.locator("[data-test='error']")).to_contain_text("First Name is required")


def test_sort_price_low_to_high(page: Page):
    page.goto("http://127.0.0.1:8791/")
    page.locator("[data-test='username']").fill("standard_user")
    page.locator("[data-test='password']").fill("secret_sauce")
    page.locator("[data-test='login-button']").click()
    page.locator("[data-test='product-sort-container']").select_option(label="Price (low to high)")
    names = page.locator("[data-test='inventory-item-name']").all_inner_texts()
    assert names[0] == "Sauce Labs Onesie"
    assert names[-1] == "Sauce Labs Fleece Jacket"
