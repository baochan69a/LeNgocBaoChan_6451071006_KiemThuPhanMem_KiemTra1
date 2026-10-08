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


@allure.epic("UTC E-Office")
@allure.feature("Đăng nhập")
@allure.id("TC4")
@allure.title("TC4 - Username sai")
@allure.severity(allure.severity_level.NORMAL)
@pytest.mark.negative
def test_TC4_wrong_user(driver):
    login = LoginPage(driver)
    login.open()
    login.fill(username="huongthunguyen", password="Sai@Pass#9999")
    login.submit()
    login.assert_invalid_credentials()


@allure.epic("UTC E-Office")
@allure.feature("Đăng nhập duy trì phiên")
@allure.id("TC5")
@allure.title("TC5 - Giữ đăng nhập sau khi mở lại trình duyệt")
@allure.severity(allure.severity_level.NORMAL)
@pytest.mark.skipif(not VALID_PASS, reason=PASSWORD_SKIP_REASON)
def test_TC5_keep_login(browser_factory):
    create, close = browser_factory
    profile = "tc5-profile"
    login = LoginPage(create(profile_name=profile))
    login.open()
    login.fill(username=VALID_USER, password=require_valid_password())
    login.enable_remember_me()
    login.submit()
    login.assert_logged_in()
    close(login.driver)

    reopened = LoginPage(create(profile_name=profile))
    reopened.open_home()
    reopened.assert_logged_in()


@allure.epic("UTC E-Office")
@allure.feature("Đăng nhập duy trì phiên")
@allure.id("TC6")
@allure.title("TC6 - Không giữ đăng nhập sau khi mở lại trình duyệt")
@allure.severity(allure.severity_level.NORMAL)
@pytest.mark.skipif(not VALID_PASS, reason=PASSWORD_SKIP_REASON)
def test_TC6_no_keep_login(browser_factory):
    create, close = browser_factory
    profile = "tc6-profile"
    login = LoginPage(create(profile_name=profile))
    login.open()
    login.fill(username=VALID_USER, password=require_valid_password())
    login.submit()
    login.assert_logged_in()
    close(login.driver)

    reopened = LoginPage(create(profile_name=profile))
    reopened.open_home()
    reopened.assert_login_page()


@allure.epic("UTC E-Office")
@allure.feature("Đăng nhập")
@allure.id("TC7")
@allure.title("TC7 - Bỏ trống username và password")
@allure.severity(allure.severity_level.NORMAL)
@pytest.mark.negative
def test_TC7_empty_both(driver):
    login = LoginPage(driver)
    login.open()
    login.submit()
    login.assert_error("Bạn chưa nhập tên đăng nhập")


@allure.epic("UTC E-Office")
@allure.feature("Đăng nhập")
@allure.id("TC8")
@allure.title("TC8 - Username và password đều sai")
@allure.severity(allure.severity_level.NORMAL)
@pytest.mark.negative
def test_TC8_wrong_both(driver):
    login = LoginPage(driver)
    login.open()
    login.fill(username="abc123", password="abc@123")
    login.submit()
    login.assert_invalid_credentials()


@allure.epic("UTC E-Office")
@allure.feature("Đăng nhập")
@allure.id("TC9")
@allure.title("TC9 - Password phân biệt chữ hoa và chữ thường")
@allure.severity(allure.severity_level.NORMAL)
@pytest.mark.negative
@pytest.mark.skipif(not VALID_PASS, reason=PASSWORD_SKIP_REASON)
def test_TC9_pass_case_sensitive(driver):
    login = LoginPage(driver)
    login.open()
    login.fill(username=VALID_USER, password=require_valid_password().upper())
    login.submit()
    login.assert_invalid_credentials()


@allure.epic("UTC E-Office")
@allure.feature("Đăng nhập")
@allure.id("TC10")
@allure.title("TC10 - Username viết hoa toàn bộ")
@allure.severity(allure.severity_level.NORMAL)
@pytest.mark.skipif(not VALID_PASS, reason=PASSWORD_SKIP_REASON)
def test_TC10_username_uppercase(driver):
    login = LoginPage(driver)
    login.open()
    login.fill(username=VALID_USER.upper(), password=require_valid_password())
    login.submit()
    result = login.assert_login_denied_or_succeeded()
    allure.attach(result, name="Kết quả thực tế", attachment_type=allure.attachment_type.TEXT)


@allure.epic("UTC E-Office")
@allure.feature("Đăng nhập")
@allure.id("TC11")
@allure.title("TC11 - Username có dấu cách ở hai đầu")
@allure.severity(allure.severity_level.NORMAL)
@pytest.mark.skipif(not VALID_PASS, reason=PASSWORD_SKIP_REASON)
def test_TC11_username_spaces_around(driver):
    login = LoginPage(driver)
    login.open()
    login.fill(username=f" {VALID_USER} ", password=require_valid_password())
    login.submit()
    result = login.assert_login_denied_or_succeeded()
    allure.attach(result, name="Kết quả thực tế", attachment_type=allure.attachment_type.TEXT)


@allure.epic("UTC E-Office")
@allure.feature("Đăng nhập")
@allure.id("TC12")
@allure.title("TC12 - Username chỉ chứa dấu cách")
@allure.severity(allure.severity_level.NORMAL)
@pytest.mark.negative
def test_TC12_username_only_spaces(driver):
    login = LoginPage(driver)
    login.open()
    login.fill(username="   ", password="Sai@Pass#9999")
    login.submit()
    login.assert_error("Bạn chưa nhập tên đăng nhập")


@allure.epic("UTC E-Office")
@allure.feature("Đăng nhập")
@allure.id("TC13")
@allure.title("TC13 - Username dài 256 ký tự")
@allure.severity(allure.severity_level.NORMAL)
@pytest.mark.negative
def test_TC13_username_too_long(driver):
    login = LoginPage(driver)
    login.open()
    login.fill(username="a" * 256, password="Sai@Pass#9999")
    login.submit()
    login.wait.until(
        lambda _driver: any(message in login.body_text for message in INVALID_LOGIN_MESSAGES)
    )
    assert login.is_form_visible(), "Username quá dài nhưng không ở lại màn hình đăng nhập."


@allure.epic("UTC E-Office")
@allure.feature("Đăng nhập")
@allure.id("TC14")
@allure.title("TC14 - Password được che")
@allure.severity(allure.severity_level.MINOR)
def test_TC14_password_masked(driver):
    login = LoginPage(driver)
    login.open()
    login.fill(password="Sai@Pass#9999")
    login.assert_password_is_masked()


@allure.epic("UTC E-Office")
@allure.feature("Đăng nhập")
@allure.id("TC15")
@allure.title("TC15 - Đăng nhập sai bằng phím Enter")
@allure.severity(allure.severity_level.NORMAL)
@pytest.mark.negative
def test_TC15_wrong_login_with_enter(driver):
    login = LoginPage(driver)
    login.open()
    login.fill(username=VALID_USER, password="Sai@Pass#9999")
    login.submit_with_enter()
    login.assert_invalid_credentials()


@allure.epic("UTC E-Office")
@allure.feature("Đăng nhập")
@allure.id("TC16")
@allure.title("TC16 - Đăng nhập đúng bằng phím Enter")
@allure.severity(allure.severity_level.NORMAL)
@pytest.mark.skipif(not VALID_PASS, reason=PASSWORD_SKIP_REASON)
def test_TC16_login_with_enter(driver):
    login = LoginPage(driver)
    login.open()
    login.fill(username=VALID_USER, password=require_valid_password())
    login.submit_with_enter()
    login.assert_logged_in()


@allure.epic("UTC E-Office")
@allure.feature("Đăng nhập duy trì phiên")
@allure.id("TC17")
@allure.title("TC17 - Giữ đăng nhập nhưng password sai")
@allure.severity(allure.severity_level.NORMAL)
@pytest.mark.negative
def test_TC17_keep_login_but_wrong_pass(browser_factory):
    create, close = browser_factory
    profile = "tc17-profile"
    login = LoginPage(create(profile_name=profile))
    login.open()
    login.fill(username=VALID_USER, password="Sai@Pass#9999")
    login.enable_remember_me()
    login.submit()
    login.assert_invalid_credentials()
    close(login.driver)

    reopened = LoginPage(create(profile_name=profile))
    reopened.open_home()
    reopened.assert_login_page()


@allure.epic("UTC E-Office")
@allure.feature("Đăng xuất")
@allure.id("TC18")
@allure.title("TC18 - Không truy cập lại trang chủ sau logout bằng Back")
@allure.severity(allure.severity_level.NORMAL)
@pytest.mark.skipif(not VALID_PASS, reason=PASSWORD_SKIP_REASON)
def test_TC18_back_after_logout(driver):
    login = LoginPage(driver)
    login.open()
    login.fill(username=VALID_USER, password=require_valid_password())
    login.submit()
    DashboardPage(driver).assert_logged_in()
    DashboardPage(driver).logout()
    driver.back()
    login.assert_login_page()


@allure.epic("UTC E-Office")
@allure.feature("Bảo vệ trang yêu cầu đăng nhập")
@allure.id("TC19")
@allure.title("TC19 - Truy cập trang chủ khi chưa đăng nhập")
@allure.severity(allure.severity_level.NORMAL)
@pytest.mark.negative
def test_TC19_home_without_login(driver):
    login = LoginPage(driver)
    login.open_home()
    login.assert_login_page()


@allure.epic("UTC E-Office")
@allure.feature("Đăng nhập đa trình duyệt")
@allure.id("TC20")
@allure.title("TC20 - Đăng nhập trên Chrome, Firefox và Edge")
@allure.severity(allure.severity_level.NORMAL)
@pytest.mark.skipif(not VALID_PASS, reason=PASSWORD_SKIP_REASON)
def test_TC20_cross_browser(browser_factory, tmp_path):
    browsers = ("chrome", "firefox", "edge")
    executables = {
        "chrome": (
            "chrome",
            Path(r"C:\Program Files\Google\Chrome\Application\chrome.exe"),
            Path(r"C:\Program Files (x86)\Google\Chrome\Application\chrome.exe"),
        ),
        "firefox": ("firefox", Path(r"C:\Program Files\Mozilla Firefox\firefox.exe")),
        "edge": (
            "msedge",
            Path(r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe"),
            Path(r"C:\Program Files\Microsoft\Edge\Application\msedge.exe"),
        ),
    }
    missing = []
    for browser in browsers:
        executable, *paths = executables[browser]
        if not shutil.which(executable) and not any(path.is_file() for path in paths):
            missing.append(browser)
    if missing:
        pytest.skip(f"Chưa cài trình duyệt: {', '.join(missing)}")

    create, close = browser_factory
    for browser in browsers:
        current = LoginPage(create(browser, f"{browser}-profile"))
        try:
            current.open()
            current.fill(username=VALID_USER, password=require_valid_password())
            current.submit()
            current.assert_logged_in()
        finally:
            close(current.driver)


@allure.epic("UTC E-Office")
@allure.feature("Bảo mật đăng nhập")
@allure.id("TC21")
@allure.title("TC21 - Ngăn chặn SQL Injection")
@allure.severity(allure.severity_level.CRITICAL)
@pytest.mark.negative
@pytest.mark.skipif(not RUN_RISKY, reason=RISKY_SKIP_REASON)
def test_TC21_sql_injection(driver):
    login = LoginPage(driver)
    login.open()
    injection = "' OR '1'='1"
    login.fill(username=injection, password=injection)
    login.submit()
    login.assert_invalid_credentials()
    body = login.body_text.lower()
    for database_error in ("sql syntax", "database error", "stack trace", "mysql", "sql server"):
        assert database_error not in body


@allure.epic("UTC E-Office")
@allure.feature("Bảo mật đăng nhập")
@allure.id("TC22")
@allure.title("TC22 - Không thực thi XSS trong username")
@allure.severity(allure.severity_level.CRITICAL)
@pytest.mark.negative
@pytest.mark.skipif(not RUN_RISKY, reason=RISKY_SKIP_REASON)
def test_TC22_xss(driver):
    login = LoginPage(driver)
    login.open()
    login.fill(username="<script>alert(1)</script>", password="Sai@Pass#9999")
    login.submit()
    with pytest.raises(TimeoutException):
        WebDriverWait(driver, 2).until(EC.alert_is_present())
    login.assert_invalid_credentials()


@allure.epic("UTC E-Office")
@allure.feature("Bảo mật đăng nhập")
@allure.id("TC23")
@allure.title("TC23 - Phản hồi khi đăng nhập sai liên tục")
@allure.severity(allure.severity_level.CRITICAL)
@pytest.mark.negative
@pytest.mark.skipif(not RUN_RISKY, reason=RISKY_SKIP_REASON)
def test_TC23_many_wrong_attempts(driver):
    login = LoginPage(driver)
    login.open()
    for attempt in range(5):
        login.find(login.USERNAME).clear()
        login.find(login.PASSWORD).clear()
        login.fill(username=VALID_USER, password="Sai@Pass#9999")
        login.submit()
        login.wait.until(
            lambda _driver: (
                "không đúng" in login.body_text.lower()
                or "captcha" in login.body_text.lower()
                or "khóa" in login.body_text.lower()
                or not login.is_form_visible()
            )
        )
        body = login.body_text.lower()
        assert login.is_form_visible(), "Sai mật khẩu nhưng đã vào được hệ thống."
        assert (
            "không đúng" in body or "captcha" in body or "khóa" in body
        ), f"Lần thử {attempt + 1}: không tìm thấy phản hồi sai mật khẩu/captcha/khóa tài khoản."
        if "captcha" in body or "khóa" in body:
            break
