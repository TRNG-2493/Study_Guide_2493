# conftest.py - shared Playwright fixtures (Wednesday pattern). Cypress twin: cypress/support/commands.js
import re

import pytest
from playwright.sync_api import Page, expect


@pytest.fixture
def logged_in_page(page: Page) -> Page:
    """Wednesday-style fixture. Cypress has no direct twin: think custom command + cy.session."""
    page.goto("/")
    page.locator('[data-test="username"]').fill("standard_user")
    page.locator('[data-test="password"]').fill("secret_sauce")
    page.locator('[data-test="login-button"]').click()
    expect(page).to_have_url(re.compile("inventory"))
    return page
