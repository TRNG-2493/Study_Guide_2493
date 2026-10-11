"""
test_project1_ui.py - the 3 Playwright (Python) tests your pair ports to Cypress.

Run (app must be running: `npm run app` in starter_code/):
    cd starter_code/playwright
    pip install -r requirements.txt && playwright install chromium
    python -m pytest -v

ASSUMPTION: these stand in for 3 of your own Project 1 UI tests. If your Project 1 app is
available and your instructor agrees, port 3 tests from YOUR suite instead and keep the
"three different shapes" rule (form/data-driven, state change with a fixture, list assertion).

Shared fixture: conftest.py (logged_in_page).
Shapes: 1 = form + data-driven, 2 = shared login fixture + conditional element, 3 = list + sort.
"""
import json
import re
from pathlib import Path

import pytest
from playwright.sync_api import Page, expect

# Same data files the Cypress project reads (cypress/fixtures) - one source of truth.
FIXTURES = Path(__file__).parent.parent / "cypress" / "fixtures"
LOGIN_CASES = json.loads((FIXTURES / "login-cases.json").read_text())


# ---- Test 1: form + data-driven ----------------------------------------------------------
@pytest.mark.parametrize("case", LOGIN_CASES, ids=[c["title"] for c in LOGIN_CASES])
def test_login_rejected(page: Page, case):
    page.goto("/")
    if case["username"]:
        page.get_by_placeholder("Username").fill(case["username"])
    if case["password"]:
        page.get_by_placeholder("Password").fill(case["password"])
    page.get_by_role("button", name="Login").click()
    expect(page.locator('[data-test="error"]')).to_contain_text(case["expectedError"])
    expect(page).not_to_have_url(re.compile("inventory"))


# ---- Test 2: state change after shared login ---------------------------------------------
def test_add_to_cart_updates_badge(logged_in_page: Page):
    page = logged_in_page
    expect(page.locator('[data-test="cart-badge"]')).to_have_count(0)
    page.locator('[data-test="add-to-cart-sauce-backpack"]').click()
    expect(page.locator('[data-test="cart-badge"]')).to_have_text("1")
    expect(page.locator('[data-test="remove-sauce-backpack"]')).to_be_visible()


# ---- Test 3: list + sort ------------------------------------------------------------------
def test_sort_price_low_to_high(logged_in_page: Page):
    page = logged_in_page
    # The list arrives ~300 ms after page load. all_inner_texts() does NOT wait, so we first
    # wait with a web-first assertion (a plain assert on an empty list would fail or pass wrongly).
    expect(page.locator('[data-test="inventory-item"]')).to_have_count(6)
    page.locator('[data-test="sort"]').select_option("lohi")
    texts = page.locator('[data-test="item-price"]').all_inner_texts()
    prices = [float(t.replace("$", "")) for t in texts]
    assert prices == sorted(prices)  # plain assert: no retry. Discuss: what does Cypress do here?
