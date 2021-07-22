import psutil as psutil
from PyQt5 import QtCore, QtGui, QtWidgets
import socket
import _pickle as cPickle
import os
import threading
import sys, time

from PyQt5.QtCore import QTimer
from PyQt5.QtWidgets import QTextEdit, QDialog, QLabel, QWidget, QMessageBox, QMainWindow
from datetime import datetime

# SERVER IP and HOST
HOST = '0.0.0.0'
PORT = 50100

# FLAGS
stop_thread = False
start_test = False
temperature_test = False
voltage_test = False
speed_test = False

temperature_fail = False
voltage_fail = False
speed_fail = False

max_temp = 30.00

class test1_Window(QWidget):
    def __init__(self, parent = None):
        super(test1_Window, self).__init__(parent)
        # label = QLabel("Sub Window", self)
        self.setupUi()

    def setupUi(self):
        self.setObjectName("Form")
        self.resize(278, 193)
        self.label_2 = QtWidgets.QLabel(self)
        self.label_2.setGeometry(QtCore.QRect(90, 10, 91, 16))
        self.label_2.setObjectName("label_2")
        self.line = QtWidgets.QFrame(self)
        self.line.setGeometry(QtCore.QRect(0, 30, 291, 16))
        self.line.setFrameShape(QtWidgets.QFrame.HLine)
        self.line.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line.setObjectName("line")
        self.line_2 = QtWidgets.QFrame(self)
        self.line_2.setGeometry(QtCore.QRect(125, 37, 20, 160))
        self.line_2.setFrameShape(QtWidgets.QFrame.VLine)
        self.line_2.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line_2.setObjectName("line_2")

        self.label = QtWidgets.QLabel(self)
        self.label.setGeometry(QtCore.QRect(20, 50, 110, 20))
        self.label.setObjectName("label")
        self.label_3 = QtWidgets.QLabel(self)
        self.label_3.setGeometry(QtCore.QRect(160, 50, 110, 20))
        self.label_3.setObjectName("label_3")
        self.lineEdit = QtWidgets.QLineEdit(self)
        self.lineEdit.setGeometry(QtCore.QRect(30, 80, 60, 20))
        self.lineEdit.setObjectName("lineEdit")
        self.lineEdit.setReadOnly(True)
        self.lineEdit_2 = QtWidgets.QLineEdit(self)
        self.lineEdit_2.setGeometry(QtCore.QRect(170, 80, 60, 20))
        self.lineEdit_2.setObjectName("lineEdit_2")
        self.lineEdit_2.setReadOnly(True)
        self.label_4 = QtWidgets.QLabel(self)
        self.label_4.setGeometry(QtCore.QRect(20, 120, 110, 20))
        self.label_4.setObjectName("label_4")
        self.label_5 = QtWidgets.QLabel(self)
        self.label_5.setGeometry(QtCore.QRect(160, 120, 110, 20))
        self.label_5.setObjectName("label_5")
        self.lineEdit_3 = QtWidgets.QLineEdit(self)
        self.lineEdit_3.setGeometry(QtCore.QRect(30, 150, 60, 20))
        self.lineEdit_3.setObjectName("lineEdit_3")
        self.lineEdit_3.setReadOnly(True)
        self.lineEdit_4 = QtWidgets.QLineEdit(self)
        self.lineEdit_4.setGeometry(QtCore.QRect(170, 150, 60, 20))
        self.lineEdit_4.setObjectName("lineEdit_4")
        self.lineEdit_4.setReadOnly(True)

        self.retranslateUi()
        QtCore.QMetaObject.connectSlotsByName(self)

    def retranslateUi(self):
        _translate = QtCore.QCoreApplication.translate
        self.setWindowTitle(_translate("Form", "Form"))
        self.label_2.setText(_translate("Form", "Temperature test"))
        self.label.setText(_translate("Form", "HBridge Temperature"))
        self.label_3.setText(_translate("Form", "Motor Temperature"))
        self.label_4.setText(_translate("Form", "HBridge Humidity"))
        self.label_5.setText(_translate("Form", "Motor Humidity"))

    def edit_temps(self,htemp, hhum, mtemp, mhum):
        self.lineEdit.setText(str(htemp))
        self.lineEdit_3.setText(str(hhum))
        self.lineEdit_2.setText(str(mtemp))
        self.lineEdit_4.setText(str(mhum))

    def closeEvent(self, event):
        event.ignore()

class Ui_MainWindow(object):

    def setupUi(self, MainWindow):
        self.test_case = 0
        self.rpm = 0
        self.test_time = 30
        self.temp = 0
        self.hum = 0
        self.maxHTemp = 0
        self.maxMTemp = 0
        self.minHTemp = 0
        self.minMTemp = 0
        self.maxHHum = 0
        self.maxMHum = 0
        self.minHHum = 0
        self.minMHum = 0

        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(1280, 768)

        self.openSub()
        self.sub.hide()

        self.MainWindow = MainWindow
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
        self.progressBar.setProperty("value", 0)
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

        self.horizontalSlider = QtWidgets.QSlider(self.centralwidget)
        self.horizontalSlider.setGeometry(QtCore.QRect(70, 110, 301, 25))
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.horizontalSlider.setFont(font)
        self.horizontalSlider.setAutoFillBackground(False)
        self.horizontalSlider.setMaximum(255)
        self.horizontalSlider.setOrientation(QtCore.Qt.Horizontal)
        self.horizontalSlider.setObjectName("horizontalSlider")
        self.horizontalSlider.sliderMoved.connect(self.slider_move)

        self.label_2 = QtWidgets.QLabel(self.centralwidget)
        self.label_2.setGeometry(QtCore.QRect(70, 72, 71, 21))
        self.label_2.setObjectName("label_2")

        self.label_3 = QtWidgets.QLabel(self.centralwidget)
        self.label_3.setGeometry(QtCore.QRect(70, 170, 81, 16))
        self.label_3.setObjectName("label_3")

        self.pushButton_3 = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_3.setGeometry(QtCore.QRect(70, 200, 130, 40))
        self.pushButton_3.setObjectName("pushButton_3")

        self.pushButton_4 = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_4.setGeometry(QtCore.QRect(240, 200, 130, 40))
        self.pushButton_4.setObjectName("pushButton_4")

        self.label_4 = QtWidgets.QLabel(self.centralwidget)
        self.label_4.setGeometry(QtCore.QRect(70, 270, 47, 13))
        self.label_4.setObjectName("label_4")

        self.textEdit = QTextEdit(self.centralwidget)
        self.textEdit.setGeometry(QtCore.QRect(70, 290, 81, 31))
        self.textEdit.setObjectName("textEdit")
        self.textEdit.setReadOnly(True)

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

        threading.Thread(target=self.start_server).start()
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
        self.label_2.setText(_translate("MainWindow", "Manual RPM"))
        self.label_3.setText(_translate("MainWindow", "Motor direction:"))
        self.pushButton_3.setText(_translate("MainWindow", "Positive"))
        self.pushButton_4.setText(_translate("MainWindow", "Negative"))
        self.label_4.setText(_translate("MainWindow", "RPM"))
        self.menu_Exit.setTitle(_translate("MainWindow", "&Exit"))
        self.menuHelp.setTitle(_translate("MainWindow", "Help"))

    def start_server(self):
        global server_created_flag
        server_created_flag = True

        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.s.bind((HOST, PORT))
        print("Waiting for client!")
        self.s.listen()
        self.conn, addr = self.s.accept()
        print('Connected by ', addr)

        threading.Thread(target=self.recv_messages).start()

    def check_temp(self, temp, hum):
        global max_temp, temperature_fail
        if temp > max_temp:
            temperature_fail = True
        else:
            print(temp)

    def recv_messages(self):
        self.stop_event = threading.Event()
        self.c_thread = threading.Thread(target=self.recv_messages_handler)
        self.c_thread.start()

    def recv_messages_handler(self):
        while True:
            if start_test:
                data = self.conn.recv(1024)
                data = data.decode()
                print(data)
                if self.test_case == 1:
                    d_s = data.split(" ")
                    self.temp = d_s[0].split("=")[1]
                    self.hum = d_s[1].split("=")[1]
                    try:
                        self.check_temp(float(self.temp), float(self.hum))
                    except:
                        pass

    def send_bytes_to_client(self, response):
        try:
            self.conn.sendall(bytes(response.encode()))
            print("Am trimis '" + response + "' catre client!")
        except BrokenPipeError:
            print("Client has been disconnected!")

    def temperature_test_status(self, state):
        global temperature_test
        if state == QtCore.Qt.Checked:
            temperature_test = True
        else:
            temperature_test = False
        print(temperature_test)


    def set_vars_to_zero(self):
        self.maxHTemp = 0
        self.maxMTemp = 0
        self.minHTemp = 0
        self.minMTemp = 0
        self.maxHHum = 0
        self.maxMHum = 0
        self.minHHum = 0
        self.minMHum = 0

    def start(self):
        global start_test, temperature_fail, voltage_fail, speed_fail, temperature_test, voltage_test, speed_test
        temperature_fail = False
        voltage_fail = False
        speed_fail = False
        self.set_vars_to_zero()

        self.textbox.setPlainText(self.textbox.toPlainText() + '\n' + datetime.now().strftime("%d/%m/%Y %H:%M:%S") + ": " + "Test started!")
        self.pushButton.setEnabled(False)
        self.pushButton_2.setEnabled(True)
        self.test_cases()
        response = "S " + str(self.test_case) + " " + str(self.horizontalSlider.value())
        self.send_bytes_to_client(response)

        start_test = True

        self.temp_box = temperature_test
        self.voltage_box = voltage_test
        self.speed_box = speed_test

        self.counter = 0
        self.timer = QTimer()
        self.timer.setInterval(1000)
        self.timer.timeout.connect(self.start_test_counter)
        self.timer.start()

        threading.Thread(target=self.start_test_counter).start()

    def stop(self):
        global start_test

        self.textbox.setPlainText(self.textbox.toPlainText() + '\n' + datetime.now().strftime("%d/%m/%Y %H:%M:%S") + ": " + "Max HTemp: " + str(self.maxHTemp))
        self.textbox.setPlainText(self.textbox.toPlainText() + '\n' + datetime.now().strftime("%d/%m/%Y %H:%M:%S") + ": " + "Max HHum: " + str(self.maxHHum))

        self.textbox.setPlainText(self.textbox.toPlainText() + '\n' + datetime.now().strftime("%d/%m/%Y %H:%M:%S") + ": " + "Max HTemp: " + str(self.maxMTemp))
        self.textbox.setPlainText(self.textbox.toPlainText() + '\n' + datetime.now().strftime("%d/%m/%Y %H:%M:%S") + ": " + "Max HHum: " + str(self.maxMHum))

        self.textbox.setPlainText(self.textbox.toPlainText() + '\n' + datetime.now().strftime("%d/%m/%Y %H:%M:%S") + ": " + "Test stopped!")
        self.pushButton.setEnabled(True)
        self.pushButton_2.setEnabled(False)
        self.send_bytes_to_client("X")
        self.timer.stop()
        self.sub.hide()
        self.progressBar.setValue(0)
        start_test = False

    def slider_move(self):
        self.rpm = int((self.horizontalSlider.value() * 14000) / 255)
        self.textEdit.setPlainText(str(self.rpm))

    def openSub(self):
        self.sub = test1_Window()
        self.sub.show()

    def check_temps(self, temp, hum):
        if temp > self.maxHTemp:
            self.maxHTemp = temp
        if temp < self.minHTemp:
           self.minHTemp = temp

        if hum > self.maxHHum:
           self.maxHHum = hum

        if hum < self.minHHum:
           self.minHHum = hum


    def start_test_counter(self):
        self.counter += 1
        self.progressBar.setValue(int((self.counter * 100) / self.test_time))

        self.check_temps(float(self.temp), float(self.hum))

        if self.temp_box:
            self.sub.edit_temps(self.temp, self.hum, 0, 0)
            self.sub.show()
        if temperature_fail:
            self.textbox.setPlainText(
                self.textbox.toPlainText() + '\n' + datetime.now().strftime("%d/%m/%Y %H:%M:%S") + ": " + "Test FAILED! Temperature is greater than limit!")
            self.stop()
        if self.counter > self.test_time:
            self.textbox.setPlainText(self.textbox.toPlainText() + '\n' + datetime.now().strftime("%d/%m/%Y %H:%M:%S") + ": " + "Test SUCCEED!")
            self.stop()

    def test_cases(self):
        global temperature_test, voltage_test, speed_test
        if temperature_test:
            if voltage_test:
                if speed_test:
                    self.test_case = 7
                    return
                self.test_case = 4
                return
            self.test_case = 1
            return
        if voltage_test:
            if speed_test:
                self.test_case = 6
                return
            self.test_case = 2
            return
        if speed_test:
            self.test_case = 3


def kill_proc_tree(pid, including_parent=True):
    parent = psutil.Process(pid)
    if including_parent:
        parent.kill()


def main():
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()

me = os.getpid()
kill_proc_tree(me)
