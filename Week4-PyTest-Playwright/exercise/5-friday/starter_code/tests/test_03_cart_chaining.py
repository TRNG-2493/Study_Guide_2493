"""Task 5: filtering and chaining locators."""
import pytest
from playwright.sync_api import Page, expect


@pytest.mark.offline
def test_add_specific_product_to_cart(logged_in_page: Page):
    """Add ONLY the 'Laptop Stand' to the cart.
    Plan: card = page.locator(".card").filter(has_text=...)  ->  card.get_by_role("button", ...)"""
    # TODO Act: click Add to cart INSIDE the Laptop Stand card.
    # TODO Assert: that card's button now reads "Remove"; cart count (get_by_test_id("cart-count")) is "1";
    #              another card (e.g. 'HD Webcam') still has an "Add to cart" button.
    pytest.skip("TODO: implement test_add_specific_product_to_cart")


@pytest.mark.offline
def test_filter_cards_by_text(logged_in_page: Page):
    """How many cards contain the word 'Wireless'? Use filter(has_text=...) and assert the count."""
    # TODO: implement (the answer is in the product list in the README).
    pytest.skip("TODO: implement test_filter_cards_by_text")
