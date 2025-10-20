"""
ログイン機能の共通ベースクラス
"""

from dataclasses import dataclass
from typing import Dict, Any, Optional
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import (
    NoSuchElementException,
    ElementClickInterceptedException,
    StaleElementReferenceException,
    TimeoutException,
    ElementNotInteractableException
)
from webdriver_manager.chrome import ChromeDriverManager

@dataclass
class LoginConfig:
    """ログイン設定を管理するデータクラス"""
    url: str
    username_field: str
    password_field: str
    submit_button: Optional[str] = None
    username: str = ""
    password: str = ""

class BaseLogin:
    """ログイン機能の共通ベースクラス"""

    def __init__(self, config: LoginConfig):
        """
        初期化

        Args:
            config (LoginConfig): ログイン設定
        """
        self.config = config
        self.driver = None

    def setup_driver(self, headless: bool = True) -> webdriver.Chrome:
        """
        WebDriverをセットアップする

        Args:
            headless (bool): ヘッドレスモードで実行するかどうか

        Returns:
            webdriver.Chrome: セットアップ済みのWebDriverインスタンス
        """
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

        # webdriver-managerを使用してChromeDriverを自動管理
        service = Service(ChromeDriverManager().install())
        driver = webdriver.Chrome(service=service, options=options)
        driver.execute_cdp_cmd("Page.addScriptToEvaluateOnNewDocument", {
            "source": """
                Object.defineProperty(navigator, 'webdriver', {
                    get: () => undefined
                })
            """
        })
        driver.implicitly_wait(5)  # 待機時間を5秒に調整
        return driver

    def login(self, username: str, password: str, headless: bool = True) -> webdriver.Chrome:
        """
        ログインを実行する

        Args:
            username (str): ユーザー名
            password (str): パスワード
            headless (bool): ヘッドレスモードで実行するかどうか

        Returns:
            webdriver.Chrome: ログイン済みのWebDriverインスタンス

        Raises:
            TimeoutException: ログインフォームの要素が見つからない場合
            ElementClickInterceptedException: クリック操作が妨げられた場合
            StaleElementReferenceException: 要素が古くなった場合
        """
        self.driver = self.setup_driver(headless=headless)
        wait = WebDriverWait(self.driver, 10)  # 待機時間を10秒に調整

        try:
            # ページにアクセス
            self.driver.get(self.config.url)

            # oldLoginクラスのフォームを待機
            form = wait.until(
                EC.presence_of_element_located((By.CLASS_NAME, "oldLogin"))
            )
            wait.until(EC.visibility_of(form))

            # ユーザー名フィールドが操作可能になるまで待機
            username_element = wait.until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, ".oldLogin input[name='txt_account']"))
            )
            wait.until(EC.visibility_of(username_element))
            self.driver.execute_script("arguments[0].value = arguments[1]", username_element, username)

            # パスワードフィールドが操作可能になるまで待機
            password_element = wait.until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, ".oldLogin input[name='txt_password']"))
            )
            wait.until(EC.visibility_of(password_element))
            self.driver.execute_script("arguments[0].value = arguments[1]", password_element, password)

            # 送信ボタンがある場合はクリック
            if self.config.submit_button:
                submit_element = wait.until(
                    EC.element_to_be_clickable((By.NAME, self.config.submit_button))
                )
                wait.until(EC.visibility_of(submit_element))
                submit_element.click()
            else:
                # 送信ボタンがない場合はフォームを送信
                password_element.submit()

            # DOMの遷移完了を待機
            wait.until(EC.staleness_of(password_element))

            # ページの読み込みを待機
            wait.until(lambda driver: driver.current_url != self.config.url)

            return self.driver

        except (TimeoutException, ElementClickInterceptedException, NoSuchElementException, ElementNotInteractableException) as e:
            if self.driver:
                self.driver.quit()
            raise e
        except Exception as e:
            if self.driver:
                self.driver.quit()
            raise Exception(str(e)) 