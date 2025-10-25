from selenium import webdriver
import chromedriver_binary
import time
import datetime
from selenium.webdriver.chrome.options import Options 
from selenium.common.exceptions import NoSuchElementException, NoAlertPresentException
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support.ui import WebDriverWait
import csv
import utilites
import os


def town_login(headless=True, detach=False):
    options = Options()
    if headless:
        options.add_argument('--headless')  # ヘッドレスモード
    if detach:
        options.add_experimental_option("detach", True)  # detachオプションを追加

    driver = webdriver.Chrome(options=options) 
    driver.implicitly_wait(10)
    url = "https://www.dto.jp/a/auth"
    utilites.dget(driver, url, checkf=True)

    time.sleep(1)  # ページの読み込みを待機

    for attempt in range(5):
        try:
            town_id = driver.find_element_by_id("login_id")
            town_pass = driver.find_element_by_name("password")
            town_id.click()
            town_id.send_keys("mbasato@icloud.com")
            town_pass.click()
            town_pass.send_keys("shakeshake")
            driver.find_element_by_id("login_button").click()

            return driver

        except (NoSuchElementException, TimeoutException) as e:
            driver.refresh()
            time.sleep(5)

    driver.quit()
    return None

def town_pickup(int=None, get_count=None):

    def get_cast_count(driver):
        
        try:
            count = 0
            gal_list = driver.find_element_by_xpath('//*[@id="gals"]')
            count = len(gal_list.find_elements_by_tag_name('li'))
            finished_gal_count = len(gal_list.find_elements_by_class_name("disabled"))

            count -= finished_gal_count

            #print("count:",count)
            driver.quit()
            return count
        finally:
            driver.quit()
    

    driver = town_login()
    time.sleep(1)
    utilites.dget(driver, 'https://admin.dto.jp/shop-admin/37056/standby')

    if get_count:# カウント取得
        count = get_cast_count(driver)
        driver.quit()
        return count
    
    time.sleep(1)            
    for l in range(5):
        try:
            driver.find_element_by_link_text("待機情報").click()
            driver.find_element_by_link_text("女の子の並び順で表示").click()
            driver.find_element_by_xpath(f'//*[@id="gals"]/li[{int}]/div/div[4]/a[2]').click() #待機中ボタン
            try:
              xpath = '//*[@id="one_left_flag"]'
              chkbox = driver.find_element_by_xpath(xpath)
              # チェックボックスが非選択の状態を確認
              if not chkbox.is_selected():
                  # 非選択の場合はJavaScriptでクリックする
                  driver.execute_script("arguments[0].click();", chkbox)
            except:
                pass
            driver.find_element_by_xpath(f'//*[@id="gals"]/li[{int}]/div/div[4]/div/div/div/div/a[1]').click() #待機中モーダル
            time.sleep(2)
        except NoAlertPresentException:
            pass
        except:
            driver.refresh()
            time.sleep(5)
            pass
        else:
            break

    for l in range(5):
        try:
            driver.find_element_by_xpath(f'//*[@id="gals"]/li[{int}]/div/div[4]/a[3]').click() #pickupボタン
            alert = driver.switch_to_alert() #pickupアラート
            alert.accept()
        except NoAlertPresentException:
            pass
            break
        except:
            driver.refresh()
            time.sleep(5)
        else:
            break
        
    time.sleep(1)
    driver.quit()

def town_gal_count():
    driver = town_login(True)
    utilites.dget(driver, 'https://admin.dto.jp/shop-admin/37056/standby')
    count = 0
    for l in range(5):
        try:
            gal_list = driver.find_element_by_xpath('//*[@id="gals"]')
            count = len(gal_list.find_elements_by_tag_name('li'))
        except:
            driver.refresh()
            time.sleep(5)
            count = 8
            pass
        else:
            break
    
    for l in range(5):
        try:
            finished_gal_count = len(gal_list.find_elements_by_class_name("disabled"))
        except:
            driver.refresh()
            time.sleep(5)
            pass
        else:
            #print("finishled_gal:",finished_gal_count)
            break
    count -= finished_gal_count

    if count <= 0:
        count = 8
    #print("count:",count)
    driver.quit()
    return count

def town_news(int):
    driver = town_login()
    time.sleep(1)
    for l in range(5):
        try:
            driver.find_element_by_link_text("お知らせ").click()
            driver.find_element_by_link_text("お知らせ新規登録").click()
        except:
            driver.refresh()
            time.sleep(5)
            pass
        else:
            break
    
    with open('shake_town_news/shake_town_news_text.csv', "r", encoding = "utf-8") as f:
        reader = csv.reader(f)
        l = [row for row in reader]
    time.sleep(5)
    for k in range(5):
        try:
            driver.find_element_by_id(f"type_{l[int][0]}").click()
            driver.find_element_by_name("title").send_keys(l[int][1])
            driver.find_element_by_name("content").send_keys(l[int][2])
            utilites.send_img_form(driver, os.path.join('shake_town_news', f"{l[int][3]}.jpg"), 'image')
            driver.find_element_by_css_selector("body > div.main_frame > div > div.shop_admin > div.shop_admin_body > div.information_regist > form > div > input").click()
            time.sleep(1)
            driver.find_element_by_css_selector("body > div.main_frame > div > div.shop_admin > div.shop_admin_body > div.com_button_frame.style1 > form:nth-child(2) > input.com_button.style1").click()
            time.sleep(1)
        except:
            driver.refresh()
            time.sleep(5)
            pass
        else:
            break
    driver.quit()

def get_town_diary_list():
    driver = town_login()
    for l in range(2):
        try: 
            utilites.dget(driver, 'https://admin.dto.jp/shop-admin/37056/diary/list')
            diary_table_d = driver.find_element_by_xpath('//*[@id="diaries"]/table/tbody')
            rows = diary_table_d.find_elements_by_tag_name('tr')
        except:
            driver.refresh()
            time.sleep(5)
            pass
        else:
            break
    content_d = []
    for i in range(2,len(rows)+1):
        cast_d = utilites.clean_and_extract_text(diary_table_d.find_element_by_xpath(f'tr[{i}]/td[1]').get_attribute("innerHTML"))
        title_d = utilites.clean_and_extract_text(diary_table_d.find_element_by_xpath(f'tr[{i}]/td[2]/a').get_attribute("innerHTML"))
        date_d = utilites.clean_and_extract_text(diary_table_d.find_element_by_xpath(f'tr[{i}]/td[4]').get_attribute("innerHTML"))
        content_d.append([cast_d, title_d, date_d])
        #print(cast_d, title_d, date_d)
    utilites.dget(driver, 'https://admin.dto.jp/shop-admin/37056/diary/list?page=2')
    time.sleep(3)
    diary_table_d = driver.find_element_by_xpath('//*[@id="diaries"]/table/tbody')
    rows = diary_table_d.find_elements_by_tag_name('tr')
    for j in range(2,len(rows)+1):
        cast_d = utilites.clean_and_extract_text(diary_table_d.find_element_by_xpath(f'tr[{j}]/td[1]').get_attribute("innerHTML"))
        title_d = utilites.clean_and_extract_text(diary_table_d.find_element_by_xpath(f'tr[{j}]/td[2]/a').get_attribute("innerHTML"))
        date_d = utilites.clean_and_extract_text(diary_table_d.find_element_by_xpath(f'tr[{j}]/td[4]').get_attribute("innerHTML"))
        content_d.append([cast_d, title_d, date_d])
    utilites.dget(driver, 'https://admin.dto.jp/shop-admin/37056/diary/list?page=3')
    time.sleep(3)
    diary_table_d = driver.find_element_by_xpath('//*[@id="diaries"]/table/tbody')
    rows = diary_table_d.find_elements_by_tag_name('tr')
    for j in range(2,len(rows)+1):
        cast_d = utilites.clean_and_extract_text(diary_table_d.find_element_by_xpath(f'tr[{j}]/td[1]').get_attribute("innerHTML"))
        title_d = utilites.clean_and_extract_text(diary_table_d.find_element_by_xpath(f'tr[{j}]/td[2]/a').get_attribute("innerHTML"))
        date_d = utilites.clean_and_extract_text(diary_table_d.find_element_by_xpath(f'tr[{j}]/td[4]').get_attribute("innerHTML"))
        content_d.append([cast_d, title_d, date_d])
    driver.quit()
    return content_d

def set_town_schedule(cont):
    for l in range(2):
        try: 
            driver = town_login()
            utilites.dget(driver, 'https://admin.dto.jp/shop-admin/37056/schedule/list')
            #Select(driver.find_element_by_xpath('//*[@id="top"]/div[3]/div/div[2]/div[2]/div[3]/div[3]/form/select')).select_by_visible_text("300件")
            schedule_table_t = driver.find_element_by_xpath('//*[@id="schedules"]/tbody')
            gals_count = len(schedule_table_t.find_elements_by_tag_name('tr'))
        except:
            driver.refresh()
            time.sleep(5)
            pass

    #try:
    k = 0
    for cast_cont in cont:
        cast_name = cast_cont[0]  # 配列内キャストの名前
        printbox = []
        k += 1
        for i in range (1, gals_count + 1):
            target_cast_table = schedule_table_t.find_element_by_xpath(f'tr[{i}]')
            target_cast_name = schedule_table_t.find_element_by_xpath(f'tr[{i}]/td[1]/a').get_attribute("innerHTML")
            if target_cast_name == cast_name:
                printbox.append(cast_name)
                gal_days = []
                #print(target_cast_name + "+town")
                for j in range(3, 10):
                    target_checkbox = (f'/html/body/div[3]/div/div[2]/div[2]/table/tbody/tr[{i}]/td[{j}]/div/div[1]/label/input')

                    if utilites.set_checkbox_for_time(cast_cont[j - 2][0], driver, target_checkbox) == True:
                        start_time = cast_cont[j - 2][0]
                        end_time = cast_cont[j - 2][1]
                        gal_day = [start_time, end_time]
                        Select(target_cast_table.find_element_by_xpath(f'td[{j}]/div/div[2]/div[1]/select')).select_by_visible_text(start_time)
                        Select(target_cast_table.find_element_by_xpath(f'td[{j}]/div/div[2]/div[3]/select')).select_by_visible_text(end_time)
                        gal_days.append(gal_day)
                    else:
                        gal_days.append('休み')
        printbox.append(gal_days)
    driver.find_element_by_xpath('//*[@id="save_button"]').click()
    time.sleep(3)  
    """except:
        pass"""
    driver.quit()
                  





if __name__=="__main__":
    town_login()
    town_pickup()
    town_gal_count()
    town_news()