from selenium import webdriver
import chromedriver_binary
import time
import re
import utilites
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.alert import Alert
from selenium.webdriver.chrome import service
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.action_chains import ActionChains
import random
import math


def ekichika_login(headless=True):
    options = Options()
    if headless:
        options.add_argument('--headless')  # ヘッドレスモード

    driver = webdriver.Chrome(options=options)
    driver.implicitly_wait(10)
    url = "https://ranking-deli.jp/admin/login"
    time.sleep(1)
    utilites.dget(driver, url)

    time.sleep(1)
    for l in range(5):
        try:
            ekichika_id = driver.find_element(By.CSS_SELECTOR, "#form_email")
            ekichika_pass = driver.find_element(By.CSS_SELECTOR, "#form_password")
            ekichika_id.click()
            ekichika_id.send_keys("38872")
            ekichika_pass.click()
            ekichika_pass.send_keys("shakeshake")
            driver.find_element(By.CSS_SELECTOR, "#form_submit").click()
        except:
            driver.refresh()
            time.sleep(5)
        else:
            break
    return driver

def ekichika_pickup():
    driver = ekichika_login()

    for l in range(2):
        try:
            driver.find_element(By.XPATH,'/html/body/div[2]/div[2]/div[2]/div[2]/div/img').click()
            time.sleep(2)
            try:
                assert driver.switch_to.alert.text == "一括上位表示します。\nよろしいですか？"
                time.sleep(2)
                driver.switch_to.alert.accept()
                time.sleep(2)
                assert driver.switch_to.alert.text == "一括上位に成功しました。"
                
            except:
                print("駅チカ更新失敗")
                pass
        except:
            driver.refresh()
            time.sleep(5)
            pass
        else:
            break
    driver.quit()

def ekichika_gals_count():
    driver = ekichika_login(True)
    time.sleep(1)
    utilites.dget(driver, "https://ranking-deli.jp/admin/playinggirls/")
    time.sleep(1)
    gal_list = driver.find_element(By.XPATH,'//*[@id="girls-list-box"]')
    now_gal_count = len(gal_list.find_elements(By.CLASS_NAME,"state_play"))
    state_gal_count = len(gal_list.find_elements(By.CLASS_NAME,"state-now"))
    fast_gal_count = len(gal_list.find_elements(By.CLASS_NAME,"state-fast"))
    total_gal_count = now_gal_count + state_gal_count + fast_gal_count
    count = [math.ceil(total_gal_count / 4),now_gal_count,total_gal_count]
    print(count)
    driver.quit()
    return count
    
def ekichika_gals_picup(count):
    def ekichika_cast_count(driver):

        gal_list = driver.find_element_by_id('girls-list-box')
        now_gal_count = len(gal_list.find_elements_by_class_name("state_play"))
        state_gal_count = len(gal_list.find_elements_by_class_name("state-now"))
        fast_gal_count = len(gal_list.find_elements_by_class_name("state-fast"))
        total_gal_count = now_gal_count + state_gal_count + fast_gal_count
        count = [math.ceil(total_gal_count / 4), now_gal_count, total_gal_count]
        print(count)
        return count

    try:
        driver = ekichika_login(False)
        utilites.dget(driver, "https://ranking-deli.jp/admin/playinggirls/")
        count = ekichika_cast_count(driver)
        count_a = int(count[0])
        count_b = count[1] + 1
        count_c = count[2]
        for i in range(count_a):
            j = count_b + i
            if count_c < j:
                break
            else:
                driver.execute_script("arguments[0].click();", driver.find_element_by_xpath(f'/html/body/div[2]/div[2]/div[1]/div[2]/ul/li[{j}]/div[2]'))
                time.sleep(1)
                driver.execute_script("arguments[0].click();", driver.find_element_by_id('form_playing_now'))
                driver.execute_script("arguments[0].click();", driver.find_element_by_id('upload-btn'))
        
    except Exception as e:
        print(f"[駅チカ今すぐ] エラーが発生しました: {e}")
    finally:
        driver.quit()
        
def ekichika_sokuiku(source_num, target_num):
    driver = ekichika_login(False)

    for l in range(2):
        try:
            time.sleep(1)
            utilites.dget(driver, "https://ranking-deli.jp/admin/sokuiku/")
            time.sleep(1)  # ページの読み込み待ち
            
            # **1. SourceとTargetの要素を取得**
            source = driver.find_element(By.XPATH, f'//*[@id="girls-list-box"]/li[{source_num}]/div[2]/a')            
            target = driver.find_element(By.ID, f'sokuiku_set0{target_num}')

            # **2. Sourceをドラッグ開始**
            actions = ActionChains(driver)
            actions.click_and_hold(source).perform()
            time.sleep(0.5)  # クリックした状態を維持
            
            # **3. 一番上までスクロール**
            driver.execute_script("window.scrollTo(0, 0);")
            time.sleep(0.5)  # スクロールが完了するのを待つ

            # **4. Targetの位置を調整**
            target.location_once_scrolled_into_view
            driver.execute_script("window.scrollBy(0, -100);")  # 少し上にスクロールして安定させる
            time.sleep(0.5)

            # **5. Targetにドロップ**
            actions.move_to_element(target).release().perform()
            time.sleep(1)

            # **6. アラートを承認**
            Alert(driver).accept()
            time.sleep(1)

            driver.quit()
        except:
            driver.refresh()
            time.sleep(2)
            pass
        else:
            break
   
def ekichika_sokuiku_count():
    driver = ekichika_login(True)
    
    for l in range(2):
        try:
            time.sleep(1)
            utilites.dget(driver, "https://ranking-deli.jp/admin/sokuiku/")
            driver.execute_script("window.scrollTo(0,152)")

            gal_list = driver.find_element(By.XPATH,'//*[@id="girls-list-box"]')
            gal_count = len(gal_list.find_elements(By.TAG_NAME, "li"))
            now_gal_count = len(gal_list.find_elements(By.CLASS_NAME,"state-fast"))
            
            count = [now_gal_count,gal_count]
            driver.quit()
            return count
        except:
            gal_count = 0
            now_gal_count = 0
            count = [now_gal_count,gal_count]
            driver.quit()
            return count
            pass
        else:
            break

def ekichika_news():
    driver = ekichika_login(True)
    
    for l in range(2):
        try:
            time.sleep(1)
            utilites.dget(driver, "https://ranking-deli.jp/admin/articles/")
            driver.execute_script("window.scrollTo(0,152)")
            driver.find_element(By.CSS_SELECTOR,'body > div.main > div.col-md-12 > table > tbody > tr:nth-child(5) > td.editbtn_s.textcenter > a').click()
            driver.find_element(By.XPATH,'//*[@id="article_form"]/div[2]/div[1]/input').click()
        except:
            driver.refresh()
            pass
        else:
            break
    driver.quit()

def convert_shift_to_ekichika(shift_array):
    """
    シフト配列を24時以降の時間を25時以降の形式に変換する関数
    """
    
    # 時刻の変換関数を内部に定義
    def convert_time_format(time_str):
        if not time_str:  # 空の値に対応
            return time_str

        # 時刻を "HH:MM" から分割
        hour, minute = map(int, time_str.split(':'))

        # 00:00 から 07:59 の間は 24時間を足す
        if 0 <= hour < 8:
            hour += 24

        # フォーマットを整えて返す
        return f'{hour:02}:{minute:02}'

    # シフト配列を変換
    converted_array = []
    for cast in shift_array:
        # キャスト名をそのまま保持
        cast_name = cast[0]

        # シフト時間を変換
        converted_shifts = [
            [convert_time_format(start), convert_time_format(end)] if start and end else ['', ''] 
            for start, end in cast[1:]
        ]

        # キャスト名と変換後のシフトをまとめる
        converted_array.append([cast_name] + converted_shifts)
    
    return converted_array

def set_ekichika_schedule(cont):

    def get_target_cast_info(driver, cast_num):
        cast_table = driver.find_element_by_xpath(f'//*[@id="frmfix"]/ul[{cast_num}]')
        cast_name = cast_table.find_element_by_xpath(f'li[1]/span').text
        
        cast_info = [cast_table, cast_name]
        return cast_info

    def set_target_schedule(driver, cast_num, target_cast_table, cast_cont):
        for i in range(2, 9):
            start_time = cast_cont[i - 1][0]
            end_time = cast_cont[i - 1][1]
            start_time_box = f'/html/body/div[2]/div[2]/div[1]/div/div/form/ul[{cast_num}]/li[{i}]/div/select[1]'
            end_time_box   = f'/html/body/div[2]/div[2]/div[1]/div/div/form/ul[{cast_num}]/li[{i}]/div/select[2]'
            check_b =        f'/html/body/div[2]/div[2]/div[1]/div/div/form/ul[{cast_num}]/li[{i}]/div/div/input'

            if start_time == "":
                utilites.set_checkbox(driver, check_b, False)
            else:
                utilites.select_option(driver, start_time_box, start_time, True)
                utilites.select_option(driver, end_time_box, end_time, True)
    for l in range(2):
        try:
            driver = ekichika_login(False)
            utilites.dget(driver, "https://ranking-deli.jp/admin/girlswork/")
            time.sleep(120)
            schedule_table_e = driver.find_element_by_xpath('//*[@id="frmfix"]')
            gals_count = len(schedule_table_e.find_elements_by_tag_name("ul"))
        except:
            driver.refresh()
            time.sleep(5)
            pass
        else:
            break
    
    for l in range(2):
        try:
            for cast_cont in cont:
                cast_name = cast_cont[0]  # 配列内キャストの名前
                for i in range (1, gals_count + 1):
                    target_cast = get_target_cast_info(driver, i)
                    target_cast_table = target_cast[0]
                    target_cast_name =  target_cast[1]
                    if target_cast_name == cast_name:
                        print(cast_name + "+ekichika")
                        set_target_schedule(driver, i, target_cast_table, cast_cont)
                        break
        except:
            driver.refresh()
            time.sleep(5)
            pass
        else:
            break
            print("ekichika-shift-done")
    for l in range(2):
        try:
            # ページ最下部にスクロール
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(3)  # スクロール完了を待つ
            driver.execute_script("arguments[0].click();", driver.find_element(By.XPATH,'//*[@id="form_work_btn"]'))
        except:
            time.sleep(5)
            pass
        else:
            break
    print("Ekichika Shift Done")
    time.sleep(10)
    driver.quit()
                

#ekichika_gals_picup(ekichika_gals_count())
#ekichika_pickup()
