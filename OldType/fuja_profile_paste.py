#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
fujaプロフィールペースト実行スクリプト
"""

import json
from profile_copy import ProfileCopy

def get_profile_from_heaven(name):
    """ヘブンからプロフィール情報を取得"""
    print(f"ヘブンからプロフィール情報を取得中... (キャスト名: {name})")
    profile_copy = ProfileCopy(name, "test@example.com")
    
    # プロフィール情報を辞書形式で出力
    profile_data = {
        "name": profile_copy.info[0],
        "age": profile_copy.info[1],
        "height": profile_copy.info[2],
        "bust": profile_copy.info[3],
        "cup": profile_copy.info[4],
        "waist": profile_copy.info[5],
        "hip": profile_copy.info[6],
        "girl_comment": profile_copy.info[7],
        "owner_comment": profile_copy.info[8],
        "prev_job": profile_copy.info[9],
        "hobby": profile_copy.info[10],
        "personality": profile_copy.info[11],
        "charm_point": profile_copy.info[12],
        "sommelier": profile_copy.info[13],
        "skill": profile_copy.info[14],
        "e_zone": profile_copy.info[15],
        "underwear": profile_copy.info[16],
        "masturbation": profile_copy.info[17],
        "option": profile_copy.info[18],
        "message": profile_copy.message
    }
    
    print("\n=== 取得したプロフィール情報 ===")
    print(json.dumps(profile_data, ensure_ascii=False, indent=2))
    print("\n=== 次回実行用のコード ===")
    print("以下のコードをスクリプト内のEMBEDDED_PROFILEにコピーしてください:")
    print("EMBEDDED_PROFILE = " + json.dumps(profile_data, ensure_ascii=False, indent=2))
    
    return profile_data

def create_profile_copy_from_embedded(profile_data):
    """埋め込まれたプロフィール情報からProfileCopyインスタンスを作成"""
    class EmbeddedProfileCopy:
        def __init__(self, profile_data):
            self.name = profile_data["name"]
            self.mail = "test@example.com"
            self.info = [
                profile_data["name"],
                profile_data["age"],
                profile_data["height"],
                profile_data["bust"],
                profile_data["cup"],
                profile_data["waist"],
                profile_data["hip"],
                profile_data["girl_comment"],
                profile_data["owner_comment"],
                profile_data["prev_job"],
                profile_data["hobby"],
                profile_data["personality"],
                profile_data["charm_point"],
                profile_data["sommelier"],
                profile_data["skill"],
                profile_data["e_zone"],
                profile_data["underwear"],
                profile_data["masturbation"],
                profile_data["option"]
            ]
            self.message = profile_data["message"]
            self.INPUT_EMOJI = """
                    arguments[0].value += arguments[1];
                    arguments[0].dispatchEvent(new Event('change'));
                        """
        
        def profile_paste_fuja(self):
            import fuja
            driver = fuja.fuja_login(False)
            print('fujaStart')
            import time
            time.sleep(5)
            
            print("1. ガール追加メニューをクリック中...")
            gal_add = driver.find_element_by_css_selector('#wrapper > div > div.leftColumn > nav > div:nth-child(8) > div > ul > li:nth-child(2) > a')
            driver.execute_script("arguments[0].click();", gal_add)
            print("   ガール追加メニュークリック完了")
            
            for l in range(2):
                try:
                    print(f"2. 試行 {l+1}/2: フォーム要素を取得中...")
                    from selenium.webdriver.support.ui import Select
                    element0 = driver.find_element_by_xpath('//*[@id="form_girl_name"]')
                    print("   名前フィールド取得成功")
                    Select(driver.find_element_by_xpath('//*[@id="form_girl_cup"]')).select_by_visible_text(self.info[4])
                    print("   カップ選択完了")
                    element1 = driver.find_element_by_xpath('//*[@id="form_girl_age"]')
                    element2 = driver.find_element_by_xpath('//*[@id="form_girl_height"]')
                    element3 = driver.find_element_by_xpath('//*[@id="form_girl_sizeb"]')
                    element5 = driver.find_element_by_xpath('//*[@id="form_girl_sizew"]')
                    element6 = driver.find_element_by_xpath('//*[@id="form_girl_sizeh"]')
                    element7 = driver.find_element_by_xpath('//*[@id="form_girl_pr"]')
                    #element8 = driver.find_element_by_xpath('//*[@id="form_comments"]')  # コメントアウト
                    element9 = driver.find_element_by_xpath('//*[@id="form_prof_a1"]')  # 前職
                    element10 = driver.find_element_by_xpath('//*[@id="form_prof_a2"]')  # 趣味
                    element11 = driver.find_element_by_xpath('//*[@id="form_prof_a3"]')  # 性格
                    element12 = driver.find_element_by_xpath('//*[@id="form_prof_a4"]')  # チャームポイント
                    element13 = driver.find_element_by_xpath('//*[@id="form_prof_a5"]')  # S?%M?%
                    element14 = driver.find_element_by_xpath('//*[@id="form_prof_a6"]')  # 得意プレイ
                    element15 = driver.find_element_by_xpath('//*[@id="form_prof_a7"]')  # 性感帯
                    element16 = driver.find_element_by_xpath('//*[@id="form_prof_a8"]')  # パイパン？
                    element17 = driver.find_element_by_xpath('//*[@id="form_prof_a9"]')  # オナニー
                    element18 = driver.find_element_by_xpath('//*[@id="form_prof_a10"]')  # 好きなオプション
                    driver.execute_script(self.INPUT_EMOJI, element0, self.info[0])
                    driver.execute_script(self.INPUT_EMOJI, element1, self.info[1])
                    driver.execute_script(self.INPUT_EMOJI, element2, self.info[2])
                    driver.execute_script(self.INPUT_EMOJI, element3, self.info[3])
                    driver.execute_script(self.INPUT_EMOJI, element5, self.info[5])
                    driver.execute_script(self.INPUT_EMOJI, element6, self.info[6])
                    driver.execute_script(self.INPUT_EMOJI, element9, self.info[9])   # 前職
                    driver.execute_script(self.INPUT_EMOJI, element10,self.info[10])  # 趣味
                    driver.execute_script(self.INPUT_EMOJI, element11,self.info[11])  # 性格
                    driver.execute_script(self.INPUT_EMOJI, element12,self.info[12])  # チャームポイント
                    driver.execute_script(self.INPUT_EMOJI, element13,self.info[13])  # S?%M?%
                    driver.execute_script(self.INPUT_EMOJI, element14,self.info[14])  # 得意プレイ
                    driver.execute_script(self.INPUT_EMOJI, element15,self.info[15])  # 性感帯
                    driver.execute_script(self.INPUT_EMOJI, element16,self.info[16])  # パイパン？
                    driver.execute_script(self.INPUT_EMOJI, element17,self.info[17])  # オナニー
                    driver.execute_script(self.INPUT_EMOJI, element18,self.info[18])  # 好きなオプション
                    driver.execute_script(self.INPUT_EMOJI, element7, self.message)
                    print("   全フィールド入力完了")
                    time.sleep(1)
                    print("3. 送信ボタンをクリック中...")
                    driver.find_element_by_name('entry-submit').click()
                    print("   送信ボタンクリック完了")
                except Exception as e:
                    print(f"fuja-failed: {str(e)}")
                    import traceback
                    traceback.print_exc()
                    pass
                else:
                    break
                time.sleep(2)
            driver.quit()
    
    return EmbeddedProfileCopy(profile_data)

def main():
    # キャスト名を設定（ここを変更してください）
    name = "あやせ"  # 実際のキャスト名に変更してください
    
    # 埋め込まれたプロフィール情報（初回実行時はNone、取得後にコピーして使用）
    EMBEDDED_PROFILE = {
      "name": "あやせ",
      "age": "19",
      "height": "162",
      "bust": "85",
      "cup": "E",
      "waist": "55",
      "hip": "82",
      "girl_comment": "おっとりマイペースな性格ですがお兄さんに気持ちよくなって笑顔で帰って貰えるようにがんばります♡♡",
      "owner_comment": "可能ｵﾌﾟｼｮﾝ\nﾉｰﾊﾟﾝ入室→〇\nﾛｰﾀｰ→〇\nｺｽﾌﾟﾚ→〇\nｱﾅﾙ舐め→〇\n即尺→〇\n聖水→〇\nﾊﾞｲﾌﾞ→〇\n電ﾏ→〇\nごっくん→〇\n撮影(顔なし)→〇\n撮影(顔あり)→〇\nﾁｪｷ（顔あり）→〇\nお客様2名の3p→〇",
      "prev_job": "メイドさん",
      "hobby": "音楽、居酒屋めぐり",
      "personality": " おっとり？",
      "charm_point": "くりくりおめめ、ピンク色のち♡び",
      "sommelier": "S40%M60%",
      "skill": "ふぇら",
      "e_zone": "色んな所敏感なので探しに来てください🙈",
      "underwear": "はい♡♡",
      "masturbation": "します♡♡",
      "option": "玩具、コスプレ",
      "message": "おっとりマイペースな性格ですがお兄さんに気持ちよくなって笑顔で帰って貰えるようにがんばります♡♡\n\n\n可能ｵﾌﾟｼｮﾝ\nﾉｰﾊﾟﾝ入室→〇\nﾛｰﾀｰ→〇\nｺｽﾌﾟﾚ→〇\nｱﾅﾙ舐め→〇\n即尺→〇\n聖水→〇\nﾊﾞｲﾌﾞ→〇\n電ﾏ→〇\nごっくん→〇\n撮影(顔なし)→〇\n撮影(顔あり)→〇\nﾁｪｷ（顔あり）→〇\nお客様2名の3p→〇"
    }
    
    # 初回実行時はヘブンから取得、2回目以降は埋め込まれたデータを使用
    if EMBEDDED_PROFILE is None:
        # 初回実行：ヘブンからプロフィール情報を取得
        profile_data = get_profile_from_heaven(name)
        print("\n初回実行完了。上記のEMBEDDED_PROFILEをスクリプト内にコピーして再実行してください。")
    else:
        # 2回目以降：埋め込まれたプロフィール情報を使用
        print(f"埋め込まれたプロフィール情報を使用: {EMBEDDED_PROFILE['name']}")
        profile_copy = create_profile_copy_from_embedded(EMBEDDED_PROFILE)
        profile_copy.profile_paste_fuja()
        print(f"{EMBEDDED_PROFILE['name']}のプロフィールをfujaにペーストしました")

if __name__ == "__main__":
    main() 