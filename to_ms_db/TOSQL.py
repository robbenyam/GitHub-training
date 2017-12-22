# coding=utf-8
"""
    script for py35
"""
import pandas as pd
import numpy as np
import datetime
import pymssql
import collections

SAMPLE_CSV_FILE = 'sample.csv'

# SERVER = 'JPTYODEVDBS08'
SERVER = '10.37.8.102'
DATABASE = 'SalesManagement'

DF_TYPE_TO_SQL_TYPE = {
    str: 'TEXT'
}


def create_sample():
    df = pd.DataFrame(data={
        'd': [1, 2, 3],
        'f': [1.2, 3.4, 5.6],
        's': [u'sky', u'桐', u'1192'],
        't': [datetime.date(year=1981, month=5, day=11),
              datetime.date(year=2017, month=4, day=5),
              datetime.date(year=2039, month=12, day=29)]
    })

    return df


def sql_dtype(v):
    if isinstance(v, np.int64):
        return 'INT'
    elif isinstance(v, np.float):
        return 'FLOAT'
    elif isinstance(v, str):
        return 'TEXT'
    elif isinstance(v, datetime.datetime):
        return 'DATETIME'
    elif isinstance(v, datetime.date):
        return 'DATETIME'
    elif isinstance(v, np.bool_):
        return 'TEXT'
    elif isinstance(v, bool):
        return 'TEXT'
    print(type(v))
    return 'TEXT'


def add_quotation(cols, record, types):
    values = [record[c] for c in cols]

    for i in range(len(cols)):
        t = types[cols[i]]
        if t == 'INT':
            values[i] = '{}'.format(values[i])
        elif t == 'FLOAT':
            values[i] = '{}'.format(values[i])
        elif t.endswith('TEXT'):
            values[i] = "'{}'".format(values[i])
        elif t == 'DATETIME':
            values[i] = "'{}'".format(values[i].isoformat())

    return values


def create_table(conn, table_name, df_data, overwrite):
    cur = conn.cursor()

    # テーブルがあるか確認する
    df_table = pd.read_sql("SELECT * FROM sysobjects WHERE name = '{}'".format(table_name), conn)

    if len(df_table) > 0:
        if overwrite:
            sql = 'DROP TABLE {t}'.format(t=table_name)
            cur.execute(sql)
            print('{t} dropped'.format(t=table_name))
        else:
            print('{t} already exists'.format(t=table_name))
            return

    # データのカラムと型を取得する
    col_types = collections.OrderedDict()
    for c in df_data.columns:
        col_types[c] = sql_dtype(df_data.loc[0, c])

    # クエリを実行する
    cols_sql = ['{c} {t}'.format(c=c, t=col_types[c]) for c in df_data.columns]
    sql = 'CREATE TABLE {t} ({c})'.format(t=table_name, c=', '.join(cols_sql))
    print(sql)
    cur.execute(sql)

    # テーブルができたか確認する
    df_table = pd.read_sql("SELECT * FROM sysobjects WHERE name = '{}'".format(table_name), conn)
    if len(df_table) == 0:
        print('{t} not found'.format(t=table_name))
        return
    else:
        print(df_table)

    for i in range(len(df_data)):
        record = df_data.iloc[i, :].to_dict()
        values = add_quotation(df_data.columns, record, col_types)
        sql = "INSERT INTO {t} ({c}) VALUES ({v})".format(t=table_name,
                                                          c=', '.join(df_data.columns),
                                                          v=', '.join(values))
        print(sql)
        cur.execute(sql)

    # データが入ったかを確認する
    df = pd.read_sql(sql='SELECT * FROM {t}'.format(t=table_name), con=conn)
    print(df.head())
    print('{:,d} records'.format(len(df)))

    conn.commit()


def main():
    conn = pymssql.connect(server=SERVER, database=DATABASE)
    df_table = pd.read_sql("SELECT * FROM sysobjects WHERE xtype = 'u'", conn)
    print(df_table)

    df = create_sample()
    print(df)
    create_table(conn, 'sample', df, True)

    conn.close()


if __name__ == '__main__':
    main()
