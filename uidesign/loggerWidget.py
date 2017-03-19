# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file '/home/eduard/programming/Streak-Viewer/StreakViewer/uidesign/loggerWidget.ui'
#
# Created by: PyQt5 UI code generator 5.8
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_Form(object):
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(689, 589)
        self.gridLayout = QtWidgets.QGridLayout(Form)
        self.gridLayout.setObjectName("gridLayout")
        self.layoutPlotWidget = QtWidgets.QGridLayout()
        self.layoutPlotWidget.setObjectName("layoutPlotWidget")
        self.gridLayout.addLayout(self.layoutPlotWidget, 0, 0, 1, 1)
        self.layoutMenu = QtWidgets.QVBoxLayout()
        self.layoutMenu.setObjectName("layoutMenu")
        spacerItem = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.layoutMenu.addItem(spacerItem)
        self.gridLayout.addLayout(self.layoutMenu, 0, 1, 1, 1)

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "Form"))

