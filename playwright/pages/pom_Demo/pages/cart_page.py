from playwright.sync_api import Locator, Page

from pages.base_page import BasePage


class CartPage(BasePage):
    URL = "/cart.html"

    def __init__(self, page: Page):
        super().__init__(page)
        self.heading = page.get_by_role("heading", name="Your cart")
        self.rows = page.get_by_role("table", name="Cart items").locator("tbody tr")
        self.empty_message = page.get_by_text("Your cart is empty")
        self.subtotal = page.locator("#subtotal")
        self.checkout_button = page.get_by_role("button", name="Checkout")
        self.continue_shopping_link = page.get_by_role("link", name="Continue shopping")

    def row(self, name: str) -> Locator:
        return self.rows.filter(has_text=name)

    def remove(self, name: str) -> None:
        self.row(name).get_by_role("button", name="Remove").click()

    def get_item_names(self) -> list[str]:
        return [row.get_by_role("cell").first.text_content() for row in self.rows.all()]

    def checkout(self) -> None:
        self.checkout_button.click()