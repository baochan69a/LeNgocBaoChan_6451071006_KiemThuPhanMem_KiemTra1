"""Page object for the UTC electronic-office login form."""

from urllib.parse import urlsplit

import allure
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

from src.test.python.e2e.base.base_test import BASE_URL, HOME_URL
from src.test.python.e2e.pages.base_page import BasePage

INVALID_LOGIN_MESSAGES = (
    "Tài khoản không đúng",
    "Tài khoản hoặc mật khẩu không đúng.",
)


class LoginPage(BasePage):
    USERNAME = (By.NAME, "username")
    PASSWORD = (By.NAME, "userpwd")
    REMEMBER = (By.ID, "persistent")
    SUBMIT = (By.CSS_SELECTOR, 'form input[type="submit"], form button[type="submit"]')

    @allure.step("Mở trang đăng nhập")
    def open(self) -> None:
        self.driver.get(BASE_URL)
        self.find(self.USERNAME)

    @allure.step("Nhập thông tin đăng nhập")
    def fill(self, username: str | None = None, password: str | None = None) -> None:
        if username is not None:
            self.type_text(self.USERNAME, username)
        if password is not None:
            self.type_text(self.PASSWORD, password)

    @allure.step("Chọn giữ đăng nhập")
    def enable_remember_me(self) -> None:
        checkbox = self.find(self.REMEMBER)
        if not checkbox.is_selected():
            checkbox.click()

    @allure.step("Gửi thông tin đăng nhập")
    def submit(self) -> None:
        self.click(self.SUBMIT)

    @allure.step("Gửi thông tin đăng nhập bằng phím Enter")
    def submit_with_enter(self) -> None:
        self.find(self.PASSWORD).send_keys(Keys.ENTER)

    def is_form_visible(self) -> bool:
        return self.visible(self.USERNAME)

    @allure.step("Xác nhận thông báo: {expected_message}")
    def assert_error(self, expected_message: str) -> None:
        self.wait.until(lambda _driver: expected_message in self.body_text)
        assert self.is_form_visible(), "Sai đăng nhập nhưng không còn ở màn hình đăng nhập."

    @allure.step("Xác nhận thông báo sai thông tin đăng nhập")
    def assert_invalid_credentials(self) -> None:
        self.wait.until(
            lambda _driver: any(message in self.body_text for message in INVALID_LOGIN_MESSAGES)
        )
        assert self.is_form_visible(), "Sai đăng nhập nhưng không còn ở màn hình đăng nhập."

    def assert_login_page(self) -> None:
        self.wait.until(lambda _driver: self.is_form_visible())

    def assert_logged_in(self) -> None:
        self.wait.until(
            lambda _driver: (
                urlsplit(self.driver.current_url).path.rstrip("/").lower() != "/login"
                and not self.is_form_visible()
            )
        )

    def assert_login_denied_or_succeeded(self) -> str:
        result = self.wait.until(
            lambda _driver: (
                "Đăng nhập thành công"
                if not self.is_form_visible()
                else next(
                    (message for message in INVALID_LOGIN_MESSAGES if message in self.body_text),
                    False,
                )
            )
        )
        return result

    @allure.step("Mở trang chủ trực tiếp")
    def open_home(self) -> None:
        self.driver.get(HOME_URL)

    def assert_password_is_masked(self) -> None:
        assert self.find(self.PASSWORD).get_attribute("type") == "password"
