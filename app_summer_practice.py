import os
import socket
import threading
from datetime import datetime

import psutil as psutil
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import QTimer, Qt
from PyQt5.QtGui import QPalette, QColor, QPixmap
from PyQt5.QtWidgets import QTextEdit

import graph_window
import settings
import window_testcase_1
import window_testcase_2
import window_testcase_3
import flags_window

# SERVER IP and HOST
HOST = '0.0.0.0'
PORT = 50100

# FLAGS
stop_thread = False
start_test = False
temperature_test = False
voltage_test = False
speed_test = False

# ERROR FLAGS
temperature_fail = False
voltage_fail = False
speed_fail = False
distance_fail = False

max_temp = 28.00
max_voltage = 50.00

settings.init()


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
        self.motor_sens = 1  # 1 -> positive  / 2 -> negative
        self.maxVoltage = 0
        self.minVoltage = 100
        self.maxSpeed = 0
        self.minSpeed = 99999
        self.bridgeTemp = []
        self.voltageV = []
        self.cnt = 0
        self.distance = 100

        # values for flags
        self.x_values_for_flags = []
        self.y_values_temperature = []
        self.y_values_voltage = []
        self.y_values_distance = []

        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(1280, 768)

        scriptDir = os.path.dirname(os.path.realpath(__file__))
        MainWindow.setWindowIcon(QtGui.QIcon(scriptDir + os.path.sep + "Images" + os.path.sep + "icon.png"))

        self.openTestCase1Window()
        self.openTestCase2Window()
        self.openTestCase3Window()
        self.openGraphWindow()
        self.openFlagsWindow()

        self.MainWindow = MainWindow
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")

        # Continental image
        self.image_label = QtWidgets.QLabel(self.centralwidget)
        self.image_label.setGeometry(QtCore.QRect(180, 400, 350, 120))
        pixmap = QPixmap("Images" + os.path.sep + "conti.png")
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
        self.pushButton.setStyleSheet("""QPushButton {
                                    border-width: 1px;
                                    padding: 1px;
                                    border-style: solid;
                                    border-radius:10px;
                                    background: qlineargradient(
                                        x1:0, y1:0, x2:1, y2:1,
                                        stop: 0.01 orange, stop: 0.8 rgb(255,140,0), stop:0 white
                                    )
                                    }""")

        self.pushButton_2 = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_2.setGeometry(QtCore.QRect(1020, 480, 130, 40))
        self.pushButton_2.setObjectName("pushButton_2")
        self.pushButton_2.setEnabled(False)
        self.pushButton_2.clicked.connect(self.stop)
        self.pushButton_2.setStyleSheet("""QPushButton {
                                            border-width: 1px;
                                            padding: 1px;
                                            border-style: solid;
                                            border-radius:10px;
                                            background: qlineargradient(
                                                x1:0, y1:0, x2:1, y2:1,
                                                stop: 0.01 orange, stop: 0.8 rgb(255,140,0), stop:0 white
                                            )
                                            }""")

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
        self.pushButton_3.setStyleSheet("""QPushButton {
                                            border-width: 1px;
                                            padding: 1px;
                                            border-style: solid;
                                            border-radius:10px;
                                            background: qlineargradient(
                                                x1:0, y1:0, x2:1, y2:1,
                                                stop: 0.01 orange, stop: 0.8 rgb(255,140,0), stop:0 white
                                            )
                                            }""")

        self.pushButton_4 = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_4.setGeometry(QtCore.QRect(240, 200, 130, 40))
        self.pushButton_4.setObjectName("pushButton_4")
        self.pushButton_4.clicked.connect(self.negative_click)
        self.pushButton_4.setStyleSheet("""QPushButton {
                                            border-width: 1px;
                                            padding: 1px;
                                            border-style: solid;
                                            border-radius:10px;
                                            background: qlineargradient(
                                                x1:0, y1:0, x2:1, y2:1,
                                                stop: 0.01 orange, stop: 0.8 rgb(255,140,0), stop:0 white
                                            )
                                            }""")

        self.label_4 = QtWidgets.QLabel(self.centralwidget)
        self.label_4.setGeometry(QtCore.QRect(70, 270, 47, 13))
        self.label_4.setObjectName("label_4")

        self.textEdit = QTextEdit(self.centralwidget)
        self.textEdit.setGeometry(QtCore.QRect(70, 290, 81, 31))
        self.textEdit.setObjectName("textEdit")
        self.textEdit.setReadOnly(True)
        self.textEdit.setStyleSheet(""" QTextEdit{
                                    border-width: 1px;
                                    padding: 1px;
                                    border-style: solid;
                                    border-radius: 10px
                                    }""")

        self.label_temp = QtWidgets.QLabel(self.centralwidget)
        self.label_temp.setGeometry(QtCore.QRect(705, 260, 120, 31))
        self.label_temp.setObjectName("label")
        self.label_temp.setText("Maximum Temperature")

        self.textEditTemperature = QTextEdit(self.centralwidget)
        self.textEditTemperature.setGeometry(QtCore.QRect(705, 290, 81, 31))
        self.textEditTemperature.setObjectName("textEditTemperature")
        self.textEditTemperature.setStyleSheet("""QTextEdit{
                                    border-width: 1px;
                                    padding: 1px;
                                    border-style: solid;
                                    border-radius: 10px
                                    }""")
        self.textEditTemperature.setText(str(max_temp))

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
        MainWindow.setWindowTitle(_translate("MainWindow", "Wifi Test Framework"))
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
                flag = True
                data = self.conn.recv(1024)
                data = data.decode()
                print(data)
                data_split = data.split(" ")
                if data_split[0] == "STOP":
                    self.distance = float(data_split[1])
                    flag = False
                if self.test_case == 1 and flag:
                    self.test_case_1(data)
                if self.test_case == 2 and flag:
                    self.test_case_2(data)
                if self.test_case == 3 and flag:
                    self.test_case_3(data)
                if self.test_case == 4 and flag:
                    self.test_case_1(data)
                    self.test_case_2(data.split(" ")[4])
                if self.test_case == 5 and flag:
                    self.test_case_2(data.split(" ")[0])
                    self.test_case_3(data.split(" ")[1])
                if self.test_case == 6 and flag:
                    self.test_case_1(data)
                    self.test_case_2(data.split(" ")[4])
                    self.test_case_3(data.split(" ")[5])

    def test_case_1(self, data):
        global temperature
        d_s = data.split(" ")
        self.temp = d_s[0].split("=")[1]
        self.hum = d_s[1].split("=")[1]
        self.motor_temp = d_s[2].split("=")[1]
        self.motor_hum = d_s[3].split("=")[1]
        self.bridgeTemp.append(self.motor_temp)
        try:
            self.check_temp(float(self.temp), float(self.hum), float(self.motor_temp), float(self.motor_hum))
        except:
            pass
        settings.temperature = self.temp

    def test_case_2(self, data):
        global voltage
        self.voltage = float(data)
        self.voltage = round(self.voltage / 21.99, 2)
        print(self.voltage)
        settings.voltage = self.voltage
        if self.voltage > self.maxVoltage:
            self.maxVoltage = self.voltage
        if self.voltage < self.minVoltage:
            self.minVoltage = self.voltage

        self.voltageV.append(self.voltage)
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
        self.cnt = 0
        self.distance = 100

        self.x_values_for_flags = []
        self.y_values_temperature = []
        self.y_values_voltage = []
        self.y_values_distance = []

    def start(self):
        global start_test, temperature_fail, voltage_fail, speed_fail, distance_fail, \
            temperature_test, voltage_test, speed_test, max_temp

        temperature_fail = False
        voltage_fail = False
        speed_fail = False
        distance_fail = False

        self.set_vars_to_zero()
        dt = datetime.now()
        logfile = 'Log-%s-%s-%s.csv' % (dt.year, dt.month, dt.day)
        self.file = open("Logs/" + logfile, 'a')

        try:
            max_temp = float(self.textEditTemperature.toPlainText())
        except:
            max_temp = 0

        self.textbox.setPlainText(self.textbox.toPlainText() + '\n' + datetime.now().strftime("%d/%m/%Y %H:%M:%S")
                                  + ": " + "Test started!")
        self.file.write(datetime.now().strftime("%d/%m/%Y %H:%M:%S") + ": " + "Test started!" + "\n")
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

        self.graphWindow.start_timer()
        self.graphWindow.setVisible(True)
        self.graphWindow.activateWindow()

        # self.flagsWindow.setVisible(True)
        # self.flagsWindow.activateWindow()

        self.counter = 0
        self.timer = QTimer()
        self.timer.setInterval(1000)
        self.timer.timeout.connect(self.start_test_counter)
        self.timer.start()

        threading.Thread(target=self.start_test_counter).start()

    def stop(self):
        global start_test

        while len(self.x_values_for_flags) < 30:
            self.x_values_for_flags.append(self.x_values_for_flags[-1] + 1)
            self.y_values_voltage.append(0)
            self.y_values_temperature.append(0)
            self.y_values_distance.append(0)

        if len(self.x_values_for_flags) > 30:
            self.x_values_for_flags = self.x_values_for_flags[0:29]
            self.y_values_voltage = self.y_values_voltage[0:29]
            self.y_values_distance = self.y_values_distance[0:29]
            self.y_values_temperature = self.y_values_temperature[0:29]

        self.flagsWindow.setVisible(True)
        self.flagsWindow.activateWindow()

        if temperature_test:
            self.textbox.setPlainText(self.textbox.toPlainText() + '\n' + datetime.now().strftime("%d/%m/%Y %H:%M:%S")
                                      + ": " + "Maximum H Bridge Temperature: " + str(self.maxHTemp))
            self.textbox.setPlainText(self.textbox.toPlainText() + '\n' + datetime.now().strftime("%d/%m/%Y %H:%M:%S")
                                      + ": " + "Maximum H Bridge Humidity: " + str(self.maxHHum))
            self.file.write(datetime.now().strftime("%d/%m/%Y %H:%M:%S") + ": " + "Maximum H Bridge Temperature: "
                            + str(self.maxHTemp) + "\n")
            self.file.write(datetime.now().strftime("%d/%m/%Y %H:%M:%S") + ": " + "Maximum H Bridge Humidity: "
                            + str(self.maxHHum) + "\n")

            self.textbox.setPlainText(self.textbox.toPlainText() + '\n' + datetime.now().strftime("%d/%m/%Y %H:%M:%S")
                                      + ": " + "Maximum Motor Temperature: " + str(self.maxMTemp))
            self.textbox.setPlainText(self.textbox.toPlainText() + '\n' + datetime.now().strftime("%d/%m/%Y %H:%M:%S")
                                      + ": " + "Maximum Motor Humidity: " + str(self.maxMHum))
            self.file.write(datetime.now().strftime("%d/%m/%Y %H:%M:%S") + ": " + "Maximum Motor Temperature: "
                            + str(self.maxMTemp) + "\n")
            self.file.write(datetime.now().strftime("%d/%m/%Y %H:%M:%S") + ": " + "Maximum Motor Humidity: "
                            + str(self.maxMHum) + "\n")

        if voltage_test:
            self.textbox.setPlainText(self.textbox.toPlainText() + '\n' + datetime.now().strftime("%d/%m/%Y %H:%M:%S")
                                      + ": " + "Maximum Supply Voltage: " + str(self.maxVoltage))
            self.textbox.setPlainText(self.textbox.toPlainText() + '\n' + datetime.now().strftime("%d/%m/%Y %H:%M:%S")
                                      + ": " + "Minimum Supply Voltage: " + str(self.minVoltage))
            self.file.write(datetime.now().strftime("%d/%m/%Y %H:%M:%S") + ": " + "Maximum Supply Voltage: "
                            + str(self.maxVoltage) + "\n")
            self.file.write(datetime.now().strftime("%d/%m/%Y %H:%M:%S") + ": " + "Minimum Supply Voltage: "
                            + str(self.minVoltage) + "\n")

        if speed_test:
            self.textbox.setPlainText(self.textbox.toPlainText() + '\n' + datetime.now().strftime("%d/%m/%Y %H:%M:%S")
                                      + ": " + "Maximum Speed: " + str(self.maxSpeed))
            self.textbox.setPlainText(self.textbox.toPlainText() + '\n' + datetime.now().strftime("%d/%m/%Y %H:%M:%S")
                                      + ": " + "Minimum Speed: " + str(self.minSpeed))
            self.file.write(datetime.now().strftime("%d/%m/%Y %H:%M:%S") + ": " + "Maximum Speed: "
                            + str(self.maxSpeed) + "\n")
            self.file.write(datetime.now().strftime("%d/%m/%Y %H:%M:%S") + ": " + "Minimum Speed: "
                            + str(self.minSpeed) + "\n")

        self.textbox.setPlainText(self.textbox.toPlainText() + '\n' + datetime.now().strftime("%d/%m/%Y %H:%M:%S")
                                  + ": " + "Test stopped!")
        self.file.write("\n" + datetime.now().strftime("%d/%m/%Y %H:%M:%S") + ": " + "Test stopped!" + "\n")

        self.pushButton.setEnabled(True)
        self.pushButton_2.setEnabled(False)
        self.send_bytes_to_client("X")
        self.timer.stop()
        self.flagsWindow.draw_flags(self.x_values_for_flags, self.y_values_temperature, self.y_values_voltage,
                                    self.y_values_distance)

        self.testCase1Window.setVisible(False)
        self.testCase2Window.setVisible(False)
        self.testCase3Window.setVisible(False)
        # self.graphWindow.setVisible(False)
        # self.flagsWindow.setVisible(False)
        self.graphWindow.stop_plot()

        self.progressBar.setValue(0)
        self.file.close()
        start_test = False

    def slider_move(self):
        self.rpm = int((self.horizontalSlider.value() * 14000) / 255)
        self.textEdit.setPlainText(str(self.rpm))

    def openTestCase1Window(self):
        self.testCase1Window = window_testcase_1.test1_Window()
        self.testCase1Window.show()
        self.testCase1Window.setVisible(False)

    def openTestCase2Window(self):
        self.testCase2Window = window_testcase_2.test2_Window()
        self.testCase2Window.show()
        self.testCase2Window.setVisible(False)

    def openTestCase3Window(self):
        self.testCase3Window = window_testcase_3.test3_Window()
        self.testCase3Window.show()
        self.testCase3Window.setVisible(False)

    def openGraphWindow(self):
        self.graphWindow = graph_window.GraphWindow()
        self.graphWindow.show()
        self.graphWindow.setVisible(False)

    def openFlagsWindow(self):
        self.flagsWindow = flags_window.FlagsWindow()
        self.flagsWindow.show()
        self.flagsWindow.setVisible(False)

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
        global temperature_fail, speed_fail, voltage_fail, distance_fail

        # add values for x axis
        self.x_values_for_flags.append(self.counter)

        self.counter += 1
        self.progressBar.setValue(int((self.counter * 100) / self.test_time))

        self.y_values_temperature.append(int(temperature_fail))
        self.y_values_voltage.append(int(voltage_fail))
        self.y_values_distance.append(int(distance_fail))

        self.check_temps(float(self.temp), float(self.hum), float(self.motor_temp), float(self.motor_hum))

        if self.temp_box:
            self.testCase1Window.edit_temps(self.temp, self.hum, self.motor_temp, self.motor_hum)

        if self.voltage_box:
            self.testCase2Window.edit_voltage(self.voltage)

        if self.speed_box:
            self.testCase3Window.edit_speed(int(self.speed * self.voltage / 12))

        if voltage_fail:
            self.textbox.setPlainText(
                self.textbox.toPlainText() + '\n' + datetime.now().strftime("%d/%m/%Y %H:%M:%S") + ": "
                + "Test FAILED! Voltage is greater than limit!")
            self.textbox.setPlainText(
                self.textbox.toPlainText() + '\n' + datetime.now().strftime("%d/%m/%Y %H:%M:%S") + ": "
                + "Voltage: " + str(self.voltage))
            self.file.write(datetime.now().strftime("%d/%m/%Y %H:%M:%S") + ": "
                            + "Test FAILED! Voltage is greater than limit!" + "\n")
            self.file.write(datetime.now().strftime("%d/%m/%Y %H:%M:%S") + ": "
                            + "Voltage: " + str(self.voltage) + "\n")

            self.stop()

        if temperature_fail:
            self.textbox.setPlainText(
                self.textbox.toPlainText() + '\n' + datetime.now().strftime("%d/%m/%Y %H:%M:%S") + ": "
                + "Test FAILED! Temperature is greater than limit!")
            self.file.write(datetime.now().strftime("%d/%m/%Y %H:%M:%S") + ": "
                            + "Test FAILED! Temperature is greater than limit!" + "\n")
            self.stop()

        if self.counter > self.test_time:
            self.textbox.setPlainText(self.textbox.toPlainText() + '\n' + datetime.now().strftime("%d/%m/%Y %H:%M:%S")
                                      + ": " + "Test SUCCEED!")
            self.file.write(datetime.now().strftime("%d/%m/%Y %H:%M:%S")
                            + ": " + "Test SUCCEED!" + "\n")
            self.stop()

        if self.distance < 20.0:
            distance_fail = True
            self.y_values_distance.pop()
            self.y_values_distance.append(int(distance_fail))

            self.textbox.setPlainText(self.textbox.toPlainText() + '\n' + datetime.now().strftime("%d/%m/%Y %H:%M:%S")
                                      + ": " + "Distance from motor lower than limit! ")
            self.file.write('\n' + datetime.now().strftime("%d/%m/%Y %H:%M:%S")
                            + ": " + "Distance from motor lower than limit! " + "\n")
            self.textbox.setPlainText(self.textbox.toPlainText() + '\n' + datetime.now().strftime("%d/%m/%Y %H:%M:%S")
                                      + ": " + "Distance:" + str(self.distance))
            self.file.write('\n' + datetime.now().strftime("%d/%m/%Y %H:%M:%S")
                            + ": " + "Distance:" + str(self.distance))
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

import mysql.connector as mc


class Ui_Form(object):
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(352, 271)
        self.lineEditEmail = QtWidgets.QLineEdit(Form)
        self.lineEditEmail.setGeometry(QtCore.QRect(110, 100, 131, 20))
        self.lineEditEmail.setObjectName("lineEdit")
        self.lineEditEmail.setStyleSheet("""QLineEdit{
                                    border-width: 1px;
                                    padding: 1px;
                                    border-style: solid;
                                    border-radius: 10px
                                    }""")

        self.lineEditPassword = QtWidgets.QLineEdit(Form)
        self.lineEditPassword.setGeometry(QtCore.QRect(110, 150, 131, 20))
        self.lineEditPassword.setObjectName("lineEdit_2")
        self.lineEditPassword.setStyleSheet("""QLineEdit{
                                            border-width: 1px;
                                            padding: 1px;
                                            border-style: solid;
                                            border-radius: 10px
                                            }""")
        self.lineEditPassword.setEchoMode(QtWidgets.QLineEdit.Password)

        self.label = QtWidgets.QLabel(Form)
        self.label.setGeometry(QtCore.QRect(160, 80, 47, 13))
        self.label.setObjectName("label")
        self.label_2 = QtWidgets.QLabel(Form)
        self.label_2.setGeometry(QtCore.QRect(150, 130, 47, 13))
        self.label_2.setObjectName("label_2")
        self.pushButton = QtWidgets.QPushButton(Form)
        self.pushButton.setGeometry(QtCore.QRect(120, 190, 111, 23))
        self.pushButton.setObjectName("pushButton")
        self.pushButton.setStyleSheet("""QPushButton {
                                            border-width: 1px;
                                            padding: 1px;
                                            border-style: solid;
                                            border-radius:10px;
                                            background: qlineargradient(
                                                x1:0, y1:0, x2:1, y2:1,
                                                stop: 0.01 orange, stop: 0.8 rgb(255,140,0), stop:0 white
                                            )
                                            }""")
        self.pushButton.clicked.connect(self.login)

        self.labelResult = QtWidgets.QLabel(Form)
        font = QtGui.QFont()
        font.setPointSize(14)
        font.setBold(True)
        font.setWeight(75)
        self.labelResult.setFont(font)
        self.labelResult.setGeometry(QtCore.QRect(16, 230, 321, 20))
        self.labelResult.setText("")
        self.labelResult.setObjectName("labelResult")

        self.image_label = QtWidgets.QLabel(Form)
        self.image_label.setGeometry(QtCore.QRect(65, -20, 350, 120))
        pixmap = QPixmap("Images" + os.path.sep + "conti.png")
        pixmap = pixmap.scaled(300, 100, QtCore.Qt.KeepAspectRatio)
        self.image_label.setPixmap(pixmap)


        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def login(self):
        try:
            email = self.lineEditEmail.text()
            password = self.lineEditPassword.text()

            mydb = mc.connect(
                host="remotemysql.com",
                user="yTDutguUaL",
                password="n2NTQEy74T",
                database="yTDutguUaL"

            )

            mycursor = mydb.cursor()
            query = "SELECT email,password from users where email " \
                    "like '" + email + "'and password like '" \
                    + password + "'"
            mycursor.execute(query)
            result = mycursor.fetchone()

            if result == None:
                self.labelResult.setText("Incorrect email or password")

            else:
                self.labelResult.setText("You are logged in")
                mydialog = Ui_MainWindow()
                MainWindow = QtWidgets.QMainWindow()
                mydialog.setupUi(MainWindow)
                MainWindow.show()


        except mc.Error as e:
            self.labelResult.setText("Error")

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Login", "Login"))
        self.label.setText(_translate("Login", "Email"))
        self.label_2.setText(_translate("Login", "Password"))
        self.pushButton.setText(_translate("Login", "Login"))


def main():
    import sys
    app = QtWidgets.QApplication(sys.argv)
    app.setPalette(palette)
    Form = QtWidgets.QWidget()
    ui = Ui_Form()
    ui.setupUi(Form)
    Form.show()
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()

me = os.getpid()
kill_proc_tree(me)
