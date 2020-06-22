import sys
import importlib
importlib.reload(sys)
# sys.setdefaultencoding('utf-8')
from PyQt5 import QtCore, QtGui


import pyqtgraph as pg


class MacdPaint(pg.GraphicsObject):
    def __init__(self, data):
        pg.GraphicsObject.__init__(self)
        self.data = data
        self.generatePicture()

    def generatePicture(self):
        self.picture = QtGui.QPicture()
        p = QtGui.QPainter(self.picture)
        p.setPen(pg.mkPen('w'))
        w = (self.data[1][0] - self.data[0][0]) / 3.

        dif = 0
        dea = 0

        for (t, DIF, DEA) in self.data:


            if dif != 0:
                p.setPen(pg.mkPen('r'))
                p.setBrush(pg.mkBrush('r'))
                p.drawLine(QtCore.QPointF(t-1, dif), QtCore.QPointF(t, DIF))
            dif = DIF
            if dea != 0:
                p.setPen(pg.mkPen('b'))
                p.setBrush(pg.mkBrush('b'))
                p.drawLine(QtCore.QPointF(t-1, dea), QtCore.QPointF(t, DEA))
            dea = DEA
            '''if EMA20 != 0:
                p.setPen(pg.mkPen('m'))
                p.setBrush(pg.mkBrush('m'))
                p.drawLine(QtCore.QPointF(t-1, EMA20), QtCore.QPointF(t, ma20))
            EMA20 = ma20'''
        p.end()

    def paint(self, p, *args):
        p.drawPicture(0, 0, self.picture)

    def boundingRect(self):
        return QtCore.QRectF(self.picture.boundingRect())