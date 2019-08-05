import os
import sys
import cv2
import numpy as np

from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QFileDialog
from PyQt5.QtGui import *
from PyQt5.QtCore import *

class FileIO(QtWidgets.QWidget):
    def __init__(self, mainWiz):
        super(FileIO, self).__init__()
        self.mainWiz = mainWiz
        self.cached_img_flg = False
        self.img_cache = None

        self.cached_vid_flg = False
        self.vid_cache = None

        self.cam_showing = False

    def save_pic(self):
        fileName, ok = QFileDialog.getSaveFileName(self,
                                                     "save a picture",
                                                     "./",
                                                     "Pictures (*.jpg);;All Files (*)")
        img = self.img_cache
        path, filename = os.path.split(fileName)
        cv2.imwrite(os.path.join(path, "tmp.jpg"), img)
        if fileName:
            os.rename(os.path.join(path, "tmp.jpg"), fileName)

        self.test_cam()
        self.mainWiz.take_pic_push.setText("take a picture")
        self.cached_img_flg = False

        self.button_relation()


    def save_vid(self):
        wz = self.mainWiz
        wz.cap_thread.snap_shot()
        fileName, ok = QFileDialog.getSaveFileName(self,
                                                     "save a video",
                                                     "./",
                                                     "Videos (*.avi);;All Files (*)")
        wz.cap_thread.vid_writer.release()
        tmp_filename = wz.cap_thread.vid_filename
        if fileName:
            os.remove(fileName)
            os.rename(tmp_filename, fileName)

        self.test_cam()
        self.mainWiz.take_vid_push.setText("take a video")
        self.cached_vid_flg = False

        self.button_relation()

    def test_cam(self):
        wz = self.mainWiz
        wz.cap_thread.do_start()
        wz.cap_thread.start()
        if wz.param_setter.params.det:
            frame = wz.detect_thread.detect_frame(wz.cap_thread.frame)
        else:
            frame = wz.cap_thread.frame
        self.show_view(frame)

    def take_pic(self):
        wz = self.mainWiz
        if not self.cached_img_flg:
            wz.cap_thread.snap_shot()
            img = wz.cap_thread.frame
            if wz.param_setter.params.det:
                frame = wz.detect_thread.detect_frame(img)
            else:
                frame = img
            self.show_view(frame)
            wz.take_pic_push.setText("Cancel")
            self.img_cache = frame.copy()
            self.cached_img_flg = True
        else:
            self.test_cam()
            wz.take_pic_push.setText("take a picture")
            self.cached_img_flg = False

        self.button_relation()

    def take_vid(self):
        wz = self.mainWiz
        if not self.cached_vid_flg:
            wz.cap_thread.do_start()
            wz.cap_thread.start()
            wz.take_vid_push.setText("Cancel")
            self.cached_vid_flg = True
        else:
            self.test_cam()
            wz.take_vid_push.setText("take a video")
            self.cached_vid_flg = False

        self.button_relation()

    def show_view(self, frame):
        wz = self.mainWiz
        if frame.ndim == 3:
            # print("3 channel")
            rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        elif frame.ndim == 2:
            rgb = cv2.cvtColor(frame, cv2.COLOR_GRAY2BGR)
        size = wz.vid_view.geometry()
        # temp_image = QImage(rgb.data, size.width(), size.height(), QImage.Format_RGB888)
        temp_image = QImage(rgb, rgb.shape[1], rgb.shape[0], QImage.Format_RGB888)
        temp_pixmap_pre = QPixmap.fromImage(temp_image)
        pixmap = QPixmap(temp_pixmap_pre)
        wz.vid_view.setPixmap(pixmap.scaled(size.width(), size.height(), Qt.KeepAspectRatio))
        # rgb.data.clear()



    @pyqtSlot(object)
    def show_vid_frame(self, img):
        wz = self.mainWiz
        if wz.param_setter.params.det and wz.cap_thread.frame_idx % 1 == 0:
            # kernel = np.ones((5, 5), np.float32) / 25
            # frame = cv2.filter2D(img, -1, kernel)
            # frame = self.detect_thread.detect_frame(img)
            frame, _ = wz.detector.detect_frame(img)
        else:
            frame = img
        if self.cached_vid_flg:
            width, height = frame.shape[1], frame.shape[0]
            frame_vid = frame.copy()
            cv2.circle(frame_vid, (int(width * 0.2), int(height * 0.2)), 30, (0, 0, 255), -1)
            wz.cap_thread.vid_writer.write(frame)
        else:
            frame_vid = frame
        self.show_view(frame_vid)

    def button_relation(self):
        wz = self.mainWiz
        wz.save_pic_push.setEnabled(self.cached_img_flg)
        wz.save_vid_push.setEnabled(self.cached_vid_flg)
        if (not self.cached_img_flg) and (not self.cached_vid_flg):
            wz.test_cam_check.setEnabled(True)
        else:
            wz.test_cam_check.setEnabled(False)

        wz.take_pic_push.setEnabled(self.cam_showing)
        wz.take_vid_push.setEnabled(self.cam_showing)

    def show_cam(self):
        def show_static():
            self.show_view(wz.cap_thread.default_frame)

        wz = self.mainWiz
        if not self.cam_showing:
            self.cam_showing = True
            self.test_cam()
        else:
            self.cam_showing = False
            wz.cap_thread.stop = True
            # wz.cap_thread.snap_shot()
            wz.cap_thread.trigger.connect(show_static)

        self.button_relation()

    def set_logic(self):
        wz = self.mainWiz
        wz.take_pic_push.clicked.connect(self.take_pic)
        wz.save_pic_push.clicked.connect(self.save_pic)

        wz.take_vid_push.clicked.connect(self.take_vid)
        wz.cap_thread.changePixmap.connect(self.show_vid_frame)
        wz.save_vid_push.clicked.connect(self.save_vid)
        wz.test_cam_check.clicked.connect(self.show_cam)
