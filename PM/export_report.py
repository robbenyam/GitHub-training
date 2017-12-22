# coding=utf-8
from selenium import webdriver
from selenium.webdriver.support.ui import Select
import time
import os
import pandas as pd
import datetime
import sys
import shutil

OPATH = os.path.dirname(os.path.abspath(__name__))
DOWNLOAD_PATH = OPATH
URL = "https://cbrecrm.my.salesforce.com/"
OPPO = "oppo_data.csv"
SPOC = "SPOC_data.csv."
OPPO_PATH = os.path.join(OPATH, OPPO)
SPOC_PATH = os.path.join(OPATH, SPOC)

REPORT_IDS = ["00O1Y000006cmFY", "00O1Y000006cifS"]
REPORT_NAME = {
    "00O1Y000006cmFY": OPPO, # 0:oppo_data
    "00O1Y000006cifS": SPOC,
}

def download_report(report_id):
    chromeOptions = webdriver.ChromeOptions()
    prefs = {"download.default_directory": DOWNLOAD_PATH}
    chromeOptions.add_experimental_option("prefs", prefs)
    driver = webdriver.Chrome(chrome_options=chromeOptions)

    driver.get(URL + report_id)
    tag = driver.find_element_by_xpath("//div[contains(@class, 'reportActions')]")
    [btn for btn in tag.find_elements_by_xpath("//input[contains(@class, 'btn')]")
     if btn.get_attribute('value') == u'詳細のエクスポート'][0].click()

    elem = driver.find_element_by_id('xf')
    select_obj = Select(elem)
    select_obj.select_by_visible_text(u'カンマ区切り形式(.csv)')

    # ダウンロード前にあるダウンロードファイルの数を数える
    n_files = len([f for f in os.listdir(DOWNLOAD_PATH) if f.startswith('report') and f.endswith('.csv')])

    tag = driver.find_element_by_xpath("//div[contains(@class, 'pbBottomButtons')]")
    [btn for btn in tag.find_elements_by_xpath("//input[contains(@class, 'btn')]")
     if btn.get_attribute('value') == u'エクスポート'][0].click()

    # ダウンロードファイルが増えない限り待つ
    while len([f for f in os.listdir(DOWNLOAD_PATH) if f.startswith('report') and f.endswith('.csv')]) == n_files:
        time.sleep(1)

    driver.quit()

def rename(REP_FILE,name):
    name = str(name)
    print (name)
    file_path_d =  os.path.join(DOWNLOAD_PATH,'{}.csv'.format(name))
    print (file_path_d)
    old_file = os.path.join(DOWNLOAD_PATH, REP_FILE)
    new_file = os.path.join(DOWNLOAD_PATH, name)
    os.rename(old_file, new_file)
    return

def format_report(report_id,name):
    files = [f for f in os.listdir(DOWNLOAD_PATH) if f.startswith('report') and f.endswith('.csv')]
    print(files)
    REP_FILE = os.path.join(DOWNLOAD_PATH, files[0])
    print(REP_FILE)
    if os.path.isfile(REP_FILE):
        rename(REP_FILE,name)

def main():
    print ("export report")
    for report_id in REPORT_IDS:
        print(report_id)
        download_report(report_id)
        print('download ok')
        format_report(report_id,REPORT_NAME[report_id])
        print('format ok')

if __name__ == '__main__':
    main()
