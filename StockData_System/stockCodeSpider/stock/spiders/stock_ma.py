# -*- coding: utf-8 -*-
# 计算平均移动线
# Ma5 Ma10 Ma20 Ma30 Ma60 Ma120 Ma240
# 均线类型，
# AMA,算术移动平均值;
# DWMA,末日加权移动平均值;
# LWMA线性加权移动平均值;
# TWMA梯形加权移动平均值;
# SCWMA平方系数加权移动平均值;
# ESMA指数平滑移动平均线;
import time


class StockMaCompute(object):
    ma_type = ['AMA', 'DWMA', 'LWMA', 'TWMA', 'SCWMA', 'ESMA']

    def __init__(self):
        pass


if __name__ == '__main__':
    date_start = time.strftime('%Y%m%d', time.localtime())
    print(date_start)
