from sklearn.externals import joblib
from sklearn import svm
from face_recognition import face_locations, face_encodings
from PyQt5.QtGui import QPixmap, QImage
import socket
import xml.etree.ElementTree as EL
import numpy as np
from cv2.cv2 import *
import threading
import time
import dlib


path = "./sys.xml"
tree = EL.parse(path)
root = tree.getroot()
param_dict = dict()

for param in root.iter("param"):
    name = param.attrib['name']
    count = param.attrib['count']
    param_dict[name] = count

# parameters of system
RECOGNITION_FRAME = param_dict["recognition_frame"]
REGISTER_FRAME = param_dict["register_frame"]
AUTO_SLEEP_INTERIM = param_dict["auto_sleep_interim"]

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
                # start timer
                threading.Thread(target=Utility.camera_timer, args=(device, float(AUTO_SLEEP_INTERIM))).start()
                while True:
                    # capture frame
                    success, frame = device.read()
                    if not success:  # not captured  successfully
                        msg = "no frame was captured!"
                        print("no frame was captured!\nstop working...")
                        return
                    elif success:  # captured successfully
                        # data of frame
                        row = frame.shape[0]
                        col = frame.shape[1]
                        bytesPerLine = frame.shape[2] * col

                        # image processing
                        frame_flipped = flip(frame, 1)  # 0-vertical 1-horizontal -1-ver&hor
                        # thread of recognition
                        cvtColor(frame_flipped, COLOR_BGR2RGB, frame_flipped)

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


    @staticmethod
    def camera_timer(camera, seconds):
        """
        close the camera after some interim
        :param camera: the object of camera
        :param seconds: interim
        :return: none
        """

        print "start counting seconds..."
        time.sleep(seconds)
        # if there is a detected face pass
        # or not so, release the object of camera
        detector = dlib.get_frontal_face_detector()
        for i in range(3):
            ret, frame = camera.read()
            dets = detector(frame, 1)
            if len(dets) > 0:
                print "there is face detected, continue working..."
                threading.Thread(target=Utility.camera_timer, args=(camera, seconds)).start()
                break
        else:
            # no face was detected
            print "camera was closed..."
            camera.release()


    @staticmethod
    def read_param_from_xml():
        """
        parse the XML file for getting the parameters of system
        :return: params_dict that a dictionary containing the parameters of system
        """

        path = "./sys.xml"
        tree = EL.parse(path)
        root = tree.getroot()
        params_dict = dict()

        for param in root.iter("param"):
            name = param.attrib['name']
            count = param.attrib['count']
            params_dict[name] = count

        return params_dict

