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

def heaven_login(headless=True):
    options = Options()
    if headless:
        options.add_argument('--headless')  # ヘッドレスモード

    driver = webdriver.Chrome(options=options)   #(※２）
    driver.implicitly_wait(10)
    url = "https://newmanager.cityheaven.net"
    utilites.dget(driver, url)
    n = random.randint(1, 5)
    time.sleep(n)
    # browser.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    try:
        heaven_id = driver.find_element_by_css_selector("td > #id")
        heaven_pass = driver.find_element_by_css_selector("td > #pass")    
        heaven_id.click()
        heaven_id.send_keys("2510021932")
        heaven_pass.click()
        heaven_pass.send_keys("i7Qt5Jnj")    
        driver.find_element_by_css_selector(".oldLogin > table > tbody > tr:nth-child(2) > td").click()
        driver.find_element_by_css_selector("td img").click()
        time.sleep(3)
        driver.find_element_by_class_xpath('//*[@id="header_wrapper"]/div[2]/div[2]/a[1]').click()
        time.sleep(5)
    except:
        pass
    return driver





def login(self, username: str, password: str, headless: bool = True) -> webdriver.Chrome:
    """
    ログインを実行する

    Args:
        username (str): ユーザー名
        password (str): パスワード
        headless (bool): ヘッドレスモードで実行するかどうか

    Returns:
        webdriver.Chrome: ログイン済みのWebDriverインスタンス

    Raises:
        TimeoutException: ログインフォームの要素が見つからない場合
        ElementClickInterceptedException: クリック操作が妨げられた場合
        StaleElementReferenceException: 要素が古くなった場合
    """
    self.driver = self.setup_driver(headless=headless)
    wait = WebDriverWait(self.driver, 10)  # 待機時間を10秒に調整

    try:
        # ページにアクセス
        self.driver.get(self.config.url)

        # oldLoginクラスのフォームを待機
        form = wait.until(
            EC.presence_of_element_located((By.CLASS_NAME, "oldLogin"))
        )
        wait.until(EC.visibility_of(form))

        # ユーザー名フィールドが操作可能になるまで待機
        username_element = wait.until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, ".oldLogin input[name='txt_account']"))
        )
        wait.until(EC.visibility_of(username_element))
        self.driver.execute_script("arguments[0].value = arguments[1]", username_element, username)

        # パスワードフィールドが操作可能になるまで待機
        password_element = wait.until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, ".oldLogin input[name='txt_password']"))
        )
        wait.until(EC.visibility_of(password_element))
        self.driver.execute_script("arguments[0].value = arguments[1]", password_element, password)

        # 送信ボタンがある場合はクリック
        if self.config.submit_button:
            submit_element = wait.until(
                EC.element_to_be_clickable((By.NAME, self.config.submit_button))
            )
            wait.until(EC.visibility_of(submit_element))
            submit_element.click()
        else:
            # 送信ボタンがない場合はフォームを送信
            password_element.submit()

        # DOMの遷移完了を待機
        wait.until(EC.staleness_of(password_element))

        # ページの読み込みを待機
        wait.until(lambda driver: driver.current_url != self.config.url)

        return self.driver

    except (TimeoutException, ElementClickInterceptedException, NoSuchElementException, ElementNotInteractableException) as e:
        if self.driver:
            self.driver.quit()
        raise e
    except Exception as e:
        if self.driver:
            self.driver.quit()
        raise Exception(str(e)) 
























def pdeco_login(gal,id,ps):
    options = Options()
    #options.add_argument('--headless')   #ヘッドレスモード
    options.add_argument('--incognito')  #シークレットモード
    options.add_experimental_option("detach", True)
    driver = webdriver.Chrome(options=options)   #(※２）
    driver.implicitly_wait(10)
    url = "https://spgirl.cityheaven.net"
    utilites.dget(driver, url)
    
    driver.find_element_by_id("userid").send_keys(id)
    driver.find_element_by_id("passwd").send_keys(ps)
    driver.execute_script("arguments[0].click();", driver.find_element_by_xpath('//*[@id="loginBtn"]'))

    return driver

def heaven_update():

    driver = heaven_login()
    n = random.randint(1, 5)
    time.sleep(n)
    driver.execute_script("arguments[0].click();", driver.find_element_by_xpath('//*[@id="cntButton"]/div[1]'))
    time.sleep(n)
    try:
        assert driver.switch_to.alert.text == "お店ページの更新日時を更新しますか？"
        driver.switch_to.alert.accept()
    except:
        pass
    driver.execute_script("arguments[0].click();", driver.find_element_by_xpath('//*[@id="cntButtonGirls"]/div[1]'))
    time.sleep(n)
    try:
        assert driver.switch_to.alert.text == "ガールズヘブンのお店ページ更新日時を更新しますか？"
        driver.switch_to.alert.accept()
    except:
        pass
    time.sleep(n + 2)
    driver.quit()


def get_gals_info():
    driver = heaven_login(False)
    time.sleep(2)
    for l in range(5):
        try:
            utilites.dget(driver, 'https://newmanager.cityheaven.net/C8GirlMyPageRegist.php?member_id=57542771')
            gal_list = driver.find_element_by_xpath('//*[@id="form_container"]/div/ul')
            count = len(gal_list.find_elements_by_tag_name('li'))
        except:
            driver.refresh()
            time.sleep(5)
            pass
        else:
            break
    
    gals_cont = []
    gals_cont.append(count)

    for i in range(1,count+1):
        driver.refresh()
        for l in range(5):
            try:
                gal_name = driver.find_element_by_xpath(f'//*[@id="form_container"]/div/ul/li[{i}]/div[2]/a')
                gal_name_text = gal_name.get_attribute("innerHTML")
                driver.execute_script("arguments[0].click();", gal_name)
                ipass = driver.find_element_by_xpath('//*[@id="form_container"]/table/tbody/tr/td[2]/table/tbody/tr[2]/td/div')
            except:
                driver.refresh()
                time.sleep(5)
                pass
            else:
                break
        
        txt = driver.find_element_by_xpath('//*[@id="form_container"]/table/tbody/tr/td[2]/table/tbody/tr[1]/td/table/tbody/tr[1]/td').text
        if txt == "未登録":
            continue
        print(str(i) + gal_name_text + ipass.get_attribute("innerHTML").strip())

        ss = ipass.get_attribute("innerHTML").split('　')
        ssid = ss[0].split('：')
        ssps = ss[1].split('：')
        
        gal_info = [gal_name_text,ssid[1],ssps[1].strip()]
        print(gal_info)
        gals_cont.append(gal_info)

        driver.back()
    driver.quit()
    return(gals_cont)

def get_target_gal_info(name_list):
    def get_gal_info(driver, gal_name, gal_name_text):
        driver.execute_script("arguments[0].click();", gal_name)
        
        ipass = driver.find_element_by_xpath('//*[@id="form_container"]/table/tbody/tr/td[2]/table/tbody/tr[2]/td/div')
        ss = ipass.get_attribute("innerHTML").split('　')
        ssid = ss[0].split('：')
        ssps = ss[1].split('：')
        gal_info = [gal_name_text, ssid[1].strip(), ssps[1].strip()]

        driver.back()

        # ページが戻るまで待機（ulが再表示されるまで待つ）
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, '//*[@id="form_container"]/div/ul'))
        )
        return gal_info

    driver = heaven_login()
    utilites.dget(driver, 'https://newmanager.cityheaven.net/C8GirlMyPageRegist.php?member_id=57542771')
    gal_list = driver.find_element_by_xpath('//*[@id="form_container"]/div/ul')
    count = len(gal_list.find_elements_by_tag_name('li'))

    gals_cont = []

    for i in range(1, count + 1):
        gal_name = driver.find_element_by_xpath(f'//*[@id="form_container"]/div/ul/li[{i}]/div[2]/a')
        gal_name_text = gal_name.get_attribute("innerHTML").strip()

        if isinstance(name_list, str):
            if gal_name_text == name_list:
                return get_gal_info(driver, gal_name, gal_name_text)

        elif isinstance(name_list, list):
            for name in name_list:
                if gal_name_text == name:
                    g_info = get_gal_info(driver, gal_name, gal_name_text)
                    gals_cont.append(g_info)
                    break  # 同名で複数マッチしても1人だけ取得
    print(gals_cont)
    return gals_cont

def heaven_kitene2(gal,id,ps):
    options = webdriver.ChromeOptions()
    #options.add_argument("--headless")
    options.add_argument('--incognito')
    options.add_argument('--disable-dev-shm-usage')
    options.add_argument("--no-sandbox")
    options = Options()

    driver = webdriver.Chrome(options=options)   #(※２）
    driver.implicitly_wait(30)
    url = "https://spgirl.cityheaven.net"
    utilites.dget(driver, url)

    for l in range(5):
        try:
            driver.find_element(By.ID,"userid").send_keys(id)
            driver.find_element(By.ID,"passwd").send_keys(ps)
            driver.execute_script("arguments[0].click();", driver.find_element(By.XPATH,'//*[@id="loginBtn"]'))
        except:
            driver.refresh()
            time.sleep(5)
            pass
        else:
            break
    

    time.sleep(2)
    driver.execute_script("window.scrollTo(0, 2500);")
    time.sleep(2)
    try:
        driver.find_element(By.CSS_SELECTOR,".jqmOverlay").click()
    except Exception:
        driver.refresh()
        pass

    for l in range(5):
        try:
            driver.execute_script("arguments[0].click();", driver.find_element(By.XPATH,'//*[@id="home"]/article/section[2]/ul/div/li/a/div/span[1]'))
        except:
            driver.refresh()
            time.sleep(5)
            pass
        else:
            break
    for l in range(5):
        try:
            driver.execute_script("arguments[0].click();", driver.find_element(By.XPATH,'/html/body/main/div[2]/div/ul/li[5]/a'))
        except:
            driver.refresh()
            time.sleep(5)
            pass
        else:
            break
    driver.refresh()
    s = 0
    f = 0

    for l in range(5):
        try:
            elements = driver.find_elements(By.CLASS_NAME,"kitene_point")
        except:
            driver.refresh()
        else:
            break
    kitene_count = 0
    for element in elements:
        text = element.text
        if "残り回数" in text:
            kitene_count = int(text.split("：")[1].split("/")[0])
            #print(gal,"残り回数:", kitene_count)
            time.sleep(5)
        elif "本日はキテネを使い切りました" in text:
            #print("キテネ済み")
            kitene_count = "本日はキテネを使い切りました"
            driver.quit()
            return "done"
        else:
            print("条件に該当するテキストが見つかりませんでした")

    for k in range(1,30):
        if kitene_count == "本日はキテネを使い切りました":
            driver.quit()
            return "done"
            break
        n = random.uniform(2, 5)
        time.sleep(1+n)
        for l in range(5):
            try:
                wait = WebDriverWait(driver, 10)
                element = wait.until(EC.presence_of_element_located((By.XPATH,f'//*[@id="reviewtabContents"]/ul/li[{k}]/a/div[2]/div[1]/object/a/span')))
                driver.execute_script("arguments[0].click();",driver.find_element(By.XPATH,f'//*[@id="reviewtabContents"]/ul/li[{k}]/a/div[2]/div[1]/object/a/span'))
                n2 = random.uniform(2, 3)
                time.sleep(n2)
                Alert(driver).accept()
            except:
                time.sleep(n)
                driver.refresh()
                f += 1
                if f == 10:
                    driver.quit()
                    return "retry"
            else:
                s += 1
                break
        if s == kitene_count:
            break
        time.sleep(n)
    time.sleep(3)
    driver.quit()
    return "done"

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
    
def get_heaven_schedule():
    import blog_db
    
    success_count = 0
    total_gals = 0
    
    for k in range(3):
        try:
            driver  = heaven_login()
            utilites.dget(driver, 'https://newmanager.cityheaven.net/C9ShukkinShiftList.php?shopdir=cb_mbsentai')
            Select(driver.find_element_by_xpath('//*[@id="list_cnt"]')).select_by_visible_text("全件表示")
            schedule_table = driver.find_element_by_xpath('//*[@id="shukkinShiftTable"]/tbody')
            row_count = len(schedule_table.find_elements_by_tag_name('tr'))
            title_count = len(schedule_table.find_elements_by_class_name('title'))
            gals_count = row_count - title_count
            print(f"取得したガール数: {gals_count}")
            total_gals = gals_count
            
            j = 0
            for i in range(3, gals_count + 3): 
                j += 1
                gal_elm = schedule_table.find_element_by_xpath(f'tr[{i}]')
                if j % 11 == 0:
                    continue     
                
                gal_name = gal_elm.find_element_by_xpath(f'td[1]/a').text.split("\n")[0]
                print(f"ガール名: {gal_name}")
                
                # スケジュールデータを取得
                schedule_data = []
                for l in range(2, 9):
                    day_elm = gal_elm.find_element_by_xpath(f'td[{l}]')
                    start_value = day_elm.find_element_by_xpath('input[7]').get_attribute('value')
                    end_value = day_elm.find_element_by_xpath('input[8]').get_attribute('value')
                    schedule_data.append([utilites.format_time(start_value), utilites.format_time(end_value)])
                
                # DBに保存
                if blog_db.add_heaven_schedule(gal_name, schedule_data):
                    success_count += 1
                    print(f"✓ {gal_name}のスケジュールを保存しました")
                else:
                    print(f"✗ {gal_name}のスケジュール保存に失敗しました")
                    
        except Exception as e:
            print(f"エラーが発生しました: {e}")
            pass
        else:
            break
    
    driver.quit()
    
    print(f"スケジュール取得完了: {success_count}/{total_gals} 件保存")
    return {
        'success': True,
        'saved_count': success_count,
        'total_count': total_gals,
        'message': f"{success_count}/{total_gals} 件のスケジュールを保存しました"
    }

def okini_talk_auto(name, message):

    def navigate_talk(driver):
        time.sleep(2)
        driver.execute_script("window.scrollTo(0, 2500);")
        time.sleep(2)
        try:
            driver.find_element(By.CSS_SELECTOR,".jqmOverlay").click()
        except Exception:
            driver.refresh()
            pass
        driver.execute_script("arguments[0].click();", driver.find_element_by_xpath('//*[@id="fixedMenu"]/nav/ul/li[2]/a'))
        time.sleep(2)

        return driver

    def send_templete_message(driver, message):
        INPUT_EMOJI = """
                        arguments[0].value += arguments[1];
                        arguments[0].dispatchEvent(new Event('input', { bubbles: true }));
                        arguments[0].dispatchEvent(new Event('change', { bubbles: true }));
                    """
        try:
            talk_box = driver.find_element_by_name('talk_editor_box')
            talk_box.click()
            print("1")
            time.sleep(utilites.get_random_delay(0, (0, 0), (1, 2)).total_seconds())

            # 絵文字などを含むメッセージを入力（input イベントを発火させる）
            driver.execute_script(INPUT_EMOJI, talk_box, message)
            print("2")
            time.sleep(utilites.get_random_delay(0, (0, 0), (1, 3)).total_seconds())

            # 送信ボタンをクリック
            submit_button = driver.find_element_by_class_name('te_submit')
            driver.execute_script("arguments[0].click();", submit_button)
            print("3")

            time.sleep(0.2)
        except Exception as e:
            print(f"error: {e}")

    def is_within_three_months(reply_element) -> bool:
        """
        reply_element: SeleniumのWebElement（data-create_date属性を持つ）
        3ヶ月以内ならTrue、それより前ならFalseを返す
        """
        create_date_str = reply_element.get_attribute('data-create_date')
        if not create_date_str:
            print("日付属性が取得できませんでした。")
            return False

        try:
            # "2025/04/06 01:05:28" 形式に合わせて変換
            create_date = datetime.strptime(create_date_str, "%Y/%m/%d %H:%M:%S")
        except ValueError:
            print(f"日付の形式が不正です: {create_date_str}")
            return False

        today = datetime.now()
        three_months_ago = today - relativedelta(months=3)

        return create_date >= three_months_ago

    try:
        kg_target = get_target_gal_info(name)
        driver = pdeco_login(kg_target[0],kg_target[1],kg_target[2])
        navigate_talk(driver)

        counter_text = driver.find_element_by_class_name('counter').text
        match = re.search(r'全(\d+)人', counter_text)
        if match:
            total_people = int(match.group(1))
            print(total_people)
            num_loops = (total_people + 30 - 1) // 30  # 切り上げてループ回数を計算
            for j in range(num_loops):
                print(f"{j+1}回目のループ（表示人数: {j * 30 + 1}〜{min((j + 1) * 30, total_people)}人）")
                # ここに処理を入れる（例えば、ページネーションの処理など）  
                talk_box = driver.find_element_by_class_name('talk_box')
                count = len(talk_box.find_elements_by_class_name('list'))
                print(count)
                for i in range(1, count + 1):
                    talk_box = driver.find_element_by_class_name('talk_box')
                    target_user = talk_box.find_element_by_xpath(f'li[{i}]')
                    driver.execute_script("arguments[0].click();", target_user.find_element_by_class_name('link_user'))
                    driver.implicitly_wait(0) 
                    time.sleep(1)
                    user_name = driver.find_element_by_class_name('head_name').text
                    talk_main = driver.find_element_by_class_name('tb_main')

                    try:
                        replys = WebDriverWait(driver, 3).until(EC.presence_of_all_elements_located((By.CLASS_NAME, 'tb_left')))
                    except TimeoutException:
                        replys = []
                    try:
                        submiteds = WebDriverWait(driver, 3).until(EC.presence_of_all_elements_located((By.CLASS_NAME, 'tb_right')))
                    except TimeoutException:
                        submiteds = []
                    print(i, user_name, len(replys), len(submiteds))
                    
                    if replys or submiteds:
                        last_reply = replys[-1] if replys else None
                        last_submit = submiteds[-1] if submiteds else None

                        reply_recent = is_within_three_months(last_reply) if last_reply else False
                        submit_recent = is_within_three_months(last_submit) if last_submit else False

                        if not reply_recent and not submit_recent:
                            print("送信済みメッセージ、返信共に3ヶ月以上前のため送信")
                            send_templete_message(driver, message)
                    else:
                        print("返信が見つかりませんでした。問答無用で送信")
                        send_templete_message(driver, message)
                    driver.back()
                    driver.refresh()
                    driver.implicitly_wait(10)
                driver.execute_script("arguments[0].click();", driver.find_element_by_id('pagenext'))
        else:
            print("数値が見つかりませんでした。")         
    finally:
        driver.quit()


if __name__=="__main__":
    heaven_login()
    heaven_update()
    heaven_kitene2()
    pdeco_create()
    
