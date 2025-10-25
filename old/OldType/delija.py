from selenium import webdriver
import chromedriver_binary
import time
import csv
import os
import json
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
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
import random
import math


def delija_login(headless=True):
    options = Options()
    if headless:
        options.add_argument('--headless')  # ヘッドレスモード
    driver = webdriver.Chrome(options=options)
    driver.implicitly_wait(10)
    url = "https://deli-fuzoku.jp/entry/"
    utilites.dget(driver, url)

    time.sleep(1)
    for l in range(5):
        try:
            delija_id = driver.find_element(By.CSS_SELECTOR, "#form_username")
            delija_pass = driver.find_element(By.CSS_SELECTOR, "#form_password")
            delija_id.click()
            delija_id.send_keys("dieseldiesel01")
            delija_pass.click()
            delija_pass.send_keys("diesel01")
            driver.find_element(By.CSS_SELECTOR, "#button > img").click()
        except:
            driver.refresh()
            time.sleep(5)
        else:
            break
    return driver

def set_delija_schedule(schedule_cont):

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
            start_selector = f'/html/body/div/div/div[1]/div[2]/div[6]/div/table[{table_number}]/tbody/tr[{i}]/td[{j}]/div[1]/select'
            finish_selector = f'/html/body/div/div/div[1]/div[2]/div[6]/div/table[{table_number}]/tbody/tr[{i}]/td[{j}]/div[2]/select'
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

                for cast_cont in schedule_cont:
                    if cast_name == cast_cont[0]:
                        utilites.scroll_to_element(driver, cast_table)
                        #print(cast_name + "Delija")
                        time.sleep(2)
                        cast_existing_schedule = fetch_schedule_from_table(cast_table)
                        
                        if schedules_match(cast_cont, cast_existing_schedule):
                            print("スケジュールが一致しました。次の処理を行います。")
                        else:
                            #print(cast_name + "Delija Schedule not match")
                            update_schedule(driver, cast_table, cast_cont, table_number, i)
                time.sleep(2)
        except NoSuchElementException:
            print(f"テーブル {table_number} が見つかりません。")
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
            print("これ以上リンクがないため、ループを終了します")
            return False

    for l in range(2):
        try:
            driver = delija_login()
            navigate_to_schedule_management(driver)
            page_number = 1
            while True:
                #print(f"ページ {page_number} ------")
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
    print("delija-shift-done")
        
    driver.quit()

def delija_news(int):
    
    driver = delija_login()
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

def delija_pickup():

    try:
        driver = delija_login()
        pickup_manage = driver.find_element_by_css_selector(
                '#wrapper > div > div.leftColumn > nav > div:nth-child(2) > div > ul > li:nth-child(2) > a'
            )
        driver.execute_script("arguments[0].click();", pickup_manage)
    except:
        driver.refresh()
        time.sleep(5)
        pass
    
    try:
        ready_labels = driver.find_elements(By.XPATH, '//label[contains(text(), "即ヒメ")]')
        if len(ready_labels) == 0:
            print("デリじゃ出勤無")
            driver.quit()
        else:
            for label in ready_labels:
                driver.execute_script("arguments[0].click();", label)
                time.sleep(1)
                #print(f"{label.text}ボタンがクリックされました。")
            driver.quit()
    except Exception as e:
        print(f"ボタンをクリック中にエラーが発生しました: {e}")
