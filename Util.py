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
RECOGNITION_FRAME = param_dict["recognition_frame"] # the number of captured frames for recognition
REGISTER_FRAME = param_dict["register_frame"] # the number of captured frames for register
AUTO_SLEEP_INTERIM = param_dict["auto_sleep_interim"] # the seconds of interim
DETECT_FRAME = param_dict["detect_frame"] # the number of captured frames for detect

SWITCH = True # the status of camera - T => open F => close
DET_CACHE_SIGNAL = False # permission for saving detect cache
REC_CACHE_SIGNAL = False # permission for saving recognition cache
REG_CACHE_SIGNAL = False # permission for saving register cache

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
                global SWITCH
                SWITCH = True
                # start timer
                # threading.Thread(target=Utility.camera_timer, args=(device, float(AUTO_SLEEP_INTERIM))).start()
                threading.Thread(target=Utility.socket_transmission, args=("detect", )).start()

                NUM_RECOGNITION_CACHE = 0  # the number of saved frames for recognition
                NUM_DETECT_CACHE = 0  # the number of saved frames for detect
                NUM_SIGN_IN_CACHE = 0  # the number of saved frames for signing in

                while True:
                    if not SWITCH:
                        # close the camera
                        device.release()
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

                        # store cache of frames
                        global NUM_DETECT_CACHE
                        global NUM_RECOGNITION_CACHE
                        global NUM_SIGN_IN_CACHE
                        global DET_CACHE_SIGNAL
                        global REC_CACHE_SIGNAL
                        global REG_CACHE_SIGNAL
                        if DET_CACHE_SIGNAL:
                            print "save the cache of the frame for detect..."
                            img_path = ("./Cache/detect/det_cache_".join(NUM_DETECT_CACHE)).join(".jpg")
                            imwrite(img_path, frame)
                            NUM_DETECT_CACHE += 1
                            if NUM_DETECT_CACHE > int(DETECT_FRAME):
                                # have finished saving cache and init the var
                                DET_CACHE_SIGNAL = False
                                NUM_DETECT_CACHE = 0
                                # send msg -- saved cache and start detect
                                # threading.Thread()
                        if REC_CACHE_SIGNAL :
                            print "save the cache of the frame for recognition..."
                            img_path = ("./Cache/recognition/rec_cache_".join(NUM_RECOGNITION_CACHE)).join(".jpg")
                            imwrite(img_path, frame)
                            NUM_RECOGNITION_CACHE += 1
                            if NUM_RECOGNITION_CACHE > int(RECOGNITION_FRAME):
                                REC_CACHE_SIGNAL = False
                                NUM_RECOGNITION_CACHE = 0
                        if REG_CACHE_SIGNAL :
                            print "save the cache of the frame for signing in..."
                            img_path = ("./Cache/sign_in/sign_cache_".join(NUM_SIGN_IN_CACHE)).join(".jpg")
                            imwrite(img_path, frame)
                            NUM_SIGN_IN_CACHE += 1
                            if NUM_SIGN_IN_CACHE > int(REGISTER_FRAME):
                                REG_CACHE_SIGNAL = False
                                NUM_SIGN_IN_CACHE = 0

                        # show on the GUI
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
    def camera_timer(seconds):
        """
        close the camera after some interim
        :param seconds: interim
        :return: none
        """

        print "start counting seconds..."
        time.sleep(seconds)
        # if there is a detected face pass
        # or not so, release the object of camera
        # send msg -- start storing the cache
        detector = dlib.get_frontal_face_detector()
        threading.Thread(target=Utility.save_cache_of_frame, args=("detect", )).start()
        global NUM_DETECT_CACHE
        while not NUM_DETECT_CACHE == 0:
            print "saving the detect cache...wait..."
        global DETECT_FRAME
        for i in range(int(DETECT_FRAME)):
            img_path = ("./Cache/detect/det_cache_".join(i)).join(".jpg")
            frame = imread(img_path)
            dets = detector(frame, 1)
            if len(dets) > 0:
                print "there is face detected, continue working..."
                threading.Thread(target=Utility.camera_timer, args=(seconds, )).start()
                break
        else:
            # no face was detected
            print "camera was closed..."
            global SWITCH
            SWITCH = False

    @staticmethod
    def save_cache_of_frame(kind):
        """
        save the all kinds of frames in Cache directory for specific use
        :param kind: according to the task name, save the frames
        :return: none
        """

        if kind == "detect":
            # save the cache for detect
            global DET_CACHE_SIGNAL
            DET_CACHE_SIGNAL = True
        elif kind == "recognition":
            # save the cache for recognition
            global REC_CACHE_SIGNAL
            REC_CACHE_SIGNAL = True
        elif kind == "sign_in":
            # save the cache for register
            global REG_CACHE_SIGNAL
            REG_CACHE_SIGNAL = True



    @staticmethod
    def socket_transmission(task):
        """
        connected with backend via socket and transmit the information of task
        :param task: a string containing the name of task
        :return: none
        """

        obj = socket.socket()
        obj.connect(("127.0.0.1", 44967))

        ret_bytes = obj.recv(1024)
        ret_str = str(ret_bytes)
        if ret_str == "got":
            print "backend is working, keep accepting task..."
            obj.sendall(bytes(task))
            ret_bytes = obj.recv(1024)
            ret_str = str(ret_bytes)
            print "return the result:" + ret_str
        else:
            print "there is something wrong with backend...\nfail to connect"


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

