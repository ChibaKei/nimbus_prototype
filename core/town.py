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
    NoAlertPresentException,
)
from utils.selenium_utils import click_element_by_script, handle_alert
from .base_login import create_chrome_driver, create_webdriver_wait
import os
import time
import random
from utils import utilities


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
        time.sleep(0.3)
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


def town_cast_pickup(cast_index: int | None = None, get_count: bool | None = None) -> int | None:
    """デリヘルタウンのキャストをピックアップする。

    Args:
        cast_index: ピックアップするキャストのインデックス（1始まり）。Noneの場合はget_count=Trueである必要がある。
        get_count: Trueの場合、利用可能なキャスト数を返す。FalseまたはNoneの場合はピックアップ処理を実行。

    Returns:
        get_count=Trueの場合、利用可能なキャスト数（int）。それ以外の場合、None。

    Raises:
        ValueError: cast_indexとget_countが両方Noneの場合。
        NoAlertPresentException: アラートが表示されない場合。
        NoSuchElementException: 必要な要素が見つからない場合。
    """
    if cast_index is None and not get_count:
        raise ValueError("cast_indexまたはget_countを指定してください")

    def get_cast_count(driver: webdriver.Chrome) -> int:
        """利用可能なキャスト数を取得する。"""
        try:
            gal_list = driver.find_element(By.XPATH, '//*[@id="gals"]')
            total_count = len(gal_list.find_elements(By.TAG_NAME, 'li'))
            finished_gal_count = len(gal_list.find_elements(By.CLASS_NAME, "disabled"))
            return total_count - finished_gal_count
        except NoSuchElementException:
            return 0
    
    # 認証情報は環境変数またはデフォルト値を使用
    username = os.environ.get("TOWN_USERNAME", "dieselchiba@central-agent.co.jp")
    password = os.environ.get("TOWN_PASSWORD", "dieselchiba")
    standby_url = 'https://admin.dto.jp/shop-admin/34627/standby?order=2'
    
    driver = None
    try:
        driver = town_login(username, password, headless=False)
        time.sleep(0.3)
        driver.get(standby_url)

        if get_count:
            count = get_cast_count(driver)
            return count
        
        if cast_index is None:
            raise ValueError("cast_indexを指定してください")
            
        cast_box = driver.find_element(By.XPATH, f'//*[@id="gals"]/li[{cast_index}]/div/div[4]')
        # 待機中ボタンとチェックボックスの処理
        try:
            cast_box.find_element(By.XPATH, 'a[2]').click()  # 待機中ボタン
            chkbox = driver.find_element(By.XPATH, '//*[@id="one_left_flag"]')
            if not chkbox.is_selected():  # 非選択の場合はJavaScriptでクリックする
                driver.execute_script("arguments[0].click();", chkbox)
            cast_box.find_element(By.XPATH, 'div/div/div/div/a[1]').click()  # 待機中モーダル
            time.sleep(0.3)
        except (
            NoSuchElementException,
            ElementClickInterceptedException,
            ElementNotInteractableException,
            StaleElementReferenceException,
        ):
            pass # 待機中ボタンが存在しない、またはクリックできない場合はスキップ

        # pickupボタンをクリック
        cast_box.find_element(By.XPATH, 'a[3]').click()  # pickupボタン
        
        # アラートを処理（非推奨のswitch_to_alert()を修正）
        try:
            alert = driver.switch_to.alert  # pickupアラート
            alert.accept()
        except NoAlertPresentException:
            # アラートが表示されない場合はスキップ
            pass
        
        time.sleep(0.3)
        return None
        
    finally:
        if driver:
            driver.quit()