# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'server_log_gui.ui'
#
# Created: Mon May  5 13:07:01 2014
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

class Ui_Server_log(object):
    def setupUi(self, Server_log):
        Server_log.setObjectName(_fromUtf8("Server_log"))
        Server_log.resize(800, 555)
        self.main_frame = QtGui.QFrame(Server_log)
        self.main_frame.setGeometry(QtCore.QRect(0, 0, 800, 555))
        self.main_frame.setFrameShape(QtGui.QFrame.StyledPanel)
        self.main_frame.setFrameShadow(QtGui.QFrame.Raised)
        self.main_frame.setObjectName(_fromUtf8("main_frame"))
        self.main_frame_1 = QtGui.QFrame(self.main_frame)
        self.main_frame_1.setGeometry(QtCore.QRect(10, 10, 780, 535))
        self.main_frame_1.setFrameShape(QtGui.QFrame.StyledPanel)
        self.main_frame_1.setFrameShadow(QtGui.QFrame.Raised)
        self.main_frame_1.setObjectName(_fromUtf8("main_frame_1"))
        self.search_date_groupBox = QtGui.QGroupBox(self.main_frame_1)
        self.search_date_groupBox.setGeometry(QtCore.QRect(10, 10, 210, 510))
        self.search_date_groupBox.setObjectName(_fromUtf8("search_date_groupBox"))
        self.search_date_listView = QtGui.QListView(self.search_date_groupBox)
        self.search_date_listView.setGeometry(QtCore.QRect(10, 30, 190, 450))
        self.search_date_listView.setTabKeyNavigation(True)
        self.search_date_listView.setDragEnabled(True)
        self.search_date_listView.setDragDropMode(QtGui.QAbstractItemView.InternalMove)
        self.search_date_listView.setAlternatingRowColors(True)
        self.search_date_listView.setSelectionBehavior(QtGui.QAbstractItemView.SelectRows)
        self.search_date_listView.setObjectName(_fromUtf8("search_date_listView"))
        self.search_date_pushButton_1 = QtGui.QPushButton(self.search_date_groupBox)
        self.search_date_pushButton_1.setGeometry(QtCore.QRect(120, 485, 80, 23))
        self.search_date_pushButton_1.setObjectName(_fromUtf8("search_date_pushButton_1"))
        self.search_result_groupBox = QtGui.QGroupBox(self.main_frame_1)
        self.search_result_groupBox.setGeometry(QtCore.QRect(230, 10, 530, 510))
        self.search_result_groupBox.setObjectName(_fromUtf8("search_result_groupBox"))
        self.search_result_textEdit = QtGui.QTextEdit(self.search_result_groupBox)
        self.search_result_textEdit.setGeometry(QtCore.QRect(10, 30, 520, 475))
        self.search_result_textEdit.setObjectName(_fromUtf8("search_result_textEdit"))

        self.retranslateUi(Server_log)
        QtCore.QObject.connect(self.search_date_pushButton_1, QtCore.SIGNAL(_fromUtf8("clicked()")), Server_log.search_log)
        QtCore.QMetaObject.connectSlotsByName(Server_log)

    def retranslateUi(self, Server_log):
        Server_log.setWindowTitle(_translate("Server_log", "Server_log", None))
        self.search_date_groupBox.setTitle(_translate("Server_log", "选择查询日期", None))
        self.search_date_pushButton_1.setText(_translate("Server_log", "查询", None))
        self.search_result_groupBox.setTitle(_translate("Server_log", "当天日志", None))

