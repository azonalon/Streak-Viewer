# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'uidesign/mainWindow.ui'
#
# Created by: PyQt5 UI code generator 5.8
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.setEnabled(True)
        MainWindow.resize(1017, 768)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.gridLayout = QtWidgets.QGridLayout(self.centralwidget)
        self.gridLayout.setObjectName("gridLayout")
        self.verticalLayout = QtWidgets.QVBoxLayout()
        self.verticalLayout.setObjectName("verticalLayout")
        self.areaCalcTreeWidget = QtWidgets.QScrollArea(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(4)
        sizePolicy.setVerticalStretch(2)
        sizePolicy.setHeightForWidth(self.areaCalcTreeWidget.sizePolicy().hasHeightForWidth())
        self.areaCalcTreeWidget.setSizePolicy(sizePolicy)
        self.areaCalcTreeWidget.setWidgetResizable(True)
        self.areaCalcTreeWidget.setObjectName("areaCalcTreeWidget")
        self.bla = QtWidgets.QWidget()
        self.bla.setGeometry(QtCore.QRect(0, 0, 68, 452))
        self.bla.setObjectName("bla")
        self.areaCalcTreeWidget.setWidget(self.bla)
        self.verticalLayout.addWidget(self.areaCalcTreeWidget)
        self.label = QtWidgets.QLabel(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(3)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label.sizePolicy().hasHeightForWidth())
        self.label.setSizePolicy(sizePolicy)
        self.label.setObjectName("label")
        self.verticalLayout.addWidget(self.label)
        self.area_info = QtWidgets.QScrollArea(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(2)
        sizePolicy.setVerticalStretch(1)
        sizePolicy.setHeightForWidth(self.area_info.sizePolicy().hasHeightForWidth())
        self.area_info.setSizePolicy(sizePolicy)
        self.area_info.setWidgetResizable(True)
        self.area_info.setObjectName("area_info")
        self.scrollAreaWidgetContents = QtWidgets.QWidget()
        self.scrollAreaWidgetContents.setGeometry(QtCore.QRect(0, 0, 68, 225))
        self.scrollAreaWidgetContents.setObjectName("scrollAreaWidgetContents")
        self.area_info.setWidget(self.scrollAreaWidgetContents)
        self.verticalLayout.addWidget(self.area_info)
        self.gridLayout.addLayout(self.verticalLayout, 0, 0, 1, 1)
        self.tabWidget = QtWidgets.QTabWidget(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(1)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.tabWidget.sizePolicy().hasHeightForWidth())
        self.tabWidget.setSizePolicy(sizePolicy)
        self.tabWidget.setObjectName("tabWidget")
        self.gridLayout.addWidget(self.tabWidget, 0, 1, 1, 1)
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 1017, 19))
        self.menubar.setObjectName("menubar")
        self.menuDo = QtWidgets.QMenu(self.menubar)
        self.menuDo.setObjectName("menuDo")
        self.menuNodes = QtWidgets.QMenu(self.menuDo)
        self.menuNodes.setObjectName("menuNodes")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)
        self.actionRecalc = QtWidgets.QAction(MainWindow)
        self.actionRecalc.setObjectName("actionRecalc")
        self.actionAddSumNode = QtWidgets.QAction(MainWindow)
        self.actionAddSumNode.setObjectName("actionAddSumNode")
        self.actionAdd_File = QtWidgets.QAction(MainWindow)
        self.actionAdd_File.setObjectName("actionAdd_File")
        self.actionAddPolarizationNode = QtWidgets.QAction(MainWindow)
        self.actionAddPolarizationNode.setObjectName("actionAddPolarizationNode")
        self.actionAutoLevel = QtWidgets.QAction(MainWindow)
        self.actionAutoLevel.setObjectName("actionAutoLevel")
        self.actionSleep = QtWidgets.QAction(MainWindow)
        self.actionSleep.setObjectName("actionSleep")
        self.actionSave = QtWidgets.QAction(MainWindow)
        self.actionSave.setObjectName("actionSave")
        self.menuNodes.addAction(self.actionAddSumNode)
        self.menuNodes.addAction(self.actionAddPolarizationNode)
        self.menuDo.addAction(self.actionRecalc)
        self.menuDo.addAction(self.actionAdd_File)
        self.menuDo.addAction(self.menuNodes.menuAction())
        self.menuDo.addAction(self.actionAutoLevel)
        self.menuDo.addAction(self.actionSleep)
        self.menuDo.addAction(self.actionSave)
        self.menubar.addAction(self.menuDo.menuAction())

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.label.setText(_translate("MainWindow", "Image Info"))
        self.menuDo.setTitle(_translate("MainWindow", "Do..."))
        self.menuNodes.setTitle(_translate("MainWindow", "Add Nodes"))
        self.actionRecalc.setText(_translate("MainWindow", "Recalc"))
        self.actionAddSumNode.setText(_translate("MainWindow", "Sum"))
        self.actionAdd_File.setText(_translate("MainWindow", "Add File"))
        self.actionAddPolarizationNode.setText(_translate("MainWindow", "Polarization"))
        self.actionAutoLevel.setText(_translate("MainWindow", "Auto Level"))
        self.actionSleep.setText(_translate("MainWindow", "Sleep"))
        self.actionSave.setText(_translate("MainWindow", "Save Current Image"))

