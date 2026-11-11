from playwright.sync_api import Page

from pages.base_page import BasePage


class LoginPage(BasePage):
    URL = "/login.html"

    def __init__(self, page: Page):
        super().__init__(page)
        self.username_input = page.get_by_label("Username")
        self.password_input = page.get_by_label("Password")
        self.login_button = page.get_by_role("button", name="Log in")
        self.error_message = page.get_by_role("alert")

    def login(self, username: str, password: str) -> None:
        self.username_input.fill(username)
        self.password_input.fill(password)
        self.login_button.click()