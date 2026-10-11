"""Shared fixtures (Tuesday: conftest.py + fixtures stacking on fixtures)."""
import pytest
from playwright.sync_api import Page

import gadgethub


@pytest.fixture
def login_page(page: Page) -> Page:
    """PROVIDED. `page` comes from pytest-playwright (browser -> context -> page).
    This fixture installs the offline GadgetHub site and opens its sign-in page."""
    gadgethub.install(page)
    page.goto(gadgethub.SITE_URL + "/")
    return page


# TODO (Task 2): write a fixture called `logged_in_page` that
#   - requests the `login_page` fixture,
#   - signs in as tester@gadgethub.test / Passw0rd! using built-in locators,
#   - waits (with a web-first assertion, NOT a sleep) until the URL ends with /shop.html,
#   - returns the page.
# Hint: written/5-friday/creating-playwright-tests.md, Example 6.
@pytest.fixture
def logged_in_page(login_page: Page) -> Page:
    pytest.skip("TODO: implement the logged_in_page fixture in conftest.py")
