from sklearn.externals import joblib
from sklearn import svm
from face_recognition import face_locations, face_encodings
from PyQt5.QtGui import QPixmap, QImage
import socket
import xml.etree.ElementTree
import numpy
from cv2.cv2 import *
import threading

# following functions in utilities class are scalable and pluggable
# process runs in backend

class Utility(object):
    """
    utilities
    """

    @staticmethod
    def open_camera(gui_frame):
        """
        open the camera and capture each frame to show on the GUI label
        :param gui_frame: the object of GUI label
        :return: none
        """
        # search the available device
        for i in range(4):
            device = VideoCapture(i)
            if device.isOpened():
                # device is available
                print("device connect successfully!")
                while True:
                    # capture frame
                    success, frame = device.read()
                    if not success:  # not captured  successfully
                        msg = "no frame was captured!"
                        print("no frame was captured!\nbreak...")
                        break
                    elif success:  # captured successfully
                        print("capture successfully!")

                        # data of frame
                        row = frame.shape[0]
                        col = frame.shape[1]
                        bytesPerLine = frame.shape[2] * col

                        # image processing
                        frame_flipped = flip(frame, 1)  # 0-vertical 1-horizontal -1-ver&hor
                        # thread of recognition
                        # cv2.cvtColor(frame_flipped, cv2.COLOR_BGR2RGB, frame_flipped)

                        gui_frame.setPixmap(QPixmap.fromImage(QImage(frame_flipped.data,
                                                                     col, row, bytesPerLine,
                                                                     QImage.Format_RGB888)).scaled(gui_frame.width(),
                                                                                                   gui_frame.height()))
            elif not device.isOpened():
                # device is not available
                msg = "device is not available!"
                print("device is not available!")
                device.release()
        else:
            # none of the devices is available
            msg = "none of the devices is available"
            print("none of the devices is available")
