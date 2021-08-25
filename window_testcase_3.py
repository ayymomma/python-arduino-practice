from PyQt5.QtWidgets import QWidget
from PyQt5 import QtCore, QtWidgets

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
