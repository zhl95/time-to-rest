# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'ui_timer.ui'
#
# Created by: PyQt5 UI code generator 5.11.3
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_TimerWin(object):
    def setupUi(self, TimerWin):
        TimerWin.setObjectName("TimerWin")
        TimerWin.resize(612, 198)
        self.widget = QtWidgets.QWidget(TimerWin)
        self.widget.setGeometry(QtCore.QRect(61, 28, 182, 88))
        self.widget.setObjectName("widget")
        self.gridLayout = QtWidgets.QGridLayout(self.widget)
        self.gridLayout.setContentsMargins(0, 0, 0, 0)
        self.gridLayout.setObjectName("gridLayout")
        self.label = QtWidgets.QLabel(self.widget)
        self.label.setObjectName("label")
        self.gridLayout.addWidget(self.label, 0, 0, 1, 1)
        self.mic_work_pbar = QtWidgets.QProgressBar(self.widget)
        self.mic_work_pbar.setMaximum(60)
        self.mic_work_pbar.setProperty("value", 24)
        self.mic_work_pbar.setObjectName("mic_work_pbar")
        self.gridLayout.addWidget(self.mic_work_pbar, 0, 1, 1, 1)
        self.label_2 = QtWidgets.QLabel(self.widget)
        self.label_2.setObjectName("label_2")
        self.gridLayout.addWidget(self.label_2, 1, 0, 1, 1)
        self.mac_work_pbar = QtWidgets.QProgressBar(self.widget)
        self.mac_work_pbar.setMaximum(200)
        self.mac_work_pbar.setProperty("value", 24)
        self.mac_work_pbar.setObjectName("mac_work_pbar")
        self.gridLayout.addWidget(self.mac_work_pbar, 1, 1, 1, 1)
        self.label_3 = QtWidgets.QLabel(self.widget)
        self.label_3.setObjectName("label_3")
        self.gridLayout.addWidget(self.label_3, 2, 0, 1, 1)
        self.total_pbar = QtWidgets.QProgressBar(self.widget)
        self.total_pbar.setMaximum(1000)
        self.total_pbar.setProperty("value", 24)
        self.total_pbar.setObjectName("total_pbar")
        self.gridLayout.addWidget(self.total_pbar, 2, 1, 1, 1)

        self.retranslateUi(TimerWin)
        QtCore.QMetaObject.connectSlotsByName(TimerWin)

    def retranslateUi(self, TimerWin):
        _translate = QtCore.QCoreApplication.translate
        TimerWin.setWindowTitle(_translate("TimerWin", "Dialog"))
        self.label.setText(_translate("TimerWin", "mic-break"))
        self.label_2.setText(_translate("TimerWin", "mac-break"))
        self.label_3.setText(_translate("TimerWin", "total"))

