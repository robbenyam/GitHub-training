# coding=utf-8
"""
for py35
"""
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.keys import Keys
import os
import time
import datetime
import sys
import pandas as pd
import numpy as np
import athome_common_set as acs

# athomeサービスURLロード
HOME_PAGE_URL = acs.HOME_PAGE_URL
ALERT_PAGE_URL = acs.ALERT_PAGE_URL
SEARCH_URL = acs.SEARCH_URL
IMAG_URL = acs.IMAG_URL

# athomeログイン情報
USER_ID = acs.USER_ID
PASSWORD = acs.PASSWORD

# ファイルpath情報
OPATH = os.path.dirname(os.path.abspath(__name__))
UPDATE = acs.UPDATE
UPDATE_PATH = os.path.join(OPATH, UPDATE)

# ファイル形式情報
PRO_HEAD = acs.PRO_HEAD

# リンク、ボタンなど
SEC_TO_WAIT = acs.SEC_TO_WAIT
WAIT_COUNT = acs.WAIT_COUNT
SEARCH_CONDITIONS = acs.SEARCH_CONDITIONS
rbtn = acs.AT_HOME_BTN
SCROLL_PAUSE_TIME = 3
Pro_NO_LIM = 11


def click_btn(driver, attribute_name, value, trial_count):
    for i in range(trial_count):
        time.sleep(SEC_TO_WAIT)
        print ("click_btn")
        btns = [tag for tag in driver.find_elements_by_tag_name('input') if tag.get_attribute(attribute_name) == value]
        print ("click_btn_over")
        if len(btns) == 0:
            print('{i} waiting for {v} to be populated'.format(i=i, v=value))
        else:
            btns[0].click()
            return


def click_link(driver, link_title, trial_count):
    for i in range(trial_count):
        links = [tag for tag in driver.find_elements_by_link_text(link_title)]
        if len(links) == 0:
            print('{i} waiting for {t} to be populated'.format(i=i, t=link_title))
        else:
            links[0].click()
            return


def click_num(driver, link_title, trial_count):
    for i in range(trial_count):
        time.sleep(SEC_TO_WAIT)
        textbox = [tag for tag in driver.find_elements_by_xpath(link_title)]
        if len(textbox) == 0:
            print('{i} waiting for {t} to be populated'.format(i=i, t=link_title))
        else:
            for j in range(trial_count):
                time.sleep(SEC_TO_WAIT)
                value = textbox[0].find_elements_by_css_selector('input')
                if len(value) > 0:
                    num = value[0].get_attribute('value')
                    print (num)
                    textbox[0].click()
                    return[driver,num]


def login_page(driver):
    textbox = [tag for tag in driver.find_elements_by_tag_name('input') if tag.get_attribute('name') == 'loginId'][0]
    textbox.send_keys(USER_ID)
    textbox = [tag for tag in driver.find_elements_by_tag_name('input') if tag.get_attribute('name') == 'password'][0]
    textbox.send_keys(PASSWORD[USER_ID])
    click_btn(driver, 'value', u'ログイン', WAIT_COUNT)
    return driver


def search(driver, rbtn,trial_count):
    click_link(driver, rbtn, WAIT_COUNT)
    # 流通物件検索（保存した条件）をクリックしてページ遷移
    for i in range(trial_count):
        print ('物件検索')
        time.sleep(SEC_TO_WAIT)
        textbox = [tag for tag in driver.find_elements_by_tag_name('div') if tag.get_attribute('data-action') == SEARCH_URL[0]]
        if len(textbox) == 0:
            print('{i} waiting for {t} to be populated'.format(i=i, t=rbtn))
        else:
            textbox[0].click()
            return driver


def kick_page(driver):
    click_btn(driver, 'value', u'強制ログアウト', WAIT_COUNT)
    time.sleep(SEC_TO_WAIT)
    print("kick_ass_1")
    alert = driver.switch_to_alert()
    print("kick_ass_2")
    print(alert)
    alert.accept()
    print("kick_ass_3")
    return driver


def page_scroll(driver,id):
    print ('scroll down page')
    print (id)
    last_height = driver.execute_script("return document.body.scrollHeight")
    if (id == 0) | (id == 1) | (id == 2) | (id == 3):
        GAP = last_height / 5
    elif (id == 4) | (id == 5):
        GAP = last_height / 4
    elif (id == 6) | (id == 7):
        GAP = last_height / 3
    elif (id == 8) | (id == 9):
        GAP = last_height / 2
    elif (id == 10):
        GAP = last_height / 2
    elif (id == 11):
        GAP = last_height / 1.5
    ##検索条件の修正が発生した場合、こちらに追加
    elif (id == 12) | (id == 13):
        GAP = last_height / 1.5
    driver.execute_script("window.scrollTo(0,{});".format(GAP))
    return driver



def main():
    today = datetime.date.today()
    print (today)
    # at home起動
    #driver = webdriver.Chrome()
    driver = webdriver.PhantomJS()
    driver.get(HOME_PAGE_URL)
    # データフォーマット作成
    df_pro = pd.DataFrame(columns=[PRO_HEAD])
    df_pro_temp = pd.DataFrame(columns=[PRO_HEAD])

    # at homeログイン
    driver = login_page(driver)
    print("loginok")
    # at home検索画面アクセス
    driver = search(driver, rbtn, WAIT_COUNT)
    driver.switch_to.window(driver.window_handles[-1])
    # 初登録する際に、本処理はいらないため、初登録の確認を事前に行う必要がある
    if driver.current_url == ALERT_PAGE_URL:
        print("kickass")
        driver = kick_page(driver)
        print("kickass_ok")
    time.sleep(SEC_TO_WAIT)
    temp_url = driver.current_url
    print (temp_url)

    # 保存上件数確認
    CON_URL = '/html/body/table/tbody/tr[3]/td/table/tbody/tr[1]/td[3]/form[27]/table[2]/tbody/tr/td[1]/span[3]'
    search_con = driver.find_elements_by_xpath(CON_URL)
    con_list = list()
    for rowc in search_con:
        print(rowc)
        con_list.append(rowc.text)
    SEARCH_CONDITIONS = int(con_list[0])

    # 検索結果からデータを抽出
    for id in range(SEARCH_CONDITIONS):#SEARCH_CONDITIONS
        driver.get(temp_url)
        df_pro_temp = pd.DataFrame(columns=[PRO_HEAD])
        link_num = '//*[@id="gaitoSuAfterShiteibi[{}]"]/a'.format(id)
        print (link_num)
        page_scroll(driver,id)
        values = click_num(driver, link_num, WAIT_COUNT)
        driver = values[0]
        driver_num = int(values[1])
        print (driver_num)
        #データテーブルを保存する
        if driver_num > 0:
            i = 0
            for count in range(driver_num):
                cont_list = list()
                PRO_URL = '//div[contains(@class,"bukkenKensakuKekkaWrapper")]/table[{}]/tbody/tr/td'.format(count+1)
                print (PRO_URL)
                # 物件のデータを抽出
                table_cont = driver.find_elements_by_xpath(PRO_URL)
                for rowc in table_cont:
                    cont_list.append(rowc.text)
                cont_list = cont_list[:-1]
                df_pro_temp.loc[i] = np.array(cont_list)
                i += 1
        else:
            print ('no update today')
        print ('loop over')
        df_pro = pd.concat([df_pro,df_pro_temp])
        print (df_pro)
    df_pro[u'物件番号'] = df_pro[u'物件番号'].astype(str).str.zfill(Pro_NO_LIM)
    df_pro.to_csv(UPDATE_PATH,index=False)
    driver.quit()


if __name__ == '__main__':
    main()

