# -*- coding: utf-8 -*-
# @Time : 2020/4/10 0:12
# @Author : 永
# @File : run_mytest.py
# @Software: PyCharm


import sys
from PyQt5 import QtCore
from PyQt5.QtWidgets import QMainWindow,QApplication,QMessageBox
from PyQt5.QtCore import QDate,pyqtSlot
import pyqtgraph as pg
import talib
import fbprophet
import matplotlib.pyplot as plt

from gui.ui.newwindow import Ui_MainWindow
from gui.mydata.get_data import *
from gui.mydata.DataItem import *
from gui.draw.Candlestick import CandlestickItem
from gui.draw.DrawMACD import MacdPaint
from gui.stockindex.Stock_index import *

import traceback
import cgitb

# 这句放在所有程序开始前，这样就可以正常打印异常了
cgitb.enable(format="text")

class MyWindow(QMainWindow):
    def __init__(self,parent=None):
        super(MyWindow, self).__init__(parent)

        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        self.ui.StartDataEdit.setCalendarPopup(True)
        self.ui.StartDataEdit.dateChanged.connect(self.onStartDateChanged)
        self.ui.EndDataEdit.setCalendarPopup(True)
        self.ui.EndDataEdit.dateChanged.connect(self.onEndDateChanged)

        self.ui.StartDataEdit_2.setCalendarPopup(True)
        self.ui.StartDataEdit_2.dateChanged.connect(self.onStartDateChanged2)
        self.ui.EndDataEdit_2.setCalendarPopup(True)
        self.ui.EndDataEdit_2.dateChanged.connect(self.onEndDateChanged2)

        # 创建画布
        self.plt1 = pg.PlotWidget()
        self.plt2 = pg.PlotWidget()
        self.plt3 = pg.PlotWidget()
        self.plt4 = pg.PlotWidget()
        self.plt5 = pg.PlotWidget()

        #创建Y轴标签
        self.plt1.setLabels(left='K-Line')
        self.plt2.setLabels(left=u'成交量')
        self.plt3.setLabels(left='MACD(DIF/DEA)')

        #把画布变成Widget控件
        self.ui.verticalLayout_11.addWidget(self.plt2, 1)
        self.ui.verticalLayout_11.addWidget(self.plt1, 3)
        self.ui.horizontalLayout_3.addWidget(self.plt3, )
        self.ui.verticalLayout.addWidget(self.plt4)
        self.ui.verticalLayout_2.addWidget((self.plt5))

        self.draw_Shangzheng_Volumn()
        self.draw_Shangzheng_K_line()
        self.draw_Shangzheng_MACD()

        # 鼠标交互信号
        self.move_slot1 = pg.SignalProxy(self.plt1.scene().sigMouseMoved, rateLimit=60, slot=self.mousemove1)
        self.move_slot2 = pg.SignalProxy(self.plt1.scene().sigMouseMoved, rateLimit=60, slot=self.mousemove2)
        self.move_slot3 = pg.SignalProxy(self.plt1.scene().sigMouseMoved, rateLimit=60, slot=self.mousemove3)
        self.move_slot4 = pg.SignalProxy(self.plt1.scene().sigMouseMoved, rateLimit=60, slot=self.mousemove4)

    # 时间改变信号
    def onStartDateChanged(self, Startdate):
        self.Startdate = QDate.toString(Startdate,"yyyy-MM-dd")

    def onEndDateChanged(self, Enddate):
        self.Enddate = QDate.toString(Enddate, "yyyy-MM-dd")

    def onStartDateChanged2(self, Startdate2):
        self.Startdate2 = QDate.toString(Startdate2,"yyyy-MM-dd")

    def onEndDateChanged2(self, Enddate2):
        self.Enddate2 = QDate.toString(Enddate2, "yyyy-MM-dd")

    # 上证指数
    @pyqtSlot()
    def on_ShangZhengbtn_clicked(self):

        self.ui.textEdit.clear()

        self.draw_Shangzheng_Volumn()
        self.draw_Shangzheng_K_line()
        self.draw_Shangzheng_MACD()

#   绘制成交量图
    def draw_Shangzheng_Volumn(self):
        self.plt2.plotItem.clear()
        self.code1 = '000001'
        self.df1 = getdata2(self.code1)

        self.name1 = self.df1['Name'][0]
        self.da1 = self.df1['DataTime']
        self.Volumns1 = self.df1['volumns']
        self.Close1 = self.df1['Close']
        self.df1.index = self.df1['DataTime']
        self.df1.drop(['DataTime', 'Name'], axis=1, inplace=True)

        y = self.Volumns1
        a1 = len(y)
        x = []
        for i in range(0, a1):
            i += 0
            x.append(i)

        self.data_list1 = []
        t = 0
        for dates, row in self.df1.iterrows():
            open, high, low, close, volumns = row[:5]
            datas = (t, open, close, low, high, volumns)
            self.data_list1.append(datas)
            t += 1
        self.xdict1 = {0: str(self.df1.index[0]).replace('-', '/'),
                      int((t + 1) / 2) - 1: str(self.df1.index[int((t + 1) / 2)]).replace('-', '/'),
                      t - 2: str(self.df1.index[-1]).replace('-', '/')}
        self.stringaxis = pg.AxisItem(orientation='bottom')
        self.stringaxis.setTicks([self.xdict1.items()])
        self.plt2.plot(y,pen='b')
        self.plt2.getAxis('bottom').setTicks([self.xdict1.items()])
        bg1 = pg.BarGraphItem(x=x, height=y, width=1, pen='b')
        self.plt2.addItem(bg1)
        name = str(self.code1 + self.name1)
        self.plt2.setTitle(name, color='w')
        #self.plt2.showGrid(x=True, y=True)

#   绘制K线图
    def draw_Shangzheng_K_line(self):
        self.plt1.plotItem.clear()

        ma5 = movingaverage(self.df1.Close.values, 5)
        ma20 = movingaverage(self.df1.Close.values, 20)
        ma50 = movingaverage(self.df1.Close.values, 50)
        self.df1['ma5'] = ma5
        self.df1['ma20'] = ma20
        self.df1['ma50'] = ma50

        self.plt1.plot(ma5,pen='w',name='5日移动均线')
        self.plt1.plot(ma20,pen='c',name='20日移动均线')
        self.plt1.plot(ma50,pen='m',name='50日移动均线')
        #self.plt1.addLegend()
        self.item1 = CandlestickItem(self.data_list1)
        self.stringaxis.setTicks([self.xdict1.items()])
        self.plt1.getAxis('bottom').setTicks([self.xdict1.items()])
        self.plt1.addItem(self.item1)
        #self.plt1.showGrid(x=True, y=True)


        self.label1 = pg.TextItem()  # 创建一个文本项
        self.plt1.addItem(self.label1)  # 在图形部件中添加文本项
        self.vLine1 = pg.InfiniteLine(angle=90, movable=False, )  # 创建一个垂直线条
        self.hLine1 = pg.InfiniteLine(angle=0, movable=False, )  # 创建一个水平线条
        self.vLine1.setPen(0,0,0)
        self.hLine1.setPen(0,0,0)
        self.plt1.plotItem.addItem(self.vLine1, ignoreBounds=True)  # 在图形部件中添加垂直线条
        self.plt1.plotItem.addItem(self.hLine1, ignoreBounds=True)  # 在图形部件中添加水平线条


#   绘制MACD指标
    def draw_Shangzheng_MACD(self):
        self.plt3.plotItem.clear()
        self.plt4.plotItem.clear()
        self.plt5.plotItem.clear()
        # MA_Type: 0=SMA, 1=EMA, 2=WMA, 3=DEMA, 4=TEMA, 5=TRIMA, 6=KAMA, 7=MAMA, 8=T3 (Default=SMA)
        DIF, DEA, MACD = talib.MACD(self.Close1, 12, 26, 9)

        c = {"DIF":DIF[33:],"DEA":DEA[33:]}
        mydata = pd.DataFrame(c)

        a = {'MACD':MACD[33:]}
        macd = pd.DataFrame(a)
        macd=macd.reset_index()
        y = macd['MACD']

        b = []
        for i in range(0,len(y)):
            i+=0
            b.append(i)
        bg1 = pg.BarGraphItem(x=b, height=y, width=1, )
        self.plt3.addItem(bg1)

        mydata2=[]
        t=0
        for data,row in mydata.iterrows():
            DIF,DEA = row[:2]
            datas = (t,DIF,DEA)
            mydata2.append(datas)
            t +=1

        dif=[]
        for i in mydata.DIF:
            dif.append(i)
        dea=[]
        for i in mydata.DEA:
            dea.append(i)

        self.plt3.plot(dif,pen='r',name='DIF')
        self.plt3.plot(dea[1:], pen='b', name='DEA')
        #self.plt3.addLegend()
        self.stringaxis.setTicks([self.xdict1.items()])
        self.plt3.getAxis('bottom').setTicks([self.xdict1.items()])

        RSI1 = rsiFunc(self.Close1.values,6)
        RSI2 = rsiFunc(self.Close1.values,12)
        RSI3 = rsiFunc(self.Close1.values,24)
        self.plt4.plot(RSI1,pen=(255,99,71),name='RSI6')
        self.plt4.plot(RSI2,pen=(144,238,144),name='RSI12')
        self.plt4.plot(RSI3,pen=(205,201,201),name='RSI24')
        #self.plt4.addLegend()
        self.stringaxis.setTicks([self.xdict1.items()])
        self.plt4.getAxis('bottom').setTicks([self.xdict1.items()])

        k, d, j = kdj(self.df1['Low'], self.df1['High'], self.df1['Close'])
        self.plt5.plot(k,pen='r')
        self.plt5.plot(d,pen='b')
        self.plt5.plot(j,pen='y')


    # 深证成指
    @pyqtSlot()
    def on_ShenZhengbtn_clicked(self):
        self.ui.textEdit.clear()
        self.code2 = '399001'
        self.df2 = getdata2(self.code2)

        self.da2 = self.df2['DataTime']
        self.Volumns2 = self.df2['volumns']
        self.Close2 = self.df2['Close']
        self.df2.index = self.df2['DataTime']
        self.df2.drop(['DataTime', 'Name'], axis=1, inplace=True)




        self.draw_Shenzheng_Volumn()
        self.draw_Shenzheng_K_line()
        self.draw_Shenzheng_MACD()

#   绘制成交量tu
    def draw_Shenzheng_Volumn(self):
        self.plt2.plotItem.clear()

        y = self.Volumns2
        a = len(y)
        x = []
        for i in range(0, a):
            i += 0
            x.append(i)

        self.data_list2 = []
        t = 0
        for dates, row in self.df2.iterrows():
            open, high, low, close, volumns = row[:5]
            datas = (t, open, close, low, high, volumns)
            self.data_list2.append(datas)
            t += 1
        # 创建X轴及刻度
        self.xdict2 = {0: str(self.df2.index[0]).replace('-', '/'),
                      int((t + 1) / 2) - 1: str(self.df2.index[int((t + 1) / 2)]).replace('-', '/'),
                      t - 2: str(self.df2.index[-1]).replace('-', '/')}
        self.stringaxis = pg.AxisItem(orientation='bottom')
        self.stringaxis.setTicks([self.xdict2.items()])
        self.plt2.getAxis('bottom').setTicks([self.xdict2.items()])
        bg = pg.BarGraphItem(x=x,height=y,width=1,pen='b')
        self.plt2.plot(y, pen='b',)

        self.plt2.addItem(bg)
        name = str(self.code2 + '深证成指')
        self.plt2.setTitle(name, color='w')
        #self.plt2.showGrid(x=True, y=True)

#   绘制K线图
    def draw_Shenzheng_K_line(self):
        self.plt1.plotItem.clear()

        ma5 = movingaverage(self.df2.Close.values, 5)
        ma20 = movingaverage(self.df2.Close.values, 20)
        ma50 = movingaverage(self.df2.Close.values, 50)
        self.df2['ma5'] = ma5
        self.df2['ma20'] = ma20
        self.df2['ma50'] = ma50
        self.plt1.plot(ma5, pen='w')
        self.plt1.plot(ma20, pen='c')
        self.plt1.plot(ma50, pen='m')
        #self.plt1.addLegend()
        self.item2 = CandlestickItem(self.data_list2)

        self.stringaxis.setTicks([self.xdict2.items()])
        self.plt1.getAxis('bottom').setTicks([self.xdict2.items()])
        self.plt1.addItem(self.item2)
        #self.plt1.showGrid(x=True, y=True)
        self.label2 = pg.TextItem()  # 创建一个文本项
        self.plt1.addItem(self.label2)  # 在图形部件中添加文本项
        self.vLine2 = pg.InfiniteLine(angle=90, movable=False, )  # 创建一个垂直线条
        self.hLine2 = pg.InfiniteLine(angle=0, movable=False, )  # 创建一个水平线条
        self.vLine2.setPen(0, 0, 0)
        self.hLine2.setPen(0, 0, 0)
        self.plt1.plotItem.addItem(self.vLine2, ignoreBounds=True)  # 在图形部件中添加垂直线条
        self.plt1.plotItem.addItem(self.hLine2, ignoreBounds=True)  # 在图形部件中添加水平线条

#   绘制MACD指标
    def draw_Shenzheng_MACD(self):
        self.plt3.plotItem.clear()
        self.plt4.plotItem.clear()
        self.plt5.plotItem.clear()
        # MA_Type: 0=SMA, 1=EMA, 2=WMA, 3=DEMA, 4=TEMA, 5=TRIMA, 6=KAMA, 7=MAMA, 8=T3 (Default=SMA)
        DIF, DEA, MACD = talib.MACD(self.Close2, 12, 26, 9)

        c = {"DIF": DIF[33:], "DEA": DEA[33:]}
        mydata = pd.DataFrame(c)

        mydata2 = []
        t = 0
        for data, row in mydata.iterrows():
            DIF, DEA = row[:2]
            datas = (t, DIF, DEA)
            mydata2.append(datas)
            t += 1

        a = {'MACD': MACD[33:]}
        macd = pd.DataFrame(a)
        macd = macd.reset_index()
        y = macd['MACD']

        b = []
        for i in range(0, len(y)):
            i += 0
            b.append(i)
        bg1 = pg.BarGraphItem(x=b, height=y, width=1, )
        self.plt3.addItem(bg1)
        item = MacdPaint(mydata2[2:])
        self.plt3.addItem(item)

        #self.plt3.plot(ma[33:], pen='r', width='1')
        self.stringaxis.setTicks([self.xdict2.items()])
        self.plt3.getAxis('bottom').setTicks([self.xdict2.items()])

        RSI1 = rsiFunc(self.Close2.values, 6)
        RSI2 = rsiFunc(self.Close2.values, 12)
        RSI3 = rsiFunc(self.Close2.values, 24)
        self.plt4.plot(RSI1, pen=(255, 99, 71), )
        self.plt4.plot(RSI2, pen=(144, 238, 144), )
        self.plt4.plot(RSI3, pen=(205, 201, 201), )
        self.stringaxis.setTicks([self.xdict2.items()])
        self.plt4.getAxis('bottom').setTicks([self.xdict2.items()])

        k, d, j = kdj(self.df2['Low'], self.df2['High'], self.df2['Close'])
        self.plt5.plot(k, pen='r')
        self.plt5.plot(d, pen='b')
        self.plt5.plot(j, pen='y')

    # 沪深300
    @pyqtSlot()
    def on_HuShenbtn_clicked(self):
        self.ui.textEdit.clear()
        self.code3 = '399300'
        self.df3 = getdata2(self.code3)
        self.da3 = self.df3['DataTime']
        self.Volumns3 = self.df3['volumns']
        self.Close3 = self.df3['Close']
        self.df3.index = self.df3['DataTime']
        self.df3.drop(['DataTime', 'Name'], axis=1, inplace=True)


        self.draw_HuShen_Volumn()
        self.draw_HuShen_K_line()

        self.draw_HuShen_MACD()

#绘制成交量图
    def draw_HuShen_Volumn(self):
        self.plt2.plotItem.clear()
        y = self.Volumns3
        a = len(y)
        x = []
        for i in range(0, a):
            i += 0
            x.append(i)

        self.data_list3 = []
        t = 0
        for dates, row in self.df3.iterrows():
            open, high, low, close, volumns = row[:5]
            datas = (t, open, close, low, high, volumns)
            self.data_list3.append(datas)
            t += 1

        # 创建X轴及刻度
        self.xdict3 = {0: str(self.df3.index[0]).replace('-', '/'),
                       int((t + 1) / 2) - 1: str(self.df3.index[int((t + 1) / 2)]).replace('-', '/'),
                       t - 2: str(self.df3.index[-1]).replace('-', '/')}
        self.stringaxis = pg.AxisItem(orientation='bottom')
        self.stringaxis.setTicks([self.xdict3.items()])
        self.plt2.getAxis('bottom').setTicks([self.xdict3.items()])

        self.plt2.plot(y, pen='b',name='volumn' )
        bg = pg.BarGraphItem(x=x,height=y,width=1,pen='b')
        #self.plt2.addLegend()
        # bg1 = pg.BarGraphItem(x=x, height=y, width=0.3, pen='b')
        self.plt2.addItem(bg)
        name = str(self.code3 + '沪深300')
        self.plt2.setTitle(name, color='w')
        #self.plt2.showGrid(x=True, y=True)

#   绘制K线图
    def draw_HuShen_K_line(self):
        self.plt1.plotItem.clear()

        ma5 = movingaverage(self.df3.Close.values, 5)
        ma20 = movingaverage(self.df3.Close.values, 20)
        ma50 = movingaverage(self.df3.Close.values, 50)
        self.plt1.plot(ma5, pen='w')
        self.plt1.plot(ma20, pen='c')
        self.plt1.plot(ma50, pen='m')
        #self.plt1.addLegend()


        self.item3 = CandlestickItem(self.data_list3)

        self.stringaxis.setTicks([self.xdict3.items()])
        self.plt1.getAxis('bottom').setTicks([self.xdict3.items()])
        self.plt1.addItem(self.item3)
        #self.plt1.showGrid(x=True, y=True)

        self.label3 = pg.TextItem()  # 创建一个文本项
        self.plt1.addItem(self.label3)  # 在图形部件中添加文本项
        self.vLine3 = pg.InfiniteLine(angle=90, movable=False, )  # 创建一个垂直线条
        self.hLine3 = pg.InfiniteLine(angle=0, movable=False, )  # 创建一个水平线条
        self.vLine3.setPen(0, 0, 0)
        self.hLine3.setPen(0, 0, 0)
        self.plt1.plotItem.addItem(self.vLine3, ignoreBounds=True)  # 在图形部件中添加垂直线条
        self.plt1.plotItem.addItem(self.hLine3, ignoreBounds=True)  # 在图形部件中添加水平线条

#绘制MACD指标
    def draw_HuShen_MACD(self):
        self.plt3.plotItem.clear()
        self.plt4.plotItem.clear()
        self.plt5.plotItem.clear()

        # MA_Type: 0=SMA, 1=EMA, 2=WMA, 3=DEMA, 4=TEMA, 5=TRIMA, 6=KAMA, 7=MAMA, 8=T3 (Default=SMA)
        DIF, DEA, MACD = talib.MACD(self.Close3, 12, 26, 9)


        c = {"DIF": DIF[33:], "DEA": DEA[33:]}
        mydata = pd.DataFrame(c)

        mydata2 = []
        t = 0
        for data, row in mydata.iterrows():
            DIF, DEA = row[:2]
            datas = (t, DIF, DEA)
            mydata2.append(datas)
            t += 1

        a = {'MACD': MACD[33:]}
        macd = pd.DataFrame(a)
        macd = macd.reset_index()
        y = macd['MACD']

        b = []
        for i in range(0, len(y)):
            i += 0
            b.append(i)
        bg1 = pg.BarGraphItem(x=b, height=y, width=1, )
        self.plt3.addItem(bg1)

        item = MacdPaint(mydata2[2:])
        self.plt3.addItem(item)

        #self.plt3.plot(ma[33:], pen='r', width='1')
        self.stringaxis.setTicks([self.xdict3.items()])
        self.plt3.getAxis('bottom').setTicks([self.xdict3.items()])

        RSI1 = rsiFunc(self.Close3.values, 6)
        RSI2 = rsiFunc(self.Close3.values, 12)
        RSI3 = rsiFunc(self.Close3.values, 24)
        self.plt4.plot(RSI1, pen=(255, 99, 71))
        self.plt4.plot(RSI2, pen=(144, 238, 144))
        self.plt4.plot(RSI3, pen=(205, 201, 201))
        self.stringaxis.setTicks([self.xdict3.items()])
        self.plt4.getAxis('bottom').setTicks([self.xdict3.items()])

        k, d, j = kdj(self.df3['Low'], self.df3['High'], self.df3['Close'])
        self.plt5.plot(k, pen='r')
        self.plt5.plot(d, pen='b')
        self.plt5.plot(j, pen='y')

    def messageDialog(self,title,message):
        msg_box = QMessageBox(QMessageBox.Warning,title,message)
        msg_box.exec_()
    @pyqtSlot()
    def on_Selectbtn_clicked(self):
        self.ui.textEdit.clear()
        self.code = self.ui.lineEdit.text()
        try:
            self.df = getdata(self.code, self.Startdate, self.Enddate)
        except:
            self.messageDialog('警告', '信息输入错误，请重新输入')
        self.name = self.df['Name'][0]
        self.da = self.df['DataTime']
        self.Volumns = self.df['volumns']
        self.Close = self.df['Close']

        self.ma5 = movingaverage(self.df.Close.values, 5)
        self.ma20 = movingaverage(self.df.Close.values, 20)
        self.ma50 = movingaverage(self.df.Close.values, 50)
        self.df["ma5"] = self.ma5
        self.df["ma20"] = self.ma20
        self.df["ma50"] = self.ma50
       # 计算金叉死叉
        golden_cross = []
        death_cross = []
        for i in range(1, len(self.df)):
            if self.df["ma5"][i] >= self.df["ma20"][i] and self.df["ma5"][i - 1] < self.df["ma20"][i - 1]:
                golden_cross.append(self.df.index[i])
            if self.df["ma5"][i] <= self.df["ma20"][i] and self.df["ma5"][i - 1] > self.df["ma20"][i - 1]:
                death_cross.append(self.df.index[i])
        #print(self.df['DataTime'].loc[golden_cross])
        a = self.df['DataTime'].loc[golden_cross]#金叉日期
        c = self.df['DataTime'].loc[death_cross]#死叉日期

        self.b = []
        for i in a.values:
            i = ('金叉日期:' + str(i))
            self.b.append(i)
        self.d = []
        for i in c.values:
            i = ('死叉日期' + str(i))
            self.d.append(i)

        self.df.index = self.df['DataTime']
        self.df.drop(['DataTime', 'Name'], axis=1, inplace=True)
        self.data_list = []
        t = 0
        for dates, row in self.df.iterrows():
            open, high, low, close, volumns = row[:5]
            datas = (t, open, close, low, high, volumns)
            self.data_list.append(datas)
            t += 1
        self.draw_volums()
        self.K_line()
        self.MACD_line()


#  成交量柱状图
    def draw_volums(self):
        self.plt2.plotItem.clear()
        y = self.Volumns
        a = len(y)
        x=[]
        t = 0
        for i in range(0,a):
            i += 0
            x.append(i)
            t +=1
    # 创建X轴及刻度
        self.xdict = {0: str(self.df.index[0]).replace('-', '/'),
                      int((t + 1) / 2) - 1: str(self.df.index[int((t + 1) / 2)]).replace('-', '/'),
                      t - 2: str(self.df.index[-1]).replace('-', '/')}
        self.stringaxis = pg.AxisItem(orientation='bottom')
        self.stringaxis.setTicks([self.xdict.items()])
        self.plt2.plot(y,pen='b')
        self.plt2.getAxis('bottom').setTicks([self.xdict.items()])
        bg1 = pg.BarGraphItem(x=x, height=y, width=1, pen='b')
        self.plt2.addItem(bg1)
        name = str(self.code + self.name)
        self.plt2.setTitle(name, color='w')
        #self.plt2.showGrid(x=True, y=True)

#   K线图
    def K_line(self):
        self.plt1.plotItem.clear()
        self.plt1.plot(self.ma5, pen='w')
        self.plt1.plot(self.ma20, pen='c')
        self.plt1.plot(self.ma50, pen='m')
        #self.plt1.addLegend()

        self.item = CandlestickItem(self.data_list)
        self.stringaxis.setTicks([self.xdict.items()])
        self.plt1.getAxis('bottom').setTicks([self.xdict.items()])
        self.plt1.addItem(self.item)
        #self.plt1.showGrid(x=True, y=True)

        self.label = pg.TextItem()  # 创建一个文本项
        self.plt1.addItem(self.label)  # 在图形部件中添加文本项
        self.vLine = pg.InfiniteLine(angle=90, movable=False, )  # 创建一个垂直线条
        self.hLine = pg.InfiniteLine(angle=0, movable=False, )  # 创建一个水平线条
        self.vLine.setPen(0, 0, 0)
        self.hLine.setPen(0, 0, 0)
        self.plt1.plotItem.addItem(self.vLine, ignoreBounds=True)  # 在图形部件中添加垂直线条
        self.plt1.plotItem.addItem(self.hLine, ignoreBounds=True)  # 在图形部件中添加水平线条

#  MACD指标
    def MACD_line(self):
        self.plt3.plotItem.clear()
        self.plt4.plotItem.clear()
        self.plt5.plotItem.clear()

        # MA_Type: 0=SMA, 1=EMA, 2=WMA, 3=DEMA, 4=TEMA, 5=TRIMA, 6=KAMA, 7=MAMA, 8=T3 (Default=SMA)
        DIF, DEA, MACD = talib.MACD(self.Close, 12, 26, 9)


        c = {"DIF": DIF[33:], "DEA": DEA[33:]}
        mydata = pd.DataFrame(c)

        mydata2 = []
        t = 0
        for data, row in mydata.iterrows():
            DIF, DEA = row[:2]
            datas = (t, DIF, DEA)
            mydata2.append(datas)
            t += 1

        a = {'MACD': MACD[33:]}
        macd = pd.DataFrame(a)
        macd = macd.reset_index()
        y = macd['MACD']

        b = []
        for i in range(0, len(y)):
            i += 0
            b.append(i)
        bg1 = pg.BarGraphItem(x=b, height=y, width=1, )
        self.plt3.addItem(bg1)
        item = MacdPaint(mydata2[2:])
        self.plt3.addItem(item)
        self.stringaxis.setTicks([self.xdict.items()])
        self.plt3.getAxis('bottom').setTicks([self.xdict.items()])

        RSI1 = rsiFunc(self.Close.values, 6)
        RSI2 = rsiFunc(self.Close.values, 12)
        RSI3 = rsiFunc(self.Close.values, 24)
        self.plt4.plot(RSI1, pen=(255, 99, 71))
        self.plt4.plot(RSI2, pen=(144, 238, 144))
        self.plt4.plot(RSI3, pen=(205, 201, 201))
        self.stringaxis.setTicks([self.xdict.items()])
        self.plt4.getAxis('bottom').setTicks([self.xdict.items()])

        k, d, j = kdj(self.df1['Low'], self.df1['High'], self.df1['Close'])
        self.plt5.plot(k, pen='r')
        self.plt5.plot(d, pen='b')
        self.plt5.plot(j, pen='y')

    def on_chkBox_jincha_clicked(self):
        self.ui.textEdit.clear()
        jincha = str(self.b)
        self.ui.textEdit.setText(jincha)

    def on_chkbox_sicha_clicked(self):
        self.ui.textEdit.clear()
        sicha = str(self.d)
        self.ui.textEdit.setText(sicha)

    # 鼠标交互事件
    def mousemove1(self, event):
        if event is None:
            print("事件为空")
        else:
            pos = event[0]  # 获取事件的鼠标位置
            try:
                # 如果鼠标位置在绘图部件中
                if self.plt1.sceneBoundingRect().contains(pos):
                    mousePoint = self.plt1.plotItem.vb.mapSceneToView(pos)  # 转换鼠标坐标
                    index = int(mousePoint.x())
                    #print(index)# 鼠标所处的X轴坐标
                    #pos_y = int(mousePoint.y())  # 鼠标所处的Y轴坐标
                    if 0 < index < len(self.df.index):
                        # 在label中写入HTML
                        self.label.setHtml(
                            "<p style='color:white'><strong>日期：{0}</strong></p><p style='color:white'>"
                            "开盘：{1}</p><p style='color:white'>收盘：{2}</p><p style='color:white'>"
                            "最高价：<span style='color:red;'>{3}</span></p><p style='color:white'>"
                            "最低价：<span style='color:green;'>{4}</span></p>".format(self.da[index],
                            self.df['Open'][index], self.df['Close'][index],
                            self.df['High'][index], self.df['Low'][index]))
                        self.label.setPos(mousePoint.x(), mousePoint.y())  # 设置label的位置
                    # 设置垂直线条和水平线条的位置组成十字光标
                        self.vLine.setPos(mousePoint.x())
                        self.hLine.setPos(mousePoint.y())
                        self.vLine.setPen(255, 250, 205)
                        self.hLine.setPen(255, 250, 205)
                    else:
                        self.label.setHtml(None)
                        self.vLine.setPen(0, 0, 0)
                        self.hLine.setPen(0, 0, 0)
            except Exception as e:
                print(traceback.print_exc())

    def mousemove2(self, event):
        if event is None:
            print("事件为空")
        else:
            pos = event[0]  # 获取事件的鼠标位置
            try:
                # 如果鼠标位置在绘图部件中
                if self.plt1.sceneBoundingRect().contains(pos):
                    mousePoint = self.plt1.plotItem.vb.mapSceneToView(pos)  # 转换鼠标坐标
                    index = int(mousePoint.x())
                    # print(index)# 鼠标所处的X轴坐标
                    # pos_y = int(mousePoint.y())  # 鼠标所处的Y轴坐标
                    if 0 < index < len(self.df1.index):
                        # 在label中写入HTML
                        self.label1.setHtml(
                            "<p style='color:white'><strong>日期：{0}</strong></p><p style='color:white'>"
                            "开盘：{1}</p><p style='color:white'>收盘：{2}</p><p style='color:white'>"
                            "最高价：<span style='color:red;'>{3}</span></p><p style='color:white'>"
                            "最低价：<span style='color:green;'>{4}</span></p>".format(self.da1[index],
                                                                                   self.df1['Open'][index],
                                                                                   self.df1['Close'][index],
                                                                                   self.df1['High'][index],
                                                                                   self.df1['Low'][index]))
                        self.label1.setPos(mousePoint.x(), mousePoint.y())  # 设置label的位置
                        # 设置垂直线条和水平线条的位置组成十字光标
                        self.vLine1.setPos(mousePoint.x())
                        self.hLine1.setPos(mousePoint.y())
                        self.vLine1.setPen(255,250,205)
                        self.hLine1.setPen(255, 250, 205)
                    else:
                        self.label1.setHtml(None)
                        self.vLine1.setPen(0, 0, 0)
                        self.hLine1.setPen(0, 0, 0)
            except Exception as e:
                print(traceback.print_exc())

    def mousemove3(self, event):
        if event is None:
            print("事件为空")
        else:
            pos = event[0]  # 获取事件的鼠标位置
            try:
                # 如果鼠标位置在绘图部件中
                if self.plt1.sceneBoundingRect().contains(pos):
                    mousePoint = self.plt1.plotItem.vb.mapSceneToView(pos)  # 转换鼠标坐标
                    index = int(mousePoint.x())
                    # print(index)# 鼠标所处的X轴坐标
                    # pos_y = int(mousePoint.y())  # 鼠标所处的Y轴坐标
                    if 0 < index < len(self.df2.index):
                        # 在label中写入HTML
                        self.label2.setHtml(
                            "<p style='color:white'><strong>日期：{0}</strong></p><p style='color:white'>"
                            "开盘：{1}</p><p style='color:white'>收盘：{2}</p><p style='color:white'>"
                            "最高价：<span style='color:red;'>{3}</span></p><p style='color:white'>"
                            "最低价：<span style='color:green;'>{4}</span></p>".format(self.da2[index],
                                                                                   self.df2['Open'][index],
                                                                                   self.df2['Close'][index],
                                                                                   self.df2['High'][index],
                                                                                   self.df2['Low'][index]))
                        self.label2.setPos(mousePoint.x(), mousePoint.y())  # 设置label的位置
                        # 设置垂直线条和水平线条的位置组成十字光标
                        self.vLine2.setPos(mousePoint.x())
                        self.hLine2.setPos(mousePoint.y())
                        self.vLine2.setPen(255, 250, 205)
                        self.hLine2.setPen(255, 250, 205)
                    else:
                        self.label2.setHtml(None)
                        self.vLine2.setPen(0, 0, 0)
                        self.hLine2.setPen(0, 0, 0)
            except Exception as e:
                print(traceback.print_exc())

    def mousemove4(self, event):
        if event is None:
            print("事件为空")
        else:
            pos = event[0]  # 获取事件的鼠标位置
            try:
                # 如果鼠标位置在绘图部件中
                if self.plt1.sceneBoundingRect().contains(pos):
                    mousePoint = self.plt1.plotItem.vb.mapSceneToView(pos)  # 转换鼠标坐标
                    index = int(mousePoint.x())
                    # print(index)# 鼠标所处的X轴坐标
                    # pos_y = int(mousePoint.y())  # 鼠标所处的Y轴坐标
                    if 0 < index < len(self.df3.index):
                        # 在label中写入HTML
                        self.label3.setHtml(
                            "<p style='color:white'><strong>日期：{0}</strong></p><p style='color:white'>"
                            "开盘：{1}</p><p style='color:white'>收盘：{2}</p><p style='color:white'>"
                            "最高价：<span style='color:red;'>{3}</span></p><p style='color:white'>"
                            "最低价：<span style='color:green;'>{4}</span></p>".format(self.da3[index],
                                                                                   self.df3['Open'][index],
                                                                                   self.df3['Close'][index],
                                                                                   self.df3['High'][index],
                                                                                   self.df3['Low'][index]))
                        self.label3.setPos(mousePoint.x(), mousePoint.y())  # 设置label的位置
                        # 设置垂直线条和水平线条的位置组成十字光标
                        self.vLine3.setPos(mousePoint.x())
                        self.hLine3.setPos(mousePoint.y())
                        self.vLine3.setPen(255, 250, 205)
                        self.hLine3.setPen(255, 250, 205)
                    else:
                        self.label3.setHtml(None)
                        self.vLine3.setPen(0, 0, 0)
                        self.hLine3.setPen(0, 0, 0)
            except Exception as e:
                print(traceback.print_exc())

    @pyqtSlot()
    def on_Selectbtn_2_clicked(self):
        code = self.ui.lineEdit_2.text()
        df = getdata3(code,self.Startdate2,self.Enddate2)
        model = pandasModel(df)
        self.ui.tableView.setModel(model)

        data = getdata3(code,self.Startdate2,self.Enddate2)
        data['涨跌幅'] = data['涨跌幅'].values.astype(np.float)
        close_mean = data['收盘价'].mean()
        open_mean = data['开盘价'].mean()
        high_mean = data['最高价'].mean()
        low_mean = data['最低价'].mean()
        pchg_mean = (data['收盘价'].values[1] - data['收盘价'].values[-1])/data['收盘价'].values[-1]
        turnover_mean = data['换手率'].mean()
        volums_mean = data['成交量'].mean()
        print(pchg_mean)

        self.ui.CloseText.setText("%.10f" %close_mean)
        self.ui.OpenText.setText("%.10f" %open_mean)
        self.ui.HighText.setText("%.10f" %high_mean)
        self.ui.LowText.setText("%.10f" %low_mean)
        self.ui.P_ChgText.setText("%.2f%%" % (pchg_mean * 100))
        self.ui.TurnoverText.setText("%.2f%%" % (turnover_mean * 100))
        self.ui.VolumsText.setText("%.0f" %volums_mean)

    @pyqtSlot()
    def on_pushButton_clicked(self):

        code = self.ui.codeText.text()
        day = self.ui.periodsText.text()
        df = getdata4(code)
        close = df['Close']
        date = df['DataTime']
        name = df['Name'][0]
        data = {"ds": date, "y": close}
        data = pd.DataFrame(data)

        model = fbprophet.Prophet(changepoint_prior_scale=0.05, daily_seasonality=True)
        model.fit(data)
        # print(model)
        forccast_df = model.make_future_dataframe(periods=int(day), freq='D')
        forecast_data = model.predict(forccast_df)
        model.plot(forecast_data, xlabel='Data', ylabel='Close Price')
        plt.show()
        #self.ui.textEdit_3.setText('预测完成')

if __name__=='__main__':
    app = QApplication(sys.argv)
    form = MyWindow()
    form.show()
    sys.exit(app.exec_())