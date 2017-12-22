# coding=utf-8
"""
    script for python 3.5 (source activate py35)
"""
import sys
import os
sys.path.append(os.path.join('..', '..'))

#登録情報取得用
USER_ID= 'hiroshi.okubo@cbre.co.jp'
PASSWORD = {'hiroshi.okubo@cbre.co.jp': 'cbre123'}

#登録情報記入用
USER_ID_SF= 'hakucho.nin@cbre.co.jp.crm'
PASSWORD_SF = "1Qaz2wsx4"

#athomeURL
HOME_PAGE_URL = 'http://nfm.nikkeibp.co.jp/'
SF_GROUP_URL = 'https://cbrecrm.my.salesforce.com/_ui/core/chatter/groups/GroupProfilePage?g=0F9i0000000Laob'
LOGIN_PAGE_URL = "https://g-signon.nikkeibp.co.jp/front/login/?ts=nfm&ct=m&ru=http://kenplatz.nikkeibp.co.jp/NFM/"


#file path
OPATH = "C:/Users/hakucho.nin/Desktop/forwork/02_project/02_pro/16_chatternews"#ルート
#UPDATE = "update_list.csv" #更新リスト
UPDATE_T = "update_list_T.csv"


#更新リスト項目
PRO_HEAD = ['date', 'title', 'text']
#other
SEC_TO_WAIT = 2
WAIT_COUNT = 10
ID = '//*[@id="header"]/div[2]/nav/p/a[2]'
news_id = '//*[@id="articleBody"]'
LINK = '//*[@id="ext-gen2"]/div[1]'

TARGET_GROUP = "0F9i0000000LaobCAC"
FEEDITEM = "FeedItem"
TYPE = "text"
POSTURL = "/services/data/v41.0/chatter/feed-elements?"
access_token_url= "https://login.salesforce.com/services/oauth2/token"

CLIENT_ID = "3MVG9A2kN3Bn17huxONua276cOhKKVrVlkhXGcJqcE2XgTalsb2qZ0e7r9tzLavy7o_V7AAQG7jKctPLq.qDq"
CLIENT_SECRET = "805249544794237623"

"""
{
	"username": "hakucho.nin@cbre.co.jp.crm",
	"client_id": "3MVG9A2kN3Bn17huxONua276cOhKKVrVlkhXGcJqcE2XgTalsb2qZ0e7r9tzLavy7o_V7AAQG7jKctPLq.qDq",
	"client_secret": "805249544794237623",
	"password": "1Qaz2wsx4",
	"sandbox": "False",
	"access_token_url": "https://login.salesforce.com/services/oauth2/token",
	"access_token_url_sandbox": "https://test.salesforce.com/services/oauth2/token"
}
"""
