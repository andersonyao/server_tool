#!/usr/bin/env python
#coding=utf8

from PyQt4 import QtGui,QtCore
import sys
from syman_tool_main_gui import Ui_MainWindow
from syman_tool_qwidget import UiServerControlWidget,FaderWidget,UiServerLogWidget


class SymanToolMain(QtGui.QMainWindow):
    def __init__(self,parent = None):
        QtGui.QMainWindow.__init__(self,parent)
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.server_control = UiServerControlWidget(self)
        self.server_log = UiServerLogWidget(self)

        self.ui.stackedWidget.addWidget(self.server_control)
        self.ui.stackedWidget.addWidget(self.server_log)
        self.ui.stackedWidget.setCurrentWidget(self.server_control)
        self.fader_widget = None
        self.connect(self.ui.stackedWidget, QtCore.SIGNAL("currentChanged(int)"),self.fadeInWidget)
        
    def fadeInWidget(self,index):
        self.faderWidget = FaderWidget(self.ui.stackedWidget.widget(index))
        self.faderWidget.start()
        
    def new_create(self):
        pass
    
    def old_open(self):
        pass
    
    def old_save(self):
        pass

    def main_check(self):
        self.ui.stackedWidget.setCurrentWidget(self.server_control)

    def log_check(self):
        self.ui.stackedWidget.setCurrentWidget(self.server_log)

def main():
    app = QtGui.QApplication(sys.argv)
    stm = SymanToolMain()
    stm.show()
    return sys.exit(app.exec_())

if __name__ == "__main__":
    main()
    