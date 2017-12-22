# coding=utf-8
"""
for py35
"""
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
import os
import time
import datetime
import sys
import pandas as pd
import numpy as np
import res_common_set as acs

# athomeサービスURLロード
HOME_PAGE_URL = acs.HOME_PAGE_URL
LOGIN_PAGE_URL = acs.LOGIN_PAGE_URL


# athomeログイン情報
ID = acs.ID
USER_ID = acs.USER_ID
PASSWORD = acs.PASSWORD

# ファイルpath情報
OPATH = acs.OPATH
UPDATE_T = acs.UPDATE_T
UPDATE_PATH_T = os.path.join(OPATH, UPDATE_T)
UPDATE_PATH_M = os.path.join(OPATH, 'testm.csv')
UPDATE_PATH_L = os.path.join(OPATH, 'testl.csv')
UPDATE_PATH_S = os.path.join(OPATH, 'tests.csv')

# ファイル形式情報
PRO_HEAD = acs.PRO_HEAD

# リンク、ボタンなど
SEC_TO_WAIT = acs.SEC_TO_WAIT
WAIT_COUNT = acs.WAIT_COUNT
news_id = acs.news_id


def click_btn(driver, attribute_name, value, trial_count):
    for i in range(trial_count):
        time.sleep(SEC_TO_WAIT)
        btns = [tag for tag in driver.find_elements_by_tag_name('input') if tag.get_attribute(attribute_name) == value]
        if len(btns) == 0:
            print('{i} waiting for {v} to be populated'.format(i=i, v=value))
        else:
            btns[0].click()
            return

def click_link(driver, link_title, trial_count):
    error = 0
    for i in range(trial_count):
        links = [tag for tag in driver.find_elements_by_xpath(link_title)]
        if len(links) == 0:
            print('{i} waiting for {t} to be populated'.format(i=i, t=link_title))
        else:
            error = 1
            links[0].click()
            print("data fetch ok")
    return (driver,error)


def login_page(driver):
    textbox = [tag for tag in driver.find_elements_by_tag_name('input') if tag.get_attribute('name') == 'LA0310Form01:LA0310Email'][0]
    textbox.send_keys(USER_ID)
    textbox = [tag for tag in driver.find_elements_by_tag_name('input') if tag.get_attribute('name') == 'LA0310Form01:LA0310Password'][0]
    textbox.send_keys(PASSWORD[USER_ID])
    click_btn(driver, 'name', u'LA0310Form01:j_id31', WAIT_COUNT)
    return driver


def login_page_access(driver,ID):
    for i in range(WAIT_COUNT):
        time.sleep(SEC_TO_WAIT)
        links = [tag for tag in driver.find_elements_by_xpath(ID)]
        print ("access login page")
        if len(links) == 0:
            print('{i} waiting for {t} to be populated'.format(i=i, t=link_title))
        else:
            links[0].click()
            return driver

def fetch_text(driver, news_id, SEC_TO_WAIT):
    for i in range(WAIT_COUNT):
        time.sleep(SEC_TO_WAIT)
        text_obj = driver.find_elements_by_xpath(news_id)
        if text_obj is not None and len(text_obj) > 0:
            text = text_obj[0].text
        else:
            print('{i} waiting for {t} to be populated'.format(i=i, t=news_id))
        #for rowc in text:
        #    text_list.append(rowc.text)
        #    print(text_list)
    return (driver,text)


def main():
    today = datetime.date.today()
    print (today)
    # BP起動
    driver = webdriver.Chrome()
    driver.get(HOME_PAGE_URL)
    # データフォーマット作成
    df_text = pd.DataFrame(columns=[PRO_HEAD])

    # PBログインページ
    driver = login_page_access(driver,ID)

    # PBログイン
    driver = login_page(driver)
    # 少し待つ
    time.sleep(SEC_TO_WAIT)

    # ホームに戻り、最新記事確認
    main_text = list()
    list_text = list()
    sub_text = list()

    # ホームに戻り、最新記事確認
    main_num = len(driver.find_elements(By.XPATH,'//*[@id="mainContent"]/section[1]//section[@class="pickup-nfm"]'))#主要記事数
    li_num = len(driver.find_elements(By.XPATH,'//*[@id="mainContent"]/section[1]//ul[@class="list-type1"]//p[@class="shoulder"]'))#リスト記事数
    print(main_num)
    print(li_num)


    for i in range(main_num):#主要記事
        print("subtext")
        news_m = '//*[@id="mainContent"]/section[1]/section[{}]/a/h3'.format(i+1)
        print(news_m)
        link_result_m = click_link(driver, news_m, SEC_TO_WAIT)
        if link_result_m[1] == 1:
            print("m result ok")
            fetch_result_m = fetch_text(link_result_m[0], news_id, SEC_TO_WAIT)
            driver = fetch_result_m[0]
            text_data_m = fetch_result_m[1]
            main_text.append(text_data_m)
            driver.back()
            rel_link = '//*[@id="mainContent"]/section[1]/section[{}]//div[@class="topRelatedLinkBox"]//em[@class="icon auth"]'.format(i+1)
            rela_num = len(driver.find_elements(By.XPATH,rel_link))
            print(rela_num)
            if rela_num > 0:
                for j in range(rela_num):
                    news_s = '//*[@id="mainContent"]/section[1]/section[{}]/div/ul/li[{}]/a'.format(i+1,j+1)
                    link_result_s = click_link(driver, news_s, SEC_TO_WAIT)
                    if link_result_s[1] == 1:
                        fetch_result_s = fetch_text(link_result_m[0], news_id, SEC_TO_WAIT)
                        driver = fetch_result_s[0]
                        text_data_s = fetch_result_s[1]
                        sub_text.append(text_data_s)
                        driver.back()

    for k in range(li_num):#リスト記事
        print("subtext")
        news_l = '//*[@id="mainContent"]/section[1]/ul/li[{}]/a'.format(k + 1)
        link_result_l = click_link(driver, news_l, SEC_TO_WAIT)
        if link_result_l[1] == 1:
            fetch_result_l = fetch_text(link_result_m[0], news_id, SEC_TO_WAIT)
            driver = fetch_result_l[0]
            text_data_l = fetch_result_l[1]
            list_text.append(text_data_l)
            driver.back()
            l_rel_link = '//*[@id="mainContent"]/section[1]/ul/li[{}]//div[@class="topRelatedLinkBox"]//em[@class="icon auth"]'.format(k + 1)
            print(l_rel_link)
            l_rela_num = len(driver.find_elements(By.XPATH, l_rel_link))
            print(l_rela_num)
            if l_rela_num > 0:
                for q in range(l_rela_num):
                    print("l sub")
                    news_s = '//*[@id="mainContent"]/section[1]/ul/li[{}]/div/ul/li[{}]/a'.format(k+1,q+1)
                    link_result_s = click_link(driver, news_s, SEC_TO_WAIT)
                    fetch_result_s = fetch_text(link_result_m[0], news_id, SEC_TO_WAIT)
                    if link_result_s[1] == 1:
                        driver = fetch_result_s[0]
                        text_data_s = fetch_result_s[1]
                        sub_text.append(text_data_s)
                        driver.back()

    driver.quit()

    #ここではテキストをマージすることもＯＫ
    df_text_m = pd.DataFrame({'Body':main_text})
    df_text_m.to_csv(UPDATE_PATH_M,index=False)
    df_text_l = pd.DataFrame({'Body':list_text})
    df_text_l.to_csv(UPDATE_PATH_L,index=False)
    df_text_s = pd.DataFrame({'Body':sub_text})
    df_text_s.to_csv(UPDATE_PATH_S,index=False)
    df_text_t = df_text_m.append(df_text_l, ignore_index=True).append(df_text_s, ignore_index=True)
    df_text_t.to_csv(UPDATE_PATH_T,index=False)

if __name__ == '__main__':
    main()