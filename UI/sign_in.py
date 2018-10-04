# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'sign_in.ui'
#
# Created by: PyQt5 UI code generator 5.4.2
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_Sign_In_UI(object):
    def setupUi(self, Sign_In_UI):
        Sign_In_UI.setObjectName("Sign_In_UI")
        Sign_In_UI.resize(696, 543)
        Sign_In_UI.setStyleSheet("background-color: rgb(255, 255, 255);")
        self.frame_button = QtWidgets.QDialogButtonBox(Sign_In_UI)
        self.frame_button.setGeometry(QtCore.QRect(310, 480, 341, 32))
        self.frame_button.setStyleSheet("background-color: rgb(255, 255, 255);")
        self.frame_button.setOrientation(QtCore.Qt.Horizontal)
        self.frame_button.setStandardButtons(QtWidgets.QDialogButtonBox.Cancel|QtWidgets.QDialogButtonBox.Ok)
        self.frame_button.setObjectName("frame_button")

        self.retranslateUi(Sign_In_UI)
        self.frame_button.accepted.connect(Sign_In_UI.accept)
        self.frame_button.rejected.connect(Sign_In_UI.reject)
        QtCore.QMetaObject.connectSlotsByName(Sign_In_UI)

    def retranslateUi(self, Sign_In_UI):
        _translate = QtCore.QCoreApplication.translate
        Sign_In_UI.setWindowTitle(_translate("Sign_In_UI", "Sign In"))

