from playwright.sync_api import Page


class BasePage:
    """Things every page has in common."""

    URL = "/"

    def __init__(self, page: Page):
        self.page = page
        # The header shown on every page after logging in
        self.cart_link = page.get_by_role("link", name="Cart")
        self.products_link = page.get_by_role("link", name="Products", exact=True)
        self.logout_button = page.get_by_role("button", name="Log out")

    def open(self):
        self.page.goto(self.URL)
        return self

    def go_to_cart(self):
        self.cart_link.click()

    def log_out(self):
        self.logout_button.click()