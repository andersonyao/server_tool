#!/user/bin/env python
#coding=utf8

from PyQt4 import QtCore
from PyQt4 import QtGui
# from datetime import datetime
# from HRMS_DB_Tables import UserInfo,Session


class ServerListTableModel(QtCore.QAbstractTableModel):
    def __init__(self, data,headers,parent=None):
        super(ServerListTableModel, self).__init__(parent)
        self.parent=parent
        self.arraydata = data
        self.headers=headers
        self.rows=[str(i) for i in xrange(1,len(self.arraydata)+1)]
        
    def rowCount(self, parent=QtCore.QModelIndex()):
        return len(self.arraydata)

    def columnCount(self, parent=QtCore.QModelIndex()):
        if not self.arraydata:
            return 0
        return len(self.arraydata[0])
    
    def data(self, index, role=QtCore.Qt.DisplayRole):
        if not index.isValid():
            return QtCore.QVariant()
        else:
            row = index.row()
            column = index.column()
            if role != QtCore.Qt.DisplayRole and role != QtCore.Qt.EditRole and role != QtCore.Qt.BackgroundRole and role != QtCore.Qt.ItemDataRole:
                return QtCore.QVariant()
            if role == QtCore.Qt.BackgroundRole:
                if self.arraydata[row][column][1]==2:
                    return QtGui.QBrush(QtCore.Qt.yellow)
                elif self.arraydata[row][column][1]==1:
                    return QtGui.QBrush(QtCore.Qt.green)
                elif self.arraydata[row][column][1]==3:
                    return QtGui.QBrush(QtCore.Qt.lightGray)
            if role==QtCore.Qt.DisplayRole or role==QtCore.Qt.EditRole:
                return QtCore.QVariant(self.arraydata[row][column][0])
     
    def headerData(self, section, orientation, role):
        if role == QtCore.Qt.DisplayRole:
            if orientation == QtCore.Qt.Horizontal:
                return QtCore.QString(self.headers[section])
            else:
                return QtCore.QString(self.rows[section])
        if role == QtCore.Qt.ToolTipRole:
            if orientation == QtCore.Qt.Horizontal:
                return QtCore.QString("Horizontal Header: %s" % self.headers[section])
            else:
                return QtCore.QString("Vertical Header: %s" % self.arraydata[section][1][0])
             
    def flags(self, index):
#         if index.column() == 0:
#             return QtCore.Qt.ItemIsEnabled | QtCore.Qt.ItemIsSelectable
        return QtCore.Qt.ItemIsEnabled | QtCore.Qt.ItemIsEditable | QtCore.Qt.ItemIsSelectable
     
    def setData(self, index, value, role = QtCore.Qt.EditRole):
        if role == QtCore.Qt.EditRole:
            row = index.row()
            column = index.column()
            if self.arraydata[row][column][0]!=value:
                self.arraydata[row][column][1]=1
                self.arraydata[row][column][0]=value.toString()
#                 session= Session()
#                 if column==4:
#                     try:
#                         datetime.strptime(unicode(self.arraydata[row][column][0]),"%Y-%m-%d")                        
#                         session.query(UserInfo).filter_by(uid=self.arraydata[row][0][0]).update({'%s'%self.headers[column]:datetime.strptime(unicode(self.arraydata[row][column][0]),"%Y-%m-%d")})
#                     except:
#                         QtGui.QMessageBox.information(self.parent, u'警告！',u'您填写的日期格式错误，请重新按照（%Y-%m-%d）格式填写，否则会导致此项数据更新失败。', QtGui.QMessageBox.NoButton)
#                 else:
#                     session.query(UserInfo).filter_by(uid=self.arraydata[row][0][0]).update({'%s'%self.headers[column]:unicode(self.arraydata[row][column][0])})
#                 session.commit()
#                 session.close()
            else:
                self.arraydata[row][column][1]=2
            return True






