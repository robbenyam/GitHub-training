# coding=utf-8
"""
    script for python 3.5 (source activate py35)
"""
import sys
import os
sys.path.append(os.path.join('..', '..'))

#登録情報
USER_ID= '000195210001'
PASSWORD = {
    '000195210001': 'cbrelogi1',
    '000195210002': 'cbrelogi2'
}
#athomeURL
HOME_PAGE_URL = 'http://atbb.athome.jp/'
ALERT_PAGE_URL = "https://atbb.athome.co.jp/front-web/login/ConcurrentLoginException.jsp"
SEARCH_URL = ['/atbb/hozonJokenIchiran?from=global_menu_bukkenKensaku',
              '/atbb/nyushuSearch?from=global_menu_bukkenKensaku']
IMAG_URL = '//img[contains(@src,"menu_buttons/sub_bnyushu04")]'
PRO_URL = '//div[contains(@class,"bukkenKensakuKekkaWrapper")]/table/tbody/tr/td'
PDF_URL = 'https://zmn.atbb.athome.co.jp/infosheets/info_sheet'

#file path
OPATH = "C:/Users/hakucho.nin/Desktop/forwork/02_project/02_pro/10_athome/20171114"#ルート
OPATH_PDF = "C:/Users/hakucho.nin/Desktop/forwork/02_project/02_pro/10_athome/20171114/pdf"#ルート
RECO = "intro_list.csv" #推薦リスト
GROUP = "group_list.xlsx" #推薦
CLIENT = "client_list.xlsx" #テナントリスト
UPDATE = "update_list.csv" #更新リスト
MATCH = "match_list.csv" #マッチング結果リスト
PDF = "info_sheet.pdf"

#更新リスト項目
PRO_HEAD = ['NO', '物件種目', '所在地', '建物名/部屋番号', '公開日', '画像',
            '登録賃料', '交通（沿線駅/バス停）', '礼金', '管理費等',
            '築年月', '広告転載', '敷金', '保証金', '階建/階', '取引態様', '建物面積',
            '登録会員', 'TEL', '敷引', '坪単価', '建物構造', '物件番号']
#other
SEC_TO_WAIT = 5
WAIT_COUNT = 10
SEARCH_CONDITIONS = 13
CRATE = [0.3025]

M_TITLE = '最新物件紹介'
AT_HOME_BTN = u'物件検索'
P_NO_COL = u'物件番号'