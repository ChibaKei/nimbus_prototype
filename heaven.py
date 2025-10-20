from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import (
    TimeoutException,
    NoSuchElementException,
    ElementClickInterceptedException,
    StaleElementReferenceException,
    ElementNotInteractableException,
)
from webdriver_manager.chrome import ChromeDriverManager
import os
import time


def heaven_login(username: str = "", password: str = "", headless: bool = True) -> webdriver.Chrome:
    """CityHeaven 管理画面にログインし、ログイン済みの WebDriver を返す。

    環境変数 ``HEAVEN_USERNAME`` / ``HEAVEN_PASSWORD`` が設定されていれば、
    引数が空文字のときにそれらを自動利用する。
    失敗時はドライバーを確実に終了して例外を送出する。
    """
    if not username:
        username = os.environ.get("HEAVEN_USERNAME", "")
    if not password:
        password = os.environ.get("HEAVEN_PASSWORD", "")

    if not username or not password:
        raise ValueError("username/password が指定されていません (引数または環境変数を設定してください)")

    options = webdriver.ChromeOptions()
    if headless:
        options.add_argument("--headless")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--disable-gpu")
    options.add_argument("--window-size=1920,1080")
    options.add_argument("--start-maximized")
    options.add_argument("--disable-blink-features=AutomationControlled")
    options.add_experimental_option("excludeSwitches", ["enable-automation"])
    options.add_experimental_option("useAutomationExtension", False)

    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=options)

    driver.execute_cdp_cmd(
        "Page.addScriptToEvaluateOnNewDocument",
        {"source": "Object.defineProperty(navigator, 'webdriver', {get: () => undefined})"},
    )
    driver.implicitly_wait(5)

    wait = WebDriverWait(driver, 10)
    login_url = "https://newmanager.cityheaven.net"

    try:
        driver.get(login_url)
        
        # ページ読み込み待機
        time.sleep(1)
        # フォームの表示を待機
        wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, ".oldLogin input[name='txt_account']")))

        # ユーザー名フィールドを探して入力（oldLoginフォーム内を指定）
        heaven_id = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, ".oldLogin input[name='txt_account']")))
        heaven_id.click()
        heaven_id.send_keys(username)
        time.sleep(1)

        # パスワードフィールドを探して入力（oldLoginフォーム内を指定）
        heaven_pass = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, ".oldLogin input[name='txt_password']")))
        heaven_pass.click()
        heaven_pass.send_keys(password)
        time.sleep(1)

        # ログインボタンをクリック（oldLoginフォーム内を指定）
        login_button = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, ".oldLogin button[name='login']")))
        login_button.click()
        
        # ログイン後のページ遷移を待機
        wait.until(lambda d: d.current_url != login_url)

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


if __name__ == "__main__":
    # 例: 環境変数を設定して実行、または引数で渡す
    heaven_login()