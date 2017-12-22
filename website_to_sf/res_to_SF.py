# coding=utf-8
"""
for py35
"""
import urllib.request
import json
import os
import time
import datetime
import sys
import pypyodbc as ppo
import pandas as pd
import numpy as np
import res_common_set as acs



# 各パラメータ
TARGET_GROUP = acs.TARGET_GROUP
FEEDITEM = acs.FEEDITEM
TYPE = acs.TYPE
POSTURL = acs.POSTURL
access_token_url = acs.access_token_url

# ログイン情報
USER_ID = acs.USER_ID_SF
PASSWORD = acs.PASSWORD_SF
CLIENT_ID = acs.CLIENT_ID
CLIENT_SECRET = acs.CLIENT_SECRET

# ファイルpath情報
OPATH = acs.OPATH
UPDATE_T = acs.UPDATE_T
UPDATE_PATH_T = os.path.join(OPATH, UPDATE_T)

# API指示を作成
def PostFeedItem(val,token):
    #入力内容を記入
    try:
        chatter_param = {
            "body": {
                "messageSegments": [{
                    "type": TYPE,#送信タイプ
                    "text":  str(val)#送信内容
                }]
            },
            "feedElementType": FEEDITEM,#feedタイプ
            "subjectId": TARGET_GROUP#グループＩＤ

        }

        chatter_headers = {
            "Content-Type": "application/json",
            "Authorization": "Bearer " + token["access_token"]
        }

        chatter_req = urllib.request.Request(
            url=token["instance_url"] + POSTURL,#SFv40用URL
            data=json.dumps(chatter_param).encode(),
            headers=chatter_headers
        )
        chatter_res = urllib.request.urlopen(chatter_req)
        print(chatter_res.read().decode())
    except urllib.error.HTTPError as e:
        print(e.read())


def main():
    today = datetime.date.today()
    print (today)
    #データをロード
    df_text_t = pd.read_csv(UPDATE_PATH_T, encoding="SHIFT-JISx0213")

    request_param = {
        "grant_type": "password",
        "client_id": CLIENT_ID,
        "client_secret": CLIENT_SECRET,
        "username": USER_ID,
        "password": PASSWORD
    }

    headers = {
        "Content-Type": "application/x-www-form-urlencoded"
    }
    req = urllib.request.Request(
        url=access_token_url,
        data=urllib.parse.urlencode(request_param).encode(),
        headers=headers
    )

    res = urllib.request.urlopen(req)
    token = json.loads(res.read().decode())

    lenoftext = len(df_text_t)
    #テキスト入力COUNT
    for i in range(lenoftext):
        text = today + '\n' + df_text_t.loc[i][0]
        PostFeedItem(text,token)

if __name__ == '__main__':
    main()

