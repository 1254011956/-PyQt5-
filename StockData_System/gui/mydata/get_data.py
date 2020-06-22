# -*- coding: utf-8 -*-
# @Time : 2020/3/15 12:46 
# @Author : 永
# @File : get_data.py 
# @Software: PyCharm

# -*- coding: utf-8 -*-
# @Time : 2020/3/14 18:48
# @Author : 永
# @File : get_data.py
# @Software: PyCharm

import pandas as pd
import datetime as dt
import numpy as np

def getdata(stockcode,start,end):
    path = 'D:/PythonProject/StockData_System/股票数据/20100303_20200506/'
    code = stockcode
    df = pd.DataFrame()
    filename = path + code + '.csv'
    try:
        rawdata = pd.read_csv(filename,parse_dates = True,encoding = 'gbk')
    except IOError:
        raise Exception('IoError when reading dayline data file:' + filename)
    df = pd.concat([rawdata, df])
    df = df.sort_index()
    #da['日期'] = pd.to_datetime(da['日期']).dt.date
    df = df[(df['日期'] >= start) & (df['日期'] <= end)]

    df = df[~df['成交量'].isin(['0'])]
    df.drop(['股票代码', '前收盘', '涨跌额', '涨跌幅', '换手率',
                 '成交金额', '总市值', '流通市值'], axis=1, inplace=True)
    df = df.rename(columns={'日期': 'DataTime','名称':'Name','收盘价': 'Close', '最高价': 'High', '最低价': 'Low',
                                '开盘价': 'Open', '成交量': 'volumns'})
    order = ['DataTime', 'Name','Open', 'High', 'Low', 'Close', 'volumns']  # 修改columns的顺序
    df = df[order]
    df=df.reset_index(drop=True)
    df.sort_values(by='DataTime', ascending=True, inplace=True)
    df = df.reset_index(drop=True)
    return df

def getdata2(stockcode):
    startdate = dt.date(2019, 2, 18)
    enddate = dt.date(2020, 3, 2)

    code = stockcode
    path = (r'D:/PythonProject/StockData_System/股票数据/沪深行情/' + code + '.csv').strip()
    data = open(path, 'r', encoding='GBK')
    file = pd.read_csv(data)
    df = pd.DataFrame(file)
    df['日期'] = pd.to_datetime(df['日期']).dt.date
    df = df[(df['日期'] >= startdate) & (df['日期'] <= enddate)]

    df.drop(['股票代码', '前收盘', '涨跌额', '涨跌幅','成交金额'], axis=1, inplace=True)
    df = df.rename(columns={'日期': 'DataTime', '名称': 'Name', '收盘价': 'Close', '最高价': 'High', '最低价': 'Low',
                            '开盘价': 'Open', '成交量': 'volumns'})
    order = ['DataTime', 'Name', 'Open', 'High', 'Low', 'Close', 'volumns']  # 修改columns的顺序
    df = df[order]
    df = df.reset_index(drop=True)
    df.sort_values(by='DataTime', ascending=True, inplace=True)
    df = df.reset_index(drop=True)
    return df

def getdata3(stockcode,start,end):
    path = r'D:/PythonProject/StockData_System/股票数据/20100303_20200506/'
    code = stockcode
    df = pd.DataFrame()
    filename = path + code + '.csv'
    try:
        rawdata = pd.read_csv(filename,parse_dates = True,encoding = 'gbk')
    except IOError:
        raise Exception('IoError when reading dayline data file:' + filename)
    df = pd.concat([rawdata, df])
    df = df.sort_index()
    #da['日期'] = pd.to_datetime(da['日期']).dt.date
    df = df[(df['日期'] >= start) & (df['日期'] <= end)]

    df = df[~df['成交量'].isin(['0'])]

    return df
def getdata4(stockcode):
    startdate = dt.date(2015, 2, 18)
    enddate = dt.date(2020, 3, 2)

    code = stockcode
    path = (r'D:/PythonProject/StockData_System/股票数据/20100303_20200506/' + code + '.csv').strip()
    data = open(path, 'r', encoding='GBK')
    file = pd.read_csv(data)
    df = pd.DataFrame(file)
    df['日期'] = pd.to_datetime(df['日期']).dt.date
    df = df[(df['日期'] >= startdate) & (df['日期'] <= enddate)]

    df.drop(['股票代码', '前收盘', '涨跌额', '涨跌幅', '成交金额'], axis=1, inplace=True)
    df = df.rename(columns={'日期': 'DataTime', '名称': 'Name', '收盘价': 'Close', '最高价': 'High', '最低价': 'Low',
                            '开盘价': 'Open', '成交量': 'volumns'})
    order = ['DataTime', 'Name', 'Open', 'High', 'Low', 'Close', 'volumns']  # 修改columns的顺序
    df = df[order]
    df = df.reset_index(drop=True)
    df.sort_values(by='DataTime', ascending=True, inplace=True)
    df = df.reset_index(drop=True)
    return df





