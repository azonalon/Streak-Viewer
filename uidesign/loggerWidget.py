# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'StreakViewer/uidesign/loggerWidget.ui'
#
# Created by: PyQt5 UI code generator 5.8
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_Form(object):
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(627, 576)
        self.gridLayout = QtWidgets.QGridLayout(Form)
        self.gridLayout.setObjectName("gridLayout")
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        spacerItem = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_2.addItem(spacerItem)
        self.buttonReset = QtWidgets.QPushButton(Form)
        self.buttonReset.setObjectName("buttonReset")
        self.horizontalLayout_2.addWidget(self.buttonReset)
        self.buttonStart = QtWidgets.QPushButton(Form)
        self.buttonStart.setObjectName("buttonStart")
        self.horizontalLayout_2.addWidget(self.buttonStart)
        self.buttonStop = QtWidgets.QPushButton(Form)
        self.buttonStop.setObjectName("buttonStop")
        self.horizontalLayout_2.addWidget(self.buttonStop)
        self.gridLayout.addLayout(self.horizontalLayout_2, 0, 0, 1, 1)
        self.layoutPlotWidget = QtWidgets.QGridLayout()
        self.layoutPlotWidget.setObjectName("layoutPlotWidget")
        self.gridLayout.addLayout(self.layoutPlotWidget, 1, 0, 1, 1)

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "Form"))
        self.buttonReset.setText(_translate("Form", "Reset"))
        self.buttonStart.setText(_translate("Form", "Start"))
        self.buttonStop.setText(_translate("Form", "Stop"))

