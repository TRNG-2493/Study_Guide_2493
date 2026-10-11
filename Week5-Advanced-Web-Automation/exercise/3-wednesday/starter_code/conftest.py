"""Shared fixtures and hooks.

=== PROVIDED (do not edit): starts the local practice shop for the test session ===
"""
import socket
import threading
from http.server import ThreadingHTTPServer

import pytest

from app.mock_shop import Handler

APP_HOST, APP_PORT = "127.0.0.1", 8791


@pytest.fixture(scope="session", autouse=True)
def local_app():
    """Serve the practice shop in a background thread (skipped if already running)."""
    with socket.socket() as probe:
        already_running = probe.connect_ex((APP_HOST, APP_PORT)) == 0
    if already_running:
        yield
        return
    server = ThreadingHTTPServer((APP_HOST, APP_PORT), Handler)
    thread = threading.Thread(target=server.serve_forever, daemon=True)
    thread.start()
    yield
    server.shutdown()


# =============================== YOUR WORK BELOW ===============================
# TODO (Task 2a): session-scoped, autouse fixture `configure_test_id(playwright)` that calls
#                 playwright.selectors.set_test_id_attribute("data-test")
#                 (this app uses data-test, not data-testid; needed as soon as a page object
#                 uses get_by_test_id).
# TODO (Task 3a): fixtures `login_page(page)` and `inventory_page(login_page, users)`.
# TODO (Task 3b): session fixtures `users` and `customer` that read JSON via utils.data_loader
#                 (inline dicts are fine until Task 4 gives you the loader).
# TODO (Task 3c): override `browser_context_args` (EXTEND the built-in, do not replace it).
# TODO (Task 3d): autouse fixture `log_test_boundaries(request)` with a `yield`.
# TODO (Task 3e): hook `pytest_runtest_makereport` (hookwrapper) -> screenshot on failure.
# TODO (Task 7):  `pytest_html_report_title` + project metadata via `pytest_configure`.
