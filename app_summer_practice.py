import psutil as psutil
from PyQt5 import QtCore, QtGui, QtWidgets
import socket
import _pickle as cPickle
import os
import threading
import sys, time

from PyQt5.QtCore import QTimer, Qt
from PyQt5.QtGui import QPalette, QColor, QPixmap
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
max_voltage = 10.00

class test1_Window(QWidget):
    def __init__(self, parent = None):
        super(test1_Window, self).__init__(parent)
        # label = QLabel("Sub Window", self)
        self.setupUi()

    def setupUi(self):
        self.setObjectName("Test case 1")
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

        self.lineEdit.setStyleSheet("""QLineEdit { background-color: rgb(25, 25, 25) }""")
        self.lineEdit_2.setStyleSheet("""QLineEdit { background-color: rgb(25, 25, 25) }""")
        self.lineEdit_3.setStyleSheet("""QLineEdit { background-color: rgb(25, 25, 25) }""")
        self.lineEdit_4.setStyleSheet("""QLineEdit { background-color: rgb(25, 25, 25) }""")


        self.retranslateUi()
        QtCore.QMetaObject.connectSlotsByName(self)

    def retranslateUi(self):
        _translate = QtCore.QCoreApplication.translate
        self.setWindowTitle(_translate("Form", "Test Case 1"))
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

class test2_Window(QWidget):
    def __init__(self, parent = None):
        super(test2_Window, self).__init__(parent)
        self.setupUi()

    def setupUi(self):
        self.setObjectName("Test Case 2")
        self.resize(278, 193)
        self.label_2 = QtWidgets.QLabel(self)
        self.label_2.setGeometry(QtCore.QRect(105, 10, 81, 16))
        self.label_2.setObjectName("label_2")
        self.line = QtWidgets.QFrame(self)
        self.line.setGeometry(QtCore.QRect(0, 30, 291, 16))
        self.line.setFrameShape(QtWidgets.QFrame.HLine)
        self.line.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line.setObjectName("line")
        self.label_3 = QtWidgets.QLabel(self)
        self.label_3.setGeometry(QtCore.QRect(108, 70, 131, 20))
        self.label_3.setObjectName("label_3")
        self.lineEdit_2 = QtWidgets.QLineEdit(self)
        self.lineEdit_2.setGeometry(QtCore.QRect(90, 100, 101, 31))
        self.lineEdit_2.setObjectName("lineEdit_2")
        self.lineEdit_2.setReadOnly(True)
        self.lineEdit_2.setStyleSheet("""QLineEdit { background-color: rgb(25, 25, 25) }""")

        self.retranslateUi()
        QtCore.QMetaObject.connectSlotsByName(self)


    def retranslateUi(self):
        _translate = QtCore.QCoreApplication.translate
        self.setWindowTitle(_translate("Form", "Test Case 2"))
        self.label_2.setText(_translate("Form", "Voltage Test"))
        self.label_3.setText(_translate("Form", "Supply Voltage"))

    def edit_voltage(self, voltage):
        self.lineEdit_2.setText(str(voltage))
    def closeEvent(self, event):
        event.ignore()


class test3_Window(QWidget):
    def __init__(self, parent=None):
        super(test3_Window, self).__init__(parent)
        self.setupUi()

    def setupUi(self):
        self.setObjectName("Test Case 3")
        self.resize(278, 193)
        self.label_2 = QtWidgets.QLabel(self)
        self.label_2.setGeometry(QtCore.QRect(90, 10, 71, 16))
        self.label_2.setObjectName("label_2")
        self.line = QtWidgets.QFrame(self)
        self.line.setGeometry(QtCore.QRect(0, 30, 291, 16))
        self.line.setFrameShape(QtWidgets.QFrame.HLine)
        self.line.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line.setObjectName("line")
        self.label = QtWidgets.QLabel(self)
        self.label.setGeometry(QtCore.QRect(90, 50, 81, 20))
        self.label.setObjectName("label")
        self.lineEdit = QtWidgets.QLineEdit(self)
        self.lineEdit.setGeometry(QtCore.QRect(70, 80, 111, 31))
        self.lineEdit.setObjectName("lineEdit")
        self.lineEdit.setReadOnly(True)
        self.lineEdit.setStyleSheet("""QLineEdit { background-color: rgb(25, 25, 25) }""")

        self.retranslateUi()
        QtCore.QMetaObject.connectSlotsByName(self)

    def retranslateUi(self):
        _translate = QtCore.QCoreApplication.translate
        self.setWindowTitle(_translate("Form", "Test Case 3"))
        self.label_2.setText(_translate("Form", "Speed Test"))
        self.label.setText(_translate("Form", "Motor Speed"))

    def edit_speed(self, speed):
        self.lineEdit.setText(str(speed))

    def closeEvent(self, event):
        event.ignore()


class Ui_MainWindow(object):

    def setupUi(self, MainWindow):
        self.test_case = 0
        self.rpm = 0
        self.test_time = 30
        self.temp = 0
        self.hum = 0
        self.motor_temp = 0
        self.motor_hum = 0
        self.voltage = 0
        self.speed = 0
        self.maxHTemp = 0
        self.maxMTemp = 0
        self.minHTemp = 100
        self.minMTemp = 100
        self.maxHHum = 0
        self.maxMHum = 0
        self.minHHum = 100
        self.minMHum = 100
        self.motor_sens = 1 # 1 -> positive  / 2 -> negative
        self.maxVoltage = 0
        self.minVoltage = 100
        self.maxSpeed = 0
        self.minSpeed = 99999

        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(1280, 768)

        self.openTestCase1Window()
        self.openTestCase2Window()
        self.openTestCase3Window()

        self.MainWindow = MainWindow
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")

        # Continental image
        self.image_label = QtWidgets.QLabel(self.centralwidget)
        self.image_label.setGeometry(QtCore.QRect(180, 400, 350, 120))
        pixmap = QPixmap("conti.png")
        pixmap = pixmap.scaled(350, 120, QtCore.Qt.KeepAspectRatio)
        self.image_label.setPixmap(pixmap)

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
        self.checkBox_2.stateChanged.connect(self.voltage_test_status)

        self.checkBox_3 = QtWidgets.QCheckBox(self.centralwidget)
        self.checkBox_3.setGeometry(QtCore.QRect(700, 200, 201, 41))
        self.checkBox_3.setObjectName("checkBox_3")
        self.checkBox_3.stateChanged.connect(self.speed_test_status)

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
        self.pushButton_3.clicked.connect(self.positive_click)

        self.pushButton_4 = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_4.setGeometry(QtCore.QRect(240, 200, 130, 40))
        self.pushButton_4.setObjectName("pushButton_4")
        self.pushButton_4.clicked.connect(self.negative_click)

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

    def check_temp(self, temp, hum, m_temp, m_hum):
        global max_temp, temperature_fail
        if temp > max_temp or m_temp > max_temp:
            temperature_fail = True

    def check_voltage(self, voltage):
        global max_voltage, voltage_fail
        if voltage > max_voltage:
            voltage_fail = True


    def positive_click(self):
        self.motor_sens = 1

    def negative_click(self):
        self.motor_sens = 2

    def recv_messages(self):
        self.stop_event = threading.Event()
        self.c_thread = threading.Thread(target=self.recv_messages_handler)
        self.c_thread.start()

    def recv_messages_handler(self):
        while True:
            if start_test:
                data = self.conn.recv(1024)
                data = data.decode()
                if self.test_case == 1:
                    self.test_case_1(data)
                if self.test_case == 2:
                    self.test_case_2(data)
                if self.test_case == 3:
                    self.test_case_3(data)
                if self.test_case == 4:
                    self.test_case_1(data)
                    self.test_case_2(data.split(" ")[4])
                if self.test_case == 5:
                    self.test_case_2(data.split(" ")[0])
                    self.test_case_3(data.split(" ")[1])
                if self.test_case == 6:
                    self.test_case_1(data)
                    self.test_case_2(data.split(" ")[4])
                    self.test_case_3(data.split(" ")[5])

    def test_case_1(self, data):
        d_s = data.split(" ")
        self.temp = d_s[0].split("=")[1]
        self.hum = d_s[1].split("=")[1]
        self.motor_temp = d_s[2].split("=")[1]
        self.motor_hum = d_s[3].split("=")[1]
        try:
            self.check_temp(float(self.temp), float(self.hum), float(self.motor_temp), float(self.motor_hum))
        except:
            pass

    def test_case_2(self, data):
        self.voltage = float(data)
        self.voltage = round(self.voltage / 20.83, 2)
        print(self.voltage)
        if self.voltage > self.maxVoltage:
            self.maxVoltage = self.voltage
        if self.voltage < self.minVoltage:
            self.minVoltage = self.voltage

        self.check_voltage(self.voltage)

    def test_case_3(self, data):
        try:
            self.speed = float(data)
            if self.speed > self.maxSpeed:
                self.maxSpeed = self.speed
            if self.speed < self.minSpeed:
                self.minSpeed = self.speed
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

    def voltage_test_status(self, state):
        global voltage_test
        if state == QtCore.Qt.Checked:
            voltage_test = True
        else:
            voltage_test = False
        print(voltage_test)

    def speed_test_status(self, state):
        global speed_test
        if state == QtCore.Qt.Checked:
            speed_test = True
        else:
            speed_test = False


    def set_vars_to_zero(self):
        self.maxHTemp = 0
        self.maxMTemp = 0
        self.minHTemp = 100
        self.minMTemp = 100
        self.maxHHum = 0
        self.maxMHum = 0
        self.minHHum = 100
        self.minMHum = 100
        self.maxVoltage = 0
        self.minVoltage = 100
        self.maxSpeed = 0
        self.minSpeed = 99999

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
        response = "S " + str(self.motor_sens) + " " + str(self.test_case) + " " + str(self.horizontalSlider.value())
        self.send_bytes_to_client(response)

        start_test = True

        self.temp_box = temperature_test
        self.voltage_box = voltage_test
        self.speed_box = speed_test

        if self.temp_box:
            self.testCase1Window.setVisible(True)
            self.testCase1Window.activateWindow()

        if self.voltage_box:
            self.testCase2Window.setVisible(True)
            self.testCase2Window.activateWindow()

        if self.speed_box:
            self.testCase3Window.setVisible(True)
            self.testCase3Window.activateWindow()

        self.counter = 0
        self.timer = QTimer()
        self.timer.setInterval(1000)
        self.timer.timeout.connect(self.start_test_counter)
        self.timer.start()

        threading.Thread(target=self.start_test_counter).start()

    def stop(self):
        global start_test

        if temperature_test:
            self.textbox.setPlainText(self.textbox.toPlainText() + '\n' + datetime.now().strftime("%d/%m/%Y %H:%M:%S") + ": " + "Maximum H Bridge Temperature: " + str(self.maxHTemp))
            self.textbox.setPlainText(self.textbox.toPlainText() + '\n' + datetime.now().strftime("%d/%m/%Y %H:%M:%S") + ": " + "Maximum H Bridge Humidity: " + str(self.maxHHum))

            self.textbox.setPlainText(self.textbox.toPlainText() + '\n' + datetime.now().strftime("%d/%m/%Y %H:%M:%S") + ": " + "Maximum Motor Temperature: " + str(self.maxMTemp))
            self.textbox.setPlainText(self.textbox.toPlainText() + '\n' + datetime.now().strftime("%d/%m/%Y %H:%M:%S") + ": " + "Maximum Motor Humidity: " + str(self.maxMHum))

        if voltage_test:
            self.textbox.setPlainText(self.textbox.toPlainText() + '\n' + datetime.now().strftime("%d/%m/%Y %H:%M:%S") + ": " + "Maximum Supply Voltage: " + str(self.maxVoltage))
            self.textbox.setPlainText(self.textbox.toPlainText() + '\n' + datetime.now().strftime("%d/%m/%Y %H:%M:%S") + ": " + "Minimum Supply Voltage: " + str(self.minVoltage))

        if speed_test:
            self.textbox.setPlainText(self.textbox.toPlainText() + '\n' + datetime.now().strftime("%d/%m/%Y %H:%M:%S") + ": " + "Maximum Speed: " + str(self.maxSpeed))
            self.textbox.setPlainText(self.textbox.toPlainText() + '\n' + datetime.now().strftime("%d/%m/%Y %H:%M:%S") + ": " + "Minimum Speed: " + str(self.minSpeed))

        self.textbox.setPlainText(self.textbox.toPlainText() + '\n' + datetime.now().strftime("%d/%m/%Y %H:%M:%S") + ": " + "Test stopped!")



        self.pushButton.setEnabled(True)
        self.pushButton_2.setEnabled(False)
        self.send_bytes_to_client("X")
        self.timer.stop()


        self.testCase1Window.setVisible(False)
        self.testCase2Window.setVisible(False)
        self.testCase3Window.setVisible(False)

        self.progressBar.setValue(0)
        start_test = False

    def slider_move(self):
        self.rpm = int((self.horizontalSlider.value() * 14000) / 255)
        self.textEdit.setPlainText(str(self.rpm))

    def openTestCase1Window(self):
        self.testCase1Window = test1_Window()
        self.testCase1Window.show()
        self.testCase1Window.setVisible(False)

    def openTestCase2Window(self):
        self.testCase2Window = test2_Window()
        self.testCase2Window.show()
        self.testCase2Window.setVisible(False)

    def openTestCase3Window(self):
        self.testCase3Window = test3_Window()
        self.testCase3Window.show()
        self.testCase3Window.setVisible(False)

    def check_temps(self, temp, hum, motor_temp, motor_hum):
        if temp > self.maxHTemp:
            self.maxHTemp = temp
        if temp < self.minHTemp:
           self.minHTemp = temp

        if hum > self.maxHHum:
           self.maxHHum = hum

        if hum < self.minHHum:
           self.minHHum = hum

        if motor_temp > self.maxMTemp:
            self.maxMTemp = motor_temp
        if motor_temp < self.minMTemp:
           self.minMTemp = motor_temp

        if motor_hum > self.maxMHum:
           self.maxMHum = motor_hum

        if motor_hum < self.minMHum:
           self.minMHum = motor_hum


    def start_test_counter(self):
        global temperature_fail, speed_fail, voltage_fail
        self.counter += 1
        self.progressBar.setValue(int((self.counter * 100) / self.test_time))

        self.check_temps(float(self.temp), float(self.hum), float(self.motor_temp), float(self.motor_hum))

        if self.temp_box:
            self.testCase1Window.edit_temps(self.temp, self.hum, self.motor_temp, self.motor_hum)

        if self.voltage_box:
            self.testCase2Window.edit_voltage(self.voltage)

        if self.speed_box:
            self.testCase3Window.edit_speed(self.speed)

        if voltage_fail:
            self.textbox.setPlainText(
                self.textbox.toPlainText() + '\n' + datetime.now().strftime("%d/%m/%Y %H:%M:%S") + ": "
                + "Test FAILED! Voltage is greater than limit!")
            self.stop()


        if temperature_fail:
            self.textbox.setPlainText(
                self.textbox.toPlainText() + '\n' + datetime.now().strftime("%d/%m/%Y %H:%M:%S") + ": "
                + "Test FAILED! Temperature is greater than limit!")
            self.stop()

        if self.counter > self.test_time:
            self.textbox.setPlainText(self.textbox.toPlainText() + '\n' + datetime.now().strftime("%d/%m/%Y %H:%M:%S")
                                      + ": " + "Test SUCCEED!")
            self.stop()


    def test_cases(self):
        global temperature_test, voltage_test, speed_test
        if temperature_test:
            if voltage_test:
                if speed_test:
                    self.test_case = 6
                    return
                self.test_case = 4
                return
            self.test_case = 1
            return
        if voltage_test:
            if speed_test:
                self.test_case = 5
                return
            self.test_case = 2
            return
        if speed_test:
            self.test_case = 3


def kill_proc_tree(pid, including_parent=True):
    parent = psutil.Process(pid)
    if including_parent:
        parent.kill()



palette = QPalette()
palette.setColor(QPalette.Window, QColor(40, 40, 40))
palette.setColor(QPalette.WindowText, QColor(200, 200, 200))
palette.setColor(QPalette.Base, QColor(25, 25, 25))
palette.setColor(QPalette.AlternateBase, QColor(53, 53, 53))
palette.setColor(QPalette.ToolTipBase, Qt.black)
palette.setColor(QPalette.ToolTipText, QColor(200, 200, 200))
palette.setColor(QPalette.Text, QColor(200, 200, 200))
palette.setColor(QPalette.Button, QColor(53, 53, 53))
palette.setColor(QPalette.ButtonText, Qt.black)
palette.setColor(QPalette.BrightText, Qt.red)
palette.setColor(QPalette.Link, QColor(42, 130, 218))
palette.setColor(QPalette.Highlight, QColor(42, 130, 218))
palette.setColor(QPalette.HighlightedText, Qt.black)

def main():
    import sys
    app = QtWidgets.QApplication(sys.argv)
    app.setPalette(palette)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()

me = os.getpid()
kill_proc_tree(me)
