from playwright.sync_api import Page

from pages.base_page import BasePage


class CheckoutPage(BasePage):
    URL = "/checkout.html"

    def __init__(self, page: Page):
        super().__init__(page)
        # Step 1: details
        self.first_name_input = page.get_by_label("First name")
        self.last_name_input = page.get_by_label("Last name")
        self.postcode_input = page.get_by_label("Postcode")
        self.continue_button = page.get_by_role("button", name="Continue")
        self.error_message = page.get_by_role("alert")
        # Step 2: summary
        self.summary_items = page.locator("#summary-items li")
        self.item_total = page.locator("#item-total")
        self.tax = page.locator("#tax")
        self.total = page.locator("#total")
        self.place_order_button = page.get_by_role("button", name="Place order")
        # Step 3: complete
        self.complete_heading = page.get_by_role("heading", name="Thank you for your order!")

    def enter_details(self, first_name: str, last_name: str, postcode: str) -> None:
        self.first_name_input.fill(first_name)
        self.last_name_input.fill(last_name)
        self.postcode_input.fill(postcode)
        self.continue_button.click()

    def place_order(self) -> None:
        self.place_order_button.click()