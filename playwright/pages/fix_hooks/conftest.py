"""Shared fixtures for Lecture 7.

pytest loads this file automatically for every test in this folder
(and its subfolders). Tests never import it.
"""
import threading
from functools import partial
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path

import pytest
from playwright.sync_api import Browser, Page

SITE_DIR = Path(__file__).parent / "site"


# ---------- A tiny web server for the practice site (session scope) ----------

class QuietHandler(SimpleHTTPRequestHandler):
    def log_message(self, *args):
        pass  # don't print every request


@pytest.fixture(scope="session")
def server():
    """Start a local web server once for the whole test run."""
    handler = partial(QuietHandler, directory=SITE_DIR)
    httpd = ThreadingHTTPServer(("127.0.0.1", 0), handler)   # port 0 = any free port
    threading.Thread(target=httpd.serve_forever, daemon=True).start()
    print(f"\n[server] started on port {httpd.server_port}")

    yield f"http://127.0.0.1:{httpd.server_port}"            # ---- tests run here ----

    httpd.shutdown()
    print("\n[server] stopped")


@pytest.fixture(scope="session")
def base_url(server):
    """Override pytest-playwright's base_url so page.goto("/login.html") works."""
    return server


# ---------- Helper ----------

def log_in(page: Page, username: str, password: str = "secret123") -> None:
    page.goto("/login.html")
    page.get_by_label("Username").fill(username)
    page.get_by_label("Password").fill(password)
    page.get_by_role("button", name="Log in").click()
    page.wait_for_url("**/account.html")


# ---------- Page fixtures ----------

@pytest.fixture
def login_page(page: Page) -> Page:
    """A page that starts on the login screen."""
    page.goto("/login.html")
    return page


@pytest.fixture
def ui_logged_in_page(page: Page) -> Page:
    """Logs in through the UI before EVERY test (slow: ~1 second each)."""
    log_in(page, "student")
    return page


@pytest.fixture
def login_as(new_context):
    """A "factory" fixture: returns a function that logs in any user in a new context."""
    def _login_as(username: str) -> Page:
        page = new_context().new_page()
        log_in(page, username)
        return page
    return _login_as


# ---------- Saved login state (storage_state) ----------

@pytest.fixture(scope="session")
def student_state(browser: Browser, base_url: str, tmp_path_factory) -> Path:
    """Log in ONCE per test run and save cookies + localStorage to a file."""
    context = browser.new_context(base_url=base_url)
    page = context.new_page()
    log_in(page, "student")

    state_file = tmp_path_factory.mktemp("auth") / "student.json"
    context.storage_state(path=state_file)
    context.close()
    return state_file


@pytest.fixture
def logged_in_page(new_context, student_state: Path) -> Page:
    """A NEW context for each test, already logged in from the saved state."""
    context = new_context(storage_state=student_state)
    page = context.new_page()
    page.goto("/account.html")
    return page