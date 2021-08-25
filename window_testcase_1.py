from PyQt5.QtWidgets import QWidget
from PyQt5 import QtCore, QtWidgets


class test1_Window(QWidget):
    def __init__(self, parent=None):
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

    def edit_temps(self, htemp, hhum, mtemp, mhum):
        self.lineEdit.setText(str(htemp))
        self.lineEdit_3.setText(str(hhum))
        self.lineEdit_2.setText(str(mtemp))
        self.lineEdit_4.setText(str(mhum))

    def closeEvent(self, event):
        event.ignore()

