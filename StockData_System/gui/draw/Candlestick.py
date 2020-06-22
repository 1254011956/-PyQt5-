# -*- coding: utf-8 -*-
# @Time : 2020/3/15 14:57 
# @Author : 永
# @File : candalist.py 
# @Software: PyCharm


import sys
import importlib
importlib.reload(sys)
# sys.setdefaultencoding('utf-8')
from PyQt5 import QtCore, QtGui


import pyqtgraph as pg


class CandlestickItem(pg.GraphicsObject):
    def __init__(self, data):
        pg.GraphicsObject.__init__(self)
        self.data = data
        self.generatePicture()
    def generatePicture(self):
        self.picture = QtGui.QPicture()
        p = QtGui.QPainter(self.picture)
        p.setPen(pg.mkPen('w'))
        w = (self.data[1][0] - self.data[0][0]) / 3.
        for (t, open, close, min, max, volume) in self.data:
            if open > close:
                p.setPen(pg.mkPen('g'))
                p.setBrush(pg.mkBrush('g'))
            else:
                p.setPen(pg.mkPen('r'))
                p.setBrush(pg.mkBrush('r'))
            p.drawLine(QtCore.QPointF(t, min), QtCore.QPointF(t, max))
            p.drawRect(QtCore.QRectF(t - w, open, w * 2, close - open))
        p.end()
    def paint(self, p, *args):
        p.drawPicture(0, 0, self.picture)
    def boundingRect(self):
        return QtCore.QRectF(self.picture.boundingRect())
