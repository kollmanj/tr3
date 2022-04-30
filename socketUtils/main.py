# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.

#from clientSide import Base
from clientSide import *
from PyQt5 import QtCore, QtGui, QtWidgets
import sys
#from serverSide import Base

def client(name):
    
    app = QtWidgets.QApplication(sys.argv)
    socketClient = QtWidgets.QMainWindow()
    ui = Ui_socketClient()
    ui.setupUi(socketClient)
    socketClient.show()
    sys.exit(app.exec_())
    
    # app = QtWidgets.QApplication(sys.argv)
    # gui = QtWidgets.QMainWindow()
    # ui = Ui_clientSocketGUI()
    # ui.setupUi(gui)
    # gui.show()
    # sys.exit(app.exec_())

    #sc = Base()  # client side test line 1
    #sc.test()    # client side test line 2 End
    
def server(name):  #TODO

    sc = Base()  # client side test line 1
    sc.test()    # client side test line 2 End



# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    client('PyCharm')

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
