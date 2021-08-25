
from PyQt5.QtWidgets import QWidget

import settings, threading
from PyQt5 import QtCore, QtGui, QtWidgets

class MyGraphicsView(QtWidgets.QGraphicsView):
    def __init__(self, parent):
        QtWidgets.QGraphicsView.__init__(self, parent)
        self.setMouseTracking(True)

    def mouseMoveEvent(self, event):
        settings.x_value_mouse_move = event.pos().x()
        print(event.pos().x())


class FlagsWindow(QWidget):
    def __init__(self, parent=None):
        super(FlagsWindow, self).__init__(parent)
        self.setupUi()
        self.x_vals = []
        self.y_temp = []
        self.y_volt = []
        self.y_dist = []
        self.fsf_vals = [1] * 30
        self.stop = False

    def setupUi(self):
        self.setObjectName("Form")
        self.resize(1100, 400)
        self.setStyleSheet("background-color: rgb(56, 56, 56);")
        self.line = QtWidgets.QFrame(self)
        self.line.setGeometry(QtCore.QRect(0, 60, 1081, 16))
        self.line.setFrameShape(QtWidgets.QFrame.HLine)
        self.line.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line.setObjectName("line")
        self.line_2 = QtWidgets.QFrame(self)
        self.line_2.setGeometry(QtCore.QRect(470, 0, 20, 721))
        self.line_2.setFrameShape(QtWidgets.QFrame.VLine)
        self.line_2.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line_2.setObjectName("line_2")
        self.line_3 = QtWidgets.QFrame(self)
        self.line_3.setGeometry(QtCore.QRect(250, 0, 20, 731))
        self.line_3.setFrameShape(QtWidgets.QFrame.VLine)
        self.line_3.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line_3.setObjectName("line_3")
        self.lineEdit = QtWidgets.QLineEdit(self)
        self.lineEdit.setGeometry(QtCore.QRect(60, 11, 121, 41))
        self.lineEdit.setStyleSheet("background-color: rgb(0, 0, 0);")
        self.lineEdit.setObjectName("lineEdit")
        self.lineEdit.setAlignment(QtCore.Qt.AlignCenter)
        self.lineEdit.setReadOnly(True)
        self.lineEdit_2 = QtWidgets.QLineEdit(self)
        self.lineEdit_2.setGeometry(QtCore.QRect(300, 10, 121, 41))
        self.lineEdit_2.setStyleSheet("background-color: rgb(0, 0, 0);")
        self.lineEdit_2.setObjectName("lineEdit_2")
        self.lineEdit_2.setAlignment(QtCore.Qt.AlignCenter)
        self.lineEdit_2.setReadOnly(True)
        self.label = QtWidgets.QLabel(self)
        self.label.setGeometry(QtCore.QRect(20, 90, 181, 31))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.label.setFont(font)
        self.label.setStyleSheet("color: red;\n"
                                 "\n"
                                 "")
        self.label.setObjectName("label")
        self.label_3 = QtWidgets.QLabel(self)
        self.label_3.setGeometry(QtCore.QRect(20, 220, 81, 16))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.label_3.setFont(font)
        self.label_3.setStyleSheet("color: blue;\n"
                                   "")
        self.label_3.setObjectName("label_3")

        self.label_5 = QtWidgets.QLabel(self)
        self.label_5.setGeometry(QtCore.QRect(20, 160, 141, 16))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.label_5.setFont(font)
        self.label_5.setStyleSheet("color: yellow;")
        self.label_5.setObjectName("label_5")

        self.label_6 = QtWidgets.QLabel(self)
        self.label_6.setGeometry(QtCore.QRect(20, 280, 81, 16))
        self.label_6.setFont(font)
        self.label_6.setStyleSheet("color: green;")
        self.label_6.setObjectName("label_6")

        self.lineEdit_3 = QtWidgets.QLineEdit(self)
        self.lineEdit_3.setGeometry(QtCore.QRect(300, 100, 113, 22))
        self.lineEdit_3.setStyleSheet("border-color: rgb(56, 56, 56);\n"
                                      "border-width : 1.2px;\n"
                                      "border-style:inset;")
        self.lineEdit_3.setObjectName("lineEdit_3")
        self.lineEdit_3.setAlignment(QtCore.Qt.AlignCenter)
        self.lineEdit_4 = QtWidgets.QLineEdit(self)
        self.lineEdit_4.setGeometry(QtCore.QRect(300, 160, 113, 22))
        self.lineEdit_4.setStyleSheet("border-color: rgb(56, 56, 56);\n"
                                      "border-width : 1.2px;\n"
                                      "border-style:inset;")
        self.lineEdit_4.setObjectName("lineEdit_4")
        self.lineEdit_4.setAlignment(QtCore.Qt.AlignCenter)
        self.lineEdit_5 = QtWidgets.QLineEdit(self)
        self.lineEdit_5.setGeometry(QtCore.QRect(300, 220, 113, 22))
        self.lineEdit_5.setStyleSheet("border-color: rgb(56, 56, 56);\n"
                                      "border-width : 1.2px;\n"
                                      "border-style:inset;")
        self.lineEdit_5.setObjectName("lineEdit_5")
        self.lineEdit_5.setAlignment(QtCore.Qt.AlignCenter)

        self.lineEdit_6 = QtWidgets.QLineEdit(self)
        self.lineEdit_6.setGeometry(QtCore.QRect(300, 280, 113, 22))
        self.lineEdit_6.setStyleSheet("border-color: rgb(56, 56, 56);\n"
                                      "border-width : 1.2px;\n"
                                      "border-style:inset;")
        self.lineEdit_6.setObjectName("lineEdit_6")
        self.lineEdit_6.setAlignment(QtCore.Qt.AlignCenter)

        self.graphicsView = MyGraphicsView(self)
        self.graphicsView.setGeometry(QtCore.QRect(490, 80, 560, 270))
        self.graphicsView.setObjectName("graphicsView")

        self.retranslateUi()
        QtCore.QMetaObject.connectSlotsByName(self)

    def retranslateUi(self):
        _translate = QtCore.QCoreApplication.translate
        self.setWindowTitle(_translate("Form", "Flags Window"))
        self.lineEdit.setText(_translate("Form", "VARIABLES NAME"))
        self.lineEdit_2.setText(_translate("Form", "VALUES"))
        self.label.setText(_translate("Form", "H-Bridge & Motor Temperature"))
        self.label_3.setText(_translate("Form", "Ultrasonic Sensor"))
        self.label_5.setText(_translate("Form", "DC - Link"))
        self.label_6.setText(_translate("Form", "Motor State"))

    def draw_flags(self, x_vals, y_temp_vals, y_voltage_vals, y_distance_vals):
        self.scene = QtWidgets.QGraphicsScene()
        self.graphicsView.setScene(self.scene)

        self.x_vals = x_vals
        self.y_temp = y_temp_vals
        self.y_volt = y_voltage_vals
        self.y_dist = y_distance_vals

        self.fsf_vals = [1] * 30

        for i in range(1, len(x_vals)):
            red_pen = QtGui.QPen(QtCore.Qt.red)
            yellow_pen = QtGui.QPen(QtCore.Qt.yellow)
            blue_pen = QtGui.QPen(QtCore.Qt.blue)
            green_pen = QtGui.QPen(QtCore.Qt.green)
            if y_temp_vals[i] == 1:
                self.fsf_vals[i] = 2
                for j in range(i + 1, len(self.fsf_vals)):
                    self.fsf_vals[j] = 0
                r = QtCore.QLineF(QtCore.QPoint((x_vals[i - 1] * 19) * 1, (y_temp_vals[i - 1] * 20) * (-1)),
                                  QtCore.QPoint((x_vals[i - 1] * 19) * 1, (y_temp_vals[i] * 20) * (-1)))
                self.scene.addLine(r, red_pen)
                r = QtCore.QLineF(QtCore.QPoint((x_vals[i - 1] * 19) * 1, (y_temp_vals[i] * 20) * (-1)),
                                  QtCore.QPoint((x_vals[i] * 19) * 1, (y_temp_vals[i] * 20) * (-1)))
                self.scene.addLine(r, red_pen)
                r = QtCore.QLineF(QtCore.QPoint((x_vals[i] * 19) * 1, (y_temp_vals[i - 1] * 20) * (-1)),
                                  QtCore.QPoint((x_vals[i] * 19) * 1, (y_temp_vals[i] * 20) * (-1)))
                self.scene.addLine(r, red_pen)
            else:
                if y_temp_vals[i - 1] == 1:
                    r = QtCore.QLineF(QtCore.QPoint((x_vals[i - 1] * 19) * 1, (y_temp_vals[i] * 20) * (-1)),
                                      QtCore.QPoint((x_vals[i] * 19) * 1, (y_temp_vals[i] * 20) * (-1)))
                    self.scene.addLine(r, red_pen)
                else:
                    r = QtCore.QLineF(QtCore.QPoint((x_vals[i - 1] * 19) * 1, (y_temp_vals[i] * 20) * (-1)),
                                      QtCore.QPoint((x_vals[i] * 19) * 1, (y_temp_vals[i - 1] * 20) * (-1)))
                    self.scene.addLine(r, red_pen)

            if y_voltage_vals[i] == 1:
                self.fsf_vals[i] = 3
                for j in range(i + 1, len(self.fsf_vals)):
                    self.fsf_vals[j] = 0
                r = QtCore.QLineF(QtCore.QPoint((x_vals[i - 1] * 19) * 1, (y_voltage_vals[i - 1] * 20 - 50) * (-1)),
                                  QtCore.QPoint((x_vals[i - 1] * 19) * 1, (y_voltage_vals[i] * 20 - 50) * (-1)))
                self.scene.addLine(r, yellow_pen)
                r = QtCore.QLineF(QtCore.QPoint((x_vals[i - 1] * 19) * 1, (y_voltage_vals[i] * 20 - 50) * (-1)),
                                  QtCore.QPoint((x_vals[i] * 19) * 1, (y_voltage_vals[i] * 20 - 50) * (-1)))
                self.scene.addLine(r, yellow_pen)
                r = QtCore.QLineF(QtCore.QPoint((x_vals[i] * 19) * 1, (y_voltage_vals[i] * 20 - 50) * (-1)),
                                  QtCore.QPoint((x_vals[i] * 19) * 1, (y_voltage_vals[i - 1] * 20 - 50) * (-1)))
                self.scene.addLine(r, yellow_pen)
            else:
                if y_voltage_vals[i - 1] == 1:
                    r = QtCore.QLineF(QtCore.QPoint((x_vals[i - 1] * 19) * 1, (y_voltage_vals[i] * 20 - 50) * (-1)),
                                      QtCore.QPoint((x_vals[i] * 19) * 1, (y_voltage_vals[i] * 20 - 50) * (-1)))
                    self.scene.addLine(r, yellow_pen)
                else:
                    r = QtCore.QLineF(QtCore.QPoint((x_vals[i - 1] * 19) * 1, (y_voltage_vals[i - 1] * 20 - 50) * (-1)),
                                      QtCore.QPoint((x_vals[i] * 19) * 1, (y_voltage_vals[i] * 20 - 50) * (-1)))
                    self.scene.addLine(r, yellow_pen)

            if y_distance_vals[i] == 1:
                self.fsf_vals[i] = 4
                for j in range(i + 1, len(self.fsf_vals)):
                    self.fsf_vals[j] = 0
                r = QtCore.QLineF(QtCore.QPoint((x_vals[i - 1] * 19) * 1, (y_distance_vals[i - 1] * 20 - 100) * (-1)),
                                  QtCore.QPoint(((x_vals[i - 1]) * 19) * 1, (y_distance_vals[i] * 20 - 100) * (-1)))
                self.scene.addLine(r, blue_pen)
                r = QtCore.QLineF(QtCore.QPoint((x_vals[i - 1] * 19) * 1, (y_distance_vals[i] * 20 - 100) * (-1)),
                                  QtCore.QPoint((x_vals[i] * 19) * 1, (y_distance_vals[i] * 20 - 100) * (-1)))
                self.scene.addLine(r, blue_pen)
                r = QtCore.QLineF(QtCore.QPoint((x_vals[i] * 19) * 1, (y_distance_vals[i] * 20 - 100) * (-1)),
                                  QtCore.QPoint((x_vals[i] * 19) * 1, (y_distance_vals[i - 1] * 20 - 100) * (-1)))
                self.scene.addLine(r, blue_pen)
            else:
                if y_distance_vals[i - 1] == 1:
                    r = QtCore.QLineF(
                        QtCore.QPoint((x_vals[i - 1] * 19) * 1, (y_distance_vals[i] * 20 - 100) * (-1)),
                        QtCore.QPoint((x_vals[i] * 19) * 1, (y_distance_vals[i] * 20 - 100) * (-1)))
                    self.scene.addLine(r, blue_pen)
                else:
                    r = QtCore.QLineF(
                        QtCore.QPoint((x_vals[i - 1] * 19) * 1, (y_distance_vals[i - 1] * 20 - 100) * (-1)),
                        QtCore.QPoint((x_vals[i] * 19) * 1, (y_distance_vals[i] * 20 - 100) * (-1)))
                    self.scene.addLine(r, blue_pen)

            if self.fsf_vals[i] == 2 or self.fsf_vals[i] == 3 or self.fsf_vals[i] == 4:
                r = QtCore.QLineF(QtCore.QPoint((x_vals[i - 1] * 19) * 1, (self.fsf_vals[i - 1] * 20 - 200) * (-1)),
                                  QtCore.QPoint((x_vals[i - 1] * 19) * 1, (self.fsf_vals[i] * 20 - 200) * (-1)))
                self.scene.addLine(r, green_pen)
                r = QtCore.QLineF(QtCore.QPoint((x_vals[i - 1] * 19) * 1, (self.fsf_vals[i] * 20 - 200) * (-1)),
                                  QtCore.QPoint((x_vals[i] * 19) * 1, (self.fsf_vals[i] * 20 - 200) * (-1)))
                self.scene.addLine(r, green_pen)
                r = QtCore.QLineF(QtCore.QPoint((x_vals[i] * 19) * 1, (self.fsf_vals[i - 1] * 20 - 200) * (-1)),
                                  QtCore.QPoint((x_vals[i] * 19) * 1, (self.fsf_vals[i] * 20 - 200) * (-1)))
                self.scene.addLine(r, green_pen)
                r = QtCore.QLineF(QtCore.QPoint((x_vals[i] * 19) * 1, (20 - 200) * (-1)),
                                  QtCore.QPoint((x_vals[i] * 19) * 1, (- 200) * (-1)))
                self.scene.addLine(r, green_pen)
            else:
                if self.fsf_vals[i - 1] == 2 or self.fsf_vals[i - 1] == 3 or self.fsf_vals[i - 1] == 4:
                    r = QtCore.QLineF(
                        QtCore.QPoint((x_vals[i - 1] * 19) * 1, (self.fsf_vals[i] * 20 - 200) * (-1)),
                        QtCore.QPoint((x_vals[i] * 19) * 1, (self.fsf_vals[i] * 20 - 200) * (-1)))
                    self.scene.addLine(r, green_pen)
                else:
                    r = QtCore.QLineF(QtCore.QPoint((x_vals[i - 1] * 19) * 1, (self.fsf_vals[i - 1] * 20 - 200) * (-1)),
                                      QtCore.QPoint((x_vals[i] * 19) * 1, (self.fsf_vals[i] * 20 - 200) * (-1)))
                    self.scene.addLine(r, green_pen)

        self.stop = False
        self.thr = threading.Thread(target=self.change_values)
        self.thr.start()

    def change_values(self):
        while not self.stop:
            self.lineEdit_3.setText(str(self.y_temp[int(settings.x_value_mouse_move / 20 + 1)]))
            self.lineEdit_4.setText(str(self.y_volt[int(settings.x_value_mouse_move / 20 + 1)]))
            self.lineEdit_5.setText(str(self.y_dist[int(settings.x_value_mouse_move / 20 + 1)]))
            self.lineEdit_6.setText(str(self.fsf_vals[int(settings.x_value_mouse_move / 20 + 1)]))

    def closeEvent(self, event):
        self.stop = True
