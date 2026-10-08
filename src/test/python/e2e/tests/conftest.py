"""Pytest fixtures and Allure attachments for browser tests."""

import allure
import pytest

from src.test.python.e2e.base.base_test import browser_factory, driver


@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item, call):
    outcome = yield
    report = outcome.get_result()
    if report.when == "call" and report.failed:
        browser = item.funcargs.get("driver")
        if browser is not None:
            allure.attach(
                browser.get_screenshot_as_png(),
                name=f"{item.name}-failure",
                attachment_type=allure.attachment_type.PNG,
            )
