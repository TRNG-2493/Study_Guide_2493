"""
Tiny plumbing so every test is a plain function (no pytest fixtures - those are Wednesday).

    with open_page() as page:        # starts the local app once, opens a fresh headless browser context
        page.goto("/orders")         # relative URLs work because the context has a base_url

You do not need to edit this file.
"""

import threading
from contextlib import contextmanager

from playwright.sync_api import sync_playwright

from app import make_server

_server = None
_base_url = None


def base_url() -> str:
    """Start the practice app on a free port the first time it is needed."""
    global _server, _base_url
    if _server is None:
        _server = make_server(0)
        threading.Thread(target=_server.serve_forever, daemon=True).start()
        _base_url = f"http://127.0.0.1:{_server.server_address[1]}"
    return _base_url


@contextmanager
def open_page(**context_options):
    """Yield a Page in a brand-new context. Locale and time zone are pinned so results do not depend on your laptop."""
    with sync_playwright() as p:
        browser = p.chromium.launch()          # headless by default; use p.chromium.launch(headless=False, slow_mo=300) to watch
        context = browser.new_context(base_url=base_url(), locale="en-US", timezone_id="UTC", **context_options)
        context.set_default_timeout(10_000)    # fail fast while learning (default is 30 s)
        try:
            yield context.new_page()
        finally:
            context.close()
            browser.close()
