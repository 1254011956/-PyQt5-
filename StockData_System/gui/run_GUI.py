# -*- coding: utf-8 -*-
# @Time : 2020/4/10 0:52
# @Author : 永
# @File : run_GUI.py
# @Software: PyCharm

import sys,os
from PyQt5.QtWidgets import QApplication,QMainWindow
from gui.ui.Qmywindow import MyWindow

if __name__=='__main__':
    app =QApplication(sys.argv)
    form = MyWindow()
    form.show()
    sys.exit(app.exec_())




