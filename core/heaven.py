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

"heaven_kg_auto(),heaven_opening(),profile_copy(name),pdeco_create(name)未実装"


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

    driver = create_chrome_driver(headless, incognito=True)
    wait = create_webdriver_wait(driver, 10)
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


def heaven_store_update(username: str = "", password: str = "", headless: bool = True):
    """CityHeaven のお店ページ更新日時を更新する。
    
    Args:
        username: ログインユーザー名（空の場合は環境変数から取得）
        password: ログインパスワード（空の場合は環境変数から取得）
        headless: ヘッドレスモードで実行するかどうか
    """
    driver = None
    try:
        driver = heaven_login(username, password, headless)
        wait = WebDriverWait(driver, 10)
        
        # ランダムな待機時間（1-5秒）
        delay = random.randint(1, 3)
        
        # お店ページ更新ボタンをクリック
        click_element_by_script(driver, wait, "#cntButton > div:nth-child(1)", delay)
        handle_alert(driver, "お店ページの更新日時を更新しますか？")
        
        # ガールズヘブン更新ボタンをクリック
        click_element_by_script(driver, wait, "#cntButtonGirls > div:nth-child(1)", delay)
        handle_alert(driver, "ガールズヘブンのお店ページ更新日時を更新しますか？")
        
        # 最終待機
        time.sleep(delay)
        
    except Exception as e:
        print(f"更新処理中にエラーが発生しました: {e}")
        raise
    finally:
        if driver:
            driver.quit()


def get_pdeco_info(username: str = "2510021932", password: str = "i7Qt5Jnj", 
                  headless: bool = False, max_casts: int = None):
    """キャスト情報を取得する関数
    
    Args:
        username: ログインユーザー名
        password: ログインパスワード
        headless: ヘッドレスモードで実行するかどうか
        max_casts: 処理する最大キャスト数（Noneの場合は全キャスト）
    
    Returns:
        list: [[キャスト名, 状態, ID, パスワード], ...]
    """
    driver = None
    try:
        driver = heaven_login(username, password, headless=True)
        time.sleep(2)
        
        # キャスト一覧ページにアクセス
        driver.get('https://newmanager.cityheaven.net/C8GirlMyPageRegist.php?')
        cast_list = driver.find_element(By.XPATH, '//*[@id="form_container"]/div/ul')
        total_count = len(cast_list.find_elements(By.TAG_NAME, 'li'))
        print(f"総キャスト数: {total_count}")
        
        # 未登録キャスト数をカウントし、未登録キャストの情報も取得
        unregistered_count = 0
        casts_info = []
        
        # 未登録キャストの情報を取得
        for i in range(1, total_count + 1):
            try:
                cast_state = driver.find_element(
                    By.XPATH, f'//*[@id="form_container"]/div/ul/li[{i}]/div[1]/label'
                ).text
                if cast_state == "未登録":
                    # 未登録キャストの名前を取得
                    cast_name_element = driver.find_element(
                        By.XPATH, f'//*[@id="form_container"]/div/ul/li[{i}]/div[2]/a'
                    )
                    cast_name = cast_name_element.get_attribute("innerHTML")
                    casts_info.append([cast_name, "未登録", "", ""])
                    unregistered_count += 1
                else:
                    break  # 未登録でないキャストが見つかったら終了
            except NoSuchElementException:
                break
        
        print(f"未登録キャスト数: {unregistered_count}")
        print(f"処理対象キャスト数: {total_count - unregistered_count}")
        
        # 登録済みキャストの情報を取得
        end_index = min(unregistered_count + (max_casts or total_count), total_count)
        
        for i in range(unregistered_count + 1, end_index + 1):
            try:
                # キャスト名を取得
                cast_name_element = driver.find_element(
                    By.XPATH, f'//*[@id="form_container"]/div/ul/li[{i}]/div[2]/a'
                )
                cast_name = cast_name_element.get_attribute("innerHTML")
                
                # キャスト詳細ページに移動
                driver.execute_script("arguments[0].click();", cast_name_element)
                time.sleep(1)
                
                try:
                    # IDとパスワードを取得
                    info_element = driver.find_element(
                        By.XPATH, '//*[@id="form_container"]/table/tbody/tr/td[2]/table/tbody/tr[2]/td/div'
                    )
                    info_text = info_element.get_attribute("innerHTML")
                    
                    # 情報をパース
                    parts = info_text.split('　')
                    if len(parts) >= 2:
                        id_part = parts[0].split('：')
                        password_part = parts[1].split('：')
                        
                        cast_id = id_part[1] if len(id_part) > 1 else ""
                        cast_password = password_part[1].strip() if len(password_part) > 1 else ""
                        
                        cast_info = [cast_name, "登録済", cast_id, cast_password]
                    else:
                        cast_info = [cast_name, "登録済", "", ""]
                        
                except NoSuchElementException:
                    cast_info = [cast_name, "登録済", "", ""]
                
                casts_info.append(cast_info)
                print(cast_info)
                
            except Exception as e:
                print(f"キャスト {i} の情報取得でエラー: {e}")
                continue
        
        # キャスト情報のみを返す
        return casts_info
        
    except Exception as e:
        print(f"エラーが発生しました: {e}")
        return "failed"
    finally:
        if driver:
            driver.quit()


def get_heaven_schedule(username: str = "2510021932", password: str = "i7Qt5Jnj", headless: bool = True):
    
    driver = heaven_login(username, password, headless)

    driver.get('https://newmanager.cityheaven.net/C9ShukkinShiftList.php')
    Select(driver.find_element(By.XPATH, '//*[@id="list_cnt"]')).select_by_visible_text("全件表示")
    schedule_table = driver.find_element(By.XPATH, '//*[@id="shukkinShiftTable"]/tbody')
    casts_row = schedule_table.find_elements(By.CLASS_NAME, 'time')
    schedule_data_list = []
    for cast_row in casts_row:  # スケジュールデータを取得
        schedule_data = []
        cast_name = cast_row.find_element(By.XPATH, './/td[@class="girl-thum"]/a').text.split("\n")[0]
        # 各日のスケジュールを取得（shukkinクラスのtd要素をループ）- 7日分のみ
        shukkin_tds = cast_row.find_elements(By.CLASS_NAME, 'shukkin')
        for day_td in shukkin_tds[:7]:  # 最初の7日分のみ
            try:
                # 開始時間と終了時間を取得
                start_value = day_td.find_element(By.XPATH, './/input[@id="start_time"]').get_attribute('value')
                end_value = day_td.find_element(By.XPATH, './/input[@id="end_time"]').get_attribute('value')
                
                # 時間が設定されている場合のみ追加
                if start_value and end_value:
                    schedule_data.append([utilities.format_time(start_value), utilities.format_time(end_value)])
                else:
                    schedule_data.append(["", ""])  # 空のスケジュール
                
            except:
                schedule_data.append(["", ""])  # エラーの場合は空のスケジュール
        schedule_data_list.append([cast_name, schedule_data])
                
    driver.quit()
    
    return {
        'success': True,
        'schedule_data_list': schedule_data_list,
        'total_casts': len(schedule_data_list)
    }
    


    
if __name__ == "__main__":
    # 例: 環境変数を設定して実行、または引数で渡す
    heaven_login()