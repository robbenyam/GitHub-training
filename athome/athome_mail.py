import pandas as pd
import numpy as np
import win32com.client as win32
import psutil
import subprocess
import os
import sys
import re
sys.path.append(os.path.join('..', '..'))

OPATH = "C:/Users/Hakucho.Nin/Documents/GitHub/CBRE/self_search/auto_match_indus"
PRO = "pro_list.csv"
CLIENT = "client_list.csv"
MATCH = "match_list.csv"
PRO_PATH = os.path.join(OPATH, PRO)
CLI_PATH = os.path.join(OPATH, CLIENT)
MAT_PATH = os.path.join(OPATH, MATCH)

# Drafting and sending email notification to senders. You can add other senders' email in the list
def send_notification():
    outlook = win32.Dispatch('outlook.application')
    mail = outlook.CreateItem(0)
    mail.To = 'Masato.Omori@cbre.co.jp'
    mail.Subject = 'Great Chance'
    mail.body = "4任様\r\nお世話になっております\r\n本日の物件を紹介いたします\r\n物件名：XXXX\r\n面積：XXX坪\r\n住所：東京都渋谷区恵比寿XX\r\n下記URLでご確認お願いいたします\r\nhttp://xxx.com/120230\r\n白鳥"
    print (mail.body)
    mail.send

def load_csv_data(path):
    if os.path.exists(path):
        df = pd.read_csv(path, encoding='cp932')
        return df.reset_index(drop=True)
    else:
        sys.exit("file is not existed")

def load_exc_data(path):
    if os.path.exists(path):
        df = pd.read_excel(path,sheetname = 0)
        return df.reset_index(drop=True)
    else:
        sys.exit("file is not existed")

# Open Outlook.exe. Path may vary according to system config
# Please check the path to .exe file and update below

#def open_outlook():
    #    try:
    #        subprocess.call(['C:\Program Files (x86)\Microsoft Office\\root\Office16\OUTLOOK.EXE'],shell = True)
    #   print('open')
    #except:
#    print("Outlook didn't open successfully")


# Checking if outlook is already opened. If not, open Outlook.exe and send email
def main():

    #クライアント説明一覧をロード
    df = load_exc_data()
    #
    for item in psutil.pids():
        p = psutil.Process(item)
        print (p.name())
        if p.name() == "OUTLOOK.EXE":
            flag = 1
            break
        else:
            flag = 0

    if (flag == 1):
        send_notification()
    else:
        open_outlook()
        send_notification()

if __name__ == '__main__':
    main()