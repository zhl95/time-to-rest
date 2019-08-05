import os
import sys
import cv2


WORK = "work"
IDLE = "idle"
MIC_OVER = "mic_over"
MAC_OVER = "mac_over"
MIC_BREAK = "mic_break"
MAC_BREAK = "mac_break"



color_map = {"green": "42cc81",
             "blue": "88B0EB",
             "red": "ff4500",
             "brown": "917d7d",
             "gray": "787878",
             "yellow": "FFFF00",
             "orange": "FFA500"}

def secs(hms_tuple):
    h, m, s = hms_tuple
    return h * 3600 + m * 60 + s


def sec2tuple(secs):
    h = secs // 3600
    m = (secs % 3600) // 60
    s = (secs % 3600) % 60
    return h, m, s


def hms_remain(secs, max_):
    if max_ is tuple:
        h_, m_, s_ = sec2tuple(secs)
        return max_[0] - h_, max_[1] - m_, max_[2] - s_
    elif max_ is int:
        return sec2tuple(max_ - secs)
    else:
        raise TypeError("only int and tuple (3) supported")



class MyProgress(object):


    def __init__(self, Pbar):
        super(MyProgress, self).__init__()
        self.Pbar = Pbar
        # self._text = None
        self._color = None

    # @property
    # def color(self):
    #     return self._color
    #
    # @color.setter
    # def color(self, color):
    #     self._color = MyProgress.color_map[color]

    # @property
    # def text(self):
    #     return self._text
    #
    # def set_text(self, text):
    #     self._text = text
    def set_max(self, max_):
        self.Pbar.setMaximum(max_)

    def set_val(self, val_):
        self.Pbar.setProperty("value", val_)

    # def set_style(self):
    #     style = """
    #             QProgressBar {
    #                 border: 2px solid grey;
    #                 border-radius: 5px;
    #                 text-align: center;
    #             }
    #             QProgressBar::chunk {
    #                 background-color: #%s;
    #                 width: 2px;
    #             }""" % self._color
    #     self.Pbar.setStyleSheet(style)

    def set_style(self, color):
        style = """
                QProgressBar {
                    border: 2px solid grey;
                    border-radius: 5px;
                    text-align: center;
                }
                QProgressBar::chunk {
                    background-color: #%s;
                    width: 2px;
                }""" % color_map[color]
        self.Pbar.setStyleSheet(style)

    def set_format(self, hms_remain):
        h, m, s = hms_remain
        self.Pbar.setFormat(f"{h}:{m}:{s}")