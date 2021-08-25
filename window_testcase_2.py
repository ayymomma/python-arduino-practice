from PyQt5.QtWidgets import QWidget
from PyQt5 import QtCore, QtWidgets

class test2_Window(QWidget):
    def __init__(self, parent=None):
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
