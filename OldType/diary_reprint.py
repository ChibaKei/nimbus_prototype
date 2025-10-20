import town
import time
import datetime
import random
import ekichika
import heaven
import utilites
from datetime import datetime
import os
import requests
import re



def diary_save_and_submit(cast, title):
    def diary_save(cast, title):
        save_dir = "diary_img_draft"
        os.makedirs(save_dir, exist_ok=True)
        driver = get_heaven_diary(cast, title)

        title = driver.find_element_by_xpath('//*[@id="bodyLayout"]/div/div[2]/div/form/div/table/tbody/tr[3]/td/div/input').get_attribute("value")
        content = driver.find_element_by_xpath('//*[@id="lbl_body"]').get_attribute("value")
        r_content = re.sub(r'<img[^>]*>', '', content)

        warning_text = driver.find_element_by_xpath('//*[@id="photoArea"]/td/div[2]').get_attribute("innerHTML")

        # 条件に応じて処理を分岐
        if warning_text == "※動画につきましては変更､削除はできません。削除したい場合は日記の削除をおこなってください。":
            # 動画に関する処理
            video_element = driver.find_element_by_xpath('//video')  # video要素を取得
            img_url = video_element.get_attribute('poster')  # poster属性からサムネイル画像のURLを取得
        elif warning_text == "※静止画でアップしてください。":
            # 画像に関する処理
            img_elem = driver.find_element_by_xpath('//*[@id="preview"]/img')
            img_url = img_elem.get_attribute('src')
        else:
            print("警告テキストが想定外です。")
            # その他のケースの処理

        image_data = requests.get(img_url).content  # URLから画像を取得
        image_path = os.path.join(save_dir, 'diary_img.jpg')  # 保存パスを設定
        with open(image_path, 'wb') as file:
            file.write(image_data)


        diary_content = [cast, title, r_content]
        diary_content[2] = f"{diary_content[2]}\n\n△△"
        driver.quit()
        return diary_content
    
    def diary_submit(cast, diary_contents):
        driver = town.town_login()
        utilites.dget(driver, "https://admin.dto.jp/shop-admin/34627/diary-management/list")
        diary_conts = diary_contents
        gal_list = driver.find_element_by_xpath('//*[@id="top"]/div[3]/div/div[2]/div[2]/div[3]/table/tbody')
        count = len(gal_list.find_elements_by_tag_name('tr'))
        for i in range(2,count+1):
            gal_name = driver.find_element_by_xpath(f'/html/body/div[3]/div/div[2]/div[2]/div[3]/table/tbody/tr[{i}]/td[1]/a')
            gal_name_text = gal_name.get_attribute("innerHTML")
            if cast == gal_name_text:
                for l in range(3):
                    try:
                        driver.find_element_by_xpath(f'/html/body/div[3]/div/div[2]/div[2]/div[3]/table/tbody/tr[{i}]/td[5]/form/input').click()
                        time.sleep(2)
                        emoji = utilites.INPUT_EMOJI
                        title_elem = driver.find_element_by_xpath('//*[@id="top"]/div[3]/div/div[2]/div[2]/div[2]/div[3]/form/table/tbody/tr[3]/td[2]/input')
                        content_elem = driver.find_element_by_xpath('//*[@id="contents"]/td[2]/textarea')
                        driver.execute_script(emoji, title_elem, diary_conts[1])
                        driver.execute_script(emoji, content_elem, diary_conts[2])
                        utilites.send_img_form(driver, 'diary_img_draft/diary_img.jpg', 'image')
                        driver.find_element_by_css_selector('#top > div.main_frame > div > div.shop_admin > div.shop_admin_body > div.shop_diary > div.diary_regist > form > div > input').click()
                        time.sleep(2)
                        driver.find_element_by_css_selector('#top > div.main_frame > div > div.shop_admin > div.shop_admin_body > div.shop_diary > div.com_button_frame.style1 > form:nth-child(2) > input.com_button.style1').click()
                        break
                    except: 
                        driver.refresh()
                        time.sleep(5)
                        pass
                    else:
                        break
                break
        driver.quit()
    
    diary_cont = diary_save(cast, title)
    diary_submit(cast, diary_cont)



def get_heaven_diary(cast=None, title=None):
    driver = heaven.heaven_login()
    utilites.dget(driver, 'https://newmanager.cityheaven.net/C8KeitaiDiaryList.php?shopdir=cb_mbsentai')

    diary_table_h = driver.find_element_by_xpath('//*[@id="bodyLayout"]/div/div[2]/div/form/div/table/tbody')
    rows = diary_table_h.find_elements_by_tag_name('tr')
    content_h = []

    for i in range(1, len(rows)):
        date_h = utilites.clean_and_extract_text(diary_table_h.find_element_by_xpath(f'tr[{i}]/td[1]/h4').get_attribute("innerHTML"))
        cast_h = utilites.clean_and_extract_text(diary_table_h.find_element_by_xpath(f'tr[{i}]/td[2]').get_attribute("innerHTML"))
        title_h = utilites.clean_and_extract_text(diary_table_h.find_element_by_xpath(f'tr[{i}]/td[4]/p').get_attribute("innerHTML"))
        
        # 「マイガール限定」のチェック処理
        if title_h == 'マイガール限定':
            title_h = utilites.clean_and_extract_text(diary_table_h.find_element_by_xpath(f'tr[{i}]/td[4]/p[2]').get_attribute("innerHTML"))
        
        # 引数がない場合、全てのデータを取得
        if not cast and not title:
            content_h.append([cast_h, title_h, date_h])
        # 引数がある場合
        else:
            # 引数のcastとtitleと一致する場合
            if cast_h == cast and title_h == title:
                diary_table_h.find_element_by_xpath(f'tr[{i}]/td[5]/div/a').click()
                time.sleep(3)
                return driver
    
    driver.quit()
    return content_h


def diary_compare():
    # 現在の年を取得
    current_year = datetime.now().year

    # 日付フォーマットを統一する関数
    def convert_date_format(date_str, format_type):
        if format_type == 'A':  # A配列のフォーマット (09月05日00:55)
            # 現在の年を手動で追加し、日付をパース
            parsed_date = datetime.strptime(f"{current_year}年{date_str}", "%Y年%m月%d日%H:%M")
            return parsed_date.strftime("%Y/%m/%d"), parsed_date.strftime("%H:%M")
        
        elif format_type == 'B':  # B配列のフォーマット (2024/09/0503:56)
            # 日付をパースし、"年/月/日" と "時間:分" に分解
            parsed_date = datetime.strptime(date_str, "%Y/%m/%d%H:%M")
            return parsed_date.strftime("%Y/%m/%d"), parsed_date.strftime("%H:%M")

    # 配列を変換する関数
    def convert_arrays(arr, format_type):
        new_arr = []
        for item in arr:
            cast, title, date = item
            new_date, time = convert_date_format(date, format_type)
            new_arr.append([cast, title, new_date, time])
        return new_arr

    array_A = get_heaven_diary()
    array_B = town.get_town_diary_list()

    # 配列をそれぞれ変換
    converted_A = convert_arrays(array_A, 'A')
    converted_B = convert_arrays(array_B, 'B')
    #print(converted_A, "------", converted_B)
    def compare_arrays(array_A, array_B):
        missing_entries = []

        # Bの配列から [cast, title] のペアを抽出してセットにする
        cast_title_B = set((cast, title) for cast, title, _, _ in array_B)

        # Aの配列をループして、Bに存在するか確認
        for cast, title, _, _ in array_A:
            if (cast, title) not in cast_title_B:
                missing_entries.append([cast, title])

        return missing_entries
    cont = []
    # Aに存在するがBに存在しないペアを取得
    missing_in_B = compare_arrays(converted_A, converted_B)

    # 結果の表示
    if missing_in_B:
        for entry in missing_in_B:
            cont.append(entry)
        return(cont)
    else:
        return(False)
