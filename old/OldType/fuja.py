import os
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))  # ここを修正
import utilites 
import time
import datetime
import random
import math
import threading
import schedule
import flet as ft
import re
import pykakasi
from pykakasi import kakasi
import requests
import traceback
import csv
import os
import chromedriver_binary
from selenium import webdriver
from selenium.webdriver.support.ui import Select
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.by import By
from selenium.webdriver.common.alert import Alert
from selenium.webdriver.chrome import service
from selenium.webdriver.common.action_chains import ActionChains
from selenium.common.exceptions import TimeoutException
from selenium.common.exceptions import NoSuchElementException, NoAlertPresentException


def fuja_login(headless=True):
    options = Options()
    options.add_argument("--log-level=3")  # エラーのみ表示
    if headless:
        options.add_argument('--headless')  # ヘッドレスモード
    driver = webdriver.Chrome(options=options)
    driver.implicitly_wait(10)
    url = "https://fuzoku.jp/entry/"
    utilites.dget(driver, url)

    time.sleep(1)
    for l in range(5):
        try:
            delija_id = driver.find_element(By.CSS_SELECTOR, "#form_username")
            delija_pass = driver.find_element(By.CSS_SELECTOR, "#form_password")
            delija_id.click()
            delija_id.send_keys("nukeru21")
            delija_pass.click()
            delija_pass.send_keys("mbnukeru")
            time.sleep(1)
            driver.find_element(By.CSS_SELECTOR, "#button > img").click()
        except:
            driver.refresh()
            time.sleep(5)
        else:
            break
    return driver

def set_fuja_schedule(schedule_cont):

    def format_shift_to_fuja(casts):
        # キャスト名を修正する関数
        def clean_cast_name(name):
            return re.sub(r'★.*$', '', name)

        # シフトをフォーマットする関数
        def convert_time(shift):
            try:
                start, end = shift
                start = int(start.replace(':', '')) if start else "----"
                end_hour, end_minute = map(int, end.split(':')) if end else (0, 0)
                if 0 <= end_hour <= 7:  # 24時間表記を超えている場合
                    end_hour += 24
                end = f"{end_hour:02d}{end_minute:02d}" if end else "----"
                return [start, end]
            except Exception as e:
                print(f"エラーが発生しました: {e}")
                return ["----", "----"]

        formatted_casts = []
        for cast in casts:
            cast_name = clean_cast_name(cast[0])  # キャスト名を修正
            shifts = cast[1:]

            # シフトをフォーマット
            formatted_shifts = [convert_time(shift) if shift != ['', ''] else ['----', '----'] for shift in shifts]
            
            # 修正されたキャスト名とフォーマットされたシフトを追加
            formatted_casts.append([cast_name] + formatted_shifts)

        return formatted_casts

    def navigate_to_schedule_management(driver):
        """スケジュール管理画面へ遷移する"""
        schedule_manage = driver.find_element_by_css_selector(
            '#wrapper > div > div.leftColumn > nav > div:nth-child(5) > div > ul > li > a'
        )
        driver.execute_script("arguments[0].click();", schedule_manage)

    def fetch_schedule_from_table(cast_table):
        """テーブルからスケジュールを取得する"""
        cast_existing_schedule = []
        for k in range(2, 9):
            start_elm = driver.find_element_by_xpath(f'{cast_table}/td[{k}]/div[1]/input')
            finish_elm = driver.find_element_by_xpath(f'{cast_table}/td[{k}]/div[2]/input')
            k_cont = [start_elm.get_attribute("class"), finish_elm.get_attribute("class")]
            cast_existing_schedule.append(k_cont)
        return cast_existing_schedule

    def update_schedule(driver, cast_table, cast_cont, table_number, i):
        """スケジュールを更新する処理"""
        for j in range(2, 9):
            start_selector = f'/html/body/div/div/div[1]/div[1]/div[6]/div/table[{table_number}]/tbody/tr[{i}]/td[{j}]/div[1]/select'
            finish_selector = f'/html/body/div/div/div[1]/div[1]/div[6]/div/table[{table_number}]/tbody/tr[{i}]/td[{j}]/div[2]/select'
            start_time = cast_cont[j - 1][0]
            finish_time = cast_cont[j - 1][1]
            
            utilites.hover_and_click_element(driver, start_selector)
            utilites.select_option_with_js(driver, start_selector, start_time)
            utilites.hover_and_click_element(driver, finish_selector)
            utilites.select_option_with_js(driver, finish_selector, finish_time)
        time.sleep(1)

    def schedules_match(cast_cont, cast_existing_schedule):
        """キャストのスケジュールが一致するか確認"""
        return all(cast_cont[i + 1] == cast_existing_schedule[i] for i in range(len(cast_cont) - 1))

    def get_cast_info(driver, table_number):
        """特定のテーブルからキャスト情報を取得する"""
        cast_info_list = []
        try:
            table = driver.find_element_by_xpath(f'//*[@id="entry_content"]/div[6]/div/table[{table_number}]')
            rows = table.find_elements_by_tag_name('tr')
            for i in range(1, len(rows) + 1):
                cast_table = f'//*[@id="entry_content"]/div[6]/div/table[{table_number}]/tbody/tr[{i}]'
                cast_name = driver.find_element_by_xpath(f'{cast_table}/td[1]/span').get_attribute("innerHTML")

                for cast_cont in shift_array:
                    if cast_name == cast_cont[0]:
                        c_table_elm = f'//*[@id="entry_content"]/div[6]/div/table[{table_number}]/tbody/tr[{i}]'
                        utilites.scroll_to_element(driver, c_table_elm)
                        #print(cast_name + "Fuja")
                        time.sleep(2)
                        cast_existing_schedule = fetch_schedule_from_table(cast_table)
                        
                        if schedules_match(cast_cont, cast_existing_schedule):
                            print("スケジュールが一致しました。次の処理を行います。")
                        else:
                            #print(cast_name + "Delija Schedule not match")
                            update_schedule(driver, cast_table, cast_cont, table_number, i)
                time.sleep(2)
        except NoSuchElementException:
            driver.refresh()
        return cast_info_list

    def go_to_next_page(driver):
        """次のページに進む"""
        driver.execute_script("window.scrollTo(0, 0);")
        try:
            next_link = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.LINK_TEXT, '次の60件'))
            )
            next_link.click()
            return True
        except (NoSuchElementException, TimeoutException):
            return False

    for l in range(2):
        try:
            driver = fuja_login()
            navigate_to_schedule_management(driver)
            shift_array = format_shift_to_fuja(schedule_cont)
            page_number = 1
            while True:
                for table_number in range(2, 7):
                    get_cast_info(driver, table_number)
                if not go_to_next_page(driver):
                    break
                page_number += 1
        except:
            driver.refresh()
            time.sleep(5)
            pass
        else:
            break
    print("Fuja Shift Done")
    driver.quit()
    return "fuja_schedule_synced"

def fuja_pickup():

    try:
        driver = fuja_login()
        pickup_manage = driver.find_element_by_css_selector(
                '#wrapper > div > div.leftColumn > nav > div:nth-child(2) > div > ul > li:nth-child(2) > a'
            )
        driver.execute_script("arguments[0].click();", pickup_manage)
    except:
        driver.refresh()
        time.sleep(5)
        pass
    
    try:
        ready_labels = driver.find_elements(By.XPATH, '//label[contains(text(), "今すぐ")]')
        if len(ready_labels) == 0:
            print("風じゃ出勤無")
            driver.quit()
        else:
            for label in ready_labels:
                driver.execute_script("arguments[0].click();", label)
                time.sleep(1)
                #print(f"{label.text}ボタンがクリックされました。")
            driver.quit()
    except Exception as e:
        print(f"ボタンをクリック中にエラーが発生しました: {e}")

def register_cast_fuj(cast_info, action,  set_img=False, mail=False):

    def set_profile_fuj(driver, navigate_elm, set_img=False):

        INPUT_EMOJI = """
            arguments[0].value += arguments[1];
            arguments[0].dispatchEvent(new Event('change'));
        """
        x = [cast_info["guest_chatch"], cast_info["owner_comment"]]
        message = '\n\n\n【店長コメント】'.join(x)
        
        driver.execute_script("arguments[0].click();", navigate_elm)
        time.sleep(2)

        fields = [
            ('girl_name', 'girls_name'),
            ('girl_age', 'girls_age'),
            ('girl_height', 'girls_height'),
            ('girl_sizeb', 'girls_bust'),
            ('girl_sizew', 'girls_waist'),
            ('girl_sizeh', 'girls_hip')
        ]
        Select(driver.find_element_by_name('girl_cup')).select_by_visible_text(cast_info["sel_GirlCup"])

        for field, key in fields:
            driver.find_element_by_name(field).clear()
            driver.execute_script(INPUT_EMOJI, driver.find_element_by_name(field), cast_info[key])
        for i in range(1, 11):
            driver.find_element_by_name(f'prof_a{i}').clear()
            driver.execute_script(INPUT_EMOJI, driver.find_element_by_name(f'prof_a{i}'), cast_info[f'girls_Answer{i}'])
        driver.find_element_by_id('form_girl_pr').clear()
        driver.execute_script(INPUT_EMOJI, driver.find_element_by_id('form_girl_pr'), message)

        driver.find_element_by_name('entry-submit').click()
        time.sleep(2)

    def get_cast_element_fuj(driver, cast_name=None):
        """ キャスト一覧の WebElement リストを取得
            - `cast_name` を指定すると、そのキャストの要素を返す
            - `cast_name` を指定しない場合は、全キャストのリストを返す
        """
        driver.execute_script("arguments[0].click();", driver.find_element_by_css_selector('#wrapper > div > div.leftColumn > nav > div:nth-child(8) > div > ul > li:nth-child(3) > a'))
        gal_list = driver.find_element_by_id('ul_sortable1')
        elements = gal_list.find_elements_by_class_name('ui-state-default')

        if cast_name is None: return elements  # キャスト一覧（WebElementのリスト）を返す
        
        for elm in elements:
            data_name = elm.find_element_by_class_name('girl_name').text
            if data_name == cast_name: return elm
        return None

    def check_duplicates_fuj(driver, cast_name):
        """キャストがすでに存在するか確認（存在する場合は False, 存在しない場合は True）"""
        return get_cast_element_fuj(driver, cast_name) is None
    
    def get_edit_cast_element_fuj(driver, cast_name):
        """ 編集対象キャストの編集URLを取得 """
        cast_element = get_cast_element_fuj(driver, cast_name)
        if cast_element:
            edit_element = cast_element.find_element_by_class_name('edit')
            time.sleep(1)
            return edit_element

    def get_create_cast_element_fuj(driver):
        """新規作成のエレメントを戻す"""
        return driver.find_element_by_css_selector('#wrapper > div > div.leftColumn > nav > div:nth-child(8) > div > ul > li:nth-child(2) > a')

    def get_mail_fuj(driver, cast_name):#完成
        
        time.sleep(1)
        mail_manage = driver.find_element_by_css_selector('#wrapper > div > div.leftColumn > nav > div:nth-child(7) > div > ul > li:nth-child(1) > a')
        driver.execute_script("arguments[0].click();", mail_manage)
        d_gal_list = driver.find_element_by_xpath('//*[@id="girls"]/ul')
        count_d = len(d_gal_list.find_elements_by_tag_name('li')) 

        for i in range(1,count_d + 1):
            d_gal_name = driver.find_element_by_xpath(f'//*[@id="girls"]/ul/li[{i}]/a/div[1]')
            d_gal_name_text = d_gal_name.get_attribute("innerHTML")
            if cast_name == d_gal_name_text:
                driver.find_element_by_xpath(f'//*[@id="girls"]/ul/li[{i}]/a').click()
                element = driver.find_element_by_xpath('//*[@id="form_diary_email"]')
                return element.get_attribute('value')
    
    try:    
        driver = fuja_login()
        print(cast_name, ":", dup_result)

        c_elm = get_create_cast_element_fuj(driver)
        set_profile_fuj(driver, c_elm, set_img)
        if mail: return get_mail_fuj(driver, cast_name)
        print("キャスト追加")

    finally:
        driver.quit()

def fuja_news(int):
    
    driver = fuja_login()
    news_manage = driver.find_element_by_css_selector(
            '#wrapper > div > div.leftColumn > nav > div:nth-child(2) > div > ul > li:nth-child(1) > a'
        )
    driver.execute_script("arguments[0].click();", news_manage)

    driver.find_element_by_link_text("新規投稿").click()

    with open('town_news/town_news_text.csv', "r", encoding = "utf-8") as f:
        reader = csv.reader(f)
        l = [row for row in reader]
    time.sleep(5)
    for k in range(3):
        try:
            driver.find_element_by_name("title").send_keys(l[int][1])
            utilites.input_iframe_textarea(driver, '//*[@id="cke_1_contents"]/iframe', '/html/body', l[int][2])
            utilites.send_img_form(driver, os.path.join('town_news', f"{l[int][3]}.jpg"), 'img')
            time.sleep(5)
            driver.find_element_by_css_selector("#form_register_btn").click()
            time.sleep(5)
            driver.quit()
        except:
            driver.refresh()
            time.sleep(5)
            pass
        else:
            break