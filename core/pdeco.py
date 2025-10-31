import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.alert import Alert
from .base_login import create_chrome_driver, create_webdriver_wait
import time
import sqlite3
from database import cast_db_manager, heaven_schedule_db_manager
import random


def pdeco_login(cast_name: str = "", id: str = "", password: str = "", headless: bool = True) -> webdriver.Chrome:
    """PDECO 管理画面にログインし、ログイン済みの WebDriver を返す。

    Args:
        cast_name: キャスト名
        id: ログインID
        password: ログインパスワード
        headless: ヘッドレスモードで実行するかどうか
    """
    driver = create_chrome_driver(headless, incognito=True)
    wait = create_webdriver_wait(driver, 10)
    login_url = "https://spgirl.cityheaven.net"

    try:
        driver.get(login_url)
        # ページ読み込み待機
        time.sleep(1)
        # フォームの表示を待機
        wait.until(EC.presence_of_element_located((By.ID, "userid")))

        # ユーザー名フィールドを探して入力
        id_field = wait.until(EC.element_to_be_clickable((By.ID, "userid")))
        id_field.click()
        id_field.send_keys(id)
        time.sleep(1)

        # パスワードフィールドを探して入力
        password_field = wait.until(EC.element_to_be_clickable((By.ID, "passwd")))
        password_field.click()
        password_field.send_keys(password)
        time.sleep(1)

        # ログインボタンをクリック
        login_button = wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@id="loginBtn"]')))
        login_button.click()
        
        # ログイン後のページ遷移を待機
        wait.until(lambda d: d.current_url != login_url)

        # ログイン失敗の判定（エラーメッセージが表示されている場合）
        try:
            error_element = driver.find_element(By.CLASS_NAME, 'title-txt')
            if error_element:
                print(f"認証が必要です: {cast_name}")
                driver.quit()
                return f"{cast_name}: 認証が必要です"
        except:
            # エラー要素が見つからない場合は正常ログイン
            pass

        return driver
    except Exception:
        if driver:
            driver.quit()
        return cast_name

def pdeco_easy_login(cast_name: str, headless: bool = True) -> str:
    conn = None
    driver = None
    print(cast_name)
    try:
        # キャスト情報を取得
        cast_info = cast_db_manager.get_cast_info(cast_name)
        print(cast_info)
        if cast_info and cast_info[5]:  # pdeco_urlが存在する場合
            driver = create_chrome_driver(headless, incognito=True)
            wait = create_webdriver_wait(driver, 10)
            login_url = cast_info[5]  # pdeco_url
            print(f"アクセスURL: {login_url}")
            
            try:
                driver.get(login_url)
                driver.execute_script("arguments[0].click();", driver.find_element(By.CLASS_NAME, "loginBtn"))
                time.sleep(1)
                return driver
            except Exception as driver_error:
                print(f"ページアクセスエラー: {driver_error}")
                if driver:
                    try:
                        driver.quit()
                    except:
                        pass
                # 例外をraiseせず、エラーメッセージを返す
                return f"{cast_name}: ページアクセスエラー - {str(driver_error)}"
        else:
            return f"{cast_name}: キャスト情報またはURLが見つかりません"
    except Exception as e:
        print(f"キャスト情報取得エラー: {e}")
        print(f"エラータイプ: {type(e).__name__}")
        import traceback
        traceback.print_exc()
        # エラー時のみドライバーを終了
        if driver:
            driver.quit()
        return f"{cast_name}: キャスト情報取得エラー"

def get_pdeco_easy_login(cast_name: str = "", id: str = "", password: str = "", headless: bool = True) -> webdriver.Chrome:
    driver = pdeco_login(cast_name, id, password, headless)
    
    # driverが文字列の場合（エラーまたは認証が必要な場合）
    if isinstance(driver, str):
        if "認証が必要です" in driver:
            easy_login_url = "authentication_required"
        else:
            # その他のエラーの場合
            print(f"ログインエラー: {driver}")
            return "failed"
    else:
        # driverが正常に取得できた場合
        try:
            driver.execute_script("arguments[0].click();", driver.find_element(By.XPATH, '//*[@id="menuGrobal"]/a[1]'))
            time.sleep(2)
            driver.execute_script("arguments[0].click();", driver.find_element(By.CLASS_NAME, 'btnClose'))
            driver.execute_script("arguments[0].click();", driver.find_element(By.XPATH, '//*[@id="etceteraList"]/form/ul/li[1]/a'))
            easy_login_url = driver.current_url
            driver.quit()
        except Exception as e:
            print(f"URL取得エラー: {e}")
            if driver:
                driver.quit()
            return "failed"
    
    conn = None
    try:
        conn = sqlite3.connect('nimbus.db')
        cursor = conn.cursor()
        cursor.execute('UPDATE cast_info SET pdeco_url = ? WHERE cast_name = ?', (easy_login_url, cast_name))
        conn.commit()
        return "success"
    except Exception as e:
        if conn:
            conn.rollback()
        print(f"キャスト情報更新エラー: {e}")
        return "failed"
    finally:
        if conn:
            conn.close()

def heaven_kitene(cast_name: str, max_retries: int = 1):
    driver = None
    retry_count = 0
    
    while retry_count < max_retries:
        try:
            driver = pdeco_easy_login(cast_name, False)
            if isinstance(driver, str):
                # エラーメッセージが返された場合
                return driver
            # ページの読み込み完了を待つ
            wait = WebDriverWait(driver, 5)
            try:
                wait.until(lambda d: d.execute_script("return document.readyState") == "complete")
                # より汎用的な要素を待つ（キテネ関連の要素）
                wait.until(EC.any_of(
                    EC.presence_of_element_located((By.CLASS_NAME, 'kitene_text')),
                    EC.presence_of_element_located((By.CLASS_NAME, 'gift_text')),
                    EC.presence_of_element_located((By.CLASS_NAME, 'kitene_btn'))
                ))
            except Exception as e:
                # エラーでも続行（ページが部分的に読み込まれている可能性）
                pass
            
            time.sleep(0.5)
            try:
                # オーバーレイが存在するかチェック
                overlay_elements = driver.find_elements(By.CSS_SELECTOR,".jqmOverlay")
                if overlay_elements:
                    overlay_elements[0].click()
            except Exception as e:
                # オーバーレイがない場合はエラーでも続行
                pass

            # キテネ要素の存在を確認（常に「キテネを送る」をクリック）
            try:
                # パターン1: gift_textクラスが存在する場合（キテネギフト）
                gift_text_element = wait.until(EC.presence_of_element_located((By.CLASS_NAME,'gift_text')))
                driver.execute_script("arguments[0].scrollIntoView(true);", gift_text_element)
                time.sleep(0.2)
                driver.execute_script("arguments[0].click();", gift_text_element)
                time.sleep(0.5)
            except:
                # パターン2: kitene_textクラスが存在する場合（通常のキテネ）
                try:
                    kitene_text_element = wait.until(EC.presence_of_element_located((By.CLASS_NAME,'kitene_text')))
                    driver.execute_script("arguments[0].scrollIntoView(true);", kitene_text_element)
                    time.sleep(0.2)
                    driver.execute_script("arguments[0].click();", kitene_text_element)
                    time.sleep(0.2)
                except:
                    # どちらも見つからない場合は処理を終了
                    return "キテネ要素が見つかりません"
            
            # モーダルが表示されている場合はクリックして閉じる
            try:
                modal_close = driver.find_element(By.CLASS_NAME,'tb_close')
                if modal_close:
                    driver.execute_script("arguments[0].click();", modal_close)
            except Exception as e:
                driver.refresh()
            
            driver.execute_script("arguments[0].click();", driver.find_element(By.XPATH,'/html/body/main/div[2]/div/ul/li[5]/a'))
            time.sleep(0.5)
            
            s = 0
            f = 0

            kitene_count_elements = driver.find_elements(By.CLASS_NAME, "kitene_point")
            if not kitene_count_elements or kitene_count_elements[0].text == "本日はキテネを使い切りました":
                return "done"
            else:
                kitene_count = int(kitene_count_elements[0].text.split("：")[1].split("/")[0])

            wait = WebDriverWait(driver, 5)
            xpath_template = '//*[@id="reviewtabContents"]/ul/li[{}]/a/div[2]/div[1]/object/a/span'
            
            for i in range(1, kitene_count + 1):
                time.sleep(random.uniform(0.5, 1.8))
                
                try:
                    # 要素を待機して取得
                    element = wait.until(EC.element_to_be_clickable((By.XPATH, xpath_template.format(i))))
                    driver.execute_script("arguments[0].click();", element)
                    
                    time.sleep(random.uniform(0.5, 2.2))
                    Alert(driver).accept()
                    s += 1
                    
                except Exception as e:
                    time.sleep(random.uniform(0.5, 1.5))
                    driver.refresh()
                    f += 1
                    if f >= 10:
                        return "retry"
                    # 失敗時は同じiを再試行
                    i -= 1
                    continue
            return "done"
            
        except Exception as e:
            retry_count += 1
            if retry_count < max_retries:
                time.sleep(5)  # 5秒待ってからリトライ
                continue
            else:
                return f"エラー: {e}"
        finally:
            # driverがWebDriverオブジェクトの場合のみquitを呼び出す
            if driver and not isinstance(driver, str) and hasattr(driver, 'quit'):
                try:
                    driver.quit()
                except Exception as e:
                    print(f"ドライバー終了エラー: {e}")
    
    return "最大リトライ回数に達しました"
    

def okini_talk_auto(name, message):

    def navigate_talk(driver):
        time.sleep(2)
        driver.execute_script("window.scrollTo(0, 2500);")
        time.sleep(2)
        try:
            driver.find_element(By.CSS_SELECTOR,".jqmOverlay").click()
        except Exception:
            driver.refresh()
            pass
        driver.execute_script("arguments[0].click();", driver.find_element_by_xpath('//*[@id="fixedMenu"]/nav/ul/li[2]/a'))
        time.sleep(2)

        return driver

    def send_templete_message(driver, message):
        INPUT_EMOJI = """
                        arguments[0].value += arguments[1];
                        arguments[0].dispatchEvent(new Event('input', { bubbles: true }));
                        arguments[0].dispatchEvent(new Event('change', { bubbles: true }));
                    """
        try:
            talk_box = driver.find_element_by_name('talk_editor_box')
            talk_box.click()
            print("1")
            time.sleep(utilites.get_random_delay(0, (0, 0), (1, 2)).total_seconds())

            # 絵文字などを含むメッセージを入力（input イベントを発火させる）
            driver.execute_script(INPUT_EMOJI, talk_box, message)
            print("2")
            time.sleep(utilites.get_random_delay(0, (0, 0), (1, 3)).total_seconds())

            # 送信ボタンをクリック
            submit_button = driver.find_element_by_class_name('te_submit')
            driver.execute_script("arguments[0].click();", submit_button)
            print("3")

            time.sleep(0.2)
        except Exception as e:
            print(f"error: {e}")

    def is_within_three_months(reply_element) -> bool:
        """
        reply_element: SeleniumのWebElement（data-create_date属性を持つ）
        3ヶ月以内ならTrue、それより前ならFalseを返す
        """
        create_date_str = reply_element.get_attribute('data-create_date')
        if not create_date_str:
            print("日付属性が取得できませんでした。")
            return False

        try:
            # "2025/04/06 01:05:28" 形式に合わせて変換
            create_date = datetime.strptime(create_date_str, "%Y/%m/%d %H:%M:%S")
        except ValueError:
            print(f"日付の形式が不正です: {create_date_str}")
            return False

        today = datetime.now()
        three_months_ago = today - relativedelta(months=3)

        return create_date >= three_months_ago

    try:
        kg_target = get_target_gal_info(name)
        driver = pdeco_login(kg_target[0],kg_target[1],kg_target[2])
        navigate_talk(driver)

        counter_text = driver.find_element_by_class_name('counter').text
        match = re.search(r'全(\d+)人', counter_text)
        if match:
            total_people = int(match.group(1))
            print(total_people)
            num_loops = (total_people + 30 - 1) // 30  # 切り上げてループ回数を計算
            for j in range(num_loops):
                print(f"{j+1}回目のループ（表示人数: {j * 30 + 1}〜{min((j + 1) * 30, total_people)}人）")
                # ここに処理を入れる（例えば、ページネーションの処理など）  
                talk_box = driver.find_element_by_class_name('talk_box')
                count = len(talk_box.find_elements_by_class_name('list'))
                print(count)
                for i in range(1, count + 1):
                    talk_box = driver.find_element_by_class_name('talk_box')
                    target_user = talk_box.find_element_by_xpath(f'li[{i}]')
                    driver.execute_script("arguments[0].click();", target_user.find_element_by_class_name('link_user'))
                    driver.implicitly_wait(0) 
                    time.sleep(1)
                    user_name = driver.find_element_by_class_name('head_name').text
                    talk_main = driver.find_element_by_class_name('tb_main')

                    try:
                        replys = WebDriverWait(driver, 3).until(EC.presence_of_all_elements_located((By.CLASS_NAME, 'tb_left')))
                    except TimeoutException:
                        replys = []
                    try:
                        submiteds = WebDriverWait(driver, 3).until(EC.presence_of_all_elements_located((By.CLASS_NAME, 'tb_right')))
                    except TimeoutException:
                        submiteds = []
                    print(i, user_name, len(replys), len(submiteds))
                    
                    if replys or submiteds:
                        last_reply = replys[-1] if replys else None
                        last_submit = submiteds[-1] if submiteds else None

                        reply_recent = is_within_three_months(last_reply) if last_reply else False
                        submit_recent = is_within_three_months(last_submit) if last_submit else False

                        if not reply_recent and not submit_recent:
                            print("送信済みメッセージ、返信共に3ヶ月以上前のため送信")
                            send_templete_message(driver, message)
                    else:
                        print("返信が見つかりませんでした。問答無用で送信")
                        send_templete_message(driver, message)
                    driver.back()
                    driver.refresh()
                    driver.implicitly_wait(10)
                driver.execute_script("arguments[0].click();", driver.find_element_by_id('pagenext'))
        else:
            print("数値が見つかりませんでした。")         
    finally:
        driver.quit()