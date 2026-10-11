"""Small page-level helpers (provided). They use plain CSS locators from the lessons."""
from locator_catalog import config


def open_login(page):
    page.goto(config.LOGIN_URL)


def login(page, username=config.USERNAME, password=config.PASSWORD):
    """Log in. After this the product page is showing."""
    page.locator("#user-name").fill(username)
    page.locator("#password").fill(password)
    page.locator("#login-button").click()
    if config.SITE == "live":
        # The real site changes URL. count() does not wait, so wait once for the new page.
        # (Friday explains Playwright's auto-waiting properly.)
        page.wait_for_url("**/inventory.html")


def failed_login(page):
    """Submit a wrong password so the error message appears."""
    page.locator("#user-name").fill(config.USERNAME)
    page.locator("#password").fill(config.BAD_PASSWORD)
    page.locator("#login-button").click()
    page.locator("[data-test='error']").wait_for()     # wait until the error exists (Friday: why this works)
