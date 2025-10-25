"""Selenium の共通ユーティリティ関数"""

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException


def click_element_by_script(driver, wait, selector, delay=1):
    """JavaScript を使用して要素をクリックする。
    
    Args:
        driver: WebDriver インスタンス
        wait: WebDriverWait インスタンス
        selector: CSS セレクター
        delay: クリック後の待機時間（秒）
        
    Raises:
        TimeoutException: 要素が見つからない場合
        NoSuchElementException: 要素が存在しない場合
    """
    try:
        element = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, selector)))
        driver.execute_script("arguments[0].click();", element)
        if delay > 0:
            import time
            time.sleep(delay)
    except (TimeoutException, NoSuchElementException) as e:
        print(f"要素のクリックに失敗しました ({selector}): {e}")
        raise


def handle_alert(driver, expected_text=None, accept=True):
    """アラートを処理する。
    
    Args:
        driver: WebDriver インスタンス
        expected_text: 期待するアラートテキスト（None の場合はテキストをチェックしない）
        accept: True の場合はアラートを承認、False の場合は拒否
        
    Returns:
        bool: アラートが処理された場合は True、アラートが存在しない場合は False
    """
    try:
        alert = driver.switch_to.alert
        alert_text = alert.text
        
        if expected_text and alert_text != expected_text:
            print(f"予期しないアラートテキスト: {alert_text} (期待値: {expected_text})")
            alert.dismiss()
            return False
            
        if accept:
            alert.accept()
            print(f"アラートを承認しました: {alert_text}")
        else:
            alert.dismiss()
            print(f"アラートを拒否しました: {alert_text}")
            
        return True
        
    except Exception:
        # アラートが表示されない場合は何もしない
        return False


def wait_and_click(driver, wait, selector, delay=1):
    """要素を待機してクリックする。
    
    Args:
        driver: WebDriver インスタンス
        wait: WebDriverWait インスタンス
        selector: CSS セレクター
        delay: クリック後の待機時間（秒）
    """
    try:
        element = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, selector)))
        element.click()
        if delay > 0:
            import time
            time.sleep(delay)
    except (TimeoutException, NoSuchElementException) as e:
        print(f"要素のクリックに失敗しました ({selector}): {e}")
        raise
