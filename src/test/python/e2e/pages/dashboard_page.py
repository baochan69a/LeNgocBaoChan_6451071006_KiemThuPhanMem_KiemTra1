"""Page object for authenticated-page checks and logout."""

from selenium.webdriver.common.by import By

from src.test.python.e2e.pages.base_page import BasePage
from src.test.python.e2e.pages.login_page import LoginPage


class DashboardPage(BasePage):
    LOGOUT = (
        By.XPATH,
        "//a[contains(normalize-space(.), 'Đăng xuất')] | "
        "//button[contains(normalize-space(.), 'Đăng xuất')]",
    )

    def assert_logged_in(self) -> None:
        LoginPage(self.driver).assert_logged_in()

    def logout(self) -> None:
        self.click(self.LOGOUT)
        LoginPage(self.driver).assert_login_page()
