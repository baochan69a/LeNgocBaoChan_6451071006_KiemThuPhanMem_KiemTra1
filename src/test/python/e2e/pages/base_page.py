"""Common Selenium interactions used by page objects."""

from selenium.common.exceptions import (
    NoSuchElementException,
    StaleElementReferenceException,
)
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support.ui import WebDriverWait

from src.test.python.e2e.base.base_test import WAIT_SECONDS


class BasePage:
    def __init__(self, driver: WebDriver):
        self.driver = driver
        self.wait = WebDriverWait(
            driver,
            WAIT_SECONDS,
            ignored_exceptions=(StaleElementReferenceException,),
        )

    def visible(self, locator: tuple[str, str]) -> bool:
        try:
            return self.driver.find_element(*locator).is_displayed()
        except (NoSuchElementException, StaleElementReferenceException):
            return False

    def find(self, locator: tuple[str, str]) -> WebElement:
        return self.wait.until(lambda driver: driver.find_element(*locator))

    def click(self, locator: tuple[str, str]) -> None:
        self.wait.until(lambda driver: self.find(locator).is_displayed())
        self.find(locator).click()

    def type_text(self, locator: tuple[str, str], value: str) -> None:
        self.find(locator).send_keys(value)

    @property
    def body_text(self) -> str:
        return self.driver.find_element("tag name", "body").text
