# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'socketClient.ui'
#
# Created by: PyQt5 UI code generator 5.9.2
#
# WARNING! All changes made in this file will be lost!

# Avoid
# "attempted relative import with no known parent package"
import os
import sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from clientSide import Base

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_socketClient(object):
    def setupUi(self, socketClient):
        socketClient.setObjectName("socketClient")
        socketClient.resize(266, 162)
        self.centralwidget = QtWidgets.QWidget(socketClient)
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
        socketClient.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(socketClient)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 266, 20))
        self.menubar.setObjectName("menubar")
        socketClient.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(socketClient)
        self.statusbar.setObjectName("statusbar")
        socketClient.setStatusBar(self.statusbar)

        self.startButton.clicked.connect(self.startPressed)

        self.retranslateUi(socketClient)
        QtCore.QMetaObject.connectSlotsByName(socketClient)

    def startPressed(self):
        appToRun = self.comboBoxApp.currentText()
        # ipaddressString = self.ipAddressLineEdit.
        if appToRun == 'test':
            ipaddressString = self.ipAddressLineEdit.text()
            portNumberString = self.portLineEdit_2.text()
            a = Base(ipaddressString, int(portNumberString))
            print('test')
            a.test()
        else:
            print('Plot')

    def retranslateUi(self, socketClient):
        _translate = QtCore.QCoreApplication.translate
        socketClient.setWindowTitle(_translate("socketClient", "MainWindow"))
        self.startButton.setText(_translate("socketClient", "Start"))
        self.ipAddressLineEdit.setText(_translate("socketClient", "10.0.0.187"))
        self.label.setText(_translate("socketClient", "Port Number"))
        self.label_2.setText(_translate("socketClient", "IP Address"))
        self.stopButton.setText(_translate("socketClient", "Stop"))
        self.portLineEdit_2.setText(_translate("socketClient", "1234"))
        self.comboBoxApp.setItemText(0, _translate("socketClient", "test"))
        self.comboBoxApp.setItemText(1, _translate("socketClient", "plotter"))

if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    socketClient = QtWidgets.QMainWindow()
    ui = Ui_socketClient()
    ui.setupUi(socketClient)
    socketClient.show()
    sys.exit(app.exec_())
