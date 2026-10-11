"""Task 2 and Task 3: login scenarios (Project 1 milestone: scenarios 1 and 2)."""
import re

import pytest
from playwright.sync_api import Page, expect


# ---------------------------------------------------------------- Scenario 1
@pytest.mark.offline
@pytest.mark.project1
def test_valid_login_reaches_shop(login_page: Page):
    """P1 scenario 1 (manual case TC-UI-01): a valid user can sign in."""
    # TODO Arrange: nothing to do, the `login_page` fixture already opened the page.
    # TODO Act: fill Email and Password (use get_by_label), click the Sign in button (get_by_role).
    # TODO Assert (web-first!): URL ends with /shop.html AND the heading "Shop" is visible
    #      AND the welcome text contains the e-mail you used.
    pytest.skip("TODO: implement test_valid_login_reaches_shop")


# ---------------------------------------------------------------- Scenario 2
@pytest.mark.offline
@pytest.mark.project1
@pytest.mark.parametrize(
    "email, password, expected_message",
    [
        # TODO: add the cases from the README table (at least 4 rows incl. the locked-out account).
        # ("tester@gadgethub.test", "wrong", "Invalid email or password"),
    ],
    ids=[],
)
def test_invalid_login_shows_error(login_page: Page, email, password, expected_message):
    """P1 scenario 2 (manual case TC-UI-02): bad logins show a message and stay on the sign-in page."""
    # TODO: fill both fields (an empty string is fine for fill), click Sign in,
    #       expect the alert (get_by_role("alert") OR get_by_test_id("login-error")) to contain the message,
    #       and expect the URL NOT to contain "shop".
    pytest.skip("TODO: implement test_invalid_login_shows_error")


# ---------------------------------------------------------------- Task 3
@pytest.mark.offline
def test_protected_page_redirects_when_not_signed_in(login_page: Page):
    """Extra thinking test: opening /shop.html directly (no sign-in) must bounce back to sign-in.
    Hint: login_page already has the site installed. Use page.goto, then a web-first URL assertion."""
    # TODO: goto SITE_URL + "/shop.html"; expect the title to be "GadgetHub - Sign in".
    pytest.skip("TODO: implement test_protected_page_redirects_when_not_signed_in")
