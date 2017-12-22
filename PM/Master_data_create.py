import os
import time
import datetime
import sys
import pandas as pd
import numpy as np
import xlrd


# データ準備
OPATH = os.path.dirname(os.path.abspath(__name__))
OPPO = "oppo_data.csv"
SPOC = "SPOC_data.csv."
HR = "HR_data.xlsx"
MA = "Master_data.csv"
SP = "SP_data.csv"


OPPO_PATH = os.path.join(OPATH, OPPO)
SPOC_PATH = os.path.join(OPATH, SPOC)
HR_PATH = os.path.join(OPATH, HR)
MA_PATH = os.path.join(OPATH, MA)
SP_PATH = os.path.join(OPATH, SP)

def main():
    #データ準備
    print("go with master")
    df_oppo = pd.read_csv(OPPO_PATH, encoding="SHIFT-JISx0213") #商談データロード
    df_spoc = pd.read_csv(SPOC_PATH, encoding="SHIFT-JISx0213") #SPCOデータロード
    df_hrt = pd.read_excel(HR_PATH,sheet_name = 0) #人事マスタロード
    Today = datetime.date.today()#抽出日
    # データフレームの作成
    # 商談データ作成
    df_oppo = df_oppo[df_oppo[u'氏名'].notnull()]
    # SPOCデータ作成
    df_spoc = df_spoc[df_spoc[u'アカウント: 固有アカウントID'].notnull()]
    df_spoc_t = df_spoc[[u'アカウント: 固有アカウントID',u'ソースブローカー',u'SPOC: 所有者 氏名',u'CBRE SPOCメール アドレス']].copy()
    # 人事データ作成
    df_hrt.columns = df_hrt.iloc[1].tolist()
    df_hr = df_hrt[2:].copy()

    # 項目作成
    # 時間項目作成
    df_oppo[u'データ抽出日'] = None
    df_oppo[u'計上予定日YEAR'] = None
    df_oppo[u'データ抽出日'] = Today
    df_oppo[u'計上予定日YEAR']=  df_oppo[u'計上予定日'].str[:4]

    # ＨＲ項目作成
    df_hr['email'] = df_hr['email'].str.lower()
    df_hr['email'] = df_hr['email'].str.replace('@cbre.co.jp','@cbre.com')
    df_oppo[u'メール'] = df_oppo[u'メール'].str.replace('@cbre.co.jp','@cbre.com')
    df_oppo = pd.merge(df_oppo,df_hr[[u'email',u'Start Date',u'PD/SP\n職種']],how='left',left_on=[u'メール'],right_on=[u'email'])
    print(len(df_oppo))
    print('ok')

    #SPOC項目作成
    df_spoc_t = df_spoc_t.drop_duplicates(subset=[u'アカウント: 固有アカウントID',u'CBRE SPOCメール アドレス'],keep='first')
    df_spoc_t[u'SPOCRank'] = None
    df_spoc_t.loc[(df_spoc_t[u'ソースブローカー'].isnull()), u'SPOCRank'] = '未決定'
    df_spoc_t.loc[(df_spoc_t[u'ソースブローカー'] == u'1st_tier'), u'SPOCRank'] = u'1st_tier'
    df_spoc_t.loc[(df_spoc_t[u'ソースブローカー'] == u'2nd_tier'), u'SPOCRank'] = u'2nd_tier'
    df_spoc_t[u'CBRE SPOCメール アドレス'] = df_spoc_t[u'CBRE SPOCメール アドレス'].str.replace('@cbre.co.jp','@cbre.com')
    df_spoc_t.rename(columns={u'アカウント: 固有アカウントID':u'アカウント名: 固有アカウントID', u'CBRE SPOCメール アドレス':'メール'}, inplace=True)#これはSPOCデータマージするため、項目名を統一
      #SPOC：案件担当者の氏名＝SPOC所有者氏名、商談アカウントID＝ＳＰＯＣアカウントID
    df_oppo = pd.merge(df_oppo,df_spoc_t,how='left',on=[u'アカウント名: 固有アカウントID',u'メール'])
    df_oppo.loc[(df_oppo[u'SPOCRank'].isnull()), u'SPOCRank'] = '非対象'

    #最後処理
    df_oppo.drop([u'アカウント名: 固有アカウントID',u'email',u'メール', u'SPOC: 所有者 氏名',u'ソースブローカー'], inplace=True, axis=1)
    df_oppo.rename(columns={u'Start Date': u'入社年次',u'PD/SP\n職種':u'PD/SD職種'}, inplace=True)
    print(len(df_oppo))
    df_oppo.to_csv(MA_PATH, index=False)

if __name__ == '__main__':
    main()