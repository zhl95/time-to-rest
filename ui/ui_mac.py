# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'ui_mac.ui'
#
# Created by: PyQt5 UI code generator 5.11.3
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_MacWin(object):
    def setupUi(self, MacWin):
        MacWin.setObjectName("MacWin")
        MacWin.resize(489, 167)
        self.label = QtWidgets.QLabel(MacWin)
        self.label.setGeometry(QtCore.QRect(130, 20, 211, 16))
        self.label.setObjectName("label")
        self.layoutWidget = QtWidgets.QWidget(MacWin)
        self.layoutWidget.setGeometry(QtCore.QRect(90, 90, 295, 30))
        self.layoutWidget.setObjectName("layoutWidget")
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.layoutWidget)
        self.horizontalLayout.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.OK = QtWidgets.QPushButton(self.layoutWidget)
        self.OK.setObjectName("OK")
        self.horizontalLayout.addWidget(self.OK)
        self.overdraft = QtWidgets.QPushButton(self.layoutWidget)
        self.overdraft.setObjectName("overdraft")
        self.horizontalLayout.addWidget(self.overdraft)
        self.reset = QtWidgets.QPushButton(self.layoutWidget)
        self.reset.setObjectName("reset")
        self.horizontalLayout.addWidget(self.reset)
        self.progressBar = QtWidgets.QProgressBar(MacWin)
        self.progressBar.setEnabled(True)
        self.progressBar.setGeometry(QtCore.QRect(210, 40, 118, 23))
        self.progressBar.setProperty("value", 24)
        self.progressBar.setInvertedAppearance(False)
        self.progressBar.setObjectName("progressBar")

        self.retranslateUi(MacWin)
        QtCore.QMetaObject.connectSlotsByName(MacWin)

    def retranslateUi(self, MacWin):
        _translate = QtCore.QCoreApplication.translate
        MacWin.setWindowTitle(_translate("MacWin", "Dialog"))
        self.label.setText(_translate("MacWin", "time to take a macro break"))
        self.OK.setText(_translate("MacWin", "OK"))
        self.overdraft.setText(_translate("MacWin", "overdraft"))
        self.reset.setText(_translate("MacWin", "reset"))
        self.progressBar.setFormat(_translate("MacWin", "%p%"))

