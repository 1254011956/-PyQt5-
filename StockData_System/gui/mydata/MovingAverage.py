# -*- coding: utf-8 -*-
# @Time : 2020/3/16 11:07 
# @Author : 永
# @File : MovingAverage.py 
# @Software: PyCharm

import numpy as np
import pandas as pd
from get_data import getdata
import talib
import cgitb
# 这句放在所有程序开始前，这样就可以正常打印异常了
cgitb.enable(format="text")
df = getdata()
def movingaverage(l, N):
    sum = 0
    result = list(0 for x in l)
    for i in range(0, N):
        sum = sum + l[i]
        result[i] = sum / (i + 1)
    for i in range(N, len(l)):
        sum = sum - l[i - N] + l[i]
        result[i] = sum / N
    return result
def rsiFunc(prices, n=14):
    deltas = np.diff(prices)
    seed = deltas[:n+1]
    up = (seed[seed>=0].sum())/n+0.000001
    down = (-seed[seed<0].sum())/n+0.000001
    rs = up/down
    rsi = np.zeros_like(prices)
    rsi[:n] = 100. - 100./(1.+rs)
    for i in range(n, len(prices)):
        delta = deltas[i-1] # cause the diff is 1 shorter
        if delta>0:
            upval = delta
            downval = 0.
        else:
            upval = 0.
            downval = -delta
        up = (up*(n-1) + upval)/n
        down = (down*(n-1) + downval)/n
        rs = up/down
        rsi[i] = 100. - 100./(1.+rs)
    return rsi


def macd(close):
    dif,dea,macd = talib.MA_Type(df.Close,fastperiod=12,fastmatype=1,slowperiod=26,slowmatype=1,signalperiod=9,signalmatype=1)
    macd = macd * 2
    return dif,dea,macd




