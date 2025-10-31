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




def town_gal_count():
    driver = town_login(True)
    utilites.dget(driver, 'https://admin.dto.jp/shop-admin/34627/standby')
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
    
    with open('town_news/town_news_text.csv', "r", encoding = "utf-8") as f:
        reader = csv.reader(f)
        l = [row for row in reader]
    time.sleep(5)
    for k in range(5):
        try:
            driver.find_element_by_id(f"type_{l[int][0]}").click()
            driver.find_element_by_name("title").send_keys(l[int][1])
            driver.find_element_by_name("content").send_keys(l[int][2])
            utilites.send_img_form(driver, os.path.join('town_news', f"{l[int][3]}.jpg"), 'image')
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
            utilites.dget(driver, 'https://admin.dto.jp/shop-admin/34627/diary/list')
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
    utilites.dget(driver, 'https://admin.dto.jp/shop-admin/34627/diary/list?page=2')
    time.sleep(3)
    diary_table_d = driver.find_element_by_xpath('//*[@id="diaries"]/table/tbody')
    rows = diary_table_d.find_elements_by_tag_name('tr')
    for j in range(2,len(rows)+1):
        cast_d = utilites.clean_and_extract_text(diary_table_d.find_element_by_xpath(f'tr[{j}]/td[1]').get_attribute("innerHTML"))
        title_d = utilites.clean_and_extract_text(diary_table_d.find_element_by_xpath(f'tr[{j}]/td[2]/a').get_attribute("innerHTML"))
        date_d = utilites.clean_and_extract_text(diary_table_d.find_element_by_xpath(f'tr[{j}]/td[4]').get_attribute("innerHTML"))
        content_d.append([cast_d, title_d, date_d])
    utilites.dget(driver, 'https://admin.dto.jp/shop-admin/34627/diary/list?page=3')
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
            utilites.dget(driver, 'https://admin.dto.jp/shop-admin/34627/schedule/list')
            Select(driver.find_element_by_xpath('//*[@id="top"]/div[3]/div/div[2]/div[2]/div[3]/div[3]/form/select')).select_by_visible_text("300件")
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