# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file '.\socketClient.ui'
#
# Created by: PyQt5 UI code generator 5.9.2
#
# WARNING! All changes made in this file will be lost!
from PyQt5 import QtCore, QtGui, QtWidgets

# Avoid
# "attempted relative import with no known parent package"
import os
import sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from serverSide import Base


class Ui_socketServer(object):
    def setupUi(self, sockeServer):
        sockeServer.setObjectName("socketServer")
        sockeServer.resize(266, 162)
        self.centralwidget = QtWidgets.QWidget(sockeServer)
        self.centralwidget.setObjectName("centralwidget")
        self.startButton = QtWidgets.QPushButton(self.centralwidget)
        self.startButton.setGeometry(QtCore.QRect(110, 80, 75, 23))
        self.startButton.setObjectName("startButton")
        self.ipAddressLineEdit = QtWidgets.QLineEdit(self.centralwidget)
        self.ipAddressLineEdit.setGeometry(QtCore.QRect(80, 40, 61, 20))
        self.ipAddressLineEdit.setObjectName("ipAddressLineEdit")
        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setGeometry(QtCore.QRect(10, 10, 71, 16))
        self.label.setObjectName("label")
        self.label_2 = QtWidgets.QLabel(self.centralwidget)
        self.label_2.setGeometry(QtCore.QRect(10, 40, 61, 16))
        self.label_2.setObjectName("label_2")
        self.stopButton = QtWidgets.QPushButton(self.centralwidget)
        self.stopButton.setGeometry(QtCore.QRect(10, 80, 75, 23))
        self.stopButton.setObjectName("stopButton")
        self.portLineEdit_2 = QtWidgets.QLineEdit(self.centralwidget)
        self.portLineEdit_2.setGeometry(QtCore.QRect(80, 10, 61, 20))
        self.portLineEdit_2.setObjectName("portLineEdit_2")
        self.comboBoxApp = QtWidgets.QComboBox(self.centralwidget)
        self.comboBoxApp.setGeometry(QtCore.QRect(160, 10, 69, 22))
        self.comboBoxApp.setObjectName("comboBoxApp")
        self.comboBoxApp.addItem("")
        self.comboBoxApp.addItem("")
        sockeServer.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(sockeServer)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 266, 21))
        self.menubar.setObjectName("menubar")
        sockeServer.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(sockeServer)
        self.statusbar.setObjectName("statusbar")
        sockeServer.setStatusBar(self.statusbar)
        
        self.startButton.clicked.connect(self.startPressed)

        self.retranslateUi(sockeServer)
        QtCore.QMetaObject.connectSlotsByName(sockeServer)
        
    def startPressed(self):
        appToRun = self.comboBoxApp.currentText()
        #ipaddressString = self.ipAddressLineEdit.
        if appToRun == 'test':
            a = Base('10.0.0.187',1234)
            print('test')
            a.test()
        else:
            print('Plot')
        

    def retranslateUi(self, sockeServer):
        _translate = QtCore.QCoreApplication.translate
        sockeServer.setWindowTitle(_translate("sockeServer", "MainWindow"))
        self.startButton.setText(_translate("sockeServer", "Start"))
        self.ipAddressLineEdit.setText(_translate("sockeServer", "10.0.0.187"))
        self.label.setText(_translate("sockeServer", "Port Number"))
        self.label_2.setText(_translate("sockeServer", "IP Address"))
        self.stopButton.setText(_translate("sockeServer", "Stop"))
        self.portLineEdit_2.setText(_translate("sockeServer", "1234"))
        self.comboBoxApp.setItemText(0, _translate("sockeServer", "plotter"))
        self.comboBoxApp.setItemText(1, _translate("sockeServer", "test"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    sockeServer = QtWidgets.QMainWindow()
    ui = Ui_socketServer()
    ui.setupUi(sockeServer)
    sockeServer.show()
    sys.exit(app.exec_())

