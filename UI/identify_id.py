# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'identify_id.ui'
#
# Created by: PyQt5 UI code generator 5.4.2
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_Identity_ID_UI(object):
    def setupUi(self, Identity_ID_UI):
        Identity_ID_UI.setObjectName("Identity_ID_UI")
        Identity_ID_UI.resize(402, 219)
        Identity_ID_UI.setStyleSheet("background-color: rgb(255, 255, 255);")
        self.formLayoutWidget = QtWidgets.QWidget(Identity_ID_UI)
        self.formLayoutWidget.setGeometry(QtCore.QRect(30, 80, 341, 41))
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
        self.id_input = QtWidgets.QLineEdit(self.formLayoutWidget)
        font = QtGui.QFont()
        font.setPointSize(14)
        font.setItalic(True)
        self.id_input.setFont(font)
        self.id_input.setAlignment(QtCore.Qt.AlignCenter)
        self.id_input.setObjectName("id_input")
        self.formLayout.setWidget(0, QtWidgets.QFormLayout.FieldRole, self.id_input)
        self.tip = QtWidgets.QLabel(Identity_ID_UI)
        self.tip.setEnabled(False)
        self.tip.setGeometry(QtCore.QRect(30, 130, 211, 17))
        font = QtGui.QFont()
        font.setItalic(True)
        font.setUnderline(True)
        self.tip.setFont(font)
        self.tip.setStyleSheet("color: rgb(255, 67, 10);")
        self.tip.setText("")
        self.tip.setObjectName("tip")
        self.ok = QtWidgets.QPushButton(Identity_ID_UI)
        self.ok.setGeometry(QtCore.QRect(300, 170, 71, 27))
        font = QtGui.QFont()
        font.setPointSize(14)
        font.setItalic(True)
        self.ok.setFont(font)
        self.ok.setObjectName("ok")
        self.cancel = QtWidgets.QPushButton(Identity_ID_UI)
        self.cancel.setGeometry(QtCore.QRect(210, 170, 71, 27))
        font = QtGui.QFont()
        font.setPointSize(14)
        font.setItalic(True)
        self.cancel.setFont(font)
        self.cancel.setObjectName("cancel")
        self.formLayoutWidget_2 = QtWidgets.QWidget(Identity_ID_UI)
        self.formLayoutWidget_2.setGeometry(QtCore.QRect(30, 30, 341, 41))
        self.formLayoutWidget_2.setObjectName("formLayoutWidget_2")
        self.formLayout_2 = QtWidgets.QFormLayout(self.formLayoutWidget_2)
        self.formLayout_2.setObjectName("formLayout_2")
        self.label_2 = QtWidgets.QLabel(self.formLayoutWidget_2)
        font = QtGui.QFont()
        font.setPointSize(11)
        font.setItalic(True)
        self.label_2.setFont(font)
        self.label_2.setObjectName("label_2")
        self.formLayout_2.setWidget(0, QtWidgets.QFormLayout.LabelRole, self.label_2)
        self.name_input = QtWidgets.QLineEdit(self.formLayoutWidget_2)
        font = QtGui.QFont()
        font.setPointSize(14)
        font.setItalic(True)
        self.name_input.setFont(font)
        self.name_input.setAlignment(QtCore.Qt.AlignCenter)
        self.name_input.setObjectName("name_input")
        self.formLayout_2.setWidget(0, QtWidgets.QFormLayout.FieldRole, self.name_input)

        self.retranslateUi(Identity_ID_UI)
        QtCore.QMetaObject.connectSlotsByName(Identity_ID_UI)

    def retranslateUi(self, Identity_ID_UI):
        _translate = QtCore.QCoreApplication.translate
        Identity_ID_UI.setWindowTitle(_translate("Identity_ID_UI", "Identify ID"))
        self.label.setText(_translate("Identity_ID_UI", "请输入ID："))
        self.id_input.setText(_translate("Identity_ID_UI", "201610414206"))
        self.ok.setText(_translate("Identity_ID_UI", "ok"))
        self.cancel.setText(_translate("Identity_ID_UI", "cancel"))
        self.label_2.setText(_translate("Identity_ID_UI", "姓名小写拼音："))
        self.name_input.setText(_translate("Identity_ID_UI", "201610414206"))

