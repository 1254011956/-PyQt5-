# -*- coding: utf-8 -*-
# @Time : 2020/3/22 18:29
# @Author : 永
# @File : Stock_index.py
# @Software: PyCharm

# from StockData_System.gui.mydata.get_data import *
import numpy as np
import pandas as pd
import talib

class StockIndex(object):
    def movingaverage(self,l, N):
        sum = 0
        result = list(0 for x in l)
        for i in range(0, N):
            sum = sum + l[i]
            result[i] = sum / (i + 1)
        for i in range(N, len(l)):
            sum = sum - l[i - N] + l[i]
            result[i] = sum / N
        return result

    def macd(self,close):
        dif,dea,macd = talib.MA_Type(close,
                                    fastperiod=12,fastmatype=1,slowperiod=26,
                                    slowmatype=1,signalperiod=9,signalmatype=1)
        macd = macd * 2
        return dif,dea,macd

    def rsiFunc(self,prices, n):
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

    def kdj(self,low,high,close):
        low_list = low.rolling(9, min_periods=9).min()
        low_list.fillna(value=low.expanding().min(), inplace=True)
        high_list = high.rolling(9, min_periods=9).max()
        high_list.fillna(value=high.expanding().max(), inplace=True)
        rsv = (close - low_list) / (high_list - low_list) * 100
        k = pd.DataFrame(rsv).ewm(com=2).mean()
        d = k.ewm(com=2).mean()
        j = 3 * k - 2 * d

        K = []
        for i in k.values:
            K.append(i)
        K = np.hstack(K)

        D = []
        for i in d.values:
            D.append(i)
        D = np.hstack(D)

        J = []
        for i in j.values:
            J.append(i)
        J = np.hstack(J)
        return K,D,J


