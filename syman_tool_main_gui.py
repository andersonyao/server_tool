# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'syman_tool_main_gui.ui'
#
# Created: Mon May  5 13:06:54 2014
#      by: PyQt4 UI code generator 4.10.4
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    def _fromUtf8(s):
        return s

try:
    _encoding = QtGui.QApplication.UnicodeUTF8
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig, _encoding)
except AttributeError:
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig)

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName(_fromUtf8("MainWindow"))
        MainWindow.resize(800, 600)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(_fromUtf8(":/images/168.ico")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        MainWindow.setWindowIcon(icon)
        self.centralwidget = QtGui.QWidget(MainWindow)
        self.centralwidget.setObjectName(_fromUtf8("centralwidget"))
        self.horizontalLayout = QtGui.QHBoxLayout(self.centralwidget)
        self.horizontalLayout.setSpacing(0)
        self.horizontalLayout.setMargin(0)
        self.horizontalLayout.setObjectName(_fromUtf8("horizontalLayout"))
        self.stackedWidget = QtGui.QStackedWidget(self.centralwidget)
        self.stackedWidget.setObjectName(_fromUtf8("stackedWidget"))
        self.horizontalLayout.addWidget(self.stackedWidget)
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtGui.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 800, 26))
        self.menubar.setObjectName(_fromUtf8("menubar"))
        self.menu_F = QtGui.QMenu(self.menubar)
        self.menu_F.setObjectName(_fromUtf8("menu_F"))
        self.menu_C = QtGui.QMenu(self.menubar)
        self.menu_C.setObjectName(_fromUtf8("menu_C"))
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtGui.QStatusBar(MainWindow)
        self.statusbar.setObjectName(_fromUtf8("statusbar"))
        MainWindow.setStatusBar(self.statusbar)
        self.action_N = QtGui.QAction(MainWindow)
        self.action_N.setObjectName(_fromUtf8("action_N"))
        self.action_O = QtGui.QAction(MainWindow)
        self.action_O.setObjectName(_fromUtf8("action_O"))
        self.action_S = QtGui.QAction(MainWindow)
        self.action_S.setObjectName(_fromUtf8("action_S"))
        self.action_E = QtGui.QAction(MainWindow)
        self.action_E.setObjectName(_fromUtf8("action_E"))
        self.action_L = QtGui.QAction(MainWindow)
        self.action_L.setObjectName(_fromUtf8("action_L"))
        self.action_T = QtGui.QAction(MainWindow)
        self.action_T.setObjectName(_fromUtf8("action_T"))
        self.menu_F.addAction(self.action_N)
        self.menu_F.addAction(self.action_O)
        self.menu_F.addAction(self.action_S)
        self.menu_F.addSeparator()
        self.menu_F.addAction(self.action_E)
        self.menu_C.addAction(self.action_T)
        self.menu_C.addAction(self.action_L)
        self.menubar.addAction(self.menu_F.menuAction())
        self.menubar.addAction(self.menu_C.menuAction())

        self.retranslateUi(MainWindow)
        QtCore.QObject.connect(self.action_N, QtCore.SIGNAL(_fromUtf8("triggered()")), MainWindow.new_create)
        QtCore.QObject.connect(self.action_O, QtCore.SIGNAL(_fromUtf8("triggered()")), MainWindow.old_open)
        QtCore.QObject.connect(self.action_S, QtCore.SIGNAL(_fromUtf8("triggered()")), MainWindow.old_save)
        QtCore.QObject.connect(self.action_E, QtCore.SIGNAL(_fromUtf8("triggered()")), MainWindow.close)
        QtCore.QObject.connect(self.action_L, QtCore.SIGNAL(_fromUtf8("triggered()")), MainWindow.log_check)
        QtCore.QObject.connect(self.action_T, QtCore.SIGNAL(_fromUtf8("triggered()")), MainWindow.main_check)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(_translate("MainWindow", "Bat Shell Tool", None))
        self.menu_F.setTitle(_translate("MainWindow", "文件(F)", None))
        self.menu_C.setTitle(_translate("MainWindow", "查看(C)", None))
        self.action_N.setText(_translate("MainWindow", "新建(N)", None))
        self.action_O.setText(_translate("MainWindow", "打开(O)", None))
        self.action_S.setText(_translate("MainWindow", "保存(S)", None))
        self.action_E.setText(_translate("MainWindow", "退出(E)", None))
        self.action_L.setText(_translate("MainWindow", "日志(L)", None))
        self.action_T.setText(_translate("MainWindow", "工具(T)", None))

import syman_tool_main_source_rc
