"""STRETCH: the same three scenarios against the public site https://www.saucedemo.com.
Needs internet and is skipped unless you run:  python -m pytest -m live -v
(Public sites can change their markup without notice. If a test here fails but the offline
version passes, check the site first.)  Note: SauceDemo has NO search box, so scenario 3
becomes 'find a specific product card and read its price'."""
import pytest
from playwright.sync_api import Page, expect

LIVE_URL = "https://www.saucedemo.com/"


@pytest.mark.live
def test_live_valid_login(page: Page):
    # TODO: log in as standard_user / secret_sauce (placeholders "Username" / "Password"), assert URL ends /inventory.html
    pytest.skip("TODO (stretch)")


@pytest.mark.live
def test_live_locked_out_login(page: Page):
    # TODO: locked_out_user / secret_sauce -> error contains "locked out"
    pytest.skip("TODO (stretch)")


@pytest.mark.live
def test_live_find_product_and_price(page: Page):
    # TODO: log in, then find the "Sauce Labs Backpack" card (.inventory_item filter has_text) and assert its price is $29.99
    pytest.skip("TODO (stretch)")
