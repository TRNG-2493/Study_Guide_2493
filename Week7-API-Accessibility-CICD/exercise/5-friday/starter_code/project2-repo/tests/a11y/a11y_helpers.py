"""Helpers for the accessibility tests (provided).

- `page`        : fixture, see below. Do not add a conftest.py in tests/a11y (see the brief, section 4).
- `mock_api`    : intercepts GET <API>/items with Playwright's page.route() (Wednesday's
                  mocking idea, applied in the browser). No server needed, fully deterministic.
- `open_state`  : puts a storefront variant into a named UI state.
"""
import json
from pathlib import Path

import os

import pytest
from playwright.sync_api import sync_playwright

from project2_api_server import SEED  # the five stand-in items

ROOT = Path(__file__).resolve().parents[2]
PAGES = {
    "bad": ROOT / "storefront" / "index.html",
    "fixed": ROOT / "storefront_fixed" / "index.html",   # YOU create this copy in task 4
}
CORS = {"access-control-allow-origin": "*"}


@pytest.fixture
def page():
    """Fresh Chromium page per test. Function scope on purpose: sync Playwright keeps an event loop
    alive while started, which would break the pytest-asyncio MCP tests if it outlived a test."""
    with sync_playwright() as p:
        exe = os.environ.get("CHROMIUM_PATH")
        browser = p.chromium.launch(headless=True, executable_path=exe) if exe else p.chromium.launch(headless=True)
        pg = browser.new_page()
        yield pg
        browser.close()


def url_of(variant):
    path = PAGES[variant]
    if not path.exists():
        pytest.skip(f"{path} does not exist yet")
    return path.as_uri()


def mock_api(page, *, fail=False):
    def handler(route):
        if fail:
            route.fulfill(status=500, headers=CORS, content_type="application/json", body='{"error":"boom"}')
        else:
            body = json.dumps({"total": len(SEED), "page": 1, "limit": 50, "items": SEED})
            route.fulfill(status=200, headers=CORS, content_type="application/json", body=body)
    page.route("**/items*", handler)


STATES = ["loaded", "form-error", "api-down"]


def open_state(page, variant, state):
    """Navigate to a storefront variant and drive it into one UI state."""
    mock_api(page, fail=(state == "api-down"))
    page.goto(url_of(variant))
    if state == "api-down":
        page.wait_for_function("document.getElementById('status').textContent.includes('Could not')")
        return
    page.wait_for_selector(".add-btn")
    if state == "form-error":
        page.fill("#email", "not-an-email")
        page.click("#subscribe")
        page.wait_for_function("document.getElementById('email-error').textContent.length > 0")
