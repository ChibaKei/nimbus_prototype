
from selenium import webdriver
import chromedriver_binary
import time
import re
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
from selenium.webdriver.support.ui import Select
import random
import math
import heaven
import town
import ekichika
import delija
import fuja
import utilites


class ProfileCopy:

    def __init__(self, name, mail):
        self.name = name
        self.mail = mail

        self.info = heaven.profile_copy(self.name)
        x = [self.info[7], self.info[8]]
        self.message = '\n\n\n'.join(x)
        self.INPUT_EMOJI = """
                arguments[0].value += arguments[1];
                arguments[0].dispatchEvent(new Event('change'));
                    """
        
    def profile_paste_delija(self):
        driver = delija.delija_login(False)
        print('deliStart')
        time.sleep(5)
        gal_add = driver.find_element_by_css_selector('#wrapper > div > div.leftColumn > nav > div:nth-child(8) > div > ul > li:nth-child(2) > a')
        driver.execute_script("arguments[0].click();", gal_add)
        
        for l in range(2):
            try:
                element0 = driver.find_element_by_xpath('//*[@id="form_girl_name"]')
                Select(driver.find_element_by_xpath('//*[@id="form_girl_cup"]')).select_by_visible_text(self.info[4])
                element1 = driver.find_element_by_xpath('//*[@id="form_girl_age"]')
                element2 = driver.find_element_by_xpath('//*[@id="form_girl_height"]')
                element3 = driver.find_element_by_xpath('//*[@id="form_girl_sizeb"]')
                element5 = driver.find_element_by_xpath('//*[@id="form_girl_sizew"]')
                element6 = driver.find_element_by_xpath('//*[@id="form_girl_sizeh"]')
                element7 = driver.find_element_by_xpath('//*[@id="form_girl_pr"]')#comment+Option
                #element8 = driver.find_element_by_xpath('//*[@id="form_comments"]')
                element9 = driver.find_element_by_xpath('//*[@id="form_prof_a2"]')
                element10 = driver.find_element_by_xpath('//*[@id="form_prof_a3"]')
                element11 = driver.find_element_by_xpath('//*[@id="form_prof_a4"]')
                element12 = driver.find_element_by_xpath('//*[@id="form_prof_a5"]')
                element13 = driver.find_element_by_xpath('//*[@id="form_prof_a6"]')
                element14 = driver.find_element_by_xpath('//*[@id="form_prof_a7"]')
                element15 = driver.find_element_by_xpath('//*[@id="form_prof_a8"]')
                element16 = driver.find_element_by_xpath('//*[@id="form_prof_a9"]')
                element17 = driver.find_element_by_xpath('//*[@id="form_prof_a10"]')
                driver.execute_script(self.INPUT_EMOJI, element0, self.info[0])
                driver.execute_script(self.INPUT_EMOJI, element1, self.info[1])
                driver.execute_script(self.INPUT_EMOJI, element2, self.info[2])
                driver.execute_script(self.INPUT_EMOJI, element3, self.info[3])
                driver.execute_script(self.INPUT_EMOJI, element5, self.info[5])
                driver.execute_script(self.INPUT_EMOJI, element6, self.info[6])
                driver.execute_script(self.INPUT_EMOJI, element9, self.info[9])
                driver.execute_script(self.INPUT_EMOJI, element10,self.info[10])
                driver.execute_script(self.INPUT_EMOJI, element11,self.info[11])
                driver.execute_script(self.INPUT_EMOJI, element12,self.info[12])
                driver.execute_script(self.INPUT_EMOJI, element13,self.info[13])
                driver.execute_script(self.INPUT_EMOJI, element14,self.info[14])
                driver.execute_script(self.INPUT_EMOJI, element15,self.info[15])
                driver.execute_script(self.INPUT_EMOJI, element16,self.info[16])
                driver.execute_script(self.INPUT_EMOJI, element17,self.info[17])
                driver.execute_script(self.INPUT_EMOJI, element7, self.message)
                time.sleep(1)
                driver.find_element_by_xpath('//*[@id="girls_add"]/form/div[2]/p/label').click()
            except:
                print("delija-failed")
                pass
            else:
                break
            time.sleep(2)
            driver.quit()

    def profile_paste_fuja(self):
        driver = fuja.fuja_login(False)
        print('fujaStart')
        time.sleep(5)
        gal_add = driver.find_element_by_css_selector('#wrapper > div > div.leftColumn > nav > div:nth-child(8) > div > ul > li:nth-child(2) > a')
        driver.execute_script("arguments[0].click();", gal_add)
        
        for l in range(2):
            try:
                element0 = driver.find_element_by_xpath('//*[@id="form_girl_name"]')
                Select(driver.find_element_by_xpath('//*[@id="form_girl_cup"]')).select_by_visible_text(self.info[4])
                element1 = driver.find_element_by_xpath('//*[@id="form_girl_age"]')
                element2 = driver.find_element_by_xpath('//*[@id="form_girl_height"]')
                element3 = driver.find_element_by_xpath('//*[@id="form_girl_sizeb"]')
                element5 = driver.find_element_by_xpath('//*[@id="form_girl_sizew"]')
                element6 = driver.find_element_by_xpath('//*[@id="form_girl_sizeh"]')
                element7 = driver.find_element_by_xpath('//*[@id="form_girl_pr"]')#comment+Option
                #element8 = driver.find_element_by_xpath('//*[@id="form_comments"]')
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
                time.sleep(1)
                driver.find_element_by_name('entry-submit').click()
            except:
                print("fuja-failed")
                pass
            else:
                break
            time.sleep(2)
            driver.quit()
    

    def profile_paste_ekichika(self):#完成
        driver = ekichika.ekichika_login(False)
        utilites.dget(driver, 'https://ranking-deli.jp/admin/girls/create/')

        for l in range(2):
            try:
                element0 = driver.find_element_by_xpath('//*[@id="form_name"]')
                Select(driver.find_element_by_xpath('//*[@id="form_cup"]')).select_by_visible_text(self.info[4] +"カップ")
                element1 = driver.find_element_by_xpath('//*[@id="form_age"]')
                element2 = driver.find_element_by_xpath('//*[@id="form_tall"]')
                element3 = driver.find_element_by_xpath('//*[@id="form_bust"]')
                element5 = driver.find_element_by_xpath('//*[@id="form_waist"]')
                element6 = driver.find_element_by_xpath('//*[@id="form_hip"]')
                element7 = driver.find_element_by_xpath('//*[@id="form_girl_comments"]')
                element8 = driver.find_element_by_xpath('//*[@id="form_comments"]')
                element9 = driver.find_element_by_xpath('//*[@id="form_answers[2]"]')
                element10 = driver.find_element_by_xpath('//*[@id="form_answers[3]"]')
                element11 = driver.find_element_by_xpath('//*[@id="form_answers[4]"]')
                element12 = driver.find_element_by_xpath('//*[@id="form_answers[5]"]')
                element13 = driver.find_element_by_xpath('//*[@id="form_answers[6]"]')
                element14 = driver.find_element_by_xpath('//*[@id="form_answers[7]"]')
                element15 = driver.find_element_by_xpath('//*[@id="form_answers[8]"]')
                element16 = driver.find_element_by_xpath('//*[@id="form_answers[9]"]')
                element17 = driver.find_element_by_xpath('//*[@id="form_answers[10]"]')
                driver.execute_script(self.INPUT_EMOJI, element0, self.info[0])
                driver.execute_script(self.INPUT_EMOJI, element1, self.info[1])
                driver.execute_script(self.INPUT_EMOJI, element2, self.info[2])
                driver.execute_script(self.INPUT_EMOJI, element3, self.info[3])
                driver.execute_script(self.INPUT_EMOJI, element5, self.info[5])
                driver.execute_script(self.INPUT_EMOJI, element6, self.info[6])
                
                driver.execute_script(self.INPUT_EMOJI, element8, self.info[8])
                driver.execute_script(self.INPUT_EMOJI, element9, self.info[9])
                driver.execute_script(self.INPUT_EMOJI, element10,self.info[10])
                driver.execute_script(self.INPUT_EMOJI, element11,self.info[11])
                driver.execute_script(self.INPUT_EMOJI, element12,self.info[12])
                driver.execute_script(self.INPUT_EMOJI, element13,self.info[13])
                driver.execute_script(self.INPUT_EMOJI, element14,self.info[14])
                driver.execute_script(self.INPUT_EMOJI, element15,self.info[15])
                driver.execute_script(self.INPUT_EMOJI, element16,self.info[16])
                driver.execute_script(self.INPUT_EMOJI, element17,self.info[17])

                
                if len(self.info[7]) <= 200:
                    driver.find_element_by_name('girl_comments').clear()
                    driver.execute_script(self.INPUT_EMOJI, element7, self.info[7])
                time.sleep(1)
            except:
                print("ekichika-failed")
                pass
            else:
                break
        driver.find_element_by_xpath('//*[@id="genre41"]').click()
        driver.find_element_by_xpath('//*[@id="form_update-btn"]').click()
        time.sleep(1)

        driver.quit()

    def profile_paste_town(self):#完成
        driver = town.town_login()
        for l in range(2):
            try:
                utilites.dget(driver, 'https://admin.dto.jp/shop-admin/34627/gal/input')

                element0 = driver.find_element_by_xpath('//*[@id="name"]')
                element1 = driver.find_element_by_xpath('//*[@id="age"]')
                element2 = driver.find_element_by_xpath('//*[@id="height"]')
                element3 = driver.find_element_by_xpath('//*[@id="bust"]')
                element5 = driver.find_element_by_xpath('//*[@id="waist"]')
                element6 = driver.find_element_by_xpath('//*[@id="hip"]')
                element9 = driver.find_element_by_xpath('//*[@id="custom_2_value"]')
                element10 = driver.find_element_by_xpath('//*[@id="custom_3_value"]')
                element11 = driver.find_element_by_xpath('//*[@id="custom_4_value"]')
                element12 = driver.find_element_by_xpath('//*[@id="custom_5_value"]')
                element14 = driver.find_element_by_xpath('//*[@id="custom_6_value"]')
                element15 = driver.find_element_by_xpath('//*[@id="custom_7_value"]')
                element16 = driver.find_element_by_xpath('//*[@id="custom_8_value"]')
                element13 = driver.find_element_by_xpath('//*[@id="custom_9_value"]')
                element17 = driver.find_element_by_xpath('//*[@id="custom_10_value"]')
                element18 = driver.find_element_by_xpath('//*[@id="custom_11_value"]')
                element7 = driver.find_element_by_xpath('//*[@id="form_table"]/tbody/tr[38]/td[2]/textarea')
                Select(driver.find_element_by_xpath('//*[@id="form_table"]/tbody/tr[9]/td[2]/select')).select_by_visible_text(self.info[4])
                driver.execute_script(self.INPUT_EMOJI, element0, self.info[0])
                driver.execute_script(self.INPUT_EMOJI, element1, self.info[1])
                driver.execute_script(self.INPUT_EMOJI, element2, self.info[2])
                driver.execute_script(self.INPUT_EMOJI, element3, self.info[3])
                driver.execute_script(self.INPUT_EMOJI, element5, self.info[5])
                driver.execute_script(self.INPUT_EMOJI, element6, self.info[6])
                driver.execute_script(self.INPUT_EMOJI, element9, self.info[9])
                driver.execute_script(self.INPUT_EMOJI, element10,self.info[10])
                driver.execute_script(self.INPUT_EMOJI, element11,self.info[11])
                driver.execute_script(self.INPUT_EMOJI, element12,self.info[12])
                driver.execute_script(self.INPUT_EMOJI, element13,self.info[13])
                driver.execute_script(self.INPUT_EMOJI, element14,self.info[14])
                driver.execute_script(self.INPUT_EMOJI, element15,self.info[15])
                driver.execute_script(self.INPUT_EMOJI, element16,self.info[16])
                driver.execute_script(self.INPUT_EMOJI, element17,self.info[17])
                driver.execute_script(self.INPUT_EMOJI, element18,self.info[18])
                driver.execute_script(self.INPUT_EMOJI, element7, self.message)
                time.sleep(1)
                driver.find_element_by_xpath('//*[@id="top"]/div[3]/div/div[2]/div[2]/form/div/input').click()
                time.sleep(1)
                driver.find_element_by_xpath('//*[@id="top"]/div[3]/div/div[2]/div[2]/div[4]/form[2]/input[2]').click()
                time.sleep(1)

            except:
                print("town-failed")
                pass
            else:
                break

        driver.quit()
          
    def town_mail_signup(self):#完成
        driver = town.town_login()
        utilites.dget(driver, "https://admin.dto.jp/shop-admin/34627/diary-management/list")

        gal_list = driver.find_element_by_xpath('//*[@id="top"]/div[3]/div/div[2]/div[2]/div[3]/table/tbody')
        count = len(gal_list.find_elements_by_tag_name('tr'))
        print(count)
        for i in range(2,count+1):
            gal_name = driver.find_element_by_xpath(f'/html/body/div[3]/div/div[2]/div[2]/div[3]/table/tbody/tr[{i}]/td[1]/a')
            gal_name_text = gal_name.get_attribute("innerHTML")
            print(gal_name_text)
            if self.name == gal_name_text:
                driver.find_element_by_xpath(f'/html/body/div[3]/div/div[2]/div[2]/div[3]/table/tbody/tr[{i}]/td[3]/form/input').click()
                time.sleep(2)
                element_mail = driver.find_element_by_name('email')
                driver.execute_script(self.INPUT_EMOJI, element_mail, self.mail)
                driver.find_element_by_css_selector('#top > div.main_frame > div > div.shop_admin > div.shop_admin_body > div.shop_diary > form > div > input').click()
                break
        t_mail = driver.find_element_by_css_selector('#top > div.main_frame > div > div.shop_admin > div.shop_admin_body > div.shop_diary > div.com_message.style1 > div.com_size_large.com_margin_bottom > b').get_attribute("innerHTML")
        print(t_mail)
        driver.quit()
        return t_mail

    def ekichika_mail_signup(self):#完成
        driver = ekichika.ekichika_login()
        utilites.dget(driver, "https://ranking-deli.jp/admin/maildiary/notification/")
        time.sleep(2)
        gal_list = driver.find_element_by_xpath('//*[@id="girls-list-box"]')
        count = len(gal_list.find_elements_by_tag_name('li'))

        for i in range(1,count+1):
            e_gal_name = driver.find_element_by_xpath(f'/html/body/div[2]/div[4]/div[2]/ul/li[{i}]/a/div/p')
            e_gal_name_text = e_gal_name.get_attribute("innerHTML")
            print(e_gal_name_text)
            if self.name == e_gal_name_text:
                driver.execute_script("arguments[0].click();", e_gal_name)
                e_mail = driver.find_element_by_xpath('//*[@id="mao1"]/span[2]').get_attribute("innerHTML")
                break
        print(e_mail)
        driver.quit()
        return e_mail

    def delija_mail_signup(self):#完成
        driver = delija.delija_login()
        time.sleep(3)
        mail_manage = driver.find_element_by_css_selector('#wrapper > div > div.leftColumn > nav > div:nth-child(7) > div > ul > li:nth-child(1) > a')
        driver.execute_script("arguments[0].click();", mail_manage)
        d_gal_list = driver.find_element_by_xpath('//*[@id="girls"]/ul')
        count_d = len(d_gal_list.find_elements_by_tag_name('li')) 

        for i in range(1,count_d + 1):
            d_gal_name = driver.find_element_by_xpath(f'//*[@id="girls"]/ul/li[{i}]/a/div[1]')
            d_gal_name_text = d_gal_name.get_attribute("innerHTML")
            if self.name == d_gal_name_text:
                driver.find_element_by_xpath(f'//*[@id="girls"]/ul/li[{i}]/a').click()
                element = driver.find_element_by_xpath('//*[@id="form_diary_email"]')
                d_mail = element.get_attribute('value')
                break
        print(d_mail)
        driver.quit()
        return d_mail
    
    def fuja_mail_signup(self):#完成
        driver = fuja.fuja_login()
        time.sleep(3)
        mail_manage = driver.find_element_by_css_selector('#wrapper > div > div.leftColumn > nav > div:nth-child(7) > div > ul > li:nth-child(1) > a')
        driver.execute_script("arguments[0].click();", mail_manage)
        d_gal_list = driver.find_element_by_xpath('//*[@id="girls"]/ul')
        count_d = len(d_gal_list.find_elements_by_tag_name('li')) 

        for i in range(1,count_d + 1):
            d_gal_name = driver.find_element_by_xpath(f'//*[@id="girls"]/ul/li[{i}]/a/div[1]')
            d_gal_name_text = d_gal_name.get_attribute("innerHTML")
            if self.name == d_gal_name_text:
                driver.find_element_by_xpath(f'//*[@id="girls"]/ul/li[{i}]/a').click()
                element = driver.find_element_by_xpath('//*[@id="form_diary_email"]')
                f_mail = element.get_attribute('value')
                break
        print(f_mail)
        driver.quit()
        return f_mail

    def town_mail_cc(self,any_mail):#完成
        driver = town.town_login()
        utilites.dget(driver, "https://admin.dto.jp/shop-admin/34627/diary-management/list")

        gal_list = driver.find_element_by_xpath('//*[@id="top"]/div[3]/div/div[2]/div[2]/div[3]/table/tbody')
        count = len(gal_list.find_elements_by_tag_name('tr'))
        print(count)
        for i in range(2,count+1):
            gal_name = driver.find_element_by_xpath(f'/html/body/div[3]/div/div[2]/div[2]/div[3]/table/tbody/tr[{i}]/td[1]/a')
            gal_name_text = gal_name.get_attribute("innerHTML")
            if self.name == gal_name_text:
                print(gal_name_text)
                driver.find_element_by_xpath(f'/html/body/div[3]/div/div[2]/div[2]/div[3]/table/tbody/tr[{i}]/td[4]/a').click()
                time.sleep(5)
                handle_array = driver.window_handles
                driver.switch_to.window(handle_array[1])

                element_mail = driver.find_element_by_name('to_email')
                time.sleep(1)
                driver.execute_script(self.INPUT_EMOJI, element_mail, any_mail)
                time.sleep(1)
                driver.find_element_by_css_selector('#top > div.com_margin_bottom.regist > form > table > tbody > tr:nth-child(1) > td:nth-child(3) > input').click()
                time.sleep(1)
                break
        time.sleep(1)
        driver.quit()


    def summary(self):
        

        
        print(self.info[0] + "の作成が完了しました")
        
    