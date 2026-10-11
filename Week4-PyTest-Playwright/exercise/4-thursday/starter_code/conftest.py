"""Shared fixtures (Tuesday: conftest.py, fixture scopes)."""
import pytest
from playwright.sync_api import sync_playwright

from locator_catalog import config as _cfg, pages


def pytest_report_header(config):
    return f"practice site: {_cfg.SITE} ({_cfg.LOGIN_URL}) | headless={_cfg.HEADLESS}"


@pytest.fixture(scope="session")
def site_browser():
    """ONE browser for the whole run: launching is the slow part, so scope='session'."""
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=_cfg.HEADLESS, slow_mo=_cfg.SLOW_MO)
        yield browser
        browser.close()


@pytest.fixture
def login_page(site_browser):
    """A FRESH context (clean cookies/storage) and tab for every test, parked on the login page."""
    context = site_browser.new_context()
    page = context.new_page()
    pages.open_login(page)
    yield page
    context.close()


@pytest.fixture
def error_page(login_page):
    """Login page after a failed login (the error message is showing)."""
    # TODO (Task 4): build on `login_page` and use a helper from locator_catalog/pages.py
    raise NotImplementedError("TODO Task 4: error_page fixture")


@pytest.fixture
def inventory_page(login_page):
    """Logged in, product page showing."""
    # TODO (Task 4): build on `login_page` and use a helper from locator_catalog/pages.py
    raise NotImplementedError("TODO Task 4: inventory_page fixture")
