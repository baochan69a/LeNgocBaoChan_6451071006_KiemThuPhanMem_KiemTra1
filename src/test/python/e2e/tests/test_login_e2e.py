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


