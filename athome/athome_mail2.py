import pandas as pd
import win32com.client as win32
import psutil
import subprocess
import os
import sys
import re
sys.path.append(os.path.join('..', '..'))
import athome_common_set as acs

OPATH = acs.OPATH
MATCH = acs.MATCH
GROUP = acs.GROUP
MAT_PATH = os.path.join(OPATH, MATCH)
GRO_PATH = os.path.join(OPATH, GROUP)

M_TITLE = acs.M_TITLE

# Drafting and sending email notification to senders. You can add other senders' email in the list
def send_notification(id,sub,address,pro_list,body):
    outlook = win32.Dispatch('outlook.application')
    mail = outlook.CreateItem(0)
    mail.To = address
    mail.Subject = sub
    mail.body = body
    if len(pro_list) > 0:
        for att in pro_list():
            att_path = os.path.join(OPATH,att,"pdf")
            mail.attachments.add(Source=att_path)
    mail.display()
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

# Checking if outlook is already opened. If not, open Outlook.exe and send email
def main():
    #ユーザー名で社員番号を検索
    user = os.getlogin()
    df_gro = load_exc_data(GRO_PATH)
    #df_gro['user'] = None
    #df.loc[(df['Email'].str.contains(user)),'None'] = True
    eid = list(set(df_gro.loc[(df_gro['Email'].str.contains(user)),'emp_no_g']))
    address = list(set(df_gro.loc[(df_gro['Email'].str.contains(user)),'Email']))
    sub = M_TITLE


    #クライアント説明一覧をロード
    df = load_csv_data(MAT_PATH)
    emp_list = list(set(df['emp_no_c']))
    #担当者案件を抽出
    if any(eid in s for s in emp_list):
        df_work = df.loc[df['emp_no_c'] == eid]

        ten_list = list(set(df_work.loc[['emp_no_c' == eid], [u'テナント名']]))  # テナント名リスト
        for ts in ten_list:
            df_work_t = df_work.loc[df_work[u'テナント名'] == ts]
            #そのテナントに提供するデータを抽出
            pro_list = df.loc[['emp_no_c' == eid], ['Property_No']]  # 添付ファイル物件番号
            loc_list = df.loc[['emp_no_c' == eid], [u'所在地']]  # 添付ファイル物件番号
            are_list = df.loc[['emp_no_c' == eid], [u'建物面積']]  # 添付ファイル物件番号
            pri_list = df.loc[['emp_no_c' == eid], [u'登録賃料']]  # 添付ファイル物件番号
            #物件情報を抽出、メール内容を整理
            body = '{}様'.format(ts)
            body = body + '\r\n\r\nお世話になっております'
            body = body + '\r\nCBREの｛｝でございます'
            body = body + '\r\n本日推薦したい物件は下記となります'
            body = body + '\r\n---------------------------------------'
            i = 0
            for row in range(len(ten_list)):
                body = body + '\r\n物件{}：'.format(i+1)
                body = body + '\r\n物件所在地:{}'.format(loc_list[i])
                body = body + '\r\n物件面積:{}'.format(are_list[i])
                body = body + '\r\n物件賃料:{}'.format(pri_list[i])
                i = +i
            body = body + '\r\n---------------------------------------'
            body = body + '\r\n詳細は添付ファイルでご確認お願いいたします。'
            body = body + '\r\nよろしくお願いいたします。'
            send_notification(eid, address,pro_list,body)

    else:
        body = '本日更新データの中、紹介できる物件がありません'
        send_notification(eid, address,'', body)


if __name__ == '__main__':
    main()