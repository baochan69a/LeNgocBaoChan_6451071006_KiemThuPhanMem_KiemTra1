"""Shared WebDriver setup and test configuration."""

import os
from collections.abc import Callable
from pathlib import Path

import pytest
from selenium import webdriver

BASE_URL = "https://vanphongdientu.utc.edu.vn"
HOME_URL = f"{BASE_URL}/"
VALID_USER = os.getenv("VALID_USER", "huongnt")
VALID_PASS = os.getenv("VALID_PASS")
RUN_RISKY = os.getenv("RUN_RISKY") == "1"
WAIT_SECONDS = 10


def create_driver(browser: str = "chrome", profile_dir: Path | None = None):
    if browser == "chrome":
        options = webdriver.ChromeOptions()
        if os.getenv("HEADLESS", "1") != "0":
            options.add_argument("--headless=new")
        options.add_argument("--window-size=1440,1000")
        if profile_dir is not None:
            options.add_argument(f"--user-data-dir={profile_dir}")
        return webdriver.Chrome(options=options)

    if browser == "edge":
        options = webdriver.EdgeOptions()
        if os.getenv("HEADLESS", "1") != "0":
            options.add_argument("--headless=new")
        options.add_argument("--window-size=1440,1000")
        if profile_dir is not None:
            options.add_argument(f"--user-data-dir={profile_dir}")
        return webdriver.Edge(options=options)

    if browser == "firefox":
        options = webdriver.FirefoxOptions()
        if os.getenv("HEADLESS", "1") != "0":
            options.add_argument("-headless")
        if profile_dir is not None:
            profile_dir.mkdir(parents=True, exist_ok=True)
            options.add_argument("-profile")
            options.add_argument(str(profile_dir))
        return webdriver.Firefox(options=options)

    raise ValueError(f"Trình duyệt không được hỗ trợ: {browser}")


@pytest.fixture
def browser_factory(tmp_path):
    active_drivers = []

    def create(browser: str = "chrome", profile_name: str | None = None):
        profile = tmp_path / profile_name if profile_name else None
        browser_driver = create_driver(browser, profile)
        active_drivers.append(browser_driver)
        return browser_driver

    def close(browser_driver):
        browser_driver.quit()
        active_drivers.remove(browser_driver)

    yield create, close

    for browser_driver in active_drivers:
        browser_driver.quit()


@pytest.fixture
def driver(browser_factory):
    create, close = browser_factory
    browser_driver = create()
    try:
        yield browser_driver
    finally:
        close(browser_driver)


def require_valid_password() -> str:
    if not VALID_PASS:
        pytest.skip("Thiếu biến môi trường VALID_PASS để chạy ca cần đăng nhập thành công.")
    return VALID_PASS
