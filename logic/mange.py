import os
import sys
import cv2
import numpy as np

from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QFileDialog
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5 import QtCore
from easydict import EasyDict as edict
from .helper import *


class Manager(QtWidgets.QWidget):

    def __init__(self, mainWiz):
        self.mainWiz = mainWiz
        wz = self.mainWiz
        super(Manager, self).__init__()
        self.check_timer = QBasicTimer()
        self.counter = edict()
        self.checking = False
        self.init_counter()
        self.cam_param = wz.param_setter.params.camera


        # camera = edict()
        # camera.sample_period = [0, 0, 0]
        # camera.sample_duration = [0, 0, 0]
        # self.params.camera = camera

    def init_counter(self):
        self.counter.waiting_check = 0
        self.counter.already_check = 0
        self.counter.active_counts = 0


    def start_timer(self):
        self.check_timer.start(50, self)

    @pyqtSlot(object)
    def check_detected(self, bbox):
        # bbox = self.mainWiz.
        if bbox:
            self.counter.active_counts += 1


    def timerEvent(self, event): # 50ms trigger or 100ms, try and see
        wz = self.mainWiz
        waiting_check = self.counter.waiting_check
        already_check = self.counter.already_check
        # FSM
        if not self.checking:
            waiting_check += 1
            if waiting_check > secs(self.cam_param.sample_period)*20:
                self.checking = True
        else:
            already_check += 1
            if already_check > secs(self.cam_param.sample_duration)*20:
                self.checking = False

        # do check detected
        if self.checking:
            wz.cap_thread.do_start()
            wz.cap_thread.start()
            self.detect_thread.trigger.connect(self.check_detected)

        # determine if is working when finishing checking
        if already_check == secs(self.cam_param.sample_duration)*20:
            state = wz.timing.timer.state
            if self.counter.active_counts > 0.5 * secs(self.cam_param.sample_duration)*20:
                if state in ["idle"]:
                    wz.timing.timer.change_state(WORK)
            else:
                if state in ["work"]:
                    wz.timing.timer.change_state(IDLE)




    def if_timer_show(self):
        wz = self.mainWiz
        if wz.show_timer_cbox.isChecked():
            wz.timer_win.show()
        else:
            wz.timer_win.close()

    def show_mic(self):
        mic_win = self.mainWiz.mic_win
        mic_win.show()
        mic_win.OK.setEnabled(True)
        mic_win.overdraft.setEnabled(True)
        mic_win.reset.setEnabled(True)


    def take_mic(self):
        wz = self.mainWiz
        # wz.mic_win.close()
        # wz.mic_win.setWindowFlags(QtCore.Qt.WindowStaysOnTopHint)
        wz.mic_win.OK.setEnabled(False)
        wz.mic_win.overdraft.setEnabled(False)
        wz.mic_win.reset.setEnabled(False)
        wz.timing.timer.change_state(MIC_BREAK)

    def take_mic_post(self):
        wz = self.mainWiz
        wz.mic_win.close()
        wz.timing.timer.change_state("mic_over")


    def show_mac(self):
        mac_win = self.mainWiz.mac_win
        mac_win.show()
        mac_win.OK.setEnabled(True)
        mac_win.overdraft.setEnabled(True)
        mac_win.reset.setEnabled(True)

    def take_mac(self):
        wz = self.mainWiz
        # wz.mac_win.close()
        wz.timing.timer.change_state("mac_break")
        wz.mac_win.setWindowFlags(QtCore.Qt.WindowStaysOnTopHint)
        wz.mac_win.OK.setEnabled(False)
        wz.mac_win.overdraft.setEnabled(False)
        wz.mac_win.reset.setEnabled(False)

    def take_mac_post(self):
        wz = self.mainWiz
        wz.mac_win.close()
        wz.timing.timer.change_state("mac_over")

    def set_logic(self):
        wz = self.mainWiz

        wz.show_timer_cbox.stateChanged.connect(self.if_timer_show)
        wz.mic_win.OK.clicked.connect(self.take_mic)
        wz.mic_win.overdraft.clicked.connect(self.take_mic_post)
        wz.mac_win.OK.clicked.connect(self.take_mac)
        wz.mac_win.overdraft.clicked.connect(self.take_mac_post)
        wz.mic_win.reset.clicked.connect(wz.timing.timer.init_counter)
        wz.mac_win.reset.clicked.connect(wz.timing.timer.init_counter)



