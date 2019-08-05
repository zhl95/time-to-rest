# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'ui_mic.ui'
#
# Created by: PyQt5 UI code generator 5.11.3
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_MicWin(object):
    def setupUi(self, MicWin):
        MicWin.setObjectName("MicWin")
        MicWin.resize(387, 188)
        self.label = QtWidgets.QLabel(MicWin)
        self.label.setGeometry(QtCore.QRect(30, 40, 211, 16))
        self.label.setObjectName("label")
        self.progressBar = QtWidgets.QProgressBar(MicWin)
        self.progressBar.setEnabled(True)
        self.progressBar.setGeometry(QtCore.QRect(120, 70, 118, 23))
        self.progressBar.setProperty("value", 24)
        self.progressBar.setInvertedAppearance(False)
        self.progressBar.setObjectName("progressBar")
        self.widget = QtWidgets.QWidget(MicWin)
        self.widget.setGeometry(QtCore.QRect(40, 120, 295, 30))
        self.widget.setObjectName("widget")
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.widget)
        self.horizontalLayout.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.OK = QtWidgets.QPushButton(self.widget)
        self.OK.setObjectName("OK")
        self.horizontalLayout.addWidget(self.OK)
        self.overdraft = QtWidgets.QPushButton(self.widget)
        self.overdraft.setObjectName("overdraft")
        self.horizontalLayout.addWidget(self.overdraft)
        self.reset = QtWidgets.QPushButton(self.widget)
        self.reset.setObjectName("reset")
        self.horizontalLayout.addWidget(self.reset)

        self.retranslateUi(MicWin)
        QtCore.QMetaObject.connectSlotsByName(MicWin)

    def retranslateUi(self, MicWin):
        _translate = QtCore.QCoreApplication.translate
        MicWin.setWindowTitle(_translate("MicWin", "Dialog"))
        self.label.setText(_translate("MicWin", "time to take a small break"))
        self.progressBar.setFormat(_translate("MicWin", "%p%"))
        self.OK.setText(_translate("MicWin", "OK"))
        self.overdraft.setText(_translate("MicWin", "overdraft"))
        self.reset.setText(_translate("MicWin", "reset"))

