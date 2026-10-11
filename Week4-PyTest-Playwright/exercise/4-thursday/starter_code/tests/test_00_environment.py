"""Is the toolchain alive? Run this first. (Thursday: playwright-architecture-and-setup.md)"""
import pytest

pytestmark = pytest.mark.smoke


def test_browser_launches_and_page_loads(login_page):
    assert "Swag Labs" in login_page.title()


def test_locator_is_lazy_count_is_the_search(login_page):
    locator = login_page.locator(".inventory_item")      # created on the login page: no error, nothing searched
    assert locator.count() == 0                           # the search happens now: product list not there yet
