import sys
from PyQt5 import QtCore, QtGui, QtWidgets

import socket
from _thread import *

from PyQt5.QtWidgets import QLineEdit, QTextEdit

HOST = '0.0.0.0'
PORT = 50100
serversocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
serversocket.bind((HOST, PORT))
serversocket.listen(5)

start_test = False
temperature_test = False

temperature = 0


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):

        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(1280, 768)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")

        self.line = QtWidgets.QFrame(self.centralwidget)
        self.line.setGeometry(QtCore.QRect(0, 550, 1281, 21))
        self.line.setFrameShape(QtWidgets.QFrame.HLine)
        self.line.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line.setObjectName("line")

        self.line_2 = QtWidgets.QFrame(self.centralwidget)
        self.line_2.setGeometry(QtCore.QRect(630, 0, 20, 561))
        self.line_2.setFrameShape(QtWidgets.QFrame.VLine)
        self.line_2.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line_2.setObjectName("line_2")

        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setGeometry(QtCore.QRect(700, 60, 60, 31))
        self.label.setObjectName("label")

        self.checkBox = QtWidgets.QCheckBox(self.centralwidget)
        self.checkBox.setGeometry(QtCore.QRect(700, 90, 201, 41))
        self.checkBox.setObjectName("checkBox")
        self.checkBox.stateChanged.connect(self.temperature_test_status)

        self.checkBox_2 = QtWidgets.QCheckBox(self.centralwidget)
        self.checkBox_2.setGeometry(QtCore.QRect(700, 140, 201, 41))
        self.checkBox_2.setObjectName("checkBox_2")

        self.checkBox_3 = QtWidgets.QCheckBox(self.centralwidget)
        self.checkBox_3.setGeometry(QtCore.QRect(700, 200, 201, 41))
        self.checkBox_3.setObjectName("checkBox_3")

        self.progressBar = QtWidgets.QProgressBar(self.centralwidget)
        self.progressBar.setGeometry(QtCore.QRect(690, 390, 571, 23))
        self.progressBar.setProperty("value", 24)
        self.progressBar.setObjectName("progressBar")

        self.pushButton = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton.setGeometry(QtCore.QRect(770, 480, 130, 40))
        self.pushButton.setObjectName("pushButton")
        self.pushButton.clicked.connect(self.start)

        self.pushButton_2 = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_2.setGeometry(QtCore.QRect(1020, 480, 130, 40))
        self.pushButton_2.setObjectName("pushButton_2")
        self.pushButton_2.setEnabled(False)
        self.pushButton_2.clicked.connect(self.stop)

        self.textbox = QTextEdit(self.centralwidget)
        self.textbox.move(10, 570)
        self.textbox.resize(1260, 150)
        self.textbox.setReadOnly(True)

        MainWindow.setCentralWidget(self.centralwidget)

        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 1280, 21))
        self.menubar.setObjectName("menubar")

        self.menu_Exit = QtWidgets.QMenu(self.menubar)
        self.menu_Exit.setObjectName("menu_Exit")

        self.menuHelp = QtWidgets.QMenu(self.menubar)
        self.menuHelp.setObjectName("menuHelp")
        MainWindow.setMenuBar(self.menubar)

        self.menubar.addAction(self.menuHelp.menuAction())
        self.menubar.addAction(self.menu_Exit.menuAction())

        self.retranslateUi(MainWindow)
        MainWindow.setStatusBar(self.statusbar)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)
        MainWindow.show()

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.checkBox.setText(_translate("MainWindow", "Temperature test ( H Bridge, Motor )"))
        self.label.setText(_translate("MainWindow", "Test cases:"))
        self.checkBox_2.setText(_translate("MainWindow", "Voltage test (  Supply )"))
        self.checkBox_3.setText(_translate("MainWindow", "Motor speed"))
        self.pushButton.setText(_translate("MainWindow", "Start test"))
        self.pushButton_2.setText(_translate("MainWindow", "Stop test"))
        self.menu_Exit.setTitle(_translate("MainWindow", "&Exit"))
        self.menuHelp.setTitle(_translate("MainWindow", "Help"))

    def temperature_test_status(self, state):
        global temperature_test
        if state == QtCore.Qt.Checked:
            temperature_test = True
        else:
            temperature_test = False
        print(temperature_test)

    def start(self):
        global start_test
        self.textbox.setPlainText(self.textbox.toPlainText() + '\n' + "Test started!")
        self.pushButton.setEnabled(False)
        self.pushButton_2.setEnabled(True)
        start_test = True

    def stop(self):
        global start_test
        self.textbox.setPlainText(self.textbox.toPlainText() + '\n' + "Test stoped!")
        self.pushButton.setEnabled(True)
        self.pushButton_2.setEnabled(False)
        start_test = False


class MyWindow(QtWidgets.QMainWindow):
    def closeEvent(self, event):
        result = QtWidgets.QMessageBox.question(self,
                                                "Confirm Exit",
                                                "Are you sure you want to exit ?",
                                                QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No)

        if result == QtWidgets.QMessageBox.Yes:
            event.accept()

        elif result == QtWidgets.QMessageBox.No:
            event.ignore()

    def center(self):
        frameGm = self.frameGeometry()
        screen = QtWidgets.QApplication.desktop().screenNumber(QtWidgets.QApplication.desktop().cursor().pos())
        centerPoint = QtWidgets.QApplication.desktop().screenGeometry(screen).center()
        frameGm.moveCenter(centerPoint)
        self.move(frameGm.topLeft())


# Server
def fun(clientsocket, address):
    global ui
    global temperature, temperature_test, start_test
    print('Connected by', address)
    while True:
        if start_test:
            if temperature_test:
                clientsocket.sendall('a'.encode())
                print("Temperature test")
                try:
                    data = clientsocket.recv(1024)
                    if not data:
                        break
                    try:
                        temperature = float(data.decode())
                    except:
                        pass
                    print('Temperature: ', temperature)
                except:
                    print('Disconnected!')
                    return
            if temperature > 30:
                print("Test failed! Temperature higher than 30. Temperature = " + str(temperature))
               # ui.textbox.setPlainText(ui.textbox.toPlainText() + '\n' + "Test failed! Temperature higher than 30. " +
             #                                                             "Temperature = " + str(temperature))
                start_test = False
                clientsocket.sendall('x'.encode())

    clientsocket.close()
    print('S-a terminat comunicarea cu ', address)


def run_server():
    while True:
        print('#########################################################################')
        print('Serverul asculta potentiali clienti.')
        print('#########################################################################')
        (conn, addr) = serversocket.accept()
        start_new_thread(fun, (conn, addr))


app = QtWidgets.QApplication(sys.argv)
MainWindow = MyWindow()
ui = Ui_MainWindow()
ui.setupUi(MainWindow)

if __name__ == "__main__":
    start_new_thread(run_server, ())
    MainWindow.center()
    sys.exit(app.exec_())