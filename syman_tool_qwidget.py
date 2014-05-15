#!/usr/bin/env python
#coding=utf8

from syman_tool_qtablemodel import ServerListTableModel
from server_control_gui import Ui_Server_control
from server_log_gui import Ui_Server_log
from PyQt4 import QtGui,QtCore
from xlutils.copy import copy
import subprocess
import paramiko
import time
import xlrd
import sys
import re
import os


class FaderWidget(QtGui.QWidget):  
    def __init__(self,parent=None):  
        super(FaderWidget,self).__init__(parent)  
        if parent is not None:  
            self.startColor = parent.palette().window().color()  
        else:  
            self.startColor = QtCore.Qt.White  
        self.currentAlpha = 0  
        self.duration = 1000  
        self.timer = QtCore.QTimer(self)  
        self.connect(self.timer,QtCore.SIGNAL("timeout()"),self.update)  
        self.setAttribute(QtCore.Qt.WA_DeleteOnClose)  
        self.resize(parent.size())  
        
    def start(self):  
        self.currentAlpha = 255  
        self.timer.start(100)  
        self.show()  
        
    def paintEvent(self,event):  
        semiTransparentColor = self.startColor  
        semiTransparentColor.setAlpha(self.currentAlpha)  
        painter = QtGui.QPainter(self)  
        painter.fillRect(self.rect(),semiTransparentColor)  
        self.currentAlpha -= (255*self.timer.interval()/self.duration)  
        if self.currentAlpha <= 0:  
            self.timer.stop()  
            self.close()

class MyThread(QtCore.QThread):
    # trigger = QtCore.pyqtSignal(list,QString)
    def __init__(self,parent=None):
        super(MyThread, self).__init__(parent)

    def tran_para(self,item_get1,frame_command_input_1_groupBox_3_tabWidget_1_textEdit_1):
        self.item_get1 = item_get1
        self.frame_command_input_1_groupBox_3_tabWidget_1_textEdit_1 = frame_command_input_1_groupBox_3_tabWidget_1_textEdit_1

    def run(self):
        self.emit(QtCore.SIGNAL("finished(PyQt_PyObject,QString)"),self.item_get1,self.frame_command_input_1_groupBox_3_tabWidget_1_textEdit_1)
    

class UiServerControlWidget(QtGui.QWidget):
    def __init__(self,parent=None):
        super(UiServerControlWidget,self).__init__(parent)
        self.parent = parent
        self.frame_command_input_1_groupBox_3_textEdit_2_text = ''
        self.ui = Ui_Server_control()
        self.ui.setupUi(self)
        self.headers,self.data = self.server_control_list_data_get()
        self.model = ServerListTableModel(self.data,self.headers,self.ui.frame_command_input_1_groupBox_2_tableView_1)
        self.proxy = QtGui.QSortFilterProxyModel(self)
        self.proxy.setSourceModel(self.model)
        self.ui.frame_command_input_1_groupBox_2_tableView_1.setModel(self.proxy)
        # self.ui.frame_command_input_1_groupBox_2_tableView_1.sortByColumn(0, QtCore.Qt.AscendingOrder)
        font = QtGui.QFont("Times New Roman", 10)
        self.ui.frame_command_input_1_groupBox_2_tableView_1.setFont(font)
        # self.ui.frame_command_input_1_groupBox_2_tableView_1.resizeColumnsToContents()
        for i in xrange(len(self.headers)):
            QtGui.qApp.processEvents()
            if i == 0:
                self.ui.frame_command_input_1_groupBox_2_tableView_1.setColumnWidth(i,80)
            elif i == 1:
                self.ui.frame_command_input_1_groupBox_2_tableView_1.setColumnWidth(i,70)
            elif i == 2:
                self.ui.frame_command_input_1_groupBox_2_tableView_1.setColumnWidth(i,60)
        self.total_current_data = self.model.arraydata[:]

        self.data_task = []
        self.model_task = ServerListTableModel(self.data_task,self.headers,self.ui.frame_command_input_1_groupBox_4_tabWidget_1_tableView_1)
        self.proxy_task = QtGui.QSortFilterProxyModel(self)
        self.proxy_task.setSourceModel(self.model_task)
        self.ui.frame_command_input_1_groupBox_4_tabWidget_1_tableView_1.setModel(self.proxy_task)
        font = QtGui.QFont("Times New Roman", 10)
        self.ui.frame_command_input_1_groupBox_4_tabWidget_1_tableView_1.setFont(font)
        for i in xrange(len(self.headers)):
            QtGui.qApp.processEvents()
            if i == 0:
                self.ui.frame_command_input_1_groupBox_4_tabWidget_1_tableView_1.setColumnWidth(i,80)
            elif i == 1:
                self.ui.frame_command_input_1_groupBox_4_tabWidget_1_tableView_1.setColumnWidth(i,40)
            elif i == 2:
                self.ui.frame_command_input_1_groupBox_4_tabWidget_1_tableView_1.setColumnWidth(i,30)
        self.total_current_data_task = self.model_task.arraydata[:]

    def server_control_list_data_get(self):
        headers = ["IP",u"用户名",u"密码"]
        data = [[["192.168.11.10",0],["yy",0],["654321",0]],[["192.168.11.11",0],["xx",0],["111111",0]]]

        # if os.path.exists("/home/yy/py_project/syman_tool/src/syman_tool.xls"):
        #     file = xlrd.open_workbook("/home/yy/py_project/syman_tool/src/syman_tool.xls",'r')
        #     table = file.sheets()[0]
        #     nrows = table.nrows
        #     ncols = table.ncols
        #     data = []
        #     for k in xrange(1,nrows):
        #         data_row = []
        #         for j in xrange(0,ncols):
        #             data_row.append([table.row_values(k)[j],0])
        #         data.append(data_row)

        return headers,data
    
    def add_server_list(self):
        lineEdit_warning_info = ""
        re_judge_string = re.compile("\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}")
        if not self.ui.frame_command_input_1_groupBox_1_lineEdit_1.text():
            lineEdit_warning_info = u'IP地址不能为空！'
        elif not re.findall(re_judge_string,self.ui.frame_command_input_1_groupBox_1_lineEdit_1.text()):
            lineEdit_warning_info = u'IP地址格式不正确！'
        elif not self.ui.frame_command_input_1_groupBox_1_lineEdit_2.text():
            lineEdit_warning_info = u'用户名不能为空！'
        elif len(self.ui.frame_command_input_1_groupBox_1_lineEdit_2.text()) < 2:
            lineEdit_warning_info = u'用户名至少4位！'
        elif not self.ui.frame_command_input_1_groupBox_1_lineEdit_3.text():
            lineEdit_warning_info = u'密码不能为空！'
        elif len(self.ui.frame_command_input_1_groupBox_1_lineEdit_3.text()) < 5:
            lineEdit_warning_info = u'密码至少6位！'
        if lineEdit_warning_info:
            return QtGui.QMessageBox.warning(self.parent, u'警告！',lineEdit_warning_info, QtGui.QMessageBox.NoButton)
        self.model.arraydata.append([[self.ui.frame_command_input_1_groupBox_1_lineEdit_1.text(),0],[self.ui.frame_command_input_1_groupBox_1_lineEdit_2.text(),0],[self.ui.frame_command_input_1_groupBox_1_lineEdit_3.text(),0]])
        self.model.rows = [str(i) for i in xrange(1,len(self.model.arraydata)+1)]
        self.model.reset()

        file = xlrd.open_workbook("/home/yy/py_project/syman_tool/src/syman_tool.xls",formatting_info=True)          
        cp_file = copy(file)                             
        cp_file_add = cp_file.get_sheet(0)
        table = file.sheets()[0]
        nrows = table.nrows
        cp_file_add.write(nrows, 0, unicode(self.ui.frame_command_input_1_groupBox_1_lineEdit_1.text()))
        cp_file_add.write(nrows, 1, unicode(self.ui.frame_command_input_1_groupBox_1_lineEdit_2.text()))
        cp_file_add.write(nrows, 2, unicode(self.ui.frame_command_input_1_groupBox_1_lineEdit_3.text()))  
        cp_file.save("/home/yy/py_project/syman_tool/src/syman_tool.xls")
        
        self.ui.frame_command_input_1_groupBox_1_lineEdit_1.setText("")
        self.ui.frame_command_input_1_groupBox_1_lineEdit_2.setText("")
        self.ui.frame_command_input_1_groupBox_1_lineEdit_3.setText("")
        return QtGui.QMessageBox.information(self.parent, u'提示！',u'新服务器信息成功加入服务器列表！', QtGui.QMessageBox.NoButton)
    
    def delete_choose(self):
        item_get = self.ui.frame_command_input_1_groupBox_2_tableView_1.selectedIndexes()
        if item_get:
            temp_row = 0
            exists_flag = 0
            if len(self.model.arraydata):
                for acl_row in xrange(len(self.model.arraydata)):
                    if self.model.data(self.ui.frame_command_input_1_groupBox_2_tableView_1.selectedIndexes()[0], role = QtCore.Qt.DisplayRole).toString() == QtCore.QString(self.model.arraydata[acl_row][0][0]):
                        exists_flag = 1
                        temp_row = acl_row
                        break
                if exists_flag == 1:
                    self.model.arraydata.pop(temp_row)
                    self.model.rows = [str(i) for i in xrange(1,len(self.model.arraydata)+1)]
                    self.model.reset()

                file = xlrd.open_workbook("/home/yy/py_project/syman_tool/src/syman_tool.xls",formatting_info=True)          
                cp_file = copy(file)                             
                cp_file_add = cp_file.get_sheet(0)
                table = file.sheets()[0]
                nrows = table.nrows
                ncols = table.ncols
                for row in xrange(nrows):
                    for ncol in xrange(ncols):
                        cp_file_add.write(row+1, ncol, "")
                for row in xrange(len(self.model.arraydata)):
                    cp_file_add.write(row+1, 0, unicode(self.model.arraydata[row][0][0]))
                    cp_file_add.write(row+1, 1, unicode(self.model.arraydata[row][1][0]))
                    cp_file_add.write(row+1, 2, unicode(self.model.arraydata[row][2][0])) 
                cp_file.save("/home/yy/py_project/syman_tool/src/syman_tool.xls")

            return QtGui.QMessageBox.information(self.parent, u'提示！',u'被选中服务器数据已成功被删除！', QtGui.QMessageBox.NoButton)
        else:
            return QtGui.QMessageBox.warning(self.parent, u'警告！',u'您没选中任何服务器，请选中后再点击删除选中按钮！', QtGui.QMessageBox.NoButton)
        
    def add_task(self):
        item_get = self.ui.frame_command_input_1_groupBox_2_tableView_1.selectedIndexes()
        if len(item_get) == 3:
            self.ui.frame_command_input_1_groupBox_4_lineEdit_1.setText(self.model.data(self.ui.frame_command_input_1_groupBox_2_tableView_1.selectedIndexes()[0], role = QtCore.Qt.DisplayRole).toString())
            self.ui.frame_command_input_1_groupBox_4_lineEdit_2.setText(self.model.data(self.ui.frame_command_input_1_groupBox_2_tableView_1.selectedIndexes()[1], role = QtCore.Qt.DisplayRole).toString())
            self.ui.frame_command_input_1_groupBox_4_lineEdit_3.setText(self.model.data(self.ui.frame_command_input_1_groupBox_2_tableView_1.selectedIndexes()[2], role = QtCore.Qt.DisplayRole).toString())
            self.model_task.arraydata = []
            self.model_task.rows = [str(i) for i in xrange(1,len(self.model_task.arraydata)+1)]
            self.model_task.reset()
            self.ui.frame_command_input_1_groupBox_4_tabWidget_1.setCurrentIndex(0)
            return QtGui.QMessageBox.information(self.parent, u'提示！',u'被选中单服务器数据已成功导入任务创建栏的选择单服务器栏中！', QtGui.QMessageBox.NoButton)
        elif len(item_get) > 3:
            for n in xrange(0,len(item_get),3):
                self.model_task.arraydata.append([[self.model.data(self.ui.frame_command_input_1_groupBox_2_tableView_1.selectedIndexes()[n], role = QtCore.Qt.DisplayRole),0],[self.model.data(self.ui.frame_command_input_1_groupBox_2_tableView_1.selectedIndexes()[n+1], role = QtCore.Qt.DisplayRole),0],[self.model.data(self.ui.frame_command_input_1_groupBox_2_tableView_1.selectedIndexes()[n+2], role = QtCore.Qt.DisplayRole),0]])
            self.model_task.rows = [str(i) for i in xrange(1,len(self.model_task.arraydata)+1)]
            self.model_task.reset()
            self.ui.frame_command_input_1_groupBox_4_lineEdit_1.setText("")
            self.ui.frame_command_input_1_groupBox_4_lineEdit_2.setText("")
            self.ui.frame_command_input_1_groupBox_4_lineEdit_3.setText("")
            self.ui.frame_command_input_1_groupBox_4_tabWidget_1.setCurrentIndex(1)
            return QtGui.QMessageBox.information(self.parent, u'提示！',u'被选中多服务器数据已成功导入任务创建栏的选择多服务器栏中！', QtGui.QMessageBox.NoButton)
        else:
            return QtGui.QMessageBox.warning(self.parent, u'警告！',u'您没选中任何服务器，请选中后再点击加入任务按钮！', QtGui.QMessageBox.NoButton)  
    
    def task_run_1(self):
        frame_command_input_1_groupBox_3_tabWidget_1_textEdit_2 = self.ui.frame_command_input_1_groupBox_3_tabWidget_1_textEdit_2.toPlainText()
        # frame_command_input_1_groupBox_4_lineEdit_1 = self.ui.frame_command_input_1_groupBox_4_lineEdit_1.text()
        # frame_command_input_1_groupBox_4_lineEdit_2 = self.ui.frame_command_input_1_groupBox_4_lineEdit_2.text()
        # frame_command_input_1_groupBox_4_lineEdit_3 = self.ui.frame_command_input_1_groupBox_4_lineEdit_3.text()
        if frame_command_input_1_groupBox_3_tabWidget_1_textEdit_2:
            self.frame_command_input_1_groupBox_3_textEdit_2_text = u"没有找到任何脚本"
            file_path,ext = os.path.splitext(unicode(frame_command_input_1_groupBox_3_tabWidget_1_textEdit_2))
            file_path_split = os.path.split(file_path)
            if file_path_split[1] == 'fabfile':
                cmd = "cd %s;fab deploy;"%(file_path_split[0])
                p_1 = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
                if p_1.stderr is not None:
                    return QtGui.QMessageBox.warning(self.parent, u'警告！',u'网络异常，请先检查网络连接！')
                else:
                    self.frame_command_input_1_groupBox_3_textEdit_2_text = p_1.stdout.read()
                self.ui.frame_command_input_1_groupBox_3_tabWidget_1_textEdit_2.setText("")

            self.ui.frame_command_input_1_groupBox_3_textEdit_2.setText(self.frame_command_input_1_groupBox_3_textEdit_2_text.decode('utf8'))
            self.add_log(self.frame_command_input_1_groupBox_3_textEdit_2_text)
            self.frame_command_input_1_groupBox_3_textEdit_2_text = ''
            return QtGui.QMessageBox.information(self.parent, u'提示！',u'已经在服务器上执行该脚本！', QtGui.QMessageBox.NoButton)
        else:
            return QtGui.QMessageBox.warning(self.parent, u'警告！',u'需要执行的任务输入框不为空！', QtGui.QMessageBox.NoButton)

    def task_run_2(self):
        frame_command_input_1_groupBox_3_tabWidget_1_textEdit_1 = self.ui.frame_command_input_1_groupBox_3_tabWidget_1_textEdit_1.toPlainText()
        frame_command_input_1_groupBox_4_lineEdit_1 = self.ui.frame_command_input_1_groupBox_4_lineEdit_1.text()
        frame_command_input_1_groupBox_4_lineEdit_2 = self.ui.frame_command_input_1_groupBox_4_lineEdit_2.text()
        frame_command_input_1_groupBox_4_lineEdit_3 = self.ui.frame_command_input_1_groupBox_4_lineEdit_3.text()
        if frame_command_input_1_groupBox_3_tabWidget_1_textEdit_1:
            cmd_list = unicode(frame_command_input_1_groupBox_3_tabWidget_1_textEdit_1).split("\n")
            self.frame_command_input_1_groupBox_3_textEdit_2_text = ""
            self.frame_command_input_1_groupBox_3_textEdit_2_text_temp = []
            item_get = self.ui.frame_command_input_1_groupBox_4_tabWidget_1_tableView_1.selectedIndexes()
            if frame_command_input_1_groupBox_4_lineEdit_1:
                selected_ipaddress = frame_command_input_1_groupBox_4_lineEdit_1
                ssh = paramiko.SSHClient()
                ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
                ssh.load_system_host_keys()
                # ssh.set_missing_host_key_policy(paramiko.MissingHostKeyPolicy())
                try:
                    ssh.connect(unicode(frame_command_input_1_groupBox_4_lineEdit_1),username = unicode(frame_command_input_1_groupBox_4_lineEdit_2), password = unicode(frame_command_input_1_groupBox_4_lineEdit_3))      
                except Exception,e:
                    ssh.close()
                    return QtGui.QMessageBox.warning(self.parent, u'警告！',u'网络异常，请先检查网络连接！')
                i = 0
                for cmd in cmd_list:
                    stdin,stdout,stderr = ssh.exec_command(cmd)
                    if cmd:
                        i += 1
                        self.frame_command_input_1_groupBox_3_textEdit_2_text_temp.append("***********Command %d************\n"%i+stdout.read())
                self.frame_command_input_1_groupBox_3_textEdit_2_text = "".join(self.frame_command_input_1_groupBox_3_textEdit_2_text_temp)
                self.ui.frame_command_input_1_groupBox_3_tabWidget_1_textEdit_1.setText("")
                self.ui.frame_command_input_1_groupBox_3_textEdit_2.setText(self.frame_command_input_1_groupBox_3_textEdit_2_text.decode('utf8'))
                ssh.close()

            elif item_get:
                # self.threads = []
                for n in xrange(0,len(item_get),3):
                    thread = MyThread(self)
                    self.connect(thread, QtCore.SIGNAL("finished(PyQt_PyObject,QString)"), self.ssh_execu)
                    # self.threads.append(thread)
                    thread.tran_para(item_get[n:n+3],frame_command_input_1_groupBox_3_tabWidget_1_textEdit_1)
                    thread.start()
                    selected_ipaddress = unicode(self.model.data(self.ui.frame_command_input_1_groupBox_2_tableView_1.selectedIndexes()[n], role = QtCore.Qt.DisplayRole).toString())

                # for n in xrange(0,len(item_get),3):
                #     affair=threading.Thread(target=self.ssh_execu,args=(n,cmd_list))
                #     affair.start()
                #     threads.append(affair)
                # for m in xrange(0,len(item_get),3):
                #     threads[m].start()
                # for o in xrange(0,len(item_get),3):
                #     threads[o].join()

                self.ui.frame_command_input_1_groupBox_3_tabWidget_1_textEdit_1.setText("")

            elif not item_get:
                return QtGui.QMessageBox.warning(self.parent, u'警告！',u'请选择多服务器栏选项！', QtGui.QMessageBox.NoButton)       

            # channel = ssh.invoke_shell()
            # for cmd in cmd_list:
            #     time.sleep(2)
            #     print "cmd:",cmd
            #     channel.send(cmd+'\n')
            #     out = channel.recv(1024)
            #     print "out:",out

            # stdin.write('lol\n')
            # stdin.flush() sudo时填写密码
            
            self.add_log(self.frame_command_input_1_groupBox_3_textEdit_2_text)
            self.frame_command_input_1_groupBox_3_textEdit_2_text = ''
            return QtGui.QMessageBox.information(self.parent, u'提示！',u'已经在服务器(%s)上执行该脚本！'%selected_ipaddress, QtGui.QMessageBox.NoButton)
        else:
            return QtGui.QMessageBox.warning(self.parent, u'警告！',u'需要执行的任务输入框不为空！', QtGui.QMessageBox.NoButton)

    def ssh_execu(self,item_get1,frame_command_input_1_groupBox_3_tabWidget_1_textEdit_1):
        cmd_list = unicode(frame_command_input_1_groupBox_3_tabWidget_1_textEdit_1).split("\n")
        try:
            ssh = paramiko.SSHClient()
            ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            ssh.load_system_host_keys()
            ssh.set_missing_host_key_policy(paramiko.MissingHostKeyPolicy())

            ssh.connect(unicode(self.model_task.data(item_get1[0], role = QtCore.Qt.DisplayRole).toString()),username = unicode(self.model_task.data(item_get1[1], role = QtCore.Qt.DisplayRole).toString()), password = unicode(self.model_task.data(item_get1[2], role = QtCore.Qt.DisplayRole).toString()))
            i = 0
            for cmd in cmd_list:
                stdin,stdout,stderr = ssh.exec_command(cmd)
                if cmd:
                    i += 1
                    output = stdout.read()
                    self.frame_command_input_1_groupBox_3_textEdit_2_text_temp.append("***********Command %d on IP:%s************\n"%(i,unicode(self.model_task.data(item_get1[0], role = QtCore.Qt.DisplayRole).toString()).encode('utf8'))+output)
            self.frame_command_input_1_groupBox_3_textEdit_2_text = "".join(self.frame_command_input_1_groupBox_3_textEdit_2_text_temp)
            ssh.close()
        except Exception,e:
            s = sys.exc_info()
            print "Error '%s' happened on line %d" % (s[1],s[2].tb_lineno)
            return QtGui.QMessageBox.warning(self.parent, u'警告！',u'网络异常，请先检查网络连接！')
        self.ui.frame_command_input_1_groupBox_3_textEdit_2.setText(self.frame_command_input_1_groupBox_3_textEdit_2_text.decode('utf8'))
    
    def add_log(self,input_text):
        current_time = time.strftime("%Y_%m_%d_%H_%M",time.localtime(time.time()))
        with open("log/%s_log.txt"%current_time,"a") as log_file:
            data = log_file.write(input_text)

    def task_read(self):
        dlg2 = QtGui.QFileDialog()
        upload_script = dlg2.getOpenFileName(self,u"请选择打开脚本的路径", os.getcwd(), "text files (*.txt)")
        if not upload_script:
            QtGui.QMessageBox.warning(self.parent, u'警告！',u'您没有选择正确的脚本打开路径，请重新选择！', QtGui.QMessageBox.NoButton)
        else:
            file_open = open(upload_script,"r")
            script_text = file_open.read()
            file_open.close()
            self.ui.frame_command_input_1_groupBox_3_tabWidget_1_textEdit_1.setText(script_text)

    def task_save(self):
        frame_command_input_1_groupBox_3_tabWidget_1_textEdit_1 = self.ui.frame_command_input_1_groupBox_3_tabWidget_1_textEdit_1.toPlainText()
        frame_command_input_1_groupBox_3_textEdit_1_end = ""
        frame_command_input_1_groupBox_3_textEdit_1_end_temp = []
        for item in unicode(frame_command_input_1_groupBox_3_tabWidget_1_textEdit_1).split("\n"):
            if item:
                frame_command_input_1_groupBox_3_textEdit_1_end_temp.append(item + "\n")
        frame_command_input_1_groupBox_3_textEdit_1_end = "".join(frame_command_input_1_groupBox_3_textEdit_1_end_temp)
        dlg1 = QtGui.QFileDialog()
        download_script = dlg1.getSaveFileName(self,u"请选择保存脚本的路径", os.getcwd(),"text files (*.txt)")
        if not download_script:
            QtGui.QMessageBox.warning(self.parent, u'警告！',u'您没有选择正确的脚本保存路径，请重新选择！', QtGui.QMessageBox.NoButton)
        else:
            download_script = unicode(download_script)
            if not download_script.endswith(".txt"):
                download_script = download_script+".txt"
            file_save = open(download_script,"w")
            file_save.write(frame_command_input_1_groupBox_3_textEdit_1_end)
            file_save.close()


class UiServerLogWidget(QtGui.QWidget):
    def __init__(self,parent=None):
        super(UiServerLogWidget,self).__init__(parent)
        self.parent = parent
        self.ui = Ui_Server_log()
        self.ui.setupUi(self)
        # listWidget.insertItem(0,self.tr("窗口1"))



    def search_log(self):
         pass 



    
        
    
        
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    

