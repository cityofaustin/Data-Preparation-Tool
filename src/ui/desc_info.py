# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'desc_info.ui'
#
# Created by: PyQt5 UI code generator 5.15.4
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_desc_infoWindow(object):
    def setupUi(self, desc_infoWindow):
        desc_infoWindow.setObjectName("desc_infoWindow")
        desc_infoWindow.setWindowModality(QtCore.Qt.ApplicationModal)
        desc_infoWindow.resize(439, 280)
        self.centralwidget = QtWidgets.QWidget(desc_infoWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(self.centralwidget)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.verticalLayout = QtWidgets.QVBoxLayout()
        self.verticalLayout.setObjectName("verticalLayout")
        self.txtInfo = QtWidgets.QTextEdit(self.centralwidget)
        self.txtInfo.setReadOnly(True)
        self.txtInfo.setObjectName("txtInfo")
        self.verticalLayout.addWidget(self.txtInfo)
        self.verticalLayout_2.addLayout(self.verticalLayout)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.btnClose = QtWidgets.QPushButton(self.centralwidget)
        self.btnClose.setObjectName("btnClose")
        self.horizontalLayout.addWidget(self.btnClose)
        self.btnExport = QtWidgets.QPushButton(self.centralwidget)
        self.btnExport.setObjectName("btnExport")
        self.horizontalLayout.addWidget(self.btnExport)
        self.verticalLayout_2.addLayout(self.horizontalLayout)
        desc_infoWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(desc_infoWindow)
        QtCore.QMetaObject.connectSlotsByName(desc_infoWindow)

    def retranslateUi(self, desc_infoWindow):
        _translate = QtCore.QCoreApplication.translate
        desc_infoWindow.setWindowTitle(_translate("desc_infoWindow", "Describe"))
        self.btnClose.setText(_translate("desc_infoWindow", "Close"))
        self.btnExport.setText(_translate("desc_infoWindow", "Export to CSV"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    desc_infoWindow = QtWidgets.QMainWindow()
    ui = Ui_desc_infoWindow()
    ui.setupUi(desc_infoWindow)
    desc_infoWindow.show()
    sys.exit(app.exec_())
