# coding=utf-8
import os
import datetime
import json
import pandas as pd
from simple_salesforce import Salesforce
import requests

REPOSITORY_NAME = 'CBRE'
USER_HOME_PATH = os.path.join(os.path.expandvars("%userprofile%"))
DOWNLOAD_PATH = os.path.join(USER_HOME_PATH, 'Downloads')
#CLOUD_PATH = os.path.join(USER_HOME_PATH, 'OneDrive - CBRE, Inc', 'cloud_data_repository')
CLOUD_PATH = os.path.join(USER_HOME_PATH, 'OneDrive - CBRE, Inc','attach_files','CBRE', 'cloud_data_repository')

#CLOUD_PATH_1 = os.path.join(r'D:\cloud', 'OneDrive - CBRE, Inc', 'cloud_data_repository')
#CLOUD_PATH_2 = os.path.join(USER_HOME_PATH, 'OneDrive', 'cloud_data_repository')
#CLOUD_PATH = CLOUD_PATH if os.path.exists(CLOUD_PATH) else CLOUD_PATH_1
#CLOUD_PATH = CLOUD_PATH if os.path.exists(CLOUD_PATH) else CLOUD_PATH_2

#PRIVATE_SETTING_PATH = os.path.join(CLOUD_PATH, REPOSITORY_NAME, 'private_settings')
SET_PATH = os.path.join('C:/Users/hakucho.nin/Desktop/forwork/02_project/02_pro/15_chatter/text_data')
SF_CONF_FILE = os.path.join(SET_PATH, 'salesforce_conf.json')

# 各プロジェクトから見たときのパス
SFDC_EXPORT_DATA_PATH = os.path.join(CLOUD_PATH, REPOSITORY_NAME, 'sfdc_export')


def project_data_path(project_name):
    return os.path.join(CLOUD_PATH, REPOSITORY_NAME, project_name)


def project_data_file(project_name, file_name):
    return os.path.join(project_data_path(project_name), file_name)


def server_property(name, key):
    df = pd.DataFrame(json.loads(open(os.path.join(PRIVATE_SETTING_PATH, 'servers.json')).read()))
    return df.ix[key, name]


def sf_conf():
    return json.loads(open(SF_CONF_FILE).read())


def list_files(path):
    print('files in {}'.format(path))
    for f in os.listdir(path):
        print(datetime.datetime.fromtimestamp(os.stat(os.path.join(path, f)).st_mtime), f)


# --------------------------------------------------------------------------------
# クラス・関数宣言 for Salesforce Access
# --------------------------------------------------------------------------------
def lambda_handler(event, context):
    """
        SalesforceにOauth2を使ってログインします
    """
    access_token_url = sf_conf()["access_token_url"]
    data = {
        'grant_type': 'password',
        'client_id': sf_conf()["client_id"],
        'client_secret': sf_conf()["client_secret"],
        'username': sf_conf()["username"],
        'password': sf_conf()["password"]
    }
    headers = {'content-type': 'application/x-www-form-urlencoded'}
    response = requests.post(access_token_url, data=data, headers=headers)
    response = response.json()
    if response.get('error'):
        raise Exception(response.get('error_description'))

    session = requests.Session()
    sf = Salesforce(instance_url=response['instance_url'],
                    session_id=response['access_token'],
                    sandbox=sf_conf()["sandbox"],
                    session=session)

    return sf


def simple_query(sf, cols, table, condition, limit):
    soql = 'SELECT {}'.format(cols[0])

    if len(cols) > 1:
        for col in cols[1:]:
            soql += ', {}'.format(col)

    soql += ' FROM {}'.format(table)

    if condition is not None:
        soql += ' WHERE {}'.format(condition)

    if limit is not None:
        soql += ' LIMIT {}'.format(limit)

    print(soql)

    records = sf.query(soql)
    # query returns OrderedDict
    # - totalSize: number
    # - done: True / False
    # - records: list of OrderedDict
    #     - attributes: cols, url
    #     - col[0]:
    #     - col[1]:
    #     -   ...
    #     - col[n]:
    print('number of records: {:,d}'.format(records['totalSize']))

    if records['done']:
        results = records['records']

        # 結果を１行ずつDictに変換してDataFrameにまとめる
        df = pd.DataFrame()
        for i in range(records['totalSize']):
            results[i].pop('attributes')

            # DictのValue側をListに変換する
            for col in cols:
                results[i][col] = [results[i][col]]

            df = pd.concat([df, pd.DataFrame(data=dict(results[i]))])
        return df.reset_index(drop=True)
    else:
        print('WARNING: Query has not completed!')
        return None


def table_cols(sf, table, key):
    if table == 'Account':
        return [f[key] for f in sf.Account.describe()['fields']]
    elif table == 'spoc__c':
        return [f[key] for f in sf.spoc__c.describe()['fields']]
    elif table == 'User':
        return [f[key] for f in sf.User.describe()['fields']]
    elif table == 'Opportunity':
        return [f[key] for f in sf.Opportunity.describe()['fields']]
    elif table == 'Opportunity_Properties__c':
        return [f[key] for f in sf.Opportunity_Properties__c.describe()['fields']]
    elif table == 'Property__c':
        return [f[key] for f in sf.Property__c.describe()['fields']]
    else:
        return None


def test():
    list_files(DOWNLOAD_PATH)
    list_files(CLOUD_PATH)

    sf = lambda_handler({}, {})
    print(simple_query(sf, ['Id', 'Name', 'Business_Line__c', 'City'], 'User', None, 10))


def main():
    test()


if __name__ == '__main__':
    main()
