"""Task 7 helper (PROVIDED): fails on purpose so the report can show screenshot evidence.

Skipped by default.  Needs your `inventory_page` fixture (Task 3).  Run it with:
    pytest -m fails_on_purpose
It is an AssertionError, so your --only-rerun filter must NOT retry it.
"""
import pytest
from playwright.sync_api import expect


@pytest.mark.fails_on_purpose
def test_deliberate_failure_for_report(inventory_page):
    expect(inventory_page.header.cart_badge).to_have_text("99", timeout=1500)
