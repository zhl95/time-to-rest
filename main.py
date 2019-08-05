# -*- coding: utf-8 -*-
import cv2
import numpy as np
import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QFileDialog, QDialog
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from ui.ui_window import Ui_MainWindow
from ui.ui_timer import Ui_TimerWin
from ui.ui_mic import Ui_MicWin
from ui.ui_mac import Ui_MacWin
from logic.param_rt import ParamSetter
from logic.fileIO import FileIO
from logic.mange import Manager
from logic.timing import Timing
# from . import detect_thread as detect
import detect_thread as detect

from easydict import EasyDict as edict
from pprint import pprint

class MainForm(QMainWindow, Ui_MainWindow):
    def __init__(self):
        print(super(MainForm, self))
        # print(dir(MainForm))
        super(MainForm, self).__init__()
        # QMainWindow.__init__()
        self.setupUi(self)

        self.timer_win = TimerWin()
        self.mic_win = MicWin()
        self.mac_win = MacWin()

        self.cap_thread = detect.CapThread()
        self.detect_thread = detect.WorkThread()
        self.detector = detect.Detector()
        self.param_setter = ParamSetter(self)
        self.manager = Manager(self)
        self.timing = Timing(self)
        self.fileIO = FileIO(self)


        self.setup_logic()



    def setup_logic(self):
        self.get_value_push.clicked.connect(self.param_setter.get_values)


        self.fileIO.set_logic()
        self.timing.set_logic()
        self.manager.set_logic()

        def work():
            self.detect_thread.start()
            # 当获得循环完毕的信号时，停止计数
            self.detect_thread.trigger.connect(timeStop)
        def timeStop():
            # it will be printed multi times, I think it is because the clicked mouse is multi times, might be better for using pressed.
            print("detecttion finished")
            cv2.imshow("Face Detection Comparison", self.detect_thread.detected)

        # self.start_push.clicked.connect(work)
        self.start_push.clicked.connect(self.timing.timer.start)
        self.start_push.clicked.connect(self.manager.start_timer)




    # def btnstate(self, btn):
    #     if btn.text() == "Buttonl":
    #         if btn.isChecked() == True:
    #             print(btn.text() + " is selected")
    #         else:
    #             print(btn.text() + " is deselected")
    #     if btn.text() == "Button2":
    #         if btn.isChecked() == True:
    #             print(btn.text() + " is selected")
    #         else:
    #             print(btn.text() + " is deselected")


class TimerWin(QDialog, Ui_TimerWin):
    def __init__(self):
        super(TimerWin, self).__init__()
        self.setupUi(self)


class MicWin(QDialog, Ui_MicWin):
    def __init__(self):
        super(MicWin, self).__init__()
        self.setupUi(self)


class MacWin(QDialog, Ui_MacWin):
    def __init__(self):
        super(MacWin, self).__init__()
        self.setupUi(self)




if __name__ == "__main__":
    app = QApplication(sys.argv)
    win = MainForm()
    # win.timer_win = TimerWin()
    # win.resize(500, 500)
    win.show()
    sys.exit(app.exec_())
