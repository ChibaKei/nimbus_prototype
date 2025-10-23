from selenium import webdriver
import chromedriver_binary
import time
import re
import utilites
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait, Select
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.common.alert import Alert
from datetime import datetime
from dateutil.relativedelta import relativedelta 
import random
from pykakasi import kakasi




def pdeco_create(name):
    driver = heaven_login(False)
    time.sleep(1)
    for l in range(5):
        try:
            utilites.dget(driver, "https://newmanager.cityheaven.net/C8GirlMyPageRegist.php?member_id=57542771")
            gal_list = driver.find_element_by_xpath('//*[@id="form_container"]/div/ul')
            count = len(gal_list.find_elements_by_tag_name('li'))
        except:
            driver.refresh()
            time.sleep(5)
            pass
        else:
            break
    
    gals_info = []
    gals_info.append(count)

    for i in range(1,count+1):
        gal_name = driver.find_element_by_xpath(f'//*[@id="form_container"]/div/ul/li[{i}]/div[2]/a')
        gal_name_text = gal_name.get_attribute("innerHTML")
        if gal_name_text == name:
            driver.execute_script("arguments[0].click();", gal_name)
            p_url = driver.find_element_by_xpath('//*[@id="form_container"]/table/tbody/tr/td[2]/table/tbody/tr[2]/td/div[4]/p[2]').get_attribute("innerHTML").strip()
            break


    kks = kakasi()
    # ローマ字にする
    result = kks.convert(gal_name_text)
    p_pass = result[0].get('hepburn')
  
    print(p_url)
    driver.get(p_url)
    time.sleep(3)
    p_divid = driver.find_element_by_class_name('login-id')
    p_id = p_divid.text
    driver.find_element_by_xpath('/html/body/div[1]/div[4]/form/div/div[1]/input[1]').send_keys(p_pass)
    driver.find_element_by_xpath('/html/body/div[1]/div[4]/form/div/div[1]/input[2]').send_keys(p_pass)
    driver.find_element_by_xpath('//*[@id="setting"]').click()
    driver.quit()
    pdeco_info = [gal_name_text,p_id.split("：")[1],p_pass,p_url]
    return pdeco_info

def profile_copy(name):
    driver = heaven_login(True)
    utilites.dget(driver, "https://newmanager.cityheaven.net/C2GirlList.php?shopdir=cb_mbsentai")
    for l in range(5): #キャストの人数カウント
        try:
            gal_list = driver.find_element_by_xpath('//*[@id="list"]')
            count = len(gal_list.find_elements_by_tag_name('li'))
            print("succ")
        except:
            driver.refresh()
            time.sleep(5)
            print("failed")
            pass
        else:
            break

    gals_info = []
    gals_info.append(count)

    for i in range(1,count+1): #キャストリスト作成
        gal_name = driver.find_element_by_xpath(f'//*[@id="list"]/li[{i}]/div/h5')
        gal_name_text = gal_name.get_attribute("innerHTML")
        gals_info.append(gal_name_text)

    search_element = name
    try:
        index = gals_info.index(search_element)
        print("要素が見つかりました。インデックス:", index)
    except ValueError:
        print("要素が見つかりませんでした")
        pass
    
    for l in range(2):
        try:
            driver.find_element_by_xpath(f'//*[@id="list"]/li[{index}]/div/div[4]/input[1]').click()
            #= //*[@id="bodyLayout"]/div/div[2]/div/form/div[1]/table/tbody/tr[24]/td/div/input[1]
            gal_name_t = driver.find_element_by_xpath('//*[@id="bodyLayout"]/div/div[2]/div/form/div[1]/table/tbody/tr[6]/td/div/input').get_attribute("value")
            age = driver.find_element_by_xpath('//*[@id="bodyLayout"]/div/div[2]/div/form/div[1]/table/tbody/tr[21]/td/div/input').get_attribute("value")
            tall = driver.find_element_by_xpath('//*[@id="bodyLayout"]/div/div[2]/div/form/div[1]/table/tbody/tr[24]/td/div/input[1]').get_attribute("value")
            bust = driver.find_element_by_xpath('//*[@id="bodyLayout"]/div/div[2]/div/form/div[1]/table/tbody/tr[24]/td/div/input[2]').get_attribute("value")
            bust_cup = Select(driver.find_element_by_id('sel_GirlCup')).first_selected_option.text
            west = driver.find_element_by_xpath('//*[@id="bodyLayout"]/div/div[2]/div/form/div[1]/table/tbody/tr[24]/td/div/input[3]').get_attribute("value")
            hip = driver.find_element_by_xpath('//*[@id="bodyLayout"]/div/div[2]/div/form/div[1]/table/tbody/tr[24]/td/div/input[4]').get_attribute("value")
            gal_comment = driver.find_element_by_xpath('//*[@id="bodyLayout"]/div/div[2]/div/form/div[1]/table/tbody/tr[26]/td/div/textarea').get_attribute("value")
            owner_comment = driver.find_element_by_xpath('//*[@id="bodyLayout"]/div/div[2]/div/form/div[1]/table/tbody/tr[27]/td/div/textarea').get_attribute("value")
            preview_job = driver.find_element_by_xpath('//*[@id="bodyLayout"]/div/div[2]/div/form/div[1]/table/tbody/tr[29]/td/div/input').get_attribute("value")
            fav = driver.find_element_by_xpath('//*[@id="bodyLayout"]/div/div[2]/div/form/div[1]/table/tbody/tr[31]/td/div/input').get_attribute("value")
            personality = driver.find_element_by_xpath('//*[@id="bodyLayout"]/div/div[2]/div/form/div[1]/table/tbody/tr[33]/td/div/input').get_attribute("value")
            charm_point = driver.find_element_by_xpath('//*[@id="bodyLayout"]/div/div[2]/div/form/div[1]/table/tbody/tr[35]/td/div/input').get_attribute("value")
            sorm = driver.find_element_by_xpath('//*[@id="bodyLayout"]/div/div[2]/div/form/div[1]/table/tbody/tr[37]/td/div/input').get_attribute("value")
            skill = driver.find_element_by_xpath('//*[@id="bodyLayout"]/div/div[2]/div/form/div[1]/table/tbody/tr[39]/td/div/input').get_attribute("value")
            ezone = driver.find_element_by_xpath('//*[@id="bodyLayout"]/div/div[2]/div/form/div[1]/table/tbody/tr[41]/td/div/input').get_attribute("value")
            under_hair = driver.find_element_by_xpath('//*[@id="bodyLayout"]/div/div[2]/div/form/div[1]/table/tbody/tr[43]/td/div/input').get_attribute("value")
            masterbation = driver.find_element_by_xpath('//*[@id="bodyLayout"]/div/div[2]/div/form/div[1]/table/tbody/tr[45]/td/div/input').get_attribute("value")
            option = driver.find_element_by_xpath('//*[@id="bodyLayout"]/div/div[2]/div/form/div[1]/table/tbody/tr[47]/td/div/input').get_attribute("value")
        except:
            driver.refresh()
            time.sleep(5)
            pass
        else:
            break
    
    #姫デコ登録//*[@id="form_container"]/table/tbody/tr/td[2]/table/tbody/tr[2]/td/div[4]/p[2]/text()
    #driver.find_element_by_xpath('//*[@id="bodyLayout"]/div/div[1]/ul/li[6]/a').click()
    

    info = [gal_name_t,age,tall,bust,bust_cup,west,hip,gal_comment,owner_comment,preview_job,fav,personality,charm_point,sorm,skill,ezone,under_hair,masterbation,option,gals_info]
    i=0
    for item in info:
        #print(i,item)
        i += 1
    driver.quit()
    return info

def heaven_opening():
    """try:"""
    driver  = heaven_login(False)
    print('heaven-opening_start!')
    utilites.dget(driver, "https://newmanager.cityheaven.net/C9StandbyGirlList.php?shopdir=cb_mbsentai#TopAnchor")
    today_gal_list = driver.find_element_by_xpath('//*[@id="today"]/table/tbody/tr/td/ul')
    count = len(today_gal_list.find_elements_by_tag_name('li'))
    for i in range(1,count+1):
        gal_cont = driver.find_element_by_xpath(f'//*[@id="today"]/table/tbody/tr/td/ul/li[{i}]')
        time_elm = driver.find_element_by_xpath(f'//*[@id="today"]/table/tbody/tr/td/ul/li[{i}]/table/tbody/tr[1]/td[2]/table[1]/tbody/tr[2]/td')
        time_text = time_elm.get_attribute("innerHTML").split(":")[0]
        if time_text == "":
            continue
        utilites.scroll_to_element(driver, f'//*[@id="today"]/table/tbody/tr/td/ul/li[{i}]/table/tbody/tr[2]/td/table/tbody/tr/td/img[1]')
        time.sleep(1)
        btn = driver.find_element_by_xpath(f'//*[@id="today"]/table/tbody/tr/td/ul/li[{i}]/table/tbody/tr[2]/td/table/tbody/tr/td/img[1]')
        driver.execute_script("arguments[0].click();", btn)
        hour = driver.find_element_by_xpath('//*[@id="servingEndHourList"]')
        Select(hour).select_by_visible_text(time_text.lstrip())
        minute = driver.find_element_by_xpath('//*[@id="servingEndMinuteList"]')
        Select(minute).select_by_visible_text("00")
        driver.execute_script("arguments[0].click();", driver.find_element_by_xpath('//*[@id="popup_ok"]'))
        
        time.sleep(1)
    print('heaven-opening_finish!')
    driver.quit()
    """except:
        pass"""

def heaven_kg_auto():

    def get_kg_list():
        driver = heaven_login()
        utilites.dget(driver, "https://newmanager.cityheaven.net/C2ComeOnGiftList.php?shopdir=cb_mbsentai")
        driver.find_element_by_xpath('//*[@id="form_event"]/div/table/tbody/tr[1]/td[6]/div/a').click()
        giftgals = driver.find_element_by_xpath('//*[@id="girlsSelectedStr"]')
        gg_list = giftgals.get_attribute("innerHTML").replace("\n", "").replace(" ", "").split("、")
        #print(gg_list)
        targets = []
        for i in range(0,5):
            targets.append(utilites.truncate_text(gg_list[i])) 
        #print(targets)

        return targets

    kg_target = get_target_gal_info(get_kg_list())
    print(kg_target)
    for i in range(5):
        pdeco_login(kg_target[i][0],kg_target[i][1],kg_target[i][2])
    



if __name__=="__main__":
    heaven_login()
    heaven_update()
    heaven_kitene2()
    pdeco_create()
    
