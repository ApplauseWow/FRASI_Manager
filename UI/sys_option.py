# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'sys_option.ui'
#
# Created by: PyQt5 UI code generator 5.4.2
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_sys_option(object):
    def setupUi(self, sys_option):
        sys_option.setObjectName("sys_option")
        sys_option.resize(296, 300)
        sys_option.setStyleSheet("background-color: rgb(255, 255, 255);")
        self.buttonBox = QtWidgets.QDialogButtonBox(sys_option)
        self.buttonBox.setGeometry(QtCore.QRect(100, 240, 171, 32))
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtWidgets.QDialogButtonBox.Cancel|QtWidgets.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName("buttonBox")
        self.formLayoutWidget = QtWidgets.QWidget(sys_option)
        self.formLayoutWidget.setGeometry(QtCore.QRect(60, 50, 191, 81))
        self.formLayoutWidget.setObjectName("formLayoutWidget")
        self.formLayout = QtWidgets.QFormLayout(self.formLayoutWidget)
        self.formLayout.setObjectName("formLayout")
        self.label = QtWidgets.QLabel(self.formLayoutWidget)
        font = QtGui.QFont()
        font.setPointSize(16)
        font.setItalic(True)
        self.label.setFont(font)
        self.label.setObjectName("label")
        self.formLayout.setWidget(0, QtWidgets.QFormLayout.LabelRole, self.label)
        self.label_2 = QtWidgets.QLabel(self.formLayoutWidget)
        font = QtGui.QFont()
        font.setPointSize(16)
        font.setItalic(True)
        self.label_2.setFont(font)
        self.label_2.setObjectName("label_2")
        self.formLayout.setWidget(1, QtWidgets.QFormLayout.LabelRole, self.label_2)
        self.sign_in_count = QtWidgets.QLineEdit(self.formLayoutWidget)
        font = QtGui.QFont()
        font.setPointSize(16)
        font.setItalic(True)
        self.sign_in_count.setFont(font)
        self.sign_in_count.setAlignment(QtCore.Qt.AlignCenter)
        self.sign_in_count.setObjectName("sign_in_count")
        self.formLayout.setWidget(1, QtWidgets.QFormLayout.FieldRole, self.sign_in_count)
        self.recognition_count = QtWidgets.QLineEdit(self.formLayoutWidget)
        font = QtGui.QFont()
        font.setPointSize(16)
        font.setItalic(True)
        self.recognition_count.setFont(font)
        self.recognition_count.setAlignment(QtCore.Qt.AlignCenter)
        self.recognition_count.setObjectName("recognition_count")
        self.formLayout.setWidget(0, QtWidgets.QFormLayout.FieldRole, self.recognition_count)

        self.retranslateUi(sys_option)
        self.buttonBox.accepted.connect(sys_option.accept)
        self.buttonBox.rejected.connect(sys_option.reject)
        QtCore.QMetaObject.connectSlotsByName(sys_option)

    def retranslateUi(self, sys_option):
        _translate = QtCore.QCoreApplication.translate
        sys_option.setWindowTitle(_translate("sys_option", "System Option"))
        self.label.setText(_translate("sys_option", "识别帧数"))
        self.label_2.setText(_translate("sys_option", "注册帧数"))
        self.sign_in_count.setText(_translate("sys_option", "4"))
        self.recognition_count.setText(_translate("sys_option", "3"))

