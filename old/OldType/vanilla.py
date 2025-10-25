from selenium import webdriver
import chromedriver_binary
import time
import re
import os
import csv
import html
import utilites
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.common.alert import Alert
from selenium.webdriver.chrome import service
from selenium.common.exceptions import NoSuchElementException
import random
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import Select
from pykakasi import kakasi
import pykakasi
import requests
import blog_db

INPUT_EMOJI = """
                arguments[0].value += arguments[1];
                arguments[0].dispatchEvent(new Event('change'));
                    """

def vanilla_login(headless=True):
    options = Options()
    if headless:
        options.add_argument('--headless')  # ヘッドレスモード

    driver = webdriver.Chrome(options=options)   #(※２）
    driver.implicitly_wait(10)
    url = "https://qzin.jp/entry/"
    utilites.dget(driver, url)
    n = random.randint(1, 5)
    time.sleep(n)
    # browser.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    for l in range(5):
        try:
            vanilla_id = driver.find_element_by_css_selector("#form_username")
            vanilla_pass = driver.find_element_by_css_selector("#form_password")    
            vanilla_id.click()
            vanilla_id.send_keys("mbsentai")
            vanilla_pass.click()
            vanilla_pass.send_keys("sentai01")    
            driver.find_element_by_css_selector("#button").click()
        except:
            driver.refresh()
            time.sleep(5)
            pass
        else:
            break
    return driver
# テンプレートフォルダのパス

def cocoa_login(headless=True):
    options = Options()
    if headless:
        options.add_argument('--headless')  # ヘッドレスモード

    driver = webdriver.Chrome(options=options)   #(※２）
    driver.implicitly_wait(10)
    url = "https://cocoa-job.jp/entry/login/"
    utilites.dget(driver, url)
    n = random.randint(1, 5)
    time.sleep(n)
    # browser.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    for l in range(5):
        try:
            vanilla_id = driver.find_element_by_css_selector("#email")
            vanilla_pass = driver.find_element_by_css_selector("#main > div > div > form > div:nth-child(2) > input")    
            vanilla_id.click()
            vanilla_id.send_keys("34027")
            vanilla_pass.click()
            vanilla_pass.send_keys("dieseldeli")    
            driver.find_element_by_css_selector("#main > div > div > form > div.btn-area > input").click()
            
        except:
            driver.refresh()
            time.sleep(5)
            pass
        else:
            break
    return driver

def post_template(article_id):
    """
    指定されたIDの記事を投稿する
    """
    try:
        # データベースから記事を取得
        article = blog_db.get_blog_by_id(article_id)
        if article is None:
            raise Exception(f"記事ID {article_id} が見つかりません")

        # タプルを辞書に変換
        article_dict = {
            'title': article[1],
            'content': article[2],
            'images': article[3]
        }

        title = article_dict['title']
        body = article_dict['content']
        images = article_dict['images'].split(',') if article_dict['images'] else []

        # バニラに投稿
        log = post_template_vanilla(title, body, images)
        
        # ココアに投稿
        try:
            post_template_cocoa(title, body, images)
        except Exception as e:
            print(f"ココアへの投稿に失敗しました: {e}")
        
        return log
    except Exception as e:
        print(f"投稿に失敗しました: {e}")
        return None

def post_template_vanilla(title, body, images):
    """
    バニラに記事を投稿する
    """
    def navigate_to_blog_submit_manage():
        driver = vanilla_login()
        time.sleep(1)
        driver.find_element_by_css_selector("body > center > table:nth-child(2) > tbody > tr:nth-child(1) > td:nth-child(2) > table > tbody > tr > td > table > tbody > tr:nth-child(6) > td > table:nth-child(16) > tbody > tr:nth-child(3) > td:nth-child(3) > form > input").click()
        return driver

    try:
        driver = navigate_to_blog_submit_manage()

        try:
            radio_buttons = driver.find_elements(By.NAME, "status")
            for radio_button in radio_buttons:
                if radio_button.get_attribute("value") == "1":
                    radio_button.click()
                    break
        except Exception as e:
            print(f"ラジオボタンの選択に失敗しました: {e}")

        # 投稿内容をフォームに入力
        elm_title = driver.find_element_by_name("title")
        driver.execute_script(utilites.INPUT_EMOJI, elm_title, title)
        driver.find_element_by_id('cke_12').click()
        time.sleep(1)
        elm_body = driver.find_element_by_xpath('//*[@id="cke_1_contents"]/textarea')
        driver.execute_script(utilites.INPUT_EMOJI, elm_body, body)

        # 画像をアップロード
        for image in images:
            utilites.send_img_form(driver, image, 'image')
            time.sleep(2)

        driver.find_element_by_css_selector('body > center > table:nth-child(2) > tbody > tr:nth-child(1) > td:nth-child(2) > table > tbody > tr > td > form > div.submit_btn > input[type=submit]').click()
        time.sleep(1)
        driver.find_element_by_css_selector('body > center > table:nth-child(2) > tbody > tr:nth-child(1) > td:nth-child(2) > table > tbody > tr > td > form > div > input[type=button]:nth-child(3)').click()
        time.sleep(1)
        driver.quit()
    except Exception as e:
        print(f"バニラへの投稿に失敗しました: {e}")
        raise
    return title

def post_template_cocoa(title, body, images):
    """
    ココアに記事を投稿する
    """
    driver = cocoa_login()
    time.sleep(1)
    utilites.dget(driver, "https://cocoa-job.jp/entry/blog/add/?lid=gNNxYUQfq2BucgzM6rGYUmNRdkV0OG5VV0tMclJ1d1lIMlU2MEwwOERqMTRuU1drZFZDTE9RZ0RNQTg")
    
    try:
        elm_title = driver.find_element_by_name("title")
        driver.execute_script(utilites.INPUT_EMOJI, elm_title, title)
        driver.find_element_by_id('cke_12').click()
        time.sleep(1)
        elm_body = driver.find_element_by_xpath('//*[@id=\"cke_1_contents\"]/textarea')
        driver.execute_script(utilites.INPUT_EMOJI, elm_body, body)
        
        # 画像をアップロード
        for image in images:
            utilites.send_img_form(driver, image, 'blog_file')
            time.sleep(2)

        driver.find_element_by_css_selector('#main > div.col-md-12 > form > div > input.blog_submit').click()
        time.sleep(2)
        driver.quit()
    except Exception as e:
        print(f"ココアへの投稿に失敗しました: {e}")
        raise

