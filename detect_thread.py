# -*- coding: utf-8 -*-

import cv2
import numpy as np
import os
import time
import sys
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *

global sec
sec = 0




class Detector(object):
    def __init__(self):
        super(Detector, self).__init__()
        modelFile = "models/opencv_face_detector_uint8.pb"
        configFile = "models/opencv_face_detector.pbtxt"
        self.net = cv2.dnn.readNetFromTensorflow(modelFile, configFile)

    @staticmethod
    def detectFaceOpenCVDnn(net, frame, conf_threshold):
        frameOpencvDnn = frame
        frameHeight = frameOpencvDnn.shape[0]
        frameWidth = frameOpencvDnn.shape[1]
        blob = cv2.dnn.blobFromImage(frameOpencvDnn, 1.0, (150, 150), [104, 117, 123], False, False)

        net.setInput(blob)
        detections = net.forward()
        bboxes = []
        for i in range(detections.shape[2]):
            confidence = detections[0, 0, i, 2]
            if confidence > conf_threshold:
                x1 = int(detections[0, 0, i, 3] * frameWidth)
                y1 = int(detections[0, 0, i, 4] * frameHeight)
                x2 = int(detections[0, 0, i, 5] * frameWidth)
                y2 = int(detections[0, 0, i, 6] * frameHeight)
                bboxes.append([x1, y1, x2, y2])
                cv2.rectangle(frameOpencvDnn, (x1, y1), (x2, y2), (0, 255, 0), int(round(frameHeight / 150)), 8)
        return frameOpencvDnn, bboxes

    def detect_frame(self, frame):
        outOpencvDnn, bboxes = self.detectFaceOpenCVDnn(self.net, frame, 0.6)
        return outOpencvDnn, bboxes



class WorkThread(QThread):
    trigger = pyqtSignal(object)

    def __init__(self):
        super(WorkThread, self).__init__()
        self.detector = Detector()
        self.frame = cv2.imread('obama.jpg')
        self.detected = cv2.imread('obama.jpg')
        print("work thread initialized")
        source = 0
        cap = cv2.VideoCapture(source)
        self.cap = cap
        self._boxes = None
        #

    @property
    def detected(self):
        return self._boxes

    @detected.setter
    def detected(self, box):
        self._boxes = box


    def set_frame(self, frame):
        self.frame = frame


    def detect_frame(self, frame):
        outOpencvDnn, bboxes = self.detector.detect_frame(frame)
        return outOpencvDnn


    def run(self):
        hasFrame, frame = self.cap.read()
        outOpencvDnn, bboxes = self.detector.detect_frame(frame)
        self.detected = bboxes

        # 完毕后发出信号
        self.trigger.emit(bboxes)


class CapThread(QThread):
    trigger = pyqtSignal()
    changePixmap = pyqtSignal(object)

    def __init__(self):
        super(CapThread, self).__init__()
        self.frame_idx = 0
        self.default_frame = cv2.imread('obama.jpg')
        self.frame = self.default_frame.copy()
        self.stop = False
        # self.changePixmap.connect(self.set_frame)

        source = 0
        home = os.environ['HOMEPATH']
        self.vid_filename = os.path.join(home, 'ttttttmpoutput-dnn-{}.avi'.format(str(source).split(".")[0]))

        if len(sys.argv) > 1:
            source = sys.argv[1]

        cap = cv2.VideoCapture(source)
        hasFrame, frame = cap.read()

        vid_writer = cv2.VideoWriter(self.vid_filename,
                                     cv2.VideoWriter_fourcc('M', 'J', 'P', 'G'), 30, (frame.shape[1], frame.shape[0]))
        self.cap = cap
        self.vid_writer = vid_writer
        print("cap thread initialized")

    # @pyqtSlot(object)
    def set_frame(self, frame):
        self.frame = frame

    def snap_shot(self):
        self.do_stop()
        hasFrame, frame = self.cap.read()
        assert hasFrame, "no frame captured!"
        self.set_frame(frame)

    def do_stop(self):
        self.stop = True

    def do_start(self):
        self.stop = False

    def run(self):
        while not self.stop:
            hasFrame, frame = self.cap.read()
            if not hasFrame:
                break
            self.frame_idx += 1
            if self.frame_idx > 10000:
                self.frame_idx = 0
            self.set_frame(frame)
            self.changePixmap.emit(frame)
        # 完毕后发出信号
        self.trigger.emit()
