# -*- coding: utf-8 -*-
from simple_salesforce import Salesforce
import datetime
import requests
import os
import sys
from datetime import datetime, timedelta
import pandas as pd
from pytz import timezone

sys.path.append(os.path.join(os.pardir, os.pardir))
import common_settings

"""
[salesforce_conf]の中身
client_id                = ""
client_secret            = ""
username                 = ""
password                 = ""
sandbox                  = False
access_token_url         = 'https://login.salesforce.com/services/oauth2/token'
access_token_url_sandbox = 'https://test.salesforce.com/services/oauth2/token'
"""

# --------------------------------------------------------------------------------
# 初期化処理
# --------------------------------------------------------------------------------
# sf_conf = {}
# execfile(CONF_FILE, sf_conf)
sf_conf = common_settings.sf_conf()
SETPATH = common_settings.SET_PATH

# --------------------------------------------------------------------------------
# クラス・関数宣言
# --------------------------------------------------------------------------------
def lambda_handler(event, context):
    """
        SalesforceにOauth2を使ってログインし、オブジェクト一覧を表示します
    """
    access_token_url = sf_conf["access_token_url"]
    data = {
        'grant_type': 'password',
        'client_id': sf_conf["client_id"],
        'client_secret': sf_conf["client_secret"],
        'username': sf_conf["username"],
        'password': sf_conf["password"]
    }
    headers = {'content-type': 'application/x-www-form-urlencoded'}
    response = requests.post(access_token_url, data=data, headers=headers)
    response = response.json()
    if response.get('error'):
        raise Exception(response.get('error_description'))

    session = requests.Session()
    sf = Salesforce(instance_url=response['instance_url'],
                    session_id=response['access_token'],
                    sandbox=sf_conf["sandbox"],
                    session=session)
    return sf


def describe_instance(sf):
    print ("describe_instance")
    result = sf.describe()
    print ("result")
    print (len(result['sobjects']))
    if len(result['sobjects']):
        print('name,label')
        for record in result['sobjects']:
            print('{n},{l}'.format(n=record['name'].encode('cp932'), l=record['label'].encode('cp932')))


# elseifにテーブルを追加すること
def table_cols(sf, table, key):
    if table == 'FeedComment':
        return [f[key] for f in sf.FeedComment.describe()['fields']]
    if table == 'CollaborationGroupRecord':
        return [f[key] for f in sf.CollaborationGroupRecord.describe()['fields']]
    if table == 'ChatterActivity':
        return [f[key] for f in sf.ChatterActivity.describe()['fields']]
    if table == 'CollaborationGroup':
        return [f[key] for f in sf.CollaborationGroup.describe()['fields']]
    if table == 'CollaborationGroupFeed':
        return [f[key] for f in sf.CollaborationGroupFeed.describe()['fields']]
    if table == 'ChatterActivity':
        return [f[key] for f in sf.ChatterActivity.describe()['fields']]
    if table == 'Collaboration':
        return [f[key] for f in sf.Collaboration.describe()['fields']]
    else:
        return None


def select_query(sf, cols, table, condition, limit):
    soql = 'SELECT {}'.format(cols[0])

    if len(cols) > 1:
        for col in cols[1:]:
            soql += ', {}'.format(col)

    soql += ' FROM {}'.format(table)

    if condition is not None:
        soql += ' WHERE {}'.format(condition)

    if limit is not None:
        soql += ' LIMIT {}'.format(limit)

    records = sf.query(soql)
    size = records['totalSize']

    if records['done']:
        table_result = records['records']

    data = {}
    for rec in table_result:
        for k in cols:
            data.setdefault(k, []).append(rec[k])
    df = pd.DataFrame(data)
    return (df)


def main():
    # SF連結
    argv = sys.argv
    argc = len(argv)
    if(argc !=3):
        print ("日時入力漏れ")
        sys.exit()
    start_date = argv[1]
    end_date = argv[2]
    OUTFILE = 'feeddata_{}_{}.csv'.format(start_date, end_date)
    OUTPATH = os.path.join(SETPATH,OUTFILE)

    start_date = datetime.strptime(start_date, '%Y-%m-%d')
    end_date = datetime.strptime(end_date, '%Y-%m-%d')
    work_start_date = timezone('Asia/Tokyo').localize(start_date).astimezone(timezone('UTC')).isoformat()
    work_end_date = timezone('Asia/Tokyo').localize(end_date).astimezone(timezone('UTC')).isoformat()

    print(work_start_date)

    print ("login")
    sf = lambda_handler({}, {})
    df_CGF = select_query(sf, [u'Id',
                               u'ParentId',
                               u'CreatedDate',
                               u'Type',
                               u'CreatedById',
                               u'LastModifiedDate',
                               u'Title',
                               u'Body',
                               u'LinkUrl',
                               ],
                           'CollaborationGroupFeed', "ParentId in ('0F9i0000000LackCAC') and CreatedDate >= {} and CreatedDate <= {}".format(work_start_date,work_end_date), None)
    if df_CGF is not None:
        print ('df_CGF is ok')

    ids = set(df_CGF['CreatedById'].tolist())
    df_name = pd.DataFrame()
    for att in ids:
        df_name_t = select_query(sf, ['Id',
                                      'Title',
                                      'Name',
                                      'Email'],
                                 'User', "Id in ('{}')".format(att), None)
        if len(df_name_t) > 0:
            df_name = pd.concat([df_name, df_name_t])

    df_feeddata = pd.merge(df_CGF,df_name,how='left',left_on='CreatedById',right_on='Id')
    drop_cal=['CreatedById','Id_y']
    df_feeddata = df_feeddata.drop(drop_cal,axis=1)

    df_feeddata = df_feeddata.rename(columns={'Id_x':'FeedID',
                                'CreatedDate': '作成時間',
                                'LastModifiedDate':'最終更新時間',
                                'LinkUrl':'添付リンク',
                                'Name': '作成者名',
                                'Title_y': '作成者タイトル',
                                'Email': '作成者メール',
                                'Body': '作成内容',
                                'Title_x':'添付ファイル名'})

    df_feeddata = df_feeddata.sort_values(by=["作成時間"], ascending=False)
    sequence = ['ParentId','FeedID','作成時間','最終更新時間','作成者名','作成者タイトル','作成者メール','作成内容','Type','添付ファイル名','添付リンク']
    df_feeddata = df_feeddata.reindex(columns=sequence)
    df_feeddata.to_csv(OUTPATH,index = False)

# メイン関数
if __name__ == "__main__":
    main()
