from playwright.sync_api import Locator, Page

from pages.base_page import BasePage


class ProductsPage(BasePage):
    URL = "/products.html"

    def __init__(self, page: Page):
        super().__init__(page)
        self.heading = page.get_by_role("heading", name="Products")
        self.sort_dropdown = page.get_by_label("Sort by")
        self.products = page.locator(".product")
        self.product_names = page.locator(".product h3")
        self.product_prices = page.locator(".product .price")

    def product(self, name: str) -> Locator:
        """The card for one product."""
        return self.products.filter(has=self.page.get_by_role("heading", name=name, exact=True))

    def add_to_cart(self, *names: str) -> None:
        for name in names:
            self.product(name).get_by_role("button", name="Add to cart").click()

    def remove_from_cart(self, name: str) -> None:
        self.product(name).get_by_role("button", name="Remove").click()

    def price_of(self, name: str) -> str:
        return self.product(name).locator(".price").text_content()

    def sort_by(self, option: str) -> None:
        self.sort_dropdown.select_option(label=option)

    def get_product_names(self) -> list[str]:
        return self.product_names.all_text_contents()

    def get_prices(self) -> list[float]:
        return [float(p.replace("$", "")) for p in self.product_prices.all_text_contents()]