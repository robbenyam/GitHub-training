# coding=utf-8
"""
for py35
"""
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver import ActionChains
from selenium.webdriver.common.keys import Keys
import pandas as pd
import os
import shutil
import tempfile
import time
import datetime
import sys
import athome_common_set as acs

#athomeサービスURLロード
HOME_PAGE_URL = acs.HOME_PAGE_URL
ALERT_PAGE_URL = acs.ALERT_PAGE_URL
SEARCH_URL = acs.SEARCH_URL
IMAG_URL = acs.IMAG_URL
PRO_URL = acs.PRO_URL
PDF_URL = acs.PDF_URL

USER_ID = acs.USER_ID
PASSWORD = acs.PASSWORD
SEC_TO_WAIT = acs.SEC_TO_WAIT
WAIT_COUNT = acs.WAIT_COUNT

OPATH = acs.OPATH
OPATH_PDF = acs.OPATH_PDF
UPDATE = acs.UPDATE
PDF = acs.PDF
UPDATE_PATH = os.path.join(OPATH, UPDATE)
PDF_PATH = os.path.join(OPATH_PDF, PDF)

rbtn = acs.AT_HOME_BTN
P_NO_COL = acs.P_NO_COL

def load_master_data(path):
    if os.path.exists(path):
        df = pd.read_csv(path, encoding='cp932')
        return df.reset_index(drop=True)
    else:
        sys.exit("file is not existed")

def click_btn(driver, attribute_name, value, trial_count):
    print ("click_btn方法")
    for i in range(trial_count):
        time.sleep(SEC_TO_WAIT)
        btns = [tag for tag in driver.find_elements_by_tag_name('input') if tag.get_attribute(attribute_name) == value]
        if len(btns) == 0:
            print('{i} waiting for {v} to be populated'.format(i=i, v=value))
            time.sleep(SEC_TO_WAIT)
        else:
            btns[0].click()
            return

def click_link(driver, link_title, trial_count):
    print ("click_link方法")
    for i in range(trial_count):
        time.sleep(SEC_TO_WAIT)
        links = [tag for tag in driver.find_elements_by_link_text(link_title)]
        if len(links) == 0:
            print('{i} waiting for {t} to be populated'.format(i=i, t=link_title))
            time.sleep(SEC_TO_WAIT)
        else:
            links[0].click()
            return


def click_css(driver, link_title, trial_count):
    print ("click_css方法")
    for i in range(trial_count):
        time.sleep(SEC_TO_WAIT)
        imgs = [tag for tag in driver.find_elements_by_xpath(link_title)]
        if len(imgs) == 0:
            print('{i} waiting for {t} to be populated'.format(i=i, t=link_title))
            time.sleep(SEC_TO_WAIT)
        else:
            imgs[0].click()
            return


def click_text(driver, link_title, trial_count):
    print ("click_text方法")
    for i in range(trial_count):
        time.sleep(SEC_TO_WAIT)
        texts = [tag for tag in driver.find_elements_by_xpath('//a[contains(text(),"%s")]' % link_title)]
        if len(texts) == 0:
            print ("物件番号入力間違い")
            print (link_title)
            error = True
            return [driver,error]
        else:
            texts[0].click()
            error = False
            return [driver,error]


def login_page(driver):
    textbox = [tag for tag in driver.find_elements_by_tag_name('input') if tag.get_attribute('name') == 'loginId'][0]
    textbox.send_keys(USER_ID)
    textbox = [tag for tag in driver.find_elements_by_tag_name('input') if tag.get_attribute('name') == 'password'][0]
    textbox.send_keys(PASSWORD[USER_ID])
    click_btn(driver, 'value', u'ログイン', WAIT_COUNT)
    return driver


def search(driver, rbtn, trial_count):
    click_link(driver, rbtn, WAIT_COUNT)
    # 流通物件検索（保存した条件）をクリックしてページ遷移
    for i in range(trial_count):
        print ('物件検索')
        time.sleep(SEC_TO_WAIT)
        textbox = [tag for tag in driver.find_elements_by_tag_name('div') if tag.get_attribute('data-action') == SEARCH_URL[1]]
        if len(textbox) == 0:
            print('{i} waiting for {t} to be populated'.format(i=i, t=rbtn))
        else:
            textbox[0].click()
            return driver


def search_no(driver):
    print ("search_no方法")
    click_css(driver, IMAG_URL, WAIT_COUNT)
    # 流通物件検索（保存した条件）をクリックしてページ遷移
    # driver.find_element_by_css_selector(u'物件番号検索').click()
    return driver


def kick_page(driver):
    print ("kick_start")
    time.sleep(SEC_TO_WAIT)
    driver.switch_to.window(driver.window_handles[-1])
    click_btn(driver, 'value', u'強制ログアウト', WAIT_COUNT)
    time.sleep(SEC_TO_WAIT)
    alert = driver.switch_to_alert()
    alert.accept()
    return driver

def property_info(driver):
    print ("property info")
    click_btn(driver, 'value', u'インフォシート', WAIT_COUNT)
    return driver

def property_pdf_for(driver,name):
    print ("pdf for")
    time.sleep(8)
    driver.switch_to.window(driver.window_handles[-1])
    click_css(driver, '//*[@id = "button-pdf-format"]', WAIT_COUNT)
    time.sleep(SEC_TO_WAIT)
    if os.path.isfile(PDF_PATH):
        rename(name)
    return driver


def rename(name):
    name = str(name)
    print (name)
    pdf_path_d =  os.path.join(OPATH_PDF,'{}.pdf'.format(name))
    print (pdf_path_d)
    shutil.move(PDF_PATH,pdf_path_d)
    return


def main():
    today = datetime.date.today()
    # 物件リストを導入
    print (UPDATE_PATH)
    df = load_master_data(UPDATE_PATH)
    df_p = set(df[P_NO_COL].copy().tolist())
    print (df_p)
    # at home起動
    options = webdriver.ChromeOptions()
    options.add_experimental_option("prefs", {
        "download.default_directory": OPATH_PDF,
        "download.prompt_for_download": False,
        "download.directory_upgrade": True,
        "plugins.plugins_disabled": ["Chrome PDF Viewer"],
        "plugins.always_open_pdf_externally": True
    })
    options.add_argument("--disable-extensions")
    options.add_argument("--disable-print-preview")
    driver = webdriver.Chrome(chrome_options=options)
    driver.get(HOME_PAGE_URL)
    print ("login")
    driver = login_page(driver)
    print ("search画面")
    driver = search(driver,rbtn,WAIT_COUNT)
    driver.switch_to.window(driver.window_handles[-1])
    if driver.current_url == ALERT_PAGE_URL:
        print ("kick out") #初登録する際に、本処理はいらないため、初登録の確認を事前に行う必要がある
        driver = kick_page(driver)
    print (driver.current_url)
    time.sleep(SEC_TO_WAIT)
    print ("search by NO")
    driver = search_no(driver)
    print (driver.current_url)
    temp_url = driver.current_url
    for name in df_p:
        print (name)
        i = 0
        cont_list = list()
        driver.get(temp_url)
        textbox = [tag for tag in driver.find_elements_by_tag_name('input') if tag.get_attribute('name') == 'bukkenNumber'][0]
        # 物件番号を入力
        textbox.send_keys(name)
        click_btn(driver, 'value', u'検索', WAIT_COUNT)
        # 検索結果があった場合、リンクをクリック、なかった場合の処理を追加
        vals = click_text(driver, name, WAIT_COUNT)
        driver = vals[0]
        driver_error = vals[1]
        if driver_error == 0:
            # 物件のPDFdownload
            driver = property_info(driver)
            print ('info ok')
            print (driver.current_url)
            driver = property_pdf_for(driver,name)

if __name__ == '__main__':
    main()



