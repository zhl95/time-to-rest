

from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QFileDialog, QWidget
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5 import QtCore
from easydict import EasyDict as edict
from pprint import pprint
from .helper import *



class MyTimer(QWidget):
    trigger = pyqtSignal()

    def __init__(self, mainWiz):
        super(MyTimer, self).__init__()
        self.state = "pause"
        # self.need_change_flag = False
        self.counter = edict()
        self.mainWiz = mainWiz

        self.init_counter()

        self.timer = QBasicTimer()  # QTimer()貌似不行，不知何故？
        # self.timer.start(1000, self)

        # 覆写计时器事件处理函数timerEvent()
        # if type == "mic":
        #     timeout = param.mic

    def start(self):
        self.state = WORK
        self.timer.start(1000, self)

    def init_counter(self):
        mic = edict()
        mic.work = 0
        mic.break_ = 0
        mic.overdraft = 0
        mic.idle = 0
        self.counter.mic = mic

        mac = edict()
        mac.work = 0
        mac.break_ = 0
        mac.overdraft = 0
        mac.idle = 0
        self.counter.mac = mac

        self.counter.total = 0
        # self.counter.check_idle = 0

    def timerEvent(self, event):
        self.trigger.emit()
        # pprint(self.counter)
        # pprint(self.mainWiz.param_setter.params.mic.work_duration)
        state = self.state
        param = self.mainWiz.param_setter.params
        wz = self.mainWiz

        if state == ["pause", "waiting"]:
            pass

        elif state == WORK:
            self.counter.mic.work += 1
            self.counter.mac.work += 1
            self.counter.total += 1
            self.counter.mic.idle = 0
            self.counter.mac.idle = 0

            if self.counter.mic.work > secs(param.mic.work_duration):
                # call MicWin
                self.state = IDLE
                wz.manager.show_mic()
                self.counter.mic.work = 0
            print(self.counter.mac.work, param.mac.work_duration)

            if self.counter.mac.work > secs(param.mac.work_duration):
                self.state = IDLE
                wz.manager.show_mac()
                self.counter.mac.work = 0

        elif state == MIC_BREAK:
            self.counter.mic.break_ += 1
            if self.counter.mic.break_ > secs(param.mic.break_duration):
                # call MicWin
                wz.mic_win.close()
                self.counter.mic.idle = 0
                self.counter.mic.break_ = 0
                self.state = WORK

        elif state == MAC_BREAK:
            self.counter.mac.break_ += 1
            if self.counter.mac.break_ > secs(param.mac.break_duration):
                # call MicWin
                wz.mac_win.close()
                self.counter.mac.idle = 0
                self.counter.mac.break_ = 0
                self.state = WORK

        elif state in [IDLE]:
            self.counter.mic.idle += 1
            self.counter.mac.idle += 1
            if self.counter.mic.idle > secs(param.mic.idle):
                self.counter.mic.work = 0
            if self.counter.mac.idle > secs(param.mac.idle):
                self.counter.mac.work = 0

        elif state in [MIC_OVER]:
            self.counter.mic.overdraft += 1
            self.counter.mac.work += 1
            self.counter.total += 1
            if self.counter.mic.overdraft > secs(param.mic.postpone):
                # call MicWin
                self.state = IDLE
                wz.manager.show_mic()
                self.counter.mic.work = 0

        elif state in [MAC_BREAK]:
            self.counter.mac.overdraft += 1
            self.counter.mic.work += 1
            self.counter.total += 1
            if self.counter.mac.overdraft > secs(param.mac.postpone):
                # call MicWin
                self.state = IDLE
                wz.manager.show_mac()
                self.counter.mac.work = 0



    def change_state(self, state):
        self.state = state

class Timing(QtWidgets.QWidget):
    def __init__(self, mainWiz):
        self.mainWiz = mainWiz
        wz = self.mainWiz
        super(Timing, self).__init__()
        self.timer = MyTimer(mainWiz)

        self.mic_work_pbar = MyProgress(wz.timer_win.mic_work_pbar)
        self.mac_work_pbar = MyProgress(wz.timer_win.mac_work_pbar)
        self.total_pbar = MyProgress(wz.timer_win.total_pbar)
        self.mic_work_pbar.set_style("green")
        self.mac_work_pbar.set_style("blue")
        self.total_pbar.set_style("yellow")

        self.mic_break_pbar = MyProgress(wz.mic_win.progressBar)
        self.mac_break_pbar = MyProgress(wz.mac_win.progressBar)

        self.mic_post_pbar = self.mic_work_pbar
        self.mac_post_pbar = self.mac_work_pbar
        self.mic_idle_pbar = self.mic_work_pbar
        self.mac_idle_pbar = self.mac_work_pbar

        self.param = self.mainWiz.param_setter.params

        # self.state = self.timer.state  # work, break, pause, overdraft, idle

    def set_pbar_max(self):
        state = self.timer.state
        if state == WORK:
            self.mic_work_pbar.set_max(secs(self.param.mic.work_duration))
            self.mac_work_pbar.set_max(secs(self.param.mac.work_duration))
        elif state == IDLE:
            self.mic_idle_pbar.set_max(secs(self.param.mic.idle))
            self.mac_idle_pbar.set_max(secs(self.param.mac.idle))
        elif state == MIC_OVER:
            self.mic_post_pbar.set_max(secs(self.param.mic.postpone))
        elif state == MAC_OVER:
            self.mac_post_pbar.set_max(secs(self.param.mac.postpone))

        self.total_pbar.set_max(secs(self.param.total_time))
        self.mic_break_pbar.set_max(secs(self.param.mic.break_duration))
        self.mac_break_pbar.set_max(secs(self.param.mac.break_duration))

    # def pbar_format(self):
    #     self.mic_work_pbar.set

    def set_pbar_val(self):
        state = self.timer.state
        counter = self.timer.counter
        if state == WORK:
            self.mic_work_pbar.set_val(counter.mic.work)
            self.mic_work_pbar.set_style("green")
            self.mic_work_pbar.set_format(sec2tuple(counter.mic.work))
            self.mac_work_pbar.set_val(counter.mac.work)
            self.mac_work_pbar.set_style("blue")
            self.mac_work_pbar.set_format(sec2tuple(counter.mac.work))
        elif state == MIC_BREAK:
            self.mic_break_pbar.set_val(counter.mic.break_)
        elif state == MAC_BREAK:
            self.mac_break_pbar.set_val(counter.mac.break_)
        elif state == MIC_OVER:
            self.mic_post_pbar.set_val(counter.mic.overdraft)
            self.mic_post_pbar.set_style("orange")
            self.mic_post_pbar.set_format(sec2tuple(counter.mic.overdraft))
            self.mac_work_pbar.set_val(counter.mac.work)
        elif state == MAC_OVER:
            self.mac_post_pbar.set_val(counter.mac.overdraft)
            self.mac_post_pbar.set_style("red")
            self.mac_post_pbar.set_format(sec2tuple(counter.mac.overdraft))
            self.mic_work_pbar.set_val(counter.mic.work)
        elif state == IDLE:
            self.mic_idle_pbar.set_val(counter.mic.idle)
            self.mic_idle_pbar.set_style("gray")
            self.mic_idle_pbar.set_format(sec2tuple(counter.mic.idle))
            self.mac_idle_pbar.set_val(counter.mac.idle)
            self.mac_idle_pbar.set_style("gray")
            self.mac_idle_pbar.set_format(sec2tuple(counter.mac.idle))

        self.total_pbar.set_val(counter.total)




    def set_logic(self):
        wz = self.mainWiz
        wz.param_setter.value_changed_signal.connect(self.set_pbar_max)
        self.timer.trigger.connect(self.set_pbar_val)
        self.timer.trigger.connect(self.set_pbar_max)
        # self.set_pbar_max()





