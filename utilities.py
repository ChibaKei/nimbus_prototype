import time
import datetime
import random
import threading
import schedule
import re
import requests
import json
import os

from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.support import expected_conditions as EC

INPUT_EMOJI = """
                arguments[0].value += arguments[1];
                arguments[0].dispatchEvent(new Event('change'));
                """

def dget(driver, target_url, max_retries=5, wait_time=3, checkf=False):
    """
    指定されたURLに遷移し、遷移したかどうかを確認します。
    遷移していない場合はリトライします。
    
    :param driver: SeleniumのWebDriver
    :param target_url: 目的のURL
    :param max_retries: 最大リトライ回数（デフォルトは5回）
    :param wait_time: ページ遷移後の待機時間（デフォルトは3秒）
    :return: 遷移が成功したDriver
    """
    for attempt in range(max_retries):
        try:
            time.sleep(2)
            #print("try for:", target_url)
            driver.get(target_url)  # 目的のURLに遷移

            # ページが読み込まれるまで待機
            WebDriverWait(driver, wait_time).until(
                EC.presence_of_element_located((By.TAG_NAME, "body"))  # bodyタグがロードされるまで待機
            )

            # 現在のURLが目的のURLかどうかを確認
            current_url = driver.current_url
            if checkf:
                return driver
            if current_url == target_url:
                #print(f"Successfully navigated to {current_url}")
                return driver  # 目的のURLに遷移できたらそのまま返す

            #print(f"Attempt {attempt + 1}/{max_retries}: Failed to navigate to {target_url}. Retrying...")
        except Exception as e:
            print(f"Error occurred during navigation: {e}")
            print(f"Attempt {attempt + 1}/{max_retries}: Retrying...")

    print("Max retries reached. Navigation failed.")
    return None  # 最大リトライ回数に達しても遷移できなかった場合
    
def get_random_delay(base_minutes=5, rand_min_range=(0, 0), rand_sec_range=(1, 30)):
    #乱数を作る
    n_sec = random.randint(*rand_sec_range)
    n_min = random.randint(*rand_min_range)
    basedelay = datetime.timedelta(minutes=base_minutes)
    randdelay = datetime.timedelta(minutes=n_min) + datetime.timedelta(seconds=n_sec)
    return basedelay + randdelay


def ensure_four_characters(input_str):#引数が4文字以下の場合、「1」を文字列に付け足して返す関数
    if input_str is None:
        input_str = ''
    while len(input_str) < 4:
        input_str += '1'
    
    return input_str

def truncate_text(text):#引数が5文字以上の場合、5文字以降を省略して三点リーダーに置き換える
    if len(text) >= 5:
        return text[:5] + "…"
    else:
        return text

def clean_and_extract_text(html_content):# 改行とスペース,HTMLタグを削除
    text = re.sub(r'<[^>]+>', '', html_content)
    text = re.sub(r'\s+', '', text)
    return text

def array_to_text(array):
    # 各行を文字列に変換し、改行を加えて連結
    return "\n".join([" | ".join(map(str, row)) for row in array])

def format_time(time_str):
    """時間を 'HHMM' 形式から 'HH:MM' に変換する関数"""
    if not time_str:  # 空文字列の場合はそのまま返す
        return ''
    return f"{time_str[:2].zfill(2)}:{time_str[2:].zfill(2)}"

def set_checkbox_for_time(time_str, driver, xpath):
    """時間に基づいてチェックボックスを操作する関数"""
    try:
        # チェックボックス要素を取得
        checkbox = driver.find_element_by_xpath(xpath)
        
        # チェックボックスの状態を確認
        if time_str:  # 時間が空でない場合
            if not checkbox.is_selected():
                driver.execute_script("arguments[0].click();", checkbox)
                return True
            return True
        else:  # 時間が空の場合
            if checkbox.is_selected():
                driver.execute_script("arguments[0].click();", checkbox)  # チェックを外す
                return False
            return False
    except Exception as e:
        print(f"エラー: {e}")

def set_checkbox(driver, checkbox_xpath, value):
    """
    指定したXPathのチェックボックスを引数に基づいて操作する関数
    :param driver: Selenium WebDriverインスタンス
    :param checkbox_xpath: チェックボックスのXPath
    :param value: Trueならチェックを入れる。Falseならチェックを外す。
    """
    try:
        # チェックボックスの要素を取得
        checkbox = driver.find_element_by_xpath(checkbox_xpath)
        
        # チェックボックスの現在の状態を取得
        is_checked = checkbox.is_selected()

        # Trueの場合、チェックを入れる (未チェックならクリック)
        if value and not is_checked:
            checkbox.click()
            #print("チェックを入れました。")
        # Falseの場合、チェックを外す (チェックされていればクリック)
        elif not value and is_checked:
            checkbox.click()
            #print("チェックを外しました。")
    
    except Exception as e:
        pass
        #print(f"チェックボックスの操作中にエラーが発生しました: {e}")

def send_discord_message(content):
    # Discord側で作成したボットのウェブフックURL
    discord_webhook_url = "https://discord.com/api/webhooks/1127236627048181851/74acLzQ6BQHsRc8RmS5fpXPUPPmKpDH0adtDpfFSyVFhVFj28QQPbi1fH2ThP-O_cI_R"

    # 投稿するチャット内容と設定
    message = {
        "content": content,  # チャット本文
        "tts": False  # ロボットによる読み上げ機能を無効化
    }

    headers = {
        "Content-Type": "application/json"
    }

    # POSTリクエストを送信
    response = requests.post(discord_webhook_url, data=json.dumps(message), headers=headers)

    # 結果を確認
    if response.status_code == 204:
        print("メッセージが送信されました。")
    else:
        print(f"エラーが発生しました: {response.status_code}")

def format_shift_to_delija(casts):
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

def scroll_to_element(driver, xpath):
    try:
        # JavaScriptを使って要素を画面の中心にスクロール
        driver.execute_script(f"""
            var element = document.evaluate('{xpath}', document, null, XPathResult.FIRST_ORDERED_NODE_TYPE, null).singleNodeValue;
            if (element) {{
                element.scrollIntoView({{ behavior: 'smooth', block: 'center', inline: 'center' }});
                return true;
            }}
            return false;
        """)
        time.sleep(0.2)
    except Exception as e:
        print(f"要素のスクロール中にエラーが発生しました: {e}")

def hover_and_click_element(driver, xpath):
    try:
        scroll_to_element(driver, xpath)  # 要素をスクロールして画面に表示
        element = driver.find_element(By.XPATH, xpath)
        actions = ActionChains(driver)
        actions.move_to_element(element).perform()  # マウスオーバー
        time.sleep(0.2)  # 少し待つ
        driver.execute_script("arguments[0].click();", element)  # クリック
    except Exception as e:
        print(f"要素にマウスオーバー中にエラーが発生しました: {e}")

def select_option_with_js(driver, xpath, value):
    try:
        # JavaScriptを使ってセレクトボックスの値を変更
        driver.execute_script(f"""
            var select = document.evaluate('{xpath}', document, null, XPathResult.FIRST_ORDERED_NODE_TYPE, null).singleNodeValue;
            if (select) {{
                select.value = '{value}';
                var event = new Event('change', {{ bubbles: true }});
                select.dispatchEvent(event);
            }}
        """)
    except Exception as e:
        print(f"セレクトボックスの操作中にエラーが発生しました: {e}")

def select_option(driver, target_selectbox_xpath, value_or_visibletext, use_value=True):
    """
    指定されたセレクトボックスに値を設定する関数。

    Args:
        driver: Selenium WebDriverオブジェクト
        target_selectbox_xpath: セレクトボックスのXPath
        value_or_visibletext: 設定する値（value属性またはvisible text）
        use_value: Trueならvalue属性を使用し、Falseならvisible textを使用する

    Returns:
        成功すればTrue、失敗すればFalseを返す
    """
    try:
        # セレクトボックスを取得
        select_element = driver.find_element_by_xpath(target_selectbox_xpath)
        select_box = Select(select_element)
        
        if use_value:
            # value属性で選択
            select_box.select_by_value(value_or_visibletext)
            #print(f"セレクトボックスの値 '{value_or_visibletext}' をvalue属性で選択しました。")
        else:
            # visible textで選択
            select_box.select_by_visible_text(value_or_visibletext)
            #print(f"セレクトボックスの値 '{value_or_visibletext}' をvisible textで選択しました。")
        
        return True
    except NoSuchElementException as e:
        print(f"エラー: セレクトボックスが見つかりませんでした。詳細: {e}")
    except Exception as e:
        print(f"エラー: 値の設定中に問題が発生しました。詳細: {e}")
    
    return False

def input_iframe_textarea(driver, iframe_xpath, content_area_xpath, content):
    """
    指定したiframe内のcontentEditableエリアにテキストを入力する関数

    Parameters:
        driver: WebDriver インスタンス
        iframe_xpath: iframe の XPath
        content_area_xpath: テキストを入力する contentEditable なエリアの XPath
        content: 入力するテキスト
    """
    try:
        # JavaScript用にテキストをエスケープ
        escaped_content = json.dumps(content)


        # 1. iframeに切り替える
        iframe = driver.find_element(By.XPATH, iframe_xpath)
        driver.switch_to.frame(iframe)

        # 2. contentEditableな要素を取得してテキストを入力
        content_area = driver.find_element(By.XPATH, content_area_xpath)

        # JavaScriptを使ってテキストを入力
        driver.execute_script(f"arguments[0].innerHTML = {escaped_content}", content_area)

        # 3. 元のコンテキストに戻す
        driver.switch_to.default_content()

    except Exception as e:
        print(f"エラーが発生しました: {e}")

def send_img_form(driver, img_path, form_name):
    """
    画像の相対パスをフルパスに変換し、指定されたフォームに画像を送信する関数
    
    Args:
        driver: Selenium WebDriver オブジェクト
        img_path: 画像の相対パス (例: 'town_news/image.jpg')
        form_name: 画像を送信するフォームのname属性 (例: 'img')
    """
    # 相対パスからフルパスに変換
    full_image_path = os.path.abspath(img_path)
    
    # 指定されたname属性のフォームに画像を送信
    driver.find_element_by_name(form_name).send_keys(full_image_path)
    #print(f"画像 {full_image_path} をフォーム {form_name} に送信しました。")

def count_jpg_files(directory):
    """ 指定ディレクトリ内のJPGファイル数をカウントする """
    return sum(1 for file in os.listdir(directory) if file.lower().endswith('.jpg'))





if __name__=="__main__":
    ensure_four_characters()
    truncate_text()