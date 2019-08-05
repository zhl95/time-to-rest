# -*- coding: utf-8 -*-
import cv2

import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QFileDialog
from PyQt5 import QtCore
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from ui.ui_window import Ui_MainWindow
# from . import detect_thread as detect
import detect_thread as detect

from easydict import EasyDict as edict
from pprint import pprint


class ParamSetter(QObject):
    value_changed_signal = pyqtSignal()
    def __init__(self, mainWiz):
        super(ParamSetter, self).__init__()
        self.mainWiz = mainWiz
        self.changed = False
        self.monitoring_panel()
        self.setup_param()

    def setup_param(self):
        self.params = edict()
        mic = edict()
        mic.work_duration = [0, 0, 0]
        mic.break_duration = [0, 0, 0]
        mic.postpone = [0, 0, 0]
        mic.idle = [0, 0, 0]
        self.params.mic = mic

        mac = edict()
        mac.work_duration = [0, 0, 0]
        mac.break_duration = [0, 0, 0]
        mac.postpone = [0, 0, 0]
        mac.idle = [0, 0, 0]
        self.params.mac = mac

        self.params.total_time = [0, 0, 0]

        camera = edict()
        camera.sample_period = [0, 0, 0]
        camera.sample_duration = [0, 0, 0]
        self.params.camera = camera

        algorithm = edict()
        algorithm.which = ""
        algorithm.thre = 0.
        algorithm.img_res = 0.
        self.params.algorithm = algorithm
        self.params.det = True
        self.params.test_cam = True

        self.default_values()

    def default_values(self):
        def set_hms(h_box, m_box, s_box, values):
            h_box.setProperty("value", values[0])
            m_box.setProperty("value", values[1])
            s_box.setProperty("value", values[2])

        ws = self.mainWiz
        set_hms(ws.work_h_mic, ws.work_m_mic, ws.work_s_mic, [0, 20, 0])
        set_hms(ws.break_h_mic, ws.break_m_mic, ws.break_s_mic, [0, 2, 0])
        set_hms(ws.post_h_mic, ws.post_m_mic, ws.post_s_mic, [0, 5, 0])
        set_hms(ws.idle_h_mic, ws.idle_m_mic, ws.idle_s_mic, [0, 3, 0])
        set_hms(ws.work_h_mac, ws.work_m_mac, ws.work_s_mac, [0, 50, 0])
        set_hms(ws.break_h_mac, ws.break_m_mac, ws.break_s_mac, [0, 10, 0])
        set_hms(ws.post_h_mac, ws.post_m_mac, ws.post_s_mac, [0, 10, 0])
        set_hms(ws.idle_h_mac, ws.idle_m_mac, ws.idle_s_mac, [0, 5, 0])
        set_hms(ws.sample_period_h, ws.sample_period_m, ws.sample_period_s, [0, 1, 0])
        set_hms(ws.sample_duration_h, ws.sample_duration_m, ws.sample_duration_s, [0, 0, 3])

        ws.total_time.setTime(QtCore.QTime(10, 0, 0))
        ws.param_box_tf.setProperty("value", 0.5)
        ws.img_resize_box.setProperty("value", 0.5)
        ws.rbut_tf.setChecked(True)
        # self.piclabel.setPixmap(QPixmap.fromImage(self.image))

        size = ws.vid_view.geometry()
        print(size, size.width())
        init_image = QPixmap("obama.jpg").scaled(size.width(), size.height())
        ws.vid_view.setPixmap(init_image)

    def value_changed(self):
        self.changed = True
        self.get_values()
        self.value_changed_signal.emit()


    def get_values(self):
        def QTime2hms(qtime):
            str_raw = str(qtime)
            h = str_raw.split(",")[-2]
            m = str_raw.split(",")[-1][:-1]
            return int(h), int(m), 0

        # self.break_s_mic.setProperty("value", 59)
        # print(self.work_m_mac.value())
        wz = self.mainWiz
        self.params.mic.work_duration = [wz.work_h_mic.value(),
                                         wz.work_m_mic.value(),
                                         wz.work_s_mic.value()]
        self.params.mic.break_duration = [wz.break_h_mic.value(),
                                          wz.break_m_mic.value(),
                                          wz.break_s_mic.value()]
        self.params.mic.postpone = [wz.post_h_mic.value(),
                                    wz.post_m_mic.value(),
                                    wz.post_s_mic.value()]
        self.params.mic.idle = [wz.idle_h_mic.value(),
                                wz.idle_m_mic.value(),
                                wz.idle_s_mic.value()]

        self.params.mac.work_duration = [wz.work_h_mac.value(),
                                         wz.work_m_mac.value(),
                                         wz.work_s_mac.value()]
        self.params.mac.break_duration = [wz.break_h_mac.value(),
                                          wz.break_m_mac.value(),
                                          wz.break_s_mac.value()]
        self.params.mac.postpone = [wz.post_h_mac.value(),
                                    wz.post_m_mac.value(),
                                    wz.post_s_mac.value()]
        self.params.mac.idle = [wz.idle_h_mac.value(),
                                wz.idle_m_mac.value(),
                                wz.idle_s_mac.value()]

        self.params.total_time = QTime2hms(wz.total_time.dateTime())

        self.params.camera.sample_period = [wz.sample_period_h.value(),
                                            wz.sample_period_m.value(),
                                            wz.sample_period_s.value()]
        self.params.camera.sample_duration = [wz.sample_duration_h.value(),
                                              wz.sample_duration_m.value(),
                                              wz.sample_duration_s.value()]

        self.params.algorithm.which = "tf"
        self.params.algorithm.thre = wz.param_box_tf.value()
        self.params.algorithm.img_res = wz.img_resize_box.value()

        self.params.det = wz.det_check.isChecked()
        # self.params.test_cam = wz.test_cam_check.isChecked()

        pprint(self.params)
        # print(str(self.params.total_time))
        # print(QTime2hms(self.params.total_time))

    def monitoring_panel(self):
        wz = self.mainWiz
        def monitor(itms):
            for itm in itms:
                itm.valueChanged.connect(self.value_changed)

        monitored = [wz.work_h_mic, wz.work_m_mic, wz.work_s_mic,
                     wz.break_h_mic, wz.break_m_mic, wz.break_s_mic,
                     wz.post_h_mic, wz.post_m_mic, wz.post_s_mic,
                     wz.work_h_mac, wz.work_m_mac, wz.work_s_mac,
                     wz.break_h_mac, wz.break_m_mac, wz.break_s_mac,
                     wz.post_h_mac, wz.post_m_mac, wz.post_s_mac,
                     wz.sample_period_h, wz.sample_period_m, wz.sample_period_s,
                     wz.sample_duration_h, wz.sample_duration_m, wz.sample_duration_s] + \
                    [wz.param_box_tf, wz.img_resize_box]
        monitor(monitored)

        wz.det_check.stateChanged.connect(self.value_changed)
        # wz.test_cam_check.stateChanged.connect(self.value_changed)
        # wz.total_time.valueChanged.connect(self.value_changed)





