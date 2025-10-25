import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait, Select
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import (
    TimeoutException,
    NoSuchElementException,
    ElementClickInterceptedException,
    StaleElementReferenceException,
    ElementNotInteractableException,
)
from utils.selenium_utils import click_element_by_script, handle_alert
from .base_login import create_chrome_driver, create_webdriver_wait
import os
import time
import random
from utils import utilities
import io

# Windows環境での文字化け対策
if sys.platform == "win32":
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8')



def town_login(username: str = "", password: str = "", headless: bool = True) -> webdriver.Chrome:
    """デリヘルタウンにログインし、ログイン済みの WebDriver を返す。

    環境変数 ``TOWN_USERNAME`` / ``TOWN_PASSWORD`` が設定されていれば、
    引数が空文字のときにそれらを自動利用する。
    失敗時はドライバーを確実に終了して例外を送出する。
    """
    if not username:
        username = os.environ.get("TOWN_USERNAME", "")
    if not password:
        password = os.environ.get("TOWN_PASSWORD", "")

    if not username or not password:
        raise ValueError("username/password が指定されていません (引数または環境変数を設定してください)")

    driver = create_chrome_driver(headless, incognito=True)
    wait = create_webdriver_wait(driver, 10)
    login_url = "https://admin.dto.jp/a/auth"
    driver.get(login_url)
    wait.until(EC.presence_of_element_located((By.ID, "login_id")))

    try:
        town_id = wait.until(EC.element_to_be_clickable((By.NAME, "login_id")))
        town_id.click()
        town_id.send_keys(username)
        time.sleep(0.2)

        town_pass = wait.until(EC.element_to_be_clickable((By.NAME, "password")))
        town_pass.click()
        town_pass.send_keys(password)
        time.sleep(0.2)

        login_button = wait.until(EC.element_to_be_clickable((By.ID, "login_button")))
        login_button.click()
        # ログイン後のページ遷移を待機
        wait.until(lambda d: d.current_url != login_url)
        time.sleep(10)
        return driver

    except (
        TimeoutException,
        ElementClickInterceptedException,
        NoSuchElementException,
        ElementNotInteractableException,
        StaleElementReferenceException,
    ) as e:
        driver.quit()
        raise e
    except Exception:
        driver.quit()
        raise

