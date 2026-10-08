"""End-to-end login test cases for the UTC electronic-office website."""

import shutil
from pathlib import Path

import allure
import pytest
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

from src.test.python.e2e.base.base_test import (
    RUN_RISKY,
    VALID_PASS,
    VALID_USER,
    WAIT_SECONDS,
    require_valid_password,
)
from src.test.python.e2e.pages.dashboard_page import DashboardPage
from src.test.python.e2e.pages.login_page import INVALID_LOGIN_MESSAGES, LoginPage

RISKY_SKIP_REASON = "Ca kiểm thử rủi ro chỉ chạy khi RUN_RISKY=1."
PASSWORD_SKIP_REASON = "Thiếu biến môi trường VALID_PASS."


@allure.epic("UTC E-Office")
@allure.feature("Đăng nhập")
@allure.id("TC1")
@allure.title("TC1 - Bỏ trống username")
@allure.severity(allure.severity_level.NORMAL)
@pytest.mark.negative
def test_TC1_empty_user(driver):
    login = LoginPage(driver)
    login.open()
    login.fill(password="Sai@Pass#9999")
    login.submit()
    login.assert_error("Bạn chưa nhập tên đăng nhập")


@allure.epic("UTC E-Office")
@allure.feature("Đăng nhập")
@allure.id("TC2")
@allure.title("TC2 - Bỏ trống password")
@allure.severity(allure.severity_level.NORMAL)
@pytest.mark.negative
def test_TC2_empty_pass(driver):
    login = LoginPage(driver)
    login.open()
    login.fill(username=VALID_USER)
    login.submit()
    login.assert_error("Bạn chưa nhập mật khẩu")


@allure.epic("UTC E-Office")
@allure.feature("Đăng nhập")
@allure.id("TC3")
@allure.title("TC3 - Username đúng, password sai")
@allure.severity(allure.severity_level.NORMAL)
@pytest.mark.negative
def test_TC3_right_user_wrong_pass(driver):
    login = LoginPage(driver)
    login.open()
    login.fill(username=VALID_USER, password="Sai@Pass#9999")
    login.submit()
    login.assert_invalid_credentials()


