"""Task 6 - DEBUG ME. Each test below is BROKEN on purpose (the site is fine, the TEST is wrong).
They currently FAIL. Use the error message, the Inspector (PWDEBUG=1) and the Pick-locator tool to find
the bug, fix the test, and write one sentence per test in NOTES.md ('what was wrong / how I found it').
Do not change gadgethub.py or conftest.py."""
import pytest
from playwright.sync_api import Page, expect


@pytest.mark.offline
def test_bug_a_sign_out_returns_to_sign_in(logged_in_page: Page):
    logged_in_page.get_by_role("button", name="Log out").click(timeout=3000)
    expect(logged_in_page).to_have_title("GadgetHub - Sign in")


@pytest.mark.offline
def test_bug_b_add_first_product(logged_in_page: Page):
    logged_in_page.get_by_role("button", name="Add to cart").click(timeout=3000)
    expect(logged_in_page.get_by_test_id("cart-count")).to_have_text("1")


@pytest.mark.offline
def test_bug_c_search_result_count(logged_in_page: Page):
    logged_in_page.get_by_placeholder("Search gadgets...").fill("wireless")
    assert logged_in_page.locator(".card").count() == 2
